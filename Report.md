# Efficient Page Replacement Algorithm Simulator

## 1. Project Overview

### 1.1 Problem Context

In a virtual memory system, a process may need more pages than the number of physical frames available. When a requested page is not in memory (page fault), the operating system must **choose a victim page** to remove from memory and load the new page. The decision strategy is called a **page replacement algorithm**.

Different algorithms (e.g., FIFO, LRU, Optimal) give different performance depending on the reference pattern. For students, it is often difficult to understand:
- how frames are updated step by step
- why one algorithm produces more or fewer page faults than another

### 1.2 Goal of the Project

The goal of this project is to **design and implement a simulator** that:

- Accepts a page reference string and number of frames.
- Simulates **FIFO**, **LRU**, and **Optimal** page replacement algorithms.
- Shows **step‑by‑step visualization** of frame contents.
- Calculates and displays **performance metrics**:
  - total page faults
  - total hits
  - hit ratio / miss ratio
- Compares algorithms using **simple charts and tables**.

### 1.3 Expected Outcomes

By the end of the project, the user should be able to:

- Clearly **see how each algorithm works** at each page reference.
- **Compare efficiency** of different algorithms for the same input.
- Understand the trade‑offs between algorithms (e.g., FIFO anomaly, LRU vs Optimal).
- Use the simulator as a **learning tool** for Operating Systems concepts.

### 1.4 Scope

Included in scope:
- Implementation of three classical algorithms: FIFO, LRU, Optimal.
- Menu‑driven CLI interface with basic text visualization.
- Simple bar chart for page‑fault comparison.
- Clean, modular Python implementation with comments.

Out of scope (optional extensions / future work):
- Advanced algorithms like LFU, MFU, Second‑Chance, Clock.
- Web‑based GUI or desktop GUI using frameworks.
- Extremely large‑scale performance testing.

---

## 2. Module‑Wise Breakdown

The project is divided into **three main modules**:

1. **Core Simulation Module**
2. **User Interface & Control Module**
3. **Visualization & Reporting Module**

### 2.1 Core Simulation Module

**Purpose:**  
Implements the actual page replacement logic for FIFO, LRU and Optimal. This module is responsible for:
- reading the reference string (from UI layer)
- simulating each algorithm
- returning detailed step‑by‑step results and summary metrics

**Key Responsibilities:**
- Maintain frame states at each step.
- Detect page faults / hits.
- Calculate metrics such as total faults and hit ratio.

**Files / Components:**
- `PageReplacementSimulator` class
- Functions: `simulate_fifo`, `simulate_lru`, `simulate_optimal`

### 2.2 User Interface & Control Module

**Purpose:**  
Provides a simple, menu‑driven command‑line interface to:
- get inputs from the user
- allow algorithm selection
- coordinate calls to the Core Simulation Module
- show outputs in a readable format

**Key Responsibilities:**
- Display menus and read user choices.
- Validate user input (e.g., number of frames > 0).
- Call appropriate simulation functions.
- Print frame‑by‑frame tables and final metrics.

**Files / Components:**
- `main()` function in `main.py`
- Input helper functions
- Console output formatting functions

### 2.3 Visualization & Reporting Module

**Purpose:**  
Helps users **visually compare** algorithm performance.

**Key Responsibilities:**
- Draw a **bar chart** showing page faults of each algorithm.
- Display tabular results in a uniform format.
- Support exporting results (this version prints to screen; file export can be future work).

**Files / Components:**
- `visualize_comparison` function (uses `matplotlib`)
- Simple text‑based tables for each algorithm.

---

## 3. Functionalities

### 3.1 Core Simulation Module Functionalities

1. **Reference String Parsing**
   - Input: string like `7 0 1 2 0 3 0 4 2 3 0 3`.
   - Output: list of integers `[7,0,1,2,...]`.

2. **FIFO Simulation**
   - Uses a queue to store pages in frames.
   - When a new page fault occurs and memory is full, removes the **oldest loaded page**.
   - Tracks:
     - frame contents after each reference
     - whether current access was hit or fault

3. **LRU Simulation**
   - Uses a data structure (e.g., list or dictionary) to track **last used time**.
   - On page fault with full frames, removes the page that was **least recently used**.

4. **Optimal Simulation**
   - Looks ahead in the reference string to find which page will be used **farthest in the future** (or not used at all) and removes it.
   - Gives the minimum possible number of page faults for the given reference string.

5. **Metric Calculation**
   - **Total page faults** for each algorithm.
   - **Total hits** = length(reference string) − faults.
   - **Hit ratio** and **miss ratio**.

### 3.2 User Interface & Control Module Functionalities

1. **Menu Display**
   - Example menu:
     - 1. Run all algorithms (FIFO, LRU, Optimal)
     - 2. Run a single algorithm
     - 0. Exit

2. **Input Collection**
   - Number of frames.
   - Reference string:
     - User can enter manually, or
     - Choose from predefined examples.

3. **Simulation Control**
   - Based on user choice, calls:
     - `simulate_fifo`, `simulate_lru`, `simulate_optimal`
   - Aggregates results for visualization.

4. **Text‑based Visualization**
   - For each step, prints a row:
     - current page
     - frame contents
     - status (Hit / Fault)
   - Example:

     ```
     Step | Page | Frames  | Result
     -----+------+---------+--------
       1  |  7   | 7 - -   | Fault
       2  |  0   | 7 0 -   | Fault
       3  |  1   | 7 0 1   | Fault
       4  |  2   | 2 0 1   | Fault (replaced 7)
     ```

### 3.3 Visualization & Reporting Module Functionalities

