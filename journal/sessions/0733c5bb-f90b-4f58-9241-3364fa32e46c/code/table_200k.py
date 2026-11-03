#!/usr/bin/env python3
"""table_200k.py — le tableau 60 k vs 200 k, généré depuis les deux JSON d'évaluation.

Aucune valeur recopiée à la main : la fiche colle la sortie de ce script. Les gains sont
calculés dans le sens 60 k → 200 k (négatif = le run long fait mieux).

Usage :
  python3 work/n2ac/table_200k.py [--a work/n2ac/eval-mix60.json] [--b work/n2ac/eval-mix200.json]
"""
from __future__ import annotations

import argparse
import json
import pathlib

LIGNES = [
    ("validation française (L128)", "val_fr_L128"),
    ("validation française (L256)", "val_fr_L256"),
    ("validation française (L512)", "val_fr_L512"),
    ("validation du grand corpus (L128)", "val_big_L128"),
    ("validation du grand corpus (L512)", "val_big_L512"),
    ("littérature (jamais vue)", "litterature"),
    ("anglais (jamais vu)", "anglais"),
    ("wikitext2 (jamais vu)", "wikitext2"),
    ("corpus propre du dépôt (transfert)", "corpus_propre_val"),
    ("permutation (contrôle)", "val_fr_permute"),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", default="work/n2ac/eval-mix60.json")
    ap.add_argument("--b", default="work/n2ac/eval-mix200.json")
    a = ap.parse_args()
    x = json.loads(pathlib.Path(a.a).read_text(encoding="utf-8"))
    y = json.loads(pathlib.Path(a.b).read_text(encoding="utf-8"))
    print("| mesure | 60 000 pas (N2.ac) | **200 000 pas** | écart |")
    print("|---|---:|---:|---:|")
    for nom, cle in LIGNES:
        va, vb = x.get(cle), y.get(cle)
        if va is None or vb is None:
            print(f"| {nom} | {va} | {vb} | — |")
            continue
        print(f"| {nom} | {va:.4f} | **{vb:.4f}** | {vb - va:+.4f} |")


if __name__ == "__main__":
    main()
