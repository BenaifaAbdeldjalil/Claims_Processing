<!DOCTYPE html>
<html lang="en">

<div align="center">
  <h1> 30 Days Of Python: Day 2 - Variables, Builtin Functions</h1>
  <a class="header-badge" target="_blank" href="https://www.linkedin.com/in/abdeldjalil-benaifa-87b6a6132/">
  <img src="https://img.shields.io/badge/style--5eba00.svg?label=LinkedIn&logo=linkedin&style=social">
  </a>

<sub>Author:
<a href="https://www.linkedin.com/in/abdeldjalil-benaifa-87b6a6132/" target="_blank">Abdeldjalil Benaifa</a><br>
<small> First Edition: September, 2026</small>
</sub>
</div>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mutuelle Data Project - Bronze / Silver / Gold</title>

    <style>
        :root {
            --primary: #1f4e79;
            --secondary: #2e75b6;
            --light: #f4f7fb;
            --border: #d9e2ec;
            --text: #243b53;
            --code-bg: #0f172a;
            --code-text: #e2e8f0;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: "Segoe UI", Arial, sans-serif;
            background-color: var(--light);
            color: var(--text);
            line-height: 1.6;
        }

        header {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 48px 24px;
            text-align: center;
        }

        header h1 {
            margin: 0 0 12px;
            font-size: 34px;
        }

        header p {
            margin: 0;
            font-size: 18px;
            opacity: 0.9;
        }

        main {
            max-width: 1100px;
            margin: 0 auto;
            padding: 32px 24px 64px;
        }

        section {
            background: white;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 28px;
            margin-bottom: 28px;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.05);
        }

        h2 {
            color: var(--primary);
            border-bottom: 2px solid var(--border);
            padding-bottom: 10px;
            margin-top: 0;
        }

        h3 {
            color: var(--secondary);
            margin-bottom: 10px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 15px;
        }

        th, td {
            border: 1px solid var(--border);
            padding: 10px 12px;
            text-align: left;
            vertical-align: top;
        }

        th {
            background-color: #eaf1f8;
            color: var(--primary);
        }

        tr:nth-child(even) {
            background-color: #fafcff;
        }

        pre {
            background-color: var(--code-bg);
            color: var(--code-text);
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 14px;
            line-height: 1.5;
        }

        code {
            font-family: Consolas, Monaco, "Courier New", monospace;
        }

        p code, li code, td code {
            background-color: #eef2f7;
            color: #b91c1c;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 13px;
        }

        pre code {
            background: none;
            color: inherit;
            padding: 0;
        }

        ul {
            padding-left: 22px;
        }

        li {
            margin-bottom: 6px;
        }

        .badge {
            display: inline-block;
            background-color: var(--secondary);
            color: white;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 13px;
            margin-right: 8px;
        }

        .architecture {
            background-color: #f8fafc;
            border: 1px dashed var(--secondary);
            border-radius: 8px;
            padding: 16px;
            font-family: Consolas, monospace;
            white-space: pre;
            overflow-x: auto;
        }

        footer {
            text-align: center;
            padding: 24px;
            color: #64748b;
            font-size: 14px;
        }

        @media (max-width: 700px) {
            header h1 {
                font-size: 26px;
            }

            section {
                padding: 20px;
            }

            table {
                font-size: 13px;
            }
        }
    </style>
</head>
<body>

<header>
    <h1>Mutuelle Data Project</h1>
    <p>End-to-end data pipeline: API & files → Bronze → Silver → Gold → PostgreSQL</p>
</header>

