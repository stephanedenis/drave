#!/usr/bin/env python3
"""c8_sonde_lineaire.py — C8 : que peut lire une TÊTE sur un état intermédiaire ?

LA QUESTION. Le réflexe mesuré jusqu'ici emprunte la tête du modèle et lit l'état de la couche
16 : perplexité **728 388** contre **9,43** pour le modèle complet (mesuré le 2026-10-10). Mais
cela ne dit pas si l'état *contient* l'information, ou si c'est la TÊTE qui ne sait pas la lire.
La sonde répond à la seconde question, et elle est linéaire : **quelle part du prochain jeton
est LINÉAIREMENT décodable depuis l'état de la couche 16 ?**

PROTOCOLE.
  1. `drave --couches 0:15 --tete-partielle --etat-sortie F --etat-pos 4,5,…` écrit l'état de
     la couche 16 (896 f32, juste avant la norme finale) à chaque position ;
  2. la cible est le jeton SUIVANT du corpus (apprentissage supervisé ordinaire) ;
  3. la sonde est une régression ridge fermée (W = (XᵀX + λI)⁻¹ Xᵀ Y), entraînée sur la moitié
     des positions, évaluée sur l'autre — **aucune fuite** : les positions de test ne sont pas
     vues à l'entraînement ;
  4. les classes sont les K jetons les plus fréquents du corpus (K réglable), et la référence
     est la classe majoritaire (« toujours le jeton le plus fréquent »), plus la fréquence
     moyenne des cibles.

CE QU'ELLE MESURE, ET CE QU'ELLE NE MESURE PAS. Elle mesure la **décodabilité linéaire** : si
elle est proche du hasard, une tête entraînée n'y changera rien (l'information n'est pas là) ;
si elle est nette, alors la tête empruntée est bien le maillon faible, et C8 a un sens. Elle ne
mesure PAS ce qu'une tête **non linéaire** entraînée atteindrait — c'est l'étape d'après.

Usage : tools/c8_sonde_lineaire.py --etats /tmp/c8/etat --ids F --limite 1024 [--classes 256]
"""
from __future__ import annotations

import argparse
import pathlib
import struct
import sys

import numpy as np


def charger_ids(chemin: str, limite: int) -> np.ndarray:
    """Les identifiants du corpus. Le fichier est de la même forme que celle lue par le moteur :
    des entiers, un par ligne (format des `ids` de la campagne)."""
    # Les `ids` de la campagne sont un CSV sur UNE ligne (séparateur virgule, pas de retour
    # ligne) : un découpage sur les blancs ne lit alors RIEN — et la sonde, elle, mesurait
    # « 0 position » au lieu de le dire. On accepte les deux formes, virgules et blancs.
    import re
    texte = pathlib.Path(chemin).read_text()
    vals = []
    for morceau in re.split(r"[,\s]+", texte):
        if not morceau:
            continue
        try:
            vals.append(int(morceau))
        except ValueError:
            continue
        if len(vals) >= limite:
            break
    if not vals:
        raise SystemExit(f"{chemin} : aucun identifiant lisible (attendu : CSV ou un par ligne)")
    return np.array(vals, dtype=np.int64)


