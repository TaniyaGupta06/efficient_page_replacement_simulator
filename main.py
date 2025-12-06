"""
Efficient Page Replacement Algorithm Simulator
=============================================
Implements FIFO, LRU, and Optimal page replacement algorithms with:

- Step-by-step frame table printing.
- Summary metrics (faults, hits, hit ratio).
- Bar chart comparison of page faults using matplotlib.

Run this file directly:

    python main.py
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple
import math

import matplotlib.pyplot as plt


@dataclass
class StepResult:
    step: int
    page: int
    frames: List[int]
    is_hit: bool


@dataclass
class AlgorithmResult:
    name: str
    steps: List[StepResult]
    total_faults: int

    @property
    def total_accesses(self) -> int:
        return len(self.steps)

    @property
    def total_hits(self) -> int:
        return self.total_accesses - self.total_faults

    @property
    def hit_ratio(self) -> float:
        if self.total_accesses == 0:
            return 0.0
        return self.total_hits / self.total_accesses

    @property
    def miss_ratio(self) -> float:
        return 1.0 - self.hit_ratio


def simulate_fifo(reference: List[int], frames_count: int) -> AlgorithmResult:
    name = "FIFO"
    frames: List[int] = []
    order: List[int] = []  # queue for FIFO
    steps: List[StepResult] = []
    faults = 0

    for i, page in enumerate(reference, start=1):
        if page in frames:
            # hit
            is_hit = True
        else:
            # fault
            faults += 1
            is_hit = False
            if len(frames) < frames_count:
                frames.append(page)
                order.append(page)
            else:
                # remove oldest (front of queue)
                victim = order.pop(0)
                victim_index = frames.index(victim)
                frames[victim_index] = page
                order.append(page)
        steps.append(StepResult(i, page, frames.copy(), is_hit))

    return AlgorithmResult(name=name, steps=steps, total_faults=faults)


def simulate_lru(reference: List[int], frames_count: int) -> AlgorithmResult:
    name = "LRU"
    frames: List[int] = []
    last_used: Dict[int, int] = {}  # page -> last used step
    steps: List[StepResult] = []
    faults = 0

    for i, page in enumerate(reference, start=1):
        if page in frames:
            # hit
            is_hit = True
            last_used[page] = i
        else:
            # fault
            faults += 1
            is_hit = False
            if len(frames) < frames_count:
                frames.append(page)
                last_used[page] = i
            else:
                # choose least recently used page
                lru_page = min(frames, key=lambda p: last_used.get(p, 0))
                victim_index = frames.index(lru_page)
                frames[victim_index] = page
                last_used[page] = i
        steps.append(StepResult(i, page, frames.copy(), is_hit))

    return AlgorithmResult(name=name, steps=steps, total_faults=faults)


def simulate_optimal(reference: List[int], frames_count: int) -> AlgorithmResult:
    name = "Optimal"
    frames: List[int] = []
    steps: List[StepResult] = []
    faults = 0

    n = len(reference)

    for i, page in enumerate(reference, start=1):
        current_index = i - 1
        if page in frames:
            # hit
            is_hit = True
        else:
            # fault
            faults += 1
            is_hit = False
            if len(frames) < frames_count:
                frames.append(page)
            else:
                # choose the page that will not be used for the longest time
                farthest_use = -1
                victim_index = -1
                for idx, p in enumerate(frames):
                    try:
                        next_use = reference.index(p, current_index + 1)
                    except ValueError:
                        # not used again – best choice
                        victim_index = idx
                        farthest_use = math.inf
                        break
                    if next_use > farthest_use:
                        farthest_use = next_use
                        victim_index = idx
                if victim_index == -1:
                    victim_index = 0
                frames[victim_index] = page
        steps.append(StepResult(i, page, frames.copy(), is_hit))

    return AlgorithmResult(name=name, steps=steps, total_faults=faults)


def print_step_table(result: AlgorithmResult) -> None:
    print(f"\n===== {result.name} Algorithm Step-by-Step =====")
    # Determine max number of frames to format columns
    if not result.steps:
        print("No steps to show.")
        return

    max_frames = len(result.steps[0].frames)
    header_frames = " ".join([f"F{i+1}" for i in range(max_frames)])
    print(f"{'Step':>4} | {'Page':>4} | {header_frames:<{3*max_frames}} | Result")
    print("-" * (17 + 3 * max_frames))

    for step in result.steps:
        frame_strs = []
        for j in range(max_frames):
            if j < len(step.frames) and step.frames[j] is not None:
                frame_strs.append(str(step.frames[j]))
            else:
                frame_strs.append("-")
        frame_str = " ".join(f"{fs:>2}" for fs in frame_strs)
        res = "Hit" if step.is_hit else "Fault"
        print(f"{step.step:>4} | {step.page:>4} | {frame_str:<{3*max_frames}} | {res}")


def print_summary(results: List[AlgorithmResult]) -> None:
    print("\n===== Summary Comparison =====")
    print(f"{'Algorithm':<10} | {'Faults':>6} | {'Hits':>6} | {'Hit Ratio (%)':>13}")
    print("-" * 45)
    for res in results:
        hit_ratio_percent = res.hit_ratio * 100
        print(f"{res.name:<10} | {res.total_faults:>6} | {res.total_hits:>6} | {hit_ratio_percent:>12.2f}")


def visualize_comparison(results: List[AlgorithmResult]) -> None:
    names = [r.name for r in results]
    faults = [r.total_faults for r in results]

    plt.figure()
    plt.bar(names, faults)
    plt.xlabel("Algorithm")
    plt.ylabel("Total Page Faults")
    plt.title("Page Fault Comparison")
    plt.tight_layout()
    print("\nShowing bar chart window... Close the window to continue.")
    plt.show()


def get_reference_string_from_user() -> List[int]:
    print("\nChoose reference string input mode:")
    print("1. Enter manually")
    print("2. Use sample reference string (7 0 1 2 0 3 0 4 2 3 0 3 2)")
    choice = input("Enter choice (1/2): ").strip()

    if choice == "2":
        return [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]

    while True:
        s = input("Enter space-separated page reference string (e.g., 7 0 1 2 0 3 0 4): ").strip()
        try:
            ref = [int(x) for x in s.split()]
            if not ref:
                raise ValueError
            return ref
        except ValueError:
            print("Invalid input. Please enter integers separated by spaces.")


def get_frames_from_user() -> int:
    while True:
        s = input("Enter number of frames (positive integer): ").strip()
        try:
            n = int(s)
            if n <= 0:
                raise ValueError
            return n
        except ValueError:
            print("Invalid input. Please enter a positive integer.")


def main_menu():
    print("\n==============================")
    print(" Efficient Page Replacement Simulator")
    print("==============================")
    print("1. Run all algorithms (FIFO, LRU, Optimal)")
    print("2. Run a single algorithm")
    print("0. Exit")


def select_single_algorithm():
    print("\nSelect algorithm:")
    print("1. FIFO")
    print("2. LRU")
    print("3. Optimal")
    choice = input("Enter choice (1/2/3): ").strip()
    mapping = {"1": "FIFO", "2": "LRU", "3": "Optimal"}
    return mapping.get(choice)


def main():
    while True:
        main_menu()
        choice = input("Enter choice: ").strip()

        if choice == "0":
            print("Exiting simulator. Goodbye!")
            break

        elif choice in ("1", "2"):
            frames = get_frames_from_user()
            reference = get_reference_string_from_user()

            if choice == "1":
                # Run all algorithms
                fifo_res = simulate_fifo(reference, frames)
                lru_res = simulate_lru(reference, frames)
                opt_res = simulate_optimal(reference, frames)

                for res in (fifo_res, lru_res, opt_res):
                    print_step_table(res)

                print_summary([fifo_res, lru_res, opt_res])

                visualize_comparison([fifo_res, lru_res, opt_res])

            else:
                # Single algorithm
                algo_name = select_single_algorithm()
                if not algo_name:
                    print("Invalid algorithm choice.")
                    continue

                if algo_name == "FIFO":
                    res = simulate_fifo(reference, frames)
                elif algo_name == "LRU":
                    res = simulate_lru(reference, frames)
                else:
                    res = simulate_optimal(reference, frames)

                print_step_table(res)
                print_summary([res])

        else:
            print("Invalid menu choice. Please try again.")


if __name__ == "__main__":
    main()
