#!/bin/bash
# porte-horloge.sh — la porte du premier pas de C4 : compteur de pas et borne.
#
# Ce qui est vérifié, et pourquoi ces trois cas :
#   1. sans borne   : référence — la région locale sert N pas, le nœud aussi ;
#   2. borne = N    : MÊME résultat (la borne n'est pas atteinte) et pas annoncés ;
#   3. borne < N    : l'exécution S'ARRÊTE et le DIT, sans rendre de résultat
#      partiel — une perplexité calculée sur la moitié des jetons aurait l'air d'un
#      résultat complet, et c'est exactement ce que le dépôt refuse.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
LIMITE=${LIMITE:-64}
PORT=${PORT:-$((54000 + RANDOM % 800))}
T=$(mktemp -d)
cat > "$T/topo.json" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"d","couches":[12,23],"instance":"127.0.0.1:$PORT"}],
 "liens":[{"de":"local","vers":"d","mode":"f32"}]}
JSON
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }
essai() { # essai <options...>
    $D "$M" --flux-serveur "$PORT" --ctx 256 --threads 8 "$@" > "$T/n.log" 2>&1 & local N=$!
    sleep 2
    local S
    S=$($D "$M" --ppl-reparti "127.0.0.1:$PORT" --topologie "$T/topo.json" --ids-file "$IDS" \
         --limit "$LIMITE" --ctx 256 --threads 8 --flux "$@" 2>&1); local C=$?
    kill $N 2>/dev/null; wait $N 2>/dev/null
    printf '  %s\n' "$(printf '%s' "$S" | grep -E 'horloge|deux nœuds|borne' | tr '\n' ' ')"
    printf '  nœud : %s\n' "$(grep -E 'horloge' "$T/n.log" | tail -1)"
    PPL=$(printf '%s' "$S" | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
    CODE=$C
}
echo "=== 1. sans borne ==="; essai; A=$PPL; CA=$CODE
echo "=== 2. borne = $LIMITE (non atteinte) ==="; essai --pas-max "$LIMITE"; B=$PPL; CB=$CODE
echo "=== 3. borne = 32 (atteinte) ==="; essai --pas-max 32
echo "=== verdict ==="
[ "$A" = "$B" ] && [ "$CA" = "0" ] && [ "$CB" = "0" ] \
  && echo "  ✅ borne non atteinte : même résultat ($A), code 0" \
  || { echo "  ❌ $A/$CA vs $B/$CB"; exit 1; }
[ "$CODE" = "5" ] && [ -z "$PPL" ] \
  && echo "  ✅ borne atteinte : arrêt EXPLICITE (code 5) et AUCUNE perplexité rendue" \
  || { echo "  ❌ borne atteinte mais code $CODE et perplexité « $PPL »"; exit 1; }
rm -rf "$T"
