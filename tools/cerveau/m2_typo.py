#!/usr/bin/env python3
"""m2_typo.py — B22 : quelles typos M2 sauve-t-il ?

B19 a montré que M2 sauve les suppressions de caractère (71,9/75,1 %) mieux que
M1 (36,8 %). Ici on distingue suppression, substitution, insertion et
transposition, à code constant.
"""
from __future__ import annotations

import json
import random

from .hub import Hub
from .voies import entrainer, evaluer_champs
from semantique.typed_corpus import ItemType
from semantique.universaux import code_rsn
from jeux.corpus import construire_corpus
from jeux.corpus_multilingue import construire_corpus_multilingue


def _reels():
    return [it for c in (construire_corpus(), construire_corpus_multilingue())
            for it in c.items if it.attendu.nature == "coup"]


def _typo(texte: str, mode: str, rng: random.Random) -> str:
    if len(texte) < 3:
        return texte
    i = rng.randrange(1, len(texte) - 1)
    if mode == "suppression":
        return texte[:i] + texte[i + 1:]
    if mode == "substitution":
        return texte[:i] + rng.choice("abcdefgh") + texte[i + 1:]
    if mode == "insertion":
        return texte[:i] + rng.choice("xyz") + texte[i:]
    if mode == "transposition":
        return texte[:i] + texte[i + 1] + texte[i] + texte[i + 2:]
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
    for mode in ("original", "suppression", "substitution", "insertion", "transposition"):
        pert = []
        for it in reels:
            s = it.texte if mode == "original" else _typo(it.texte, mode, rng)
            pert.append(ItemType(s, code_rsn(it.attendu), it.jeu, "coup",
                                 it.langue, it.paire, "typo", it.contexte))
        m1 = sum(int(hub.percevoir(it.texte, it.jeu, it.contexte) == it.code)
                 for it in pert) / len(pert)
        r = evaluer_champs(m, pert, champs=("de", "vers"), device=device,
                           retour_pred=True)
        out["modes"][mode] = {
            "M1": m1,
            "M2_de": sum(int(a == b) for a, b in zip(r["de"]["pred"], r["de"]["cible"])) / max(1, len(r["de"]["pred"])),
            "M2_vers": sum(int(a == b) for a, b in zip(r["vers"]["pred"], r["vers"]["cible"])) / max(1, len(r["vers"]["pred"])),
        }
    return out


def main() -> None:
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
