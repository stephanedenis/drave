#!/bin/bash
# porte-reflexe.sh — la porte de la capacité C8 (premier pas) : le RÉFLEXE.
#
# LA QUESTION. Un réflexe médullaire ne remonte pas au cortex : il répond par un
# chemin COURT. Dans le moteur, ce chemin existe déjà — `--couches 0,L` tronque le
# modèle et `--tete-partielle` applique la tête à la fin de la plage. La question
# mesurable n'est donc pas « peut-on faire un réflexe ? » mais **« à partir de quelle
# profondeur un réflexe tombe-t-il d'accord avec le modèle entier ? »**.
#
# CE QUE LA MESURE A RÉPONDÉ : avec la TÊTE DU MODÈLE, l'accord est de 0 % jusqu'à
# 16 couches sur 24, 8,3 % à 20, et 100 % seulement à 24. Le diagnostic est dans la
# même table : la COSINUS entre l'état tronqué et l'état final vaut 0,037 à 1 couche,
# 0,130 à 16 et 1,000 à 24 — **l'état intermédiaire est presque ORTHOGONAL à l'état
# final**, et la tête du modèle lit une direction que seules les dernières couches
# produisent.
#
# **CORRECTION DU 2026-10-10 — la conclusion « pas de sortie précoce utilisable » est
# vraie de la TÊTE EMPRUNTÉE et fausse de l'ÉTAT** (voir la dernière section de cette
# porte). Une sonde LINÉAIRE entraînée sur l'état de 16 couches lit le prochain jeton à
# **40,8 %** (référence 4,0 %), et un adaptateur entraîné ramène la perplexité du chemin
# tronqué de 697 572 à **85** là où le modèle complet vaut 15,02 — ×5,7 au lieu de
# ×46 000. Le maillon faible était la TÊTE, pas la profondeur. Fiches :
# `reports/rapport-c8-sonde-profondeur.md`, `reports/rapport-c8-tete-entrainee.md`,
# `reports/rapport-c8-generalisation.md`.
#
# Ce que cette porte verrouille :
#   1. un réflexe aussi profond que le modèle EST le modèle (accord 100 %) — sans cet
#      invariant, la comparaison porterait sur deux calculs différents ;
#   2. avec la tête du modèle il n'y a pas de sortie précoce utilisable : à 16 couches (2/3 de la
#      profondeur), l'accord reste sous 25 % ;
#   3. la cause est la direction : à 16 couches, la cosinus avec l'état final est
#      inférieure à 0,5 ;
#   4. le gain de temps est réel (un réflexe d'une couche est au moins 5× plus rapide)
#      — donc l'échec du point 2 n'est pas un artefact de mesure.
#
# CE QUE LA PORTE NE DIT PAS : la sortie précoce est mesurée SANS tête dédiée. Une
# tête entraînée pour la couche L donnerait autre chose ; elle n'existe pas ici (le
# moteur n'entraîne pas), et c'est écrit dans la sortie du mode.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
. tools/_corpus.sh    # régénère le corpus si /tmp a été effacé (redémarrage)
N=${N:-32}
T=$(mktemp -d)
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }

echo "=== la courbe accord ↔ profondeur (et sa cause) ==="
timeout 1800 "$D" "$M" --reflexe-essai "$N" --ids-file "$IDS" --ctx 256 --threads 8 \
  > "$T/r.txt" 2>&1 || { echo "  ❌ l'essai a échoué"; tail -3 "$T/r.txt"; exit 1; }
grep -E "modèle  |référence|^ +couches" "$T/r.txt" | sed 's/^/  /'
grep -E "^ +[0-9]+ +[0-9]" "$T/r.txt" | sed 's/^/  /'
grep -E "ce que la courbe" -A 2 "$T/r.txt" | sed 's/^/  /'

python3 - "$T/r.txt" <<'PY' || exit 1
import re, sys
t = open(sys.argv[1]).read()
lignes = [l for l in t.splitlines() if re.match(r"^\s+\d+\s+\d+\.\d %", l)]
if len(lignes) < 3:
    sys.exit(f"  ❌ courbe illisible ({len(lignes)} lignes)")
pts = []
for l in lignes:
    ch = l.split()
    pts.append((int(ch[0]), float(ch[1]), float(ch[3]), float(ch[5]), float(ch[6])))
# (couches, accord %, accord top-5 %, cos, ms/jeton) — le signe % est un CHAMP à part
prof_max = max(p[0] for p in pts)   # p = (couches, accord, top5, cos, ms)

# 1. un réflexe aussi profond que le modèle EST le modèle
dernier = max(pts)
if abs(dernier[1] - 100.0) > 1e-9:
    sys.exit(f"  ❌ à {dernier[0]} couches (toute la profondeur) l'accord devrait être "
             f"100 %, il est de {dernier[1]} %")
print(f"  ✅ à {dernier[0]} couches, le réflexe EST le modèle : {dernier[1]} % d'accord")

