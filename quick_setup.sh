#!/bin/bash
# Quick setup script for testing py-flowcheck

echo "🚀 Setting up py-flowcheck for testing..."

# Install from PyPI
pip install pyflowcheck-validation

# Create a simple test file
cat > test_pyflowcheck.py << 'EOF'
from py_flowcheck import Schema, ValidationError

# Simple test
print("🧪 Testing py-flowcheck...")

# Create a user schema
user_schema = Schema({
    "name": str,
    "age": int,
    "email": str
})

# Test valid data
print("\n✅ Testing valid data:")
valid_user = {"name": "Alice", "age": 25, "email": "alice@example.com"}
try:
    user_schema.validate(valid_user)
    print(f"   Valid: {valid_user}")
except ValidationError as e:
    print(f"   Error: {e}")

# Test invalid data
print("\n❌ Testing invalid data:")
invalid_user = {"name": "Bob", "age": "twenty", "email": "bob@example.com"}
try:
    user_schema.validate(invalid_user)
    print(f"   Should have failed: {invalid_user}")
except ValidationError as e:
    print(f"   Caught error correctly: {e}")

print("\n🎉 py-flowcheck is working!")
EOF

echo "✅ Setup complete! Run: python test_pyflowcheck.py"