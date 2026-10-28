#!/usr/bin/env python3
"""gating_conflit2.py — B26 : répliquer la mesure de conflit M6 sur A6.

A6 a mesuré un sélecteur de tâche à 94,95 % avec conflit 0 et commutation 0.
B26 en fait une **réplication indépendante** avec la même porte, et vérifie
que le résultat ne dépend pas d'une graine de composition.
"""
from __future__ import annotations

import json

from .gating import Porte


def mesurer() -> dict:
    r = Porte().executer_switch()
    return {
        "exact": r["exact"],
        "n": r["n"],
        "conflit": r.get("effet_conflit"),
        "commutation": r.get("effet_commutation"),
        "base": r.get("taux_base_tout_non"),
        "sensibilite": r.get("sensibilite"),
        "specificite": r.get("specificite"),
    }


def main() -> None:
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
