#!/usr/bin/env python3
"""peripherie_poursuite.py — C8, la TÂCHE FERMÉE : le signal injecté est-il dans la sortie ?

LA QUESTION. La porte de la périphérie vérifie que l'entrée est injectée, que la sortie est écrite
et que le délai est exact — elle ne dit **rien de la qualité**. La tâche fermée du plan
(`docs/plan-cerveau-complet.md` § C8) est de **poursuivre une consigne** : la sortie doit porter
le signal d'entrée, et si l'on demande un délai, elle doit porter **le signal d'il y a N pas**.

CE QUI EST MESURÉ, ET COMMENT. On ne suppose pas qu'un canal de sortie « est » la réponse : on
**apprend une lecture** (régression ridge) de l'état de sortie vers la valeur visée, sur la
**première moitié** des pas, et on mesure l'erreur sur la **seconde** (jamais vue). Trois
lectures, du plus facile au plus dur :

  1. `v[t]`      — le signal du pas courant : l'état le porte-t-il ?
  2. `v[t-N]`    — le signal d'il y a N pas (LA poursuite : mémoire du signal) ;
  3. `v[t+N]`    — le signal du pas suivant (pire cas : information qui n'existe pas encore).

La lecture 3 sert de **témoin** : une erreur basse y signalerait une fuite de protocole (le
modèle ne peut pas connaître l'avenir). C'est le même rôle que le contrôle de la borne exclue
dans la courbe de profondeur de C8.

Usage :
  tools/peripherie_poursuite.py --signal F --etats G[,H…] --delai N [--pas 64]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

import numpy as np


def lire_signal(chemin: str) -> np.ndarray:
    vals = []
    for l in pathlib.Path(chemin).read_text().splitlines():
        t = l.split("#")[0].strip()
        if not t:
            continue
        try:
            vals.append(float(t))
        except ValueError:
            continue
    if not vals:
        raise SystemExit(f"{chemin} : aucun signal lisible")
    return np.array(vals, dtype=np.float64)


def lire_etats(chemin: str, hidden: int | None = None) -> np.ndarray:
    octets = pathlib.Path(chemin).read_bytes()
    if hidden is None:
        # le moteur écrit un nombre ENTIER de pas ; on déduit la largeur en essayant les valeurs
        # plausibles (896 pour ce modèle) et en gardant celle qui divise exactement
        for h in (896, 1024, 2048, 4096, 768, 512, 256):
            if len(octets) % (4 * h) == 0:
                hidden = h
                break
        else:
            raise SystemExit(f"{chemin} : taille {len(octets)} non divisible — largeur inconnue")
    return np.frombuffer(octets, dtype="<f4").reshape(-1, hidden).astype(np.float64)


def ajuste(X: np.ndarray, y: np.ndarray, lam: float = 1.0) -> tuple[np.ndarray, float, float]:
    """Ridge fermé sur la première moitié, erreur sur la seconde. Rend (poids, rmse, r2)."""
    coupe = len(y) // 2
    Xtr, Xte, ytr, yte = X[:coupe], X[coupe:], y[:coupe], y[coupe:]
    moy, ect = Xtr.mean(0), Xtr.std(0) + 1e-6
    Xtr, Xte = (Xtr - moy) / ect, (Xte - moy) / ect
    ytr_c = ytr - ytr.mean()
    G = Xtr.T @ Xtr + lam * np.eye(Xtr.shape[1])
    w = np.linalg.solve(G, Xtr.T @ ytr_c)
    pred = Xte @ w + ytr.mean()
    err = pred - yte
    rmse = float(np.sqrt((err ** 2).mean()))
    var = float(((yte - yte.mean()) ** 2).mean())
    r2 = float(1.0 - (err ** 2).mean() / var) if var > 0 else float("nan")
    return w, rmse, r2


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--signal", required=True)
    ap.add_argument("--etats", required=True, help="un ou plusieurs fichiers d'états, séparés par des virgules")
    ap.add_argument("--delai", type=int, default=0, help="le délai demandé au moteur (pour la lecture 1)")
    ap.add_argument("--cachee", type=int, default=896)
    ap.add_argument("--lags", default="0,8,-1",
                    help="décalages à lire : `k` = v[t-k] (mémoire du signal), `-1` = v[t+1] (TÉMOIN)")
    a = ap.parse_args()

    v = lire_signal(a.signal)
    print(f"signal : {len(v)} valeurs · étendue [{v.min():.3f}, {v.max():.3f}]")

    for chemin in a.etats.split(","):
        X = lire_etats(chemin, a.cachee)
        n = min(len(X), len(v))
        X, vv = X[:n], v[:n]
        print(f"\n--- {chemin} : {n} pas × {X.shape[1]} canaux")
        for lag in [int(x) for x in a.lags.split(",")]:
            if lag >= 0:
                cible = np.array([vv[t - lag] if t >= lag else 0.0 for t in range(n)])
                nom = f"v[t-{lag}]" if lag else "v[t]  "
                # en mode statique, l'état ne dépend QUE de la valeur injectée : lire v[t-delai]
                # y est donc trivial, et c'est ce que le tableau montre (colonne de gauche).
                note = "  ← injecté" if lag == a.delai else ""
            else:
                k = -lag
                cible = np.array([vv[t + k] if t + k < n else 0.0 for t in range(n)])
                nom = f"v[t+{k}]"
                note = "  ← TÉMOIN : ne doit PAS être lisible"
            _, rmse, r2 = ajuste(X, cible)
            if lag < 0:
                verdict = "✅ (bas, attendu)" if r2 < 0.2 else "❌ FUITE"
            else:
                verdict = "✅" if r2 > 0.5 else "—"
            print(f"  lecture {nom:<7} RMSE {rmse:8.4f} · R² {r2:+.3f} {verdict}{note}")

    print("\nLecture : R² proche de 1 = l'état de sortie PORTE la valeur visée ; proche de 0 = il ne")
    print("la porte pas. Le témoin v[t+1] doit rester BAS : s'il monte, c'est le protocole qui fuit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
