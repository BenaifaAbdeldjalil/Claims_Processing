 -- =============================================
-- Create a read/write role for mutuelle_db
-- =============================================

-- 1. Create the role
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_roles
        WHERE rolname = 'mutuelle_rw'
    ) THEN
        CREATE ROLE mutuelle_rw
        WITH LOGIN
        PASSWORD 'MotDePasseFort123!';
    END IF;
END
$$;
