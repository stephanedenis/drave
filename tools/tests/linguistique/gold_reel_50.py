#!/usr/bin/env python3
"""gold_reel_50.py — les 50 phrases réelles que l'heuristique rate (proposition C3/R).

POURQUOI. Le gold réel (`gold.json` 20 hand + `gold_reel.json` 432 reel) mesure le bloc
linguistique depuis B13. Ses erreurs ne sont plus réparties : le POS porte 275 erreurs de
tokens, la segmentation 346 segments manquants (dont 74 ADJ/ADV/PONCT que l'heuristique ne
produit pas), l'attachement **une seule** (g017, SUB). Le « gold 200+ » des fiches R n'est
donc pas un problème de **nombre** (452 > 200) : c'est un problème de **discrimination**.
Ce banc sélectionne 50 phrases réelles que l'heuristique rate, mesure ce qu'elles ajoutent,
et liste les **candidats à annoter** — sans modifier le gold (territoire S/D).

RÈGLE DE SÉLECTION (déterministe, aucune graine).
  1. score = 3 × (cible d'attachement absente ou fausse)
           + 2 × (token POS faux)
           + 1 × (segment gold absent au même span) ;
  2. quota 25 français + 25 anglais ;
  3. au plus 2 phrases par **signature d'erreur** (POS confondus, types de segments absents,
     types d'attachement) : une construction ne peut pas prendre tout le lot (les 11 négations
     « Ne …-t-il pas ? » sont plafonnées) ;
  4. départage par identifiant.

CONTRÔLES. 50 tirées au hasard (8 graines), 50 stratifiées (25 fr + 25 en, 1 hand par langue),
majoritaire (classe POS la plus fréquente) et uniforme (12 classes). Le tirage aléatoire ne
mesure pas la généralisation : il mesure que le lot dur n'est pas un hasard de composition.

USAGE.
    python3 tools/tests/linguistique/gold_reel_50.py \
      --sortie reports/rapport-gold-reel-50.json

Le gold est lu deux fois (sha256 avant/après) ; le script ne l'écrit jamais.
"""
from __future__ import annotations

import argparse
import collections
import copy
import hashlib
import json
import pathlib
import random
import subprocess
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import bloc_linguistique as bl  # noqa: E402

GOLD = RACINE / "tools/tests/linguistique/gold.json"
REEL = RACINE / "tools/tests/linguistique/gold_reel.json"
FERME = {"DET", "PREP", "PRON", "CONJ", "AUX", "ADV", "NUM"}
CLASSES = ["DET", "NOUN", "VERB", "ADJ", "ADV", "PRON", "PREP", "CONJ", "AUX", "NUM", "PONCT", "?"]
TYPES = ["GN", "GV", "GP", "REL", "SUB", "ADJ", "ADV", "PONCT"]


# --------------------------------------------------------------------------- lecture


def sha256(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def charger() -> list[dict]:
    """Les 452 phrases réelles : 20 hand + 432 reel, chacune avec sa source."""
    phrases = []
    for chemin, source in ((GOLD, "hand"), (REEL, "reel")):
        for p in json.loads(chemin.read_text(encoding="utf-8"))["phrases"]:
            p = dict(p)
            p["source"] = source
            phrases.append(p)
    return phrases


def commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=RACINE, capture_output=True,
                              text=True, timeout=10).stdout.strip() or "inconnu"
    except (OSError, subprocess.SubprocessError):
        return "inconnu"


# --------------------------------------------------------------------------- analyse


def _span(texte: str, d: int, f: int) -> str:
    return texte[d:f]


