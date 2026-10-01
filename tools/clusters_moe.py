#!/usr/bin/env python3
"""Découpage des MoE en clusters — à partir d'une trace de routage réelle.

Le moteur écrit une ligne par (couche, jeton) avec les experts retenus :
`DRAVE_TRACE_EXPERTS=/tmp/trace.txt drave <modele> --ppl <ids> --limit N --lot L`

Ce script répond à la question de placement : **quels experts s'allument
ENSEMBLE ?** Les compteurs d'usage disent quels experts sont chauds ; ils ne
disent pas lesquels sont chauds en même temps, et c'est pourtant ce qui décide si
un jeton peut être servi par UN nœud ou doit en interroger quatre.

Trois mesures, et une comparaison qui les rend honnêtes :

* **couverture** : part des k experts d'un jeton qui tiennent dans son meilleur
  cluster (1,0 = un seul nœud suffit) ;
* **ventilation** (fan-out) : nombre de clusters nécessaires pour couvrir 90 % des
  experts d'un jeton (1,0 = le meilleur cas possible) ;
* **équilibre** : taille des clusters (un cluster géant ne compte pas comme un
  bon découpage) ;
* **témoin** : les mêmes mesures avec des clusters ALÉATOIRES de même taille. Sans
  ce témoin, une couverture de 0,4 ne dit rien — elle peut être le hasard.

Usage :
    clusters_moe.py /tmp/routage.txt [--clusters 8] [--json /tmp/clusters.json]
"""
import argparse
import json
import random
from collections import Counter, defaultdict


def lire(chemin):
    """→ {couche: {jeton: [experts]}}"""
    par_couche = defaultdict(dict)
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            morceaux = ligne.split()
            if len(morceaux) < 3:
                continue
            couche, jeton = int(morceaux[0]), int(morceaux[1])
            par_couche[couche][jeton] = [int(x) for x in morceaux[2:]]
    return par_couche


def co_activation(jetons, ne):
    """Comptes de co-occurrence, normalisés par le nombre de jetons."""
    co = [[0.0] * ne for _ in range(ne)]
    for experts in jetons.values():
        for i in experts:
            for j in experts:
                if i != j:
                    co[i][j] += 1.0
    n = max(1, len(jetons))
    for i in range(ne):
        for j in range(ne):
            co[i][j] /= n
    return co


def partition_equilibree(co, ne, g, frequences=None, passes=6):
    """Partition équilibrée qui garde les experts co-activés ensemble.

    L'agglomératif naïf donne UN cluster géant (121 experts sur 128) : la
    couverture d'un jeton y est trivialement de 1,0 et la mesure ne dit plus rien.
    Le problème réel est un partitionnement de graphe ÉQUILIBRÉ — chaque cluster
    a la taille d'un nœud — que l'on construit gloutonnement :

      1. les experts sont pris du plus fréquent au plus rare ;
      2. chacun rejoint le cluster qui a de la place et maximise la
         co-activation moyenne avec ses membres ;
      3. une recherche locale échange ensuite les experts qui gagnent à changer.

    `frequences` sert au témoin « groupé par fréquence » : mêmes tailles, mais
    sans regarder qui s'allume avec qui.
    """
    taille_max = (ne + g - 1) // g
    if frequences is not None:
        ordre = sorted(range(ne), key=lambda e: (-frequences[e], e))
    else:
        ordre = sorted(range(ne), key=lambda e: (-sum(co[e]), e))
    affectation = {}
    membres = [[] for _ in range(g)]
    for e in ordre:
        meilleur, score = None, None
        for c in range(g):
            if len(membres[c]) >= taille_max:
                continue
            s = sum(co[e][f] for f in membres[c]) / max(1, len(membres[c]))
            if score is None or s > score:
                meilleur, score = c, s
        if meilleur is None:
            meilleur = min(range(g), key=lambda c: len(membres[c]))
        affectation[e] = meilleur
        membres[meilleur].append(e)
    # recherche locale : un expert change de cluster si la co-activation moyenne
    # avec ses nouveaux voisins augmente et que l'équilibre reste tenu
    for _ in range(passes):
        change = 0
        for e in range(ne):
            c0 = affectation[e]
            meilleur, score = c0, sum(co[e][f] for f in membres[c0] if f != e) / max(1, len(membres[c0]) - 1)
            for c in range(g):
                if c == c0 or len(membres[c]) >= taille_max:
                    continue
                s = sum(co[e][f] for f in membres[c]) / max(1, len(membres[c]))
                if s > score:
                    meilleur, score = c, s
            if meilleur != c0:
                membres[c0].remove(e)
                membres[meilleur].append(e)
                affectation[e] = meilleur
                change += 1
        if change == 0:
            break
    return affectation, membres


