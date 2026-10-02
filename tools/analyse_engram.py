#!/usr/bin/env python3
"""Analyse du **flux d'adresses** de l'engram (DeepSeek-V4.1).

Lit ce que `drave <modele> --engram-adresses F` a écrit — un `i32` par jeton,
par couche et par colonne de hachage — et dit ce que ce flux **est** :

* combien de rangées il touche, et quelle part de la table ;
* comment il se répartit entre les deux couches et les 24 colonnes ;
* à quelle distance les rangées successives tombent (la localité) ;
* ce qui se répète : entre jetons voisins, et sur toute la séquence.

C'est la porte Drave de la phase P8 : un flux qui n'est pas lisible par un outil
n'est pas un flux, c'est un tampon.

Usage :
    python3 tools/analyse_engram.py <adresses.bin> [--jetons N] [--couches 1,14]
                                    [--colonnes 24] [--rangees R]
"""
import argparse
import collections
import struct
import sys


def lire(chemin):
    with open(chemin, "rb") as f:
        b = f.read()
    return list(struct.unpack(f"<{len(b) // 4}i", b))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fichier")
    ap.add_argument("--jetons", type=int, default=10000)
    ap.add_argument("--couches", default="1,14")
    ap.add_argument("--colonnes", type=int, default=24)
    ap.add_argument("--rangees", type=int, default=768_022_850,
                    help="total des rangées des tables (somme de `engram.rows`)")
    a = ap.parse_args()

    adr = lire(a.fichier)
    couches = [int(x) for x in a.couches.split(",")]
    nl, nhc = len(couches), a.colonnes
    par_jeton = nl * nhc
    if len(adr) % par_jeton:
        raise SystemExit(f"{len(adr)} adresses n'est pas un multiple de {par_jeton} "
                         f"({nl} couches × {nhc} colonnes)")
    jetons = len(adr) // par_jeton
    print(f"# {a.fichier}")
    print(f"{jetons} jetons × {nl} couches × {nhc} colonnes = {len(adr)} adresses")

    distinctes = len(set(adr))
    print(f"rangées distinctes      : {distinctes} ({100 * distinctes / len(adr):.1f} % "
          f"des adresses, {100 * distinctes / a.rangees:.4f} % de la table)")

    # Répartition par couche et par colonne : un hachage sain ne privilégie rien.
    par_couche = collections.Counter()
    par_colonne = collections.Counter()
    for j in range(jetons):
        base = j * par_jeton
        for i in range(nl):
            for c in range(nhc):
                par_couche[couches[i]] += 1
                par_colonne[(i, c)] += 1
    print("par couche              : " + " · ".join(
        f"{k} → {v}" for k, v in sorted(par_couche.items())))

    # Localté : de combien les rangées successives s'écartent-elles ? Un hachage
    # qui « dérive » lentement toucherait des rangées voisines — donc les mêmes
    # pages, et le coût de lecture ne serait pas celui d'un accès dispersé.
    ecarts = []
    for j in range(1, jetons):
        for i in range(nl * nhc):
            ecarts.append(abs(adr[j * par_jeton + i] - adr[(j - 1) * par_jeton + i]))
    ecarts.sort()
    n = len(ecarts)
    print(f"écart entre jetons      : médiane {ecarts[n // 2]:,} · p95 "
          f"{ecarts[int(n * 0.95)]:,} · max {ecarts[-1]:,}")

    # Répétition : ce qui revient. Entre jetons VOISINS (colonne identique) et
    # sur toute la séquence. Le second dit combien de fois une rangée est réutilisée
    # — donc combien de la table sert vraiment.
    voisins = 0
    for j in range(1, jetons):
        for i in range(nl * nhc):
            if adr[j * par_jeton + i] == adr[(j - 1) * par_jeton + i]:
                voisins += 1
    comptes = collections.Counter(adr)
    reutilisees = sum(1 for v in comptes.values() if v > 1)
    print(f"identiques au jeton précédent : {voisins} ({100 * voisins / len(adr):.2f} %)")
    print(f"rangées touchées plus d'une fois : {reutilisees} "
          f"({100 * reutilisees / distinctes:.2f} % des distinctes) · "
          f"la plus fréquente : {comptes.most_common(1)[0][1]} fois")

    # Couverture : combien de la table est atteinte, et où. Une table de 101 Go
    # dont 0,06 % des rangées servent n'est pas lue au hasard : elle est
    # PARCOURUE, ce qui décide du préchargement possible.
    mini, maxi = min(adr), max(adr)
    print(f"étendue adressée        : {mini:,} … {maxi:,} "
          f"({100 * (maxi - mini) / a.rangees:.4f} % de la table)")
    print("\nCe que ce flux coûte à lire : 264 octets par rangée distincte, soit "
          f"{distinctes * 264 / 1e6:.1f} Mo pour ces {jetons} jetons "
          f"({distinctes * 264 / max(jetons, 1):.0f} octets par jeton)")


if __name__ == "__main__":
    sys.exit(main())
