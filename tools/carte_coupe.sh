#!/bin/bash
# carte_coupe.sh — OÙ COUPER le modèle ? Le coût du pont selon le point de coupe.
#
# POURQUOI CETTE MESURE. Le découpage en régions (C1) et le pont (C9) ont été mesurés
# séparément, chacun à un endroit : 12 couches locales, 12 distantes. Mais rien ne dit
# que 12/12 soit le bon endroit — et la mesure de C8 (l'état intermédiaire est presque
# orthogonal à l'état final, cos 0,145 à 16 couches sur 24) suggère que la nature de
# l'état dépend FORTEMENT de la profondeur. La question pratique est donc : à quel
# point de coupe le lien coûte-t-il le moins cher, à qualité égale ?
#
# CE QU'ELLE MESURE, POUR CHAQUE COUPE (N local, 24−N distant) :
#   · la perplexité SANS pont (référence du découpage — elle ne dépend pas que du
#     modèle : chaque coupe a la sienne, et c'est déjà une information) ;
#   · la perplexité avec un pont de 448 fibres (la moitié) et de 224 ;
#   · donc le COÛT du pont à cet endroit, en pourcentage.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
LIMITE=${LIMITE:-48}
PORT=${PORT:-$((59000 + RANDOM % 400))}
T=$(mktemp -d)
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }

mesure() { # $1 = N local, $2 = pont (0 = aucun)
  local N=$1 PONT=$2
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
      --limit "$LIMITE" --ctx 256 --threads 8 --flux-blocs --pont-k "$PONT" 2>&1)
  kill $NPID 2>/dev/null; wait $NPID 2>/dev/null
  printf '%s\n' "$R" | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$"
}

echo "  coupe   PPL sans pont   pont 448   coût 448   pont 224   coût 224   octets 448"
for N in 4 6 8 10 12 15 18 20; do
  REF=$(mesure "$N" 0)
  P448=$(mesure "$N" 448)
  P224=$(mesure "$N" 224)
  [ -n "$REF" ] && [ -n "$P448" ] && [ -n "$P224" ] || { echo "  ❌ mesure manquante à N=$N"; continue; }
  python3 -c "
ref, a, b = float('$REF'), float('$P448'), float('$P224')
print('  %2d/%-2d  %12s  %9s  %+8.2f %%  %9s  %+8.2f %%' % ($N, 24-$N, '$REF', '$P448',
      100.0*(a-ref)/ref, '$P224', 100.0*(b-ref)/ref))"
done
echo
echo "  lecture : « coût » est la dégradation apportée par le pont à ce point de coupe."
echo "  Un coût faible signifie que l'état échangé à cette profondeur est REDONDANT :"
echo "  on peut en jeter la moitié. Un coût élevé signifie que tout y porte."
rm -rf "$T"
