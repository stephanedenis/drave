#!/usr/bin/env python3
"""seuil_bruit.py — DU MARQUEUR AU SEUIL : détecter le bruit d'entrée, puis le CORRIGER, et le mesurer.

POURQUOI ✓✓. La mesure 60 a montré que les marqueurs de bruit **voient** l'entrée abîmée (fautes ×3-5 de
surprisal, langue mêlée ×1,5-3, accents ×1,3-1,5) ✓✓, mais elle s'arrêtait là : *un marqueur qui voit ne sert à rien
s'il ne **décide** rien* ✗✓. Ici, on en fait un **seuil** ✓✓ : à partir de quelle valeur de surprisal l'interface
doit-elle **rejeter** ou **corriger** l'entrée ? Et la correction **marche-t-elle** ? ✓✓

LE DISPOSITIF ✓✓. Sur des articles propres (UDHR français ✓), on fabrique des versions abîmées à taux **contrôlé** :
  · **fautes** : p % des caractères remplacés (p = 2, 5, 10, 20) ✓ ;
  · **accents perdus** (le bruit réel le plus courant : copier-coller, OCR, claviers) ✓ ;
  · **langue mêlée** : p % des mots remplacés par les mots anglais de l'article aligné (p = 10, 30, 50) ✓✓ ;
  · **mots supprimés** : 10 % des mots retirés ✓.
Pour chaque version, on calcule la **surprisal par token** (le marqueur) ✓, puis :
  1. **le seuil** : on prend le 95ᵉ centile des textes **propres** (le taux de fausses alertes est donc fixé à 5 % ✓),
     et on mesure le **taux de détection** de chaque corruption ✓✓ — plus l'**AUC** (séparation propre/abîmé,
     indépendante du seuil) ✓ ;
  2. **la correction** : on demande au modèle de **corriger** le texte abîmé (sans le traduire) ✓, et on mesure le
     **taux d'erreur caractère** (CER, distance de Levenshtein / longueur) **avant** et **après** ✓✓.

CE QUE CE BANC NE DIT PAS ✗ : il ne prouve pas que la correction **préserve le sens** (le CER, lui, est aveugle au
sens ✓✗) ; et un texte court a une surprisal plus variable ✓ (mesure 58, 22ᵉ piège) ✓.
"""
from __future__ import annotations
import argparse, json, math, pathlib, random, unicodedata
import numpy as np


def levenshtein(a: str, b: str) -> int:
    """Distance d'édition en caractères ✓ (O(len(a)·len(b)), les textes font < 2000 caractères)."""
    if len(a) < len(b):
        a, b = b, a
    prec = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prec[j] + 1, cur[j - 1] + 1, prec[j - 1] + (ca != cb)))
        prec = cur
    return prec[-1]


def cer(hyp: str, ref: str) -> float:
    return 100 * levenshtein(hyp, ref) / max(1, len(ref))


def auc(propres, abimes) -> float:
    """AUC par Mann-Whitney : P(un abîmé score plus haut qu'un propre) ✓✓."""
    if not propres or not abimes:
        return 0.5
    g = 0
    for a in abimes:
        for b in propres:
            g += (a > b) + 0.5 * (a == b)
    return g / (len(propres) * len(abimes))


