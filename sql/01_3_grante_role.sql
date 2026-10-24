 -- =============================================
-- Create a read/write role for mutuelle_db
-- =============================================

-- 2. Allow connection to the database
GRANT CONNECT ON DATABASE mutuelle_db TO mutuelle_rw;

-- 3. Allow usage of the schemas
GRANT USAGE ON SCHEMA bronze TO mutuelle_rw;
GRANT USAGE ON SCHEMA silver TO mutuelle_rw;
GRANT USAGE ON SCHEMA gold TO mutuelle_rw;

-- 4. Grant read/write privileges on existing tables
GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA bronze
TO mutuelle_rw;

GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA silver
TO mutuelle_rw;

GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA gold
TO mutuelle_rw;

-- 5. Grant privileges on sequences
GRANT USAGE, SELECT
ON ALL SEQUENCES IN SCHEMA bronze
TO mutuelle_rw;

GRANT USAGE, SELECT
ON ALL SEQUENCES IN SCHEMA silver
TO mutuelle_rw;

GRANT USAGE, SELECT
ON ALL SEQUENCES IN SCHEMA gold
TO mutuelle_rw;

-- 6. Apply the same privileges to future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA bronze
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO mutuelle_rw;

ALTER DEFAULT PRIVILEGES IN SCHEMA bronze
GRANT USAGE, SELECT ON SEQUENCES TO mutuelle_rw;

ALTER DEFAULT PRIVILEGES IN SCHEMA silver
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO mutuelle_rw;

ALTER DEFAULT PRIVILEGES IN SCHEMA silver
GRANT USAGE, SELECT ON SEQUENCES TO mutuelle_rw;

ALTER DEFAULT PRIVILEGES IN SCHEMA gold
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO mutuelle_rw;

ALTER DEFAULT PRIVILEGES IN SCHEMA gold
GRANT USAGE, SELECT ON SEQUENCES TO mutuelle_rw;