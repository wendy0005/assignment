SENTINELSLEEP FINAL PROJECT — EXAMINER README

Student: Chan Jing Yi
Student ID: SUOL2500321
Module: BCL1123 Internet of Things

CONTENTS
1. report/20260805_SUOL2500321_SentinelSleep_Final_Report.docx
2. report/20260805_SUOL2500321_SentinelSleep_Final_Report.pdf
3. YouTube Video Demonstration: https://youtu.be/CVU9OjcAe5A
4. video/20260807_SentinelSleep_Final_Presentation_1080p.mp4
5. project/ — complete VS Code, PlatformIO and Wokwi project
6. evidence/ — implementation test matrix and captured evidence

BLYNK EXAMINER ACCESS
Login URL: https://blynk.cloud/
Email: [INSERT PRIVATE BLYNK LOGIN EMAIL]
Password: [INSERT PRIVATE BLYNK LOGIN PASSWORD]
Organization: [INSERT ORGANIZATION NAME]
Device: SentinelSleep-SUOL2500321

Never publish this file in a public repository. It is intended only for the private assessment folder.

RUNNING THE PROJECT
1. Open the project/ folder in VS Code with PlatformIO and the Wokwi extension.
2. Confirm project/include/secrets.h contains the supplied Blynk template ID and device auth token.
3. Run "PlatformIO: Build". The verified environment is esp32dev.
4. Run "Wokwi: Start Simulator".
5. Open Blynk Console, select the SentinelSleep-SUOL2500321 device, and open its dashboard.
6. Change Wokwi sensor values to test temperature, humidity, light, motion and gas scenarios.

DASHBOARD CONTROLS
- Operating mode: Auto, Sleep, Study, Away
- Light override: Auto, Off, On
- Fan override: Auto, Off, On
- Curtain position: 0–180 degrees
- Alert acknowledgement: records acknowledgement but does not cancel an active gas alarm

SAFETY NOTE
The MQ-2 and relay paths are simulations for academic demonstration. They do not replace certified alarms or qualified mains wiring.
