#!/usr/bin/env python3
"""index_reports.py — génère reports/INDEX.md à partir des en-têtes de fiches.

L'index est **exhaustif** et **déterministe** : une ligne par fiche, triée par nom,
avec son titre (premier `# `). Les fichiers d'infrastructure (`README.md`, `INDEX.md`
et `historique-*`) sont exclus du tableau ; les compteurs de `docs/pilotage/en-cours.md`
comptent, eux, tous les `.md` de `reports/`.

Usage :
    python3 tools/index_reports.py              # réécrit reports/INDEX.md
    python3 tools/index_reports.py --verifier   # ne réécrit rien, sort 1 si périmé
    python3 tools/index_reports.py --aide       # affiche l'aide (ne touche à rien)
"""
from __future__ import annotations

import argparse
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent


def titre(p: pathlib.Path) -> str:
    for ligne in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        if ligne.startswith("# "):
            return ligne[2:].strip().replace("|", "—")
    return p.stem.replace("-", " ")


def fiches() -> list[pathlib.Path]:
    return sorted(
        p for p in (RACINE / "reports").glob("*.md")
        if p.name not in ("README.md", "INDEX.md") and not p.name.startswith("historique-")
    )


def index() -> str:
    fs = fiches()
    lignes = [
        "# Index des fiches de reports/",
        "",
        f"> **Généré** par `tools/index_reports.py` — **{len(fs)} fiches**. Les fichiers",
        "> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;",
        "> la page d'état, elle, compte tous les `.md` de `reports/`.",
        "",
        "| fiche | titre |",
        "|---|---|",
    ]
    lignes += [f"| [{p.name}]({p.name}) | {titre(p)} |" for p in fs]
    return "\n".join(lignes) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Génère reports/INDEX.md (déterministe).")
    ap.add_argument("--verifier", action="store_true",
                    help="ne réécrit rien : compare l'index au disque, sort 1 s'il est périmé")
    ap.add_argument("--aide", action="store_true", help="affiche l'aide et sort")
    args = ap.parse_args()
    if args.aide:
        ap.print_help()
        return 0
    sortie = RACINE / "reports/INDEX.md"
    contenu = index()
    if args.verifier:
        actuel = sortie.read_text(encoding="utf-8") if sortie.exists() else ""
        return 0 if actuel == contenu else 1
    sortie.write_text(contenu, encoding="utf-8")
    print(f"  {len(fiches())} fiches → reports/INDEX.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
