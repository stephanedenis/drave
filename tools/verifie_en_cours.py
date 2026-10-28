#!/usr/bin/env python3
"""verifie_en_cours.py — l'état doit rester court, structuré et reprenable.

Le fichier `docs/pilotage/en-cours.md` est la seule source de l'état. Ce contrôle vérifie :
  1. un budget de **2 000 mots** ;
  2. les **huit sections** du template ;
  3. une section « Session en cours » avec l'ID DSH, les sous-agents actifs et la reprise ;
  4. **10 puces au plus** dans « Ce qui est en cours », sans doublon et sans puce de plus de 80 mots ;
  5. **5 questions ouvertes au plus** ;
  6. une **prochaine action nommée** dans « Ce qui reste » ;
  7. aucune ligne de journal A7.x dans l'état (les mesures vont dans `reports/`).

Usage : python3 tools/verifie_en_cours.py   (code 0 = l'état est reprenable)
"""
from __future__ import annotations
import pathlib
import re

RACINE = pathlib.Path(__file__).resolve().parent.parent
FICHIER = RACINE / "docs/pilotage/en-cours.md"
SECTIONS = [
    "Session en cours",
    "Ce qui est en cours",
    "Les chiffres de l'état",
    "Où l'on en est",
    "Les sept chantiers, en une ligne",
    "Ce qui reste",
    "Les questions ouvertes",
    "La carte",
]


def mots(texte: str) -> int:
    return len(re.findall(r"\S+", texte))


def corps_section(texte: str, titre: str) -> str:
    m = re.search(rf"^## {re.escape(titre)}\s*$", texte, re.M)
    if not m:
        return ""
    debut = m.end()
    suivant = re.search(r"^## ", texte[debut:], re.M)
    return texte[debut: debut + suivant.start()] if suivant else texte[debut:]


def puces(section: str) -> list[str]:
    return [l.strip("- ").strip() for l in section.splitlines() if l.startswith("- ")]


def main() -> int:
    alertes: list[str] = []
    if not FICHIER.exists():
        print(f"  ❌ {FICHIER.relative_to(RACINE)} manque")
        return 1
    texte = FICHIER.read_text(encoding="utf-8")
    n = mots(texte)
    if n > 2000:
        alertes.append(f"{n} mots > budget 2 000")
    if not re.search(r"^\*\*Mis à jour : 2026-\d\d-\d\d", texte, re.M):
        alertes.append("date « Mis à jour : AAAA-MM-JJ » absente")
    for section in SECTIONS:
        if f"## {section}" not in texte:
            alertes.append(f"section absente : « {section} »")

    session = corps_section(texte, "Session en cours")
    for attendu in ("Id DSH", "Sous-agents actifs", "Reprise"):
        if attendu not in session:
            alertes.append(f"« Session en cours » ne dit pas « {attendu} »")

    en_cours = corps_section(texte, "Ce qui est en cours")
    liste = puces(en_cours)
    if len(liste) > 10:
        alertes.append(f"{len(liste)} puces dans « Ce qui est en cours » > 10")
    vus = set()
    for p in liste:
        if p in vus:
            alertes.append(f"puce en double : {p[:60]}")
        vus.add(p)
        if len(re.findall(r"\S+", p)) > 80:
            alertes.append(f"puce > 80 mots : {p[:60]}")

    questions = puces(corps_section(texte, "Les questions ouvertes"))
    if len(questions) > 5:
        alertes.append(f"{len(questions)} questions ouvertes > 5")

    reste = corps_section(texte, "Ce qui reste")
    if not re.search(r"\b(N\d|B\d|A\d|C\d)", reste):
        alertes.append("« Ce qui reste » ne nomme aucune prochaine action (N/B/A/C)")

    if re.search(r"^- \*\*A7\.\d", texte, re.M):
        alertes.append("ligne de journal A7.x dans l'état — la déplacer dans reports/")

    print(f"  en-cours · {n} mots · {len(SECTIONS)} sections · {len(liste)} puces · {len(questions)} questions")
    if not alertes:
        print("  ✅ état court, structuré et reprenable")
        return 0
    print(f"  ❌ {len(alertes)} anomalie(s) :")
    for a in alertes:
        print(f"     · {a}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
