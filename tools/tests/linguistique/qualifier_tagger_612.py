#!/usr/bin/env python3
"""qualifier_tagger_612.py — le tagger POS API sur le gold 612 (hand 20 + reel 432 + synth 160).

POURQUOI. Le banc `qualifier_quatre_modes.py` ne charge que `gold_reel.json` (432 phrases) ; le
gold courant en compte 612, et le tagger n'y a jamais été mesuré. Ce banc ajoute la ventilation
hand / reel / synth, la latence réelle des appels et le modèle effectivement renvoyé par l'API.
Il ne modifie aucun autre fichier et n'écrit que le JSON demandé.

COÛT. Deux appels par phrase (POS + syntagmes), partagés par les six modes grâce au cache des
tagger : ~1 214 appels, ~360 k tokens, ~20 min pour 612 phrases.

USAGE.
    DEEPSEEK_KEY_FILE=$HOME/.config/drave/deepseek.key \
    DEEPSEEK_CACHE=$(mktemp -d /tmp/j43-cache.XXXX) \
    DEEPSEEK_MODEL=deepseek-chat \
    PYTHONPATH=. python3 tools/tests/linguistique/qualifier_tagger_612.py \
      --sortie /tmp/tagger-612.json

La clé n'est jamais lue en dur : `tools/llm/deepseek.py` lit `DEEPSEEK_API_KEY` ou le fichier
`DEEPSEEK_KEY_FILE` (0600). Le cache doit être neuf : le cache par défaut contient les réponses
du 2026-11-04 et rejouerait l'ancien modèle au lieu de mesurer celui d'aujourd'hui.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys
import time
from collections import Counter

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE))
sys.path.insert(0, str(RACINE / "tools/tests/linguistique"))

from tools.bloc_linguistique import (PRIORITE_NIVEAU, PRIORITE_TYPE, Cascade, Heuristique,
                                     NeuronalLLMChunks, NeuronalLLMCompose,
                                     NeuronalLLMPOS, Parallele)
from tools.llm.deepseek import DeepSeek
from tools.tests.linguistique.evaluer_gold import evaluer_bloc

GOLD = RACINE / "tools/tests/linguistique/gold.json"
REEL = RACINE / "tools/tests/linguistique/gold_reel.json"
SYNTH = RACINE / "tools/tests/linguistique/gold_synthetique.json"


def charger_612() -> list[dict]:
    """Les 612 phrases, chacune étiquetée par sa source : hand, reel ou synth."""
    phrases = []
    for chemin, source in ((GOLD, "hand"), (REEL, "reel"), (SYNTH, "synth")):
        for p in json.loads(chemin.read_text(encoding="utf-8"))["phrases"]:
            p = dict(p)
            p["source"] = source
            phrases.append(p)
    return phrases


def _lecture(bloc, phrases: list[dict]) -> dict:
    r = evaluer_bloc("x", bloc, phrases)
    return {"pos": r["pos"], "syntagme": r["syntagme"], "tete": r["syntagme"]["tete"],
            "pragmatique": r["pragmatique"], "fraction_semantique": r["fraction_semantique"]}


def _sources(bloc, phrases: list[dict]) -> dict:
    """Le tout + chaque source ; une source vide est omise (utile avec --limite)."""
    subsets = {"all": phrases}
    for source in ("hand", "reel", "synth"):
        subsets[source] = [p for p in phrases if p["source"] == source]
    return {nom: _lecture(bloc, ps) for nom, ps in subsets.items() if ps}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--limite", type=int, default=0, help="ne mesurer que les N premières phrases")
    ap.add_argument("--sortie", default="/tmp/tagger-612.json")
    ap.add_argument("--seuil", type=float, default=0.6)
    a = ap.parse_args()
    phrases = charger_612()
    if a.limite:
        phrases = phrases[: a.limite]
    print("phrases", len(phrases), "tokens", sum(len(p["mots"]) for p in phrases), flush=True)
    print("sources", Counter(p["source"] for p in phrases), flush=True)

    client = DeepSeek()
    if not client.disponible():
        raise SystemExit("clé DeepSeek absente : exporter DEEPSEEK_KEY_FILE")
    usage = {"appels": 0, "tokens": 0, "latence_s": 0.0}
    latences: list[float] = []
    modeles: Counter = Counter()

    def transport(invite: str, grammaire: str, max_jetons: int) -> str:
        r = client.demande(invite, temperature=0.0,
                           max_tokens=max(64, int(max_jetons or 256)))
        usage["appels"] += 1
        u = r.usage if isinstance(r.usage, dict) else {}
        usage["tokens"] += int(u.get("total_tokens", 0) or 0)
        usage["latence_s"] += float(r.latence_s or 0.0)
        latences.append(float(r.latence_s or 0.0))
        modeles[r.modele] += 1
        return r.contenu

    h = Heuristique()
    pos = NeuronalLLMPOS("deepseek-chat", transport=transport)
    chunks = NeuronalLLMChunks("deepseek-chat", transport=transport)
    compose = NeuronalLLMCompose(pos, chunks)  # sans pragmatique : la décision est POS
    modes = {
        "heuristique": h,
        "neuronal": compose,
        "parallele": Parallele([h, compose], priorite_syntagme="confiance"),
        "cascade": Cascade(h, compose, seuil=a.seuil, priorite_syntagme="confiance"),
        "parallele_niveau": Parallele([h, compose], priorite_syntagme="confiance",
                                      priorite_par_niveau=PRIORITE_NIVEAU,
                                      priorite_par_type=PRIORITE_TYPE),
        "cascade_niveau": Cascade(h, compose, seuil=a.seuil, priorite_syntagme="confiance",
                                  priorite_par_niveau=PRIORITE_NIVEAU,
                                  priorite_par_type=PRIORITE_TYPE),
    }
    t0 = time.perf_counter()
    mesures = {}
    for nom, bloc in modes.items():
        t1 = time.perf_counter()
        mesures[nom] = _sources(bloc, phrases)
        mesures[nom]["duree_s"] = round(time.perf_counter() - t1, 2)
        print(nom, "·", mesures[nom]["duree_s"], "s",
              "POS all", mesures[nom]["all"]["pos"]["exactitude"], flush=True)

    refus = []
    for p in phrases:
        ann = compose.analyser(p["texte"], p["langue"])
        if ann.refus:
            refus.append(p["id"])

    pos_par_source = {nom: {s: m[s]["pos"]["exactitude"] for s in m if s != "duree_s"}
                      for nom, m in mesures.items()}
    resultat = {
        "date": time.strftime("%Y-%m-%d %H:%M %Z"),
        "gold": {"phrases": len(phrases),
                 "tokens": sum(len(p["mots"]) for p in phrases),
                 "sources": dict(Counter(p["source"] for p in phrases)),
                 "modalite": "api-deepseek (deepseek-chat → modèle renvoyé), aucun serveur local"},
        "modeles_renvoyes": dict(modeles),
        "modes": mesures,
        "pos_par_source": pos_par_source,
        "seuils": {
            "heuristique": True,
            "neuronal": all(mesures["neuronal"]["all"]["pos"]["exactitude"] > 0 for _ in [0]),
            "parallele": mesures["parallele"]["all"]["pos"]["exactitude"]
                         >= mesures["heuristique"]["all"]["pos"]["exactitude"] - 0.001,
            "cascade": mesures["cascade"]["all"]["pos"]["exactitude"]
                       >= mesures["heuristique"]["all"]["pos"]["exactitude"] - 0.001,
            "parallele_niveau": mesures["parallele_niveau"]["all"]["pos"]["exactitude"]
                                >= max(mesures["heuristique"]["all"]["pos"]["exactitude"],
                                       mesures["neuronal"]["all"]["pos"]["exactitude"]) - 0.001,
            "cascade_niveau": mesures["cascade_niveau"]["all"]["pos"]["exactitude"]
                              >= mesures["neuronal"]["all"]["pos"]["exactitude"] - 0.001,
            "aucun_refus": len(refus) == 0,
        },
        "refus": len(refus), "refus_detail": refus[:10],
        "appels": {"pos": pos.appels, "syntagmes": chunks.appels},
        "api": usage,
        "latence_s": {"moyenne": round(statistics.fmean(latences), 3) if latences else 0.0,
                      "mediane": round(statistics.median(latences), 3) if latences else 0.0},
        "duree_totale_s": round(time.perf_counter() - t0, 1),
        "limites": [
            "mesure exécutée hors dépôt, sur une copie de travail : aucun code existant modifié",
            "le modèle demandé est deepseek-chat ; le modèle renvoyé est consigné",
            "le cache DeepSeek est neuf : aucun rejeu des réponses du 2026-11-04",
            "la pragmatique reste à l'heuristique (non appelée) ; la décision porte sur le POS",
        ],
    }
    pathlib.Path(a.sortie).write_text(json.dumps(resultat, ensure_ascii=False, indent=2) + "\n",
                                      encoding="utf-8")
    print(json.dumps({"pos_par_source": pos_par_source, "appels": usage["appels"],
                      "tokens": usage["tokens"], "refus": len(refus),
                      "latence_moyenne": resultat["latence_s"]["moyenne"]},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
