#!/bin/bash
# porte-lecture.sh — R0.6 : le pipeline de lecture tient son contrat, et sa calibration tient.
#
# POURQUOI CETTE PORTE EXISTE. Un pipeline qui répond « avec l'air de savoir » n'est pas un
# pipeline : sans budget tenu, sans provenance vérifiable, sans refus, il rend des passages au
# hasard avec une citation décorative. Et une calibration qui ne se reproduit pas n'est pas une
# politique : le seuil publié doit se recalculer à l'identique sur le banc qu'il nomme.
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE R0.6 — LE PIPELINE DE LECTURE ==="
python3 tools/lecture.py --autotest
CODE=$?
if [ "$CODE" = 0 ]; then
  echo "--- la calibration publiée se reproduit ---"
  python3 tools/calibrer.py --verifie tools/tests/documents/calibration-lexical.json || CODE=1
  python3 tools/calibrer.py --verifie tools/tests/documents/calibration-paraphrase.json || CODE=1
fi
[ "$CODE" = 0 ] && echo "✅ porte lecture verte" || echo "❌ porte lecture ROUGE (code $CODE)"
exit "$CODE"
