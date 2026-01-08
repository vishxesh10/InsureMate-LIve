import os
from pathlib import Path

# Centralized configuration for InsureMate
BASE_DIR = Path(__file__).resolve().parents[2]

# Database URL (use env var in production). Defaults to local sqlite file.
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'insurance_results.db'}")

# Model path: can be set via env var. Defaults to model.pkl in project root.
MODEL_PATH = Path(os.environ.get("MODEL_PATH", str(BASE_DIR / "model.pkl"))).resolve()

# App settings
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 8000))

# For SQLAlchemy connect args for SQLite
def get_sqlalchemy_connect_args():
    if DATABASE_URL.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}
