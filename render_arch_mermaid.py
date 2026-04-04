#!/usr/bin/env python3
import base64
import requests
from pathlib import Path

diagrams = {
    'dataflow-diagram.mmd': 'dataflow-diagram.png',
    'logic-flowchart.mmd': 'logic-flowchart.png'
}

base_dir = Path("/Users/jingyichan/PycharmProjects/assignment/20260402_ComputerArchitectureFinalAssessment")

for mmd_file, png_file in diagrams.items():
    diagram_path = base_dir / mmd_file
    diagram_content = diagram_path.read_text()

    # Encode for Mermaid API
    encoded = base64.b64encode(diagram_content.encode()).decode()
    url = f"https://mermaid.ink/img/{encoded}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            output_path = base_dir / png_file
            output_path.write_bytes(response.content)
            print(f"✓ Rendered {mmd_file} → {png_file}")
        else:
            print(f"✗ Failed to render {mmd_file}: {response.status_code}")
    except Exception as e:
        print(f"✗ Error rendering {mmd_file}: {e}")
