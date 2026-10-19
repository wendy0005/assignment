import json

with open("20260806_precise_transcriptions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for filename, info in data.items():
    print(f"=== {filename} (Total: {info['segments'][-1]['end'] if info['segments'] else 0}s) ===")
    print(f"Full Text: {info['full_text']}\n")
    print("Segments:")
    for idx, seg in enumerate(info["segments"]):
        print(f"  [{seg['start']}s -> {seg['end']}s] ({int(seg['start']*30)}f -> {int(seg['end']*30)}f): {seg['text']}")
    print("-" * 60)
