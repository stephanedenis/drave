#!/usr/bin/env python3
"""mesurer_cout.py — R4.4 : ce que le prétraitement et l'OCR coûtent, par page et par famille.

POURQUOI CE FICHIER. La métrique du lecteur n'est pas le débit : c'est la **compréhension par
unité de calcul** (R0.2). Le coût de l'OCR est donc un terme de la mesure, pas un détail. Ce banc
chronomètre, sur les scans de développement, le prétraitement (`nettoyer_scan.auto`) et l'OCR
(`graphe_document_ocr.manifeste`), page par page, famille par famille.

CE QU'IL MESURE : des secondes, sur une machine à 40 cœurs, avec tesseract 5.5.3 — une **borne**
indicative, pas une référence portable (le temps dépend du CPU et du nombre de threads).

Usage : python3 tools/mesurer_cout.py --pages 3 --sortie reports/r44-cout.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import graphe_document_ocr  # noqa: E402
import mesurer_ocr  # noqa: E402
import nettoyer_scan  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corpus", type=pathlib.Path, default=RACINE / "work/r44/scans/manifeste.json")
    ap.add_argument("--pages", type=int, default=3, help="pages par famille")
    ap.add_argument("--sortie", type=pathlib.Path, default=RACINE / "reports/r44-cout.json")
    args = ap.parse_args()
    corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
    vus: dict[str, int] = {}
    entrees = []
    for e in corpus["entrees"]:
        if e["split"] != "dev":
            continue
        if vus.get(e["famille"], 0) >= args.pages:
            continue
        vus[e["famille"]] = vus.get(e["famille"], 0) + 1
        entrees.append(e)
    from PIL import Image
    lignes = []
    for e in entrees:
        image = args.corpus.resolve().parent / e["image"]
        im = Image.open(image).convert("RGB")
        t0 = time.perf_counter()
        nettoyee, trace = nettoyer_scan.auto(im)
        t_net = time.perf_counter() - t0
        chemin = RACINE / "work/r44/cout" / f"{image.stem}-net.png"
        chemin.parent.mkdir(parents=True, exist_ok=True)
        nettoyee.save(chemin)
        t0 = time.perf_counter()
        manifeste = graphe_document_ocr.manifeste(chemin, e["langue"])
        t_ocr = time.perf_counter() - t0
        t0 = time.perf_counter()
        graphe_document_ocr.manifeste(image, e["langue"])
        t_brut = time.perf_counter() - t0
        lignes.append({"image": e["image"], "famille": e["famille"], "langue": e["langue"],
                       "nettoyage_s": round(t_net, 2), "ocr_s": round(t_ocr, 2),
                       "ocr_brut_s": round(t_brut, 2), "trace": trace,
                       "mots_ocr": len(mesurer_ocr.jetons(
                           mesurer_ocr.texte_du_manifeste(manifeste)))})
        print(f"  {e['image'][:42]:42s} nettoyage {t_net:5.2f} s · OCR {t_ocr:5.2f} s "
              f"(brut {t_brut:5.2f} s)", flush=True)
    from collections import defaultdict
    par = defaultdict(list)
    for l in lignes:
        par[l["famille"]].append(l)
    agregat = {f: {"pages": len(ls),
                   "nettoyage_s": round(sum(x["nettoyage_s"] for x in ls) / len(ls), 2),
                   "ocr_s": round(sum(x["ocr_s"] for x in ls) / len(ls), 2),
                   "ocr_brut_s": round(sum(x["ocr_brut_s"] for x in ls) / len(ls), 2)}
               for f, ls in par.items()}
    resultat = {"date": "2026-11-01", "ligne": "R4.4", "nature": "coût mesuré",
                "machine": "40 cœurs, tesseract 5.5.3, CPU", "agregat": agregat,
                "pages": lignes}
    args.sortie.parent.mkdir(parents=True, exist_ok=True)
    args.sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8")
    print()
    for f, a in sorted(agregat.items()):
        print(f"  {f:<11} nettoyage {a['nettoyage_s']:5.2f} s · OCR {a['ocr_s']:5.2f} s "
              f"· OCR brut {a['ocr_brut_s']:5.2f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
