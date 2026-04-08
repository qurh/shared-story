# shared-story backend

Python/FastAPI backend for shared-story.

## Run (from repo root)

```powershell
.\.venv\Scripts\python -m uvicorn app.main:app --reload --app-dir apps/backend
```

## Test (from repo root)

```powershell
.\.venv\Scripts\python -m pytest -q apps/backend/tests
.\.venv\Scripts\python -m ruff check apps/backend
```

