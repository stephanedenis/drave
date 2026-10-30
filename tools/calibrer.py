#!/usr/bin/env python3
"""calibrer.py — R06 v6 : publier la cascade à confiance (le seuil vient d'un fichier daté).

POURQUOI CE FICHIER EXISTE. R06 v4/v5 a montré que la cascade à confiance, **calibrée par
corpus**, égale l'oracle (0,911 lexical / 0,415 paraphrases) et qu'il faut ~50 golds. Mais le
seuil se réglait à la main sur la ligne de commande (`--seuil-confiance 0.16`) : ce n'est pas une
politique publiée, c'est un réglage de séance.

Ce fichier fait le passage : un **banc** (questions + golds) → un **fichier de calibration**
daté et vérifiable (banc, empreinte du corpus gelé, n, seuil, taux de calibration), que le
pipeline lit ensuite (`lecture.py --cascade --calibration`).

Usage :
  python3 tools/calibrer.py --banc tools/tests/documents/bench-complet.json \\
      --extractif reports/r03-banc-extractif.json --modele reports/r03-banc-modele.json \\
      --part paires --ecrit tools/tests/documents/calibration-lexical.json
  python3 tools/calibrer.py --verifie tools/tests/documents/calibration-lexical.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import graphe_document  # noqa: E402
import index_spans  # noqa: E402
import lecteur_controleur as lc  # noqa: E402
import lecture  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
MANIFESTE_CORPUS = RACINE / "tools/tests/documents/corpus/manifeste.json"


def empreinte_corpus() -> str:
    return hashlib.sha256(MANIFESTE_CORPUS.read_bytes()).hexdigest()[:16] if MANIFESTE_CORPUS.exists() else ""


def charge_lignes(banc: pathlib.Path, chemin_ext: pathlib.Path, chemin_modele: pathlib.Path,
                  part: str) -> list[dict]:
    bench = json.loads(banc.read_text(encoding="utf-8"))
    ext = {(d["document"], d["question"]): d for d in
           json.loads(chemin_ext.read_text(encoding="utf-8"))["details"]}
    modele = {(d["document"], d["question"]): d for d in
              json.loads(chemin_modele.read_text(encoding="utf-8"))["details"]}
    cache: dict[str, tuple] = {}
    for document in bench["documents"]:
        manifeste = graphe_document.manifeste(RACINE / document["chemin"])
        passages = lc.passages(manifeste)
        cache[document["chemin"]] = (passages, lc.Index(passages), index_spans.IndexSpans(manifeste))
    lignes = []
    for i, (cle, detail) in enumerate(sorted(ext.items())):
        if cle not in modele:
            continue
        if part == "paires" and i % 2:
            continue
        if part == "impaires" and i % 2 == 0:
            continue
        passages, index, spans = cache[cle[0]]
        c = lecture.confiance(cle[1], passages, index.scores(cle[1]), spans)
        lignes.append({"question": cle[1], "conf": c["confiance"],
                       "extractif": int(detail["controlee_0.30"]["valeur"]),
                       "modele": int(modele[cle]["controlee_0.30"]["valeur"])})
    return lignes


def regle(lignes: list[dict]) -> tuple[float, float]:
    """Le seuil qui maximise le taux sur l'échantillon, et ce taux."""
    meilleur, seuil = -1.0, 0.0
    for s in sorted({l["conf"] for l in lignes}):
        taux = float(np.mean([l["modele"] if l["conf"] < s else l["extractif"] for l in lignes]))
        if taux > meilleur:
            meilleur, seuil = taux, s
    return seuil, meilleur


