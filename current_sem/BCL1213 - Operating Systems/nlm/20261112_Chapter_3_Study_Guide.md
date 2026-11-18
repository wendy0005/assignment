# Chapter 3 Revision Guide: Memory Management

---

### 1. Course Context & Module Overview

> **COURSE METADATA & CONTEXT**
> * **Course Codes:** BTL1213 / BIT1213 / BCL1213 Operating Systems
> * **Institution:** SEGi University
> * **Topic:** Chapter 3: Memory Management (Part B)
> * **Lecturer:** Ruffinus Rusell

Memory management is an essential core function of operating systems responsible for dynamically allocating, tracking, and freeing memory space for active processes. The primary objective of memory management is to enable multiple programs to execute simultaneously in a shared environment while preventing inter-process memory corruption, optimizing CPU instruction speed, and maximizing physical RAM utilization.

**Key Learning Objectives:**
* **Understand Memory Concepts:** Define operating system memory management and explain its critical role in system execution and process isolation.
* **Identify Memory Architecture Types:** Classify different forms of physical and virtual memory within the hardware storage hierarchy.
* **Analyze Allocation Techniques:** Evaluate contiguous and non-contiguous memory allocation strategies through practical examples.
* **Explain Factors Affecting Memory Speed:** Identify and explain the performance metrics that influence access speed, address translation, and dynamic memory efficiency.

---

### 2. Memory Allocation Strategies & Memory Hierarchy

#### Memory Hierarchy
The memory hierarchy organizes system memory units into distinct structural layers based on access speed, capacity, and cost per byte:

1. **Registers:** Ultra-fast, high-cost, low-capacity storage units situated directly inside the CPU core (32 to 64 registers per core).
   * **Accumulator (ACC):** Temporarily stores arithmetic and logic processing results.
   * **Program Counter (PC):** Holds the memory address of the next instruction to be fetched and executed.
   * **Instruction Register (IR):** Holds the instruction currently undergoing decoding/execution.
   * **Stack Pointer (SP):** Stores the boundary offset of the active function execution stack.
2. **Main Memory (Physical RAM):** Moderate-capacity, high-speed volatile storage accessed directly by the CPU via the system bus.
3. **Secondary Storage:** Slower, low-cost, high-capacity non-volatile storage used for persistent file systems and virtual memory paging space.

#### Memory Allocation Classification
Memory allocation strategies determine how physical memory blocks are assigned to process instructions and data during execution:

| Property | Contiguous Memory Allocation | Non-Contiguous Memory Allocation |
| :--- | :--- | :--- |
| **Definition** | Assigns a single, continuous block of adjacent physical memory addresses to a process. | Divides a process into multiple sections placed across non-adjacent physical memory locations. |
| **Flexibility** | Rigid; requires a single unbroken block large enough to house the entire process footprint. | Highly flexible; allows processes to load even if available physical memory is fragmented into separate blocks. |
| **Partitioning Type** | Fixed (Static) Partitioning or Dynamic (Variable) Partitioning. | Page-based (fixed-size) or Segment-based (variable-size) logical structures. |
| **Typical Sub-techniques** | • Single Contiguous Allocation<br>• Fixed (Static) Partitioning<br>• Dynamic (Variable) Partitioning | • Paged Memory Management<br>• Segmented Memory Management<br>• Segmented Memory Management with Paging |

#### OS Memory Performance Factors
The efficiency of a memory management subsystem is evaluated using five key performance factors:
1. **Access Time:** The operational time (measured in nanoseconds) required for the CPU to read or write data to a memory location.
2. **Page Fault Rate:** The ratio of memory accesses that result in page faults requiring disk fetch operations.
3. **Memory Efficiency / Utilization:** The percentage of total physical RAM actively holding usable process data without being lost to internal or external fragmentation.
4. **Scalability:** The system's capacity to maintain acceptable memory access times as the number of concurrent processes scales up.
5. **Reliability:** The ability of the OS to maintain memory boundary protection, preventing illegal memory references, memory leaks, and system crashes.

---

### 3. Memory Fragmentation: Internal vs. External

Fragmentation is the degradation of usable memory space over time, which reduces system efficiency and can prevent process allocation despite having sufficient total free capacity.

