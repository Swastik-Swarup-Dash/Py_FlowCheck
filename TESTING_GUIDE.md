# 🚀 Test py-flowcheck with Your Friends!

Hey! Want to test out the **py-flowcheck** validation library? Here are super easy ways to try it:

## 🎯 Option 1: Quick Test (2 minutes)

```bash
# Install the library
pip install pyflowcheck-validation

# Run the simple test
python simple_real_world_test.py
```

## 🎮 Option 2: Interactive Demo (5 minutes)

```bash
# Run the interactive demo
python interactive_demo.py
```

This lets you:
- ✅ Test basic validation
- 🔍 Try nested objects  
- ⚡ See performance metrics
- 🎛️ Test different modes
- 🛠️ Create your own schemas

## 🌐 Option 3: Web Interface (Fun!)

```bash
# Install Flask if needed
pip install flask

# Start the web demo
python web_demo.py

# Open http://localhost:5000 in your browser
```

Test validation through a web interface!

## 📱 Option 4: One-Line Test

```python
from py_flowcheck import Schema
schema = Schema({"name": str, "age": int})
schema.validate({"name": "Alice", "age": 25})  # ✅ Works!
schema.validate({"name": "Bob", "age": "old"})  # ❌ Fails!
```

## 🎯 What to Test

Try these scenarios:

### ✅ Valid Data
```python
user = {"name": "John", "age": 25, "active": True}
```

### ❌ Invalid Data
```python
user = {"name": "Jane", "age": "twenty", "active": True}  # age should be int
```

### 🏗️ Nested Objects
```python
profile = {
    "user": {
        "name": "Alice",
        "settings": {"theme": "dark", "notifications": True}
    }
}
```

## 🚀 Performance Test

The library can handle **3+ million validations per second**! Try the performance demo to see.

## 🎛️ Configuration Modes

- **raise**: Throws exceptions (development)
- **log**: Logs errors (staging) 
- **silent**: Ignores errors (production sampling)

## 📊 What Makes This Special?

- ⚡ **Super Fast**: 3M+ validations/second
- 🏭 **Production Ready**: Built-in sampling and monitoring
- 🎛️ **Configurable**: Different modes for different environments
- 🔍 **Detailed Errors**: Clear validation messages
- 🏗️ **Nested Support**: Complex object validation

## 🤝 Feedback

After testing, let me know:
- ✅ What worked well?
- ❌ Any issues you found?
- 💡 Feature ideas?
- 🚀 Would you use this in your projects?

## 📚 More Info

- 📦 **PyPI**: `pip install pyflowcheck-validation`
- 🐙 **GitHub**: [Py_FlowCheck Repository](https://github.com/Swastik-Swarup-Dash/Py_FlowCheck)
- 📖 **Docs**: Check the examples in the repo

---

**Happy Testing! 🎉**