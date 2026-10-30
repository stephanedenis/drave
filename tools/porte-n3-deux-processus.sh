#!/bin/bash
# porte-n3-deux-processus.sh — N3.5b : le découpage en DEUX PROCESSUS (fichier)
# rend-il les mêmes logits que le `pas` plein ?
#
# L'amont écrit les hiddens de frontière de TOUTES les positions ; l'aval les
# relit, traverse k..n et applique la tête. Le fichier est le support ; le calcul
# est réparti en deux exécutions séparées. Aucun réseau (N3.5c).
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-deux-processus-XXXXXX")
trap 'rm -rf "$T"' EXIT
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

ref() { "$D" --drvm-pas-hex "$T/m.drvm" "$1" 2>/dev/null; }
H=$(ref abc); [ -n "$H" ] || { echo "  ❌ référence vide"; exit 1; }
echo "=== 2. deux processus, K=0..4 ==="
for K in 0 1 2 3 4; do
    "$D" --drvm-split-amont "$T/m.drvm" "$K" abc "$T/h.$K" 2>/dev/null || { echo "  ❌ amont K=$K"; exit 1; }
    S=$("$D" --drvm-split-aval "$T/m.drvm" "$K" "$T/h.$K" 2>/dev/null) || { echo "  ❌ aval K=$K"; exit 1; }
    [ "$S" = "$H" ] || { echo "  ❌ K=$K : $S ≠ $H"; exit 1; }
    printf '  K=%s ✅ %s…\n' "$K" "${S:0:16}"
done
echo "=== 3. prompt zzz, K=1/2 ==="
H2=$(ref zzz)
for K in 1 2; do
    "$D" --drvm-split-amont "$T/m.drvm" "$K" zzz "$T/z.$K" 2>/dev/null
    S=$("$D" --drvm-split-aval "$T/m.drvm" "$K" "$T/z.$K" 2>/dev/null)
    [ "$S" = "$H2" ] || { echo "  ❌ zzz K=$K"; exit 1; }
done
echo "  ✅ zzz identique"
echo "PORTE TENUE : deux processus · fichier de frontière · logits identiques au pas plein"
