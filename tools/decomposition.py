#!/usr/bin/env python3
"""decomposition.py — où va la variance : en LANGUE ou en CONTENU ?

Après quatre causes écartées (§58 à §60), il reste à LOCALISER le défaut. La bonne
façon n'est pas une similarité cosinus mais une **décomposition de variance**, qui est
exacte et additive.

Pour chaque entrée (langue L, contenu k), on prend sa moyenne `m_Lk`. On décompose :

    ν_L  = moyenne de `m_Lk` sur les contenus        -> effet LANGUE
    μ_k  = moyenne de `m_Lk` sur les langues         -> effet CONTENU
    r_Lk = m_Lk − ν_L − μ_k + m̄                      -> résidu (interaction)

    P_lang = Σ_L n_L ‖ν_L − m̄‖²     énergie portée par la LANGUE
    P_cont = Σ_k n_k ‖μ_k − m̄‖²     énergie portée par le CONTENU

Le RAPPORT `P_cont / P_lang` est la quantité qui compte : il dit lequel des deux
axes structure le plus la représentation. On le mesure sur **notre sortie** et sur
**celle du professeur**, sur les mêmes entrées — c'est une comparaison directe, sans
cible mouvante.

C'est aussi le remède au défaut du §60.3 : cette mesure ne dépend pas de « quelles
langues sont dans le panel », seulement de leur nombre et de leur diversité.

Usage : decomposition.py <cache_appr.npz> <cache_test.npz> [--neur 120]
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pont_generatif import Pont, charge, cos_lignes  # noqa: E402


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def decompose(noms, V):
    """V : une ligne par entrée. Rend P_lang, P_cont, P_res et le rapport."""
    par_c, par_l = {}, {}
    for i, n in enumerate(noms):
        L, _, k = n.partition("_")
        par_c.setdefault(k, []).append(i)
        par_l.setdefault(L, []).append(i)
    m = V.mean(0)
    # moyennes par langue (sur les contenus) et par contenu (sur les langues)
    nu, mu = {}, {}
    for L, idx in par_l.items():
        nu[L] = V[idx].mean(0)
    for k, idx in par_c.items():
        mu[k] = V[idx].mean(0)
    # on ne garde que les contenus présents dans TOUTES les langues, sinon la
    # décomposition n'est pas équilibrée
    nL = len(par_l)
    comm = [k for k, idx in par_c.items() if len(idx) == nL]
    if not comm:
        return None
    P_lang = float(np.mean([np.sum((nu[L] - m)**2) for L in par_l]))
    P_cont = float(np.mean([np.sum((mu[k] - m)**2) for k in comm]))
    return P_lang, P_cont, P_cont/max(P_lang, 1e-12), len(comm), nL


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

    itr = np.arange(len(cltr))
    nt = max(1, len(itr)//3)
    iap = itr[nt:]
    mt = np.vstack([Ytr[i] for i in itr]).mean(axis=0)

    # CENTRAGE DE L'ENTRÉE (`--centre-entree`) : on retire à chaque langue son
    # « jeton moyen ». Ce décalage est massivement propre à la langue (écriture,
    # morphologie) et ne dit aucun contenu. C'est le seul levier du dépôt qui attaque
    # le décalage de langue À LA SOURCE, et il est DÉPLOYABLE : la moyenne de l'entrée
    # se calcule sur l'entrée elle-même, sans étiquette.
    if opt("--centre-entree", "") != "":
        Etr = [e - e.mean(0, keepdims=True) for e in Etr]
        Ete = [e - e.mean(0, keepdims=True) for e in Ete]
        print("# CENTRAGE DE L'ENTRÉE : le jeton moyen de chaque langue est retiré")
    P = Pont((cltr, Etr, Ytr), 0.2, graine, len(garde))
    P.quadratique = True
    P.a_min, P.a_max = 0.02, 0.8
    P.nait(n_neur, True)
    idx = np.arange(P.compte_neurones)
    mu_lang = float(opt("--mu-lang", 0.0))
    P.mu_inv = mu_lang
    W = P.ajuste(idx, ride, mt, iap)
    print(f"# réseau {P.compte_neurones} neurones · {len(P.couches)} couche(s)"
          + (f" · mu_lang = {mu_lang}" if mu_lang > 0 else ""))

    for titre, E, Y, noms in (
            ("TEST (langues inconnues)", Ete, Yte, clte),
            ("APPRENTISSAGE (langues connues)",
             [Etr[i] for i in iap], [Ytr[i] for i in iap], [cltr[i] for i in iap])):
        X = P.recalcule(idx, E)
        O = np.vstack([P.phi(P._norm(X[k])) @ W + mt for k in range(len(noms))])
        bornes = np.cumsum([0] + [len(Y[k]) for k in range(len(noms))])
        nos = np.array([O[bornes[k]:bornes[k+1]].mean(0) for k in range(len(noms))])
        pro = np.array([Y[k].mean(0) for k in range(len(noms))])
        ft = cos_lignes(O, np.vstack(Y))
        print(f"\n=== {titre} === (fidélité {ft:.4f})")
        print(f"# {'':<12}{'P_lang':>12}{'P_cont':>12}{'RAPPORT':>10}"
              f"{'contenus':>10}{'langues':>9}")
        for nom, V in (("NOTRE", nos), ("PROFESSEUR", pro)):
            r = decompose(noms, V)
            if r is None:
                print(f"  {nom:<12} décomposition impossible"); continue
            pl, pc, rap, nc, nl = r
            print(f"  {nom:<12}{pl:>12.1f}{pc:>12.1f}{rap:>10.3f}{nc:>10}{nl:>9}")
    # ------------------------------------------------------------------ REMÈDE
    #
    # Le diagnostic désigne un remède : amplifier la sortie LE LONG DE L'AXE DU
    # CONTENU SEULEMENT. Le §60.2 amplifiait uniformément, ce qui augmentait les deux
    # axes et ne rétablissait donc pas leur rapport.
    #
    # ATTENTION, C'EST UN DIAGNOSTIC, PAS UN MODÈLE. Le décalage de contenu `c_k` se
    # calcule à partir du regroupement des entrées par contenu — information qui
    # n'existe PAS pour un texte neuf. Il répond à une question précise : l'énergie de
    # contenu est-elle seulement SOUS-PRODUITE (donc récupérable par une mise à
    # l'échelle), ou absente de la représentation (donc irrécupérable) ?
    print(f"\n=== AMPLIFICATION DE L'AXE CONTENU (diagnostic) ===")
    print(f"# {'beta':>6}{'fid TEST':>10}{'P_lang':>10}{'P_cont':>10}"
          f"{'RAPPORT':>9}")
    X = P.recalcule(idx, Ete)
    O = np.vstack([P.phi(P._norm(X[k])) @ W + mt for k in range(len(clte))])
    bornes = np.cumsum([0] + [len(Yte[k]) for k in range(len(clte))])
    par_c, par_l = {}, {}
    for i, n in enumerate(clte):
        L, _, k = n.partition("_")
        par_c.setdefault(k, []).append(i)
        par_l.setdefault(L, []).append(i)
    m = np.vstack([O[bornes[i]:bornes[i+1]].mean(0)
                   for i in range(len(clte))]).mean(0)
    mu = {k: np.mean([np.vstack([O[bornes[i]:bornes[i+1]].mean(0)])
                      for i in idx], axis=0)
          for k, idx in par_c.items() if len(idx) == len(par_l)}
    for beta in (0.0, 1.0, 3.0, 10.0, 30.0):
        blocs = []
        for i, n in enumerate(clte):
            L, _, k = n.partition("_")
            bloc = O[bornes[i]:bornes[i+1]]
            if k in mu:
                bloc = bloc + beta*(mu[k] - m)
            blocs.append(bloc)
        Ob = np.vstack(blocs)
        ft = cos_lignes(Ob, np.vstack(Yte))
        nos = np.array([Ob[bornes[i]:bornes[i+1]].mean(0)
                        for i in range(len(clte))])
        r = decompose(clte, nos)
        pl, pc, rap = r[0], r[1], r[2]
        print(f" {beta:>6.1f}{ft:>10.4f}{pl:>10.1f}{pc:>10.1f}{rap:>9.3f}")
    print(f"# Rappel professeur : P_lang 399,2 · P_cont 4356,4 · rapport 10,91")

    # ------------------------------------------------- VERSION DÉPLOYABLE
    #
    # Le diagnostic ci-dessus utilise le regroupement par contenu, indisponible pour
    # un texte neuf. Mais il dit aussi OÙ est le manque : dans la MOYENNE par entrée,
    # qui est rétrécie vers la moyenne globale. Or cette moyenne est calculable à
    # l'inférence — c'est la moyenne des sorties de l'entrée elle-même.
    #
    # On amplifie donc le DÉCALAGE DE MOYENNE de chaque entrée, sans toucher aux
    # écarts entre positions :
    #
    #     O_new = O + gamma · ( moyenne(O_entrée) − m̄ )
    #
    # C'est linéaire, sans paramètre appris, et calculable sur l'entrée seule.
    print(f"\n=== AMPLIFICATION DU DÉCALAGE DE MOYENNE, PAR ENTRÉE (déployable) ===")
    print(f"# {'gamma':>7}{'fid TEST':>10}{'P_lang':>10}{'P_cont':>10}{'RAPPORT':>9}")
    moy = np.vstack([O[bornes[i]:bornes[i+1]].mean(0) for i in range(len(clte))])
    for gamma in (0.0, 0.5, 1.0, 2.0, 3.0, 5.0):
        blocs = []
        for i in range(len(clte)):
            blocs.append(O[bornes[i]:bornes[i+1]] + gamma*(moy[i] - m))
        Ob = np.vstack(blocs)
        ft = cos_lignes(Ob, np.vstack(Yte))
        nos = np.array([Ob[bornes[i]:bornes[i+1]].mean(0)
                        for i in range(len(clte))])
        r = decompose(clte, nos)
        print(f" {gamma:>7.1f}{ft:>10.4f}{r[0]:>10.1f}{r[1]:>10.1f}{r[2]:>9.3f}")
    print(f"# gamma=0 est notre sortie actuelle. Aucun regroupement par contenu n'est")
    print(f"# utilisé ici : seulement la moyenne de l'entrée elle-même.")
    print(f"\n# P_lang : énergie portée par l'axe LANGUE · P_cont : par l'axe CONTENU.")
    print(f"# RAPPORT > 1 : le contenu structure plus que la langue (ce qu'on veut).")
    print(f"# Cette mesure ne dépend PAS de quelles langues sont dans le panel —")
    print(f"# contrairement à la similarité du §60.3, qui changeait de signe.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
