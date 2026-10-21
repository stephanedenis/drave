#!/usr/bin/env python3
"""lora_pidgin.py — L'ÉCRITURE DU PIDGIN EST-ELLE APPRENABLE SUR 39 PAGES ?

POURQUOI ✓✓. La mesure 89 a montré que le modèle **lit** le pidgin (pcm → eng : +3,2 au 7 B, +4,4 au 14 B) mais ne
l'**écrit** pas (eng → pcm : −1,5 au 7 B, +2,3 marginal au 14 B, −6,9 en few-shot) ✗✗. *Est-ce un manque de
**données** ou une **incapacité** ?* ✓✓ On entraîne un **LoRA** sur **4 contes** (39 pages) et on teste sur le
**5ᵉ conte** (11 pages), tenu à part ✓✓. Si l'écriture passe le plancher, elle est **apprenable sur presque rien** ;
sinon, il faut plus de données ✓✓.

⚠️ CE QUE CELA NE DIT PAS ✗ : 39 pages d'entraînement, 11 de test, un corpus **non post-cutoff** ✓✗ ; le LoRA
apprend la **surface** du pidgin, pas la langue ✓✓ ; et le test est un **seul** conte ✓✗.
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


def prompt(en: str) -> str:
    return f"Translate into Nigerian Pidgin (Naijá).\nEnglish: {en}\nNigerian Pidgin:"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--dtype", default="float16")
    ap.add_argument("--epoques", type=int, default=30)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--rang", type=int, default=16)
    ap.add_argument("--sortie", default="reports/lora-pidgin.json")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model
    data = json.loads(pathlib.Path("data/pidgin/pidgin.json").read_text())
    unites = data["unites"]
    histoires = sorted({u["histoire"] for u in unites})
    train_h, test_h = histoires[:-1], histoires[-1]
    train = [u for u in unites if u["histoire"] in train_h]
    test = [u for u in unites if u["histoire"] == test_h]
    print(f"  train {len(train)} pages ({len(train_h)} contes) · test {len(test)} pages ({test_h})")
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=getattr(torch, a.dtype)).to("cuda").eval()

    def genere(p: str) -> str:
        ids = tok(p, return_tensors="pt").to(model.device)
        with torch.no_grad():
            g = model.generate(**ids, max_new_tokens=200, do_sample=False, pad_token_id=tok.eos_token_id)
        return tok.decode(g[0][ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()

    def evalue() -> dict:
        scores, planchers = [], []
        for u in test:
            p = prompt(u["textes"]["eng"])
            sortie = genere(p)
            scores.append(chrf(sortie, u["textes"]["pcm"]))
            planchers.append(chrf(u["textes"]["eng"], u["textes"]["pcm"]))
        d = np.array(scores) - np.array(planchers)
        rng = np.random.default_rng(1234)
        boot = [float(np.mean(rng.choice(d, len(d), replace=True))) for _ in range(3000)]
        return {"chrf": round(float(np.mean(scores)), 1), "plancher": round(float(np.mean(planchers)), 1),
                "marge": round(float(np.mean(d)), 1),
                "ic95": [round(float(np.percentile(boot, 2.5)), 1), round(float(np.percentile(boot, 97.5)), 1)],
                "positives": int((d > 0).sum()), "n": len(d)}

    avant = evalue()
    print(f"  avant LoRA : chrF {avant['chrf']} · plancher {avant['plancher']} · marge {avant['marge']:+} · IC {avant['ic95']}")

    # entraînement : la perte ne porte QUE sur la cible pidgin ✓
    exemples = []
    for u in train:
        p_ids = tok(prompt(u["textes"]["eng"]), add_special_tokens=False)["input_ids"]
        t_ids = tok(" " + u["textes"]["pcm"] + tok.eos_token, add_special_tokens=False)["input_ids"]
        ids = (p_ids + t_ids)[:256]
        labels = ([-100] * len(p_ids) + t_ids)[:256]
        exemples.append((ids, labels))
    config = LoraConfig(r=a.rang, lora_alpha=2 * a.rang, lora_dropout=0.05, bias="none",
                        task_type="CAUSAL_LM", target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
    model = get_peft_model(model, config)
    model.print_trainable_parameters()
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=a.lr)
    rng = random.Random(1234)
    for ep in range(a.epoques):
        rng.shuffle(exemples); total = 0.0; nb = 0
        for i in range(0, len(exemples) - 3, 4):
            lot = exemples[i:i + 4]
            L = max(len(x[0]) for x in lot)
            ids = torch.tensor([[tok.pad_token_id] * (L - len(x[0])) + x[0] for x in lot]).to("cuda")
            lab = torch.tensor([[-100] * (L - len(x[1])) + x[1] for x in lot]).to("cuda")
            att = (ids != tok.pad_token_id).long()
            sortie = model(input_ids=ids, attention_mask=att, labels=lab)
            sortie.loss.backward(); opt.step(); opt.zero_grad()
            total += float(sortie.loss); nb += 1
        if ep % 5 == 0:
            print(f"  époque {ep} · perte {total / max(1, nb):.3f}")
    model.eval()
    apres = evalue()
    print(f"  après LoRA : chrF {apres['chrf']} · plancher {apres['plancher']} · marge {apres['marge']:+} · IC {apres['ic95']}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({"hf": a.hf, "rang": a.rang, "epoques": a.epoques,
                                                  "train": train_h, "test": test_h,
                                                  "avant": avant, "apres": apres}, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
