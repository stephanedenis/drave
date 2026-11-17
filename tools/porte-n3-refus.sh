#!/bin/bash
# porte-n3-refus.sh — N3.5d : le protocole REFUSE un aval qui n'a pas le même modèle.
#
# 2ᵉ partie (17/11) — le LECTEUR DRVM refuse ce qu'il n'exécute pas. Le format
# déclarait `routes`, `regions`, `heads`, `thought`, `bridge` et les ignorait en
# silence : une clé inconnue, une région/tête/pont vers un bloc absent, une route
# mal formée (bloc inconnu ou non mixeur, condition inconnue, deux routes pour un
# bloc, `alors` absent) sont maintenant refusés, nommés, par les DEUX lecteurs
# (Python et Rust). Une route VALIDE, elle, s'écrit et se lit — c'est le moteur qui
# l'exécute (porte-n3-route). Contrôle négatif : le DRVM valide doit passer, une
# route valide doit s'écrire, et les DRVM déjà sur le disque restent lisibles.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-refus-XXXXXX")
trap 'kill ${SRV:-} 2>/dev/null; wait ${SRV:-} 2>/dev/null; rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. modèles A (normal) et B (pont nul) ==="
"$PY" - "$T" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
base = dict(vocab=256, d_model=64, n_blocks=4, n_heads=4, expert_hidden=32,
            n_experts=4, top_k=2, kwta=0.5, window=32, max_pos=2048,
            thought_steps=1, early_blocks=(1,), rsn_dim=8)
torch.manual_seed(7); a = NativeModel(NativeConfig(**base)); exporter_drvm(a, sys.argv[1] + "/a.drvm")
torch.manual_seed(7); b = NativeModel(NativeConfig(**base))
for nom, p in b.state_dict().items():
    if "bridge" in nom: p.zero_()
exporter_drvm(b, sys.argv[1] + "/b.drvm")
print(f"  A/B : {a.nb_parametres()} paramètres")
PY
PORT=$((64000 + RANDOM % 1200))
"$D" --drvm-serve-aval "$T/b.drvm" 2 "$PORT" > "$T/srv.log" 2>&1 & SRV=$!
for _ in $(seq 1 80); do grep -q 'drvm-serve-aval' "$T/srv.log" 2>/dev/null && break; kill -0 $SRV 2>/dev/null || { cat "$T/srv.log"; exit 2; }; sleep 0.2; done

echo "=== 2. client A contre aval B : REFUS ==="
set +e
OUT=$("$D" --drvm-split-net "$T/a.drvm" 2 abc "127.0.0.1:$PORT" 2>&1); CODE=$?
set +e
[ "$CODE" = "4" ] || { echo "  ❌ code $CODE au lieu de 4 : $OUT"; exit 1; }
printf '%s\n' "$OUT" | grep -q "REFUS" || { echo "  ❌ pas de REFUS : $OUT"; exit 1; }
echo "  ✅ REFUS (code 4) sans logits"
kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; SRV=""

echo "=== 3. client A contre aval A : succès ==="
PORT=$((65200 + RANDOM % 300))
"$D" --drvm-serve-aval "$T/a.drvm" 2 "$PORT" > "$T/srv.log" 2>&1 & SRV=$!
for _ in $(seq 1 80); do grep -q 'drvm-serve-aval' "$T/srv.log" 2>/dev/null && break; kill -0 $SRV 2>/dev/null || { cat "$T/srv.log"; exit 2; }; sleep 0.2; done
H=$("$D" --drvm-pas-hex "$T/a.drvm" abc 2>/dev/null)
S=$("$D" --drvm-split-net "$T/a.drvm" 2 abc "127.0.0.1:$PORT" 2>/dev/null)
[ "$S" = "$H" ] || { echo "  ❌ succès non bit-exact"; exit 1; }
echo "  ✅ succès bit-exact"

