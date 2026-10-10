#!/bin/bash
# porte-registre.sh — C11 (découverte) : le registre des régions.
#
# POURQUOI. Une topologie qui écrit « 127.0.0.1:50001 » décrit UN déploiement ; la même
# topologie sur trois machines en demanderait trois. Le plan (§3.2, ligne « découverte »)
# prévoit un registre statique, puis dynamique. Voici le statique.
#
# Ce que la porte verrouille :
#   1. une topologie qui NOMME ses régions + un registre ⇒ le MÊME résultat qu'avec des
#      adresses écrites en dur (le registre ne change pas le calcul, seulement la façon de
#      le désigner) ;
#   2. une région ABSENTE du registre est REFUSÉE en la nommant — un repli silencieux sur
#      localhost ferait parler le moteur à la mauvaise machine ;
#   3. une instance qui est DÉJÀ une adresse (elle contient « : ») n'est pas touchée : les
#      topologies existantes continuent de marcher au caractère près (cas 1 et 3 le
#      montrent ensemble).
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
LIMITE=${LIMITE:-48}
PORT=${PORT:-$((64000 + RANDOM % 400))}
T=$(mktemp -d)
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }

# La topologie NOMME la région distante : « d », pas une adresse.
cat > "$T/topo.json" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"d","couches":[12,23],"instance":"d"}],
 "liens":[{"de":"local","vers":"d","mode":"f32"}]}
JSON
cat > "$T/registre.txt" <<REG
# region  hote:port
local     127.0.0.1
d         127.0.0.1:$PORT
REG

echo "=== 1. topologie NOMMÉE + registre ==="
$D "$M" --flux-serveur "$PORT" --ctx 256 --threads 8 > "$T/n.log" 2>&1 & N=$!
sleep 2
A=$($D "$M" --ppl-reparti "127.0.0.1:$PORT" --topologie "$T/topo.json" --registre "$T/registre.txt" \
    --ids-file "$IDS" --limit "$LIMITE" --ctx 256 --threads 8 --flux 2>&1); CA=$?
kill $N 2>/dev/null; wait $N 2>/dev/null
PPL=$(printf '%s\n' "$A" | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
printf '%s\n' "$A" | grep -E "topologie\]" | head -2 | sed 's/^/  /'
echo "  perplexité ${PPL:-aucune} · code $CA"
[ -n "$PPL" ] || { echo "  ❌ aucune perplexité par le registre"; exit 1; }

echo "=== 2. la MÊME topologie, adresse en dur : même résultat ==="
cat > "$T/topo2.json" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"d","couches":[12,23],"instance":"127.0.0.1:$PORT"}],
 "liens":[{"de":"local","vers":"d","mode":"f32"}]}
JSON
$D "$M" --flux-serveur "$PORT" --ctx 256 --threads 8 > "$T/n2.log" 2>&1 & N=$!
sleep 2
B=$($D "$M" --ppl-reparti "127.0.0.1:$PORT" --topologie "$T/topo2.json" --ids-file "$IDS" \
    --limit "$LIMITE" --ctx 256 --threads 8 --flux 2>&1); CB=$?
kill $N 2>/dev/null; wait $N 2>/dev/null
PPL2=$(printf '%s\n' "$B" | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
echo "  perplexité ${PPL2:-aucune} · code $CB"
[ "$PPL" = "$PPL2" ] && [ "$CB" = 0 ] \
  || { echo "  ❌ le registre change le résultat ($PPL contre $PPL2) — il ne devrait changer que la désignation"; exit 1; }
echo "  ✅ registre et adresse en dur donnent le MÊME résultat ($PPL)"

echo "=== 3. région ABSENTE du registre : refus en la nommant ==="
cat > "$T/registre2.txt" <<REG
# seule « local » est déclarée
local     127.0.0.1
REG
C=$($D "$M" --ppl-reparti "127.0.0.1:$PORT" --topologie "$T/topo.json" --registre "$T/registre2.txt" \
    --ids-file "$IDS" --limit 8 --ctx 256 --threads 8 --flux 2>&1); CC=$?
printf '%s\n' "$C" | grep -E "registre\]" | sed 's/^/  /'
[ "$CC" = 2 ] || { echo "  ❌ une région absente devrait être refusée (code 2), code $CC"; exit 1; }
printf '%s' "$C" | grep -q "ABSENTE" || { echo "  ❌ le refus ne nomme pas l'absence"; exit 1; }
printf '%s' "$C" | grep -qE "deux nœuds +: perplexité" \
  && { echo "  ❌ une perplexité a été rendue sans registre complet"; exit 1; }
echo "  ✅ région absente : refusée en la nommant (code 2), rien n'est calculé"

rm -rf "$T"
