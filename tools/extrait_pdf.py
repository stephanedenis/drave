#!/usr/bin/env python3
"""extrait_pdf.py — le texte natif des PDF locaux (les livres, les cours, les documents).

POURQUOI. Les corpus Wikipédia sont de la prose encyclopédique ; les documents locaux (les 104
livres de `Biblio_large`, les 2 711 notes de cours du CEGEP, les documents personnels) sont un
genre différent : des livres, des cours, des rapports. Ce script extrait le **texte natif** avec
`pdftotext`, détecte les **scannés** (texte trop court par page), déduplique, sépare par document
et écrit un corpus mesuré — les licences sont **nommées** (droits réservés, usage local ; le
corpus n'est pas diffusé).

Ce qu'il ne fait pas : l'**OCR** des scannés (le pipeline R4.4 le fera ; ici ils sont comptés et
signalés), la mise en page (les en-têtes/pieds de page restent), les formules et les tableaux
(perdus par le texte natif).

Usage :
  python3 tools/extrait_pdf.py --max-pdf 100      # pilote
  python3 tools/extrait_pdf.py                    # tous les PDF des racines
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
RACINES = [
    ("Biblio_large", pathlib.Path("/home/stephane/Data13TB/stephane/Biblio_large"),
     "livres — droits réservés, usage local, non diffusé"),
    ("CEGEP", pathlib.Path("/home/stephane/Data13TB/stephane/archives/CEGEP"),
     "notes de cours — droits réservés, usage local, non diffusé"),
]


def pages(pdf: pathlib.Path) -> int:
    try:
        s = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, timeout=30).stdout
        for ligne in s.splitlines():
            if ligne.startswith("Pages:"):
                return int(ligne.split()[1])
    except Exception:
        pass
    return 0


def texte(pdf: pathlib.Path) -> str:
    try:
        r = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
                           capture_output=True, timeout=120)
        return r.stdout.decode("utf-8", "ignore")
    except Exception:
        return ""


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
    ap.add_argument("--racine", action="append", default=[],
                    help="chemin:libellé (répétable) ; par défaut Biblio_large et CEGEP")
    ap.add_argument("--sortie", type=pathlib.Path, default=RACINE / "data/corpus_pdf")
    ap.add_argument("--manifeste", type=pathlib.Path,
                    default=RACINE / "reports/corpus-pdf.json")
    ap.add_argument("--max-pdf", type=int, default=0)
    ap.add_argument("--min-chars", type=int, default=300)
    ap.add_argument("--seuil-scan", type=int, default=50, help="caractères par page sous lesquels le PDF est scanné")
    ap.add_argument("--chunk", type=int, default=8192)
    ap.add_argument("--val", type=float, default=0.05)
    ap.add_argument("--test", type=float, default=0.05)
    ap.add_argument("--graine", type=int, default=1)
    args = ap.parse_args()
    racines = ([(lib, pathlib.Path(chemin)) for chemin, lib in
                (r.split(":", 1) if ":" in r else (r, "") for r in args.racine)]
               or [(lib, chemin) for lib, chemin, _ in RACINES])
    args.sortie.mkdir(parents=True, exist_ok=True)
    seuil_val, seuil_test = int(args.val * 1000), int((args.val + args.test) * 1000)
    fichiers = {n: (args.sortie / f"{n}.txt").open("w", encoding="utf-8") for n in ("train", "val", "test")}
    vus, vus_troncons = set(), set()
    stats = {"racines": [], "pdfs": 0, "pages": 0, "documents_gardes": 0,
             "documents_scannes": 0, "documents_courts": 0, "documents_doublons": 0,
             "caracteres_gardes": 0, "troncons": 0, "troncons_doublons": 0,
             "octets": {"train": 0, "val": 0, "test": 0},
             "documents": {"train": 0, "val": 0, "test": 0},
             "echantillon": ""}
    for lib, racine in racines:
        if not racine.exists():
            print(f"  ! racine absente : {racine}", flush=True)
            continue
        pdfs = sorted(racine.rglob("*.pdf"))
        stats["racines"].append({"nom": lib, "chemin": racine.as_posix(), "pdfs": len(pdfs)})
        for pdf in pdfs:
            if args.max_pdf and stats["pdfs"] >= args.max_pdf:
                break
            stats["pdfs"] += 1
            npages = pages(pdf)
            stats["pages"] += npages
            t = texte(pdf)
            propre = t.strip()
            if npages and len(propre) / max(npages, 1) < args.seuil_scan:
                stats["documents_scannes"] += 1
                continue
            if len(propre) < args.min_chars:
                stats["documents_courts"] += 1
                continue
            marque = empreinte(propre)
            if marque in vus:
                stats["documents_doublons"] += 1
                continue
            vus.add(marque)
            doc = f"{pdf.stem}\n{propre}"
            h = int(empreinte(f"{args.graine}:{pdf.as_posix()}", 8), 16) % 1000
            split = "val" if h < seuil_val else ("test" if h < seuil_test else "train")
            morceaux = []
            for m in troncons(doc, args.chunk):
                if split == "train":
                    mq = empreinte(m)
                    if mq in vus_troncons:
                        stats["troncons_doublons"] += 1
                        continue
                    vus_troncons.add(mq)
                morceaux.append(m)
            if not morceaux:
                continue
            fichiers[split].write("\n\n".join(morceaux) + "\n\n")
            stats["documents_gardes"] += 1
            stats["documents"][split] += 1
            stats["troncons"] += len(morceaux)
            stats["caracteres_gardes"] += len(propre)
            if stats["documents_gardes"] <= 2:
                stats["echantillon"] = (stats["echantillon"] + "\n---\n" + doc[:400]).strip()
            if stats["pdfs"] % 500 == 0:
                print(f"  {stats['pdfs']} PDF · {stats['documents_gardes']} gardés · "
                      f"{stats['caracteres_gardes'] / 1e6:.1f} M car", flush=True)
    for f in fichiers.values():
        f.close()
    stats["mots_estimes"] = int(stats["caracteres_gardes"] / 6.2)
    stats["note_mots"] = "caractères / 6,2 (estimation, le cas échéant)"
    for nom in ("train", "val", "test"):
        chemin = args.sortie / f"{nom}.txt"
        stats["octets"][nom] = chemin.stat().st_size
        h = hashlib.sha256()
        with chemin.open("rb") as f:
            for bloc in iter(lambda: f.read(1 << 20), b""):
                h.update(bloc)
        stats[f"sha256_{nom}"] = h.hexdigest()
    stats["licences"] = []
    for lib, _ in racines:
        lic = next((l for n, _, l in RACINES if n == lib), "à préciser")
        stats["licences"].append({"racine": lib, "licence": lic})
    args.manifeste.parent.mkdir(parents=True, exist_ok=True)
    args.manifeste.write_text(json.dumps({
        "date": "2026-11-01", "ligne": "Données", "nature": "corpus PDF local (texte natif)",
        "methode": {"extraction": "pdftotext -enc UTF-8", "page": "pdfinfo",
                    "scanne": f"moins de {args.seuil_scan} caractères/page",
                    "deduplication": "documents + tronçons (BLAKE2b)",
                    "split": f"hash salé du chemin : {args.val:.0%} val, {args.test:.0%} test"},
        **stats,
        "limites": ["texte natif seulement : les scannés sont comptés, pas océrisés",
                    "en-têtes et pieds de page conservés ; formules et tableaux perdus",
                    "licences : droits réservés, corpus local non diffusé"]},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: stats[k] for k in ("pdfs", "pages", "documents_gardes",
                                             "documents_scannes", "caracteres_gardes",
                                             "octets", "troncons")}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
