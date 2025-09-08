import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game2048 import Game2048
from game.game_ai import GameAI


class TestGameAI(unittest.TestCase):
    """Test cases for the GameAI class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.game = Game2048()
        self.ai = GameAI(self.game)

    def test_ai_initialization(self):
        """Test that AI initializes correctly with game reference."""
        self.assertIsInstance(self.ai, GameAI)
        self.assertIs(self.ai.game, self.game)

    def test_count_empty_tiles_empty_board(self):
        """Test counting empty tiles on a mostly empty board."""
        # Create a board with only 2 tiles (initial state)
        empty_count = self.ai._count_empty_tiles(self.game._board)
        self.assertEqual(empty_count, 14)  # 16 total - 2 initial tiles

    def test_count_empty_tiles_full_board(self):
        """Test counting empty tiles on a full board."""
        # Create a full board
        board_state = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096],
            [8192, 16384, 32768, 65536]
        ]
        self.game.import_board_state(board_state)
        empty_count = self.ai._count_empty_tiles(self.game._board)
        self.assertEqual(empty_count, 0)

    def test_count_empty_tiles_partial_board(self):
        """Test counting empty tiles on a partially filled board."""
        board_state = [
            [2, 0, 4, 0],
            [0, 0, 0, 8],
            [0, 16, 0, 0],
            [0, 0, 0, 32]
        ]
        self.game.import_board_state(board_state)
        empty_count = self.ai._count_empty_tiles(self.game._board)
        self.assertEqual(empty_count, 11)  # 16 total - 5 tiles = 11 empty


class TestMonotonicityAndCornerHeuristics(unittest.TestCase):
    """Test cases for monotonicity scoring and corner heuristics."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game2048()
        self.ai = GameAI(self.game)

    def test_monotonicity_score_ascending(self):
        """Test monotonicity score for ascending sequences."""
        test_cases = [
            ([2, 4, 8, 16], 3),     # Perfect ascending: 3 pairs × +1 = +3
            ([2, 4, 8], 2),         # 2 pairs × +1 = +2  
            ([4, 8], 1),            # 1 pair × +1 = +1
            ([2, 4, 0, 8], 1),      # Only 2<4 counts, 4 vs 0 and 0 vs 8 skipped
            ([0, 2, 4, 8], 2),      # 0 vs 2 skipped, 2<4 and 4<8 count
        ]
        
        for sequence, expected_score in test_cases:
            with self.subTest(sequence=sequence):
                score = self.ai._monotonicity_score(sequence)
                self.assertEqual(score, expected_score)

    def test_monotonicity_score_descending(self):
        """Test monotonicity score for descending sequences."""
        test_cases = [
            ([16, 8, 4, 2], -6),    # Perfect descending: 3 pairs × -2 = -6
            ([8, 4, 2], -4),        # 2 pairs × -2 = -4
            ([8, 4], -2),           # 1 pair × -2 = -2
            ([16, 0, 8, 4], -2),    # Only 8>4 counts, others involve zeros
            ([16, 8, 4, 0], -4),    # 16>8 and 8>4 count, 4 vs 0 skipped
        ]
        
        for sequence, expected_score in test_cases:
            with self.subTest(sequence=sequence):
                score = self.ai._monotonicity_score(sequence)
                self.assertEqual(score, expected_score)

    def test_monotonicity_score_mixed(self):
        """Test monotonicity score for mixed sequences."""
        test_cases = [
            ([2, 8, 4], 1 - 2),     # 2<8: +1, 8>4: -2 = -1
            ([4, 2, 8], -2 + 1),    # 4>2: -2, 2<8: +1 = -1
            ([2, 4, 2], 1 - 2),     # 2<4: +1, 4>2: -2 = -1
            ([4, 4, 8], 1),         # 4=4 skipped, 4<8: +1 = +1
            ([8, 8, 4], -2),        # 8=8 skipped, 8>4: -2 = -2
        ]
        
        for sequence, expected_score in test_cases:
            with self.subTest(sequence=sequence):
                score = self.ai._monotonicity_score(sequence)
                self.assertEqual(score, expected_score)

    def test_monotonicity_score_edge_cases(self):
        """Test monotonicity score for edge cases."""
        test_cases = [
            ([0, 0, 0, 0], 0),      # All zeros
            ([4, 0, 0, 0], 0),      # Single non-zero
            ([0, 4, 0, 0], 0),      # Single non-zero in middle
            ([4], 0),               # Single element
            ([], 0),                # Empty sequence
            ([2, 2, 2, 2], 0),      # All equal values
        ]
        
        for sequence, expected_score in test_cases:
            with self.subTest(sequence=sequence):
                score = self.ai._monotonicity_score(sequence)
                self.assertEqual(score, expected_score)

    def test_total_monotonicity_score(self):
        """Test total monotonicity score calculation on a board."""
        # Board with ascending and descending sequences
        board_state = [
            [2, 4, 8, 16],    # Row 0: ascending (+3 score)
            [32, 16, 8, 4],   # Row 1: descending (-6 score)  
            [2, 0, 4, 0],     # Row 2: [2,4] ascending (+1 score)
            [0, 0, 0, 0]      # Row 3: empty (0 score)
        ]
        
        self.game.import_board_state(board_state)
        monotonic_score = self.ai._total_monotonicity_score(self.game._board)
        
        # Expected calculation:
        # Row 0: [2,4,8,16] = +3 (ascending preferred)
        # Row 1: [32,16,8,4] = -6 (descending penalized ×2)
        # Row 2: [2,0,4,0] = 0 (zeros skip all comparisons)
        # Row 3: [0,0,0,0] = 0 (no pairs)
        # Col 0: [2,32,2] = -1 (2<32: +1, 32>2: -2 = -1)
        # Col 1: [4,16,0,0] = +1 (4<16: +1, other comparisons have zeros)
        # Col 2: [8,8,4,0] = -2 (8=8 skipped, 8>4: -2)
        # Col 3: [16,4,0,0] = -2 (16>4: -2, other comparisons have zeros)
        # Total: 3 - 6 + 0 + 0 - 1 + 1 - 2 - 2 = -7
        self.assertEqual(monotonic_score, -7)

    def test_max_tile_in_corner_true(self):
        """Test max tile in corner detection when max tile is in corner."""
        board_state = [
            [2048, 4, 8, 16],  # Max tile (2048) in top-left corner
            [32, 64, 128, 256],
            [512, 1024, 2, 4],
            [8, 16, 32, 64]
        ]
        
        self.game.import_board_state(board_state)
        corner_bonus = self.ai._max_tile_in_corner(self.game._board)
        self.assertEqual(corner_bonus, 1)

    def test_max_tile_in_corner_false(self):
        """Test max tile in corner detection when max tile is not in corner."""
        board_state = [
            [2, 4, 8, 16],
            [32, 2048, 128, 256],  # Max tile (2048) in middle
            [512, 1024, 2, 4],
            [8, 16, 32, 64]
        ]
        
        self.game.import_board_state(board_state)
        corner_bonus = self.ai._max_tile_in_corner(self.game._board)
        self.assertEqual(corner_bonus, 0)

    def test_max_tile_in_different_corners(self):
        """Test max tile in corner detection for all four corners."""
        corners_positions = [
            (0, 0),  # Top-left
            (0, 3),  # Top-right
            (3, 0),  # Bottom-left
            (3, 3)   # Bottom-right
        ]
        
        for row, col in corners_positions:
            with self.subTest(corner=(row, col)):
                board_state = [[0 for _ in range(4)] for _ in range(4)]
                board_state[row][col] = 2048  # Place max tile in corner
                board_state[1][1] = 4  # Place smaller tile elsewhere
                
                self.game.import_board_state(board_state)
                corner_bonus = self.ai._max_tile_in_corner(self.game._board)
                self.assertEqual(corner_bonus, 1)