def analyser(h, p: dict) -> dict:
    """Une phrase : POS, segments, attachement, et la liste de ses erreurs."""
    texte = p["texte"]
    a = h.analyser(texte, p.get("langue") or "fr")
    pos = {(e.debut, e.fin): e.type for e in a.etiquettes if e.niveau == "pos"}

    pos_erreurs, pos_n = [], len(p["mots"])
    ok = ok_ferme = ok_ouvert = n_ferme = n_ouvert = 0
    for m in p["mots"]:
        pred = pos.get((m["debut"], m["fin"]), "?")
        juste = pred == m["pos"]
        ok += juste
        if m["pos"] in FERME:
            n_ferme += 1
            ok_ferme += juste
        else:
            n_ouvert += 1
            ok_ouvert += juste
        if not juste:
            pos_erreurs.append({"token": m["texte"], "gold": m["pos"], "predit": pred,
                                "debut": m["debut"], "fin": m["fin"],
                                "classe": "fermé" if m["pos"] in FERME else "ouvert",
                                # « ? » = aucun token prédit à ce span : c'est la
                                # tokenisation (élision, trait d'union), pas l'étiquette.
                                "genre": "tokenisation" if pred == "?" else "etiquette"})

    pred_seg = {(e.type, e.debut, e.fin) for e in a.etiquettes if e.niveau == "syntagme"}
    gold_seg = {(s["type"], s["debut"], s["fin"]) for s in p["segments"]}
    fn = sorted(gold_seg - pred_seg)
    fp = sorted(pred_seg - gold_seg)
    tp = sorted(gold_seg & pred_seg)

    labels = {(e.type, e.debut, e.fin): e for e in a.etiquettes if e.niveau == "syntagme"}
    att_erreurs, targets, att_ok = [], 0, 0
    for s in p["segments"]:
        cibles = s.get("cibles") or ([s["cible"]] if s.get("cible") else [])
        if not cibles:
            continue
        targets += 1
        e = labels.get((s["type"], s["debut"], s["fin"]))
        if e is None:
            att_erreurs.append({"type": s["type"], "erreur": "span_absent",
                                "segment": s["texte"], "cible_attendue": cibles[0],
                                "cible_predite": None})
        else:
            cible = ((e.meta or {}).get("attachement") or {}).get("cible", "")
            if cible == cibles[0]:
                att_ok += 1
            else:
                att_erreurs.append({"type": s["type"], "erreur": "cible",
                                    "segment": s["texte"], "cible_attendue": cibles[0],
                                    "cible_predite": cible})

    signature = (
        p.get("langue") or "fr",
        tuple(sorted((x["gold"], x["predit"]) for x in pos_erreurs)),
        tuple(sorted(x[0] for x in fn)),
        tuple(sorted((x["type"], x["erreur"]) for x in att_erreurs)),
    )
    return {
        "id": p["id"], "source": p["source"], "langue": p.get("langue") or "fr",
        "texte": texte, "n_mots": pos_n, "n_segments": len(p["segments"]),
        "pos": {"n": pos_n, "ok": ok, "n_ferme": n_ferme, "ok_ferme": ok_ferme,
                "n_ouvert": n_ouvert, "ok_ouvert": ok_ouvert, "erreurs": pos_erreurs},
        "segments": {
            "tp": [{"type": t, "texte": _span(texte, d, f), "debut": d, "fin": f}
                   for t, d, f in tp],
            "fn": [{"type": t, "texte": _span(texte, d, f), "debut": d, "fin": f}
                   for t, d, f in fn],
            "fp": [{"type": t, "texte": _span(texte, d, f), "debut": d, "fin": f}
                   for t, d, f in fp],
        },
        "attachement": {"cibles": targets, "justes": att_ok, "erreurs": att_erreurs},
        "signature": signature,
        "score": 3 * len(att_erreurs) + 2 * len(pos_erreurs) + len(fn),
    }


# --------------------------------------------------------------------------- sélection


def _rangs(rows: list[dict], wa: int, wp: int, wf: int) -> list[dict]:
    for r in rows:
        r["score"] = wa * len(r["attachement"]["erreurs"]) + wp * len(r["pos"]["erreurs"]) \
            + wf * len(r["segments"]["fn"])
    return sorted(rows, key=lambda r: (-r["score"], r["id"]))


def selectionner(rows: list[dict], wa: int = 3, wp: int = 2, wf: int = 1,
                 quota: int = 25, cap: int = 2) -> list[dict]:
    """25 français + 25 anglais, au plus `cap` phrases par signature d'erreur."""
    choisies = []
    for langue in ("fr", "en"):
        candidates = _rangs([r for r in rows if r["langue"] == langue], wa, wp, wf)
        signatures = collections.Counter()
        prises, ids = [], set()
        for r in candidates:
            if len(prises) >= quota:
                break
            if signatures[r["signature"]] >= cap:
                continue
            prises.append(r)
            ids.add(r["id"])
            signatures[r["signature"]] += 1
        # filet de sécurité : si le plafond empêche d'atteindre le quota, on complète.
        if len(prises) < quota:
            for r in candidates:
                if len(prises) >= quota:
                    break
                if r["id"] not in ids:
                    prises.append(r)
                    ids.add(r["id"])
        choisies.extend(prises)
    return sorted(choisies, key=lambda r: (r["langue"], r["id"]))


