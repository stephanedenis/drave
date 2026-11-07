#!/usr/bin/env python3
"""mesurer_restitution_v0.py — produit le JSON de la fiche J1.4.

Mesure la restitution v0 sur les **50 textes libres** de
`reports/pensee-fiabilite-produit.json` (le banc de l'audit A26) et écrit
`reports/pensee-restitution-v0.json`. La fiche `reports/rapport-restitution-v0.md`
cite ce JSON.

    python3 tools/mesurer_restitution_v0.py
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
SORTIE = RACINE / "reports" / "pensee-restitution-v0.json"

LIMITES = [
    "4 refus sans annotation (f14 emoji, f15 vide, f16 espaces, f17 « ... ») : "
    "la surface n'est pas reconstructible, ils sont comptés à part.",
    "La fidélité binaire du miroir compare la sortie à la source exacte : la ponctuation "
    "séparée des mots fait tomber mots et POS à 5/46, alors que la fidélité de caractères "
    "reste à 0,9506. Les deux mesures disent des choses différentes.",
    "La surface est le niveau `graphème` ; les niveaux `mot` et `pos` ne portent ni les "
    "espaces ni les sauts de ligne. La restitution v0 est un codec de surface, pas un "
    "décodeur neuronal : elle ne prouve pas la fidélité sémantique.",
    "Le contrôle négatif mélange les graphèmes (ou les retourne s'il n'y en a qu'un) et "
    "retire le dernier : il teste l'ordre et le contenu, pas le sens.",
    "Le banc est écrit à la main (audit A26) et n'a pas de gold de restitution : la "
    "mesure est un invariant de surface, pas une exactitude linguistique.",
]


def _sha256(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def main() -> int:
    donnees = json.loads(BANC.read_text(encoding="utf-8"))
    items = restitution.items_banc(donnees)
    mesure = restitution.mesurer_banc(items)
    rapport = {
        "schema": restitution.SCHEMA + ".banc",
        "version": restitution.VERSION,
        "date": datetime.date.today().isoformat(),
        "ligne": "B13",
        "tache": "J1.4",
        "titre": "La restitution v0 — annotation → surface, et le miroir",
        "banc": str(BANC.relative_to(RACINE)),
        "banc_sha256": _sha256(BANC),
        "commande": "python3 tools/drave.py restituer --banc "
                    "reports/pensee-fiabilite-produit.json --json",
        "dispositif": {
            "outil": "tools/restitution.py",
            "cli": "python3 tools/drave.py restituer TEXTE",
            "analyse": "bloc_linguistique.Heuristique().analyser(texte, langue=None)",
            "niveau_surface": "graphème",
            "correctif": "catégorie Unicode C (contrôle) annotée comme graphème ; "
                         "sans lui, f50 perd ses 10 sauts de ligne (45/46)",
            "fidelite": "binaire (rendu == source) + Levenshtein normalisé",
            "miroir": restitution.DEFINITION_MIROIR,
        },
        "synthese": mesure["synthese"],
        "resultats": mesure["resultats"],
        "limites": LIMITES,
    }
    SORTIE.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n",
                      encoding="utf-8")
    print(restitution.formater_banc(rapport, str(BANC.relative_to(RACINE))))
    print(f"\nécrit : {SORTIE.relative_to(RACINE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
