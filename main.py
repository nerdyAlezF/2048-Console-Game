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
    print("  R - Restart Game")
    print("  Q - Quit Game")
    print("="*50)


def get_user_input():
    """Get and validate user input."""
    try:
        move = input("\nEnter your move (W/A/S/D/R/Q): ").strip().upper()
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
        elif move == 'W':
            moved = game.move_up()
        elif move == 'A':
            moved = game.move_left()
        elif move == 'S':
            moved = game.move_down()
        elif move == 'D':
            moved = game.move_right()
        else:
            print("Invalid input! Use W/A/S/D/R to move or Q to quit.")
            continue
        
        # Provide feedback if no movement occurred
        if not moved:
            print("No tiles moved! Try a different direction.")


if __name__ == "__main__":
    main()