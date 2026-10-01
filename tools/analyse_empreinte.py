#!/usr/bin/env python3
"""Chiffrer l'empreinte mémoire d'un MoE depuis une trace de routage.

    # 1. produire la trace (modèle en clusters ou GGUF ordinaire)
    DRAVE_TRACE_EXPERTS=/tmp/routage.txt ./drave-core/target/release/drave \\
        <modele|dossier> --ppl <ids.txt> --ctx 2048 --limit 2048 --dense --threads 10 --lot 1

    # 2. l'analyser
    python3 tools/analyse_empreinte.py /tmp/routage.txt
    python3 tools/analyse_empreinte.py /tmp/routage.txt --modele deepseek41

La trace est un texte : « couche jeton expert1 expert2 … ». Rien n'est deviné :
tout ce qui suit est calculé sur les appels réellement effectués.

Ce que l'outil rend, et pourquoi chaque chiffre compte :

* **la courbe succès/empreinte par couche** — combien d'experts garder pour
  servir X % des appels. C'est la seule mesure qui dimensionne un cache ;
* **le verdict sur l'allocation non uniforme** — la même courbe, mais avec les
  experts distribués par gain marginal, pour voir si cibler certaines couches
  paie (mesuré : non, +1,2 % au mieux) ;
* **la taille minimale utile d'un cache** — sous le top-k du routeur, un cache
  ne sert à rien : un jeton consomme ses k experts d'un coup ;
* **la structure périodique** — les experts se répètent-ils à intervalle
  régulier ? (mesuré sur Qwen3-30B : écart 12, Jaccard 0,32 contre 0,035 ailleurs) ;
* **l'extrapolation** — ce que ces chiffres donnent sur un autre modèle, en
  supposant la même concentration relative.
"""
import argparse
import collections
import sys


def charge(chemin, limite=None):
    trace = collections.defaultdict(dict)
    for ligne in open(chemin):
        p = ligne.split()
        if len(p) < 3:
            continue
        l, j = int(p[0]), int(p[1])
        if limite is not None and j >= limite:
            continue
        trace[l][j] = [int(e) for e in p[2:]]
    return trace


