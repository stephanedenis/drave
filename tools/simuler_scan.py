#!/usr/bin/env python3
"""simuler_scan.py — le corpus de scans SIMULÉS de R4.4, avec sa vérité terrain.

POURQUOI CE FICHIER. Le pilote R4.4 a mesuré des pages **rendues** (vectorielles) : propre,
mais ce n'est pas un scan. Il n'y a pas de scanner sur la machine, et un corpus de photocopies
réelles ne se fabrique pas. On simule donc les **dégradations** qui font échouer un OCR, une
famille par cause — et on le dit : ce sont des scans **simulés**, pas des scans réels.

CINQ FAMILLES, CINQ CAUSES (et un contrôle) :
  - `propre`      : le rendu 300 dpi, sans dégradation — le contrôle de la chaîne ;
  - `photocopie`  : niveaux de gris, 200 dpi, flou léger, 1,2° de travers, mouchetures, JPEG q45 ;
  - `photo`       : perspective (coins décalés), éclairage inégal + ombre, flou de mouvement,
                    180 dpi, bruit, JPEG q25 — une photo de téléphone ;
  - `fax`         : 120 dpi, binarisation dure, sel-et-poivre, gigue horizontale par ligne ;
  - `papier`      : texture de papier, jaunissement, vignettage, taches, flou, JPEG q35.

La **graine** est explicite : deux graines donnent deux scans différents de la même page. Les
paramètres de chaque image sont écrits dans `manifeste.json` — un scan qui ne dit pas comment il
a été fabriqué n'est pas une mesure, c'est une image.

Usage :
  python3 tools/simuler_scan.py --sortie work/r44/scans --pages 10 --graines 1
  python3 tools/simuler_scan.py --liste          # les familles et leurs paramètres
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

import numpy as np
from PIL import Image, ImageFilter, ImageOps
from scipy.ndimage import gaussian_filter, map_coordinates

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import graphe_document_pdf  # noqa: E402
import mesurer_ocr  # noqa: E402  (les pages du banc et le cache de rendu)

RACINE = pathlib.Path(__file__).resolve().parent.parent
FAMILLES = ("propre", "photocopie", "photo", "fax", "papier", "petit")


def _rng(graine: int, page: int, famille: str) -> np.random.Generator:
    """La graine dépend de (graine, page, famille) : rejouable, et indépendante entre pages.
    `hash()` de Python est randomisé par processus (PYTHONHASHSEED) — sha256, pas hash()."""
    empreinte = hashlib.sha256(f"{graine}-{page}-{famille}".encode()).hexdigest()
    return np.random.default_rng(int(empreinte[:8], 16))


def rendre_300(pdf: pathlib.Path, page: int) -> Image.Image:
    """Le rendu de référence : 300 dpi, depuis le PDF vectoriel. C'est le cache du pilote."""
    png = mesurer_ocr.rendu(pdf, page, 300)
    return Image.open(png).convert("RGB")


def _jpeg(im: Image.Image, qualite: int, tmp: pathlib.Path) -> Image.Image:
    im.save(tmp, "JPEG", quality=qualite)
    with Image.open(tmp) as out:
        return out.convert("RGB")


def _perspective(im: Image.Image, rng: np.random.Generator, force: float) -> Image.Image:
    """Les quatre coins de la page sont décalés ; l'homographie est calculée puis INVERSÉE
    (PIL échantillonne la sortie dans l'entrée)."""
    w, h = im.size
    src = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=np.float64)
    dst = src + rng.uniform(-force, force, size=(4, 2)) * np.array([w, h])
    # H : src -> dst (8 inconnues, h33 = 1)
    a = []
    for (x, y), (u, v) in zip(src, dst):
        a.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        a.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    b = dst.reshape(-1)
    homographie = np.append(np.linalg.solve(np.array(a), b), 1.0).reshape(3, 3)
    h_inv = np.linalg.inv(homographie)
    coeffs = (h_inv / h_inv[2, 2]).flatten()[:8]
    return im.transform((w, h), Image.PERSPECTIVE, tuple(coeffs),
                        resample=Image.BICUBIC, fillcolor=(255, 255, 255))


