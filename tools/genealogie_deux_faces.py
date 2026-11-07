#!/usr/bin/env python3
"""genealogie_deux_faces.py — J3.2 : la généalogie à deux faces.

POURQUOI. Panini tient une **théorie** de la généalogie (14 atomes, 9 dhātus, une échelle de
distance à quatre niveaux) ; Drave tient une **mesure** de l'alignement (Glottolog + retrieval sur
le corpus commun). Les deux faces ne mesurent pas la même chose : l'une est une signature de texte,
l'autre une distance de langues. Ce script les confronte sur les 21 langues du corpus commun et sur
les signatures de Panini, et écrit les chiffres dans `reports/genealogie-deux-faces.json`.

CE QUI EST MESURÉ.
  1. Couverture des trois représentations généalogiques : `lang_distance` de Panini (LANG_TREE),
     les métadonnées UDHR de Panini, Glottolog.
  2. Accord des deux faces sur les langues couvertes (famille, branche, distances).
  3. Alignement : retrieval UDHR (J3.1) vs distance Panini / Glottolog, avec le script en contrôle.
     Contrôles négatifs : permutations de labels et de chemins, leave-one-language-out, et
     décomposition de l'effet « inconnu ».
  4. Atomes : ACP des 14 parts (44 œuvres), stabilité split-half, contrôle par permutation ;
     ce que les 9 dhātus peuvent et ne peuvent pas être mesurés.
  5. L'avertissement §150 de Panini : reproduction des β et vérification de ce que « filiation »
     veut dire dans leur corpus (presque aucune paire inter-langues).

SORTIE. `reports/genealogie-deux-faces.json` (versionné). Aucune écriture dans Panini.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
from scipy import stats

RACINE = Path(__file__).resolve().parent.parent
RAPPORTS = RACINE / "reports"
PANINI_DEFAUT = RACINE.parent / "Panini" / "research"

V14 = ["ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS", "MODALITÉ",
       "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION", "STRUCTURE", "SYMÉTRIE", "ÉQUATION"]
DHATUS_SANSKRIT = ["BHŪ", "KR", "STHĀ", "DĀ", "JÑĀ", "BUDH", "MAN", "VAC", "DṚŚ"]
DHATUS_COMPUTATIONNELS = ["EXIST", "TRANS", "EVAL", "LOCATE", "FEEL", "ACT", "QUAL", "REL", "KNOW"]

# La nomenclature de Panini n'est pas toujours celle de Glottolog : « Niger-Congo » est la
# famille large, « Atlantic-Congo » le nœud Glottolog qui la contient. On garde les deux
# lectures (brute et appariée) et on le dit.
FAMILLE_PANINI_VERS_GLOTTO = {"Niger-Congo": "Atlantic-Congo"}

# Branche Panini → nœud Glottolog le plus proche. Pour « Tibeto-Burman », le nœud exact
# (tibe1272) n'est pas dans le chemin de mya ; burm1265 est le descendant le plus proche.
BRANCHE_PANINI_VERS_GLOTTO = {
    "Germanic": "germ1287",
    "Indo-Iranian": "indo1320",
    "Slavic": "slav1255",
    "Hellenic": "grae1234",
    "Bantu": "bant1294",
    "Volta-Niger": "volt1241",
    "Malayo-Polynesian": "mala1545",
    "Tibeto-Burman": "burm1265",
    "Sinitic": "sini1245",
    "Semitic": "semi1276",
    "Chadic": "chad1250",
    "Romance": "roma1334",
}
BRANCHES_EXACTES = {k: v for k, v in BRANCHE_PANINI_VERS_GLOTTO.items() if k != "Tibeto-Burman"}


# ---------------------------------------------------------------------------
# Chargement
# ---------------------------------------------------------------------------

def lire_json(chemin: Path):
    return json.loads(chemin.read_text(encoding="utf-8"))


def charger_corpus(rapports: Path):
    corpus = lire_json(rapports / "corpus-commun.json")
    retrieval = lire_json(rapports / "retrieval-epoque.json")
    textes = corpus["textes"]
    paires = retrieval["udhr"]["paires"]

    ids = [t["id"] for t in textes]
    index = {x: i for i, x in enumerate(ids)}
    mrr, top1 = {}, {}
    for p in paires:
        cle = tuple(sorted((p["a"], p["b"])))
        mrr.setdefault(cle, []).append(float(p["mrr"]))
        top1.setdefault(cle, []).append(float(p["top1"]))
    mrr = {k: float(np.mean(v)) for k, v in mrr.items()}
    top1 = {k: float(np.mean(v)) for k, v in top1.items()}
    return corpus, retrieval, textes, ids, index, mrr, top1


def charger_lang_tree(panini: Path):
    """Lit LANG_TREE sans importer Panini (dépendances absentes côté Drave)."""
    source = (panini / "src" / "nipada" / "signing" / "language_genealogy.py").read_text(encoding="utf-8")
    bloc = source.split("LANG_TREE: dict[str, LangInfo] = {", 1)[1].split("\n}", 1)[0]
    entries = {}
    for m in re.finditer(
        r'"([a-z]{3})":\s*LangInfo\(\s*"([a-z]{3})",\s*"([^"]+)",\s*"([^"]+)"', bloc
    ):
        entries[m.group(1)] = {"family": m.group(3), "branch": m.group(4)}
    return entries


# ---------------------------------------------------------------------------
# Distances
# ---------------------------------------------------------------------------

def distance_lang_tree(a: str, b: str, tree: dict) -> float:
    """La fonction `lang_distance` de Panini, réimplémentée à l'identique."""
    if a == b:
        return 0.0
    if a not in tree or b not in tree:
        return 1.0
    if tree[a]["family"] != tree[b]["family"]:
        return 0.75
    if tree[a]["branch"] == tree[b]["branch"]:
        return 0.15
    return 0.40


def distance_panini_udhr(a: dict, b: dict) -> float:
    """L'échelle de Panini appliquée à leurs métadonnées UDHR (famille, branche)."""
    if a["id"] == b["id"]:
        return 0.0
    if a["famille_panini"] == "Other" or b["famille_panini"] == "Other":
        return 1.0
    if a["famille_panini"] != b["famille_panini"]:
        return 0.75
    if a["branche_panini"] == b["branche_panini"]:
        return 0.15
    return 0.40


