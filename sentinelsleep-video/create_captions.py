"""Generate word-timed Remotion captions for the SentinelSleep recordings."""

from __future__ import annotations

import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

from faster_whisper import WhisperModel


ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
CAPTION_DIR = PUBLIC / "captions"
MODEL_NAME = "small.en"
SCRIPT_PATH = (
    ROOT.parent
    / "current_sem"
    / "BCL1123 - Internet of Things"
    / "20260718_SUOL2500321_Smart_Bedroom_Presentation_Script.md"
)

INITIAL_PROMPT = (
    "SentinelSleep smart bedroom presentation by Chan Jing Yi, student ID "
    "SUOL2500321. Technical terms include ESP32, DHT22, PIR, photoresistor, "
    "MQ-2, MQTT, TLS, AWS IoT Core, Wokwi, Wi-Fi, hysteresis, telemetry, "
    "occupancy, illumination, and combustible gas."
)


def clean_word(text: str) -> str:
    """Keep Whisper spacing while correcting recurring technical spellings."""
    leading = " " if text[:1].isspace() else ""
    value = text.strip()
    normalized = re.sub(r"[^a-z0-9]", "", value.lower())
    corrections = {
        "sentinelsleep": "SentinelSleep",
        "esp32": "ESP32",
        "dht22": "DHT22",
        "mq2": "MQ-2",
        "mqtt": "MQTT",
        "wokwi": "Wokwi",
        "wifi": "Wi-Fi",
        "tls": "TLS",
    }
    replacement = corrections.get(normalized)
    if replacement is None:
        return text
    suffix = value[len(value.rstrip(".,!?;:")) :]
    return leading + replacement + suffix


def reference_sections() -> list[str]:
    markdown = SCRIPT_PATH.read_text(encoding="utf-8")
    sections = re.split(r"^##\s+", markdown, flags=re.MULTILINE)[1:]
    references: list[str] = []
    for section in sections:
        body = section.split("\n", 1)[1]
        body = re.sub(r"\[[^\]]*\]\s*", "", body)
        body = re.sub(r"https?://\S+", "", body)
        references.append(" ".join(body.split()))
    if len(references) != 9:
        raise ValueError(f"Expected nine script sections, found {len(references)}")
    return references


def tokenise_reference(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:[-'.][A-Za-z0-9]+)*[.,!?;:]?", text)


def normalise_token(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def timed_reference_tokens(tokens: list[str], source: list[dict]) -> list[dict]:
    if not tokens or not source:
        return []
    start = source[0]["startMs"]
    end = source[-1]["endMs"]
    span = max(1, end - start)
    output: list[dict] = []
    for index, token in enumerate(tokens):
        token_start = start + round(span * index / len(tokens))
        token_end = start + round(span * (index + 1) / len(tokens))
        output.append(
            {
                "text": (" " if output else "") + token,
                "startMs": token_start,
                "endMs": max(token_start + 1, token_end),
                "timestampMs": token_start,
                "confidence": min(item.get("confidence") or 1 for item in source),
            }
        )
    for index, item in enumerate(output):
        item["text"] = ("" if index == 0 else " ") + item["text"].strip()
    return output


def align_to_reference(captions: list[dict], reference: str) -> list[dict]:
    reference_tokens = tokenise_reference(reference)
    matcher = SequenceMatcher(
        None,
        [normalise_token(item["text"]) for item in captions],
        [normalise_token(token) for token in reference_tokens],
        autojunk=False,
    )
    output: list[dict] = []
    for tag, rec_start, rec_end, ref_start, ref_end in matcher.get_opcodes():
        source = captions[rec_start:rec_end]
        target = reference_tokens[ref_start:ref_end]
        if tag == "equal":
            for item, token in zip(source, target, strict=True):
                output.append({**item, "text": (" " if output else "") + token})
        elif tag == "replace" and source and target:
            output.extend(timed_reference_tokens(target, source))
        elif tag == "delete":
            for item in source:
                output.append({**item, "text": (" " if output else "") + item["text"].strip()})
        # Reference-only insertions are skipped because the presenter did not say them.
    for index, item in enumerate(output):
        item["text"] = ("" if index == 0 else " ") + item["text"].strip()
    return output


def align_existing() -> None:
    references = reference_sections()
    for clip_number, reference in enumerate(references, start=1):
        path = CAPTION_DIR / f"{clip_number}.json"
        captions = json.loads(path.read_text(encoding="utf-8"))
        aligned = align_to_reference(captions, reference)
        path.write_text(
            json.dumps(aligned, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Clip {clip_number}: aligned {len(aligned)} caption tokens")


def transcribe_clip(model: WhisperModel, clip_number: int) -> tuple[list[dict], list[str]]:
    path = PUBLIC / f"{clip_number}.mp4"
    segments, _ = model.transcribe(
        str(path),
        language="en",
        beam_size=5,
        vad_filter=True,
        word_timestamps=True,
        initial_prompt=INITIAL_PROMPT,
        condition_on_previous_text=True,
    )

    captions: list[dict] = []
    transcript: list[str] = []
    for segment in segments:
        transcript.append(
            f"[{segment.start:7.2f}s -> {segment.end:7.2f}s] {segment.text.strip()}"
        )
        for word in segment.words or []:
            text = clean_word(word.word)
            if not text.strip():
                continue
            captions.append(
                {
                    "text": text,
                    "startMs": round(word.start * 1000),
                    "endMs": max(round(word.end * 1000), round(word.start * 1000) + 1),
                    "timestampMs": round(word.start * 1000),
                    "confidence": round(word.probability, 4),
                }
            )
    return captions, transcript


def main() -> None:
    CAPTION_DIR.mkdir(parents=True, exist_ok=True)
    if "--align-existing" in sys.argv:
        align_existing()
        return

    model = WhisperModel(MODEL_NAME, device="cpu", compute_type="int8")
    combined_transcript: list[str] = []

    for clip_number in range(1, 10):
        captions, transcript = transcribe_clip(model, clip_number)
        aligned = align_to_reference(captions, reference_sections()[clip_number - 1])
        (CAPTION_DIR / f"{clip_number}.json").write_text(
            json.dumps(aligned, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        combined_transcript.append(f"\n## Clip {clip_number}\n")
        combined_transcript.extend(transcript)
        print(
            f"Clip {clip_number}: {len(captions)} words, "
            f"{captions[0]['startMs'] if captions else 0}–"
            f"{captions[-1]['endMs'] if captions else 0}ms"
        )

    (CAPTION_DIR / "transcript.txt").write_text(
        "\n".join(combined_transcript).strip() + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
