#!/usr/bin/env python3
"""ou_entre_la_langue.py — d'où vient l'axe de langue : entrée, réservoir, ou lecture ?

LA CONCLUSION DU §69, ET CE QU'ELLE EXIGE. Neuf moyens de post-traitement ont butté sur
la même frontière : les états du réservoir contiennent la structure contenu/langue, mais
**mêlée à la langue** d'une façon qu'aucune transformation linéaire ne démêle sans perdre
le contenu. Le §69 conclut qu'il faut **une caractéristique différente**, séparable par
construction.

**Mais avant de la concevoir, il faut savoir OÙ entre la langue.** Trois candidats, et
ils se départagent par une mesure :

  A. **L'ENTRÉE** — les plongements de couche 0 du professeur, qui portent l'écriture et
     la morphologie ;
  B. **LE RÉSERVOIR** — la dynamique récurrente, qui pourrait amplifier ou mêler ;
  C. **LA LECTURE** — l'ajustement lui-même, qui choisit quelles directions servent.

On mesure `P_cont/P_lang` sur la sortie obtenue à partir de trois jeux de
caractéristiques **emboîtés** :

  A. l'entrée seule          (aucun neurone)
  B. les états du réservoir  (ce qu'on utilise aujourd'hui)
  C. l'entrée ET les états

PRÉDICTION, ÉCRITE AVANT LA MESURE : si l'axe de langue vient de l'**entrée**, A aura un
rapport beaucoup plus bas que B et C, et le réservoir n'y sera pour rien. S'il vient de
la **dynamique**, A sera proche de B. S'il vient de la **lecture**, les trois se
ressembleront et c'est l'ajustement qu'il faudra revoir.

C'est la mesure qui dit où porter l'effort — et elle n'a pas été faite.

Usage : ou_entre_la_langue.py <cache_appr.npz> <cache_test.npz> [--neur 120]
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
    se = int(opt("--sous-ech", 5))

    cltr, Etr, Ytr, H = charge(tr_p)
    clte, Ete, Yte, _ = charge(te_p)
    vivant = np.zeros(Ytr[0].shape[1])
    for y in Ytr:
        vivant += ((y != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(Ytr)
    garde = np.where(vivant >= part)[0]
    Ytr = [y[:, garde] for y in Ytr]
    Yte = [y[:, garde] for y in Yte]

    centre = opt("--centre-entree", "") != ""
    if centre:
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
          f"{len(garde)} canaux")

    def ajuste_evalue(fait, nom):
        G = D = None
        ntot = 0
        for i in itr:
            A = fait(i, True)[::se]
            Z = Ytr[i][::se] - mt
            G = A.T @ A if G is None else G + A.T @ A
            D = A.T @ Z if D is None else D + A.T @ Z
            ntot += len(A)
        W = np.linalg.solve(G + ride*ntot*np.eye(G.shape[0]), D)
        blocs = [fait(k, False) @ W + mt for k in range(len(clte))]
        O = np.vstack(blocs)
        ft = cos_lignes(O, np.vstack(Yte))
        bornes = np.cumsum([0] + [len(Ete[k]) for k in range(len(clte))])
        dm = decompose(clte, moyennes(clte, O, bornes))
        print(f"  {nom:<34}{ft:>10.4f}{dm[0]:>10.1f}{dm[1]:>10.1f}{dm[2]:>10.3f}")
        return ft, dm

    Xa = P.recalcule(idx, Etr)
    Xt = P.recalcule(idx, Ete)
    quad = lambda A: np.hstack([A, A*A])  # noqa: E731

    print(f"\n# {'caractéristiques':<34}{'fid TEST':>10}{'P_lang':>10}"
          f"{'P_cont':>10}{'RAPPORT':>10}")
    ajuste_evalue(lambda i, tr: quad(np.asarray(Etr[i] if tr else Ete[i],
                                                dtype=np.float64)),
                  "A · l'ENTRÉE seule (0 neurone)")
    ajuste_evalue(lambda i, tr: quad(np.asarray(Xa[i] if tr else Xt[i],
                                                dtype=np.float64)),
                  "B · les ÉTATS du réservoir")
    ajuste_evalue(lambda i, tr: quad(np.hstack([
        np.asarray(Xa[i] if tr else Xt[i], dtype=np.float64),
        np.asarray(Etr[i] if tr else Ete[i], dtype=np.float64)])),
                  "C · ENTRÉE + ÉTATS")
    rq = decompose(clte, moyennes(clte, np.vstack(Yte),
                                  np.cumsum([0] + [len(Ete[k])
                                                   for k in range(len(clte))])))
    print(f"  {'PROFESSEUR (rappel)':<34}{'—':>10}{rq[0]:>10.1f}{rq[1]:>10.1f}"
          f"{rq[2]:>10.3f}")
    print(f"\n# PRÉDICTION : si A est proche de B et C, l'axe de langue vient de l'ENTRÉE")
    print(f"# et le réservoir n'y est pour rien. Si les trois se ressemblent, il vient de")
    print(f"# la LECTURE. Si A est bien plus haut, la dynamique l'ajoute.")
    print(f"# CRITÈRE (§62.3) : P_cont PROCHE du professeur ET P_lang qui ne le dépasse")
    print(f"# pas — le rapport seul peut être gonflé par le dénominateur.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
