#include <WiFi.h>
#include <DHT.h>
#include <PubSubClient.h>
#include <time.h>

#define DHTPIN 15
#define DHTTYPE DHT22
#define PIR_PIN 16
#define LDR_PIN 34
#define MQ2_AOUT 35
#define MQ2_DOUT 17
#define LIGHT_RELAY 23
#define FAN_RELAY 22
#define NIGHT_LIGHT 19
#define BUZZER 18
#define RGB_R 25
#define RGB_G 26
#define RGB_B 27
#define SERVO_PIN 13

const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* mqttServer = "broker.emqx.io";
const int mqttPort = 1883;
String clientId;

const char* topicTelemetry = "sentinelsleep/SUOL2500321/telemetry";
const char* topicState = "sentinelsleep/SUOL2500321/state";
const char* topicAlert = "sentinelsleep/SUOL2500321/alert";

const int LIGHT_THRESHOLD_DAY = 100;
const int LIGHT_THRESHOLD_NIGHT = 30;
const float FAN_ON_TEMP = 28.0;
const float FAN_OFF_TEMP = 26.0;
const float HUMIDITY_WARN = 70.0;
const int GAS_CLEAR_READS = 3;
const unsigned long VACANCY_MS = 5000;
const unsigned long VACANCY_NIGHT_MS = 2000;
const unsigned long SIMULATED_HOUR_MS = 60000;

// Wokwi photoresistor model values (must match the part attributes).
const float LDR_GAMMA = 0.7;
const float LDR_RL10 = 50.0;
const float SENSOR_SUPPLY_VOLTAGE = 5.0;
const float GAS_DOUT_THRESHOLD_V = 4.8; // Must match gas1.threshold in diagram.json.

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
DHT dht(DHTPIN, DHTTYPE);

bool motionDetected = false;
bool motionEverDetected = false;
unsigned long lastMotionTime = 0;
bool lightState = false;
bool fanState = false;
bool nightLightState = false;
bool gasAlert = false;
float lastTemp = 0;
float lastHumidity = 0;
int lastLightRaw = 0;
float lastLightLux = 0;
int lastGasLevel = 0;
int gasSafeReadCount = 0;
unsigned long lastPublishTime = 0;
unsigned long lastSensorReadTime = 0;
unsigned long lastSimulatedHourTime = 0;
int currentHour = 12;
bool timeSynced = false;

// ----- WiFi -----
void setupWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println(" OK");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println(" FAIL (local mode)");
  }
}

// ----- NTP -----
void syncTime() {
  if (!WiFi.isConnected()) return;
  configTime(28800, 0, "pool.ntp.org", "time.nist.gov");
  struct tm timeinfo;
  int attempts = 0;
  while (!getLocalTime(&timeinfo) && attempts < 10) {
    delay(500);
    attempts++;
  }
  if (getLocalTime(&timeinfo)) {
    currentHour = timeinfo.tm_hour;
    timeSynced = true;
    Serial.printf("NTP: %02d:%02d\n", timeinfo.tm_hour, timeinfo.tm_min);
  } else {
    Serial.println("NTP failed, using simulated time");
  }
}

// ----- MQTT -----
void setupMQTT() {
  mqttClient.setServer(mqttServer, mqttPort);
}

bool connectMQTT() {
  if (!WiFi.isConnected()) return false;
  if (mqttClient.connected()) return true;
  Serial.print("MQTT...");
  const char* offlineState = "{\"device\":\"sentinelsleep\",\"status\":\"offline\"}";
  if (mqttClient.connect(clientId.c_str(), topicState, 0, true, offlineState)) {
    Serial.println(" connected");
    mqttClient.publish(topicState, "{\"device\":\"sentinelsleep\",\"status\":\"online\"}", true);
    return true;
  }
  Serial.print(" fail ");
  Serial.println(mqttClient.state());
  return false;
}

void publishAlert(const char* msg) {
  if (!connectMQTT()) return;
  mqttClient.publish(topicAlert, msg);
}