# --------------------------------------------------------------------------- mesures


def _f1(tp: int, fp: int, fn: int) -> dict:
    p = tp / max(1, tp + fp)
    r = tp / max(1, tp + fn)
    return {"tp": tp, "fp": fp, "fn": fn, "precision": round(p, 4), "rappel": round(r, 4),
            "f1": round(2 * p * r / max(1e-9, p + r), 4)}


def metriques(rows: list[dict]) -> dict:
    """Les trois niveaux, plus le détail par type de segment et d'attachement."""
    pos_n = sum(r["pos"]["n"] for r in rows)
    pos_ok = sum(r["pos"]["ok"] for r in rows)
    nf = sum(r["pos"]["n_ferme"] for r in rows)
    okf = sum(r["pos"]["ok_ferme"] for r in rows)
    no = sum(r["pos"]["n_ouvert"] for r in rows)
    oko = sum(r["pos"]["ok_ouvert"] for r in rows)
    tp = sum(len(r["segments"]["tp"]) for r in rows)
    fp = sum(len(r["segments"]["fp"]) for r in rows)
    fn = sum(len(r["segments"]["fn"]) for r in rows)
    targets = sum(r["attachement"]["cibles"] for r in rows)
    att_ok = sum(r["attachement"]["justes"] for r in rows)
    att_err = sum(len(r["attachement"]["erreurs"]) for r in rows)
    tokenisation = sum(1 for r in rows for e in r["pos"]["erreurs"]
                       if e.get("genre") == "tokenisation")

    par_type = {}
    for t in TYPES:
        tp_t = sum(1 for r in rows for x in r["segments"]["tp"] if x["type"] == t)
        fp_t = sum(1 for r in rows for x in r["segments"]["fp"] if x["type"] == t)
        fn_t = sum(1 for r in rows for x in r["segments"]["fn"] if x["type"] == t)
        if tp_t + fp_t + fn_t:
            par_type[t] = _f1(tp_t, fp_t, fn_t)

    att_type = {}
    for t in ("GP", "REL", "SUB", "GN", "GV"):
        cibles = sum(1 for r in rows for s in r["_segments"] if s["type"] == t
                     and (s.get("cibles") or s.get("cible")))
        erreurs = sum(1 for r in rows for e in r["attachement"]["erreurs"] if e["type"] == t)
        if cibles:
            att_type[t] = {"cibles": cibles, "justes": cibles - erreurs,
                           "erreurs": erreurs,
                           "exactitude": round((cibles - erreurs) / cibles, 4)}

    return {
        "phrases": len(rows), "tokens": pos_n,
        "pos": {"exactitude": round(pos_ok / max(1, pos_n), 4),
                "ferme": round(okf / max(1, nf), 4), "ouvert": round(oko / max(1, no), 4),
                "justes": pos_ok, "erreurs": pos_n - pos_ok,
                "tokenisation": tokenisation,
                "etiquette_exactitude": round(pos_ok / max(1, pos_n - tokenisation), 4),
                "note": "`exactitude` compte la tokenisation ; `etiquette_exactitude` "
                        "retire les tokens gold sans token prédit (« ? »)."},
        "segmentation": _f1(tp, fp, fn),
        "segmentation_par_type": par_type,
        "attachement": {"cibles": targets, "justes": att_ok, "erreurs": att_err,
                        "exactitude": round(att_ok / max(1, targets), 4),
                        "par_type": att_type},
    }


def projeter(global_: dict, hard: dict) -> dict:
    """Projection si un **nouveau** lot du même profil était ajouté (452 → 502).

    Ce n'est **pas** une mesure : les 50 sont déjà dans le gold. C'est le coût d'honnêteté
    qu'aurait un gold qui contiendrait 50 phrases de plus de ce profil.
    """
    tp = global_["segmentation"]["tp"] + hard["segmentation"]["tp"]
    fp = global_["segmentation"]["fp"] + hard["segmentation"]["fp"]
    fn = global_["segmentation"]["fn"] + hard["segmentation"]["fn"]
    f1 = 2 * tp / max(1, 2 * tp + fp + fn)
    pos = (global_["pos"]["justes"] + hard["pos"]["justes"]) / max(
        1, global_["tokens"] + hard["tokens"])
    att = (global_["attachement"]["justes"] + hard["attachement"]["justes"]) / max(
        1, global_["attachement"]["cibles"] + hard["attachement"]["cibles"])
    return {
        "phrases": global_["phrases"] + hard["phrases"],
        "pos": round(pos, 4),
        "f1": round(f1, 4),
        "attachement": round(att, 4),
        "delta_pos": round((pos - global_["pos"]["exactitude"]) * 100, 2),
        "delta_f1": round((f1 - global_["segmentation"]["f1"]) * 100, 2),
        "delta_attachement": round((att - global_["attachement"]["exactitude"]) * 100, 2),
        "note": "projection, pas une mesure : les 50 sont déjà dans le gold.",
    }


