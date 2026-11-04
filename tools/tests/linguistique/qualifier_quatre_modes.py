#!/usr/bin/env python3
"""qualifier_quatre_modes.py — la porte des quatre modes du contrat de L sur le gold 432.

Les quatre modes du contrat (`docs/theorie/contrat-bloc-langue.md`) mesurés sur le
**même** gold réel 432 :

  1. heuristique seule ;
  2. neuronal seul (le composite POS + syntagmes, via l'API DeepSeek — règle 11) ;
  3. parallèle (`Parallele`) ;
  4. cascade (`Cascade`, seuil 0,6).

Mêmes mesures que la cascade : POS, syntagmes F1, tête F1, acte, fraction, refus.
Le coût est mesuré : appels du tagger, tokens API, latence, durée.

Usage :
    DEEPSEEK_KEY_FILE=~/.config/drave/deepseek.key \
    python3 tools/tests/linguistique/qualifier_quatre_modes.py --limite 3
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE))

from tools.bloc_linguistique import (PRIORITE_NIVEAU, Cascade, Heuristique,
                                     NeuronalLLMChunks, NeuronalLLMCompose,
                                     NeuronalLLMPOS, NeuronalLLMPragmatique, Parallele)
from tools.llm.deepseek import DeepSeek
from tools.tests.linguistique.evaluer_gold import evaluer_bloc
from tools.tests.linguistique.qualifier_cascade import _sources, charger


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limite", type=int, default=0)
    ap.add_argument("--gold-reel", action="store_true", default=True)
    ap.add_argument("--sortie", default=str(RACINE / "reports/pensee-quatre-modes.json"))
    ap.add_argument("--seuil", type=float, default=0.6)
    ap.add_argument("--temperature", type=float, default=0.0)
    a = ap.parse_args()
    phrases = charger(a.gold_reel)
    if a.limite:
        phrases = phrases[: a.limite]
    client = DeepSeek()
    if not client.disponible():
        raise SystemExit("clé DeepSeek absente : exporter DEEPSEEK_KEY_FILE")
    usage = {"appels": 0, "tokens": 0, "latence_s": 0.0}

    def transport(invite: str, grammaire: str, max_jetons: int) -> str:
        r = client.demande(invite, temperature=a.temperature, max_tokens=max(64, int(max_jetons or 256)))
        usage["appels"] += 1
        u = r.usage if isinstance(r.usage, dict) else {}
        usage["tokens"] += int(u.get("total_tokens", 0) or 0)
        usage["latence_s"] += float(r.latence_s or 0.0)
        return r.contenu

    h = Heuristique()
    pos = NeuronalLLMPOS("deepseek-chat", transport=transport)
    chunks = NeuronalLLMChunks("deepseek-chat", transport=transport)
    pragma = NeuronalLLMPragmatique("deepseek-chat", transport=transport)
    compose = NeuronalLLMCompose(pos, chunks, pragma)
    modes = {
        "heuristique": h,
        "neuronal": compose,
        "parallele": Parallele([h, compose], priorite_syntagme="confiance"),
        "cascade": Cascade(h, compose, seuil=a.seuil, priorite_syntagme="confiance"),
        "parallele_niveau": Parallele([h, compose], priorite_syntagme="confiance",
                                      priorite_par_niveau=PRIORITE_NIVEAU),
        "cascade_niveau": Cascade(h, compose, seuil=a.seuil, priorite_syntagme="confiance",
                                  priorite_par_niveau=PRIORITE_NIVEAU),
    }
    t0 = time.perf_counter()
    mesures = {}
    for nom, bloc in modes.items():
        t1 = time.perf_counter()
        mesures[nom] = _sources(bloc, phrases)
        mesures[nom]["duree_s"] = round(time.perf_counter() - t1, 2)
        print(nom, "·", round(time.perf_counter() - t1, 1), "s", flush=True)
    refus = [p["id"] for p in phrases if compose.analyser(p["texte"], p["langue"]).refus]
    latences = [float(compose.analyser(p["texte"], p["langue"]).cout.get("duree_s", 0.0))
                for p in phrases]
    seuils = {
        "heuristique": True,
        "neuronal": all(mesures["neuronal"]["all"]["pos"]["exactitude"] > 0 for _ in [0]),
        # le parallèle (confiance) ne peut pas battre le max : il doit tenir l'heuristique
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
    }
    resultat = {
        "date": time.strftime("%Y-%m-%d %H:%M %Z"),
        "gold": {"phrases": len(phrases),
                 "tokens": sum(len(p["mots"]) for p in phrases),
                 "modalite": "api-deepseek (deepseek-chat), aucun serveur local"},
        "modes": mesures,
        "seuils": seuils,
        "refus": len(refus), "refus_detail": refus[:10],
        "appels": {"pos": pos.appels, "syntagmes": chunks.appels},
        "api": usage,
        "latence_s": {"moyenne": round(statistics.fmean(latences), 3) if latences else 0.0,
                      "mediane": round(statistics.median(latences), 3) if latences else 0.0},
        "duree_totale_s": round(time.perf_counter() - t0, 1),
        "limites": [
            "le neuronal passe par l'API DeepSeek (règle 11) ; aucun GPU, aucun serveur local",
            "le gold réel 432 n'a pas de source hand/synth : la ventilation hand/synth est vide",
            "la pragmatique reste à l'heuristique dans tous les modes",
        ],
    }
    p = pathlib.Path(a.sortie)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(resultat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for nom, m in mesures.items():
        print(nom, {k: m["all"][k]["exactitude"] if k == "pos" else
                    (m["all"]["syntagme"]["f1"] if k == "syntagme" else
                     (m["all"]["tete"]["f1"] if k == "tete" else m["all"][k]))
                    for k in ("pos", "syntagme", "tete", "pragmatique", "fraction_semantique")})


if __name__ == "__main__":
    main()
