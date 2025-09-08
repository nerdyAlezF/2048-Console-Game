# 2048 Console Game (Python)

A lightweight, console-based version of the classic **2048 game**, built in Python.  
This implementation focuses on clean architecture, testability, and correctness — developed as a personal side project.

---

## Features
- 4×4 board with random tile initialization (2 or 4)
- Full move support: up, down, left, right
- Proper tile merging logic (merge-once-per-move)
- Accurate score tracking
- Game-over detection when no valid moves remain
- Console-based user interface
- Board import and export
- AI move suggestion system with intelligent heuristics
- Modular structure with comprehensive unit tests
- Written Integration Test


## AI System
The game includes an intelligent AI assistant that analyzes the board state and suggests
optimal moves using:
- Empty tile counting (more empty tiles = better position)
- Monotonicity scoring (ascending sequences preferred)
- Corner positioning bonus (largest tile in corner = strategic advantage)

Press **H** during gameplay to get AI move suggestions.

---

## Requirements
- Python 3.6 or higher

---

## How to Run the Game

```bash
python main.py
```

---

## Game Controls
- **W** - Move Up
- **A** - Move Left
- **S** - Move Down
- **D** - Move Right
- **H** - Get AI Hint (move suggestion)
- **R** - Restart Game
- **Q** - Quit Game

--

## Running Tests

Main test suite (all tests):

```bash
python3 -m unittest tests.test_game2048 -v
```

Individual test modules:

```bash
python3 -m unittest tests.test_initialization -v
python3 -m unittest tests.test_movement -v
python3 -m unittest tests.test_main -v
python3 -m unittest tests.test_game_ai -v
python3 -m unittest tests.test_helper_methods -v
```

Run integration tests:
```bash
python3 -m unittest tests.test_integration -v
```

---

## License

This project is licensed under the MIT License - see the (LICENSE) file for details.

---

## Author
Alex Fong