#!/usr/bin/env python3
"""fabriquer_colonnes.py — un corpus de pages à DEUX COLONNES, avec sa vérité terrain.

POURQUOI CE FICHIER. R4.4 doit mesurer la **mise en page**, pas seulement les mots : sur une
page à deux colonnes, un lecteur naïf entrelace la gauche et la droite, et le WER mot à mot
le voit (l'ordre compte). Le corpus ONU est mono-colonne : il ne peut pas poser la question.
On fabrique donc des PDF à deux colonnes dont on CONNAÎT l'ordre de lecture — colonne gauche
entière, puis colonne droite — et une version mono-colonne de contrôle.

Le texte vient de `docs/theorie/vision.md` (les docs du dépôt, pas le corpus d'entraînement
de N2). Chaque ligne dessinée est ajoutée à la vérité terrain, donc le WER compare exactement
ce qui a été écrit.

Usage :
  python3 tools/fabriquer_colonnes.py --sortie work/r44/colonnes --pages 10
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

RACINE = pathlib.Path(__file__).resolve().parent.parent
SOURCE = RACINE / "docs/theorie/vision.md"
LARGEUR, HAUTEUR = A4
MARGE = 50.0
INTERLIGNE = 12.5
CORPS = 9.5


def texte_source() -> str:
    """Le texte des docs, sans balisage : des phrases réelles, pas du lorem ipsum."""
    t = SOURCE.read_text(encoding="utf-8")
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    t = re.sub(r"^#+\s*", "", t, flags=re.M)
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"[*_`>|-]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def _mots(texte: str) -> list[str]:
    return texte.split()


def fabrique(sortie: pathlib.Path, pages: int) -> dict:
    sortie.mkdir(parents=True, exist_ok=True)
    mots = _mots(texte_source())
    # Deux colonnes : 2 × 240 pt utiles ; on distribution ~55 caractères par ligne.
    colonne_l = MARGE
    colonne_r = LARGEUR / 2 + 12
    largeur_col = LARGEUR / 2 - MARGE - 12
    lignes_par_colonne = int((HAUTEUR - 2 * MARGE - 40) / INTERLIGNE)
    par_page = 2 * lignes_par_colonne * 9  # ~9 mots par ligne : on avance par paquets
    entrees = []
    for page in range(1, pages + 1):
        depart = ((page - 1) * par_page) % max(len(mots) - par_page, 1)
        paquet = mots[depart:depart + par_page]
        if len(paquet) < par_page:  # on boucle proprement si le texte est court
            paquet += mots[:par_page - len(paquet)]
        moitie = len(paquet) // 2
        colonnes = [" ".join(paquet[:moitie]), " ".join(paquet[moitie:])]
        vrai = []
        for mono, chemin in ((True, sortie / f"colonnes-mono-p{page}.pdf"),
                             (False, sortie / f"colonnes-deux-p{page}.pdf")):
            c = canvas.Canvas(str(chemin), pagesize=A4)
            c.setFont("Helvetica-Bold", 13)
            entete = (f"R4.4 — page {page} — "
                      f"{'mono-colonne (contrôle)' if mono else 'deux colonnes'}")
            c.drawString(MARGE, HAUTEUR - MARGE, entete)
            c.setFont("Helvetica", CORPS)
            if mono:
                # contrôle : le même texte, une seule colonne très large
                texte = " ".join(colonnes)
                lignes = simpleSplit(texte, "Helvetica", CORPS, LARGEUR - 2 * MARGE)
                lignes = lignes[: int((HAUTEUR - 2 * MARGE - 40) / INTERLIGNE)]
                for i, ligne in enumerate(lignes):
                    y = HAUTEUR - MARGE - 30 - i * INTERLIGNE
                    c.drawString(MARGE, y, ligne)
                vrai.append(entete + " " + " ".join(lignes))
            else:
                vrai.append(entete)
                for indice, (x, texte) in enumerate(zip((colonne_l, colonne_r), colonnes)):
                    lignes = simpleSplit(texte, "Helvetica", CORPS, largeur_col)
                    lignes = lignes[:lignes_par_colonne]
                    for i, ligne in enumerate(lignes):
                        y = HAUTEUR - MARGE - 30 - i * INTERLIGNE
                        c.drawString(x, y, ligne)
                    vrai.append(" ".join(lignes))
            c.showPage()
            c.save()
        entrees.append({"page": page, "mono": f"colonnes-mono-p{page}.pdf",
                        "deux": f"colonnes-deux-p{page}.pdf",
                        "verite_mono": vrai[0], "verite_deux": " ".join(vrai[1:])})
    manifeste = {"date": "2026-10-31", "ligne": "R4.4", "nature": "colonnes synthétiques",
                 "source": "docs/theorie/vision.md", "entrees": entrees}
    (sortie / "manifeste.json").write_text(
        json.dumps(manifeste, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return manifeste


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sortie", type=pathlib.Path, default=RACINE / "work/r44/colonnes")
    ap.add_argument("--pages", type=int, default=10)
    args = ap.parse_args()
    m = fabrique(args.sortie, args.pages)
    print(f"  {len(m['entrees'])} pages × 2 versions → {args.sortie}/manifeste.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
