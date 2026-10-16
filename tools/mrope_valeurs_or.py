#!/usr/bin/env python3
"""mrope_valeurs_or.py — LES VALEURS D'OR DU mRoPE, OBTENUES PAR COMPORTEMENT.

POURQUOI PAS EN APPELANT LA RÉFÉRENCE. Le pas 1 du projet mRoPE (`rapport-vision-qwen2vl.md` § 4)
était « extraire les positions que la référence calcule » ✗ — et il a résisté : **dans la version
installée, `get_rope_index` et son helper ne s'accordent pas** ✗✓ (le premier lui passe la **ligne 1-D**
de son itérateur quand le second attend un tenseur **2-D**, et une fois réparé il rend **16 positions
pour une image qui produit 4 jetons** : il numérote les **patchs**, la séquence porte les jetons
**fusionnés**). Lire le code d'une version et l'appeler dans une autre, c'est mesurer deux choses à la
fois ✗.

CE QUE CET OUTIL FAIT À LA PLACE : il **fait parler le modèle** ✓.
  1. on lui donne la séquence (texte + image + texte) et on laisse les positions **par défaut** ✓ ;
     on garde ses **logits** — c'est la vérité à reproduire ✓ ;
  2. on lui redonne la **même** séquence avec des `position_ids` **explicites**, candidats successifs ✓ ;
  3. le candidat qui reproduit les logits **au bit près** (ou à un epsilon dit ✓) **est** la convention
     de la version installée ✓✓ — sans lire une ligne de son code ✗.

Les candidats essayés, et pourquoi eux (tout ce que la nuit a mesuré de la convention ✗) :
  · **A** texte `(p,p,p)`, image `(t,h,w)` en **block-major** (0→(0,0), 1→(0,1), 2→(1,0), 3→(1,1)) ✓,
    le texte après l'image reprenant à `max + 1` ✓ — la convention documentée par Qwen ✓ ;
  · **B** la même, mais l'image en **raster** ((0,0), (0,1), (1,0), (1,1) sur la grille **fusionnée**) ✓ ;
  · **C** des positions **dégénérées** (t = h = w = p ✓) : si c'est C qui gagne, alors la version
    installée **n'applique pas** le mRoPE sur cette entrée ✗ — et ce serait une information ✓.

⚠️ CE QU'IL FAUT POUR LE LANCER : le modèle de référence en mémoire (~4,4 Go en f32 ✗) — donc **pas
pendant une passe de portes** ✗ (les portes mesurent des latences, et un modèle qui prend la carte les
fausse ✓). C'est écrit ici pour que personne (moi compris) ne le lance au mauvais moment ✓.

Usage :
  CUDA_VISIBLE_DEVICES=0 python tools/mrope_valeurs_or.py --hf <dossier safetensors> \\
      [--cote 4] [--epsilon 0] [--sortie /tmp/mrope-valeurs-or.json]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np
import torch


def grille_et_jetons(cote: int, fusion: int = 2):
    """La grille d'image et le nombre de jetons APRÈS fusion (c'est ce que la séquence porte)."""
    return (1, cote, cote), (cote // fusion) ** 2


def positions_candidates(cote: int, n_texte_avant: int, fusion: int = 2):
    """Les conventions candidates, en (nom, tenseur (3, T)).

    ⚠️ IL FAUT UNE GRILLE FUSIONNÉE PLUS GRANDE QUE 2 × 2 POUR QUE LES CANDIDATS DIFFÈRENT : sur une
    grille 2 × 2, « par blocs » et « en raster » donnent **le même** ordre ✗ (le premier essai l'a
    montré : les candidats A et B sortaient identiques ✓✗). Avec 8 × 8 (fusionné en 4 × 4), les deux
    ordres se séparent : par blocs `h = 0,0,1,1,0,0,1,1…`, en raster `h = 0,0,0,0,1,1,1,1…` ✓.
    """
    cotes, n_img = grille_et_jetons(cote, fusion)
    n_lignes = cote // fusion
    poses = {}
    # A — par BLOCS 2 × 2 : chaque bloc livre ses quatre jetons dans l'ordre (dy, dx) avant le suivant
    bloc = []
    for i in range(0, n_lignes, 2):
        for j in range(0, n_lignes, 2):
            for dy in range(2):
                for dx in range(2):
                    bloc.append((i + dy, j + dx))
    # B — en RASTER : ligne par ligne sur la grille fusionnée
    raster = [(i, j) for i in range(n_lignes) for j in range(n_lignes)]
    for nom, couples in (("A_par_blocs", bloc), ("B_raster", raster)):
        t = [0] * n_texte_avant + [0] * n_img          # une seule trame : t = 0 partout sur l'image
        h = [0] * n_texte_avant + [i for (i, _) in couples]
        w = [0] * n_texte_avant + [j for (_, j) in couples]
        base = cote // fusion                          # le texte après l'image reprend à max + 1
        t += [base + k for k in range(3)]
        h += [base + k for k in range(3)]
        w += [base + k for k in range(3)]
        poses[nom] = np.stack([t, h, w])
    # C — dégénéré : les trois lignes égales (aucun mRoPE)
    t = list(range(n_texte_avant + n_img + 3))
    poses["C_degenere"] = np.stack([t, t, t])
    return poses


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True, help="dossier des poids de référence (safetensors)")
    ap.add_argument("--cote", type=int, default=4, help="côté de la grille d'image (4 => 4 jetons)")
    ap.add_argument("--texte-avant", type=int, default=4)
    ap.add_argument("--texte-apres", type=int, default=3)
    ap.add_argument("--epsilon", type=float, default=0.0,
                    help="tolérance sur les logits (0 = au bit près)")
    ap.add_argument("--sortie", default="/tmp/mrope-valeurs-or.json")
    a = ap.parse_args()

    from transformers import AutoModelForImageTextToText
    m = AutoModelForImageTextToText.from_pretrained(a.hf, dtype=torch.float32).eval()

    cotes, n_img = grille_et_jetons(a.cote)
    ids = [9707] * a.texte_avant + [151655] * n_img + [44] * a.texte_apres
    n = len(ids)
    grille = torch.tensor([[1, a.cote, a.cote]])
    # les « pixel_values » : n_img patchs de la bonne dimension, valeurs quelconques mais FIXES
    coté_patch = 14
    n_canaux = 3 * 2 * coté_patch * coté_patch
    rng = np.random.default_rng(0)
    patchs = torch.tensor(rng.standard_normal((a.cote * a.cote, n_canaux)).astype(np.float32) * 0.1)
    type_jeton = torch.zeros(1, n, dtype=torch.long)
    type_jeton[0, a.texte_avant:a.texte_avant + n_img] = 1

    def logits(position_ids=None):
        kw = dict(input_ids=torch.tensor([ids]), pixel_values=patchs, image_grid_thw=grille,
                  attention_mask=torch.ones(1, n, dtype=torch.long),
                  mm_token_type_ids=type_jeton)
        if position_ids is not None:
            kw["position_ids"] = torch.tensor(np.asarray(position_ids)[None])   # (1, 3, T)
        with torch.no_grad():
            return m(**kw).logits[0].float().numpy()

    print(f"séquence : {a.texte_avant} texte + {n_img} image ({a.cote}×{a.cote} fusionné) "
          f"+ {a.texte_apres} texte = {n} jetons")
    ref = logits(None)
    print(f"logits par DÉFAUT : {ref.shape} · norme {np.linalg.norm(ref):.4f}")

    gagnants = []
    for nom, pos in positions_candidates(a.cote, a.texte_avant).items():
        if pos.shape[1] != n:
            print(f"  {nom:14s} : {pos.shape[1]} positions pour {n} jetons — écarté ✗")
            continue
        ecart = float(np.abs(logits(pos) - ref).max())
        ok = ecart <= a.epsilon
        print(f"  {nom:14s} : écart max aux logits {ecart:.3e}" + ("   ← REPRODUIT ✓✓" if ok else ""))
        if ok:
            gagnants.append((nom, pos))

    if not gagnants:
        print()
        print("  ❌ AUCUN candidat ne reproduit la sortie par défaut.")
        print("     Ce n'est pas un échec : c'est la mesure qui dit que la convention de cette version")
        print("     n'est AUCUNE des trois — il faut alors en lire la source (et pas la deviner ✓).")
        return 1
    nom, pos = gagnants[0]
    print()
    print(f"  ✅ LA CONVENTION DE CETTE VERSION EST : {nom}")
    for k, etiquette in enumerate(("t", "h", "w")):
        print(f"     {etiquette} : {pos[k].tolist()}")
    pathlib.Path(a.sortie).write_text(json.dumps(
        {"convention": nom, "positions": pos.tolist(), "cote": a.cote,
         "texte_avant": a.texte_avant, "texte_apres": a.texte_apres}, indent=1))
    print(f"  écrit dans {a.sortie} — ce sont les VALEURS D'OR à vérifier en Rust (pas 2)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
