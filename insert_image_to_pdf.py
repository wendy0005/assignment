#!/usr/bin/env python3
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from PIL import Image as PILImage

# Read the existing PDF
pdf_path = "/Users/jingyichan/PycharmProjects/assignment/20260326_FA_Programming Fundamentals/20260326_Appointment_Booking_System_Report.pdf"
reader = PdfReader(pdf_path)

# Create a new canvas with just the image (for page 2, between diagram description and design decisions)
# Get image dimensions
img = PILImage.open("/Users/jingyichan/PycharmProjects/assignment/20260326_FA_Programming Fundamentals/class-diagram.png")
img_width, img_height = img.size

# Create an image-only page
packet = BytesIO()
c = canvas.Canvas(packet, pagesize=letter)
width, height = letter

# Add image scaled to fit the page
c.drawString(50, height - 50, "2. Improved Class Diagram")
c.drawImage("/Users/jingyichan/PycharmProjects/assignment/20260326_FA_Programming Fundamentals/class-diagram.png",
            50, height - 500, width=500, height=400, preserveAspectRatio=True)

c.save()
packet.seek(0)
image_page_reader = PdfReader(packet)
image_page = image_page_reader.pages[0]

# Create writer and insert image page after first page
writer = PdfWriter()

# Add first page
writer.add_page(reader.pages[0])

# Add image page
writer.add_page(image_page)

# Add remaining pages (from page 2 onwards)
for page_num in range(1, len(reader.pages)):
    writer.add_page(reader.pages[page_num])

# Write output
output_path = pdf_path
with open(output_path, "wb") as output_file:
    writer.write(output_file)

print(f"✓ PDF updated with embedded diagram: {output_path}")
