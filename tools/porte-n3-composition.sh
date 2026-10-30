#!/bin/bash
# porte-n3-composition.sh — N3.4a : les briques natives composent-elles sur UN modèle ?
#
# N3.2a (service), N3.2b0 (profondeur), N3.3a (routage) et N3.3c (comptage) ont
# chacun leur porte. Ici tout tourne sur les MÊMES deux modèles (A/B, mêmes poids,
# top_k différent) : le service, la profondeur 1, la génération et les compteurs.
# Ce n'est pas encore la composition avec seuil de confiance (N3.2b) ni avec le
# pont/placement ; c'est N3.4a, la composition des briques déjà branchées.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-composition-XXXXXX")
trap 'kill ${SRV:-} 2>/dev/null; wait ${SRV:-} 2>/dev/null; rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. deux modèles à 2 blocs, mêmes poids ==="
"$PY" - "$T" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
base = dict(vocab=256, d_model=32, n_blocks=2, n_heads=2, expert_hidden=16,
            n_experts=4, window=16, max_pos=2048, thought_steps=1,
            early_blocks=(0,), rsn_dim=8)
for nom, top_k in (("a", 2), ("b", 1)):
    torch.manual_seed(7)
    m = NativeModel(NativeConfig(top_k=top_k, kwta=0.5, **base))
    exporter_drvm(m, f"{sys.argv[1]}/{nom}.drvm")
    print(f"  {nom.upper()} : top_k={top_k} · {m.nb_parametres()} paramètres")
PY

demarrer() { "$D" --drvm-serve "$1" "$2" > "$3" 2>&1 & SRV=$!; for _ in $(seq 1 80); do grep -q 'drvm-serve' "$3" 2>/dev/null && return 0; kill -0 $SRV 2>/dev/null || return 1; sleep 0.2; done; return 1; }
gen() { "$PY" - "$1" "$2" <<'PY'
import json, sys, urllib.request
req = urllib.request.Request(f"http://127.0.0.1:{sys.argv[1]}/generer?n=12", data=sys.argv[2].encode(), method="POST")
with urllib.request.urlopen(req, timeout=20) as r:
    d = json.loads(r.read().decode("utf-8", "replace"), strict=False)
print(json.dumps({"octets": d["octets"], "texte": d["texte"]}, ensure_ascii=False))
PY
}
sante() { "$PY" - "$1" <<'PY'
import json, sys, urllib.request
with urllib.request.urlopen(f"http://127.0.0.1:{sys.argv[1]}/sante", timeout=10) as r:
    print(json.load(r)["parametres"])
PY
}
P1=$((64000 + RANDOM % 500)); P2=$((64500 + RANDOM % 500)); P3=$((65000 + RANDOM % 500))

echo "=== 2. A pleine : /sante + deux générations ==="
demarrer "$T/a.drvm" "$P1" "$T/a.log" || { cat "$T/a.log"; exit 2; }
S=$(sante "$P1"); A1=$(gen "$P1" "abc"); A2=$(gen "$P1" "abc"); kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; SRV=""
[ "$A1" = "$A2" ] || { echo "  ❌ A non déterministe"; exit 1; }
echo "  ✅ /sante $S · A identique : $A1"

echo "=== 3. A profondeur 1 : différente et déterministe ==="
export DRAVE_NATIVE_PROFONDEUR=1
demarrer "$T/a.drvm" "$P2" "$T/a1.log" || { cat "$T/a1.log"; exit 2; }
A3=$(gen "$P2" "abc"); A4=$(gen "$P2" "abc"); kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; SRV=""; unset DRAVE_NATIVE_PROFONDEUR
[ "$A3" = "$A4" ] || { echo "  ❌ profondeur 1 non déterministe"; exit 1; }
[ "$A1" != "$A3" ] || { echo "  ❌ profondeur 1 identique à la pleine"; exit 1; }
echo "  ✅ profondeur 1 déterministe et différente : $A3"

echo "=== 4. B (top_k=1) : différente de A ==="
demarrer "$T/b.drvm" "$P3" "$T/b.log" || { cat "$T/b.log"; exit 2; }
B1=$(gen "$P3" "abc"); kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; SRV=""
[ "$A1" != "$B1" ] || { echo "  ❌ top_k=1 identique à top_k=2"; exit 1; }
echo "  ✅ B différente : $B1"

echo "=== 5. compteurs réels des deux modèles ==="
CA=$("$D" --drvm-sparsite "$T/a.drvm" "abc" 2>/dev/null); CB=$("$D" --drvm-sparsite "$T/b.drvm" "abc" 2>/dev/null)
python3 - "$CA" "$CB" <<'PY' || exit 1
import sys
for nom, ligne, att in (("A", sys.argv[1], (6, 12, 96)), ("B", sys.argv[2], (6, 6, 48))):
    vals = tuple(int(x) for x in ligne.split() if x.isdigit())
    if vals != att:
        sys.exit(f"  ❌ {nom} : {vals} (attendu {att})")
    print(f"  ✅ {nom} : appels={vals[0]} experts={vals[1]} canaux={vals[2]}")
PY
echo "PORTE TENUE : service + profondeur + routage + comptage composés sur les mêmes modèles"
