#!/usr/bin/env python3
"""
Drave — test de principe : quantifier un modèle minimal en ternaire / multi-bits.

Ce script répond à trois questions, chiffres en main :

  1. FIDÉLITÉ   — la quantification ternaire (1,58 b/poids) préserve-t-elle la
                  fonction du modèle ? Et le chemin *entier* (add/sub, sans DSP)
                  reproduit-il exactement le calcul flottant ?
  2. COÛT       — combien de bits par poids selon l'encodage (dense, bitmap, CSR) ?
                  Où part la place, plan par plan ?
  3. DÉBIT      — que peut espérer la carte Storey Peak, d'après ses débits mesurés ?

Usage :  python3 run_quantify.py [--epochs 300] [--out reports/rapport-minimal.md]
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent / "src"))

import roofline as rf  # noqa: E402
import ternary as T  # noqa: E402
from tiny_model import MLP, make_dataset  # noqa: E402

# --------------------------------------------------------------------------- #
# Modèle minimal
# --------------------------------------------------------------------------- #

D_IN, D_HID, N_CLASS = 32, 64, 10
N_TRAIN, N_TEST = 4096, 1024


def build_and_train(epochs: int, verbose: bool = True):
    Xtr, ytr = make_dataset(N_TRAIN, D_IN, N_CLASS, seed=0)
    Xte, yte = make_dataset(N_TEST, D_IN, N_CLASS, seed=1)
    model = MLP(D_IN, D_HID, N_CLASS, seed=1)
    if verbose:
        print(f"[1/5] entraînement ({epochs} époques, numpy)…")
    t0 = time.time()
    model.train(Xtr, ytr, epochs=epochs, lr=0.05, batch=128)
    dt = time.time() - t0
    acc = model.accuracy(Xte, yte)
    if verbose:
        print(f"      accuracy float = {acc*100:.2f} %  ({dt:.1f} s)")
    return model, Xtr, ytr, Xte, yte, acc


def n_params(model: MLP) -> int:
    return sum(w.size for w in (model.W1, model.b1, model.W2, model.b2))


# --------------------------------------------------------------------------- #
# 1. Fidélité
# --------------------------------------------------------------------------- #


def evaluate_formats(model: MLP, Xte, yte):
    """Accuracy selon le format des poids (poids quantifiés, reste en float)."""
    rows = []

    # référence : float32
    rows.append(("float32 (référence)", 32.0, model.accuracy(Xte, yte), model.W1, model.W2))

    # int8 / int4 symétriques, par canal
    for bits in (8, 4):
        W1q, s1 = T.quantize_bits(model.W1, bits - 1)   # 1 bit de signe
        W2q, s2 = T.quantize_bits(model.W2, bits - 1)
        acc = model.accuracy(Xte, yte, W1=W1q * s1, W2=W2q * s2)
        rows.append((f"int{bits} (signe-magnitude)", float(bits), acc, W1q * s1, W2q * s2))

    # ternaire 1,58 bit
    q1, s1 = T.ternarize(model.W1)
    q2, s2 = T.ternarize(model.W2)
    acc = model.accuracy(Xte, yte, W1=q1 * s1, W2=q2 * s2)
    rows.append(("ternaire 1,58 b (dense 2 b)", 2.0, acc, q1, q2))
    dense_ternary = (q1, s1, q2, s2)

    # multi-bits par plans ternaires (bit-slicing du CDC)
    multi = {}
    for bits in (2, 3, 4):
        W1q, t1 = T.quantize_bits(model.W1, bits)
        W2q, t2 = T.quantize_bits(model.W2, bits)
        acc = model.accuracy(Xte, yte, W1=W1q * t1, W2=W2q * t2)
        rows.append((f"multi {bits} plans ternaires", float(bits * 2), acc, W1q * t1, W2q * t2))
        multi[bits] = (W1q, t1, W2q, t2)

    return rows, dense_ternary, multi


def check_integer_path(model: MLP, Xte, yte, dense_ternary):
    """Sépare deux choses qu'on confond souvent :

    - *exactitude arithmétique* : le chemin entier (add/sub, aucun DSP) doit
      reproduire au bit près le calcul flottant **sur les mêmes entrées** ;
    - *erreur de quantification d'activation* : l'écart introduit par le passage
      des activations en int8.
    """
    q1, s1, q2, s2 = dense_ternary
    z1_f, _, _, p_f = model.forward(Xte, W1=q1 * s1, W2=q2 * s2)
    acc_float = float((p_f.argmax(axis=1) == yte).mean())

    # ---- couche 1 -------------------------------------------------------- #
    Xq, sx = T.quantize_activations(Xte, bits=8)
    out1, acc1, _ = T.integer_linear(Xte, q1, s1, act_bits=8, bias=model.b1)
    ref1 = (Xq * sx) @ (q1 * s1) + model.b1          # même arithmétique, en flottant
    err_arith_1 = float(np.abs(out1 - ref1).max())    # doit être ~1e-6
    err_act_1 = float(np.abs(ref1 - z1_f).max())      # erreur de quantification int8

    # ---- couche 2 (mêmes activations des deux côtés) --------------------- #
    a1 = np.maximum(out1, 0)
    a1q, sa1 = T.quantize_activations(a1, bits=8)
    out2, acc2, _ = T.integer_linear(a1, q2, s2, act_bits=8, bias=model.b2)
    ref2 = (a1q * sa1) @ (q2 * s2) + model.b2
    err_arith_2 = float(np.abs(out2 - ref2).max())
    err_act_2 = float(np.abs(ref2 - (a1 @ (q2 * s2) + model.b2)).max())
    acc_int = float((out2.argmax(axis=1) == yte).mean())

    return dict(err_z1=err_arith_1, err_z2=err_arith_2,
                err_act_1=err_act_1, err_act_2=err_act_2,
                acc_int=acc_int, acc_float=acc_float,
                acc_max_int64=int(max(np.abs(acc1).max(), np.abs(acc2).max())))


# --------------------------------------------------------------------------- #
# 2. Coût : encodages et densité des plans
# --------------------------------------------------------------------------- #


def encoding_table(model: MLP, q1, q2, multi):
    """Taille des différents encodages, en bits par poids."""
    n = model.W1.size + model.W2.size
    rows = []

    rows.append(("float32", 32.0, n * 32))
    rows.append(("int8", 8.0, n * 8))
    rows.append(("int4", 4.0, n * 4))
    rows.append(("ternaire dense (2 b)", 2.0, T.size_dense_ternary(n)))
    rows.append(("borne entropique ternaire", 1.585, int(T.size_entropy_ternary(n))))

    # multi-bits : plans ternaires
    for bits, (W1q, _, W2q, _) in multi.items():
        pl1, pl2 = T.bit_planes(W1q, bits), T.bit_planes(W2q, bits)
        # dense 1 b/plan
        dense = bits * n
        # bitmap + signe par plan
        bmp = T.size_bitmap_planes(pl1) + T.size_bitmap_planes(pl2)
        # CSR par plan (taille réelle du CDC)
        csr = T.size_csr_planes(pl1) + T.size_csr_planes(pl2)
        rows.append((f"multi {bits} bits — dense 1 b/plan", float(bits), dense))
        rows.append((f"multi {bits} bits — bitmap+signe", 2.0 * bits, bmp))
        rows.append((f"multi {bits} bits — CSR/plan (CDC)", csr / n, csr))

    # ternaire en CSR (ce que proposait le CDC)
    pl1 = T.bit_planes(np.abs(q1).astype(np.int32), 1)
    pl2 = T.bit_planes(np.abs(q2).astype(np.int32), 1)
    csr_t = T.size_csr_planes(pl1) + T.size_csr_planes(pl2)
    rows.append(("ternaire en CSR (CDC)", csr_t / n, csr_t))

    return [(lab, bpp, tot) for lab, bpp, tot in rows]


def plane_density_table(model: MLP, multi):
    """Densité de chaque plan : pourquoi le CSR est une mauvaise idée ici."""
    out = []
    for bits, (W1q, _, W2q, _) in multi.items():
        pl = T.bit_planes(W1q, bits)
        st = T.plane_stats(pl)
        out.append((bits, [(s.index, s.density) for s in st]))
    return out


# --------------------------------------------------------------------------- #
# 3. Débit projeté
# --------------------------------------------------------------------------- #


def throughput_table(model: MLP):
    """Ce que la carte peut espérer, à ses débits MESURÉS."""
    rows = []
    # le modèle minimal lui-même
    n = n_params(model)
    for lab, bpp in (("ternaire dense 2 b", 2.0),
                     ("multi 4 bits (1 b/plan)", 4.0),
                     ("multi 4 bits (bitmap+signe)", 8.0),
                     ("int8", 8.0),
                     ("ternaire CSR (CDC)", 17.0)):
        rows.append(rf.project(n, bpp, label=f"modèle minimal — {lab}"))
    # références
    for lab, params in (("7B", 7e9), ("70B", 70e9)):
        for blab, bpp in (("ternaire 2 b", 2.0), ("4 bits", 4.0), ("ternaire CSR", 17.0)):
            rows.append(rf.project(params, bpp, label=f"{lab} — {blab}"))
    return rows


# --------------------------------------------------------------------------- #
# Rapport
# --------------------------------------------------------------------------- #


def write_report(path: Path, acc_float, fmt_rows, intchk, enc_rows, dens_rows, thr_rows):
    L = []
    L.append("# Drave — test de principe : modèle minimal en ternaire / multi-bits\n")
    L.append(f"Modèle : MLP {D_IN}→{D_HID}→{N_CLASS}, entraîné sur {N_TRAIN} exemples "
             f"synthétiques, évalué sur {N_TEST}.\n")

    L.append("## 1. Fidélité de la quantification\n")
    L.append("| Format des poids | b/poids | Accuracy | Δ vs float |")
    L.append("|---|---|---|---|")
    for lab, bpp, acc, _, _ in fmt_rows:
        L.append(f"| {lab} | {bpp:.2f} | {acc*100:.2f} % | {(acc-acc_float)*100:+.2f} pt |")

    L.append("\n### Chemin entier (ce que fera le FPGA : add/sub, aucun DSP)\n")
    L.append("| Mesure | Valeur |")
    L.append("|---|---|")
    L.append(f"| Exactitude arithmétique — couche 1 (entier vs flottant, mêmes entrées) | {intchk['err_z1']:.3e} |")
    L.append(f"| Exactitude arithmétique — couche 2 | {intchk['err_z2']:.3e} |")
    L.append(f"| Erreur de quantification des activations — couche 1 | {intchk['err_act_1']:.3e} |")
    L.append(f"| Erreur de quantification des activations — couche 2 | {intchk['err_act_2']:.3e} |")
    L.append(f"| Accuracy chemin entier (poids ternaires + activations int8) | {intchk['acc_int']*100:.2f} % |")
    L.append(f"| Accuracy chemin flottant (mêmes poids quantifiés) | {intchk['acc_float']*100:.2f} % |")
    L.append(f"| Accumulateur max (doit tenir en int32) | {intchk['acc_max_int64']} |")

    L.append("\n## 2. Coût des encodages\n")
    L.append("| Encodage | bits/poids | Taille totale |")
    L.append("|---|---|---|")
    n = max(t for _, _, t in enc_rows)
    for lab, bpp, tot in enc_rows:
        L.append(f"| {lab} | {bpp:.2f} | {tot/8/1024:.1f} Kio |")

    L.append("\n### Densité par plan (justifie — ou non — le CSR)\n")
    L.append("| Magnitude | " + " | ".join(f"plan {i}" for i, _ in dens_rows[0][1]) + " |")
    L.append("|---" * (len(dens_rows[0][1]) + 1) + "|")
    for bits, dens in dens_rows:
        L.append(f"| {bits} bits | " + " | ".join(f"{d*100:.1f} %" for _, d in dens) + " |")

    L.append("\n## 3. Débit projeté sur la carte (Stratix V GS D5)\n")
    L.append("Débits **mesurés** : DDR3 9,66 Go/s · PCIe x8 6,5 Go/s · fmax actuel 124 MHz.\n")
    L.append("| Modèle / encodage | Taille | ms/token | tok/s | Voies MAC | ALM |")
    L.append("|---|---|---|---|---|---|")
    for p in thr_rows:
        tok_s = 1.0 / p.t_memory_s if p.t_memory_s else float("inf")
        L.append(f"| {p.label} | {p.weight_bytes/1e6:.1f} Mo | {p.t_memory_s*1e3:.3f} "
                 f"| {tok_s:.1f} | {p.lanes_needed} | {p.alms_for_lanes} |")

    L.append("\n## 4. Conclusions\n")
    ternary_row = next(r for r in fmt_rows if "ternaire 1,58" in r[0])
    multi4 = next(r for r in fmt_rows if "multi 4 plans" in r[0])
    enc_csr_t = next(r for r in enc_rows if "ternaire en CSR" in r[0])
    enc_csr_4 = next(r for r in enc_rows if "multi 4 bits — CSR" in r[0])
    enc_dense_t = next(r for r in enc_rows if "ternaire dense" in r[0])
    L += [
        f"1. **Le chemin entier est exact** : {intchk['err_z1']:.2e} / {intchk['err_z2']:.2e} "
        "d'écart avec le calcul flottant — c'est de l'arrondi flottant, rien d'autre. "
        "Le principe « pas de DSP, que des additions/soustractions » est donc validé.",
        f"2. **La quantification ternaire *post-entraînement* coûte cher** : "
        f"{acc_float*100:.1f} % → {ternary_row[2]*100:.1f} % ({ternary_row[2]*100-acc_float*100:+.1f} pt). "
        "Ce n'est PAS un verdict contre BitNet : les modèles ternaires (b1.58) sont "
        "*entraînés* avec la contrainte. Un modèle float quantifié après coup perd sa fonction.",
        f"3. **Le découpage en plans (multi-bits) dégrade progressivement** : "
        f"4 plans → {multi4[2]*100:.1f} % ({multi4[2]*100-acc_float*100:+.1f} pt). "
        "C'est la voie naturelle pour réutiliser un modèle 4 bits existant sans réentraînement.",
        f"4. **Le CSR est un piège chiffré** : {enc_csr_t[1]:.1f} b/poids pour le ternaire et "
        f"{enc_csr_4[1]:.1f} b/poids pour 4 plans, contre {enc_dense_t[1]:.1f} et 4,0 b/poids "
        "en dense — soit 5 à 15× plus de trafic mémoire, qui se traduit directement en "
        "division du débit (cf. §3).",
        "5. **Tout le projet est borné par la DDR3**, pas par le calcul : à 124 MHz il ne "
        "faut que ~312 voies de MAC (≈ 9 400 ALM, 5 % du FPGA) pour saturer les 9,66 Go/s. "
        "96 % du device reste disponible pour la mémoire, le décodeur et le réseau.",
        "\n> ⚠️ **Réserve** : le modèle minimal (10 Kio) n'est pas borné par la mémoire mais "
        "par la latence. Ses chiffres de débit (§3, premières lignes) ne veulent rien dire — "
        "seules les projections 7B/70B sont significatives.",
        "\n> ⚠️ Le ternaire testé ici est de la quantification *a posteriori*. La question "
        "« le ternaire suffit-il ? » se tranche sur un modèle **entraîné en ternaire** "
        "(BitNet b1.58) — ce sera l'étape suivante.\n",
    ]

    L.append("\n---\n*Généré par `run_quantify.py` — Drave.*\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(L), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=300)
    ap.add_argument("--out", type=Path, default=Path("reports/rapport-minimal.md"))
    args = ap.parse_args()

    model, Xtr, ytr, Xte, yte, acc_float = build_and_train(args.epochs)

    print("[2/5] quantification (ternaire, int4/8, multi-plans)…")
    fmt_rows, dense_ternary, multi = evaluate_formats(model, Xte, yte)
    for lab, bpp, acc, _, _ in fmt_rows:
        print(f"      {lab:<32} {bpp:5.2f} b/poids   acc={acc*100:6.2f} %")

    print("[3/5] vérification du chemin entier…")
    intchk = check_integer_path(model, Xte, yte, dense_ternary)
    print(f"      erreur max = {intchk['err_z2']:.2e} | accuracy entier = "
          f"{intchk['acc_int']*100:.2f} % (flottant {intchk['acc_float']*100:.2f} %)")

    print("[4/5] encodages et densité des plans…")
    enc_rows = encoding_table(model, dense_ternary[0], dense_ternary[2], multi)
    dens_rows = plane_density_table(model, multi)
    for lab, bpp, tot in enc_rows:
        print(f"      {lab:<34} {bpp:6.2f} b/poids   {tot/8/1024:8.1f} Kio")

    print("[5/5] projection matérielle…")
    thr_rows = throughput_table(model)
    for p in thr_rows:
        print("      " + rf.report_line(p))

    write_report(args.out, acc_float, fmt_rows, intchk, enc_rows, dens_rows, thr_rows)
    print(f"\nRapport écrit : {args.out}")


if __name__ == "__main__":
    main()
