
# Pathfinder

## Overview
A full-screen interactive pathfinding visualizer. Features a 50x50 node grid (2,500 nodes) covering the entire screen. Click any node to set a start point, click another to set the end point, and watch the shortest path illuminate instantly using the A* algorithm.

## How to Use
1. **Click a node** - Sets the start point (green)
2. **Click another node** - Sets the end point (red) and calculates the shortest path (yellow)
3. **Click again** - Resets and selects a new start point
4. **New Graph** - Generates a fresh random graph
5. **Clear** - Clears selection without regenerating

## Project Structure
```
/
├── app.py              # Flask API server
├── src/
│   ├── __init__.py
│   └── algorithms.py   # Dijkstra & A* with binary heap
├── templates/
│   └── index.html      # Full-screen canvas visualization
└── replit.md           # This file
```

## Features
- **50x50 Node Grid** - 2,500 interconnected nodes with random jitter for organic appearance
- **Real-time Pathfinding** - A* algorithm with Euclidean heuristic
- **Performance Stats** - Distance, nodes explored, and execution time displayed live
- **Minimalistic UI** - Dark theme with floating controls

## Running Locally
```bash
pip install flask flask-cors
python app.py
```
Open http://localhost:5000

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Interactive visualizer |
| `/api/health` | GET | Health check |
| `/api/pathfind/dijkstra` | POST | Dijkstra's algorithm |
| `/api/pathfind/astar` | POST | A* algorithm |
| `/api/pathfind/compare` | POST | Compare all algorithms |
| `/api/docs` | GET | API documentation (JSON) |

## Algorithm Complexity
- **Dijkstra**: O((V + E) log V) using binary heap
- **A***: O((V + E) log V) with heuristic optimization

## Technologies
- Python 3.11
- Flask + Flask-CORS
- HTML5 Canvas
- heapq (binary heap priority queue)
