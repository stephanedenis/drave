#!/usr/bin/env python3
"""protocole_date.py — B1 : le protocole Panini à date contrôlée (suite de la note 4A).

Ce script ne modifie jamais Panini. Il lit les artefacts §334 en lecture seule,
vérifie leurs SHA-256, construit le manifeste des **60 paires** en trois groupes
(20 contemporaines de traditions différentes à ±10 ans, 20 de même tradition à
±200 ans, 20 de même langue source à dates décalées), puis peut rejouer le test
si Panini fournit les signatures V14 des 26 textes qui n'en ont pas encore.

Usage :
  python3 tools/protocole_date.py --verifier
  python3 tools/protocole_date.py --construire --sortie reports/protocole-date.json
  python3 tools/protocole_date.py --rejouer --signatures /tmp/v14.json
  python3 tools/protocole_date.py --rejouer --rapide --sortie /tmp/resultats.json

Le manifeste est **gelé** : la sélection ne regarde que les métadonnées (année,
tradition, langue, auteur, titre), jamais les 14 atomes ni les distances
lexicales. Le test se rejoue sur le fichier gelé, jamais en re-sélectionnant.
"""
from __future__ import annotations

import argparse
import collections
import datetime as _dt
import hashlib
import heapq
import itertools
import json
import math
import pathlib
import random
import re
import subprocess
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
PANINI = RACINE.parent / "Panini" / "research"
FALS = PANINI / "nipada" / "falsification"
CACHE = PANINI / "nipada" / "corpus" / "_cache"

PAIRES_334 = FALS / "pairs334_axes_v1.json"
GRAPHE = FALS / "nipada_v334_graph_v35.json"
SIGNATURES_44 = FALS / "analytic_sigs_v1.json"
REVALIDATION = FALS / "nipada_v334_revalidation_v35.json"
COUVERTURE = CACHE / "sources_coverage.json"
MANIFESTE_SOURCES = CACHE / "sources_manifest.json"
V150 = FALS / "nipada_v150_validation.json"

SORTIE_DEFAUT = RACINE / "reports" / "protocole-date.json"
RESULTATS_DEFAUT = RACINE / "reports" / "protocole-date-resultats.json"

ATOMES = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS", "MODALITÉ",
    "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION", "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]

# Familles larges : on ne fusionne que les étiquettes qui séparent le même texte
# ou le même auteur (GRECO_PLATONIC vs GRECO_LATIN_AXIAL, JUDEAN vs ABRAHAMIC).
FAMILLES = {
    "GRECO_LATIN_AXIAL": "GRECO", "GRECO_PLATONIC": "GRECO",
    "GRECO_LAT_MATERIAL": "GRECO", "GRECO_PRESOCRATIC": "GRECO",
    "ANCIENT_EPICUREAN": "GRECO", "SCEPT": "GRECO", "STOIC_ROMAN": "GRECO",
    "ABRAHAMIC_PROPHETIC_AXIAL": "ABRAHAMIC", "JUDEAN_APOCALYPTIC_LATE": "ABRAHAMIC",
    "BUDDHIST_AXIAL": "BUDDHIST",
    "CHINESE_AXIAL": "CHINESE", "DAOISM": "CHINESE", "CONFUCIAN_AXIAL": "CHINESE",
    "INDIAN_AXIAL": "INDIAN", "INDIAN_MATERIAL": "INDIAN",
    "ISLAMIC": "ISLAMIC", "ISLAMIC_RATIONALIST": "ISLAMIC",
    "MILLENARIAN_MODERN_PROTESTANT": "MILLENARIAN",
    "COMBINATORY_LOGIC": "FORMAL_LOGIC", "RECURSIVE_FUNCTIONS": "FORMAL_LOGIC",
    "MANY_VALUED_LOGIC": "FORMAL_LOGIC", "FUZZY_LOGIC": "FORMAL_LOGIC",
    "SEMANTIC_NETWORKS": "COGNITIVE_SCIENCE", "CONCEPTUAL_DEPENDENCY": "COGNITIVE_SCIENCE",
    "DISTRIBUTIONAL_SEMANTICS": "COGNITIVE_SCIENCE", "NEURAL_LANGUAGE_MODELS": "COGNITIVE_SCIENCE",
    "NEUROSEMIOTICS": "COGNITIVE_SCIENCE", "COGNITIVE_LIMITS": "COGNITIVE_SCIENCE",
    "MODERN_WESTERN": "EUROPE_MODERN", "EUR_RATIONALIST_CRITIC": "EUROPE_MODERN",
    "EUR_ANTI_CHRISTIAN": "EUROPE_MODERN", "FRENCH_ENLIGHTENMENT": "EUROPE_MODERN",
    "EUR_MATERIALIST_ATHEIST": "EUROPE_MODERN", "EUR_SCEPTICAL_EMPIRICIST": "EUROPE_MODERN",
    "EUR_PESSIMIST_CRITIC": "EUROPE_MODERN", "MATERIALIST_MODERN": "EUROPE_MODERN",
    "AMERICAN_FREETHINKER": "EUROPE_MODERN", "EUR_THEOL_CRITIC": "EUROPE_MODERN",
    "CLASSICAL_ORACULAR": "CLASSICAL_ORACULAR", "NORSE_EDDIC_MEDIEVAL": "NORSE_EDDIC",
    "RENAISSANCE_OCCULT_EARLY_MODERN": "RENAISSANCE_OCCULT",
}

ALIASES_AUTEUR = {
    "platon jowett": "plato", "platon cousin": "plato",
    "paul henri thiry baron d holbach": "holbach", "ludwig feuerbach": "feuerbach",
    "darwin bronn": "darwin", "charles darwin": "darwin",
    "david hume": "hume", "anonymous sangha": "anonymous",
}

