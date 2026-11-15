#!/usr/bin/env python3
"""panini_manifeste.py — W4 : le manifeste des 26 signatures V14 et le rejeu disponible.

Ce script construit `reports/panini-manifeste.json`. Il ne modifie jamais Panini :
il lit le manifeste gelé B1, les 44 signatures `analytic_sigs_v1`, les sources du
§334 et le graphe v35. Le rejeu est **descriptif** : 27 des 60 paires ont leurs
deux signatures ; les 33 autres sont listées. Aucune p-value de H0 n'est écrite.

Usage :
  python3 tools/panini_manifeste.py --construire
  python3 tools/panini_manifeste.py --verifier
  python3 tools/panini_manifeste.py --resume
"""
from __future__ import annotations

import argparse
import collections
import datetime as _dt
import hashlib
import json
import math
import pathlib
import subprocess
import sys

import numpy as np

RACINE = pathlib.Path(__file__).resolve().parent.parent
PANINI = RACINE.parent / "Panini"
PANINI_RESEARCH = PANINI / "research"
FALS = PANINI_RESEARCH / "nipada" / "falsification"
SOURCES = PANINI_RESEARCH / "nipada" / "corpus" / "_cache" / "sources"
MANIFESTE_B1 = RACINE / "reports" / "protocole-date.json"
SIGNATURES_44 = FALS / "analytic_sigs_v1.json"
PAIRES_334 = FALS / "pairs334_axes_v1.json"
SORTIE = RACINE / "reports" / "panini-manifeste.json"
CALIBRATION = pathlib.Path("/tmp/calibration_44.json")

V14 = [
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS", "MODALITÉ",
    "NOMBRE", "ESPACE", "OPÉRATION", "FONCTION", "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
]
SEUIL_MOTS = 300
SEUIL_COS = 0.99
SEUIL_L2 = 0.01
GRAINE = 20261115
N_PERM = 2000


def lire(p: pathlib.Path):
    return json.loads(p.read_text(encoding="utf-8"))


