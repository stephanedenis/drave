#!/usr/bin/env python3
"""verifier_performance_fix.py — le contrôle négatif de U1, rejouable.

U1 a remplacé des boucles O(k²) par des index (bloc linguistique et générateur S) **sans
changer les sorties**. Ce script le vérifie de deux façons :

1. `--sortie DIR` écrit les annotations **canoniques** (JSON trié, sans durée) du préfixe
   de 10 000 mots, du bloc contrôlé T4 répété ×1…×40, et des 612 phrases du gold (dont les
   452 réelles) ;
2. `--comparer AVANT APRÈS` compare deux répertoires produits ainsi : chaque fichier doit
   être identique **octet pour octet** (le diff est vide), et le script affiche les sha256.

    PYTHONHASHSEED=0 python3 tools/verifier_performance_fix.py --sortie /tmp/u1-apres
    python3 tools/verifier_performance_fix.py --comparer /tmp/u1-avant /tmp/u1-apres

Le résultat attendu est `10/10 identiques` et un code 0. Une seule différence rend le code 1.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "tools"))

import banc_performance as bp  # noqa: E402
import bloc_linguistique as bl  # noqa: E402

BLOCS = (1, 2, 4, 8, 16, 32, 40)
FICHIERS = (["corpus-10000.json"]
            + [f"bloc-x{k}.json" for k in BLOCS]
            + ["gold-annotations-612.json", "gold-annotations-452.json"])


def _canon(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _charger_gold() -> list[dict]:
    chemin = RACINE / "tools" / "tests" / "linguistique" / "evaluer_gold.py"
    spec = importlib.util.spec_from_file_location("evaluer_gold_u1", chemin)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.charger()


def _sha256(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def generer(sortie: pathlib.Path) -> int:
    """Écrit les annotations canoniques ; rend le nombre de fichiers écrits."""
    sortie.mkdir(parents=True, exist_ok=True)
    source = (RACINE / "data" / "corpus_fr_litterature.txt").read_text(encoding="utf-8")
    texte, mots = bp._prefixe_mots(source, 10000)
    assert mots == 10000, mots
    h = bl.Heuristique()

    a = h.analyser(texte, "fr")
    (sortie / "corpus-10000.json").write_text(_canon(a.json()), encoding="utf-8")

    bloc, _debut, _fin = bp._bloc_phrases(texte, 250)
    for k in BLOCS:
        t = "\n\n".join([bloc] * k)
        (sortie / f"bloc-x{k}.json").write_text(_canon(h.analyser(t, "fr").json()),
                                                encoding="utf-8")

    phrases = _charger_gold()
    rows = []
    for p in phrases:
        a = h.analyser(p["texte"], p["langue"])
        rows.append({"id": p.get("id"), "source": p.get("source"), "texte": p["texte"],
                     "langue": p["langue"], "annotation": a.json()})
    (sortie / "gold-annotations-612.json").write_text(_canon(rows), encoding="utf-8")
    reel = [r for r in rows if r["source"] in ("hand", "reel")]
    (sortie / "gold-annotations-452.json").write_text(_canon(reel), encoding="utf-8")
    print(f"{len(FICHIERS)} fichiers écrits dans {sortie}")
    return 0


def comparer(avant: pathlib.Path, apres: pathlib.Path) -> int:
    """Compare les fichiers canoniques ; rend 0 si le diff est vide."""
    manquants = [nom for nom in FICHIERS
                 if not (avant / nom).is_file() or not (apres / nom).is_file()]
    if manquants:
        print("fichiers manquants : " + ", ".join(manquants), file=sys.stderr)
        return 2
    identiques = 0
    for nom in FICHIERS:
        a, b = avant / nom, apres / nom
        ha, hb = _sha256(a), _sha256(b)
        same = ha == hb
        identiques += int(same)
        etat = "identique" if same else "DIFF"
        print(f"{etat:9s} {nom:28s} {a.stat().st_size:>9d} octets  {ha[:16]}")
        if not same:
            print(f"  avant {ha}\n  après {hb}", file=sys.stderr)
    print(f"{identiques}/{len(FICHIERS)} identiques — "
          + ("diff vide" if identiques == len(FICHIERS) else "diff non vide"))
    return 0 if identiques == len(FICHIERS) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sortie", default="", help="répertoire où écrire les annotations canoniques")
    ap.add_argument("--comparer", nargs=2, metavar=("AVANT", "APRES"), default=None,
                    help="compare deux répertoires produits par --sortie")
    args = ap.parse_args()
    if args.sortie and args.comparer:
        ap.error("choisir --sortie ou --comparer, pas les deux")
    if args.sortie:
        return generer(pathlib.Path(args.sortie))
    if args.comparer:
        return comparer(pathlib.Path(args.comparer[0]), pathlib.Path(args.comparer[1]))
    ap.error("il faut --sortie DIR ou --comparer AVANT APRES")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
