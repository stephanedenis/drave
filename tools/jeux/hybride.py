"""hybride.py — B11.10b : lire une surface ambiguë quand la phrase nomme le jeu.

Le codec refuse une coordonnée nue (`E4`, `A1`, `d4`, `b6-c5`) sans jeu. Ici,
si la phrase contient « aux échecs », « au go », « aux dames » ou « au morpion »,
on **strippe l'indice** et on passe le jeu explicite au codec. `E4` reste refusé
aux échecs : un SAN exige une position ; le routage est correct, la lecture non.
"""
from __future__ import annotations

import re

from .codecs.base import Lecture, lit

_INDICES = (
    (r"(?:aux?|au|jeu de|jeu d'|partie de|partie d')\s+(?:échecs|echecs)", "echecs"),
    (r"(?:aux?|au|jeu de|jeu d'|partie de|partie d')\s+go", "go"),
    (r"(?:aux?|au|jeu de|jeu d'|partie de|partie d')\s+dames", "dames"),
    (r"(?:aux?|au|jeu de|jeu d'|partie de|partie d')\s+morpion", "morpion"),
)


def lit_avec_indice(texte: str, niveau: int = 4) -> Lecture:
    """Lit `E4 aux échecs` en strippant l'indice ; sans indice, `lit` normal."""
    for motif, jeu in _INDICES:
        m = re.search(motif, texte, re.IGNORECASE)
        if m:
            surface = (texte[:m.start()] + " " + texte[m.end():]).strip(" ,.;:!?")
            return lit(surface, jeu=jeu, niveau=niveau)
    return lit(texte, niveau=niveau)
