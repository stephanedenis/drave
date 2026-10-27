#!/usr/bin/env python3
"""pipeline_memoire.py — B17 : M1 → mémoire LFU → M8.

La chaîne B13 ignore la mémoire bornée. Ici, un flux de 528 items est coupé en
préfixe (422) et suffixe (106) : la mémoire voit le préfixe, puis on interroge
le suffixe. On compare FIFO, LRU et LFU, et on mesure ce que M8 peut couvrir.

Le point honnête : LFU retient mieux les répétés (A11), mais M8 sur les codes
retenus est un **lookup** ; la couverture du suffixe reste faible.
"""
from __future__ import annotations

import collections
import json
import random

from .episodique import Episodique
from .neuromodulation import MemoireFrequence
from .sommeil import Sommeil


class PipelineMemoire:
    nom = "B17-pipeline-memoire"

    def __init__(self, capacite: int = 16, politique: str = "lfu"):
        self.memoire = MemoireFrequence(capacite=capacite, politique=politique)

    def flux(self, items, graine: int = 0) -> dict:
        idx = list(range(len(items)))
        random.Random(graine).shuffle(idx)
        prefixe = [items[i] for i in idx[:422]]
        suffixe = [items[i] for i in idx[422:]]
        self.memoire = MemoireFrequence(capacite=16, politique=self.memoire.politique)
        for it in prefixe:
            self.memoire.stocker(it.texte, it.code)
        suf_surface = sum(self.memoire.contient(it.texte) for it in suffixe) / max(1, len(suffixe))
        suf_code = sum(self.memoire.contient_code(it.code) for it in suffixe) / max(1, len(suffixe))
        return {"suf_surface": suf_surface, "suf_code": suf_code,
                "codes_memoire": len(self.memoire.codes())}

    def mesurer(self, items, permutations: int = 30) -> dict:
        out = collections.defaultdict(list)
        for graine in range(permutations):
            for pol in ("fifo", "lru", "lfu"):
                self.memoire = MemoireFrequence(capacite=16, politique=pol)
                r = self.flux(items, graine)
                out[pol].append(r)
        moyens = {pol: {k: sum(v[k] for v in rs) / len(rs) for k in rs[0]}
                  for pol, rs in out.items()}
        # M8 : prototypes sur les codes retenus ; couverture du suffixe
        idx = list(range(len(items)))
        random.Random(0).shuffle(idx)
        prefixe = [items[i] for i in idx[:422]]
        suffixe = [items[i] for i in idx[422:]]
        mem = MemoireFrequence(capacite=16, politique="lfu")
        for it in prefixe:
            mem.stocker(it.texte, it.code)
        ep = Episodique()
        for i, code in enumerate(mem.codes()):
            ep.stocker(f"memoire-{i}", code, "?")
        protos = Sommeil().consolider(ep.episodes)
        couverts = [it for it in suffixe if mem.contient_code(it.code)]
        exact = sum(1 for it in couverts if mem.contient_code(it.code)) / max(1, len(couverts))
        return {"politiques": moyens, "M8": {"prototypes": len(protos),
                                             "suffixe": len(suffixe),
                                             "couverts": len(couverts),
                                             "couverture": len(couverts) / max(1, len(suffixe)),
                                             "exact_sur_couverts": exact,
                                             "generalisation": 0.0}}
