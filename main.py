#!/usr/bin/env python3
"""
2048 Game - Command Line Interface
"""

from game.game2048 import Game2048
import sys


def print_instructions():
    """Print game instructions."""
    print("\n" + "="*50)
    print("Welcome to 2048!")
    print("="*50)
    print("Use WASD to move tiles:")
    print("  W - Move Up")
    print("  A - Move Left") 
    print("  S - Move Down")
    print("  D - Move Right")
    print("  H - Local Model Hint (get move suggestion)")
    print("  C - Claude AI Hint (requires API key)")
    print("  R - Restart Game")
    print("  Q - Quit Game")
    print("="*50)


def get_user_input():
    """Get and validate user input."""
    try:
        move = input("\nEnter your move (W/A/S/D/H/C/R/Q): ").strip().upper()
        return move
    except (KeyboardInterrupt, EOFError):
        print("\nGame interrupted. Goodbye!")
        sys.exit(0)


def main():
    """Main game loop."""
    game = Game2048()
    print_instructions()
    
    while True:
        # Display current game state
        print("\n")
        game.display_game()
        print("Controls: W/A/S/D=Move  H=Local Model Hint  C=Claude AI  R=Restart  Q=Quit")
        
        # Check win condition
        if game.has_won():
            print("\nCongratulations! You reached 2048! You won!")
            play_again = input("Continue playing? (y/n): ").strip().lower()
            if play_again != 'y':
                break
        
        # Check game over condition
        if game.is_game_over():
            print("\nGame Over! No more moves possible.")
            print(f"Final Score: {game.get_score()}")
            restart = input("Restart game? (y/n): ").strip().lower()
            if restart == 'y':
                game.restart_game()
                print("\nGame restarted!")
                continue
            else:
                break
        
        # Get user input
        move = get_user_input()
        
        # Process move
        if move == 'Q':
            print("Thanks for playing!")
            break
        elif move == 'R':
            confirm = input("Are you sure you want to restart? (y/n): ").strip().lower()
            if confirm == 'y':
                game.restart_game()
                print("\nGame restarted!")
            continue
        elif move == 'H':
            # Get AI hint
            ai = game.get_ai()
            best_move = ai.get_best_move()
            if best_move:
                move_names = {
                    'up': 'W (Up)',
                    'left': 'A (Left)', 
                    'down': 'S (Down)',
                    'right': 'D (Right)'
                }
                print(f"\n Local Model Suggestion: {move_names[best_move]}")
            else:
                print("\n Local Model Suggestion: No moves available!")
            continue
        elif move == 'C':
            # Get Claude AI hint
            claude_ai = game.get_claude_ai()
            if not claude_ai.is_available():
                print("\n Claude AI: Not available")
                print("   • Install: pip install anthropic")
                print("   • Set ANTHROPIC_API_KEY environment variable")
                continue
            
            print("\n Claude AI: Analyzing board state...")
            best_move = claude_ai.get_best_move()
            if best_move:
                move_names = {
                    'up': 'W (Up)',
                    'left': 'A (Left)', 
                    'down': 'S (Down)',
                    'right': 'D (Right)'
                }
                print(f" Claude AI Suggestion: {move_names[best_move]}")
            else:
                print(" Claude AI: Unable to get suggestion (API error or no moves available)")
            continue
        elif move == 'W':
            moved = game.move_up()
        elif move == 'A':
            moved = game.move_left()
        elif move == 'S':
            moved = game.move_down()
        elif move == 'D':
            moved = game.move_right()
        else:
            print("Invalid input! Use W/A/S/D/H/C/R to move or Q to quit.")
            continue
        
        # Provide feedback if no movement occurred
        if not moved:
            print("No tiles moved! Try a different direction.")


if __name__ == "__main__":
    main()