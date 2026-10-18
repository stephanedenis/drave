#!/usr/bin/env python3
"""sonder_udhr.py — LA LANGUE EST-ELLE LISIBLE DANS L'ÉTAT ? (400 langues, même contenu)

LA QUESTION, ET POURQUOI LE CORPUS UDHR LA REND PROPRE ✓✓. Le chapitre 7 avait mesuré la neutralité du noyau
sur **deux** langues ✓. Ici, **toutes les langues disent la MÊME CHOSE** (les 30 articles de la Déclaration ✓✓) :
le contenu est **constant** d'une langue à l'autre ✓. Donc un classifieur qui identifie la langue **ne peut pas**
s'appuyer sur le contenu ✗ — il n'a que la langue ✓✓. *C'est le dispositif le plus propre qu'on puisse avoir pour
cette question* ✓.

ET IL EST ENTRAÎNÉ SUR 20 ARTICLES, TESTÉ SUR LES 10 AUTRES ✓✓ : au test, le **contenu** est nouveau ✗✓ — le
classifieur doit généraliser à des articles qu'il n'a jamais vus, donc identifier la **langue** et pas l'article ✓.

TROIS TÂCHES ✗ :
  · `langue`   : identifier la langue parmi N (échantillon stratifié par écriture ✓) ;
  · `script`   : identifier l'**écriture** (latin, cyrillique, arabe, devanagari…) ✓ — la frontière la plus
    grossière, et la première à tomber si le noyau abstrait ✓✓ ;
  · `variante` : identifier la **variante** d'une même langue ✗✓ (l'occitan en a 7 ✓, le romanche 7, le hunde 3,
    le roumain 3 ✓) — c'est-à-dire distinguer des **traductions/dialectes** de la même langue ✓✓. *C'est le test
    « dialectes et styles » ✓.*

⚠️ CE QU'IL NE DIT PAS ✗ : il ne mesure pas si la langue est **utilisée** ✓, seulement si elle est **lisible** ✓ ;
et la moyenne des positions détruit l'ordre des mots ✗✓ — acceptable pour une langue ✓, pas pour un sens fin ✓.

Usage :
  python3 tools/sonder_udhr.py --hf /tmp/jouet-udhr --mode langue --n-langues 60
  python3 tools/sonder_udhr.py --hf /tmp/jouet-udhr --mode script
  python3 tools/sonder_udhr.py --hf /tmp/jouet-udhr --mode variante
"""
from __future__ import annotations
import argparse, collections, json, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from udhr_commun import charger_articles, charger_meta, charger_modele, etats_par_couche


def choisir_langues(meta, articles, mode, n_langues, script_filtre="", iso=""):
    dispo = {f: a for f, a in articles.items() if len(a) >= 28}
    if iso:
        gardes = {x.strip() for x in iso.split(",") if x.strip()}
        dispo = {f: v for f, v in dispo.items() if meta[f]["iso3"] in gardes}

    if mode == "script":
        # toutes les langues, mais on ne garde que les écritures assez représentées ✓
        par_script = collections.defaultdict(list)
        for f in dispo:
            par_script[meta[f]["script"]].append(f)
        gardes = {s: fs for s, fs in par_script.items() if len(fs) >= 2}
        return {f: (meta[f]["script"], meta[f]["script"]) for fs in gardes.values() for f in fs}
    if mode == "variante":
        par_iso = collections.defaultdict(list)
        for f in dispo:
            par_iso[meta[f]["iso3"]].append(f)
        multi = {k: v for k, v in par_iso.items() if len(v) >= 2}
        if not multi:
            return {}
        # on garde la langue qui a le PLUS de variantes ✓ (l'occitan ou le romanche, 7 chacune ✓)
        iso = max(multi, key=lambda k: len(multi[k]))
        return {f: (iso, meta[f]["variante"]) for f in multi[iso]}
    # mode langue : échantillon stratifié par écriture ✓
    par_script = collections.defaultdict(list)
    for f in sorted(dispo):
        if script_filtre and meta[f]["script"] != script_filtre:
            continue
        par_script[meta[f]["script"]].append(f)
    choisis = {}
    i = 0
    while len(choisis) < n_langues and i < 200:
        for s in sorted(par_script, key=lambda x: -len(par_script[x])):
            if i < len(par_script[s]) and len(choisis) < n_langues:
                f = par_script[s][i]
                choisis[f] = (meta[f]["iso3"], meta[f]["nom"])
        i += 1
    return choisis


