#!/usr/bin/env python3
"""retrieval_udhr.py — LA TRADUCTION : LE MÊME ARTICLE SE RETROUVE-T-IL D'UNE LANGUE À L'AUTRE ?

LA MESURE DE « TRADUCTION » DE CETTE SÉRIE ✓✓. Les 30 articles de la Déclaration sont **alignés** ✓ : l'article 7
dit la même chose dans toutes les langues ✓✓. On demande donc au modèle : *pour l'état de l'article 7 en français,
quel article de la liste anglaise est le plus proche ?* ✓ Si c'est **l'article 7** ✓✓, l'état porte le **sens**
d'une langue à l'autre ✓ — c'est exactement la couche commune en traduction ✓.

TROIS DISPOSITIFS DANS LE MÊME OUTIL ✗ :
  · `--mode paires`    : un jeu de paires représentatives (même famille, familles différentes, écritures
    différentes ✓) — la question « le sens traverse-t-il la frontière des langues ? » ✓ ;
  · `--mode variantes` : les variantes d'une **même** langue ✗✓ (occitan 7, romanche 7, houndé 3, roumain 3 ✓) —
    c'est le test « **dialectes et styles** » ✓✓ : le même sens, deux traductions, la même langue ✓ ;
  · `--mode temoin`    : le **contrôle négatif** ✓✓ — on mélange les articles d'une langue et on refait la mesure ✓ ;
    il **doit** retomber au hasard ✓ (3,3 %) ✗ — sinon, c'est que la mesure ne mesure rien ✓✓.

⚠️ CE QU'IL NE DIT PAS ✗ : il ne lit que **30 articles** ✓ (chance 3,3 % ✓) et compare des **états moyens** ✓✗
(une moyenne sur les positions, pas un alignement mot à mot ✓) ; et il ne dit rien de la **qualité** de la
traduction ✗ — seulement si le **bon article** est retrouvé ✓.
"""
from __future__ import annotations
import argparse, collections, json, pathlib, sys
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from udhr_commun import charger_articles, charger_meta, charger_modele, etats_par_couche

# paires représentatives : (langue A, langue B, pourquoi) ✓
PAIRES = [
    ("fra", "eng", "familles différentes, même écriture"),
    ("fra", "deu", "familles différentes, même écriture"),
    ("fra", "spa", "même famille (romane)"),
    ("fra", "ita", "même famille (romane)"),
    ("spa", "por", "même famille (ibérique)"),
    ("rus", "ukr", "même famille (slave), même écriture"),
    ("hin", "urd", "même famille, écritures différentes"),
    ("fra", "rus", "écritures différentes"),
    ("fra", "ara", "écritures et familles différentes"),
    ("fra", "cmn", "écritures et familles très différentes"),
    ("fra", "jpn", "écritures et familles très différentes"),
    ("eng", "cmn", "écritures et familles très différentes"),
    ("eng", "jpn", "écritures et familles très différentes"),
]


def etats_langue(m, encoder, articles, fichier, couches, longueur):
    """Les états moyens des articles d'une langue, par couche ✓."""
    out = {c: [] for c in couches}
    nums = []
    for n in sorted(articles[fichier]):
        ids = encoder(articles[fichier][n], longueur)
        if len(ids) < 8:
            continue
        e = etats_par_couche(m, ids, couches)
        for c in couches:
            out[c].append(e[c])
        nums.append(n)
    return {c: np.asarray(v, dtype=np.float32) for c, v in out.items()}, nums