<main>

    <section>
        <h2>Overview</h2>

        <p>
            This project is a complete, hands-on data engineering project built around a
            <strong>health insurance / mutuelle</strong> business domain.
            It collects data from a free public API and local files, stores raw data,
            cleans and models it, then builds analytical tables and KPIs in PostgreSQL.
        </p>

        <p>
            <span class="badge">Python</span>
            <span class="badge">Pandas</span>
            <span class="badge">PostgreSQL</span>
            <span class="badge">SQLAlchemy</span>
            <span class="badge">Bronze / Silver / Gold</span>
            <span class="badge">Data Quality</span>
            <span class="badge">SCD Type 2</span>
        </p>

        <h3>Objectives</h3>
        <ul>
            <li>Collect data from an API, CSV, Excel, and JSON files.</li>
            <li>Store raw source data in JSON files and PostgreSQL Bronze tables.</li>
            <li>Clean, type, normalize, and deduplicate data in the Silver layer.</li>
            <li>Build analytical fact and dimension tables in the Gold layer.</li>
            <li>Implement automated data-quality checks.</li>
            <li>Track contract changes using SCD Type 2 historization.</li>
            <li>Answer business questions about claims, reimbursements, and portfolio performance.</li>
        </ul>
    </section>

    <section>
        <h2>Business Domain</h2>

        <p>
            The project focuses on a health insurance company with three main business objects:
            <strong>members</strong>, <strong>contracts</strong>, and <strong>claims</strong>.
        </p>

        <table>
            <thead>
                <tr>
                    <th>Domain</th>
                    <th>Description</th>
                    <th>Main fields</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Members</td>
                    <td>People affiliated with the health insurance company</td>
                    <td>
                        <code>id_adherent</code>,
                        <code>last_name</code>,
                        <code>first_name</code>,
                        <code>date_of_birth</code>,
                        <code>gender</code>,
                        <code>enrollment_date</code>,
                        <code>status</code>,
                        <code>email</code>
                    </td>
                </tr>
                <tr>
                    <td>Contracts</td>
                    <td>Insurance contracts subscribed by members</td>
                    <td>
                        <code>id_contrat</code>,
                        <code>id_adherent</code>,
                        <code>plan_type</code>,
                        <code>start_date</code>,
                        <code>end_date</code>,
                        <code>status</code>,
                        <code>monthly_premium</code>
                    </td>
                </tr>
                <tr>
                    <td>Claims</td>
                    <td>Reimbursement requests linked to a contract</td>
                    <td>
                        <code>id_sinistre</code>,
                        <code>id_contrat</code>,
                        <code>id_adherent</code>,
                        <code>incident_date</code>,
                        <code>declaration_date</code>,
                        <code>claim_type</code>,
                        <code>claimed_amount</code>,
                        <code>reimbursed_amount</code>,
                        <code>status</code>
                    </td>
                </tr>
            </tbody>
        </table>

        <h3>Business Rules</h3>
        <ul>
            <li>A member can have one or more contracts.</li>
            <li>A contract belongs to one main member.</li>
            <li>A claim is linked to one contract and one member.</li>
            <li>A claim can be <code>SUBMITTED</code>, <code>IN_REVIEW</code>, <code>APPROVED</code>, <code>DENIED</code>, or <code>REIMBURSED</code>.</li>
            <li>A contract can be <code>ACTIVE</code>, <code>PENDING</code>, <code>CANCELLED</code>, or <code>EXPIRED</code>.</li>
            <li>The incident date must not be later than the declaration date.</li>
            <li>The reimbursed amount must be positive and must not exceed the claimed amount.</li>
            <li>The monthly premium must be positive.</li>
        </ul>
    </section>

    <section>
        <h2>Architecture</h2>

        <p>
            The project follows a medallion architecture with three layers:
            <strong>Bronze</strong>, <strong>Silver</strong>, and <strong>Gold</strong>.
        </p>

        <div class="architecture">
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
        </div>

        <table>
            <thead>
                <tr>
                    <th>Layer</th>
                    <th>Purpose</th>
                    <th>Rules</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Bronze</td>
                    <td>Preserve source data exactly as received</td>
                    <td>
                        No business transformation.
                        Add metadata such as <code>source_system</code>,
                        <code>source_endpoint</code>, and <code>ingestion_date</code>.
                    </td>
                </tr>
                <tr>
                    <td>Silver</td>
                    <td>Prepare trusted and reusable data</td>
                    <td>
                        Clean text, convert dates and amounts,
                        normalize statuses, remove duplicates,
                        and validate business rules.
                    </td>
                </tr>
                <tr>
                    <td>Gold</td>
                    <td>Serve analytics and reporting</td>
                    <td>
                        Build fact tables, dimensions,
                        KPI views, and business indicators.
                    </td>
                </tr>
            </tbody>
        </table>
    </section>

    <section>
        <h2>API Data Source</h2>

        <p>
            The main external source is the free
            <strong>Claims Processing Insights API</strong> from
            <code>databasesample.com</code>.
            It provides claims, policies, and beneficiaries data without requiring an API key.
        </p>

        <table>
            <thead>
                <tr>
                    <th>Mutuelle domain</th>
                    <th>API table</th>
                    <th>Silver target table</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Claims</td>
                    <td><code>claims</code></td>
                    <td><code>silver.sinistres</code></td>
                </tr>
                <tr>
                    <td>Contracts</td>
                    <td><code>policies</code></td>
                    <td><code>silver.contrats</code></td>
                </tr>
                <tr>
                    <td>Members</td>
                    <td><code>beneficiaries</code></td>
                    <td><code>silver.adherents</code></td>
                </tr>
            </tbody>
        </table>

        <h3>API endpoints</h3>

        <pre><code>https://databasesample.com/api/v1/datasets/claims-processing-insights/tables/claims/rows?limit=100
