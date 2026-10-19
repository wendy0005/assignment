import os
import glob
import json
import ssl
import whisper

ssl._create_default_https_context = ssl._create_unverified_context

mov_dir = "/Users/jingyichan/CodingArea/assignment/current_sem/BCL1123 - Internet of Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT"

mov_files = [
    "01_Introduction.MOV",
    "02_Hardware_and_Architecture.MOV",
    "03_Baseline_Operation.MOV",
    "04_Normal_Lighting.MOV",
    "05_Temperature_and_Humidity.MOV",
    "06_Sleep_Mode.MOV",
    "07_Study_Mode.MOV",
    "08_Away_Mode.MOV",
    "09_Light_Override.MOV",
    "10_Fan_Override.MOV",
    "11_Curtain_Servo.MOV",
    "12_Gas_Alert_and_Acknowledgement.MOV",
    "13_Network_and_Security.MOV",
    "14_Reflection.MOV",
    "15_Closing.MOV"
]

print("Loading Whisper model ('base')...")
model = whisper.load_model("base")

precise_transcriptions = {}

for mov_name in mov_files:
    mov_path = os.path.join(mov_dir, mov_name)
    if not os.path.exists(mov_path):
        print(f"Warning: {mov_name} not found!")
        continue
    
    print(f"Transcribing {mov_name}...")
    res = model.transcribe(mov_path, fp16=False, language="en")
    
    segments = []
    for seg in res["segments"]:
        segments.append({
            "start": round(seg["start"], 2),
            "end": round(seg["end"], 2),
            "text": seg["text"].strip()
        })
    
    precise_transcriptions[mov_name] = {
        "full_text": res["text"].strip(),
        "segments": segments
    }
    print(f"  Done ({len(segments)} segments)")

output_json = os.path.join(mov_dir, "20260806_precise_transcriptions.json")
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(precise_transcriptions, f, indent=2, ensure_ascii=False)

print(f"\nSaved precise transcriptions to {output_json}")
