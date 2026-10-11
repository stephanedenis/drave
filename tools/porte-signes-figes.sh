#!/bin/bash
# porte-signes-figes.sh — la recette « signes figés » rend-elle vraiment l'élagage indolore ?
#
# CE QUE LA PORTE VERROUILLE. E6 a été tranché le 11/10 par un plan 2x2 : sous élagage agressif,
# c'est la **contrainte de signe** (`w = signe · |θ|`, signe choisi à la naissance) qui porte la
# robustesse, pas la loi des magnitudes — et la loi log-normale **nuit**. À 25 % de poids gardés et
# 3 000 pas, le témoin dense vaut **49,43** et le modèle à signes figés **7,95** (×6,2, sur trois
# graines). C'est le seul levier du dépôt qui rende l'élagage supportable, donc il mérite un verrou.
#
# POURQUOI UN PROTOCOLE COURT. La porte refait l'expérience à **600 pas** (≈3 min au lieu de 8) et
# exige un **rapport**, pas une valeur : à ce stade les deux modèles sont loin d'avoir convergé, et
# c'est le RAPPORT qui porte le résultat (mesuré : 17,74 contre 12,01, soit ×1,48). Le chiffre
# publié, lui, est celui des 3 000 pas — il est dans `reports/rapport-e6-poids-lognormaux.md`.
#
# CE QU'ELLE NE VERROUILLE PAS : la raison intime du phénomène (pourquoi figer les signes aide
# reste une question ouverte), ni le coût — le compteur de paires ne voit pas l'occupation (M9).
set -u
cd "$(dirname "$0")/.."
P=${P:-/home/stephane/gpu-env/bin/python}
D=${D:-./drave-core/target/release/drave}
T=${TRAVAIL:-/tmp/porte-signes-figes}
PAS=${PAS:-600}
GARDE=${GARDE:-0.25}
RAPPORT=${RAPPORT:-1.2}
VALIDATION=${VALIDATION:-/tmp/e6/val.ids}
DELAI=${DELAI:-1800}
# Permet de vérifier que la porte SAIT rougir : `EXTRA_SIGFIGES=--signes-libres` remplace la
# recette par une autre, et la porte doit alors échouer.
EXTRA_SIGFIGES=${EXTRA_SIGFIGES:---signes-figes}

for f in data/corpus_en.txt data/corpus_en_val.txt; do
    [ -s "$f" ] || { echo "  ❌ $f manquant : cette porte entraîne deux petits modèles"; exit 2; }
done
$P -c "import torch, transformers" 2>/dev/null || { echo "  ❌ $P n'a pas torch/transformers"; exit 2; }
[ -s "$VALIDATION" ] || { echo "  ❌ $VALIDATION manquant (le corpus d'évaluation) : cette porte"
                          echo "     compare deux modèles SUR LE MÊME TEXTE"; exit 2; }
rm -rf "$T"; mkdir -p "$T"

C="--famille route --dim 192 --couches 4 --tetes 4 --cache 768 --experts 8 --k 2 --seq 128 \
   --lot 32 --lr 3e-4 --graine 1 --pas $PAS --eval-tous $PAS --elagage-tous 200 --elagage $GARDE"

mesurer () { # $1 = nom, $2.. = drapeaux de la variante
    local nom=$1; shift
    timeout "$DELAI" $P -u tools/entrainer_moteur.py $C "$@" --sortie "$T/$nom" \
        > "$T/$nom.log" 2>&1 || { echo "  ❌ entraînement $nom en échec"; tail -5 "$T/$nom.log"; exit 1; }
    timeout "$DELAI" $P tools/exporter_gguf.py --hf "$T/$nom" --sortie "$T/$nom.gguf" \
        > "$T/export-$nom.log" 2>&1 || { echo "  ❌ export $nom en échec"; tail -5 "$T/export-$nom.log"; exit 1; }
    local occ
    occ=$($P tools/occupation_poids.py --modele "$T/$nom.gguf" \
          | grep -E "^\| \*\*total" | grep -oE "[0-9]+\.[0-9]+" | head -1)
    local ppl
    ppl=$(timeout "$DELAI" "$D" "$T/$nom.gguf" --ppl "$VALIDATION" --limit 512 --ctx 512 \
          --threads 4 2>&1 | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+")
    echo "$occ $ppl"
}

echo "=== 1. témoin dense et recette « signes figés » ($PAS pas, élagage à $GARDE gardé) ==="
read -r OCC_D PPL_D <<< "$(mesurer dense)"
read -r OCC_S PPL_S <<< "$(mesurer sigfiges "$EXTRA_SIGFIGES")"
echo "  dense      : occupation $OCC_D · perplexité $PPL_D"
echo "  signes figés ($EXTRA_SIGFIGES) : occupation $OCC_S · perplexité $PPL_S"

echo
echo "=== 2. le verrou ==="
$P - "$PPL_D" "$PPL_S" "$RAPPORT" "$OCC_D" "$OCC_S" "$EXTRA_SIGFIGES" <<'PY'
import sys
dense, sig, seuil, occ_d, occ_s, recette = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), \
    sys.argv[4], sys.argv[5], sys.argv[6]
# L'occupation doit être comparable : sinon on ne compare pas la même chose (leçon du 11/10, où
# « 25 % gardés » valait 78 % à cause du meilleur point).
fd, fs = float(occ_d.rstrip(' %')), float(occ_s.rstrip(' %'))
print(f"  occupation : dense {fd:.1f} % · signes figés {fs:.1f} %")
if abs(fd - fs) > 8:
    print(f"  ❌ les deux modèles n'ont PAS la même occupation ({fd:.1f} % contre {fs:.1f} %) :")
    print("     la comparaison ne porterait pas sur le même élagage")
    sys.exit(1)
rapport = dense / sig
print(f"  perplexité : dense {dense:,.4f} · signes figés {sig:,.4f} · rapport ×{rapport:.2f} "
      f"(seuil ×{seuil:.2f})")
if rapport < seuil:
    print(f"  ❌ la recette {recette} n'apporte plus l'avantage attendu (×{rapport:.2f} < ×{seuil:.2f})")
    sys.exit(1)
print(f"  ✅ la recette {recette} rend l'élagage à {fd:.0f} % gardé ×{rapport:.2f} moins cher "
      f"que le témoin")
PY
CODE=$?
[ "$CODE" = 0 ] || exit "$CODE"

echo
echo "✅ porte signes figés : la contrainte de signe rend l'élagage indolore (et la porte a été"
echo "   vue ROUGE avec une autre recette : EXTRA_SIGFIGES=--signes-libres)."
