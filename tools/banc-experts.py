#!/usr/bin/env python3
"""banc-experts.py — quel mécanisme de lecture tient la bande passante de l'array ?

`tools/banc-prelire.py` a montré qu'une grappe de 1 Mio préchargée par `madvise` rend
**1 230 Mo/s** là où des défauts de page au hasard rendent 29 Mo/s. Mais la passe réelle
du moteur, elle, ne rend que **~130 Mo/s** (`tools/porte-prechargement.sh`, bras
`actuel`) : le moteur touche les pages d'un expert **dans l'ordre du calcul**, pas dans
l'ordre du fichier, et chaque défaut qui tombe hors de la fenêtre déjà lue paie une
lecture synchrone.

Ce banc reproduit ce motif — des **plages d'expert** (4 Mio) dispersées, parcourues page
par page **dans un ordre tiré au hasard** — et compare quatre mécanismes :

  1. `demande`        : on touche, le noyau se débrouille (le régime du manque) ;
  2. `madvise-plage`  : `madvise(WILLNEED)` sur la plage entière, puis on touche ;
  3. `madvise-tranches`: `madvise` par tranches de 1 Mio alignées, puis on touche ;
  4. `pread-fils`     : on lit les plages avec `pread` depuis N fils (ce que le moteur
                        ne fait pas — il mmap — mais qui dit si le parallélisme explicite
                        est la réponse, ce que le § 6.5.1 du doc de configuration suppose).

Précautions identiques à `banc-prelire.py` : zones distinctes par bras et par répétition,
contrôle à froid hors zone, trois répétitions entrelacées, médiane.

usage : banc-experts.py [fichier] [--plages E] [--taille Mio] [--fils N]
"""
import mmap
import os
import random
import statistics
import sys
import threading
import time

PAGE = 4096
MIO = 1 << 20
GIO = 1 << 30


def mo_par_s(octets, secondes):
    return octets / secondes / 1e6


def melange_pages(base, octets, rng):
    """L'ordre dans lequel le calcul touche les pages d'une plage (tiré au hasard)."""
    pages = list(range(base, base + octets, PAGE))
    rng.shuffle(pages)
    return pages


def bras_demande(mm, plages, rng):
    t0 = time.perf_counter()
    n = 0
    for base, octets in plages:
        for p in melange_pages(base, octets, rng):
            mm[p]
            n += 1
    return mo_par_s(n * PAGE, time.perf_counter() - t0)


def bras_madvise_plage(mm, plages, rng):
    t0 = time.perf_counter()
    n = 0
    for base, octets in plages:
        mm.madvise(mmap.MADV_WILLNEED, base, octets)
        for p in melange_pages(base, octets, rng):
            mm[p]
            n += 1
    return mo_par_s(n * PAGE, time.perf_counter() - t0)


def bras_madvise_tranches(mm, plages, rng):
    t0 = time.perf_counter()
    n = 0
    for base, octets in plages:
        for t in range(0, octets, MIO):
            mm.madvise(mmap.MADV_WILLNEED, base + t, min(MIO, octets - t))
        for p in melange_pages(base, octets, rng):
            mm[p]
            n += 1
    return mo_par_s(n * PAGE, time.perf_counter() - t0)


def bras_pread_fils(fichier, plages, fils):
    """Lecture explicite en parallèle, dans un tampon par fil (pas de mmap)."""
    taches = [(i, plage) for i, plage in enumerate(plages)]
    verrou = threading.Lock()
    lu = [0]
    tampons = {}

    def travail(part):
        fd = os.open(fichier, os.O_RDONLY)
        buf = bytearray(1 << 20)
        local = 0
        try:
            for _, (base, octets) in part:
                off = 0
                while off < octets:
                    n = os.preadv(fd, [memoryview(buf)[:min(1 << 20, octets - off)]], base + off)
                    off += n
                    local += n
        finally:
            os.close(fd)
        with verrou:
            lu[0] += local

    t0 = time.perf_counter()
    fils_ = [threading.Thread(target=travail, args=(taches[i::fils],)) for i in range(fils)]
    for f in fils_:
        f.start()
    for f in fils_:
        f.join()
    dt = time.perf_counter() - t0
    tampons.clear()
    return mo_par_s(lu[0], dt)


