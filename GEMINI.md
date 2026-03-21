# Directory Overview

This workspace is dedicated to the generation and management of high-quality academic and technical reports, specifically focused on the subject of **Computer Architecture**. It utilizes specialized AI-driven tools (Agents) to automate the analysis of assignment briefs, drafting of technical content (including LaTeX and Mermaid diagrams), and the professional rendering of PDF documents.

## Project Structure

- **`.agents/skills/`**: Contains specialized AI skills that extend the capabilities of the Gemini CLI:
    - **`academic-report-generator`**: The core workflow for creating A-grade reports. It manages tone, visual integration, and PDF rendering.
    - **`mermaid-diagrams`**: Provides references and guides for creating various software and architectural diagrams.
    - **`pdf`**: Documentation and scripts for advanced PDF processing and form filling.
    - **`skill-creator`**: Tools for developing and evaluating new AI skills.
- **`20260321_Computer_Architecture_Assignments/`**: A dated repository for completed assignment artifacts. Files are prefixed with `YYYYMMDD_` for organizational clarity.
    - Includes both Markdown (`.md`) sources and professionally rendered PDFs.
- **`Computer_Architecture_Assignment.pdf`**: A sample/reference assignment document.
- **`eTutorialCOMPUTERARCHITECTURE_DegreeWK-ODLJAN2026.pdf`**: A course-specific tutorial brief.
- **`FACOMPUTERARCHITECTURE_DegreeWK-ODLJAN2026.pdf`**: A Final Assessment brief for the Computer Architecture module.
- **`circuit_mockup.html`**: A visual logic breadboard mockup for a Smart Home Security system, used for illustrating digital logic concepts.

## Usage

### Generating Reports
To generate a new report, activate the `academic-report-generator` skill. The general workflow is:
1.  **Analyze**: Read the provided PDF or text brief (e.g., `FACOMPUTERARCHITECTURE...pdf`).
2.  **Draft**: Create a structured Markdown file (`.md`) incorporating technical analysis, LaTeX formulas, and Mermaid diagrams.
3.  **Render**: Use the Playwright-based rendering workflow within the skill to convert the Markdown/HTML into a submission-ready PDF.

### Organization Convention
New files and folders should be prefixed with the current date in **YYYYMMDD** format (e.g., `20260321_filename`). Submissions should always deliver both the Markdown source and the final PDF.

### Technical Tools
- **Mermaid.js**: Used for all architectural and flow diagrams.
- **MathJax/LaTeX**: Used for all mathematical calculations and performance metrics.
- **Playwright**: Used for converting styled HTML templates into professional A4 PDF documents.
