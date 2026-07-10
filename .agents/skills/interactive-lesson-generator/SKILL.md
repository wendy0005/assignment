---
name: interactive-lesson-generator
description: "Generate interactive lesson content stored in SQLite from tutorial transcripts, answer guides, or module lecture notes (PDF/markdown). Trigger when the user asks to create interactive learning, study guides, teaching materials, online lessons, or flashcard-style content from Q&A transcripts, lecture notes, or tutorial answers. Best for course content where material has structured sections (definitions, explanations, examples, review questions). Output is a Python migration script that inserts lesson data into progress.db for serving via Flask templates (step-by-step progressive disclosure, Mermaid diagrams, glossary popups, full-text search, and progress tracking). Also updates the course hub at templates/index.html. Do NOT use for general web development, non-educational content, or PDF/PPTX conversion."
allowed-tools: Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*), playwright_browser_navigate(*), playwright_browser_run_code_unsafe(*)
---

# Interactive Lesson Generator

Generate a self-contained, single-file HTML interactive learning experience from course material. The page teaches content step-by-step like a classroom lesson, with progressive disclosure, visual diagrams, glossary terms, full-text search, and progress tracking.

Supports two content formats:
1. **Q&A format** — tutorial transcripts with numbered questions and answers (Database Fundamentals)
2. **Lecture/Module format** — structured markdown with topics, learning outcomes, sections, diagrams, and review questions (Internet of Things)

## Architecture

The output is a Python script that inserts lesson content into SQLite (`progress.db`). The Flask server + Jinja2 templates handle all rendering, so no HTML file is generated.

Three content types exist:
1. **Interactive Lessons** — step-by-step with tabs, sidebar, search, Mermaid diagrams, glossary
2. **Practice Quizzes** — multiple choice with chapter filtering, shuffle, score tracking
3. **Answer Documents** — static print-formatted answer sheets for assignments/tests

## Course Hub

The course hub is `templates/index.html` — a hardcoded page with 4 course cards. To add a new course:
1. Insert content into SQLite via the migration script
2. Add a new `<a class="course-card">` element to `templates/index.html`
3. Link to `/course/<course_id>/lessons` (for lessons) or `/course/<course_id>/quiz` (for quizzes)

## Output: Python Migration Script

Write a Python script like `datamigrate.py` that inserts content into `progress.db`:

```python
import json, sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / 'progress.db'

def migrate(conn):
    c = conn.cursor()
    
    # 1. Insert course
    c.execute("INSERT OR REPLACE INTO courses (id, code, name, description, icon, course_type) VALUES (?,?,?,?,?,?)",
              ('course_id', 'CODE123', 'Course Name', 'Description', '📖', 'lesson'))
    
    # 2. Insert glossary terms
    c.execute("INSERT OR REPLACE INTO glossary (course_id, term, definition) VALUES (?,?,?)",
              ('course_id', 'Term', 'Definition'))
    
    # 3. Insert tutorials (tabs)
    c.execute("INSERT OR REPLACE INTO tutorials (id, course_id, title, short_title, sort_order) VALUES (?,?,?,?,?)",
              ('tutorial1', 'course_id', 'Tutorial 1 — Topic', 'Short', 0))
    
    # 4. Insert lessons (with steps and recaps)
    c.execute("INSERT INTO lessons (tutorial_id, number, title, intro, sort_order) VALUES (?,?,?,?,?)",
              ('tutorial1', 1, 'Lesson Title', 'Intro paragraph...', 0))
    lesson_id = c.lastrowid
    
    c.execute("INSERT INTO lesson_steps (lesson_id, title, body_html, diagram_mermaid, sort_order) VALUES (?,?,?,?,?)",
              (lesson_id, 'Step Title', '<p>HTML content</p>', None, 0))
    
    c.execute("INSERT INTO lesson_recaps (lesson_id, text, sort_order) VALUES (?,?,?)",
              (lesson_id, 'Key takeaway', 0))
    
    conn.commit()

if __name__ == '__main__':
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    migrate(conn)
    conn.close()
    print("Migration complete")
```

## Lesson Data Structure

Content is stored across these SQLite tables:

```
courses (id, code, name, description, icon, course_type)
tutorials (id, course_id, title, short_title, sort_order)
lessons (id, tutorial_id, number, title, intro, sort_order)
lesson_steps (id, lesson_id, title, body_html, diagram_mermaid, sort_order)
lesson_recaps (id, lesson_id, text, sort_order)
glossary (id, course_id, term, definition)
quiz_questions (id, course_id, chapter_idx, question_text, options_json, correct_idx, explanation, sort_order)
quiz_chapters (id, course_id, chapter_idx, name)
document_sections (id, course_id, section_number, title, content_html, sort_order)
```

For Q&A transcripts, each tutorial tab contains ~10 questions as lessons. For lecture/module content, each topic tab contains ~2 lessons.

The same content structuring rules apply as before — each lesson has 2-5 steps, an intro, and a recap.

## Content Processing Rules

