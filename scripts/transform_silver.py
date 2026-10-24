import json
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
    "adherents": "adherents",
    "contrats": "contrats",
    "sinistres": "sinistres",
}

SILVER_SCHEMA = "mutuelle_silver"

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
        FROM mutuelle_bronze.{domain}
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
    print(f"\n--- SILVER: {domain} ---")

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
        schema=SILVER_SCHEMA,   # ← le schéma est séparé
        if_exists="append",
        index=False,
    )

    print(f"[SILVER] {len(df)} rows loaded into {table_name}")


def run_silver_transformation():
    for domain in DOMAINS:
        transform_domain(domain)


if __name__ == "__main__":
    run_silver_transformation()