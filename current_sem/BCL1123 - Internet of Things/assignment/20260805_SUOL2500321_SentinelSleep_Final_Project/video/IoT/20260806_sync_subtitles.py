import json
import os

json_path = "/Users/jingyichan/CodingArea/assignment/current_sem/BCL1123 - Internet of Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/20260806_precise_transcriptions.json"
script_md_path = "/Users/jingyichan/CodingArea/assignment/current_sem/BCL1123 - Internet of Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/20260805_SUOL2500321_SentinelSleep_Final_Video_Script.md"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Cleaned transcript text overrides per section for crisp academic wording
CLEAN_TEXTS = {
    "01_Introduction.MOV": [
        "Hello, my name is Chan Jing Yi, and this is my final project called SentinelSleep.",
        "SentinelSleep is a smart bedroom system built using an ESP32 microcontroller,",
        "with Wokwi simulations and a Blynk IoT cloud platform.",
        "It monitors temperature, humidity, room brightness, occupancy, and gas safety.",
        "It can control the main light, fan, night light, buzzer, and curtain servo."
    ],
    "02_Hardware_and_Architecture.MOV": [
        "This is the Wokwi circuit. The DHT22 measures temperature and humidity, PIR detects occupancy,",
        "the photoresistor measures illuminance, and the MQ-2 provides gas safety input.",
        "The system contains relays for main light and fan, RGB status indicators,",
        "a night light indicator, a buzzer, and a curtain servo.",
        "The ESP32 processes sensor readings locally and sends telemetry to Blynk via virtual datastreams.",
        "The Blynk dashboard displays both sensor readings and confirmed actuator states."
    ],
    "03_Baseline_Operation.MOV": [
        "First, I will demonstrate the normal operating condition.",
        "The device is online.",
        "The temperature is approximately 27.3°C.",
        "Humidity is 65%.",
        "Illuminance is about 499 lux, and gas voltage is approximately 4.43V.",
        "The system status is SAFE, and comfort outputs are currently inactive."
    ],
    "04_Normal_Lighting.MOV": [
        "Next, I will reduce the illuminance below threshold and trigger the PIR sensor.",
        "The room is now dark and occupied. The ESP32 detects this and activates the main light.",
        "The Blynk dashboard confirms occupancy state, main light state, and active reasons.",
        "When motion stops, the vacancy timer expires and the light turns off."
    ],
    "05_Temperature_and_Humidity.MOV": [
        "Now I increase the temperature to approximately 30°C while occupied.",
        "The fan activates because the temperature is above the fan threshold.",
        "When temperature is reduced, hysteresis logic prevents rapid switching.",
        "I will now raise the humidity above 70%.",
        "The Blynk dashboard changes to COMFORT WARNING,",
        "and red and green RGB channels illuminate together to show warning condition."
    ],
    "06_Sleep_Mode.MOV": [
        "I will now select Sleep Mode.",
        "The illuminance is approximately 25 lux (below sleep lighting threshold),",
        "and the PIR detects occupancy.",
        "The night light activates while main light and fan remain off.",
        "This provides low-level lighting suitable for sleeping."
    ],
    "07_Study_Mode.MOV": [
        "Next, I will select Study Mode.",
        "The temperature is approximately 30.2°C,",
        "and illuminance is below 100 lux. Study Mode treats room as occupied.",
        "The Blynk dashboard shows occupancy,",
        "main light and fan active.",
        "Physical indicators and relays show the same confirmed output state."
    ],
    "08_Away_Mode.MOV": [
        "I will now select Away Mode.",
        "The dashboard reports Away Mode has disabled comfort outputs.",
        "Main light, fan, and night light are off.",
        "Wokwi circuit confirms outputs are inactive,",
        "preventing unnecessary operation when unoccupied."
    ],
    "09_Light_Override.MOV": [
        "I'll set operating mode back to Auto and select Light Override On.",
        "The main light turns on immediately.",
        "The Blynk dashboard reports override and active main light state,",
        "while physical main light indicator and relay also activate."
    ],
    "10_Fan_Override.MOV": [
        "Now I will select Fan Override On.",
        "Blynk fan indicator turns on, and Wokwi fan relay activates.",
        "Manual command is applied and confirmed output state is reported separately from requested control."
    ],
    "11_Curtain_Servo.MOV": [
        "I will now move curtain control from 0° to 90° and then to 180°.",
        "The Wokwi servo follows the selected position,",
        "and Blynk dashboard reports confirmed curtain position."
    ],
    "12_Gas_Alert_and_Acknowledgement.MOV": [
        "Next, I increase MQ-2 gas value until safety threshold is reached.",
        "The system now reports GAS ALERT; red indicator and buzzer activate.",
        "Comfort outputs are forced off because gas safety has highest priority.",
        "I will press Acknowledge Alert control.",
        "Acknowledgement is recorded, but alarm remains active while gas condition is unsafe.",
        "After lowering gas value, system waits for multiple safe readings before clearing alarm."
    ],
    "13_Network_and_Security.MOV": [
        "The ESP32 continues running sensor and safety logic locally even if cloud connection is interrupted.",
        "When connection is restored, device reconnects and Blynk telemetry updates.",
        "For security, Blynk token is stored in private secrets file,",
        "not displayed in video or committed as a public credential."
    ],
    "14_Reflection.MOV": [
        "This project demonstrates separating requested control states from confirmed actual state.",
        "It also shows why gas safety must take priority over comfort controls.",
        "The system is validated through simulation and cloud interaction,",
        "however Wokwi prototype does not replace certified gas alarms,",
        "mains-safety testing, or real sensor calibration.",
        "Thank you for watching."
    ],
    "15_Closing.MOV": [
        "To conclude, SentinelSleep demonstrates ESP32 sensor integration,",
        "local priority-based automation, Blynk cloud monitoring,",
        "operating modes, manual overrides, and gas safety handling.",
        "The system provides explainable output decisions while keeping safety active at device level.",
        "Thank you for watching."
    ]
}

# Process segments into frame-accurate timed subtitles
SECTION_TIMED_SUBTITLES = {}

for mov_name, mov_info in data.items():
    segments = mov_info["segments"]
    clean_lines = CLEAN_TEXTS.get(mov_name, [])
    
    timed_list = []
    for idx, seg in enumerate(segments):
        start_sec = seg["start"]
        end_sec = seg["end"]
        
        # Calculate start and end frames at 30 FPS
        start_frame = int(round(start_sec * 30))
        end_frame = int(round(end_sec * 30))
        
        # Use clean text line if index matches, otherwise Whisper text
        text = clean_lines[idx] if idx < len(clean_lines) else seg["text"]
        
        timed_list.append({
            "startFrame": start_frame,
            "endFrame": end_frame,
            "text": text
        })
    
    SECTION_TIMED_SUBTITLES[mov_name] = timed_list

# Generate TS code for sectionsData.ts
ts_output_path = "/Users/jingyichan/CodingArea/assignment/current_sem/BCL1123 - Internet of Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/20260806_sentinelsleep_video/src/sectionsData.ts"

with open(ts_output_path, "r", encoding="utf-8") as f:
    existing_ts = f.read()

print("Synchronized timed subtitles ready!")
with open("/Users/jingyichan/CodingArea/assignment/current_sem/BCL1123 - Internet of Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/20260806_timed_subtitles.json", "w", encoding="utf-8") as f:
    json.dump(SECTION_TIMED_SUBTITLES, f, indent=2)
