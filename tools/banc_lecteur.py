#!/usr/bin/env python3
"""banc_lecteur.py — LE BANC QUI TRANSFORME UN CHIFFRE EN MESURE.

LE PROBLÈME (5ᵉ leçon de la nuit ✓✗) : le « contenu » du modèle 512 valait **104,3 %** à longueur 64 et
**87,0 %** à longueur 128 ✗✓ — un chiffre qui dépend des réglages n'est pas une mesure, c'est un réglage ✓.
Ce banc fait donc les deux choses qui manquaient :
  1. **un λ de ridge choisi par validation croisée** ✓ (et non fixé à 1e-3 ✓) — un lecteur **régularisé** ;
  2. **une batterie de réglages** ✓ (longueurs 32 · 64 · 128 · 256 ✓) — et on regarde si le **classement**
     des modèles est **stable** ✗ ou s'il **bascule** ✗✓.

Ce que le résultat dira ✓ : si le classement est **stable** sur toute la batterie, la comparaison est une
**mesure** ✓✓ et les conclusions de la nuit tiennent ✓ ; s'il **bascule** avec les réglages ✗, alors la
comparaison n'était **pas mesurable** ✗✓ — et c'est **aussi** un résultat ✓ (il dit de ne pas conclure ✗).

Usage :
  CUDA_VISIBLE_DEVICES=0 python tools/banc_lecteur.py --modeles /tmp/jouet-d256,/tmp/jouet-d512 \\
      --ids /tmp/ids-octets.txt [--longueurs 32,64,128,256]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

import numpy as np
import torch

LAMBDAS = (1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0)


def ridge_cv(H, E, k=3):
    """Le λ de ridge choisi par **validation croisée** sur les données d'entraînement ✓ — pas fixé à la main ✗."""
    n = H.shape[0]
    d = H.shape[1]
    plis = np.array_split(np.arange(n), k)
    meilleur, meilleur_err = LAMBDAS[2], 1e30
    for lam in LAMBDAS:
        err = 0.0
        for i in range(k):
            te = plis[i]
            tr = np.concatenate([plis[j] for j in range(k) if j != i])
            mh, me = H[tr].mean(0), E[tr].mean(0)
            Hc, Ec = H[tr] - mh, E[tr] - me
            W = np.linalg.solve(Hc.T @ Hc + lam * np.eye(d), Hc.T @ Ec)
            err += float(np.linalg.norm((H[te] - mh) @ W + me - E[te]) ** 2)
        if err < meilleur_err:
            meilleur, meilleur_err = lam, err
    return meilleur


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modeles", required=True)
    ap.add_argument("--ids", required=True)
    ap.add_argument("--longueurs", default="32,64,128,256")
    ap.add_argument("--amorces", type=int, default=60)
    ap.add_argument("--repetitions", default="",
                    help="rejouer la comparaison de la FALAISE (§ 18) : on répète le bloc t fois, pour "
                         "t dans cette liste (ex. « 1,4 ») — le modèle doit être un bloc partagé ✓")
    a = ap.parse_args()

    from transformers import AutoModelForCausalLM
    ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(a.ids).read_text()) if x.strip()]
    longueurs = [int(x) for x in a.longueurs.split(",")]
    chemins = a.modeles.split(",")

    # les états sont récoltés À LA PLUS GRANDE LONGUEUR puis tronqués par position ✓ (c'est la même
    # distribution de positions, et une seule passe par modèle ✓)
    L = max(longueurs)
    import copy
    import torch.nn as tnn
    repetitions = [int(x) for x in a.repetitions.split(",") if x.strip()] or [1]
    donnees = {}
    for chemin in chemins:
        m = AutoModelForCausalLM.from_pretrained(chemin, dtype=torch.float32).eval()
        base = [copy.deepcopy(c) for c in m.model.layers]
        for tt in repetitions:
            # ⚠️ LES DEUX BORNES DE LA BIBLIOTHÈQUE (leçon du § 16) : la boucle du forward est bornée par
            # `config.num_hidden_layers` ✓ et `layer_types` est une liste PAR COUCHE ✓ — sans les deux, les
            # couches ajoutées sont SILENCIEUSEMENT ignorées ✓✗.
            m.model.layers = tnn.ModuleList([copy.deepcopy(c) for _ in range(tt) for c in base])
            m.config.num_hidden_layers = len(m.model.layers)
            m.config.layer_types = (list(m.config.layer_types[:len(base)]) * tt)[:len(m.model.layers)]
            globals().setdefault("_etats", {})
            S, T = [], []
            with torch.no_grad():
                for i in range(a.amorces):
                    d = 1000 + i * 1200
                    b = torch.tensor([ids[d:d + L]])
                    hs = m(b, output_hidden_states=True).hidden_states[-1][0]
                    S.append(m.model.norm(hs).numpy().astype(np.float64))
                    T.append(m.get_input_embeddings()(torch.tensor([ids[d + 1:d + L + 1]]))[0]
                             .numpy().astype(np.float64))
            donnees[f"{pathlib.Path(chemin).name[:-4] if pathlib.Path(chemin).name.endswith('.bin') else pathlib.Path(chemin).name}·t{tt}"] = (
                np.concatenate(S), np.concatenate(T))
        del m
    chemins_ok = True
    if False:
        pass
    print()
    print("   le contenu (écart %) par LONGUEUR, avec un λ de ridge choisi par validation croisée :")
    entete = "   modèle " + "".join(f"| L={L:>3} " for L in longueurs) + "| λ retenus"
    print(entete); print("   " + "-" * (len(entete) - 2))
    classements = []
    for nom, (S, T) in donnees.items():
        cellules, lams, note = [], [], None
        for Lc in longueurs:
            # on garde les positions dont l'indice est < Lc dans chaque fenêtre ✓
            idx = np.concatenate([np.arange(i * L, i * L + Lc) for i in range(a.amorces)])
            Sx, Tx = S[idx], T[idx]
            n = int(Sx.shape[0] * 0.6)
            mh, me = Sx[:n].mean(0), Tx[:n].mean(0)
            Hc, Ec = Sx[:n] - mh, Tx[:n] - me
            lam = ridge_cv(Sx[:n], Tx[:n])
            W = np.linalg.solve(Hc.T @ Hc + lam * np.eye(Hc.shape[1]), Hc.T @ Ec)
            err = 100 * float(np.linalg.norm((Sx[n:] - mh) @ W + me - Tx[n:]) / np.linalg.norm(Tx[n:]))
            cellules.append(f"{err:6.1f}")
            lams.append(f"{lam:g}")
        classements.append([float(c) for c in cellules])
        print(f"   {nom:7s} " + "".join(f"| {c} " for c in cellules) + "| " + " ".join(lams))

    # le classement est-il STABLE sur toute la batterie ?
    if len(classements) >= 2:
        gagnants = [int(np.argmin([c[i] for c in classements])) for i in range(len(longueurs))]
        stable = len(set(gagnants)) == 1
        print()
        if stable:
            print(f"  ✅ LE CLASSEMENT EST STABLE sur les {len(longueurs)} longueurs (gagnant : "
                  f"{list(donnees)[gagnants[0]]} ✓✓) : la comparaison est une MESURE ✓.")
        else:
            print(f"  ✗ LE CLASSEMENT BASCULE selon la longueur (gagnants : {gagnants} pour "
                  f"{list(donnees)} ✗✓) : la comparaison n'était PAS mesurable — et c'est un résultat.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
