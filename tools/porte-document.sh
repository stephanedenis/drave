#!/bin/bash
# porte-document.sh — R0.1 : le document est un graphe, et le graphe se vérifie.
#
# POURQUOI CETTE PORTE EXISTE. Une découpe de document qui « a l'air bonne » n'est pas une
# découpe : sans partition exacte, un offset faux ne se voit pas ; sans extraction
# indépendante, un extracteur qui invente des mots ne se voit pas non plus. Cette porte
# exige donc les trois choses ensemble — partition, fidélité, rejeu — plus trois contrôles
# négatifs qui doivent ÉCHOUER (texte plat, deux colonnes, notes hors corps).
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE R0.1 — LE GRAPHE DE DOCUMENT ==="
python3 tools/graphe_document.py --porte
CODE=$?
[ "$CODE" = 0 ] && echo "✅ porte document verte" || echo "❌ porte document ROUGE (code $CODE)"
exit "$CODE"
