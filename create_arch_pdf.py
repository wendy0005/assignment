#!/usr/bin/env python3
from pathlib import Path
from weasyprint import HTML

md_path = Path("/Users/jingyichan/PycharmProjects/assignment/20260402_ComputerArchitectureFinalAssessment/20260402_Computer_Architecture_Final_Assessment.md")
output_pdf = Path("/Users/jingyichan/PycharmProjects/assignment/20260402_ComputerArchitectureFinalAssessment/20260402_Computer_Architecture_Final_Assessment.pdf")

# Read markdown
content = md_path.read_text()

# Use the existing HTML file if available, otherwise convert markdown to HTML
html_path = md_path.parent / "20260402_Computer_Architecture_Final_Assessment.html"

if html_path.exists():
    # Use existing HTML and set base URL for images
    base_url = md_path.parent.as_uri() + "/"
    HTML(filename=str(html_path), base_url=base_url).write_pdf(str(output_pdf))
    print(f"✓ PDF created from HTML: {output_pdf}")
else:
    # Convert markdown to PDF using WeasyPrint
    from markdown import markdown

    html_content = markdown(content, extensions=['extra', 'codehilite', 'toc'])

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
            h1 {{ color: #333; margin-top: 20px; font-size: 24px; }}
            h2 {{ color: #555; margin-top: 15px; font-size: 18px; border-bottom: 2px solid #ddd; padding-bottom: 5px; }}
            h3 {{ color: #666; margin-top: 12px; font-size: 14px; }}
            p {{ line-height: 1.6; text-align: justify; }}
            img {{ max-width: 100%; height: auto; margin: 15px 0; border: 1px solid #eee; padding: 5px; }}
            table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            th {{ background-color: #f2f2f2; font-weight: bold; }}
            code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; font-family: 'Courier New', monospace; }}
            pre {{ background-color: #f4f4f4; padding: 10px; overflow-x: auto; border-left: 3px solid #555; }}
            ul, ol {{ margin: 10px 0; padding-left: 30px; }}
            li {{ margin: 5px 0; }}
        </style>
    </head>
    <body>
    {html_content}
    </body>
    </html>
    """

    base_url = md_path.parent.as_uri() + "/"
    HTML(string=full_html, base_url=base_url).write_pdf(str(output_pdf))
    print(f"✓ PDF created from markdown: {output_pdf}")
