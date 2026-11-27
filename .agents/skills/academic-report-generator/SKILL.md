---
name: academic-report-generator
description: >
  A comprehensive workflow for producing "Excellent" (A-grade) academic assignments and technical reports.
  Use this skill whenever the user wants to generate or refine a formal assignment, research paper, technical report,
  or answer tutorial/subject questions in academic format, especially when a source PDF or marking scheme is provided.
  It handles schema analysis, academic tone refinement (less AI, more scholarly), visual integration (Mermaid/LaTeX),
  and professional PDF rendering via Playwright. Trigger phrases: "use this to answer", "use this skill to answer",
  "answer using academic", "generate report".
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
    - **Answer punctuation:** By default, write tutorial and assignment answers without hyphens, en dashes, or em dashes. Rephrase naturally with commas, full stops, or words such as “to” and “and”. Preserve a hyphen only when it is essential to an exact name, quotation, formula, or technical notation. Do not use dash bullets. Check the rendered answers as well as the source for unwanted dashes; do not damage Markdown syntax, diagrams, or URLs through mechanical replacement. Explicit user instructions take precedence.
    - **Paragraph-First Approach:** ALWAYS use professional paragraphs and cohesive sentences for all analysis, descriptions, and theoretical discussions. **Avoid bullet points and numbered lists for narrative content.** Lists should be used only for step-by-step mathematical workings or simple enumerations of items (e.g., a list of components).
    - **Case Studies:** Ground technical concepts in real-world examples (e.g., Smart Greenhouse, Building Monitoring).
    - **Referencing:** Use **APA or Harvard style** (as requested) for all in-text citations and the reference list. **Crucially, ensure every reference includes its full source (URL, DOI, or publication details) and double-check that the source is active and accurately supports the claim.** Ensure all technical claims are backed by credible academic or industry sources. **NEVER include a URL that has not been empirically verified via search.**
    - **Do not cite the question or assessment brief:** Treat the user's own question, assignment brief and marking scheme as task instructions, not as literature sources. Do not add author and year citations such as `(SEGi University, 2026)` or reference list entries for those documents merely to describe the assignment, its requirements, sample data or marking criteria. Continue citing external sources that support substantive technical or academic claims. Cite a brief only when the user explicitly asks for it or when the brief itself is the subject of a critical source analysis.

3. **Anti-Detection & Humanization Strategy (CRITICAL):**
    - **Eliminate "AI-isms":** Strictly avoid phrases that trigger AI detectors.
        - **BANNED HOOKS:** "In contemporary...", "In the rapidly evolving...", "In today's digital age...", "To address these challenges...", "Paramount to...".
        - **BANNED TRANSITIONS:** "Furthermore," "Moreover," "In addition," "Notably," "It is important to note," "Overall," "In conclusion," "Moving forward," "Additionally," "Lastly," "Finally," "Basically," "Essentially."
        - **BANNED CLOSING PHRASES:** "Deepened my understanding," "A comprehensive exercise," "Crucial for maintaining," "Significantly reduce," "Enhance performance."
        - **BANNED CONVERSATIONAL FILLERS (Avoid Over-Correction):** Do not sacrifice academic tone to bypass AI detectors. NEVER use: "When we think about it," "For one thing," "Look at," "Basically," "To put it simply," "One of the aspects," "It is worrying that," "Imagine if," "Let's consider."
    - **Logical Flow over Transitional Fillers:** Use the *content* of the previous paragraph to bridge to the next. For example, instead of "Furthermore, the GUI...", use "While the backend manages the logic, the user interface provides the necessary interaction points..."
    - **Avoid Formulaic Paragraphs:** AI often uses a predictable [Topic Sentence -> Data -> Elaboration -> Conclusion] structure. Break this by starting with an active scholarly argument or a direct critique. Integrate citations natively into the argument (e.g., "Predatory behavior exploits systemic vulnerabilities (Finkelhor, 2009)" instead of "According to Finkelhor (2009)...").
    - **Vary Sentence Dynamics:** Intentionally vary sentence length (short, punchy sentences followed by complex, compound ones). This increases "burstiness," a key metric human writers naturally produce.
    - **Achieve "Burstiness" through Academic Syntax:** Use academic punctuation such as semicolons and inverted clauses. Follow a dense, technical compound sentence with a short, declarative one to create natural variation.
    - **Inject Nuance and Critique:** Move beyond factual reporting. Include professional critique, discuss limitations of a technology, or reflect on architectural trade-offs. AI often struggles with nuanced "grey areas."
    - **Specific Technical Depth:** Use precise industry terminology and deep-dive into specific architectural details (e.g., mentioning specific register names or instruction pipeline stages) to move away from generic AI descriptions.