def courbe(exps_par_jeton, n_exp, capacite_max):
    """Taux de succès d'un cache LRU de taille t, pour t = 1..capacite_max."""
    res = {}
    for t in range(1, capacite_max + 1):
        cache = collections.OrderedDict()
        suc = tot = 0
        for exps in exps_par_jeton:
            for e in exps:
                if e in cache:
                    suc += 1
                    cache.move_to_end(e)
                else:
                    if len(cache) >= t:
                        cache.popitem(last=False)
                    cache[e] = 1
                tot += 1
        res[t] = suc / tot if tot else 0.0
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("trace")
    ap.add_argument("--limite", type=int, default=None,
                    help="ne lire que les N premiers jetons")
    ap.add_argument("--modele", default=None,
                    help="nom d'un modèle connu pour l'extrapolation "
                         "(deepseek4, deepseek41, qwen3moe)")
    args = ap.parse_args()

    trace = charge(args.trace, args.limite)
    if not trace:
        sys.exit("trace vide ou illisible")
    couches = sorted(trace)
    n_jet = min(len(v) for v in trace.values())
    if not all(len(v) == n_jet for v in trace.values()):
        print(f"[note] couches inégales : on tronque à {n_jet} jetons", file=sys.stderr)
    for l in couches:
        trace[l] = {j: e for j, e in trace[l].items() if j < n_jet}
    n_exp = max(max(e) for v in trace.values() for e in v.values()) + 1
    topk = len(next(iter(trace[couches[0]].values())))
    print(f"{len(couches)} couches · {n_jet} jetons · {n_exp} experts · top-{topk}")

    # --- courbe globale par couche -----------------------------------------
    print()
    print("=== EMPREINTE : experts à garder pour servir X % des appels ===")
    print(f"{'objectif':>9} " + " ".join(f"{p:>6}%" for p in (50, 70, 80, 90, 95, 99)))
    seuils = (0.50, 0.70, 0.80, 0.90, 0.95, 0.99)
    besoins = {p: [] for p in seuils}
    for l in couches:
        f = collections.Counter()
        for exps in trace[l].values():
            f.update(exps)
        a = sum(f.values())
        cum = 0
        trouve = {}
        for i, (_, c) in enumerate(f.most_common(), 1):
            cum += c
            for p in seuils:
                if p not in trouve and cum >= p * a:
                    trouve[p] = i
        for p in seuils:
            besoins[p].append(trouve.get(p, len(f)))
    moy = {p: sum(v) / len(v) for p, v in besoins.items()}
    print(f"{'experts':>9} " + " ".join(f"{moy[p]:>7.1f}" for p in seuils))
    print(f"{'% du total':>9} " + " ".join(f"{100*moy[p]/n_exp:>6.1f}%" for p in seuils))

    # --- cache réel (LRU), pas seulement la fréquence ----------------------
    print()
    print("=== CACHE LRU : taux de succès mesuré ===")
    par_couche = {l: list(trace[l].values()) for l in couches}
    C = {l: courbe(par_couche[l], n_exp, n_exp) for l in couches}
    for t in (topk, 16, 32, 64, 128):
        if t > n_exp:
            continue
        m = sum(C[l][t] for l in couches) / len(couches)
        print(f"  cache de {t:3d} experts ({100*t/n_exp:4.1f} %) : {100*m:5.1f} % de succès")
    if topk > 1:
        print(f"  (sous top-{topk}, un cache ne sert à RIEN : un jeton consomme")
        print(f"   ses {topk} experts d'un coup et le vide avant de resservir)")

    # --- allocation non uniforme -------------------------------------------
    print()
    print("=== ALLOCATION NON UNIFORME (le gain vaut-il la complexité ?) ===")
    def alloue(budget):
        taille = {l: topk for l in couches}
        reste = budget - topk * len(couches)
        while reste > 0:
            best, gain = None, 1e-9
            for l in couches:
                t = taille[l]
                if t >= n_exp:
                    continue
                g = C[l][t + 1] - C[l][t]
                if g > gain:
                    best, gain = l, g
            if best is None:
                break
            taille[best] += 1
            reste -= 1
        return taille
    for n_par_couche in (16, 32, 64):
        if n_par_couche > n_exp:
            continue
        budget = n_par_couche * len(couches)
        uni = sum(C[l][n_par_couche] for l in couches) / len(couches)
        ad = alloue(budget)
        ada = sum(C[l][ad[l]] for l in couches) / len(couches)
        print(f"  {n_par_couche:3d}/couche : uniforme {100*uni:5.1f} % · "
              f"adaptatif {100*ada:5.1f} % · gain {100*(ada-uni):+.1f} %")

    # --- structure périodique ----------------------------------------------
    print()
    print("=== STRUCTURE : les experts se répètent-ils entre couches ? ===")
    def jac(a, b):
        tot = 0.0
        for j in range(n_jet):
            A, B = trace[a].get(j), trace[b].get(j)
            if A and B:
                sa, sb = set(A), set(B)
                tot += len(sa & sb) / len(sa | sb)
        return tot / n_jet
    ecarts = collections.defaultdict(list)
    for a in couches:
        for b in couches:
            if b > a:
                ecarts[b - a].append(jac(a, b))
    meilleurs = sorted(ecarts.items(), key=lambda kv: -sum(kv[1]) / len(kv[1]))[:4]
    for e, vals in sorted(meilleurs):
        print(f"  écart {e:2d} : Jaccard moyen {sum(vals)/len(vals):.3f} "
              f"({len(vals)} paires)")
    ref = sum(ecarts[1]) / len(ecarts[1]) if 1 in ecarts else 0
    print(f"  écart  1 : Jaccard moyen {ref:.3f}  <- des couches VOISINES")
    print("  Un écart qui dépasse nettement ses voisins révèle une périodicité.")
    print("  Attention : ces experts sont des tenseurs DIFFÉRENTS — la")
    print("  périodicité dit qu'ils sont appelés ensemble, pas qu'ils sont")
    print("  interchangeables. Aucune économie de stockage directe.")

    # --- extrapolation ------------------------------------------------------
    if args.modele:
        connus = {
            "deepseek4":  (43, 256, 6, 5.51),     # (couches, experts, top-k, Mo/expert)
            "deepseek41": (40, 384, 6, 9.95),
            "qwen3moe":   (48, 128, 8, 3.05),
        }
        if args.modele not in connus:
            sys.exit(f"modèle inconnu : {args.modele} (connus : {', '.join(connus)})")
        nc, ne, tk, mo = connus[args.modele]
        total = nc * ne * mo / 1000
        print()
        print(f"=== EXTRAPOLATION à {args.modele} : {nc} couches · {ne} experts · "
              f"top-{tk} · {total:.0f} Go d'experts ===")
        print("  (on suppose la même concentration RELATIVE que celle mesurée ici)")
        print(f"  {'objectif':>9} {'% du total':>12} {'Go à garder':>13}")
        for p in seuils:
            part = moy[p] / n_exp
            print(f"  {100*p:>8.0f}% {100*part:>11.1f}% {part*total:>12.1f}")


if __name__ == "__main__":
    main()
