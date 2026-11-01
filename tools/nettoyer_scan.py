#!/usr/bin/env python3
"""nettoyer_scan.py — le prétraitement d'un scan, par étapes NOMMÉES et mesurables.

POURQUOI CE FICHIER. Un OCR ne voit pas un document, il voit des pixels. Le pilote R4.4 l'a
montré sur une photo simulée : **51,8 %** de WER sur l'image brute, **3,8 %** après correction
de l'éclairage — le même OCR, la même page. Le prétraitement n'est donc pas un confort : c'est
la moitié de la lecture. Chaque étape est **nommée** pour que la mesure dise laquelle paie, et
aucune n'est appliquée « au cas où » : une étape qui ne paie pas est une étape qui coûte.

LES ÉTAPES :
  - `recadrage`    : enlève les bords sombres (fond de photo), garde la page ;
  - `eclairage`    : estime le fond par un flou large et divise — l'éclairage inégal tue l'OCR ;
  - `redressement` : estime l'angle par la variance du profil horizontal des lignes, redresse ;
  - `echelle`      : remonte à ~2 500 px de large (tesseract aime ~300 dpi) ;
  - `lissage`      : pour une image déjà binaire (fax), adoucit puis re-seuille — sinon
                     l'upscaling fabrique des marches d'escalier que tesseract lit mal ;
  - `median`       : filtre médian 3×3 (sel-et-poivre) ;
  - `sauvola`      : binarisation locale (fond non uniforme).

`auto` choisit d'après un **diagnostic** mesuré de l'image (binaire ? éclairage inégal ? petit ?
incliné ?) et rend la trace des étapes appliquées : un prétraitement qui ne dit pas ce qu'il a
fait n'est pas reproductible.

Usage :
  python3 tools/nettoyer_scan.py scan.png --sortie scan-nettoye.png --etapes auto
  python3 tools/nettoyer_scan.py scan.png --etapes eclairage,echelle --json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter, median_filter, rotate, uniform_filter

RACINE = pathlib.Path(__file__).resolve().parent.parent
ETAPES = ("recadrage", "eclairage", "redressement", "echelle", "lissage", "median", "sauvola")


def _gris(im: Image.Image) -> np.ndarray:
    return np.asarray(im.convert("L"), dtype=np.float64)


def _image(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGB")


def diagnostic(im: Image.Image) -> dict:
    """Ce que l'image est, avant de décider ce qu'on lui fait.

    `binaire` n'est PAS « la page est blanche » (une page de texte est blanche à 97 %) : c'est
    la part des pixels d'ENCRE qui n'ont pas de niveau intermédiaire. Un rendu propre a des
    bords anti-aliasés (donc des gris) ; un fax 1 bit n'en a aucun. Sans cette distinction,
    une page propre était prise pour un fax et lissée — et le lissage abîme un rendu propre."""
    g = _gris(im)
    h, w = g.shape
    encre = g < 245
    intermediaires = int(((g > 10) & (g < 245)).sum())
    binaire = 1.0 - intermediaires / max(int(encre.sum()), 1)
    fond = gaussian_filter(g, sigma=max(min(h, w) / 20, 8))
    bas, haut = np.percentile(fond, 5), np.percentile(fond, 95)
    ratio = float(haut / max(bas, 1))
    return {
        "largeur": w, "hauteur": h,
        "binaire": round(binaire, 3),
        "fond_ratio": round(ratio, 2),
        "petit": w < 1800,
        "inclinaison": round(angle_de_redressement(im), 2),
    }


def angle_de_redressement(im: Image.Image) -> float:
    """L'angle qui rend les lignes les plus horizontales : on maximise la variance du profil
    horizontal (des lignes de texte alignées font des pics). Sur une vignette, c'est rapide."""
    g = _gris(im)
    petit = Image.fromarray(g.astype(np.uint8)).resize(
        (max(int(im.width * 0.2), 60), max(int(im.height * 0.2), 60)), Image.BILINEAR)
    a = np.asarray(petit, dtype=np.float64)
    encre = (a < np.percentile(a, 25)).astype(np.float64)
    meilleur, score_max = 0.0, -1.0
    for angle in np.arange(-3.0, 3.001, 0.25):
        tourne = rotate(encre, angle, reshape=False, order=1, mode="nearest")
        score = float(np.var(tourne.sum(axis=1)))
        if score > score_max:
            meilleur, score_max = float(angle), score
    return meilleur


def recadrage(im: Image.Image) -> Image.Image:
    g = _gris(im)
    seuil = max(np.percentile(g, 2) + 20, 40)
    encre = g < seuil
    if encre.mean() < 0.002:  # page blanche ou uniforme : on ne recadre pas au hasard
        return im
    lignes = np.where(encre.any(axis=1))[0]
    colonnes = np.where(encre.any(axis=0))[0]
    if not len(lignes) or not len(colonnes):
        return im
    marge = max(int(min(g.shape) * 0.01), 4)
    haut, bas = max(int(lignes[0]) - marge, 0), min(int(lignes[-1]) + marge, g.shape[0])
    gauche, droite = max(int(colonnes[0]) - marge, 0), min(int(colonnes[-1]) + marge, g.shape[1])
    return im.crop((gauche, haut, droite, bas))


