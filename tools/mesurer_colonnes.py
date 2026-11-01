#!/usr/bin/env python3
"""mesurer_colonnes.py — R4.4 : la mise en page à deux colonnes, mesurée et corrigée.

POURQUOI CE FICHIER. Sur une page à deux colonnes, un lecteur naïf entrelace la gauche et la
droite : le WER mot à mot le voit (l'ordre compte), mais un sac de mots ne le verrait pas — et
c'est pourquoi la mesure est une distance d'édition sur les jetons, pas un rappel. Le corpus
ONU est mono-colonne ; `fabriquer_colonnes.py` fabrique donc des pages à deux colonnes dont la
vérité terrain est connue, et une version mono-colonne de contrôle.

CE QUI EST MESURÉ :
  - la page **deux colonnes** sans détection de gouttière (le contrôle qui doit ÉCHOUER) ;
  - la même avec `graphe_document_ocr` en mode `colonnes` (gouttière verticale, puis lecture
    colonne gauche entière, colonne droite entière) ;
  - la page **mono-colonne** dans les deux modes : la détection ne doit RIEN changer.

Usage :
  python3 tools/mesurer_colonnes.py --sortie work/r44/colonnes.json --familles propre,photocopie,photo
  python3 tools/mesurer_colonnes.py --porte
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
import simuler_scan  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
CORPUS = RACINE / "work/r44/colonnes"
RENDUS = CORPUS / "rendus"
SEUILS = {
    # sur deux colonnes, la détection doit ramener le WER sous ces seuils
    "deux": {"propre": 0.03, "photocopie": 0.06, "photo": 0.20},
    # la détection ne doit pas dégrader la page mono de plus de 0,5 point
    "mono_ecart": 0.005,
    # et le contrôle sans détection doit rester CATASTROPHIQUE (au moins 50 points)
    "controle_deux": 0.50,
}


def rendu(pdf: pathlib.Path) -> pathlib.Path:
    RENDUS.mkdir(parents=True, exist_ok=True)
    png = RENDUS / f"{pdf.stem}.png"
    if not png.exists():
        subprocess.run(["pdftoppm", "-r", "300", "-singlefile", "-png",
                        str(pdf), str(png.with_suffix(""))], check=True, capture_output=True)
    return png


def mesure(entree: dict, version: str, verite: str, familles: list[str]) -> list[dict]:
    from PIL import Image
    lignes = []
    image_propre = Image.open(rendu(CORPUS / entree[version])).convert("RGB")
    for famille in familles:
        if famille == "propre":
            image = image_propre
        else:
            image, _ = simuler_scan.fabriquer(image_propre, famille, 1, entree["page"],
                                              pathlib.Path("/tmp/col.jpg"))
        scan = CORPUS / "scans" / f"{entree[version][:-4]}-{famille}.png"
        scan.parent.mkdir(parents=True, exist_ok=True)
        if not scan.exists():
            image.save(scan)
        for colonnes in (False, True):
            manifeste = mesurer_scans.manifeste_ocr(scan, "fra", colonnes=colonnes)
            hypothese = mesurer_ocr.jetons(mesurer_ocr.texte_du_manifeste(manifeste))
            reference = mesurer_ocr.jetons(verite)
            distance = mesurer_ocr.wer(reference, hypothese)
            lignes.append({
                "page": entree["page"], "version": version, "famille": famille,
                "colonnes": colonnes, "mots": len(reference),
                "distance": distance, "wer": round(distance / max(len(reference), 1), 4),
            })
    return lignes


def agrege(lignes: list[dict]) -> dict:
    out: dict[str, dict] = {}
    for l in lignes:
        cle = f"{l['version']}|{l['famille']}|{'colonnes' if l['colonnes'] else 'brut'}"
        a = out.setdefault(cle, {"version": l["version"], "famille": l["famille"],
                                 "colonnes": l["colonnes"], "mots": 0, "distance": 0,
                                 "pages": 0})
        a["mots"] += l["mots"]
        a["distance"] += l["distance"]
        a["pages"] += 1
    for a in out.values():
        a["wer"] = round(a["distance"] / max(a["mots"], 1), 4)
    return out


def verdict(a: dict) -> list[tuple[str, bool]]:
    bareme = []
    for famille, seuil in SEUILS["deux"].items():
        cle = f"deux|{famille}|colonnes"
        if cle in a:
            bareme.append((f"deux colonnes · {famille} : WER ≤ {seuil:.0%} (mesuré {a[cle]['wer']:.1%})",
                           a[cle]["wer"] <= seuil))
    for famille in {x["famille"] for x in a.values()}:
        brut, col = f"deux|{famille}|brut", f"deux|{famille}|colonnes"
        if brut in a and col in a:
            bareme.append((f"contrôle sans gouttière · {famille} : ≥ 50 % (mesuré {a[brut]['wer']:.1%})",
                           a[brut]["wer"] >= SEUILS["controle_deux"]))
        mono_b, mono_c = f"mono|{famille}|brut", f"mono|{famille}|colonnes"
        if mono_b in a and mono_c in a:
            ecart = abs(a[mono_c]["wer"] - a[mono_b]["wer"])
            bareme.append((f"mono-colonne · {famille} : écart ≤ 0,5 pt (mesuré {ecart:.2%})",
                           ecart <= SEUILS["mono_ecart"]))
    return bareme


def affiche(a: dict, bareme: list[tuple[str, bool]]) -> int:
    print("=== R4.4 — LA MISE EN PAGE À DEUX COLONNES ===")
    print(f"  {'version':<6}{'famille':<12}{'lecture':<10}{'WER':>8}{'pages':>7}")
    for cle, x in sorted(a.items()):
        print(f"  {x['version']:<6}{x['famille']:<12}"
              f"{'colonnes' if x['colonnes'] else 'brut':<10}{x['wer']:>8.2%}"
              f"{x['pages']:>7}")
    print()
    for libelle, ok in bareme:
        print(f"  {'✅' if ok else '❌'} {libelle}")
    return 0 if all(ok for _, ok in bareme) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corpus", type=pathlib.Path, default=CORPUS / "manifeste.json")
    ap.add_argument("--familles", default="propre,photocopie,photo")
    ap.add_argument("--pages", type=int, default=0)
    ap.add_argument("--sortie", type=pathlib.Path, default=RACINE / "work/r44/colonnes.json")
    ap.add_argument("--porte", action="store_true")
    args = ap.parse_args()
    corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
    familles = [f for f in args.familles.split(",") if f]
    entrees = corpus["entrees"][: args.pages] if args.pages else corpus["entrees"]
    lignes = []
    for entree in entrees:
        for version, verite in (("mono", entree["verite_mono"]),
                                ("deux", entree["verite_deux"])):
            lignes += mesure(entree, version, verite, familles)
            print(f"  page {entree['page']} · {version} : mesuré", flush=True)
    a = agrege(lignes)
    bareme = verdict(a)
    resultat = {"date": "2026-10-31", "ligne": "R4.4", "nature": "colonnes synthétiques",
                "source": "docs/theorie/vision.md", "familles": familles,
                "pages": len(entrees), "seuils": SEUILS, "agregat": a, "mesures": lignes}
    args.sortie.parent.mkdir(parents=True, exist_ok=True)
    args.sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8")
    code = affiche(a, bareme)
    print(f"\n  → {args.sortie}")
    return code if args.porte else 0


if __name__ == "__main__":
    sys.exit(main())
