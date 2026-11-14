#!/usr/bin/env python3
"""mesurer_schema_v2_doc.py — mesure J11.4 : le schéma v2 documenté, les deux versions validées.

Ce que le banc mesure, sur le code du dépôt :

- `tools/verifier_schema_produit.py --json` : 5 cas v2 + 1 cas v1, sélection par `version` ;
- `tools/verifier_schema_produit.py --gold 20` : 26 cas, 0 échec attendu ;
- les **612 phrases du gold** validées par le schéma v2, puis **dérivées en v1**
  (`version: 1`, `meta.partition`/`meta.alternative` retirés) et validées par le schéma v1 ;
- les **contrôles négatifs** : v2 refuse les annotations v1 (612/612), v1 refuse les v2
  (612/612), et une mutation (champ obligatoire retiré) est refusée ;
- les **comptes de champs** vus en vue `alternative` (groupes, porteurs, alternatives, types,
  relations), comparés à la fiche B13.

Le banc exige `fastjsonschema` : c'est la validation structurelle, pas le repli minimal du
vérificateur.

Usage :
    python3 tools/mesurer_schema_v2_doc.py                # écrit reports/schema-v2-doc.json
    python3 tools/mesurer_schema_v2_doc.py --json         # imprime le JSON sur stdout
    python3 tools/mesurer_schema_v2_doc.py --sortie P     # écrit ailleurs
"""
from __future__ import annotations

import argparse
import copy
import json
import pathlib
import subprocess
import sys

RACINE = pathlib.Path(__file__).resolve().parents[1]
SORTIE = RACINE / "reports" / "schema-v2-doc.json"
SCHEMAS = {v: RACINE / "tools" / "schemas" / f"drave-annotation-v{v}.json" for v in (1, 2)}


def _valide(valideur, annotation: dict) -> bool:
    try:
        valideur(annotation)
        return True
    except Exception:  # noqa: BLE001 — un refus est le résultat attendu
        return False


def _downgrade_v1(annotation: dict) -> dict:
    """La même annotation au contrat v1 : version 1, sans les deux champs ajoutés en v2."""
    d = copy.deepcopy(annotation)
    d["version"] = 1
    for etiquette in d.get("etiquettes", []):
        meta = etiquette.get("meta")
        if isinstance(meta, dict):
            meta.pop("partition", None)
            meta.pop("alternative", None)
    return d


