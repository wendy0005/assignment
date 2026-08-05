#include "secrets.h"

#define BLYNK_PRINT Serial

#include <Arduino.h>
#include <BlynkSimpleEsp32.h>
#include <DHT.h>
#include <ESP32Servo.h>
#include <WiFi.h>
#include <time.h>

// Physical pin allocation
constexpr uint8_t DHT_PIN = 15;
constexpr uint8_t PIR_PIN = 16;
constexpr uint8_t LDR_PIN = 34;
constexpr uint8_t MQ2_AOUT_PIN = 35;
constexpr uint8_t MQ2_DOUT_PIN = 17;
constexpr uint8_t LIGHT_RELAY_PIN = 23;
constexpr uint8_t FAN_RELAY_PIN = 22;
constexpr uint8_t NIGHT_LIGHT_PIN = 19;
constexpr uint8_t BUZZER_PIN = 18;
constexpr uint8_t RGB_RED_PIN = 25;
constexpr uint8_t RGB_GREEN_PIN = 26;
constexpr uint8_t RGB_BLUE_PIN = 27;
constexpr uint8_t CURTAIN_SERVO_PIN = 13;

// Blynk datastream contract
constexpr uint8_t VPIN_TEMPERATURE = V0;
constexpr uint8_t VPIN_HUMIDITY = V1;
constexpr uint8_t VPIN_ILLUMINANCE = V2;
constexpr uint8_t VPIN_GAS_VOLTAGE = V3;
constexpr uint8_t VPIN_OCCUPANCY = V4;
constexpr uint8_t VPIN_LIGHT_STATE = V5;
constexpr uint8_t VPIN_FAN_STATE = V6;
constexpr uint8_t VPIN_NIGHT_LIGHT_STATE = V7;
constexpr uint8_t VPIN_SYSTEM_STATUS = V8;
constexpr uint8_t VPIN_ACTION_REASON = V9;
constexpr uint8_t VPIN_MODE = V10;
constexpr uint8_t VPIN_LIGHT_OVERRIDE = V11;
constexpr uint8_t VPIN_FAN_OVERRIDE = V12;
constexpr uint8_t VPIN_CURTAIN_POSITION = V13;
constexpr uint8_t VPIN_ALERT_ACK = V14;

enum class OperatingMode : uint8_t { AUTO = 0, SLEEP = 1, STUDY = 2, AWAY = 3 };
enum class OverrideMode : uint8_t { AUTO = 0, FORCE_OFF = 1, FORCE_ON = 2 };

constexpr float FAN_ON_TEMPERATURE_C = 28.0F;
constexpr float FAN_OFF_TEMPERATURE_C = 26.0F;
constexpr float HUMIDITY_WARNING_ON = 70.0F;
constexpr float HUMIDITY_WARNING_OFF = 65.0F;
constexpr float LDR_GAMMA = 0.7F;
constexpr float LDR_RL10_KOHM = 50.0F;
constexpr float SENSOR_SUPPLY_VOLTAGE = 5.0F;
constexpr uint16_t LIGHT_THRESHOLD_DAY_LUX = 100;
constexpr uint16_t LIGHT_THRESHOLD_NIGHT_LUX = 30;
constexpr uint8_t GAS_CLEAR_READS_REQUIRED = 3;
constexpr unsigned long VACANCY_DAY_MS = 5000;   // Demo: production target is five minutes.
constexpr unsigned long VACANCY_NIGHT_MS = 2000; // Demo: production target is two minutes.
constexpr unsigned long WIFI_RETRY_MS = 10000;
constexpr unsigned long BLYNK_RETRY_MS = 10000;

DHT dht(DHT_PIN, DHT22);
Servo curtainServo;
BlynkTimer timer;

float temperatureC = NAN;
float humidityPercent = NAN;
float illuminanceLux = 0.0F;
float gasVoltage = 0.0F;
int lightRaw = 0;
int gasRaw = 0;
bool motionDetected = false;
bool motionEverDetected = false;
bool gasAlert = false;
bool humidityWarning = false;
bool sensorFault = false;
bool lightState = false;
bool fanState = false;
bool nightLightState = false;
bool alertAcknowledged = false;
bool connectedOnce = false;
uint8_t gasSafeReadCount = 0;
uint8_t curtainPosition = 0;
uint8_t currentHour = 12;
unsigned long lastMotionAt = 0;
unsigned long lastWiFiAttemptAt = 0;
unsigned long lastBlynkAttemptAt = 0;
OperatingMode operatingMode = OperatingMode::AUTO;
OverrideMode lightOverride = OverrideMode::AUTO;
OverrideMode fanOverride = OverrideMode::AUTO;
String systemStatus = "STARTING";
String actionReason = "Initialising sensors";

