import functools
from typing import Callable, Any
from py_flowcheck.schema import Schema, ValidationError 

# For Logging Func calls
def log_function_call(func: Callable) -> Callable:
    """logs functions calls with their args"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} returned: {result}")
        return result
    return wrapper


#Ensuring preconditions are met
def precondition(precondition: Callable[..., bool]) -> Callable:
    """Decorator to ensure the precondtions are met before executing the funcion"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not precondition(*args, **kwargs):
                raise ValueError("PreCondtion has bee failed for function '{func.__name__}'")
            return func(*args, **kwargs)
        return wrapper
    return decorator



# Decorator for debugging function calls
def debug_function_call(func: Callable) -> Callable:
    """Logs the function name, arguments, and return value for debugging purposes."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[DEBUG] Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"[DEBUG] {func.__name__} returned: {result}")
        return result
    return wrapper



# Decorator for enforcing postconditions
def postcondition(postcondition: Callable[[Any], bool]) -> Callable:
    """Ensures a postcondition is met after executing the function."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if not postcondition(result):
                raise ValueError(f"Postcondition failed for function '{func.__name__}'")
            return result
        return wrapper
    return decorator


# Decorator for validating function inputs
def check_input(schema: Schema, source: str = "json") -> Callable:
    """
    Decorator to validate function inputs against a schema.

    :param schema: The Schema instance to validate against.
    :param source: The source of the data (e.g., "json", "query").
    :return: The decorated function.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extract data from the source
            if source == "json":
                data = kwargs.get("data") or args[0]
            else:
                raise ValueError(f"Unsupported source: {source}")

            # Validate the data
            try:
                schema.validate(data)
            except ValidationError as e:
                raise ValueError(f"Input validation failed: {e.violations}")

            return func(*args, **kwargs)
        return wrapper
    return decorator



# Decorator for validating function outputs
def check_output(schema: Schema) -> Callable:
    """
    Decorator to validate function outputs against a schema.

    :param schema: The Schema instance to validate the output.
    :return: The decorated function.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            # Validate the result
            try:
                schema.validate(result)
            except ValidationError as e:
                raise ValueError(f"Output validation failed: {e.violations}")

            return result
        return wrapper
    return decorator




if __name__ == "__main__":
    # Example precondition function
    def precondition_example(*args, **kwargs) -> bool:
        return args[0] > 10  

    # Example postcondition function
    def postcondition_example(result: Any) -> bool:
        return result < 100 

    @log_function_call
    @precondition(precondition_example)
    @postcondition(postcondition_example)
    @debug_function_call
    def example_function(a: int, b: int) -> int:
        return a + b

    try:
        print(example_function(15, 20))  # Should pass
        print(example_function(5, 20))   # Should fail precondition
    except ValueError as e:
        print(f"Error: {e}")
            







