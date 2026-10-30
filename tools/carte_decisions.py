#!/usr/bin/env python3
"""carte_decisions.py — la carte de décision des chantiers (SVG).

POURQUOI CETTE CARTE EXISTE. Trois vues ont échoué à aider la décision rapide : le WBS d'états
(il ne montre ni les dépendances ni les sources de blocage, et il dérive), le Gantt (il étale le
travail en jours alors qu'on décide par périodes courtes), et le graphe d'items (37 nœuds, juste
pour la lecture d'ensemble mais dense). Ce qui manque est une vue **par chantier**, où la
position verticale n'est pas le temps mais la **profondeur de dépendance** : en haut, ce qui
peut démarrer maintenant ; en dessous, ce que ça débloque ; en rouge, ce qu'une ressource
externe bloque, avec la ressource nommée.

La carte se lit donc de haut en bas comme un ordre de travail, jamais comme un calendrier.

Usage :
  python3 tools/carte_decisions.py --svg docs/schemas/chantiers-decision.svg
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import verifie_backlog as vb  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
LARGEUR, HAUTEUR = 1240, 760
COULOIRS = (("A", "le moteur"), ("B", "l'intelligence"), ("N", "le natif"), ("R", "le lecteur"))
COULEUR = {"A": "#24558f", "B": "#b26a00", "N": "#2e7d32", "R": "#6a1b9a"}
FOND = {"A": "#eaf1fb", "B": "#fdf3e3", "N": "#eaf5ea", "R": "#f3e8f8"}
STATUT = {"mesurée": ("#eeeeee", "#555555"), "prête": ("#c8e6c9", "#2e7d32"),
          "en cours": ("#ffe0b2", "#b26a00"), "partiel": ("#ffe0b2", "#b26a00"),
          "spécifiée": ("#f5f5f5", "#666666"), "bloquée": ("#ffcdd2", "#b03a2e"),
          "sans fiche": ("#fdecea", "#b03a2e")}
POLICE = "Verdana, DejaVu Sans, sans-serif"


def tronque(t: str, n: int) -> str:
    return t if len(t) <= n else t[:n - 1] + "…"


def carte(noeuds: dict, niveau: dict, frontier: list[str], chemin: list[str]) -> str:
    xs = {c: 30 + i * 300 for i, (c, _) in enumerate(COULOIRS)}
    largeur_couloir = 280
    haut = 118
    prof_max = max(niveau.values()) if niveau else 0
    par_case: dict[tuple[str, int], list[str]] = {}
    for n, d in noeuds.items():
        par_case.setdefault((d["programme"], niveau.get(n, 0)), []).append(n)
    for k in par_case:
        par_case[k].sort()
    # la hauteur d'une rangée (une profondeur) = la pile la plus haute d'un couloir : six items
    # à la profondeur 0 de A ne doivent pas chevaucher la profondeur 1.
    hauteurs = [10 + 26 * max((len(v) for (c, prof), v in par_case.items() if prof == d), default=1)
                for d in range(prof_max + 1)]
    y_depart = [haut + sum(hauteurs[:d]) for d in range(prof_max + 1)]
    elements: list[str] = []
    hauteur_totale = max(HAUTEUR, haut + sum(hauteurs) + 130)

    # les couloirs
    for c, nom in COULOIRS:
        elements.append(f'<rect x="{xs[c]}" y="{haut - 34}" width="{largeur_couloir}" '
                        f'height="{hauteur_totale - haut + 10}" rx="9" fill="{FOND[c]}" '
                        f'stroke="{COULEUR[c]}" stroke-width="1" opacity="0.55"/>')
        elements.append(f'<text x="{xs[c] + 10}" y="{haut - 16}" font-family="{POLICE}" '
                        f'font-size="12" font-weight="bold" fill="{COULEUR[c]}">'
                        f'{c} — {nom}</text>')
    # l'axe : la profondeur, pas le temps
    elements.append(f'<text x="16" y="{haut - 6}" font-family="{POLICE}" font-size="9" '
                    f'fill="#555555" transform="rotate(-90 16 {haut - 6})">'
                    f'profondeur de dépendance →</text>')

    # les nœuds
    place: dict[str, tuple[float, float, float, float]] = {}
    for (c, prof), noms in sorted(par_case.items()):
        if c not in xs:
            continue
        for i, n in enumerate(noms):
            d = noeuds[n]
            x = xs[c] + 8
            y = y_depart[min(prof, len(y_depart) - 1)] + i * 26
            w, h = largeur_couloir - 16, 24
            place[n] = (x, y, w, h)
            fond, encre = STATUT.get(d["statut"], ("#f5f5f5", "#666666"))
            bord = "#2e7d32" if n in frontier else encre
            epais = "2.4" if n in frontier else "1"
            elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" '
                            f'fill="{fond}" stroke="{bord}" stroke-width="{epais}"/>')
            elements.append(f'<text x="{x + 6}" y="{y + 16}" font-family="{POLICE}" '
                            f'font-size="8.6" font-weight="bold" fill="{encre}">{n}</text>')
            titre = tronque(d["titre"], 40)
            elements.append(f'<text x="{x + 46}" y="{y + 16}" font-family="{POLICE}" '
                            f'font-size="7.8" fill="#333333">{vb.echapper(titre)}</text>')
            if n in chemin:
                elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" '
                                f'fill="none" stroke="#b03a2e" stroke-width="1.4" '
                                f'stroke-dasharray="3 2"/>')

    # les arêtes (dures) : intra-couloir et inter-couloirs
    for n, d in noeuds.items():
        if n not in place:
            continue
        x1, y1, w1, h1 = place[n]
        for cible, _ in d["dures"]:
            if cible not in place:
                continue
            x2, y2, w2, h2 = place[cible]
            if noeuds[cible]["programme"] == d["programme"]:
                depart = (x1 + w1 / 2, y1)
                arrivee = (x2 + w2 / 2, y2 + h2)
                elements.append(f'<line x1="{depart[0]}" y1="{depart[1]}" x2="{arrivee[0]}" '
                                f'y2="{arrivee[1]}" stroke="#9a9a9a" stroke-width="1"/>')
            else:  # inter-couloirs : la dépendance qui traverse
                depart = (x1 + w1, y1 + h1 / 2)
                arrivee = (x2, y2 + h2 / 2)
                millieu = (depart[0] + arrivee[0]) / 2
                elements.append(
                    f'<path d="M {depart[0]} {depart[1]} C {millieu} {depart[1]}, '
                    f'{millieu} {arrivee[1]}, {arrivee[0]} {arrivee[1]}" fill="none" '
                    f'stroke="#b03a2e" stroke-width="1.4" stroke-dasharray="4 3"/>')
                elements.append(f'<text x="{millieu}" y="{(depart[1] + arrivee[1]) / 2 - 4}" '
                                f'text-anchor="middle" font-family="{POLICE}" font-size="7" '
                                f'fill="#b03a2e">{n}→{cible}</text>')

    # les sources de blocage
    blocages = [(n, d["bloque"]) for n, d in noeuds.items() if d["bloque"] and n in place]
    y_blocage = hauteur_totale - 96
    elements.append(f'<rect x="30" y="{y_blocage}" width="{LARGEUR - 60}" height="64" rx="8" '
                    f'fill="#fdecea" stroke="#b03a2e" stroke-width="1.1"/>')
    elements.append(f'<text x="42" y="{y_blocage + 18}" font-family="{POLICE}" font-size="10" '
                    f'font-weight="bold" fill="#b03a2e">Les sources de blocage (une ressource '
                    f'externe — le graphe ne peut pas la lever)</text>')
    for i, (n, source) in enumerate(blocages):
        elements.append(f'<text x="42" y="{y_blocage + 34 + i * 12}" font-family="{POLICE}" '
                        f'font-size="8.4" fill="#7a2a20">{n} : {vb.echapper(source)}</text>')

    # l'en-tête et la légende
    elements.insert(0, f'<text x="24" y="30" font-family="{POLICE}" font-size="15" '
                       f'font-weight="bold" fill="#1a1a1a">La carte de décision des chantiers</text>')
    elements.insert(1, f'<text x="24" y="48" font-family="{POLICE}" font-size="9" fill="#555555">'
                       f'quatre couloirs · la verticale est la PROFONDEUR DE DÉPENDANCE, pas le '
                       f'temps · vert = peut démarrer (frontière) · orange = en cours · '
                       f'gris = mesuré · rouge = bloqué · pointillé rouge = dépendance entre '
                       f'chantiers · encadré rouge = chemin critique</text>')
    elements.insert(2, f'<text x="24" y="66" font-family="{POLICE}" font-size="9" fill="#2e7d32">'
                       f'frontière ({len(frontier)}) : {", ".join(frontier)}</text>')
    elements.insert(3, f'<text x="24" y="82" font-family="{POLICE}" font-size="9" fill="#b03a2e">'
                       f'chemin critique : {" → ".join(chemin)}</text>')
    titre = ("La carte de décision des chantiers — la profondeur de dépendance comme axe, "
             "les sources de blocage nommées")
    desc = (f"Quatre couloirs (A le moteur, B l'intelligence, N le natif, R le lecteur) ; les "
            f"{len(noeuds)} items du backlog y sont placés par leur profondeur de dépendance, "
            f"pas par une date. La frontière ({len(frontier)} items) est encadrée en vert : ce "
            f"qui peut démarrer maintenant. Les sources de blocage externes sont nommées en bas. "
            f"Le chemin critique est encadré en pointillé rouge.")
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGEUR} {hauteur_totale}" '
            f'role="img" width="{LARGEUR}" height="{hauteur_totale}">\n'
            f'  <title>{vb.echapper(titre)}</title>\n  <desc>{vb.echapper(desc)}</desc>\n'
            f'  <rect x="0" y="0" width="{LARGEUR}" height="{hauteur_totale}" fill="#ffffff"/>\n'
            + "\n".join("  " + e for e in elements) + "\n</svg>\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="La carte de décision des chantiers (SVG).")
    ap.add_argument("--svg", type=pathlib.Path, required=True)
    args = ap.parse_args()
    noeuds = vb.construire()
    erreurs, _avert, niveau = vb.controler(noeuds)
    if erreurs:
        print("❌ le graphe a des erreurs ; carte refusée :")
        for e in erreurs:
            print(f"  · {e}")
        return 1
    frontier = vb.frontiere(noeuds)
    _, chemin_txt = vb.chemin_le_plus_long(noeuds, niveau)
    chemin = chemin_txt.split(" → ")
    args.svg.write_text(carte(noeuds, niveau, frontier, chemin), encoding="utf-8")
    print(f"carte écrite : {args.svg} · {len(noeuds)} items · frontière {len(frontier)} · "
          f"chemin {chemin_txt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
