#!/usr/bin/env python3
"""extrait_crime.py — deuxième œuvre PARALLÈLE, et deuxième paire de langues.

Le corpus parallèle du pont ne comptait qu'UNE œuvre : *Roméo et Juliette*, en
anglais et en français (24 scènes). L'objectif demande des œuvres parallèles
Gutenberg ; les bases `backlog_gutenberg_{en,fr,de,es}.db` en contiennent trois
paires exploitables, dont deux jamais utilisées :

  Roméo et Juliette        en ↔ fr   24 scènes      (déjà traité)
  Le Comte de Monte-Cristo en ↔ fr   découpage malcommode (tomes inégaux)
  CRIME ET CHÂTIMENT       en ↔ es   38 chapitres   ← celui-ci

L'intérêt de *Crime et Châtiment* n'est pas seulement d'ajouter du texte : c'est
d'ajouter une **paire de langues différente**. Si le transfert se comporte comme sur
Romeo, c'est une propriété du pont ; s'il se comporte autrement, c'était une
propriété du couple en–fr. Une seule paire ne permet pas de trancher.

ALIGNEMENT EXACT. On ne découpe PAS à offsets fixes : le même caractère ne dit pas la
même chose dans les deux langues. On découpe par CHAPITRE, et le chapitre `i` d'une
langue correspond au chapitre `i` de l'autre — vérifié sur les tailles, dont le
rapport reste entre 0,82 et 1,14 sur les 38 premiers chapitres.

CONTEXTE. Un chapitre fait 18 000 à 40 000 caractères, soit trop pour `--ctx 1024`.
On garde les chapitres qui tiennent dans `--ctx 8192` **dans les deux langues**, et on
n'écrit que ceux-là : un chapitre tronqué d'un côté seulement romprait l'alignement
sans le dire.

Usage : extrait_crime.py <sortie_dir> [--max-car 26000] [--min-car 4000]
"""
import os
import re
import sqlite3
import sys

DB = "/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion"


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def texte(langue, motif):
    p = os.path.join(DB, f"backlog_gutenberg_{langue}.db")
    c = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
    r = c.execute("select raw_text from backlog where title like ?",
                  (f"%{motif}%",)).fetchone()
    c.close()
    return r[0] if r else None


def decoupe(t, motif):
    pos = [m.start() for m in re.finditer(motif, t, re.M)]
    return [t[pos[i]:(pos[i + 1] if i + 1 < len(pos) else len(t))].strip()
            for i in range(len(pos))]


def main():
    sortie = sys.argv[1]
    mx = int(opt("--max-car", 26000))
    mn = int(opt("--min-car", 4000))
    os.makedirs(sortie, exist_ok=True)

    en = texte("en", "Crime and Punishment")
    es = texte("es", "crimen")
    if en is None or es is None:
        print("# œuvre absente des bases"); return 1
    # l'anglais marque « CHAPTER <romain> » ; l'espagnol, une ligne ne portant que
    # le numéro romain. Comptes mesurés : 39 contre 40 — d'où l'alignement par index
    # borné au plus court.
    A = decoupe(en, r"^\s*CHAPTER\s+[IVXLC]+")
    B = decoupe(es, r"^\s*[IVXLC]{1,6}\s*$")
    print(f"# anglais : {len(A)} chapitres · espagnol : {len(B)} chapitres")

    n = min(len(A), len(B))
    gardes = []
    for i in range(n):
        if mn <= len(A[i]) <= mx and mn <= len(B[i]) <= mx:
            gardes.append(i)
    print(f"# {len(gardes)} chapitres tiennent dans [{mn}, {mx}] caractères "
          f"DANS LES DEUX LANGUES, sur {n} alignables")

    tot = {"en": 0, "es": 0}
    for j, i in enumerate(gardes, start=1):
        for L, S in (("en", A), ("es", B)):
            p = os.path.join(sortie, f"{L}_{j:02d}.txt")
            open(p, "w", encoding="utf-8").write(S[i])
            tot[L] += len(S[i])
    print(f"\n# CORPUS ÉCRIT DANS {sortie}")
    for L in ("en", "es"):
        print(f"  {L} : {len(gardes)} chapitres · {tot[L]:,} caractères · "
              f"{tot[L]/max(len(gardes),1):,.0f} par chapitre")
    print(f"\n# Rappel : le corpus Romeo (en–fr) sert de comparaison. Une paire ne "
          f"permet pas de distinguer une propriété du PONT d'une propriété du COUPLE "
          f"de langues ; deux paires, si.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
