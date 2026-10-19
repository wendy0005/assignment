from pathlib import Path

import markdown


BASE_DIR = Path(__file__).resolve().parent
SOURCE = BASE_DIR / "20260801_SUOL2500321_BCL1123_IoT_Test_Answers.md"
OUTPUT = BASE_DIR / "20260801_SUOL2500321_BCL1123_IoT_Test_Answers.html"


body = markdown.markdown(
    SOURCE.read_text(encoding="utf-8"),
    extensions=["tables", "sane_lists"],
)

html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>BCL1123 Internet of Things Test Answers</title>
<style>
  @page {{ size: A4; margin: 20mm 18mm 20mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: Arial, sans-serif; color: #111; font-size: 11pt; line-height: 1.5; margin: 0; }}
  h1 {{ font-size: 20pt; text-align: center; margin: 0 0 12pt; color: #111; }}
  h2 {{ font-size: 15pt; margin: 18pt 0 8pt; border-bottom: 1.5pt solid #0a6f86; padding-bottom: 4pt; break-after: avoid; }}
  h3 {{ font-size: 12pt; margin: 14pt 0 5pt; color: #064f61; break-after: avoid; }}
  p {{ margin: 0 0 8pt; text-align: justify; orphans: 3; widows: 3; }}
  h1 + p {{ text-align: center; }}
  table {{ border-collapse: collapse; width: 100%; margin: 8pt 0 14pt; break-inside: avoid; }}
  th, td {{ border: 0.75pt solid #888; padding: 5pt 8pt; text-align: center; }}
  th {{ background: #0a6f86; color: white; }}
  tbody tr:nth-child(even) {{ background: #eef6f8; }}
  blockquote {{ margin: 10pt 0 14pt; min-height: 90pt; padding: 14pt; border: 1.5pt solid #c65911; background: #fff2cc; display: flex; align-items: center; }}
  blockquote p {{ margin: 0; color: #9c0006; font-weight: 700; text-align: center; width: 100%; }}
  a {{ color: #064f61; overflow-wrap: anywhere; }}
  ul {{ margin-top: 4pt; padding-left: 20pt; }}
  li {{ margin-bottom: 4pt; }}
  .identity {{ text-align: center; border-top: 1pt solid #999; padding-top: 7pt; margin-top: 8pt; font-size: 9pt; color: #555; }}
</style>
</head>
<body>
{body}
<div class="identity">Chan Jing Yi | SUOL2500321 | BCL1123 Internet of Things</div>
</body>
</html>
"""

OUTPUT.write_text(html, encoding="utf-8")
print(OUTPUT)
