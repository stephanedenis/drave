#!/usr/bin/env python3
"""peripherie_memoire.py — C8 : la mémoire du signal est-elle APPRENABLE ?

LA QUESTION, ET ELLE EST PRÉCISE. La lecture LINÉAIRE de l'état de sortie ne retrouve pas le
signal d'il y a N pas (`R² = −0,973`, fiche `rapport-c8-peripherie.md`) : le modèle ne le garde
pas. Mais une lecture linéaire qui échoue ne prouve pas que l'information est absente — elle
prouve qu'elle n'est pas **linéairement** accessible depuis cet état. C'est exactement la leçon de
la sonde C8, où la même question s'était posée pour le prochain jeton.

CE QUI EST MESURÉ. Trois lectures du MÊME état, du plus faible au plus fort :

  1. **linéaire** (ridge fermé) — la référence, déjà connue : elle échoue ;
  2. **non linéaire** (perceptron 896→K→1, GELU) — l'information est-elle là, mais tordue ?
  3. **témoin** : la même lecture non linéaire vers `v[t+1]` (l'avenir). S'il devient lisible,
     c'est le protocole qui fuit, pas la mémoire qui existe.

Et un second témoin, plus fin : la lecture de `v[t]` (le signal courant). Si le réseau n'apprend
même pas à lire le PRÉSENT, l'échec sur le passé ne dit rien de la mémoire.

Usage :
  tools/peripherie_memoire.py --signal F --etats G --lag 8 [--cachee 256] [--epoques 300]
"""
from __future__ import annotations

import argparse
import pathlib
import sys

import numpy as np
import torch


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


def lire_etats(chemin: str, hidden: int = 896) -> np.ndarray:
    octets = pathlib.Path(chemin).read_bytes()
    if len(octets) % (4 * hidden):
        raise SystemExit(f"{chemin} : {len(octets)} octets non divisibles par 4×{hidden}")
    return np.frombuffer(octets, dtype="<f4").reshape(-1, hidden).astype(np.float64)


def cible(v: np.ndarray, lag: int) -> np.ndarray:
    n = len(v)
    if lag >= 0:
        return np.array([v[t - lag] if t >= lag else 0.0 for t in range(n)])
    k = -lag
    return np.array([v[t + k] if t + k < n else 0.0 for t in range(n)])


def ridge(Xtr, ytr, Xte) -> tuple[np.ndarray, float]:
    moy, ect = Xtr.mean(0), Xtr.std(0) + 1e-6
    A, B = (Xtr - moy) / ect, (Xte - moy) / ect
    yc = ytr - ytr.mean()
    w = np.linalg.solve(A.T @ A + np.eye(A.shape[1]), A.T @ yc)
    return B @ w + ytr.mean(), float(w @ w)


def mlp(Xtr, ytr, Xte, cachee: int, epoques: int, graine: int = 0):
    torch.manual_seed(graine)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    moy, ect = Xtr.mean(0), Xtr.std(0) + 1e-6
    Xa = torch.from_numpy((Xtr - moy) / ect).float().to(dev)
    Xb = torch.from_numpy((Xte - moy) / ect).float().to(dev)
    ya = torch.from_numpy(ytr - ytr.mean()).float().to(dev).unsqueeze(1)
    net = torch.nn.Sequential(
        torch.nn.Linear(Xa.shape[1], cachee), torch.nn.GELU(), torch.nn.Linear(cachee, 1)
    ).to(dev)
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    for _ in range(epoques):
        opt.zero_grad()
        perte = torch.nn.functional.mse_loss(net(Xa), ya)
        perte.backward()
        opt.step()
    with torch.no_grad():
        pred = net(Xb).squeeze(1).cpu().numpy() + ytr.mean()
    return pred, dev


def metriques(pred: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    err = pred - y
    rmse = float(np.sqrt((err ** 2).mean()))
    var = float(((y - y.mean()) ** 2).mean())
    return rmse, (float(1 - (err ** 2).mean() / var) if var > 0 else float("nan"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--signal", required=True)
    ap.add_argument("--etats", required=True)
    ap.add_argument("--lag", type=int, default=8, help="le décalage à lire (8 = il y a 8 pas)")
    ap.add_argument("--cachee", type=int, default=256)
    ap.add_argument("--epoques", type=int, default=300)
    ap.add_argument("--graine", type=int, default=0)
    a = ap.parse_args()

    v = lire_signal(a.signal)
    X = lire_etats(a.etats)
    n = min(len(X), len(v))
    X, v = X[:n], v[:n]
    print(f"signal : {n} pas · états : {X.shape[1]} canaux · décalage lu : {a.lag}")

    coupe = n // 2
    print(f"apprentissage sur les {coupe} premiers pas, mesure sur les {n - coupe} derniers\n")
    print(f"{'cible':<26} {'lecture':<12} {'RMSE':>9} {'R²':>8}")
    for nom, lag in (("v[t]   (le présent)", 0), (f"v[t-{a.lag}] (la mémoire)", a.lag),
                     ("v[t+1] (TÉMOIN avenir)", -1)):
        y = cible(v, lag)
        ytr, yte = y[:coupe], y[coupe:]
        pl, _ = ridge(X[:coupe], ytr, X[coupe:])
        rmse_l, r2_l = metriques(pl, yte)
        pn, dev = mlp(X[:coupe], ytr, X[coupe:], a.cachee, a.epoques, a.graine)
        rmse_n, r2_n = metriques(pn, yte)
        print(f"{nom:<26} {'linéaire':<12} {rmse_l:9.4f} {r2_l:+8.3f}")
        print(f"{'':<26} {'non linéaire':<12} {rmse_n:9.4f} {r2_n:+8.3f}")

    print(f"\nappareil : {dev}")
    print("Lecture : si le PRÉSENT est lisible et la MÉMOIRE non, l'information n'est pas dans")
    print("l'état — aucun entraînement de lecture ne la fera apparaître. Si le TÉMOIN avenir est")
    print("lisible, c'est le protocole qui fuit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
