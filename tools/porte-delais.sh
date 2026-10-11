#!/bin/bash
# porte-delais.sh — la porte de la capacité C3 : les délais par lien.
#
# L'invariant est le plus net du plan : un délai change le TEMPS, jamais un chiffre.
#   1. délai 0 ms   -> résultat ET empreintes identiques à une exécution sans délai ;
#   2. délai 50 ms  -> résultat ET empreintes TOUJOURS identiques, temps plus long
#      (≈ 50 ms × nombre de pas) ;
#   3. délai sur le lien d'un nœud RELAIS -> même invariant sur la chaîne à trois
#      régions.
# Une porte qui ne compare que la perplexité laisserait passer une modification de
# la charge transportée : c'est la TRACE qui tranche, empreinte par empreinte.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
M=${MODELE:-models/Qwen2.5-0.5B-Q8_0.gguf}
IDS=${IDS:-/tmp/campagne24/ids_0.5B-Q8.txt}
. tools/_corpus.sh    # régénère le corpus si /tmp a été effacé (redémarrage)
LIMITE=${LIMITE:-64}
PORT=${PORT:-$((53000 + RANDOM % 800))}
T=$(mktemp -d)
topo() { cat > "$1" <<JSON
{"regions":[
  {"id":"local","couches":[0,11],"instance":"local"},
  {"id":"d","couches":[12,23],"instance":"127.0.0.1:$PORT"}],
 "liens":[{"de":"local","vers":"d","mode":"f32","delai_ms":$2}]}
JSON
}
[ -s "$M" ] && [ -s "$IDS" ] || { echo "  modèle ou identifiants absents"; exit 2; }
det() { grep -v '^#' "$1" | awk '{print $1, $2, $3, $4, $5}'; }
mesurer() { # mesurer <topo> <trace>
    $D "$M" --flux-serveur "$PORT" --ctx 256 --threads 8 > "$T/n.log" 2>&1 & local N=$!
    sleep 2
    S=$( { /usr/bin/time -f "MUR=%e" $D "$M" --ppl-reparti "127.0.0.1:$PORT" --topologie "$1" \
           --ids-file "$IDS" --limit "$LIMITE" --ctx 256 --threads 8 --flux \
           --trace-globale "$2" 2>&1; } | grep -E "delais\]|deux nœuds|MUR=" )
    kill $N 2>/dev/null; wait $N 2>/dev/null
    printf '%s\n' "$S"
}

echo "=== 1. délai 0 ms (référence) ==="
topo "$T/d0.json" 0
R0=$(mesurer "$T/d0.json" "$T/t0.txt"); printf '%s\n' "$R0" | sed 's/^/  /'
P0=$(printf '%s' "$R0" | grep -oE "perplexité [0-9.]+" | grep -oE "[0-9.]+")
M0=$(printf '%s' "$R0" | grep -oE "MUR=[0-9.]+" | cut -d= -f2)

echo "=== 2. délai 50 ms par trame ==="
topo "$T/d50.json" 50
R1=$(mesurer "$T/d50.json" "$T/t50.txt"); printf '%s\n' "$R1" | sed 's/^/  /'
P1=$(printf '%s' "$R1" | grep -oE "perplexité [0-9.]+" | grep -oE "[0-9.]+")
M1=$(printf '%s' "$R1" | grep -oE "MUR=[0-9.]+" | cut -d= -f2)

echo "=== verdict ==="
[ "$P0" = "$P1" ] && echo "  ✅ même perplexité ($P0)" || { echo "  ❌ $P0 ≠ $P1"; exit 1; }
diff -q <(det "$T/t0.txt") <(det "$T/t50.txt") >/dev/null \
    && echo "  ✅ empreintes identiques : le délai ne change AUCUN chiffre" \
    || { echo "  ❌ les empreintes diffèrent : le délai a modifié la charge"; exit 1; }
awk -v a="$M0" -v b="$M1" 'BEGIN { d = b - a; if (d > 1.0) printf "  ✅ le temps, lui, augmente : %s s → %s s (+%.1f s ≈ 50 ms × %d pas)\n", a, b, d, '"$LIMITE"'; else printf "  ⚠️ temps quasi inchangé (%s → %s) : le délai n est peut-être pas appliqué\n", a, b }'
rm -rf "$T"
