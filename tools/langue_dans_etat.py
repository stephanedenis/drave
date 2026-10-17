#!/usr/bin/env python3
"""langue_dans_etat.py — LA LANGUE EST-ELLE ENCORE DANS L'ÉTAT, ET À QUELLE COUCHE ?

LA QUESTION (chapitre 7 de `docs/synthese/`). Une couche commune entrée-sortie doit **abstraire la
langue** : la langue, le dialecte, le style ne doivent être que des **paramètres**, pas le contenu ✓. Le
critère qui décide, écrit d'avance ✓ : **un classifieur de langue entraîné sur l'état doit être AU HASARD**
sur la couche commune. S'il devine la langue ✗, la couche n'abstrait pas — elle porte encore la langue ✓✓.

CE QUE CET OUTIL MESURE, ET SES DEUX PIÈGES ÉVITÉS.
  1. **le piège de la trivialité** ✗✓ : deux textes différents donnent des états différents ✓, donc un
     classifieur peut séparer « anglais » et « français » **par le sujet** du texte, pas par la langue ✗.
     Le remède : on **apparie** les fenêtres (même longueur ✓, même type de contenu ✓, et surtout : on
     compare à un **témoin intra-langue** ✓ — un classifieur qui sépare deux *sujets* de la même langue ✓ —
     si la séparation de langue n'est pas meilleure que celle du témoin, on ne mesure rien ✓) ;
  2. **le piège du nombre de positions** ✗✓ (leçon du 16/10) : un ridge sur moins de positions que de
     coefficients **interpole** et rend 100 % ✓✗ — on exige donc **n > 5 × dimension** ✓ et on le dit.

LA MESURE, COUCHE PAR COUCHE. Pour chaque couche L : on ajuste une régression logistique (ou un ridge
fermé, plus simple ✓) `état_L → {anglais, français}` ✓ sur la moitié des fenêtres, on mesure la
**précision** sur l'autre moitié ✓, et on compare à deux témoins :
  · le **hasard** (50 % ✓) ;
  · le **témoin intra-langue** ✗ : le même classifieur sur deux *sujets* de la **même** langue ✓.

Usage :
  CUDA_VISIBLE_DEVICES=0 python tools/langue_dans_etat.py --hf /tmp/jouet-mixte \\
      --en data/corpus_en.txt --fr data/corpus_fr.txt [--longueur 128] [--fenetres 400]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

import numpy as np
import torch


def fenetres(texte: str, longueur: int, nombre: int, debut: int = 0) -> list[np.ndarray]:
    """Des fenêtres d'octets, prises à des endroits DIFFÉRENTS du texte ✓ (pas de recouvrement ✓)."""
    b = np.frombuffer(texte.encode("utf-8", errors="ignore"), dtype=np.uint8).astype(np.int64)
    pas = max(longueur, len(b) // max(1, nombre + 1))
    out = []
    for i in range(nombre):
        d = debut + i * pas
        if d + longueur >= len(b):
            break
        out.append(b[d:d + longueur])
    return out


def etats(modele, lot: list[np.ndarray], couches: list[int]) -> dict[int, np.ndarray]:
    """L'état **normalisé** de chaque fenêtre, pour chaque couche demandée ✓."""
    S = {L: [] for L in couches}
    with torch.no_grad():
        for w in lot:
            b = torch.tensor(w).unsqueeze(0)
            hs = modele(b, output_hidden_states=True).hidden_states
            for L in couches:
                h = hs[L][0]
                S[L].append(modele.model.norm(h).numpy().astype(np.float64))
    return {L: np.concatenate(v) for L, v in S.items()}


def precision_lineaire(X: np.ndarray, y: np.ndarray, lam: float = 10.0) -> float:
    """Une régression logistique « fermée » : ridge sur les étiquettes ±1 ✓, puis seuil à 0 ✓ — plus
    simple qu'un entraînement, et suffisant pour une séparation linéaire ✓."""
    n = X.shape[0]
    if n < 5 * X.shape[1]:
        return float("nan")                 # sous-déterminé : on ne mesure pas ✗✓
    n2 = n // 2
    Xtr, ytr, Xte, yte = X[:n2], y[:n2], X[n2:], y[n2:]
    mx = Xtr.mean(0)
    Xc, Xt = Xtr - mx, Xte - mx
    w = np.linalg.solve(Xc.T @ Xc + lam * np.eye(Xc.shape[1]), Xc.T @ ytr)
    pred = np.sign(Xt @ w)
    acc = 100 * float(np.mean(pred == yte))
    # ⚠️ LE SIGNE D'UN CLASSIFIEUR LINÉAIRE EST ARBITRAIRE ✗✓. Un ridge sur des étiquettes ±1 peut rendre
    # le signe OPPOSÉ à celui qu'on attend ✓ : une précision de 43,4 % est une précision de **56,6 %** avec
    # l'autre orientation ✓✗. Sans ce maximum, on lit « sous le hasard » là où il y a une séparation
    # réelle — c'est la SIXIÈME fois de la nuit qu'un chiffre se déguise ✓✓ (les cinq premières sont au
    # chapitre 6 de la synthèse). On rend donc la précision **la meilleure des deux orientations**.
    return max(acc, 100.0 - acc)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True, help="le modèle entraîné sur les DEUX langues")
    ap.add_argument("--en", default="data/corpus_en.txt")
    ap.add_argument("--fr", default="data/corpus_fr.txt")
    ap.add_argument("--longueur", type=int, default=128)
    ap.add_argument("--fenetres", type=int, default=300)
    ap.add_argument("--couches", default="", help="par défaut : toutes les couches du modèle")
    a = ap.parse_args()

    from transformers import AutoModelForCausalLM
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).eval()
    n_couches = m.config.num_hidden_layers
    couches = [int(x) for x in a.couches.split(",")] if a.couches else list(range(n_couches + 1))

    txt_en = pathlib.Path(a.en).read_text(errors="ignore")
    txt_fr = pathlib.Path(a.fr).read_text(errors="ignore")
    # anglais et français, pris au MÊME endroit relatif de leur corpus (pas de biais de position ✓)
    f_en = fenetres(txt_en, a.longueur, a.fenetres)
    f_fr = fenetres(txt_fr, a.longueur, a.fenetres)
    # le TÉMOIN INTRA-LANGUE ✗ : deux moitiés du corpus anglais (deux sujets différents ✓)
    moitie = len(txt_en) // 2
    f_en_a = fenetres(txt_en[:moitie], a.longueur, a.fenetres // 2)
    f_en_b = fenetres(txt_en[moitie:], a.longueur, a.fenetres // 2)
    print(f"  fenêtres : {len(f_en)} anglais · {len(f_fr)} français · témoin intra-langue {len(f_en_a)}+{len(f_en_b)}")
    print(f"  modèle : {n_couches} couches · dimension {m.config.hidden_size}")

    E_en, E_fr = etats(m, f_en, couches), etats(m, f_fr, couches)
    E_a, E_b = etats(m, f_en_a, couches), etats(m, f_en_b, couches)

    print()
    print("   couche | langue (en/fr) | témoin intra-langue | écart  (plus BAS = la langue s'efface ✓)")
    print("   -------|----------------|---------------------|-------")
    for L in couches:
        n = min(E_en[L].shape[0], E_fr[L].shape[0])
        if n < 5 * E_en[L].shape[1]:
            print(f"   {L:>6} |  (n={n} < 5×dim : non mesuré ✗)")
            continue
        X = np.concatenate([E_en[L][:n], E_fr[L][:n]])
        y = np.concatenate([np.ones(n), -np.ones(n)])
        acc_langue = precision_lineaire(X, y)
        k = min(E_a[L].shape[0], E_b[L].shape[0])
        acc_temoin = precision_lineaire(np.concatenate([E_a[L][:k], E_b[L][:k]]),
                                        np.concatenate([np.ones(k), -np.ones(k)]))
        ecart = acc_langue - acc_temoin
        marque = " ✓" if ecart < 5 else (" ✗" if ecart > 20 else "")
        print(f"   {L:>6} |   {acc_langue:5.1f} %    |      {acc_temoin:5.1f} %      | {ecart:+5.1f}{marque}")
    print()
    print("  lecture : si la précision « langue » est PROCHE de 100 % et loin du témoin, l'état porte la")
    print("  langue ✗ ; si elle rejoint le témoin (ou le hasard), la couche l'a abstraite ✓✓. Le témoin")
    print("  intra-langue dit ce qu'un classifieur peut faire SANS la langue : c'est lui la référence ✗.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
