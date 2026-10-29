#!/usr/bin/env python3
"""routeur.py — R0.5 : choisir le lecteur (extractif ou génératif) selon la question.

POURQUOI CE FICHIER. Deux régimes mesurés, pas supposés : sur 249 questions qui partagent les
mots du document, l'extractif donne 0,72–1,00 et le modèle 0,23 ; sur 19 paraphrases, le modèle
donne 0,717 et l'extractif 0,30. Un seul lecteur perd la moitié des cas. Le routeur doit
décider — et la seule question qui compte est : **le signal prédit-il quel lecteur va gagner ?**

Le signal candidat est le **meilleur score BM25** des passages du document pour la question.
S'il est haut, les mots de la question sont dans le document : l'extractif suffit. S'il est
bas, la question parle d'autre chose : il faut le modèle.

Ce que ce fichier mesure :
  - l'**AUC du signal** pour l'étiquette « l'extractif bat le modèle » (toutes les questions,
    les deux bancs mélangés) ;
  - l'**exactitude du routeur** au seuil, et le **transfert** : seuil réglé sur un banc, testé
    sur l'autre ;
  - le **regret** contre un oracle qui choisirait toujours le bon lecteur ;
  - les **contrôles** : signal aléatoire, longueur de la question, choix fixes.

Usage :
  python3 tools/routeur.py --json reports/r07-routeur.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import graphe_document  # noqa: E402
import lecteur_controleur as lc  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
BANCS = [
    ("lexical", RACINE / "tools/tests/documents/bench-complet.json",
     RACINE / "reports/r03-banc-extractif.json", RACINE / "reports/r03-banc-modele.json"),
    ("paraphrase", RACINE / "tools/tests/documents/bench-durci.json",
     RACINE / "reports/r03-banc-durci-extractif.json", RACINE / "reports/r03-banc-durci-modele.json"),
]
GRAINE = 20261029


def charge() -> list[dict]:
    """Une ligne par question : le signal, et ce qu'a fait chaque lecteur."""
    lignes = []
    for banc, chemin_banc, chemin_ext, chemin_modele in BANCS:
        bench = json.loads(chemin_banc.read_text(encoding="utf-8"))
        ext = {(d["document"], d["question"]): d for d in
               json.loads(chemin_ext.read_text(encoding="utf-8"))["details"]}
        modele = {(d["document"], d["question"]): d for d in
                  json.loads(chemin_modele.read_text(encoding="utf-8"))["details"]}
        index_par_document = {}
        jetons_par_document = {}
        for document in bench["documents"]:
            passages = lc.passages(graphe_document.manifeste(RACINE / document["chemin"]))
            index_par_document[document["chemin"]] = lc.Index(passages)
            jetons_par_document[document["chemin"]] = set(
                j for p in passages for j in lc.jetons(p["texte"]))
        for cle, detail in ext.items():
            if cle not in modele:
                continue
            scores = index_par_document[cle[0]].scores(cle[1])
            mots = set(lc.jetons(cle[1]))
            couverture = (len(mots & jetons_par_document[cle[0]]) / len(mots)) if mots else 0.0
            lignes.append({
                "banc": banc, "document": cle[0], "question": cle[1],
                "type": detail["type"],
                "signal": round(max(scores), 3) if scores else 0.0,
                "couverture": round(couverture, 3),
                "extractif": 1 if detail["controlee_0.30"]["valeur"] else 0,
                "modele": 1 if modele[cle]["controlee_0.30"]["valeur"] else 0,
                "longueur": len(lc.jetons(cle[1])),
            })
    return lignes


def auc(scores: list[float], labels: list[int]) -> float:
    positifs = [s for s, l in zip(scores, labels) if l == 1]
    negatifs = [s for s, l in zip(scores, labels) if l == 0]
    if not positifs or not negatifs:
        return 0.5
    return sum((p > n) + 0.5 * (p == n) for p in positifs for n in negatifs) / (
        len(positifs) * len(negatifs))


def exactitude_sur(lignes: list[dict], seuil: float, champ: str = "signal") -> float:
    if not lignes:
        return 0.0
    return sum(l["extractif"] if l[champ] >= seuil else l["modele"] for l in lignes) / len(lignes)


