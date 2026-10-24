import os
from pathlib import Path

# Projet créé dans le dossier courant
base = Path("mutuelle-api-project")

# 1) Dossiers principaux
folders = [
    "config",

    "data/raw/adherents",
    "data/raw/contrats",
    "data/raw/sinistres",

    "data/bronze/adherents",
    "data/bronze/contrats",
    "data/bronze/sinistres",

    "data/silver",
    "data/gold",
    "data/logs",

    "sql/bronze",
    "sql/silver",
    "sql/gold",

    "scripts",
    "tests",
    "notebooks",
]

# Création du dossier principal
if not base.exists():
    base.mkdir(parents=True, exist_ok=True)
    print(f"✅ Projet créé : {base.resolve()}")
else:
    print(f"⏭️  Projet déjà existant : {base.resolve()}")

# Création des dossiers
for folder in folders:
    path = base / folder

    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Dossier créé : {path}")
    else:
        print(f"⏭️  Dossier déjà existant : {path}")


# 2) Fichiers principaux
files = [
    "requirements.txt",

    "config/.env.example",

    "data/raw/adherents/.gitkeep",
    "data/raw/contrats/.gitkeep",
    "data/raw/sinistres/.gitkeep",

    "data/bronze/adherents/.gitkeep",
    "data/bronze/contrats/.gitkeep",
    "data/bronze/sinistres/.gitkeep",

    "data/silver/.gitkeep",
    "data/gold/.gitkeep",
    "data/logs/.gitkeep",

    "sql/01_create_database.sql",
    "sql/02_create_schemas.sql",
    "sql/bronze/03_create_bronze_tables.sql",
    "sql/silver/04_create_silver_tables.sql",
    "sql/gold/05_create_gold_tables.sql",
    "sql/gold/06_create_gold_views.sql",

    "scripts/__init__.py",
    "scripts/config.py",
    "scripts/extract_api.py",
    "scripts/extract_files.py",
    "scripts/load_bronze.py",
    "scripts/transform_silver.py",
    "scripts/build_gold.py",
    "scripts/historisation.py",
    "scripts/run_quality_checks.py",
    "scripts/run_pipeline.py",

    "tests/__init__.py",
    "tests/test_data_quality.py",

    "notebooks/claims_analysis.ipynb",
]

