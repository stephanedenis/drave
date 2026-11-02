#!/usr/bin/env python3
"""ocr_pdf.py — l'OCR des PDF **scannés** (R4.4 appliqué aux documents réels).

POURQUOI. `extrait_pdf.py` extrait le texte natif ; les PDF sans couche texte (les scans) sont
comptés et écartés. Ce script les **océrise** avec le tesseract installé sans root par
`installer_ocr.sh` (5.5.3, fra+eng) : `pdftoppm` rend les pages, `tesseract` les lit.

Ce qu'il ne fait pas (encore) : le prétraitement d'image de R4.4 (`nettoyer_scan.py` : rotation,
contraste, colonnes) — le pilote mesure l'OCR **brut** ; la WER réelle n'a pas de vérité terrain
(seule la parité R4.4 sur scans simulés la donne), donc la fiche donne le débit, les caractères et
un échantillon, pas une WER inventée.

Usage :
  python3 tools/ocr_pdf.py --max-doc 20          # pilote (les 20 premiers scannés)
  python3 tools/ocr_pdf.py                       # tous les scannés des racines
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time

RACINE = pathlib.Path(__file__).resolve().parent.parent
ROOT = RACINE / "work/ocr/root"
TESS = ROOT / "usr/bin/tesseract"
ENV = dict(os.environ, LD_LIBRARY_PATH=str(ROOT / "usr/lib64"),
           TESSDATA_PREFIX=str(ROOT / "usr/share/tessdata"))
RACINES = [("Biblio_large", pathlib.Path("/home/stephane/Data13TB/stephane/Biblio_large"),
            "livres — droits réservés, usage local, non diffusé"),
           ("CEGEP", pathlib.Path("/home/stephane/Data13TB/stephane/archives/CEGEP"),
            "notes de cours — droits réservés, usage local, non diffusé")]


def pages(pdf: pathlib.Path) -> int:
    try:
        s = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, timeout=30).stdout
        for ligne in s.splitlines():
            if ligne.startswith("Pages:"):
                return int(ligne.split()[1])
    except Exception:
        pass
    return 0


def natif(pdf: pathlib.Path) -> str:
    try:
        return subprocess.run(["pdftotext", "-f", "1", "-l", "2", "-enc", "UTF-8", str(pdf), "-"],
                              capture_output=True, timeout=60).stdout.decode("utf-8", "ignore")
    except Exception:
        return ""


def ocr(pdf: pathlib.Path, dpi: int, langues: str, max_pages: int) -> tuple[str, int]:
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="ocr-pdf-"))
    try:
        cmd = ["pdftoppm", "-r", str(dpi), "-gray", "-png"]
        if max_pages:
            cmd += ["-f", "1", "-l", str(max_pages)]
        cmd += [str(pdf), str(tmp / "p")]
        try:
            subprocess.run(cmd, capture_output=True, timeout=1800)
        except subprocess.TimeoutExpired:
            print(f"  ! timeout pdftoppm : {pdf.name} (ignoré)", flush=True)
            return "", 0
        textes = []
        for png in sorted(tmp.glob("p-*.png")):
            r = subprocess.run([str(TESS), str(png), "stdout", "-l", langues, "--psm", "3"],
                               capture_output=True, env=ENV, timeout=120)
            textes.append(r.stdout.decode("utf-8", "ignore"))
        return "\n".join(textes).strip(), len(textes)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def empreinte(t: str, taille: int = 16) -> str:
    return hashlib.blake2b(t.encode("utf-8"), digest_size=taille).hexdigest()


def troncons(t: str, taille: int):
    debut = 0
    while debut < len(t):
        fin = min(debut + taille, len(t))
        if fin < len(t):
            coupe = t.rfind(" ", debut + taille // 2, fin)
            if coupe > debut:
                fin = coupe
        m = t[debut:fin].strip()
        if m:
            yield m
        debut = fin


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-doc", type=int, default=0)
    ap.add_argument("--racine", default="", help="restreindre à une racine : Biblio_large, CEGEP")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--langues", default="fra+eng")
    ap.add_argument("--max-pages", type=int, default=0)
    ap.add_argument("--min-chars", type=int, default=300)
    ap.add_argument("--chunk", type=int, default=8192)
    ap.add_argument("--val", type=float, default=0.05)
    ap.add_argument("--test", type=float, default=0.05)
    ap.add_argument("--graine", type=int, default=1)
    ap.add_argument("--sortie", type=pathlib.Path, default=RACINE / "data/corpus_ocr")
    ap.add_argument("--manifeste", type=pathlib.Path, default=RACINE / "reports/ocr-pdf.json")
    args = ap.parse_args()
    if not TESS.exists():
        sys.exit("tesseract absent : lancer tools/installer_ocr.sh")
    args.sortie.mkdir(parents=True, exist_ok=True)
    seuil_val, seuil_test = int(args.val * 1000), int((args.val + args.test) * 1000)
    fichiers = {n: (args.sortie / f"{n}.txt").open("w", encoding="utf-8") for n in ("train", "val", "test")}
    vus, vus_troncons = set(), set()
    stats = {"pdfs": 0, "scannes": 0, "ocrises": 0, "pages_ocr": 0, "caracteres": 0,
             "troncons": 0, "documents": {"train": 0, "val": 0, "test": 0},
             "octets": {"train": 0, "val": 0, "test": 0}, "temps_s": 0,
             "echantillon": "", "racines": []}
    t0 = time.time()
    for lib, racine, lic in RACINES:
        if args.racine and lib != args.racine:
            continue
        if not racine.exists():
            continue
        pdfs = sorted(racine.rglob("*.pdf"))
        stats["racines"].append({"nom": lib, "chemin": racine.as_posix(), "pdfs": len(pdfs), "licence": lic})
        for pdf in pdfs:
            if args.max_doc and stats["ocrises"] >= args.max_doc:
                break
            npages = pages(pdf)
            if not npages:
                continue
            stats["pdfs"] += 1
            t = natif(pdf)
            if len(t.strip()) / max(npages, 1) >= 50:
                continue  # il a du texte natif : déjà dans le corpus PDF
            stats["scannes"] += 1
            texte, n = ocr(pdf, args.dpi, args.langues, args.max_pages)
            if len(texte) < args.min_chars:
                continue
            marque = empreinte(texte)
            if marque in vus:
                continue
            vus.add(marque)
            doc = f"{pdf.stem}\n{texte}"
            h = int(empreinte(f"{args.graine}:{pdf.as_posix()}", 8), 16) % 1000
            split = "val" if h < seuil_val else ("test" if h < seuil_test else "train")
            morceaux = []
            for m in troncons(doc, args.chunk):
                if split == "train":
                    mq = empreinte(m)
                    if mq in vus_troncons:
                        continue
                    vus_troncons.add(mq)
                morceaux.append(m)
            if not morceaux:
                continue
            fichiers[split].write("\n\n".join(morceaux) + "\n\n")
            stats["ocrises"] += 1
            stats["documents"][split] += 1
            stats["pages_ocr"] += n
            stats["troncons"] += len(morceaux)
            stats["caracteres"] += len(texte)
            if stats["ocrises"] <= 2:
                stats["echantillon"] = (stats["echantillon"] + "\n---\n" + doc[:500]).strip()
            print(f"  {lib} · {pdf.name[:40]} · {n} p · {len(texte)} car", flush=True)
    for f in fichiers.values():
        f.close()
    stats["temps_s"] = round(time.time() - t0, 1)
    stats["mots_estimes"] = int(stats["caracteres"] / 6.2)
    for nom in ("train", "val", "test"):
        chemin = args.sortie / f"{nom}.txt"
        stats["octets"][nom] = chemin.stat().st_size
        h = hashlib.sha256()
        with chemin.open("rb") as f:
            for bloc in iter(lambda: f.read(1 << 20), b""):
                h.update(bloc)
        stats[f"sha256_{nom}"] = h.hexdigest()
    args.manifeste.parent.mkdir(parents=True, exist_ok=True)
    args.manifeste.write_text(json.dumps({
        "date": "2026-11-01", "ligne": "Données (R4.4 appliqué)", "nature": "corpus OCR des PDF scannés",
        "dispositif": {"ocr": "tesseract 5.5.3 sans root (work/ocr/root)", "langues": args.langues,
                       "dpi": args.dpi, "psm": 3, "pretraitement": "aucun (le R4.4 le fera)",
                       "split": f"hash salé du chemin : {args.val:.0%} val, {args.test:.0%} test",
                       "deduplication": "documents + tronçons"},
        **stats,
        "limites": ["OCR brut : rotation/contraste/colonnes non traités (le R4.4 les traite)",
                    "WER non mesurée (pas de vérité terrain sur les scans réels)",
                    "licences : droits réservés, corpus local non diffusé"]},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: stats[k] for k in ("scannes", "ocrises", "pages_ocr", "caracteres",
                                             "temps_s", "octets")}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
