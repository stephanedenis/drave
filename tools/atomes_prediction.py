#!/usr/bin/env python3
"""B2 — les 14 atomes de Panini prédisent-ils les niveaux de Drave ?

Ce que le dispositif mesure
---------------------------
44 œuvres du §334 de Panini ont une signature V14 (14 parts, somme 1) calculée
par Panini sur les **10 000 premiers jetons** du fichier source. On mesure, pour
chaque œuvre, des statistiques de **niveau** avec le bloc linguistique de Drave
(heuristique CPU) :

  - POS : distribution des classes, entropie ;
  - syntagmes : densité par phrase, longueur, types, profondeur ;
  - attachement : taux d'attachement, distance moyenne/mediane, part de GP ;
  - et, en secondaire, graphème, mot, phrase, pragmatique, discours.

Puis on demande aux 14 atomes (transformés en CLR) de prédire ces statistiques
par **validation croisée leave-one-work-out groupée** (les doublons de texte
restent dans le même pli), avec deux contrôles :

  1. **permutation des colonnes** : chaque colonne d'atome est permutée
     indépendamment ; la prédiction doit tomber au hasard ;
  2. **contrôle de date** : l'année de composition (graphe v35 de Panini) est
     un prédicteur concurrent ; on compare le modèle atomes, le modèle date et
     le modèle joint, et on permute les années.

Aucune écriture dans Panini : les sources sont lues en lecture seule.

Usage
-----
  python3 tools/atomes_prediction.py --mesurer          # cache les mesures de niveau
  python3 tools/atomes_prediction.py --analyser         # écrit reports/atomes-prediction.json
  python3 tools/atomes_prediction.py --tout             # les deux
  python3 tools/atomes_prediction.py --rapide --tout    # 500 permutations (mise au point)
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import html
import json
import math
import pathlib
import re
import subprocess
import sys
import time
from html.parser import HTMLParser

import numpy as np
from scipy import stats

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "tools"))

from bloc_linguistique import Heuristique  # noqa: E402
import panini_334 as panini  # noqa: E402

SORTIE_MESURES = RACINE / "reports" / "atomes-prediction-mesures.json"
SORTIE = RACINE / "reports" / "atomes-prediction.json"
GRAINE = 20261115

# ---------------------------------------------------------------------------
# 0. Petits outils
# ---------------------------------------------------------------------------

MOTS_VIDES = set(
    "the of and to in a is that it for as with was on be by this are or from at not "
    "have an but they you which we can all has their been if will would there one what "
    "when who so no more about his her she he them its our your my me i do does did "
    "le la les de des du un une et en est que qui dans pour pas sur au aux ce cette ces "
    "il elle ils elles nous vous se sa son ses leur leurs plus ou mais ne par avec".split()
)
MARQUE_BALISE = re.compile(
    r"^(?:data-|class|href|src|span|div|px|hover|http|www|id=|style|button|aria-|svg|"
    r"path|xml|html|body|head|script|style|[{}<>])",
    re.I,
)
MOT = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:['’\-][A-Za-zÀ-ÖØ-öø-ÿ]+)*")
MOT_SIMPLE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+")


class _StripHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.skip += 1
        if tag in ("p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6",
                   "section", "article", "blockquote"):
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self.skip:
            self.skip -= 1
        if tag in ("p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6",
                   "section", "article", "blockquote"):
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def strip_html(texte: str) -> str:
    p = _StripHTML()
    try:
        p.feed(texte)
        p.close()
    except Exception:
        return re.sub(r"<[^>]+>", " ", texte)
    return "".join(p.out)


def lire_source(chemin: pathlib.Path) -> tuple[str, dict]:
    """Lit une source et retire l'appareil Gutenberg / HTML / wiki.

    Les 44 fichiers sont **sur une seule ligne** (aucun \\n) : on ne peut donc
    pas filtrer par ligne. On retire les balises, les modèles wiki, les URL et
    les caractères de contrôle, puis on filtre les phrases non-prose.
    """
    brut = chemin.read_bytes()
    meta = {"octets": len(brut), "format": "texte"}
    if brut[:4] == b"%PDF":
        meta["format"] = "pdf"
        try:
            r = subprocess.run(["pdftotext", "-raw", str(chemin), "-"],
                               capture_output=True, text=True, timeout=120)
            texte = r.stdout
        except Exception:
            texte = ""
        meta["extrait"] = bool(texte.strip())
        if not texte.strip():
            return "", meta
    else:
        texte = brut.decode("utf-8-sig", errors="replace")
    texte = texte.replace("\r\n", "\n").replace("\r", "\n")

    # Gutenberg : les marqueurs sont sur la même ligne que le texte.
    m1 = re.search(r"\*\*\*\s*START OF.*?\*\*\*", texte, re.I | re.S)
    m2 = re.search(r"\*\*\*\s*END OF.*?\*\*\*", texte, re.I | re.S)
    if m1:
        fin = m2.start() if (m2 and m2.start() > m1.end()) else len(texte)
        texte = texte[m1.end():fin]
        meta["gutenberg"] = True

    if re.search(r"<html|<!doctype|<head|<body|<div|<p[ >]", texte[:20_000], re.I):
        texte = strip_html(texte)
        meta["html"] = True
    texte = re.sub(r"<script.*?</script>", " ", texte, flags=re.I | re.S)
    texte = re.sub(r"<style.*?</style>", " ", texte, flags=re.I | re.S)

    for _ in range(10):
        nouveau = re.sub(r"\{\{[^{}]*\}\}", "", texte)
        if nouveau == texte:
            break
        texte = nouveau
    texte = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", texte)
    texte = re.sub(r"\{[^{}]*\}", " ", texte)
    texte = re.sub(r"<[^>]{1,200}>", " ", texte)
    texte = html.unescape(texte)
    texte = re.sub(r"https?://\S+", " ", texte)
    texte = "".join(ch if ch in "\n\t" or ord(ch) >= 32 else " " for ch in texte)
    texte = re.sub(r"[ \t]+", " ", texte)
    texte = re.sub(r"\n\s*\n+", "\n", texte)
    return texte.strip(), meta


def filtrer_prose(texte: str) -> str:
    """Garde les phrases qui ressemblent à de la prose (mots vides, lettres).

    Le filtre retire le JS/CSS, les tables des matières numériques et les
    pages de navigation que les sources brutes contiennent. Il est **déclaré**
    et le taux de rétention est publié par œuvre.
    """
    phrases = re.split(r"(?<=[.!?;:])\s+", texte)
    garde = []
    for p in phrases:
        mots = MOT_SIMPLE.findall(p)
        if len(mots) < 5:
            continue
        stop = sum(1 for m in mots if m.lower() in MOTS_VIDES) / len(mots)
        alpha = sum(1 for c in p if c.isalpha()) / max(1, len(p))
        if stop >= 0.12 and alpha >= 0.55:
            garde.append(p)
    sortie = " ".join(garde).strip()
    if len(sortie) < 2_000:
        return texte.strip()
    return sortie


def qualite_fenetre_signature(texte: str) -> dict:
    """Qualité des 10 000 premiers jetons, la fenêtre exacte de Panini."""
    jetons = texte.split()[:10_000]
    n = len(jetons)
    if not n:
        return {"n_jetons": 0, "stopwords": 0.0, "balises": 0.0, "lettres": 0.0,
                "propre": False}
    stop = sum(1 for x in jetons if re.sub(r"\W", "", x.lower()) in MOTS_VIDES) / n
    balises = sum(1 for x in jetons if MARQUE_BALISE.search(x)) / n
    lettres = sum(sum(1 for c in x if c.isalpha()) for x in jetons) / max(
        1, sum(len(x) for x in jetons))
    return {
        "n_jetons": n,
        "stopwords": round(stop, 4),
        "balises": round(balises, 4),
        "lettres": round(lettres, 4),
        "propre": bool(stop >= 0.15 and balises <= 0.05 and lettres >= 0.75),
    }


def entropie(compte: collections.Counter | dict) -> float:
    total = sum(compte.values())
    if total <= 0:
        return float("nan")
    return float(-sum((v / total) * math.log(v / total, 2) for v in compte.values() if v))


def fenetres(texte: str, n: int = 6, taille: int = 10_000) -> list[str]:
    """Fenêtres non chevauchantes de `taille` caractères, ou le texte entier."""
    if len(texte) <= n * taille:
        return [texte]
    debuts = np.linspace(0, len(texte) - taille, n).astype(int)
    sorties = []
    for d in debuts:
        d = int(d)
        if d > 0:
            j = texte.find(" ", d)
            if 0 <= j < d + 200:
                d = j + 1
        f = min(len(texte), d + taille)
        if f < len(texte):
            j = texte.rfind(" ", d, f)
            if j > d + taille // 2:
                f = j
        sortie = texte[d:f].strip()
        if len(sortie) > 1_000:
            sorties.append(sortie)
    return sorties or [texte]


# ---------------------------------------------------------------------------
# 1. Mesures de niveau
# ---------------------------------------------------------------------------

POS_ORDRE = ["NOUN", "VERB", "AUX", "ADJ", "ADV", "PRON", "DET", "PREP",
             "CONJ", "NUM", "PONCT"]


def _norm(s: str) -> str:
    return re.sub(r"\W+", "", s.lower())


def mesurer_oeuvre(texte_prose: str, langue: str) -> dict:
    """Analyse les fenêtres et agrège les compteurs de niveau."""
    h = Heuristique()
    pos = collections.Counter()
    syn_types = collections.Counter()
    roles = collections.Counter()
    pragma = collections.Counter()
    phrase_type = collections.Counter()
    phrase_neg = 0
    phrase_mod = 0
    n_phrases = 0
    n_syn = 0
    n_syn_len = 0
    profondeur = []
    n_att = 0
    n_att_cible = 0
    n_att_introuvable = 0
    n_att_self = 0
    distances = []
    n_mots = 0
    n_lettres_mots = 0
    n_lettres_chars = 0
    n_ponct = 0
    n_alpha_num = 0
    att_types = collections.Counter()
    chars = collections.Counter()
    types_mots = collections.Counter()
    n_connecteurs = 0
    n_fenetres = 0
    erreurs = []

    for fen in fenetres(texte_prose):
        try:
            ann = h.analyser(fen, langue)
            j = ann.json()
        except Exception as e:  # une fenêtre qui casse ne doit pas perdre l'œuvre
            erreurs.append(type(e).__name__)
            continue
        if j.get("refus"):
            erreurs.append(j["refus"])
            continue
        n_fenetres += 1
        etiq = j["etiquettes"]

        # tokens mots (hors ponctuation) pour les distances d'attachement
        mots = [(e["debut"], _norm(e["valeur"])) for e in etiq
                if e["niveau"] == "mot" and e["type"] == "mot"]
        debuts = [m[0] for m in mots]
        par_mot = collections.defaultdict(list)
        for idx, (_, m) in enumerate(mots):
            par_mot[m].append(idx)

        for e in etiq:
            niv = e["niveau"]
            if niv == "pos":
                pos[e["type"]] += 1
            elif niv == "syntagme":
                n_syn += 1
                syn_types[e["type"]] += 1
                roles[e["meta"].get("role", "?")] += 1
                profondeur.append(int(e["meta"].get("niveau", 0) or 0))
                lg = len(MOT.findall(e["valeur"]))
                n_syn_len += lg
                att = e["meta"].get("attachement")
                if att and att.get("cible"):
                    n_att += 1
                    att_types[e["type"]] += 1
                    cible = _norm(att["cible"])
                    occ = par_mot.get(cible, [])
                    if not occ:
                        n_att_introuvable += 1
                        continue
                    i0 = int(np.searchsorted(debuts, e["debut"], side="left"))
                    i1 = int(np.searchsorted(debuts, e["fin"], side="right")) - 1
                    d = min(max(0, k - i1, i0 - k) for k in occ)
                    if d == 0:
                        n_att_self += 1
                        continue
                    n_att_cible += 1
                    distances.append(d)
            elif niv == "phrase":
                if e["type"] == "type":
                    n_phrases += 1
                    phrase_type[e["valeur"]] += 1
                elif e["type"] == "négation" and e["valeur"] == "oui":
                    phrase_neg += 1
                elif e["type"] == "modalité" and e["valeur"] == "oui":
                    phrase_mod += 1
            elif niv == "pragmatique" and e["type"] == "acte":
                pragma[e["valeur"]] += 1
            elif niv == "discours" and e["type"] == "connecteur":
                n_connecteurs += 1
            elif niv == "mot" and e["type"] == "mot":
                v = e["valeur"]
                n_mots += 1
                n_lettres_mots += sum(1 for c in v if c.isalpha())
                types_mots[v.lower()] += 1
            elif niv == "graphème":
                for c in e["valeur"]:
                    if c.isalpha():
                        chars[c.lower()] += 1

        for c in fen:
            if c.isalpha():
                n_alpha_num += 1
                n_lettres_chars += 1
            elif c.isdigit():
                n_alpha_num += 1
            elif not c.isspace():
                n_ponct += 1

    total_pos = sum(pos.values())
    total_pos_hp = sum(v for k, v in pos.items() if k != "PONCT")
    total_syn = max(1, n_syn)
    total_pragma = max(1, sum(pragma.values()))
    total_phrase = max(1, n_phrases)
    total_att = max(1, n_att)
    total_att_cible = max(1, n_att_cible)
    n_mots_total = max(1, n_mots)
    n_alpha_total = max(1, n_alpha_num)

    m = {
        "n_fenetres": n_fenetres,
        "n_mots": n_mots,
        "n_phrases": n_phrases,
        "n_syntagmes": n_syn,
        "n_attachements": n_att,
        "n_attachements_cible": n_att_cible,
        "erreurs": erreurs,
        # graphème
        "graph_lettres": n_lettres_chars / max(1, n_lettres_chars + n_ponct),
        "graph_ponctuation": n_ponct / max(1, n_ponct + n_alpha_num),
        "graph_entropie": entropie(chars),
        # mot
        "mot_longueur": n_lettres_mots / n_mots_total,
        "mot_ttr": len(types_mots) / n_mots_total,
        "mot_hapax": sum(1 for v in types_mots.values() if v == 1) / n_mots_total,
        # pos
        "pos_entropie": entropie({k: v for k, v in pos.items() if k != "PONCT"}),
        "pos_part_nom": pos.get("NOUN", 0) / max(1, total_pos_hp),
        "pos_part_verbe": (pos.get("VERB", 0) + pos.get("AUX", 0)) / max(1, total_pos_hp),
        "pos_part_adj": pos.get("ADJ", 0) / max(1, total_pos_hp),
        "pos_part_adv": pos.get("ADV", 0) / max(1, total_pos_hp),
        "pos_part_pron": pos.get("PRON", 0) / max(1, total_pos_hp),
        "pos_part_det": pos.get("DET", 0) / max(1, total_pos_hp),
        "pos_part_prep": pos.get("PREP", 0) / max(1, total_pos_hp),
        "pos_part_conj": pos.get("CONJ", 0) / max(1, total_pos_hp),
        "pos_part_num": pos.get("NUM", 0) / max(1, total_pos_hp),
        "pos_ponct": pos.get("PONCT", 0) / max(1, total_pos),
        # syntagmes
        "syn_par_phrase": n_syn / total_phrase,
        "syn_longueur": n_syn_len / total_syn,
        "syn_part_gn": syn_types.get("GN", 0) / total_syn,
        "syn_part_gv": syn_types.get("GV", 0) / total_syn,
        "syn_part_gp": syn_types.get("GP", 0) / total_syn,
        "syn_part_rel": syn_types.get("REL", 0) / total_syn,
        "syn_part_sub": syn_types.get("SUB", 0) / total_syn,
        "syn_profondeur": float(np.mean(profondeur)) if profondeur else float("nan"),
        # attachement
        "att_taux": n_att_cible / total_att,
        "att_distance": float(np.mean(distances)) if distances else float("nan"),
        "att_distance_mediane": float(np.median(distances)) if distances else float("nan"),
        "att_part_gp": att_types.get("GP", 0) / total_att,
        "att_introuvable": n_att_introuvable / total_att,
        "att_self": n_att_self / total_att,
        # phrase
        "phrase_longueur": n_mots_total / total_phrase,
        "phrase_negation": phrase_neg / total_phrase,
        "phrase_modalite": phrase_mod / total_phrase,
        "phrase_interrogative": phrase_type.get("interrogative", 0) / total_phrase,
        # pragmatique
        "pragma_assertion": pragma.get("assertion", 0) / total_pragma,
        "pragma_entropie": entropie(pragma),
        # discours
        "disc_connecteurs_1000": n_connecteurs / n_mots_total * 1000,
        # document : non mesurable (sources sur une ligne)
        "doc_paragraphes_1000": float("nan"),
    }
    return m


# ---------------------------------------------------------------------------
# 2. Chargement des données
# ---------------------------------------------------------------------------

def charger_donnees(forcer: bool = False) -> dict:
    if SORTIE_MESURES.exists() and not forcer:
        return json.loads(SORTIE_MESURES.read_text(encoding="utf-8"))

    paires, graphe, signatures, revalidation, textes, ids_paires, ids_signes, audit = panini.charger()
    sources = panini.PANINI / "nipada" / "corpus" / "_cache" / "sources"
    oeuvres = []
    t0 = time.time()
    for k, tid in enumerate(ids_signes, 1):
        chemin = sources / f"{tid}.txt"
        brut, meta = lire_source(chemin)
        # la fenêtre de Panini est celle des 10 000 premiers jetons du fichier
        # **brut**, avant notre nettoyage : on la mesure telle quelle.
        try:
            brut_qualite = chemin.read_text(encoding="utf-8", errors="replace")
        except Exception:
            brut_qualite = ""
        signature_q = qualite_fenetre_signature(brut_qualite)
        signature_q["assez_long"] = bool(signature_q["n_jetons"] >= 1000)
        signature_q["utilisable"] = bool(signature_q["propre"] and signature_q["assez_long"])
        prose = filtrer_prose(brut) if brut else ""
        n_mots_prose = len(MOT_SIMPLE.findall(prose))
        langue = "fr" if textes[tid]["langue_source"] == "fra" else "en"
        mesures = mesurer_oeuvre(prose, langue) if n_mots_prose >= 200 else {}
        if mesures:
            mesures["n_mots_mesures"] = mesures.get("n_mots", 0)
            mesures["n_mots_prose"] = n_mots_prose
        oeuvres.append({
            "id": tid,
            "titre": textes[tid]["titre"],
            "annee": textes[tid]["annee"],
            "tradition": textes[tid]["tradition_large"],
            "langue_source": textes[tid]["langue_source"],
            "langue_forcee": langue,
            "signature": [float(signatures[tid][a]) for a in panini.ATOMES],
            "qualite_source": signature_q,
            "n_mots_source": textes[tid]["mots_source"],
            "n_mots_prose": n_mots_prose,
            "meta_source": meta,
            "mesures": mesures,
        })
        print(f"  [{k:2d}/44] {tid:<32} mots={n_mots_prose:6d} "
              f"propre={signature_q['propre']} syn={mesures.get('n_syntagmes', 0):5d} "
              f"({time.time()-t0:5.1f}s)", flush=True)

    data = {
        "version": "1.0",
        "date": "2026-11-15",
        "source": str(panini.SIGNATURES),
        "atomes": panini.ATOMES,
        "oeuvres": oeuvres,
    }
    SORTIE_MESURES.write_text(json.dumps(data, ensure_ascii=False, indent=1),
                              encoding="utf-8")
    return data


# ---------------------------------------------------------------------------
# 3. Statistique : ridge LOOCV groupée, dates, permutations
# ---------------------------------------------------------------------------

def clr(X: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    L = np.log(np.clip(X, eps, None))
    return L - L.mean(axis=1, keepdims=True)


def _groupes(oeuvres: list[dict]) -> list[list[int]]:
    """Les doublons de texte (même sha256) restent dans le même pli."""
    par_id = collections.defaultdict(list)
    for i, o in enumerate(oeuvres):
        par_id[o["id"]].append(i)
    # les deux paires connues : gorgias/gorgias_jowett, meno/meno_jowett
    paires = [("plato_gorgias", "plato_gorgias_jowett"),
              ("plato_meno", "plato_meno_jowett")]
    vus = set()
    groupes = []
    for a, b in paires:
        idx = [i for i, o in enumerate(oeuvres) if o["id"] in (a, b)]
        if idx:
            groupes.append(idx)
            vus.update(idx)
    for i in range(len(oeuvres)):
        if i not in vus:
            groupes.append([i])
    return groupes


def _standardiser(Xtr, Xte):
    mx = Xtr.mean(0)
    sx = Xtr.std(0)
    sx[sx == 0] = 1.0
    return (Xtr - mx) / sx, (Xte - mx) / sx, mx, sx


def cv_ridge_multi(X, Y, lambdas, groupes=None, dates=None, mode="atomes",
                   permutation=None, rng=None):
    """Ridge multi-sorties, LOOCV groupée.

    mode : "atomes" | "date" | "joint".
    dates : matrice (n, d) de la date (déjà construite), requise pour date/joint.
    permutation : None | "colonnes" | "lignes" (pour le contrôle négatif).
    Retourne (preds (n,k), r2 (k,), lambdas_choisis (n,)).
    """
    X = np.array(X, float)
    Y = np.array(Y, float)
    n, k = Y.shape
    if permutation == "colonnes":
        X = X.copy()
        for j in range(X.shape[1]):
            X[:, j] = X[rng.permutation(n), j]
    elif permutation == "lignes":
        X = X[rng.permutation(n)].copy()
    preds = np.full((n, k), np.nan)
    lambdas_choisis = []
    if groupes is None:
        groupes = [[i] for i in range(n)]
    for g in groupes:
        te = np.array(g, dtype=int)
        tr = np.setdiff1d(np.arange(n), te)
        Xtr, Xte = X[tr], X[te]
        Ytr = Y[tr]
        Dtr = dates[tr] if dates is not None else None
        Dte = dates[te] if dates is not None else None
        if mode in ("date", "joint") and Dtr is None:
            raise ValueError("dates requises")
        if mode == "date":
            B, *_ = np.linalg.lstsq(Dtr, Ytr, rcond=None)
            preds[te] = Dte @ B
            continue
        if mode == "joint":
            B, *_ = np.linalg.lstsq(Dtr, Ytr, rcond=None)
            Ytr_r = Ytr - Dtr @ B
            Bx, *_ = np.linalg.lstsq(Dtr, Xtr, rcond=None)
            Xtr_r = Xtr - Dtr @ Bx
            Xte_r = Xte - Dte @ Bx
            Xtr_s, Xte_s, mx, sx = _standardiser(Xtr_r, Xte_r)
            # moyenne **globale** : centrer sur la moyenne d'entraînement rendrait
            # la prédiction LOOCV artificiellement anti-corrélée à la valeur tenue
            # à l'écart (le retrait d'un y élevé abaisse la moyenne du pli).
            my = Yr.mean(0)
            Yc = Ytr_r - my
        else:
            Xtr_s, Xte_s, mx, sx = _standardiser(Xtr, Xte)
            my = Y.mean(0)
            Yc = Ytr - my
        U, s, Vt = np.linalg.svd(Xtr_s, full_matrices=False)
        f = s[None, :] ** 2 / (s[None, :] ** 2 + lambdas[:, None])  # (L,p)
        # (L,n,k)
        F = f[:, :, None] * (U.T @ Yc)[None, :, :]
        yhat = np.einsum("np,lpk->lnk", U, F)
        h = f @ (U ** 2).T  # (L,n)
        res = (Yc[None, :, :] - yhat) / (1 - h)[:, :, None]
        sse = (res ** 2).sum(axis=1)  # (L,k)
        for j in range(k):
            lam = lambdas[int(np.argmin(sse[:, j]))]
            coef = Vt.T @ ((s / (s ** 2 + lam))[:, None] * (U.T @ Yc[:, j])[:, None])
            pred = Xte_s @ coef.ravel() + my[j]
            if mode == "joint":
                pred = Dte @ B[:, j] + pred
            preds[te, j] = pred
            lambdas_choisis.append(float(lam))
    r2 = 1 - ((Y - preds) ** 2).sum(0) / ((Y - Y.mean(0)) ** 2).sum(0)
    return preds, r2, np.array(lambdas_choisis)


def _design_date(annees: np.ndarray, degre: int = 1) -> np.ndarray:
    z = (annees - np.nanmean(annees)) / (np.nanstd(annees) or 1)
    colonnes = [np.ones(len(z)), z]
    for d in range(2, degre + 1):
        colonnes.append(z ** d)
    return np.column_stack(colonnes)


def _p_perm(null, observe, sens="superieur") -> float:
    null = np.asarray(null, float)
    if sens == "superieur":
        return float((1 + np.sum(null >= observe)) / (1 + len(null)))
    return float((1 + np.sum(null <= observe)) / (1 + len(null)))


def _holm(p):
    p = np.asarray(p, float)
    ordre = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    courant = 0.0
    for rang, i in enumerate(ordre):
        courant = max(courant, min(1.0, (m - rang) * p[i]))
        adj[i] = courant
    return adj


def _bh(p):
    p = np.asarray(p, float)
    ordre = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    courant = 1.0
    for rang in range(m - 1, -1, -1):
        i = ordre[rang]
        courant = min(courant, p[i] * m / (rang + 1))
        adj[i] = courant
    return adj


# ---------------------------------------------------------------------------
# 4. Analyse
# ---------------------------------------------------------------------------

METRIQUES = [
    "graph_lettres", "graph_ponctuation", "graph_entropie",
    "mot_longueur", "mot_ttr", "mot_hapax",
    "pos_entropie", "pos_part_nom", "pos_part_verbe", "pos_part_adj",
    "pos_part_adv", "pos_part_pron", "pos_part_det", "pos_part_prep",
    "pos_part_conj", "pos_part_num", "pos_ponct",
    "syn_par_phrase", "syn_longueur", "syn_part_gn", "syn_part_gv",
    "syn_part_gp", "syn_part_rel", "syn_part_sub", "syn_profondeur",
    "att_taux", "att_distance", "att_distance_mediane", "att_part_gp",
    "att_introuvable", "att_self",
    "phrase_longueur", "phrase_negation", "phrase_modalite", "phrase_interrogative",
    "pragma_assertion", "pragma_entropie", "disc_connecteurs_1000",
]

FAMILLES = {
    "POS": ["pos_entropie", "pos_part_nom", "pos_part_verbe", "pos_part_adj",
            "pos_part_adv", "pos_part_pron", "pos_part_det", "pos_part_prep",
            "pos_part_conj", "pos_part_num", "pos_ponct"],
    "SYNTAGMES": ["syn_par_phrase", "syn_longueur", "syn_part_gn", "syn_part_gv",
                  "syn_part_gp", "syn_part_rel", "syn_part_sub", "syn_profondeur"],
    "ATTACHEMENT": ["att_taux", "att_distance", "att_distance_mediane", "att_part_gp"],
}
PRIMAIRES = list(FAMILLES)


def _filtre_cohorte(o: dict, cohorte: str) -> bool:
    """Cohortes pré-déclarées. La cohorte « mesurable » est le mandat (44 œuvres
    dont 36 mesurables) ; « utilisable » retire les sources dont la fenêtre de
    signature n'est pas de la prose ; « strict » exige en plus ≥ 2 000 mots
    mesurés."""
    if not o.get("mesures") or not np.isfinite(o["mesures"].get("pos_entropie", np.nan)):
        return False
    q = o["qualite_source"]
    if cohorte == "mesurable":
        return True
    if cohorte == "utilisable":
        return bool(q.get("utilisable"))
    if cohorte == "propre":
        return bool(q.get("propre"))
    if cohorte == "propre_500":
        return bool(q.get("propre")) and o["mesures"].get("n_mots_mesures", 0) >= 500
    if cohorte == "strict":
        return bool(q.get("utilisable")) and o["mesures"].get("n_mots_mesures", 0) >= 2000
    if cohorte == "strict_plus":
        return bool(q.get("utilisable")) and o["mesures"].get("n_mots_mesures", 0) >= 5000
    raise ValueError(f"cohorte inconnue : {cohorte}")


def _r2(y, p) -> float:
    den = ((y - y.mean()) ** 2).sum()
    if den <= 0:
        return float("nan")
    return float(1 - ((y - p) ** 2).sum() / den)


def _rho(y, p) -> float:
    if len(y) < 3 or np.std(y) == 0 or np.std(p) == 0:
        return float("nan")
    return float(stats.spearmanr(y, p).statistic)


def cv_residuel(X, Y, D, lambdas, groupes):
    """Atomes sur les résidus de la date (ajustement de date in-sample).

    Le même ajustement est refait sous permutation de la date : le null teste
    « les atomes prédisent-ils ce que la date ne dit pas ? ».
    """
    B, *_ = np.linalg.lstsq(D, Y, rcond=None)
    Yr = Y - D @ B
    Bx, *_ = np.linalg.lstsq(D, X, rcond=None)
    Xr = X - D @ Bx
    preds, r2, lam = cv_ridge_multi(Xr, Yr, lambdas, groupes=groupes)
    return preds, Yr, r2, lam


def analyser(data: dict, cohorte: str = "mesurable", n_perm_col: int = 2000,
             n_perm_date: int = 1000, degre_date: int = 1) -> dict:
    oeuvres = data["oeuvres"]
    sous = [o for o in oeuvres if _filtre_cohorte(o, cohorte)]
    n = len(sous)
    if n < 8:
        raise ValueError(f"cohorte {cohorte} : n={n} trop petit")
    Xfull = clr(np.array([o["signature"] for o in sous], float))
    # le CLR de 14 parts est de rang 13 (somme des logs nulle) : on retire la
    # dernière colonne pour une base pleine, de condition ~28.
    X = Xfull[:, :-1]
    annees = np.array([o["annee"] for o in sous], float)
    D = _design_date(annees, degre_date)
    noms = [k for k in METRIQUES if all(k in o["mesures"] for o in sous)]
    Y = np.array([[o["mesures"].get(k, np.nan) for k in noms] for o in sous], float)
    nan_par_metrique = {k: int(np.sum(~np.isfinite(Y[:, j]))) for j, k in enumerate(noms)}
    for j in range(Y.shape[1]):
        col = Y[:, j]
        if np.any(~np.isfinite(col)):
            col[~np.isfinite(col)] = np.nanmean(col)
            Y[:, j] = col
    # une métrique constante n'a pas de prédiction mesurable
    garde = [j for j in range(Y.shape[1]) if np.std(Y[:, j]) > 0]
    ecartees = [noms[j] for j in range(Y.shape[1]) if j not in garde]
    noms = [noms[j] for j in garde]
    Y = Y[:, garde]

    groupes = _groupes(sous)
    lambdas = np.logspace(-2, 3, 30)
    rng = np.random.default_rng(GRAINE)

    # --- observé ---------------------------------------------------------
    print(f"  [{cohorte}] n={n} : CV atomes…", flush=True)
    preds_atomes, r2_atomes, lam_atomes = cv_ridge_multi(X, Y, lambdas, groupes=groupes)
    rho_atomes = np.array([_rho(Y[:, j], preds_atomes[:, j]) for j in range(len(noms))])

    print(f"  [{cohorte}] : date in-sample + atomes sur résidus…", flush=True)
    B, *_ = np.linalg.lstsq(D, Y, rcond=None)
    Ydate = D @ B
    r2_date_in = np.array([_r2(Y[:, j], Ydate[:, j]) for j in range(len(noms))])
    preds_res, Yr, r2_res, _ = cv_residuel(X, Y, D, lambdas, groupes)
    rho_res = np.array([_rho(Yr[:, j], preds_res[:, j]) for j in range(len(noms))])

    # --- permutations ----------------------------------------------------
    print(f"  [{cohorte}] permutations colonnes ({n_perm_col})…", flush=True)
    null_col = np.empty((n_perm_col, len(noms)))
    null_col_rho = np.empty((n_perm_col, len(noms)))
    t0 = time.time()
    for b in range(n_perm_col):
        p, r2, _ = cv_ridge_multi(X, Y, lambdas, groupes=groupes,
                                  permutation="colonnes", rng=rng)
        null_col[b] = r2
        null_col_rho[b] = [_rho(Y[:, j], p[:, j]) for j in range(len(noms))]
        if (b + 1) % 200 == 0:
            print(f"    {b+1}/{n_perm_col} ({time.time()-t0:5.1f}s)", flush=True)

    print(f"  [{cohorte}] permutations date ({n_perm_date})…", flush=True)
    null_res = np.empty((n_perm_date, len(noms)))
    null_res_rho = np.empty((n_perm_date, len(noms)))
    null_date_in = np.empty((n_perm_date, len(noms)))
    for b in range(n_perm_date):
        annee_p = rng.permutation(annees)
        Dp = _design_date(annee_p, degre_date)
        Bp, *_ = np.linalg.lstsq(Dp, Y, rcond=None)
        Ydp = Dp @ Bp
        null_date_in[b] = [_r2(Y[:, j], Ydp[:, j]) for j in range(len(noms))]
        p, Yrp, r2, _ = cv_residuel(X, Y, Dp, lambdas, groupes)
        null_res[b] = r2
        null_res_rho[b] = [_rho(Yrp[:, j], p[:, j]) for j in range(len(noms))]
        if (b + 1) % 200 == 0:
            print(f"    date {b+1}/{n_perm_date} ({time.time()-t0:5.1f}s)", flush=True)

    # --- résultats par métrique -----------------------------------------
    metriques = {}
    for j, k in enumerate(noms):
        metriques[k] = {
            "famille": next((f for f, ks in FAMILLES.items() if k in ks), "autre"),
            "n": n,
            "r2_atomes": round(float(r2_atomes[j]), 4),
            "rho_cv": round(float(rho_atomes[j]), 4),
            "p_col": _p_perm(null_col[:, j], r2_atomes[j]),
            "r2_exces": round(float(r2_atomes[j] - np.nanmean(null_col[:, j])), 4),
            "p_rho_col": _p_perm(null_col_rho[:, j], rho_atomes[j]),
            "rho_exces": round(float(rho_atomes[j] - np.nanmean(null_col_rho[:, j])), 4),
            "r2_date_in": round(float(r2_date_in[j]), 4),
            "p_date_in": _p_perm(null_date_in[:, j], r2_date_in[j]),
            "r2_resid": round(float(r2_res[j]), 4),
            "rho_resid": round(float(rho_res[j]), 4),
            "p_resid": _p_perm(null_res[:, j], r2_res[j]),
            "r2_res_exces": round(float(r2_res[j] - np.nanmean(null_res[:, j])), 4),
            "p_rho_resid": _p_perm(null_res_rho[:, j], rho_res[j]),
            "rho_res_exces": round(float(rho_res[j] - np.nanmean(null_res_rho[:, j])), 4),
            "part_atomes": round(float(r2_res[j] * (1 - r2_date_in[j])), 4)
            if np.isfinite(r2_res[j]) and np.isfinite(r2_date_in[j]) else None,
            "lambda_median": round(float(np.median(lam_atomes)), 4),
            "nan": nan_par_metrique[k],
        }
    # BH sur les métriques
    for cle in ("p_col", "p_rho_col", "p_resid", "p_rho_resid", "p_date_in"):
        ps = [metriques[k][cle] for k in noms]
        for k, p in zip(noms, _bh(ps)):
            metriques[k][cle + "_bh"] = round(float(p), 4)

    # --- familles --------------------------------------------------------
    familles = {}
    for f, ks in FAMILLES.items():
        js = [j for j, k in enumerate(noms) if k in ks]
        if not js:
            continue
        obs = float(np.mean(r2_atomes[js]))
        null = null_col[:, js].mean(1)
        obs_rho = float(np.nanmean(rho_atomes[js]))
        null_rho = np.nanmean(null_col_rho[:, js], axis=1)
        obs_res = float(np.mean(r2_res[js]))
        null_r = null_res[:, js].mean(1)
        obs_date = float(np.mean(r2_date_in[js]))
        null_d = null_date_in[:, js].mean(1)
        familles[f] = {
            "metriques": ks,
            "r2_atomes_moyen": round(obs, 4),
            "p_col": _p_perm(null, obs),
            "r2_exces_moyen": round(obs - float(np.nanmean(null)), 4),
            "rho_cv_moyen": round(obs_rho, 4),
            "p_rho_col": _p_perm(null_rho, obs_rho),
            "rho_exces_moyen": round(obs_rho - float(np.nanmean(null_rho)), 4),
            "r2_date_in_moyen": round(obs_date, 4),
            "p_date_in": _p_perm(null_d, obs_date),
            "r2_resid_moyen": round(obs_res, 4),
            "p_resid": _p_perm(null_r, obs_res),
            "r2_res_exces_moyen": round(obs_res - float(np.nanmean(null_r)), 4),
        }
    pf = [familles[f]["p_col"] for f in PRIMAIRES if f in familles]
    for f, p in zip([f for f in PRIMAIRES if f in familles], _holm(pf)):
        familles[f]["p_col_holm"] = round(float(p), 4)
    pr = [familles[f]["p_resid"] for f in PRIMAIRES if f in familles]
    for f, p in zip([f for f in PRIMAIRES if f in familles], _holm(pr)):
        familles[f]["p_resid_holm"] = round(float(p), 4)

    # descriptif des atomes : date, colinéarité, ACP
    atomes_dates = {}
    for j, a in enumerate(panini.ATOMES):
        rho, p = stats.spearmanr(Xfull[:, j], annees)
        atomes_dates[a] = {"rho_date": round(float(rho), 4), "p_date": float(p)}
    # ACP sur les colonnes **standardisées** (eigenvalues de la matrice de
    # corrélation) : le critère de Kaiser (> 1) est alors lisible.
    Xs = (X - X.mean(0)) / (X.std(0) + 1e-12)
    sv = np.linalg.svd(Xs - Xs.mean(0), compute_uv=False)
    ev = sv ** 2 / (n - 1)
    var = ev / ev.sum()
    return {
        "cohorte": cohorte,
        "n": n,
        "base_clr": f"{X.shape[1]} colonnes (CLR de rang {X.shape[1]})",
        "atomes_dates": atomes_dates,
        "condition": round(float(np.linalg.cond(Xs)), 2),
        "acp": {"valeurs_propres": np.round(ev, 4).tolist(),
                "variance_expliquee": np.round(var, 4).tolist(),
                "nb_composantes_kaiser": int(np.sum(ev > 1))},
        "metriques": metriques,
        "familles": familles,
        "metriques_ecartees": ecartees,
        "permutations": {"colonnes": n_perm_col, "date": n_perm_date,
                         "graine": GRAINE, "degre_date": degre_date},
        "null_col": {"moyenne": np.round(np.nanmean(null_col, axis=0), 4).tolist(),
                     "p95": np.round(np.nanpercentile(null_col, 95, axis=0), 4).tolist()},
        "null_resid": {"moyenne": np.round(np.nanmean(null_res, axis=0), 4).tolist(),
                       "p95": np.round(np.nanpercentile(null_res, 95, axis=0), 4).tolist()},
        "null_date_in": {"moyenne": np.round(np.nanmean(null_date_in, axis=0), 4).tolist(),
                         "p95": np.round(np.nanpercentile(null_date_in, 95, axis=0), 4).tolist()},
        "noms": noms,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mesurer", action="store_true")
    ap.add_argument("--analyser", action="store_true")
    ap.add_argument("--tout", action="store_true")
    ap.add_argument("--forcer", action="store_true")
    ap.add_argument("--rapide", action="store_true", help="500 permutations")
    ap.add_argument("--cohorte", default="toutes",
                    choices=["toutes", "mesurable", "utilisable", "strict", "strict_plus"])
    args = ap.parse_args(argv)
    if args.tout or args.mesurer:
        data = charger_donnees(forcer=args.forcer)
        print(f"mesures : {len(data['oeuvres'])} œuvres → {SORTIE_MESURES}")
    if args.tout or args.analyser:
        data = charger_donnees()
        n_col = 500 if args.rapide else 2000
        n_date = 500 if args.rapide else 1000
        if args.cohorte == "toutes":
            plan = [("utilisable", n_col, n_date, 1),
                    ("mesurable", max(300, n_col // 4), max(300, n_date // 4), 1),
                    ("propre", max(300, n_col // 4), max(300, n_date // 4), 1),
                    ("strict", max(300, n_col // 4), max(300, n_date // 4), 1),
                    ("utilisable", max(300, n_col // 4), max(300, n_date // 4), 2)]
        else:
            plan = [(args.cohorte, n_col, n_date, 1)]
        resultats = []
        for cohorte, nc, nd, deg in plan:
            print(f"=== cohorte {cohorte} (colonnes={nc}, date={nd}, degré date={deg})", flush=True)
            r = analyser(data, cohorte=cohorte, n_perm_col=nc,
                         n_perm_date=nd, degre_date=deg)
            r["cle"] = f"{cohorte}_d{deg}"
            resultats.append(r)
        primaire = resultats[0]
        res = {
            "fiche": "reports/rapport-atomes-prediction.md",
            "version": "1.0",
            "date": "2026-11-15",
            "titre": "Les 14 atomes de Panini prédisent-ils les niveaux de Drave ?",
            "statut": "mesure",
            "source": data["source"],
            "atomes": data["atomes"],
            "cohorte_primaire": primaire["cohorte"],
            "n": primaire["n"],
            "familles": primaire["familles"],
            "metriques": primaire["metriques"],
            "metriques_ecartees": primaire["metriques_ecartees"],
            "permutations": primaire["permutations"],
            "null_col": primaire["null_col"],
            "null_resid": primaire["null_resid"],
            "null_date_in": primaire["null_date_in"],
            "noms": primaire["noms"],
            "cohortes": resultats,
            "oeuvres": data["oeuvres"],
        }
        SORTIE.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"résultats → {SORTIE}")
        for r in resultats:
            print(f"-- {r['cle']} (n={r['n']})")
            for f in PRIMAIRES:
                if f not in r["familles"]:
                    continue
                x = r["familles"][f]
                print(f"  {f:<12} R²A={x['r2_atomes_moyen']:+.4f} pC={x['p_col']:.4f} "
                      f"rhoA={x['rho_cv_moyen']:+.4f} pR={x['p_rho_col']:.4f} "
                      f"R²date={x['r2_date_in_moyen']:+.4f} "
                      f"R²res={x['r2_resid_moyen']:+.4f} pRes={x['p_resid']:.4f}")


if __name__ == "__main__":
    main()
