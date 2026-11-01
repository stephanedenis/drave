#!/usr/bin/env python3
"""surveille_sessions.py — les fichiers qui bougent, rangés par session.

POURQUOI CET OUTIL. Tout le monde travaille sur le **même arbre** : deux sessions qui écrivent le
même fichier se marchent dessus sans le voir. `sessions.py --check` vérifie les réservations
**déclarées** (périmètres, fichiers) ; cet outil regarde les fichiers **réellement en mouvement**
(`git status`) et les range :

- **par session** : les fichiers qui tombent dans son territoire réservé ;
- **partagés** : l'état, la roadmap, le journal, l'index — réservés au hub (une session à la fois) ;
- **orphelins** : personne ne les réclame — à attribuer, commiter ou supprimer ;
- **conflits** : deux sessions actives les réclament — c'est l'erreur à corriger.

Usage :
  python3 tools/surveille_sessions.py            # résumé + orphelins + conflits
  python3 tools/surveille_sessions.py --tout     # tous les fichiers, un par ligne
  python3 tools/surveille_sessions.py --check    # code 1 si un conflit existe
"""
from __future__ import annotations

import argparse
import fnmatch
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sessions as sess  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
PARTAGES = ("docs/pilotage/en-cours.md", "docs/pilotage/roadmap.md",
            "docs/pilotage/chantiers.md", "docs/pilotage/plan-travail.md",
            "docs/pilotage/README.md", "AGENTS.md", "reports/INDEX.md",
            "tools/surveille_sessions.py", "tools/sessions.py", "tools/docwatch",
            "journal/2026-*", "docs/README.md")


def fichiers_en_mouvement() -> list[str]:
    sortie = subprocess.run(["git", "status", "--porcelain"], cwd=RACINE,
                            capture_output=True, text=True).stdout
    fichiers = []
    for ligne in sortie.splitlines():
        if len(ligne) < 4:
            continue
        chemin = ligne[3:].strip()
        if " -> " in chemin:  # renommage
            chemin = chemin.split(" -> ", 1)[1]
        fichiers.append(chemin.strip('"'))
    return fichiers


def appartient(fichier: str, patron: str) -> bool:
    patron = patron.strip().strip("`").rstrip("/")
    if not patron:
        return False
    if fnmatch.fnmatch(fichier, patron):
        return True
    return fichier == patron or fichier.startswith(patron + "/")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tout", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    plans = [p for p in sess.decouvrir(RACINE) if p["etat"] in sess.ACTIFS]
    fichiers = fichiers_en_mouvement()
    print(f"surveille-sessions · {len(plans)} session(s) active(s) · {len(fichiers)} fichier(s) en mouvement")
    for p in plans:
        age = "—" if p["age"] is None else f"{p['age']:.0f} min"
        print(f"  {p['id'][:18]:18} · {p['etat']:7} · {age:>7} · {len(p['fichiers'])} réservation(s)")
    proprietaires: dict[str, list[str]] = {}
    for f in fichiers:
        noms = [p["id"] for p in plans
                if any(appartient(f, r) for r in p["fichiers"])]
        if any(appartient(f, x) for x in PARTAGES):
            noms = noms + ["hub"] if "hub" not in noms else noms
        proprietaires[f] = noms
    orphelins = [f for f, noms in proprietaires.items() if not noms]
    conflits = [f for f, noms in proprietaires.items() if len(noms) > 1]
    if args.tout:
        for f in sorted(proprietaires):
            print(f"  {' '.join(proprietaires[f]) or 'ORPHELIN':16} {f}")
    else:
        for p in plans:
            siens = [f for f, noms in proprietaires.items() if p["id"] in noms]
            print(f"  {p['id'][:18]:18} · {len(siens)} fichier(s) : " +
                  ", ".join(siens[:6]) + (" …" if len(siens) > 6 else ""))
        hub = [f for f, noms in proprietaires.items() if "hub" in noms]
        print(f"  {'hub (partagé)':18} · {len(hub)} fichier(s) : " +
              ", ".join(hub[:5]) + (" …" if len(hub) > 5 else ""))
    print(f"\n  orphelins ({len(orphelins)}) — à attribuer, commiter ou supprimer :")
    for f in sorted(orphelins)[:20]:
        print(f"    · {f}")
    print(f"  conflits ({len(conflits)}) — deux sessions les réclament :")
    for f in sorted(conflits):
        print(f"    ! {f} — {', '.join(proprietaires[f])}")
    if args.check and conflits:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
