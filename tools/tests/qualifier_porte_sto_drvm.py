#!/usr/bin/env python3
"""qualifier_porte_sto_drvm.py — la porte **stochastique** : la sonde ouvre avec 80 %.

`LABYRINTHE_PORTE_STO` (registre `REGISTRE_PSTO`) : depuis `(3,2)`, la sonde ouvre la porte
`(3,3)` avec **80 %** de chance ; en cas d'échec, le pas ne change pas l'état (il faut réessayer).
On mesure l'oracle, l'aveugle, le hasard, le LLM `porte_sto` (le 80 % et le réessai dans le
prompt), le LLM `labyrinthe` (sans la porte) et la Q-table `PolitiqueAppriseOuverte` (T33).

    python3 tools/tests/qualifier_porte_sto_drvm.py --endpoint http://127.0.0.1:18082 \
        --sortie reports/pensee-porte-sto.json

Le serveur est sur CPU (`-ngl 0`) : les GPU de N2 restent intacts.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE))
sys.path.insert(0, str(RACINE / "tools/tests/linguistique"))
from qualifier_neuronal import _sante, demarrer_serveur  # noqa: E402
from tools.pensee.courbe import seule_sto  # noqa: E402
from tools.pensee.moteur import AStar  # noqa: E402
from tools.pensee.operateurs import (DRVM, LABYRINTHE_PORTE_STO, REGISTRE_PSTO,  # noqa: E402
                                     PolitiqueAppriseOuverte, PolitiqueAveugle,
                                     PolitiqueHasard, PolitiqueLLM, PolitiqueManhattan)
from tools.pensee.store import Budget  # noqa: E402


def _mesure(politique) -> dict:
    t0 = time.perf_counter()
    d = DRVM(REGISTRE_PSTO, politique)
    d.penser(LABYRINTHE_PORTE_STO, AStar(), Budget(200))
    b = d.instantane()
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
    ap.add_argument("--sortie", default=str(RACINE / "reports/pensee-porte-sto.json"))
    args = ap.parse_args()
    modele = pathlib.Path(args.modele)
    if not modele.exists():
        raise SystemExit(f"modèle absent : {modele}")
    endpoint = args.endpoint or f"http://127.0.0.1:{args.port}"
    proc = None
    if not _sante(endpoint):
        if not args.demarrer:
            raise SystemExit(f"serveur absent sur {endpoint} — relancer avec --demarrer")
        proc = demarrer_serveur(modele, args.port, pathlib.Path("/tmp/qualifier-porte-sto-serveur.log"))
    try:
        apprendre = PolitiqueAppriseOuverte(episodes=1000, graine=0)
        apprendre.apprendre()
        ok_seule, pas_seule, essais_seule = seule_sto(apprendre, graine=0, p_ouvre=0.8)
        llm = PolitiqueLLM(modele, endpoint=endpoint, jeu="porte_sto")
        llm_lab = PolitiqueLLM(modele, endpoint=endpoint, jeu="labyrinthe")
        mesures = {
            "oracle": _mesure(PolitiqueManhattan()),
            "aveugle": _mesure(PolitiqueAveugle()),
            "hasard": _mesure(PolitiqueHasard()),
            "llm_porte_sto": _mesure(llm),
            "llm_labyrinthe": _mesure(llm_lab),
        }
        l = mesures["llm_porte_sto"]
        seuils = {
            "oracle_but": mesures["oracle"]["but"],
            "oracle_sonde": mesures["oracle"]["par_operateur"].get("sonde", 0) > 0,
            "aveugle_non": not mesures["aveugle"]["but"],
            "hasard_non": not mesures["hasard"]["but"],
            "apprise_but": ok_seule,
            "llm_but": l["but"],
            "llm_sonde": l["par_operateur"].get("sonde", 0) > 0,
            "labyrinthe_non": not mesures["llm_labyrinthe"]["but"],
            "aucune_erreur_llm": l["erreurs"] == 0 and mesures["llm_labyrinthe"]["erreurs"] == 0,
            "latence_mesuree": l["latence_s"] > 0,
        }
        resultat = {
            "date": time.strftime("%Y-%m-%d %H:%M %Z"),
            "modele": str(modele),
            "endpoint": endpoint,
            "probleme": {"nom": "labyrinthe_porte_sto", "porte": [3, 3], "but": [4, 4],
                         "regle": "depuis (3,2), la sonde ouvre avec 80 % ; en cas d'échec, réessayer",
                         "budget": 200},
            "politique": {"classe": "PolitiqueLLM", "jeux": ["porte_sto", "labyrinthe"],
                          "contrainte": "grammaire GBNF, quatre directions"},
            "apprise": {"classe": "PolitiqueAppriseOuverte", "episodes": 1000,
                        "etats_q": len(apprendre.q), "seule_but": ok_seule,
                        "seule_pas": pas_seule, "essais": essais_seule},
            "mesures": mesures,
            "seuils": seuils,
            "verdict": all(seuils.values()),
            "limites": [
                "La porte s'ouvre à 80 % ; le hasard/la chance peut passer un essai ; le contrôle "
                "propre est l'aveugle et le labyrinthe.",
                "La Q-table `PolitiqueAppriseOuverte` (T33, 1000 épisodes) est la référence sans A* ; "
                "elle est mesurée à 80 %.",
                "L'A* explore et réessaie ; le nombre de nœuds dépend du tirage aléatoire.",
                "La latence inclut la file du serveur ; CPU seulement ; une graine, température 0.",
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
                      "apprise": resultat["apprise"],
                      "mesures": {k: (v["but"], v["noeuds"], v["cout"], v["appels"],
                                      v["par_operateur"].get("sonde", 0), v["latence_s"],
                                      v["erreurs"]) for k, v in mesures.items()}},
                     ensure_ascii=False, indent=1))
    print(f"écrit : {sortie}")
    return 0 if resultat["verdict"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
