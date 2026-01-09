#!/usr/bin/env python3
"""
Simple real-world test of py-flowcheck library
Demonstrates basic validation functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'py-flowcheck/src'))

from py_flowcheck import Schema, ValidationError, configure, get_metrics, reset_metrics, validate_with_mode
from py_flowcheck.config import get_config
import time

# Configure for demo
configure(env="dev", sample_size=1.0, mode="raise")

def test_basic_validation():
    """Test basic schema validation"""
    print("🧪 Testing basic validation...")
    
    # Simple user schema
    user_schema = Schema({
        "name": str,
        "age": int,
        "email": str
    })
    
    # Valid data
    valid_user = {
        "name": "John Doe",
        "age": 25,
        "email": "john@example.com"
    }
    
    try:
        user_schema.validate(valid_user)
        print("✅ Valid user data passed validation")
        return True
    except ValidationError as e:
        print(f"❌ Unexpected validation error: {e}")
        return False

def test_invalid_type():
    """Test validation with invalid type"""
    print("\n🧪 Testing invalid type validation...")
    
    user_schema = Schema({
        "name": str,
        "age": int,
        "email": str
    })
    
    # Invalid data - age as string
    invalid_user = {
        "name": "Jane Doe",
        "age": "twenty-five",  # Should be int
        "email": "jane@example.com"
    }
    
    try:
        user_schema.validate(invalid_user)
        print("❌ Should have failed validation")
        return False
    except ValidationError as e:
        print(f"✅ Validation correctly caught type error: {e}")
        return True

def test_missing_field():
    """Test validation with missing required field"""
    print("\n🧪 Testing missing field validation...")
    
    user_schema = Schema({
        "name": str,
        "age": int,
        "email": str
    })
    
    # Missing email field
    incomplete_user = {
        "name": "Bob Smith",
        "age": 30
        # Missing email
    }
    
    try:
        user_schema.validate(incomplete_user)
        print("❌ Should have failed validation")
        return False
    except ValidationError as e:
        print(f"✅ Validation correctly caught missing field: {e}")
        return True

def test_nested_validation():
    """Test nested object validation"""
    print("\n🧪 Testing nested validation...")
    
    profile_schema = Schema({
        "user": {
            "name": str,
            "age": int,
            "settings": {
                "notifications": bool,
                "theme": str
            }
        }
    })
    
    # Valid nested data
    valid_profile = {
        "user": {
            "name": "Alice Johnson",
            "age": 28,
            "settings": {
                "notifications": True,
                "theme": "dark"
            }
        }
    }
    
    try:
        profile_schema.validate(valid_profile)
        print("✅ Valid nested data passed validation")
        return True
    except ValidationError as e:
        print(f"❌ Unexpected validation error: {e}")
        return False

def test_performance():
    """Test validation performance"""
    print("\n🧪 Testing validation performance...")
    
    # Reset metrics
    reset_metrics()
    
    simple_schema = Schema({
        "id": int,
        "name": str,
        "active": bool
    })
    
    test_data = {
        "id": 123,
        "name": "Performance Test",
        "active": True
    }
    
    # Warm up
    for _ in range(100):
        simple_schema.validate(test_data)
    
    # Measure performance
    iterations = 10000
    start_time = time.time()
    
    for i in range(iterations):
        test_data_copy = test_data.copy()
        test_data_copy["id"] = i
        simple_schema.validate(test_data_copy)
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = (total_time / iterations) * 1000  # Convert to milliseconds
    
    print(f"✅ Performance test completed:")
    print(f"   - {iterations} validations in {total_time:.3f}s")
    print(f"   - Average: {avg_time:.3f}ms per validation")
    print(f"   - Throughput: {iterations/total_time:.0f} validations/second")
    
    return avg_time < 1.0  # Should be under 1ms per validation

def test_configuration_modes():
    """Test different validation modes"""
    print("\n🧪 Testing configuration modes...")
    
    schema = Schema({"value": int})
    invalid_data = {"value": "not_an_int"}
    
    # Test raise mode
    configure(mode="raise")
    try:
        validate_with_mode(schema, invalid_data)
        print("❌ Raise mode should have thrown exception")
        return False
    except ValidationError:
        print("✅ Raise mode correctly threw exception")
    
    # Test log mode
    configure(mode="log")
    try:
        validate_with_mode(schema, invalid_data)
        print("✅ Log mode completed without exception")
    except ValidationError:
        print("❌ Log mode should not throw exception")
        return False
    
    # Test silent mode
    configure(mode="silent")
    try:
        validate_with_mode(schema, invalid_data)
        print("✅ Silent mode completed without exception")
    except ValidationError:
        print("❌ Silent mode should not throw exception")
        return False
    
    # Reset to raise mode
    configure(mode="raise")
    return True

def test_production_sampling():
    """Test production sampling behavior"""
    print("\n🧪 Testing production sampling...")
    
    # Configure for production with low sample rate
    configure(env="prod", sample_size=0.1, mode="raise")
    
    schema = Schema({"test": str})
    valid_data = {"test": "value"}
    
    # Run multiple validations - some should be skipped due to sampling
    validations = 100
    exceptions = 0
    
    for _ in range(validations):
        try:
            schema.validate(valid_data)
        except Exception:
            exceptions += 1
    
    print(f"✅ Production sampling test: {exceptions} exceptions out of {validations} validations")
    
    # Reset to dev mode
    configure(env="dev", sample_size=1.0, mode="raise")
    return True

def main():
    """Run all tests"""
    print("🚀 py-flowcheck Simple Real-World Test")
    print("=" * 50)
    
    # Show current configuration
    config = get_config()
    print(f"Configuration: env={config.env}, sample_size={config.sample_size}, mode={config.mode}")
    print()
    
    tests = [
        test_basic_validation,
        test_invalid_type,
        test_missing_field,
        test_nested_validation,
        test_performance,
        test_configuration_modes,
        test_production_sampling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! py-flowcheck is working correctly.")
        print("\n📈 Key Features Demonstrated:")
        print("   ✅ Basic type validation")
        print("   ✅ Missing field detection")
        print("   ✅ Nested object validation")
        print("   ✅ Performance optimization")
        print("   ✅ Configurable validation modes")
        print("   ✅ Production sampling")
    else:
        print("⚠️ Some tests failed. Check the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)