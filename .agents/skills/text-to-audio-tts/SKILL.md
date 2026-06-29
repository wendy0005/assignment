---
name: text-to-audio-tts
description: "Generate narrated MP3 audio from course assignment/tutorial markdown answer files using Edge TTS. Combine questions + answers into natural narration, upload to Google Drive. Triggers: text to audio, TTS, narration, generate audio, convert to speech, read answers aloud, audio for assignment, create podcast from notes"
allowed-tools: "Bash(edge-tts), Bash(pip install edge-tts), Bash(gws drive +upload), Read(*), Write(*)"
---

# Text-to-Audio TTS Skill

Generate natural-sounding narrated MP3 files from course assignment/tutorial answer markdown files using Microsoft Edge TTS, combining case study context, questions, and answers into a flowing spoken narrative.

## Workflow

### 1. Read the source files
- Read the answer markdown file (e.g. `BCL1233Assignment1_Answers.md`)
- Read the question PDF (via pypdf) to extract exact question text
- Identify the case study/context section from the PDF

### 2. Build the spoken script
Construct a natural narration structure:
- Begin with the case study as an intro
- For each section: introduce the section name and marks, then read each question followed by its answer
- Clean all markdown artifacts: remove `**`, `` ` ``, `#`, `|` table chars, `---` separators
- Format numbers and codes for speech (e.g. "FR-01" → "F R 0 1")

### 3. Generate audio
```bash
pip install edge-tts -q
python3 << 'PYEOF'
import edge_tts, asyncio
async def go():
    tts = edge_tts.Communicate(SPOKEN_TEXT, "en-US-JennyNeural")
    await tts.save(OUTPUT_PATH)
asyncio.run(go())
PYEOF
```

Voices available: `en-US-JennyNeural` (default, natural female), `en-US-GuyNeural` (male), `en-GB-SoniaNeural` (British female)

### 4. Upload to Google Drive (optional)
```bash
gws drive +upload <audio.mp3> --parent <FOLDER_ID> --name <course_name.mp3>
```

### 5. File naming convention
- Course code + description (e.g. `BCL1223_Database_Tutorial1_DatabaseConcepts.mp3`)
- Store in Google Drive folder called "Course Audio"

## Script Location
The reusable script is at: `scripts/generate_tts_audio.py`

Usage:
```bash
python3 scripts/generate_tts_audio.py <answer.md> <questions.txt> <output.mp3> [voice]
```

## Input Format
The answer markdown should have sections delimited by `## N. Section Name`. Questions can be provided as a text file with labeled sections.
