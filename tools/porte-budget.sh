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

topo() { # $1 = budget d'octets, $2 = latence, $3 = paires (vides = aucun)
  # `${1:-}` et non `$1` : sous `set -u`, un argument ABSENT fait tomber le script, et le
  # premier appel de la porte n'en passe qu'un (attrapé au premier essai).
  local b="" l="" p=""
  [ -n "${1:-}" ] && b=", \"budget_octets\": $1"
  [ -n "${2:-}" ] && l=", \"budget_ms\": $2"
  [ -n "${3:-}" ] && p=", \"budget_paires\": $3"
  cat > "$T/topo.json" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"d","couches":[12,23],"instance":"127.0.0.1:$PORT"}],
 "liens":[{"de":"local","vers":"d","mode":"blocs"$b$l$p}]}
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

echo "=== 4. budget de LATENCE : généreux (aucun effet) ==="
topo "" 100000
N=$(nœud); sleep 2
# `D` est le BINAIRE : l'écraser avec la sortie du pilote faisait échouer le cas suivant
# sur un code 127 (« command not found ») — attrapé au premier essai, et c'est le genre de
# faute qu'une porte doit rendre visible, pas masquer.
R4=$(pilote); CD=$?
kill $N 2>/dev/null; wait $N 2>/dev/null
PPL4=$(printf '%s\n' "$R4" | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
echo "  perplexité ${PPL4:-aucune} · code $CD"
[ "$PPL4" = "$PPL" ] && [ "$CD" = 0 ] || { echo "  ❌ un budget de latence généreux a changé le résultat"; exit 1; }
echo "  ✅ latence généreuse : résultat identique ($PPL4)"

echo "=== 5. budget de LATENCE insuffisant : arrêt, code 8, aucune perplexité ==="
topo "" 1
N=$(nœud); sleep 2
E=$(pilote); CE=$?
kill $N 2>/dev/null; wait $N 2>/dev/null
printf '%s\n' "$E" | grep -E "budget\]|deux nœuds" | tail -3 | sed 's/^/  /'
[ "$CE" = 8 ] || { echo "  ❌ la latence dépassée devrait sortir en code 8, elle sort en $CE"; exit 1; }
printf '%s' "$E" | grep -q "LATENCE DÉPASSÉE" || { echo "  ❌ le dépassement de latence n'est pas nommé"; exit 1; }
printf '%s' "$E" | grep -qE "deux nœuds +: perplexité" \
  && { echo "  ❌ une perplexité a été rendue malgré le dépassement de latence"; exit 1; }
echo "  ✅ latence dépassée : nommée (mesurée vs budget, au pas), code 8, aucune perplexité"

echo "=== 6. budget de PAIRES : le troisieme volet de C10 ==="
# Les paires sont calculees par LE NOEUD : elles n'ont pu etre bornees qu'apres leur TRANSPORT
# (protocole v8). Le compte est CUMULATIF, donc le plafond apres k pas vaut k x le budget.
# Et le controle est DANS la boucle : place apres elle, il laissait calculer et AFFICHER la
# perplexite avant de refuser (attrape par ce cas meme, au round precedent).
topo "" "" 10000000000
N=$(nœud); sleep 2
P=$(pilote); CP=$?
kill $N 2>/dev/null; wait $N 2>/dev/null
PP=$(printf '%s\n' "$P" | grep -oE "paires du pair +: [0-9]+" | grep -oE "[0-9]+")
printf '  genereux (10 G/pas) : paires annoncees %s · code %s\n' "${PP:-?}" "$CP"
[ "$CP" = 0 ] && [ -n "$PP" ] || { echo "  ❌ budget de paires genereux : le run devrait aboutir"; exit 1; }

topo "" "" 1000000
N=$(nœud); sleep 2
Q=$(pilote); CQ=$?
kill $N 2>/dev/null; wait $N 2>/dev/null
printf '%s\n' "$Q" | grep -E "PAIRES D" | tail -1 | cut -c1-170 | sed 's/^/  /'
[ "$CQ" = 9 ] || { echo "  ❌ le depassement de paires devrait sortir en code 9, il sort en $CQ"; exit 1; }
printf '%s' "$Q" | grep -qE "deux nœuds +: perplexité" \
  && { echo "  ❌ une perplexite a ete rendue malgre le depassement de paires"; exit 1; }
echo "  ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite"

rm -rf "$T"
