import random


class TileGenerator:
    """Handles random tile generation and placement."""
    
    def __init__(self, tile_2_probability=0.9):
        """Initialize the tile generator with probability settings."""
        self.tile_2_probability = tile_2_probability
    
    def generate_tile_value(self):
        """Generate a new tile value (2 or 4) based on probability."""
        return 2 if random.random() < self.tile_2_probability else 4
    
    def add_random_tile(self, board):
        """Add a random tile to an empty cell on the board.
        
        Args:
            board: Board instance to add tile to
            
        Returns:
            bool: True if a tile was added, False if board was full
        """
        empty_cells = board.get_empty_cells()
        
        if not empty_cells:
            return False
        
        # Randomly select an empty cell
        row, col = random.choice(empty_cells)
        tile_value = self.generate_tile_value()
        board.set_cell(row, col, tile_value)
        
        return True