#!/usr/bin/env python3
import base64
import requests
from pathlib import Path

# Read the Mermaid diagram
diagram_path = Path("/Users/jingyichan/PycharmProjects/assignment/20260326_FA_Programming Fundamentals/class-diagram.mmd")
diagram_content = diagram_path.read_text()

# Use Mermaid's rendering API via the live editor
# Encode the diagram
encoded = base64.b64encode(diagram_content.encode()).decode()

# Create the Mermaid Live Editor URL for rendering
url = f"https://mermaid.ink/img/{encoded}"

try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        output_path = diagram_path.parent / "class-diagram.png"
        output_path.write_bytes(response.content)
        print(f"✓ Rendered class diagram to {output_path}")
    else:
        print(f"✗ Failed: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")