def main():
    args = sys.argv[1:]
    fichier = "/home/stephane/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf"
    if args and not args[0].startswith("-"):
        fichier = args.pop(0)
    plages_n, taille_mio, fils = 24, 4, 8
    if "--plages" in args:
        plages_n = int(args[args.index("--plages") + 1])
    if "--taille" in args:
        taille_mio = int(args[args.index("--taille") + 1])
    if "--fils" in args:
        fils = int(args[args.index("--fils") + 1])
    fichier = os.path.expanduser(fichier)

    taille = os.path.getsize(fichier)
    octets_plage = taille_mio * MIO
    besoin = plages_n * octets_plage
    bras = ("demande", "madvise-plage", "madvise-tranches", "pread-fils")
    # L'espacement s'adapte au fichier : il faut 3 zones disjointes par bras, plus la marge
    # du contrôle à froid (8 Mio), et chaque zone doit rester bien plus grande que ce qu'un
    # bras y lit — sinon deux bras partagent des pages et le second lit du cache.
    ecart = min(2 * GIO, max(256 * MIO, (taille - 2 * besoin) // (len(bras) * 3)))
    if taille < len(bras) * 3 * ecart + besoin:
        print(f"fichier trop petit : {taille / 1e9:.1f} Go — réduire --plages ou --taille")
        return 1

    rng = random.Random(20261012)
    print(f"fichier : {os.path.basename(fichier)} ({taille / 1e9:.1f} Go)")
    print(f"  {plages_n} plages de {taille_mio} Mio ({besoin / 1e6:.0f} Mo utiles par bras), "
          f"pages parcourues dans un ordre tiré au hasard · {fils} fils pour `pread-fils` · "
          f"3 zones de {ecart / GIO:.0f} Gio par bras")
    resultats = {b: [] for b in bras}
    with open(fichier, "rb") as f:
        fd_evince = os.open(fichier, os.O_RDONLY)
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            for r in range(3):
                for i, b in enumerate(bras):
                    base_zone = (i * 3 + r) * ecart + 64 * MIO
                    base_zone -= base_zone % PAGE
                    plages = [(base_zone + j * octets_plage, octets_plage)
                              for j in range(plages_n)]
                    # LA ZONE EST ÉVINCÉE AVANT D'ÊTRE MESURÉE, par `posix_fadvise` sur un
                    # descripteur (c'est ce qui marche : `madvise(DONTNEED)` sur le mapping
                    # laissait les pages en place — premier essai, témoin à 13 µs et
                    # « demande » à 5 181 Mo/s, c'est-à-dire de la RAM).
                    os.posix_fadvise(fd_evince, base_zone, besoin, os.POSIX_FADV_DONTNEED)
                    # contrôle à froid, DANS la zone (dernière page) : une page sur 25 600,
                    # le bras ne s'en trouve pas réchauffé
                    t0 = time.perf_counter()
                    mm[base_zone + besoin - PAGE]
                    froid = (time.perf_counter() - t0) * 1e6
                    if b == "demande":
                        v = bras_demande(mm, plages, rng)
                    elif b == "madvise-plage":
                        v = bras_madvise_plage(mm, plages, rng)
                    elif b == "madvise-tranches":
                        v = bras_madvise_tranches(mm, plages, rng)
                    else:
                        v = bras_pread_fils(fichier, plages, fils)
                    resultats[b].append(v)
                    print(f"  {b:17} rép {r + 1} : {v:9.2f} Mo/s utiles "
                          f"(témoin à froid : {froid:9.1f} µs)")
        finally:
            mm.close()
            os.close(fd_evince)
    print(f"{'bras':18} {'médiane':>11}   les trois répétitions")
    for b in bras:
        v = resultats[b]
        print(f"{b:18} {statistics.median(v):8.2f} Mo/s   " + " ".join(f"{x:.2f}" for x in v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
