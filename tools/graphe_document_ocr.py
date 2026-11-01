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

import numpy as np
import statistics
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import graphe_document  # noqa: E402  (le manifeste commun)
import graphe_document_pdf  # noqa: E402  (le vocabulaire des lignes de titre)

RACINE = pathlib.Path(__file__).resolve().parent.parent
VERSION = 1
# Version de la CONSTRUCTION du manifeste (lignes, blocs, colonnes) : la changer invalide les
# caches de mesure — sinon une amélioration de l'ordre de lecture n'est jamais mesurée.
VERSION_MANIFESTE = 6
# Version de la seule RÉCUPÉRATION (exposants) : la changer invalide les caches de mesure.
RECUPERATION_VERSION = 2
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


RE_EXPOSANT = re.compile(r"^[!?|Il1'°.,;:*+=]+$")


def _ocr_boite(image: pathlib.Path, boite: tuple[int, int, int, int], langue: str,
               marge: int = 5, hauteur: int = 96, psm: int = 10) -> list[tuple[str, float]]:
    """OCRise UNE petite boîte, agrandie, avec une liste blanche de chiffres. C'est la
    deuxième chance d'un appel de note : le premier passage l'a lu « ! » ou « !? »."""
    from PIL import Image, ImageFilter
    x0, y0, x1, y1 = boite
    with Image.open(image) as im:
        g = im.convert("L").crop((max(x0 - marge, 0), max(y0 - marge, 0),
                                  x1 + marge, y1 + marge))
    facteur = max(hauteur / max(g.height, 1), 3.0)
    g = g.resize((max(int(g.width * facteur), 1), max(int(g.height * facteur), 1)),
                 Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.4))
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        chemin = pathlib.Path(tmp.name)
    try:
        g.save(chemin)
        sortie = subprocess.run(
            [str(BIN), str(chemin), "stdout", "-l", langue, "--psm", str(psm),
             "-c", "tessedit_char_whitelist=0123456789", "-c", "tessedit_create_tsv=1"],
            env=_env(), capture_output=True, text=True)
    finally:
        chemin.unlink(missing_ok=True)
    resultats = []
    for ligne in sortie.stdout.splitlines()[1:]:
        champs = ligne.split("\t")
        if len(champs) >= 12 and champs[0] == "5" and champs[11].strip():
            try:
                resultats.append((champs[11].strip(), float(champs[10])))
            except ValueError:
                pass
    return resultats


