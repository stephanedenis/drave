#!/usr/bin/env python3
"""typed_corpus.py — les surfaces de jeux avec leur code typé fixe.

La source est le corpus B5/B6 (112 items, formats canoniques) et le corpus
multilingue B7 (449 surfaces, 66 langues). On ne garde que les **coups** : ce
sont les items dont le code typé est complet (source, cible, matériel).
Le découpage se fait **par paire** : les surfaces d'un même sens restent du même
côté ; aucune langue d'une paire de validation n'est vue à l'entraînement.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

from jeux.corpus import construire_corpus
from jeux.corpus_multilingue import construire_corpus_multilingue
from semantique.universaux import code_item


@dataclass(frozen=True)
class ItemType:
    texte: str
    code: dict
    jeu: str
    nature: str
    langue: str
    paire: str
    format: str


def items() -> list[ItemType]:
    out = []
    vus = set()
    for corpus in (construire_corpus(), construire_corpus_multilingue()):
        for it in corpus.items:
            if it.attendu.nature != "coup":
                continue
            cle = (it.texte, it.jeu, it.paire, it.langue)
            if cle in vus:
                continue
            vus.add(cle)
            out.append(ItemType(it.texte, code_item(it), it.jeu, it.attendu.nature,
                                it.langue, it.paire, it.format))
    return out


def decouper(items_: list[ItemType], graine: int = 1, fraction: float = 0.2):
    paires = sorted({i.paire for i in items_ if i.paire})
    rng = random.Random(graine)
    rng.shuffle(paires)
    n_val = max(1, int(len(paires) * fraction))
    val_paires = set(paires[:n_val])
    train = [i for i in items_ if i.paire not in val_paires]
    val = [i for i in items_ if i.paire in val_paires]
    return train, val


def octets(texte: str, seq: int = 64) -> list[int]:
    b = list(texte.encode("utf-8"))[:seq]
    return b if b else [32]


def lot(items_: list[ItemType], lot: int, seq: int, rng: random.Random):
    choix = [rng.choice(items_) for _ in range(lot)]
    return [octets(i.texte, seq) for i in choix], choix


def lot_par_paire(items_: list[ItemType], lot: int, seq: int, rng: random.Random,
                  par_paire: int = 4):
    """Échantillonne des groupes de surfaces de même paire (langues différentes).

    C'est ce qui rend la perte de consistance possible : le lot contient le même
    sens dans plusieurs langues, et le modèle doit produire le même code.
    """
    groupes = {}
    for it in items_:
        groupes.setdefault(it.paire, []).append(it)
    paires = [p for p, v in groupes.items() if len(v) >= 2]
    if not paires:
        return lot(items_, lot, seq, rng)
    n_groupes = max(1, lot // par_paire)
    choix = []
    for _ in range(n_groupes):
        p = rng.choice(paires)
        v = groupes[p]
        if len(v) >= par_paire:
            choix.extend(rng.sample(v, par_paire))
        else:
            choix.extend(rng.choice(v) for _ in range(par_paire))
    return [octets(i.texte, seq) for i in choix], choix
