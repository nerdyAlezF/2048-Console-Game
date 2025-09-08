from .board import Board
from .tile_generator import TileGenerator
from .movement_engine import MovementEngine
from .game_display import GameDisplay


class Game2048:
    """Main game class with clean, encapsulated API."""
    
    def __init__(self, tile_2_probability=0.9, size=4):
        """Initialize the game with configuration parameters."""
        self._size = size
        self._board = Board(size)
        self._tile_generator = TileGenerator(tile_2_probability)
        self._movement_engine = MovementEngine(size)
        self._display = GameDisplay()
        self._score = 0
        
        # Add initial tiles
        self._tile_generator.add_random_tile(self._board)
        self._tile_generator.add_random_tile(self._board)
    
    # Public API - Game Actions
    def _execute_move(self, move_function):
        """Execute a move and handle score/tile generation.
        
        Args:
            move_function: Function that performs the movement on the board
            
        Returns:
            bool: True if any tiles moved, False otherwise
        """
        score_gained, moved = move_function(self._board)
        if moved:
            self._score += score_gained
            self._tile_generator.add_random_tile(self._board)
        return moved
    
    def move_left(self):
        """Move all tiles to the left.
        
        Returns:
            bool: True if any tiles moved, False otherwise
        """
        return self._execute_move(self._movement_engine.move_left)
    
    def move_right(self):
        """Move all tiles to the right.
        
        Returns:
            bool: True if any tiles moved, False otherwise
        """
        return self._execute_move(self._movement_engine.move_right)
    
    def move_up(self):
        """Move all tiles up.
        
        Returns:
            bool: True if any tiles moved, False otherwise
        """
        return self._execute_move(self._movement_engine.move_up)
    
    def move_down(self):
        """Move all tiles down.
        
        Returns:
            bool: True if any tiles moved, False otherwise
        """
        return self._execute_move(self._movement_engine.move_down)
    
    def display_game(self):
        """Display the current game state."""
        self._display.display_board_and_score(self._board, self._score)
    
    def restart_game(self):
        """Restart the game with a fresh board and reset score."""
        self._score = 0
        self._board = Board(self._size)
        
        # Add initial tiles
        self._tile_generator.add_random_tile(self._board)
        self._tile_generator.add_random_tile(self._board)
    
    def import_board_state(self, board_state, score=None):
        """Import a specific board state for testing or game setup.
        
        Args:
            board_state: Either a 2D list [[row1], [row2], ...] or 
                        a flat list [cell1, cell2, ...] with size*size elements
            score: Optional score to set (defaults to current score)
        """
        self._board.import_state(board_state)
        if score is not None:
            self._score = score
    
    def export_board_state(self):
        """Export the current board state as a 2D list.
            
        Returns:
            Tuple of (board_state, score)
        """
        return self._board.export_state(), self._score
    
    @classmethod
    def from_state(cls, board_state, score=0, tile_2_probability=0.9, size=4):
        """Create a game instance with a specific board state.
        
        Args:
            board_state: Initial board state
            score: Initial score
            tile_2_probability: Probability of generating 2s vs 4s
            size: Board size
            
        Returns:
            Game2048 instance with the specified state
        """
        game = cls(tile_2_probability, size)
        game.import_board_state(board_state, score)
        return game
    
    # Public API - Game State (Read-only)
    def get_score(self):
        """Get the current score."""
        return self._score
    
    def get_board_size(self):
        """Get the board size."""
        return self._size
    
    def is_game_over(self):
        """Check if the game is over (no moves possible)."""
        # If there are empty cells, game is not over
        if not self._board.is_full():
            return False
        
        # Board is full - now check if any moves are possible in any direction
        # Create a temporary copy to test moves without affecting the real board
        from .board import Board
        
        def reset_test_board():
            test_board = Board(self._size)
            for i in range(self._size):
                for j in range(self._size):
                    test_board.set_cell(i, j, self._board.get_cell(i, j))
            return test_board
        
        # Test each direction - if any move is possible, game is not over
        # Only reset the test board when the previous move actually changed it
        test_board = reset_test_board()
        
        _, left_moved = self._movement_engine.move_left(test_board)
        if left_moved:
            return False
            
        _, right_moved = self._movement_engine.move_right(test_board)
        if right_moved:
            return False
            
        _, up_moved = self._movement_engine.move_up(test_board)
        if up_moved:
            return False
            
        _, down_moved = self._movement_engine.move_down(test_board)
        if down_moved:
            return False
        
        # No moves possible in any direction - game over
        return True
    
    def has_won(self):
        """Check if player has reached 2048 tile."""
        for i in range(self._size):
            for j in range(self._size):
                if self._board.get_cell(i, j) == 2048:
                    return True
        return False
    
    def get_ai(self):
        """Get an AI instance for this game.
        
        Returns:
            GameAI: AI instance that can analyze and suggest moves
        """
        from .game_ai import GameAI
        return GameAI(self)