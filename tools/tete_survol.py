#!/usr/bin/env python3
"""tete_survol.py — R0.4 : une tête apprend la pertinence sur les états précoces.

POURQUOI CE FICHIER. Le contrôleur de R0.2 décide avec BM25 : il partage donc le scoreur du
lecteur extractif, et il ne sait pas ce qu'est une **paraphrase**. R0.4 demande une tête
apprise : lire la question ET le début d'une région, et prédire si la région vaut la peine
d'être lue. La question de la fiche est précise : **la tête bat-elle le scoreur classique à
budget égal ?**

Le dispositif, et ses garde-fous :
  - **l'état précoce** est capturé par le moteur, après les 4 premières couches du modèle
    (`--couches 0:3 --tete-partielle --etat-sortie`) : 896 valeurs par paire (question, début
    de passage) ;
  - **les négatifs** sont des passages du MÊME document, tirés au sort : la tête ne peut pas
    apprendre « ce document est le bon » ;
  - **le partage est par document** (leave-one-document-out) : aucun passage du test n'a été vu
    à l'entraînement — c'est la règle de la fiche ;
  - **la référence est BM25** sur les mêmes paires, et la métrique est l'**AUC** : à budget
    égal, la tête doit classer le gold devant les négatifs mieux que le scoreur classique.

Usage :
  python3 tools/tete_survol.py --extrait          # capture les états (moteur, CPU)
  python3 tools/tete_survol.py --mesure           # entraîne et mesure (numpy)
  python3 tools/tete_survol.py --tout --json reports/r04-tete-survol.json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import subprocess
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import graphe_document  # noqa: E402
import lecteur_controleur as lc  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
BINAIRE = RACINE / "drave-core/target/release/drave"
MODELE = RACINE / "models/Qwen2.5-0.5B-Q8_0.gguf"
BANC = RACINE / "tools/tests/documents/bench-durci.json"
NEGATIFS = 5
COUCHES = __import__("os").environ.get("TETE_COUCHES", "0:3")
DURS = __import__("os").environ.get("TETE_DURS", "0") == "1"
GRAINE = 20261029
CACHE = pathlib.Path(f"/tmp/tete-survol-{COUCHES.replace(':', '-')}{'-durs' if DURS else ''}.npz")


def paires() -> list[dict]:
    """Le jeu : pour chaque question du banc durci, le gold et N négatifs du même document."""
    banc = json.loads(BANC.read_text(encoding="utf-8"))
    aleatoire = random.Random(GRAINE)
    out = []
    for document in banc["documents"]:
        passages = lc.passages(graphe_document.manifeste(RACINE / document["chemin"]))
        for q in document["questions"]:
            or_ = next((i for i, p in enumerate(passages) if q["indice"] in p["texte"]), None)
            if or_ is None:
                continue
            # négatifs DURS : les passages de la MÊME section que le gold (même vocabulaire),
            # au lieu de passages tirés au hasard — sinon BM25 (et la tête) les séparent sans peine.
            section = passages[or_]["section"]
            if DURS:
                autres = [i for i in range(len(passages))
                          if i != or_ and passages[i]["section"] == section
                          and len(passages[i]["texte"]) > 60]
                if len(autres) < NEGATIFS:
                    autres += [i for i in range(len(passages))
                               if i != or_ and i not in autres and len(passages[i]["texte"]) > 60]
            else:
                autres = [i for i in range(len(passages)) if i != or_ and len(passages[i]["texte"]) > 60]
            choix = aleatoire.sample(autres, min(NEGATIFS, len(autres)))
            for indice, etiquette in [(or_, 1)] + [(i, 0) for i in choix]:
                out.append({"document": document["chemin"], "type": document["type"],
                            "question": q["question"], "passage": passages[indice]["texte"][:140],
                            "etiquette": etiquette})
    return out


def extrait(paire: dict, numero: int) -> np.ndarray | None:
    """L'état précoce (896 valeurs) au dernier jeton du prompt question+passage."""
    prompt = (f"Question : {paire['question']}\n"
              f"Passage : {paire['passage']}\n")
    base = pathlib.Path(f"/tmp/tete-{numero}")
    for vieux in pathlib.Path("/tmp").glob(f"tete-{numero}.*"):
        vieux.unlink()
    subprocess.run(
        [str(BINAIRE), str(MODELE), "--infer", "--prompt", prompt, "--n", "1", "--temp", "0",
         "--couches", COUCHES, "--tete-partielle", "--etat-sortie", str(base),
         "--etat-pos", ",".join(str(i) for i in range(64)), "--threads", "4"],
        capture_output=True, timeout=120)
    fichiers = sorted(pathlib.Path("/tmp").glob(f"tete-{numero}.*"),
                      key=lambda p: int(p.suffix[1:]))
    if not fichiers:
        return None
    return np.frombuffer(fichiers[-1].read_bytes(), dtype="<f4").astype(np.float64)