void publishReportedState();
void applyControlRules();

const char *modeName(OperatingMode mode) {
  switch (mode) {
    case OperatingMode::SLEEP: return "SLEEP";
    case OperatingMode::STUDY: return "STUDY";
    case OperatingMode::AWAY: return "AWAY";
    default: return "AUTO";
  }
}

void setRgb(bool red, bool green, bool blue) {
  digitalWrite(RGB_RED_PIN, red ? HIGH : LOW);
  digitalWrite(RGB_GREEN_PIN, green ? HIGH : LOW);
  digitalWrite(RGB_BLUE_PIN, blue ? HIGH : LOW);
}

float lightRawToLux(int rawValue) {
  const float voltage = rawValue / 4095.0F * SENSOR_SUPPLY_VOLTAGE;
  if (voltage <= 0.01F) return 100000.0F;
  if (voltage >= SENSOR_SUPPLY_VOLTAGE - 0.01F) return 0.0F;
  const float resistance = 2000.0F * voltage / (1.0F - voltage / SENSOR_SUPPLY_VOLTAGE);
  return pow(LDR_RL10_KOHM * 1000.0F * pow(10.0F, LDR_GAMMA) / resistance,
             1.0F / LDR_GAMMA);
}

bool isNightMode() {
  if (operatingMode == OperatingMode::SLEEP) return true;
  if (operatingMode == OperatingMode::STUDY) return false;
  return currentHour >= 23 || currentHour < 6;
}

bool isOccupied() {
  if (operatingMode == OperatingMode::STUDY) return true;
  if (operatingMode == OperatingMode::AWAY) return false;
  const unsigned long timeout = isNightMode() ? VACANCY_NIGHT_MS : VACANCY_DAY_MS;
  return motionEverDetected && millis() - lastMotionAt < timeout;
}

void writeActuators(bool mainLight, bool fan, bool nightLight) {
  lightState = mainLight;
  fanState = fan;
  nightLightState = nightLight;
  digitalWrite(LIGHT_RELAY_PIN, mainLight ? HIGH : LOW);
  digitalWrite(FAN_RELAY_PIN, fan ? HIGH : LOW);
  digitalWrite(NIGHT_LIGHT_PIN, nightLight ? HIGH : LOW);
}

void enterGasAlert() {
  gasAlert = true;
  alertAcknowledged = false;
  gasSafeReadCount = 0;
  systemStatus = "GAS ALERT";
  actionReason = "MQ-2 threshold active; safety override engaged";
  writeActuators(false, false, false);
  digitalWrite(BUZZER_PIN, HIGH);
  setRgb(true, false, false);
  Serial.println("!!! GAS ALERT: local outputs have priority !!!");
  if (Blynk.connected()) {
    Blynk.logEvent("gas_alert", String("Prototype MQ-2 alert at ") + gasVoltage + " V");
  }
}

void clearGasAlert() {
  gasAlert = false;
  digitalWrite(BUZZER_PIN, LOW);
  systemStatus = "SAFE";
  actionReason = "Gas input returned safe for three consecutive readings";
  setRgb(false, true, false);
  Serial.println("Gas alert cleared after stable safe readings");
}