# Les 60 paires, gelées. Chaque paire est (id_a, id_b) ; l'ordre est sans effet.
G1 = [
    ("baudhayana_dharmasutra", "plato_crito"),
    ("vasistha_dharmasutra", "plato_euthyphro_jowett"),
    ("hiranyakesi_grhya_sutra", "plato_charmides"),
    ("paraskara_grhya_sutra", "plato_crito"),
    ("apastamba_grhya_sutra", "plato_euthyphro_jowett"),
    ("sankhayana_grhya_sutra", "plato_charmides"),
    ("daodejing", "plato_laws"),
    ("daodejing", "plato_sophist"),
    ("qiwulun", "epicurus_letters"),
    ("mengzi", "epicurus_letters"),
    ("mandukya_upanishad", "qiwulun"),
    ("mandukya_upanishad", "mengzi"),
    ("mandukya_upanishad", "xiaojing"),
    ("burnet_early_greek_philosophy", "curry_1930"),
    ("miller_1956", "zadeh_1965"),
    ("ingersoll_works", "russell_parousia_1878"),
    ("chandogya_upanishad", "isaiah_book"),
    ("brihadaranyaka_upanishad", "isaiah_book"),
    ("book_of_enoch", "yueji"),
    ("book_of_enoch", "sibylline_oracles"),
]
G2 = [
    ("plato_gorgias", "aristotle_posterior_analytics"),
    ("plato_meno", "aristotle_de_caelo"),
    ("plato_republic_jowett", "aristotle_parts_of_animals"),
    ("plato_symposium_jowett", "aristotle_categories"),
    ("plato_republic_jowett", "aristotle_nicomachean_ethics"),
    ("plato_laws", "aristotle_parts_of_animals"),
    ("plato_gorgias", "aristotle_prior_analytics"),
    ("plato_phaedo", "aristotle_de_caelo"),
    ("isaiah_book", "zechariah_book"),
    ("jeremiah_book", "hosea_book"),
    ("ezekiel_book", "zechariah_book"),
    ("daniel_book", "book_of_enoch"),
    ("isaiah_book", "ezekiel_book"),
    ("jeremiah_book", "zechariah_book"),
    ("chandogya_upanishad", "isa_upanishad"),
    ("brihadaranyaka_upanishad", "isa_upanishad"),
    ("isa_upanishad", "mandukya_upanishad"),
    ("zhuangzi", "yueji"),
    ("xiaojing", "yueji"),
    ("daodejing", "liji"),
]
G3 = [
    ("2_esdras", "miller_evidence_prophecy"),
    ("daniel_book", "kleene_1936"),
    ("book_of_enoch", "curry_1930"),
    ("sibylline_oracles", "schank_1972"),
    ("voluspa", "isaiah_book"),
    ("lucretius_drn", "holbach_systeme_en"),
    ("hume_dialogues_nhr", "russell_parousia_1878"),
    ("miller_evidence_prophecy", "bengio_2003"),
    ("2_esdras", "schank_1972"),
    ("daniel_book", "miller_evidence_prophecy"),
    ("book_of_enoch", "kleene_1936"),
    ("sibylline_oracles", "curry_1930"),
    ("sextus_pyrrho", "plato_republic_jowett"),
    ("sextus_pyrrho", "plato_phaedo"),
    ("sextus_pyrrho", "plato_gorgias_jowett"),
    ("plato_gorgias", "aristotle_parts_of_animals"),
    ("plato_symposium_jowett", "aristotle_de_caelo"),
    ("chandogya_upanishad", "baudhayana_dharmasutra"),
    ("brihadaranyaka_upanishad", "baudhayana_dharmasutra"),
    ("daodejing", "yueji"),
]
PAIRES_PROTOCOLE = {"G1": G1, "G2": G2, "G3": G3}

CRITERE = {
    "G1": "|Δannée| ≤ 10 et familles larges différentes",
    "G2": "20 ≤ |Δannée| ≤ 200 et même famille large",
    "G3": "|Δannée| ≥ 50 et même langue source documentée",
}

COMMIT_PANINI_4A = "e10d695e65f52031222819cb1bdbb290d08f8e57"
GRAINE = 20261115
DATE_PROTOCOLE = "2026-11-15"
VERSION = "1.0"
SEUIL_G3 = 50

LIMITES = [
    "Les dates sont celles de la composition (ou de l'estimation) et non de la traduction ; "
    "les signatures sont calculées sur des traductions majoritairement anglaises.",
    "Les 60 paires ne portent que 59 textes distincts ; un texte peut servir jusqu'à 5 paires "
    "(isaiah_book, book_of_enoch). Les paires ne sont donc pas indépendantes ; l'inférence "
    "regroupe par texte (permutation et bootstrap par texte).",
    "Le §334 ne fournit que 44 signatures mesurées (analytic_sigs_v1) ; 26 des 59 textes du "
    "manifeste n'en ont pas. Le test complet exige que Panini signe ces 26 textes avec le même "
    "extracteur V14, sans mélanger avec les v14_signature du graphe v35 (instrument différent : "
    "cosinus 0,42–0,82 sur les 11 œuvres communes).",
    "G1 ne contient qu'une paire dont les deux signatures sont déjà mesurées "
    "(book_of_enoch / sibylline_oracles) ; les 19 autres exigent au moins une nouvelle signature. "
    "Le contrôle positif de filiation est donc, lui aussi, en attente de signatures.",
    "G3 est majoritairement anglais (12/20 paires, toutes inter-familles) ; les 8 autres paires "
    "sont intra-famille (grec 5, sanskrit 2, chinois 1). La strate « surface contrôlée » est donc "
    "surtout la strate anglaise.",
    "Avec 20 paires par groupe, la puissance est faible : le design ne détecte que des effets "
    "standardisés |β| ≳ 0,55 (α = 0,05, 80 %) ; les effets plus petits seront bornés par l'IC et "
    "le ROPE, pas testés.",
    "La distance topologique d_topo est recalculée par plus court chemin non pondéré dans le "
    "graphe v35 ; elle corrèle à r = 0,943 avec le d_topo publié des 655 paires, mais ce n'est "
    "pas la même quantité exacte.",
    "Les étiquettes de tradition sont celles de Panini ; le regroupement en familles larges est "
    "une décision de Drave, documentée dans FAMILLES et vérifiable dans le JSON.",
]

# ---------------------------------------------------------------------------
# Outils
# ---------------------------------------------------------------------------

