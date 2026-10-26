#!/usr/bin/env python3
"""grammaire.py — la couche syntaxique : des unités de surface aux motifs.

Ce module ne connaît **aucun** jeu. Il fournit ce dont les codecs ont besoin
pour passer d'une surface à un **arbre** :

- `jetons` : découpe en unités avec leur position (mots, nombres, symboles,
  ponctuation) — la trace qui permet d'annoter « ceci vient de là » ;
- `naturel` : une forme canonique pour les **phrases** (casse pliée, accents
  retirés, ponctuation en espaces), qui laisse vivants les symboles de cartes ;
- `segmente` : découpe une grille ou une liste sur les séparateurs déclarés ;
- `motif` : un petit enrobage de `re` qui rend les groupes nommés et la
  confiance, pour que chaque codec déclare ses motifs au lieu de les cacher.

La règle de conception : **le niveau 3 (grammaire) ne décide pas de la
légalité**. Il produit un arbre avec ce que la surface dit, et marque ce qu'elle
ne dit pas (`None`) ; c'est le niveau 4 (sémantique) qui tranche avec les règles
du jeu. C'est cette séparation qui rend l'ablation mesurable.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Iterable, Match, Pattern

from .lexique import normalise, plie, unites


@dataclass(frozen=True)
class Jeton:
    forme: str
    plie: str
    debut: int
    fin: int
    genre: str  # "mot" | "nombre" | "symbole" | "ponctuation"

    @property
    def est_symbole_carte(self) -> bool:
        return self.forme in "\u2660\u2665\u2666\u2663"


def _genre(u: str) -> str:
    if u in "\u2660\u2665\u2666\u2663":
        return "symbole"
    if u.isdigit():
        return "nombre"
    if re.search(r"[A-Za-zÀ-ÖØ-öø-ÿ]", u):
        return "mot"
    return "ponctuation"


def jetons(texte: str) -> list[Jeton]:
    """Unités avec positions ; la somme des formes redonne la surface normalisée."""
    t = normalise(texte)
    out: list[Jeton] = []
    pos = 0
    for u in unites(t):
        i = t.find(u, pos)
        if i < 0:  # ne devrait pas arriver : la découpe vient de la même chaîne
            i = pos
        out.append(Jeton(u, plie(u), i, i + len(u), _genre(u)))
        pos = i + len(u)
    return out


def naturel(texte: str) -> str:
    """Forme de phrase : minuscules, sans accents, ponctuation → espaces.

    On GARDE les symboles de cartes (♥♠♦♣) : ils portent du sens, pas de la
    ponctuation. On garde aussi les lettres et les chiffres, donc `e2e4`,
    `c3xe5`, `a1`, `10h` restent des unités.
    """
    t = unicodedata.normalize("NFD", normalise(texte).casefold())
    from .lexique import sans_diacritiques
    t = sans_diacritiques(t)
    if t.isascii():
        return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\u2660\u2661\u2662\u2663\u2664\u2665\u2666\u2667]+", " ", t)).strip()
    # on garde TOUTE lettre/chiffre Unicode (cyrillique, arabe, CJK, devanagari…)
    # et les quatre symboles de cartes ; le reste devient un espace.
    out = []
    for c in t:
        if c.isalnum() or unicodedata.category(c).startswith("M") or c in "\u2660\u2661\u2662\u2663\u2664\u2665\u2666\u2667":
            out.append(c)
        else:
            out.append(" ")
    return unicodedata.normalize("NFC", re.sub(r"\s+", " ", "".join(out)).strip())


def nature_lots(texte: str) -> list[str]:
    """Comme `naturel`, mais chaque unité reste séparée (pour les listes)."""
    return naturel(texte).split()


def segmente(texte: str, separateurs: str = r"[/|\n;]+") -> list[str]:
    """Découpe une grille/liste ; nettoie les bords et jette les vides."""
    return [s.strip() for s in re.split(separateurs, normalise(texte)) if s.strip()]


def motif(texte: str, expression: str | Pattern[str], options: int = 0) -> Match[str] | None:
    """Cherche un motif ; l'expression est compilée si nécessaire."""
    m = re.compile(expression, options) if isinstance(expression, str) else expression
    return m.search(texte)


def groupes(m: Match[str] | None) -> dict[str, str]:
    return {k: v for k, v in (m.groupdict().items() if m else []) if v is not None}


def premier_motif(texte: str, motifs: Iterable[str]) -> tuple[str, Match[str]] | None:
    """Le premier motif qui matche, avec sa source — pour nommer le format lu."""
    for source in motifs:
        m = re.search(source, texte)
        if m:
            return source, m
    return None


def nombre(texte: str, defaut: int | None = None) -> int | None:
    """Lit un entier simple (chiffres, ou mot français/anglais via le lexique)."""
    from .lexique import est_nombre

    m = re.search(r"\d+", texte)
    if m:
        return int(m.group(0))
    for u in nature_lots(texte):
        n = est_nombre(u)
        if n is not None:
            return n
    return defaut


def sans_articles(texte: str) -> list[str]:
    """Les unités de contenu : articles et mots vides retirés (pour les motifs)."""
    from .lexique import est_article

    return [u for u in nature_lots(texte) if not est_article(u)]


def contient_un(texte: str, formes: Iterable[str]) -> bool:
    ws = set(nature_lots(texte))
    return any(plie(f) in ws for f in formes)


# Les nombres écrits en toutes lettres, pour les coordonnées et les rangs.
_NOMBRES_ORDINAUX = {
    "premier": 1, "premiere": 1, "first": 1,
    "deuxieme": 2, "second": 2, "seconde": 2, "second": 2, "two": 2,
    "troisieme": 3, "third": 3, "quatrieme": 4, "fourth": 4,
    "cinquieme": 5, "fifth": 5, "sixieme": 6, "sixth": 6,
    "septieme": 7, "seventh": 7, "huitieme": 8, "eighth": 8,
    "neuvieme": 9, "ninth": 9, "dixieme": 10, "tenth": 10,
}


def ordinal(texte: str) -> int | None:
    for u in nature_lots(texte):
        if u in _NOMBRES_ORDINAUX:
            return _NOMBRES_ORDINAUX[u]
    return None