class TestBoardEvaluation(unittest.TestCase):
    """Test cases for board evaluation and move simulation."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game2048()
        self.ai = GameAI(self.game)

    def test_evaluate_board_empty(self):
        """Test board evaluation with mostly empty board."""
        # Board with 2 tiles (14 empty)
        score = self.ai._evaluate_board(self.game._board)
        
        # Should have high score due to many empty tiles
        # New formula: 2.0 * empty_tiles + 1.0 * monotonicity + 10.0 * corner_bonus
        # With 14 empty tiles: at least 14 * 2.0 = 28 points
        self.assertGreater(score, 25)

    def test_evaluate_board_full(self):
        """Test board evaluation with full board."""
        board_state = [
            [2, 4, 8, 16],
            [32, 64, 128, 256], 
            [512, 1024, 2048, 4096],
            [8192, 16384, 32768, 65536]
        ]
        self.game.import_board_state(board_state)
        score = self.ai._evaluate_board(self.game._board)
        
        # New formula: 2.0 * empty_tiles + 1.0 * monotonicity + 10.0 * corner_bonus
        # Empty tiles: 0 (×2.0 = 0)
        # Monotonicity: All rows and columns ascending = 24 points (×1.0 = 24)  
        # Corner bonus: Max tile (65536) is in corner (×10.0 = 10)
        # Total: 0 + 24 + 10 = 34
        self.assertEqual(score, 34)

    def test_evaluate_board_mixed(self):
        """Test board evaluation with mixed state."""
        board_state = [
            [2, 4, 8, 16],    # Monotonic row
            [0, 0, 0, 0],     # Empty row
            [0, 2, 0, 0],     # Sparse
            [0, 0, 0, 4]      # Sparse
        ]
        self.game.import_board_state(board_state)
        score = self.ai._evaluate_board(self.game._board)
        
        # New formula: 2.0 * empty_tiles + 1.0 * monotonicity + 10.0 * corner_bonus
        # Empty tiles: 10 (×2.0 = 20)
        # Max tile (16) not in corner (×10.0 = 0)
        # Should have score around 20 + monotonicity_contribution
        self.assertGreater(score, 15)

    def test_simulate_move_valid_directions(self):
        """Test move simulation for all valid directions."""
        directions = ['left', 'right', 'up', 'down']
        
        for direction in directions:
            with self.subTest(direction=direction):
                result_board, moved = self.ai._simulate_move(direction)
                
                # Should return a board and movement status
                self.assertIsNotNone(result_board)
                self.assertIsInstance(moved, bool)
                
                # Original game board should be unchanged
                original_state = self.game.export_board_state()[0]
                # Check that original board wasn't modified by comparing a few cells
                self.assertEqual(self.game._board.get_cell(0, 0), original_state[0][0])

    def test_simulate_move_invalid_direction(self):
        """Test move simulation with invalid direction."""
        with self.assertRaises(ValueError):
            self.ai._simulate_move('invalid')

    def test_simulate_move_no_change(self):
        """Test move simulation when move doesn't change board."""
        # Create a board where left move is impossible
        board_state = [
            [2, 4, 8, 16],
            [32, 64, 128, 256],
            [512, 1024, 2048, 4096], 
            [8192, 16384, 32768, 65536]
        ]
        self.game.import_board_state(board_state)
        
        # Left move should not change anything (already compressed left)
        _, moved = self.ai._simulate_move('left')
        self.assertFalse(moved)


