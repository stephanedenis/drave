#!/usr/bin/env python3
"""code_partage.py — ÉTAGE 2 : un **code partagé** de petite dimension suffit-il pour aligner le raisonnement ?

POURQUOI ✓✓. Les mesures 126-137 ont montré qu'un pont **linéaire** EN→FR (pleine dimension, 2048) rend le
raisonnement transitif indépendant de la langue (0,94 / 0,91 / 0,81 poolé ; 7 B : 0,95 / 0,87 / 0,81). La question de
la « tête bien faite » : combien de dimensions faut-il à ce code partagé ? Si **64** suffisent, l'alignement est une
très petite structure ; s'il faut les 2048, c'est une carte riche. ✓✓

CE QU'ON MESURE ✓✓ : une **ACP** (k dimensions) ajustée sur les états FR **et** EN d'entraînement (le code commun),
puis un pont linéaire EN→FR **dans ce code** (k×k), une sonde FR dans le code, et le retrieval sur les états EN
projetés ✓✓ ; contrôles : pont mélangé, sans pont ✓✓. Hasard **5 %** ✓✓.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np


def sonde(Xtr, ytr, Xte, classes, lam=10.0):
    moy = Xtr.mean(0, keepdims=True); ect = Xtr.std(0, keepdims=True) + 1e-6
    A = (Xtr - moy) / ect; B = (Xte - moy) / ect
    Y = np.eye(classes, dtype=np.float32)[ytr]
    Xb = np.hstack([A, np.ones((len(A), 1), np.float32)])
    W = np.linalg.solve(Xb.T @ Xb + lam * np.eye(Xb.shape[1], dtype=np.float32), Xb.T @ Y)
    return np.argmax(np.hstack([B, np.ones((len(B), 1), np.float32)]) @ W, 1)


def pont(Xe, Xf, lam=1.0):
    A = np.hstack([Xe, np.ones((len(Xe), 1), np.float32)])
    return np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1], dtype=np.float32), A.T @ Xf)


def appliquer(X, W):
    return np.hstack([X, np.ones((len(X), 1), np.float32)]) @ W


def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="data/raisonnement/transitif_paires_3langues.json")
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--couche", type=int, default=18)
    ap.add_argument("--k", type=int, default=64)
    ap.add_argument("--sortie", default="reports/code-partage-3b.json")
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
    # ACP commune (FR + EN d'entraînement), centrée
    X = np.vstack([Efr[tr], Een[tr]]).astype(np.float32)
    moy = X.mean(0, keepdims=True)
    U, S, Vt = np.linalg.svd(X - moy, full_matrices=False)
    P = Vt[:a.k].T  # d × k
    Zfr = (Efr - moy) @ P; Zen = (Een - moy) @ P
    res = {"couche": a.couche, "k": a.k, "hasard": 1.0 / len(noms), "resultats": []}
    for L in (2, 3, 4, 5, 6):
        m_tr = (longueur == L) & tr; m_te = (longueur == L) & (split == "test")
        if m_tr.sum() < 30 or m_te.sum() < 10:
            continue
        W = pont(Zen[m_tr], Zfr[m_tr])
        mel = np.random.default_rng(7).permutation(np.where(m_tr)[0])
        Wn = pont(Zen[mel], Zfr[m_tr])
        pred = sonde(Zfr[m_tr], y[m_tr], appliquer(Zen[m_te], W), len(noms))
        pred_n = sonde(Zfr[m_tr], y[m_tr], appliquer(Zen[m_te], Wn), len(noms))
        pred_sans = sonde(Zfr[m_tr], y[m_tr], Zen[m_te], len(noms))
        pred_fr = sonde(Zfr[m_tr], y[m_tr], Zfr[m_te], len(noms))
        r = {"longueur": L, "k": a.k, "fr_fr": round(float(np.mean(pred_fr == y[m_te])), 4),
             "sans_pont": round(float(np.mean(pred_sans == y[m_te])), 4),
             "pont": round(float(np.mean(pred == y[m_te])), 4),
             "pont_melange": round(float(np.mean(pred_n == y[m_te])), 4)}
        res["resultats"].append(r)
        print(f"  L{L} · FR→FR {r['fr_fr']:.3f} · sans pont {r['sans_pont']:.3f} · "
              f"**code {a.k} + pont {r['pont']:.3f}** · mélangé {r['pont_melange']:.3f}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
