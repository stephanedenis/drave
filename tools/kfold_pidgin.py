#!/usr/bin/env python3
"""kfold_pidgin.py — LA VALIDATION CROISÉE DU PIDGIN (5 contes) : l'écriture passe-t-elle le plancher sur 50 pages ?

POURQUOI ✓✓. La mesure 92 a amélioré l'écriture (+1,2) sur **11 pages** seulement ✗✗. On fait une **validation
croisée par conte** : pour chacun des **5 contes**, on entraîne un LoRA **mélangé** (BBC + les 4 autres contes +
anglais) et on teste sur le conte **tenu à part** ✓✓. Les **50 pages** sont ainsi testées, chacune par un modèle qui
ne l'a jamais vue ✓✓ — le test le plus propre de la **production** du pidgin ✓✓.
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--pas", type=int, default=300)
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--sortie", default="reports/kfold-pidgin.json")
    ap.add_argument("--repartir", action="store_true", help="répartir le modèle sur les deux cartes (7 B)")
    ap.add_argument("--batch", type=int, default=2)
    ap.add_argument("--max-jetons", type=int, default=256)
    ap.add_argument("--huit-bit", action="store_true", help="charger le modèle en 8 bits (bitsandbytes)")
    ap.add_argument("--test", default=None, help="ne faire qu'un pli (conte de test)")
    ap.add_argument("--bible", default=None, help="paires bibliques à mélanger (50/50 avec translatewiki)")
    ap.add_argument("--sans-checkpointing", action="store_true", help="désactiver le gradient checkpointing")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    d = json.loads(pathlib.Path("data/pidgin/pidgin.json").read_text())
    mono = json.loads(pathlib.Path("data/pidgin/mono_bbc_clean.json").read_text())
    anglais = pathlib.Path("data/corpus_en_val.txt").read_text(encoding="utf-8", errors="ignore")[:2_000_000]
    tw_en = pathlib.Path("data/pidgin/translatewiki_en.txt").read_text(encoding="utf-8", errors="ignore").splitlines()
    tw_pcm = pathlib.Path("data/pidgin/translatewiki_pcm.txt").read_text(encoding="utf-8", errors="ignore").splitlines()
    tw = [(a.strip(), b.strip()) for a, b in zip(tw_en, tw_pcm) if len(a.strip()) > 2 and len(b.strip()) > 2]
    bible = json.loads(pathlib.Path(a.bible).read_text()) if a.bible else []
    print(f"  {len(tw)} paires translatewiki · {len(bible)} paires bibliques")
    histoires = ([a.test] if a.test else sorted({u["histoire"] for u in d["unites"]}))
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    resultats = []
    for test_h in histoires:
        train = [u for u in d["unites"] if u["histoire"] != test_h]
        test = [u for u in d["unites"] if u["histoire"] == test_h]
        if a.huit_bit:
            from transformers import BitsAndBytesConfig
            bnb = BitsAndBytesConfig(load_in_8bit=True)
            model = AutoModelForCausalLM.from_pretrained(a.hf, quantization_config=bnb,
                                                         device_map="auto").eval()
            model = prepare_model_for_kbit_training(model)
        elif a.repartir:
            model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float16,
                                                         device_map="auto").eval()
        else:
            model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float16).to("cuda").eval()
        n_couches = model.config.num_hidden_layers
        debut = max(0, n_couches - 12)
        config = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, bias="none", task_type="CAUSAL_LM",
                            target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
                            layers_to_transform=list(range(debut, n_couches)), layers_pattern="layers")
        model = get_peft_model(model, config)
        if (a.repartir or a.huit_bit) and not a.sans_checkpointing:
            model.gradient_checkpointing_enable()
            model.enable_input_require_grads()
        opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=a.lr)
        rng = random.Random(1234)
        ids_en = tok(anglais, add_special_tokens=False)["input_ids"]
        for step in range(a.pas):
            r = rng.random()
            if r < 0.35:
                # paires translatewiki : la MÊME consigne de traduction, cible pidgin ✓✓
                lot, labels = [], []
                for _ in range(a.batch):
                    if bible and rng.random() < 0.5:
                        paire = rng.choice(bible); src_, tgt_ = paire["en"], paire["pcm"]
                    else:
                        src_, tgt_ = rng.choice(tw)
                    p = tok(p_pcm(src_), add_special_tokens=False)["input_ids"][:128]
                    t = tok(" " + tgt_ + tok.eos_token, add_special_tokens=False)["input_ids"][:a.max_jetons]
                    lot.append((p + t)[:a.max_jetons]); labels.append(([-100] * len(p) + t)[:a.max_jetons])
            elif r < 0.6:
                lot = [tok(rng.choice(mono), add_special_tokens=False)["input_ids"][:a.max_jetons] for _ in range(a.batch)]
                labels = [x[:] for x in lot]
            elif r < 0.85:
                lot, labels = [], []
                for u in rng.sample(train, a.batch):
                    p = tok(p_pcm(u["textes"]["eng"]), add_special_tokens=False)["input_ids"][:128]
                    t = tok(" " + u["textes"]["pcm"] + tok.eos_token, add_special_tokens=False)["input_ids"][:a.max_jetons]
                    lot.append((p + t)[:a.max_jetons]); labels.append(([-100] * len(p) + t)[:a.max_jetons])
            else:
                deb = rng.randrange(0, max(1, len(ids_en) - 600))
                lot = [ids_en[deb:deb + a.max_jetons] for _ in range(a.batch)]
                labels = [x[:] for x in lot]
            L = max(len(x) for x in lot)
            ids = torch.tensor([[tok.pad_token_id] * (L - len(x)) + x for x in lot]).to("cuda")
            lab = torch.tensor([[-100] * (L - len(y)) + y for y in labels]).to("cuda")
            att = (ids != tok.pad_token_id).long()
            s = model(input_ids=ids, attention_mask=att, labels=lab)
            s.loss.backward(); opt.step(); opt.zero_grad()
        model.eval()
        for u in test:
            ids = tok(p_pcm(u["textes"]["eng"]), return_tensors="pt").to(model.device)
            with torch.no_grad():
                g = model.generate(**ids, max_new_tokens=200, do_sample=False, pad_token_id=tok.eos_token_id)
            sortie = tok.decode(g[0][ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()
            resultats.append({"histoire": test_h, "chrf": chrf(sortie, u["textes"]["pcm"]),
                              "plancher": chrf(u["textes"]["eng"], u["textes"]["pcm"])})
        m = np.array([x["chrf"] - x["plancher"] for x in resultats if x["histoire"] == test_h])
        print(f"  {test_h} : n {len(m)} · marge {m.mean():+.1f} · >0 {int((m > 0).sum())}/{len(m)}")
        del model
        torch.cuda.empty_cache()
    dd = np.array([x["chrf"] - x["plancher"] for x in resultats])
    rng = np.random.default_rng(1234)
    boot = [float(np.mean(rng.choice(dd, len(dd), replace=True))) for _ in range(5000)]
    resume = {"n": len(dd), "marge": round(float(dd.mean()), 1),
              "ic95": [round(float(np.percentile(boot, 2.5)), 1), round(float(np.percentile(boot, 97.5)), 1)],
              "positives": int((dd > 0).sum()), "chrf": round(float(np.mean([x["chrf"] for x in resultats])), 1),
              "plancher": round(float(np.mean([x["plancher"] for x in resultats])), 1)}
    print(f"  POOLÉ : chrF {resume['chrf']} · plancher {resume['plancher']} · marge {resume['marge']:+} · "
          f"IC {resume['ic95']} · >0 {resume['positives']}/{resume['n']}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({"pas": a.pas, "resume": resume, "pages": resultats},
                                                 ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
