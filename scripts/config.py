import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parents [databasesample]("https://databasesample.com/datasets/claims-processing-insights")

load_dotenv(BASE_DIR / "config" / ".env")

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DB = os.getenv("PG_DB", "mutuelle_db")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "")

DATABASE_URL = (
    f"postgresql://{PG_USER}:{PG_PASSWORD}"
    f"@{PG_HOST}:{PG_PORT}/{PG_DB}"
)

engine = create_engine(DATABASE_URL)

RAW_DIR = BASE_DIR / "data" / "raw"
BRONZE_DIR = BASE_DIR / "data" / "bronze"
LOG_DIR = BASE_DIR / "data" / "logs"

API_BASE_URL = (
    "https://databasesample.com/api/v1/datasets/"
    "claims-processing-insights/tables"
)

API_TABLES = {
    "sinistres": "claims",
    "contrats": "policies",
    "adherents": "beneficiaries",
}

DOMAINS = ["adherents", "contrats", "sinistres"]