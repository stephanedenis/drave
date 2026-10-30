#!/bin/bash
# porte-n3-seuil.sh — N3.2b1 : le service décide par SEUIL DE CONFIANCE.
#
# Le service calcule, pour chaque jeton, le chemin court (profondeur 1) ET le
# chemin plein ; il garde le jeton court si sa confiance (softmax max) atteint
# `seuil=`, sinon le jeton plein. Les deux caches sont entretenus : ce n'est PAS
# encore un saut de calcul (N3.2b), c'est la DÉCISION, et elle est comptée.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-seuil-XXXXXX")
trap 'kill ${SRV:-} 2>/dev/null; wait ${SRV:-} 2>/dev/null; rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. DRVM reproductible (2 blocs, graine 7) ==="
"$PY" - "$T/m.drvm" "$T/params" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
torch.manual_seed(7)
cfg = NativeConfig(vocab=256, d_model=32, n_blocks=2, n_heads=2, expert_hidden=16,
                   n_experts=4, top_k=2, kwta=0.5, window=16, max_pos=2048,
                   thought_steps=1, early_blocks=(0,), rsn_dim=8)
m = NativeModel(cfg); exporter_drvm(m, sys.argv[1]); open(sys.argv[2], "w").write(str(m.nb_parametres()))
print(f"  {m.nb_parametres()} paramètres")
PY
PORT=${PORT:-$((64000 + RANDOM % 1500))}
"$D" --drvm-serve "$T/m.drvm" "$PORT" > "$T/srv.log" 2>&1 & SRV=$!
for _ in $(seq 1 80); do grep -q 'drvm-serve' "$T/srv.log" 2>/dev/null && break; kill -0 $SRV 2>/dev/null || { cat "$T/srv.log"; exit 2; }; sleep 0.2; done
SANTE=$("$PY" - "$PORT" <<'PY'
import json, sys, urllib.request
with urllib.request.urlopen(f"http://127.0.0.1:{sys.argv[1]}/sante", timeout=10) as r:
    print(json.load(r)["parametres"])
PY
)
[ "$SANTE" = "$(cat "$T/params")" ] || { echo "  ❌ /sante : $SANTE"; exit 1; }
echo "  ✅ /sante $SANTE"

gen() { "$PY" - "$PORT" "$1" <<'PY'
import json, sys, urllib.request
req = urllib.request.Request(f"http://127.0.0.1:{sys.argv[1]}/generer?n=12&profondeur=1&seuil={sys.argv[2]}",
                             data=b"abc", method="POST")
with urllib.request.urlopen(req, timeout=20) as r:
    d = json.loads(r.read().decode("utf-8", "replace"), strict=False)
print(json.dumps({"a": d["choix_anticipe"], "c": d["choix_complet"], "t": d["texte"]}, ensure_ascii=False))
PY
}

echo "=== 2. seuil 0 : tout anticipé ; seuil 1 : tout plein ==="
S0=$(gen 0); S1=$(gen 1)
python3 - "$S0" "$S1" <<'PY' || exit 1
import json, sys
a, b = json.loads(sys.argv[1]), json.loads(sys.argv[2])
if (a["a"], a["c"]) != (12, 0): sys.exit(f"  ❌ seuil 0 : {a['a']}/{a['c']}")
if (b["a"], b["c"]) != (0, 12): sys.exit(f"  ❌ seuil 1 : {b['a']}/{b['c']}")
if a["t"] == b["t"]: sys.exit("  ❌ les deux chemins donnent le même texte")
print("  ✅ seuil 0 : 12/0 · seuil 1 : 0/12 · textes différents")
PY

echo "=== 3. seuil 0,01 : décision mixte, déterministe ==="
S01=$(gen 0.01); S01B=$(gen 0.01)
[ "$S01" = "$S01B" ] || { echo "  ❌ le seuil 0,01 n'est pas déterministe : $S01 vs $S01B"; exit 1; }
python3 - "$S01" <<'PY' || exit 1
import json, sys
d = json.loads(sys.argv[1])
if (d["a"], d["c"]) != (11, 1): sys.exit(f"  ❌ seuil 0,01 : {d['a']}/{d['c']} (attendu 11/1)")
print("  ✅ seuil 0,01 : 11 anticipés / 1 plein, déterministe")
PY
echo "PORTE TENUE : décision à seuil comptée · 0/1 aux extrêmes · mixte à 0,01 · déterministe"
