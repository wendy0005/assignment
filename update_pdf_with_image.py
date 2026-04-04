#!/usr/bin/env python3
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import re

# Read the markdown file
md_path = "/Users/jingyichan/PycharmProjects/assignment/20260326_FA_Programming Fundamentals/20260326_Appointment_Booking_System_Report.md"
with open(md_path, 'r') as f:
    content = f.read()

# Create PDF
output_path = "/Users/jingyichan/PycharmProjects/assignment/20260326_FA_Programming Fundamentals/20260326_Appointment_Booking_System_Report.pdf"
doc = SimpleDocTemplate(output_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)

styles = getSampleStyleSheet()
# Create custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=16,
    textColor='#000000',
    spaceAfter=12,
    alignment=0
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=12,
    textColor='#000000',
    spaceAfter=6,
    alignment=0
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['Normal'],
    fontSize=10,
    alignment=0
)

story = []

# Split by sections
sections = content.split('\n## ')
title_section = sections[0]

# Parse title section
title_match = re.search(r'^# (.+)$', title_section, re.MULTILINE)
if title_match:
    story.append(Paragraph(title_match.group(1), title_style))
    story.append(Spacer(1, 0.2*inch))

# Parse metadata lines
for line in title_section.split('\n')[2:]:
    line = line.strip()
    if line and not line.startswith('---'):
        story.append(Paragraph(line, body_style))

story.append(Spacer(1, 0.2*inch))

# Process remaining sections
for i, section in enumerate(sections[1:], 1):
    lines = section.split('\n')
    section_title = lines[0].strip()

    # Add section heading
    story.append(Paragraph(f"## {section_title}", heading_style))
    story.append(Spacer(1, 0.1*inch))

    section_content = '\n'.join(lines[1:])

    # Handle Mermaid diagram - replace with image
    if 'classDiagram' in section_content and 'mermaid' in section_content:
        story.append(Spacer(1, 0.1*inch))
        img = Image("/Users/jingyichan/PycharmProjects/assignment/20260326_FA_Programming Fundamentals/class-diagram.png", width=6*inch, height=4.5*inch)
        story.append(img)
        story.append(Spacer(1, 0.2*inch))
        # Remove the mermaid code block from content
        section_content = re.sub(r'```mermaid\n.+?```', '', section_content, flags=re.DOTALL)

    # Parse remaining content into paragraphs
    paragraphs = re.split(r'\n(?=\n)', section_content)

    for para in paragraphs:
        para = para.strip()
        if not para or para.startswith('```'):
            continue

        # Handle code blocks
        if para.startswith('```'):
            story.append(Paragraph(f"<font face='Courier' size='9'>{para}</font>", body_style))
        else:
            # Clean up formatting
            para = para.replace('**', '<b>').replace('**', '</b>')
            para = para.replace('`', '<font face="Courier">')
            para = para.replace('`', '</font>')

            if para:
                story.append(Paragraph(para, body_style))
                story.append(Spacer(1, 0.05*inch))

    if i < len(sections) - 1:
        story.append(PageBreak())

# Build PDF
doc.build(story)
print(f"✓ Updated PDF created: {output_path}")
