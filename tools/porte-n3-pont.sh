#!/bin/bash
# porte-n3-pont.sh — N3.4b : le PONT natif agit-il dans la génération ?
#
# Deux DRVM de mêmes poids (graine 7), sauf le pont : B a `bridge.weight` et
# `bridge.bias` mis à zéro. Si le pont est branché, la génération doit différer ;
# A deux fois doit être identique. C'est la brique « pont » de N3, dans le moteur.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-pont-XXXXXX")
trap 'rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. deux DRVM, mêmes poids, pont nul dans B ==="
"$PY" - "$T" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
base = dict(vocab=256, d_model=64, n_blocks=4, n_heads=4, expert_hidden=32,
            n_experts=4, top_k=2, kwta=0.5, window=32, max_pos=2048,
            thought_steps=1, early_blocks=(1,), rsn_dim=8)
torch.manual_seed(7); a = NativeModel(NativeConfig(**base))
torch.manual_seed(7); b = NativeModel(NativeConfig(**base))
zero = 0
for nom, p in b.state_dict().items():
    if "bridge" in nom:
        p.zero_(); zero += p.numel()
exporter_drvm(a, sys.argv[1] + "/a.drvm")
exporter_drvm(b, sys.argv[1] + "/b.drvm")
print(f"  A : {a.nb_parametres()} paramètres · B : pont nul ({zero} poids)")
PY

gen() { "$D" --drvm-generate "$1" "abc" 16 2>/dev/null; }
echo "=== 2. A déterministe ==="
gen "$T/a.drvm" > "$T/a1"; gen "$T/a.drvm" > "$T/a2"
cmp -s "$T/a1" "$T/a2" || { echo "  ❌ A non déterministe"; exit 1; }
[ -s "$T/a1" ] || { echo "  ❌ A vide"; exit 1; }
echo "  ✅ A identique ($(wc -c < "$T/a1") octets)"

echo "=== 3. le pont nul change la génération ==="
gen "$T/b.drvm" > "$T/b1"; [ -s "$T/b1" ] || { echo "  ❌ B vide"; exit 1; }
if cmp -s "$T/a1" "$T/b1"; then echo "  ❌ le pont nul ne change rien : le pont est inerte"; exit 1; fi
echo "  ✅ pont actif : A et B diffèrent"
echo "PORTE TENUE : pont natif branché · A déterministe · pont nul change la sortie"
