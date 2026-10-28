#!/usr/bin/env python3
"""kv_reseau.py — A7.9 : le coût réseau du cache KV.

A7.6 exécute une couche à distance mais ne transfère pas le cache KV (prefill).
Ici on mesure le **cache** seul : pour la couche 12 de Qwen 0.5B, 2 têtes KV,
head_dim 64, f32 = 1 024 o par jeton et par couche ; on le transporte par TCP
loopback et on compare au hidden de A7.6.
"""
from __future__ import annotations

import json
import socket
import struct
import threading
import time

import numpy as np

MAGIC = b"K4KV"
VERSION = 1


def encoder_kv(kv: np.ndarray) -> bytes:
    a = np.ascontiguousarray(kv.astype(np.float32))
    return MAGIC + struct.pack("<II", VERSION, a.size) + a.tobytes()


def decoder_kv(b: bytes) -> np.ndarray:
    if b[:4] != MAGIC:
        raise ValueError("mauvais magic")
    version, n = struct.unpack_from("<II", b, 4)
    if version != VERSION:
        raise ValueError(f"version {version}")
    arr = np.frombuffer(b[12:], dtype="<f4", count=n).copy()
    return arr.reshape(2, n // (2 * 2 * 64), 2, 64)


def _serveur(pret, sortie, port_box):
    s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 0)); s.listen(1); port_box.append(s.getsockname()[1]); pret.set()
    conn, _ = s.accept()
    with conn:
        n = struct.unpack("<I", conn.recv(4))[0]
        data = b""
        while len(data) < n:
            data += conn.recv(n - len(data))
        sortie["data"] = data
        conn.sendall(b"OK")
    s.close()


def _kv(ntok: int, n_kv_heads: int = 2, head_dim: int = 64) -> np.ndarray:
    rng = np.random.default_rng(0)
    return rng.standard_normal((2, ntok, n_kv_heads, head_dim)).astype(np.float32)


def mesurer(ntok: int = 64, n_kv_heads: int = 2, head_dim: int = 64,
            essais: int = 5) -> dict:
    kv = _kv(ntok, n_kv_heads, head_dim)
    payload = encoder_kv(kv)
    relu = decoder_kv(payload)
    exact = bool(np.array_equal(kv, relu))
    octets = len(payload)
    lat = []
    ok = True
    for _ in range(essais):
        pret = threading.Event(); sortie = {}; port_box = []
        th = threading.Thread(target=_serveur, args=(pret, sortie, port_box), daemon=True)
        th.start(); pret.wait(2)
        c = socket.create_connection(("127.0.0.1", port_box[0]), timeout=2)
        t0 = time.perf_counter()
        c.sendall(struct.pack("<I", len(payload)) + payload)
        ack = c.recv(2)
        lat.append((time.perf_counter() - t0) * 1000)
        c.close(); th.join(2)
        ok = ok and ack == b"OK" and sortie.get("data") == payload
    return {
        "couche": 12, "ntok": ntok, "n_kv_heads": n_kv_heads, "head_dim": head_dim,
        "octets_kv": octets, "octets_par_jeton": octets / ntok,
        "fidelite": exact, "messages_identiques": ok,
        "latence_ms_moyenne": sum(lat) / len(lat),
        "latence_ms_min": min(lat), "latence_ms_max": max(lat),
        "comparaison_hidden_a76": {"octets_par_jeton": 4105, "ratio_kv_hidden": (octets / ntok) / 4105},
        "projection_24_couches": {"octets_par_jeton": 24 * octets / ntok,
                                   "mio_pour_4096_jetons": 24 * octets / ntok * 4096 / 2**20},
    }


def main() -> None:
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
