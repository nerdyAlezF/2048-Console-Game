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
- Modular structure with comprehensive unit tests
- Written Integration Test

---

## Requirements
- Python 3.6 or higher

---

## How to Run the Game

```bash
python main.py
```

---

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