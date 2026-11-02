#!/bin/bash
# porte-sessions.sh — les plans de session sont lisibles et le linter refuse un doublon.
set -u
cd "$(dirname "$0")/.."
python3 tools/sessions.py --autotest || exit 1
python3 tools/sessions.py --check --strict || exit 1
echo "PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict"