def mesurer(jetons, affectation, n_clusters):
    """Couverture, ventilation et tailles pour une affectation donnée."""
    couvertures, ventilations = [], []
    for experts in jetons.values():
        par_cluster = Counter(affectation[e] for e in experts)
        couvertures.append(par_cluster.most_common(1)[0][1] / len(experts))
        cumul, n = 0, 0
        for _, c in par_cluster.most_common():
            cumul += c
            n += 1
            if cumul >= 0.9 * len(experts):
                break
        ventilations.append(n)
    tailles = Counter(affectation.values())
    return {
        "couverture_moyenne": sum(couvertures) / len(couvertures),
        "couverture_min": min(couvertures),
        "ventilation_moyenne": sum(ventilations) / len(ventilations),
        "ventilation_max": max(ventilations),
        "taille_min": min(tailles.values()),
        "taille_max": max(tailles.values()),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("trace")
    ap.add_argument("--clusters", type=int, default=8,
                    help="nombre de groupes visés (nœuds ou GPU disponibles)")
    ap.add_argument("--json", default="")
    ap.add_argument("--graine", type=int, default=1234)
    args = ap.parse_args()

    par_couche = lire(args.trace)
    couches = sorted(par_couche)
    ne = 1 + max(e for j in par_couche.values() for ex in j.values() for e in ex)
    n_jetons = len(par_couche[couches[0]])
    print(f"trace : {len(couches)} couches × {n_jetons} jetons · {ne} experts · "
          f"{len(next(iter(par_couche.values()))[0])} par jeton")
    print(f"découpage visé : {args.clusters} clusters\n")

    resultat = {"couches": {}, "clusters": args.clusters, "n_jetons": n_jetons,
                "n_experts": ne}
    entetes = (f"{'couche':>6} {'couv.':>6} {'vent.':>6} {'taille':>9} "
               f"{'couv.hasard':>12} {'couv.freq':>10} {'vent.hasard':>12}")
    print(entetes)
    print("-" * len(entetes))
    for l in couches:
        jetons = par_couche[l]
        co = co_activation(jetons, ne)
        freq = [sum(co[e]) for e in range(ne)]
        affectation, membres = partition_equilibree(co, ne, args.clusters, freq)
        m = mesurer(jetons, affectation, args.clusters)
        # témoin 1 : mêmes tailles, au hasard
        tailles = [len(x) for x in membres]
        liste = [e for x in membres for e in x]
        random.Random(args.graine + l).shuffle(liste)
        au_hasard, i2 = {}, 0
        for c, t in enumerate(tailles):
            for e in liste[i2:i2 + t]:
                au_hasard[e] = c
            i2 += t
        h = mesurer(jetons, au_hasard, args.clusters)
        # témoin 2 : groupé par FRÉQUENCE seule (sans regarder qui s'allume avec
        # qui) — le classement par fréquence décroissante découpé en tranches
        # égales. C'est le témoin qui compte : si la co-activation ne fait pas
        # mieux, le découpage n'apporte rien.
        ordre_freq = sorted(range(ne), key=lambda e: (-freq[e], e))
        taille = (ne + args.clusters - 1) // args.clusters
        par_freq = {e: min(args.clusters - 1, i // taille)
                    for i, e in enumerate(ordre_freq)}
        f = mesurer(jetons, par_freq, args.clusters)
        resultat["couches"][l] = {"appris": m, "hasard": h, "frequence": f,
                                  "affectation": affectation, "membres": membres}
        print(f"{l:>6} {m['couverture_moyenne']:>6.3f} {m['ventilation_moyenne']:>6.2f} "
              f"{m['taille_min']:>3}-{m['taille_max']:<5} {h['couverture_moyenne']:>12.3f} "
              f"{f['couverture_moyenne']:>10.3f} {h['ventilation_moyenne']:>12.2f}")

    # Accord entre la partition apprise et celle par fréquence : si elles
    # coïncident, la co-activation n'apporte rien que la fréquence ne donne.
    accords = []
    for l in couches:
        a = resultat["couches"][l]["affectation"]
        freq = [sum(co_activation(par_couche[l], ne)[e]) for e in range(ne)]
        ordre = sorted(range(ne), key=lambda e: (-freq[e], e))
        taille = (ne + args.clusters - 1) // args.clusters
        b = {e: min(args.clusters - 1, i // taille) for i, e in enumerate(ordre)}
        paires = [(x, y) for x in range(ne) for y in range(x + 1, ne)]
        accords.append(sum(1 for x, y in paires if (a[x] == a[y]) == (b[x] == b[y])) / len(paires))
    print(f"accord appris/fréquence (paires) : {sum(accords)/len(accords):.3f}")

    def moyenne(cle, source):
        return sum(resultat["couches"][l][source][cle]
                   for l in couches) / len(couches)
    print()
    for source in ("appris", "frequence", "hasard"):
        print(f"MOYENNE {source:>9} : couverture "
              f"{moyenne('couverture_moyenne', source):.3f} · ventilation "
              f"{moyenne('ventilation_moyenne', source):.2f}")
    if args.json:
        json.dump(resultat, open(args.json, "w"), indent=1)
        print(f"\n→ {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
