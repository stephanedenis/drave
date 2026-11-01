#!/usr/bin/env python3
"""mesurer_reel.py — R4.4 : un VRAI scan, et un jumeau qui n'est pas parfait.

POURQUOI CE FICHIER. Les scans de `simuler_scan.py` sont des dégradations **simulées** : ils
mesurent la robustesse, pas la réalité du papier. Il n'y a pas de scanner sur la machine, mais
il y a des scans publics : ce banc prend un PDF **réellement scanné** (Internet Archive, OCR
d'éditeur) et compare notre lecture à la **couche texte du PDF** — page par page, même page.

CE QUE LA MESURE VAUT, ET CE QU'ELLE NE VAUT PAS. La référence est la couche OCR d'Internet
Archive : ce n'est PAS une vérité humaine, c'est un **autre moteur**. Le WER mesure donc un
**accord entre moteurs** sur un vrai scan, pas une exactitude absolue — c'est écrit dans la
fiche. Ce que ce banc prouve : la chaîne tourne sur du papier réel, sans vérité terrain
fabriquée, et le prétraitement y fait (ou n'y fait pas) ce qu'il promet.

SOURCE UTILISÉE (domaine public) :
  https://archive.org/download/voyageaucentrede00vernuoft/voyageaucentrede00vernuoft.pdf
  Jules Verne, *Voyage au centre de la terre* — scan LuraDocument, 300 dpi, 244 pages.

Usage :
  python3 tools/mesurer_reel.py --pdf work/r44/reel/livre.pdf --pages 30,50,70 --sortie work/r44/reel.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import graphe_document_ocr  # noqa: E402
import mesurer_ocr  # noqa: E402
import mesurer_scans  # noqa: E402
import nettoyer_scan  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
CACHE = RACINE / "work/r44/reel"


def rendu(pdf: pathlib.Path, page: int) -> pathlib.Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    png = CACHE / f"{pdf.stem}-p{page}.png"
    if not png.exists():
        subprocess.run(["pdftoppm", "-r", "300", "-f", str(page), "-l", str(page),
                        "-singlefile", "-png", str(pdf), str(png.with_suffix(""))],
                       check=True, capture_output=True)
    return png


def reference(pdf: pathlib.Path, page: int) -> str:
    return subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), "-layout",
                           str(pdf), "-"], capture_output=True, text=True, check=True).stdout


def mesure(pdf: pathlib.Path, page: int) -> dict:
    from PIL import Image
    png = rendu(pdf, page)
    im = Image.open(png).convert("RGB")
    propre, trace = nettoyer_scan.auto(im)
    chemin = CACHE / f"{pdf.stem}-p{page}-net.png"
    if not chemin.exists():
        propre.save(chemin)
    ref = mesurer_ocr.jetons(reference(pdf, page))
    m = mesurer_scans.manifeste_ocr(chemin, "fra", exposants=True, colonnes=True)
    hyp = mesurer_ocr.jetons(mesurer_ocr.texte_du_manifeste(m))
    # contrôle : la même page sans prétraitement (l'écart dit ce que le nettoyage apporte
    # sur un scan réel — parfois rien, et c'est une information)
    m_brut = mesurer_scans.manifeste_ocr(png, "fra", exposants=True, colonnes=True)
    hyp_brut = mesurer_ocr.jetons(mesurer_ocr.texte_du_manifeste(m_brut))
    return {"page": page, "mots_reference": len(ref), "mots_ocr": len(hyp),
            "wer": round(mesurer_ocr.wer(ref, hyp) / max(len(ref), 1), 4),
            "wer_brut": round(mesurer_ocr.wer(ref, hyp_brut) / max(len(ref), 1), 4),
            "confiance": mesurer_ocr.confiance_moyenne(m),
            "trace": trace}


def agrege(lignes: list[dict]) -> dict:
    mots = sum(l["mots_reference"] for l in lignes)
    return {"pages": len(lignes), "mots_reference": mots,
            "wer": round(sum(round(l["wer"] * l["mots_reference"]) for l in lignes) / max(mots, 1), 4),
            "wer_brut": round(sum(round(l["wer_brut"] * l["mots_reference"]) for l in lignes) / max(mots, 1), 4),
            "confiance": round(sum(l["confiance"] * l["mots_reference"] for l in lignes) / max(mots, 1), 1)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pdf", type=pathlib.Path, required=True)
    ap.add_argument("--pages", default="30,50,70,90,110,130,150,170,190,210")
    ap.add_argument("--sortie", type=pathlib.Path, default=RACINE / "work/r44/reel.json")
    args = ap.parse_args()
    pages = [int(p) for p in args.pages.split(",") if p.strip()]
    lignes = []
    for page in pages:
        ligne = mesure(args.pdf, page)
        lignes.append(ligne)
        print(f"  page {page:3d} · WER {ligne['wer']:6.2%} (brut {ligne['wer_brut']:6.2%}) "
              f"· conf {ligne['confiance']:5.1f} · {ligne['mots_reference']} mots", flush=True)
    resultat = {"date": "2026-10-31", "ligne": "R4.4", "nature": "scan RÉEL",
                "reference": "couche OCR du PDF (Internet Archive) — pas une vérité humaine",
                "source": "Voyage au centre de la terre, Internet Archive "
                          "voyageaucentrede00vernuoft (LuraDocument, 300 dpi)",
                "agregat": agrege(lignes), "pages": lignes}
    args.sortie.parent.mkdir(parents=True, exist_ok=True)
    args.sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8")
    a = resultat["agregat"]
    print(f"\n  {a['pages']} pages · WER {a['wer']:.2%} nettoyé · {a['wer_brut']:.2%} brut "
          f"· confiance {a['confiance']:.1f} → {args.sortie}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
