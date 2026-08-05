# Blynk Template Setup — SentinelSleep

Use Blynk Developer Mode to create a template named **SentinelSleep** with hardware **ESP32** and connection type **WiFi**. Create a device from the template named **SentinelSleep-SUOL2500321**, then copy its template ID and device auth token into the private `include/secrets.h` file.

## Live cloud configuration (verified 5 August 2026)

- Region: **SGP1**
- Template: **SentinelSleep**
- Template ID: **TMPL6tkq1B_ye**
- Device: **SentinelSleep-SUOL2500321**
- Device URI: **device://4153170**
- Web dashboard: **Saved and applied**
- Device credentials: stored only in the ignored `include/secrets.h`; the auth token is intentionally omitted from this document.
- Project MCP connection: configured in the repository-scoped `.codex/config.toml` using Blynk OAuth.

The live template was verified through Blynk MCP after creation: all V0–V14 datastreams and the four event definitions below are present.

## Datastreams

| Name | Pin | Type | Min | Max | Unit | History |
|---|---:|---|---:|---:|---|---|
| Temperature | V0 | Double | 0 | 60 | °C | On |
| Humidity | V1 | Double | 0 | 100 | % | On |
| Illuminance | V2 | Double | 0 | 100000 | lux | On |
| Gas Voltage | V3 | Double | 0 | 5 | V | On |
| Occupancy | V4 | Integer | 0 | 1 | — | On |
| Main Light State | V5 | Integer | 0 | 1 | — | On |
| Fan State | V6 | Integer | 0 | 1 | — | On |
| Night Light State | V7 | Integer | 0 | 1 | — | On |
| System Status | V8 | String | — | — | — | Off |
| Action Reason | V9 | String | — | — | — | Off |
| Operating Mode | V10 | Enumerable | 0 | 3 | — | Off |
| Light Override | V11 | Enumerable | 0 | 2 | — | Off |
| Fan Override | V12 | Enumerable | 0 | 2 | — | Off |
| Curtain Position | V13 | Integer | 0 | 180 | degrees | On |
| Alert Acknowledged | V14 | Integer | 0 | 1 | — | On |

Enumerable rows:

- V10: `0 Auto`, `1 Sleep`, `2 Study`, `3 Away`.
- V11 and V12: `0 Auto`, `1 Off`, `2 On`.

## Events

| Event code | Severity | Notification purpose |
|---|---|---|
| `gas_alert` | Critical | Supplementary MQ-2 threshold warning |
| `humidity_warning` | Warning | Relative humidity reached 70% |
| `sensor_fault` | Warning | DHT22 returned an invalid reading |
| `device_reconnected` | Information | Cloud session restored after interruption |

Apply notification limits so one continuing condition cannot repeatedly notify the examiner. The firmware also latches gas/humidity conditions locally.

## Web dashboard

Create a device-template dashboard containing:

1. Value widgets for V0–V3.
2. Indicator widgets for V4–V7, with the V14 button label showing READY/ACK state.
3. Text/label widgets for V8 and V9.
4. A combined temperature/humidity trend chart using V0 and V1.
5. A mode selector on V10.
6. Light and fan selectors on V11 and V12.
7. A 0–180 slider on V13.
8. An acknowledgement button on V14.

The applied web dashboard contains:

- V0–V3 reading labels;
- V4–V7 state indicators;
- V8/V9 status labels;
- a V10 Auto/Sleep/Study/Away segmented selector;
- V11 and V12 Auto/Off/On menus;
- a V13 0–180° curtain slider;
- a V14 READY/ACK push button; and
- a combined **Bedroom Environment Trends** chart for V0 and V1.

Use the actual device view—not the template editor—to capture live evidence.

## Mobile dashboard

Configure equivalent widgets in Blynk.App because mobile and web widgets are maintained independently even when they share datastreams. Put system status and alerts at the top, readings/trends in the middle, and controls at the bottom.

## Evidence capture

- Hide the template ID/auth token before recording or taking screenshots.
- Show the device as online.
- Show Wokwi and Blynk side by side when changing a sensor or control.
- Capture the event timeline after the gas, humidity and reconnect tests.
- Record the final values in `../evidence/20260805_Implementation_Test_Matrix.md`.
