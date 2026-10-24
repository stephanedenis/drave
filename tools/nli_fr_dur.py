#!/usr/bin/env python3
"""nli_fr_dur.py — ÉTAGE 2 : le raisonnement naturel FRANÇAIS **plus dur que XNLI**.

POURQUOI ✓✓. XNLI est le seul jeu NLI français « courant ». DACCORD (1 034 paires de
contradictions) et GQNLI-FR (300 paires, les quantificateurs) ont été construits pour
être **plus durs** que XNLI et FraCaS (Skandalis et al., LREC-COLING 2024). La question :
la sonde lit-elle encore la réponse dans l'état sur ces jeux **difficiles** — ou le
0,50 de XNLI était-il déjà le plafond du facile ? ✓✓

CE QU'ON MESURE ✓✓ :
  1. la sonde FR sur le jeu (in-langue) ✓✓ ;
  2. le contrôle : les mêmes états avec les **étiquettes mélangées** (attendu : le hasard) ✓✓ ;
  3. la sonde MLP (le pont n'a pas de sens ici : DACCORD et GQNLI-FR sont **français seulement**).

Usage :
  nli_fr_dur.py --tsv data/daccord/daccord.tsv --binaire --hf Qwen/Qwen2.5-1.5B-Instruct \
      --sortie reports/nli-daccord-1.5b.json
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


def mlp_sonde(Xtr, ytr, Xte, classes, cache=512, epochs=30, graine=1234):
    import torch
    import torch.nn as nn
    torch.manual_seed(graine); torch.set_num_threads(8)
    X = torch.from_numpy(Xtr.astype(np.float32)); Y = torch.from_numpy(ytr.astype(np.int64))
    T = torch.from_numpy(Xte.astype(np.float32))
    moy = X.mean(0, keepdim=True); ect = X.std(0, keepdim=True) + 1e-6
    X = (X - moy) / ect; T = (T - moy) / ect
    m = nn.Sequential(nn.Linear(X.shape[1], cache), nn.GELU(), nn.Dropout(0.2), nn.Linear(cache, classes))
    opt = torch.optim.AdamW(m.parameters(), lr=1e-3, weight_decay=1e-4)
    for _ in range(epochs):
        perm = torch.randperm(len(X))
        for i in range(0, len(X), 128):
            idx = perm[i:i + 128]
            perte = nn.functional.cross_entropy(m(X[idx]), Y[idx])
            opt.zero_grad(); perte.backward(); opt.step()
    with torch.no_grad():
        return m(T).argmax(1).numpy()


def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", required=True)
    ap.add_argument("--hf", default="Qwen/Qwen2.5-1.5B-Instruct")
    ap.add_argument("--couche", type=int, default=18)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--binaire", action="store_true", help="2 classes (DACCORD) ; sinon 3 (GQNLI)")
    ap.add_argument("--sortie", default="reports/nli-dur.json")
    a = ap.parse_args()
    lignes = pathlib.Path(a.tsv).read_text(encoding="utf-8").splitlines()
    entete = lignes[0].split("\t")
    idx = {c: i for i, c in enumerate(entete)}
    paires = []
    for l in lignes[1:]:
        cols = l.split("\t")
        if len(cols) <= max(idx["premise"], idx["hypothesis"], idx["label"]):
            continue
        try:
            y = int(cols[idx["label"]])
        except ValueError:
            continue
        paires.append((cols[idx["premise"]], cols[idx["hypothesis"]], y))
    classes = 2 if a.binaire else 3
    print(f"  {len(paires)} paires · {classes} classes · hasard {1/classes:.3f}")
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float16).to("cuda").eval()
    consigne = ("Ces deux phrases se contredisent-elles (oui ou non) ?" if a.binaire
                else "Relation (impliqué, neutre ou contradictoire) :")

    def etats(items):
        textes = [tok.apply_chat_template(
            [{"role": "user", "content":
              f"Prémisse : {s1}\nHypothèse : {s2}\n{consigne}"}],
            tokenize=False, add_generation_prompt=True) for s1, s2, _ in items]
        out = []
        for i in range(0, len(textes), a.batch):
            enc = tok(textes[i:i + a.batch], return_tensors="pt", padding=True,
                      truncation=True, max_length=256).to("cuda")
            with torch.no_grad():
                hs = model(**enc, output_hidden_states=True).hidden_states
            j = enc["attention_mask"].sum(1) - 1
            out.append(hs[a.couche][torch.arange(len(j)), j].float().cpu().numpy())
        return np.concatenate(out, 0)

    rng = np.random.default_rng(1234)
    ordre = rng.permutation(len(paires))
    n_tr = int(0.7 * len(paires))
    tr = [paires[i] for i in ordre[:n_tr]]
    te = [paires[i] for i in ordre[n_tr:]]
    Etr, Ete = etats(tr), etats(te)
    ytr = np.array([p[2] for p in tr]); yte = np.array([p[2] for p in te])
    pred = sonde(Etr, ytr, Ete, classes)
    rng2 = np.random.default_rng(7)
    pred_neg = sonde(Etr, rng2.permutation(ytr), Ete, classes)
    pred_m = mlp_sonde(Etr, ytr, Ete, classes)
    pred_neg_m = mlp_sonde(Etr, rng2.permutation(ytr), Ete, classes)
    res = {"jeu": pathlib.Path(a.tsv).stem, "modele": a.hf, "couche": a.couche,
           "n_train": len(tr), "n_test": len(te), "classes": classes, "hasard": 1 / classes,
           "fr_fr": round(float(np.mean(pred == yte)), 4),
           "negatif": round(float(np.mean(pred_neg == yte)), 4),
           "fr_fr_mlp": round(float(np.mean(pred_m == yte)), 4),
           "negatif_mlp": round(float(np.mean(pred_neg_m == yte)), 4)}
    for k, v in res.items():
        print(f"  {k}: {v}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
