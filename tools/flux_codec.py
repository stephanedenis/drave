#!/usr/bin/env python3
"""Encodeur/décodeur de RÉFÉRENCE du flux d'activation (format DRVF v1 et v2).

Le format de trace et le contrat d'échange de la phase 3 sont le MÊME format :
une liste d'activation est ce qu'un nœud distant doit recevoir pour continuer le
calcul. Ce fichier est la deuxième implémentation de ce format — la première est
en Rust (`--trace-flux`) — et c'est ce qui permet de dire qu'il est sans
ambiguïté : deux implémentations indépendantes, un aller-retour identique.

Structure :
    en-tête   "DRVF" · u16 version · u32 n_layer · u32 hidden
    liste     u16 couche · u32 position · u32 n_actifs · f32 echelle
              puis n_actifs × ( u32 indice · i16 valeur )          [v1]
              puis n_actifs × ( u8 écart · i16 valeur )            [v2]
                   l'écart de 255 annonce l'indice ABSOLU sur u16
    fin       u16 0xFFFF

v2 : les indices sont écrits par ÉCARTS (la liste est triée). Mesuré sur une trace
réelle de 512 jetons : 132 396 736 octets en v1, **66 370 408** en v2 (−49,87 %),
à contenu identique — le rejeu redonne la même perplexité au chiffre près.

Usage :
    flux_codec.py <trace>            # vérifie l'aller-retour et mesure le débit
    flux_codec.py <trace> --jetons N # projette le coût pour N jetons
"""
import struct
import sys
import time

MAGIE = b"DRVF"
VERSION = 2        # ce que ce fichier ÉCRIT ; il LIT la 1 et la 2
ENTETE = struct.Struct("<4sHII")
LISTE = struct.Struct("<HIIf")
PAIRE_V1 = struct.Struct("<Ih")
PAIRE_V2 = struct.Struct("<Bh")
FIN = struct.Struct("<H")


def encoder(n_layer, hidden, listes, version=VERSION):
    """listes : itérable de (couche, position, echelle, [(indice, valeur)])."""
    out = bytearray(ENTETE.pack(MAGIE, version, n_layer, hidden))
    for couche, pos, echelle, actifs in listes:
        out += LISTE.pack(couche, pos, len(actifs), echelle)
        prev = 0
        for i, v in actifs:
            if version == 1:
                out += PAIRE_V1.pack(i, v)
            else:
                ecart = i - prev
                if ecart < 255:
                    out += PAIRE_V2.pack(ecart, v)
                else:
                    out += bytes([255]) + struct.pack("<H", i) + struct.pack("<h", v)
                prev = i
    out += FIN.pack(0xFFFF)
    return bytes(out)


def decoder(blob):
    magie, version, n_layer, hidden = ENTETE.unpack_from(blob, 0)
    assert magie == MAGIE, "magie absente"
    assert version in (1, 2), f"version {version} inconnue (ce lecteur lit la 1 et la 2)"
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
        prev = 0
        for _ in range(n):
            if version == 1:
                i, v = PAIRE_V1.unpack_from(blob, off)
                off += PAIRE_V1.size
            else:
                d = blob[off]
                off += 1
                if d == 255:
                    i = struct.unpack_from("<H", blob, off)[0]
                    off += 2
                else:
                    i = prev + d
                prev = i
                v = struct.unpack_from("<h", blob, off)[0]
                off += 2
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
