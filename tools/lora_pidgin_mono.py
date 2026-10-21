#!/usr/bin/env python3
"""lora_pidgin_mono.py — L'ÉCRITURE DU PIDGIN PAR ADAPTATION MONOLINGUE (BBC Pidgin + contes, sans le test).

POURQUOI ✓✓. La mesure 90 a montré qu'un LoRA **supervisé** sur 39 pages mémorise sans transférer ✗✗. Mais le
modèle **lit** le pidgin (mesure 89) : il lui manque la **production**. *Une adaptation **monolingue** — voir
beaucoup de pidgin, sans paires — apprend-elle la surface ?* ✓✓ On entraîne un LoRA sur **24 articles BBC Pidgin**
et les **pages des contes d'entraînement** (le conte de test 0210 est **exclu**), puis on évalue la traduction
eng → pcm sur le conte tenu à part ✓✓.

⚠️ CE QUE CELA NE DIT PAS ✗ : 63 textes seulement, un registre mixte (presse + contes), un conte de test ✓✗.
"""
from __future__ import annotations
import argparse, json, pathlib
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
    ap.add_argument("--epoques", type=int, default=2)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--sortie", default="reports/lora-pidgin-mono-3b.json")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import LoraConfig, get_peft_model
    d = json.loads(pathlib.Path("data/pidgin/pidgin.json").read_text())
    test = [u for u in d["unites"] if u["histoire"] == "0210"]
    textes = json.loads(pathlib.Path("data/pidgin/mono.json").read_text())
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
        sc, pl = [], []
        for u in test:
            sc.append(chrf(genere(prompt(u["textes"]["eng"])), u["textes"]["pcm"]))
            pl.append(chrf(u["textes"]["eng"], u["textes"]["pcm"]))
        dd = np.array(sc) - np.array(pl)
        rng = np.random.default_rng(1234)
        boot = [float(np.mean(rng.choice(dd, len(dd), replace=True))) for _ in range(3000)]
        return {"chrf": round(float(np.mean(sc)), 1), "plancher": round(float(np.mean(pl)), 1),
                "marge": round(float(np.mean(dd)), 1),
                "ic95": [round(float(np.percentile(boot, 2.5)), 1), round(float(np.percentile(boot, 97.5)), 1)],
                "positives": int((dd > 0).sum()), "n": len(dd)}

    avant = evalue()
    print(f"  avant : chrF {avant['chrf']} · plancher {avant['plancher']} · marge {avant['marge']:+} · IC {avant['ic95']}")
    # corpus monolingue : concaténer les textes, découper en blocs de 256 jetons
    ids_all = []
    for t in textes:
        ids_all += tok(t, add_special_tokens=False)["input_ids"] + [tok.eos_token_id]
    blocs = [ids_all[i:i + 256] for i in range(0, len(ids_all) - 256, 256)]
    print(f"  {len(textes)} textes · {len(ids_all)} jetons · {len(blocs)} blocs")
    config = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, bias="none", task_type="CAUSAL_LM",
                        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
    model = get_peft_model(model, config)
    model.print_trainable_parameters()
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=a.lr)
    import random
    rng = random.Random(1234)
    for ep in range(a.epoques):
        rng.shuffle(blocs); total = 0.0; nb = 0
        for i in range(0, len(blocs) - 1, 2):
            lot = blocs[i:i + 2]
            L = max(len(x) for x in lot)
            ids = torch.tensor([[tok.pad_token_id] * (L - len(x)) + x for x in lot]).to("cuda")
            lab = ids.clone(); lab[ids == tok.pad_token_id] = -100
            att = (ids != tok.pad_token_id).long()
            s = model(input_ids=ids, attention_mask=att, labels=lab)
            s.loss.backward(); opt.step(); opt.zero_grad(); total += float(s.loss); nb += 1
        print(f"  époque {ep} · perte {total / max(1, nb):.3f}")
    model.eval()
    apres = evalue()
    print(f"  après : chrF {apres['chrf']} · plancher {apres['plancher']} · marge {apres['marge']:+} · IC {apres['ic95']}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({"hf": a.hf, "epoques": a.epoques, "textes": len(textes),
                                                  "avant": avant, "apres": apres}, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
