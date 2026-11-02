#!/usr/bin/env python3
"""canal_structure.py — la classe de structure de chaque octet, pour le canal d'annotation.

Le canal est une **seconde entrée** : à chaque octet du texte, une classe (0–5) que le modèle
reçoit en plus de l'octet. Les classes viennent du générateur de structures
([`tools/structures/generateur.py`](../tools/structures/generateur.py)) : mot plein, mot
grammatical, espace, ponctuation, chiffre, et **frontière de proposition**.

    python3 tools/canal_structure.py --entree data/wiki_fr/propre/train.txt --sortie data/wiki_fr/propre/train.canal
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "structures"))
import generateur  # noqa: E402

MOTIF = __import__("re").compile(r"[A-Za-zÀ-ÿ'’-]+|\d+|[.,;:!?…()«»]|\s+|[^\s]")
PLEIN, GRAMMA, ESPACE, PONCT, CHIFFRE, FRONTIERE = 0, 1, 2, 3, 4, 5
CLASSES_GRAM = {"DET", "PREP", "CONJ", "RELATIF", "PRON", "AUX"}
PONCT_FORTE = set(".;:!?…")


def canal(texte: str) -> bytes:
    """Une classe par octet, de la même longueur que `texte.encode('utf-8')`."""
    sortie = bytearray()
    for m in MOTIF.finditer(texte):
        t = m.group()
        n = len(t.encode("utf-8", "surrogateescape"))
        if t.isspace():
            c = ESPACE
        elif t in generateur.PONCT:
            c = PONCT
        elif t.isdigit():
            c = CHIFFRE
        else:
            tok = generateur.Token(t, m.start(), m.end(), False)
            c = GRAMMA if tok.cls in CLASSES_GRAM else PLEIN
        sortie.extend([c] * n)
    return bytes(sortie)


def canal_frontieres(texte: str, classes: bytes) -> bytes:
    """Marque d'une classe `FRONTIERE` le premier octet après une ponctuation forte."""
    sortie = bytearray(classes)
    octets = texte.encode("utf-8", "surrogateescape")
    for i, b in enumerate(octets[:-1]):
        if b in b".;:!?" and octets[i + 1:i + 2] in (b" ", b"\n"):
            j = i + 1
            while j < len(octets) and octets[j:j + 1].isspace():
                j += 1
            if j < len(octets):
                sortie[j] = FRONTIERE
    return bytes(sortie)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--entree", required=True)
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--frontieres", action="store_true")
    a = ap.parse_args()
    with open(a.entree, encoding="utf-8", errors="surrogateescape", newline="") as f:
        texte = f.read()
    c = canal(texte)
    if a.frontieres:
        c = canal_frontieres(texte, c)
    pathlib.Path(a.sortie).write_bytes(c)
    print(f"{len(c)} octets de canal · {a.sortie}", flush=True)


if __name__ == "__main__":
    main()
