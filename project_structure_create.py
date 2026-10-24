import os
from pathlib import Path

# Projet créé dans le dossier courant
base = Path(".")

# 1) Dossiers à créer
folders = [
    "config",

    "data/raw/adherents",
    "data/raw/contrats",
    "data/raw/sinistres",

    "data/bronze/adherents",
    "data/bronze/contrats",
    "data/bronze/sinistres",

    "data/silver",
    "data/gold",
    "data/logs",

    "sql/bronze",
    "sql/silver",
    "sql/gold",

    "scripts",
    "tests",
    "notebooks",
]

# 2) Fichiers vides à créer
files = [
    "requirements.txt",

    "config/.env",

    "data/raw/adherents/.gitkeep",
    "data/raw/contrats/.gitkeep",
    "data/raw/sinistres/.gitkeep",

    "data/bronze/adherents/.gitkeep",
    "data/bronze/contrats/.gitkeep",
    "data/bronze/sinistres/.gitkeep",

    "data/silver/.gitkeep",
    "data/gold/.gitkeep",
    "data/logs/.gitkeep",

    "sql/01_create_database.sql",
    "sql/02_create_schemas.sql",

    "sql/bronze/03_create_bronze_tables.sql",
    "sql/silver/04_create_silver_tables.sql",
    "sql/gold/05_create_gold_tables.sql",
    "sql/gold/06_create_gold_views.sql",

    "scripts/config.py",
    "scripts/extract_api.py",
    "scripts/extract_files.py",
    "scripts/load_bronze.py",
    "scripts/transform_silver.py",
    "scripts/build_gold.py",
    "scripts/historisation.py",
    "scripts/run_quality_checks.py",
    "scripts/run_pipeline.py",

    "tests/test_data_quality.py",

    "notebooks/claims_analysis.ipynb",
]

# Création du dossier principal
if not base.exists():
    base.mkdir(parents=True, exist_ok=True)
    print(f"✅ Projet créé : {base.resolve()}")
else:
    print(f"⏭️  Projet déjà existant : {base.resolve()}")

# Création des dossiers
for folder in folders:
    path = base / folder

    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Dossier créé : {path}")
    else:
        print(f"⏭️  Dossier déjà existant : {path}")

# Création des fichiers vides
for file_path in files:
    file = base / file_path

    if file.exists():
        print(f"⏭️  Fichier déjà existant : {file}")
        continue

    file.parent.mkdir(parents=True, exist_ok=True)
    file.touch()

    print(f"✅ Fichier vide créé : {file}")

print("\n🎉 Structure du projet créée avec succès.")
print(f"📂 Chemin du projet : {base.resolve()}")

print("\n📁 Contenu de la racine du projet :")
print(os.listdir(base))