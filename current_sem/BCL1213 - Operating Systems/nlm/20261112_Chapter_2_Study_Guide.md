# Chapter 2 Exam Revision Guide: Process Management & Scheduling

### 1. Core Concepts & Process Structure

#### 1.1 Program vs. Process Definition
A **program** is a passive, static set of instructions stored on mass storage or disk (such as an executable file). It remains static until loaded into main memory.

A **process** is an active, running program currently being executed by the CPU. Beyond the instruction code itself, a process encompasses execution state, CPU registers, memory allocation, and operational data required to complete execution.

| Component | Purpose |
| :--- | :--- |
| **Program Code** | The executable instructions (text section) to be processed by the CPU. |
| **Process State** | The current operational condition of the process (e.g., New, Ready, Running, Waiting, Terminated). |
| **Program Counter (PC)** | A dedicated register holding the memory address of the next instruction to be executed for the process. |
| **Stack** | Temporary data storage used for function/method calls, local variables, return addresses, and parameter passing. |
| **Data Section** | Stores global and static variables initialized or uninitialized prior to execution. |
| **Heap** | Memory dynamically allocated at runtime during process execution. |

> 💡 **Real-World Architecture Note: Multiprocess Web Browsers**  
> Modern applications like Google Chrome utilize a **multiprocess architecture** to ensure stability and security (Silberschatz, p. 123). Rather than running all tabs inside a single process—where one crashing tab brings down the entire browser—Chrome separates tasks into distinct process types:
> * **Browser Process:** Manages the user interface, disk I/O, and network requests (only one instance runs).
> * **Renderer Processes:** Contain logic for rendering web pages (HTML, JavaScript, images). A separate renderer process is typically spawned for each opened tab, isolating websites from one another.
> * **Plug-in Processes:** Manage execution for browser extensions and external media components.  
> 
> Furthermore, renderer processes execute inside a **sandbox**, restricting unauthorized access to disk and network resources to prevent security exploits.

---

#### 1.2 Process Control Block (PCB)
The **Process Control Block (PCB)** is a central data structure maintained by the operating system for every active process. It acts as the primary repository for all process-specific operational information required to manage execution and system control.

Key attributes stored within a PCB include:
*   **Process ID (PID):** A unique numerical identifier assigned to the process by the OS.
*   **Process State:** Indicates the current execution phase (New, Ready, Running, Waiting, or Terminated).
*   **Program Counter (PC):** Contains the memory address of the next instruction to execute.
*   **CPU Registers:** Preserves architecture-specific register state (including accumulators, index registers, stack pointers, general-purpose registers, and condition codes).
*   **CPU Scheduling Information:** Stores data relevant to scheduling decisions, including process priority, scheduling queue pointers, and associated parameters.
*   **Memory Management Information:** Contains structural memory data such as base and limit register values, page tables, or segment tables.
*   **Accounting Information:** Tracks operational statistics including CPU time used, clock time elapsed, execution time limits, account numbers, and job/process IDs.
*   **I/O Status Information:** Maintains details regarding hardware assigned to the process, including allocated I/O devices and a list of open files.

---

#### 1.3 Context Switching
When an interrupt or system call occurs during execution, the operating system performs a **context switch** to pause the running process and assign the CPU to another process. The Process Control Block (PCB) preserves the execution state so the preempted process can resume seamlessly later.

**Step-by-Step Context Switch Procedure:**
1. Process $P_0$ is actively executing on the CPU when an interrupt or system call is triggered.
2. The OS halts $P_0$'s execution and saves its operational context (specifically the Program Counter and CPU hardware registers) into its Process Control Block ($PCB_0$). Process $P_0$ transitions to an idle state.
3. The OS selects Process $P_1$ for execution and reloads $P_1$'s saved state from its Process Control Block ($PCB_1$) into the CPU hardware registers.
4. The CPU resumes execution of Process $P_1$.
5. When a subsequent interrupt or system call occurs, the OS saves $P_1$'s state into $PCB_1$ and restores $P_0$'s saved state from $PCB_0$, returning CPU control back to $P_0$.

