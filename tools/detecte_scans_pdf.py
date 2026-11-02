#!/usr/bin/env python3
"""detecte_scans_pdf.py — quels PDF sont *vraiment* des scans, et lesquels restent.

POURQUOI. `tools/ocr_pdf.py` classe un PDF « scanné » sur le texte natif de ses **deux premières
pages**. Sur le fonds CEGEP, cela donne 807 candidats ; le texte **intégral** (`pdftotext` complet,
seuil de 50 caractères par page, la règle de `tools/extrait_pdf.py`) n'en confirme que 147 : les
couvertures sans texte des livres natifs font sur-classer 5,5×. Ce script mesure la vérité, déduit
les doublons exacts (SHA-256) et écrit la liste des scans à océriser.

Ne pas confondre les deux questions : `--deja N` (dans `ocr_pdf.py`) saute N PDF **dans l'ordre du
parcours** ; ce script dit **quels** PDF sont des scans. Une reprise de fond passe par `--liste`.

Usage :
  python3 tools/detecte_scans_pdf.py --racine CEGEP --sortie reports/ocr-pdf-cegep-detection.json \\
      --liste work/ocr/scans-uniques.txt
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import pathlib
import subprocess
import time

RACINE = pathlib.Path(__file__).resolve().parent.parent
RACINES = {"Biblio_large": pathlib.Path("/home/stephane/Data13TB/stephane/Biblio_large"),
           "CEGEP": pathlib.Path("/home/stephane/Data13TB/stephane/archives/CEGEP")}


def mesurer(p: pathlib.Path, seuil: int) -> dict:
    try:
        s = subprocess.run(["pdfinfo", str(p)], capture_output=True, text=True, timeout=30).stdout
        pages = 0
        for ligne in s.splitlines():
            if ligne.startswith("Pages:"):
                pages = int(ligne.split()[1])
                break
        if not pages:
            return {"chemin": str(p), "pages": 0, "caracteres": 0, "scan": False}
        t = subprocess.run(["pdftotext", "-enc", "UTF-8", str(p), "-"],
                           capture_output=True, timeout=120).stdout.decode("utf-8", "ignore")
        car = len(t.strip())
        return {"chemin": str(p), "pages": pages, "caracteres": car, "scan": car / pages < seuil}
    except Exception:
        return {"chemin": str(p), "pages": 0, "caracteres": 0, "scan": False}


def empreinte(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--racine", default="CEGEP", help="CEGEP, Biblio_large, ou un chemin absolu")
    ap.add_argument("--sortie", type=pathlib.Path,
                    default=RACINE / "reports/ocr-pdf-cegep-detection.json")
    ap.add_argument("--liste", type=pathlib.Path, default=None,
                    help="écrire les chemins des scans uniques (un par ligne)")
    ap.add_argument("--seuil", type=int, default=50, help="caractères natifs par page sous lesquels c'est un scan")
    ap.add_argument("--ouvriers", type=int, default=16)
    ap.add_argument("--sans-dedup", action="store_true", help="ne pas dédupliquer par SHA-256")
    args = ap.parse_args()
    racine = RACINES.get(args.racine, pathlib.Path(args.racine))
    if not racine.exists():
        raise SystemExit(f"racine absente : {racine}")
    pdfs = sorted(racine.rglob("*.pdf"))
    with cf.ThreadPoolExecutor(max_workers=args.ouvriers) as ex:
        mesures = list(ex.map(lambda p: mesurer(p, args.seuil), pdfs))
    scans = [m for m in mesures if m["scan"]]
    if args.sans_dedup:
        uniques = scans
        for m in uniques:
            m["sha256"] = ""
    else:
        with cf.ThreadPoolExecutor(max_workers=args.ouvriers) as ex:
            hs = list(ex.map(lambda m: empreinte(pathlib.Path(m["chemin"])), scans))
        vus: dict[str, dict] = {}
        uniques = []
        for m, h in zip(scans, hs):
            m["sha256"] = h
            m["doublon"] = h in vus
            if h not in vus:
                vus[h] = m
                uniques.append(m)
    sortie = {
        "date": time.strftime("%Y-%m-%d"),
        "ligne": "Données (R4.4 appliqué)",
        "nature": "détection des PDF scannés sur le texte intégral",
        "methode": {"outil": "pdftotext complet + pdfinfo", "seuil_car_par_page": args.seuil,
                    "deduplication": "SHA-256 des fichiers" if not args.sans_dedup else "aucune",
                    "racine": str(racine)},
        "pdfs": len(pdfs),
        "scans": len(scans),
        "pages_scans": sum(m["pages"] for m in scans),
        "uniques": len(uniques),
        "pages_uniques": sum(m["pages"] for m in uniques),
        "doublons": len(scans) - len(uniques),
        "detail": sorted(uniques, key=lambda m: m["chemin"]),
    }
    args.sortie.parent.mkdir(parents=True, exist_ok=True)
    args.sortie.write_text(json.dumps(sortie, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if args.liste:
        args.liste.parent.mkdir(parents=True, exist_ok=True)
        args.liste.write_text("".join(m["chemin"] + "\n" for m in uniques), encoding="utf-8")
    print(json.dumps({k: sortie[k] for k in ("pdfs", "scans", "pages_scans", "uniques",
                                             "pages_uniques", "doublons")},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
