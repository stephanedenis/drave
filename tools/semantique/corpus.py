#!/usr/bin/env python3
"""corpus.py — les articles UDHR parallèles, pour le protocole sémantique.

Chaque **sens** est un article (1..30), écrit dans plusieurs langues. Le découpage
est fait **par article**, jamais par phrase : une phrase d'un article de validation
ne doit pas se retrouver dans l'entraînement. C'est la fuite la plus facile du
protocole, et la plus difficile à voir ensuite.

Les textes sont byte-level : 256 symboles, aucun tokeniseur à choisir. Le modèle
natif `route` est byte-level ; le protocole reste dans le même alphabet.
"""
from __future__ import annotations

import json
import pathlib
import random

RACINE = pathlib.Path(__file__).resolve().parents[2]
ARTICLES = RACINE / "data" / "udhr" / "articles.jsonl"

LANGUES = ["fra", "spa", "deu", "ita", "por", "rus", "arb", "cmn", "hin", "swh"]


def charger(langues: list[str] | None = None, max_art: int = 30,
            chemin: pathlib.Path | None = None) -> dict[int, dict[str, str]]:
    """Rend {article: {langue: texte}} pour les langues demandées."""
    langues = langues or LANGUES
    garde = set(langues)
    out: dict[int, dict[str, str]] = {}
    for ligne in (chemin or ARTICLES).read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        d = json.loads(ligne)
        iso, art = d.get("iso3"), int(d.get("art", 0))
        if iso in garde and 1 <= art <= max_art:
            out.setdefault(art, {})[iso] = d["texte"]
    # ne garder que les articles complets pour toutes les langues
    return {a: t for a, t in sorted(out.items()) if all(l in t for l in langues)}


def decouper(articles: dict[int, dict[str, str]], val: tuple[int, ...] = (25, 30)):
    """Découpage par article : train hors [val[0], val[1]]."""
    train = {a: t for a, t in articles.items() if not (val[0] <= a <= val[1])}
    test = {a: t for a, t in articles.items() if val[0] <= a <= val[1]}
    return train, test


def octets(texte: str, seq: int = 128) -> list[int]:
    """Les octets UTF-8, tronqués à `seq` ; au moins 8 octets."""
    b = list(texte.encode("utf-8"))[:seq]
    return b if len(b) >= 8 else b + [32] * (8 - len(b))


def exemple(articles: dict[int, dict[str, str]], art: int, langue: str,
            seq: int = 128) -> list[int]:
    return octets(articles[art][langue], seq)


def lot(articles: dict[int, dict[str, str]], langues: list[str], lot: int,
        seq: int, rng: random.Random) -> tuple[list[list[int]], list[int], list[list[int]], list[int], list[int]]:
    """Un lot de sens : (x_source, langue_source, x_cible, langue_cible, article)."""
    arts = list(articles)
    choix = [rng.choice(arts) for _ in range(lot)]
    src = [rng.choice(langues) for _ in range(lot)]
    tgt = []
    for s in src:
        autres = [l for l in langues if l != s]
        tgt.append(rng.choice(autres))
    xs = [exemple(articles, a, s, seq) for a, s in zip(choix, src)]
    xt = [exemple(articles, a, t, seq) for a, t in zip(choix, tgt)]
    ids_src = [langues.index(s) for s in src]
    ids_tgt = [langues.index(t) for t in tgt]
    return xs, ids_src, xt, ids_tgt, choix
