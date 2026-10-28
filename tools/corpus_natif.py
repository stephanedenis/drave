#!/usr/bin/env python3
"""corpus_natif.py — N2.1 : fenêtres d'entraînement pour `drave-n0`.

Découpe un corpus d'octets en fenêtres de `fenetre` octets, avec un pas fixe,
puis un split train/validation déterministe. Écrit un manifeste JSON (offsets)
et, si demandé, un fichier binaire concaténé — les corpus de `data/` sont
ignorés par git.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random


def construire(source: str, fenetre: int = 128, pas: int = 64,
               max_fenetres: int = 50_000, val: int = 5_000,
               graine: int = 0) -> dict:
    b = pathlib.Path(source).read_bytes()
    if fenetre < 2 or pas < 1:
        raise ValueError("fenetre >= 2 et pas >= 1")
    if len(b) < fenetre:
        raise ValueError("corpus trop court")
    offsets = list(range(0, len(b) - fenetre + 1, pas))[:max_fenetres]
    rng = random.Random(graine); rng.shuffle(offsets)
    n_val = min(val, len(offsets) // 2)
    return {
        "source": source, "octets": len(b), "fenetre": fenetre, "pas": pas,
        "fenetres": len(offsets), "train": len(offsets) - n_val, "val": n_val,
        "graine": graine, "offsets_train": offsets[n_val:], "offsets_val": offsets[:n_val],
        "licence": "source locale data/corpus_fr.txt — licence à vérifier avant diffusion",
        "note": "manifeste d'offsets ; le corpus n'est pas versionné",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="data/corpus_fr.txt")
    ap.add_argument("--fenetre", type=int, default=128)
    ap.add_argument("--pas", type=int, default=64)
    ap.add_argument("--max", type=int, default=50_000)
    ap.add_argument("--val", type=int, default=5_000)
    ap.add_argument("--graine", type=int, default=0)
    ap.add_argument("--sortie", default="reports/native-corpus.json")
    a = ap.parse_args()
    d = construire(a.source, a.fenetre, a.pas, a.max, a.val, a.graine)
    pathlib.Path(a.sortie).write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps({k: d[k] for k in ("source","octets","fenetres","train","val","fenetre","pas")},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
