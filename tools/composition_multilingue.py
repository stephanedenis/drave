#!/usr/bin/env python3
"""composition_multilingue.py — ÉTAGE 2 : le sens partagé est-il COMPOSITIONNEL, ou un sac de mots ?

POURQUOI ✓✓. Les mesures 77-78 ont montré qu'un pont linéaire retrouve la bonne **traduction d'un paragraphe**
dans 28-69 % des cas ✓✓. Mais un état de **dernier token** peut n'être qu'un **résumé** du paragraphe (sac de
mots) ✓✗ : si c'était le cas, l'alignement ne dirait rien de la **composition** du sens — or c'est elle que la RSN
multi-niveaux doit représenter ✓✓.

LE TEST ✓✓. On coupe chaque paragraphe en **préfixes proportionnels** (25 %, 50 %, 75 %, 100 % des **caractères**,
pas des phrases : les traductions ne découpent pas pareil) ✓✓. On fait lire chaque préfixe au modèle et on garde
l'état du dernier token ✓. Puis :
  · **retrieval par niveau** : pour un préfixe (p, q) en X, l'état anglais le plus proche parmi les 40 paragraphes
    est-il le **même** (p, q) ? hasard = 1/40 = 2,5 % ✓✓ ;
  · **contrôle croisé** : pour un préfixe (p, q), le plus proche parmi les **quatre niveaux** du même paragraphe
    est-il le **bon** q ? hasard = 25 % ✓✓ — *si la représentation est un sac, tous les niveaux se ressemblent* ✗✗ ;
  · **trajectoire** : le **changement** d'état entre deux niveaux (q2 − q1) est-il partagé entre X et l'anglais ?
    cosinus de la différence ✓✓ — *c'est la mesure de composition la plus stricte* ✓✓.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np


def norm(x):
    return x / np.maximum(1e-9, np.linalg.norm(x, axis=1, keepdims=True))


def retr(A, B):
    return float(np.mean(np.argmax(norm(A) @ norm(B).T, 1) == np.arange(len(A))))


def extraction(model, tok, textes, couches, batch=8, max_len=512):
    import torch
    dev = next(model.parameters()).device
    sorties = {L: [] for L in couches}
    for i in range(0, len(textes), batch):
        lot = textes[i:i + batch]
        enc = tok(lot, return_tensors="pt", padding=True, truncation=True, max_length=max_len).to(dev)
        with torch.no_grad():
            hs = model(**enc, output_hidden_states=True).hidden_states
        idx = enc["attention_mask"].sum(1) - 1
        for L in couches:
            sorties[L].append(hs[L][torch.arange(len(lot)), idx].float().cpu().numpy())
    return {L: np.concatenate(v, 0) for L, v in sorties.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--dtype", default="float16")
    ap.add_argument("--paragraphes", type=int, default=40)
    ap.add_argument("--sortie", default="reports/composition-multilingue.json")
    ap.add_argument("--etats", default="data/composition-etats.npz")
    ap.add_argument("--reutiliser", action="store_true", help="réutiliser les états déjà extraits")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    data = json.loads(pathlib.Path("data/jw/jw_2026.json").read_text())
    langues = [lg for lg in data["langues"] if lg != "eng"]
    # 40 paragraphes étalés, avec au moins 200 caractères dans chaque langue
    unites = [u for u in data["unites"]
              if min(len(u["textes"][lg]) for lg in data["langues"]) >= 200]
    pas = max(1, len(unites) // a.paragraphes)
    unites = unites[::pas][: a.paragraphes]
    niveaux = (0.25, 0.5, 0.75, 1.0)
    textes, meta = [], []
    for u in unites:
        for lg in ["eng"] + langues:
            t = u["textes"][lg]
            for q in niveaux:
                textes.append(t[: max(20, int(len(t) * q))])
                meta.append((u["id"], lg, q))
    if a.reutiliser and pathlib.Path(a.etats).exists():
        z = np.load(a.etats, allow_pickle=False)
        couches = [int(c) for c in z["couches"]]
        meta = []
        for s in z["noms"]:
            pid, lg, q = str(s).split("|")
            meta.append((pid, lg, float(q)))
        etats = {L: z[f"L{L}"] for L in couches}
        print(f"  états réutilisés : {len(meta)} préfixes, couches {couches}")
    else:
        tok = AutoTokenizer.from_pretrained(a.hf)
        if tok.pad_token is None:
            tok.pad_token = tok.eos_token
        model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=getattr(torch, a.dtype)).to("cuda").eval()
        n_layers = model.config.num_hidden_layers
        couches = sorted(set([0, n_layers // 6, n_layers // 3, n_layers // 2, 2 * n_layers // 3,
                              5 * n_layers // 6, n_layers]))
        etats = extraction(model, tok, textes, couches)
        np.savez_compressed(a.etats, **{f"L{L}": etats[L] for L in couches},
                            couches=np.array(couches), noms=np.array([f"{i}|{l}|{q}" for i, l, q in meta]))
    res = []
    for L in couches:
        E = etats[L]
        # index par (langue, niveau) et par paragraphe
        idx = {(lg, q): [] for lg in ["eng"] + langues for q in niveaux}
        for i, (pid, lg, q) in enumerate(meta):
            idx[(lg, q)].append(i)
        for lg in langues:
            # 1) retrieval par niveau : X(q) contre anglais(q), 40 paragraphes ✓
            r_niv = []
            for q in niveaux:
                A = E[idx[(lg, q)]]; B = E[idx[("eng", q)]]
                r_niv.append(retr(A, B))
            r_moy = float(np.mean(r_niv))
            # 2) contrôle croisé : le bon niveau parmi les quatre, même paragraphe ✓✓
            justes = 0; total = 0
            for i, (pid, l, q) in enumerate(meta):
                if l != lg:
                    continue
                # les quatre niveaux anglais du même paragraphe
                cands = [j for j, (p2, l2, q2) in enumerate(meta) if p2 == pid and l2 == "eng"]
                sims = [float((norm(E[i:i+1]) @ norm(E[j:j+1]).T).item()) for j in cands]
                if cands:
                    meilleur = cands[int(np.argmax(sims))]
                    justes += (meta[meilleur][2] == q); total += 1
            score_niv = justes / max(1, total)
            # 3) trajectoire : cosinus des différences 50-25 et 75-50, X contre anglais ✓✓
            cos_traj = []
            for q1, q2 in ((0.25, 0.5), (0.5, 0.75), (0.75, 1.0)):
                A = E[idx[(lg, q2)]] - E[idx[(lg, q1)]]
                B = E[idx[("eng", q2)]] - E[idx[("eng", q1)]]
                cos_traj.append(float(np.mean(np.sum(norm(A) * norm(B), 1))))
            res.append({"couche": int(L), "langue": lg, "retrieval_par_niveau": [round(x, 4) for x in r_niv],
                        "retrieval_moyen": round(r_moy, 4), "niveau_exact": round(score_niv, 4),
                        "cosinus_trajectoire": [round(x, 4) for x in cos_traj],
                        "cosinus_trajectoire_moyen": round(float(np.mean(cos_traj)), 4)})
        print(f"  couche {L:2d} : fait")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps({"n_paragraphes": len(unites), "niveaux": list(niveaux),
                                                  "resultats": res}, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
