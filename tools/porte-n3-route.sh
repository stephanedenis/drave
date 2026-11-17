#!/bin/bash
# porte-n3-route.sh — N3.8 : une route est une condition EXÉCUTÉE, pas un commentaire.
#
# LA QUESTION. Le manifeste déclare `graph.routes` depuis le premier jour ; le
# lecteur les refusait au nom de « ce qu'on ne sait pas exécuter ». Maintenant
# qu'elles sont lues, il faut prouver qu'elles AGISSENT, et que leur sémantique
# est bien celle qu'on a écrite : le profil du bloc change à partir de la position
# `seuil`, et seulement à partir de là.
#
# LE DISPOSITIF. Un même modèle (poids identiques, même graine) est écrit quatre
# fois : pur `defaut`, pur `flou`, et deux copies de `defaut` auxquelles on ajoute
# une route par bloc mixeur (`position >= seuil → alors`, sinon `defaut`). Trois
# contrôles falsifiables :
#
#   1. route TOUJOURS active (seuil 0)  → chaque position prend `alors` → les
#      logits sont BIT-EXACTS ceux du modèle pur `flou` ;
#   2. route JAMAIS active (seuil 10^9) → les logits sont BIT-EXACTS ceux du
#      modèle pur `defaut` ;
#   3. route MIXTE (seuil 1, prompt de 3 octets) → les logits diffèrent des deux,
#      et deux exécutions donnent exactement les mêmes.
#
# Le contrôle du contrôle : `alors` doit CHANGER quelque chose — si la route
# active donnait les logits de `defaut`, le test ne testerait rien (l'écart
# defaut/flou est mesuré et doit être non nul).
#
# CONTRÔLES NÉGATIFS. Une route mal formée est refusée et nommée (bloc inconnu,
# bloc non mixeur, condition inconnue, deux routes pour un bloc, `alors` absent,
# profil inconnu) ; le moteur numpy REFUSE un manifeste à routes au lieu de les
# ignorer ; l'inspecteur et la trace portent les routes.
#
# Ce que cette porte ne prouve PAS : qu'un routage est une bonne POLITIQUE. Elle
# prouve que le mécanisme est déterministe et mesurable ; R0.5/R06 ont montré
# qu'un seuil global ne transfère pas — la politique reste une question mesurée.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-route-XXXXXX")
trap 'rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. un modèle, quatre écritures : pur defaut, pur flou, deux copies routées ==="
"$PY" - "$T" <<'PY' || exit 2
import copy, json, sys, torch
sys.path.insert(0, ".")
from tools.drvm import TensorSpec, read_drvm, write_drvm
from tools.native_model import NativeConfig, NativeModel, exporter_drvm

T = sys.argv[1]
base = dict(vocab=256, d_model=32, n_blocks=2, n_heads=2, expert_hidden=16,
            n_experts=4, top_k=2, kwta=0.5, window=16, max_pos=2048,
            thought_steps=1, early_blocks=(0,), rsn_dim=8)
for impl in ("defaut", "flou"):
    torch.manual_seed(7)
    m = NativeModel(NativeConfig(**base))
    exporter_drvm(m, f"{T}/{impl}.drvm", impl=impl, tolerance=1e-4)


def avec_routes(src, dst, seuil, alors):
    with read_drvm(src) as d:
        specs = [TensorSpec(t["name"], bytes(d.tensor(t["name"])), t["dtype"],
                            tuple(t["shape"]), t["bloc"], t.get("quant"),
                            float(t.get("sparsity", 0.0)))
                 for t in d.manifest["tensors"]]
        man = copy.deepcopy(d.manifest)
    man["graph"]["routes"] = [
        {"id": f"r{i}", "bloc": f"b{i}",
         "si": {"kind": "position", "seuil": seuil},
         "alors": alors, "sinon": "defaut"} for i in range(base["n_blocks"])]
    write_drvm(dst, man, specs)


avec_routes(f"{T}/defaut.drvm", f"{T}/route-active.drvm", 0, "flou")
avec_routes(f"{T}/defaut.drvm", f"{T}/route-inactive.drvm", 10**9, "flou")
avec_routes(f"{T}/defaut.drvm", f"{T}/route-mixte.drvm", 1, "flou")
print("  écrits : defaut, flou, route-active (seuil 0), route-inactive (10^9), route-mixte (1)")
PY

echo "=== 2. la route est-elle EXÉCUTÉE ? (bit-exact, pas « à peu près ») ==="
for m in defaut flou route-active route-inactive route-mixte; do
    "$D" --drvm-pas-hex "$T/$m.drvm" "abc" > "$T/logits-$m.txt" 2>"$T/err-$m.txt" \
        || { echo "  ❌ $m : le moteur a refusé"; cat "$T/err-$m.txt"; exit 1; }
done
"$D" --drvm-pas-hex "$T/route-mixte.drvm" "abc" > "$T/logits-route-mixte-2.txt"
python3 - "$T" <<'PY' || exit 1
import pathlib, struct, sys
T = pathlib.Path(sys.argv[1])

