# SentinelSleep Final Demonstration Speech Script

## Introduction

**Show:** Project title, your face, name and student ID.

“Hello, my name is Chan Jing Yi, and my student ID is SUOL2500321. This is my BCL1123 Internet of Things final project, called SentinelSleep.

SentinelSleep is a smart-bedroom system built using an ESP32, Wokwi simulation and the Blynk IoT platform. It monitors temperature, humidity, room brightness, occupancy and gas safety. It can control the main light, fan, night light, buzzer and curtain servo.”

## Hardware and architecture

**Show:** Full Wokwi circuit, then point to the DHT22, PIR, photoresistor, MQ-2, relays, RGB indicators, night light, buzzer and servo. Then show the Blynk dashboard and architecture diagram.

“This is the Wokwi circuit. The DHT22 measures temperature and humidity. The PIR sensor detects occupancy. The photoresistor measures illuminance, and the MQ-2 provides gas-safety input.

The system also contains relays for the main light and fan, RGB status indicators, a night-light indicator, a buzzer and a curtain servo.

The ESP32 processes the sensor readings locally. It then sends telemetry to Blynk through virtual datastreams. The Blynk dashboard displays both sensor readings and confirmed actuator states.”

## Baseline operation

**Show:** Blynk device online with approximately 27.3°C, 65% humidity, 499 lx, 4.43V gas voltage and SAFE status. Show the normal Wokwi circuit with outputs inactive.

“First, I will demonstrate the normal operating condition.

The device is online. The temperature is approximately 27.3 degrees Celsius, humidity is 65 percent, illuminance is about 499 lux, and gas voltage is approximately 4.43 volts.

The system status is SAFE, and the comfort outputs are currently inactive.”

## Normal lighting

**Show:** Wokwi LDR control below 100 lux and PIR motion control. Show the main-light indicator/relay activating, then stop motion and wait for the vacancy timeout.

“Next, I will reduce the illuminance below the lighting threshold and trigger the PIR sensor.

The room is now dark and occupied. The ESP32 detects these conditions and activates the main light.

The Blynk dashboard confirms the occupancy state, the main-light state and the action reason. When motion stops, the demonstration vacancy timer expires and the light turns off again.”

## Temperature and humidity

**Show:** Wokwi DHT22 at approximately 30°C, then reduce it to demonstrate fan hysteresis. Raise humidity to at least 70% and show Blynk `COMFORT WARNING` plus the Wokwi red-and-green warning indication.

“Now I will increase the temperature to approximately 30 degrees Celsius while the room is occupied.

The fan activates because the temperature is above the fan threshold. When the temperature is reduced, the hysteresis logic prevents the fan from switching rapidly between states.

I will now raise the humidity above 70 percent. The Blynk dashboard changes to COMFORT WARNING, and the Wokwi red and green RGB channels illuminate together to show the warning condition.”

## Sleep mode

**Show:** Blynk Sleep selected with approximately 25 lx, Occupancy active and Night Light active. Show Wokwi night-light output active and main light/fan inactive.

“I will now select Sleep mode.

The illuminance is approximately 25 lux, which is below the sleep lighting threshold, and the PIR detects occupancy.

The night light activates, while the main light and fan remain off. This provides low-level lighting that is suitable for sleeping.”

## Study mode

**Show:** Blynk Study selected with approximately 30.2°C and below 100 lx. Show Occupancy, Main Light and Fan active, then show the matching Wokwi indicators and relays.

“Next, I will select Study mode.

The temperature is approximately 30.2 degrees Celsius and the illuminance is below 100 lux. Study mode treats the room as occupied.

The Blynk dashboard shows occupancy, main light and fan active. The Wokwi indicators and relays show the same confirmed output state.”

## Away mode

**Show:** Blynk Away selected with `Away mode disabled` and all comfort outputs off. Show the matching Wokwi outputs inactive.

“I will now select Away mode.

The dashboard reports that Away mode has disabled the comfort outputs. The main light, fan and night light are off.

The Wokwi circuit confirms that the corresponding outputs are also inactive. This prevents unnecessary operation when the room is unoccupied.”

## Light override

**Show:** Blynk Operating Mode Auto and Light Override On. Show Main Light active in Blynk and the corresponding Wokwi LED and relay active.

“I will set the operating mode back to Auto and select Light Override On.

The main light turns on immediately. The Blynk dashboard reports the override and the active main-light state, while the Wokwi main-light indicator and relay also activate.”

## Fan override

**Show:** Blynk Operating Mode Auto and Fan Override On. Show Fan active in Blynk and the corresponding Wokwi LED and relay active.

“Now I will select Fan Override On.

The fan indicator turns on in Blynk, and the Wokwi fan indicator and relay activate. This demonstrates that the manual command is applied and that the confirmed output state is reported separately from the requested control.”

## Curtain servo

**Show:** Blynk curtain slider at 0°, 90° and 180°. Show the Wokwi servo moving and the confirmed position value updating.

“I will now move the curtain control from zero degrees to 90 degrees and then to 180 degrees.

The Wokwi servo follows the selected position, and the Blynk dashboard reports the confirmed curtain position.”

## Gas alert and acknowledgement

**Show:** Increase the Wokwi MQ-2 value until Blynk displays `GAS ALERT`, approximately 4.81V and 6918 ppm. Show the Wokwi red indicator and buzzer, press Acknowledge Alert, then lower the gas value and show recovery to SAFE.

“Next, I will increase the MQ-2 gas value until the safety threshold is reached.

The system now reports GAS ALERT. The red indicator and buzzer activate, and the comfort outputs are forced off because gas safety has the highest priority.

I will press the Acknowledge Alert control. The acknowledgement is recorded, but the alarm remains active while the gas condition is still unsafe.

After lowering the gas value, the system waits for multiple safe readings before clearing the alarm and returning to the SAFE state.”

## Network and security

**Show:** Serial monitor during a simulated connection interruption and reconnection. Show selected code such as `BlynkTimer`, the gas-priority branch and enum controls. Do not show `secrets.h` or any token.

“The ESP32 continues running its sensor and safety logic locally, even if the cloud connection is interrupted. When the connection is restored, the device reconnects and the Blynk telemetry updates again.

For security, the Blynk token is stored in a private ignored secrets file. It is not displayed in the video or committed as a public credential.”

## Reflection

**Show:** The final dashboard and Wokwi circuit while explaining the design decisions and simulation limitations.

“This project demonstrates the importance of separating requested control states from confirmed actuator states. It also shows why gas safety must take priority over comfort controls.

The system is validated through simulation and cloud interaction. However, the Wokwi prototype does not replace certified gas alarms, mains-safety testing or real sensor calibration.”

## Closing

**Show:** Blynk dashboard and Wokwi circuit together, followed by the project title.

“To conclude, SentinelSleep demonstrates ESP32 sensor integration, local priority-based automation, Blynk cloud monitoring, operating modes, manual overrides and gas-safety handling.

The system provides explainable output decisions while keeping safety logic active at the device level.

Thank you for watching.”
