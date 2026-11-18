#!/usr/bin/env python3
"""balayage_decodage.py — quel décodage pour le natif ? (le greedy se dégrade avec l'entraînement)

POURQUOI. Le checkpoint r1 (73 M, 13 000 pas) a un top-40 à 0,831 de mots valides mais un
**greedy qui boucle** (répétition 11, écho 0,149) : le banc à trois réglages ne dit pas s'il
existe un décodage qui garde le vocabulaire ET casse la boucle. Ce balayage répond avec le même
banc (20 prompts, 128 octets, mêmes métriques) sur une grille (top_k, température), et le greedy
comme point de comparaison.

Usage :
  PYTHONPATH=. python3 bench/balayage_decodage.py --modele work/n3/r1.pt --n 128 --n-regimes 9 \\
      --sortie reports/balayage-decodage-r1.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import torch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from tools.banc_generation import (PROMPTS, charger, generer, mesurer,  # noqa: E402
                                   vocabulaires)

# (nom, top_k, température) — 0 / 0 = greedy
GRILLE = [
    ("greedy", 0, 0.0),
    ("k20_T0.5", 20, 0.5), ("k20_T0.8", 20, 0.8), ("k20_T1.0", 20, 1.0),
    ("k40_T0.5", 40, 0.5), ("k40_T0.8", 40, 0.8), ("k40_T1.0", 40, 1.0),
    ("k80_T0.5", 80, 0.5), ("k80_T0.8", 80, 0.8), ("k80_T1.0", 80, 1.0),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", required=True)
    ap.add_argument("--n", type=int, default=128)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--graine", type=int, default=1234)
    ap.add_argument("--sortie", default="")
    a = ap.parse_args()
    torch.manual_seed(a.graine)
    modele, cfg = charger(a.modele, a.device)
    vocab = vocabulaires(50_000)
    resultats = {}
    for nom, k, t in GRILLE:
        mesures = []
        for prompt in PROMPTS:
            texte, _ = generer(modele, prompt, a.n, k, t)
            mesures.append(mesurer(texte, prompt, vocab))
        n = len(mesures)
        moy = {c: round(sum(m[c] for m in mesures) / n, 4)
               for c in ("mots_valides", "distinct_2", "repetition", "echo")}
        moy["mots"] = round(sum(m["mots"] for m in mesures) / n, 1)
        moy["top_k"], moy["temperature"] = k, t
        resultats[nom] = moy
        print(f"  {nom:10} mots {moy['mots']:5.1f} · valides {moy['mots_valides']:.3f} · "
              f"d2 {moy['distinct_2']:.3f} · rép {moy['repetition']:.1f} · écho {moy['echo']:.3f}",
              flush=True)
    if a.sortie:
        pathlib.Path(a.sortie).write_text(json.dumps(
            {"schema": "drave.balayage-decodage", "version": 1, "modele": a.modele,
             "n": a.n, "graine": a.graine, "regimes": resultats},
            indent=1, ensure_ascii=False))
        print(f"  écrit : {a.sortie}")


if __name__ == "__main__":
    main()
