#!/usr/bin/env python3
"""retrieval_epoque.py — J3.1 : le retrieval inter-langues à ÉPOQUE CONTRÔLÉE.

LA QUESTION. Panini avertit : leur signature lexicale capte l'époque (β +0,138) bien plus que la filiation
(β +0,049). Un retrieval inter-langues mesuré sans contrôler la date peut donc mesurer l'époque, pas la langue.
Ce script mesure trois choses, avec le même retrieval de surface (n-grammes de caractères, TF-IDF, cosinus) :

  1. **B7** (71 langues, 35 concepts, libellés Wikidata 2026) : le retrieval de CONCEPTS, à date unique.
     Il porte la SURFACE (écriture, famille) ; il ne peut pas porter l'époque.
  2. **UDHR** (21 langues du corpus commun, 30 articles, 1948) : le retrieval d'ARTICLES, à date unique.
     Toutes les paires sont contemporaines par construction ; il porte la surface.
  3. **BIBLE** (12 traductions datées de 1744 à 2019) : le retrieval de VERSETS, avec des couples
     contemporains et décalés. C'est le seul bras où l'époque varie ; il porte le contrôle de date.

LE RETRIEVAL. On représente chaque texte par ses n-grammes de caractères (n=3), pondérés TF-IDF, normalisés
L2 ; la similarité est le cosinus. Pour chaque requête de A, on classe les candidats de B et on regarde si le
bon (même concept, même article, même verset) est rang 1. Le hasard est 1/k (k candidats).

CE QUE CE N'EST PAS. Un retrieval de SURFACE : il ne teste pas le sens profond, seulement la signature
lexicale/orthographique. C'est exactement la grandeur de l'avertissement de Panini, mais ce n'est pas un modèle
neuronal. La fiche le dit.

CONTRÔLES NÉGATIFS. (a) mélanger les candidats de B : le top-1 doit retomber au hasard ; (b) pour B7, permuter
les libellés entre concepts et apparier une autre langue ; (c) pour la Bible, permuter les années des
traductions et refaire la régression : si l'époque compte, le coefficient observé doit sortir de la
distribution permutée.

Usage :
  python3 tools/retrieval_epoque.py                 # mesure complète, écrit reports/retrieval-epoque.json
  python3 tools/retrieval_epoque.py --rapide        # échantillon réduit, pour vérifier le dispositif
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import pathlib
import random
import re
import sys
import unicodedata
import urllib.request
import zipfile
from dataclasses import dataclass, field

import numpy as np
from scipy.sparse import csr_matrix

RACINE = pathlib.Path(__file__).resolve().parent.parent
SORTIE = RACINE / "reports" / "retrieval-epoque.json"
CACHE = RACINE / "work" / "retrieval-epoque" / "bibles"

# ---------------------------------------------------------------------------
# 0. Outils de surface
# ---------------------------------------------------------------------------

def normalise(texte: str) -> str:
    """NFKC, casse pliée, diacritiques retirés, ponctuation → espace."""
    t = unicodedata.normalize("NFKC", texte or "").casefold()
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^\w]+", " ", t, flags=re.UNICODE)
    return " ".join(t.split())


def ngrammes(texte: str, n: int = 3) -> collections.Counter:
    t = normalise(texte)
    return collections.Counter(t[i:i + n] for i in range(max(0, len(t) - n + 1)))


def tfidf(documents: list[str], n: int = 3):
    """TF-IDF creux, idf lissé, tf sous-linéaire, lignes normalisées L2."""
    compteurs = [ngrammes(d, n) for d in documents]
    df: collections.Counter = collections.Counter()
    for c in compteurs:
        df.update(c.keys())
    vocab = {g: i for i, g in enumerate(sorted(df))}
    N = len(documents)
    idf = np.array([math.log((1.0 + N) / (1.0 + df[g])) + 1.0 for g in vocab], dtype=np.float64)
    lignes, colonnes, valeurs = [], [], []
    for i, c in enumerate(compteurs):
        for g, k in c.items():
            j = vocab[g]
            lignes.append(i)
            colonnes.append(j)
            valeurs.append((1.0 + math.log(k)) * idf[j])
    M = csr_matrix((valeurs, (lignes, colonnes)), shape=(N, len(vocab)), dtype=np.float64)
    normes = np.sqrt(np.asarray(M.multiply(M).sum(axis=1)).ravel())
    normes[normes == 0] = 1.0
    M = csr_matrix(M.multiply(1.0 / normes[:, None]))
    return M, vocab, idf


def top1_et_rangs(MA, MB) -> tuple[float, float, float, np.ndarray]:
    """Top-1, MRR, rang médian et rangs pour des matrices de même nombre de lignes."""
    S = (MA @ MB.T).toarray()
    ordre = np.argsort(-S, axis=1)
    n = S.shape[0]
    rangs = np.array([int(np.where(ordre[i] == i)[0][0]) + 1 for i in range(n)])
    return float((rangs == 1).mean()), float((1.0 / rangs).mean()), float(np.median(rangs)), rangs


def bootstrap_proportion(hits: np.ndarray, B: int = 1000, graine: int = 0) -> tuple[float, float]:
    """IC 95 % par bootstrap sur les requêtes (hits ∈ {0,1})."""
    if len(hits) == 0:
        return (float("nan"), float("nan"))
    rng = np.random.RandomState(graine)
    moy = []
    for _ in range(B):
        idx = rng.randint(0, len(hits), len(hits))
        moy.append(float(hits[idx].mean()))
    return float(np.percentile(moy, 2.5)), float(np.percentile(moy, 97.5))


def derangement(n: int, rng: random.Random) -> list[int]:
    """Une permutation sans point fixe : la cible « mélangée » n'est jamais la bonne."""
    if n <= 1:
        return list(range(n))
    while True:
        p = rng.sample(range(n), n)
        if all(p[i] != i for i in range(n)):
            return p


