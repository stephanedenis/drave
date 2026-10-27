#!/usr/bin/env python3
"""M5 — codage prédictif : prédire l'action suivante, mesurer l'erreur.

Un prédicteur de Markov, volontairement simple, sur les séquences de jeu. Il
fournit une **prédiction** et une **surprise** ; l'erreur est l'information que le
module suivant peut consommer.
"""
from __future__ import annotations

import collections
import math


class Predictif:
    nom = "M5-predictif"

    def __init__(self) -> None:
        self.transitions = collections.defaultdict(collections.Counter)
        self.majoritaire = {}

    def entrainer(self, sequences) -> None:
        for seq in sequences:
            pas = [p.code for p in seq.pas]
            for a, b in zip(pas, pas[1:]):
                self.transitions[(a["jeu"], a["action"])][b["action"]] += 1
            for p in pas:
                self.majoritaire.setdefault(p["jeu"], collections.Counter())[p["action"]] += 1
        self.majoritaire = {j: c.most_common(1)[0][0] for j, c in self.majoritaire.items()}

    def predire(self, code: dict) -> tuple[str, float]:
        c = self.transitions.get((code["jeu"], code["action"]))
        if not c:
            return self.majoritaire.get(code["jeu"], "deplacer"), 0.0
        total = sum(c.values())
        action, n = c.most_common(1)[0]
        return action, n / total

    def evaluer(self, sequences) -> dict:
        total = ok = 0
        surprise = []
        for seq in sequences:
            pas = [p.code for p in seq.pas]
            for a, b in zip(pas, pas[1:]):
                p, prob = self.predire(a)
                total += 1
                ok += int(p == b["action"])
                surprise.append(-math.log(max(prob, 1e-6)))
        base = 0
        n_base = 0
        for seq in sequences:
            pas = [p.code for p in seq.pas]
            for a, b in zip(pas, pas[1:]):
                n_base += 1
                base += int(self.majoritaire.get(a["jeu"], "deplacer") == b["action"])
        return {"exact": ok / max(1, total), "majoritaire": base / max(1, n_base),
                "surprise": sum(surprise) / max(1, len(surprise)), "n": total}
