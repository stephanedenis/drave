#!/usr/bin/env python3
"""plan_entrainement.py — ÉTAGE 2 : peut-on ENTRAÎNER le plan dans le modèle (et non le lire après coup) ?

POURQUOI ✓✓. Les mesures 113-118 ont montré que les états **figés** portent la phrase et la langue, pas le plan ✗✗ :
l'opérateur linéaire prédit la moyenne, le MLP mémorise, le contexte ne porte pas le contenu, un code de 32 dimensions
ne dépasse la moyenne que de +0,02, et la position n'est pas décodable quand la langue l'est à 1,00. La question de la
phase suivante : un **objectif de plan** entraîné dans le modèle peut-il faire mieux ? ✓✓

LE TEST ✓✓ : sur les séries Verne FR (8 phrases), on donne au modèle les **4 premières phrases** et on lui demande de
produire un **état de plan** (le dernier état caché de l'invite) qui retrouve l'état de la **5ᵉ phrase** parmi
**8 candidats non vus** d'autres séries (hasard 12,5 %) ✓✓. Le modèle est un 3 B + LoRA, entraîné par **InfoNCE**
(contrastif) ; on compare le retrieval **avant** et **après** ✓✓.

CE QUE CHAQUE ISSUE VEUT DIRE ✓✓ :
  · retrieval qui **monte** au-dessus du hasard → le plan s'entraîne ; il faut alors l'échelle et la dynamique ✓✓ ;
  · retrieval qui **reste au hasard** → même l'entraînement ne fait pas émerger le plan sur ce corpus : la question est
    celle de la **donnée** (séries trop courtes, dépendance faible) ✓✗.
"""
from __future__ import annotations
import argparse, json, pathlib, random
import numpy as np


