#!/usr/bin/env python3
"""ancre_professeur.py — le rapport contenu/langue du professeur, et de quoi il dépend.

POURQUOI CET OUTIL EXISTE. Le rapport `P_cont/P_lang` est devenu le chiffre central du
projet — « le professeur est à 12,001, notre pont à 2,487 ». Or ce chiffre n'est PAS une
propriété du professeur seul : il dépend du PANEL DE LANGUES sur lequel on le mesure.
Sur trois langues romanes (es/it/pt) la langue est un axe faible et le rapport explose ;
sur six langues qui incluent deux germaniques, l'axe de langue est bien plus énergique et
le rapport s'effondre. Comparer un chiffre mesuré sur trois langues romanes à un chiffre
mesuré sur six langues n'a aucun sens — et c'est exactement ce que fait le rapport.

Cet outil rend la dépendance VISIBLE au lieu de la laisser dans un coin : il donne le
rapport pour chaque sous-ensemble de langues, en poolant sur les positions comme le fait
`discriminant_contenu.moyennes`.

FORMAT DU CHIFFRE. Le professeur est ici lu dans un CACHE (`cache_pont.py`) : `E` = la
couche d'entrée, `Y` = la couche cible, une ligne par position. On moyenne chaque entrée
sur ses positions, puis :
    P_lang = moyenne, sur les langues, de ‖moyenne_de_la_langue − moyenne_globale‖²
    P_cont = moyenne, sur les contenus, de ‖moyenne_du_contenu − moyenne_globale‖²

DEUX MASQUES, ET LEQUEL EST LE BON. `discriminant_contenu` restreint les canaux à ceux
« vivants » dans au moins la moitié des entrées (`--part 0,5`). Ce masque change P_lang
et P_cont — donc tout chiffre cité doit dire s'il est masqué ou non. Les deux sont
affichés.

Usage : ancre_professeur.py <cache.npz> [--part 0.5] [--sans-masque]
"""
import os
import sys
from itertools import combinations

import numpy as np


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def charge(p):
    z = np.load(p, allow_pickle=True)
    cles = [str(c) for c in z["cles"]]
    E = [z[f"E{i}"].astype(np.float64) for i in range(len(cles))]
    Y = [z[f"Y{i}"].astype(np.float64) for i in range(len(cles))]
    return cles, E, Y, int(z["hidden"])


def moyennes(V):
    """Une ligne par entrée : la moyenne de ses positions."""
    return np.vstack([v.mean(0) for v in V])


def decompose(noms, M):
    """(P_lang, P_cont, rapport) sur les moyennes par entrée, sous-ensemble de langues."""
    m = M.mean(0)
    par_l, par_c = {}, {}
    for i, n in enumerate(noms):
        L, _, k = n.partition("_")
        par_l.setdefault(L, []).append(i)
        par_c.setdefault(k, []).append(i)
    comm = [k for k, idx in par_c.items() if len(idx) == len(par_l)]
    if not comm or len(par_l) < 2:
        return None
    Pl = float(np.mean([np.sum((M[idx].mean(0) - m)**2) for idx in par_l.values()]))
    Pc = float(np.mean([np.sum((M[par_c[k]].mean(0) - m)**2) for k in comm]))
    return Pl, Pc, Pc/max(Pl, 1e-12)


def langues_de(noms):
    return {n.partition("_")[0] for n in noms}


def main():
    chemin = sys.argv[1]
    part = float(opt("--part", 0.5))
    cles, E, Y, hid = charge(chemin)
    print(f"# {len(cles)} entrées · {hid} canaux · {chemin}")
    print(f"# langues : {', '.join(sorted(langues_de(cles)))}")

    vivant = np.zeros(Y[0].shape[1])
    for y in Y:
        vivant += ((y != 0).mean(0) >= 0.05).astype(float)
    vivant /= len(Y)
    garde = np.where(vivant >= part)[0]

    variantes = [("tous canaux", np.arange(hid))]
    if len(garde) and len(garde) < hid:
        variantes.append((f"masque vivant ≥{part:.2f}", garde))

    for nom_masque, idx in variantes:
        Mm = moyennes([y[:, idx] for y in Y])
        tous = sorted(langues_de(cles))
        print(f"\n=== {nom_masque} — {len(idx)} canaux ===")
        r = decompose(cles, Mm)
        print(f"  {'6 langues (toutes)':<26}" if len(tous) > 3 else
              f"  {'langues du cache':<26}", end="")
        print(f"P_lang {r[0]:>9.1f} · P_cont {r[1]:>9.1f} · RAPPORT {r[2]:>8.3f}")
        if len(tous) > 3:
            for k in range(2, len(tous)+1):
                vals = []
                for combo in combinations(tous, k):
                    sel = [i for i, n in enumerate(cles)
                           if n.partition("_")[0] in combo]
                    if len(sel) < 4:
                        continue
                    rr = decompose([cles[i] for i in sel], Mm[sel])
                    if rr:
                        vals.append(rr[2])
                if vals:
                    print(f"  {'  ' + str(k) + ' langues quelconques':<26}"
                          f"rapport min {min(vals):>6.2f} · médian "
                          f"{np.median(vals):>6.2f} · max {max(vals):>6.2f} "
                          f"· {len(vals)} combinaisons")
    return 0


if __name__ == "__main__":
    sys.exit(main())
