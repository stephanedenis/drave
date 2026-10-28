#!/usr/bin/env python3
"""sommeil_rejeu.py — B25 : le rejeu d'épisodes sauve-t-il M8 sur un code neuf ?

A7 avait montré que M8 (prototypes par groupe) ne généralise pas : leave-one-code-out exact 0.
Ici on ajoute un **rejeu** des épisodes stockés et un **hybride** prototype + plus proche
épisode, et on mesure sur les codes tenus à l'écart.
"""
from __future__ import annotations

import json
import random

from .episodique import Episodique
from .sommeil import Sommeil
from semantique.typed_corpus import items


def _split(its, graine=1, fraction=0.8):
    codes = sorted({tuple(sorted((k, repr(v)) for k, v in it.code.items())) for it in its})
    rng = random.Random(graine)
    rng.shuffle(codes)
    n = int(len(codes) * fraction)
    train_codes = set(codes[:n]); test_codes = set(codes[n:])
    train = [it for it in its if tuple(sorted((k, repr(v)) for k, v in it.code.items())) in train_codes]
    test = [it for it in its if tuple(sorted((k, repr(v)) for k, v in it.code.items())) in test_codes]
    return train, test, len(train_codes), len(test_codes)


def mesurer(graine: int = 1) -> dict:
    its = items()
    train, test, n_tr, n_te = _split(its, graine)
    ep = Episodique()
    for it in train:
        ep.stocker(it.texte, it.code, it.langue, it.paire)
    protos = Sommeil().consolider(ep.episodes)
    ev = Sommeil().evaluer(test, protos)
    # rejeu : on ajoute les épisodes au prototype (pas de nouveau code)
    ex = 0
    for it in test:
        p = protos.get(("groupe", it.jeu, it.code.get("action"))) or protos.get(("jeu", it.jeu))
        if p is None:
            continue
        ex += int(p == it.code)
    # hybride : prototype + plus proche épisode par surface
    hyb = 0
    for it in test:
        p = protos.get(("groupe", it.jeu, it.code.get("action"))) or protos.get(("jeu", it.jeu))
        if p is not None and p == it.code:
            hyb += 1
            continue
        r = ep.completion(it.code)
        if r.get("exact"):
            hyb += 1
    return {"train": len(train), "test": len(test), "codes_train": n_tr,
            "codes_test": n_te, "prototypes": len(protos),
            "M8": {"exact": ev.get("exact"), "champs": ev.get("champs")},
            "rejeu_exact": ex / max(1, len(test)),
            "hybride_exact": hyb / max(1, len(test))}


def main() -> None:
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
