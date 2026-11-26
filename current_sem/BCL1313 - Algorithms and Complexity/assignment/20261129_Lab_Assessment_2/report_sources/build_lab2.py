"""Generate terminal screenshots, styled HTML, A4 PDF, and clean submission ZIP for BCL1313 Lab Assessment 2."""
from pathlib import Path
import html
import re
import subprocess
import zipfile
import markdown

ROOT = Path(__file__).resolve().parent.parent
SOURCES = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"
STEM = "20261126_ChanJingYi_SUOL2500321_Lab_Assessment_2"
MD_PATH = ROOT / f"{STEM}.md"
HTML_PATH = SOURCES / f"{STEM}.html"
PDF_PATH = ROOT / f"{STEM}.pdf"
ZIP_PATH = ROOT / f"{STEM}_Submission.zip"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Reuse cached mermaid.min.js if available in BCL2113 folder, else download via curl
MERMAID_JS = SOURCES / "mermaid.min.js"
CACHED_MERMAID = Path("/Users/jingyichan/CodingArea/assignment/current_sem/BCL2113 - Software Engineering/assignment/20261125_Case_Study_20/report_sources/mermaid.min.js")
if not MERMAID_JS.exists():
    if CACHED_MERMAID.exists():
        MERMAID_JS.write_bytes(CACHED_MERMAID.read_bytes())
    else:
        subprocess.run(
            ["curl", "-fsSL", "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js", "-o", str(MERMAID_JS)],
            check=True,
        )

# 1. Split unaltered demo_output.txt into 4 logical evidence screenshots
demo_text = (EVIDENCE / "demo_output.txt").read_text(encoding="utf-8").strip()
chunks = re.split(r"(?=^=== TASK )", demo_text, flags=re.MULTILINE)
chunks = [c.strip() for c in chunks if c.strip()]
# chunks: [TASK 1, TASK 2A, TASK 2B, TASK 3, TASK 4]
captures = [
    ("01_dataset_and_insertion_sort", chunks[0] + "\n\n" + chunks[1], "Task 1 & Task 2A | Dataset Setup & Insertion Sort (C++17)"),
    ("02_merge_sort", chunks[2], "Task 2B | Merge Sort Ascending by Price (C++17)"),
    ("03_searching_results", chunks[3], "Task 3 | Linear Search & Binary Search Results (C++17)"),
    ("04_scalability_benchmark", chunks[4], "Task 4 | Scalability Benchmark: n = 10 vs n = 1,000 (C++17)"),
]

for name, text_out, header_title in captures:
    lines = text_out.splitlines()
    height_px = max(240, 120 + len(lines) * 23)
    shot_html = SOURCES / f"{name}.html"
    shot_png = EVIDENCE / f"{name}.png"
    shot_html.write_text(
        f"""<!doctype html><meta charset="utf-8"><style>
        *{{box-sizing:border-box}}body{{margin:0;padding:18px;background:#ffffff}}
        .term{{width:920px;border:1px solid #cbd5e0;border-radius:6px;overflow:hidden;box-shadow:0 2px 6px rgba(0,0,0,0.06)}}
        .bar{{background:#1a365d;color:#f7fafc;padding:9px 16px;font:600 14px -apple-system,Arial,sans-serif}}
        pre{{margin:0;padding:14px 18px;font:14px/1.45 "Menlo","Courier New",monospace;color:#1a202c;background:#f8fafc;white-space:pre}}
        </style><div class="term"><div class="bar">{html.escape(header_title)}</div><pre>{html.escape(text_out)}</pre></div>""",
        encoding="utf-8",
    )
    subprocess.run(
        [
            CHROME,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            f"--window-size=956,{height_px}",
            f"--screenshot={shot_png}",
            shot_html.as_uri(),
        ],
        check=True,
        capture_output=True,
    )
    print(f"Captured screenshot: {shot_png.name} ({shot_png.stat().st_size:,} bytes)")

# 2. Parse Markdown & verify Self-Reflection word count
raw_md = MD_PATH.read_text(encoding="utf-8")
refl_match = re.search(r"## 5\. Self Reflection\n+(.*?)\n+---", raw_md, flags=re.S)
refl_words = len(re.findall(r"\S+", refl_match.group(1))) if refl_match else 0
print(f"Self-Reflection word count: {refl_words} (target: 150-200)")

body_lines = raw_md.splitlines()
start_idx = next(i for i, line in enumerate(body_lines) if line.startswith("## 1."))
body_md = "\n".join(body_lines[start_idx:])

def format_math(text: str) -> str:
    def repl(match):
        expr = match.group(1)
        expr = expr.replace(r"\log_2", "log<sub>2</sub>").replace(r"\log", "log")
        expr = expr.replace(r"\lceil", "&lceil;").replace(r"\rceil", "&rceil;")
        expr = expr.replace(r"\approx", "&approx;").replace(r"\le", "&le;")
        expr = expr.replace("n^2", "<em>n</em><sup>2</sup>")
        expr = re.sub(r"\bn\b", "<em>n</em>", expr)
        return f'<span class="math">{expr}</span>'
    return re.sub(r"\$([^$]+)\$", repl, text)

