#!/usr/bin/env python3
"""ou_est_le_contenu.py — le moindres carrés néglige-t-il l'information de contenu ?

LE CONSTAT DU §58. Une lecture LINÉAIRE des mêmes états de réservoir **atteint** la
structure contenu/langue du professeur (séparation +0,0519 contre +0,0517) — mais
seulement avec un objectif à deux curseurs NON CONVEXE, erratique, et coûtant 0,14 de
fidélité. Donc : **les caractéristiques suffisent, c'est l'objectif qui ne les extrait
pas.**

L'HYPOTHÈSE, et elle est simple. La fidélité est un **cosinus par ligne**. Le
moindres carrés, lui, minimise une erreur **quadratique absolue**. Or la cible a une
norme de ~440 et une structure dominante commune à tout le corpus ; les écarts qui
distinguent les CONTENUS sont **petits devant cette masse commune**. En minimisant
l'erreur absolue, la lecture est donc surtout payée pour reproduire la masse commune —
et les petites composantes, celles qui portent le contenu, pèsent peu dans l'objectif.

TROIS VARIANTES, toutes CONVEXES et en forme fermée, testées contre la référence :

  A. référence       — moindres carrés ordinaires sur Y
  B. cible centrée   — on retire à chaque entrée SA propre moyenne avant d'ajuster :
                       la lecture ne peut plus se payer sur la masse commune
  C. lignes normées  — chaque ligne de Y est ramenée à la norme 1 : toutes les
                       positions pèsent pareil, les petites composantes comptent

MESURES : fidélité TEST, et surtout la SÉPARATION = S_langue − S_domaine, dont la
cible est celle du professeur.

PRÉDICTION, ÉCRITE AVANT LA MESURE : si l'hypothèse est juste, B et C doivent
**augmenter la séparation** vers celle du professeur, en coûtant de la fidélité. Le
point intéressant est de savoir si elles font **mieux que le §58** — c'est-à-dire si
elles atteignent la même séparation pour un coût de fidélité moindre — et si la courbe
est **monotone** (ce qu'un objectif convexe doit donner, et que le §58 ne donnait pas).

Usage : ou_est_le_contenu.py <cache_appr.npz> <cache_test.npz> [--neur 120]
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pont_generatif import Pont, charge, cos_lignes  # noqa: E402


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def moy_croisee(V):
    V = np.asarray(V, dtype=np.float64)
    N = np.linalg.norm(V, axis=1)
    ok = N > 1e-12
    if ok.sum() < 2:
        return []
    M = V[ok]/N[ok][:, None]
    S = M @ M.T
    iu = np.triu_indices(len(M), 1)
    return list(S[iu])


def deux_axes(noms, V):
    lang, unit = {}, {}
    for i, n in enumerate(noms):
        L, _, k = n.partition("_")
        lang.setdefault(L, {})[k] = i
        unit.setdefault(k, {})[L] = i
    sl, sd = [], []
    for par in unit.values():
        if len(par) >= 2:
            sl += moy_croisee([V[i] for i in par.values()])
    for par in lang.values():
        if len(par) >= 2:
            sd += moy_croisee([V[i] for i in par.values()])
    return float(np.mean(sl)), float(np.mean(sd))


def main():
    tr_p, te_p = sys.argv[1], sys.argv[2]
    n_neur = int(opt("--neur", 120))
    part = float(opt("--part", 0.5))
    ride, graine = 0.03, 5

    cltr, Etr, Ytr, H = charge(tr_p)
    clte, Ete, Yte, _ = charge(te_p)
    vivant = np.zeros(Ytr[0].shape[1])
    for y in Ytr:
        vivant += ((y != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(Ytr)
    garde = np.where(vivant >= part)[0]
    Ytr = [y[:, garde] for y in Ytr]
    Yte = [y[:, garde] for y in Yte]
    print(f"# {len(cltr)} entrées d'apprentissage · {len(clte)} de test · "
          f"{len(garde)} canaux")

    itr = np.arange(len(cltr))
    # DÉCOUPAGE CORRIGÉ. `itr[nt:]` supprimait le bloc entier de la première langue :
    # les entrées sont ORDONNÉES PAR LANGUE, donc sur le cache Wikipedia (de/en/fr)
    # l'ajustement ne portait que sur en et fr — deux langues au lieu de trois. On
    # ajuste sur TOUTES les entrées : le panneau hors vivier est le cache de TEST.
    iap, ival = itr, itr
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)

    P = Pont((cltr, Etr, Ytr), 0.2, graine, len(garde))
    P.quadratique = True
    P.a_min, P.a_max = 0.02, 0.8
    P.nait(n_neur, True)
    idx = np.arange(P.compte_neurones)
    Xt = P.recalcule(idx, Ete)
    At = P.phi(np.vstack(Xt))
    print(f"# réseau {P.compte_neurones} neurones · {len(P.couches)} couche(s)")

    pro = np.array([Yte[k].mean(0) for k in range(len(clte))])
    tl, td = deux_axes(clte, pro)
    print(f"\n# CIBLE — professeur : S_langue {tl:.4f} · S_domaine {td:.4f} · "
          f"SÉPARATION {tl-td:+.4f}")

    # blocs d'apprentissage, mis en forme une fois
    Ab = [P.phi(P._norm(P.X[i][:, idx])) for i in iap]
    Yb = [Ytr[i] for i in iap]

    def ajuste_et_mesure(mode, force=0.0):
        """mode : 'ref' | 'centre' | 'norme' | 'centre+norme'."""
        G = None
        D = None
        ntot = 0
        for A, Y in zip(Ab, Yb):
            Z = np.asarray(Y, dtype=np.float64)
            if "centre" in mode:
                Z = Z - Z.mean(0, keepdims=True)
            if "norme" in mode:
                Z = Z/np.maximum(np.linalg.norm(Z, axis=1, keepdims=True), 1e-9)
            A64 = np.asarray(A, dtype=np.float64)
            G = A64.T @ A64 if G is None else G + A64.T @ A64
            D = A64.T @ Z if D is None else D + A64.T @ Z
            ntot += len(A64)
        W = np.linalg.solve(G + ride*ntot*np.eye(G.shape[0]), D)
        # fidélité : on remet la moyenne de l'entrée si la cible a été centrée
        dec = 0
        pred = []
        for k in range(len(clte)):
            n = len(Yte[k])
            A = At[dec:dec+n]
            dec += n
            out = A @ W + mt
            if "norme" in mode:
                out = out/np.maximum(np.linalg.norm(out, axis=1, keepdims=True), 1e-9)
                out = out*np.linalg.norm(Yte[k], axis=1, keepdims=True)
            pred.append(out)
        ft = cos_lignes(np.vstack(pred), np.vstack(Yte))
        ours = np.array([pred[k].mean(0) for k in range(len(clte))])
        nl, nd = deux_axes(clte, ours)
        return ft, nl, nd

    # ---------------------------------------------------------------- BLANCHIMENT
    #
    # L'idée qui manquait, et elle est CONVEXE. La cible a une structure de covariance
    # très inégale : quelques directions portent presque toute l'énergie (la masse
    # commune au corpus), et les directions FAIBLES portent ce qui distingue les
    # contenus. Le moindres carrés, en erreur absolue, est payé surtout pour les
    # premières. **Blanchir la cible** — la multiplier par C^(-1/2) — égalise
    # l'importance de toutes les directions. L'ajustement reste un moindres carrés
    # ordinaire, donc CONVEXE et en forme fermée ; seule la cible change.
    #
    # On dose le blanchiment par un exposant alpha : alpha=0 est la référence,
    # alpha=1 blanchit complètement. La comparaison est donc une COURBE, pas un point.
    Yall = np.vstack([np.asarray(Yb[j], dtype=np.float64) for j in range(len(Yb))])
    Yc = Yall - Yall.mean(0, keepdims=True)
    C = (Yc.T @ Yc)/len(Yc)
    w, V = np.linalg.eigh(C)
    w = np.maximum(w, 0.0)
    print(f"\n# SPECTRE DE LA CIBLE : {len(w)} directions · "
          f"énergie de la 1re {w[-1]/w.sum():.1%} · "
          f"des 10 premières {w[-10:].sum()/w.sum():.1%}")

    def ajuste_blanchi(alpha):
        if alpha == 0.0:
            T = np.eye(len(w))
        else:
            T = (V * (np.maximum(w, 1e-12)**(-alpha/2))) @ V.T
        G = D = None
        ntot = 0
        for A, Y in zip(Ab, Yb):
            Z = (np.asarray(Y, dtype=np.float64) - mt) @ T
            A64 = np.asarray(A, dtype=np.float64)
            G = A64.T @ A64 if G is None else G + A64.T @ A64
            D = A64.T @ Z if D is None else D + A64.T @ Z
            ntot += len(A64)
        W = np.linalg.solve(G + ride*ntot*np.eye(G.shape[0]), D)
        pred = []
        dec = 0
        for k in range(len(clte)):
            n = len(Yte[k])
            A = At[dec:dec+n]
            dec += n
            pred.append((A @ W) @ T.T + mt)
        ft = cos_lignes(np.vstack(pred), np.vstack(Yte))
        ours = np.array([pred[k].mean(0) for k in range(len(clte))])
        nl, nd = deux_axes(clte, ours)
        return ft, nl, nd

    print(f"\n# {'variante':<16}{'fid TEST':>10}{'S_langue':>10}{'S_domaine':>11}"
          f"{'SÉPARATION':>12}{'vs prof':>9}")
    for mode, nom in (("ref", "A référence"), ("centre", "B cible centrée"),
                      ("norme", "C lignes normées")):
        ft, nl, nd = ajuste_et_mesure(mode)
        print(f"  {nom:<16}{ft:>10.4f}{nl:>10.4f}{nd:>11.4f}{nl-nd:>+12.4f}"
              f"{(nl-nd)-(tl-td):>+9.4f}")
    for alpha in (0.25, 0.5, 0.75, 1.0):
        ft, nl, nd = ajuste_blanchi(alpha)
        print(f"  {'D blanchiment':<14}{alpha:>4.2f}{ft:>10.4f}{nl:>10.4f}"
              f"{nd:>11.4f}{nl-nd:>+12.4f}{(nl-nd)-(tl-td):>+9.4f}")
    print(f"\n# Rappel du §58 : l'objectif à deux curseurs atteignait +0,0003 de la")
    print(f"# cible, mais au prix de 0,139 de fidélité et avec une courbe NON MONOTONE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
