"""
Generic TTS audio generator for course answers.
Usage: python3 generate_tts_audio.py <answers.md> <questions.json> <output.mp3> [voice]

questions.json should be:
{
  "case_study": "optional intro text...",
  "sections": {
    "Problem Analysis": {
      "intro": "Section 1, Problem Analysis. Worth 20 marks.",
      "questions": ["Question 1A: ...", "Question 1B: ..."]
    },
    ...
  }
}
"""

import asyncio
import json
import re
import sys
import edge_tts

DEFAULT_VOICE = "en-US-JennyNeural"


def clean(text):
    lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("|") or stripped == "---":
            continue
        cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", stripped)
        cleaned = re.sub(r"`(.*?)`", r"\1", cleaned)
        cleaned = re.sub(r"<[^>]+>", "", cleaned)
        cleaned = re.sub(r">\s+", "", cleaned)
        if cleaned.startswith("#"):
            cleaned = cleaned.lstrip("#").strip()
        lines.append(cleaned)
    return " ".join(lines)


def extract_sections(md_path):
    sections = {}
    current = None
    buffer = []
    with open(md_path) as f:
        for line in f:
            m = re.match(r"^##\s+\d+\.\s+(.*)", line)
            if m:
                if current and buffer:
                    sections[current] = "\n".join(buffer)
                current = m.group(1).strip()
                buffer = []
            elif current:
                buffer.append(line)
        if current and buffer:
            sections[current] = "\n".join(buffer)
    return sections


def build_script(md_path, questions_json):
    with open(questions_json) as f:
        config = json.load(f)

    sections = extract_sections(md_path)
    parts = []

    if config.get("case_study"):
        parts.append(config["case_study"])

    for q_key, q_data in config["sections"].items():
        answer = None
        for md_key, md_val in sections.items():
            if md_key.startswith(q_key):
                answer = md_val
                break
        if not answer:
            continue

        parts.append(q_data["intro"])
        cleaned = clean(answer)

        q_list = q_data["questions"]
        if len(q_list) == 1:
            parts.append(q_list[0])
            parts.append(cleaned)
        else:
            answer_blocks = [
                s.strip()
                for s in re.split(r"(?<=\.)\s+", cleaned)
                if s.strip() and len(s.strip()) > 5
            ]
            blocks_per_q = max(1, len(answer_blocks) // len(q_list))
            idx = 0
            for q_text in q_list:
                parts.append(q_text)
                chunk = " ".join(answer_blocks[idx: idx + blocks_per_q])
                if chunk:
                    parts.append(chunk)
                idx += blocks_per_q
            if idx < len(answer_blocks):
                parts.append(" ".join(answer_blocks[idx:]))

    spoken = re.sub(r"\s+", " ", "\n\n".join(parts)).strip()
    return spoken


async def main():
    if len(sys.argv) < 4:
        print("Usage: python3 generate_tts_audio.py <answers.md> <questions.json> <output.mp3> [voice]")
        sys.exit(1)

    md_path = sys.argv[1]
    questions_path = sys.argv[2]
    output_path = sys.argv[3]
    voice = sys.argv[4] if len(sys.argv) > 4 else DEFAULT_VOICE

    spoken = build_script(md_path, questions_path)
    print(f"Generating audio ({len(spoken)} chars, voice: {voice})...")
    communicate = edge_tts.Communicate(spoken, voice)
    await communicate.save(output_path)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
