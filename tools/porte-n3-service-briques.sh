#!/bin/bash
# porte-n3-service-briques.sh — N3.6 : pont, placement et seuil composent-ils DANS LE SERVICE ?
#
# POURQUOI CETTE PORTE EXISTE. N3.4a compose service + profondeur + routage +
# comptage, mais sa propre en-tête dit qu'elle ne couvre « ni le seuil de
# confiance ni le pont/placement ». N3.4b a prouvé le pont par `--drvm-generate` ;
# N3.4c a prouvé que `placement` est une métadonnée inerte ; N3.2b1 décide par
# seuil mais calcule les DEUX chemins. Ici, les trois passent par le chemin réel
# de production, `--drvm-serve`.
#
# Ce que la porte vérifie :
#   1. A (pont normal) est DÉTERMINISTE dans le service ;
#   2. B (pont nul, mêmes poids) change la sortie → le pont AGIT dans le service ;
#   3. C (placement=remote, mêmes poids) ne change rien → le placement reste une
#      MÉTADONNÉE (condition N3.4c, rejouée ici) ;
#   4. le seuil 0/1 compte 12/0 et 0/12, et les deux textes diffèrent ;
#   5. un seuil mixte est DÉTERMINISTE (le rejeu redonne la même décision).
#
# Ce qu'elle ne prouve PAS : le saut de calcul. N3.2b2 a nommé la condition —
# les deux chemins sont calculés ; la profondeur 1 change le contenu parce que
# les couches sautées ne fournissent plus leurs K/V. Cette porte mesure la
# composition, pas un gain de temps qui n'existe pas encore.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-service-briques-XXXXXX")
trap 'kill ${SRV:-} 2>/dev/null; wait ${SRV:-} 2>/dev/null; rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent : construire d'abord"; exit 2; }
[ -x "$PY" ] || { echo "  ❌ $PY absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. les modèles : A pont normal, B pont nul, C placement distant, T seuil ==="
"$PY" - "$T" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
t = sys.argv[1]
base4 = dict(vocab=256, d_model=64, n_blocks=4, n_heads=4, expert_hidden=32,
             n_experts=4, top_k=2, kwta=0.5, window=32, max_pos=2048,
             thought_steps=1, early_blocks=(1,), rsn_dim=8)
torch.manual_seed(7); a = NativeModel(NativeConfig(**base4)); exporter_drvm(a, t + "/a.drvm", "local")
torch.manual_seed(7); b = NativeModel(NativeConfig(**base4))
zero = 0
for nom, p in b.state_dict().items():
    if "bridge" in nom:
        p.zero_(); zero += p.numel()
exporter_drvm(b, t + "/b.drvm", "local")
torch.manual_seed(7); c = NativeModel(NativeConfig(**base4)); exporter_drvm(c, t + "/c.drvm", "remote")
base2 = dict(vocab=256, d_model=32, n_blocks=2, n_heads=2, expert_hidden=16,
             n_experts=4, top_k=2, kwta=0.5, window=16, max_pos=2048,
             thought_steps=1, early_blocks=(0,), rsn_dim=8)
torch.manual_seed(7); m = NativeModel(NativeConfig(**base2)); exporter_drvm(m, t + "/t.drvm", "local")
print(f"  A/B/C : {a.nb_parametres()} paramètres (4 blocs, pont nul = {zero} poids)")
print(f"  T : {m.nb_parametres()} paramètres (2 blocs, seuil)")
PY

demarrer() { # $1 modèle, $2 port, $3 log
    "$D" --drvm-serve "$1" "$2" > "$3" 2>&1 &
    SRV=$!
    for _ in $(seq 1 100); do
        grep -q 'drvm-serve' "$3" 2>/dev/null && return 0
        kill -0 "$SRV" 2>/dev/null || { cat "$3"; return 1; }
        sleep 0.2
    done
    return 1
}
arreter() { kill ${SRV:-} 2>/dev/null; wait ${SRV:-} 2>/dev/null; SRV=""; }

gen() { # $1 port, $2 seuil (vide = plein)
    "$PY" - "$1" "${2:-}" <<'PY'
import json, sys, urllib.request
port, seuil = sys.argv[1], sys.argv[2]
q = f"http://127.0.0.1:{port}/generer?n=12"
if seuil:
    q += f"&profondeur=1&seuil={seuil}"
req = urllib.request.Request(q, data=b"abc", method="POST")
with urllib.request.urlopen(req, timeout=20) as r:
    d = json.loads(r.read().decode("utf-8", "replace"), strict=False)
print(json.dumps({"a": d.get("choix_anticipe", 0), "c": d.get("choix_complet", 0),
                  "t": d["texte"], "ms": round(float(d.get("ms", 0)), 2)}, ensure_ascii=False))
PY
}

identique() {
    python3 - "$1" "$2" <<'PY'
import json, sys
a, b = json.loads(sys.argv[1]), json.loads(sys.argv[2])
if (a["a"], a["c"], a["t"]) != (b["a"], b["c"], b["t"]):
    sys.exit(1)
PY
}

P1=$((62000 + RANDOM % 500)); P2=$((63000 + RANDOM % 500))
P3=$((64000 + RANDOM % 500)); P4=$((65000 + RANDOM % 500))

echo "=== 2. A (pont normal) est déterministe dans le service ==="
demarrer "$T/a.drvm" "$P1" "$T/a.log" || { echo "  ❌ service A"; exit 2; }
A1=$(gen "$P1"); A2=$(gen "$P1")
identique "$A1" "$A2" || { echo "  ❌ A n'est pas déterministe"; exit 1; }
echo "  ✅ A identique"
arreter

echo "=== 3. le pont nul change la sortie dans le service ==="
demarrer "$T/b.drvm" "$P2" "$T/b.log" || { echo "  ❌ service B"; exit 2; }
B1=$(gen "$P2")
python3 - "$A1" "$B1" <<'PY' || { echo "  ❌ le pont nul ne change rien : le pont est inerte dans le service"; exit 1; }
import json, sys
a, b = json.loads(sys.argv[1]), json.loads(sys.argv[2])
if a["t"] == b["t"]:
    sys.exit(1)
PY
echo "  ✅ pont nul : A et B diffèrent"
arreter

echo "=== 4. placement=remote : même sortie que local (métadonnée) ==="
demarrer "$T/c.drvm" "$P3" "$T/c.log" || { echo "  ❌ service C"; exit 2; }
C1=$(gen "$P3")
python3 - "$A1" "$C1" <<'PY' || { echo "  ❌ le placement change la sortie : un chemin distribué existe"; exit 1; }
import json, sys
a, c = json.loads(sys.argv[1]), json.loads(sys.argv[2])
if a["t"] != c["t"]:
    sys.exit(1)
PY
echo "  ✅ local et remote : même sortie — le placement est une métadonnée"
arreter

echo "=== 5. la décision à seuil compose : 0 → 12/0, 1 → 0/12 ==="
demarrer "$T/t.drvm" "$P4" "$T/t.log" || { echo "  ❌ service T"; exit 2; }
S0=$(gen "$P4" 0); S1=$(gen "$P4" 1)
python3 - "$S0" "$S1" <<'PY' || { echo "  ❌ la décision à seuil ne compose pas"; exit 1; }
import json, sys
a, b = json.loads(sys.argv[1]), json.loads(sys.argv[2])
if (a["a"], a["c"]) != (12, 0):
    sys.exit(f"seuil 0 : {a['a']}/{a['c']}")
if (b["a"], b["c"]) != (0, 12):
    sys.exit(f"seuil 1 : {b['a']}/{b['c']}")
if a["t"] == b["t"]:
    sys.exit("les deux chemins donnent le même texte")
PY
echo "  ✅ seuil 0 : 12/0 · seuil 1 : 0/12 · textes différents"

echo "=== 6. rejeu : un seuil mixte redonne la même décision ==="
S01=$(gen "$P4" 0.01); S01B=$(gen "$P4" 0.01)
python3 - "$S01" "$S01B" <<'PY' || { echo "  ❌ le seuil 0,01 n'est pas déterministe"; exit 1; }
import json, sys
a, b = json.loads(sys.argv[1]), json.loads(sys.argv[2])
if (a["a"], a["c"], a["t"]) != (b["a"], b["c"], b["t"]):
    sys.exit(1)
if not (0 < a["a"] < 12):
    sys.exit(f"seuil 0,01 : {a['a']}/12 (pas de mixte)")
PY
echo "  ✅ seuil 0,01 : $(python3 -c 'import json,sys; d=json.loads(sys.argv[1]); print(str(d["a"])+"/"+str(d["c"]))' "$S01") · rejeu identique"
arreter

echo "PORTE TENUE : pont actif dans le service · placement métadonnée · décision à seuil 12/0 vs 0/12 · rejeu déterministe"
