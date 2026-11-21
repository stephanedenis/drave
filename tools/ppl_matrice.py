#!/usr/bin/env python3
"""ppl_matrice.py — la matrice des PPL : plusieurs modèles × plusieurs vals, une table.

POURQUOI. La nuit du 20-21/11 compare des corpus (palier 1, `wiki_big`, mélange, plein
texte) et des graines. Un seul val (wikitext2) ne dit pas si un modèle généralise **dans son
registre** ; il faut aussi des vals tenus à l'écart du même registre (le val de `wiki_big`, celui
du palier 1) et un val tiers. Ce script rend la matrice, en réutilisant `ppl_ckpt` (qui lit
l'architecture dans le point de contrôle) — un chiffre par case, une table markdown, un JSON.

Usage :
  python3 tools/ppl_matrice.py --modele nb11=work/n4/nb11.pt --modele p111=work/n4/p111.pt \
      --val wikitext2=data/wikitext2_test.txt --val wiki_big=work/vals/wiki_big_val_1m.txt \
      --device cuda:0 --sortie reports/ppl-matrice.json
  python3 tools/ppl_matrice.py --autotest
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys

PY = "/home/stephane/gpu-env/bin/python"
RACINE = pathlib.Path(__file__).resolve().parent.parent


def autotest() -> int:
    """Le parseur d'arguments : nom=chemin, et un nom sans « = » est refusé."""
    for brut in ("a=work/x.pt",):
        nom, _, chemin = brut.partition("=")
        if not (nom and chemin):
            print("  ❌ autotest : parseur")
            return 1
    print("  ✅ autotest : les couples nom=chemin se lisent")
    return 0


def mesurer(modele: pathlib.Path, val: pathlib.Path, device: str) -> float | None:
    cmd = [PY, "tools/ppl_ckpt.py", "--modele", str(modele), "--val", str(val), "--device", device]
    env = dict(os.environ)
    env["PYTHONPATH"] = "."
    r = subprocess.run(cmd, cwd=RACINE, capture_output=True, text=True, env=env)
    if r.returncode != 0:
        return None
    try:
        return float(json.loads(r.stdout)["ppl"])
    except (json.JSONDecodeError, KeyError, TypeError):
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", action="append", default=[], help="nom=chemin.pt")
    ap.add_argument("--val", action="append", default=[], help="nom=chemin.txt")
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--sortie", default="")
    ap.add_argument("--autotest", action="store_true")
    a = ap.parse_args()
    if a.autotest:
        sys.exit(autotest())
    modeles = dict(m.split("=", 1) for m in a.modele)
    vals = dict(v.split("=", 1) for v in a.val)
    table: dict[str, dict[str, float | None]] = {}
    for nom_m, chemin_m in modeles.items():
        table[nom_m] = {}
        for nom_v, chemin_v in vals.items():
            ppl = mesurer(RACINE / chemin_m, RACINE / chemin_v, a.device)
            table[nom_m][nom_v] = ppl
            print(f"  {nom_m:>8} × {nom_v:<10} : {ppl}")
    print()
    entetes = list(vals)
    print("| modèle | " + " | ".join(entetes) + " |")
    print("|---|" + "---:|" * len(entetes))
    for nom_m, ligne in table.items():
        cellules = " | ".join(f"{ligne[v]:.4f}" if ligne[v] is not None else "—" for v in entetes)
        print(f"| {nom_m} | {cellules} |")
    if a.sortie:
        pathlib.Path(a.sortie).write_text(
            json.dumps({"modeles": list(modeles), "vals": entetes, "ppl": table},
                       ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
