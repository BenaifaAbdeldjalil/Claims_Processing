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

PG_ADMIN_HOST = os.getenv("PG_ADMIN_HOST", "localhost")
PG_ADMIN_PORT = os.getenv("PG_ADMIN_PORT", "5432")
PG_ADMIN_USER = os.getenv("PG_ADMIN_USER", "postgres")
PG_ADMIN_PASSWORD = os.getenv("PG_ADMIN_PASSWORD", "")

PG_DB = os.getenv("PG_DB", "mutuelle_db")
PG_ROLE = os.getenv("PG_ROLE", "mutuelle_rw")
PG_ROLE_PASSWORD = os.getenv("PG_ROLE_PASSWORD", "MotDePasseFort123!")

SQL_DIR = BASE_DIR / "sql"


# ----------------------------------------
# Helper functions
# ----------------------------------------

def get_admin_connection(database: str = "postgres"):
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
    """
    Execute a SQL file using a psycopg2 connection.
    """
    print(f"\n>>> Executing SQL file: {file_path}")

    with file_path.open("r", encoding="utf-8") as file:
        sql_script = file.read()

    with connection.cursor() as cursor:
        cursor.execute(sql_script)

    print(f"[OK] SQL file executed: {file_path.name}")


def create_role(connection):
    """
    Create the PostgreSQL role if it does not already exist.
    """
    print(f"\n>>> Checking role: {PG_ROLE}")

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM pg_roles WHERE rolname = %s",
            (PG_ROLE,),
        )
        role_exists = cursor.fetchone() is not None

    if role_exists:
        print(f"[SKIP] Role already exists: {PG_ROLE}")
        return

    with connection.cursor() as cursor:
        cursor.execute(
            sql.SQL(
                "CREATE ROLE {} WITH LOGIN PASSWORD %s"
            ).format(sql.Identifier(PG_ROLE)),
            (PG_ROLE_PASSWORD,),
        )

    print(f"[OK] Role created: {PG_ROLE}")


def create_database(connection):
    """
    Create the application database if it does not already exist.
    """
    print(f"\n>>> Checking database: {PG_DB}")

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (PG_DB,),
        )
        database_exists = cursor.fetchone() is not None

    if database_exists:
        print(f"[SKIP] Database already exists: {PG_DB}")
        return

    with connection.cursor() as cursor:
        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(PG_DB)
            )
        )

    print(f"[OK] Database created: {PG_DB}")


def grant_database_privileges(connection):
    """
    Grant connection privilege on the application database.
    """
    print(f"\n>>> Granting database privileges on: {PG_DB}")

    with connection.cursor() as cursor:
        cursor.execute(
            sql.SQL(
                "GRANT CONNECT ON DATABASE {} TO {}"
            ).format(
                sql.Identifier(PG_DB),
                sql.Identifier(PG_ROLE),
            )
        )

    print(f"[OK] CONNECT granted on {PG_DB} to {PG_ROLE}")


def create_schemas():
    """
    Connect to the application database and create the schemas.
    """
    print(f"\n>>> Creating schemas in database: {PG_DB}")

    connection = get_admin_connection(database=PG_DB)

    try:
        execute_sql_file(
            connection,
            SQL_DIR / "02_create_schemas.sql",
        )
    finally:
        connection.close()

    print("[OK] Schemas created: bronze, silver, gold")


def grant_schema_privileges():
    """
    Connect to the application database and grant privileges.
    """
    print(f"\n>>> Granting schema privileges in database: {PG_DB}")

    connection = get_admin_connection(database=PG_DB)

    try:
        execute_sql_file(
            connection,
            SQL_DIR / "03_grant_privileges.sql",
        )
    finally:
        connection.close()

    print(f"[OK] Read/write privileges granted to {PG_ROLE}")


# ----------------------------------------
# Main execution
# ----------------------------------------

def main():
    print("========================================")
    print(" PostgreSQL setup - mutuelle data project")
    print("========================================")

    # 1. Connect to the default PostgreSQL database
    admin_connection = get_admin_connection(database="postgres")

    try:
        # 2. Create the application role
        create_role(admin_connection)

        # 3. Create the application database
        create_database(admin_connection)

        # 4. Grant CONNECT on the application database
        grant_database_privileges(admin_connection)
    finally:
        admin_connection.close()

    # 5. Create schemas inside the application database
    create_schemas()

    # 6. Grant privileges on schemas, tables and sequences
    grant_schema_privileges()

    print("\n========================================")
    print(" PostgreSQL setup completed successfully")
    print("========================================")
    print(f"Database : {PG_DB}")
    print(f"Role     : {PG_ROLE}")
    print("Schemas  : bronze, silver, gold")


if __name__ == "__main__":
    main()