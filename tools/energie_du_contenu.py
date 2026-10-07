#!/usr/bin/env python3
"""energie_du_contenu.py — peut-on retrouver l'ÉNERGIE de contenu, pas seulement son rapport ?

CE QUI MÈNE ICI. Le §87 a mesuré, hors vivier sur un panel de 6 langues, que notre pont
atteint **136 % du RAPPORT** du professeur avec **3,4 % de son énergie de contenu** et
2,5 % de son énergie de langue. Le rapport est un quotient : deux énergies qui s'effondrent
ensemble le laissent intact. Le critère qui compte est celui du §62.3 — **`P_cont` proche du
professeur ET `P_lang` qui ne le dépasse pas**.

L'HYPOTHÈSE, ET ELLE EST ANCIENNE (§58, `ou_est_le_contenu.py`). La fidélité est un cosinus
par ligne, mais l'ajustement est une erreur QUADRATIQUE ABSOLUE. La cible a une masse
commune énorme (norme ~440) et les écarts qui distinguent les contenus sont petits devant
elle. En minimisant l'erreur absolue, la lecture est payée pour reproduire la masse
commune — et les petites composantes, celles qui portent le contenu, pèsent peu.

TROIS FAMILLES DE REMÈDES, toutes CONVEXES et en forme fermée :

  A. référence          — moindres carrés ordinaires sur Y
  B. cible centrée      — on retire à chaque entrée sa propre moyenne avant d'ajuster
  C. lignes normées     — chaque ligne de Y ramenée à la norme 1 : toutes les positions
                          pèsent pareil
  D. blanchiment α      — on égalise l'importance des directions de la cible avant
                          d'ajuster ; α=0 est la référence, α=1 blanchit complètement

CE QUI EST MESURÉ, ET C'EST NOUVEAU ICI : non pas le rapport seul, mais **les deux énergies
ET leur part de celles du professeur**, plus la fidélité de test. Un remède qui monte le
rapport en écrasant les deux énergies n'est pas un remède.

Usage : energie_du_contenu.py <cache_appr.npz> <cache_test.npz> [--neur 120]
                              [--rides 0.03] [--alphas 0.25,0.5,0.75,1.0]
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pont_generatif import Pont, charge, cos_lignes  # noqa: E402


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def decompose(noms, M):
    m = M.mean(0)
    par_l, par_c = {}, {}
    for i, n in enumerate(noms):
        L, _, k = n.partition("_")
        par_l.setdefault(L, []).append(i)
        par_c.setdefault(k, []).append(i)
    comm = [k for k, idx in par_c.items() if len(idx) == len(par_l)]
    Pl = float(np.mean([np.sum((M[idx].mean(0) - m)**2) for idx in par_l.values()]))
    Pc = float(np.mean([np.sum((M[par_c[k]].mean(0) - m)**2) for k in comm]))
    return Pl, Pc, Pc/max(Pl, 1e-12)


def main():
    tr_p, te_p = sys.argv[1], sys.argv[2]
    n_neur = int(opt("--neur", 120))
    rides = [float(x) for x in opt("--rides", "0.03").split(",")]
    alphas = [float(x) for x in opt("--alphas", "0.25,0.5,0.75,1.0").split(",")]

    cltr, Etr, Ytr, _ = charge(tr_p)
    clte, Ete, Yte, _ = charge(te_p)
    vivant = np.zeros(Ytr[0].shape[1])
    for y in Ytr:
        vivant += ((y != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(Ytr)
    garde = np.where(vivant >= 0.5)[0]
    Ytr = [y[:, garde] for y in Ytr]
    Yte = [y[:, garde] for y in Yte]
    ncan = len(garde)
    itr = np.arange(len(cltr))
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)

    P = Pont((cltr, Etr, Ytr), 0.2, 5, ncan)
    P.quadratique = True
    P.a_min, P.a_max = 0.02, 0.8
    P.nait(n_neur, True)
    idx = np.arange(P.compte_neurones)
    Xt = P.recalcule(idx, Ete)
    At = P.phi(np.vstack(Xt))
    print(f"# {len(cltr)} entrées d'apprentissage · {len(clte)} de test · {ncan} canaux"
          f" · {P.compte_neurones} neurones")

    # ------------------------------------------------ la cible de référence du professeur
    pro_te = np.vstack([y.mean(0) for y in Yte])
    # le professeur sur l'APPRENTISSAGE sert d'échelle pour le blanchiment
    Yall = np.vstack([Ytr[i] for i in itr]).astype(np.float64)
    Yc = Yall - Yall.mean(0, keepdims=True)
    C = (Yc.T @ Yc)/len(Yc)
    w, V = np.linalg.eigh(C)
    w = np.maximum(w, 0.0)
    print(f"# SPECTRE DE LA CIBLE : 1re direction {w[-1]/w.sum():.1%} de l'énergie · "
          f"10 premières {w[-10:].sum()/w.sum():.1%} · "
          f"rang utile (99 %) {int(np.searchsorted(np.cumsum(np.sort(w)[::-1])/w.sum(), 0.99))+1}")

    def ajuste(ride, transforme):
        """transforme(Y) -> cible ajustée ; renvoie aussi la transformation inverse."""
        G = D = None
        ntot = 0
        for i in itr:
            A = P.phi(P._norm(P.X[i][:, idx])).astype(np.float64)
            Z = transforme(np.asarray(Ytr[i], dtype=np.float64))
            G = A.T @ A if G is None else G + A.T @ A
            D = A.T @ Z if D is None else D + A.T @ Z
            ntot += len(A)
        W = np.linalg.solve(G + ride*ntot*np.eye(G.shape[0]), D)
        return W

    def predit(W, T=None, Tn=None):
        out = []
        dec = 0
        for k in range(len(clte)):
            n = len(Yte[k])
            o = At[dec:dec+n] @ W
            dec += n
            if T is not None:          # blanchiment : on repasse par Tᵀ
                o = o @ T.T
            o = o + mt
            if Tn is not None:         # lignes normées : on rend l'échelle d'origine
                o = o/np.maximum(np.linalg.norm(o, axis=1, keepdims=True), 1e-9)
                o = o*np.linalg.norm(Yte[k], axis=1, keepdims=True)
            out.append(o)
        return out

    def mesure(nom, pred):
        ft = cos_lignes(np.vstack(pred), np.vstack(Yte))
        M = np.vstack([p.mean(0) for p in pred])
        pl, pc, rap = decompose(clte, M)
        ppl, ppc, prap = decompose(clte, pro_te)
        print(f"  {nom:<20}{ft:>9.4f}{pl:>10.1f}{pc:>10.1f}{rap:>9.3f}"
              f"{pl/ppl:>9.1%}{pc/ppc:>9.1%}")

    ppl, ppc, prap = decompose(clte, pro_te)
    print(f"\n# {'variante':<20}{'fid TEST':>9}{'P_lang':>10}{'P_cont':>10}"
          f"{'RAPPORT':>9}{'% P_lang':>9}{'% P_cont':>9}")
    print(f"  {'PROFESSEUR':<20}{'—':>9}{ppl:>10.1f}{ppc:>10.1f}{prap:>9.3f}"
          f"{'100 %':>9}{'100 %':>9}")

    ride = rides[0]
    for mode, nom, tr, T, Tn in (
            ("ref", "A référence", lambda Z: Z, None, None),
            ("centre", "B cible centrée", lambda Z: Z - Z.mean(0, keepdims=True), None, None),
            ("norme", "C lignes normées",
             lambda Z: Z/np.maximum(np.linalg.norm(Z, axis=1, keepdims=True), 1e-9),
             None, True)):
        W = ajuste(ride, tr)
        mesure(nom, predit(W, T, Tn))

    for a in alphas:
        T = np.eye(len(w)) if a == 0 else (V*(np.maximum(w, 1e-12)**(-a/2))) @ V.T
        W = ajuste(ride, lambda Z, T=T: (Z - mt) @ T)
        mesure(f"D blanchiment {a:.2f}", predit(W, T, None))

    if len(rides) > 1:
        print()
        for r in rides:
            W = ajuste(r, lambda Z: Z)
            mesure(f"A référence r={r}", predit(W, None, None))

    print(f"\n# « % P_lang » et « % P_cont » : la part de l'énergie du professeur.")
    print(f"# Un remède qui monte le RAPPORT en écrasant les DEUX énergies n'en est pas un")
    print(f"# (§62.3) : c'est le quotient de deux petites choses.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
