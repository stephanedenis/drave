#!/bin/bash
# porte-n3-cache.sh — N3.2b2 : que gagne-t-on à couper la profondeur en génération ?
#
# Le service peut calculer à profondeur 1 (`DRAVE_NATIVE_PROFONDEUR=1`) ou pleine.
# La porte mesure le TEMPS et la SORTIE des deux, sur un modèle à 8 blocs :
#   - la profondeur 1 est plus rapide ;
#   - elle change la génération ;
#   - ce n'est pas une sortie précoce gratuite : les couches sautées ne fournissent
#     plus leurs K/V aux jetons suivants. La porte nomme la condition, elle ne
#     prétend pas que le saut de calcul se transpose tel quel au cache.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-cache-XXXXXX")
trap 'kill ${SRV:-} 2>/dev/null; wait ${SRV:-} 2>/dev/null; rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. DRVM à 8 blocs, graine 7 ==="
"$PY" - "$T/m.drvm" "$T/params" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
torch.manual_seed(7)
cfg = NativeConfig(vocab=256, d_model=64, n_blocks=8, n_heads=4, expert_hidden=32,
                   n_experts=4, top_k=2, kwta=0.5, window=32, max_pos=2048,
                   thought_steps=1, early_blocks=(3,), rsn_dim=8)
m = NativeModel(cfg); exporter_drvm(m, sys.argv[1]); open(sys.argv[2], "w").write(str(m.nb_parametres()))
print(f"  {m.nb_parametres()} paramètres")
PY

demarrer() { if [ "$1" = plein ]; then unset DRAVE_NATIVE_PROFONDEUR; else export DRAVE_NATIVE_PROFONDEUR=1; fi; "$D" --drvm-serve "$T/m.drvm" "$2" > "$3" 2>&1 & SRV=$!; for _ in $(seq 1 80); do grep -q 'drvm-serve' "$3" 2>/dev/null && return 0; kill -0 $SRV 2>/dev/null || return 1; sleep 0.2; done; return 1; }
gen() { "$PY" - "$1" <<'PY'
import json, sys, urllib.request
req = urllib.request.Request(f"http://127.0.0.1:{sys.argv[1]}/generer?n=16", data=b"abc", method="POST")
with urllib.request.urlopen(req, timeout=30) as r:
    d = json.loads(r.read().decode("utf-8", "replace"), strict=False)
print(json.dumps({"ms": d["ms"], "octets": d["octets"], "texte": d["texte"]}, ensure_ascii=False))
PY
}
P1=$((64500 + RANDOM % 300)); P2=$((64800 + RANDOM % 300))

echo "=== 2. pleine profondeur (3 mesures) ==="
demarrer plein "$P1" "$T/plein.log" || { cat "$T/plein.log"; exit 2; }
for i in 1 2 3; do gen "$P1" > "$T/f$i"; done; kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; SRV=""
echo "=== 3. profondeur 1 (3 mesures) ==="
demarrer un "$P2" "$T/un.log" || { cat "$T/un.log"; exit 2; }
for i in 1 2 3; do gen "$P2" > "$T/u$i"; done; kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; SRV=""

python3 - "$T" <<'PY' || exit 1
import json, pathlib, statistics, sys
T = pathlib.Path(sys.argv[1])
f = [json.loads((T / f"f{i}").read_text()) for i in (1, 2, 3)]
u = [json.loads((T / f"u{i}").read_text()) for i in (1, 2, 3)]
for nom, xs in (("plein", f), ("profondeur 1", u)):
    if len({x["texte"] for x in xs}) != 1:
        sys.exit(f"  ❌ {nom} n'est pas déterministe")
mf, mu = statistics.median(x["ms"] for x in f), statistics.median(x["ms"] for x in u)
print(f"  plein : {mf:.1f} ms médian · profondeur 1 : {mu:.1f} ms médian")
if not (mu < mf):
    sys.exit(f"  ❌ la profondeur 1 n'est pas plus rapide ({mu:.1f} vs {mf:.1f} ms)")
if f[0]["texte"] == u[0]["texte"]:
    sys.exit("  ❌ la profondeur 1 rend le même texte que la pleine")
print("  ✅ profondeur 1 plus rapide ET sortie différente")
print(f"  ⚠️ les couches sautées ne fournissent plus leurs K/V : ce n'est pas un saut gratuit")
PY
echo "PORTE TENUE : saut de calcul mesuré · sortie changée · condition K/V nommée"
