#!/usr/bin/env python3
"""mesurer_restitution_v1.py — produit le JSON de la fiche J8.1.

Mesure la **forme canonique v1** sur les **50 textes libres** de
`reports/pensee-fiabilite-produit.json` (le banc de l'audit A26) et écrit
`reports/pensee-restitution-v1.json`. La fiche `reports/rapport-restitution-v1.md`
cite ce JSON.

La v1 ne remplace pas la v0 : elle ajoute une lecture **structurelle** (segments +
rôles + cibles) et un **miroir canonique** comparé à une source canonisée. Le miroir
strict (surface brute) reste mesuré, pour que la réponse à « doit-il monter ? » soit
vérifiable.

    python3 tools/mesurer_restitution_v1.py
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

BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
SORTIE = RACINE / "reports" / "pensee-restitution-v1.json"

LIMITES = [
    "Le miroir canonique vaut 1,0000 **par construction** : les jetons viennent des "
    "spans `mot`/`pos`, qui sont des sous-chaînes de la source ; la canonisation retire "
    "la casse, la ponctuation et les espaces. C'est un invariant de codec, pas une "
    "compréhension sémantique.",
    "Le miroir strict **ne monte pas** (5/46 = 0,1087) et la forme canonique le fait "
    "tomber à 1/46 = 0,0217 si on la compare à la source brute : elle n'est pas la "
    "surface. Le seul texte exact est `f18` (`1234567890`), sans casse ni ponctuation.",
    "Les segments ne couvrent que 65,84 % des jetons et 75,19 % des caractères en "
    "moyenne : le plancher lexical (`mot` > `pos` > `graphème`) remplit le reste. Les "
    "rôles et les cibles sont des mesures de **cohérence**, pas de justesse — il n'y a "
    "pas de gold de forme canonique.",
    "La stabilité structurelle n'est que 18/46 = 0,3913 : re-analyser la surface "
    "canonique (sans ponctuation ni casse) change la segmentation. Le lexique, lui, est "
    "stable 46/46. La forme canonique n'est donc pas un point fixe du bloc heuristique.",
    "Les 4 refus (`f14`, `f15`, `f16`, `f17`) n'ont pas d'annotation : 46 textes "
    "mesurables sur 50. Le banc est écrit à la main (audit A26), pas un échantillon "
    "aléatoire.",
]


def _sha256(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def main() -> int:
    donnees = json.loads(BANC.read_text(encoding="utf-8"))
    items = restitution.items_banc(donnees)
    mesure = restitution.mesurer_banc_v1(items)
    rapport = {
        "schema": restitution.SCHEMA_CANONIQUE + ".banc",
        "version": restitution.VERSION_CANONIQUE,
        "date": datetime.date.today().isoformat(),
        "ligne": "B13",
        "tache": "J8.1",
        "titre": "La restitution v1 — la forme canonique, et la réponse au miroir strict",
        "banc": str(BANC.relative_to(RACINE)),
        "banc_sha256": _sha256(BANC),
        "commande": "python3 tools/drave.py restituer --banc "
                    "reports/pensee-fiabilite-produit.json --canonique --json",
        "dispositif": {
            "outil": "tools/restitution.py",
            "cli": "python3 tools/drave.py restituer TEXTE --canonique",
            "analyse": "bloc_linguistique.Heuristique().analyser(texte, langue=None)",
            "forme": restitution.DEFINITION_FORME_CANONIQUE,
            "miroir_strict": restitution.DEFINITION_MIROIR,
            "miroir_canonique": restitution.DEFINITION_MIROIR_CANONIQUE,
            "canonisation": "casse repliée ; lettres et chiffres seulement ; espaces "
                            "réduits (regex [^\\W_]+)",
            "linearisation": "segments triés par (union, largeur, confiance, début, fin, "
                             "type), puis sans chevauchement",
            "stabilite": "re-analyser la surface canonique et comparer le squelette",
        },
        "synthese": mesure["synthese"],
        "resultats": mesure["resultats"],
        "limites": LIMITES,
    }
    SORTIE.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n",
                      encoding="utf-8")
    print(restitution.formater_banc_v1(rapport, str(BANC.relative_to(RACINE))))
    print(f"\nécrit : {SORTIE.relative_to(RACINE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
