#!/usr/bin/env python3
"""mesurer_ocr.py — R4.4 : dix pages lues en OCR, leur WER, leur parité, leurs contrôles.

POURQUOI CET OUTIL. La ligne R4.4 était bloquée, pas mesurée : « aucun OCR installé ».
Une fois l'OCR là (`tools/installer_ocr.sh`), la question n'est plus « peut-on lire une
image ? » mais « la page lue en OCR donne-t-elle la MÊME réponse que la page lue en texte
natif ? ». C'est la porte de R4.4, et elle se mesure en trois temps :

  1. le WER mot à mot, contre le texte natif de la même page — un chiffre, avec son
     rappel et sa précision de vocabulaire ;
  2. la PARITÉ : les questions du banc R0.3 (`bench-complet.json`) dont le gold tombe sur
     la page, lues par LE MÊME lecteur extractif sur les deux manifestes (natif, OCR) ;
  3. les CONTRÔLES : sans OCR aucune réponse ne doit sortir ; une page dégradée (flou,
     JPEG, rotation) doit faire MONTER le WER et BAISSER la parité — sinon le chiffre ne
     mesure rien.

CE QUE L'OUTIL N'EST PAS. Ce n'est pas un banc de layout : les pages sont des rendus
propres du PDF, pas des photocopies. Le contrôle « page bruitée » simule une dégradation,
il ne remplace pas un corpus de scans réels — c'est écrit dans la fiche.

Usage :
  python3 tools/mesurer_ocr.py                       # 10 pages, écrit reports/r44-ocr-pilote.json
  python3 tools/mesurer_ocr.py --porte               # les seuils de la porte R4.4, code 0/1
  python3 tools/mesurer_ocr.py --pages 2 --sortie /tmp/r44.json   # fumée, sans écrire une fiche
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import re
import subprocess
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import graphe_document  # noqa: E402
import graphe_document_ocr  # noqa: E402
import graphe_document_pdf  # noqa: E402
import lecteur_controleur as lc  # noqa: E402
from banc_lecture import f1 as f1_mots, normalise  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
BENCH = RACINE / "tools/tests/documents/bench-complet.json"
SORTIE = RACINE / "reports/r44-ocr-pilote.json"
CACHE = RACINE / "work/ocr/pages"
RE_MOT = re.compile(r"[0-9a-zà-öø-ÿ]+")
LANGUE = {"-fr": "fra", "-en": "eng", "-es": "spa"}

# Les seuils de la porte. Ils sont écrits ici, pas dans la fiche : la porte doit pouvoir
# échouer sans lire un document.
SEUILS = {
    "pages": 10,
    "wer": 0.10,
    "rappel": 0.90,
    "parite_region": 0.90,
    "f1_median": 0.95,
    "exactitude_natif": 0.90,
    "sans_ocr": 0.0,
}


def jetons(texte: str) -> list[str]:
    return RE_MOT.findall(texte.lower())


def wer(reference: list[str], hypothese: list[str]) -> int:
    """La distance d'édition en MOTS (Levenshtein), pas en caractères : un mot faux compte
    un, pas quatre — et c'est le mot que les questions du banc manipulent."""
    if not reference:
        return len(hypothese)
    precedente = list(range(len(hypothese) + 1))
    for i, mot_ref in enumerate(reference, 1):
        courante = [i] + [0] * len(hypothese)
        for j, mot_hyp in enumerate(hypothese, 1):
            courante[j] = min(
                precedente[j] + 1, courante[j - 1] + 1,
                precedente[j - 1] + (mot_ref != mot_hyp))
        precedente = courante
    return precedente[-1]


def texte_du_manifeste(manifeste: dict) -> str:
    return " ".join(r["texte"] for r in manifeste["regions"] if r["type"] != "blanc")


def confiance_moyenne(manifeste: dict) -> float:
    """La confiance de l'OCR, pondérée par les mots : un bloc de dix mots pèse dix fois un
    bloc d'un mot. Sans cette pondération, une ligne de titre courte dominerait la page."""
    total, poids = 0.0, 0
    for region in manifeste["regions"]:
        conf = region["prov"].get("confiance")
        if region["type"] == "blanc" or conf is None:
            continue
        n = max(len(jetons(region["texte"])), 1)
        total += conf * n
        poids += n
    return round(total / poids, 1) if poids else 0.0


def langue_de(chemin: pathlib.Path) -> str:
    for suffixe, langue in LANGUE.items():
        if chemin.stem.endswith(suffixe):
            return langue
    raise SystemExit(f"langue inconnue pour {chemin} : la politique de langue doit être explicite")