def capture() -> tuple[np.ndarray, np.ndarray, list[dict]]:
    jeu = paires()
    X, y, meta = [], [], []
    for numero, paire in enumerate(jeu):
        etat = extrait(paire, numero)
        if etat is None:
            continue
        X.append(etat)
        y.append(paire["etiquette"])
        meta.append({k: paire[k] for k in ("document", "type", "question", "passage", "etiquette")})
        if numero % 20 == 0:
            print(f"  {numero + 1}/{len(jeu)} paires…")
    return np.array(X), np.array(y), meta


def bm25_scores(meta: list[dict]) -> np.ndarray:
    """La référence classique : BM25 de la question sur les passages du même groupe."""
    scores = []
    groupes: dict[str, list[int]] = {}
    for i, m in enumerate(meta):
        groupes.setdefault(m["document"] + m["question"], []).append(i)
    for indices in groupes.values():
        passages = [{"texte": meta[i]["passage"]} for i in indices]
        index = lc.Index(passages)
        s = index.scores(meta[indices[0]]["question"])
        scores += list(zip(indices, s))
    scores.sort()
    return np.array([s for _, s in scores])


def auc(scores: np.ndarray, labels: np.ndarray) -> float:
    positifs = scores[labels == 1]
    negatifs = scores[labels == 0]
    if len(positifs) == 0 or len(negatifs) == 0:
        return 0.5
    return float(np.mean([(p > n) + 0.5 * (p == n) for p in positifs for n in negatifs]))


def entraine(X: np.ndarray, y: np.ndarray, lam: float = 10.0) -> np.ndarray:
    """Régression logistique ridge, fermée : peu de données, un modèle linéaire, pas de torch."""
    Xb = np.hstack([X, np.ones((len(X), 1))])
    w = np.zeros(Xb.shape[1])
    for _ in range(2000):
        p = 1 / (1 + np.exp(-Xb @ w))
        gradient = Xb.T @ (p - y) / len(y) + lam * np.r_[w[:-1], 0] / len(y)
        w -= 0.5 * gradient
    return w