def seuil_sur(lignes: list[dict], champ: str = "signal") -> float:
    return max(sorted({l[champ] for l in lignes}), key=lambda s: exactitude_sur(lignes, s, champ))


def exactitude(lignes: list[dict], seuil: float) -> float:
    """Le routeur choisit l'extractif si signal ≥ seuil, le modèle sinon."""
    if not lignes:
        return 0.0
    justes = 0
    for l in lignes:
        choix = l["extractif"] if l["signal"] >= seuil else l["modele"]
        justes += choix
    return justes / len(lignes)


def meilleur_seuil(lignes: list[dict]) -> float:
    candidats = sorted({l["signal"] for l in lignes})
    return max(candidats, key=lambda s: exactitude(lignes, s))


def main() -> int:
    ap = argparse.ArgumentParser(description="R0.5 — le routeur extractif/génératif.")
    ap.add_argument("--json", type=pathlib.Path)
    args = ap.parse_args()
    lignes = charge()
    if not lignes:
        raise SystemExit("aucune question : les JSON de lecteurs manquent")

    # 1. le signal prédit-il le gagnant ? (sur les questions où les deux diffèrent)
    differes = [l for l in lignes if l["extractif"] != l["modele"]]
    labels = [l["extractif"] for l in differes]
    signal_auc = auc([l["signal"] for l in differes], labels)
    couverture_auc = auc([l["couverture"] for l in differes], labels)
    longueur_auc = auc([l["longueur"] for l in differes], labels)
    hasard = random.Random(GRAINE)
    aleatoire_auc = auc([hasard.random() for _ in differes], labels)

    # 2. exactitude : choix fixes, oracle, routeur réglé sur un banc et testé sur l'autre
    extractif_fixe = sum(l["extractif"] for l in lignes) / len(lignes)
    modele_fixe = sum(l["modele"] for l in lignes) / len(lignes)
    oracle = sum(max(l["extractif"], l["modele"]) for l in lignes) / len(lignes)
    transferts = []
    for banc_test in ("lexical", "paraphrase"):
        apprentissage = [l for l in lignes if l["banc"] != banc_test]
        test = [l for l in lignes if l["banc"] == banc_test]
        seuil = seuil_sur(apprentissage, "couverture")
        transferts.append({"banc_test": banc_test, "seuil": round(seuil, 3),
                           "exactitude": round(exactitude_sur(test, seuil, "couverture"), 3),
                           "n": len(test),
                           "fixe_extractif": round(sum(l["extractif"] for l in test) / len(test), 3),
                           "fixe_modele": round(sum(l["modele"] for l in test) / len(test), 3),
                           "oracle": round(sum(max(l["extractif"], l["modele"]) for l in test) / len(test), 3)})

    print("=== ROUTEUR EXTRACTIF / GÉNÉRATIF ===")
    print(f"  {len(lignes)} questions · {len(differes)} où les deux lecteurs diffèrent")
    print(f"  AUC du signal BM25   : {signal_auc:.3f}")
    print(f"  AUC couverture       : {couverture_auc:.3f}")
    print(f"  AUC longueur (faux)  : {longueur_auc:.3f}")
    print(f"  AUC aléatoire        : {aleatoire_auc:.3f}")
    print(f"  exactitude : fixe extractif {extractif_fixe:.3f} · fixe modèle {modele_fixe:.3f} "
          f"· oracle {oracle:.3f}")
    for t in transferts:
        print(f"  couverture : seuil appris ailleurs, testé sur {t['banc_test']:11s} "
              f"(n={t['n']:3d}, seuil {t['seuil']:.2f}) : {t['exactitude']:.3f} "
              f"· fixe ext {t['fixe_extractif']:.3f} · fixe modèle {t['fixe_modele']:.3f} "
              f"· oracle {t['oracle']:.3f}")
    if args.json:
        args.json.write_text(json.dumps({
            "date": "2026-10-29", "ligne": "R0.5", "questions": len(lignes),
            "differes": len(differes), "auc_signal": round(signal_auc, 3),
            "auc_longueur": round(longueur_auc, 3), "auc_aleatoire": round(aleatoire_auc, 3),
            "fixe_extractif": round(extractif_fixe, 3), "fixe_modele": round(modele_fixe, 3),
            "oracle": round(oracle, 3), "transferts": transferts,
            "lignes": lignes,
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  résultats : {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
