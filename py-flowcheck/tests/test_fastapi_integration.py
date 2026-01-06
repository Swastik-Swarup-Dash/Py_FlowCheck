from fastapi import FastAPI
from fastapi.testclient import TestClient
from py_flowcheck import check_input, check_output, Schema

app = FastAPI()

request_schema = Schema({
    "user_id": int,
    "action": {"type": str, "enum": ["create", "update", "delete"]}
})

response_schema = Schema({
    "success": bool,
    "message": str
})

@app.post("/action")
@check_input(schema=request_schema, source="json")
@check_output(schema=response_schema)
async def perform_action(request):
    return {"success": True, "message": "Action performed"}

client = TestClient(app)

def test_perform_action_create():
    response = client.post("/action", json={"user_id": 1, "action": "create"})
    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "Action performed"}

def test_perform_action_update():
    response = client.post("/action", json={"user_id": 1, "action": "update"})
    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "Action performed"}

def test_perform_action_delete():
    response = client.post("/action", json={"user_id": 1, "action": "delete"})
    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "Action performed"}

def test_perform_action_invalid_action():
    response = client.post("/action", json={"user_id": 1, "action": "invalid"})
    assert response.status_code == 422  # Unprocessable Entity for invalid input

def test_perform_action_missing_user_id():
    response = client.post("/action", json={"action": "create"})
    assert response.status_code == 422  # Unprocessable Entity for missing required field