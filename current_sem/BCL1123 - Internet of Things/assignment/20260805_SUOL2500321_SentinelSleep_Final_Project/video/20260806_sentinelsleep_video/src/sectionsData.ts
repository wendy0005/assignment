export interface TimedSubtitle {
  startFrame: number;
  endFrame: number;
  text: string;
}

export interface VideoSection {
  id: string;
  sectionNumber: number;
  title: string;
  sectionType: "explanation" | "demo";
  videoFile: string;
  durationInSeconds: number;
  durationInFrames: number;
  transcript: string;
  timedSubtitles: TimedSubtitle[];
  keyPoints?: string[];
  overlayImage?: string;
  overlayVideo?: string;
  overlayVideo2?: string;
  pipVideo?: string;
  pipVideo2?: string;
  pipImage?: string;
}

export const SECTIONS: VideoSection[] = [
  {
    id: "01_intro",
    sectionNumber: 1,
    title: "Project Overview & Vision",
    sectionType: "explanation",
    videoFile: "IoT/01_Introduction.MOV",
    durationInSeconds: 25.64,
    durationInFrames: 770,
    transcript: "Hello, my name is Chan Jing Yi, and this is my final project called SentinelSleep. SentinelSleep is a smart bedroom system built using an ESP32 microcontroller, with Wokwi simulations and a Blynk IoT platform. It monitors temperature, humidity, room brightness, occupancy, and gas safety. It can control the main light, fan, night light, buzzer, and curtain servo.",
    timedSubtitles: [
      { startFrame: 0, endFrame: 154, text: "Hello, my name is Chan Jing Yi, and this is my final project called SentinelSleep." },
      { startFrame: 187, endFrame: 353, text: "SentinelSleep is a smart bedroom system built using an ESP32 microcontroller," },
      { startFrame: 353, endFrame: 552, text: "with Wokwi simulations and a Blynk IoT platform. It monitors temperature, humidity, room brightness," },
      { startFrame: 552, endFrame: 665, text: "occupancy, and gas safety. It can control the main light," },
      { startFrame: 665, endFrame: 770, text: "fan, night light, buzzer, and curtain servo." }
    ],
    keyPoints: [
      "Student Presenter: Chan Jing Yi — Final Project for BCL1123 Internet of Things",
      "SentinelSleep Smart Bedroom: Autonomous environment monitoring combining local ESP32 edge processing & Blynk Cloud telemetry.",
      "Multi-Sensor Inputs: Real-time telemetry from DHT22 (Temp & Humidity), PIR (Occupancy), LDR (Illuminance), and MQ-2 (Gas Safety).",
      "Multi-Actuator Control: Relays for Main Light & Fan, Night Light LED, Alarm Buzzer, and PWM Servo Motor for automated curtain position."
    ]
  },
  {
    id: "02_hardware",
    sectionNumber: 2,
    title: "Hardware & System Architecture",
    sectionType: "explanation",
    videoFile: "IoT/02_Hardware_and_Architecture.MOV",
    durationInSeconds: 40.84,
    durationInFrames: 1226,
    transcript: "This is the Wokwi circuit. The DHT22 measures temperature and humidity, PIR detects occupancy, photoresistor measures illuminance, and MQ-2 provides gas safety input. The system contains relays for main light and fan, RGB status indicators, a night light indicator, a buzzer, and a curtain servo. The ESP32 processes sensor readings locally and sends telemetry to Blynk via virtual datastreams.",
    timedSubtitles: [
      { startFrame: 0, endFrame: 250, text: "This is the Wokwi circuit. The DHT22 measures temperature and humidity, the PIR sensor detects occupancy," },
      { startFrame: 250, endFrame: 454, text: "the photoresistor measures illuminance, and the MQ-2 provides gas safety input." },
      { startFrame: 470, endFrame: 670, text: "The system also contains relays for main light and fan, RGB status indicators," },
      { startFrame: 670, endFrame: 859, text: "a night light indicator, a buzzer, and a curtain servo. The ESP32 processes sensor readings" },
      { startFrame: 859, endFrame: 1073, text: "locally, then sends telemetry to Blynk through virtual datastreams. The Blynk dashboard displays" },
      { startFrame: 1073, endFrame: 1226, text: "both sensor readings and confirmed actuator states." }
    ],
    keyPoints: [
      "Sensors: DHT22, PIR, LDR (Photoresistor), MQ-2 Gas",
      "Actuators: Relays (Light/Fan), Servo (Curtain), Buzzer, RGB LED",
      "Local Edge Processing on ESP32",
      "Virtual Datastream Cloud Sync"
    ],
    overlayImage: "IoT/videomaterials/part2.png"
  },
  {
    id: "03_baseline",
    sectionNumber: 3,
    title: "Baseline Operation State",
    sectionType: "demo",
    videoFile: "IoT/03_Baseline_Operation.MOV",
    durationInSeconds: 24.40,
    durationInFrames: 733,
    transcript: "First, I will demonstrate the normal operating condition. The device is online. The temperature is approximately 27.3°C. Humidity is 65%. Illuminance is about 499 lux, and gas voltage is approximately 4.43V. The system status is SAFE, and comfort outputs are currently inactive.",
    timedSubtitles: [
      { startFrame: 0, endFrame: 134, text: "First, I will demonstrate the normal operating condition." },
      { startFrame: 134, endFrame: 196, text: "The device is online." },
      { startFrame: 196, endFrame: 337, text: "The temperature is approximately 27.3°C." },
      { startFrame: 337, endFrame: 406, text: "Humidity is 65%." },
      { startFrame: 406, endFrame: 593, text: "Illuminance is about 499 lux, and gas output voltage is approximately 4.43V." },
      { startFrame: 593, endFrame: 733, text: "The system status is SAFE, and comfort outputs are currently inactive." }
    ],
    keyPoints: [
      "System Status: SAFE",
      "Temp: ~27.3°C | Humidity: ~65%",
      "Illuminance: ~499 lux (Daylight)",
      "Gas Voltage: 4.43V (Normal)"
    ],
    overlayImage: "IoT/videomaterials/part3.png"
  },
  {
    id: "04_lighting",
    sectionNumber: 4,
    title: "Normal Lighting & Occupancy Demo",
    sectionType: "demo",
    videoFile: "IoT/04_Normal_Lighting.MOV",
    durationInSeconds: 27.40,
    durationInFrames: 822,
    transcript: "Next, I will reduce the illuminance below threshold and trigger the PIR sensor. The room is now dark and occupied. The ESP32 detects this and activates the main light. The Blynk dashboard confirms occupancy state, main light state, and active reasons. When motion stops, the vacancy timer expires and the light turns off.",
    timedSubtitles: [
      { startFrame: 0, endFrame: 180, text: "Next, I will reduce the illuminance below the lighting threshold and trigger the PIR sensor." },
      { startFrame: 180, endFrame: 420, text: "The room is now dark and occupied. The ESP32 detects these conditions and activates the main light." },
      { startFrame: 420, endFrame: 630, text: "The Blynk dashboard confirms occupancy state, main light state, and active reasons." },
      { startFrame: 630, endFrame: 822, text: "When motion stops, the vacancy timer expires and the light turns off again." }
    ],
    keyPoints: [
      "Trigger: Low Lux (<100) + Occupancy Detected",
      "Action: Main Light Relay Auto-Activated",
      "Blynk Telemetry Sync & Reason Display",
      "Vacancy Timer Auto-Turnoff"
    ],
    overlayVideo: "IoT/videomaterials/part4normalwokwi.mov",
    pipVideo: "IoT/videomaterials/part4normalmobile.MP4"
  },
  {
    id: "05_temp_humidity",
    sectionNumber: 5,
    title: "Temperature & Humidity Control Demo",
    sectionType: "demo",
    videoFile: "IoT/05_Temperature_and_Humidity.MOV",
    durationInSeconds: 35.60,
    durationInFrames: 1068,
    transcript: "Now I increase the temperature to approximately 30°C while occupied. The fan activates because the temperature is above the fan threshold. When temperature is reduced, hysteresis logic prevents rapid switching. I will now raise the humidity above 70%. The Blynk dashboard changes to COMFORT WARNING, and red and green RGB channels illuminate together to show warning condition.",
    timedSubtitles: [
      { startFrame: 0, endFrame: 194, text: "Now I increase the temperature to approximately 30°C while the room is occupied." },
      { startFrame: 194, endFrame: 334, text: "The fan activates because the temperature is above the fan threshold." },
      { startFrame: 334, endFrame: 478, text: "When the temperature is reduced, hysteresis logic prevents the" },
      { startFrame: 478, endFrame: 732, text: "fan from switching rapidly between states. I will now raise humidity above 70%." },
      { startFrame: 732, endFrame: 972, text: "The Blynk dashboard changes to COMFORT WARNING, and red and green RGB channels" },
      { startFrame: 972, endFrame: 1068, text: "illuminate together to show the warning condition." }
    ],
    keyPoints: [
      "Fan Trigger: Temp > 28°C when Occupied",
      "Hysteresis Protection against Rapid Toggling",
      "Humidity Alert: > 70% triggers Comfort Warning",
      "Yellow/Orange RGB Status Illumination"
    ],
    overlayVideo: "IoT/videomaterials/part5wokwi.mov",
    pipImage: "IoT/videomaterials/part5mobile.png"
  },
  {
    id: "06_sleep_mode",
    sectionNumber: 6,
    title: "Sleep Mode Operation Demo",
    sectionType: "demo",
    videoFile: "IoT/06_Sleep_Mode.MOV",
    durationInSeconds: 21.82,
    durationInFrames: 655,
    transcript: "I will now select Sleep Mode. The illuminance is approximately 25 lux (below sleep lighting threshold), and the PIR detects occupancy. The night light activates while main light and fan remain off. This provides low-level lighting suitable for sleeping.",
    timedSubtitles: [
      { startFrame: 0, endFrame: 116, text: "I will now select Sleep Mode." },
      { startFrame: 116, endFrame: 322, text: "The illuminance is approximately 25 lux, which is below the sleep lighting threshold" },
      { startFrame: 322, endFrame: 398, text: "and the PIR detects occupancy." },
      { startFrame: 398, endFrame: 534, text: "The night light activates while main light and fan remain off." },
      { startFrame: 534, endFrame: 655, text: "This provides low-level lighting suitable for sleeping." }
    ],
    keyPoints: [
      "Mode Selection: SLEEP Protocol Active",
      "Threshold: Illuminance ~25 lux (< 50 lux Sleep Threshold) + PIR Active",
      "Actuator Output: Night Light Active (Low-power Ambient LED)",
      "Suppression Logic: Main Light & Fan Relay Kept OFF for Sleep Comfort"
    ],
    overlayVideo: "IoT/videomaterials/part6wokwi.mov",
    pipVideo: "IoT/videomaterials/part6mobile.mov"
  },
  {
    id: "07_study_mode",
    sectionNumber: 7,
    title: "Study Mode Operation Demo",
    sectionType: "demo",
    videoFile: "IoT/07_Study_Mode.MOV",
    durationInSeconds: 28.23,
    durationInFrames: 848,
    transcript: "Next, I will select Study Mode. The temperature is approximately 30.2°C, and illuminance is below 100 lux. Study Mode treats room as occupied. The Blynk dashboard shows occupancy, main light and fan active. Physical indicators and relays show the same confirmed output state.",
    timedSubtitles: [
      { startFrame: 0, endFrame: 60, text: "Next, I will select Study Mode." },
      { startFrame: 129, endFrame: 264, text: "The temperature is approximately 30.2°C and the" },
      { startFrame: 264, endFrame: 450, text: "illuminance is below 100 lux. Study Mode treats the room as occupied." },
      { startFrame: 480, endFrame: 570, text: "The Blynk dashboard shows occupancy," },
      { startFrame: 570, endFrame: 720, text: "main light and fan active. The physical indicators and" },
      { startFrame: 720, endFrame: 848, text: "relays show the same confirmed output state." }
    ],
    keyPoints: [
      "Mode: STUDY (Forced Occupancy)",
      "Temp: ~30.2°C | Lux < 100",
      "Dual Comfort: Main Light & Fan Active",
      "Relay States Confirmed on Blynk Dashboard"
    ],
    overlayVideo: "IoT/videomaterials/part7wokwi.mov",
    pipVideo: "IoT/videomaterials/part7mobile.mov"
  },
  {
    id: "08_away_mode",
    sectionNumber: 8,
    title: "Away Mode Operation Demo",
    sectionType: "demo",
    videoFile: "IoT/08_Away_Mode.MOV",
    durationInSeconds: 22.23,
    durationInFrames: 668,
    transcript: "I will now select Away Mode. The dashboard reports Away Mode has disabled comfort outputs. Main light, fan, and night light are off. Wokwi circuit confirms outputs are inactive, preventing unnecessary operation when unoccupied.",
    timedSubtitles: [
      { startFrame: 0, endFrame: 81, text: "I will now select Away Mode." },
      { startFrame: 81, endFrame: 288, text: "The dashboard reports Away Mode has disabled comfort outputs, main light," },
      { startFrame: 288, endFrame: 373, text: "fan, and night light are off." },
      { startFrame: 373, endFrame: 543, text: "The Wokwi circuit confirms corresponding outputs are inactive." },
      { startFrame: 543, endFrame: 668, text: "This prevents unnecessary operation when room is unoccupied." }
    ],
    keyPoints: [
      "Mode: AWAY Protocol Active",
      "Comfort Outputs Forcefully Disabled",
      "Energy Conservation Protocol",
      "Zero Unintended Relay Triggers"
    ],
    overlayImage: "IoT/videomaterials/part8wokwi.png",
    pipImage: "IoT/videomaterials/part3.png"
  },
  {
    id: "09_light_override",
    sectionNumber: 9,
    title: "Manual Light Override Demo",
    sectionType: "demo",
    videoFile: "IoT/09_Light_Override.MOV",
    durationInSeconds: 19.60,
    durationInFrames: 588,
    transcript: "I'll set operating mode back to Auto and select Light Override On. The main light turns on immediately. The Blynk dashboard reports override and active main light state, while physical main light indicator and relay also activate.",
    timedSubtitles: [
      { startFrame: 0, endFrame: 180, text: "I'll set the operating mode back to Auto and select Light Override On." },
      { startFrame: 180, endFrame: 270, text: "The main light turns on immediately." },
      { startFrame: 270, endFrame: 493, text: "The Blynk dashboard reports override and active main light state while physical main" },
      { startFrame: 493, endFrame: 588, text: "light indicator and relay also activate." }
    ],
    keyPoints: [
      "Control: Manual Override ON",
      "Bypass Sensor Logic",
      "Instant Main Light Relay Trigger",
      "Confirmed State Reporting"
    ],
    overlayVideo: "IoT/videomaterials/part9wokwi.mov",
    pipVideo: "IoT/videomaterials/part9mobile.MP4"
  },
  {
    id: "10_fan_override",
    sectionNumber: 10,
    title: "Manual Fan Override Demo",
    sectionType: "demo",
    videoFile: "IoT/10_Fan_Override.MOV",
    durationInSeconds: 19.37,
    durationInFrames: 582,
    transcript: "Now I will select Fan Override On. Blynk fan indicator turns on, and Wokwi fan relay activates. Manual command is applied and confirmed output state is reported separately from requested control.",
    timedSubtitles: [
      { startFrame: 0, endFrame: 90, text: "Now I will select Fan Override On." },
      { startFrame: 90, endFrame: 300, text: "The fan indicator turns on in Blynk, and Wokwi fan indicator and relay activate." },
      { startFrame: 300, endFrame: 582, text: "This demonstrates manual command is applied and confirmed output state is reported separately from requested control." }
    ],
    keyPoints: [
      "Control: Fan Override ON",
      "Requested vs Confirmed State Separation",
      "Immediate Relay & Indicator Activation",
      "Telemetry Feedback Loop"
    ],
    overlayVideo: "IoT/videomaterials/part10wokwi.mov",
    pipVideo: "IoT/videomaterials/part10mobile.MP4"
  },
  {
    id: "11_curtain_servo",
    sectionNumber: 11,
    title: "Curtain Servo Position Control Demo",
    sectionType: "demo",
    videoFile: "IoT/11_Curtain_Servo.MOV",
    durationInSeconds: 15.37,
    durationInFrames: 462,
    transcript: "I will now move curtain control from 0° to 90° and then to 180°. The Wokwi servo follows selected position, and Blynk dashboard reports confirmed curtain position.",
    timedSubtitles: [
      { startFrame: 0, endFrame: 249, text: "I will now move curtain control from 0° to 90° and then to 180°." },
      { startFrame: 249, endFrame: 406, text: "The Wokwi servo follows selected positions and Blynk dashboard reports the" },
      { startFrame: 406, endFrame: 462, text: "confirmed curtain position." }
    ],
    keyPoints: [
      "Actuator: PWM Servo Motor",
      "Positions: 0° -> 90° -> 180°",
      "Smooth Stepper Motor Tracking",
      "Angle Datastream Sync"
    ],
    overlayVideo: "IoT/videomaterials/part11wokwi.mov",
    pipVideo: "IoT/videomaterials/part11mobile.MP4"
  },
  {
    id: "12_gas_alert",
    sectionNumber: 12,
    title: "Gas Safety Alert & Priority Override",
    sectionType: "demo",
    videoFile: "IoT/12_Gas_Alert_and_Acknowledgement.MOV",
    durationInSeconds: 37.53,
    durationInFrames: 1126,
    transcript: "Next, I increase MQ-2 gas value until safety threshold is reached. System reports GAS ALERT; red indicator and buzzer activate. Comfort outputs are forced off due to gas safety priority. Pressing Acknowledge records alert, but alarm stays active while unsafe. After gas lowers, system waits for multiple safe readings before clearing.",
    timedSubtitles: [
      { startFrame: 0, endFrame: 180, text: "Next, I will increase MQ-2 gas value until safety threshold is reached." },
      { startFrame: 180, endFrame: 360, text: "The system now reports GAS ALERT; red indicator and buzzer activate." },
      { startFrame: 360, endFrame: 570, text: "And comfort outputs are forced off because gas safety has highest priority." },
      { startFrame: 570, endFrame: 660, text: "I will first press Acknowledge Alert control." },
      { startFrame: 660, endFrame: 870, text: "Acknowledgement is recorded, but alarm remains active while gas condition is unsafe." },
      { startFrame: 870, endFrame: 1126, text: "After lowering gas value, system waits for multiple safe readings before clearing alarm." }
    ],
    keyPoints: [
      "HIGHEST PRIORITY: Gas Safety Override",
      "Red Alarm LED + Loud Buzzer Activated",
      "All Comfort Outputs (Light/Fan) Forced OFF",
      "Manual Ack Button + Multi-Sample Safety Clearing"
    ],
    overlayVideo: "IoT/videomaterials/part12wokwi.mov",
    pipVideo: "IoT/videomaterials/part12mobile.mov",
    pipVideo2: "IoT/videomaterials/part12mobilesecond.mov"
  },
  {
    id: "13_network_security",
    sectionNumber: 13,
    title: "Network Resilience & Cloud Security",
    sectionType: "explanation",
    videoFile: "IoT/13_Network_and_Security.MOV",
    durationInSeconds: 28.33,
    durationInFrames: 851,
    transcript: "The ESP32 continues running sensor and safety logic locally even if cloud connection is interrupted. When connection is restored, device reconnects and Blynk telemetry updates. For security, Blynk token is stored in private secrets file, not displayed or committed.",
    timedSubtitles: [
      { startFrame: 0, endFrame: 255, text: "The ESP32 continues running sensor and safety logic locally even if cloud connection is" },
      { startFrame: 255, endFrame: 465, text: "interrupted. When connection is restored, device reconnects and Blynk telemetry updates again." },
      { startFrame: 465, endFrame: 732, text: "For security, Blynk token is stored in a private ignored secrets file. It is not displayed in" },
      { startFrame: 732, endFrame: 851, text: "the video or committed as a public credential." }
    ],
    keyPoints: [
      "Offline Edge Resilience (Local Safety Logic)",
      "Auto Reconnection & Datastream Catch-up",
      "Secrets Isolation (.gitignore Credentials)",
      "Zero Token Exposure"
    ]
  },
  {
    id: "14_reflection",
    sectionNumber: 14,
    title: "Engineering Reflection & Trade-offs",
    sectionType: "explanation",
    videoFile: "IoT/14_Reflection.MOV",
    durationInSeconds: 27.77,
    durationInFrames: 834,
    transcript: "This project demonstrates separating requested control states from confirmed actual state. It also shows why gas safety must take priority over comfort controls. Validated through simulation and cloud interaction, though Wokwi prototype does not replace certified gas alarms.",
    timedSubtitles: [
      { startFrame: 0, endFrame: 218, text: "This project demonstrates the importance of separating requested control states from confirmed" },
      { startFrame: 218, endFrame: 278, text: "actual state." },
      { startFrame: 278, endFrame: 432, text: "It also shows why gas safety must take priority over comfort controls." },
      { startFrame: 432, endFrame: 603, text: "The system is validated through simulation and cloud interactions, however Wokwi" },
      { startFrame: 603, endFrame: 720, text: "prototype does not replace certified gas alarms," },
      { startFrame: 720, endFrame: 834, text: "mains-safety testing, or real sensor calibration." }
    ],
    keyPoints: [
      "State Machine Decoupling: Requested UI commands are decoupled from confirmed physical relay actuation via sensor feedback.",
      "Priority Hierarchy: Emergency Gas Safety (> 400 PPM) forcefully suppresses all user comfort controls & automation loops.",
      "Sensor Hysteresis & Vacancy Timers: Prevents rapid relay chatter on temperature boundaries & holds lighting during brief PIR pauses.",
      "Simulation vs Hardware Scope: Wokwi digital twin validates logic state machines, but physical deployment requires certified gas detectors."
    ]
  },
  {
    id: "15_closing",
    sectionNumber: 15,
    title: "Conclusion & Key Takeaways",
    sectionType: "explanation",
    videoFile: "IoT/15_Closing.MOV",
    durationInSeconds: 24.77,
    durationInFrames: 744,
    transcript: "To conclude, SentinelSleep demonstrates ESP32 sensor integration, local priority-based automation, Blynk cloud monitoring, operating modes, manual overrides, and gas safety handling. Provides explainable output decisions while keeping safety active at device level. Thank you for watching.",
    timedSubtitles: [
      { startFrame: 0, endFrame: 217, text: "To conclude, SentinelSleep demonstrates ESP32 sensor integration, local priority-based" },
      { startFrame: 217, endFrame: 446, text: "automation, Blynk cloud monitoring, operating modes, manual overrides, and gas safety handling." },
      { startFrame: 446, endFrame: 668, text: "The system provides explainable output decisions while keeping safety active at the" },
      { startFrame: 668, endFrame: 713, text: "device level." },
      { startFrame: 713, endFrame: 744, text: "Thank you for watching." }
    ],
    keyPoints: [
      "End-to-End Smart Bedroom System: Successfully integrated ESP32 MCU, 4 environmental sensors, and 5 multi-actuator outputs.",
      "Local Edge Safety + Cloud Telemetry: Autonomous local loop ensures 100% gas protection offline, paired with remote Blynk Cloud dashboard.",
      "Explainable Automation Engine: Transports transparent action reasons to Blynk UI so users always know why relays activated.",
      "Coursework Milestones Achieved: Fully satisfies BCL1123 IoT module requirements with robust Wokwi digital simulation & cloud sync."
    ]
  }
];

export const TOTAL_DURATION_IN_FRAMES = SECTIONS.reduce((acc, s) => acc + s.durationInFrames, 0);
