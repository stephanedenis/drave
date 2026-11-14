#!/usr/bin/env python3
"""retrieval_familles.py — J7.1 : le retrieval approfondi par famille Glottolog.

LA QUESTION. J3.1 a mesuré le retrieval de surface sur 21 langues UDHR (30 articles, 1948) :
top-1 0,049, écriture +0,062, famille +0,056, R² 0,14. J3.2 a montré que, sur ces 21 langues,
le signal de famille vit dans 2-3 paires et que les paires hors écriture sont exactement au hasard.
J7.1 demande d'aller plus loin : utiliser les **532 langues UDHR de Panini** (même source XML,
article 1), mesurer le retrieval **par famille Glottolog** sur les **29 langues de
`language_genealogy.py`** et sur l'**échantillon 20** du corpus commun, avec le **contrôle
d'époque**, et comparer à J3.1.

LE DISPOSITIF, EN DEUX TEMPS.
  1. **Global 532** (article 1, 1948) : chaque langue est une requête ; on classe les 440 autres
     langues (une par code ISO, les variantes d'une même langue sont dédupliquées) par similarité
     de surface. On regarde si le top-1 est de la même famille, de la même branche (sœur), ou d'une
     autre famille. C'est un retrieval de **voisinage généalogique**, pas un retrieval parallèle.
  2. **Parallèle 30 articles** (les 29 langues de LANG_TREE + l'échantillon 20) : pour chaque paire
     (A,B), on retrouve l'article i de B parmi les 30 articles de B. C'est exactement la mesure de
     J3.1, appliquée à deux jeux de langues choisis pour leur généalogie. On reproduit aussi J3.1
     à l'identique sur ses 21 langues (contrôle de mise en œuvre).

CE QUI EST MESURÉ. N-grammes de caractères (n=3), TF-IDF, cosinus, top-1 et MRR — les mêmes
fonctions que `retrieval_epoque.py` (J3.1), importées pour que la comparaison soit exacte.
« Sœur » = même famille Glottolog **et** LCA de profondeur ≥ 3, en excluant les couples
ancêtre/descendant (un chemin est préfixe de l'autre). « Famille, autre branche » = même famille
mais LCA < 3. « Famille différente » = famille différente. Les isolats sont des familles d'un seul
élément. On rapporte aussi une définition stricte (LCA ≥ 4).

CONTRÔLES NÉGATIFS.
  (a) **Familles différentes vs sœurs** : le contraste demandé, avec IC bootstrap et test de
      permutation des étiquettes de famille/chemin ; les sœurs doivent dominer les familles
      différentes, et l'écart doit disparaître quand on permute.
  (b) **Étiquettes de famille permutées** (1 000) : les taux de top-1 famille/sœur doivent
      retomber au hasard.
  (c) **Requêtes permutées** (200) : remplacer le texte de la requête par celui d'une autre langue
      doit ramener le top-1 famille au hasard.
  (d) **Candidats mélangés** (J3.1) : une permutation sans point fixe des articles de B doit
      ramener le top-1 au hasard (1/30).
  (e) **Époque** : l'UDHR est mono-époque (1948) ; le contrôle est un placebo de dates aléatoires
      (le coefficient de date doit être nul) et le rappel du bras Bible de J3.1, où la date varie
      (−0,034/siècle, p = 0,19). L'époque ne peut donc pas expliquer un effet de famille ici.

SORTIE. `reports/retrieval-familles.json` (versionné), plus un résumé sur stdout.
Aucune écriture dans Panini : les sources sont lues en lecture seule, avec SHA-256.

Usage :
  python3 tools/retrieval_familles.py
  python3 tools/retrieval_familles.py --rapide          # permutations réduites
  python3 tools/retrieval_familles.py --sortie /tmp/j71.json
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import pathlib
import random
import re
import subprocess
import sys

import numpy as np
from scipy import stats

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "tools"))
from retrieval_epoque import (  # noqa: E402  (import après le path)
    derangement,
    normalise,
    regression_surface,
    tfidf,
    top1_et_rangs,
)

SORTIE = RACINE / "reports" / "retrieval-familles.json"
PANINI_CORPUS = RACINE.parent / "Panini" / "research" / "data" / "udhr_corpus.json"
PANINI_LANG_TREE = RACINE.parent / "Panini" / "research" / "src" / "nipada" / "signing" / "language_genealogy.py"
ARTICLES = RACINE / "data" / "udhr" / "articles_propres.jsonl"
GENEALOGIE = RACINE / "data" / "udhr" / "genealogie.json"
META = RACINE / "data" / "udhr" / "meta.json"
LANGUES = RACINE / "data" / "udhr" / "langues.jsonl"
GLOTTOLOG_LANGS = RACINE / "data" / "glottolog" / "languages.csv"
GLOTTOLOG_VALUES = RACINE / "data" / "glottolog" / "values.csv"
J31_JSON = RACINE / "reports" / "retrieval-epoque.json"
CORPUS_COMMUN = RACINE / "reports" / "corpus-commun.json"

# Les 29 langues de `language_genealogy.py` (LANG_TREE) → la clé Panini correspondante.
# Les absentes de l'UDHR (grec ancien, pali, chinois littéraire) sont None et comptées.
LANG_TREE_VERS_PANINI = {
    "eng": "eng", "deu": "deu_1996", "nld": "nld", "swe": "swe", "nor": "nob",
    "dan": "dan", "fin": "fin", "hun": "hun",
    "fra": "fra", "ita": "ita", "spa": "spa", "por": "por_PT", "ron": "ron_2006",
    "lat": "lat", "grc": None, "ell": "ell_monotonic", "san": "san", "pli": None,
    "hin": "hin", "ben": "ben", "per": "pes_1", "fas": "pes_1",
    "ara": "arb", "heb": "heb", "lzh": None, "zho": "cmn_hant",
    "jpn": "jpn", "kor": "kor", "tur": "tur",
}
# Le choix `nor -> nob` et `zho -> cmn_hant` est explicite : ce sont les variantes UDHR
# disponibles. `per` et `fas` pointent vers le même texte (`pes_1`), dédupliqué ensuite.

# Quelques variantes ISO/UDHR dont le code n'est pas l'ISO 639-3 : on les apparie par
# préfixe ou par nom quand c'est non ambigu. Le reste est laissé « inconnu » et compté.
ALIAS_ISO = {
    "fuv2": "fuv", "gsw1": "gsw", "hau_3": "hau", "ven2": "ven",
    "mal_chillus": "mal", "khk_mong": "khk", "tzm_tfng": "tzm",
    "tgl_tglg": "tgl", "jpn_osaka": "jpn", "jpn_tokyo": "jpn",
    "cmn_hans_beijing": "cmn", "cmn_hans_guiyang": "cmn",
    "cmn_hans_harbin": "cmn", "cmn_hans_nanjing": "cmn",
    "cmn_hans_tianjin": "cmn",
}
# Noms UDHR numériques dont l'ISO est connu sans ambiguïté dans Glottolog. On ne les
# invente pas : on vérifie que le code existe dans `languages.csv`.
ALIAS_NOM = {
    "030": "mkw", "041": "lav", "042": "spa", "043": "dje", "045": "mas",
    "046": "pmy", "047": "abs", "048": "min", "050": "btk", "053": "hau",
    "054": "cat", "058": "som", "059": "sme", "063": "swh",
    "067": "fin", "068": "fra", "069": "mri", "072": "oci",
}


# ---------------------------------------------------------------------------
# 0. Outils
# ---------------------------------------------------------------------------

def sha256(chemin: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def lire_json(chemin: pathlib.Path):
    return json.loads(chemin.read_text(encoding="utf-8"))


def commit(chemin: pathlib.Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(chemin), "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return None


def moyenne(valeurs) -> float | None:
    return float(np.mean(valeurs)) if len(valeurs) else None


def ic95(valeurs) -> list[float] | None:
    if not len(valeurs):
        return None
    return [float(np.percentile(valeurs, 2.5)), float(np.percentile(valeurs, 97.5))]


# ---------------------------------------------------------------------------
# 1. Glottolog — la famille et le chemin
# ---------------------------------------------------------------------------

class Glottolog:
    def __init__(self, langs_csv: pathlib.Path, values_csv: pathlib.Path):
        self.noms: dict[str, str] = {}
        self.par_iso: dict[str, list[dict]] = collections.defaultdict(list)
        self.par_nom: dict[str, list[dict]] = collections.defaultdict(list)
        for r in csv.DictReader(langs_csv.open(encoding="utf-8")):
            self.noms[r["ID"]] = r.get("Name") or r["ID"]
            iso = (r.get("ISO639P3code") or "").strip().lower()
            if iso:
                self.par_iso[iso].append(r)
            self.par_nom[(r.get("Name") or "").strip().lower()].append(r)
        self.classif: dict[str, str] = {}
        for r in csv.DictReader(values_csv.open(encoding="utf-8")):
            if r.get("Parameter_ID") == "classification":
                self.classif[r["Language_ID"]] = r.get("Value") or ""

    def chemin_codes(self, r: dict) -> list[str]:
        c = self.classif.get(r["ID"], "")
        if c:
            return [x for x in c.split("/") if x]
        fam = r.get("Family_ID") or ""
        return [fam] if fam else []

    def chemin_noms(self, codes: list[str]) -> list[str]:
        return [self.noms.get(x, x) for x in codes]

    def meta_iso(self, iso: str) -> dict | None:
        rs = self.par_iso.get(iso.lower())
        if not rs:
            return None
        # Un code ISO peut couvrir plusieurs languoïdes : on préfère le niveau « language ».
        rs = sorted(rs, key=lambda r: (r.get("Level") != "language", r["ID"]))
        r = rs[0]
        codes = self.chemin_codes(r)
        chemin = self.chemin_noms(codes)
        famille = chemin[0] if chemin else (self.noms.get(r.get("Family_ID", ""), r.get("Family_ID", "")) or "")
        return {"source": "glottolog", "iso3": r.get("ISO639P3code") or iso,
                "famille": famille, "chemin": chemin, "codes": codes,
                "glottocode": r.get("Glottocode") or r["ID"]}


# ---------------------------------------------------------------------------
# 2. Métadonnées — Drave d'abord, Glottolog ensuite
# ---------------------------------------------------------------------------

def construire_meta(panini: dict, glotto: Glottolog, genealogie: dict) -> tuple[dict, dict]:
    meta: dict[str, dict] = {}
    inconnus: list[dict] = []
    for cle, v in panini.items():
        m = None
        # 2.1 Drave (même source XML, 441 fichiers, chemins de glottocodes)
        g = genealogie.get(f"udhr_{cle}.xml")
        if g and g.get("famille") not in (None, "", "(inconnue)"):
            codes = [x for x in (g.get("branche") or "").split("/") if x]
            chemin = glotto.chemin_noms(codes)
            if not chemin:
                chemin = [g["famille"]]
            m = {"source": "drave", "iso3": g.get("iso3") or v.get("iso"),
                 "famille": chemin[0], "chemin": chemin, "codes": codes,
                 "glottocode": codes[-1] if codes else ""}
        # 2.2 ISO direct, alias, préfixe, chiffres finaux
        if m is None:
            iso = str(v.get("iso") or "").strip()
            candidats = [ALIAS_ISO.get(cle), ALIAS_NOM.get(cle), iso,
                         iso.split("_")[0], re.sub(r"\d+$", "", iso)]
            for c in candidats:
                if not c or str(c).isdigit():
                    continue
                m = glotto.meta_iso(str(c))
                if m:
                    break
        # 2.3 nom exact, seulement s'il est unique
        if m is None:
            rs = glotto.par_nom.get((v.get("name") or "").strip().lower(), [])
            if len(rs) == 1:
                r = rs[0]
                codes = glotto.chemin_codes(r)
                chemin = glotto.chemin_noms(codes)
                if not chemin:
                    chemin = [glotto.noms.get(r.get("Family_ID", ""), r.get("Family_ID", "")) or ""]
                m = {"source": "nom", "iso3": r.get("ISO639P3code") or v.get("iso"),
                     "famille": chemin[0], "chemin": chemin, "codes": codes,
                     "glottocode": r.get("Glottocode") or r["ID"]}
        if m is None:
            inconnus.append({"cle": cle, "iso": v.get("iso"), "nom": v.get("name")})
            continue
        # Isolat ou famille vide : famille d'un seul élément, pour ne pas fabriquer de sœurs.
        if not m.get("famille"):
            m["famille"] = f"Isolate:{cle}"
            m["chemin"] = [m["famille"]]
        m.update({"cle": cle, "script": v.get("script") or "", "nom_panini": v.get("name") or "",
                  "famille_panini": v.get("family") or ""})
        meta[cle] = m
    return meta, {"n_inconnus": len(inconnus), "inconnus": inconnus}


# ---------------------------------------------------------------------------
# 3. Relations de parenté
# ---------------------------------------------------------------------------

def relation(meta: dict, a: str, b: str) -> dict:
    pa = meta[a].get("chemin") or ["?"]
    pb = meta[b].get("chemin") or ["?"]
    d = 0
    for x, y in zip(pa, pb):
        if x == y:
            d += 1
        else:
            break
    ancetre = pa == pb[:len(pa)] or pb == pa[:len(pb)]
    meme_famille = pa[0] == pb[0]
    soeur = bool(meme_famille and d >= 3 and not ancetre)
    soeur_stricte = bool(meme_famille and d >= 4 and not ancetre)
    famille_autre = bool(meme_famille and not soeur)
    return {"lca": int(d), "ancetre_descendant": bool(ancetre),
            "meme_famille": bool(meme_famille), "soeur": soeur,
            "soeur_stricte": soeur_stricte, "famille_autre_branche": famille_autre,
            "famille_differente": bool(not meme_famille)}


def relation_chemins(pa: list[str], pb: list[str]) -> dict:
    d = 0
    for x, y in zip(pa, pb):
        if x == y:
            d += 1
        else:
            break
    ancetre = pa == pb[:len(pa)] or pb == pa[:len(pb)]
    meme = pa[0] == pb[0]
    soeur = bool(meme and d >= 3 and not ancetre)
    return {"lca": d, "ancetre_descendant": ancetre, "meme_famille": meme,
            "soeur": soeur, "soeur_stricte": bool(meme and d >= 4 and not ancetre),
            "famille_autre_branche": bool(meme and not soeur),
            "famille_differente": bool(not meme)}


# ---------------------------------------------------------------------------
# 4. Ensembles de langues
# ---------------------------------------------------------------------------

def construire_ensembles(meta: dict, panini: dict) -> dict:
    # 4.1 Les 29 de LANG_TREE, avec la table de correspondance explicite.
    lang_tree = {}
    for code, cle in LANG_TREE_VERS_PANINI.items():
        if cle and cle in meta:
            lang_tree[code] = cle
    # 4.2 L'échantillon 20 du corpus commun (les 20 strates, sans le pivot français).
    corpus = lire_json(CORPUS_COMMUN)
    echantillon = [t["id"].replace("udhr_", "") for t in corpus["textes"]
                   if t.get("role") == "strate"]
    echantillon = [k for k in echantillon if k in meta]
    # 4.3 Les 21 de J3.1 (20 strates + fra) pour la reproduction exacte.
    j31 = [k.replace("udhr_", "") for k in lire_json(J31_JSON)["udhr"]["meta_langues"]]
    j31 = [k for k in j31 if k in meta]
    # 4.4 L'union (sans doublon de texte).
    union = sorted(set(lang_tree.values()) | set(echantillon))
    # 4.5 Les textes Panini non dédupliqués : un représentant par code ISO.
    langid = {k: (m.get("iso3") or k) for k, m in meta.items()}
    groupes = collections.defaultdict(list)
    for k in panini:
        if k in meta:
            groupes[langid[k]].append(k)
    preferes = set(union) | set(j31)
    def choisir(v: list[str]) -> str:
        for k in v:
            if k in preferes:
                return k
        for k in v:
            if "_" not in k:
                return k
        return sorted(v)[0]
    representants_iso = {g: choisir(v) for g, v in groupes.items()}
    # 4.6 Déduplication par texte exact : 12 groupes de textes identiques dans les 532,
    # dont 3 seulement changent de code ISO (kng/ktu, ckb/kmr, bos_latn/hrv). Sans cela,
    # deux textes identiques fabriquent un top-1 « famille » trivial.
    par_texte = collections.defaultdict(list)
    for g, rep in representants_iso.items():
        par_texte[normalise(panini[rep]["text"])].append((g, rep))
    representants = []
    doublons_texte = []
    for items in par_texte.values():
        items = sorted(items, key=lambda gr: (gr[1] not in preferes, len(gr[1]), gr[1]))
        garde = items[0][1]
        representants.append(garde)
        for g, rep in items[1:]:
            doublons_texte.append({"garde": garde, "retire": rep, "groupe_iso": g})
    representants.sort()
    return {
        "lang_tree": lang_tree,
        "echantillon_20": echantillon,
        "j31_21": j31,
        "union": union,
        "representants": representants,
        "groupes": {g: v for g, v in groupes.items()},
        "n_groupes": len(representants),
        "n_groupes_iso": len(groupes),
        "n_textes_labelises": sum(len(v) for v in groupes.values()),
        "doublons_texte": doublons_texte,
    }


# ---------------------------------------------------------------------------
# 5. Mesure globale — les 532 textes, article 1
# ---------------------------------------------------------------------------

def mesure_globale(meta: dict, panini: dict, cles: list[str], graine: int = 0,
                   permutations: int = 1000) -> dict:
    cles = sorted(cles)
    n = len(cles)
    docs = [panini[k]["text"] for k in cles]
    M, _, _ = tfidf(docs, n=3)
    S = (M @ M.T).toarray()
    np.fill_diagonal(S, -np.inf)
    ordre = np.argsort(-S, axis=1)
    scripts = [meta[k].get("script") or panini[k].get("script") or "" for k in cles]
    familles = [meta[k].get("famille") or f"Isolate:{k}" for k in cles]
    chemins = [meta[k].get("chemin") or ["?"] for k in cles]
    # relations précalculées
    rel = [[relation_chemins(chemins[i], chemins[j]) for j in range(n)] for i in range(n)]
    def metriques_pool(i: int, o: list[int]) -> dict | None:
        """Les métriques d'une requête sur un pool ordonné de candidats (sans soi-même)."""
        if not o:
            return None
        top = o[0]
        memes = [j for j in o if rel[i][j]["meme_famille"]]
        soeurs = [j for j in o if rel[i][j]["soeur"]]
        r_fam = next((r + 1 for r, j in enumerate(o) if rel[i][j]["meme_famille"]), 0)
        hits = 0
        ap = 0.0
        for r, j in enumerate(o):
            if rel[i][j]["meme_famille"]:
                hits += 1
                ap += hits / (r + 1)
        ap = ap / len(memes) if memes else 0.0
        return {
            "top1": cles[top], "top1_famille": bool(rel[i][top]["meme_famille"]),
            "top1_soeur": bool(rel[i][top]["soeur"]),
            "top1_soeur_stricte": bool(rel[i][top]["soeur_stricte"]),
            "top1_famille_autre": bool(rel[i][top]["famille_autre_branche"]),
            "top1_famille_differente": bool(rel[i][top]["famille_differente"]),
            "top1_script": bool(scripts[top] == scripts[i]),
            "p_famille": len(memes) / len(o),
            "p_soeur": len(soeurs) / len(o),
            "p_script": sum(1 for j in o if scripts[j] == scripts[i]) / len(o),
            "mrr_famille": 1.0 / r_fam if r_fam else 0.0,
            "ap_famille": ap,
            "top5_famille": float(np.mean([rel[i][j]["meme_famille"] for j in o[:5]])),
            "n_candidats": len(o),
        }

    lignes = []
    for i, cle in enumerate(cles):
        o_all = [j for j in ordre[i] if j != i]
        o_ss = [j for j in o_all if scripts[j] == scripts[i]]
        o_ds = [j for j in o_all if scripts[j] != scripts[i]]
        lignes.append({
            "cle": cle, "famille": familles[i], "script": scripts[i],
            "all": metriques_pool(i, o_all),
            "ss": metriques_pool(i, o_ss),
            "ds": metriques_pool(i, o_ds),
        })

    def agreger(pool: str, filtre=lambda x: True) -> dict:
        v = [x[pool] for x in lignes if filtre(x) and x[pool] is not None]
        if not v:
            return {"n_requetes": 0}
        return {
            "n_requetes": len(v),
            "top1_famille": moyenne([x["top1_famille"] for x in v]),
            "p_famille": moyenne([x["p_famille"] for x in v]),
            "top1_soeur": moyenne([x["top1_soeur"] for x in v]),
            "p_soeur": moyenne([x["p_soeur"] for x in v]),
            "top1_soeur_stricte": moyenne([x["top1_soeur_stricte"] for x in v]),
            "top1_famille_autre": moyenne([x["top1_famille_autre"] for x in v]),
            "top1_famille_differente": moyenne([x["top1_famille_differente"] for x in v]),
            "top1_script": moyenne([x["top1_script"] for x in v]),
            "p_script": moyenne([x["p_script"] for x in v]),
            "mrr_famille": moyenne([x["mrr_famille"] for x in v]),
            "ap_famille": moyenne([x["ap_famille"] for x in v]),
            "top5_famille": moyenne([x["top5_famille"] for x in v]),
        }

    agregats = {
        "toutes": agreger("all"),
        "script_meme": agreger("ss"),
        "script_different": agreger("ds"),
    }
    # par famille (≥ 3 requêtes)
    par_famille = {}
    for f in sorted({x["famille"] for x in lignes}):
        v = [x for x in lignes if x["famille"] == f]
        if len(v) >= 3:
            par_famille[f] = agreger("all", lambda x, f=f: x["famille"] == f)
    # par écriture (≥ 3 requêtes)
    par_script = {}
    for s in sorted({x["script"] for x in lignes}):
        v = [x for x in lignes if x["script"] == s]
        if len(v) >= 3:
            par_script[s] = agreger("all", lambda x, s=s: x["script"] == s)
    # paires les plus similaires (hors diagonale)
    paires = []
    for i in range(n):
        for j in range(i + 1, n):
            paires.append((float(S[i, j]), cles[i], cles[j], familles[i], familles[j],
                           rel[i][j]["soeur"], rel[i][j]["famille_autre_branche"]))
    paires.sort(key=lambda x: -x[0])
    top_paires = [{"similarite": p[0], "a": p[1], "b": p[2], "famille_a": p[3],
                   "famille_b": p[4], "soeur": p[5], "famille_autre": p[6]}
                  for p in paires[:20]]

    # ---- contrôle (b) : permutation des étiquettes de famille/chemin -------------
    rng = np.random.RandomState(graine + 101)
    top1_idx = np.array([int(ordre[i][0]) for i in range(n)])
    obs_fam = float(np.mean([rel[i][top1_idx[i]]["meme_famille"] for i in range(n)]))
    obs_soeur = float(np.mean([rel[i][top1_idx[i]]["soeur"] for i in range(n)]))
    null_fam, null_soeur = [], []
    for _ in range(permutations):
        perm = rng.permutation(n)
        fam_p = [familles[i] for i in perm]
        chem_p = [chemins[i] for i in perm]
        nf = float(np.mean([fam_p[top1_idx[i]] == fam_p[i] for i in range(n)]))
        ns = float(np.mean([relation_chemins(chem_p[i], chem_p[top1_idx[i]])["soeur"]
                            for i in range(n)]))
        null_fam.append(nf)
        null_soeur.append(ns)
    p_fam = (1 + sum(1 for x in null_fam if x >= obs_fam)) / (permutations + 1)
    p_soeur = (1 + sum(1 for x in null_soeur if x >= obs_soeur)) / (permutations + 1)
    permutation = {
        "n_permutations": permutations,
        "observe_famille": obs_fam, "nul_famille_moyen": float(np.mean(null_fam)),
        "nul_famille_ic95": ic95(null_fam), "p_famille": p_fam,
        "observe_soeur": obs_soeur, "nul_soeur_moyen": float(np.mean(null_soeur)),
        "nul_soeur_ic95": ic95(null_soeur), "p_soeur": p_soeur,
    }

    # ---- contrôle (c) : requêtes permutées (textes échangés) --------------------
    rng2 = random.Random(graine + 202)
    ctrl_fam = []
    for _ in range(200):
        perm = derangement(n, rng2)
        vals = []
        for i in range(n):
            row = perm[i]
            o = [j for j in ordre[row] if j != i]
            top = o[0]
            vals.append(rel[i][top]["meme_famille"])
        ctrl_fam.append(float(np.mean(vals)))
    requetes_permutees = {
        "n_permutations": 200,
        "top1_famille_moyen": float(np.mean(ctrl_fam)),
        "ic95": ic95(ctrl_fam),
        "baseline_famille": agregats["toutes"]["p_famille"],
        "top1_famille_observe": obs_fam,
    }

    return {
        "n_requetes": n,
        "n_candidats": n - 1,
        "agregats": agregats,
        "par_famille": par_famille,
        "par_script": par_script,
        "top_paires": top_paires,
        "controles": {"permutation_etiquettes": permutation,
                      "requetes_permutees": requetes_permutees},
        "lignes": lignes,
    }


