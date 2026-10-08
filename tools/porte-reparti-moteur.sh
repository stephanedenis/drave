#!/bin/bash
# Porte de RÉPARTITION du modèle entraîné ici : deux nœuds, deux plages de couches.
#
# Ce qu'elle vérifie, et pourquoi elle est distincte de `tools/porte-flux.sh` :
# celle-ci tourne sur Qwen2.5-0.5B, un modèle venu d'ailleurs. Ici c'est NOTRE
# modèle (Qwen3-MoE entraîné sur le corpus d'octets), et la question n'est pas
# « le transport est-il fidèle » mais « le modèle qu'on a produit est-il
# découpable sans changer un chiffre ». Un modèle dont le routage d'experts ou
# les normes dépendraient d'un état global ne passerait pas.
#
#   tools/porte-reparti-moteur.sh
#   MODELE=/tmp/moteur_dense.gguf COUCHES=2 tools/porte-reparti-moteur.sh
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
MODELE=${MODELE:-/tmp/moteur_route.gguf}
IDS=${IDS:-/tmp/route_ids.txt}
PORT=${PORT:-$((49000 + RANDOM % 800))}
CTX=${CTX:-256}
LIMITE=${LIMITE:-128}          # doit valoir le nombre de jetons du fichier IDS
COUCHES=${COUCHES:-2}          # couches gardées côté pilote ; le reste au nœud

TRAVAIL=$(mktemp -d "${TMPDIR:-/tmp}/porte-reparti-XXXXXX")
LOG_SRV="$TRAVAIL/serveur.log"

[ -x "$D" ] || { echo "  $D absent : construire d'abord"; exit 1; }
[ -s "$MODELE" ] || { echo "  $MODELE absent"; exit 1; }
[ -s "$IDS" ] || { echo "  $IDS absent"; exit 1; }

echo "=== référence : le modèle ENTIER, un seul processus ==="
REF=$(timeout 300 "$D" "$MODELE" --ppl "$IDS" --limit "$LIMITE" --ctx "$CTX" --threads 8 2>&1 \
      | grep -oE "perplexité [0-9.]+ sur" | grep -oE "[0-9.]+")
[ -n "$REF" ] || { echo "  la référence n'a pas rendu de perplexité"; exit 1; }
echo "  perplexité entière : $REF"

echo "=== deux nœuds : $COUCHES couches locales, le reste à distance ==="
"$D" "$MODELE" --flux-serveur "$PORT" --ctx "$CTX" --threads 8 > "$LOG_SRV" 2>&1 &
SRV=$!
for _ in $(seq 1 120); do
    grep -q "nœud moteur sur" "$LOG_SRV" 2>/dev/null && break
    kill -0 $SRV 2>/dev/null || { echo "  le nœud est mort :"; tail -3 "$LOG_SRV"; exit 1; }
    sleep 0.25
done

# `--abits 16` : le mode réparti quantifie les activations à 8 bits par défaut,
# la perplexité à 16. Comparer les deux sans aligner ce réglage mesurerait la
# quantification, pas le découpage (mesuré : +0,6 % de perplexité à 8 bits).
SORTIE=$(timeout 300 "$D" "$MODELE" --ppl-reparti "127.0.0.1:$PORT" --ids-file "$IDS" \
         --couches-locales "$COUCHES" --limit "$LIMITE" --ctx "$CTX" --threads 8 \
         --abits 16 2>&1)
CODE=$?
kill $SRV 2>/dev/null; wait $SRV 2>/dev/null
DEUX=$(printf '%s\n' "$SORTIE" | grep -oE "perplexité [0-9.]+" | tail -1 | grep -oE "[0-9.]+")
ECART=$(printf '%s\n' "$SORTIE" | grep -oE "écart +: +[0-9.e+-]+" | grep -oE "[0-9.e+-]+$")

if [ -z "$DEUX" ]; then
    echo "  le pilote n'a pas rendu de perplexité (code $CODE) :"
    printf '%s\n' "$SORTIE" | tail -5
    exit 1
fi
echo "  perplexité répartie : $DEUX · écart de flux : ${ECART:-?}"

# Le critère : la perplexité répartie doit être celle du modèle entier. Sur un
# flux EXACT (mode dense f32) l'écart est nul ; sur un flux quantifié il est une
# perte assumée du codec, et c'est l'écart de flux — pas la perplexité — qui la
# porte. On exige donc l'égalité de perplexité à 0,1 % près.
VERDICT=$(/home/stephane/gpu-env/bin/python - "$REF" "$DEUX" <<'PY'
import sys
a, b = float(sys.argv[1]), float(sys.argv[2])
rel = abs(a - b) / a
print(f"{rel*100:.4f}")
sys.exit(0 if rel < 0.001 else 1)
PY
)
if [ $? -eq 0 ]; then
    echo "PORTE TENUE : le découpage ne change pas la perplexité (écart relatif $VERDICT %)"
    exit 0
fi
echo "PORTE NON TENUE : écart relatif $VERDICT % entre entier et réparti"
exit 1
