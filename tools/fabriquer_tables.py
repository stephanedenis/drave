#!/usr/bin/env python3
"""fabriquer_tables.py — des pages à TABLEAU, avec la vérité terrain des cellules.

POURQUOI CE FICHIER. R4.1 a mesuré les tableaux **texte** (Markdown/HTML). Un tableau
**scanné** est un autre problème : les cellules n'existent plus, il n'y a que des mots et des
traits. Ce générateur fabrique des pages dont on connaît chaque cellule, pour mesurer
l'extraction (lignes/colonnes/cellules) et pas seulement le WER.

Chaque page : un titre, un tableau à `colonnes` colonnes et `lignes` lignes (dont l'en-tête),
avec des valeurs numériques et des mots, puis un paragraphe. La vérité est écrite en clair.

Usage :
  python3 tools/fabriquer_tables.py --sortie work/r44/tables --pages 10
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

RACINE = pathlib.Path(__file__).resolve().parent.parent
COLONNES = ["Région", "Population", "Taux", "Superficie", "Capitale", "Indice"]
LIGNES = 9
MOTS = ["nord", "sud", "est", "ouest", "centre", "littoral", "montagne", "plaine"]
VILLES = ["Paris", "Lyon", "Lille", "Nice", "Nantes", "Brest", "Metz", "Dijon", "Tours"]
PARAGRAPHES = [
    "Le tableau ci-dessus résume les grandeurs retenues pour la région étudiée.",
    "Les valeurs sont arrondies et proviennent du recensement le plus récent.",
    "La superficie est exprimée en kilomètres carrés, le taux en pourcentage.",
]


def cellule(page: int, ligne: int, colonne: int) -> str:
    if ligne == 0:
        return COLONNES[colonne % len(COLONNES)]
    if colonne == 0:
        return VILLES[(ligne - 1) % len(VILLES)]
    if colonne == 1:
        return f"{120 + page * 7 + ligne * 13} 450"
    if colonne == 2:
        return f"{2 + (ligne % 5)},{(page + ligne) % 10} %"
    if colonne == 3:
        return f"{ligne * 137 + page}"
    if colonne == 4:
        return MOTS[(page + ligne) % len(MOTS)].capitalize()
    return f"{ligne + page}.{(ligne * 3) % 10}"


def fabrique(sortie: pathlib.Path, pages: int, colonnes: int, lignes: int) -> dict:
    sortie.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    entrees = []
    for page in range(1, pages + 1):
        chemin = sortie / f"tableau-p{page}.pdf"
        doc = SimpleDocTemplate(str(chemin), pagesize=A4,
                                leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
        grille = [[cellule(page, l, c) for c in range(colonnes)] for l in range(lignes)]
        tableau = Table(grille, repeatRows=1, colWidths=[(A4[0] - 80) / colonnes] * colonnes)
        tableau.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.7, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
            ("FONT", (0, 0), (-1, -1), "Helvetica", 8.5),
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
            ("ALIGN", (1, 1), (2, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        histoire = [
            Paragraph(f"R4.4 — tableau {page} — {colonnes} colonnes", styles["Title"]),
            Spacer(1, 10),
            tableau,
            Spacer(1, 14),
            Paragraph(PARAGRAPHES[page % len(PARAGRAPHES)], styles["BodyText"]),
        ]
        doc.build(histoire)
        entrees.append({"page": page, "pdf": chemin.name, "colonnes": colonnes,
                        "lignes": lignes, "cellules": grille})
    manifeste = {"date": "2026-10-31", "ligne": "R4.4", "nature": "tableaux synthétiques",
                 "entrees": entrees}
    (sortie / "manifeste.json").write_text(
        json.dumps(manifeste, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return manifeste


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sortie", type=pathlib.Path, default=RACINE / "work/r44/tables")
    ap.add_argument("--pages", type=int, default=10)
    ap.add_argument("--colonnes", type=int, default=6)
    ap.add_argument("--lignes", type=int, default=9)
    args = ap.parse_args()
    m = fabrique(args.sortie, args.pages, args.colonnes, args.lignes)
    print(f"  {len(m['entrees'])} tableaux {args.colonnes}×{args.lignes} → {args.sortie}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
