#!/usr/bin/env python3
"""panini_334.py — J12.1 : le corpus §334 et les signatures des 44 œuvres.

LA QUESTION. Panini/Nipada ont mesuré que leur signature lexicale capte l'époque
(β +0,138) bien plus que la filiation (β +0,049). J12.1 demande la même chose sur
la **deuxième vague** de leurs artefacts : le corpus §334 (114 textes actifs, 655
paires finies, 102 sources acquises) et les signatures V14 de 44 œuvres (14 parts
flottantes). Le retrieval retrouve-t-il la **filiation** ou l'**époque** ? La
prédiction de l'année est-elle plus forte que celle de la tradition ? Et que
devient cet arbitrage quand on **contrôle la date** ?

CE QUI EST MESURÉ, EN DEUX TEMPS.
  1. **Niveau paire (655 paires)** : la loi H0 de Panini
     `d_lex ~ d_topo^0,67` (R² = 0,909139 officiel) est reproduite, puis opposée
     à un modèle d'**époque** (`d_lex ~ |Δannée|`), à un modèle joint et à un
     modèle inverse (`d_topo^0,67 ~ |Δannée|`). Les coefficients standardisés,
     les R² partiels et les intervalles bootstrap par texte disent laquelle des
     deux variables porte la variance — et si le plan permet seulement de les
     séparer.
  2. **Niveau œuvre (44 signatures)** : retrieval du plus proche voisin par
     cosinus des 14 atomes ; on regarde si le top-1 partage la **tradition**
     (filiation) ou s'il est **proche dans le temps** (époque). Puis prédiction
     leave-one-out de l'année (kNN, ridge) et de la tradition (kNN), avec les
     mêmes contrôles.

LES CONTRÔLES DE DATE, ET LES AUTRES.
  (a) **Date contrôlée** : les étiquettes de tradition sont permutées **dans des
      tranches de 250 ans** ; le retrieval de filiation doit survivre à cette
      permutation, sinon il ne fait que retrouver l'époque.
  (b) **Filiation contrôlée** : les années sont permutées **dans chaque
      tradition** ; le retrieval d'époque doit survivre, sinon il ne fait que
      retrouver la tradition.
  (c) **Signatures permutées** : on assigne les signatures aux mauvaises œuvres ;
      tous les taux doivent retomber au hasard.
  (d) **Doublons exacts** : `plato_gorgias`/`plato_gorgias_jowett` et
      `plato_meno`/`plato_meno_jowett` ont la même signature (cos = 1) ; on les
      retire des candidats de retrieval et on refait la mesure sans eux.
  (e) **Surface** : les 44 œuvres sont massivement des traductions anglaises
      (24 sources `eng`, 1 `fra`, 19 langue inconnue). On refait le modèle de
      signature sur les paires `eng–eng` seulement.
  (f) **Négatifs de paire** : années permutées entre textes, traditions
      permutées entre textes, `d_topo` permuté entre paires.

CE QUE LE DISPOSITIF NE PEUT PAS DIRE.
  - La date attachée à une œuvre est sa date de **composition** (ou son
    estimation), pas la date de sa **traduction** ; les signatures sont
    calculées sur des traductions majoritairement anglaises du XIXe–XXe siècle.
    Le test d'époque est donc biaisé **contre** un effet de la date de
    composition.
  - Les 655 paires ne mettent en jeu que **48 textes distincts** (44 signés) :
    le « corpus de 114 textes » est une étiquette de corpus actif, pas un
    échantillon de retrieval de 114 textes.
  - `d_topo` est une distance de **tradition/transmission**, pas une distance de
    famille de langues ; elle est corrélée à l'écart de dates.

SORTIE. `reports/panini-334.json` (versionné), plus un résumé sur stdout.
Aucune écriture dans Panini : les sources sont lues en lecture seule, avec
SHA-256 et commit git.

Usage :
  python3 tools/panini_334.py
  python3 tools/panini_334.py --rapide
  python3 tools/panini_334.py --sortie /tmp/panini-334.json
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import pathlib
import subprocess

import numpy as np
from scipy import stats

RACINE = pathlib.Path(__file__).resolve().parent.parent
PANINI = RACINE.parent / "Panini" / "research"
PAIRES = PANINI / "nipada" / "falsification" / "pairs334_axes_v1.json"
GRAPHE = PANINI / "nipada" / "falsification" / "nipada_v334_graph_v35.json"
SIGNATURES = PANINI / "nipada" / "falsification" / "analytic_sigs_v1.json"
REVALIDATION = PANINI / "nipada" / "falsification" / "nipada_v334_revalidation_v35.json"
COUVERTURE = PANINI / "nipada" / "corpus" / "_cache" / "sources_coverage.json"
MANIFESTE = PANINI / "nipada" / "corpus" / "_cache" / "sources_manifest.json"
V150 = PANINI / "nipada" / "falsification" / "nipada_v150_validation.json"
SORTIE_DEFAUT = RACINE / "reports" / "panini-334.json"

ATOMES = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS", "MODALITÉ",
    "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION", "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]

# Les étiquettes brutes de `tradition_label` sont incohérentes pour un même
# ensemble : les dialogues de Platon sont tantôt GRECO_LATIN_AXIAL, tantôt
# GRECO_PLATONIC (et le même texte apparaît sous les deux). On regroupe les
# traditions larges, et on garde l'étiquette fine comme seconde lecture.
TRADITION_LARGE = {
    "GRECO_LATIN_AXIAL": "GRECO",
    "GRECO_PLATONIC": "GRECO",
    "ABRAHAMIC_PROPHETIC_AXIAL": "ABRAHAMIC",
    "JUDEAN_APOCALYPTIC_LATE": "ABRAHAMIC",
    "BUDDHIST_AXIAL": "BUDDHIST",
    "CHINESE_AXIAL": "CHINESE",
    "INDIAN_AXIAL": "INDIAN",
    "MILLENARIAN_MODERN_PROTESTANT": "MILLENARIAN",
    "COMBINATORY_LOGIC": "FORMAL_LOGIC",
    "RECURSIVE_FUNCTIONS": "FORMAL_LOGIC",
    "MANY_VALUED_LOGIC": "FORMAL_LOGIC",
    "FUZZY_LOGIC": "FORMAL_LOGIC",
    "SEMANTIC_NETWORKS": "COGNITIVE_SCIENCE",
    "CONCEPTUAL_DEPENDENCY": "COGNITIVE_SCIENCE",
    "DISTRIBUTIONAL_SEMANTICS": "COGNITIVE_SCIENCE",
    "NEURAL_LANGUAGE_MODELS": "COGNITIVE_SCIENCE",
    "RENAISSANCE_OCCULT_EARLY_MODERN": "RENAISSANCE_OCCULT",
    "CLASSICAL_ORACULAR": "CLASSICAL_ORACULAR",
    "NORSE_EDDIC_MEDIEVAL": "NORSE_EDDIC",
}

# Quelques auteurs sont écrits deux fois pour le même auteur (Platon vs
# « Platon (Jowett) »). On ne fusionne que ce cas évident.
AUTEUR_CANONIQUE = {
    "Platon (Jowett)": "plato",
}

BINS_DATE = [-10_000, -500, -250, 0, 250, 500, 1000, 1800, 2000, 2020, 10_000]
# Indexés comme np.digitize sur BINS_DATE : l'indice 0 n'est pas utilisé.
NOMS_BINS = [
    "hors", "< -500", "-500..-250", "-250..0", "0..250", "250..500",
    "500..1000", "1000..1800", "1800..2000", "2000..2020", "> 2020",
]
SEUIL_PROCHE = 50  # ans, comme J3.1
SEUIL_DOUBLON = 0.99999  # cosinus : deux signatures identiques


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


def commit_git(chemin: pathlib.Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(chemin), "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return None


def moyenne(valeurs) -> float:
    return float(np.mean(valeurs)) if len(valeurs) else float("nan")


def ecart_type(valeurs) -> float:
    return float(np.std(valeurs, ddof=0)) if len(valeurs) else float("nan")


def ic95(valeurs) -> list[float] | None:
    if not len(valeurs):
        return None
    return [float(np.percentile(valeurs, 2.5)), float(np.percentile(valeurs, 97.5))]


def p_unilateral(null, observe, sens="superieur") -> float:
    """p = (1 + #{null >= obs}) / (B + 1) (ou <= pour sens='inferieur')."""
    null = np.asarray(null, dtype=float)
    if sens == "superieur":
        return float((1 + np.sum(null >= observe)) / (len(null) + 1))
    return float((1 + np.sum(null <= observe)) / (len(null) + 1))


def p_bilateral(null, observe) -> float:
    null = np.asarray(null, dtype=float)
    centre = float(np.mean(null))
    return float((1 + np.sum(np.abs(null - centre) >= abs(observe - centre))) / (len(null) + 1))


def standardise(v: np.ndarray) -> np.ndarray:
    v = np.asarray(v, dtype=float)
    e = float(np.std(v))
    return (v - float(np.mean(v))) / e if e > 0 else np.zeros_like(v)


def ols(y, X, poids=None):
    """OLS avec intercept. X sans colonne de 1. Retourne (beta, r2, yhat)."""
    y = np.asarray(y, dtype=float)
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X[:, None]
    A = np.column_stack([np.ones(len(y)), X])
    if poids is None:
        beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    else:
        w = np.asarray(poids, dtype=float)
        sw = np.sqrt(w)
        beta, *_ = np.linalg.lstsq(A * sw[:, None], y * sw, rcond=None)
    yhat = A @ beta
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return beta, r2, yhat


def r2_partiel(r2_joint: float, r2_sans: float) -> float:
    return (r2_joint - r2_sans) / (1.0 - r2_sans) if r2_sans < 1 else float("nan")


def auc(y, score) -> float:
    """AUC de rang, sans sklearn."""
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    pos = score[y == 1]
    neg = score[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    rangs = stats.rankdata(np.concatenate([pos, neg]))
    return float((np.sum(rangs[: len(pos)]) - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def logit(y, X, max_iter=100):
    """Logistique Newton avec intercept. X sans colonne de 1."""
    y = np.asarray(y, dtype=float)
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X[:, None]
    A = np.column_stack([np.ones(len(y)), X])
    w = np.zeros(A.shape[1])
    for _ in range(max_iter):
        p = 1.0 / (1.0 + np.exp(-np.clip(A @ w, -30, 30)))
        W = np.clip(p * (1 - p), 1e-9, None)
        H = A.T @ (W[:, None] * A) + 1e-6 * np.eye(A.shape[1])
        pas = np.linalg.solve(H, A.T @ (y - p))
        w += pas
        if float(np.max(np.abs(pas))) < 1e-8:
            break
    p = 1.0 / (1.0 + np.exp(-np.clip(A @ w, -30, 30)))
    return w, auc(y, p)


def bin_date(annee: float) -> int:
    return int(np.digitize([annee], BINS_DATE)[0])


def tradition_large(etiquette: str | None) -> str:
    etiquette = etiquette or ""
    return TRADITION_LARGE.get(etiquette, etiquette or "INCONNU")


def auteur_canonique(auteur: str | None) -> str:
    auteur = auteur or "INCONNU"
    return AUTEUR_CANONIQUE.get(auteur, auteur)


# ---------------------------------------------------------------------------
# 1. Chargement et audit
# ---------------------------------------------------------------------------

def charger():
    paires = lire_json(PAIRES)
    graphe = lire_json(GRAPHE)
    signatures = lire_json(SIGNATURES)
    revalidation = lire_json(REVALIDATION)
    couverture = {x["id"]: x for x in lire_json(COUVERTURE)}
    manifeste = {x["id"]: x for x in lire_json(MANIFESTE)}
    noeuds = graphe["nodes"]

    ids_paires = sorted({p["a"] for p in paires["pairs"]} | {p["b"] for p in paires["pairs"]})
    ids_signes = sorted(signatures)

    textes = {}
    for tid in ids_paires:
        n = noeuds.get(tid, {})
        m = manifeste.get(tid, {})
        c = couverture.get(tid, {})
        textes[tid] = {
            "id": tid,
            "annee": n.get("year"),
            "tradition_fine": n.get("tradition_label") or "",
            "tradition_large": tradition_large(n.get("tradition_label")),
            "tradition_micro": n.get("tradition_micro") or "",
            "auteur": auteur_canonique(n.get("author")),
            "auteur_brut": n.get("author") or "",
            "langue_origine": n.get("language_original") or n.get("lang") or "",
            "langue_source": (m.get("lang") or "").strip(),
            "url_source": (m.get("url") or "").strip(),
            "source_ok": bool(c.get("ok")),
            "mots_source": c.get("words"),
            "titre": n.get("title_en") or n.get("title_original") or tid,
            "kind": n.get("kind") or "",
            "signe": tid in signatures,
        }

    for tid in ids_signes:
        if tid not in textes:
            raise RuntimeError(f"signature sans texte dans les paires : {tid}")
        textes[tid]["signature"] = [float(signatures[tid][a]) for a in ATOMES]

    audit = {
        "corpus_actif_officiel": revalidation.get("corpus_actif", {}).get("total"),
        "corpus_actif_tradition": revalidation.get("corpus_actif", {}).get("trad"),
        "corpus_actif_references": revalidation.get("corpus_actif", {}).get("refs"),
        "paires": len(paires["pairs"]),
        "sections": dict(collections.Counter(p["section"] for p in paires["pairs"])),
        "textes_distincts_paires": len(ids_paires),
        "textes_absents_des_paires": (revalidation.get("corpus_actif", {}).get("total") or 0) - len(ids_paires),
        "oeuvres_signees": len(ids_signes),
        "textes_paires_sans_signature": sorted(set(ids_paires) - set(ids_signes)),
        "sources_manifeste": len(manifeste),
        "sources_ok": sum(1 for x in couverture.values() if x.get("ok")),
        "sources_ok_parmi_48": sum(1 for tid in ids_paires if textes[tid]["source_ok"]),
        "sources_ok_parmi_44": sum(1 for tid in ids_signes if textes[tid]["source_ok"]),
        "urls_non_vides": sum(1 for m in manifeste.values() if (m.get("url") or "").strip()),
        "urls_uniques_non_vides": len({(m.get("url") or "").strip() for m in manifeste.values() if (m.get("url") or "").strip()}),
        "langues_source_44": dict(collections.Counter(textes[t]["langue_source"] or "inconnu" for t in ids_signes)),
        "textes": [textes[t] for t in sorted(textes)],
    }

    return paires["pairs"], graphe, signatures, revalidation, textes, ids_paires, ids_signes, audit


# ---------------------------------------------------------------------------
# 2. Niveau paire — H0, époque, filiation, contrôles
# ---------------------------------------------------------------------------

def analyser_paires(paires, textes, ids_paires, n_perm=2000, n_boot=1000, graine=0):
    # 655 **lignes** de paires, mais 160 doublons et 7 auto-paires : l'unité
    # d'inférence est la paire non ordonnée de deux textes distincts.
    paires_officielles = list(paires)
    vues = set()
    paires_inf = []
    n_auto = 0
    for p in paires_officielles:
        cle = tuple(sorted((p["a"], p["b"])))
        if cle in vues:
            continue
        vues.add(cle)
        if p["a"] == p["b"]:
            n_auto += 1
            continue
        paires_inf.append(p)
    paires = paires_inf
    idx = {tid: i for i, tid in enumerate(ids_paires)}
    annees = np.array([textes[t]["annee"] for t in ids_paires], dtype=float)
    trad = np.array([textes[t]["tradition_large"] for t in ids_paires], dtype=object)
    auteur = np.array([textes[t]["auteur"] for t in ids_paires], dtype=object)
    langue = np.array([textes[t]["langue_source"] or "" for t in ids_paires], dtype=object)

    ia = np.array([idx[p["a"]] for p in paires])
    ib = np.array([idx[p["b"]] for p in paires])
    d_lex = np.array([p["d_lex"] for p in paires], dtype=float)
    d_topo = np.array([p["d_topo"] for p in paires], dtype=float)
    cos = np.array([p["cos"] for p in paires], dtype=float)
    dy = np.abs(annees[ia] - annees[ib])
    dy_siecle = dy / 100.0
    same_trad = np.array([trad[i] == trad[j] for i, j in zip(ia, ib)])
    same_auteur = np.array([auteur[i] == auteur[j] for i, j in zip(ia, ib)])
    same_langue = np.array([bool(langue[i]) and langue[i] == langue[j] for i, j in zip(ia, ib)])
    topo67 = d_topo ** 0.67

    # H0 officielle : les 655 lignes, y compris doublons et auto-paires.
    ia_all = np.array([idx[p["a"]] for p in paires_officielles])
    ib_all = np.array([idx[p["b"]] for p in paires_officielles])
    d_lex_all = np.array([p["d_lex"] for p in paires_officielles], dtype=float)
    topo_all = np.array([p["d_topo"] for p in paires_officielles], dtype=float) ** 0.67
    _, r2_h0_655, _ = ols(d_lex_all, topo_all)

    # --- modèles principaux (488 paires uniques non auto) ------------------
    b_h0, r2_h0, _ = ols(d_lex, topo67)
    b_date, r2_date, _ = ols(d_lex, dy_siecle)
    b_joint, r2_joint, _ = ols(d_lex, np.column_stack([topo67, dy_siecle]))
    b_joint_std, r2_joint_std, _ = ols(
        standardise(d_lex), np.column_stack([standardise(topo67), standardise(dy_siecle)])
    )
    b_inverse, r2_inverse, _ = ols(topo67, dy_siecle)
    b_trad, r2_trad, _ = ols(d_lex, same_trad.astype(float))
    b_trad_joint, r2_trad_joint, _ = ols(
        d_lex, np.column_stack([topo67, same_trad.astype(float)])
    )
    b_complet, r2_complet, _ = ols(
        standardise(d_lex),
        np.column_stack([standardise(topo67), standardise(dy_siecle), same_trad.astype(float)]),
    )

    modeles = {
        "H0": {
            "formule": "d_lex ~ 1 + d_topo^0.67",
            "beta": [float(x) for x in b_h0],
            "r2": float(r2_h0),
            "n": int(len(d_lex)),
            "n_officiel": int(len(d_lex_all)),
            "r2_655_lignes": float(r2_h0_655),
            "officiel_r2": 0.909139,
            "ecart_officiel_655": float(abs(r2_h0_655 - 0.909139)),
            "ecart_officiel_488": float(abs(r2_h0 - 0.909139)),
        },
        "date_seule": {
            "formule": "d_lex ~ 1 + |Δannée|/100",
            "beta": [float(x) for x in b_date],
            "r2": float(r2_date),
            "correlation_spearman_dy_dlex": float(stats.spearmanr(dy, d_lex).statistic),
        },
        "joint": {
            "formule": "d_lex ~ 1 + d_topo^0.67 + |Δannée|/100",
            "beta": [float(x) for x in b_joint],
            "r2": float(r2_joint),
            "partiel_topo_apres_date": float(r2_partiel(r2_joint, r2_date)),
            "partiel_date_apres_topo": float(r2_partiel(r2_joint, r2_h0)),
        },
        "joint_standardise": {
            "formule": "z(d_lex) ~ z(d_topo^0.67) + z(|Δannée|/100)",
            "beta": [float(x) for x in b_joint_std],
            "r2": float(r2_joint_std),
        },
        "inverse": {
            "formule": "d_topo^0.67 ~ 1 + |Δannée|/100",
            "beta": [float(x) for x in b_inverse],
            "r2": float(r2_inverse),
        },
        "tradition_seule": {
            "formule": "d_lex ~ 1 + même_tradition_large",
            "beta": [float(x) for x in b_trad],
            "r2": float(r2_trad),
        },
        "tradition_apres_topo": {
            "formule": "d_lex ~ 1 + d_topo^0.67 + même_tradition_large",
            "beta": [float(x) for x in b_trad_joint],
            "r2": float(r2_trad_joint),
            "partiel_tradition_apres_topo": float(r2_partiel(r2_trad_joint, r2_h0)),
        },
        "complet_standardise": {
            "formule": "z(d_lex) ~ z(d_topo^0.67) + z(|Δannée|/100) + même_tradition_large",
            "beta": [float(x) for x in b_complet],
            "r2": float(r2_complet),
        },
    }

    # --- positivité : où vit le contraste --------------------------------
    n_same = int(same_trad.sum())
    n_diff = int((~same_trad).sum())
    same_dy = dy[same_trad]
    diff_dy = dy[~same_trad]
    positivite = {
        "n_meme_tradition": n_same,
        "n_tradition_differente": n_diff,
        "dy_meme_tradition": {
            "moyenne": float(np.mean(same_dy)),
            "mediane": float(np.median(same_dy)),
            "p95": float(np.percentile(same_dy, 95)),
            "max": float(np.max(same_dy)),
            "n_sup_100_ans": int(np.sum(same_dy > 100)),
        },
        "dy_tradition_differente": {
            "moyenne": float(np.mean(diff_dy)),
            "mediane": float(np.median(diff_dy)),
            "p95": float(np.percentile(diff_dy, 95)),
            "max": float(np.max(diff_dy)),
            "n_inf_100_ans": int(np.sum(diff_dy <= 100)),
        },
        "recouvrement": {
            "meme_tradition_sup_100_ans": int(np.sum(same_dy > 100)),
            "tradition_differente_inf_100_ans": int(np.sum(diff_dy <= 100)),
            "lecture": "les couples de même tradition sont presque tous contemporains ; les couples longs sont presque tous inter-traditions",
        },
    }

    # --- bins de date : le contraste à date contrôlée ---------------------
    bins = np.array([bin_date(a) for a in annees])
    bins_paire = np.where(bins[ia] == bins[ib], bins[ia], -1)
    bins_date = []
    for b in sorted(set(bins_paire)):
        m = bins_paire == b
        if m.sum() == 0:
            continue
        ms, md = m & same_trad, m & ~same_trad
        bins_date.append({
            "bin": int(b),
            "nom": NOMS_BINS[b] if 0 <= b < len(NOMS_BINS) else "hors",
            "n": int(m.sum()),
            "n_meme_tradition": int(ms.sum()),
            "n_tradition_differente": int(md.sum()),
            "d_lex_meme_tradition": float(np.mean(d_lex[ms])) if ms.sum() else None,
            "d_lex_tradition_differente": float(np.mean(d_lex[md])) if md.sum() else None,
            "delta": float(np.mean(d_lex[ms]) - np.mean(d_lex[md])) if ms.sum() and md.sum() else None,
            "cos_meme_tradition": float(np.mean(cos[ms])) if ms.sum() else None,
            "cos_tradition_differente": float(np.mean(cos[md])) if md.sum() else None,
        })
    # contraste apparié par tranche, pondéré par le minimum des deux effectifs
    deltas, poids = [], []
    for b in bins_date:
        if b["delta"] is not None:
            deltas.append(b["delta"])
            poids.append(min(b["n_meme_tradition"], b["n_tradition_differente"]))
    delta_pondere = float(np.average(deltas, weights=poids)) if deltas else None

    # --- permutations ------------------------------------------------------
    rng = np.random.default_rng(graine)

    # (a) années permutées entre textes
    null_date_r2, null_date_partiel, null_inverse_r2, null_joint_date_coef = [], [], [], []
    for _ in range(n_perm):
        yp = rng.permutation(annees)
        dyp = np.abs(yp[ia] - yp[ib]) / 100.0
        _, r2d, _ = ols(d_lex, dyp)
        _, r2j, _ = ols(d_lex, np.column_stack([topo67, dyp]))
        _, r2i, _ = ols(topo67, dyp)
        bj, _, _ = ols(d_lex, np.column_stack([topo67, dyp]))
        null_date_r2.append(r2d)
        null_date_partiel.append(r2_partiel(r2j, r2_h0))
        null_inverse_r2.append(r2i)
        null_joint_date_coef.append(float(bj[2]))

    # (b) traditions permutées entre textes
    null_trad_delta, null_trad_partiel = [], []
    for _ in range(n_perm):
        tp = rng.permutation(trad)
        sp = np.array([tp[i] == tp[j] for i, j in zip(ia, ib)])
        _, r2t, _ = ols(d_lex, sp.astype(float))
        _, r2tj, _ = ols(d_lex, np.column_stack([topo67, sp.astype(float)]))
        null_trad_delta.append(float(np.mean(d_lex[sp]) - np.mean(d_lex[~sp])) if sp.sum() and (~sp).sum() else np.nan)
        null_trad_partiel.append(r2_partiel(r2tj, r2_h0))

    # (c) d_topo permuté entre paires
    null_h0 = []
    for _ in range(n_perm):
        _, r2, _ = ols(d_lex, rng.permutation(topo67))
        null_h0.append(r2)

    permutations = {
        "n": n_perm,
        "date": {
            "r2_date_seule_observe": float(r2_date),
            "r2_date_seule_null_moyen": float(np.nanmean(null_date_r2)),
            "p_date_seule": p_unilateral(null_date_r2, r2_date),
            "partiel_date_apres_topo_observe": float(r2_partiel(r2_joint, r2_h0)),
            "partiel_date_apres_topo_null_moyen": float(np.nanmean(null_date_partiel)),
            "p_partiel_date_apres_topo": p_bilateral(null_date_partiel, r2_partiel(r2_joint, r2_h0)),
            "coef_date_joint_observe": float(b_joint[2]),
            "coef_date_joint_null_moyen": float(np.nanmean(null_joint_date_coef)),
            "p_coef_date_joint": p_bilateral(null_joint_date_coef, float(b_joint[2])),
            "r2_inverse_observe": float(r2_inverse),
            "r2_inverse_null_moyen": float(np.nanmean(null_inverse_r2)),
            "p_inverse": p_unilateral(null_inverse_r2, r2_inverse),
        },
        "tradition": {
            "delta_observe": float(np.mean(d_lex[same_trad]) - np.mean(d_lex[~same_trad])),
            "delta_null_moyen": float(np.nanmean(null_trad_delta)),
            "p_delta": p_unilateral(null_trad_delta, float(np.mean(d_lex[same_trad]) - np.mean(d_lex[~same_trad])), "inferieur"),
            "partiel_tradition_apres_topo_observe": float(r2_partiel(r2_trad_joint, r2_h0)),
            "partiel_tradition_apres_topo_null_moyen": float(np.nanmean(null_trad_partiel)),
            "p_partiel_tradition_apres_topo": p_unilateral(null_trad_partiel, float(r2_partiel(r2_trad_joint, r2_h0))),
        },
        "H0": {
            "r2_observe": float(r2_h0),
            "r2_null_moyen": float(np.nanmean(null_h0)),
            "p_h0": p_unilateral(null_h0, r2_h0),
        },
    }

    # --- bootstrap par texte (IC des coefficients) ------------------------
    boot = {"n": n_boot, "r2_h0": [], "r2_date": [], "partiel_date": [],
            "partiel_topo": [], "coef_date_joint": [], "coef_topo_joint": []}
    for _ in range(n_boot):
        tirage = rng.integers(0, len(ids_paires), len(ids_paires))
        multiplicite = collections.Counter(tirage.tolist())
        poids = np.array([multiplicite.get(int(i), 0) * multiplicite.get(int(j), 0) for i, j in zip(ia, ib)], dtype=float)
        m = poids > 0
        if m.sum() < 20:
            continue
        w = poids[m]
        y = d_lex[m]
        t = topo67[m]
        dd = dy_siecle[m]
        _, r2h, _ = ols(y, t, w)
        _, r2d, _ = ols(y, dd, w)
        bj, r2j, _ = ols(y, np.column_stack([t, dd]), w)
        boot["r2_h0"].append(r2h)
        boot["r2_date"].append(r2d)
        boot["partiel_date"].append(r2_partiel(r2j, r2h))
        boot["partiel_topo"].append(r2_partiel(r2j, r2d))
        boot["coef_topo_joint"].append(float(bj[1]))
        boot["coef_date_joint"].append(float(bj[2]))

    bootstrap = {
        "n_demandes": n_boot,
        "n_valides": len(boot["r2_h0"]),
        "r2_h0": {"moyenne": float(np.mean(boot["r2_h0"])), "ic95": ic95(boot["r2_h0"])},
        "r2_date": {"moyenne": float(np.mean(boot["r2_date"])), "ic95": ic95(boot["r2_date"])},
        "partiel_date_apres_topo": {"moyenne": float(np.mean(boot["partiel_date"])), "ic95": ic95(boot["partiel_date"])},
        "partiel_topo_apres_date": {"moyenne": float(np.mean(boot["partiel_topo"])), "ic95": ic95(boot["partiel_topo"])},
        "coef_topo_joint": {"moyenne": float(np.mean(boot["coef_topo_joint"])), "ic95": ic95(boot["coef_topo_joint"])},
        "coef_date_joint": {"moyenne": float(np.mean(boot["coef_date_joint"])), "ic95": ic95(boot["coef_date_joint"])},
    }

    # --- surface : paires de même langue source connue --------------------
    surface = {}
    for code in ("eng", "fra"):
        m = (langue[ia] == code) & (langue[ib] == code)
        if m.sum() < 20:
            continue
        _, r2h, _ = ols(d_lex[m], topo67[m])
        _, r2d, _ = ols(d_lex[m], dy_siecle[m])
        bj, r2j, _ = ols(d_lex[m], np.column_stack([topo67[m], dy_siecle[m]]))
        surface[code] = {
            "n": int(m.sum()),
            "r2_h0": float(r2h),
            "r2_date": float(r2d),
            "r2_joint": float(r2j),
            "beta_topo": float(bj[1]),
            "beta_date": float(bj[2]),
            "partiel_date_apres_topo": float(r2_partiel(r2j, r2h)),
        }

    # --- doublons exacts ---------------------------------------------------
    # On identifie les signatures identiques des 44 œuvres (cos >= 0.99999).
    ids_signes = sorted([t for t in textes if textes[t].get("signature")])
    sig = np.array([textes[t]["signature"] for t in ids_signes])
    sig_n = sig / np.linalg.norm(sig, axis=1, keepdims=True)
    C = sig_n @ sig_n.T
    doublons = []
    for i in range(len(ids_signes)):
        for j in range(i + 1, len(ids_signes)):
            if C[i, j] >= SEUIL_DOUBLON:
                doublons.append({
                    "a": ids_signes[i], "b": ids_signes[j], "cos": float(C[i, j]),
                    "meme_tradition_large": textes[ids_signes[i]]["tradition_large"] == textes[ids_signes[j]]["tradition_large"],
                })

    # --- contraste à date et surface contrôlées ---------------------------
    # Le bin axial est celui qui contient assez de paires des deux classes.
    # On le reprend à surface constante (même langue source connue).
    def contraste(masque):
        ms, md = masque & same_trad, masque & ~same_trad
        return {
            "n": int(masque.sum()),
            "n_meme_tradition": int(ms.sum()),
            "n_tradition_differente": int(md.sum()),
            "d_lex_meme_tradition": float(np.mean(d_lex[ms])) if ms.sum() else None,
            "d_lex_tradition_differente": float(np.mean(d_lex[md])) if md.sum() else None,
            "delta": float(np.mean(d_lex[ms]) - np.mean(d_lex[md])) if ms.sum() and md.sum() else None,
            "cos_panini_meme_tradition": float(np.mean(cos[ms])) if ms.sum() else None,
            "cos_panini_tradition_differente": float(np.mean(cos[md])) if md.sum() else None,
        }

    masque_axial = bins_paire == 2
    masque_axial_langue = masque_axial & same_langue
    masque_eng = same_langue & (langue[ia] == "eng")
    contraste_date_surface = {
        "bin_axial": contraste(masque_axial),
        "bin_axial_meme_langue": contraste(masque_axial_langue),
        "meme_langue_eng": contraste(masque_eng),
    }
    # OLS avec effets fixes de tranche et de langue (langue = même code connu ou 'mix')
    langue_paire = np.array([
        langue[i] if langue[i] and langue[i] == langue[j] else "mix"
        for i, j in zip(ia, ib)
    ], dtype=object)
    X_fe = [same_trad.astype(float)]
    for bv in sorted(set(bins_paire.tolist()))[1:]:
        X_fe.append((bins_paire == bv).astype(float))
    for lv in sorted(set(langue_paire.tolist()))[1:]:
        X_fe.append((langue_paire == lv).astype(float))
    b_fe, r2_fe, _ = ols(d_lex, np.column_stack(X_fe))
    contraste_date_surface["ols_effets_fixes"] = {
        "beta_meme_tradition": float(b_fe[1]),
        "r2": float(r2_fe),
        "formule": "d_lex ~ 1 + même_tradition + tranche_date + langue_source",
    }
    # Contrôle de date du contraste de filiation : étiquettes permutées dans
    # chaque tranche de date, puis delta recalculé dans la tranche axiale.
    rng_c = np.random.default_rng(graine + 11)
    null_axial, null_eng = [], []
    for _ in range(n_perm):
        tp = trad.copy()
        for b in sorted(set(bins.tolist())):
            idx_b = np.where(bins == b)[0]
            vals = tp[idx_b].copy()
            rng_c.shuffle(vals)
            tp[idx_b] = vals
        sp = np.array([tp[i] == tp[j] for i, j in zip(ia, ib)])
        for masque, stock in ((masque_axial, null_axial), (masque_eng, null_eng)):
            ms, md = masque & sp, masque & ~sp
            if ms.sum() and md.sum():
                stock.append(float(np.mean(d_lex[ms]) - np.mean(d_lex[md])))
    obs_axial = contraste_date_surface["bin_axial"]["delta"]
    obs_eng = contraste_date_surface["meme_langue_eng"]["delta"]
    contraste_date_surface["permutation_date_controlee"] = {
        "n": n_perm,
        "bin_axial": {
            "delta_observe": obs_axial,
            "delta_null_moyen": float(np.mean(null_axial)) if null_axial else None,
            "p": p_unilateral(null_axial, obs_axial, "inferieur") if null_axial else None,
        },
        "meme_langue_eng": {
            "delta_observe": obs_eng,
            "delta_null_moyen": float(np.mean(null_eng)) if null_eng else None,
            "p": p_unilateral(null_eng, obs_eng, "inferieur") if null_eng else None,
        },
    }

    return {
        "n_paires": int(len(d_lex)),
        "n_paires_officielles": int(len(paires_officielles)),
        "n_paires_uniques": int(len(vues)),
        "n_auto_paires": int(n_auto),
        "n_doublons_lignes": int(len(paires_officielles) - len(vues)),
        "n_textes": int(len(ids_paires)),
        "contraste_date_surface": contraste_date_surface,
        "modeles": modeles,
        "positivite": positivite,
        "bins_date": bins_date,
        "delta_pondere_bins": delta_pondere,
        "permutations": permutations,
        "bootstrap": bootstrap,
        "surface_meme_langue": surface,
        "doublons_exacts": doublons,
        "correlations": {
            "d_lex_vs_dy_spearman": float(stats.spearmanr(d_lex, dy).statistic),
            "d_lex_vs_topo_spearman": float(stats.spearmanr(d_lex, d_topo).statistic),
            "dy_vs_topo_spearman": float(stats.spearmanr(dy, d_topo).statistic),
            "cos_vs_dy_spearman": float(stats.spearmanr(cos, dy).statistic),
            "cos_vs_same_trad": float(stats.pointbiserialr(same_trad.astype(int), cos).statistic),
        },
        "paires": [
            {
                "a": p["a"], "b": p["b"], "section": p["section"],
                "d_topo": float(p["d_topo"]), "d_lex": float(p["d_lex"]),
                "cos": float(p["cos"]), "dy": float(dy[k]),
                "meme_tradition_large": bool(same_trad[k]),
                "meme_tradition_fine": bool(textes[p["a"]]["tradition_fine"] == textes[p["b"]]["tradition_fine"]),
                "meme_auteur": bool(same_auteur[k]),
            }
            for k, p in enumerate(paires)
        ],
    }


# ---------------------------------------------------------------------------
# 3. Niveau œuvre — retrieval, prédiction, contrôles
# ---------------------------------------------------------------------------

def construire_matrice(textes, ids_signes):
    X = np.array([textes[t]["signature"] for t in ids_signes], dtype=float)
    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
    C = Xn @ Xn.T
    return X, C


def ordre_candidats(C, seuil_doublon=SEUIL_DOUBLON):
    n = len(C)
    ordre = []
    for i in range(n):
        cand = [j for j in range(n) if j != i and C[i, j] < seuil_doublon]
        cand.sort(key=lambda j: (-C[i, j], j))
        ordre.append(np.array(cand, dtype=int))
    return ordre


def retrieval(ordre, annees, trad, auteur, seuil_proche=SEUIL_PROCHE):
    n = len(annees)
    top1 = np.array([o[0] for o in ordre])
    same_t = np.array([trad[i] == trad[top1[i]] for i in range(n)])
    same_a = np.array([auteur[i] == auteur[top1[i]] for i in range(n)])
    dy = np.array([abs(annees[i] - annees[top1[i]]) for i in range(n)])
    proche = dy <= seuil_proche

    chance_t, chance_a, chance_p = [], [], []
    for i, o in enumerate(ordre):
        chance_t.append(float(np.mean(trad[o] == trad[i])))
        chance_a.append(float(np.mean(auteur[o] == auteur[i])))
        chance_p.append(float(np.mean(np.abs(annees[o] - annees[i]) <= seuil_proche)))

    # top-3 : au moins un voisin de la même tradition / du même auteur
    top3_t, top3_a, top3_p = [], [], []
    for i, o in enumerate(ordre):
        k = o[: min(3, len(o))]
        top3_t.append(any(trad[j] == trad[i] for j in k))
        top3_a.append(any(auteur[j] == auteur[i] for j in k))
        top3_p.append(any(abs(annees[j] - annees[i]) <= seuil_proche for j in k))

    return {
        "n": int(n),
        "top1_idx": [int(x) for x in top1],
        "top1_meme_tradition": float(np.mean(same_t)),
        "top1_meme_auteur": float(np.mean(same_a)),
        "top1_proche_50ans": float(np.mean(proche)),
        "top1_dy_moyen": float(np.mean(dy)),
        "top1_dy_median": float(np.median(dy)),
        "chance_meme_tradition": float(np.mean(chance_t)),
        "chance_meme_auteur": float(np.mean(chance_a)),
        "chance_proche_50ans": float(np.mean(chance_p)),
        "enrichissement_tradition": float(np.mean(same_t) / np.mean(chance_t)) if np.mean(chance_t) > 0 else None,
        "enrichissement_auteur": float(np.mean(same_a) / np.mean(chance_a)) if np.mean(chance_a) > 0 else None,
        "enrichissement_proche": float(np.mean(proche) / np.mean(chance_p)) if np.mean(chance_p) > 0 else None,
        "top3_meme_tradition": float(np.mean(top3_t)),
        "top3_meme_auteur": float(np.mean(top3_a)),
        "top3_proche_50ans": float(np.mean(top3_p)),
        "detail": [
            {
                "requete": None,  # rempli par l'appelant
                "top1": None,
                "meme_tradition": bool(same_t[i]),
                "meme_auteur": bool(same_a[i]),
                "dy": float(dy[i]),
            }
            for i in range(n)
        ],
    }


def remplit_detail(res, ids):
    for i, d in enumerate(res["detail"]):
        d["requete"] = ids[i]
        d["top1"] = ids[res["top1_idx"][i]]
    return res


def metrique_annee(pred, vrai):
    pred = np.asarray(pred, dtype=float)
    vrai = np.asarray(vrai, dtype=float)
    mae = float(np.mean(np.abs(pred - vrai)))
    rmse = float(np.sqrt(np.mean((pred - vrai) ** 2)))
    ss_tot = float(np.sum((vrai - np.mean(vrai)) ** 2))
    r2 = 1.0 - float(np.sum((pred - vrai) ** 2)) / ss_tot if ss_tot > 0 else float("nan")
    rho = float(stats.spearmanr(pred, vrai).statistic)
    return {"mae": mae, "rmse": rmse, "r2": r2, "spearman": rho}


def knn_annee(ordre, annees, k=1):
    pred = []
    for i, o in enumerate(ordre):
        kk = o[: min(k, len(o))]
        pred.append(float(np.mean(annees[kk])))
    return np.array(pred)


def knn_classe(ordre, labels, k=1):
    pred = []
    for i, o in enumerate(ordre):
        kk = o[: min(k, len(o))]
        c = collections.Counter(labels[j] for j in kk)
        # départage déterministe : effectif puis ordre lexicographique
        pred.append(sorted(c.items(), key=lambda kv: (-kv[1], str(kv[0])))[0][0])
    return pred


def metrique_classe(pred, vrai):
    pred = np.asarray(pred, dtype=object)
    vrai = np.asarray(vrai, dtype=object)
    acc = float(np.mean(pred == vrai))
    classes = sorted(set(vrai.tolist()))
    recalls = []
    f1s = []
    for c in classes:
        m = vrai == c
        tp = int(np.sum((pred == c) & m))
        fp = int(np.sum((pred == c) & (~m)))
        fn = int(np.sum((pred != c) & m))
        recalls.append(tp / (tp + fn) if (tp + fn) else 0.0)
        prec = tp / (tp + fp) if (tp + fp) else 0.0
        f1s.append(2 * prec * recalls[-1] / (prec + recalls[-1]) if (prec + recalls[-1]) else 0.0)
    return {
        "exactitude": acc,
        "exactitude_equilibree": float(np.mean(recalls)),
        "f1_macro": float(np.mean(f1s)),
        "n_classes": len(classes),
    }


def ridge_loocv(X, y, C, lam=1.0):
    n = len(y)
    pred = []
    for i in range(n):
        tr = [j for j in range(n) if j != i and C[i, j] < SEUIL_DOUBLON]
        if len(tr) < 5:
            pred.append(float(np.mean(y)))
            continue
        mu = X[tr].mean(axis=0)
        sd = X[tr].std(axis=0)
        sd[sd == 0] = 1.0
        Z = (X[tr] - mu) / sd
        Zi = (X[i] - mu) / sd
        A = np.column_stack([np.ones(len(tr)), Z])
        w = np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ y[tr])
        pred.append(float(np.r_[1.0, Zi] @ w))
    return np.array(pred)


def analyser_oeuvres(textes, ids_signes, n_perm=5000, n_boot=1000, graine=0):
    X, C = construire_matrice(textes, ids_signes)
    n = len(ids_signes)
    annees = np.array([textes[t]["annee"] for t in ids_signes], dtype=float)
    trad = np.array([textes[t]["tradition_large"] for t in ids_signes], dtype=object)
    auteur = np.array([textes[t]["auteur"] for t in ids_signes], dtype=object)
    langue = np.array([textes[t]["langue_source"] or "" for t in ids_signes], dtype=object)
    bins = np.array([bin_date(a) for a in annees])

    ordre = ordre_candidats(C)
    ret = remplit_detail(retrieval(ordre, annees, trad, auteur), ids_signes)

    # --- nulls propres au retrieval --------------------------------------
    # Date contrôlée : années permutées dans chaque tradition.
    # Filiation contrôlée : traditions permutées dans chaque tranche de 250 ans.
    rng_ret = np.random.default_rng(graine + 7)
    bins_ret = np.array([bin_date(a) for a in annees])
    null_proche_date, null_dy_date, null_trad_filiation = [], [], []
    for _ in range(n_perm):
        yp = annees.copy()
        for t in sorted(set(trad.tolist())):
            idx = np.where(trad == t)[0]
            vals = yp[idx].copy()
            rng_ret.shuffle(vals)
            yp[idx] = vals
        rp = retrieval(ordre, yp, trad, auteur)
        null_proche_date.append(rp["top1_proche_50ans"])
        null_dy_date.append(rp["top1_dy_moyen"])
    for _ in range(n_perm):
        tp = trad.copy()
        for b in sorted(set(bins_ret.tolist())):
            idx = np.where(bins_ret == b)[0]
            vals = tp[idx].copy()
            rng_ret.shuffle(vals)
            tp[idx] = vals
        rp = retrieval(ordre, annees, tp, auteur)
        null_trad_filiation.append(rp["top1_meme_tradition"])
    retrieval_nulls = {
        "n": n_perm,
        "date_controlee": {
            "top1_proche_50ans_observe": ret["top1_proche_50ans"],
            "top1_proche_50ans_null_moyen": float(np.mean(null_proche_date)),
            "p_top1_proche_50ans": p_unilateral(null_proche_date, ret["top1_proche_50ans"]),
            "top1_dy_moyen_observe": ret["top1_dy_moyen"],
            "top1_dy_moyen_null_moyen": float(np.mean(null_dy_date)),
            "p_top1_dy_moyen": p_unilateral(null_dy_date, ret["top1_dy_moyen"], "inferieur"),
        },
        "filiation_controlee": {
            "top1_meme_tradition_observe": ret["top1_meme_tradition"],
            "top1_meme_tradition_null_moyen": float(np.mean(null_trad_filiation)),
            "p_top1_meme_tradition": p_unilateral(null_trad_filiation, ret["top1_meme_tradition"]),
        },
    }

    # --- modèle cos ~ tradition + date -----------------------------------
    iu = np.triu_indices(n, 1)
    cos_paires = C[iu]
    dy_paires = np.abs(annees[:, None] - annees[None, :])[iu]
    same_t = np.array([trad[i] == trad[j] for i in range(n) for j in range(i + 1, n)])
    same_a = np.array([auteur[i] == auteur[j] for i in range(n) for j in range(i + 1, n)])
    b_modele, r2_modele, _ = ols(
        cos_paires, np.column_stack([same_t.astype(float), standardise(np.log1p(dy_paires))])
    )
    b_modele_std, r2_modele_std, _ = ols(
        standardise(cos_paires), np.column_stack([same_t.astype(float), standardise(np.log1p(dy_paires))])
    )
    _, r2_trad_seule, _ = ols(cos_paires, same_t.astype(float))
    _, r2_date_seule, _ = ols(cos_paires, np.log1p(dy_paires))
    modele_cos = {
        "n_paires": int(len(cos_paires)),
        "beta": [float(x) for x in b_modele],
        "beta_standardise": [float(x) for x in b_modele_std],
        "r2": float(r2_modele),
        "r2_standardise": float(r2_modele_std),
        "r2_tradition_seule": float(r2_trad_seule),
        "r2_date_seule": float(r2_date_seule),
        "partiel_tradition_apres_date": float(r2_partiel(r2_modele, r2_date_seule)),
        "partiel_date_apres_tradition": float(r2_partiel(r2_modele, r2_trad_seule)),
        "logistique_tradition": None,
        "logistique_proche50": None,
    }
    # logistiques : la filiation et l'époque sont-elles prédites par le cosinus ?
    for nom, cible in [("logistique_tradition", same_t.astype(float)),
                       ("logistique_proche50", (dy_paires <= SEUIL_PROCHE).astype(float)),
                       ("logistique_proche100", (dy_paires <= 100).astype(float))]:
        w_cos, auc_cos = logit(cible, standardise(cos_paires))
        modele_cos[nom] = {
            "auc_cos": float(auc_cos),
            "beta_cos": [float(x) for x in w_cos],
            "note_controle": "le contrôle de date n'est pas interprétable pour proche50/proche100 (la date définit la cible) ; voir les taux stratifiés",
        }

    # --- retrieval : bins de date et contrastes ---------------------------
    bins_retrieval = []
    for b in sorted(set(bins)):
        m = bins == b
        if m.sum() < 2:
            continue
        # le contraste top1 par tranche n'a de sens que si la tranche a 2+ traditions
        idx = np.where(m)[0]
        if len(set(trad[m])) >= 2:
            same = 0
            total = 0
            for i in idx:
                cand = [j for j in ordre[i] if bins[j] == b]
                if not cand:
                    continue
                total += 1
                same += int(trad[cand[0]] == trad[i])
            bins_retrieval.append({
                "bin": int(b), "nom": NOMS_BINS[b] if b < len(NOMS_BINS) else "hors",
                "n_oeuvres": int(m.sum()), "n_traditions": len(set(trad[m])),
                "top1_meme_tradition_dans_le_bin": float(same / total) if total else None,
                "n_requetes": int(total),
            })

    # --- prédiction de l'année --------------------------------------------
    pred_knn = {k: knn_annee(ordre, annees, k) for k in (1, 3, 5)}
    pred_ridge = ridge_loocv(X, annees, C)
    baseline_med = float(np.median(annees))
    baseline_moy = float(np.mean(annees))
    annee = {
        "baseline_mediane": {"mae": float(np.mean(np.abs(baseline_med - annees))), "valeur": baseline_med},
        "baseline_moyenne": {"mae": float(np.mean(np.abs(baseline_moy - annees))), "valeur": baseline_moy},
        "knn": {str(k): metrique_annee(pred_knn[k], annees) for k in pred_knn},
        "ridge": metrique_annee(pred_ridge, annees),
    }

    # nulls : années permutées (global, puis dans chaque tradition)
    rng = np.random.default_rng(graine)
    null_global, null_dans_tradition, null_residu = [], [], []
    for _ in range(n_perm):
        yp = rng.permutation(annees)
        p = knn_annee(ordre, yp, 1)
        null_global.append(metrique_annee(p, yp)["mae"])
    for _ in range(n_perm):
        yp = annees.copy()
        for t in sorted(set(trad.tolist())):
            idx = np.where(trad == t)[0]
            vals = yp[idx].copy()
            rng.shuffle(vals)
            yp[idx] = vals
        p = knn_annee(ordre, yp, 1)
        null_dans_tradition.append(metrique_annee(p, yp)["mae"])
    # résidu within-tradition : le signal d'année qui reste après la tradition
    moyennes = {t: float(np.mean(annees[trad == t])) for t in sorted(set(trad.tolist()))}
    residu = np.array([annees[i] - moyennes[trad[i]] for i in range(n)])
    pred_res = knn_annee(ordre, residu, 1)
    for _ in range(n_perm):
        yp = annees.copy()
        for t in sorted(set(trad.tolist())):
            idx = np.where(trad == t)[0]
            vals = yp[idx].copy()
            rng.shuffle(vals)
            yp[idx] = vals
        pm = {t: float(np.mean(yp[trad == t])) for t in sorted(set(trad.tolist()))}
        rp = np.array([yp[i] - pm[trad[i]] for i in range(n)])
        pr = knn_annee(ordre, rp, 1)
        null_residu.append(metrique_annee(pr, rp)["mae"])

    obs_mae = annee["knn"]["1"]["mae"]
    obs_res_mae = metrique_annee(pred_res, residu)["mae"]
    annee["nulls"] = {
        "n": n_perm,
        "global": {"mae_null_moyen": float(np.mean(null_global)), "p": p_unilateral(null_global, obs_mae, "inferieur")},
        "dans_tradition": {"mae_null_moyen": float(np.mean(null_dans_tradition)), "p": p_unilateral(null_dans_tradition, obs_mae, "inferieur")},
        "residu_within_tradition": {
            "mae_observe": obs_res_mae,
            "r2_observe": metrique_annee(pred_res, residu)["r2"],
            "mae_null_moyen": float(np.mean(null_residu)),
            "p": p_unilateral(null_residu, obs_res_mae, "inferieur"),
        },
    }

    # --- prédiction de la tradition ----------------------------------------
    pred_cls = {k: knn_classe(ordre, trad, k) for k in (1, 3, 5)}
    majoritaire = collections.Counter(trad).most_common(1)[0]
    classes = {
        "baseline_majoritaire": {
            "classe": str(majoritaire[0]),
            "exactitude": float(majoritaire[1] / n),
        },
        "knn": {str(k): metrique_classe(pred_cls[k], trad) for k in pred_cls},
    }
    # nulls : étiquettes permutées (global, puis dans chaque tranche de date)
    null_cls_global, null_cls_bins = [], []
    null_cls_global_bal, null_cls_bins_bal = [], []
    for _ in range(n_perm):
        tp = rng.permutation(trad)
        mc = metrique_classe(knn_classe(ordre, tp, 1), tp)
        null_cls_global.append(mc["exactitude"])
        null_cls_global_bal.append(mc["exactitude_equilibree"])
    for _ in range(n_perm):
        tp = trad.copy()
        for b in sorted(set(bins.tolist())):
            idx = np.where(bins == b)[0]
            vals = tp[idx].copy()
            rng.shuffle(vals)
            tp[idx] = vals
        mc = metrique_classe(knn_classe(ordre, tp, 1), tp)
        null_cls_bins.append(mc["exactitude"])
        null_cls_bins_bal.append(mc["exactitude_equilibree"])
    obs_cls = classes["knn"]["1"]["exactitude"]
    obs_bal = classes["knn"]["1"]["exactitude_equilibree"]
    classes["nulls"] = {
        "n": n_perm,
        "global": {
            "exactitude_null_moyenne": float(np.mean(null_cls_global)),
            "p": p_unilateral(null_cls_global, obs_cls),
            "exactitude_equilibree_null_moyenne": float(np.mean(null_cls_global_bal)),
            "p_equilibree": p_unilateral(null_cls_global_bal, obs_bal),
        },
        "dans_bins_date": {
            "exactitude_null_moyenne": float(np.mean(null_cls_bins)),
            "p": p_unilateral(null_cls_bins, obs_cls),
            "exactitude_equilibree_null_moyenne": float(np.mean(null_cls_bins_bal)),
            "p_equilibree": p_unilateral(null_cls_bins_bal, obs_bal),
        },
    }
    classes["classes"] = dict(collections.Counter(trad.tolist()))
    # matrice de confusion (classes réelles -> prédites)
    confusion = {}
    for c in sorted(set(trad)):
        m = trad == c
        confusion[str(c)] = dict(collections.Counter(np.array(pred_cls[1], dtype=object)[m]))

    # --- effet standardisé : comparer les deux z --------------------------
    z_annee_global = (float(np.mean(null_global)) - obs_mae) / (float(np.std(null_global)) or float("nan"))
    z_annee_tradition = (float(np.mean(null_dans_tradition)) - obs_mae) / (float(np.std(null_dans_tradition)) or float("nan"))
    z_trad_global = (obs_cls - float(np.mean(null_cls_global))) / (float(np.std(null_cls_global)) or float("nan"))
    z_trad_bins = (obs_cls - float(np.mean(null_cls_bins))) / (float(np.std(null_cls_bins)) or float("nan"))

    # --- surface : paires eng-eng -----------------------------------------
    surface_eng = None
    paires_eng = [(i, j) for i in range(n) for j in range(i + 1, n)
                  if langue[i] == "eng" and langue[j] == "eng"]
    if len(paires_eng) >= 20:
        ce = np.array([C[i, j] for i, j in paires_eng])
        ste = np.array([trad[i] == trad[j] for i, j in paires_eng])
        dte = np.array([abs(annees[i] - annees[j]) for i, j in paires_eng])
        be, r2e, _ = ols(ce, np.column_stack([ste.astype(float), standardise(np.log1p(dte))]))
        surface_eng = {
            "n_paires": int(len(paires_eng)),
            "n_oeuvres": int(len(set([i for i, _ in paires_eng] + [j for _, j in paires_eng]))),
            "beta": [float(x) for x in be],
            "r2": float(r2e),
            "top1_tradition_dans_eng": None,
            "top1_proche50_dans_eng": None,
        }
        # retrieval restreint aux candidates eng
        same_e, prox_e, n_e = 0, 0, 0
        for i in range(n):
            if langue[i] != "eng":
                continue
            cand = [j for j in ordre[i] if langue[j] == "eng"]
            if not cand:
                continue
            n_e += 1
            same_e += int(trad[cand[0]] == trad[i])
            prox_e += int(abs(annees[cand[0]] - annees[i]) <= SEUIL_PROCHE)
        if n_e:
            chance_t_e, chance_p_e = [], []
            for i in range(n):
                if langue[i] != "eng":
                    continue
                cand = [j for j in ordre[i] if langue[j] == "eng"]
                if not cand:
                    continue
                chance_t_e.append(float(np.mean(trad[cand] == trad[i])))
                chance_p_e.append(float(np.mean(np.abs(annees[cand] - annees[i]) <= SEUIL_PROCHE)))
            surface_eng["top1_tradition_dans_eng"] = float(same_e / n_e)
            surface_eng["top1_proche50_dans_eng"] = float(prox_e / n_e)
            surface_eng["chance_tradition_dans_eng"] = float(np.mean(chance_t_e)) if chance_t_e else None
            surface_eng["chance_proche50_dans_eng"] = float(np.mean(chance_p_e)) if chance_p_e else None
            surface_eng["n_requetes"] = n_e

    # --- sans doublons exacts ---------------------------------------------
    sans_doublons = None
    ordre_sd = ordre_candidats(C, seuil_doublon=0.9999)
    if any(len(o) != n - 1 for o in ordre_sd):
        ret_sd = remplit_detail(retrieval(ordre_sd, annees, trad, auteur), ids_signes)
        sans_doublons = {
            "n_candidats_retires": int(sum((n - 1) - len(o) for o in ordre_sd)),
            "retrieval": {k: ret_sd[k] for k in ("top1_meme_tradition", "top1_meme_auteur",
                                                  "top1_proche_50ans", "chance_meme_tradition",
                                                  "chance_meme_auteur", "chance_proche_50ans")},
        }

    # --- bootstrap par œuvre (IC des taux et du modèle) -------------------
    boot = {"top1_tradition": [], "top1_auteur": [], "top1_proche": [],
            "beta_tradition": [], "beta_date": [], "r2_modele": []}
    for _ in range(n_boot):
        tirage = rng.integers(0, n, n)
        uniq = np.unique(tirage)
        if len(uniq) < 10:
            continue
        # sous-matrice et sous-vecteurs
        Cb = C[np.ix_(uniq, uniq)]
        yb = annees[uniq]
        tb = trad[uniq]
        ab = auteur[uniq]
        ob = ordre_candidats(Cb)
        rb = retrieval(ob, yb, tb, ab)
        boot["top1_tradition"].append(rb["top1_meme_tradition"])
        boot["top1_auteur"].append(rb["top1_meme_auteur"])
        boot["top1_proche"].append(rb["top1_proche_50ans"])
        paires_b = [(i, j) for i in range(len(uniq)) for j in range(i + 1, len(uniq))]
        cb = np.array([Cb[i, j] for i, j in paires_b])
        db = np.array([abs(yb[i] - yb[j]) for i, j in paires_b])
        sb = np.array([tb[i] == tb[j] for i, j in paires_b])
        bb, r2b, _ = ols(cb, np.column_stack([sb.astype(float), standardise(np.log1p(db))]))
        boot["beta_tradition"].append(float(bb[1]))
        boot["beta_date"].append(float(bb[2]))
        boot["r2_modele"].append(float(r2b))

    bootstrap = {
        "n_demandes": n_boot,
        "n_valides": len(boot["top1_tradition"]),
        "top1_meme_tradition": {"moyenne": float(np.mean(boot["top1_tradition"])), "ic95": ic95(boot["top1_tradition"])},
        "top1_meme_auteur": {"moyenne": float(np.mean(boot["top1_auteur"])), "ic95": ic95(boot["top1_auteur"])},
        "top1_proche_50ans": {"moyenne": float(np.mean(boot["top1_proche"])), "ic95": ic95(boot["top1_proche"])},
        "beta_tradition": {"moyenne": float(np.mean(boot["beta_tradition"])), "ic95": ic95(boot["beta_tradition"])},
        "beta_date": {"moyenne": float(np.mean(boot["beta_date"])), "ic95": ic95(boot["beta_date"])},
        "r2_modele": {"moyenne": float(np.mean(boot["r2_modele"])), "ic95": ic95(boot["r2_modele"])},
    }

    # --- permutations de signatures (contrôle négatif) --------------------
    null_sig = {"top1_tradition": [], "top1_auteur": [], "top1_proche": []}
    for _ in range(min(n_perm, 2000)):
        perm = rng.permutation(n)
        Cp = C[np.ix_(perm, perm)]
        op = ordre_candidats(Cp)
        rp = retrieval(op, annees, trad, auteur)
        null_sig["top1_tradition"].append(rp["top1_meme_tradition"])
        null_sig["top1_auteur"].append(rp["top1_meme_auteur"])
        null_sig["top1_proche"].append(rp["top1_proche_50ans"])
    signatures_permutees = {
        "n": len(null_sig["top1_tradition"]),
        "top1_tradition_null_moyen": float(np.mean(null_sig["top1_tradition"])),
        "top1_auteur_null_moyen": float(np.mean(null_sig["top1_auteur"])),
        "top1_proche_null_moyen": float(np.mean(null_sig["top1_proche"])),
        "p_top1_tradition": p_unilateral(null_sig["top1_tradition"], ret["top1_meme_tradition"]),
        "p_top1_auteur": p_unilateral(null_sig["top1_auteur"], ret["top1_meme_auteur"]),
        "p_top1_proche": p_unilateral(null_sig["top1_proche"], ret["top1_proche_50ans"]),
    }

    # --- tentative de reproduction du modèle v150 ------------------------
    # v150 : d_sig ~ 1 + d_graph + Δyear/1000 + même_tradition, R² = 0,3004,
    # beta publiés [0,1594 ; 0,0489 ; 0,1378 ; 0,0022]. On reconstruit d_sig
    # par la distance L2 des 14 atomes sur les paires qui ont un d_topo.
    d_topo_lookup = {}
    # paires_brutes est passé par l'appelant via textes ? non : on le lit ici
    # une seule fois, en lecture seule.
    for p in lire_json(PAIRES)["pairs"]:
        d_topo_lookup[(p["a"], p["b"])] = float(p["d_topo"])
        d_topo_lookup[(p["b"], p["a"])] = float(p["d_topo"])
    lignes_v150 = []
    idx_v150 = []
    for i in range(n):
        for j in range(i + 1, n):
            cle = (ids_signes[i], ids_signes[j])
            if cle not in d_topo_lookup:
                continue
            d_sig = float(np.linalg.norm(X[i] - X[j]))
            lignes_v150.append((
                d_sig, d_topo_lookup[cle], abs(annees[i] - annees[j]) / 1000.0,
                float(trad[i] == trad[j]),
            ))
            idx_v150.append((i, j))
    v150 = None
    if len(lignes_v150) >= 20:
        A = np.array(lignes_v150, dtype=float)
        dv, tv, dyv, stv = A[:, 0], A[:, 1], A[:, 2], A[:, 3]
        bv, r2v, _ = ols(dv, np.column_stack([tv, dyv, stv]))
        bv_std, _, _ = ols(
            standardise(dv), np.column_stack([standardise(tv), standardise(dyv), stv])
        )
        # p de permutation (années permutées entre les 44 œuvres) pour le
        # coefficient de date du modèle v150 reconstruit.
        rng_v150 = np.random.default_rng(graine + 13)
        null_v150 = []
        for _ in range(min(n_perm, 2000)):
            yp = rng_v150.permutation(annees)
            dyp = np.array([ab[1] for ab in [(0, abs(yp[i] - yp[j]) / 1000.0) for i, j in idx_v150]])
            bvp, _, _ = ols(dv, np.column_stack([tv, dyp, stv]))
            null_v150.append(float(bvp[2]))
        v150 = {
            "n_paires": int(len(dv)),
            "formule": "d_sig(L2 V14) ~ 1 + d_topo + Δannée/1000 + même_tradition",
            "beta_brut": [float(x) for x in bv],
            "beta_standardise": [float(x) for x in bv_std],
            "r2": float(r2v),
            "date_coef": float(bv[2]),
            "date_coef_null_moyen": float(np.mean(null_v150)) if null_v150 else None,
            "date_p_permutation": p_bilateral(null_v150, float(bv[2])) if null_v150 else None,
            "date_n_permutations": len(null_v150),
            "publie_v150": {
                "beta": [0.1594, 0.0489, 0.1378, 0.0022],
                "r2": 0.3004,
                "formule": "d_sig ~ 1 + d_graph + Δyear/1000 + même_tradition",
            },
            "lecture": "le coefficient de date reconstruit est négatif ; le +0,138 publié n'est pas reproduit sur les 44 signatures du §334",
        }

    return {
        "n": n,
        "v150": v150,
        "retrieval": ret,
        "retrieval_nulls": retrieval_nulls,
        "bins_retrieval": bins_retrieval,
        "modele_cos": modele_cos,
        "prediction": {
            "annee": annee,
            "tradition": classes,
            "confusion": confusion,
            "comparaison_effets": {
                "z_annee_global": float(z_annee_global),
                "z_annee_dans_tradition": float(z_annee_tradition),
                "z_tradition_global": float(z_trad_global),
                "z_tradition_dans_bins_date": float(z_trad_bins),
                "lecture": "z = (null - observé)/écart-type du null pour l'erreur d'année ; (observé - null)/écart-type pour l'exactitude de tradition",
            },
        },
        "surface_eng": surface_eng,
        "sans_doublons": sans_doublons,
        "bootstrap": bootstrap,
        "signatures_permutees": signatures_permutees,
        "oeuvres": [
            {
                "id": t,
                "annee": textes[t]["annee"],
                "tradition_fine": textes[t]["tradition_fine"],
                "tradition_large": textes[t]["tradition_large"],
                "auteur": textes[t]["auteur"],
                "langue_source": textes[t]["langue_source"],
                "signature": textes[t]["signature"],
            }
            for t in ids_signes
        ],
    }


# ---------------------------------------------------------------------------
# 4. Synthèse et sortie
# ---------------------------------------------------------------------------

def synthese(audit, paires, oeuvres):
    tests = [
        ("retrieval_filiation", "top1 même tradition > null à date contrôlée",
         oeuvres["retrieval_nulls"]["filiation_controlee"]["p_top1_meme_tradition"]),
        ("retrieval_epoque", "top1 proche ≤50 ans > null à filiation contrôlée",
         oeuvres["retrieval_nulls"]["date_controlee"]["p_top1_proche_50ans"]),
        ("prediction_filiation", "exactitude tradition > null dans les tranches de date",
         oeuvres["prediction"]["tradition"]["nulls"]["dans_bins_date"]["p"]),
        ("prediction_epoque", "MAE année < null dans chaque tradition",
         oeuvres["prediction"]["annee"]["nulls"]["dans_tradition"]["p"]),
    ]
    # Holm-Bonferroni sur les 4 tests principaux.
    m = len(tests)
    ordre = sorted(range(m), key=lambda k: tests[k][2])
    p_holm = [None] * m
    courant = 0.0
    for rang, k in enumerate(ordre):
        valeur = min(1.0, tests[k][2] * (m - rang))
        courant = max(courant, valeur)
        p_holm[k] = courant
    tests_principaux = [
        {"nom": nom, "hypothese": hyp, "p_brut": float(pv), "p_holm": float(ph)}
        for (nom, hyp, pv), ph in zip(tests, p_holm)
    ]
    return {
        "tests_principaux": tests_principaux,
        "audit": {
            "corpus_actif_officiel": audit["corpus_actif_officiel"],
            "paires": audit["paires"],
            "textes_distincts_paires": audit["textes_distincts_paires"],
            "textes_absents_des_paires": audit["textes_absents_des_paires"],
            "oeuvres_signees": audit["oeuvres_signees"],
            "sources_ok": audit["sources_ok"],
            "sources_manifeste": audit["sources_manifeste"],
            "sources_ok_parmi_44": audit["sources_ok_parmi_44"],
            "urls_uniques_non_vides": audit["urls_uniques_non_vides"],
            "paires_uniques": paires["n_paires_uniques"],
            "paires_auto": paires["n_auto_paires"],
            "paires_doublons_lignes": paires["n_doublons_lignes"],
            "paires_inference": paires["n_paires"],
        },
        "paires": {
            "r2_h0": paires["modeles"]["H0"]["r2"],
            "r2_h0_655": paires["modeles"]["H0"]["r2_655_lignes"],
            "n_paires_inference": paires["n_paires"],
            "r2_date": paires["modeles"]["date_seule"]["r2"],
            "partiel_topo_apres_date": paires["modeles"]["joint"]["partiel_topo_apres_date"],
            "partiel_date_apres_topo": paires["modeles"]["joint"]["partiel_date_apres_topo"],
            "beta_date_joint": paires["modeles"]["joint"]["beta"][2],
            "n_meme_tradition": paires["positivite"]["n_meme_tradition"],
            "dy_moyen_meme_tradition": paires["positivite"]["dy_meme_tradition"]["moyenne"],
            "dy_moyen_tradition_differente": paires["positivite"]["dy_tradition_differente"]["moyenne"],
            "delta_bin_axial": paires["contraste_date_surface"]["bin_axial"]["delta"],
            "p_filiation_date_controlee": paires["contraste_date_surface"]["permutation_date_controlee"]["bin_axial"]["p"],
            "delta_eng": paires["contraste_date_surface"]["meme_langue_eng"]["delta"],
            "p_filiation_date_surface_controlee": paires["contraste_date_surface"]["permutation_date_controlee"]["meme_langue_eng"]["p"],
        },
        "oeuvres": {
            "top1_meme_tradition": oeuvres["retrieval"]["top1_meme_tradition"],
            "chance_meme_tradition": oeuvres["retrieval"]["chance_meme_tradition"],
            "top1_meme_auteur": oeuvres["retrieval"]["top1_meme_auteur"],
            "chance_meme_auteur": oeuvres["retrieval"]["chance_meme_auteur"],
            "top1_proche_50ans": oeuvres["retrieval"]["top1_proche_50ans"],
            "chance_proche_50ans": oeuvres["retrieval"]["chance_proche_50ans"],
            "p_top1_tradition_bins": oeuvres["retrieval_nulls"]["filiation_controlee"]["p_top1_meme_tradition"],
            "p_tradition_prediction_equilibree": oeuvres["prediction"]["tradition"]["nulls"]["dans_bins_date"]["p_equilibree"],
            "p_top1_proche_tradition": oeuvres["retrieval_nulls"]["date_controlee"]["p_top1_proche_50ans"],
            "top1_proche_null_date": oeuvres["retrieval_nulls"]["date_controlee"]["top1_proche_50ans_null_moyen"],
            "top1_tradition_null_bins": oeuvres["retrieval_nulls"]["filiation_controlee"]["top1_meme_tradition_null_moyen"],
            "mae_annee_knn1": oeuvres["prediction"]["annee"]["knn"]["1"]["mae"],
            "r2_annee_knn1": oeuvres["prediction"]["annee"]["knn"]["1"]["r2"],
            "mae_annee_null_dans_tradition": oeuvres["prediction"]["annee"]["nulls"]["dans_tradition"]["mae_null_moyen"],
            "residu_within_tradition_r2": oeuvres["prediction"]["annee"]["nulls"]["residu_within_tradition"]["r2_observe"],
            "residu_within_tradition_p": oeuvres["prediction"]["annee"]["nulls"]["residu_within_tradition"]["p"],
            "p_tradition_prediction_equilibree": oeuvres["prediction"]["tradition"]["nulls"]["dans_bins_date"]["p_equilibree"],
            "surface_eng": oeuvres.get("surface_eng"),
            "v150": oeuvres.get("v150"),
        },
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="J12.1 — Panini §334 et les 44 signatures")
    ap.add_argument("--sortie", default=str(SORTIE_DEFAUT))
    ap.add_argument("--rapide", action="store_true", help="permutations et bootstrap réduits")
    ap.add_argument("--graine", type=int, default=0)
    args = ap.parse_args(argv)

    n_perm = 500 if args.rapide else 5000
    n_boot_paires = 300 if args.rapide else 1000
    n_boot_oeuvres = 300 if args.rapide else 1000

    paires_brutes, graphe, signatures, revalidation, textes, ids_paires, ids_signes, audit = charger()
    paires = analyser_paires(
        paires_brutes, textes, ids_paires,
        n_perm=min(n_perm, 2000), n_boot=n_boot_paires, graine=args.graine,
    )
    oeuvres = analyser_oeuvres(
        textes, ids_signes,
        n_perm=n_perm, n_boot=n_boot_oeuvres, graine=args.graine + 1,
    )

    resultat = {
        "tache": "J12.1",
        "titre": "Panini — le §334 et les 44 œuvres : retrieval et prédiction de l'époque vs la filiation, à date contrôlée",
        "date": "2026-11-14",
        "graine": args.graine,
        "sources": {
            "paires": {"chemin": str(PAIRES.relative_to(RACINE.parent)), "sha256": sha256(PAIRES)},
            "graphe": {"chemin": str(GRAPHE.relative_to(RACINE.parent)), "sha256": sha256(GRAPHE)},
            "signatures": {"chemin": str(SIGNATURES.relative_to(RACINE.parent)), "sha256": sha256(SIGNATURES)},
            "revalidation": {"chemin": str(REVALIDATION.relative_to(RACINE.parent)), "sha256": sha256(REVALIDATION)},
            "couverture": {"chemin": str(COUVERTURE.relative_to(RACINE.parent)), "sha256": sha256(COUVERTURE)},
            "manifeste": {"chemin": str(MANIFESTE.relative_to(RACINE.parent)), "sha256": sha256(MANIFESTE)},
            "v150": {"chemin": str(V150.relative_to(RACINE.parent)), "sha256": sha256(V150)},
            "commit_panini": commit_git(PANINI),
            "commit_drave": commit_git(RACINE),
        },
        "audit": audit,
        "paires": paires,
        "oeuvres": oeuvres,
        "synthese": synthese(audit, paires, oeuvres),
        "limites": [
            "les 655 paires ne mettent en jeu que 48 textes distincts (44 signés) ; les 114 textes actifs sont une étiquette de corpus, pas un échantillon de retrieval",
            "les signatures des 44 œuvres ne sont pas les vecteurs qui produisent d_lex/cos des 655 paires : cos recalculé vs cos du fichier, r ≈ 0,37 sur 490 paires",
            "la date est la date de composition (ou son estimation), pas la date de traduction ; 24/44 sources sont anglaises, 1 française, 19 de langue inconnue",
            "d_topo est une distance de tradition/transmission, pas une distance de famille de langues ; elle est corrélée à l'écart de dates",
            "les couples de même tradition sont presque tous contemporains (max 230 ans) ; les couples longs sont presque tous inter-traditions : le plan ne sépare pas complètement époque et filiation",
            "les paires ne sont pas indépendantes : les tests de paire sont permutés au niveau des textes et les IC sont des bootstrap par texte",
            "les 44 œuvres sont peu nombreuses et les classes de tradition sont déséquilibrées (19 GRECO sur 44) ; l'exactitude équilibrée est le chiffre à lire, pas l'exactitude brute",
            "les seuils (50 ans, 250 ans, cos 0,99999) sont des conventions ; les sensibilités sont dans le JSON",
        ],
    }

    sortie = pathlib.Path(args.sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=1), encoding="utf-8")

    s = resultat["synthese"]
    print("J12.1 — Panini §334 et 44 signatures")
    print(f"audit : {s['audit']}")
    print(f"paires : H0 R2={s['paires']['r2_h0']:.6f} | date R2={s['paires']['r2_date']:.4f} | "
          f"partiel date|topo={s['paires']['partiel_date_apres_topo']:.4f} | "
          f"partiel topo|date={s['paires']['partiel_topo_apres_date']:.4f}")
    print(f"œuvres : top1 tradition={s['oeuvres']['top1_meme_tradition']:.3f} "
          f"(hasard {s['oeuvres']['chance_meme_tradition']:.3f}, p_bins={s['oeuvres']['p_top1_tradition_bins']:.4f}) | "
          f"top1 proche50={s['oeuvres']['top1_proche_50ans']:.3f} "
          f"(hasard {s['oeuvres']['chance_proche_50ans']:.3f}, p_trad={s['oeuvres']['p_top1_proche_tradition']:.4f})")
    print(f"prédiction : MAE année={s['oeuvres']['mae_annee_knn1']:.1f} "
          f"(R2={s['oeuvres']['r2_annee_knn1']:.3f}, null dans tradition={s['oeuvres']['mae_annee_null_dans_tradition']:.1f}) | "
          f"résidu within-tradition R2={s['oeuvres']['residu_within_tradition_r2']:.3f} p={s['oeuvres']['residu_within_tradition_p']:.4f}")
    print(f"écrit : {sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