* **Internal Fragmentation:**
  * **Exact Cause:** Occurs when a process is assigned a fixed-size memory partition (or page frame) that exceeds its actual size requirement. The unused space remains trapped inside the assigned block and cannot be used by other processes.
  * **Associated Partitioning Method:** Fixed (Static) Partitioning and Paging systems.
  * **Primary Remedy:** Utilizing Dynamic Partitioning or selecting smaller, optimal page frame sizes.

* **External Fragmentation:**
  * **Exact Cause:** Occurs when dynamic memory allocation leaves small, non-contiguous gaps ("holes") between occupied memory regions. Although the total aggregate free memory is sufficient for an incoming process, no single continuous block is large enough to satisfy the allocation request.
  * **Associated Partitioning Method:** Dynamic (Variable) Partitioning and pure Segmentation systems.
  * **Primary Remedy:** Memory compaction (revising allocated memory to merge free gaps) or adopting non-contiguous allocation strategies such as Paging.

---

### 4. Paging and Segmentation Architecture

Non-contiguous memory management decouples a program's logical address space from physical RAM layout using Paging or Segmentation.

#### Paging Mechanics
* **Pages & Frames:** Logical memory is divided into fixed-sized blocks called **Pages**. Physical memory (RAM) is divided into equal fixed-sized blocks called **Frames**.
* **Mapping:** The system maintains a **Page Table** for each process to translate logical page numbers directly into physical frame numbers.

```
LOGICAL MEMORY (Process)          PAGE TABLE               PHYSICAL RAM
+------------------+          +--------------+          +------------------+
| Page 0           |--------->| Page | Frame |--------->| Frame 0 (Page 1) |
+------------------+          +------+-------+          +------------------+
| Page 1           |-------+  |  0   |   2   |          | Frame 1          |
+------------------+       |  |  1   |   0   |---+      +------------------+
| Page 2           |----+  |  |  2   |   3   |  +------>| Frame 2 (Page 0) |
+------------------+    |  +--+------+-------+          +------------------+
                        +------------------------------>| Frame 3 (Page 2) |
                                                        +------------------+
```

#### Segmentation Mechanics
* **Variable Segments:** Logical memory is structured into variable-sized, user-centric blocks called **Segments** based on logical program components (e.g., Code, Data, Stack).
* **Segment Table:** Translates logical segment addresses using two core attributes:
  * **Base Address:** The physical starting address of the segment in RAM.
  * **Limit:** The length/size of the segment.
* **Validation Condition:** A segment address request is valid **if and only if**:
  $$\text{Offset} < \text{Limit}$$

```
LOGICAL ADDRESS: [ Segment Number | Offset ]
                                       |
                                       v
                         +---------------------------+
                         |   Is Offset < Limit ?     |
                         +---------------------------+
                           /                       \
                   YES    /                         \  NO
                         v                           v
        +---------------------------------+   [ TRAP: SEGMENT FAULT ]
        | Physical Address = Base + Offset |   (Out-of-Bounds Access)
        +---------------------------------+
```

#### Structural Comparison

| Factor | Paging | Segmentation |
| :--- | :--- | :--- |
| **Block Size** | Fixed size (e.g., 4KB blocks). | Variable size tailored to logical program units. |
| **Hardware Terminology** | Pages (Logical) and Frames (Physical). | Segments (Logical units with physical Base addresses). |
| **Division Basis** | System/Hardware view (physical block partitioning). | User/Programmer logical view (Code, Data, Stack). |
| **Overhead / Fragmentation** | Subject to **Internal Fragmentation**. | Subject to **External Fragmentation**. |
| **Address Components** | `[Page Number, Offset]` | `[Segment Number, Offset]` |
| **Protection & Sharing** | Configured per individual fixed page block. | Configured naturally along logical code/data segment boundaries. |

---

### 5. Virtual Memory & Page Fault Dynamics

Virtual memory enables the execution of processes that are not fully loaded into physical RAM, expanding addressable memory by utilizing secondary storage space.

#### Page Fault Execution Workflow

