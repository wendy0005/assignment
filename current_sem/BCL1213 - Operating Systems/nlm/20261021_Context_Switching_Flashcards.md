# Operating Systems Flashcards

## Card 1

**Front:** How does the same-desk versus different-desk analogy explain thread versus process context switching?

**Back:** Switching threads is like swapping active papers on the same desk (shared memory), while switching processes is like moving to a completely different desk (isolated memory).

---

## Card 2

**Front:** How does data sharing between threads compare to data sharing between processes?

**Back:** Threads share data directly through common memory, while processes require explicit Inter-Process Communication (IPC).

---

## Card 3

**Front:** The process memory section reserved for dynamic memory allocation, which is shared by all threads in that process, is called the _____.

**Back:** Heap

---

## Card 4

**Front:** Scenario: Thread A modifies a global variable in the data section. Can Thread B in the same process directly read this updated value?

**Back:** They share the same variable, so Thread B can access it. Correct synchronization is needed to coordinate updates and ensure visibility.

---

## Card 5

**Front:** How does thread creation and termination speed compare to process creation and termination?

**Back:** Creating or terminating a thread is generally faster because it reuses the existing process resources.

---

## Card 6

**Front:** Why are threads often called lightweight processes?

**Back:** Because they share common process memory and resources, reducing creation, switching, and termination overhead.

---

## Card 7

**Front:** Scenario: When switching execution from Thread 1 to Thread 2 in Process A, must the OS swap out the process's main code and data sections?

**Back:** No, because both threads share the exact same code (text) and data sections.

---

## Card 8

**Front:** What is the fundamental difference in memory space between a process and a thread?

**Back:** A process operates in its own isolated memory space, whereas threads within the same process share a common memory space.

---

## Card 9

**Front:** Context switching between threads within the same process is faster than switching between processes primarily because threads share the same _____ space.

**Back:** Memory

---

## Card 10

**Front:** Scenario: When additional threads are created within an existing process, what components are allocated for each new thread?

**Back:** Each new thread receives its own Program Counter, set of CPU registers, and private stack.

---

## Card 11

**Front:** Which key memory sections are shared among all threads belonging to the same process?

**Back:** The text (code) section, data section (global and static variables), and heap (dynamic memory).

---

## Card 12

**Front:** Why is context switching between threads in the same process usually faster than switching between processes?

**Back:** Because threads share the same memory space and resources, eliminating the overhead of switching memory spaces.

---

## Card 13

**Front:** What four primary resource sections compose a complete process in memory?

**Back:** Text (code), Data, Heap, and Stack.

---

## Card 14

**Front:** Why can multithreading within a single process have lower overhead than using separate processes?

**Back:** It enables concurrent task execution while sharing memory, avoiding the CPU time and memory overhead of creating separate processes.

---

## Card 15

**Front:** What function do CPU registers serve during active thread execution?

**Back:** They hold current working values and computational state for the active thread.

---

## Card 16

**Front:** What specific role does the Program Counter (PC) perform in thread execution?

**Back:** It holds the address of the next instruction to be executed by that specific thread.

---

## Card 17

**Front:** Why does each thread within a process require its own private stack?

**Back:** To store temporary, thread-specific data such as function parameters, local variables, and return addresses.

---

## Card 18

**Front:** In operating systems, what is defined as a context switch?

**Back:** The mechanism where the CPU saves the state of a running entity and loads the saved state of another entity to resume execution.

---

## Card 19

**Front:** Where does the operating system store state information so execution can be restored after a context switch?

**Back:** In control blocks (such as the Process Control Block or thread control structures).

---

## Card 20

**Front:** Scenario: Can Process A directly access a local variable stored on Process B's stack without explicit IPC?

**Back:** No, because processes execute in completely separate, isolated memory spaces.

---

## Card 21

**Front:** What private execution state does each thread maintain independently within a process?

**Back:** Its own program counter, CPU registers, and stack.

---

## Card 22

**Front:** When a suspended thread resumes execution following a context switch, how does the CPU know where to continue?

**Back:** The CPU restores the thread's saved Program Counter address, pointing to its next instruction.

---

## Card 23

**Front:** When switching execution between two threads in the same process, what minimal state must the CPU save and restore?

**Back:** The thread's private execution state: its Program Counter, register values, and stack pointer.

---

## Card 24

**Front:** What communication mechanism is required for two separate processes to exchange data?

**Back:** Inter-Process Communication (IPC) methods.

---
