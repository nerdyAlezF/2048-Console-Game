import unittest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.game2048 import Game2048


class TestClaudeAI(unittest.TestCase):
    """Test cases for the ClaudeAI class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.game = Game2048()

    @patch('game.claude_ai.ANTHROPIC_AVAILABLE', True)
    @patch('os.getenv')
    @patch('game.claude_ai.anthropic')
    def test_claude_ai_initialization_with_api_key(self, mock_anthropic, mock_getenv):
        """Test ClaudeAI initialization when API key is available."""
        mock_getenv.return_value = 'test_api_key'
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client
        
        from game.claude_ai import ClaudeAI
        ai = ClaudeAI(self.game)
        
        self.assertIs(ai.game, self.game)
        self.assertIs(ai.client, mock_client)
        mock_anthropic.Anthropic.assert_called_once_with(api_key='test_api_key')

    @patch('game.claude_ai.ANTHROPIC_AVAILABLE', True)
    @patch('os.getenv')
    def test_claude_ai_initialization_without_api_key(self, mock_getenv):
        """Test ClaudeAI initialization when API key is not available."""
        mock_getenv.return_value = None
        
        from game.claude_ai import ClaudeAI
        ai = ClaudeAI(self.game)
        
        self.assertIs(ai.game, self.game)
        self.assertIsNone(ai.client)

    @patch('game.claude_ai.ANTHROPIC_AVAILABLE', False)
    def test_claude_ai_initialization_without_anthropic_module(self):
        """Test ClaudeAI initialization when anthropic module is not available."""
        from game.claude_ai import ClaudeAI
        ai = ClaudeAI(self.game)
        
        self.assertIs(ai.game, self.game)
        self.assertIsNone(ai.client)

    @patch('game.claude_ai.ANTHROPIC_AVAILABLE', True)
    @patch('os.getenv')
    @patch('game.claude_ai.anthropic')
    def test_claude_ai_initialization_client_exception(self, mock_anthropic, mock_getenv):
        """Test ClaudeAI initialization when client creation raises exception."""
        mock_getenv.return_value = 'test_api_key'
        mock_anthropic.Anthropic.side_effect = Exception("API error")
        
        with patch('builtins.print') as mock_print:
            from game.claude_ai import ClaudeAI
            ai = ClaudeAI(self.game)
            
            self.assertIs(ai.game, self.game)
            self.assertIsNone(ai.client)
            mock_print.assert_called_once_with("Failed to initialize Anthropic client: API error")

    @patch('game.claude_ai.ANTHROPIC_AVAILABLE', True)
    @patch('os.getenv')
    @patch('game.claude_ai.anthropic')
    def test_is_available_true(self, mock_anthropic, mock_getenv):
        """Test is_available returns True when client is available."""
        mock_getenv.return_value = 'test_api_key'
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client
        
        from game.claude_ai import ClaudeAI
        ai = ClaudeAI(self.game)
        
        self.assertTrue(ai.is_available())

    @patch('game.claude_ai.ANTHROPIC_AVAILABLE', False)
    def test_is_available_false_no_module(self):
        """Test is_available returns False when anthropic module is not available."""
        from game.claude_ai import ClaudeAI
        ai = ClaudeAI(self.game)
        
        self.assertFalse(ai.is_available())

    @patch('game.claude_ai.ANTHROPIC_AVAILABLE', True)
    @patch('os.getenv')
    def test_is_available_false_no_client(self, mock_getenv):
        """Test is_available returns False when client is None."""
        mock_getenv.return_value = None
        
        from game.claude_ai import ClaudeAI
        ai = ClaudeAI(self.game)
        
        self.assertFalse(ai.is_available())

    @patch('game.claude_ai.ANTHROPIC_AVAILABLE', True)
    @patch('os.getenv')
    @patch('game.claude_ai.anthropic')
    def test_format_board_state(self, mock_anthropic, mock_getenv):
        """Test board state formatting."""
        mock_getenv.return_value = 'test_api_key'
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client
        
        # Set up a specific board state
        board_state = [
            [2, 4, 8, 16],
            [0, 0, 32, 64],
            [0, 0, 0, 128],
            [0, 0, 0, 0]
        ]
        self.game.import_board_state(board_state, 500)
        
        from game.claude_ai import ClaudeAI
        ai = ClaudeAI(self.game)
        
        formatted_state = ai._format_board_state()
        
        self.assertIn("Current 2048 Board State:", formatted_state)
        self.assertIn("Score: 500", formatted_state)
        self.assertIn("   2|   4|   8|  16|", formatted_state)
        self.assertIn("    |    |  32|  64|", formatted_state)
        self.assertIn("    |    |    | 128|", formatted_state)
        self.assertIn("    |    |    |    |", formatted_state)

    @patch('game.claude_ai.ANTHROPIC_AVAILABLE', True)
    @patch('os.getenv')
    @patch('game.claude_ai.anthropic')
    def test_get_best_move_success(self, mock_anthropic, mock_getenv):
        """Test successful AI move suggestion."""
        mock_getenv.return_value = 'test_api_key'
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client
        
        # Mock the API response
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = "left"
        mock_client.messages.create.return_value = mock_response
        
        from game.claude_ai import ClaudeAI
        ai = ClaudeAI(self.game)
        
        with patch('builtins.print'):
            move = ai.get_best_move()
        
        self.assertEqual(move, "left")
        mock_client.messages.create.assert_called_once()

    @patch('game.claude_ai.ANTHROPIC_AVAILABLE', True)
    @patch('os.getenv')
    @patch('game.claude_ai.anthropic')
    def test_get_best_move_invalid_response(self, mock_anthropic, mock_getenv):
        """Test AI move suggestion with invalid response."""
        mock_getenv.return_value = 'test_api_key'
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client
        
        # Mock invalid API response
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = "invalid_move"
        mock_client.messages.create.return_value = mock_response
        
        from game.claude_ai import ClaudeAI
        ai = ClaudeAI(self.game)
        
        with patch('builtins.print'):
            move = ai.get_best_move()
        
        self.assertIsNone(move)

    @patch('game.claude_ai.ANTHROPIC_AVAILABLE', True)
    @patch('os.getenv')
    @patch('game.claude_ai.anthropic')
    def test_get_best_move_empty_response(self, mock_anthropic, mock_getenv):
        """Test AI move suggestion with empty response."""
        mock_getenv.return_value = 'test_api_key'
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client
        
        # Mock empty API response
        mock_response = MagicMock()
        mock_response.content = []
        mock_client.messages.create.return_value = mock_response
        
        from game.claude_ai import ClaudeAI
        ai = ClaudeAI(self.game)
        
        with patch('builtins.print'):
            move = ai.get_best_move()
        
        self.assertIsNone(move)

    @patch('game.claude_ai.ANTHROPIC_AVAILABLE', True)
    @patch('os.getenv')
    @patch('game.claude_ai.anthropic')
    def test_get_best_move_api_exception(self, mock_anthropic, mock_getenv):
        """Test AI move suggestion when API call raises exception."""
        mock_getenv.return_value = 'test_api_key'
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client
        
        # Mock API exception
        mock_client.messages.create.side_effect = Exception("API error")
        
        from game.claude_ai import ClaudeAI
        ai = ClaudeAI(self.game)
        
        move = ai.get_best_move()
        
        self.assertIsNone(move)

    def test_get_best_move_unavailable(self):
        """Test get_best_move when AI is not available."""
        from game.claude_ai import ClaudeAI
        ai = ClaudeAI(self.game)
        
        move = ai.get_best_move()
        
        self.assertIsNone(move)

    @patch('game.claude_ai.ANTHROPIC_AVAILABLE', True)
    @patch('os.getenv')
    @patch('game.claude_ai.anthropic')
    def test_get_best_move_valid_directions(self, mock_anthropic, mock_getenv):
        """Test that all valid directions are accepted."""
        mock_getenv.return_value = 'test_api_key'
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client
        
        from game.claude_ai import ClaudeAI
        ai = ClaudeAI(self.game)
        
        valid_moves = ['up', 'left', 'down', 'right']
        
        for move in valid_moves:
            mock_response = MagicMock()
            mock_response.content = [MagicMock()]
            mock_response.content[0].text = move.upper()  # Test case insensitivity
            mock_client.messages.create.return_value = mock_response
            
            with patch('builtins.print'):
                result = ai.get_best_move()
            self.assertEqual(result, move)

    @patch('game.claude_ai.ANTHROPIC_AVAILABLE', True)
    @patch('os.getenv')
    @patch('game.claude_ai.anthropic')
    def test_get_best_move_prompt_content(self, mock_anthropic, mock_getenv):
        """Test that the prompt contains expected content."""
        mock_getenv.return_value = 'test_api_key'
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = "up"
        mock_client.messages.create.return_value = mock_response
        
        from game.claude_ai import ClaudeAI
        ai = ClaudeAI(self.game)
        
        with patch('builtins.print'):
            ai.get_best_move()
        
        # Verify the API call was made with correct parameters
        call_args = mock_client.messages.create.call_args
        self.assertEqual(call_args.kwargs['model'], "claude-sonnet-4-20250514")
        self.assertEqual(call_args.kwargs['max_tokens'], 100)
        
        prompt_content = call_args.kwargs['messages'][0]['content']
        self.assertIn("Current 2048 Board State:", prompt_content)
        self.assertIn("Available moves: Up (W), Left (A), Down (S), Right (D)", prompt_content)
        self.assertIn("Creating merge opportunities", prompt_content)
        self.assertIn("Keeping high-value tiles in corners", prompt_content)


if __name__ == '__main__':
    unittest.main()