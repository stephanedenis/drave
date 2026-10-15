#!/usr/bin/env python3
"""vision_hf_ref.py — la tour de vision du MOTEUR, vérifiée par une SECONDE implémentation.

POURQUOI. `--banc-vision` sait maintenant dérouler la tour entière de Qwen2-VL (32 couches,
rotation 2-D, fenêtre locale, `v.post_ln`, projecteur `mm.0`/`mm.2`) — mais elle n'était vérifiée
que sur sa PREMIÈRE tranche (l'embedding de patchs, 5,4e-7 contre la référence numpy). Une
implémentation qui « tourne » n'est pas une implémentation qui « a raison » : il faut une
**seconde implémentation**, écrite indépendamment, sur la MÊME image.

CE QUE CE SCRIPT FAIT. Il reconstruit l'image synthétique **exactement** comme le banc du moteur
(224 × 224, dégradé `(x + y + c)/(2·cote)`, carré central 10..17 en valeur 1), la donne à la tour
de vision de `transformers` (`Qwen2VLForConditionalGeneration.visual`) et compare ses 64 jetons
fusionnés × 1536 canaux à ceux que le moteur a écrits.

CE QUE LA COMPARAISON VAUT, ET SA LIMITE, DITE D'AVANCE. Le moteur lit des poids **Q8_0** (le
mmproj quantifié) ; la référence lit des poids **bf16**. L'écart mesuré contient donc la
quantification — il ne peut pas descendre à 1e-6 comme la tranche des patchs (qui comparait la même
arithmétique sur les mêmes poids). Ce qui est vérifié ici est l'**ARCHITECTURE** : les bonnes
matrices, la bonne activation, la bonne rotation, la bonne fenêtre, le bon projecteur. Un écart
systématique le dirait tout de suite ; un accord à ~1 % dit que la structure est la bonne et que
le reste est de la quantification.

Usage :
  python tools/vision_hf_ref.py --hf /home/stephane/IA/cache/huggingface/qwen2vl-ref \\
      --moteur /tmp/vision-tour.bin.projecteur
"""
from __future__ import annotations

import argparse
import pathlib
import struct

import numpy as np


def image_du_banc(cote: int = 224, cin: int = 3) -> np.ndarray:
    """L'image du banc, reconstruite à l'IDENTIQUE (mêmes formules, même ordre)."""
    img = np.zeros((cin, cote, cote), dtype=np.float32)
    for y in range(cote):
        for x in range(cote):
            carre = 10 <= x < 18 and 10 <= y < 18
            for c in range(cin):
                img[c, y, x] = 1.0 if carre else (x + y + c) / (2.0 * cote)
    return img


