#!/usr/bin/env python3
"""contenu_par_couche.py — LE NOYAU NEUTRE EST-IL UTILE ? (le sens survit-il à l'effacement de la langue ?)

LA QUESTION, ET POURQUOI ELLE DÉCIDE DE TOUT (chapitre 7). La première mesure a montré qu'aux couches **1 et
2** d'un modèle bilingue, un classifieur linéaire ne sait plus dire la langue (50,2 % = le hasard ✓✓). C'est
la « couche commune » cherchée ✓. Mais une couche qui ne dit plus la langue pourrait tout simplement **ne plus
rien dire** ✗✓ — et alors la neutralité serait une **perte**, pas une abstraction ✗✗.

CE QUE CET OUTIL MESURE. Pour **chaque couche**, et pour **chaque langue** séparément, l'écart du mapping
`état normalisé → embedding du jeton suivant` ✓ (le « contenu », méthode du chapitre 5 ✓, avec un **λ de ridge
choisi par validation croisée** ✗✓ — leçon du 16/10). Trois nombres par couche, et le quatrième qui compte :
le contenu **au niveau neutre** (couches 1-2 ✓) comparé au contenu **au niveau où la langue reparaît**
(couches 6-7 ✓).

Si le contenu est **aussi lisible** aux couches neutres ✓✓ → le noyau abstrait la langue **sans perdre le
sens** ✓✓ — c'est la réponse qu'on cherche. S'il s'effondre aux couches neutres ✗ → la neutralité se paie en
sens ✗✓, et il faut le dire.

Usage :
  CUDA_VISIBLE_DEVICES=0 python tools/contenu_par_couche.py --hf /tmp/jouet-mixte \\
      --en data/corpus_en.txt --fr data/corpus_fr.txt [--longueur 128] [--fenetres 250]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

import numpy as np
import torch

LAMBDAS = (1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0)


def lambda_cv(H, E, plis=3):
    """λ de ridge par validation croisée ✓ (leçon du 16/10 : un λ fixé rend les chiffres dépendants des
    réglages ✗✓)."""
    idx = np.array_split(np.arange(H.shape[0]), plis)
    meilleur, err_min = 1e-3, 1e30
    for lam in LAMBDAS:
        err = 0.0
        for i in range(plis):
            te = idx[i]
            tr = np.concatenate([idx[j] for j in range(plis) if j != i])
            mh, me = H[tr].mean(0), E[tr].mean(0)
            Hc, Ec = H[tr] - mh, E[tr] - me
            W = np.linalg.solve(Hc.T @ Hc + lam * np.eye(Hc.shape[1]), Hc.T @ Ec)
            err += float(np.linalg.norm((H[te] - mh) @ W + me - E[te]) ** 2)
        if err < err_min:
            meilleur, err_min = lam, err
    return meilleur


def contenu(H, E):
    """L'écart relatif du mapping, λ par validation croisée, mesuré sur une moitié tenue à l'écart ✓."""
    n = H.shape[0]
    n2 = n // 2
    lam = lambda_cv(H[:n2], E[:n2])
    mh, me = H[:n2].mean(0), E[:n2].mean(0)
    Hc, Ec = H[:n2] - mh, E[:n2] - me
    W = np.linalg.solve(Hc.T @ Hc + lam * np.eye(Hc.shape[1]), Hc.T @ Ec)
    P = (H[n2:] - mh) @ W + me
    return 100 * float(np.linalg.norm(P - E[n2:]) / np.linalg.norm(E[n2:]))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True, help="le modèle bilingue (octets)")
    ap.add_argument("--en", default="data/corpus_en.txt")
    ap.add_argument("--fr", default="data/corpus_fr.txt")
    ap.add_argument("--longueur", type=int, default=128)
    ap.add_argument("--fenetres", type=int, default=250)
    a = ap.parse_args()

    from transformers import AutoModelForCausalLM
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).eval()
    n_couches = m.config.num_hidden_layers

    def recolter(chemin):
        b = np.frombuffer(pathlib.Path(chemin).read_text(errors="ignore").encode("utf-8"),
                          dtype=np.uint8).astype(np.int64)
        pas = max(a.longueur, len(b) // (a.fenetres + 2))
        S = {L: [] for L in range(n_couches + 1)}
        T = []
        with torch.no_grad():
            for i in range(a.fenetres):
                d = i * pas
                if d + a.longueur + 1 >= len(b):
                    break
                x = torch.tensor(b[d:d + a.longueur]).unsqueeze(0)
                hs = m(x, output_hidden_states=True).hidden_states
                cible = m.get_input_embeddings()(torch.tensor(b[d + 1:d + a.longueur + 1])).unsqueeze(0)
                T.append(cible[0].numpy().astype(np.float64))
                for L in S:
                    S[L].append(m.model.norm(hs[L][0]).numpy().astype(np.float64))
        return {L: np.concatenate(v) for L, v in S.items()}, np.concatenate(T)

    S_en, T_en = recolter(a.en)
    S_fr, T_fr = recolter(a.fr)
    print(f"  {n_couches} couches · {S_en[0].shape[0]} positions d'anglais · {S_fr[0].shape[0]} de français")
    print()
    print("   couche | contenu ANGLAIS | contenu FRANÇAIS | contenu MÊLÉ | la langue ? (ch.7)")
    print("   -------|-----------------|------------------|--------------|-------------------")
    # la référence de langue, mesurée au chapitre 7 : le hasard aux couches 1-2, ~59 % aux couches 6-7
    for L in range(n_couches + 1):
        c_en = contenu(S_en[L], T_en)
        c_fr = contenu(S_fr[L], T_fr)
        n = min(S_en[L].shape[0], S_fr[L].shape[0])
        S_mix = np.concatenate([S_en[L][:n], S_fr[L][:n]])
        T_mix = np.concatenate([T_en[:n], T_fr[:n]])
        c_mix = contenu(S_mix, T_mix)
        note = "NEUTRE (50 %)" if L in (1, 2) else ("la langue revient" if L in (6, 7) else "")
        print(f"   {L:>6} |      {c_en:5.1f} %    |      {c_fr:5.1f} %     |    {c_mix:5.1f} %   | {note}")
    print()
    print("  lecture : ce qui compte est la comparaison entre les couches NEUTRES (1-2) et celles où la langue")
    print("  revient (6-7). Si le contenu y est comparable, le noyau abstrait la langue SANS perdre le sens ✓✓.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
