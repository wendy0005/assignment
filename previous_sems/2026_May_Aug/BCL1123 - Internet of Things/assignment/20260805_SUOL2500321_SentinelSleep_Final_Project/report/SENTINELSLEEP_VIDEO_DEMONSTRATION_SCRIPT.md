# SentinelSleep Video Demonstration Script

## 1. Introduction

**Show:** The project title, Blynk device name and Wokwi circuit.

**Say:**

> This is SentinelSleep, an ESP32 smart-bedroom IoT system. It monitors temperature, humidity, illuminance, occupancy and gas safety, while controlling the light, fan, night light and curtain.

## 2. Baseline operation

**Show in Blynk:**

- Device Online
- Temperature approximately 27.3°C
- Humidity 65%
- Illuminance approximately 499 lx
- Gas voltage approximately 4.43V
- SAFE status
- Comfort outputs off

**Show in Wokwi:** The normal circuit with outputs inactive.

**Say:**

> The system is online and operating safely under normal conditions. The environmental readings are stable, gas voltage is safe, and the comfort outputs are currently off.

## 3. Humidity warning

**Show:** Raise the DHT22 humidity to 72.5%. Display `COMFORT WARNING` in Blynk and the red-plus-green RGB warning indication in Wokwi.

**Say:**

> When humidity rises above the 70 percent threshold, SentinelSleep changes the system status to Comfort Warning. The Blynk dashboard reports the warning and the Wokwi RGB indicator shows the warning colour.

## 4. Gas alert and acknowledgement

**Show:** Increase the MQ-2 value until the alert activates. Display `GAS ALERT`, approximately 4.81V and 6918 ppm in Blynk, plus the red alarm indicator and buzzer in Wokwi. Press Acknowledge Alert and show the acknowledgement reason while the alert remains active.

**Say:**

> When the MQ-2 threshold is reached, gas safety takes priority over comfort controls. The dashboard reports Gas Alert, while Wokwi activates the red indicator and buzzer. Acknowledging the alert records the acknowledgement, but does not clear the active safety alarm.

## 5. Sleep mode

**Show:** Select Sleep, set illuminance below 30 lux and trigger the PIR. Display approximately 25.12 lx, Occupancy active and Night Light active in Blynk. Show the Wokwi night-light indicator active with the main light and fan off.

**Say:**

> In Sleep mode, a dark occupied room activates the night light. The main light and fan remain off, which provides low-level lighting suitable for sleeping.

## 6. Study mode

**Show:** Select Study, set temperature to approximately 30.2°C and illuminance below 100 lux. Display Study selected, Occupancy active, Main Light active and Fan active in Blynk. Show the Wokwi main-light and fan indicators active.

**Say:**

> Study mode treats the room as occupied. Under low-light and warm conditions, the main light and fan are activated automatically.

## 7. Away mode

**Show:** Select Away. Display `Away mode disabled` in Blynk, with Occupancy, Main Light, Fan and Night Light off. Show the corresponding Wokwi outputs inactive.

**Say:**

> Away mode disables the comfort outputs, even if sensor conditions would normally request them. This prevents unnecessary operation while the room is unoccupied.

## 8. Light Override On

**Show:** Set Operating Mode to Auto and Light Override to On. Display the Main Light indicator active in Blynk and the main-light LED and relay active in Wokwi.

**Say:**

> The Light Override On command manually enables the main light, and the confirmed dashboard state matches the Wokwi output.

## 9. Fan Override On

**Show:** Keep Operating Mode at Auto and set Fan Override to On. Display Fan Override On and the Fan indicator active in Blynk, with the Wokwi fan LED and relay active.

**Say:**

> The Fan Override On command manually enables the fan. The Blynk confirmed state and Wokwi output agree.

## 10. Closing

**Show:** The Blynk dashboard and Wokwi circuit together.

**Say:**

> These tests demonstrate normal monitoring, environmental warnings, gas-safety priority, operating modes and manual overrides. SentinelSleep combines local ESP32 control with Blynk cloud monitoring while keeping safety decisions active at the device.
