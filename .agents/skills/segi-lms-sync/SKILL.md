---
name: segi-lms-sync
description: >
  Synchronize, crawl, and download learning materials from SEGi Camu LMS (staff-spark.segi.edu.my)
  with intelligent de-duplication so existing downloads are never overlapped or re-downloaded.
  Automatically categorizes course materials into standard folders (Course Documents, Lectures, Tutorials, E-Books).
  Prepare downloaded materials for NotebookLM, convert unsupported document or slide formats to PDF when needed,
  and create beginner-friendly learning materials whenever new notes are uploaded.
  Triggers: download course materials, sync lms, camu download, get latest course slides, avoid overlap,
  download learning materials, prepare materials for NotebookLM, NotebookLM upload, beginner study guide,
  learning materials for new notes, segi lms, lms sync.
---

# SEGi Camu LMS Synchronizer (`segi-lms-sync`)

This skill enables automated crawling, extracting, and non-overlapping incremental synchronization of course materials from the SEGi University Camu LMS platform (`https://staff-spark.segi.edu.my/lms`).

---

## 1. How Information Is Extracted

### A. Authentication & Session
The browser subagent navigates to `https://staff-spark.segi.edu.my/lms#/home-page` under the active student session (e.g., Bachelor of Computer Science ODL).

### B. Enrolled Courses Discovery
The agent lists all active semester courses either via:
1. The course dropdown / subject switcher cards on the LMS dashboard.
2. The internal API endpoint `/course/get-enrolled-courses`.

Each enrolled course exposes:
- **`code`** (e.g., `BCL1213`, `BCL1313`, `BCL1333`, `BCL2113`, `BCL2344`)
- **`name`** (e.g., `Operating Systems`, `Algorithms and Complexity`, `Software Engineering`)
- **`subjId`** (Camu internal subject identifier)

### C. Chapters & Subchapters Crawling
For each course, the agent iterates through its chapters and subchapters:
- **Chapters**: `1 Documents`, `2 Lectures and Tutorials`, `3 Assessments`, etc.
- **Subchapters**: `1.1 Introduction`, `1.2 Pro-Forma`, `1.3 E-Books`, `Topic 1`, `Tutorials`, `Lab Practices`.

### D. Direct S3 Download URLs & The Referer Requirement
Each file attachment is hosted on Amazon S3 (`segicamuattachments.s3.ap-southeast-1.amazonaws.com`).

> [!IMPORTANT]
> **S3 Bucket Referer Restriction**:
> Amazon S3 returns **HTTP 403 Forbidden** if requested without an authorized `Referer`.
> Any download request via `curl`, `requests`, or `wget` **MUST** include:
> `-H "Referer: https://staff-spark.segi.edu.my/"`

---

## 2. De-Duplication & Non-Overlapping Logic

To avoid re-downloading files that already exist on disk or re-downloading when new materials are added, the sync workflow employs a **3-tier deduplication check**:

1. **Manifest Verification (`current_sem/.lms_manifest.json`)**:
   Tracks every downloaded file by its unique identifier, filename, course, category, byte size, and timestamp. If an entry is marked synced, it is skipped.
2. **On-Disk Search**:
   Before downloading any item, the script searches the entire course directory (`current_sem/<Course Code> - <Course Name>/`). If a file with the identical name and valid size (> 0 bytes) already exists anywhere within the course directory, it is marked as `[ALREADY DOWNLOADED]` and skipped.
3. **Atomic File Writes**:
   Files are downloaded to a `.tmp` file and only renamed once transfer completes with HTTP 200 and valid content, preventing interrupted or corrupt 0-byte files from blocking future syncs.

---

## 3. Directory & Category Standards

All course folders follow the pattern specified in `AGENTS.md`:

```
current_sem/
├── <Course Code> - <Course Name>/
│   ├── Course Documents/    # Pro-forma, course briefing, welcome videos, grading scheme
│   ├── Lectures/            # Slide decks (.pdf, .pptx, .ppt), infographics, SIM documents
│   ├── Tutorials/           # Tutorial problem sets (.pdf), lab exercise sheets
│   ├── E-Books/             # Reference textbooks and e-book PDFs
│   └── assignment/          # Nested assignment briefs and student submissions
└── .lms_manifest.json       # Central tracking manifest ensuring zero overlap
```

---

## 4. Preparing Materials for NotebookLM

When the user asks to upload synchronized materials to NotebookLM, use the course-specific notebook and avoid adding sources that are already present.