def entrainer(X_train, y_train, X_test, n_classes, epochs=400, lr=2e-2):
    """Entraîne sur X_train, PRÉDIT sur X_test ✓✓ (le premier essai prédisait sur l'entraînement et
    indexait ensuite avec le masque de test ✗ — 800 contre 1 200, IndexError ✓✗)."""
    import torch
    torch.manual_seed(0)
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    Xt = torch.tensor(X_train, dtype=torch.float32, device=dev)
    yt = torch.tensor(y_train, dtype=torch.long, device=dev)
    Xv = torch.tensor(X_test, dtype=torch.float32, device=dev)
    couche = torch.nn.Linear(X_train.shape[1], n_classes).to(dev)
    opt = torch.optim.Adam(couche.parameters(), lr=lr, weight_decay=1e-3)
    for _ in range(epochs):
        opt.zero_grad()
        perte = torch.nn.functional.cross_entropy(couche(Xt), yt)
        perte.backward()
        opt.step()
    with torch.no_grad():
        logits = couche(Xv)
        pred = logits.argmax(1).cpu().numpy()
        top5 = logits.topk(min(5, n_classes), dim=1).indices.cpu().numpy()
    return pred, top5, couche


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="/tmp/jouet-udhr")
    ap.add_argument("--mode", choices=["langue", "script", "variante"], default="langue")
    ap.add_argument("--n-langues", type=int, default=60)
    ap.add_argument("--longueur", type=int, default=256)
    ap.add_argument("--couches", default="0,1,2,3,4,5,6,7,8")
    ap.add_argument("--pooling", choices=["moyenne", "position"], default="moyenne",
                    help="« moyenne » : un vecteur par article ✓ ; « position » : un vecteur par position ✓✓ "
                         "(c'est le choix du chapitre 7 ✓ — les deux ne mesurent pas la même chose ✓)")
    ap.add_argument("--train", type=int, default=20, help="nombre d'articles pour l'entraînement ✓")
    ap.add_argument("--tokeniseur", action="store_true")
    ap.add_argument("--script-filtre", default="", help="ne garder qu'une écriture ✓ (Latn, Cyrl, Arab…) : "
                    "sans cela, un classifieur de langue peut gagner en reconnaissant l'ÉCRITURE ✓✗")
    ap.add_argument("--iso", default="", help="liste d'iso3 à garder ✓ (ex. fra,eng) — pour comparer EXACTEMENT "
                    "deux langues entre deux modèles ✓✓")
    ap.add_argument("--temoin", action="store_true", help="CONTRÔLE NÉGATIF : mélanger les étiquettes ✓ — "
                    "la précision doit retomber au hasard ✓✓, sinon la sonde mesure autre chose ✗✗")
    ap.add_argument("--sortie", default="")
    a = ap.parse_args()
    couches = [int(x) for x in a.couches.split(",")]
    articles = charger_articles()
    meta = charger_meta()
    sel = choisir_langues(meta, articles, a.mode, a.n_langues, a.script_filtre, a.iso)
    if not sel:
        print("  ✗ aucune langue sélectionnée"); return 2
    fichiers = sorted(sel)
    classes = sorted({v[0] for v in sel.values()})
    cidx = {c: i for i, c in enumerate(classes)}
    print(f"  mode {a.mode} · {len(fichiers)} fichiers · {len(classes)} classes · {len(couches)} couches lues")
    m, encoder, device = charger_modele(a.hf, tokeniseur=a.tokeniseur)
    # on encode tout une fois ✓ : 30 articles par fichier ✓
    etats = {c: [] for c in couches}     # listes de vecteurs ✓
    y, art_ids = [], []
    for f in fichiers:
        for n in sorted(articles[f]):
            ids = encoder(articles[f][n], a.longueur)
            if len(ids) < 8:
                continue
            e = etats_par_couche(m, ids, couches, a.pooling)
            for c in couches:
                z = e[c]
                if a.pooling == "position":
                    # une ligne par position ✓ : la langue de l'article est répétée sur chaque position ✓
                    etats[c].append(np.atleast_2d(z))
                else:
                    etats[c].append(z[None, :])
            nrep = z.shape[0] if a.pooling == "position" else 1
            y.extend([cidx[sel[f][0]]] * nrep)
            art_ids.extend([n] * nrep)
    y = np.array(y); art_ids = np.array(art_ids)
    if a.temoin:
        rng = np.random.RandomState(0)
        y = rng.permutation(y) if a.pooling == "moyenne" else y[rng.permutation(len(y))]
        print("  ⚠️ CONTRÔLE NÉGATIF : étiquettes mélangées ✓ — la précision doit être au hasard ✓✓")
    masque_train, masque_test = art_ids <= a.train, art_ids > a.train
    print(f"  {len(y)} états · entraînement sur {masque_train.sum()} · test sur {masque_test.sum()}")
    hasard = 100 / len(classes)
    print(f"\n  couche | exactitude (test) | top-5 | hasard | verdict")
    resultats = {}
    for c in couches:
        X = np.concatenate(etats[c], axis=0).astype(np.float32)
        X = (X - X.mean(0)) / (X.std(0) + 1e-6)
        pred, top5, modele = entrainer(X[masque_train], y[masque_train], X[masque_test], len(classes))
        acc = 100 * float((pred == y[masque_test]).mean())
        acc5 = 100 * float(np.mean([y[masque_test][i] in top5[i] for i in range(masque_test.sum())]))
        verdict = "LA LANGUE ✓ (lisible)" if acc > 1.5 * hasard else ("neutre ✓✓" if acc < 1.2 * hasard else "±")
        resultats[c] = (acc, acc5, pred)
        print(f"  {c:>6} | {acc:>18.1f} | {acc5:>5.1f} | {hasard:>6.1f} | {verdict}")
    # la meilleure couche : par-classe et confusions ✓
    cbest = max(couches, key=lambda c: resultats[c][0])
    acc, acc5, pred = resultats[cbest]
    test = masque_test
    par_classe = collections.defaultdict(lambda: [0, 0])
    for p, v in zip(pred, y[test]):
        par_classe[int(v)][1] += 1
        if int(p) == int(v): par_classe[int(v)][0] += 1
    pires = sorted(((v[0] / max(1, v[1]), classes[k]) for k, v in par_classe.items()))[:5]
    meilleurs = sorted(((-v[0] / max(1, v[1]), classes[k]) for k, v in par_classe.items()))[:5]
    print(f"\n  couche {cbest} · exactitude {acc:.1f} % · top-5 {acc5:.1f} % · hasard {hasard:.1f} %")
    print("  les classes les MIEUX reconnues :", [f"{c} {1+r:.0%}" for r, c in meilleurs])
    print("  les classes les MOINS reconnues :", [f"{c} {r:.0%}" for r, c in pires])
    # confusions : les paires les plus fréquentes ✓
    conf = collections.Counter((classes[int(v)], classes[int(p)]) for p, v in zip(pred, y[test]) if int(p) != int(v))
    print("  confusions les plus fréquentes :", [(f"{v}→{p}", n) for (v, p), n in conf.most_common(5)])
    if a.sortie:
        pathlib.Path(a.sortie).write_text(json.dumps({"mode": a.mode, "classes": classes, "couches": couches,
            "resultats": {str(c): [resultats[c][0], resultats[c][1]] for c in couches}}, ensure_ascii=False, indent=1))
        print(f"  → {a.sortie}")
    return 0


raise SystemExit(main())