void readSensors() {
  const float newTemperature = dht.readTemperature();
  const float newHumidity = dht.readHumidity();
  if (isnan(newTemperature) || isnan(newHumidity)) {
    if (!sensorFault && Blynk.connected()) {
      Blynk.logEvent("sensor_fault", "DHT22 returned an invalid reading");
    }
    sensorFault = true;
    systemStatus = "SENSOR FAULT";
    actionReason = "DHT22 reading invalid; last valid values retained";
  } else {
    sensorFault = false;
    temperatureC = newTemperature;
    humidityPercent = newHumidity;
  }

  lightRaw = analogRead(LDR_PIN);
  illuminanceLux = lightRawToLux(lightRaw);
  gasRaw = analogRead(MQ2_AOUT_PIN);
  gasVoltage = gasRaw / 4095.0F * SENSOR_SUPPLY_VOLTAGE;
  motionDetected = digitalRead(PIR_PIN) == HIGH;
  if (motionDetected) {
    motionEverDetected = true;
    lastMotionAt = millis();
  }

  const bool gasThresholdActive = digitalRead(MQ2_DOUT_PIN) == LOW;
  if (gasThresholdActive) {
    gasSafeReadCount = 0;
    if (!gasAlert) enterGasAlert();
  } else {
    if (gasSafeReadCount < GAS_CLEAR_READS_REQUIRED) gasSafeReadCount++;
    if (gasAlert && gasSafeReadCount >= GAS_CLEAR_READS_REQUIRED) clearGasAlert();
  }

  if (!isnan(humidityPercent) && humidityPercent >= HUMIDITY_WARNING_ON && !humidityWarning) {
    humidityWarning = true;
    if (Blynk.connected()) {
      Blynk.logEvent("humidity_warning", String("Humidity reached ") + humidityPercent + "%");
    }
  } else if (!isnan(humidityPercent) && humidityPercent <= HUMIDITY_WARNING_OFF) {
    humidityWarning = false;
  }

  Serial.printf("Sensors | T %.1f C | H %.1f %% | Light %.1f lux | Gas %.2f V | PIR %d\n",
                temperatureC, humidityPercent, illuminanceLux, gasVoltage, motionDetected);
  applyControlRules();
}

void applyControlRules() {
  if (gasAlert) {
    writeActuators(false, false, false);
    publishReportedState();
    return;
  }

  bool desiredLight = lightState;
  bool desiredFan = fanState;
  bool desiredNightLight = nightLightState;
  const bool occupied = isOccupied();
  const bool night = isNightMode();

  if (operatingMode == OperatingMode::AWAY) {
    desiredLight = false;
    desiredFan = false;
    desiredNightLight = false;
    actionReason = "Away mode disables comfort actuators; safety monitoring remains active";
  } else {
    if (lightOverride == OverrideMode::FORCE_ON) {
      desiredLight = true;
      desiredNightLight = false;
      actionReason = "Main light enabled by authenticated dashboard override";
    } else if (lightOverride == OverrideMode::FORCE_OFF) {
      desiredLight = false;
      desiredNightLight = false;
      actionReason = "Lighting disabled by authenticated dashboard override";
    } else if (night) {
      desiredLight = false;
      desiredNightLight = occupied && illuminanceLux < LIGHT_THRESHOLD_NIGHT_LUX;
      actionReason = desiredNightLight ? "Night light: occupied and dark" : "Night lighting idle";
    } else {
      desiredNightLight = false;
      desiredLight = occupied && illuminanceLux < LIGHT_THRESHOLD_DAY_LUX;
      actionReason = desiredLight ? "Main light: occupied and dark" : "Main light idle";
    }

    if (fanOverride == OverrideMode::FORCE_ON) {
      desiredFan = true;
      actionReason += "; fan manually enabled";
    } else if (fanOverride == OverrideMode::FORCE_OFF) {
      desiredFan = false;
      actionReason += "; fan manually disabled";
    } else if (!occupied) {
      desiredFan = false;
    } else if (!isnan(temperatureC) && temperatureC >= FAN_ON_TEMPERATURE_C) {
      desiredFan = true;
    } else if (!isnan(temperatureC) && temperatureC <= FAN_OFF_TEMPERATURE_C) {
      desiredFan = false;
    }
  }

  writeActuators(desiredLight, desiredFan, desiredNightLight);
  if (sensorFault) {
    systemStatus = "SENSOR FAULT";
    setRgb(false, false, true);
  } else if (humidityWarning) {
    systemStatus = "COMFORT WARNING";
    setRgb(true, true, false);
  } else {
    systemStatus = "SAFE";
    setRgb(false, true, false);
  }

  Serial.printf("Control | Mode %s | Light %d | Fan %d | Night %d | Curtain %u\n",
                modeName(operatingMode), lightState, fanState, nightLightState, curtainPosition);
  publishReportedState();
}

void publishTelemetry() {
  if (!Blynk.connected()) return;
  Blynk.beginGroup();
  if (!isnan(temperatureC)) Blynk.virtualWrite(VPIN_TEMPERATURE, temperatureC);
  if (!isnan(humidityPercent)) Blynk.virtualWrite(VPIN_HUMIDITY, humidityPercent);
  Blynk.virtualWrite(VPIN_ILLUMINANCE, illuminanceLux);
  Blynk.virtualWrite(VPIN_GAS_VOLTAGE, gasVoltage);
  Blynk.virtualWrite(VPIN_OCCUPANCY, isOccupied() ? 1 : 0);
  Blynk.endGroup();
  publishReportedState();
}

