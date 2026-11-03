#!/usr/bin/env python3
"""qualifier_cascade.py — la cascade **complète** avec le vrai modèle (POS + syntagmes).

Le bloc neuronal est `NeuronalLLMCompose` : `NeuronalLLMPOS` + `NeuronalLLMChunks`, appelés
une fois par phrase, réunis en une annotation. La cascade garde l'heuristique pour la
pragmatique (acte 1,0 sur le gold) et applique la politique `confiance` au syntagme.

On mesure six lectures : heuristique, neuronal composite, cascade POS seule, cascade
syntagmes seule, cascade complète (confiance), cascade complète (priorité heuristique). Les
quatre dernières sont les **ablations** : la complète doit valoir les parties, sans perte.

    python3 tools/tests/linguistique/qualifier_cascade.py --endpoint http://127.0.0.1:18082 \
        --workers 1 --sortie reports/pensee-gold-cascade.json

Le serveur est sur CPU (`-ngl 0`) : les GPU de N2 restent intacts.
"""
from __future__ import annotations

import argparse
import json
import pathlib
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


GOLD_REEL = pathlib.Path(__file__).with_name("gold_reel.json")


def charger(reel: bool = False) -> list[dict]:
    if reel:
        ph = json.loads(GOLD_REEL.read_text(encoding="utf-8"))["phrases"]
        for p in ph:
            p["source"] = "reel"
        return ph
    hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
    synth = json.loads(SYNTH.read_text(encoding="utf-8"))["phrases"]
    for p in hand:
        p["source"] = "hand"
    for p in synth:
        p["source"] = "synth"
    return hand + synth


def _lecture(nom: str, bloc, phrases: list[dict]) -> dict:
    r = evaluer_bloc(nom, bloc, phrases)
    return {"pos": r["pos"], "syntagme": r["syntagme"], "tete": r["syntagme"]["tete"],
            "pragmatique": r["pragmatique"], "fraction_semantique": r["fraction_semantique"]}