def controler(rows: list[dict], choisies: list[dict], tirages: int = 8) -> dict:
    """Tirages aléatoires (simple et stratifié) + planchers majoritaire/uniforme."""
    hard_ids = {r["id"] for r in choisies}
    hand_fr = [r for r in rows if r["source"] == "hand" and r["langue"] == "fr"]
    hand_en = [r for r in rows if r["source"] == "hand" and r["langue"] == "en"]
    reel_fr = [r for r in rows if r["source"] == "reel" and r["langue"] == "fr"]
    reel_en = [r for r in rows if r["source"] == "reel" and r["langue"] == "en"]

    simple, stratifie = [], []
    for graine in range(tirages):
        rng = random.Random(graine)
        simple.append({"graine": graine, "mesure": metriques(rng.sample(rows, 50))})
        rng2 = random.Random(1000 + graine)
        tirage = (rng2.sample(reel_fr, 24) + [rng2.choice(hand_fr)]
                  + rng2.sample(reel_en, 24) + [rng2.choice(hand_en)])
        stratifie.append({"graine": graine, "mesure": metriques(tirage)})

    # les tokens gold sont stockés dans `_tokens` par `main` pour les planchers.
    def majoritaire(rs: list[dict]) -> dict:
        c = collections.Counter(t for r in rs for t in r["_tokens"])
        classe, n = c.most_common(1)[0]
        total = sum(c.values())
        return {"classe": classe, "justes": n, "tokens": total, "exactitude": round(n / total, 4)}

    def uniforme(rs: list[dict], graine: int = 0) -> dict:
        rng = random.Random(graine)
        n = ok = 0
        for r in rs:
            for gold in r["_tokens"]:
                n += 1
                ok += rng.choice(CLASSES) == gold
        return {"graine": graine, "justes": ok, "tokens": n, "exactitude": round(ok / max(1, n), 4)}

    return {
        "simple": simple,
        "stratifie": stratifie,
        "majoritaire": {"hard_50": majoritaire(choisies), "global_452": majoritaire(rows)},
        "uniforme": {"hard_50": uniforme(choisies), "global_452": uniforme(rows)},
    }


def sensibilite(rows: list[dict], reference: list[dict]) -> list[dict]:
    """Le lot change-t-il quand on change les poids ? (contrôle de la règle)."""
    base = {r["id"] for r in reference}
    sorties = []
    for wa, wp, wf in ((3, 2, 1), (2, 2, 1), (5, 2, 1), (3, 3, 1), (3, 1, 1), (1, 1, 1)):
        # copie : `_rangs` réécrit `score` sur les objets, et le lot de référence doit garder
        # les scores du poids 3/2/1 pour la fiche.
        lot = {r["id"] for r in selectionner(copy.deepcopy(rows), wa, wp, wf)}
        sorties.append({"poids": f"{wa}/{wp}/{wf}", "commun": len(base & lot),
                        "jaccard": round(len(base & lot) / len(base | lot), 3)})
    return sorties


# --------------------------------------------------------------------------- candidats


