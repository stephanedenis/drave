"""graines.py — la robustesse du curriculum `open` sur plusieurs graines.

La `PolitiqueAppriseOuverte` est entraînée (1000 épisodes) sur 5 graines, puis exécutée seule
sur la porte stochastique (graine de bruit = graine d'entraînement) et sur la porte stable.
Le résultat est le taux de but et le nombre d'essais.

    python3 -m tools.pensee.graines --json reports/pensee-graines.json
"""
from __future__ import annotations

import argparse
import json
import pathlib

from .courbe import seule, seule_sto
from .operateurs import (PolitiqueAppriseBouge, PolitiqueAppriseMobile,
                         PolitiqueAppriseOuverte, seule_bouge, seule_mobile)

GRAINES = (0, 1, 2, 3, 4)


def executer() -> list[dict]:
    lignes = []
    for g in GRAINES:
        p = PolitiqueAppriseOuverte(episodes=1000, graine=g)
        p.apprendre()
        ok_sto, pas_sto, essais = seule_sto(p, graine=g)
        ok_s, pas_s = seule(p)
        lignes.append({"graine": g, "etats_q": len(p.q),
                       "sto_but": ok_sto, "sto_pas": pas_sto, "sto_essais": essais,
                       "stable_but": ok_s, "stable_pas": pas_s})
    return lignes


def executer_mobile() -> list[dict]:
    """La porte mobile sur les 5 graines : la même politique réussit-elle aux deux d ?"""
    lignes = []
    for g in GRAINES:
        p = PolitiqueAppriseMobile(episodes=1000, graine=g)
        p.apprendre()
        b0, p0 = seule_mobile(p, 0)
        b1, p1 = seule_mobile(p, 1)
        lignes.append({"graine": g, "etats_q": len(p.q),
                       "d0_but": b0, "d0_pas": p0, "d1_but": b1, "d1_pas": p1})
    return lignes


def executer_bouge() -> list[dict]:
    """La porte qui bouge sur les 5 graines : le but et le nombre de pas."""
    lignes = []
    for g in GRAINES:
        p = PolitiqueAppriseBouge(episodes=1000, graine=g)
        p.apprendre()
        but, pas = seule_bouge(p)
        lignes.append({"graine": g, "etats_q": len(p.q), "but": but, "pas": pas})
    return lignes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", default="")
    args = ap.parse_args()
    lignes = executer()
    for l in lignes:
        print(f"graine {l['graine']}  Q {l['etats_q']:3d}  "
              f"bruit {l['sto_but']}/{l['sto_pas']} pas ({l['sto_essais']} essais)  "
              f"stable {l['stable_but']}/{l['stable_pas']} pas")
    if args.json and "bouge" in args.json:
        lignes_b = executer_bouge()
        for l in lignes_b:
            print(f"graine {l['graine']}  Q {l['etats_q']:3d}  bouge {l['but']}/{l['pas']} pas")
        p = pathlib.Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"date": "2026-11-01", "ligne": "B13", "graines": GRAINES,
                                 "lignes": lignes_b}, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8")
        return 0
    if args.json and "mobile" in args.json:
        lignes_m = executer_mobile()
        for l in lignes_m:
            print(f"graine {l['graine']}  Q {l['etats_q']:3d}  "
                  f"d0 {l['d0_but']}/{l['d0_pas']} pas  d1 {l['d1_but']}/{l['d1_pas']} pas")
        p = pathlib.Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"date": "2026-11-02", "ligne": "B13", "graines": GRAINES,
                                 "lignes": lignes_m}, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8")
        return 0
    if args.json:
        p = pathlib.Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"date": "2026-11-02", "ligne": "B13", "graines": GRAINES,
                                 "lignes": lignes}, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
