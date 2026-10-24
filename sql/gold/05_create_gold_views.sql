CREATE OR REPLACE VIEW gold.kpi_active_members AS
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
    ) AS global_reimbursement_rate
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