#!/usr/bin/env python3
"""composition_latente.py — ÉTAGE 2 : un état latent ENTRAÎNÉ AVEC LA TÂCHE (pas des états figés).

POURQUOI ✓✓. Toutes les mesures de dynamique (82, 83, 87, 88, 108) ont utilisé des états **figés** du modèle et un
opérateur appris **après coup** : le linéaire tient deux pas, la contraction dégrade, le MLP sur-apprend, la
récurrence partagée ne tient pas ✗✗. La seule piste qui reste : entraîner **ensemble** l'état (par un LoRA sur le
modèle) et le **pas partagé** F — l'état latent est optimisé **pour** la dynamique, pas seulement lu ✓✓.

LE TEST ✓✓ : les 200 phrases anglaises des 50 séries de 4 (Verne, paires strictes 1:1) ; le modèle 3 B + LoRA sur
les 12 dernières couches ; F = x + MLP(x) partagé ; la perte multi-pas F¹/F²/F³ depuis la phrase 0 + les
transitions ; les cibles **détachées** (pour que le modèle ne puisse pas tout écraser) ✓✓. L'évaluation est la même
que la mesure 82 : le retrieval de la bonne position parmi les 4 phrases de la série (hasard 25 %) aux pas 1, 2, 3,
sur les séries **tenues à part** ✓✓.

⚠️ CE QUE CELA NE DIT PAS ✗ : 50 séries, un LoRA, 300 pas ; et le retrieval à 4 candidats est un test dur ✓✗.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np
import torch
import torch.nn.functional as Fn
from peft import LoraConfig, get_peft_model


def norm(x):
    return x / x.norm(dim=-1, keepdim=True).clamp_min(1e-9)


class Pas(torch.nn.Module):
    def __init__(self, d: int, cache: int = 256):
        super().__init__()
        self.f = torch.nn.Sequential(torch.nn.Linear(d, cache), torch.nn.GELU(), torch.nn.Linear(cache, d))

    def forward(self, x):
        return x + self.f(x)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--couche", type=int, default=18)
    ap.add_argument("--series", type=int, default=50)
    ap.add_argument("--pas", type=int, default=300)
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--sortie", default="reports/composition-latente.json")
    ap.add_argument("--repartir", action="store_true", help="répartir le modèle sur les deux cartes (14 B)")
    a = ap.parse_args()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    # données : les mêmes séries que la mesure 82 (Verne FR/EN, 1:1)
    d = json.loads(pathlib.Path("data/alignement/verne_fr_en.json").read_text())
    paires = [p for p in d["paires"] if p.get("n_fr") == 1 and p.get("n_en") == 1]
    par_chap = {}
    for p in paires:
        par_chap.setdefault(p["chapitre"], []).append(p)
    series = []
    for ch in sorted(par_chap):
        ps = sorted(par_chap[ch], key=lambda p: p["i_fr"])
        for i in range(0, len(ps) - 4 + 1, 4):
            bloc = ps[i:i + 4]
            if len(bloc) == 4:
                series.append([p["en"] for p in bloc])
    pas_ = max(1, len(series) // a.series)
    series = series[::pas_][: a.series]
    rng = np.random.default_rng(1234)
    cles = np.arange(len(series)); rng.shuffle(cles)
    n_tr = int(0.7 * len(cles))
    train_s, test_s = [series[k] for k in cles[:n_tr]], [series[k] for k in cles[n_tr:]]
    print(f"  {len(train_s)} séries d'entraînement · {len(test_s)} de test")
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    if a.repartir:
        base = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float16, device_map="auto").eval()
    else:
        base = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float16).to("cuda").eval()
    n_layers = base.config.num_hidden_layers
    debut = max(0, n_layers - 12)
    cfg = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, bias="none", task_type="CAUSAL_LM",
                     target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
                     layers_to_transform=list(range(debut, n_layers)), layers_pattern="layers")
    model = get_peft_model(base, cfg)
    modele_pas = Pas(model.config.hidden_size).cuda()
    opt = torch.optim.AdamW([
        {"params": [p for p in model.parameters() if p.requires_grad], "lr": a.lr},
        {"params": list(modele_pas.parameters()), "lr": 1e-3},  # le pas apprend vite, le modèle doucement
    ])

    def etats(phrases, max_len=256):
        enc = tok(phrases, return_tensors="pt", padding=True, truncation=True, max_length=max_len).to("cuda")
        hs = model(**enc, output_hidden_states=True).hidden_states
        idx = enc["attention_mask"].sum(1) - 1
        return hs[a.couche][torch.arange(len(phrases)), idx].float().to("cuda")

    for step in range(1, a.pas + 1):
        bloc = train_s[step % len(train_s)]
        h = etats(bloc)                     # 4 × D, avec grad (LoRA)
        cibles = h.detach()
        perte = 0.0
        # transitions 1 pas (h_j -> h_{j+1})
        for j in range(3):
            perte = perte + (1 - (norm(modele_pas(h[j:j+1])) * norm(cibles[j+1:j+2])).sum()).mean()
        # multi-pas depuis la phrase 0
        z = h[0:1]
        for k in (1, 2, 3):
            z = modele_pas(z)
            perte = perte + (1 - (norm(z) * norm(cibles[k:k+1])).sum()).mean()
        opt.zero_grad(); perte.backward()
        torch.nn.utils.clip_grad_norm_(list(model.parameters()) + list(modele_pas.parameters()), 1.0)
        opt.step()
        if step % 50 == 0:
            print(f"  pas {step:4d} · perte {perte.item():.4f}", flush=True)
    model.eval(); modele_pas.eval()
    with torch.no_grad():
        rets = []
        for k in (1, 2, 3):
            justes = 0
            for bloc in test_s:
                h = etats(bloc)
                z = h[0:1]
                for _ in range(k):
                    z = modele_pas(z)
                sims = (norm(z) @ norm(h).T)[0]
                justes += int(torch.argmax(sims) == min(k, 3))
            rets.append(justes / len(test_s))
        print(f"  retrieval des pas 1/2/3 : {[round(x, 3) for x in rets]} (hasard 0,25)")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({"hf": a.hf, "couche": a.couche, "pas": a.pas,
                                                  "retrieval": [round(float(x), 4) for x in rets],
                                                  "n_train": len(train_s), "n_test": len(test_s)},
                                                 ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
