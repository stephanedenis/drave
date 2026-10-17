#!/usr/bin/env python3
"""boucle_directe.py — ÉTAPE 4 : la BOUCLE SANS PONT, maintenant que les espaces coïncident.

L'ÉTAT DE LA QUESTION (16/10). Trois mesures ont rendu la boucle directe pensable ✓ :
  1. sans alignement, réinjecter l'état brut EXPLOSE (×30 000 ✗) et normer n'y change rien ✗✓, parce
     que les deux espaces diffèrent **d'un facteur 648** ET par la direction (cosinus **+0,14** ✗) ;
  2. un **alignement entraîné** (`--alignement` ✓) amène le jouet 2 M à **cosinus +0,70** et **échelle
     1,015** ✓✓, **sans** dégrader la langue (val **4,30** contre 4,69 bits/octet ✓✓ — mieux !) ;
  3. et le **balayage par horizon** montre que le contenu long **survit** ✓✓ (k = 16 : 88,3 % contre
     89,0 pour le témoin ✓) — le risque d'un **effondrement au mot** ✗ n'est pas advenu ✓✓.

CE QUE CET OUTIL FAIT, ET COMMENT IL INJECTE SANS PONT ✓. On remplace l'embedding du jeton à une position
par **`norm(h)` de l'état précédent** ✓ — c'est-à-dire qu'on **récupère l'état comme entrée**, sans aucune
projection apprise ✗ (c'est la différence avec `pensee_silencieuse.py --pont` ✓). On itère k fois, et on
mesure deux choses :
  · **λ**, l'amplification d'une perturbation infime sous le pas ✓ (le même λ que partout ailleurs ✓) ;
  · **le contenu** : ce que l'état itéré dit du jeton à venir ✓ (le mapping ridge du § 5 ✓), comparé à
    l'état **non itéré** ✓ — si le contenu tient, la pensée silencieuse est **itérative** ✓✓ ; s'il
    s'effondre, la boucle ne fait que dériver ✗.
Et le **témoin** : la même chose sur le modèle **sans alignement** ✗ — c'est lui qui explose ✓.

Usage :
  CUDA_VISIBLE_DEVICES=0 python tools/boucle_directe.py --hf /tmp/jouet-aligne --ids /tmp/ids-octets.txt \\
      [--pas 1,2,4,8] [--amorces 40]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

import numpy as np
import torch


def ecart(P: np.ndarray, E: np.ndarray) -> float:
    return 100 * float(np.linalg.norm(P - E) / np.linalg.norm(E))


def ridge(H: np.ndarray, E: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """Le mapping `état → embedding` (ridge ✓) et son écart **hors échantillon** (moitié test ✓)."""
    n = H.shape[0]
    mh, me = H.mean(0), E.mean(0)
    Hc, Ec = H - mh, E - me
    W = np.linalg.solve(Hc.T @ Hc + 1e-3 * np.eye(Hc.shape[1]), Hc.T @ Ec)
    P = Hc @ W + me
    rel = ecart(P, E)
    return W, mh, me, rel


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True, help="le modèle ALIGNÉ (dossier HuggingFace)")
    ap.add_argument("--temoin", default="", help="le même modèle SANS alignement (témoin ✗)")
    ap.add_argument("--ids", required=True, help="corpus d'octets (identifiants 0-255)")
    ap.add_argument("--longueur", type=int, default=64)
    ap.add_argument("--pas", default="1,2,4,8")
    ap.add_argument("--amorces", type=int, default=40)
    ap.add_argument("--sortie", default="/tmp/boucle-directe.npz")
    a = ap.parse_args()

    from transformers import AutoModelForCausalLM
    ids = [int(x) for x in re.split(r"[,\s]+", pathlib.Path(a.ids).read_text()) if x.strip()]
    L = a.longueur
    pas_liste = [int(x) for x in a.pas.split(",")]

    def charger(chemin):
        m = AutoModelForCausalLM.from_pretrained(chemin, dtype=torch.float32).eval()
        return m

    def boucler(m, amorce, k: int):
        """Injection SANS PONT : à la position du dernier jeton, l'entrée devient `norm(h)` ✓."""
        b = torch.tensor([amorce])
        with torch.no_grad():
            hs = m(b, output_hidden_states=True).hidden_states[-1][0, -1]      # l'état, avant norme ✓
            etat = m.model.norm(hs.unsqueeze(0))[0]                           # calibré par l'alignement ✓
            for _ in range(k):
                # on remplace l'embedding du DERNIER jeton par l'état ✓ — aucun pont, aucune projection ✗
                emb = m.get_input_embeddings()(b).clone()
                emb[0, -1] = etat
                hs = m(inputs_embeds=emb, output_hidden_states=True).hidden_states[-1][0, -1]
                etat = m.model.norm(hs.unsqueeze(0))[0]
        return etat

    def contenu(m, k: int):
        """Ce que l'état itéré k fois dit du jeton à venir : écart relatif du mapping appris ✓."""
        H, E = [], []
        with torch.no_grad():
            for i in range(a.amorces):
                d = 1000 + i * 1200
                amorce = ids[d:d + L]
                if len(amorce) < L: continue
                etat = boucler(m, amorce, k)
                H.append(etat.numpy().astype(np.float64))
                # la cible : l'embedding du jeton **suivant** (celui qu'on aurait dû lire ✓)
                E.append(m.get_input_embeddings()(torch.tensor([[ids[d + L]]]))[0, 0].numpy().astype(np.float64))
        H, E = np.stack(H), np.stack(E)
        if H.shape[0] < 10:
            return None
        # mapping appris sur la moitié, mesuré sur l'autre ✓ (sinon on mesurerait l'apprentissage du ridge ✗)
        n = H.shape[0] // 2
        W, mh, me, _ = ridge(H[:n], E[:n])
        return ecart((H[n:] - mh) @ W + me, E[n:])

    resultats = {}
    for nom, chemin in [("ALIGNÉ", a.hf)] + ([("témoin", a.temoin)] if a.temoin else []):
        m = charger(chemin)
        print(f"\n=== {nom} : {chemin} ===")
        # λ : croissance d'une perturbation infime sous le pas ✓
        with torch.no_grad():
            hs = m(torch.tensor([ids[1000:1000 + L]]), output_hidden_states=True).hidden_states[-1][0, -1]
            base = m.model.norm(hs.unsqueeze(0))[0]
            eps = 1e-4
            dir_ = torch.randn_like(base); dir_ = dir_ / dir_.norm() * (eps * base.norm())
            emb = m.get_input_embeddings()(torch.tensor([ids[1000:1000 + L]])).clone()
            emb[0, -1] = base + dir_
            hsp = m(inputs_embeds=emb, output_hidden_states=True).hidden_states[-1][0, -1]
            ecart_pert = (m.model.norm(hsp.unsqueeze(0))[0] - base).norm()
        lam = float(ecart_pert / (eps * float(base.norm())))
        print(f"  λ (perturbation infime, un pas direct) = {lam:.4f}"
              + ("  → AMPLIFIE ✗" if lam > 1 else "  → contracte ✓"))
        ligne = {}
        for k in pas_liste:
            c = contenu(m, k)
            ligne[k] = c
            print(f"  {k} pas direct(s) : contenu de l'état = {c:.1f} % d'écart" if c else f"  {k} pas : (trop peu)")
        resultats[nom] = (lam, ligne)
        del m

    print()
    print("  lecture : le contenu est ce que l'état dit du jeton à venir ✓ (plus bas est mieux) ;")
    print("  le témoin SANS alignement est là pour montrer ce que la boucle directe fait sans lui ✗.")
    np.savez(a.sortie, **{f"{nom}_lam": np.array(lam) for nom, (lam, _) in resultats.items()},
             **{f"{nom}_contenu_{k}": np.array(c) for nom, (_, l) in resultats.items() for k, c in l.items() if c})
    print(f"  écrit dans {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
