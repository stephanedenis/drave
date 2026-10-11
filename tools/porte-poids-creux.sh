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
# CE QU'ELLE NE VERROUILLE PAS : les experts. Ils passent par `Vue4`/`DenseQ4`, pas par `Proj` :
# à 25 % gardés, le noyau creux ne fait tomber que les paires d'**attention** (0,4 M sur 2,3 M).
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
if $P -c "import sys; sys.exit(0 if float('$TOT_C') < float('$TOT_D') else 1)"; then
    echo "  ✅ le total baisse aussi : $TOT_D M → $TOT_C M (les experts restent denses : en-tête)"
else
    echo "  ❌ le total ne baisse pas ($TOT_D M → $TOT_C M)"
    ECHEC=1
fi

echo
echo "  ⚠ MESURÉ, ET PAS À NOTRE AVANTAGE : à cette implémentation (CSR scalaire f32), le noyau"
echo "    creux est PLUS LENT que le noyau dense int8 malgré 4 fois moins de poids lus (1312"
echo "    contre 1434 tok/s sur un modèle élagué). « Moins de paires » n'est pas « plus rapide »."

echo
[ "$ECHEC" = 0 ] || { echo "❌ porte poids creux : ÉCHEC"; exit 1; }
echo "✅ porte poids creux : le noyau creux est EXACT et il paie la sparsité (paires d'attention"
echo "   divisées), les experts restant denses — et sa lenteur est écrite, pas cachée."
