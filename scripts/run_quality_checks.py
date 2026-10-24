import pandas as pd

from config.scripts.config import engine

CHECKS = []


def quality_check(name):
    def decorator(func):
        CHECKS.append((name, func))
        return func
    return decorator


@quality_check("No duplicate members")
def check_duplicate_members():
    return pd.read_sql(
        """
        SELECT id
        FROM mutuelle_silver.adherents
        GROUP BY id
        HAVING COUNT(*) > 1
        """,
        engine,
    )


@quality_check("No duplicate contracts")
def check_duplicate_contracts():
    return pd.read_sql(
        """
        SELECT id_contrat
        FROM mutuelle_silver.contrats
        GROUP BY id_contrat
        HAVING COUNT(*) > 1
        """,
        engine,
    )


@quality_check("No duplicate claims")
def check_duplicate_claims():
    return pd.read_sql(
        """
        SELECT id_sinistre
        FROM mutuelle_silver.sinistres
        GROUP BY id_sinistre
        HAVING COUNT(*) > 1
        """,
        engine,
    )


@quality_check("No negative amounts")
def check_negative_amounts():
    return pd.read_sql(
        """
        SELECT id_sinistre
        FROM mutuelle_silver.sinistres
        WHERE claimed_amount < 0
           OR amount < 0
        """,
        engine,
    )


@quality_check("Reimbursement must not exceed claimed amount")
def check_reimbursement_consistency():
    return pd.read_sql(
        """
        SELECT id_sinistre
        FROM mutuelle_silver.sinistres
        WHERE amount > claimed_amount
        """,
        engine,
    )


@quality_check("Incident date must not be after declaration date")
def check_claim_dates():
    return pd.read_sql(
        """
        SELECT id_sinistre
        FROM mutuelle_silver.sinistres
        WHERE created_at >  submitted_at
        """,
        engine,
    )


@quality_check("Every claim must have a contract")
def check_claim_contract():
    return pd.read_sql(
        """
        SELECT s.id_sinistre
        FROM mutuelle_silver.sinistres s
        LEFT JOIN mutuelle_silver.contrats c
            ON s.id_contrat = c.id_contrat
        WHERE c.id_contrat IS NULL
        """,
        engine,
    )


@quality_check("Every contract must have a member")
def check_contract_member():
    return pd.read_sql(
        """
        SELECT c.id_contrat
        FROM mutuelle_silver.contrats c
        LEFT JOIN mutuelle_silver.adherents m
            ON c.id= m.id
        WHERE m.id IS NULL
        """,
        engine,
    )


@quality_check("Claim statuses must be normalized")
def check_claim_status():
    return pd.read_sql(
        """
        SELECT DISTINCT status
        FROM mutuelle_silver.sinistres
        WHERE status NOT IN (
            'SUBMITTED', 'IN_REVIEW', 'APPROVED', 'DENIED', 'REIMBURSED'
        )
        """,
        engine,
    )


def run_quality_checks():
    print("\n========== DATA QUALITY CHECKS ==========")
    failures = 0

    for name, check in CHECKS:
        result = check()

        if result.empty:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}")
            print(result.to_string(index=False))

    print("==========================================")
    print(f"Failed checks: {failures}")

    return failures


if __name__ == "__main__":
    failures = run_quality_checks()
    raise SystemExit(1 if failures > 0 else 0)