def regression_surface(paires: list[dict], variables: list[str], graine: int = 0) -> dict:
    """OLS top1 ~ variables, avec IC bootstrap sur les paires (pas sur les requêtes)."""
    X = np.array([[float(p[v]) for v in variables] for p in paires], dtype=float)
    y = np.array([p["top1"] for p in paires], dtype=float)
    Xd = np.column_stack([np.ones(len(X)), X])
    coef, *_ = np.linalg.lstsq(Xd, y, rcond=None)
    rng = np.random.RandomState(graine + 11)
    coefs = []
    for _ in range(1000):
        idx = rng.randint(0, len(y), len(y))
        c, *_ = np.linalg.lstsq(Xd[idx], y[idx], rcond=None)
        coefs.append(c)
    coefs = np.array(coefs)
    noms = ["constante"] + variables
    return {
        "n_paires": len(y),
        "variables": variables,
        "coef": {nom: float(coef[i]) for i, nom in enumerate(noms)},
        "ic95": {nom: [float(np.percentile(coefs[:, i], 2.5)), float(np.percentile(coefs[:, i], 97.5))]
                 for i, nom in enumerate(noms)},
        "r2": float(1.0 - np.sum((y - Xd @ coef) ** 2) / np.sum((y - y.mean()) ** 2)),
    }


# ---------------------------------------------------------------------------
# 1. B7 — le lexique des 71 langues
# ---------------------------------------------------------------------------

# Familles (Glottolog, macro) : on ne prétend pas à la précision d'une feuille, seulement au niveau
# « même famille » qui est celui du test. Les isolats et les créoles sont nommés.
FAMILLE_B7 = {
    # indo-européen
    "ca": "Indo-European", "cs": "Indo-European", "da": "Indo-European", "de": "Indo-European",
    "el": "Indo-European", "en": "Indo-European", "es": "Indo-European", "fr": "Indo-European",
    "gl": "Indo-European", "hi": "Indo-European", "hr": "Indo-European", "it": "Indo-European",
    "lt": "Indo-European", "lv": "Indo-European", "mk": "Indo-European", "nb": "Indo-European",
    "ne": "Indo-European", "nl": "Indo-European", "nn": "Indo-European", "pl": "Indo-European",
    "pt": "Indo-European", "ro": "Indo-European", "ru": "Indo-European", "si": "Indo-European",
    "sk": "Indo-European", "sl": "Indo-European", "sq": "Indo-European", "sr": "Indo-European",
    "sv": "Indo-European", "uk": "Indo-European", "ur": "Indo-European", "fa": "Indo-European",
    "be": "Indo-European", "bs": "Indo-European", "cy": "Indo-European", "ga": "Indo-European",
    "hy": "Indo-European", "pa": "Indo-European", "bn": "Indo-European",
    # autres
    "hu": "Uralic", "fi": "Uralic", "et": "Uralic",
    "eu": "Basque", "mt": "Afro-Asiatic", "tr": "Turkic", "az": "Turkic", "kk": "Turkic",
    "ky": "Turkic", "uz": "Turkic", "mn": "Mongolic", "ja": "Japonic", "ko": "Koreanic",
    "zh": "Sino-Tibetan", "ta": "Dravidian", "th": "Tai-Kadai", "vi": "Austroasiatic",
    "km": "Austroasiatic", "id": "Austronesian", "ms": "Austronesian",
    "sw": "Atlantic-Congo", "yo": "Atlantic-Congo", "zu": "Atlantic-Congo",
    "am": "Afro-Asiatic", "ar": "Afro-Asiatic", "he": "Afro-Asiatic", "so": "Afro-Asiatic",
    "ka": "Kartvelian", "eo": "Constructed", "af": "Indo-European", "is": "Indo-European",
    "lo": "Tai-Kadai",
}


