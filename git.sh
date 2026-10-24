#!/usr/bin/env bash

echo
echo "git starting ......"
echo

# Vérifier qu'un paramètre est passé
if [ -z "$1" ]; then
    echo "Usage: ./git.sh <parametre>"
    exit 1
fi

PARAM="$1"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "Fetching latest changes from remote..."
echo

# Récupérer les modifications distantes
# - --rebase : évite un commit de merge inutile
# - -X theirs : en cas de conflit, garde la version LOCALE
#   (pendant un rebase, "theirs" correspond à vos commits locaux)
# - --autostash : met temporairement de côté les fichiers non commités
git pull --rebase --autostash -X theirs origin main

if [ $? -ne 0 ]; then
    echo
    echo "❌ Git pull/rebase failed. Please resolve the issue manually."
    exit 1
fi

echo
echo "Adding files..."
echo

# Ajouter tous les fichiers modifiés
git add .

# Vérifier s'il y a quelque chose à committer
if git diff --cached --quiet; then
    echo
    echo "⚠️  No changes to commit."
    exit 0
fi

echo
echo "Committing changes: $PARAM ..."
echo

# Commit avec message personnalisé
git commit -m "add modifications $PARAM $TIMESTAMP"

if [ $? -ne 0 ]; then
    echo
    echo "❌ Git commit failed."
    exit 1
fi

echo
echo "Commit OK!"
echo

echo "Pushing changes... $TIMESTAMP"
echo

# Push vers le dépôt distant
git push origin main

if [ $? -ne 0 ]; then
    echo
    echo "❌ Git push failed."
    exit 1
fi

echo
echo "✅ git ok!"