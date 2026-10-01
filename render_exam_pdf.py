import re
import os
import markdown
from playwright.sync_api import sync_playwright

MD_PATH = "/Users/tankarhau/PycharmProjects/assignment/current_sem/BCL1223 - Database Fundamentals/BCL1223_May2026_Final_Exam_Answers.md"
HTML_PATH = "/Users/tankarhau/PycharmProjects/assignment/current_sem/BCL1223 - Database Fundamentals/BCL1223_May2026_Final_Exam_Answers.html"
PDF_PATH = "/Users/tankarhau/PycharmProjects/assignment/current_sem/BCL1223 - Database Fundamentals/BCL1223_May2026_Final_Exam_Answers.pdf"

with open(MD_PATH, "r", encoding="utf-8") as f:
    md_content = f.read()

def convert_mermaid_blocks(text):
    return re.sub(r"```mermaid\n([\s\S]*?)\n```", r'<pre class="mermaid">\1</pre>', text)

processed_md = convert_mermaid_blocks(md_content)

html_body = markdown.markdown(
    processed_md,
    extensions=['extra', 'tables', 'fenced_code', 'nl2br']
)

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>BCL1223 Database Fundamentals - Final Exam Answers</title>
    <script>
    MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
      }},
      svg: {{
        fontCache: 'global'
      }}
    }};
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
      document.addEventListener("DOMContentLoaded", function() {{
        mermaid.initialize({{
          startOnLoad: true,
          theme: 'default',
          securityLevel: 'loose',
          er: {{
            useMaxWidth: true,
            fill: '#f8fafc',
            stroke: '#334155'
          }}
        }});
      }});
    </script>

    <style>
        @page {{
            size: A4;
            margin: 15mm 12mm 15mm 12mm;
        }}

        body {{
            font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
            font-size: 10pt;
            line-height: 1.5;
            color: #1e293b;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
        }}

        .container {{
            max-width: 100%;
            margin: 0 auto;
            padding: 10px;
        }}

        h1 {{
            font-size: 16pt;
            color: #0f172a;
            border-bottom: 2px solid #2563eb;
            padding-bottom: 6px;
            margin-top: 24px;
            margin-bottom: 12px;
            page-break-after: avoid;
        }}

        h2 {{
            font-size: 13pt;
            color: #1e3a8a;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 4px;
            margin-top: 20px;
            margin-bottom: 10px;
            page-break-after: avoid;
        }}

        h3 {{
            font-size: 11pt;
            color: #1e293b;
            margin-top: 14px;
            margin-bottom: 6px;
            page-break-after: avoid;
        }}

        p {{
            margin-top: 0;
            margin-bottom: 10px;
        }}

        /* Fix long code line truncation in PDF */
        pre {{
            background-color: #0f172a;
            color: #f8fafc;
            padding: 10px 12px;
            border-radius: 6px;
            font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
            font-size: 8.5pt;
            line-height: 1.4;
            white-space: pre-wrap !important;
            word-wrap: break-word !important;
            word-break: break-word !important;
            overflow-x: hidden;
            margin: 10px 0;
            page-break-inside: avoid;
        }}

        code {{
            font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
            font-size: 8.5pt;
            background-color: #f1f5f9;
            color: #0f172a;
            padding: 2px 4px;
            border-radius: 4px;
            white-space: pre-wrap !important;
            word-break: break-word !important;
        }}

        pre code {{
            background-color: transparent;
            color: inherit;
            padding: 0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 12px 0;
            font-size: 9pt;
            page-break-inside: avoid;
        }}

        th, td {{
            padding: 6px 10px;
            border: 1px solid #cbd5e1;
            text-align: left;
        }}

        th {{
            background-color: #1e293b;
            color: #ffffff;
            font-weight: 600;
        }}

        tr:nth-child(even) {{
            background-color: #f8fafc;
        }}

        .mermaid {{
            display: flex;
            justify-content: center;
            background-color: #ffffff;
            padding: 12px;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            margin: 14px 0;
            page-break-inside: avoid;
        }}

        hr {{
            border: none;
            border-top: 1px solid #e2e8f0;
            margin: 18px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_body}
    </div>
</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"HTML successfully generated at: {HTML_PATH}")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file://{HTML_PATH}")
    
    page.wait_for_timeout(3000)
    
    page.pdf(
        path=PDF_PATH,
        format="A4",
        print_background=True,
        margin={
            "top": "15mm",
            "bottom": "15mm",
            "left": "12mm",
            "right": "12mm"
        }
    )
    browser.close()

print(f"PDF successfully generated at: {PDF_PATH}")
