#!/usr/bin/env python3
"""graphe_document_ocr.py — l'OCR entre dans R0.1 par la MÊME porte que le texte natif.

POURQUOI CE FICHIER. R4.4 était bloquée par une ressource absente, pas par une idée :
« aucun OCR installé (ni tesseract ni pytesseract) ». `tools/installer_ocr.sh` installe
tesseract sans root ; ce module le branche sur le graphe de document de R0.1. L'OCR ne
réinvente donc ni un format ni des offsets : il rend des **blocs**, et le manifeste est
construit par `graphe_document.manifeste_de_blocs`. La comparaison entre une page lue en
texte natif et la même page lue en OCR mesure l'OCR — pas deux façons de compter les octets.

CE QUE LE MODULE GARDE, ET POURQUOI. La confiance de chaque mot (sortie TSV de tesseract)
est agrégée par **bloc** et rangée dans `prov` : une lecture OCR qui ne dit pas son score
n'est pas une lecture, c'est une devinette — la porte R4.4 exige que les scores soient
tracés. La provenance d'un bloc porte aussi sa **page** et son **y**, comme le parseur PDF.

CE QU'IL NE REVENDIQUE PAS. La mise en page est reconstruite par la hauteur de ligne,
l'écart vertical et le retrait — la même heuristique que `graphe_document_pdf.py`, pas un
modèle de layout. Un scan de travers, une page à deux colonnes denses ou un tableau non
balisé ne sont pas revendiqués : ils restent à mesurer (R4.4, étapes 2 et 3).

Usage :
  python3 tools/graphe_document_ocr.py work/ocr/pages/p1-1.png --json
  python3 tools/graphe_document_ocr.py image.png --langue fra
  python3 tools/graphe_document_ocr.py --version
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import statistics
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import graphe_document  # noqa: E402  (le manifeste commun)
import graphe_document_pdf  # noqa: E402  (le vocabulaire des lignes de titre)

RACINE = pathlib.Path(__file__).resolve().parent.parent
VERSION = 1
PREFIXE = pathlib.Path(os.environ.get("TESSERACT_PREFIX", RACINE / "work/ocr/root"))
BIN = pathlib.Path(os.environ.get("TESSERACT", PREFIXE / "usr/bin/tesseract"))
TESSDATA = pathlib.Path(os.environ.get("TESSDATA_PREFIX", PREFIXE / "usr/share/tessdata"))


def _env() -> dict:
    """L'environnement de l'exécutable extrait : ses bibliothèques, ses données, rien d'autre."""
    env = dict(os.environ)
    lib = PREFIXE / "usr/lib64"
    if lib.exists():
        env["LD_LIBRARY_PATH"] = f"{lib}:{env.get('LD_LIBRARY_PATH', '')}".rstrip(":")
    env["TESSDATA_PREFIX"] = str(TESSDATA)
    return env


def exige() -> None:
    if not BIN.exists():
        raise SystemExit(
            f"OCR absent : {BIN}\n"
            "  l'installer sans root : tools/installer_ocr.sh")


def version() -> str:
    exige()
    sortie = subprocess.run([str(BIN), "--version"], env=_env(),
                            capture_output=True, text=True)
    return (sortie.stdout or sortie.stderr).splitlines()[0].strip()


def mots(image: pathlib.Path, langue: str = "fra", psm: int = 3) -> list[dict]:
    """Les mots, avec leur boîte et leur CONFIANCE. On demande le TSV explicitement par
    `-c` : les configs (`tsv`, `hocr`) ne sont pas dans le paquet de données, et une
    installation qui dépend d'un fichier de config absent échoue lentement, en silence."""
    exige()
    commande = [str(BIN), str(image), "stdout", "-l", langue, "--psm", str(psm),
                "-c", "tessedit_create_tsv=1"]
    sortie = subprocess.run(commande, env=_env(), capture_output=True, text=True)
    if sortie.returncode != 0:
        raise SystemExit(f"tesseract a échoué ({sortie.returncode}) : {sortie.stderr[-300:]}")
    lignes = sortie.stdout.splitlines()
    if not lignes:
        return []
    entetes = lignes[0].split("\t")
    if "conf" not in entetes:  # un TSV sans confiance n'est pas le TSV qu'on a demandé
        raise SystemExit("sortie tesseract inattendue : pas de colonne « conf »")
    out = []
    for ligne in lignes[1:]:
        champs = ligne.split("\t")
        if len(champs) < len(entetes):
            continue
        d = dict(zip(entetes, champs))
        if d.get("level") != "5" or not d.get("text", "").strip():
            continue
        try:
            conf = float(d["conf"])
        except ValueError:
            continue
        if conf < 0:  # -1 = mot vide côté tesseract, ce n'est pas un mot lu
            continue
        out.append({
            "texte": d["text"], "conf": conf,
            "left": int(d["left"]), "top": int(d["top"]),
            "width": int(d["width"]), "height": int(d["height"]),
            "bloc": int(d["block_num"]), "par": int(d["par_num"]),
            "ligne": int(d["line_num"]), "mot": int(d["word_num"]),
        })
    return out


