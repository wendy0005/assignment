# Operating Systems Midterm Test: Suggested Answers

**Student:** Chan Jing Yi  
**Student ID:** SUOL2500321  
**Subject:** BCL1213 Operating Systems

## Question 1

### (a) Operating system fundamentals

An operating system (OS) is system software that acts as an intermediary between users and applications on one side and computer hardware on the other. It manages resources such as the processor, memory, storage and input/output devices, and provides services and protection that allow programs to run efficiently and safely.

### (b) Interaction and multiprogramming

Figure 1 shows four interacting layers: the user, applications, the operating system and hardware. A user requests work through an application. The application requests OS services through system calls, for example to read a file or allocate memory. The OS controls the hardware through mechanisms such as device drivers and returns results to the application, which presents them to the user.

To support multiprogramming, the OS admits several jobs into memory, subject to available resources. Its memory manager allocates and protects their address spaces, while the scheduler selects a ready process to use the processor. If that process waits for an input/output operation, the OS saves its state and schedules another ready process. The device operates while another process uses the CPU; an interrupt informs the OS when the operation finishes and the waiting process can become ready again. Maintaining a suitable mix of CPU intensive and input/output intensive jobs increases the chance that a process is ready to run. The degree of multiprogramming must still be limited when memory is scarce, since too many active processes can cause excessive paging and reduce performance.

### (c) Fragmentation

**Internal fragmentation** is unused space inside an allocated block. For example, allocating a 300 KB fixed partition to a 200 KB job leaves 100 KB unused within that partition.

**External fragmentation** is free space split into separate holes between allocations. The total free space may be sufficient for a request, but no single contiguous hole is large enough. Compaction can combine holes when relocation is supported; paging avoids external fragmentation in physical memory.

### (d) Memory allocation

The paper says three jobs but lists four. The table shows all four in arrival order. Assume the blocks are free contiguous holes, each allocated hole is split, its remainder remains available, and first fit scans from Block 1 to Block 4 by address. Each algorithm starts with the original free blocks.

| Job | Best fit | First fit | Worst fit |
|---|---|---|---|
| Job 1, 200 KB | Block 3, 100 KB remains | Block 1, 300 KB remains | Block 4, 600 KB remains |
| Job 2, 450 KB | Block 1, 50 KB remains | Block 2, 250 KB remains | Block 2, 250 KB remains |
| Job 3, 350 KB | Block 2, 350 KB remains | Block 4, 450 KB remains | Block 4 remainder, 250 KB remains |
| Job 4, 600 KB | Block 4, 200 KB remains | Not allocated | Not allocated |

For example, under worst fit, Job 1 leaves a 600 KB hole in Block 4. After Job 2 takes 450 KB from Block 2, that 600 KB hole is the largest and therefore receives Job 3. Job 4 cannot fit in any remaining single hole. If blocks are treated as indivisible partitions instead, the answers differ.

### (e) Advantages of multiprogramming

Multiprogramming improves CPU utilisation because another job can execute while one waits for input/output. It can increase throughput by completing more jobs over a period of time. It also improves utilisation of resources by allowing CPU work and input/output activity to overlap.

## Question 2

### (a) Swapping

Swapping is a memory management technique in which the OS temporarily moves a process's memory contents from RAM to secondary storage and later restores them so the process can continue. In classical process swapping, the process is suspended while its memory is outside RAM; modern systems commonly move individual pages instead of whole processes.

### (b) Two reasons for swapping

First, the laboratory has insufficient RAM for all active applications. Moving an inactive or blocked process out frees memory for an application that needs to run, such as the video editor.

Second, swapping helps the OS regulate the number of processes competing for memory. Suspending a process can relieve memory pressure and allow the remaining processes to retain enough working memory to make progress. Excessive swapping, however, introduces disk overhead and may lead to thrashing.

### (c) Swapping out and in

To swap out a process, the OS selects a suitable process, ensures its execution is suspended, preserves its execution state and moves the required memory contents to a backing store. The physical frames can then be reused. The process cannot execute while the required memory is absent.

When the process is eligible to resume and sufficient RAM is available, the OS loads its contents back into memory, updates memory mappings and places the process in the appropriate ready or waiting state. Once ready and selected by the scheduler, its saved CPU state is restored and it continues from where it stopped. A pending input/output operation must be handled safely before the relevant memory is moved.

### (d) Two concurrency principles or challenges

**Race conditions:** Concurrent processes or threads can interleave operations on shared data. If two database transactions read the same account balance and independently write updates, one update may overwrite the other. The result then depends on execution order.

**Deadlock:** Processes can wait indefinitely if each holds a resource and waits for another resource held by the other. For example, two transactions may lock accounts in opposite order. A consistent lock order or a deadlock detection and recovery policy can address this problem.

### (e) Critical section and mutual exclusion

