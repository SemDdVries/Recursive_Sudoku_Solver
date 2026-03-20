# Recursive Sudoku Solver

A constraint-satisfaction Sudoku solver for standard **9×9** puzzles. It combines **arc consistency (AC-3)** to shrink variable domains with **recursive backtracking** to complete the grid, and supports several **queue-processing heuristics** for comparing solver behavior.

---

## What this project does

- Loads puzzles from plain-text files (digits `0`–`9`, where `0` means empty).
- Builds a grid of cells (`Field`) linked to all peers in the same row, column, and 3×3 box.
- Runs **AC-3**: repeatedly revises arcs so each value in a cell’s domain remains supportable by at least one different value in each neighbor’s domain.
- If domains are not enough to fix every cell, runs **depth-first search with backtracking** over remaining possibilities, restoring state on failure.
- Verifies the result with **`valid_solution()`** (no duplicate values among neighbors; arc consistency of final domains).
- Prints **complexity-style metrics**: number of `revise` calls, domain removals, and maximum arc-queue size.

Sample puzzles are provided under `Sudokus/` (`Sudoku1.txt` … `Sudoku5.txt`).

---

## How it works (architecture)

| Module | Role |
|--------|------|
| **`Field.py`** | One cell: value (`0` = unknown), domain `{1..9}` for unknowns, and neighbor list. |
| **`Sudoku.py`** | Reads a puzzle file into a 9×9 grid, wires neighbors, and formats the board for display. |
| **`Game.py`** | AC-3 loop + heuristics, `revised()`, recursive backtracking (`solve_sudoku_rec`), and solution validation. |
| **`App.py`** | CLI: pick a puzzle file, run the solver, optionally repeat. |

**Execution flow**

1. `Sudoku.read_sudoku()` builds the grid and `Sudoku.add_neighbours()` attaches all constrained peers to each `Field`.
2. `Game.solve(heuristic)` seeds the arc queue with every ordered pair (cell, neighbor), then processes arcs until the queue is empty (or a domain becomes empty → failure).
3. Heuristics only change **which arc is processed next** from the queue (see below).
4. `solve_sudoku_rec()` finalizes singleton domains, then backtracks on the first cell that still has multiple values in its domain.

**Heuristics** (configured in `App.solve_sudoku()` via `game.solve(...)`)

| Name | Behavior |
|------|----------|
| `'fifo'` | Baseline: process arcs in first-in, first-out order. |
| `'mrv'` | **Minimum Remaining Values**: prefer arcs whose head cell has the smallest domain (often reduces branching). |
| `'lcv'` | **Least Constraining Values**: prefer arcs where either endpoint already has domain size 1 (near-finalized); otherwise falls back to index `0` (FIFO-like). |

---

## Requirements

- **Python 3.8+** recommended (uses f-strings and type hints as in `Game.py`).
- **No third-party packages** — only the standard library (`os`, `re`) and the project’s own modules.

---

## Installation

### 1. Get the code

Clone or copy this folder so your tree includes at least:

```
Recursive_Sudoku_Solver/
├── App.py
├── Game.py
├── Sudoku.py
├── Field.py
├── Sudokus/
│   ├── Sudoku1.txt
│   └── ...
└── README.md
```

### 2. (Optional) Virtual environment

Using a virtual environment keeps your system Python clean.

**Windows (Command Prompt / PowerShell)**

```bat
cd path\to\Recursive_Sudoku_Solver
python -m venv .venv
.venv\Scripts\activate
```

**Windows (Git Bash)**

```bash
cd /c/path/to/Recursive_Sudoku_Solver
python -m venv .venv
source .venv/Scripts/activate
```

**macOS / Linux**

```bash
cd /path/to/Recursive_Sudoku_Solver
python3 -m venv .venv
source .venv/bin/activate
```

There is no `pip install` step unless you add dependencies later.

---

## How to run

Run the interactive entry point from the **project root** (the folder that contains `App.py` and `Sudokus/`) so relative paths resolve correctly.

**Windows (Command Prompt / PowerShell)**

```bat
cd path\to\Recursive_Sudoku_Solver
python App.py
```

**Windows (Git Bash), macOS, Linux**

```bash
cd /path/to/Recursive_Sudoku_Solver
python3 App.py
```

You will be prompted to enter a Sudoku file number **`1`–`5`** (matched against filenames in `Sudokus/`). The program prints the puzzle, solver statistics, and the solved grid (or a failure message). Answer the **Continue?** prompt with something starting with **`y`** to try another puzzle.

### Changing the heuristic

Open `App.py` and edit the argument passed to `game.solve(...)`:

```python
game.solve('fifo')  # baseline
# game.solve('mrv')
# game.solve('lcv')
```

Only one call should be active for a given run.

### Puzzle file format

- **9 lines**, each **9 characters** (no spaces): digits `1`–`9` for given cells, **`0`** for empty.
- Encoding: plain UTF-8 ASCII is sufficient.

Example (first row all unknown except one digit):

```
000006080
009105372
...
```

To add your own puzzle, create `Sudokus/Sudoku6.txt` (or any name containing your chosen menu digit) and extend the prompt range in `App.start()` if you want more than five files.

---

## Troubleshooting

| Issue | What to check |
|--------|----------------|
| `FileNotFoundError` / cannot open puzzle | Run `App.py` from the directory that contains `Sudokus/`, or fix `sudoku_folder` in `App.py`. |
| `python` not found | On macOS/Linux use `python3`; on Windows install Python from [python.org](https://www.python.org/downloads/) and ensure **“Add python.exe to PATH”** is enabled. |
| Wrong puzzle loaded | The menu matches any filename in `Sudokus/` that **contains** the typed string (e.g. `1` matches `Sudoku1.txt`). |

---

## License / course use

This repository is structured as a **Knowledge AI / CSP** coursework-style solver. If you reuse it academically, follow your institution’s policies on attribution and collaboration.
