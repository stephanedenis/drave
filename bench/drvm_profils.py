#!/usr/bin/env python3
"""bench/drvm_profils.py — le catalogue de profils sur un modèle ENTRAÎNÉ.

LA QUESTION. Les portes N3.7–N3.10 mesurent les profils sur un `drave-n0`
synthétique : la sémantique et le coût, pas la qualité. Ici on prend un modèle
**entraîné** (34 M, fenêtre 1 024) et on mesure, pour chaque profil, la
**perplexité** et le **temps** de la même passe.

CE QUE LE CONTRÔLE DOIT MONTRER.
- `bloque` (même fonction, autre ordre de somme) : la perplexité doit être
  IDENTIQUE à `defaut` — c'est le théorème d'indifférence sur un vrai modèle.
- `flou` (seuil net → appartenance sigmoïde) : la perplexité doit DIFFÉRER — un
  autre corps, donc un autre modèle.
- `court` (fenêtre / 4) : ce que coûte (ou non) de couper la fenêtre.

Usage :
  python3 bench/drvm_profils.py --drvm work/n2ac/mix1024-60k.drvm \\
      --texte data/corpus_mixte.txt --limite 2048 --sortie reports/profils-34m.json
"""
from __future__ import annotations

import argparse
import copy
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import time

RACINE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
from tools.drvm import TensorSpec, read_drvm, write_drvm  # noqa: E402

D = RACINE / "drave-core/target/release/drave"
PPL = re.compile(r"PPL native ([0-9.]+) sur (\d+) octets")


def _reecrit(drvm: str, impl: str, dest: pathlib.Path) -> None:
    """Le même modèle, tous ses blocs mixeurs portant le profil `impl`."""
    with read_drvm(drvm) as d:
        specs = [TensorSpec(t["name"], bytes(d.tensor(t["name"])), t["dtype"],
                            tuple(t["shape"]), t["bloc"], t.get("quant"),
                            float(t.get("sparsity", 0.0)))
                 for t in d.manifest["tensors"]]
        man = copy.deepcopy(d.manifest)
    for b in man["graph"]["blocks"]:
        if b["kind"] == "local_mixer":
            b["impl"] = impl
            b["contrat"] = {"version": 0, "tolerance": 0.0}
    write_drvm(dest, man, specs)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--drvm", required=True)
    ap.add_argument("--texte", required=True)
    ap.add_argument("--limite", type=int, default=2048)
    ap.add_argument("--impls", default="defaut,bloque,flou,court")
    ap.add_argument("--sortie", default="")
    a = ap.parse_args()
    assert D.exists(), f"{D} absent : cargo build --release"
    with read_drvm(a.drvm) as d:
        man = d.manifest
        arg = man["model"]["architecture"]
        params = man["model"].get("parametres", 0)
    print(f"modèle : {a.drvm} · {params} paramètres · d_model {arg['d_model']} · "
          f"{arg['n_blocks']} blocs · fenêtre {arg['window']}")
    print(f"texte  : {a.texte} ({a.limite} octets)")

    resultats = {}
    for impl in a.impls.split(","):
        impl = impl.strip()
        with tempfile.TemporaryDirectory() as td:
            if impl == "defaut":
                chemin = pathlib.Path(a.drvm)   # le manifeste d'origine n'a pas d'`impl`
            else:
                chemin = pathlib.Path(td) / f"{impl}.drvm"
                _reecrit(a.drvm, impl, chemin)
            t0 = time.perf_counter()
            out = subprocess.run([str(D), "--drvm-native-ppl", str(chemin),
                                  f"@{a.texte}", str(a.limite)],
                                 capture_output=True, text=True, check=True).stdout
            temps = time.perf_counter() - t0
        m = PPL.search(out)
        assert m, out
        resultats[impl] = {"ppl": float(m.group(1)), "octets": int(m.group(2)), "s": temps}
        print(f"  {impl:7} PPL {m.group(1):>9} sur {m.group(2)} octets  "
              f"({temps:6.1f} s, chargement du modèle inclus)")

    ref = resultats["defaut"]["ppl"]
    for impl, r in resultats.items():
        r["delta_pct"] = (r["ppl"] / ref - 1.0) * 100.0
    if a.sortie:
        pathlib.Path(a.sortie).write_text(json.dumps(
            {"schema": "drave.profils-modele", "version": 1, "drvm": a.drvm,
             "texte": a.texte, "limite": a.limite, "resultats": resultats},
            indent=1, ensure_ascii=False))
        print(f"  écrit : {a.sortie}")


if __name__ == "__main__":
    main()
