#!/bin/bash
# carte_latence.sh — « à partir de quel aller-retour le découpage cesse de payer ? »
#
# POURQUOI CETTE CARTE. Le découpage à deux nœuds est prouvé exact (écart 0,00e0,
# § 8 et portes). Mais il est prouvé sur LOCALHOST, où l'aller-retour vaut quelques
# dizaines de microsecondes — un plancher optimiste. Sur un vrai réseau, la
# question n'est pas le débit (0,25 Mbit/s de flux) mais la LATENCE par message :
# chaque jeton traverse la frontière une fois par couche échangée.
#
# `tools/proxy_latence.py` est un relais TCP qui ajoute un délai réglable. On
# l'intercale entre le pilote et le nœud, et on refait la mesure pour 0, 1, 5, 20
# et 50 ms : le temps mur dit où le découpage perd son avantage, et la perplexité
# dit si le transport reste exact (elle ne doit PAS bouger).
#
# Usage :
#   carte_latence.sh [--modele M.gguf] [--ids F] [--couches 2] ["--delais 0 1 5 20 50"]
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
MODELE=/tmp/m5_d384_route_distille.gguf
IDS=${IDS:-/tmp/campagne24/route_ids128.txt}
COUCHES=2
LIMITE=128
CTX=256
DELAIS="0 1 5 20 50"
while [ $# -gt 0 ]; do
    case "$1" in
        --modele) MODELE="$2"; shift 2 ;;
        --ids) IDS="$2"; shift 2 ;;
        --couches) COUCHES="$2"; shift 2 ;;
        --limite) LIMITE="$2"; shift 2 ;;
        --delais) DELAIS="$2"; shift 2 ;;
        *) shift ;;
    esac
done
[ -s "$MODELE" ] && [ -s "$IDS" ] || { echo "modèle ou identifiants absents"; exit 2; }

# La référence : le modèle entier, un seul processus, même quantification.
REF_T0=$(date +%s.%N)
REF=$(timeout 600 $D "$MODELE" --ppl "$IDS" --limit "$LIMITE" --ctx "$CTX" --threads 8 2>&1 \
      | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+")
REF_T1=$(date +%s.%N)
REF_S=$(echo "$REF_T1 $REF_T0" | awk '{printf "%.1f", $1-$2}')
echo "# $(basename "$MODELE") · entier : perplexité $REF en ${REF_S} s"
echo
echo "| latence par message | perplexité | mur (s) | vs entier |"
echo "|---:|---:|---:|---:|"

for ms in $DELAIS; do
    PORT=$(( 50000 + RANDOM % 5000 ))
    RELAIS=$(( PORT + 1 ))
    LOGS=$(mktemp -d)
    $D "$MODELE" --flux-serveur "$PORT" --ctx "$CTX" --threads 8 > "$LOGS/noeud.log" 2>&1 &
    SRV=$!
    for _ in $(seq 1 120); do
        grep -q "nœud moteur sur" "$LOGS/noeud.log" 2>/dev/null && break
        kill -0 $SRV 2>/dev/null || break
        sleep 0.25
    done
    /home/stephane/gpu-env/bin/python tools/proxy_latence.py "$RELAIS" "127.0.0.1:$PORT" "$ms" \
        > "$LOGS/relais.log" 2>&1 &
    REL=$!
    sleep 0.5
    T0=$(date +%s.%N)
    SORTIE=$(timeout 900 $D "$MODELE" --ppl-reparti "127.0.0.1:$RELAIS" --ids-file "$IDS" \
             --couches-locales "$COUCHES" --limit "$LIMITE" --ctx "$CTX" --threads 8 \
             --abits 16 2>&1)
    T1=$(date +%s.%N)
    kill $REL $SRV 2>/dev/null; wait $REL $SRV 2>/dev/null
    PPL=$(printf '%s\n' "$SORTIE" | grep -oE "perplexité [0-9.]+" | tail -1 | grep -oE "[0-9.]+")
    MUR=$(echo "$T1 $T0" | awk '{printf "%.1f", $1-$2}')
    RAP=$(echo "$MUR $REF_S" | awk '{printf "x%.2f", $1/($2+0.001)}')
    echo "| +${ms} ms | ${PPL:-échec} | $MUR | $RAP |"
    rm -rf "$LOGS"
done