# ---------------------------------------------------------------------------
# 6. Mesure parallèle — 30 articles, paires ordonnées
# ---------------------------------------------------------------------------

def charger_articles() -> dict[str, dict[int, str]]:
    arts: dict[str, dict[int, str]] = collections.defaultdict(dict)
    for ligne in ARTICLES.read_text(encoding="utf-8").splitlines():
        x = json.loads(ligne)
        arts[x["fichier"]][int(x["art"])] = x["texte"]
    return dict(arts)


def docs_langue(articles: dict, cle: str) -> list[str]:
    f = f"udhr_{cle}.xml"
    return [articles[f][a] for a in sorted(articles[f])]


def _ols_sans_chance(paires: list[dict], variables: list[str]) -> dict:
    X = np.array([[float(p[v]) for v in variables] for p in paires], dtype=float)
    y = np.array([p["top1"] for p in paires], dtype=float)
    Xd = np.column_stack([np.ones(len(X)), X])
    coef, *_ = np.linalg.lstsq(Xd, y, rcond=None)
    pred = Xd @ coef
    ssr = float(((y - pred) ** 2).sum())
    sst = float(((y - y.mean()) ** 2).sum())
    return {"coef": {"constante": float(coef[0]), **{v: float(coef[i + 1]) for i, v in enumerate(variables)}},
            "r2": float(1.0 - ssr / sst) if sst else 0.0}


