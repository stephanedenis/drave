#!/bin/bash
# porte-n3-service.sh — N3.2a : le service natif (`--drvm-serve`) répond-il, et le même
# modèle donne-t-il la même génération que le chemin CLI ?
#
# LA QUESTION. N3 demande que les briques natives tournent **dans le moteur**, pas seulement
# dans un outil. Le service `--drvm-serve` est le chemin de production ; cette porte le fait
# tourner sur un DRVM **reproductible** (petit modèle généré par `tools/native_model.py`,
# graine fixe), vérifie `/sante`, deux générations identiques, une génération différente pour
# un autre prompt, et un 404. Elle ne prétend pas tester la sortie précoce (le service ne
# l'a pas encore) : c'est N3.2a, le service et le routage/k-WTA du modèle natif.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
PORT=${PORT:-$((61000 + RANDOM % 2000))}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-service-XXXXXX")
trap 'kill ${SRV:-} 2>/dev/null; wait ${SRV:-} 2>/dev/null; rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent : construire d'abord"; exit 2; }
[ -x "$PY" ] || { echo "  ❌ $PY absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. le DRVM reproductible (graine 7, 1 bloc, 4 experts top-2) ==="
"$PY" - "$T/modele.drvm" "$T/params" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
torch.manual_seed(7)
cfg = NativeConfig(vocab=256, d_model=32, n_blocks=1, n_heads=2, expert_hidden=16,
                   n_experts=4, top_k=2, kwta=0.5, window=16, max_pos=2048,
                   thought_steps=1, early_blocks=(0,), rsn_dim=8)
m = NativeModel(cfg)
exporter_drvm(m, sys.argv[1])
open(sys.argv[2], "w").write(str(m.nb_parametres()))
print(f"  modèle : {m.nb_parametres()} paramètres · {sys.argv[1]}")
PY
[ -s "$T/modele.drvm" ] || { echo "  ❌ DRVM vide"; exit 2; }

echo "=== 2. le service démarre et /sante répond ==="
"$D" --drvm-serve "$T/modele.drvm" "$PORT" > "$T/srv.log" 2>&1 &
SRV=$!
for _ in $(seq 1 80); do grep -q 'drvm-serve' "$T/srv.log" 2>/dev/null && break; kill -0 $SRV 2>/dev/null || { cat "$T/srv.log"; exit 2; }; sleep 0.25; done
grep -q 'drvm-serve' "$T/srv.log" || { echo "  ❌ le service n'écoute pas"; cat "$T/srv.log"; exit 2; }
SANTE=$("$PY" - "$PORT" <<'PY'
import json, sys, urllib.request
with urllib.request.urlopen(f"http://127.0.0.1:{sys.argv[1]}/sante", timeout=10) as r:
    print(json.load(r)["parametres"])
PY
)
ATTENDU=$(cat "$T/params")
[ "$SANTE" = "$ATTENDU" ] || { echo "  ❌ /sante : $SANTE paramètres (attendu $ATTENDU)"; exit 1; }
echo "  ✅ /sante : $SANTE paramètres, identiques au modèle"

echo "=== 3. deux générations identiques, un autre prompt différent ==="
gen() { "$PY" - "$PORT" "$1" <<'PY'
import json, sys, urllib.request
req = urllib.request.Request(f"http://127.0.0.1:{sys.argv[1]}/generer?n=8",
                             data=sys.argv[2].encode(), method="POST")
with urllib.request.urlopen(req, timeout=20) as r:
    d = json.loads(r.read().decode("utf-8", "replace"), strict=False)
print(json.dumps({"octets": d["octets"], "texte": d["texte"]}, ensure_ascii=False))
PY
}
A=$(gen "abc"); B=$(gen "abc"); C=$(gen "zzz")
[ "$A" = "$B" ] || { echo "  ❌ deux générations identiques diffèrent : $A vs $B"; exit 1; }
echo "  ✅ deux générations « abc » identiques : $A"
[ "$A" != "$C" ] || { echo "  ❌ un autre prompt donne la même sortie : $C"; exit 1; }
echo "  ✅ prompt « zzz » différent : $C"

echo "=== 4. le 404 est un refus, pas une génération ==="
CODE=$("$PY" - "$PORT" <<'PY'
import sys, urllib.request, urllib.error
try:
    urllib.request.urlopen(f"http://127.0.0.1:{sys.argv[1]}/inconnu", timeout=5)
    print(200)
except urllib.error.HTTPError as e:
    print(e.code)
PY
)
[ "$CODE" = "404" ] || { echo "  ❌ /inconnu rend $CODE au lieu de 404"; exit 1; }
echo "  ✅ /inconnu : 404"

echo "PORTE TENUE : service natif vivant · /sante exact · génération déterministe · 404"