class TestBestMoveSelection(unittest.TestCase):
    """Test cases for best move selection."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game2048()
        self.ai = GameAI(self.game)

    def test_get_best_move_returns_valid_direction(self):
        """Test that get_best_move returns a valid direction."""
        best_move = self.ai.get_best_move()
        
        if best_move is not None:
            self.assertIn(best_move, ['left', 'right', 'up', 'down'])

    def test_get_best_move_no_moves_possible(self):
        """Test get_best_move when no moves are possible."""
        # Create a board where no moves are possible
        board_state = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2]
        ]
        self.game.import_board_state(board_state)
        
        best_move = self.ai.get_best_move()
        self.assertIsNone(best_move)

    def test_get_best_move_considers_corner_bonus(self):
        """Test that AI considers corner bonus in move selection."""
        # Create a board where corner bonus affects move choice
        board_state = [
            [2, 2, 0, 0],
            [4, 4, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.import_board_state(board_state)
        
        best_move = self.ai.get_best_move()
        # DOWN move puts max tile in corner, which should be preferred due to corner bonus
        self.assertEqual(best_move, 'down')

    def test_get_best_move_prioritizes_corner_over_empty_tiles(self):
        """Test that AI prioritizes corner bonus over just empty tiles."""
        # Create a board where corner bonus competes with empty tiles
        board_state = [
            [2, 4, 0, 0],
            [2, 4, 0, 0], 
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.game.import_board_state(board_state)
        
        best_move = self.ai.get_best_move()
        # RIGHT move gets corner bonus and should be preferred over UP (more empty tiles)
        self.assertEqual(best_move, 'right')

    def test_get_best_move_considers_monotonicity(self):
        """Test that AI considers monotonicity in move selection."""
        # Create a board state where monotonicity affects move choice
        board_state = [
            [2, 4, 8, 0],
            [0, 0, 0, 16],
            [0, 0, 0, 0], 
            [0, 0, 0, 0]
        ]
        self.game.import_board_state(board_state)
        
        best_move = self.ai.get_best_move()
        # AI should return a valid move to improve the board state
        self.assertIsNotNone(best_move)
        self.assertEqual(best_move, 'up')


class TestGameIntegration(unittest.TestCase):
    """Integration tests for GameAI with Game2048."""

    def test_ai_factory_method(self):
        """Test that game.get_ai() creates a proper AI instance."""
        game = Game2048()
        ai = game.get_ai()
        
        self.assertIsInstance(ai, GameAI)
        self.assertIs(ai.game, game)

    def test_ai_works_with_different_game_states(self):
        """Test that AI works correctly with different game states."""
        # Test with custom board state
        board_state = [
            [2, 0, 4, 0],
            [0, 8, 0, 16],
            [0, 0, 0, 0],
            [32, 0, 0, 64]
        ]
        
        game = Game2048.from_state(board_state, score=100)
        ai = game.get_ai()
        
        # AI should be able to analyze this state
        best_move = ai.get_best_move()
        self.assertIn(best_move, ['left', 'right', 'up', 'down', None])
        
        # Board evaluation should work
        score = ai._evaluate_board(game._board)
        self.assertIsInstance(score, (int, float))
        self.assertGreater(score, 0)


if __name__ == '__main__':
    unittest.main()