## Power Rankings Backend

Keeps data via SQLModel and SQLite on power rankings for the frolf coalition

### Prerequisites
- Python 3.11 or 3.12 recommended
- Install `uv` (fast Python package manager)
  - macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows (PowerShell): `irm https://astral.sh/uv/install.ps1 | iex`

### 1) Create a virtual environment
```bash
uv venv
```

Activate it:
- macOS/Linux:
```bash
source .venv/bin/activate
```
- Windows (PowerShell):
```powershell
.venv\\Scripts\\Activate.ps1
```

### 2) Install dependencies
```bash
uv pip install -r requirements.txt
```

### 3) Configuration
Copy the example environment file and adjust as needed:
```bash
cp env.example .env
```

Environment variables:
- `DATABASE_URL`: SQLAlchemy URL for the database. Defaults to `sqlite:///./app.db`.

SQLite files will be created in the project root by default.

### 4) Run the development server
Using uv to run Uvicorn with auto-reload:
```bash
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Then open `http://127.0.0.1:8000/docs` for interactive API docs.

### Project structure
```text
app/
  __init__.py
  main.py            # FastAPI app/entrypoint
  config.py          # App settings from env
  db.py              # Engine/session creation and table init
  models.py          # SQLModel models
  api/
    __init__.py
    routes.py        # API routers and endpoints
env.example          # Example environment config
requirements.txt     # Dependencies for uv pip
README.md            # This file
```

### Common tasks
- Run with a different DB URL:
```bash
DATABASE_URL="sqlite:///./dev.db" uv run uvicorn app.main:app --reload
```

- Reset SQLite DB (dangerous: deletes file):
```bash
rm -f app.db
```