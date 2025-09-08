class Board:
    """Manages the 2D game board state."""
    
    def __init__(self, size=4):
        """Initialize an empty board of the given size."""
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
    
    def get_cell(self, row, col):
        """Get the value at a specific position."""
        return self.grid[row][col]
    
    def set_cell(self, row, col, value):
        """Set the value at a specific position."""
        self.grid[row][col] = value
    
    def get_row(self, row_index):
        """Get a copy of a specific row."""
        return self.grid[row_index][:]
    
    def set_row(self, row_index, row):
        """Set a specific row."""
        self.grid[row_index] = row[:]
    
    def get_empty_cells(self):
        """Get a list of all empty cell positions (row, col)."""
        empty_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    empty_cells.append((i, j))
        return empty_cells
    
    def is_full(self):
        """Check if the board has no empty cells."""
        return len(self.get_empty_cells()) == 0
    
    def copy(self):
        """Create a deep copy of the board."""
        new_board = Board(self.size)
        for i in range(self.size):
            for j in range(self.size):
                new_board.grid[i][j] = self.grid[i][j]
        return new_board
    
    def transpose(self):
        """Transpose the board (swap rows and columns)."""
        transposed_grid = [[self.grid[j][i] for j in range(self.size)] 
                          for i in range(self.size)]
        self.grid = transposed_grid
    
    def __eq__(self, other):
        """Check if two boards are equal."""
        if not isinstance(other, Board) or self.size != other.size:
            return False
        return self.grid == other.grid