"""audit.py — l'audit des mesures « seule » : le but rendu est-il l'état final ?

Le bug de `seule_minute` (round 31) comparait un triplet à un couple : la mesure rendait un
échec qui n'existait pas. Cet audit vérifie, pour chaque politique et chaque labyrinthe, que
`but == (état final == P_BUT)` et que `pas == len(chemin)`. Toute incohérence est une mesure
fausse, pas un résultat.

    python3 -m tools.pensee.audit --json reports/pensee-audit.json
"""
from __future__ import annotations

import argparse
import json
import pathlib

from .courbe import trace_seule, trace_seule_minute, trace_seule_sto
from .operateurs import (P_BUT, PolitiqueApprise, PolitiqueAppriseComplete,
                         PolitiqueAppriseMinute, PolitiqueMLP, PolitiqueReseau)

POLITIQUES = (
    ("stable", PolitiqueApprise, dict(episodes=200, graine=0)),
    ("minute", PolitiqueAppriseMinute, dict(episodes=200, graine=0)),
    ("complete", PolitiqueAppriseComplete, dict(episodes=1000, graine=0)),
    ("reseau", PolitiqueReseau, dict(episodes=200)),
    ("mlp", PolitiqueMLP, dict(epochs=200)),
)

MONDES = (
    ("stable", trace_seule),
    ("minute", trace_seule_minute),
    ("stochastique", trace_seule_sto),
)


def auditer() -> list[dict]:
    lignes = []
    for nom, C, kw in POLITIQUES:
        p = C(**kw)
        p.apprendre()
        for monde, f in MONDES:
            if monde == "stochastique":
                but, pas, final, chemin = f(p, graine=0)[0], f(p, graine=0)[1], f(p, graine=0)[3], f(p, graine=0)[4]
            else:
                but, pas, final, chemin = f(p)
            coherent = (but == (tuple(final[:2]) == P_BUT)) and (pas == len(chemin))
            lignes.append({"politique": nom, "monde": monde, "but": but,
                           "final": list(final[:2]), "pas": pas,
                           "chemin": len(chemin), "coherent": coherent})
    return lignes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", default="")
    args = ap.parse_args()
    lignes = auditer()
    for l in lignes:
        etat = "✅" if l["coherent"] else "❌"
        print(f"{etat} {l['politique']:9s} {l['monde']:13s} but={l['but']!s:5s} "
              f"final={l['final']} pas={l['pas']:3d} chemin={l['chemin']:3d}")
    if args.json:
        p = pathlib.Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"date": "2026-11-02", "ligne": "B13",
                                 "coherents": sum(1 for l in lignes if l["coherent"]),
                                 "total": len(lignes), "lignes": lignes},
                                ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0 if all(l["coherent"] for l in lignes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