def rendu(pdf: pathlib.Path, page: int, dpi: int) -> pathlib.Path:
    """La page en PNG, 300 dpi par défaut. Le cache rend l'outil rejouable : la mesure ne
    dépend pas d'un rendu refait à chaque passage."""
    CACHE.mkdir(parents=True, exist_ok=True)
    # La clé du cache porte l'empreinte du PDF : si le document change, la page rendue ne
    # peut pas rester l'ancienne — une mesure qui relit silencieusement un autre fichier est
    # exactement le défaut que ce dépôt traque.
    empreinte = graphe_document.sha256(pdf.read_bytes())[:8]
    png = CACHE / f"{pdf.stem}-{empreinte}-p{page}-{dpi}.png"
    if png.exists():
        return png
    subprocess.run(["pdftoppm", "-r", str(dpi), "-f", str(page), "-l", str(page),
                    "-singlefile", "-png", str(pdf), str(png.with_suffix(""))],
                   check=True, capture_output=True)
    if not png.exists():
        raise SystemExit(f"rendu absent après pdftoppm : {png}")
    return png


def degradee(png: pathlib.Path) -> pathlib.Path:
    """Le contrôle « page bruitée » : flou, JPEG de mauvaise qualité, rotation légère.
    C'est une dégradation SIMULÉE, nommée comme telle dans la fiche : elle prouve que la
    mesure est sensible, elle ne remplace pas des scans réels."""
    from PIL import Image, ImageFilter
    sortie = png.with_name(png.stem + "-degradee.png")
    if sortie.exists():
        return sortie
    with Image.open(png) as im:
        im = im.convert("RGB")
        # Une photo de téléphone, simulée : 0,35× la définition, flou, JPEG qualité 20,
        # 0,8° de travers — puis remise à l'échelle du rendu pour que l'OCR travaille dans
        # les mêmes conditions. Le réglage a été choisi POUR que le WER bouge (de 4,5 %
        # propre à 14,2 % dégradé sur A_RES_80_10-fr p2) : un contrôle qui ne bouge pas ne
        # contrôle rien.
        petit = im.resize((max(int(im.width * 0.35), 1), max(int(im.height * 0.35), 1)),
                          Image.LANCZOS)
        petit = petit.filter(ImageFilter.GaussianBlur(radius=1.0))
        petit = petit.rotate(0.8, resample=Image.BICUBIC, expand=False,
                             fillcolor=(255, 255, 255))
        temporaire = sortie.with_suffix(".jpg")
        petit.save(temporaire, "JPEG", quality=20)
    with Image.open(temporaire) as im:
        im.convert("RGB").resize(Image.open(png).size, Image.LANCZOS).save(sortie)
    temporaire.unlink(missing_ok=True)
    return sortie


def manifeste_natif(pdf: pathlib.Path, page: int, langue: str) -> dict:
    """Le manifeste de la MÊME page en texte natif, par le graphe R0.1 : les blocs sont
    filtrés par page, le reste de la construction est commun (offsets, partition)."""
    blocs = [b for b in graphe_document_pdf.analyse(pdf) if b["prov"].get("page") == page]
    if not blocs:
        raise SystemExit(f"page {page} vide côté natif : {pdf}")
    octets = pdf.read_bytes()
    return graphe_document.manifeste_de_blocs(
        blocs,
        {"chemin": f"{pdf.as_posix()}#page={page}",
         "sha256": graphe_document.sha256(octets), "octets": len(octets),
         "format": "pdf", "langue": langue, "page": page},
        {"outil": "graphe_document_pdf.py", "version": graphe_document.VERSION,
         "page": page},
    )


def lire(manifeste: dict, question: dict) -> dict | None:
    passages = lc.passages(manifeste)
    if not passages:
        return None
    scores = lc.Index(passages).scores(question["question"])
    return lc.repondre(passages, question, scores)


def trouve(reponse: dict | None, valeur: str) -> bool:
    return bool(reponse and normalise(valeur) in normalise(reponse["texte"]))


def texte_de_region(manifeste: dict, region_id: str | None) -> str:
    """Le texte du PASSAGE (bloc) d'où la réponse a été extraite. La parité de valeur de la
    spécification porte sur le passage choisi, pas sur la fenêtre de réponse : un chiffre lu
    dans le bloc mais coupé par la fenêtre ne doit pas compter comme une perte d'OCR."""
    if not region_id:
        return ""
    for r in manifeste.get("regions", []):
        if r.get("id") == region_id:
            return r.get("texte", "")
    return ""