### For Q&A Transcripts
- Each question and its sub-questions (a, b, c) become one lesson
- The intro explains why this question matters at this point in the learning journey
- Break long answers into 2-5 progressive steps
- Step 1: Introduce the concept with definition
- Middle steps: Examples, comparisons, diagrams, real-world applications
- Last step: "Why it matters" or practical application

### For Lecture/Module Markdown
Each topic (numbered 1 to N) typically contains these sections:
- **Topic Overview** — use as the intro for the first lesson
- **Learning Outcome** — reference the LO numbers but don't make a separate step
- **Interactive SIM** — the main content body. Break into 2-4 lessons per topic:
  - Lesson 1: Core concepts (first half of SIM content)
  - Lesson 2: Applications / advanced topics (second half)
- **Discussion** — incorporate as real-world examples in steps
- **Additional Resources** — skip (not lesson content)
- **Reflection Activity** — can become the "why it matters" step
- **Overall Feedback** — skip

### Handling Embedded Mermaid Diagrams in Source Material
When the source markdown contains Mermaid diagrams (in ````mermaid ... ```` blocks):
1. Extract the diagram definition string
2. Clean it up — remove any figure caption lines (like `Figure 2.1: ...`)
3. Fix indentation issues (remove excess leading whitespace)
4. Include as `diagram` property in the step data
5. The diagram will render automatically via Mermaid.js

⚠️ **Mermaid Gotcha — double quotes inside `[...]` node labels:**
  Mermaid 10.x treats `"` inside square bracket node labels as syntax, causing parse errors.
  ```
  S[Sensor: "value"]   → ✨ Syntax error in Mermaid 10.x
  S[Sensor: value]     → ✅ OK
  S[Sensor: #quot;value#quot;]  → ✅ OK (if quotes are essential)
  ```
  Always strip literal double quotes from node label text, or use `#quot;` entity.

### Review Questions in Source Material
Source material often has multiple-choice review questions (MCQs, true/false, matching tasks). The interactive lesson format does NOT make these auto-checkable — they are displayed as plain text within step body content for the student to think about. Do not add quiz/answer-checking logic.

### Glossary Integration
- Define key terms in a `glossary` object at the JS top level
- In step body text, mark glossary terms as `{{TermName}}` — `processBody()` auto-converts to clickable spans
- Terms to always include: core subject concepts (IoT, RFID, Sensor, NB-IoT, MQTT, etc. for IoT; Database, DBMS, SQL, etc. for DB)
- Glossary definitions: 1-2 sentences with concrete example where possible

### Content Formatting
- Use `<div class="highlight-box">` for key concepts, definitions, important takeaways
- Use `<div class="example-box">` for real-world examples (prepends 💡 automatically via CSS)
- Use `<table>` for comparisons (before/after, pros/cons, feature comparisons)
- Use `<strong>` for emphasis on key terms within paragraphs
- Keep paragraphs short — 2-4 sentences max
- Use step titles as mini-headings that reveal one new idea per step

### Embedding External Images
When teaching hardware, protocols, or physical concepts (e.g., RS-232 pinouts, CAN bus topology, sensor wiring), embed real-world reference images from **Wikimedia Commons** to help students visually identify components and architectures.

**CSS classes to add in `<style>`:**
```css
.img-box { background: #fff; border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 16px; margin: 18px 0; text-align: center; }
.img-box img { max-width: 100%; height: auto; border-radius: 4px; }
.img-box .img-caption { font-size: 12px; color: var(--slate-light); margin-top: 8px; font-style: italic; }
```

**Usage in step body:**
```html
<div class="img-box">
  <img src="https://upload.wikimedia.org/wikipedia/commons/..." alt="Brief description">
  <div class="img-caption">Caption explaining what the image shows.</div>
</div>
```

**Where to find images:**
- Wikipedia articles for the topic (e.g., RS-232, CAN bus) — extract `.svg` or `.png` URLs from the infobox or figures
- Use the Wikimedia Commons URL pattern: `https://upload.wikimedia.org/wikipedia/commons/...`
- Prefer `.svg` diagrams for schematics/pinouts (scalable); `.png` for photographs of hardware
- Always include an `alt` attribute for accessibility and a caption `<div>` for context
- Add an `<h4>` heading before each image group to structure the content

### Mermaid Diagrams to Include

| Subject | Diagram Type | Concepts |
|---------|------------|----------|
| Database | `flowchart LR` | Data→Info flow, DBMS architecture, Centralized vs Distributed, Keys hierarchy |
| Database | `flowchart TB` | Normalization before/after, Site A/B communication |
| Database | `flowchart LR` with subgraphs | Failure scenarios |
| IoT | `flowchart TD` | 4-layer IoT architecture, 5G network slicing, 1+2+N smart home |
| IoT | `flowchart LR` | Sensor working principle, RFID vs barcode, AIoT edge processing |
| IoT | `graph LR`/`graph TD` | V2X communication, CAN bus topology, LoRaWAN star topology |
| IoT | `sequenceDiagram` | RFID read sequence, NB-IoT PSM sleep cycle |