# Création des fichiers
for file_path in files:
    file = base / file_path

    if file.exists():
        print(f"⏭️  Fichier déjà existant : {file}")
        continue

    file.parent.mkdir(parents=True, exist_ok=True)

    # requirements.txt
    if file_path == "requirements.txt":
        file.write_text(
            """pandas
sqlalchemy
psycopg2-binary
requests
python-dotenv
openpyxl
pytest
""",
            encoding="utf-8",
        )

    # Exemple de configuration
    elif file_path == "config/.env.example":
        file.write_text(
            """PG_HOST=localhost
PG_PORT=5432
PG_DB=mutuelle_db
PG_USER=postgres
PG_PASSWORD=your_password
""",
            encoding="utf-8",
        )

    # SQL : création de la base
    elif file_path == "sql/01_create_database.sql":
        file.write_text(
            """-- Run this script while connected to PostgreSQL,
-- outside the mutuelle_db database.

CREATE DATABASE mutuelle_db;
""",
            encoding="utf-8",
        )

    # SQL : création des schémas
    elif file_path == "sql/02_create_schemas.sql":
        file.write_text(
            """CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
""",
            encoding="utf-8",
        )

    # SQL : tables Bronze
    elif file_path == "sql/bronze/03_create_bronze_tables.sql":
        file.write_text(
            """CREATE TABLE IF NOT EXISTS bronze.adherents (
    bronze_id BIGSERIAL PRIMARY KEY,
    source_system VARCHAR(100),
    source_endpoint VARCHAR(255),
    ingestion_date TIMESTAMP NOT NULL DEFAULT NOW(),
    raw_data JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS bronze.contrats (
    bronze_id BIGSERIAL PRIMARY KEY,
    source_system VARCHAR(100),
    source_endpoint VARCHAR(255),
    ingestion_date TIMESTAMP NOT NULL DEFAULT NOW(),
    raw_data JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS bronze.sinistres (
    bronze_id BIGSERIAL PRIMARY KEY,
    source_system VARCHAR(100),
    source_endpoint VARCHAR(255),
    ingestion_date TIMESTAMP NOT NULL DEFAULT NOW(),
    raw_data JSONB NOT NULL
);
""",
            encoding="utf-8",
        )

    # SQL : tables Silver
    elif file_path == "sql/silver/04_create_silver_tables.sql":
        file.write_text(
            """CREATE TABLE IF NOT EXISTS silver.adherents (
    id_adherent VARCHAR(50) PRIMARY KEY,
    last_name VARCHAR(100),
    first_name VARCHAR(100),
    date_of_birth DATE,
    gender VARCHAR(1),
    enrollment_date DATE,
    status VARCHAR(30),
    email VARCHAR(150),
    source_system VARCHAR(100),
    loaded_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS silver.contrats (
    id_contrat VARCHAR(50) PRIMARY KEY,
    id_adherent VARCHAR(50),
    plan_type VARCHAR(100),
    start_date DATE,
    end_date DATE,
    status VARCHAR(30),
    monthly_premium NUMERIC(10, 2),
    source_system VARCHAR(100),
    loaded_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS silver.sinistres (
    id_sinistre VARCHAR(50) PRIMARY KEY,
    id_contrat VARCHAR(50),
    id_adherent VARCHAR(50),
    incident_date DATE,
    declaration_date DATE,
    claim_type VARCHAR(100),
    claimed_amount NUMERIC(12, 2),
    reimbursed_amount NUMERIC(12, 2),
    status VARCHAR(30),
    source_system VARCHAR(100),
    loaded_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS silver.contrats_history (
    history_id BIGSERIAL PRIMARY KEY,
    id_contrat VARCHAR(50) NOT NULL,
    id_adherent VARCHAR(50),
    plan_type VARCHAR(100),
    start_date DATE,
    end_date DATE,
    status VARCHAR(30),
    monthly_premium NUMERIC(10, 2),
    valid_from TIMESTAMP NOT NULL,
    valid_to TIMESTAMP,
    is_current BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_contrats_history_id
ON silver.contrats_history (id_contrat);

CREATE INDEX IF NOT EXISTS idx_contrats_history_current
ON silver.contrats_history (id_contrat, is_current);
""",
            encoding="utf-8",
        )

    # SQL : tables Gold
    elif file_path == "sql/gold/05_create_gold_tables.sql":
        file.write_text(
            """CREATE TABLE IF NOT EXISTS gold.dim_members (
    id_adherent VARCHAR(50) PRIMARY KEY,
    last_name VARCHAR(100),
    first_name VARCHAR(100),
    date_of_birth DATE,
    age INT,
    gender VARCHAR(1),
    enrollment_date DATE,
    enrollment_year INT,
    status VARCHAR(30),
    email VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS gold.fact_contracts (
    id_contrat VARCHAR(50) PRIMARY KEY,
    id_adherent VARCHAR(50),
    plan_type VARCHAR(100),
    start_date DATE,
    end_date DATE,
    start_year INT,
    status VARCHAR(30),
    monthly_premium NUMERIC(10, 2),
    annual_premium NUMERIC(12, 2),
    contract_duration_days INT
);

CREATE TABLE IF NOT EXISTS gold.fact_claims (
    id_sinistre VARCHAR(50) PRIMARY KEY,
    id_contrat VARCHAR(50),
    id_adherent VARCHAR(50),
    plan_type VARCHAR(100),
    claim_type VARCHAR(100),
    incident_date DATE,
    declaration_date DATE,
    incident_year INT,
    incident_month INT,
    claimed_amount NUMERIC(12, 2),
    reimbursed_amount NUMERIC(12, 2),
    reimbursement_rate NUMERIC(5, 2),
    status VARCHAR(30)
);
""",
            encoding="utf-8",
        )

    # SQL : vues Gold
    elif file_path == "sql/gold/06_create_gold_views.sql":
        file.write_text(
            """CREATE OR REPLACE VIEW gold.kpi_active_members AS
SELECT COUNT(*) AS active_members
FROM silver.adherents
WHERE status = 'ACTIVE';

CREATE OR REPLACE VIEW gold.kpi_contracts_by_status AS
SELECT
    status,
    COUNT(*) AS contract_count
FROM silver.contrats
GROUP BY status
ORDER BY contract_count DESC;

CREATE OR REPLACE VIEW gold.kpi_contracts_by_plan AS
SELECT
    plan_type,
    COUNT(*) AS contract_count,
    SUM(monthly_premium) AS total_monthly_premium,
    ROUND(AVG(monthly_premium), 2) AS average_premium
FROM silver.contrats
GROUP BY plan_type
ORDER BY contract_count DESC;

CREATE OR REPLACE VIEW gold.kpi_claims_by_type AS
SELECT
    claim_type,
    COUNT(*) AS claim_count,
    SUM(claimed_amount) AS total_claimed,
    SUM(reimbursed_amount) AS total_reimbursed,
    ROUND(
        SUM(reimbursed_amount)
        / NULLIF(SUM(claimed_amount), 0) * 100,
        2
    ) AS reimbursement_rate
FROM gold.fact_claims
GROUP BY claim_type
ORDER BY total_claimed DESC;

CREATE OR REPLACE VIEW gold.kpi_monthly_claims AS
SELECT
    incident_year,
    incident_month,
    COUNT(*) AS claim_count,
    SUM(claimed_amount) AS total_claimed,
    SUM(reimbursed_amount) AS total_reimbursed
FROM gold.fact_claims
GROUP BY incident_year, incident_month
ORDER BY incident_year, incident_month;

CREATE OR REPLACE VIEW gold.kpi_top_members_by_reimbursement AS
SELECT
    m.id_adherent,
    m.last_name,
    m.first_name,
    COUNT(c.id_sinistre) AS claim_count,
    SUM(c.reimbursed_amount) AS total_reimbursed
FROM silver.adherents m
LEFT JOIN silver.sinistres c
    ON m.id_adherent = c.id_adherent
GROUP BY m.id_adherent, m.last_name, m.first_name
ORDER BY total_reimbursed DESC NULLS LAST
LIMIT 10;
""",
            encoding="utf-8",
        )

    # Python : configuration
    elif file_path == "scripts/config.py":
        file.write_text(
            '''import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parents[1]

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
SILVER_DIR = BASE_DIR / "data" / "silver"
GOLD_DIR = BASE_DIR / "data" / "gold"
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
''',
            encoding="utf-8",
        )

    # Python : extraction API
    elif file_path == "scripts/extract_api.py":
        file.write_text(
            '''import requests
import pandas as pd

from config import API_BASE_URL, API_TABLES

PAGE_SIZE = 100
MAX_PAGES = 20
TIMEOUT = 30


def extract_records_from_payload(payload):
    """Extract records regardless of the API response structure."""
    if isinstance(payload, list):
        return payload

    for key in ["data", "rows", "results", "records", "items"]:
        if isinstance(payload, dict) and isinstance(payload.get(key), list):
            return payload[key]

    return []


def extract_table(domain: str, api_table: str) -> pd.DataFrame:
    """Retrieve all available pages for one API table."""
    all_records = []
    page = 1

    endpoint = f"{API_BASE_URL}/{api_table}/rows"

    while page <= MAX_PAGES:
        params = {
            "limit": PAGE_SIZE,
            "page": page,
        }

        response = requests.get(
            endpoint,
            params=params,
            timeout=TIMEOUT,
        )
        response.raise_for_status()

        payload = response.json()
        records = extract_records_from_payload(payload)

        if not records:
            break

        all_records.extend(records)

        print(f"[API] {domain} - page {page}: {len(records)} rows")

        if len(records) < PAGE_SIZE:
            break

        page += 1

    if not all_records:
        raise ValueError(
            f"No data retrieved for {domain} ({endpoint})"
        )

    df = pd.DataFrame(all_records)

    df["source_system"] = "databasesample_claims_api"
    df["source_endpoint"] = endpoint
    df["extraction_date"] = pd.Timestamp.now()

    return df


def extract_all_domains():
    """Extract all domains from the API."""
    datasets = {}

    for domain, api_table in API_TABLES.items():
        print(f"\\n--- API extraction: {domain} ({api_table}) ---")
        datasets[domain] = extract_table(domain, api_table)

    return datasets


if __name__ == "__main__":
    datasets = extract_all_domains()

    for domain, df in datasets.items():
        print(f"\\n{domain}: {len(df)} rows")
        print("Columns:", list(df.columns))
        print(df.head())
''',
            encoding="utf-8",
        )

    # Python : extraction fichiers
    elif file_path == "scripts/extract_files.py":
        file.write_text(
            '''import json
from pathlib import Path

import pandas as pd

from config import RAW_DIR


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def read_excel(path: Path) -> pd.DataFrame:
    return pd.read_excel(path, dtype=str)


def read_json(path: Path) -> pd.DataFrame:
    with path.open("r", encoding="utf-8") as file:
        records = json.load(file)
    return pd.DataFrame(records)


def extract_domain(domain: str) -> pd.DataFrame:
    """Read all CSV, Excel, and JSON files for one domain."""
    domain_dir = RAW_DIR / domain
    dataframes = []

    for path in sorted(domain_dir.iterdir()):
        if path.suffix.lower() == ".csv":
            df = read_csv(path)
        elif path.suffix.lower() in [".xlsx", ".xls"]:
            df = read_excel(path)
        elif path.suffix.lower() == ".json":
            df = read_json(path)
        else:
            continue

        df["source_system"] = "local_file"
        df["source_endpoint"] = str(path.name)
        dataframes.append(df)

    if not dataframes:
        raise FileNotFoundError(
            f"No file found for domain {domain}"
        )

    return pd.concat(dataframes, ignore_index=True)
''',
            encoding="utf-8",
        )

    # Python : chargement Bronze
    elif file_path == "scripts/load_bronze.py":
        file.write_text(
            '''import json
from datetime import datetime

import pandas as pd

from config import BRONZE_DIR, DOMAINS, engine
from extract_api import extract_all_domains
from extract_files import extract_domain


def save_bronze_file(
    df: pd.DataFrame,
    domain: str,
    source_type: str,
):
    """Save raw data as a JSON file in data/bronze/<domain>."""
    domain_dir = BRONZE_DIR / domain
    domain_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = domain_dir / f"{domain}_{source_type}_{timestamp}.json"

    df.to_json(
        output_path,
        orient="records",
        force_ascii=False,
        indent=2,
    )

    return output_path


def load_to_bronze_table(
    df: pd.DataFrame,
    domain: str,
    source_system: str,
    source_endpoint: str,
):
    """Load each raw record into bronze.<domain> as JSONB."""
    records = []

    for _, row in df.iterrows():
        raw_record = row.to_dict()

        records.append(
            {
                "source_system": source_system,
                "source_endpoint": source_endpoint,
                "raw_data": json.dumps(
                    raw_record,
                    ensure_ascii=False,
                    default=str,
                ),
            }
        )

    bronze_df = pd.DataFrame(records)

    bronze_df.to_sql(
        f"bronze.{domain}",
        engine,
        if_exists="append",
        index=False,
    )

    return len(bronze_df)


def run_bronze_load():
    # API sources
    api_datasets = extract_all_domains()

    for domain, df in api_datasets.items():
        print(f"\\n[BRONZE-API] Domain: {domain}")

        endpoint = df["source_endpoint"].iloc[0]
        source_system = df["source_system"].iloc[0]

        output_path = save_bronze_file(df, domain, "api")
        row_count = load_to_bronze_table(
            df,
            domain,
            source_system,
            endpoint,
        )

        print(f"[BRONZE-API] {row_count} rows loaded")
        print(f"[BRONZE-API] Raw file: {output_path}")

    # Local file sources
    for domain in DOMAINS:
        try:
            df = extract_domain(domain)
        except FileNotFoundError:
            print(f"\\n[BRONZE-FILE] No local file for {domain}")
            continue

        print(f"\\n[BRONZE-FILE] Domain: {domain}")

        endpoint = df["source_endpoint"].iloc[0]
        source_system = df["source_system"].iloc[0]

        output_path = save_bronze_file(df, domain, "file")
        row_count = load_to_bronze_table(
            df,
            domain,
            source_system,
            endpoint,
        )

        print(f"[BRONZE-FILE] {row_count} rows loaded")
        print(f"[BRONZE-FILE] Raw file: {output_path}")


if __name__ == "__main__":
    run_bronze_load()
''',
            encoding="utf-8",
        )

    # Python : transformation Silver
    elif file_path == "scripts/transform_silver.py":
        file.write_text(
            '''import json
from datetime import datetime

import pandas as pd
from sqlalchemy import text

from config import DOMAINS, engine

COLUMN_MAPPING = {
    "sinistres": {
        "id": "id_sinistre",
        "claim_id": "id_sinistre",
        "policy_id": "id_contrat",
        "beneficiary_id": "id_adherent",
        "claim_date": "incident_date",
        "submission_date": "declaration_date",
        "claim_type": "claim_type",
        "amount": "claimed_amount",
        "approved_amount": "reimbursed_amount",
        "status": "status",
    },
    "contrats": {
        "id": "id_contrat",
        "policy_id": "id_contrat",
        "beneficiary_id": "id_adherent",
        "policy_type": "plan_type",
        "start_date": "start_date",
        "end_date": "end_date",
        "status": "status",
        "premium": "monthly_premium",
    },
    "adherents": {
        "id": "id_adherent",
        "beneficiary_id": "id_adherent",
        "first_name": "first_name",
        "last_name": "last_name",
        "date_of_birth": "date_of_birth",
        "gender": "gender",
        "enrollment_date": "enrollment_date",
        "status": "status",
        "email": "email",
    },
}

DATE_COLUMNS = {
    "adherents": ["date_of_birth", "enrollment_date"],
    "contrats": ["start_date", "end_date"],
    "sinistres": ["incident_date", "declaration_date"],
}

NUMERIC_COLUMNS = {
    "contrats": ["monthly_premium"],
    "sinistres": ["claimed_amount", "reimbursed_amount"],
}

PRIMARY_KEYS = {
    "adherents": "id_adherent",
    "contrats": "id_contrat",
    "sinistres": "id_sinistre",
}

SILVER_TABLES = {
    "adherents": "silver.adherents",
    "contrats": "silver.contrats",
    "sinistres": "silver.sinistres",
}

CLAIM_STATUS_MAPPING = {
    "submitted": "SUBMITTED",
    "in_review": "IN_REVIEW",
    "approved": "APPROVED",
    "denied": "DENIED",
    "paid": "REIMBURSED",
}

POLICY_STATUS_MAPPING = {
    "active": "ACTIVE",
    "cancelled": "CANCELLED",
    "expired": "EXPIRED",
    "pending": "PENDING",
}


def read_bronze(domain: str) -> pd.DataFrame:
    """Read JSONB records from the Bronze table."""
    query = f"""
        SELECT raw_data, source_system, source_endpoint
        FROM bronze.{domain}
        ORDER BY bronze_id
    """

    with engine.connect() as connection:
        result = connection.execute(text(query))
        rows = result.fetchall()

    records = []

    for raw_data, source_system, source_endpoint in rows:
        record = (
            json.loads(raw_data)
            if isinstance(raw_data, str)
            else dict(raw_data)
        )

        record["source_system"] = source_system
        record["source_endpoint"] = source_endpoint
        records.append(record)

    return pd.DataFrame(records)


def rename_columns(df: pd.DataFrame, domain: str) -> pd.DataFrame:
    """Rename API columns to the mutuelle business model."""
    mapping = COLUMN_MAPPING[domain]

    for source_column, target_column in mapping.items():
        if source_column in df.columns:
            df[target_column] = df[source_column]

    return df


def clean_text(df: pd.DataFrame) -> pd.DataFrame:
    """Clean text columns."""
    for column in df.select_dtypes(include="object").columns:
        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
            .replace({"nan": None, "": None, "None": None})
        )
    return df


def clean_dates(df: pd.DataFrame, domain: str) -> pd.DataFrame:
    """Convert date columns without blocking the pipeline."""
    for column in DATE_COLUMNS.get(domain, []):
        if column in df.columns:
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce",
            ).dt.date
    return df


def clean_numerics(df: pd.DataFrame, domain: str) -> pd.DataFrame:
    """Convert amount columns to numeric values."""
    for column in NUMERIC_COLUMNS.get(domain, []):
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )
    return df


def normalize_status(df: pd.DataFrame, domain: str) -> pd.DataFrame:
    """Normalize API statuses into business statuses."""
    if "status" not in df.columns:
        return df

    if domain == "sinistres":
        mapping = CLAIM_STATUS_MAPPING
    elif domain == "contrats":
        mapping = POLICY_STATUS_MAPPING
    else:
        mapping = {}

    df["status"] = (
        df["status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(mapping)
        .fillna(df["status"].astype(str).str.upper().str.replace(" ", "_"))
    )

    return df


def remove_duplicates(df: pd.DataFrame, primary_key: str) -> pd.DataFrame:
    """Remove duplicates based on the business primary key."""
    before = len(df)
    df = df.drop_duplicates(subset=[primary_key], keep="last")
    after = len(df)

    print(f"[QUALITY] Duplicates removed on {primary_key}: {before - after}")
    return df


def add_audit_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add Silver loading metadata."""
    df["loaded_at"] = datetime.now()
    return df


def transform_domain(domain: str):
    print(f"\\n--- SILVER: {domain} ---")

    df = read_bronze(domain)
    df = rename_columns(df, domain)
    df = clean_text(df)
    df = clean_dates(df, domain)
    df = clean_numerics(df, domain)
    df = normalize_status(df, domain)

    primary_key = PRIMARY_KEYS[domain]
    df = remove_duplicates(df, primary_key)
    df = add_audit_columns(df)

    table_name = SILVER_TABLES[domain]

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False,
    )

    print(f"[SILVER] {len(df)} rows loaded into {table_name}")


def run_silver_transformation():
    for domain in DOMAINS:
        transform_domain(domain)


if __name__ == "__main__":
    run_silver_transformation()
''',
            encoding="utf-8",
        )

    # Python : construction Gold
    elif file_path == "scripts/build_gold.py":
        file.write_text(
            '''import pandas as pd
from sqlalchemy import text

from config import engine

GOLD_QUERIES = {
    "gold.dim_members": """
        TRUNCATE TABLE gold.dim_members;

        INSERT INTO gold.dim_members
        SELECT
            id_adherent,
            last_name,
            first_name,
            date_of_birth,
            EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth))::INT AS age,
            gender,
            enrollment_date,
            EXTRACT(YEAR FROM enrollment_date)::INT AS enrollment_year,
            status,
            email
        FROM silver.adherents;
    """,
    "gold.fact_contracts": """
        TRUNCATE TABLE gold.fact_contracts;

        INSERT INTO gold.fact_contracts
        SELECT
            id_contrat,
            id_adherent,
            plan_type,
            start_date,
            end_date,
            EXTRACT(YEAR FROM start_date)::INT AS start_year,
            status,
            monthly_premium,
            monthly_premium * 12 AS annual_premium,
            CASE
                WHEN end_date IS NOT NULL
                THEN end_date - start_date
                ELSE CURRENT_DATE - start_date
            END AS contract_duration_days
        FROM silver.contrats;
    """,
    "gold.fact_claims": """
        TRUNCATE TABLE gold.fact_claims;

        INSERT INTO gold.fact_claims
        SELECT
            s.id_sinistre,
            s.id_contrat,
            s.id_adherent,
            c.plan_type,
            s.claim_type,
            s.incident_date,
            s.declaration_date,
            EXTRACT(YEAR FROM s.incident_date)::INT AS incident_year,
            EXTRACT(MONTH FROM s.incident_date)::INT AS incident_month,
            s.claimed_amount,
            s.reimbursed_amount,
            CASE
                WHEN s.claimed_amount > 0
                THEN ROUND(
                    (s.reimbursed_amount / s.claimed_amount) * 100,
                    2
                )
                ELSE NULL
            END AS reimbursement_rate,
            s.status
        FROM silver.sinistres s
        LEFT JOIN silver.contrats c
            ON s.id_contrat = c.id_contrat;
    """,
}


def build_gold():
    print("\\n--- GOLD: building analytical tables ---")

    with engine.begin() as connection:
        for table_name, query in GOLD_QUERIES.items():
            connection.execute(text(query))
            print(f"[GOLD] Table loaded: {table_name}")


if __name__ == "__main__":
    build_gold()
''',
            encoding="utf-8",
        )

    # Python : historisation
    elif file_path == "scripts/historisation.py":
        file.write_text(
            '''import pandas as pd
from sqlalchemy import text

from config import engine

BUSINESS_COLUMNS = [
    "id_adherent",
    "plan_type",
    "start_date",
    "end_date",
    "status",
    "monthly_premium",
]


def get_current_contract(connection, id_contrat):
    query = """
        SELECT *
        FROM silver.contrats_history
        WHERE id_contrat = :id_contrat
          AND is_current = TRUE
    """
    return pd.read_sql_query(
        query,
        connection,
        params={"id_contrat": id_contrat},
    )


def close_current_version(connection, history_id):
    connection.execute(
        text(
            """
            UPDATE silver.contrats_history
            SET valid_to = NOW(),
                is_current = FALSE
            WHERE history_id = :history_id
            """
        ),
        {"history_id": history_id},
    )


def insert_new_version(connection, contract):
    connection.execute(
        text(
            """
            INSERT INTO silver.contrats_history
            (
                id_contrat,
                id_adherent,
                plan_type,
                start_date,
                end_date,
                status,
                monthly_premium,
                valid_from,
                valid_to,
                is_current
            )
            VALUES
            (
                :id_contrat,
                :id_adherent,
                :plan_type,
                :start_date,
                :end_date,
                :status,
                :monthly_premium,
                NOW(),
                NULL,
                TRUE
            )
            """
        ),
        {
            "id_contrat": contract["id_contrat"],
            "id_adherent": contract["id_adherent"],
            "plan_type": contract["plan_type"],
            "start_date": contract["start_date"],
            "end_date": contract["end_date"],
            "status": contract["status"],
            "monthly_premium": contract["monthly_premium"],
        },
    )


def process_contract(connection, contract):
    current = get_current_contract(
        connection,
        contract["id_contrat"],
    )

    if current.empty:
        insert_new_version(connection, contract)
        print(f"[SCD2] New version created: {contract['id_contrat']}")
        return

    current_record = current.iloc[0]

    has_changed = any(
        str(current_record[column]) != str(contract[column])
        for column in BUSINESS_COLUMNS
    )

    if has_changed:
        close_current_version(
            connection,
            current_record["history_id"],
        )
        insert_new_version(connection, contract)
        print(f"[SCD2] Change detected: {contract['id_contrat']}")
    else:
        print(f"[SCD2] No change: {contract['id_contrat']}")


def run_historization():
    contracts = pd.read_sql(
        "SELECT * FROM silver.contrats",
        engine,
    )

    with engine.begin() as connection:
        for _, contract in contracts.iterrows():
            process_contract(connection, contract)


if __name__ == "__main__":
    run_historization()
''',
            encoding="utf-8",
        )

    # Python : contrôles qualité
    elif file_path == "scripts/run_quality_checks.py":
        file.write_text(
            '''import pandas as pd

from config import engine

CHECKS = []


def quality_check(name):
    def decorator(func):
        CHECKS.append((name, func))
        return func
    return decorator


@quality_check("No duplicate members")
def check_duplicate_members():
    return pd.read_sql(
        """
        SELECT id_adherent
        FROM silver.adherents
        GROUP BY id_adherent
        HAVING COUNT(*) > 1
        """,
        engine,
    )


@quality_check("No duplicate contracts")
def check_duplicate_contracts():
    return pd.read_sql(
        """
        SELECT id_contrat
        FROM silver.contrats
        GROUP BY id_contrat
        HAVING COUNT(*) > 1
        """,
        engine,
    )


@quality_check("No duplicate claims")
def check_duplicate_claims():
    return pd.read_sql(
        """
        SELECT id_sinistre
        FROM silver.sinistres
        GROUP BY id_sinistre
        HAVING COUNT(*) > 1
        """,
        engine,
    )


@quality_check("No negative amounts")
def check_negative_amounts():
    return pd.read_sql(
        """
        SELECT id_sinistre
        FROM silver.sinistres
        WHERE claimed_amount < 0
           OR reimbursed_amount < 0
        """,
        engine,
    )


@quality_check("Reimbursement must not exceed claimed amount")
def check_reimbursement_consistency():
    return pd.read_sql(
        """
        SELECT id_sinistre
        FROM silver.sinistres
        WHERE reimbursed_amount > claimed_amount
        """,
        engine,
    )


@quality_check("Incident date must not be after declaration date")
def check_claim_dates():
    return pd.read_sql(
        """
        SELECT id_sinistre
        FROM silver.sinistres
        WHERE incident_date > declaration_date
        """,
        engine,
    )


@quality_check("Every claim must have a contract")
def check_claim_contract():
    return pd.read_sql(
        """
        SELECT s.id_sinistre
        FROM silver.sinistres s
        LEFT JOIN silver.contrats c
            ON s.id_contrat = c.id_contrat
        WHERE c.id_contrat IS NULL
        """,
        engine,
    )


@quality_check("Every contract must have a member")
def check_contract_member():
    return pd.read_sql(
        """
        SELECT c.id_contrat
        FROM silver.contrats c
        LEFT JOIN silver.adherents m
            ON c.id_adherent = m.id_adherent
        WHERE m.id_adherent IS NULL
        """,
        engine,
    )


def run_quality_checks():
    print("\\n========== DATA QUALITY CHECKS ==========")
    failures = 0

    for name, check in CHECKS:
        result = check()

        if result.empty:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}")
            print(result.to_string(index=False))

    print("==========================================")
    print(f"Failed checks: {failures}")

    return failures


if __name__ == "__main__":
    failures = run_quality_checks()
    raise SystemExit(1 if failures > 0 else 0)
''',
            encoding="utf-8",
        )

    # Python : orchestration
    elif file_path == "scripts/run_pipeline.py":
        file.write_text(
            '''import subprocess
import sys

PIPELINE_STEPS = [
    "scripts/load_bronze.py",
    "scripts/transform_silver.py",
    "scripts/build_gold.py",
    "scripts/historisation.py",
    "scripts/run_quality_checks.py",
]


def run_pipeline():
    for step in PIPELINE_STEPS:
        print(f"\\n>>> Running: {step}")

        result = subprocess.run([sys.executable, step])

        if result.returncode != 0:
            raise SystemExit(
                f"Pipeline stopped at step: {step}"
            )

    print("\\nAPI -> Bronze -> Silver -> Gold pipeline completed.")


if __name__ == "__main__":
    run_pipeline()
''',
            encoding="utf-8",
        )

    # Tests qualité
    elif file_path == "tests/test_data_quality.py":
        file.write_text(
            '''import pandas as pd

from config import engine


def test_no_duplicate_members():
    df = pd.read_sql(
        "SELECT id_adherent FROM silver.adherents",
        engine,
    )
    assert df["id_adherent"].is_unique


def test_no_duplicate_contracts():
    df = pd.read_sql(
        "SELECT id_contrat FROM silver.contrats",
        engine,
    )
    assert df["id_contrat"].is_unique


def test_no_duplicate_claims():
    df = pd.read_sql(
        "SELECT id_sinistre FROM silver.sinistres",
        engine,
    )
    assert df["id_sinistre"].is_unique


def test_no_negative_amounts():
    df = pd.read_sql(
        """
        SELECT id_sinistre
        FROM silver.sinistres
        WHERE claimed_amount < 0
           OR reimbursed_amount < 0
        """,
        engine,
    )
    assert df.empty


def test_reimbursement_not_greater_than_claimed_amount():
    df = pd.read_sql(
        """
        SELECT id_sinistre
        FROM silver.sinistres
        WHERE reimbursed_amount > claimed_amount
        """,
        engine,
    )
    assert df.empty
''',
            encoding="utf-8",
        )

    # Fichiers vides
    else:
        file.write_text("", encoding="utf-8")

    print(f"✅ Fichier créé : {file}")


print("\\n🎉 Structure du projet mutuelle créée avec succès.")
print(f"📂 Chemin du projet : {base.resolve()}")