"""
Qtrinet — encodages de *structure* : éliminer complètement la valeur.

Idée : si tous les poids valent ±1, la valeur n'a plus besoin d'être stockée.
On remplace la matrice par **deux listes de destinations** par source (les « + »
et les « − »). Le signe est porté par l'appartenance à la liste ; il ne reste
que des **positions**, c'est-à-dire un graphe biparti signé.

Conséquence : le coût n'est plus « 1 bit par poids + 1 bit par non-nul » mais
seulement le coût de l'information de *position*. Comme chaque liste est triée,
on encode des **écarts (deltas)** — c'est exactement ce que font les formats de
graphes compressés (WebGraph/LLP).

Conventions de coût, en BITS, mesurées sur la matrice réelle :

  bitmap + signe    n + nnz              (1 b/poids + 1 b par non-nul)
  listes signées    Σ_lignes 2·32 + Σ_écarts γ(gap)   (aucun bit de valeur)
  CSR plat          nnz·(32 + k) + lignes·32
  dense k bits      n·k

γ(x) = code d'Elias gamma : 2·⌊log2 x⌋ + 1 bits — bon proxy d'un code
variable réel, et proche de l'entropie des écarts (loi géométrique).
"""

from __future__ import annotations

import math

import numpy as np


def gamma_bits(x: int) -> int:
    """Longueur du code d'Elias gamma pour un entier positif."""
    if x <= 0:
        return 1
    return 2 * (x.bit_length() - 1) + 1


def list_cost_row(positions: np.ndarray) -> int:
    """Coût des écarts d'une liste triée de positions (hors en-tête)."""
    if positions.size == 0:
        return 0
    gaps = np.diff(np.concatenate(([-1], positions)))
    return int(sum(gamma_bits(int(g)) for g in gaps))


def signed_lists_cost(q: np.ndarray, header_bits: int = 32) -> int:
    """Coût des deux listes signées (+, −) par ligne, écarts compris."""
    q = np.asarray(q)
    total = 0
    for i in range(q.shape[0]):
        row = q[i]
        pos_p = np.flatnonzero(row > 0)
        pos_m = np.flatnonzero(row < 0)
        total += 2 * header_bits                       # longueur des 2 listes
        total += list_cost_row(pos_p) + list_cost_row(pos_m)
    return total


def bitmap_sign_cost(q: np.ndarray) -> int:
    """1 bit par poids (bitmap des non-nuls) + 1 bit par non-nul (le signe)."""
    q = np.asarray(q)
    return int(q.size + np.count_nonzero(q))


def csr_flat_cost(q: np.ndarray, idx_bits: int = 32, sign_bits: int = 1) -> int:
    q = np.asarray(q)
    return int(np.count_nonzero(q) * (idx_bits + sign_bits) + q.shape[0] * 32)


def dense_cost(q: np.ndarray, bits: int) -> int:
    return int(np.asarray(q).size * bits)


def entropy_bound(q: np.ndarray, block: int | None = None) -> float:
    """Borne informationnelle : entropie des positions des non-nuls.

    Sans structure : H ≈ nnz·log2(n/nnz) + nnz·log2(e)  (modèle de Poisson)
    Avec blocs : les positions intra-bloc sont limitées au bloc.
    """
    q = np.asarray(q)
    n = q.size
    nnz = int(np.count_nonzero(q))
    if nnz == 0:
        return 0.0
    if block is None:
        return nnz * (math.log2(n / nnz) + math.log2(math.e))
    n_blocks = n // block
    return nnz * math.log2(block) + n_blocks


def block_statistics(q: np.ndarray, block: int = 8) -> dict:
    """Répartition des non-nuls par bloc — un motif groupé coûte moins cher."""
    q = np.asarray(q)
    flat = (q != 0).astype(np.int32).reshape(-1)
    nb = flat.size // block
    if nb == 0:
        return {"blocks": 0, "nonempty": 0.0, "mean_gap": float("nan")}
    counts = flat[:nb * block].reshape(nb, block).sum(axis=1)
    pos = np.flatnonzero(q.reshape(-1))
    gaps = np.diff(pos) if pos.size > 1 else np.array([1])
    return {
        "blocks": int(nb),
        "nonempty": float((counts > 0).mean()),
        "mean_gap": float(gaps.mean()) if gaps.size else float("nan"),
    }


# --------------------------------------------------------------------------- #
# 4. Coût projeté sur une ligne de largeur réaliste
# --------------------------------------------------------------------------- #


def projected_list_cost(d: float, N: int = 4096, header_bits: int = 32, k: int = 1) -> float:
    """Coût (bits/poids) des listes signées pour une ligne de largeur N, densité d.

    L'en-tête (longueur des deux listes) est amorti sur N : c'est lui qui rend
    l'encodage ruineux sur une petite matrice, et négligeable sur une vraie.
    L'écart moyen entre non-nuls d'une ligne vaut N/nnz = 1/d.
    """
    nnz = d * N
    if nnz <= 0:
        return 2 * header_bits / N
    gap = N / nnz
    gb = gamma_bits(int(round(gap)))
    return (2 * header_bits + nnz * gb) / N + (0.0 if k == 1 else d * k)


def projected_bitmap_cost(d: float, k: int = 1) -> float:
    """bitmap (1 b/poids) + k bits par non-nul — indépendant de la largeur."""
    return 1.0 + k * d


def crossover_density(N: int = 4096, header_bits: int = 32, k: int = 1) -> float | None:
    """Densité sous laquelle les listes signées battent le bitmap."""
    lo, hi = 1e-4, 0.999
    if projected_list_cost(hi, N, header_bits, k) <= projected_bitmap_cost(hi, k):
        return hi
    if projected_list_cost(lo, N, header_bits, k) >= projected_bitmap_cost(lo, k):
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if projected_list_cost(mid, N, header_bits, k) < projected_bitmap_cost(mid, k):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
