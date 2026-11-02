#!/usr/bin/env python3
"""eval_longueurs.py — la courbe de longueur d'un point de contrôle (absolu ou RoPE).

Le mètre est celui de N2 (`work/n2j/evalue_canal.py`) : canal fourni, fenêtres Van der Corput
dans des chunks de 8192 octets, 8 lots × 16 fenêtres. On peut demander n'importe quelle
longueur, y compris **1 000 octets** (la porte R1.1).

Usage :
  PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/eval_longueurs.py <point.pt> \
      --longueurs 128,256,512,1000 [--rope] [--val data/wiki_fr/propre]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "work/n2j")

import torch  # noqa: E402

from tools.eval_n2_propre import charge, charger_bytes  # noqa: E402
import evalue_canal as ec  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("point")
    ap.add_argument("--longueurs", default="128,256,512")
    ap.add_argument("--rope", action="store_true")
    ap.add_argument("--val", default="data/wiki_fr/propre")
    ap.add_argument("--sortie", default=None)
    a = ap.parse_args()

    if a.rope:
        from work.n2ac.rope_model import charge_rope
        m = charge_rope(a.point)
    else:
        m = charge(a.point)

    val = charger_bytes(f"{a.val}/val.txt")
    ct = torch.tensor(list(pathlib.Path(f"{a.val}/val.canal").read_bytes()), dtype=torch.long)
    res = {"fichier": pathlib.Path(a.point).name, "val": a.val,
           "positions": "rope" if a.rope else "absolues"}
    for L in [int(x) for x in a.longueurs.split(",")]:
        res[f"L{L}"] = ec.ppl(m, val, ct, L, avec_canal=True)
        print(f"  L{L} : {res[f'L{L}']}", flush=True)
    print(json.dumps(res, ensure_ascii=False), flush=True)
    if a.sortie:
        pathlib.Path(a.sortie).write_text(
            json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
