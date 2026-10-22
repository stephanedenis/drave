#!/usr/bin/env python3
"""pont_croise.py — ÉTAGE 2 : un pont appris sur le RAISONNEMENT aligne-t-il l'état de PLAN ?

POURQUOI ✓✓. Les mesures 126-133 ont montré qu'un petit pont linéaire rend le **raisonnement** transitif indépendant
de la langue (quatre langues indo-européennes + l'arabe). La mesure 132 a montré qu'un pont appris **sur le plan**
dégrade le plan (0,148 contre 0,250 sans pont). La question de la « tête bien faite » : la géométrie est-elle
**partagée entre les tâches** — un pont appris sur le raisonnement aligne-t-il aussi le plan ? ✓✓

CE QU'ON MESURE ✓✓ : un pont EN→FR appris sur les **paires de raisonnement** (textes bruts, sans template), appliqué
aux **prompts de plan** (4 phrases Verne) ; retrieval de la 5ᵉ phrase parmi les 8 de la série (hasard 12,5 %) ✓✓ ;
contrôle : pont appris sur des paires de raisonnement **mélangées** ✓✓.

CE QUE CHAQUE ISSUE VEUT DIRE ✓✓ :
  · le pont croisé **récupère** le plan → la géométrie est **partagée entre tâches** ✓✓ ;
  · le pont croisé **échoue** → chaque tâche a sa géométrie ; il faut un pont par tâche (ou un code partagé
    entraîné) ✓✗.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np


def norm(x):
    return x / np.maximum(1e-9, np.linalg.norm(x, axis=1, keepdims=True))


def pont(Xe, Xf, lam=10.0):
    A = np.hstack([Xe, np.ones((len(Xe), 1), np.float32)])
    return np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1], dtype=np.float32), A.T @ Xf)


def appliquer(X, W):
    return norm(np.hstack([X, np.ones((len(X), 1), np.float32)]) @ W)


def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--couche", type=int, default=18)
    ap.add_argument("--sortie", default="reports/pont-croise-3b.json")
    ap.add_argument("--batch", type=int, default=16)
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float16).to("cuda").eval()

    def etats(textes, max_len=256):
        out = []
        for i in range(0, len(textes), a.batch):
            enc = tok(textes[i:i + a.batch], return_tensors="pt", padding=True, truncation=True,
                      max_length=max_len).to("cuda")
            with torch.no_grad():
                hs = model(**enc, output_hidden_states=True).hidden_states
            idx = enc["attention_mask"].sum(1) - 1
            out.append(hs[a.couche][torch.arange(len(idx)), idx].float().cpu().numpy())
        return np.concatenate(out, 0)

    # --- raisonnement : paires EN/FR brutes, pont EN→FR
    d = json.loads(pathlib.Path("data/raisonnement/transitif_paires_3langues.json").read_text())
    rap = [p for p in d["paires"] if "fr" in p and "en" in p]
    print(f"  raisonnement : {len(rap)} paires")
    Rfr = etats([p["fr"] for p in rap]); Ren = etats([p["en"] for p in rap])
    tr = np.array([p["split"] == "train" for p in rap])
    W = pont(norm(Ren[tr]), norm(Rfr[tr]))
    mel = np.random.default_rng(7).permutation(np.where(tr)[0])
    Wn = pont(norm(Ren[mel]), norm(Rfr[tr]))

    # --- plan : séries Verne appariées
    v = json.loads(pathlib.Path("data/alignement/verne_fr_en.json").read_text())
    paires = [p for p in v["paires"] if p.get("n_fr") == 1 and p.get("n_en") == 1]
    par_chap = {}
    for p in paires:
        par_chap.setdefault(p["chapitre"], []).append(p)
    series = []
    for ch in sorted(par_chap):
        ps = sorted(par_chap[ch], key=lambda p: p["i_fr"])
        for i in range(0, len(ps) - 8 + 1, 8):
            bloc = ps[i:i + 8]
            if len(bloc) == 8:
                series.append(([p["fr"] for p in bloc], [p["en"] for p in bloc]))
    pas = max(1, len(series) // 315)
    series = series[::pas][:315]
    rng = np.random.default_rng(1234)
    cles = np.arange(len(series)); rng.shuffle(cles)
    n_tr = int(0.7 * len(cles)); te = cles[n_tr:]
    Pfr = norm(etats([" ".join(series[k][0][:4]) for k in range(len(series))]))
    Pen = norm(etats([" ".join(series[k][1][:4]) for k in range(len(series))]))
    Cfr = norm(etats([series[k][0][4] for k in range(len(series))], 128))
    Cen = norm(etats([series[k][1][4] for k in range(len(series))], 128))
    justes = {k: 0 for k in ("fr_fr", "en_en", "en_fr_sans_pont", "en_fr_pont_croise", "en_fr_pont_melange")}
    tot = 0
    for i in range(0, len(te) - 7, 8):
        groupe = te[i:i + 8]; c = np.arange(8)
        justes["fr_fr"] += int(np.sum(np.argmax(Pfr[groupe] @ Cfr[groupe].T, 1) == c))
        justes["en_en"] += int(np.sum(np.argmax(Pen[groupe] @ Cen[groupe].T, 1) == c))
        justes["en_fr_sans_pont"] += int(np.sum(np.argmax(Pen[groupe] @ Cfr[groupe].T, 1) == c))
        justes["en_fr_pont_croise"] += int(np.sum(np.argmax(appliquer(Pen[groupe], W) @ Cfr[groupe].T, 1) == c))
        justes["en_fr_pont_melange"] += int(np.sum(np.argmax(appliquer(Pen[groupe], Wn) @ Cfr[groupe].T, 1) == c))
        tot += 8
    res = {"couche": a.couche, "n_series": len(series), "n_test": tot, "hasard": 0.125,
           "resultats": {k: round(v / max(1, tot), 4) for k, v in justes.items()}}
    print(f"  FR→FR {res['resultats']['fr_fr']:.3f} · EN→EN {res['resultats']['en_en']:.3f} · EN→FR sans pont "
          f"{res['resultats']['en_fr_sans_pont']:.3f} · **pont croisé {res['resultats']['en_fr_pont_croise']:.3f}** · "
          f"mélangé {res['resultats']['en_fr_pont_melange']:.3f} (hasard 0,125)")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
