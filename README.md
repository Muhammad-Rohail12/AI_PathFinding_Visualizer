# 🤖 AI Dynamic Pathfinding Agent

> An interactive Python-based visualizer for pathfinding algorithms, built using Pygame. 

This tool demonstrates **A* (A-Star)** and **Greedy Best-First Search (GBFS)** in real-time, navigating around user-drawn walls and adapting to dynamically generated obstacles. It is designed to help visualize how different heuristics and algorithms explore a grid to find the optimal path.

---

## ✨ Key Features
* 🧠 **Multiple Algorithms:** Compare the efficiency of **A* Search** and **Greedy Best-First Search**.
* 📏 **Swappable Heuristics:** Toggle seamlessly between **Manhattan** and **Euclidean** distance calculations.
* 🚧 **Dynamic Obstacle Mode:** Watch the agent recalculate its path in real-time as random obstacles spawn while it moves.
* 🔍 **Preserved Grid Resizing:** Zoom in (`+`) and out (`-`) on the fly without losing your drawn walls, start, or end points.
* 📊 **Real-Time Metrics:** Live tracking of nodes expanded, final path cost, and computation time.

---

## ⚙️ Prerequisites & Installation

To run this project, you will need **Python 3.x** installed on your machine. The visualizer relies on the `pygame` library for graphics.

**1. Download the project:**
Download the `main.py` file to your computer, or clone this repository.

**2. Install dependencies:**
Open your terminal or command prompt and run the following command:
```bash
pip install pygame
```

---

## 🚀 How to Run

Once Pygame is installed, navigate to the folder containing the file and run the visualizer:
```bash
python main.py
```

---

## 🎮 User Controls & Commands

| Action | Key / Input | Description |
| :--- | :--- | :--- |
| **Draw Start/End/Wall** | `Left Click` | Places Start (Orange), End (Turquoise), and Walls (Black). |
| **Erase Node/Wall** | `Right Click` | Removes any node or wall from the grid. |
| **Start Search** | `SPACE` | Begins the pathfinding algorithm visualization. |
| **Clear Board** | `C` | Wipes the entire grid clean. |
| **Generate Maze** | `R` | Fills the board with a random 30% wall distribution. |
| **Toggle Algorithm** | `A` / `G` | Switches between A* (`A`) and GBFS (`G`). |
| **Toggle Heuristic** | `H` | Switches between Manhattan and Euclidean calculations. |
| **Dynamic Mode** | `D` | Turns real-time moving/spawning obstacles ON or OFF. |
| **Resize Grid** | `+` / `-` | Scales the grid up or down while preserving your layout. |

---
*Created for AI Pathfinding Assignment.*