def mesure(json_path: pathlib.Path | None = None) -> int:
    if not CACHE.exists():
        raise SystemExit("états absents : lancer --extrait d'abord")
    donnees = np.load(CACHE, allow_pickle=True)
    X, y, meta = donnees["X"], donnees["y"], list(donnees["meta"])
    # le texte des passages n'est pas dans le cache : le jeu est déterministe (graine fixe),
    # on le reconstruit et on l'aligne par indice.
    jeu = paires()
    # Le cache ne porte pas les passages pour les anciennes captures : on aligne par POSITION
    # (les groupes sont contigus et dans l'ordre du banc). Un document qui a bougé depuis la
    # capture fait perdre un groupe entier — on l'écarte, au lieu de tout refuser.
    passages: list[str | None] = []
    if "passage" in meta[0]:
        passages = [m["passage"] for m in meta]
    else:
        pos = 0
        for m in meta:
            if pos < len(jeu) and (jeu[pos]["document"], jeu[pos]["question"]) == (m["document"], m["question"]):
                passages.append(jeu[pos]["passage"])
                pos += 1
            else:
                passages.append(None)
        ecartees = sum(1 for x in passages if x is None)
        if ecartees:
            print(f"  ⚠️ {ecartees} paires écartées (gold déplacé depuis la capture)")
    garder = [i for i, x in enumerate(passages) if x is not None]
    X = X[garder]
    y = y[garder]
    meta = [{**meta[i], "passage": passages[i]} for i in garder]
    scores_bm25 = bm25_scores(meta)
    plis = sorted({m["document"] for m in meta})
    resultats = []
    melange = np.random.RandomState(GRAINE)
    for document in plis:
        test = np.array([m["document"] == document for m in meta])
        w = entraine(X[~test], y[~test])
        p = 1 / (1 + np.exp(-np.hstack([X[test], np.ones((test.sum(), 1))]) @ w))
        # contrôle : les MÊMES états, les étiquettes d'entraînement mélangées. Si la tête garde
        # son AUC, elle lit une fuite (longueur, type, ordre) et non la pertinence.
        y_melange = y[~test].copy()
        melange.shuffle(y_melange)
        w0 = entraine(X[~test], y_melange)
        p0 = 1 / (1 + np.exp(-np.hstack([X[test], np.ones((test.sum(), 1))]) @ w0))
        resultats.append({"document": document, "type": meta[int(np.argmax(test))]["type"],
                          "n_test": int(test.sum()),
                          "auc_tete": round(auc(p, y[test]), 3),
                          "auc_bm25": round(auc(scores_bm25[test], y[test]), 3),
                          "auc_etiquettes_melangees": round(auc(p0, y[test]), 3)})
    print("=== TÊTE DE SURVOL — leave-one-document-out ===")
    for r in resultats:
        print(f"  {r['type']:10s} {r['document']:44s} n={r['n_test']:3d} "
              f"AUC tête {r['auc_tete']:.3f} · BM25 {r['auc_bm25']:.3f} "
              f"· mélangé {r['auc_etiquettes_melangees']:.3f}")
    tete = np.mean([r["auc_tete"] for r in resultats])
    classique = np.mean([r["auc_bm25"] for r in resultats])
    gagne = sum(1 for r in resultats if r["auc_tete"] > r["auc_bm25"])
    melange = np.mean([r["auc_etiquettes_melangees"] for r in resultats])
    print(f"  moyenne : tête {tete:.3f} · BM25 {classique:.3f} · mélangé {melange:.3f} "
          f"· la tête gagne {gagne}/{len(resultats)} documents")
    if json_path is not None:
        json_path.write_text(json.dumps({
            "date": "2026-10-29", "ligne": "R0.4", "paires": int(len(y)),
            "positifs": int(y.sum()), "couches": COUCHES,
            "negatifs": "durs (même section)" if DURS else "aléatoires",
            "modele": "Qwen2.5-0.5B-Q8_0",
            "partage": "leave-one-document-out",
            "resultats": resultats,
            "moyennes": {"tete": round(float(tete), 3), "bm25": round(float(classique), 3),
                         "etiquettes_melangees": round(float(melange), 3)},
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  résultats : {json_path}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="R0.4 — la tête de survol sur états précoces.")
    ap.add_argument("--extrait", action="store_true")
    ap.add_argument("--mesure", action="store_true")
    ap.add_argument("--tout", action="store_true")
    ap.add_argument("--json", type=pathlib.Path)
    args = ap.parse_args()
    if args.extrait or args.tout:
        X, y, meta = capture()
        np.savez(CACHE, X=X, y=y, meta=np.array(meta, dtype=object))
        print(f"états capturés : {len(y)} paires ({int(y.sum())} positifs) → {CACHE}")
        return 0
    if args.mesure or args.tout:
        return mesure(args.json)
    ap.error("--extrait, --mesure ou --tout")
    return 2


if __name__ == "__main__":
    sys.exit(main())
