"""Build styled HTML preview and print-ready A4 PDF for BCL2113 Case Study (20%)."""
from pathlib import Path
import html
import re
import subprocess
import urllib.request
import markdown

ROOT = Path(__file__).resolve().parent.parent
SOURCES = Path(__file__).resolve().parent
STEM = "20261125_ChanJingYi_SUOL2500321_BCL2113_Case_Study"
MD_PATH = ROOT / f"{STEM}.md"
HTML_PATH = SOURCES / f"{STEM}.html"
PDF_PATH = ROOT / f"{STEM}.pdf"
MERMAID_JS = SOURCES / "mermaid.min.js"

if not MERMAID_JS.exists():
    urllib.request.urlretrieve(
        "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js",
        MERMAID_JS,
    )

raw_md = MD_PATH.read_text(encoding="utf-8")

# Strip top title/identity lines (rendered cleanly on formal cover page)
body_lines = raw_md.splitlines()
start_idx = next(i for i, line in enumerate(body_lines) if line.startswith("## 1."))
body_md = "\n".join(body_lines[start_idx:])

# Convert inline math cleanly to italic/HTML math without requiring external MathJax CDN
def format_math(text: str) -> str:
    def repl(match):
        expr = match.group(1)
        expr = expr.replace(r"\le", "&le;").replace(r"\ge", "&ge;")
        expr = re.sub(r"\bL\b", "<em>L</em>", expr)
        return f'<span class="math">{expr}</span>'
    return re.sub(r"\$([^$]+)\$", repl, text)

# Protect mermaid code blocks before markdown conversion
mermaid_blocks = []
def stash_mermaid(match):
    idx = len(mermaid_blocks)
    mermaid_blocks.append(match.group(1).strip())
    return f"@@MERMAID_BLOCK_{idx}@@"

body_md = re.sub(r"```mermaid\n(.*?)```", stash_mermaid, body_md, flags=re.DOTALL)
body_md = format_math(body_md)

# Split Scenario 1, Scenario 2, and References into clean sections for pagination
parts = re.split(r"\n---\n", body_md)
rendered_sections = []
for idx, part in enumerate(parts):
    html_part = markdown.markdown(part.strip(), extensions=["tables", "sane_lists"])
    for m_idx, m_code in enumerate(mermaid_blocks):
        html_part = html_part.replace(
            f"<p>@@MERMAID_BLOCK_{m_idx}@@</p>",
            f'<div class="mermaid-wrap"><div class="mermaid">{html.escape(m_code)}</div></div>',
        )
    # Style table and figure captions
    html_part = re.sub(
        r"<p><em>((?:Table|Figure)\s+\d+\..*?)</em></p>",
        r'<p class="caption">\1</p>',
        html_part,
    )
    cls = "section-break" if idx > 0 else ""
    rendered_sections.append(f'<div class="report-section {cls}">{html_part}</div>')

body_html = "\n".join(rendered_sections)

# Style references hanging indent
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
    <p class="programme">BACHELOR OF INFORMATION TECHNOLOGY (HONOURS)</p>
  </div>

  <div class="cover-mid">
    <p class="module-code">BCL2113 SOFTWARE ENGINEERING</p>
    <h1 class="cover-title">Continuous Assessment: Case Study (20%)</h1>
    <p class="cover-subtitle">Boundary Value Testing for Authentication Security and Design Pattern Architecture for a Student Management System</p>
  </div>

  <table class="meta-table">
    <tr><th>Student Name</th><td>Chan Jing Yi</td></tr>
    <tr><th>Student ID</th><td>SUOL2500321</td></tr>
    <tr><th>Module</th><td>BCL2113 Software Engineering</td></tr>
    <tr><th>Assessment</th><td>Continuous Assessment Case Study (20%)</td></tr>
    <tr><th>Submission Date</th><td>25 November 2026</td></tr>
  </table>
