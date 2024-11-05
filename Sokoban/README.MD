# Project Title

A Sokoban game created in Python using Pygame with AI pathfinding algorithms (DFS, BFS, UCS, A\*).

This project uses various search algorithms—Depth First Search (DFS), Breadth First Search (BFS), Uniform Cost Search (UCS), and A\*—to find solutions for each level. Players can select a level and the algorithm to solve the puzzle. The interface is built with Pygame, providing a fun and interactive experience for exploring pathfinding algorithms in action.

# SOKOBAN INTRODUCTION

Sokoban is a puzzle video game genre in which the player pushes crates or boxes around in a warehouse, trying to get them to some goal locations.The game is played on a board of squares, where each square is a floor or a wall. Some floor squares contain boxes, and some floor squares are marked as goal locations.

The player is confined to the board and may move horizontally or vertically onto empty squares (never through walls or boxes). The player can move a box by walking up to it and push it to the square in front. Boxes cannot be pulled, and they cannot be pushed to squares with walls or other boxes. The number of boxes equals the number of storage locations. The puzzle is solved when all boxes are placed at storage locations.

<div align="center">
<img src="themes/images/screenshot.png" align="center"/>
</div>

# Authors

**Quach Thanh Kiet - Vo Ha Lam - Huynh Gia Khanh - Nguyen Tan Dong**

# Lasted Version

1.1.0

# Features

- Interactive GUI built with **Pygame**
- **AI Pathfinding Algorithms:**
  - Depth First Search (DFS)
  - Breadth First Search (BFS)
  - Uniform Cost Search (UCS)
  - A* Search (A*)
- Level selection and algorithm choice for solving levels
- Console-based testing for unit validation

# Requirements

- **Python 3.12** or higher
- **Pip 24.3.1** or higher

# Installation

**Install Dependencies**

```sh
$ pip install -r requirements.txt
```

# Usage

## Run test algorithm

```sh
$ python runmain.py
```

This command will start the main script, `runmain.py`, to compare the effectiveness of different algorithms in solving mazes. Running this test helps you observe and analyze how each algorithm approaches maze-solving, highlighting their strengths and weaknesses in various scenarios.
**Purpose:**

- This command is specifically aimed at showcasing the _differences in efficiency_ and _problem-solving approaches_ among the algorithms.
- It allows you to see variations in _speed_, _path optimization_, and _computational resource_ usage for each algorithm.

The output will be created, <a href="output/"> here </a>
To see the result, [click here](output/).

## Run game

### Step 1: Launching the game

```sh
$ python main.py
```

# Contributing

Guidelines for contributing to the project.

## License

Information about the project's license.