def trouve_dans_passage(manifeste: dict, reponse: dict | None, valeur: str) -> bool:
    return bool(reponse and normalise(valeur) in normalise(
        texte_de_region(manifeste, reponse.get("region"))))


def pages_du_banc(limite: int) -> list[dict]:
    """Les pages qui portent les questions du banc R0.3 : une page par son PDF, son numéro,
    sa langue et SES questions. C'est le dispositif, pas un choix après coup."""
    bench = json.loads(BENCH.read_text(encoding="utf-8"))
    candidates: dict[tuple[pathlib.Path, int], list[dict]] = {}
    for document in bench["documents"]:
        if document["type"] != "juridique":
            continue
        pdf = pathlib.Path(document["source"])
        passages = lc.passages(graphe_document.manifeste(pdf, langue_de(pdf)))
        for question in document["questions"]:
            prefixe = question["passage"][:60]
            gold = next((p for p in passages if prefixe in p["texte"]), None)
            if gold is None:
                raise SystemExit(f"gold introuvable : {question['question']}")
            page = gold["prov"].get("page")
            if not isinstance(page, int):
                continue
            candidates.setdefault((pdf, page), []).append(question)
    # Diversité : d'abord la meilleure page de CHAQUE document, puis les pages suivantes
    # par nombre de questions. Une page sans question reste utile au WER, pas à la parité.
    classement = sorted(candidates.items(), key=lambda kv: (-len(kv[1]), kv[0][0].name, kv[0][1]))
    choisies: list[dict] = []
    vus: set[pathlib.Path] = set()
    for (pdf, page), questions in classement:
        if pdf in vus:
            continue
        choisies.append({"pdf": pdf, "page": page, "questions": questions})
        vus.add(pdf)
    for (pdf, page), questions in classement:
        if len(choisies) >= limite:
            break
        if any(c["pdf"] == pdf and c["page"] == page for c in choisies):
            continue
        choisies.append({"pdf": pdf, "page": page, "questions": questions})
    # Compléter jusqu'à `limite` avec des pages voisines (sans question) : le WER porte
    # alors sur dix pages, la parité sur celles qui portent des questions — dit tel quel.
    if len(choisies) < limite:
        for pdf in sorted(vus):
            nb = len(graphe_document_pdf.lignes_du_pdf(pdf))
            for page in range(1, nb + 1):
                if any(c["pdf"] == pdf and c["page"] == page for c in choisies):
                    continue
                if len(choisies) >= limite:
                    break
                choisies.append({"pdf": pdf, "page": page, "questions": []})
    return choisies[:limite]


def mesure(page: dict, dpi: int, bruit: bool) -> dict:
    pdf, numero = page["pdf"], page["page"]
    langue = langue_de(pdf)
    natif = manifeste_natif(pdf, numero, langue)
    png = rendu(pdf, numero, dpi)
    ocr = graphe_document_ocr.manifeste(png, langue)
    reference = jetons(texte_du_manifeste(natif))
    hypothese = jetons(texte_du_manifeste(ocr))
    commun = sum((Counter(reference) & Counter(hypothese)).values())
    distance = wer(reference, hypothese)
    ligne = {
        "pdf": pdf.name, "page": numero, "langue": langue,
        "mots_natifs": len(reference), "mots_ocr": len(hypothese),
        "distance": distance, "commun": commun,
        "wer": round(distance / max(len(reference), 1), 4),
        "rappel": round(commun / max(len(reference), 1), 4),
        "precision": round(commun / max(len(hypothese), 1), 4),
        "confiance": confiance_moyenne(ocr),
        "questions": len(page["questions"]),
        "detail_questions": [],
    }
    for question in page["questions"]:
        rep_natif = lire(natif, question)
        rep_ocr = lire(ocr, question)
        rep_sans = lire(graphe_document_ocr.manifeste_sans_ocr(png, langue), question)
        trouve_natif = trouve(rep_natif, question["valeur"])
        trouve_ocr = trouve(rep_ocr, question["valeur"])
        f1 = (round(f1_mots(rep_natif["texte"], rep_ocr["texte"]), 4)
              if rep_natif and rep_ocr else 0.0)
        ligne["detail_questions"].append({
            "question": question["question"], "valeur": question["valeur"],
            "trouve_natif": trouve_natif, "trouve_ocr": trouve_ocr,
            "parite_valeur": trouve_natif == trouve_ocr,
            "f1_reponse": f1, "parite_region": f1 >= 0.90,
            "sans_ocr": trouve(rep_sans, question["valeur"]),
            "reponse_natif": (rep_natif or {}).get("texte", "")[:120] or None,
            "reponse_ocr": (rep_ocr or {}).get("texte", "")[:120] or None,
            "page": numero, "pdf": pdf.name,
        })
    if bruit:
        png_bruitee = degradee(png)
        ocr_bruitee = graphe_document_ocr.manifeste(png_bruitee, langue)
        hypothese_bruitee = jetons(texte_du_manifeste(ocr_bruitee))
        distance_bruitee = wer(reference, hypothese_bruitee)
        ligne["distance_bruitee"] = distance_bruitee
        ligne["wer_bruitee"] = round(distance_bruitee / max(len(reference), 1), 4)
        ligne["confiance_bruitee"] = confiance_moyenne(ocr_bruitee)
        for detail, question in zip(ligne["detail_questions"], page["questions"]):
            rep_bruitee = lire(ocr_bruitee, question)
            detail["trouve_bruitee"] = trouve(rep_bruitee, question["valeur"])
            detail["f1_bruitee"] = (
                round(f1_mots(lire(natif, question)["texte"], rep_bruitee["texte"]), 4)
                if rep_bruitee else 0.0)
    return ligne


