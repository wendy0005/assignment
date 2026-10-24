# PCB Flashcards

## Card 1

**Front:** What happens to a Process Control Block (PCB) when a process finishes its execution?

**Back:** The OS records that the process has terminated. Its bookkeeping is released during cleanup; some information may remain temporarily until the parent collects the exit status.

---

## Card 2

**Front:** How does a PCB's state change when a process pauses to wait for input/output (I/O)?

**Back:** The operating system updates the process state in its PCB from 'running' to 'waiting' until the requested resource or I/O operation completes.

---

## Card 3

**Front:** Is a Process Control Block (PCB) the process itself?

**Back:** No. A process is an active program executing in memory, while the PCB is only the operating system's internal record-keeping file about that process.

---

## Card 4

**Front:** What information is recorded in the I/O Status Information field of a PCB?

**Back:** It tracks hardware input/output devices allocated to the process and maintains a list of all currently open files.

---

## Card 5

**Front:** What is the role of the Program Counter inside a Process Control Block?

**Back:** It stores the memory address of the next code instruction to be executed for that process.

---

## Card 6

**Front:** What is a context switch in operating systems?

**Back:** A context switch occurs when the OS pauses the running process, saves its context into its PCB, and restores the saved context of another process from its PCB.

---

## Card 7

**Front:** Why does an operating system need a Process Control Block (PCB) for every process?

**Back:** It allows the operating system to track process execution, temporarily pause running tasks, switch to other tasks, and later resume the paused process seamlessly.

---

## Card 8

**Front:** Why must the Program Counter be saved into the PCB when a process is paused?

**Back:** Saving the Program Counter ensures the processor knows exactly which line of instruction to pick up from when the process is resumed.

---

## Card 9

**Front:** Is a Process Control Block (PCB) the CPU?

**Back:** No. The CPU is the physical hardware processor, whereas the PCB is a software data structure maintained by the operating system.

---

## Card 10

**Front:** What is a helpful everyday analogy for understanding a Process Control Block (PCB)?

**Back:** Analogy: A PCB is like a video game save record that stores your exact location, stats, and inventory so you can pause the game and resume later.

---

## Card 11

**Front:** What is the function of the Process ID (PID) field in a PCB?

**Back:** The Process ID (PID) is a unique numerical identifier assigned by the operating system to distinguish one process from all others.

---

## Card 12

**Front:** Does a Process Control Block (PCB) hold a copy of all the process's code and memory contents?

**Back:** No. The PCB contains metadata and tracking information; the process's actual code, global variables, heap, and stack live in separate main memory regions.

---

## Card 13

**Front:** What is a Process Control Block (PCB) in an operating system?

**Back:** A PCB is a dedicated data structure created by the operating system to store bookkeeping information and manage the state of a specific process.

---

## Card 14

**Front:** What is the purpose of Accounting Information in a PCB?

**Back:** It tracks system resource metrics, such as total CPU time used, execution time limits, process ID numbers, and user account data.

---

## Card 15

**Front:** Does a Process Control Block (PCB) store actual copies of the contents of open files?

**Back:** No. It stores references or pointers to open files and allocated hardware devices, not the actual file contents.

---

## Card 16

**Front:** Where is a Process Control Block (PCB) stored inside computer memory?

**Back:** PCBs are normally maintained in kernel memory (RAM), where the OS manages them.

---

## Card 17

**Front:** How do PCBs enable process pausing and resuming during a context switch?

**Back:** The OS saves the current process's execution state, then restores the saved state of the process selected to run next.

---

## Card 18

**Front:** What core fields make up the internal structure of a Process Control Block (PCB)?

**Back:** A PCB typically includes PID, process state, saved program counter and registers, scheduling information, memory information, I/O and open-file information, and accounting information.

---

## Card 19

**Front:** What is stored in the Process Scheduling Information section of a PCB?

**Back:** It stores process priority levels, scheduling queue pointers, and execution parameters used by the operating system to decide which task runs next.

---

## Card 20

**Front:** What are CPU Registers, and why are their values saved into a PCB during a pause?

**Back:** CPU Registers are high-speed temporary storage cells in the processor; saving their values preserves active calculations so work isn't lost when switching tasks.

---

## Card 21

**Front:** What is the role of the Stack Pointer in process execution?

**Back:** The Stack Pointer points to the current top of the stack memory, which holds temporary data like function parameters, local variables, and return addresses.

---

## Card 22

**Front:** What information does the Process State field in a PCB hold?

**Back:** It tracks the current stage of the process lifecycle, such as new, ready, running, waiting, or terminated.

---

## Card 23

**Front:** What is the purpose of Memory Management Information inside a PCB?

**Back:** It keeps track of memory boundaries assigned to the process, such as base and limit register values, page tables, or segment tables.

---
