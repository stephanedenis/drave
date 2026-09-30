#!/usr/bin/env python3
"""Encodeur/décodeur de RÉFÉRENCE du flux d'activation (format DRVF v1).

Le format de trace et le contrat d'échange de la phase 3 sont le MÊME format :
une liste d'activation est ce qu'un nœud distant doit recevoir pour continuer le
calcul. Ce fichier est la deuxième implémentation de ce format — la première est
en Rust (`--trace-flux`) — et c'est ce qui permet de dire qu'il est sans
ambiguïté : deux implémentations indépendantes, un aller-retour identique.

Structure :
    en-tête   "DRVF" · u16 version · u32 n_layer · u32 hidden
    liste     u16 couche · u32 position · u32 n_actifs · f32 echelle
              puis n_actifs × ( u32 indice · i16 valeur )
    fin       u16 0xFFFF

Usage :
    flux_codec.py <trace>            # vérifie l'aller-retour et mesure le débit
    flux_codec.py <trace> --jetons N # projette le coût pour N jetons
"""
import struct
import sys
import time

MAGIE = b"DRVF"
VERSION = 1
ENTETE = struct.Struct("<4sHII")
LISTE = struct.Struct("<HIIf")
PAIRE = struct.Struct("<Ih")
FIN = struct.Struct("<H")


def encoder(n_layer, hidden, listes):
    """listes : itérable de (couche, position, echelle, [(indice, valeur)])."""
    out = bytearray(ENTETE.pack(MAGIE, VERSION, n_layer, hidden))
    for couche, pos, echelle, actifs in listes:
        out += LISTE.pack(couche, pos, len(actifs), echelle)
        for i, v in actifs:
            out += PAIRE.pack(i, v)
    out += FIN.pack(0xFFFF)
    return bytes(out)


def decoder(blob):
    magie, version, n_layer, hidden = ENTETE.unpack_from(blob, 0)
    assert magie == MAGIE, "magie absente"
    assert version == VERSION, f"version {version} inconnue"
    off = ENTETE.size
    listes = []
    while True:
        if off + FIN.size > len(blob):
            break                      # fin de fichier : la sentinelle est optionnelle
        couche, = FIN.unpack_from(blob, off)
        if couche == 0xFFFF:
            break
        couche, pos, n, echelle = LISTE.unpack_from(blob, off)
        off += LISTE.size
        actifs = []
        for _ in range(n):
            i, v = PAIRE.unpack_from(blob, off)
            off += PAIRE.size
            actifs.append((i, v))
        listes.append((couche, pos, echelle, actifs))
    return n_layer, hidden, listes


def lire_rust(chemin):
    """Lit le fichier écrit par le moteur, sans le ré-encoder."""
    with open(chemin, "rb") as f:
        blob = f.read()
    n_layer, hidden, listes = decoder(blob)
    return n_layer, hidden, listes, blob


def main():
    chemin = sys.argv[1]
    n_layer, hidden, listes, blob = lire_rust(chemin)
    n_actifs = sum(len(a) for _, _, _, a in listes)
    jetons = len({p for _, p, _, _ in listes})
    print(f"{chemin}")
    print(f"  {len(listes)} listes · {jetons} jetons · {n_layer} couches · {hidden} cachés")
    print(f"  {len(blob)} octets · {len(blob)/max(1,jetons)/1024:.1f} ko par jeton "
          f"· {len(blob)/max(1,n_actifs):.2f} octet par neurone actif")

    t0 = time.time()
    blob2 = encoder(n_layer, hidden, listes)
    t_enc = time.time() - t0
    t0 = time.time()
    n2, h2, listes2 = decoder(blob2)
    t_dec = time.time() - t0
    identique = (blob2 == blob) and (listes2 == listes)
    print(f"  aller-retour : {'IDENTIQUE' if identique else 'DIFFÉRENT'} "
          f"({len(blob2)} octets réencodés)")
    mb = len(blob) / 1e6
    print(f"  débit : encodage {mb/t_enc:.0f} Mo/s · décodage {mb/t_dec:.0f} Mo/s")
    if not identique:
        return 1

    if "--jetons" in sys.argv:
        n = int(sys.argv[sys.argv.index("--jetons") + 1])
        par_jeton = len(blob) / max(1, jetons)
        total = par_jeton * n
        print(f"  projection : {n} jetons -> {total/1e9:.2f} Go "
              f"({total/1e6:.0f} Mo), soit {total/1e6:.0f} Mo à faire passer sur le réseau")
        for debit in (100, 1000, 10000):
            print(f"    à {debit} Mo/s : {total/1e6/debit:.2f} s par passe complète")
    return 0


if __name__ == "__main__":
    sys.exit(main())
