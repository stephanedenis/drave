#!/usr/bin/env python3
"""mesure_maitres.py — le pilote de la mesure des principes des maîtres."""
import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from jeux.mesure_maitres import mesure_maitres


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--complet", action="store_true")
    ap.add_argument("--rapide", action="store_true")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    resultat = mesure_maitres(rapide=args.rapide and not args.complet)
    if args.json:
        pathlib.Path(args.json).write_text(
            json.dumps(resultat, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(resultat, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