def script_dominant(libelles: list[str]) -> str:
    """L'écriture dominante d'un ensemble de libellés, par comptage de points de code."""
    plages = [
        ("Latn", [(0x0041, 0x024F), (0x1E00, 0x1EFF)]),
        ("Cyrl", [(0x0400, 0x04FF), (0x0500, 0x052F)]),
        ("Grek", [(0x0370, 0x03FF), (0x1F00, 0x1FFF)]),
        ("Arab", [(0x0600, 0x06FF), (0x0750, 0x077F), (0x08A0, 0x08FF), (0xFB50, 0xFDFF)]),
        ("Hebr", [(0x0590, 0x05FF)]),
        ("Deva", [(0x0900, 0x097F)]),
        ("Beng", [(0x0980, 0x09FF)]),
        ("Guru", [(0x0A00, 0x0A7F)]),
        ("Taml", [(0x0B80, 0x0BFF)]),
        ("Sinh", [(0x0D80, 0x0DFF)]),
        ("Thai", [(0x0E00, 0x0E7F)]),
        ("Laoo", [(0x0E80, 0x0EFF)]),
        ("Ethi", [(0x1200, 0x137F)]),
        ("Armn", [(0x0530, 0x058F)]),
        ("Geor", [(0x10A0, 0x10FF)]),
        ("Khmr", [(0x1780, 0x17FF)]),
        ("Mymr", [(0x1000, 0x109F)]),
        ("Hang", [(0xAC00, 0xD7AF), (0x1100, 0x11FF)]),
        ("Kana", [(0x3040, 0x30FF)]),
        ("Hani", [(0x3400, 0x4DBF), (0x4E00, 0x9FFF)]),
    ]
    compte: collections.Counter = collections.Counter()
    for lib in libelles:
        for c in lib:
            cp = ord(c)
            for nom, bornes in plages:
                if any(a <= cp <= b for a, b in bornes):
                    compte[nom] += 1
                    break
    if not compte:
        return "Inconnu"
    # le japonais mêle kanji et kana : le kana est le marqueur
    if compte.get("Kana", 0) > 0:
        return "Jpan"
    return compte.most_common(1)[0][0]


def charge_b7() -> dict:
    chemin = RACINE / "tools" / "jeux" / "lexique_multilingue.json"
    d = json.loads(chemin.read_text(encoding="utf-8"))
    concepts = d["concepts"]
    langues = d["langues"]
    # libellés par langue
    par_langue: dict[str, dict[str, list[str]]] = {l: {} for l in langues}
    for concept, c in concepts.items():
        for langue, formes in c.get("labels", {}).items():
            if langue in par_langue and formes:
                par_langue[langue][concept] = list(formes)
    meta = {}
    for l in langues:
        libelles = [x for formes in par_langue[l].values() for x in formes]
        meta[l] = {
            "famille": FAMILLE_B7.get(l, "Inconnue"),
            "script": script_dominant(libelles),
            "n_concepts": len(par_langue[l]),
        }
    return {"donnees": d, "langues": langues, "concepts": concepts,
            "par_langue": par_langue, "meta": meta}


