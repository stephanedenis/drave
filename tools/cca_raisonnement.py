#!/usr/bin/env python3
"""cca_raisonnement.py — ÉTAGE 2 : un code partagé **supervisé par les paires** (CCA) suffit-il à petite dimension ?

POURQUOI ✓✓. La mesure 138 a montré qu'une ACP commune (non supervisée) de 64 ou 256 dimensions ne suffit pas :
0,14-0,98 et 0,34-1,00 contre 0,46-1,00 pour le pont pleine dimension. Mais l'ACP ne cherche pas à **aligner** les
langues ; la **CCA** le fait : elle trouve les directions où FR et EN sont le plus corrélés. La question : un code
CCA de 64 dimensions (calculé sur les paires d'entraînement) porte-t-il le raisonnement d'une langue à l'autre ? ✓✓

CE QU'ON MESURE ✓✓ (hasard 5 %) :
  1. le code CCA **poolé** (ajusté sur toutes les longueurs d'entraînement), sonde FR poolée, test EN par longueur ✓✓ ;
  2. le même, **par longueur** (CCA et sonde sur la longueur) ✓✓ ;
  3. le contrôle : CCA ajustée sur des paires **mélangées** ✓✓.

CE QUE CHAQUE ISSUE VEUT DIRE ✓✓ :
  · la CCA **récupère** le raisonnement à 64 dims → il existe un code partagé **supervisé** de petite dimension ✓✓ ;
  · la CCA **échoue** → même supervisé, le code perd l'information : c'est le pont pleine dimension qui est la
    structure minimale ✓✗.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np


def invsqrt(C, r=1e-6):
    w, V = np.linalg.eigh(C)
    w = np.maximum(w, r * max(1.0, float(w.max())))
    return V @ np.diag(1.0 / np.sqrt(w)) @ V.T


def cca(X, Y, k, r=0.1):
    X = X - X.mean(0); Y = Y - Y.mean(0)
    d = X.shape[1]
    Cxx = X.T @ X / len(X) + r * np.eye(d, dtype=np.float64)
    Cyy = Y.T @ Y / len(Y) + r * np.eye(d, dtype=np.float64)
    Wx0, Wy0 = invsqrt(Cxx), invsqrt(Cyy)
    C = Wx0 @ (X.T @ Y / len(X)) @ Wy0
    U, S, Vt = np.linalg.svd(C, full_matrices=False)
    return Wx0 @ U[:, :k], Wy0 @ Vt[:k].T, S[:k]


def sonde(Xtr, ytr, Xte, classes, lam=10.0):
    moy = Xtr.mean(0, keepdims=True); ect = Xtr.std(0, keepdims=True) + 1e-6
    A = (Xtr - moy) / ect; B = (Xte - moy) / ect
    Y = np.eye(classes, dtype=np.float32)[ytr]
    Xb = np.hstack([A, np.ones((len(A), 1), np.float32)])
    W = np.linalg.solve(Xb.T @ Xb + lam * np.eye(Xb.shape[1], dtype=np.float32), Xb.T @ Y)
    return np.argmax(np.hstack([B, np.ones((len(B), 1), np.float32)]) @ W, 1)


def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="data/raisonnement/transitif_paires_3langues.json")
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--couche", type=int, default=18)
    ap.add_argument("--k", type=int, default=64)
    ap.add_argument("--pca", type=int, default=256, help="réduction ACP avant la CCA (0 = pleine dimension)")
    ap.add_argument("--sortie", default="reports/cca-raisonnement-3b.json")
    ap.add_argument("--batch", type=int, default=16)
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    d = json.loads(pathlib.Path(a.corpus).read_text())
    noms = d["noms"]; index = {n: i for i, n in enumerate(noms)}
    paires = [p for p in d["paires"] if p["reponse"] in index and "fr" in p and "en" in p]
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float16).to("cuda").eval()

    def etats(textes):
        out = []
        for i in range(0, len(textes), a.batch):
            enc = tok(textes[i:i + a.batch], return_tensors="pt", padding=True, truncation=True,
                      max_length=256).to("cuda")
            with torch.no_grad():
                hs = model(**enc, output_hidden_states=True).hidden_states
            idx = enc["attention_mask"].sum(1) - 1
            out.append(hs[a.couche][torch.arange(len(idx)), idx].float().cpu().numpy())
        return np.concatenate(out, 0)

    Efr = etats([p["fr"] for p in paires]); Een = etats([p["en"] for p in paires])
    y = np.array([index[p["reponse"]] for p in paires])
    longueur = np.array([p["longueur"] for p in paires])
    split = np.array([p["split"] for p in paires])
    tr = split == "train"
    # ACP commune éventuelle (pooled), puis CCA
    X = np.vstack([Efr[tr], Een[tr]]).astype(np.float32)
    moy = X.mean(0, keepdims=True)
    if a.pca:
        _, _, Vt = np.linalg.svd(X - moy, full_matrices=False)
        P = Vt[:a.pca].T
        Zfr = (Efr - moy) @ P; Zen = (Een - moy) @ P
    else:
        Zfr, Zen = Efr - moy, Een - moy
    res = {"couche": a.couche, "k": a.k, "pca": a.pca, "hasard": 1.0 / len(noms), "pooled": [], "par_longueur": []}
    # CCA poolée
    Wx, Wy, S = cca(Zen[tr].astype(np.float64), Zfr[tr].astype(np.float64), a.k)
    Cfr = (Zfr - Zfr[tr].mean(0)) @ Wy; Cen = (Zen - Zen[tr].mean(0)) @ Wx
    for L in (2, 3, 4, 5, 6):
        m_te = (longueur == L) & (split == "test")
        if m_te.sum() < 10:
            continue
        pred = sonde(Cfr[tr], y[tr], Cen[m_te], len(noms))
        pred_fr = sonde(Cfr[tr], y[tr], Cfr[m_te], len(noms))
        r = {"longueur": L, "fr_fr": round(float(np.mean(pred_fr == y[m_te])), 4),
             "cca": round(float(np.mean(pred == y[m_te])), 4)}
        res["pooled"].append(r)
        print(f"  poolée L{L} · FR→FR {r['fr_fr']:.3f} · **CCA {r['cca']:.3f}**")
    # contrôle : CCA sur paires mélangées (poolée)
    mel = np.random.default_rng(7).permutation(np.where(tr)[0])
    Wxn, Wyn, _ = cca(Zen[mel].astype(np.float64), Zfr[tr].astype(np.float64), a.k)
    Cfrn = (Zfr - Zfr[tr].mean(0)) @ Wyn; Cenn = (Zen - Zen[tr].mean(0)) @ Wxn
    for L in (2, 3, 4, 5, 6):
        m_te = (longueur == L) & (split == "test")
        if m_te.sum() < 10:
            continue
        pred = sonde(Cfrn[tr], y[tr], Cenn[m_te], len(noms))
        res["pooled"][ [r["longueur"] for r in res["pooled"]].index(L) ]["cca_melange"] = round(float(np.mean(pred == y[m_te])), 4)
        print(f"  poolée L{L} · CCA mélangée {res['pooled'][[r['longueur'] for r in res['pooled']].index(L)]['cca_melange']:.3f}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
