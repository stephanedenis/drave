#!/usr/bin/env python3
"""M4 — mémoire épisodique adressable par contenu.

Chaque épisode est (surface, code, langue, paire). La clé est le one-hot du code
typé ; la lecture est un plus proche voisin. On mesure le rappel exact, la
complétion sur un code partiel et la séparation de codes voisins.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from semantique.universaux import CHAMPS, vecteur


@dataclass
class Episode:
    surface: str
    code: dict
    langue: str = "?"
    paire: str = ""
    poids: float = 1.0
    meta: dict = field(default_factory=dict)


class Episodique:
    nom = "M4-episodique"

    def __init__(self) -> None:
        self.episodes: list[Episode] = []

    def stocker(self, surface: str, code: dict, langue: str = "?", paire: str = "",
                poids: float = 1.0) -> None:
        self.episodes.append(Episode(surface, dict(code), langue, paire, poids))

    def _cle(self, code: dict):
        return vecteur(code)

    def classer(self, code: dict, k: int = 1):
        """Classe les épisodes par similarité cosinus décroissante.

        Renvoie des couples `(score, episode)`, le score restant dans [0, 1] pour
        des poids unitaires. La marge top1 - top2 est la seule mesure de
        confiance disponible : sans seuil, un voisin proche n'est pas distingué
        d'une réponse sûre.
        """
        q = self._cle(code)
        scores = []
        for e in self.episodes:
            v = self._cle(e.code)
            dot = sum(a * b for a, b in zip(q, v))
            nq = math.sqrt(sum(a * a for a in q)) or 1.0
            nv = math.sqrt(sum(b * b for b in v)) or 1.0
            scores.append((dot / (nq * nv)) * e.poids)
        ordre = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [(scores[i], self.episodes[i]) for i in ordre]

    def chercher(self, code: dict, k: int = 1):
        return [e for _, e in self.classer(code, k)]

    def _marge(self, code: dict) -> tuple[float, float]:
        c = self.classer(code, 2)
        if not c:
            return 0.0, 0.0
        s1 = c[0][0]
        s2 = c[1][0] if len(c) > 1 else 0.0
        return s1, s1 - s2

    def rappel(self, code: dict) -> dict:
        e = self.chercher(code, 1)
        s, marge = self._marge(code)
        return {"exact": bool(e and e[0].code == code), "surface": e[0].surface if e else None,
                "similarite": s, "marge": marge}

    def completion(self, code_partiel: dict) -> dict:
        e = self.chercher(code_partiel, 1)
        s, marge = self._marge(code_partiel)
        if not e:
            return {"exact": False, "champs": 0.0, "similarite": s, "marge": marge}
        ok = sum(1 for nom, _ in CHAMPS if e[0].code.get(nom) == code_partiel.get(nom))
        return {"exact": e[0].code == code_partiel, "champs": ok / len(CHAMPS),
                "code": e[0].code, "similarite": s, "marge": marge}

    def separation(self, code_a: dict, code_b: dict) -> dict:
        """Deux codes qui ne diffèrent que d'un champ doivent rester distincts."""
        e = self.chercher(code_a, 2)
        if len(e) < 2:
            return {"distincts": False}
        return {"distincts": e[0].code != e[1].code, "premier": e[0].code == code_a,
                "second": e[1].code == code_b}
