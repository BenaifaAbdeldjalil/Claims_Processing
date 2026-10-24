"""
Setup PostgreSQL for the mutuelle data project.

This script:
1. Creates the application role.
2. Creates the application database.
3. Creates bronze, silver and gold schemas.
4. Grants read/write privileges to the role.
"""

from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# ----------------------------------------
# Configuration
# ----------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(BASE_DIR / "config" / ".env")

import os

PG_ADMIN_HOST = os.getenv("PG_ADMIN_HOST")
PG_ADMIN_PORT = os.getenv("PG_ADMIN_PORT")
PG_ADMIN_USER = os.getenv("PG_ADMIN_USER")
PG_ADMIN_PASSWORD = os.getenv("PG_ADMIN_PASSWORD")

PG_DB = os.getenv("PG_DB")
PG_ROLE = os.getenv("PG_USER")
PG_ROLE_PASSWORD = os.getenv("PG_PASSWORD")

SQL_DIR = BASE_DIR / "sql"


# ----------------------------------------
# Helper functions
# ----------------------------------------

def get_admin_connection_super(database: str = "postgres"):
    """
    Connect to PostgreSQL using the administrator account.
    The connection is created in autocommit mode because commands
    such as CREATE DATABASE cannot run inside a transaction.
    """
    connection = psycopg2.connect(
        host=PG_ADMIN_HOST,
        port=PG_ADMIN_PORT,
        user=PG_ADMIN_USER,
        password=PG_ADMIN_PASSWORD,
        dbname=database,
    )

    connection.autocommit = True

    return connection

def get_admin_connection(database: str =PG_DB ):
    """
    Connect to PostgreSQL using the administrator account.
    The connection is created in autocommit mode because commands
    such as CREATE DATABASE cannot run inside a transaction.
    """
    connection = psycopg2.connect(
        host=PG_ADMIN_HOST,
        port=PG_ADMIN_PORT,
        user=PG_ADMIN_USER,
        password=PG_ADMIN_PASSWORD,
        dbname=database,
    )

    connection.autocommit = True

    return connection



def execute_sql_file(connection, file_path: Path):
    old_autocommit = connection.autocommit
    connection.autocommit = True
    """
    Execute a SQL file using a psycopg2 connection.
    """
    print(f"\n>>> Executing SQL file: {file_path}")
    try:

        with file_path.open("r", encoding="utf-8") as file:
            sql_script = file.read()

        with connection.cursor() as cursor:
            cursor.execute(sql_script)
    except psycopg2.errors.DuplicateDatabase:
        print(f"[SKIP] Database already exists.")

    print(f"[OK] SQL file executed: {file_path.name}")

# ----------------------------------------
# Main execution
# ----------------------------------------
def close_connexion():
    """
    Connect to the application database and grant privileges.
    """
    connection = get_admin_connection(database=PG_DB)
    connection.close()

    print(f"[OK] Read/write privileges granted to {PG_ROLE}")
    
def main():
    print("========================================")
    print(" PostgreSQL setup - mutuelle data project")
    print("========================================")

    # 1. Connect to the default PostgreSQL database
    admin_connection_super = get_admin_connection_super(database="postgres")
    file_create_role = SQL_DIR /"01_1_create_role.sql"
    file_create_database = SQL_DIR /"01_2_create_database.sql"
    admin_connection = get_admin_connection(database="claims_processing")
    file_create_schema = SQL_DIR /"01_4_create_schema.sql"
    file_grante_role = SQL_DIR /"01_3_grante_role.sql"

    try:
        # 2. Create the application role
        execute_sql_file(admin_connection_super, file_create_role)

        # 3. Create the application database
        execute_sql_file(admin_connection_super, file_create_database)

        # 4. Create schemas inside the application database
        execute_sql_file(admin_connection, file_create_schema)

        # 5. Grant privileges on schemas, tables and sequences
        execute_sql_file(admin_connection, file_grante_role)

    finally:
        admin_connection.close()


    print("\n========================================")
    print(" PostgreSQL setup completed successfully")
    print("========================================")
    print(f"Database : {PG_DB}")
    print(f"Role     : {PG_ROLE}, {PG_ROLE_PASSWORD} ")
    
    print("Schemas  : mutuelle_bronze, mutuelle_silver, mutuelle_gold")


if __name__ == "__main__":
    main()