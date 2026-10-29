#!/usr/bin/env python3
"""declencheur.py — R06 v3 : un déclencheur qui ne soit pas une échelle de scores.

POURQUOI CE FICHIER EXISTE. Trois tentatives de seuil ont échoué (R0.5, R06, la cascade) : un
seuil **absolu** sur un score BM25 ne transfère pas d'un corpus à l'autre, parce que l'échelle
change avec le document. Le verrou n'est donc pas la cascade, c'est le **déclencheur** : le
signal qui dit « cette réponse est douteuse, paie le modèle ».

Ce fichier teste des signaux **sans échelle**, censés transférer :
  - **dispersion** : (top1 − top2) / top1 — l'écart relatif du meilleur passage au second ;
  - **couverture** : la part des mots de la question présents dans la réponse ;
  - **accord** : le span du balayage tombe-t-il dans le passage que l'extractif a choisi ?
  - **stabilité** : le meilleur passage reste-t-il le meilleur quand on retire un mot de la
    question ?

L'étiquette est « l'extractif a juste » ; l'AUC dit si le signal sait quand il se trompe ; le
**transfert** (appris sur un banc, testé sur l'autre) dit si c'est une règle ou une échelle.

Usage :
  python3 tools/declencheur.py --json reports/r06-declencheur.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import graphe_document  # noqa: E402
import index_spans  # noqa: E402
import lecteur_controleur as lc  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
JEUX = (
    ("lexical", RACINE / "tools/tests/documents/bench-complet.json",
     RACINE / "reports/r03-banc-extractif.json", RACINE / "reports/r03-banc-modele.json"),
    ("paraphrase", RACINE / "tools/tests/documents/bench-durci.json",
     RACINE / "reports/r03-banc-durci-extractif.json", RACINE / "reports/r03-banc-durci-modele.json"),
)
SIGNAUX = ("dispersion", "couverture", "accord", "stabilite")


def charge() -> list[dict]:
    lignes = []
    for banc, chemin_banc, chemin_ext, chemin_modele in JEUX:
        bench = json.loads(chemin_banc.read_text(encoding="utf-8"))
        ext = {(d["document"], d["question"]): d for d in
               json.loads(chemin_ext.read_text(encoding="utf-8"))["details"]}
        modele = {(d["document"], d["question"]): d for d in
                  json.loads(chemin_modele.read_text(encoding="utf-8"))["details"]}
        index_doc: dict[str, tuple] = {}
        for document in bench["documents"]:
            manifeste = graphe_document.manifeste(RACINE / document["chemin"])
            passages = lc.passages(manifeste)
            index_doc[document["chemin"]] = (passages, lc.Index(passages),
                                             index_spans.IndexSpans(manifeste))
        for cle, detail in ext.items():
            if cle not in modele:
                continue
            passages, index, spans = index_doc[cle[0]]
            scores = index.scores(cle[1])
            ordre = sorted(range(len(passages)), key=lambda i: -scores[i])
            top = ordre[0]
            second = scores[ordre[1]] if len(ordre) > 1 else 0.0
            mots = set(lc.jetons(cle[1]))
            couv = len(mots & set(lc.jetons(passages[top]["texte"]))) / max(len(mots), 1)
            # accord : le meilleur span du balayage est-il dans le passage choisi par l'extractif ?
            haut = spans.chercher(cle[1], 1)
            accord = int(bool(haut) and haut[0]["passage"] == top)
            # stabilité : retirer le mot le plus rare de la question change-t-il le gagnant ?
            rares = sorted(mots, key=lambda m: index.df.get(m, 0))
            if rares and len(mots) > 2:
                reduite = " ".join(m for m in lc.jetons(cle[1]) if m != rares[0])
                scores2 = index.scores(reduite)
                stable = int(sorted(range(len(passages)), key=lambda i: -scores2[i])[0] == top)
            else:
                stable = 1
            lignes.append({
                "banc": banc, "document": cle[0], "question": cle[1],
                "extractif_juste": int(detail["controlee_0.30"]["valeur"]),
                "modele_juste": int(modele[cle]["controlee_0.30"]["valeur"]),
                "dispersion": round((scores[top] - second) / max(scores[top], 1e-9), 3),
                "couverture": round(couv, 3), "accord": accord, "stabilite": stable,
            })
    return lignes


def auc(scores, labels) -> float:
    pos = [s for s, l in zip(scores, labels) if l == 1]
    neg = [s for s, l in zip(scores, labels) if l == 0]
    if not pos or not neg:
        return 0.5
    return sum((p > n) + 0.5 * (p == n) for p in pos for n in neg) / (len(pos) * len(neg))


def entraine(X, y, lam=1.0) -> np.ndarray:
    Xb = np.hstack([X, np.ones((len(X), 1))])
    w = np.zeros(Xb.shape[1])
    for _ in range(3000):
        p = 1 / (1 + np.exp(-np.clip(Xb @ w, -30, 30)))
        w -= 0.5 * (Xb.T @ (p - y) / len(y) + lam * np.r_[w[:-1], 0] / len(y))
    return w


def confiance(lignes: list[dict], w: np.ndarray) -> np.ndarray:
    X = np.array([[l[s] for s in SIGNAUX] for l in lignes])
    return 1 / (1 + np.exp(-np.clip(np.hstack([X, np.ones((len(X), 1))]) @ w, -30, 30)))


def main() -> int:
    ap = argparse.ArgumentParser(description="R06 v3 — le déclencheur sans échelle.")
    ap.add_argument("--json", type=pathlib.Path)
    args = ap.parse_args()
    lignes = charge()
    resultats = {"n": len(lignes), "signaux": {}, "transferts": [], "politiques": {}}

    print("=== SIGNAUX (AUC pour « l'extractif a juste ») ===")
    for s in SIGNAUX:
        a = auc([l[s] for l in lignes], [l["extractif_juste"] for l in lignes])
        resultats["signaux"][s] = round(a, 3)
        print(f"  {s:11s} AUC {a:.3f}")

    # la référence : l'extractif seul, le modèle seul, l'oracle — PAR BANC (le pool les mélange)
    for banc in ("lexical", "paraphrase"):
        sous = [l for l in lignes if l["banc"] == banc]
        ext_b = float(np.mean([l["extractif_juste"] for l in sous]))
        mod_b = float(np.mean([l["modele_juste"] for l in sous]))
        oracle_b = float(np.mean([max(l["extractif_juste"], l["modele_juste"]) for l in sous]))
        resultats["politiques"][banc] = {"extractif": round(ext_b, 3), "modele": round(mod_b, 3),
                                         "oracle": round(oracle_b, 3)}
        print(f"  {banc:11s} n={len(sous):3d} · extractif {ext_b:.3f} · modèle {mod_b:.3f} "
              f"· oracle {oracle_b:.3f}")

    # le transfert : appris sur un banc, testé sur l'autre
    print("=== TRANSFERT ===")
    for banc_test in ("lexical", "paraphrase"):
        app = [l for l in lignes if l["banc"] != banc_test]
        test = [l for l in lignes if l["banc"] == banc_test]
        w = entraine(np.array([[l[s] for s in SIGNAUX] for l in app]),
                     np.array([l["extractif_juste"] for l in app]))
        conf = confiance(test, w)
        a = auc(list(conf), [l["extractif_juste"] for l in test])
        # politique : sous le seuil de confiance, on paie le modèle
        meilleur = max(0.05, min(0.95, np.median(conf)))
        taux = float(np.mean([l["modele_juste"] if c < meilleur else l["extractif_juste"]
                              for l, c in zip(test, conf)]))
        appels = int(np.sum(conf < meilleur))
        # le plafond de la politique sur ce banc : le meilleur seuil (réglé sur le test, donc
        # un ORACLE de seuil — il dit ce que la politique peut rapporter, pas ce qu'elle rapporte)
        plafond, seuil_plafond = 0.0, 0.0
        for s in sorted(set(conf)):
            taux_s = float(np.mean([l["modele_juste"] if c < s else l["extractif_juste"]
                                    for l, c in zip(test, conf)]))
            if taux_s > plafond:
                plafond, seuil_plafond = taux_s, s
        # « toujours le modèle » et « toujours l'extractif » sur ce banc
        ext_b = float(np.mean([l["extractif_juste"] for l in test]))
        mod_b = float(np.mean([l["modele_juste"] for l in test]))
        resultats["transferts"].append({"banc_test": banc_test, "n": len(test),
                                        "auc": round(a, 3), "seuil": round(float(meilleur), 3),
                                        "taux": round(taux, 3), "appels_modele": appels,
                                        "plafond_seuil": round(plafond, 3),
                                        "seuil_plafond": round(float(seuil_plafond), 3),
                                        "fixe_extractif": round(ext_b, 3),
                                        "fixe_modele": round(mod_b, 3)})
        print(f"  testé sur {banc_test:11s} (n={len(test)}) : AUC {a:.3f} · transféré {taux:.3f} "
              f"({appels} appels) · plafond {plafond:.3f} · fixe ext {ext_b:.3f} / modèle {mod_b:.3f}")

    if args.json:
        args.json.write_text(json.dumps({"date": "2026-10-29", "ligne": "R06", **resultats},
                                        ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  résultats : {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
