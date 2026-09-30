#!/usr/bin/env python3
"""Pair factice du protocole de flux (v2) : il ÉCOUTE et DIT ce qu'il reçoit.

Pourquoi cet outil : un banc à deux nœuds qui « marche » peut cacher un
protocole faux — c'est exactement ce qui est arrivé avec un flux de 919 canaux
là où le modèle en a 896. Un pair qui parle le protocole sans calculer le modèle
rend visible ce que l'autre bout envoie vraiment : tailles, positions, modes,
réglages. Il répond un flux de la dimension demandée pour que le pilote continue.

    python3 tools/pair_factice.py <port> [dimension]
"""
import socket, struct, sys

MAGIE = 0x44525631
TETE = 39
MODES = {0: "dense f32", 1: "listes quantifiées"}


def lire_tout(sock, n):
    buf = b""
    while len(buf) < n:
        morceau = sock.recv(n - len(buf))
        if not morceau:
            raise EOFError("pair fermé")
        buf += morceau
    return buf


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 45760
    dimension = int(sys.argv[2]) if len(sys.argv) > 2 else 896
    ecoute = socket.socket()
    ecoute.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ecoute.bind(("127.0.0.1", port))
    ecoute.listen(1)
    print(f"[factice] écoute sur 127.0.0.1:{port} · je réponds {dimension} canaux", flush=True)
    sock, pair = ecoute.accept()
    print(f"[factice] client {pair}", flush=True)
    vus = []
    while True:
        try:
            tete = lire_tout(sock, TETE)
        except EOFError:
            break
        magie, version, mode = struct.unpack("<IBB", tete[:6])
        debut, fin, pos, n = struct.unpack("<IIII", tete[6:22])
        echelle, levels, thresh = struct.unpack("<fff", tete[22:34])
        topk, renorm = struct.unpack("<IB", tete[34:39])
        corps = lire_tout(sock, n * 4)
        if magie != MAGIE:
            print(f"[factice] MAGIE INCONNUE {magie:#x}", flush=True)
            break
        vus.append(n)
        if len(vus) <= 3 or len(vus) % 20 == 0:
            print(f"[factice] flux {len(vus)} : couches {debut}..{fin} pos {pos} · "
                  f"version {version} · mode {MODES.get(mode, mode)} · n={n} · "
                  f"échelle {echelle:g} · niveaux {levels:g} seuil {thresh:g} "
                  f"topk {topk} renorm {renorm} · corps {len(corps)} octets", flush=True)
        # réponse : un flux de la dimension attendue, valeurs nulles
        reponse = struct.pack("<IBBIIIIfffIB", MAGIE, version, mode, debut, fin, pos,
                              dimension, 0.0, levels, thresh, topk, renorm)
        reponse += b"\0" * (dimension * 4 if mode == 0 else 4 * dimension)
        sock.sendall(reponse)
    if vus:
        print(f"[factice] {len(vus)} flux · n min {min(vus)} max {max(vus)} "
              f"moyen {sum(vus)/len(vus):.1f}", flush=True)


if __name__ == "__main__":
    main()