def _typographie(texte: str) -> str:
    """Les blancs que l'OCR ajoute autour de la ponctuation française. On ne touche à aucun
    mot : seule l'espace fautive part, sinon le WER mesurerait la typographie."""
    texte = re.sub(r"\s+([,;:.!?»%])", r"\1", texte)
    texte = re.sub(r"«\s+", "« ", texte)
    return re.sub(r"\s+", " ", texte).strip()


def lignes_de_mots(les_mots: list[dict]) -> list[dict]:
    """Les mots groupés en lignes, dans l'ordre de lecture. Tesseract donne déjà les
    numéros de bloc/paragraphe/ligne du TSV : on s'en sert au lieu de recalculer une
    géométrie — mais on ORDONNE par y, parce que l'ordre du TSV n'est pas garanti."""
    groupes: dict[tuple, list[dict]] = {}
    for mot in les_mots:
        groupes.setdefault((mot["bloc"], mot["par"], mot["ligne"]), []).append(mot)
    lignes = []
    for mots_ligne in groupes.values():
        mots_ligne.sort(key=lambda m: m["left"])
        texte = _typographie(" ".join(m["texte"] for m in mots_ligne))
        if not texte:
            continue
        y0 = min(m["top"] for m in mots_ligne)
        y1 = max(m["top"] + m["height"] for m in mots_ligne)
        x0 = min(m["left"] for m in mots_ligne)
        confs = [m["conf"] for m in mots_ligne]
        lignes.append({
            "texte": texte, "x0": x0, "y0": y0, "y1": y1,
            "hauteur": y1 - y0, "conf": round(sum(confs) / len(confs), 1),
            "confs": confs,
        })
    return sorted(lignes, key=lambda l: (l["y0"], l["x0"]))


def _recoller(texte: str, suivant: str) -> str:
    """Une césure de fin de ligne se recolle ; une espace avant le tiret reste (même règle
    que le parseur PDF, pour que les deux lectures se comparent mot à mot)."""
    if texte.endswith("-") and suivant[:1].islower():
        return texte[:-1] + suivant
    return texte + " " + suivant


def blocs_de_page(lignes: list[dict], numero: int = 1,
                  langue: str = "fra") -> list[dict]:
    """Les blocs d'une page OCR : notes à part, titres par la hauteur, le reste en
    paragraphes. La provenance porte la page, le y et la CONFIANCE moyenne du bloc."""
    if not lignes:
        return []
    corps = statistics.median(l["hauteur"] for l in lignes)
    blocs: list[dict] = []
    paragraphe: list[dict] = []

    def fin_paragraphe() -> None:
        if not paragraphe:
            return
        texte = paragraphe[0]["texte"]
        confs = list(paragraphe[0]["confs"])
        for ligne in paragraphe[1:]:
            texte = _recoller(texte, ligne["texte"])
            confs += ligne["confs"]
        blocs.append({
            "type": "paragraphe", "texte": re.sub(r"\s+", " ", texte).strip(),
            "prov": {"page": numero, "y": round(paragraphe[0]["y0"], 1),
                     "confiance": round(sum(confs) / len(confs), 1),
                     "moteur": "tesseract", "langue": langue},
        })
        paragraphe.clear()

    for ligne in lignes:
        petit = ligne["hauteur"] < corps * 0.85
        grand = ligne["hauteur"] > corps * 1.12
        court = len(ligne["texte"]) < 90
        if petit:
            fin_paragraphe()
            blocs.append({
                "type": "note", "texte": ligne["texte"],
                "prov": {"page": numero, "y": round(ligne["y0"], 1),
                         "confiance": ligne["conf"], "moteur": "tesseract", "langue": langue},
            })
            continue
        if grand or (court and graphe_document_pdf.TYPES_LIGNES.match(ligne["texte"])):
            fin_paragraphe()
            premier = not any(b["type"] in ("titre", "section") for b in blocs)
            blocs.append({
                "type": "titre" if premier and grand else "section",
                "texte": ligne["texte"],
                "prov": {"page": numero, "y": round(ligne["y0"], 1),
                         "confiance": ligne["conf"], "moteur": "tesseract", "langue": langue},
            })
            continue
        if paragraphe:
            ecart = ligne["y0"] - paragraphe[-1]["y1"]
            retrait = abs(ligne["x0"] - paragraphe[-1]["x0"])
            if ecart > corps * 0.9 or retrait > corps * 1.5:
                fin_paragraphe()
        paragraphe.append(ligne)
    fin_paragraphe()
    return blocs


