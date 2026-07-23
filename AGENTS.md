# Workspace Overview

This workspace hosts a **Flask + SQLite** interactive course platform for technical/security education. Content is served dynamically; standalone hardcoded HTML files are **not used**.

## Architecture

- **`server.py`** — Flask app that serves course pages from `templates/` using data from `progress.db`
- **`templates/`** — Jinja2 templates (`study.html`, `quiz.html`, `index.html`, etc.)
- **`progress.db`** — SQLite database with all course content, glossary, and quiz questions
- **`current_sem/`** — Generated/exported files (backup snapshots, not authoritative)

## Adding Learning Material — CRITICAL

**NEVER hardcode learning data into standalone HTML files.** All content must go into SQLite via a Python migration script.

### Pattern (follow `migrate_netfund.py` or `migrate_wireshark.py`):

1. Create `migrate_<topic>.py` in the project root
2. Define `GLOSSARY`, `TUTORIALS` (with lessons, steps, recaps), and `QUIZ_QUESTIONS`
3. Use the insert pattern:
   - `tutorials` table: course link, title, `c_idx`, `sort_order`
   - `lessons` table: tutorial link, number, title, intro
   - `lesson_steps` table: lesson link, title, body_html (may contain glossary {{terms}}), optional mermaid diagram
   - `lesson_recaps` table: lesson link, summary text
   - `glossary` table: course link, term, definition
   - `quiz_questions` table: course link, chapter_idx, question text, options JSON, correct_idx, explanation, optional card_ref
4. Run the script: `python3 migrate_<topic>.py`
5. Restart Flask: `python3 server.py`

### Data Flow

```
migrate_*.py → SQLite (progress.db) → Flask (server.py) → templates/study.html
```

### Quiz Chapter Mapping

Match `quiz_questions.chapter_idx` to the `c_idx` of the tutorial it belongs to. For a new chapter N, use `chapter_idx = N` and `c_idx = N`.

## Key Courses in Database

| Course ID | Name | Type |
|-----------|------|------|
| `secplus` | CompTIA Security+ (18 chapters incl. Wireshark) | Study + Quiz |
| `netfund` | Networking for Security+ | Study |
| `iot` | Internet of Things | Study |
| `bcl1223` | Database Fundamentals | Study |
| `ghf` | GitHub Foundations | Quiz only |

## Running Locally

```bash
python3 server.py
# Opens http://localhost:8000/
```

## Google Calendar Management — CRITICAL

When adding or modifying calendar events for course deadlines:
1. **Always Extract Course Details**: Locate the course code (e.g., `BCL1123`, `BCL1223`) and its full course name.
2. **Standardized Event Title Format**: Always use the format `[Course Code] [Course Name] [Event/Assignment Name]` (e.g., `BCL1223 Database Fundamentals Assignment`). Avoid generic summaries like "Assignment Submission".
3. **Keep Detailed Descriptions**: Include any context, due date labels, and attachment list references in the description field.
4. **Time Alignment**: By default, schedule the event to end exactly at the deadline time (e.g., `23:59:00` or `00:00:00`) and start 30 minutes prior.

