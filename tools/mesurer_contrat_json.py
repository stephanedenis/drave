#!/usr/bin/env python3
"""mesurer_contrat_json.py — T2 : les candidats d'attachement en objets, les rôles normalisés.

Le banc mesure, sur le gold vivant (612 phrases), ce que le consommateur du JSON peut
supposer :

- chaque `meta.attachement` porte des `candidats` **objets** `{span, cible, source}` ;
- chaque `span` découpe exactement sa `cible` dans `texte` ;
- chaque `meta.role` non vide appartient au vocabulaire fermé (huit rôles) ;
- les 21 rôles bruts observés passent tous par la table de correspondance ;
- le schéma v2 valide les 612 annotations, et les 612 annotations dérivées v1 restent lues.

Trois contrôles négatifs :

1. un consommateur qui filtre `role == "predicat"` trouve les prédicats (711 GV), et
   `role == "prédicat"` n'en trouve aucun (l'ancienne forme accentuée n'est plus publiée) ;
2. `normaliser_role("role_invente")` lève `RoleHorsVocabulaire` ;
3. un candidat ramené à une chaîne (ou privé de `span`) est refusé par le schéma v2.

Usage :
    python3 tools/mesurer_contrat_json.py                # écrit reports/contrat-json.json
    python3 tools/mesurer_contrat_json.py --json         # imprime le JSON sur stdout
    python3 tools/mesurer_contrat_json.py --sortie P     # écrit ailleurs
"""
from __future__ import annotations

import argparse
import collections
import copy
import json
import pathlib
import re
import subprocess
import sys

RACINE = pathlib.Path(__file__).resolve().parents[1]
SORTIE = RACINE / "reports" / "contrat-json.json"


def _ran(sortie: str) -> int:
    """Le nombre de tests lus dans la sortie d'`unittest`."""
    trouve = re.search(r"Ran (\d+) tests", sortie or "")
    return int(trouve.group(1)) if trouve else 0


def _valide(valideur, annotation: dict) -> bool:
    try:
        valideur(annotation)
        return True
    except Exception:  # noqa: BLE001 — un refus est le résultat attendu
        return False


def _downgrade_v1(annotation: dict) -> dict:
    """La même annotation au contrat v1 : version 1, sans les champs ajoutés en v2."""
    d = copy.deepcopy(annotation)
    d["version"] = 1
    for etiquette in d.get("etiquettes", []):
        meta = etiquette.get("meta")
        if isinstance(meta, dict):
            meta.pop("partition", None)
            meta.pop("alternative", None)
            attachement = meta.get("attachement")
            if isinstance(attachement, dict):
                attachement.pop("candidats", None)
    return d


def _mutation_candidat_chaine(annotation: dict) -> dict | None:
    d = copy.deepcopy(annotation)
    for etiquette in d.get("etiquettes", []):
        attachement = ((etiquette.get("meta") or {}).get("attachement") or {})
        candidats = attachement.get("candidats")
        if candidats:
            candidats[0] = "« une chaîne d'affichage »"
            return d
    return None


def _mutation_candidat_sans_span(annotation: dict) -> dict | None:
    d = copy.deepcopy(annotation)
    for etiquette in d.get("etiquettes", []):
        attachement = ((etiquette.get("meta") or {}).get("attachement") or {})
        candidats = attachement.get("candidats")
        if candidats:
            candidats[0].pop("span", None)
            return d
    return None


