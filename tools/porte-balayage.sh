#!/bin/bash
# porte-balayage.sh — R05 : l'index de spans tient ses offsets.
#
# POURQUOI CETTE PORTE EXISTE. Un index de spans qui « trouve à peu près » ne vaut rien : un
# offset faux fait citer le mauvais octet, et un rejeu qui change d'ordre fait perdre la trace.
# Cette porte exige les offsets exacts, le rejeu, la recherche exacte, le balayage, et deux
# contrôles négatifs (terme absent, terme d'un autre document).
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE R05 — L'INDEX DE SPANS ==="
python3 tools/index_spans.py --autotest
CODE=$?
[ "$CODE" = 0 ] && echo "✅ porte balayage verte" || echo "❌ porte balayage ROUGE (code $CODE)"
exit "$CODE"
