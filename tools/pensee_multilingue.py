#!/usr/bin/env python3
"""pensee_multilingue.py — ÉTAGE 2, PREMIÈRE MESURE : la représentation est-elle la même dans toutes les langues ?

POURQUOI ✓✓. L'étage 1 est à **19/20** langues (mesures 73-76) : on peut ouvrir l'**étage 2** (pensée abstraite).
La première question n'est pas métaphysique : *le modèle porte-t-il un **espace de sens partagé** entre les
langues ?* ✓✓ Si les états internes de la **même phrase** dans deux langues sont proches — et si un **pont
linéaire** suffit à passer de l'un à l'autre — alors il existe une **représentation neutre** sur laquelle bâtir la
pensée ✓✓ ; sinon, il faudra l'apprendre (le pont de la nuit du 16, cosinus 0,70) ✓✗.

LE DISPOSITIF ✓✓. Le corpus **JW 2026** (mesure 76) : 139 paragraphes, **les mêmes** dans 12 langues, alignés par
`data-pid` ✓✓. On fait lire chaque paragraphe au modèle **Qwen2.5-3B** et on garde l'état du **dernier token** à
plusieurs couches ✓.

DEUX MESURES, UN CONTRÔLE ✓✓ :
  1. **retrieval** : pour un paragraphe hindi, l'état anglais le plus proche (parmi 139) est-il **sa traduction** ?
     hasard = 1/139 = 0,7 % ✓✓ ;
  2. **pont linéaire** (ridge) : apprendre X → anglais sur 100 paragraphes, tester sur 39 ; mesure le **cosinus**
     et le **retrieval après pont** ✓✓ — *si un simple linéaire aligne les espaces, la représentation est
     linéairement partagée* ✓✓ ;
  3. **contrôle négatif** : apprendre le pont sur des paires **mélangées** (mauvaises traductions) ; le retrieval
     doit tomber au hasard ✓✓. *Sans ce contrôle, un pont peut « réussir » en apprenant la moyenne* ✗✗.

CE QUE L'OUTIL NE FAIT PAS ✗ : il ne teste pas la **pensée** (raisonnement, composition) ; il teste la **neutralité
de la représentation**, qui en est la condition ✓✓.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np


def extraire(model, tok, textes, couches, batch=8, max_len=512):
    """États du dernier token, par couche : {couche: (n, D)} ✓."""
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


def normalise(x):
    return x / np.maximum(1e-9, np.linalg.norm(x, axis=1, keepdims=True))


def retrieval(A, B):
    """Pour chaque ligne de A, la ligne de B la plus proche est-elle la bonne ? (même index) ✓."""
    S = normalise(A) @ normalise(B).T
    return float(np.mean(np.argmax(S, 1) == np.arange(len(A))))


def apprend_pont(X, Y, lam=1.0):
    """Ridge X → Y ✓ (biais inclus) : renvoie W, pas la prédiction."""
    Xb = np.hstack([X, np.ones((len(X), 1), np.float32)])
    return np.linalg.solve(Xb.T @ Xb + lam * np.eye(Xb.shape[1], dtype=np.float32), Xb.T @ Y)


def applique(X, W):
    return np.hstack([X, np.ones((len(X), 1), np.float32)]) @ W


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--dtype", default="float16")
    ap.add_argument("--sortie", default="reports/pensee-multilingue.json")
    ap.add_argument("--etats", default="reports/pensee-multilingue-etats.npz")
    ap.add_argument("--max", type=int, default=139)
    ap.add_argument("--repartir", action="store_true", help="répartir le modèle sur les deux cartes (7 B)")
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    data = json.loads(pathlib.Path("data/jw/jw_2026.json").read_text())
    unites = data["unites"][: a.max]
    langues = data["langues"]
    texte = {lg: [u["textes"][lg] for u in unites] for lg in langues}
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    if a.repartir:
        model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=getattr(torch, a.dtype),
                                                     device_map="auto").eval()
    else:
        model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=getattr(torch, a.dtype)).to("cuda").eval()
    dev = next(model.parameters()).device
    n_layers = model.config.num_hidden_layers
    couches = sorted(set([0, n_layers // 6, n_layers // 3, n_layers // 2, 2 * n_layers // 3,
                          5 * n_layers // 6, n_layers]))
    etats = {}
    for lg in langues:
        etats[lg] = extraire(model, tok, texte[lg], couches)
        print(f"  états {lg} : {etats[lg][couches[0]].shape}")
    np.savez_compressed(a.etats, **{f"{lg}_{L}": etats[lg][L] for lg in langues for L in couches},
                        couches=np.array(couches), langues=np.array(langues))

    rng = np.random.default_rng(1234)
    n = len(unites); idx = rng.permutation(n); train, test = idx[:100], idx[100:]
    res = []
    for lg in langues:
        if lg == "eng":
            continue
        for L in couches:
            X, Y = etats[lg][L], etats["eng"][L]
            # retrieval brut, sans pont ✓
            brut = retrieval(X[test], Y[test])
            # pont appris sur les bonnes paires, testé sur les autres ✓
            # λ choisi par validation croisée interne (le pont a 2049 paramètres pour 100 exemples : sans
            # validation, il sur-apprend) ✓✓
            tr, va = train[:70], train[70:]
            meilleur = max((0.1, 1.0, 10.0, 100.0, 1000.0),
                           key=lambda lam: retrieval(applique(X[va], apprend_pont(X[tr], Y[tr], lam)), Y[va]))
            W = apprend_pont(X[train], Y[train], meilleur)
            Yp = applique(X[test], W)
            cos = float(np.mean(np.sum(normalise(Yp) * normalise(Y[test]), 1)))
            pont_test = retrieval(Yp, Y[test])
            # contrôle négatif : pont appris sur des paires MÉLANGÉES ✓✓
            mel = rng.permutation(len(train))
            Wn = apprend_pont(X[train], Y[train][mel])
            neg = retrieval(applique(X[test], Wn), Y[test])
            res.append({"langue": lg, "couche": int(L), "lambda": meilleur,
                        "retrieval_brut": round(brut, 4),
                        "cosinus_pont": round(cos, 4), "retrieval_pont": round(pont_test, 4),
                        "retrieval_negatif": round(neg, 4)})
        print(f"  {lg} : meilleur retrieval pont "
              f"{max(r['retrieval_pont'] for r in res if r['langue'] == lg):.3f}")
    sortie = pathlib.Path(a.sortie); sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps({"n": n, "couches": [int(c) for c in couches], "langues": langues,
                                  "resultats": res}, ensure_ascii=False, indent=1))
    print(f"  → {sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