def b7_mesure(b7: dict, graine: int = 0) -> dict:
    langues = b7["langues"]
    par_langue = b7["par_langue"]
    meta = b7["meta"]
    # vocabulaire global des libellés, puis matrices par langue
    docs, index = [], []
    for l in langues:
        for concept, formes in par_langue[l].items():
            for f in formes:
                docs.append(f)
                index.append((l, concept))
    M, vocab, idf = tfidf(docs, n=3)
    # matrice par langue : moyenne des vecteurs de ses libellés, par concept
    matrices: dict[str, tuple[list[str], csr_matrix]] = {}
    for l in langues:
        concepts_l = sorted(par_langue[l])
        positions = {c: [] for c in concepts_l}
        for i, (ll, c) in enumerate(index):
            if ll == l:
                positions[c].append(i)
        lignes = []
        for c in concepts_l:
            v = M[positions[c]].mean(axis=0)
            lignes.append(v)
        if lignes:
            X = csr_matrix(np.vstack([np.asarray(x).ravel() for x in lignes]))
            normes = np.sqrt(np.asarray(X.multiply(X).sum(axis=1)).ravel())
            normes[normes == 0] = 1.0
            X = csr_matrix(X.multiply(1.0 / normes[:, None]))
            matrices[l] = (concepts_l, X)
    rng = random.Random(graine)
    paires = []
    for a in langues:
        if a not in matrices:
            continue
        for b in langues:
            if a == b or b not in matrices:
                continue
            ca, XA = matrices[a]
            cb, XB = matrices[b]
            communs = [c for c in ca if c in set(cb)]
            if len(communs) < 5:
                continue
            ia = [ca.index(c) for c in communs]
            ib = [cb.index(c) for c in communs]
            A = XA[ia]
            B = XB[ib]
            t1, mrr, rk, rangs = top1_et_rangs(A, B)
            chance = 1.0 / len(cb)
            # contrôle 1 : étiquettes mélangées — la bonne réponse est une cible tirée au hasard
            S = (A @ B.T).toarray()
            pred = np.argmax(S, axis=1)
            perm = derangement(len(communs), rng)
            t1p = float((pred == perm).mean())
            paires.append({
                "a": a, "b": b,
                "script_a": meta[a]["script"], "script_b": meta[b]["script"],
                "famille_a": meta[a]["famille"], "famille_b": meta[b]["famille"],
                "script_match": meta[a]["script"] == meta[b]["script"],
                "famille_match": meta[a]["famille"] == meta[b]["famille"],
                "n_concepts": len(communs), "n_candidats": len(cb),
                "top1": t1, "mrr": mrr, "rang_median": rk,
                "chance": chance, "controle_permutation": t1p,
                "ic_bas": None, "ic_haut": None,
            })
            # IC bootstrap sur les requêtes (seulement pour un sous-ensemble, pour la vitesse)
            if len(paires) % 7 == 0:
                bas, haut = bootstrap_proportion((rangs == 1).astype(float), B=300, graine=graine)
                paires[-1]["ic_bas"], paires[-1]["ic_haut"] = bas, haut
    # agrégats
    def agg(filtre):
        vals = [p["top1"] for p in paires if filtre(p)]
        return {
            "n_paires": len(vals),
            "top1_moyen": float(np.mean(vals)) if vals else None,
            "top1_median": float(np.median(vals)) if vals else None,
            "ic_bas": float(np.percentile(vals, 2.5)) if vals else None,
            "ic_haut": float(np.percentile(vals, 97.5)) if vals else None,
        }
    agregats = {
        "toutes": agg(lambda p: True),
        "script_meme": agg(lambda p: p["script_match"]),
        "script_different": agg(lambda p: not p["script_match"]),
        "famille_meme": agg(lambda p: p["famille_match"]),
        "famille_differente": agg(lambda p: not p["famille_match"]),
        "script_meme_famille_meme": agg(lambda p: p["script_match"] and p["famille_match"]),
        "script_meme_famille_differente": agg(lambda p: p["script_match"] and not p["famille_match"]),
        "script_different_famille_meme": agg(lambda p: not p["script_match"] and p["famille_match"]),
        "script_different_famille_differente": agg(lambda p: not p["script_match"] and not p["famille_match"]),
    }
    # contrôle global : permutation des libellés et appariement d'une autre langue
    rng2 = random.Random(graine + 1)
    echantillon = rng2.sample(paires, min(200, len(paires)))
    ctrl_langue = []
    for p in echantillon:
        a, b = p["a"], p["b"]
        autres = [l for l in langues if l not in (a, b) and l in matrices]
        if not autres:
            continue
        b2 = rng2.choice(autres)
        ca, XA = matrices[a]
        cb2, XB2 = matrices[b2]
        communs = [c for c in ca if c in set(cb2)]
        if len(communs) < 5:
            continue
        ia = [ca.index(c) for c in communs]
        ib = [cb2.index(c) for c in communs]
        t1, _, _, _ = top1_et_rangs(XA[ia], XB2[ib])
        ctrl_langue.append(t1)
    controles = {
        "permutation_libelles_top1_moyen": float(np.mean([p["controle_permutation"] for p in paires])),
        "permutation_libelles_chance_moyenne": float(np.mean([p["chance"] for p in paires])),
        "appariement_autre_langue_top1_moyen": float(np.mean(ctrl_langue)) if ctrl_langue else None,
        "appariement_autre_langue_n": len(ctrl_langue),
    }
    regression = regression_surface(
        paires, ["script_match", "famille_match", "chance"],
        graine=graine)
    langues_paires = {p["a"] for p in paires} | {p["b"] for p in paires}
    return {
        "n_langues": len(langues), "n_concepts": len(b7["concepts"]),
        "n_langues_avec_libelle": len(matrices),
        "n_langues_dans_paires": len(langues_paires),
        "langues_hors_paires": sorted(set(langues) - langues_paires),
        "meta_langues": meta,
        "agregats": agregats,
        "regression": regression,
        "controles": controles,
        "paires": paires,
    }


# ---------------------------------------------------------------------------
# 2. UDHR — le corpus commun, 21 langues, 30 articles, 1948
# ---------------------------------------------------------------------------

LANGUES_UDHR = [
    "udhr_amh", "udhr_arb", "udhr_bel", "udhr_cmn_hant", "udhr_cnh", "udhr_ctd",
    "udhr_ell_monotonic", "udhr_eng", "udhr_ewe", "udhr_fra", "udhr_fuf_adlm",
    "udhr_hau_NE", "udhr_heb", "udhr_hin", "udhr_ibo", "udhr_ind", "udhr_jav",
    "udhr_kin", "udhr_mly_arab", "udhr_mya", "udhr_tgl",
]


def charge_udhr() -> dict:
    fichiers = {f + ".xml": f for f in LANGUES_UDHR}
    articles: dict[str, dict[int, str]] = {}
    for ligne in (RACINE / "data" / "udhr" / "articles_propres.jsonl").read_text(encoding="utf-8").splitlines():
        x = json.loads(ligne)
        if x["fichier"] in fichiers:
            articles.setdefault(fichiers[x["fichier"]], {})[int(x["art"])] = x["texte"]
    meta = json.loads((RACINE / "data" / "udhr" / "meta.json").read_text(encoding="utf-8"))
    genealogie = json.loads((RACINE / "data" / "udhr" / "genealogie.json").read_text(encoding="utf-8"))
    meta_l = {}
    for f in LANGUES_UDHR:
        m = dict(meta[f + ".xml"])
        g = genealogie.get(f + ".xml", {})
        m["famille"] = g.get("famille", "Inconnue")
        m["branche"] = g.get("branche", "")
        m["epoque"] = 1948
        meta_l[f] = m
    return {"articles": articles, "meta": meta_l}


