---
name: course-material-ultimate-note
description: >
  Organize course materials into current/previous semesters and compile "ultimate note" markdown files.
  Triggers: reorganize folders, organize assignments, ultimate note, combine materials, extract from PDF/PPTX/PPT,
  compile notes, course material organizer, semester folder structure.
allowed-tools: "Read(*), Write(*), Edit(*), Glob(*), Grep(*), Bash(uv run python3 *), Bash(mv *), Bash(mkdir *), Bash(rm *)"
---

# Course Material Ultimate Note

Organize assignment/course folders into `current_sem/` and `previous_sems/`, and compile all lecture materials (PDFs, PPTXs, old binary PPTs) into a single "ultimate note" markdown file per module.

## Workflow

### 1. Organize Folder Structure

Given a root folder with multiple dated assignment folders and course materials:

1. Create `current_sem/` and `previous_sems/` directories at the root
2. Move current semester items into `current_sem/`:
   - Module folders (e.g., `BCL1223 - Database Fundamentals/`)
   - Module topic files (e.g., `camu-module-topics-*.md`)
3. Move all dated/past semester items into `previous_sems/`:
   - Past assignment folders (e.g., `20260321_*/`, `20260405_*/`)
   - Past loose files (e.g., `20260327_*.md`, `test_case_*.md`)
4. Keep these at root:
   - Git files (`.git/`, `.gitignore`)
   - Config folders (`.agents/`, `.claude/`, `.playwright-mcp/`)
   - Utility tools (e.g., `camu-lms-scraper/`)
   - Utility scripts (`.py` scripts, `requirements.txt`, etc.)

### 2. Compile Ultimate Note per Module

For each module folder inside `current_sem/`, run the extraction script:

```bash
uv run python3 .agents/skills/course-material-ultimate-note/scripts/extract_ultimate_note.py \
  "/path/to/current_sem/BCL1223 - Database Fundamentals"
```

Or compile all at once:

```bash
uv run python3 << 'PYEOF'
from .agents.skills.course-material-ultimate-note.scripts.extract_ultimate_note import compile_ultimate_note
import os, glob

base = "/path/to/current_sem"
for folder in sorted(os.listdir(base)):
    fp = os.path.join(base, folder)
    if os.path.isdir(fp):
        compile_ultimate_note(fp)
PYEOF
```

This will:
- Extract text from all **PDFs** using PyMuPDF (page-by-page)
- Extract text from all **PPTXs** using python-pptx (slide-by-slide)
- Attempt text extraction from old binary **PPTs** via OLE/UTF-16 scanning
- Include any existing **markdown** files in the folder
- Skip existing "ultimate note" files to avoid duplication
- Output `"{folder name} ultimate note.md"` inside each module folder

### 3. Handle Binary PPT Limitations

Old `.ppt` files (PowerPoint 97-2003 format) have limited text extraction support. If the user wants full content:
- Ask the user to open the file in PowerPoint and save as `.pptx`
- Once converted, re-run the extraction script
- Delete the old `.ppt` file after confirmation

### Dependencies

Required Python packages (install via `uv pip install`):
- `python-pptx` — Extract text from `.pptx` files
- `PyMuPDF` — Extract text from PDFs
- `olefile` — Read OLE containers for old `.ppt` extraction

### Quick Check

After compilation, verify the output:
```bash
find current_sem/ -name "*ultimate*" -type f
```
