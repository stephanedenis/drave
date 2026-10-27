#!/usr/bin/env python3
"""seuil_reseau.py — A7.5b : quand le flux sparse gagne-t-il sur le réseau ?

A7.5 mesure le volume et la latence loopback. Ici on modélise un lien :
temps = encodage + octets × 8 / débit + latence + décodage.
Le sparse paie moins d'octets, mais un décodage plus coûteux ; on cherche le
seuil de latence où il bat le dense. Le modèle est explicite, pas un `sleep`.
"""
from __future__ import annotations

import json
import time

from tools.grappe_reseau import decoder, encoder


def _flux(ntok: int = 4, h: int = 448, pas: int = 5):
    return [[float((t + 1) * (i + 1) % 97) / 97.0 if i % pas == 0 else 0.0
             for i in range(h)] for t in range(ntok)]


def _temps(fn, *args, n: int = 20):
    t0 = time.perf_counter()
    for _ in range(n):
        fn(*args)
    return (time.perf_counter() - t0) / n


def mesurer(ntok: int = 4, h: int = 448, debit_mbps: float = 1000.0,
            latences_ms=(0, 5, 20, 50, 100)) -> dict:
    flux = _flux(ntok, h)
    dense = encoder(flux, dense=True)
    sparse = encoder(flux)
    enc_d = _temps(encoder, flux, True)
    enc_s = _temps(encoder, flux, False)
    dec_d = _temps(decoder, dense)
    dec_s = _temps(decoder, sparse)
    debit = debit_mbps * 1e6 / 8.0  # octets/s
    lignes = []
    for lat in latences_ms:
        td = enc_d + len(dense) / debit + dec_d + lat / 1000.0
        ts = enc_s + len(sparse) / debit + dec_s + lat / 1000.0
        lignes.append({"latence_ms": lat, "dense_ms": td * 1000,
                       "sparse_ms": ts * 1000, "gain": td / ts})
    # seuil : latence où sparse = dense (les termes CPU et débit se compensent)
    cpu_d = enc_d + dec_d
    cpu_s = enc_s + dec_s
    seuil = ((cpu_s - cpu_d) + (len(sparse) - len(dense)) / debit) * 1000
    return {
        "flux": {"ntok": ntok, "canaux": h, "non_nuls": sum(1 for l in flux for v in l if v)},
        "octets": {"dense": len(dense), "sparse": len(sparse),
                   "ratio": len(dense) / len(sparse)},
        "temps_local": {"enc_dense_ms": enc_d * 1000,
                        "enc_sparse_ms": enc_s * 1000,
                        "dec_dense_ms": dec_d * 1000,
                        "dec_sparse_ms": dec_s * 1000},
        "lien": {"debit_mbps": debit_mbps},
        "latences": lignes,
        "seuil_latence_ms": seuil,
        "lecture": ("sparse gagne si la latence dépasse le seuil"
                    if seuil > 0 else "sparse gagne même à latence nulle"),
    }


def main() -> None:
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