1. **Logical Request:** The CPU issues a memory request for a logical page that is currently not present in physical RAM (the valid-invalid bit in the page table is set to invalid).
2. **Trap Interception:** The Memory Management Unit (MMU) detects the invalid access and issues a page fault hardware exception, pausing the executing process and transferring control to the OS.
3. **Storage Location:** The OS intercepts the trap and locates the required page on secondary storage (swap space/disk).
4. **Free Frame Check & Eviction Decision:**
   * The OS inspects physical RAM to determine if an unallocated **Frame** is available.
   * **Critical Eviction Rule:** If an unallocated physical frame is available, the requested page is loaded directly into that frame **without evicting existing pages**. Page replacement (eviction) occurs **only if physical RAM is completely full** (zero free frames).
5. **Page Fetch & Table Update:** The OS fetches the missing page from disk, writes it into the designated physical frame, and updates the process Page Table entry to mark it valid with its new frame index.
6. **Execution Resumption:** The OS restores CPU register states and restarts the specific instruction that triggered the page fault exception.

---

### 6. Worked Example: Segment Address Translation & Validation

#### Scenario Parameters
A system contains the following Segment Table:

| Segment Number | Base Address | Limit (Length) |
| :---: | :---: | :---: |
| **0** | 500 | 700 |
| **1** | 2000 | 450 |
| **2** | 3000 | 300 |

---

#### Calculation 1
**Problem:** A process requests access to **Segment 0** at **Offset 200**. Determine validity and calculate physical address.

* **Step 1: Validate Boundary Condition**
  Check if $\text{Offset} < \text{Limit}$:
  $$\text{Offset} = 200,\quad \text{Limit} = 700$$
  $$200 < 700 \implies \mathbf{Valid\ (True)}$$

* **Step 2: Calculate Physical Address**
  $$\text{Physical Address} = \text{Base} + \text{Offset}$$
  $$\text{Physical Address} = 500 + 200 = \mathbf{700}$$

* **Conclusion:** The request is valid. Physical address generated = **700**.

---

#### Calculation 2
**Problem:** A process requests access to **Segment 1** at **Offset 500**. Determine whether the logical address is valid.

* **Step 1: Validate Boundary Condition**
  Check if $\text{Offset} < \text{Limit}$:
  $$\text{Offset} = 500,\quad \text{Limit} = 450$$
  $$500 < 450 \implies \mathbf{Invalid\ (False)}$$

* **Conclusion:** The request is **invalid**. An out-of-bounds exception (Segment Fault trap) is raised because the requested offset ($500$) exceeds the permitted segment length ($450$). No physical address is generated.

---

#### Calculation 3
**Problem:** A process requests access to **Segment 2** at **Offset 350**. Determine validity and explain your answer.

* **Step 1: Validate Boundary Condition**
  Check if $\text{Offset} < \text{Limit}$:
  $$\text{Offset} = 350,\quad \text{Limit} = 300$$
  $$350 < 300 \implies \mathbf{Invalid\ (False)}$$

* **Conclusion:** The request is **invalid**. The requested offset ($350$) exceeds the segment limit ($300$). Access is rejected by hardware boundary checking.

---

#### Calculation 4
**Problem:** A process requests access to **Segment 1** at **Offset 600**. Determine whether the logical address is valid.

* **Step 1: Validate Boundary Condition**
  Check if $\text{Offset} < \text{Limit}$:
  $$\text{Offset} = 600,\quad \text{Limit} = 450$$
  $$600 < 450 \implies \mathbf{Invalid\ (False)}$$

* **Conclusion:** The request is **invalid**. Access is denied and a Segment Fault exception is generated because $600 \ge 450$.

---

### 7. Common Exam Pitfalls & Student Mistakes

> **Common Pitfall 1: Confusing Logical Pages with Physical Frames**  
> **Clarification Rule:** Pages exist exclusively in virtual/logical memory, whereas Frames exist in physical RAM. Pages map into frames via page tables. Do not interchange these terms during conceptual explanations.

> **Common Pitfall 2: Assuming Page Replacement Always Occurs During a Page Fault**  
> **Clarification Rule:** Eviction/replacement is **not** an automatic step for every page fault. Eviction occurs **only** when all physical RAM frames are occupied. If an unallocated free frame exists, the page is loaded directly into RAM without evicting existing pages.

> **Common Pitfall 3: Calculating Physical Addresses Without Validating Segment Limits**  
> **Clarification Rule:** Never add base addresses to offsets blindly. Always verify if $\text{Offset} < \text{Limit}$ first. If $\text{Offset} \ge \text{Limit}$, the access request is invalid and results in a segment fault; calculation of a physical address must be halted.