def chemin_glottolog(t: dict) -> list[str]:
    return t["branche"].split("/") if t.get("branche") else []


def lca_glottolog(a: dict, b: dict) -> tuple[int, str]:
    p, q = chemin_glottolog(a), chemin_glottolog(b)
    d = 0
    for x, y in zip(p, q):
        if x == y:
            d += 1
        else:
            break
    return d, (p[d - 1] if d else "")


def distance_glottolog(a: dict, b: dict) -> float:
    """Distance de chemin normalisée : (|a|+|b|-2·lca)/(|a|+|b|-2)."""
    if a["id"] == b["id"]:
        return 0.0
    p, q = chemin_glottolog(a), chemin_glottolog(b)
    d, _ = lca_glottolog(a, b)
    return (len(p) - d + len(q) - d) / max(1, len(p) + len(q) - 2)


# ---------------------------------------------------------------------------
# Statistiques
# ---------------------------------------------------------------------------

def ols(X: np.ndarray, y: np.ndarray) -> dict:
    X = np.column_stack([np.ones(len(y)), X])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    pred = X @ b
    ssr = float(((y - pred) ** 2).sum())
    sst = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - ssr / sst if sst else 0.0
    n, k = X.shape
    sigma2 = ssr / max(1, n - k)
    se = np.sqrt(np.diag(sigma2 * np.linalg.pinv(X.T @ X)))
    t = np.divide(b, se, out=np.zeros_like(b), where=se > 0)
    p = 2 * (1 - stats.t.cdf(np.abs(t), max(1, n - k)))
    aic = n * np.log(ssr / n) + 2 * k if ssr > 0 else float("inf")
    return {"b": b.tolist(), "se": se.tolist(), "t": t.tolist(), "p": p.tolist(),
            "r2": float(r2), "aic": float(aic), "n": int(n), "k": int(k)}


def stats_groupe(masque: np.ndarray, y: np.ndarray) -> dict:
    x = y[masque]
    if len(x) == 0:
        return {"n": 0}
    plancher = 1.0 / 30.0 * sum(1.0 / i for i in range(1, 31))  # MRR du hasard sur 30 candidats
    above = x > plancher + 1e-6
    return {
        "n": int(len(x)),
        "moyenne": float(x.mean()),
        "mediane": float(np.median(x)),
        "min": float(x.min()),
        "max": float(x.max()),
        "au_dessus_du_hasard": int(above.sum()),
        "part_au_dessus_du_hasard": float(above.mean()),
        "moyenne_au_dessus": float(x[above].mean()) if above.any() else None,
    }


def pca_correlation(M: np.ndarray):
    """ACP sur la matrice de corrélation (convention J2.1)."""
    Z = (M - M.mean(0)) / M.std(0, ddof=1)
    C = np.cov(Z, rowvar=False)
    ev, V = np.linalg.eigh(C)
    ordre = np.argsort(ev)[::-1]
    return ev[ordre], V[:, ordre]


def pca_covariance(M: np.ndarray):
    Z = M - M.mean(0)
    C = np.cov(Z, rowvar=False)
    ev, V = np.linalg.eigh(C)
    ordre = np.argsort(ev)[::-1]
    return ev[ordre], V[:, ordre]


def n_pour_variance(ev: np.ndarray, seuil: float) -> int:
    return int(np.searchsorted(np.cumsum(ev) / ev.sum(), seuil) + 1)


def sous_espace(M: np.ndarray, k: int) -> np.ndarray:
    _, V = pca_correlation(M)
    return V[:, :k]


