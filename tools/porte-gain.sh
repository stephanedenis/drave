#!/bin/bash
# porte-gain.sh — E4 : le GAIN de la FFN par couche, et l'équilibre excitation/inhibition.
#
# L'HYPOTHÈSE BIOLOGIQUE (docs/biologie-pour-drave.md, E4) : un réseau cortical équilibré
# vit près d'un point où excitation et inhibition se compensent, et un déséquilibre dans un
# sens ou dans l'autre coûte. Transposée au moteur, la question mesurable est : **existe-t-il
# un gain de la FFN, par couche, qui AMÉLIORE la perplexité — et est-il intérieur** (ni 0,
# ni 1, ni l'infini) ?
#
# CE QUE LA MESURE A DONNÉ, et les deux moitiés ne disent pas la même chose :
#   · du côté INHIBITION (gain < 1), la courbe est MONOTONE : toute inhibition dégrade, et
#     l'hypothèse d'un optimum intérieur y est RÉFUTÉE ;
#   · du côté AMPLIFICATION, l'optimum est INTÉRIEUR et net sur les premières couches :
#     couche 0 à 0,75 → **12,9635** contre **14,6496** sans réglage (**−11,5 %**), et couche
#     1 à 0,5 → 13,7907 (−5,9 %) ; la couche 2 n'a plus d'optimum utile.
#   · en dessous de l'optimum, une FALAISE : couche 0 à 0,25 → **996,04** (le gain trop
#     faible à la première couche casse le modèle, il ne le dégrade pas un peu).
#
# Ce que la porte verrouille :
#   1. `--ffn-gain L:1.0` **EST** l'absence de réglage (perplexité identique AU CHIFFRE,
#      vérifiée sur trois couches) — sans cet invariant, aucune des autres lignes ne
#      comparerait quoi que ce soit ;
#   2. l'inhibition est MONOTONE : à une couche du milieu, chaque gain plus petit que 1 fait
#      strictement pire que le précédent ;
#   3. l'optimum intérieur existe là où il a été trouvé (couche 0 : 0,75 bat 0,5 ET 1,5) ;
#   4. et la falaise est réelle (0,25 à la couche 0 est catastrophique) — un résultat qu'un
#      réglage « un peu plus prudent » ne laisse pas deviner.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
LIMITE=${LIMITE:-128}
CTX=${CTX:-512}
T=$(mktemp -d)
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }

ppl() { # $@ = drapeaux
  $D "$M" --ppl "$IDS" --limit "$LIMITE" --ctx "$CTX" --threads 8 "$@" 2>&1 \
    | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+"
}

echo "=== 1. invariant : --ffn-gain L:1.0 EST l'absence de réglage ==="
REF=$(ppl)
echo "  sans réglage : $REF"
for L in 0 6 18; do
  P=$(ppl --ffn-gain "$L:1.0")
  printf '  couche %-3s gain 1.0 : %s\n' "$L" "${P:-échec}"
  [ "$P" = "$REF" ] || { echo "  ❌ le gain 1.0 à la couche $L n'est pas l'identité ($P contre $REF)"; exit 1; }
done
echo "  ✅ l'identité est exacte sur trois couches"

echo "=== 2. inhibition MONOTONE (couche 12) ==="
PREV=""
for V in 0.0 -0.25 -0.5 -1.0; do
  P=$(ppl --ffn-gain "12:$V")
  printf '  gain %-6s : %s\n' "$V" "${P:-échec}"
  if [ -n "$PREV" ]; then
    python3 -c "
import sys
a, b = float('$PREV'), float('$P')
sys.exit(0 if b >= a else 1)" || { echo "  ❌ l'inhibition n'est pas monotone ($PREV → $P)"; exit 1; }
  fi
  PREV=$P
done
echo "  ✅ toute inhibition dégrade, et de plus en plus : l'optimum intérieur est réfuté de ce côté"

echo "=== 3. optimum INTÉRIEUR (couche 0) : 0,75 doit battre 0,5 ET 1,5 ==="
P05=$(ppl --ffn-gain "0:0.5"); P075=$(ppl --ffn-gain "0:0.75"); P15=$(ppl --ffn-gain "0:1.5")
printf '  gain 0,5 : %s · 0,75 : %s · 1,5 : %s\n' "$P05" "$P075" "$P15"
python3 - "$P05" "$P075" "$P15" "$REF" <<'PY' || exit 1
import sys
a, b, c, ref = (float(x) for x in sys.argv[1:5])
if not (b < a and b < c and b < ref):
    sys.exit(f"  ❌ pas d'optimum intérieur à la couche 0 : {b} n'est pas sous {a}, {c} et {ref}")
