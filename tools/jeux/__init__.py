"""jeux — la sémantique des jeux symboliques, puis la logique de la pensée.

Deux étages, dans cet ordre :

1. `codecs` : la **couche linguistique** de chaque jeu — surface (FR/EN,
   notations, diagrammes) → RSN-jeu canonique, avec annotations de bruit ;
2. `regles` + `pensee` : la **logique de la pensée** — les règles du jeu et la
   recherche, qui ne consomment que la RSN (jamais la surface).

Le contrat est dans `rsn.py` ; la mesure et les contrôles dans `mesure.py`.
"""
from . import rsn  # noqa: F401
from .codecs.base import Arbre, Codec, Lecture, codec, detecte_jeu, lit, rend  # noqa: F401

__all__ = ["rsn", "Arbre", "Codec", "Lecture", "codec", "detecte_jeu", "lit", "rend"]
