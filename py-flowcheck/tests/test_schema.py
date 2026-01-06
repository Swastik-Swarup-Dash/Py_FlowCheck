from py_flowcheck import Schema, check_input

# Define a sample schema for testing
user_schema = Schema({
    "id": int,
    "email": {"type": str, "regex": r".+@.+\..+"},
    "age": {"type": int, "nullable": True, "min": 0},
})

def test_schema_validation_valid():
    valid_data = {
        "id": 1,
        "email": "test@example.com",
        "age": 30
    }
    violations = user_schema.validate(valid_data)
    assert not violations, f"Expected no violations, but got: {violations}"

def test_schema_validation_invalid_email():
    invalid_data = {
        "id": 1,
        "email": "invalid-email",
        "age": 30
    }
    violations = user_schema.validate(invalid_data)
    assert violations, "Expected violations for invalid email"

def test_schema_validation_missing_required_field():
    invalid_data = {
        "email": "test@example.com",
        "age": 30
    }
    violations = user_schema.validate(invalid_data)
    assert violations, "Expected violations for missing required field 'id'"

def test_schema_validation_nullable_field():
    valid_data = {
        "id": 1,
        "email": "test@example.com",
        "age": None
    }
    violations = user_schema.validate(valid_data)
    assert not violations, f"Expected no violations, but got: {violations}"

def test_schema_validation_invalid_age():
    invalid_data = {
        "id": 1,
        "email": "test@example.com",
        "age": -1
    }
    violations = user_schema.validate(invalid_data)
    assert violations, "Expected violations for invalid age"