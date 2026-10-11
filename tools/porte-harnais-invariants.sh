#!/bin/bash
# porte-harnais-invariants.sh — les deux invariants dont DÉPENDENT toutes les mesures d'élagage.
#
# POURQUOI CETTE PORTE EXISTE, ET POURQUOI ELLE REMPLACE UN SEUIL DE QUALITÉ. Le 11/10, deux
# défauts du harnais ont invalidé des mesures déjà publiées — aucun des deux n'était visible dans
# un chiffre de perplexité :
#
#   1. **l'inverse appliqué DEUX FOIS à l'installation.** `register_parametrization` réutilise le
#      tenseur du poids et le modifie SUR PLACE ; relire `w` après coup rend `log|log|w||`. Le
#      modèle log-normal partait avec des poids de **±12** au lieu de ±0,08 (θ moyen 1,097 au lieu
#      de −2,8), et sa validation d'entraînement valait 3,0713 bits/octet au lieu de 2,4874 ;
#   2. **les poids reparamétrés n'étaient plus élagués du tout.** Sous reparamétrisation,
#      `named_parameters()` rend `...parametrizations.weight.original` et non `...weight` : un
#      filtre sur les noms excluait le poids lui-même, et l'**attention** restait intacte
#      (1,0 % de zéros au lieu de 75 %) pendant que la couverture annoncée disait « 100 % ».
#
# Une porte qui verrouillerait un SEUIL DE QUALITÉ (par exemple « les signes figés battent le
# témoin de 20 % ») aurait mesuré l'artefact du défaut n° 2, puis serait devenue rouge toute seule
# une fois le défaut corrigé — ce qui est arrivé. On verrouille donc les **invariants**, pas un
# résultat : ils sont vrais indépendamment de ce que l'expérience raconte.
#
# COÛT : trois entraînements d'un pas, trois de 200 pas, trois exports — ~1 min 30.
set -u
cd "$(dirname "$0")/.."
P=${P:-/home/stephane/gpu-env/bin/python}
T=${TRAVAIL:-/tmp/porte-harnais-invariants}
PAS=${PAS:-200}
GARDE=${GARDE:-0.25}
TOL_INSTALL=${TOL_INSTALL:-1e-4}
DELAI=${DELAI:-1200}

for f in data/corpus_en.txt data/corpus_en_val.txt; do
    [ -s "$f" ] || { echo "  ❌ $f manquant : cette porte entraîne de petits modèles"; exit 2; }
done
$P -c "import torch, transformers" 2>/dev/null || { echo "  ❌ $P n'a pas torch/transformers"; exit 2; }
rm -rf "$T"; mkdir -p "$T"
C="--famille route --dim 192 --couches 4 --tetes 4 --cache 768 --experts 8 --k 2 --seq 128 --lot 32 \
   --lr 3e-4 --graine 1"
ECHEC=0

echo "=== 1. installer une reparamétrisation NE CHANGE PAS le modèle ==="
for V in "sigfiges:--signes-figes" "lognormal:--poids-lognormaux" "libres:--poids-lognormaux --signes-libres"; do
    NOM="${V%%:*}"; EXTRA="${V#*:}"
    # shellcheck disable=SC2086
    timeout "$DELAI" $P -u tools/entrainer_moteur.py $C $EXTRA --pas 2 --eval-tous 2 \
        --sortie "$T/inst-$NOM" > "$T/inst-$NOM.log" 2>&1
    LIGNE=$(grep -m1 "installation : le modèle est INCHANGÉ" "$T/inst-$NOM.log" || true)
    if [ -z "$LIGNE" ]; then
        echo "  ❌ $NOM : le harnais n'annonce PAS l'écart d'installation"
        ECHEC=1
        continue
    fi
    ECART=$(printf '%s' "$LIGNE" | grep -oE "[0-9.]+e[-+][0-9]+" | head -1)
    echo "  $NOM : $LIGNE"
    if $P -c "import sys; sys.exit(0 if float('$ECART') <= float('$TOL_INSTALL') else 1)"; then
        echo "    ✅ écart $ECART ≤ $TOL_INSTALL : le modèle part du même point que le témoin"
    else
        echo "    ❌ écart $ECART > $TOL_INSTALL : le modèle reparamétré n'est PAS celui du témoin"
        ECHEC=1
    fi
done

echo
echo "=== 2. l'élagage atteint AUSSI les poids reparamétrés (l'attention, pas seulement les experts) ==="
for V in "sigfiges:--signes-figes" "lognormal:--poids-lognormaux" "libres:--poids-lognormaux --signes-libres"; do
    NOM="${V%%:*}"; EXTRA="${V#*:}"
    # shellcheck disable=SC2086
    timeout "$DELAI" $P -u tools/entrainer_moteur.py $C $EXTRA --pas "$PAS" --eval-tous "$PAS" \
        --elagage-tous 100 --elagage "$GARDE" --sortie "$T/$NOM" > "$T/$NOM.log" 2>&1
    timeout "$DELAI" $P tools/exporter_gguf.py --hf "$T/$NOM" --sortie "$T/$NOM.gguf" \
        > "$T/exp-$NOM.log" 2>&1 || { echo "  ❌ export $NOM en échec"; ECHEC=1; continue; }
    OCC=$($P tools/occupation_poids.py --modele "$T/$NOM.gguf" \
          | grep -E "^\| attention" | grep -oE "[0-9]+\.[0-9]+" | tail -1)
    echo "  $NOM : occupation de l'ATTENTION à $OCC % (cible : $GARDE gardé)"
    if $P -c "import sys; o=float('$OCC'); c=100*float('$GARDE'); sys.exit(0 if abs(o-c) <= 10 else 1)"; then
        echo "    ✅ l'attention est élaguée comme les experts"
    else
        echo "    ❌ l'attention NE SUIT PAS la cible : les poids reparamétrés échappent à l'élagage"
        ECHEC=1
    fi
done

echo
[ "$ECHEC" = 0 ] || { echo "❌ porte harnais : ÉCHEC"; exit 1; }
echo "✅ porte harnais : installer une reparamétrisation laisse le modèle intact, et l'élagage"
echo "   atteint les poids reparamétrés (attention comprise) — pour les trois variantes."
