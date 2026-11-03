#!/usr/bin/env python3
"""qualifier_porte_sto_graines.py — la porte **stochastique** sur cinq graines.

Le tirage `random.random() < 0.8` de `sonde_p_sto` n'est pas fixé : une seule exécution ne dit
pas si le 7B passe **5/5**. On rejoue `LABYRINTHE_PORTE_STO` avec `random.seed(0..4)` : le LLM
`porte_sto` (le 80 % et le réessai), puis les contrôles (aveugle, labyrinthe, oracle).

    python3 tools/tests/qualifier_porte_sto_graines.py --endpoint http://127.0.0.1:18082 \
        --sortie reports/pensee-porte-sto-graines.json

Le serveur est sur CPU (`-ngl 0`) : les GPU de N2 restent intacts.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import random
import subprocess
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE))
sys.path.insert(0, str(RACINE / "tools/tests/linguistique"))
from qualifier_neuronal import _sante, demarrer_serveur  # noqa: E402
from tools.pensee.moteur import AStar  # noqa: E402
from tools.pensee.operateurs import (DRVM, LABYRINTHE_PORTE_STO, REGISTRE_PSTO,  # noqa: E402
                                     PolitiqueAveugle, PolitiqueLLM, PolitiqueManhattan)
from tools.pensee.store import Budget  # noqa: E402

GRAINES = (0, 1, 2, 3, 4)


def _mesure(politique, graine: int) -> dict:
    random.seed(graine)
    t0 = time.perf_counter()
    d = DRVM(REGISTRE_PSTO, politique)
    d.penser(LABYRINTHE_PORTE_STO, AStar(), Budget(200))
    b = d.instantane()
    b["graine"] = graine
    b["latence_s"] = round(float(getattr(politique, "latence", 0.0)), 3)
    b["erreurs"] = int(getattr(politique, "erreurs", 0))
    b["duree_s"] = round(time.perf_counter() - t0, 3)
    return b


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--modele", default=str(RACINE / "models/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf"))
    ap.add_argument("--endpoint", default="")
    ap.add_argument("--port", type=int, default=18082)
    ap.add_argument("--demarrer", action="store_true")
    ap.add_argument("--sortie", default=str(RACINE / "reports/pensee-porte-sto-graines.json"))
    args = ap.parse_args()
    modele = pathlib.Path(args.modele)
    if not modele.exists():
        raise SystemExit(f"modèle absent : {modele}")
    endpoint = args.endpoint or f"http://127.0.0.1:{args.port}"
    proc = None
    if not _sante(endpoint):
        if not args.demarrer:
            raise SystemExit(f"serveur absent sur {endpoint} — relancer avec --demarrer")
        proc = demarrer_serveur(modele, args.port, pathlib.Path("/tmp/qualifier-porte-sto-graines-serveur.log"))
    try:
        llm = PolitiqueLLM(modele, endpoint=endpoint, jeu="porte_sto")
        llm_lab = PolitiqueLLM(modele, endpoint=endpoint, jeu="labyrinthe")
        llm_runs = [_mesure(llm, g) for g in GRAINES]
        lab_runs = [_mesure(llm_lab, g) for g in (0,)]
        controles = {
            "oracle": _mesure(PolitiqueManhattan(), 0),
            "aveugle": _mesure(PolitiqueAveugle(), 0),
        }
        tout = all(r["but"] for r in llm_runs)
        seuils = {
            "llm_5": tout,
            "labyrinthe_non": not lab_runs[0]["but"],
            "aveugle_non": not controles["aveugle"]["but"],
            "oracle_but": controles["oracle"]["but"],
            "aucune_erreur_llm": all(r["erreurs"] == 0 for r in llm_runs + lab_runs),
            "latence_mesuree": all(r["latence_s"] > 0 for r in llm_runs),
        }
        resultat = {
            "date": time.strftime("%Y-%m-%d %H:%M %Z"),
            "modele": str(modele),
            "endpoint": endpoint,
            "probleme": {"nom": "labyrinthe_porte_sto", "porte": [3, 3], "but": [4, 4],
                         "regle": "depuis (3,2), la sonde ouvre avec 80 % ; en cas d'échec, réessayer",
                         "budget": 200, "graines": list(GRAINES)},
            "politique": {"classe": "PolitiqueLLM", "jeu": "porte_sto"},
            "llm": [{"graine": r["graine"], "but": r["but"], "noeuds": r["noeuds"],
                     "sonde": r["par_operateur"].get("sonde", 0), "appels": r["appels"],
                     "latence_s": r["latence_s"], "erreurs": r["erreurs"]} for r in llm_runs],
            "labyrinthe": [{"graine": r["graine"], "but": r["but"], "noeuds": r["noeuds"],
                            "sonde": r["par_operateur"].get("sonde", 0), "latence_s": r["latence_s"]}
                           for r in lab_runs],
            "controles": {k: {"but": v["but"], "noeuds": v["noeuds"],
                              "sonde": v["par_operateur"].get("sonde", 0)} for k, v in controles.items()},
            "seuils": seuils,
            "verdict": all(seuils.values()),
            "limites": [
                "Cette fois le tirage est fixé (random.seed(0..4)) : le 5/5 est reproductible.",
                "Le labyrinthe (sans la règle) ne passe pas ; l'aveugle non plus ; le hasard n'est "
                "pas rejoué (la chance de la porte 80 % est nommée).",
                "La latence inclut la file du serveur ; CPU seulement ; température 0.",
                "Le 7B peut passer par chance une graine ; le 5/5 et les contrôles sont la mesure.",
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
                      "llm": resultat["llm"], "labyrinthe": resultat["labyrinthe"],
                      "controles": resultat["controles"]}, ensure_ascii=False, indent=1))
    print(f"écrit : {sortie}")
    return 0 if resultat["verdict"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
