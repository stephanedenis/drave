#!/bin/bash
# porte-ocr-scans.sh — R4.4 : les scans (5 familles), les colonnes, les tableaux.
#
# POURQUOI CETTE PORTE EXISTE. La première porte OCR vérifiait dix pages **rendues** ; elle ne
# voyait ni une photocopie, ni une photo, ni un fax, ni une page à deux colonnes, ni un tableau.
# Cette porte mesure ce que R4.4 promet : cinq familles de dégradation, un split dev/test, la
# parité du lecteur, la gouttière des colonnes et les cellules des tableaux — chacune avec ses
# contrôles négatifs (page noire, page mono, contrôle sans redressement, texte à plat).
#
# CE QU'ELLE NE VÉRIFIE PAS : les scans RÉELS (la validation externe est dans la fiche, sur un
# PDF d'Internet Archive) ; les seuils sont des PLANCHERS mesurés, pas des prédictions.
#
# Usage : tools/porte-ocr-scans.sh
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE R4.4 — SCANS, COLONNES, TABLEAUX ==="
if ! bash tools/installer_ocr.sh --verifie; then
    echo "  ❌ OCR absent de la machine : tools/installer_ocr.sh (environnementale)"
    exit 2
fi
J=$(mktemp -d)
if [ ! -s work/r44/scans/manifeste.json ]; then
    echo "  corpus de scans absent : fabrication (10 pages dev + 10 test × 5 familles)"
    python3 tools/simuler_scan.py --pages 10 --test 10 > "$J/corpus.log" 2>&1 || {
        tail -3 "$J/corpus.log"; exit 1; }
fi
if [ ! -s work/r44/colonnes/manifeste.json ]; then
    python3 tools/fabriquer_colonnes.py --pages 10 > /dev/null 2>&1 || exit 1
fi
if [ ! -s work/r44/tables/manifeste.json ]; then
    python3 tools/fabriquer_tables.py --pages 10 > /dev/null 2>&1 || exit 1
fi
echo "--- 1. les familles de scans (100 scans, dev + test)"
python3 tools/mesurer_scans.py --pipelines auto --exposants --colonnes --porte > "$J/scans.log" 2>&1
C1=$?
tail -n 24 "$J/scans.log"
echo "--- 2. les colonnes (10 pages × 2 versions × 3 familles)"
python3 tools/mesurer_colonnes.py --porte > "$J/colonnes.log" 2>&1
C2=$?
tail -n 12 "$J/colonnes.log"
echo "--- 3. les tableaux (10 pages × 3 familles)"
python3 tools/mesurer_tables.py --porte > "$J/tables.log" 2>&1
C3=$?
tail -n 12 "$J/tables.log"
CODE=0
[ "$C1" = 0 ] || CODE=1
[ "$C2" = 0 ] || CODE=1
[ "$C3" = 0 ] || CODE=1
if [ "$CODE" = 0 ]; then
    echo "✅ porte OCR-scans verte : familles, colonnes et tableaux tiennent leurs planchers"
else
    echo "❌ porte OCR-scans ROUGE (scans $C1, colonnes $C2, tableaux $C3)"
fi
exit "$CODE"
