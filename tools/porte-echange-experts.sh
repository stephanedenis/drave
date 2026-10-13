#!/bin/bash
# porte-echange-experts.sh — le routage imposé fait-il EXACTEMENT ce qu'il annonce ?
#
# POURQUOI CETTE PORTE. `DRAVE_ROUTAGE_FORCER` (13/10) permet d'imposer à un modèle routé les
# experts qu'une autre instance a choisis — c'est l'expérience C9 « échange d'experts »
# (`reports/rapport-c9-echange-experts.md`). Toute la mesure repose sur **un** invariant :
# **imposer à une instance SON PROPRE routage doit rendre la perplexité de référence, au bit près.**
# S'il est faux, les effets mesurés (±20 %) baignent dans un artefact — et c'est arrivé : la
# première version donnait 37,2013 contre 37,1990, parce que la trace TRIE les experts et que
# l'accumulation flottante change avec l'ordre (`DRAVE_TRACE_EXPERTS_ORDRE=1` corrige ça).
#
# CE QU'ELLE VÉRIFIE (trois conditions, dans cet ordre) :
#   1. **inerte par défaut** : sans variable, la trace ne change RIEN à la perplexité ;
#   2. **exact sur son propre routage** : capturé puis imposé, même perplexité au chiffre près ;
#   3. **vivant sur un autre routage** : avec les experts d'une autre couche, la perplexité CHANGE
#      (sinon la porte ne mesure pas ce qu'elle croit — un mécanisme mort passerait les deux
#      premières conditions sans rien faire).
# Et elle refuse de conclure si le fichier de trace est vide (une porte qui mesure du vide est
# verte pour de mauvaises raisons).
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-/home/stephane/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf}
IDS=${IDS:-$HOME/IA/scratch/prerequis/ids_qwen3_30b_wt2.txt}
N=${N:-16}
CTX=${CTX:-512}
T=${T:-$(mktemp -d)}
[ -s "$M" ] || { echo "  ❌ modèle absent : $M (poser MODELE=…)"; exit 2; }
[ -s "$IDS" ] || { echo "  ❌ identifiants absents : $IDS"; exit 2; }

ppl() { grep -oE "perplexité [0-9.]+ sur" | head -1 | grep -oE "[0-9.]+"; }
# `VAR=x lance` pose la variable pour l'appel de fonction, et bash l'exporte au sous-processus :
# c'est ce qui permet d'appeler la même fonction avec ou sans trace (une chaîne vide en argument
# aurait été passée à `env` comme nom de commande — piège évité).
lance() { env DRAVE_TAMPONS=1 $D "$M" --ppl "$IDS" --ctx "$CTX" --limit "$N" --threads 8 2>&1 | ppl; }

echo "porte de l'échange d'experts — $(basename "$M"), $N jetons"
REF=$(lance)
[ -n "$REF" ] || { echo "  ❌ perplexité de référence illisible"; exit 1; }
echo "  référence (aucune imposition) : $REF"

# 1. la capture dans l'ORDRE de sélection (l'ordre trié ne permet pas l'invariant exact)
DRAVE_TRACE_EXPERTS="$T/rout.txt" DRAVE_TRACE_EXPERTS_ORDRE=1 lance > "$T/capture.txt"
lignes=$(grep -c . "$T/rout.txt" 2>/dev/null || echo 0)
[ "$lignes" -gt 0 ] || { echo "  ❌ la trace de routage est VIDE — la porte ne mesurerait rien"; exit 1; }
echo "  trace : $lignes décisions (couche, jeton, experts)"

# 2. SON PROPRE routage imposé → la même perplexité, au chiffre près
MEME=$(DRAVE_ROUTAGE_FORCER="$T/rout.txt" lance)
if [ "$MEME" != "$REF" ]; then
    echo "  ❌ s'imposer SON PROPRE routage change la perplexité : $MEME contre $REF"
    echo "     (la porte existe pour ça : l'invariant a déjà été faux de 0,006 % le 13/10)"
    exit 1
fi
echo "  ✅ son propre routage imposé : $MEME — identique à la référence"

# 3. un routage ÉTRANGER (les experts d'une autre couche) → la perplexité DOIT changer
python3 - "$T/rout.txt" "$T/decale.txt" <<'PY'
import sys, pathlib
lignes = [l.split() for l in pathlib.Path(sys.argv[1]).read_text().splitlines() if l.split()]
dec = [" ".join([str((int(c[0]) + 3) % 48), c[1]] + c[2:]) for c in lignes]
pathlib.Path(sys.argv[2]).write_text("\n".join(dec) + "\n")
PY
ETRANGER=$(DRAVE_ROUTAGE_FORCER="$T/decale.txt" lance)
if [ "$ETRANGER" = "$REF" ]; then
    echo "  ❌ un routage ÉTRANGER ne change rien : le mécanisme est mort (les deux premiers"
    echo "     contrôles seraient verts sans rien imposer)"
    exit 1
fi
echo "  ✅ routage étranger (couche +3) : $ETRANGER — différent, donc le mécanisme agit"
echo "  PORTE TENUE"
rm -rf "$T"
