import os
from typing import Optional

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    anthropic = None


class ClaudeAI:
    """AI system using Claude API for 2048 move suggestions."""
    
    def __init__(self, game):
        """Initialize Claude AI with a reference to the game instance.
        
        Args:
            game: Game2048 instance to analyze
        """
        self.game = game
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Anthropic client if module and API key are available."""
        if not ANTHROPIC_AVAILABLE:
            self.client = None
            return
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            try:
                self.client = anthropic.Anthropic(api_key=api_key)
            except Exception as e:
                # Debug: print exception for troubleshooting
                print(f"Failed to initialize Anthropic client: {e}")
                self.client = None
        else:
            self.client = None
    
    def is_available(self) -> bool:
        """Check if Claude AI is available (module installed and API key configured)."""
        return ANTHROPIC_AVAILABLE and self.client is not None
    
    def _format_board_state(self) -> str:
        """Format the current board state for Claude API."""
        board_state, score = self.game.export_board_state()
        
        # Create a readable board representation
        board_str = "Current 2048 Board State:\n"
        board_str += f"Score: {score}\n\n"
        
        for row in board_state:
            row_str = "|"
            for cell in row:
                if cell == 0:
                    row_str += "    |"
                else:
                    row_str += f"{cell:4}|"
            board_str += row_str + "\n"
        
        return board_str
    
    def get_best_move(self) -> Optional[str]:
        """Get move suggestion from Claude API.
        
        Returns:
            str or None: Move direction ('up', 'left', 'down', 'right') or None if unavailable
        """
        if not self.is_available():
            return None
        
        try:
            board_state_str = self._format_board_state()
            
            prompt = f"""You are an expert 2048 game player. Analyze the current board state and suggest the best move.

            {board_state_str}

            Available moves: Up (W), Left (A), Down (S), Right (D)

            Rules:
            - Tiles slide in the chosen direction until they hit another tile or wall
            - Adjacent tiles with same numbers merge into one tile with doubled value
            - Only one merge per tile per move
            - After each move, a new tile (2 or 4) appears randomly

            Please analyze the board and suggest the best move considering:
            1. Creating merge opportunities
            2. Keeping high-value tiles in corners
            3. Maintaining monotonic sequences
            4. Maximizing empty spaces

            Respond with just one word: "up", "left", "down", or "right" for your recommended move."""

            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=100,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract the response text
            if message.content and len(message.content) > 0:
                response_text = message.content[0].text.strip().lower()
                
                # Validate response is a valid direction
                if response_text in ['up', 'left', 'down', 'right']:
                    return response_text
            
            return None
            
        except Exception:
            # Return None if API call fails
            return None