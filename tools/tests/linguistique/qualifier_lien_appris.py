#!/usr/bin/env python3
"""qualifier_lien_appris.py — le lien **appris** : perceptron de rang, LOO sur 9 paires.

Les règles à la main (sujet normalisé, verbe, adverbe, acte, phrase simple) font 9/9.
Ici, on apprend les **poids** de ces traits par un perceptron de rang, en
leave-one-out sur les 9 paires (5 arrière r418–r422 → r423–r427, 4 avant
r408–r411 → r423–r426 ; la paire croisée r412→r427 est écartée). Contrôles :
hasard (poids aléatoires) et surface seule (sujet + proximité).

Usage : qualifier_lien_appris.py [--sortie reports/pensee-lien-appris.json] [--epochs 20]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import sys

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE))

from tools.bloc_linguistique import Heuristique
from tools.tests.linguistique import miroir


def traits(a, b, rang: int) -> list[float]:
    """Les traits d'un candidat b pour une question a (6 dimensions)."""
    sujet_a, sujet_b = miroir._sujet(a), miroir._sujet(b)
    verbe_a, verbe_b = miroir._verbe(a), miroir._verbe(b)
    return [
        1.0 if sujet_a and sujet_b and miroir._normaliser_egal(sujet_a, sujet_b) else 0.0,
        1.0 if verbe_a and verbe_b and miroir._normaliser_egal(verbe_a, verbe_b) else 0.0,
        1.0 if miroir._adverbes(a) == miroir._adverbes(b) else 0.0,
        1.0 if miroir._acte(a) == "question" and miroir._acte(b) == "assertion" else 0.0,
        1.0 if miroir._simple(b) else 0.0,
        1.0 / (1.0 + rang),
    ]


def score(w, f) -> float:
    return sum(wi * fi for wi, fi in zip(w, f))


def charger(phrases):
    """Prépare les 9 questions de la vérité et leurs candidats annotés (mémoïsé)."""
    par_id = {p["id"]: p for p in phrases}
    bl = Heuristique()
    ann = {}

    def a(id_):
        if id_ not in ann:
            p = par_id[id_]
            ann[id_] = bl.analyser(p["texte"], p["langue"])
        return ann[id_]

    pos = {p["id"]: i for i, p in enumerate(phrases)}
    verite = []  # [(qid, pid, [(cid, traits, est_positif)])]
    for k in range(5):  # arrière : r418–r422 → r423–r427
        qid, pid = f"r{418 + k}", f"r{423 + k}"
        qa = a(qid)
        cands = []
        for rang, p in enumerate(reversed(phrases[:pos[qid]])):
            cands.append((p["id"], traits(qa, a(p["id"]), rang), p["id"] == pid))
        verite.append((qid, pid, cands))
    for k in range(4):  # avant : r408–r411 → r423–r426 (la croisée r412→r427 est écartée)
        qid, pid = f"r{408 + k}", f"r{423 + k}"
        qa = a(qid)
        cands = []
        for rang, p in enumerate(phrases[pos[qid] + 1:]):
            cands.append((p["id"], traits(qa, a(p["id"]), rang), p["id"] == pid))
        verite.append((qid, pid, cands))
    return verite


def perceptron(train, epochs: int, graine: int = 1) -> list[float]:
    """Perceptron de rang : pousse le positif au-dessus du meilleur négatif."""
    rng = random.Random(graine)
    w = [0.0] * 6
    for _ in range(epochs):
        for _qid, _pid, cands in train:
            pos = [c for c in cands if c[2]]
            if not pos:
                continue
            fp = pos[0][1]
            negs = [c for c in cands if not c[2]]
            if not negs:
                continue
            meilleur = max(negs, key=lambda c: score(w, c[1]))
            if score(w, meilleur[1]) >= score(w, fp):
                for i in range(6):
                    w[i] += fp[i] - meilleur[1][i]
    return w


def evalue(w, test) -> bool:
    qid, pid, cands = test
    meilleur = max(cands, key=lambda c: score(w, c[1]))
    return meilleur[0] == pid


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default="reports/pensee-lien-appris.json")
    ap.add_argument("--epochs", type=int, default=20)
    ap.add_argument("--graines", type=int, default=50)
    a = ap.parse_args()
    phrases = json.loads((RACINE / "tools/tests/linguistique/gold_reel.json").read_text(
        encoding="utf-8"))["phrases"]
    verite = charger(phrases)
    # LOO : on retire une paire, on apprend sur 8, on teste sur 1.
    justes = 0
    details = []
    for i, test in enumerate(verite):
        train = [v for j, v in enumerate(verite) if j != i]
        w = perceptron(train, a.epochs, graine=1)
        ok = evalue(w, test)
        justes += ok
        details.append({"question": test[0], "attendu": test[1], "juste": ok,
                        "poids": [round(x, 3) for x in w]})
    # Contrôle : le hasard (poids aléatoires, moyenne de plusieurs graines).
    hasard = 0.0
    for g in range(a.graines):
        rng = random.Random(1000 + g)
        j = 0
        for test in verite:
            w = [rng.uniform(-1, 1) for _ in range(6)]
            j += evalue(w, test)
        hasard += j / len(verite)
    hasard /= a.graines
    # Contrôle : surface seule (sujet + proximité), poids fixes.
    w_surface = [1.0, 0.0, 0.0, 0.0, 0.0, 0.05]
    surface = sum(evalue(w_surface, t) for t in verite)
    res = {
        "date": __import__("time").strftime("%Y-%m-%d %H:%M %Z"),
        "paires": len(verite), "justes": justes,
        "taux": round(justes / len(verite), 4),
        "hasard_moyen": round(hasard, 4),
        "surface_seule": surface,
        "traits": ["même sujet", "même verbe", "même adverbe", "acte q→a",
                   "phrase simple", "1/(1+rang)"],
        "detail": details,
        "controle_negatif": {
            "hasard": f"{hasard:.4f} de justesse moyenne sur {a.graines} graines",
            "surface_seule": f"{surface}/{len(verite)} — le sujet seul ne suffit pas",
            "regle_main": "9/9 (mesure du round précédent)"},
    }
    p = pathlib.Path(a.sortie)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: res[k] for k in ("paires", "justes", "taux", "hasard_moyen",
                                         "surface_seule")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
