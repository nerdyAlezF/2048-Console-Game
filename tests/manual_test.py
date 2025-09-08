import sys
import os

# Add parent directory to path to import game module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game2048 import Game2048

# Test basic initialization and display
game = Game2048()
print("Testing Game2048 initialization:")
game.display_game()

print(f"\nBoard has {game.get_board_size()}x{game.get_board_size()} dimensions")
print(f"Initial score: {game.get_score()}")

# Count non-zero tiles (should be 2)
non_zero_count = 0
for i in range(game.get_board_size()):
    for j in range(game.get_board_size()):
        if game._board.get_cell(i, j) != 0:
            non_zero_count += 1

print(f"Number of initial tiles: {non_zero_count} (should be 2)")

# Test some movements
print("\nTesting movement:")
moved = game.move_left()
print(f"Move left result: {'Success' if moved else 'No movement'}")
game.display_game()

print(f"\nScore after move: {game.get_score()}")

# Test game state methods
print(f"Has won: {game.has_won()}")
print(f"Game over: {game.is_game_over()}")

print("\nManual test completed successfully!")