import requests
import pandas as pd
from config import API_BASE_URL, API_TABLES

PAGE_SIZE = 100
MAX_PAGES = 20
TIMEOUT = 30


def extract_records_from_payload(payload):
    """
    Extract the record list regardless of the API response structure.
    """
    if isinstance(payload, list):
        return payload

    for key in ["data", "rows", "results", "records", "items"]:
        if isinstance(payload, dict) and isinstance(payload.get(key), list):
            return payload[key]

    return []


def extract_table(domain: str, api_table: str) -> pd.DataFrame:
    """
    Retrieve all available pages for one API table.
    """
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
    """Extract all three domains from the API."""
    datasets = {}

    for domain, api_table in API_TABLES.items():
        print(f"\n--- API extraction: {domain} ({api_table}) ---")
        datasets[domain] = extract_table(domain, api_table)

    return datasets


if __name__ == "__main__":
    datasets = extract_all_domains()

    for domain, df in datasets.items():
        print(f"\n{domain}: {len(df)} rows")
        print("Columns:", list(df.columns))
        print(df.head())