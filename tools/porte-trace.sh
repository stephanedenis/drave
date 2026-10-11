#!/bin/bash
# porte-trace.sh — la porte de la capacité C12 : la trace globale et son rejeu.
#
# Trois cas, et le troisième est le plus important :
#   1. une exécution répartie ÉCRIT une trace (un croisement par pas et par lien) ;
#   2. le REJEU de la même exécution ne diverge pas — c'est l'invariant ;
#   3. une trace FAUSSÉE d'un seul bit est DÉTECTÉE et NOMMÉE (pas, région, lien).
# Une porte qui ne sait pas échouer ne vérifie rien : le cas 3 est là pour ça.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
. tools/_corpus.sh    # régénère le corpus si /tmp a été effacé (redémarrage)
LIMITE=${LIMITE:-64}
PORT=${PORT:-$((51000 + RANDOM % 800))}
T=$(mktemp -d)
TOPO="$T/topo.json"
cat > "$TOPO" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"d","couches":[12,23],"instance":"127.0.0.1:$PORT"}],
 "liens":[{"de":"local","vers":"d","mode":"f32"}]}
JSON
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }

nœud() { $D "$M" --flux-serveur "$PORT" --ctx 256 --threads 8 > "$T/n.log" 2>&1 & echo $!; }
pilote() { $D "$M" --ppl-reparti "127.0.0.1:$PORT" --topologie "$TOPO" --ids-file "$IDS" \
           --limit "$LIMITE" --ctx 256 --threads 8 --flux "$@" 2>&1; }

echo "=== 1. exécution + trace globale ==="
N=$(nœud); sleep 2
S=$(pilote --trace-globale "$T/trace.txt")
printf '%s\n' "$S" | grep -E "trace\]|deux nœuds" | sed 's/^/  /'
kill $N 2>/dev/null; wait $N 2>/dev/null
LIGNES=$(grep -vc '^#' "$T/trace.txt" 2>/dev/null || echo 0)
echo "  croisements enregistrés : $LIGNES"

echo "=== 2. rejeu de la même exécution ==="
N=$(nœud); sleep 2
R=$(pilote --verifier-globale "$T/trace.txt")
printf '%s\n' "$R" | grep -E "rejeu" | sed 's/^/  /'
kill $N 2>/dev/null; wait $N 2>/dev/null
printf '%s' "$R" | grep -q "AUCUNE divergence" && echo "  ✅ rejeu identique" || { echo "  ❌ rejeu divergent"; exit 1; }

echo "=== 3. trace FAUSSÉE d'un seul bit ==="
python3 - "$T/trace.txt" "$T/fausse.txt" <<'PY'
import sys
lignes = open(sys.argv[1]).read().splitlines()
for i, l in enumerate(lignes):
    if l.startswith('local '):
        ch = l.split(); ch[4] = hex(int(ch[4], 16) ^ 1); lignes[i] = ' '.join(ch); break
open(sys.argv[2], 'w').write('\n'.join(lignes) + '\n')
PY
N=$(nœud); sleep 2
F=$(pilote --verifier-globale "$T/fausse.txt"); CODE=$?
kill $N 2>/dev/null; wait $N 2>/dev/null
printf '%s\n' "$F" | grep -E "DIVERGENCE" | sed 's/^/  /'
printf '%s' "$F" | grep -q "DIVERGENCE AU BIT PRÈS" && echo "  ✅ la trace fausse est détectée et nommée" || { echo "  ❌ trace fausse NON détectée"; exit 1; }
rm -rf "$T"
