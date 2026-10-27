#!/usr/bin/env python3
"""hybride.py — le codec d'abord, la mémoire ensuite, le natif en secours.

Le codec classique lit les surfaces de jeux à 100 % sur B5/B7. On mesure ici
deux blocs **déterministes** qui ne dépendent pas du natif :

- **lecture** : surface → RSN exacte, couverture et exactitude ;
- **traduction** : surface source → RSN → surface cible, par mémoire parallèle
  (même paire, autre langue) ; c'est une mémoire, pas un modèle, et on le dit.
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from jeux.codecs import codec  # noqa: E402
from semantique.typed_corpus import items  # noqa: E402


def main() -> int:
    its = items()
    lecture = 0
    par_jeu = collections.Counter()
    # ItemType n'a pas l'attendu : on relit le corpus source pour la vérité et le contexte.
    from jeux.corpus import construire_corpus
    from jeux.corpus_multilingue import construire_corpus_multilingue
    vrais = {}
    for c in (construire_corpus(), construire_corpus_multilingue()):
        for it in c.items:
            if it.attendu.nature == "coup":
                vrais[(it.texte, it.jeu, it.paire, it.langue)] = (it.attendu, it.contexte)
    for it in its:
        paire = vrais.get((it.texte, it.jeu, it.paire, it.langue))
        if paire is None:
            continue
        r, contexte = paire
        try:
            lec = codec(it.jeu).lit(it.texte, niveau=4, contexte=contexte)
        except Exception:
            continue
        if lec and lec.rsn and lec.rsn.corps == r.corps:
            lecture += 1
            par_jeu[it.jeu] += 1
    # mémoire de traduction : même paire, langue cible
    memo = collections.defaultdict(dict)
    for it in its:
        if it.paire:
            memo[it.paire][it.langue] = it.texte
    trad_ok = 0
    trad_n = 0
    for it in its:
        cible = "en" if it.langue != "en" else "fr"
        t = memo.get(it.paire, {}).get(cible)
        if not t:
            continue
        trad_n += 1
        if t.strip().lower() != it.texte.strip().lower():
            trad_ok += 1  # la cible existe et est une autre surface
    resultat = {
        "items": len(its),
        "lecture_codec": lecture,
        "lecture_couverture": lecture / max(1, len(its)),
        "par_jeu": dict(par_jeu),
        "memoire_traduction": {"cibles": trad_n, "autres_surfaces": trad_ok,
                               "note": "mémoire parallèle, pas un modèle"},
    }
    pathlib.Path("/tmp/hybride.json").write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(resultat, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
