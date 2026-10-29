#!/usr/bin/env python3
"""graphe_document_pdf.py — les blocs d'un PDF, dans l'ordre de LECTURE.

POURQUOI CE FICHIER. Un PDF n'a pas de paragraphes : il a des mots placés à des
coordonnées. `pdftotext` reconstruit des lignes, mais l'ordre du fichier n'est pas l'ordre de
lecture : sur une page à deux colonnes, une lecture naïve entrelace la gauche et la droite.
C'est le contrôle négatif du chantier R0.1, et c'est la seule raison d'être de ce module.

Ce qu'il fait, dans cet ordre :
  1. `pdftotext -bbox-layout` donne les lignes et leurs boîtes (on ne réécrit pas un
     extracteur de PDF) ;
  2. une **bande verticale vide** est cherchée dans la page : si elle existe et qu'il y a des
     lignes des deux côtés, la page a deux colonnes — et on lit toute la gauche, puis toute
     la droite ;
  3. les lignes sont groupées en paragraphes par l'écart vertical et le retrait ;
  4. les lignes de corps plus petit que la médiane sont des **notes** (en-têtes, pieds de page,
     notes de bas de page) : elles sortent du corps, elles n'y sont pas recopiées ;
  5. les tableaux ne sont **pas** revendiqués : un tableau PDF non balisé est du texte. Mieux
     vaut ne rien dire que l'inventer (le bloc R4.1 le traitera).

Usage :
  python3 tools/graphe_document_pdf.py --json data/onu/pdf/A_RES_80_10-fr.pdf
  python3 tools/graphe_document_pdf.py --fabrique tools/tests/documents/pdf/deux-colonnes.pdf
  python3 tools/graphe_document_pdf.py --autotest
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import statistics
import subprocess
import sys
import xml.etree.ElementTree as ET

TYPES_LIGNES = re.compile(
    r"^(article\s+\d+|chapitre\s+[ivx\d]+|section\s+[ivx\d]+|[ivx]+\.|\d+\.(?!\d))\s", re.I)


def _etiquette(element) -> str:
    return element.tag.split("}")[-1]


def lignes_du_pdf(chemin: pathlib.Path) -> list[dict]:
    """Les pages, et pour chacune ses lignes avec leur boîte. C'est poppler qui lit, pas nous."""
    sortie = subprocess.run(
        ["pdftotext", "-bbox-layout", str(chemin), "-"],
        capture_output=True, text=True, check=True).stdout
    racine = ET.fromstring(sortie)
    pages = []
    for page in racine.iter():
        if _etiquette(page) != "page":
            continue
        lignes = []
        for ligne in page.iter():
            if _etiquette(ligne) != "line":
                continue
            mots = [mot.text or "" for mot in ligne if _etiquette(mot) == "word"]
            texte = " ".join(mots).strip()
            if not texte:
                continue
            y0, y1 = float(ligne.get("yMin")), float(ligne.get("yMax"))
            lignes.append({
                "x0": float(ligne.get("xMin")), "x1": float(ligne.get("xMax")),
                "y0": y0, "y1": y1, "hauteur": y1 - y0, "texte": texte,
            })
        pages.append({"largeur": float(page.get("width")),
                      "hauteur": float(page.get("height")), "lignes": lignes})
    return pages


def bande_vide(lignes: list[dict], largeur: float) -> tuple[float, float] | None:
    """La plus large bande verticale qu'AUCUNE ligne ne traverse. Si elle est assez large et
    qu'il y a des lignes des deux côtés, c'est la gouttière entre deux colonnes."""
    if len(lignes) < 6:
        return None
    bornes = sorted({l["x0"] for l in lignes} | {l["x1"] for l in lignes})
    meilleure: tuple[float, float, float] | None = None
    for debut, fin in zip(bornes, bornes[1:]):
        if fin - debut < max(20.0, largeur * 0.04):
            continue
        if debut < largeur * 0.15 or fin > largeur * 0.95:
            continue
        if any(l["x0"] < fin and l["x1"] > debut for l in lignes):
            continue  # une ligne traverse la bande : ce n'est pas une gouttière
        if meilleure is None or fin - debut > meilleure[0]:
            meilleure = (fin - debut, debut, fin)
    return (meilleure[1], meilleure[2]) if meilleure else None


