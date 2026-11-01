#!/usr/bin/env bash
# Porte du bloc linguistique — tests de contrat + mesure UDHR (langue/script).
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "=== PORTE BLOC LINGUISTIQUE ==="
python3 -m unittest discover -s tools/tests/linguistique -p 'test_bloc_linguistique.py' || { echo "❌ tests"; exit 1; }
python3 tools/bloc_linguistique.py --autotest --udhr data/udhr/articles.jsonl --sortie /tmp/bloc-linguistique-porte.json || { echo "❌ autotest"; exit 1; }
python3 tools/tests/linguistique/gold.py >/dev/null || { echo "❌ gold"; exit 1; }
python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/pensee-gold-porte.json >/dev/null || { echo "❌ évaluation gold"; exit 1; }
echo "✅ porte bloc linguistique verte"