def _flou_mouvement(im: Image.Image, longueur: int, angle: float) -> Image.Image:
    """Un noyau en ligne, tourné : la traînée d'un téléphone qui bouge pendant la pose."""
    noyau = np.zeros((longueur, longueur), dtype=np.float64)
    noyau[longueur // 2, :] = 1.0 / longueur
    from scipy.ndimage import rotate as nd_rotate, convolve
    noyau = nd_rotate(noyau, angle, reshape=False, order=1)
    noyau = np.clip(noyau, 0, None)
    noyau /= noyau.sum() or 1
    arr = np.asarray(im, dtype=np.float64)
    for c in range(arr.shape[2]):
        arr[..., c] = convolve(arr[..., c], noyau, mode="nearest")
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def _bruit(im: Image.Image, sigma: float, rng: np.random.Generator) -> Image.Image:
    arr = np.asarray(im, dtype=np.float64)
    arr += rng.normal(0, sigma, arr.shape)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def _ombre(im: Image.Image, rng: np.random.Generator, force: float = 0.35) -> Image.Image:
    w, h = im.size
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = rng.uniform(0.2, 0.8) * w, rng.uniform(0.2, 0.8) * h
    sx, sy = rng.uniform(0.3, 0.6) * w, rng.uniform(0.3, 0.6) * h
    champ = 1.0 - force * np.exp(-(((xx - cx) ** 2) / (2 * sx ** 2) +
                                   ((yy - cy) ** 2) / (2 * sy ** 2)))
    arr = np.asarray(im, dtype=np.float64) * champ[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def _eclairage(im: Image.Image, rng: np.random.Generator) -> Image.Image:
    w, h = im.size
    champ = gaussian_filter(rng.normal(0, 1, (h, w)), sigma=max(min(h, w) / 6, 2))
    champ = (champ - champ.min()) / (float(np.ptp(champ)) or 1)
    champ = 0.72 + 0.45 * champ
    arr = np.asarray(im, dtype=np.float64) * champ[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def _reduire(im: Image.Image, dpi: int) -> Image.Image:
    if dpi >= 300:
        return im
    f = dpi / 300.0
    return im.resize((max(int(im.width * f), 1), max(int(im.height * f), 1)), Image.LANCZOS)


def _texture_papier(im: Image.Image, rng: np.random.Generator) -> Image.Image:
    w, h = im.size
    basse = gaussian_filter(rng.normal(0, 1, (h, w)), sigma=max(min(h, w) / 40, 3))
    haute = gaussian_filter(rng.normal(0, 1, (h, w)), sigma=0.7)
    champ = 0.90 + 0.05 * basse / (basse.std() or 1) + 0.03 * haute
    arr = np.asarray(im, dtype=np.float64) * champ[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def fabriquer(im: Image.Image, famille: str, graine: int, page: int,
              tmp: pathlib.Path) -> tuple[Image.Image, dict]:
    """Une page propre -> un scan, avec les paramètres qui l'ont fabriqué."""
    rng = _rng(graine, page, famille)
    p: dict = {"famille": famille, "graine": graine}
    if famille == "propre":
        return im, p
    if famille == "photocopie":
        angle = float(rng.uniform(-1.2, 1.2))
        gris = ImageOps.autocontrast(_reduire(im.convert("L"), 200), cutoff=1)
        gris = gris.filter(ImageFilter.GaussianBlur(0.6)).rotate(
            angle, resample=Image.BICUBIC, expand=False, fillcolor=255)
        arr = np.asarray(gris, dtype=np.float64)
        mouchetures = rng.random(arr.shape) < 0.0008
        arr[mouchetures] = 0
        arr += rng.normal(0, 5, arr.shape)
        out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGB")
        p.update({"dpi": 200, "angle": round(angle, 2), "flou": 0.6, "jpeg": 45})
        return _jpeg(out, 45, tmp), p
    if famille == "photo":
        base = _reduire(im, 180)
        base = _perspective(base, rng, force=0.012)
        base = _eclairage(base, rng)
        base = _ombre(base, rng)
        base = _flou_mouvement(base, longueur=int(rng.integers(3, 6)),
                               angle=float(rng.uniform(0, 180)))
        base = _bruit(base, 6.0, rng)
        p.update({"dpi": 180, "perspective": 0.012, "flou_mouvement": True,
                  "bruit": 6.0, "jpeg": 25})
        return _jpeg(base, 25, tmp), p
    if famille == "fax":
        # Un fax : 120 dpi, binarisation dure, sel-et-poivre. La gigue par ligne a été
        # essayée puis RETIRÉE : elle rendait le texte irrécupérable (WER ~95 % après
        # upscaling), et une famille qu'aucun prétraitement ne relève ne mesure rien.
        gris = _reduire(im.convert("L"), 120)
        arr = np.asarray(gris, dtype=np.float64)
        arr = np.where(arr < 128, 0.0, 255.0)
        sel = rng.random(arr.shape)
        arr[sel < 0.004] = 0
        arr[sel > 0.996] = 255
        h, w = arr.shape
        bord = np.full((h + 40, w + 40), 255.0)
        bord[20:20 + h, 20:20 + w] = arr
        out = Image.fromarray(bord.astype(np.uint8)).convert("RGB")
        p.update({"dpi": 120, "binarisation": 128, "sel_poivre": 0.004, "gigue": 0.0})
        return out, p
    if famille == "petit":
        # un PETIT TEXTE : la même page rendue à 120 dpi, sans autre dégradation. C'est le
        # test de la politique d'échelle : l'image fait ~1 060 px de large, le prétraitement
        # doit décider de l'agrandir (ou pas) — et la mesure dit si c'était le bon choix.
        petite = _reduire(im, 120)
        p.update({"dpi": 120})
        return petite, p
    if famille == "papier":
        base = _reduire(im, 170)
        base = _texture_papier(base, rng)
        # jaunissement : le bleu baisse plus que le rouge
        arr = np.asarray(base, dtype=np.float64)
        arr[..., 0] *= 1.0
        arr[..., 2] *= 0.80
        base = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        # vignettage
        w, h = base.size
        yy, xx = np.mgrid[0:h, 0:w]
        r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
        base = Image.fromarray(np.clip(
            np.asarray(base, dtype=np.float64) * (1 - 0.30 * np.clip(r, 0, 1))[..., None],
            0, 255).astype(np.uint8))
        # deux taches
        for _ in range(2):
            cx, cy = rng.uniform(0.15, 0.85) * w, rng.uniform(0.15, 0.85) * h
            rayon = rng.uniform(0.03, 0.08) * w
            tache = ((xx - cx) ** 2 + (yy - cy) ** 2) < rayon ** 2
            arr = np.asarray(base, dtype=np.float64)
            arr[tache] *= 0.82
            base = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        base = base.rotate(0.6, resample=Image.BICUBIC, expand=False, fillcolor=(255, 255, 255))
        base = base.filter(ImageFilter.GaussianBlur(0.8))
        p.update({"dpi": 170, "texture": True, "jaunissement": 0.80, "vignettage": 0.30,
                  "taches": 2, "rotation": 0.6, "flou": 0.8, "jpeg": 28})
        return _jpeg(base, 28, tmp), p
    raise SystemExit(f"famille inconnue : {famille}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sortie", type=pathlib.Path, default=RACINE / "work/r44/scans")
    ap.add_argument("--pages", type=int, default=10)
    ap.add_argument("--test", type=int, default=0,
                    help="pages de test supplémentaires, SANS questions (WER seul)")
    ap.add_argument("--graines", type=int, default=1)
    ap.add_argument("--graine", type=int, default=0,
                    help="une seule graine (pour la variance) ; 0 = 1..--graines")
    ap.add_argument("--splits", default="dev,test")
    ap.add_argument("--familles", default=",".join(FAMILLES))
    ap.add_argument("--liste", action="store_true")
    args = ap.parse_args()
    if args.liste:
        for f in FAMILLES:
            print(f"  {f}")
        return 0
    familles = [f for f in args.familles.split(",") if f]
    graines = [args.graine] if args.graine else list(range(1, args.graines + 1))
    splits = {x for x in args.splits.split(",") if x}
    inconnues = sorted(set(familles) - set(FAMILLES))
    if inconnues:
        raise SystemExit(f"familles inconnues : {inconnues}")
    dev = mesurer_ocr.pages_du_banc(args.pages)
    for p in dev:
        p["split"] = "dev"
    dev = [p for p in dev if "dev" in splits]
    pages = list(dev)
    if args.test:
        deja = {(p["pdf"].name, p["page"]) for p in dev}
        # 1) les pages latines RESTANTES des PDF du banc (la vérité terrain existe déjà)
        for pdf in sorted({p["pdf"] for p in dev}):
            if pdf.stem.endswith(("-ru", "-zh", "-ar")):
                continue
            for numero in range(1, len(graphe_document_pdf.lignes_du_pdf(pdf)) + 1):
                if len([x for x in pages if x["split"] == "test"]) >= args.test // 2:
                    break
                if (pdf.name, numero) not in deja:
                    pages.append({"pdf": pdf, "page": numero, "questions": [], "split": "test"})
                    deja.add((pdf.name, numero))
        # 2) des pages d'AUTRES résolutions ONU, en latin, pour la variété des mises en page
        for pdf in sorted((RACINE / "data/onu/pdf").glob("A_RES_80_*.pdf")):
            if len([x for x in pages if x["split"] == "test"]) >= args.test:
                break
            if pdf.stem.endswith(("-ru", "-zh", "-ar")) or pdf in {p["pdf"] for p in dev}:
                continue
            for numero in range(1, min(len(graphe_document_pdf.lignes_du_pdf(pdf)), 2) + 1):
                if len([x for x in pages if x["split"] == "test"]) >= args.test:
                    break
                pages.append({"pdf": pdf, "page": numero, "questions": [], "split": "test"})
    args.sortie.mkdir(parents=True, exist_ok=True)
    tmp = args.sortie / "_tmp.jpg"
    entrees = []
    for page in pages:
        pdf, numero = page["pdf"], page["page"]
        propre = rendre_300(pdf, numero)
        for famille in familles:
            for graine in graines:
                image, params = fabriquer(propre, famille, graine, numero, tmp)
                nom = f"{pdf.stem}-p{numero}-s{graine}-{famille}.png"
                chemin = args.sortie / nom
                image.save(chemin)
                entrees.append({
                    "image": nom, "pdf": pdf.name, "page": numero, "split": page["split"],
                    "langue": mesurer_ocr.langue_de(pdf),
                    "famille": famille, "graine": graine,
                    "largeur": image.width, "hauteur": image.height,
                    "parametres": params,
                })
                print(f"  {nom} · {image.width}×{image.height}", flush=True)
    tmp.unlink(missing_ok=True)
    manifeste = {"date": "2026-10-31", "ligne": "R4.4", "nature": "scans SIMULÉS",
                 "generateur": "tools/simuler_scan.py", "entrees": entrees}
    (args.sortie / "manifeste.json").write_text(
        json.dumps(manifeste, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"\n{len(entrees)} scans → {args.sortie}/manifeste.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
