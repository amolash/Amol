#!/usr/bin/env python3
"""
Simple test script to demonstrate testing capabilities
This script tests basic shopping cart functionality without Django dependencies
"""

import unittest
from decimal import Decimal


class Product:
    """Simple Product class for testing"""
    def __init__(self, name, price, description=""):
        self.name = name
        self.price = Decimal(str(price))
        self.description = description
    
    def __str__(self):
        return self.name
    
    def get_discounted_price(self, discount_percent):
        """Calculate discounted price"""
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount percent must be between 0 and 100")
        discount_amount = self.price * (Decimal(discount_percent) / 100)
        result = self.price - discount_amount
        # Round to 2 decimal places for currency
        return result.quantize(Decimal('0.01'))


class ShoppingCart:
    """Simple shopping cart for testing"""
    def __init__(self):
        self.items = []
    
    def add_item(self, product, quantity=1):
        """Add item to cart"""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.items.append({'product': product, 'quantity': quantity})
    
    def get_total(self):
        """Calculate total price"""
        total = Decimal('0')
        for item in self.items:
            total += item['product'].price * item['quantity']
        return total
    
    def get_item_count(self):
        """Get total number of items"""
        return sum(item['quantity'] for item in self.items)
    
    def clear(self):
        """Clear the cart"""
        self.items = []


class TestProduct(unittest.TestCase):
    """Test cases for Product class"""
    
    def setUp(self):
        """Set up test data"""
        self.product = Product("Test Product", 29.99, "A test product")
    
    def test_product_creation(self):
        """Test product creation"""
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, Decimal('29.99'))
        self.assertEqual(self.product.description, "A test product")
    
    def test_product_str_representation(self):
        """Test string representation"""
        self.assertEqual(str(self.product), "Test Product")
    
    def test_discount_calculation_valid(self):
        """Test valid discount calculation"""
        discounted_price = self.product.get_discounted_price(10)
        expected = Decimal('26.99')
        self.assertEqual(discounted_price, expected)
    
    def test_discount_calculation_zero(self):
        """Test zero discount"""
        discounted_price = self.product.get_discounted_price(0)
        self.assertEqual(discounted_price, self.product.price)
    
    def test_discount_calculation_full(self):
        """Test 100% discount"""
        discounted_price = self.product.get_discounted_price(100)
        self.assertEqual(discounted_price, Decimal('0'))
    
    def test_discount_invalid_negative(self):
        """Test invalid negative discount"""
        with self.assertRaises(ValueError):
            self.product.get_discounted_price(-10)
    
    def test_discount_invalid_over_100(self):
        """Test invalid discount over 100%"""
        with self.assertRaises(ValueError):
            self.product.get_discounted_price(150)


class TestShoppingCart(unittest.TestCase):
    """Test cases for ShoppingCart class"""
    
    def setUp(self):
        """Set up test data"""
        self.cart = ShoppingCart()
        self.product1 = Product("Product 1", 10.00)
        self.product2 = Product("Product 2", 20.00)
    
    def test_empty_cart(self):
        """Test empty cart"""
        self.assertEqual(self.cart.get_total(), Decimal('0'))
        self.assertEqual(self.cart.get_item_count(), 0)
    
    def test_add_single_item(self):
        """Test adding single item"""
        self.cart.add_item(self.product1, 1)
        self.assertEqual(self.cart.get_total(), Decimal('10.00'))
        self.assertEqual(self.cart.get_item_count(), 1)
    
    def test_add_multiple_items(self):
        """Test adding multiple items"""
        self.cart.add_item(self.product1, 2)
        self.cart.add_item(self.product2, 1)
        expected_total = Decimal('40.00')  # (10*2) + (20*1)
        self.assertEqual(self.cart.get_total(), expected_total)
        self.assertEqual(self.cart.get_item_count(), 3)
    
    def test_add_item_zero_quantity(self):
        """Test adding item with zero quantity"""
        with self.assertRaises(ValueError):
            self.cart.add_item(self.product1, 0)
    
    def test_add_item_negative_quantity(self):
        """Test adding item with negative quantity"""
        with self.assertRaises(ValueError):
            self.cart.add_item(self.product1, -1)
    
    def test_clear_cart(self):
        """Test clearing cart"""
        self.cart.add_item(self.product1, 2)
        self.cart.add_item(self.product2, 1)
        self.cart.clear()
        self.assertEqual(self.cart.get_total(), Decimal('0'))
        self.assertEqual(self.cart.get_item_count(), 0)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_shopping_scenario(self):
        """Test complete shopping scenario"""
        # Create products
        laptop = Product("Laptop", 999.99, "Gaming laptop")
        mouse = Product("Mouse", 25.50, "Wireless mouse")
        keyboard = Product("Keyboard", 75.00, "Mechanical keyboard")
        
        # Create cart and add items
        cart = ShoppingCart()
        cart.add_item(laptop, 1)
        cart.add_item(mouse, 2)
        cart.add_item(keyboard, 1)
        
        # Check totals
        expected_total = Decimal('999.99') + (Decimal('25.50') * 2) + Decimal('75.00')
        self.assertEqual(cart.get_total(), expected_total)
        self.assertEqual(cart.get_item_count(), 4)
        
        # Test discount on laptop
        discounted_laptop_price = laptop.get_discounted_price(10)
        expected_discounted = Decimal('899.99')
        self.assertEqual(discounted_laptop_price, expected_discounted)
    
    def test_bulk_discount_calculation(self):
        """Test bulk discount scenarios"""
        products = []
        for i in range(5):
            product = Product(f"Product {i+1}", (i+1)*10)
            products.append(product)
        
        cart = ShoppingCart()
        for i, product in enumerate(products):
            cart.add_item(product, i+1)  # Add 1, 2, 3, 4, 5 items respectively
        
        # Expected: (10*1) + (20*2) + (30*3) + (40*4) + (50*5) = 550
        expected_total = Decimal('550')
        self.assertEqual(cart.get_total(), expected_total)


if __name__ == '__main__':
    print("Running Shopping App Tests...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestProduct))
    suite.addTests(loader.loadTestsFromTestCase(TestShoppingCart))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\nAll tests passed! ✅")
    else:
        print("\nSome tests failed! ❌")
    
    exit(0 if result.wasSuccessful() else 1)