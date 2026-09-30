"""
Drave — quantification ternaire et multi-bits, encodages matériels.

Aucune dépendance hors numpy.

Vocabulaire
-----------
- ternaire (BitNet b1.58) : w ≈ scale * q, q ∈ {-1, 0, +1}       → 2 bits/poids en dense
- multi-bits              : w ≈ scale * Σ_b 2^b * m_b, m_b ∈ {0,1}  (signe-magnitude)
                            décomposé en `bits` plans, chacun valant ±m_b ∈ {-1,0,+1}
                            → c'est le « bit-slicing » du cahier des charges

Toutes les fonctions de taille renvoient des BITS.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

# --------------------------------------------------------------------------- #
# 1. Quantification
# --------------------------------------------------------------------------- #


def ternarize(W: np.ndarray, per_channel: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """Quantifie W en ternaire {-1,0,+1}. Retourne (q, scale) tels que W ≈ scale*q.

    Convention : W est de forme (d_in, d_out), le calcul est X @ W — donc les
    canaux de sortie sont les COLONNES. L'échelle par canal est prise sur axis=0
    et vaut (1, d_out), ce qui la rend diffusable sur (batch, d_out).

    per_channel=True → une échelle par neurone de sortie (comme BitNet).
    """
    W = np.asarray(W, dtype=np.float32)
    if per_channel:
        scale = np.abs(W).max(axis=0, keepdims=True)
    else:
        scale = np.abs(W).max()
    scale = np.where(scale == 0, 1.0, scale).astype(np.float32)
    q = np.clip(np.round(W / scale), -1, 1).astype(np.int8)
    return q, scale


def quantize_bits(
    W: np.ndarray, bits: int, per_channel: bool = True
) -> tuple[np.ndarray, np.ndarray]:
    """Quantification signe-magnitude sur `bits` bits de magnitude.

    La magnitude est arrondie sur [0, 2^bits - 1] ; le signe est porté à part.
    Retourne (Wq_entier_signe, scale) tels que W ≈ scale * Wq.
    Même convention d'axe que `ternarize` (échelle par colonne).
    """
    if bits < 1:
        raise ValueError("bits >= 1")
    W = np.asarray(W, dtype=np.float32)
    qmax = float((1 << bits) - 1)
    if per_channel:
        scale = np.abs(W).max(axis=0, keepdims=True)
    else:
        scale = np.abs(W).max()
    scale = np.where(scale == 0, 1.0, scale).astype(np.float32)
    # magnitude quantifiée, signe séparé (signe-magnitude, pas complément à 2)
    mag = np.round(np.abs(W) / scale * qmax).clip(0, qmax).astype(np.int32)
    sign = np.where(W < 0, -1, 1).astype(np.int32)
    return (sign * mag).astype(np.int32), scale


def bit_planes(Wq: np.ndarray, bits: int) -> list[np.ndarray]:
    """Décompose Wq (entier signé) en `bits` plans ternaires {-1,0,+1}.

    Plan b = signe(Wq) * bit_b(|Wq|) : c'est exactement la décomposition du CDC
    (magnitude découpée en plans, signe appliqué à chaque plan), et elle vérifie
        Wq = Σ_b 2^b * plan_b
    """
    Wq = np.asarray(Wq)
    mag = np.abs(Wq)
    sign = np.where(Wq < 0, -1, 1)
    return [((mag >> b) & 1) * sign for b in range(bits)]


def planes_to_int(planes: list[np.ndarray]) -> np.ndarray:
    """Reconstruit l'entier signé depuis ses plans (vérification)."""
    out = np.zeros_like(planes[0], dtype=np.int64)
    for b, p in enumerate(planes):
        out += (1 << b) * p.astype(np.int64)
    return out


# --------------------------------------------------------------------------- #
# 2. Encodages matériels : taille en bits
# --------------------------------------------------------------------------- #


def size_dense_ternary(n: int) -> int:
    """Ternaire dense : 2 bits par poids (codes 01=+1, 10=-1, 00=0, 11 libre)."""
    return 2 * n


def size_dense_multibit(n: int, bits: int) -> int:
    """Multi-bits dense : 1 bit par plan × bits plans (pas de signe séparé :
    le signe est déjà appliqué dans chaque plan ternaire)."""
    return bits * n


def size_bitmap_planes(planes: list[np.ndarray]) -> int:
    """Un bitmap de non-nuls + un bitmap de signe par plan = 2 bits/poids/plan."""
    return sum(2 * p.size for p in planes)


def size_csr_planes(planes: list[np.ndarray], idx_bits: int = 32) -> int:
    """CSR par plan (l'approche du cahier des charges d'origine) :
    data 2 bits + indices idx_bits bits par non-nul, + indptr par ligne.
    """
    total = 0
    for p in planes:
        n_rows = p.shape[0]
        nnz = int(np.count_nonzero(p))
        total += nnz * (2 + idx_bits) + n_rows * idx_bits
    return total


def size_entropy_ternary(n: int) -> float:
    """Borne entropique d'un poids ternaire : log2(3) = 1,585 bit."""
    return n * math.log2(3)


@dataclass
class PlaneStats:
    index: int
    density: float
    nnz: int
    size: int


def plane_stats(planes: list[np.ndarray]) -> list[PlaneStats]:
    return [
        PlaneStats(
            index=b,
            density=float(np.count_nonzero(p)) / p.size,
            nnz=int(np.count_nonzero(p)),
            size=p.size,
        )
        for b, p in enumerate(planes)
    ]


# --------------------------------------------------------------------------- #
# 3. Inférence entière (ce que fera le FPGA : add/sub, aucun DSP)
# --------------------------------------------------------------------------- #


def quantize_activations(X: np.ndarray, bits: int = 8, per_tensor: bool = True):
    """Active en entier signé, échelle par tenseur (comme BitNet)."""
    X = np.asarray(X, dtype=np.float32)
    qmax = float((1 << (bits - 1)) - 1)
    amax = np.abs(X).max() if per_tensor else np.abs(X).max(axis=0, keepdims=True)
    amax = amax if amax > 0 else 1.0
    scale = amax / qmax
    Xq = np.clip(np.round(X / scale), -qmax, qmax).astype(np.int32)
    return Xq, scale


def integer_mac(Xq: np.ndarray, q: np.ndarray) -> np.ndarray:
    """Accumulation entière exacte : Xq (int) @ q (ternaire) → int64.

    C'est l'opération du PE : chaque poids ternaire = addition, soustraction ou NOP.
    """
    return Xq.astype(np.int64) @ q.astype(np.int64)


def integer_linear(X: np.ndarray, q: np.ndarray, scale: np.ndarray,
                   act_bits: int = 8, bias: np.ndarray | None = None):
    """Couche linéaire complète en arithmétique entière + remise à l'échelle.

    Le biais est ajouté APRÈS l'accumulation, à l'étape de remise à l'échelle :
    c'est là qu'il se place dans le matériel (hors du réseau de MAC), et c'est
    aussi ce qui évite d'élargir l'accumulateur.

    Retourne (sortie_float, accumulateur_entier, (sx, scale)).
    """
    Xq, sx = quantize_activations(X, bits=act_bits)
    acc = integer_mac(Xq, q)                      # exact, aucun flottant
    out = acc * (sx * np.asarray(scale).reshape(1, -1))
    if bias is not None:
        out = out + np.asarray(bias, dtype=np.float64).reshape(1, -1)
    return out, acc, (sx, scale)
