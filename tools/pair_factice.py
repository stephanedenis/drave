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
TETE = 79   # en-tête v4 : magie, version, mode, plage, position, n, échelle,
            # niveaux, seuil, top-k, renorm, 7 top-k par projection, 3 top-k globaux
MODES = {0: "dense f32", 1: "listes quantifiées", 2: "blocs (i8 + écarts)",
         3: "lot (t états × dimension)"}


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
    while True:                      # un client après l'autre : un banc se relance
        sock, pair = ecoute.accept()
        print(f"[factice] client {pair}", flush=True)
        vus = []
        servir(sock, dimension)
        if vus:
            print(f"[factice] {len(vus)} flux · n min {min(vus)} max {max(vus)} "
                  f"moyen {sum(vus)/len(vus):.1f}", flush=True)


def servir(sock, dimension):
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
        # Le corps dépend du MODE : dense et listes i16 font 4 octets par
        # élément, les blocs font 2 octets par actif plus les échelles et les
        # échappements. Un pair factice qui suppose une seule disposition mentirait
        # exactement là où on l'interroge.
        if mode == 3:
            # LOT : `n` est le nombre d'ÉTATS, le corps fait n × dimension × 4.
            # Lire n × 4 (comme avant) laissait le client BLOQUÉ dans read_exact
            # et tuait le pair — c'est pour cela que le mode lot n'avait jamais
            # été confronté à un pair indépendant (relecture adversariale, D4).
            corps = lire_tout(sock, n * dimension * 4)
        elif mode == 2:
            nb = struct.unpack("<I", lire_tout(sock, 4))[0]
            echelles = lire_tout(sock, nb * 4)
            longueur = struct.unpack("<I", lire_tout(sock, 4))[0]
            corps = echelles + lire_tout(sock, longueur)
        else:
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
        # Réponse : en mode dense, `n` est la DIMENSION et le corps fait 4 octets
        # par canal ; dans les modes « listes », `n` est le nombre de paires et il
        # n'y en a aucune (le pair factice ne calcule rien). Annoncer la dimension
        # dans un mode liste ferait lire au pilote un corps tronqué — c'est
        # exactement l'erreur que ce fichier a commise, et le moteur l'a dite.
        n_paires = dimension if mode == 0 else 0
        reponse = struct.pack("<IBBIIIIfffIBIIIIIIIIII", MAGIE, version, mode, debut, fin, pos,
                              n if mode == 3 else n_paires, 0.0, levels, thresh, topk, renorm,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        if mode == 3:
            # réponse : le MÊME nombre d'états, valeurs nulles (le pair factice
            # ne calcule rien) — annoncer n états et n'envoyer qu'un vecteur
            # faisait lire au client un corps tronqué.
            reponse += b"\0" * (n * dimension * 4)
        elif mode == 2:
            # réponse : aucune valeur active (n=0), une échelle par bloc
            nb = (dimension + 31) // 32
            reponse += struct.pack("<I", nb) + struct.pack("<f", 0.0) * nb + struct.pack("<I", 0)
        else:
            reponse += b"\0" * (dimension * 4)
        sock.sendall(reponse)
    return vus


if __name__ == "__main__":
    main()
