import re
import os
import functools
from typing import Any, Dict, Callable, Optional, List, Union

class ValidationError(Exception):
    """
    Custom exception raised when schema validation fails.
    """
    def __init__(self, message: str, violations: Optional[List[str]] = None):
        super().__init__(message)
        self.violations = violations or []


class Schema:
    """
    A class for defining and validating schemas for data validation.

    Example:
        user_schema = Schema({
            "id": int,
            "email": {"type": str, "regex": r".+@.+\..+"},
            "age": {"type": int, "nullable": True, "min": 0},
        })
    """

    def __init__(self, schema: Dict[str, Any]):
        """
        Initializes the schema with validation rules.

        :param schema: A dictionary defining the schema rules.
        """
        self.schema = schema

    @staticmethod
    def from_dict(defn: Dict[str, Any]) -> "Schema":
        """
        Creates a Schema instance from a dictionary definition.

        :param defn: The schema definition as a dictionary.
        :return: A Schema instance.
        """
        return Schema(defn)

    def validate(self, data: Dict[str, Any]) -> None:
        """
        Validates the given data against the schema.

        :param data: The data to validate.
        :raises ValidationError: If validation fails.
        """
        violations = []

        for field, rule in self.schema.items():
            value = data.get(field)

            # Check for missing required fields
            if value is None and not (isinstance(rule, dict) and rule.get("nullable")):
                violations.append(f"Field '{field}' is required but missing")
                continue

            # Handle nullable fields
            if isinstance(rule, dict) and rule.get("nullable") and value is None:
                continue

            # Type validation
            expected_type = rule if isinstance(rule, type) else rule.get("type")
            if expected_type and not isinstance(value, expected_type):
                violations.append(f"Field '{field}' must be of type {expected_type.__name__}, got {type(value).__name__}")
                continue

            # Regex validation
            if isinstance(rule, dict) and "regex" in rule:
                if not re.match(rule["regex"], str(value)):
                    violations.append(f"Field '{field}' does not match the required pattern")

            # Min value validation
            if isinstance(rule, dict) and "min" in rule:
                if value < rule["min"]:
                    violations.append(f"Field '{field}' must be at least {rule['min']}")

        if violations:
            raise ValidationError("Schema validation failed", violations)

    def __repr__(self) -> str:
        return f"<Schema rules={self.schema}>"


def check_input(schema: Schema, source: str = "json", sample_rate: float = 1.0) -> Callable:
    """
    Decorator to validate function inputs against a schema.

    :param schema: The Schema instance to validate against.
    :param source: The source of the data (e.g., "json", "query").
    :param sample_rate: Probability of validation in production (0.0 to 1.0).
    :return: The decorated function.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Determine environment
            env = os.getenv("ENV", "dev").lower()

            # Skip validation in production based on sample rate
            if env == "prod" and sample_rate < 1.0:
                import random
                if random.random() > sample_rate:
                    return func(*args, **kwargs)

            # Extract data from the source
            if source == "json":
                request = kwargs.get("request") or args[0]
                data = request.json
            elif source == "query":
                request = kwargs.get("request") or args[0]
                data = request.args
            else:
                raise ValueError(f"Unsupported source: {source}")

            # Validate data
            try:
                schema.validate(data)
            except ValidationError as e:
                raise ValidationError(f"Input validation failed: {e.violations}")

            return func(*args, **kwargs)
        return wrapper
    return decorator


# Example usage
if __name__ == "__main__":
    # Define a schema
    user_schema = Schema({
        "id": int,
        "email": {"type": str, "regex": r".+@.+\..+"},
        "age": {"type": int, "nullable": True, "min": 0},
    })

    @check_input(schema=user_schema, source="json", sample_rate=1.0)
    def create_user(request):
        data = request.json
        print(f"User created with data: {data}")

    # Mock request object for testing
    class MockRequest:
        def __init__(self, json):
            self.json = json

    # Test valid data
    valid_request = MockRequest({"id": 1, "email": "test@example.com", "age": 25})
    try:
        create_user(valid_request)
    except ValidationError as e:
        print(f"Validation error: {e}")

    # Test invalid data
    invalid_request = MockRequest({"id": "abc", "email": "invalid-email", "age": -5})
    try:
        create_user(invalid_request)
    except ValidationError as e:
        print(f"Validation error: {e}")