def mesure_paire(meta: dict, articles: dict, cles: list[str], graine: int = 0,
                 permutations: int = 500) -> dict:
    cles = sorted(set(k for k in cles if k in meta and f"udhr_{k}.xml" in articles))
    docs = [t for k in cles for t in docs_langue(articles, k)]
    M, _, _ = tfidf(docs, n=3)
    mats = {}
    pos = 0
    for k in cles:
        n = len(docs_langue(articles, k))
        mats[k] = M[pos:pos + n]
        pos += n
    rng = random.Random(graine + 303)
    paires = []
    for a in cles:
        for b in cles:
            if a == b:
                continue
            A, B = mats[a], mats[b]
            t1, mrr, rk, rangs = top1_et_rangs(A, B)
            S = (A @ B.T).toarray()
            pred = np.argmax(S, axis=1)
            perm = derangement(A.shape[0], rng)
            t1p = float((pred == perm).mean())
            r = relation(meta, a, b)
            paires.append({
                "a": a, "b": b,
                "script_a": meta[a].get("script"), "script_b": meta[b].get("script"),
                "famille_a": meta[a]["famille"], "famille_b": meta[b]["famille"],
                "script_match": meta[a].get("script") == meta[b].get("script"),
                "famille_match": r["meme_famille"],
                "soeur": r["soeur"], "soeur_stricte": r["soeur_stricte"],
                "famille_autre_branche": r["famille_autre_branche"],
                "famille_differente": r["famille_differente"],
                "lca": r["lca"], "ancetre_descendant": r["ancetre_descendant"],
                "n_requetes": int(A.shape[0]), "n_candidats": int(B.shape[0]),
                "top1": float(t1), "mrr": float(mrr), "rang_median": float(rk),
                "chance": 1.0 / B.shape[0], "controle_permutation": t1p,
                "epoque_a": 1948, "epoque_b": 1948,
            })

    def agreger(filtre=lambda p: True) -> dict:
        v = [p for p in paires if filtre(p)]
        return {
            "n_paires": len(v),
            "top1_moyen": moyenne([p["top1"] for p in v]),
            "top1_median": float(np.median([p["top1"] for p in v])) if v else None,
            "ic_bas": float(np.percentile([p["top1"] for p in v], 2.5)) if v else None,
            "ic_haut": float(np.percentile([p["top1"] for p in v], 97.5)) if v else None,
            "mrr_moyen": moyenne([p["mrr"] for p in v]),
        }

    agregats = {
        "toutes": agreger(),
        "script_meme": agreger(lambda p: p["script_match"]),
        "script_different": agreger(lambda p: not p["script_match"]),
        "famille_meme": agreger(lambda p: p["famille_match"]),
        "famille_differente": agreger(lambda p: p["famille_differente"]),
        "soeur": agreger(lambda p: p["soeur"]),
        "soeur_stricte": agreger(lambda p: p["soeur_stricte"]),
        "famille_autre_branche": agreger(lambda p: p["famille_autre_branche"]),
        "script_meme_soeur": agreger(lambda p: p["script_match"] and p["soeur"]),
        "script_meme_famille_autre": agreger(lambda p: p["script_match"] and p["famille_autre_branche"]),
        "script_meme_famille_differente": agreger(lambda p: p["script_match"] and p["famille_differente"]),
        "script_different_soeur": agreger(lambda p: not p["script_match"] and p["soeur"]),
        "script_different_famille_meme": agreger(lambda p: not p["script_match"] and p["famille_match"]),
        "script_different_famille_differente": agreger(lambda p: not p["script_match"] and p["famille_differente"]),
    }

    # régressions : A = J3.1 exact (avec `chance`, constante 1/30) ; B/C = décomposition
    reg_a = regression_surface(paires, ["script_match", "famille_match", "chance"], graine=graine)
    reg_b = _ols_sans_chance(paires, ["script_match", "soeur", "famille_autre_branche"])
    reg_c = _ols_sans_chance(paires, ["script_match", "soeur_stricte", "famille_autre_branche"])

    # permutation des étiquettes (famille/chemin) pour les coefficients B et C
    idx_paires = [(cles.index(p["a"]), cles.index(p["b"])) for p in paires]
    chemins = [meta[k].get("chemin") or ["?"] for k in cles]
    rng2 = np.random.RandomState(graine + 404)
    null_soeur, null_fam_autre, null_fam_match = [], [], []
    for _ in range(permutations):
        perm = rng2.permutation(len(cles))
        chem_p = [chemins[i] for i in perm]
        for p, (ia, ib) in zip(paires, idx_paires):
            r = relation_chemins(chem_p[ia], chem_p[ib])
            p["_soeur_p"] = r["soeur"]
            p["_fam_autre_p"] = r["famille_autre_branche"]
            p["_fam_match_p"] = r["meme_famille"]
        rb = _ols_sans_chance(paires, ["script_match", "_soeur_p", "_fam_autre_p"])
        ra = _ols_sans_chance(paires, ["script_match", "_fam_match_p"])
        null_soeur.append(rb["coef"]["_soeur_p"])
        null_fam_autre.append(rb["coef"]["_fam_autre_p"])
        null_fam_match.append(ra["coef"]["_fam_match_p"])
    # nettoyer les colonnes temporaires
    for p in paires:
        for k in ("_soeur_p", "_fam_autre_p", "_fam_match_p"):
            p.pop(k, None)
    p_soeur = (1 + sum(1 for x in null_soeur if x >= reg_b["coef"]["soeur"])) / (permutations + 1)
    p_fam_autre = (1 + sum(1 for x in null_fam_autre if x >= reg_b["coef"]["famille_autre_branche"])) / (permutations + 1)
    p_fam_match = (1 + sum(1 for x in null_fam_match if x >= reg_a["coef"]["famille_match"])) / (permutations + 1)
    reg_b["controle_permutation"] = {
        "n_permutations": permutations,
        "p_soeur": p_soeur,
        "p_famille_autre": p_fam_autre,
        "null_soeur_moyen": float(np.mean(null_soeur)),
        "null_soeur_ic95": ic95(null_soeur),
        "null_famille_autre_moyen": float(np.mean(null_fam_autre)),
    }
    reg_a["controle_permutation"] = {
        "n_permutations": permutations,
        "p_famille_match": p_fam_match,
        "null_famille_match_moyen": float(np.mean(null_fam_match)),
        "null_famille_match_ic95": ic95(null_fam_match),
    }

    # leave-one-language-out sur le modèle B
    loo = []
    for k in cles:
        sous = [p for p in paires if p["a"] != k and p["b"] != k]
        if len(sous) < 20:
            continue
        r = _ols_sans_chance(sous, ["script_match", "soeur", "famille_autre_branche"])
        loo.append({"retire": k, **r["coef"], "r2": r["r2"]})
    loo_resume = {}
    for var in ("script_match", "soeur", "famille_autre_branche"):
        vals = [x[var] for x in loo]
        if vals:
            loo_resume[var] = {"min": float(min(vals)), "median": float(np.median(vals)),
                               "max": float(max(vals))}

    # contraste demandé : sœurs vs familles différentes
    soeurs = [p["top1"] for p in paires if p["soeur"]]
    diff = [p["top1"] for p in paires if p["famille_differente"]]
    diff_s = [p["top1"] for p in paires if p["soeur"] and p["script_match"]]
    diff_d = [p["top1"] for p in paires if p["famille_differente"] and p["script_match"]]
    def delta_ic(a, b, B=1000, graine=0):
        if not a or not b:
            return None
        rng3 = np.random.RandomState(graine + 505)
        vals = []
        for _ in range(B):
            va = rng3.choice(a, len(a), replace=True)
            vb = rng3.choice(b, len(b), replace=True)
            vals.append(float(np.mean(va) - np.mean(vb)))
        return {"delta": float(np.mean(a) - np.mean(b)), "ic95": ic95(vals),
                "n_soeurs": len(a), "n_differentes": len(b)}
    contraste = {
        "toutes": delta_ic(soeurs, diff, graine=graine),
        "script_meme": delta_ic(diff_s, diff_d, graine=graine),
        "ratio_toutes": (float(np.mean(soeurs) / np.mean(diff))) if soeurs and diff and np.mean(diff) else None,
        "ratio_script_meme": (float(np.mean(diff_s) / np.mean(diff_d))) if diff_s and diff_d and np.mean(diff_d) else None,
    }
    # contraste apparié par langue A (même script, au moins une sœur et une différente)
    apparies = []
    for a in cles:
        sa = [p["top1"] for p in paires if p["a"] == a and p["soeur"] and p["script_match"]]
        da = [p["top1"] for p in paires if p["a"] == a and p["famille_differente"] and p["script_match"]]
        if sa and da:
            apparies.append({"a": a, "soeur": float(np.mean(sa)), "differentes": float(np.mean(da)),
                             "delta": float(np.mean(sa) - np.mean(da))})
    if apparies:
        deltas = [x["delta"] for x in apparies]
        pos = sum(1 for x in deltas if x > 0)
        try:
            p_sign = float(stats.binomtest(pos, len(deltas), 0.5).pvalue)
        except Exception:
            p_sign = None
        try:
            p_wil = float(stats.wilcoxon(deltas).pvalue)
        except Exception:
            p_wil = None
        contraste["apparie_par_langue"] = {
            "n_langues": len(apparies),
            "delta_moyen": float(np.mean(deltas)),
            "positives": pos,
            "p_signe": p_sign,
            "p_wilcoxon": p_wil,
            "detail": apparies,
        }
    else:
        contraste["apparie_par_langue"] = {"n_langues": 0}

    # contrôle (d) : candidats mélangés (déjà par paire) et moyenne
    controle_perm = {
        "top1_permute_moyen": moyenne([p["controle_permutation"] for p in paires]),
        "chance_moyenne": moyenne([p["chance"] for p in paires]),
    }

    # exemples : meilleures sœurs, meilleures familles différentes
    soeurs_p = sorted([p for p in paires if p["soeur"]], key=lambda p: -p["top1"])[:12]
    diff_p = sorted([p for p in paires if p["famille_differente"]], key=lambda p: -p["top1"])[:8]
    exemples = {
        "meilleures_soeurs": [{"a": p["a"], "b": p["b"], "top1": p["top1"], "mrr": p["mrr"],
                               "lca": p["lca"], "famille": p["famille_a"]} for p in soeurs_p],
        "meilleures_familles_differentes": [{"a": p["a"], "b": p["b"], "top1": p["top1"],
                                             "famille_a": p["famille_a"], "famille_b": p["famille_b"]}
                                            for p in diff_p],
    }

    return {
        "n_langues": len(cles),
        "langues": cles,
        "n_paires": len(paires),
        "epoque": 1948,
        "agregats": agregats,
        "regressions": {"j31_compatible": reg_a, "decomposition": reg_b,
                        "decomposition_stricte": reg_c},
        "leave_one_language_out": {"n_retraits": len(loo), "resume": loo_resume, "detail": loo},
        "contraste_soeurs": contraste,
        "controle_candidats_melanges": controle_perm,
        "exemples": exemples,
        "paires": paires,
    }


