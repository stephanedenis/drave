#!/usr/bin/env python3
"""trajectoire.py — la courbe PPL(pas) lue dans le journal d'entraînement, et sa loi.

Le journal de `entrainer_native.py` imprime, tous les 50 pas, la perte du pas et la PPL de
validation interne (les 5 % finaux du corpus). On en tire :

  - la **trajectoire** (pas, perte, PPL) pour le tableau de la fiche ;
  - un **ajustement en loi de puissance** PPL = a · pas^(−b), estimé en log-log sur la plage
    indiquée (`--depuis`), et le nombre de pas qu'il faudrait pour atteindre une cible.

L'extrapolation n'est pas une mesure : c'est une **borne de lecture** qu'on donne avec son
exposant, pour que « il faudrait N pas » ne soit pas une impression.

Usage :
  python3 work/n2ac/trajectoire.py work/n2ac/mix-200k.log [--depuis 20000] [--cible 2.5]
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import re

LIGNE = re.compile(r"^pas\s+(\d+) · perte ([\d.]+) · PPL val ([\d.]+) · (\d+) s$")


def lire(chemin: pathlib.Path) -> list[tuple[int, float, float]]:
    out = []
    for ligne in chemin.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = LIGNE.match(ligne.strip())
        if m:
            out.append((int(m.group(1)), float(m.group(2)), float(m.group(3))))
    return out


def ajuste(points: list[tuple[int, float]], depuis: int) -> tuple[float, float]:
    pts = [(p, v) for p, v in points if p >= depuis and v > 0]
    n = len(pts)
    sx = sum(math.log(p) for p, _ in pts)
    sy = sum(math.log(v) for _, v in pts)
    sxx = sum(math.log(p) ** 2 for p, _ in pts)
    sxy = sum(math.log(p) * math.log(v) for p, v in pts)
    b = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    a = math.exp((sy - b * sx) / n)
    return a, -b


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("journal")
    ap.add_argument("--depuis", type=int, default=20000)
    ap.add_argument("--cible", type=float, default=2.5)
    ap.add_argument("--sortie", default=None)
    a = ap.parse_args()
    pts = lire(pathlib.Path(a.journal))
    if not pts:
        raise SystemExit("aucune ligne de mesure dans le journal")
    a_coef, b_exp = ajuste([(p, v) for p, _, v in pts], a.depuis)
    dernier_pas, _, dernier = pts[-1]
    res = {"journal": a.journal, "points": len(pts), "dernier_pas": dernier_pas,
           "ppl_finale": dernier, "ajustement": {"depuis": a.depuis, "a": round(a_coef, 6),
                                                 "b": round(b_exp, 6)}}
    if 0 < b_exp:
        res["pas_pour_cible"] = int((a_coef / a.cible) ** (1 / b_exp))
    # une mesure tous les 10 000 pas, pour le tableau
    res["trajectoire"] = [[p, v] for p, _, v in pts if p % 10000 == 0]
    print(json.dumps(res, ensure_ascii=False, indent=1))
    if a.sortie:
        pathlib.Path(a.sortie).write_text(
            json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
