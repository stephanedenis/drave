#!/bin/bash
# porte-sessions.sh — les plans de session sont lisibles et le linter refuse un doublon.
set -u
cd "$(dirname "$0")/.."
python3 tools/sessions.py --autotest || exit 1
python3 tools/sessions.py --check || exit 1
python3 tools/sessions.py --status | grep -q '71d57f53' || {
    echo "  ❌ le plan de la session de coordination n'est pas lisible"; exit 1; }
echo "PORTE TENUE : plan lisible · autotest doublon/champ manquant · check en-cours"