> **Common Pitfall 4: Misidentifying Fragmentation Types Across Allocation Methods**  
> **Clarification Rule:** Internal fragmentation occurs **inside** allocated fixed blocks (Fixed Partitioning, Paging) when assigned memory exceeds process requirements. External fragmentation occurs **between** dynamic partitions (Dynamic Partitioning, Segmentation) when available space is broken into small, non-contiguous holes.

---

### 8. Exam-Style Practice Questions & Model Solutions

#### Question 1 (Conceptual)
**Question:** Differentiate between physical RAM frames and virtual memory pages. Explain the specific system condition required to trigger a page replacement (eviction) routine during a page fault exception.

<details>
<summary><b>View Model Solution & Marking Scheme</b></summary>

* **Pages vs. Frames Differentiation:**  
  Pages are fixed-size logical address partitions defined in virtual memory. Frames are fixed-size physical memory blocks in physical RAM. The operating system page table maps logical pages to physical frames.  
* **Page Replacement Trigger Condition:**  
  Page replacement (eviction) is triggered **only when physical RAM has no free frames available** to host the missing page. If a free physical frame exists, the page is loaded into memory directly without replacing active pages.  
* **Marking Breakdown:**
  * **2 Marks:** Accurate definition and structural differentiation between Pages and Frames.
  * **2 Marks:** Correct state rule for triggering page replacement (RAM completely full / zero free frames).

</details>

---

#### Question 2 (Fragmentation Calculation)
**Question:** A system employs a fixed partitioning allocation strategy with block sizes of $4\,\text{KB}$. A process requesting $3\,\text{KB}$ of memory is assigned to one of these partitions. Identify the type of fragmentation generated, compute the precise amount of wasted memory, and state the underlying cause.

<details>
<summary><b>View Model Solution & Marking Scheme</b></summary>

* **Type of Fragmentation:** Internal Fragmentation.
* **Mathematical Calculation:**
  $$\text{Wasted Space} = \text{Partition Size} - \text{Requested Process Size}$$
  $$\text{Wasted Space} = 4\,\text{KB} - 3\,\text{KB} = \mathbf{1\,\text{KB}}$$
* **Underlying Cause:** Fixed partitioning allocates an entire static block to a single process. Any memory within the assigned block that is not used by the process remains trapped inside the partition boundary and cannot be allocated to other processes.
* **Marking Breakdown:**
  * **1 Mark:** Correctly identifying Internal Fragmentation.
  * **1 Mark:** Accurate quantitative computation ($1\,\text{KB}$).
  * **1 Mark:** Valid explanation based on static block assignment boundaries.

</details>

---

#### Question 3 (Segmentation Translation)
**Question:** A system using segmented memory management contains a segment (Segment $3$) defined by a **Base** address of $1200$ and a **Limit** of $400$.
1. Evaluate a logical request for Segment $3$ at **Offset 250**. Validate boundary conditions using LaTeX expressions and calculate the resulting physical address.
2. Evaluate a logical request for Segment $3$ at **Offset 420**. Determine request validity with mathematical proof.

<details>
<summary><b>View Model Solution & Marking Scheme</b></summary>

* **Part 1 (Offset $250$):**
  * *Boundary Validation Check:* Check if $\text{Offset} < \text{Limit}$:
    $$\text{Offset} = 250,\quad \text{Limit} = 400$$
    $$250 < 400 \implies \mathbf{True\ (Valid)}$$
  * *Address Calculation:*
    $$\text{Physical Address} = \text{Base} + \text{Offset} = 1200 + 250 = \mathbf{1450}$$
* **Part 2 (Offset $420$):**
  * *Boundary Validation Check:* Check if $\text{Offset} < \text{Limit}$:
    $$\text{Offset} = 420,\quad \text{Limit} = 400$$
    $$420 < 400 \implies \mathbf{False\ (Invalid)}$$
  * *Outcome:* Request is **Invalid**. The requested offset exceeds the segment limit ($420 \ge 400$), generating a Segment Fault hardware trap exception.
* **Marking Breakdown:**
  * **2 Marks:** Part 1 validation step ($250 < 400$) and address output ($1450$).
  * **2 Marks:** Part 2 validation proof ($420 \ge 400$) and explicit declaration of invalid access.

</details>