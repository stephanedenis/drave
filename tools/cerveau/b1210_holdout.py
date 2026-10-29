#!/usr/bin/env python3
"""b1210_holdout.py — B12.10 : le pipeline sur des codes tenus à l'écart.

Le score publié (96,33 % de complétion) est mesuré sur des codes **stockés** :
M4 retrouve l'épisode, M8 en donne la marginale. Ici, on tient des **codes
entiers** à l'écart (toutes leurs surfaces), on masque un champ non nul, et on
compare trois chemins :

- **M4** : le plus proche voisin parmi les épisodes d'entraînement ;
- **M8** : le prototype `(jeu, action)` consolidé ;
- **pipeline** : `Pipeline.repondre`, c'est-à-dire le chemin réellement branché.

Le contrôle est le même exercice sur les codes **stockés** : M4 doit y être
parfait, et c'est la tautologie que la fiche B12.10 doit remplacer.
"""
from __future__ import annotations

import argparse
import json
import random
from collections import Counter

from semantique.typed_corpus import items
from semantique.universaux import CHAMPS
from cerveau.pipeline import Pipeline

NOMS = tuple(n for n, _ in CHAMPS)
MASQUES = ("vers", "de", "carte", "point", "case", "chemin_0",
           "promotion", "roque", "symbole", "taille", "passe")


def non_nuls(code: dict) -> list[str]:
    return [n for n in MASQUES if code.get(n) is not None]


def cle(code: dict) -> tuple:
    return tuple(sorted(code.items()))


def split(its, graine: int, n_test: int):
    codes = sorted({cle(i.code) for i in its}, key=str)
    rng = random.Random(graine)
    rng.shuffle(codes)
    test = set(codes[:n_test])
    train = [i for i in its if cle(i.code) not in test]
    val = [i for i in its if cle(i.code) in test]
    return train, val


def construire(train):
    p = Pipeline()
    for it in train:
        p.percevoir_item(it)
    p.consolider()
    return p


def eval_m4(p, its):
    n = ok = exact = 0
    for it in its:
        for f in non_nuls(it.code):
            cue = dict(it.code)
            cue[f] = None
            c = p.memoire.classer(cue, 1)
            if not c:
                continue
            ret = c[0][1].code
            n += 1
            ok += int(ret.get(f) == it.code.get(f))
            exact += int(ret == it.code)
    return {"n": n, "champ": ok / n if n else 0.0, "exact": exact / n if n else 0.0}


def eval_proto(p, its):
    n = ok = exact = 0
    couverts = 0
    for it in its:
        proto = p.prototypes.get((it.code.get("jeu"), it.code.get("action")))
        if proto is None:
            continue
        couverts += 1
        for f in non_nuls(it.code):
            n += 1
            ok += int(proto.get(f) == it.code.get(f))
            exact += int(proto == it.code)
    return {"n": n, "champ": ok / n if n else 0.0, "exact": exact / n if n else 0.0,
            "couverts": couverts}


def eval_pipeline(p, its):
    n = ok = 0
    kinds = Counter()
    for it in its:
        for f in non_nuls(it.code):
            cue = dict(it.code)
            cue[f] = None
            kind, r = p.repondre(cue)
            kinds[kind] += 1
            code = r.get("code") if isinstance(r, dict) else None
            if code is None:
                continue
            n += 1
            ok += int(code.get(f) == it.code.get(f))
    return {"n": n, "champ": ok / n if n else 0.0, "chemins": dict(kinds)}


def eval_sans_m4(p, its):
    """M8 seul : on vide la mémoire après consolidation, les prototypes restent."""
    p.memoire.episodes = []
    return eval_proto(p, its)


def principal():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graines", default="1,2,3")
    ap.add_argument("--test", type=int, default=6)
    ap.add_argument("--sortie", default="")
    a = ap.parse_args()
    its = items()
    graines = [int(x) for x in a.graines.split(",") if x.strip()]
    resultats = []
    for g in graines:
        train, val = split(its, g, a.test)
        p = construire(train)
        stocke = eval_m4(p, train)
        test_m4 = eval_m4(p, val)
        proto = eval_proto(p, val)
        sans = eval_sans_m4(p, val)
        pipe = eval_pipeline(p, val)
        resultats.append({
            "graine": g,
            "train_items": len(train), "test_items": len(val),
            "train_codes": len({cle(i.code) for i in train}),
            "test_codes": len({cle(i.code) for i in val}),
            "stocke_m4": stocke,
            "test_m4": test_m4,
            "test_m8": proto,
            "test_m8_sans_m4": sans,
            "test_pipeline": pipe,
        })
    # agrégats
    def moy(cle_, sous=""):
        vals = []
        for r in resultats:
            v = r[cle_]
            if sous:
                v = v[sous]
            vals.append(v)
        return sum(vals) / len(vals)
    ag = {
        "graines": graines,
        "test_codes": a.test,
        "stocke_m4_champ": moy("stocke_m4", "champ"),
        "test_m4_champ": moy("test_m4", "champ"),
        "test_m8_champ": moy("test_m8", "champ"),
        "test_m8_sans_m4_champ": moy("test_m8_sans_m4", "champ"),
        "test_pipeline_champ": moy("test_pipeline", "champ"),
        "test_m4_exact": moy("test_m4", "exact"),
        "test_m8_exact": moy("test_m8", "exact"),
    }
    out = {"agregats": ag, "par_graine": resultats}
    print(json.dumps(out, ensure_ascii=False, indent=1))
    if a.sortie:
        with open(a.sortie, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
            f.write("\n")


if __name__ == "__main__":
    principal()