</section>
"""

css = """
@page {
  size: A4;
  margin: 22mm 20mm 22mm 20mm;
  @top-left {
    content: "BCL2113 Software Engineering | Case Study (20%)";
    font-family: "Times New Roman", Times, serif;
    font-size: 9.5pt;
    color: #4a5568;
    border-bottom: 0.5pt solid #cbd5e0;
    padding-bottom: 3pt;
    margin-bottom: 6pt;
  }
  @top-right {
    content: "Chan Jing Yi | SUOL2500321";
    font-family: "Times New Roman", Times, serif;
    font-size: 9.5pt;
    color: #4a5568;
    border-bottom: 0.5pt solid #cbd5e0;
    padding-bottom: 3pt;
    margin-bottom: 6pt;
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
  padding-top: 16mm;
  gap: 22mm;
  min-height: 256mm;
}

.cover-top {
  text-align: center;
  border-bottom: 1.5pt solid #1a365d;
  padding-bottom: 12pt;
}
.cover-top .uni {
  font-size: 16pt;
  font-weight: 700;
  letter-spacing: 1pt;
  color: #1a365d;
  margin: 0 0 4pt;
}
.cover-top .faculty {
  font-size: 10.5pt;
  font-weight: 700;
  color: #2d3748;
  margin: 0 0 4pt;
}
.cover-top .programme {
  font-size: 10.5pt;
  color: #4a5568;
  margin: 0;
}

.cover-mid {
  text-align: center;
  margin: 18pt 0;
}
.module-code {
  font-size: 12pt;
  font-weight: 700;
  color: #2b6cb0;
  letter-spacing: 0.5pt;
  margin: 0 0 8pt;
}
.cover-title {
  font-size: 20pt;
  font-weight: 700;
  color: #1a365d;
  margin: 0 0 10pt;
  line-height: 1.25;
}
.cover-subtitle {
  font-size: 12pt;
  font-style: italic;
  color: #4a5568;
  margin: 0 auto;
  max-width: 145mm;
}

.meta-table {
  width: 100%;
  border-collapse: collapse;
  margin: 12pt 0 16pt;
  font-size: 11pt;
}
.meta-table th, .meta-table td {
  border: 0.6pt solid #a0aec0;
  padding: 6.5pt 10pt;
  text-align: left;
}
.meta-table th {
  width: 34%;
  background: #edf2f7;
  color: #1a365d;
  font-weight: 700;
}

.declaration {
  border: 0.8pt solid #718096;
  background: #f7fafc;
  padding: 11pt 13pt;
  font-size: 9.8pt;
  line-height: 1.42;
}
.declaration .decl-title {
  font-weight: 700;
  color: #1a365d;
  margin: 0 0 5pt;
  font-size: 10.5pt;
}
.declaration p {
  margin: 0 0 8pt;
  text-align: justify;
}
.sig-row {
  display: flex;
  justify-content: space-between;
  margin-top: 10pt;
  padding-top: 6pt;
  border-top: 0.5pt solid #cbd5e0;
}

.section-break {
  page-break-before: always;
}

h2 {
  font-size: 14.5pt;
  font-weight: 700;
  color: #1a365d;
  border-bottom: 1pt solid #2b6cb0;
  padding-bottom: 3pt;
  margin: 0 0 10pt;
  page-break-after: avoid;
}

h3 {
  font-size: 12pt;
  font-weight: 700;
  color: #2c5282;
  margin: 13pt 0 6pt;
  page-break-after: avoid;
}

p {
  margin: 0 0 8.5pt;
  text-align: justify;
  orphans: 3;
  widows: 3;
}

.caption {
  font-size: 10pt;
  font-style: italic;
  font-weight: 700;
  color: #2d3748;
  text-align: center;
  margin: 4pt 0 10pt;
  page-break-before: avoid;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 8pt 0 10pt;
  font-size: 9.8pt;
  line-height: 1.35;
}
thead { display: table-header-group; }
tr { page-break-inside: avoid; }
th, td {
  border: 0.6pt solid #a0aec0;
  padding: 5.5pt 6.5pt;
  vertical-align: top;
  text-align: left;
}
th {
  background: #e2e8f0;
  color: #1a365d;
  font-weight: 700;
}
tbody tr:nth-child(even) {
  background: #f8fafc;
}

code {
  font-family: "Courier New", Courier, monospace;
  font-size: 9.2pt;
  background: #edf2f7;
  padding: 1pt 3pt;
  border-radius: 2pt;
}

.math {
  font-family: "Times New Roman", Times, serif;
  white-space: nowrap;
}

.mermaid-wrap {
  margin: 10pt 0 6pt;
  text-align: center;
  page-break-inside: avoid;
}
.mermaid svg {
  max-width: 100% !important;
  height: auto !important;
  max-height: 125mm !important;
}

.references p {
  text-align: left;
  padding-left: 22pt;
  text-indent: -22pt;
  margin-bottom: 7pt;
  font-size: 10.5pt;
  line-height: 1.45;
  overflow-wrap: anywhere;
}
"""

mermaid_src = MERMAID_JS.read_text(encoding="utf-8")

full_html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>BCL2113 Software Engineering Case Study - Chan Jing Yi</title>
<style>{css}</style>
<script>{mermaid_src}</script>
</head>
<body>
{cover_html}
{body_html}
<script>
mermaid.initialize({{
  startOnLoad: true,
  securityLevel: 'loose',
  theme: 'neutral',
  fontFamily: 'Times New Roman, serif',
  flowchart: {{ useMaxWidth: true, htmlLabels: true }},
  class: {{ useMaxWidth: true }}
}});
</script>
</body>
</html>
"""

HTML_PATH.write_text(full_html, encoding="utf-8")
print(f"Wrote HTML: {HTML_PATH}")

chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cmd = [
    chrome,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--virtual-time-budget=12000",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF_PATH}",
    HTML_PATH.as_uri(),
]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Chrome error:", res.stderr)
    raise SystemExit(res.returncode)
print(f"Wrote PDF: {PDF_PATH} ({PDF_PATH.stat().st_size:,} bytes)")
