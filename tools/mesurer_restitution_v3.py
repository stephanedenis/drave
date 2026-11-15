#!/usr/bin/env python3
"""mesurer_restitution_v3.py — produit le JSON de la fiche W5 (restitution v3).

Mesure la **restitution v3** — les rôles des groupes prépositionnels — sur les deux ors
existants :

- le **gold v2** (46 textes, 46 cadres agent/prédicat/lieu) : précision et rappel des
  trois rôles, avant (v2) et après (v3) ; le gold n'annote pas les cinq rôles de GP ;
- le **gold S** (61 phrases, 144 rôles) : précision et rappel **par rôle**, avec les
  effectifs ; les cinq rôles n'y ont que 18 occurrences, `complement` zéro.

Le JSON sépare les deux leviers du gain sur le gold S : les **rôles** (v2 → v3 à
appariement v2) et l'**appariement** (tie-break du span le plus court). Sans cette
séparation, le 144/144 ferait croire à un gain de rôles qui est en partie un gain de
mesure.

Écrit `reports/pensee-restitution-v3.json`. La fiche `reports/rapport-restitution-v3.md`
cite ce JSON.

    python3 tools/mesurer_restitution_v3.py
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
import tools.restitution_v3 as v3  # noqa: E402

BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
GOLD = v3.GOLD_DEFAUT
GOLD_S = v3.GOLD_ANALYSEUR
REFERENCE_V2 = RACINE / "reports" / "pensee-restitution-v2.json"
SORTIE = RACINE / "reports" / "pensee-restitution-v3.json"

LIMITES = [
    "Le **gold v2** (46 textes) n'annote que `agent`, `prédicat` et `lieu` : les cinq rôles "
    "de GP (`lieu`, `temps`, `destinataire`, `possession`, `complement`) ne sont donc "
    "**pas** mesurés sur ce banc. La précision/rappel des cinq ne vient que du gold S.",
    "Le **gold S** (61 phrases, 144 rôles) est un or de la **même famille de règles**, écrit "
    "avant la v3 : 144/144 n'est pas une validation humaine indépendante. Les cinq rôles "
    "n'y ont que **18 occurrences** (3 lieux, 9 temps, 5 destinataires, 1 possession, "
    "0 complément) : un score parfait sur 18 items est une preuve faible.",
    "Le rôle `complement` n'a **aucune occurrence** dans le gold S. Le repli de la règle "
    "n'est donc pas mesuré par l'or ; il n'est couvert que par les cas de séparation "
    "synthétiques, qui ne sont pas un gold.",
    "Les lexiques de temps, de lieu et de personne ont été écrits en lisant le gold S : "
    "c'est un biais nommé, pas un test aveugle. Un autre lexique changerait les chiffres.",
    "Le **144/144** du gold S mélange deux leviers : les rôles (v2 → v3) et l'appariement "
    "(tie-break du span le plus court). Le JSON les sépare : +4 rôles et +1 appariement. "
    "Le chiffre global ne doit pas être lu comme un gain de rôles seul.",
    "Le dédoublonnage des GP de même début garde le plus long quand le plus court est **nu** "
    "(`vers` / `vers 9 h`), sinon le plus court. Ce choix jette parfois un GP long correct "
    "(`sur le toit de la maison` ramené à `sur le toit`) ; il est assumé pour la précision.",
    "La **segmentation** reste la première cause d'échec sur le banc v2 : `f08` n'a pas de "
    "GP, `f24` et `f49` non plus, `f50` en invente. La règle de rôle ne peut pas corriger "
    "un span absent ou trop large (`à Paris dure deux heures`).",
    "Le **cadre principal** est le premier prédicat qui porte un agent ou un lieu : un cadre "
    "correct ailleurs ne compte pas. Le chiffre mesure un cadre par texte, pas la phrase.",
    "Le **codec** `relire_roles(rendre_roles(a)) == principal` est exact 46/46 **par "
    "construction** : il recopie puis relit les valeurs. Il ne compte pas comme fidélité.",
    "Les 46 textes sont écrits à la main (audit A26), pas un échantillon aléatoire ; le banc "
    "mêle français et anglais, et `agent` n'a pas la même définition syntaxique dans les deux.",
]


def _sha256(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def _reference_v2() -> dict:
    if not REFERENCE_V2.exists():
        return {}
    d = json.loads(REFERENCE_V2.read_text(encoding="utf-8"))
    s = d.get("synthese", {})
    ext = (d.get("dispositif") or {}).get("controle_externe") or {}
    return {
        "fichier": str(REFERENCE_V2.relative_to(RACINE)),
        "date": d.get("date"),
        "banc": {
            "cadres_exacts": s.get("cadre", {}).get("exacts"),
            "exacts_non_vides": s.get("cadre", {}).get("exacts_non_vides"),
            "roles_justes": s.get("roles", {}).get("justes"),
            "roles_attendus": s.get("roles", {}).get("attendus"),
            "precision": s.get("roles", {}).get("precision"),
            "rappel": s.get("roles", {}).get("rappel"),
            "f1": s.get("roles", {}).get("f1"),
            "par_role": s.get("roles", {}).get("par_role"),
        },
        "gold_s": {
            "roles_justes": ext.get("roles_justes"),
            "roles_total": ext.get("roles_total"),
            "taux": ext.get("taux"),
            "baseline_role_constant": ext.get("baseline_role_constant"),
        },
    }


def main() -> int:
    donnees = json.loads(BANC.read_text(encoding="utf-8"))
    gold = json.loads(GOLD.read_text(encoding="utf-8"))
    items = restitution.items_banc(donnees)
    mesure = v3.mesurer_banc_v3(items, gold)
    controles_banc = v3.controler_banc_v3(items, gold)
    gold_s = v3.mesurer_gold_analyseur_v3()
    gold_s_v2 = v3.mesurer_gold_analyseur_v3(appariement="v2")
    gold_s_v2_roles = v3.mesurer_gold_analyseur_v3(appariement="v2", preparer=False)
    gold_s_v3_roles = v3.mesurer_gold_analyseur_v3(appariement="v3", preparer=False)
    separation = v3.mesurer_separation()
    ref = _reference_v2()

    v3_bank = mesure["synthese"]
    v2_bank = ref.get("banc") or {}
    comparaison = {
        "banc": {
            "v2": v2_bank,
            "v3": {
                "cadres_exacts": v3_bank["cadre"]["exacts"],
                "exacts_non_vides": v3_bank["cadre"]["exacts_non_vides"],
                "roles_justes": v3_bank["roles"]["justes"],
                "roles_attendus": v3_bank["roles"]["attendus"],
                "precision": v3_bank["roles"]["precision"],
                "rappel": v3_bank["roles"]["rappel"],
                "f1": v3_bank["roles"]["f1"],
                "par_role": v3_bank["roles"]["par_role"],
            },
        },
        "gold_s_decoupage": {
            "v2_roles_v2_appariement": {
                "global": f"{gold_s_v2_roles['base']['justes']}/{gold_s_v2_roles['base']['total']}",
                "cinq": f"{gold_s_v2_roles['base']['cinq_roles']['justes']}/"
                        f"{gold_s_v2_roles['base']['cinq_roles']['attendus']}",
                "f1_cinq": gold_s_v2_roles["base"]["cinq_roles"]["f1"],
                "par_role": gold_s_v2_roles["base"]["par_role"],
            },
            "v2_roles_v3_appariement": {
                "global": f"{gold_s_v3_roles['base']['justes']}/{gold_s_v3_roles['base']['total']}",
                "cinq": f"{gold_s_v3_roles['base']['cinq_roles']['justes']}/"
                        f"{gold_s_v3_roles['base']['cinq_roles']['attendus']}",
                "f1_cinq": gold_s_v3_roles["base"]["cinq_roles"]["f1"],
                "par_role": gold_s_v3_roles["base"]["par_role"],
            },
            "v3_roles_v2_appariement": {
                "global": f"{gold_s_v2['base']['justes']}/{gold_s_v2['base']['total']}",
                "cinq": f"{gold_s_v2['base']['cinq_roles']['justes']}/"
                        f"{gold_s_v2['base']['cinq_roles']['attendus']}",
                "f1_cinq": gold_s_v2["base"]["cinq_roles"]["f1"],
                "par_role": gold_s_v2["base"]["par_role"],
            },
            "v3_roles_v3_appariement": {
                "global": f"{gold_s['base']['justes']}/{gold_s['base']['total']}",
                "cinq": f"{gold_s['base']['cinq_roles']['justes']}/"
                        f"{gold_s['base']['cinq_roles']['attendus']}",
                "f1_cinq": gold_s["base"]["cinq_roles"]["f1"],
                "par_role": gold_s["base"]["par_role"],
            },
            "gain_roles": {
                "global": (gold_s_v2["base"]["justes"] - gold_s_v2_roles["base"]["justes"]),
                "cinq": (gold_s_v2["base"]["cinq_roles"]["justes"]
                         - gold_s_v2_roles["base"]["cinq_roles"]["justes"]),
            },
            "gain_appariement": {
                "global": (gold_s["base"]["justes"] - gold_s_v2["base"]["justes"]),
                "cinq": (gold_s["base"]["cinq_roles"]["justes"]
                         - gold_s_v2["base"]["cinq_roles"]["justes"]),
            },
        },
    }

    rapport = {
        "schema": v3.SCHEMA_BANC,
        "version": v3.VERSION,
        "date": datetime.date.today().isoformat(),
        "ligne": "B13",
        "tache": "W5 (J3 après-midi)",
        "titre": "La restitution v3 — les rôles des groupes prépositionnels",
        "banc": str(BANC.relative_to(RACINE)),
        "banc_sha256": _sha256(BANC),
        "gold": str(GOLD.relative_to(RACINE)),
        "gold_sha256": _sha256(GOLD),
        "gold_s": str(GOLD_S.relative_to(RACINE)),
        "gold_s_sha256": _sha256(GOLD_S),
        "reference_v2": ref,
        "commande": ("python3 tools/drave.py restituer --banc "
                     "reports/pensee-fiabilite-produit.json --roles-v3 --json"),
        "dispositif": {
            "outil": "tools/restitution_v3.py",
            "regle": "tools/roles_gp.py (rôle = préposition + contexte)",
            "cli": "python3 tools/drave.py restituer TEXTE --roles-v3",
            "analyse": "bloc_linguistique.Heuristique().analyser(texte, langue=None)",
            "preparation": ("dédoublonnage des GP de même début (long si le court est nu, "
                            "sinon court) puis rôle v3 avec le syntagme précédent"),
            "or_v2": "tools/tests/linguistique/gold_restitution_v2.json (46 cadres)",
            "or_s": "tools/structures/donnees/gold-analyseur.json (61 phrases, 144 rôles)",
            "appariement_gold_s": ("recouvrement maximal à type égal, tie-break du span "
                                    "le plus court ; l'appariement v2 est conservé pour "
                                    "séparer le gain de rôles du gain de mesure"),
            "cinq_roles": list(v3.CINQ),
            "controle_negatif": ("permutation cyclique des cinq rôles, permutation de tous "
                                 "les rôles, rôle constant"),
        },
        "synthese": v3_bank,
        "resultats": mesure["resultats"],
        "controles": {
            "banc": controles_banc,
            "gold_s": {
                "baseline_role_constant": gold_s["baseline_role_constant"],
                "role_constant_lieu": gold_s["role_constant_lieu"],
                "permutation_cinq": gold_s["permutation_cinq"],
                "permutation_tous": gold_s["permutation_tous"],
            },
            "codec": {
                "rendu": v3_bank["controles"]["rendu"],
                "negatif_rendu": v3_bank["controles"]["negatif_rendu"],
                "spans_dans_source": v3_bank["controles"]["spans_dans_source"],
            },
        },
        "gold_s": gold_s,
        "gold_s_decoupage": comparaison["gold_s_decoupage"],
        "separation": separation,
        "comparaison_v2_v3": comparaison,
        "limites": LIMITES,
    }
    SORTIE.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n",
                      encoding="utf-8")
    print(v3.formater_banc_v3(rapport, str(BANC.relative_to(RACINE))))
    print("")
    print(f"gold S : {gold_s['base']['justes']}/{gold_s['base']['total']} "
          f"({gold_s['base']['taux']:.4f}) · cinq rôles "
          f"{gold_s['base']['cinq_roles']['justes']}/"
          f"{gold_s['base']['cinq_roles']['attendus']} "
          f"(F1 {gold_s['base']['cinq_roles']['f1']:.4f})")
    print(f"permutation des cinq : {gold_s['permutation_cinq']['mesure']['cinq_roles']['justes']}"
          f"/{gold_s['permutation_cinq']['mesure']['cinq_roles']['attendus']} ; "
          f"permutation de tous : {gold_s['permutation_tous']['mesure']['taux']:.4f} global")
    print(f"séparation : {separation['justes']}/{separation['total']}")
    print(f"écrit : {SORTIE.relative_to(RACINE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
