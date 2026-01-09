#!/usr/bin/env python3
"""
Web Demo for py-flowcheck
Run this to create a web interface for testing
"""

try:
    from flask import Flask, render_template_string, request, jsonify
    from py_flowcheck import Schema, ValidationError
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install flask pyflowcheck-validation")
    exit(1)

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>py-flowcheck Web Demo</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 10px 0; }
        .success { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
        .error { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
        textarea { width: 100%; height: 150px; font-family: monospace; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .example { background: #e9ecef; padding: 10px; border-radius: 4px; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>🚀 py-flowcheck Web Demo</h1>
    <p>Test the py-flowcheck validation library in your browser!</p>
    
    <div class="container">
        <h3>📝 Test Validation</h3>
        <form id="testForm">
            <label>Schema (Python dict format):</label>
            <textarea id="schema" placeholder='{"name": str, "age": int, "email": str}'>{
    "name": str,
    "age": int,
    "email": str
}</textarea>
            
            <label>Test Data (JSON format):</label>
            <textarea id="data" placeholder='{"name": "John", "age": 25, "email": "john@example.com"}'>{"name": "John", "age": 25, "email": "john@example.com"}</textarea>
            
            <button type="submit">🧪 Test Validation</button>
        </form>
        
        <div id="result"></div>
    </div>
    
    <div class="container">
        <h3>📚 Examples</h3>
        <div class="example">
            <strong>Valid User:</strong><br>
            Schema: {"name": str, "age": int, "active": bool}<br>
            Data: {"name": "Alice", "age": 30, "active": true}
        </div>
        <div class="example">
            <strong>Invalid Type:</strong><br>
            Schema: {"score": int}<br>
            Data: {"score": "not_a_number"}
        </div>
        <div class="example">
            <strong>Nested Object:</strong><br>
            Schema: {"user": {"name": str, "settings": {"theme": str}}}<br>
            Data: {"user": {"name": "Bob", "settings": {"theme": "dark"}}}
        </div>
    </div>

    <script>
        document.getElementById('testForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const schema = document.getElementById('schema').value;
            const data = document.getElementById('data').value;
            const resultDiv = document.getElementById('result');
            
            try {
                const response = await fetch('/validate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({schema: schema, data: data})
                });
                
                const result = await response.json();
                
                if (result.success) {
                    resultDiv.innerHTML = `<div class="container success">
                        <h4>✅ Validation Passed!</h4>
                        <p>${result.message}</p>
                    </div>`;
                } else {
                    resultDiv.innerHTML = `<div class="container error">
                        <h4>❌ Validation Failed</h4>
                        <p>${result.error}</p>
                    </div>`;
                }
            } catch (error) {
                resultDiv.innerHTML = `<div class="container error">
                    <h4>❌ Error</h4>
                    <p>${error.message}</p>
                </div>`;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/validate', methods=['POST'])
def validate():
    try:
        data = request.json
        schema_str = data['schema']
        test_data_str = data['data']
        
        # Parse schema (simple eval for demo - not production safe)
        schema_dict = eval(schema_str)
        schema = Schema(schema_dict)
        
        # Parse test data
        import json
        test_data = json.loads(test_data_str)
        
        # Validate
        schema.validate(test_data)
        
        return jsonify({
            'success': True,
            'message': f'Data validation passed! Schema: {schema_dict}'
        })
        
    except ValidationError as e:
        return jsonify({
            'success': False,
            'error': f'Validation Error: {str(e)}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {str(e)}'
        })

if __name__ == '__main__':
    print("🌐 Starting py-flowcheck web demo...")
    print("📱 Open http://localhost:5000 in your browser")
    print("🛑 Press Ctrl+C to stop")
    app.run(debug=True, host='0.0.0.0', port=5000)