def series_verne(par_serie: int, n_max: int):
    d = json.loads(pathlib.Path("data/alignement/verne_fr_en.json").read_text())
    paires = [p for p in d["paires"] if p.get("n_fr") == 1 and p.get("n_en") == 1]
    par_chap = {}
    for p in paires:
        par_chap.setdefault(p["chapitre"], []).append(p)
    series = []
    for ch in sorted(par_chap):
        ps = sorted(par_chap[ch], key=lambda p: p["i_fr"])
        for i in range(0, len(ps) - par_serie + 1, par_serie):
            bloc = ps[i:i + par_serie]
            if len(bloc) == par_serie:
                series.append([p["fr"] for p in bloc])
    pas = max(1, len(series) // n_max)
    return series[::pas][:n_max]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--par-serie", type=int, default=8)
    ap.add_argument("--series", type=int, default=315)
    ap.add_argument("--couche", type=int, default=18)
    ap.add_argument("--prompt", type=int, default=4, help="nombre de phrases données en invite")
    ap.add_argument("--pas", type=int, default=300)
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--accum", type=int, default=2, help="accumulation de gradient (batch effectif = batch × accum)")
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--horizons", default="1", help="pas de plan à prédire (ex. 1,2,3)")
    ap.add_argument("--graine", type=int, default=1234)
    ap.add_argument("--melange", action="store_true", help="contrôle : cibles mélangées dans le lot")
    ap.add_argument("--sortie", default="reports/plan-entrainement.json")
    a = ap.parse_args()
    horizons = [int(h) for h in a.horizons.split(",")]
    assert a.prompt + max(horizons) <= a.par_serie, (a.prompt, horizons)
    import torch
    from transformers import AutoModel, AutoTokenizer
    from peft import LoraConfig, get_peft_model

    series = series_verne(a.par_serie, a.series)
    rng = random.Random(a.graine)
    idx = list(range(len(series))); rng.shuffle(idx)
    n_tr = int(0.7 * len(idx))
    tr, te = idx[:n_tr], idx[n_tr:]
    print(f"  {len(series)} séries · {len(tr)} entraînement · {len(te)} test")

    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModel.from_pretrained(a.hf, dtype=torch.float16).to("cuda").eval()
    n_layers = model.config.num_hidden_layers
    # toutes les couches : l'état lu (couche a.couche) doit dépendre de paramètres entraînables
    config = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, bias="none", task_type="FEATURE_EXTRACTION",
                        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
    model = get_peft_model(model, config)
    model.gradient_checkpointing_enable()
    model.enable_input_require_grads()
    scaler = torch.amp.GradScaler("cuda")

    def etats(textes, max_len=256):
        """Dernier état caché de la couche a.couche, pour chaque texte."""
        enc = tok(textes, return_tensors="pt", padding=True, truncation=True, max_length=max_len).to("cuda")
        with torch.autocast("cuda", dtype=torch.float16):
            hs = model(**enc, output_hidden_states=True).hidden_states
        idxs = enc["attention_mask"].sum(1) - 1
        return hs[a.couche][torch.arange(len(textes)), idxs].float()

    def retrieval(ids):
        """8 candidats non vus (séries différentes, même position), hasard 12,5 %, par horizon."""
        justes = {h: 0 for h in horizons}; tot = 0
        for i in range(0, len(ids) - 7, 8):
            groupe = ids[i:i + 8]
            invites = [" ".join(series[k][:a.prompt]) for k in groupe]
            with torch.no_grad():
                z = torch.nn.functional.normalize(etats(invites, 256), dim=1)
                for h in horizons:
                    cibles = [series[k][a.prompt + h - 1] for k in groupe]
                    y = torch.nn.functional.normalize(etats(cibles, 128), dim=1)
                    justes[h] += int((torch.argmax(z @ y.T, 1) == torch.arange(8, device=z.device)).sum())
            tot += 8
        return {h: justes[h] / max(1, tot) for h in horizons}

    def cache_cibles(ids):
        """Cibles du modèle FIGÉ (avant entraînement), gardées pour le contrôle."""
        cache = []
        for i in range(0, len(ids) - 7, 8):
            groupe = ids[i:i + 8]
            with torch.no_grad():
                ys = {h: torch.nn.functional.normalize(etats([series[k][a.prompt + h - 1] for k in groupe], 128), dim=1)
                      for h in horizons}
            cache.append((groupe, ys))
        return cache

    def retrieval_avec(ids, cache):
        justes = {h: 0 for h in horizons}; tot = 0
        for groupe, ys in cache:
            invites = [" ".join(series[k][:a.prompt]) for k in groupe]
            with torch.no_grad():
                z = torch.nn.functional.normalize(etats(invites, 256), dim=1)
                for h in horizons:
                    justes[h] += int((torch.argmax(z @ ys[h].T, 1) == torch.arange(8, device=z.device)).sum())
            tot += 8
        return {h: justes[h] / max(1, tot) for h in horizons}

    cache_base = cache_cibles(te)
    avant = retrieval_avec(te, cache_base)
    print("  AVANT : " + " · ".join(f"h{h} {v:.3f}" for h, v in avant.items()))

    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=a.lr)
    ordre = list(tr); rng.shuffle(ordre)
    pos = 0
    opt.zero_grad()
    for pas in range(a.pas):
        if pos + a.batch > len(ordre):
            rng.shuffle(ordre); pos = 0
        groupe = ordre[pos:pos + a.batch]; pos += a.batch
        invites = [" ".join(series[k][:a.prompt]) for k in groupe]
        with torch.autocast("cuda", dtype=torch.float16):
            z = torch.nn.functional.normalize(etats(invites, 256), dim=1)
            pertes = []
            for h in horizons:
                cibles = [series[k][a.prompt + h - 1] for k in groupe]
                y = torch.nn.functional.normalize(etats(cibles, 128), dim=1)
                if a.melange:
                    y = y[torch.randperm(len(y), device=y.device)]
                logits = (z @ y.T) / 0.05
                pertes.append(torch.nn.functional.cross_entropy(logits, torch.arange(len(groupe), device=logits.device)))
            perte = torch.stack(pertes).mean()
        scaler.scale(perte / a.accum).backward()
        if (pas + 1) % a.accum == 0:
            scaler.step(opt); scaler.update(); opt.zero_grad()
        if pas % 50 == 0:
            print(f"    pas {pas:4d} · perte {float(perte.detach()):.3f}")
    apres = retrieval(te)
    apres_base = retrieval_avec(te, cache_base)
    print("  APRÈS : " + " · ".join(f"h{h} {v:.3f}" for h, v in apres.items()))
    print("  APRÈS (cibles du modèle figé) : " + " · ".join(f"h{h} {v:.3f}" for h, v in apres_base.items()))

    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({
        "hf": a.hf, "n_series": len(series), "n_train": len(tr), "n_test": len(te),
        "couche": a.couche, "prompt": a.prompt, "horizons": horizons, "pas": a.pas, "batch": a.batch, "accum": a.accum, "lr": a.lr,
        "graine": a.graine, "avant": {str(h): round(v, 4) for h, v in avant.items()}, "apres": {str(h): round(v, 4) for h, v in apres.items()}, "apres_base": {str(h): round(v, 4) for h, v in apres_base.items()}, "melange": a.melange, "hasard": 0.125}, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
