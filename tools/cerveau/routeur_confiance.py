#!/usr/bin/env python3
"""routeur_confiance.py — B24 : un score de confiance M1 pour router vers M2.

Le routeur B23 choisit par appartenance au lexique ; il échoue sur les typos
qui retombent sur une surface valide. Ici on ajoute un **round-trip M1** :
le code lu doit se rendre puis se relire à l'identique. Si ce n'est pas le cas,
on bascule sur M2.
"""
from __future__ import annotations

import json
import random

from .hub import Hub
from .m2_typo import _reels, _typo
from .routeur_m1_m2 import _perturber, _lexique
from .voies import entrainer, evaluer_champs
from semantique.typed_corpus import ItemType
from semantique.universaux import code_rsn


def confiance_m1(hub: Hub, surface: str, jeu: str, contexte) -> bool:
    code = hub.percevoir(surface, jeu, contexte)
    if code is None:
        return False
    rendu = hub.rendre(code, contexte)
    if rendu is None:
        return False
    return hub.percevoir(rendu, jeu, contexte) == code


def router(surface: str, hub: Hub, jeu: str, contexte, lexique: set[str]) -> str:
    if surface != surface.strip():
        return "M2"
    if confiance_m1(hub, surface, jeu, contexte):
        return "M1"
    if " " in surface and len(surface) > 10:
        return "M1"
    if surface.upper() == surface and surface.lower() in lexique:
        return "M1"
    return "M2"


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
                         it.jeu, "coup", it.langue, it.paire, "confiance", it.contexte)
                for it in reels]
        m1_pred = [hub.percevoir(it.texte, it.jeu, it.contexte) for it in pert]
        r = evaluer_champs(m, pert, champs=("de", "vers"), device=device,
                           retour_pred=True)
        m1_ok = [int(p == it.code) for it, p in zip(pert, m1_pred)]
        m2_ok = [int(d == it.code.get("de") and v == it.code.get("vers"))
                 for it, d, v in zip(pert, r["de"]["pred"], r["vers"]["pred"])]
        decisions = [router(it.texte, hub, it.jeu, it.contexte, lex) for it in pert]
        routeur = [m1_ok[i] if decisions[i] == "M1" else m2_ok[i]
                   for i in range(len(pert))]
        oracle = [max(m1_ok[i], m2_ok[i]) for i in range(len(pert))]
        out["modes"][mode] = {
            "M1": sum(m1_ok) / len(pert),
            "M2": sum(m2_ok) / len(pert),
            "routeur": sum(routeur) / len(pert),
            "oracle": sum(oracle) / len(pert),
            "part_M2": sum(1 for d in decisions if d == "M2") / len(decisions),
        }
    return out


def main() -> None:
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
