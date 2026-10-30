#!/bin/bash
# porte-n3-deux-regions.sh — N3.5a : le modèle natif coupé en deux régions
# (blocs 0..k puis k..n) rend-il EXACTEMENT le modèle plein ?
#
# Aucun réseau ici : c'est le contrôle du DÉCOUPAGE, en un processus. K=0 et
# K=n encadrent le pont ; K=1 le met dans l'aval, K=2 dans l'amont (4 blocs).
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-deux-regions-XXXXXX")
trap 'rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. modèle à 4 blocs (pont à l'indice 1) ==="
"$PY" - "$T/m.drvm" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
torch.manual_seed(7)
cfg = NativeConfig(vocab=256, d_model=64, n_blocks=4, n_heads=4, expert_hidden=32,
                   n_experts=4, top_k=2, kwta=0.5, window=32, max_pos=2048,
                   thought_steps=1, early_blocks=(1,), rsn_dim=8)
m = NativeModel(cfg); exporter_drvm(m, sys.argv[1])
print(f"  {m.nb_parametres()} paramètres · 4 blocs")
PY

ref() { "$D" --drvm-generate-hex "$T/m.drvm" "$1" 12 2>/dev/null; }
split() { "$D" --drvm-generate-split "$T/m.drvm" "$1" "$2" 12 2>/dev/null; }

echo "=== 2. balayage K=0..4, prompt abc ==="
H=$(ref abc); [ -n "$H" ] || { echo "  ❌ référence vide"; exit 1; }
for K in 0 1 2 3 4; do
    S=$(split "$K" abc)
    [ "$S" = "$H" ] || { echo "  ❌ K=$K : $S ≠ $H"; exit 1; }
    printf '  K=%s ✅ %s…\n' "$K" "${S:0:16}"
done
echo "  ✅ cinq découpages identiques au modèle plein"

echo "=== 3. un autre prompt, K=1 et K=2 ==="
H2=$(ref zzz); [ -n "$H2" ] || { echo "  ❌ référence zzz vide"; exit 1; }
for K in 1 2; do S=$(split "$K" zzz); [ "$S" = "$H2" ] || { echo "  ❌ zzz K=$K"; exit 1; }; done
echo "  ✅ zzz identique aussi"
echo "PORTE TENUE : découpage 0..k / k..n bit-exact · pont des deux côtés · prompt différent"
