#!/bin/bash
# porte-adaptateur-sortie.sh — l'écriture d'un GGUF est-elle FIDÈLE, et l'adaptateur de sortie
# fait-il quelque chose ?
#
# POURQUOI CETTE PORTE. N4 (le chemin court entraîné) a été mesuré en torch le 14/10
# (`reports/rapport-n4-dessin-b.md`) ; la **porte d'exécution** consiste à rendre ce modèle
# exécutable par le MOTEUR — donc à écrire un GGUF (`tools/exporter_gguf_dense.py`, dense Qwen2 :
# biais q/k/v, tête liée) et à poser le lecteur appris sur le chemin tronqué
# (`--adaptateur-sortie`). Deux façons de se tromper en silence, et c'est ce qu'on vérifie :
#
#   1. un GGUF écrit de travers (dimensions inversées, quantification refaite, métadonnées
#      perdues) — le moteur le lirait quand même et rendrait un AUTRE modèle : la porte compare
#      donc les chiffres du fichier RÉÉCRIT à ceux de l'ORIGINAL, sur place ;
#   2. un drapeau qui ne fait rien — le défaut le plus coûteux du dépôt. L'invariant d'identité
#      (adaptateur = I ⇒ chiffre EXACTEMENT identique) ne suffit pas à l'exclure : une échelle
#      globale est absorbée par la norme finale, donc la porte vérifie AUSSI qu'un adaptateur qui
#      n'est pas une échelle globale CHANGE le chiffre, et que les cas invalides sont REFUSÉS
#      (code 2) au lieu d'être ignorés.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
P=${P:-python3}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
COUCHES=${COUCHES:-8}
LIMITE=${LIMITE:-256}
T=${T:-/tmp/porte-adaptateur}
[ -s "$M" ] || { echo "  ❌ modèle absent : $M"; exit 2; }
[ -x "$D" ] || { echo "  ❌ binaire du moteur absent : $D"; exit 2; }
$P -c "import numpy" 2>/dev/null || { echo "  ❌ $P n'a pas numpy (l'export en a besoin)"; exit 2; }
. tools/_corpus.sh       # régénère le corpus s'il manque (voir l'en-tête du fichier)
mkdir -p "$T"

# Le morceau de texte : les LIMITE premiers jetons du corpus, en clair pour le moteur.
$P - "$IDS" "$T/morceau.txt" "$LIMITE" <<'PY'
import pathlib, re, sys
ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(sys.argv[1]).read_text()) if x.strip()]
pathlib.Path(sys.argv[2]).write_text(",".join(str(x) for x in ids[:int(sys.argv[3])]))
PY

ppl_de() {   # $1 = arguments supplémentaires ; rend la perplexité
    "$D" "$M" --ppl "$T/morceau.txt" --limit "$LIMITE" --ctx "$LIMITE" --threads 8 \
        --couches "0:$COUCHES" --tete-partielle $1 2>&1 \
        | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+" | head -1
}
ppl_complet() {   # $1 = modèle ; perplexité du modèle entier
    "$D" "$1" --ppl "$T/morceau.txt" --limit "$LIMITE" --ctx "$LIMITE" --threads 8 2>&1 \
        | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+" | head -1
}

echo "porte de l'adaptateur de sortie — $(basename "$M") · plage 0:$COUCHES · $LIMITE jetons"

# ---------------------------------------------------------------- 1. l'ÉCRITURE est fidèle
# On réécrit le modèle de référence (déquantifié puis requantifié Q8_0, normes et biais en f32) et
# on exige les MÊMES chiffres pour le modèle complet ET pour le chemin tronqué. Un export faux se
# voit ici, pas dans une comparaison lointaine.
$P tools/exporter_gguf_dense.py --depuis-gguf "$M" --sortie "$T/reecrit.gguf" \
    > "$T/export.log" 2>&1
