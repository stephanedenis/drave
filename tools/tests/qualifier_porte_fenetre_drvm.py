#!/usr/bin/env python3
"""qualifier_porte_fenetre_drvm.py — la porte **fenêtre** : libre quand t % 3 == 0.

`LABYRINTHE_PORTE_FENETRE` (registre `REGISTRE_PW`) : la porte `(3,3)` n'est libre que lorsque
`t % 3 == 0` ; l'horloge avance à chaque pas, saut ou **attente**. On mesure l'oracle, l'aveugle,
le hasard, le LLM `porte_fenetre` (l'horloge et l'attente dans le prompt) et le LLM `labyrinthe`
(sans l'horloge).

    python3 tools/tests/qualifier_porte_fenetre_drvm.py --endpoint http://127.0.0.1:18082 \
        --sortie reports/pensee-porte-fenetre.json

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
from tools.pensee.moteur import AStar  # noqa: E402
from tools.pensee.operateurs import (DRVM, LABYRINTHE_PORTE_FENETRE, REGISTRE_PW,  # noqa: E402
                                     PolitiqueAveugle, PolitiqueHasard, PolitiqueLLM,
                                     PolitiqueManhattan)
from tools.pensee.store import Budget  # noqa: E402


def _mesure(politique) -> dict:
    t0 = time.perf_counter()
    d = DRVM(REGISTRE_PW, politique)
    d.penser(LABYRINTHE_PORTE_FENETRE, AStar(), Budget(200))
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
    ap.add_argument("--sortie", default=str(RACINE / "reports/pensee-porte-fenetre.json"))
    args = ap.parse_args()
    modele = pathlib.Path(args.modele)
    if not modele.exists():
        raise SystemExit(f"modèle absent : {modele}")
    endpoint = args.endpoint or f"http://127.0.0.1:{args.port}"
    proc = None
    if not _sante(endpoint):
        if not args.demarrer:
            raise SystemExit(f"serveur absent sur {endpoint} — relancer avec --demarrer")
        proc = demarrer_serveur(modele, args.port, pathlib.Path("/tmp/qualifier-porte-fenetre-serveur.log"))
    try:
        llm = PolitiqueLLM(modele, endpoint=endpoint, jeu="porte_fenetre")
        llm_lab = PolitiqueLLM(modele, endpoint=endpoint, jeu="labyrinthe")
        mesures = {
            "oracle": _mesure(PolitiqueManhattan()),
            "aveugle": _mesure(PolitiqueAveugle()),
            "hasard": _mesure(PolitiqueHasard()),
            "llm_porte_fenetre": _mesure(llm),
            "llm_labyrinthe": _mesure(llm_lab),
        }
        l = mesures["llm_porte_fenetre"]
        seuils = {
            "oracle_but": mesures["oracle"]["but"],
            "oracle_sonde": mesures["oracle"]["par_operateur"].get("sonde", 0) > 0,
            "aveugle_non": not mesures["aveugle"]["but"],
            "hasard_non": not mesures["hasard"]["but"],
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
            "probleme": {"nom": "labyrinthe_porte_fenetre", "porte": [3, 3], "but": [4, 4],
                         "regle": "la porte (3,3) n'est libre que si t % 3 == 0 ; l'horloge avance "
                                  "à chaque pas, saut ou attente",
                         "budget": 200},
            "politique": {"classe": "PolitiqueLLM", "jeux": ["porte_fenetre", "labyrinthe"],
                          "contrainte": "grammaire GBNF, quatre directions"},
            "mesures": mesures,
            "seuils": seuils,
            "verdict": all(seuils.values()),
            "limites": [
                "La porte n'est libre qu'à t % 3 == 0 ; l'horloge avance avec le pas, le saut et "
                "l'attente ; l'A* choisit l'attente, le LLM la direction.",
                "Le hasard peut tomber sur t % 3 == 0 ; le contrôle propre est l'aveugle et le "
                "labyrinthe.",
                "L'A* explore ; le nombre de nœuds dépend du tie-breaking ; le but et la sonde "
                "sont les mesures.",
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
                      "mesures": {k: (v["but"], v["noeuds"], v["cout"], v["appels"],
                                      v["par_operateur"].get("sonde", 0),
                                      v["par_operateur"].get("attendre", 0),
                                      v["latence_s"], v["erreurs"]) for k, v in mesures.items()}},
                     ensure_ascii=False, indent=1))
    print(f"écrit : {sortie}")
    return 0 if resultat["verdict"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