Style diagrams consistently:
- `fill:#dbeafe,stroke:#3b82f6` for primary elements (blue — main concepts)
- `fill:#f0fdf4,stroke:#059669` for secondary elements (green — results, positive)
- `fill:#fef3c7,stroke:#f59e0b` for tertiary elements (amber — examples, highlights)
- `fill:#fecaca,stroke:#ef4444` for error/failure elements (red — problems, bad states)
- `fill:#002b5e,color:#fff` for title/brain elements (dark navy)

## Search Implementation

The search must index the FULL body text of each step (not truncated to 120 chars):

```javascript
function buildSearchIndex() {
  searchIndex = [];
  // For each lesson step, store full stripped body text
  searchIndex.push({
    tutorialIdx, lessonIdx, stepIdx,
    path: "Topic · L1",
    title: "Lesson — Step",
    fullText: stripHtml(step.body) // FULL text, no substring
  });
}
function makeSnippet(text, query, contextLen) {
  // Find match position, extract contextLen chars on each side
  // Returns "…context…matched…context…"
}
```

This avoids the bug where long step bodies had their searchable content truncated.

## Design Specifications

### Colors (CSS Variables)
```css
--navy: #0f172a; --slate: #334155; --slate-light: #64748b;
--blue: #3b82f6; --blue-light: #eff6ff; --blue-dark: #1e40af;
--teal: #14b8a6; --teal-light: #f0fdfa;
--amber: #f59e0b; --amber-light: #fffbeb;
--rose: #f43f5e; --rose-light: #fff1f2;
--bg: #f8fafc; --card: #ffffff; --border: #e2e8f0;
```

### Layout
- **Sticky header** — dark gradient, flex layout with title left, search center, "All Courses" link right
- **Sticky tabs** — below header, one tab per tutorial/topic with lesson count badges
- **Sidebar** — 280px wide, sticky, scrollable list of lessons with `L1`, `L2` etc. numbers and ✓ progress marks
- **Main content** — flexible, max 1400px container, card-based lessons
- **Responsive** — sidebar hidden below 900px, search goes full-width on mobile

### Search Bar
- Magnifying glass icon left, input field, clear button (✕) right
- Results dropdown below with: path (topic + lesson), title, highlighted snippet
- Keyboard: ArrowUp/Down to navigate, Enter to select, Escape to close
- `⌘K` or `Ctrl+F` to focus search from anywhere

### Step Navigation
- Step progress dots (done=green, current=blue scaled up, future=gray faded)
- "← Previous" button (disabled on step 1)
- "Continue →" button, turns into "Next Lesson →" on last step
- Recap box on final step with ✓ bullet takeaways
- Keyboard: ArrowRight=next, ArrowLeft=prev

### Glossary Modal
- Overlay with backdrop blur
- Centered card with term title + definition
- "Got it" button or click backdrop to close

## Implementation Flow

1. **Read source material** — Read the transcript/markdown file. Identify structure:
   - For Q&A: extract all questions and sub-questions
   - For lecture markdown: extract topics, sections, embedded diagrams, review questions
2. **Structure content** — Group into tutorials/topics. Each gets 2-10 lessons. Each lesson gets 2-5 steps.
3. **Write the migration script** — Create a Python script (or add to `datamigrate.py`) that inserts the structured content into `progress.db` using the SQLite tables described above.
4. **Run the migration** — Execute the script to populate the database:
   ```bash
   cd /path/to/project && .venv/bin/python3 your_migration_script.py
   ```
5. **Add course card to hub** — Edit `templates/index.html` to add a new `<a class="course-card">` for the new course, linking to `/course/<course_id>/lessons` or `/course/<course_id>/quiz`.
6. **Verify** — Start the Flask server and check:
   ```bash
   PORT=8080 .venv/bin/python3 server.py
   ```
   - Visit `http://localhost:8080/course/<course_id>/lessons` and verify:
     - All tabs render with correct badge counts
     - All lessons load and display content correctly
     - Navigation buttons work (Continue, Previous, Next Lesson)
     - Glossary terms are clickable and show modal
     - Mermaid diagrams render (check browser console for errors)
     - External images load (check browser console for 404s)
     - Search works (test multiple terms, verify results highlight in body text)
     - Progress ✓ marks update in sidebar
     - "All Courses" link goes to `/`
     - Keyboard navigation (ArrowRight, ArrowLeft, Escape, ⌘K)

## Reference Files

- `server.py` — Flask app with all routes and DB initialization
- `templates/lesson.html` — Lesson viewer template (copy of iot_lessons.html with data injection)
- `templates/quiz.html` — Quiz template (for Security+ style quizzes)
- `templates/quiz_ghf.html` — Quiz template with profile system (for GitHub Foundations style)
- `templates/document.html` — Answer document template
- `datamigrate.py` — Example migration script showing all table insert patterns
- `progress.db` — SQLite database with all migrated content

## Dependencies
- Flask (`pip install flask`)
- json5 (`pip install json5`) — for parsing JS literals in migration scripts
- Python 3.10+
- Mermaid.js v10 CDN (loaded by templates)
- Google Fonts Inter + Merriweather (loaded by templates)