# ---------------------------------------------------------------------------
# 7. Reproduction de J3.1 — contrôle de mise en œuvre
# ---------------------------------------------------------------------------

def verifier_j31(mesure: dict, j31_json: dict) -> dict:
    j = j31_json["udhr"]
    paires = mesure["paires"]
    def agg(f):
        v = [p["top1"] for p in paires if f(p)]
        return float(np.mean(v)) if v else None
    ecarts = {}
    for nom, obs, ref in [
        ("n_paires", len(paires), j["agregats"]["toutes"]["n_paires"]),
        ("top1_moyen", agg(lambda p: True), j["agregats"]["toutes"]["top1_moyen"]),
        ("script_meme", agg(lambda p: p["script_match"]), j["agregats"]["script_meme"]["top1_moyen"]),
        ("script_different", agg(lambda p: not p["script_match"]), j["agregats"]["script_different"]["top1_moyen"]),
        ("famille_meme", agg(lambda p: p["famille_match"]), j["agregats"]["famille_meme"]["top1_moyen"]),
        ("famille_differente", agg(lambda p: p["famille_differente"]), j["agregats"]["famille_differente"]["top1_moyen"]),
        ("script_meme_famille_meme", agg(lambda p: p["script_match"] and p["famille_match"]),
         j["agregats"]["script_meme_famille_meme"]["top1_moyen"]),
        ("script_meme_famille_differente", agg(lambda p: p["script_match"] and p["famille_differente"]),
         j["agregats"]["script_meme_famille_differente"]["top1_moyen"]),
    ]:
        ecarts[nom] = {"observe": obs, "j31": ref,
                       "ecart": abs(obs - ref) if (obs is not None and ref is not None) else None}
    reg_obs = mesure["regressions"]["j31_compatible"]
    for nom, obs, ref in [
        ("coef_script", reg_obs["coef"]["script_match"], j["regression"]["coef"]["script_match"]),
        ("coef_famille", reg_obs["coef"]["famille_match"], j["regression"]["coef"]["famille_match"]),
        ("r2", reg_obs["r2"], j["regression"]["r2"]),
    ]:
        ecarts[nom] = {"observe": obs, "j31": ref, "ecart": abs(obs - ref)}
    max_ecart = max(x["ecart"] for x in ecarts.values() if x["ecart"] is not None)
    return {"ok": bool(max_ecart < 1e-9), "ecart_max": float(max_ecart), "detail": ecarts}


