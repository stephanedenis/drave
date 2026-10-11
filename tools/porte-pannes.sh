#!/bin/bash
# porte-pannes.sh — C11 : la PANNE d'un lien, nommée, et sans résultat partiel.
#
# POURQUOI « best-effort » N'EST PAS « SAUTER LA RÉGION ». Le plan prévoyait de sauter une
# région perdue et d'annoncer l'écart. Mais un modèle dont on saute douze couches ne
# calcule pas une version approchée du même résultat : il calcule un AUTRE modèle, et
# l'« écart » annoncé serait un écart entre deux choses différentes. La seule conduite
# honnête est de S'ARRÊTER en disant tout : quel lien, quel pas, combien d'octets avaient
# passé — et qu'aucun résultat ne sera rendu.
#
# Ce que la porte verrouille :
#   1. une exécution nominale rend son résultat (code 0) — sans quoi rien de ce qui suit
#      ne porterait sur une exécution qui marche ;
#   2. un pair TUÉ EN COURS DE ROUTE arrête le pilote, nomme le lien ET le pas, sort en
#      **code 7** (distinct de 5 = borne de pas et 6 = budget), et **ne rend aucune
#      perplexité** ;
#   3. un pair ABSENT (personne n'écoute) échoue de la même façon, sans pendre.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
. tools/_corpus.sh    # régénère le corpus si /tmp a été effacé (redémarrage)
LIMITE=${LIMITE:-256}
PORT=${PORT:-$((61000 + RANDOM % 400))}
T=$(mktemp -d)
# La topologie est réécrite pour CHAQUE cas avec son propre port : réutiliser le même
# laissait le port en TIME_WAIT, le nœud suivant ne se liait pas, et le cas 2 échouait sur
# « le pilote ne s'est jamais connecté » — un défaut de la PORTE, pas du moteur.
topo() { # $1 = port
cat > "$T/topo.json" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"d","couches":[12,23],"instance":"127.0.0.1:$1"}],
 "liens":[{"de":"local","vers":"d","mode":"f32"}]}
JSON
}
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }

pilote() { # $1 = port
  $D "$M" --ppl-reparti "127.0.0.1:$1" --topologie "$T/topo.json" --ids-file "$IDS" \
     --limit "$LIMITE" --ctx 512 --threads 8 --flux 2>&1
}

echo "=== 1. exécution nominale : le résultat est rendu ==="
P1=$PORT; topo $P1
$D "$M" --flux-serveur "$P1" --ctx 512 --threads 8 > "$T/n.log" 2>&1 & NPID=$!
sleep 2
A=$(pilote $P1); CA=$?
kill $NPID 2>/dev/null; wait $NPID 2>/dev/null
PPL=$(printf '%s\n' "$A" | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
echo "  perplexité ${PPL:-aucune} · code $CA"
[ -n "$PPL" ] && [ "$CA" = 0 ] || { echo "  ❌ l'exécution nominale n'a pas rendu son résultat"; exit 1; }

echo "=== 2. pair TUÉ en cours de route ==="
# Le pilote est lancé EN FOND et tué par le chronomètre : attendre « client connecté » dans
# le journal du nœud était fragile (le pilote calcule sa référence locale ~10 s avant de se
# connecter, et un port en TIME_WAIT faisait échouer le cas pour une raison qui n'était pas
# celle qu'on mesure). Ce qu'on vérifie est le CODE et le MESSAGE, pas l'instant.
P2=$((PORT + 1)); topo $P2
$D "$M" --flux-serveur "$P2" --ctx 512 --threads 8 > "$T/n2.log" 2>&1 & NPID=$!
sleep 2
$D "$M" --ppl-reparti "127.0.0.1:$P2" --topologie "$T/topo.json" --ids-file "$IDS" \
   --limit "$LIMITE" --ctx 512 --threads 8 --flux > "$T/p2.txt" 2>&1 & DPID=$!
sleep 16
kill -9 $NPID 2>/dev/null
wait $DPID; CB=$?
kill $NPID 2>/dev/null; wait $NPID 2>/dev/null
grep -E "pannes\]|deux nœuds" "$T/p2.txt" | sed 's/^/  /'
[ "$CB" = 7 ] || { echo "  ❌ un pair mort devrait sortir en code 7, il sort en $CB"; exit 1; }
grep -qE "PANNE sur le lien local → d|INJOIGNABLE" "$T/p2.txt" \
  || { echo "  ❌ la panne n'est pas nommée"; exit 1; }
grep -qE "deux nœuds +: perplexité" "$T/p2.txt" \
  && { echo "  ❌ une perplexité a été rendue malgré la panne"; exit 1; }
grep -qE "au pas [0-9]+|[0-9]+ octets échangés" "$T/p2.txt" \
  || { echo "  ❌ la panne ne dit pas où elle est survenue"; exit 1; }
echo "  ✅ panne nommée (lien, pas ou octets échangés), code 7, aucune perplexité"

echo "=== 3. pair ABSENT : échec immédiat, sans pendre ==="
P3=$((PORT + 2)); topo $P3
T0=$(date +%s)
$D "$M" --ppl-reparti "127.0.0.1:$P3" --topologie "$T/topo.json" --ids-file "$IDS" \
   --limit 16 --ctx 512 --threads 8 --flux > "$T/p3.txt" 2>&1; CC=$?
DT=$(( $(date +%s) - T0 ))
grep -E "pannes\]|deux nœuds" "$T/p3.txt" | sed 's/^/  /'
echo "  code $CC · $DT s"
[ "$CC" = 7 ] || { echo "  ❌ un pair absent devrait sortir en code 7, il sort en $CC"; exit 1; }
grep -qE "deux nœuds +: perplexité" "$T/p3.txt" \
  && { echo "  ❌ une perplexité a été rendue sans pair"; exit 1; }
[ "$DT" -lt 120 ] || { echo "  ❌ le pilote a pendu ($DT s) au lieu d'échouer"; exit 1; }
echo "  ✅ pair absent : échec annoncé en $DT s (code 7), aucune perplexité"

rm -rf "$T"
