#!/usr/bin/env python3
"""lora_pidgin_bbc.py — LA PRODUCTION DU PIDGIN S'APPREND-ELLE SUR BBC SEUL ? (test sur les 50 pages)

POURQUOI ✓✓. La mesure 92 a amélioré l'écriture (+1,2) avec un mélange **50 % pidgin / 25 % traduction / 25 %
anglais**, testé sur **11 pages** seulement ✗✗. Ici, on retire les **paires de traduction** : on entraîne sur
**BBC Pidgin seul** (+ replay anglais) et on teste sur **les 50 pages** des contes, jamais vues ✓✓. *La production
s'apprend-elle sur un corpus monolingue de 1 840 articles, et le gain est-il significatif sur 50 pages ?* ✓✓
"""
from __future__ import annotations
import argparse, json, pathlib, random
import numpy as np


def chrf(hyp: str, ref: str, n_max: int = 6, beta: float = 2.0) -> float:
    from collections import Counter
    hyp = " ".join(hyp.split()); ref = " ".join(ref.split())
    if not hyp or not ref:
        return 0.0
    prec, rec = [], []
    for n in range(1, n_max + 1):
        H = [hyp[i:i + n] for i in range(max(0, len(hyp) - n + 1))]
        R = [ref[i:i + n] for i in range(max(0, len(ref) - n + 1))]
        ch, cr = Counter(H), Counter(R)
        inter = sum((ch & cr).values())
        prec.append(inter / max(1, len(H))); rec.append(inter / max(1, len(R)))
    p, r = float(np.mean(prec)), float(np.mean(rec))
    b2 = beta * beta
    return 100 * (1 + b2) * p * r / max(1e-9, b2 * p + r)


def p_pcm(en: str) -> str:
    return f"Translate into Nigerian Pidgin (Naijá).\nEnglish: {en}\nNigerian Pidgin:"


def p_eng(pcm: str) -> str:
    return f"Translate from Nigerian Pidgin (Naijá) into English.\nNigerian Pidgin: {pcm}\nEnglish:"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--pas", type=int, default=400)
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--sortie", default="reports/lora-pidgin-bbc-3b.json")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model
    d = json.loads(pathlib.Path("data/pidgin/pidgin.json").read_text())
    test = d["unites"]  # les 50 pages, jamais vues à l'entraînement
    mono = json.loads(pathlib.Path("data/pidgin/mono_bbc_clean.json").read_text())
    anglais = pathlib.Path("data/corpus_en_val.txt").read_text(encoding="utf-8", errors="ignore")[:2_000_000]
    verne = json.loads(pathlib.Path("data/alignement/verne_fr_en.json").read_text())
    paires = [p for p in verne["paires"] if p.get("n_fr") == 1 and p.get("n_en") == 1][:10]
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float16).to("cuda").eval()

    def genere(p: str, n: int = 200) -> str:
        ids = tok(p, return_tensors="pt").to(model.device)
        with torch.no_grad():
            g = model.generate(**ids, max_new_tokens=n, do_sample=False, pad_token_id=tok.eos_token_id)
        return tok.decode(g[0][ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()

    def evalue() -> dict:
        res = {}
        for nom, (src, dst, pr) in {"eng→pcm": ("eng", "pcm", p_pcm), "pcm→eng": ("pcm", "eng", p_eng)}.items():
            sc, pl = [], []
            for u in test:
                sc.append(chrf(genere(pr(u["textes"][src])), u["textes"][dst]))
                pl.append(chrf(u["textes"][src], u["textes"][dst]))
            dd = np.array(sc) - np.array(pl)
            rng = np.random.default_rng(1234)
            boot = [float(np.mean(rng.choice(dd, len(dd), replace=True))) for _ in range(3000)]
            res[nom] = {"chrf": round(float(np.mean(sc)), 1), "plancher": round(float(np.mean(pl)), 1),
                        "marge": round(float(np.mean(dd)), 1),
                        "ic95": [round(float(np.percentile(boot, 2.5)), 1),
                                 round(float(np.percentile(boot, 97.5)), 1)],
                        "positives": int((dd > 0).sum()), "n": len(dd)}
        sc, pl = [], []
        for p in paires:
            sc.append(chrf(genere(f"Translate into French:\n{p['en']}\nFrench:", 150), p["fr"]))
            pl.append(chrf(p["en"], p["fr"]))
        res["eng→fra"] = {"chrf": round(float(np.mean(sc)), 1), "plancher": round(float(np.mean(pl)), 1),
                          "marge": round(float(np.mean(sc) - np.mean(pl)), 1), "n": len(paires)}
        return res

    avant = evalue()
    print(f"  avant : {json.dumps(avant, ensure_ascii=False)}")
    config = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, bias="none", task_type="CAUSAL_LM",
                        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
                        layers_to_transform=list(range(24, 36)), layers_pattern="layers")
    model = get_peft_model(model, config)
    model.print_trainable_parameters()
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=a.lr)
    rng = random.Random(1234)
    pertes = []
    ids_en = tok(anglais, add_special_tokens=False)["input_ids"]
    for step in range(a.pas):
        if rng.random() < 0.7:
            lot = [tok(rng.choice(mono), add_special_tokens=False)["input_ids"][:256] for _ in range(2)]
        else:
            deb = rng.randrange(0, max(1, len(ids_en) - 600))
            lot = [ids_en[deb:deb + 256], ids_en[deb + 256:deb + 512]]
        L = max(len(x) for x in lot)
        ids = torch.tensor([[tok.pad_token_id] * (L - len(x)) + x for x in lot]).to("cuda")
        lab = ids.clone(); lab[ids == tok.pad_token_id] = -100
        att = (ids != tok.pad_token_id).long()
        s = model(input_ids=ids, attention_mask=att, labels=lab)
        s.loss.backward(); opt.step(); opt.zero_grad(); pertes.append(float(s.loss))
        if step % 100 == 0:
            print(f"  pas {step} · perte {np.mean(pertes[-20:]):.3f}")
    model.eval()
    apres = evalue()
    print(f"  après : {json.dumps(apres, ensure_ascii=False)}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({"hf": a.hf, "pas": a.pas, "textes": len(mono),
                                                  "avant": avant, "apres": apres}, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
