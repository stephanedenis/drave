#!/usr/bin/env python3
"""restitution.py — B18 : sortie canonique depuis le code typé.

Le miroir de M1 : un code doit pouvoir être **rendu** en une surface canonique
et relu sans perte. Ce n'est pas un décodeur neuronal (B10 est négatif) : c'est
le **codec canonique**, mesuré comme sortie.
"""
from __future__ import annotations

import collections
import json

from .hub import Hub
from semantique.universaux import code_rsn
from jeux.corpus import construire_corpus
from jeux.corpus_multilingue import construire_corpus_multilingue


class Restitution:
    nom = "B18-restitution"

    def __init__(self) -> None:
        self.hub = Hub()

    def rendre(self, code: dict, contexte=None):
        return self.hub.rendre(code, contexte)

    def mesurer(self, items_=None) -> dict:
        if items_ is None:
            its = [it for c in (construire_corpus(), construire_corpus_multilingue())
                   for it in c.items if it.attendu.nature == "coup"]
        else:
            its = items_
        ok = relu = 0
        echecs = []
        for it in its:
            code = code_rsn(it.attendu) if hasattr(it, "attendu") else it.code
            s = self.rendre(code, it.contexte)
            if s is None:
                echecs.append(it.texte)
                continue
            ok += 1
            c = self.hub.percevoir(s, it.jeu, it.contexte)
            if c == code:
                relu += 1
            else:
                echecs.append(it.texte)
        n = len(its)
        return {"n": n, "rendus": ok, "rendu": ok / max(1, n),
                "relus": relu, "roundtrip": relu / max(1, n),
                "echecs": echecs[:10]}


def main() -> None:
    print(json.dumps(Restitution().mesurer(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
