#!/usr/bin/env python3
"""granularite_flux.py — le volume d'un flux de coupure selon sa GRANULARITÉ.

Un flux entre deux unités de traitement, c'est un ou plusieurs LISTES d'activation
(les événements). Ce script mesure, sur des activations RÉELLES vidées par le
moteur (`DRAVE_DUMP_COUCHES`), ce que coûte un flux selon :

  - la REPRÉSENTATION : dense f32, dense f16, liste DRVF v2 (écart u8 + valeur i16),
    liste « v3 » (échelle f16 par bloc de 32 + valeurs i8, estimée) ;
  - le SEUIL θ (fraction du max) qui décide quelles valeurs sont des événements ;
  - la GRANULARITÉ G : en combien de listes indépendantes on découpe le flux.

C'est la question de l'axe 3 (`docs/vision.md`) : « une liste est une unité de
travail autonome », donc plus de listes = plus de liberté de placement — mais
chaque liste paie son en-tête. Ce script donne le point où l'en-tête rattrape le
gain, et l'erreur qu'on accepte en échange.

Usage :
    granularite_flux.py <prefixe> --tensor l_last [--couches 0,20,42] [--positions 0,3]
                        [--seuils 0.01,0.02,0.05,0.1] [--granularites 1,4,16,64,512]
"""
import os
import struct
import sys

import numpy as np

ENTETE_LISTE = 14          # couche u16 + position u32 + n u32 + échelle f32 [v1/v2]


def lire(chemin):
    with open(chemin, "rb") as f:
        return np.frombuffer(f.read(), dtype="<f4").astype(np.float64)


def octets_v2(x, masque):
    """Liste DRVF v2 : en-tête + (écart u8 + valeur i16) par événement."""
    n = int(masque.sum())
    return ENTETE_LISTE + 3 * n


def octets_v3(x, masque, bloc=32):
    """Estimation DRVF v3 : échelle f16 par bloc de 32 canaux, écart u8 (255 →
    indice absolu u16) et valeur i8 par événement."""
    n_blocs = (len(x) + bloc - 1) // bloc
    n = int(masque.sum())
    return ENTETE_LISTE + 2 * n_blocs + n * 1 + n * 1


def erreur(x, masque):
    """Erreur relative L2 de la reconstruction « zéro hors événements »."""
    ref = np.linalg.norm(x)
    if ref == 0:
        return 0.0
    garde = np.where(masque, x, 0.0)
    return float(np.linalg.norm(x - garde) / ref)


def mesure(x, seuil, G):
    """Découpe x en G tranches égales, chacune avec son échelle (max local)."""
    n = len(x)
    bords = [round(i * n / G) for i in range(G + 1)]
    octets, evts, err_num, err_den = 0, 0, 0.0, 0.0
    for g in range(G):
        tranche = x[bords[g]:bords[g + 1]]
        if len(tranche) == 0:
            continue
        mx = float(np.abs(tranche).max())
        if mx == 0:
            continue
        masque = np.abs(tranche) >= seuil * mx
        octets += octets_v2(tranche, masque)
        evts += int(masque.sum())
        err_num += float(np.linalg.norm(tranche - np.where(masque, tranche, 0.0)) ** 2)
        err_den += float(np.linalg.norm(tranche) ** 2)
    return octets, evts, (err_num / err_den) ** 0.5 if err_den else 0.0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    prefixe = sys.argv[1]
    tenseur = "l_last"
    couches, positions = [0, 20, 42], [0, 3]
    seuils = [0.01, 0.02, 0.05, 0.1]
    grans = [1, 4, 16, 64, 512]
    for i, a in enumerate(sys.argv):
        if a == "--tensor" and i + 1 < len(sys.argv):
            tenseur = sys.argv[i + 1]
        if a == "--couches" and i + 1 < len(sys.argv):
            couches = [int(v) for v in sys.argv[i + 1].split(",")]
        if a == "--positions" and i + 1 < len(sys.argv):
            positions = [int(v) for v in sys.argv[i + 1].split(",")]
        if a == "--seuils" and i + 1 < len(sys.argv):
            seuils = [float(v) for v in sys.argv[i + 1].split(",")]
        if a == "--granularites" and i + 1 < len(sys.argv):
            grans = [int(v) for v in sys.argv[i + 1].split(",")]

    echantillons = []
    for l in couches:
        for p in positions:
            chemin = f"{prefixe}-{tenseur}-{l}-{p}.bin"
            if os.path.exists(chemin):
                echantillons.append((l, p, lire(chemin)))
    if not echantillons:
        print(f"aucun vidage {prefixe}-{tenseur}-*-*.bin")
        return 2
    n = len(echantillons[0][2])
    print(f"tenseur `{tenseur}` · {n} valeurs · {len(echantillons)} vidages "
          f"(couches {couches} × positions {positions})")
    print(f"  dense f32 : {4*n} octets · dense f16 : {2*n} octets  (par flux)")

    # 1. Le coût d'un flux selon le seuil, à granularité 1 (une liste par couche).
    print(f"\n--- granularité 1 : une liste pour tout le flux ---")
    print(f"{'seuil':>8} {'événements':>11} {'octets v2':>10} {'% dense':>8} "
          f"{'octets v3':>10} {'% dense':>8} {'erreur L2':>10}")
    for s in seuils:
        o2 = o3 = e = 0.0
        ev = 0
        for _, _, x in echantillons:
            mx = float(np.abs(x).max())
            masque = np.abs(x) >= s * mx if mx > 0 else np.zeros(len(x), bool)
            o2 += octets_v2(x, masque)
            o3 += octets_v3(x, masque)
            ev += int(masque.sum())
            e += erreur(x, masque)
        k = len(echantillons)
        print(f"{s:8.2f} {ev/k:11.0f} {o2/k:10.0f} {100*o2/k/(4*n):7.1f} % "
              f"{o3/k:10.0f} {100*o3/k/(4*n):7.1f} % {e/k:10.5f}")

    # 2. Le coût de la GRANULARITÉ, à seuil fixe : plus de listes, plus d'en-têtes.
    s = 0.05
    print(f"\n--- seuil {s} · ce que coûte la finesse (en-tête de {ENTETE_LISTE} octets "
          f"par liste) ---")
    print(f"{'listes':>8} {'valeurs/liste':>14} {'octets v2':>10} {'% dense f32':>12} "
          f"{'événements':>11} {'erreur L2':>10}")
    for G in grans:
        o2 = ev = 0.0
        e = 0.0
        for _, _, x in echantillons:
            a, b, c = mesure(x, s, G)
            o2 += a; ev += b; e += c
        k = len(echantillons)
        print(f"{G:8d} {n//G:14d} {o2/k:10.0f} {100*o2/k/(4*n):11.1f} % "
              f"{ev/k:11.0f} {e/k:10.5f}")

    # 3. Le cas réel du découpage : le flux de V4 porte `hc` copies.
    print("\n--- rappel du découpage V4 : le flux de coupure porte les `hc` copies ---")
    print("  (vision.md : 4 × 4 096 = 16 384 canaux, 64 Ko par flux en f32)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