---

### 2. Process Lifecycle & Explicit Directed Transitions

#### 2.1 The Five Fundamental Process States
Throughout its lifecycle, a process transitions through five primary states. While operating systems may use slightly different naming conventions, these conceptual states remain universal:

1.  **New:** The process is being created and initialized.
2.  **Ready:** The process is loaded into main memory, prepared to execute, and awaiting CPU allocation.
3.  **Running:** The process's instructions are actively being executed by the CPU.
4.  **Waiting:** The process cannot execute until a specific external event or I/O operation completes.
5.  **Terminated:** The process has finished execution, releasing its allocated memory, resources, and PCB.

*(Note: On a single processor core, only one process can reside in the **Running** state at any given instant, while multiple processes can reside in the **Ready** or **Waiting** states.)*

---

#### 2.2 Directed State Transitions
Processes move between states via defined, explicit transitions:

1.  **New $\rightarrow$ Ready:** The operating system initializes the process, loads it into main memory, and places it into the ready queue.
2.  **Ready $\rightarrow$ Running:** The CPU scheduler selects (dispatches) the process from the ready queue and allocates CPU time for execution.
3.  **Running $\rightarrow$ Ready (on preemption):** An executing process is interrupted—such as when its assigned time quantum expires or a higher-priority task preempts it—and returns to the ready queue.
4.  **Running $\rightarrow$ Waiting (on I/O):** An executing process requests an event or I/O operation (e.g., reading disk data) and enters the waiting state until the operation completes.
5.  **Waiting $\rightarrow$ Ready (on I/O completion):** The pending event or I/O operation finishes, moving the process from the waiting state back into the ready queue.
6.  **Running $\rightarrow$ Terminated:** The process completes its final instruction or encounters a fatal error, triggering the OS to reclaim its assigned memory, resources, and PCB.

---

### 3. Schedulers & Scheduling Queues

#### 3.1 Types of Schedulers

| Scheduler Type | Alternate Name | Frequency of Execution | Primary Function |
| :--- | :--- | :--- | :--- |
| **Long-Term Scheduler** | Job Scheduler | Less frequently (often when a process exits) | Manages process selection from the job pool (mass storage) to main memory; controls the degree of multiprogramming; balances I/O-bound and CPU-bound processes. |
| **Short-Term Scheduler** | CPU Scheduler | Frequently (immediate decisions) | Selects processes from the ready queue for immediate CPU execution; must execute quickly to minimize overhead. |
| **Medium-Term Scheduler** | Swapping Scheduler | Temporarily / As needed | Manages memory load by temporarily removing processes from main memory (swapping out) and restoring them later (swapping in). |

---

#### 3.2 Scheduling Queues & Process Movement
As processes progress through their execution cycle, they navigate distinct system queues:

*   **Job Queue:** Houses all processes in the system, including those stored in mass storage awaiting memory allocation.
*   **Ready Queue:** Houses processes residing in main memory that are ready for CPU execution. This queue is typically maintained as a linked list, where a queue header points to the head and tail PCBs, and each PCB links to the next process in line.
*   **Device Queues:** Dedicated queues maintained by individual I/O devices (e.g., disk units, network interface units, or terminal units). If a process requests a busy device, it waits in that device's queue.

**Process Navigation Flow:**
1. A newly admitted process is enqueued into the **Ready Queue**.
2. The short-term scheduler dispatches the process to the **CPU**.
3. While executing, one of four queue movement events occurs:
   * The process issues an I/O request and is placed in an **I/O Device Queue**. Upon I/O completion, it returns to the Ready Queue.
   * The process creates (forks) a child process and enters a wait queue until the child terminates, after which it returns to the Ready Queue.
   * The process experiences an interrupt or time-slice expiration and is immediately returned to the Ready Queue.
   * The process completes execution, whereupon it is removed from all queues, and its PCB and resources are fully released.

