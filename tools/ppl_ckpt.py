#!/usr/bin/env python3
"""ppl_ckpt.py — la perplexité d'un checkpoint sur un val, tout le val.

POURQUOI. Le 19/11, les deux 142 M (corpus v1 et v2) ont été comparés sur le val de
v1 : le val est v1-centré, et la conclusion « v1 meilleur » peut être un artefact de
distribution. Cet outil mesure **n'importe quel checkpoint** sur **n'importe quel
val**, en lisant l'architecture dans le checkpoint (pas d'arguments de taille à
retenir) et en couvrant tout le fichier (n_lots calculé, pas 8 lots par défaut).

Usage :
  python3 tools/ppl_ckpt.py --modele work/n4/v211.pt --val data/wikitext2_test.txt \
      --device cuda:0 --sortie reports/ppl-wikitext2.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import torch  # noqa: E402

from tools.entrainer_native import charger, ppl  # noqa: E402
from tools.native_model import NativeConfig, NativeModel  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", required=True)
    ap.add_argument("--val", required=True)
    ap.add_argument("--seq", type=int, default=1024)
    ap.add_argument("--lot", type=int, default=8)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--sortie", default="")
    a = ap.parse_args()

    ck = torch.load(a.modele, map_location="cpu", weights_only=False)
    cfg = ck["config"]
    modele = NativeModel(NativeConfig(d_model=cfg["d_model"],
                                      expert_hidden=cfg["expert_hidden"])).to(a.device)
    modele.load_state_dict(ck["state"], strict=False)
    val = charger(a.val)
    n_lots = max(1, len(val) // (a.lot * a.seq))          # tout le val, pas un échantillon
    p, n = ppl(modele, val, a.seq, a.lot, a.device, n_lots=n_lots)
    res = {"modele": a.modele, "parametres": modele.nb_parametres(),
           "val": a.val, "octets_val": len(val), "seq": a.seq, "lot": a.lot,
           "n_lots": n_lots, "jetons": n, "ppl": p}
    print(json.dumps(res, ensure_ascii=False, indent=1))
    if a.sortie:
        pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
