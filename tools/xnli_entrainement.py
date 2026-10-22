#!/usr/bin/env python3
"""xnli_entrainement.py — ÉTAGE 2 : entraîner le modèle sur l'inférence **naturelle** (XNLI, LoRA + tête 3 classes).

POURQUOI ✓✓. La mesure 162 a montré que la sonde (même MLP) plafonne à ~50-59 % sur XNLI : ce n'est pas le readout
qui limite, c'est l'**état**. La suite est donc d'**entraîner le modèle** : un LoRA (attention) + une tête 3 classes
sur la couche 18, sur les paires XNLI. L'anglais en hérite-t-il sans pont ? ✓✓

CE QU'ON MESURE ✓✓ (hasard 1/3) :
  1. la tête FR et EN (transfert zéro-ressource) ✓✓ ;
  2. une sonde neuve sur les états FR du modèle entraîné, testée en EN ✓✓ ;
  3. le pont EN→FR ✓✓ ;
  4. le modèle figé (mesure 160) comme contrôle ✓✓.
"""
from __future__ import annotations
import argparse, json, pathlib, random
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


def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", default="data/xnli/XNLI-1.0/xnli.dev.tsv")
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--couche", type=int, default=18)
    ap.add_argument("--pas", type=int, default=400)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--accum", type=int, default=2)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--lr-tete", type=float, default=1e-2)
    ap.add_argument("--echauffement", type=int, default=100)
    ap.add_argument("--langue", choices=["both", "fr", "en"], default="both")
    ap.add_argument("--graine", type=int, default=1234)
    ap.add_argument("--sortie", default="reports/xnli-entrainement-3b.json")
    a = ap.parse_args()
    import torch
    import torch.nn as nn
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model
    torch.manual_seed(a.graine); random.seed(a.graine); np.random.seed(a.graine)
    etiquettes = {"entailment": 0, "neutral": 1, "contradiction": 2}
    donnees = {"fr": {}, "en": {}}
    with open(a.tsv, encoding="utf-8") as f:
        entete = f.readline().rstrip("\n").split("\t")
        idx = {c: i for i, c in enumerate(entete)}
        for ligne in f:
            cols = ligne.rstrip("\n").split("\t")
            if len(cols) <= idx["pairID"] or cols[idx["language"]] not in donnees:
                continue
            lang = cols[idx["language"]]
            donnees[lang].setdefault(cols[idx["pairID"]],
                                     (cols[idx["sentence1"]], cols[idx["sentence2"]], etiquettes[cols[idx["gold_label"]]]))
    communs = sorted(set(donnees["fr"]) & set(donnees["en"]))
    rng = np.random.default_rng(a.graine); rng.shuffle(communs)
    n_tr = int(0.8 * len(communs)); tr, te = communs[:n_tr], communs[n_tr:]
    print(f"  {len(communs)} paires ({len(tr)} train, {len(te)} test)")
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    base = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float16).to("cuda")
    lora = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, bias="none", task_type="FEATURE_EXTRACTION",
                      target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
    model = get_peft_model(base, lora)
    head = nn.Sequential(nn.LayerNorm(model.config.hidden_size), nn.Linear(model.config.hidden_size, 3)).to("cuda")
    opt = torch.optim.AdamW([{"params": [p for p in model.parameters() if p.requires_grad], "lr": 0.0},
                             {"params": list(head.parameters()), "lr": a.lr_tete}])
    scaler = torch.amp.GradScaler("cuda")

    def prompt(lang, s1, s2):
        if lang == "fr":
            c = f"Prémisse : {s1}\nHypothèse : {s2}\nRelation (impliqué, neutre ou contradictoire) :"
        else:
            c = f"Premise: {s1}\nHypothesis: {s2}\nRelation (entailment, neutral or contradiction):"
        return tok.apply_chat_template([{"role": "user", "content": c}], tokenize=False, add_generation_prompt=True)

    def lot(items, lang):
        textes = [prompt(lang, donnees[lang][p][0], donnees[lang][p][1]) for p in items]
        enc = tok(textes, return_tensors="pt", padding=True, truncation=True, max_length=256).to("cuda")
        y = torch.tensor([donnees["fr"][p][2] for p in items], device="cuda")
        return enc, y

    for pas in range(1, a.pas + 1):
        if pas == a.echauffement:
            opt.param_groups[0]["lr"] = a.lr
        langue = ("fr", "en")[pas % 2] if a.langue == "both" else a.langue
        items = random.sample(tr, a.batch)
        enc, y = lot(items, langue)
        with torch.autocast("cuda", dtype=torch.float16):
            hs = model(**enc, output_hidden_states=True, use_cache=False).hidden_states
        j = enc["attention_mask"].sum(1) - 1
        z = hs[a.couche][torch.arange(len(j)), j].float()
        perte = nn.functional.cross_entropy(head(z), y)
        scaler.scale(perte / a.accum).backward()
        if pas % a.accum == 0:
            scaler.step(opt); scaler.update(); opt.zero_grad()
        if pas % 50 == 0:
            print(f"  pas {pas} · perte {float(perte):.3f}")
    model.eval()

    @torch.no_grad()
    def etats(items, lang):
        out = []
        for i in range(0, len(items), 8):
            enc, _ = lot(items[i:i + 8], lang)
            with torch.autocast("cuda", dtype=torch.float16):
                hs = model(**enc, output_hidden_states=True, use_cache=False).hidden_states
            j = enc["attention_mask"].sum(1) - 1
            out.append(hs[a.couche][torch.arange(len(j)), j].float().cpu().numpy())
        return np.concatenate(out, 0)

    Efr_tr, Efr_te = etats(tr, "fr"), etats(te, "fr")
    Een_tr, Een_te = etats(tr, "en"), etats(te, "en")
    y_tr = np.array([donnees["fr"][p][2] for p in tr])
    y_te = np.array([donnees["fr"][p][2] for p in te])
    with torch.no_grad():
        tete_fr = float((head(torch.from_numpy(Efr_te).to("cuda")).argmax(1).cpu().numpy() == y_te).mean())
        tete_en = float((head(torch.from_numpy(Een_te).to("cuda")).argmax(1).cpu().numpy() == y_te).mean())
    pred_fr = sonde(Efr_tr, y_tr, Efr_te, 3)
    pred_en = sonde(Efr_tr, y_tr, Een_te, 3)
    W = pont(Een_tr, Efr_tr)
    pred_pont = sonde(Efr_tr, y_tr, appliquer(Een_te, W), 3)
    res = {"couche": a.couche, "pas": a.pas, "langue": a.langue, "n_train": len(tr), "n_test": len(te),
           "hasard": 1 / 3, "tete_fr": round(tete_fr, 4), "tete_en": round(tete_en, 4),
           "sonde_fr": round(float(np.mean(pred_fr == y_te)), 4),
           "sonde_en": round(float(np.mean(pred_en == y_te)), 4),
           "pont": round(float(np.mean(pred_pont == y_te)), 4)}
    for k, v in res.items():
        print(f"  {k}: {v}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
