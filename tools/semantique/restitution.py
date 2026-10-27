#!/usr/bin/env python3
"""restitution.py — la surface canonique, et son aller-retour RSN.

Le codec classique rend une RSN dans un format canonique par jeu. On mesure
deux choses : le rendu réussit, et la surface rendue se relit en **la même RSN**.
C'est la restitution **déterministe** ; elle ne dépend pas du natif.
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from jeux.corpus import construire_corpus  # noqa: E402
from jeux.corpus_multilingue import construire_corpus_multilingue  # noqa: E402
from jeux.codecs import codec  # noqa: E402

FORMATS = {"morpion": "cellule", "echecs": "san", "dames": "numerique",
           "go": "gtp", "cartes": "carte"}


def main() -> int:
    resultat = {}
    for nom, corpus in (("B5", construire_corpus()), ("B7", construire_corpus_multilingue())):
        total = rendu = roundtrip = 0
        erreurs = collections.Counter()
        for it in corpus.items:
            if it.attendu.nature != "coup":
                continue
            total += 1
            try:
                lec = codec(it.jeu).lit(it.texte, niveau=4, contexte=it.contexte)
                if not (lec and lec.rsn and lec.rsn.corps == it.attendu.corps):
                    erreurs["lecture"] += 1
                    continue
                fmt = FORMATS[it.jeu]
                surface = codec(it.jeu).rend(lec.rsn, format=fmt, contexte=it.contexte)
                rendu += 1
                relu = codec(it.jeu).lit(surface, niveau=4, contexte=it.contexte)
                if relu and relu.rsn and relu.rsn.corps == lec.rsn.corps:
                    roundtrip += 1
                else:
                    erreurs["relecture"] += 1
            except Exception as e:
                erreurs[type(e).__name__] += 1
        resultat[nom] = {"total": total, "rendu": rendu, "roundtrip": roundtrip,
                         "erreurs": dict(erreurs)}
    pathlib.Path("/tmp/restitution.json").write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(resultat, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
