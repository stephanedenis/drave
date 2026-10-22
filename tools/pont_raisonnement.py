#!/usr/bin/env python3
"""pont_raisonnement.py — ÉTAGE 2 : un pont linéaire rend-il le raisonnement INDÉPENDANT de la langue ?

POURQUOI ✓✓. La mesure 125 a montré que la conclusion d'une chaîne transitive est **dans l'état** (1,00 → 0,51 en
FR, 1,00 → 0,53 en EN, hasard 5 %), mais qu'une sonde FR ne lit pas l'état EN : la géométrie n'est pas partagée ✗✗.
La mesure 77 avait montré qu'un **pont linéaire** aligne déjà les traductions ; on teste ici s'il aligne aussi le
**raisonnement** : un pont EN→FR appris sur les chaînes **appariées** (mêmes entités, même ordre) permet-il à la
sonde FR de lire l'état EN ? ✓✓

CE QU'ON MESURE ✓✓, par longueur (2 à 6 entités ; hasard 5 %) :
  1. la sonde **FR→FR** (référence) et **EN→EN** (référence) ✓✓ ;
  2. la sonde FR appliquée à l'état EN **sans pont** (mesure 125 : au hasard) ✓✗ ;
  3. la sonde FR appliquée au **pont EN→FR** ✓✓ ;
  4. le **contrôle** : pont appris sur des paires **mélangées** ✓✓.

CE QUE CHAQUE ISSUE VEUT DIRE ✓✓ :
  · le pont **récupère** le niveau in-langue → la géométrie est alignable, le raisonnement devient indépendant de la
    langue ✓✓ ;
  · le pont **ne récupère pas** → il faut un pont non linéaire ou un code partagé entraîné ✓✗.
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


def pont(Xe, Xf, lam):
    """Pont ridge EN → FR (avec biais)."""
    A = np.hstack([Xe, np.ones((len(Xe), 1), np.float32)])
    return np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1], dtype=np.float32), A.T @ Xf)


def appliquer(X, W):
    return np.hstack([X, np.ones((len(X), 1), np.float32)]) @ W


def cos(A, B):
    A = A / np.maximum(1e-9, np.linalg.norm(A, axis=1, keepdims=True))
    B = B / np.maximum(1e-9, np.linalg.norm(B, axis=1, keepdims=True))
    return float(np.mean(np.sum(A * B, 1)))


def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="data/raisonnement/transitif_paires.json")
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--couche", type=int, default=18)
    ap.add_argument("--sortie", default="reports/pont-raisonnement-3b.json")
    ap.add_argument("--batch", type=int, default=16)
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    d = json.loads(pathlib.Path(a.corpus).read_text())
    noms = d["noms"]; index = {n: i for i, n in enumerate(noms)}
    paires = [p for p in d["paires"] if p["reponse"] in index]
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float16).to("cuda").eval()

    def etats(textes):
        prompts = [tok.apply_chat_template([{"role": "user", "content": t}], tokenize=False,
                                           add_generation_prompt=True) for t in textes]
        sorties = []
        for i in range(0, len(prompts), a.batch):
            enc = tok(prompts[i:i + a.batch], return_tensors="pt", padding=True, truncation=True,
                      max_length=512).to("cuda")
            with torch.no_grad():
                hs = model(**enc, output_hidden_states=True).hidden_states
            idx = enc["attention_mask"].sum(1) - 1
            sorties.append(hs[a.couche][torch.arange(len(idx)), idx].float().cpu().numpy())
        return np.concatenate(sorties, 0)

    Efr = etats([p["fr"] for p in paires])
    Een = etats([p["en"] for p in paires])
    y = np.array([index[p["reponse"]] for p in paires])
    longueur = np.array([p["longueur"] for p in paires])
    split = np.array([p["split"] for p in paires])
    res = {"couche": a.couche, "n_paires": len(paires), "hasard": 1.0 / len(noms), "resultats": []}
    for L in (2, 3, 4, 5, 6):
        m_tr = (longueur == L) & (split == "train")
        m_te = (longueur == L) & (split == "test")
        if m_tr.sum() < 30 or m_te.sum() < 10:
            continue
        pred_fr = sonde(Efr[m_tr], y[m_tr], Efr[m_te], len(noms))
        pred_en = sonde(Een[m_tr], y[m_tr], Een[m_te], len(noms))
        # pont EN→FR, λ choisi sur 10 % des paires d'entraînement (cosinus)
        idx = np.where(m_tr)[0]
        nv = max(10, len(idx) // 10)
        trn, val = idx[:-nv], idx[-nv:]
        lam = max((0.1, 1.0, 10.0, 100.0, 1000.0),
                  key=lambda l: cos(appliquer(Een[val], pont(Een[trn], Efr[trn], l)), Efr[val]))
        W = pont(Een[trn], Efr[trn], lam)
        pred_pont = sonde(Efr[m_tr], y[m_tr], appliquer(Een[m_te], W), len(noms))
        # contrôle : pont appris sur des paires mélangées
        mel = np.random.default_rng(7).permutation(trn)
        Wn = pont(Een[mel], Efr[trn], lam)
        pred_neg = sonde(Efr[m_tr], y[m_tr], appliquer(Een[m_te], Wn), len(noms))
        r = {"longueur": L, "n_train": int(m_tr.sum()), "n_test": int(m_te.sum()),
             "fr_fr": round(float(np.mean(pred_fr == y[m_te])), 4),
             "en_en": round(float(np.mean(pred_en == y[m_te])), 4),
             "pont": round(float(np.mean(pred_pont == y[m_te])), 4),
             "pont_melange": round(float(np.mean(pred_neg == y[m_te])), 4), "lambda": lam}
        # sans pont : la sonde FR appliquée directement à l'état EN
        pred_sans = sonde(Efr[m_tr], y[m_tr], Een[m_te], len(noms))
        r["fr_sur_en_sans_pont"] = round(float(np.mean(pred_sans == y[m_te])), 4)
        res["resultats"].append(r)
        print(f"  L{L} · FR→FR {r['fr_fr']:.3f} · EN→EN {r['en_en']:.3f} · FR sur EN sans pont "
              f"{r['fr_sur_en_sans_pont']:.3f} · **pont {r['pont']:.3f}** · pont mélangé {r['pont_melange']:.3f}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