def sha256(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def arr(x, n=6):
    if x is None:
        return None
    x = float(x)
    if math.isnan(x) or math.isinf(x):
        return None
    return round(x, n)


def commit_git(p: pathlib.Path):
    try:
        return subprocess.check_output(["git", "-C", str(p), "rev-parse", "HEAD"],
                                       stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        return None


def statut_panini() -> str:
    try:
        out = subprocess.check_output(
            ["git", "-C", str(PANINI), "status", "--porcelain", "--",
             "research/nipada/falsification", "research/nipada/corpus/_cache/sources"],
            stderr=subprocess.DEVNULL, text=True,
        )
    except Exception:
        out = ""
    return hashlib.sha256(out.encode("utf-8")).hexdigest()


def vecteur(sig):
    return np.array([float(sig[a]) for a in V14], float)


def ols(y, x):
    y = np.asarray(y, float)
    x = np.asarray(x, float)
    X = np.column_stack([np.ones(len(x)), x])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    pred = X @ b
    ssr = float(np.sum((y - pred) ** 2))
    sst = float(np.sum((y - y.mean()) ** 2))
    return float(b[1]), (1.0 - ssr / sst if sst else 0.0)


def stats(valeurs):
    v = [float(x) for x in valeurs]
    if not v:
        return {"n": 0}
    return {"n": len(v), "min": arr(min(v)), "median": arr(float(np.median(v))),
            "max": arr(max(v)), "moyenne": arr(float(np.mean(v)))}


def p_percentile(null, obs):
    null = np.asarray(null, float)
    lo = (float(np.sum(null <= obs)) + 1.0) / (len(null) + 1.0)
    hi = (float(np.sum(null >= obs)) + 1.0) / (len(null) + 1.0)
    return min(1.0, 2.0 * min(lo, hi)), lo, hi


def perm_dates(rows, groupe, cle, n=N_PERM):
    xs = [r for r in rows if r["groupe"] == groupe]
    if len(xs) < 3:
        return {"n": len(xs), "statut": "non executable (n < 3)"}
    y = np.array([r["d_sig"] for r in xs], float)
    x = np.array([r["delta_annee"] / 1000.0 for r in xs], float)
    b_obs, r2 = ols(y, x)
    groupes = collections.defaultdict(list)
    for i, r in enumerate(xs):
        groupes[r[cle]].append(i)
    rng = np.random.default_rng(GRAINE)
    null = []
    for _ in range(n):
        xp = x.copy()
        for idx in groupes.values():
            vals = xp[idx].copy()
            rng.shuffle(vals)
            xp[idx] = vals
        bn, _ = ols(y, xp)
        null.append(bn)
    null = np.asarray(null, float)
    p, lo, hi = p_percentile(null, b_obs)
    return {
        "n": len(xs), "beta_obs": arr(b_obs), "r2_obs": arr(r2),
        "n_permutations": n, "null_moyenne": arr(float(np.mean(null))),
        "null_sd": arr(float(np.std(null))),
        "null_q025": arr(float(np.quantile(null, 0.025))),
        "null_q975": arr(float(np.quantile(null, 0.975))),
        "p_perm": arr(p), "percentile_bas": arr(lo), "percentile_haut": arr(hi),
        "groupes": {k: len(v) for k, v in groupes.items()},
        "role": "controle_negatif_de_pipeline (pas le test H0, pas de p-value de H0)",
    }


def perm_signatures(rows, groupe, n=N_PERM):
    xs = [r for r in rows if groupe == "ALL" or r["groupe"] == groupe]
    if len(xs) < 3:
        return {"n": len(xs), "statut": "non executable (n < 3)"}
    textes = sorted({r["a"] for r in rows} | {r["b"] for r in rows})
    V = {r["a"]: vecteur(r["va"]) for r in rows}
    V.update({r["b"]: vecteur(r["vb"]) for r in rows})
    obs = float(np.mean([r["d_sig"] for r in xs]))
    y = np.array([r["d_sig"] for r in xs], float)
    x = np.array([r["delta_annee"] / 1000.0 for r in xs], float)
    b_obs, _ = ols(y, x)
    rng = np.random.default_rng(GRAINE)
    null_moy, null_pente = [], []
    for _ in range(n):
        perm = rng.permutation(len(textes))
        remap = {textes[i]: V[textes[perm[i]]] for i in range(len(textes))}
        vals = np.array([float(np.linalg.norm(remap[r["a"]] - remap[r["b"]])) for r in xs], float)
        null_moy.append(float(np.mean(vals)))
        bn, _ = ols(vals, x)
        null_pente.append(bn)
    null_moy = np.asarray(null_moy, float)
    null_pente = np.asarray(null_pente, float)
    p_moy, _, _ = p_percentile(null_moy, obs)
    p_pente, _, _ = p_percentile(null_pente, b_obs)
    return {
        "n": len(xs), "n_permutations": n,
        "d_sig_moyenne_obs": arr(obs), "d_sig_moyenne_null": arr(float(np.mean(null_moy))),
        "d_sig_null_sd": arr(float(np.std(null_moy))), "p_perm_moyenne": arr(p_moy),
        "beta_date_obs": arr(b_obs), "beta_date_null_moyenne": arr(float(np.mean(null_pente))),
        "p_perm_pente_date": arr(p_pente),
        "role": "controle_negatif_de_pipeline (signatures permutées entre textes)",
    }


def construire(argv=None) -> dict:
    manifeste_b1 = lire(MANIFESTE_B1)
    sigs = lire(SIGNATURES_44)
    graphe = lire(FALS / "nipada_v334_graph_v35.json")
    nodes = graphe["nodes"]
    paires655 = lire(PAIRES_334)["pairs"]
    textes655 = {x for p in paires655 for x in (p["a"], p["b"])}
    signes = set(sigs)
    a_signer_ids = {x["id"] for x in manifeste_b1["a_signer"]}
    statut_avant = statut_panini()

    textes = {t["id"]: t for t in manifeste_b1["textes"]}
    paires = manifeste_b1["paires"]

    # --- sources et doublons -------------------------------------------------
    info_sources = {}
    for ident in sorted(textes):
        p = SOURCES / f"{ident}.txt"
        if p.exists():
            mots = len(p.read_text(encoding="utf-8", errors="replace").split())
            info_sources[ident] = {
                "fichier": str(p.relative_to(PANINI_RESEARCH)),
                "sha256": sha256(p), "octets": p.stat().st_size, "mots": mots,
                "seuil_300": mots >= SEUIL_MOTS,
            }
        else:
            info_sources[ident] = {"fichier": None, "sha256": None, "mots": 0,
                                   "seuil_300": False, "absent": True}
    par_hash = collections.defaultdict(list)
    for ident, info in info_sources.items():
        if info.get("sha256"):
            par_hash[info["sha256"]].append(ident)
    doublons = []
    for h, ids in par_hash.items():
        if len(ids) > 1:
            doublons.append({
                "sha256": h,
                "ids": sorted(ids),
                "signes": sorted(i for i in ids if i in signes),
                "a_signer": sorted(i for i in ids if i in a_signer_ids),
                "mots": info_sources[ids[0]]["mots"],
            })
    doublons.sort(key=lambda d: d["ids"])
    twin = {}
    for d in doublons:
        for i in d["ids"]:
            twin.setdefault(i, []).extend(x for x in d["ids"] if x != i)
    for i in twin:
        twin[i] = sorted(set(twin[i]))

    paires_par_texte = collections.defaultdict(list)
    for p in paires:
        paires_par_texte[p["a"]].append(p["id"])
        paires_par_texte[p["b"]].append(p["id"])

    a_signer = []
    for x in manifeste_b1["a_signer"]:
        ident = x["id"]
        info = info_sources.get(ident, {})
        sig_graph = nodes.get(ident, {}).get("v14_signature") is not None
        deja = [i for i in twin.get(ident, []) if i in signes]
        a_signer.append({
            "id": ident,
            "annee": x["annee"],
            "langue": x["langue"],
            "famille": x["famille"],
            "source_url": x.get("source") or None,
            "fichier_source": info.get("fichier"),
            "source_sha256": info.get("sha256"),
            "mots": info.get("mots"),
            "seuil_300": info.get("seuil_300", False),
            "usage": x["usage"],
            "paires": sorted(paires_par_texte[ident]),
            "dans_655": ident in textes655,
            "signature_graphe_v35": sig_graph,
            "doublon_de": twin.get(ident, []),
            "signature_deja_disponible_via": deja,
        })
    a_signer.sort(key=lambda t: t["id"])
    courts = [t for t in a_signer if not t["seuil_300"]]

    # les 3 textes du §334 sans signature hors protocole
    hors = []
    for ident in sorted(textes655 - signes - a_signer_ids):
        p = SOURCES / f"{ident}.txt"
        hors.append({
            "id": ident,
            "source_presente": p.exists(),
            "raison": "hors des 60 paires ; source non acquise" if not p.exists() else "hors des 60 paires",
        })

    # --- rejeu disponible ----------------------------------------------------
    calculees, manquantes = [], []
    for p in paires:
        if p["a"] in signes and p["b"] in signes:
            d = float(np.linalg.norm(vecteur(sigs[p["a"]]) - vecteur(sigs[p["b"]])))
            calculees.append({
                "id": p["id"], "groupe": p["groupe"], "a": p["a"], "b": p["b"],
                "delta_annee": p["delta_annee"], "d_sig": arr(d),
                "meme_famille": p["meme_famille"], "meme_langue": p["meme_langue"],
                "famille": p["famille_a"], "langue": p["langue_a"],
                "d_topo": p["d_topo"],
                "textes_doublons": sorted(set(twin.get(p["a"], [])) | set(twin.get(p["b"], []))),
            })
        else:
            absents = [t for t in (p["a"], p["b"]) if t not in signes]
            manquantes.append({"id": p["id"], "groupe": p["groupe"], "a": p["a"], "b": p["b"],
                               "textes_sans_signature": absents})
    rows = [{"id": r["id"], "groupe": r["groupe"], "a": r["a"], "b": r["b"],
             "delta_annee": r["delta_annee"], "d_sig": r["d_sig"],
             "famille": r["famille"], "langue": r["langue"],
             "va": sigs[r["a"]], "vb": sigs[r["b"]]} for r in calculees]

    par_groupe = {}
    for g in ("G1", "G2", "G3"):
        n_total = sum(1 for p in paires if p["groupe"] == g)
        n_calc = sum(1 for p in calculees if p["groupe"] == g)
        par_groupe[g] = {"n_total": n_total, "n_calculees": n_calc,
                         "n_manquantes": n_total - n_calc}
    descriptif = {}
    for g in ("G1", "G2", "G3"):
        xs = [r for r in rows if r["groupe"] == g]
        descriptif[g] = {
            "n": len(xs),
            "d_sig": stats([r["d_sig"] for r in xs]),
            "delta_annee": stats([r["delta_annee"] for r in xs]),
        }
    for g in ("G2", "G3", "ALL"):
        xs = [r for r in rows if g == "ALL" or r["groupe"] == g]
        if len(xs) >= 3:
            b, r2 = ols([r["d_sig"] for r in xs], [r["delta_annee"] / 1000.0 for r in xs])
            descriptif.setdefault(g, {})["pente_date"] = {"beta_brut": arr(b), "r2": arr(r2),
                                                          "n": len(xs)}

    # --- contrôles -----------------------------------------------------------
    n2 = perm_dates(rows, "G2", "famille")
    n3 = perm_dates(rows, "G3", "langue")
    n4_g2 = perm_signatures(rows, "G2")
    n4_g3 = perm_signatures(rows, "G3")
    n4_all = perm_signatures(rows, "ALL")
    # sensibilité : paires dont un texte a un jumeau de source
    avec_doublon = [r for r in rows if twin.get(r["a"]) or twin.get(r["b"])]
    sans_doublon = [r for r in rows if not (twin.get(r["a"]) or twin.get(r["b"]))]
    sens = {"n_exclues": len(avec_doublon), "paires_exclues": [r["id"] for r in avec_doublon]}
    for g in ("G2", "G3"):
        xs = [r for r in sans_doublon if r["groupe"] == g]
        if len(xs) >= 3:
            b, r2 = ols([r["d_sig"] for r in xs], [r["delta_annee"] / 1000.0 for r in xs])
            sens[g] = {"n": len(xs), "d_sig_moyenne": arr(float(np.mean([r["d_sig"] for r in xs]))),
                       "beta_date": arr(b), "r2": arr(r2)}
    # G1 positif : 1 paire -> non exécutable
    g1 = [r for r in rows if r["groupe"] == "G1"]
    positif = {
        "n": len(g1),
        "statut": "non executable" if len(g1) < 3 else "executable",
        "raison": "une seule paire G1 a ses deux signatures (G1-20)" if len(g1) == 1 else None,
        "d_sig_moyenne": arr(float(np.mean([r["d_sig"] for r in g1]))) if g1 else None,
    }

    # calibration : lue depuis /tmp (résultat de `panini_signatures_26.py`), sinon
    # reprise du JSON déjà écrit : un rebuild ne perd pas la mesure.
    calibration = None
    source_cal = None
    if CALIBRATION.exists():
        source_cal = CALIBRATION
    elif SORTIE.exists():
        source_cal = SORTIE
    if source_cal is not None:
        try:
            c = lire(source_cal)
            if source_cal == SORTIE:
                c = c.get("calibration", {}).get("mesure") or {}
            fails = sorted(k for k, v in c.items() if not v.get("ok"))
            if c:
                calibration = {
                    "n": len(c), "ok": len(c) - len(fails), "echecs": fails,
                    "seuil": {"cos": SEUIL_COS, "l2": SEUIL_L2, "regle": "cos >= 0,99 ou L2 <= 0,01"},
                    "min_cos": arr(min(v["cos"] for v in c.values())),
                    "max_l2": arr(max(v["l2"] for v in c.values())),
                    "par_oeuvre": {k: {"cos": arr(v["cos"]), "l2": arr(v["l2"]),
                                       "mots": v.get("mots", v.get("words")),
                                       "ok": bool(v["ok"])} for k, v in sorted(c.items())},
                }
        except Exception:
            calibration = None

    statut_apres = statut_panini()

    # --- références et format ------------------------------------------------
    reference = {k: {a: float(sigs[k][a]) for a in V14} for k in sorted(sigs)}

    doc = {
        "tache": "W4",
        "version": "1.0",
        "titre": "Manifeste Panini — les 26 signatures V14 et le rejeu disponible des 60 paires",
        "date": _dt.date.today().isoformat(),
        "commit_drave": commit_git(RACINE),
        "commit_panini": commit_git(PANINI),
        "sources": {
            "manifeste_b1": {"chemin": "reports/protocole-date.json", "sha256": sha256(MANIFESTE_B1)},
            **{k: dict(v, chemin=("Panini/" + v["chemin"]) if not str(v["chemin"]).startswith("Panini/") else v["chemin"])
               for k, v in manifeste_b1["sources"].items()},
        },
        "panini_lecture_seule": {
            "statut_sha256_avant": statut_avant,
            "statut_sha256_apres": statut_apres,
            "identique": statut_avant == statut_apres,
            "note": "git status --porcelain limité à falsification/ et sources/ ; aucune écriture W4 dans Panini.",
        },
        "manifeste": {
            "n_textes": len(textes),
            "n_deja_signes": len([t for t in textes if t in signes]),
            "n_a_signer": len(a_signer),
            "n_paires": len(paires),
            "a_signer": a_signer,
            "sources_courtes": [t["id"] for t in courts],
            "doublons_sources": doublons,
            "hors_protocole_sans_signature": hors,
            "reduction_effective": {
                "textes_distincts_a_signer": len(a_signer),
                "vecteurs_distincts": len({info_sources[t["id"]]["sha256"] for t in a_signer if info_sources[t["id"]].get("sha256")}),
                "vecteurs_deja_disponibles": sorted({i for t in a_signer for i in t["signature_deja_disponible_via"]}),
                "vecteurs_nouveaux_distincts": len({info_sources[t["id"]]["sha256"] for t in a_signer
                                                   if info_sources[t["id"]].get("sha256")
                                                   and not t["signature_deja_disponible_via"]}),
            },
            "format": {
                "fichier": "JSON UTF-8",
                "enveloppe": {"instrument": "chaîne", "commit": "sha1 Panini", "signatures": "objet {id: {14 atomes}}"},
                "cles_exactes": V14,
                "contrainte": "14 clés exactes, valeurs flottantes >= 0, somme = 1 ± 1e-6",
                "exemple_oeuvre_deja_signee": {"2_esdras": reference.get("2_esdras")},
                "note": "Ne pas mélanger avec les v14_signature du graphe v35 (instrument différent).",
            },
            "commandes": {
                "panini_production": (
                    "cd /chemin/vers/Panini/research && .venv/bin/python "
                    "/chemin/vers/Qtrinet/tools/panini_signatures_26.py "
                    "--manifeste /chemin/vers/Qtrinet/reports/panini-manifeste.json "
                    "--sortie /tmp/panini-v14-26.json"
                ),
                "pilote_rejeu": (
                    "python3 tools/protocole_date.py --rejouer "
                    "--signatures /tmp/panini-v14-26.json "
                    "--sortie reports/protocole-date-resultats.json"
                ),
                "verification_manifeste": "python3 tools/panini_manifeste.py --verifier",
            },
        },
        "calibration": {
            "reference": reference,
            "mesure": calibration,
        },
        "rejeu": {
            "statut": "incomplet",
            "n_paires": len(paires),
            "n_calculees": len(calculees),
            "n_manquantes": len(manquantes),
            "par_groupe": par_groupe,
            "descriptif": descriptif,
            "paires_calculees": calculees,
            "paires_manquantes": manquantes,
            "controles": {
                "negatif_2_annees_permutees_G2": n2,
                "negatif_3_annees_permutees_G3": n3,
                "negatif_4_signatures_permutees_G2": n4_g2,
                "negatif_4_signatures_permutees_G3": n4_g3,
                "negatif_4_signatures_permutees_tout": n4_all,
                "negatif_5_colonnes_atomes": {
                    "statut": "non execute — controle vide",
                    "raison": "une permutation commune des 14 colonnes laisse ||s_a - s_b||_2 invariante ; "
                              "le contrôle tel qu'écrit ne peut pas détruire la distance. Il faut permuter "
                              "les étiquettes indépendamment par signature, ou remplacer par la permutation "
                              "des signatures (N4).",
                },
                "negatif_6_doublons_sources": sens,
                "positif_G1": positif,
                "calibration_44": calibration,
            },
            "p_value_H0": None,
            "verdict": "incomplet : 27/60 paires calculées, 33 manquantes ; aucune p-value de H0 ; "
                       "la calibration 42/44 échoue sur bengio_2003 et mengzi ; 3 sources < 300 mots.",
        },
        "limites": [
            "Le rejeu ne porte que sur 27 des 60 paires : les 33 autres exigent les signatures des 26 textes. "
            "Ce n'est pas un échantillon choisi par disponibilité pour un test ; c'est un noyau décrit, sans p-value.",
            "G1 n'a qu'une paire signée (G1-20) : le contrôle positif de filiation n'est pas exécutable, "
            "et P1/P2 n'auraient pas d'assise même avec les 26 signatures si G1 restait incomplet.",
            "5 groupes de sources sont byte-identiques parmi les 26 (10 textes) : 10 signatures seront "
            "identiques deux à deux ; daodejing et zhuangzi sont même identiques à qiwulun, déjà signé. "
            "Le manifeste demande quand même les 26 pour la traçabilité.",
            "3 des 26 sources sont sous le plancher de 300 mots utilisé par loi_analytique.py : "
            "epicurus_letters (84), sextus_pyrrho (42), zadeh_1965 (278). L'extracteur sign_analytic "
            "produit quand même un vecteur, mais il est hors du support des 44 signatures de référence.",
            "La calibration sur les 44 échoue sur 2 œuvres dans notre copie (bengio_2003 0,9678 ; "
            "mengzi 0,9891) : le test est bloqué tant que Panini ne fournit pas une calibration 44/44 "
            "ou une explication de l'écart (version de l'extracteur, WordNet, source).",
            "Le contrôle N5 du protocole B1 (colonnes d'atomes permutées) est vide pour la distance L2 : "
            "une permutation commune des colonnes est une isométrie. Il ne teste rien.",
            "Le corpus reste petit et biaisé : 59 textes, 27 paires signées, 5 doublons de sources, "
            "des dates de composition et des traductions anglaises. Le résultat ne se transporte pas.",
        ],
        "fichiers": {
            "fiche": "reports/rapport-panini-manifeste.md",
            "manifeste": "reports/panini-manifeste.json",
            "protocole_b1": "reports/protocole-date.json",
            "outil_panini": "tools/panini_signatures_26.py",
            "outil_rejeu": "tools/protocole_date.py",
        },
    }
    return doc


def verifier(doc: dict) -> list[str]:
    e = []
    if doc.get("tache") != "W4":
        e.append("tache != W4")
    m = doc.get("manifeste", {})
    if m.get("n_a_signer") != 26:
        e.append(f"n_a_signer={m.get('n_a_signer')} (attendu 26)")
    if len(m.get("a_signer", [])) != 26:
        e.append("a_signer != 26")
    ids = [t["id"] for t in m.get("a_signer", [])]
    if len(set(ids)) != len(ids):
        e.append("a_signer : ids dupliqués")
    if m.get("n_textes") != 59:
        e.append(f"n_textes={m.get('n_textes')} (attendu 59)")
    r = doc.get("rejeu", {})
    if r.get("n_paires") != 60:
        e.append(f"n_paires={r.get('n_paires')} (attendu 60)")
    if r.get("n_calculees") + r.get("n_manquantes") != 60:
        e.append("n_calculees + n_manquantes != 60")
    if r.get("p_value_H0") is not None:
        e.append("p_value_H0 ne doit pas être écrit")
    if r.get("statut") != "incomplet":
        e.append("statut != incomplet")
    if not doc.get("panini_lecture_seule", {}).get("identique"):
        e.append("Panini a changé pendant la construction")
    return e


def resume(doc: dict):
    m = doc["manifeste"]
    r = doc["rejeu"]
    c = doc.get("calibration", {}).get("mesure") or {}
    print("W4 — manifeste Panini")
    print(f"  à signer           : {m['n_a_signer']} textes ({len(m['sources_courtes'])} sources < 300 mots)")
    print(f"  doublons de sources: {len(m['doublons_sources'])} groupes")
    print(f"  rejeu              : {r['n_calculees']}/60 paires")
    print(f"  par groupe         : G1 {r['par_groupe']['G1']['n_calculees']}/20, "
          f"G2 {r['par_groupe']['G2']['n_calculees']}/20, G3 {r['par_groupe']['G3']['n_calculees']}/20")
    print(f"  calibration        : {c.get('ok')}/{c.get('n')} ; échecs {c.get('echecs')}")
    print(f"  p-value H0         : {r['p_value_H0']}")
    print(f"  verdict            : {r['verdict']}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="W4 — manifeste Panini et rejeu disponible")
    ap.add_argument("--construire", action="store_true")
    ap.add_argument("--verifier", action="store_true")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--sortie", default=str(SORTIE))
    args = ap.parse_args(argv)
    if args.verifier:
        doc = lire(pathlib.Path(args.sortie))
        e = verifier(doc)
        print("OK" if not e else "ÉCHEC : " + " ; ".join(e))
        return 0 if not e else 1
    doc = construire()
    e = verifier(doc)
    if e:
        raise SystemExit("manifeste invalide : " + " ; ".join(e))
    p = pathlib.Path(args.sortie).resolve()
    if str(p).startswith(str(PANINI.resolve())):
        raise SystemExit("refus d'écrire dans Panini")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"écrit : {p}")
    resume(doc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