def charger_etats(prefixe: str) -> tuple[np.ndarray, np.ndarray]:
    fichiers = sorted(pathlib.Path(prefixe).parent.glob(pathlib.Path(prefixe).name + ".*"),
                      key=lambda f: int(f.name.rsplit(".", 1)[1]))
    positions, lignes = [], []
    for f in fichiers:
        octets = f.read_bytes()
        if len(octets) % 4:
            continue
        positions.append(int(f.name.rsplit(".", 1)[1]))
        lignes.append(np.frombuffer(octets, dtype="<f4"))
    if not lignes:
        raise SystemExit("aucun état lisible")
    return np.array(positions), np.vstack(lignes)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--etats", required=True, help="préfixe des fichiers d'état (etat.4, etat.5, …)")
    ap.add_argument("--ids", required=True)
    ap.add_argument("--limite", type=int, default=1024)
    ap.add_argument("--classes", type=int, default=256, help="K plus fréquents du corpus")
    ap.add_argument("--lambda_", type=float, default=1.0)
    a = ap.parse_args()

    ids = charger_ids(a.ids, a.limite)
    pos, X = charger_etats(a.etats)
    if len(pos) == 0:
        raise SystemExit(f"{a.etats} : aucun état lisible (attendu : {a.etats}.<position>)")
    # la cible de la position p est le jeton p+1 (bornée au corpus)
    garde = pos + 1 < len(ids)
    pos, X = pos[garde], X[garde]
    y = ids[pos + 1]
    print(f"états : {X.shape[0]} positions × {X.shape[1]} canaux · corpus : {len(ids)} jetons")

    # les K classes les plus fréquentes DU CORPUS (pas du jeu d'entraînement : pas de fuite)
    freq = np.bincount(ids, minlength=int(ids.max()) + 1)
    classes = np.argsort(-freq)[: a.classes]
    ou = {int(c): i for i, c in enumerate(classes)}
    masque = np.array([int(t) in ou for t in y])
    print(f"cibles dans les {a.classes} classes les plus fréquentes : "
          f"{masque.sum()} / {len(y)} positions")

    X, y = X[masque], y[masque]
    Y = np.zeros((len(y), a.classes), dtype=np.float32)
    for i, t in enumerate(y):
        Y[i, ou[int(t)]] = 1.0

    # partage TRAIN / TEST par position (jamais aléatoire : le texte est ordonné)
    coupe = int(len(y) * 0.5)
    Xtr, Ytr, Xte, yte = X[:coupe], Y[:coupe], X[coupe:], y[coupe:]
    # normalisation (les états ont des échelles très différentes)
    moy, ect = Xtr.mean(0), Xtr.std(0) + 1e-6
    Xtr, Xte = (Xtr - moy) / ect, (Xte - moy) / ect

    G = Xtr.T @ Xtr + a.lambda_ * np.eye(Xtr.shape[1], dtype=np.float32)
    W = np.linalg.solve(G, Xtr.T @ Ytr)
    pred = (Xte @ W).argmax(1)
    justes = (pred == np.array([ou[int(t)] for t in yte])).mean()

    # références : la classe majoritaire du TRAIN, et la fréquence moyenne des cibles
    majoritaire = np.bincount([ou[int(t)] for t in y[:coupe]], minlength=a.classes).argmax()
    ref_majoritaire = (np.array([ou[int(t)] for t in yte]) == majoritaire).mean()
    p_max = freq[classes].max() / freq.sum()
    print()
    print(f"sonde linéaire (ridge λ={a.lambda_}) : {justes * 100:.1f} % de justes sur le TEST")
    print(f"référence « toujours la classe majoritaire » : {ref_majoritaire * 100:.1f} %")
    print(f"référence « hasard uniforme sur {a.classes} classes » : {100 / a.classes:.2f} %")
    print(f"référence « fréquence du jeton le plus fréquent du corpus » : {p_max * 100:.2f} %")
    print()
    if justes > max(ref_majoritaire, p_max) * 1.5:
        print("VERDICT : l'état de la couche 16 CONTIENT le prochain jeton, linéairement.")
        print("  ⇒ la tête empruntée (728 388 de perplexité) est bien le maillon faible :")
        print("    C8 a un sens, et la suite est d'entraîner une tête NON linéaire par profondeur.")
    else:
        print("VERDICT : la sonde linéaire ne dépasse pas les références de fréquence.")
        print("  ⇒ soit l'information n'est pas là à cette profondeur, soit elle n'est pas")
        print("    linéairement accessible ; une tête non linéaire reste à essayer avant de")
        print("    conclure que C8 est hors de portée.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
