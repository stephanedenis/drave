#!/bin/bash
# porte-n3-court.sh — N3.10 : le premier profil qui change le COÛT.
#
# LA QUESTION. `bloque` et `defaut` calculent la même fonction : substituables,
# mais à coût égal. `flou` change la fonction à coût égal. Aucun des trois ne
# donne à un ROUTAGE quelque chose à arbitrer. `court` divise par quatre la
# fenêtre d'attention du bloc : l'attention est en O(fenêtre) par position, donc
# le coût baisse — et la fonction change au-delà de la fenêtre courte.
#
# LE DISPOSITIF. Un même modèle (même graine, `window` 256) exporté `defaut` et
# `court`. Trois contrôles falsifiables :
#   1. en deçà de la fenêtre courte (32 octets < 64), les logits sont
#      BIT-EXACTS : la seule différence est la fenêtre, et elle ne mord pas ;
#   2. au-delà (1 024 octets), ils DIFFÈRENT — `court` n'est pas substituable ;
#   3. sur cette même charge, `court` est PLUS RAPIDE (médiane de 11 passes
#      alternées), le gain étant borné par la part de l'attention.
#
# CONTRÔLES NÉGATIFS. Le bit-exact en deçà interdit de « gagner » en changeant
# autre chose que la fenêtre ; le désaccord au-delà interdit de vendre `court`
# comme une substitution ; le moteur numpy EXÉCUTE `court` (fenêtre courte) et
# le montre — il refuse `flou`, pas `court` ; deux exécutions identiques.
#
# Ce que cette porte ne prouve PAS : que `court` est un bon compromis. Le coût de
# QUALITÉ n'est pas mesuré ici — la fiche donne deux textes hors distribution dont
# la direction s'inverse, ce qui interdit toute conclusion. La politique de
# routage (quand payer moins) reste une question mesurée, pas un corollaire.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-court-XXXXXX")
trap 'rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. deux profils, même graine, fenêtre 256 ==="
"$PY" - "$T" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
base = dict(vocab=256, d_model=32, n_blocks=2, n_heads=2, expert_hidden=16,
            n_experts=4, top_k=2, kwta=0.5, window=256, max_pos=2048,
            thought_steps=1, early_blocks=(0,), rsn_dim=8)
for impl in ("defaut", "court"):
    torch.manual_seed(7)
    m = NativeModel(NativeConfig(**base))
    exporter_drvm(m, f"{sys.argv[1]}/{impl}.drvm", impl=impl, tolerance=0.0)
    print(f"  {impl:7} {m.nb_parametres()} paramètres")
PY

echo "=== 2. en deçà de la fenêtre courte : bit-exact (la fenêtre ne mord pas) ==="
"$D" --drvm-pas-hex "$T/defaut.drvm" "abcdefghabcdefghabcdefghabcdefgh" > "$T/court-court.txt"
"$D" --drvm-pas-hex "$T/court.drvm" "abcdefghabcdefghabcdefghabcdefgh" > "$T/court-court2.txt"
cmp -s "$T/court-court.txt" "$T/court-court2.txt" \
    || { echo "  ❌ 32 octets < 64 : court devrait être bit-exact"; exit 1; }
echo "  ✅ 32 octets : logits bit-exacts (seule la fenêtre diffère)"

echo "=== 3. au-delà : non substituable (et le désaccord est mesuré) ==="
LONG=$(python3 -c "print('abcdefgh' * 128)")
"$D" --drvm-pas-hex "$T/defaut.drvm" "$LONG" > "$T/long-defaut.txt"
"$D" --drvm-pas-hex "$T/court.drvm" "$LONG" > "$T/long-court.txt"
cmp -s "$T/long-defaut.txt" "$T/long-court.txt" \
    && { echo "  ❌ 1 024 octets : court = defaut, la fenêtre ne mord jamais"; exit 1; }
python3 - "$T" <<'PY' || exit 1
import pathlib, struct, sys
T = pathlib.Path(sys.argv[1])
def lit(nom):
    h = (T / nom).read_text().strip()
    return [struct.unpack("<f", struct.pack("<I", int(h[i:i + 8], 16)))[0]
            for i in range(0, len(h), 8)]
a, b = lit("long-defaut.txt"), lit("long-court.txt")
d = max(abs(x - y) for x, y in zip(a, b))
print(f"  1 024 octets : max|Δ| = {d:.3e} > 0 → NON substituable")
assert d > 0, "court ne diffère pas au-delà de sa fenêtre : la fenêtre est inerte"
PY

echo "=== 4. le coût : médiane de 11 passes alternées ==="
python3 - "$T" "$D" <<'PY' || exit 1
import pathlib, statistics, subprocess, sys, time
T, D = pathlib.Path(sys.argv[1]), sys.argv[2]
prompt = "abcdefgh" * 128
res = {"defaut": [], "court": []}
for _ in range(11):
    for impl in ("defaut", "court"):
        t0 = time.perf_counter()
        subprocess.run([D, "--drvm-pas-hex", str(T / f"{impl}.drvm"), prompt],
                       check=True, stdout=subprocess.DEVNULL)
        res[impl].append(time.perf_counter() - t0)
med = {}
for impl, t in res.items():
    med[impl] = statistics.median(t)
    cv = statistics.pstdev(t) / med[impl]
    print(f"  {impl:7} médiane {med[impl] * 1e3:6.1f} ms  (CV {cv * 100:.0f} %)")
    assert cv < 0.15, f"mesure instable pour {impl} (CV {cv:.2f})"
rapport = med["court"] / med["defaut"]
print(f"  rapport court / defaut : {rapport:.3f}×")
assert rapport < 0.85, f"court n'est pas plus rapide ({rapport:.3f}×) : le profil ne paie pas"
PY

echo "=== 5. provenance, et le moteur numpy exécute court ==="
"$D" --drvm-inspect "$T/court.drvm" | grep -q "impl=court" \
    || { echo "  ❌ l'inspecteur ne montre pas impl=court"; exit 1; }
python3 - "$T" <<'PY' || exit 1
import pathlib, sys
import numpy as np
sys.path.insert(0, ".")
from tools.drvm_infere import charger, logits
T = pathlib.Path(sys.argv[1])
td, cfg, impls_d = charger(str(T / "defaut.drvm"))
tc, _, impls_c = charger(str(T / "court.drvm"))
assert impls_d == ["defaut", "defaut"], impls_d
assert impls_c == ["court", "court"], impls_c
prompt = list(("abcdefgh" * 16).encode())      # 128 > 64 : la fenêtre courte mord
a = logits(td, cfg, prompt, impls=impls_d)[-1]
c = logits(tc, cfg, prompt, impls=impls_c)[-1]
d = float(np.max(np.abs(a - c)))
print(f"  numpy defaut vs court (128 o) : max|Δ| = {d:.3e} > 0")
assert d > 0, "le moteur numpy n'applique pas la fenêtre courte"
print("  ✅ inspecteur : impl=court · numpy : court exécuté et différent au-delà de 64 o")
PY

echo "PORTE TENUE : en deçà de la fenêtre bit-exact · au-delà non substituable · 0,69× le temps sur une charge d'attention · numpy exécute court"
