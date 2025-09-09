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
- Board import/export for testing or debugging
- AI move suggestion system with intelligent heuristics & Claude API
- Modular structure with comprehensive unit tests
- Written Integration Test


## AI System (Offline Heuristic Model)
AI assistant that analyzes the board state and suggests optimal moves using board heuristics:
- Empty tile counting (more empty tiles = better position)
- Monotonicity scoring (ascending sequences preferred)
- Max-tile corner bonus

Press **H** during gameplay to get AI move suggestions.

## Claude AI Integration (Optional)
For advanced AI suggestions using Claude's reasoning capabilities:

### Setup
```bash
# Install dependency
pip install anthropic

# Set your API key
export ANTHROPIC_API_KEY=your_key_here
```

### Usage
- Press **C** during gameplay for Claude AI suggestions

### Remarks
- Since I wasn't able to obtain a valid API key from Anthropic, the API call functionality wasn't tested yet.

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
- **H** - Get AI Hint (heuristic model)
- **C** - Get Claude AI Hint (requires API key)
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
python3 -m unittest tests.test_main -v            # CLI and game loop tests
python3 -m unittest tests.test_game_ai -v         # AI suggestion system tests
python3 -m unittest tests.test_movement -v        # Tile movement logic tests
python3 -m unittest tests.test_initialization -v  # Game setup tests
python3 -m unittest tests.test_helper_methods -v  # Board operations tests
python3 -m unittest tests.test_integration -v     # Integration tests
```

---

## Test Coverage
Achieved overall 97% code coverage using [`coverage.py`](https://coverage.readthedocs.io/).

To analyze test coverage and ensure code quality:

### Install Coverage Tool
```bash
pip install coverage
```

#### Run Tests with Coverage Analysis
```bash
coverage run -m unittest tests.test_game2048
```

### Generate Coverage Report

#### Terminal report (excludes test files from analysis)
```bash
coverage report --omit="tests/*"
```

#### Detailed HTML report
```bash
coverage html --omit="tests/*"
```

---

## Optional Future Enhancements
- Backtest and fine tune the Heuristic Model
- Integrate with Claude AI model for more advanced hints once there is a valid API key.
- Support for larger board sizes, different scoring variants
- Undo functionality
- Further improve the integration test

---

## License

This project is licensed under the MIT License - see the (LICENSE) file for details.

---

## Author
Alex Fong