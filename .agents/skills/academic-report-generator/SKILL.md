---
name: academic-report-generator
description: A comprehensive workflow for producing "Excellent" (A-grade) academic assignments and technical reports. Use this skill whenever the user wants to generate or refine a formal assignment, research paper, or technical report, especially when a source PDF or marking scheme is provided. It handles schema analysis, academic tone refinement (less AI, more scholarly), visual integration (Mermaid/LaTeX), and professional PDF rendering via Playwright.
---

# Academic Report Generator Skill

This skill provides a rigorous workflow for transforming assignment briefs or research requirements into submission-ready, professional academic documents.

## Workflow Overview

1.  **Analysis Phase:**
    - Read provided source documents (PDF, Docx, or text).
    - Extract and analyze the **Marking Scheme** and specific requirements.
    - Identify key parameters (e.g., clock rates, specific instruction sets, formula requirements).

2.  **Drafting Phase (Narrative Strategy):**
    - **Academic Tone:** Use a formal, scholarly voice. Avoid robotic transitions.
    - **No Bullet Points for Analysis:** ALWAYS use professional paragraphs and cohesive sentences for theoretical analysis. Bullet points are reserved for simple lists or step-by-step math.
    - **Case Studies:** Ground technical concepts in real-world examples (e.g., Smart Greenhouse, Building Monitoring).
    - **Human-Centric Writing:** Refine the text to be "less AI" by varying sentence structure and ensuring a natural flow.

3. **Technical & Visual Rigor:**
    - **Latex Support:** Use LaTeX syntax ($ ... $) for all mathematical formulas and calculations.
    - **Step-by-Step Working:** Show every logical step for any calculations.
    - **Mermaid Diagrams:** Integrate Mermaid.js for flowcharts, architecture diagrams, and logic circuits.
    - **Academic Styling:** Use "Times New Roman" or "Arial", 12pt/11pt font, and 1.5 line spacing as the standard for academic reports.

4. **Professional Rendering Workflow:**
    - **Step 1 (Markdown Source):** Create a clean, well-structured `.md` file containing all text, LaTeX formulas, and Mermaid diagrams. This serves as the editable source and raw submission.
    - **Step 2 (HTML Preview):** Generate a professionally styled HTML version based on the Markdown content.
    - **Step 3 (PDF Generation):** Use the `mcp_playwright_browser_run_code` tool to convert the HTML to a professional A4 PDF. **Note:** Do not use `require('fs')` inside the browser context as it is not supported. Instead, pass the HTML content as a string variable.

## Final Output Structure
ALWAYS deliver both:
1.  **Markdown Source:** The `.md` file for version control and raw text access.
2.  **PDF Final:** The official submission-ready document with full styling and rendered visuals.
