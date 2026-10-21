#!/usr/bin/env python3
"""pas_de_pensee.py — ÉTAGE 2 : un PAS DE PENSÉE appris (l'état de la phrase i prédit-il l'état de la phrase i+1 ?).

POURQUOI ✓✓. La mesure 80 a montré que le sens de la phrase est **partagé et positionné** à mi-profondeur ✓✓. La
question de l'étage 2 est maintenant **dynamique** : peut-on apprendre un **opérateur** F tel que
`F(état de la phrase i) ≈ état de la phrase i+1` ? ✓✓ Si oui, on peut **itérer** la pensée sans émettre de jetons —
c'est le « penser sans verbaliser » du chapitre 5 ✓✓. La nuit du 16 avait trouvé une **falaise** dès le premier pas
sur un petit modèle ✗✗ ; on la reteste sur un modèle moderne, avec des **phrases alignées** ✓✓.

LE DISPOSITIF ✓✓ : les états Verne (200 phrases, 50 séries de 4, 3 B), déjà extraits ✓. On apprend F (ridge) sur
les transitions **d'une série à la suivante** (150 transitions), on le teste sur des séries **tenues à part** ✓✓.
  · **un pas** : cosinus et retrieval de la phrase suivante (parmi les 4 de la série, hasard 25 %) ✓✓ ;
  · **itération** : F¹, F², F³ depuis la phrase 0, cosinus et retrieval à chaque pas ✓✓ ;
  · **baselines** : l'identité (F = I) et la moyenne ✓✗ ;
  · **contrôle négatif** : F appris sur des transitions **mélangées** ✓✓.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np


def norm(x):
    return x / np.maximum(1e-9, np.linalg.norm(x, axis=1, keepdims=True))


def cos(a, b):
    return float(np.mean(np.sum(norm(a) * norm(b), 1)))


def retrieval(pred, cand):
    """Pour chaque ligne de pred, la bonne ligne de cand (même index) est-elle la plus proche ?"""
    return float(np.mean(np.argmax(norm(pred) @ norm(cand).T, 1) == np.arange(len(pred))))


def fit(X, Y, lam):
    Xb = np.hstack([X, np.ones((len(X), 1), np.float32)])
    return np.linalg.solve(Xb.T @ Xb + lam * np.eye(Xb.shape[1], dtype=np.float32), Xb.T @ Y)


def apply(X, W):
    return np.hstack([X, np.ones((len(X), 1), np.float32)]) @ W


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--etats", default="data/composition-verne-etats.npz")
    ap.add_argument("--sortie", default="reports/pas-de-pensee.json")
    a = ap.parse_args()
    z = np.load(a.etats, allow_pickle=False)
    couches = [int(c) for c in z["couches"]]
    noms = [str(s) for s in z["noms"]]
    series = {}
    for i, s in enumerate(noms):
        k, j = s.split("|")
        series.setdefault(int(k), {})[int(j)] = i
    cles = sorted(series)
    rng = np.random.default_rng(1234)
    rng.shuffle(cles)
    n_tr = int(0.7 * len(cles))
    train_s, test_s = cles[:n_tr], cles[n_tr:]
    res = []
    for L in couches:
        E = z[f"L{L}"].astype(np.float32)
        # transitions (i -> i+1) dans les séries d'entraînement
        Xtr, Ytr, Xte, Yte, prem = [], [], [], [], []
        for k in train_s:
            for j in range(3):
                Xtr.append(E[series[k][j]]); Ytr.append(E[series[k][j + 1]])
        for k in test_s:
            prem.append(E[series[k][0]])
            for j in range(3):
                Xte.append(E[series[k][j]]); Yte.append(E[series[k][j + 1]])
        Xtr, Ytr = np.array(Xtr), np.array(Ytr)
        # λ par validation interne (10 % des transitions)
        nv = max(10, len(Xtr) // 5)
        lam = max((0.1, 1.0, 10.0, 100.0, 1000.0),
                  key=lambda l: cos(apply(Xtr[-nv:], fit(Xtr[:-nv], Ytr[:-nv], l)), Ytr[-nv:]))
        W = fit(Xtr, Ytr, lam)
        # contrôle négatif : transitions mélangées
        mel = rng.permutation(len(Xtr))
        Wn = fit(Xtr, Ytr[mel], lam)
        # un pas
        pred1 = apply(np.array(Xte), W)
        cos1 = cos(pred1, np.array(Yte))
        r1 = retrieval(pred1, np.array(Yte))
        neg1 = retrieval(apply(np.array(Xte), Wn), np.array(Yte))
        # itération depuis la phrase 0 de chaque série de test
        S0 = np.array(prem)
        cos_id = [cos(S0, np.array([E[series[k][j + 1]] for k in test_s]))]
        cos_it = []
        ret_it = []
        for pas in range(1, 4):
            if pas == 1:
                cur = apply(S0, W)
            else:
                cur = apply(cur, W)
            cibles = np.array([E[series[k][min(pas, 3)]] for k in test_s])
            cos_it.append(cos(cur, cibles))
            # retrieval parmi les 4 phrases de la série : la bonne position est min(pas,3)
            justes = 0
            for idx, k in enumerate(test_s):
                cand = np.stack([E[series[k][j]] for j in range(4)])
                sims = norm(cur[idx:idx + 1]) @ norm(cand).T
                justes += int(np.argmax(sims) == min(pas, 3))
            ret_it.append(justes / len(test_s))
        res.append({"couche": int(L), "lambda": lam, "cos_un_pas": round(cos1, 4),
                    "retrieval_un_pas": round(r1, 4), "retrieval_negatif": round(neg1, 4),
                    "cos_identite": round(cos_id[0], 4),
                    "cos_iteration": [round(x, 4) for x in cos_it],
                    "retrieval_iteration": [round(x, 4) for x in ret_it]})
        print(f"  couche {L:2d} · un pas cos {cos1:.3f} ret {r1:.3f} · itération ret {ret_it} · identité cos {cos_id[0]:.3f}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({"n_series_train": len(train_s), "n_series_test": len(test_s),
                                                  "resultats": res}, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
