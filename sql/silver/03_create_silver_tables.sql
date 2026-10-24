CREATE TABLE IF NOT EXISTS mutuelle_silver.adherents (
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

CREATE TABLE IF NOT EXISTS mutuelle_silver.contrats (
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

CREATE TABLE IF NOT EXISTS mutuelle_silver.sinistres (
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

CREATE TABLE IF NOT EXISTS mutuelle_silver.contrats_history (
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
ON mutuelle_silver.contrats_history (id_contrat);

CREATE INDEX IF NOT EXISTS idx_contrats_history_current
ON mutuelle_silver.contrats_history (id_contrat, is_current);