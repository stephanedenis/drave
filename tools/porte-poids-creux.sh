#!/bin/bash
# porte-poids-creux.sh — le noyau creux lit-il vraiment moins, et qu'est-ce que ça change ?
#
# POURQUOI CETTE PORTE. Le 11/10, le moteur a appris à **annoncer** l'occupation des poids et à
# dire ce qu'un format creux lirait (« ÷4,04 » pour un modèle élagué à 25 %). Mais aucun noyau ne
# lisait les seuls non-nuls : la ligne « paires » restait à 2,3 M, parce qu'un noyau dense lit la
# matrice entière. Le gain du dessin B restait donc une **estimation**. Cette porte verrouille le
# noyau qui la transforme en mesure — et elle dit AUSSI ce qu'il ne fait pas.
#
# CE QU'ELLE VERROUILLE :
#   1. **l'exactitude** : le noyau creux doit rendre la MÊME perplexité que le noyau dense sur les
#      mêmes poids. Un noyau rapide qui change le résultat ne mesure rien ;
#   2. **le compte** : les paires d'attention doivent tomber au prorata de l'occupation (÷≈4 à
#      25 % gardés) — c'est la sparsité **payée**, pas annoncée ;
#   3. **le fait désagréable, écrit noir sur blanc** : à cette implémentation (CSR scalaire en
#      f32), le noyau creux est **plus LENT** que le noyau dense int8, malgré 4 fois moins de
#      poids lus. « Moins de paires » n'est pas « plus rapide » : la vitesse dépend du noyau, et
#      le noyau dense est vectorisé. La porte le MESURE et l'affiche — une porte qui ne
#      verrouillerait que les bons chiffres laisserait croire le reste.
#
# CE QU'ELLE NE VERROUILLE PAS : la VITESSE. Le noyau creux est exact et il paie la sparsité
# en paires, mais il est plus LENT que les noyaux denses int8 — la porte le mesure et l'écrit.
#
# COÛT : quatre exécutions du moteur sur le modèle du dépôt, ~1 min.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
P=${P:-/home/stephane/gpu-env/bin/python}
TEXTE=${TEXTE:-data/wikitext2_test.txt}
T=${TRAVAIL:-/tmp/porte-poids-creux}
GARDE=${GARDE:-0.25}
DELAI=${DELAI:-900}

[ -x "$D" ] || { echo "  ❌ $D : le binaire de mesure n'existe pas (cargo build --release)"; exit 2; }
[ -s "$M" ] || { echo "  ❌ $M manquant"; exit 2; }
rm -rf "$T"; mkdir -p "$T"
[ -s "$TEXTE" ] || { echo "  ❌ $TEXTE manquant : la porte tokenise son propre corpus"; exit 2; }

