#!/usr/bin/env python3
"""M8 — sommeil : rejouer les épisodes, consolider des prototypes.

Le sommeil ne touche pas aux poids du réseau : il **compacte** les épisodes en
prototypes par (jeu, action) et mesure si la complétion d'un code partiel
s'améliore ou se dégrade.
"""
from __future__ import annotations

import collections

from semantique.universaux import CHAMPS


class Sommeil:
    nom = "M8-sommeil"

    def consolider(self, episodes) -> dict:
        groupes = collections.defaultdict(list)
        for e in episodes:
            groupes[(e.code.get("jeu"), e.code.get("action"))].append(e.code)
        prototypes = {}
        for cle, codes in groupes.items():
            proto = {}
            for nom, _ in CHAMPS:
                vals = [c.get(nom) for c in codes]
                proto[nom] = collections.Counter(vals).most_common(1)[0][0]
            prototypes[cle] = proto
        return prototypes

    def evaluer(self, episodes, prototypes) -> dict:
        ok = n = 0
        for e in episodes:
            proto = prototypes.get((e.code.get("jeu"), e.code.get("action")))
            if not proto:
                continue
            n += 1
            ok += sum(1 for nom, _ in CHAMPS if proto.get(nom) == e.code.get(nom))
        return {"champs": ok / max(1, n * len(CHAMPS)), "n": n,
                "prototypes": len(prototypes)}
