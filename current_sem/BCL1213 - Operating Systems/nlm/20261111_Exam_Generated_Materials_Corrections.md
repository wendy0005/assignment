# Corrections for the NotebookLM exam materials

## 12 November replacements

- **Chapter 2 infographic:** its Round Robin table is incorrect. For arrival times (0, 1, 2), bursts (8, 6, 4), and quantum 4, the Gantt chart is P1 0–4, P2 4–8, P3 8–12, P1 12–16, P2 16–18. Completion times for P1/P2/P3 are 16/18/12; turnaround times 16/17/10; waiting times 8/11/6. This assumes no context-switch overhead.
- **Chapter 2 study guide, section 4.5:** the priority example incorrectly runs P4 before higher-priority P5. Assuming non-preemptive priority scheduling with lower numbers higher, after P3 completes at 14, P5 runs 14–16 and P4 runs 16–20. P5 has completion/turnaround/waiting times 16/4/2; P4 has 20/9/5. Average waiting time is 2.4 ms and average turnaround time is 6.4 ms. Priority numbering and preemption conventions must be stated in the question.
- The waiting-time formula turnaround minus CPU burst assumes the example has one CPU burst and no other blocking time.

- The generated study guide emphasizes OS introductions and file systems and does not adequately cover Chapters 2–4. Its proposed exam format describes the **practice mock**, not a confirmed format for the actual exam. Use the course materials and the existing chapter-specific quizzes and flashcards for the missing topics.
- Paging divides a process's virtual address space into **pages** and physical memory into **frames**, not physical memory into pages.
- A page fault occurs when a referenced page is not currently available in physical memory. The OS loads the required page; it may evict another page if necessary, but an eviction is not always required.
- In the Chapter 4 infographic, withdrawing $100 twice from $500 correctly leaves $300; this does not itself show an overdraft or a race-condition error. A possible lost-update race would leave an incorrect balance of $400 after two withdrawals if both transactions read $500 and each writes $400.
- The Chapter 2 lifecycle picture does not clearly identify transition directions. The normal transitions include new → ready, ready → running, running → ready (preemption), running → waiting, waiting → ready, and running → terminated.
- Treat the generated infographics as overviews; confirm detailed definitions and calculations against the lecturer's sources and your mock-exam answer sheet.
