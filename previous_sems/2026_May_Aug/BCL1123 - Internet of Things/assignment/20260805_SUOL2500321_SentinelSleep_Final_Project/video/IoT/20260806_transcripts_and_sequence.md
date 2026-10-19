# SentinelSleep Final Demonstration Speech Script & Video Mapping

This document maps all 15 demonstration video clips to their respective sections in [`20260805_SUOL2500321_SentinelSleep_Final_Video_Script.md`](file:///Users/jingyichan/CodingArea/assignment/current_sem/BCL1123%20-%20Internet%20of%20Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/20260805_SUOL2500321_SentinelSleep_Final_Video_Script.md).

---

## 🎬 15-Section Descriptive Video Files & Transcripts

### Section 01: Introduction
- **File**: [`01_Introduction.MOV`](file:///Users/jingyichan/CodingArea/assignment/current_sem/BCL1123%20-%20Internet%20of%20Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/01_Introduction.MOV)
- **Duration**: ~20.91s
- **Transcript**:
  > *"Hello, my name is Chan Jing Yi, and this is my final project called SentinelSleep. SentinelSleep is a smart bedroom system built using an ESP32 with Wokwi simulations and a Blynk IoT platform. It monitors temperature, humidity, room brightness, occupancy, and gas safety. It can control the main light, fan, night light, buzzer, and curtain servo."*

---

### Section 02: Hardware and Architecture
- **File**: [`02_Hardware_and_Architecture.MOV`](file:///Users/jingyichan/CodingArea/assignment/current_sem/BCL1123%20-%20Internet%20of%20Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/02_Hardware_and_Architecture.MOV)
- **Duration**: ~36.47s
- **Transcript**:
  > *"This is the Wokwi circuit. The DHT22 measures temperature and humidity. The PIR sensor detects occupancy. The photoresistor measures illuminance, and the MQ-2 provides gas-safety input. The system also contains relays for the main light and fan, RGB status indicators, a night-light indicator, a buzzer, and a curtain servo. The ESP32 processes the sensor readings locally. It then sends telemetry to Blynk through virtual datastreams. The Blynk dashboard displays both sensor readings and confirmed actuator states."*

---

### Section 03: Baseline Operation
- **File**: [`03_Baseline_Operation.MOV`](file:///Users/jingyichan/CodingArea/assignment/current_sem/BCL1123%20-%20Internet%20of%20Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/03_Baseline_Operation.MOV)
- **Duration**: ~24.41s
- **Transcript**:
  > *"First, I will demonstrate the normal operating condition. The device is online. The temperature is approximately 27.3 degrees Celsius, humidity is 65 percent, illuminance is about 499 lux, and gas output voltage is approximately 4.43 volts. The system status is SAFE, and the comfort outputs are currently inactive."*

---

### Section 04: Normal Lighting
- **File**: [`04_Normal_Lighting.MOV`](file:///Users/jingyichan/CodingArea/assignment/current_sem/BCL1123%20-%20Internet%20of%20Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/04_Normal_Lighting.MOV)
- **Duration**: ~27.38s
- **Transcript**:
  > *"Next, I will reduce the illuminance below the lighting threshold and trigger the PIR sensor. The room is now dark and occupied. The ESP32 detects these conditions and activates the main light. The Blynk dashboard confirms the occupancy state, the main light state, and the active reasons. When motion stops, the demonstration vacancy timer expires and the light turns off again."*

---

### Section 05: Temperature and Humidity
- **File**: [`05_Temperature_and_Humidity.MOV`](file:///Users/jingyichan/CodingArea/assignment/current_sem/BCL1123%20-%20Internet%20of%20Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/05_Temperature_and_Humidity.MOV)
- **Duration**: ~35.60s
- **Transcript**:
  > *"Now I will increase the temperature to approximately 30 degrees Celsius while the room is occupied. The fan activates because the temperature is above the fan threshold. When the temperature is reduced, the hysteresis logic prevents the fan from switching rapidly between states. I will now raise the humidity above 70%. The Blynk dashboard changes to COMFORT WARNING, and the red and green RGB channels illuminate together to show the warning condition."*

---

### Section 06: Sleep Mode
- **File**: [`06_Sleep_Mode.MOV`](file:///Users/jingyichan/CodingArea/assignment/current_sem/BCL1123%20-%20Internet%20of%20Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/06_Sleep_Mode.MOV)
- **Duration**: ~21.82s
- **Transcript**:
  > *"I will now select Sleep Mode. The illuminance is approximately 25 lux, which is below the sleep lighting threshold, and the PIR detects occupancy. The night light activates, while the main light and fan remain off. This provides low-level lighting that is suitable for sleeping."*

---

### Section 07: Study Mode
- **File**: [`07_Study_Mode.MOV`](file:///Users/jingyichan/CodingArea/assignment/current_sem/BCL1123%20-%20Internet%20of%20Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/07_Study_Mode.MOV)
- **Duration**: ~28.23s
- **Transcript**:
  > *"Next, I will select Study Mode. The temperature is approximately 30.2 degrees Celsius and the illuminance is below 100 lux. Study Mode treats the room as occupied. The Blynk dashboard shows occupancy, main light and fan active. The physical indicators and relays show the same confirmed output state."*

---

### Section 08: Away Mode
- **File**: [`08_Away_Mode.MOV`](file:///Users/jingyichan/CodingArea/assignment/current_sem/BCL1123%20-%20Internet%20of%20Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/08_Away_Mode.MOV)
- **Duration**: ~22.23s
- **Transcript**:
  > *"I will now select Away Mode. The dashboard reports that Away Mode has disabled the comfort outputs. The main light, fan, and night light are off. The Wokwi circuit confirms that the corresponding outputs are also inactive. This prevents unnecessary operation when the room is unoccupied."*

---

### Section 09: Light Override
- **File**: [`09_Light_Override.MOV`](file:///Users/jingyichan/CodingArea/assignment/current_sem/BCL1123%20-%20Internet%20of%20Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/09_Light_Override.MOV)
- **Duration**: ~19.60s
- **Transcript**:
  > *"I'll set the operating mode back to Auto and select Light Override On. The main light turns on immediately. The Blynk dashboard reports the override and active main light state while the physical main light indicator and relay also activate."*

---

### Section 10: Fan Override
- **File**: [`10_Fan_Override.MOV`](file:///Users/jingyichan/CodingArea/assignment/current_sem/BCL1123%20-%20Internet%20of%20Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/10_Fan_Override.MOV)
- **Duration**: ~13.22s
- **Transcript**:
  > *"Now I will select Fan Override On. The fan indicator turns on in Blynk, and the Wokwi fan indicator and relay activate. This demonstrates that the manual command is applied and that the confirmed output state is reported separately from the requested control."*

---

### Section 11: Curtain Servo
- **File**: [`11_Curtain_Servo.MOV`](file:///Users/jingyichan/CodingArea/assignment/current_sem/BCL1123%20-%20Internet%20of%20Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/11_Curtain_Servo.MOV)
- **Duration**: ~15.37s
- **Transcript**:
  > *"I will now move the curtain control from zero degrees to 90 degrees and then to 180 degrees. The Wokwi servo follows the selected position, and the Blynk dashboard reports the confirmed curtain position."*

---

### Section 12: Gas Alert and Acknowledgement
- **File**: [`12_Gas_Alert_and_Acknowledgement.MOV`](file:///Users/jingyichan/CodingArea/assignment/current_sem/BCL1123%20-%20Internet%20of%20Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/12_Gas_Alert_and_Acknowledgement.MOV)
- **Duration**: ~37.53s
- **Transcript**:
  > *"Next, I will increase the MQ-2 gas value until the safety threshold is reached. The system now reports GAS ALERT. The red indicator and buzzer activate, and the comfort outputs are forced off because gas safety has the highest priority. I will press the Acknowledge Alert control. The acknowledgement is recorded, but the alarm remains active while the gas condition is still unsafe. After lowering the gas value, the system waits for multiple safe readings before clearing the alarm and returning to the SAFE state."*

---

### Section 13: Network and Security
- **File**: [`13_Network_and_Security.MOV`](file:///Users/jingyichan/CodingArea/assignment/current_sem/BCL1123%20-%20Internet%20of%20Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/13_Network_and_Security.MOV)
- **Duration**: ~28.33s
- **Transcript**:
  > *"The ESP32 continues running its sensor and safety logic locally, even if the cloud connection is interrupted. When the connection is restored, the device reconnects and the Blynk telemetry updates again. For security, the Blynk token is stored in a private ignored secrets file. It is not displayed in the video or committed as a public credential."*

---

### Section 14: Reflection
- **File**: [`14_Reflection.MOV`](file:///Users/jingyichan/CodingArea/assignment/current_sem/BCL1123%20-%20Internet%20of%20Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/14_Reflection.MOV)
- **Duration**: ~27.77s
- **Transcript**:
  > *"This project demonstrates the importance of separating requested control states from confirmed actual state. It also shows why gas safety must take priority over comfort controls. The system is validated through simulation and cloud interaction. However, the Wokwi prototype does not replace certified gas alarms, mains-safety testing, or real sensor calibration."*

---

### Section 15: Closing
- **File**: [`15_Closing.MOV`](file:///Users/jingyichan/CodingArea/assignment/current_sem/BCL1123%20-%20Internet%20of%20Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/15_Closing.MOV)
- **Duration**: ~24.77s
- **Transcript**:
  > *"To conclude, SentinelSleep demonstrates ESP32 sensor integration, local priority-based automation, Blynk cloud monitoring, operating modes, manual overrides, and gas safety handling. The system provides explainable output decisions while keeping safety logic active at the device level. Thank you for watching."*