https://databasesample.com/api/v1/datasets/claims-processing-insights/tables/policies/rows?limit=100
https://databasesample.com/api/v1/datasets/claims-processing-insights/tables/beneficiaries/rows?limit=100</code></pre>

        <h3>Field mapping</h3>

        <table>
            <thead>
                <tr>
                    <th>API field</th>
                    <th>Target field</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>claims.id</code></td>
                    <td><code>id_sinistre</code></td>
                    <td>Claim identifier</td>
                </tr>
                <tr>
                    <td><code>claims.policy_id</code></td>
                    <td><code>id_contrat</code></td>
                    <td>Linked contract</td>
                </tr>
                <tr>
                    <td><code>claims.amount</code></td>
                    <td><code>claimed_amount</code></td>
                    <td>Claimed amount</td>
                </tr>
                <tr>
                    <td><code>claims.status</code></td>
                    <td><code>status</code></td>
                    <td>Claim status</td>
                </tr>
                <tr>
                    <td><code>policies.id</code></td>
                    <td><code>id_contrat</code></td>
                    <td>Contract identifier</td>
                </tr>
                <tr>
                    <td><code>policies.beneficiary_id</code></td>
                    <td><code>id_adherent</code></td>
                    <td>Linked member</td>
                </tr>
                <tr>
                    <td><code>policies.policy_type</code></td>
                    <td><code>plan_type</code></td>
                    <td>Insurance plan</td>
                </tr>
                <tr>
                    <td><code>beneficiaries.id</code></td>
                    <td><code>id_adherent</code></td>
                    <td>Member identifier</td>
                </tr>
            </tbody>
        </table>
    </section>

    <section>
        <h2>Project Structure</h2>

        <pre><code>mutuelle-api-project/
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
└── README.html</code></pre>
    </section>

    <section>
        <h2>Installation</h2>

        <h3>1. Create a Python virtual environment</h3>

        <pre><code>python -m venv .venv
source .venv/bin/activate</code></pre>

        <p>On Windows:</p>

        <pre><code>python -m venv .venv
.venv\Scripts\activate</code></pre>

        <h3>2. Install dependencies</h3>

        <pre><code>pip install pandas sqlalchemy psycopg2-binary requests python-dotenv openpyxl pytest</code></pre>

        <h3>3. Create the PostgreSQL database</h3>

        <pre><code>CREATE DATABASE mutuelle_db;</code></pre>

        <h3>4. Configure environment variables</h3>

        <p>Create a file named <code>config/.env</code>:</p>

        <pre><code>PG_HOST=localhost
