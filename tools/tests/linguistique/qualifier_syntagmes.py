#!/usr/bin/env python3
"""qualifier_syntagmes.py — qualifie le tagger de syntagmes local sur le gold (180 phrases).

Le tagger est `bloc_linguistique.NeuronalLLMChunks` : un modèle GGUF servi par `llama-server`,
une étiquette **BIO par token** contrainte par grammaire GBNF, et les spans reconstruits sur
la tokenisation du bloc. On mesure quatre lectures — **heuristique**, **neuronal seul**,
**cascade à priorité heuristique** (le défaut), **cascade à priorité confiance** — et trois
contrôles négatifs (vide, BIO aléatoire, têtes au hasard).

    python3 tools/tests/linguistique/qualifier_syntagmes.py --demarrer --port 18082 --workers 1 \
        --sortie reports/pensee-gold-syntagmes.json

Le serveur est lancé sur CPU (`-ngl 0`) : les GPU de N2 restent intacts.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import pathlib
import random
import statistics
import subprocess
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import bloc_linguistique as bl  # noqa: E402
from evaluer_gold import evaluer_bloc  # noqa: E402
from qualifier_neuronal import _fichiers, _sante, _version, demarrer_serveur  # noqa: E402

GOLD = pathlib.Path(__file__).with_name("gold.json")
SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")


def charger() -> list[dict]:
    hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
    synth = json.loads(SYNTH.read_text(encoding="utf-8"))["phrases"]
    for p in hand:
        p["source"] = "hand"
    for p in synth:
        p["source"] = "synth"
    return hand + synth


def _segments_bio(tokens: list[dict], bio: list[str]) -> set[tuple[str, int, int]]:
    """Reconstruit les spans d'une séquence BIO (même règle tolérante que le tagger)."""
    segs: set[tuple[str, int, int]] = set()
    courant = None
    for m, etiquette in zip(tokens, bio):
        if etiquette == "O":
            if courant:
                segs.add(tuple(courant)); courant = None
            continue
        prefixe, typ = etiquette.split("-", 1)
        if prefixe == "B" or courant is None or courant[0] != typ:
            if courant:
                segs.add(tuple(courant))
            courant = [typ, m["debut"], m["fin"]]
        else:
            courant[2] = m["fin"]
    if courant:
        segs.add(tuple(courant))
    return segs


def _aleatoire(phrases: list[dict], graine: int = 0) -> dict[str, set]:
    rng = random.Random(graine)
    sortie = {}
    for p in phrases:
        n = len(p["mots"])
        bio = [rng.choice(bl.ETIQUETTES_BIO) for _ in range(n)]
        sortie[p["id"]] = _segments_bio(p["mots"], bio)
    return sortie


def _score_ensembles(ensembles: dict[str, set], phrases: list[dict], mode: str) -> dict:
    tp = fp = fn = 0
    for p in phrases:
        if mode == "exact":
            gold = {(s["type"], s["debut"], s["fin"]) for s in p["segments"]}
            pred = ensembles[p["id"]]
        else:
            gold = {(s["type"], s["debut"]) for s in p["segments"]}
            pred = {(t, d) for t, d, _ in ensembles[p["id"]]}
        tp += len(gold & pred); fp += len(pred - gold); fn += len(gold - pred)
    p = tp / max(1, tp + fp); r = tp / max(1, fn + tp)
    return {"precision": round(p, 4), "rappel": round(r, 4),
            "f1": round(2 * p * r / max(1e-9, p + r), 4), "tp": tp, "fp": fp, "fn": fn}


