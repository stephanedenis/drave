#!/usr/bin/env python3
"""position_multilingue.py — ÉTAGE 2 : la STRUCTURE d'une série (sa position) est-elle indépendante de la langue ?

POURQUOI ✓✓. La mesure 80 a montré que le sens d'une phrase est partagé entre le FR et l'EN (retrieval 0,61) et que
sa **position** dans la série est retrouvée (ordre 0,84) — mais toujours **dans la même langue** : on aligne FR→EN
par un pont, on ne teste pas si la **structure** elle-même est commune. C'est la question de l'étage 2 : une pensée
abstraite, indépendante de la langue, doit porter la **position** (le rôle dans la série) de la même façon dans les
deux langues ✓✓.

CE QU'ON MESURE ✓✓, sur les séries Verne FR/EN (8 phrases) :
  1. une **sonde linéaire** de position (0..7) entraînée sur le **FR**, testée sur le **FR** (référence) puis sur
     l'**EN** (transfert) — et réciproquement ✓✓ ; hasard = 1/8 = 12,5 % ✓✓ ;
  2. le **contrôle négatif** : étiquettes mélangées ✓✓ ;
  3. une **sonde de langue** (FR vs EN) sur les mêmes états : la langue est-elle, elle, très lisible ? ✓✓.

CE QUE CHAQUE ISSUE VEUT DIRE ✓✓ :
  · transfert **au-dessus du hasard** → la structure de position est **commune** aux langues : il y a bien un niveau
    abstrait, indépendant de la langue ✓✓ ;
  · transfert **au hasard** alors que la sonde de langue est haute → la structure reste **langue-spécifique** : le pont
    aligne le contenu, pas la structure ✓✗.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np


def standardiser(Xtr, Xte):
    moy = Xtr.mean(0, keepdims=True)
    ect = Xtr.std(0, keepdims=True) + 1e-6
    return (Xtr - moy) / ect, (Xte - moy) / ect


def sonde(Xtr, ytr, Xte, yte, classes, lam=10.0):
    """Ridge one-hot : classe prédite = argmax."""
    Y = np.eye(classes, dtype=np.float32)[ytr]
    Xb = np.hstack([Xtr, np.ones((len(Xtr), 1), np.float32)])
    W = np.linalg.solve(Xb.T @ Xb + lam * np.eye(Xb.shape[1], dtype=np.float32), Xb.T @ Y)
    pred = np.argmax(np.hstack([Xte, np.ones((len(Xte), 1), np.float32)]) @ W, 1)
    return float(np.mean(pred == yte))


def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--etats", required=True)
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--par-serie", type=int, default=8)
    ap.add_argument("--couches", default="6,12,18,24,30")
    a = ap.parse_args()
    z = np.load(a.etats, allow_pickle=False)
    couches = [int(c) for c in a.couches.split(",")]
    E0 = z[f"L{couches[0]}"]
    n_phrases = E0.shape[0] // 2
    T = a.par_serie
    n_series = n_phrases // T
    rng = np.random.default_rng(1234)
    cles = np.arange(n_series); rng.shuffle(cles)
    n_tr = int(0.7 * n_series)
    tr, te = cles[:n_tr], cles[n_tr:]
    res = []
    for L in couches:
        E = z[f"L{L}"].astype(np.float32)
        F = E[0::2].reshape(n_series, T, -1)
        A = E[1::2].reshape(n_series, T, -1)
        # étiquettes de position : 0..T-1 pour chaque phrase
        y = np.tile(np.arange(T), n_series)
        Ftr = F[tr].reshape(-1, F.shape[2]); Fte = F[te].reshape(-1, F.shape[2])
        Atr = A[tr].reshape(-1, A.shape[2]); Ate = A[te].reshape(-1, A.shape[2])
        ytr = np.tile(np.arange(T), len(tr)); yte = np.tile(np.arange(T), len(te))
        # statistiques du côté qui entraîne : le transfert ne doit pas re-calibrer la langue cible
        mf, sf = Ftr.mean(0), Ftr.std(0) + 1e-6
        ma, sa = Atr.mean(0), Atr.std(0) + 1e-6
        Ftr_s, Fte_s = (Ftr - mf) / sf, (Fte - mf) / sf
        Atr_s, Ate_s = (Atr - ma) / sa, (Ate - ma) / sa
        fr_fr = sonde(Ftr_s, ytr, Fte_s, yte, T)
        fr_en = sonde(Ftr_s, ytr, (Ate - mf) / sf, yte, T)
        en_en = sonde(Atr_s, ytr, Ate_s, yte, T)
        en_fr = sonde(Atr_s, ytr, (Fte - ma) / sa, yte, T)
        # contrôle : étiquettes mélangées
        mel = rng.permutation(len(ytr))
        neg = sonde(Ftr_s, ytr[mel], Ate_s, yte, T)
        # sonde de langue (FR vs EN), phrases appariées
        Xl = np.vstack([Ftr_s, (Atr - mf) / sf]); yl = np.array([0] * len(Ftr_s) + [1] * len(Atr_s))
        Xl_te = np.vstack([Fte_s, (Ate - mf) / sf]); yl_te = np.array([0] * len(Fte_s) + [1] * len(Ate_s))
        langue = sonde(Xl, yl, Xl_te, yl_te, 2)
        res.append({"couche": int(L), "fr_fr": round(fr_fr, 4), "fr_en": round(fr_en, 4),
                    "en_en": round(en_en, 4), "en_fr": round(en_fr, 4), "negatif": round(neg, 4),
                    "langue": round(langue, 4)})
        print(f"  L{L:<2} FR→FR {fr_fr:.3f} · FR→EN {fr_en:.3f} · EN→EN {en_en:.3f} · EN→FR {en_fr:.3f} · "
              f"négatif {neg:.3f} · langue {langue:.3f} (hasard position {1 / T:.3f})")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({
        "etats": a.etats, "n_series": n_series, "n_series_train": len(tr), "n_series_test": len(te),
        "par_serie": T, "hasard_position": round(1.0 / T, 4), "resultats": res}, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
