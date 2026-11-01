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


def reference_colonnes(xml: pathlib.Path, page: int, inverse: bool = False) -> str:
    """La référence dans l'ORDRE DE LECTURE des colonnes, construite depuis les coordonnées
    des mots du DjVu : les mots à gauche du centre, groupés en lignes, puis ceux de droite.
    `inverse` rend l'ordre opposé — le contrôle qui doit ÉCHOUER si notre lecteur lit bien
    la gauche d'abord."""
    import statistics
    import xml.etree.ElementTree as ET
    root = ET.parse(xml).getroot()
    objets = [o for o in root.iter() if o.tag.split("}")[-1] == "OBJECT"]
    o = objets[page - 1]
    centre = int(o.get("width", "0")) / 2
    mots = []
    for w in o.iter():
        if w.tag.split("}")[-1] != "WORD":
            continue
        champs = (w.get("coords") or "").split(",")
        if len(champs) != 4:
            continue
        x1, y1, x2, y2 = map(int, champs)
        mots.append({"x": (x1 + x2) / 2, "top": y2, "bas": y1, "texte": w.text or ""})
    if not mots:
        return ""
    hauteur = statistics.median(max(m["bas"] - m["top"], 1) for m in mots)

    def lignes(colonne):
        out = []
        for m in sorted(colonne, key=lambda m: (m["top"], m["x"])):
            if out and abs(m["top"] - out[-1]["top"]) < hauteur * 0.6:
                out[-1]["mots"].append(m)
                out[-1]["top"] = min(out[-1]["top"], m["top"])
            else:
                out.append({"top": m["top"], "mots": [m]})
        return out

    gauche = lignes([m for m in mots if m["x"] < centre])
    droite = lignes([m for m in mots if m["x"] >= centre])
    ordre = (droite + gauche) if inverse else (gauche + droite)
    return " ".join(m["texte"] for l in ordre for m in sorted(l["mots"], key=lambda m: m["x"]))


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


def mesure(pdf: pathlib.Path, page: int, xml: pathlib.Path | None = None,
           langue: str = "fra") -> dict:
    from PIL import Image
    png = rendu(pdf, page)
    im = Image.open(png).convert("RGB")
    propre, trace = nettoyer_scan.auto(im)
    chemin = CACHE / f"{pdf.stem}-p{page}-net.png"
    if not chemin.exists():
        propre.save(chemin)
    ref = mesurer_ocr.jetons(reference(pdf, page))
    m = mesurer_scans.manifeste_ocr(chemin, langue, exposants=True, colonnes=True)
    hyp = mesurer_ocr.jetons(mesurer_ocr.texte_du_manifeste(m))
    # le RAPPEL MULTIENSEMBLE ne dépend pas de l'ordre : sur une page à deux colonnes, la
    # couche de référence peut lire en lignes entrelacées et notre lecteur par colonne — le WER
    # compte alors un désaccord d'ORDRE, pas de reconnaissance. Les deux chiffres sont dits.
    from collections import Counter
    commun = sum((Counter(ref) & Counter(hyp)).values())
    # contrôle : la même page sans prétraitement (l'écart dit ce que le nettoyage apporte
    # sur un scan réel — parfois rien, et c'est une information)
    m_brut = mesurer_scans.manifeste_ocr(png, langue, exposants=True, colonnes=True)
    hyp_brut = mesurer_ocr.jetons(mesurer_ocr.texte_du_manifeste(m_brut))
    ligne = {"page": page, "mots_reference": len(ref), "mots_ocr": len(hyp),
             "wer": round(mesurer_ocr.wer(ref, hyp) / max(len(ref), 1), 4),
             "wer_brut": round(mesurer_ocr.wer(ref, hyp_brut) / max(len(ref), 1), 4),
             "rappel": round(commun / max(len(ref), 1), 4),
             "precision": round(commun / max(len(hyp), 1), 4),
             "confiance": mesurer_ocr.confiance_moyenne(m),
             "trace": trace}
    if xml is not None:
        # l'ordre des colonnes, et son contrôle : l'ordre INVERSE doit échouer
        ordre = mesurer_ocr.jetons(reference_colonnes(xml, page))
        inverse = mesurer_ocr.jetons(reference_colonnes(xml, page, inverse=True))
        ligne["wer_colonnes"] = round(mesurer_ocr.wer(ordre, hyp) / max(len(ordre), 1), 4)
        ligne["wer_colonnes_inverse"] = round(
            mesurer_ocr.wer(inverse, hyp) / max(len(inverse), 1), 4)
        ligne["mots_reference_colonnes"] = len(ordre)
    return ligne


