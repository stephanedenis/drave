#!/usr/bin/env python3
"""
Qtrinet — l'architecture « push » (AER) tient-elle sur un CPU ?

Architecture testée
-------------------
Au lieu de TIRER les activations à des indices arbitraires (gather, irrégulier),
on POUSSE : chaque source dont l'activation est non nulle émet un événement, sa
liste de destinations se lit séquentiellement (flux idéal depuis la DDR), et on
disperse (`acc[dest] += signe * x[src]`).

- la liste d'activation se construit **en cascade** (compaction des non-nuls),
- l'accès aléatoire se déplace de l'entrée (activation, 4096 large, non bornée)
  vers la sortie (accumulateur, 4096 x 24 bits = 12 Kio, tient en M20K),
- les poids se lisent en flux séquentiel : plus aucun gather.

Questions mesurées ici :
  1. quelle bande passante mémoire ce bi-Xeon offre-t-il réellement ?
  2. à quelle cadence un CPU disperse-t-il des événements ?
  3. qu'est-ce que cela donne pour un 7B dans ce format, face à une carte FPGA ?

Usage :  python3 run_cpu.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent / "src"))

from roofline import CARD  # noqa: E402

# Couche type d'un 7B (Llama) : gate/up proj
N_IN, N_OUT = 4096, 11008
DENSITY = 0.05
N_EVENTS_TARGET = 4_000_000


def timed(fn, repeat: int = 3):
    best = float("inf")
    out = None
    for _ in range(repeat):
        t0 = time.perf_counter()
        out = fn()
        best = min(best, time.perf_counter() - t0)
    return best, out


# --------------------------------------------------------------------------- #
# 1. Bande passante mémoire
# --------------------------------------------------------------------------- #


def bench_memory():
    print("=== 1. Bande passante mémoire du bi-Xeon E5-2687W v3 ===")
    n = 64 * 1024 * 1024                       # 256 Mo en float32
    a = np.ones(n, dtype=np.float32)
    b = np.ones(n, dtype=np.float32)
    c = np.empty_like(a)

    dt, _ = timed(lambda: a.sum())
    bw = n * 4 / dt / 1e9
    print(f"  lecture séquentielle  : {bw:7.1f} Go/s")

    dt, _ = timed(lambda: np.add(a, b, out=c))
    bw3 = 3 * n * 4 / dt / 1e9
    print(f"  triad (2 lectures + 1 écriture) : {bw3:7.1f} Go/s")

    del a, b, c
    return bw


# --------------------------------------------------------------------------- #
# 2. Cadence de dispersion
# --------------------------------------------------------------------------- #


def bench_scatter():
    print("\n=== 2. Cadence de dispersion (acc[dest] += v) ===")
    rng = np.random.default_rng(0)
    acc = np.zeros(N_OUT, dtype=np.float32)
    dest = rng.integers(0, N_OUT, size=N_EVENTS_TARGET)
    vals = rng.standard_normal(N_EVENTS_TARGET).astype(np.float32)

    t0 = time.perf_counter()
    np.add.at(acc, dest, vals)
    dt_addat = time.perf_counter() - t0
    print(f"  np.add.at   : {N_EVENTS_TARGET/dt_addat/1e9:6.2f} G événements/s")

    t0 = time.perf_counter()
    _ = np.bincount(dest, weights=vals, minlength=N_OUT)
    dt_bc = time.perf_counter() - t0
    print(f"  np.bincount : {N_EVENTS_TARGET/dt_bc/1e9:6.2f} G événements/s")

    # dispersion dans un accumulateur volontairement petit (tient en L1/L2)
    acc_small = np.zeros(1024, dtype=np.float32)
    dest_small = rng.integers(0, 1024, size=N_EVENTS_TARGET)
    t0 = time.perf_counter()
    np.add.at(acc_small, dest_small, vals)
    dt_small = time.perf_counter() - t0
    print(f"  np.add.at sur 1024 accumulateurs (L1) : "
          f"{N_EVENTS_TARGET/dt_small/1e9:6.2f} G événements/s")

    return N_EVENTS_TARGET / dt_bc, N_EVENTS_TARGET / dt_addat


# --------------------------------------------------------------------------- #
# 3. Couche complète en mode « push »
# --------------------------------------------------------------------------- #


def bench_layer(density: float = DENSITY):
    """Construit une couche creuse ternaire et l'exécute en mode push."""
    print(f"\n=== 3. Couche {N_IN}→{N_OUT} à {density*100:.0f} % de densité, mode push ===")
    rng = np.random.default_rng(1)

    # --- encodage : listes signées triées (deltas) ---
    nnz_per_row = int(round(density * N_OUT))
    t0 = time.perf_counter()
    src_all, dst_all, sign_all = [], [], []
    for i in range(N_IN):
        d = np.sort(rng.choice(N_OUT, size=nnz_per_row, replace=False))
        src_all.append(np.full(nnz_per_row, i, dtype=np.int32))
        dst_all.append(d.astype(np.int32))
        sign_all.append(rng.choice(np.array([-1, 1], dtype=np.int8), size=nnz_per_row))
    src = np.concatenate(src_all)
    dst = np.concatenate(dst_all)
    sign = np.concatenate(sign_all)
    dt_enc = time.perf_counter() - t0
    n_events = src.size
    print(f"  {n_events/1e6:.2f} M événements ({n_events*100/(N_IN*N_OUT):.1f} % de la matrice)")

    # --- activation : 50 % de non-nuls, valeurs quelconques ---
    x = rng.standard_normal(N_IN).astype(np.float32)
    x[rng.random(N_IN) < 0.5] = 0.0
    active = x != 0

    # la liste d'activation se construit en cascade (compaction)
    t0 = time.perf_counter()
    act_idx = np.flatnonzero(active)
    dt_cascade = time.perf_counter() - t0
    print(f"  construction de la liste d'activation (cascade) : "
          f"{len(act_idx)}/{N_IN} actifs en {dt_cascade*1e6:.1f} µs")

    # --- exécution push : on saute les sources inactives ---
    keep = active[src]
    src_a, dst_a, sign_a = src[keep], dst[keep], sign[keep]
    n_ev = src_a.size
    vals = sign_a.astype(np.float32) * x[src_a]

    t0 = time.perf_counter()
    acc = np.bincount(dst_a, weights=vals, minlength=N_OUT)
    dt_run = time.perf_counter() - t0
    print(f"  {n_ev/1e6:.2f} M événements effectifs en {dt_run*1e3:7.3f} ms "
          f"→ {n_ev/dt_run/1e9:6.2f} G événements/s")
    print(f"  (encodage/décodage de la couche mesuré à part : {dt_enc*1e3:.1f} ms)")

    # --- comparaison : dense int8 sur la même couche ---
    W_dense = np.zeros((N_IN, N_OUT), dtype=np.float32)
    W_dense[src, dst] = sign
    t0 = time.perf_counter()
    _ = x @ W_dense
    dt_dense = time.perf_counter() - t0
    dense_bytes = W_dense.nbytes
    print(f"  comparaison dense float32 : {dt_dense*1e3:7.1f} ms "
          f"({dense_bytes/1e6:.0f} Mo lus → {dense_bytes/dt_dense/1e9:.1f} Go/s)")

    return n_ev, dt_run