def sha256(chemin: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def lire_json(chemin: pathlib.Path):
    return json.loads(chemin.read_text(encoding="utf-8"))


def commit_git(chemin: pathlib.Path):
    try:
        return subprocess.check_output(
            ["git", "-C", str(chemin), "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return None


def normaliser(texte) -> str:
    if not texte:
        return ""
    s = str(texte).lower()
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"\b(trans|translation|transl\.?|trad\.?)\b.*$", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def auteur(v) -> str:
    a = normaliser(v.get("author"))
    return ALIASES_AUTEUR.get(a, a)


def titre(v) -> str:
    return normaliser(v.get("title_en") or v.get("title_original") or "")


def famille(v):
    t = v.get("tradition_label")
    return FAMILLES.get(t, t)


def arrondi(x, n=6):
    if x is None:
        return None
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return None
    return round(float(x), n)


# ---------------------------------------------------------------------------
# Chargement et métadonnées
# ---------------------------------------------------------------------------

class Corpus:
    def __init__(self):
        self.manifeste = lire_json(MANIFESTE_SOURCES)
        self.couverture = {x["id"]: x for x in lire_json(COUVERTURE)}
        self.graphe = lire_json(GRAPHE)
        self.noeuds = self.graphe["nodes"]
        self.aretes = self.graphe["edges"]
        self.signatures = lire_json(SIGNATURES_44)
        self.paires334 = lire_json(PAIRES_334)["pairs"]
        self.ids = list(dict.fromkeys(x["id"] for x in self.manifeste))

    def meta(self, ident: str):
        v = self.noeuds.get(ident, {})
        a = auteur(v)
        t = titre(v)
        return {
            "id": ident,
            "annee": v.get("year"),
            "langue": v.get("language_original") or v.get("lang"),
            "tradition_label": v.get("tradition_label"),
            "famille": famille(v),
            "auteur": a,
            "titre": t,
            "travail": (a, t) if t else (a, ident),
            "source": next((x.get("url") for x in self.manifeste if x["id"] == ident), None),
            "source_ok": bool(self.couverture.get(ident, {}).get("ok")),
            "signature_44": ident in self.signatures,
            "signature_graphe": v.get("v14_signature") is not None,
        }

    def lignes(self):
        return [self.meta(i) for i in self.ids if self.noeuds.get(i, {}).get("year") is not None]


def meme_travail(a, b) -> bool:
    if a["id"] == b["id"]:
        return True
    if a["titre"] and a["titre"] == b["titre"]:
        return True
    return bool(a["travail"][1] and a["travail"] == b["travail"])


def auteurs_differents(a, b) -> bool:
    return not (a["auteur"] == b["auteur"] and a["auteur"] not in ("anonymous", ""))


def candidats(corpus: Corpus, groupe: str):
    out = []
    for a, b in itertools.combinations(corpus.lignes(), 2):
        if meme_travail(a, b) or not auteurs_differents(a, b):
            continue
        d = abs(a["annee"] - b["annee"])
        if groupe == "G1" and d <= 10 and a["famille"] and b["famille"] and a["famille"] != b["famille"]:
            out.append((a, b))
        if groupe == "G2" and 20 <= d <= 200 and a["famille"] and a["famille"] == b["famille"]:
            out.append((a, b))
        if groupe == "G3" and d >= SEUIL_G3 and a["langue"] and a["langue"] == b["langue"]:
            out.append((a, b))
    return out


# ---------------------------------------------------------------------------
# d_topo : plus court chemin non pondéré
# ---------------------------------------------------------------------------

def construire_adjacence(corpus: Corpus):
    adj = collections.defaultdict(list)
    for e in corpus.aretes:
        s, t = e.get("src"), e.get("tgt")
        if s in corpus.noeuds and t in corpus.noeuds:
            adj[s].append(t)
            adj[t].append(s)
    return adj


def bfs(adj, source, cibles):
    dist = {source: 0}
    file = collections.deque([source])
    restants = set(cibles)
    while file and restants:
        u = file.popleft()
        for v in adj.get(u, []):
            if v not in dist:
                dist[v] = dist[u] + 1
                if v in restants:
                    restants.discard(v)
                file.append(v)
    return {c: dist.get(c) for c in cibles}


def distances_topo(corpus: Corpus, ids):
    adj = construire_adjacence(corpus)
    cache = {}
    for i in ids:
        cache[i] = bfs(adj, i, ids)
    return cache


# ---------------------------------------------------------------------------
# Construction du manifeste
# ---------------------------------------------------------------------------

def construire(corpus: Corpus) -> dict:
    lignes = corpus.lignes()
    textes_manifeste = []
    for groupe, paires in PAIRES_PROTOCOLE.items():
        for a, b in paires:
            if a not in textes_manifeste:
                textes_manifeste.append(a)
            if b not in textes_manifeste:
                textes_manifeste.append(b)

    # vérifications de base
    for ident in textes_manifeste:
        if ident not in corpus.noeuds:
            raise SystemExit(f"texte absent du graphe v35 : {ident}")
        if not corpus.couverture.get(ident, {}).get("ok"):
            raise SystemExit(f"source non acquise (§334) : {ident}")

    topo = distances_topo(corpus, sorted(set(textes_manifeste)))

    paires = []
    for groupe, liste in PAIRES_PROTOCOLE.items():
        for rang, (a, b) in enumerate(liste, 1):
            ma, mb = corpus.meta(a), corpus.meta(b)
            d = abs(ma["annee"] - mb["annee"])
            if groupe == "G1":
                assert d <= 10 and ma["famille"] != mb["famille"], (a, b, d)
            elif groupe == "G2":
                assert 20 <= d <= 200 and ma["famille"] == mb["famille"], (a, b, d)
            else:
                assert d >= SEUIL_G3 and ma["langue"] == mb["langue"], (a, b, d)
            signatures = int(ma["signature_44"]) + int(mb["signature_44"])
            paires.append({
                "id": f"{groupe}-{rang:02d}",
                "groupe": groupe,
                "a": a,
                "b": b,
                "annee_a": ma["annee"],
                "annee_b": mb["annee"],
                "delta_annee": d,
                "famille_a": ma["famille"],
                "famille_b": mb["famille"],
                "meme_famille": ma["famille"] == mb["famille"],
                "langue_a": ma["langue"],
                "langue_b": mb["langue"],
                "meme_langue": ma["langue"] == mb["langue"],
                "tradition_a": ma["tradition_label"],
                "tradition_b": mb["tradition_label"],
                "titre_a": ma["titre"],
                "titre_b": mb["titre"],
                "auteur_a": ma["auteur"],
                "auteur_b": mb["auteur"],
                "source_a": ma["source"],
                "source_b": mb["source"],
                "d_topo": topo[a].get(b),
                "signatures_44": signatures,
                "etat_signatures": {2: "deux", 1: "une", 0: "aucune"}[signatures],
            })

    # composition
    comp = {
        "G1": {
            "n": len(G1),
            "paires_de_familles": dict(collections.Counter(
                "–".join(sorted((p["famille_a"], p["famille_b"]))) for p in paires if p["groupe"] == "G1"
            )),
            "delta_annee": _stats([p["delta_annee"] for p in paires if p["groupe"] == "G1"]),
        },
        "G2": {
            "n": len(G2),
            "familles": dict(collections.Counter(p["famille_a"] for p in paires if p["groupe"] == "G2")),
            "delta_annee": _stats([p["delta_annee"] for p in paires if p["groupe"] == "G2"]),
        },
        "G3": {
            "n": len(G3),
            "langues": dict(collections.Counter(p["langue_a"] for p in paires if p["groupe"] == "G3")),
            "inter_familles": sum(1 for p in paires if p["groupe"] == "G3" and not p["meme_famille"]),
            "delta_annee": _stats([p["delta_annee"] for p in paires if p["groupe"] == "G3"]),
        },
        "textes_distincts": len(textes_manifeste),
        "paires_distinctes": len(set(tuple(sorted((p["a"], p["b"]))) for p in paires)),
        "usage_max": None,
        "usage": {},
    }
    usage = collections.Counter()
    for p in paires:
        usage[p["a"]] += 1
        usage[p["b"]] += 1
    comp["usage"] = dict(usage.most_common())
    comp["usage_max"] = max(usage.values())

    # textes et à signer
    textes = []
    for ident in sorted(textes_manifeste):
        m = corpus.meta(ident)
        textes.append({
            "id": ident,
            "annee": m["annee"],
            "langue": m["langue"],
            "tradition_label": m["tradition_label"],
            "famille": m["famille"],
            "auteur": m["auteur"],
            "titre": m["titre"],
            "source": m["source"],
            "source_ok": m["source_ok"],
            "signature_44": m["signature_44"],
            "signature_graphe": m["signature_graphe"],
            "usage": usage[ident],
        })
    a_signer = [
        {"id": t["id"], "annee": t["annee"], "langue": t["langue"], "famille": t["famille"],
         "source": t["source"], "usage": t["usage"]}
        for t in textes if not t["signature_44"]
    ]

    # faisabilité
    pools = {}
    for g in ("G1", "G2", "G3"):
        cand = candidats(corpus, g)
        n_deux = sum(1 for a, b in cand if a["signature_44"] and b["signature_44"])
        n_une = sum(1 for a, b in cand if bool(a["signature_44"]) ^ bool(b["signature_44"]))
        pools[g] = {
            "critere": CRITERE[g],
            "candidats": len(cand),
            "deux_signatures_44": n_deux,
            "une_signature_44": n_une,
            "aucune_signature_44": len(cand) - n_deux - n_une,
        }
    # composition des pools G1/G2/G3 (pour le rapport)
    g1p = collections.Counter("–".join(sorted((a["famille"], b["famille"]))) for a, b in candidats(corpus, "G1"))
    g2p = collections.Counter(a["famille"] for a, b in candidats(corpus, "G2"))
    g3p = collections.Counter(a["langue"] for a, b in candidats(corpus, "G3"))
    pools["G1"]["paires_de_familles"] = dict(g1p)
    pools["G2"]["familles"] = dict(g2p)
    pools["G3"]["langues"] = dict(g3p)

    # instrument : deux sources de signatures, à ne pas mélanger
    ov = [k for k in corpus.signatures if corpus.noeuds.get(k, {}).get("v14_signature")]
    cos = []
    l2 = []
    for k in ov:
        cles = list(corpus.signatures[k])
        a = [float(corpus.signatures[k][x]) for x in cles]
        b = [float(corpus.noeuds[k]["v14_signature"].get(x, 0.0)) for x in cles]
        na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(x * x for x in b))
        cos.append(sum(x * y for x, y in zip(a, b)) / (na * nb) if na and nb else None)
        l2.append(math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b))))

    # sources et hashes
    sources = {}
    for nom, chemin in [
        ("paires334", PAIRES_334), ("graphe334", GRAPHE), ("signatures44", SIGNATURES_44),
        ("revalidation334", REVALIDATION), ("couverture", COUVERTURE),
        ("manifeste_sources", MANIFESTE_SOURCES), ("v150", V150),
    ]:
        sources[nom] = {
            "chemin": str(chemin.relative_to(RACINE.parent)),
            "sha256": sha256(chemin),
        }

    commit_lu = commit_git(RACINE.parent / "Panini")
    manifeste = {
        "tache": "B1",
        "version": VERSION,
        "titre": "Protocole Panini à date contrôlée — 60 paires en trois groupes",
        "date": DATE_PROTOCOLE,
        "commit_drave": commit_git(RACINE),
        "commit_panini": {
            "attendu_4a": COMMIT_PANINI_4A,
            "lu": commit_lu,
            "identique": commit_lu == COMMIT_PANINI_4A,
            "note": "Le HEAD de Panini peut avancer ; les SHA-256 des artefacts §334 sont la référence.",
        },
        "sources": sources,
        "protocole": _protocole(),
        "pre_enregistrement": _pre_enregistrement(),
        "faisabilite": {
            "univers": {
                "sources_manifeste": len(corpus.ids),
                "sources_ok": sum(1 for i in corpus.ids if corpus.couverture.get(i, {}).get("ok")),
                "sources_non_ok": [i for i in corpus.ids if not corpus.couverture.get(i, {}).get("ok")],
                "textes_dates": len(lignes),
                "signatures_44": len(corpus.signatures),
                "signatures_graphe": sum(1 for v in corpus.noeuds.values() if v.get("v14_signature")),
            },
            "pools": pools,
            "instrument": {
                "signatures_44": len(corpus.signatures),
                "signatures_graphe": sum(1 for v in corpus.noeuds.values() if v.get("v14_signature")),
                "communes": len(ov),
                "cosinus_communes": {"min": arrondi(min(cos)), "moyenne": arrondi(sum(cos) / len(cos)), "max": arrondi(max(cos))},
                "l2_communes": {"min": arrondi(min(l2)), "moyenne": arrondi(sum(l2) / len(l2)), "max": arrondi(max(l2))},
                "regle": "Ne jamais mélanger analytic_sigs_v1 et les v14_signature du graphe v35.",
            },
        },
        "composition": comp,
        "paires": paires,
        "textes": textes,
        "a_signer": a_signer,
        "commande": (
            "python3 tools/protocole_date.py --rejouer "
            "--signatures /chemin/vers/v14.json "
            "--sortie reports/protocole-date-resultats.json"
        ),
        "limites": LIMITES,
    }
    return manifeste


