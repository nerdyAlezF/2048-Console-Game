import unittest
import sys
import os

# Add parent directory to path to import game module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all test modules
from .test_initialization import TestGameInitialization, TestGameStateManagement
from .test_helper_methods import TestHelperMethods, TestBoardOperations
from .test_movement import TestMovement
from .test_main import TestMainCLI, TestMainGameLoop, TestGameOverScenarios, TestMovementFeedback
from .test_integration import TestIntegration
from .test_game_ai import TestBestMoveSelection, TestBoardEvaluation, TestGameAI, TestGameIntegration, TestMonotonicityAndCornerHeuristics
from .test_claude_ai import TestClaudeAI


def create_test_suite():
    """Create a test suite combining all test classes."""
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGameInitialization))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGameStateManagement))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestHelperMethods))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBoardOperations))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMovement))
    # Heuristic Eval
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBestMoveSelection))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBoardEvaluation))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestGameAI))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestGameIntegration))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMonotonicityAndCornerHeuristics))
    
    # Add Claude AI tests
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestClaudeAI))
    
    # Add main CLI test classes
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMainCLI))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMainGameLoop))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGameOverScenarios))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMovementFeedback))
    
    # Add integration tests
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestIntegration))
    
    return suite


if __name__ == '__main__':
    # Run the combined test suite
    runner = unittest.TextTestRunner(verbosity=2)
    suite = create_test_suite()
    runner.run(suite)