# ---------------------------------------------------------------------------
# Programme
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="J3.2 — la généalogie à deux faces")
    ap.add_argument("--panini", default=str(PANINI_DEFAUT), help="racine de Panini/research")
    ap.add_argument("--sortie", default=str(RAPPORTS / "genealogie-deux-faces.json"))
    ap.add_argument("--permutations", type=int, default=1000)
    ap.add_argument("--graine", type=int, default=0)
    a = ap.parse_args()

    panini = Path(a.panini)
    if not (panini / "nipada" / "falsification" / "analytic_sigs_v1.json").exists():
        print(f"ERREUR : {panini} introuvable ou incomplet (lecture seule requise)")
        return 2
    rng = np.random.default_rng(a.graine)

    corpus, retrieval, textes, ids, index, mrr, top1 = charger_corpus(RAPPORTS)
    tree = charger_lang_tree(panini)
    sigs = lire_json(panini / "nipada" / "falsification" / "analytic_sigs_v1.json")
    validation = lire_json(panini / "nipada" / "falsification" / "nipada_v150_validation.json")
    udhr_panini = lire_json(panini / "data" / "udhr_corpus.json")
    decompose = lire_json(panini / "data" / "udhr_decomposed_v14.json")
    convergence_v14 = lire_json(panini / "data" / "udhr_convergence_v14.json")
    paires334 = lire_json(panini / "nipada" / "falsification" / "pairs334_axes_v1.json")

    n = len(textes)
    paires = [(i, j) for i in range(n) for j in range(i + 1, n)]
    cle = lambda i, j: tuple(sorted((ids[i], ids[j])))
    y = np.array([mrr[cle(i, j)] for i, j in paires], float)
    y_top = np.array([top1[cle(i, j)] for i, j in paires], float)
    script = np.array([float(textes[i]["script"] == textes[j]["script"]) for i, j in paires])

    P1 = np.array([distance_lang_tree(textes[i]["iso3"], textes[j]["iso3"], tree) for i, j in paires])
    P2 = np.array([distance_panini_udhr(textes[i], textes[j]) for i, j in paires])
    G = np.array([distance_glottolog(textes[i], textes[j]) for i, j in paires])
    labelise = P2 != 1.0
    inconnu = ~labelise

    # ---- 1. Couverture -----------------------------------------------------
    fam_panini = {}
    for v in udhr_panini["languages"].values():
        fam_panini[v["family"]] = fam_panini.get(v["family"], 0) + 1
    n_panini_connues = sum(1 for v in udhr_panini["languages"].values() if v["family"] != "Other")
    iso_communs = {t["iso3"] for t in textes}
    decompose_communs = sorted(iso_communs & set(decompose["results"]))
    convergence_communs = sorted(iso_communs & set(convergence_v14))
    tree_communs = sorted(iso_communs & set(tree))
    panini_udhr_communs = sorted(t["iso3"] for t in textes if t["famille_panini"] != "Other")
    glotto_communs = sorted(t["iso3"] for t in textes if t.get("branche"))
    non_labelises = sorted(t["iso3"] for t in textes if t["famille_panini"] == "Other")

    # ---- 2. Accord des deux faces sur les 15 couvertes ----------------------
    labelise_textes = [t for t in textes if t["famille_panini"] != "Other"]
    accord_famille_brut = 0
    accord_famille_mappe = 0
    desaccords_famille_brute = []
    desaccords_famille_mappee = []
    accord_branche_exact = 0
    accord_branche_proche = 0
    desaccords_branche_exacte = []
    desaccords_branche = []
    for t in labelise_textes:
        f_glotto = t["famille"]
        f_panini = t["famille_panini"]
        if f_panini == f_glotto:
            accord_famille_brut += 1
            accord_famille_mappe += 1
        elif FAMILLE_PANINI_VERS_GLOTTO.get(f_panini) == f_glotto:
            accord_famille_mappe += 1
            desaccords_famille_brute.append({
                "id": t["id"], "panini": f_panini, "glottolog": f_glotto,
                "note": "nomenclature : Niger-Congo est la famille large, Atlantic-Congo le nœud Glottolog",
            })
        else:
            desaccords_famille_mappee.append({"id": t["id"], "panini": f_panini,
                                              "glottolog": f_glotto})
        noeud = BRANCHE_PANINI_VERS_GLOTTO.get(t["branche_panini"])
        path = chemin_glottolog(t)
        if noeud and noeud in path:
            accord_branche_proche += 1
            if t["branche_panini"] == "Tibeto-Burman":
                desaccords_branche_exacte.append({
                    "id": t["id"], "panini": t["branche_panini"], "noeud": noeud,
                    "note": "le nœud exact tibe1272 n'est pas dans le chemin Glottolog ; "
                            "burm1265 est le descendant le plus proche",
                })
            else:
                accord_branche_exact += 1
        else:
            desaccords_branche.append({"id": t["id"], "panini": t["branche_panini"],
                                       "glottolog": t["branche"], "noeud_attendu": noeud})
    # distances P2 vs G sur les paires couvertes
    x_p2 = P2[labelise]
    x_g = G[labelise]
    spearman_p2_g = stats.spearmanr(x_p2, x_g)
    pearson_p2_g = stats.pearsonr(x_p2, x_g)
    # P1 vs P2 sur les 5 langues de LANG_TREE
    paires_p1 = [(i, j) for i, j in paires
                 if textes[i]["iso3"] in tree and textes[j]["iso3"] in tree]
    p1_p2_vals = [(distance_lang_tree(textes[i]["iso3"], textes[j]["iso3"], tree),
                   distance_panini_udhr(textes[i], textes[j])) for i, j in paires_p1]

    # ---- 3. Alignement -----------------------------------------------------
    plancher_mrr = float(np.mean([1.0 / i for i in range(1, 31)]))
    plancher_top1 = 1.0 / 30.0
    groupes = {}
    for nom, D in [("panini_lang_tree", P1), ("panini_udhr", P2), ("glottolog", G)]:
        groupes[nom] = {}
        for v in sorted(set(np.round(D, 6))):
            m = np.isclose(D, v)
            groupes[nom][f"{v:.2f}"] = {**stats_groupe(m, y),
                                        "script_meme": float(script[m].mean()) if m.any() else None,
                                        "top1_moyen": float(y_top[m].mean()) if m.any() else None}
    # table script × famille
    table_script_famille = []
    for fam in [True, False]:
        for sc in [True, False]:
            m = np.array([(textes[i]["famille"] == textes[j]["famille"]) == fam
                          and (textes[i]["script"] == textes[j]["script"]) == sc for i, j in paires])
            table_script_famille.append({"famille_meme": fam, "script_meme": sc,
                                         **stats_groupe(m, y)})
    # liste des paires même famille + même script
    paires_famille_script = []
    for i, j in paires:
        if textes[i]["famille"] == textes[j]["famille"] and script[paires.index((i, j))]:
            paires_famille_script.append({
                "a": ids[i], "b": ids[j], "mrr": float(y[paires.index((i, j))]),
                "top1": float(y_top[paires.index((i, j))]), "panini": float(P2[paires.index((i, j))]),
                "branche_a": textes[i]["branche_panini"], "branche_b": textes[j]["branche_panini"],
            })
    # régressions
    def regression(nom, D, masque=None):
        if masque is None:
            masque = np.ones(len(y), bool)
        cols = [script[masque]]
        if D is not None:
            cols.append(D[masque])
        r = ols(np.column_stack(cols), y[masque])
        res = {"nom": nom, "n": int(masque.sum()),
               "coef_script": r["b"][1], "p_script": r["p"][1],
               "r2": r["r2"], "aic": r["aic"]}
        if D is not None:
            res.update({"coef_distance": r["b"][2], "p_distance": r["p"][2]})
        return res
    regressions = {
        "toutes": [regression("script", None),
                   regression("script+panini_lang_tree", P1),
                   regression("script+panini_udhr", P2),
                   regression("script+glottolog", G)],
        "labelisees": [regression("script", None, labelise),
                       regression("script+panini_lang_tree", P1, labelise),
                       regression("script+panini_udhr", P2, labelise),
                       regression("script+glottolog", G, labelise)],
    }
    # décomposition « inconnu » : distance seulement sur les paires couvertes + indicateur
    def decomposition(nom, D):
        Dl = np.where(labelise, D, 0.0)
        X = np.column_stack([script, Dl, inconnu.astype(float)])
        r = ols(X, y)
        return {"nom": nom, "coef_script": r["b"][1], "coef_distance": r["b"][2],
                "coef_inconnu": r["b"][3], "p_distance": r["p"][2], "p_inconnu": r["p"][3],
                "r2": r["r2"], "aic": r["aic"], "n": int(len(y))}
    decomposition_inconnu = [decomposition("panini_udhr", P2), decomposition("glottolog", G)]

    # permutations de labels / chemins
    def permuter(nom, iterations):
        if nom == "panini_udhr":
            D = P2
        elif nom == "glottolog":
            D = G
        else:
            D = P1

        def coef(Dv, masque):
            return ols(np.column_stack([script[masque], Dv[masque]]), y[masque])["b"][2]

        obs = {"toutes": coef(D, np.ones(len(y), bool)), "labelisees": coef(D, labelise)}
        nul = {"toutes": [], "labelisees": []}
        for _ in range(iterations):
            perm = rng.permutation(n)
            if nom == "panini_udhr":
                fam = [textes[k]["famille_panini"] for k in perm]
                br = [textes[k]["branche_panini"] for k in perm]

                def dd(i, j):
                    if fam[i] == "Other" or fam[j] == "Other":
                        return 1.0
                    if fam[i] != fam[j]:
                        return 0.75
                    return 0.15 if br[i] == br[j] else 0.40
            elif nom == "glottolog":
                paths = [chemin_glottolog(textes[k]) for k in perm]

                def dd(i, j):
                    p, q = paths[i], paths[j]
                    d = 0
                    for x, z in zip(p, q):
                        if x == z:
                            d += 1
                        else:
                            break
                    return (len(p) - d + len(q) - d) / max(1, len(p) + len(q) - 2)
            else:
                isos = [textes[k]["iso3"] for k in perm]

                def dd(i, j):
                    return distance_lang_tree(isos[i], isos[j], tree)

            Dv = np.array([dd(i, j) for i, j in paires])
            for masque_nom, masque in [("toutes", np.ones(len(y), bool)), ("labelisees", labelise)]:
                nul[masque_nom].append(float(coef(Dv, masque)))
        res = {}
        for k in nul:
            arr = np.array(nul[k])
            p = (int(np.sum(arr <= obs[k])) + 1) / (len(arr) + 1)
            res[k] = {"observe": float(obs[k]), "p": float(p),
                      "nul_moyenne": float(arr.mean()),
                      "nul_2_5": float(np.percentile(arr, 2.5)),
                      "nul_97_5": float(np.percentile(arr, 97.5))}
        return {"representation": nom, "n_permutations": iterations, "resultats": res}

    permutations = {nom: permuter(nom, a.permutations)
                    for nom in ["panini_lang_tree", "panini_udhr", "glottolog"]}

    # leave-one-language-out (sur les paires couvertes)
    def loo(D, masque_base):
        coefs, r2s = [], []
        for drop in range(n):
            m = masque_base & np.array([i != drop and j != drop for i, j in paires])
            if m.sum() < 20:
                continue
            r = ols(np.column_stack([script[m], D[m]]), y[m])
            coefs.append(float(r["b"][2]))
            r2s.append(float(r["r2"]))
        return {"n_langues_retirees": len(coefs),
                "coef_min": float(min(coefs)), "coef_mediane": float(np.median(coefs)),
                "coef_max": float(max(coefs)),
                "r2_min": float(min(r2s)), "r2_mediane": float(np.median(r2s)),
                "r2_max": float(max(r2s)),
                "langue_la_plus_influente": ids[int(np.argmin(coefs))],
                "langue_la_moins_influente": ids[int(np.argmax(coefs))]}
    leave_one_out = {
        "panini_udhr_labelisees": loo(P2, labelise),
        "glottolog_labelisees": loo(G, labelise),
        "panini_udhr_toutes": loo(P2, np.ones(len(y), bool)),
        "glottolog_toutes": loo(G, np.ones(len(y), bool)),
    }

    # ---- 4. Atomes ---------------------------------------------------------
    oeuvres = list(sigs)
    Xa = np.array([[sigs[o][at] for at in V14] for o in oeuvres], float)
    Xa = np.where(Xa <= 0, 1e-6, Xa)
    clr = np.log(Xa) - np.log(Xa).mean(axis=1, keepdims=True)
    ev_corr, V_corr = pca_correlation(clr)
    ev_cov, _ = pca_covariance(clr)
    var_corr = ev_corr / ev_corr.sum()
    var_cov = ev_cov / ev_cov.sum()
    charges = []
    for k in range(4):
        ordre = np.argsort(-np.abs(V_corr[:, k]))
        charges.append({"pc": k + 1, "valeur_propre": float(ev_corr[k]),
                        "variance": float(var_corr[k]),
                        "charges": [{"atome": V14[j], "charge": float(V_corr[j, k])}
                                    for j in ordre[:6]]})
    # split-half
    c1, o3, n1 = [], [], []
    for _ in range(a.permutations):
        perm = rng.permutation(len(oeuvres))
        h = len(oeuvres) // 2
        A, B = clr[perm[:h]], clr[perm[h:]]
        va, vb = sous_espace(A, 1)[:, 0], sous_espace(B, 1)[:, 0]
        c1.append(abs(float(va @ vb)))
        Va, Vb = sous_espace(A, 3), sous_espace(B, 3)
        s = np.linalg.svd(Va.T @ Vb, compute_uv=False)
        o3.append(float(np.mean(s ** 2)))
        n1.append(int((pca_correlation(A)[0] > 1).sum()))
    # permutation des colonnes
    n1p, v3p = [], []
    for _ in range(a.permutations):
        Xp = clr.copy()
        for j in range(len(V14)):
            rng.shuffle(Xp[:, j])
        evp, _ = pca_correlation(Xp)
        n1p.append(int((evp > 1).sum()))
        v3p.append(float((np.cumsum(evp) / evp.sum())[2]))
    var3 = float((np.cumsum(ev_corr) / ev_corr.sum())[2])
    atomes = {
        "n_oeuvres": len(oeuvres), "n_atomes": len(V14),
        "pca_correlation_clr": {
            "valeurs_propres": [float(x) for x in ev_corr],
            "variance": [float(x) for x in var_corr],
            "variance_cumulee": [float(x) for x in np.cumsum(ev_corr) / ev_corr.sum()],
            "n_valeurs_propres_sup_1": int((ev_corr > 1).sum()),
            "n_pour_80_pct": n_pour_variance(ev_corr, 0.80),
            "n_pour_90_pct": n_pour_variance(ev_corr, 0.90),
            "n_pour_95_pct": n_pour_variance(ev_corr, 0.95),
        },
        "pca_covariance_clr": {
            "valeurs_propres": [float(x) for x in ev_cov],
            "variance": [float(x) for x in var_cov],
            "n_valeurs_propres_sup_1": int((ev_cov > 1).sum()),
            "variance_premiere": float(var_cov[0]),
        },
        "charges": charges,
        "split_half": {
            "n": a.permutations,
            "cos_pc1_moyen": float(np.mean(c1)),
            "cos_pc1_2_5": float(np.percentile(c1, 2.5)),
            "cos_pc1_97_5": float(np.percentile(c1, 97.5)),
            "recouvrement_sous_espace3_moyen": float(np.mean(o3)),
            "recouvrement_sous_espace3_2_5": float(np.percentile(o3, 2.5)),
            "recouvrement_sous_espace3_97_5": float(np.percentile(o3, 97.5)),
            "n_sup_1_median": int(np.median(n1)),
        },
        "permutation_colonnes": {
            "n": a.permutations,
            "n_sup_1_moyen": float(np.mean(n1p)),
            "n_sup_1_observe": int((ev_corr > 1).sum()),
            "p_n_sup_1": float((np.sum(np.array(n1p) <= (ev_corr > 1).sum()) + 1) / (len(n1p) + 1)),
            "var3_moyenne": float(np.mean(v3p)),
            "var3_observee": var3,
            "p_var3": float((np.sum(np.array(v3p) >= var3) + 1) / (len(v3p) + 1)),
        },
        "dhatus": {
            "sanskrit": DHATUS_SANSKRIT,
            "computationnels": DHATUS_COMPUTATIONNELS,
            "statut_panini": "macros (patterns nommés) dans l'espace V14, pas un second jeu d'atomes",
            "matrice_v14_publiee": False,
            "consequence": "les 9 dhātus ne sont pas identifiables à partir des seules signatures de 14 atomes ; "
                           "il faudrait publier leur décomposition V14. Le nombre 9 est architectural, pas mesuré.",
        },
    }

    # ---- 5. Avertissement §150 --------------------------------------------
    h3 = validation["H3_ols_regression"]["ols_dsig"]
    beta = h3["beta"]
    n_655 = len(paires334["pairs"])
    n_inter_langues = sum(1 for p in paires334["pairs"]
                          if p.get("lang_a") and p.get("lang_b") and p["lang_a"] != p["lang_b"])
    n_meme_langue = sum(1 for p in paires334["pairs"]
                        if p.get("lang_a") and p.get("lang_b") and p["lang_a"] == p["lang_b"])
    n_langue_vide = sum(1 for p in paires334["pairs"]
                        if not p.get("lang_a") or not p.get("lang_b"))
    avertissement = {
        "source": "nipada_v150_validation.json",
        "n_paires": n_655,
        "betas": {"constante": beta[0], "d_graph": beta[1], "dyear_par_1000_ans": beta[2],
                  "meme_tradition": beta[3]},
        "r2": h3["r2"],
        "ratio_filiation_epoque": beta[1] / beta[2] if beta[2] else None,
        "n_paires_deux_langues_connues_differentes": n_inter_langues,
        "n_paires_meme_langue": n_meme_langue,
        "n_paires_avec_une_langue_vide": n_langue_vide,
        "lecture": "Le coefficient « filiation » est un d_graph de tradition, pas une distance de famille "
                   "de langues : 3 paires seulement ont deux langues connues différentes.",
        "verdict_panini": validation["verdict"],
    }

    # ---- 6. Corpus commun ------------------------------------------------
    familles = sorted({t["famille"] for t in textes})
    scripts = sorted({t["script"] for t in textes})
    corpus_json = {
        "n_textes": n, "n_familles": len(familles), "n_ecritures": len(scripts),
        "familles": familles, "ecritures": scripts,
        "n_paires_non_ordonnees": len(paires), "n_paires_ordonnees": len(retrieval["udhr"]["paires"]),
        "textes": [{k: t[k] for k in ("id", "iso3", "langue", "script", "famille", "branche_feuille",
                                      "famille_panini", "branche_panini", "tradition_panini")}
                   for t in textes],
    }

    # ---- 7. Paires brutes -------------------------------------------------
    paires_json = []
    for i, j in paires:
        paires_json.append({
            "a": ids[i], "b": ids[j],
            "script_meme": bool(script[paires.index((i, j))]),
            "famille_glottolog_meme": bool(textes[i]["famille"] == textes[j]["famille"]),
            "panini_lang_tree": float(P1[paires.index((i, j))]),
            "panini_udhr": float(P2[paires.index((i, j))]),
            "glottolog": float(G[paires.index((i, j))]),
            "mrr": float(y[paires.index((i, j))]),
            "top1": float(y_top[paires.index((i, j))]),
        })

    # ---- 8. Convergence / divergence / à mesurer --------------------------
    convergence = [
        {"constat": "La surface passe avant la filiation, des deux côtés.",
         "preuve": "Panini §150 : β époque 0,1378 > β filiation 0,0489 (R² 0,30). Drave : le script est une "
                   "porte (154/154 paires hors script au hasard exact), la famille ne vit que dans 56 paires "
                   "de même script.",
         "ou": "reports/rapport-genealogie-deux-faces.md § 3.1"},
        {"constat": "Le rapport filiation/surface est du même ordre : environ un tiers.",
         "preuve": "Panini : 0,0489/0,1378 = 0,355. J3.1 Bible : famille 0,181 / script 0,609 = 0,297.",
         "ou": "reports/rapport-retrieval-epoque.md § 4.3 et § 5"},
        {"constat": "Les deux généalogies sont le même arbre sur les langues couvertes.",
         "preuve": "15/15 familles après appariement Niger-Congo→Atlantic-Congo ; 14/15 branches au nœud "
                   "exact (15/15 si l'on accepte le descendant le plus proche pour Tibeto-Burman) ; "
                   "Spearman 0,657 et Pearson 0,918 entre les distances P2 et Glottolog sur les 105 paires.",
         "ou": "reports/rapport-genealogie-deux-faces.md § 2.2"},
        {"constat": "Les deux généalogies prédisent le retrieval de façon comparable.",
         "preuve": "Sur les 105 paires couvertes : R² 0,256 (Panini UDHR) contre 0,230 (Glottolog) ; l'écart "
                   "est petit mais stable (positif dans les 21 retraits, 0,007–0,055).",
         "ou": "reports/rapport-genealogie-deux-faces.md § 3.3"},
        {"constat": "Un signal de filiation résiduel est détectable quand la surface est contrôlée.",
         "preuve": "Panini : β filiation 0,0489 (H3 OK). Drave : coefficient de distance −0,212 sur les 105 "
                   f"paires couvertes, p={permutations['panini_udhr']['resultats']['labelisees']['p']:.3f} "
                   "par permutation des labels.",
         "ou": "reports/rapport-genealogie-deux-faces.md § 3.2"},
    ]
    divergence = [
        {"constat": "Les deux « filiations » ne sont pas le même objet.",
         "preuve": "Panini §150 : 3/655 paires ont deux langues connues différentes, 173 sont eng-eng, "
                   "479 ont au moins une langue vide ; leur d_graph est une distance de tradition. "
                   "Drave : 5 familles, 210 paires, une distance de famille de langues.",
         "ou": "reports/rapport-genealogie-deux-faces.md § 2.1"},
        {"constat": "La couverture de la théorie est très inférieure à celle de la mesure.",
         "preuve": "LANG_TREE de Panini : 5/21 langues (200/210 paires à 1,0, « inconnu »). Métadonnées UDHR "
                   "de Panini : 15/21 (105/210 inconnues). Glottolog : 21/21. Les 6 langues sans label Panini "
                   "sont toutes non indo-européennes.",
         "ou": "reports/rapport-genealogie-deux-faces.md § 2.1"},
        {"constat": "L'échelle à quatre niveaux n'est pas une distance.",
         "preuve": "Sur les 21 langues, LANG_TREE n'utilise jamais le niveau 0,15 ; son niveau 0,40 mélange "
                   "eng-fra (MRR 0,952) et cinq paires au plancher (0,133). Le niveau 0,40 des métadonnées UDHR "
                   "contient une seule paire au-dessus du hasard sur 14. Les 4 paires de même branche sont "
                   "précisément celles que LANG_TREE code 1,0.",
         "ou": "reports/rapport-genealogie-deux-faces.md § 2.3"},
        {"constat": "Le confondant dominant n'est pas le même : époque chez Panini, écriture chez Drave.",
         "preuve": "Le corpus commun est mono-époque (1948) : il ne peut pas tester l'époque. J3.1, à écriture "
                   "contrôlée, trouve −0,034/siècle (p=0,19). Le script, lui, est une porte exacte : 154/154 "
                   "paires hors script sont au hasard.",
         "ou": "reports/rapport-retrieval-epoque.md § 4.3 ; rapport-genealogie-deux-faces.md § 3.1"},
        {"constat": "Le signal de famille tient à peu de paires.",
         "preuve": "Les 8 paires même famille + même script ont 7/8 au-dessus du hasard, mais deux paires "
                   "(eng-fra 0,952, ind-jav 0,918) portent la moyenne ; les six autres vont de 0,131 à 0,346. "
                   "Le leave-one-language-out du coefficient va de −0,296 à −0,103.",
         "ou": "reports/rapport-genealogie-deux-faces.md § 3.2"},
        {"constat": "La face « atomes » n'est pas une généalogie de langues.",
         "preuve": "V14 couvre 3/21 langues (décomposition) et 1/21 (convergence). Les 14 atomes ont 4 "
                   "dimensions effectives (ACP sur la corrélation des parts CLR) ou 1 (ACP sur la covariance) ; "
                   "les 9 dhātus sont des macros, avec deux nomenclatures non réconciliées et aucune matrice "
                   "V14 publiée.",
         "ou": "reports/rapport-genealogie-deux-faces.md § 4"},
        {"constat": "Le code « inconnu = 1,0 » est une valeur manquante, pas une distance.",
         "preuve": "Il n'est pas missing at random : les 6 langues non labellisées sont toutes non-IE, et les "
                   "paires inconnues ont un MRR plus bas (0,140 contre 0,162). Séparer l'indicateur d'inconnu "
                   "laisse le coefficient de distance à −0,22 et ajoute un effet d'inconnu de −0,172 ; le R² "
                   "« toutes » de 0,198 est donc un artefact de couverture, pas une supériorité généalogique.",
         "ou": "reports/rapport-genealogie-deux-faces.md § 3.4"},
    ]
    a_mesurer = [
        {"mesure": "Signature V14 des 21 langues du corpus commun",
         "pourquoi": "La face atomes n'existe que pour 3/21 langues ; sans elle, la confrontation atomes ↔ "
                     "généalogie sur le même corpus n'est pas possible.",
         "dispositif": "Projection multilingue (wordnets ou embeddings alignés) des 14 atomes sur les 21 textes, "
                       "puis test : les parts d'atomes sont-elles invariantes entre traductions (universalité) ou "
                       "clustérisent-elles par famille (filiation) ?",
         "controle": "Traduire un même texte dans deux langues de la même famille et dans deux familles "
                     "différentes ; l'invariance doit être plus forte dans le premier cas si les atomes sont "
                     "universaux."},
        {"mesure": "Matrice 9 dhātus → 14 atomes",
         "pourquoi": "Les 9 dhātus sont déclarés macros ; sans matrice publiée, ils ne sont pas mesurables. "
                     "Deux nomenclatures coexistent (BHŪ…DṚŚ et EXIST…KNOW).",
         "dispositif": "Publier la décomposition de chaque dhātu en V14, puis projeter les signatures de 44 "
                       "œuvres sur les 9 dhātus et comparer la variance expliquée à celle des 14 atomes.",
         "controle": "Permutation des colonnes de la matrice : si la projection n'explique pas plus que le "
                     "hasard, les dhātus ne sont pas identifiables."},
        {"mesure": "Distance Panini continue et étendue aux 21 langues",
         "pourquoi": "LANG_TREE couvre 5/21 et l'échelle à quatre niveaux sature ; 200/210 paires sont "
                     "« inconnues ».",
         "dispositif": "Étendre LANG_TREE aux 21 langues (ou apprendre une distance continue sur Glottolog) et "
                       "refaire la régression sur 210 paires.",
         "controle": "Comparer à la distance discrète actuelle : si le R² ne bouge pas, le gain de granularité "
                     "est nul."},
        {"mesure": "Corpus équilibré même script / familles différentes",
         "pourquoi": "Les 21 langues ne donnent que 56 paires de même script et 8 paires de même famille + "
                     "même script ; le signal tient à 2-3 paires.",
         "dispositif": "Choisir 6 familles × 6 langues de même écriture (latin, cyrillique, arabe…), avec "
                       "plusieurs branches par famille et plusieurs familles par écriture.",
         "controle": "Le coefficient de famille doit rester stable quand on retire une langue (leave-one-out) "
                     "et ne pas s'effondrer quand on retire les deux paires extrêmes."},
        {"mesure": "Retrieval neuronal (états cachés)",
         "pourquoi": "Le retrieval de J3.1/J3.2 est de surface ; la porte du script peut être une propriété "
                     "des n-grammes, pas du sens.",
         "dispositif": "Refaire le retrieval UDHR avec les états cachés d'un modèle multilingue, à contenu "
                       "identique et script contrôlé.",
         "controle": "Mêmes paires, même découpage ; si le modèle traverse le script, la conclusion « la "
                     "surface d'abord » est propre à l'instrument."},
        {"mesure": "Corpus multi-époques avec les mêmes langues",
         "pourquoi": "Le corpus commun est mono-époque (1948) ; l'avertissement de Panini sur l'époque ne peut "
                     "pas y être testé.",
         "dispositif": "Bible ou corpus daté dans un sous-ensemble des 21 langues, avec plusieurs traductions "
                       "par langue et des écarts de plus d'un siècle.",
         "controle": "Permutation des années ; le coefficient d'époque doit sortir de la distribution nulle "
                     "pour être retenu."},
        {"mesure": "Poids des arêtes Glottolog",
         "pourquoi": "La distance de chemin traite toutes les arêtes comme égales ; l'arbre est très "
                     "déséquilibré (IE > 10 niveaux, austronésien > 5).",
         "dispositif": "Calibrer les longueurs de branches (temps de séparation, distance lexicale) et refaire "
                       "la régression.",
         "controle": "Comparer aux arêtes uniformes : si le classement des paires ne change pas, le gain est "
                     "cosmétique."},
    ]

    # ---- 9. Assemblage ----------------------------------------------------
    sortie = {
        "titre": "J3.2 — La généalogie à deux faces : la théorie de Panini et l'alignement Glottolog sur le corpus commun",
        "version": "1.0",
        "date": "2026-11-07",
        "ligne_roadmap": "R0.7 (le bloc langue) / L",
        "chantier": "semaine Panini, J3.2",
        "statut": "mesuré, écrit, contrôlé",
        "question": "Ce que la théorie de Panini (14 atomes, 9 dhātus, une échelle de distance) et nos "
                    "mesures d'alignement (Glottolog + retrieval) disent de la même généalogie sur les 21 "
                    "langues du corpus commun : ce qui converge, ce qui diverge, ce qui reste à mesurer.",
        "sources": {
            "corpus_commun": "reports/corpus-commun.json (21 textes, 21/11/07)",
            "retrieval": "reports/retrieval-epoque.json (J3.1, 420 paires ordonnées)",
            "panini_udhr": "../Panini/research/data/udhr_corpus.json (532 langues)",
            "panini_lang_tree": "../Panini/research/src/nipada/signing/language_genealogy.py (29 langues)",
            "panini_signatures": "../Panini/research/nipada/falsification/analytic_sigs_v1.json (44 œuvres)",
            "panini_validation": "../Panini/research/nipada/falsification/nipada_v150_validation.json",
            "panini_paires334": "../Panini/research/nipada/falsification/pairs334_axes_v1.json (655 paires)",
            "panini_v14_udhr": "../Panini/research/data/udhr_decomposed_v14.json ; udhr_convergence_v14.json",
            "glottolog": "../data/udhr/genealogie.json (441 langues, chemins de glottocodes)",
        },
        "corpus_commun": corpus_json,
        "theorie_panini": {
            "atomes": [{"nom": a, "rang": i + 1} for i, a in enumerate(V14)],
            "dhatus": atomes["dhatus"],
            "distance": {
                "echelle": {"meme_langue": 0.0, "meme_branche": 0.15, "meme_famille": 0.40,
                            "familles_differentes": 0.75, "inconnu": 1.0},
                "lang_tree_n": len(tree),
                "lang_tree_communs": tree_communs,
                "lang_tree_couverture": len(tree_communs) / n,
            },
            "metadonnees_udhr": {
                "n_langues": len(udhr_panini["languages"]),
                "n_famille_connue": n_panini_connues,
                "n_famille_other": len(udhr_panini["languages"]) - n_panini_connues,
                "familles": fam_panini,
                "communs_couverts": panini_udhr_communs,
                "communs_non_couverts": non_labelises,
                "couverture": len(panini_udhr_communs) / n,
            },
            "v14_udhr": {
                "decompose": {"n": decompose["total_languages_processed"],
                              "langues": sorted(decompose["results"]),
                              "communs": decompose_communs,
                              "couverture_communs": len(decompose_communs) / n},
                "convergence": {"n": len(convergence_v14), "langues": sorted(convergence_v14),
                                "communs": convergence_communs,
                                "couverture_communs": len(convergence_communs) / n},
            },
            "avertissement_150": avertissement,
        },
        "accord_genealogies": {
            "n_langues_labelisees": len(labelise_textes),
            "famille_brute": {"accord": accord_famille_brut, "n": len(labelise_textes),
                              "taux": accord_famille_brut / len(labelise_textes),
                              "desaccords": desaccords_famille_brute},
            "famille_mappee": {"accord": accord_famille_mappe, "n": len(labelise_textes),
                               "taux": accord_famille_mappe / len(labelise_textes),
                               "desaccords": desaccords_famille_mappee},
            "branche_exacte": {"accord": accord_branche_exact, "n": len(labelise_textes),
                               "taux": accord_branche_exact / len(labelise_textes),
                               "desaccords": desaccords_branche_exacte + desaccords_branche},
            "branche_proche": {"accord": accord_branche_proche, "n": len(labelise_textes),
                               "taux": accord_branche_proche / len(labelise_textes)},
            "distances_p2_glottolog": {
                "n_paires": int(labelise.sum()),
                "spearman": {"rho": float(spearman_p2_g.statistic), "p": float(spearman_p2_g.pvalue)},
                "pearson": {"r": float(pearson_p2_g.statistic), "p": float(pearson_p2_g.pvalue)},
            },
            "p1_p2": {"n_paires": len(p1_p2_vals),
                      "valeurs_identiques": bool(all(abs(a - b) < 1e-9 for a, b in p1_p2_vals)),
                      "exemple": [{"p1": x, "p2": y} for x, y in p1_p2_vals[:5]]},
        },
        "alignement": {
            "mrr_moyen": float(y.mean()), "top1_moyen": float(y_top.mean()),
            "hasard_mrr": plancher_mrr, "hasard_top1": plancher_top1,
            "script": {
                "n_meme": int((script == 1).sum()), "n_different": int((script == 0).sum()),
                "mrr_meme": float(y[script == 1].mean()), "mrr_different": float(y[script == 0].mean()),
                "top1_meme": float(y_top[script == 1].mean()),
                "top1_different": float(y_top[script == 0].mean()),
                "hors_script_au_hasard": bool(np.allclose(y[script == 0], plancher_mrr, atol=1e-9)),
                "mrr_hors_script_unique": float(np.unique(np.round(y[script == 0], 8))[0]),
            },
            "groupes": groupes,
            "table_script_famille": table_script_famille,
            "paires_famille_script": paires_famille_script,
            "regressions": regressions,
            "decomposition_inconnu": decomposition_inconnu,
            "permutations": permutations,
            "leave_one_out": leave_one_out,
            "paires": paires_json,
        },
        "atomes": atomes,
        "convergence": convergence,
        "divergence": divergence,
        "a_mesurer": a_mesurer,
        "limites": [
            "Le retrieval est de surface (n-grammes de caractères, TF-IDF, cosinus) : il ne teste pas le sens. "
            "La porte du script peut être une propriété de l'instrument, pas de la langue.",
            "Le corpus commun est mono-époque (1948), mono-genre (déclaration), 21 langues, 5 familles, "
            "10 écritures. Il ne permet ni le contrôle de l'époque ni une estimation de famille stable.",
            "Les paires ne sont pas indépendantes (chaque langue apparaît dans 20 paires) : les p-values OLS "
            "sont descriptives ; les tests d'inférence sont les permutations de labels et le leave-one-out.",
            "La distance Glottolog est une distance de chemin à arêtes uniformes ; l'arbre est très "
            "déséquilibré, et le choix de normalisation (division par |a|+|b|-2) est une convention.",
            "Les métadonnées UDHR de Panini et LANG_TREE sont deux représentations différentes : la première "
            "couvre 111/532 langues, la seconde 29 langues. Leur accord n'est vérifié que sur 5 langues.",
            "L'ACP des 14 atomes porte sur 44 œuvres philosophiques et religieuses, pas sur les 21 langues : "
            "c'est une propriété de la signature de Panini, pas du corpus commun.",
            "Le coefficient de famille est un effet moyen sur des paires hétérogènes ; il ne dit pas quelles "
            "langues sont proches, et il est porté par 2-3 paires.",
            "La huitième et la neuvième langues de la même branche (ind/tgl/jav, amh/heb) sont codées 1,0 "
            "par LANG_TREE : la fonction de distance de Panini ne voit pas ses propres paires les plus proches.",
        ],
        "controles_negatifs": {
            "retrieval_hors_script": {
                "attendu": "Au hasard exact (MRR 1/30, top1 1/30)",
                "obtenu": {"n": int((script == 0).sum()), "mrr": float(y[script == 0].mean()),
                           "top1": float(y_top[script == 0].mean())},
                "verdict": "PASS" if np.allclose(y[script == 0], plancher_mrr, atol=1e-9) else "FAIL",
            },
            "permutation_labels_panini": {
                "attendu": "Coefficient ~0",
                "obtenu": permutations["panini_udhr"]["resultats"]["labelisees"],
                "verdict": "PASS" if permutations["panini_udhr"]["resultats"]["labelisees"]["p"] < 0.05 else "FAIL",
            },
            "permutation_chemins_glottolog": {
                "attendu": "Coefficient ~0",
                "obtenu": permutations["glottolog"]["resultats"]["labelisees"],
                "verdict": "PASS" if permutations["glottolog"]["resultats"]["labelisees"]["p"] < 0.05 else "FAIL",
            },
            "permutation_colonnes_atomes": {
                "attendu": "Plus de valeurs propres > 1 que l'observé (les colonnes indépendantes sont moins "
                           "colinéaires)",
                "obtenu": atomes["permutation_colonnes"],
                "verdict": "PASS" if atomes["permutation_colonnes"]["p_n_sup_1"] < 0.05 else "FAIL",
            },
            "split_half_atomes": {
                "attendu": "PC1 stable ; sous-espace 3 partiellement stable",
                "obtenu": atomes["split_half"],
                "verdict": "PASS" if atomes["split_half"]["cos_pc1_moyen"] > 0.8 else "FAIL",
            },
        },
        "fichiers": {
            "fiche": "reports/rapport-genealogie-deux-faces.md",
            "json": "reports/genealogie-deux-faces.json",
            "outil": "tools/genealogie_deux_faces.py",
        },
    }
    Path(a.sortie).write_text(json.dumps(sortie, ensure_ascii=False, indent=1), encoding="utf-8")

    # ---- 10. Résumé -------------------------------------------------------
    print("J3.2 — la généalogie à deux faces")
    print(f"  corpus commun : {n} langues, {len(familles)} familles, {len(scripts)} écritures, "
          f"{len(paires)} paires non ordonnées")
    print(f"  couverture : LANG_TREE {len(tree_communs)}/{n} ; métadonnées UDHR {len(panini_udhr_communs)}/{n} ; "
          f"Glottolog {len(glotto_communs)}/{n}")
    print(f"  V14 : décomposition {len(decompose_communs)}/{n} ; convergence {len(convergence_communs)}/{n}")
    print(f"  accord familles (mappé) : {accord_famille_mappe}/{len(labelise_textes)} ; "
          f"branches exactes : {accord_branche_exact}/{len(labelise_textes)}")
    print(f"  retrieval : MRR {y.mean():.4f} ; hors script {y[script == 0].mean():.4f} "
          f"(hasard {plancher_mrr:.4f}), même script {y[script == 1].mean():.4f}")
    print(f"  régression labelisées : R² Panini {regressions['labelisees'][2]['r2']:.4f} ; "
          f"Glottolog {regressions['labelisees'][3]['r2']:.4f}")
    print(f"  atomes : {atomes['pca_correlation_clr']['n_valeurs_propres_sup_1']} valeurs propres > 1 "
          f"(corrélation), {atomes['pca_covariance_clr']['n_valeurs_propres_sup_1']} (covariance) ; "
          f"90 % à {atomes['pca_correlation_clr']['n_pour_90_pct']} composantes")
    print(f"  §150 : {n_inter_langues}/{n_655} paires inter-langues ; "
          f"β filiation/époque = {avertissement['ratio_filiation_epoque']:.3f}")
    print(f"  → {a.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
