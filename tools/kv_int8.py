#!/usr/bin/env python3
"""kv_int8.py — A7.10 : cache KV quantifié par canal.

A7.9 : 1 024 o/jeton/couche, 24 580 o/jeton sur 24 couches, 96 Mio pour 4 096.
Ici on quantifie le KV en int8 avec une échelle **par canal** (256 canaux
KV = 2 têtes × 2 × 64), partagée entre les jetons.
"""
from __future__ import annotations

import json

import numpy as np

from tools.kv_reseau import _kv

MAGIC = b"K4Q8"
VERSION = 1


def encoder(kv: np.ndarray) -> bytes:
    a = np.ascontiguousarray(kv.astype(np.float32))
    # canaux : (2, ntok, 2, 64) ; l'échelle est par (2, 1, 2, 64)
    maximum = np.max(np.abs(a), axis=1, keepdims=True)
    echelles = np.where(maximum > 0, maximum / 127.0, 1.0).astype(np.float32)
    q = np.clip(np.round(a / echelles), -127, 127).astype(np.int8)
    return MAGIC + VERSION.to_bytes(4, "little") + a.shape[1].to_bytes(4, "little") + echelles.tobytes() + q.tobytes()


def decoder(b: bytes) -> np.ndarray:
    if b[:4] != MAGIC:
        raise ValueError("mauvais magic")
    ntok = int.from_bytes(b[8:12], "little")
    nscale = 2 * 2 * 64
    echelles = np.frombuffer(b[12:12 + 4 * nscale], dtype="<f4").reshape(2, 1, 2, 64)
    q = np.frombuffer(b[12 + 4 * nscale:], dtype=np.int8, count=2 * ntok * 2 * 64).reshape(2, ntok, 2, 64)
    return q.astype(np.float32) * echelles


def mesurer(ntok: int = 64) -> dict:
    kv = _kv(ntok)
    b = encoder(kv)
    relu = decoder(b)
    diff = np.abs(kv - relu)
    return {
        "ntok": ntok,
        "octets_f32": int(kv.size * 4 + 12),
        "octets_int8": len(b),
        "ratio": (len(b)) / (kv.size * 4 + 12),
        "fidelite_exacte": bool(np.array_equal(kv, relu)),
        "diff_max": float(diff.max()),
        "diff_moyenne": float(diff.mean()),
        "par_jeton_int8": len(b) / ntok,
        "projection_24_couches_4096_mio": (len(b) / ntok) * 24 * 4096 / 2**20,
    }


def main() -> None:
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
