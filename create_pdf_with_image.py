#!/usr/bin/env python3
import re
from pathlib import Path

# Read the markdown file
md_path = Path("/Users/jingyichan/PycharmProjects/assignment/20260326_FA_Programming Fundamentals/20260326_Appointment_Booking_System_Report.md")
content = md_path.read_text()

# Replace the Mermaid code block with an image reference
# The image is in the same directory
mermaid_pattern = r'```mermaid\n.+?```'
replacement = '![Class Diagram](class-diagram.png)'
modified_content = re.sub(mermaid_pattern, replacement, content, flags=re.DOTALL)

# Save to a temporary markdown file
temp_md_path = md_path.parent / "temp_report.md"
temp_md_path.write_text(modified_content)

print(f"✓ Created temp markdown: {temp_md_path}")

# Now convert to PDF using weasyprint directly
from weasyprint import HTML, CSS
from markdown import markdown

# Convert markdown to HTML
html_content = markdown(modified_content, extensions=['extra', 'codehilite', 'toc'])

# Wrap in basic HTML structure
full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; margin-top: 20px; }}
        h2 {{ color: #555; margin-top: 15px; }}
        p {{ line-height: 1.6; }}
        img {{ max-width: 100%; height: auto; margin: 20px 0; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
        pre {{ background-color: #f4f4f4; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

# Save HTML for debugging
html_path = md_path.parent / "temp_report.html"
Path(html_path).write_text(full_html)

# Convert HTML to PDF
output_pdf = Path("/Users/jingyichan/PycharmProjects/assignment/20260326_FA_Programming Fundamentals/20260326_Appointment_Booking_System_Report.pdf")

# Set base URL to the directory containing the markdown so relative image paths work
base_url = md_path.parent.as_uri() + "/"

HTML(string=full_html, base_url=base_url).write_pdf(str(output_pdf))
print(f"✓ PDF created: {output_pdf}")

# Clean up temp files
temp_md_path.unlink()
html_path.unlink()
