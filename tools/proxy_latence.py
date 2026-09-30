#!/usr/bin/env python3
"""Relais TCP qui ajoute une latence par message, pour mesurer ce qu'un lien
distant coûte à un découpage de modèle.

Pourquoi : sur localhost, l'attente du pair vaut 1,01× le calcul local — c'est un
plancher optimiste. Une VM Colab est à quelques dizaines de millisecondes, et la
phase 3.3 demande « à partir de quel débit le découpage gagne ». Le débit n'est
jamais le problème (0,25 Mbit/s) ; la latence, si. Ce relais la rend réglable.

    python3 tools/proxy_latence.py <port_écoute> <hôte_cible:port> [délai_ms]
"""
import socket, sys, threading, time


def relais(src, dst, delai):
    try:
        while True:
            donnees = src.recv(65536)
            if not donnees:
                break
            if delai:
                time.sleep(delai)
            dst.sendall(donnees)
    except OSError:
        pass
    finally:
        for s in (src, dst):
            try:
                s.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass


def main():
    port = int(sys.argv[1])
    hote, port_cible = sys.argv[2].rsplit(":", 1)
    delai = float(sys.argv[3]) / 1000.0 if len(sys.argv) > 3 else 0.0
    ecoute = socket.socket()
    ecoute.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ecoute.bind(("127.0.0.1", port))
    ecoute.listen(4)
    print(f"[relais] 127.0.0.1:{port} → {hote}:{port_cible} · +{delai*1000:.0f} ms par message",
          flush=True)
    while True:
        client, _ = ecoute.accept()
        amont = socket.create_connection((hote, int(port_cible)))
        for s in (client, amont):
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        threading.Thread(target=relais, args=(client, amont, delai), daemon=True).start()
        threading.Thread(target=relais, args=(amont, client, delai), daemon=True).start()


if __name__ == "__main__":
    main()
