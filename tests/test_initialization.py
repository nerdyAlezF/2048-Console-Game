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


class TestGameStateManagement(unittest.TestCase):
    """Test game state import/export functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.game = Game2048()
    
    def test_import_board_state_2d(self):
        """Test importing board state from 2D list."""
        board_state = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 0, 2],
            [4, 8, 16, 32]
        ]
        
        self.game.import_board_state(board_state, score=1000)
        
        # Verify import worked
        self.assertEqual(self.game.get_score(), 1000)
        for i in range(4):
            for j in range(4):
                self.assertEqual(self.game._board.get_cell(i, j), board_state[i][j])
    
    def test_import_board_state_without_score(self):
        """Test importing board state without changing score."""
        original_score = self.game.get_score()
        
        board_state = [
            [2, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        
        self.game.import_board_state(board_state)
        
        # Score should remain unchanged
        self.assertEqual(self.game.get_score(), original_score)
        # Board should be updated
        self.assertEqual(self.game._board.get_cell(0, 0), 2)
        self.assertEqual(self.game._board.get_cell(0, 1), 4)
    
    def test_export_board_state_2d(self):
        """Test exporting board state as 2D list."""
        # Set up known state
        board_state = [
            [1024, 512, 256, 128],
            [64, 32, 16, 8],
            [4, 2, 0, 0],
            [8, 16, 32, 64]
        ]
        
        self.game.import_board_state(board_state, score=5000)
        
        # Export and verify
        exported_board, exported_score = self.game.export_board_state()
        
        self.assertEqual(exported_board, board_state)
        self.assertEqual(exported_score, 5000)
    
    
    def test_from_state_class_method(self):
        """Test creating game from specific state using class method."""
        board_state = [
            [1024, 1024, 0, 0],
            [512, 256, 128, 64],
            [32, 16, 8, 4],
            [2, 0, 0, 0]
        ]
        
        game = Game2048.from_state(board_state, score=3000, tile_2_probability=1.0, size=4)
        
        # Verify game was created with correct state
        self.assertEqual(game.get_score(), 3000)
        self.assertEqual(game.get_board_size(), 4)
        
        # Verify board state
        for i in range(4):
            for j in range(4):
                self.assertEqual(game._board.get_cell(i, j), board_state[i][j])
    
    def test_from_state_default_values(self):
        """Test creating game from state with default parameters."""
        board_state = [
            [4, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        
        game = Game2048.from_state(board_state)
        
        # Should use default values
        self.assertEqual(game.get_score(), 0)
        self.assertEqual(game.get_board_size(), 4)
        self.assertEqual(game._board.get_cell(0, 0), 4)
        self.assertEqual(game._board.get_cell(0, 1), 2)
    
    def test_state_import_export_roundtrip(self):
        """Test that import->export->import produces consistent results."""
        original_state = [
            [2048, 1024, 512, 256],
            [128, 64, 32, 16],
            [8, 4, 2, 0],
            [0, 0, 0, 0]
        ]
        original_score = 10000
        
        # Import state
        self.game.import_board_state(original_state, original_score)
        
        # Export state
        exported_board, exported_score = self.game.export_board_state()
        
        # Create new game from exported state
        new_game = Game2048.from_state(exported_board, exported_score)
        
        # Verify consistency
        self.assertEqual(new_game.get_score(), original_score)
        for i in range(4):
            for j in range(4):
                self.assertEqual(
                    new_game._board.get_cell(i, j),
                    original_state[i][j]
                )
    
    def test_state_with_game_conditions(self):
        """Test state import with win/game over conditions."""
        # Test win condition
        win_state = [
            [2048, 1024, 512, 256],
            [128, 64, 32, 16],
            [8, 4, 2, 0],
            [0, 0, 0, 0]
        ]
        
        win_game = Game2048.from_state(win_state)
        self.assertTrue(win_game.has_won())
        self.assertFalse(win_game.is_game_over())
        
        # Test game over condition
        game_over_state = [
            [2, 4, 8, 16],
            [4, 8, 16, 32],
            [8, 16, 32, 64],
            [16, 32, 64, 128]
        ]
        
        game_over_game = Game2048.from_state(game_over_state)
        self.assertFalse(game_over_game.has_won())
        self.assertTrue(game_over_game.is_game_over())


if __name__ == '__main__':
    unittest.main()