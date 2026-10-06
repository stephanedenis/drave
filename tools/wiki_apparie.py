#!/usr/bin/env python3
"""wiki_apparie.py — construire un corpus Wikipedia ALIGNÉ sur plusieurs langues.

POURQUOI. Le pont a été mesuré sur l'UDHR : **un seul texte** traduit en 392 langues.
C'est idéal pour l'invariance, mais pauvre comme professeur — la Déclaration fait
~1 300 jetons par langue, et son contenu est juridique et répétitif. L'objectif
demande des professeurs plus RICHES.

Ce que la machine contient déjà et qui n'avait pas été utilisé : **dix bases
Wikipedia décompressées** (`data/wikipedia/db/*.db`, 30 Go au total) — arabe,
allemand, anglais, espagnol, français, italien, japonais, portugais, russe, chinois.
Chacune porte, par article, son **résumé** (2 000 caractères), indexé par titre.

L'APPARIEMENT. Wikipedia n'est pas aligné — les articles diffèrent d'une langue à
l'autre. Mais un article donné existe dans plusieurs langues **sous le même titre**
quand ce titre est un nom propre ou un internationalisme (« Albert Einstein »,
« Albedo », « Achilles »). On garde donc les titres présents dans TOUTES les langues
visées : ils portent le même contenu, ce qui rend l'invariance mesurable.

Rendement mesuré sur 400 titres anglais tirés au hasard : fr 173 · de 179 · es 142 ·
it 182 · pt 149 · ru 39 · zh 27 · ja 22 · ar 1. Les écritures non latines
transcrivent les noms, donc l'appariement par titre y est stérile — on bâtit donc le
corpus aligné sur les **six langues latines**, et l'arabe, le chinois, le japonais et
le russe restent disponibles pour des mesures de fidélité et de transfert, pas
d'invariance.

Usage : wiki_apparie.py <sortie_dir> [--n 3000] [--langues en,fr,de,es,it,pt]
"""
import os
import re
import sqlite3
import sys

DB = "/home/stephane/Data13TB/stephane/data/wikipedia/db"


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def propre(t):
    """Nettoyage léger du résumé : on retire le balisage le plus courant, on garde
    la ponctuation et les accents (ils font partie de la langue)."""
    t = re.sub(r"<ref[^>]*>.*?</ref>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\{\{[^}]*\}\}", " ", t)
    t = re.sub(r"\[\[([^\]|]*\|)?([^\]]*)\]\]", r"\2", t)
    t = re.sub(r"'''?", "", t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{2,}", "\n", t)
    return t.strip()


def main():
    sortie = sys.argv[1]
    n = int(opt("--n", 3000))
    langues = opt("--langues", "en,fr,de,es,it,pt").split(",")
    os.makedirs(sortie, exist_ok=True)

    conns = {}
    for L in langues:
        p = os.path.join(DB, f"{L}wiki_v14.db")
        if not os.path.exists(p):
            print(f"# {L} : base absente ({p})")
            continue
        conns[L] = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
    langues = [L for L in langues if L in conns]
    print(f"# langues retenues : {', '.join(langues)}")

    # titres candidats : on part de l'anglais, en se limitant aux articles dont le
    # résumé est substantiel — un titre sans texte ne sert à rien.
    t0 = conns["en"]
    cand = [r[0] for r in t0.execute(
        "select title from articles where length(summary) > 900 limit ?", (n,))]
    print(f"# {len(cand)} titres anglais candidats (résumé > 900 caractères)")

    gardes = []
    for t in cand:
        tl = t.lower()
        ok = True
        for L in langues:
            if L == "en":
                continue
            if not conns[L].execute(
                    "select 1 from articles where title_lower=? and "
                    "length(summary)>900", (tl,)).fetchone():
                ok = False
                break
        if ok:
            gardes.append(t)
    print(f"# {len(gardes)} titres présents dans les {len(langues)} langues "
          f"({len(gardes)/max(len(cand),1):.0%})")

    ecrits = {L: 0 for L in langues}
    car = {L: 0 for L in langues}
    for t in gardes:
        tl = t.lower()
        slug = re.sub(r"[^A-Za-z0-9]+", "_", t)[:60].strip("_")
        if not slug:
            continue
        blocs = {}
        for L in langues:
            r = conns[L].execute(
                "select summary from articles where title_lower=? and "
                "length(summary)>900 order by length(summary) desc limit 1",
                (tl,)).fetchone()
            if not r:
                blocs = None
                break
            blocs[L] = propre(r[0])
        if not blocs or any(len(v) < 400 for v in blocs.values()):
            continue
        for L in langues:
            p = os.path.join(sortie, f"{L}_{slug}.txt")
            open(p, "w", encoding="utf-8").write(blocs[L])
            ecrits[L] += 1
            car[L] += len(blocs[L])

    print(f"\n# CORPUS APPARIÉ ÉCRIT DANS {sortie}")
    print(f"# {'langue':<8}{'articles':>10}{'caractères':>13}{'moyenne':>10}")
    for L in langues:
        print(f"  {L:<8}{ecrits[L]:>10}{car[L]:>13,}"
              f"{car[L]/max(ecrits[L],1):>10.0f}")
    for c in conns.values():
        c.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