void publishState() {
  if (!connectMQTT()) return;
  char buf[320];
  snprintf(buf, sizeof(buf),
    "{\"t\":%.1f,\"h\":%.1f,\"lux\":%.1f,\"ldrRaw\":%d,\"gasRaw\":%d,\"pir\":%d,\"light\":%d,\"fan\":%d,\"night\":%d,\"alert\":%d}",
    lastTemp, lastHumidity, lastLightLux, lastLightRaw, lastGasLevel,
    motionDetected, lightState, fanState, nightLightState, gasAlert);
  mqttClient.publish(topicTelemetry, buf);
}

// ----- RGB -----
void rgbWrite(bool r, bool g, bool b) {
  digitalWrite(RGB_R, r);
  digitalWrite(RGB_G, g);
  digitalWrite(RGB_B, b);
}

void rgbColor(const char* c) {
  if      (strcmp(c, "red")    == 0) rgbWrite(HIGH, LOW,  LOW);
  else if (strcmp(c, "green")  == 0) rgbWrite(LOW,  HIGH, LOW);
  else if (strcmp(c, "blue")   == 0) rgbWrite(LOW,  LOW,  HIGH);
  else if (strcmp(c, "yellow") == 0) rgbWrite(HIGH, HIGH, LOW);
  else if (strcmp(c, "cyan")   == 0) rgbWrite(LOW,  HIGH, HIGH);
  else                               rgbWrite(LOW,  LOW,  LOW);
}

// ----- Gas Alert (highest priority) -----
void enterGasAlert() {
  gasAlert = true;
  rgbColor("red");
  digitalWrite(BUZZER, HIGH);
  digitalWrite(LIGHT_RELAY, LOW);
  digitalWrite(FAN_RELAY, LOW);
  digitalWrite(NIGHT_LIGHT, LOW);
  lightState = false;
  fanState = false;
  nightLightState = false;
  Serial.println("!!! GAS ALERT !!!");
  publishAlert("GAS_ALERT");
}

void exitGasAlert() {
  gasAlert = false;
  digitalWrite(BUZZER, LOW);
  rgbColor("green");
  Serial.println("Gas cleared");
  publishAlert("GAS_CLEARED");
}

// ----- Sensors -----
float lightRawToLux(int rawValue) {
  float voltage = rawValue / 4095.0 * SENSOR_SUPPLY_VOLTAGE;
  if (voltage <= 0.01) return 100000.0;
  if (voltage >= SENSOR_SUPPLY_VOLTAGE - 0.01) return 0.0;

  float resistance = 2000.0 * voltage / (1.0 - voltage / SENSOR_SUPPLY_VOLTAGE);
  return pow(LDR_RL10 * 1000.0 * pow(10.0, LDR_GAMMA) / resistance, 1.0 / LDR_GAMMA);
}

void readSensors() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  if (isnan(t) || isnan(h)) {
    Serial.println("DHT ERR");
    return;
  }
  lastTemp = t;
  lastHumidity = h;
  lastLightRaw = analogRead(LDR_PIN);
  lastLightLux = lightRawToLux(lastLightRaw);
  lastGasLevel = analogRead(MQ2_AOUT);
  motionDetected = digitalRead(PIR_PIN) == HIGH;
  if (motionDetected) {
    motionEverDetected = true;
    lastMotionTime = millis();
  }

  int gasDigitalRaw = digitalRead(MQ2_DOUT);
  float gasVoltage = lastGasLevel / 4095.0 * SENSOR_SUPPLY_VOLTAGE;

  Serial.println("=== SENSORS ===");
  Serial.printf("Temp:%.1fC  Hum:%.1f%%  Light:%.1flux(%d raw)  Gas:%d(A)=%.2fV  %d(D)  PIR:%d\n",
    t, h, lastLightLux, lastLightRaw, lastGasLevel, gasVoltage, gasDigitalRaw, motionDetected);

  bool gasDigital = gasDigitalRaw == LOW; // Wokwi MQ-2 DOUT is active LOW.
  if (gasDigital) {
    gasSafeReadCount = 0;
    if (!gasAlert) enterGasAlert();
  } else {
    if (gasSafeReadCount < GAS_CLEAR_READS) gasSafeReadCount++;
    if (gasAlert && gasSafeReadCount >= GAS_CLEAR_READS) exitGasAlert();
  }
}

