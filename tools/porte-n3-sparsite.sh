#!/bin/bash
# porte-n3-sparsite.sh — N3.3b : `kwta` et `top_k` agissent-ils SÉPARÉMENT ?
#
# N3.3a changeait `top_k` ET `kwta` ensemble. Ici trois DRVM partagent les mêmes
# poids (graine 7) et ne diffèrent que par un paramètre :
#   A : top_k=2, kwta=0.5   (référence)
#   B : top_k=2, kwta=0.25  (même top_k, plus de sparsité)
#   C : top_k=3, kwta=0.5   (même kwta, un expert de plus)
# La génération A doit être déterministe ; A/B et A/C doivent différer. C'est la
# séparation que N3.3a ne faisait pas.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-sparsite-XXXXXX")
trap 'rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. trois DRVM, mêmes poids, un paramètre diffère ==="
"$PY" - "$T" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
base = dict(vocab=256, d_model=32, n_blocks=1, n_heads=2, expert_hidden=16,
            n_experts=4, window=16, max_pos=2048, thought_steps=1,
            early_blocks=(0,), rsn_dim=8)
for nom, top_k, kwta in (("a", 2, 0.5), ("b", 2, 0.25), ("c", 3, 0.5)):
    torch.manual_seed(7)
    m = NativeModel(NativeConfig(top_k=top_k, kwta=kwta, **base))
    exporter_drvm(m, f"{sys.argv[1]}/{nom}.drvm")
    print(f"  {nom.upper()} : top_k={top_k}, kwta={kwta} · {m.nb_parametres()} paramètres")
PY

gen() { "$D" --drvm-generate "$1" "abc" 12 2>/dev/null; }

echo "=== 2. A deux fois est identique ==="
gen "$T/a.drvm" > "$T/a1"; gen "$T/a.drvm" > "$T/a2"
cmp -s "$T/a1" "$T/a2" || { echo "  ❌ A n'est pas déterministe"; exit 1; }
[ -s "$T/a1" ] || { echo "  ❌ génération A vide"; exit 1; }
echo "  ✅ A identique ($(wc -c < "$T/a1") octets)"

echo "=== 3. kwta seul change la sortie ==="
gen "$T/b.drvm" > "$T/b1"; [ -s "$T/b1" ] || { echo "  ❌ génération B vide"; exit 1; }
if cmp -s "$T/a1" "$T/b1"; then echo "  ❌ kwta ne change pas la sortie"; exit 1; fi
echo "  ✅ kwta=0.5 contre 0.25 : sorties différentes"

echo "=== 4. top_k seul change la sortie ==="
gen "$T/c.drvm" > "$T/c1"; [ -s "$T/c1" ] || { echo "  ❌ génération C vide"; exit 1; }
if cmp -s "$T/a1" "$T/c1"; then echo "  ❌ top_k ne change pas la sortie"; exit 1; fi
echo "  ✅ top_k=2 contre 3 : sorties différentes"
echo "PORTE TENUE : kwta et top_k agissent séparément · A déterministe"
