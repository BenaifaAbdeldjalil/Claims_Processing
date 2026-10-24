import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine


BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BASE_DIR / "config" / ".env")

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DB = os.getenv("PG_DB", "claims_processing")
PG_USER = os.getenv("PG_USER", "mutuelle_rw")
PG_PASSWORD = os.getenv("PG_PASSWORD", "")

DATABASE_URL = (
    f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}"
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