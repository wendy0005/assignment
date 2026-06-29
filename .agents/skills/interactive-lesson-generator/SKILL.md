---
name: interactive-lesson-generator
description: "Generate self-contained interactive HTML lesson pages from tutorial transcripts, answer guides, or module lecture notes (PDF/markdown). Trigger when the user asks to create interactive learning, study guides, teaching materials, online lessons, or flashcard-style content from Q&A transcripts, lecture notes, or tutorial answers. Best for course content where material has structured sections (definitions, explanations, examples, review questions). Output is a single .html file with step-by-step progressive disclosure, Mermaid diagrams, glossary popups, search, and progress tracking. Also generates course hub index.html pages connecting multiple courses. Do NOT use for general web development, non-educational content, or PDF/PPTX conversion."
allowed-tools: Read(*), Write(*), Edit(*), Bash(*), Glob(*), Grep(*), playwright_browser_navigate(*), playwright_browser_run_code_unsafe(*)
---

# Interactive Lesson Generator

Generate a self-contained, single-file HTML interactive learning experience from course material. The page teaches content step-by-step like a classroom lesson, with progressive disclosure, visual diagrams, glossary terms, full-text search, and progress tracking.

Supports two content formats:
1. **Q&A format** — tutorial transcripts with numbered questions and answers (Database Fundamentals)
2. **Lecture/Module format** — structured markdown with topics, learning outcomes, sections, diagrams, and review questions (Internet of Things)

## Architecture

The output is a single `.html` file with:
1. **Embedded CSS** — full styling, responsive layout, dark header, card-based lesson UI
2. **Embedded JavaScript** — step navigation, tab switching, glossary modals, progress tracking, search, keyboard shortcuts
3. **Mermaid.js** via CDN — renders live diagrams
4. **JSON data structure** — lesson content defined as a JS array of objects

## Course Hub (index.html)

When creating or updating a course hub at the project root:
- Create `index.html` with styled cards linking to each course's lesson page
- Each lesson page should have a `📚 All Courses` link in the header pointing back to `index.html`
- Use relative paths: `current_sem/BCL1223 - Database Fundamentals/database_interactive_lessons.html`
- Design: dark gradient background, glassmorphism cards, course code tags

## Required Output Structure

```
<!DOCTYPE html>
<html>
  <head>
    <title>Course Name — Interactive Lessons</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style> /* ALL CSS */ </style>
  </head>
  <body>
    <header>
      <div class="header-left"> /* Title, subtitle, Teacher Mode badge */ </div>
      <div class="search-wrapper"> /* Search input + results dropdown */ </div>
      <a class="header-link" href="index.html">📚 All Courses</a>
    </header>
    <div class="tabs" id="tabsContainer"></div>
    <div class="app-layout">
      <aside class="sidebar" id="sidebar">
        <h3>Lessons</h3>
        <ul class="sidebar-list" id="sidebarList"></ul>
      </aside>
      <main class="main-content" id="mainContent"></main>
    </div>
    <div class="modal-overlay" id="glossaryModal"> /* Glossary popup */ </div>
    <script> /* ALL JavaScript */ </script>
  </body>
</html>
```

## Lesson Data Structure (JavaScript)

For Q&A transcripts, each tutorial tab contains 10 questions as lessons:
```javascript
const tutorials = [
  {
    id: 'tutorial1',
    title: 'Tutorial 1 — Topic',
    short: 'Short Name',
    questions: [
      {
        number: 1,
        title: 'Question 1 Title',
        intro: 'Teacher-style paragraph explaining why this matters.',
        steps: [
          { title: 'Step Title', body: 'HTML content', diagram: null },
          // 2-5 steps total
        ],
        recap: ['Key takeaway 1', 'Key takeaway 2']
      }
    ]
  }
];
```

For lecture/module content, each topic tab contains 2 lessons:
```javascript
const topics = [
  {
    id: 'topic1',
    title: 'Topic 1 — Name',
    short: 'Short Name',
    questions: [
      {
        number: 1, // Lesson number (1-10 across all topics)
        title: 'Lesson Title',
        intro: 'Teacher intro',
        steps: [ /* steps */ ],
        recap: [ /* takeaways */ ]
      }
    ]
  }
];
```

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
3. **Write the HTML file** — Follow the full architecture (CSS + JS + data)
4. **Create/update course hub** — If other courses exist, update `index.html` to include the new course
5. **Verify** — Serve locally with `python3 -m http.server 8000` and check:
   - All tabs render with correct badge counts
   - All lessons load and display content correctly
   - Navigation buttons work (Continue, Previous, Next Lesson)
   - Glossary terms are clickable and show modal
   - Mermaid diagrams render (check browser console for errors)
   - Search works (test multiple terms, verify results highlight in body text)
   - Progress ✓ marks update in sidebar
   - "All Courses" link goes to index.html
   - Responsive: test at 600px and 1200px widths
   - Keyboard navigation (ArrowRight, ArrowLeft, Escape, ⌘K)

## Reference Files

- `assets/template.html` — Database Fundamentals example (20 lessons across 2 tutorials, Q&A format, 1825 lines)
- `../../../iot_lessons.html` — Internet of Things example (10 lessons across 5 topics, lecture format)

## Dependencies
- Mermaid.js v10 CDN (`https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js`)
- Google Fonts (Inter + Merriweather)
- No other external dependencies — pure HTML/CSS/JS
