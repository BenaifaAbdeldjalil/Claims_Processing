CREATE TABLE IF NOT EXISTS gold.dim_members (
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