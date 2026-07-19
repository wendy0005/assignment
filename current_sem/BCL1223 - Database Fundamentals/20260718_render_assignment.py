#!/usr/bin/env python3
"""Render the BCL1223 Markdown assignment to styled HTML and A4 PDF."""

from pathlib import Path
import re

import markdown
from playwright.sync_api import sync_playwright


BASE = Path(__file__).resolve().parent
STEM = "20260718_Database_Fundamentals_Assignment"
MD_PATH = BASE / f"{STEM}.md"
HTML_PATH = BASE / f"{STEM}.html"
PDF_PATH = BASE / f"{STEM}.pdf"


def build_html() -> str:
    source = MD_PATH.read_text(encoding="utf-8")
    body = markdown.markdown(
        source,
        extensions=["extra", "fenced_code", "tables", "toc", "sane_lists"],
        output_format="html5",
    )
    body = re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        lambda match: f'<div class="mermaid">{match.group(1)}</div>',
        body,
        flags=re.DOTALL,
    )
    executive_marker = '<h2 id="executive-summary">'
    cover, remainder = body.split(executive_marker, 1)
    body = f'<section class="cover">{cover}</section>{executive_marker}{remainder}'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BCL1223 Database Fundamentals Assignment — Chan Jing Yi</title>
<style>
  @page {{ size: A4; margin: 18mm 16mm 20mm 16mm; }}
  * {{ box-sizing: border-box; }}
  html {{ background: #eef1f4; }}
  body {{
    max-width: 210mm; margin: 0 auto; padding: 0;
    background: #fff; color: #19212a;
    font-family: "Times New Roman", Times, serif;
    font-size: 11pt; line-height: 1.5;
  }}
  .cover {{
    height: 255mm; page-break-after: always;
    display: flex; flex-direction: column; justify-content: center;
    text-align: center; border-top: 12px solid #163a5f;
    border-bottom: 3px solid #b99142; padding: 20mm 15mm;
  }}
  .cover h1 {{ color: #163a5f; font-size: 27pt; line-height: 1.18; margin: 0 0 14mm; }}
  .cover h2 {{ border: 0; color: #354b61; font-size: 15pt; margin: 0 0 18mm; }}
  .cover p {{ text-align: center; margin: 2.8mm 0; font-size: 12pt; }}
  .cover hr {{ display: none; }}
  h1, h2, h3 {{ font-family: Arial, Helvetica, sans-serif; color: #163a5f; }}
  body > h1 {{ font-size: 20pt; line-height: 1.2; border-bottom: 2px solid #b99142;
    padding-bottom: 3mm; margin: 0 0 7mm; break-before: page; }}
  h2 {{ font-size: 14pt; line-height: 1.25; margin: 9mm 0 4mm;
    border-bottom: 1px solid #aeb9c4; padding-bottom: 1.8mm; break-after: avoid; }}
  h2#complete-entityrelationship-diagram {{ break-before: page; }}
  h3 {{ font-size: 11.5pt; margin: 6mm 0 2.5mm; break-after: avoid; }}
  p {{ margin: 0 0 4mm; text-align: justify; orphans: 3; widows: 3; }}
  a {{ color: #174d7d; text-decoration: none; overflow-wrap: anywhere; }}
  strong {{ color: #172d42; }}
  hr {{ border: 0; border-top: 1px solid #c9d1d8; margin: 7mm 0; }}
  table {{ width: 100%; border-collapse: collapse; margin: 4mm 0 6mm;
    font-size: 8.4pt; line-height: 1.27; break-inside: auto; }}
  thead {{ display: table-header-group; }}
  tr {{ break-inside: avoid; }}
  th {{ background: #163a5f; color: #fff; font-family: Arial, Helvetica, sans-serif;
    font-weight: 700; text-align: left; }}
  th, td {{ border: 0.6px solid #8796a5; padding: 1.7mm 2mm; vertical-align: top; }}
  tbody tr:nth-child(even) {{ background: #f2f5f7; }}
  code {{ font-family: "Courier New", monospace; font-size: 8.5pt; }}
  p code, td code {{ background: #eef2f5; padding: 0.2mm 0.7mm; border-radius: 2px; }}
  pre {{ background: #f4f6f8; border-left: 3px solid #b99142; padding: 3.5mm;
    margin: 4mm 0 6mm; white-space: pre-wrap; overflow-wrap: anywhere;
    line-height: 1.28; font-size: 7.6pt; break-inside: auto; }}
  pre code {{ font-size: inherit; }}
  .mermaid {{ text-align: center; margin: 0 auto 4mm;
    padding: 3mm; border: 1px solid #ccd4dc; background: white; }}
  .mermaid svg {{ display: block; margin: 0 auto; max-width: 100%; max-height: 198mm; height: auto; }}
  ul, ol {{ margin: 2mm 0 4mm 7mm; padding-left: 5mm; }}
  li {{ margin: 1mm 0; }}
  blockquote {{ border-left: 3px solid #b99142; margin: 4mm 0; padding: 2mm 4mm; color: #465565; }}
  @media print {{
    html, body {{ background: #fff; }}
    body {{ max-width: none; }}
  }}
</style>
</head>
<body>
{body}
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({{
    startOnLoad: false,
    theme: 'base',
    securityLevel: 'loose',
    er: {{ useMaxWidth: true, layoutDirection: 'TB', minEntityWidth: 115 }},
    themeVariables: {{
      primaryColor: '#edf3f8', primaryTextColor: '#172d42',
      primaryBorderColor: '#163a5f', lineColor: '#53687b',
      secondaryColor: '#fff8e8', tertiaryColor: '#f5f7f9',
      fontFamily: 'Arial, Helvetica, sans-serif', fontSize: '11px'
    }}
  }});
  window.__mermaidDone = mermaid.run({{ querySelector: '.mermaid' }});
</script>
</body>
</html>"""


def render() -> None:
    HTML_PATH.write_text(build_html(), encoding="utf-8")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.goto(HTML_PATH.as_uri(), wait_until="networkidle", timeout=120_000)
        page.wait_for_function("window.__mermaidDone !== undefined", timeout=30_000)
        page.evaluate("window.__mermaidDone")
        page.wait_for_selector(".mermaid svg", timeout=30_000)
        page.emulate_media(media="print")
        page.pdf(
            path=str(PDF_PATH),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            display_header_footer=True,
            header_template=(
                '<div style="width:100%;font-size:8px;color:#53687b;padding:0 16mm;'
                'font-family:Arial,sans-serif">BCL1223 Database Fundamentals</div>'
            ),
            footer_template=(
                '<div style="width:100%;font-size:8px;color:#53687b;padding:0 16mm;'
                'font-family:Arial,sans-serif;display:flex;justify-content:space-between">'
                '<span>Chan Jing Yi · SUOL2500321</span>'
                '<span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>'
                '</div>'
            ),
            margin={"top": "18mm", "right": "16mm", "bottom": "20mm", "left": "16mm"},
        )
        browser.close()


if __name__ == "__main__":
    render()
    print(f"Created {HTML_PATH.name}")
    print(f"Created {PDF_PATH.name}")
