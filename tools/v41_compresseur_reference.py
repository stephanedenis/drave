#!/usr/bin/env python3
"""Référence numpy du **compresseur de V4.1** (ratios 1 et 2), hors du moteur.

Recopiée de la référence d'exécution :
`vllm/models/deepseek_v41/common/ops/fused_compress_quant_cache.py`
(`_fused_save_compress_norm_kernel` et `_store_latent`) et
`vllm/models/deepseek_v41/compressor.py` (`has_gate = compress_ratio > 1`).
Le noyau dit exactement :

  * ratio 1 : `pooled = kv` — aucun groupe, aucune porte, aucun `ape` ;
  * ratio 2 : `pooled = sum(kv * softmax(score, axis=0), axis=0)` — un softmax
    **par canal** sur les `ratio` jetons du groupe ;
  * puis `variance = sum(pooled²)/512`, `normed = pooled * rsqrt(variance + eps)
    * poids`, et le RoPE n'est appliqué qu'aux **64 dernières** composantes
    (`pair = arange(256) - 224`), à la position du PREMIER jeton du groupe
    (`position // ratio * ratio`), en appariement **NORM** (paires 2i, 2i+1).

Ce que ce script sert à vérifier : la projection (`attn_compressor_kv`), la
norme, le RoPE de bloc et l'instant d'émission du bloc — contre les vides
`comp_brut<bloc>` et `comp_bloc<bloc>` du moteur.

Limite assumée : l'état injecté est le MÊME à toutes les positions (l'injection
par position demande un fichier REFD). Le pool d'un groupe y vaut donc la valeur
du jeton quel que soit le jeu de poids — ce script ne prouve PAS l'orientation du
softmax par canal ; c'est le test unitaire Rust qui s'en charge.

Usage :
    python3 tools/v41_compresseur_reference.py <modele.gguf> <prefixe_dump> \
        <couche> <etat.bin> [positions…]
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier_v41_mhc import Gguf          # lecteur GGUF (F32/F16) déjà écrit

EPS = 1e-20        # `rms_norm_eps` de V4.1
BASE_COMP = 160000.0   # `compress_rope_theta`


def rms_norm(x, poids, eps=EPS):
    return x / np.sqrt(np.mean(x * x) + eps) * poids


def rope_norm(vecteur, pos, base, n_rot):
    """RoPE « NORM » (paires 2i, 2i+1) sur `n_rot` composantes — celui du
    compresseur (`_rope_quant_insert_kernel`, `tl.split(reshape(., (256,2)))`)."""
    v = vecteur.copy()
    demi = n_rot // 2
    for i in range(demi):
        theta = pos / (base ** (2.0 * i / n_rot))
        c, s = np.cos(theta), np.sin(theta)
        a, b = v[2 * i], v[2 * i + 1]
        v[2 * i] = a * c - b * s
        v[2 * i + 1] = b * c + a * s
    return v


def dump(prefixe, nom, couche, pos):
    return np.fromfile(f"{prefixe}-{nom}-{couche}-{pos}.bin", dtype="<f4").astype(np.float64)


def main():
    modele, prefixe, couche, etat_f = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    reste = [int(v) for v in sys.argv[5:]]
    ratio = reste.pop(0)
    positions = reste or list(range(min(4, 8)))
    g = Gguf(modele)
    norme_attn = g.lire(f"blk.{couche}.attn_norm.weight").reshape(-1)
    kv_w = g.lire(f"blk.{couche}.attn_compressor_kv.weight")       # [512, 5120]
    norme_comp = g.lire(f"blk.{couche}.attn_compressor_norm.weight").reshape(-1)
    hd = norme_comp.size
    a_gate = f"blk.{couche}.attn_compressor_gate.weight" in g.tenseurs
    gate_w = (g.lire(f"blk.{couche}.attn_compressor_gate.weight") if a_gate else None)
    a_ape = f"blk.{couche}.attn_compressor_ape.weight" in g.tenseurs
    print(f"# couche {couche} · ratio {ratio} · hd {hd} · porte "
          f"{'OUI' if a_gate else 'NON'} · ape {'OUI' if a_ape else 'NON'}")
    assert (ratio > 1) == a_gate, "la porte doit exister si et seulement si ratio > 1"
    # La couche consomme `hn = rmsnorm(xin, attn_norm)` où `xin` est la copie 0 de
    # l'état (premier raccord de la plage → convention de sonde).
    etat = np.fromfile(etat_f, dtype="<f4").astype(np.float64)
    xin = etat[:len(norme_attn)]
    hn = rms_norm(xin, norme_attn)
    kv = kv_w @ hn
    portes = (gate_w @ hn) if a_gate else None
    print(f"# |hn| {np.linalg.norm(hn):.6e} · |kv| {np.linalg.norm(kv):.6e}")
    nope = hd - 64
    for pos in positions:
        # Un bloc n'est publié qu'à la fin d'un groupe — la référence le dit en
        # une ligne : `if (position + 1) % COMPRESS_RATIO != 0: return`.
        if (pos + 1) % ratio:
            print(f"  pos {pos} : pas de bloc (le groupe n'est pas complet)")
            continue
        bloc = pos // ratio
        f_brut = f"{prefixe}-comp_brut{bloc}-{couche}-{pos}.bin"
        f_bloc = f"{prefixe}-comp_bloc{bloc}-{couche}-{pos}.bin"
        if not os.path.exists(f_brut):
            print(f"  pos {pos} : aucun vide « {f_brut} »")
            continue
        # L'état est le même à toutes les positions : le pool d'un groupe vaut
        # alors la valeur du jeton quel que soit le jeu de poids (limite assumée).
        pool = kv.copy()
        if a_gate and ratio > 1:
            tous = np.stack([portes] * ratio)
            e = np.exp(tous - tous.max(axis=0, keepdims=True))
            poids = e / e.sum(axis=0, keepdims=True)
            pool = (np.stack([kv] * ratio) * poids).sum(axis=0)
        norme = rms_norm(pool, norme_comp)
        debut = pos + 1 - ratio
        attendu_bloc = norme.copy()
        attendu_bloc[nope:] = rope_norm(norme[nope:], debut, BASE_COMP, 64)
        obtenu_brut = dump(prefixe, f"comp_brut{bloc}", couche, pos)
        obtenu_bloc = dump(prefixe, f"comp_bloc{bloc}", couche, pos)
        e1 = np.max(np.abs(pool - obtenu_brut))
        e2 = np.max(np.abs(attendu_bloc - obtenu_bloc))
        dyn = np.max(np.abs(obtenu_bloc))
        ok = max(e1, e2) < 1e-4 * max(dyn, 1e-9) + 1e-6
        print(f"  pos {pos} (bloc {bloc}, début {debut}) : pool {e1:.3e} · "
              f"norme+rope {e2:.3e}  (dynamique {dyn:.3e})  {'OK ' if ok else 'ÉCART'}")


if __name__ == "__main__":
    main()
