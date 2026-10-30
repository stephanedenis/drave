#!/usr/bin/env python3
"""taille_documents.py — le budget de contexte et la cohésion des documents.

Ce que l'outil vérifie :
  1. la taille des documents **chargeables** (T0/T1) en mots, avec un budget par catégorie ;
  2. la cohésion minimale : un titre, un résumé en tête, et pour les documents datés un
     « Résumé » + « ne pas charger par défaut » ;
  3. les fiches de résultats trop longues pour être lues d'un bloc (avertissement, pas échec) ;
  4. le classement des plus gros documents, pour voir où le contexte part.

Les fiches de `reports/` (sauf `reports/README.md`) et le `journal/` sont **hors budget** :
ils ne sont pas chargés automatiquement. Le budget est en **mots** ; l'estimation de tokens
est donnée à titre indicatif (≈ caractères / 4).

Les **sources de diagrammes** (` ```plantuml `, ` ```mermaid `) sont **rendues, pas lues** :
elles ne comptent pas dans le budget ; le document les porte, la page montre le SVG.
"""
from __future__ import annotations
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent

# (catégorie, budget en mots). Les globs sont résolus dans l'ordre ; le premier match gagne.
BUDGETS: list[tuple[str, str, int]] = [
    ("T0", "AGENTS.md", 1200),
    ("T0", "docs/pilotage/en-cours.md", 2000),
    ("T1", "docs/methode/organisation-du-depot.md", 1800),
    ("T1", "docs/methode/modularisation.md", 1600),
    ("T1", "docs/methode/relations-humaines.md", 1400),
    ("T0", "docs/methode/*.md", 1200),
    ("T1", "docs/README.md", 1000),
    ("T1", "docs/theorie/carte.md", 1100),
    ("T1", "docs/theorie/synthese/index.md", 2000),
    ("T1", "docs/theorie/synthese/0*.md", 2000),
    ("T1", "docs/pilotage/roadmap.md", 9000),
    ("T1", "docs/theorie/glossaire.md", 1500),
    ("T1", "docs/theorie/glossaire/0*.md", 5000),
    ("T1", "docs/theorie/glossaire/1*.md", 5000),
    ("T1", "docs/theorie/glossaire/README.md", 2000),
    ("T1", "docs/schemas/README.md", 1500),
    ("CARTE", "docs/theorie/glossaire/entrees/*.md", 150),
    ("T1", "reports/README.md", 2800),
    ("T1", "README.md", 3500),
    ("T1", "REPRISE.md", 2000),
    ("T1", "docs/pilotage/utilisation.md", 2500),
    ("T1", "docs/pilotage/references-non-regression.md", 2500),
    ("T1", "docs/implantation/format-*.md", 2500),
    ("T1", "docs/theorie/jeux-symboliques.md", 2500),
    ("T1", "docs/theorie/protocole-semantique.md", 2500),
    ("T1", "docs/pilotage/manques.md", 2500),
    ("T1", "docs/theorie/semantique-universaux.md", 2000),
    ("T1", "docs/theorie/vision.md", 1500),
    ("T1", "docs/methode/modularisation.md", 1500),
    ("DATÉ", "docs/implantation/contexte-long.md", 0),
    ("DATÉ", "docs/implantation/numa-segregation.md", 0),
    ("DATÉ", "docs/implantation/convertisseur.md", 0),
    ("DATÉ", "docs/implantation/configuration-nvme-raid-amd.md", 0),
]

DATE_DOCS = {
    "docs/implantation/contexte-long.md",
    "docs/implantation/numa-segregation.md",
    "docs/implantation/convertisseur.md",
    "docs/implantation/configuration-nvme-raid-amd.md",
    "docs/methode/modularisation.md",
    "docs/pilotage/manques.md",
}


def mots(texte: str) -> int:
    return len(re.findall(r"\S+", texte))


