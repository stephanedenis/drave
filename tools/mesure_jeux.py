#!/usr/bin/env python3
"""mesure_jeux.py — le pilote du banc des jeux symboliques.

    python3 tools/mesure_jeux.py --rapide          # la porte (contrôles courts)
    python3 tools/mesure_jeux.py --json reports/jeux-mesures.json

Le module est `tools/jeux/mesure.py` ; ce pilote ne fait que rendre l'appel
possible sans `PYTHONPATH` (le dépôt lance ses outils depuis la racine).
"""
from __future__ import annotations

import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(RACINE))

from jeux.mesure import principal  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(principal())
