#!/usr/bin/env python3
"""eval_production.py — un point de contrôle sur les deux validations, à toutes les longueurs.

Étend `eval_200k.py` (qui s'arrête à 512) aux contextes longs et aux modèles RoPE : la même
mesure, avec le canal, sur les deux validations appariées (français et grand corpus), à
128 / 256 / 512 / 1 000 / 2 000 octets, plus le panneau hors domaine à 128 et le contrôle par
permutation.

`--rope` charge le modèle avec `work.n2ac.rope_model.charge_rope` ; sans, c'est le natif absolu.

Usage :
  PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/eval_production.py <point.pt> \
      [--rope] [--longueurs 128,256,512,1000,2000] [--sortie x.json]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "work/n2j")

import torch  # noqa: E402

from tools.eval_n2_propre import charge, charger_bytes, ordre_vdc  # noqa: E402
from tools.canal_structure import canal as canal_de  # noqa: E402
import evalue_canal as ec  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("point")
    ap.add_argument("--rope", action="store_true")
    ap.add_argument("--longueurs", default="128,256,512,1000,2000")
    ap.add_argument("--sortie", default=None)
    a = ap.parse_args()

    if a.rope:
        from work.n2ac.rope_model import charge_rope
        m = charge_rope(a.point)
    else:
        m = charge(a.point)
    res = {"fichier": pathlib.Path(a.point).name, "params": m.nb_parametres(),
           "positions": "rope" if a.rope else "absolues", "ppl": {}}
    longueurs = [int(x) for x in a.longueurs.split(",")]
    for nom, d in (("val_fr", "data/wiki_fr/propre"), ("val_big", "data/wiki_big/propre")):
        val = charger_bytes(f"{d}/val.txt")
        ct = torch.tensor(list(pathlib.Path(f"{d}/val.canal").read_bytes()), dtype=torch.long)
        res["ppl"][nom] = {str(L): ec.ppl(m, val, ct, L, avec_canal=True) for L in longueurs}
        if nom == "val_fr":
            n = 4_000_000
            perm = torch.tensor(ordre_vdc(n), dtype=torch.long)
            res["permute_fr"] = ec.ppl(m, val[:n][perm], ct[:n][perm], 128, avec_canal=True)
        del val, ct
        torch.cuda.empty_cache()
    for nom, chemin in (("litterature", "data/corpus_fr_litterature.txt"),
                        ("anglais", "data/corpus_en.txt"),
                        ("wikitext2", "data/wikitext2_test.txt"),
                        ("corpus_propre", "data/corpus_propre/val.txt")):
        texte = pathlib.Path(chemin).read_text(encoding="utf-8", errors="replace")
        data = charger_bytes(chemin)
        ct = torch.tensor(list(canal_de(texte)), dtype=torch.long)
        res[nom] = ec.ppl(m, data, ct, 128, avec_canal=True)
        del data, ct
        torch.cuda.empty_cache()
    print(json.dumps(res, ensure_ascii=False, indent=1), flush=True)
    if a.sortie:
        pathlib.Path(a.sortie).write_text(
            json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
