# Arslan’s Land — Pathfinding Adventure

A simple Python simulation showing how a robot navigates a 2D grid world using the **Weighted A*** algorithm.
The program visualises how terrain, obstacles, and heuristic weight affect pathfinding decisions.

 ## Project Overview
The program models a map (grid world) where each cell can represent:
- N → Normal terrain (cost 1)
- H → Hill (cost 3)
- W → Water (cost 5)
- O → Obstacle (impassable)
Using the Weighted A* algorithm, the robot calculates the most cost-effective route from start to goal, balancing between speed and accuracy depending on the heuristic weight chosen by the user.

## Features
Interactive terminal interface (choose grid size, terrain type, heuristic weight)
Random terrain generation with adjustable probabilities
Real-time robot path animation in the console
Option to manually add new obstacles and re-run pathfinding
Weighted A* algorithm — customise heuristic weight to simulate:
* w = 0 → Dijkstra’s algorithm
* 0 < w < 1 → Cautious A*
* w = 1 → Standard A*
* w > 1 → Aggressive A*

## Project Structure

 - mapworld.py: Contains the Map class and all algorithms (A*, helpers, animation)
 - main.py: Handles user input, menus, and overall program control
 - README.md        

## Weighted A* Algorithm Explained
Weighted A* adds a heuristic multiplier (w) to the standard A* formula:
* f(n) = g(n) + w * h(n) <br>where:
* w = 1 → Standard A* (optimal and efficient)
* w > 1 → Prioritises speed (less accurate but faster)
* w < 1 → Prioritises accuracy (more cautious, slower)

## Key Components
 ### Map class (mapworld.py)
 * Grid generation
 * Boundary check
 * Obstacle detection
 * Terrain cost calculation
 * A* pathfinding
 * animation of robot movement

### Main Program (main.py)
* User input
* Menu navigation
* Execution flow
* Visual display and final summary

## Learning Objectives 
- How pathfinding algorithms work (BFS, Dijkstra, A*)
- The impact of terrain cost on route selection
- How heuristics affect performance and accuracy
- Modular Python design for clarity and maintainability

## Future Improvements
* Add diagonal movement options
* Implement GUI (Tkinter or Pygame) for visual display
* Compare multiple algorithms side by side
* Add file saving/loading for maps