#: Une source de diagramme est **rendue**, pas lue comme de la prose : elle ne compte
#: pas dans le budget de contexte. Le rendu (docwatch) est ce que voit le lecteur ;
#: la source reste dans le document pour être révisée avec lui.
DIAGRAMME = re.compile(
    r"^[ \t]*```[ \t]*(?:plantuml|puml|pu|mermaid|mmd)[ \t]*\n.*?^[ \t]*```[ \t]*$",
    re.MULTILINE | re.DOTALL,
)


def mots_hors_diagrammes(texte: str) -> int:
    return mots(DIAGRAMME.sub("", texte))


def classe(rel: str) -> tuple[str, int]:
    for cat, motif, budget in BUDGETS:
        if pathlib.Path(rel).match(motif):
            return cat, budget
    return "", 0


def main() -> int:
    lignes: list[tuple[int, int, str, str, int]] = []
    violations: list[str] = []
    avertissements: list[str] = []
    specifiques = {"organisation-du-depot.md", "modularisation.md", "relations-humaines.md"}
    for cat, motif, budget in BUDGETS:
        for p in sorted(RACINE.glob(motif)):
            if not p.is_file():
                continue
            if motif == "docs/methode/*.md" and p.name in specifiques:
                continue
            rel = str(p.relative_to(RACINE))
            t = p.read_text(encoding="utf-8", errors="ignore")
            n = mots_hors_diagrammes(t)
            lignes.append((n, t.count("\n") + 1, rel, cat, budget))
            tete = "\n".join(t.splitlines()[:20])
            if cat in ("T0", "T1"):
                if not t.lstrip().startswith("#"):
                    violations.append(f"{rel} : pas de titre (#) en tête")
                if "> " not in tete:
                    violations.append(f"{rel} : pas de résumé (blockquote) dans les 20 premières lignes")
            if rel in DATE_DOCS:
                if "Résumé" not in tete:
                    violations.append(f"{rel} : document daté sans « Résumé » en tête")
                if "ne pas charger" not in tete.lower() and "ne jamais charger" not in tete.lower():
                    violations.append(f"{rel} : document daté sans consigne « ne pas charger par défaut »")
            if budget and n > budget:
                violations.append(f"{rel} : {n} mots > budget {budget} ({cat})")

    # fiches de résultats trop longues : avertissement, pas échec
    longues = []
    for p in sorted((RACINE / "reports").glob("*.md")):
        if p.name in ("README.md", "INDEX.md") or p.name.startswith("historique-"):
            continue
        n = p.read_text(encoding="utf-8", errors="ignore").count("\n") + 1
        if n > 300:
            longues.append((n, p.name))
    if longues:
        longues.sort(reverse=True)
        avertissements.append(
            f"{len(longues)} fiche(s) > 300 lignes : lire le verdict + une section, jamais tout "
            f"(plus longues : {', '.join(f'{n} l. {nom}' for n, nom in longues[:5])})"
        )

    # T0 : la somme des trois lectures par défaut
    def poids(rel: str) -> int:
        q = RACINE / rel
        return mots_hors_diagrammes(q.read_text(encoding="utf-8", errors="ignore")) if q.exists() else 0

    agents = list((RACINE / "docs/methode").glob("*.md"))
    t0 = poids("AGENTS.md") + poids("docs/pilotage/en-cours.md") + max(
        (poids(str(a.relative_to(RACINE))) for a in agents), default=0
    )
    if t0 > 4000:
        violations.append(f"T0 : {t0} mots (AGENTS + en-cours + une tâche) > budget 4 000")

    # classement
    lignes.sort(reverse=True)
    print("  budget de contexte · documents chargeables")
    print(f"  {'mots':>6} {'lignes':>6} {'cat':>4} {'budget':>6}  document")
    for n, l, rel, cat, budget in lignes[:18]:
        print(f"  {n:6d} {l:6d} {cat:>4} {budget:6d}  {rel}")

    print(f"  T0 max : {t0} mots (budget 4 000)")

    if avertissements:
        print("\n  avertissements :")
        for a in avertissements:
            print(f"     · {a}")
    if violations:
        print(f"\n  ❌ {len(violations)} violation(s) :")
        for v in violations:
            print(f"     · {v}")
        return 1
    print("\n  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
