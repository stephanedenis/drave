#!/usr/bin/env python3
"""qualifier_politique_drvm.py — la politique **DRVM/native** : un vrai modèle dans le DRVM.

Le conteneur `DRVM` exécute les problèmes de B13 (cadenas linéaire, labyrinthe 5×5, porte) avec
quatre politiques : l'**oracle** (Manhattan/Cadenas), le **contrôle négatif** (aveugle), le
**hasard** (graine 0) et le **modèle local** (`PolitiqueLLM`, Qwen2.5-7B-Instruct, grammaire
GBNF). On mesure le but, les nœuds, le coût du registre, les appels et la **latence réelle**.

    python3 tools/tests/qualifier_politique_drvm.py --endpoint http://127.0.0.1:18082 \
        --sortie reports/pensee-politique-llm.json

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
from tools.pensee.operateurs import (BUT_C, CADENAS, DRVM, LABYRINTHE,  # noqa: E402
                                     LABYRINTHE_PORTE, L_BUT, PolitiqueAveugle,
                                     PolitiqueCadenas, PolitiqueCadenasAveugle,
                                     PolitiqueHasard, PolitiqueLLM, PolitiqueManhattan,
                                     REGISTRE_CADENAS, REGISTRE_L, REGISTRE_P)
from tools.pensee.store import Budget  # noqa: E402


def _mesure(probleme, registre, politique, budget: int) -> dict:
    t0 = time.perf_counter()
    d = DRVM(registre, politique)
    d.penser(probleme, AStar(), Budget(budget))
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
    ap.add_argument("--sortie", default=str(RACINE / "reports/pensee-politique-llm.json"))
    args = ap.parse_args()
    endpoint = args.endpoint or f"http://127.0.0.1:{args.port}"
    est_api = not endpoint.startswith(("http://127.0.0.1", "http://localhost"))
    modele = args.modele if est_api else pathlib.Path(args.modele)
    if not est_api and not modele.exists():
        raise SystemExit(f"modèle absent : {modele}")
    proc = None
    if not est_api and not _sante(endpoint):
        if not args.demarrer:
            raise SystemExit(f"serveur absent sur {endpoint} — relancer avec --demarrer")
        proc = demarrer_serveur(modele, args.port, pathlib.Path("/tmp/qualifier-drvm-serveur.log"))
    try:
        mesures = {}
        cadenas = (
            ("oracle", PolitiqueCadenas()),
            ("aveugle", PolitiqueCadenasAveugle()),
            ("hasard", PolitiqueHasard(("avant", "arriere"))),
            ("minimal", PolitiqueLLM(modele, endpoint=endpoint, jeu="cadenas", variante="minimal")),
            ("regle", PolitiqueLLM(modele, endpoint=endpoint, jeu="cadenas", variante="regle")),
        )
        mesures["cadenas"] = {nom: _mesure(CADENAS, REGISTRE_CADENAS, politique, 20)
                              for nom, politique in cadenas}
        for nom, probleme, registre, budget, oracle, negatif, hasard in (
            ("labyrinthe", LABYRINTHE, REGISTRE_L, 160,
             PolitiqueManhattan(), PolitiqueAveugle(), PolitiqueHasard()),
            ("porte", LABYRINTHE_PORTE, REGISTRE_P, 200,
             PolitiqueManhattan(), PolitiqueAveugle(), PolitiqueHasard()),
        ):
            llm = PolitiqueLLM(modele, endpoint=endpoint, jeu="labyrinthe")
            mesures[nom] = {
                "oracle": _mesure(probleme, registre, oracle, budget),
                "aveugle": _mesure(probleme, registre, negatif, budget),
                "hasard": _mesure(probleme, registre, hasard, budget),
                "llm": _mesure(probleme, registre, llm, budget),
            }
        c = mesures["cadenas"]["regle"]
        l = mesures["labyrinthe"]["llm"]
        p = mesures["porte"]["llm"]
        seuils = {
            "cadenas_oracle": mesures["cadenas"]["oracle"]["but"],
            "cadenas_aveugle_non": not mesures["cadenas"]["aveugle"]["but"],
            "cadenas_minimal_non": not mesures["cadenas"]["minimal"]["but"],
            "cadenas_regle": c["but"],
            "cadenas_regle_appels": c["appels"] > 0,
            "labyrinthe_oracle": mesures["labyrinthe"]["oracle"]["but"],
            "labyrinthe_llm_sonde": l["par_operateur"].get("sonde", 0) > 0,
            "porte_oracle": mesures["porte"]["oracle"]["but"],
            "aucune_erreur_llm": all(m["erreurs"] == 0 for m in
                                      (mesures["cadenas"]["minimal"], c, l, p)),
            "latence_mesuree": all(m["latence_s"] > 0 for m in
                                   (mesures["cadenas"]["minimal"], c, l, p)),
        }
        resultat = {
            "date": time.strftime("%Y-%m-%d %H:%M %Z"),
            "modele": str(modele),
            "endpoint": endpoint,
            "politique": {"classe": "PolitiqueLLM", "jeu": "cadenas/labyrinthe",
                          "contrainte": "grammaire GBNF, un mot de direction"},
            "mesures": mesures,
            "seuils": seuils,
            "verdict": all(seuils.values()),
            "limites": [
                "Le labyrinthe a des opérateurs pas/saut : le but seul ne prouve pas la politique ; "
                "on lit les appels à la sonde.",
                "Le prompt minimal du cadenas échoue (`arriere` à la position 0) : la variante "
                "`regle` est celle qui qualifie ; le modèle n'infère pas la sémantique d'avant.",
                "La porte n'est pas décrite dans le prompt : le modèle ne peut pas deviner sa règle.",
                "Le coût du registre est symbolique (1 ou 5) ; la latence réelle est à côté.",
                "CPU seulement (GPU de N2 réservés) ; une seule graine de serveur.",
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
                      "cadenas": {k: (v["but"], v["noeuds"], v["cout"], v["appels"],
                                      v["latence_s"], v["erreurs"])
                                  for k, v in mesures["cadenas"].items()},
                      "labyrinthe": {k: (v["but"], v["noeuds"], v["par_operateur"].get("sonde", 0),
                                        v["latence_s"], v["erreurs"])
                                    for k, v in mesures["labyrinthe"].items()},
                      "porte": {k: (v["but"], v["noeuds"], v["par_operateur"].get("sonde", 0),
                                    v["latence_s"], v["erreurs"])
                                for k, v in mesures["porte"].items()}},
                     ensure_ascii=False, indent=1))
    print(f"écrit : {sortie}")
    return 0 if resultat["verdict"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