def eclairage(im: Image.Image) -> Image.Image:
    """Divise par le fond estimé : c'est ce qui a fait passer la photo de 51,8 % à 3,8 %."""
    g = _gris(im)
    fond = gaussian_filter(g, sigma=max(min(g.shape) / 20, 8))
    return _image(np.clip(g / np.maximum(fond, 1) * 240, 0, 255))


def redressement(im: Image.Image, angle: float | None = None) -> Image.Image:
    if angle is None:
        angle = angle_de_redressement(im)
    if abs(angle) < 0.25:
        return im
    return im.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=(255, 255, 255))


def echelle(im: Image.Image, largeur: int = 2500) -> Image.Image:
    if im.width >= largeur:
        return im
    facteur = largeur / im.width
    return im.resize((largeur, max(int(im.height * facteur), 1)), Image.LANCZOS)


def lissage(im: Image.Image, seuil: int = 160, flou: float = 1.2) -> Image.Image:
    """Pour une image binaire : adoucir AVANT de re-seuiller. L'upscaling d'un fax 1 bit
    fabrique des marches ; sans ce lissage, l'agrandir fait EMPIRER le WER (97 %)."""
    gris = im.convert("L").filter(ImageFilter.GaussianBlur(flou))
    return _image(np.where(np.asarray(gris) < seuil, 0, 255))


def median(im: Image.Image, taille: int = 3) -> Image.Image:
    return _image(median_filter(_gris(im), size=taille))


def sauvola(im: Image.Image, k: float = 0.2, fraction: float = 0.02) -> Image.Image:
    g = _gris(im)
    fenetre = max(int(min(g.shape) * fraction) | 1, 15)
    moyenne = uniform_filter(g, size=fenetre)
    carre = uniform_filter(g * g, size=fenetre)
    ecart = np.sqrt(np.maximum(carre - moyenne * moyenne, 0))
    seuil = moyenne * (1 + k * (ecart / 128 - 1))
    return _image(np.where(g > seuil, 255, 0))


def auto(im: Image.Image) -> tuple[Image.Image, list[str]]:
    """Le diagnostic décide ; la trace dit ce qui a été appliqué.

    DEUX LEÇONS DE LA MESURE, écrites ici parce qu'elles sont contre-intuitives :
    1. **ne pas agrandir une image déjà propre** : passer une photocopie de 200 dpi à 2 500 px
       a DOUBLÉ son WER (6,6 % → 12,9 %) — tesseract lit mieux 200 dpi qu'un upscaling ;
    2. **l'angle se mesure APRÈS le recadrage** : sur la page entière, le bord et le
       vignettage biaisent le profil, et un redressement estimé là a coûté 29 points de WER
       (13 % → 42 %) ; recadrée puis redressée, la même page reste à 13 %."""
    trace: list[str] = []
    d = diagnostic(im)
    binaire = d["binaire"] > 0.85
    if not binaire:
        im = recadrage(im)
        trace.append("recadrage")
    # Le papier japonais du simulateur a un fond à 1,33 : sous l'ancien seuil (1,5) il
    # n'était pas corrigé, et la page tombait à 62,8 % de WER ; corrigée, elle est à 5,7 %.
    if d["fond_ratio"] > 1.25:
        im = eclairage(im)
        trace.append("eclairage")
    # Le redressement n'est appliqué que si l'inclinaison est FRANCHE et l'image assez
    # définie : tourner une page de 170 dpi de 0,75° la détruit (62,8 → 84,8 % de WER).
    angle = angle_de_redressement(im) if im.width >= 2000 else 0.0
    if abs(angle) >= 1.5:
        im = redressement(im, angle)
        trace.append(f"redressement({angle:+.2f})")
    if binaire:
        if im.width < 2100:
            im = echelle(im, 2100)
            trace.append("echelle(2100)")
        im = lissage(im)
        trace.append("lissage")
    elif im.width < 1200:
        im = echelle(im, 1800)
        trace.append("echelle(1800)")
    return im, trace


def appliquer(im: Image.Image, etapes: list[str]) -> tuple[Image.Image, list[str]]:
    if etapes == ["auto"]:
        return auto(im)
    trace: list[str] = []
    for etape in etapes:
        if etape not in ETAPES:
            raise SystemExit(f"étape inconnue : {etape} (connues : {', '.join(ETAPES)})")
        im = globals()[etape](im)
        trace.append(etape)
    return im, trace


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("image", type=pathlib.Path)
    ap.add_argument("--sortie", type=pathlib.Path)
    ap.add_argument("--etapes", default="auto",
                    help="auto, ou une liste : recadrage,eclairage,redressement,echelle,lissage,median,sauvola")
    ap.add_argument("--json", action="store_true", help="le diagnostic et la trace")
    args = ap.parse_args()
    im = Image.open(args.image).convert("RGB")
    d = diagnostic(im)
    etapes = [e.strip() for e in args.etapes.split(",") if e.strip()]
    sortie, trace = appliquer(im, etapes)
    if args.json:
        print(json.dumps({"diagnostic": d, "trace": trace,
                          "sortie": [sortie.width, sortie.height]},
                         ensure_ascii=False, indent=1))
        return 0
    sortie_path = args.sortie or args.image.with_name(args.image.stem + "-nettoye.png")
    sortie.save(sortie_path)
    print(f"  {args.image.name} · {im.width}×{im.height} → {sortie.width}×{sortie.height} · "
          f"{' → '.join(trace) or 'rien'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
