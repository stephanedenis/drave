#!/usr/bin/env python3
"""m2_secours.py — B19 : M2 peut-il sauver les surfaces que M1 ne lit pas ?

Le corpus réel est lu à 100 % par M1 ; M2 n'a donc aucune niche mesurée. On
perturbe les surfaces (casse, espaces, faute, phrase libre) **sans changer le
code attendu**, puis on compare M1 et M2 sur les champs `de`/`vers`.
"""
from __future__ import annotations

import json
import random
import re

from .hub import Hub
from .voies import Voies, entrainer, evaluer_champs
from semantique.typed_corpus import ItemType, items
from semantique.universaux import CHAMPS
from jeux.corpus import construire_corpus
from jeux.corpus_multilingue import construire_corpus_multilingue
from semantique.universaux import code_rsn


def _reels():
    return [it for c in (construire_corpus(), construire_corpus_multilingue())
            for it in c.items if it.attendu.nature == "coup"]


def _perturber(texte: str, mode: str, rng: random.Random) -> str:
    if mode == "casse":
        return texte.upper()
    if mode == "espaces":
        return "  " + texte.replace(" ", "") + "  "
    if mode == "typo" and len(texte) > 3:
        i = rng.randrange(1, len(texte) - 1)
        return texte[:i] + texte[i + 1:]
    if mode == "phrase":
        return f"le coup {texte} est joue"
    return texte


def mesurer(pas: int = 300, graine: int = 1, device: str = "cuda",
            base_checkpoint: str = "/tmp/natif-600-512-8-align-s1") -> dict:
    from transformers import AutoModelForCausalLM
    base = AutoModelForCausalLM.from_pretrained(base_checkpoint, torch_dtype="auto")
    m, _ = entrainer(base, pas=pas, lot=32, seq=64, graine=graine,
                     device=device, synth=True, champs=("de", "vers"),
                     pool="mean+last", contexte=False)
    hub = Hub()
    reels = _reels()
    rng = random.Random(graine)
    out = {"n": len(reels), "modes": {}}
    for mode in ("original", "casse", "espaces", "typo", "phrase"):
        pert = []
        for it in reels:
            s = it.texte if mode == "original" else _perturber(it.texte, mode, rng)
            pert.append(ItemType(s, code_rsn(it.attendu), it.jeu, "coup",
                                 it.langue, it.paire, "perturbe", it.contexte))
        m1 = sum(int(hub.percevoir(it.texte, it.jeu, it.contexte) == it.code)
                 for it in pert) / len(pert)
        r = evaluer_champs(m, pert, champs=("de", "vers"), device=device,
                           retour_pred=True)
        out["modes"][mode] = {
            "M1": m1,
            "M2_de": (sum(int(a == b) for a, b in zip(r["de"]["pred"], r["de"]["cible"]))
                      / max(1, len(r["de"]["pred"]))),
            "M2_vers": (sum(int(a == b) for a, b in zip(r["vers"]["pred"], r["vers"]["cible"]))
                        / max(1, len(r["vers"]["pred"]))),
            "n": len(pert),
        }
    return out


def main() -> None:
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