4. **Technical & Visual Rigor:**
    - **Latex Support:** Use LaTeX syntax ($ ... $) only for actual complex mathematical formulas, equations, and calculations. **Do NOT use raw dollar signs for simple non-mathematical terms or ratios (e.g., database cardinalities like M:N, 1:M, or 1:1)**; use regular bold text or code blocks instead.
    - **Step-by-Step Working:** Show every logical step for any calculations.
    - **Mermaid Diagrams:** Integrate Mermaid.js for flowcharts, architecture diagrams, and logic circuits.
    - **Default Report Style**. Use the [StudyPocket proposal](<../../../current_sem/BCL2344 - Web and Mobile Development/assignment/20261021_StudyPocket_Proposal/ChanJingYi_SUOL2500321_Proposal.pdf>) as the visual reference for academic PDFs in this workspace. Follow any formatting requirements in the assessment brief or the user's instructions first.
      - Set the page to A4 portrait with 19 mm top and 20 mm side and bottom margins. Use a white background, 11 pt Arial body text in `#202A34`, and 1.5 line spacing.
      - Use navy `#173D57` for headings, links, and primary accents. Set section titles in 17 pt bold with a thin `#B8C7D3` rule and subsection titles in 12.5 pt bold. Use pale blue `#F7F9FC` and blue-grey `#BBC7D2` for figure surfaces and outlines where appropriate.
      - On the cover, left-align the 34 pt bold title and 18 pt regular subtitle. Place the assessment label, course details, and student details below in distinct blocks. Use a slim header with the course on the left and assessment name on the right. Put the student name and ID at the left of the footer and the current and total page numbers at the right.
      - Keep figures and labels readable at print size. Use fewer figures per page or split a dense diagram across sections if needed. Check the rendered PDF against the reference for typography, colour, cover layout, and page furniture.

5. **Professional Rendering Workflow:**
    - **Step 1 (Markdown Source):** Create a clean, well-structured `.md` file containing all text, LaTeX formulas, and Mermaid diagrams. Retain it as the editable working source; include it in an assessed submission only if the brief or user requests Markdown.
    - **Step 2 (HTML Preview):** Generate a professionally styled HTML version based on the Markdown content. If LaTeX is used in the markdown, ensure the HTML preview includes **MathJax** or **KaTeX** loading and config scripts (e.g., via CDN) to render math elements correctly. Ensure you include the **Mermaid.js** script and a custom renderer (e.g., in `marked.js`) that converts `mermaid` code blocks into `<div class="mermaid">` elements. Use a listener (like `mermaid.run()`) to trigger the rendering.
    - **Step 3 (PDF Generation):** Use the `mcp_playwright_browser_run_code` tool to convert the HTML to a professional A4 PDF. **Crucially, your Playwright script MUST wait for both the Mermaid diagrams and MathJax/KaTeX (if loaded) to finish rendering.** Use `await page.waitForSelector('.mermaid svg', { timeout: 10000 });` and appropriate wait loops for math elements to ensure they are fully drawn before calling `page.pdf()`. **Note:** Do not use `require('fs')` inside the browser context as it is not supported. Instead, pass the HTML content as a string variable or navigate to a local file.

## Submission-Facing Cleanliness

Write the final report for the marker or assessor, not as a record of the agent's production process. The document should stand on its own and should not expose internal implementation details that do not answer the brief.

- Do not mention local paths, generated filenames, helper scripts, containers, Docker, Playwright, browser automation, temporary credentials, or internal rendering commands unless the brief explicitly requires a methodology section or the user asks for those details in the report.
- Do not defer required content with sentences such as “the complete answer appears in `filename.ext`.” State the implementation directly and include enough explanation or evidence in the report itself. Deliver supplementary SQL, datasets, logs, Markdown, HTML, or source files separately without making the report depend on their names.
- When a brief requires a live demonstration, describe what the student must show in platform-neutral terms. Keep machine-specific start-up commands in a separate handoff note or chat response rather than the submission document.
- Distinguish submission artifacts from production artifacts. Markdown, HTML, rendering scripts and execution logs may be retained for reproducibility, but only identify them inside the report when the assessment instructions require them.
- Mention the target academic or technical platform when relevant (for example, Oracle SQL), but omit how the platform was hosted or automated unless that hosting choice is itself assessed.

## Submission ZIP Contents

Package only the deliverables required by the assessment brief or explicitly requested by the user. Build the ZIP from an explicit list of those files, not by archiving the entire working folder.

Exclude Markdown working sources, HTML previews, rendering scripts such as `render_report.py`, test and verification helpers, execution logs, build files, downloaded dependencies, the original brief and internal README files unless they are specifically required. Required program source code belongs in the ZIP; scripts used only to produce or check the report do not. Include only screenshots required as submission evidence.

Keep editable sources and production files locally, separate from the submission ZIP. Before delivery, inspect the archive contents and confirm every included file satisfies a submission requirement. Providing Markdown alongside the final PDF does not mean including it in the submission ZIP.

## Student Identity Configuration
ALWAYS include the following student information in the cover page and header/footer of every generated report:
- **Student Name:** Chan Jing Yi
- **Student ID:** SUOL2500321

## Final Output Structure
ALWAYS deliver both:
1.  **Markdown Source:** The `.md` file for version control and raw text access, provided separately from the submission ZIP unless explicitly required inside it.
2.  **PDF Final:** The official submission-ready document with full styling and rendered visuals.

## Course PDF naming and processing helpers

Prefix newly generated course PDFs and PDF output folders with the current date in `YYYYMMDD` format, unless the user specifies a filename. Preserve the original names of downloaded source files. For the previous project PDF form and OCR helpers, consult [the processing guide](references/pdf-processing/GUIDE.md). The bundled PDF skill handles general PDF work.
