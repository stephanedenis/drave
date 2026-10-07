#!/usr/bin/env python3
"""renforcement_directions.py — la réserve du §72 : apprendre QUOI LIRE.

LA SEULE RÉSERVE QUI RESTAIT. Le §72 a testé **la forme de renforcement implémentée
dans le dépôt** — mettre à l'échelle les poids d'un neurone selon sa capture du résidu —
et elle échoue : +1,7 % du chemin nécessaire, plateau dès la deuxième passe. La raison
était nette : la capture moyenne vaut ≈ 0,5, **aucun neurone ne capte le résidu mieux
que le hasard**, donc aucun n'est franchement renforcé.

**Mais mettre à l'échelle ne change PAS ce qu'un neurone lit** — seulement l'amplitude
de ce qu'il lit déjà. Or si aucun neurone ne capte le résidu, c'est peut-être qu'aucun
ne lit la bonne direction de l'entrée.

LA FORME DIFFÉRENTE, testée ici. On apprend à chaque neurone **la direction de l'entrée
qui prédit le résidu**, par corrélation seule :

    G = Eᵀ·R          (H × canaux) — covariance croisée entrée / résidu
    SVD(G) = U·S·Vᵀ   — les colonnes de U sont les directions de l'entrée
                        les plus prédictives du résidu
    B_j ← U[:, j]     — chaque neurone reçoit SA direction

**Aucune rétropropagation** : `G` est une corrélation entre l'entrée et le résidu, et
chaque neurone ne reçoit qu'une direction. C'est la règle de Hebb appliquée à l'entrée
du réservoir, et c'est **local** — `G` ne dépend d'aucun gradient à travers la lecture.

PRÉDICTION, ÉCRITE AVANT LA MESURE : si l'échec du §72 venait de ce que les neurones
lisent des directions aléatoires, alors leur donner les directions prédictives doit faire
**monter la capture du résidu au-dessus de 0,5** et **monter le rapport** vers 10,912.

Si la capture reste à 0,5 et le rapport à 1,3, alors le réservoir ne peut pas être
réparé par ce qu'on lui fait lire non plus — et la conclusion du §72 serait confirmée
sur une seconde forme, indépendante.

Usage : renforcement_directions.py <cache_appr.npz> <cache_test.npz> [--neur 120]
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
    passes = int(opt("--passes", 5))
    melange = float(opt("--melange", 1.0))   # 0 = directions aléatoires, 1 = apprises

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

    # COMPOSITION DES TROIS LEVIERS DÉPLOYABLES : le centrage agit sur l'ENTRÉE (§64),
    # « apprendre quoi lire » sur les CARACTÉRISTIQUES (§73), le discriminant sur la
    # LECTURE (§69). Trois aspects différents, trois mécanismes dans les règles.
    if opt("--centre-entree", "") != "":
        Etr = [e - e.mean(0, keepdims=True) for e in Etr]
        Ete = [e - e.mean(0, keepdims=True) for e in Ete]
        print("# CENTRAGE DE L'ENTRÉE activé (§64)")
    # RETRAIT DU SOUS-ESPACE DE LANGUE DANS LES ÉTATS (§66), si demandé
    r_etats = int(opt("--rang-etats", 0))

    P = Pont((cltr, Etr, Ytr), 0.2, graine, len(garde))
    P.quadratique = True
    P.a_min, P.a_max = 0.02, 0.8
    P.nait(n_neur, True)
    idx = np.arange(P.compte_neurones)
    print(f"# réseau {P.compte_neurones} neurones · {len(P.couches)} couche(s) · "
          f"canaux d'entrée {H} · {passes} passes")

    bo_t = np.cumsum([0] + [len(Yte[k]) for k in range(len(clte))])
    rq = decompose(clte, moyennes(clte, np.vstack(Yte), bo_t))
    print(f"# CIBLE — professeur : P_lang {rq[0]:.1f} · P_cont {rq[1]:.1f} · "
          f"rapport {rq[2]:.3f}")

    Ea = np.vstack([np.asarray(Etr[i], dtype=np.float64) for i in itr])
    Ya = np.vstack([Ytr[i] for i in itr])

    def capte(W):
        X = np.vstack([P.X[i] for i in itr])
        R = Ya - (P.phi(X) @ W + mt)
        b_ = R - R.mean(0)
        nb = np.linalg.norm(b_, axis=0)
        ok = (nb > 0) & np.isfinite(nb)
        cs = []
        for j in range(P.compte_neurones):
            xj = np.concatenate([P.X[i][:, j] for i in itr]).astype(np.float64)
            a_ = xj - xj.mean()
            na = float(np.linalg.norm(a_))
            cs.append(float(np.abs(a_ @ b_[:, ok]).max()/(na*nb[ok].max()))
                      if na > 0 and ok.any() else 0.0)
        return float(np.mean(cs)), R

    print(f"\n# {'passe':>6}{'capture':>9}{'fid TEST':>10}{'P_lang':>10}"
          f"{'P_cont':>10}{'RAPPORT':>10}{'  s'}")
    W = P.ajuste(idx, ride, mt, itr)
    cap, R = capte(W)
    Xt = P.recalcule(idx, Ete)
    Ot = np.vstack([P.phi(P._norm(Xt[k])) @ W + mt for k in range(len(clte))])
    ft = cos_lignes(Ot, np.vstack(Yte))
    dm = decompose(clte, moyennes(clte, Ot, bo_t))
    print(f" {0:>6}{cap:>9.3f}{ft:>10.4f}{dm[0]:>10.1f}{dm[1]:>10.1f}{dm[2]:>10.3f}")

    for k in range(passes):
        t = time.time()
        # LES DIRECTIONS DE L'ENTRÉE QUI PRÉDISENT LE RÉSIDU — corrélation seule
        G = Ea.T @ (R - R.mean(0))                 # (H, canaux)
        U, S, Vt = np.linalg.svd(G, full_matrices=False)
        kk = min(P.compte_neurones, U.shape[1])
        for j in range(P.compte_neurones):
            d = U[:, j % kk]
            w_par, w_self, bb, c = P.poids[j]
            b_new = (1.0 - melange)*bb + melange*d*float(np.linalg.norm(bb))
            P.poids[j] = (w_par, w_self, b_new, c)
        P.X = P.recalcule(idx, P.E)
        W = P.ajuste(idx, ride, mt, itr)
        cap, R = capte(W)
        Xt = P.recalcule(idx, Ete)
        Ot = np.vstack([P.phi(P._norm(Xt[k])) @ W + mt for k in range(len(clte))])
        ft = cos_lignes(Ot, np.vstack(Yte))
        dm = decompose(clte, moyennes(clte, Ot, bo_t))
        print(f" {k+1:>6}{cap:>9.3f}{ft:>10.4f}{dm[0]:>10.1f}{dm[1]:>10.1f}"
              f"{dm[2]:>10.3f}{time.time()-t:>6.0f}")
    # ------------------------------- COMBINAISON AVEC LE DISCRIMINANT (§69)
    #
    # « Apprendre quoi lire » agit sur les CARACTÉRISTIQUES ; le discriminant agit sur
    # la LECTURE. Le §69 a montré que le discriminant optimise le rapport en écrasant le
    # contenu (P_cont 30,2) ; le §73 a montré que les directions d'entrée font MONTER
    # P_cont. Les deux devraient donc être complémentaires — et leur combinaison n'avait
    # jamais été essayée.
    print(f"\n=== COMBINAISON : quoi lire PUIS discriminant ===")
    # ATTENTION À L'ESPACE : le discriminant du §69 vit dans l'espace des SORTIES
    # (896 canaux), pas dans celui des états (120). La première version prenait
    # `P.X[i].mean(0)` — 120 dimensions — et la projection échouait. On calcule donc
    # les moyennes sur les SORTIES d'apprentissage.
    Xa2 = P.recalcule(idx, Etr)
    Oa2 = np.vstack([P.phi(P._norm(Xa2[j])) @ W + mt for j in range(len(cltr))])
    bo_a2 = np.cumsum([0] + [len(Ytr[i]) for i in range(len(cltr))])
    Ma = np.vstack([Oa2[bo_a2[j]:bo_a2[j+1]].mean(0) for j in range(len(cltr))])
    ma = Ma.mean(0)
    pc, pl = {}, {}
    for r2, n in enumerate(cltr):
        L, _, kk2 = n.partition("_")
        pc.setdefault(kk2, []).append(r2)
        pl.setdefault(L, []).append(r2)
    pc = {k2: v for k2, v in pc.items() if len(v) == len(pl)}
    def covg(M, par, m):
        C = np.zeros((M.shape[1], M.shape[1]))
        for idxg in par.values():
            d = M[idxg].mean(0) - m
            C += np.outer(d, d)
        return C/max(len(par), 1)
    Cc, Cl = covg(Ma, pc, ma), covg(Ma, pl, ma)
    lam = 1e-2*float(np.trace(Cl))/Ma.shape[1]
    w2, V2 = np.linalg.eigh(np.linalg.solve(Cl + max(lam, 1e-12)*np.eye(Ma.shape[1]), Cc))
    V2 = V2[:, np.argsort(-w2)]
    Xt2 = P.recalcule(idx, Ete)
    Ot2 = np.vstack([P.phi(P._norm(Xt2[k])) @ W + mt for k in range(len(clte))])
    print(f"# {'rang':>6}{'fid TEST':>10}{'P_lang':>10}{'P_cont':>10}{'RAPPORT':>10}")
    for r3 in (2, 5, 10, 20):
        Vr = V2[:, :r3]
        Oc = (Ot2 - ma) @ Vr @ Vr.T + ma
        f3 = cos_lignes(Oc, np.vstack(Yte))
        d3 = decompose(clte, moyennes(clte, Oc, bo_t))
        print(f" {r3:>6}{f3:>10.4f}{d3[0]:>10.1f}{d3[1]:>10.1f}{d3[2]:>10.3f}")
    print(f"# Comparaison : discriminant SEUL (§69, sans apprentissage des directions)")
    print(f"#   rang 2 : fid 0,4341 · P_lang 4,3 · P_cont 30,2 · rapport 6,961")
    print(f"#   rang 20 : fid 0,4575 · P_lang 17,4 · P_cont 57,9 · rapport 3,326")
    print(f"\n# La capture est la moyenne, sur les neurones, de leur corrélation maximale")
    print(f"# avec le résidu. 0,5 = le hasard. Le §72 trouvait ≈ 0,5 et un plateau.")
    print(f"# PRÉDICTION : si l'échec venait de directions aléatoires, la capture doit")
    print(f"# monter au-dessus de 0,5 et le rapport vers 10,912.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