def ordre_de_lecture(page: dict) -> list[dict]:
    """Les lignes de la page, dans l'ordre de lecture : colonne par colonne s'il y en a deux."""
    lignes = page["lignes"]
    gouttiere = bande_vide(lignes, page["largeur"])
    if gouttiere:
        gauche, droite = gouttiere
        colonne_gauche = sorted([l for l in lignes if l["x1"] <= gauche], key=lambda l: l["y0"])
        colonne_droite = sorted([l for l in lignes if l["x0"] >= droite], key=lambda l: l["y0"])
        return colonne_gauche + colonne_droite
    return sorted(lignes, key=lambda l: l["y0"])


def _recoller(texte: str, suivant: str) -> str:
    """Une césure de fin de ligne se recolle : `inter-` + `national` = `international`.
    Une espace avant le tiret (`decision -making`) est un artefact de PDF, on la garde telle
    quelle : le mot reste lisible et la fidélité le retrouve."""
    if texte.endswith("-") and suivant[:1].islower():
        return texte[:-1] + suivant
    return texte + " " + suivant


def blocs_de_page(page: dict, numero: int) -> list[dict]:
    """Les blocs d'une page : notes à part, titres par la hauteur, le reste en paragraphes."""
    lignes = ordre_de_lecture(page)
    if not lignes:
        return []
    hauteur_corps = statistics.median(l["hauteur"] for l in lignes)
    blocs: list[dict] = []
    paragraphe: list[dict] = []

    def vide_paragraphe() -> None:
        if not paragraphe:
            return
        texte = paragraphe[0]["texte"]
        for ligne in paragraphe[1:]:
            texte = _recoller(texte, ligne["texte"])
        blocs.append({"type": "paragraphe", "texte": re.sub(r"\s+", " ", texte).strip(),
                      "prov": {"page": numero, "y": round(paragraphe[0]["y0"], 1)}})
        paragraphe.clear()

    for ligne in lignes:
        petit = ligne["hauteur"] < hauteur_corps * 0.85
        grand = ligne["hauteur"] > hauteur_corps * 1.12
        court = len(ligne["texte"]) < 90
        if petit:
            vide_paragraphe()
            blocs.append({"type": "note", "texte": ligne["texte"],
                          "prov": {"page": numero, "y": round(ligne["y0"], 1)}})
            continue
        if grand or (court and TYPES_LIGNES.match(ligne["texte"])):
            vide_paragraphe()
            premier = not any(b["type"] in ("titre", "section") for b in blocs)
            blocs.append({"type": "titre" if premier and grand else "section",
                          "texte": ligne["texte"],
                          "prov": {"page": numero, "y": round(ligne["y0"], 1)}})
            continue
        if paragraphe:
            ecart = ligne["y0"] - paragraphe[-1]["y1"]
            retrait = abs(ligne["x0"] - paragraphe[-1]["x0"])
            if ecart > hauteur_corps * 1.2 or retrait > hauteur_corps * 1.5:
                vide_paragraphe()
        paragraphe.append(ligne)
    vide_paragraphe()
    return blocs


def analyse(chemin: pathlib.Path) -> list[dict]:
    blocs: list[dict] = []
    for indice, page in enumerate(lignes_du_pdf(chemin), start=1):
        blocs += blocs_de_page(page, indice)
    return blocs


# --------------------------------------------------------------------- les fixtures