PG_PORT=5432
PG_DB=mutuelle_db
PG_USER=postgres
PG_PASSWORD=your_password</code></pre>
    </section>

    <section>
        <h2>Database Schemas</h2>

        <pre><code>CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;</code></pre>

        <table>
            <thead>
                <tr>
                    <th>Schema</th>
                    <th>Content</th>
                    <th>Example tables</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>bronze</code></td>
                    <td>Raw API and file data stored as JSONB</td>
                    <td>
                        <code>bronze.adherents</code>,
                        <code>bronze.contrats</code>,
                        <code>bronze.sinistres</code>
                    </td>
                </tr>
                <tr>
                    <td><code>silver</code></td>
                    <td>Cleaned, typed, and deduplicated business data</td>
                    <td>
                        <code>silver.adherents</code>,
                        <code>silver.contrats</code>,
                        <code>silver.sinistres</code>,
                        <code>silver.contrats_history</code>
                    </td>
                </tr>
                <tr>
                    <td><code>gold</code></td>
                    <td>Analytical tables and KPI views</td>
                    <td>
                        <code>gold.dim_members</code>,
                        <code>gold.fact_contracts</code>,
                        <code>gold.fact_claims</code>
                    </td>
                </tr>
            </tbody>
        </table>
    </section>

    <section>
        <h2>Pipeline Workflow</h2>

        <h3>1. Extract data</h3>
        <p>
            The script <code>extract_api.py</code> queries the API with pagination
            and returns one Pandas DataFrame per domain.
            The script <code>extract_files.py</code> reads local CSV, Excel, and JSON files.
        </p>

        <h3>2. Load Bronze</h3>
        <p>
            The script <code>load_bronze.py</code> saves a raw copy of the data as JSON
            and loads each record into PostgreSQL Bronze tables as JSONB.
        </p>

        <pre><code>python scripts/load_bronze.py</code></pre>

        <h3>3. Transform Silver</h3>
        <p>
            The script <code>transform_silver.py</code> maps API fields to the mutuelle model,
            cleans text and dates, converts amounts, normalizes statuses,
            removes duplicates, and loads trusted data into Silver.
        </p>

        <pre><code>python scripts/transform_silver.py</code></pre>

        <h3>4. Build Gold</h3>
        <p>
            The script <code>build_gold.py</code> creates and loads the analytical tables:
            member dimension, contract fact table, and claims fact table.
        </p>

        <pre><code>python scripts/build_gold.py</code></pre>

        <h3>5. Run quality checks</h3>

        <pre><code>python scripts/run_quality_checks.py</code></pre>

        <h3>6. Run the complete pipeline</h3>

        <pre><code>python scripts/run_pipeline.py</code></pre>
    </section>

    <section>
        <h2>Data Quality Checks</h2>

        <p>
            The pipeline includes automated checks to detect common data issues.
        </p>

        <ul>
            <li>Duplicate member identifiers.</li>
            <li>Duplicate contract identifiers.</li>
            <li>Duplicate claim identifiers.</li>
            <li>Negative claimed or reimbursed amounts.</li>
            <li>Reimbursed amount greater than claimed amount.</li>
            <li>Incident date later than declaration date.</li>
            <li>Claims linked to a non-existing contract.</li>
            <li>Contracts linked to a non-existing member.</li>
            <li>Invalid or non-normalized claim statuses.</li>
        </ul>

        <h3>Example SQL check</h3>

        <pre><code>SELECT id_sinistre
FROM silver.sinistres
WHERE reimbursed_amount > claimed_amount;</code></pre>
    </section>

    <section>
        <h2>Historization - SCD Type 2</h2>

        <p>
            Contract changes are tracked in the table
            <code>silver.contrats_history</code>.
            When a business field changes, the current record is closed and a new version is created.
        </p>

        <table>
            <thead>
                <tr>
                    <th>Field</th>
                    <th>Role</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>valid_from</code></td>
                    <td>Date when the version became active</td>
                </tr>
                <tr>
                    <td><code>valid_to</code></td>
                    <td>Date when the version was closed</td>
                </tr>
                <tr>
                    <td><code>is_current</code></td>
                    <td>Indicates whether the version is the current one</td>
                </tr>
            </tbody>
        </table>

        <h3>Run historization</h3>

        <pre><code>python scripts/historisation.py</code></pre>

        <h3>Check contract history</h3>

        <pre><code>SELECT *
FROM silver.contrats_history
ORDER BY id_contrat, valid_from;</code></pre>
    </section>

    <section>
        <h2>Gold Layer and KPIs</h2>

        <table>
            <thead>
                <tr>
                    <th>Gold object</th>
                    <th>Type</th>
                    <th>Purpose</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><code>gold.dim_members</code></td>
                    <td>Dimension</td>
                    <td>Member information, age, enrollment year, status</td>
                </tr>
                <tr>
                    <td><code>gold.fact_contracts</code></td>
                    <td>Fact table</td>
                    <td>Contract portfolio, premiums, duration, status</td>
                </tr>
                <tr>
                    <td><code>gold.fact_claims</code></td>
                    <td>Fact table</td>
                    <td>Claims, claimed and reimbursed amounts, reimbursement rate</td>
                </tr>
                <tr>
                    <td><code>gold.kpi_active_members</code></td>
                    <td>View</td>
                    <td>Number of active members</td>
                </tr>
                <tr>
                    <td><code>gold.kpi_contracts_by_status</code></td>
                    <td>View</td>
                    <td>Contracts by status</td>
                </tr>
                <tr>
                    <td><code>gold.kpi_contracts_by_plan</code></td>
                    <td>View</td>
                    <td>Contracts and premiums by plan</td>
                </tr>
                <tr>
                    <td><code>gold.kpi_claims_by_type</code></td>
                    <td>View</td>
                    <td>Claims and reimbursement rate by claim type</td>
                </tr>
                <tr>
                    <td><code>gold.kpi_monthly_claims</code></td>
                    <td>View</td>
                    <td>Monthly claims trend</td>
                </tr>
                <tr>
                    <td><code>gold.kpi_top_members_by_reimbursement</code></td>
                    <td>View</td>
                    <td>Top members by reimbursed amount</td>
                </tr>
            </tbody>
        </table>

        <h3>Example KPI query</h3>

        <pre><code>SELECT
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
ORDER BY total_claimed DESC;</code></pre>
    </section>

    <section>
        <h2>Pandas Analysis</h2>

        <p>
            The notebook <code>notebooks/claims_analysis.ipynb</code> connects to PostgreSQL,
            reads the Gold claims table, and performs business analysis with Pandas.
        </p>

        <h3>Example: reimbursement rate by claim type</h3>

        <pre><code>import pandas as pd
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

