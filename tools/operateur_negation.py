#!/usr/bin/env python3
"""operateur_negation.py — B4.1 : la négation est-elle une OPÉRATION portée par l'état ?

L'étage 2 est jugé sur des **opérations**. La première : la **négation**. On prend les paires DACCORD
(prémisse, hypothèse, étiquette binaire 0/1), on **nie l'hypothèse** (« Il est faux que : H ») — l'étiquette
doit **basculer** (1 − étiquette) — et on demande à la sonde, **entraînée sur les paires originales**, de lire
les états des paires **niées** :

  - si la sonde lit l'étiquette **basculée** bien au-dessus du hasard → la négation est une opération
    **portée par l'état** (l'opérateur existe) ;
  - si elle lit l'étiquette **originale** → elle ignore l'opération : elle lit la forme, pas le sens.

Contrôles : les étiquettes **mélangées** (le hasard), et le taux sur l'étiquette **non basculée**.

Usage : operateur_negation.py --tsv data/daccord/daccord.tsv --hf Qwen/Qwen2.5-1.5B-Instruct --couche 22 \
            --sortie reports/operateur-negation-1.5b-l22.json
"""
import argparse
import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, "tools")
from nli_fr_dur import mlp_sonde, sonde  # le même socle que les mesures NLI


def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", default="data/daccord/daccord.tsv")
    ap.add_argument("--hf", default="Qwen/Qwen2.5-1.5B-Instruct")
    ap.add_argument("--couche", type=int, default=22)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--sortie", default="reports/operateur-negation.json")
    ap.add_argument("--lora", action="store_true",
                    help="B4 suite : apprendre la négation DANS les poids (LoRA rang 8) avant les tests")
    ap.add_argument("--sans-entrainement", action="store_true",
                    help="diagnostic : poser le LoRA SANS l'entraîner (la référence doit rester à ~0,81)")
    a = ap.parse_args()
    lignes = pathlib.Path(a.tsv).read_text(encoding="utf-8").splitlines()
    entete = lignes[0].split("\t")
    idx = {c: i for i, c in enumerate(entete)}
    paires = []
    for l in lignes[1:]:
        cols = l.split("\t")
        if len(cols) <= max(idx["premise"], idx["hypothesis"], idx["label"]):
            continue
        try:
            y = int(cols[idx["label"]])
        except ValueError:
            continue
        if y in (0, 1):
            paires.append((cols[idx["premise"]], cols[idx["hypothesis"]], y))
    print(f"  {len(paires)} paires · 2 classes · hasard 0.5")

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float16).to("cuda").eval()
    consigne = "Ces deux phrases se contredisent-elles (oui ou non) ?"

    def etats(items):
        textes = [tok.apply_chat_template(
            [{"role": "user", "content":
              f"Prémisse : {s1}\nHypothèse : {s2}\n{consigne}"}],
            tokenize=False, add_generation_prompt=True) for s1, s2, _ in items]
        out = []
        for i in range(0, len(textes), a.batch):
            enc = tok(textes[i:i + a.batch], return_tensors="pt", padding=True,
                      truncation=True, max_length=256).to("cuda")
            with torch.no_grad():
                hs = model(**enc, output_hidden_states=True).hidden_states
            j = enc["attention_mask"].sum(1) - 1
            out.append(hs[a.couche][torch.arange(len(j)), j].float().cpu().numpy())
        return np.concatenate(out, 0)

    rng = np.random.default_rng(1234)
    ordre = rng.permutation(len(paires))
    n_tr = int(0.7 * len(paires))
    tr = [paires[i] for i in ordre[:n_tr]]
    te = [paires[i] for i in ordre[n_tr:]]
    # Les paires niées : même prémisse, hypothèse niée, étiquette basculée.
    te_neg = [(s1, f"Il est faux que : {s2}", 1 - y) for s1, s2, y in te]
    tr_neg = [(s1, f"Il est faux que : {s2}", 1 - y) for s1, s2, y in tr]
    # B4 (suite) — le LoRA : apprendre l'opération DANS les poids, puis refaire les cinq
    # tests. Le modèle est gelé sauf le LoRA ; l'entraînement porte sur les paires NIÉES.
    if a.lora:
        import sys
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        from adaptateur_langue import poser_lora
        poser_lora(model, rang=8)   # modifie le modèle EN PLACE ; il rend la liste des conteneurs
        if a.sans_entrainement:
            print("  [lora] posé SANS entraînement — la référence doit rester à ~0,81")
        else:
            model.train()
            params = [p for p in model.parameters() if p.requires_grad]
            opt = torch.optim.AdamW(params, lr=1e-5)   # 1e-4 faisait diverger (référence tombée à 0,48)
            oui = tok(" oui", add_special_tokens=False).input_ids[0]
            non = tok(" non", add_special_tokens=False).input_ids[0]
            perdre = torch.nn.CrossEntropyLoss()
            for _ in range(1):
                for s1, s2, y in tr_neg:
                    txt = tok.apply_chat_template(
                        [{"role": "user", "content": f"Prémisse : {s1}\nHypothèse : {s2}\n{consigne}"}],
                        tokenize=False, add_generation_prompt=True)
                    enc = tok(txt, return_tensors="pt", truncation=True, max_length=256).to("cuda")
                    logits = model(**enc).logits[0, -1][[oui, non]]
                    cible = torch.tensor([0 if y == 1 else 1], device="cuda")
                    perte = perdre(logits.unsqueeze(0), cible)
                    opt.zero_grad(); perte.backward()
                    torch.nn.utils.clip_grad_norm_(params, 1.0)
                    opt.step()
            model.eval()
            print(f"  [lora] {len(tr_neg)} paires niées, rang 8, 1 époque, lr 1e-5 — perte finale {perte.item():.4f}")
    Etr = etats(tr)
    Ete = etats(te)
    Ete_neg = etats(te_neg)
    Etr_neg = etats(tr_neg)
    te_double = [(s1, f"Il est faux que : il est faux que : {s2}", y) for s1, s2, y in te]
    Ete_double = etats(te_double)
    tr_double = [(s1, f"Il est faux que : il est faux que : {s2}", y) for s1, s2, y in tr]
    Etr_double = etats(tr_double)
    ytr = np.array([p[2] for p in tr])
    yte = np.array([p[2] for p in te])

    pred_orig = sonde(Etr, ytr, Ete, 2)               # la référence : les paires originales
    pred_flip = sonde(Etr, ytr, Ete_neg, 2)            # entraînée sur l'original, lit le nié
    pred_flip_m = mlp_sonde(Etr, ytr, Ete_neg, 2)
    rng2 = np.random.default_rng(7)
    E_mix = np.vstack([Etr, Etr_neg])
    y_mix = np.concatenate([ytr, 1 - ytr])
    pred_ctrl = sonde(Etr, rng2.permutation(ytr), Ete_neg, 2)
    res = {
        "jeu": "daccord", "modele": a.hf, "couche": a.couche,
        "n_train": len(tr), "n_test": len(te), "hasard": 0.5,
        "reference_orig": round(float(np.mean(pred_orig == yte)), 4),
        "flip_sonde": round(float(np.mean(pred_flip == 1 - yte)), 4),
        "garde_sonde": round(float(np.mean(pred_flip == yte)), 4),
        "flip_mlp": round(float(np.mean(pred_flip_m == 1 - yte)), 4),
        "garde_mlp": round(float(np.mean(pred_flip_m == yte)), 4),
        "negatif_flip": round(float(np.mean(pred_ctrl == 1 - yte)), 4),
        # B4.2 — la négation APPRISE : une sonde entraînée sur les paires niées (étiquette basculée)
        "appris_negatif": round(float(np.mean(sonde(Etr_neg, np.array([p[2] for p in tr_neg]), Ete_neg, 2) == 1 - yte)), 4),
        "appris_original": round(float(np.mean(sonde(Etr_neg, np.array([p[2] for p in tr_neg]), Ete, 2) == yte)), 4),
        "negatif_appris": round(float(np.mean(sonde(Etr_neg, rng2.permutation(np.array([p[2] for p in tr_neg])), Ete_neg, 2) == 1 - yte)), 4),
        # B4.3 — les DEUX opérations dans UN seul opérateur : on entraîne sur le mélange (l'original + le nié)
        "mixte_negatif": round(float(np.mean(sonde(E_mix, y_mix, Ete_neg, 2) == 1 - yte)), 4),
        "mixte_original": round(float(np.mean(sonde(E_mix, y_mix, Ete, 2) == yte)), 4),
        "mixte_controle": round(float(np.mean(sonde(E_mix, rng2.permutation(y_mix), Ete_neg, 2) == 1 - yte)), 4),
        # B4.4 — la COMPOSITION : le nié du nié doit revenir à l'original (la cible est yte)
        "double_original": round(float(np.mean(sonde(Etr, ytr, Ete_double, 2) == yte)), 4),
        "double_mixte": round(float(np.mean(sonde(E_mix, y_mix, Ete_double, 2) == yte)), 4),
        "double_negatif": round(float(np.mean(sonde(Etr_neg, np.array([p[2] for p in tr_neg]), Ete_double, 2) == yte)), 4),
        "double_controle": round(float(np.mean(sonde(E_mix, rng2.permutation(y_mix), Ete_double, 2) == yte)), 4),
        # B4.5 — la composition APPRISE : le triple (original, nié, double nié) avec les cibles (y, 1−y, y)
        "appris_double": round(float(np.mean(sonde(np.vstack([Etr, Etr_neg, Etr_double]),
                                                    np.concatenate([ytr, 1 - ytr, ytr]), Ete_double, 2) == yte)), 4),
        "appris_double_controle": round(float(np.mean(sonde(np.vstack([Etr, Etr_neg, Etr_double]),
                                                             rng2.permutation(np.concatenate([ytr, 1 - ytr, ytr])), Ete_double, 2) == yte)), 4),
    }
    for k, v in res.items():
        print(f"  {k}: {v}")
    if res["flip_sonde"] > 0.55:
        print("  → la négation est une OPÉRATION portée par l'état (le flip passe le hasard)")
    else:
        print("  → la négation n'est PAS portée par l'état (le flip reste au hasard)")
    pathlib.Path(a.sortie).write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n",
                                      encoding="utf-8")
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    sys.exit(principal())
