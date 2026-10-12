#!/usr/bin/env python3
"""banc-prelire.py — le mécanisme de lecture du moteur, mesuré hors du moteur.

Ce que la porte de S4 doit comparer : **lecture à la demande** (défaut de page) contre
**lecture préchargée par grappe** (`madvise(MADV_WILLNEED)` puis parcours). Le banc isole
le mécanisme : il mappe un fichier, lit le MÊME nombre d'octets utiles de trois façons, et
rend des **Mo/s utiles**.

Pourquoi des pages touchées et pas des `pread` : le chiffre connu du dépôt (**8,6 Mo/s**
sur disque dur, `docs/modele-pour-drave.md` § 12 bis) vient de la lecture **par défauts de
page**, où le noyau ajoute sa propre lecture en avance. Un `O_DIRECT` de 4 Kio au hasard
mesure autre chose, et bien pire.

QUATRE PRÉCAUTIONS, chacune payée par une mesure fausse :

  * **une fenêtre plus petite que la lecture en avance du noyau n'est pas un hasard** :
    avec 400 pages dans 1,6 Mo, le noyau lisait tout le voisinage au premier défaut et le
    bras « au hasard » rendait 300 Mo/s (du cache) — les pages sont donc tirées sur
    **2 Gio**, très au-delà de toute lecture en avance (`read_ahead_kb` = 1 024 Kio ici) ;
  * **le contrôle à froid ne doit pas chauffer ce qu'on mesure** : il touche une page
    **8 Mio à côté** de la zone mesurée, et son temps est publié (froid ≈ ms sur plateau,
    ≈ 0 en cache) ;
  * **`madvise` est asynchrone** : on le lance sur la fenêtre entière, puis on la touche ;
  * trois répétitions entrelacées (règle du dépôt), médiane publiée, détail par répétition.

usage : banc-prelire.py [fichier] [--pages N] [--grappe K]
"""
import mmap
import os
import random
import statistics
import sys
import time

PAGE = 4096
MIO = 1 << 20
GIO = 1 << 30


def mo_par_s(octets, secondes):
    return octets / secondes / 1e6


def controle_froid(mm, base, marge=8 * MIO):
    """Défaut de page HORS de la zone mesurée (8 Mio à côté)."""
    t0 = time.perf_counter()
    mm[base + marge]
    return (time.perf_counter() - t0) * 1e6      # µs


def bras_demande(mm, base, pages, etendue, rng):
    """Des pages tirées au hasard sur `etendue` octets — le régime du manque."""
    t0 = time.perf_counter()
    for _ in range(pages):
        mm[base + rng.randrange(0, etendue // PAGE) * PAGE]
    return mo_par_s(pages * PAGE, time.perf_counter() - t0)


def bras_sequentiel(mm, base, pages):
    """Des pages consécutives — la borne haute."""
    t0 = time.perf_counter()
    for i in range(pages):
        mm[base + i * PAGE]
    return mo_par_s(pages * PAGE, time.perf_counter() - t0)


def bras_grappe(mm, base, pages, etendue, k, rng):
    """Des grappes de `k` pages dispersées sur `etendue` : madvise PUIS parcours."""
    nb = max(1, pages // k)
    debuts = sorted(rng.randrange(0, max(1, etendue // PAGE - k)) * PAGE for _ in range(nb))
    t0 = time.perf_counter()
    fait = 0
    for debut in debuts:
        mm.madvise(mmap.MADV_WILLNEED, base + debut, k * PAGE)
        for i in range(k):
            mm[base + debut + i * PAGE]
        fait += k
    return mo_par_s(fait * PAGE, time.perf_counter() - t0)


def main():
    args = sys.argv[1:]
    fichier = "/home/stephane/IA/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf"
    if args and not args[0].startswith("-"):
        fichier = args.pop(0)
    pages, grappe = 2000, 256
    if "--pages" in args:
        pages = int(args[args.index("--pages") + 1])
    if "--grappe" in args:
        grappe = int(args[args.index("--grappe") + 1])
    fichier = os.path.expanduser(fichier)

    taille = os.path.getsize(fichier)
    etendue = 2 * GIO                     # l'étendue du tirage au hasard
    # Une zone par (bras, répétition) : 4 Gio d'écart, plus les 8 Mio du contrôle à froid
    ecart = 4 * GIO
    besoin = etendue + 16 * MIO
    bras = ("demande", "sequentiel", "grappe")
    if taille < len(bras) * 3 * ecart + besoin:
        print(f"fichier trop petit ({taille / 1e9:.1f} Go) pour 9 zones de "
              f"{ecart / 1e9:.0f} Gio — réduire --pages")
        return 1

    rng = random.Random(20261012)
    print(f"fichier : {os.path.basename(fichier)} ({taille / 1e9:.1f} Go)")
    print(f"  {pages} pages utiles par bras ({pages * PAGE / 1e6:.1f} Mo) · "
          f"tirage au hasard sur {etendue / GIO:.0f} Gio · grappe {grappe} pages "
          f"({grappe * PAGE / 1024:.0f} Kio) · 3 zones de {ecart / GIO:.0f} Gio par bras")
    resultats = {b: [] for b in bras}
    with open(fichier, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            for r in range(3):
                for i, b in enumerate(bras):
                    base = (i * 3 + r) * ecart + 32 * MIO
                    base -= base % PAGE
                    froid = controle_froid(mm, base)
                    if b == "demande":
                        v = bras_demande(mm, base, pages, etendue, rng)
                    elif b == "sequentiel":
                        v = bras_sequentiel(mm, base, pages)
                    else:
                        v = bras_grappe(mm, base, pages, etendue, grappe, rng)
                    resultats[b].append(v)
                    print(f"  {b:11} rép {r + 1} : {v:9.2f} Mo/s utiles   "
                          f"(défaut de page témoin, 8 Mio à côté : {froid:8.1f} µs)")
        finally:
            mm.close()
    print(f"{'bras':12} {'médiane':>11}   les trois répétitions")
    for b in bras:
        v = resultats[b]
        print(f"{b:12} {statistics.median(v):8.2f} Mo/s   "
              + " ".join(f"{x:.2f}" for x in v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
