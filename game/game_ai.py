class GameAI:
    """AI system for analyzing and suggesting moves in 2048 game."""
    
    def __init__(self, game):
        """Initialize AI with a reference to the game instance.
        
        Args:
            game: Game2048 instance to analyze
        """
        self.game = game
    
    def _count_empty_tiles(self, board):
        """Count the number of empty tiles on the board.
        
        Args:
            board: Board instance to analyze
            
        Returns:
            int: Number of empty tiles (cells with value 0)
        """
        return len(board.get_empty_cells())
    
    def _monotonicity_score(self, line):
        """Calculate monotonicity score for a single row or column.
        
        Args:
            line: List of integers representing a row or column
            
        Returns:
            int: Monotonicity score (positive for ascending, negative for descending)
        """
        score = 0
        
        for i in range(len(line) - 1):
            current = line[i]
            next_val = line[i + 1]
            
            # Skip scoring if either value is zero
            if current == 0 or next_val == 0:
                continue
            
            if current < next_val:
                # Reward ascending order
                score += 1
            elif current > next_val:
                # Penalize descending order (×2 penalty)
                score -= 2
            # Equal values don't affect score
        
        return score
    
    def _total_monotonicity_score(self, board):
        """Calculate total monotonicity score for the entire board.
        
        Args:
            board: Board instance to analyze
            
        Returns:
            int: Total monotonicity score across all rows and columns (ascending preferred)
        """
        total_score = 0
        size = board.size
        
        # Score all rows (ascending preferred)
        for i in range(size):
            row = board.get_row(i)
            total_score += self._monotonicity_score(row)
        
        # Score all columns (ascending preferred)
        for j in range(size):
            column = [board.get_cell(i, j) for i in range(size)]
            total_score += self._monotonicity_score(column)
        
        return total_score
    
    def _max_tile_in_corner(self, board):
        max_tile = max(cell for row in board.grid for cell in row)
        corners = [
            board.get_cell(0, 0),
            board.get_cell(0, board.size - 1),
            board.get_cell(board.size - 1, 0),
            board.get_cell(board.size - 1, board.size - 1)
        ]
        return 1 if max_tile in corners else 0

    def _simulate_move(self, direction):
        """Simulate a move without modifying the actual game state.
        
        Args:
            direction: String indicating direction ('left', 'right', 'up', 'down')
            
        Returns:
            tuple: (board_after_move, moved) where moved is True if the move caused changes
        """
        # Create a copy of the current board
        test_board = self.game._board.copy()
        
        # Apply the move to the test board
        if direction == 'left':
            _, moved = self.game._movement_engine.move_left(test_board)
        elif direction == 'right':
            _, moved = self.game._movement_engine.move_right(test_board)
        elif direction == 'up':
            _, moved = self.game._movement_engine.move_up(test_board)
        elif direction == 'down':
            _, moved = self.game._movement_engine.move_down(test_board)
        else:
            raise ValueError(f"Invalid direction: {direction}")
        
        return test_board, moved
    
    def _evaluate_board(self, board):
        """Evaluate a board state using the heuristic function.
        
        Args:
            board: Board instance to evaluate
            
        Returns:
            int: Heuristic score for the board state
        """
        
        return (
            # Count empty tiles
            2.0 * self._count_empty_tiles(board) +
            # Calculate monotonicity score
            1.0 * self._total_monotonicity_score(board) +
            # Calculate if largest tile is in a corner
            10.0 * self._max_tile_in_corner(board)
        )
    
    def get_best_move(self):
        """Analyze all possible moves and return the best one based on heuristics.
        
        Returns:
            str or None: Best move direction ('left', 'right', 'up', 'down') or None if no moves possible
        """
        directions = ['left', 'right', 'up', 'down']
        best_move = None
        best_score = -1
        
        for direction in directions:
            # Simulate the move
            resulting_board, moved = self._simulate_move(direction)
            
            # Skip if move doesn't change the board
            if not moved:
                continue
            
            # Evaluate the resulting board state
            score = self._evaluate_board(resulting_board)
            
            # Track the best scoring move
            if score > best_score:
                best_score = score
                best_move = direction
        
        return best_move