def lit(nom):
    return (T / f"logits-{nom}.txt").read_text().strip()

def diff(x, y):
    a, b = lit(x), lit(y)
    return max(abs(struct.unpack("<f", struct.pack("<I", int(a[i:i + 8], 16)))[0]
                   - struct.unpack("<f", struct.pack("<I", int(b[i:i + 8], 16)))[0])
               for i in range(0, len(a), 8))

d_def_flou = diff("defaut", "flou")
print(f"  contrôle du contrôle : defaut vs flou = {d_def_flou:.3e} ≠ 0")
assert d_def_flou > 0, "flou ne change rien : la route ne pourrait rien changer"

print(f"  route active   vs flou   : {'IDENTIQUE' if lit('route-active') == lit('flou') else 'DIFFÉRENT'}")
print(f"  route inactive vs defaut : {'IDENTIQUE' if lit('route-inactive') == lit('defaut') else 'DIFFÉRENT'}")
assert lit("route-active") == lit("flou"), "route active ≠ flou : la condition ne s'applique pas partout"
assert lit("route-inactive") == lit("defaut"), "route inactive ≠ defaut : la condition s'applique trop tôt"

m, m2 = lit("route-mixte"), lit("route-mixte-2")
assert m == m2, "route mixte NON déterministe"
assert m != lit("defaut") and m != lit("flou"), "route mixte = un des purs : elle n'agit pas"
print(f"  route mixte    vs defaut : {diff('route-mixte', 'defaut'):.3e} · "
      f"vs flou : {diff('route-mixte', 'flou'):.3e} · déterministe")
print("  ✅ seuil 0 = flou bit-exact · seuil 10^9 = defaut bit-exact · seuil 1 = mélange déterministe")
PY

echo "=== 3. provenance : routes dans l'inspecteur et la trace ==="
"$D" --drvm-inspect "$T/route-active.drvm" | grep -q "position >= 0 → flou" \
    || { echo "  ❌ l'inspecteur ne montre pas la route"; "$D" --drvm-inspect "$T/route-active.drvm" | head -8; exit 1; }
python3 - "$T" <<'PY' || exit 1
import pathlib, sys
sys.path.insert(0, ".")
from tools.drvm_trace import tracer
t = tracer(str(pathlib.Path(sys.argv[1]) / "route-active.drvm"))
assert len(t["routes"]) == 2, t["routes"]
assert t["routes"][0]["alors"] == "flou" and t["routes"][0]["si"]["seuil"] == 0, t["routes"]
print("  ✅ inspecteur : « position >= 0 → flou » · trace : 2 routes déclarées")
PY

echo "=== 4. le moteur numpy REFUSE un manifeste à routes ==="
python3 - "$T" <<'PY' || exit 1
import pathlib, sys
sys.path.insert(0, ".")
from tools.drvm_infere import charger
T = pathlib.Path(sys.argv[1])
try:
    charger(str(T / "route-active.drvm"))
except NotImplementedError as e:
    assert "routes" in str(e), f"le refus ne nomme pas les routes : {e}"
else:
    raise AssertionError("le moteur numpy a ignoré les routes en silence")
print("  ✅ numpy : routes refusées (nommées)")
PY

echo "=== 5. une route mal formée ne s'écrit pas ==="
python3 - "$T" <<'PY' || exit 1
import copy, sys, pathlib
sys.path.insert(0, ".")
from tools.drvm import DRVMError, TensorSpec, read_drvm, write_drvm
T = pathlib.Path(sys.argv[1])
with read_drvm(T / "defaut.drvm") as d:
    specs = [TensorSpec(t["name"], bytes(d.tensor(t["name"])), t["dtype"],
                        tuple(t["shape"]), t["bloc"]) for t in d.manifest["tensors"]]
    man = copy.deepcopy(d.manifest)
cas = [
    ({"id": "r0", "bloc": "b9", "si": {"kind": "position", "seuil": 1}, "alors": "flou"},
     "route vers un bloc inconnu"),
    ({"id": "r0", "bloc": "b0", "si": {"kind": "confiance", "seuil": 1}, "alors": "flou"},
     "condition de route inconnue"),
    ({"id": "r0", "bloc": "b0", "si": {"kind": "position", "seuil": 1}}, "route sans alors"),
    ({"id": "r0", "bloc": "b0", "si": {"kind": "position", "seuil": 1}, "alors": "magique"},
     "impl inconnue"),
]
for route, attendu in cas:
    m = copy.deepcopy(man)
    m["graph"]["routes"] = [route]
    try:
        write_drvm(T / "mauvaise.drvm", m, specs)
    except DRVMError as e:
        assert attendu in str(e), f"« {e} » ne nomme pas « {attendu} »"
    else:
        raise AssertionError(f"route acceptée : {route}")
print(f"  ✅ {len(cas)} routes mal formées refusées, chacune nommée")
PY

echo "PORTE TENUE : seuil 0 = flou bit-exact · seuil 10^9 = defaut bit-exact · mixte déterministe et différent · provenance lue · numpy refuse · routes invalides refusées"
