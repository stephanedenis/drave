#!/usr/bin/env python3
"""pas_de_pensee_corrige.py — ÉTAGE 2 : le pas de pensée, sur la CARTE DE LIGNES CORRECTE.

POURQUOI ✓✓. Les mesures 82-88, 108-110 ont lu les états Verne avec `noms` : 200 noms pour 400 lignes. Or
`composition_verne.py` écrit **deux** états par phrase (FR puis EN) et n'un nomme qu'**un** : les « séries » de la
mesure 82 étaient donc `fr0, en0, fr1, en1` — des **paires de traduction**, pas quatre phrases consécutives. Le
« pas de pensée » appris sur ces transitions est un opérateur de **traduction**, et la falaise au troisième pas est
un artefact de l'alternance des langues ✗✗.

CE QU'ON MESURE ✓✓, sur la carte correcte (phrase i → ligne 2i pour le FR, 2i+1 pour l'EN) :
  1. **un pas** : cosinus et retrieval de la phrase suivante (global 45 candidats, hasard 2,2 % ; et parmi les 4 de
     la série, hasard 25 %) ✓✓ ;
  2. **itération** : F¹, F², F³ depuis la phrase 0, retrieval parmi les 4 phrases de la série ✓✓ ;
  3. **baselines** : identité, prédicteur de la moyenne (le meilleur opérateur constant), contrôle négatif
     (transitions mélangées) ✓✓ ;
  4. **objectif contrastif** : un F linéaire entraîné à *discriminer* la bonne suite (InfoNCE) au lieu de régresser
     dessus — si le retrieval monte, l'information était dans l'état et l'objectif MSE était le défaut ✓✓ ;
  5. **effondrement** : cosinus moyen entre les sorties de F (1,0 = sortie constante = régression vers la moyenne) ✓✓.

CE QUE CE N'EST PAS ✗ : ce n'est pas une mesure de « pensée » — c'est le test le plus propre du **pas appris** sur
des états de modèle, avec les contrôles qui manquaient.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np


def norm(x):
    return x / np.maximum(1e-9, np.linalg.norm(x, axis=1, keepdims=True))


def cos(a, b):
    return float(np.mean(np.sum(norm(a) * norm(b), 1)))


def retrieval(pred, cand):
    """Chaque ligne de pred doit être la plus proche de la ligne de cand de même index."""
    return float(np.mean(np.argmax(norm(pred) @ norm(cand).T, 1) == np.arange(len(pred))))


def fit(X, Y, lam):
    Xb = np.hstack([X, np.ones((len(X), 1), np.float32)])
    W = np.linalg.solve(Xb.T @ Xb + lam * np.eye(Xb.shape[1], dtype=np.float32), Xb.T @ Y)
    return W


def apply(X, W):
    return np.hstack([X, np.ones((len(X), 1), np.float32)]) @ W


def effondrement(A):
    """Cosinus moyen entre les sorties, hors diagonale (1,0 = toutes identiques)."""
    n = norm(A)
    S = n @ n.T
    m = ~np.eye(len(A), dtype=bool)
    return float(S[m].mean())


def contraste(Xtr, Ytr, Xte, Yte, epochs=400, lr=1e-3, tau=0.05, graine=1234):
    """F linéaire entraîné par InfoNCE : discriminer la bonne suite parmi les paires du lot."""
    import torch
    torch.manual_seed(graine)
    Xt = torch.from_numpy(Xtr); Yt = torch.from_numpy(Ytr)
    Xe = torch.from_numpy(Xte); Ye = torch.from_numpy(Yte)
    d = Xt.shape[1]
    W = torch.zeros(d, d, requires_grad=True)
    b = torch.zeros(d, requires_grad=True)
    opt = torch.optim.Adam([W, b], lr=lr)
    n = len(Xt)
    for _ in range(epochs):
        F = Xt @ W + b
        logits = (torch.nn.functional.normalize(F, dim=1) @ torch.nn.functional.normalize(Yt, dim=1).T) / tau
        perte = torch.nn.functional.cross_entropy(logits, torch.arange(n))
        opt.zero_grad(); perte.backward(); opt.step()
    with torch.no_grad():
        pred = (Xe @ W + b).numpy()
    return pred, float(perte.detach())


def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--etats", required=True)
    ap.add_argument("--sortie", required=True)
    ap.add_argument("--par-serie", type=int, default=4)
    ap.add_argument("--epochs", type=int, default=400, help="époques du contraste linéaire")
    a = ap.parse_args()
    z = np.load(a.etats, allow_pickle=False)
    couches = [int(c) for c in z["couches"]]
    noms = [str(s) for s in z["noms"]]
    E0 = z[f"L{couches[0]}"]
    n_lignes, d = E0.shape
    n_phrases = n_lignes // 2
    n_series = n_phrases // a.par_serie
    assert n_lignes % 2 == 0 and n_phrases % a.par_serie == 0, (n_lignes, n_phrases)
    assert len(noms) == n_phrases, f"noms {len(noms)} ≠ phrases {n_phrases} : la carte des lignes est cassée"
    rng = np.random.default_rng(1234)
    cles = list(range(n_series)); rng.shuffle(cles)
    n_tr = int(0.7 * n_series)
    tr, te = cles[:n_tr], cles[n_tr:]
    res = []
    for L in couches:
        E = z[f"L{L}"].astype(np.float32)
        F = E[0::2]; A = E[1::2]          # phrase i : FR = 2i, EN = 2i+1
        assert len(F) == n_phrases
        i_tr = [k * a.par_serie + j for k in tr for j in range(a.par_serie - 1)]
        i_te = [k * a.par_serie + j for k in te for j in range(a.par_serie - 1)]
        Xtr = np.array([F[i] for i in i_tr]); Ytr = np.array([F[i + 1] for i in i_tr])
        Xte = np.array([F[i] for i in i_te]); Yte = np.array([F[i + 1] for i in i_te])
        # λ par validation interne (les 20 % dernières transitions du train)
        nv = max(10, len(Xtr) // 5)
        lam = max((0.1, 1.0, 10.0, 100.0, 1000.0),
                  key=lambda l: cos(apply(Xtr[-nv:], fit(Xtr[:-nv], Ytr[:-nv], l)), Ytr[-nv:]))
        W = fit(Xtr, Ytr, lam)
        Wneg = fit(Xtr, Ytr[rng.permutation(len(Ytr))], lam)
        pred1 = apply(Xte, W)
        predn = apply(Xte, Wneg)
        # identité et moyenne
        cerr = F[[k * a.par_serie for k in te]]
        S0 = np.array([F[k * a.par_serie] for k in te])
        cibles = [np.stack([F[k * a.par_serie + j] for j in range(a.par_serie)]) for k in te]
        # itération + retrieval dans la série
        it_ret = []
        cur = S0.copy()
        for pas in range(1, 4):
            cur = apply(cur, W)
            justes = 0
            for idx, cand in enumerate(cibles):
                justes += int(np.argmax(norm(cur[idx:idx + 1]) @ norm(cand).T) == min(pas, a.par_serie - 1))
            it_ret.append(justes / len(te))
        # un pas, retrieval dans la série (4 candidats)
        justes = 0
        for idx, cand in enumerate(cibles):
            justes += int(np.argmax(norm(pred1[idx:idx + 1]) @ norm(cand).T) == 1)
        ret_serie = justes / len(te)
        # contrastif
        predc, perte = contraste(Xtr, Ytr, Xte, Yte, epochs=a.epochs)
        res.append({
            "couche": int(L), "lambda": lam,
            "cos_un_pas": round(cos(pred1, Yte), 4),
            "cos_identite": round(cos(Xte, Yte), 4),
            "cos_moyenne": round(cos(np.repeat(Ytr.mean(0, keepdims=True), len(Yte), 0), Yte), 4),
            "effondrement": round(effondrement(pred1), 4),
            "retrieval_un_pas_global": round(retrieval(pred1, Yte), 4),
            "retrieval_un_pas_serie": round(ret_serie, 4),
            "retrieval_negatif": round(retrieval(predn, Yte), 4),
            "retrieval_iteration": [round(x, 4) for x in it_ret],
            "contrastif_cos": round(cos(predc, Yte), 4),
            "contrastif_retrieval_global": round(retrieval(predc, Yte), 4),
            "contrastif_perte": round(perte, 4),
        })
        print(f"  L{L:<2} cos {res[-1]['cos_un_pas']:.3f} (id {res[-1]['cos_identite']:.3f}, moy "
              f"{res[-1]['cos_moyenne']:.3f}) · ret global {res[-1]['retrieval_un_pas_global']:.3f} · "
              f"série {ret_serie:.3f} · nég {res[-1]['retrieval_negatif']:.3f} · "
              f"iter {it_ret} · contrastif {res[-1]['contrastif_retrieval_global']:.3f}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({
        "etats": a.etats, "n_series": n_series, "n_series_train": len(tr), "n_series_test": len(te),
        "n_phrases": n_phrases, "hasard_global": round(1.0 / len(i_te), 4),
        "hasard_serie": round(1.0 / a.par_serie, 4), "resultats": res}, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