echo "=== 4. le manifeste : le lecteur REFUSE ce qu'il n'exécute pas ==="
python3 - "$T" <<'PY' || exit 2
import glob, hashlib, json, pathlib, sys
sys.path.insert(0, ".")
import tools.drvm as d

T = pathlib.Path(sys.argv[1])


def entete(manifeste, payload=b"\x01\x02\x03\x04"):
    """Écrit un DRVM brut (en-tête + manifeste + payload), sans passer par _valide."""
    mj = d._canonique(manifeste)
    mj_pad = mj + b"\0" * (d._aligne(len(mj)) - len(mj))
    poff = d.HEADER.size + len(mj_pad)
    total = poff + len(payload)
    return d.HEADER.pack(d.MAGIC, d.VERSION, d.HEADER.size, len(mj), poff, total,
                         hashlib.sha256(mj).digest(),
                         hashlib.sha256(payload).digest()) + mj_pad + payload


def valide():
    return {"format": "DRVM", "version": 0, "model": {"name": "t"},
            "graph": {"blocks": [{"id": "b0", "kind": "input",
                                  "inputs": [], "outputs": []}],
                      "regions": [{"id": "r0", "blocks": ["b0"]}],
                      "routes": [], "heads": [], "thought": None, "bridge": None},
            "tensors": [{"name": "b0.w", "bloc": "b0", "dtype": "f32", "shape": [1],
                         "offset": 0, "nbytes": 4, "quant": None, "sparsity": 0.0}],
            "execution": {"activation": "DRVF", "placement": "local"}}


cas = {}


def _mixeur():
    m = valide()
    m["graph"]["blocks"][0]["kind"] = "local_mixer"
    return m


def ajoute(nom, attendu, muter, base=valide):
    m = base()
    muter(m)
    (T / f"{nom}.drvm").write_bytes(entete(m))
    cas[nom] = attendu


def _route_bloc(m):   m["graph"]["routes"] = [{"id": "r0", "bloc": "b1",
                                                "si": {"kind": "position", "seuil": 1}, "alors": "flou"}]
def _route_cond(m):   m["graph"]["routes"] = [{"id": "r0", "bloc": "b0",
                                                "si": {"kind": "confiance", "seuil": 1}, "alors": "flou"}]
def _route_double(m): m["graph"]["routes"] = [
    {"id": "r0", "bloc": "b0", "si": {"kind": "position", "seuil": 1}, "alors": "flou"},
    {"id": "r1", "bloc": "b0", "si": {"kind": "position", "seuil": 2}, "alors": "bloque"}]
def _route_alors(m):  m["graph"]["routes"] = [{"id": "r0", "bloc": "b0",
                                                "si": {"kind": "position", "seuil": 1}}]
def _graphe(m): m["graph"]["quota"] = 1
def _bloc(m):   m["graph"]["blocks"][0]["poids"] = 1
def _region(m): m["graph"]["regions"][0]["blocks"] = ["b1"]
def _tete(m):   m["graph"]["heads"] = ["b1"]
def _pont(m):   m["graph"]["bridge"] = "b1"
def _pensee(m): m["graph"]["thought"] = {"steps": -1}
def _sans(m):   del m["graph"]["thought"]
def _exec(m):   m["execution"]["regime"] = "eager"
def _racine(m): m["inconnue"] = 1


# les routes se jugent sur un bloc MIXEUR : un bloc `input` n'en accepte pas
ajoute("route_bloc",   "route vers un bloc inconnu : b1", _route_bloc, base=_mixeur)
ajoute("route_cond",   "condition de route inconnue : confiance", _route_cond, base=_mixeur)
ajoute("route_double", "deux routes pour le bloc : b0", _route_double, base=_mixeur)
ajoute("route_alors",  "route sans alors : r0", _route_alors, base=_mixeur)
ajoute("graphe", "clé inconnue dans graph : quota", _graphe)
ajoute("bloc",   "clé inconnue dans un bloc : poids", _bloc)
ajoute("region", "région vers un bloc inconnu : b1", _region)
ajoute("tete",   "tête vers un bloc inconnu : b1", _tete)
ajoute("pont",   "pont vers un bloc inconnu : b1", _pont)
ajoute("pensee", "thought.steps invalide", _pensee)
ajoute("sans",   "clé absente : graph.thought", _sans)
ajoute("exec",   "clé inconnue dans execution : regime", _exec)
ajoute("racine", "clé inconnue dans le manifeste : inconnue", _racine)