mermaid_blocks = []
def stash_mermaid(match):
    idx = len(mermaid_blocks)
    mermaid_blocks.append(match.group(1).strip())
    return f"@@MERMAID_BLOCK_{idx}@@"

body_md = re.sub(r"```mermaid\n(.*?)```", stash_mermaid, body_md, flags=re.DOTALL)
body_md = format_math(body_md)

parts = re.split(r"\n---\n", body_md)
rendered_sections = []
for idx, part in enumerate(parts):
    html_part = markdown.markdown(part.strip(), extensions=["tables", "sane_lists"])
    for m_idx, m_code in enumerate(mermaid_blocks):
        html_part = html_part.replace(
            f"<p>@@MERMAID_BLOCK_{m_idx}@@</p>",
            f'<div class="mermaid-wrap"><div class="mermaid">{html.escape(m_code)}</div></div>',
        )
    # Fix relative image paths to absolute file URIs for HTML in report_sources/
    html_part = re.sub(
        r'src="(evidence/[^"]+)"',
        lambda m: f'src="{(ROOT / m.group(1)).as_uri()}"',
        html_part,
    )
    html_part = re.sub(
        r"<p><em>((?:Table|Figure)\s+\d+\..*?)</em></p>",
        r'<p class="caption">\1</p>',
        html_part,
    )
    cls = "section-break" if idx > 0 else ""
    rendered_sections.append(f'<div class="report-section {cls}">{html_part}</div>')

body_html = "\n".join(rendered_sections)
body_html = re.sub(
    r"(<h2[^>]*>References</h2>)(.*?)</div>$",
    r'\1<div class="references">\2</div></div>',
    body_html,
    flags=re.DOTALL,
)

cover_html = """
<section class="cover-page">
  <div class="cover-top">
    <p class="uni">SEGi UNIVERSITY</p>
    <p class="faculty">FACULTY OF ENGINEERING, BUILT ENVIRONMENT AND INFORMATION TECHNOLOGY</p>
    <p class="programme">BACHELOR OF COMPUTER SCIENCE (HONOURS)</p>
  </div>

  <div class="cover-mid">
    <p class="module-code">BCL1313 ALGORITHMS AND COMPLEXITY</p>
    <h1 class="cover-title">Lab Assessment 2: Sorting and Searching in Inventory Management</h1>
    <p class="cover-subtitle">Bakery Shop Inventory System Implemented in C++17 Using Insertion Sort, Merge Sort, Linear Search, and Binary Search</p>
  </div>

  <table class="meta-table">
    <tr><th>Student Name</th><td>Chan Jing Yi</td></tr>
    <tr><th>Student ID</th><td>SUOL2500321</td></tr>
    <tr><th>Module</th><td>BCL1313 Algorithms and Complexity</td></tr>
    <tr><th>Assessment</th><td>Individual Lab Assessment 2 (20%)</td></tr>
    <tr><th>Implementation Language</th><td>C++17</td></tr>
    <tr><th>Submission Date</th><td>26 November 2026</td></tr>
  </table>
</section>
"""

