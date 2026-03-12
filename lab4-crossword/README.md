# Lab 4 — Crossword

## 📝 Overview
This lab generates crossword puzzles using constraint satisfaction and backtracking search.  
The solver fills a crossword grid with words that satisfy structural and semantic constraints.

## 🧠 Concepts Covered
- Constraint satisfaction problems (CSPs)
- Backtracking search
- Node and arc consistency
- Heuristics (MRV, degree, LCV)

## 📂 Files
- `crossword.py` — crossword structure  
- `generate.py` — CSP solver and generator  
- `data/` — word lists and structures

## ▶️ How to Run
python3 generate.py data/structure0.txt data/words0.txt output.png

## 🧪 Notes
This lab demonstrates how heuristics dramatically improve CSP performance.