def _stats(valeurs):
    if not valeurs:
        return {"n": 0, "min": None, "median": None, "max": None, "moyenne": None}
    v = sorted(valeurs)
    return {
        "n": len(v),
        "min": v[0],
        "median": v[len(v) // 2] if len(v) % 2 else (v[len(v) // 2 - 1] + v[len(v) // 2]) / 2,
        "max": v[-1],
        "moyenne": sum(v) / len(v),
    }


def _protocole():
    return {
        "question": (
            "Après contrôle de la filiation (famille, topologie) et de la surface "
            "(langue source), l'écart de dates ajoute-t-il de la distance entre les "
            "signatures V14 ? C'est l'avertissement de Panini (β époque +0,138), "
            "testé sur un plan où date, filiation et surface ne sont plus confondues."
        ),
        "H0": (
            "H0 : dans le modèle d_sig ~ 1 + d_topo^0,67 + même_famille + même_langue "
            "+ |Δannée|/1000, le coefficient de |Δannée| est nul (β_date = 0) et le R² "
            "partiel de la date après filiation et surface est nul (ΔR²_date = 0). "
            "La signature V14 est une signature de filiation/surface, pas d'époque."
        ),
        "H1": (
            "H1 : β_date ≠ 0 (test bilatéral principal) ; H1+ : β_date > 0 (test "
            "directionnel secondaire, l'avertissement de Panini). Un β_date < 0 est "
            "rapporté comme un effet d'époque inversé, pas comme une confirmation."
        ),
        "atomes": ATOMES,
        "distance": (
            "d_sig(a,b) = ||s_a − s_b||_2 sur les 14 parts (somme 1). "
            "Distance cosinus en secondaire. Aucune autre transformation."
        ),
        "modeles": {
            "principal_G2": "d_sig ~ 1 + |Δannée|/1000, dans la même famille (20 paires)",
            "principal_G3": "d_sig ~ 1 + |Δannée|/1000, dans la même langue (20 paires)",
            "pooled": "d_sig ~ 1 + d_topo^0,67 + même_famille + même_langue + |Δannée|/1000 (60 paires)",
            "controle_positif_G1": (
                "Les 20 paires de G1 sont toutes inter-familles à date fixe ; on compare "
                "leur d_sig moyenne à un nul où les étiquettes de famille sont permutées "
                "dans des tranches de 250 ans. Si l'instrument voit la filiation, les "
                "paires inter-familles observées doivent être plus éloignées que le nul."
            ),
        },
        "tests_principaux": [
            "P1 (G2) : pente standardisée de |Δannée| dans la même famille ; R² partiel de la date.",
            "P2 (G3) : pente standardisée de |Δannée| dans la même langue ; R² partiel de la date.",
        ],
        "controles": [
            "Négatif 1 — étiquettes de famille permutées dans des tranches de 250 ans (G1) : "
            "le contraste de filiation doit disparaître.",
            "Négatif 2 — années permutées dans chaque famille (G2) : la pente de date doit disparaître.",
            "Négatif 3 — années permutées dans chaque langue (G3) : la pente de date doit disparaître.",
            "Négatif 4 — signatures permutées entre textes : tous les contrastes doivent disparaître.",
            "Négatif 5 — colonnes d'atomes permutées : le résultat ne doit pas survivre.",
            "Négatif 6 — doublons/traductions retirés : le résultat doit tenir sans les paires "
            "dont un texte est une traduction de l'autre (déjà exclues par meme_travail).",
            "Positif 1 — G1 inter-familles à date fixe : l'instrument doit voir la filiation, "
            "sinon le test d'époque n'a pas d'assise.",
            "Positif 2 — les 44 signatures de analytic_sigs_v1 doivent être reproduites par "
            "l'extracteur V14 au cosinus ≥ 0,99 (ou L2 ≤ 0,01) avant tout test.",
        ],
        "decision": {
            "alpha": 0.05,
            "correction": "Holm-Bonferroni sur P1 et P2 (m = 2).",
            "rejet_H0": (
                "H0 est rejetée si P1 ou P2 survit à Holm (p < 0,05) ET si l'effet sort du ROPE. "
                "Si les deux sont dans le ROPE, on conclut « pas d'effet d'époque détectable », "
                "pas « H0 vraie »."
            ),
            "ROPE": {
                "beta_standardise": 0.10,
                "R2_partiel": 0.02,
                "lecture": "|β| < 0,10 ou ΔR² < 0,02 = effet négligeable ; 0,10–0,30 = petit ; > 0,30 = notable.",
            },
            "manquant": (
                "Si les 60 paires ne sont pas signées, le test est « incomplet » : on ne "
                "remplace pas les signatures manquantes, on ne réduit pas l'échantillon "
                "sans le déclarer. Le noyau déjà signé est décrit, pas testé."
            ),
        },
        "inference": {
            "permutations": 2000,
            "bootstrap": 1000,
            "unite": "texte (les paires ne sont pas indépendantes)",
            "graine": GRAINE,
        },
    }


def _pre_enregistrement():
    return {
        "date": DATE_PROTOCOLE,
        "graine": GRAINE,
        "statut": "gelé avant toute lecture des 14 atomes des 26 textes non signés",
        "aveugle": (
            "La sélection des 60 paires n'utilise que annee, tradition_label, "
            "language_original, author et title. Elle n'utilise ni les 14 atomes, ni "
            "d_lex, ni cos, ni d_sig. Les 44 signatures déjà publiées ne sont lues "
            "qu'après le gel, pour compter les paires « déjà signées »."
        ),
        "regles_selection": {
            "G1": CRITERE["G1"] + " ; auteurs différents (sauf anonymes) ; pas de même titre/travail.",
            "G2": CRITERE["G2"] + " ; auteurs différents (sauf anonymes) ; pas de même titre/travail.",
            "G3": CRITERE["G3"] + " ; auteurs différents (sauf anonymes) ; pas de même titre/travail.",
            "quotes": {
                "G1": "6 GRECO–INDIAN, 4 CHINESE–GRECO, 3 CHINESE–INDIAN, 2 ABRAHAMIC–INDIAN, "
                      "1 ABRAHAMIC–CHINESE, 1 ABRAHAMIC–CLASSICAL_ORACULAR, 1 GRECO–FORMAL_LOGIC, "
                      "1 COGNITIVE_SCIENCE–FORMAL_LOGIC, 1 EUROPE_MODERN–MILLENARIAN.",
                "G2": "8 GRECO, 6 ABRAHAMIC, 3 INDIAN, 3 CHINESE.",
                "G3": "12 anglais inter-familles, 5 grec, 2 sanskrit, 1 chinois.",
            },
            "source": "sources_manifest.json et sources_coverage.json du §334 ; seules les sources ok=true.",
        },
        "exclusions": [
            "sources non acquises (ok=false) : brahma_sutra_badarayana, atharvaveda_samhita, "
            "an7_64_kodhana, aristotle_de_anima, plato_republic_fr ; aucune n'est dans les 60 paires.",
            "même texte, même titre normalisé ou même travail auteur+titre.",
            "paires déjà présentes dans un autre groupe.",
            "aucune paire n'est exclue après lecture des signatures ; le manifeste est gelé.",
        ],
        "arret": (
            "Aucun arrêt anticipé, aucun ajout de paire, aucun remplacement après lecture des "
            "résultats. Si une signature manque, le test est incomplet et le reste."
        ),
        "deviations": (
            "Toute déviation (signature manquante, source corrompue, extracteur différent) est "
            "écrite dans le JSON de résultats avec son SHA-256 et la date."
        ),
        "fichier_gelé": "reports/protocole-date.json",
    }


# ---------------------------------------------------------------------------
# Vérification du manifeste
# ---------------------------------------------------------------------------

def verifier(manifeste: dict, corpus: Corpus, silencieux=False):
    erreurs = []
    paires = manifeste.get("paires", [])
    if len(paires) != 60:
        erreurs.append(f"60 paires attendues, {len(paires)} trouvées")
    groupes = collections.Counter(p["groupe"] for p in paires)
    for g in ("G1", "G2", "G3"):
        if groupes[g] != 20:
            erreurs.append(f"{g} : 20 paires attendues, {groupes[g]} trouvées")
    vus = set()
    textes = set()
    for p in paires:
        a, b = p["a"], p["b"]
        ma, mb = corpus.meta(a), corpus.meta(b)
        if ma["annee"] is None or mb["annee"] is None:
            erreurs.append(f"{p['id']} : année manquante")
        d = abs(ma["annee"] - mb["annee"])
        if d != p["delta_annee"]:
            erreurs.append(f"{p['id']} : delta incohérent")
        if p["groupe"] == "G1" and not (d <= 10 and ma["famille"] != mb["famille"]):
            erreurs.append(f"{p['id']} : ne respecte pas G1")
        if p["groupe"] == "G2" and not (20 <= d <= 200 and ma["famille"] == mb["famille"]):
            erreurs.append(f"{p['id']} : ne respecte pas G2")
        if p["groupe"] == "G3" and not (d >= SEUIL_G3 and ma["langue"] == mb["langue"]):
            erreurs.append(f"{p['id']} : ne respecte pas G3")
        if not ma["source_ok"] or not mb["source_ok"]:
            erreurs.append(f"{p['id']} : source non acquise")
        if meme_travail(ma, mb):
            erreurs.append(f"{p['id']} : même travail")
        cle = tuple(sorted((a, b)))
        if cle in vus:
            erreurs.append(f"{p['id']} : paire dupliquée {cle}")
        vus.add(cle)
        textes.add(a); textes.add(b)
    if len(textes) != manifeste["composition"]["textes_distincts"]:
        erreurs.append("textes_distincts incohérent")
    if manifeste["composition"]["paires_distinctes"] != len(vus):
        erreurs.append("paires_distinctes incohérent")
    if not silencieux:
        if erreurs:
            print("ÉCHEC : " + str(len(erreurs)) + " erreur(s)")
            for e in erreurs:
                print(" -", e)
        else:
            print(f"OK : 60 paires uniques, 20/20/20, {len(textes)} textes, sources acquises.")
    return erreurs


def verifier_hashes(manifeste: dict):
    """Refuse de rejouer sur des artefacts qui ne sont plus ceux du manifeste gelé."""
    carte = {
        "paires334": PAIRES_334, "graphe334": GRAPHE, "signatures44": SIGNATURES_44,
        "revalidation334": REVALIDATION, "couverture": COUVERTURE,
        "manifeste_sources": MANIFESTE_SOURCES, "v150": V150,
    }
    erreurs = []
    for nom, info in manifeste.get("sources", {}).items():
        chemin = carte.get(nom) or (RACINE.parent / info["chemin"])
        if not chemin.exists():
            erreurs.append(f"{nom} : fichier absent ({chemin})")
            continue
        actuel = sha256(chemin)
        if actuel != info["sha256"]:
            erreurs.append(f"{nom} : SHA-256 {actuel} ≠ {info['sha256']}")
    if erreurs:
        for e in erreurs:
            print(" -", e)
        raise SystemExit("artefacts §334 modifiés : rejeu refusé")
    return True


# ---------------------------------------------------------------------------
# Rejeu
# ---------------------------------------------------------------------------

def _g1_controle(g1, sigs, n_perm=2000):
    """Contrôle positif : les paires inter-familles doivent être plus loin que le nul.

    Le nul permute les **signatures** entre les textes du groupe G1, puis
    recalcule la moyenne de d_sig sur les mêmes paires. Si l'instrument voit la
    filiation, la moyenne observée doit être supérieure au nul.
    """
    import numpy as np
    textes = sorted({t for x in g1 for t in (x["a"], x["b"])})
    if any(t not in sigs for t in textes):
        return {"n": len(g1), "d_sig_moyenne": None,
                "note": "signatures manquantes : contrôle positif non exécuté."}
    obs = sum(_d_sig(sigs[x["a"]], sigs[x["b"]]) for x in g1) / len(g1)
    rng = np.random.default_rng(GRAINE)
    idx = np.arange(len(textes))
    cnt = 0
    for _ in range(n_perm):
        perm = rng.permutation(idx)
        remap = {textes[i]: sigs[textes[perm[i]]] for i in range(len(textes))}
        m = sum(_d_sig(remap[x["a"]], remap[x["b"]]) for x in g1) / len(g1)
        if m >= obs - 1e-12:
            cnt += 1
    return {"n": len(g1), "d_sig_moyenne": obs, "p_permutation": (cnt + 1) / (n_perm + 1),
            "note": "nul : signatures permutées entre les textes du groupe G1."}


def _lire_signatures(chemin: pathlib.Path):
    d = lire_json(chemin)
    if isinstance(d, dict) and "signatures" in d:
        d = d["signatures"]
    if not isinstance(d, dict):
        raise SystemExit("format de signatures attendu : {id: {14 atomes}}")
    propre = {}
    for k, v in d.items():
        if not isinstance(v, dict):
            continue
        if set(v) != set(ATOMES):
            continue
        vals = [float(v[a]) for a in ATOMES]
        if any(x < -1e-9 for x in vals) or abs(sum(vals) - 1.0) > 1e-6:
            raise SystemExit(f"signature invalide pour {k} : somme={sum(vals)}")
        propre[k] = vals
    return propre


def _d_sig(x, y):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(x, y)))


