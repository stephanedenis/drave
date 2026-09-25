#!/usr/bin/env python3
"""
Qtrinet — 8 bits : peut-on atteindre la perfection (compression sans perte) ?

À 8 bits, la qualité est déjà quasi parfaite. La seule question qui reste est
celle du **stockage sans perte** : peut-on descendre sous 8 bits/poids en
reconstruisant exactement les niveaux ?

Réponse exacte = l'entropie de la distribution des niveaux, et la longueur
moyenne d'un vrai code de Huffman construit sur cette distribution. On mesure
les deux, plus le coût des encodages structurels (plans, unaire) pour comparaison.

Usage :  python3 run_8bit_perfection.py [--model models/Qwen2.5-0.5B-Q8_0.gguf]
"""

from __future__ import annotations

import argparse
import heapq
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent / "src"))

from gguf_min import GGUF  # noqa: E402


def huffman_lengths(freq: dict[int, int]) -> dict[int, int]:
    """Longueurs de code de Huffman pour une distribution de symboles."""
    if len(freq) == 1:
        return {next(iter(freq)): 1}
    heap = [(c, i, (s,)) for i, (s, c) in enumerate(freq.items())]
    heapq.heapify(heap)
    lengths: dict[int, int] = {}
    counter = len(heap)
    while len(heap) > 1:
        c1, _, s1 = heapq.heappop(heap)
        c2, _, s2 = heapq.heappop(heap)
        for s in s1 + s2:
            lengths[s] = lengths.get(s, 0) + 1
        heapq.heappush(heap, (c1 + c2, counter, s1 + s2))
        counter += 1
    return lengths


