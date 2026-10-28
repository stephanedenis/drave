#!/usr/bin/env python3
"""decouper_sous_familles.py — C3.2d : découper l'IE par branche glottolog.

Les corpus de `data/` sont ignorés par git ; ce script les **régénère** depuis
`data/udhr/genealogie.json` et `data/udhr/articles_propres.jsonl`.
"""
from __future__ import annotations

import json
import pathlib

RACINE = pathlib.Path(__file__).resolve().parents[1]
SOUS = {
    "ital1284": "italique",
    "indo1320": "indo_iranien",
    "germ1287": "germanique",
    "balt1263": "baltique",
    "celt1248": "celtique",
}


def generer() -> dict[str, int]:
    g = json.loads((RACINE / "data/udhr/genealogie.json").read_text())
    arts = [json.loads(l) for l in
            (RACINE / "data/udhr/articles_propres.jsonl").read_text().splitlines() if l.strip()]
    sortie = {}
    for code, nom in SOUS.items():
        keep = []
        for a in arts:
            gg = g.get(a["fichier"])
            if not gg or gg.get("famille") != "Indo-European":
                continue
            parts = gg["branche"].split("/")
            if len(parts) > 2 and parts[2] == code:
                keep.append(a)
        p = RACINE / f"data/udhr/familles/ie_{nom}.jsonl"
        p.write_text("\n".join(json.dumps(a, ensure_ascii=False) for a in keep) + "\n")
        sortie[nom] = len(keep)
    return sortie


if __name__ == "__main__":
    print(json.dumps(generer(), ensure_ascii=False, indent=1))