(T / "valide.drvm").write_bytes(entete(valide()))
with d.read_drvm(T / "valide.drvm") as v:
    assert v.manifest["model"]["name"] == "t", "le DRVM valide ne se lit pas"

for nom, attendu in cas.items():
    try:
        d.read_drvm(T / f"{nom}.drvm")
    except d.DRVMError as e:
        assert attendu in str(e), f"{nom} : « {e} » ne nomme pas « {attendu} »"
    else:
        raise AssertionError(f"{nom} : le lecteur Python a accepté ce qu'il n'exécute pas")

# L'écriture est le miroir de la lecture : une route VALIDE s'écrit, une route
# mal formée ne s'écrit pas (un manifeste ne peut pas naître menteur).
man = _mixeur()
man["graph"]["routes"] = [{"id": "r0", "bloc": "b0",
                           "si": {"kind": "position", "seuil": 1}, "alors": "flou"}]
d.write_drvm(T / "ecrit-route.drvm", man,
             [d.TensorSpec("b0.w", b"\x01\x02\x03\x04", bloc="b0")])
with d.read_drvm(T / "ecrit-route.drvm") as v:
    assert v.manifest["graph"]["routes"][0]["alors"] == "flou", "route perdue à l'écriture"
man = _mixeur()
man["graph"]["routes"] = [{"id": "r0", "bloc": "b9",
                           "si": {"kind": "position", "seuil": 1}, "alors": "flou"}]
try:
    d.write_drvm(T / "ecrit-faux.drvm", man,
                 [d.TensorSpec("b0.w", b"\x01\x02\x03\x04", bloc="b0")])
except d.DRVMError as e:
    assert "route vers un bloc inconnu" in str(e), e
else:
    raise AssertionError("écriture acceptée avec une route vers un bloc inconnu")

# Non-régression : les DRVM déjà sur le disque restent lisibles (dont la fixture).
fixture = pathlib.Path("drave-core/tests/fixtures/tiny_n0.drvm")
assert fixture.exists(), "fixture absente"
with d.read_drvm(fixture, verifier=False):
    pass
n = 0
for f in glob.glob("**/*.drvm", recursive=True):
    with d.read_drvm(f, verifier=False):
        n += 1

(T / "cas.json").write_text(json.dumps(cas))
print(f"  Python : {len(cas)} refus nommés · valide lu · route valide écrite · "
      f"route fausse refusée · {n} DRVM existants relus")
PY

"$D" --drvm-inspect "$T/valide.drvm" >/dev/null 2>&1 || { echo "  ❌ le DRVM valide est refusé par le lecteur Rust"; exit 1; }
while IFS=$'\t' read -r nom attendu; do
    OUT=$("$D" --drvm-inspect "$T/$nom.drvm" 2>&1); CODE=$?
    [ "$CODE" = "3" ] || { echo "  ❌ $nom : code $CODE au lieu de 3 : $OUT"; exit 1; }
    printf '%s' "$OUT" | grep -Fq -- "$attendu" || { echo "  ❌ $nom : « $OUT » ne nomme pas « $attendu »"; exit 1; }
done < <(python3 -c "import json;[print(k,v,sep='\t') for k,v in json.load(open('$T/cas.json')).items()]")
N=$(python3 -c "import json;print(len(json.load(open('$T/cas.json'))))")
echo "  ✅ Rust : $N refus nommés (code 3) · le valide passe"

echo "PORTE TENUE : empreinte refusée (code 4) · même modèle bit-exact · manifeste refusé ($N cas, deux lecteurs)"
