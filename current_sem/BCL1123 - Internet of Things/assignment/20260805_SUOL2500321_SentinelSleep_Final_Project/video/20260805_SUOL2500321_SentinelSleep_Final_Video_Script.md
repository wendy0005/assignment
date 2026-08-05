# SentinelSleep Final Demonstration Script

Target duration: **12–14 minutes**. The presenter’s face must remain visible throughout, including screen demonstrations. Use a picture-in-picture camera layout rather than cutting to a full-screen recording without the presenter.

## 0:00–0:45 — Introduction

**Show:** Title, face camera, student name and ID.

“Hello, I am Chan Jing Yi, student ID SUOL2500321. This is my BCL1123 Internet of Things final project, SentinelSleep. It implements my smart-bedroom proposal using an ESP32 simulation in Wokwi and an authenticated Blynk dashboard. I will demonstrate the hardware integration, local rules, cloud data, controls, security measures and failure behavior.”

## 0:45–1:45 — Environment and objective

**Show:** Bedroom and switch-panel photographs.

Explain that the bedroom supports sleeping and study, while its existing controls cannot combine occupancy, brightness, temperature, mode and safety. State that the prototype coordinates these conditions without using a bedroom camera or microphone.

## 1:45–3:00 — Wokwi hardware

**Show:** Full Wokwi circuit, then zoom into each input/output.

Identify the DHT22, PIR, photoresistor, MQ-2, light and fan relays, night light, RGB indicators, buzzer and curtain servo. Mention the exact ESP32 pins only when pointing at the corresponding wires. Explain that the relay and MQ-2 paths are simulations and not certified physical safety equipment.

## 3:00–4:00 — Architecture and cloud contract

**Show:** Figure 4 architecture, then Blynk device dashboard.

Explain the path from sensors to the ESP32, through Wokwi Wi-Fi to Blynk virtual datastreams, and into the web/mobile interface. Point out that V10–V14 carry desired controls while V5–V9 report confirmed state and reasons.

## 4:00–5:20 — Normal lighting test

**Show:** Wokwi and Blynk side by side.

1. Start with 500 lux and no motion; show that lighting is off.
2. Reduce light below 100 lux and trigger PIR motion.
3. Show the main-light output and confirm V4/V5 plus the action reason on Blynk.
4. Stop motion and wait for the shortened five-second demonstration timeout.

Explain that production timing would be longer; the short timeout makes the live logic observable within the assessment video.

## 5:20–6:35 — Temperature, fan and humidity

1. Trigger occupancy and set temperature to 28 °C; show fan activation.
2. Lower temperature into the 26–28 °C band; show that hysteresis keeps the fan stable.
3. Lower to 26 °C; show fan release.
4. Raise humidity to 70%; show the yellow warning and Blynk event.

## 6:35–7:45 — Modes and overrides

**Show:** Blynk controls and confirmed outputs.

Demonstrate Sleep, Study and Away. Then show the light and fan Auto/Off/On overrides. State that the dashboard requests a change, but the separate reported-state indicators confirm what the ESP32 actually applied.

## 7:45–8:20 — Curtain servo

Move the curtain slider from 0 to 90 and 180 degrees. Show the Wokwi servo and the confirmed Blynk value.

## 8:20–9:50 — Gas safety priority

1. Increase the MQ-2 concentration until its digital output becomes active-low.
2. Show the red indicator, buzzer and comfort outputs turning off.
3. Show the Blynk `gas_alert` event and GAS ALERT status.
4. Press acknowledgement and show that the local alarm remains active.
5. Lower the concentration and wait for three safe reads before the alarm clears.

State clearly that the prototype supplements rather than replaces certified smoke or carbon-monoxide alarms.

## 9:50–10:50 — Network interruption

Interrupt the simulated network or Blynk connection. Show through the serial monitor that sensor reads and local rules continue. Restore connectivity and show the device returning online, telemetry refreshing and the reconnect event.

## 10:50–11:50 — Code and security

**Show:** Selected code only; never show `secrets.h`.

Point to `BlynkTimer`, constrained enum values, the gas-priority branch, bounded reconnection and the gitignored secret file. Explain that the private examiner README contains login information only because the brief requires it; credentials are not committed publicly or printed in logs.

## 11:50–12:40 — Reflection

Discuss the MQ-2 threshold issue, why a blocking cloud connection was unsuitable, and why desired dashboard controls had to be separated from reported actuator state. Mention the limits of simulation: it verifies logic and cloud interaction, not mains safety or sensor calibration.

## 12:40–13:10 — Closing

“SentinelSleep demonstrates stable ESP32 integration, local priority-based control, authenticated cloud telemetry, dashboard interaction and explicit security boundaries. Thank you.”

## Recording checklist

- Face visible continuously.
- Screen text readable at 1080p.
- No auth token, password, email inbox or unrelated private tabs visible.
- Blynk and Wokwi clocks/readings synchronized with the spoken test.
- Final duration below 15 minutes.
- Test the exported MP4 from beginning to end before upload.

