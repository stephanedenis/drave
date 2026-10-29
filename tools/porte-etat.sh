#!/bin/bash
# porte-etat.sh — l'état est COURT, STRUCTURÉ, et À JOUR (le fait et sa ligne).
#
# POURQUOI CETTE PORTE EXISTE. `verifie_en_cours.py` vérifie la forme ; il ne peut pas
# savoir qu'un fait a été commité sans sa ligne. Le 29/10, A8.0 (15 h 51) est passé
# après le dernier état (15 h 34) : la revue comparait des DATES, donc deux commits du
# même jour passaient. Cette porte compare des COMMITS, et vérifie son propre contrôle
# négatif dans un dépôt temporaire (fait seul → refus ; état ensuite → passe).
#
# Ce qu'elle verrouille :
#   1. la forme et le budget de l'état (délégué à verifie_en_cours.py) ;
#   2. aucun fait commité après le dernier commit d'`en-cours` ;
#   3. le contrôle négatif des deux modes (--head, --index) reste valide.
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE ÉTAT — LE FAIT ET SA LIGNE ==="
python3 tools/verifie_en_cours.py || { echo "❌ porte état ROUGE : forme"; exit 1; }
python3 tools/verifie_etat_a_jour.py --head || { echo "❌ porte état ROUGE : fraîcheur"; exit 1; }
python3 tools/verifie_etat_a_jour.py --autotest || { echo "❌ porte état ROUGE : contrôle négatif"; exit 1; }
echo "✅ porte état verte : aucun fait commité après le dernier état"
