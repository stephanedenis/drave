#!/usr/bin/env python3
"""analyse_reutilisation_experts.py — la réutilisation des experts, mesurée.

Lit une trace de routage (`DRAVE_TRACE_EXPERTS=chemin` : une ligne par
(couche, jeton), `couche jeton e1 e2 …`) et répond à LA question qui décide si un
cache d'experts peut servir un modèle trop gros pour tenir en mémoire :

    les mêmes experts reviennent-ils d'un jeton à l'autre ?

Ce qu'il rend, par couche et globalement :

  - la **couverture** : combien d'experts DISTINCTS sont touchés sur N jetons ;
  - la **réutilisation immédiate** : part des experts du jeton t déjà vus au
    jeton t−1 (le chiffre qui compte pour un cache LRU sans réentraînement) ;
  - la **réutilisation à distance** : part des experts du jeton t déjà vus dans
    les k jetons précédents (k = 1, 4, 16, tout) ;
  - la **courbe d'un cache LRU** : pour une capacité donnée (en experts par
    couche), le taux de succès mesuré — donc les octets économisés par jeton.

Usage :
    analyse_reutilisation_experts.py <trace> [--experts-par-jeton N] [--couches-totales N]
"""
import sys
from collections import Counter, OrderedDict


def lire(chemin):
    """Rend {couche: {jeton: [experts]}}."""
    par_couche = {}
    with open(chemin) as f:
        for ligne in f:
            p = ligne.split()
            if len(p) < 3:
                continue
            l, j = int(p[0]), int(p[1])
            par_couche.setdefault(l, {})[j] = [int(x) for x in p[2:]]
    return par_couche


def lru_taux(suite, capacite):
    """Taux de succès d'un cache LRU de `capacite` experts, sur la suite de
    jetons (chacun étant une liste d'experts)."""
    cache = OrderedDict()
    touche = total = 0
    for experts in suite:
        for e in experts:
            total += 1
            if e in cache:
                touche += 1
                cache.move_to_end(e)
            else:
                cache[e] = True
                if len(cache) > capacite:
                    cache.popitem(last=False)
    return touche / total if total else 0.0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    chemin = sys.argv[1]
    par_couche = lire(chemin)
    if not par_couche:
        print("trace vide")
        return 2
    n_jetons = max(len(v) for v in par_couche.values())
    k_par_jeton = max(len(e) for v in par_couche.values() for e in v.values())
    n_experts = max(e for v in par_couche.values() for lst in v.values() for e in lst) + 1
    print(f"{chemin} : {len(par_couche)} couches · {n_jetons} jetons · "
          f"{k_par_jeton} experts par jeton · indices jusqu'à {n_experts - 1}")

    # --- global ---
    dist = set()
    immediat = immediat_tot = 0
    for l, v in par_couche.items():
        js = sorted(v)
        for a, b in zip(js, js[1:]):
            sa, sb = set(v[a]), set(v[b])
            immediat += len(sa & sb)
            immediat_tot += len(sb)
            dist |= sb
    print(f"\n  experts DISTINCTS touchés (toutes couches) : {len(dist)}")
    print(f"  réutilisation IMMÉDIATE (t−1 → t) : "
          f"{100 * immediat / max(immediat_tot, 1):.1f} %")

    for fenetre in (2, 4, 8, 16, 10**9):
        vu, bon, tot = {}, 0, 0
        for l, v in par_couche.items():
            js = sorted(v)
            historique = []
            for j in js:
                s = set(v[j])
                vus = {e for lst in historique[-fenetre:] for e in lst}
                bon += len(s & vus)
                tot += len(s)
                historique.append(v[j])
        print(f"  réutilisation dans une fenêtre de {fenetre if fenetre < 10**9 else 'N'} "
              f"jetons : {100 * bon / max(tot, 1):.1f} %")

    # --- cache LRU : combien d'experts par couche pour quel taux ---
    print(f"\n  {'capacité/couche':>16} {'taux de succès':>15} {'octets/jeton':>14}")
    # octets par expert : déduit de la trace ? non — on rend le TAUX, et
    # l'appelant multiplie par les octets d'un expert (outil de budget).
    for cap in (2, 4, 8, 16, 32, 64, 128, 256, 512, 1024):
        taux = [lru_taux([par_couche[l][j] for j in sorted(par_couche[l])], cap)
                for l in sorted(par_couche)]
        m = sum(taux) / len(taux)
        print(f"  {cap:16d} {100 * m:14.1f} % {'':>14}")
    print("\n  (les octets/jeton se calculent en multipliant (1 − taux) par les "
          "octets d'experts par jeton — voir tools/budget_execution_locale.py)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
