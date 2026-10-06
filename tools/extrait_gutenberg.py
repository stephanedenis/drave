#!/usr/bin/env python3
"""extrait_gutenberg.py — sortir des SEGMENTS PARALLÈLES d'œuvres alignables.

Un grand corpus monolingue ne permet pas de mesurer l'invariance inter-langue :
il faut du contenu APPARIÉ. Les œuvres traduites de Gutenberg en fournissent, à
condition de trouver un découpage commun. *Romeo and Juliet* en a un : 24 scènes
dans les deux langues, alignables par l'ORDRE.

Usage : extrait_gutenberg.py <sortie.txt> --db <base.db> --titre <motif> --motif <regex>
"""
import re, sqlite3, sys


def main():
    sortie = sys.argv[1]
    db = sys.argv[sys.argv.index("--db")+1]
    titre = sys.argv[sys.argv.index("--titre")+1]
    motif = sys.argv[sys.argv.index("--motif")+1]
    c = sqlite3.connect(db)
    r = c.execute("select title, raw_text from backlog where title like ?",
                  (f"%{titre}%",)).fetchall()
    if not r:
        print(f"aucune œuvre pour {titre!r} dans {db}"); return 1
    t, txt = r[0]
    pos = [m.start() for m in re.finditer(motif, txt, re.M)]
    print(f"{db} · {t[:50]!r} · {len(txt):,} caractères · {len(pos)} segments")
    segs = []
    for i, p in enumerate(pos):
        fin = pos[i+1] if i+1 < len(pos) else len(txt)
        segs.append(txt[p:fin].strip())
    # NORMALISATION DES FINS DE LIGNE. Les textes Gutenberg n'ont pas tous les
    # mêmes : le français emploie des retours chariot SEULS (`\r`), que Python
    # traduit en `\n` en mode texte mais que `wc` ne compte pas. Sans cela on croit
    # à 24 segments et on en écrit 4835 lignes.
    import re as _re
    with open(sortie, "w") as f:
        for s in segs:
            f.write(_re.sub(r"\s+", " ", s).strip() + "\n")
    print(f"  {len(segs)} segments écrits dans {sortie} "
          f"({sum(len(s) for s in segs):,} caractères)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
