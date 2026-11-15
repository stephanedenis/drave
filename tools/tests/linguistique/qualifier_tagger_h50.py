#!/usr/bin/env python3
"""qualifier_tagger_h50.py — W2 : le tagger POS sur le split 402 / H50.

POURQUOI. W1 a figé le gold réel 452 en un split **402** (l'entraînement) et **H50** (la tenue
à l'écart, sélectionnée sur les erreurs de l'heuristique). W2 mesure le tagger POS de l'API
DeepSeek sur les deux bases, avec le **cache chaud** puis l'**API**, et applique la règle :
une règle qui ne gagne que sur H50 est **rejetée** ; le contrôle est la non-régression du 402.

CE QUE LE BANC MESURE.
- POS de l'heuristique et du tagger (`Cascade` 0,6, POS neuronal, syntagmes heuristiques) sur
  402, H50, le total 452 et un tirage aléatoire de composition (hors H50).
- Le delta POS (exactitude, fermé, ouvert), le F1 et l'attachement (contrôles de non-régression).
- Le coût : appels, requêtes réseau, cache, tokens, latence par requête et par phrase.
- Trois passes : **cache chaud** (cache disque existant), **API** (cache neuf, tout le réseau),
  **cache chaud après API** (le cache neuf, rejoué : 0 réseau, 0 token).

USAGE.
    python3 tools/tests/linguistique/qualifier_tagger_h50.py \
      --sortie reports/rapport-tagger-h50.json --mode tous

La clé est lue par `tools/llm/deepseek.py` (DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key,
DEEPSEEK_API_KEY). Elle n'est jamais affichée, ni écrite dans le JSON, ni dans le cache.
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import pathlib
import shutil
import statistics
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE))
sys.path.insert(0, str(RACINE / "tools"))
sys.path.insert(0, str(RACINE / "tools" / "tests" / "linguistique"))

import bloc_linguistique as bl  # noqa: E402
import drave  # noqa: E402
from tools.llm.deepseek import DeepSeek  # noqa: E402
from tools.tests.linguistique.evaluer_gold import evaluer_bloc  # noqa: E402

GOLD = RACINE / "tools" / "tests" / "linguistique" / "gold.json"
REEL = RACINE / "tools" / "tests" / "linguistique" / "gold_reel.json"
SPLIT = RACINE / "reports" / "rapport-gold-452.json"
CLASSES = ("DET", "NOUN", "VERB", "ADJ", "ADV", "PRON", "PREP", "CONJ", "AUX", "NUM", "PONCT", "?")
BASES = ("reste_402", "h50", "total", "tirage")
LIBELLES = {"reste_402": "402 (l'entraînement)", "h50": "H50 (la tenue à l'écart)",
            "total": "452 (total)", "tirage": "tirage 20261116 hors H50 (composition)"}


# --------------------------------------------------------------------------- données


def charger_452() -> list[dict]:
    """Les 452 phrases réelles : 20 hand + 432 corpus, avec leur source."""
    phrases = []
    for chemin, source in ((GOLD, "hand"), (REEL, "reel")):
        for p in json.loads(chemin.read_text(encoding="utf-8"))["phrases"]:
            p = dict(p)
            p["source"] = source
            phrases.append(p)
    return phrases


def charger_split() -> dict:
    """Le split figé par W1 ; si le JSON manque, le reproduire par le script C3/W1."""
    if SPLIT.is_file():
        return json.loads(SPLIT.read_text(encoding="utf-8"))["split"]
    import gold_reel_50 as c3
    rows = [c3.analyser(bl.Heuristique(), p) for p in c3.charger()]
    choisies = c3.selectionner(rows)
    h50 = sorted(r["id"] for r in choisies)
    total = {p["id"] for p in c3.charger()}
    reste = sorted(total - set(h50))
    return {"nom": "402 / H50", "manifeste_sha256": "recalculé (W1 absent)",
            "h50_ids": h50, "reste_402_ids": reste,
            "partition": {"h50": len(h50), "reste_402": len(reste), "total": len(total),
                          "intersection": 0},
            "controle_aleatoire_graine": {"ids": []}}


def construire_bases(phrases: list[dict], split: dict) -> dict[str, list[dict]]:
    h50_ids = set(split["h50_ids"])
    reste_ids = set(split["reste_402_ids"])
    total_ids = {p["id"] for p in phrases}
    if len(h50_ids) != 50 or len(reste_ids) != 402:
        raise SystemExit(f"split inattendu : H50={len(h50_ids)} 402={len(reste_ids)}")
    if h50_ids & reste_ids or h50_ids | reste_ids != total_ids:
        raise SystemExit("partition invalide : H50 ∩ 402 non vide ou union ≠ 452")
    tirage_ids = set(split.get("controle_aleatoire_graine", {}).get("ids", []))
    tirage_ids -= h50_ids
    bases = {
        "reste_402": [p for p in phrases if p["id"] in reste_ids],
        "h50": [p for p in phrases if p["id"] in h50_ids],
        "total": list(phrases),
        "tirage": [p for p in phrases if p["id"] in tirage_ids],
    }
    for nom, ps in bases.items():
        if not ps:
            raise SystemExit(f"base vide : {nom}")
    return {nom: {"nom": nom, "phrases": ps} for nom, ps in bases.items()}


def duplicats(phrases: list[dict]) -> list[dict]:
    """Les textes identiques (même langue) : le tagger les sert une fois par cache mémoire."""
    groupes = collections.defaultdict(list)
    for p in phrases:
        groupes[(p["texte"], p.get("langue", "fr"))].append(p["id"])
    return [{"texte": t, "langue": lg, "n": len(ids), "ids": ids}
            for (t, lg), ids in groupes.items() if len(ids) > 1]


def composition(phrases: list[dict]) -> dict:
    langues = collections.Counter(p.get("langue", "fr") for p in phrases)
    sources = collections.Counter(p.get("source", "?") for p in phrases)
    return {"phrases": len(phrases), "tokens": sum(len(p["mots"]) for p in phrases),
            "langues": dict(langues), "sources": dict(sources),
            "ids": sorted(p["id"] for p in phrases)}


# --------------------------------------------------------------------------- cache


def meta_cache(chemin: pathlib.Path) -> dict:
    """Ce que le cache disque contient : nombre, dates, modèles (sans la clé)."""
    if not chemin.is_dir():
        return {"fichiers": 0, "dates": {}, "modeles": {}}
    fichiers = sorted(chemin.glob("*.json"))
    dates, modeles = [], collections.Counter()
    for f in fichiers:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if d.get("recu_le"):
            dates.append(d["recu_le"])
        if d.get("modele"):
            modeles[d["modele"]] += 1
    return {"fichiers": len(fichiers),
            "dates": {"min": min(dates) if dates else None,
                      "max": max(dates) if dates else None},
            "modeles": dict(modeles)}


# --------------------------------------------------------------------------- mesure


class Journal:
    """Les appels réellement faits au transport, avec la phrase courante."""

    def __init__(self) -> None:
        self.calls: list[dict] = []
        self.phrase: str | None = None
        self.langue: str | None = None
        self.tokens_reseau = 0
        self.tokens_cache = 0
        self.latence_reseau_s = 0.0
        self.latence_cache_s = 0.0

    def par_phrase(self) -> dict:
        return collections.defaultdict(lambda: {"appels": 0, "requetes": 0, "cache": 0,
                                                 "tokens_reseau": 0, "tokens_cache": 0,
                                                 "latence_reseau_s": 0.0,
                                                 "latence_wall_s": 0.0})

    def cout(self, phrases: list[dict]) -> dict:
        textes = {(p["texte"], p.get("langue") or "fr") for p in phrases}
        calls = [c for c in self.calls if (c["phrase"], c["langue"]) in textes]
        appels = len(calls)
        requetes = sum(1 for c in calls if not c["cache"])
        cache = sum(1 for c in calls if c["cache"])
        tokens_reseau = sum(c["tokens"] for c in calls if not c["cache"])
        tokens_cache = sum(c["tokens"] for c in calls if c["cache"])
        lat_reseau = sum(c["latence_api_s"] for c in calls if not c["cache"])
        lat_cache = sum(c["latence_api_s"] for c in calls if c["cache"])
        lat_wall = sum(c["latence_wall_s"] for c in calls)
        lat_net = sorted(c["latence_api_s"] for c in calls if not c["cache"])
        n = max(1, len(phrases))
        sans_appel = [p["id"] for p in phrases
                      if (p["texte"], p.get("langue") or "fr") not in
                      {(c["phrase"], c["langue"]) for c in calls}]
        return {
            "phrases": len(phrases),
            "appels": appels, "requetes": requetes, "cache": cache,
            "tokens_reseau": tokens_reseau, "tokens_cache": tokens_cache,
            "latence_reseau_s": round(lat_reseau, 3), "latence_cache_s": round(lat_cache, 3),
            "latence_wall_s": round(lat_wall, 3),
            "latence_requete": {
                "moyenne": round(statistics.fmean(lat_net), 3) if lat_net else 0.0,
                "mediane": round(statistics.median(lat_net), 3) if lat_net else 0.0,
                "p95": round(lat_net[min(len(lat_net) - 1,
                                          max(0, math.ceil(0.95 * len(lat_net)) - 1))], 3)
                       if lat_net else 0.0,
                "max": round(lat_net[-1], 3) if lat_net else 0.0,
            },
            "par_phrase": {
                "appels": round(appels / n, 4), "requetes": round(requetes / n, 4),
                "cache": round(cache / n, 4), "tokens_reseau": round(tokens_reseau / n, 2),
                "tokens_total": round((tokens_reseau + tokens_cache) / n, 2),
                "latence_reseau_s": round(lat_reseau / n, 4),
                "latence_wall_s": round(lat_wall / n, 4),
            },
            "phrases_sans_appel": {"n": len(sans_appel), "ids": sans_appel[:20]},
        }


def _suivi(cascade, journal: Journal):
    class Suivi:
        nom = "cascade"

        def analyser(self, texte, langue=None, contexte=None):
            journal.phrase = texte
            journal.langue = langue or "fr"
            return cascade.analyser(texte, langue, contexte)

    return Suivi()


def _resume_pos(m: dict) -> dict:
    p = m["pos"]
    conf = p.get("confusions", {})
    justes = sum(conf.get(classe, {}).get(classe, 0) for classe in conf)
    return {"exactitude": p["exactitude"], "exactitude_ferme": p["exactitude_ferme"],
            "exactitude_ouvert": p["exactitude_ouvert"], "tokens": p["tokens"],
            "justes": justes, "confusions": conf}


def mesurer_base(nom: str, phrases: list[dict], client, pause: float = 0.0,
                 partition: str = "alternative") -> dict:
    """Heuristique + cascade tagger sur une base, avec le coût de CETTE mesure."""
    h = bl.Heuristique(partition=partition)
    journal = Journal()
    stats = {"appels": 0, "requetes": 0, "cache": 0, "tokens": 0, "latence_s": 0.0,
             "modeles": {}, "cle_refusee": 0}

    def transport(invite: str, grammaire: str, max_jetons: int) -> str:
        stats["appels"] += 1
        if pause:
            time.sleep(pause)
        t0 = time.perf_counter()
        try:
            r = client.demande(invite, temperature=0.0,
                               max_tokens=max(64, int(max_jetons or 256)))
        except Exception as exc:  # noqa: BLE001
            code = getattr(exc, "code", None)
            if code in (401, 403):
                stats["cle_refusee"] = int(code)
            raise
        dt = time.perf_counter() - t0
        usage = r.usage if isinstance(r.usage, dict) else {}
        tokens = int(usage.get("total_tokens", 0) or 0)
        lat_api = float(r.latence_s or 0.0)
        journal.calls.append({"phrase": journal.phrase, "langue": journal.langue,
                              "cache": bool(r.cache), "tokens": tokens,
                              "latence_api_s": lat_api, "latence_wall_s": dt,
                              "modele": r.modele})
        if r.cache:
            stats["cache"] += 1
            journal.tokens_cache += tokens
            journal.latence_cache_s += lat_api
        else:
            stats["requetes"] += 1
            stats["tokens"] += tokens
            stats["latence_s"] += lat_api
            journal.tokens_reseau += tokens
            journal.latence_reseau_s += lat_api
        stats["modeles"][r.modele] = stats["modeles"].get(r.modele, 0) + 1
        return r.contenu

    cascade = drave._cascade_tagger(transport, partition=partition, stats=stats)
    suivi = _suivi(cascade, journal)
    t0 = time.perf_counter()
    mh = evaluer_bloc("heuristique", h, phrases)
    mt = evaluer_bloc("cascade", suivi, phrases)
    refus = [p["id"] for p in phrases if suivi.analyser(p["texte"], p["langue"]).refus]
    duree = time.perf_counter() - t0
    par_langue = {}
    for langue in sorted({p.get("langue", "fr") for p in phrases}):
        sous = [p for p in phrases if p.get("langue", "fr") == langue]
        if not sous:
            continue
        mhl = evaluer_bloc("heuristique", bl.Heuristique(partition=partition), sous)
        mtl = evaluer_bloc("cascade", suivi, sous)
        par_langue[langue] = {
            "phrases": len(sous), "tokens": mhl["pos"]["tokens"],
            "heuristique": _resume_pos(mhl), "tagger": _resume_pos(mtl),
            "delta_pos": round(mtl["pos"]["exactitude"] - mhl["pos"]["exactitude"], 4),
            "delta_pos_ferme": round(mtl["pos"]["exactitude_ferme"]
                                     - mhl["pos"]["exactitude_ferme"], 4),
            "delta_pos_ouvert": round(mtl["pos"]["exactitude_ouvert"]
                                      - mhl["pos"]["exactitude_ouvert"], 4),
        }
    delta = {
        "pos": round(mt["pos"]["exactitude"] - mh["pos"]["exactitude"], 4),
        "pos_ferme": round(mt["pos"]["exactitude_ferme"] - mh["pos"]["exactitude_ferme"], 4),
        "pos_ouvert": round(mt["pos"]["exactitude_ouvert"] - mh["pos"]["exactitude_ouvert"], 4),
        "f1": round(mt["syntagme"]["f1"] - mh["syntagme"]["f1"], 4),
        "attachement": round(mt["attachement"]["exact_taux"]
                            - mh["attachement"]["exact_taux"], 4),
    }
    return {
        "base": nom, "libelle": LIBELLES.get(nom, nom),
        "composition": composition(phrases),
        "duree_mesure_s": round(duree, 2),
        "heuristique": {"pos": _resume_pos(mh), "syntagme": mh["syntagme"],
                        "attachement": mh["attachement"], "pragmatique": mh["pragmatique"],
                        "fraction_semantique": mh["fraction_semantique"]},
        "tagger": {"pos": _resume_pos(mt), "syntagme": mt["syntagme"],
                   "attachement": mt["attachement"], "pragmatique": mt["pragmatique"],
                   "fraction_semantique": mt["fraction_semantique"]},
        "delta": delta,
        "par_langue": par_langue,
        "refus": {"n": len(refus), "ids": refus},
        "cout": journal.cout(phrases),
        "stats_tagger": {"appels": stats["appels"], "requetes": stats["requetes"],
                         "cache": stats["cache"], "tokens": stats["tokens"],
                         "latence_s": round(stats["latence_s"], 3),
                         "modeles": dict(stats["modeles"]),
                         "cle_refusee": stats["cle_refusee"]},
    }


def passe(nom: str, bases: list[dict], client, cache_dir: pathlib.Path,
          pause: float, limite: int = 0, partition: str = "alternative") -> dict:
    """Une passe : chaque base a sa propre cascade (cache mémoire neuf), cache disque partagé."""
    client.cache_dir = pathlib.Path(cache_dir)
    avant = meta_cache(cache_dir)
    resultat = {"nom": nom, "cache_dir": str(cache_dir), "cache_avant": avant,
                "bases": {}, "modeles_renvoyes": collections.Counter()}
    cumul_modeles = collections.Counter()
    t0 = time.perf_counter()
    for base in bases:
        phrases = base["phrases"]
        if limite:
            phrases = phrases[:limite]
        print(f"[{nom}] {base['nom']} · {len(phrases)} phrases …", flush=True)
        m = mesurer_base(base["nom"], phrases, client, pause=pause, partition=partition)
        resultat["bases"][base["nom"]] = m
        cumul_modeles.update(m["stats_tagger"]["modeles"])
        print(f"[{nom}] {base['nom']} · POS {m['heuristique']['pos']['exactitude']:.4f} → "
              f"{m['tagger']['pos']['exactitude']:.4f} (Δ {m['delta']['pos']:+.4f}) · "
              f"requêtes {m['cout']['requetes']} · cache {m['cout']['cache']} · "
              f"{m['duree_mesure_s']:.1f} s", flush=True)
    resultat["duree_s"] = round(time.perf_counter() - t0, 2)
    resultat["cache_apres"] = meta_cache(cache_dir)
    resultat["modeles_renvoyes"] = dict(cumul_modeles)
    return resultat


# --------------------------------------------------------------------------- contrôles


def controle_hasard(phrases: list[dict], graine: int = 0) -> dict:
    """Deux planchers POS : classe majoritaire et classe tirée au hasard (graine 0)."""
    import random
    gold = [m["pos"] for p in phrases for m in p["mots"]]
    n = len(gold)
    majoritaire, n_maj = collections.Counter(gold).most_common(1)[0]
    rng = random.Random(graine)
    justes = sum(1 for c in gold if rng.choice(CLASSES) == c)
    return {"tokens": n,
            "majoritaire": {"classe": majoritaire, "taux": round(n_maj / max(1, n), 4)},
            "uniforme": {"graine": graine, "classes": len(CLASSES),
                         "taux": round(justes / max(1, n), 4)},
            "lecture": "le tagger et l'heuristique doivent être très au-dessus ; sinon le score "
                       "n'est qu'un effet de la distribution des classes."}


def regle_decision(api: dict) -> dict:
    """La règle de W2 appliquée au tagger : non-régression du 402, pas le gain H50 seul."""
    b402 = api["bases"]["reste_402"]
    b50 = api["bases"]["h50"]
    d402 = b402["delta"]["pos"]
    d50 = b50["delta"]["pos"]
    f1_402 = b402["delta"]["f1"]
    att_402 = b402["delta"]["attachement"]
    non_regression_402 = d402 >= 0 and f1_402 >= 0 and att_402 >= 0
    gagne_h50_seulement = d50 > 0 and d402 <= 0
    if non_regression_402 and d50 >= 0 and not gagne_h50_seulement:
        verdict = "accepté"
        raison = ("le tagger gagne sur 402 sans dégrader F1/attachement, et ne perd pas sur H50 : "
                  "il ne gagne pas seulement sur H50.")
    elif gagne_h50_seulement:
        verdict = "rejeté"
        raison = ("le tagger ne gagne que sur H50 (delta 402 ≤ 0) : sur-apprentissage du lot dur, "
                  "la règle le rejette.")
    elif d402 < 0:
        verdict = "rejeté"
        raison = "le 402 baisse : le contrôle de non-régression échoue."
    elif d50 < 0:
        verdict = "rejeté"
        raison = "H50 baisse : le tagger ne tient pas la tenue à l'écart."
    else:
        verdict = "rejeté"
        raison = "aucun gain sur les deux bases."
    return {
        "enonce": "Une règle qui ne gagne que sur H50 est rejetée ; le contrôle est la "
                  "non-régression du 402, pas le gain sur H50.",
        "critere": "delta POS 402 ≥ 0 ; F1 402 ≥ 0 ; attachement 402 ≥ 0 ; delta POS H50 ≥ 0 ; "
                   "rejet si le seul gain est H50 (delta 402 ≤ 0 et delta H50 > 0).",
        "application": {
            "delta_pos_402": d402, "delta_f1_402": f1_402,
            "delta_attachement_402": att_402, "delta_pos_h50": d50,
            "non_regression_402": non_regression_402,
            "gagne_h50_seulement": gagne_h50_seulement,
            "verdict": verdict, "raison": raison,
        },
    }


# --------------------------------------------------------------------------- sortie


def _cout_api_452(api: dict) -> dict:
    """Le coût de la passe API pour 402 + H50 (la base total est un rejeu cache)."""
    if not api:
        return {}
    b402, b50 = api["bases"]["reste_402"]["cout"], api["bases"]["h50"]["cout"]
    appels = b402["appels"] + b50["appels"]
    requetes = b402["requetes"] + b50["requetes"]
    cache = b402["cache"] + b50["cache"]
    tokens_reseau = b402["tokens_reseau"] + b50["tokens_reseau"]
    tokens_cache = b402["tokens_cache"] + b50["tokens_cache"]
    latence = b402["latence_reseau_s"] + b50["latence_reseau_s"]
    phrases = b402["phrases"] + b50["phrases"]
    n = max(1, phrases)
    return {
        "phrases": phrases, "appels": appels, "requetes": requetes, "cache": cache,
        "tokens_reseau": tokens_reseau, "tokens_cache": tokens_cache,
        "latence_reseau_s": round(latence, 3),
        "par_phrase": {
            "appels": round(appels / n, 4), "requetes": round(requetes / n, 4),
            "cache": round(cache / n, 4),
            "tokens_reseau": round(tokens_reseau / n, 2),
            "tokens_total": round((tokens_reseau + tokens_cache) / n, 2),
            "latence_reseau_s": round(latence / n, 4),
        },
        "lecture": "somme des bases 402 et H50 de la passe API ; la base total 452 est un "
                   "rejeu cache (0 réseau, 0 token réseau).",
    }


def _scores_api_452(api: dict) -> dict:
    if not api:
        return {}
    return {nom: {"pos_heuristique": b["heuristique"]["pos"]["exactitude"],
                  "pos_tagger": b["tagger"]["pos"]["exactitude"],
                  "delta_pos": b["delta"]["pos"],
                  "f1_heuristique": b["heuristique"]["syntagme"]["f1"],
                  "f1_tagger": b["tagger"]["syntagme"]["f1"],
                  "attachement_heuristique": b["heuristique"]["attachement"]["exact_taux"],
                  "attachement_tagger": b["tagger"]["attachement"]["exact_taux"]}
            for nom, b in api.get("bases", {}).items()}


def construire_rapport(args, phrases, split, bases, passes) -> dict:
    api = passes.get("api") or {}
    return {
        "date": time.strftime("%Y-%m-%d %H:%M %Z"),
        "tache": "W2 — le tagger POS sur le split 402 / H50",
        "ligne_roadmap": "R0.7 (le lecteur) / B13",
        "commit_mesure": _commit(),
        "modele_demande": args.modele or "deepseek-chat (défaut du client)",
        "or": {
            "phrases": len(phrases), "tokens": sum(len(p["mots"]) for p in phrases),
            "sources": dict(collections.Counter(p.get("source") for p in phrases)),
            "langues": dict(collections.Counter(p.get("langue", "fr") for p in phrases)),
            "textes_dupliques": duplicats(phrases),
        },
        "split": {
            "nom": split["nom"],
            "manifeste_sha256": split["manifeste_sha256"],
            "h50_ids": split["h50_ids"],
            "reste_402_ids": split["reste_402_ids"],
            "partition": split["partition"],
            "composition": {nom: composition(ps) for nom, ps in
                            (("h50", bases["h50"]["phrases"]),
                             ("reste_402", bases["reste_402"]["phrases"]),
                             ("total", bases["total"]["phrases"]),
                             ("tirage_hors_h50", bases["tirage"]["phrases"]))},
        },
        "dispositif": {
            "mesure": "evaluer_bloc de tools/tests/linguistique/evaluer_gold.py, la même "
                      "mesure que `drave evaluer` ; cascade `_cascade_tagger` de tools/drave.py",
            "fusion": "POS → neuronal ; syntagmes, rôles, attachement, pragmatique → heuristique",
            "seuil": drave.SEUIL_TAGGER,
            "partition": args.partition,
            "passes": {
                "cache_chaud": "cache disque existant (data/deepseek/cache), rejeu des réponses "
                               "déjà reçues ; les manquants vont à l'API",
                "api": "cache neuf (répertoire dédié), toutes les phrases passent par l'API",
                "cache_chaud_apres_api": "le cache neuf de la passe API, rejoué : 0 réseau, 0 token",
            },
            "ordre": "cache chaud → API → cache chaud après API",
        },
        "controles_negatifs": {
            "hasard_402": controle_hasard(bases["reste_402"]["phrases"]),
            "hasard_h50": controle_hasard(bases["h50"]["phrases"]),
            "hasard_tirage": controle_hasard(bases["tirage"]["phrases"]),
            "non_regression_402": "F1 et attachement du 402 doivent rester identiques : le tagger "
                                  "ne change que le POS ; un écart signalerait une fuite de la "
                                  "fusion sur les autres niveaux.",
            "tirage": "tirage aléatoire 20261116 de W1, H50 retiré (45 phrases) : contrôle de "
                      "composition, pas un échantillon neuf (les phrases sont dans le gold).",
        },
        "passes": passes,
        "regle_decision": regle_decision(api) if api else None,
        "cout_par_phrase": ({nom: {"phrases": b["cout"]["phrases"],
                                   "appels": b["cout"]["appels"],
                                   "requetes": b["cout"]["requetes"],
                                   "cache": b["cout"]["cache"],
                                   "tokens_reseau": b["cout"]["tokens_reseau"],
                                   "tokens_cache": b["cout"]["tokens_cache"],
                                   "par_phrase": b["cout"]["par_phrase"],
                                   "latence_requete": b["cout"]["latence_requete"]}
                             for nom, b in api.get("bases", {}).items()} if api else {}),
        "cout_api_452": _cout_api_452(api),
        "scores_api_452": _scores_api_452(api),
        "limites": [
            "H50 est sélectionné sur les erreurs de l'heuristique : son gain est circulaire et "
            "ne mesure pas la généralisation.",
            "Le 402 est l'entraînement de l'heuristique, pas du tagger : le tagger est un modèle "
            "externe, jamais entraîné sur ce gold ; le 402 est un contrôle de non-régression.",
            "Pas d'échantillon neuf annoté : le tirage 20261116 est un contrôle de composition, "
            "pas une généralisation hors gold.",
            "Le cache chaud rejoue des réponses d'un modèle et d'une date antérieurs ; la passe "
            "API (cache neuf) est la mesure de référence du modèle du jour.",
            "La température 0 n'est pas un déterminisme garanti de l'API ; le cache disque fige "
            "chaque réponse, le rejeu hors ligne est exact.",
            "Le tagger est un prompt français ; l'anglais de H50 (25 phrases) est mesuré mais "
            "le prompt n'est pas adapté à l'anglais.",
            "Les 4 cibles GP/SUB de H50 ne sont pas encore annotées : l'attachement de H50 porte "
            "sur 22 cibles, pas 26.",
        ],
        "ce_qui_ferait_faux": [
            "Une écriture dans gold.json ou gold_reel.json : le split et les scores changent.",
            "Un changement de l'heuristique ou de la tokenisation après le 2026-11-15 : H50, "
            "donc le delta, change.",
            "Une annotation des 4 cibles de H50 après cette mesure : le test serait contaminé.",
            "Un modèle d'API différent (deepseek-chat demandé, modèle renvoyé consigné) ou un "
            "changement de routage.",
            "Un cache chaud pris pour la mesure API : les réponses peuvent venir d'un autre jour.",
            "Une lecture du delta H50 sans le delta 402 : c'est précisément le sur-apprentissage "
            "que la règle rejette.",
        ],
        "fichiers": {
            "fiche": "reports/rapport-tagger-h50.md",
            "json": "reports/rapport-tagger-h50.json",
            "banc": "tools/tests/linguistique/qualifier_tagger_h50.py",
            "lus_non_modifies": ["tools/tests/linguistique/gold.json",
                                 "tools/tests/linguistique/gold_reel.json",
                                 "reports/rapport-gold-452.json"],
        },
    }


def _commit() -> str:
    import subprocess
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=RACINE, capture_output=True,
                              text=True, timeout=10).stdout.strip() or "inconnu"
    except (OSError, subprocess.SubprocessError):
        return "inconnu"


def ecrire(chemin: pathlib.Path, rapport: dict) -> None:
    chemin.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n",
                      encoding="utf-8")


# --------------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sortie", default="/tmp/tagger-h50.json")
    ap.add_argument("--mode", choices=("tous", "chaud", "api", "chaud_apres_api"), default="tous")
    ap.add_argument("--cache-chaud", default=str(RACINE / "data" / "deepseek" / "cache"),
                    help="cache disque de la passe cache chaud")
    ap.add_argument("--cache-api", default="/tmp/tagger-h50-api-cache",
                    help="cache neuf de la passe API")
    ap.add_argument("--reset-api-cache", action="store_true",
                    help="vider le cache API avant la passe (par défaut : seulement en mode tous)")
    ap.add_argument("--limite", type=int, default=0, help="N premières phrases par base (test)")
    ap.add_argument("--pause", type=float, default=0.0, help="pause entre appels (s)")
    ap.add_argument("--partition", default="alternative")
    ap.add_argument("--modele", default=None, help="modèle demandé (défaut : client)")
    a = ap.parse_args()

    phrases = charger_452()
    split = charger_split()
    bases = construire_bases(phrases, split)
    cache_chaud = pathlib.Path(a.cache_chaud)
    cache_api = pathlib.Path(a.cache_api)
    if a.mode in ("tous", "api") and not cache_api.is_absolute():
        raise SystemExit("--cache-api doit être un chemin absolu")
    if a.mode in ("tous", "api") and (a.reset_api_cache or a.mode == "tous"):
        if cache_api.exists():
            shutil.rmtree(cache_api)
        cache_api.mkdir(parents=True, exist_ok=True)
    try:
        cle = drave._cle_tagger()
    except drave.CleTaggerAbsente as exc:
        raise SystemExit(f"clé DeepSeek absente : {exc}") from None
    client = DeepSeek(cle=cle, modele=a.modele) if a.modele else DeepSeek(cle=cle)
    a.modele = client.modele
    if not client.disponible():
        raise SystemExit("clé DeepSeek absente : exportez DEEPSEEK_KEY_FILE ou déposez "
                         "~/.config/drave/deepseek.key")
    ordre = {"chaud": ["cache_chaud"], "api": ["api"],
             "chaud_apres_api": ["cache_chaud_apres_api"],
             "tous": ["cache_chaud", "api", "cache_chaud_apres_api"]}[a.mode]
    passes = {}
    for nom in ordre:
        cache_dir = cache_api if nom in ("api", "cache_chaud_apres_api") else cache_chaud
        resultat = passe(nom, [bases[b] for b in BASES],
                         client, cache_dir, a.pause, a.limite, a.partition)
        passes[nom] = resultat
        rapport = construire_rapport(a, phrases, split, bases, passes)
        ecrire(pathlib.Path(a.sortie), rapport)
        print(f"[{nom}] écrit · {a.sortie}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
