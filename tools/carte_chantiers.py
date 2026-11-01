#!/usr/bin/env python3
"""carte_chantiers.py — la carte des chantiers et de leurs relations (SVG).

POURQUOI CETTE CARTE. La carte de décision (`carte_decisions.py`) lit le backlog A/B/N/R et
répond à « par quoi commencer ». Elle ne montre pas les deux chantiers que les demandes des
48 h ont fait sortir de l'implicite — **L** (le bloc langue, heuristique + neuronal) et **D**
(les données, 10 corpus) — ni **S** (les structures/interprétations) et **B13** (la pensée).
Cette carte-là montre les **huit chantiers et leurs relations** : ce que chacun alimente, ce
qu'il attend, et où sont les ressources partagées.

Usage : python3 tools/carte_chantiers.py --svg docs/schemas/chantiers-vision.svg
"""
from __future__ import annotations

import argparse
import pathlib
import sys

POLICE = "Verdana, DejaVu Sans, sans-serif"
LARGEUR, HAUTEUR = 1260, 720
# (x, y, largeur, hauteur, couleur, fond)
CHANTIERS = {
    "D": dict(case=(60, 96), taille=(200, 86), couleur="#37474f", fond="#eceff1",
              titre="D — les données", sous="10 corpus · 38,8 Go"),
    "L": dict(case=(340, 96), taille=(200, 86), couleur="#6d4c41", fond="#efebe9",
              titre="L — le bloc langue", sous="surface · heuristique + neuronal"),
    "S": dict(case=(620, 96), taille=(200, 86), couleur="#00695c", fond="#e0f2f1",
              titre="S — les structures", sous="candidats · validation humaine"),
    "B": dict(case=(900, 96), taille=(200, 86), couleur="#b26a00", fond="#fdf3e3",
              titre="B — l'intelligence", sous="sens · jeux · B13"),
    "A": dict(case=(60, 330), taille=(200, 86), couleur="#24558f", fond="#eaf1fb",
              titre="A — le moteur", sous="flux typés · rejeu"),
    "N": dict(case=(340, 330), taille=(200, 86), couleur="#2e7d32", fond="#eaf5ea",
              titre="N — le natif", sous="DRVM · distillation"),
    "R": dict(case=(620, 330), taille=(200, 86), couleur="#6a1b9a", fond="#f3e8f8",
              titre="R — le lecteur", sous="preuve d'usage · R0–R4"),
    "P": dict(case=(900, 330), taille=(200, 86), couleur="#b03a2e", fond="#fdecea",
              titre="B13 — la pensée", sous="états pluriels · anytime"),
}
# (source, cible, chemin SVG, libellé, x, y, pointillé)
# Les chemins sont explicites : chaque longue arête passe par un rail (au-dessus, en dessous)
# ou par un canal (les gouttières entre les colonnes), jamais à travers une boîte.
CHEMINS = [
    ("D", "L", "M260,139 L340,139", "corpus", 275, 132, False),
    ("L", "S", "M540,139 L620,139", "annotations", 550, 132, False),
    ("S", "B", "M820,139 L900,139", "pragmatique", 830, 132, False),
    ("A", "N", "M260,373 L340,373", "exécution", 275, 366, False),
    ("N", "R", "M540,373 L620,373", "R1–R3", 550, 366, False),
    ("P", "R", "M900,373 L820,373", "états", 830, 366, False),
    ("L", "N", "M440,182 L440,330", "surface (allège)", 446, 256, False),
    ("D", "N", "M160,182 L160,250 L300,250 L300,373 L340,373", "entraînement", 190, 244, False),
    ("D", "S", "M160,96 L160,76 L720,76 L720,96", "banque", 400, 70, False),
    ("L", "B", "M440,96 L440,88 L860,88 L860,139 L900,139", "résidu ambigu", 600, 82, False),
    ("S", "L", "M720,182 L720,250 L520,250 L520,182", "validations", 600, 244, True),
    ("B", "R", "M1000,182 L1000,250 L860,250 L860,373 L820,373", "B10.3 → R5", 870, 244, True),
    ("A", "B", "M160,416 L160,470 L880,470 L880,139 L900,139", "blocs", 500, 464, True),
    ("P", "L", "M1000,330 L1000,290 L460,290 L460,182", "opérateurs", 700, 284, True),
    ("P", "N", "M1000,416 L1000,480 L440,480 L440,416", "opérateurs", 700, 474, True),
]


def boite(c: dict) -> str:
    x, y = c["case"]
    w, h = c["taille"]
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
            f'fill="{c["fond"]}" stroke="{c["couleur"]}" stroke-width="2"/>'
            f'<text x="{x + w/2}" y="{y + 34}" text-anchor="middle" font-size="16" '
            f'font-weight="bold" fill="{c["couleur"]}">{c["titre"]}</text>'
            f'<text x="{x + w/2}" y="{y + 58}" text-anchor="middle" font-size="11" '
            f'fill="#444">{c["sous"]}</text>')


