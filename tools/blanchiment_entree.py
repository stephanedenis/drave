#!/usr/bin/env python3
"""blanchiment_entree.py — retirer de l'entrée sa structure de COVARIANCE par langue.

CE QUE LE §70 A ÉTABLI. L'axe de langue vient de **l'entrée** du professeur, et le
réservoir ne fait que l'**amplifier** : `P_lang` passe de 199,5 (entrée seule) à 238,8
(réservoir), pendant que `P_cont` baisse. La couche 8 du professeur a un rapport de
10,912 ; sa propre couche 0, lue le mieux possible, n'en a que 1,698.

CE QUI RESTE PERMIS PAR LES CONTRAINTES : `A` et `B` sont aléatoires et **gelés**, seule
la lecture s'ajuste. On ne peut donc pas *apprendre* la transformation manquante. Mais
on peut **changer ce qu'on donne à lire** au réservoir.

Le §64 a montré qu'en retirant à l'entrée son **jeton moyen** (le premier moment), le
rapport gagne 28 %. Reste le **second moment** : la structure de covariance, qui est
elle aussi massivement propre à la langue (écriture, morphologie, longueur des mots).
On la retire par un **blanchiment par langue** :

    E' = (E − moyenne) · C_langue^(-1/2)

où `C_langue` est la covariance de l'entrée **de cette langue**, estimée sur
l'apprentissage. **Déployable** : à l'inférence, la covariance s'estime sur le texte
d'entrée lui-même, sans étiquette ni regroupement.

PRÉDICTION, ÉCRITE AVANT LA MESURE : si la structure de second moment de l'entrée est
une part importante de l'axe de langue, le blanchiment doit faire **baisser `P_lang`**
et **monter le rapport** au-delà des 1,698 de l'entrée centrée — et, appliqué avant le
réservoir, il doit aussi empêcher le réservoir d'amplifier ce qui n'est plus là.

Usage : blanchiment_entree.py <cache_appr.npz> <cache_test.npz> [--neur 120]
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
    alphas = [float(x) for x in opt("--alphas", "0,0.25,0.5,1").split(",")]
    plancher = float(opt("--plancher", 1e-3))

    cltr, Etr0, Ytr, H = charge(tr_p)
    clte, Ete0, Yte, _ = charge(te_p)
    vivant = np.zeros(Ytr[0].shape[1])
    for y in Ytr:
        vivant += ((y != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(Ytr)
    garde = np.where(vivant >= part)[0]
    Ytr = [y[:, garde] for y in Ytr]
    Yte = [y[:, garde] for y in Yte]

    itr = np.arange(len(cltr))
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)

    print(f"# {'alpha':>7}{'fid TEST':>10}{'P_lang':>10}{'P_cont':>10}"
          f"{'RAPPORT':>10}{'  (entrée seule, 0 neurone)'}")
    for alpha in alphas:
        # blanchiment appris par langue sur l'APPRENTISSAGE, appliqué aux deux panels
        T = {}
        if alpha > 0:
            par_l = {}
            for i, n in enumerate(cltr):
                par_l.setdefault(n.partition("_")[0], []).append(i)
            for L, idx in par_l.items():
                A = np.vstack([Etr0[i] for i in idx])
                m = A.mean(0)
                Ac = A - m
                C = (Ac.T @ Ac)/len(Ac)
                w, V = np.linalg.eigh((C + C.T)/2)
                w = np.maximum(w, plancher*float(np.trace(C))/len(w))
                T[L] = (m, (V * w**(-alpha/2)) @ V.T)
        def tr(E, noms):
            out = []
            for i, n in enumerate(noms):
                L = n.partition("_")[0]
                if L in T:
                    m, M = T[L]
                    out.append(np.asarray(E[i], dtype=np.float64) @ M)
                else:
                    out.append(np.asarray(E[i], dtype=np.float64)
                               - np.asarray(E[i], dtype=np.float64).mean(0))
            return out
        Etr = tr(Etr0, cltr)
        Ete = tr(Ete0, clte)
        # ENTREÉ SEULE : lecture linéaire-quadratique directe, aucun neurone
        quad = lambda A: np.hstack([A, A*A])  # noqa: E731
        G = D = None
        ntot = 0
        for i in itr:
            A = quad(Etr[i])
            Z = Ytr[i] - mt
            G = A.T @ A if G is None else G + A.T @ A
            D = A.T @ Z if D is None else D + A.T @ Z
            ntot += len(A)
        W = np.linalg.solve(G + ride*ntot*np.eye(G.shape[0]), D)
        blocs = [quad(Ete[k]) @ W + mt for k in range(len(clte))]
        O = np.vstack(blocs)
        ft = cos_lignes(O, np.vstack(Yte))
        bornes = np.cumsum([0] + [len(Ete0[k]) for k in range(len(clte))])
        dm = decompose(clte, moyennes(clte, O, bornes))
        print(f" {alpha:>7.2f}{ft:>10.4f}{dm[0]:>10.1f}{dm[1]:>10.1f}{dm[2]:>10.3f}")
        del Etr, Ete, G, D, O

    print(f"\n# RAPPEL : entrée centrée seule (alpha 0 ici, moyenne retirée) = 1,698")
    print(f"# au §70 ; réservoir seul = 1,354 ; professeur = 10,912.")
    print(f"# CRITÈRE (§62.3) : P_cont PROCHE du professeur ET P_lang qui ne le dépasse")
    print(f"# pas — le rapport seul peut être gonflé par le dénominateur.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
