#!/usr/bin/env python3
"""analyse_union_experts.py — ce que le REGROUPEMENT des jetons par expert
économise, calculé sur une trace de routage réelle.

Le fait : en préremplissage par lots (`--lot N`), les jetons d'un même lot qui
ont choisi le même expert partagent UNE lecture de sa matrice (`forward_lot`
appelle un seul `gemm_dense_q4` par expert non vide). Jeton par jetons, la même
matrice est relue autant de fois qu'elle a d'ayants droit.

Ce que le script mesure, par couche et globalement :

  - les **lectures d'experts** en mode jeton (`N_jetons × k`) et en mode groupe
    (`Σ_blocs |union des experts du bloc|`) — c'est le nombre exact de matrices
    lues, pas une estimation ;
  - le **rapport** entre les deux, en fonction de la taille de bloc N ;
  - les **octets** correspondants, pour une taille d'expert donnée ;
  - la **borne** : quand N → ∞ le mode groupe lit chaque expert une fois par
    couche, donc le coût par jeton tombe à `n_experts/N` experts-équivalents.
    Un modèle dont les experts pèsent E Go au total coûte alors E/N Go par jeton.

Le résultat ne dépend PAS de la vitesse du disque : c'est un compte d'octets
lus. La traduction en secondes demande la bande du support, qui est mesurée
ailleurs (`reports/rapport-budget-kimi-k3.md`).

Usage :
    analyse_union_experts.py <trace> [--experts-par-jeton K] [--taille-expert Mo]
                             [--blocs 1,2,4,8,16,32,64,128,256,512]
"""
import sys
from collections import Counter


def lire(chemin):
    """Rend {couche: [(jeton, [experts]), …]} trié par jeton."""
    par_couche = {}
    with open(chemin) as f:
        for ligne in f:
            p = ligne.split()
            if len(p) < 3:
                continue
            l, j = int(p[0]), int(p[1])
            par_couche.setdefault(l, []).append((j, [int(x) for x in p[2:]]))
    for l in par_couche:
        par_couche[l].sort()
    return par_couche


def compte(par_couche, bloc, k_defaut):
    """Rend (lectures_jeton, lectures_groupe, n_jetons, n_experts)."""
    lj = lg = njet = 0
    ne = 0
    for l, suite in par_couche.items():
        experts = [e for _, es in suite for e in es]
        ne = max(ne, (max(experts) + 1) if experts else 0)
        njet += len(suite)
        lj += sum(len(es) for _, es in suite)
        for d in range(0, len(suite), bloc):
            tranche = suite[d:d + bloc]
            union = set()
            for _, es in tranche:
                union.update(es)
            lg += len(union)
    return lj, lg, njet, ne


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    trace = sys.argv[1]
    k = 8
    taille = None
    blocs = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    a = sys.argv[2:]
    i = 0
    while i < len(a):
        if a[i] == "--experts-par-jeton":
            k = int(a[i + 1]); i += 2
        elif a[i] == "--taille-expert":
            taille = float(a[i + 1]); i += 2
        elif a[i] == "--blocs":
            blocs = [int(x) for x in a[i + 1].split(',')]; i += 2
        else:
            print(f"option inconnue : {a[i]}"); return 1
    par_couche = lire(trace)
    if not par_couche:
        print("trace vide"); return 1

    # Le k réellement observé, s'il diffère de celui annoncé.
    k_obs = sum(len(es) for s in par_couche.values() for _, es in s) / \
        sum(len(s) for s in par_couche.values())
    n_layer = len(par_couche)
    n_jet = max(len(s) for s in par_couche.values())
    ne = max(max(es) for s in par_couche.values() for _, es in s) + 1
    print(f"# trace      : {trace}")
    print(f"# couches    : {n_layer} · jetons : {n_jet} · experts vus : {ne} · "
          f"experts/jeton observés : {k_obs:.2f} (annoncé {k})")
    if taille:
        print(f"# taille d'un expert : {taille} Mo → un expert-équivalent = {taille} Mo")
    print()

    entete = f"{'bloc':>6} {'lect_jeton':>11} {'lect_groupe':>12} {'gain':>7} " \
             f"{'exp-éq/jeton':>13}"
    if taille:
        entete += f" {'Mo/jeton':>10}"
    print(entete)
    l0 = None
    for N in blocs:
        lj, lg, nj, _ = compte(par_couche, N, k)
        gain = lj / lg if lg else 0.0
        if N == 1:
            l0 = lj / nj
        eq = lg / nj
        ligne = f"{N:>6} {lj:>11} {lg:>12} {gain:>6.2f}× {eq:>13.3f}"
        if taille:
            ligne += f" {eq * taille:>10.3f}"
        print(ligne)

    # La borne : un bloc assez grand pour voir tous les experts d'une couche.
    print()
    print(f"# borne (N → ∞) : {ne} experts-équivalents par couche, soit "
          f"{ne / n_jet:.3f} par jeton pour cette invite de {n_jet} jetons")
    print(f"#                contre {l0:.3f} en mode jeton — soit "
          f"{l0 * n_jet / ne:.1f}× moins d'octets d'experts")
    if taille:
        tot = ne * n_layer * taille / 1024.0
        print(f"#                un balayage complet des experts = {tot:.2f} Go "
              f"({n_layer} couches × {ne} experts × {taille} Mo)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
