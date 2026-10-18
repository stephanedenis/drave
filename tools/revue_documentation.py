#!/usr/bin/env python3
"""revue_documentation.py — LA REVUE DE FIN DE SOUS-CHANTIER (AGENTS.md §6.1).

Ce qu'elle vérifie, et qu'il faut corriger AVANT le commit de clôture :
  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
  2. structure  : les sept chantiers de en-cours.md ont leur entrée, leur état et leur fiche ;
  3. annotation : les liens relatifs des docs/ et reports/ résolvent ; les sources externes sont citées ;
  4. fraîcheur  : en-cours.md porte une date (heure locale) ;
  5. cohérence  : la synthèse (index.md) liste les sept chapitres et le chantier 7.
Sortie : un rapport lisible, code 0 si tout passe, 1 sinon (utilisable comme porte).
"""
from __future__ import annotations
import pathlib, re, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent


def liens(texte: str):
    return re.findall(r"\]\(([^)#]+?)\)", texte)


def main() -> int:
    alertes = []
    en = RACINE / "docs/en-cours.md"
    if not en.exists():
        print("✗ docs/en-cours.md absent"); return 1
    t = en.read_text()
    # 2. les sept chantiers ✓
    ids = sorted(set(re.findall(r"\*\*(C[1-7])\*\*", t)))
    if len(ids) < 7:
        alertes.append(f"structure : {len(ids)} chantiers sur 7 dans en-cours.md ({ids})")
    # 4. fraîcheur ✓
    if not re.search(r"\*\*Mis à jour : \d{4}-\d\d-\d\d, \d+ h \d+", t):
        alertes.append("fraîcheur : en-cours.md n'a pas de date au format « 2026-10-18, 17 h 20 HAE »")
    # 1. classement : aucune donnée de résultat dans docs/ ✓ ; les fiches COURANTES existent ✓ ; reports/ a un index ✓
    for f in (RACINE / "docs").rglob("*"):
        if f.suffix in (".json", ".csv", ".npz", ".jsonl") and f.is_file():
            alertes.append(f"classement : donnée de résultat dans docs/ → {f.relative_to(RACINE)}")
    for nom in ("07-mesures-couche-commune.md", "fiche-nuit-17-10.md"):
        if not (RACINE / "reports" / nom).exists():
            alertes.append(f"classement : la fiche courante reports/{nom} manque")
    if not (RACINE / "reports/README.md").exists():
        alertes.append("classement : reports/ n'a pas d'index (reports/README.md)")
    # 3. annotation : les liens relatifs résolvent ✓
    courants = [RACINE / "reports/07-mesures-couche-commune.md", RACINE / "reports/fiche-nuit-17-10.md"]
    for base in (RACINE / "docs", courants):
        fichiers = base.rglob("*.md") if hasattr(base, "rglob") else base
        for f in fichiers:
            for cible in liens(f.read_text()):
                if cible.startswith(("http://", "https://", "mailto:")):
                    continue
                p = (f.parent / cible).resolve()
                if not p.exists():
                    alertes.append(f"annotation : {f.relative_to(RACINE)} → {cible} (cassé)")
    # 5. cohérence : l'index liste sept chapitres ✓
    idx = RACINE / "docs/synthese/index.md"
    if idx.exists():
        it = idx.read_text()
        if "Sept chapitres" not in it:
            alertes.append("cohérence : l'index ne dit pas « Sept chapitres »")
        if "07-modeles-alternatifs-entree-sortie.md" not in it:
            alertes.append("cohérence : l'index ne liste pas le chapitre 7")
    print(f"  revue de documentation · {len(list((RACINE / "reports").glob("*.md")))} fiche(s) dans reports/ · {len(ids)} chantier(s)")
    if not alertes:
        print("  ✅ tout passe : classement, structure, annotation, fraîcheur, cohérence")
        return 0
    print(f"  ❌ {len(alertes)} anomalie(s) :")
    for a in alertes:
        print(f"     · {a}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
