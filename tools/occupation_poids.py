#!/usr/bin/env python3
"""occupation_poids.py — M9 : quelle part des poids est réellement STOCKÉE non nulle ?

POURQUOI CET INSTRUMENT EXISTE. Le compteur de paires du moteur additionne `n_in × n_out` par
projection : il mesure le travail d'un noyau **dense**, fidèlement — un noyau dense lit la matrice
entière, zéros compris — mais il ne dit **rien** de ce qui est stocké. Mesuré le 10/10 : 2,3 M de
paires avant comme après un élagage à 50 % de **tous** les tenseurs, sur `--flux`,
`--flux-listes`, `--flux-blocs` et sous `--keep 0.5` (qui fait pourtant chuter la perplexité de
4,56 à 5,82). Le harnais n'est pas mieux loti (0,59 M de « poids lus » pour huit modèles à
100 %, 50 % et 25 % de poids gardés).

Sans ce chiffre, « élaguer divise les paires » n'est vérifiable par **aucun** instrument du dépôt.
C'est le manque **M9**, et ce script est sa première moitié : l'**occupation**, lue dans le fichier.

CE QU'IL MESURE, ET COMMENT. Chaque tenseur est déquantifié (Q8_0, Q4_0, F32 — les formats que
l'exporteur écrit) et on compte les poids **exactement nuls**. Le résultat est donné par **genre**
(attention, experts, table d'entrée, tête) parce qu'un chiffre global cacherait le défaut même
qu'on cherche à voir : une couverture partielle qui se tait.

CE QU'IL PERMET DE DIRE. Avec les paires que le moteur imprime (`--ppl`), l'occupation donne la
**borne basse** de ce qu'un format creux lirait : `paires_creuses ≈ occupation × paires_noyau`,
en supposant les non-nuls répartis comme les activations vivantes. C'est une **hypothèse**, elle
est écrite ici et répétée à l'affichage — pas un résultat.

Usage :
  tools/occupation_poids.py --modele F.gguf [--paires-attention 0.4 --paires-experts 1.8]
"""
from __future__ import annotations

import argparse
import pathlib
import struct
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lecture_etat import _chaine, _valeur, lire_q8_0  # noqa: E402

GGML_F32, GGML_F16, GGML_Q4_0, GGML_Q8_0 = 0, 1, 2, 8


def lire_tout(chemin: str):
    """{nom: (forme, tableau f32)} pour les tenseurs 2D des formats que l'exporteur écrit."""
    f = open(chemin, "rb")
    if f.read(4) != b"GGUF":
        raise SystemExit(f"{chemin} : ce n'est pas un GGUF")
    struct.unpack("<I", f.read(4))[0]
    n_t, n_kv = struct.unpack("<QQ", f.read(16))
    align = 32
    for _ in range(n_kv):
        cle = _chaine(f)
        t = struct.unpack("<I", f.read(4))[0]
        v = _valeur(f, t)
        if cle == "general.alignment":
            align = int(v)
    entetes = []
    for _ in range(n_t):
        nom = _chaine(f)
        nd = struct.unpack("<I", f.read(4))[0]
        dims = [struct.unpack("<Q", f.read(8))[0] for _ in range(nd)]
        ty = struct.unpack("<I", f.read(4))[0]
        off = struct.unpack("<Q", f.read(8))[0]
        entetes.append((nom, dims, ty, off))
    debut = (f.tell() + align - 1) // align * align
    sortie = {}
    for nom, dims, ty, off in entetes:
        n = 1
        for d in dims:
            n *= d
        if ty == GGML_Q8_0 and n % 32 == 0:
            w = lire_q8_0(f, debut + off, n)
        elif ty == GGML_Q4_0 and n % 32 == 0:
            f.seek(debut + off)
            brut = np.frombuffer(f.read((n // 32) * 18), dtype=np.uint8).reshape(-1, 18)
            d = np.ascontiguousarray(brut[:, :2]).view(np.float16).astype(np.float32).reshape(-1, 1)
            qs = brut[:, 2:]
            bas = (qs & 0x0F).astype(np.float32) - 8.0
            haut = ((qs >> 4) & 0x0F).astype(np.float32) - 8.0
            w = (np.concatenate([bas, haut], axis=1) * d).reshape(-1)
        elif ty in (GGML_F32, GGML_F16):
            f.seek(debut + off)
            if ty == GGML_F32:
                w = np.frombuffer(f.read(4 * n), dtype="<f4").astype(np.float32)
            else:
                w = np.frombuffer(f.read(2 * n), dtype="<f2").astype(np.float32)
        else:
            continue
        sortie[nom] = (tuple(dims), np.asarray(w, dtype=np.float32))
    return sortie


def genre(nom: str) -> str:
    if "exps" in nom or "expert" in nom:
        return "experts"
    if "attn" in nom or "q_proj" in nom or "k_proj" in nom or "v_proj" in nom or "o_proj" in nom:
        return "attention"
    if "token_embd" in nom or "embed" in nom:
        return "table d'entrée"
    if "output" in nom or "lm_head" in nom:
        return "tête"
    return "autres"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", required=True)
    ap.add_argument("--paires-attention", type=float, default=None,
                    help="paires/token du moteur pour l'attention (colonne « attention » de la "
                         "ligne « paires », en millions)")
    ap.add_argument("--paires-experts", type=float, default=None,
                    help="idem pour les experts")
    a = ap.parse_args()

    tenseurs = lire_tout(a.modele)
    if not tenseurs:
        raise SystemExit("aucun tenseur lisible (formats gérés : F32, F16, Q8_0, Q4_0)")
    par_genre = {}
    for nom, (_forme, w) in tenseurs.items():
        g = genre(nom)
        nnz, tot = par_genre.get(g, (0, 0))
        par_genre[g] = (nnz + int(np.count_nonzero(w)), tot + w.size)

    n_tot = sum(t for _, t in par_genre.values())
    n_nnz = sum(z for z, _ in par_genre.values())
    print(f"modèle : {pathlib.Path(a.modele).name} · {len(tenseurs)} tenseurs · "
          f"{n_tot:,} poids")
    print()
    print("| genre | poids | non nuls | occupation |")
    print("|---|---:|---:|---:|")
    for g in sorted(par_genre, key=lambda k: -par_genre[k][1]):
        z, t = par_genre[g]
        print(f"| {g} | {t:,} | {z:,} | **{100 * z / t:.1f} %** |")
    print(f"| **total** | **{n_tot:,}** | **{n_nnz:,}** | **{100 * n_nnz / n_tot:.1f} %** |")

    if a.paires_attention is not None or a.paires_experts is not None:
        print()
        print("Ce qu'un format CREUX lirait, en supposant les non-nuls répartis comme les")
        print("activations vivantes (**hypothèse**, pas un résultat) :")
        for g, paires in (("attention", a.paires_attention), ("experts", a.paires_experts)):
            if paires is None:
                continue
            z, t = par_genre.get(g, (0, 1))
            occ = z / t
            print(f"  {g:<10} paires noyau {paires:.2f} M → paires creuses ≈ "
                  f"**{paires * occ:.2f} M** (÷{1 / occ:.2f})")
    else:
        print()
        print("Donner `--paires-attention` et `--paires-experts` (lus sur la ligne « paires » du")
        print("moteur) pour obtenir l'estimation « ce qu'un format creux lirait ».")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
