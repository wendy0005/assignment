# BCL1213 Chapters 1–4: answer key

Use after completing the quiz. Each explanation identifies the key rule or calculation.

## Question 1: B

Hard Real-Time Operating System

Safety-critical systems like air-traffic monitoring demand guaranteed, deterministic response times where missing a deadline could lead to catastrophic system failure.

## Question 2: A

The core OS component that manages privileged operations and system resources.

The kernel performs core OS resource-management and protection functions.

## Question 3: B

It allocates CPU time, memory and I/O resources.

The OS coordinates allocation and protection of shared hardware resources.

## Question 4: C

Translate OS requests into commands for a particular device.

A driver provides device-specific control behind an OS interface.

## Question 5: B

Jobs are submitted and processed with little or no interaction during execution.

Batch systems emphasize queued jobs rather than ongoing user interaction.

## Question 6: C

Another ready job can run while one job waits for I/O.

Keeping multiple jobs available allows CPU work to overlap another job I/O wait.

## Question 7: A

Responsive interactive service through frequent CPU switching.

Short CPU allocations let users interact while other tasks also make progress.

## Question 8: A

Correctness includes meeting its required deadline.

A high average speed alone does not establish an upper bound on response time.

## Question 9: A

A network OS exposes network services across identifiable machines; a distributed OS aims to coordinate machines as a more integrated system.

Both use networking, but their integration and presentation of resources differ.

## Question 10: A

It requests an OS service through a controlled interface.

System calls request services; only operations that need to wait must block.

## Question 11: B

Data section

The data areas hold global/static variables, including initialized data and the zero-initialized BSS area in common layouts.

## Question 12: B

$\text{TAT} = 8\text{ ms}$, $\text{WT} = 1\text{ ms}$

Completion Time is $7 + 7 = 14\text{ ms}$. Turnaround Time is $\text{CT} - \text{Arrival} = 14 - 6 = 8\text{ ms}$. Waiting Time is $\text{TAT} - \text{Burst} = 8 - 7 = 1\text{ ms}$.

## Question 13: B

$3\text{ ms}$

Waiting Time is the difference between the execution start time and arrival time: $14\text{ ms} - 11\text{ ms} = 3\text{ ms}$ (or $\text{TAT} - \text{Burst} = 7 - 4 = 3\text{ ms}$).

## Question 14: C

They share the process address space but have separate execution registers and stacks.

Threads share process resources while retaining independent execution state.

## Question 15: D

$7\text{ ms}$

$P_2$ starts at $4\text{ ms}$ and runs for $3\text{ ms}$, completing at $t = 7\text{ ms}$. Turnaround Time is $\text{CT} - \text{Arrival} = 7 - 0 = 7\text{ ms}$.

## Question 16: A

Ready

Completion makes it eligible for CPU service; the scheduler still decides when it runs.

## Question 17: C

Saved program counter and register state.

The PCB is process bookkeeping used to manage and resume execution.

## Question 18: A

3 ms, 10 ms, 4 ms

Response = 5−2=3; turnaround = 12−2=10; waiting = 10−6=4. Assume no I/O and negligible overhead.

## Question 19: A

P1 0–2, P2 2–4, P1 4–5

P1 uses one quantum and queues behind P2. P2 finishes in its quantum; P1 then uses its remaining 1 ms.

## Question 20: C

Aging: gradually increase the effective priority of waiting jobs.

Aging helps long-waiting jobs eventually receive CPU service.

## Question 21: B

Tertiary Storage

Tertiary storage (such as tape drives or archival optical media) provides very low cost per byte and massive capacity specifically designed for long-term data archiving.

## Question 22: A

3250

The offset $750$ is valid because $0 \le 750 < 800$. The physical address is computed as $\text{base} + \text{offset} = 2500 + 750 = 3250$.

## Question 23: D

An invalid address fault occurs because offset 350 exceeds the segment limit of 300.

For segmentation memory bounds checking, valid offsets must satisfy $0 \le \text{offset} < \text{limit}$. Since $350 \ge 300$, the memory access is illegal.

## Question 24: C

Paging uses fixed-size memory blocks causing internal fragmentation, while Segmentation uses logical variable-sized blocks causing external fragmentation.

Paging allocates uniform fixed-size pages (leading to wasted space inside the last page), whereas Segmentation allocates variable program sections (leading to external memory gaps).

## Question 25: B

Trap to the page-fault handler; validate the access, obtain a frame (evicting a page if necessary), load the page, update the mapping, and restart the instruction.

The OS must check that access is valid, locate the backing data, obtain a frame, perform the necessary I/O, update translation state and resume. A clean eviction may not require a write to disk.

## Question 26: A

Severe performance degradation caused by continuous and excessive swapping of pages between RAM and disk storage.

Thrashing occurs when processes spend more time handling page faults and swapping pages in and out of disk than executing real instructions.

## Question 27: C

1400

Offset $200 < 500$ limit is valid. Physical address = $\text{base} + \text{offset} = 1200 + 200 = 1400$.

## Question 28: B

Secondary Storage (SSDs / HDDs)

Secondary storage devices such as SSDs and HDDs retain files permanently when power is turned off, providing large capacity at low relative cost.

## Question 29: A

7620 bytes

2500=2×1024+452; physical address=7×1024+452=7620 bytes.

## Question 30: C

2 KiB

The allocation is 8 KiB and the process uses 6 KiB: internal fragmentation is 2 KiB. Assume no other overhead.

## Question 31: D

RM800, caused by a race condition resulting in a lost update of Thread A's deposit.

Thread B writes $\text{RM1,000} - \text{RM200} = \text{RM800}$ based on its stale read, completely overwriting Thread A's deposit of RM100.

## Question 32: C

Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait

These four conditions represent Coffman's necessary conditions required for concurrent processes to fall into a deadlock state.

## Question 33: B

Deadlock Avoidance

Deadlock Avoidance dynamically analyzes allocation states and claim vectors (e.g., Banker's Algorithm) to ensure requests are granted only if the system remains in a safe state.

## Question 34: D

It lowers overall system resource efficiency and utilization.

By enforcing conservative constraints to invalidate one of Coffman's conditions (e.g., forcing processes to release all resources), system throughput and resource efficiency decrease.

## Question 35: D

Ostrich Algorithm

The Ostrich Algorithm simplifies design by ignoring deadlocks, accepting the small risk of failure in exchange for zero runtime overhead.

## Question 36: D

A mutex has an owner that must unlock it; a semaphore provides permit counting/signaling.

Ownership is a key mutex rule; semaphore signaling need not come from an owning thread.

## Question 37: D

It waits until a permit becomes available.

All three permits have been consumed, so the next acquire cannot proceed until a release.

## Question 38: A

Atomically releases it while blocking and reacquires it before returning.

The release lets another thread change shared state; the predicate must be rechecked after waking.

## Question 39: D

Circular wait

A consistent global acquisition order prevents a cycle of lock dependencies.

## Question 40: D

A starved process waits indefinitely while others progress; a deadlocked set cannot progress because of resource dependencies.

Unrelated processes may continue during a deadlock; starvation does not require a resource cycle.
