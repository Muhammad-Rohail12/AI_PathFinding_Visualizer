# AI Dynamic Pathfinding Agent

This project is a Python-based visualizer for pathfinding algorithms, built using Pygame. It demonstrates A* (A-Star) and Greedy Best-First Search (GBFS) navigating around user-drawn walls and dynamically generated obstacles.

## Features
* **Algorithms:** A* Search and Greedy Best-First Search.
* **Heuristics:** Toggle between Manhattan and Euclidean distances.
* **Dynamic Mode:** Obstacles can spawn in real-time while the agent is moving.
* **Grid Resizing:** Zoom in and out without losing your drawn walls.

## Prerequisites
To run this project, you need to have Python installed on your computer. You also need the Pygame library.

## Installation & Setup
1. Clone this repository or download the `main.py` file to your machine.
2. Open your terminal or command prompt.
3. Install the required dependency by running the following command:
   ```bash
   pip install pygame

How to Run
Once Pygame is installed, navigate to the folder containing the file and run:
Bash
python main.py

**Controls**
**Left Click:** Draw Start Node (Orange), End Node (Turquoise), and Walls (Black).

**Right Click:** Erase nodes/walls.

**SPACE:** Start the pathfinding algorithm.

**C:** Clear the board.

**R:** Generate a random 30% wall maze.

**A / G:** Toggle between A* and GBFS.

**H:** Toggle between Manhattan and Euclidean heuristics.

**D:** Toggle Dynamic Mode (moving obstacles) ON/OFF.

**+ / -:** Increase or decrease the grid size.