def main():
    bw = bench_memory()
    bc_rate, addat_rate = bench_scatter()
    n_ev, dt_run = bench_layer()

    # ---------------- projection 7B ---------------------------------------- #
    # 7B paramètres, densité 5 %, coût 0,476 b/poids (mesuré au run précédent)
    from math import log2
    d = DENSITY
    bits_per_weight = 0.476
    bytes_per_token = 7e9 * bits_per_weight / 8
    events_per_token = 7e9 * d

    print("\n=== 4. Projection 7B (densité 5 %, listes signées 0,476 b/poids) ===")
    print(f"  poids à lire par token : {bytes_per_token/1e6:7.1f} Mo")
    print(f"  événements par token   : {events_per_token/1e6:7.1f} M")

    # Nombres mesurés par bench/cpu_aer.c (16 threads, gcc -O3 -fopenmp)
    BW_C = 28.7e9          # Go/s, lecture séquentielle
    EV_C = 7.79e9          # événements/s, décodage d'écarts + dispersion

    t_cpu_bw = bytes_per_token / BW_C
    t_cpu_ev = events_per_token / EV_C
    print(f"  borné par la bande passante CPU ({BW_C/1e9:.1f} Go/s) : {t_cpu_bw*1e3:7.2f} ms/token "
          f"→ {1/t_cpu_bw:6.1f} tok/s")
    print(f"  borné par le noyau ({EV_C/1e9:.2f} G év/s)          : {t_cpu_ev*1e3:7.2f} ms/token "
          f"→ {1/t_cpu_ev:6.1f} tok/s")
    t_cpu = max(t_cpu_bw, t_cpu_ev)
    print(f"  → CPU réaliste : {t_cpu*1e3:.2f} ms/token, soit {1/t_cpu:.1f} tok/s")

    t_fpga = bytes_per_token / CARD["ddr3_read_Bps"]
    print(f"  → 1 carte FPGA (DDR3 9,66 Go/s) : {t_fpga*1e3:.2f} ms/token, "
          f"soit {1/t_fpga:.1f} tok/s")
    print(f"  → 4 cartes (modèle réparti) : {t_fpga*1e3/4:.2f} ms/token, soit {4/t_fpga:.1f} tok/s")
    print(f"\n  RAPPORT : CPU {1/t_cpu:.1f} tok/s  vs  1 carte {1/t_fpga:.1f} tok/s "
          f"→ {1/t_cpu/(1/t_fpga):.2f}x")

    # ----------------------------- rapport --------------------------------- #
    L = ["# Qtrinet — l'architecture « push » (AER) sur CPU\n",
         "## L'architecture\n",
         "Au lieu de **tirer** les activations à des indices arbitraires (gather), on",
         "**pousse** : chaque source active émet un événement, sa liste de destinations se",
         "lit **séquentiellement**, et on disperse `acc[dest] += signe · x[src]`.\n",
         "- la liste d'activation se construit **en cascade** (compaction des non-nuls) ;",
         "- l'accès aléatoire se déplace de l'entrée (activation, large) vers la sortie",
         "  (accumulateur, 4096 × 24 bits = **12 Kio**, tient dans les M20K) ;",
         "- les poids se lisent en **flux séquentiel** : plus aucun gather.\n",
         "## Mesures sur ce bi-Xeon E5-2687W v3\n",
         f"- bande passante lecture séquentielle : **{bw:.1f} Go/s**",
         f"- dispersion (`np.bincount`) : **{bc_rate:.2f} G événements/s**",
         f"- dispersion (`np.add.at`) : {addat_rate:.2f} G événements/s\n",
         "## Limites mesurées du CPU (bench/cpu_aer.c, 16 threads)\n",
         "| Test | 1 th | 8 th | 16 th | 32 th |", "|---|---|---|---|---|",
         "| Lecture séquentielle | 4,1 Go/s | 23,4 | **28,7** | 28,2 |",
         "| Dispersion pure | 0,96 G év/s | 3,46 | 3,20 | 3,22 |",
         "| **Écarts + dispersion** | 0,87 | 4,55 | **7,79** | 6,79 |",
         "\nLa dispersion sature vers 8 threads : c'est l'accès aléatoire à",
         "l'accumulateur qui limite, pas la bande passante. Le décodage par écarts est",
         "quasi gratuit (le noyau complet est plus rapide que la dispersion pure).\n",
         "## Projection 7B (densité 5 %, 0,476 b/poids)\n",
         "| Cible | ms/token | tok/s |", "|---|---|---|",
         f"| CPU, borné bande passante (28,7 Go/s) | {t_cpu_bw*1e3:.2f} | {1/t_cpu_bw:.1f} |",
         f"| CPU, borné noyau (7,79 G év/s) | {t_cpu_ev*1e3:.2f} | {1/t_cpu_ev:.1f} |",
         f"| **CPU réaliste** | **{t_cpu*1e3:.2f}** | **{1/t_cpu:.1f}** |",
         f"| 1 carte FPGA | {t_fpga*1e3:.2f} | {1/t_fpga:.1f} |",
         f"| 4 cartes FPGA (modèle réparti) | {t_fpga*1e3/4:.2f} | {4/t_fpga:.1f} |",
         "\n## Verdict\n",
         f"1. **Oui, c'est pensable sur CPU** — et c'est même la bonne façon de valider le",
         "   format avant d'écrire du RTL : un CPU sert de **modèle d'or** pour la sémantique",
         "   des événements (quels non-nuls, quel ordre, quelles échelles).",
         "2. **La dispersion n'est pas le goulot** tant que l'accumulateur tient dans le",
         f"   cache : {bc_rate:.1f} G événements/s mesurés contre "
         f"{events_per_token/1e9:.2f} G nécessaires par token.",
         f"3. **Une carte FPGA ≈ ce CPU** ({1/t_fpga:.0f} contre {1/t_cpu:.0f} tok/s) : le CPU a",
         "   3× la bande passante (28,7 contre 9,66 Go/s) mais il est limité par sa",
         "   **cadence d'événements** (7,8 G/s), là où la carte est limitée par sa DDR3.",
         "   Les deux arrivent au même point par des chemins opposés.",
         "4. **L'avantage du FPGA est le passage à l'échelle, pas la carte seule** :",
         "   4 cartes = 4 mémoires et 4 jeux de voies indépendants → 4× le débit, là où",
         "   le CPU bute sur ses contrôleurs mémoire. C'est **exactement l'argument du",
         "   ring** : additionner des systèmes mémoire autonomes.",
         "5. **Conséquence pratique** : écrire d'abord l'implémentation CPU. Elle est",
         "   immédiate, elle valide le format et la sémantique des événements, et elle",
         "   fournit le **modèle d'or** que le RTL devra reproduire. Le FPGA n'a de sens",
         "   qu'à partir de 2-4 cartes.",
         "\n> ⚠️ Mesures sur un seul type de couche et un CPU donné. La dispersion réelle",
         "> d'un noyau optimisé (SIMD, multi-thread, accumulateurs par banc) peut aller",
         "> plus vite que `np.bincount` ; à confirmer avec un noyau C/OpenMP avant de",
         "> conclure définitivement.\n",
         "\n---\n*Généré par `run_cpu.py` — Qtrinet.*\n"]

    out = Path("reports/rapport-cpu-aer.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"\nRapport écrit : {out}")


if __name__ == "__main__":
    main()
