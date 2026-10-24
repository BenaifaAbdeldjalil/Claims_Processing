 -- =============================================
-- Create a read/write role for mutuelle_db
-- =============================================

-- 2. Allow connection to the database
GRANT CONNECT ON DATABASE Claims_Processing TO mutuelle_rw;

-- 3. Allow usage of the schemas
GRANT USAGE ON SCHEMA mutuelle_bronze TO mutuelle_rw;
GRANT USAGE ON SCHEMA mutuelle_silver TO mutuelle_rw;
GRANT USAGE ON SCHEMA mutuelle_gold TO mutuelle_rw;

-- 4. Grant read/write privileges on existing tables
GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA mutuelle_bronze
TO mutuelle_rw;

GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA mutuelle_silver
TO mutuelle_rw;

GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA mutuelle_gold
TO mutuelle_rw;

-- 5. Grant privileges on sequences
GRANT USAGE, SELECT
ON ALL SEQUENCES IN SCHEMA mutuelle_bronze
TO mutuelle_rw;

GRANT USAGE, SELECT
ON ALL SEQUENCES IN SCHEMA mutuelle_silver
TO mutuelle_rw;

GRANT USAGE, SELECT
ON ALL SEQUENCES IN SCHEMA mutuelle_gold
TO mutuelle_rw;

-- 6. Apply the same privileges to future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA mutuelle_bronze
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO mutuelle_rw;

ALTER DEFAULT PRIVILEGES IN SCHEMA mutuelle_bronze
GRANT USAGE, SELECT ON SEQUENCES TO mutuelle_rw;

ALTER DEFAULT PRIVILEGES IN SCHEMA mutuelle_silver
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO mutuelle_rw;

ALTER DEFAULT PRIVILEGES IN SCHEMA mutuelle_silver
GRANT USAGE, SELECT ON SEQUENCES TO mutuelle_rw;

ALTER DEFAULT PRIVILEGES IN SCHEMA mutuelle_gold
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO mutuelle_rw;

ALTER DEFAULT PRIVILEGES IN SCHEMA mutuelle_gold
GRANT USAGE, SELECT ON SEQUENCES TO mutuelle_rw;