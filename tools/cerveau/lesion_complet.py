#!/usr/bin/env python3
"""lesion_complet.py — B21 : dose-réponse et sham sur M3/M5.

M9 avait une table de privations ; ici on fait varier la **dose** (capacité M3,
ordre M5), on mesure les déficits, et on ajoute un **sham** (copie sans effet)
et une **double lésion** M3+M5.
"""
from __future__ import annotations

import json
import random

from .memoire_travail import MemoireTravail
from .predictif import Predictif
from .sequences import corpus


def _seqs():
    return corpus(0, 200, 12)


def _split(seqs, fraction=0.8):
    ordre = list(seqs)
    random.Random(0).shuffle(ordre)
    n = int(len(ordre) * fraction)
    return ordre[:n], ordre[n:]


def mesurer() -> dict:
    seqs = _seqs()
    train, test = _split(seqs)
    out = {"M3": {"capacites": {}}, "M5": {"ordres": {}}, "sham": {},
           "double": {}}
    for cap in (0, 4, 8, 12, 16):
        m = MemoireTravail(cap)
        r = m.span(seqs)
        out["M3"]["capacites"][str(cap)] = {"span": r["span"],
                                            "exact": r["exact"],
                                            "essais": r["essais"]}
    for ordre in (0, 1, 2):
        p = Predictif(cible="source", ordre=ordre, contexte=True, melange=0.5)
        p.entrainer(train)
        r = p.evaluer(test)
        out["M5"]["ordres"][str(ordre)] = {k: r[k] for k in
                                            ("exact", "majoritaire", "surprise",
                                             "gain_surprise", "n")}
    # sham : copie de la mémoire intacte, aucune modification
    m = MemoireTravail(12)
    r = m.span(seqs)
    out["sham"]["M3"] = {"span": r["span"], "exact": r["exact"]}
    p = Predictif(cible="source", ordre=1, contexte=True, melange=0.5)
    p.entrainer(train)
    out["sham"]["M5"] = {"exact": p.evaluer(test)["exact"]}
    # double : capacité 0 + ordre 0
    out["double"]["M3_0_M5_0"] = {"M3_span": out["M3"]["capacites"]["0"]["span"],
                                  "M5_exact": out["M5"]["ordres"]["0"]["exact"]}
    return out


def main() -> None:
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
