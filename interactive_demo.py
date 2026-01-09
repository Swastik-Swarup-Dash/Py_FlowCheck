#!/usr/bin/env python3
"""
Interactive py-flowcheck Demo
Let your friends test the library with different scenarios
"""

try:
    from py_flowcheck import Schema, ValidationError, configure
    print("✅ py-flowcheck imported successfully!")
except ImportError:
    print("❌ py-flowcheck not found. Install with: pip install pyflowcheck-validation")
    exit(1)

def demo_basic_validation():
    """Demo basic validation"""
    print("\n" + "="*50)
    print("🧪 DEMO 1: Basic Validation")
    print("="*50)
    
    schema = Schema({
        "username": str,
        "age": int,
        "active": bool
    })
    
    test_cases = [
        {"username": "john", "age": 25, "active": True},  # Valid
        {"username": "jane", "age": "twenty", "active": True},  # Invalid age
        {"username": "bob", "active": False},  # Missing age
    ]
    
    for i, data in enumerate(test_cases, 1):
        print(f"\nTest {i}: {data}")
        try:
            schema.validate(data)
            print("   ✅ PASSED")
        except ValidationError as e:
            print(f"   ❌ FAILED: {e}")

def demo_nested_validation():
    """Demo nested object validation"""
    print("\n" + "="*50)
    print("🧪 DEMO 2: Nested Object Validation")
    print("="*50)
    
    schema = Schema({
        "user": {
            "name": str,
            "profile": {
                "bio": str,
                "settings": {
                    "theme": str,
                    "notifications": bool
                }
            }
        }
    })
    
    valid_data = {
        "user": {
            "name": "Alice",
            "profile": {
                "bio": "Software developer",
                "settings": {
                    "theme": "dark",
                    "notifications": True
                }
            }
        }
    }
    
    print(f"Testing: {valid_data}")
    try:
        schema.validate(valid_data)
        print("   ✅ Complex nested validation PASSED")
    except ValidationError as e:
        print(f"   ❌ FAILED: {e}")

def demo_performance():
    """Demo performance testing"""
    print("\n" + "="*50)
    print("🧪 DEMO 3: Performance Test")
    print("="*50)
    
    import time
    
    schema = Schema({
        "id": int,
        "name": str,
        "score": int
    })
    
    test_data = {"id": 1, "name": "test", "score": 100}
    
    # Performance test
    iterations = 10000
    start = time.time()
    
    for i in range(iterations):
        schema.validate(test_data)
    
    end = time.time()
    total_time = end - start
    avg_time = (total_time / iterations) * 1000
    
    print(f"   📊 {iterations} validations in {total_time:.3f}s")
    print(f"   📊 Average: {avg_time:.3f}ms per validation")
    print(f"   📊 Throughput: {iterations/total_time:.0f} validations/second")

def demo_configuration():
    """Demo different configuration modes"""
    print("\n" + "="*50)
    print("🧪 DEMO 4: Configuration Modes")
    print("="*50)
    
    from py_flowcheck import validate_with_mode
    
    schema = Schema({"value": int})
    invalid_data = {"value": "not_an_int"}
    
    modes = ["raise", "log", "silent"]
    
    for mode in modes:
        configure(mode=mode)
        print(f"\nTesting mode: {mode}")
        try:
            validate_with_mode(schema, invalid_data)
            print(f"   ✅ Mode '{mode}' handled gracefully")
        except ValidationError:
            print(f"   ❌ Mode '{mode}' raised exception")

def interactive_test():
    """Let user create their own test"""
    print("\n" + "="*50)
    print("🧪 DEMO 5: Create Your Own Test!")
    print("="*50)
    
    print("Let's create a simple schema together!")
    
    # Simple interactive schema builder
    schema_dict = {}
    
    while True:
        field = input("\nEnter field name (or 'done' to finish): ").strip()
        if field.lower() == 'done':
            break
        
        type_choice = input(f"Type for '{field}' (str/int/bool): ").strip().lower()
        if type_choice == 'str':
            schema_dict[field] = str
        elif type_choice == 'int':
            schema_dict[field] = int
        elif type_choice == 'bool':
            schema_dict[field] = bool
        else:
            print("Invalid type, using str")
            schema_dict[field] = str
    
    if schema_dict:
        schema = Schema(schema_dict)
        print(f"\n✅ Created schema: {schema_dict}")
        
        # Test with user data
        print("\nNow let's test it!")
        test_data = {}
        for field, field_type in schema_dict.items():
            value = input(f"Enter value for '{field}' ({field_type.__name__}): ")
            
            # Convert to appropriate type
            try:
                if field_type == int:
                    test_data[field] = int(value)
                elif field_type == bool:
                    test_data[field] = value.lower() in ['true', '1', 'yes']
                else:
                    test_data[field] = value
            except ValueError:
                test_data[field] = value  # Keep as string to test validation
        
        print(f"\nTesting data: {test_data}")
        try:
            schema.validate(test_data)
            print("   ✅ Your data is valid!")
        except ValidationError as e:
            print(f"   ❌ Validation failed: {e}")

def main():
    """Main demo function"""
    print("🎉 Welcome to py-flowcheck Interactive Demo!")
    print("This demo will show you how py-flowcheck works.")
    
    demos = [
        ("Basic Validation", demo_basic_validation),
        ("Nested Objects", demo_nested_validation),
        ("Performance Test", demo_performance),
        ("Configuration Modes", demo_configuration),
        ("Interactive Test", interactive_test),
    ]
    
    while True:
        print("\n" + "="*50)
        print("📋 Available Demos:")
        for i, (name, _) in enumerate(demos, 1):
            print(f"   {i}. {name}")
        print("   0. Exit")
        
        try:
            choice = int(input("\nChoose a demo (0-5): "))
            if choice == 0:
                print("👋 Thanks for trying py-flowcheck!")
                break
            elif 1 <= choice <= len(demos):
                demos[choice-1][1]()
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Please enter a number")
        except KeyboardInterrupt:
            print("\n👋 Thanks for trying py-flowcheck!")
            break

if __name__ == "__main__":
    main()