---

### 4. Scheduling Metrics & Algorithm Worked Examples

#### 4.1 Key Performance Metrics & Formulas
*   **Completion Time (CT):** The exact timestamp when a process finishes execution.
*   **Turnaround Time (TAT):** The total elapsed time from process arrival to execution completion.
*   **Waiting Time (WT):** The total accumulated time a process spends waiting in the ready queue.
*   **Average Waiting Time:** The sum of waiting times for all processes divided by the total number of processes.

> **Turnaround Time (TAT):**  
> $$\mathbf{\text{TAT} = \text{Completion Time (CT)} - \text{Arrival Time (AT)}}$$

> **Waiting Time (WT):**  
> $$\mathbf{\text{WT} = \text{Turnaround Time (TAT)} - \text{Burst Time (BT)}}$$

> **Average Waiting Time:**  
> $$\mathbf{\text{Average WT} = \frac{\sum \text{Waiting Times}}{\text{Total Number of Processes}}}$$

---

#### 4.2 First-Come, First-Served (FCFS) Scheduling
**Concept:** A non-preemptive algorithm that executes processes strictly in order of their arrival in the ready queue. Once execution begins, a task runs to completion without interruption.

**Worked Example:**
Processes arrive in order $P_1, P_2, P_3, P_4$ with Arrival Time $AT = 0\text{ ms}$:
*   $P_1$: Burst Time = $21\text{ ms}$
*   $P_2$: Burst Time = $3\text{ ms}$
*   $P_3$: Burst Time = $6\text{ ms}$
*   $P_4$: Burst Time = $2\text{ ms}$

**Gantt Chart:**
```
| P1 (0-21) | P2 (21-24) | P3 (24-30) | P4 (30-32) |
```

**Step-by-Step Calculations:**
*   $WT_{P1} = 0\text{ ms}$
*   $WT_{P2} = 21\text{ ms}$
*   $WT_{P3} = 21 + 3 = 24\text{ ms}$
*   $WT_{P4} = 21 + 3 + 6 = 30\text{ ms}$

$$\text{Average Waiting Time} = \frac{0 + 21 + 24 + 30}{4} = \frac{75}{4} = 18.75\text{ ms}$$

---

#### 4.3 Shortest Job First (SJF / SJN) Scheduling
**Concept:** Schedules processes based on CPU burst times, prioritizing the shortest available task. 
*   **Non-Preemptive:** Once allocated to the CPU, a process runs to completion regardless of new arrivals.
*   **Preemptive (Shortest Remaining Time First - SRTF):** If a newly arrived process has a shorter remaining burst time than the currently running process, the running process is preempted.

**Worked Example (Non-Preemptive):**
Processes $P_1, P_2, P_3, P_4$ arrive at $AT = 0\text{ ms}$:
*   $P_1$: Burst Time = $21\text{ ms}$
*   $P_2$: Burst Time = $3\text{ ms}$
*   $P_3$: Burst Time = $6\text{ ms}$
*   $P_4$: Burst Time = $2\text{ ms}$

**Execution Sequence:** $P_4 \rightarrow P_2 \rightarrow P_3 \rightarrow P_1$

**Gantt Chart:**
```
| P4 (0-2) | P2 (2-5) | P3 (5-11) | P1 (11-32) |
```

**Calculations:**
*   $WT_{P4} = 0\text{ ms}$, $TAT_{P4} = 2 - 0 = 2\text{ ms}$
*   $WT_{P2} = 2\text{ ms}$, $TAT_{P2} = 5 - 0 = 5\text{ ms}$
*   $WT_{P3} = 5\text{ ms}$, $TAT_{P3} = 11 - 0 = 11\text{ ms}$
*   $WT_{P1} = 11\text{ ms}$, $TAT_{P1} = 32 - 0 = 32\text{ ms}$

