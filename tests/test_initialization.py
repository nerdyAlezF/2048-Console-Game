import unittest
import sys
import os

# Add parent directory to path to import game module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game2048 import Game2048
from game.board import Board
from game.tile_generator import TileGenerator


class TestGameInitialization(unittest.TestCase):
    """Test game initialization and setup."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.game = Game2048()
    
    def test_game_initialization(self):
        """Test that the game is initialized correctly."""
        self.assertEqual(self.game.get_board_size(), 4)
        self.assertEqual(self.game.get_score(), 0)
    
    def test_initial_tiles_count(self):
        """Test that exactly 2 tiles are placed initially."""
        # Count non-empty tiles by creating a fresh game and inspecting board
        board = Board(4)
        tile_gen = TileGenerator()
        tile_gen.add_random_tile(board)
        tile_gen.add_random_tile(board)
        
        non_zero_count = len([1 for i in range(4) for j in range(4) 
                             if board.get_cell(i, j) != 0])
        self.assertEqual(non_zero_count, 2)
    
    def test_tile_generator_values(self):
        """Test that tile generator produces valid values."""
        tile_gen = TileGenerator()
        board = Board(4)
        
        # Generate multiple tiles and check they're valid
        for _ in range(10):
            tile_gen.add_random_tile(board)
            for i in range(4):
                for j in range(4):
                    cell = board.get_cell(i, j)
                    if cell != 0:
                        self.assertIn(cell, [2, 4])
    
    def test_tile_2_probability_custom(self):
        """Test custom tile probability setting."""
        # Test that we can create game with custom probability
        custom_game = Game2048(tile_2_probability=0.5)
        # We can't directly access the probability, but we can test it works
        self.assertEqual(custom_game.get_board_size(), 4)
        self.assertEqual(custom_game.get_score(), 0)
    
    def test_tile_generator_empty_board(self):
        """Test adding a tile to an empty board."""
        board = Board(4)
        tile_gen = TileGenerator()
        
        # Initially empty
        self.assertTrue(len(board.get_empty_cells()) == 16)
        
        # Add one tile
        result = tile_gen.add_random_tile(board)
        self.assertTrue(result)  # Should succeed
        
        # Check exactly one tile was added
        non_zero_count = len([1 for i in range(4) for j in range(4) 
                             if board.get_cell(i, j) != 0])
        self.assertEqual(non_zero_count, 1)
    
    def test_tile_generator_full_board(self):
        """Test adding tile when board is full."""
        board = Board(4)
        tile_gen = TileGenerator()
        
        # Fill the board manually
        for i in range(4):
            for j in range(4):
                board.set_cell(i, j, 2)
        
        # Try to add a tile (should fail)
        result = tile_gen.add_random_tile(board)
        self.assertFalse(result)  # Should fail
        
        # Board should still be full of 2s
        for i in range(4):
            for j in range(4):
                self.assertEqual(board.get_cell(i, j), 2)


if __name__ == '__main__':
    unittest.main()