#!/bin/bash
# porte-ocr.sh — R4.4 : l'OCR lit, il dit son score, et ses contrôles négatifs échouent.
#
# POURQUOI CETTE PORTE EXISTE. La ligne R4.4 était bloquée par « aucun OCR installé » : on
# ne pouvait pas mesurer. Maintenant qu'on peut, la porte doit dire ce qui est TENU, et pas
# seulement « ça tourne » : dix pages rendues depuis le corpus gelé, un WER contre le texte
# natif, la PARITÉ des réponses sur les questions du banc R0.3, et deux contrôles négatifs
# qui doivent ÉCHOUER — sans OCR aucune réponse, page dégradée le WER monte et la parité
# baisse. Une porte qui passerait avec l'OCR débranché ne mesurerait rien.
#
# CE QU'ELLE NE VÉRIFIE PAS. Pas de scans réels, pas de mise en page à deux colonnes, pas de
# tableaux : ce sont les étapes 2 et 3 de R4.4, et elles restent ouvertes. La porte le dit.
#
# Usage : tools/porte-ocr.sh
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE R4.4 — L'OCR, SA PARITÉ ET SES CONTRÔLES ==="
if ! bash tools/installer_ocr.sh --verifie; then
    echo "  ❌ OCR absent de la machine : tools/installer_ocr.sh (environnementale)"
    exit 2
fi
python3 tools/mesurer_ocr.py --porte --sans-ecrire
CODE=$?
if [ "$CODE" = 0 ]; then
    echo "✅ porte OCR verte : 10 pages lues, WER sous le seuil, parité tenue et contrôles en échec"
else
    echo "❌ porte OCR ROUGE (code $CODE)"
fi
exit "$CODE"