def fabrique(destination: pathlib.Path) -> None:
    """Une page à deux colonnes dont on CONNAÎT l'ordre : 1–6 à gauche, 1–6 à droite. Un
    lecteur naïf les entrelace ; c'est exactement ce que la porte doit voir échouer."""
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    destination.parent.mkdir(parents=True, exist_ok=True)
    largeur, hauteur = letter
    toile = canvas.Canvas(str(destination), pagesize=letter)
    toile.setFont("Helvetica", 11)
    for indice in range(1, 7):
        toile.drawString(72, hauteur - 72 - (indice - 1) * 40,
                         f"GAUCHE-{indice} : la colonne gauche, ligne {indice}.")
        toile.drawString(largeur / 2 + 20, hauteur - 72 - (indice - 1) * 40,
                         f"DROITE-{indice} : la colonne droite, ligne {indice}.")
    # une note de bas de page, plus petite, pour vérifier qu'elle sort du corps
    toile.setFont("Helvetica", 7)
    toile.drawString(72, 60, "NOTE-1 : le petit corps est une note, pas du corps.")
    toile.save()


def verifie(chemin: pathlib.Path) -> tuple[float, list[str]]:
    """Le contrôle de fidélité contre `pypdf` : le contenu du flux doit se retrouver dans
    l'extraction indépendante, et réciproquement. On compare des CARACTÈRES, pas des mots :
    deux extracteurs ne placent ni les césures ni les espaces au même endroit, et le CJK n'a
    pas de mots séparés. L'ordre de lecture, lui, est testé par la fixture deux-colonnes."""
    import pypdf
    from collections import Counter

    flux = " ".join(b["texte"] for b in analyse(chemin))
    reference = "\n".join((p.extract_text() or "") for p in pypdf.PdfReader(str(chemin)).pages)

    def propre(texte: str) -> str:
        return re.sub(r"[\W_]+", "", texte.lower())

    a, b = Counter(propre(reference)), Counter(propre(flux))
    communs = sum((a & b).values())
    perte = communs / max(sum(a.values()), 1)
    invention = communs / max(sum(b.values()), 1)
    ecarts = []
    if perte < 1.0:
        ecarts.append("absents : " + " ".join(sorted((a - b).elements())[:8]))
    if invention < 1.0:
        ecarts.append("ajoutés : " + " ".join(sorted((b - a).elements())[:8]))
    return min(perte, invention), ecarts


def autotest() -> int:
    racine = pathlib.Path(__file__).resolve().parent.parent
    deux = racine / "tools/tests/documents/pdf/deux-colonnes.pdf"
    fabrique(deux)
    m = analyse(deux)
    corps = [b["texte"] for b in m if b["type"] != "note"]
    motif = [("G" if "GAUCHE" in t else "D") for t in corps if "GAUCHE" in t or "DROITE" in t]
    attendu = ["G"] * 6 + ["D"] * 6
    notes = [b for b in m if b["type"] == "note"]
    print(f"deux-colonnes.pdf : {len(corps)} blocs de corps, ordre {''.join(motif)}")
    print(f"  attendu {''.join(attendu)} · notes {len(notes)}")
    ok = motif == attendu and len(notes) >= 1
    temoins = sorted((racine / "data/onu/pdf").glob("*.pdf"))[:3]
    for temoin in temoins:
        ratio, ecarts = verifie(temoin)
        print(f"  {temoin.name:32s} fidélité {ratio:.4f} {ecarts[0] if ecarts else ''}")
        ok = ok and ratio >= 0.99
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Les blocs d'un PDF, en ordre de lecture.")
    ap.add_argument("chemin", nargs="?", type=pathlib.Path)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--fabrique", type=pathlib.Path, help="fabrique la fixture deux-colonnes")
    ap.add_argument("--autotest", action="store_true")
    args = ap.parse_args()
    if args.fabrique:
        fabrique(args.fabrique)
        print(f"fixture écrite : {args.fabrique}")
        return 0
    if args.autotest:
        return autotest()
    if not args.chemin:
        ap.error("un chemin est requis")
    blocs = analyse(args.chemin)
    if args.json:
        print(json.dumps(blocs, ensure_ascii=False, indent=1))
    else:
        for bloc in blocs:
            print(f"{bloc['type']:10s} p{bloc['prov']['page']:2d} :: {bloc['texte'][:80]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
