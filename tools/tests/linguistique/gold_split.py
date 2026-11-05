"""gold_split.py — le gold 612 coupé en **dev** et **test**, de façon déterministe.

Le problème. Toutes les mesures de la session sont **in-sample** : les règles de segmentation et
d'attachement ont été dessinées en regardant les échecs du même gold qui les mesure. Pour juger
une règle, il faut un gold **tenu à l'écart** : on règle sur `dev`, on évalue sur `test`.

Protocole (fixé ici). Le split est un **hash stable de l'identifiant** (`crc32(id) % 3 == 0` →
test, sinon dev), donc reproductible, insensible à l'ordre et indépendant du contenu. Il est
**stratifié par source** (`hand`, `reel`, `synthetique`) et par langue : on vérifie l'équilibre
dans la fiche. Aucune phrase n'est dupliquée entre les deux ; l'union redonne les 612.

Usage :
    from tools.tests.linguistique.gold_split import dev, test, compter
    ph = charger(); d = dev(ph); t = test(ph)
"""
from __future__ import annotations

import zlib

PART_TEST = 3  # une phrase sur trois va au test


def _est_test(phrase: dict) -> bool:
    return zlib.crc32(str(phrase.get("id", "")).encode()) % PART_TEST == 0


def dev(phrases: list[dict]) -> list[dict]:
    """Les phrases de développement (2/3)."""
    return [p for p in phrases if not _est_test(p)]


def test(phrases: list[dict]) -> list[dict]:
    """Les phrases tenues à l'écart (1/3)."""
    return [p for p in phrases if _est_test(p)]


def compter(phrases: list[dict]) -> dict:
    """L'équilibre du split : phrases, cibles et labels par source et par langue."""
    import collections
    d = {"phrases": 0, "cibles": 0}
    src = collections.Counter()
    lang = collections.Counter()
    for p in phrases:
        d["phrases"] += 1
        d["cibles"] += sum(1 for s in p["segments"] if s.get("cible") or s.get("cibles"))
        src[p.get("source", "?")] += 1
        lang[p.get("langue", "?")] += 1
    d["sources"] = dict(src)
    d["langues"] = dict(lang)
    return d
