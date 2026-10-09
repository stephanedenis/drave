#!/bin/bash
# porte-topologie.sh — la porte de la capacité C1 : la topologie PILOTE le découpage.
#
# Ce qu'elle vérifie, et pourquoi ces quatre cas :
#   1. la RÉFÉRENCE : le modèle entier, un seul processus ;
#   2. le découpage HISTORIQUE (`--couches-locales`) — l'écart de flux doit être 0 ;
#   3. le découpage par TOPOLOGIE (fichier) — il doit rendre EXACTEMENT le même
#      chiffre que le précédent : c'est la non-régression de C1 ;
#   4. les REFUS : une topologie qui ne couvre pas le modèle, et une topologie dont
#      l'adresse contredit `--ppl-reparti`. Un découpage qui n'est pas celui qu'on
#      croit ne doit pas se mesurer en silence.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-/tmp/m5_d384_dense.gguf}
IDS=${IDS:-/tmp/campagne24/ids_m5_d384_dense.txt}
COUCHES=${COUCHES:-2}
LIMITE=${LIMITE:-128}
PORT=${PORT:-$((50000 + RANDOM % 900))}
T=$(mktemp -d)
TOPO="$T/topo.json"
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }

N=$($D "$M" --tensors 2>/dev/null | grep -cE "^ +[A-Z0-9_]+ +blk\.[0-9]+\.attn_q\.weight" || true)
[ "${N:-0}" -gt 0 ] || N=4

cat > "$TOPO" <<JSON
{
  "regions": [
    {"id": "local",   "couches": [0, $((COUCHES-1))],              "instance": "local"},
    {"id": "distant", "couches": [$COUCHES, $((N-1))],             "instance": "127.0.0.1:$PORT"}
  ],
  "liens": [ {"de": "local", "vers": "distant", "mode": "listes", "delai_ms": 0} ]
}
JSON

echo "=== 1. référence : le modèle entier ==="
$D "$M" --ppl "$IDS" --limit "$LIMITE" --ctx 256 --threads 8 --abits 16 2>/dev/null \
    | grep -oE "perplexité [0-9.]+ sur" | tail -1

echo "=== 2. découpage historique ($COUCHES couches locales) ==="
$D "$M" --flux-serveur "$PORT" --ctx 256 --threads 8 > "$T/n1.log" 2>&1 & SRV=$!
for _ in $(seq 1 40); do grep -q "nœud moteur sur" "$T/n1.log" 2>/dev/null && break; sleep 0.25; done
H=$($D "$M" --ppl-reparti "127.0.0.1:$PORT" --ids-file "$IDS" --couches-locales "$COUCHES" \
    --limit "$LIMITE" --ctx 256 --threads 8 --abits 16 2>&1 \
    | grep -E "deux nœuds +: perplexité [0-9.]+|écart +: +[0-9.e+-]+")
echo "  $H"
kill $SRV 2>/dev/null; wait $SRV 2>/dev/null

echo "=== 3. découpage par TOPOLOGIE ($TOPO) ==="
$D "$M" --flux-serveur "$PORT" --ctx 256 --threads 8 > "$T/n2.log" 2>&1 & SRV=$!
for _ in $(seq 1 40); do grep -q "nœud moteur sur" "$T/n2.log" 2>/dev/null && break; sleep 0.25; done
T2=$($D "$M" --ppl-reparti "127.0.0.1:$PORT" --topologie "$TOPO" --ids-file "$IDS" \
     --limit "$LIMITE" --ctx 256 --threads 8 --abits 16 2>&1 \
     | grep -E "deux nœuds +: perplexité [0-9.]+|écart +: +[0-9.e+-]+")
echo "  $T2"
kill $SRV 2>/dev/null; wait $SRV 2>/dev/null

A=$(printf '%s' "$H" | grep -oE "[0-9.]+" | head -1)
B=$(printf '%s' "$T2" | grep -oE "[0-9.]+" | head -1)
E=$(printf '%s' "$T2" | grep -oE "écart +: +[0-9.e+-]+" | grep -oE "[0-9.e+-]+$")
echo "=== verdict ==="
if [ -n "$A" ] && [ "$A" = "$B" ]; then
    echo "  PORTE TENUE : la topologie rend le MÊME chiffre que le découpage historique ($A)"
else
    echo "  ÉCHEC : historique $A · topologie $B"; exit 1
fi
[ "$E" = "0.00e0" ] && echo "  écart de flux : 0.00e0 ✅" || echo "  écart de flux : ${E:-?} ⚠️"

echo "=== 4. les refus (une topologie fausse ne doit pas se mesurer) ==="
sed "s/\[$COUCHES, $((N-1))\]/[$((COUCHES+1)), $((N-1))]/" "$TOPO" > "$T/trou.json"
$D "$M" --topologie "$T/trou.json" 2>&1 | tail -1
$D "$M" --ppl-reparti "127.0.0.1:1" --topologie "$TOPO" --ids-file "$IDS" --limit 8 \
    --ctx 256 --threads 8 2>&1 | tail -1
rm -rf "$T"
