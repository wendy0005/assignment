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

3.  **Technical & Visual Rigor:**
    - **Latex Support:** Use LaTeX syntax ($ ... $) for all mathematical formulas and calculations.
    - **Step-by-Step Working:** Show every logical step for any calculations.
    - **Mermaid Diagrams:** Integrate Mermaid.js for flowcharts, architecture diagrams, and logic circuits.

4.  **Professional Rendering Workflow:**
    - **Step 1 (HTML Preview):** Generate a professionally styled HTML version using GitHub-style CSS. Include scripts for MathJax and Mermaid.
    - **Step 2 (PDF Generation):** Use the `mcp_playwright_browser_run_code` tool to set the content, wait for visuals to render, and export a final A4 PDF.

## Final Output Structure
- **Markdown Source:** The raw text and diagrams.
- **HTML Preview:** Temporary interactive and styled version.
- **PDF Final:** The official submission-ready document.

## Rendering Code Snippet (Playwright)
When generating the PDF, use a pattern similar to this in `mcp_playwright_browser_run_code`:
```javascript
async (page) => {
    const htmlContent = `...`; // The full HTML string
    await page.setContent(htmlContent, { waitUntil: 'networkidle' });
    // Wait for visuals (Mermaid/MathJax) to render
    await page.waitForTimeout(5000); 
    const pdfPath = 'Output_Report.pdf';
    await page.pdf({
        path: pdfPath,
        format: 'A4',
        margin: { top: '20mm', bottom: '20mm', left: '20mm', right: '20mm' },
        printBackground: true
    });
    return `PDF successfully saved to ${pdfPath}`;
}
```
