from fastapi import FastAPI, Request, Response
from py_flowcheck import check_input, check_output, Schema

# Define request and response schemas
request_schema = Schema({
    "user_id": int,
    "action": {"type": str, "enum": ["create", "update", "delete"]}
})

response_schema = Schema({
    "success": bool,
    "message": str
})

# Create FastAPI app instance
app = FastAPI()

@app.post("/action")
@check_input(schema=request_schema, source="json")
@check_output(schema=response_schema)
async def perform_action(request: Request):
    data = await request.json()
    # Your handler logic here
    # For example, process the action based on data['action']
    return {"success": True, "message": "Action performed successfully."}