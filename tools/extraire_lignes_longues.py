#!/usr/bin/env python3
"""extraire_lignes_longues.py — le corpus « long-forme » : les lignes qui portent du texte.

POURQUOI. Le 19/11, la décomposition de la sélection a montré que `wiki_big` (lignes de
407 o) généralise mieux que le plein texte fragmenté (108 o/ligne) et que les résumés.
Le recollement de *toutes* les lignes a échoué (7,75 contre 7,43) : joindre des titres et
des listes fabrique de fausses phrases. Cette extraction prend l'autre chemin — **garder
les lignes déjà longues** (les paragraphes) et jeter le reste, sans rien recoller.

Usage :
  python3 tools/extraire_lignes_longues.py --entree data/wiki_mix_v2/train.txt \
      --sortie work/long/train.txt --min 200 --json work/long/extraction.json
  python3 tools/extraire_lignes_longues.py --autotest
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys


def autotest() -> int:
    lignes = ["court\n", "x" * 250 + "\n", "moyen\n", "y" * 300 + "\n"]
    gardees = [l for l in lignes if len(l.rstrip("\n")) >= 200]
    if len(gardees) != 2:
        print(f"  ❌ autotest : {len(gardees)} gardées au lieu de 2")
        return 1
    print("  ✅ autotest : 2 lignes longues gardées, 2 courtes jetées")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--entree", default="")
    ap.add_argument("--sortie", default="")
    ap.add_argument("--min", type=int, default=200)
    ap.add_argument("--json", default="")
    ap.add_argument("--autotest", action="store_true")
    a = ap.parse_args()
    if a.autotest:
        sys.exit(autotest())
    if not a.entree or not a.sortie:
        ap.error("--entree et --sortie sont requis (sauf --autotest)")
    src = pathlib.Path(a.entree)
    dst = pathlib.Path(a.sortie)
    dst.parent.mkdir(parents=True, exist_ok=True)
    lignes_in = lignes_out = octets_in = octets_out = 0
    with src.open("r", encoding="utf-8", errors="replace") as f, dst.open("w", encoding="utf-8") as g:
        for ligne in f:
            lignes_in += 1
            l = ligne.rstrip("\n")
            if len(l) >= a.min:
                g.write(l + "\n")
                lignes_out += 1
                octets_out += len(l.encode("utf-8")) + 1
    octets_in = src.stat().st_size
    res = {"entree": str(src), "sortie": str(dst), "min": a.min,
           "lignes_in": lignes_in, "lignes_out": lignes_out,
           "octets_in": octets_in, "octets_out": octets_out,
           "pct_octets_gardes": round(100 * octets_out / max(1, octets_in), 2),
           "octets_par_ligne": round(octets_out / max(1, lignes_out), 1)}
    print(json.dumps(res, ensure_ascii=False, indent=1))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
