from typing import Any, Dict, List, Union

class Schema:
    def __init__(self, definition: Dict[str, Any]):
        self.definition = definition

    @classmethod
    def from_dict(cls, defn: Dict[str, Any]) -> 'Schema':
        return cls(defn)

    def validate(self, data: Dict[str, Any]) -> List[str]:
        violations = []
        for key, rules in self.definition.items():
            if key not in data:
                violations.append(f"Missing key: {key}")
                continue
            
            value = data[key]
            if not self._validate_type(value, rules.get("type")):
                violations.append(f"Invalid type for key: {key}")
            
            if "nullable" in rules and rules["nullable"] and value is None:
                continue
            
            if "min" in rules and value < rules["min"]:
                violations.append(f"Value for key: {key} is below minimum: {rules['min']}")
            
            if "max" in rules and value > rules["max"]:
                violations.append(f"Value for key: {key} is above maximum: {rules['max']}")
            
            if "regex" in rules and not self._validate_regex(value, rules["regex"]):
                violations.append(f"Value for key: {key} does not match regex: {rules['regex']}")
        
        return violations

    def _validate_type(self, value: Any, expected_type: Union[type, None]) -> bool:
        if expected_type is None:
            return True
        return isinstance(value, expected_type)

    def _validate_regex(self, value: str, pattern: str) -> bool:
        import re
        return re.match(pattern, value) is not None

def check_input(schema: Schema, source: str):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Logic to extract data from the specified source
            data = {}  # Replace with actual data extraction logic
            violations = schema.validate(data)
            if violations:
                raise ValueError(f"Validation errors: {violations}")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def check_output(schema: Schema):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            violations = schema.validate(result)
            if violations:
                raise ValueError(f"Validation errors: {violations}")
            return result
        return wrapper
    return decorator