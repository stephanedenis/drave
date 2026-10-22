#!/usr/bin/env python3
"""plan_entrainement_bilingue.py — ÉTAGE 2 : entraîner l'état de PLAN en bilingue (FR/EN), et voir si l'EN→FR s'aligne.

POURQUOI ✓✓. Les mesures 132-134 et 153 ont montré que l'état de plan **ne s'aligne pas** par un pont (ni par
l'adaptateur du raisonnement) : chaque tâche a sa géométrie. La seule voie restante est d'**entraîner le plan
lui-même**, dans les deux langues, avec son objectif propre (le prompt de 4 phrases doit retrouver la 5ᵉ parmi 8) ✓✓.

CE QU'ON MESURE ✓✓ (hasard 12,5 %) :
  1. **FR→FR** et **EN→EN** (in-langue) ✓✓ ;
  2. **EN→FR** (le prompt EN contre les cibles FR) — l'alignement cherché ✓✓ ;
  3. le contrôle : le modèle **figé** (mesure 132 : 0,250) et l'adaptateur de raisonnement (mesure 153 : 0,273) ✓✓.

CE QUE CHAQUE ISSUE VEUT DIRE ✓✓ :
  · l'EN→FR monte au-dessus de 0,25 → l'entraînement bilingue **aligne le plan** ✓✓ ;
  · il reste à ~0,25 → la géométrie du plan résiste ; il faudra un objectif cross-lingue explicite ✓✗.
"""
from __future__ import annotations
import argparse, json, pathlib, random
import numpy as np


def norm(x):
    return x / np.maximum(1e-9, np.linalg.norm(x, axis=1, keepdims=True))


def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--couche", type=int, default=18)
    ap.add_argument("--pas", type=int, default=800)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--accum", type=int, default=2)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--tau", type=float, default=0.05)
    ap.add_argument("--graine", type=int, default=1234)
    ap.add_argument("--sortie", default="reports/plan-bilingue-3b.json")
    ap.add_argument("--langue", choices=["both", "fr", "en"], default="both")
    ap.add_argument("--sauver", default="")
    a = ap.parse_args()
    import torch
    import torch.nn as nn
    from transformers import AutoModel, AutoTokenizer
    from peft import LoraConfig, get_peft_model
    torch.manual_seed(a.graine); random.seed(a.graine); np.random.seed(a.graine)
    # séries Verne appariées
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
    pas_ech = max(1, len(series) // 315)
    series = series[::pas_ech][:315]
    rng = np.random.default_rng(a.graine)
    cles = np.arange(len(series)); rng.shuffle(cles)
    n_tr = int(0.7 * len(cles)); tr, te = cles[:n_tr], cles[n_tr:]
    print(f"  {len(series)} séries ({len(tr)} train, {len(te)} test)")
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    base = AutoModel.from_pretrained(a.hf, dtype=torch.float16).to("cuda")
    lora = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, bias="none", task_type="FEATURE_EXTRACTION",
                      target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
    model = get_peft_model(base, lora)
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=a.lr)
    scaler = torch.amp.GradScaler("cuda")

    def lot(textes, max_len):
        enc = tok(textes, return_tensors="pt", padding=True, truncation=True, max_length=max_len).to("cuda")
        return enc

    def etats(textes, max_len=256):
        enc = lot(textes, max_len)
        hs = model(**enc, output_hidden_states=True, use_cache=False).hidden_states
        idx = enc["attention_mask"].sum(1) - 1
        return hs[a.couche][torch.arange(len(idx)), idx].float()

    model.train()
    for pas in range(1, a.pas + 1):
        langue = ("fr", "en")[pas % 2] if a.langue == "both" else a.langue
        k = random.sample(list(tr), a.batch)
        textes_p = [" ".join(series[int(j)][0 if langue == "fr" else 1][:4]) for j in k]
        textes_t = [series[int(j)][0 if langue == "fr" else 1][4] for j in k]
        with torch.autocast("cuda", dtype=torch.float16):
            zp = etats(textes_p, 256)
            zt = etats(textes_t, 128)
        logits = nn.functional.normalize(zp, dim=1) @ nn.functional.normalize(zt, dim=1).T / a.tau
        cible = torch.arange(len(k), device="cuda")
        perte = nn.functional.cross_entropy(logits, cible)
        scaler.scale(perte / a.accum).backward()
        if pas % a.accum == 0:
            scaler.step(opt); scaler.update(); opt.zero_grad()
        if pas % 50 == 0:
            print(f"  pas {pas} · perte {float(perte):.3f}")
    model.eval()
    if a.sauver:
        dd = pathlib.Path(a.sauver); dd.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(dd); print(f"  adaptateur → {dd}")

    @torch.no_grad()
    def etats_eval(textes, max_len):
        out = []
        for i in range(0, len(textes), 8):
            out.append(etats(textes[i:i + 8], max_len).cpu().numpy())
        return np.concatenate(out, 0)

    Pfr = norm(etats_eval([" ".join(s[0][:4]) for s in series], 256))
    Pen = norm(etats_eval([" ".join(s[1][:4]) for s in series], 256))
    Cfr = norm(etats_eval([s[0][4] for s in series], 128))
    Cen = norm(etats_eval([s[1][4] for s in series], 128))
    justes = {k: 0 for k in ("fr_fr", "en_en", "en_fr")}
    tot = 0
    for i in range(0, len(te) - 7, 8):
        g = te[i:i + 8]; c = np.arange(8)
        justes["fr_fr"] += int(np.sum(np.argmax(Pfr[g] @ Cfr[g].T, 1) == c))
        justes["en_en"] += int(np.sum(np.argmax(Pen[g] @ Cen[g].T, 1) == c))
        justes["en_fr"] += int(np.sum(np.argmax(Pen[g] @ Cfr[g].T, 1) == c))
        tot += 8
    res = {"couche": a.couche, "pas": a.pas, "batch": a.batch, "hasard": 0.125, "n_test": tot,
           "resultats": {k: round(v / max(1, tot), 4) for k, v in justes.items()}}
    for k, v in res.items():
        print(f"  {k}: {v}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