def calibre(args) -> int:
    lignes = charge_lignes(args.banc, args.extractif, args.modele, args.part)
    seuil, taux = regle(lignes)
    sortie = {"date": args.date, "ligne": "R06", "banc": str(args.banc.resolve().relative_to(RACINE)),
              "part": args.part, "n": len(lignes), "seuil": round(float(seuil), 3),
              "taux_calibration": round(taux, 3),
              "empreinte_corpus": empreinte_corpus(),
              "poids": {"couverture": 0.5, "accord": 0.3, "dispersion": 0.2}}
    if args.ecrit:
        args.ecrit.write_text(json.dumps(sortie, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"calibration : n={len(lignes)} · seuil {seuil:.3f} · taux {taux:.3f} → {args.ecrit}")
    else:
        print(json.dumps(sortie, ensure_ascii=False, indent=1))
    return 0


def verifie(chemin: pathlib.Path) -> int:
    """La reproductibilité : le fichier de calibration correspond-il au banc qu'il nomme ?"""
    cal = json.loads(chemin.read_text(encoding="utf-8"))
    banc = RACINE / cal["banc"]
    prefixe = banc.parent.name
    chemin_ext = RACINE / "reports" / ("r03-banc-extractif.json" if "complet" in prefixe
                                       else "r03-banc-durci-extractif.json") if False else None
    # les bancs ont des JSON de lecteurs nommés par famille : on les déduit du chemin
    if "complet" in cal["banc"]:
        chemins = (RACINE / "reports/r03-banc-extractif.json", RACINE / "reports/r03-banc-modele.json")
    else:
        chemins = (RACINE / "reports/r03-banc-durci-extractif.json",
                   RACINE / "reports/r03-banc-durci-modele.json")
    lignes = charge_lignes(banc, chemins[0], chemins[1], cal["part"])
    seuil, taux = regle(lignes)
    ok = abs(seuil - cal["seuil"]) < 0.005 and abs(taux - cal["taux_calibration"]) < 0.005
    print(f"{'✅' if ok else '❌'} calibration reproductible : seuil {seuil:.3f} (fichier {cal['seuil']}), "
          f"taux {taux:.3f} (fichier {cal['taux_calibration']}) · n={len(lignes)}")
    return 0 if ok else 1


def teste(chemin: pathlib.Path) -> int:
    """Le taux HORS ÉCHANTILLON : la calibration a été réglée sur les paires, on applique son
    seuil aux impaires — sans jamais les avoir vus."""
    cal = json.loads(chemin.read_text(encoding="utf-8"))
    banc = RACINE / cal["banc"]
    if "complet" in cal["banc"]:
        chemins = (RACINE / "reports/r03-banc-extractif.json", RACINE / "reports/r03-banc-modele.json")
    else:
        chemins = (RACINE / "reports/r03-banc-durci-extractif.json",
                   RACINE / "reports/r03-banc-durci-modele.json")
    lignes = charge_lignes(banc, chemins[0], chemins[1], "impaires")
    seuil = cal["seuil"]
    taux = float(np.mean([l["modele"] if l["conf"] < seuil else l["extractif"] for l in lignes]))
    appels = sum(1 for l in lignes if l["conf"] < seuil)
    fixe_ext = float(np.mean([l["extractif"] for l in lignes]))
    fixe_mod = float(np.mean([l["modele"] for l in lignes]))
    oracle = float(np.mean([max(l["extractif"], l["modele"]) for l in lignes]))
    print(f"test {cal['part']}→impaires : n={len(lignes)} · seuil {seuil:.3f} · cascade {taux:.3f} "
          f"({appels} appels) · fixe ext {fixe_ext:.3f} · fixe modèle {fixe_mod:.3f} · oracle {oracle:.3f}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="R06 — la calibration de la cascade.")
    ap.add_argument("--banc", type=pathlib.Path)
    ap.add_argument("--extractif", type=pathlib.Path)
    ap.add_argument("--modele", type=pathlib.Path)
    ap.add_argument("--part", choices=("toutes", "paires", "impaires"), default="paires")
    ap.add_argument("--date", default="2026-10-30")
    ap.add_argument("--ecrit", type=pathlib.Path)
    ap.add_argument("--verifie", type=pathlib.Path)
    ap.add_argument("--teste", type=pathlib.Path)
    args = ap.parse_args()
    if args.verifie:
        return verifie(args.verifie)
    if args.teste:
        return teste(args.teste)
    if not (args.banc and args.extractif and args.modele):
        ap.error("--banc, --extractif et --modele sont requis")
    return calibre(args)


if __name__ == "__main__":
    sys.exit(main())
