from flask import request, jsonify
from py_flowcheck import check_input, check_output, Schema

# Define request schema
request_schema = Schema({
    "user_id": int,
    "action": {"type": str, "enum": ["create", "update", "delete"]}
})

# Define response schema
response_schema = Schema({
    "success": bool,
    "message": str
})

@check_input(schema=request_schema, source="json")
@check_output(schema=response_schema)
def perform_action():
    data = request.json
    # Your logic here
    user_id = data["user_id"]
    action = data["action"]
    
    # Example logic
    if action == "create":
        # Logic for creating a resource
        return jsonify({"success": True, "message": "Resource created"}), 201
    elif action == "update":
        # Logic for updating a resource
        return jsonify({"success": True, "message": "Resource updated"}), 200
    elif action == "delete":
        # Logic for deleting a resource
        return jsonify({"success": True, "message": "Resource deleted"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid action"}), 400