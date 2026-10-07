#!/usr/bin/env python3
"""objectif_du_pont.py — ajuster la lecture pour SÉPARER le contenu, pas seulement
rapprocher les langues.

CE QUE LE §57 A ÉTABLI. Depuis le §41 on lisait l'invariance (0,90-0,96) comme la
preuve que le pont fonctionnait. Le test à deux axes a montré autre chose : **notre
sortie ne sépare plus les contenus** (S_domaine ≈ S_langue), alors que **le
professeur, si**. Une invariance élevée peut donc s'obtenir de deux façons — en
rapprochant les langues À CONTENU ÉGAL (ce qu'on veut) ou en effaçant tout (ce qu'on
ne veut pas), et **rien dans l'objectif ne distinguait les deux**.

LE SECOND TERME. On ajuste donc la lecture sous un objectif à deux curseurs :

    ‖XW − Y‖²  +  μ_lang·P_lang(W)  −  μ_cont·P_cont(W)

  P_lang = variance INTER-LANGUE de la sortie   (à MINIMISER)
  P_cont = variance INTER-CONTENU de la sortie  (à MAXIMISER)

Les deux sont quadratiques en W — tr(WᵀCW) — donc la solution reste en FORME FERMÉE :
aucune rétropropagation, même mécanique que le §48.

LA MESURE QUI COMPTE n'est plus l'invariance seule, mais la **SÉPARATION** :

    séparation = S_langue − S_domaine

  S_langue   : même contenu, langues différentes   → à garder
  S_domaine  : même langue, contenus différents    → à distinguer

Séparation positive = la sortie rapproche les langues **plus** qu'elle n'efface les
contenus. C'est la définition mesurable d'un pont qui fonctionne.

PRÉDICTION, ÉCRITE AVANT LA MESURE : μ_cont doit faire MONTER la séparation vers celle
du professeur, au prix d'un peu de fidélité. Le point intéressant est le taux
d'échange, et si l'on peut atteindre la séparation du professeur sans effondrer la
fidélité.

Usage : objectif_du_pont.py <cache_appr.npz> <cache_test.npz> [--neur 120]
                            [--grille "0,0;0,03,0;0,1,0;0,03,0.03;0.1,0.1"]
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
    grille = []
    for cellule in opt("--grille", "0,0;0.1,0;0,0.1;0.1,0.1;0.3,0.3;1,1").split(";"):
        a, b = cellule.split(",")
        grille.append((float(a), float(b)))

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
    print(f"# réseau {P.compte_neurones} neurones · {len(P.couches)} couche(s)")

    pro = np.array([Yte[k].mean(0) for k in range(len(clte))])
    tl, td = deux_axes(clte, pro)
    print(f"\n# CIBLE — le professeur : S_langue {tl:.4f} · S_domaine {td:.4f} · "
          f"SÉPARATION {tl-td:+.4f}")

    print(f"\n# {'mu_lang':>8}{'mu_cont':>9}{'fid TEST':>10}{'S_langue':>10}"
          f"{'S_domaine':>11}{'SÉPARATION':>12}{'vs prof':>9}")
    for a, b in grille:
        P.mu_inv, P.mu_cont = a, b
        W = P.ajuste(idx, ride, mt, iap)
        ft = cos_lignes(P.phi(np.vstack(Xt)) @ W + mt, np.vstack(Yte))
        nos = np.array([(P.phi(P._norm(Xt[k])) @ W + mt).mean(0)
                        for k in range(len(clte))])
        nl, nd = deux_axes(clte, nos)
        print(f" {a:>8.3f}{b:>9.3f}{ft:>10.4f}{nl:>10.4f}{nd:>11.4f}"
              f"{nl-nd:>+12.4f}{(nl-nd)-(tl-td):>+9.4f}")
    P.mu_inv = P.mu_cont = 0.0
    print(f"\n# SÉPARATION = S_langue − S_domaine. Positive : la sortie rapproche les")
    print(f"# langues PLUS qu'elle n'efface les contenus. C'est la définition mesurable")
    print(f"# d'un pont qui fonctionne — et elle manquait à tous les chiffres du rapport.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
