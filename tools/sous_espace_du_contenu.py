#!/usr/bin/env python3
"""sous_espace_du_contenu.py — rendre le remède DÉPLOYABLE.

LE PROBLÈME, EN UNE PHRASE (§62). L'énergie de contenu de notre sortie est
sous-produite d'un facteur ~3,6 ; elle est récupérable par mise à l'échelle ; mais la
mise à l'échelle essayée exigeait de savoir **quelles entrées partagent un contenu** —
information qui n'existe pas pour un texte neuf.

L'IDÉE QUI MANQUAIT, et elle est simple. Ce regroupement n'est pas nécessaire **à
l'inférence** : il ne l'est qu'à l'**apprentissage**. On apprend donc, une fois pour
toutes et sur les données d'apprentissage :

  1. le SOUS-ESPACE DU CONTENU — l'espace engendré par les écarts de contenu
     `μ_k − m̄`, où `μ_k` est la moyenne des sorties des entrées partageant le
     contenu `k` ;
  2. un projecteur `Π` sur ce sous-espace.

Puis, à l'inférence, on applique à la sortie d'un texte neuf :

    O_new = O + (γ − 1)·Π·(O − m̄)

`Π` est une **matrice fixe** de 896×896 apprise une fois. Aucun regroupement n'est
demandé au texte neuf : on ne fait que **décomposer sa sortie selon un axe appris**, et
amplifier cet axe. C'est linéaire, sans rétropropagation, sans paramètre ajusté sur le
test.

PRÉDICTION, ÉCRITE AVANT LA MESURE : si le sous-espace du contenu se TRANSFÈRE d'un
panel à l'autre, amplifier dedans doit faire monter `P_cont` sans faire monter
`P_lang`, donc **augmenter le rapport** — ce que l'amplification uniforme du §62.2 ne
faisait pas (rapport figé à 1,460).

Si le sous-espace ne se transfère pas, `P_lang` montera autant que `P_cont` et le
rapport restera figé : ce serait une réponse négative, et elle serait nette.

Usage : sous_espace_du_contenu.py <cache_appr.npz> <cache_test.npz> [--neur 120]
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
    gammas = [float(x) for x in opt("--gammas", "1,1.5,2,3,5").split(",")]
    rang_max = int(opt("--rang", 0))          # 0 = rang complet du sous-espace

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

    P = Pont((cltr, Etr, Ytr), 0.2, graine, len(garde))
    P.quadratique = True
    P.a_min, P.a_max = 0.02, 0.8
    P.nait(n_neur, True)
    idx = np.arange(P.compte_neurones)
    W = P.ajuste(idx, ride, mt, iap)
    print(f"# réseau {P.compte_neurones} neurones · {len(P.couches)} couche(s) · "
          f"{len(garde)} canaux · {len(iap)} entrées d'apprentissage")

    # ------------------------------------------------ SOUS-ESPACE APPRIS (apprentissage)
    noms_a = [cltr[i] for i in iap]
    Xa = P.recalcule(idx, [Etr[i] for i in iap])
    Oa = np.vstack([P.phi(P._norm(Xa[j])) @ W + mt for j in range(len(iap))])
    bo_a = np.cumsum([0] + [len(Ytr[i]) for i in iap])
    Ma = moyennes(noms_a, Oa, bo_a)
    ma = Ma.mean(0)
    par_c = {}
    for j, n in enumerate(noms_a):
        _, _, k = n.partition("_")
        par_c.setdefault(k, []).append(j)
    comm = [k for k, v in par_c.items() if len(v) == len(set(n.partition("_")[0]
                                                            for n in noms_a))]
    E = np.vstack([Ma[par_c[k]].mean(0) - ma for k in comm])      # (contenus, canaux)
    U, S, Vt = np.linalg.svd(E, full_matrices=False)
    r = len(S) if rang_max <= 0 else min(rang_max, len(S))
    # projecteur sur le sous-espace du contenu, APPRIS UNE FOIS
    Pi = Vt[:r].T @ Vt[:r]
    print(f"# SOUS-ESPACE DU CONTENU : {r} directions apprises sur {len(comm)} "
          f"contenus · énergie captée {np.sum(S[:r]**2)/max(np.sum(S**2),1e-12):.1%}")

    # ---------------------------------------------------------------- ÉVALUATION
    Xt = P.recalcule(idx, Ete)
    Ot = np.vstack([P.phi(P._norm(Xt[k])) @ W + mt for k in range(len(clte))])
    bo_t = np.cumsum([0] + [len(Yte[k]) for k in range(len(clte))])
    Yt = np.vstack(Yte)
    # ÉTIQUETTE CORRIGÉE : la première version affichait « professeur » alors que
    # c'étaient les chiffres de NOTRE sortie. Le professeur, sur le même panel, vaut
    # P_lang 399,2 · P_cont 4 356,4 · rapport 10,912.
    rp = decompose(clte, moyennes(clte, Ot, bo_t))
    rq = decompose(clte, moyennes(clte, np.vstack(Yte), bo_t))
    print(f"\n# NOTRE SORTIE (TEST) : P_lang {rp[0]:.1f} · P_cont {rp[1]:.1f} · "
          f"rapport {rp[2]:.3f}")
    print(f"# PROFESSEUR  (TEST) : P_lang {rq[0]:.1f} · P_cont {rq[1]:.1f} · "
          f"rapport {rq[2]:.3f}")

    print(f"\n# {'gamma':>7}{'rang':>6}{'fid TEST':>10}{'P_lang':>10}{'P_cont':>10}"
          f"{'RAPPORT':>9}")
    for r2 in (r, max(1, r//2), min(r, 20)):
        for g in ([1.0] if r2 != r else gammas):
            blocs = []
            for i in range(len(clte)):
                bloc = Ot[bo_t[i]:bo_t[i+1]]
                d = bloc.mean(0) - mt
                blocs.append(bloc + (g - 1.0)*(Pi @ d))
            Ob = np.vstack(blocs)
            ft = cos_lignes(Ob, Yt)
            nos = moyennes(clte, Ob, bo_t)
            dm = decompose(clte, nos)
            print(f" {g:>7.2f}{r2:>6}{ft:>10.4f}{dm[0]:>10.1f}{dm[1]:>10.1f}"
                  f"{dm[2]:>9.3f}")
    print(f"\n# Le projecteur est APPRIS sur l'apprentissage, puis appliqué tel quel au")
    print(f"# test : aucun regroupement par contenu n'est demandé au texte neuf.")
    print(f"# CRITÈRE (leçon du §62.3) : P_cont proche du professeur ET P_lang qui ne")
    print(f"# le dépasse pas. Le rapport seul peut être gonflé par le dénominateur.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