def udhr_mesure(udhr: dict, graine: int = 0) -> dict:
    langues = [f for f in LANGUES_UDHR if len(udhr["articles"].get(f, {})) >= 28]
    textes = {f: [udhr["articles"][f][a] for a in sorted(udhr["articles"][f])] for f in langues}
    tous = [t for f in langues for t in textes[f]]
    M, vocab, idf = tfidf(tous, n=3)
    # découpe par langue
    matrices = {}
    pos = 0
    for f in langues:
        k = len(textes[f])
        matrices[f] = M[pos:pos + k]
        pos += k
    rng = random.Random(graine)
    paires = []
    for a in langues:
        for b in langues:
            if a == b:
                continue
            A, B = matrices[a], matrices[b]
            t1, mrr, rk, rangs = top1_et_rangs(A, B)
            # contrôle : étiquettes mélangées — la bonne réponse est une cible tirée au hasard
            S = (A @ B.T).toarray()
            pred = np.argmax(S, axis=1)
            perm = derangement(A.shape[0], rng)
            t1p = float((pred == perm).mean())
            ma, mb = udhr["meta"][a], udhr["meta"][b]
            paires.append({
                "a": a, "b": b,
                "script_a": ma.get("script"), "script_b": mb.get("script"),
                "famille_a": ma.get("famille"), "famille_b": mb.get("famille"),
                "script_match": ma.get("script") == mb.get("script"),
                "famille_match": ma.get("famille") == mb.get("famille"),
                "n_requetes": len(textes[a]), "n_candidats": len(textes[b]),
                "top1": t1, "mrr": mrr, "rang_median": rk,
                "chance": 1.0 / len(textes[b]),
                "controle_permutation": t1p,
                "epoque_a": ma.get("epoque"), "epoque_b": mb.get("epoque"),
            })
    def agg(filtre):
        vals = [p["top1"] for p in paires if filtre(p)]
        return {
            "n_paires": len(vals),
            "top1_moyen": float(np.mean(vals)) if vals else None,
            "top1_median": float(np.median(vals)) if vals else None,
            "ic_bas": float(np.percentile(vals, 2.5)) if vals else None,
            "ic_haut": float(np.percentile(vals, 97.5)) if vals else None,
        }
    agregats = {
        "toutes": agg(lambda p: True),
        "script_meme": agg(lambda p: p["script_match"]),
        "script_different": agg(lambda p: not p["script_match"]),
        "famille_meme": agg(lambda p: p["famille_match"]),
        "famille_differente": agg(lambda p: not p["famille_match"]),
        "script_meme_famille_meme": agg(lambda p: p["script_match"] and p["famille_match"]),
        "script_meme_famille_differente": agg(lambda p: p["script_match"] and not p["famille_match"]),
        "script_different_famille_meme": agg(lambda p: not p["script_match"] and p["famille_match"]),
        "script_different_famille_differente": agg(lambda p: not p["script_match"] and not p["famille_match"]),
    }
    controles = {
        "permutation_articles_top1_moyen": float(np.mean([p["controle_permutation"] for p in paires])),
        "chance_moyenne": float(np.mean([p["chance"] for p in paires])),
        "epoques_distinctes": sorted({p["epoque_a"] for p in paires} | {p["epoque_b"] for p in paires}),
    }
    regression = regression_surface(
        paires, ["script_match", "famille_match", "chance"],
        graine=graine)
    return {
        "n_langues": len(langues), "n_articles": 30, "epoque": 1948,
        "meta_langues": udhr["meta"],
        "agregats": agregats, "regression": regression,
        "controles": controles, "paires": paires,
    }


# ---------------------------------------------------------------------------
# 3. BIBLE — 12 traductions datées
# ---------------------------------------------------------------------------

BIBLES = {
    # id : (nom, langue, iso3, script, famille, année, licence, url, fichier local)
    "OST": ("Ostervald", "français", "fra", "Latn", "Indo-European", 1744, "domaine public",
            "https://ebible.org/Scriptures/fra_fob_usfm.zip", "fra_fob_usfm.zip"),
    "KJV": ("King James (texte standard 1769)", "anglais", "eng", "Latn", "Indo-European", 1769,
            "domaine public", "https://ebible.org/Scriptures/eng-kjv_usfm.zip", "eng-kjv_usfm.zip"),
    "RUS": ("Synodal", "russe", "rus", "Cyrl", "Indo-European", 1876, "domaine public",
            "https://ebible.org/Scriptures/russyn_usfm.zip", "russyn_usfm.zip"),
    "SPA": ("Reina-Valera 1909", "espagnol", "spa", "Latn", "Indo-European", 1909, "domaine public",
            "https://ebible.org/Scriptures/spaRV1909_usfm.zip", "spaRV1909_usfm.zip"),
    "LSG": ("Louis Segond 1910", "français", "fra", "Latn", "Indo-European", 1910, "domaine public",
            "https://ebible.org/Scriptures/fraLSG_usfm.zip", "fraLSG_usfm.zip"),
    "LUT": ("Luther 1912", "allemand", "deu", "Latn", "Indo-European", 1912, "domaine public",
            "https://ebible.org/Scriptures/deu1912_usfm.zip", "deu1912_usfm.zip"),
    "CUV": ("Chinese Union Version", "chinois", "cmn", "Hani", "Sino-Tibetan", 1919, "domaine public",
            "https://ebible.org/Scriptures/cmn-cu89s_usfm.zip", "cmn-cu89s_usfm.zip"),
    "WEB": ("World English Bible", "anglais", "eng", "Latn", "Indo-European", 2000, "domaine public",
            "https://ebible.org/Scriptures/eng-web_usfm.zip", "eng-web_usfm.zip"),
    "ARB": ("New Arabic Version", "arabe", "arb", "Arab", "Afro-Asiatic", 2012, "CC BY-SA 4.0",
            "https://ebible.org/Scriptures/arbnav_usfm.zip", "arbnav_usfm.zip"),
    "HIN": ("Indian Revised Version", "hindi", "hin", "Deva", "Indo-European", 2017, "CC BY-SA 4.0",
            "https://ebible.org/Scriptures/hin2017_usfm.zip", "hin2017_usfm.zip"),
    "POR": ("Bíblia Livre", "portugais", "por", "Latn", "Indo-European", 2018, "CC BY 4.0",
            "https://ebible.org/Scriptures/porbr2018_usfm.zip", "porbr2018_usfm.zip"),
    "PCM": ("Nigerian Pidgin", "pidgin nigérian", "pcm", "Latn", "Creole anglais", 2019,
            "© Wycliffe, redistribution", "https://ebible.org/Scriptures/pcm_usfm.zip", "pcm_usfm.zip"),
}

