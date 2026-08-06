import os
import glob
import sys
import json
import ssl

# Disable SSL verification for model download if needed
ssl._create_default_https_context = ssl._create_unverified_context

# Ensure python can import whisper
import whisper

audio_dir = "/Users/jingyichan/CodingArea/assignment/current_sem/BCL1123 - Internet of Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/20260806_temp_audio"


wav_files = sorted(glob.glob(os.path.join(audio_dir, "*.wav")))

print(f"Loading Whisper model ('base')...")
model = whisper.load_model("base")

results = {}

for wav_file in wav_files:
    fname = os.path.basename(wav_file)
    print(f"Transcribing {fname}...")
    res = model.transcribe(wav_file, fp16=False)
    text = res["text"].strip()
    results[fname] = {
        "text": text,
        "segments": res["segments"]
    }
    print(f"  -> {fname}: {text}\n")

output_json = "/Users/jingyichan/CodingArea/assignment/current_sem/BCL1123 - Internet of Things/assignment/20260805_SUOL2500321_SentinelSleep_Final_Project/video/IoT/20260806_transcriptions.json"
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Saved transcriptions to {output_json}")
