#!/usr/bin/env python3
"""pont_plan.py — ÉTAGE 2 : le pont qui aligne le RAISONNEMENT aligne-t-il aussi l'état de PLAN ?

POURQUOI ✓✓. Les mesures 125-131 ont montré qu'un petit pont **linéaire** rend le raisonnement transitif indépendant
de la langue (1,00 / 0,91 / 0,68 / 0,52 / 0,46 pour 2 à 6 entités ; quatre langues ; couches 12-24). Les mesures
119-124 ont montré qu'un **état de plan** (les 4 premières phrases d'une série) porte la suite, mais seulement dans
la langue où il a été entraîné. La question : le **même** genre de pont aligne-t-il l'état de plan, ou le plan est-il
une représentation plus « collée » à la langue ? ✓✓

CE QU'ON MESURE ✓✓, sur les séries Verne FR/EN appariées (8 phrases) :
  1. **FR→FR** et **EN→EN** : le prompt (4 phrases) retrouve la 5ᵉ parmi les 8 cibles de sa série (hasard 12,5 %) ✓✓ ;
  2. **EN→FR sans pont** (attendu au hasard) ✓✗ ;
  3. **EN→FR avec pont** appris sur les prompts appariés ✓✓ ;
  4. **contrôle** : pont appris sur des paires mélangées ✓✓.

CE QUE CHAQUE ISSUE VEUT DIRE ✓✓ :
  · le pont **récupère** le plan → l'alignement est un mécanisme général de l'étage 2 ✓✓ ;
  · le pont **échoue** → le plan est plus dépendant de la langue que le raisonnement ; il faudra l'entraîner dans le
    modèle, pas le ponter ✓✗.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np


def cos(A, B):
    A = A / np.maximum(1e-9, np.linalg.norm(A, axis=1, keepdims=True))
    B = B / np.maximum(1e-9, np.linalg.norm(B, axis=1, keepdims=True))
    return float(np.mean(np.sum(A * B, 1)))


def retrieval(pred, cand):
    return float(np.mean(np.argmax(pred @ cand.T, 1) == np.arange(len(pred))))


def norm(x):
    return x / np.maximum(1e-9, np.linalg.norm(x, axis=1, keepdims=True))


def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--couche", type=int, default=18)
    ap.add_argument("--series", type=int, default=315)
    ap.add_argument("--prompt", type=int, default=4)
    ap.add_argument("--sortie", default="reports/pont-plan-3b.json")
    ap.add_argument("--batch", type=int, default=16)
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    d = json.loads(pathlib.Path("data/alignement/verne_fr_en.json").read_text())
    paires = [p for p in d["paires"] if p.get("n_fr") == 1 and p.get("n_en") == 1]
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
    pas = max(1, len(series) // a.series)
    series = series[::pas][:a.series]
    print(f"  {len(series)} séries appariées")
    rng = np.random.default_rng(1234)
    cles = np.arange(len(series)); rng.shuffle(cles)
    n_tr = int(0.7 * len(cles)); tr, te = cles[:n_tr], cles[n_tr:]
    prompts_fr = [" ".join(series[k][0][:a.prompt]) for k in range(len(series))]
    prompts_en = [" ".join(series[k][1][:a.prompt]) for k in range(len(series))]
    cibles_fr = [series[k][0][a.prompt] for k in range(len(series))]
    cibles_en = [series[k][1][a.prompt] for k in range(len(series))]
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float16).to("cuda").eval()

    def etats(textes, max_len):
        out = []
        for i in range(0, len(textes), a.batch):
            enc = tok(textes[i:i + a.batch], return_tensors="pt", padding=True, truncation=True,
                      max_length=max_len).to("cuda")
            with torch.no_grad():
                hs = model(**enc, output_hidden_states=True).hidden_states
            idx = enc["attention_mask"].sum(1) - 1
            out.append(hs[a.couche][torch.arange(len(idx)), idx].float().cpu().numpy())
        return np.concatenate(out, 0)

    print("  extraction des états…")
    Pfr, Pen = etats(prompts_fr, 256), etats(prompts_en, 256)
    Cfr, Cen = etats(cibles_fr, 128), etats(cibles_en, 128)
    Pfr_n, Pen_n, Cfr_n, Cen_n = norm(Pfr), norm(Pen), norm(Cfr), norm(Cen)

    def pont(Xe, Xf, lam=10.0):
        A = np.hstack([Xe, np.ones((len(Xe), 1), np.float32)])
        return np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1], dtype=np.float32), A.T @ Xf)

    def appliquer(X, W):
        return norm(np.hstack([X, np.ones((len(X), 1), np.float32)]) @ W)

    W = pont(Pen_n[tr], Pfr_n[tr])
    mel = np.random.default_rng(7).permutation(tr)
    Wn = pont(Pen_n[mel], Pfr_n[tr])
    res = {"couche": a.couche, "n_series": len(series), "hasard": 0.125}
    justes = {k: 0 for k in ("fr_fr", "en_en", "en_fr_sans_pont", "en_fr_pont", "en_fr_pont_melange")}
    tot = 0
    for i in range(0, len(te) - 7, 8):
        groupe = te[i:i + 8]
        cand_fr = Cfr_n[groupe]; cand_en = Cen_n[groupe]
        c = np.arange(8)
        justes["fr_fr"] += int(np.sum(np.argmax(Pfr_n[groupe] @ cand_fr.T, 1) == c))
        justes["en_en"] += int(np.sum(np.argmax(Pen_n[groupe] @ cand_en.T, 1) == c))
        justes["en_fr_sans_pont"] += int(np.sum(np.argmax(Pen_n[groupe] @ cand_fr.T, 1) == c))
        justes["en_fr_pont"] += int(np.sum(np.argmax(appliquer(Pen[groupe], W) @ cand_fr.T, 1) == c))
        justes["en_fr_pont_melange"] += int(np.sum(np.argmax(appliquer(Pen[groupe], Wn) @ cand_fr.T, 1) == c))
        tot += 8
    res["resultats"] = {k: round(v / max(1, tot), 4) for k, v in justes.items()}
    res["n_test"] = tot
    print(f"  FR→FR {res['resultats']['fr_fr']:.3f} · EN→EN {res['resultats']['en_en']:.3f} · "
          f"EN→FR sans pont {res['resultats']['en_fr_sans_pont']:.3f} · **pont {res['resultats']['en_fr_pont']:.3f}** · "
          f"pont mélangé {res['resultats']['en_fr_pont_melange']:.3f} (hasard 0,125)")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
