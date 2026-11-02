#!/usr/bin/env python3
"""init_figee.py — une initialisation aléatoire **figée**, la même pour les deux schémas de position.

Pourquoi : les points de contrôle de N2 partent tous de `base-wiki-45m.pt`, un modèle **absolu**
déjà entraîné. Comparer RoPE à absolu depuis cette initialisation mesure l'**adaptation**, pas
l'apprentissage. Ici on retire l'entraînement : on tire **une** initialisation au hasard, on la
fige sur disque, et les deux bras (absolu, RoPE) partent exactement des mêmes poids. Il ne reste
que le schéma de position.

Usage :
  PYTHONPATH=. python3 work/n2ac/init_figee.py --sortie work/n2ac/init-figee.pt
"""
from __future__ import annotations

import argparse
import pathlib

import torch

from tools.native_model import NativeConfig, NativeModel


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default="work/n2ac/init-figee.pt")
    ap.add_argument("--dim", type=int, default=384)
    ap.add_argument("--expert-hidden", type=int, default=512)
    ap.add_argument("--graine", type=int, default=20261102)
    a = ap.parse_args()
    torch.manual_seed(a.graine)
    cfg = NativeConfig(d_model=a.dim, expert_hidden=a.expert_hidden)
    m = NativeModel(cfg)
    p = pathlib.Path(a.sortie)
    p.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"config": cfg.__dict__, "state": m.state_dict()}, p)
    print(f"  {p} · {m.nb_parametres()} paramètres · graine {a.graine}")


if __name__ == "__main__":
    main()
