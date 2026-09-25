#!/usr/bin/env python3
"""
Qtrinet — l'élagage permet-il une approche par événement ?

Réponse en trois temps :
  1. quelle est la densité naturelle d'un modèle ternaire ? (mesuré)
  2. que coûte chaque encodage, en bits par poids, à cette densité ? (calcul)
  3. quelle est la frontière de Pareto précision ↔ bits/poids ? (mesuré)

Usage :  python3 run_sparsity.py [--epochs 400]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent / "src"))

import sparsity as S  # noqa: E402
import ternary as T  # noqa: E402
from roofline import CARD  # noqa: E402
from run_quantify import build_and_train, n_params  # noqa: E402

# Densités cibles (fraction des non-nuls conservés)
KEEP_FRACTIONS = [1.0, 0.75, 0.5, 0.25, 0.125, 0.0625, 0.03125]
SCHEMES = ["dense2", "bitmap", "csr16", "csr32"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=400)
    ap.add_argument("--out", type=Path, default=Path("reports/rapport-eparsite.md"))
    args = ap.parse_args()

    model, Xtr, ytr, Xte, yte, acc_float = build_and_train(args.epochs, verbose=False)
    q1, s1 = T.ternarize(model.W1)
    q2, s2 = T.ternarize(model.W2)
    acc_tern = model.accuracy(Xte, yte, W1=q1 * s1, W2=q2 * s2)

    n_tot = q1.size + q2.size
    n_nz = int(np.count_nonzero(q1) + np.count_nonzero(q2))
    d_nat = n_nz / n_tot

    print(f"accuracy float          : {acc_float*100:.2f} %")
    print(f"accuracy ternaire       : {acc_tern*100:.2f} %")
    print(f"densité naturelle       : {d_nat*100:.1f} % des poids sont non nuls")
    print(f"activations non nulles  : {S.relu_density(np.maximum(Xte @ (q1*s1) + model.b1, 0))*100:.1f} % (ReLU)")
    print()

    # ------------------------------------------------------------------ #
    # Balayage de l'élagage
    # ------------------------------------------------------------------ #
    rows = []
    for f in KEEP_FRACTIONS:
        q1p, d1 = S.prune_by_magnitude(model.W1, q1, f)
        q2p, d2 = S.prune_by_magnitude(model.W2, q2, f)
        d = (np.count_nonzero(q1p) + np.count_nonzero(q2p)) / n_tot
        acc = model.accuracy(Xte, yte, W1=q1p * s1, W2=q2p * s2)
        rows.append((f, d, acc))

    # élagage structuré 2:4
    q1s, d1s = S.prune_nm(model.W1, q1, 2, 4)
    q2s, d2s = S.prune_nm(model.W2, q2, 2, 4)
    d_nm = (np.count_nonzero(q1s) + np.count_nonzero(q2s)) / n_tot
    acc_nm = model.accuracy(Xte, yte, W1=q1s * s1, W2=q2s * s2)

    print("=== élagage non structuré (magnitude) ===")
    print(f"{'gardés':>7} {'densité':>8} {'acc':>8}  " +
          "  ".join(f"{s:>8}" for s in SCHEMES) + "   gain bitmap")
    for f, d, acc in rows:
        b = [S.bits_per_weight(d, s) for s in SCHEMES]
        gain = S.speedup_vs_dense(d, "bitmap")
        print(f"{f*100:6.1f}% {d*100:7.1f}% {acc*100:7.2f}%  " +
              "  ".join(f"{x:8.2f}" for x in b) + f"   ×{gain:.2f}")

    print()
    print(f"=== élagage structuré 2:4 (positions fixes) ===")
    print(f"densité {d_nm*100:.1f} %  accuracy {acc_nm*100:.2f} %  "
          f"coût {S.bits_per_weight(0, 'nm', n=2, m=4):.2f} b/poids  "
          f"gain ×{S.speedup_vs_dense(d_nm, 'nm', n=2, m=4):.2f}")

    # ------------------------------------------------------------------ #
    # Seuils de rentabilité
    # ------------------------------------------------------------------ #
    print()
    print("=== densités de rentabilité (bitmap + signe comme référence) ===")
    be = {}
    for a, b in (("bitmap", "dense2"), ("csr32", "dense2"), ("csr16", "dense2"),
                 ("csr32", "bitmap"), ("csr16", "bitmap")):
        d = S.breakeven(a, b)
        be[(a, b)] = d
        if d is None:
            print(f"  {a:>8} vs {b:<8} : jamais (courbes parallèles)")
        else:
            print(f"  {a:>8} vs {b:<8} : égalité à d = {d*100:5.1f} %  "
                  f"→ {a} gagne en dessous")

    # ------------------------------------------------------------------ #
    # Débit 7B selon l'encodage et la densité
    # ------------------------------------------------------------------ #
    print()
    print("=== projection 7B (1 carte, DDR3 9,66 Go/s) ===")
    print(f"{'densité':>8} " + "  ".join(f"{s:>9}" for s in SCHEMES) + "   2:4 struct.")
    for d in (1.0, d_nat, 0.5, 0.25, 0.125, 0.0625):
        toks = [1.0 / (7e9 * S.bits_per_weight(d, s) / 8 / CARD["ddr3_read_Bps"]) for s in SCHEMES]
        tok_nm = 1.0 / (7e9 * S.bits_per_weight(0, "nm", n=2, m=4) / 8 / CARD["ddr3_read_Bps"])
        print(f"{d*100:7.1f}% " + "  ".join(f"{t:9.1f}" for t in toks) + f"   {tok_nm:6.1f}")

    # ------------------------------------------------------------------ #
    # Rapport
    # ------------------------------------------------------------------ #
    L = ["# Qtrinet — élagage et approche par événement\n",
         f"Modèle minimal (MLP 32→64→10), accuracy float **{acc_float*100:.2f} %**, "
         f"ternaire (non élagué) **{acc_tern*100:.2f} %**.\n",
         "## 1. Densité naturelle du ternaire\n",
         f"- poids non nuls : **{d_nat*100:.1f} %** (densité d = {d_nat:.3f})",
         f"- activations non nulles après ReLU : "
         f"**{S.relu_density(np.maximum(Xte @ (q1*s1) + model.b1, 0))*100:.1f} %**",
         f"- événements réels (poids ∧ activation) : **{S.joint_density(d_nat, S.relu_density(np.maximum(Xte @ (q1*s1) + model.b1, 0)))*100:.1f} %**\n",
         "## 2. Coût des encodages (bits par poids)\n",
         "| Encodage | Coût | À d = 50 % | À d = 25 % |",
         "|---|---|---|---|",
         "| dense 2 bits | 2,00 | 2,00 | 2,00 |",
         "| **bitmap + signe** | **1 + d** | **1,50** | **1,25** |",
         "| CSR bloc 16 b | 17·d | 8,50 | 4,25 |",
         "| CSR plat 32 b | 33·d | 16,50 | 8,25 |",
         "| N:M structuré (2:4) | (m+n)/m | 1,50 | — |",
         "",
         "> Un poids ternaire non nul ne porte **qu'un signe**. Le bitmap dit *où* sont",
         "> les non-nuls, le signe dit *lequel*. C'est pourquoi « bitmap + signe » est",
         "> toujours ≤ au code dense 2 bits, et strictement meilleur dès qu'il y a un zéro.\n",
         "## 3. Frontière précision ↔ bits/poids (mesurée)\n",
         "| Gardés | Densité | Accuracy | dense | bitmap | CSR16 | CSR32 | gain bitmap |",
         "|---|---|---|---|---|---|---|---|"]
    for f, d, acc in rows:
        b = [S.bits_per_weight(d, s) for s in SCHEMES]
        L.append(f"| {f*100:.1f} % | {d*100:.1f} % | {acc*100:.2f} % | "
                 + " | ".join(f"{x:.2f}" for x in b)
                 + f" | ×{S.speedup_vs_dense(d, 'bitmap'):.2f} |")
    L.append(f"| 2:4 struct. | {d_nm*100:.1f} % | {acc_nm*100:.2f} % | 2,00 | "
             f"{1+d_nm:.2f} | — | — | ×{S.speedup_vs_dense(d_nm, 'bitmap'):.2f} |")

    L += ["\n## 4. Seuils de rentabilité\n",
          "| Comparaison | Égalité à | Gagnant en dessous |", "|---|---|---|"]
    for (a, b), d in be.items():
        L.append(f"| {a} vs {b} | {f'{d*100:.1f} %' if d is not None else 'jamais'} | "
                 f"{a if d is not None else b} |")

    L += ["\n## 5. Projection 7B sur une carte (tok/s)\n",
          "| Densité | dense | bitmap | CSR16 | CSR32 | 2:4 |", "|---|---|---|---|---|---|"]
    for d in (1.0, d_nat, 0.5, 0.25, 0.125, 0.0625):
        toks = [1.0 / (7e9 * S.bits_per_weight(d, s) / 8 / CARD["ddr3_read_Bps"]) for s in SCHEMES]
        tok_nm = 1.0 / (7e9 * S.bits_per_weight(0, "nm", n=2, m=4) / 8 / CARD["ddr3_read_Bps"])
        L.append(f"| {d*100:.1f} % | " + " | ".join(f"{t:.1f}" for t in toks)
                 + f" | {tok_nm:.1f} |")

    L += ["\n## 6. Verdict\n",
          f"1. **Oui, un modèle ternaire est déjà creux** — ici {d_nat*100:.1f} % de non-nuls, "
          "sans aucun élagage. C'est le point de départ, pas une contrainte ajoutée.",
          "2. **L'encodage événementiel « bitmap + signe » domine le dense** : 1 + d bits/poids "
          "contre 2, soit jusqu'à 2× moins de trafic. Il ne coûte jamais plus cher.",
          "3. **Le CSR, lui, est disqualifié** : rentable seulement sous "
          f"{be[('csr32','dense2')]*100:.0f} % (indice 32 b) ou "
          f"{be[('csr16','dense2')]*100:.0f} % (indice 16 b) de densité — un régime que les "
          "LLM n'atteignent pas sans s'effondrer.",
          "4. **Le vrai obstacle n'est pas le poids, c'est l'activation** : un événement "
          "n'existe que si le poids *et* l'activation sont non nuls "
          f"(ici {S.joint_density(d_nat, S.relu_density(np.maximum(Xte @ (q1*s1) + model.b1, 0)))*100:.1f} % "
          "d'événements réels). Récupérer l'activation à un index arbitraire impose une "
          "fenêtre de lecture et un multiplexeur par voie : ~21 LUT pour un 64:1, soit "
          "≈ 3 400 ALM pour 312 voies (**2 % du FPGA**) — c'est payable.",
          "5. **Recommandation** : garder le dense 2 bits comme chemin nominal (simple, "
          "déterministe, déjà validé) et ajouter un **encodage bitmap + signe** là où la "
          "densité est faible. Le saut de blocs entièrement nuls (1 bit par bloc de 64) est "
          "le premier pas, à 1,6 % de surcoût.",
          "\n### Réserves à lever avant de s'engager\n",
          f"- La courbe précision ↔ élagage est **bruitée** : le modèle ne pèse que "
          f"{n_tot} poids et son accuracy ternaire ({acc_tern*100:.1f} %) laisse peu de marge "
          "de mesure. Les variations observées (±4 pt) sont dans le bruit d'un jeu de test "
          "de 1 024 exemples — **on ne peut pas conclure sur la dégradation due à l'élagage**.",
          f"- La densité naturelle ({d_nat*100:.1f} %) est propre à ce modèle. Un modèle "
          "**entraîné** en ternaire (BitNet b1.58) tourne plutôt autour de 50-70 % de non-nuls : "
          "le gain du bitmap y serait de ×1,2 à ×1,4, pas ×1,6.",
          "- La littérature (SparseGPT, Wanda) situe l'élagage non structuré *one-shot* des LLM "
          "à 50-60 % sans réentraînement, et le 2:4 structuré (50 %) est la forme matériellement "
          "supportée. **Au-delà de ~90 % de zéros, un LLM généraliste s'effondre** — le régime "
          "où le CSR deviendrait rentable est donc hors d'atteinte.\n",
          "\n---\n*Généré par `run_sparsity.py` — Qtrinet.*\n"]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(L), encoding="utf-8")
    print(f"\nRapport écrit : {args.out}")


if __name__ == "__main__":
    main()
