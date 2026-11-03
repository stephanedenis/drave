#!/usr/bin/env python3
"""eval_fenetre.py — le **même texte**, vu avec des contextes de 256, 512 et 1 000 octets.

C'est le contrôle qui sépare les deux schémas de position, et il doit être mesuré sur le
**même flux d'octets** : on prend une fenêtre de 1 000 octets, on ne garde que ses C derniers
octets (C = 256, 512, 1 000) et on note la PPL des **128 derniers** octets — le même texte, la
même cible, seule la longueur du préfixe change.

Prédiction des positions **relatives** (RoPE) : le masque d'attention borne à 256 octets en
arrière, et l'écart relatif des 128 derniers octets ne dépend pas de C. Les trois valeurs
doivent donc être **identiques** (aux aléas de flottants près). Prédiction des positions
**absolues** : les mêmes octets tombent sur des lignes de table différentes — 0…255, 488…999,
etc. — la PPL doit **dépendre de C** ; au-delà de 511, elle tombe sur des lignes jamais
entraînées et explose.

Usage :
  PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/eval_fenetre.py <point.pt> [--rope] [--sortie x.json]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "work/n2j")

import torch  # noqa: E402
import torch.nn.functional as F  # noqa: E402

from tools.eval_n2_propre import charge, charger_bytes  # noqa: E402
import evalue_canal as ec  # noqa: E402

CONTEXTES = (256, 512, 1000)
CIBLE = 128
N_FENETRES = 16
MAX = 1000


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("point")
    ap.add_argument("--rope", action="store_true")
    ap.add_argument("--val", default="data/wiki_fr/propre")
    ap.add_argument("--contextes", default="256,512,1000")
    ap.add_argument("--sortie", default=None)
    a = ap.parse_args()

    if a.rope:
        from work.n2ac.rope_model import charge_rope
        m = charge_rope(a.point)
    else:
        m = charge(a.point)

    val = charger_bytes(f"{a.val}/val.txt")
    ct = torch.tensor(list(pathlib.Path(f"{a.val}/val.canal").read_bytes()), dtype=torch.long)
    contextes = [int(x) for x in a.contextes.split(",")]
    maxi = max(contextes)
    res = {"fichier": pathlib.Path(a.point).name,
           "positions": "rope" if a.rope else "absolues",
           "cible": CIBLE, "contextes": contextes, "ppl": {}}
    for C in contextes:
        tot = n = 0.0
        for k in range(8):
            # fenêtres de 1000 octets, tirées une fois pour toutes : les mêmes pour tous les C
            x, c = ec.fenetres(val, ct, N_FENETRES, maxi + 1, k * N_FENETRES)
            x, c = x[:, maxi - C:], c[:, maxi - C:]
            with torch.no_grad():
                logits = m(x[:, :-1], canal=c[:, :-1])["logits"]
            perte = F.cross_entropy(logits.reshape(-1, 256), x[:, 1:].reshape(-1),
                                    reduction="none").view(x.shape[0], -1)
            tot += float(perte[:, -(CIBLE + 1):-1].sum())
            n += perte[:, -(CIBLE + 1):-1].numel()
        res["ppl"][str(C)] = round(float(torch.tensor(tot / n).exp()), 4)
        print(f"  contexte {C:4d} · PPL des {CIBLE} derniers octets {res['ppl'][str(C)]:.4f}",
              flush=True)
    print(json.dumps(res, ensure_ascii=False), flush=True)
    if a.sortie:
        pathlib.Path(a.sortie).write_text(
            json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
