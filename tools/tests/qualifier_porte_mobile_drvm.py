#!/usr/bin/env python3
"""qualifier_porte_mobile_drvm.py — la porte **mobile** : deux positions (3,3) et (1,3).

`LABYRINTHE_PORTE_MOBILE_0/1` (registre `REGISTRE_PMOB`) : la porte est en `(3,3)` ou en
`(1,3)` — cette dernière est dans un mur du labyrinthe. La politique doit **visser** la porte
pour que la sonde l'ouvre. On mesure l'oracle (`PolitiqueManhattan`, la porte T31), la Q-table
sans A* (`PolitiqueAppriseMobile`, T31), l'aveugle, le hasard, le LLM avec le prompt
`porte_mobile` (la position de la porte) et le LLM avec le prompt `labyrinthe` (sans la porte).

    python3 tools/tests/qualifier_porte_mobile_drvm.py --endpoint http://127.0.0.1:18082 \
        --sortie reports/pensee-porte-mobile.json

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
from tools.pensee.operateurs import (DRVM, LABYRINTHE_PORTE_MOBILE_0,  # noqa: E402
                                     LABYRINTHE_PORTE_MOBILE_1, REGISTRE_PMOB,
                                     PolitiqueAppriseMobile, PolitiqueAveugle,
                                     PolitiqueHasard, PolitiqueLLM, PolitiqueManhattan,
                                     seule_mobile)
from tools.pensee.store import Budget  # noqa: E402

LABS = (("0", LABYRINTHE_PORTE_MOBILE_0), ("1", LABYRINTHE_PORTE_MOBILE_1))


def _mesure(politique, lab) -> dict:
    t0 = time.perf_counter()
    d = DRVM(REGISTRE_PMOB, politique)
    d.penser(lab, AStar(), Budget(200))
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
    ap.add_argument("--sortie", default=str(RACINE / "reports/pensee-porte-mobile.json"))
    args = ap.parse_args()
    modele = pathlib.Path(args.modele)
    if not modele.exists():
        raise SystemExit(f"modèle absent : {modele}")
    endpoint = args.endpoint or f"http://127.0.0.1:{args.port}"
    proc = None
    if not _sante(endpoint):
        if not args.demarrer:
            raise SystemExit(f"serveur absent sur {endpoint} — relancer avec --demarrer")
        proc = demarrer_serveur(modele, args.port, pathlib.Path("/tmp/qualifier-porte-mobile-serveur.log"))
    try:
        apprise = PolitiqueAppriseMobile(episodes=1000, graine=0)
        apprise.apprendre()
        seule = {nom: seule_mobile(apprise, int(nom)) for nom, _ in LABS}
        llms = {(nom, jeu): PolitiqueLLM(modele, endpoint=endpoint, jeu=jeu)
                for nom, _ in LABS for jeu in ("porte_mobile", "labyrinthe")}
        mesures = {}
        for nom, lab in LABS:
            mesures[nom] = {
                "oracle": _mesure(PolitiqueManhattan(), lab),
                "aveugle": _mesure(PolitiqueAveugle(), lab),
                "hasard": _mesure(PolitiqueHasard(), lab),
                "llm_porte_mobile": _mesure(llms[(nom, "porte_mobile")], lab),
                "llm_labyrinthe": _mesure(llms[(nom, "labyrinthe")], lab),
            }
        m0, m1 = mesures["0"], mesures["1"]
        llm_err = [v["erreurs"] for m in mesures.values() for k, v in m.items() if k.startswith("llm_")]
        seuils = {
            "oracle_0": m0["oracle"]["but"],
            "oracle_1": m1["oracle"]["but"],
            "aveugle_0_non": not m0["aveugle"]["but"],
            "aveugle_1_non": not m1["aveugle"]["but"],
            "llm_0": m0["llm_porte_mobile"]["but"],
            "llm_1": m1["llm_porte_mobile"]["but"],
            "llm_sonde_0": m0["llm_porte_mobile"]["par_operateur"].get("sonde", 0) > 0,
            "llm_sonde_1": m1["llm_porte_mobile"]["par_operateur"].get("sonde", 0) > 0,
            "labyrinthe_1_non": not m1["llm_labyrinthe"]["but"],
            "llm_mieux_labyrinthe_1": m1["llm_porte_mobile"]["but"] and not m1["llm_labyrinthe"]["but"],
            "apprise_0": seule["0"][0],
            "apprise_1": seule["1"][0],
            "aucune_erreur_llm": all(e == 0 for e in llm_err),
            "latence_mesuree": m0["llm_porte_mobile"]["latence_s"] > 0,
        }
        resultat = {
            "date": time.strftime("%Y-%m-%d %H:%M %Z"),
            "modele": str(modele),
            "endpoint": endpoint,
            "probleme": {"nom": "labyrinthe_porte_mobile", "portes": [[3, 3], [1, 3]],
                         "but": [4, 4],
                         "regle": "depuis une case voisine, la sonde ouvre la porte si la "
                                  "politique vise sa direction",
                         "budget": 200},
            "politique": {"classe": "PolitiqueLLM", "jeux": ["porte_mobile", "labyrinthe"],
                          "contrainte": "grammaire GBNF, quatre directions"},
            "mesures": mesures,
            "apprise": {"episodes": 1000, "etats_q": len(apprise.q),
                        "seule_0": {"but": seule["0"][0], "pas": seule["0"][1]},
                        "seule_1": {"but": seule["1"][0], "pas": seule["1"][1]}},
            "seuils": seuils,
            "verdict": all(seuils.values()),
            "limites": [
                "La porte mobile a deux positions ; (1,3) est dans un mur du labyrinthe : c'est "
                "la position qui discrimine le prompt.",
                "Le hasard peut ouvrir une porte ; le contrôle propre est l'aveugle et le "
                "labyrinthe (surtout à (1,3)).",
                "L'A* explore ; le nombre de nœuds dépend du tie-breaking ; le but et la sonde "
                "sont les mesures.",
                "La Q-table `PolitiqueAppriseMobile` (1000 épisodes) est la référence sans A* "
                "(porte T31) ; elle n'est pas le LLM.",
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
                      "mesures": {nom: {k: (v["but"], v["noeuds"], v["cout"], v["appels"],
                                            v["par_operateur"].get("sonde", 0),
                                            v["latence_s"], v["erreurs"])
                                       for k, v in m.items()}
                                  for nom, m in mesures.items()}},
                     ensure_ascii=False, indent=1))
    print(f"écrit : {sortie}")
    return 0 if resultat["verdict"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
