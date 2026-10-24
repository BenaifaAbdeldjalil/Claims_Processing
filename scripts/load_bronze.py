import json
import math
from datetime import datetime

import numpy as np
import pandas as pd

from config import BRONZE_DIR, DOMAINS, engine
from extract_api import extract_all_domains
from extract_files import extract_domain

def sanitize_value(v):
    if isinstance(v, dict):
        return {k: sanitize_value(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [sanitize_value(x) for x in v]
    if isinstance(v, str):
        # Tenter de parser comme JSON
        s = v.strip()
        if s.startswith(("{", "[")):
            try:
                parsed = json.loads(s)
                cleaned = sanitize_value(parsed)
                return json.dumps(cleaned, ensure_ascii=False, default=str, allow_nan=False)
            except (json.JSONDecodeError, ValueError):
                # Remplacement brut des NaN dans la chaîne
                return s.replace(": NaN", ": null").replace(":NaN", ":null").replace("[NaN", "[null")
        return v
    # Détection NaN/NA/NaT
    try:
        if pd.isna(v):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(v, (float, np.floating)):
        if math.isnan(v) or math.isinf(v):
            return None
        return float(v)
    if isinstance(v, np.integer):
        return int(v)
    if isinstance(v, np.bool_):
        return bool(v)
    return v

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

    clean_df = df.copy()
    clean_df = clean_df.map(sanitize_value)

    clean_df.to_json(
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
    """Load each raw record into mutuelle_bronze.<domain> as JSONB."""
    records = []

    for _, row in df.iterrows():
        raw_record = sanitize_value(row.to_dict())

        records.append(
            {
                "source_system": source_system,
                "source_endpoint": source_endpoint,
                "raw_data": json.dumps(
                    raw_record,
                    ensure_ascii=False,
                    default=str,
                    allow_nan=False,
                ),
            }
        )

    bronze_df = pd.DataFrame(records)

    bronze_df.to_sql(
        name=domain,
        con=engine,
        schema="mutuelle_bronze",
        if_exists="append",
        index=False,
    )

    return len(bronze_df)


def run_bronze_load():
    # 1. API sources
    api_datasets = extract_all_domains()

    for domain, df in api_datasets.items():
        print(f"\n[BRONZE-API] Domain: {domain}")

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

    # 2. Local file sources
    for domain in DOMAINS:
        try:
            df = extract_domain(domain)
        except FileNotFoundError:
            print(f"\n[BRONZE-FILE] No local file for {domain}")
            continue

        print(f"\n[BRONZE-FILE] Domain: {domain}")

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