$$\text{Average Waiting Time} = \frac{0 + 2 + 5 + 11}{4} = \frac{18}{4} = 4.5\text{ ms}$$
$$\text{Average Turnaround Time} = \frac{2 + 5 + 11 + 32}{4} = \frac{50}{4} = 12.5\text{ ms}$$

---

#### 4.4 Round Robin (RR) Scheduling
**Concept:** A preemptive algorithm designed for time-sharing systems. Each process receives a fixed execution time slice called a **time quantum**. If a task does not complete within its quantum, it is preempted and re-queued at the back of the ready queue.

**Worked Example:**
Time Quantum = $5\text{ ms}$, $AT = 0\text{ ms}$ for all processes:
*   $P_1$: Burst Time = $21\text{ ms}$
*   $P_2$: Burst Time = $3\text{ ms}$
*   $P_3$: Burst Time = $6\text{ ms}$
*   $P_4$: Burst Time = $2\text{ ms}$

**Gantt Chart:**
```
| P1 (0-5) | P2 (5-8) | P3 (8-13) | P4 (13-15) | P1 (15-20) | P3 (20-21) | P1 (21-26) | P1 (26-31) | P1 (31-32) |
```

**Metrics Breakdown:**

| Process | Burst Time (BT) | Completion Time (CT) | Turnaround Time ($\text{TAT} = \text{CT} - \text{AT}$) | Waiting Time ($\text{WT} = \text{TAT} - \text{BT}$) |
| :--- | ---: | ---: | ---: | ---: |
| **P1** | 21 ms | 32 ms | $32 - 0 = 32\text{ ms}$ | $32 - 21 = 11\text{ ms}$ |
| **P2** | 3 ms | 8 ms | $8 - 0 = 8\text{ ms}$ | $8 - 3 = 5\text{ ms}$ |
| **P3** | 6 ms | 21 ms | $21 - 0 = 21\text{ ms}$ | $21 - 6 = 15\text{ ms}$ |
| **P4** | 2 ms | 15 ms | $15 - 0 = 15\text{ ms}$ | $15 - 2 = 13\text{ ms}$ |

$$\text{Average Waiting Time} = \frac{11 + 5 + 15 + 13}{4} = \frac{44}{4} = 11\text{ ms}$$

---

#### 4.5 Priority Scheduling
**Concept:** CPU allocation is determined by explicit priority numbers assigned to each process. By standard convention, **lower numerical values indicate higher priority**.

**Worked Example:**
Consider 5 processes ($P_1$ to $P_5$) with specified Arrival Times, Burst Times, and Priorities:

| Process | Priority | Burst Time (BT) | Arrival Time (AT) |
| :--- | ---: | ---: | ---: |
| **P1** | 1 | 4 ms | 0 ms |
| **P2** | 2 | 3 ms | 0 ms |
| **P3** | 1 | 7 ms | 6 ms |
| **P4** | 3 | 4 ms | 11 ms |
| **P5** | 2 | 2 ms | 12 ms |

**Step-by-Step Execution Calculations:**
*   **P1:** Executes from $t=0$ to $t=4$.
    *   $\text{CT} = 0 + 4 = 4\text{ ms}$
    *   $\text{TAT} = 4 - 0 = 4\text{ ms}$
    *   $\text{WT} = 4 - 4 = 0\text{ ms}$
*   **P2:** Executes from $t=4$ to $t=7$.
    *   $\text{CT} = 4 + 3 = 7\text{ ms}$
    *   $\text{TAT} = 7 - 0 = 7\text{ ms}$
    *   $\text{WT} = 7 - 3 = 4\text{ ms}$
*   **P3:** Arrives at $t=6$. Executes from $t=7$ to $t=14$.
    *   $\text{CT} = 7 + 7 = 14\text{ ms}$
    *   $\text{TAT} = 14 - 6 = 8\text{ ms}$
    *   $\text{WT} = 8 - 7 = 1\text{ ms}$
