#!/usr/bin/env python3
"""census_routage.py — ce que coûterait de répartir par EXPERTS, chiffré.

POURQUOI. Le dépôt sait découper un modèle par PLAGES DE COUCHES : deux nœuds,
écart de flux 0,00e0, c'est prouvé. Mais l'unité de travail naturelle d'un modèle
routé n'est pas la couche, c'est l'EXPERT — et l'inventaire du 08/10 note que la
sommation inter-nœuds des experts **n'existe pas** : un nœud partiel saute
l'expert absent sans un mot (`model.rs`, `Moe::ou` → `None` → `continue`).

Avant d'écrire cette sommation, il faut les trois chiffres qui décident :
  1. la CHARGE par expert — un expert qui reçoit 30 % des jetons impose un nœud
     trois fois plus chargé que les autres ;
  2. le VOLUME qui traverserait le réseau si les experts étaient sur deux
     machines — en octets par jeton, comparable aux 848 octets d'un flux de
     couche déjà mesurés ;
  3. le JEU CHAUD — combien d'experts couvrent 90 % des jetons. S'il en faut la
     moitié, la répartition par experts ne réduit rien.

Usage :
    census_routage.py --modele /tmp/m4_route [--lots 8] [--seq 128]
"""
import argparse
import sys

import numpy as np
import torch
import torch.nn.functional as F


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--modele", default="/tmp/m4_route")
    p.add_argument("--corpus", default="data/corpus_en_val.txt")
    p.add_argument("--lots", type=int, default=8)
    p.add_argument("--seq", type=int, default=128)
    p.add_argument("--top", type=int, default=4, help="experts retenus par le recensement")
    a = p.parse_args()

    from transformers import AutoModelForCausalLM
    modele = AutoModelForCausalLM.from_pretrained(a.modele, dtype=torch.float32).eval()
    cfg = modele.config
    n_exp = getattr(cfg, "num_experts", None) or getattr(cfg, "num_local_experts", 0)
    k = getattr(cfg, "num_experts_per_tok", 0)
    if not n_exp:
        print(f"# {a.modele} n'est pas un modèle routé : rien à recenser", file=sys.stderr)
        return 1
    couches = [m for m in modele.modules() if hasattr(m, "gate") and hasattr(m, "experts")]
    print(f"# {a.modele} : {len(couches)} couches routées · {n_exp} experts · top-{k}")

    # Le corpus est lu en octets : le vocabulaire de ces modèles est de 256.
    data = np.frombuffer(open(a.corpus, "rb").read(1_000_000), dtype=np.uint8).astype(np.int64)
    total = np.zeros((len(couches), n_exp), dtype=np.int64)
    capturés = []

    def crochet(idx):
        def fn(mod, entree, sortie):
            # Le routeur de Qwen3-MoE rend un TRIPLET
            # (logits, poids, experts choisis) : le troisième élément EST le
            # top-k, inutile de le recalculer — et le prendre pour un tenseur
            # lève « 'tuple' object has no attribute 'detach' ».
            choix = sortie[2] if isinstance(sortie, tuple) else sortie
            capturés.append((idx, choix.detach()))
        return fn
    for i, c in enumerate(couches):
        c.gate.register_forward_hook(crochet(i))

    with torch.no_grad():
        for lot in range(a.lots):
            deb = lot * a.seq
            x = torch.from_numpy(data[deb:deb + a.seq]).unsqueeze(0)
            capturés.clear()
            modele(x)
            for idx, choix in capturés:
                choix = choix.reshape(-1, choix.shape[-1])
                for e in range(n_exp):
                    total[idx, e] += int((choix == e).any(dim=-1).sum())

    jetons = total.sum(axis=1) // max(k, 1)
    print(f"\n# {'couche':>7}{'jetons':>9}{'charge max':>12}{'charge moy':>12}"
          f"{'max/moy':>9}{'experts pour 90 %':>19}")
    for i in range(len(couches)):
        charge = total[i]
        if charge.sum() == 0:
            continue
        ordre = np.sort(charge)[::-1]
        cum = np.cumsum(ordre) / ordre.sum()
        chaud = int(np.searchsorted(cum, 0.90) + 1)
        moy = charge.mean()
        print(f"  {i:>7}{jetons[i]:>9}{charge.max():>12}{moy:>12.0f}"
              f"{charge.max()/max(moy,1):>9.2f}{chaud:>19}")

    # Volume réseau si les experts étaient sur deux machines : les jetons dont
    # l'expert est distant font un aller-retour d'état (192 canaux × 4 octets,
    # plus l'en-tête de 79 octets du protocole v6).
    etat = getattr(cfg, "hidden_size", 0) * 4 + 79
    charge_moy = total.sum(axis=1).mean() / max(n_exp, 1)
    desequilibre = float(total.sum(axis=1).max() / max(total.sum(axis=1).mean(), 1))
    print(f"\n# état transporté par jeton : {etat} octets (79 d'en-tête + {getattr(cfg,'hidden_size',0)} × 4)")
    print(f"# pour un partage à 2 nœuds, le déséquilibre de jetons par couche vaut ×{desequilibre:.2f}")
    print(f"# un expert « moyen » reçoit {charge_moy:.0f} jetons sur la fenêtre de {a.lots*a.seq}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
