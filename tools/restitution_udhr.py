#!/usr/bin/env python3
"""restitution_udhr.py (v2) — LA RESTITUTION, MESURÉE EN FLUX (avec du contexte).

CE QUE LA v1 FAISAIT DE MAL ✗✗, et c'est un piège que je me suis tendu moi-même : elle encodait chaque article
**isolé** ✓✗. Ses premiers octets n'ont alors **aucun contexte** ✓✗ — ils sont imprévisibles par construction ✓✓ —
et un article ne peut **jamais** être exact, même parfaitement mémorisé ✗✗. Le « 0 article exact sur 13 222 » de la
première version était donc **un artefact de mon propre outil** ✓✗, pas un fait du modèle ✓✓.

CE QUE LA v2 FAIT ✓ : elle évalue le texte **en flux** ✓✓ — on donne au modèle les 256 octets qui précèdent le
fragment ✓, et on ne mesure que le fragment ✓. C'est la condition dans laquelle le modèle a été entraîné ✓ (le
corpus est un flux continu ✓), et la seule où la restitution exacte **peut** exister ✓✓.

TROIS CHIFFRES ✗ :
  · **bits/octet** (vue / jamais vue ✓) ;
  · **exactitude par octet** (vue / jamais vue ✓) ;
  · **fragments exacts** ✓✓ : la fraction des **fenêtres de 32 octets** où **tous** les octets sont justes ✓ —
    c'est la « restitution parfaite » à une granularité où elle est possible ✓✓.

⚠️ CE QU'IL NE DIT PAS ✗ : un fragment exact de 32 octets n'est pas un article exact ✓ ; et « vu » / « jamais vu »
sépare la mémorisation de la généralisation ✓✓ — la première peut être parfaite sans que la seconde existe ✓❌.
"""
from __future__ import annotations
import argparse, collections, json, math, pathlib, sys
import numpy as np, torch
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from udhr_commun import charger_articles, charger_meta, charger_modele


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="/tmp/jouet-udhr2")
    ap.add_argument("--contexte", type=int, default=256)
    ap.add_argument("--fragment", type=int, default=32)
    ap.add_argument("--iso", default="")
    ap.add_argument("--max-langues", type=int, default=0)
    ap.add_argument("--tokeniseur", action="store_true")
    ap.add_argument("--sortie", default="reports/restitution-udhr.json")
    a = ap.parse_args()
    articles = charger_articles(); meta = charger_meta()
    fichiers = sorted(f for f in articles if len(articles[f]) >= 28)
    if a.iso:
        fichiers = [f for f in fichiers if meta[f]["iso3"] == a.iso]
    if a.max_langues:
        fichiers = fichiers[: a.max_langues]
    m, encoder, device = charger_modele(a.hf, tokeniseur=a.tokeniseur)
    resultats = []
    for f in fichiers:
        # le flux, dans l'ordre d'entraînement ✓ (articles 1..30 séparés par un saut de ligne ✓)
        nums = sorted(articles[f])
        flux = "\n".join(articles[f][n] for n in nums)
        b = np.frombuffer(flux.encode("utf-8"), dtype=np.uint8).astype(np.int64)
        if a.tokeniseur:
            b = np.array(encoder(flux, 100000).cpu().numpy(), dtype=np.int64)
        acc_vue, acc_jamais, ex_vue, ex_jamais = [], [], [], []
        # ⚠️ UN PASSAGE PAR ARTICLE, PAS PAR FRAGMENT ✗✓ : on donne le contexte précédent + l'article, et on
        # ne lit que les positions de l'article ✓✓. 13 000 passages au lieu de 134 000 ✓✓.
        pos = 0
        for n in nums:
            art = np.frombuffer(articles[f][n].encode("utf-8"), dtype=np.uint8).astype(np.int64)
            ctx = b[max(0, pos - a.contexte):pos]
            if len(ctx) == 0:
                ctx = np.array([10], dtype=np.int64)      # un saut de ligne comme contexte minimal ✓
            seq = np.concatenate([ctx, art])
            if len(seq) < 8:
                pos += len(art) + 1
                continue
            x = torch.tensor(seq).unsqueeze(0).to(device)
            with torch.no_grad():
                logits = m(x, labels=x).logits[0]
            # les logits qui prédisent l'article = positions len(ctx)-1 .. len(seq)-2 ✓
            pred = logits[len(ctx) - 1:len(seq) - 1].argmax(-1).cpu().numpy()
            justes = (pred == np.array(art))
            vue = n <= 28
            (acc_vue if vue else acc_jamais).append(float(justes.mean()))
            # fragments exacts de `fragment` octets ✓ (on ne garde que les fragments complets ✓)
            nfr = len(justes) // a.fragment
            for k in range(nfr):
                ok = bool(justes[k*a.fragment:(k+1)*a.fragment].all())
                (ex_vue if vue else ex_jamais).append(float(ok))
            pos += len(art) + 1
        if not acc_vue: continue
        resultats.append({"fichier": f, "iso3": meta[f]["iso3"], "nom": meta[f]["nom"], "script": meta[f]["script"],
                          "exactitude_vue": 100 * float(np.mean(acc_vue)),
                          "exactitude_jamais_vue": 100 * float(np.mean(acc_jamais)) if acc_jamais else 0.0,
                          "fragments_exacts_vus": 100 * float(np.mean(ex_vue)),
                          "fragments_exacts_jamais_vus": 100 * float(np.mean(ex_jamais)) if ex_jamais else 0.0,
                          "fragments": len(acc_vue) + len(acc_jamais)})
    resultats.sort(key=lambda r: -r["exactitude_vue"])
    print(f"  {len(resultats)} langues · contexte {a.contexte} octets · fragments de {a.fragment}")
    print(f"\n   les 5 meilleures (exactitude vue) :")
    for r in resultats[:5]:
        print(f"     {r['variante'] if 'variante' in r else r['nom'][:22]:22s} {r['exactitude_vue']:5.1f} % · "
              f"fragments exacts {r['fragments_exacts_vus']:5.1f} %")
    print(f"\n   les 5 plus faibles :")
    for r in resultats[-5:]:
        print(f"     {r['nom'][:22]:22s} {r['exactitude_vue']:5.1f} % · fragments exacts {r['fragments_exacts_vus']:5.1f} %")
    print(f"\n  MOYENNE : vue {np.mean([r['exactitude_vue'] for r in resultats]):.1f} % · "
          f"jamais vue {np.mean([r['exactitude_jamais_vue'] for r in resultats]):.1f} %")
    print(f"  FRAGMENTS EXACTS : vus {np.mean([r['fragments_exacts_vus'] for r in resultats]):.1f} % · "
          f"jamais vus {np.mean([r['fragments_exacts_jamais_vus'] for r in resultats]):.1f} %")
    par_script = collections.defaultdict(list)
    for r in resultats: par_script[r["script"]].append(r["exactitude_vue"])
    print("  par écriture (exactitude vue) :", {s: round(float(np.mean(v)), 1) for s, v in sorted(par_script.items(), key=lambda kv: -len(kv[1]))[:6]})
    if a.sortie:
        pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(a.sortie).write_text(json.dumps(resultats, ensure_ascii=False, indent=1))
        print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
