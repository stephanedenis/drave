#!/usr/bin/env python3
"""grappe_reseau.py — A7.5 : transporter la grappe sparse entre deux processus.

Le format v2 de K3RL (masque 1 bit par canal + valeurs f32 non nulles) est
mesuré localement en A7.4 (1 704 o contre 7 196 o). Ici on le **sérialise**,
on l'envoie par **TCP loopback** à un second processus, on le **relit** et on
compare : octets, fidélité, latence. Le contrôle est le flux **dense**.
"""
from __future__ import annotations

import json
import socket
import struct
import threading
import time

MAGIC = b"K3RL"
VERSION = 2


def encoder(flux: list[list[float]], dense: bool = False) -> bytes:
    """Encode un flux (n_tokens × canaux) en v2.

    `dense=False` : masque des non-nuls + valeurs (le flux sparse).
    `dense=True`  : masque plein + toutes les valeurs (le contrôle).
    """
    ntok = len(flux)
    h = len(flux[0]) if ntok else 0
    out = bytearray(MAGIC)
    out += struct.pack("<I", VERSION)
    out += struct.pack("<Q", ntok)
    out += struct.pack("<I", h)
    nbit = ntok * h
    masque = bytearray((nbit + 7) // 8)
    val = []
    for t, ligne in enumerate(flux):
        for i, v in enumerate(ligne):
            if dense or abs(v) > 1e-12:
                pos = t * h + i
                masque[pos // 8] |= 1 << (pos % 8)
                val.append(float(v))
    out += struct.pack("<I", len(val))
    out += bytes(masque)
    out += struct.pack("<%df" % len(val), *val)
    return bytes(out)


def decoder(b: bytes) -> tuple[list[list[float]], dict]:
    if b[:4] != MAGIC:
        raise ValueError("mauvais magic")
    version, ntok, h = struct.unpack_from("<IQI", b, 4)
    if version != VERSION:
        raise ValueError(f"version {version} non supportée")
    nval = struct.unpack_from("<I", b, 20)[0]
    nmask = (ntok * h + 7) // 8
    masque = b[24:24 + nmask]
    vals = struct.unpack_from("<%df" % nval, b, 24 + nmask)
    flux = [[0.0] * h for _ in range(ntok)]
    k = 0
    for t in range(ntok):
        for i in range(h):
            pos = t * h + i
            if masque[pos // 8] & (1 << (pos % 8)):
                flux[t][i] = vals[k]
                k += 1
    return flux, {"version": version, "ntok": ntok, "h": h, "nval": nval,
                  "octets": len(b)}


def _serveur(pret: threading.Event, resultat: dict, port_box: list[int]):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 0))
    s.listen(1)
    port_box.append(s.getsockname()[1])
    pret.set()
    conn, _ = s.accept()
    with conn:
        n = struct.unpack("<I", conn.recv(4))[0]
        data = b""
        while len(data) < n:
            data += conn.recv(n - len(data))
        resultat["data"] = data
        conn.sendall(b"OK")
    s.close()


def mesurer(ntok: int = 4, h: int = 448, top: int = 96, essais: int = 5) -> dict:
    # flux synthétique : 20 % de non-nuls
    flux = [[0.0] * h for _ in range(ntok)]
    for t in range(ntok):
        for i in range(0, h, 5):
            flux[t][i] = float((t + 1) * (i + 1) % 97) / 97.0
    dense = encoder(flux, dense=True)
    sparse = encoder(flux)
    # fidélité locale
    relu, meta = decoder(sparse)
    exact = sum(1 for t in range(ntok) for i in range(h)
                if abs(relu[t][i] - (flux[t][i] if abs(flux[t][i]) > 0 else 0.0)) < 1e-6)
    # réseau loopback
    lat = []
    ok = True
    for _ in range(essais):
        pret = threading.Event(); resultat = {}; port_box = []
        th = threading.Thread(target=_serveur, args=(pret, resultat, port_box), daemon=True)
        th.start(); pret.wait(2)
        port = port_box[0]
        c = socket.create_connection(("127.0.0.1", port), timeout=2)
        t0 = time.perf_counter()
        c.sendall(struct.pack("<I", len(sparse)) + sparse)
        ack = c.recv(2)
        lat.append((time.perf_counter() - t0) * 1000)
        c.close(); th.join(2)
        if ack != b"OK" or resultat.get("data") != sparse:
            ok = False
    return {
        "flux": {"ntok": ntok, "canaux": h, "top": top},
        "octets": {"dense": len(dense), "sparse": len(sparse),
                   "ratio": len(dense) / len(sparse)},
        "fidelite": {"exact": exact, "total": ntok * h,
                     "taux": exact / (ntok * h)},
        "reseau": {"essais": essais, "identiques": ok,
                   "latence_ms_moyenne": sum(lat) / len(lat),
                   "latence_ms_min": min(lat), "latence_ms_max": max(lat)},
        "meta": meta,
    }


def main() -> None:
    print(json.dumps(mesurer(), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
