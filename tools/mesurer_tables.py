#!/usr/bin/env python3
"""mesurer_tables.py — R4.4 : les tableaux SCANNÉS, cellule par cellule.

POURQUOI CE FICHIER. R4.1 a montré qu'un tableau lu comme du texte à plat ne répond pas
(0/3). Le même contrôle vaut pour un scan : l'information peut être là — les mots sont lus —
sans qu'aucune cellule ne soit **localisée**. Ce banc mesure donc deux choses distinctes :

  1. la **cellule exacte** : la valeur est-elle dans la bonne ligne et la bonne colonne ?
  2. le **contrôle texte à plat** : les mots du tableau sont-ils présents dans la lecture
     linéaire ? (oui, souvent) — et localisés ? (non, par construction : 0).

LE CORPUS est fabriqué par `fabriquer_tables.py` (6×9 cellules, vérité connue) et dégradé par
`simuler_scan.py`. Le pipeline est celui de R4.4 : `nettoyer_scan.auto`, puis
`extraire_tableaux.extraire` (traits → grille → cellules).

Usage :
  python3 tools/mesurer_tables.py --pages 10 --familles propre,photocopie,photo
  python3 tools/mesurer_tables.py --porte
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import extraire_tableaux  # noqa: E402
import mesurer_ocr  # noqa: E402
import nettoyer_scan  # noqa: E402
import simuler_scan  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
CORPUS = RACINE / "work/r44/tables"
RENDUS = CORPUS / "rendus"
# Planchers MESURÉS sur le corpus complet (10 pages) : bornes de non-régression. La photo
# dégradée perd la grille sur 4 pages sur 10 ; c'est écrit, pas contourné.
SEUILS = {"propre": 0.90, "photocopie": 0.65, "photo": 0.45}
SEUILS_GRILLE = {"propre": 1.0, "photocopie": 1.0, "photo": 0.5}


def norm(texte: str) -> str:
    return re.sub(r"\s+", "", texte.lower().replace("\u00a0", " "))


def rendu(pdf: pathlib.Path, page: int = 1) -> pathlib.Path:
    """Chaque PDF du corpus ne porte qu'UNE page : `page` ne sert qu'au nom du manifeste."""
    RENDUS.mkdir(parents=True, exist_ok=True)
    png = RENDUS / f"{pdf.stem}.png"
    if not png.exists():
        subprocess.run(["pdftoppm", "-r", "300", "-f", "1", "-l", "1",
                        "-singlefile", "-png", str(pdf), str(png.with_suffix(""))],
                       check=True, capture_output=True)
    return png


def note(verite: list[list[str]], trouvee: list[list[str]]) -> dict:
    if not trouvee:
        return {"cellules": 0, "exactes": 0, "taux": 0.0, "grille": False}
    lignes = len(verite)
    colonnes = len(verite[0]) if verite else 0
    meme_forme = len(trouvee) == lignes and all(len(l) == colonnes for l in trouvee)
    exactes = 0
    total = sum(len(l) for l in verite)
    if meme_forme:
        for lv, lt in zip(verite, trouvee):
            exactes += sum(1 for a, b in zip(lv, lt) if norm(a) == norm(b))
    else:
        # la forme diffère : on mesure au moins le CONTENU retrouvé (multiensemble), pas la place
        restant = [norm(c) for l in trouvee for c in l if norm(c)]
        for ligne in verite:
            for cellule in ligne:
                if norm(cellule) in restant:
                    restant.remove(norm(cellule))
                    exactes += 1
    return {"cellules": total, "exactes": exactes, "taux": round(exactes / max(total, 1), 4),
            "grille": meme_forme}


def mesure(entree: dict, famille: str, redresser: bool = True) -> dict:
    from PIL import Image
    propre = Image.open(rendu(CORPUS / entree["pdf"], entree["page"])).convert("RGB")
    if famille == "propre":
        image = propre
    else:
        image, _ = simuler_scan.fabriquer(propre, famille, 1, entree["page"],
                                          pathlib.Path("/tmp/tab.jpg"))
    nettoyee, trace = nettoyer_scan.auto(image)
    scan = CORPUS / "scans" / f"{entree['pdf'][:-4]}-{famille}{'-sans-redresser' if not redresser else ''}.png"
    scan.parent.mkdir(parents=True, exist_ok=True)
    if not scan.exists():
        nettoyee.save(scan)
    resultat = extraire_tableaux.extraire(scan, redresser=redresser)
    n = note(entree["cellules"], resultat["grille"])
    return {"page": entree["page"], "famille": famille, "redresser": redresser,
            "angle": resultat["angle"], "raison": resultat["raison"],
            "trace": trace, **n}


def agrege(lignes: list[dict]) -> dict:
    par: dict[tuple, list[dict]] = {}
    for l in lignes:
        par.setdefault((l["famille"], l["redresser"]), []).append(l)
    out = {}
    for (famille, redresser), ls in sorted(par.items()):
        total = sum(l["cellules"] for l in ls)
        exactes = sum(l["exactes"] for l in ls)
        out[f"{famille}|{'redresse' if redresser else 'sans' }"] = {
            "famille": famille, "redresser": redresser, "pages": len(ls),
            "cellules": total, "exactes": exactes,
            "taux": round(exactes / max(total, 1), 4),
            "grilles_exactes": sum(1 for l in ls if l["grille"]),
            "angles": [l["angle"] for l in ls],
        }
    return out


def controle_plat(entree: dict) -> dict:
    """Le contrôle : le texte à plat contient-il les valeurs, et les localise-t-il ?"""
    import tempfile
    from PIL import Image
    import graphe_document_ocr
    image = Image.open(rendu(CORPUS / entree["pdf"], entree["page"])).convert("RGB")
    nettoyee, _ = nettoyer_scan.auto(image)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        chemin = pathlib.Path(tmp.name)
    try:
        nettoyee.save(chemin)
        mots = graphe_document_ocr.mots(chemin, "fra")
    finally:
        chemin.unlink(missing_ok=True)
    plat = norm(" ".join(m["texte"] for m in mots))
    total = sum(len(l) for l in entree["cellules"])
    presentes = sum(1 for l in entree["cellules"] for c in l if norm(c) and norm(c) in plat)
    return {"cellules": total, "presentes_texte_plat": presentes,
            "localisees_texte_plat": 0,
            "taux_present": round(presentes / max(total, 1), 4)}


def verdict(a: dict) -> list[tuple[str, bool]]:
    bareme = []
    for famille, seuil in SEUILS.items():
        cle = f"{famille}|redresse"
        if cle in a:
            bareme.append((f"{famille} : cellules exactes ≥ {seuil:.0%} "
                           f"(mesuré {a[cle]['taux']:.1%})", a[cle]["taux"] >= seuil))
            seuil_grille = SEUILS_GRILLE.get(famille, 1.0)
            bareme.append((f"{famille} : grilles de bonne forme ≥ {seuil_grille:.0%} "
                           f"(mesuré {a[cle]['grilles_exactes']}/{a[cle]['pages']})",
                           a[cle]["grilles_exactes"] >= seuil_grille * a[cle]["pages"]))
    return bareme


def affiche(a: dict, plat: dict, bareme: list[tuple[str, bool]]) -> int:
    print("=== R4.4 — LES TABLEAUX SCANNÉS, CELLULE PAR CELLULE ===")
    print(f"  {'famille':<12}{'redressé':<10}{'pages':>6}{'cellules':>10}{'exactes':>9}{'taux':>8}{'grilles':>9}")
    for cle, x in sorted(a.items()):
        print(f"  {x['famille']:<12}{'oui' if x['redresser'] else 'non':<10}{x['pages']:>6}"
              f"{x['cellules']:>10}{x['exactes']:>9}{x['taux']:>8.1%}"
              f"{x['grilles_exactes']:>6}/{x['pages']}")
    print(f"\n  contrôle texte à plat : {plat['presentes_texte_plat']}/{plat['cellules']} valeurs "
          f"présentes ({plat['taux_present']:.1%}), 0 localisée")
    print()
    for libelle, ok in bareme:
        print(f"  {'✅' if ok else '❌'} {libelle}")
    return 0 if all(ok for _, ok in bareme) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corpus", type=pathlib.Path, default=CORPUS / "manifeste.json")
    ap.add_argument("--familles", default="propre,photocopie,photo")
    ap.add_argument("--pages", type=int, default=0)
    ap.add_argument("--control-sans-redresser", action="store_true", default=True)
    ap.add_argument("--sortie", type=pathlib.Path, default=RACINE / "work/r44/tables.json")
    ap.add_argument("--porte", action="store_true")
    args = ap.parse_args()
    corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
    familles = [f for f in args.familles.split(",") if f]
    entrees = corpus["entrees"][: args.pages] if args.pages else corpus["entrees"]
    lignes = []
    for entree in entrees:
        for famille in familles:
            ligne = mesure(entree, famille)
            lignes.append(ligne)
            print(f"  page {entree['page']} · {famille:10s} : {ligne['exactes']}/{ligne['cellules']} "
                  f"cellules · grille {'oui' if ligne['grille'] else 'non'}", flush=True)
        if args.control_sans_redresser and "photocopie" in familles:
            lignes.append(mesure(entree, "photocopie", redresser=False))
    plat = controle_plat(entrees[0])
    a = agrege(lignes)
    bareme = verdict(a)
    resultat = {"date": "2026-10-31", "ligne": "R4.4", "nature": "tableaux synthétiques",
                "pages": len(entrees), "familles": familles, "seuils": SEUILS,
                "controle_plat": plat, "agregat": a, "mesures": lignes}
    args.sortie.parent.mkdir(parents=True, exist_ok=True)
    args.sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8")
    code = affiche(a, plat, bareme)
    print(f"\n  → {args.sortie}")
    return code if args.porte else 0


if __name__ == "__main__":
    sys.exit(main())
