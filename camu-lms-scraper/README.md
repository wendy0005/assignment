# Camu LMS Scraper

Chrome extension to extract course content from Camu LMS pages.

## Installation (Developer Mode)

1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer mode** (toggle top-right)
3. Click **Load unpacked**
4. Select the `camu-lms-scraper` folder
5. The extension icon will appear in your toolbar

## Usage

1. Navigate to a Camu LMS course content page (e.g. `staff-spark.segi.edu.my/lms`)
2. Click the extension icon
3. **Scrape Current Page** – extracts the currently visible content
4. **Scrape All Items** – clicks through every topic item and collects all content
5. Export as **JSON** or **Markdown**, or copy to clipboard

## Supported layouts

The extension detects the page layout automatically:

- **Topic/COMPLETE accordion layout** (e.g. BCL1123 IoT) – extracts text
  content (Quill editors / iframes) and exports it.
- **Nested sections layout** (e.g. BCL1213 Operating Systems) – the content
  page is built from collapsible sections (`1 Documents`,
  `2 Lectures and Tutorials`, `3 Assessments`) with sub-sections and item
  rows. The popup shows a single **Extract Everything** button (no topic
  selection) and grabs every item in the course:
  - **FILE** items → resolves full attachment metadata through the item API,
    keeps the original extension (PDF, PNG, etc.), and downloads the file.
  - **PAGE** items → exports full HTML, text, and linked resources to JSON;
    embedded images are downloaded separately.

  The full course outline is always enumerated through the site's APIs,
  including sections that are collapsed in the sidebar. Empty sections are
  recorded, and API/download errors produce a partial result instead of a
  false success. Downloads are saved under `Downloads/Camu Materials/<Course Name>/`;
  Chrome's downloads API confirms completion before an item is marked saved.
  A course materials JSON export is saved automatically after extraction.

### Course folders and skip existing downloads (v1.3.2)

Each course gets its own folder automatically, for example
`Downloads/Camu Materials/BCL1313 - Algorithms and Complexity/`.

Before fetching an attachment, the scraper checks Chrome download history for
an existing completed file in `Downloads/Camu Materials/<Course Name>/`. Existing files are
marked **already saved** and skipped, including embedded page images. Deleted
or interrupted downloads are retried. Changed attachment URLs or image content
are downloaded again, replacing the old filename. An unchanged JSON export is
also skipped. Older scraper downloads within the same course folder are recognized by their exact filename
on the first run; later runs track source revisions in extension storage.

This uses Chrome's download history and file existence flags. Files manually
moved/renamed or copied outside Chrome cannot be discovered by the extension;
clearing download history also prevents recognizing those files.

After reloading the extension, refresh the Camu tab once. If Camu shows
“All Courses” after navigating a deep link, select the course from the LMS
course dashboard first. Keep the popup open to see progress; extraction itself
runs in the content tab. Do not navigate away or reload that tab during a run.

### Verified on 2026-10-01

BCL1213 Operating Systems: all 15 sections enumerated, with 8 currently
published items (5 PDFs, 1 PNG attachment, and 2 information pages).
Chapters 2–7, Links, and Assessments currently return no published items.
These counts describe the live course at extraction time and may change.

## Files

- `manifest.json` – Extension config (Chrome Manifest V3)
- `inject.js` – MAIN-world script (document_start) that captures the course
  context IDs from the site's own API requests (published on
  `<html data-camu-ctx="...">` so `content.js` can call the same APIs)
- `content.js` – Content script that extracts data from the DOM / site APIs
- `popup.html` / `popup.css` / `popup.js` – Extension popup UI
- `icon.png` – Extension icon