def candidats(phrases: list[dict], choisies: list[dict]) -> dict:
    """Les segments sans `cible` : ce que S devrait annoter pour étendre le gold."""
    hard_ids = {r["id"] for r in choisies}
    prioritaires, gn_gv = [], []
    for p in phrases:
        for s in p["segments"]:
            cibles = s.get("cibles") or ([s["cible"]] if s.get("cible") else [])
            if cibles:
                continue
            item = {"id": p["id"], "type": s["type"], "segment": s["texte"],
                    "debut": s["debut"], "fin": s["fin"], "phrase": p["texte"],
                    "dans_hard_50": p["id"] in hard_ids}
            if s["type"] in ("GP", "REL", "SUB"):
                prioritaires.append(item)
            elif s["type"] in ("GN", "GV"):
                gn_gv.append(item)
    hard_gn_gv = [x for x in gn_gv if x["dans_hard_50"]]
    autres_gn_gv = [x for x in gn_gv if not x["dans_hard_50"]]
    return {
        "priorite_1_attachement": {
            "principe": "les types qui portent une cible d'attachement (GP, REL, SUB) ; "
                        "le gold en a 0 sans cible sur 58 REL, 9 GP et 1 SUB.",
            "candidats": prioritaires,
            "total": len(prioritaires),
            "dans_hard_50": sum(1 for x in prioritaires if x["dans_hard_50"]),
        },
        "priorite_2_gn_gv": {
            "principe": "les GN/GV n'ont aucune cible dans le gold courant ; les annoter "
                        "étend l'attachement à la structure argumentale (effort plus lourd).",
            "total": len(gn_gv),
            "dans_hard_50": len(hard_gn_gv),
            "par_type": dict(collections.Counter(x["type"] for x in gn_gv)),
            "dans_hard_50_par_type": dict(collections.Counter(x["type"] for x in hard_gn_gv)),
            "exemples_hard_50": hard_gn_gv[:12],
            "exemples": hard_gn_gv[:10] + autres_gn_gv[:2],
        },
        "non_candidats": {
            "principe": "ADJ/ADV/PONCT ne sont pas des cibles d'attachement ; l'heuristique "
                        "ne les produit pas (rappel 0), donc les ajouter mesurerait une "
                        "fonction manquante, pas une annotation.",
            "par_type": dict(collections.Counter(s["type"] for p in phrases
                                                 for s in p["segments"]
                                                 if s["type"] in ("ADJ", "ADV", "PONCT"))),
        },
        "phrases_du_lot": [
            {"id": r["id"], "source": r["source"], "langue": r["langue"],
             "texte": r["texte"], "score": r["score"],
             "pos_erreurs": len(r["pos"]["erreurs"]),
             "segments_fn": len(r["segments"]["fn"]),
             "att_erreurs": len(r["attachement"]["erreurs"])}
            for r in choisies
        ],
    }


