#!/usr/bin/env python3
"""qualifier_porte_drvm.py — la porte DRVM avec sa règle **dans le prompt**.

L'ancien prompt du labyrinthe ne décrivait pas la porte : le 7B échouait (200 nœuds, 3 appels,
sans but). Ici la politique `jeu="porte"` reçoit les murs du labyrinthe-porte, la porte `(3,3)`
et la règle « depuis (3,2), la sonde ouvre la porte si tu réponds bas ». On mesure l'oracle,
l'aveugle, le hasard et le LLM sur le même `DRVM` (budget 200, A*).

    python3 tools/tests/qualifier_porte_drvm.py --endpoint http://127.0.0.1:18082 \
        --sortie reports/pensee-porte-llm.json

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
from tools.pensee.operateurs import (DRVM, LABYRINTHE_PORTE, P_BUT, REGISTRE_P,  # noqa: E402
                                     PolitiqueAveugle, PolitiqueHasard, PolitiqueLLM,
                                     PolitiqueManhattan)
from tools.pensee.store import Budget  # noqa: E402


def _mesure(politique) -> dict:
    t0 = time.perf_counter()
    d = DRVM(REGISTRE_P, politique)
    d.penser(LABYRINTHE_PORTE, AStar(), Budget(200))
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
    ap.add_argument("--sortie", default=str(RACINE / "reports/pensee-porte-llm.json"))
    args = ap.parse_args()
    modele = pathlib.Path(args.modele)
    if not modele.exists():
        raise SystemExit(f"modèle absent : {modele}")
    endpoint = args.endpoint or f"http://127.0.0.1:{args.port}"
    proc = None
    if not _sante(endpoint):
        if not args.demarrer:
            raise SystemExit(f"serveur absent sur {endpoint} — relancer avec --demarrer")
        proc = demarrer_serveur(modele, args.port, pathlib.Path("/tmp/qualifier-porte-serveur.log"))
    try:
        llm = PolitiqueLLM(modele, endpoint=endpoint, jeu="porte")
        mesures = {
            "oracle": _mesure(PolitiqueManhattan()),
            "aveugle": _mesure(PolitiqueAveugle()),
            "hasard": _mesure(PolitiqueHasard()),
            "llm": _mesure(llm),
        }
        l = mesures["llm"]
        seuils = {
            "oracle_but": mesures["oracle"]["but"],
            "aveugle_non": not mesures["aveugle"]["but"],
            "llm_sonde": l["par_operateur"].get("sonde", 0) > 0,
            "aucune_erreur_llm": l["erreurs"] == 0,
            "latence_mesuree": l["latence_s"] > 0,
        }
        resultat = {
            "date": time.strftime("%Y-%m-%d %H:%M %Z"),
            "modele": str(modele),
            "endpoint": endpoint,
            "probleme": {"nom": "labyrinthe_porte", "porte": [3, 3], "but": [4, 4],
                         "regle": "depuis (3,2), la sonde ouvre la porte si la politique dit bas",
                         "budget": 200},
            "politique": {"classe": "PolitiqueLLM", "jeu": "porte",
                          "contrainte": "grammaire GBNF, quatre directions"},
            "mesures": mesures,
            "seuils": seuils,
            "verdict": all(seuils.values()),
            "limites": [
                "Le hasard ouvre la porte par chance ; l'aveugle échoue : le contrôle propre est l'aveugle.",
                "L'ancien prompt (sans la règle de la porte) a donné 200 nœuds, 3 appels, 179,5 s, "
                "sans but (fiche DRVM/native) : c'est le contrôle négatif du prompt.",
                "La latence inclut la file du serveur ; CPU seulement.",
                "Une seule graine de serveur, température 0, grammaire.",
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
                                      v["par_operateur"].get("sonde", 0), v["latence_s"],
                                      v["erreurs"]) for k, v in mesures.items()}},
                     ensure_ascii=False, indent=1))
    print(f"écrit : {sortie}")
    return 0 if resultat["verdict"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