The code that reads, calculates and writes an account balance is a critical section. A mutex or database lock ensures that only one transaction at a time performs the protected update on the same account. The second transaction waits until the first completes and releases the lock, then reads the updated balance. This prevents lost updates when all accesses follow the same locking protocol.

### (f) Consequence and solution

Poor concurrency control can cause a lost update, leaving an account balance incorrect. For example, two withdrawals may both read the original balance, but the later write may overwrite the first withdrawal. Use database transactions with suitable isolation and row locks, so each read and update is protected until the transaction commits or rolls back.

## Question 3

### (a) Process state transitions

Although the prompt says three states, the supplied figure contains five. The standard directed transitions are:

| From | To | Arc label | Explanation |
|---|---|---|---|
| New | Ready | Admitted | The OS accepts the newly created process into the ready queue. |
| Ready | Running | Dispatch | The scheduler assigns the CPU to the ready process. |
| Running | Ready | Preemption | The process loses the CPU, for example when its time slice expires. |
| Running | Waiting | Block | The process needs an event or input/output operation before it can continue. |
| Waiting | Ready | Completion | The awaited event or input/output operation completes. |
| Running | Terminated | Exit | The process finishes or is terminated, and the OS releases its resources. |

A waiting process normally goes to Ready rather than directly to Running, because it must first be selected by the scheduler.

### (b) Process and thread

| Aspect | Process | Thread |
|---|---|---|
| Memory allocation | Has its own protected virtual address space. | Shares the process address space, including code and heap, with other threads; has its own stack. |
| Execution | An independent program in execution containing at least one thread. | An execution path within a process, with its own program counter and registers. |
| Resource sharing | Resources are generally isolated from other processes; communication requires an appropriate interprocess mechanism. | Shares process resources such as memory and open files with peer threads, so shared data may require synchronisation. |

### (c) Five items in a PCB

1. **Process identifier:** uniquely identifies the process for OS management.
2. **Process state:** records whether it is ready, running, waiting or in another state.
3. **Program counter:** identifies the next instruction to execute when the process resumes.
4. **CPU registers:** hold execution values that must be restored after an interruption.
5. **Memory management information:** includes references to page tables or other mappings used to access the process address space.

### (d) Context switching

An interrupt, system call, time slice expiry or blocking operation transfers control to the OS. It saves P1's execution context, including its program counter and registers, in its PCB or associated kernel structures, and updates its state. P1 may become ready or waiting according to the reason for the switch.

The scheduler selects P2 from the ready queue. The OS updates the active memory management context as needed, restores P2's saved registers and program counter, marks P2 as running and returns control to it. P2 resumes from its previously saved point. Context switching lets multiple processes share a CPU and lets another process run while one waits for input/output. The switch itself consumes time without directly executing the processes' useful work, so it is an overhead.

## Question 4

### (a) Paging

Paging divides a process's logical address space into fixed size **pages** and physical memory into equal size **frames**. A **page table** records the mapping from each virtual page to its physical frame when resident. The memory management unit uses the page number to find the frame and combines it with the unchanged offset within the page to form the physical address. Pages need not occupy adjacent physical frames.

### (b) Calculations

**i. Number of pages** = logical address space ÷ page size = 16 KB ÷ 4 KB = **4 pages**.

**ii. Number of frames** = physical memory ÷ frame size = 64 KB ÷ 4 KB = **16 frames**.

**iii. Relationship:** Each page and frame is 4 KB. A resident page occupies one frame, and the page table maps its page number to that frame. The four logical pages may occupy any four available physical frames; they do not have to be consecutive. A logical address has a page number and an offset, while the corresponding physical address has a frame number and the same offset. Other frames can hold pages of other processes or OS data.

### (c) Segmentation and comparison

Segmentation divides a program into variable size logical units, such as code, data or stack. A logical address identifies a segment and an offset, and a segment table provides the base and limit for address translation and protection.

Paging uses fixed size pages and frames, generally independent of the program's logical structure. Segmentation reflects logical units and uses variable size segments. Paging can cause internal fragmentation but avoids external fragmentation of physical frames; contiguous segment allocation can cause external fragmentation. Both approaches can provide protection and address translation.

### (d) Virtual memory

Virtual memory gives each process a logical address space that can be larger than the RAM currently allocated to it. With demand paging, only the pages needed at a given time must be present in physical frames; other pages can remain in backing storage or be loaded from their files. When a process accesses a nonresident page, a page fault causes the OS to find a frame, load the page and resume the instruction. If necessary, the OS first replaces another page, writing it back when required. This allows large programs to run with limited RAM, but frequent page faults can severely slow execution.

## References

OpenStax. (2023). *Introduction to computer science*, sections 6.3 and 6.4. https://openstax.org/books/introduction-computer-science/pages/6-3-processes-and-concurrency and https://openstax.org/books/introduction-computer-science/pages/6-4-memory-management

Bell, J. (n.d.). *Operating systems: Processes* and *Main memory*. University of Illinois Chicago. https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/3_Processes.html and https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/8_MainMemory.html