def _ols(y, X):
    """Moindres carrés avec intercept ; renvoie beta, r2."""
    import numpy as np
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    X = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ beta
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return beta, r2


def _pente(y, x):
    import numpy as np
    y = np.asarray(y, float); x = np.asarray(x, float)
    if len(y) < 3 or np.std(x) == 0:
        return 0.0, 0.0
    beta, r2 = _ols(y, x)
    return float(beta[1]), float(r2)


def _permutation_p(y, x, n=2000, graine=GRAINE, bilaterale=True):
    import numpy as np
    rng = np.random.default_rng(graine)
    obs, _ = _pente(y, x)
    xs = np.asarray(x, float)
    cnt = 0
    for _ in range(n):
        rng.shuffle(xs)
        b, _ = _pente(y, xs)
        if bilaterale:
            if abs(b) >= abs(obs) - 1e-12:
                cnt += 1
        else:
            if b >= obs - 1e-12:
                cnt += 1
    return (cnt + 1) / (n + 1), obs


def rejouer(manifeste: dict, signatures_path, rapide=False, sortie=None):
    corpus = Corpus()
    verifier_hashes(manifeste)
    erreurs = verifier(manifeste, corpus, silencieux=True)
    if erreurs:
        raise SystemExit("manifeste incohérent : " + "; ".join(erreurs[:5]))
    sigs = _lire_signatures(pathlib.Path(signatures_path))
    n_perm = 300 if rapide else int(manifeste["protocole"]["inference"]["permutations"])
    paires = manifeste["paires"]
    manquantes = []
    lignes = []
    for p in paires:
        a, b = p["a"], p["b"]
        if a not in sigs or b not in sigs:
            manquantes.append(p["id"])
            continue
        d = _d_sig(sigs[a], sigs[b])
        lignes.append({"id": p["id"], "groupe": p["groupe"], "a": a, "b": b,
                       "delta_annee": p["delta_annee"], "d_sig": d,
                       "meme_famille": p["meme_famille"], "meme_langue": p["meme_langue"],
                       "d_topo": p["d_topo"]})
    resume = {
        "statut": "complet" if not manquantes else "incomplet",
        "n_paires": len(lignes),
        "n_manquantes": len(manquantes),
        "paires_manquantes": manquantes,
        "n_permutations": n_perm,
        "tests": {},
        "verdict": "non exécuté : signatures manquantes",
        "date": _dt.datetime.now().isoformat(timespec="seconds"),
    }
    if not lignes:
        resume["message"] = "Aucune paire complète : fournir les signatures V14 des 26 textes à signer."
    else:
        # descriptif toujours permis (noyau), même incomplet
        resume["descriptif"] = {}
        for g in ("G1", "G2", "G3"):
            xs = [x for x in lignes if x["groupe"] == g]
            if xs:
                resume["descriptif"][g] = {
                    "n": len(xs),
                    "d_sig_moyenne": sum(x["d_sig"] for x in xs) / len(xs),
                    "delta_annee_moyen": sum(x["delta_annee"] for x in xs) / len(xs),
                }
        if not manquantes:
            # G1 : contrôle positif inter-familles, nul par permutation des signatures
            g1 = [x for x in lignes if x["groupe"] == "G1"]
            if len(g1) >= 3:
                resume["tests"]["G1_controle_positif"] = _g1_controle(g1, sigs, n_perm)
            # G2 / G3 : pentes de date
            for g, cle in [("G2", "P1_G2"), ("G3", "P2_G3")]:
                xs = [x for x in lignes if x["groupe"] == g]
                if len(xs) >= 5:
                    y = [x["d_sig"] for x in xs]
                    dx = [x["delta_annee"] / 1000.0 for x in xs]
                    p, beta = _permutation_p(y, dx, n=n_perm, bilaterale=True)
                    b, r2 = _pente(y, dx)
                    resume["tests"][cle] = {
                        "n": len(xs), "beta_brut": b, "r2": r2, "p_permutation": p,
                        "beta_standardise": _beta_std(y, dx),
                    }
            # pooled
            if len(lignes) >= 10:
                y = [x["d_sig"] for x in lignes]
                X = [[1.0 if x["meme_famille"] else 0.0,
                      1.0 if x["meme_langue"] else 0.0,
                      x["delta_annee"] / 1000.0] for x in lignes]
                beta, r2 = _ols(y, X)
                resume["tests"]["pooled"] = {"n": len(lignes), "beta": list(map(float, beta)), "r2": r2}
            resume["verdict"] = _verdict(resume["tests"])
        else:
            resume["verdict"] = "incomplet : le noyau est décrit, pas testé (pas de p-value sur un sous-ensemble)"
    if sortie:
        chemin = pathlib.Path(sortie).resolve()
        if str(chemin).startswith(str((RACINE.parent / "Panini").resolve())):
            raise SystemExit("refus d'écrire dans Panini")
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text(json.dumps(resume, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"résultats écrits : {chemin}")
    else:
        print(json.dumps(resume, ensure_ascii=False, indent=1))
    return resume


def _beta_std(y, x):
    import numpy as np
    y = np.asarray(y, float); x = np.asarray(x, float)
    if np.std(y) == 0 or np.std(x) == 0:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def _verdict(tests):
    """Holm sur P1/P2 + ROPE (|β std| < 0,10 ou R² < 0,02 = négligeable)."""
    cles = [k for k in ("P1_G2", "P2_G3") if k in tests and tests[k].get("p_permutation") is not None]
    if not cles:
        return "non exécuté"
    ps = [tests[k]["p_permutation"] for k in cles]
    ordre = sorted(range(len(ps)), key=lambda i: ps[i])
    seuils = [0.05 / (len(ps) - k) for k in range(len(ps))]
    survivants = []
    for k, i in enumerate(ordre):
        if ps[i] <= seuils[k]:
            survivants.append(cles[i])
    if not survivants:
        return "H0 non rejetée : aucun effet d'époque détectable sur ce plan"
    for k in survivants:
        t = tests[k]
        if abs(t.get("beta_standardise") or 0) < 0.10 or (t.get("r2") or 0) < 0.02:
            return ("effet statistiquement détectable mais dans le ROPE "
                    "(|β| < 0,10 ou R² < 0,02) : négligeable en pratique")
    return "H0 rejetée (un test principal survit à Holm et sort du ROPE) — effet d'époque à examiner"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description="B1 — protocole Panini à date contrôlée")
    ap.add_argument("--verifier", action="store_true", help="vérifie le manifeste gelé")
    ap.add_argument("--construire", action="store_true", help="reconstruit le manifeste")
    ap.add_argument("--rejouer", action="store_true", help="rejoue le test avec des signatures V14")
    ap.add_argument("--signatures", type=str, default=None, help="JSON {id: {14 atomes}}")
    ap.add_argument("--manifeste", type=str, default=str(SORTIE_DEFAUT), help="manifeste gelé à rejouer")
    ap.add_argument("--sortie", type=str, default=None, help="fichier de sortie")
    ap.add_argument("--force", action="store_true", help="écrase le manifeste existant")
    ap.add_argument("--rapide", action="store_true", help="300 permutations au lieu de 2000")
    ap.add_argument("--panini", type=str, default=None, help="racine Panini (défaut ../Panini)")
    args = ap.parse_args(argv)

    global PANINI, FALS, CACHE, PAIRES_334, GRAPHE, SIGNATURES_44, REVALIDATION, COUVERTURE, MANIFESTE_SOURCES, V150
    if args.panini:
        PANINI = pathlib.Path(args.panini).resolve() / "research"
        FALS = PANINI / "nipada" / "falsification"
        CACHE = PANINI / "nipada" / "corpus" / "_cache"
        PAIRES_334 = FALS / "pairs334_axes_v1.json"
        GRAPHE = FALS / "nipada_v334_graph_v35.json"
        SIGNATURES_44 = FALS / "analytic_sigs_v1.json"
        REVALIDATION = FALS / "nipada_v334_revalidation_v35.json"
        COUVERTURE = CACHE / "sources_coverage.json"
        MANIFESTE_SOURCES = CACHE / "sources_manifest.json"
        V150 = FALS / "nipada_v150_validation.json"

    if args.construire:
        corpus = Corpus()
        manifeste = construire(corpus)
        erreurs = verifier(manifeste, corpus)
        if erreurs:
            raise SystemExit("manifeste invalide")
        sortie = pathlib.Path(args.sortie) if args.sortie else SORTIE_DEFAUT
        if str(sortie.resolve()).startswith(str((RACINE.parent / "Panini").resolve())):
            raise SystemExit("refus d'écrire dans Panini")
        if sortie.exists() and not args.force:
            raise SystemExit(f"{sortie} existe déjà ; utiliser --force pour l'écraser")
        sortie.parent.mkdir(parents=True, exist_ok=True)
        sortie.write_text(json.dumps(manifeste, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"manifeste écrit : {sortie}")
        return 0

    if args.rejouer:
        if not args.signatures:
            raise SystemExit("--rejouer exige --signatures")
        manifeste = lire_json(pathlib.Path(args.manifeste))
        sortie = args.sortie if args.sortie else RESULTATS_DEFAUT
        rejouer(manifeste, args.signatures, rapide=args.rapide, sortie=sortie)
        return 0

    # défaut : vérifier
    corpus = Corpus()
    manifeste = lire_json(pathlib.Path(args.manifeste))
    erreurs = verifier(manifeste, corpus)
    if erreurs:
        return 1
    print(f"commit Drave : {manifeste.get('commit_drave')}")
    print(f"commit Panini lu : {manifeste.get('commit_panini', {}).get('lu')}")
    print(f"paires : {len(manifeste['paires'])} ; textes : {manifeste['composition']['textes_distincts']} ; "
          f"à signer : {len(manifeste['a_signer'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
