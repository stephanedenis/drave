#!/usr/bin/env python3
"""etats_sans_langue.py — retirer l'axe de langue DANS L'ESPACE DES ÉTATS.

POURQUOI AILLEURS QUE LES §58-§64. Tous les moyens essayés jusqu'ici agissaient soit
sur l'OBJECTIF du fit, soit sur la SORTIE. Or le §64 a montré que les deux axes sont
**mêlés dans les états du réservoir** : centrer l'entrée réduit l'axe de langue d'un
facteur 4,8 mais réduit l'axe du contenu de 3,8× en même temps.

L'idée ici est **structurellement différente** : agir sur les ÉTATS, avant la lecture.

  1. Sur les données d'apprentissage, on calcule la covariance INTER-LANGUE des états :
     `C_lang = Σ_L n_L (ν_L − ν̄)(ν_L − ν̄)ᵀ`, où `ν_L` est l'état moyen de la langue L.
  2. On en prend les `r` directions dominantes, et on **projette les états sur leur
     complément** : `X' = X·(I − Π_lang)`.
  3. On ajuste la lecture sur `X'`.

`Π_lang` est une **matrice fixe** apprise une fois. À l'inférence, on applique la même
projection à un texte neuf : aucune étiquette de langue, aucun regroupement.

LA DIFFÉRENCE AVEC LE §63. Le §63 retirait/amplifiait dans l'espace des SORTIES, après
que la lecture ait déjà mélangé les deux axes. Ici on agit **avant** : on retire de
l'entrée de la lecture ce qui ne porte QUE la langue. Si le sous-espace de langue est
mieux séparé dans l'espace des états que dans celui des sorties, cela doit marcher.

PRÉDICTION, ÉCRITE AVANT LA MESURE : retirer les directions de langue doit faire
**BAISSER `P_lang`** sans faire baisser `P_cont` d'autant, donc **monter le rapport**.
Et contrairement au §63, l'effet doit se **transférer** aux langues inconnues, parce que
la projection est appliquée aux états — qui sont calculés de la même façon quelle que
soit la langue.

Si `P_cont` baisse autant que `P_lang`, c'est une réponse négative, et elle sera nette :
les deux axes seraient mêlés jusque dans l'espace des états.

Usage : etats_sans_langue.py <cache_appr.npz> <cache_test.npz> [--neur 120]
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


def main():
    tr_p, te_p = sys.argv[1], sys.argv[2]
    n_neur = int(opt("--neur", 120))
    part = float(opt("--part", 0.5))
    ride, graine = 0.03, 5
    rangs = [int(x) for x in opt("--rangs", "0,2,5,10,20,40").split(",")]
    alphas_rangs = {int(x) for x in opt("--alphas-rangs", "5,40").split(",")}

    cltr, Etr, Ytr, H = charge(tr_p)
    clte, Ete, Yte, _ = charge(te_p)
    vivant = np.zeros(Ytr[0].shape[1])
    for y in Ytr:
        vivant += ((y != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(Ytr)
    garde = np.where(vivant >= part)[0]
    Ytr = [y[:, garde] for y in Ytr]
    Yte = [y[:, garde] for y in Yte]

    # DÉCOUPAGE CORRIGÉ — voir le commentaire détaillé dans les autres outils : la
    # version `itr[nt:]` supprimait le bloc entier de la première langue, les entrées
    # étant ordonnées par langue.
    itr = np.arange(len(cltr))
    iap = itr
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)

    # COMBINAISON avec le levier retenu du §64 : on peut centrer l'entrée ET retirer
    # le sous-espace de langue des états. Les deux attaquent le même axe par des
    # chemins différents — l'entrée avant le réservoir, les états après.
    if opt("--centre-entree", "") != "":
        Etr = [e - e.mean(0, keepdims=True) for e in Etr]
        Ete = [e - e.mean(0, keepdims=True) for e in Ete]
        print("# CENTRAGE DE L'ENTRÉE activé")
    P = Pont((cltr, Etr, Ytr), 0.2, graine, len(garde))
    P.quadratique = True
    P.a_min, P.a_max = 0.02, 0.8
    P.nait(n_neur, True)
    idx = np.arange(P.compte_neurones)
    print(f"# réseau {P.compte_neurones} neurones · {len(P.couches)} couche(s) · "
          f"{len(garde)} canaux")

    # ------------------------------------------- SOUS-ESPACE DE LANGUE (apprentissage)
    Xa = P.recalcule(idx, [Etr[i] for i in iap])
    noms_a = [cltr[i] for i in iap]
    bo_a = np.cumsum([0] + [len(Etr[i]) for i in iap])
    Ma = moyennes(noms_a, np.vstack(Xa), bo_a)      # état moyen par entrée
    par_l = {}
    for j, n in enumerate(noms_a):
        par_l.setdefault(n.partition("_")[0], []).append(j)
    nu = np.vstack([Ma[v].mean(0) for v in par_l.values()])
    nbl = np.array([len(v) for v in par_l.values()], dtype=np.float64)
    nub = (nbl[:, None]*nu).sum(0)/nbl.sum()
    D = nu - nub
    C = (D*nbl[:, None]).T @ D
    w, V = np.linalg.eigh(C)
    print(f"# SOUS-ESPACE DE LANGUE : {len(par_l)} langues d'apprentissage · "
          f"{len(w)} directions · la 1re porte {w[-1]/max(w.sum(),1e-12):.1%} de "
          f"l'énergie de langue")

    # ---------------------------------------------------------------- ÉVALUATION
    Xt = np.vstack(P.recalcule(idx, Ete))
    bo_t = np.cumsum([0] + [len(Yte[k]) for k in range(len(clte))])
    print(f"\n# {'rang':>6}{'fid TEST':>10}{'P_lang':>10}{'P_cont':>10}"
          f"{'RAPPORT':>9}")
    for r in rangs:
        Pi = (V[:, -r:] @ V[:, -r:].T) if r > 0 else 0.0
        # on retire le sous-espace de langue des ÉTATS, puis on ajuste la lecture
        Xa2 = [np.asarray(x, dtype=np.float64) @ (np.eye(Xa[0].shape[1]) - Pi)
               for x in Xa]
        Xt2 = Xt @ (np.eye(Xt.shape[1]) - Pi)
        G = D2 = None
        ntot = 0
        for j in range(len(iap)):
            A = P.phi(Xa2[j])
            Z = np.asarray(Ytr[iap[j]], dtype=np.float64) - mt
            G = A.T @ A if G is None else G + A.T @ A
            D2 = A.T @ Z if D2 is None else D2 + A.T @ Z
            ntot += len(A)
        W = np.linalg.solve(G + ride*ntot*np.eye(G.shape[0]), D2)
        Ot = P.phi(Xt2) @ W + mt
        ft = cos_lignes(Ot, np.vstack(Yte))
        nos = moyennes(clte, Ot, bo_t)
        dm = decompose(clte, nos)
        print(f" {r:>6}{ft:>10.4f}{dm[0]:>10.1f}{dm[1]:>10.1f}{dm[2]:>9.3f}")
        # AMPLIFICATION DE L'ÉCART, maintenant que l'axe de langue a été retiré.
        # Le §60.2 avait montré qu'amplifier uniformément ne change pas le rapport,
        # parce que les deux axes montent ensemble. Mais si le sous-espace de langue
        # a été RETIRÉ des états, l'écart restant devrait porter surtout du contenu —
        # et l'amplification devrait alors monter P_cont plus que P_lang.
        if r in alphas_rangs:
            print(f"        # amplification de l'écart, rang {r} :")
            for a in (1.5, 2.0, 3.0, 5.0):
                Oa = mt + a*(Ot - mt)
                fa = cos_lignes(Oa, np.vstack(Yte))
                na = moyennes(clte, Oa, bo_t)
                da = decompose(clte, na)
                print(f"        #   alpha {a:>4.1f} : fid {fa:.4f} · P_lang "
                      f"{da[0]:>8.1f} · P_cont {da[1]:>9.1f} · rapport {da[2]:>7.3f}")
    rq = decompose(clte, moyennes(clte, np.vstack(Yte), bo_t))
    print(f"# professeur : P_lang {rq[0]:.1f} · P_cont {rq[1]:.1f} · "
          f"rapport {rq[2]:.3f}")
    print(f"\n# rang 0 = notre sortie actuelle, sans retrait.")
    print(f"# CRITÈRE (leçon du §62.3) : P_cont proche du professeur ET P_lang qui ne")
    print(f"# le dépasse pas — le rapport seul peut être gonflé par le dénominateur.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
