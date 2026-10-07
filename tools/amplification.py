#!/usr/bin/env python3
"""amplification.py — notre sortie est-elle ÉCRASÉE VERS LA MOYENNE ?

L'OBSERVATION QUI N'AVAIT PAS ÉTÉ FAITE. Le §57 a montré que notre sortie ne sépare
plus contenu et langue (S_langue ≈ S_domaine ≈ 0,99 sur Wikipedia), là où le
professeur, si (0,9454 / 0,8937 · écart +0,052). Quatre objectifs ont été essayés
pour corriger cela (§58, §59), tous écartés.

Mais une chose n'a jamais été regardée : **notre sortie est-elle seulement plus PETITE
que sa cible, autour du même point ?**

La lecture prédit `O = φ(X)·W + mt`, où `mt` est la moyenne globale des cibles. Si les
caractéristiques ne peuvent pas produire toute l'amplitude de la cible, le moindres
carrés **rétrécit** la prédiction vers la moyenne — c'est le phénomène classique de
régression vers la moyenne. Or `mt` est **le même pour toutes les entrées** : une
prédiction dominée par `mt` a donc des moyennes par entrée presque identiques, ce qui
produit exactement le tableau du §57 — `S_langue ≈ S_domaine ≈ 1`.

LE TEST, et il est trivial. On écrit la sortie comme `mt + α·(O − mt)` et on balaie α :

    α = 1   la prédiction telle quelle
    α > 1   on AMPLIFIE l'écart à la moyenne — donc le contenu

α est un simple facteur d'échelle appliqué à l'écart. C'est **linéaire**, donc dans les
règles : aucune rétropropagation, aucune non-convexité, un paramètre.

MESURES : le rapport ‖écart‖/‖moyenne‖ (le rétrécissement, directement), la fidélité,
et surtout la SÉPARATION dont la cible est celle du professeur.

PRÉDICTION, ÉCRITE AVANT LA MESURE : si le rétrécissement est la cause, notre rapport
‖écart‖/‖moyenne‖ doit être NETTEMENT plus petit que celui du professeur, et une
amplification α > 1 doit ramener la séparation vers +0,052 — sans détruire la
fidélité, parce qu'un cosinus est insensible à l'échelle quand il n'y a pas de
constante, mais SENSIBLE ici justement parce qu'il y en a une.

Usage : amplification.py <cache_appr.npz> <cache_test.npz> [--neur 120]
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
    alphas = [float(x) for x in opt("--alphas", "0.5,0.75,1,1.25,1.5,2,3").split(",")]

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
    nt = max(1, len(itr)//3)
    iap, ival = itr[nt:], itr[:nt]
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)

    P = Pont((cltr, Etr, Ytr), 0.2, graine, len(garde))
    P.quadratique = True
    P.a_min, P.a_max = 0.02, 0.8
    P.nait(n_neur, True)
    idx = np.arange(P.compte_neurones)
    Xt = P.recalcule(idx, Ete)
    W = P.ajuste(idx, ride, mt, iap)
    print(f"# réseau {P.compte_neurones} neurones · {len(P.couches)} couche(s)")

    O = np.vstack([P.phi(P._norm(Xt[k])) @ W + mt for k in range(len(clte))])
    Y = np.vstack(Yte)
    # LES ENTRÉES N'ONT PAS TOUTES LA MÊME LONGUEUR : on garde les bornes, au lieu
    # de supposer un pas fixe (première version, qui produisait « Mean of empty
    # slice » et des moyennes par entrée fausses).
    bornes = np.cumsum([0] + [len(Yte[k]) for k in range(len(clte))])

    # LE RÉTRÉCISSEMENT, mesuré directement
    Om, Ym = O.mean(0), Y.mean(0)
    rap_o = float(np.linalg.norm(O - Om, axis=1).mean() /
                  max(np.linalg.norm(Om), 1e-9))
    rap_y = float(np.linalg.norm(Y - Ym, axis=1).mean() /
                  max(np.linalg.norm(Ym), 1e-9))
    print(f"\n# RÉTRÉCISSEMENT — ‖écart à la moyenne‖ / ‖moyenne‖, par ligne :")
    print(f"#   notre sortie : {rap_o:.4f}")
    print(f"#   professeur   : {rap_y:.4f}")
    print(f"#   rapport      : {rap_o/max(rap_y,1e-9):.3f}  "
          f"({'RÉTRÉCIE' if rap_o < rap_y else 'amplifie'})")

    pro = np.array([Yte[k].mean(0) for k in range(len(clte))])
    tl, td = deux_axes(clte, pro)
    print(f"\n# CIBLE — professeur : S_langue {tl:.4f} · S_domaine {td:.4f} · "
          f"SÉPARATION {tl-td:+.4f}")

    print(f"\n# {'alpha':>7}{'fid TEST':>10}{'S_langue':>10}{'S_domaine':>11}"
          f"{'SÉPARATION':>12}{'vs prof':>9}")
    for a in alphas:
        Oa = mt + a*(O - mt)
        ft = cos_lignes(Oa, Y)
        nos = np.array([Oa[bornes[k]:bornes[k+1]].mean(0)
                        for k in range(len(clte))])
        nl, nd = deux_axes(clte, nos)
        print(f" {a:>7.2f}{ft:>10.4f}{nl:>10.4f}{nd:>11.4f}{nl-nd:>+12.4f}"
              f"{(nl-nd)-(tl-td):>+9.4f}")
    # CONTRÔLE INDIQUÉ PAR LE RÉSULTAT : les paires « même article, langues
    # différentes » du test sont ENTRE LANGUES INCONNUES, alors que les paires « même
    # langue, articles différents » sont DANS une langue inconnue. Si l'inversion
    # vient de là, elle doit disparaître sur les langues d'APPRENTISSAGE.
    print(f"\n# CONTRÔLE — les deux axes sur les langues d'APPRENTISSAGE")
    Xa = P.recalcule(idx, [Etr[i] for i in iap])
    Oa2 = np.vstack([P.phi(P._norm(Xa[j])) @ W + mt for j in range(len(iap))])
    Ya2 = np.vstack([Ytr[i] for i in iap])
    nms_a = [cltr[i] for i in iap]
    bornes_a = np.cumsum([0] + [len(Ytr[i]) for i in iap])
    for a in (1.0, 2.0):
        Oa3 = mt + a*(Oa2 - mt)
        ft = cos_lignes(Oa3, Ya2)
        nos = np.array([Oa3[bornes_a[j]:bornes_a[j+1]].mean(0)
                        for j in range(len(iap))])
        nl, nd = deux_axes(nms_a, nos)
        print(f"  alpha {a:>4.2f} : fid {ft:.4f} · S_langue {nl:.4f} · "
              f"S_domaine {nd:.4f} · SÉPARATION {nl-nd:+.4f}")
    proa = np.array([Ytr[i].mean(0) for i in iap])
    tl2, td2 = deux_axes(nms_a, proa)
    print(f"  professeur (mêmes entrées) : S_langue {tl2:.4f} · "
          f"S_domaine {td2:.4f} · SÉPARATION {tl2-td2:+.4f}")
    print(f"\n# PRÉDICTION : si le rétrécissement est la cause, le rapport ci-dessus")
    print(f"# est nettement < 1 et une amplification ramène la séparation vers +0,052.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
