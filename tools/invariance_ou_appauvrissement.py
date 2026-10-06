#!/usr/bin/env python3
"""invariance_ou_appauvrissement.py — LA question non tranchée du rapport.

Depuis le §41, un même fait revient : **notre sortie est beaucoup plus invariante
entre langues que la représentation du professeur qu'elle imite.** Sur l'UDHR :
0,95 contre 0,65. Sur le corpus Wikipedia multi-domaine (§56) : **0,928 contre
0,347** — un écart de 0,58.

Deux lectures, et rien ne les départageait :

  1. C'est la MISSION. Un pont linguistico-sémantique veut l'invariance ; notre
     sortie fait ce que le professeur ne fait pas.
  2. C'est de l'APPAUVRISSEMENT. Une sortie qui ne dépend presque plus de l'entrée
     est invariante pour la mauvaise raison : elle a effacé le contenu avec la langue.

LE TEST QUI TRANCHE, et il ne demande aucun corpus nouveau — seulement de mesurer la
MÊME similarité sur les DEUX axes :

    S_langue   : même ARTICLE, langues DIFFÉRENTES   -> ce qu'on veut garder
    S_domaine  : même LANGUE, articles DIFFÉRENTS    -> ce qu'il faut distinguer

Si S_domaine ≈ S_langue, notre sortie ne distingue plus les contenus : elle a tout
aplati. Si S_domaine << S_langue, elle distingue les contenus ET rapproche les
langues — c'est exactement ce qu'un pont doit faire.

On mesure les deux sur NOTRE sortie et sur celle du PROFESSEUR, sur les mêmes
entrées, pour que la comparaison soit directe.

Usage : invariance_ou_appauvrissement.py <cache_appr.npz> <cache_test.npz>
                                         [--neur 120] [--couche 8]
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pont_generatif import Pont, charge  # noqa: E402


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
    """V : une ligne par entrée. Rend (S_langue, S_domaine) et le détail par unité."""
    lang, unit = {}, {}
    for i, n in enumerate(noms):
        L, _, k = n.partition("_")
        lang.setdefault(L, {})[k] = i
        unit.setdefault(k, {})[L] = i
    sl, sd = [], []
    for k, par in unit.items():
        if len(par) >= 2:
            sl += moy_croisee([V[i] for i in par.values()])
    for L, par in lang.items():
        if len(par) >= 2:
            sd += moy_croisee([V[i] for i in par.values()])
    return sl, sd


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
    nt = max(1, len(itr)//3)
    iap, ival = itr[nt:], itr[:nt]
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)

    t = 0
    P = Pont((cltr, Etr, Ytr), 0.2, graine, len(garde))
    P.quadratique = True
    P.a_min, P.a_max = 0.02, 0.8
    P.nait(n_neur, True)
    idx = np.arange(P.compte_neurones)
    P.mu_inv = float(opt("--mu-inv", 0.0))
    if P.mu_inv > 0:
        print(f"# pénalité d'invariance mu = {P.mu_inv}")
    W = P.ajuste(idx, ride, mt, iap)
    Xte = P.recalcule(idx, Ete)
    print(f"# réseau {P.compte_neurones} neurones · {len(P.couches)} couche(s)")

    # POOLING. La dernière position d'un résumé d'article est peut-être stéréotypée
    # (« fin d'article »), ce qui fabriquerait un faux effondrement. On mesure donc
    # DEUX pooling : la dernière position ET la moyenne sur toutes les positions.
    # Si les deux donnent le même verdict, ce n'est pas un artefact de position.
    pool = opt("--pool", "les_deux")

    def sortie(k, mode):
        A = P.phi(P._norm(Xte[k])) @ W + mt
        return A[-1] if mode == "derniere" else A.mean(0)

    def cible(k, mode):
        B = Yte[k]
        return B[-1] if mode == "derniere" else B.mean(0)

    modes = ["derniere", "moyenne"] if pool == "les_deux" else [pool]
    for mode in modes:
        notre = np.array([sortie(k, mode) for k in range(len(clte))])
        prof = np.array([cible(k, mode) for k in range(len(clte))])
        print(f"\n=== POOLING : {mode.upper()} ===")
        print(f"# {'':<18}{'S_langue':>10}{'S_domaine':>11}{'écart':>10}{'rapport':>9}")
        for nom, V in (("NOTRE SORTIE", notre), ("PROFESSEUR", prof)):
            sl, sd = deux_axes(clte, V)
            ml, md = float(np.mean(sl)), float(np.mean(sd))
            print(f"  {nom:<18}{ml:>10.4f}{md:>11.4f}{ml-md:>+10.4f}"
                  f"{ml/max(md,1e-9):>9.2f}")
    return 0

    notre = np.array([(P.phi(P._norm(Xte[k])) @ W + mt)[-1]
                      for k in range(len(clte))])
    prof = np.array([Yte[k][-1] for k in range(len(clte))])

    print(f"\n# {'':<18}{'S_langue':>10}{'S_domaine':>11}{'écart':>10}"
          f"{'rapport':>9}")
    for nom, V in (("NOTRE SORTIE", notre), ("PROFESSEUR", prof)):
        sl, sd = deux_axes(clte, V)
        ml, md = float(np.mean(sl)), float(np.mean(sd))
        print(f"  {nom:<18}{ml:>10.4f}{md:>11.4f}{ml-md:>+10.4f}"
              f"{ml/max(md,1e-9):>9.2f}")
    print(f"\n# ({len(clte)} entrées · S_langue sur les articles vus dans ≥ 2 langues)")
    print(f"\n# LECTURE : si S_domaine ≈ S_langue, notre sortie ne distingue plus les")
    print(f"# contenus — elle a aplati. Si S_domaine << S_langue, elle distingue les")
    print(f"# contenus ET rapproche les langues : c'est ce qu'un pont doit faire.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
