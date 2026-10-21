#!/usr/bin/env python3
"""lora_pidgin_mixte.py — L'ÉCRITURE DU PIDGIN PAR ENTRAÎNEMENT MÉLANGÉ (BBC + contes + anglais).

POURQUOI ✓✓. Les mesures 90-91 ont montré que le LoRA supervisé **mémorise** et que le LoRA monolingue **détruit** la
traduction (oubli catastrophique) ✗✗. On mélange : **50 % de pidgin** (1 840 articles BBC + 39 pages de contes),
**25 % de traduction** eng → pcm (les 39 pages), **25 % d'anglais** (replay) ✓✓ ; LoRA sur les **12 dernières
couches**, lr **1e-5** (doux) ✓✓. On évalue la traduction eng → pcm sur le conte tenu à part (0210), la lecture
pcm → eng, et une **traduction générale** eng → fra (10 phrases de Verne) pour détecter l'oubli ✓✓.
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
    ap.add_argument("--pas", type=int, default=300)
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--sortie", default="reports/lora-pidgin-mixte-3b.json")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model
    d = json.loads(pathlib.Path("data/pidgin/pidgin.json").read_text())
    train = [u for u in d["unites"] if u["histoire"] != "0210"]
    test = [u for u in d["unites"] if u["histoire"] == "0210"]
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
        for nom, (src, dst, prompt) in {
            "eng→pcm": ("eng", "pcm", p_pcm),
            "pcm→eng": ("pcm", "eng", p_eng),
        }.items():
            sc, pl = [], []
            for u in test:
                sc.append(chrf(genere(prompt(u["textes"][src])), u["textes"][dst]))
                pl.append(chrf(u["textes"][src], u["textes"][dst]))
            dd = np.array(sc) - np.array(pl)
            rng = np.random.default_rng(1234)
            boot = [float(np.mean(rng.choice(dd, len(dd), replace=True))) for _ in range(2000)]
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
    for step in range(a.pas):
        r = rng.random()
        if r < 0.5:
            lot = [tok(rng.choice(mono), add_special_tokens=False)["input_ids"][:256] for _ in range(2)]
            labels = [x[:] for x in lot]
        elif r < 0.75:
            lot, labels = [], []
            for u in rng.sample(train, 2):
                p = tok(p_pcm(u["textes"]["eng"]), add_special_tokens=False)["input_ids"]
                t = tok(" " + u["textes"]["pcm"] + tok.eos_token, add_special_tokens=False)["input_ids"]
                lot.append((p + t)[:256])
                labels.append(([-100] * len(p) + t)[:256])
        else:
            ids = tok(anglais, add_special_tokens=False)["input_ids"]
            deb = rng.randrange(0, max(1, len(ids) - 300))
            lot = [ids[deb:deb + 256], ids[deb + 256:deb + 512]]
            labels = [x[:] for x in lot]
        L = max(len(x) for x in lot)
        ids = torch.tensor([[tok.pad_token_id] * (L - len(x)) + x for x in lot]).to("cuda")
        lab = torch.tensor([[-100] * (L - len(y)) + y for y in labels]).to("cuda")
        att = (ids != tok.pad_token_id).long()
        s = model(input_ids=ids, attention_mask=att, labels=lab)
        s.loss.backward(); opt.step(); opt.zero_grad(); pertes.append(float(s.loss))
        if step % 50 == 0:
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
