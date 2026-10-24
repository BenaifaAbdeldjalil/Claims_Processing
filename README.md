<!DOCTYPE html>
<html lang="en">

<div align="center">
  <h1> Mutuelle Data Project </h1>
  <a class="header-badge" target="_blank" href="https://www.linkedin.com/in/abdeldjalil-benaifa-87b6a6132/">
  <img src="https://img.shields.io/badge/style--5eba00.svg?label=LinkedIn&logo=linkedin&style=social">
  </a>

<sub>Author:
<a href="https://www.linkedin.com/in/abdeldjalil-benaifa-87b6a6132/" target="_blank">Abdeldjalil Benaifa</a><br>
<small> First Edition: September, 2026</small>
</sub>
</div>

# Mutuelle Data Project

End-to-end data engineering project for a health insurance / mutuelle domain.

The project collects data from a free public API and local files, stores raw data, cleans and models it, then builds analytical tables and KPIs in PostgreSQL using a **Bronze / Silver / Gold** architecture.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue)
![Pandas](https://img.shields.io/badge/Pandas-data%20processing-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-database-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## Project Overview

This project simulates a real data platform for a health insurance company.

It allows you to:

- Collect data from a public API and local CSV, Excel, and JSON files.
- Store raw source data in JSON files and PostgreSQL Bronze tables.
- Clean, type, normalize, and deduplicate data in the Silver layer.
- Build analytical fact and dimension tables in the Gold layer.
- Implement automated data-quality checks.
- Track contract changes using SCD Type 2 historization.
- Analyze claims, reimbursements, and portfolio performance.

## Tech Stack

| Technology | Usage |
|---|---|
| Python | Data extraction, transformation, and orchestration |
| Pandas | Data manipulation and analysis |
| PostgreSQL | Data storage and analytical queries |
| SQLAlchemy | Python-to-PostgreSQL connection |
| Requests | API ingestion |
| pytest | Automated data-quality tests |
| JSON / CSV | Raw data storage |

## Architecture

The project follows a medallion architecture:

```text
databasesample.com API          CSV / Excel / JSON files
            |                              |
            +--------------+---------------+
                           |
                           v
                        BRONZE
            Raw API JSON + raw source files
                           |
                           v
                        SILVER
            Cleaning, typing, mapping, deduplication
                           |
                           v
                         GOLD
            Fact tables, dimensions, KPIs, reporting
```

| Layer | Purpose | Rules |
|---|---|---|
| Bronze | Preserve source data | No business transformation; add ingestion metadata |
| Silver | Prepare trusted data | Clean, type, normalize, deduplicate, validate |
| Gold | Serve analytics | Fact tables, dimensions, KPIs, reporting views |

## Business Domain

The project focuses on three main business objects:

| Domain | Description | Main fields |
|---|---|---|
| Members | People affiliated with the health insurance company | `id_adherent`, `last_name`, `first_name`, `date_of_birth`, `gender`, `enrollment_date`, `status`, `email` |
| Contracts | Insurance contracts subscribed by members | `id_contrat`, `id_adherent`, `plan_type`, `start_date`, `end_date`, `status`, `monthly_premium` |
| Claims | Reimbursement requests linked to a contract | `id_sinistre`, `id_contrat`, `id_adherent`, `incident_date`, `declaration_date`, `claim_type`, `claimed_amount`, `reimbursed_amount`, `status` |

## Business Rules

- A member can have one or more contracts.
- A contract belongs to one main member.
- A claim is linked to one contract and one member.
- A claim can be `SUBMITTED`, `IN_REVIEW`, `APPROVED`, `DENIED`, or `REIMBURSED`.
- A contract can be `ACTIVE`, `PENDING`, `CANCELLED`, or `EXPIRED`.
- The incident date must not be later than the declaration date.
- The reimbursed amount must be positive and must not exceed the claimed amount.
- The monthly premium must be positive.

## API Data Source

The main external source is the free **Claims Processing Insights API** from `databasesample.com`.

| Mutuelle domain | API table | Silver target table |
|---|---|---|
| Claims | `claims` | `silver.sinistres` |
| Contracts | `policies` | `silver.contrats` |
| Members | `beneficiaries` | `silver.adherents` |

Example API endpoint:

```text
[https://databasesample.com/api/v1/datasets/claims-processing-insights/tables/claims/rows?limit=100](https://databasesample.com/api/v1/datasets/claims-processing-insights/tables/claims/rows?limit=100)
```

### Field Mapping

| API field | Target field | Description |
|---|---|---|
| `claims.id` | `id_sinistre` | Claim identifier |
| `claims.policy_id` | `id_contrat` | Linked contract |
| `claims.amount` | `claimed_amount` | Claimed amount |
| `claims.status` | `status` | Claim status |
| `policies.id` | `id_contrat` | Contract identifier |
| `policies.beneficiary_id` | `id_adherent` | Linked member |
| `policies.policy_type` | `plan_type` | Insurance plan |
| `beneficiaries.id` | `id_adherent` | Member identifier |

## Project Structure

```text
mutuelle-api-project/
│
├── config/
│   └── .env
│
├── data/
│   ├── raw/
│   │   ├── adherents/
│   │   ├── contrats/
│   │   └── sinistres/
│   ├── bronze/
│   │   ├── adherents/
│   │   ├── contrats/
│   │   └── sinistres/
│   └── logs/
│
├── sql/
│   ├── 01_create_schemas.sql
│   ├── 02_create_bronze.sql
│   ├── 03_create_silver.sql
│   ├── 04_create_gold.sql
│   └── 05_create_gold_views.sql
│
├── scripts/
│   ├── config.py
│   ├── extract_api.py
│   ├── extract_files.py
│   ├── load_bronze.py
│   ├── transform_silver.py
│   ├── build_gold.py
│   ├── historisation.py
│   ├── run_quality_checks.py
│   └── run_pipeline.py
│
├── tests/
│   └── test_data_quality.py
│
├── notebooks/
│   └── claims_analysis.ipynb
│
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone [https://github.com/your-username/mutuelle-data-project.git](https://github.com/your-username/mutuelle-data-project.git)
cd mutuelle-data-project
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

```sql
CREATE DATABASE mutuelle_db;
```

### 5. Configure environment variables

Create a file named `config/.env`:

```env
PG_HOST=localhost
PG_PORT=5432
PG_DB=mutuelle_db
PG_USER=postgres
PG_PASSWORD=your_password
```

> Never commit the `.env` file to GitHub. It must be listed in `.gitignore`.

## Database Schemas

```sql
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
```

| Schema | Content | Example tables |
|---|---|---|
| `bronze` | Raw API and file data stored as JSONB | `bronze.adherents`, `bronze.contrats`, `bronze.sinistres` |
| `silver` | Cleaned, typed, and deduplicated business data | `silver.adherents`, `silver.contrats`, `silver.sinistres`, `silver.contrats_history` |
| `gold` | Analytical tables and KPI views | `gold.dim_members`, `gold.fact_contracts`, `gold.fact_claims` |

## Pipeline Workflow

### 1. Extract API data

```bash
python scripts/extract_api.py
```

### 2. Load data into Bronze

```bash
python scripts/load_bronze.py
```

### 3. Transform data into Silver

```bash
python scripts/transform_silver.py
```

### 4. Build the Gold layer

```bash
python scripts/build_gold.py
```

### 5. Run data-quality checks

```bash
python scripts/run_quality_checks.py
```

### 6. Run contract historization

```bash
python scripts/historisation.py
```

### 7. Run the complete pipeline

```bash
python scripts/run_pipeline.py
```

## Data Quality Checks

The pipeline includes automated checks for:

- Duplicate member identifiers.
- Duplicate contract identifiers.
- Duplicate claim identifiers.
- Negative claimed or reimbursed amounts.
- Reimbursed amount greater than claimed amount.
- Incident date later than declaration date.
- Claims linked to a non-existing contract.
- Contracts linked to a non-existing member.
- Invalid or non-normalized claim statuses.

Example SQL check:

```sql
SELECT id_sinistre
FROM silver.sinistres
WHERE reimbursed_amount > claimed_amount;
```

## Historization - SCD Type 2

Contract changes are tracked in `silver.contrats_history`.

When a business field changes:

1. The current record is closed with `valid_to = NOW()`.
2. `is_current` is set to `FALSE`.
3. A new version is inserted with `valid_from = NOW()` and `is_current = TRUE`.

Run historization:

```bash
python scripts/historisation.py
```

Check contract history:

```sql
SELECT *
FROM silver.contrats_history
ORDER BY id_contrat, valid_from;
```

## Gold Layer and KPIs

| Gold object | Type | Purpose |
|---|---|---|
| `gold.dim_members` | Dimension | Member information, age, enrollment year, status |
| `gold.fact_contracts` | Fact table | Contract portfolio, premiums, duration, status |
| `gold.fact_claims` | Fact table | Claims, claimed and reimbursed amounts, reimbursement rate |
| `gold.kpi_active_members` | View | Number of active members |
| `gold.kpi_contracts_by_status` | View | Contracts by status |
| `gold.kpi_contracts_by_plan` | View | Contracts and premiums by plan |
| `gold.kpi_claims_by_type` | View | Claims and reimbursement rate by claim type |
| `gold.kpi_monthly_claims` | View | Monthly claims trend |
| `gold.kpi_top_members_by_reimbursement` | View | Top members by reimbursed amount |

### Example KPI query

```sql
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
```

## Pandas Analysis

The notebook `notebooks/claims_analysis.ipynb` connects to PostgreSQL and analyzes the Gold claims table.

```python
import pandas as pd
from config import engine

df = pd.read_sql(
    "SELECT * FROM gold.fact_claims",
    engine,
)

claims_by_type = (
    df.groupby("claim_type")
    .agg(
        claim_count=("id_sinistre", "count"),
        total_claimed=("claimed_amount", "sum"),
        total_reimbursed=("reimbursed_amount", "sum"),
    )
    .assign(
        reimbursement_rate=lambda x: (
            x["total_reimbursed"] / x["total_claimed"] * 100
        ).round(2)
    )
    .sort_values("total_claimed", ascending=False)
)

claims_by_type
```

## Business Questions

- How many members are active?
- How many contracts are active, cancelled, or pending?
- How are contracts distributed by plan type?
- What is the total claimed amount?
- What is the total reimbursed amount?
- What is the global reimbursement rate?
- What is the reimbursement rate by claim type?
- Which claim types generate the highest costs?
- How do claims evolve month by month?
- Which members receive the highest reimbursements?
- Which contracts have unusually high claim activity?
- Which API records are incomplete or inconsistent?

## Future Improvements

- Docker Compose for PostgreSQL and the Python application.
- Airflow or Prefect for pipeline scheduling and monitoring.
- dbt for versioned and tested Silver-to-Gold transformations.
- Great Expectations for declarative data-quality rules.
- Incremental ingestion for new or updated API records.
- FastAPI for a local mock mutuelle API.
- Power BI or Metabase dashboards based on the Gold layer.
- CI/CD to automatically run quality tests.

## License

This project is for learning and portfolio purposes.