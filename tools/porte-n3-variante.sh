#!/bin/bash
# porte-n3-variante.sh — N3.7 : la SUBSTITUTION d'implémentation est un contrat.
#
# LA QUESTION. Un bloc peut avoir plusieurs implémentations (neuronal, heuristique,
# flou). Peut-on les déclarer et les remplacer sans mentir ? Oui, à une condition :
# distinguer deux choses que l'on confond tout le temps.
#
#   1. SUBSTITUTION — même fonction, autre algorithme. `bloque` calcule le même
#      produit matrice-vecteur que `defaut`, en tuilant la somme sur quatre
#      accumulateurs : autre ordre d'addition, mêmes logits à l'arrondi f32 près.
#      Elle doit être INDIFFÉRENTE dans la tolérance déclarée par le manifeste
#      (`contrat.tolerance`). C'est le théorème d'indifférence, mesuré.
#
#   2. ROUTAGE — autre fonction, même signature. `flou` remplace le seuil net du
#      k-WTA par une appartenance sigmoïde. Ce n'est PAS une substitution : elle
#      DOIT échouer le test d'indifférence. Sinon le test ne teste rien, et une
#      variante dégradée se ferait passer pour la même fonction.
#
# CONTRÔLES NÉGATIFS. Le contrôle « flou doit échouer » est le contrôle du test
# lui-même ; une `impl` inconnue est refusée à l'écriture ET à la lecture ; le
# moteur numpy REFUSE les profils qu'il n'implémente pas au lieu de les ignorer ;
# la provenance (`impl`, tolérance) est lisible dans l'inspecteur et la trace ; le
# coût est chronométré, avec un garde-fou de stabilité (CV < 50 %).
#
# Ce que cette porte ne prouve PAS : que `bloque` est plus rapide (le rapport est
# imprimé, pas promis), ni que `flou` est un bon choix de routage (c'est R0.5/R06,
# et leur réponse est négative pour un seuil global).
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-variante-XXXXXX")
trap 'rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. trois profils, les MÊMES poids (même graine), un contrat déclaré ==="
"$PY" - "$T" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
base = dict(vocab=256, d_model=32, n_blocks=2, n_heads=2, expert_hidden=16,
            n_experts=4, top_k=2, kwta=0.5, window=16, max_pos=2048,
            thought_steps=1, early_blocks=(0,), rsn_dim=8)
for impl in ("defaut", "bloque", "flou"):
    torch.manual_seed(7)
    m = NativeModel(NativeConfig(**base))
    exporter_drvm(m, f"{sys.argv[1]}/{impl}.drvm", impl=impl, tolerance=1e-4)
    print(f"  {impl:7} {m.nb_parametres()} paramètres")
PY

echo "=== 2. le même pas, trois profils : ce que la tolérance déclare ==="
for impl in defaut bloque flou; do
    "$D" --drvm-pas-hex "$T/$impl.drvm" "abc" > "$T/logits-$impl.txt" 2>"$T/err-$impl.txt" \
        || { echo "  ❌ $impl : le moteur a refusé"; cat "$T/err-$impl.txt"; exit 1; }
done
TOL=1e-4
python3 - "$T" "$TOL" <<'PY' || exit 1
import struct, sys, pathlib
T, tol = pathlib.Path(sys.argv[1]), float(sys.argv[2])

def lit(nom):
    h = (T / nom).read_text().strip()
    return [struct.unpack("<f", struct.pack("<I", int(h[i:i + 8], 16)))[0]
            for i in range(0, len(h), 8)]

def ecart(x, y):
    return max(abs(u - v) for u, v in zip(x, y))

a, b, c = lit("logits-defaut.txt"), lit("logits-bloque.txt"), lit("logits-flou.txt")
assert len(a) == len(b) == len(c) == 256, "vecteur de logits inattendu"
d_sub, d_aut = ecart(a, b), ecart(a, c)   # substitution · autre fonction
print(f"  tolérance déclarée (contrat) : {tol:g}")
print(f"  defaut vs bloque : max|Δ| = {d_sub:.3e}  → "
      f"{'INDIFFÉRENT' if d_sub <= tol else 'NON INDIFFÉRENT'}")
print(f"  defaut vs flou   : max|Δ| = {d_aut:.3e}  → "
      f"{'INDIFFÉRENT' if d_aut <= tol else 'NON INDIFFÉRENT'}")