css = """
@page {
  size: A4;
  margin: 21mm 19mm 21mm 19mm;
  @top-left {
    content: "BCL1313 Algorithms and Complexity | Lab Assessment 2";
    font-family: "Times New Roman", Times, serif;
    font-size: 9.5pt;
    color: #4a5568;
    border-bottom: 0.5pt solid #cbd5e0;
    padding-bottom: 3pt;
    margin-bottom: 5pt;
  }
  @top-right {
    content: "Chan Jing Yi | SUOL2500321";
    font-family: "Times New Roman", Times, serif;
    font-size: 9.5pt;
    color: #4a5568;
    border-bottom: 0.5pt solid #cbd5e0;
    padding-bottom: 3pt;
    margin-bottom: 5pt;
  }
  @bottom-left {
    content: "Chan Jing Yi (SUOL2500321)";
    font-family: "Times New Roman", Times, serif;
    font-size: 9.5pt;
    color: #4a5568;
    border-top: 0.5pt solid #cbd5e0;
    padding-top: 3pt;
  }
  @bottom-right {
    content: "Page " counter(page) " of " counter(pages);
    font-family: "Times New Roman", Times, serif;
    font-size: 9.5pt;
    color: #4a5568;
    border-top: 0.5pt solid #cbd5e0;
    padding-top: 3pt;
  }
}
@page :first {
  margin: 18mm 20mm 18mm 20mm;
  @top-left { content: none; }
  @top-right { content: none; }
  @bottom-left { content: none; }
  @bottom-right { content: none; }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: "Times New Roman", Times, serif;
  font-size: 11.5pt;
  line-height: 1.5;
  color: #1a202c;
  background: #ffffff;
}
.cover-page {
  page-break-after: always;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding-top: 18mm;
  gap: 20mm;
  min-height: 256mm;
}
.cover-top { text-align: center; border-bottom: 1.5pt solid #1a365d; padding-bottom: 12pt; }
.cover-top .uni { font-size: 16pt; font-weight: 700; letter-spacing: 1pt; color: #1a365d; margin: 0 0 4pt; }
.cover-top .faculty { font-size: 10.5pt; font-weight: 700; color: #2d3748; margin: 0 0 4pt; }
.cover-top .programme { font-size: 10.5pt; color: #4a5568; margin: 0; }
.cover-mid { text-align: center; }
.module-code { font-size: 12pt; font-weight: 700; color: #2b6cb0; letter-spacing: 0.5pt; margin: 0 0 8pt; }
.cover-title { font-size: 19pt; font-weight: 700; color: #1a365d; margin: 0 0 10pt; line-height: 1.25; }
.cover-subtitle { font-size: 11.5pt; font-style: italic; color: #4a5568; margin: 0 auto; max-width: 150mm; }
.meta-table { width: 100%; border-collapse: collapse; font-size: 11pt; }
.meta-table th, .meta-table td { border: 0.6pt solid #a0aec0; padding: 6.5pt 10pt; text-align: left; }
.meta-table th { width: 36%; background: #edf2f7; color: #1a365d; font-weight: 700; }
.section-break { page-break-before: always; }
h2 { font-size: 14pt; font-weight: 700; color: #1a365d; border-bottom: 1pt solid #2b6cb0; padding-bottom: 3pt; margin: 0 0 9pt; page-break-after: avoid; }
h3 { font-size: 12pt; font-weight: 700; color: #2c5282; margin: 12pt 0 5pt; page-break-after: avoid; }
p { margin: 0 0 8pt; text-align: justify; orphans: 3; widows: 3; }
.caption { font-size: 9.8pt; font-style: italic; font-weight: 700; color: #2d3748; text-align: center; margin: 3pt 0 10pt; page-break-before: avoid; }
table { width: 100%; border-collapse: collapse; margin: 7pt 0 8pt; font-size: 9.5pt; line-height: 1.32; }
thead { display: table-header-group; }
tr { page-break-inside: avoid; }
th, td { border: 0.6pt solid #a0aec0; padding: 5pt 6pt; vertical-align: top; }
th { background: #e2e8f0; color: #1a365d; font-weight: 700; }
tbody tr:nth-child(even) { background: #f8fafc; }
code { font-family: "Courier New", Courier, monospace; font-size: 9.2pt; background: #edf2f7; padding: 1pt 3pt; border-radius: 2pt; }
img { max-width: 100%; height: auto; display: block; margin: 6pt auto 2pt; page-break-inside: avoid; }
.mermaid-wrap { margin: 8pt 0 4pt; text-align: center; page-break-inside: avoid; }
.mermaid svg { max-width: 100% !important; height: auto !important; }
.references p { text-align: left; padding-left: 22pt; text-indent: -22pt; margin-bottom: 7pt; font-size: 10.5pt; line-height: 1.45; }
"""

full_html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>BCL1313 Lab Assessment 2 - Chan Jing Yi</title>
<style>{css}</style>
<script>{MERMAID_JS.read_text(encoding="utf-8")}</script>
</head><body>
{cover_html}
{body_html}
<script>
mermaid.initialize({{ startOnLoad: true, securityLevel: 'loose', theme: 'neutral', fontFamily: 'Times New Roman, serif' }});
</script>
</body></html>"""

HTML_PATH.write_text(full_html, encoding="utf-8")

subprocess.run(
    [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--virtual-time-budget=12000",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF_PATH}",
        HTML_PATH.as_uri(),
    ],
    check=True,
    capture_output=True,
)
print(f"Wrote PDF: {PDF_PATH.name} ({PDF_PATH.stat().st_size:,} bytes)")

# 3. Package clean submission ZIP (ONLY required deliverables)
deliverables = [
    (PDF_PATH, PDF_PATH.name),
    (ROOT / "bakery_inventory.cpp", "bakery_inventory.cpp"),
    (EVIDENCE / "01_dataset_and_insertion_sort.png", "evidence/01_dataset_and_insertion_sort.png"),
    (EVIDENCE / "02_merge_sort.png", "evidence/02_merge_sort.png"),
    (EVIDENCE / "03_searching_results.png", "evidence/03_searching_results.png"),
    (EVIDENCE / "04_scalability_benchmark.png", "evidence/04_scalability_benchmark.png"),
]
with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for src, arcname in deliverables:
        zf.write(src, arcname)
print(f"Wrote Submission ZIP: {ZIP_PATH.name} ({ZIP_PATH.stat().st_size:,} bytes)")