void publishReportedState() {
  if (!Blynk.connected()) return;
  Blynk.virtualWrite(VPIN_LIGHT_STATE, lightState ? 1 : 0);
  Blynk.virtualWrite(VPIN_FAN_STATE, fanState ? 1 : 0);
  Blynk.virtualWrite(VPIN_NIGHT_LIGHT_STATE, nightLightState ? 1 : 0);
  Blynk.virtualWrite(VPIN_SYSTEM_STATUS, systemStatus);
  Blynk.virtualWrite(VPIN_ACTION_REASON, actionReason);
  Blynk.virtualWrite(VPIN_CURTAIN_POSITION, curtainPosition);
  Blynk.virtualWrite(VPIN_ALERT_ACK, alertAcknowledged ? 1 : 0);
}

void maintainConnections() {
  const unsigned long now = millis();
  if (WiFi.status() != WL_CONNECTED && now - lastWiFiAttemptAt >= WIFI_RETRY_MS) {
    lastWiFiAttemptAt = now;
    Serial.println("Wi-Fi reconnect attempt; local automation remains active");
    WiFi.disconnect();
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD, 6);
  }
  if (WiFi.status() == WL_CONNECTED && !Blynk.connected() && now - lastBlynkAttemptAt >= BLYNK_RETRY_MS) {
    lastBlynkAttemptAt = now;
    Serial.println("Blynk reconnect attempt");
    Blynk.connect(1500);
  }
}

void updateClock() {
  struct tm timeInfo;
  if (getLocalTime(&timeInfo, 50)) currentHour = timeInfo.tm_hour;
}

BLYNK_CONNECTED() {
  Serial.println("Blynk connected: synchronising desired controls");
  Blynk.syncVirtual(VPIN_MODE, VPIN_LIGHT_OVERRIDE, VPIN_FAN_OVERRIDE,
                    VPIN_CURTAIN_POSITION, VPIN_ALERT_ACK);
  publishTelemetry();
  if (connectedOnce) Blynk.logEvent("device_reconnected", "SentinelSleep restored cloud connectivity");
  connectedOnce = true;
}

BLYNK_WRITE(V10) {
  operatingMode = static_cast<OperatingMode>(constrain(param.asInt(), 0, 3));
  applyControlRules();
}

BLYNK_WRITE(V11) {
  lightOverride = static_cast<OverrideMode>(constrain(param.asInt(), 0, 2));
  applyControlRules();
}

BLYNK_WRITE(V12) {
  fanOverride = static_cast<OverrideMode>(constrain(param.asInt(), 0, 2));
  applyControlRules();
}

BLYNK_WRITE(V13) {
  curtainPosition = static_cast<uint8_t>(constrain(param.asInt(), 0, 180));
  curtainServo.write(curtainPosition);
  actionReason = String("Curtain moved to ") + curtainPosition + " degrees by dashboard";
  publishReportedState();
}

BLYNK_WRITE(V14) {
  alertAcknowledged = param.asInt() == 1;
  if (alertAcknowledged && gasAlert) {
    actionReason = "Gas alert acknowledged; local alarm remains active until sensor is safe";
  }
  publishReportedState();
}

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
  pinMode(MQ2_DOUT_PIN, INPUT);
  pinMode(LIGHT_RELAY_PIN, OUTPUT);
  pinMode(FAN_RELAY_PIN, OUTPUT);
  pinMode(NIGHT_LIGHT_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(RGB_RED_PIN, OUTPUT);
  pinMode(RGB_GREEN_PIN, OUTPUT);
  pinMode(RGB_BLUE_PIN, OUTPUT);
  writeActuators(false, false, false);
  digitalWrite(BUZZER_PIN, LOW);
  setRgb(false, false, true);

  curtainServo.setPeriodHertz(50);
  curtainServo.attach(CURTAIN_SERVO_PIN, 500, 2400);
  curtainServo.write(curtainPosition);
  dht.begin();

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD, 6);
  Blynk.config(BLYNK_AUTH_TOKEN);
  configTime(8 * 3600, 0, "pool.ntp.org", "time.nist.gov");

  timer.setInterval(2000L, readSensors);
  timer.setInterval(10000L, publishTelemetry);
  timer.setInterval(1000L, maintainConnections);
  timer.setInterval(60000L, updateClock);
  Serial.println("SentinelSleep ready: local rules start before cloud connection");
}

void loop() {
  if (Blynk.connected()) Blynk.run();
  timer.run();
  delay(5);
}

