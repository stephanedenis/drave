#!/bin/bash
# porte-n3-moteurs.sh — N3.9 : les deux moteurs du même manifeste rendent le même corps.
#
# LA QUESTION. Un DRVM a deux moteurs : le Rust (`native.rs`, le chemin de
# service, avec cache KV) et le numpy (`drvm_infere.py`, le « 0 dépendance
# lourde »). Le théorème d'indifférence ne vaut que si les deux rendent le MÊME
# corps pour les mêmes entrées : sinon « le même modèle » n'en est pas un, et
# une substitution mesurée sur un moteur ne dit rien de l'autre. La parité 4/4
# de N4 a été mesurée une fois ; rien ne la gardait.
#
# LE DISPOSITIF. Un même modèle (même graine) exporté avec les profils `defaut`,
# `bloque` et `court` ; trois exécutions : les logits du dernier pas par
# `--drvm-pas-hex` (Rust) et par `logits()` (numpy), comparés à la tolérance
# déclarée par le manifeste (`contrat.tolerance`).
#
# CONTRÔLES NÉGATIFS. (1) Le comparateur doit VOIR une différence réelle : le
# profil `flou` (autre fonction) diffère de `defaut` de 5,790e-03 > 1e-4 — s'il
# passait la tolérance, le comparateur serait aveugle. (2) Le moteur numpy refuse
# `flou` au lieu de l'ignorer. (3) Deux exécutions identiques de chaque côté : le
# déterminisme est la condition du rejeu.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-moteurs-XXXXXX")
trap 'rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. un modèle, trois profils (même graine) ==="
"$PY" - "$T" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
base = dict(vocab=256, d_model=32, n_blocks=2, n_heads=2, expert_hidden=16,
            n_experts=4, top_k=2, kwta=0.5, window=16, max_pos=2048,
            thought_steps=1, early_blocks=(0,), rsn_dim=8)
for impl in ("defaut", "bloque", "court", "flou"):
    torch.manual_seed(7)
    m = NativeModel(NativeConfig(**base))
    exporter_drvm(m, f"{sys.argv[1]}/{impl}.drvm", impl=impl, tolerance=1e-4)
    print(f"  {impl:7} {m.nb_parametres()} paramètres")
PY

echo "=== 2. Rust et numpy : les mêmes logits dans la tolérance déclarée ==="
P=$(python3 -c "print('abcdefgh' * 16)")   # 128 octets : la fenêtre courte de court mord
for m in defaut bloque court flou; do
    "$D" --drvm-pas-hex "$T/$m.drvm" "$P" > "$T/rust-$m.txt" 2>"$T/err-$m.txt" \
        || { echo "  ❌ $m : le moteur Rust a refusé"; cat "$T/err-$m.txt"; exit 1; }
done
"$D" --drvm-pas-hex "$T/defaut.drvm" "$P" > "$T/rust-defaut-2.txt"

python3 - "$T" <<'PY' || exit 1
import pathlib, struct, sys
import numpy as np
sys.path.insert(0, ".")
from tools.drvm_infere import charger, logits

T = pathlib.Path(sys.argv[1])
TOL = 1e-4


def rust(nom):
    h = (T / f"rust-{nom}.txt").read_text().strip()
    return np.array([struct.unpack("<f", struct.pack("<I", int(h[i:i + 8], 16)))[0]
                     for i in range(0, len(h), 8)], dtype=np.float32)


PROMPT = list(("abcdefgh" * 16).encode())


def numpy_logits(nom):
    t, cfg, impls = charger(str(T / f"{nom}.drvm"))
    return logits(t, cfg, PROMPT, impls=impls)[-1]


for nom in ("defaut", "bloque", "court"):
    ecart = float(np.max(np.abs(rust(nom) - numpy_logits(nom))))
    print(f"  {nom:7} Rust vs numpy : max|Δ| = {ecart:.3e}  (tolérance {TOL:g})")
    assert ecart <= TOL, f"{nom} : les deux moteurs ne rendent pas le même corps"

# Déterminisme : le rejeu exige que deux exécutions identiques le restent.
assert (T / "rust-defaut.txt").read_text() == (T / "rust-defaut-2.txt").read_text(), \
    "Rust non déterministe"
assert np.array_equal(numpy_logits("defaut"), numpy_logits("defaut")), \
    "numpy non déterministe"

# Le comparateur doit VOIR une différence réelle, sinon il est aveugle.
d_flou = float(np.max(np.abs(rust("defaut") - rust("flou"))))
print(f"  contrôle : Rust defaut vs flou = {d_flou:.3e} > {TOL:g}")
assert d_flou > TOL, "le comparateur ne voit pas une différence réelle : il est aveugle"

# Le moteur numpy refuse ce qu'il n'exécute pas.
try:
    numpy_logits("flou")
except NotImplementedError as e:
    assert "flou" in str(e), f"le refus ne nomme pas flou : {e}"
else:
    raise AssertionError("le moteur numpy a accepté flou en silence")

print("  ✅ deux moteurs d'accord (defaut, bloque, court) · déterminisme des deux côtés · "
      "comparateur non vide · numpy refuse flou")
PY

echo "PORTE TENUE : Rust et numpy rendent le même corps dans la tolérance (defaut, bloque, court) · le comparateur voit une différence réelle · les deux moteurs sont déterministes · numpy refuse ce qu'il n'exécute pas"