1. Attempt to upload each original file first. For local files, use `nlm source add <notebook-id> --file <path> --wait` and check the result.
2. If NotebookLM rejects a document or slide deck because its file type is unsupported, make a PDF copy locally and upload that copy. Keep the downloaded original unchanged; save the PDF beside it in the same course category folder with the same base filename.
3. For legacy PowerPoint `.ppt` files, use Keynote's **File → Export To → PDF** workflow when Keynote is installed. Do not use an online converter. If Keynote presents a software licence or terms prompt, get the user's confirmation before accepting it.
4. Verify the PDF before uploading: confirm it opens, check that its page count matches the document or slide deck, and visually review rendered pages for missing or unreadable content. Then wait for NotebookLM processing and verify the source appears as processed.
5. Do not convert audio, video, code, or other non-document files to PDF as a fallback. If NotebookLM cannot process one of those files, report the specific filename and failure and leave the original untouched.
6. Report which originals uploaded, which PDFs were created, and any files that NotebookLM could not process.

### Beginner Learning Materials (Required After Uploading New Notes)

The user is new to the subjects. After each batch of new notes is successfully uploaded and processed in NotebookLM, create beginner learning materials for the affected course notebook. Treat this as a required part of every NotebookLM upload workflow, even if the user only asks to upload the notes.

1. Identify genuinely new educational lecture-note sources in that notebook. Exclude course overviews, pro-formas, administrative documents, and assessment instructions from the learning-material source set.
2. Process lecture-note sources **one at a time**. For each lecture, create a separate beginner **Start Here guide**, **easy practice quiz**, and **simple flashcards**, explicitly passing only that lecture's source ID to each generation command. Never combine multiple lectures or include the course overview in that lecture's pack.
3. Use plain language, define unfamiliar terms, introduce prerequisites before advanced ideas, give small examples, and include answers/explanations in the quiz. Keep the scope grounded in that lecture's source; do not invent course topics.
4. If the notebook already has a beginner pack for that exact lecture source, do not create an identical duplicate. If existing materials were based on several sources together, create a separate lecture-only pack so the learner can study the lecture on its own. Use clear lecture/topic labels in artifact titles.
5. If a notebook contains mismatched or misleadingly titled lecture sources, name the actual source topic in the guide and quiz rather than implying that the material covers the notebook title.
6. Wait for each artifact to finish generating and check its status. Retry status checks while generation is pending. Report any artifact that remains failed or unconfirmed instead of saying it is ready.
7. In the completion summary, link the course notebook and list the guide, quiz, and flashcards created or refreshed for each lecture. Mention any uploaded notes that NotebookLM could not process and whether the learning pack covers them.

---

## 5. Execution Workflow

### Step 1: Run Browser Crawler (When Discovering New Content)
Invoke the `browser` subagent to extract the latest items JSON from Camu LMS:

```
Navigate to https://staff-spark.segi.edu.my/lms#/home-page
Iterate over active courses and subchapters, extracting all downloadable items:
{ code, name, fileName, url, category, chapter, subchapter, id }
Output dataset as JSON to `lms_materials_all.json`.
```

### Step 2: Run Incremental Sync Script
Execute the bundled synchronization script with `.venv`:

```bash
# Standard incremental sync (skips all existing files)
.venv/bin/python .agents/skills/segi-lms-sync/scripts/sync_lms_materials.py

# Optional: Dry run to preview what would be downloaded without making changes
.venv/bin/python .agents/skills/segi-lms-sync/scripts/sync_lms_materials.py --dry-run

# Optional: Force re-download if an existing file is corrupted
.venv/bin/python .agents/skills/segi-lms-sync/scripts/sync_lms_materials.py --force
```

### Script CLI Options
- `--input <path>`: Path to extracted LMS items JSON (defaults to `lms_materials_all.json`).
- `--target-dir <path>`: Target root directory (defaults to `current_sem`).
- `--dry-run`: Reports what would be downloaded without downloading.
- `--force`: Overrides deduplication checks to force re-downloading.

### Step 3: Upload and Generate Learning Materials

For each course with newly synchronized notes, follow **Preparing Materials for NotebookLM** above, wait for new sources to process, then complete **Beginner Learning Materials** for that course before reporting the sync task finished. Use the course's existing NotebookLM notebook when available; if the notebook mapping is unclear, locate it from the user's prior context or ask only when it cannot be reliably identified.
