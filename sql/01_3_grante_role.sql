-- =============================================
-- Grant all privileges to mutuelle_rw
-- Schemas: mutuelle_bronze, mutuelle_silver, mutuelle_gold
-- =============================================

-- 1. Grant all privileges on the schemas
GRANT ALL PRIVILEGES ON SCHEMA mutuelle_bronze TO mutuelle_rw;
GRANT ALL PRIVILEGES ON SCHEMA mutuelle_silver TO mutuelle_rw;
GRANT ALL PRIVILEGES ON SCHEMA mutuelle_gold TO mutuelle_rw;

-- 2. Grant all privileges on existing tables and views
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA mutuelle_bronze TO mutuelle_rw;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA mutuelle_silver TO mutuelle_rw;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA mutuelle_gold TO mutuelle_rw;

-- 3. Grant all privileges on existing sequences
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA mutuelle_bronze TO mutuelle_rw;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA mutuelle_silver TO mutuelle_rw;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA mutuelle_gold TO mutuelle_rw;

-- 4. Grant all privileges on existing functions and procedures
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA mutuelle_bronze TO mutuelle_rw;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA mutuelle_silver TO mutuelle_rw;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA mutuelle_gold TO mutuelle_rw;

-- 5. Apply the same privileges to future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA mutuelle_bronze
GRANT ALL PRIVILEGES ON TABLES TO mutuelle_rw;

ALTER DEFAULT PRIVILEGES IN SCHEMA mutuelle_silver
GRANT ALL PRIVILEGES ON TABLES TO mutuelle_rw;

ALTER DEFAULT PRIVILEGES IN SCHEMA mutuelle_gold
GRANT ALL PRIVILEGES ON TABLES TO mutuelle_rw;

-- 6. Apply the same privileges to future sequences
ALTER DEFAULT PRIVILEGES IN SCHEMA mutuelle_bronze
GRANT ALL PRIVILEGES ON SEQUENCES TO mutuelle_rw;

ALTER DEFAULT PRIVILEGES IN SCHEMA mutuelle_silver
GRANT ALL PRIVILEGES ON SEQUENCES TO mutuelle_rw;

ALTER DEFAULT PRIVILEGES IN SCHEMA mutuelle_gold
GRANT ALL PRIVILEGES ON SEQUENCES TO mutuelle_rw;

-- 7. Apply the same privileges to future functions
ALTER DEFAULT PRIVILEGES IN SCHEMA mutuelle_bronze
GRANT ALL PRIVILEGES ON FUNCTIONS TO mutuelle_rw;

ALTER DEFAULT PRIVILEGES IN SCHEMA mutuelle_silver
GRANT ALL PRIVILEGES ON FUNCTIONS TO mutuelle_rw;

ALTER DEFAULT PRIVILEGES IN SCHEMA mutuelle_gold
GRANT ALL PRIVILEGES ON FUNCTIONS TO mutuelle_rw;