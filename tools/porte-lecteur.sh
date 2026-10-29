#!/bin/bash
# porte-lecteur.sh — R0.2 : à 30 % du budget, le contrôleur retrouve la réponse.
#
# POURQUOI CETTE PORTE EXISTE. Un contrôleur de lecture peut sembler bon et ne rien
# sélectionner : sans comparaison à la lecture intégrale, sans contrôle aléatoire et sans
# contrôle « sans but », on mesure une impression. Cette porte exige les quatre à la fois :
# récupération ≥ 90 % à 30 % du budget, réponse préservée, hasard nettement plus bas, et
# closed-book silencieux.
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE R0.2 — LE CONTRÔLEUR DE LECTURE ==="
python3 tools/banc_lecture.py --porte
CODE=$?
[ "$CODE" = 0 ] && echo "✅ porte lecteur verte" || echo "❌ porte lecteur ROUGE (code $CODE)"
exit "$CODE"
