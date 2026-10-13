#!/usr/bin/env python3
"""predictibilite_etats.py — un état PRÉCOCE prédit-il un état PROFOND ?

POURQUOI CETTE MESURE. La question N4 (« entraîner le chemin court ») suppose que sortir tôt
**perd** de l'information. Deux mesures de la journée la soutiennent déjà (la courbe de profondeur :
×1,14 à ×2,00 par 4 couches ; et la capacité qui ne remplace pas les données). Celle-ci demande à
l'état lui-même : ce que la profondeur ajoute est-il **déjà dans l'état précoce** (auquel cas un
lecteur suffirait), ou est-il **créé** par les couches intermédiaires (auquel cas il faut les
entraîner) ?

LA RÉPONSE, mesurée le 13/10 sur 33 morceaux (30 d'entraînement, 3 de test jamais vus), régression
ridge linéaire, R² sur le test :

    profondeur  8 → 16 : R² = 0,6547   (identité : 0,1913)
    profondeur 16 →  8 : R² = 0,7226   (identité : −0,4997)
    profondeur  8 → 12 : R² = 0,7825
    profondeur 12 → 16 : R² = 0,7531

Deux lectures : (1) **65 % de l'état profond est linéairement déterminé par l'état précoce** — il
n'est donc pas créé par la profondeur ; (2) mais les **pas élémentaires** (8→12, 12→16) sont mieux
prédits que le saut direct (8→16), donc la composition n'est **pas** linéaire : ~35 % de la variance
profonde **apparaît** dans les couches intermédiaires. C'est le manque N4, chiffré.

Usage : predictibilite_etats.py --profond <préfixe> --precoce <préfixe> [--intermediaire <préfixe>]
        [--entrain 30] [--test 3]
Les préfixes sont ceux des `--etat-sortie` du moteur (`PREFIXE.<position>`), lus par la lecture
PARTAGÉE du dépôt (`tools/lecture_etat.py`) comme tout le reste.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lecture_etat import charger_etats  # noqa: E402


def r2(Y: np.ndarray, Yhat: np.ndarray) -> float:
    return 1.0 - ((Y - Yhat) ** 2).sum() / ((Y - Y.mean(axis=0)) ** 2).sum()


def ajuste(X: np.ndarray, Y: np.ndarray, lam: float = 1e-3) -> np.ndarray:
    """Ridge avec biais : (X|1) → Y. `lam` est relatif (multiplié par n)."""
    n, d = X.shape
    Xb = np.hstack([X, np.ones((n, 1), dtype=X.dtype)])
    return np.linalg.solve(Xb.T @ Xb + lam * n * np.eye(d + 1, dtype=X.dtype), Xb.T @ Y)


def applique(W: np.ndarray, X: np.ndarray) -> np.ndarray:
    return np.hstack([X, np.ones((X.shape[0], 1), dtype=X.dtype)]) @ W


def charge(base: pathlib.Path, morceaux: list[int]) -> np.ndarray:
    return np.vstack([charger_etats(str(base / f"etat-m{i}"))[1] for i in morceaux])


def main() -> int:
    a = argparse.ArgumentParser()
    a.add_argument("--precoce", required=True, help="dossier des états de la profondeur PRÉCOCE")
    a.add_argument("--profond", required=True, help="dossier des états de la profondeur PROFONDE")
    a.add_argument("--intermediaire", default=None, help="dossier d'une profondeur intermédiaire")
    a.add_argument("--entrain", type=int, default=30, help="morceaux d'entraînement (les premiers)")
    a.add_argument("--test", type=int, default=3, help="morceaux de test (les suivants)")
    o = a.parse_args()
    tr = list(range(o.entrain))
    te = list(range(o.entrain, o.entrain + o.test))
    print(f"  morceaux : {len(tr)} d'entraînement, {len(te)} de test")
    Xtr, Ytr = charge(pathlib.Path(o.precoce), tr), charge(pathlib.Path(o.profond), tr)
    Xte, Yte = charge(pathlib.Path(o.precoce), te), charge(pathlib.Path(o.profond), te)
    print(f"  états : {Xtr.shape[0]} positions × {Xtr.shape[1]} canaux")
    print(f"  précoce → profond : R² TEST = {r2(Yte, applique(ajuste(Xtr, Ytr), Xte)):.4f}"
          f"  (identité : {r2(Yte, Xte):.4f})")
    print(f"  profond → précoce : R² TEST = {r2(Xte, applique(ajuste(Ytr, Xtr), Yte)):.4f}"
          f"  (identité : {r2(Xte, Yte):.4f})")
    if o.intermediaire:
        Ztr = charge(pathlib.Path(o.intermediaire), tr)
        Zte = charge(pathlib.Path(o.intermediaire), te)
        print(f"  précoce → intermédiaire : R² TEST = {r2(Zte, applique(ajuste(Xtr, Ztr), Xte)):.4f}")
        print(f"  intermédiaire → profond : R² TEST = {r2(Yte, applique(ajuste(Ztr, Ytr), Zte)):.4f}")
        print("  (si les pas élémentaires sont MIEUX prédits que le saut direct, la composition "
              "n'est pas linéaire : la profondeur CRÉE de l'information)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
