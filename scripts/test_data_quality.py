import pandas as pd

from config import engine


def test_no_duplicate_members():
    df = pd.read_sql(
        "SELECT id_adherent FROM mutuelle_silver.adherents",
        engine,
    )
    assert df["id_adherent"].is_unique


def test_no_duplicate_contracts():
    df = pd.read_sql(
        "SELECT id_contrat FROM mutuelle_silver.contrats",
        engine,
    )
    assert df["id_contrat"].is_unique


def test_no_duplicate_claims():
    df = pd.read_sql(
        "SELECT id_sinistre FROM mutuelle_silver.sinistres",
        engine,
    )
    assert df["id_sinistre"].is_unique


def test_no_negative_amounts():
    df = pd.read_sql(
        """
        SELECT id_sinistre
        FROM mutuelle_silver.sinistres
        WHERE claimed_amount < 0
           OR amount < 0
        """,
        engine,
    )
    assert df.empty


def test_reimbursement_not_greater_than_claimed_amount():
    df = pd.read_sql(
        """
        SELECT id_sinistre
        FROM mutuelle_silver.sinistres
        WHERE amount > claimed_amount
        """,
        engine,
    )
    assert df.empty