def centre(c: dict, cote: str) -> tuple[float, float]:
    x, y = c["case"]
    w, h = c["taille"]
    return {"g": (x, y + h / 2), "d": (x + w, y + h / 2),
            "h": (x + w / 2, y), "b": (x + w / 2, y + h)}[cote]


def fleche(src: str, dst: str, chemin: str, libelle: str, lx: float, ly: float,
           pointille: bool) -> str:
    tiret = ' stroke-dasharray="6 5"' if pointille else ""
    return (f'<path d="{chemin}" fill="none" stroke="#546e7a" stroke-width="1.6"{tiret} '
            f'marker-end="url(#pointe)"/>'
            f'<text x="{lx}" y="{ly}" font-size="10" fill="#37474f">{libelle}</text>')


def svg() -> str:
    pieces = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGEUR} {HAUTEUR}" '
              f'width="{LARGEUR}" height="{HAUTEUR}" role="img">',
              '<title>Les huit chantiers de Drave et leurs relations</title>',
              '<desc>D (données) alimente L (bloc langue), N (natif), S (structures) et R '
              '(lecteur) ; L alimente S, B et N ; S alimente B et renvoie ses validations à L ; '
              'A (moteur) exécute N et B ; N porte R1–R3 ; B10.3 attend R5 ; B13 (pensée) '
              'consomme R, L et N. Trait plein : alimente ou débloque ; pointillé : attend ou '
              'plafonne.</desc>',
              '<defs><marker id="pointe" markerWidth="8" markerHeight="8" refX="7" refY="4" '
              'orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#546e7a"/></marker></defs>',
              f'<rect width="{LARGEUR}" height="{HAUTEUR}" fill="#ffffff"/>',
              f'<text x="30" y="40" font-size="20" font-weight="bold" fill="#263238">'
              f'Les huit chantiers et leurs relations</text>',
              f'<text x="30" y="64" font-size="12" fill="#546e7a">'
              f'vue d\u2019ensemble au 2026-11-01 \u00b7 le d\u00e9tail des ar\u00eates '
              f'A/B/N/R est dans docs/pilotage/backlog/dependances.md</text>']
    for c in CHANTIERS.values():
        pieces.append(boite(c))
    for src, dst, chemin, lib, lx, ly, point in CHEMINS:
        pieces.append(fleche(src, dst, chemin, lib, lx, ly, point))
    # légende et ressources
    pieces.append('<rect x="60" y="520" width="520" height="150" rx="8" fill="#fafafa" '
                  'stroke="#cfd8dc"/>')
    pieces.append('<text x="80" y="548" font-size="14" font-weight="bold" fill="#263238">'
                  'Ressources partagées</text>')
    for j, ligne in enumerate([
            'R03 — le banc de lecture : tout le programme R se mesure par lui.',
            'les corpus D — 10 langues, 21,6 M articles, splits, 0 fuite exacte.',
            'le state store — State, Proposal, Score, Decision, Trace (B13, S, L).',
            'les portes — 80 portes, dont la porte OCR-scans et la porte état.']):
        pieces.append(f'<text x="80" y="{574 + j*22}" font-size="11" fill="#37474f">'
                      f'• {ligne}</text>')
    pieces.append('<rect x="620" y="520" width="580" height="150" rx="8" fill="#fafafa" '
                  'stroke="#cfd8dc"/>')
    pieces.append('<text x="640" y="548" font-size="14" font-weight="bold" fill="#263238">'
                  'Les trois chemins</text>')
    for j, ligne in enumerate([
            'du lecteur : R01 → R02 → R03 → R31 → R32 → R51 (profondeur 5).',
            'de la langue : D → L → S → B (la surface, puis les interprétations, puis le sens).',
            'du natif : D → N2 → R1 → R2 → R3 (corpus, modèle, fenêtre, mémoire, restitution).']):
        pieces.append(f'<text x="640" y="{574 + j*22}" font-size="11" fill="#37474f">'
                      f'• {ligne}</text>')
    pieces.append('<text x="640" y="650" font-size="11" fill="#546e7a">'
                  'Trait plein : alimente ou débloque. Pointillé : attend ou plafonne.</text>')
    pieces.append('</svg>')
    return "\n".join(pieces)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--svg", type=pathlib.Path,
                    default=pathlib.Path(__file__).resolve().parent.parent
                    / "docs/schemas/chantiers-vision.svg")
    args = ap.parse_args()
    args.svg.write_text(svg(), encoding="utf-8")
    print(f"→ {args.svg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
