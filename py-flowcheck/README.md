# py-flowcheck

A lightweight runtime contract validation library for Python backends and data pipelines.

## 🎯 Vision

py-flowcheck provides runtime validation for Python applications with minimal overhead. Add 1-2 decorators to your functions and get immediate contract checks in dev/staging, with configurable sampling in production.

## 🚀 Roadmap to v1.0

### 1. Narrow the First Use Case

**Target Applications:**
- FastAPI / Flask request handlers
- Celery / RQ task functions
- Data pipeline steps

**Problem We Solve:**
Input/output shape and type bugs slipping through to staging/prod because:
- Type hints are incomplete
- Pydantic models aren't used everywhere
- Runtime validation is missing

**Our Advantage:**
More focused than design-by-contract libs like `deal` and lighter than teaching tools like `python_ta.contracts`.

### 2. MVP Feature Set

#### Core Decorators

```python
@check_input(schema=..., source="json|query|body")
@check_output(schema=...)
```

#### Schema Language

Support for:
- Dict with required/optional keys
- Primitive types (int, str, float, bool)
- Enums
- Nullable values
- Min/max constraints for numbers and lengths
- Optional: Pydantic model compatibility

#### Configuration

```python
PY_FLOWCHECK_ENV = "dev|staging|prod"
PY_FLOWCHECK_SAMPLE_RATE = 0.0–1.0  # 0-100% sampling in prod
PY_FLOWCHECK_MODE = "log|raise|sentry"
```

#### Framework Integrations

- FastAPI
- Flask
- Celery
- Future: Airflow, Prefect

### 3. Package Structure

```
py-flowcheck/
  pyproject.toml
  src/py_flowcheck/
    __init__.py
    config.py
    schema.py
    decorators.py
    integrations/
      fastapi.py
      flask.py
      celery.py
  tests/
    test_schema.py
    test_decorators.py
    test_fastapi_integration.py
  examples/
    fastapi_app/
    celery_app/
  README.md
  CHANGELOG.md
  LICENSE
```

**Tooling:**
- Build: `pyproject.toml` with hatchling/poetry
- CI: GitHub Actions (Python 3.9–3.13 matrix + coverage)
- Quality: ruff, mypy, pytest

### 4. Implementation Sketch

#### Basic Schema Definition

```python
from py_flowcheck import check_input, Schema

user_schema = Schema({
    "id": int,
    "email": {"type": str, "regex": r".+@.+\..+"},
    "age": {"type": int, "nullable": True, "min": 0},
})

@check_input(schema=user_schema, source="json")
def create_user(request):
    data = request.json
    # Your logic here
    ...
```

#### Validation Logic

- `Schema.from_dict(defn)` compiles dict schema into checks
- Validation returns list of violations with paths (e.g., `body.user.age`)
- Smart environment handling:
  - **dev/staging**: Always validate
  - **prod**: Validate with probability = `sample_rate`

#### Example FastAPI Integration

```python
from fastapi import FastAPI
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
    # Handler logic
    ...
```

### 5. Launch Plan

#### Phase 1: Initial Release
1. Implement core schema engine
2. Build decorators for FastAPI/Flask
3. Add Celery support
4. Publish to TestPyPI

#### Phase 2: Iterate
1. Gather feedback from GitHub issues
2. Improve error reporting
3. Add dashboard/metrics
4. Publish to PyPI

#### Phase 3: Expand (v2+)
- Async framework support (Starlette, aiohttp)
- DataFrame validation (Pandas/Polars)
- Data pipeline schemas (Airflow/Prefect operators)
- Great Expectations-style data quality checks

## 🎓 Inspiration

- **Great Expectations**: Clear expectation failure messages, summary objects
- **Pydantic**: Runtime validation, but lighter weight
- **deal**: Design-by-contract, but more focused on backend use cases

## 📦 Quick Start (Coming Soon)

```bash
pip install py-flowcheck
```

```python
from py_flowcheck import check_input, Schema

schema = Schema({"name": str, "age": int})

@check_input(schema=schema, source="json")
def my_handler(request):
    ...
```

## 🤝 Contributing

We welcome contributions! Once the MVP is ready, check our GitHub Issues for:
- Feature requests
- Bug reports
- Integration examples

## 📄 License

[To be determined - suggest MIT or Apache 2.0]

## 🗺️ Status

**Current Phase:** Planning & Design  
**Target MVP:** Q2 2024  
**Python Support:** 3.9+

---

*Built with ❤️ for Python developers tired of production bugs from missing validation*