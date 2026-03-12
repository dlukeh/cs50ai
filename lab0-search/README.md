# Lab 0 — Search

## 📝 Overview
This lab implements search algorithms to find the shortest path between two actors using the “Six Degrees of Kevin Bacon” problem.  
The program loads a dataset of movies and actors, builds a graph, and uses search to find the connection path.

## 🧠 Concepts Covered
- Breadth-first search (BFS)
- Depth-first search (DFS)
- Graph modeling
- Queue-based frontier management
- Path reconstruction

## 📂 Files
- `degrees.py` — main solution  
- `util.py` — helper functions  
- `large/` and `small/` — datasets (ignored in GitHub)

## ▶️ How to Run
python3 degrees.py

## 🧪 Notes
This lab builds foundational intuition for search algorithms and state-space exploration.  
BFS guarantees the shortest path, making it ideal for this problem.
