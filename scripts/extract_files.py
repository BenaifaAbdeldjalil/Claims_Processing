import json
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