import asyncio
import re
import edge_tts

ANSWERS_PATH = "/Users/tankarhau/PycharmProjects/assignment/current_sem/BCL1233 - System Analysis/BCL1233Assignment1_Answers.md"
VOICE = "en-US-JennyNeural"
OUTPUT = "/Users/tankarhau/PycharmProjects/assignment/current_sem/BCL1233 - System Analysis/BCL1233Assignment1_Audio.mp3"

CASE_STUDY = (
    "This assignment is about a Requirement Analysis for a Hybrid Work Monitoring System. "
    "A technology company has adopted a hybrid working model where employees work either from home or the office. "
    "Currently, the company uses manual tools such as spreadsheets, chat messages, and emails to track employee attendance, task updates, and work progress. "
    "This approach has led to several issues. First, inaccurate attendance tracking. "
    "Second, lack of real-time work visibility. "
    "Third, difficulty in monitoring task progress. "
    "Fourth, communication delays between employees and managers. "
    "And fifth, no centralized reporting system. "
    "To address these issues, the company plans to develop a Hybrid Work Monitoring System. "
    "The proposed system will allow employees to digitally check in and check out. "
    "It will record work location, whether remote or office. "
    "It will enable task assignment and tracking. "
    "It will provide real-time work status updates. "
    "It will generate attendance and productivity reports. "
    "It will send notifications for tasks and meetings. "
    "And it will provide a management dashboard."
)

NARRATIVE = [
    (
        "Problem Analysis",
        "Section 1, Problem Analysis. This section is worth 20 marks.",
        [
            "Question 1 A: Identify two problems in the current manual system.",
            "Question 1 B: Analyze each problem in terms of its impact on employees, managers, and organization.",
        ],
    ),
    (
        "System Objectives",
        "Section 2, System Objectives. This section is worth 20 marks.",
        [
            "Question 2 A: Propose and explain five objectives of the Hybrid Work Monitoring System.",
        ],
    ),
    (
        "Stakeholder Analysis",
        "Section 3, Stakeholder Analysis. This section is worth 10 marks.",
        [
            "Question 3 A: Identify five stakeholders involved in the system.",
            "Question 3 B: Classify each stakeholder according to their role and involvement.",
            "Question 3 C: Describe the responsibility of each stakeholder within the system context.",
        ],
    ),
    (
        "System Requirements",
        "Section 4, System Requirements. This section is worth 20 marks.",
        [
            "Question 4 A: Specify three functional requirements describing system behaviour or functions.",
            "Question 4 B: Specify two non-functional requirements based on system quality attributes.",
        ],
    ),
    (
        "Requirement Gathering Technique",
        "Section 5, Requirement Gathering Technique. This section is worth 10 marks.",
        [
            "Question 5 A: Select one suitable requirement gathering technique for the system.",
            "Question 5 B: Justify its suitability in relation to the system context.",
            "Question 5 C: Explain its application in collecting system requirements.",
        ],
    ),
    (
        "System Function Description",
        "Section 6, System Function Description. This section is worth 10 marks.",
        [
            "Question 6 A: Select one system function from the proposed system.",
            "Question 6 B: Describe the process flow in a structured format including function specification, user roles involved, pre-conditions, sequential process flow, and post-condition.",
        ],
    ),
    (
        "System Failure Prevention",
        "Section 7, System Failure Prevention. This section is worth 10 marks.",
        [
            "Question 7 A: Discuss the importance of requirement analysis in system development and evaluate its role in minimizing system design and implementation failures.",
        ],
    ),
]


def clean(text):
    lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("|"):
            continue
        if stripped == "---":
            continue
        cleaned = stripped
        cleaned = re.sub(r"\*\*(.*?)\*\*", r"\1", cleaned)
        cleaned = re.sub(r"`(.*?)`", r"\1", cleaned)
        cleaned = re.sub(r"<[^>]+>", "", cleaned)
        cleaned = re.sub(r">\s+", "", cleaned)
        if cleaned.startswith("#"):
            cleaned = cleaned.lstrip("#").strip()
        lines.append(cleaned)
    return " ".join(lines)


def extract_sections(md):
    sections = {}
    current_key = None
    current_lines = []
    for line in md.split("\n"):
        m = re.match(r"^##\s+\d+\.\s+(.*)", line)
        if m:
            if current_key:
                sections[current_key] = "\n".join(current_lines)
            current_key = m.group(1).strip()
            current_lines = []
        elif current_key:
            current_lines.append(line)
    if current_key:
        sections[current_key] = "\n".join(current_lines)
    return sections


async def main():
    with open(ANSWERS_PATH) as f:
        md = f.read()

    sections = extract_sections(md)
    spoken_parts = [CASE_STUDY]

    for q_key, section_intro, q_list in NARRATIVE:
        answer = None
        for md_key, md_val in sections.items():
            if md_key.startswith(q_key):
                answer = md_val
                break
        if not answer:
            continue

        spoken_parts.append(section_intro)
        cleaned = clean(answer)

        # Split answer into sentence-like blocks
        answer_blocks = [
            s.strip()
            for s in re.split(r"(?<=\.)\s+", cleaned)
            if s.strip() and len(s.strip()) > 5
        ]

        if len(q_list) == 1:
            spoken_parts.append(q_list[0])
            spoken_parts.append(cleaned)
        else:
            # Split answer blocks evenly across sub-questions
            blocks_per_q = max(1, len(answer_blocks) // len(q_list))
            idx = 0
            for q_text in q_list:
                spoken_parts.append(q_text)
                chunk = " ".join(answer_blocks[idx: idx + blocks_per_q])
                if chunk:
                    spoken_parts.append(chunk)
                idx += blocks_per_q
            # Add any remaining blocks
            if idx < len(answer_blocks):
                spoken_parts.append(" ".join(answer_blocks[idx:]))

    spoken = "\n\n".join(spoken_parts)

    # Final cleanup
    spoken = re.sub(r"\s+", " ", spoken)
    spoken = spoken.strip()

    print(f"Generating narration ({len(spoken)} characters)...")
    print("Preview:")
    print(spoken[:400])
    print("...")

    communicate = edge_tts.Communicate(spoken, VOICE)
    await communicate.save(OUTPUT)
    print(f"\nAudio saved to: {OUTPUT}")


if __name__ == "__main__":
    asyncio.run(main())
