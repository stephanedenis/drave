#!/usr/bin/env python3
"""qualifier_pragmatique.py — qualifie le tagger pragmatique local sur le gold (180 phrases).

Le tagger `NeuronalLLMPragmatique` rend l'acte (`assertion`/`question`/`exclamation`), la
négation, la modalité et le double sens, sous grammaire GBNF. On mesure trois lectures —
**heuristique**, **neuronal seul**, **cascade** — et trois contrôles (majoritaire, hasard,
permutation). Le **double sens** est le point dur : le modèle doit battre 0,8889.

    python3 tools/tests/linguistique/qualifier_pragmatique.py --endpoint http://127.0.0.1:18082 \
        --sortie reports/pensee-gold-pragmatique.json

Le serveur est sur CPU (`-ngl 0`) : les GPU de N2 restent intacts.
"""
from __future__ import annotations

import argparse
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


def _pred_annotation(a: bl.Annotation) -> dict:
    acte = next((e.valeur for e in a.etiquettes
                 if e.niveau == "pragmatique" and e.type == "acte"), "")
    return {
        "acte": acte,
        "negation": any(e.niveau == "phrase" and e.type == "négation" for e in a.etiquettes),
        "modalite": any(e.niveau == "phrase" and e.type == "modalité" for e in a.etiquettes),
        "double_sens": any(e.niveau == "pragmatique" and e.type == "double_sens"
                           for e in a.etiquettes),
    }


def _score(pred: dict[str, dict], phrases: list[dict]) -> dict:
    acte = neg = mod = ds = 0
    for p in phrases:
        g = p["pragma"]
        q = pred[p["id"]]
        acte += int(q["acte"] == g.get("acte", "assertion"))
        neg += int(q["negation"] == bool(g.get("negation", False)))
        mod += int(q["modalite"] == bool(g.get("modalite", False)))
        ds += int(q["double_sens"] == bool(g.get("double_sens", False)))
    n = max(1, len(phrases))
    return {"phrases": len(phrases), "acte": round(acte / n, 4), "negation": round(neg / n, 4),
            "modalite": round(mod / n, 4), "double_sens": round(ds / n, 4)}


