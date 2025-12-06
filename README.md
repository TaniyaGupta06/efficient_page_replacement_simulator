# Efficient Page Replacement Algorithm Simulator

This project is a simple simulator to understand and compare **page replacement algorithms**:
- FIFO (First-In, First-Out)
- LRU (Least Recently Used)
- Optimal (Belady's algorithm)

It is designed for an Operating Systems mini‑project and follows your college format:
- Project overview
- Module-wise breakdown
- Functionality description
- Technology used
- Flow diagram
- GitHub revision tracking
- Conclusion & future scope
- Appendices (AI breakdown, problem statement, code)

## How to Run

1. Make sure you have **Python 3.8+** installed.
2. (Optional) Create and activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the simulator:
   ```bash
   python src/main.py
   ```

## What the Simulator Does

- Accepts a page reference string and number of frames.
- Simulates FIFO, LRU and Optimal algorithms.
- Shows a **step-by-step frame table** for each algorithm.
- Shows **page faults, hits, hit ratio**.
- Draws a **bar chart** comparing page faults of each algorithm.

You can use the outputs and screenshots from this simulator in your **project report** and **presentation**.
