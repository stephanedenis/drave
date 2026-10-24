#!/usr/bin/env python3
"""xnli_latent.py — ÉTAGE 2 : le raisonnement **NATUREL** (inférence) est-il dans l'état, et transfère-t-il FR↔EN ?

POURQUOI ✓✓. Les mesures 125-158 ont mesuré le raisonnement sur un corpus **synthétique** (chaînes d'ordre). XNLI
est un corpus **naturel** : 2 490 paires (prémisse, hypothèse) **traduites** en français et en anglais, étiquetées
*impliqué / neutre / contradictoire* ✓✓. La question : l'état caché porte-t-il l'inférence — et le pont FR↔EN la
transfère-t-il comme pour le synthétique ? ✓✓

CE QU'ON MESURE ✓✓ (hasard **1/3**) :
  1. sonde FR→FR et EN→EN (in-langue) ✓✓ ;
  2. sonde FR→EN **sans pont** (attendu au hasard) ✓✗ ;
  3. pont EN→FR appris sur les paires appariées ✓✓ ;
  4. contrôle : étiquettes mélangées ✓✓.
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


def pont(Xe, Xf, lam=10.0):
    A = np.hstack([Xe, np.ones((len(Xe), 1), np.float32)])
    return np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1], dtype=np.float32), A.T @ Xf)


def appliquer(X, W):
    return np.hstack([X, np.ones((len(X), 1), np.float32)]) @ W


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
    ap.add_argument("--tsv", default="data/xnli/XNLI-1.0/xnli.dev.tsv")
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--couche", type=int, default=18)
    ap.add_argument("--sortie", default="reports/xnli-3b.json")
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--repartir", action="store_true", help="répartir le modèle sur les GPU (device_map=auto)")
    ap.add_argument("--quatre-bits", action="store_true", help="charger en 4 bits nf4 (le 32 B sur 2 × 16 Go)")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    etiquettes = {"entailment": 0, "neutral": 1, "contradiction": 2}
    par_langue = {"fr": {}, "en": {}}
    with open(a.tsv, encoding="utf-8") as f:
        entete = f.readline().rstrip("\n").split("\t")
        idx = {c: i for i, c in enumerate(entete)}
        for ligne in f:
            cols = ligne.rstrip("\n").split("\t")
            if len(cols) <= idx["pairID"]:
                continue
            lang = cols[idx["language"]]
            if lang not in par_langue:
                continue
            pid = cols[idx["pairID"]]
            par_langue[lang].setdefault(pid, (cols[idx["sentence1"]], cols[idx["sentence2"]],
                                              etiquettes[cols[idx["gold_label"]]]))
    communs = sorted(set(par_langue["fr"]) & set(par_langue["en"]))
    print(f"  {len(communs)} paires FR/EN")
    rng = np.random.default_rng(1234); rng.shuffle(communs)
    n_tr = int(0.7 * len(communs)); tr, te = communs[:n_tr], communs[n_tr:]
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    if a.quatre_bits:
        # Le 32 B en fp16 (~64 Go) ne tient pas sur 2 × 16 Go : le nf4 le ramène à
        # ~18-20 Go, réparti par `device_map`. Le calcul reste en fp16 (le dtype
        # des états lus par les sondes ne change pas).
        from transformers import BitsAndBytesConfig
        bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                 bnb_4bit_compute_dtype=torch.float16,
                                 bnb_4bit_use_double_quant=True)
        # `auto` a mélangé CPU et GPU sur le 14 B (des couches sur le CPU, l'entrée sur
        # le cuda → « index is on cuda:0, different from other tensors on cpu »). En 4
        # bits le modèle tient sur UNE carte : `{"": 0}` force tout dessus. Le 32 B,
        # lui, a besoin des deux — ses mesures sont faites avec `auto`.
        model = AutoModelForCausalLM.from_pretrained(a.hf, quantization_config=bnb,
                                                     device_map={"": 0}).eval()
    elif a.repartir:
        # `auto` charge le 14 B à 15,28 Go sur la carte 0 (15,55) — OOM mesuré le 24/10,
        # et `balanced` (14+14) OOM aussi (la tête et les activations retombent sur la 0).
        # On plafonne à 13 Go par carte et on laisse déborder sur le CPU : le 14 B tient,
        # lentement, mais il tient.
        model = AutoModelForCausalLM.from_pretrained(
            a.hf, dtype=torch.float16, device_map="auto",
            max_memory={0: "13GiB", 1: "13GiB", "cpu": "40GiB"}).eval()
    else:
        model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float16).to("cuda").eval()

    def prompt(lang, s1, s2):
        if lang == "fr":
            consigne = f"Prémisse : {s1}\nHypothèse : {s2}\nRelation (impliqué, neutre ou contradictoire) :"
        else:
            consigne = f"Premise: {s1}\nHypothesis: {s2}\nRelation (entailment, neutral or contradiction):"
        return tok.apply_chat_template([{"role": "user", "content": consigne}], tokenize=False,
                                       add_generation_prompt=True)

    def etats(items, lang):
        textes = [prompt(lang, par_langue[lang][p][0], par_langue[lang][p][1]) for p in items]
        out = []
        for i in range(0, len(textes), a.batch):
            enc = tok(textes[i:i + a.batch], return_tensors="pt", padding=True, truncation=True,
                      max_length=256).to("cuda")
            with torch.no_grad():
                hs = model(**enc, output_hidden_states=True).hidden_states
            j = enc["attention_mask"].sum(1) - 1
            out.append(hs[a.couche][torch.arange(len(j)), j].float().cpu().numpy())
        return np.concatenate(out, 0)

    Efr_tr, Efr_te = etats(tr, "fr"), etats(te, "fr")
    Een_tr, Een_te = etats(tr, "en"), etats(te, "en")
    y_tr = np.array([par_langue["fr"][p][2] for p in tr])
    y_te = np.array([par_langue["fr"][p][2] for p in te])
    pred_fr = sonde(Efr_tr, y_tr, Efr_te, 3)
    pred_en = sonde(Efr_tr, y_tr, Een_te, 3)
    pred_en_en = sonde(Een_tr, y_tr, Een_te, 3)
    W = pont(Een_tr, Efr_tr)
    pred_pont = sonde(Efr_tr, y_tr, appliquer(Een_te, W), 3)
    rng2 = np.random.default_rng(7)
    pred_neg = sonde(Efr_tr, rng2.permutation(y_tr), Efr_te, 3)
    pred_fr_m = mlp_sonde(Efr_tr, y_tr, Efr_te, 3)
    pred_en_m = mlp_sonde(Efr_tr, y_tr, Een_te, 3)
    pred_pont_m = mlp_sonde(Efr_tr, y_tr, appliquer(Een_te, W), 3)
    pred_neg_m = mlp_sonde(Efr_tr, rng2.permutation(y_tr), Efr_te, 3)
    res = {"couche": a.couche, "n_train": len(tr), "n_test": len(te), "hasard": 1 / 3,
           "fr_fr": round(float(np.mean(pred_fr == y_te)), 4),
           "fr_en": round(float(np.mean(pred_en == y_te)), 4),
           "en_en": round(float(np.mean(pred_en_en == y_te)), 4),
           "pont_en_fr": round(float(np.mean(pred_pont == y_te)), 4),
           "negatif": round(float(np.mean(pred_neg == y_te)), 4),
           "fr_fr_mlp": round(float(np.mean(pred_fr_m == y_te)), 4),
           "fr_en_mlp": round(float(np.mean(pred_en_m == y_te)), 4),
           "pont_mlp": round(float(np.mean(pred_pont_m == y_te)), 4),
           "negatif_mlp": round(float(np.mean(pred_neg_m == y_te)), 4)}
    for k, v in res.items():
        print(f"  {k}: {v}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