LIVRES_NARRATIFS = {"GEN", "EXO", "MAT", "MRK", "LUK", "JHN", "ACT"}


def sha256(chemin: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def telecharge(url: str, dest: pathlib.Path) -> pathlib.Path:
    if dest.exists() and dest.stat().st_size > 100_000:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Drave-J3.1/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        dest.write_bytes(r.read())
    return dest


def parse_usfm(texte: str) -> dict[tuple[str, int, int], str]:
    out: dict[tuple[str, int, int], str] = {}
    livre = None
    chapitre = None
    for ligne in texte.splitlines():
        m = re.match(r"\\id\s+([A-Z0-9]{3})", ligne)
        if m:
            livre = m.group(1)
            continue
        m = re.match(r"\\c\s+(\d+)", ligne)
        if m:
            chapitre = int(m.group(1))
            continue
        m = re.match(r"\\v\s+(\d+)\s+(.*)", ligne)
        if m and livre and chapitre:
            t = re.sub(r"\\[a-z]+\*?", " ", m.group(2))
            t = re.sub(r"\{[^}]*\}", " ", t)
            t = " ".join(t.split())
            if t:
                out[(livre, chapitre, int(m.group(1)))] = t
    return out


def charge_usfm(zip_path: pathlib.Path) -> dict[tuple[str, int, int], str]:
    out = {}
    with zipfile.ZipFile(zip_path) as zf:
        for nom in zf.namelist():
            if nom.lower().endswith(".usfm"):
                out.update(parse_usfm(zf.read(nom).decode("utf-8", "ignore")))
    return out


def charge_bible(n_versets: int = 1000, graine: int = 0, rapide: bool = False) -> dict:
    CACHE.mkdir(parents=True, exist_ok=True)
    textes: dict[str, dict] = {}
    empreintes = {}
    for cle, (nom, langue, iso3, script, famille, annee, licence, url, fichier) in BIBLES.items():
        chemin = CACHE / fichier
        telecharge(url, chemin)
        empreintes[fichier] = sha256(chemin)
        textes[cle] = charge_usfm(chemin)
    communs = set.intersection(*[set(t) for t in textes.values()])
    communs = {k for k in communs if k[0] in LIVRES_NARRATIFS}
    # longueur 20–600 dans toutes les traductions, puis déduplication des versets répétés
    cles = [k for k in sorted(communs) if all(20 <= len(textes[c][k]) <= 600 for c in textes)]
    for c in textes:
        vus: collections.Counter = collections.Counter()
        for k in cles:
            vus[normalise(textes[c][k])] += 1
        cles = [k for k in cles if vus[normalise(textes[c][k])] == 1]
    rng = random.Random(graine)
    if rapide:
        cles = cles[:300]
    elif len(cles) > n_versets:
        cles = rng.sample(cles, n_versets)
    cles = sorted(cles)
    meta = {}
    for cle, (nom, langue, iso3, script, famille, annee, licence, url, fichier) in BIBLES.items():
        meta[cle] = {
            "nom": nom, "langue": langue, "iso3": iso3, "script": script,
            "famille": famille, "annee": annee, "licence": licence, "url": url,
            "fichier": fichier, "sha256": empreintes[fichier],
            "n_versets_source": len(textes[cle]),
        }
    return {"cles": cles, "textes": {c: [textes[c][k] for k in cles] for c in BIBLES},
            "meta": meta, "n_communs": len(communs), "n_retenus": len(cles)}


def bible_mesure(bible: dict, graine: int = 0, rapide: bool = False) -> dict:
    cles = bible["cles"]
    noms = list(BIBLES)
    docs = [t for c in noms for t in bible["textes"][c]]
    M, vocab, idf = tfidf(docs, n=3)
    matrices = {}
    pos = 0
    for c in noms:
        k = len(bible["textes"][c])
        matrices[c] = M[pos:pos + k]
        pos += k
    rng = random.Random(graine)
    paires = []
    for a in noms:
        for b in noms:
            if a == b:
                continue
            A, B = matrices[a], matrices[b]
            t1, mrr, rk, rangs = top1_et_rangs(A, B)
            # contrôle : étiquettes mélangées — la bonne réponse est une cible tirée au hasard
            S = (A @ B.T).toarray()
            pred = np.argmax(S, axis=1)
            perm = derangement(A.shape[0], rng)
            t1p = float((pred == perm).mean())
            ma, mb = bible["meta"][a], bible["meta"][b]
            paires.append({
                "a": a, "b": b,
                "annee_a": ma["annee"], "annee_b": mb["annee"],
                "delta_annees": abs(ma["annee"] - mb["annee"]),
                "script_a": ma["script"], "script_b": mb["script"],
                "famille_a": ma["famille"], "famille_b": mb["famille"],
                "langue_a": ma["langue"], "langue_b": mb["langue"],
                "script_match": ma["script"] == mb["script"],
                "famille_match": ma["famille"] == mb["famille"],
                "langue_match": ma["langue"] == mb["langue"],
                "n_requetes": A.shape[0], "n_candidats": B.shape[0],
                "top1": t1, "mrr": mrr, "rang_median": rk,
                "chance": 1.0 / B.shape[0],
                "controle_permutation": t1p,
            })
    # matrice top-1
    matrice = {a: {b: next((p["top1"] for p in paires if p["a"] == a and p["b"] == b), None)
                   for b in noms} for a in noms}
    # agrégats
    def agg(filtre):
        vals = [p["top1"] for p in paires if filtre(p)]
        return {
            "n_paires": len(vals),
            "top1_moyen": float(np.mean(vals)) if vals else None,
            "top1_median": float(np.median(vals)) if vals else None,
            "ic_bas": float(np.percentile(vals, 2.5)) if vals else None,
            "ic_haut": float(np.percentile(vals, 97.5)) if vals else None,
        }
    agregats = {
        "toutes": agg(lambda p: True),
        "script_meme": agg(lambda p: p["script_match"]),
        "script_different": agg(lambda p: not p["script_match"]),
        "famille_meme": agg(lambda p: p["famille_match"]),
        "famille_differente": agg(lambda p: not p["famille_match"]),
        "langue_meme": agg(lambda p: p["langue_match"]),
        "langue_differente": agg(lambda p: not p["langue_match"]),
        "contemporain_50": agg(lambda p: p["delta_annees"] <= 50),
        "decalé_150": agg(lambda p: p["delta_annees"] >= 150),
        "script_meme_contemporain": agg(lambda p: p["script_match"] and p["delta_annees"] <= 50),
        "script_meme_decalé": agg(lambda p: p["script_match"] and p["delta_annees"] >= 150),
    }
    # contrastes appariés : pivot anglais (KJV 1769 vs WEB 2000), pivot français (OST 1744 vs LSG 1910)
    contrastes = []
    for pivot_vieux, pivot_moderne, cibles in [
        ("KJV", "WEB", [c for c in noms if c not in ("KJV", "WEB")]),
        ("OST", "LSG", [c for c in noms if c not in ("OST", "LSG")]),
    ]:
        for t in cibles:
            p_vieux = next(p for p in paires if p["a"] == pivot_vieux and p["b"] == t)
            p_moderne = next(p for p in paires if p["a"] == pivot_moderne and p["b"] == t)
            # rangs appariés : on a besoin des rangs, on les recalcule
            A_v, B_v = matrices[pivot_vieux], matrices[t]
            A_m, B_m = matrices[pivot_moderne], matrices[t]
            _, _, _, r_v = top1_et_rangs(A_v, B_v)
            _, _, _, r_m = top1_et_rangs(A_m, B_m)
            ok_v = r_v == 1
            ok_m = r_m == 1
            b = int(np.sum(~ok_v & ok_m))
            c = int(np.sum(ok_v & ~ok_m))
            n_disc = b + c
            if n_disc > 0:
                from scipy.stats import binomtest
                p = float(binomtest(b, n_disc, 0.5).pvalue)
            else:
                p = 1.0
            contrastes.append({
                "pivot_vieux": pivot_vieux, "pivot_moderne": pivot_moderne, "cible": t,
                "delta_annees_pivot": abs(BIBLES[pivot_moderne][5] - BIBLES[pivot_vieux][5]),
                "top1_vieux": p_vieux["top1"], "top1_moderne": p_moderne["top1"],
                "delta_top1": p_moderne["top1"] - p_vieux["top1"],
                "gagne_moderne": b, "gagne_vieux": c, "discordants": n_disc,
                "p_mcnemar": p,
            })
    # 2×2 anglais × français
    def t1(a, b):
        return next(p["top1"] for p in paires if p["a"] == a and p["b"] == b)
    carre = {
        "KJV_OST": t1("KJV", "OST"), "KJV_LSG": t1("KJV", "LSG"),
        "WEB_OST": t1("WEB", "OST"), "WEB_LSG": t1("WEB", "LSG"),
    }
    carre["interaction"] = (carre["WEB_LSG"] - carre["WEB_OST"]) - (carre["KJV_LSG"] - carre["KJV_OST"])
    # régression : top1 ~ |delta années| + script_match + famille_match + langue_match
    X = np.array([[p["delta_annees"] / 100.0, float(p["script_match"]),
                   float(p["famille_match"]), float(p["langue_match"])] for p in paires])
    y = np.array([p["top1"] for p in paires])
    Xd = np.column_stack([np.ones(len(X)), X])
    coef, *_ = np.linalg.lstsq(Xd, y, rcond=None)
    # erreurs-types par bootstrap sur les paires
    rng2 = np.random.RandomState(graine + 7)
    coefs = []
    for _ in range(1000):
        idx = rng2.randint(0, len(y), len(y))
        c, *_ = np.linalg.lstsq(Xd[idx], y[idx], rcond=None)
        coefs.append(c)
    coefs = np.array(coefs)
    regression = {
        "n_paires": len(y),
        "coef": {"constante": float(coef[0]), "delta_annees_par_siecle": float(coef[1]),
                 "script_match": float(coef[2]), "famille_match": float(coef[3]),
                 "langue_match": float(coef[4])},
        "ic95": {nom: [float(np.percentile(coefs[:, i], 2.5)), float(np.percentile(coefs[:, i], 97.5))]
                 for i, nom in enumerate(["constante", "delta_annees_par_siecle", "script_match",
                                          "famille_match", "langue_match"])},
        "r2": float(1.0 - np.sum((y - Xd @ coef) ** 2) / np.sum((y - y.mean()) ** 2)),
    }
    # contrôle de la régression : permuter les années des traductions
    annees = {c: BIBLES[c][5] for c in noms}
    perm_coefs = []
    for _ in range(500):
        vals = list(annees.values())
        rng2.shuffle(vals)
        perm = dict(zip(noms, vals))
        Xp = np.array([[abs(perm[p["a"]] - perm[p["b"]]) / 100.0, float(p["script_match"]),
                        float(p["famille_match"]), float(p["langue_match"])] for p in paires])
        Xpd = np.column_stack([np.ones(len(Xp)), Xp])
        cp, *_ = np.linalg.lstsq(Xpd, y, rcond=None)
        perm_coefs.append(cp[1])
    perm_coefs = np.array(perm_coefs)
    regression["controle_annees_permutees"] = {
        "coef_observe": regression["coef"]["delta_annees_par_siecle"],
        "moyenne_permutee": float(perm_coefs.mean()),
        "p_value_unilaterale_negative": float((np.sum(perm_coefs <= regression["coef"]["delta_annees_par_siecle"]) + 1) / (len(perm_coefs) + 1)),
        "n_permutations": len(perm_coefs),
    }
    controles = {
        "permutation_versets_top1_moyen": float(np.mean([p["controle_permutation"] for p in paires])),
        "chance_moyenne": float(np.mean([p["chance"] for p in paires])),
        "n_versets": len(cles),
    }
    return {
        "n_traductions": len(noms), "n_langues": len({BIBLES[c][2] for c in noms}),
        "n_versets_communs": bible["n_communs"], "n_versets_retenus": bible["n_retenus"],
        "traductions": bible["meta"], "matrice_top1": matrice,
        "agregats": agregats, "contrastes": contrastes, "carre_2x2": carre,
        "regression": regression, "controles": controles, "paires": paires,
    }


# ---------------------------------------------------------------------------
# 4. Sortie
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapide", action="store_true")
    ap.add_argument("--n-versets", type=int, default=1000)
    ap.add_argument("--graine", type=int, default=0)
    ap.add_argument("--sortie", default=str(SORTIE))
    a = ap.parse_args()

    print("B7 — lexique des 71 langues…", flush=True)
    b7 = b7_mesure(charge_b7(), graine=a.graine)
    print(f"  {b7['n_langues']} langues, {len(b7['paires'])} paires ordonnées", flush=True)

    print("UDHR — corpus commun, 21 langues, 30 articles…", flush=True)
    udhr = udhr_mesure(charge_udhr(), graine=a.graine)
    print(f"  {udhr['n_langues']} langues, {len(udhr['paires'])} paires", flush=True)

    print("BIBLE — 12 traductions datées…", flush=True)
    bible = bible_mesure(charge_bible(n_versets=a.n_versets, graine=a.graine, rapide=a.rapide),
                         graine=a.graine, rapide=a.rapide)
    print(f"  {bible['n_versets_retenus']} versets, {len(bible['paires'])} paires", flush=True)

    resultat = {
        "tache": "J3.1",
        "titre": "le retrieval inter-langues à époque contrôlée",
        "date": "2026-11-07",
        "methode": {
            "retrieval": "n-grammes de caractères n=3, TF-IDF (idf lissé, tf sous-linéaire), cosinus, top-1",
            "chance": "1 / nombre de candidats",
            "controle_negatif": "candidats mélangés ; libellés permutés (B7) ; années permutées (Bible)",
            "graine": a.graine,
            "n_versets_bible": a.n_versets,
        },
        "b7": b7,
        "udhr": udhr,
        "bible": bible,
    }
    sortie = pathlib.Path(a.sortie)
    # --rapide ne doit pas écraser le résultat complet versionné
    if a.rapide and sortie.resolve() == SORTIE.resolve():
        sortie = RACINE / "work" / "retrieval-epoque-rapide.json"
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ {sortie}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
