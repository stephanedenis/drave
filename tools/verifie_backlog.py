#!/usr/bin/env python3
"""verifie_backlog.py — le graphe des dépendances du backlog, vérifié et dessiné.

POURQUOI CET OUTIL EXISTE. Le backlog est passé de 19 à 29 fiches en une nuit, et les
dépendances ont été écrites à la main, deux fois (la fiche, puis l'index). Un graphe écrit
deux fois diverge : au premier passage, `N5` désignait à la fois l'échelle (roadmap) et la
mémoire (manques), `B10.3` dépendait d'un `B10.2` qui n'a pas de fiche, et `R06` (P1)
dépendait de `R22` (P2) — c'est-à-dire qu'une fiche urgente attendait une fiche moins
urgente. Aucun de ces défauts n'était visible à la lecture : ils ne le sont que si on
parcourt le graphe.

CE QUE L'OUTIL VÉRIFIE
  1. chaque identifiant cité dans « Dépend de » existe (fiche, ligne acquise, ou ligne
     ouverte déclarée sans fiche) — sinon c'est une arête qui ne mène nulle part ;
  2. le graphe est acyclique (les arêtes dures et les plafonds) ;
  3. une fiche « prête » n'a aucune dépendance dure non levée ;
  4. une priorité ne dépend pas d'une priorité plus basse (P1 ← P2 = défaut de graphe) ;
  5. le vocabulaire (statut, priorité, programme) est celui de l'index ;
  6. il calcule la **frontière** : ce qui est réellement non bloqué aujourd'hui, et la
     **profondeur** (le plus long chemin), c'est-à-dire ce qui décide de l'ordre.

TROIS TYPES D'ARÊTE, ET POURQUOI UN SEUL NE SUFFIT PAS
  - **dure** (`Dépend de`)   : l'artefact d'entrée n'existe pas ; la fiche est bloquée ;
  - **douce** (`Plafonné par`) : le travail peut avancer, le résultat est plafonné ;
  - **fait**  (`Contraint par`) : un résultat déjà mesuré contraint le contrat et n'attend
    rien. Confondre « fait » et « dure » fait croire bloqué ce qui est libre : `R21`
    attendait un `N5` (mémoire) déjà mesuré, négatif, et qui ne demande aucun travail.

Usage :
  python3 tools/verifie_backlog.py                 # le rapport, code 0 si cohérent
  python3 tools/verifie_backlog.py --svg docs/schemas/backlog-dependances.svg
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
BACKLOG = RACINE / "docs/pilotage/backlog"

STATUTS = {
    "idée", "spécifiée", "prête", "à faire", "en cours", "partiel", "mesurée",
    "bloquée", "abandonnée",
}
PRIORITES = {"P0", "P1", "P2", "P3"}
PROGRAMMES = {"A", "B", "N", "R"}

# Les lignes mesurées ou closes de la roadmap. Une fiche peut en dépendre : elles ne
# demandent aucun travail, elles sont le socle. (Relevé le 2026-10-29, roadmap § A/B/N.)
ACQUIS = {
    "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8",
    "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10.1",
    "B11", "B12",
    "N0", "N1",
}

# Les lignes ouvertes de la roadmap qui n'ont PAS de fiche. Elles sont des nœuds du graphe
# (elles bloquent des fiches) mais elles ne portent ni porte ni contrôle négatif : c'est un
# trou nommé, pas une ligne du backlog.
SANS_FICHE = {
    "N5": ("Échelle 50–100 M", ["N2", "N4"], "roadmap § N, ligne N5"),
}

# Les contraintes mesurées n'ont pas d'arête : elles sont portées par la clé
# « Contraint par » de chaque fiche, et listées dans les tables du graphe.


def fiches() -> list[pathlib.Path]:
    """Une fiche = un fichier dont le nom porte un id (R01-, N0.3b-, A3.4-…). Les index, le
    modèle et le graphe lui-même ne sont pas des fiches."""
    return sorted(p for p in BACKLOG.glob("*.md") if id_de(p) != p.stem)


def id_de(p: pathlib.Path) -> str:
    m = re.match(r"^([A-Za-z]+[0-9][A-Za-z0-9.]*?)-", p.name)
    return m.group(1) if m else p.stem

def champs(p: pathlib.Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for ligne in p.read_text(encoding="utf-8").splitlines()[:10]:
        if not ligne.startswith(">"):
            continue
        for segment in ligne.lstrip(">").split("·"):
            m = re.match(r"\s*\*\*(.+?)\*\*\s*:\s*(.+?)\s*$", segment)
            if m:
                out[m.group(1).strip()] = m.group(2).strip()
    return out


def liste(valeur: str | None) -> list[tuple[str, str]]:
    """« R01 (schéma), R03 » → [(R01, schéma), (R03, "")]."""
    if not valeur or valeur.strip() in {"—", "-", "aucune"}:
        return []
    out: list[tuple[str, str]] = []
    # la virgule qui sépare deux dépendances n'est pas celle d'une parenthèse
    for morceau in re.split(r",\s*(?![^()]*\))", valeur):
        m = re.match(r"\s*([A-Za-z]+[0-9][A-Za-z0-9.]*)\s*(?:\((.*?)\))?\s*$", morceau)
        if m:
            out.append((m.group(1), (m.group(2) or "").strip()))
    return out


def construire():
    noeuds: dict[str, dict] = {}
    for p in fiches():
        c = champs(p)
        nid = id_de(p)
        titre = p.read_text(encoding="utf-8").splitlines()[0].lstrip("#").strip()
        titre = re.sub(r"^[A-Za-z0-9.]+ — ", "", titre)
        noeuds[nid] = {
            "titre": titre,
            "fiche": p.name,
            "statut": c.get("Statut", ""),
            "prio": c.get("Priorité", ""),
            "programme": c.get("Programme", nid[0]),
            "ligne": c.get("Ligne de roadmap", ""),
            "dures": liste(c.get("Dépend de")),
            "douces": liste(c.get("Plafonné par")),
            "faits": [
                f.strip() for f in re.split(r"[;]", c.get("Contraint par", "")) if f.strip()
            ],
            "bloque": c.get("Bloqué par", ""),
            "sans_fiche": False,
        }
    for nid, (titre, deps, note) in SANS_FICHE.items():
        noeuds[nid] = {
            "titre": titre, "fiche": "", "statut": "sans fiche", "prio": "—",
            "programme": nid[0], "ligne": nid,
            "dures": [(d, "") for d in deps], "douces": [], "faits": [],
            "bloque": "", "sans_fiche": True, "note": note,
        }
    return noeuds


def arreter(noeuds: dict, erreurs: list[str], avertissements: list[str]) -> None:
    niveau = {n: 0 for n in noeuds}
    vus: set[str] = set()

    def profondeur(n: str) -> int:
        if n in vus:
            return niveau.get(n, 0)
        vus.add(n)
        for d, _ in noeuds[n]["dures"] + noeuds[n]["douces"]:
            if d in noeuds:
                niveau[n] = max(niveau[n], profondeur(d) + 1)
        return niveau[n]

    sys.setrecursionlimit(10_000)
    for n in noeuds:
        profondeur(n)


def controler_index(noeuds: dict, erreurs: list[str]) -> None:
    """L'index et les fiches disent-ils le MÊME statut ? Le backlog est écrit deux fois (la
    fiche, puis l'index) ; un graphe écrit deux fois diverge — c'est la raison d'être de cet
    outil. Sans ce contrôle, l'index peut annoncer « spécifiée » une fiche mesurée depuis
    trois versions (arrivé à R05 et R06)."""
    index = (BACKLOG / "index.md").read_text(encoding="utf-8")
    vus = set()
    for ligne in index.splitlines():
        m = re.match(r"\|\s*([A-Z]\d+(?:\.\d+)?[a-z0-9]*)\s*\|\s*[^|]+\|\s*([^|]+)\|", ligne)
        if not m:
            continue
        nid, statut_index = m.group(1).strip(), m.group(2).strip()
        if nid not in noeuds or noeuds[nid]["sans_fiche"]:
            continue
        vus.add(nid)
        if noeuds[nid]["statut"] != statut_index:
            erreurs.append(f"{nid} : l'index dit « {statut_index} », la fiche dit "
                           f"« {noeuds[nid]['statut']} »")
    for nid, noeud in noeuds.items():
        if not noeud["sans_fiche"] and nid not in vus:
            erreurs.append(f"{nid} : fiche absente de l'index")


def controler(noeuds: dict):
    erreurs: list[str] = []
    avert: list[str] = []
    tous = set(noeuds)

    # 1. les arêtes mènent quelque part
    for n, d in noeuds.items():
        for cible, note in d["dures"] + d["douces"]:
            if cible not in tous and cible not in ACQUIS:
                erreurs.append(f"{n} dépend de {cible}, qui n'existe pas (ni fiche, ni ligne acquise)")

    # 2. le vocabulaire
    for n, d in noeuds.items():
        if d["sans_fiche"]:
            continue
        if d["statut"] not in STATUTS:
            erreurs.append(f"{n} : statut « {d['statut']} » hors vocabulaire")
        if d["prio"] not in PRIORITES:
            erreurs.append(f"{n} : priorité « {d['prio']} » hors vocabulaire")
        if d["programme"] not in PROGRAMMES:
            erreurs.append(f"{n} : programme « {d['programme']} » hors vocabulaire")

    # 3. acyclicité (arêtes dures + plafonds)
    niveau = {n: 0 for n in noeuds}
    vus: set[str] = set()

    def prof(n: str, pile: tuple[str, ...] = ()) -> int:
        if n in pile:
            erreurs.append("cycle : " + " → ".join(pile + (n,)))
            return 0
        if n in vus:
            return niveau[n]
        vus.add(n)
        for d, _ in noeuds[n]["dures"] + noeuds[n]["douces"]:
            if d in noeuds:
                niveau[n] = max(niveau[n], prof(d, pile + (n,)) + 1)
        return niveau[n]

    for n in noeuds:
        prof(n)

    # 4. « prête » = aucune dépendance dure non levée
    leve = {"mesurée", "abandonnée"}
    for n, d in noeuds.items():
        if d["statut"] != "prête":
            continue
        for cible, _ in d["dures"]:
            if cible in noeuds and noeuds[cible]["statut"] not in leve:
                erreurs.append(
                    f"{n} est dite prête mais dépend de {cible} ({noeuds[cible]['statut']})"
                )

    # 5. une priorité ne dépend pas d'une priorité plus basse
    for n, d in noeuds.items():
        if d["prio"] not in PRIORITES:
            continue
        for cible, _ in d["dures"]:
            if cible in noeuds and noeuds[cible]["prio"] in PRIORITES:
                if int(noeuds[cible]["prio"][1]) > int(d["prio"][1]):
                    avert.append(
                        f"priorité : {n} ({d['prio']}) dépend de {cible} "
                        f"({noeuds[cible]['prio']}) — l'urgent attend le moins urgent"
                    )

    # 6. les dépendances dures sans fiche : un trou nommé, pas une erreur
    for n, d in noeuds.items():
        for cible, _ in d["dures"]:
            if cible in noeuds and noeuds[cible]["sans_fiche"]:
                avert.append(f"trou : {n} dépend de {cible}, qui n'a pas de fiche")

    controler_index(noeuds, erreurs)
    return erreurs, avert, niveau


def frontiere(noeuds: dict) -> list[str]:
    """Ce sur quoi on peut travailler aujourd'hui : aucune dépendance dure non levée, et
    aucun blocage externe nommé. Une ligne « en cours » ou « partielle » en fait partie :
    non bloquée ne veut pas dire non commencée."""
    leve = {"mesurée", "abandonnée"}
    out = []
    for n, d in sorted(noeuds.items()):
        if d["statut"] in leve or d["bloque"]:
            continue
        libre = True
        for cible, _ in d["dures"]:
            if cible in noeuds and noeuds[cible]["statut"] not in leve:
                libre = False
        if libre:
            out.append(n)
    return out


def chemin_le_plus_long(noeuds: dict, niveau: dict) -> tuple[int, str]:
    fin = max(niveau, key=lambda n: niveau[n]) if niveau else ""
    chemin = [fin]
    while True:
        dures = [d for d, _ in noeuds[chemin[-1]]["dures"] if d in noeuds]
        if not dures:
            break
        suivant = max(dures, key=lambda d: niveau[d])
        if niveau[suivant] >= niveau[chemin[-1]]:
            break
        chemin.append(suivant)
    return niveau.get(fin, 0), " → ".join(reversed(chemin))


# --------------------------------------------------------------------------- le dessin

COULEURS = {
    "A": ("#eaf1fb", "#24558f"),
    "B": ("#f5ecfd", "#6a2c91"),
    "N": ("#e8f7ee", "#1e6b46"),
    "R": ("#fff3e2", "#96550a"),
}
BOITE_L, BOITE_H, ECART, MARGE_G = 174, 52, 30, 54
PAR_LIGNE = 6


def decouper(texte: str, largeur: int = 23, lignes_max: int = 2) -> list[str]:
    mots, lignes, courante = texte.split(), [], ""
    for mot in mots:
        candidat = (courante + " " + mot).strip()
        if len(candidat) <= largeur:
            courante = candidat
        else:
            if courante:
                lignes.append(courante)
            courante = mot
            if len(lignes) == lignes_max:
                break
    if courante and len(lignes) < lignes_max:
        lignes.append(courante)
    if not lignes:
        lignes = [texte[:largeur]]
    reste = " ".join(mots[len(" ".join(lignes).split()):])
    if reste and lignes:
        lignes[-1] = (lignes[-1][:largeur - 1] + "…") if len(lignes[-1]) >= largeur else lignes[-1]
    return lignes


def echapper(texte: str) -> str:
    return texte.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def dessiner(noeuds: dict, niveau: dict, chemin: pathlib.Path) -> None:
    couche: dict[int, list[str]] = {}
    ordre_prog = "ABNR"
    for n, d in noeuds.items():
        couche.setdefault(niveau[n], []).append(n)
    for c in couche.values():
        c.sort(key=lambda n: (ordre_prog.index(noeuds[n]["programme"]), n))

    lignes: list[list[str]] = []
    for c in sorted(couche):
        noeuds_c = couche[c]
        for i in range(0, len(noeuds_c), PAR_LIGNE):
            lignes.append(noeuds_c[i:i + PAR_LIGNE])

    colonnes = max(len(l) for l in lignes) if lignes else 1
    largeur = MARGE_G + colonnes * (BOITE_L + ECART) - ECART + 26
    hauteur = 74 + len(lignes) * (BOITE_H + 24) + 78

    pos: dict[str, tuple[float, float]] = {}
    for i, ligne in enumerate(lignes):
        y = 74 + i * (BOITE_H + 24)
        depart = MARGE_G + (colonnes - len(ligne)) * (BOITE_L + ECART) / 2
        for j, n in enumerate(ligne):
            pos[n] = (depart + j * (BOITE_L + ECART), y)

    # Chaque arête reçoit un couloir : les segments horizontaux vivent dans la bande libre
    # entre deux rangées (jamais au-dessus d'une boîte), les longues arêtes descendent le
    # rail de gauche (x < marge), qui ne croise aucune boîte.
    couloir: dict[tuple[str, str], int] = {}
    for n, d in noeuds.items():
        for cible, _ in d["dures"] + d["douces"]:
            if cible in noeuds:
                couloir[(n, cible)] = len(couloir) % 3

    def arete(n: str, cible: str, genre: str) -> list[str]:
        x1, y1 = pos[n]
        x2, y2 = pos[cible]
        x1 += BOITE_L / 2
        x2 += BOITE_L / 2
        couleur = "#3a3a3a" if genre == "dure" else "#b26a00"
        marqueur = "fleche" if genre == "dure" else "fleche-douce"
        style = f'stroke="{couleur}" stroke-width="{1.3 if genre == "dure" else 1.1}" fill="none"'
        if genre == "douce":
            style += ' stroke-dasharray="4 3"'
        couloir_n = couloir.get((n, cible), 0)
        bande_source = y1 + BOITE_H + 5 + couloir_n * 5
        bande_cible = y2 - 6 - couloir_n * 5
        adjacente = niveau[cible] == niveau[n] + 1
        if adjacente and abs(x1 - x2) < 1:
            chemin_d = f"M {x1:.0f} {y1 + BOITE_H:.0f} V {y2 - 6:.0f}"
        elif adjacente:
            chemin_d = (
                f"M {x1:.0f} {y1 + BOITE_H:.0f} V {bande_source:.0f} "
                f"H {x2:.0f} V {y2 - 6:.0f}"
            )
        else:
            rail = 16 + couloir_n * 9
            chemin_d = (
                f"M {x1:.0f} {y1 + BOITE_H:.0f} V {bande_source:.0f} H {rail:.0f} "
                f"V {bande_cible:.0f} H {x2:.0f} V {y2 - 6:.0f}"
            )
        return [f'  <path d="{chemin_d}" {style} marker-end="url(#{marqueur})"/>']

    sortie = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largeur:.0f} {hauteur:.0f}" '
        f'role="img" width="{largeur:.0f}" height="{hauteur:.0f}">',
        "  <title>Le graphe des dépendances du backlog Drave</title>",
        "  <desc>Trente-sept nœuds : les vingt-neuf fiches du backlog, les huit lignes "
        "ouvertes sans fiche et les dépendances dures et douces entre elles. Les flèches "
        "pleines sont des dépendances dures, les pointillés des plafonds. La lecture va de "
        "haut en bas ; un nœud sans flèche entrante est non bloqué.</desc>",
        "  <defs>",
        '    <marker id="fleche" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto-start-reverse">',
        '      <path d="M 0 0 L 10 5 L 0 10 z" fill="#3a3a3a"/>',
        "    </marker>",
        '    <marker id="fleche-douce" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto-start-reverse">',
        '      <path d="M 0 0 L 10 5 L 0 10 z" fill="#b26a00"/>',
        "    </marker>",
        "  </defs>",
        f'  <rect x="0" y="0" width="{largeur:.0f}" height="{hauteur:.0f}" fill="#ffffff"/>',
        '  <text x="16" y="24" font-family="Verdana, DejaVu Sans, sans-serif" font-size="14" '
        'font-weight="bold" fill="#1a1a1a">Le graphe des dépendances du backlog</text>',
        '  <text x="16" y="42" font-family="Verdana, DejaVu Sans, sans-serif" font-size="9" '
        'fill="#555555">lecture de haut en bas · plein = dépendance dure · pointillé = plafond '
        '· bord interrompu = bloquée ou sans fiche · 2026-10-29</text>',
    ]

    for n, (x, y) in sorted(pos.items(), key=lambda kv: (kv[1][1], kv[1][0])):
        d = noeuds[n]
        fill, trait = COULEURS[d["programme"]]
        if d["sans_fiche"]:
            fill, trait = "#fdecea", "#b03a2e"
        pointille = ' stroke-dasharray="5 3"' if (d["sans_fiche"] or d["statut"] == "bloquée") else ""
        sortie.append(
            f'  <rect x="{x:.0f}" y="{y:.0f}" width="{BOITE_L}" height="{BOITE_H}" rx="7" '
            f'fill="{fill}" stroke="{trait}" stroke-width="1.3"{pointille}/>'
        )
        sortie.append(
            f'  <text x="{x + 9:.0f}" y="{y + 16:.0f}" font-family="Verdana, DejaVu Sans, '
            f'sans-serif" font-size="10.5" font-weight="bold" fill="{trait}">{echapper(n)}</text>'
        )
        for k, ligne in enumerate(decouper(d["titre"])):
            sortie.append(
                f'  <text x="{x + 9:.0f}" y="{y + 30 + k * 11:.0f}" '
                f'font-family="Verdana, DejaVu Sans, sans-serif" font-size="8.2" '
                f'fill="#333333">{echapper(ligne)}</text>'
            )
        if d["sans_fiche"]:
            sortie.append(
                f'  <text x="{x + BOITE_L - 8:.0f}" y="{y + 16:.0f}" text-anchor="end" '
                f'font-family="Verdana, DejaVu Sans, sans-serif" font-size="7.5" '
                f'fill="#b03a2e">sans fiche</text>'
            )

    for n, d in noeuds.items():
        for cible, _ in d["dures"]:
            if cible in noeuds:
                sortie += arete(n, cible, "dure")
    for n, d in noeuds.items():
        for cible, _ in d["douces"]:
            if cible in noeuds:
                sortie += arete(n, cible, "douce")

    y0 = 74 + len(lignes) * (BOITE_H + 24) + 16
    sortie.append(
        f'  <text x="16" y="{y0}" font-family="Verdana, DejaVu Sans, sans-serif" '
        f'font-size="10" font-weight="bold" fill="#1a1a1a">Légende</text>'
    )
    x = 16
    for prog, nom in (("A", "moteur"), ("B", "intelligence"), ("N", "natif"), ("R", "lecteur")):
        fill, trait = COULEURS[prog]
        sortie.append(
            f'  <rect x="{x}" y="{y0 + 10}" width="11" height="11" rx="2" fill="{fill}" '
            f'stroke="{trait}" stroke-width="1.1"/>'
        )
        sortie.append(
            f'  <text x="{x + 16}" y="{y0 + 19}" font-family="Verdana, DejaVu Sans, sans-serif" '
            f'font-size="8.5" fill="#333333">{prog} — {nom}</text>'
        )
        x += 148
    sortie.append(
        f'  <rect x="{x}" y="{y0 + 10}" width="11" height="11" rx="2" fill="#fdecea" '
        f'stroke="#b03a2e" stroke-width="1.1" stroke-dasharray="4 2"/>'
    )
    sortie.append(
        f'  <text x="{x + 16}" y="{y0 + 19}" font-family="Verdana, DejaVu Sans, sans-serif" '
        f'font-size="8.5" fill="#333333">sans fiche (trou nommé)</text>'
    )
    x += 178
    sortie.append(
        f'  <path d="M {x} {y0 + 16} H {x + 30}" stroke="#3a3a3a" stroke-width="1.3" '
        f'fill="none" marker-end="url(#fleche)"/>'
    )
    sortie.append(
        f'  <text x="{x + 38}" y="{y0 + 19}" font-family="Verdana, DejaVu Sans, sans-serif" '
        f'font-size="8.5" fill="#333333">dépendance dure</text>'
    )
    x += 152
    sortie.append(
        f'  <path d="M {x} {y0 + 16} H {x + 30}" stroke="#b26a00" stroke-width="1.1" '
        f'stroke-dasharray="4 3" fill="none" marker-end="url(#fleche-douce)"/>'
    )
    sortie.append(
        f'  <text x="{x + 38}" y="{y0 + 19}" font-family="Verdana, DejaVu Sans, sans-serif" '
        f'font-size="8.5" fill="#333333">plafond</text>'
    )
    sortie.append("</svg>")
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text("\n".join(sortie) + "\n", encoding="utf-8")


def tables(noeuds: dict) -> str:
    """Les quatre tables du graphe, dans l'ordre des chantiers. Générees, jamais recopiees :
    une table ecrite a la main diverge de la fiche au premier ajout."""
    sortie = []
    noms = {"A": "A — le moteur", "B": "B — l'intelligence", "N": "N — le natif",
            "R": "R — le lecteur"}
    for prog in "ABNR":
        sortie.append(f"### {noms[prog]}\n")
        sortie.append("| item | état | dépend de (dure) | plafond / contrainte | débloque | fiche |")
        sortie.append("|---|---|---|---|---|---|")
        for n in sorted(k for k, d in noeuds.items() if d["programme"] == prog):
            d = noeuds[n]
            dures = ", ".join(
                f"{c} ({'dure' if c in noeuds else 'acquis'})" for c, _ in d["dures"]
            ) or "—"
            autres = [
                f"{c} (plafond)" for c, _ in d["douces"]
            ] + list(d["faits"])
            if d["bloque"]:
                autres.append(f"bloqué : {d['bloque']}")
            aval = sorted(
                k for k, x in noeuds.items() if any(c == n for c, _ in x["dures"])
            )
            etat = "sans fiche" if d["sans_fiche"] else d["statut"]
            fiche = f"[{d['fiche']}]({d['fiche']})" if d["fiche"] else "—"
            sortie.append(
                f"| **{n}** | {etat} | {dures} | {' ; '.join(autres) or '—'} | "
                f"{', '.join(aval) or '—'} | {fiche} |"
            )
        sortie.append("")
    return "\n".join(sortie)


def main() -> int:
    ap = argparse.ArgumentParser(description="Vérifie le graphe des dépendances du backlog.")
    ap.add_argument("--svg", type=pathlib.Path, help="écrit aussi le graphe en SVG")
    ap.add_argument("--tables", action="store_true", help="imprime les tables du graphe")
    args = ap.parse_args()

    noeuds = construire()
    if args.tables:
        print(tables(noeuds))
        return 0
    erreurs, avert, niveau = controler(noeuds)
    libres = frontiere(noeuds)
    prof, chemin = chemin_le_plus_long(noeuds, niveau)
    dures = sum(1 for d in noeuds.values() for c, _ in d["dures"] if c in noeuds)
    douces = sum(1 for d in noeuds.values() for c, _ in d["douces"] if c in noeuds)
    fiches_n = sum(1 for d in noeuds.values() if not d["sans_fiche"])

    print("=== GRAPHE DU BACKLOG ===")
    print(
        f"  fiches {fiches_n} · lignes sans fiche {len(SANS_FICHE)} · "
        f"arêtes dures {dures} · plafonds {douces}"
    )
    print(f"  profondeur {prof} : {chemin}")
    print(f"  frontière ({len(libres)}) : {', '.join(libres) if libres else 'aucune'}")
    if args.svg:
        dessiner(noeuds, niveau, args.svg)
        print(f"  dessin : {args.svg.relative_to(RACINE) if args.svg.is_absolute() else args.svg}")

    for message in avert:
        print(f"  ⚠️  {message}")
    for message in erreurs:
        print(f"  ❌ {message}")
    if erreurs:
        print(f"\n❌ {len(erreurs)} erreur(s) — le graphe ment.")
        return 1
    if avert:
        print(f"\n✅ aucune erreur ; {len(avert)} avertissement(s) à arbitrer.")
        return 0
    print("\n✅ le graphe est cohérent : aucune arête morte, aucun cycle, aucune priorité inversée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