def _sources(bloc, phrases: list[dict]) -> dict:
    hand = [p for p in phrases if p["source"] == "hand"]
    synth = [p for p in phrases if p["source"] == "synth"]
    sortie = {}
    for nom, ps in (("all", phrases), ("hand", hand), ("synth", synth)):
        r = evaluer_bloc(nom, bloc, ps)
        sortie[nom] = {"pragmatique": r["pragmatique"],
                       "fraction_semantique": r["fraction_semantique"]}
    return sortie


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--modele", default=str(RACINE / "models/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf"))
    ap.add_argument("--endpoint", default="")
    ap.add_argument("--port", type=int, default=18082)
    ap.add_argument("--demarrer", action="store_true")
    ap.add_argument("--limite", type=int, default=0)
    ap.add_argument("--sortie", default=str(RACINE / "reports/pensee-gold-pragmatique.json"))
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
        proc = demarrer_serveur(modele, args.port, pathlib.Path("/tmp/qualifier-pragmatique-serveur.log"))
    try:
        tagger = bl.NeuronalLLMPragmatique(modele, endpoint=endpoint)
        h = bl.Heuristique()
        t0 = time.perf_counter()
        annotations = {p["id"]: tagger.analyser(p["texte"], p["langue"]) for p in phrases}
        refus = [p["id"] for p in phrases if annotations[p["id"]].refus]
        latences = [float(annotations[p["id"]].cout.get("duree_s", 0.0)) for p in phrases]
        mesures = {"heuristique": _sources(h, phrases),
                   "neuronal": _sources(tagger, phrases),
                   "cascade": _sources(bl.Cascade(h, tagger), phrases)}
        pred_modele = {p["id"]: _pred_annotation(annotations[p["id"]]) for p in phrases}
        majorite = {p["id"]: {"acte": "assertion", "negation": False, "modalite": False,
                              "double_sens": False} for p in phrases}
        rng = random.Random(0)
        hasard = {p["id"]: {"acte": rng.choice(("assertion", "question", "exclamation")),
                            "negation": rng.random() < 0.5, "modalite": rng.random() < 0.5,
                            "double_sens": rng.random() < 0.5} for p in phrases}
        champs = {k: [pred_modele[p["id"]][k] for p in phrases]
                  for k in ("acte", "negation", "modalite", "double_sens")}
        for v in champs.values():
            random.Random(0).shuffle(v)
        permutation = {p["id"]: {k: champs[k][i] for k in champs}
                       for i, p in enumerate(phrases)}
        controles = {
            "majoritaire": {"description": "assertion, sans négation/mod./double sens",
                            **_score(majorite, phrases)},
            "hasard": {"description": "acte uniforme, trois booléens à 0,5 (graine 0)",
                       **_score(hasard, phrases)},
            "permutation": {"description": "les prédictions du modèle sont permutées entre phrases",
                            **_score(permutation, phrases)},
        }
        h_all = mesures["heuristique"]["all"]["pragmatique"]
        n_all = mesures["neuronal"]["all"]["pragmatique"]
        c_all = mesures["cascade"]["all"]["pragmatique"]
        seuils = {
            "acte_modele": n_all["acte"] >= 0.99,
            "negation_modele": n_all["negation"] >= 0.99,
            "modalite_modele": n_all["modalite"] >= 0.99,
            "double_sens_modele": n_all["double_sens"] >= h_all["double_sens"] - 0.001,
            "cascade_acte": c_all["acte"] >= h_all["acte"] - 0.001,
            "cascade_double_sens": c_all["double_sens"] >= h_all["double_sens"] - 0.001,
            "aucun_refus": len(refus) == 0,
            "controles_acte": max(controles[k]["acte"] for k in controles) < 0.80,
        }
        resultat = {
            "date": time.strftime("%Y-%m-%d %H:%M %Z"),
            "modele": {"nom": modele.name, "fichiers": _fichiers(modele),
                       "quantisation": "Q4_K_M", "runtime": _version(), "gpu": 0},
            "gold": {"phrases": len(phrases), "hand": sum(1 for p in phrases if p["source"] == "hand"),
                     "synth": sum(1 for p in phrases if p["source"] == "synth")},
            "tagger": {"classe": "NeuronalLLMPragmatique", "confiance": 0.6,
                       "champs": "acte, négation, modalité, double sens",
                       "actes": list(bl.ACTES)},
            "mesures": mesures,
            "controles": controles,
            "seuils": seuils,
            "verdict": all(seuils.values()),
            "refus": len(refus), "refus_detail": refus[:10],
            "appels": tagger.appels,
            "latence_s": {"moyenne": round(statistics.fmean(latences), 3) if latences else 0.0,
                          "mediane": round(statistics.median(latences), 3) if latences else 0.0},
            "duree_totale_s": round(time.perf_counter() - t0, 1),
            "limites": [
                "Le gold n'a que trois actes (assertion, question, exclamation) ; le prompt suit.",
                "Le double sens est le point dur : les ambiguïtés « prêt à manger » sont manquées.",
                "La modalité a un faux positif connu (« Peux-tu venir ? ») que l'heuristique fait aussi.",
                "Les 20 réelles ont servi au prompt ; les 160 synthétiques sont le test.",
                "CPU seulement (GPU de N2 réservés) ; une seule graine.",
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
                      "heuristique": h_all, "neuronal": n_all, "cascade": c_all,
                      "controles": controles, "refus": len(refus), "appels": tagger.appels,
                      "latence": resultat["latence_s"]}, ensure_ascii=False, indent=1))
    print(f"écrit : {sortie}")
    return 0 if resultat["verdict"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
