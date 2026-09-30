"""
Drave — élagage, densité et coût des encodages « par événement ».

Question posée : un modèle quantifié peut-il être élagué assez pour qu'une
approche par événement (on ne traite que les non-nuls) soit rentable ?

Tout se ramène à une seule grandeur : le **coût en bits par poids**, sachant
qu'un poids ternaire non nul ne porte qu'un **signe** (1 bit) — l'information
est dans le fait qu'il soit non nul, pas dans sa valeur.

Encodages comparés, d = densité (fraction de poids non nuls) :

  dense 2 bits        2 b/poids          (codes 00=0, 01=+1, 10=-1)
  bitmap + signe      1 + d b/poids      (1 b/poids pour le bitmap, + 1 b par non-nul)
  CSR plat            34·d b/poids       (indice 32 b + signe 1 b, arrondi)
  CSR bloc 16 bits    17·d b/poids
  N:M structuré       (m + n)/m b/poids  (masque + signes, positions implicites)

Le « bitmap + signe » est le seul encodage événementiel qui **domine** le dense :
il est égal à 2 b/poids en densité 100 % et strictement meilleur en dessous.
"""

from __future__ import annotations

import math

import numpy as np

# --------------------------------------------------------------------------- #
# 1. Élagage
# --------------------------------------------------------------------------- #


def prune_by_magnitude(W: np.ndarray, q: np.ndarray, keep_fraction: float):
    """Élague un tenseur ternaire q en gardant les non-nuls de plus grande |W|.

    keep_fraction s'entend **parmi les non-nuls existants** (1.0 = on garde tout).
    Retourne (q_élagué, densité résultante).
    """
    q = np.asarray(q)
    nz = q != 0
    n_nz = int(nz.sum())
    if n_nz == 0:
        return q.copy(), 0.0
    n_keep = int(round(keep_fraction * n_nz))
    if n_keep >= n_nz:
        return q.copy(), n_nz / q.size
    order = np.argsort(-np.abs(np.where(nz, W, 0.0)), axis=None)
    keep = np.zeros(q.size, dtype=bool)
    keep[order[:n_keep]] = True
    keep = keep.reshape(q.shape) & nz
    out = np.where(keep, q, 0).astype(np.int8)
    return out, int(keep.sum()) / q.size


def prune_nm(W: np.ndarray, q: np.ndarray, n: int, m: int):
    """Élagage structuré N:M : garde les n plus grandes |W| de chaque groupe de m.

    C'est la forme matériellement la plus favorable (positions implicites,
    fenêtre d'activation bornée) — cf. 2:4 sur les tenseurs cores NVIDIA.
    """
    q = np.asarray(q)
    flat_W = np.abs(np.asarray(W)).reshape(-1)
    flat_q = q.reshape(-1)
    n_groups = flat_q.size // m
    rest = flat_q.size - n_groups * m

    Wg = flat_W[:n_groups * m].reshape(n_groups, m)
    qg = flat_q[:n_groups * m].reshape(n_groups, m)
    keep = np.zeros_like(qg, dtype=bool)
    idx = np.argsort(-Wg, axis=1)[:, :n]
    np.put_along_axis(keep, idx, True, axis=1)
    out = np.where(keep, qg, 0).astype(np.int8).reshape(-1)
    if rest:
        out = np.concatenate([out, flat_q[n_groups * m:]])
    return out.reshape(q.shape), float(keep.mean())


# --------------------------------------------------------------------------- #
# 2. Coût des encodages (bits par poids)
# --------------------------------------------------------------------------- #


def bits_per_weight(d: float, scheme: str, **kw) -> float:
    """Coût en bits par poids d'un encodage, à densité d."""
    if scheme == "dense2":
        return 2.0
    if scheme == "bitmap":                     # bitmap (1 b/poids) + signe par non-nul
        return 1.0 + d
    if scheme == "csr32":                      # indice 32 b + signe 1 b par non-nul
        return 33.0 * d
    if scheme == "csr16":
        return 17.0 * d
    if scheme == "nm":                         # masque (m bits / m poids) + signes
        n = kw.get("n", 2)
        m = kw.get("m", 4)
        return (m + n) / m
    if scheme == "block_skip":                 # dense 2 b + 1 b par bloc de B
        B = kw.get("B", 64)
        return 2.0 + 1.0 / B
    raise ValueError(scheme)


def breakeven(scheme_a: str, scheme_b: str, **kw) -> float | None:
    """Densité à laquelle deux encodages coûtent le même nombre de bits/poids."""
    # tous les schémas utiles sont affines en d : a0 + a1·d
    def coefs(s):
        f0, f1 = bits_per_weight(0.0, s, **kw), bits_per_weight(1.0, s, **kw)
        return f0, f1 - f0

    a0, a1 = coefs(scheme_a)
    b0, b1 = coefs(scheme_b)
    if abs(a1 - b1) < 1e-12:
        return None
    d = (b0 - a0) / (a1 - b1)
    return d if 0.0 <= d <= 1.0 else None


def speedup_vs_dense(d: float, scheme: str, **kw) -> float:
    """Gain de débit (borné par la mémoire) par rapport au dense 2 bits."""
    return bits_per_weight(1.0, "dense2") / bits_per_weight(d, scheme, **kw)


# --------------------------------------------------------------------------- #
# 3. Densité des activations (l'autre moitié du problème événementiel)
# --------------------------------------------------------------------------- #


def relu_density(x: np.ndarray) -> float:
    """Fraction d'activations non nulles après ReLU — un événement n'existe que si
    l'activation *et* le poids sont non nuls."""
    return float((x > 0).mean())


def joint_density(w_density: float, a_density: float) -> float:
    """Densité des événements réels (poids ET activation non nuls), en supposant
    l'indépendance — hypothèse optimiste mais usuelle."""
    return w_density * a_density
