#!/bin/bash
# porte-n3-refus.sh — N3.5d : le protocole REFUSE un aval qui n'a pas le même modèle.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-refus-XXXXXX")
trap 'kill ${SRV:-} 2>/dev/null; wait ${SRV:-} 2>/dev/null; rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. modèles A (normal) et B (pont nul) ==="
"$PY" - "$T" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
base = dict(vocab=256, d_model=64, n_blocks=4, n_heads=4, expert_hidden=32,
            n_experts=4, top_k=2, kwta=0.5, window=32, max_pos=2048,
            thought_steps=1, early_blocks=(1,), rsn_dim=8)
torch.manual_seed(7); a = NativeModel(NativeConfig(**base)); exporter_drvm(a, sys.argv[1] + "/a.drvm")
torch.manual_seed(7); b = NativeModel(NativeConfig(**base))
for nom, p in b.state_dict().items():
    if "bridge" in nom: p.zero_()
exporter_drvm(b, sys.argv[1] + "/b.drvm")
print(f"  A/B : {a.nb_parametres()} paramètres")
PY
PORT=$((64000 + RANDOM % 1200))
"$D" --drvm-serve-aval "$T/b.drvm" 2 "$PORT" > "$T/srv.log" 2>&1 & SRV=$!
for _ in $(seq 1 80); do grep -q 'drvm-serve-aval' "$T/srv.log" 2>/dev/null && break; kill -0 $SRV 2>/dev/null || { cat "$T/srv.log"; exit 2; }; sleep 0.2; done

echo "=== 2. client A contre aval B : REFUS ==="
set +e
OUT=$("$D" --drvm-split-net "$T/a.drvm" 2 abc "127.0.0.1:$PORT" 2>&1); CODE=$?
set +e
[ "$CODE" = "4" ] || { echo "  ❌ code $CODE au lieu de 4 : $OUT"; exit 1; }
printf '%s\n' "$OUT" | grep -q "REFUS" || { echo "  ❌ pas de REFUS : $OUT"; exit 1; }
echo "  ✅ REFUS (code 4) sans logits"
kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; SRV=""

echo "=== 3. client A contre aval A : succès ==="
PORT=$((65200 + RANDOM % 300))
"$D" --drvm-serve-aval "$T/a.drvm" 2 "$PORT" > "$T/srv.log" 2>&1 & SRV=$!
for _ in $(seq 1 80); do grep -q 'drvm-serve-aval' "$T/srv.log" 2>/dev/null && break; kill -0 $SRV 2>/dev/null || { cat "$T/srv.log"; exit 2; }; sleep 0.2; done
H=$("$D" --drvm-pas-hex "$T/a.drvm" abc 2>/dev/null)
S=$("$D" --drvm-split-net "$T/a.drvm" 2 abc "127.0.0.1:$PORT" 2>/dev/null)
[ "$S" = "$H" ] || { echo "  ❌ succès non bit-exact"; exit 1; }
echo "  ✅ succès bit-exact"
echo "PORTE TENUE : empreinte refusée (code 4) · même modèle bit-exact"