def _sources(fonction, phrases: list[dict]) -> dict:
    """`fonction(ps)` rend les annotations d'un bloc sur un sous-ensemble."""
    hand = [p for p in phrases if p["source"] == "hand"]
    synth = [p for p in phrases if p["source"] == "synth"]
    fr = [p for p in hand if p["langue"] == "fr"]
    en = [p for p in hand if p["langue"] == "en"]
    sortie = {}
    for nom, ps in (("all", phrases), ("hand", hand), ("synth", synth),
                    ("hand_fr", fr), ("hand_en", en)):
        r = evaluer_bloc(nom, fonction, ps)
        sortie[nom] = {"syntagme": r["syntagme"], "tete": r["syntagme"]["tete"],
                       "fraction_semantique": r["fraction_semantique"]}
    return sortie


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--modele", default=str(RACINE / "models/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf"))
    ap.add_argument("--endpoint", default="")
    ap.add_argument("--port", type=int, default=18082)
    ap.add_argument("--demarrer", action="store_true")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--confiance", type=float, default=0.6)
    ap.add_argument("--limite", type=int, default=0)
    ap.add_argument("--sortie", default=str(RACINE / "reports/pensee-gold-syntagmes.json"))
    args = ap.parse_args()

    phrases = charger()
    if args.limite:
        phrases = phrases[:args.limite]
    modele = pathlib.Path(args.modele)
    if not modele.exists():
        raise SystemExit(f"modèle absent : {modele}")
    endpoint = args.endpoint or f"http://127.0.0.1:{args.port}"
    proc = None
    if not _sante(endpoint):
        if not args.demarrer:
            raise SystemExit(f"serveur absent sur {endpoint} — relancer avec --demarrer")
        proc = demarrer_serveur(modele, args.port, pathlib.Path("/tmp/qualifier-syntagmes-serveur.log"))
    else:
        print(f"serveur existant utilisé : {endpoint}")

    tagger = bl.NeuronalLLMChunks(modele, endpoint=endpoint, confiance=args.confiance)
    t0 = time.perf_counter()
    try:
        # Une passe de cache par phrase : les quatre lectures relisent les mêmes annotations.
        with cf.ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
            list(ex.map(lambda p: tagger.analyser(p["texte"], p["langue"]), phrases))
        refus = [p["id"] for p in phrases
                 if tagger.analyser(p["texte"], p["langue"]).refus]
        latences = [float(tagger.analyser(p["texte"], p["langue"]).cout.get("duree_s", 0.0))
                    for p in phrases]
        h = bl.Heuristique()
        mesures = {
            "heuristique": _sources(h, phrases),
            "neuronal": _sources(tagger, phrases),
            "cascade_heuristique": _sources(bl.Cascade(h, tagger), phrases),
            "cascade_confiance": _sources(bl.Cascade(h, tagger, priorite_syntagme="confiance"),
                                          phrases),
        }
        aleatoire = _aleatoire(phrases)
        controles = {
            "vide": {"description": "aucun syntagme (tout O)",
                     "exact": {"f1": 0.0}, "tete": {"f1": 0.0}},
            "aleatoire": {"description": "BIO tiré uniformément (graine 0)",
                          "exact": _score_ensembles(aleatoire, phrases, "exact"),
                          "tete": _score_ensembles(aleatoire, phrases, "tete")},
        }
        seuils = {
            "neuronal_exact_all": mesures["neuronal"]["all"]["syntagme"]["f1"] >= 0.45,
            "neuronal_tete_all": mesures["neuronal"]["all"]["tete"]["f1"] >= 0.70,
            "neuronal_hand_exact": mesures["neuronal"]["hand"]["syntagme"]["f1"] >= 0.40,
            "neuronal_hand_tete": mesures["neuronal"]["hand"]["tete"]["f1"] >= 0.58,
            "neuronal_synth_exact": mesures["neuronal"]["synth"]["syntagme"]["f1"] >= 0.50,
            "neuronal_synth_tete": mesures["neuronal"]["synth"]["tete"]["f1"] >= 0.75,
            "cascade_confiance_tete": (mesures["cascade_confiance"]["all"]["tete"]["f1"]
                                       >= mesures["neuronal"]["all"]["tete"]["f1"] - 0.03),
            "cascade_confiance_exact": (mesures["cascade_confiance"]["all"]["syntagme"]["f1"]
                                        >= mesures["neuronal"]["all"]["syntagme"]["f1"] - 0.03),
            "cascade_sans_regression": (mesures["cascade_heuristique"]["all"]["tete"]["f1"]
                                        >= mesures["heuristique"]["all"]["tete"]["f1"]),
            "aucun_refus": len(refus) == 0,
            "controles_sous_0_20": max(controles["aleatoire"]["exact"]["f1"],
                                       controles["aleatoire"]["tete"]["f1"]) < 0.20,
        }
        resultat = {
            "date": time.strftime("%Y-%m-%d %H:%M %Z"),
            "modele": {"nom": modele.name, "fichiers": _fichiers(modele),
                       "quantisation": "Q4_K_M", "runtime": _version(), "gpu": 0},
            "gold": {"phrases": len(phrases), "tokens": sum(len(p["mots"]) for p in phrases),
                     "hand": sum(1 for p in phrases if p["source"] == "hand"),
                     "synth": sum(1 for p in phrases if p["source"] == "synth")},
            "tagger": {"classe": "NeuronalLLMChunks", "confiance": args.confiance,
                       "tokenisation": "Heuristique._mots (mot/nombre)",
                       "contrainte": "grammaire GBNF BIO, une étiquette par token",
                       "exemples": "5 exemples hors gold"},
            "mesures": mesures,
            "controles": controles,
            "seuils": seuils,
            "verdict": all(seuils.values()),
            "refus": len(refus), "appels": tagger.appels,
            "latence_s": {"moyenne": round(statistics.fmean(latences), 3) if latences else 0.0,
                          "mediane": round(statistics.median(latences), 3) if latences else 0.0},
            "duree_totale_s": round(time.perf_counter() - t0, 1),
            "limites": [
                "Syntagmes seulement : le tagger ne rend ni POS ni pragmatique.",
                "4 segments du gold sont imbriqués (GP dans GV) : BIO ne peut pas les rendre ensemble.",
                "Les 20 réelles ont servi au choix du prompt (dev) ; les 160 synthétiques sont le test.",
                "Le seuil de confiance 0,6 est celui du POS ; la politique `confiance` est une variante.",
                "CPU seulement (GPU de N2 réservés) ; pas de mesure GPU.",
            ],
        }
    finally:
        if proc is not None:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()

    sortie = pathlib.Path(args.sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": resultat["verdict"], "seuils": seuils,
                      "heur": {k: (mesures["heuristique"][k]["syntagme"]["f1"],
                                   mesures["heuristique"][k]["tete"]["f1"])
                               for k in ("all", "hand", "synth")},
                      "neuronal": {k: (mesures["neuronal"][k]["syntagme"]["f1"],
                                       mesures["neuronal"][k]["tete"]["f1"])
                                   for k in ("all", "hand", "synth")},
                      "cascade_h": {k: (mesures["cascade_heuristique"][k]["syntagme"]["f1"],
                                        mesures["cascade_heuristique"][k]["tete"]["f1"])
                                    for k in ("all", "hand", "synth")},
                      "cascade_c": {k: (mesures["cascade_confiance"][k]["syntagme"]["f1"],
                                        mesures["cascade_confiance"][k]["tete"]["f1"])
                                    for k in ("all", "hand", "synth")},
                      "refus": len(refus), "appels": tagger.appels,
                      "latence": resultat["latence_s"]}, ensure_ascii=False, indent=1))
    print(f"écrit : {sortie}")
    return 0 if resultat["verdict"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