def lire_jetons(chemin: str) -> tuple[np.ndarray, int]:
    """Le fichier `.jetons` du moteur : [int32 n_jetons][int32 n_canaux][f32 × n_jetons × n_canaux].

    ⚠️ Le fichier `.projecteur`, lui, contient les POIDS (quatre entiers puis w0, b0, w2, b2) : la
    première version de ce script l'a pris pour la sortie et a compté 34 085 379 valeurs pour 5 120
    jetons — l'erreur venait du format supposé, pas de la tour.
    """
    brut = pathlib.Path(chemin).read_bytes()
    n, c = struct.unpack_from("<ii", brut, 0)
    vals = np.frombuffer(brut, dtype="<f4", offset=8)
    if vals.size != n * c:
        raise SystemExit(f"  ❌ {vals.size} valeurs pour {n} × {c} annoncées")
    return vals.reshape(n, c), n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True, help="dossier des poids de référence (safetensors)")
    ap.add_argument("--moteur", required=True, help="fichier .jetons écrit par --banc-vision")
    ap.add_argument("--cote", type=int, default=224)
    a = ap.parse_args()

    import torch
    from transformers import AutoModelForImageTextToText

    ref, n_ref = lire_jetons(a.moteur)
    print(f"moteur   : {n_ref} jetons × {ref.shape[1]} canaux · |sortie| = {np.linalg.norm(ref):.4f}")

    modele = AutoModelForImageTextToText.from_pretrained(a.hf, dtype=torch.float32)
    modele.eval()
    img = image_du_banc(a.cote)
    # ⚠ LA TOUR DE QWEN2-VL NE PREND PAS UNE IMAGE [1, C, H, W] : elle prend des PATCHS APLATIS,
    # [n_patch, C · t · 14 · 14], dans l'ordre de lecture, et une grille (t, h, w). Le premier
    # essai a donné une image 4-D et `transformers` a échoué dans la rotation (« size of tensor a
    # (128) must match b (256) ») — l'erreur venait du format, pas de la tour.
    n_cote = a.cote // 14
    cadre = 2                                                   # temporal_patch_size de Qwen2-VL
    fusion = 2                                                  # spatial_merge_size
    # ⚠ L'ORDRE DES PATCHS N'EST PAS L'ORDRE DE LECTURE. `get_vision_position_ids` attribue à
    # l'indice 2 la position (1, 0) et à l'indice 4 la position (0, 2) — mesuré sur une grille
    # 4 × 4 : la séquence est ordonnée par BLOCS de fusion 2 × 2 (quatre patchs consécutifs par
    # bloc), pas ligne par ligne. Nourrir la référence en ordre de lecture (ce que faisait la
    # première version) décale donc TOUTES les positions dès le troisième patch — de quoi
    # expliquer à elle seule l'essentiel de l'écart de 55 à 78 %.
    ordre = []                                                  # indice de séquence → (ligne, colonne)
    for by in range(n_cote // fusion):
        for bx in range(n_cote // fusion):
            for dy in range(fusion):
                for dx in range(fusion):
                    ordre.append((by * fusion + dy, bx * fusion + dx))
    patchs = np.zeros((n_cote * n_cote, 3 * cadre * 14 * 14), dtype=np.float32)
    for k, (py, px_) in enumerate(ordre):
        bloc = img[:, py * 14:(py + 1) * 14, px_ * 14:(px_ + 1) * 14]          # [3, 14, 14]
        for c in range(3):
            for t_ in range(cadre):                                            # image fixe : 2 fois
                deb = (c * cadre + t_) * 196
                patchs[k, deb:deb + 196] = bloc[c].reshape(-1)
    px = torch.tensor(patchs, dtype=torch.float32)               # [n_patch, C·t·14·14]
    grille = torch.tensor([[1, n_cote, n_cote]], dtype=torch.long)
    with torch.no_grad():
        brut_hf = modele.model.visual(px, grid_thw=grille)
        # Selon la version de `transformers`, la tour rend un tenseur ou un objet de sortie :
        # les deux sont acceptés (et l'erreur « no attribute float » a coûté un essai).
        tenseur = brut_hf if hasattr(brut_hf, "float") else brut_hf.last_hidden_state
        sortie = tenseur.float().cpu().numpy()
    print(f"référence: {sortie.shape[0]} jetons × {sortie.shape[1]} canaux · "
          f"|sortie| = {np.linalg.norm(sortie):.4f}")

    # Le moteur écrit ses patchs dans l'ORDRE DE LECTURE : on ramène la sortie de la référence
    # (ordre par blocs) dans ce même ordre avant de comparer quoi que ce soit.
    if sortie.shape[0] == len(ordre):
        inverse = np.empty(len(ordre), dtype=int)
        for k, (py, px_) in enumerate(ordre):
            inverse[k] = py * n_cote + px_
        sortie = sortie[inverse]
    if sortie.shape != ref.shape:
        print(f"  ❌ FORMES DIFFÉRENTES : moteur {ref.shape} contre référence {sortie.shape}")
        return 1
    # La comparaison qui a du sens ici : la STRUCTURE (corrélation, cosinus) et l'écart relatif
    # global — pas le 1e-6 de la même arithmétique.
    cos = float((ref.ravel() @ sortie.ravel()) /
                (np.linalg.norm(ref) * np.linalg.norm(sortie) + 1e-12))
    ecart = float(np.linalg.norm(ref - sortie) / (np.linalg.norm(sortie) + 1e-12))
    par_jeton = np.linalg.norm(ref - sortie, axis=1) / (np.linalg.norm(sortie, axis=1) + 1e-12)
    print(f"\n  cosinus (moteur ↔ référence)        : {cos:+.6f}")
    print(f"  écart relatif global (‖Δ‖/‖réf‖)    : {ecart * 100:.2f} %")
    print(f"  écart par jeton : médian {np.median(par_jeton) * 100:.2f} % · "
          f"max {par_jeton.max() * 100:.2f} % (jeton {int(par_jeton.argmax())})")
    print("\n  lecture : cosinus > 0,99 et écart de l'ordre du pour cent ⇒ l'ARCHITECTURE est la")
    print("  bonne (les matrices, l'activation, la rotation, la fenêtre, le projecteur) et le")
    print("  reste est la quantification Q8_0 du mmproj. Un cosinus bas désignerait la structure.")
    return 0 if cos > 0.99 else 1


if __name__ == "__main__":
    raise SystemExit(main())
