import unittest
import sys
import os

# Add parent directory to path to import game module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game2048 import Game2048


class TestIntegration(unittest.TestCase):
    """Integration tests using predefined board states."""
    
    def test_simple_merge_left(self):
        """Test left merge with known board state."""
        # Setup: Two 2s in the first row that should merge
        board_state = [
            [2, 2, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        
        game = Game2048.from_state(board_state, score=0)
        
        # Perform left move
        moved = game.move_left()
        
        # Verify results
        self.assertTrue(moved)
        self.assertEqual(game.get_score(), 4)  # 2+2=4 points
        
        # Check resulting board (4 should be in position [0,0], new tile added somewhere)
        self.assertEqual(game._board.get_cell(0, 0), 4)
        
        # Should have exactly 2 non-zero tiles (the merged 4 + 1 new random tile)
        non_zero_count = sum(1 for i in range(4) for j in range(4) 
                           if game._board.get_cell(i, j) != 0)
        self.assertEqual(non_zero_count, 2)
    
    def test_no_merge_possible(self):
        """Test move when no merge is possible."""
        # Setup: Alternating pattern where no merges are possible
        board_state = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]
        
        game = Game2048.from_state(board_state, score=100)
        
        # Try all moves - none should be possible
        self.assertFalse(game.move_left())
        self.assertFalse(game.move_right())
        self.assertFalse(game.move_up())
        self.assertFalse(game.move_down())
        
        # Score should remain unchanged
        self.assertEqual(game.get_score(), 100)
        
        # Game should be over
        self.assertTrue(game.is_game_over())
    
    def test_multiple_merges_in_row(self):
        """Test multiple merges in a single row."""
        # Setup: Four 2s in first row
        board_state = [
            [2, 2, 2, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        
        game = Game2048.from_state(board_state, score=0)
        
        # Perform left move
        moved = game.move_left()
        
        # Verify results
        self.assertTrue(moved)
        self.assertEqual(game.get_score(), 8)  # Two merges: 4+4 = 8 points
        
        # Check resulting board: should have [4, 4, 0, 0] + one new tile
        self.assertEqual(game._board.get_cell(0, 0), 4)
        self.assertEqual(game._board.get_cell(0, 1), 4)
        self.assertEqual(game._board.get_cell(0, 2), 0)
        self.assertEqual(game._board.get_cell(0, 3), 0)
    
    def test_win_condition_detection(self):
        """Test win condition with specific board setup."""
        # Setup: Almost winning state - one move away from 2048
        board_state = [
            [1024, 1024, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        
        game = Game2048.from_state(board_state, score=2000)
        
        # Should not have won yet
        self.assertFalse(game.has_won())
        
        # Perform left move to create 2048
        moved = game.move_left()
        
        # Verify win condition
        self.assertTrue(moved)
        self.assertTrue(game.has_won())
        self.assertEqual(game.get_score(), 4048)  # 2000 + 2048 from merge
        
        # Verify 2048 tile exists
        self.assertEqual(game._board.get_cell(0, 0), 2048)
    
    def test_game_over_detection_specific(self):
        """Test game over detection with specific full board."""
        # Setup: Full board with no possible merges
        board_state = [
            [2, 4, 8, 16],
            [4, 8, 16, 32],
            [8, 16, 32, 64],
            [16, 32, 64, 128]
        ]
        
        game = Game2048.from_state(board_state, score=1000)
        
        # Should be game over
        self.assertTrue(game.is_game_over())
        self.assertFalse(game.has_won())
        
        # No moves should be possible
        self.assertFalse(game.move_left())
        self.assertFalse(game.move_right())
        self.assertFalse(game.move_up())
        self.assertFalse(game.move_down())
    
    def test_game_continues_with_possible_merges(self):
        """Test that game continues when merges are possible on full board."""
        # Setup: Full board but with possible merges
        board_state = [
            [2, 2, 4, 8],
            [4, 8, 16, 32],
            [8, 16, 32, 64],
            [16, 32, 64, 128]
        ]
        
        game = Game2048.from_state(board_state, score=500)
        
        # Should NOT be game over (first row has mergeable tiles)
        self.assertFalse(game.is_game_over())
        
        # Left move should be possible
        self.assertTrue(game.move_left())
        
        # After move, should have [4, 4, 8, 0] in first row + score increase
        self.assertEqual(game._board.get_cell(0, 0), 4)
        self.assertEqual(game._board.get_cell(0, 1), 4)
        self.assertEqual(game._board.get_cell(0, 2), 8)
        self.assertEqual(game.get_score(), 504)  # 500 + 4 from merge
    
    def test_transpose_movement_up(self):
        """Test upward movement using specific board state."""
        # Setup: Tiles that should merge upward
        board_state = [
            [2, 0, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        
        game = Game2048.from_state(board_state, score=0)
        
        # Perform up move
        moved = game.move_up()
        
        # Verify results
        self.assertTrue(moved)
        self.assertEqual(game.get_score(), 4)  # 2+2=4 points
        
        # Check resulting board: merged tile should be at [0,0]
        self.assertEqual(game._board.get_cell(0, 0), 4)
        # Note: A new random tile will be added after the move, so check tile count instead
        non_zero_count = sum(1 for i in range(4) for j in range(4) 
                           if game._board.get_cell(i, j) != 0)
        self.assertEqual(non_zero_count, 2)  # merged tile + 1 new tile
    
    def test_reverse_movement_right(self):
        """Test rightward movement using specific board state."""
        # Setup: Tiles that should merge rightward
        board_state = [
            [0, 0, 2, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        
        game = Game2048.from_state(board_state, score=0)
        
        # Perform right move
        moved = game.move_right()
        
        # Verify results
        self.assertTrue(moved)
        self.assertEqual(game.get_score(), 4)  # 2+2=4 points
        
        # Check resulting board: merged tile should be at [0,3]
        self.assertEqual(game._board.get_cell(0, 3), 4)
        # Note: A new random tile will be added after the move, so check tile count instead
        non_zero_count = sum(1 for i in range(4) for j in range(4) 
                           if game._board.get_cell(i, j) != 0)
        self.assertEqual(non_zero_count, 2)  # merged tile + 1 new tile
    
    def test_complex_scoring_scenario(self):
        """Test complex scoring with multiple merges."""
        # Setup: Board with multiple mergeable tiles
        board_state = [
            [2, 2, 4, 4],
            [8, 8, 16, 16],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        
        game = Game2048.from_state(board_state, score=100)
        
        # Perform left move
        moved = game.move_left()
        
        # Verify results
        self.assertTrue(moved)
        # Score: 100 + 4 (2+2) + 8 (4+4) + 16 (8+8) + 32 (16+16) = 160
        self.assertEqual(game.get_score(), 160)
        
        # Check resulting board
        self.assertEqual(game._board.get_cell(0, 0), 4)
        self.assertEqual(game._board.get_cell(0, 1), 8)
        self.assertEqual(game._board.get_cell(1, 0), 16)
        self.assertEqual(game._board.get_cell(1, 1), 32)
    
    def test_board_export_import_consistency(self):
        """Test that board export/import maintains consistency."""
        # Original board state
        original_state = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 0, 2],
            [4, 8, 16, 32]
        ]
        
        # Create game with this state
        game = Game2048.from_state(original_state, score=5000)
        
        # Export the state
        exported_state, exported_score = game.export_board_state()
        
        # Verify export matches original
        self.assertEqual(exported_state, original_state)
        self.assertEqual(exported_score, 5000)
        
        # Create new game from exported state
        new_game = Game2048.from_state(exported_state, exported_score)
        
        # Verify consistency
        self.assertEqual(new_game.get_score(), 5000)
        for i in range(4):
            for j in range(4):
                self.assertEqual(
                    new_game._board.get_cell(i, j),
                    original_state[i][j]
                )
    
    def test_restart_from_custom_state(self):
        """Test restart functionality from custom state."""
        # Setup complex board
        complex_state = [
            [1024, 512, 256, 128],
            [64, 32, 16, 8],
            [4, 2, 4, 2],
            [8, 16, 32, 64]
        ]
        
        game = Game2048.from_state(complex_state, score=10000)
        
        # Verify initial state
        self.assertEqual(game.get_score(), 10000)
        self.assertEqual(game._board.get_cell(0, 0), 1024)
        
        # Restart game
        game.restart_game()
        
        # Verify restart worked
        self.assertEqual(game.get_score(), 0)
        
        # Should have exactly 2 tiles after restart
        non_zero_count = sum(1 for i in range(4) for j in range(4) 
                           if game._board.get_cell(i, j) != 0)
        self.assertEqual(non_zero_count, 2)
        
        # All tiles should be 2 or 4
        for i in range(4):
            for j in range(4):
                value = game._board.get_cell(i, j)
                if value != 0:
                    self.assertIn(value, [2, 4])
    
    def test_transpose_movement_down(self):
        """Test downward movement using specific board state."""
        # Setup: Tiles that should merge downward
        board_state = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 0, 0, 0],
            [2, 0, 0, 0]
        ]
        
        game = Game2048.from_state(board_state, score=0)
        
        # Perform down move
        moved = game.move_down()
        
        # Verify results
        self.assertTrue(moved)
        self.assertEqual(game.get_score(), 4)  # 2+2=4 points
        
        # Check resulting board: merged tile should be at [3,0]
        self.assertEqual(game._board.get_cell(3, 0), 4)
        # Note: A new random tile will be added after the move, so check tile count instead
        non_zero_count = sum(1 for i in range(4) for j in range(4) 
                           if game._board.get_cell(i, j) != 0)
        self.assertEqual(non_zero_count, 2)  # merged tile + 1 new tile
    
    def test_compression_without_merging(self):
        """Test tile compression scenarios where tiles slide but don't merge."""
        # Setup: Tiles that should compress but not merge (different values)
        board_state = [
            [0, 2, 0, 4],
            [8, 0, 16, 0],
            [0, 0, 32, 0],
            [0, 64, 0, 128]
        ]
        
        game = Game2048.from_state(board_state, score=50)
        
        # Perform left move - should compress but no merges
        moved = game.move_left()
        
        # Verify results
        self.assertTrue(moved)
        self.assertEqual(game.get_score(), 50)  # No score change (no merges)
        
        # Check key positions after compression to left
        # Row 0: 2 and 4 should be compressed to leftmost positions
        self.assertEqual(game._board.get_cell(0, 0), 2)
        self.assertEqual(game._board.get_cell(0, 1), 4)
        
        # Row 1: 8 and 16 should be compressed to leftmost positions
        self.assertEqual(game._board.get_cell(1, 0), 8)
        self.assertEqual(game._board.get_cell(1, 1), 16)
        
        # Row 2: 32 should be compressed to leftmost position
        self.assertEqual(game._board.get_cell(2, 0), 32)
        
        # Row 3: 64 and 128 should be compressed to leftmost positions
        self.assertEqual(game._board.get_cell(3, 0), 64)
        self.assertEqual(game._board.get_cell(3, 1), 128)
        
        # Note: A random tile is added after movement, so we don't check empty positions
        
        # Original board had 7 tiles (2,4,8,16,32,64,128)
        # After move: 7 original + 1 new random tile = 8 total
        non_zero_count = sum(1 for i in range(4) for j in range(4) 
                           if game._board.get_cell(i, j) != 0)
        self.assertEqual(non_zero_count, 8)  # 7 original + 1 new random
    
    def test_partial_compression_scenarios(self):
        """Test various compression scenarios including gaps and partial fills."""
        # Setup: Board with gaps that will compress differently in each direction
        board_state = [
            [0, 0, 0, 2],  # Should compress to [2, 0, 0, 0] left, stay [0, 0, 0, 2] right
            [4, 0, 0, 8],  # Should compress to [4, 8, 0, 0] left, [0, 0, 4, 8] right
            [0, 16, 0, 32], # Should compress to [16, 32, 0, 0] left, [0, 0, 16, 32] right
            [0, 0, 0, 0]   # Empty row
        ]
        
        # Test left compression
        game_left = Game2048.from_state(board_state, score=0)
        moved_left = game_left.move_left()
        
        self.assertTrue(moved_left)
        self.assertEqual(game_left.get_score(), 0)  # No merges, just compression
        
        # Verify left compression results
        self.assertEqual(game_left._board.get_cell(0, 0), 2)
        self.assertEqual(game_left._board.get_cell(1, 0), 4)
        self.assertEqual(game_left._board.get_cell(1, 1), 8)
        self.assertEqual(game_left._board.get_cell(2, 0), 16)
        self.assertEqual(game_left._board.get_cell(2, 1), 32)
        
        # Test right compression
        game_right = Game2048.from_state(board_state, score=0)
        moved_right = game_right.move_right()
        
        self.assertTrue(moved_right)
        self.assertEqual(game_right.get_score(), 0)  # No merges, just compression
        
        # Verify right compression results
        self.assertEqual(game_right._board.get_cell(0, 3), 2)
        self.assertEqual(game_right._board.get_cell(1, 2), 4)
        self.assertEqual(game_right._board.get_cell(1, 3), 8)
        self.assertEqual(game_right._board.get_cell(2, 2), 16)
        self.assertEqual(game_right._board.get_cell(2, 3), 32)
        
        # Test up compression
        game_up = Game2048.from_state(board_state, score=0)
        moved_up = game_up.move_up()
        
        self.assertTrue(moved_up)
        self.assertEqual(game_up.get_score(), 0)  # No merges, just compression
        
        # Verify up compression results - tiles should move up to fill gaps
        # Column 1: 4 and 16 should compress up
        self.assertEqual(game_up._board.get_cell(0, 1), 16)  # 16 moves to top
        
        # Test down compression  
        game_down = Game2048.from_state(board_state, score=0)
        moved_down = game_down.move_down()
        
        self.assertTrue(moved_down)
        self.assertEqual(game_down.get_score(), 0)  # No merges, just compression
        
        # Verify down compression results - tiles should move down to fill gaps
        # The 16 from column 1 should move to bottom row
        self.assertEqual(game_down._board.get_cell(3, 1), 16)  # 16 at bottom
        # Note: Random tile generation affects the exact layout, so just verify key positions


if __name__ == '__main__':
    unittest.main()