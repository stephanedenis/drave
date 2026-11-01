#!/usr/bin/env python3
"""extraire_tableaux.py — un tableau scanné : les traits d'abord, les cellules ensuite.

POURQUOI CE FICHIER. Sur un scan, une cellule n'existe pas : il y a des mots et des **traits**.
Un OCR qui rend du texte à plat ne peut pas dire « 2,3 % est dans la colonne Taux, ligne Lille »
— et R4.1 a montré que le texte plat ne répond pas (0/3). Ici on lit la **grille** (les lignes
horizontales et verticales du tableau), puis on range chaque mot dans la cellule qui le contient.
C'est classique, c'est mesurable, et ça ne demande aucun modèle.

CE QUE L'OUTIL NE FAIT PAS : un tableau SANS traits (aligné par espaces). Il le dit : sans
grille, il n'invente pas de colonnes.

Usage :
  python3 tools/extraire_tableaux.py image.png --json
  python3 tools/extraire_tableaux.py image.png --mots mots.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import median_filter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import graphe_document_ocr  # noqa: E402
import nettoyer_scan  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent


def _plus_longue_serie(masque: np.ndarray) -> np.ndarray:
    """La plus longue suite de pixels allumés, par ligne. Un TRAIT est continu ; une ligne
    de texte ne l'est pas (les espaces entre les mots la coupent). C'est ce qui distingue
    les deux — un simple comptage de pixels sombres confondait le texte dense et la grille."""
    out = np.zeros(masque.shape[0], dtype=np.int32)
    for i in range(masque.shape[0]):
        idx = np.flatnonzero(masque[i])
        if len(idx) == 0:
            continue
        ruptures = np.flatnonzero(np.diff(idx) > 1)
        debuts = np.r_[0, ruptures + 1]
        fins = np.r_[ruptures, len(idx) - 1]
        out[i] = int((idx[fins] - idx[debuts]).max()) + 1
    return out


def _grille_reguliere(indices: list[int], tolerance: float = 0.2) -> list[int]:
    """Parmi des candidats (traits + lignes de texte), garde la suite ARITHMÉTIQUE dont
    TOUS les points sont présents : les traits d'un tableau sont également espacés, le texte
    ne l'est pas. Un point manquant disqualifie la suite — sinon deux lignes de texte
    suffisent à inventer une grille."""
    if len(indices) < 4:
        return indices
    meilleur = None  # (nombre de points, pas, bornes)
    for i in range(len(indices)):
        for j in range(i + 1, len(indices)):
            total = indices[j] - indices[i]
            for k in range(3, 21):
                pas = total / k
                if pas < 15:
                    break
                points = [indices[i] + m * pas for m in range(k + 1)]
                if all(any(abs(c - x) <= tolerance * pas for c in indices) for x in points):
                    if meilleur is None or (k + 1) > meilleur[0]:
                        meilleur = (k + 1, pas, points)
    return [int(round(x)) for x in meilleur[2]] if meilleur else indices


def _groupes(indices: np.ndarray, ecart: int = 3) -> list[int]:
    """Des indices consécutifs (à `ecart` près) → leur centre. Une ligne de 1-2 px d'épaisseur
    peut être détectée sur plusieurs colonnes voisines : c'est le MÊME trait."""
    if len(indices) == 0:
        return []
    centres, debut, precedent = [], int(indices[0]), int(indices[0])
    for i in indices[1:]:
        if int(i) - precedent > ecart:
            centres.append((debut + precedent) // 2)
            debut = int(i)
        precedent = int(i)
    centres.append((debut + precedent) // 2)
    return centres


def angle_tableau(im: Image.Image) -> float:
    """L'angle qui rend les traits du tableau horizontaux : on maximise la somme des carrés
    du profil de lignes d'un masque BINAIRE, pas la variance d'une image grise. Sur un trait
    de grille, c'est plus précis de 0,1° — et 0,1° sur 2 000 px, c'est deux pixels de dérive,
    assez pour couper un trait en morceaux."""
    from scipy.ndimage import rotate as nd_rotate
    g = np.asarray(im.convert("L"), dtype=np.uint8)
    facteur = 800 / max(g.shape[1], 1)
    petit = np.asarray(Image.fromarray(g).resize(
        (800, max(int(g.shape[0] * facteur), 1)), Image.BILINEAR))
    encre = (petit < 190).astype(np.float32)
    meilleur, score_max = 0.0, -1.0
    for angle in np.arange(-2.0, 2.001, 0.1):
        tourne = nd_rotate(encre, angle, reshape=False, order=0)
        score = float((tourne.sum(axis=1) ** 2).sum())
        if score > score_max:
            meilleur, score_max = float(angle), score
    return meilleur


def redresser_tableau(im: Image.Image) -> tuple[Image.Image, float]:
    """Un tableau supporte mal l'inclinaison : les traits verticaux se couchent sur plusieurs
    colonnes et la projection les perd. On redresse TOUJOURS (au-delà de 0,15°), même quand
    l'OCR s'en passe — c'est la grille qui l'exige, pas les mots."""
    angle = angle_tableau(im)
    if abs(angle) < 0.15:
        return im, 0.0
    return im.rotate(angle, resample=Image.BICUBIC, expand=True,
                     fillcolor=(255, 255, 255)), angle


def effacer_traits(im: Image.Image) -> Image.Image:
    """Enlève les TRAITS du tableau avant l'OCR. Sans cela, tesseract lit une ligne sur deux :
    les règles horizontales coupent la page en « cellules » et la segmentation saute des
    lignes (mesuré : 56 mots au lieu de 86, les lignes Lyon/Nice/Brest/Dijon absentes).
    Les traits sont les suites de pixels sombres plus longues que la moitié de la page."""
    gris = np.asarray(im.convert("L"), dtype=np.uint8)
    encre = gris < 128
    traits = np.zeros_like(encre)
    for i in range(encre.shape[0]):
        idx = np.flatnonzero(encre[i])
        if len(idx) == 0:
            continue
        ruptures = np.flatnonzero(np.diff(idx) > 1)
        debuts = np.r_[0, ruptures + 1]
        fins = np.r_[ruptures, len(idx) - 1]
        for d, f in zip(debuts, fins):
            if idx[f] - idx[d] > encre.shape[1] * 0.5:
                traits[i, idx[d]:idx[f] + 1] = True
    for j in range(encre.shape[1]):
        idx = np.flatnonzero(encre[:, j])
        if len(idx) == 0:
            continue
        ruptures = np.flatnonzero(np.diff(idx) > 1)
        debuts = np.r_[0, ruptures + 1]
        fins = np.r_[ruptures, len(idx) - 1]
        for d, f in zip(debuts, fins):
            if idx[f] - idx[d] > encre.shape[0] * 0.3:
                traits[idx[d]:idx[f] + 1, j] = True
    from scipy.ndimage import binary_dilation
    traits = binary_dilation(traits, iterations=2)
    return Image.fromarray(np.where(encre & ~traits, 0, 255).astype(np.uint8)).convert("RGB")


def grille(im: Image.Image) -> dict:
    """Les frontières du tableau : les traits horizontaux, puis les verticaux DANS la zone
    du tableau (un trait de page ou un titre ne doit pas devenir une frontière)."""
    gris = np.asarray(im.convert("L"), dtype=np.uint8)
    encre = gris < 128
    if encre.mean() < 0.0005:
        return {"xs": [], "ys": [], "raison": "aucune encre"}
    hauteur, largeur = encre.shape
    # seuil 190 : un trait de scan est noir mais le JPEG l'éclaircit ; à 128, il se coupe
    encre = gris < 190
    candidats = _groupes(np.where(_plus_longue_serie(encre) > largeur * 0.60)[0])
    ys = _grille_reguliere(candidats)
    if len(ys) < 3:
        return {"xs": [], "ys": [], "raison": f"trop peu de traits horizontaux ({len(ys)})"}
    haut, bas = ys[0], ys[-1]
    region = encre[haut:bas + 1, :]
    candidats_x = _groupes(np.where(_plus_longue_serie(region.T) > region.shape[0] * 0.55)[0])
    xs = _grille_reguliere(candidats_x)
    if len(xs) < 3:
        return {"xs": [], "ys": ys, "raison": f"trop peu de traits verticaux ({len(xs)})"}
    return {"xs": xs, "ys": ys, "raison": ""}


def cellules(im: Image.Image, les_mots: list[dict], gr: dict) -> list[list[str]]:
    """Range chaque mot dans la cellule qui contient son centre, puis recolle le texte."""
    xs, ys = gr["xs"], gr["ys"]
    if len(xs) < 2 or len(ys) < 2:
        return []
    lignes = len(ys) - 1
    colonnes = len(xs) - 1
    grille_vide = [[[] for _ in range(colonnes)] for _ in range(lignes)]
    import re
    artifacts = re.compile(r"^[|\-_—~^]+$")
    for mot in les_mots:
        if artifacts.match(mot["texte"].strip()):
            continue  # un trait de grille lu comme un mot : ce n'est pas une cellule
        cx = mot["left"] + mot["width"] / 2
        cy = mot["top"] + mot["height"] / 2
        # hors de la grille, il n'y a pas de cellule : le titre et le paragraphe ne doivent
        # pas tomber dans la première ligne (c'est l'erreur qu'a faite la première version)
        if not (ys[0] <= cy <= ys[-1] and xs[0] <= cx <= xs[-1]):
            continue
        i = sum(1 for y in ys[1:-1] if cy > y)
        j = sum(1 for x in xs[1:-1] if cx > x)
        if 0 <= i < lignes and 0 <= j < colonnes:
            grille_vide[i][j].append(mot)
    return [[" ".join(m["texte"] for m in sorted(cellule, key=lambda m: (m["top"], m["left"])))
             for cellule in ligne] for ligne in grille_vide]


def extraire(image: pathlib.Path, langue: str = "fra", redresser: bool = True) -> dict:
    """Redresse, OCRise l'image redressée, puis range les mots dans la grille. Les mots et
    les traits doivent être dans le MÊME repère : on n'essaie pas de transformer des boîtes,
    on refait l'OCR sur l'image redressée — c'est une seconde de plus, pas une erreur."""
    import tempfile
    im = Image.open(image).convert("RGB")
    angle = 0.0
    if redresser:
        im, angle = redresser_tableau(im)
    gr = grille(im)
    if gr["raison"]:
        return {"xs": gr["xs"], "ys": gr["ys"], "raison": gr["raison"],
                "angle": round(angle, 2), "grille": []}
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        chemin = pathlib.Path(tmp.name)
    try:
        # les traits effacés, l'OCR lit TOUTES les lignes ; psm 6 = un seul bloc, ordre ligne
        effacer_traits(im).save(chemin)
        mots = graphe_document_ocr.mots(chemin, langue, psm=6)
    finally:
        chemin.unlink(missing_ok=True)
    return {"xs": gr["xs"], "ys": gr["ys"], "raison": "",
            "angle": round(angle, 2), "grille": cellules(im, mots, gr)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("image", type=pathlib.Path)
    ap.add_argument("--langue", default="fra")
    ap.add_argument("--sans-redresser", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    resultat = extraire(args.image, args.langue, redresser=not args.sans_redresser)
    if args.json:
        print(json.dumps(resultat, ensure_ascii=False, indent=1))
    else:
        print(f"  angle {resultat['angle']:+.2f}° · {len(resultat['grille'])} lignes × "
              f"{len(resultat['grille'][0]) if resultat['grille'] else 0} colonnes"
              f"{' · ' + resultat['raison'] if resultat['raison'] else ''}")
        for ligne in resultat["grille"][:4]:
            print("   ", " | ".join(c[:18] for c in ligne))
    return 0 if resultat["grille"] else 1


if __name__ == "__main__":
    sys.exit(main())
