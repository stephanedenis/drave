#!/usr/bin/env python3
"""renforcement.py — le mécanisme du mandat peut-il produire la transformation ?

LA QUESTION OUVERTE, APRÈS LES §57-§71. Le professeur crée, entre sa couche 0 et sa
couche 8, une séparation contenu/langue d'un facteur **10,912** — que sa propre couche 0
n'a pas (**1,698** au mieux). Un réservoir à poids **aléatoires gelés** ne la produit
pas : mesuré, il l'**abaisse** à 1,354 (§70).

LA CONTRAINTE DU PROJET est explicite : *« A et B aléatoires et gelés, seule la lecture
s'ajuste en forme fermée »* — **mais** elle sanctionne aussi, mot pour mot :
*« L'ajout d'une couche suppose donc une relecture du corpus pour réajuster les poids
par renforcement/atrophie (pas de backprop). »*

**Le renforcement/atrophie est donc le seul mécanisme d'ajustement autorisé** — et il
n'a JAMAIS été testé sur l'axe contenu/langue. C'est ce que fait ce script.

LE MÉCANISME, tel qu'il est implémenté dans `Pont.renforce` :
  1. on ajuste la lecture, puis on calcule le **résidu** `R = Y − (φ(X)·W + mt)` ;
  2. pour chaque neurone, on mesure sa **capture** du résidu —
     `cap = |corrélation entre sa trace et le résidu|`, normalisée dans [0, 1] ;
  3. on multiplie ses poids par `f = 1 + η·(2·cap − 1)` : **renforcé** s'il capte plus
     de la moitié du résidu, **atrophié** sinon, et d'autant plus que `η` est grand.

On RÉPÈTE — chaque passe est une **relecture du corpus**, exactement ce que le mandat
décrit. Aucune rétropropagation : `f` ne dépend que d'une corrélation locale.

MESURES, à chaque passe : la fidélité, `P_lang`, `P_cont` et **le rapport** — dont la
cible est 10,912.

PRÉDICTION, ÉCRITE AVANT LA MESURE : si le renforcement peut façonner le réservoir vers
la transformation du professeur, **le rapport doit monter** au fil des passes. S'il
stagne autour de 1,35 (la valeur du réservoir gelé), alors ce mécanisme non plus ne
produit pas la transformation — et il ne restera, dans les règles du projet, plus grand
chose à essayer.

Usage : renforcement.py <cache_appr.npz> <cache_test.npz> [--neur 120] [--passes 8]
"""
import os
import sys
import time

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
    passes = int(opt("--passes", 8))
    etas = [float(x) for x in opt("--etas", "0.02,0.1").split(",")]

    cltr, Etr, Ytr, H = charge(tr_p)
    clte, Ete, Yte, _ = charge(te_p)
    vivant = np.zeros(Ytr[0].shape[1])
    for y in Ytr:
        vivant += ((y != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(Ytr)
    garde = np.where(vivant >= part)[0]
    Ytr = [y[:, garde] for y in Ytr]
    Yte = [y[:, garde] for y in Yte]
    if opt("--centre-entree", "") != "":
        Etr = [e - e.mean(0, keepdims=True) for e in Etr]
        Ete = [e - e.mean(0, keepdims=True) for e in Ete]
        print("# CENTRAGE DE L'ENTRÉE activé (§64)")

    itr = np.arange(len(cltr))
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)

    P = Pont((cltr, Etr, Ytr), 0.2, graine, len(garde))
    P.quadratique = True
    P.a_min, P.a_max = 0.02, 0.8
    P.nait(n_neur, True)
    idx = np.arange(P.compte_neurones)
    print(f"# réseau {P.compte_neurones} neurones · {len(P.couches)} couche(s) · "
          f"{len(garde)} canaux · {passes} passes de relecture")

    bo_t = np.cumsum([0] + [len(Yte[k]) for k in range(len(clte))])
    rq = decompose(clte, moyennes(clte, np.vstack(Yte), bo_t))
    print(f"# CIBLE — professeur : P_lang {rq[0]:.1f} · P_cont {rq[1]:.1f} · "
          f"rapport {rq[2]:.3f}")

    # référence : le réservoir GELÉ, sans aucun renforcement
    W = P.ajuste(idx, ride, mt, itr)
    Xt = P.recalcule(idx, Ete)
    Ot = np.vstack([P.phi(P._norm(Xt[k])) @ W + mt for k in range(len(clte))])
    ft = cos_lignes(Ot, np.vstack(Yte))
    dm = decompose(clte, moyennes(clte, Ot, bo_t))
    print(f"\n# {'passe':>6}{'eta':>6}{'fid TEST':>10}{'P_lang':>10}{'P_cont':>10}"
          f"{'RAPPORT':>10}")
    print(f" {0:>6}{'—':>6}{ft:>10.4f}{dm[0]:>10.1f}{dm[1]:>10.1f}{dm[2]:>10.3f}")

    # RELECTURE PAR LOT. `Pont.renforce` ajuste la lecture POUR CHAQUE NEURONE :
    # sur 120 neurones et 8 passes cela ferait 1 920 ajustements, soit ~5 heures.
    # On applique la MÊME FORMULE, mais avec UNE seule relecture du corpus par
    # passe — ce qui est d'ailleurs plus fidèle à l'idée de « relire le corpus » :
    # on lit une fois, on mesure le résidu, et on renforce chaque neurone selon sa
    # propre capture de ce résidu. Aucune rétropropagation : `f` ne dépend que
    # d'une corrélation locale entre l'activation d'un neurone et le résidu.
    def passe(eta, j_max=None):
        jm = P.compte_neurones if j_max is None else j_max
        jdx = np.arange(jm)
        Wl = P.ajuste(jdx, ride, mt, itr)
        Xl = np.vstack([P.X[i][:, jdx] for i in itr])
        Yl = np.vstack([P.Y[i] for i in itr])
        R = Yl - (P.phi(Xl) @ Wl + mt)
        b_ = R - R.mean(0)
        nb = np.linalg.norm(b_, axis=0)
        ok = (nb > 0) & np.isfinite(nb)
        caps = []
        for j in range(jm):
            xj = np.concatenate([P.X[i][:, j] for i in itr]).astype(np.float64)
            a_ = xj - xj.mean()
            na = float(np.linalg.norm(a_))
            if na == 0.0 or not ok.any():
                caps.append(0.0)
                continue
            cap = float(np.abs(a_ @ b_[:, ok]).max()/(na*nb[ok].max()))
            caps.append(cap)
            f = 1.0 + eta*(2.0*cap - 1.0)
            w_par, w_self, bb, c = P.poids[j]
            P.poids[j] = (w_par*f, w_self*f, bb*f, c)
        P.X = P.recalcule(np.arange(jm), P.E)
        return caps

    captes = []
    for eta in etas:
        for k in range(passes):
            t = time.time()
            captes = passe(eta)
            W = P.ajuste(idx, ride, mt, itr)
            Xt = P.recalcule(idx, Ete)
            Ot = np.vstack([P.phi(P._norm(Xt[k])) @ W + mt for k in range(len(clte))])
            ft = cos_lignes(Ot, np.vstack(Yte))
            dm = decompose(clte, moyennes(clte, Ot, bo_t))
            print(f" {k+1:>6}{eta:>6.2f}{ft:>10.4f}{dm[0]:>10.1f}{dm[1]:>10.1f}"
                  f"{dm[2]:>10.3f}   ({time.time()-t:.0f} s)")
    print(f"\n# Capture moyenne du résidu au dernier passage : "
          f"{np.mean(captes):.3f}")
    print(f"# PRÉDICTION : si le renforcement façonne le réservoir vers la transformation")
    print(f"# du professeur, le rapport doit MONTER au fil des passes (cible 10,912).")
    print(f"# S'il stagne vers 1,35 — la valeur du réservoir gelé — ce mécanisme non plus")
    print(f"# ne produit pas la transformation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