[ -s "$T/reecrit.gguf" ] || { echo "  ❌ l'export a échoué (voir $T/export.log)"; exit 2; }
ORIG_COMPLET=$(ppl_complet "$M")
COPIE_COMPLET=$(ppl_complet "$T/reecrit.gguf")
ORIG_TRONQ=$(ppl_de "")
COPIE_TRONQ=$("$D" "$T/reecrit.gguf" --ppl "$T/morceau.txt" --limit "$LIMITE" --ctx "$LIMITE" \
    --threads 8 --couches "0:$COUCHES" --tete-partielle 2>&1 \
    | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+" | head -1)
echo "  écriture  : complet $ORIG_COMPLET → $COPIE_COMPLET · tronqué $ORIG_TRONQ → $COPIE_TRONQ"
if [ -z "$ORIG_COMPLET" ] || [ -z "$COPIE_COMPLET" ] || [ -z "$ORIG_TRONQ" ] || [ -z "$COPIE_TRONQ" ]; then
    echo "  ❌ perplexité illisible (une porte ne mesure pas sur du vide)"; exit 1
fi
ecart_complet=$($P -c "print(abs($COPIE_COMPLET-$ORIG_COMPLET)/max($ORIG_COMPLET,1e-9))")
ecart_tronq=$($P -c "print(abs($COPIE_TRONQ-$ORIG_TRONQ)/max($ORIG_TRONQ,1e-9))")
$P -c "import sys; sys.exit(0 if $ecart_complet < 1e-6 else 1)" \
    || { echo "  ❌ le GGUF réécrit ne rend pas le modèle complet (écart $ecart_complet)"; exit 1; }
$P -c "import sys; sys.exit(0 if $ecart_tronq < 1e-6 else 1)" \
    || { echo "  ❌ le GGUF réécrit ne rend pas le chemin tronqué (écart $ecart_tronq)"; exit 1; }
echo "  ✅ l'écriture est fidèle (mêmes chiffres sur les deux chemins)"

# ---------------------------------------------------------------- 2. l'INVARIANT d'identité
$P - "$T" <<'PY'
import numpy as np, pathlib, sys
t = pathlib.Path(sys.argv[1]); h = 896
np.eye(h, dtype="<f4").tofile(t / "identite.f32")
A = np.eye(h, dtype="<f4"); A[: h // 2] *= 2.0      # PAS une échelle globale : la norme ne
A.tofile(t / "demi-echelle.f32")                    # peut donc pas l'absorber
np.eye(128, dtype="<f4").tofile(t / "mauvaise-taille.f32")
PY
PPL_IDENT=$(ppl_de "--adaptateur-sortie $T/identite.f32")
[ -n "$PPL_IDENT" ] || { echo "  ❌ l'adaptateur identité n'a rien rendu"; exit 1; }
ecart_id=$($P -c "print(abs($PPL_IDENT-$ORIG_TRONQ)/max($ORIG_TRONQ,1e-9))")
$P -c "import sys; sys.exit(0 if $ecart_id < 1e-6 else 1)" \
    || { echo "  ❌ adaptateur = identité : $PPL_IDENT au lieu de $ORIG_TRONQ"; exit 1; }
echo "  ✅ invariant d'identité : $PPL_IDENT (écart $($P -c "print(f'{$ecart_id:.2e}')"))"

# ---------------------------------------------------------------- 3. le DRAPEAU AGIT
PPL_DEMI=$(ppl_de "--adaptateur-sortie $T/demi-echelle.f32")
facteur=$($P -c "print($PPL_DEMI/max($PPL_IDENT,1e-12))")
$P -c "import sys; sys.exit(0 if $facteur > 1.5 else 1)" \
    || { echo "  ❌ le drapeau ne fait RIEN : $PPL_DEMI contre $PPL_IDENT (facteur $facteur)"; exit 1; }
echo "  ✅ le drapeau agit : demi-échelle ⇒ $PPL_DEMI (×$facteur)"

# ---------------------------------------------------------------- 4. les REFUS (code 2)
refus() {   # $1 = description, $2 = arguments
    "$D" "$M" --ppl "$T/morceau.txt" --limit 16 --ctx "$LIMITE" --threads 8 $2 >/dev/null 2>&1
    local code=$?
    if [ "$code" -ne 2 ]; then
        echo "  ❌ $1 : code $code au lieu de 2"; exit 1
    fi
}
refus "sans --tete-partielle" "--adaptateur-sortie $T/identite.f32"
refus "mauvaise taille" "--couches 0:$COUCHES --tete-partielle --adaptateur-sortie $T/mauvaise-taille.f32"
refus "fichier absent" "--couches 0:$COUCHES --tete-partielle --adaptateur-sortie $T/inexistant.f32"
echo "  ✅ les trois cas invalides sont REFUSÉS (code 2), pas ignorés"
echo "  ✅ porte tenue (écriture fidèle · invariant · effet · refus)"
exit 0
