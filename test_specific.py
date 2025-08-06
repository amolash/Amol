#!/usr/bin/env python3
"""
Specific test runner demonstrating different testing approaches
"""

import unittest
import sys
from simple_test import TestProduct, TestShoppingCart, TestIntegration


def run_specific_test_class(test_class):
    """Run tests for a specific class"""
    print(f"\n{'='*60}")
    print(f"Running tests for {test_class.__name__}")
    print(f"{'='*60}")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def run_specific_test_method(test_class, method_name):
    """Run a specific test method"""
    print(f"\n{'='*60}")
    print(f"Running {test_class.__name__}.{method_name}")
    print(f"{'='*60}")
    
    suite = unittest.TestSuite()
    suite.addTest(test_class(method_name))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def run_test_discovery():
    """Demonstrate test discovery"""
    print(f"\n{'='*60}")
    print("Running test discovery")
    print(f"{'='*60}")
    
    loader = unittest.TestLoader()
    # Discover tests in current directory
    suite = loader.discover('.', pattern='*test*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def main():
    """Main test runner with options"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'product':
            success = run_specific_test_class(TestProduct)
        elif command == 'cart':
            success = run_specific_test_class(TestShoppingCart)
        elif command == 'integration':
            success = run_specific_test_class(TestIntegration)
        elif command == 'discount':
            success = run_specific_test_method(TestProduct, 'test_discount_calculation_valid')
        elif command == 'discovery':
            success = run_test_discovery()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: product, cart, integration, discount, discovery")
            return 1
    else:
        print("Test Runner - Choose a specific test to run:")
        print("Usage: python3 test_specific.py [command]")
        print("\nAvailable commands:")
        print("  product     - Run all Product tests")
        print("  cart        - Run all ShoppingCart tests") 
        print("  integration - Run all Integration tests")
        print("  discount    - Run specific discount test")
        print("  discovery   - Run test discovery")
        print("\nExample: python3 test_specific.py product")
        return 0
    
    return 0 if success else 1


if __name__ == '__main__':
    exit(main())