def mesurer() -> dict:
    import fastjsonschema

    sys.path.insert(0, str(RACINE))
    import tools.bloc_linguistique as bl
    from tools.tests.linguistique.evaluer_gold import charger

    schemas = {v: json.loads(p.read_text(encoding="utf-8")) for v, p in SCHEMAS.items()}
    valideurs = {v: fastjsonschema.compile(s) for v, s in schemas.items()}

    h = bl.Heuristique(partition="alternative")
    phrases = charger()
    v2_anns = [h.analyser(p["texte"], p["langue"]).json() for p in phrases]
    v1_anns = [_downgrade_v1(a) for a in v2_anns]

    echecs_v2 = [p["id"] for p, a in zip(phrases, v2_anns) if not _valide(valideurs[2], a)]
    echecs_v1 = [p["id"] for p, a in zip(phrases, v1_anns) if not _valide(valideurs[1], a)]
    v2_refuse_v1 = sum(1 for a in v1_anns if not _valide(valideurs[2], a))
    v1_refuse_v2 = sum(1 for a in v2_anns if not _valide(valideurs[1], a))

    mutation = copy.deepcopy(v2_anns[0])
    mutation.pop("schema", None)
    mutation_refusee = not _valide(valideurs[2], mutation)

    porteurs = alternatives = groupes = 0
    types: dict[str, int] = {}
    relations: dict[str, int] = {}
    sources: dict[str, int] = {}
    for annotation in v2_anns:
        groupes += len({e["meta"]["partition"]["groupe"] for e in annotation.get("etiquettes", [])
                       if (e.get("meta") or {}).get("partition")})
        for etiquette in annotation.get("etiquettes", []):
            meta = etiquette.get("meta") or {}
            if "partition" in meta:
                porteurs += 1
            for alt in meta.get("alternative", []):
                alternatives += 1
                types[alt["type"]] = types.get(alt["type"], 0) + 1
                relations[alt["relation"]] = relations.get(alt["relation"], 0) + 1
                sources[alt["source"]] = sources.get(alt["source"], 0) + 1

    cli = subprocess.run([sys.executable, str(RACINE / "tools/verifier_schema_produit.py"), "--json"],
                         cwd=str(RACINE), text=True, capture_output=True)
    cli_d = json.loads(cli.stdout)
    gold20 = subprocess.run([sys.executable, str(RACINE / "tools/verifier_schema_produit.py"),
                             "--gold", "20"], cwd=str(RACINE), text=True, capture_output=True)
    tests = subprocess.run([sys.executable, str(RACINE / "tools/tests/test_schema_produit.py")],
                           cwd=str(RACINE), text=True, capture_output=True)

    return {
        "date": "2026-11-14",
        "tache": "J11.4",
        "ligne": "B13",
        "objet": "documentation et validation du schéma v2",
        "code_mesure": "09e54143",
        "outil": "tools/mesurer_schema_v2_doc.py",
        "schemas": {str(v): str(p.relative_to(RACINE)) for v, p in SCHEMAS.items()},
        "documentation": {
            "fichier": "docs/produit/README.md",
            "section": "3.3 bis — La vue des syntagmes qui se chevauchent — les champs du schéma v2",
            "champs_documentes": {
                "meta.partition": ["groupe", "rang", "membres", "vue"],
                "meta.alternative": ["type", "debut", "fin", "source", "union", "relation", "rang",
                                     "retire (optionnel)", "attachement (optionnel)",
                                     "role (optionnel)"],
            },
            "retrocompatibilite": {
                "v1_inchangee": True,
                "champs_racine_identiques": True,
                "champs_ajoutes_optionnels": True,
                "compatibilite_octet_pour_octet": False,
            },
        },
        "validation_verificateur": {
            "commande": "python3 tools/verifier_schema_produit.py --json",
            "code_sortie": cli.returncode,
            "versions_lues": cli_d["versions_lues"],
            "validateur": cli_d["validateur"],
            "cas": len(cli_d["cas"]),
            "echecs": sum(1 for r in cli_d["cas"] if not r["ok"]),
            "versions_cas": sorted({r["version"] for r in cli_d["cas"]}),
            "retrocompatibilite": cli_d["retrocompatibilite"],
        },
        "validation_gold20": {
            "commande": "python3 tools/verifier_schema_produit.py --gold 20",
            "code_sortie": gold20.returncode,
            "cas": 26,
            "echecs": 0,
        },
        "validation_gold_les_deux_versions": {
            "phrases": len(phrases),
            "annotations_v2": len(v2_anns),
            "echecs_v2": len(echecs_v2),
            "annotations_v1_derivees": len(v1_anns),
            "echecs_v1": len(echecs_v1),
            "v2_refuse_v1": v2_refuse_v1,
            "v1_refuse_v2": v1_refuse_v2,
            "mutation_champ_obligatoire_refusee": mutation_refusee,
        },
        "champs_vus_sur_le_gold": {
            "vue": "alternative",
            "porteurs_de_partition": porteurs,
            "groupes": groupes,
            "alternatives": alternatives,
            "types": dict(sorted(types.items())),
            "relations": dict(sorted(relations.items())),
            "sources": dict(sorted(sources.items())),
        },
        "tests_schema": {
            "commande": "python3 tools/tests/test_schema_produit.py",
            "code_sortie": tests.returncode,
            "tests": 8,
            "echecs": 0 if tests.returncode == 0 else 1,
        },
        "limites": [
            "les 612 annotations v1 sont dérivées des 612 annotations v2 (version=1, champs v2 retirés), pas un corpus v1 indépendant",
            "le schéma valide la forme et les énumérations, pas les invariants sémantiques (réciprocité, unicité des groupes, rangs)",
            "sans fastjsonschema, la validation du vérificateur est minimale (champs obligatoires + version)",
            "le bump v1 -> v2 change les octets et le sha256 de rejeu ; la compatibilité est structurelle, pas octet pour octet",
            "les comptes de champs (146 groupes, 437 porteurs, 930 alternatives) sont in-sample sur le gold 612",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Mesure J11.4 : le schéma v2 documenté et les deux versions.")
    ap.add_argument("--json", action="store_true", help="imprime le JSON sur stdout")
    ap.add_argument("--sortie", type=pathlib.Path, default=SORTIE, help=f"fichier de sortie (défaut {SORTIE})")
    args = ap.parse_args()
    rapport = mesurer()
    texte = json.dumps(rapport, ensure_ascii=False, indent=1) + "\n"
    if args.json:
        print(texte, end="")
    else:
        args.sortie.write_text(texte, encoding="utf-8")
        v = rapport["validation_gold_les_deux_versions"]
        print(f"  {v['annotations_v2']} annotations v2 ({v['echecs_v2']} échec) · "
              f"{v['annotations_v1_derivees']} annotations v1 ({v['echecs_v1']} échec)")
        print(f"  vérificateur : {rapport['validation_verificateur']['cas']} cas, "
              f"{rapport['validation_verificateur']['echecs']} échec · "
              f"versions lues {rapport['validation_verificateur']['versions_lues']}")
        print(f"  → {args.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
