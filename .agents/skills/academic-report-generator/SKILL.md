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
    - **Paragraph-First Approach:** ALWAYS use professional paragraphs and cohesive sentences for all analysis, descriptions, and theoretical discussions. **Avoid bullet points and numbered lists for narrative content.** Lists should be used only for step-by-step mathematical workings or simple enumerations of items (e.g., a list of components).
    - **Case Studies:** Ground technical concepts in real-world examples (e.g., Smart Greenhouse, Building Monitoring).
    - **Referencing:** Use **APA or Harvard style** (as requested) for all in-text citations and the reference list. **Crucially, ensure every reference includes its full source (URL, DOI, or publication details) and double-check that the source is active and accurately supports the claim.** Ensure all technical claims are backed by credible academic or industry sources. **NEVER include a URL that has not been empirically verified via search.**

3. **Anti-Detection & Humanization Strategy (CRITICAL):**
    - **Eliminate "AI-isms":** Strictly avoid phrases that trigger AI detectors.
        - **BANNED HOOKS:** "In contemporary...", "In the rapidly evolving...", "In today's digital age...", "To address these challenges...", "Paramount to...".
        - **BANNED TRANSITIONS:** "Furthermore," "Moreover," "In addition," "Notably," "It is important to note," "Overall," "In conclusion," "Moving forward," "Additionally," "Lastly," "Finally," "Basically," "Essentially."
        - **BANNED CLOSING PHRASES:** "Deepened my understanding," "A comprehensive exercise," "Crucial for maintaining," "Significantly reduce," "Enhance performance."
    - **Logical Flow over Transitional Fillers:** Use the *content* of the previous paragraph to bridge to the next. For example, instead of "Furthermore, the GUI...", use "While the backend manages the logic, the user interface provides the necessary interaction points..."
    - **Vary Sentence Dynamics:** Intentionally vary sentence length (short, punchy sentences followed by complex, compound ones). This increases "burstiness," a key metric human writers naturally produce.
    - **Avoid AI "Bridge" Words:** Eliminate generic AI transition phrases like "Furthermore," "In addition," "Moreover," or "In conclusion" at the start of every paragraph. Instead, use logical bridges that refer back to the previous paragraph's core concept.
    - **Inject Nuance and Critique:** Move beyond factual reporting. Include professional critique, discuss limitations of a technology, or reflect on architectural trade-offs. AI often struggles with nuanced "grey areas."
    - **Specific Technical Depth:** Use precise industry terminology and deep-dive into specific architectural details (e.g., mentioning specific register names or instruction pipeline stages) to move away from generic AI descriptions.

4. **Technical & Visual Rigor:**
    - **Latex Support:** Use LaTeX syntax ($ ... $) for all mathematical formulas and calculations.
    - **Step-by-Step Working:** Show every logical step for any calculations.
    - **Mermaid Diagrams:** Integrate Mermaid.js for flowcharts, architecture diagrams, and logic circuits.
    - **Academic Styling:** Use "Times New Roman" or "Arial", 12pt/11pt font, and 1.5 line spacing as the standard for academic reports.

5. **Professional Rendering Workflow:**
    - **Step 1 (Markdown Source):** Create a clean, well-structured `.md` file containing all text, LaTeX formulas, and Mermaid diagrams. This serves as the editable source and raw submission.
    - **Step 2 (HTML Preview):** Generate a professionally styled HTML version based on the Markdown content.
    - **Step 3 (PDF Generation):** Use the `mcp_playwright_browser_run_code` tool to convert the HTML to a professional A4 PDF. **Note:** Do not use `require('fs')` inside the browser context as it is not supported. Instead, pass the HTML content as a string variable.

## Final Output Structure
ALWAYS deliver both:
1.  **Markdown Source:** The `.md` file for version control and raw text access.
2.  **PDF Final:** The official submission-ready document with full styling and rendered visuals.
