#!/bin/bash
# porte-n3-sparsite-compte.sh — N3.3c : le moteur COMPTE les experts et canaux actifs.
#
# N3.3b montrait que `kwta` et `top_k` changent la sortie ; cette porte lit les
# compteurs réels du moteur (`--drvm-sparsite`) :
#   A : top_k=2, kwta=0.5   → 3 appels, 6 experts, 48 canaux
#   B : top_k=2, kwta=0.25  → 3 appels, 6 experts, 24 canaux (kwta seul)
#   C : top_k=1, kwta=0.5   → 3 appels, 3 experts, 24 canaux (top_k seul)
# Trois octets de prompt, un bloc : 3 appels ffn ; 8 canaux par expert à kwta=0.5,
# 4 à kwta=0.25. Le contrôle est le comptage, pas la sortie.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-sparsite-compte-XXXXXX")
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
for nom, top_k, kwta in (("a", 2, 0.5), ("b", 2, 0.25), ("c", 1, 0.5)):
    torch.manual_seed(7)
    m = NativeModel(NativeConfig(top_k=top_k, kwta=kwta, **base))
    exporter_drvm(m, f"{sys.argv[1]}/{nom}.drvm")
    print(f"  {nom.upper()} : top_k={top_k}, kwta={kwta} · {m.nb_parametres()} paramètres")
PY

compte() { "$D" --drvm-sparsite "$1" "abc" 2>/dev/null; }
A=$(compte "$T/a.drvm"); B=$(compte "$T/b.drvm"); C=$(compte "$T/c.drvm")
A2=$(compte "$T/a.drvm")
echo "  A : $A"; echo "  B : $B"; echo "  C : $C"
[ "$A" = "$A2" ] || { echo "  ❌ A n'est pas déterministe : $A vs $A2"; exit 1; }

echo "=== 2. les compteurs attendus ==="
python3 - "$A" "$B" "$C" <<'PY' || exit 1
import sys
att = {"A": (3, 6, 48), "B": (3, 6, 24), "C": (3, 3, 24)}
for nom, ligne in zip(("A", "B", "C"), sys.argv[1:]):
    vals = tuple(int(x) for x in ligne.split() if x.isdigit())
    if vals != att[nom]:
        sys.exit(f"  ❌ {nom} : {vals} (attendu {att[nom]})")
    print(f"  ✅ {nom} : appels={vals[0]} experts={vals[1]} canaux={vals[2]}")
PY
echo "PORTE TENUE : compteurs réels · top_k agit sur les experts · kwta agit sur les canaux · A déterministe"
