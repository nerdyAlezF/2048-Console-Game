class MovementEngine:
    """Handles tile movement, compression, and merging logic."""
    
    def __init__(self, board_size=4):
        """Initialize the movement engine with board size."""
        self.board_size = board_size
    
    def compress_row_left(self, row):
        """Compress a row to the left, removing zeros.
        
        Args:
            row: List representing a row of tiles
            
        Returns:
            List: Compressed row with zeros moved to the right
        """
        compressed = [cell for cell in row if cell != 0]
        return compressed + [0] * (self.board_size - len(compressed))
    
    def merge_row_left(self, row):
        """Merge adjacent equal tiles in a row from left to right.
        
        Args:
            row: List representing a row of tiles
            
        Returns:
            tuple: (merged_row, score_gained)
        """
        merged = row[:]
        score_gained = 0
        
        for i in range(self.board_size - 1):
            if merged[i] != 0 and merged[i] == merged[i + 1]:
                merged[i] *= 2
                merged[i + 1] = 0
                score_gained += merged[i]
        
        return merged, score_gained
    
    def process_row_left(self, row):
        """Process a single row for left movement (compress-merge-compress).
        
        Args:
            row: List representing a row of tiles
            
        Returns:
            tuple: (final_row, score_gained, moved)
        """
        original_row = row[:]
        
        # Step 1: Compress tiles to the left
        compressed_row = self.compress_row_left(row)
        
        # Step 2: Merge same values
        merged_row, score_gained = self.merge_row_left(compressed_row)
        
        # Step 3: Compress again after merges
        final_row = self.compress_row_left(merged_row)
        
        # Check if row changed
        moved = original_row != final_row
        
        return final_row, score_gained, moved
    
    def move_left(self, board):
        """Move all tiles on the board to the left.
        
        Args:
            board: Board instance to modify
            
        Returns:
            tuple: (total_score_gained, moved)
        """
        moved = False
        total_score_gained = 0
        
        for i in range(self.board_size):
            row = board.get_row(i)
            final_row, score_gained, row_moved = self.process_row_left(row)
            
            board.set_row(i, final_row)
            total_score_gained += score_gained
            
            if row_moved:
                moved = True
        
        return total_score_gained, moved
    
    def move_right(self, board):
        """Move all tiles on the board to the right.
        
        Uses the existing left movement logic by reversing rows.
        
        Args:
            board: Board instance to modify
            
        Returns:
            tuple: (total_score_gained, moved)
        """
        moved = False
        total_score_gained = 0
        
        for i in range(self.board_size):
            row = board.get_row(i)
            
            # Reverse row, process as left movement, then reverse back
            reversed_row = row[::-1]
            final_reversed_row, score_gained, row_moved = self.process_row_left(reversed_row)
            final_row = final_reversed_row[::-1]
            
            board.set_row(i, final_row)
            total_score_gained += score_gained
            
            if row_moved:
                moved = True
        
        return total_score_gained, moved
    
    def move_up(self, board):
        """Move all tiles up.
        
        Uses transpose-move_left-transpose pattern for maximum code reuse.
        
        Args:
            board: Board instance to modify
            
        Returns:
            tuple: (total_score_gained, moved)
        """
        # Transpose, move left, transpose back
        board.transpose()
        score_gained, moved = self.move_left(board)
        board.transpose()
        
        return score_gained, moved
    
    def move_down(self, board):
        """Move all tiles down.
        
        Uses transpose-move_right-transpose pattern for maximum code reuse.
        
        Args:
            board: Board instance to modify
            
        Returns:
            tuple: (total_score_gained, moved)
        """
        # Transpose, move right, transpose back
        board.transpose()
        score_gained, moved = self.move_right(board)
        board.transpose()
        
        return score_gained, moved