# --------------------------------------------------------------------------- sortie


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sortie", default=str(RACINE / "reports" / "rapport-gold-reel-50.json"))
    args = ap.parse_args()

    avant = {str(p): sha256(p) for p in (GOLD, REEL)}
    phrases = charger()
    h = bl.Heuristique()
    rows = [analyser(h, p) for p in phrases]
    for r, p in zip(rows, phrases):
        r["_tokens"] = [m["pos"] for m in p["mots"]]
        r["_segments"] = p["segments"]

    choisies = selectionner(rows)
    if len(choisies) != 50:
        raise SystemExit(f"la sélection doit faire 50 phrases, elle en fait {len(choisies)}")
    hard_ids = {r["id"] for r in choisies}
    reste = [r for r in rows if r["id"] not in hard_ids]

    mesures = {"global_452": metriques(rows), "hard_50": metriques(choisies),
               "reste_402": metriques(reste)}
    for nom, rs in (("hand_20", [r for r in rows if r["source"] == "hand"]),
                    ("reel_432", [r for r in rows if r["source"] == "reel"]),
                    ("fr_242", [r for r in rows if r["langue"] == "fr"]),
                    ("en_210", [r for r in rows if r["langue"] == "en"])):
        mesures[nom] = metriques(rs)

    # répartition des erreurs du lot dans le total
    def somme(rs, chemin) -> int:
        if chemin == "pos":
            return sum(len(r["pos"]["erreurs"]) for r in rs)
        if chemin == "fn":
            return sum(len(r["segments"]["fn"]) for r in rs)
        return sum(len(r["attachement"]["erreurs"]) for r in rs)

    part = {}
    for nom in ("pos", "fn", "att"):
        total = somme(rows, nom)
        lot = somme(choisies, nom)
        part[nom] = {"lot": lot, "total": total, "part": round(lot / max(1, total), 4)}

    phrases_avec = {
        "pos": sum(1 for r in rows if r["pos"]["erreurs"]),
        "segmentation": sum(1 for r in rows if r["segments"]["fn"] or r["segments"]["fp"]),
        "attachement": sum(1 for r in rows if r["attachement"]["erreurs"]),
    }

    pos_par_type_global = collections.Counter()
    genre_global = collections.Counter()
    for r in rows:
        for e in r["pos"]["erreurs"]:
            pos_par_type_global[(e["gold"], e["predit"])] += 1
            genre_global[e["genre"]] += 1
    pos_par_type_hard = collections.Counter()
    genre_hard = collections.Counter()
    for r in choisies:
        for e in r["pos"]["erreurs"]:
            pos_par_type_hard[(e["gold"], e["predit"])] += 1
            genre_hard[e["genre"]] += 1
    fn_par_type = collections.Counter(x["type"] for r in choisies for x in r["segments"]["fn"])
    fp_par_type = collections.Counter(x["type"] for r in choisies for x in r["segments"]["fp"])
    att_par_type = collections.Counter((e["type"], e["erreur"]) for r in choisies
                                       for e in r["attachement"]["erreurs"])

    apres = {str(p): sha256(p) for p in (GOLD, REEL)}
    resultat = {
        "date": time.strftime("%Y-%m-%d %H:%M %Z"),
        "ligne": "R0.7 / B13",
        "tache": "C3 — coordination R, le gold réel étendu",
        "commit_mesure": commit(),
        "objet": {
            "definition": "le gold linguistique réel (hand + reel) des fiches R/B13, "
                          "et non le « gold de pensée » ; « 200+ » est un libellé obsolète "
                          "(452 phrases) et ambigu (T15).",
            "phrases": len(phrases),
            "hand": sum(1 for p in phrases if p["source"] == "hand"),
            "reel": sum(1 for p in phrases if p["source"] == "reel"),
            "tokens": sum(len(p["mots"]) for p in phrases),
            "segments": sum(len(p["segments"]) for p in phrases),
            "cibles_attachement": sum(1 for p in phrases for s in p["segments"]
                                      if s.get("cibles") or s.get("cible")),
            "fichiers": {str(p.relative_to(RACINE)): avant[str(p)] for p in (GOLD, REEL)},
        },
        "heuristique": {
            "global": mesures["global_452"],
            "par_langue": {"fr": mesures["fr_242"], "en": mesures["en_210"]},
            "par_source": {"hand": mesures["hand_20"], "reel": mesures["reel_432"]},
            "erreurs": {
                "phrases_avec_pos": phrases_avec["pos"],
                "phrases_avec_segmentation": phrases_avec["segmentation"],
                "phrases_avec_attachement": phrases_avec["attachement"],
                "pos": {"total": somme(rows, "pos"),
                        "par_type": {f"{g}->{p}": n
                                     for (g, p), n in pos_par_type_global.most_common()},
                        "genre": dict(genre_global),
                        "note": "« ? » = token gold sans token prédit au même span "
                                "(élision/trait d'union) : erreur de tokenisation, pas "
                                "d'étiquette."},
                "segmentation": {"fn_total": somme(rows, "fn"),
                                 "fn_par_type": dict(collections.Counter(
                                     x["type"] for r in rows for x in r["segments"]["fn"])),
                                 "fp_par_type": dict(collections.Counter(
                                     x["type"] for r in rows for x in r["segments"]["fp"])),
                                 "structurel": "ADJ/ADV/PONCT : l'heuristique ne les produit "
                                               "pas (rappel 0), 74 des 346 segments absents."},
                "attachement": mesures["global_452"]["attachement"],
            },
        },
        "selection": {
            "regle": "score = 3×att + 2×POS + 1×segment absent ; 25 fr + 25 en ; "
                     "au plus 2 phrases par signature d'erreur ; départage par id.",
            "phrases": len(choisies),
            "ids": [r["id"] for r in choisies],
            "composition": {
                "sources": dict(collections.Counter(r["source"] for r in choisies)),
                "langues": dict(collections.Counter(r["langue"] for r in choisies)),
                "signatures_distinctes": len({r["signature"] for r in choisies}),
                "score_min": min(r["score"] for r in choisies),
                "score_max": max(r["score"] for r in choisies),
                "tokens": sum(r["n_mots"] for r in choisies),
                "segments": sum(r["n_segments"] for r in choisies),
                "cibles_attachement": sum(r["attachement"]["cibles"] for r in choisies),
            },
            "phrases": [{"id": r["id"], "source": r["source"], "langue": r["langue"],
                         "texte": r["texte"], "score": r["score"],
                         "pos_erreurs": len(r["pos"]["erreurs"]),
                         "segments_fn": len(r["segments"]["fn"]),
                         "segments_fp": len(r["segments"]["fp"]),
                         "att_erreurs": len(r["attachement"]["erreurs"])}
                        for r in choisies],
        },
        "mesure": {
            **mesures,
            "part_des_erreurs": part,
            "controles": controler(rows, choisies),
            "sensibilite_poids": sensibilite(rows, choisies),
            "projection_502": projeter(mesures["global_452"], mesures["hard_50"]),
        },
        "erreurs_hard_50": {
            "pos_par_type": {f"{g}->{p}": n
                             for (g, p), n in pos_par_type_hard.most_common()},
            "pos_genre": dict(genre_hard),
            "segmentation": {"fn_par_type": dict(fn_par_type), "fp_par_type": dict(fp_par_type)},
            "attachement_par_type": {f"{t}/{e}": n for (t, e), n in att_par_type.most_common()},
            "phrases": [
                {"id": r["id"], "source": r["source"], "langue": r["langue"],
                 "texte": r["texte"], "score": r["score"],
                 "pos": {"erreurs": r["pos"]["erreurs"]},
                 "segments": {"fn": r["segments"]["fn"], "fp": r["segments"]["fp"]},
                 "attachement": r["attachement"]["erreurs"]}
                for r in choisies
            ],
        },
        "candidats_a_annoter": candidats(phrases, choisies),
        "controles_negatifs": {
            "tirage_simple": "50 phrases au hasard, 8 graines : le POS reste ≥ 85 %.",
            "tirage_stratifie": "25 fr + 25 en, 1 hand par langue, 8 graines : même ordre.",
            "majoritaire": "toujours la classe POS la plus fréquente.",
            "uniforme": "tirage uniforme sur 12 classes POS.",
            "sensibilite": "le lot change peu quand les poids changent (sauf si le POS tombe "
                           "à poids 1).",
        },
        "gold_intact": {"avant": avant, "apres": apres, "identique": avant == apres},
        "limites": [
            "Les 50 sont déjà dans le gold : ce n'est pas un ajout de phrases, c'est un "
            "sous-ensemble dur tenu à l'écart (ou une base d'annotation).",
            "La sélection est faite sur les erreurs de l'heuristique : elle est circulaire "
            "par construction et ne mesure pas la généralisation.",
            "Les 20 hand ont servi à dessiner les règles : les 2 hand du lot sont in-sample.",
            "L'attachement du lot (22 cibles, 21 justes) est saturé : il ne teste que g017.",
            "Le gold lui-même peut être faux (annotations manuelles, conventions) ; une "
            "mauvaise étiquette compte comme une erreur de l'heuristique.",
            "ADJ/ADV/PONCT : 74 segments absents par construction, pas par erreur.",
            "Le tagger neuronal n'est pas mesuré ici ; la décision R0.7 garde son split réel.",
        ],
        "ce_qui_ferait_faux": [
            "Un gold corrigé (une étiquette fausse sur les 50 change le score et la sélection).",
            "Une heuristique modifiée après le 2026-11-15 (le score, donc le lot, change).",
            "Un tirage aléatoire différent (les contrôles sont à 8 graines, pas exhaustifs).",
            "Une convention d'attachement différente (GP : verbe ou nom ; SUB : verbe gouverneur).",
            "Une autre définition du « gold 200+ » (gold de pensée plutôt que gold linguistique).",
        ],
        "fichiers": {
            "fiche": "reports/rapport-gold-reel-50.md",
            "json": "reports/rapport-gold-reel-50.json",
            "script": "tools/tests/linguistique/gold_reel_50.py",
            "lus_non_modifies": ["tools/tests/linguistique/gold.json",
                                 "tools/tests/linguistique/gold_reel.json",
                                 "tools/bloc_linguistique.py"],
        },
    }
    sortie = pathlib.Path(args.sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(json.dumps({
        "phrases": len(phrases), "selection": len(choisies),
        "global": mesures["global_452"]["pos"]["exactitude"],
        "hard": mesures["hard_50"]["pos"]["exactitude"],
        "reste": mesures["reste_402"]["pos"]["exactitude"],
        "hard_f1": mesures["hard_50"]["segmentation"]["f1"],
        "hard_att": mesures["hard_50"]["attachement"]["exactitude"],
        "part_pos": part["pos"], "part_fn": part["fn"], "part_att": part["att"],
        "gold_intact": avant == apres, "sortie": str(sortie),
    }, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
