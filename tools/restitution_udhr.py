#!/usr/bin/env python3
"""restitution_udhr.py — LA RESTITUTION : LE MODÈLE REPRODUIT-IL EXACTEMENT LE TEXTE, DANS CHAQUE LANGUE ?

LE PREMIER DES DEUX RÉGIMES ✓✓. Avant de demander à une couche commune de **traduire** ✗, il faut lui demander de
**restituer** ✓ : le texte qu'elle a lu doit pouvoir être **reproduit à l'identique**, dans la même langue ✓.
C'est la borne haute : *si la restitution n'est pas parfaite sur du texte vu, la traduction ne peut rien garantir*
✓✓.

CE QU'ON MESURE ✗, ET LES TROIS CHIFFRES QUI COMPTENT :
  · **bits par octet** ✓ : la perte du modèle sur le texte (la mesure habituelle) ;
  · **exactitude par octet** ✓ : la fraction des positions où l'octet le plus probable est le **bon** ✓ — c'est
    la « restitution » au sens strict ✓ ;
  · **articles exacts** ✓✓ : la fraction des articles où **TOUS** les octets sont justes ✓ — c'est la
    « restitution **parfaite** » ✓✓ (le chiffre le plus dur, et le seul qui mérite le mot ✓).

⚠️ CE QU'IL NE DIT PAS ✗ : le modèle est entraîné sur **tout** le corpus ✓ — ces chiffres mesurent la
**mémorisation** ✓✓ (capacité à stocker 448 langues sans se tromper ✓), pas la généralisation ✗. Et un article
« exact » peut l'être par chance sur les passages répétitifs (la Déclaration répète « tous les êtres humains » ✓).
"""
from __future__ import annotations
import argparse, collections, json, math, pathlib, sys
import numpy as np, torch
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from udhr_commun import charger_articles, charger_meta, charger_modele


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="/tmp/jouet-udhr")
    ap.add_argument("--longueur", type=int, default=256)
    ap.add_argument("--max-langues", type=int, default=0, help="0 = toutes ✓")
    ap.add_argument("--couche", type=int, default=-1)
    ap.add_argument("--tokeniseur", action="store_true")
    ap.add_argument("--sortie", default="reports/restitution-udhr.json")
    a = ap.parse_args()
    articles = charger_articles(); meta = charger_meta()
    fichiers = sorted(f for f in articles if len(articles[f]) >= 28)
    if a.max_langues:
        fichiers = fichiers[: a.max_langues]
    m, encoder, device = charger_modele(a.hf, tokeniseur=a.tokeniseur)
    resultats = []
    for f in fichiers:
        bits, exacts, tot_pos, tot_art = [], 0, 0, 0
        for n in sorted(articles[f]):
            ids = encoder(articles[f][n], a.longueur)
            if len(ids) < 8: continue
            with torch.no_grad():
                x = ids.unsqueeze(0)
                sortie = m(x, labels=x)
                logits = sortie.logits[0, :-1]
                cibles = ids[1:]
                perte = float(sortie.loss)
                pred = logits.argmax(-1)
                justes = (pred == cibles)
                bits.append(perte / math.log(2))
                tot_pos += len(cibles)
                exacts += int(bool(justes.all()))
                tot_art += 1
        if not bits: continue
        resultats.append({"fichier": f, "iso3": meta[f]["iso3"], "nom": meta[f]["nom"], "script": meta[f]["script"],
                          "variante": meta[f]["variante"], "bits_octet": float(np.mean(bits)),
                          "articles": tot_art, "articles_exacts": exacts,
                          "taux_exact": 100 * exacts / max(1, tot_art)})
    resultats.sort(key=lambda x: x["bits_octet"])
    print(f"  {len(resultats)} langues · couche de sortie")
    print(f"\n  meilleures restitutions (bits/octet bas ✓) :")
    for r in resultats[:6]:
        print(f"    {r['variante']:16s} {r['nom'][:24]:24s} {r['bits_octet']:5.3f} b/o · {r['articles_exacts']}/{r['articles']} articles EXACTS")
    print(f"\n  les plus difficiles :")
    for r in resultats[-6:]:
        print(f"    {r['variante']:16s} {r['nom'][:24]:24s} {r['bits_octet']:5.3f} b/o · {r['articles_exacts']}/{r['articles']} articles EXACTS")
    par_script = collections.defaultdict(list)
    for r in resultats: par_script[r["script"]].append(r["bits_octet"])
    print("\n  par écriture (bits/octet moyen · nombre de langues) :")
    for s, v in sorted(par_script.items(), key=lambda kv: -len(kv[1])):
        print(f"    {s:6s} {np.mean(v):5.3f} · {len(v):3d} langue(s)")
    exacts_total = sum(r["articles_exacts"] for r in resultats)
    arts_total = sum(r["articles"] for r in resultats)
    print(f"\n  TOTAL : {exacts_total}/{arts_total} articles exacts ({100*exacts_total/max(1,arts_total):.1f} %) · "
          f"{np.mean([r['bits_octet'] for r in resultats]):.3f} bits/octet moyen")
    if a.sortie:
        pathlib.Path(a.sortie).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(a.sortie).write_text(json.dumps(resultats, ensure_ascii=False, indent=1))
        print(f"  → {a.sortie}")
    return 0


raise SystemExit(main())
