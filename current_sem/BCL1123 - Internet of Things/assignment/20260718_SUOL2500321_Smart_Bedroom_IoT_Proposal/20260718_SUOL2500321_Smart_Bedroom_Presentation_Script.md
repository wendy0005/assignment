# SentinelSleep Presentation Script

**Target duration:** 8-9 minutes  
**Presenter:** Chan Jing Yi (SUOL2500321)  
**Camera requirement:** Keep the camera on and face visible throughout.

## 0:00-0:40 - Introduction

[Show the title slide containing the project name, presenter name and student ID. Keep the camera visible as a small overlay throughout the screen share.]

Good morning or afternoon. My name is Chan Jing Yi, student ID SUOL2500321. My proposal is called SentinelSleep, an occupancy-aware smart bedroom comfort, energy and safety system. The project focuses on one bedroom in my current accommodation. It addresses three connected issues: unnecessary energy use, reactive comfort control, and limited visibility of environmental or safety events.

## 0:40-1:35 - Target environment and problems

[Show Figure 1, the wide bedroom photograph, followed by Figure 2, the close-up of the existing controls or proposed sensor location.] The bedroom is used for sleeping, studying and resting, so its needs change by time and occupancy. Existing light and fan controls depend on the occupant remembering to operate them. A light can remain on when the room is empty, and a fan can continue running after the occupant leaves. Temperature and humidity are not measured, so comfort decisions are reactive. Safety alarms also operate separately from comfort controls, and ordinary switches do not explain why an automated action occurred.

## 1:35-2:45 - Proposed solution and hardware

[Show Figure 3, the SentinelSleep hardware-selection chart. Briefly switch to the working Wokwi project if time permits: https://wokwi.com/projects/469850121140731905]

SentinelSleep uses an ESP32 as the local controller. A DHT22 measures temperature and humidity. A PIR sensor detects movement without using a camera. A photoresistor measures room brightness, and an MQ-2 demonstrates supplementary combustible-gas detection. Relay modules represent the light and fan. A night light, RGB indicator and buzzer provide local responses, while an optional servo can demonstrate curtain control. These parts are supported by Wokwi, so the design can be simulated before any physical build.

The MQ-2 does not replace a certified smoke or carbon-monoxide alarm. It is only a prototype input for local and remote alerts. A proper smoke alarm must remain installed and maintained independently.

## 2:45-4:05 - Control logic

[Show Figure 5, the priority-based SentinelSleep control-flow diagram. Follow the arrows from left to right.]

The flowchart begins when the ESP32 starts or wakes. It reads the DHT22, PIR sensor, photoresistor and MQ-2 gas sensor. The first decision checks whether the readings are valid. If a reading is invalid, the system retains its last safe state, records the fault and tries again instead of treating an error as a normal reading.

After validation, the gas threshold is checked before any comfort automation. This gives safety the highest priority. When the MQ-2 digital output becomes low, the ESP32 stops the normal lighting and fan rules, activates the buzzer, changes the status indicator to red and publishes an urgent MQTT alert. The system continues monitoring the sensor and clears the warning only after three consecutive safe readings.

If there is no gas alert, the controller evaluates the time of day. During sleeping hours, motion combined with very low illumination activates the low-output night light instead of the main bedroom light. Outside sleeping hours, motion and darkness activate the main light. The production proposal uses a five-minute vacancy timeout;

Both lighting paths then lead to the fan rule. The fan operates only when the room is occupied and the temperature reaches 28 degrees Celsius. It switches off when the room becomes vacant or the temperature falls to 26 degrees. This two-degree hysteresis gap prevents the relay from switching rapidly when the temperature fluctuates around one threshold.

At the end of every cycle, the ESP32 updates the local indicators and publishes the latest sensor and actuator state through MQTT. It then waits two seconds before reading the sensors again. The return arrow shows that this is a continuous control loop rather than a one-time sequence.

## 4:05-5:20 - Four-layer architecture

[Show Figure 4, the SentinelSleep four-layer system-architecture diagram.] The edge layer contains the sensors, actuators and ESP32. It reads data, validates it and runs local rules. Local processing keeps the system responsive and allows it to work when the internet is unavailable.

The connectivity layer uses 2.4 gigahertz Wi-Fi and MQTT over TLS in the proposed production design. The Wokwi demonstration uses standard MQTT over TCP for straightforward public-broker testing. MQTT provides lightweight publish-and-subscribe messaging between the ESP32 and cloud broker.

The cloud layer authenticates the device, receives messages, stores selected readings, maintains desired and reported state, and routes alerts. AWS IoT Core is a reference implementation rather than a compulsory platform.

The application layer is the mobile dashboard. It displays room safety, comfort readings, occupancy, actuator states, alerts and history. Commands move down through the same layers, and confirmed device state returns to the application.

## 5:20-6:20 - Dashboard prototype

[Show Figure 6, the SentinelSleep mobile-dashboard wireframe.] The first banner answers the most important question: whether the room is safe. Four cards show temperature, humidity, illumination and occupancy. The device panel shows whether the main light, fan and night light are operating, together with the reason for each action. Modes include Auto, Sleep, Study and Away. Manual control is time-limited so an override cannot leave a device running indefinitely.

## 6:20-7:25 - Uniqueness and comparison

[Show the market-comparison table in Section 5 of the report. Highlight the SentinelSleep column while explaining the differences.]

Commercial products usually specialise. A smart motion sensor can automate lights, a room sensor can support temperature control, and a certified alarm focuses on smoke or carbon monoxide. SentinelSleep is different because it combines occupancy, illumination, comfort and supplementary warning in one explainable rule engine. It also continues its core logic locally if cloud access fails.

The unique feature is priority-aware sensor fusion. The system does not react to one reading in isolation. It checks safety state, occupancy, light level, time and manual override, then reports why an action occurred. Privacy is protected because occupancy is sensed without a camera or microphone.

## 7:25-8:20 - Safety, limitations and next stage

[Show the live Wokwi simulation or a recorded screenshot sequence. First show the normal green state, then increase the MQ-2 concentration until the digital output becomes LOW and the red gas alert activates.]

The working Wokwi prototype demonstrates live sensor readings, occupancy-aware lighting and fan rules, MQTT telemetry, and the priority gas-alert path. The public simulation is available at https://wokwi.com/projects/469850121140731905.

The proposal has clear limitations. Thresholds must be tuned in the real bedroom. PIR movement is only an estimate of occupancy, and the MQ-2 is not a certified life-safety sensor. Mains-powered relays require proper isolation and competent installation. Security also matters, so device certificates, encrypted communication and least-privilege access are part of the proposed design.

The Wokwi simulation has now been built and tested. The next stage is to insert the original bedroom photographs, test additional normal and fault scenarios, and adjust the thresholds using observations from the actual room.

## 8:20-8:45 - Closing

[Return to a closing slide containing the project name, student name, student ID and Wokwi project link.]

SentinelSleep presents a feasible IoT proposal that improves bedroom energy control, comfort awareness and environmental visibility while preserving privacy and local reliability. Its Wokwi-compatible hardware and four-layer architecture provide a practical foundation for the Final Project. Thank you.
