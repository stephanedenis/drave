#!/usr/bin/env python3
"""M6 — porte exécutive : choisir la langue, inhiber l'autre.

Deux langues, une cible, une surface. La porte doit dire si la surface est dans la
langue cible. On mesure l'exactitude, les fausses acceptations (inhibition) et le
coût de commutation entre cibles.
"""
from __future__ import annotations

from jeux.lexique_multilingue import MULTI


class Porte:
    nom = "M6-gating"

    def langue(self, texte: str) -> str | None:
        return MULTI.detecte_langue(texte)

    def executer(self, items, cibles=("fr", "en")) -> dict:
        ok = fp = fn = 0
        switch_erreurs = 0
        switch_n = 0
        repeat_erreurs = 0
        repeat_n = 0
        precedent = None
        n = 0
        for i, it in enumerate(items):
            if it.langue not in cibles:
                continue
            n += 1
            # cible alternée par paire : commutation explicite
            cible = cibles[(i // 4) % 2]
            detectee = self.langue(it.texte)
            accepte = detectee == cible
            attendu = it.langue == cible
            ok += int(accepte == attendu)
            if accepte and not attendu:
                fp += 1
            if not accepte and attendu:
                fn += 1
            if precedent is not None:
                if cible != precedent:
                    switch_n += 1; switch_erreurs += int(accepte != attendu)
                else:
                    repeat_n += 1; repeat_erreurs += int(accepte != attendu)
            precedent = cible
        return {"exact": ok / max(1, n), "faux_positifs": fp, "faux_negatifs": fn, "n": n,
                "cout_commutation": (switch_erreurs / max(1, switch_n)
                                     - repeat_erreurs / max(1, repeat_n))}
