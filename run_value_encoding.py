#!/usr/bin/env python3
"""
Drave — peut-on éliminer la valeur en répétant l'adresse d'activation ?

Idée testée : plutôt que de stocker la valeur quantifiée v d'un poids, on
**répète l'adresse v fois** — l'accumulateur ajoute v fois l'activation. En
adressage relatif, cela revient à une suite de v−1 marqueurs « même adresse ».
C'est exact (aucune perte au-delà de la quantification d'origine), mais c'est de
l'encodage **unaire** : le coût est proportionnel à v, là où l'encodage
positionnel coûte log2(v).

On mesure sur un VRAI modèle 4 bits (Qwen2.5-0.5B Q4_0, niveaux entiers
−8..+7 stockés tels quels) :

  - la distribution réelle des niveaux |v|,
  - le coût des trois stratégies, par poids non nul :
      positionnel : k bits stockés, 1 opération
      unaire      : (v−1) marqueurs, v opérations
      plans       : popcount(v) marqueurs, popcount(v) opérations
  - le seuil de bascule entre unaire et positionnel.

Usage :  python3 run_value_encoding.py [--model models/Qwen2.5-0.5B-Q4_0.gguf]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent / "src"))

from gguf_min import GGUF  # noqa: E402


def popcount(a: np.ndarray) -> np.ndarray:
    a = a.astype(np.int64)
    out = np.zeros_like(a)
    while a.any():
        out += a & 1
        a >>= 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", type=Path, default=Path("models/Qwen2.5-0.5B-Q4_0.gguf"))
    ap.add_argument("--out", type=Path, default=Path("reports/rapport-valeur-unaire.md"))
    args = ap.parse_args()

    g = GGUF(args.model)
    print(f"Modèle : {g.arch()}  ({args.model.name})")

    mats = [n for n in g.tensors
            if n.endswith(".weight") and len(g.tensors[n].shape) == 2
            and g.tensors[n].ttype in (2, 8)]
    print(f"Matrices 2-D quantifiées : {len(mats)}\n")

    # --- séparation par type de quantification (Q4_0 = type 2, Q8_0 = type 8) ---
    def stats(ttype):
        hist = np.zeros(9, dtype=np.int64)
        n_tot = n_nz = sum_abs = sum_pop = 0
        for n in mats:
            if g.tensors[n].ttype != ttype:
                continue
            q = np.abs(g.raw_levels(n).astype(np.int32))
            hist += np.bincount(q.ravel(), minlength=9)[:9]
            n_tot += q.size
            nz = q > 0
            n_nz += int(nz.sum())
            sum_abs += int(q.sum())
            sum_pop += int(popcount(q[nz]).sum()) if nz.any() else 0
        return hist, n_tot, n_nz, sum_abs, sum_pop

    h4, n4, nz4, sa4, sp4 = stats(2)
    h8, n8, nz8, sa8, sp8 = stats(8)
    print("=== 1. Distribution réelle des niveaux, PAR TYPE DE QUANTIFICATION ===")
    for tag, h, nt, nz, sa, sp in (("Q4_0", h4, n4, nz4, sa4, sp4),
                                   ("Q8_0", h8, n8, nz8, sa8, sp8)):
        if nz == 0:
            continue
        print(f"\n  --- {tag} : {nt/1e6:.2f} M poids, densité {nz/nt*100:.1f} % ---")
        print(f"    E[|v|] sur non-nuls = {sa/nz:6.2f}   "
              f"E[popcount] = {sp/nz:5.2f}")
        for v in range(1, 9):
            if h[v]:
                print(f"      |v|={v} : {h[v]/nz*100:5.1f} % des non-nuls")

    hist, n_tot, n_nz = h4, n4, nz4
    dens = n_nz / n_tot
    E_abs = sa4 / nz4
    E_pop = sp4 / nz4

    import encoding as E
    gap = 1.0 / dens
    addr = E.gamma_bits(int(round(gap)))       # coût d'une adresse (écart), en bits
    print(f"\n=== 2. Coût COMPLET par poids (adresses incluses) ===")
    print(f"  densité {dens*100:.1f} % → écart moyen {gap:.2f} → adresse = {addr} bits")
    print(f"{'stratégie':<34} {'bits/poids':>11} {'opérations/poids':>17}")
    k = 4
    print(f"{'dense positionnel (4 bits)':<34} {k:11.2f} {dens:17.2f}")
    print(f"{'creux positionnel (4 b + adr)':<34} {dens*(k+addr):11.2f} {dens:17.2f}")
    print(f"{'creux unaire (répétition)':<34} {dens*(addr+E_abs-1):11.2f} "
          f"{dens*E_abs:17.2f}")
    print(f"{'creux plans (popcount)':<34} {dens*(addr+E_pop):11.2f} "
          f"{dens*E_pop:17.2f}")
    p1 = h4[1] / nz4                       # part des non-nuls valant ±1
    E_hyb = E_pop - p1                     # |v|=1 : gratuit (l'adresse porte le signe)
    print(f"{'creux HYBRIDE (unaire+plans)':<34} {dens*(addr+E_hyb):11.2f} "
          f"{dens*E_hyb:17.2f}")
    print(f"  (hybride = unaire pour |v|=1 — gratuit — puis plans ; "
          f"{p1*100:.1f} % des non-nuls en bénéficient)")
    best = min(4.0, dens*(k+addr), dens*(addr+E_abs-1), dens*(addr+E_pop),
               dens*(addr+E_hyb))
    print(f"\n  → meilleur : {best:.2f} b/poids contre 4,00 pour le code dense "
          f"= ×{4.0/best:.2f} de compression, SANS perte de qualité")

    print("\n=== 3. Seuil de bascule unaire vs positionnel ===")
    print("  L'unaire gagne si E[|v|] − 1 < k, soit E[|v|] < k + 1 :")
    for kk in (1, 2, 3, 4, 6, 8):
        # E[|v|] pour une distribution uniforme sur 0..2^k − 1 (non nuls)
        E_uniform = ((2 ** kk) - 1) / 2
        verdict = "UNAIRE gagne" if E_uniform - 1 < kk else "positionnel gagne"
        print(f"    k={kk} bits : E[|v|]≈{E_uniform:5.1f}  → coût unaire {E_uniform-1:5.1f} "
              f"vs {kk}  →  {verdict}")
    print(f"\n  Sur CE modèle Q4_0 réel : E[|v|] = {E_abs:.2f} par non-nul.")
    print(f"    coût unaire    = E[|v|]−1 = {E_abs-1:.2f} bit  (vs 4 bits positionnels)")
    print(f"    coût par plans = popcount = {E_pop:.2f} bit")
    print(f"    → {'UNAIRE gagne' if E_abs-1 < 4 else 'POSITIONNEL gagne'} sur le stockage")
    print(f"    → mais {E_abs:.2f} opérations par non-nul contre 1 pour le positionnel")

    print("\n=== 4. Et pour un modèle binaire / ternaire ? ===")
    print("  binaire (k=1) : les non-nuls valent tous 1 → coût unaire = 0 bit,")
    print("                  l'adresse SEULE porte la valeur. L'idée est optimale.")
    print("  ternaire      : deux listes signées (+, −) → même résultat, 0 bit de valeur.")

    # ------------------------------------------------------------------ rapport
    L = ["# Drave — éliminer la valeur par répétition d'adresse ?\n",
         f"Modèle mesuré : **{g.arch()}** quantifié **Q4_0** ({len(mats)} matrices 2-D).",
         "Les niveaux sont lus *tels que stockés* (−8..+7), avant mise à l'échelle.\n",
         "## 1. Distribution réelle des niveaux\n",
         f"- zéros : **{hist[0]/n_tot*100:.1f} %** des poids (densité {dens*100:.1f} %)",
         f"- `E[|v|]` sur les non-nuls : **{E_abs:.2f}**",
         f"- `E[popcount(|v|)]` : **{E_pop:.2f}**\n",
         "| \\|v\\| | Part des poids | Part des non-nuls |", "|---|---|---|"]
    for v in range(1, 9):
        if hist[v]:
            L.append(f"| {v} | {hist[v]/n_tot*100:.2f} % | {hist[v]/n_nz*100:.1f} % |")

    L += ["\n## 2. Coût par poids non nul\n",
          "| Stratégie | Bits stockés | Opérations |", "|---|---|---|",
          f"| positionnel (4 bits) | 4,00 | 1,00 |",
          f"| **unaire (répétition d'adresse)** | **{E_abs-1:.2f}** | **{E_abs:.2f}** |",
          f"| plans binaires (popcount) | {E_pop:.2f} | {E_pop:.2f} |",
          f"| **hybride (unaire pour \|v\|=1, puis plans)** | **{E_hyb:.2f}** | "
          f"**{E_hyb:.2f}** |",
          "\n## 3. Seuil de bascule\n",
          "L'unaire gagne si `E[|v|] − 1 < k`, c'est-à-dire `E[|v|] < k + 1` :\n",
          "| Bits k | E[\\|v\\|] uniforme | Coût unaire | Coût positionnel | Gagnant |",
          "|---|---|---|---|---|"]
    for kk in (1, 2, 3, 4, 6, 8):
        E = ((2 ** kk) - 1) / 2
        L.append(f"| {kk} | {E:.1f} | {E-1:.1f} | {kk} | "
                 f"{'**unaire**' if E-1 < kk else 'positionnel'} |")

    L += [f"\nSur ce modèle Q4_0 réel : `E[|v|] = {E_abs:.2f}` → coût de la répétition "
          f"{dens*(addr+E_abs-1):.2f} b/poids contre 4,00 en dense.\n",
          "## Verdict\n",
          "1. **L'idée est exacte** : répéter l'adresse v fois reproduit exactement la valeur",
          "   quantifiée, sans aucune perte au-delà de la quantification d'origine. Le",
          "   raisonnement est juste — et il élimine bien la valeur du stockage.\n",
          "2. **C'est de l'encodage unaire** : le coût est proportionnel à `v`, là où le",
          "   positionnel coûte `log2(v)`. Sur une distribution *uniforme*, l'unaire perd à",
          "   partir de 4 bits (E[|v|] ≈ 7,5 > k+1).\n",
          "3. **Mais les distributions réelles ne sont pas uniformes** : sur ce Q4_0,",
          f"   `E[|v|] = {E_abs:.2f}` seulement — l'échelle du bloc est fixée par son maximum,",
          f"   donc {p1*100:.0f} % des non-nuls valent ±1 et le code dense gaspille ses bits.",
          f"   La répétition gagne alors **même à 4 bits** : {dens*(addr+E_abs-1):.2f} contre 4,00 b/poids.\n",
          "4. **Sa forme hybride est la meilleure** : unaire pour |v|=1 (gratuit — l'adresse",
          "   porte le signe), puis plans binaires au-delà (`popcount` au lieu de `v`) →",
          f"   **{dens*(addr+E_hyb):.2f} b/poids, soit ×{4.0/(dens*(addr+E_hyb)):.2f}**, pour "
          f"{dens*E_hyb:.2f} opération",
          f"   par poids contre {dens:.2f} en dense : quasi gratuit en calcul aussi.\n",
          "5. **Là où l'idée est optimale** : en **binaire** (k=1) et en **ternaire** (BitNet",
          "   b1.58). Tous les non-nuls valent ±1, donc l'adresse *seule* porte la valeur :",
          "   zéro bit de valeur, zéro répétition. C'est exactement l'encodage « listes",
          "   signées » déjà mesuré à 0,39 b/poids.\n",
          "6. **Conséquence matérielle** : le décodeur doit gérer trois cas — ajouter une fois",
          "   (|v|=1), ajouter v fois (unaire), ou ajouter par plans décalés (`popcount`).",
          "   Les trois se réduisent à des additions et des décalages : **aucun DSP**, la",
          "   contrainte du cahier des charges tient.\n",
          "\n> ⚠️ Mesures sur les niveaux quantifiés d'un Q4_0 réel (Qwen2.5-0.5B). `E[|v|]`",
          "> dépend de la recette de quantification : Q4_K_M, avec ses échelles de blocs",
          "> plus fines, donnerait une distribution différente — à mesurer avant de figer",
          "> le format.\n",
          "\n---\n*Généré par `run_value_encoding.py` — Drave.*\n"]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(L), encoding="utf-8")
    print(f"\nRapport écrit : {args.out}")
    g.close()


if __name__ == "__main__":
    main()
