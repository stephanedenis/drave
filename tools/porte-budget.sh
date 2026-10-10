#!/bin/bash
# porte-budget.sh — C10 : le BUDGET D'OCTETS par lien, déclaré et vérifié.
#
# POURQUOI UN BUDGET SE VÉRIFIE AU PREMIER FLUX, ET PAS AU DÉMARRAGE. La taille d'un flux
# n'est pas une propriété du mode : elle dépend de l'ACTIVITÉ réelle (listes par blocs :
# 1 951 octets à 97,7 % d'activité, 1 096 à 50 % — mesuré). Un contrôle au démarrage ne
# pourrait donc comparer qu'à une valeur nominale inventée. Ici, le budget se compare à ce
# qui PASSE, et le dépassement ARRÊTE l'exécution en le disant, au pas où il survient.
#
# Ce que la porte verrouille :
#   1. un budget GÉNÉREUX ne change RIEN au résultat (le lien déclaré est celui qui passe) ;
#   2. un budget INSUFFISANT arrête l'exécution, nomme le lien, le dépassement et le pas,
#      sort en code 6, et **ne rend aucune perplexité** — jamais un résultat partiel ;
#   3. l'absence de budget ne change rien (le défaut) : c'est la porte de non-régression.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
LIMITE=${LIMITE:-48}
PORT=${PORT:-$((60000 + RANDOM % 400))}
T=$(mktemp -d)
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }

topo() { # $1 = budget (vide = aucun)
  local b=""
  [ -n "$1" ] && b=", \"budget_octets\": $1"
  cat > "$T/topo.json" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"d","couches":[12,23],"instance":"127.0.0.1:$PORT"}],
 "liens":[{"de":"local","vers":"d","mode":"blocs"$b}]}
JSON
}
nœud() { $D "$M" --flux-serveur "$PORT" --ctx 256 --threads 8 > "$T/n.log" 2>&1 & echo $!; }
pilote() {
  $D "$M" --ppl-reparti "127.0.0.1:$PORT" --topologie "$T/topo.json" --ids-file "$IDS" \
     --limit "$LIMITE" --ctx 256 --threads 8 --flux-blocs 2>&1
}

echo "=== 1. sans budget déclaré (défaut) ==="
topo ""
N=$(nœud); sleep 2
A=$(pilote); CA=$?
kill $N 2>/dev/null; wait $N 2>/dev/null
PPL=$(printf '%s\n' "$A" | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
OCT=$(printf '%s\n' "$A" | grep -oE "[0-9]+ octets par flux" | head -1 | grep -oE "^[0-9]+")
echo "  perplexité $PPL · $OCT octets par flux · code $CA"
[ -n "$PPL" ] || { echo "  ❌ aucune perplexité"; exit 1; }

echo "=== 2. budget GÉNÉREUX : le résultat ne doit pas changer ==="
topo $((OCT + 500))
N=$(nœud); sleep 2
B=$(pilote); CB=$?
kill $N 2>/dev/null; wait $N 2>/dev/null
PPL2=$(printf '%s\n' "$B" | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
printf '%s\n' "$B" | grep -E "budget\]" | sed 's/^/  /'
echo "  perplexité $PPL2 · code $CB"
[ "$PPL" = "$PPL2" ] && [ "$CB" = 0 ] \
  || { echo "  ❌ un budget généreux a changé le résultat ou le code"; exit 1; }
echo "  ✅ budget généreux : résultat identique ($PPL2)"

echo "=== 3. budget INSUFFISANT : arrêt explicite, code 6, AUCUNE perplexité ==="
topo $((OCT / 2))
N=$(nœud); sleep 2
C=$(pilote); CC=$?
kill $N 2>/dev/null; wait $N 2>/dev/null
printf '%s\n' "$C" | grep -E "budget\]|perplexité" | sed 's/^/  /'
[ "$CC" = 6 ] || { echo "  ❌ le dépassement devrait sortir en code 6, il sort en $CC"; exit 1; }
printf '%s' "$C" | grep -q "DÉPASSEMENT" \
  || { echo "  ❌ le dépassement n'est pas nommé"; exit 1; }
printf '%s' "$C" | grep -qE "deux nœuds +: perplexité" \
  && { echo "  ❌ une perplexité a été rendue malgré le dépassement — un résultat partiel"; exit 1; }
echo "  ✅ dépassement annoncé (lien, octets, budget, pas), code 6, aucune perplexité rendue"

rm -rf "$T"