def mesurer() -> dict:
    import fastjsonschema

    sys.path.insert(0, str(RACINE))
    import tools.bloc_linguistique as bl
    from tools.roles_vocabulaire import (CORRESPONDANCES, ROLES, TABLE,
                                         RoleHorsVocabulaire, normaliser_role)
    from tools.tests.linguistique.evaluer_gold import charger

    schemas = {v: json.loads((RACINE / "tools" / "schemas" /
                              f"drave-annotation-v{v}.json").read_text(encoding="utf-8"))
               for v in (1, 2)}
    valideurs = {v: fastjsonschema.compile(s) for v, s in schemas.items()}

    h = bl.Heuristique()
    phrases = charger()
    anns = [h.analyser(p["texte"], p["langue"]).json() for p in phrases]

    echecs_v2 = [p["id"] for p, a in zip(phrases, anns) if not _valide(valideurs[2], a)]
    v1_anns = [_downgrade_v1(a) for a in anns]
    echecs_v1 = [p["id"] for p, a in zip(phrases, v1_anns) if not _valide(valideurs[1], a)]

    bruts = collections.Counter()
    normalises = collections.Counter()
    roles_non_vides = 0
    bruts_hors_table: list[str] = []
    roles_hors_vocabulaire: list[str] = []
    segments = 0
    types_par_role: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)

    attachements = attachements_avec_objets = 0
    objets = objets_alternatives = 0
    spans_faux = 0
    cible_choisie_presente = 0
    tailles: list[int] = []
    for p, a in zip(phrases, anns):
        interne = h.analyser(p["texte"], p["langue"])
        bruts_interne = {(e.debut, e.fin, e.type): (e.meta or {}).get("role", "")
                         for e in interne.etiquettes if e.niveau == "syntagme"}
        texte = a["texte"]
        for etiquette in a["etiquettes"]:
            if etiquette["niveau"] != "syntagme":
                continue
            segments += 1
            role = (etiquette.get("meta") or {}).get("role", "")
            if role:
                roles_non_vides += 1
                normalises[role] += 1
                types_par_role[role][etiquette["type"]] += 1
                if role not in ROLES:
                    roles_hors_vocabulaire.append(role)
            brut = bruts_interne.get((etiquette["debut"], etiquette["fin"], etiquette["type"]), "")
            if brut:
                bruts[brut] += 1
                if brut.casefold() not in CORRESPONDANCES:
                    bruts_hors_table.append(brut)
            attachement = (etiquette.get("meta") or {}).get("attachement")
            if attachement:
                attachements += 1
                candidats = attachement.get("candidats") or []
                tailles.append(len(candidats))
                if candidats:
                    attachements_avec_objets += 1
                if any(c.get("cible") == attachement.get("cible") for c in candidats):
                    cible_choisie_presente += 1
                for candidat in candidats:
                    objets += 1
                    debut = candidat["span"]["debut"]
                    fin = candidat["span"]["fin"]
                    if texte[debut:fin] != candidat["cible"]:
                        spans_faux += 1
            for alternative in (etiquette.get("meta") or {}).get("alternative", []) or []:
                for candidat in ((alternative.get("attachement") or {}).get("candidats") or []):
                    objets_alternatives += 1
                    debut = candidat["span"]["debut"]
                    fin = candidat["span"]["fin"]
                    if texte[debut:fin] != candidat["cible"]:
                        spans_faux += 1

    # Contrôles négatifs.
    filtre_predicat = [e for a in anns for e in a["etiquettes"]
                       if e["niveau"] == "syntagme"
                       and (e.get("meta") or {}).get("role") == "predicat"]
    filtre_predicat_accentue = [e for a in anns for e in a["etiquettes"]
                                if e["niveau"] == "syntagme"
                                and (e.get("meta") or {}).get("role") == "prédicat"]
    try:
        normaliser_role("role_invente")
        role_inconnu_leve = False
        role_inconnu_message = ""
    except RoleHorsVocabulaire as exc:
        role_inconnu_leve = True
        role_inconnu_message = str(exc)

    mutation_chaine = _mutation_candidat_chaine(anns[0])
    mutation_sans_span = _mutation_candidat_sans_span(anns[0])
    candidat_chaine_refuse = bool(mutation_chaine) and not _valide(valideurs[2], mutation_chaine)
    candidat_sans_span_refuse = bool(mutation_sans_span) and not _valide(valideurs[2],
                                                                        mutation_sans_span)

    # Le vérificateur public et les tests produit.
    verif = subprocess.run([sys.executable, str(RACINE / "tools" / "verifier_schema_produit.py"),
                            "--json"], cwd=str(RACINE), text=True, capture_output=True)
    verif_d = json.loads(verif.stdout)
    test_produit = subprocess.run([sys.executable,
                                   str(RACINE / "tools" / "tests" / "test_produit.py")],
                                  cwd=str(RACINE), text=True, capture_output=True)
    test_schema = subprocess.run([sys.executable,
                                  str(RACINE / "tools" / "tests" / "test_schema_produit.py")],
                                 cwd=str(RACINE), text=True, capture_output=True)

    return {
        "date": "2026-11-15",
        "tache": "T2",
        "ligne": "B13",
        "objet": "l'API du JSON : candidats d'attachement en objets et rôles normalisés",
        "outil": "tools/mesurer_contrat_json.py",
        "corpus": {
            "nom": "gold vivant (hand + reel + synthétique)",
            "phrases": len(phrases),
            "segments": segments,
            "roles_non_vides": roles_non_vides,
        },
        "schema": {
            "v2": "tools/schemas/drave-annotation-v2.json",
            "v1": "tools/schemas/drave-annotation-v1.json",
            "champ_ajoute": "meta.attachement.candidats",
            "forme_candidat": ["span", "cible", "source"],
            "forme_span": ["debut", "fin"],
            "role_enum": list(ROLES),
            "v1_lue": not echecs_v1,
        },
        "vocabulaire_roles": {
            "roles": list(ROLES),
            "table": [dict(ligne) for ligne in TABLE],
            "bruts_observes": dict(sorted(bruts.items())),
            "bruts_distincts": len(bruts),
            "bruts_hors_table": sorted(set(bruts_hors_table)),
            "normalises_observes": dict(sorted(normalises.items())),
            "normalises_distincts": len(normalises),
            "roles_hors_vocabulaire": sorted(set(roles_hors_vocabulaire)),
            "types_par_role": {role: dict(sorted(comptes.items()))
                               for role, comptes in sorted(types_par_role.items())},
        },
        "candidats": {
            "attachements": attachements,
            "attachements_avec_objets": attachements_avec_objets,
            "attachements_sans_objet": attachements - attachements_avec_objets,
            "objets": objets,
            "objets_alternatives": objets_alternatives,
            "taille_moyenne": round(sum(tailles) / max(1, len(tailles)), 4),
            "cible_choisie_presente": cible_choisie_presente,
            "spans_faux": spans_faux,
        },
        "controles_negatifs": {
            "filtre_predicat": {
                "role": "predicat",
                "segments": len(filtre_predicat),
                "gv": sum(1 for e in filtre_predicat if e["type"] == "GV"),
                "verdict": "trouve" if filtre_predicat else "vide",
            },
            "filtre_predicat_accentue": {
                "role": "prédicat",
                "segments": len(filtre_predicat_accentue),
                "verdict": "vide" if not filtre_predicat_accentue else "trouve",
            },
            "role_inconnu_leve": role_inconnu_leve,
            "role_inconnu_message": role_inconnu_message,
            "candidat_chaine_refuse": candidat_chaine_refuse,
            "candidat_sans_span_refuse": candidat_sans_span_refuse,
            "v2_refuse_v1": verif_d["retrocompatibilite"]["v2_refuse_v1"],
            "v1_lue": verif_d["retrocompatibilite"]["v1_lue"],
            "role_schema_refuse": verif_d["controles_negatifs"]["role_hors_vocabulaire"],
            "candidat_chaine_schema_refuse": verif_d["controles_negatifs"]["candidat_chaine"],
        },
        "validation": {
            "v2_annotations": len(anns),
            "v2_echecs": len(echecs_v2),
            "v1_annotations": len(v1_anns),
            "v1_echecs": len(echecs_v1),
            "v2_refuse_v1": sum(1 for a in v1_anns if not _valide(valideurs[2], a)),
        },
        "tests": {
            "test_produit": {"code": test_produit.returncode,
                             "tests": _ran(test_produit.stderr),
                             "echecs": 0 if test_produit.returncode == 0 else 1},
            "test_schema_produit": {"code": test_schema.returncode,
                                    "tests": _ran(test_schema.stderr),
                                    "echecs": 0 if test_schema.returncode == 0 else 1},
        },
        "limites": [
            "la normalisation n'est pas une annotation plus fine : objet regroupe patient, "
            "complément, thème, contenu et groupe nominal sans fonction ; qualite regroupe "
            "attribut, manière, cause, concession et hypothèse",
            "le span d'un candidat est la première occurrence de la cible dans le texte ; "
            "pour une surface répétée, c'est une position, pas une résolution d'anaphore",
            "les candidats restent produits par l'heuristique : source vaut heuristique, "
            "même quand la cible vient du générateur S",
            "le gold 612 n'exerce pas les rôles instrument, manière, source, conséquence ; "
            "ils sont dans la table mais non observés sur ce corpus",
            "v1 est lue par son schéma, mais les annotations v1 sont dérivées des v2 : ce "
            "n'est pas un corpus v1 indépendant",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Mesure T2 du contrat JSON.")
    ap.add_argument("--json", action="store_true", help="imprime le JSON sur stdout")
    ap.add_argument("--sortie", type=pathlib.Path, default=SORTIE,
                    help=f"chemin d'écriture (défaut : {SORTIE})")
    args = ap.parse_args()
    resultat = mesurer()
    texte = json.dumps(resultat, ensure_ascii=False, indent=1)
    if args.json:
        print(texte)
    else:
        args.sortie.parent.mkdir(parents=True, exist_ok=True)
        args.sortie.write_text(texte + "\n", encoding="utf-8")
        c = resultat["candidats"]
        v = resultat["vocabulaire_roles"]
        n = resultat["controles_negatifs"]
        print(f"  phrases {resultat['corpus']['phrases']} · segments {resultat['corpus']['segments']} "
              f"· rôles {resultat['corpus']['roles_non_vides']}")
        print(f"  candidats : {c['objets']} objets ({c['attachements_avec_objets']}/{c['attachements']} "
              f"attachements) · spans faux {c['spans_faux']}")
        print(f"  rôles : {v['bruts_distincts']} bruts → {v['normalises_distincts']} normalisés · "
              f"hors table {len(v['bruts_hors_table'])} · hors vocabulaire "
              f"{len(v['roles_hors_vocabulaire'])}")
        print(f"  contrôle négatif : filtre predicat {n['filtre_predicat']['segments']} "
              f"({n['filtre_predicat']['gv']} GV) · prédicat accentué "
              f"{n['filtre_predicat_accentue']['segments']} · rôle inconnu levé "
              f"{n['role_inconnu_leve']}")
        print(f"  validation : v2 {resultat['validation']['v2_echecs']} échec(s), "
              f"v1 {resultat['validation']['v1_echecs']} échec(s)")
        print(f"  écrit : {args.sortie}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
