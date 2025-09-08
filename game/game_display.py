class GameDisplay:
    """Handles game display and UI rendering."""
    
    def display_board_and_score(self, board, score):
        """Display the current board state and score.
        
        Args:
            board: Board instance to display
            score: Current game score
        """
        # Score
        print(f"\nScore: {score}")
        print("-" * 25)
        
        # Board
        for i in range(board.size):
            print("|", end="")
            for j in range(board.size):
                cell = board.get_cell(i, j)
                if cell == 0:
                    print("    ", end=" |")
                else:
                    print(f"{cell:4d}", end=" |")
            print()
            print("-" * 25)