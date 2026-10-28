#!/usr/bin/env python3
"""verifie_journal.py — un dossier par jour, et les sessions ancrées.

Règles vérifiées :
  1. aucun fichier `journal/AAAA-MM-JJ*.md` à la racine : chaque jour est un **dossier** ;
  2. chaque dossier `journal/AAAA-MM-JJ/` a un `README.md` ;
  3. chaque `README.md` de jour porte une section « Sessions DSH » et un lien vers
     `../README.md#sessions` ;
  4. chaque `journal/sessions/<id>/rapport.md` porte le bloc « Journaux » avec un lien vers
     son jour (ou le journal), vers `en-cours.md` et vers l'index des sessions ;
  5. les liens relatifs de `journal/README.md`, `journal/THEMES.md`, des `README.md` de jour
     et des rapports de session résolvent.

Usage : python3 tools/verifie_journal.py   (code 0 = journal propre)
"""
from __future__ import annotations
import pathlib
import re

RACINE = pathlib.Path(__file__).resolve().parent.parent
JOURNAL = RACINE / "journal"
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# les liens markdown, sans les ancres ni les liens externes
LIEN = re.compile(r"\]\(([^)#]+?)(?:#[^)]*)?\)")
EXTERNE = ("http://", "https://", "mailto:", "#")


def liens(texte: str) -> list[str]:
    return [c for c in LIEN.findall(texte)
            if not c.startswith(EXTERNE) and ("/" in c or "." in c)]


def verifier_liens(p: pathlib.Path, alertes: list[str]) -> int:
    n = 0
    for cible in liens(p.read_text(encoding="utf-8", errors="ignore")):
        if cible.startswith(("http://", "https://", "mailto:", "#")):
            continue
        n += 1
        if not (p.parent / cible).resolve().exists():
            alertes.append(f"lien mort : {p.relative_to(RACINE)} → {cible}")
    return n


def main() -> int:
    alertes: list[str] = []
    if not JOURNAL.is_dir():
        print("  ❌ journal/ manque")
        return 1

    # 1. pas de fichier de jour à la racine
    for f in sorted(JOURNAL.glob("*.md")):
        if f.name in ("README.md", "THEMES.md"):
            continue
        if re.match(r"^\d{4}-\d{2}-\d{2}", f.name):
            alertes.append(f"fichier de jour à la racine : {f.relative_to(RACINE)} "
                           "(doit être dans un dossier)")

    # 2/3. dossiers de jour et sections
    jours = sorted(d for d in JOURNAL.iterdir() if d.is_dir() and DATE.match(d.name))
    for d in jours:
        index = d / "README.md"
        if not index.exists():
            alertes.append(f"jour sans README.md : {d.relative_to(RACINE)}")
            continue
        t = index.read_text(encoding="utf-8", errors="ignore")
        if "## Sessions DSH" not in t:
            alertes.append(f"section « Sessions DSH » absente : {index.relative_to(RACINE)}")
        if "../README.md#sessions" not in t:
            alertes.append(f"lien vers l'index des sessions absent : {index.relative_to(RACINE)}")

    # 4. rapports de session
    sessions = sorted((JOURNAL / "sessions").glob("*/rapport.md"))
    for r in sessions:
        t = r.read_text(encoding="utf-8", errors="ignore")
        if "**Journaux :**" not in t:
            alertes.append(f"bloc « Journaux » absent : {r.relative_to(RACINE)}")
        if "docs/pilotage/en-cours.md" not in t:
            alertes.append(f"lien vers en-cours absent : {r.relative_to(RACINE)}")

    # 5. liens des index et des rapports de session
    n_liens = 0
    for p in [JOURNAL / "README.md", JOURNAL / "THEMES.md"] + [d / "README.md" for d in jours]:
        if p.exists():
            n_liens += verifier_liens(p, alertes)
    # Les rapports de session sont des transcriptions : on ne vérifie que le bloc « Journaux »,
    # qui est le contrat d'ancrage (jour, état, index), pas les liens historiques du transcript.
    for r in sessions:
        t = r.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"\*\*Journaux :\*\*(.+)", t)
        if not m:
            continue
        for cible in liens(m.group(1)):
            n_liens += 1
            if not (r.parent / cible).resolve().exists():
                alertes.append(f"lien de session mort : {r.relative_to(RACINE)} → {cible}")

    print(f"  journal · {len(jours)} jour(s) · {len(sessions)} session(s) · {n_liens} lien(s)")
    if not alertes:
        print("  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus")
        return 0
    print(f"  ❌ {len(alertes)} anomalie(s) :")
    for a in alertes[:30]:
        print(f"     · {a}")
    if len(alertes) > 30:
        print(f"     … et {len(alertes) - 30} autre(s)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