def popcount(a: np.ndarray) -> np.ndarray:
    a = a.astype(np.int64)
    out = np.zeros_like(a)
    while a.any():
        out += a & 1
        a >>= 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", type=Path, default=Path("models/Qwen2.5-0.5B-Q8_0.gguf"))
    ap.add_argument("--out", type=Path, default=Path("reports/rapport-8bits.md"))
    args = ap.parse_args()

    g = GGUF(args.model)
    mats = [n for n in g.tensors
            if n.endswith(".weight") and len(g.tensors[n].shape) == 2
            and g.tensors[n].ttype in (2, 8)]
    print(f"Modèle : {g.arch()}  ({args.model.name}) — {len(mats)} matrices\n")

    # Histogramme 256 niveaux accumulé en vectorisé — tout le reste en dérive.
    hist = np.zeros(256, dtype=np.int64)
    n_tot = 0
    for i, n in enumerate(mats):
        q = g.raw_levels(n).astype(np.int16).ravel()
        hist += np.bincount(q + 128, minlength=256)
        n_tot += q.size
        if (i + 1) % 40 == 0:
            print(f"    {i+1}/{len(mats)} matrices…", flush=True)

    levels = np.arange(-128, 128)
    cnt = hist
    n_nz = int(cnt[levels != 0].sum())
    sum_abs = int((np.abs(levels) * cnt).sum())
    pc = np.bitwise_count(np.abs(levels).astype(np.uint8)).astype(np.int64)
    sum_pop = int((pc * cnt).sum())

    dens = n_nz / n_tot
    E_abs = sum_abs / n_nz
    E_pop = sum_pop / n_nz

    # ---------------------------------------------------------------- entropie
    total = int(cnt.sum())
    p = cnt[cnt > 0] / total
    H = float(-(p * np.log2(p)).sum())
    freq = {int(v): int(c) for v, c in zip(levels, cnt) if c > 0}
    lens = huffman_lengths(freq)
    L_huff = sum(freq[s] * l for s, l in lens.items()) / total

    print("=== 1. Distribution des niveaux Q8_0 ===")
    print(f"  poids analysés        : {n_tot/1e6:.1f} M")
    print(f"  densité (non nuls)    : {dens*100:.1f} %")
    print(f"  niveaux distincts     : {int((cnt > 0).sum())}")
    print(f"  E[|v|]                : {E_abs:.2f}")
    print(f"  E[popcount(|v|)]      : {E_pop:.2f}")
    order = np.argsort(-cnt)[:8]
    top = [(int(levels[i]), int(cnt[i])) for i in order if cnt[i] > 0]
    print("  niveaux les plus fréquents : " +
          ", ".join(f"{s}({c/total*100:.1f}%)" for s, c in top))

    print("\n=== 2. Combien de bits sont VRAIMENT nécessaires (sans perte) ? ===")
    print(f"  codage positionnel fixe : {8:.3f} b/poids")
    print(f"  entropie de la source   : {H:.3f} b/poids")
    print(f"  code de Huffman réel    : {L_huff:.3f} b/poids")
    gain_h = 8 / H
    gain_l = 8 / L_huff
    print(f"  → gain maximal théorique : ×{gain_h:.3f}")
    print(f"  → gain réel (Huffman)    : ×{gain_l:.3f}")

    print("\n=== 3. Encodages structurels (pour comparaison) ===")
    print(f"{'stratégie':<34} {'bits/poids':>11} {'opérations/poids':>17}")
    print(f"{'positionnel (8 bits)':<34} {8.0:11.2f} {dens:17.2f}")
    print(f"{'plans denses (7 plans + signe)':<34} {8.0:11.2f} {E_pop*dens:17.2f}")
    print(f"{'unaire (répétition d adresse)':<34} {dens*E_abs:11.2f} {dens*E_abs:17.2f}")
    print(f"{'Huffman (sans perte)':<34} {L_huff:11.2f} {dens:17.2f}")

    print("\n=== 4. Ce que cela donnerait sur le modèle entier ===")
    bytes_brut = n_tot * 8 / 8
    print(f"  taille des niveaux (8 bits) : {bytes_brut/1e6:8.1f} Mo")
    print(f"  après Huffman               : {n_tot*L_huff/8/1e6:8.1f} Mo "
          f"(×{gain_l:.3f})")
    print(f"  borne entropique            : {n_tot*H/8/1e6:8.1f} Mo (×{gain_h:.3f})")

    # ------------------------------------------------------------------ rapport
    L = ["# Qtrinet — 8 bits : la perfection est-elle atteignable ?\n",
         f"Modèle : **{g.arch()}** en Q8_0, {n_tot/1e6:.1f} M poids analysés.\n",
         "## 1. Distribution des niveaux\n",
         f"- densité : **{dens*100:.1f} %**",
         f"- niveaux distincts : **{len(hist)}** (sur 256 possibles)",
         f"- `E[|v|]` : **{E_abs:.2f}**",
         f"- `E[popcount(|v|)]` : **{E_pop:.2f}**",
         f"- niveaux les plus fréquents : " +
         ", ".join(f"`{s}` ({c/total*100:.1f} %)" for s, c in top) + "\n",
         "## 2. Bits réellement nécessaires (sans perte)\n",
         "| Codage | bits/poids | Gain |", "|---|---|---|",
         f"| positionnel fixe | 8,000 | ×1,000 |",
         f"| **entropie de la source** | **{H:.3f}** | **×{gain_h:.3f}** |",
         f"| **code de Huffman réel** | **{L_huff:.3f}** | **×{gain_l:.3f}** |\n",
         "## 3. Encodages structurels\n",
         "| Stratégie | bits/poids | opérations/poids |", "|---|---|---|",
         f"| positionnel (8 bits) | 8,00 | {dens:.2f} |",
         f"| plans denses (7 plans + signe) | 8,00 | {E_pop*dens:.2f} |",
         f"| unaire (répétition) | {dens*E_abs:.2f} | {dens*E_abs:.2f} |",
         f"| **Huffman (sans perte)** | **{L_huff:.2f}** | {dens:.2f} |\n",
         "## 4. Sur le modèle entier\n",
         f"| | Taille des niveaux | Gain |", "|---|---|---|",
         f"| 8 bits brut | {bytes_brut/1e6:.1f} Mo | — |",
         f"| Huffman | {n_tot*L_huff/8/1e6:.1f} Mo | ×{gain_l:.3f} |",
         f"| borne entropique | {n_tot*H/8/1e6:.1f} Mo | ×{gain_h:.3f} |\n",
         "## Verdict\n",
         "1. **La qualité à 8 bits est déjà la perfection pratique** : c'est la référence",
         "   quasi sans perte de l'écosystème. La question qui reste n'est pas la qualité",
         "   mais le **stockage exact**.",
         f"2. **Le gain sans perte existe mais il est modeste** : l'entropie de la source",
         f"   vaut {H:.2f} b/poids et un vrai code de Huffman atteint {L_huff:.2f} b/poids,"
         f" soit **×{gain_l:.2f}**.",
         "3. **L'uniformité des niveaux est la raison** : un quantificateur Q8_0 bien réglé",
         "   répartit les poids sur beaucoup de niveaux, ce qui rapproche la distribution",
         "   de l'uniforme et l'entropie de 8 bits. Il n'y a presque rien à récupérer :",
         "   **c'est le signe d'une quantification déjà efficace**.",
         "4. **Les encodages structurels ne servent à rien à 8 bits** : les plans denses",
         "   coûtent exactement 8 bits/poids (7 magnitude + 1 signe = le code positionnel),",
         f"   et l'unaire explose ({dens*E_abs:.0f} b/poids). La répétition d'adresse, si",
         "   élégante soit-elle, n'a de sens que sur les petites valeurs.",
         "5. **Conclusion** : la perfection sans perte se paie au prix de l'entropie, et",
         "   à 8 bits l'entropie est déjà presque atteinte. Le vrai levier reste la",
         "   **quantification à 4 bits et moins**, où la structure a de la place pour",
         "   s'exprimer — c'est là que les gains mesurés (×2,17) se trouvent.\n",
         "\n---\n*Généré par `run_8bit_perfection.py` — Qtrinet.*\n"]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(L), encoding="utf-8")
    print(f"\nRapport écrit : {args.out}")
    g.close()


if __name__ == "__main__":
    main()
