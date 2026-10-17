#!/usr/bin/env python3
"""iterer_bloc.py — LE TEST DÉCISIF : un état entraîné AVEC la récurrence est-il HABITABLE par elle ?

LA CONCLUSION DE LA NUIT, ET CE QU'IL RESTE À PROUVER. Quatre voies ont échoué pour la même raison ✓ : la
boucle **directe** (λ = 7 311 ✗), le pas `h_p → h_{p+1}` (λ de 30 à 120 ✗), le **cycle** (λ 206 → 136 ✗)
et l'**opérateur post-hoc** (qui n'a trouvé que l'**identité** ✗✓) — parce qu'**aucun modèle entraîné ici
n'a jamais eu l'itération dans sa boucle** ✗. Le § 15 en tire le programme ✓ : entraîner un modèle dont les
couches sont **un bloc répété** ✓ (`--partage` ✓), et voir si l'état devient **habitable** ✓✓.

CE QUE CET OUTIL MESURE. On prend deux modèles — **partagé** (bloc répété ✓) et **distinct** (témoin ✗) —
et on les fait tourner **t fois** sur eux-mêmes ✓ (en dupliquant leurs couches ✓, ce qui est *exactement*
une itération du bloc ✓). Pour t = 1, 2, 4, on mesure **le contenu** : ce que l'état dit du jeton à venir ✓
(mapping ridge appris sur la moitié, mesuré sur l'autre ✓). Un état **habitable** garde son contenu quand t
grandit ✓✓ ; un état « à un coup » le perd ✗.

Usage :
  CUDA_VISIBLE_DEVICES=0 python tools/iterer_bloc.py --partage /tmp/jouet-partage --distinct /tmp/jouet-distinct \\
      --ids /tmp/ids-octets.txt [--iterations 1,2,4]
"""
from __future__ import annotations

import argparse
import copy
import pathlib
import re

import numpy as np
import torch
import torch.nn as nn


def contenu(m, ids, L: int, amorces: int) -> float:
    """Le contenu : écart relatif du mapping `état normalisé → embedding du jeton suivant` ✓."""
    S, T = [], []
    with torch.no_grad():
        for i in range(amorces):
            d = 1000 + i * 400
            b = torch.tensor([ids[d:d + L]])
            hs = m(b, output_hidden_states=True).hidden_states[-1][0]
            S.append(m.model.norm(hs).numpy().astype(np.float64))
            T.append(m.get_input_embeddings()(torch.tensor([ids[d + 1:d + L + 1]]))[0].numpy().astype(np.float64))
    S, T = np.concatenate(S), np.concatenate(T)
    n = int(S.shape[0] * 0.6)
    mh, me = S[:n].mean(0), T[:n].mean(0)
    Hc, Ec = S[:n] - mh, T[:n] - me
    W = np.linalg.solve(Hc.T @ Hc + 1e-3 * np.eye(Hc.shape[1]), Hc.T @ Ec)
    P = (S[n:] - mh) @ W + me
    return 100 * float(np.linalg.norm(P - T[n:]) / np.linalg.norm(T[n:]))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partage", required=True)
    ap.add_argument("--distinct", required=True)
    ap.add_argument("--ids", required=True)
    ap.add_argument("--longueur", type=int, default=64)
    ap.add_argument("--amorces", type=int, default=60)
    ap.add_argument("--iterations", default="1,2,4")
    a = ap.parse_args()
    from transformers import AutoModelForCausalLM
    ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(a.ids).read_text()) if x.strip()]
    its = [int(x) for x in a.iterations.split(",")]

    print()
    print("   modèle    | t=1  | t=2  | t=4   (t = nombre d'applications du bloc ; plus bas est mieux)")
    print("   ----------|------|------|------")
    for nom, chemin in (("partagé", a.partage), ("distinct", a.distinct)):
        m0 = AutoModelForCausalLM.from_pretrained(chemin, dtype=torch.float32).eval()
        base = [copy.deepcopy(c) for c in m0.model.layers]
        cellules = []
        for t in its:
            m = AutoModelForCausalLM.from_pretrained(chemin, dtype=torch.float32).eval()
            m.model.layers = nn.ModuleList([copy.deepcopy(c) for _ in range(t) for c in base])
            # ⚠️ LE PIÈGE, ET IL A COÛTÉ UNE MESURE ✗✓ : la boucle de `Qwen3Model.forward` est bornée par
            # `config.num_hidden_layers` (elle fait `self.layers[: self.config.num_hidden_layers]` ✓✗).
            # Sans mettre la config à jour, les couches ajoutées sont **silencieusement ignorées** ✓✓ : la
            # sortie était **identique au chiffre près** pour t = 1, 2 et 4 ✗ (mesuré : −5463,6558 dans les
            # deux cas ✓✗) — et j'ai failli lire « l'état est habitable, le contenu ne bouge pas » ✓✗.
            m.config.num_hidden_layers = len(m.model.layers)
            # ... et `config.layer_types` est une liste PAR COUCHE (`full_attention` / `sliding_attention` ✓) :
            # elle aussi doit être étendue, sinon `causal_mask_mapping[config.layer_types[i]]` sort de la
            # liste ✓✗ (IndexError mesuré ✓).
            m.config.layer_types = (list(m.config.layer_types) * t)[:len(m.model.layers)]
            cellules.append(f"{contenu(m, ids, a.longueur, a.amorces):4.1f}")
            del m
        print(f"   {nom:9s} | " + " | ".join(cellules))
        del m0
    print()
    print("   lecture : si le modèle PARTAGÉ (bloc répété ✓) garde son contenu quand t grandit, alors son")
    print("   état est HABITABLE par l'itération ✓✓ — c'est ce que l'entraînement avec la récurrence")
    print("   dans la boucle doit acheter, et que l'opérateur post-hoc n'a pas pu trouvé ✗.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
