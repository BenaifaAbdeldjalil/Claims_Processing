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

PG_HOST = os.getenv("PG_ADMIN_HOST")
PG_PORT = os.getenv("PG_ADMIN_PORT")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

SQL_BRONZE_DIR = BASE_DIR / "sql/bronze"

# ----------------------------------------
# Helper functions
# ----------------------------------------

def get_connection(database: str =PG_DB ):
    """
    Connect to PostgreSQL using the administrator account.
    The connection is created in autocommit mode because commands
    such as CREATE DATABASE cannot run inside a transaction.
    """
    connection = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        user=PG_USER,
        password=PG_PASSWORD,
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
 
def main():
    print("========================================")
    print(" PostgreSQL setup - mutuelle data project")
    print("========================================")

    # 1. Connect to the default PostgreSQL database
    connection = get_connection(database="claims_processing")
    build_bronze = SQL_BRONZE_DIR /"02_create_bronze_tables.sql"

    try:
        # 2. Create the bronze schema
        execute_sql_file(connection, build_bronze)


    finally:
        connection.close()


    print("\n========================================")
    print(" Setup completed successfully")
    print("========================================")
    print(f"Database : {PG_DB}")
    print(f"Role     : {PG_USER} ")
    


if __name__ == "__main__":
    main()