# Computer Architecture: Cache and RAM

Chan Jing Yi | SUOL2500321 | BCL1213 Operating Systems

## Scenario and recommendation

The most practical design retains both CPU cache and RAM. Cache provides fast access to frequently used instructions and data, while RAM provides much greater working capacity at a lower cost per byte. Neither proposal offers the best balance of cost, capacity and performance for a general purpose computer.

If the company must choose between the two proposals, Proposal B is generally more practical because substantial RAM can support a conventional operating system and applications, provided the processor is designed to run without cache. However, the loss of cache would usually reduce performance. Removing cache may reduce hardware cost, but it does not generally improve performance. Proposal A could suit a specialised device with a small memory requirement, but using large amounts of cache memory as main memory would be expensive.

## 1. If cache memory is much faster than RAM, why do we not use cache memory as the computer’s only main memory?

CPU cache is usually built from static random access memory (SRAM), while main memory typically uses dynamic random access memory (DRAM). SRAM needs more circuitry for each stored bit and is less dense, so large capacities require more chip area and cost more per byte. A cache large enough to replace many gigabytes of RAM would therefore be costly and difficult to fit close to the processor.

A system can use SRAM as its main memory if it is designed for that purpose, particularly when the required capacity is small. However, memory serving as main memory is not merely a conventional cache: it must provide addressable storage for the system’s working data.

## 2. If RAM can store running applications, why do modern processors still need cache memory?

RAM holds the instructions and data that active programs need, but it is slower to access than the small caches close to the processor. Without a cache, the processor would wait more often for instructions and data to arrive from RAM.

A cache keeps copies of recently used data and nearby data that may be needed soon. When the required data is present, the processor can access it quickly; when it is absent, the memory system retrieves it from a lower level of the hierarchy. This use of locality improves average access time, although the benefit depends on the workload.

## 3. What would happen if a computer had 32 GB of RAM but no CPU cache?

The computer would have enough working memory for many ordinary applications, but the processor would need to obtain instructions and data from RAM more often. Many workloads would run slower because memory accesses take longer and the processor may spend more time waiting. The exact performance loss depends on the processor design and the program.

Such a computer could operate if its processor and firmware were designed to work without caches. A conventional processor should not be assumed to boot simply because its caches have been removed; its hardware and startup requirements matter.

## 4. What if a computer had 64 MB of cache but no RAM?

A conventional cache depends on a backing memory: when data is absent, the system fetches it from a lower level. With no addressable main memory behind it, an ordinary computer generally cannot boot or run normal applications merely because it has 64 MB of cache.

A specially designed system could configure or replace the fast memory as 64 MB of addressable main memory. It might run a small operating system and simple applications, but capacity would be very limited for modern general purpose software. Storage could provide backing for virtual memory in a suitably designed system, but frequent transfers would be much slower and would not make a standard cache work as RAM automatically.

## References

Massachusetts Institute of Technology. Computation Structures, Section 14.1: Annotated Slides. https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c14/c14s1/

Cornell University. CS 3410: Caches. https://courses.cs.cornell.edu/cs3410/2026sp/notes/caches.html
