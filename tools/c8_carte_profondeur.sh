#!/bin/bash
# c8_carte_profondeur.sh — la courbe PROFONDEUR → DÉCODABILITÉ du prochain jeton.
#
# POURQUOI ELLE EXISTE. La sonde du 10 octobre a montré qu'à la couche 16, l'état contient le
# prochain jeton (43,1 % de justes parmi les 256 plus fréquents, contre 4,0 % pour la classe
# majoritaire) alors que la tête empruntée y rend 728 388 de perplexité. Une seule profondeur ne
# dit pas OÙ placer un réflexe : s'il faut 20 couches pour que l'état soit lisible, le « chemin
# court » n'en est plus un.
#
# Ce pilote capture l'état à la sortie de chaque profondeur demandée (`--couches 0:L`, la tête
# étant appliquée pour que le moteur rende un résultat de modèle tronqué) et lance la même sonde
# linéaire sur chacune. Il imprime la courbe.
#
# Usage : tools/c8_carte_profondeur.sh [--limite N] [--classes K]
#         PROFONDEURS="3 7 11 15 19 23" tools/c8_carte_profondeur.sh
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
LIMITE=${LIMITE:-1024}
CLASSES=${CLASSES:-256}
# PROFONDEURS = le NOMBRE DE COUCHES EXÉCUTÉES (1..24). Attention : `--couches a:b` EXCLUT `b`
# — mesurer `--couches 0:15` veut dire « 15 couches », pas 16, et `0:23` n'est PAS le modèle
# complet (23 couches, 83,12 de perplexité à ctx 512 contre 14,65 pour le modèle entier). Le
# premier essai de ce pilote étiquetait « 4/24, 8/24, … » des plages qui en faisaient une de
# moins : les chiffres étaient justes, les ÉTIQUETTES fausses.
PROFONDEURS=${PROFONDEURS:-"4 8 12 16 20 24"}
T=${T:-/tmp/c8-profondeur}
CTX=${CTX:-$LIMITE}

[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }
[ -x "$D" ] || { echo "  binaire du moteur absent : $D"; exit 2; }
mkdir -p "$T"

POS=$(seq -s, 4 $((LIMITE - 1)))
echo "=== courbe profondeur → décodabilité ($LIMITE jetons, $CLASSES classes) ==="
printf '  %-8s %-10s %s\n' "couche" "perplexité" "sonde linéaire (test)"
for N in $PROFONDEURS; do
    L=$((N - 1))                       # `--couches 0:N` exécute N couches (b exclu)
    prefixe="$T/etat-$N"
    rm -f "$prefixe".*
    $D "$M" --ppl "$IDS" --limit "$LIMITE" --ctx "$CTX" --threads 8 \
       --couches "0:$N" --tete-partielle --etat-sortie "$prefixe" --etat-pos "$POS" \
       > "$T/capture-$N.log" 2>&1
    ppl=$(grep -oE "perplexité [0-9.]+ sur" "$T/capture-$N.log" | grep -oE "[0-9.]+" | head -1)
    sonde=$(python3 tools/c8_sonde_lineaire.py --etats "$prefixe" --ids "$IDS" \
              --limite "$LIMITE" --classes "$CLASSES" 2>&1 \
            | grep -oE "sonde linéaire.*: [0-9.]+ %" | grep -oE "[0-9.]+ %" | head -1)
    printf '  %-8s %-12s %s\n' "$N/24" "${ppl:-?}" "${sonde:-échec}"
done
echo
echo "Lecture : si la sonde est déjà nette tôt (couches 8-12), un réflexe court a de quoi lire ;"
echo "si elle ne l'est qu'à 20+, le « chemin court » n'existe pas et il faut le dire."
echo "Journaux de capture : $T/capture-*.log"
