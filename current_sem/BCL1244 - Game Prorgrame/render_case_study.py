from pathlib import Path
import re
import markdown
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "20260723_BCL1244_Cyber_City_Rescue_Case_Study.md"
HTML = ROOT / "20260723_BCL1244_Cyber_City_Rescue_Case_Study.html"
PDF = ROOT / "20260723_BCL1244_Cyber_City_Rescue_Case_Study.pdf"


def build_html() -> str:
    raw = SOURCE.read_text(encoding="utf-8")
    body = markdown.markdown(raw, extensions=["fenced_code", "tables", "sane_lists"])
    body = re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        lambda m: '<div class="mermaid">' + m.group(1) + '</div>',
        body,
        flags=re.DOTALL,
    )
    body = body.replace("<p>\\newpage</p>", '<div class="page-break"></div>')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>BCL1244 Cyber City Rescue Mission Case Study</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<style>
@page {{ size: A4; margin: 24mm 20mm 24mm 20mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.5; color: #182235; margin: 0; }}
h1 {{ color: #0c5678; font-size: 23pt; text-align: center; margin-top: 42mm; margin-bottom: 8mm; }}
h1 + h2 {{ color: #172a44; text-align: center; border: 0; font-size: 18pt; margin-bottom: 20mm; }}
h2 {{ color: #0c5678; font-size: 16pt; border-bottom: 2px solid #12a6a6; padding-bottom: 3px; margin: 8mm 0 4mm; break-after: avoid; }}
h3 {{ color: #173f5f; font-size: 12.5pt; margin: 6mm 0 2mm; break-after: avoid; }}
p {{ text-align: justify; margin: 0 0 3.5mm; orphans: 3; widows: 3; }}
strong {{ color: #102f49; }}
hr {{ border: 0; border-top: 2px solid #12a6a6; margin: 8mm 0; }}
.page-break {{ break-before: page; }}
.mermaid {{ text-align: center; margin: 7mm auto; break-inside: avoid; }}
table {{ width: 100%; border-collapse: collapse; font-size: 9.5pt; margin: 5mm 0; break-inside: avoid; }}
th {{ background: #0c5678; color: white; text-align: left; }}
th, td {{ border: 1px solid #8ea3b8; padding: 2.5mm; vertical-align: top; }}
tbody tr:nth-child(even) {{ background: #edf5f7; }}
pre {{ background: #f3f6f8; border-left: 4px solid #12a6a6; padding: 3mm; font-size: 8.2pt; line-height: 1.35; white-space: pre-wrap; break-inside: avoid; }}
code {{ font-family: "SFMono-Regular", Consolas, monospace; }}
a {{ color: #0b6384; text-decoration: none; overflow-wrap: anywhere; }}
blockquote {{ border-left: 4px solid #12a6a6; margin-left: 0; padding-left: 4mm; color: #40566c; }}
</style>
</head>
<body>{body}
<script>mermaid.initialize({{startOnLoad:true, theme:'base', themeVariables:{{primaryColor:'#d9f1f1', primaryTextColor:'#173f5f', primaryBorderColor:'#0c7983', lineColor:'#31526f', fontFamily:'Arial'}}}});</script>
</body></html>"""


def main() -> None:
    HTML.write_text(build_html(), encoding="utf-8")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(HTML.as_uri(), wait_until="networkidle")
        page.wait_for_selector(".mermaid svg", timeout=15000)
        page.pdf(
            path=str(PDF),
            format="A4",
            print_background=True,
            display_header_footer=True,
            header_template='<div style="width:100%;font-family:Arial,sans-serif;font-size:8px;margin:0 20mm;padding-bottom:2mm;border-bottom:1px solid #9eb1c7;color:#31526f">BCL1244 Game Programming <span style="float:right">Chan Jing Yi | SUOL2500321</span></div>',
            footer_template='<div style="width:100%;font-family:Arial,sans-serif;font-size:8px;margin:0 20mm;padding-top:2mm;border-top:1px solid #9eb1c7;color:#62758a"><span>Chan Jing Yi | SUOL2500321</span><span style="float:right"><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
            margin={"top": "24mm", "right": "20mm", "bottom": "24mm", "left": "20mm"},
        )
        browser.close()
    print(HTML)
    print(PDF)


if __name__ == "__main__":
    main()
