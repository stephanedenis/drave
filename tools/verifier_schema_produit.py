#!/usr/bin/env python3
"""verifier_schema_produit.py — valide une annotation `drave.annotation` contre le schéma de sa version.

Deux schémas sont publiés (Draft 2020-12) :

- `tools/schemas/drave-annotation-v1.json` — le contrat d'origine (version 1) ;
- `tools/schemas/drave-annotation-v2.json` — le contrat courant (version 2) : il ajoute
  `meta.partition` et `meta.alternative`, les deux champs qui documentent les syntagmes qui se
  chevauchent, les **candidats d'attachement structurés** (`meta.attachement.candidats`,
  objets `{span, cible, source}`) et les **rôles normalisés** (vocabulaire fermé).

Le vérificateur lit `version` dans l'annotation et choisit le schéma correspondant : une
annotation v1 reste donc **lue** et validée par le schéma v1. Il compile les schémas une fois,
puis valide les annotations de cas choisis : français, anglais, refus (texte vide), entrée non
textuelle, texte très long, plus une annotation v1 de rétro-compatibilité. Il ne dépend que de
`fastjsonschema` (sinon il se rabat sur une validation minimale des champs obligatoires et de la
version). Un **contrôle négatif** vérifie que le schéma v2 refuse bien une annotation v1.

Usage :
    python3 tools/verifier_schema_produit.py              # 5 cas v2 + 1 cas v1, sortie 0/1
    python3 tools/verifier_schema_produit.py --json       # le détail des cas
    python3 tools/verifier_schema_produit.py --gold 20    # + 20 phrases du gold
    python3 tools/verifier_schema_produit.py --aide
"""
from __future__ import annotations

import argparse
import copy
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parents[1]
SCHEMAS = {
    1: RACINE / "tools" / "schemas" / "drave-annotation-v1.json",
    2: RACINE / "tools" / "schemas" / "drave-annotation-v2.json",
}
OBLIGATOIRES = ("schema", "version", "texte", "langue", "script", "refus",
                "etiquettes", "unites_semantiques")

try:  # script : `python3 tools/verifier_schema_produit.py`
    from roles_vocabulaire import ROLES as ROLES_VOCABULAIRES
except ImportError:  # paquet : `python3 -m tools.verifier_schema_produit`
    from tools.roles_vocabulaire import ROLES as ROLES_VOCABULAIRES

CAS = [
    ("fr", "Le chat de la voisine qui dort sur le toit se réveille.", "fr"),
    ("en", "The cat that sleeps on the roof is black.", "en"),
    ("vide", "", "fr"),
    ("ponctuation", "!!! ???", "fr"),
    ("long", "Le chat dort. " * 40, "fr"),
]


def _annotations() -> list[tuple[str, dict]]:
    sys.path.insert(0, str(RACINE))
    import tools.bloc_linguistique as bl
    h = bl.Heuristique()
    cas = [(nom, h.analyser(texte, langue).json()) for nom, texte, langue in CAS]
    # Rétro-compatibilité : la même annotation, ramenée au contrat v1 (sans les deux champs
    # ajoutés en v2). Le vérificateur doit la lire avec le schéma v1, pas avec le v2.
    v1 = copy.deepcopy(cas[0][1])
    v1["version"] = 1
    for etiquette in v1["etiquettes"]:
        meta = etiquette.get("meta")
        if isinstance(meta, dict):
            meta.pop("partition", None)
            meta.pop("alternative", None)
            # `meta.attachement.candidats` est un champ v2 : le cas v1 ne doit pas le
            # porter, sinon la rétro-compatibilité testerait un JSON qui n'existe pas.
            attachement = meta.get("attachement")
            if isinstance(attachement, dict):
                attachement.pop("candidats", None)
    cas.append(("v1", v1))
    return cas


