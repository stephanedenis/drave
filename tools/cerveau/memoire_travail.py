#!/usr/bin/env python3
"""M3 — mémoire de travail : maintenir une suite de codes, la relire, la comparer.

Le module est volontairement **structurel** : un tampon borné, un pointeur, une
répétition. Il ne promet pas la mémoire du réseau (N5) ; il mesure ce qu'un
**bus** peut tenir sans gradient.
"""
from __future__ import annotations

from collections import deque


class MemoireTravail:
    nom = "M3-memoire-travail"

    def __init__(self, capacite: int = 12) -> None:
        self.capacite = capacite
        self.tampon: deque = deque(maxlen=capacite)

    def charger(self, codes) -> None:
        self.tampon.clear()
        for c in codes[-self.capacite:]:
            self.tampon.append(dict(c))

    def lire(self, i: int):
        return self.tampon[i] if 0 <= i < len(self.tampon) else None

    def nback(self, n: int):
        if len(self.tampon) <= n:
            return None
        return self.tampon[-1] == self.tampon[-1 - n]

    def span(self, sequences) -> dict:
        """Plus longue suite où toutes les positions sont relues exactement."""
        meilleur = 0
        essais = 0
        bons = 0
        for seq in sequences:
            codes = [p.code for p in seq.pas]
            for n in range(1, min(len(codes), self.capacite) + 1):
                self.charger(codes[:n])
                exact = all(self.lire(i) == codes[i] for i in range(n))
                essais += 1
                bons += int(exact)
                if exact:
                    meilleur = max(meilleur, n)
        return {"span": meilleur, "essais": essais, "exact": bons / max(1, essais)}

    def nback_scores(self, sequences, n: int = 1) -> dict:
        total = ok = 0
        for seq in sequences:
            codes = [p.code for p in seq.pas]
            for i in range(n, len(codes)):
                self.charger(codes[:i + 1])
                total += 1
                ok += int(self.nback(n) is True)
        return {"n": n, "exact": ok / max(1, total), "essais": total}