assert d_sub <= tol, "bloque n'est pas substituable : la porte ne peut pas tenir"
assert d_aut > tol, "contrôle négatif INERTE : flou passe l'indifférence, le test ne teste rien"
print("  ✅ substitution indifférente · contrôle négatif vivant (flou échoue)")
PY

echo "=== 3. provenance : le profil est dans le manifeste, donc dans le hash ==="
"$D" --drvm-inspect "$T/bloque.drvm" | grep -q "impl=bloque" \
    || { echo "  ❌ l'inspecteur ne montre pas impl=bloque"; exit 1; }
"$D" --drvm-inspect "$T/defaut.drvm" | grep -q "impl=defaut" \
    || { echo "  ❌ l'inspecteur ne montre pas impl=defaut"; exit 1; }
python3 - "$T" <<'PY' || exit 1
import pathlib, sys
sys.path.insert(0, ".")
from tools.drvm_trace import tracer
t = tracer(str(pathlib.Path(sys.argv[1]) / "bloque.drvm"))
assert [x["impl"] for x in t["impls"]] == ["bloque", "bloque"], t["impls"]
assert t["impls"][0]["tolerance"] == 1e-4, t["impls"]
print("  ✅ inspecteur et trace portent impl=bloque, tol=1e-4")
PY

echo "=== 4. le moteur numpy REFUSE ce qu'il n'implémente pas ==="
python3 - "$T" <<'PY' || exit 1
import pathlib, sys
sys.path.insert(0, ".")
from tools.drvm_infere import charger
T = pathlib.Path(sys.argv[1])
_, cfg = charger(str(T / "defaut.drvm"))        # contrôle positif : defaut passe
assert cfg["n_blocks"] == 2
for impl in ("bloque", "flou"):
    try:
        charger(str(T / f"{impl}.drvm"))
    except NotImplementedError as e:
        assert impl in str(e), f"le refus ne nomme pas {impl} : {e}"
    else:
        raise AssertionError(f"le moteur numpy a accepté {impl} en silence")
print("  ✅ defaut exécuté · bloque et flou refusés (nommés)")
PY

echo "=== 5. coût du même pas, chronométré (le chiffre, pas la promesse) ==="
python3 - "$T" "$D" <<'PY' || exit 1
import pathlib, statistics, subprocess, sys, time
T, D = pathlib.Path(sys.argv[1]), sys.argv[2]
prompt = "abcdefgh" * 256        # 2 048 octets : le calcul domine le démarrage
res = {}
for impl in ("defaut", "bloque"):
    temps = []
    for _ in range(7):
        t0 = time.perf_counter()
        subprocess.run([D, "--drvm-pas-hex", str(T / f"{impl}.drvm"), prompt],
                       check=True, stdout=subprocess.DEVNULL)
        temps.append(time.perf_counter() - t0)
    res[impl] = statistics.median(temps)
    cv = statistics.pstdev(temps) / max(res[impl], 1e-9)
    print(f"  {impl:7} médiane {res[impl] * 1e3:6.1f} ms  (CV {cv * 100:.0f} %)")
    assert cv < 0.5, f"mesure instable pour {impl} (CV {cv:.2f})"
print(f"  rapport bloque / defaut : {res['bloque'] / res['defaut']:.2f}×")
PY

echo "=== 6. une impl inconnue ne s'écrit pas (donc ne se lit pas) ==="
python3 - "$T" <<'PY' || exit 1
import pathlib, sys
sys.path.insert(0, ".")
import tools.drvm as d
T = pathlib.Path(sys.argv[1])
man = {"format": "DRVM", "version": 0, "model": {"name": "t"},
       "graph": {"blocks": [{"id": "b0", "kind": "local_mixer", "inputs": [], "outputs": [],
                             "impl": "magique", "contrat": {"version": 0, "tolerance": 0.0}}],
                 "regions": [], "routes": [], "heads": [], "thought": None, "bridge": None},
       "execution": {"activation": "DRVF", "placement": "local"}}
try:
    d.write_drvm(T / "magique.drvm", man, [d.TensorSpec("b0.w", b"\1\2\3\4", bloc="b0")])
except d.DRVMError as e:
    assert "impl inconnue" in str(e), e
else:
    raise AssertionError("écriture acceptée avec impl=magique")
print("  ✅ impl inconnue refusée à l'écriture")
PY

echo "PORTE TENUE : substitution indifférente dans le contrat · contrôle négatif vivant · provenance lue · numpy refuse ce qu'il n'exécute pas · coût chronométré"
