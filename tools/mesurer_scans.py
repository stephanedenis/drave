#!/usr/bin/env python3
"""mesurer_scans.py — R4.4 : les scans SIMULÉS, mesurés famille par famille et pipeline par pipeline.

POURQUOI CE FICHIER. Le pilote R4.4 a mesuré des pages rendues, pas des scans. `simuler_scan.py`
fabrique cinq familles de scans (photocopie, photo, fax, papier) et un contrôle (`propre`) ; ce
fichier mesure ce qu'elles coûtent, et ce que le prétraitement (`nettoyer_scan.py`) récupère.
La question n'est pas « quel est le WER ? » mais « quelle **famille** de dégradation casse quoi,
et quelle **étape** la relève ».

CE QUE LA MESURE GARDE :
  - le WER mot à mot contre le texte natif de la MÊME page, avec rappel et précision ;
  - la confiance moyenne de l'OCR (pondérée par les mots) ;
  - la PARITÉ des questions du banc R0.3 sur les pages de développement (même lecteur R0.2) ;
  - le split **dev / test** : les pages de test ne portent pas de questions et ne servent qu'au
    WER — le prétraitement est réglé sur dev, le test dit s'il transfère ;
  - deux contrôles : une page **noire** (aucun mot, WER 1) et la famille `propre` (le plafond).

Usage :
  python3 tools/mesurer_scans.py --corpus work/r44/scans/manifeste.json \
      --pipelines brut,auto --sortie work/r44/mesure.json
  python3 tools/mesurer_scans.py --familles photo,fax --limite 3 --pipelines brut,eclairage
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import graphe_document  # noqa: E402
import graphe_document_ocr  # noqa: E402
import mesurer_ocr  # noqa: E402
import nettoyer_scan  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
CACHE_OCR = RACINE / "work/r44/ocr"
CACHE_NET = RACINE / "work/r44/nettoye"


def _sha(octets: bytes) -> str:
    return hashlib.sha256(octets).hexdigest()[:16]


def manifeste_ocr(image: pathlib.Path, langue: str, psm: int = 3,
                  exposants: bool = False, colonnes: bool = False) -> dict:
    """L'OCR d'une image, mis en cache par l'empreinte des pixels : une même image n'est
    jamais OCRisée deux fois, et un pipeline qui ne change pas l'image ne recoûte rien."""
    CACHE_OCR.mkdir(parents=True, exist_ok=True)
    suffixe = f"-m{graphe_document_ocr.VERSION_MANIFESTE}"
    suffixe += (f"-exp{graphe_document_ocr.RECUPERATION_VERSION}" if exposants else "")
    suffixe += "-col" if colonnes else ""
    cle = _sha(image.read_bytes()) + f"-{langue}-{psm}" + suffixe
    cache = CACHE_OCR / f"{cle}.json"
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    try:
        manifeste = graphe_document_ocr.manifeste(image, langue, psm,
                                                  exposants=exposants, colonnes=colonnes)
    except SystemExit:
        # Un scan que l'OCR ne lit pas du tout est un POINT DE MESURE (WER 1), pas une panne
        # du banc : la mesure doit continuer et compter ce zéro, pas s'arrêter dessus.
        manifeste = graphe_document_ocr.manifeste_sans_ocr(image, langue)
        manifeste["extraction"]["echec"] = "aucun bloc OCR"
    cache.write_text(json.dumps(manifeste, ensure_ascii=False), encoding="utf-8")
    return manifeste


def nettoyer(image: pathlib.Path, pipeline: str) -> tuple[pathlib.Path, list[str]]:
    """Une image nettoyée, en cache. `brut` rend l'original — le contrôle."""
    if pipeline == "brut":
        return image, []
    CACHE_NET.mkdir(parents=True, exist_ok=True)
    sortie = CACHE_NET / f"{image.stem}-{pipeline.replace(',', '+')}.png"
    from PIL import Image
    im = Image.open(image).convert("RGB")
    im2, trace = nettoyer_scan.appliquer(im, pipeline.split(","))
    im2.save(sortie)
    return sortie, trace


NATIF_CACHE: dict[tuple, dict] = {}


