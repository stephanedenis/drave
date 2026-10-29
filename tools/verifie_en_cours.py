#!/usr/bin/env python3
"""verifie_en_cours.py — l'état doit rester court, structuré, reprenable et multi-session.

Le fichier `docs/pilotage/en-cours.md` est la seule source de l'état. Ce contrôle vérifie :
  1. un budget de **2 000 mots** ;
  2. les **sept sections** du template ;
  3. « Sessions en cours » : une sous-section `### Session ...` par session active, avec
     **Id**, **Rôle**, **Ce qu'elle fait**, **Ce que font les autres**, **Prochaine action**,
     **Bloquants** et **Journal** ;
  4. **10 puces au plus** dans « Ce qui est en cours », sans doublon et sans puce de plus de 80 mots ;
  5. « Les chantiers et leurs bloquants » : une ligne **A**, **B**, **N**, **R** avec un bloquant
     **non vide** (le mot « aucun » est une information, une cellule vide est un oubli) ;
  6. **5 questions ouvertes au plus**, chacune avec ce qui la débloque (`→`) ;
  7. une **prochaine action nommée** dans « Ce qui reste » (A/B/C/N/R) ;
  8. aucune ligne de journal A7.x dans l'état (les mesures vont dans `reports/`).

Usage : python3 tools/verifie_en_cours.py   (code 0 = l'état est reprenable)
"""
from __future__ import annotations
import pathlib
import re

RACINE = pathlib.Path(__file__).resolve().parent.parent
FICHIER = RACINE / "docs/pilotage/en-cours.md"
SECTIONS = [
    "Sessions en cours",
    "Ce qui est en cours",
    "Les chiffres de l'état",
    "Les chantiers et leurs bloquants",
    "Ce qui reste",
    "Les questions ouvertes",
    "La carte",
]
CHAMPS_SESSION = (
    "**Id**",
    "**Rôle**",
    "**Ce qu'elle fait**",
    "**Ce que font les autres**",
    "**Prochaine action**",
    "**Bloquants**",
    "**Journal**",
)
CHANTIERS = ("**A — le moteur**", "**B — l'intelligence**", "**N — le natif**", "**R — le lecteur**")


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


def sessions(section: str) -> list[tuple[str, str]]:
    """Rend [(titre, corps)] des sous-sections `### ...` de « Sessions en cours »."""
    titres = list(re.finditer(r"(?m)^### (.+)$", section))
    blocs = []
    for i, m in enumerate(titres):
        debut = m.end()
        fin = titres[i + 1].start() if i + 1 < len(titres) else len(section)
        blocs.append((m.group(1).strip(), section[debut:fin]))
    return blocs


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

    blocs = sessions(corps_section(texte, "Sessions en cours"))
    if not blocs:
        alertes.append("« Sessions en cours » n'a aucune sous-section `### Session ...`")
    for titre, corps in blocs:
        if not titre.startswith("Session"):
            alertes.append(f"sous-section sans « Session » : « {titre} »")
        for champ in CHAMPS_SESSION:
            if champ not in corps:
                alertes.append(f"session « {titre} » ne dit pas « {champ} »")

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

    chantiers = corps_section(texte, "Les chantiers et leurs bloquants")
    for marqueur in CHANTIERS:
        if marqueur not in chantiers:
            alertes.append(f"« Les chantiers et leurs bloquants » ne couvre pas {marqueur}")
    for ligne in chantiers.splitlines():
        if not ligne.startswith("| **"):
            continue
        cellules = [c.strip() for c in ligne.strip().strip("|").split("|")]
        if len(cellules) != 4:
            alertes.append(f"ligne de chantier à {len(cellules)} cellules (4 attendues) : {ligne[:60]}")
        elif cellules[2] in ("", "—", "-"):
            alertes.append(f"bloquant vide pour {cellules[0]}")

    questions = puces(corps_section(texte, "Les questions ouvertes"))
    if len(questions) > 5:
        alertes.append(f"{len(questions)} questions ouvertes > 5")
    for q in questions:
        if "→" not in q:
            alertes.append(f"question sans ce qui la débloque (`→`) : {q[:60]}")

    reste = corps_section(texte, "Ce qui reste")
    if not re.search(r"\b([ABCNR]\d|C[1-7])", reste):
        alertes.append("« Ce qui reste » ne nomme aucune prochaine action (A/B/C/N/R)")

    if re.search(r"^- \*\*A7\.\d", texte, re.M):
        alertes.append("ligne de journal A7.x dans l'état — la déplacer dans reports/")

    print(f"  en-cours · {n} mots · {len(SECTIONS)} sections · {len(blocs)} session(s) · "
          f"{len(liste)} puces · {len(questions)} questions")
    if not alertes:
        print("  ✅ état court, structuré, multi-session et reprenable")
        return 0
    print(f"  ❌ {len(alertes)} anomalie(s) :")
    for a in alertes:
        print(f"     · {a}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
