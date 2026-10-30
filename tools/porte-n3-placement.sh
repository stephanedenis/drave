#!/bin/bash
# porte-n3-placement.sh — N3.4c : le champ `placement` du DRVM natif agit-il ?
#
# Deux DRVM de MÊMES poids, l'un `placement=local`, l'autre `placement=remote`.
# Le service natif ne lit que l'architecture : si la génération est identique, le
# placement est MÉTADONNÉE, pas un chemin distribué. Le contrôle : un vrai
# changement (pont nul) doit, lui, changer la sortie.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-placement-XXXXXX")
trap 'rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. local, remote (mêmes poids), pont nul (contrôle) ==="
"$PY" - "$T" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
base = dict(vocab=256, d_model=64, n_blocks=4, n_heads=4, expert_hidden=32,
            n_experts=4, top_k=2, kwta=0.5, window=32, max_pos=2048,
            thought_steps=1, early_blocks=(1,), rsn_dim=8)
torch.manual_seed(7); a = NativeModel(NativeConfig(**base)); exporter_drvm(a, sys.argv[1] + "/a.drvm", "local")
torch.manual_seed(7); b = NativeModel(NativeConfig(**base)); exporter_drvm(b, sys.argv[1] + "/b.drvm", "remote")
torch.manual_seed(7); c = NativeModel(NativeConfig(**base))
for nom, p in c.state_dict().items():
    if "bridge" in nom: p.zero_()
exporter_drvm(c, sys.argv[1] + "/c.drvm", "local")
print(f"  A local · B remote · C pont nul · {a.nb_parametres()} paramètres")
PY

gen() { "$D" --drvm-generate "$1" "abc" 16 2>/dev/null; }
gen "$T/a.drvm" > "$T/a1"; gen "$T/a.drvm" > "$T/a2"; gen "$T/b.drvm" > "$T/b1"; gen "$T/c.drvm" > "$T/c1"
cmp -s "$T/a1" "$T/a2" || { echo "  ❌ A non déterministe"; exit 1; }
[ -s "$T/a1" ] || { echo "  ❌ A vide"; exit 1; }
echo "  ✅ A déterministe ($(wc -c < "$T/a1") octets)"

if cmp -s "$T/a1" "$T/b1"; then
    echo "  ✅ local et remote donnent la MÊME sortie : le placement est une métadonnée inerte"
else
    echo "  ❌ le placement change la sortie : un chemin distribué existe (à vérifier)"
    exit 1
fi
if cmp -s "$T/a1" "$T/c1"; then
    echo "  ❌ le contrôle (pont nul) ne change rien : la porte ne détecte pas un vrai changement"
    exit 1
fi
echo "  ✅ le contrôle pont nul change la sortie : la porte détecte un vrai changement"
echo "PORTE TENUE : placement natif = métadonnée · A déterministe · contrôle pont nul détecté"