def agrege(lignes: list[dict]) -> dict:
    mots = sum(l["mots_reference"] for l in lignes)
    return {"pages": len(lignes), "mots_reference": mots,
            "wer": round(sum(round(l["wer"] * l["mots_reference"]) for l in lignes) / max(mots, 1), 4),
            "wer_brut": round(sum(round(l["wer_brut"] * l["mots_reference"]) for l in lignes) / max(mots, 1), 4),
            "rappel": round(sum(round(l["rappel"] * l["mots_reference"]) for l in lignes) / max(mots, 1), 4),
            "confiance": round(sum(l["confiance"] * l["mots_reference"] for l in lignes) / max(mots, 1), 1),
            **({"wer_colonnes": round(sum(round(l["wer_colonnes"] * l["mots_reference"]) for l in lignes) / max(mots, 1), 4),
                "wer_colonnes_inverse": round(sum(round(l["wer_colonnes_inverse"] * l["mots_reference"]) for l in lignes) / max(mots, 1), 4)}
               if all("wer_colonnes" in l for l in lignes) else {})}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pdf", type=pathlib.Path, required=True)
    ap.add_argument("--pages", default="30,50,70,90,110,130,150,170,190,210")
    ap.add_argument("--langue", default="fra")
    ap.add_argument("--djvu-xml", type=pathlib.Path,
                    help="référence d'ordre des colonnes depuis les coordonnées DjVu")
    ap.add_argument("--sortie", type=pathlib.Path, default=RACINE / "work/r44/reel.json")
    args = ap.parse_args()
    pages = [int(p) for p in args.pages.split(",") if p.strip()]
    lignes = []
    for page in pages:
        ligne = mesure(args.pdf, page, args.djvu_xml, args.langue)
        lignes.append(ligne)
        print(f"  page {page:3d} · WER {ligne['wer']:6.2%} (brut {ligne['wer_brut']:6.2%}) "
              f"· rappel {ligne['rappel']:6.2%} · conf {ligne['confiance']:5.1f} "
              f"· {ligne['mots_reference']} mots"
              + (f" · colonnes {ligne['wer_colonnes']:6.2%} (inverse {ligne['wer_colonnes_inverse']:6.2%})"
                 if "wer_colonnes" in ligne else ""), flush=True)
    resultat = {"date": "2026-10-31", "ligne": "R4.4", "nature": "scan RÉEL",
                "reference": "couche OCR du PDF (Internet Archive) — pas une vérité humaine",
                **({"djvu": args.djvu_xml.as_posix()} if args.djvu_xml else {}),
                "source": args.pdf.name,
                "note_colonnes": ("la référence d'ordre des colonnes ne s'applique qu'aux pages à "
                                  "deux colonnes ; l'agrégat wer_colonnes mélange donc les deux "
                                  "mises en page — lire le détail page par page"),
                "agregat": agrege(lignes), "pages": lignes}
    args.sortie.parent.mkdir(parents=True, exist_ok=True)
    args.sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8")
    a = resultat["agregat"]
    print(f"\n  {a['pages']} pages · WER {a['wer']:.2%} nettoyé · {a['wer_brut']:.2%} brut "
          f"· rappel multiensemble {a['rappel']:.2%} · confiance {a['confiance']:.1f} "
          f"→ {args.sortie}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
