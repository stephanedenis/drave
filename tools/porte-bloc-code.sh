#!/bin/bash
# porte-bloc-code.sh — R4.2 : un code lu est un AST exécuté, et l'AST se vérifie.
#
# POURQUOI CETTE PORTE EXISTE. Un document de code n'est pas de la prose : la réponse à
# « que vaut cette expression ? » est dans l'EXÉCUTION, pas dans la ligne. R0.1 range le
# code en région et le texte reste du texte ; le banc R0.3 demande des valeurs par deux
# mots rares, ce qui mesure la recherche d'une ligne, pas la compréhension. Cette porte
# exige donc les trois choses ensemble : le PARSEUR (tout le corpus accepté), la PORTÉE
# (chaque nom rattaché à sa portée), l'EXÉCUTION EN SABLE (liste blanche, bornes) — plus
# le contrôle négatif « texte seul » qui doit ÉCHOUER.
#
# Ce qu'elle ne vérifie PAS : la sémantique d'un langage hors Python ; les bibliothèques
# (aucun import n'est exécuté) ; l'intention du code (c'est le modèle, et R0.3 le mesure).
#
# Usage : tools/porte-bloc-code.sh
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE R4.2 — LE BLOC CODE ==="
python3 tools/bloc_code.py --porte
CODE=$?
[ "$CODE" = 0 ] && echo "✅ porte bloc code verte" || echo "❌ porte bloc code ROUGE (code $CODE)"
exit "$CODE"
