#!/bin/bash
# porte-bloc-maths.sh — R4.3 : une formule est un AST évalué, et l'AST se vérifie.
#
# POURQUOI CETTE PORTE EXISTE. `\frac{1}{3}+\frac{1}{6}` vaut `1/2`, et cette valeur n'est
# écrite nulle part : un lecteur de surface retrouve les chiffres, jamais le résultat. R0.1
# range les formules en région `maths` et le texte reste du texte. Cette porte exige donc
# les trois choses ensemble : le PARSEUR LaTeX (formules, équations, refus nommés),
# l'ARITHMÉTIQUE EXACTE (fractions) et la DÉRIVATION/RÉSOLUTION — recoupées par un ORACLE
# INDÉPENDANT (sympy) — plus le contrôle « surface » qui doit ÉCHOUER.
#
# Ce qu'elle ne vérifie PAS : LaTeX complet (pas d'intégrales, de matrices, de sommes) ;
# l'équivalence symbolique générale (les dérivées sont comparées sur 5 points) ; les
# formules du dépôt, qui n'en contient pas (le corpus est une fixture assumée).
#
# Usage : tools/porte-bloc-maths.sh
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE R4.3 — LE BLOC MATHS ==="
python3 tools/bloc_maths.py --porte
CODE=$?
[ "$CODE" = 0 ] && echo "✅ porte bloc maths verte" || echo "❌ porte bloc maths ROUGE (code $CODE)"
exit "$CODE"
