#!/bin/bash
# porte-n3-positions.sh — N3.5f : le serveur vérifie la POSITION de chaque pas.
# Une position sautée est refusée (code 4), pas interprétée comme le pas suivant.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-positions-XXXXXX")
trap 'kill ${SRV:-} 2>/dev/null; wait ${SRV:-} 2>/dev/null; rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }
echo "=== 1. modèle 4 blocs ==="
"$PY" - "$T/m.drvm" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
torch.manual_seed(7)
cfg = NativeConfig(vocab=256, d_model=64, n_blocks=4, n_heads=4, expert_hidden=32,
                   n_experts=4, top_k=2, kwta=0.5, window=32, max_pos=2048,
                   thought_steps=1, early_blocks=(1,), rsn_dim=8)
m = NativeModel(cfg); exporter_drvm(m, sys.argv[1]); print(f"  {m.nb_parametres()} paramètres")
PY
PORT=$((63000 + RANDOM % 1000))
"$D" --drvm-serve-gen "$T/m.drvm" 2 "$PORT" > "$T/srv.log" 2>&1 & SRV=$!
for _ in $(seq 1 80); do grep -q 'drvm-serve-gen' "$T/srv.log" 2>/dev/null && break; kill -0 $SRV 2>/dev/null || { cat "$T/srv.log"; exit 2; }; sleep 0.2; done
echo "=== 2. succès normal (K=2) ==="
H=$("$D" --drvm-generate-hex "$T/m.drvm" abc 12 2>/dev/null)
S=$("$D" --drvm-gen-net "$T/m.drvm" 2 abc 12 "127.0.0.1:$PORT" 2>/dev/null)
[ "$S" = "$H" ] || { echo "  ❌ succès non bit-exact"; exit 1; }
echo "  ✅ bit-exact"
echo "=== 3. position désynchronisée : REFUS ==="
set +e
OUT=$(DRAVE_POS_DESYNC=1 "$D" --drvm-gen-net "$T/m.drvm" 2 abc 12 "127.0.0.1:$PORT" 2>&1); CODE=$?
set +e
[ "$CODE" = "4" ] || { echo "  ❌ code $CODE au lieu de 4 : $OUT"; exit 1; }
printf '%s\n' "$OUT" | grep -q "REFUS" || { echo "  ❌ pas de REFUS : $OUT"; exit 1; }
echo "  ✅ REFUS (code 4)"
echo "PORTE TENUE : position vérifiée pas à pas · désync refusée · succès bit-exact"
