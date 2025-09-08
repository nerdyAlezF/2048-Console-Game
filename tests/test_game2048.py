import unittest
import sys
import os

# Add parent directory to path to import game module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all test modules
from .test_initialization import TestGameInitialization
from .test_helper_methods import TestHelperMethods
from .test_movement import TestMovement
from .test_main import TestMainCLI, TestMainGameLoop, TestGameOverScenarios, TestMovementFeedback


def create_test_suite():
    """Create a test suite combining all test classes."""
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGameInitialization))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestHelperMethods))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMovement))
    
    # Add main CLI test classes
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMainCLI))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMainGameLoop))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGameOverScenarios))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMovementFeedback))
    
    return suite


if __name__ == '__main__':
    # Run the combined test suite
    runner = unittest.TextTestRunner(verbosity=2)
    suite = create_test_suite()
    runner.run(suite)