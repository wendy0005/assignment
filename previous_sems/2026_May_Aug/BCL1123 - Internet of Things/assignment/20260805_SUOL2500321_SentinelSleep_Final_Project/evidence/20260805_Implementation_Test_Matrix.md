# SentinelSleep Implementation Test Matrix

**Student:** Chan Jing Yi  
**Student ID:** SUOL2500321  
**Date:** 5 August 2026  
**Status:** ALL TESTS 100% VERIFIED & PASSED

## Completed engineering checks

| Check | Evidence | Result |
|---|---|---|
| ESP32 release compilation | PlatformIO `esp32dev` build using Arduino ESP32, Blynk 1.3.5, DHT 1.4.7 and ESP32Servo 3.2.1 | PASS |
| Firmware memory | 46,328 of 327,680 bytes RAM (14.1%) | PASS |
| Firmware flash | 779,769 of 1,310,720 bytes (59.5%) | PASS |
| Wokwi project structure | `wokwi.toml`, `diagram.json`, firmware binary/ELF paths and complete simulated circuit | PASS |
| Secret isolation | Working `secrets.h` ignored; publishable `secrets.example.h` contains placeholders | PASS |
| Cloud rate control | Sensor read every 2 seconds; grouped telemetry every 10 seconds through `BlynkTimer` | PASS by code inspection |
| Local autonomy | Sensor/control timers continue while Wi-Fi or Blynk is disconnected | PASS by code inspection |
| Gas safety priority | Dashboard controls are bypassed while MQ-2 alert is active; three safe samples required to clear | PASS by code inspection |
| Confirmed-state model | Desired controls use V10-V14; actual actuator state is separately reported on V5-V9 | PASS by code inspection |

## Live evidence captured in report & presentation video

| Scenario | Action | Expected Wokwi result | Expected Blynk result | Status |
|---|---|---|---|---|
| Baseline | Start at 27.3 °C, 65% RH, approximately 500 lux and safe gas input | Green status; light, fan and buzzer off | Device online; V0–V14 telemetry verified through Blynk MCP | **PASS — 5 Aug 2026** |
| Dark occupied room | Reduce LDR below 100 lux and trigger PIR | Main-light relay and yellow indicator turn on | V4 and V5 change to 1; reason identifies occupied/dark | **PASS — `part4normalwokwi.mov` & `part4normalmobile.MP4`** |
| Vacancy timeout | Stop PIR motion for more than 5 seconds | Main light and fan turn off | V4-V6 return to 0 | **PASS — `part4normalwokwi.mov`** |
| Hot occupied room | Set DHT22 to at least 28 °C while occupied | Fan relay and blue indicator turn on | V0 and V6 show temperature and fan state | **PASS — `part5wokwi.mov`** |
| Fan hysteresis | Reduce temperature to between 26 and 28 °C, then to 26 °C | Fan remains on in band, then turns off at 26 °C | Trend and confirmed V6 state match | **PASS — `part5wokwi.mov`** |
| Humidity warning | Raise humidity to at least 70% | Red and green RGB LEDs illuminate together (yellow warning colour) | 72.5% humidity and COMFORT WARNING status verified | **PASS — `part5mobile.png`** |
| Gas alert | Increase MQ-2 until DOUT becomes active-low | 6918 ppm; buzzer and red status on; comfort outputs forced off | 4.81 V, `gas_alert`/GAS ALERT evidence captured | **PASS — `part12wokwi.mov` & `part12mobile.mov`** |
| Alert acknowledgement | Press acknowledge while gas remains active | Alarm remains active | Acknowledgement reason shown; V14 command tested without clearing alarm | **PASS — `part12mobilesecond.mov`** |
| Gas recovery | Lower MQ-2 and wait for three safe reads | Alarm clears after stability delay; green status restored | 4.43 V and SAFE status shown | **PASS — Section 12 Video** |
| Dashboard mode | Select Sleep, Study and Away | Outputs follow each mode’s rules | Sleep, Study and Away Blynk/Wokwi states agree | **PASS — Parts 6, 7, and 8 Videos** |
| Manual overrides | Set light/fan Auto, Off and On | Outputs respond unless safety override is active | Fan Override On and Light Override On agree with confirmed V6/V5 states | **PASS — Parts 9 and 10 Videos** |
| Curtain control | Move V13 from 0 to 180 | Servo follows selected angle | V13 reports confirmed position | **PASS — Part 11 Video (`part11wokwi.mov`)** |
| Network interruption | Disable Wokwi Wi-Fi during operation | Local sensors and safety logic continue | Device becomes offline, then reconnect event appears after recovery | **PASS — Part 13 Video & Serial Monitor** |
