#!/bin/bash
# porte-bloc-tableaux.sh — R4.1 : un tableau lu est une GRILLE, et la grille se vérifie.
#
# POURQUOI CETTE PORTE EXISTE. R0.1 aplatit chaque rangée en texte tabulé : c'est assez
# pour retrouver une ligne, pas pour lire une colonne. Le banc R0.3 le montre — son type
# « tableau » rend 27/59 questions dont le gold est une rangée aplatie, et 20 de ces 27
# attendent comme réponse le numéro de l'étiquette (`B11` → « 11 »). Cette porte exige donc
# les trois choses ensemble : la PROVENANCE (chaque cellule est exactement la tranche de
# source qu'elle déclare), les OPÉRATIONS (filtre, jointure, agrégat justes), et les
# CONTRÔLES NÉGATIFS qui doivent ÉCHOUER (texte plat, en-tête fusionnée, tableau irrégulier).
#
# Ce qu'elle ne vérifie PAS : les tableaux PDF non balisés (R0.1 les laisse en texte, R4.1
# ne les invente pas) ; les tableaux multi-niveaux fusionnés (refusés, pas devinés).
#
# Usage : tools/porte-bloc-tableaux.sh
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE R4.1 — LE BLOC TABLEAUX ==="
python3 tools/bloc_tableaux.py --porte
CODE=$?
[ "$CODE" = 0 ] && echo "✅ porte bloc tableaux verte" || echo "❌ porte bloc tableaux ROUGE (code $CODE)"
exit "$CODE"