*   **P4:** Arrives at $t=11$. Executes from $t=14$ to $t=18$.
    *   $\text{CT} = 14 + 4 = 18\text{ ms}$
    *   $\text{TAT} = 18 - 11 = 7\text{ ms}$
    *   $\text{WT} = 7 - 4 = 3\text{ ms}$
*   **P5:** Arrives at $t=12$. Executes from $t=18$ to $t=20$.
    *   $\text{CT} = 18 + 2 = 20\text{ ms}$
    *   $\text{TAT} = 20 - 12 = 8\text{ ms}$
    *   $\text{WT} = 8 - 2 = 6\text{ ms}$

**Summary Metrics Table:**

| Process | Priority | Burst Time (BT) | Arrival Time (AT) | Completion Time (CT) | Turnaround Time (TAT) | Waiting Time (WT) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **P1** | 1 | 4 ms | 0 ms | 4 ms | 4 ms | 0 ms |
| **P2** | 2 | 3 ms | 0 ms | 7 ms | 7 ms | 4 ms |
| **P3** | 1 | 7 ms | 6 ms | 14 ms | 8 ms | 1 ms |
| **P4** | 3 | 4 ms | 11 ms | 18 ms | 7 ms | 3 ms |
| **P5** | 2 | 2 ms | 12 ms | 20 ms | 8 ms | 6 ms |

*   **Average Waiting Time:** $\frac{0 + 4 + 1 + 3 + 6}{5} = \frac{14}{5} = 2.80\text{ ms}$
*   **Average Turnaround Time:** $\frac{4 + 7 + 8 + 7 + 8}{5} = \frac{34}{5} = 6.80\text{ ms}$

---

### 5. Exam Preparation: Practice Questions, Model Answers, & Common Pitfalls

#### 5.1 Common Student Mistakes & Exam Pitfalls

> ⚠️ **WATCH OUT! Exam Trap: Unspecified Arrival Times**  
> Unless an explicit Arrival Time ($AT$) is given in the problem statement, **always assume $AT = 0$** for all processes. Never assume arrival times are non-zero or sequential unless specified.

> ⚠️ **WATCH OUT! Exam Trap: Confusing Performance Metrics**  
> Students often swap formulas under exam pressure. Remember:
> * $\text{Turnaround Time (TAT)} = \text{Completion Time (CT)} - \text{Arrival Time (AT)}$ (Total time spent in system)
> * $\text{Waiting Time (WT)} = \text{Turnaround Time (TAT)} - \text{Burst Time (BT)}$ (Time spent in ready queue)

> ⚠️ **WATCH OUT! Exam Trap: Incomplete PCB State Preservation**  
> In context switching short-answer questions, stating that the OS saves "CPU registers" is only half-correct. You **must explicitly mention saving the Program Counter (PC)** alongside registers into the PCB, as the PC stores the precise resumption instruction address.

> ⚠️ **WATCH OUT! Exam Trap: Round Robin Queue Insertion Order**  
> When a running process's time quantum expires at the exact same instant a new process arrives, **the newly arriving process enters the Ready Queue first**, and the preempted process is appended **behind** it.

---

#### 5.2 Exam-Style Practice Questions & Model Solutions

##### Question 1 (Conceptual)
**Question:** Differentiate clearly between a program and a process, and explain why both CPU registers and the Program Counter must be saved inside the Process Control Block (PCB) during a context switch.

**Model Solution:**
A program is a passive, static set of executable instructions stored on disk (e.g., an executable file). A process is an active, dynamic instance of a program being executed in main memory.

During a context switch, the OS halts an executing process to allocate the CPU to another task. The Program Counter (PC) holds the exact memory address of the next instruction to execute, while CPU registers hold active computational data and state flags. Saving both components into the PCB ensures that when the preempted process is rescheduled, CPU hardware registers can be restored to their exact state prior to interruption, preventing computational errors or data corruption.

