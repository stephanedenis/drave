#!/usr/bin/env python3
"""agrege_fenetre.py — assemble `reports/n2-fenetre.json` depuis les sorties de work/n2ac/.

Usage :
  python3 work/n2ac/agrege_fenetre.py [--sortie reports/n2-fenetre.json]
"""
from __future__ import annotations

import argparse
import json
import pathlib

WORK = pathlib.Path("work/n2ac")

SOURCES = {
    # la loi de la fenêtre, à octets constants (wiki_fr)
    "loi_fenetre_256": "courbe-rope.json",
    "loi_fenetre_512": "courbe-rope512-5k.json",
    "loi_fenetre_1024": "eval-rope1024-2.5k.json",
    "loi_fenetre_1024_20k": "eval-rope1024-20k.json",
    # même texte, contexte 256→2 000
    "meme_texte_256": "queue-rope256-2000.json",
    "meme_texte_512": "queue-rope512-2000.json",
    "meme_texte_1024": "queue-rope1024.json",
    # production
    "production_n2ac": "eval-mix60.json",
    "production_200k": "eval-mix200.json",
    "production_512": "eval-mix512-15k.json",
    "production_512_meme_texte": "queue-mix512.json",
    "production_1024": "eval-mix1024-7.5k.json",
    "production_1024_meme_texte": "queue-mix1024.json",
    # miroir de copie
    "miroir_1024": "miroir-rope1024-2.5k.json",
    "miroir_production_512": "miroir-mix512-15k.json",
    "miroir_256": "miroir-rope.json",
    "miroir_512": "miroir-rope512.json",
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default="reports/n2-fenetre.json")
    a = ap.parse_args()
    out = {}
    for cle, nom in SOURCES.items():
        p = WORK / nom
        if p.exists():
            out[cle] = json.loads(p.read_text(encoding="utf-8"))
    out["dispositif"] = {
        "modele": "drave-n0 34,3 M (384/512), RoPE",
        "recette": "lot 8, lr 3e-4, graine 1, canal ; seq = fenêtre",
        "runs": {
            "R1.1": "wiki_fr, 128/256, 20 000 pas, 20,5 Mo, init base-wiki-45m",
            "R1.2-512": "wiki_fr, 512/512, 5 000 pas, 20,5 Mo, init base-wiki-45m",
            "R1.2-1024": "wiki_fr, 1 024/1 024, 2 500 pas, 20,5 Mo, init base-wiki-45m",
            "R1.2-1024-long": "wiki_fr, 1 024/1 024, +17 500 pas (20 000), 164 Mo",
            "prod-512": "wiki_mix, 512/512, 15 000 pas, 61,4 Mo, init mix-60k (N2.ac)",
            "prod-1024": "wiki_mix, 1 024/1 024, 7 500 pas, 61,4 Mo, init mix-60k (N2.ac)",
        },
        "controles": [
            "même texte à contexte 256/512/1 000/2 000 (eval_fenetre)",
            "miroir de copie à distance (miroir_copie)",
            "témoins repassés dans le même mètre : N2.ac et 200 k redonnent leurs fiches",
        ],
    }
    p = pathlib.Path(a.sortie)
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"  {p} · {len(out) - 1} source(s)")


if __name__ == "__main__":
    main()
