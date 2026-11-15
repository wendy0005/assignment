# BCL1313 Lab Assessment 1

Chan Jing Yi | SUOL2500321

## Submission files

The dated PDF contains the report, explanation of FIFO and LIFO, complexity analysis, execution screenshots and the 173 word reflection. Submit it together with `restaurant_orders.cpp` and the four task screenshots in `evidence/01_queue_peek.png` through `evidence/04_stack_pop.png`. The validation screenshot is supplementary and stays outside the submission ZIP. The dated ZIP contains only the PDF report, restaurant_orders.cpp and four required task screenshots; check the submission portal's accepted file types. Editable Markdown, tests, rendering helpers and other working files stay outside the ZIP.

The reflection is a draft. Read it and adapt the first person statements to your own experience before submission. Review the code and practise the operations so you can explain the implementation.

## Compile and run

From this assignment directory, with a C++17 compiler installed:

```sh
g++ -std=c++17 -Wall -Wextra -Wpedantic restaurant_orders.cpp -o restaurant_orders
./restaurant_orders
```

Run the complete assessment demonstration:

```sh
./restaurant_orders --demo
```

The interactive program starts empty and generates an order identifier for every accepted new order. Menu choice 2 removes the front order and automatically pushes it onto the completed stack. There is no separate manual Push menu item because completion is the sole path into that stack. Each structure holds ten records. Pop removes history and does not requeue an order. Data resets on exit.

## Expected demonstration state

The initial queue is ORD001 to ORD005. ORD001 is processed, ORD006 arrives, then ORD002 and ORD003 are processed. The completed stack is ORD003, ORD002, ORD001 from top to bottom. After Pop, the stack is ORD002 above ORD001 and the queue remains ORD004, ORD005, ORD006.

## Reproduce validation

Use the workspace virtual environment for Python helpers. From the workspace root:

```sh
.venv/bin/python 'current_sem/BCL1313 - Algorithms and Complexity/assignment/20261115_Lab_Assessment_1/verify.py' --sanitize
```

The helper compiles both C++ files, checks the actual interactive program and saves genuine stdout in `evidence/`. Omit `--sanitize` if the compiler does not provide address and undefined behaviour sanitizers. Do not compile the assertion based tests with `NDEBUG`.

`render_report.py` regenerates the output screenshots and PDF from the Markdown and captured stdout. It requires the workspace's Markdown and Playwright packages, Chrome, and Mermaid JavaScript, which is downloaded into `build/` on the first run. This HTML is a print preview for the assignment report, not a course platform page.

`build/` contains local binaries, rendering dependencies and visual review images. These are excluded from the submission ZIP. The original assessment brief is retained locally and is also excluded from that ZIP.
