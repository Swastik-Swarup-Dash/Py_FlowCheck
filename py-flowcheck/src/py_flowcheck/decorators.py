from functools import wraps
from typing import Callable, Any, Dict, Optional

def check_input(schema: Dict[str, Any], source: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Logic to validate input against the schema
            # This is a placeholder for actual validation logic
            print(f"Validating input from {source} against schema: {schema}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def check_output(schema: Dict[str, Any]) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)
            # Logic to validate output against the schema
            # This is a placeholder for actual validation logic
            print(f"Validating output against schema: {schema}")
            return result
        return wrapper
    return decorator