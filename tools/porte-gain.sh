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
#      réglage « un peu plus prudent » ne laisse pas deviner ;
#   5. un réglage TRANSPORTÉ est HONORÉ des deux côtés (§9 : `--attn-window` en reparti,
#      la propriété que le v7 a rendue vraie — et la porte était rouge depuis le v7 sans
#      que personne le voie) ;
#   6. un réglage qui ne peut RIEN faire est REFUSÉ plutôt que silencieusement ignoré
#      (§10 : `--attn-sinks`, déclaré, transporté par le v7, lu nulle part).
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

echo "=== 9. le réglage transporté est appliqué des DEUX côtés : deux découpages, un seul chiffre ==="
# CETTE SECTION ÉTAIT ROUGE DEPUIS LE v7, ET PERSONNE NE L'A VUE.
#
# Elle exigeait un REFUS (`code 2`) pour `--attn-window` en réparti, écrit au commit e6f7b6b,
# quand le pilote et le nœud pouvaient appliquer DEUX FENÊTRES DIFFÉRENTES sous le même nom
# (195,5685 contre 50,3829 : deux modèles). Le v7 a fait VOYAGER les trois réglages dans la
# trame, et le refus a été retiré délibérément (`main.rs:4432`, commentaire à l'appui). La porte
# a continué d'exiger le refus : elle ne pouvait plus passer, et ne mesurait donc plus rien.
#
# CE QUI LA REMPLACE EST PLUS FORT QUE LE REFUS, et c'est décisif pour les DEUX côtés À LA FOIS.
# Le découpage est EXACT (mesuré 0,00e0 dans les modes flux) : deux découpages différents, sous
# les MÊMES drapeaux, doivent donc rendre le MÊME chiffre. Or la fenêtre ne s'applique qu'aux
# couches de la branche à fenêtre, et chaque côté n'en tient qu'une moitié :
#   · si le PILOTE n'appliquait pas la fenêtre (le défaut du round 28, où deux nombres égaux
#     cachaient deux réglages inertes), le découpage 0-11|12-23 fenêtrerait 12 couches et le
#     découpage 0-3|4-23 en fenêtrerait 20 — les chiffres divergeraient ;
#   · si le NŒUD ne la recevait pas (ce que le v7 a corrigé), même conclusion.
# Égalité des deux découpages = le réglage est honoré des deux côtés. Mesuré : 65,6625 = 65,6625.
#
# ET LA GARDE CONTRE LE PIÈGE « DEUX RÉGLAGES INERTES » : il faut d'abord que la fenêtre MORDE
# dans cette configuration (référence sans fenêtre à 59,0790, soit +11,1 % avec) — sans quoi
# l'égalité serait celle de deux calculs que le drapeau ne touche pas.
PORTF=$((60000 + RANDOM % 4000))
cat > "$T/topo_9a.json" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"d","couches":[12,23],"instance":"127.0.0.1:$PORTF"}],
 "liens":[{"de":"local","vers":"d","mode":"f32"}]}
JSON
cat > "$T/topo_9b.json" <<JSON
{"regions":[
  {"id":"local","couches":[0,3],"instance":"local"},
  {"id":"d","couches":[4,23],"instance":"127.0.0.1:$PORTF"}],
 "liens":[{"de":"local","vers":"d","mode":"f32"}]}
JSON
# le nœud sert UNE connexion : il est RELANCÉ entre chaque essai (erreur de harnais n°4 du
# sprint, celle qui faisait croire que tous les drapeaux étaient inertes)
reparti9 () { # $1 = topologie, $@ = drapeaux
  local topo=$1; shift
  $D "$M" --flux-serveur "$PORTF" --ctx "$CTX" --threads 8 > "$T/n9.log" 2>&1 & local NP=$!
  sleep 2
  $D "$M" --ppl-reparti "127.0.0.1:$PORTF" --topologie "$topo" --ids-file "$IDS" \
      --limit 64 --ctx "$CTX" --threads 8 --flux "$@" 2>&1 \
    | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$"
  kill $NP 2>/dev/null; wait $NP 2>/dev/null
}
R9=$(reparti9 "$T/topo_9a.json")
W9A=$(reparti9 "$T/topo_9a.json" --attn-window 32)
W9B=$(reparti9 "$T/topo_9b.json" --attn-window 32)
printf '  sans fenêtre (0-11|12-23) : %s\n' "${R9:-?}"
printf '  fenêtre 32 (0-11|12-23)   : %s\n' "${W9A:-?}"
printf '  fenêtre 32 (0-3|4-23)     : %s\n' "${W9B:-?}"
[ -n "$R9" ] && [ -n "$W9A" ] && [ -n "$W9B" ] || { echo "  ❌ le chemin réparti n'a pas rendu de perplexité"; exit 1; }
python3 -c "
import sys
r, a, b = float('$R9'), float('$W9A'), float('$W9B')
if not abs(a - r) / r > 0.03:
    sys.exit('la fenêtre ne MORD pas ici (%.4f vs %.4f) : légalité serait celle de deux réglages inertes' % (a, r))
if abs(a - b) / a > 0.001:
    sys.exit('les deux découpages divergent (%.4f vs %.4f) : le réglage n est pas appliqué des DEUX côtés' % (a, b))
