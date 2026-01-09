#!/usr/bin/env python3
"""
Real-world test of py-flowcheck library
Demonstrates validation in a typical web API scenario
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'py-flowcheck/src'))

from py_flowcheck import Schema, check_input, check_output, configure
from py_flowcheck.config import get_config
import time
import json

# Configure for demo
configure(env="dev", sample_size=1.0, mode="raise")

# Define schemas for a user management API
user_schema = Schema({
    "username": {"type": "string", "min_length": 3, "max_length": 20},
    "email": {"type": "string", "pattern": r"^[^@]+@[^@]+\.[^@]+$"},
    "age": {"type": "integer", "min": 13, "max": 120},
    "profile": {
        "type": "object",
        "properties": {
            "bio": {"type": "string", "max_length": 500},
            "interests": {"type": "array", "items": {"type": "string"}},
            "settings": {
                "type": "object", 
                "properties": {
                    "notifications": {"type": "boolean"},
                    "privacy": {"type": "string", "enum": ["public", "private", "friends"]}
                }
            }
        }
    }
})

response_schema = Schema({
    "id": {"type": "integer"},
    "username": {"type": "string"},
    "created_at": {"type": "string"},
    "status": {"type": "string", "enum": ["active", "pending", "suspended"]}
})

# Simulated database
users_db = []
next_id = 1

@check_input(user_schema, source="args")
@check_output(response_schema)
def create_user(data):
    """Create a new user with validation"""
    global next_id
    
    # Simulate user creation
    new_user = {
        "id": next_id,
        "username": data["username"],
        "created_at": "2024-01-15T10:30:00Z",
        "status": "active"
    }
    
    users_db.append({**data, **new_user})
    next_id += 1
    
    return new_user

def test_valid_user():
    """Test with valid user data"""
    print("🧪 Testing valid user creation...")
    
    valid_user = {
        "username": "johndoe",
        "email": "john@example.com",
        "age": 25,
        "profile": {
            "bio": "Software developer passionate about Python",
            "interests": ["coding", "music", "travel"],
            "settings": {
                "notifications": True,
                "privacy": "public"
            }
        }
    }
    
    try:
        result = create_user(valid_user)
        print(f"✅ User created successfully: {result}")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_invalid_email():
    """Test with invalid email"""
    print("\n🧪 Testing invalid email...")
    
    invalid_user = {
        "username": "jane",
        "email": "invalid-email",  # Invalid email format
        "age": 30,
        "profile": {
            "bio": "Designer",
            "interests": ["design", "art"],
            "settings": {
                "notifications": False,
                "privacy": "private"
            }
        }
    }
    
    try:
        result = create_user(invalid_user)
        print("❌ Should have failed validation")
        return False
    except Exception as e:
        print(f"✅ Validation caught invalid email: {e}")
        return True

def test_missing_required_field():
    """Test with missing required field"""
    print("\n🧪 Testing missing required field...")
    
    incomplete_user = {
        "username": "bob",
        "email": "bob@example.com",
        # Missing age field
        "profile": {
            "bio": "Student",
            "interests": ["learning"],
            "settings": {
                "notifications": True,
                "privacy": "friends"
            }
        }
    }
    
    try:
        result = create_user(incomplete_user)
        print("❌ Should have failed validation")
        return False
    except Exception as e:
        print(f"✅ Validation caught missing field: {e}")
        return True

def test_invalid_nested_enum():
    """Test with invalid nested enum value"""
    print("\n🧪 Testing invalid nested enum...")
    
    user_with_invalid_enum = {
        "username": "alice",
        "email": "alice@example.com",
        "age": 28,
        "profile": {
            "bio": "Marketing specialist",
            "interests": ["marketing", "photography"],
            "settings": {
                "notifications": True,
                "privacy": "invalid_privacy_level"  # Invalid enum value
            }
        }
    }
    
    try:
        result = create_user(user_with_invalid_enum)
        print("❌ Should have failed validation")
        return False
    except Exception as e:
        print(f"✅ Validation caught invalid enum: {e}")
        return True

def test_performance():
    """Test validation performance"""
    print("\n🧪 Testing validation performance...")
    
    test_user = {
        "username": "speedtest",
        "email": "speed@test.com",
        "age": 25,
        "profile": {
            "bio": "Performance testing user",
            "interests": ["testing", "performance"],
            "settings": {
                "notifications": True,
                "privacy": "public"
            }
        }
    }
    
    # Warm up
    for _ in range(10):
        create_user(test_user.copy())
    
    # Measure performance
    iterations = 1000
    start_time = time.time()
    
    for i in range(iterations):
        test_user_copy = test_user.copy()
        test_user_copy["username"] = f"user_{i}"
        test_user_copy["email"] = f"user_{i}@test.com"
        create_user(test_user_copy)
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = (total_time / iterations) * 1000  # Convert to milliseconds
    
    print(f"✅ Performance test completed:")
    print(f"   - {iterations} validations in {total_time:.3f}s")
    print(f"   - Average: {avg_time:.3f}ms per validation")
    print(f"   - Throughput: {iterations/total_time:.0f} validations/second")
    
    return avg_time < 1.0  # Should be under 1ms per validation

def main():
    """Run all tests"""
    print("🚀 py-flowcheck Real-World Test Suite")
    print("=" * 50)
    
    # Show current configuration
    config = get_config()
    print(f"Configuration: env={config.env}, sample_size={config.sample_size}, mode={config.mode}")
    print()
    
    tests = [
        test_valid_user,
        test_invalid_email,
        test_missing_required_field,
        test_invalid_nested_enum,
        test_performance
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! py-flowcheck is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above.")
    
    print(f"\n📈 Database now contains {len(users_db)} users")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)