---

##### Question 2 (Calculation Exercise)
**Question:** Given the following set of processes executing under the **Round Robin (RR)** algorithm with a Time Quantum of $4\text{ ms}$:

| Process | Arrival Time (AT) | Burst Time (BT) |
| :--- | ---: | ---: |
| **P1** | 0 ms | 8 ms |
| **P2** | 1 ms | 6 ms |
| **P3** | 2 ms | 4 ms |

1. Trace the step-by-step state of the Ready Queue at each time event.
2. Construct the execution Gantt chart.
3. Calculate Completion Time (CT), Turnaround Time (TAT), and Waiting Time (WT) for each process, as well as the Average Waiting Time.

**Model Solution:**

**1. Step-by-Step Ready Queue State Tracing:**
*   **$t=0\text{ ms}$:** $P_1$ arrives ($BT=8$). Ready Queue = $[P_1]$. $P_1$ is dispatched to execute from $t=0$ to $t=4$.
*   **$t=1\text{ ms}$:** $P_2$ arrives ($BT=6$). Ready Queue = $[P_2]$.
*   **$t=2\text{ ms}$:** $P_3$ arrives ($BT=4$). Ready Queue = $[P_2, P_3]$.
*   **$t=4\text{ ms}$:** $P_1$'s time quantum expires (remaining $BT=4$). $P_1$ is preempted and re-queued behind waiting processes.  
    *Updated Ready Queue:* $[P_2, P_3, P_1]$. $P_2$ is dispatched to execute from $t=4$ to $t=8$.
*   **$t=8\text{ ms}$:** $P_2$'s time quantum expires (remaining $BT=2$). $P_2$ is preempted and re-queued.  
    *Updated Ready Queue:* $[P_3, P_1, P_2]$. $P_3$ is dispatched to execute from $t=8$ to $t=12$.
*   **$t=12\text{ ms}$:** $P_3$ completes its $4\text{ ms}$ burst and **terminates**.  
    *Updated Ready Queue:* $[P_1, P_2]$. $P_1$ is dispatched to execute its remaining $4\text{ ms}$ from $t=12$ to $t=16$.
*   **$t=16\text{ ms}$:** $P_1$ completes its burst and **terminates**.  
    *Updated Ready Queue:* $[P_2]$. $P_2$ is dispatched to execute its remaining $2\text{ ms}$ from $t=16$ to $t=18$.
*   **$t=18\text{ ms}$:** $P_2$ completes execution and **terminates**. Ready Queue is empty.

**2. Execution Gantt Chart:**
```
| P1 (0-4) | P2 (4-8) | P3 (8-12) | P1 (12-16) | P2 (16-18) |
```

**3. Metric Calculations:**

| Process | Arrival Time (AT) | Burst Time (BT) | Completion Time (CT) | Turnaround Time ($\text{TAT} = \text{CT} - \text{AT}$) | Waiting Time ($\text{WT} = \text{TAT} - \text{BT}$) |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **P1** | 0 ms | 8 ms | 16 ms | $16 - 0 = 16\text{ ms}$ | $16 - 8 = 8\text{ ms}$ |
| **P2** | 1 ms | 6 ms | 18 ms | $18 - 1 = 17\text{ ms}$ | $17 - 6 = 11\text{ ms}$ |
| **P3** | 2 ms | 4 ms | 12 ms | $12 - 2 = 10\text{ ms}$ | $10 - 4 = 6\text{ ms}$ |

$$\text{Average Waiting Time} = \frac{8 + 11 + 6}{3} = \frac{25}{3} \approx 8.33\text{ ms}$$

---

#### 5.3 Cited Source References
*   Silberschatz, Abraham. *Operating System Concepts*, Page 123.
*   Studytonight - Operating System Tutorials (First-Come First-Serve & Shortest Job First).