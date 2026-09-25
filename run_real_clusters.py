#!/usr/bin/env python3
"""
Qtrinet — un vrai modèle expose-t-il déjà ses grappes ?

Test : on partitionne la dimension cachée en G grappes, puis on mesure la
**spécialisation afférente** de chaque neurone :

    part de la masse d'entrée d'un neurone venant de sa grappe dominante

  - 1/G  → aucune structure (chaque neurone lit toutes les grappes uniformément)
  - > 1/G → grappes naturelles : le neurone lit surtout la sienne
  - → 1  → structure parfaite (bloc diagonal, sous-modèles disjoints)

On mesure aussi la dividende d'encodage : réordonner les colonnes par grappe
raccourcit-il les écarts entre non-nuls (donc le coût des positions) ?

Usage :  python3 run_real_clusters.py [--model models/xxx.gguf] [--groups 4 8]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent / "src"))

import encoding as E  # noqa: E402
from gguf_min import GGUF  # noqa: E402


# --------------------------------------------------------------------------- #
# k-means minimal (numpy)
# --------------------------------------------------------------------------- #


def kmeans(X: np.ndarray, k: int, iters: int = 30, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    # k-means++ simplifié
    C = [X[rng.integers(len(X))]]
    for _ in range(k - 1):
        d2 = np.min(((X[:, None, :] - np.array(C)[None]) ** 2).sum(-1), axis=1)
        p = d2 / d2.sum() if d2.sum() > 0 else np.ones(len(X)) / len(X)
        C.append(X[rng.choice(len(X), p=p)])
    C = np.array(C, dtype=np.float32)
    lab = np.zeros(len(X), dtype=np.int32)
    for _ in range(iters):
        d = ((X[:, None, :] - C[None]) ** 2).sum(-1)
        new = d.argmin(axis=1).astype(np.int32)
        if np.array_equal(new, lab):
            break
        lab = new
        for g in range(k):
            m = lab == g
            if m.any():
                C[g] = X[m].mean(axis=0)
    return lab


def afferent_specialization(W: np.ndarray, groups: np.ndarray) -> tuple[float, float]:
    """Pour chaque ligne (neurone) de W, part de sa masse d'entrée venant de
    chaque grappe. Retourne (moyenne du max, part de la diagonale)."""
    G = groups.max() + 1
    mass = np.abs(W)
    per_group = np.stack([mass[:, groups == g].sum(axis=1) for g in range(G)], axis=1)
    tot = per_group.sum(axis=1, keepdims=True)
    tot[tot == 0] = 1.0
    share = per_group / tot
    # grappe assignée à chaque neurone = sa grappe dominante
    dom = share.argmax(axis=1)
    best = share.max(axis=1).mean()
    diag = share[np.arange(len(dom)), dom].mean()
    return float(best), float(diag)


def mean_gap(q: np.ndarray) -> float:
    gaps = []
    for r in range(q.shape[0]):
        pos = np.flatnonzero(q[r])
        if pos.size > 1:
            gaps.append(np.diff(pos).mean())
    return float(np.mean(gaps)) if gaps else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", type=Path,
                    default=Path("models/Qwen2.5-0.5B-Q8_0.gguf"))
    ap.add_argument("--groups", type=int, nargs="+", default=[4, 8])
    ap.add_argument("--layers", type=int, default=4, help="nb de couches analysées")
    ap.add_argument("--out", type=Path, default=Path("reports/rapport-modele-reel.md"))
    args = ap.parse_args()

    g = GGUF(args.model)
    arch = g.arch()
    n_layer = int(g.cfg("block_count", 0))
    n_head = int(g.cfg("attention.head_count", 0))
    n_kv = int(g.cfg("attention.head_count_kv", 0))
    hidden = int(g.cfg("embedding_length", 0))
    inter = int(g.cfg("feed_forward_length", 0))
    print(f"Modèle : {arch}  —  {n_layer} couches, hidden {hidden}, "
          f"intermédiaire {inter}, {n_head} têtes / {n_kv} KV (GQA)")
    print(f"Tenseurs : {g.n_tensors}\n")

    # ---------------------------------------------------------------- tenseurs
    names = list(g.tensors)
    show = [n for n in names if n.startswith("blk.0.") and "bias" not in n]
    print("Tenseurs de la couche 0 :")
    for n in show:
        print(f"  {n:<28} {g.tensors[n].shape}  type={g.tensors[n].ttype}")

    # ------------------------------------------------------- parcimonie brute
    print("\n=== 1. Parcimonie intrinsèque (avant tout élagage) ===")
    print(f"{'tenseur':<24} {'|w|<5%max':>10} {'|w|<10%max':>11} {'|w|<20%max':>11}")
    spars = {}
    for n in show:
        W = g.dequant(n)
        mx = np.abs(W).max()
        fr = [float((np.abs(W) < t * mx).mean()) for t in (0.05, 0.10, 0.20)]
        spars[n] = fr
        print(f"  {n:<22} {fr[0]*100:9.1f}% {fr[1]*100:10.1f}% {fr[2]*100:10.1f}%")

    # ------------------------------- grappes de la dimension cachée (features)
    print("\n=== 2. Grappes afférentes/efférentes de la dimension cachée ===")
    # IMPORTANT : les grappes sont apprises sur la SEULE couche 0, puis testées
    # sur les couches 1..n-1 — sinon le test est circulaire.
    gate0 = g.dequant("blk.0.ffn_gate.weight")
    down0 = g.dequant("blk.0.ffn_down.weight")
    fg = gate0 / (np.linalg.norm(gate0, axis=0, keepdims=True) + 1e-9)
    fd = down0 / (np.linalg.norm(down0, axis=1, keepdims=True) + 1e-9)
    F = np.concatenate([fg.T[:, :256], fd[:, :256]], axis=1).astype(np.float32)
    F /= (np.linalg.norm(F, axis=1, keepdims=True) + 1e-9)
    print(f"  features par unité cachée (couche 0) : {F.shape[1]} dimensions")
    print("  → grappes apprises sur la couche 0, TESTÉES sur les couches 1.."
          f"{min(args.layers, n_layer)-1} (validation croisée)")

    results = {}
    for G in args.groups:
        lab = kmeans(F, G, seed=0)
        sizes = np.bincount(lab, minlength=G)
        print(f"\n  --- {G} grappes (tailles {list(sizes)}) ---")
        print(f"  {'tenseur':<24} {'spécialisation':>15} {'diagonale':>10} {'réf 1/G':>9}")
        rng = np.random.default_rng(1)
        rand_lab = rng.permutation(lab)          # référence : grappes aléatoires
        ins, oos, rnd = [], [], []
        for L in range(min(args.layers, n_layer)):
            for n in (f"blk.{L}.ffn_gate.weight", f"blk.{L}.ffn_down.weight",
                      f"blk.{L}.attn_q.weight", f"blk.{L}.attn_output.weight"):
                if n not in g.tensors:
                    continue
                W = g.dequant(n)
                if W.shape[1] != hidden:
                    continue
                b, d = afferent_specialization(W, lab)
                _, dr = afferent_specialization(W, rand_lab)
                (ins if L == 0 else oos).append((n, b, d))
                rnd.append(dr)
        m_in = float(np.mean([r[1] for r in ins])) if ins else float("nan")
        m_oos = float(np.mean([r[1] for r in oos])) if oos else float("nan")
        m_rnd = float(np.mean(rnd))
        print(f"  {'couche 0 (apprise)':<26} {m_in*100:12.1f}%")
        print(f"  {'couches 1+ (TEST)':<26} {m_oos*100:12.1f}%")
        print(f"  {'grappes aléatoires':<26} {m_rnd*100:12.1f}%")
        print(f"  → rapport test/aléatoire : {m_oos/m_rnd:.2f}x")
        results[G] = (m_in, m_oos, m_rnd)

    # ---------------------------------------------- dividende d'encodage
    print("\n=== 3. Dividende d'encodage : réordonner les colonnes par grappe ===")
    G = args.groups[0]
    lab = kmeans(F, G, seed=0)
    order = np.argsort(lab, kind="stable")
    print(f"{'tenseur':<24} {'seuil':>6} {'densité':>8} {'écart natif':>12} "
          f"{'écart groupé':>13} {'gain':>7}")
    enc_rows = []
    for n in (f"blk.0.ffn_gate.weight", f"blk.0.ffn_down.weight"):
        W = g.dequant(n)
        for pct in (0.05, 0.10, 0.20):
            thr = np.quantile(np.abs(W), 1 - pct)
            q = (np.abs(W) >= thr).astype(np.int8)
            g_nat = mean_gap(q)
            g_grp = mean_gap(q[:, order]) if W.shape[1] == hidden else g_nat
            gain = g_nat / g_grp if g_grp and np.isfinite(g_grp) else float("nan")
            enc_rows.append((n, pct, float(q.mean()), g_nat, g_grp, gain))
            print(f"  {n:<22} {pct*100:5.0f}% {q.mean()*100:7.1f}% {g_nat:12.2f} "
                  f"{g_grp:13.2f} {gain:6.2f}x")

    # ------------------------------- réserve : structure explicite GQA
    print("\n=== 4. Structure explicite : GQA ===")
    q = g.dequant("blk.0.attn_q.weight")
    hd = q.shape[0] // n_head if n_head else 0
    print(f"  attn_q : {q.shape} → {n_head} têtes de {hd} dimensions")
    if hd:
        heads = q.reshape(n_head, hd, -1)
        en = (heads ** 2).sum(axis=(1, 2))
        print(f"  énergie par tête : min {en.min()/en.sum()*100:.1f}%  "
              f"max {en.max()/en.sum()*100:.1f}%  (uniforme = {100/n_head:.1f}%)")
        # similarité entre têtes (les têtes se ressemblent-elles ?)
        M = heads.reshape(n_head, -1)
        M = M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)
        S = M @ M.T
        off = S[~np.eye(n_head, dtype=bool)]
        print(f"  similarité entre têtes : moyenne {off.mean():.3f} "
              f"(max {off.max():.3f}, min {off.min():.3f})")

    # ------------------------------------------------------------- rapport
    L = [f"# Qtrinet — le modèle réel expose-t-il ses grappes ?\n",
         f"Modèle analysé : **{arch}**, {n_layer} couches, hidden {hidden}, "
         f"intermédiaire {inter}, {n_head} têtes / {n_kv} KV (GQA).\n",
         "## 1. Parcimonie intrinsèque\n",
         "| Tenseur (couche 0) | \\|w\\|<5 % max | <10 % | <20 % |", "|---|---|---|---|"]
    for n, fr in spars.items():
        L.append(f"| {n} | {fr[0]*100:.1f} % | {fr[1]*100:.1f} % | {fr[2]*100:.1f} % |")

    L += ["\n## 2. Spécialisation afférente de la dimension cachée\n",
          "Part de la masse d'entrée d'un neurone venant de sa grappe dominante.",
          f"**1/G = pas de structure, 1 = blocs disjoints.**\n",
          "| Grappes G | Couche 0 (apprise) | Couches 1+ (test) | Grappes aléatoires | Test/aléatoire |",
          "|---|---|---|---|---|"]
    for G, (mi, mo, mr) in results.items():
        L.append(f"| {G} | {mi*100:.1f} % | {mo*100:.1f} % | {mr*100:.1f} % | "
                 f"**{mo/mr:.2f}×** |")

    L += ["\n## 3. Dividende d'encodage (réordonnancement par grappe)\n",
          "| Tenseur | Seuil | Densité | Écart naturel | Écart groupé | Gain |",
          "|---|---|---|---|---|---|"]
    for n, pct, d, gn, gg, gain in enc_rows:
        L.append(f"| {n} | {pct*100:.0f} % | {d*100:.1f} % | {gn:.2f} | {gg:.2f} | {gain:.2f}× |")

    L += ["\n## 4. Structure explicite : GQA\n",
          f"- `attn_q` : {q.shape}, {n_head} têtes de {hd} dimensions",
          f"- énergie par tête : {en.min()/en.sum()*100:.1f} % à {en.max()/en.sum()*100:.1f} % "
          f"(uniforme = {100/n_head:.1f} %)" if hd else "",
          f"- similarité entre têtes : {off.mean():.3f} en moyenne\n" if hd else "",
          "\n---\n*Généré par `run_real_clusters.py` — Qtrinet.*\n"]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(x for x in L if x != ""), encoding="utf-8")
    print(f"\nRapport écrit : {args.out}")
    g.close()


if __name__ == "__main__":
    main()
