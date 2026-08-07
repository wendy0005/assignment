# SentinelSleep — Student To-Do Checklist

**Student:** Chan Jing Yi  
**Student ID:** SUOL2500321  
**Course:** BCL1123 Internet of Things  
**Updated:** 7 August 2026

## Do next

- [x] Open the Blynk mobile app and sign in to the same account.
- [x] Configure the mobile dashboard with the equivalent V0–V14 readings, indicators and controls used on the completed web dashboard.
- [x] Start the SentinelSleep Wokwi simulation.
- [x] Confirm that the simulated ESP32 appears online in Blynk.

## Complete the live test matrix

Use `evidence/20260805_Implementation_Test_Matrix.md` and test every scenario:

- [x] Normal baseline readings.
- [x] Dark occupied room.
- [x] Vacancy timeout.
- [x] Hot occupied room and fan activation.
- [x] Fan hysteresis and shutdown.
- [x] High-humidity warning.
- [x] Gas alert and safety override.
- [x] Alert acknowledgement while gas remains unsafe.
- [x] Gas recovery after three safe readings.
- [x] Sleep, Study and Away operating modes.
- [x] Light and fan Auto/Off/On overrides.
- [x] Curtain movement from 0° to 180°.
- [x] Wi-Fi interruption and Blynk reconnection.
- [x] Record the actual result of every test as PASS or FAIL in the test matrix.

## Capture evidence

- [x] Capture the complete Wokwi circuit while it is running (`report/assets/figure3_wokwi_live_baseline.png`).
- [x] Capture the Blynk mobile device showing **Online** (`report/assets/figure6_blynk_mobile_live.png`).
- [x] Capture normal sensor readings on the Blynk mobile dashboard (`report/assets/figure6_blynk_mobile_live.png`).
- [x] Capture the humidity-warning state (`evidence/mobile1.png` and `evidence/wokwi1.png`).
- [x] Capture the gas-alert event and active alarm state (`evidence/mobile2.png` and `evidence/wokwi2.png`).
- [x] Capture a dashboard mode or override changing the Wokwi output.
- [x] Capture the curtain slider controlling the servo.
- [x] Capture the device reconnect event after restoring Wi-Fi.
- [x] Ensure no device auth token, Wi-Fi password or private login is visible in any screenshot.
- [x] Send the screenshots to Codex for Figure 3, Figure 6 and final report regeneration.

## Record the demonstration

- [x] Follow `video/20260805_SUOL2500321_SentinelSleep_Final_Video_Script.md`.
- [x] Keep your face visible as required during the demonstration.
- [x] Demonstrate the real Wokwi-to-Blynk interaction rather than using static screenshots only.
- [x] Record all required sensor, alert, mode, override, curtain and reconnection tests.
- [x] Keep the completed video under 15 minutes (6m 39s).
- [x] Send the original video clips to Codex for assembly and verification.
- [x] Publish video to YouTube: https://youtu.be/CVU9OjcAe5A

## Submission details

- [x] Confirm the exact LMS submission date and time.
- [x] Privately insert the examiner's Blynk login details into `readme.txt`.
- [x] Do not publish the Blynk device auth token or Wi-Fi password.
- [x] Ask Codex to regenerate the DOCX and PDF after the verified screenshots and test results are ready.
- [x] Ask Codex to assemble and verify the final MP4.
- [ ] Upload the final report, source project, video and `readme.txt` into one Google Drive folder.
- [ ] Set the Drive folder permission required by the lecturer.
- [ ] Test the Drive link in a signed-out/private browser window.
- [ ] Insert the verified Drive URL into the final report.
- [x] Submit after the report is fully compiled.

## Already completed

- [x] Blynk MCP OAuth connection.
- [x] Live Blynk template and device.
- [x] V0–V14 datastreams.
- [x] Gas, humidity, sensor-fault and reconnection events.
- [x] Blynk web dashboard.
- [x] Private firmware credentials.
- [x] ESP32 firmware compilation.
- [x] Wokwi circuit files and report draft.
