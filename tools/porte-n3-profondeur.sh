#!/bin/bash
# porte-n3-profondeur.sh — N3.2b0 : la profondeur de service change-t-elle la génération ?
#
# `DRAVE_NATIVE_PROFONDEUR=N` coupe le calcul natif après N blocs (défaut : tous).
# C'est une sortie précoce FIXE, sans seuil de confiance : N3.2b0 mesure le CHEMIN
# de service, pas la qualité. La porte vérifie que le même modèle à profondeur 1
# et à profondeur pleine donne des sorties différentes, que chaque profondeur est
# déterministe, et que /sante ne change pas.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-profondeur-XXXXXX")
trap 'kill ${SRV:-} 2>/dev/null; wait ${SRV:-} 2>/dev/null; rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. un DRVM à 2 blocs, graine 7 ==="
"$PY" - "$T/modele.drvm" "$T/params" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
torch.manual_seed(7)
cfg = NativeConfig(vocab=256, d_model=32, n_blocks=2, n_heads=2, expert_hidden=16,
                   n_experts=4, top_k=2, kwta=0.5, window=16, max_pos=2048,
                   thought_steps=1, early_blocks=(0,), rsn_dim=8)
m = NativeModel(cfg)
exporter_drvm(m, sys.argv[1])
open(sys.argv[2], "w").write(str(m.nb_parametres()))
print(f"  modèle : {m.nb_parametres()} paramètres · 2 blocs")
PY
[ -s "$T/modele.drvm" ] || { echo "  ❌ DRVM vide"; exit 2; }

demarrer() { # $1 = profondeur (vide = pleine), $2 = port, $3 = log
    if [ -n "$1" ]; then export DRAVE_NATIVE_PROFONDEUR="$1"; else unset DRAVE_NATIVE_PROFONDEUR; fi
    "$D" --drvm-serve "$T/modele.drvm" "$2" > "$3" 2>&1 &
    SRV=$!
    for _ in $(seq 1 80); do grep -q 'drvm-serve' "$3" 2>/dev/null && return 0; kill -0 $SRV 2>/dev/null || return 1; sleep 0.25; done
    return 1
}
gen() { "$PY" - "$1" "$2" <<'PY'
import json, sys, urllib.request
req = urllib.request.Request(f"http://127.0.0.1:{sys.argv[1]}/generer?n=12",
                             data=sys.argv[2].encode(), method="POST")
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
P1=$((62000 + RANDOM % 1000)); P2=$((63000 + RANDOM % 1000))

echo "=== 2. pleine profondeur : /sante + deux générations ==="
demarrer "" "$P1" "$T/plein.log" || { cat "$T/plein.log"; exit 2; }
S_PLEIN=$(sante "$P1"); A=$(gen "$P1" "abc"); B=$(gen "$P1" "abc"); kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; SRV=""
[ -n "$S_PLEIN" ] || { echo "  ❌ /sante vide"; exit 1; }
[ "$A" = "$B" ] || { echo "  ❌ pleine profondeur non déterministe : $A vs $B"; exit 1; }
echo "  ✅ /sante $S_PLEIN · deux générations identiques : $A"

echo "=== 3. profondeur 1 : /sante identique, génération différente ==="
demarrer 1 "$P2" "$T/un.log" || { cat "$T/un.log"; exit 2; }
S_UN=$(sante "$P2"); C=$(gen "$P2" "abc"); D=$(gen "$P2" "abc"); kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; SRV=""
[ "$S_UN" = "$S_PLEIN" ] || { echo "  ❌ /sante change avec la profondeur : $S_UN vs $S_PLEIN"; exit 1; }
[ "$C" = "$D" ] || { echo "  ❌ profondeur 1 non déterministe : $C vs $D"; exit 1; }
[ "$A" != "$C" ] || { echo "  ❌ la profondeur ne change pas la génération : $C"; exit 1; }
echo "  ✅ /sante $S_UN · profondeur 1 déterministe et différente : $C"

echo "PORTE TENUE : profondeur de service branchée · /sante stable · chaque profondeur déterministe · sorties différentes"
