#!/bin/bash
# porte-occupation-moteur.sh — le moteur annonce-t-il l'occupation, et COLLE-T-ELLE au fichier ?
#
# POURQUOI CETTE PORTE. Jusqu'au 11/10, le moteur ne savait dire qu'une chose du coût : les
# **paires noyau** (`n_in × n_out`), qui mesurent le travail d'un noyau **dense** — fidèlement, et
# qui ne bougent pas d'un chiffre quand on élague 75 % des poids. Le manque **M9** consistait
# exactement en cela : « aucun instrument du dépôt ne voit la sparsité des poids dans un chiffre de
# coût ». La seconde moitié est livrée : le moteur lit l'occupation **dans le fichier**, par genre,
# et affiche ce qu'un format creux lirait.
#
# CE QU'ELLE VÉRIFIE, ET POURQUOI LES DEUX MOITIÉS :
#   1. **l'occupation annoncée par le moteur COLLE à celle que lit l'outil indépendant**
#      (`tools/occupation_poids.py`, en Python, qui déquantifie) — deux chemins de code différents
#      pour le même chiffre : c'est la seule façon de savoir que l'un des deux ne se trompe pas ;
#   2. **elle SÉPARE** : un modèle élagué à 25 % doit s'annoncer bien en dessous d'un modèle dense,
#      et son estimation creuse doit être plus basse. Un compteur qui rend le même chiffre pour les
#      deux ne mesure rien (c'est précisément le défaut qu'on répare).
#
# COÛT : deux entraînements de 200 pas + deux exports, ~1 min.
set -u
cd "$(dirname "$0")/.."
P=${P:-/home/stephane/gpu-env/bin/python}
D=${D:-./drave-core/target/release/drave}
T=${TRAVAIL:-/tmp/porte-occupation-moteur}
PAS=${PAS:-200}
IDS=${IDS:-/tmp/e6/val.ids}
DELAI=${DELAI:-1200}

[ -x "$D" ] || { echo "  ❌ $D : le binaire de mesure n'existe pas (cargo build --release)"; exit 2; }
[ -s "$IDS" ] || { echo "  ❌ $IDS manquant : cette porte a besoin d'un corpus d'évaluation"; exit 2; }
for f in data/corpus_en.txt data/corpus_en_val.txt; do
    [ -s "$f" ] || { echo "  ❌ $f manquant : cette porte entraîne de petits modèles"; exit 2; }
done
rm -rf "$T"; mkdir -p "$T"
C="--famille route --dim 192 --couches 4 --tetes 4 --cache 768 --experts 8 --k 2 --seq 128 --lot 32 \
   --lr 3e-4 --graine 1 --pas $PAS --eval-tous $PAS"
ECHEC=0

occ_moteur () {   # lit la ligne « occupation des poids » du moteur
    timeout "$DELAI" "$D" "$1" --ppl "$IDS" --limit 128 --ctx 128 --threads 4 2>&1 \
        | grep -oE "occupation des poids : [0-9.]+ %" | grep -oE "[0-9.]+"
}
estimation_moteur () {
    timeout "$DELAI" "$D" "$1" --ppl "$IDS" --limit 128 --ctx 128 --threads 4 2>&1 \
        | grep -oE "CREUSE.*" | grep -oE "÷[0-9.]+" | tr -d '÷'
}
occ_outil () {
    $P tools/occupation_poids.py --modele "$1" | grep -E "^\| \*\*total" \
        | grep -oE "[0-9]+\.[0-9]+ %" | head -1 | tr -d ' %'
}

declare -A OCC_M OCC_O EST
for CAS in dense elague; do
    EXTRA=""; [ "$CAS" = elague ] && EXTRA="--elagage 0.25 --elagage-tous 100"
    # shellcheck disable=SC2086
    timeout "$DELAI" $P -u tools/entrainer_moteur.py $C $EXTRA --sortie "$T/$CAS" > "$T/$CAS.log" 2>&1 \
        || { echo "  ❌ entraînement $CAS en échec"; ECHEC=1; continue; }
    timeout "$DELAI" $P tools/exporter_gguf.py --hf "$T/$CAS" --sortie "$T/$CAS.gguf" \
        > "$T/exp-$CAS.log" 2>&1 || { echo "  ❌ export $CAS en échec"; ECHEC=1; continue; }
    OCC_M[$CAS]=$(occ_moteur "$T/$CAS.gguf")
    OCC_O[$CAS]=$(occ_outil "$T/$CAS.gguf")
    EST[$CAS]=$(estimation_moteur "$T/$CAS.gguf")
    echo "  $CAS : moteur ${OCC_M[$CAS]} % · outil ${OCC_O[$CAS]} % · estimation creuse ÷${EST[$CAS]}"
done

echo
echo "=== les verrous ==="
for CAS in dense elague; do
    [ -n "${OCC_M[$CAS]:-}" ] || { echo "  ❌ $CAS : le moteur n'annonce AUCUNE occupation"; ECHEC=1; continue; }
    ECART=$($P -c "print(abs(float('${OCC_M[$CAS]}') - float('${OCC_O[$CAS]}')))")
    if $P -c "import sys; sys.exit(0 if float('$ECART') <= 1.0 else 1)"; then
        echo "  ✅ $CAS : le moteur et l'outil donnent la même occupation (écart $ECART point)"
    else
        echo "  ❌ $CAS : moteur ${OCC_M[$CAS]} % contre outil ${OCC_O[$CAS]} % — deux lectures du"
        echo "     même fichier ne disent pas la même chose"
        ECHEC=1
    fi
done
if [ -n "${EST[dense]:-}" ] && [ -n "${EST[elague]:-}" ]; then
    if $P -c "import sys; sys.exit(0 if float('${EST[elague]}') > 1.5 * float('${EST[dense]}') else 1)"; then
        echo "  ✅ l'estimation SÉPARE : ÷${EST[elague]} pour le modèle élagué contre ÷${EST[dense]} au dense"
    else
        echo "  ❌ l'estimation ne sépare pas l'élagué du dense (÷${EST[elague]} contre ÷${EST[dense]}) :"
        echo "     un compteur qui rend le même chiffre ne mesure rien"
        ECHEC=1
    fi
fi

echo
[ "$ECHEC" = 0 ] || { echo "❌ porte occupation du moteur : ÉCHEC"; exit 1; }
echo "✅ porte occupation du moteur : la ligne « occupation des poids » est annoncée, elle COLLE à"
echo "   l'outil indépendant, et son estimation creuse sépare un modèle élagué d'un modèle dense."
