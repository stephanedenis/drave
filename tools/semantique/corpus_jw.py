#!/usr/bin/env python3
"""corpus_jw.py — les unités parallèles de La Tour de garde (12 langues), pour B10.2bis.

POURQUOI CE CORPUS. Le protocole sémantique a été mesuré sur 30 articles UDHR (10 langues,
phrases courtes). Le levier « corpus » demande plus de texte et plus de scripts : le
manifeste `data/jw/jw_2026.json` porte **5 articles, 12 langues, 139 unités alignées**
(chaque `num` est le même paragraphe dans toutes les langues). C'est le même contrat que
`corpus.py` — un sens, plusieurs langues — avec des scripts non latins (hin, ben, mar, tel,
urd, jpn) que l'UDHR ne couvrait pas.

Le découpage est fait **par article**, jamais par unité : une unité de validation ne doit pas
se retrouver dans l'entraînement. C'est la fuite la plus facile du protocole.
"""
from __future__ import annotations

import json
import pathlib
import random

from semantique.corpus import octets

RACINE = pathlib.Path(__file__).resolve().parents[2]
JW = RACINE / "data" / "jw" / "jw_2026.json"

LANGUES = ["eng", "hin", "ben", "ind", "urd", "jpn", "mar", "tel", "vie", "swh", "arz", "hau"]
SOURCE = "eng"


def charger(langues: list[str] | None = None, max_art: int | None = None,
            chemin: pathlib.Path | None = None) -> dict[tuple[str, int], dict[str, str]]:
    """Rend {(article, num): {langue: texte}} pour les unités complètes."""
    langues = langues or LANGUES
    manifeste = json.loads((chemin or JW).read_text(encoding="utf-8"))
    out: dict[tuple[str, int], dict[str, str]] = {}
    for unite in manifeste["unites"]:
        textes = unite.get("textes", {})
        if all(l in textes for l in langues):
            out[(unite["article"], int(unite["num"]))] = {l: textes[l] for l in langues}
    return dict(sorted(out.items()))


def decouper(articles: dict, val_article: str | None = None) -> tuple[dict, dict]:
    """Découpage par article : un article entier est la validation."""
    arts = sorted({a for a, _ in articles})
    if len(arts) < 2:
        return articles, {}
    val_art = val_article or "You-Can-Win-the-Battle"
    if val_art not in arts:
        val_art = arts[-1]
    train = {k: v for k, v in articles.items() if k[0] != val_art}
    test = {k: v for k, v in articles.items() if k[0] == val_art}
    return train, test


def exemple(articles: dict, cle, langue: str, seq: int = 128) -> list[int]:
    return octets(articles[cle][langue], seq)


def lot(articles: dict, langues: list[str], lot: int, seq: int,
        rng: random.Random):
    """Un lot de sens : (x_source, langue_source, x_cible, langue_cible, unité)."""
    cles = list(articles)
    choix = [rng.choice(cles) for _ in range(lot)]
    src = [rng.choice(langues) for _ in range(lot)]
    tgt = []
    for s in src:
        autres = [l for l in langues if l != s]
        tgt.append(rng.choice(autres))
    xs = [exemple(articles, c, s, seq) for c, s in zip(choix, src)]
    xt = [exemple(articles, c, t, seq) for c, t in zip(choix, tgt)]
    ids_src = [langues.index(s) for s in src]
    ids_tgt = [langues.index(t) for t in tgt]
    return xs, ids_src, xt, ids_tgt, choix
