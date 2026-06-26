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

## Files

- `manifest.json` – Extension config (Chrome Manifest V3)
- `content.js` – Content script that extracts data from the DOM
- `popup.html` / `popup.css` / `popup.js` – Extension popup UI
- `icon.png` – Extension icon
