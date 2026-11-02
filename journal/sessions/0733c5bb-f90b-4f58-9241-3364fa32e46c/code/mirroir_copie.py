#!/usr/bin/env python3
"""miroir_copie.py — le miroir de sortie de R1 : le modèle **restitue-t-il** un code vu ?

La PPL est une mesure d'**entrée** : elle dit que la suite est moins surprenante, pas que le
modèle a **lu** l'octet lointain. Ici, on plante un code de 16 octets **deux fois** dans du
texte réel (un remplissage différent par sonde), à `d` octets d'écart, et on demande au modèle
(teacher forcing) de **prédire** la seconde occurrence : justesse top-1 sur les 16 octets.

Attendu si la **fenêtre d'attention** est la contrainte (256 pour R1.1, 512 pour R1.2) :
  d ≤ 240 → le code est copiable (justesse élevée) ;
  d > 240 → justesse au hasard (1/256 ≈ 0,004).
C'est le **contrôle négatif** de R1.1 : le RoPE ne fait pas lire au-delà de la fenêtre ; il
fait seulement disparaître la table de positions absolues.

Le contexte fait 512 octets et les codes restent sous la position 512, donc **les deux schémas
de position sont dans leur plage entraînée** : l'écart mesuré ne peut pas venir d'une ligne de
table non entraînée.

Usage :
  PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/mirroir_copie.py <point.pt> [--rope] [--sortie x.json]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, ".")

import torch  # noqa: E402

from tools.eval_n2_propre import charge  # noqa: E402
from tools.canal_structure import canal as canal_de  # noqa: E402

CONTEXTE = 512
CODE = b"K7Q2M9XA4B1Z8W3C"          # 16 octets, hors distribution du texte
DISTANCES = (16, 64, 128, 200, 240, 255, 300, 400)
N_SONDES = 8


def sonde(texte: bytes, d: int) -> bytes:
    """Code aux positions 32…47 puis 48+d…63+d ; le contexte garde 512 octets exactement."""
    p1 = 32
    p2 = p1 + len(CODE) + d
    return texte[:p1] + CODE + texte[p1:p2] + CODE + texte[p2:CONTEXTE - 2 * len(CODE)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("point")
    ap.add_argument("--rope", action="store_true")
    ap.add_argument("--sortie", default=None)
    a = ap.parse_args()

    if a.rope:
        from work.n2ac.rope_model import charge_rope
        m = charge_rope(a.point)
    else:
        m = charge(a.point)

    brut = pathlib.Path("data/wikitext2_test.txt").read_bytes()
    textes = []
    for i in range(N_SONDES):
        t = brut[i * 4000:(i + 1) * 4000 + CONTEXTE]
        if len(t) >= CONTEXTE:
            textes.append(t)
    n = len(textes)
    res = {"fichier": pathlib.Path(a.point).name,
           "positions": "rope" if a.rope else "absolues",
           "fenetre": m.cfg.window, "contexte": CONTEXTE, "code": CODE.decode(),
           "distances": {}}
    vrai = torch.tensor(list(CODE), dtype=torch.long)
    for d in DISTANCES:
        lot = b"".join(sonde(t, d) for t in textes)
        assert len(lot) == n * CONTEXTE, (len(lot), n * CONTEXTE)
        # surrogateescape : la classe par octet garde la longueur exacte du flux d'octets
        c = torch.tensor(list(canal_de(lot.decode("utf-8", "surrogateescape"))),
                         dtype=torch.long)
        x = torch.tensor(list(lot), dtype=torch.long).view(n, CONTEXTE)
        c = c[:n * CONTEXTE].view(n, CONTEXTE).cuda()
        bons = total = 0
        with torch.no_grad():
            logits = m(x.cuda()[:, :-1], canal=c[:, :-1])["logits"]
        debut = 32 + len(CODE) + d           # position du 1er octet de la 2e occurrence
        for k in range(n):
            pred = logits[k, debut - 1:debut - 1 + len(CODE)].argmax(-1).cpu()
            bons += int((pred == vrai).sum())
            total += len(CODE)
        res["distances"][str(d)] = round(bons / max(1, total), 4)
        print(f"  d={d:4d} · justesse {res['distances'][str(d)]:.4f}", flush=True)
    print(json.dumps(res, ensure_ascii=False), flush=True)
    if a.sortie:
        pathlib.Path(a.sortie).write_text(
            json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
