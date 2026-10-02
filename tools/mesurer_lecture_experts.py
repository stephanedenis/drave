#!/usr/bin/env python3
"""Lectures d'experts : série contre parallèle, sur un VRAI fichier froid.

    tools/mesurer_lecture_experts.py <shard.gguf> [nb_blocs] [nb_fils]

Pourquoi : le chargeur d'experts lit aujourd'hui les blocs un par un, en
s'appuyant sur le défaut de page du mmap. Le disque de cette machine a été
mesuré à **5,37 Go/s avec un lecteur et 31 Go/s avec seize** — donc si le défaut
de page sérialise, il y a un facteur 5 à prendre. Mais « il y a un facteur à
prendre » n'est pas une mesure, et le cache de pages a déjà fait mentir quatre
mécanismes de prélecture sur des modèles qui tenaient en RAM.

Ici on force le froid avec `posix_fadvise(DONTNEED)` sur les plages visées, et on
compare deux passes sur des blocs DIFFÉRENTS de même taille (comparaison
appariée) : une en touchant les pages une par une, l'autre en répartissant les
blocs entre `nb_fils` fils.
"""
import mmap
import os
import sys
import threading
import time

PAGE = 4096


def toucher(mm, base, octets):
    """Force la lecture des pages d'une plage (défaut de page, un par page)."""
    total = 0
    for off in range(base, base + octets, PAGE):
        total += mm[off]
    return total


def main():
    chemin = sys.argv[1]
    nb_blocs = int(sys.argv[2]) if len(sys.argv) > 2 else 240
    nb_fils = int(sys.argv[3]) if len(sys.argv) > 3 else 16
    taille_bloc = 4 << 20                      # 4 Mo, l'ordre d'un expert
    f = open(chemin, 'rb')
    taille = os.fstat(f.fileno()).st_size
    mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
    # Deux zones distinctes, de même taille, dans la partie « experts » du
    # fichier : les deux passes lisent donc des octets différents.
    debut = taille // 2
    zone_a = debut
    zone_b = debut + nb_blocs * taille_bloc
    assert zone_b + nb_blocs * taille_bloc < taille, "fichier trop court"

    def passe(base, fils):
        os.posix_fadvise(f.fileno(), base, nb_blocs * taille_bloc,
                         os.POSIX_FADV_DONTNEED)
        t0 = time.perf_counter()
        if fils <= 1:
            for i in range(nb_blocs):
                toucher(mm, base + i * taille_bloc, taille_bloc)
        else:
            def ouvrier(i0):
                for i in range(i0, nb_blocs, fils):
                    toucher(mm, base + i * taille_bloc, taille_bloc)
            th = [threading.Thread(target=ouvrier, args=(k,)) for k in range(fils)]
            for t in th:
                t.start()
            for t in th:
                t.join()
        dt = time.perf_counter() - t0
        octets = nb_blocs * taille_bloc
        return octets / dt / 1e9, dt

    go_s_1, dt1 = passe(zone_a, 1)
    go_s_n, dtn = passe(zone_b, nb_fils)
    print(f"{nb_blocs} blocs de {taille_bloc >> 20} Mo")
    print(f"  série      (1 lecteur) : {go_s_1:6.2f} Go/s en {dt1:6.2f} s")
    print(f"  parallèle ({nb_fils:2} fils)   : {go_s_n:6.2f} Go/s en {dtn:6.2f} s")
    print(f"  rapport                : ×{go_s_n / go_s_1:.2f}")
    mm.close()
    f.close()


if __name__ == "__main__":
    main()