def _valider_minimal(d: dict, version: int) -> list[str]:
    erreurs = [f"champ obligatoire absent : {k}" for k in OBLIGATOIRES if k not in d]
    if d.get("schema") != "drave.annotation":
        erreurs.append(f"schema inattendu : {d.get('schema')!r}")
    if d.get("version") != version:
        erreurs.append(f"version inattendue : {d.get('version')!r} (attendu {version})")
    for e in d.get("etiquettes", []):
        for k in ("niveau", "type", "valeur", "debut", "fin", "source", "confiance"):
            if k not in e:
                erreurs.append(f"étiquette sans {k} : {e!r}")
                break
        meta = e.get("meta") or {}
        role = meta.get("role")
        if role and role not in ROLES_VOCABULAIRES:
            erreurs.append(f"rôle hors vocabulaire : {role!r}")
        _valider_attachement_minimal(meta.get("attachement"), erreurs, e.get("valeur", ""))
        for alternative in meta.get("alternative", []) or []:
            role = (alternative or {}).get("role")
            if role and role not in ROLES_VOCABULAIRES:
                erreurs.append(f"rôle d'alternative hors vocabulaire : {role!r}")
            _valider_attachement_minimal((alternative or {}).get("attachement"), erreurs,
                                         e.get("valeur", ""))
    return erreurs


def _valider_attachement_minimal(attachement: dict | None, erreurs: list[str],
                                 etiquette: str) -> None:
    """Le repli sans `fastjsonschema` : le champ v2 des candidats reste typé."""
    if not isinstance(attachement, dict):
        return
    candidats = attachement.get("candidats")
    if candidats is None:
        return
    if not isinstance(candidats, list):
        erreurs.append(f"candidats non listés ({etiquette})")
        return
    for candidat in candidats:
        if not isinstance(candidat, dict):
            erreurs.append(f"candidat non objet ({etiquette})")
            continue
        span = candidat.get("span")
        if (not isinstance(span, dict) or "debut" not in span or "fin" not in span
                or not isinstance(candidat.get("cible"), str)
                or candidat.get("source") not in ("heuristique", "neuronal", "humain")):
            erreurs.append(f"candidat incomplet ({etiquette})")


def _gold(n: int) -> list[tuple[str, dict]]:
    """Les `n` premières phrases du gold, analysées par l'heuristique (validation du corpus)."""
    sys.path.insert(0, str(RACINE))
    from tools.tests.linguistique.evaluer_gold import charger
    import tools.bloc_linguistique as bl
    h = bl.Heuristique()
    return [(f"gold:{p['id']}", h.analyser(p["texte"], p["langue"]).json())
            for p in charger()[:max(0, n)]]


def _valider(annotation: dict, version: int, valideurs: dict[int, object]) -> list[str]:
    valideur = valideurs.get(version)
    if valideur is not None:
        try:
            valideur(annotation)
            return []
        except Exception as exc:  # noqa: BLE001
            return [str(exc)[:240]]
    return _valider_minimal(annotation, version)


def _controle_negatif(annotation_v1: dict, valideurs: dict[int, object]) -> bool:
    """Le schéma v2 doit refuser une annotation v1 (et le schéma v1 doit l'accepter)."""
    return bool(_valider(annotation_v1, 2, valideurs))


def _controle_negatif_role(annotation: dict, valideurs: dict[int, object]) -> bool:
    """Un rôle hors vocabulaire (`prédicat` accentué, l'ancienne forme) est refusé par v2."""
    mutation = copy.deepcopy(annotation)
    for etiquette in mutation.get("etiquettes", []):
        meta = etiquette.get("meta")
        if isinstance(meta, dict) and meta.get("role"):
            meta["role"] = "prédicat"
            return bool(_valider(mutation, 2, valideurs))
    return False


