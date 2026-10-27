#!/usr/bin/env python3
"""index_reports.py — génère reports/INDEX.md à partir des en-têtes de fiches.

L'index est **exhaustif** et **déterministe** : une ligne par fiche, triée par nom,
avec son titre (premier `# `). Les fichiers d'infrastructure (`README.md`, `INDEX.md`
et `historique-*`) sont exclus du tableau ; les compteurs de `docs/en-cours.md`
comptent, eux, tous les `.md` de `reports/`.
"""
from __future__ import annotations
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent


def titre(p: pathlib.Path) -> str:
    for ligne in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        if ligne.startswith("# "):
            return ligne[2:].strip().replace("|", "—")
    return p.stem.replace("-", " ")


def main() -> int:
    fiches = sorted(
        p for p in (RACINE / "reports").glob("*.md")
        if p.name not in ("README.md", "INDEX.md") and not p.name.startswith("historique-")
    )
    lignes = [
        "# Index des fiches de reports/",
        "",
        f"> **Généré** par `tools/index_reports.py` — **{len(fiches)} fiches**. Les fichiers",
        "> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;",
        "> la page d'état, elle, compte tous les `.md` de `reports/`.",
        "",
        "| fiche | titre |",
        "|---|---|",
    ]
    for p in fiches:
        lignes.append(f"| [{p.name}]({p.name}) | {titre(p)} |")
    (RACINE / "reports/INDEX.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"  {len(fiches)} fiches → reports/INDEX.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