claims_by_type</code></pre>
    </section>

    <section>
        <h2>Business Questions</h2>

        <ul>
            <li>How many members are active?</li>
            <li>How many contracts are active, cancelled, or pending?</li>
            <li>How are contracts distributed by plan type?</li>
            <li>What is the total claimed amount?</li>
            <li>What is the total reimbursed amount?</li>
            <li>What is the global reimbursement rate?</li>
            <li>What is the reimbursement rate by claim type?</li>
            <li>Which claim types generate the highest costs?</li>
            <li>How do claims evolve month by month?</li>
            <li>Which members receive the highest reimbursements?</li>
            <li>Which contracts have unusually high claim activity?</li>
            <li>Which API records are incomplete or inconsistent?</li>
        </ul>
    </section>

    <section>
        <h2>Final Deliverables</h2>

        <ul>
            <li>PostgreSQL database with <code>bronze</code>, <code>silver</code>, and <code>gold</code> schemas.</li>
            <li>Robust paginated API extraction.</li>
            <li>Raw API data stored as JSONB and JSON files.</li>
            <li>Clean, typed, and deduplicated Silver tables.</li>
            <li>Analytical Gold tables.</li>
            <li>SQL KPI views.</li>
            <li>Automated data-quality checks.</li>
            <li>SCD Type 2 contract historization.</li>
            <li>Pandas analysis notebook.</li>
            <li>Executable end-to-end pipeline.</li>
            <li>Technical documentation.</li>
        </ul>
    </section>

    <section>
        <h2>Recommended Execution Plan</h2>

        <ol>
            <li>Set up Python and PostgreSQL.</li>
            <li>Create <code>mutuelle_db</code> and the three schemas.</li>
            <li>Run <code>extract_api.py</code> to inspect the real API tables and columns.</li>
            <li>Adjust <code>COLUMN_MAPPING</code> if API field names differ.</li>
            <li>Create Bronze tables and run <code>load_bronze.py</code>.</li>
            <li>Create Silver tables and run <code>transform_silver.py</code>.</li>
            <li>Run data-quality checks and fix anomalies.</li>
            <li>Create Gold tables and run <code>build_gold.py</code>.</li>
            <li>Create the KPI views.</li>
            <li>Implement SCD Type 2 historization.</li>
            <li>Create the Pandas analysis notebook.</li>
            <li>Run <code>run_pipeline.py</code> and document the project.</li>
        </ol>
    </section>

    <section>
        <h2>Future Improvements</h2>

        <ul>
            <li><strong>Docker Compose:</strong> containerize PostgreSQL and the Python application.</li>
            <li><strong>Airflow or Prefect:</strong> schedule and monitor the pipeline.</li>
            <li><strong>dbt:</strong> version and test Silver-to-Gold transformations.</li>
            <li><strong>Great Expectations:</strong> define declarative data-quality rules.</li>
            <li><strong>Incremental ingestion:</strong> load only new or updated API records.</li>
            <li><strong>FastAPI:</strong> create a local mock API dedicated to the mutuelle domain.</li>
            <li><strong>Power BI / Metabase:</strong> build dashboards from the Gold layer.</li>
            <li><strong>CI/CD:</strong> automatically run quality tests on every code change.</li>
        </ul>
    </section>

</main>

<footer>
    Mutuelle Data Project — Data Engineering learning project using Python, Pandas, PostgreSQL, and a medallion architecture.
</footer>

</body>
</html>