# ---------------------------------------------------------------------------
# 8. Contrôle d'époque — placebo de dates
# ---------------------------------------------------------------------------

def placebo_epoque(mesure: dict, meta: dict, graine: int = 0, n: int = 200) -> dict:
    paires = mesure["paires"]
    cles = mesure["langues"]
    rng = np.random.RandomState(graine + 606)
    coefs = []
    for _ in range(n):
        annees = {k: float(rng.uniform(1900, 2000)) for k in cles}
        for p in paires:
            p["_delta_faux"] = abs(annees[p["a"]] - annees[p["b"]]) / 100.0
        r = _ols_sans_chance(paires, ["_delta_faux", "script_match", "famille_match"])
        coefs.append(r["coef"]["_delta_faux"])
    for p in paires:
        p.pop("_delta_faux", None)
    return {
        "epoques_distinctes": [1948],
        "n_placebos": n,
        "coef_date_faux_moyen": float(np.mean(coefs)),
        "coef_date_faux_ic95": ic95(coefs),
        "part_positifs": float(np.mean([c > 0 for c in coefs])),
        "lecture": "l'UDHR est mono-époque (1948) ; un coefficient de date nul est attendu. "
                   "Le seul bras où la date varie est la Bible de J3.1 (−0,034/siècle, p = 0,19).",
    }


