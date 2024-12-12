# AI 3x3 Board Game Solver  

This repository contains a project developed for the SE420 Artificial Intelligence course. The goal is to solve a 3x3 board game puzzle using the A* algorithm with Manhattan distance heuristic.

## Project Overview  
- **Goal**: Move tiles on a 3x3 board to reach the user-defined goal state.
- **Algorithm**: A* search algorithm with Manhattan distance heuristic.
- **Requirements**:
  1. User-defined initial and goal states.
  2. Moves allowed: up, down, left, right (with associated costs).
  3. Tiles move in a fixed order (Tile #1, Tile #2, Tile #3, ..., repeat).
  4. Expansion stops after 10 nodes or when the goal state is reached.
  5. Each expanded state is printed and compared with the goal state.