def agrege(lignes: list[dict]) -> dict:
    questions = [q for l in lignes for q in l["detail_questions"]]
    mots_natifs = sum(l["mots_natifs"] for l in lignes)
    mots_ocr = sum(l["mots_ocr"] for l in lignes)
    commun = sum(l["commun"] for l in lignes)
    distance = sum(l["distance"] for l in lignes)
    confiance = (sum(l["confiance"] * l["mots_natifs"] for l in lignes)
                 / max(mots_natifs, 1))
    n = max(len(questions), 1)
    agregat = {
        "pages": len(lignes),
        "pages_avec_questions": sum(1 for l in lignes if l["questions"]),
        "questions": len(questions),
        "mots_natifs": mots_natifs,
        "wer": round(distance / max(mots_natifs, 1), 4),
        "rappel": round(commun / max(mots_natifs, 1), 4),
        "precision": round(commun / max(mots_ocr, 1), 4),
        "confiance": round(confiance, 1),
        "exactitude_natif": round(sum(q["trouve_natif"] for q in questions) / n, 4),
        "exactitude_ocr": round(sum(q["trouve_ocr"] for q in questions) / n, 4),
        "parite_valeur": round(sum(q["parite_valeur"] for q in questions) / n, 4),
        "parite_region": round(sum(q["parite_region"] for q in questions) / n, 4),
        "f1_median": round(sorted(q["f1_reponse"] for q in questions)[len(questions) // 2], 4)
        if questions else 0.0,
        "sans_ocr": round(sum(q["sans_ocr"] for q in questions) / n, 4),
    }
    if "wer_bruitee" in lignes[0]:
        distance_bruitee = sum(l["distance_bruitee"] for l in lignes)
        agregat["wer_bruitee"] = round(distance_bruitee / max(mots_natifs, 1), 4)
        agregat["confiance_bruitee"] = round(
            sum(l["confiance_bruitee"] * l["mots_natifs"] for l in lignes)
            / max(mots_natifs, 1), 1)
        agregat["parite_valeur_bruitee"] = round(
            sum(q.get("trouve_bruitee", False) == q["trouve_natif"] for q in questions)
            / n, 4)
        agregat["parite_region_bruitee"] = round(
            sum(q.get("f1_bruitee", 0.0) >= 0.90 for q in questions) / n, 4)
        agregat["exactitude_bruitee"] = round(
            sum(q.get("trouve_bruitee", False) for q in questions) / n, 4)
    return agregat


def verdict(agregat: dict) -> list[tuple[str, bool]]:
    bareme = [
        (f"pages ≥ {SEUILS['pages']}", agregat["pages"] >= SEUILS["pages"]),
        (f"WER ≤ {SEUILS['wer']:.0%}", agregat["wer"] <= SEUILS["wer"]),
        (f"rappel ≥ {SEUILS['rappel']:.0%}", agregat["rappel"] >= SEUILS["rappel"]),
        (f"parité de région ≥ {SEUILS['parite_region']:.0%}",
         agregat["parite_region"] >= SEUILS["parite_region"]),
        (f"F1 médian ≥ {SEUILS['f1_median']:.2f}",
         agregat["f1_median"] >= SEUILS["f1_median"]),
        (f"exactitude natif ≥ {SEUILS['exactitude_natif']:.0%}",
         agregat["exactitude_natif"] >= SEUILS["exactitude_natif"]),
        ("sans OCR : aucune réponse", agregat["sans_ocr"] == SEUILS["sans_ocr"]),
    ]
    if "wer_bruitee" in agregat:
        bareme += [
            ("le WER MONTE sur la page dégradée", agregat["wer_bruitee"] > agregat["wer"]),
            ("la parité de région BAISSE sur la page dégradée",
             agregat["parite_region_bruitee"] < agregat["parite_region"]),
        ]
    return bareme


def affiche(resultat: dict, bareme: list[tuple[str, bool]]) -> int:
    a = resultat["agregat"]
    print("=== R4.4 — L'OCR, DIX PAGES, SA PARITÉ ET SES CONTRÔLES ===")
    print(f"  {resultat['dispositif']}")
    print(f"  {'page':<28}{'langue':<8}{'mots':>6}{'WER':>8}{'rappel':>8}{'conf':>7}{'quest.':>7}")
    for ligne in resultat["pages"]:
        print(f"  {ligne['pdf'][:24] + ' p' + str(ligne['page']):<28}{ligne['langue']:<8}"
              f"{ligne['mots_natifs']:>6}{ligne['wer']:>8.2%}{ligne['rappel']:>8.2%}"
              f"{ligne['confiance']:>7.1f}{ligne['questions']:>7}")
    print(f"\n  WER {a['wer']:.2%} · rappel {a['rappel']:.2%} · précision {a['precision']:.2%}"
          f" · confiance {a['confiance']:.1f}")
    print(f"  exactitude de la valeur : natif {a['exactitude_natif']:.2%} · OCR {a['exactitude_ocr']:.2%}")
    print(f"  PARITÉ de région (F1 ≥ 0,90) : {a['parite_region']:.2%} · médiane F1 "
          f"{a['f1_median']:.3f} · valeur stricte {a['parite_valeur']:.2%} "
          f"({a['questions']} questions)")
    if "wer_bruitee" in a:
        print(f"  page dégradée : WER {a['wer_bruitee']:.2%} · exactitude {a['exactitude_bruitee']:.2%}"
              f" · parité région {a['parite_region_bruitee']:.2%}")
    print(f"  sans OCR : {a['sans_ocr']:.2%} de réponses")
    print()
    for libelle, ok in bareme:
        print(f"  {'✅' if ok else '❌'} {libelle}")
    return 0 if all(ok for _, ok in bareme) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pages", type=int, default=10)
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--bruit", action="store_true", default=True,
                    help="passe le contrôle « page dégradée » (défaut : oui)")
    ap.add_argument("--sans-bruit", dest="bruit", action="store_false")
    ap.add_argument("--porte", action="store_true", help="applique les seuils R4.4")
    ap.add_argument("--sortie", type=pathlib.Path, default=SORTIE)
    ap.add_argument("--sans-ecrire", action="store_true")
    args = ap.parse_args()

    graphe_document_ocr.exige()
    pages = pages_du_banc(args.pages)
    lignes = [mesure(p, args.dpi, args.bruit) for p in pages]
    agregat = agrege(lignes)
    resultat = {
        "date": datetime.date.today().isoformat(), "ligne": "R4.4",
        "dispositif": (f"{len(lignes)} pages rendues à {args.dpi} dpi depuis "
                       f"{len({l['pdf'] for l in lignes})} PDF du corpus gelé · "
                       f"{graphe_document_ocr.version()} · "
                       f"lecteur extractif R0.2, questions du banc R0.3"),
        "seuils": SEUILS,
        "agregat": agregat,
        "pages": [{k: v for k, v in l.items() if k != "detail_questions"} for l in lignes],
        "questions": [q for l in lignes for q in l["detail_questions"]],
    }
    bareme = verdict(agregat)
    if not args.sans_ecrire:
        args.sortie.parent.mkdir(parents=True, exist_ok=True)
        args.sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n",
                               encoding="utf-8")
        chemin = args.sortie.relative_to(RACINE) if args.sortie.is_relative_to(RACINE) else args.sortie
        print(f"  JSON : {chemin}")
    code = affiche(resultat, bareme)
    # Sans --porte, l'outil MESURE : un seuil non atteint n'est pas une erreur d'exécution.
    return code if args.porte else 0


if __name__ == "__main__":
    sys.exit(main())
