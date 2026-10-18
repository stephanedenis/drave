#!/usr/bin/env python3
"""style_traducteur.py — LE STYLE DU TRADUCTEUR EST-IL LISIBLE ? ET LE SENS SURVIT-IL AU STYLE ?

LA TROISIÈME DISTINCTION DE LA SÉRIE ✓✓, après les langues (448 ✓) et les variantes (7 ✓) : **le style** ✗✓.
Deux **traductions anglaises de la MÊME œuvre** (L'Odyssée : Samuel Butler ✓ et Alexander Pope ✓) partagent la
langue et le contenu ✓ — elles ne diffèrent que par le **style du traducteur** ✓✓. C'est le dispositif le plus
propre pour cette question ✓.

TROIS MESURES DANS LE MÊME OUTIL ✗ :
  · **le style est-il lisible ?** ✓ : un classifieur binaire (traducteur A contre B), entraîné sur la moitié des
    segments, testé sur l'autre moitié ✓✓ — hasard 50 % ✓ ;
  · **le sens survit-il au style ?** ✓✓ : le segment *i* de A se retrouve-t-il dans B ? ✓ (retrieval, hasard
    1/N ✓) — c'est la **traduction** au sens de « même contenu, autre surface » ✓ ;
  · **le contrôle négatif** ✓✓ : étiquettes mélangées (le style doit retomber à 50 %) et segments mélangés (le
    retrieval doit retomber au hasard ✓).

⚠️ CE QU'IL NE DIT PAS ✗ : la découpe est **proportionnelle** ✓✗ (comme pour Verne le 17/10 ✓) — deux éditions
peuvent dériver ✓ ; on le verra au retrieval ✓. Et deux traductions ne diffèrent pas QUE par le style ✗ : Pope
traduit en vers ✓, Butler en prose ✓✓ — le « style » mesuré est en partie le **vers contre la prose** ✓.

Usage :
  python3 tools/style_traducteur.py --hf <Qwen> --tokeniseur --a <butler.txt> --b <pope.txt> --n 32
"""
from __future__ import annotations
import argparse, pathlib, re, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from udhr_commun import charger_modele, etats_par_couche
from udhr_commun import entrainer


def segments(chemin, n, longueur):
    t = pathlib.Path(chemin).read_text(errors="ignore")
    pas = len(t) // n
    out = []
    for i in range(n):
        seg = t[i * pas:(i + 1) * pas]
        d = max(0, len(seg) // 2 - longueur // 2)
        out.append(seg[d:d + longueur])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--a", required=True, help="traduction A (Butler)")
    ap.add_argument("--b", required=True, help="traduction B (Pope)")
    ap.add_argument("--n", type=int, default=32)
    ap.add_argument("--longueur", type=int, default=300)
    ap.add_argument("--couche", type=int, default=16)
    ap.add_argument("--tokeniseur", action="store_true")
    ap.add_argument("--mode", choices=["proportionnel", "livres"], default="proportionnel",
                    help="« livres » : découper sur les CHANTS (BOOK I, II…) ✓✓ — indispensable quand les "
                         "traductions ne se correspondent pas au caractère près ✗ (vers contre prose ✓)")
    ap.add_argument("--temoin", action="store_true")
    a = ap.parse_args()
    m, encoder, device = charger_modele(a.hf, tokeniseur=a.tokeniseur)
    if a.mode == "livres":
        def livres(chemin):
            t = pathlib.Path(chemin).read_text(errors="ignore")
            parts = re.split(r"(?im)^\s*BOOK\s+[IVXLC]+\.?\s*$", t)
            parts = [x for x in parts[1:] if len(x) > 2000]
            out = []
            for x in parts:
                d = max(0, len(x) // 2 - a.longueur // 2)
                out.append(x[d:d + a.longueur])
            return out
        segs_a, segs_b = livres(a.a), livres(a.b)
        print(f"  chants : {len(segs_a)} (A) · {len(segs_b)} (B)")
    else:
        segs_a, segs_b = segments(a.a, a.n, a.longueur), segments(a.b, a.n, a.longueur)
    def etats(segs):
        out = []
        for s in segs:
            ids = encoder(s, a.longueur)
            if len(ids) < 8:
                out.append(None); continue
            out.append(etats_par_couche(m, ids, [a.couche], "moyenne")[a.couche][None, :])
        return np.concatenate([x for x in out if x is not None])
    A, B = etats(segs_a), etats(segs_b)
    n = min(len(A), len(B), a.n)
    A, B = A[:n], B[:n]
    print(f"  {n} segments par traduction · couche {a.couche} · longueur {a.longueur}")
    # 1) le style est-il lisible ? ✓
    ma = n // 2
    X = np.concatenate([A, B]); y = np.r_[np.ones(len(A)), np.zeros(len(B))]
    Xtr = np.concatenate([A[:ma], B[:ma]]); ytr = np.r_[np.ones(ma), np.zeros(ma)]
    Xte = np.concatenate([A[ma:], B[ma:]]); yte = np.r_[np.ones(len(A) - ma), np.zeros(len(B) - ma)]
    if a.temoin:
        rng = np.random.RandomState(0); ytr = rng.permutation(ytr); yte = rng.permutation(yte)
    pred, top5, _ = entrainer(Xtr, ytr, Xte, 2)
    acc = 100 * float((pred == yte).mean())
    print(f"  style du traducteur : {acc:5.1f} % (hasard 50.0 %) → "
          f"{'LISIBLE ✓✓' if acc > 65 else ('au hasard ✗' if acc < 60 else '±')}")
    # 2) le sens survit-il au style ? ✓✓
    def retrieval(Xa, Xb):
        Xa = Xa - Xa.mean(0); Xb = Xb - Xb.mean(0)
        Xa = Xa / (np.linalg.norm(Xa, axis=1, keepdims=True) + 1e-9)
        Xb = Xb / (np.linalg.norm(Xb, axis=1, keepdims=True) + 1e-9)
        S = Xa @ Xb.T
        ordre = np.argsort(-S, axis=1)
        rangs = np.array([int(np.where(ordre[i] == i)[0][0]) + 1 for i in range(n)])
        return 100 * float((rangs == 1).mean()), float(np.median(rangs))
    t1, rk = retrieval(A, B)
    Bm = B[np.random.RandomState(1).permutation(len(B))]
    t1c, rkc = retrieval(A, Bm)
    print(f"  sens à travers le style : top-1 {t1:5.1f} % · rang médian {rk:.0f}/{n} (hasard 1/{n} = {100/n:.1f} %)")
    print(f"  contrôle (segments mélangés) : top-1 {t1c:5.1f} % · rang médian {rkc:.0f}/{n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
