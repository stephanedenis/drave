#!/bin/bash
# porte-n3-routes.sh — N3.3a : le routage/k-WTA du natif est-il VIVANT ?
#
# LA QUESTION. N3 demande une porte pour `k-WTA / routes`. Ici on ne mesure pas la
# qualité du routage : on prouve qu'il **agit**. Deux DRVM sont exportés avec les
# MÊMES poids (même graine) et des configs de routage différentes (`top_k=2`,
# `kwta=0.5` contre `top_k=1`, `kwta=1.0`) ; la génération du moteur doit différer.
# Le contrôle : le même modèle deux fois doit rendre exactement la même sortie.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-routes-XXXXXX")
trap 'rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. deux DRVM, MÊMES poids, routages différents ==="
"$PY" - "$T" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
base = dict(vocab=256, d_model=32, n_blocks=1, n_heads=2, expert_hidden=16,
            n_experts=4, window=16, max_pos=2048, thought_steps=1,
            early_blocks=(0,), rsn_dim=8)
torch.manual_seed(7)
a = NativeModel(NativeConfig(top_k=2, kwta=0.5, **base))
torch.manual_seed(7)
b = NativeModel(NativeConfig(top_k=1, kwta=1.0, **base))
exporter_drvm(a, sys.argv[1] + "/a.drvm")
exporter_drvm(b, sys.argv[1] + "/b.drvm")
print(f"  A : top_k=2, kwta=0.5 · {a.nb_parametres()} paramètres")
print(f"  B : top_k=1, kwta=1.0 · {b.nb_parametres()} paramètres")
PY

echo "=== 2. le même modèle deux fois est identique ==="
"$D" --drvm-generate "$T/a.drvm" "abc" 12 > "$T/a1" 2>/dev/null
"$D" --drvm-generate "$T/a.drvm" "abc" 12 > "$T/a2" 2>/dev/null
cmp -s "$T/a1" "$T/a2" || { echo "  ❌ le même modèle deux fois diffère"; exit 1; }
[ -s "$T/a1" ] || { echo "  ❌ génération A vide"; exit 1; }
echo "  ✅ même modèle, même sortie ($(wc -c < "$T/a1") octets)"

echo "=== 3. le routage différent change la génération ==="
"$D" --drvm-generate "$T/b.drvm" "abc" 12 > "$T/b1" 2>/dev/null
[ -s "$T/b1" ] || { echo "  ❌ génération B vide"; exit 1; }
if cmp -s "$T/a1" "$T/b1"; then
    echo "  ❌ top_k/kwta ne change pas la sortie : le routage est inerte"
    exit 1
fi
echo "  ✅ top_k=2/kwta=0.5 et top_k=1/kwta=1.0 donnent des sorties différentes"
echo "PORTE TENUE : routage vivant · même modèle déterministe · config différente change la sortie"