1. **Bar Chart for Page Faults**
   - X‑axis: algorithm names (FIFO, LRU, Optimal).
   - Y‑axis: total page faults.
   - Helps visually see which algorithm is better.

2. **Summary Table**
   - Displays:
     - Algorithm name
     - Total page faults
     - Total hits
     - Hit ratio (%)

3. **Export‑ready Output**
   - All text outputs are clean and formatted.
   - Students can take screenshots or copy text into their report.

---

## 4. Technology Used

### 4.1 Programming Languages

- **Python 3**

Reasons:
- Simple syntax and readability.
- Quick to prototype algorithms.
- Rich ecosystem for visualization (matplotlib).

### 4.2 Libraries and Tools

- **matplotlib**
  - For bar chart visualization of page faults.
- **Standard Python Libraries**
  - `dataclasses`, `typing`, `collections`, `math` (for clean implementation).

### 4.3 Other Tools

- **Git & GitHub**
  - Version control.
  - Maintaining revision history (at least 7 commits).
  - Using branches for new features:
    - e.g., `feature/lru`, `feature/optimal`, `feature/visualization`.

---

## 5. Flow Diagram

Below is a simple logical flow of the simulator:

```text
          ┌────────────────────────────┐
          │        Start Program       │
          └─────────────┬──────────────┘
                        │
              ┌─────────▼─────────┐
              │  Show Main Menu   │
              └─────────┬─────────┘
                        │
        ┌───────────────▼────────────────┐
        │ Read user choice & input data  │
        │  - number of frames            │
        │  - reference string            │
        └───────────────┬────────────────┘
                        │
        ┌───────────────▼─────────────────┐
        │ Run selected simulations         │
        │  - FIFO / LRU / Optimal          │
        └───────────────┬─────────────────┘
                        │
        ┌───────────────▼─────────────────┐
        │ For each algorithm:             │
        │  - simulate step by step        │
        │  - record frame states          │
        │  - count hits / faults          │
        └───────────────┬─────────────────┘
                        │
        ┌───────────────▼─────────────────┐
        │ Display detailed tables &       │
        │ summary metrics                 │
        └───────────────┬─────────────────┘
                        │
        ┌───────────────▼─────────────────┐
        │ Show comparison bar chart       │
        └───────────────┬─────────────────┘
                        │
        ┌───────────────▼─────────────────┐
        │ Another simulation? (Y/N)       │
        └───────┬─────────────────────────┘
                │Yes
                │
                └───────────(Back to Menu)
                │
                ▼ No
        ┌────────────────────────────┐
        │         Exit Program       │
        └────────────────────────────┘
```

---

## 6. Revision Tracking on GitHub

- **Repository Name:** `efficient-page-replacement-simulator`  *(you can change as you like)*
- **GitHub Link:** `https://github.com/<your-username>/efficient-page-replacement-simulator`

### Suggested GitHub Workflow

1. **Initialize Repository**
   - Create a new repo on GitHub.
   - Clone it to your local machine.
   - Add initial files (`README.md`, basic `main.py`) and commit.

2. **Use Branches**
   - `feature/fifo` – implement FIFO algorithm.
   - `feature/lru` – implement LRU algorithm.
   - `feature/optimal` – implement Optimal algorithm.
   - `feature/visualization` – add matplotlib charts.

3. **Minimum 7 Commits (Examples)**
   - `chore: initialize project structure`
   - `feat: add fifo page replacement`
   - `feat: add lru page replacement`
   - `feat: add optimal page replacement`
   - `feat: add step-by-step table printing`
   - `feat: add matplotlib comparison chart`
   - `refactor: clean code & improve comments`

---

## 7. Conclusion and Future Scope

### 7.1 Conclusion

This project successfully implements a **Page Replacement Algorithm Simulator** supporting:
- FIFO
- LRU
- Optimal

The simulator provides:
- clear, step‑by‑step frame visualization
- performance metrics (page faults, hits, hit ratio)
- comparison of algorithms using a bar chart

It helps students **visually understand** how page replacement works in an Operating System and why some algorithms are more efficient than others for specific reference patterns.

### 7.2 Future Scope

Possible extensions:

1. **Additional Algorithms**
   - LFU, MFU, NRU, Second‑Chance, Clock etc.

2. **Graphical User Interface**
   - Web interface using Flask/React.
   - Desktop GUI using Tkinter or PyQt.

3. **Input / Output Enhancements**
   - Load reference strings from a file.
   - Export results and charts as PDF/PNG.

4. **Performance Analysis**
   - Compare algorithms over many random reference strings.
   - Generate graphs of faults vs frames.

---

## 8. References

1. Abraham Silberschatz, Peter B. Galvin, Greg Gagne, *Operating System Concepts*.
2. William Stallings, *Operating Systems: Internals and Design Principles*.
3. Online tutorials and documentation for Python and matplotlib.

---

# Appendix

## Appendix A: AI‑Generated Project Elaboration / Breakdown Report

*(You can paste this full document as Appendix A in your college report.  
If your college needs only the “AI Explanation” part, you can paste sections 1–5.)*

## Appendix B: Problem Statement

> **Efficient Page Replacement Algorithm Simulator**  
> Design a simulator that allows users to test and compare different page replacement algorithms (e.g., FIFO, LRU, Optimal). The simulator should provide visualizations and performance metrics to aid in understanding algorithm efficiency.

## Appendix C: Solution / Code

The complete project source code is provided in the `src/` folder:

- `src/main.py` – main entry point and implementation of algorithms, CLI, and visualization.

You can paste the contents of `main.py` into your report as required.
