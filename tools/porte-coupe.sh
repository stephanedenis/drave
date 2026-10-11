#!/bin/bash
# porte-coupe.sh — OÙ COUPER ? Le point de coupe est-il neutre, et à quel prix ?
#
# LA QUESTION PRATIQUE. Le découpage en régions (C1) et le pont (C9) avaient chacun
# été mesurés à UN endroit : 12 couches locales, 12 distantes. Rien ne disait que
# 12/12 soit le bon endroit. Cette porte répond à deux questions distinctes, et les
# sépare parce qu'elles n'ont pas la même réponse :
#
#   1. **le point de coupe change-t-il le RÉSULTAT ?** Avec un lien SANS PERTE (dense
#      f32), la réponse mesurée est NON : huit points de coupe (4, 6, 8, 10, 12, 15,
#      18, 20 couches locales sur 24) donnent tous 113,0068. C'est l'invariant de C1,
#      vérifié sur huit coupes et non sur une seule ;
#   2. **le point de coupe change-t-il ce que le lien COÛTE ?** Avec un lien encodé
#      (listes par blocs), la réponse est OUI, et fortement : les mêmes coupes donnent
#      de 108,87 à 118,53 de perplexité — soit 9 % d'écart — parce que l'erreur de
#      quantification dépend de l'état échangé, qui dépend de la profondeur. Et le coût
#      d'un pont de 448 fibres va de +0,52 % (coupe 18/6) à +17,09 % (coupe 15/9).
#
# Une porte qui ne saurait pas échouer ne vérifierait rien : le cas 2 est là pour
# montrer que le cas 1 n'est pas vrai « parce que rien ne change jamais ».
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
. tools/_corpus.sh    # régénère le corpus si /tmp a été effacé (redémarrage)
LIMITE=${LIMITE:-48}
PORT=${PORT:-$((59000 + RANDOM % 400))}
T=$(mktemp -d)
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }

# `$2` est la largeur du pont, et elle est donnée AUX DEUX PROCESSUS : un pont
# limité d'un seul côté n'est pas un pont, et le laisser asymétrique ici faisait
# mesurer +4,92 % là où le pont symétrique coûte +2,81 % (attrapé en comparant avec
# `porte-pont.sh`, qui, lui, passait bien le drapeau au nœud).
mesure() { # $1 = N local, $2 = pont, $3.. = drapeaux du pilote
  local N=$1; local PONT=$2; shift 2
  cat > "$T/topo.json" <<JSON
{"regions":[
  {"id":"local","couches":[0,$((N - 1))],"instance":"local"},
  {"id":"d","couches":[$N,23],"instance":"127.0.0.1:$PORT"}],
 "liens":[{"de":"local","vers":"d","mode":"f32"}]}
JSON
  $D "$M" --flux-serveur "$PORT" --ctx 256 --threads 8 --pont-k "$PONT" > "$T/n.log" 2>&1 &
  local NPID=$!
  sleep 2
  local R
  R=$($D "$M" --ppl-reparti "127.0.0.1:$PORT" --topologie "$T/topo.json" --ids-file "$IDS" \
      --limit "$LIMITE" --ctx 256 --threads 8 --pont-k "$PONT" "$@" 2>&1 \
      | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
  kill $NPID 2>/dev/null; wait $NPID 2>/dev/null
  printf '%s' "$R"
}

echo "=== 1. lien SANS PERTE : le point de coupe ne change RIEN ==="
: > "$T/sansperte.txt"
for N in 4 6 8 10 12 15 18 20; do
  P=$(mesure "$N" 0 --flux)
  [ -n "$P" ] || { echo "  ❌ aucune perplexité à la coupe $N/24"; exit 1; }
  echo "$N $P" >> "$T/sansperte.txt"
  printf '  coupe %2d/%-2d : %s\n' "$N" "$((24 - N))" "$P"
done
python3 - "$T/sansperte.txt" <<'PY' || exit 1
import sys
pts = [(int(l.split()[0]), l.split()[1]) for l in open(sys.argv[1])]
valeurs = {p[1] for p in pts}
if len(valeurs) != 1:
    sys.exit(f"  ❌ le point de coupe change le résultat : {pts}")
print(f"  ✅ {len(pts)} points de coupe, UNE seule perplexité ({pts[0][1]}) : "
      "le découpage est numériquement neutre quand le lien est sans perte")
PY

echo "=== 2. lien ENCODÉ : le point de coupe change beaucoup (témoin) ==="
: > "$T/encode.txt"
for N in 4 6 12 18; do
  P=$(mesure "$N" 0 --flux-blocs)
  [ -n "$P" ] || { echo "  ❌ aucune perplexité à la coupe $N/24"; exit 1; }
  echo "$N $P" >> "$T/encode.txt"
  printf '  coupe %2d/%-2d : %s\n' "$N" "$((24 - N))" "$P"
done
python3 - "$T/encode.txt" <<'PY' || exit 1
import sys
pts = [(int(l.split()[0]), float(l.split()[1])) for l in open(sys.argv[1])]
ecart = (max(p[1] for p in pts) - min(p[1] for p in pts)) / min(p[1] for p in pts)
if ecart < 0.02:
    sys.exit(f"  ❌ avec un lien encodé, le point de coupe devrait compter : écart {ecart:.2%}")
print(f"  ✅ avec un lien encodé, les mêmes coupes s'écartent de {100*ecart:.1f} % — "
      "c'est l'ENCODAGE qui rend le point de coupe significatif")
PY

echo "=== 3. le coût du pont dépend AUSSI du point de coupe ==="
: > "$T/pont.txt"
for N in 12 15 18; do
  P0=$(mesure "$N" 0 --flux-blocs)
  P1=$(mesure "$N" 448 --flux-blocs)
  [ -n "$P0" ] && [ -n "$P1" ] || { echo "  ❌ mesure manquante à la coupe $N"; exit 1; }
  echo "$N $P0 $P1" >> "$T/pont.txt"
  python3 -c "
a, b = float('$P0'), float('$P1')
print('  coupe %2d/%-2d : pont 448 fibres → %+.2f %%' % ($N, 24-$N, 100.0*(b-a)/a))"
done
python3 - "$T/pont.txt" <<'PY' || exit 1
import sys
pts = [(int(l.split()[0]), float(l.split()[1]), float(l.split()[2])) for l in open(sys.argv[1])]
couts = {n: 100.0 * (p1 - p0) / p0 for n, p0, p1 in pts}
meilleur = min(couts, key=couts.get)
pire = max(couts, key=couts.get)
if couts[pire] < 3.0 * max(couts[meilleur], 0.1):
    sys.exit(f"  ❌ le coût du pont ne dépend pas assez du point de coupe : {couts}")
print(f"  ✅ le coût du pont va de {couts[meilleur]:+.2f} % (coupe {meilleur}/24) à "
      f"{couts[pire]:+.2f} % (coupe {pire}/24) — il y a un bon endroit pour couper")
PY

rm -rf "$T"