def manifeste_natif_cached(pdf: pathlib.Path, page: int, langue: str) -> dict:
    """Le même PDF est analysé une fois par page, pas une fois par scan : sans ce cache,
    100 scans = 100 pdftotext, et la porte met sept minutes au lieu d'une."""
    cle = (str(pdf), page, langue)
    if cle not in NATIF_CACHE:
        NATIF_CACHE[cle] = mesurer_ocr.manifeste_natif(pdf, page, langue)
    return NATIF_CACHE[cle]


def questions_par_page() -> dict[tuple[str, int], list[dict]]:
    return {(p["pdf"].name, p["page"]): p["questions"]
            for p in mesurer_ocr.pages_du_banc(10)}


def mesure_entree(entree: dict, pipeline: str, questions: dict,
                  exposants: bool = False, colonnes: bool = False,
                  base: pathlib.Path | None = None) -> dict:
    image = ((base or (RACINE / "work/r44/scans")) / entree["image"])
    pdf = RACINE / "data/onu/pdf" / entree["pdf"]
    natif = manifeste_natif_cached(pdf, entree["page"], entree["langue"])
    reference = mesurer_ocr.jetons(mesurer_ocr.texte_du_manifeste(natif))
    chemin, trace = nettoyer(image, pipeline)
    m = manifeste_ocr(chemin, entree["langue"], exposants=exposants, colonnes=colonnes)
    hypothese = mesurer_ocr.jetons(mesurer_ocr.texte_du_manifeste(m))
    commun = sum((Counter(reference) & Counter(hypothese)).values())
    distance = mesurer_ocr.wer(reference, hypothese)
    ligne = {
        **{k: entree[k] for k in ("image", "pdf", "page", "split", "famille", "graine")},
        "pipeline": pipeline, "trace": trace,
        "mots_natifs": len(reference), "mots_ocr": len(hypothese),
        "distance": distance, "commun": commun,
        "wer": round(distance / max(len(reference), 1), 4),
        "rappel": round(commun / max(len(reference), 1), 4),
        "precision": round(commun / max(len(hypothese), 1), 4),
        "confiance": mesurer_ocr.confiance_moyenne(m),
        "exposants": exposants, "colonnes": colonnes,
        "questions": 0, "parite_region": None, "parite_valeur": None,
        "details": [],
    }
    qs = questions.get((entree["pdf"], entree["page"]), []) if entree["split"] == "dev" else []
    if qs:
        ligne["questions"] = len(qs)
        region, valeur = 0, 0
        for q in qs:
            rep_nat = mesurer_ocr.lire(natif, q)
            rep_ocr = mesurer_ocr.lire(m, q)
            f1 = (mesurer_ocr.f1_mots(rep_nat["texte"], rep_ocr["texte"])
                  if rep_nat and rep_ocr else 0.0)
            region += f1 >= 0.90
            trouve_nat = mesurer_ocr.trouve(rep_nat, q["valeur"])
            trouve_ocr = mesurer_ocr.trouve(rep_ocr, q["valeur"])
            # parité de VALEUR de la spécification : le chiffre est dans le PASSAGE choisi
            passe_nat = mesurer_ocr.trouve_dans_passage(natif, rep_nat, q["valeur"])
            passe_ocr = mesurer_ocr.trouve_dans_passage(m, rep_ocr, q["valeur"])
            valeur += passe_ocr == passe_nat
            ligne["details"].append({"valeur": q["valeur"], "f1": round(f1, 3),
                                     "trouve_natif": trouve_nat, "trouve": trouve_ocr,
                                     "trouve_natif_passage": passe_nat,
                                     "trouve_passage": passe_ocr})
        ligne["parite_region"] = round(region / len(qs), 4)
        ligne["parite_valeur"] = round(valeur / len(qs), 4)
    return ligne


def controle_noir(pipeline: str = "brut") -> dict:
    """Le contrôle : une page NOIRE ne doit produire aucun mot. Une chaîne qui « lit » une
    page noire lit sa propre mémoire, pas le document."""
    from PIL import Image
    chemin = RACINE / "work/r44/scans/_noir.png"
    if not chemin.exists():
        Image.new("RGB", (2550, 3300), (0, 0, 0)).save(chemin)
    m = manifeste_ocr(chemin, "fra")
    texte = mesurer_ocr.texte_du_manifeste(m)
    return {"pipeline": pipeline, "mots": len(mesurer_ocr.jetons(texte)),
            "regions": len([r for r in m["regions"] if r["type"] != "blanc"])}


