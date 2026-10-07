#!/usr/bin/env python3
"""covariance_cible.py — donner à la sortie la COVARIANCE de la cible.

LE CONSTAT QUI MÈNE ICI. Le §67 a montré une chose mathématiquement nette : **le
rapport `P_cont/P_lang` est invariant d'échelle**. Une amplification uniforme de
l'écart multiplie les deux énergies par le même facteur, donc ne change jamais leur
rapport — mesuré : 3,064 exactement pour α de 1 à 5, à tous les rangs essayés.

**Le rapport ne peut donc venir que d'un changement de DIRECTIONS**, pas d'amplitude.
C'est cohérent avec tout ce que la série §58-§67 a trouvé.

L'IDÉE, et elle vise exactement cela. Le professeur a un rapport de **10,912** ; nous
sommes à 3,064. Sa **matrice de covariance** contient cette structure directionnelle.
On construit donc une transformation linéaire `A` qui **donne à notre sortie la
covariance de la cible** :

    C_O = covariance de nos sorties   (sur l'APPRENTISSAGE)
    C_Y = covariance des cibles       (sur l'APPRENTISSAGE)
    A   = C_Y^(1/2) · C_O^(-1/2)
    sortie corrigée = (O − m_O)·Aᵀ + m_Y

`A` est une **matrice fixe de 896×896 apprise une seule fois** : rien n'est demandé au
texte neuf, aucune étiquette, aucun regroupement. C'est purement linéaire, en forme
fermée, et sans rétropropagation.

PRÉDICTION, ÉCRITE AVANT LA MESURE : si la structure directionnelle du professeur est
accessible par une transformation linéaire de notre sortie, le rapport doit MONTER vers
10,912 — et pas seulement par le dénominateur, puisque la covariance de la cible fixe
les deux axes à la fois.

Le risque, et il est réel : `C_O` est mal conditionnée (nos sorties sont fortement
corrélées), donc `C_O^(-1/2)` peut amplifier du bruit. On régularise et on le dit.

Usage : covariance_cible.py <cache_appr.npz> <cache_test.npz> [--neur 120]
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pont_generatif import Pont, charge, cos_lignes  # noqa: E402


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def moyennes(noms, O, bornes):
    return np.vstack([O[bornes[i]:bornes[i+1]].mean(0) for i in range(len(noms))])


def decompose(noms, V):
    par_c, par_l = {}, {}
    for i, n in enumerate(noms):
        L, _, k = n.partition("_")
        par_c.setdefault(k, []).append(i)
        par_l.setdefault(L, []).append(i)
    m = V.mean(0)
    comm = [k for k, idx in par_c.items() if len(idx) == len(par_l)]
    if not comm:
        return None
    Pl = float(np.mean([np.sum((V[idx].mean(0) - m)**2) for idx in par_l.values()]))
    Pc = float(np.mean([np.sum((V[par_c[k]].mean(0) - m)**2) for k in comm]))
    return Pl, Pc, Pc/max(Pl, 1e-12)


def racine(C, puissance, plancher):
    w, V = np.linalg.eigh((C + C.T)/2)
    w = np.maximum(w, plancher)
    return (V * w**puissance) @ V.T


def main():
    tr_p, te_p = sys.argv[1], sys.argv[2]
    n_neur = int(opt("--neur", 120))
    part = float(opt("--part", 0.5))
    ride, graine = 0.03, 5
    melanges = [float(x) for x in opt("--melanges", "0,0.25,0.5,0.75,1").split(",")]

    cltr, Etr, Ytr, H = charge(tr_p)
    clte, Ete, Yte, _ = charge(te_p)
    vivant = np.zeros(Ytr[0].shape[1])
    for y in Ytr:
        vivant += ((y != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(Ytr)
    garde = np.where(vivant >= part)[0]
    Ytr = [y[:, garde] for y in Ytr]
    Yte = [y[:, garde] for y in Yte]

    itr = np.arange(len(cltr))
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)

    if opt("--centre-entree", "") != "":
        Etr = [e - e.mean(0, keepdims=True) for e in Etr]
        Ete = [e - e.mean(0, keepdims=True) for e in Ete]
        print("# CENTRAGE DE L'ENTRÉE activé (§64, levier retenu)")

    P = Pont((cltr, Etr, Ytr), 0.2, graine, len(garde))
    P.quadratique = True
    P.a_min, P.a_max = 0.02, 0.8
    P.nait(n_neur, True)
    idx = np.arange(P.compte_neurones)
    W = P.ajuste(idx, ride, mt, itr)
    print(f"# réseau {P.compte_neurones} neurones · {len(P.couches)} couche(s) · "
          f"{len(garde)} canaux")

    # ------------------------------------------------- COVARIANCES SUR L'APPRENTISSAGE
    Xa = P.recalcule(idx, Etr)
    Oa = np.vstack([P.phi(P._norm(Xa[j])) @ W + mt for j in range(len(cltr))])
    Ya = np.vstack(Ytr)
    mO, mY = Oa.mean(0), Ya.mean(0)
    CO = ((Oa - mO).T @ (Oa - mO))/len(Oa)
    CY = ((Ya - mY).T @ (Ya - mY))/len(Ya)
    trO, trY = float(np.trace(CO)), float(np.trace(CY))
    print(f"# trace de la covariance : notre sortie {trO:,.0f} · cible {trY:,.0f} "
          f"· rapport {trY/max(trO,1e-12):.2f}")
    plancher = float(opt("--plancher", 1e-3))*trO/len(garde)
    A = racine(CY, 0.5, plancher) @ racine(CO, -0.5, plancher)
    print(f"# plancher de régularisation : {plancher:.3e} "
          f"({opt('--plancher','1e-3')} × trace/ncanaux)")

    Xt = P.recalcule(idx, Ete)
    Ot = np.vstack([P.phi(P._norm(Xt[k])) @ W + mt for k in range(len(clte))])
    bo_t = np.cumsum([0] + [len(Yte[k]) for k in range(len(clte))])
    rq = decompose(clte, moyennes(clte, np.vstack(Yte), bo_t))
    print(f"\n# professeur : P_lang {rq[0]:.1f} · P_cont {rq[1]:.1f} · "
          f"rapport {rq[2]:.3f}")
    print(f"\n# {'melange':>9}{'fid TEST':>10}{'P_lang':>10}{'P_cont':>10}"
          f"{'RAPPORT':>10}")
    for mu in melanges:
        Oc = (Ot - mO) @ (mu*A + (1-mu)*np.eye(len(garde))).T + mY
        ft = cos_lignes(Oc, np.vstack(Yte))
        dm = decompose(clte, moyennes(clte, Oc, bo_t))
        print(f" {mu:>9.2f}{ft:>10.4f}{dm[0]:>10.1f}{dm[1]:>10.1f}{dm[2]:>10.3f}")
    print(f"\n# melange 0 = notre sortie · 1 = covariance de la cible imposée.")
    print(f"# CRITÈRE (§62.3) : P_cont PROCHE du professeur ET P_lang qui ne le dépasse")
    print(f"# pas — le rapport seul peut être gonflé par le dénominateur.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
