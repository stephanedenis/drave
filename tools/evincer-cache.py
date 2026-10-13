#!/usr/bin/env python3
"""evincer-cache.py — rend un fichier FROID pour la mesure suivante, sans root.

Sans cette étape, le deuxième bras d'une porte lit ce que le premier a laissé dans le
cache de pages et mesure de la RAM : c'est le piège qui a donné « 300 Mo/s au hasard »
au premier essai de `tools/banc-prelire.py`.

`posix_fadvise(POSIX_FADV_DONTNEED)` demande au noyau d'oublier les pages **propres**
d'un fichier : aucun droit particulier n'est requis (contrairement à
`/proc/sys/vm/drop_caches`), et l'appel ne fait aucune E/S. On procède par tranches
parce que le noyau refuse les plages trop grandes.

usage : evincer-cache.py <fichier> [<fichier>…]
sortie : « <fichier> : <Go> évincés » (la taille adressée, pas une preuve — la preuve,
c'est le témoin de `tools/porte-prechargement.sh`)
"""
import os
import sys

TRANCHE = 1 << 30          # 1 Gio par appel


def evincer(chemin):
    taille = os.path.getsize(chemin)
    fd = os.open(chemin, os.O_RDONLY)
    try:
        off = 0
        while off < taille:
            os.posix_fadvise(fd, off, min(TRANCHE, taille - off), os.POSIX_FADV_DONTNEED)
            off += TRANCHE
    finally:
        os.close(fd)
    return taille


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    for chemin in sys.argv[1:]:
        chemin = os.path.expanduser(chemin)
        if not os.path.isfile(chemin):
            print(f"{chemin} : introuvable", file=sys.stderr)
            return 1
        octets = evincer(chemin)
        print(f"{chemin} : {octets / 1e9:.1f} Go évincés du cache de pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