def analyse(image: pathlib.Path, langue: str = "fra", psm: int = 3) -> list[dict]:
    """Une image, des blocs — exactement la forme que rend `graphe_document_pdf.analyse`."""
    return blocs_de_page(lignes_de_mots(mots(image, langue, psm)), 1, langue)


def _source(image: pathlib.Path, langue: str) -> dict:
    octets = image.read_bytes()
    return {"chemin": image.as_posix(), "sha256": graphe_document.sha256(octets),
            "octets": len(octets), "format": image.suffix.lstrip(".").lower(),
            "langue": langue}


def manifeste(image: pathlib.Path, langue: str = "fra", psm: int = 3) -> dict:
    """Le manifeste d'une page lue en OCR : mêmes régions, mêmes offsets, même partition."""
    blocs = analyse(image, langue, psm)
    if not blocs:
        raise SystemExit(f"aucun bloc OCR : {image}")
    return graphe_document.manifeste_de_blocs(
        blocs, _source(image, langue),
        {"outil": "graphe_document_ocr.py", "version": VERSION,
         "moteur": "tesseract", "version_moteur": version(), "langue": langue},
    )


def manifeste_sans_ocr(image: pathlib.Path, langue: str = "fra") -> dict:
    """Le CONTRÔLE NÉGATIF : le même document, mais aucune lecture. Un manifeste vide ne
    peut pas répondre — c'est ce que la porte doit constater, pas supposer."""
    return {
        "version": graphe_document.VERSION,
        "source": _source(image, langue),
        "extraction": {"outil": "graphe_document_ocr.py", "version": VERSION,
                       "moteur": "tesseract", "langue": langue, "sans_ocr": True},
        "flux": {"octets": 0, "sha256": graphe_document.sha256(b"")},
        "regions": [],
        "stats": {"regions": 0, "types": {}},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("image", nargs="?", type=pathlib.Path)
    ap.add_argument("--langue", default="fra")
    ap.add_argument("--psm", type=int, default=3)
    ap.add_argument("--json", action="store_true", help="le manifeste, en JSON")
    ap.add_argument("--confiance", action="store_true", help="la confiance moyenne par bloc")
    ap.add_argument("--sans-ocr", action="store_true", help="le contrôle négatif : un manifeste vide")
    ap.add_argument("--version", action="store_true")
    args = ap.parse_args()
    if args.version:
        print(version())
        return 0
    if not args.image:
        ap.error("une image est requise (ou --version)")
    if args.sans_ocr:
        m = manifeste_sans_ocr(args.image, args.langue)
    else:
        m = manifeste(args.image, args.langue, args.psm)
    if args.json:
        print(json.dumps(m, ensure_ascii=False, indent=1))
        return 0
    if args.confiance:
        for region in m["regions"]:
            if region["type"] != "blanc":
                prov = region["prov"]
                print(f"{prov.get('confiance', 0):6.1f}  {region['type']:<12} "
                      f"{region['texte'][:90]}")
        return 0
    print(f"{len(m['regions'])} régions · {m['stats']['types']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