def retrieval(A, B):
    """Top-1 et rang médian : pour chaque ligne de A, la ligne de B la plus proche ✓.

    On CENTRE les états ✓ (sans quoi une direction commune les rend tous proches ✓✗ — le piège du 17/10 ✓).
    """
    A = A - A.mean(0); B = B - B.mean(0)
    A = A / (np.linalg.norm(A, axis=1, keepdims=True) + 1e-9)
    B = B / (np.linalg.norm(B, axis=1, keepdims=True) + 1e-9)
    S = A @ B.T
    n = min(len(A), len(B))
    ordre = np.argsort(-S[:n], axis=1)
    rangs = np.array([int(np.where(ordre[i] == i)[0][0]) + 1 for i in range(n)])
    return 100 * float((rangs == 1).mean()), float(np.median(rangs)), n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf", default="/tmp/jouet-udhr")
    ap.add_argument("--mode", choices=["paires", "variantes", "temoin", "grille"], default="paires")
    ap.add_argument("--n-langues", type=int, default=40, help="taille de la grille ✓ (mode grille ✓)")
    ap.add_argument("--couche", type=int, default=-1)
    ap.add_argument("--longueur", type=int, default=256)
    ap.add_argument("--tokeniseur", action="store_true")
    ap.add_argument("--max-variantes", type=int, default=7)
    ap.add_argument("--iso-variante", default="", help="la langue dont on compare les variantes ✓ (oci, roh, ron, hus…)")
    ap.add_argument("--script", default="", help="ne garder qu'une écriture dans la grille ✓✓ (Latn pour contrôler "
                    "le confondant de l'alphabet ✓)")
    ap.add_argument("--genealogie", default="", help="data/udhr/genealogie.json ✓ : regroupe les paires par FAMILLE et par BRANCHE ✓✓")
    a = ap.parse_args()
    articles = charger_articles(); meta = charger_meta()
    par_iso = collections.defaultdict(list)
    for f in articles:
        if len(articles[f]) >= 28:
            par_iso[meta[f]["iso3"]].append(f)

    if a.mode == "variantes":
        multi = {k: v for k, v in par_iso.items() if len(v) >= 2}
        # ⚠️ LA LANGUE SE CHOISIT ✗✓ : par défaut celle qui a le plus de variantes ✓, mais on peut imposer
        # n'importe quelle langue à variantes ✓✓ (la réplication demande de changer de langue ✓).
        iso = a.iso_variante if a.iso_variante in multi else max(multi, key=lambda k: len(multi[k]))
        fichiers = sorted(multi[iso])[: a.max_variantes]
        print(f"  mode variantes · langue {iso} ({meta[fichiers[0]]['nom']}) · {len(fichiers)} variantes")
        for f in fichiers: print(f"    {meta[f]['variante']:20s} {len(articles[f])} articles")
    else:
        # on résout les paires en fichiers ✓ (la première variante de chaque iso3 ✓)
        def fichier(iso):
            return sorted(par_iso[iso])[0] if iso in par_iso else None
        if a.mode == "paires":
            paires = [(fichier(x), fichier(y), r) for x, y, r in PAIRES if fichier(x) and fichier(y)]
        else:
            paires = [(fichier(x), fichier(y), r) for x, y, r in PAIRES[:6] if fichier(x) and fichier(y)]
        fichiers = sorted({f for p in paires for f in p[:2]})
        print(f"  mode {a.mode} · {len(fichiers)} langues · {len(paires)} paires")

    if a.mode == "grille":
        # échantillon stratifié par écriture ✓ : on veut toutes les écritures, pas 40 langues latines ✓✓
        import collections as _c
        par_script = _c.defaultdict(list)
        for iso in sorted(par_iso):
            # ⚠️ ON SÉLECTIONNE DES FICHIERS, PAS DES CODES ISO ✗✓ (par_iso est indexé par iso3 ✓, et
            # etats_langue attend un nom de fichier ✓✓).
            f = sorted(par_iso[iso])[0]
            par_script[meta[f]["script"]].append(f)
        choisies, i = [], 0
        if a.script:
            par_script = {a.script: par_script.get(a.script, [])}
        while len(choisies) < a.n_langues and i < 100:
            for s in sorted(par_script, key=lambda x: -len(par_script[x])):
                if i < len(par_script[s]) and len(choisies) < a.n_langues:
                    choisies.append(par_script[s][i])
            i += 1
        fichiers = sorted(set(choisies))
        paires = []
        print(f"  mode grille · {len(fichiers)} langues · ")
        m, encoder, device = charger_modele(a.hf, tokeniseur=a.tokeniseur)
        cache = {}
        for f in fichiers:
            cache[f] = etats_langue(m, encoder, articles, f, [a.couche], a.longueur)
        # 1) toutes les paires ✓
        res = []
        for i in range(len(fichiers)):
            for j in range(i + 1, len(fichiers)):
                A, _ = cache[fichiers[i]]; B, _ = cache[fichiers[j]]
                t1, rk, n = retrieval(A[a.couche], B[a.couche])
                res.append((t1, rk, fichiers[i], fichiers[j]))
        print(f"\n  {len(res)} paires · top-1 moyen {np.mean([x[0] for x in res]):.1f} % · "
              f"médian {np.median([x[0] for x in res]):.1f} % · hasard 3,3 %")
        if a.genealogie and pathlib.Path(a.genealogie).exists():
            g = json.loads(pathlib.Path(a.genealogie).read_text())
            def fam(f): return g.get(pathlib.Path(f).name, {}).get("famille", "(inconnue)")
            def br(f):
                # la « branche » = les 3 premiers niveaux du chemin Glottolog ✓ (famille + 2 sous-niveaux ✓) :
                # le chemin complet ne coïncide que pour des dialectes d'une même langue ✓✗.
                return "/".join(g.get(pathlib.Path(f).name, {}).get("branche", "").split("/")[:3])
            groupes = {"même branche": [], "même famille, autre branche": [], "familles différentes": []}
            for t1, rk, fa, fb in res:
                if br(fa) and br(fa) == br(fb):
                    groupes["même branche"].append(t1)
                elif fam(fa) == fam(fb) and fam(fa) != "(inconnue)":
                    groupes["même famille, autre branche"].append(t1)
                else:
                    groupes["familles différentes"].append(t1)
            print("\n  PAR NIVEAU GÉNÉALOGIQUE (Glottolog ✓) :")
            for k, v in groupes.items():
                if v: print(f"    {k:28s} {np.mean(v):5.1f} % · {len(v):4d} paires")
        memes = [x[0] for x in res if meta[x[2]]["script"] == meta[x[3]]["script"]]
        diff = [x[0] for x in res if meta[x[2]]["script"] != meta[x[3]]["script"]]
        print(f"  même écriture : {np.mean(memes):.1f} % ({len(memes)} paires) · "
              f"écritures différentes : {np.mean(diff):.1f} % ({len(diff)} paires)")
        print("  les 4 meilleures paires :", [(f"{x[2][5:-4]}↔{x[3][5:-4]}", f"{x[0]:.0f}%") for x in sorted(res, key=lambda z: -z[0])[:4]])
        print("  les 4 plus faibles :", [(f"{x[2][5:-4]}↔{x[3][5:-4]}", f"{x[0]:.0f}%") for x in sorted(res, key=lambda z: z[0])[:4]])
        # moyenne par langue ✓✓ : le classement dit quelles langues Qwen aligne le mieux ✓
        par_langue = {}
        for t1, rk, fa, fb in res:
            par_langue.setdefault(fa, []).append(t1)
            par_langue.setdefault(fb, []).append(t1)
        classement = sorted(((np.mean(v), k) for k, v in par_langue.items()), reverse=True)
        print("  langues les MIEUX alignées :", [(k[5:-4], f"{m:.0f}%") for m, k in classement[:5]])
        print("  langues les MOINS alignées :", [(k[5:-4], f"{m:.0f}%") for m, k in classement[-5:]])
        # 2) le test le plus dur : le même article PARMI TOUS les états des autres langues ✓✓
        #    (40 langues × 30 articles = 1 200 candidats, hasard 0,08 %)
        A = np.concatenate([cache[f][0][a.couche] for f in fichiers], axis=0)
        n_l = len(fichiers)
        A = A - A.mean(0)
        A = A / (np.linalg.norm(A, axis=1, keepdims=True) + 1e-9)
        S = A @ A.T
        np.fill_diagonal(S, -9)             # on exclut l'état lui-même ✓
        pred = S.argmax(1)
        vrais = np.arange(len(A))
        # le bon voisin = le même article dans une AUTRE langue ✓ (n'importe laquelle ✓)
        art = np.tile(np.arange(30), n_l)
        lang = np.repeat(np.arange(n_l), 30)
        ok = (art[pred] == art[vrais]) & (lang[pred] != lang[vrais])
        print(f"\n  test groupé : même article parmi {n_l*30} états d'autres langues → {100*ok.mean():.2f} % "
              f"(hasard 3,3 % — le même article existe dans les {n_l} langues)")
        # contrôle : mélanger les articles d'une langue ✓
        # ⚠️ CONTRÔLE : une permutation DIFFÉRENTE par langue ✗✓. La même permutation pour toutes serait une
        # bijection ✓✗ — elle laisserait la relation intacte et le contrôle vaudrait exactement la mesure ✓✓
        # (c'est ce que le premier essai a fait : 6,50 % des deux côtés ✓✗).
        rng = np.random.RandomState(0)
        art_m = art.copy()
        for k in range(n_l):
            art_m[k*30:(k+1)*30] = rng.permutation(30)
        ok_c = (art_m[pred] == art_m[vrais]) & (lang[pred] != lang[vrais])
        print(f"  contrôle (articles mélangés) : {100*ok_c.mean():.2f} %")
        return 0
    m, encoder, device = charger_modele(a.hf, tokeniseur=a.tokeniseur)
    cache = {}
    for f in fichiers:
        cache[f] = etats_langue(m, encoder, articles, f, [a.couche], a.longueur)
    hasard = 100 / 30
    print(f"\n  paire                          | top-1 | rang médian | hasard | verdict")
    resultats = []
    if a.mode == "variantes":
        for i in range(len(fichiers)):
            for j in range(i + 1, len(fichiers)):
                A, _ = cache[fichiers[i]]; B, _ = cache[fichiers[j]]
                t1, rk, n = retrieval(A[a.couche], B[a.couche])
                resultats.append((t1, rk, f"{meta[fichiers[i]]['variante']} ↔ {meta[fichiers[j]]['variante']}"))
    else:
        for fa, fb, raison in paires:
            A, _ = cache[fa]; B, _ = cache[fb]
            t1, rk, n = retrieval(A[a.couche], B[a.couche])
            resultats.append((t1, rk, f"{meta[fa]['variante']} ↔ {meta[fb]['variante']} ({raison})"))
            if a.mode == "temoin":
                # contrôle négatif : on mélange les articles de B ✓
                Bm = B[a.couche][np.random.RandomState(0).permutation(len(B[a.couche]))]
                t1c, rkc, _ = retrieval(A[a.couche], Bm)
                resultats[-1] = (t1, rk, f"{meta[fa]['variante']} ↔ {meta[fb]['variante']} · TÉMOIN {t1c:.0f}% (rang {rkc:.0f})")
    for t1, rk, nom in resultats:
        verdict = "sens partagé ✓✓" if t1 > 2 * hasard else ("au hasard ✗" if t1 < 1.5 * hasard else "±")
        print(f"  {nom:44s} | {t1:5.1f} | {rk:>4.0f} / 30   | {hasard:5.1f} | {verdict}")
    if resultats:
        moys = [x[0] for x in resultats]
        print(f"\n  moyenne des paires : {np.mean(moys):.1f} % · médiane : {np.median(moys):.1f} % · hasard : {hasard:.1f} %")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
