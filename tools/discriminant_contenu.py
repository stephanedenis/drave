#!/usr/bin/env python3
"""discriminant_contenu.py — maximiser le rapport contenu/langue par les DIRECTIONS.

CE QUI MÈNE ICI, en trois étapes établies :
  §67 — le rapport `P_cont/P_lang` est INVARIANT D'ÉCHELLE : aucune amplitude ne peut
        le corriger, seulement un changement de DIRECTIONS ;
  §68 — imposer la covariance TOTALE de la cible ne marche pas, parce que la covariance
        globale ne détermine pas le partage contenu/langue ;
  §61 — le partage dépend des **moyennes PAR ENTRÉE**, donc de la structure de groupes.

L'OUTIL QUI VISE EXACTEMENT CELA. On cherche les directions de l'espace de sortie qui
**maximisent le rapport** entre l'énergie de contenu et l'énergie de langue. C'est un
problème aux valeurs propres généralisé — l'analyse discriminante linéaire :

    C_cont · v = λ · C_lang · v

où, calculées sur les **moyennes par entrée** de l'APPRENTISSAGE :
    C_cont = covariance des moyennes par CONTENU   (μ_k − μ̄)
    C_lang = covariance des moyennes par LANGUE    (ν_L − ν̄)

On garde les `r` directions de plus grand λ et on y projette la sortie.

C'est **linéaire**, **en forme fermée**, **sans rétropropagation**, et **DÉPLOYABLE** :
le projecteur est une matrice fixe apprise une fois. Aucun regroupement n'est demandé au
texte neuf.

DIFFÉRENCE AVEC LE §66. Le §66 retirait le sous-espace de langue dans l'espace des
ÉTATS. Ici on **maximise un RAPPORT** dans l'espace de SORTIE, au lieu de seulement
retirer — ce qui doit aussi **amplifier** les directions de contenu, pas seulement
réduire celles de langue.

PRÉDICTION, ÉCRITE AVANT LA MESURE : si les directions discriminantes se transfèrent,
le rapport doit monter nettement au-dessus de 3,064 (le meilleur obtenu), et l'on saura
si l'écart à 10,912 est franchissable par des directions apprises.

RÉSERVE ASSUMÉE : `C_lang` est de rang au plus `nombre de langues − 1` = 2 ici. On la
régularise, et **le plancher est affiché** — un résultat obtenu avec une régularisation
non déclarée n'est pas un résultat.

Usage : discriminant_contenu.py <cache_appr.npz> <cache_test.npz> [--neur 120]
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


def groupes(noms):
    par_c, par_l = {}, {}
    for i, n in enumerate(noms):
        L, _, k = n.partition("_")
        par_c.setdefault(k, []).append(i)
        par_l.setdefault(L, []).append(i)
    return par_c, par_l


def decompose(noms, V):
    par_c, par_l = groupes(noms)
    m = V.mean(0)
    comm = [k for k, idx in par_c.items() if len(idx) == len(par_l)]
    if not comm:
        return None
    Pl = float(np.mean([np.sum((V[idx].mean(0) - m)**2) for idx in par_l.values()]))
    Pc = float(np.mean([np.sum((V[par_c[k]].mean(0) - m)**2) for k in comm]))
    return Pl, Pc, Pc/max(Pl, 1e-12)


def cov_groupes(M, par, m, ncan):
    """Covariance des moyennes de groupe autour de la moyenne globale."""
    C = np.zeros((ncan, ncan))
    for idx in par.values():
        d = M[idx].mean(0) - m
        C += np.outer(d, d)
    return C/max(len(par), 1)


def main():
    tr_p, te_p = sys.argv[1], sys.argv[2]
    n_neur = int(opt("--neur", 120))
    part = float(opt("--part", 0.5))
    ride, graine = 0.03, 5
    rangs = [int(x) for x in opt("--rangs", "0,2,5,10,20,40").split(",")]
    alphas_rangs = {int(x) for x in opt("--alphas-rangs", "2,5,20").split(",")}

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
        print("# CENTRAGE DE L'ENTRÉE activé (§64)")

    P = Pont((cltr, Etr, Ytr), 0.2, graine, len(garde))
    P.quadratique = True
    P.a_min, P.a_max = 0.02, 0.8
    P.nait(n_neur, True)
    idx = np.arange(P.compte_neurones)
    W = P.ajuste(idx, ride, mt, itr)
    print(f"# réseau {P.compte_neurones} neurones · {len(P.couches)} couche(s) · "
          f"{len(garde)} canaux")

    # -------------------------------------- DISCRIMINANT APPRIS SUR L'APPRENTISSAGE
    Xa = P.recalcule(idx, Etr)
    Oa = np.vstack([P.phi(P._norm(Xa[j])) @ W + mt for j in range(len(cltr))])
    bo_a = np.cumsum([0] + [len(Ytr[i]) for i in range(len(cltr))])
    Ma = moyennes(cltr, Oa, bo_a)
    ma = Ma.mean(0)
    pc_a, pl_a = groupes(cltr)
    pc_a = {k: v for k, v in pc_a.items() if len(v) == len(pl_a)}
    Cc = cov_groupes(Ma, pc_a, ma, len(garde))
    Cl = cov_groupes(Ma, pl_a, ma, len(garde))
    lam = float(opt("--plancher", 1e-2))*np.trace(Cl)/len(garde)
    lam = max(lam, 1e-12)
    # C_cont v = lambda C_lang v  ->  vecteurs propres généralisés
    w, V = np.linalg.eigh(np.linalg.solve(
        Cl + lam*np.eye(len(garde)), Cc))
    ordre = np.argsort(-w)
    V = V[:, ordre]
    w = w[ordre]
    print(f"# DISCRIMINANT : {len(pc_a)} contenus · {len(pl_a)} langues · "
          f"{len(garde)} canaux")
    print(f"# plancher affiché : {lam:.3e} ({opt('--plancher','1e-2')} × "
          f"trace(C_lang)/ncanaux)")
    print(f"# valeurs propres du discriminant (les 8 premières) : "
          + " · ".join(f"{x:.2f}" for x in w[:8]))

    Xt = P.recalcule(idx, Ete)
    Ot = np.vstack([P.phi(P._norm(Xt[k])) @ W + mt for k in range(len(clte))])
    bo_t = np.cumsum([0] + [len(Yte[k]) for k in range(len(clte))])
    rq = decompose(clte, moyennes(clte, np.vstack(Yte), bo_t))
    print(f"\n# professeur : P_lang {rq[0]:.1f} · P_cont {rq[1]:.1f} · "
          f"rapport {rq[2]:.3f}")
    print(f"\n# {'rang':>6}{'fid TEST':>10}{'P_lang':>10}{'P_cont':>10}"
          f"{'RAPPORT':>10}")
    for r in rangs:
        if r == 0:
            Oc = Ot
        else:
            Vr = V[:, :r]
            Oc = (Ot - ma) @ Vr @ Vr.T + ma
        ft = cos_lignes(Oc, np.vstack(Yte))
        dm = decompose(clte, moyennes(clte, Oc, bo_t))
        print(f" {r:>6}{ft:>10.4f}{dm[0]:>10.1f}{dm[1]:>10.1f}{dm[2]:>10.3f}")
        # AMPLIFICATION jusqu'aux MAGNITUDES DU PROFESSEUR. Le rapport est invariant
        # d'échelle (§67), donc amplifier ne le change pas — mais il amène les DEUX
        # énergies au niveau de la cible, ce qui est le critère du §62.3. La question
        # ouverte est le coût en fidélité.
        if r in alphas_rangs and dm[1] > 0:
            for cible in (1000.0, 4356.4):
                a = float(np.sqrt(cible/dm[1]))
                Oa = ma + a*(Oc - ma)
                fa = cos_lignes(Oa, np.vstack(Yte))
                da = decompose(clte, moyennes(clte, Oa, bo_t))
                print(f"        # -> P_cont visé {cible:>7.0f} : alpha {a:>5.1f} · "
                      f"fid {fa:.4f} · P_lang {da[0]:>7.1f} · P_cont {da[1]:>8.1f} "
                      f"· rapport {da[2]:>7.3f}")
    print(f"\n# rang 0 = notre sortie · rang r = projection sur les r meilleures")
    print(f"# directions discriminantes apprises sur l'apprentissage.")
    print(f"# CRITÈRE (§62.3) : P_cont PROCHE du professeur ET P_lang qui ne le dépasse")
    print(f"# pas — le rapport seul peut être gonflé par le dénominateur.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
