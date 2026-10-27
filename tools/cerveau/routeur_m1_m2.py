#!/usr/bin/env python3
"""routeur_m1_m2.py — B23 : routeur lexique + forme entre M1 et M2.

Le routeur ne devine pas : il choisit un canal selon la surface.
- surface déjà connue (ou sa casse normalisée) -> M1 ;
- surface longue avec espaces (phrase) -> M1 ;
- sinon (typo, espacement anormal) -> M2.

Les prédictions M1 et M2 sont calculées **une seule fois**, puis comparées.
"""
from __future__ import annotations

import json
import random

from .hub import Hub
from .m2_typo import _reels, _typo
from .voies import entrainer, evaluer_champs
from semantique.typed_corpus import ItemType
from semantique.universaux import code_rsn
from semantique.normalisation import normaliser


def _lexique(reels):
    return {normaliser(it.texte) for it in reels}


def router(surface: str, lexique: set[str]) -> str:
    if surface != surface.strip():
        return "M2"
    if normaliser(surface) in lexique:
        return "M1"
    if " " in surface and len(surface) > 10:
        return "M1"
    return "M2"


def _perturber(texte: str, mode: str, rng: random.Random):
    if mode == "original":
        return texte
    if mode == "casse":
        return texte.upper()
    if mode == "espaces":
        return "  " + texte.replace(" ", "") + "  "
    if mode == "typo":
        return _typo(texte, "suppression", rng)
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
    reels = [it for it in _reels() if code_rsn(it.attendu).get("de") is not None]
    lex = _lexique(_reels())
    rng = random.Random(graine)
    out = {"n": len(reels), "modes": {}}
    for mode in ("original", "casse", "espaces", "typo", "phrase"):
        pert = [ItemType(_perturber(it.texte, mode, rng), code_rsn(it.attendu),
                         it.jeu, "coup", it.langue, it.paire, "routeur", it.contexte)
                for it in reels]
        m1_pred = [hub.percevoir(it.texte, it.jeu, it.contexte) for it in pert]
        r = evaluer_champs(m, pert, champs=("de", "vers"), device=device,
                           retour_pred=True)
        m2_ok = [int(d == it.code.get("de") and v == it.code.get("vers"))
                 for it, d, v in zip(pert, r["de"]["pred"], r["vers"]["pred"])]
        m1_ok = [int(p == it.code) for it, p in zip(pert, m1_pred)]
        decisions = [router(it.texte, lex) for it in pert]
        routeur = [m1_ok[i] if decisions[i] == "M1" else m2_ok[i]
                   for i in range(len(pert))]
        out["modes"][mode] = {
            "M1": sum(m1_ok) / len(pert),
            "M2": sum(m2_ok) / len(pert),
            "routeur": sum(routeur) / len(pert),
            "part_M2": sum(1 for d in decisions if d == "M2") / len(decisions),
        }
    return out


def main() -> None:
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
