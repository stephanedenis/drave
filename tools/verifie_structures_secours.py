#!/usr/bin/env python3
"""verifie_structures_secours.py — la copie CI de S est-elle identique au sous-module ?

`tools/structures` est un sous-module dont l'URL est un chemin local : GitHub Actions ne peut
pas le récupérer. La CI utilise donc une copie de secours dans `.github/ci/structures/`.
Ce vérificateur compare les deux copies **quand le sous-module est présent** (le poste de
développement), et sort en :

- **0** : identiques ;
- **1** : dérive (nommer le fichier et les deux sha256) ;
- **2** : sous-module absent, rien à comparer (la copie de secours est la seule source).

Usage : `python3 tools/verifie_structures_secours.py`
"""
from __future__ import annotations

import hashlib
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parents[1]
PAIRES = (
    ("tools/structures/generateur.py", ".github/ci/structures/generateur.py"),
    ("tools/structures/donnees/gold-analyseur.json",
     ".github/ci/structures/donnees/gold-analyseur.json"),
)


def sha256(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def main() -> int:
    absentes = [source for source, _ in PAIRES if not (RACINE / source).is_file()]
    if absentes:
        print("sous-module absent : rien à comparer")
        for source in absentes:
            print(f"  · {source} manque")
        return 2
    ko = 0
    for source, secours in PAIRES:
        a = sha256(RACINE / source)
        b = sha256(RACINE / secours)
        if a == b:
            print(f"✅ {source} ≡ {secours} · {a[:12]}…")
        else:
            ko = 1
            print(f"❌ {source} ≠ {secours}")
            print(f"   source  {a}")
            print(f"   secours {b}")
    if ko:
        print("→ mettre la copie à jour : cp <source> <secours> "
              "(voir .github/ci/structures/README.md)")
    return ko


if __name__ == "__main__":
    raise SystemExit(main())
