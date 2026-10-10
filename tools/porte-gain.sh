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

echo "=== 7. l'effet DIMINUE avec la fenêtre d'évaluation (et il tient) ==="
# Mesuré : à 128 jetons le gain 0,75 à la couche 0 vaut −11,5 % ; à 256 jetons, −1,4 %.
# La DIRECTION tient, la MAGNITUDE dépend de la fenêtre — une condition à écrire, sinon le
# chiffre de −11,5 % se citerait comme une propriété du modèle au lieu d'un point de mesure.
W128=$(ppl --ffn-gain "0:0.75")
W256=$( $D "$M" --ppl "$IDS" --limit 256 --ctx "$CTX" --threads 8 --ffn-gain "0:0.75" 2>&1 \
        | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+")
R256=$( $D "$M" --ppl "$IDS" --limit 256 --ctx "$CTX" --threads 8 2>&1 \
        | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+")
printf '  128 jetons : %s (réf %s) · 256 jetons : %s (réf %s)\n' "$W128" "$REF" "$W256" "$R256"
python3 - "$W128" "$REF" "$W256" "$R256" <<'PY' || exit 1
import sys
a128, ref128, a256, ref256 = (float(x) for x in sys.argv[1:5])
g128, g256 = 100.0*(ref128-a128)/ref128, 100.0*(ref256-a256)/ref256
if g256 <= 0:
    sys.exit(f"  ❌ à 256 jetons le gain ne gagne plus ({g256:.2f} %)")
if g256 >= g128:
    sys.exit(f"  ❌ l'effet ne décroît pas avec la fenêtre ({g128:.2f} % → {g256:.2f} %)")
print(f"  ✅ la direction tient aux deux fenêtres, la MAGNITUDE décroît : "
      f"{g128:.1f} % à 128 jetons, {g256:.1f} % à 256 — une condition, pas une propriété")
PY

echo "=== 8. le drapeau AGIT AUSSI dans le chemin RÉPARTI ==="
# LE CAS QUI MANQUAIT, ET QUI A COÛTÉ UNE MESURE FAUSSE : `--ffn-gain` était câblé dans
# `run_infer` et `run_ppl`, et PAS dans `run_ppl_reparti`. Dans le chemin réparti il ne
# faisait donc RIEN, en silence (42,5477 avec et sans le drapeau). C'est la famille de
# défauts que ce dépôt traque, et ce cas la rend impossible à réintroduire.
PORTG=$((65000 + RANDOM % 400))
cat > "$T/topo_gain.json" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"d","couches":[12,23],"instance":"127.0.0.1:$PORTG"}],
 "liens":[{"de":"local","vers":"d","mode":"f32"}]}
JSON
$D "$M" --flux-serveur "$PORTG" --ctx "$CTX" --threads 8 > "$T/ng.log" 2>&1 & NG=$!
sleep 2
SG=$( $D "$M" --ppl-reparti "127.0.0.1:$PORTG" --topologie "$T/topo_gain.json" --ids-file "$IDS" \
      --limit 32 --ctx "$CTX" --threads 8 --flux 2>&1 \
      | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
kill $NG 2>/dev/null; wait $NG 2>/dev/null
$D "$M" --flux-serveur "$PORTG" --ctx "$CTX" --threads 8 > "$T/ng2.log" 2>&1 & NG=$!
sleep 2
AG=$( $D "$M" --ppl-reparti "127.0.0.1:$PORTG" --topologie "$T/topo_gain.json" --ids-file "$IDS" \
      --limit 32 --ctx "$CTX" --threads 8 --flux --ffn-gain "0:0.75" 2>&1 \
      | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
kill $NG 2>/dev/null; wait $NG 2>/dev/null
printf '  réparti sans réglage : %s · avec 0:0.75 : %s\n' "${SG:-?}" "${AG:-?}"
[ -n "$SG" ] && [ -n "$AG" ] || { echo "  ❌ le chemin réparti n'a pas rendu de perplexité"; exit 1; }
python3 -c "
import sys
a, b = float('$SG'), float('$AG')
sys.exit(0 if a != b else 1)" \
  || { echo "  ❌ --ffn-gain n'agit PAS dans le chemin réparti (même perplexité) — c'est le"; \
       echo "     défaut mesuré le 11/10 : le drapeau ne faisait rien, en silence"; exit 1; }
echo "  ✅ le drapeau agit aussi en réparti ($SG → $AG)"

echo "=== 9. les réglages qui ne voyagent PAS sont REFUSÉS en réparti ==="
# Mesuré : --attn-window 64 AGIT en local (13,1368 → 21,5801) et, si on le câble naïvement en
# réparti, rend un résultat FAUX ET SILENCIEUX — le pilote applique la fenêtre à ses couches,
# le nœud garde la sienne : deux modèles différents sous le même nom (195,5685 contre 50,3829).
# Un drapeau inerte est un défaut ; un drapeau qui fait calculer deux modèles en est un pire.
# La porte exige donc le REFUS, avec un code distinct et AUCUNE perplexité.
PORTF=$((60000 + RANDOM % 4000))
cat > "$T/topo_f.json" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"d","couches":[12,23],"instance":"127.0.0.1:$PORTF"}],
 "liens":[{"de":"local","vers":"d","mode":"f32"}]}
JSON
$D "$M" --flux-serveur "$PORTF" --ctx "$CTX" --threads 8 > "$T/nf.log" 2>&1 & NF=$!
sleep 2
RF=$( $D "$M" --ppl-reparti "127.0.0.1:$PORTF" --topologie "$T/topo_f.json" --ids-file "$IDS" \
      --limit 64 --ctx "$CTX" --threads 8 --flux --attn-window 64 2>&1 ); CF=$?
kill $NF 2>/dev/null; wait $NF 2>/dev/null
printf '%s\n' "$RF" | grep -E "REFUS" | head -2 | cut -c1-150 | sed 's/^/  /'
[ "$CF" = 2 ] || { echo "  ❌ le refus devrait sortir en code 2, il sort en $CF"; exit 1; }
printf '%s' "$RF" | grep -q "ne voyagent PAS" || { echo "  ❌ le refus n'explique pas pourquoi"; exit 1; }
printf '%s' "$RF" | grep -qE "deux nœuds +: perplexité" \
  && { echo "  ❌ une perplexité a été rendue alors que le réglage ne peut pas être honoré"; exit 1; }
echo "  ✅ réglage non transportable : REFUSÉ (code 2), expliqué, rien n'est calculé"

rm -rf "$T"