def recuperer_exposants(image: pathlib.Path, les_mots: list[dict],
                        langue: str) -> tuple[list[dict], int]:
    """Rend les appels de note en exposant que tesseract a lus comme de la ponctuation.

    La règle est TYPOGRAPHIQUE, pas devinée : un mot **petit** (hauteur < 80 % de la ligne)
    et **fait de ponctuation** (`!`, `!!`, `!?`, `!l`) est un exposant raté. On recadre sa
    boîte, on l'agrandit ×4 et on refait l'OCR avec une liste blanche de chiffres ; on ne
    remplace que si le résultat est un nombre court, crédible (confiance ≥ 30)."""
    par_ligne: dict[tuple, list[dict]] = {}
    for mot in les_mots:
        par_ligne.setdefault((mot["bloc"], mot["par"], mot["ligne"]), []).append(mot)
    recuperes = 0
    for mots_ligne in par_ligne.values():
        if len(mots_ligne) < 2:
            continue
        hauteurs = sorted(m["height"] for m in mots_ligne)
        median = hauteurs[len(hauteurs) // 2] or 1
        for mot in mots_ligne:
            if mot["height"] >= median * 0.80:
                continue
            if not RE_EXPOSANT.match(mot["texte"] or "") or len(mot["texte"]) > 3:
                continue
            boite = (mot["left"], mot["top"],
                     mot["left"] + mot["width"], mot["top"] + mot["height"])
            candidats = [c for c in _ocr_boite(image, boite, langue)
                         if 1 <= len(c[0]) <= 2 and c[0].isdigit() and c[1] >= 30]
            if not candidats:
                continue
            texte, conf = max(candidats, key=lambda c: (c[1], len(c[0])))
            mot["texte"] = texte
            mot["exposant_recupere"] = round(conf, 1)
            recuperes += 1
    return les_mots, recuperes


def bandes_vides(boites: list[tuple[float, float, float, float]],
                 largeur: float, hauteur: float | None = None) -> list[tuple[float, float]]:
    """TOUTES les gouttières : les bandes verticales sans encre, entre 15 % et 85 % de la largeur,
    larges de 2,5 % à 15 % de la page. Une page à deux colonnes en a une ; une page à trois
    colonnes en a deux, et la lecture doit alors découper en trois — sinon la moitié droite
    entrelace deux colonnes (mesuré : 52,5 % de WER à trois colonnes contre 0,5 % à deux).

    L'occupation est une **couverture verticale** (somme des hauteurs de mots / hauteur de page) :
    un en-tête centré qui traverse une gouttière ne pèse que 2 % et ne la bloque plus. Chaque
    groupe de mots entre deux gouttières doit peser au moins 12 % des mots, sinon la bande est
    un faux vide (espace de justification, titre centré)."""
    if len(boites) < 8 or largeur < 100:
        return []
    occupation = np.zeros(int(largeur) + 2, dtype=np.float64)
    for x0, x1, y0, y1 in boites:
        occupation[max(int(x0), 0):max(int(x1), 0)] += float(y1 - y0)
    if hauteur:
        occupation /= max(float(hauteur), 1.0)
    faible = occupation < 0.10
    deb, fin = int(largeur * 0.15), int(largeur * 0.85)
    largeur_min = max(largeur * 0.025, 12)
    largeur_max = largeur * 0.15
    bandes = []
    i = deb
    while i < fin:
        if faible[i]:
            j = i
            while j < fin and faible[j]:
                j += 1
            if largeur_min <= (j - i) <= largeur_max:
                bandes.append((float(i), float(j)))
            i = j
        else:
            i += 1
    if not bandes:
        return []
    # chaque groupe entre deux gouttières doit exister : au moins 12 % des mots
    bornes = [0.0] + [(a + b) / 2 for a, b in bandes] + [float(largeur)]
    for k in range(len(bornes) - 1):
        gauche, droite = bornes[k], bornes[k + 1]
        poids = sum(1 for x0, x1, _, _ in boites if gauche <= (x0 + x1) / 2 < droite)
        if poids < len(boites) * 0.12:
            return []
    return bandes


def bande_vide_boites(boites: list[tuple[float, float, float, float]],
                      largeur: float, hauteur: float | None = None) -> tuple[float, float] | None:
    """La gouttière la plus large (compatibilité) ; voir `bandes_vides` pour toutes."""
    bandes = bandes_vides(boites, largeur, hauteur)
    return max(bandes, key=lambda b: b[1] - b[0]) if bandes else None


def bande_vide(lignes: list[dict], largeur: float,
               hauteur: float | None = None) -> tuple[float, float] | None:
    return bande_vide_boites([(l["x0"], l["x1"], l["y0"], l["y1"]) for l in lignes],
                             largeur, hauteur)


def ordre_de_lecture(lignes: list[dict], largeur: float) -> list[dict]:
    """Colonne gauche entière, puis colonne droite. Sans gouttière, l'ordre est (y, x)."""
    gouttiere = bande_vide(lignes, largeur)
    if gouttiere is None:
        return sorted(lignes, key=lambda l: (l["y0"], l["x0"]))
    centre = sum(gouttiere) / 2
    gauche = sorted((l for l in lignes if (l["x0"] + l["x1"]) / 2 < centre),
                    key=lambda l: (l["y0"], l["x0"]))
    droite = sorted((l for l in lignes if (l["x0"] + l["x1"]) / 2 >= centre),
                    key=lambda l: (l["y0"], l["x0"]))
    return gauche + droite


def _typographie(texte: str) -> str:
    """Les blancs que l'OCR ajoute autour de la ponctuation française. On ne touche à aucun
    mot : seule l'espace fautive part, sinon le WER mesurerait la typographie."""
    texte = re.sub(r"\s+([,;:.!?»%])", r"\1", texte)
    texte = re.sub(r"«\s+", "« ", texte)
    return re.sub(r"\s+", " ", texte).strip()


def _lignes_depuis_mots(les_mots: list[dict]) -> list[dict]:
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
        x1 = max(m["left"] + m["width"] for m in mots_ligne)
        confs = [m["conf"] for m in mots_ligne]
        lignes.append({
            "texte": texte, "x0": x0, "x1": x1, "y0": y0, "y1": y1,
            "hauteur": y1 - y0, "conf": round(sum(confs) / len(confs), 1),
            "confs": confs,
        })
    return sorted(lignes, key=lambda l: (l["y0"], l["x0"]))


def lignes_de_mots(les_mots: list[dict], colonnes: bool = False) -> list[dict]:
    """Les mots groupés en lignes, dans l'ordre de lecture. Tesseract donne déjà les
    numéros de bloc/paragraphe/ligne du TSV : on s'en sert au lieu de recalculer une
    géométrie — mais on ORDONNE par y, parce que l'ordre du TSV n'est pas garanti.

    En mode `colonnes`, la gouttière se cherche sur les MOTS, pas sur les lignes : sur un
    lexique à deux colonnes, une ligne TSV peut contenir la gauche et la droite, et la
    gouttière disparaît des lignes. On sépare alors les mots, on reconstruit les lignes de
    chaque côté, et on lit la gauche entière puis la droite."""
    if not les_mots:
        return []
    if colonnes:
        largeur = max(m["left"] + m["width"] for m in les_mots)
        hauteur = max(m["top"] + m["height"] for m in les_mots)
        bandes = bandes_vides(
            [(m["left"], m["left"] + m["width"], m["top"], m["top"] + m["height"])
             for m in les_mots], largeur, hauteur)
        if bandes:
            bornes = [0.0] + [(a + b) / 2 for a, b in bandes] + [largeur + 1]
            sortie = []
            for k in range(len(bornes) - 1):
                groupe = [m for m in les_mots
                          if bornes[k] <= (m["left"] + m["width"] / 2) < bornes[k + 1]]
                sortie.extend(_lignes_depuis_mots(groupe))
            return sortie
    return _lignes_depuis_mots(les_mots)


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
    bas_page = max(l["y1"] for l in lignes)
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
        # Une ligne « petite » n'est une NOTE que dans le bas de la page. Au milieu du corps,
        # c'est une ligne de continuation sans hampe ni jambage (mesuré : « social et dans les
        # domaines connexes » était typée note, coupait le paragraphe, et la question « point 13 »
        # perdait sa réponse sur TOUTES les familles, page propre comprise).
        petit = ligne["hauteur"] < corps * 0.85 and ligne["y0"] > bas_page * 0.62
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


def analyse(image: pathlib.Path, langue: str = "fra", psm: int = 3,
            exposants: bool = False, colonnes: bool = False) -> list[dict]:
    """Une image, des blocs — exactement la forme que rend `graphe_document_pdf.analyse`."""
    les_mots = mots(image, langue, psm)
    if exposants:
        les_mots, _ = recuperer_exposants(image, les_mots, langue)
    return blocs_de_page(lignes_de_mots(les_mots, colonnes), 1, langue)


def _source(image: pathlib.Path, langue: str) -> dict:
    octets = image.read_bytes()
    return {"chemin": image.as_posix(), "sha256": graphe_document.sha256(octets),
            "octets": len(octets), "format": image.suffix.lstrip(".").lower(),
            "langue": langue}


def manifeste(image: pathlib.Path, langue: str = "fra", psm: int = 3,
              exposants: bool = False, colonnes: bool = False) -> dict:
    """Le manifeste d'une page lue en OCR : mêmes régions, mêmes offsets, même partition."""
    les_mots = mots(image, langue, psm)
    recuperes = 0
    if exposants:
        les_mots, recuperes = recuperer_exposants(image, les_mots, langue)
    blocs = blocs_de_page(lignes_de_mots(les_mots, colonnes), 1, langue)
    if not blocs:
        raise SystemExit(f"aucun bloc OCR : {image}")
    extraction = {"outil": "graphe_document_ocr.py", "version": VERSION,
                  "moteur": "tesseract", "version_moteur": version(), "langue": langue}
    if exposants:
        extraction["exposants_recuperes"] = recuperes
    return graphe_document.manifeste_de_blocs(blocs, _source(image, langue), extraction)


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
    ap.add_argument("--exposants", action="store_true",
                    help="récupère les appels de note en exposant (passe chiffres ciblée)")
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
        m = manifeste(args.image, args.langue, args.psm, exposants=args.exposants)
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
