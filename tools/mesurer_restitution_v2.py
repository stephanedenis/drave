#!/usr/bin/env python3
"""mesurer_restitution_v2.py — produit le JSON de la fiche D2.

Mesure la **restitution v2** — les rôles (agent, prédicat, lieu) — sur les **46 textes
annotables** du banc v0 (`reports/pensee-fiabilite-produit.json`) et compare le cadre
principal à l'**or écrit à la main** (`tools/tests/linguistique/gold_restitution_v2.json`).
Écrit `reports/pensee-restitution-v2.json`. La fiche `reports/rapport-restitution-v2.md`
cite ce JSON.

    python3 tools/mesurer_restitution_v2.py
"""
from __future__ import annotations

import datetime
import hashlib
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

import tools.restitution as restitution  # noqa: E402
import tools.restitution_v2 as v2  # noqa: E402

BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
GOLD = v2.GOLD_DEFAUT
SORTIE = RACINE / "reports" / "pensee-restitution-v2.json"

LIMITES = [
    "L'or ne note que le **cadre principal** (agent, prédicat, lieu) : 46 textes, 46 cadres, "
    "65 variantes. Il ne note ni les subordonnées, ni les seconds cadres, ni les rôles "
    "patient / destinataire / moyen. Un cadre exact ne dit pas que tous les rôles du texte "
    "sont justes ; un cadre faux ne dit pas que tous les rôles sont faux.",
    "L'or est écrit à la main en lisant le texte, mais **après avoir vu les sorties** : c'est "
    "un biais nommé, pas un or aveugle. Il est de la même main que la fiche (comme le gold S). "
    "Les variantes déclarent les ambiguïtés réelles (coordination, contraction, inversion) ; "
    "elles ne sont pas un droit à mélanger les rôles.",
    "Le lecteur v2 est une **vue** : il lit les rôles déjà présents dans l'annotation "
    "(`meta.role`) et les cibles de `meta.attachement`. Il ne ré-analyse pas la phrase : une "
    "erreur de rôle de l'analyseur reste une erreur de la v2.",
    "Le repli « groupe nominal à gauche du prédicat » fabrique un agent là où l'annotation n'en "
    "a pas (surtout en anglais). C'est une heuristique nommée, source mesurée de faux positifs.",
    "Le cadre principal est le premier prédicat qui porte un agent ou un lieu ; sur `f50` "
    "(2 144 caractères, plusieurs paragraphes), ce n'est pas nécessairement la phrase principale.",
    "La restitution du rendu est exacte 46/46 **par construction** : `relire_roles` relit les "
    "valeurs que `rendre_roles` vient d'écrire. C'est un codec, pas une compréhension.",
    "Les 4 refus (`f14`, `f15`, `f16`, `f17`) n'ont pas d'annotation : 46 textes mesurables sur "
    "50. Le banc est écrit à la main (audit A26), pas un échantillon aléatoire.",
    "Le contrôle externe (gold S, 61 phrases, 144 rôles) est un gold de la même famille de "
    "règles : 0,9653 n'est pas une validation humaine indépendante, seulement un contrôle que "
    "le lecteur n'est pas cassé quand l'or est propre.",
]


def _sha256(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def main() -> int:
    donnees = json.loads(BANC.read_text(encoding="utf-8"))
    gold = json.loads(GOLD.read_text(encoding="utf-8"))
    items = restitution.items_banc(donnees)
    mesure = v2.mesurer_banc_v2(items, gold)
    externe = v2.mesurer_gold_analyseur()
    rapport = {
        "schema": v2.SCHEMA_BANC,
        "version": v2.VERSION,
        "date": datetime.date.today().isoformat(),
        "ligne": "B13",
        "tache": "D2",
        "titre": "La restitution v2 — les rôles (agent, prédicat, lieu)",
        "banc": str(BANC.relative_to(RACINE)),
        "banc_sha256": _sha256(BANC),
        "gold": str(GOLD.relative_to(RACINE)),
        "gold_sha256": _sha256(GOLD),
        "commande": "python3 tools/drave.py restituer --banc "
                    "reports/pensee-fiabilite-produit.json --roles --json",
        "dispositif": {
            "outil": "tools/restitution_v2.py",
            "cli": "python3 tools/drave.py restituer TEXTE --roles",
            "analyse": "bloc_linguistique.Heuristique().analyser(texte, langue=None)",
            "roles": list(v2.ROLES),
            "lecture": "syntagmes + meta.role + meta.attachement",
            "cadre_principal": "premier prédicat qui porte un agent ou un lieu, sinon le premier",
            "repli_agent": "groupe nominal à gauche du prédicat si aucun rôle agent",
            "fidelite": "valeur canonique (casse, ponctuation, espaces) contre l'or ; "
                        "meilleure variante d'ambiguïté",
            "rendu": "relire_roles(rendre_roles(annotation))",
            "controle_externe": externe,
        },
        "synthese": mesure["synthese"],
        "resultats": mesure["resultats"],
        "limites": LIMITES,
    }
    SORTIE.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n",
                      encoding="utf-8")
    print(v2.formater_banc_v2(rapport, str(BANC.relative_to(RACINE))))
    print(f"\ncontrôle externe (gold S) : {externe['roles_justes']}/{externe['roles_total']} "
          f"({externe['taux']:.4f}) · baseline "
          f"{externe['baseline_role_constant']['justes']}/"
          f"{externe['baseline_role_constant']['total']} "
          f"({externe['baseline_role_constant']['taux']:.4f})")
    print(f"\nécrit : {SORTIE.relative_to(RACINE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