# ---------------------------------------------------------------------------
# 9. Sortie
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default=str(SORTIE))
    ap.add_argument("--graine", type=int, default=0)
    ap.add_argument("--permutations", type=int, default=1000)
    ap.add_argument("--permutations-paires", type=int, default=500)
    ap.add_argument("--rapide", action="store_true")
    a = ap.parse_args()
    if a.rapide:
        a.permutations = min(a.permutations, 200)
        a.permutations_paires = min(a.permutations_paires, 100)

    print("Panini UDHR 532 — chargement…", flush=True)
    panini_json = lire_json(PANINI_CORPUS)
    panini = panini_json["languages"]
    genealogie = lire_json(GENEALOGIE)
    glotto = Glottolog(GLOTTOLOG_LANGS, GLOTTOLOG_VALUES)
    meta, couverture = construire_meta(panini, glotto, genealogie)
    ensembles = construire_ensembles(meta, panini)
    print(f"  {len(panini)} textes Panini · {len(meta)} étiquetés Glottolog · "
          f"{ensembles['n_groupes']} langues distinctes", flush=True)

    print("Global 532 — article 1, voisinage généalogique…", flush=True)
    global_532 = mesure_globale(meta, panini, ensembles["representants"],
                                graine=a.graine, permutations=a.permutations)
    g = global_532["agregats"]["toutes"]
    print(f"  {global_532['n_requetes']} requêtes · top1 famille {g['top1_famille']:.4f} "
          f"(hasard {g['p_famille']:.4f}) · top1 sœur {g['top1_soeur']:.4f} "
          f"(hasard {g['p_soeur']:.4f})", flush=True)

    articles = charger_articles()
    print("Parallèle 30 articles — LANG_TREE 29, échantillon 20, J3.1 21, union…", flush=True)
    m_langtree = mesure_paire(meta, articles, list(ensembles["lang_tree"].values()),
                              graine=a.graine, permutations=a.permutations_paires)
    m_echantillon = mesure_paire(meta, articles, ensembles["echantillon_20"],
                                 graine=a.graine, permutations=a.permutations_paires)
    m_j31 = mesure_paire(meta, articles, ensembles["j31_21"],
                         graine=a.graine, permutations=a.permutations_paires)
    m_union = mesure_paire(meta, articles, ensembles["union"],
                           graine=a.graine, permutations=a.permutations_paires)
    verification = verifier_j31(m_j31, lire_json(J31_JSON))
    print(f"  LANG_TREE {m_langtree['n_langues']} langues / {m_langtree['n_paires']} paires · "
          f"J3.1 reproduit : {verification['ok']} (écart max {verification['ecart_max']:.2e})", flush=True)

    print("Contrôle d'époque — placebo de dates…", flush=True)
    epoque = {
        "udhr": placebo_epoque(m_union, meta, graine=a.graine, n=200),
        "j31_bible": {
            "coef_delta_annees_par_siecle": lire_json(J31_JSON)["bible"]["regression"]["coef"]["delta_annees_par_siecle"],
            "ic95": lire_json(J31_JSON)["bible"]["regression"]["ic95"]["delta_annees_par_siecle"],
            "p_permutation": lire_json(J31_JSON)["bible"]["regression"]["controle_annees_permutees"]["p_value_unilaterale_negative"],
            "coef_script": lire_json(J31_JSON)["bible"]["regression"]["coef"]["script_match"],
            "lecture": "seul bras daté ; l'époque ne pèse pas, l'écriture domine",
        },
    }

    # Table de comparaison J3.1 / J7.1
    def ligne(m):
        return {
            "n_langues": m["n_langues"], "n_paires": m["n_paires"],
            "top1_moyen": m["agregats"]["toutes"]["top1_moyen"],
            "script_meme": m["agregats"]["script_meme"]["top1_moyen"],
            "script_different": m["agregats"]["script_different"]["top1_moyen"],
            "famille_meme": m["agregats"]["famille_meme"]["top1_moyen"],
            "famille_differente": m["agregats"]["famille_differente"]["top1_moyen"],
            "soeur": m["agregats"]["soeur"]["top1_moyen"],
            "famille_autre_branche": m["agregats"]["famille_autre_branche"]["top1_moyen"],
            "coef_script": m["regressions"]["j31_compatible"]["coef"]["script_match"],
            "coef_famille": m["regressions"]["j31_compatible"]["coef"]["famille_match"],
            "coef_soeur": m["regressions"]["decomposition"]["coef"]["soeur"],
            "coef_famille_autre": m["regressions"]["decomposition"]["coef"]["famille_autre_branche"],
            "r2": m["regressions"]["j31_compatible"]["r2"],
        }
    comparaison = {"j31_21": ligne(m_j31), "echantillon_20": ligne(m_echantillon),
                   "lang_tree_25": ligne(m_langtree), "union_39": ligne(m_union)}

    resultat = {
        "tache": "J7.1",
        "titre": "le retrieval approfondi par famille Glottolog",
        "date": "2026-11-14",
        "ligne_roadmap": "R0.7 (le bloc langue) / L",
        "chantier": "Panini, J7.1",
        "statut": "mesuré, contrôlé",
        "question": "Sur les 532 langues UDHR (même source XML), le retrieval de surface retrouve-t-il "
                    "la famille Glottolog, et le signal de sœur résiste-t-il au contrôle d'époque ?",
        "sources": {
            "panini_corpus": {"chemin": str(PANINI_CORPUS.relative_to(RACINE.parent)),
                              "format": panini_json.get("format"), "langues": panini_json.get("total_languages"),
                              "sha256": sha256(PANINI_CORPUS), "commit_panini": commit(PANINI_CORPUS.parent)},
            "panini_lang_tree": {"chemin": str(PANINI_LANG_TREE.relative_to(RACINE.parent)),
                                 "sha256": sha256(PANINI_LANG_TREE), "n_langues": 29},
            "drave_articles": {"chemin": str(ARTICLES.relative_to(RACINE)),
                               "sha256": sha256(ARTICLES), "commit_drave": commit(RACINE)},
            "drave_genealogie": {"chemin": str(GENEALOGIE.relative_to(RACINE)),
                                 "sha256": sha256(GENEALOGIE)},
            "j31": {"chemin": str(J31_JSON.relative_to(RACINE)),
                    "sha256": sha256(J31_JSON)},
            "corpus_commun": {"chemin": str(CORPUS_COMMUN.relative_to(RACINE)),
                              "sha256": sha256(CORPUS_COMMUN)},
        },
        "methode": {
            "retrieval": "n-grammes de caractères n=3, TF-IDF (idf lissé, tf sous-linéaire), cosinus, top-1/MRR",
            "chance": "1 / nombre de candidats (30 pour le parallèle ; 1/(N-1) pour le global)",
            "famille": "Glottolog (Drave genealogie.json, puis languages.csv/values.csv)",
            "soeur": "même famille et LCA de profondeur >= 3, hors couples ancêtre/descendant",
            "soeur_stricte": "même famille et LCA de profondeur >= 4, hors couples ancêtre/descendant",
            "famille_autre_branche": "même famille, LCA < 3 (ou ancêtre/descendant)",
            "controles": "permutation des étiquettes, requêtes permutées, candidats mélangés, placebo de dates",
            "graine": a.graine,
            "permutations": a.permutations,
            "permutations_paires": a.permutations_paires,
        },
        "couverture": {
            **couverture,
            "n_textes_panini": len(panini),
            "n_textes_labelises": ensembles["n_textes_labelises"],
            "n_langues_distinctes": ensembles["n_groupes"],
            "taux_labelises": ensembles["n_textes_labelises"] / len(panini),
            "n_groupes_iso": ensembles["n_groupes_iso"],
            "variantes_iso": ensembles["n_textes_labelises"] - ensembles["n_groupes_iso"],
            "n_doublons_texte": len(ensembles["doublons_texte"]),
            "doublons_texte": ensembles["doublons_texte"],
            "variantes_dedupliquees": ensembles["n_textes_labelises"] - ensembles["n_groupes"],
            "lang_tree_29": {
                "mappees": len(ensembles["lang_tree"]),
                "uniques": len(set(ensembles["lang_tree"].values())),
                "absentes_udhr": [c for c, v in LANG_TREE_VERS_PANINI.items() if v is None],
                "table": LANG_TREE_VERS_PANINI,
            },
            "echantillon_20": ensembles["echantillon_20"],
            "j31_21": ensembles["j31_21"],
            "union": ensembles["union"],
        },
        "global_532": global_532,
        "lang_tree": m_langtree,
        "echantillon_20": m_echantillon,
        "j31_21": m_j31,
        "union_39": m_union,
        "verification_j31": verification,
        "comparaison_j31": comparaison,
        "epoque": epoque,
        "controles_negatifs": {
            "global_532": global_532["controles"],
            "lang_tree": {
                "permutation_familles": m_langtree["regressions"]["decomposition"]["controle_permutation"],
                "candidats_melanges": m_langtree["controle_candidats_melanges"],
                "contraste_soeurs": m_langtree["contraste_soeurs"],
            },
            "echantillon_20": {
                "permutation_familles": m_echantillon["regressions"]["decomposition"]["controle_permutation"],
                "candidats_melanges": m_echantillon["controle_candidats_melanges"],
                "contraste_soeurs": m_echantillon["contraste_soeurs"],
            },
            "union_39": {
                "permutation_familles": m_union["regressions"]["decomposition"]["controle_permutation"],
                "candidats_melanges": m_union["controle_candidats_melanges"],
                "contraste_soeurs": m_union["contraste_soeurs"],
            },
            "j31_reproduction": verification,
        },
        "limites": [
            "Le retrieval est de surface (n-grammes de caractères), pas neuronal ; il capture l'orthographe, "
            "les cognates et les emprunts, pas la syntaxe ni le sens profond.",
            "Le global 532 ne porte que l'article 1 (Panini ne publie que cet article) ; le parallèle 30 articles "
            "est limité aux langues de LANG_TREE et de l'échantillon 20, toutes couvertes par Drave.",
            "Les 28 textes non étiquetés (variantes numériques UDHR) sont exclus des mesures de famille ; "
            "le taux de couverture Glottolog est de 504/532.",
            "Les variantes d'une même langue (même ISO3) sont dédupliquées : 63 textes en moins, 441 langues "
            "distinctes. Le global mesure donc 441 langues, pas 532 textes indépendants.",
            "L'UDHR est mono-époque (1948) : l'époque est contrôlée par construction, pas estimée ; le placebo "
            "de dates ne peut pas prouver l'absence d'un effet d'époque, il vérifie seulement que le pipeline "
            "ne fabrique pas de signal de date.",
            "Les dates de traduction des 532 textes ne sont pas documentées ; certaines traductions sont "
            "postérieures à 1948, mais le corpus ne porte pas cette information.",
            "Les paires ne sont pas indépendantes (une langue apparaît dans plusieurs paires) ; les IC sont "
            "des intervalles inter-paires et le leave-one-language-out donne la sensibilité.",
            "La définition de « sœur » (LCA >= 3) est une convention de niveau branche ; elle inclut des "
            "couples comme indo-iranien (sanskrit/farsi) et exclut les ancêtres/descendants (latin/français). "
            "La variante stricte (LCA >= 4) est reportée.",
        ],
        "fichiers": {
            "outil": "tools/retrieval_familles.py",
            "json": "reports/retrieval-familles.json",
            "fiche": "reports/rapport-retrieval-familles.md",
        },
    }
    sortie = pathlib.Path(a.sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ {sortie}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