def _sources(bloc, phrases: list[dict]) -> dict:
    hand = [p for p in phrases if p["source"] == "hand"]
    synth = [p for p in phrases if p["source"] == "synth"]
    return {nom: _lecture(nom, bloc, ps)
            for nom, ps in (("all", phrases), ("hand", hand), ("synth", synth))}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--modele", default=str(RACINE / "models/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf"))
    ap.add_argument("--endpoint", default="")
    ap.add_argument("--port", type=int, default=18082)
    ap.add_argument("--demarrer", action="store_true")
    ap.add_argument("--confiance", type=float, default=0.6)
    ap.add_argument("--limite", type=int, default=0)
    ap.add_argument("--gold-reel", action="store_true",
                    help="charger gold_reel.json (432 phrases réelles)")
    ap.add_argument("--sortie", default=str(RACINE / "reports/pensee-gold-cascade.json"))
    args = ap.parse_args()

    phrases = charger(args.gold_reel)
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
        proc = demarrer_serveur(modele, args.port, pathlib.Path("/tmp/qualifier-cascade-serveur.log"))

    pos = bl.NeuronalLLMPOS(modele, endpoint=endpoint, confiance=args.confiance)
    chunks = bl.NeuronalLLMChunks(modele, endpoint=endpoint, confiance=args.confiance)
    compose = bl.NeuronalLLMCompose(pos, chunks)
    h = bl.Heuristique()
    t0 = time.perf_counter()
    try:
        # Le composite d'abord : il remplit les deux caches ; les ablations relisent.
        mesures = {"neuronal": _sources(compose, phrases)}
        mesures["heuristique"] = _sources(h, phrases)
        mesures["cascade_pos"] = _sources(bl.Cascade(h, pos), phrases)
        mesures["cascade_syntagmes"] = _sources(
            bl.Cascade(h, chunks, priorite_syntagme="confiance"), phrases)
        mesures["cascade_complete"] = _sources(
            bl.Cascade(h, compose, priorite_syntagme="confiance"), phrases)
        mesures["cascade_complete_defaut"] = _sources(bl.Cascade(h, compose), phrases)
        refus = [p["id"] for p in phrases
                 if compose.analyser(p["texte"], p["langue"]).refus]
        latences = [float(compose.analyser(p["texte"], p["langue"]).cout.get("duree_s", 0.0))
                    for p in phrases]
        complete = mesures["cascade_complete"]["all"]
        pos_seul = mesures["cascade_pos"]["all"]
        synt_seul = mesures["cascade_syntagmes"]["all"]
        defaut = mesures["cascade_complete_defaut"]["all"]
        # Seuils : le gold 180 (hand+synth) et le gold réel n'ont pas le même plancher.
        # Le gold réel 432 est le corpus de généralisation ; ses seuils sont ceux du 432,
        # mesurés une fois puis figés ici (il ne s'agit pas de les baisser pour passer).
        if args.gold_reel:
            s_pos, s_synt, s_tete, s_frac = 0.90, 0.45, 0.55, 0.50
        else:
            s_pos, s_synt, s_tete, s_frac = 0.94, 0.60, 0.75, 0.60
        seuils = {
            "pos_all": complete["pos"]["exactitude"] >= s_pos,
            "syntagme_exact_all": complete["syntagme"]["f1"] >= s_synt,
            "syntagme_tete_all": complete["tete"]["f1"] >= s_tete,
            "acte": complete["pragmatique"]["acte"] >= 0.99,
            "fraction": complete["fraction_semantique"] >= s_frac,
            "ablation_pos": complete["pos"]["exactitude"] >= pos_seul["pos"]["exactitude"] - 0.001,
            "ablation_syntagmes": complete["tete"]["f1"] >= synt_seul["tete"]["f1"] - 0.001,
            "policy": complete["tete"]["f1"] > defaut["tete"]["f1"],
            "aucun_refus": len(refus) == 0,
        }
        resultat = {
            "date": time.strftime("%Y-%m-%d %H:%M %Z"),
            "modele": {"nom": modele.name, "fichiers": _fichiers(modele),
                       "quantisation": "Q4_K_M", "runtime": _version(), "gpu": 0},
            "gold": {"phrases": len(phrases), "tokens": sum(len(p["mots"]) for p in phrases),
                     "hand": sum(1 for p in phrases if p.get("source") == "hand"),
                     "synth": sum(1 for p in phrases if p.get("source") == "synth")},
            "bloc": {"classe": "NeuronalLLMCompose",
                     "pos": "NeuronalLLMPOS", "syntagmes": "NeuronalLLMChunks",
                     "confiance": args.confiance, "politique": "confiance",
                     "pragmatique": "heuristique"},
            "mesures": mesures,
            "seuils": seuils,
            "verdict": all(seuils.values()),
            "refus": len(refus), "refus_detail": refus[:10],
            "appels": {"pos": pos.appels, "syntagmes": chunks.appels},
            "latence_s": {"moyenne": round(statistics.fmean(latences), 3) if latences else 0.0,
                          "mediane": round(statistics.median(latences), 3) if latences else 0.0},
            "duree_totale_s": round(time.perf_counter() - t0, 1),
            "limites": [
                "La pragmatique reste à l'heuristique : le composite ne rend que POS et syntagmes.",
                "2 appels HTTP par phrase (POS + syntagmes) ; le cache sert les ablations.",
                "Les 20 réelles ont servi au choix des prompts ; les 160 synthétiques sont le test.",
                "CPU seulement (GPU de N2 réservés) ; pas de mesure GPU.",
                "Seuils : 0,94/0,60/0,75/0,60 sur le gold 180 ; 0,90/0,45/0,55/0,50 sur le gold réel 432.",
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
                      "heur": {k: (mesures["heuristique"][k]["pos"]["exactitude"],
                                   mesures["heuristique"][k]["tete"]["f1"])
                               for k in ("all", "hand", "synth")},
                      "neuronal": {k: (mesures["neuronal"][k]["pos"]["exactitude"],
                                       mesures["neuronal"][k]["tete"]["f1"])
                                   for k in ("all", "hand", "synth")},
                      "cascade_complete": {k: (mesures["cascade_complete"][k]["pos"]["exactitude"],
                                               mesures["cascade_complete"][k]["syntagme"]["f1"],
                                               mesures["cascade_complete"][k]["tete"]["f1"],
                                               mesures["cascade_complete"][k]["pragmatique"]["acte"])
                                           for k in ("all", "hand", "synth")},
                      "defaut": {k: (mesures["cascade_complete_defaut"][k]["tete"]["f1"])
                                 for k in ("all", "hand", "synth")},
                      "refus": len(refus), "appels": resultat["appels"],
                      "latence": resultat["latence_s"]}, ensure_ascii=False, indent=1))
    print(f"écrit : {sortie}")
    return 0 if resultat["verdict"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