" || { echo "  ❌ le réglage transporté n'est pas honoré des deux côtés (cf. commentaire ci-dessus)"; exit 1; }
echo "  ✅ la fenêtre mord ($R9 → $W9A) ET les deux découpages s'accordent ($W9A = $W9B, écart 0,00 %)"

echo "=== 10. `--attn-sinks` n'est PAS mort : il est CIRCONSTANCIÉ (et le zéro n'existait pas) ==="
# CE QUE LE §46 bis AVAIT MAL LU, ET COMMENT L'ERREUR A ÉTÉ FAITE.
#
# Le sprint avait conclu que le compteur de puits était « écrit partout, transporté par le v7…
# et LU NULLE PART », et allait REFUSER le drapeau. C'était FAUX, et la vérification tenait en
# une ligne de code : `model.rs:7472` le lit (`let ns = if lo > 0 { self.attn_sinks.min(lo) }
# else { 0 }`), mais UNIQUEMENT dans la branche à fenêtre de `forward()`. La mesure d'inertie,
# elle, avait été faite SANS fenêtre — c'est-à-dire dans la seule configuration où l'inertie est
# ATTENDUE. Et l'égalité « 0 ≡ 4 » qui semblait confirmer la mort du drapeau venait d'un garde :
# `if attn_sinks > 0 { mdl.attn_sinks = attn_sinks }` AVALAIT le zéro, donc « 0 » mesurait 4.
# Corrigé (`attn_sinks_impose`, l'idiome de `--ctx`/`--threads`/`--abits`).
#
# Ce que la porte verrouille maintenant, et qui est plus fort que le refus :
#   1. `--attn-sinks 0` AVEC une fenêtre n'est pas neutre : c'est CATASTROPHIQUE
#      (1297,5437 contre 29,0206) — les puits ne sont pas décoratifs, ils DRAINENT l'attention
#      que la fenêtre ne peut pas absorber. Un zéro inexprimable cachait donc un vrai réglage ;
#   2. le drapeau AMÉLIORE : 24 puits → 27,4439 contre 29,0206 au défaut (4) ; à 128 jetons,
#      15,4339 contre 18,1141 (−14,8 %). L'optimum mesuré est 24, pas le défaut ;
#   3. SANS fenêtre il est inerte — attendu, et le moteur le DIT (`INERTE ici`) au lieu de
#      laisser croire qu'il agit ;
#   4. le tableau de bord affiche le nombre EFFECTIF et son origine (défaut/imposé) : c'est
#      précisément la valeur qu'aucune ligne ne montrait, et sans elle deux mesures égales
#      (0 et 4) se lisent comme « drapeau mort ».
ppl10 () { $D "$M" --ppl "$IDS" --limit 64 --ctx "$CTX" --threads 8 "$@" 2>&1 \
    | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+"; }
R0=$(ppl10 --attn-window 32)
R1=$(ppl10 --attn-window 32 --attn-sinks 0)
R2=$(ppl10 --attn-window 32 --attn-sinks 24)
R3=$( $D "$M" --ppl "$IDS" --limit 64 --ctx "$CTX" --threads 8 --attn-sinks 24 2>&1 )
R4=$(ppl10)
printf '  fenêtre 32 : défaut(4) %s · 0 puits %s · 24 puits %s\n' "${R0:-?}" "${R1:-?}" "${R2:-?}"
printf '  sans fenêtre : --attn-sinks 24 %s · rien %s\n' "${R3:-?}" "${R4:-?}"
[ -n "$R0" ] && [ -n "$R1" ] && [ -n "$R2" ] || { echo "  ❌ une des mesures n'a rien rendu"; exit 1; }
python3 -c "
import sys
r0, r1, r2 = float('$R0'), float('$R1'), float('$R2')
if not r1 > 20 * r0: sys.exit('le zéro devrait être CATASTROPHIQUE (drains absents)')
if not r2 < r0:     sys.exit('24 puits devraient battre le défaut de 4')
" || { echo "  ❌ la courbe de dose n'est pas celle qui a été mesurée (cf. commentaire ci-dessus)"; exit 1; }
printf '%s' "$R3" | grep -q "INERTE ici" \
  || { echo "  ❌ sans fenêtre, le moteur doit DIRE que le réglage est inerte"; exit 1; }
V3=$(printf '%s' "$R3" | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+")
[ "$V3" = "$R4" ] || { echo "  ❌ sans fenêtre, le drapeau ne doit RIEN changer ($V3 ≠ $R4)"; exit 1; }
IM=$( $D "$M" --ppl "$IDS" --limit 8 --ctx "$CTX" --threads 8 --attn-window 32 --options-actives 2>&1 \
      | grep -oE "puits d'attention [0-9]+ \(défaut\)" | head -1)
IP=$( $D "$M" --ppl "$IDS" --limit 8 --ctx "$CTX" --threads 8 --attn-window 32 --attn-sinks 0 --options-actives 2>&1 \
      | grep -oE "puits d'attention [0-9]+ \(imposé\)" | head -1)
echo "  tableau de bord : ${IM:-absent} · ${IP:-absent}"
[ -n "$IM" ] && [ -n "$IP" ] || { echo "  ❌ le tableau de bord doit montrer la valeur EFFECTIVE et son origine"; exit 1; }
echo "  ✅ drapeau VIVANT mais conditionnel : 0 casse (${R0} → ${R1}), 24 améliore (${R2}), sans fenêtre il se tait"

rm -rf "$T"
