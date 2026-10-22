#!/usr/bin/env python3
"""pas_de_pensee_non_lineaire.py — ÉTAGE 2 : l'état d'une phrase contient-il la phrase SUIVANTE ?

POURQUOI ✓✓. La mesure corrigée (113) montre que l'opérateur **linéaire** n'apprend pas la transition : il prédit la
**moyenne** (effondrement 0,93-0,99, retrieval au hasard). Deux explications restent ✗✓ :
  · **l'objectif** (régression MSE) écrase la discrimination → un objectif **contrastif** devrait la rendre ;
  · **l'information** n'est pas dans l'état d'une seule phrase → aucun opérateur, linéaire ou non, ne peut la
    retrouver.

CE QU'ON MESURE ✓✓ : un MLP (d → cache → d, GELU) entraîné par **InfoNCE** à retrouver la phrase suivante parmi les
paires du lot, évalué par retrieval **hors entraînement** (45 candidats, hasard 2,2 % ; et parmi les 4 de la série,
hasard 25 %), contre le **contrôle négatif** (cibles mélangées) ✓✓. 3 graines, moyenne ± écart-type ✓✓.

CE QUE CHAQUE ISSUE VEUT DIRE ✓✓ :
  · retrieval **au-dessus du hasard** → l'information est là, l'objectif linéaire était le défaut ✓✓ ;
  · retrieval **au hasard** → la phrase suivante n'est pas une fonction de l'état de la phrase courante : le « pas »
    n'est pas un opérateur sur un état de phrase, il faut un état qui porte le **plan** de la série ✓✓.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np
import torch
import torch.nn as nn


def norm(x):
    return x / np.maximum(1e-9, np.linalg.norm(x, axis=1, keepdims=True))


def cos(a, b):
    return float(np.mean(np.sum(norm(a) * norm(b), 1)))


def retrieval(pred, cand):
    return float(np.mean(np.argmax(norm(pred) @ norm(cand).T, 1) == np.arange(len(pred))))


def effondrement(A):
    n = norm(A)
    S = n @ n.T
    m = ~np.eye(len(A), dtype=bool)
    return float(S[m].mean())


class MLP(nn.Module):
    def __init__(self, d, cache):
        super().__init__()
        self.reseau = nn.Sequential(nn.Linear(d, cache), nn.GELU(), nn.Linear(cache, d))

    def forward(self, x):
        return self.reseau(x)


def entrainer(Xtr, Ytr, cache, epochs, lr, graine, tau=0.05, lot=0):
    torch.manual_seed(graine)
    X = torch.from_numpy(Xtr); Y = torch.from_numpy(Ytr)
    m = MLP(X.shape[1], cache)
    opt = torch.optim.AdamW(m.parameters(), lr=lr, weight_decay=1e-4)
    n = len(X)
    generateur = torch.Generator().manual_seed(graine)
    perte = torch.tensor(0.0)
    for _ in range(epochs):
        if lot and lot < n:
            ordre = torch.randperm(n, generator=generateur)
            for deb in range(0, n, lot):
                idx = ordre[deb:deb + lot]
                F = m(X[idx])
                logits = (torch.nn.functional.normalize(F, dim=1) @ torch.nn.functional.normalize(Y[idx], dim=1).T) / tau
                perte = torch.nn.functional.cross_entropy(logits, torch.arange(len(idx)))
                opt.zero_grad(); perte.backward(); opt.step()
        else:
            F = m(X)
            logits = (torch.nn.functional.normalize(F, dim=1) @ torch.nn.functional.normalize(Y, dim=1).T) / tau
            perte = torch.nn.functional.cross_entropy(logits, torch.arange(n))
            opt.zero_grad(); perte.backward(); opt.step()
    return m, float(perte.detach())


def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--etats", required=True)
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--cache", type=int, default=512)
    ap.add_argument("--epochs", type=int, default=600)
    ap.add_argument("--lot", type=int, default=0, help="paires par lot (0 = lot complet)")
    ap.add_argument("--graines", type=int, default=3)
    ap.add_argument("--par-serie", type=int, default=4)
    a = ap.parse_args()
    z = np.load(a.etats, allow_pickle=False)
    couches = [int(c) for c in z["couches"]]
    E0 = z[f"L{couches[0]}"]
    n_lignes = E0.shape[0]
    n_phrases = n_lignes // 2
    n_series = n_phrases // a.par_serie
    assert n_lignes % 2 == 0 and n_phrases % a.par_serie == 0, (n_lignes, n_phrases)
    rng = np.random.default_rng(1234)
    cles = list(range(n_series)); rng.shuffle(cles)
    n_tr = int(0.7 * n_series)
    tr, te = cles[:n_tr], cles[n_tr:]
    i_tr = [k * a.par_serie + j for k in tr for j in range(a.par_serie - 1)]
    i_te = [k * a.par_serie + j for k in te for j in range(a.par_serie - 1)]
    res = []
    for L in couches:
        E = z[f"L{L}"].astype(np.float32)
        F = E[0::2]
        Xtr = np.array([F[i] for i in i_tr]); Ytr = np.array([F[i + 1] for i in i_tr])
        Xte = np.array([F[i] for i in i_te]); Yte = np.array([F[i + 1] for i in i_te])
        cibles = [np.stack([F[k * a.par_serie + j] for j in range(a.par_serie)]) for k in te]
        mesures = {"juste": [], "serie": [], "cos": [], "eff": [], "neg": [], "neg_serie": [], "perte": []}
        for g in range(a.graines):
            m, perte = entrainer(Xtr, Ytr, a.cache, a.epochs, 1e-3, graine=1000 + g, lot=a.lot)
            with torch.no_grad():
                pred = m(torch.from_numpy(Xte)).numpy()
            justes = sum(int(np.argmax(norm(pred[idx:idx + 1]) @ norm(c).T) == 1)
                         for idx, c in enumerate(cibles))
            mesures["juste"].append(retrieval(pred, Yte))
            mesures["serie"].append(justes / len(te))
            mesures["cos"].append(cos(pred, Yte))
            mesures["eff"].append(effondrement(pred))
            mesures["perte"].append(perte)
            mel = rng.permutation(len(Ytr))
            mn, _ = entrainer(Xtr, Ytr[mel], a.cache, a.epochs, 1e-3, graine=2000 + g, lot=a.lot)
            with torch.no_grad():
                predn = mn(torch.from_numpy(Xte)).numpy()
            mesures["neg"].append(retrieval(predn, Yte))
            mesures["neg_serie"].append(sum(int(np.argmax(norm(predn[idx:idx + 1]) @ norm(c).T) == 1)
                                            for idx, c in enumerate(cibles)) / len(te))
        moy = {k: float(np.mean(v)) for k, v in mesures.items()}
        ect = {k: float(np.std(v)) for k, v in mesures.items()}
        res.append({"couche": int(L), "moyenne": {k: round(v, 4) for k, v in moy.items()},
                    "ecart_type": {k: round(v, 4) for k, v in ect.items()}})
        print(f"  L{L:<2} retrieval global {moy['juste']:.3f}±{ect['juste']:.3f} · série "
              f"{moy['serie']:.3f}±{ect['serie']:.3f} · cos {moy['cos']:.3f} · effondrement {moy['eff']:.3f} · "
              f"négatif {moy['neg']:.3f} · perte {moy['perte']:.2f}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({
        "etats": a.etats, "n_series": n_series, "n_series_train": len(tr), "n_series_test": len(te),
        "n_phrases": n_phrases, "hasard_global": round(1.0 / len(i_te), 4),
        "hasard_serie": round(1.0 / a.par_serie, 4), "graines": a.graines, "epochs": a.epochs,
        "cache": a.cache, "resultats": res}, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
