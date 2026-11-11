# Study-pack review notes

## Reviewed materials

- Guide: checked coverage against course Chapters 1–4 and independently recalculated the FCFS, SJF, Priority and Round Robin example completion times, turnaround times, waiting times and averages. Their numeric results are correct under zero-overhead, single-burst assumptions. The edited guide states those assumptions.
- Quiz: NotebookLM returned 20 rather than the requested 40 questions. The local edition contains 20 reviewed generated questions and 20 additional practice questions, arranged as 10 per chapter. Each has four options and one correct answer. Options were shuffled reproducibly; answers and explanations are in a separate file.
- Flashcards: flattened nested content blocks that were exposed as dictionary text by the CLI exporter. The local edition has 60 generated cards, eight clarified answers and 16 local recall supplements, for 76 cards total. Supplements strengthen Chapter 3 and condition-variable coverage.
- Visual: inspected the generated infographic. It misspells the Waiting state, lacks clear transition arrows, incorrectly labels RAM as the slowest hierarchy level, has spelling errors in tool names and overstates some claims. It is retained only as `infographic_DRAFT_WITH_ERRORS.png`. Use the separately authored, reviewed `revision_sheet.png` or vector SVG instead.

## Important technical corrections

1. A paging offset must be smaller than the page size. The source example with a 4 KB page and 100 KB offset is inconsistent. The local guide explicitly identifies the problem and substitutes a valid additional exercise with a 4096-byte page and 100-byte offset. The generated instruction to reproduce invalid arithmetic in an exam was removed.
2. Virtual memory is an address-space abstraction, not simply an automatic RAM deficit allocation from disk. Execution depends on working set, backing/commit limits and memory availability. Excessive paging causes thrashing.
3. Coffman's four conditions are necessary for resource deadlock. Their general presence alone does not prove that a current multi-instance resource allocation is already deadlocked.
4. A counting semaphore blocks when no permit is available. Acquiring the last available permit succeeds and leaves zero; the next acquire waits. Avoid ambiguous decrement/block rules without defining the implementation's count convention.
5. Condition-variable wait atomically releases the associated mutex and reacquires it before returning; the shared-state predicate must be checked again in a loop.
6. A system call or interrupt does not automatically cause a process to enter Waiting or Ready, respectively. The guide now names blocking and preemption as the relevant triggers.
7. Deadlock may affect only a subset of processes. A network/server failure may affect remote services while independent local work continues. Browser processes do not always correspond one-to-one with tabs.
8. Historical trivia and unsupported “Professor's Exam Insight” attribution were removed from the local guide. The revision focuses on concepts and course techniques, without claiming lecturer-endorsed exam predictions.

## Local versus NotebookLM versions

The corrected guide, 40-question quiz, answer key, 76-card set and reviewed visual are local deliverables. The original NotebookLM Studio artifacts remain in the existing notebook and may retain the generated errors or smaller question count. Raw report and JSON exports are preserved separately for traceability. Source renaming does not change their content or source IDs.

## Source naming

The seven lecture/SIM source titles now begin with the chapter number and document type: Chapter 1 Lecture Notes; Chapter 2 Lecture Notes and SIM Notes; Chapter 3 Lecture Notes Parts A/B and SIM Notes; Chapter 4 SIM Notes. The original local PDFs retain their original filenames. The upload manifest tracks source IDs and new titles.


## Interactive report review

The report is complete and its embedded flashcards, scheduling mind map and 25-question mixed assessment are complete. The embedded memory slide card and video card were not requested for generation; a separate full-course deck and audio overview were requested instead.

Embedded activities were checked against the plan and the report section, not against the original sources. The FCFS, SJF, Round Robin, page translation and segmentation arithmetic in the embedded quiz were independently checked. The assessment includes multiple-choice, multiple-select, fill-in-the-blank and short-answer questions.

Qualifications for the live generated activities:

- Quiz question 6 assumes a **blocking read that must wait**. A read satisfied from cache or a nonblocking call need not change Running to Waiting.
- An active process means a program in execution across its lifecycle; it need not be running on a CPU at the instant being discussed.
- SJF minimizes average waiting under the appropriate known-burst/all-jobs-ready assumptions; do not generalize to arbitrary future arrivals.
- DMA avoids making the CPU copy every byte, but the CPU still normally configures the transfer and handles completion.
- Priority-number conventions vary; the worked examples use lower numbers for higher priorities.

The local interactive-report export clarifies hard-deadline failure and register/cache capacity and restores missing race-condition and condition-variable pseudocode. The live NotebookLM report remains generated content; the corrected local guide is the main revision authority within this pack.
