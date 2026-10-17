#!/usr/bin/env python3
"""operateur_pensee.py — L'OPÉRATEUR DE PENSÉE APPRIS : itérer DANS l'état, sans repasser par le modèle.

POURQUOI CET OBJET, ET EN QUOI IL DIFFÈRE DE LA BOUCLE DIRECTE ✗. La nuit a mesuré trois échecs qui
convergent ✓ :
  · la boucle **directe** (réinjecter l'état comme entrée du modèle ✓) explose : λ = **7 311** ✗✗, et le
    contenu se détruit ✓ (140 % d'écart) ;
  · le pas `h_p → h_{p+1}` est **expansif** (λ de 30 à 120 ✗) et n'est pas un pas de pensée ✓ ;
  · le cycle, entraîné, **réduit** λ mais ne le soumet pas ✗ (206 → 136 ✓).
Les trois disent la même chose : **le modèle ne contient aucun opérateur de pensée** ✗ — et repasser par
lui à chaque pas est ce qui casse tout ✓✗.

DONC UN AUTRE OBJET ✓✓ : un **opérateur latent** `C` qui itère **sur l'état seul** ✓ — sans passage dans
le modèle ✗ (c'est le « mode de fonctionnement complètement différent » de Stéphane ✓). Deux exigences,
et elles ne se satisfont pas l'une sans l'autre :
  1. **CONTRACTER** ✓ : λ(C) ≤ 1 (une itération qui diverge ne pense pas, elle explose ✗) ;
  2. **PROGRESSER** ✓ : après k pas, l'état doit dire le jeton à venir **mieux** qu'avant ✓ — sinon la
     solution triviale (`C = identité` ✓, λ = 1 ✓, contenu exactement préservé ✓) gagnerait ✗✗, et elle ne
     pense **rien** ✓. C'est cette deuxième exigence qui empêche l'opérateur d'être un faux-semblant ✓.

CE QU'IL FAIT : il charge le jouet **aligné** ✓ (cosinus 0,70 · échelle 1,015 ✓), récolte des couples
`(état normalisé, embedding du jeton suivant)` ✓, entraîne `C = I + f` ✓ (f un petit MLP) avec les deux
termes ✓, et mesure **λ**, le **contenu** avant/après ✓, et le **balayage** de k ✓.

Usage :
  CUDA_VISIBLE_DEVICES=0 python tools/operateur_pensee.py --hf /tmp/jouet-aligne --ids /tmp/ids-octets.txt \\
      [--pas 3000] [--cachee 256]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

import numpy as np
import torch
import torch.nn as nn


class Cellule(nn.Module):
    """`C = I + f` : l'identité en réserve ✓ — un opérateur nul est *contractant* (λ = 1) et ne détruit
    rien ✓, donc f doit **gagner** sa place en améliorant le contenu ✓ (sinon il apprend f = 0 ✓, et
    c'est un résultat honnête : la pensée n'existe pas ✗)."""

    def __init__(self, dim: int, cachee: int):
        super().__init__()
        self.f = nn.Sequential(nn.Linear(dim, cachee), nn.GELU(), nn.Linear(cachee, dim))

    def forward(self, x):
        return x + self.f(x) * 0.1                                   # pas borné : 0,1 max par pas ✓


def ecart(P, E):
    return 100 * float(np.linalg.norm(P - E) / np.linalg.norm(E))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--ids", required=True)
    ap.add_argument("--longueur", type=int, default=64)
    ap.add_argument("--positions", type=int, default=5000)
    ap.add_argument("--cachee", type=int, default=256)
    ap.add_argument("--pas", type=int, default=3000)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--poids-contraction", type=float, default=10.0)
    ap.add_argument("--sortie", default="/tmp/operateur-pensee.pt")
    a = ap.parse_args()

    from transformers import AutoModelForCausalLM
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float32).eval()
    for p in m.parameters():
        p.requires_grad_(False)
    ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(a.ids).read_text()) if x.strip()]
    L, dim = a.longueur, m.config.hidden_size

    # ---- récolte : l'état NORMALISÉ (celui que l'alignement a calibré ✓) et la cible (embedding suivant ✓)
    S, T = [], []
    with torch.no_grad():
        i = 0
        while len(S) < a.positions and 1000 + i * 400 + L + 1 < len(ids):
            d = 1000 + i * 400
            b = torch.tensor([ids[d:d + L]])
            hs = m(b, output_hidden_states=True).hidden_states[-1][0]        # (L, dim) avant norme ✓
            sn = m.model.norm(hs)                                           # état normalisé ✓
            e = m.get_input_embeddings()(torch.tensor([ids[d + 1:d + L + 1]]))[0]
            S.append(sn.numpy()); T.append(e.numpy())
            i += 1
    S = torch.tensor(np.concatenate(S)[:a.positions], dtype=torch.float32)
    T = torch.tensor(np.concatenate(T)[:a.positions], dtype=torch.float32)
    n = int(S.shape[0] * 0.8)
    S_tr, T_tr, S_te, T_te = S[:n], T[:n], S[n:], T[n:]
    print(f"états récoltés : {S.shape[0]} · dimension {dim} · entraînement {S_tr.shape[0]} · test {S_te.shape[0]}")

    def qualite(cellule, X, Y):
        """Le contenu : écart relatif du mapping état → embedding, APRÈS le nombre de pas demandé ✓."""
        with torch.no_grad():
            Z = cellule(X)
            return ecart(Z.numpy(), Y.numpy())

    # ---- l'étalon : sans opérateur (identité ✓)
    ident = Cellule(dim, a.cachee)
    with torch.no_grad():
        for p in ident.parameters(): p.zero_()
    avant = qualite(ident, S_te, T_te)
    print(f"\n  contenu SANS opérateur (identité) : {avant:.1f} % d'écart")

    # ---- l'entraînement : contrat + progrès ✓✓
    cel = Cellule(dim, a.cachee)
    opt = torch.optim.AdamW(cel.parameters(), lr=a.lr)
    for pas in range(1, a.pas + 1):
        idx = torch.randperm(S_tr.shape[0])[:512]
        x, y = S_tr[idx], T_tr[idx]
        z = cel(x)
        # 1. le contenu après UN pas doit être plus proche de la cible qu'avant ✓ (progrès, pas simple
        #    conservation ✗ : on demande à l'opérateur de FAIRE MIEUX, pas de ne rien faire ✓✓)
        perte_contenu = ((z - y) ** 2).mean()
        # 2. la contraction : sur une perturbation infime, le pas ne doit pas amplifier ✓
        delta = torch.randn_like(x) * 1e-3
        lam = ((cel(x + delta) - z).norm(dim=-1) / delta.norm(dim=-1).clamp_min(1e-9)).mean()
        perte_contraction = torch.clamp(lam - 1.0, min=0.0) ** 2
        perte = perte_contenu + a.poids_contraction * perte_contraction
        opt.zero_grad(); perte.backward(); opt.step()
        if pas % 500 == 0 or pas == a.pas:
            with torch.no_grad():
                q = ecart(cel(S_te).numpy(), T_te.numpy())
            print(f"  pas {pas:>5} · contenu {q:6.1f} % · λ {float(lam):.3f} · perte {float(perte):.4f}")

    # ---- les mesures finales : λ, contenu, et l'ITÉRATION ✓
    with torch.no_grad():
        delta = torch.randn_like(S_te) * 1e-3
        lam_final = float(((cel(S_te + delta) - cel(S_te)).norm(dim=-1) / delta.norm(dim=-1)).mean())
    print(f"\n  λ de l'opérateur : {lam_final:.4f}" + ("  → contracte ✓" if lam_final <= 1.05 else "  → amplifie ✗"))
    print()
    print("  le contenu au fil des itérations (plus bas est mieux ; identité = %.1f %%) :" % avant)
    with torch.no_grad():
        Z = S_te.clone()
        for k in range(1, 9):
            Z = cel(Z)
            if k in (1, 2, 4, 8):
                print(f"    {k} pas : {ecart(Z.numpy(), T_te.numpy()):6.1f} %")
    torch.save({"etat": cel.state_dict(), "dim": dim, "cachee": a.cachee,
                "avant": avant, "lambda": lam_final}, a.sortie)
    print(f"\n  opérateur écrit dans {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
