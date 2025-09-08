import unittest
import sys
import os

# Add parent directory to path to import game module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.movement_engine import MovementEngine
from game.board import Board


class TestHelperMethods(unittest.TestCase):
    """Test internal helper methods for movement logic."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.movement_engine = MovementEngine(4)
    
    def test_compress_row_left(self):
        """Test row compression helper method."""
        # Test with zeros in between
        row = [2, 0, 4, 0]
        expected = [2, 4, 0, 0]
        result = self.movement_engine.compress_row_left(row)
        self.assertEqual(result, expected)
        
        # Test with all zeros
        row = [0, 0, 0, 0]
        expected = [0, 0, 0, 0]
        result = self.movement_engine.compress_row_left(row)
        self.assertEqual(result, expected)
        
        # Test with no zeros
        row = [2, 4, 8, 16]
        expected = [2, 4, 8, 16]
        result = self.movement_engine.compress_row_left(row)
        self.assertEqual(result, expected)
    
    def test_merge_row_left(self):
        """Test row merging helper method."""
        # Test simple merge
        row = [2, 2, 4, 4]
        expected_row = [4, 0, 8, 0]
        expected_score = 12
        result_row, result_score = self.movement_engine.merge_row_left(row)
        self.assertEqual(result_row, expected_row)
        self.assertEqual(result_score, expected_score)
        
        # Test no merge possible
        row = [2, 4, 8, 16]
        expected_row = [2, 4, 8, 16]
        expected_score = 0
        result_row, result_score = self.movement_engine.merge_row_left(row)
        self.assertEqual(result_row, expected_row)
        self.assertEqual(result_score, expected_score)
        
        # Test merge with zeros
        row = [2, 2, 0, 0]
        expected_row = [4, 0, 0, 0]
        expected_score = 4
        result_row, result_score = self.movement_engine.merge_row_left(row)
        self.assertEqual(result_row, expected_row)
        self.assertEqual(result_score, expected_score)
    
    def test_process_row_left(self):
        """Test complete row processing (compress-merge-compress)."""
        # Test complex scenario
        row = [2, 0, 2, 4]
        expected_row = [4, 4, 0, 0]
        expected_score = 4
        expected_moved = True
        
        result_row, result_score, moved = self.movement_engine.process_row_left(row)
        self.assertEqual(result_row, expected_row)
        self.assertEqual(result_score, expected_score)
        self.assertEqual(moved, expected_moved)
        
        # Test no movement
        row = [2, 4, 8, 16]
        expected_row = [2, 4, 8, 16]
        expected_score = 0
        expected_moved = False
        
        result_row, result_score, moved = self.movement_engine.process_row_left(row)
        self.assertEqual(result_row, expected_row)
        self.assertEqual(result_score, expected_score)
        self.assertEqual(moved, expected_moved)


class TestBoardOperations(unittest.TestCase):
    """Test Board class operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.board = Board(4)
    
    def test_board_initialization(self):
        """Test board initializes correctly."""
        self.assertEqual(self.board.size, 4)
        # All cells should be empty initially
        for i in range(4):
            for j in range(4):
                self.assertEqual(self.board.get_cell(i, j), 0)
    
    def test_set_and_get_cell(self):
        """Test setting and getting cell values."""
        self.board.set_cell(1, 2, 4)
        self.assertEqual(self.board.get_cell(1, 2), 4)
        
        self.board.set_cell(0, 0, 2)
        self.assertEqual(self.board.get_cell(0, 0), 2)
    
    def test_get_empty_cells(self):
        """Test getting empty cell positions."""
        # Initially all cells should be empty
        empty_cells = self.board.get_empty_cells()
        self.assertEqual(len(empty_cells), 16)
        
        # Add a tile and check
        self.board.set_cell(1, 1, 2)
        empty_cells = self.board.get_empty_cells()
        self.assertEqual(len(empty_cells), 15)
        self.assertNotIn((1, 1), empty_cells)
    
    def test_is_full(self):
        """Test checking if board is full."""
        self.assertFalse(self.board.is_full())
        
        # Fill the board
        for i in range(4):
            for j in range(4):
                self.board.set_cell(i, j, 2)
        
        self.assertTrue(self.board.is_full())
    
    def test_board_copy(self):
        """Test board copying."""
        self.board.set_cell(0, 0, 4)
        self.board.set_cell(2, 3, 8)
        
        copied_board = self.board.copy()
        
        self.assertEqual(copied_board.get_cell(0, 0), 4)
        self.assertEqual(copied_board.get_cell(2, 3), 8)
        
        # Verify it's a deep copy
        self.board.set_cell(0, 0, 16)
        self.assertEqual(copied_board.get_cell(0, 0), 4)  # Should not change
    
    def test_import_state_2d_list(self):
        """Test importing board state from 2D list."""
        state = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 0, 2],
            [4, 8, 16, 32]
        ]
        
        self.board.import_state(state)
        
        # Verify import worked correctly
        for i in range(4):
            for j in range(4):
                self.assertEqual(self.board.get_cell(i, j), state[i][j])
    
    def test_import_state_flat_list(self):
        """Test importing board state from flat list."""
        # Flat list: row-major order
        state = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 0, 2, 4, 8, 16, 32]
        
        self.board.import_state(state)
        
        # Verify import worked correctly
        expected = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 0, 2],
            [4, 8, 16, 32]
        ]
        
        for i in range(4):
            for j in range(4):
                self.assertEqual(self.board.get_cell(i, j), expected[i][j])
    
    def test_export_state_2d(self):
        """Test exporting board state as 2D list."""
        # Set up known state
        expected = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 0, 2],
            [4, 8, 16, 32]
        ]
        
        for i in range(4):
            for j in range(4):
                self.board.set_cell(i, j, expected[i][j])
        
        # Export and verify
        exported = self.board.export_state()
        self.assertEqual(exported, expected)
    
    
    def test_import_state_invalid_2d_size(self):
        """Test error handling for invalid 2D import size."""
        # Wrong dimensions
        invalid_state = [
            [2, 4, 8],  # Only 3 columns
            [32, 64, 128],
            [512, 1024, 0]
        ]
        
        with self.assertRaises(ValueError):
            self.board.import_state(invalid_state)
    
    def test_import_state_invalid_flat_size(self):
        """Test error handling for invalid flat import size."""
        # Wrong number of elements (should be 16 for 4x4)
        invalid_state = [2, 4, 8, 16, 32, 64, 128, 256, 512]  # Only 9 elements
        
        with self.assertRaises(ValueError):
            self.board.import_state(invalid_state)


if __name__ == '__main__':
    unittest.main()