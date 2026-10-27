#!/usr/bin/env python3
"""M7 — neuromodulation : nouveauté, incertitude, récompense.

Les signaux ne changent pas le code ; ils changent le **poids d'écriture** de la
mémoire épisodique. On mesure si cela aide le rappel des épisodes nouveaux ou
ambigus, et on publie le négatif s'il y en a un.
"""
from __future__ import annotations

from semantique.universaux import CHAMPS


class Neuromodulation:
    nom = "M7-neuromodulation"

    def __init__(self, alpha: float = 0.5, beta: float = 0.5) -> None:
        self.alpha = alpha
        self.beta = beta
        self.vus = set()

    def signal(self, code: dict, marge: float = 1.0, recompense: float = 0.0) -> dict:
        cle = tuple(code.get(n) for n, _ in CHAMPS)
        nouveau = cle not in self.vus
        self.vus.add(cle)
        nouveaute = 1.0 if nouveau else 0.0
        incertitude = max(0.0, 1.0 - marge)
        poids = 1.0 + self.alpha * nouveaute + self.beta * incertitude + 0.2 * recompense
        return {"nouveaute": nouveaute, "incertitude": incertitude, "poids": poids}
