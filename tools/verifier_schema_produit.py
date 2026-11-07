#!/usr/bin/env python3
"""verifier_schema_produit.py — valide une annotation `drave.annotation` contre le schéma v1.

Le schéma publié est `tools/schemas/drave-annotation-v1.json` (Draft 2020-12). Ce vérificateur compile le
schéma une fois, puis valide les annotations de cas choisis : français, anglais, refus (texte
vide), entrée non textuelle, texte très long. Il ne dépend que de `fastjsonschema` (sinon il se
rabat sur une validation minimale des 8 champs obligatoires).

Usage :
    python3 tools/verifier_schema_produit.py              # 5 cas, sortie 0/1
    python3 tools/verifier_schema_produit.py --json       # le détail des cas
    python3 tools/verifier_schema_produit.py --aide
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parents[1]
SCHEMA = RACINE / "tools" / "schemas" / "drave-annotation-v1.json"
OBLIGATOIRES = ("schema", "version", "texte", "langue", "script", "refus",
                "etiquettes", "unites_semantiques")

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
    return [(nom, h.analyser(texte, langue).json()) for nom, texte, langue in CAS]


def _valider_minimal(d: dict) -> list[str]:
    erreurs = [f"champ obligatoire absent : {k}" for k in OBLIGATOIRES if k not in d]
    if d.get("schema") != "drave.annotation":
        erreurs.append(f"schema inattendu : {d.get('schema')!r}")
    if d.get("version") != 1:
        erreurs.append(f"version inattendue : {d.get('version')!r}")
    for e in d.get("etiquettes", []):
        for k in ("niveau", "type", "valeur", "debut", "fin", "source", "confiance"):
            if k not in e:
                erreurs.append(f"étiquette sans {k} : {e!r}")
                break
    return erreurs


def _gold(n: int) -> list[tuple[str, dict]]:
    """Les `n` premières phrases du gold, analysées par l'heuristique (validation du corpus)."""
    sys.path.insert(0, str(RACINE))
    from tools.tests.linguistique.evaluer_gold import charger
    import tools.bloc_linguistique as bl
    h = bl.Heuristique()
    return [(f"gold:{p['id']}", h.analyser(p["texte"], p["langue"]).json())
            for p in charger()[:max(0, n)]]


def main() -> int:
    ap = argparse.ArgumentParser(description="Valide drave.annotation contre le schéma v1.")
    ap.add_argument("--json", action="store_true", help="détail JSON des cas")
    ap.add_argument("--gold", type=int, default=0, metavar="N",
                    help="valide aussi les N premières phrases du gold (0 = aucune)")
    ap.add_argument("--aide", action="store_true", help="affiche cette aide et sort")
    args = ap.parse_args()
    if args.aide:
        ap.print_help()
        return 0
    if not SCHEMA.is_file():
        print(f"  ❌ schéma absent : {SCHEMA}", file=sys.stderr)
        return 1
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    valider = None
    try:
        import fastjsonschema
        valider = fastjsonschema.compile(schema)
    except Exception:  # noqa: BLE001 — repli minimal si le validateur manque
        valider = None
    cas = list(_annotations())
    if args.gold > 0:
        cas += _gold(args.gold)
    resultats = []
    for nom, annotation in cas:
        if valider is not None:
            try:
                valider(annotation)
                erreurs = []
            except Exception as exc:  # noqa: BLE001
                erreurs = [str(exc)[:240]]
        else:
            erreurs = _valider_minimal(annotation)
        resultats.append({"cas": nom, "ok": not erreurs, "erreurs": erreurs})
    if args.json:
        print(json.dumps({"schema": str(SCHEMA), "validateur": bool(valider),
                          "cas": resultats}, ensure_ascii=False, indent=1))
    else:
        for r in resultats:
            print(f"  {'✅' if r['ok'] else '❌'} {r['cas']}"
                  + (f" — {r['erreurs'][0]}" if r["erreurs"] else ""))
        print(f"  {'✅ validateur JSON Schema' if valider else '⚠️ validation minimale (fastjsonschema absent)'}"
              f" · {len(cas)} cas")

    return 0 if all(r["ok"] for r in resultats) else 1


if __name__ == "__main__":
    raise SystemExit(main())