print(f"  ✅ optimum intérieur : {b} contre {a}, {c} et {ref} sans réglage "
      f"({100.0*(ref-b)/ref:.1f} % de mieux)")
PY

echo "=== 4. la FALAISE : 0,25 à la couche 0 casse le modèle ==="
P025=$(ppl --ffn-gain "0:0.25")
echo "  gain 0,25 : $P025"
python3 - "$P025" "$REF" <<'PY' || exit 1
import sys
a, ref = float(sys.argv[1]), float(sys.argv[2])
if a < 2.0 * ref:
    sys.exit(f"  ❌ le gain 0,25 à la couche 0 ne casse pas le modèle ({a} contre {ref})")
print(f"  ✅ la falaise est réelle : {a} contre {ref} ({a/ref:.0f}× pire)")
PY

echo "=== 5. le bénéfice est LOCALISÉ aux deux premières couches ==="
# Mesuré sur les 24 couches à 0,75 : seules les couches 0 (−11,5 %) et 1 (−4,5 %) gagnent ;
# les couches 2 et 3 perdent beaucoup (+9,2 %, +10,6 %) et les suivantes restent dans ±1 %
# (sauf 17, 21, 23 : +3,8 à +5,7 %). Le déséquilibre est donc à l'ENTRÉE, pas réparti.
P0=$(ppl --ffn-gain "0:0.75"); P1=$(ppl --ffn-gain "1:0.75"); P5=$(ppl --ffn-gain "5:0.75")
printf '  couche 0 : %s · couche 1 : %s · couche 5 : %s (référence %s)\n' "$P0" "$P1" "$P5" "$REF"
python3 - "$P0" "$P1" "$P5" "$REF" <<'PY' || exit 1
import sys
p0, p1, p5, ref = (float(x) for x in sys.argv[1:5])
if not (p0 < ref and p1 < ref):
    sys.exit(f"  ❌ les couches 0 et 1 devraient gagner : {p0}, {p1} contre {ref}")
if p5 < ref:
    sys.exit(f"  ❌ la couche 5 gagne aussi ({p5} contre {ref}) : le bénéfice n'est pas localisé")
print(f"  ✅ le bénéfice est à l'ENTRÉE : couches 0 et 1 à {p0} et {p1} (mieux que {ref}), "
      f"couche 5 à {p5} (pas mieux)")
PY

echo "=== 6. un PROFIL ne compose PAS : il défait le meilleur réglage seul ==="
# Mesuré : 0,75 seul à la couche 0 donne 12,9635 ; y AJOUTER 0,5 à la couche 1 donne 13,7679,
# soit MOINS BIEN. Les deux gains ne se composent donc pas, ils s'antagonisent en partie — et
# l'espoir d'un « profil appris par couche » (dessin I) se heurte à cette mesure : le meilleur
# profil mesuré est un réglage SEUL.
PROF1=$(ppl --ffn-gain "0:0.75")
PROF2=$(ppl --ffn-gain "0:0.75,1:0.5")
PROF3=$(ppl --ffn-gain "0:0.75,1:0.5,2:1.0")
printf '  0:0.75 seul : %s · +1:0.5 : %s · +1:0.5+2:1.0 : %s\n' "$PROF1" "$PROF2" "$PROF3"
python3 - "$PROF1" "$PROF2" "$PROF3" <<'PY' || exit 1
import sys
un, deux, trois = (float(x) for x in sys.argv[1:4])
if deux <= un:
    sys.exit(f"  ❌ la composition ({deux}) bat le réglage seul ({un}) : ma mesure serait fausse")
if trois != deux:
    sys.exit(f"  ❌ un gain de 1,0 dans un profil n'est pas neutre : {deux} → {trois}")
print(f"  ✅ la composition DÉGRADE ({un} → {deux}), et un gain 1,0 y est exactement neutre "
      f"({deux} = {trois})")
PY

rm -rf "$T"
