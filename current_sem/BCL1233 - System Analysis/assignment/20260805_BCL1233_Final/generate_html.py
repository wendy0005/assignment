import re
import markdown

md_path = "/Users/jingyichan/CodingArea/assignment/current_sem/BCL1233 - System Analysis/assignment/20260805_BCL1233_Final/BCL1233_FinalAssessment_Answers.md"
html_path = "/Users/jingyichan/CodingArea/assignment/current_sem/BCL1233 - System Analysis/assignment/20260805_BCL1233_Final/BCL1233_FinalAssessment_Answers.html"

with open(md_path, "r", encoding="utf-8") as f:
    md_text = f.read()

# Convert markdown code blocks with ```mermaid to <div class="mermaid">...</div>
def convert_mermaid_blocks(text):
    return re.sub(r'```mermaid\n(.*?)```', r'<div class="mermaid">\n\1\n</div>', text, flags=re.DOTALL)

processed_md = convert_mermaid_blocks(md_text)

# Convert Markdown to HTML using python-markdown with extensions
html_body = markdown.markdown(processed_md, extensions=['tables', 'fenced_code'])

html_document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>BCL1233 Final Project - System Design and UML for a Hybrid Work Monitoring System</title>
<style>
  @page {{
    size: A4;
    margin: 15mm 15mm 15mm 15mm;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #111;
    margin: 0;
    padding: 0;
    background-color: #fff;
  }}
  
  .cover-page {{
    height: 90vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    page-break-after: always;
    padding: 40px 20px;
    border: 2px solid #1a365d;
    margin-bottom: 30px;
  }}
  .cover-uni {{
    font-size: 18pt;
    font-weight: bold;
    color: #1a365d;
    letter-spacing: 1px;
    margin-bottom: 8px;
  }}
  .cover-faculty {{
    font-size: 12pt;
    color: #4a5568;
    margin-bottom: 30px;
    text-transform: uppercase;
  }}
  .cover-divider {{
    width: 80%;
    height: 2px;
    background-color: #1a365d;
    margin: 25px auto;
  }}
  .cover-course {{
    font-size: 15pt;
    font-weight: bold;
    color: #2b6cb0;
    margin-bottom: 12px;
  }}
  .cover-title {{
    font-size: 22pt;
    font-weight: bold;
    color: #1a365d;
    margin: 25px 0;
    line-height: 1.3;
  }}
  .cover-meta {{
    font-size: 12pt;
    line-height: 2;
    margin-top: 40px;
    color: #2d3748;
    text-align: left;
    display: inline-block;
  }}
  
  .content-container {{
    padding: 10px 0;
  }}
  
  h1 {{
    font-size: 16pt;
    color: #1a365d;
    border-bottom: 2px solid #1a365d;
    padding-bottom: 6px;
    margin-top: 30px;
    margin-bottom: 16px;
    page-break-before: always;
  }}
  h1:first-of-type {{ page-break-before: avoid; }}
  h2 {{
    font-size: 14pt;
    color: #2b6cb0;
    border-bottom: 1px solid #cbd5e0;
    padding-bottom: 4px;
    margin-top: 24px;
    margin-bottom: 12px;
  }}
  h3 {{
    font-size: 12.5pt;
    color: #2d3748;
    margin-top: 18px;
    margin-bottom: 8px;
  }}
  h4 {{
    font-size: 11.5pt;
    color: #4a5568;
    margin-top: 14px;
    margin-bottom: 6px;
    font-weight: bold;
  }}
  p {{
    text-align: justify;
    margin: 8px 0;
  }}
  
  img {{
    max-width: 100%;
    max-height: 480px;
    width: auto;
    height: auto;
    display: block;
    margin: 16px auto;
    border: 1px solid #cbd5e0;
    border-radius: 6px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    page-break-inside: avoid;
    object-fit: contain;
  }}
  
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #cbd5e0;
    padding: 8px 10px;
    text-align: left;
    vertical-align: top;
  }}
  th {{
    background-color: #ebf8ff;
    color: #1a365d;
    font-weight: bold;
    border-bottom: 2px solid #2b6cb0;
  }}
  tr:nth-child(even) td {{
    background-color: #f7fafc;
  }}
  
  pre {{
    background-color: #f7fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #2b6cb0;
    padding: 12px;
    border-radius: 4px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 8.5pt;
    line-height: 1.3;
    overflow-x: auto;
    white-space: pre;
    margin: 14px 0;
    page-break-inside: avoid;
  }}
  
  code {{
    font-family: 'Courier New', Courier, monospace;
    font-size: 9.5pt;
    background-color: #edf2f7;
    padding: 2px 4px;
    border-radius: 3px;
  }}

  .mermaid {{
    text-align: center;
    margin: 20px 0;
    page-break-inside: avoid;
    page-break-before: auto;
    page-break-after: auto;
    overflow: visible;
  }}
  .mermaid svg {{
    max-width: 100%;
    max-height: 220mm;
    width: auto;
    height: auto;
  }}
  
  ul, ol {{
    margin: 8px 0;
    padding-left: 24px;
  }}
  li {{
    margin: 4px 0;
  }}
  
  blockquote {{
    border-left: 4px solid #3182ce;
    background-color: #ebf8ff;
    margin: 12px 0;
    padding: 10px 16px;
    color: #2c5282;
  }}
  
  .footer-note {{
    text-align: center;
    font-size: 9pt;
    color: #718096;
    margin-top: 40px;
    border-top: 1px solid #e2e8f0;
    padding-top: 10px;
  }}
</style>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
</head>
<body>

<div class="cover-page">
  <div class="cover-uni">SEGi UNIVERSITY</div>
  <div class="cover-faculty">Faculty of Engineering, Built Environment, and Information Technology</div>
  <div class="cover-divider"></div>
  <div class="cover-course">BCL1233 — System Analysis and Design</div>
  <div class="cover-title">FINAL PROJECT<br><span style="font-size: 16pt; font-weight: normal; color: #4a5568;">System Design and UML for a Hybrid Work Monitoring System</span></div>
  <div class="cover-divider"></div>
  <div class="cover-meta">
    <strong>Student Name:</strong> Chan Jing Yi<br>
    <strong>Student ID:</strong> SUOL2500321<br>
    <strong>Programme:</strong> Bachelor of Computer Science (ODL)<br>
    <strong>Assessment Type:</strong> Individual Final Project (40%)<br>
    <strong>Submission Date:</strong> August 2026
  </div>
</div>

<div class="content-container">
{html_body}
</div>

<div class="footer-note"><em>BCL1233 System Analysis and Design — Final Project Specification</em></div>

<script>
  mermaid.initialize({{
    startOnLoad: true,
    theme: 'default',
    securityLevel: 'loose',
    fontFamily: 'Times New Roman, Times, serif'
  }});
  mermaid.run().then(() => {{
    document.body.classList.add('rendered');
  }});
</script>
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_document)

print("Pre-rendered HTML with single-page diagram scaling generated successfully:", html_path)
