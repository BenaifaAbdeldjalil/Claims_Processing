CREATE TABLE IF NOT EXISTS bronze.adherents (
    bronze_id BIGSERIAL PRIMARY KEY,
    source_system VARCHAR(100),
    source_endpoint VARCHAR(255),
    ingestion_date TIMESTAMP NOT NULL DEFAULT NOW(),
    raw_data JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS bronze.contrats (
    bronze_id BIGSERIAL PRIMARY KEY,
    source_system VARCHAR(100),
    source_endpoint VARCHAR(255),
    ingestion_date TIMESTAMP NOT NULL DEFAULT NOW(),
    raw_data JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS bronze.sinistres (
    bronze_id BIGSERIAL PRIMARY KEY,
    source_system VARCHAR(100),
    source_endpoint VARCHAR(255),
    ingestion_date TIMESTAMP NOT NULL DEFAULT NOW(),
    raw_data JSONB NOT NULL
);