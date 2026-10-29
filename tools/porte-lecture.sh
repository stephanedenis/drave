#!/bin/bash
# porte-lecture.sh — R0.6 : le pipeline de lecture tient son contrat.
#
# POURQUOI CETTE PORTE EXISTE. Un pipeline qui répond « avec l'air de savoir » n'est pas un
# pipeline : sans budget tenu, sans provenance vérifiable, sans refus, il rend des passages au
# hasard avec une citation décorative. Cette porte exige les six choses ensemble — réponse
# trouvée, budget, provenance, rejeu, refus, closed-book — et le rejeu est comparé octet à
# octet (hors durée).
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE R0.6 — LE PIPELINE DE LECTURE ==="
python3 tools/lecture.py --autotest
CODE=$?
[ "$CODE" = 0 ] && echo "✅ porte lecture verte" || echo "❌ porte lecture ROUGE (code $CODE)"
exit "$CODE"
