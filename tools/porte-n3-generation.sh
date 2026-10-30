#!/bin/bash
# porte-n3-generation.sh — N3.5e : génération répartie sur deux processus TCP.
# L'amont garde son cache 0..k, l'aval son cache k..n ; la sortie doit être
# bit-identique à `generer` local.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-generation-XXXXXX")
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
m = NativeModel(cfg); exporter_drvm(m, sys.argv[1])
print(f"  {m.nb_parametres()} paramètres")
PY
PORT=$((62500 + RANDOM % 1500))
"$D" --drvm-serve-gen "$T/m.drvm" 2 "$PORT" > "$T/srv.log" 2>&1 & SRV=$!
for _ in $(seq 1 80); do grep -q 'drvm-serve-gen' "$T/srv.log" 2>/dev/null && break; kill -0 $SRV 2>/dev/null || { cat "$T/srv.log"; exit 2; }; sleep 0.2; done

ref() { "$D" --drvm-generate-hex "$T/m.drvm" "$1" 12 2>/dev/null; }
echo "=== 2. K=0..4, prompt abc ==="
H=$(ref abc); [ -n "$H" ] || { echo "  ❌ référence vide"; exit 1; }
for K in 0 1 2 3 4; do
    S=$("$D" --drvm-gen-net "$T/m.drvm" "$K" abc 12 "127.0.0.1:$PORT" 2>/dev/null)
    [ "$S" = "$H" ] || { echo "  ❌ K=$K : ${S:0:16} ≠ ${H:0:16}"; exit 1; }
    printf '  K=%s ✅ %s…\n' "$K" "${S:0:16}"
done
echo "=== 3. prompt zzz, K=1/2 ==="
H2=$(ref zzz)
for K in 1 2; do
    S=$("$D" --drvm-gen-net "$T/m.drvm" "$K" zzz 12 "127.0.0.1:$PORT" 2>/dev/null)
    [ "$S" = "$H2" ] || { echo "  ❌ zzz K=$K"; exit 1; }
done
echo "  ✅ zzz identique"
echo "PORTE TENUE : génération répartie · deux caches · sortie bit-identique"