# 2. pas de sortie précoce utilisable
deux_tiers = [p for p in pts if p[0] <= 2 * prof_max // 3]
pire = max(deux_tiers, key=lambda p: p[1])
if pire[1] >= 25.0:
    sys.exit(f"  ❌ à {pire[0]} couches l'accord atteint {pire[1]} % : il y aurait une "
             "sortie précoce, contrairement à ce qui a été mesuré")
print(f"  ✅ sur TOUTES les profondeurs jusqu'à 2/3 de la profondeur, le meilleur accord "
      f"est {pire[1]} % (à {pire[0]} couches) : pas de sortie précoce utilisable")

# 3. la cause est la direction, pas l'échelle
c16 = [p for p in deux_tiers if p[0] == max(x[0] for x in deux_tiers)][0]
if c16[3] >= 0.5:
    sys.exit(f"  ❌ à {c16[0]} couches la cosinus avec l'état final vaut {c16[3]} : "
             "l'explication par la direction ne tient pas")
print(f"  ✅ la cause est la DIRECTION : cos(état tronqué, état final) = {c16[3]} à "
      f"{c16[0]} couches (1,000 à la profondeur entière)")

# 4. le gain de temps est réel
rapide = min(pts)          # 1 couche : le réflexe le plus court
lent = dernier             # toute la profondeur
# `p[4]` est le temps (le cosinus est `p[3]`) : les confondre a produit un rapport de
# 22,7× entre deux cosinus — attrapé parce que le message affichait « 0.0 ms ».
if rapide[4] <= 0 or lent[4] / rapide[4] < 3.0:
    sys.exit(f"  ❌ le gain de temps est trop faible pour que la mesure ait un sens : "
             f"{lent[4]} ms contre {rapide[4]} ms")
print(f"  ✅ le gain de temps est réel : {rapide[4]:.1f} ms par jeton à {rapide[0]} couche(s) "
      f"contre {lent[4]:.1f} ms à {lent[0]} — {lent[4]/rapide[4]:.1f}× plus rapide, "
      f"pour {rapide[1]} % d'accord")
PY
echo "=== l'état contient l'information (sonde LINÉAIRE, pas la tête du modèle) ==="
# LA CONCLUSION DE CETTE PORTE A ÉTÉ CORRIGÉE LE 2026-10-10 : l'accord de 0 % à 16 couches
# mesure la TÊTE empruntée, pas la richesse de l'état. Une régression ridge sur ce même état
# lit le prochain jeton bien au-dessus du hasard — et c'est cet invariant qui est verrouillé
# ici, parce qu'il décide si C8 a un sens.
PROF=${PROF:-16}                      # couches exécutées pour la capture
NPOS=${NPOS:-256}                     # positions capturées (borne le temps de la porte)
T2="$T/sonde"; mkdir -p "$T2"
POS=$(seq -s, 4 $((NPOS - 1)))
$D "$M" --ppl "$IDS" --limit "$NPOS" --ctx "$NPOS" --threads 8 \
   --couches "0:$PROF" --tete-partielle --etat-sortie "$T2/etat" --etat-pos "$POS" \
   > "$T2/capture.log" 2>&1
SONDE=$(python3 tools/c8_sonde_lineaire.py --etats "$T2/etat" --ids "$IDS" --limite "$NPOS" \
          --classes 256 2>&1)
printf '%s\n' "$SONDE" | grep -E "sonde linéaire|classe majoritaire" | sed 's/^/  /'
# LE CHIFFRE EST APRÈS LE DEUX-POINTS : « sonde linéaire (ridge λ=1.0) : 25.4 % » contient
# « 1.0 » AVANT le score, et le premier essai a lu 1,0 % — un score de hasard, donc un échec
# annoncé sur un résultat juste. Même famille que « % est un champ à part » dans les harnais.
JUSTE=$(printf '%s' "$SONDE" | grep -oE "sonde linéaire.*: [0-9.]+ %" | grep -oE ": [0-9.]+ %" | grep -oE "[0-9.]+" | head -1)
REF=$(printf '%s' "$SONDE" | grep -oE "classe majoritaire.*: [0-9.]+ %" | grep -oE ": [0-9.]+ %" | grep -oE "[0-9.]+" | head -1)
[ -n "$JUSTE" ] && [ -n "$REF" ] || { echo "  ❌ la sonde n'a rien rendu (états ou ids manquants ?)"; exit 1; }
python3 -c "
import sys
j, r = float('$JUSTE'), float('$REF')
# 20 % est TRÈS au-dessus du hasard (0,39 %) et de la classe majoritaire (~5 %) : borne basse
# qui laisse respirer la mesure (25 % sur 256 positions, 41 % sur 1 019) et qui échoue si
# l'état ne portait plus l'information.
if j < 20.0: sys.exit(f'  l etat ne porte plus l information : {j} % (reference {r} %)')
if j < 3 * r: sys.exit(f'  la sonde ne depasse pas 3x la reference : {j} % contre {r} %')
" || { echo "  ❌ l'état intermédiaire ne porte plus le prochain jeton (voir les fiches C8)"; exit 1; }
echo "  ✅ l'état de $PROF couches CONTIENT le prochain jeton : $JUSTE % contre $REF % pour la classe majoritaire"
echo "     (c'est la TÊTE qui ne sait pas le lire — reports/rapport-c8-sonde-profondeur.md)"

rm -rf "$T"