def agrege(lignes: list[dict]) -> dict:
    par = defaultdict(list)
    for l in lignes:
        par[(l["famille"], l["split"], l["pipeline"])].append(l)
    out = {}
    for (famille, split, pipeline), ls in sorted(par.items()):
        nat = sum(l["mots_natifs"] for l in ls)
        ocr = sum(l["mots_ocr"] for l in ls)
        commun = sum(l["commun"] for l in ls)
        dist = sum(l["distance"] for l in ls)
        details = [d for l in ls for d in l["details"]]
        q = len(details)
        natifs = sum(d["trouve_natif"] for d in details)
        f1s = sorted(d["f1"] for d in details)
        out[f"{famille}|{split}|{pipeline}"] = {
            "famille": famille, "split": split, "pipeline": pipeline, "scans": len(ls),
            "mots_natifs": nat,
            "wer": round(dist / max(nat, 1), 4),
            "rappel": round(commun / max(nat, 1), 4),
            "precision": round(commun / max(ocr, 1), 4),
            "confiance": round(sum(l["confiance"] * l["mots_natifs"] for l in ls) / max(nat, 1), 1),
            "questions": q,
            "exactitude_natif": round(natifs / max(q, 1), 4),
            "exactitude_ocr": round(sum(d["trouve"] for d in details) / max(q, 1), 4),
            # la préservation est LA mesure de parité : ce que le natif trouvait et que le
            # scan retrouve. Compter « les deux échouent » comme une parité flatterait le scan.
            "preservation": (round(sum(d.get("trouve_natif_passage", d["trouve_natif"])
                                      and d.get("trouve_passage", d["trouve"]) for d in details)
                                    / max(natifs, 1), 4) if natifs else None),
            # la variante STRICTE : le chiffre doit être dans la FENÊTRE DE RÉPONSE, pas
            # seulement dans le passage choisi. Publiée à côté, jamais à la place.
            "preservation_reponse": (round(sum(d["trouve_natif"] and d["trouve"] for d in details)
                                           / max(natifs, 1), 4) if natifs else None),
            "parite_region": (round(sum(d["f1"] >= 0.90 for d in details) / max(q, 1), 4)
                              if q else None),
            "f1_median": round(f1s[len(f1s) // 2], 4) if f1s else None,
        }
    return out


SEUILS_PORTE = {
    # Des PLANCHERS par famille, mesurés sur le corpus complet (plafonds de non-régression,
    # pas des prédictions). Le fax 1 bit à 120 dpi a sa propre limite : l'information y est
    # en partie détruite, et aucun prétraitement ne la recrée — c'est écrit, pas caché.
    "par_famille": {
        "propre":     {"wer": 0.06, "preservation": 0.85},
        # la préservation porte sur 30 questions : ±5 questions = ±16,7 points. Les planchers
        # sont donc bas et ASSUMÉS comme des bornes de non-régression, pas des cibles.
        # une seconde graine fait tomber la préservation jusqu'à 63,3 % (photo) : les
        # planchers sont sous cette variance, sinon ils refusent un tirage légitime
        "photocopie": {"wer": 0.08, "preservation": 0.60},
        "photo":      {"wer": 0.10, "preservation": 0.60},
        "papier":     {"wer": 0.10, "preservation": 0.55},
        "fax":        {"wer": 0.25, "preservation": 0.30},
    },
}


def verdict(agregat: dict, noir: dict) -> list[tuple[str, bool]]:
    bareme = [("page noire : aucun mot lu", noir["mots"] == 0 and noir["regions"] == 0)]
    for cle, a in agregat.items():
        seuil = SEUILS_PORTE["par_famille"].get(a["famille"])
        if seuil is None or a["pipeline"] != "auto":
            continue
        bareme.append((f"{a['famille']} · {a['split']} : WER ≤ {seuil['wer']:.0%} "
                       f"(mesuré {a['wer']:.1%})", a["wer"] <= seuil["wer"]))
        if a["split"] == "dev" and a["preservation"] is not None:
            bareme.append((f"{a['famille']} · dev : préservation ≥ "
                           f"{seuil['preservation']:.0%} (mesuré {a['preservation']:.1%})",
                           a["preservation"] >= seuil["preservation"]))
    return bareme


def affiche(agregat: dict, noir: dict) -> None:
    print("=== R4.4 — LES SCANS SIMULÉS, FAMILLE PAR FAMILLE ===")
    print(f"  {'famille':<11}{'split':<6}{'pipeline':<18}{'scans':>6}{'WER':>8}{'rappel':>8}"
          f"{'conf':>7}{'F1med':>7}{'préser.':>9}{'exact.':>8}")
    for cle, a in agregat.items():
        pres = f"{a['preservation']:8.1%}" if a["preservation"] is not None else "       —"
        par = f"{a['parite_region']:7.1%}" if a["parite_region"] is not None else "      —"
        print(f"  {a['famille']:<11}{a['split']:<6}{a['pipeline']:<18}{a['scans']:>6}"
              f"{a['wer']:>8.2%}{a['rappel']:>8.2%}{a['confiance']:>7.1f}"
              f"{a['f1_median'] if a['f1_median'] is not None else 0:>7.2f}{pres:>9}{par:>8}")
    print(f"\n  contrôle page noire : {noir['mots']} mot(s) lu(s), {noir['regions']} région(s)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corpus", type=pathlib.Path, default=RACINE / "work/r44/scans/manifeste.json")
    ap.add_argument("--pipelines", default="brut,auto")
    ap.add_argument("--familles", default="")
    ap.add_argument("--splits", default="dev,test")
    ap.add_argument("--limite", type=int, default=0, help="N scans par famille (fumée)")
    ap.add_argument("--exposants", action="store_true",
                    help="passe chiffres ciblée sur les appels de note")
    ap.add_argument("--colonnes", action="store_true",
                    help="détection de gouttière et ordre de lecture par colonne")
    ap.add_argument("--sortie", type=pathlib.Path, default=RACINE / "work/r44/mesure.json")
    ap.add_argument("--porte", action="store_true",
                    help="applique les planchers par famille et le contrôle page noire")
    args = ap.parse_args()
    corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
    familles = {f for f in args.familles.split(",") if f}
    splits = {s for s in args.splits.split(",") if s}
    pipelines = [p for p in args.pipelines.split(",") if p]
    questions = questions_par_page()
    entrees = [e for e in corpus["entrees"]
               if (not familles or e["famille"] in familles) and e["split"] in splits]
    if args.limite:
        vues = Counter()
        gardees = []
        for e in entrees:
            if vues[(e["famille"], e["split"])] < args.limite:
                gardees.append(e)
                vues[(e["famille"], e["split"])] += 1
        entrees = gardees
    print(f"  {len(entrees)} scans · {len(pipelines)} pipeline(s) · "
          f"{len({(e['famille'], e['split']) for e in entrees})} familles")
    lignes = []
    t0 = time.time()
    for i, e in enumerate(entrees, 1):
        for pipeline in pipelines:
            ligne = mesure_entree(e, pipeline, questions, exposants=args.exposants,
                                  colonnes=args.colonnes, base=args.corpus.resolve().parent)
            lignes.append(ligne)
            print(f"  [{i}/{len(entrees)}] {e['image'][:40]:40s} {pipeline:12s} "
                  f"WER {ligne['wer']:6.2%} conf {ligne['confiance']:5.1f}", flush=True)
    noir = controle_noir()
    agregat = agrege(lignes)
    resultat = {"date": "2026-10-31", "ligne": "R4.4",
                "corpus": str(args.corpus), "nature": "scans SIMULÉS",
                "pipelines": pipelines, "exposants": args.exposants,
                "colonnes": args.colonnes, "controle_noir": noir,
                "agregat": agregat, "entrees": lignes}
    args.sortie.parent.mkdir(parents=True, exist_ok=True)
    args.sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8")
    affiche(agregat, noir)
    bareme = verdict(agregat, noir)
    print()
    for libelle, ok in bareme:
        print(f"  {'✅' if ok else '❌'} {libelle}")
    print(f"\n  {len(lignes)} mesures en {time.time() - t0:.0f} s → {args.sortie}")
    return (0 if all(ok for _, ok in bareme) else 1) if args.porte else 0


if __name__ == "__main__":
    sys.exit(main())
