#!/usr/bin/env python3
"""raisonnement_entrainement.py — ÉTAGE 2 : faire **assimiler** le raisonnement au modèle (LoRA + tête), et voir
si l'anglais en hérite sans pont.

POURQUOI ✓✓. Les mesures 125-140 ont montré que le raisonnement transitif est **dans l'état** et qu'un pont linéaire
le rend indépendant de la langue — mais le pont est une pièce **externe**. La question de la « tête bien faite » :
si on **entraîne** le modèle à répondre (une tête de 20 classes sur la couche 18, LoRA sur l'attention), le
raisonnement devient-il **indépendant de la langue dans le modèle** — l'anglais en hérite-t-il sans pont ? ✓✓

CE QU'ON MESURE ✓✓ (hasard 5 %) :
  1. la tête entraînée, évaluée en **FR** (référence) et en **EN** (transfert zéro-ressource) ✓✓ ;
  2. une sonde **neuve** entraînée sur les états FR du modèle entraîné, testée en EN ✓✓ ;
  3. le **pont** EN→FR appris sur les paires du modèle entraîné, testé en EN ✓✓ ;
  4. les mêmes chiffres sur le modèle **figé** (mesures 125-135) servent de contrôle ✓✓.

CE QUE CHAQUE ISSUE VEUT DIRE ✓✓ :
  · la tête ou la sonde **réussit en EN** → le raisonnement est devenu indépendant de la langue **dans le modèle** ✓✓ ;
  · elle reste au hasard, mais le pont réussit → le modèle a appris une représentation **alignable**, pas alignée ✓✗ ;
  · tout échoue → l'entraînement FR ne transfère pas ; le pont reste nécessaire ✓✗.
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
    ap.add_argument("--corpus", default="data/raisonnement/transitif_paires_3langues.json")
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--couche", type=int, default=18)
    ap.add_argument("--pas", type=int, default=300)
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--accum", type=int, default=2)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--lr-tete", type=float, default=1e-2)
    ap.add_argument("--echauffement", type=int, default=100, help="pas de tête seule avant le LoRA")
    ap.add_argument("--multilingue", action="store_true", help="alterner FR et EN à chaque pas")
    ap.add_argument("--contrastif", action="store_true", help="ajouter une perte InfoNCE entre les états FR et EN de la même chaîne")
    ap.add_argument("--tau", type=float, default=0.07)
    ap.add_argument("--poids", type=float, default=1.0)
    ap.add_argument("--graine", type=int, default=1234)
    ap.add_argument("--sortie", default="reports/raisonnement-entrainement-3b.json")
    a = ap.parse_args()
    import torch
    import torch.nn as nn
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model
    torch.manual_seed(a.graine); random.seed(a.graine); np.random.seed(a.graine)
    d = json.loads(pathlib.Path(a.corpus).read_text())
    noms = d["noms"]; index = {n: i for i, n in enumerate(noms)}
    paires = [p for p in d["paires"] if p["reponse"] in index and "fr" in p and "en" in p]
    tr = [p for p in paires if p["split"] == "train"]
    te = [p for p in paires if p["split"] == "test"]
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    base = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float16).to("cuda").eval()
    lora = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, bias="none", task_type="FEATURE_EXTRACTION",
                      target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
    model = get_peft_model(base, lora)
    model.train()
    head = nn.Sequential(nn.LayerNorm(model.config.hidden_size), nn.Linear(model.config.hidden_size, len(noms))).to("cuda")
    opt = torch.optim.AdamW([
        {"params": [p for p in model.parameters() if p.requires_grad], "lr": 0.0},
        {"params": list(head.parameters()), "lr": a.lr_tete},
    ])
    scaler = torch.amp.GradScaler("cuda")

    def lot(items, langue):
        textes = [tok.apply_chat_template([{"role": "user", "content": p[langue]}], tokenize=False,
                                          add_generation_prompt=True) for p in items]
        enc = tok(textes, return_tensors="pt", padding=True, truncation=True, max_length=256).to("cuda")
        y = torch.tensor([index[p["reponse"]] for p in items], device="cuda")
        return enc, y

    for pas in range(1, a.pas + 1):
        if pas == a.echauffement:
            opt.param_groups[0]["lr"] = a.lr
        langue = ("fr", "en")[pas % 2] if a.multilingue else "fr"
        items = random.sample(tr, a.batch)
        enc, y = lot(items, langue)
        with torch.autocast("cuda", dtype=torch.float16):
            hs = model(**enc, output_hidden_states=True, use_cache=False).hidden_states
        idx = enc["attention_mask"].sum(1) - 1
        z = hs[a.couche][torch.arange(len(idx)), idx].float()
        logits = head(z)
        perte = nn.functional.cross_entropy(logits, y)
        if a.contrastif:
            enc_en, _ = lot(items, "en")
            with torch.autocast("cuda", dtype=torch.float16):
                hs_en = model(**enc_en, output_hidden_states=True, use_cache=False).hidden_states
            ide = enc_en["attention_mask"].sum(1) - 1
            z_en = hs_en[a.couche][torch.arange(len(ide)), ide].float()
            zn = nn.functional.normalize(z, dim=1); zen = nn.functional.normalize(z_en, dim=1)
            lc = zn @ zen.T / a.tau
            cible = torch.arange(len(items), device="cuda")
            perte = perte + a.poids * 0.5 * (nn.functional.cross_entropy(lc, cible)
                                             + nn.functional.cross_entropy(lc.T, cible))
        scaler.scale(perte / a.accum).backward()
        if pas % a.accum == 0:
            scaler.step(opt); scaler.update(); opt.zero_grad()
        if pas % 50 == 0:
            print(f"  pas {pas} · perte {float(perte):.3f}")
    model.eval()

    @torch.no_grad()
    def etats(items, langue):
        sorties = []
        for i in range(0, len(items), 8):
            enc, _ = lot(items[i:i + 8], langue)
            with torch.autocast("cuda", dtype=torch.float16):
                hs = model(**enc, output_hidden_states=True, use_cache=False).hidden_states
            idx = enc["attention_mask"].sum(1) - 1
            sorties.append(hs[a.couche][torch.arange(len(idx)), idx].float().cpu().numpy())
        return np.concatenate(sorties, 0)

    Efr_tr = etats(tr, "fr"); Een_tr = etats(tr, "en")
    Efr_te = etats(te, "fr"); Een_te = etats(te, "en")
    y_tr = np.array([index[p["reponse"]] for p in tr])
    y_te = np.array([index[p["reponse"]] for p in te])
    # 1. la tête entraînée
    with torch.no_grad():
        tete_fr = torch.from_numpy(Efr_te).to("cuda")
        tete_en = torch.from_numpy(Een_te).to("cuda")
        acc_tete_fr = float((head(tete_fr).argmax(1).cpu().numpy() == y_te).mean())
        acc_tete_en = float((head(tete_en).argmax(1).cpu().numpy() == y_te).mean())
    # 2. sonde neuve sur les états FR, testée EN
    pred_fr = sonde(Efr_tr, y_tr, Efr_te, len(noms))
    pred_en = sonde(Efr_tr, y_tr, Een_te, len(noms))
    # 3. pont EN→FR
    W = pont(Een_tr, Efr_tr)
    pred_pont = sonde(Efr_tr, y_tr, appliquer(Een_te, W), len(noms))
    res = {"couche": a.couche, "pas": a.pas, "graine": a.graine, "n_train": len(tr), "n_test": len(te),
           "hasard": 1.0 / len(noms),
           "tete_fr": round(acc_tete_fr, 4), "tete_en": round(acc_tete_en, 4),
           "sonde_fr": round(float(np.mean(pred_fr == y_te)), 4),
           "sonde_en": round(float(np.mean(pred_en == y_te)), 4),
           "pont_en_fr": round(float(np.mean(pred_pont == y_te)), 4)}
    for k, v in res.items():
        print(f"  {k}: {v}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
