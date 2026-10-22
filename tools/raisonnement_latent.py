#!/usr/bin/env python3
"""raisonnement_latent.py — ÉTAGE 2 : le raisonnement transitif est-il DANS L'ÉTAT, et indépendant de la langue ?

POURQUOI ✓✓. La « tête bien faite » ne se mesure pas à la taille mais à la **composition** d'opérations. Le corpus
`corpus_raisonnement.py` donne des chaînes d'ordre (A devant B, B devant C…) et demande qui est devant tout le monde ;
les prémisses sont **mélangées**, donc il faut composer, pas recopier la liste. La question : l'**état caché** à la fin
de l'invite porte-t-il la réponse — et le même état la porte-t-il en français et en anglais ? ✓✓

CE QU'ON MESURE ✓✓ : une **sonde linéaire** (ridge, 20 noms) entraînée sur une partie des chaînes et testée sur les
autres ; par **longueur** (2 à 6 entités), par **langue**, en **transfert croisé** FR→EN et EN→FR, et sur les
**contrôles** (chaînes incohérentes, paires sans relation) ✓✓. Hasard = 1/20 = **5 %** ✓✓.

CE QUE CHAQUE ISSUE VEUT DIRE ✓✓ :
  · accuracy qui **décroît avec la longueur** mais reste au-dessus du hasard → l'état compose, avec une limite ✓✓ ;
  · **transfert FR→EN** au niveau du FR → la représentation du raisonnement est **indépendante de la langue** ✓✓ ;
  · accuracy au hasard partout → la réponse n'est pas dans l'état (elle n'existe qu'à la génération) ✗✗.
"""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np


def norm(x):
    return x / np.maximum(1e-9, np.linalg.norm(x, axis=1, keepdims=True))


def sonde(Xtr, ytr, Xte, yte, classes, lam=10.0):
    moy = Xtr.mean(0, keepdims=True); ect = Xtr.std(0, keepdims=True) + 1e-6
    Xtr = (Xtr - moy) / ect; Xte = (Xte - moy) / ect
    Y = np.eye(classes, dtype=np.float32)[ytr]
    Xb = np.hstack([Xtr, np.ones((len(Xtr), 1), np.float32)])
    W = np.linalg.solve(Xb.T @ Xb + lam * np.eye(Xb.shape[1], dtype=np.float32), Xb.T @ Y)
    pred = np.argmax(np.hstack([Xte, np.ones((len(Xte), 1), np.float32)]) @ W, 1)
    return float(np.mean(pred == yte))


def principal() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="data/raisonnement/transitif.json")
    ap.add_argument("--hf", default="Qwen/Qwen2.5-3B-Instruct")
    ap.add_argument("--couche", type=int, default=18)
    ap.add_argument("--sortie", default="reports/raisonnement-latent.json")
    ap.add_argument("--batch", type=int, default=16)
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    d = json.loads(pathlib.Path(a.corpus).read_text())
    noms = d["noms"]; index = {n: i for i, n in enumerate(noms)}
    ex = [e for e in d["exemples"] if e["reponse"] in index]
    tok = AutoTokenizer.from_pretrained(a.hf)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(a.hf, dtype=torch.float16).to("cuda").eval()

    def contenu(e):
        base = e["texte"].split("Réponse :")[0].split("Answer:")[0].strip()
        consigne = "Réponds par un seul nom." if e["langue"] == "fr" else "Answer with a single name."
        return base + "\n" + consigne

    textes = [tok.apply_chat_template([{"role": "user", "content": contenu(e)}], tokenize=False,
                                      add_generation_prompt=True) for e in ex]
    etats = []
    for i in range(0, len(textes), a.batch):
        enc = tok(textes[i:i + a.batch], return_tensors="pt", padding=True, truncation=True,
                  max_length=512).to("cuda")
        with torch.no_grad():
            hs = model(**enc, output_hidden_states=True).hidden_states
        idx = enc["attention_mask"].sum(1) - 1
        etats.append(hs[a.couche][torch.arange(len(idx)), idx].float().cpu().numpy())
    E = np.concatenate(etats, 0)
    y = np.array([index[e["reponse"]] for e in ex])
    langue = np.array([e["langue"] for e in ex])
    longueur = np.array([e["longueur"] for e in ex])
    condition = np.array([e["condition"] for e in ex])
    split = np.array([e["split"] for e in ex])
    res = {"couche": a.couche, "n_exemples": len(ex), "hasard": 1.0 / len(noms), "par_groupe": [], "transfert": []}
    for lang in ("fr", "en"):
        for L in (2, 3, 4, 5, 6):
            for cond in ("coherent",):
                m_tr = (langue == lang) & (longueur == L) & (condition == cond) & (split == "train")
                m_te = (langue == lang) & (longueur == L) & (condition == cond) & (split == "test")
                if m_tr.sum() < 20 or m_te.sum() < 10:
                    continue
                acc = sonde(E[m_tr], y[m_tr], E[m_te], y[m_te], len(noms))
                neg = sonde(E[m_tr], np.random.default_rng(7).permutation(y[m_tr]), E[m_te], y[m_te], len(noms))
                res["par_groupe"].append({"langue": lang, "longueur": L, "condition": cond,
                                          "n_train": int(m_tr.sum()), "n_test": int(m_te.sum()),
                                          "accuracy": round(acc, 4), "negatif": round(neg, 4)})
                print(f"  {lang} L{L} · accuracy {acc:.3f} · négatif {neg:.3f} (hasard {1/len(noms):.2f})")
    # contrôles : la sonde apprend sur le cohérent, on la teste sur cycle / sans relation (réponse arbitraire)
    for cond in ("cycle", "sans_relation"):
        for lang in ("fr", "en"):
            m_tr = (langue == lang) & (longueur == 3) & (condition == "coherent") & (split == "train")
            m_te = (langue == lang) & (longueur == 3) & (condition == cond) & (split == "test")
            if m_te.sum() < 10:
                continue
            acc = sonde(E[m_tr], y[m_tr], E[m_te], y[m_te], len(noms))
            res.setdefault("controles", []).append({"langue": lang, "condition": cond, "accuracy": round(acc, 4)})
            print(f"  contrôle {lang} {cond} · accuracy {acc:.3f}")
    # transfert croisé FR→EN et EN→FR, par longueur
    for src, dst in (("fr", "en"), ("en", "fr")):
        for L in (2, 3, 4, 5, 6):
            m_tr = (langue == src) & (longueur == L) & (condition == "coherent") & (split == "train")
            m_te = (langue == dst) & (longueur == L) & (condition == "coherent") & (split == "test")
            if m_tr.sum() < 20 or m_te.sum() < 10:
                continue
            acc = sonde(E[m_tr], y[m_tr], E[m_te], y[m_te], len(noms))
            res["transfert"].append({"de": src, "vers": dst, "longueur": L, "accuracy": round(acc, 4)})
            print(f"  transfert {src}→{dst} L{L} · accuracy {acc:.3f}")
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
