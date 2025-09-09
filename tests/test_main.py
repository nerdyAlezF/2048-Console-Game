import unittest
import sys
import os
from unittest.mock import patch, MagicMock, call
from io import StringIO

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import print_instructions, get_user_input, main
from game.game2048 import Game2048


class TestMainCLI(unittest.TestCase):
    """Test cases for the main CLI functionality."""
    
    def test_print_instructions(self):
        """Test that instructions are printed correctly."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            print_instructions()
            output = fake_output.getvalue()
            
            # Check for key elements
            self.assertIn("Welcome to 2048!", output)
            self.assertIn("W - Move Up", output)
            self.assertIn("A - Move Left", output)
            self.assertIn("S - Move Down", output)
            self.assertIn("D - Move Right", output)
            self.assertIn("H - AI Hint (get move suggestion)", output)
            self.assertIn("R - Restart Game", output)
            self.assertIn("Q - Quit Game", output)
    
    @patch('builtins.input', return_value='W')
    def test_get_user_input_valid(self, mock_input):
        """Test get_user_input with valid input."""
        result = get_user_input()
        self.assertEqual(result, 'W')
        mock_input.assert_called_once_with("\nEnter your move (W/A/S/D/H/R/Q): ")
    
    @patch('builtins.input', return_value='  a  ')
    def test_get_user_input_case_insensitive_and_strips(self, mock_input):
        """Test get_user_input converts to uppercase and strips whitespace."""
        result = get_user_input()
        self.assertEqual(result, 'A')
    
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    @patch('sys.exit')
    def test_get_user_input_keyboard_interrupt(self, mock_exit, mock_input):
        """Test get_user_input handles KeyboardInterrupt gracefully."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            get_user_input()
            output = fake_output.getvalue()
            self.assertIn("Game interrupted. Goodbye!", output)
            mock_exit.assert_called_once_with(0)
    
    @patch('builtins.input', side_effect=EOFError)
    @patch('sys.exit')
    def test_get_user_input_eof_error(self, mock_exit, mock_input):
        """Test get_user_input handles EOFError gracefully."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            get_user_input()
            output = fake_output.getvalue()
            self.assertIn("Game interrupted. Goodbye!", output)
            mock_exit.assert_called_once_with(0)


class TestMainGameLoop(unittest.TestCase):
    """Test cases for the main game loop functionality."""
    
    @patch('main.get_user_input', return_value='Q')
    @patch('main.print_instructions')
    def test_main_quit_immediately(self, mock_instructions, mock_input):
        """Test main loop when user quits immediately."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            main()
            output = fake_output.getvalue()
            self.assertIn("Thanks for playing!", output)
            mock_instructions.assert_called_once()
    
    @patch('main.get_user_input', side_effect=['W', 'Q'])
    @patch('main.print_instructions')
    def test_main_single_move_then_quit(self, mock_instructions, mock_input):
        """Test main loop with one move then quit."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            main()
            output = fake_output.getvalue()
            self.assertIn("Thanks for playing!", output)
            mock_instructions.assert_called_once()
    
    @patch('main.get_user_input', return_value='Q')
    @patch('main.print_instructions')
    def test_main_displays_controls_reminder(self, mock_instructions, mock_input):
        """Test that controls reminder is displayed during gameplay."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            main()
            output = fake_output.getvalue()
            self.assertIn("Controls: W/A/S/D=Move  H=AI Hint  R=Restart  Q=Quit", output)
            mock_instructions.assert_called_once()
    
    @patch('main.get_user_input', side_effect=['X', 'Q'])
    @patch('main.print_instructions')
    def test_main_invalid_input(self, mock_instructions, mock_input):
        """Test main loop handles invalid input."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            main()
            output = fake_output.getvalue()
            self.assertIn("Invalid input! Use W/A/S/D/H/R to move or Q to quit.", output)
    
    @patch('main.print_instructions')
    def test_main_restart_during_game(self, mock_instructions):
        """Test restart functionality during gameplay."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            with patch('main.get_user_input', side_effect=['R', 'Q']):
                with patch('builtins.input', return_value='y'):  # Confirm restart
                    main()
                    output = fake_output.getvalue()
                    self.assertIn("Game restarted!", output)
    
    @patch('main.print_instructions')
    def test_main_restart_cancelled(self, mock_instructions):
        """Test restart cancellation during gameplay."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            with patch('main.get_user_input', side_effect=['R', 'Q']):
                with patch('builtins.input', return_value='n'):  # Don't confirm restart
                    main()
                    output = fake_output.getvalue()
                    self.assertNotIn("Game restarted!", output)
    
    @patch('main.print_instructions')
    def test_main_ai_hint_functionality(self, mock_instructions):
        """Test AI hint functionality with H key."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            with patch('main.get_user_input', side_effect=['H', 'Q']):
                # Create a mock game and AI
                with patch('main.Game2048') as mock_game_class:
                    mock_game = MagicMock()
                    mock_game.has_won.return_value = False
                    mock_game.is_game_over.return_value = False
                    
                    # Mock the AI
                    mock_ai = MagicMock()
                    mock_ai.get_best_move.return_value = 'up'
                    mock_game.get_ai.return_value = mock_ai
                    mock_game_class.return_value = mock_game
                    
                    main()
                    output = fake_output.getvalue()
                    
                    self.assertIn(" Heuristic-Model Suggestion: W (Up)", output)
                    mock_game.get_ai.assert_called_once()
                    mock_ai.get_best_move.assert_called_once()
    
    @patch('main.print_instructions')
    def test_main_ai_hint_no_moves_available(self, mock_instructions):
        """Test AI hint when no moves are available."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            with patch('main.get_user_input', side_effect=['H', 'Q']):
                # Create a mock game where AI returns no moves
                with patch('main.Game2048') as mock_game_class:
                    mock_game = MagicMock()
                    mock_game.has_won.return_value = False
                    mock_game.is_game_over.return_value = False
                    
                    # Mock the AI to return None (no moves available)
                    mock_ai = MagicMock()
                    mock_ai.get_best_move.return_value = None
                    mock_game.get_ai.return_value = mock_ai
                    mock_game_class.return_value = mock_game
                    
                    main()
                    output = fake_output.getvalue()
                    
                    self.assertIn(" Heuristic-Model Suggestion: No moves available!", output)
                    mock_game.get_ai.assert_called_once()
                    mock_ai.get_best_move.assert_called_once()
    
    @patch('main.print_instructions')  
    def test_main_ai_hint_all_directions(self, mock_instructions):
        """Test AI hint displays correct format for all directions."""
        directions = [
            ('up', 'W (Up)'),
            ('left', 'A (Left)'),
            ('down', 'S (Down)'),
            ('right', 'D (Right)')
        ]
        
        for ai_direction, expected_display in directions:
            with self.subTest(direction=ai_direction):
                with patch('sys.stdout', new=StringIO()) as fake_output:
                    with patch('main.get_user_input', side_effect=['H', 'Q']):
                        with patch('main.Game2048') as mock_game_class:
                            mock_game = MagicMock()
                            mock_game.has_won.return_value = False
                            mock_game.is_game_over.return_value = False
                            
                            mock_ai = MagicMock()
                            mock_ai.get_best_move.return_value = ai_direction
                            mock_game.get_ai.return_value = mock_ai
                            mock_game_class.return_value = mock_game
                            
                            main()
                            output = fake_output.getvalue()
                            
                            self.assertIn(f" Heuristic-Model Suggestion: {expected_display}", output)


class TestGameOverScenarios(unittest.TestCase):
    """Test cases for game over and win scenarios."""
    
    @patch('main.print_instructions')
    @patch('builtins.input', return_value='n')  # Don't restart after game over
    def test_game_over_no_restart(self, mock_restart_input, mock_instructions):
        """Test game over scenario when user chooses not to restart."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            # Create a mock game that's immediately over
            with patch('main.Game2048') as mock_game_class:
                mock_game = MagicMock()
                mock_game.has_won.return_value = False
                mock_game.is_game_over.return_value = True
                mock_game.get_score.return_value = 1234
                mock_game_class.return_value = mock_game
                
                main()
                output = fake_output.getvalue()
                
                self.assertIn("Game Over! No more moves possible.", output)
                self.assertIn("Final Score: 1234", output)
    
    @patch('main.print_instructions')
    @patch('builtins.input', side_effect=['y', 'Q'])  # Restart after game over, then quit
    def test_game_over_with_restart(self, mock_input, mock_instructions):
        """Test game over scenario when user chooses to restart."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            with patch('main.get_user_input', return_value='Q'):  # Quit after restart
                # Create a mock game that's over on first check but not after restart
                with patch('main.Game2048') as mock_game_class:
                    mock_game = MagicMock()
                    # First call: game over, second call: not game over (after restart)
                    mock_game.has_won.return_value = False
                    mock_game.is_game_over.side_effect = [True, False]
                    mock_game.get_score.return_value = 1234
                    mock_game_class.return_value = mock_game
                    
                    main()
                    output = fake_output.getvalue()
                    
                    self.assertIn("Game Over! No more moves possible.", output)
                    self.assertIn("Game restarted!", output)
                    mock_game.restart_game.assert_called_once()
    
    @patch('main.print_instructions')
    @patch('builtins.input', return_value='n')  # Don't continue after win
    def test_win_scenario_no_continue(self, mock_continue_input, mock_instructions):
        """Test win scenario when user chooses not to continue."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            # Create a mock game that has won
            with patch('main.Game2048') as mock_game_class:
                mock_game = MagicMock()
                mock_game.has_won.return_value = True
                mock_game.is_game_over.return_value = False
                mock_game_class.return_value = mock_game
                
                main()
                output = fake_output.getvalue()
                
                self.assertIn("Congratulations! You reached 2048! You won!", output)
    
    @patch('main.print_instructions')
    @patch('builtins.input', side_effect=['y', 'Q'])  # Continue after win, then quit
    def test_win_scenario_continue(self, mock_continue_input, mock_instructions):
        """Test win scenario when user chooses to continue playing."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            with patch('main.get_user_input', return_value='Q'):  # Quit after continuing
                # Create a mock game that has won but continues
                with patch('main.Game2048') as mock_game_class:
                    mock_game = MagicMock()
                    # First call: won, second call: not won (continuing play)
                    mock_game.has_won.side_effect = [True, False]
                    mock_game.is_game_over.return_value = False
                    mock_game_class.return_value = mock_game
                    
                    main()
                    output = fake_output.getvalue()
                    
                    self.assertIn("Congratulations! You reached 2048! You won!", output)


class TestMovementFeedback(unittest.TestCase):
    """Test cases for movement feedback."""
    
    @patch('main.print_instructions')
    def test_no_movement_feedback(self, mock_instructions):
        """Test feedback when no tiles move."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            with patch('main.get_user_input', side_effect=['W', 'Q']):
                # Create a mock game where move returns False (no movement)
                with patch('main.Game2048') as mock_game_class:
                    mock_game = MagicMock()
                    mock_game.has_won.return_value = False
                    mock_game.is_game_over.return_value = False
                    mock_game.move_up.return_value = False  # No movement
                    mock_game.display_game.return_value = None  # No board changes
                    mock_game_class.return_value = mock_game
                    
                    main()
                    output = fake_output.getvalue()
                    
                    self.assertIn("No tiles moved! Try a different direction.", output)
    
    @patch('main.print_instructions')
    def test_successful_movement_no_feedback(self, mock_instructions):
        """Test that successful movement doesn't show 'no movement' feedback."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            with patch('main.get_user_input', side_effect=['A', 'Q']):
                # Create a mock game where move returns True (successful movement)
                with patch('main.Game2048') as mock_game_class:
                    mock_game = MagicMock()
                    mock_game.has_won.return_value = False
                    mock_game.is_game_over.return_value = False
                    mock_game.move_left.return_value = True  # Successful movement
                    mock_game_class.return_value = mock_game
                    
                    main()
                    output = fake_output.getvalue()
                    
                    self.assertNotIn("No tiles moved! Try a different direction.", output)


if __name__ == '__main__':
    unittest.main()