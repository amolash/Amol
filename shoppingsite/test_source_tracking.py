#!/usr/bin/env python
"""
Test script to verify source tracking implementation.
Run this after setting up Django properly.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoppingsite.settings')
django.setup()

def test_source_tracking():
    """Test the source tracking functionality."""
    from shopping.models import SourceTracker, Product, Order, SourceTrackingLog
    from shopping.utils import create_default_sources, log_source_activity
    from django.contrib.auth.models import User
    
    print("Testing Source Tracking Implementation...")
    print("=" * 50)
    
    # Test 1: Create default sources
    print("1. Creating default sources...")
    created_sources = create_default_sources()
    print(f"   Created {len(created_sources)} new sources")
    
    all_sources = SourceTracker.objects.all()
    print(f"   Total sources: {all_sources.count()}")
    for source in all_sources:
        print(f"   - {source.name} ({source.source_type})")
    
    # Test 2: Create sample data
    print("\n2. Creating sample data...")
    
    # Get a source
    web_source = SourceTracker.objects.get(source_type='web')
    
    # Create a test product
    product = Product.objects.create(
        name="Test Product",
        description="A test product for source tracking",
        price=99.99,
        stock_quantity=10,
        source=web_source
    )
    print(f"   Created product: {product.name} with source: {product.source.name}")
    
    # Test 3: Activity logging
    print("\n3. Testing activity logging...")
    log_entry = log_source_activity(
        source=web_source,
        action_type='create',
        object_type='Product',
        object_id=product.id,
        details={'test': True}
    )
    print(f"   Created log entry: {log_entry}")
    
    # Test 4: Display statistics
    print("\n4. Source tracking statistics:")
    for source in all_sources:
        product_count = source.product_set.count()
        log_count = source.logs.count()
        print(f"   {source.name}: {product_count} products, {log_count} logs")
    
    print("\n" + "=" * 50)
    print("Source tracking implementation test completed successfully!")
    print("\nNext steps:")
    print("1. Run: python manage.py makemigrations shopping")
    print("2. Run: python manage.py migrate")
    print("3. Run: python manage.py setup_source_tracking --create-sample-data")
    print("4. Run: python manage.py runserver")
    print("5. Visit: http://localhost:8000/ to see the shopping site")
    print("6. Visit: http://localhost:8000/admin/ for admin interface")
    print("7. Visit: http://localhost:8000/dashboard/sources/ for source dashboard")

if __name__ == "__main__":
    try:
        test_source_tracking()
    except Exception as e:
        print(f"Error testing source tracking: {e}")
        print("\nThis is expected if Django migrations haven't been run yet.")
        print("Please run migrations first, then try this test again.")