def abime(texte: str, version: str, en: str | None, rng: random.Random, pool_en=None) -> str:
    if version == "propre" or version.startswith("accents"):
        return texte
    if version.startswith("fautes"):
        p = int(version.split()[1].rstrip("%")) / 100
        out = []
        for ch in texte:
            if ch.isalpha() and rng.random() < p:
                out.append(rng.choice("abcdefghijklmnopqrstuvwxyzéèêàç"))
            else:
                out.append(ch)
        return "".join(out)
    if version.startswith("melange"):
        p = int(version.split()[1].rstrip("%")) / 100
        mots_fr = texte.split()
        # ⚠️ BUG CORRIGÉ (mesure 65) : l'ancienne version exigeait que l'article anglais ait AUTANT de mots que le
        # français ; comme l'anglais est plus court, elle ne remplaçait RIEN et les trois taux donnaient le même
        # chiffre ✗✗. On puise dans le vocabulaire anglais de TOUT le corpus ✓✓.
        mots_en = pool_en if pool_en else (en or "").split()
        if not mots_en:
            return texte
        n_remplaces = int(p * len(mots_fr))
        positions = rng.sample(range(len(mots_fr)), n_remplaces)
        for k in positions:
            mots_fr[k] = rng.choice(mots_en)
        return " ".join(mots_fr)
    if version.startswith("suppression"):
        p = int(version.split()[1].rstrip("%")) / 100
        mots = [m for m in texte.split() if rng.random() >= p]
        return " ".join(mots)
    return texte


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", required=True)
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--dtype", default="float16", choices=["float32", "bfloat16", "float16"])
    ap.add_argument("--mode", choices=["marqueurs", "correction", "tout"], default="tout")
    ap.add_argument("--sortie", default="reports/seuil-bruit.json")
    ap.add_argument("--graine", type=int, default=0)
    a = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    m = AutoModelForCausalLM.from_pretrained(a.hf, dtype=getattr(torch, a.dtype)).to("cuda").eval()
    tok = AutoTokenizer.from_pretrained(a.hf)
    fr, en = {}, {}
    for l in pathlib.Path("data/udhr/articles_propres.jsonl").read_text().splitlines():
        x = json.loads(l)
        if x["iso3"] == "fra": fr[int(x["art"])] = x["texte"]
        if x["iso3"] == "eng": en[int(x["art"])] = x["texte"]
    versions = ["propre", "fautes 2%", "fautes 5%", "fautes 10%", "fautes 20%", "accents perdus",
                "melange 10%", "melange 30%", "melange 50%", "suppression 10%"]

    def surprisal(t: str) -> float:
        ids = tok(t, return_tensors="pt").to(m.device)
        with torch.no_grad():
            lp = torch.log_softmax(m(**ids).logits[0], dim=-1)
        c = ids["input_ids"][0][1:]
        sur = (-lp[:-1].gather(1, c.unsqueeze(1)).squeeze(1) / math.log(2)).cpu().numpy()
        return float(sur.mean())

    def corrige(t: str) -> str:
        msg = ("Corrige les fautes de frappe et restaure les accents du texte suivant. Réponds avec le texte "
               "corrigé seulement, sans commentaire ni traduction.\n\n" + t)
        p = tok.apply_chat_template([{"role": "user", "content": msg}], tokenize=False,
                                    add_generation_prompt=True)
        ids = tok(p, return_tensors="pt").to(m.device)
        with torch.no_grad():
            g = m.generate(**ids, max_new_tokens=max(120, int(len(t) / 2)), do_sample=False,
                           pad_token_id=tok.eos_token_id)
        return tok.decode(g[0][ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()

    rng = random.Random(a.graine)
    pool_en = " ".join(en.values()).split()
    donnees = []
    for art in sorted(fr)[: a.n]:
        propre = fr[art]
        for v in versions:
            texte = abime(propre, v, en.get(art), rng, pool_en)
            if v == "accents perdus":
                texte = "".join(ch for ch in unicodedata.normalize("NFD", propre)
                                if unicodedata.category(ch) != "Mn")
            d = {"article": art, "version": v, "texte": texte,
                 "cer_avant": round(cer(texte, propre), 2)}
            d["surprisal"] = round(surprisal(texte), 3)
            if a.mode in ("correction", "tout") and v != "propre":
                sortie = corrige(texte)
                d["correction"] = sortie
                d["cer_apres"] = round(cer(sortie, propre), 2)
                d["surprisal_apres"] = round(surprisal(sortie), 3)
            donnees.append(d)
            print(f"  art.{art:2d} {v:16s} · surprisal {d['surprisal']:.2f} · CER avant {d['cer_avant']:.1f} %"
                  + (f" · CER après {d['cer_apres']:.1f} %" if "cer_apres" in d else ""))
    # le seuil : 95ᵉ centile des textes propres ✓ (fausses alertes fixées à 5 %)
    propres = [d["surprisal"] for d in donnees if d["version"] == "propre"]
    seuil = float(np.percentile(propres, 95))
    print(f"\n  SEUIL (95ᵉ centile des propres) = {seuil:.2f} bits/token")
    synthese = []
    for v in versions[1:]:
        abimes = [d["surprisal"] for d in donnees if d["version"] == v]
        det = float(np.mean([s > seuil for s in abimes]))
        ligne = {"version": v, "detection": round(det, 3), "auc": round(auc(propres, abimes), 3),
                 "surprisal_moyenne": round(float(np.mean(abimes)), 3)}
        if a.mode in ("correction", "tout"):
            ligne["cer_avant"] = round(float(np.mean([d["cer_avant"] for d in donnees if d["version"] == v])), 2)
            ligne["cer_apres"] = round(float(np.mean([d["cer_apres"] for d in donnees if d["version"] == v
                                                      and "cer_apres" in d])), 2)
            ligne["surprisal_apres"] = round(float(np.mean([d["surprisal_apres"] for d in donnees
                                                           if d["version"] == v and "surprisal_apres" in d])), 3)
        synthese.append(ligne)
        print(f"  {v:16s} · détection {det:4.0%} · AUC {ligne['auc']:.2f}"
              + (f" · CER {ligne['cer_avant']:.1f} → {ligne['cer_apres']:.1f} %" if "cer_apres" in ligne else ""))
    pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(a.sortie).write_text(json.dumps(
        {"hf": a.hf, "seuil": seuil, "synthese": synthese, "details": donnees}, ensure_ascii=False, indent=1))
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
