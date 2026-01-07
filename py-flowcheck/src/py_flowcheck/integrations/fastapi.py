from fastapi import FastAPI, Request, Response, HTTPException
from py_flowcheck import check_input, Schema, ValidationError

# Initialize FastAPI app
app = FastAPI()

# Define input schema for user creation
user_input_schema = Schema({
    "id": int,
    "email": {"type": str, "regex": r".+@.+\..+"},
    "age": {"type": int, "nullable": True, "min": 0},
})

# Define output schema for user response
user_output_schema = Schema({
    "id": int,
    "email": str,
    "age": {"type": int, "nullable": True},
    "status": {"type": str, "regex": r"^(active|inactive)$"},
})

# Decorator for validating output (response payloads)
def check_output(schema: Schema):
    """
    Decorator to validate the response payload against a schema.

    :param schema: The Schema instance to validate the response.
    :return: The decorated function.
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            response = await func(*args, **kwargs)
            try:
                schema.validate(response)
            except ValidationError as e:
                raise HTTPException(status_code=500, detail=f"Response validation failed: {e.violations}")
            return response
        return wrapper
    return decorator

@app.post("/users")
@check_input(schema=user_input_schema, source="json")
@check_output(schema=user_output_schema)
async def create_user(request: Request):
    """
    Endpoint to create a user. Validates both input and output payloads.

    :param request: The incoming HTTP request.
    :return: The response payload.
    """
    data = await request.json()

    # Simulate user creation logic
    user = {
        "id": data["id"],
        "email": data["email"],
        "age": data.get("age"),
        "status": "active",  # Default status
    }

    return user

# Example usage of the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)