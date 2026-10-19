# SentinelSleep Final Project

ESP32 smart-bedroom simulation for BCL1123 Internet of Things. The controller combines DHT22 temperature/humidity, PIR occupancy, ambient light and MQ-2 prototype gas sensing with light, fan, night-light, RGB, buzzer and curtain-servo outputs. Local rules continue when cloud connectivity is unavailable.

## Setup

1. Copy `include/secrets.example.h` to `include/secrets.h`.
2. Insert the Blynk template ID, device auth token and Wi-Fi credentials.
3. Run `pio run` in VS Code/PlatformIO.
4. Open the folder with the Wokwi VS Code extension and start the simulation.
5. Open the SentinelSleep device dashboard in Blynk Console or Blynk.App.

The committed example file contains no working credentials. The private submission package includes the examiner access instructions in the root `readme.txt`.

## Dashboard contract

| Pin | Direction | Name | Type / range |
|---|---|---|---|
| V0 | Device to cloud | Temperature | Double, 0–60 °C |
| V1 | Device to cloud | Humidity | Double, 0–100% |
| V2 | Device to cloud | Illuminance | Double, 0–100000 lux |
| V3 | Device to cloud | Gas sensor voltage | Double, 0–5 V |
| V4 | Device to cloud | Occupancy | Integer, 0/1 |
| V5 | Device to cloud | Main light state | Integer, 0/1 |
| V6 | Device to cloud | Fan state | Integer, 0/1 |
| V7 | Device to cloud | Night-light state | Integer, 0/1 |
| V8 | Device to cloud | System status | String |
| V9 | Device to cloud | Action reason | String |
| V10 | Bidirectional | Operating mode | Enum: 0 Auto, 1 Sleep, 2 Study, 3 Away |
| V11 | Bidirectional | Light override | Enum: 0 Auto, 1 Off, 2 On |
| V12 | Bidirectional | Fan override | Enum: 0 Auto, 1 Off, 2 On |
| V13 | Bidirectional | Curtain position | Integer, 0–180 degrees |
| V14 | Bidirectional | Alert acknowledged | Integer, 0/1 |

Template events: `gas_alert`, `humidity_warning`, `sensor_fault`, and `device_reconnected`.

## Safety boundary

The MQ-2 path is a simulation and learning feature. It is not a certified smoke, carbon-monoxide or combustible-gas alarm. An active gas input overrides dashboard controls, activates local warning outputs, and can only clear after three consecutive safe sensor readings.