// ----- Actuators -----
void controlActuators() {
  if (gasAlert) return;

  unsigned long now = millis();
  bool occupied = motionEverDetected && (now - lastMotionTime) < VACANCY_MS;
  bool night = (currentHour >= 23 || currentHour < 6);

  // Light
  if (night) {
    if (occupied && lastLightLux < LIGHT_THRESHOLD_NIGHT) {
      digitalWrite(NIGHT_LIGHT, HIGH);
      digitalWrite(LIGHT_RELAY, LOW);
      nightLightState = true; lightState = false;
    } else if (!occupied && (now - lastMotionTime) > VACANCY_NIGHT_MS) {
      digitalWrite(NIGHT_LIGHT, LOW);
      nightLightState = false;
    }
  } else {
    if (occupied && lastLightLux < LIGHT_THRESHOLD_DAY) {
      digitalWrite(LIGHT_RELAY, HIGH);
      lightState = true;
      digitalWrite(NIGHT_LIGHT, LOW);
      nightLightState = false;
    } else if (!occupied) {
      digitalWrite(LIGHT_RELAY, LOW);
      lightState = false;
    }
  }

  // Fan (hysteresis)
  if (occupied && lastTemp >= FAN_ON_TEMP) {
    digitalWrite(FAN_RELAY, HIGH);
    fanState = true;
  } else if (!occupied || lastTemp <= FAN_OFF_TEMP) {
    digitalWrite(FAN_RELAY, LOW);
    fanState = false;
  }

  // RGB status
  if (!gasAlert) {
    if (lastHumidity > HUMIDITY_WARN) rgbColor("yellow");
    else rgbColor("green");
  }

  Serial.println("=== ACTUATORS ===");
  Serial.printf("Light:%s  Fan:%s  Night:%s  RGB:%s\n",
    lightState?"ON":"OFF", fanState?"ON":"OFF", nightLightState?"ON":"OFF",
    gasAlert?"RED":(lastHumidity>HUMIDITY_WARN?"YELLOW":"GREEN"));
}

// ===== SETUP =====
void setup() {
  Serial.begin(115200);
  clientId = "sentinelsleep-SUOL2500321-" + String((uint32_t)ESP.getEfuseMac(), HEX);

  pinMode(PIR_PIN, INPUT);
  pinMode(MQ2_DOUT, INPUT);
  pinMode(LIGHT_RELAY, OUTPUT);
  pinMode(FAN_RELAY, OUTPUT);
  pinMode(NIGHT_LIGHT, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  pinMode(RGB_R, OUTPUT);
  pinMode(RGB_G, OUTPUT);
  pinMode(RGB_B, OUTPUT);
  pinMode(SERVO_PIN, OUTPUT);

  digitalWrite(LIGHT_RELAY, LOW);
  digitalWrite(FAN_RELAY, LOW);
  digitalWrite(NIGHT_LIGHT, LOW);
  digitalWrite(BUZZER, LOW);
  rgbColor("green");

  dht.begin();
  setupWiFi();
  syncTime();
  setupMQTT();
  connectMQTT();
  Serial.println("MQTT transport: Wokwi demo TCP; production design uses TLS");
  Serial.printf("MQ-2 DOUT threshold: %.2fV (DOUT is LOW above threshold)\n", GAS_DOUT_THRESHOLD_V);

  Serial.println("\n===== SentinelSleep Ready =====");
}

// ===== LOOP =====
void loop() {
  unsigned long now = millis();

  if (WiFi.isConnected()) {
    if (!mqttClient.connected()) connectMQTT();
    mqttClient.loop();
  }

  // Simulate time if NTP unavailable (1 min = 1 hour)
  if (!timeSynced && now - lastSimulatedHourTime >= SIMULATED_HOUR_MS) {
    currentHour = (currentHour + 1) % 24;
    lastSimulatedHourTime = now;
    Serial.printf("Sim time: %02d:00\n", currentHour);
  }

  if (now - lastSensorReadTime >= 2000) {
    readSensors();
    controlActuators();
    lastSensorReadTime = now;
  }

  if (now - lastPublishTime >= 10000) {
    publishState();
    lastPublishTime = now;
  }

  delay(50);
}