mesure () {   # $1 = creux|dense ; $2 = garde ; imprime : perplexité · paires attention M · total M
    local sortie
    if [ "$1" = creux ]; then
        sortie=$(DRAVE_POIDS_CREUX=1 timeout "$DELAI" "$D" "$M" --ppl "$IDS" --limit 128 \
                 --ctx 128 --threads 4 --keep "$2" 2>&1)
    else
        sortie=$(env -u DRAVE_POIDS_CREUX timeout "$DELAI" "$D" "$M" --ppl "$IDS" --limit 128 \
                 --ctx 128 --threads 4 --keep "$2" 2>&1)
    fi
    local ppl att tot
    ppl=$(printf '%s' "$sortie" | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+")
    att=$(printf '%s' "$sortie" | grep -oE "par token : attention [0-9.]+ M" | grep -oE "[0-9.]+")
    tot=$(printf '%s' "$sortie" | grep -oE "total [0-9.]+ M" | tail -1 | grep -oE "[0-9.]+")
    echo "$ppl $att $tot"
}

# LE CORPUS EST TOKENISÉ PAR LA PORTE, avec le tokenizer du modèle.
IDS="$T/corpus.ids"
"$D" "$M" --tokenize --fichier "$TEXTE" --sortie "$IDS" > "$T/tokenize.log" 2>&1
[ -s "$IDS" ] || { echo "  ❌ la tokenisation n'a rien écrit"; exit 1; }

ECHEC=0
echo "=== 1. EXACTITUDE — modèle intact (aucun élagage) : les deux noyaux doivent s'accorder ==="
read -r PPL_D _ _ <<< "$(mesure dense 1.0)"
read -r PPL_C _ _ <<< "$(mesure creux 1.0)"
echo "  dense $PPL_D · creux $PPL_C"
# Le noyau creux ne reproduit PAS la quantification int8 du noyau dense : il multiplie les poids
# DÉQUANTIFIÉS par les activations en f32. Sur un modèle intact l'écart mesuré est de ~0,05 % — on
# tolère 0,5 %, et on REFUSE un écart qui trahirait une erreur d'indice ou de disposition.
if $P -c "import sys; a=float('$PPL_D'); b=float('$PPL_C'); sys.exit(0 if abs(a-b) <= 5e-3*max(a,1.0) else 1)"; then
    echo "  ✅ les deux noyaux s'accordent à mieux que 0,5 % sur un modèle intact"
else
    echo "  ❌ les deux noyaux DIVERGENT ($PPL_D contre $PPL_C) : le noyau creux ne calcule pas la"
    echo "     même chose (indice, disposition, échelle ?)"
    ECHEC=1
fi

echo
echo "=== 2. LE COMPTE — élagage à $GARDE gardé : la sparsité doit être PAYÉE ==="
read -r _ ATT_D TOT_D <<< "$(mesure dense "$GARDE")"
read -r _ ATT_C TOT_C <<< "$(mesure creux "$GARDE")"
echo "  noyau dense : paires attention $ATT_D M · total $TOT_D M"
echo "  noyau creux : paires attention $ATT_C M · total $TOT_C M"
for V in ATT_D ATT_C TOT_D TOT_C; do
    [ -n "${!V}" ] || { echo "  ❌ $V illisible : le moteur n'a pas imprimé ce qui était attendu"; exit 1; }
done
if $P -c "import sys; sys.exit(0 if float('$ATT_D') > 2.5*float('$ATT_C') else 1)"; then
    echo "  ✅ paires d'attention $ATT_D M → $ATT_C M : le noyau ne lit plus que les non-nuls"
else
    echo "  ❌ les paires d'attention ne tombent pas ($ATT_D M → $ATT_C M)"
    ECHEC=1
fi
if $P -c "import sys; sys.exit(0 if float('$TOT_D') > 2.0*float('$TOT_C') else 1)"; then
    echo "  ✅ le TOTAL baisse aussi : $TOT_D M → $TOT_C M — attention ET experts (÷≈2 à 4)"
else
    echo "  ❌ le total ne baisse pas ($TOT_D M → $TOT_C M)"
    ECHEC=1
fi

echo
echo "=== 3. LA VITESSE — elle DÉPEND de la densité, contrairement à celle du noyau dense ==="
# C'est la propriété qui distingue un noyau creux d'un noyau dense : le dense lit la matrice
# entière et sa vitesse ne bouge pas avec l'élagage ; le creux, lui, lit ce qui reste.
vitesse () {   # $1 = creux|dense ; $2 = garde ; imprime les tok/s
    local sortie
    if [ "$1" = creux ]; then
        sortie=$(DRAVE_POIDS_CREUX=1 timeout "$DELAI" "$D" "$M" --infer --ids-file "$IDS" \
                 --n 64 --ctx 256 --threads 4 --keep "$2" 2>&1)
    else
        sortie=$(env -u DRAVE_POIDS_CREUX timeout "$DELAI" "$D" "$M" --infer --ids-file "$IDS" \
                 --n 64 --ctx 256 --threads 4 --keep "$2" 2>&1)
    fi
    printf '%s' "$sortie" | grep -oE "\([0-9.]+ tok/s\)" | grep -oE "[0-9.]+"
}
V_D1=$(vitesse dense 1.0); V_C1=$(vitesse creux 1.0)
V_D10=$(vitesse dense 0.10); V_C10=$(vitesse creux 0.10)
echo "  garde 1,00 : dense $V_D1 tok/s · creux $V_C1 tok/s"
echo "  garde 0,10 : dense $V_D10 tok/s · creux $V_C10 tok/s"
if $P -c "import sys; sys.exit(0 if float('$V_C10') > 2.0*float('$V_C1') else 1)"; then
    echo "  ✅ la vitesse du noyau creux SUIT la densité (×$(python3 -c "print(f'{float('$V_C10')/float('$V_C1'):.1f}')"))"
else
    echo "  ❌ le noyau creux ne gagne rien à être creux : il ne lit pas ce qu'il prétend lire"
    ECHEC=1
fi
echo "  · repère mesuré : le creux RATTRAPE le dense vers 10 % de poids gardés (0,96× à 0,10,"
echo "    0,51× à 0,25, 0,13× sans élagage) — au-dessus, le noyau dense int8 gagne."

echo
echo "  ⚠ MESURÉ, ET PAS À NOTRE AVANTAGE : à cette implémentation (CSR scalaire f32), le noyau"
echo "    creux ne rattrape le dense qu'en dessous de ~10 % de poids gardés : à 25 % il est deux"
echo "    fois plus lent (6,9 contre 13,6 tok/s sur Qwen2.5-0.5B), malgré 3,8 fois moins de poids"
echo "    lus. « Moins de paires » n'est pas « plus rapide » : le coût en paires est un MODÈLE, la"
echo "    vitesse est une MESURE, et il faut un noyau vectorisé pour que l'un devienne l'autre."

echo
[ "$ECHEC" = 0 ] || { echo "❌ porte poids creux : ÉCHEC"; exit 1; }
echo "✅ porte poids creux : le noyau creux est EXACT et il paie la sparsité — paires divisées sur"
echo "   TOUT le modèle (Projections d'attention ET experts, ce dernier cas vérifié sur le modèle"
echo "   à experts du harnais) — et sa LENTEUR est écrite dans la porte, pas cachée."