def _controle_negatif_candidats(annotation: dict, valideurs: dict[int, object]) -> bool:
    """Un candidat qui redevient une chaîne est refusé par v2 (le champ est typé)."""
    mutation = copy.deepcopy(annotation)
    for etiquette in mutation.get("etiquettes", []):
        attachement = ((etiquette.get("meta") or {}).get("attachement") or {})
        candidats = attachement.get("candidats")
        if candidats:
            candidats[0] = "chaîne d'affichage"
            return bool(_valider(mutation, 2, valideurs))
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description="Valide drave.annotation contre le schéma de sa version.")
    ap.add_argument("--json", action="store_true", help="détail JSON des cas")
    ap.add_argument("--gold", type=int, default=0, metavar="N",
                    help="valide aussi les N premières phrases du gold (0 = aucune)")
    ap.add_argument("--aide", action="store_true", help="affiche cette aide et sort")
    args = ap.parse_args()
    if args.aide:
        ap.print_help()
        return 0
    schemas: dict[int, dict] = {}
    for version, chemin in SCHEMAS.items():
        if not chemin.is_file():
            print(f"  ❌ schéma v{version} absent : {chemin}", file=sys.stderr)
            return 1
        schemas[version] = json.loads(chemin.read_text(encoding="utf-8"))
    valideurs: dict[int, object] = {}
    try:
        import fastjsonschema
        valideurs = {v: fastjsonschema.compile(s) for v, s in schemas.items()}
    except Exception:  # noqa: BLE001 — repli minimal si le validateur manque
        valideurs = {}
    cas = list(_annotations())
    if args.gold > 0:
        cas += _gold(args.gold)
    resultats = []
    for nom, annotation in cas:
        version = annotation.get("version")
        if version not in schemas:
            erreurs = [f"version inconnue : {version!r}"]
        else:
            erreurs = _valider(annotation, version, valideurs)
        resultats.append({"cas": nom, "version": version, "ok": not erreurs,
                          "erreurs": erreurs})
    annotation_v1 = next(a for _, a in cas if a.get("version") == 1)
    annotation_v2 = next(a for _, a in cas if a.get("version") == 2)
    retro_ok = not _valider(annotation_v1, 1, valideurs)
    negatif_ok = _controle_negatif(annotation_v1, valideurs)
    role_negatif_ok = _controle_negatif_role(annotation_v2, valideurs)
    candidats_negatif_ok = _controle_negatif_candidats(annotation_v2, valideurs)
    if args.json:
        print(json.dumps({
            "schemas": {str(v): str(p) for v, p in SCHEMAS.items()},
            "versions_lues": sorted(schemas),
            "validateur": bool(valideurs),
            "retrocompatibilite": {"v1_lue": retro_ok, "v2_refuse_v1": negatif_ok},
            "controles_negatifs": {"role_hors_vocabulaire": role_negatif_ok,
                                   "candidat_chaine": candidats_negatif_ok},
            "cas": resultats,
        }, ensure_ascii=False, indent=1))
    else:
        for r in resultats:
            print(f"  {'✅' if r['ok'] else '❌'} {r['cas']} (v{r['version']})"
                  + (f" — {r['erreurs'][0]}" if r["erreurs"] else ""))
        print(f"  {'✅' if retro_ok else '❌'} rétro-compatibilité : annotation v1 lue par le schéma v1")
        print(f"  {'✅' if negatif_ok else '❌'} contrôle négatif : le schéma v2 refuse une annotation v1")
        print(f"  {'✅' if role_negatif_ok else '❌'} contrôle négatif : le schéma v2 refuse un rôle hors vocabulaire")
        print(f"  {'✅' if candidats_negatif_ok else '❌'} contrôle négatif : le schéma v2 refuse un candidat chaîne")
        print(f"  {'✅ validateur JSON Schema' if valideurs else '⚠️ validation minimale (fastjsonschema absent)'}"
              f" · {len(cas)} cas")

    return 0 if (all(r["ok"] for r in resultats) and retro_ok and negatif_ok
                 and role_negatif_ok and candidats_negatif_ok) else 1


if __name__ == "__main__":
    raise SystemExit(main())
