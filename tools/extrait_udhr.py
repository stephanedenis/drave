#!/usr/bin/env python3
"""extrait_udhr.py — l'UDHR en unités alignées, prêtes à passer dans le moteur.

L'UDHR est le premier corpus parce que l'alignement y est **par construction** :
les 30 articles existent dans les 456 langues, et c'est le même énoncé. Aucun
aligneur, donc aucun décalage possible — le contraire d'un corpus apparié à la
main.

Sortie : un JSON par unité `(article, paragraphe)`, et un index. Chaque unité
porte le texte de CHAQUE langue, pour qu'on puisse la faire passer dans les
couches d'entrée langue par langue et comparer les activations.

Usage :
    extrait_udhr.py <dossier_udhr_xml> <sortie.jsonl> [--min-langues 50]
"""
import glob
import json
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET

NS = "{http://www.unhchr.ch/udhr}"


def texte(el):
    """Le texte d'un élément, espaces normalisés — deux langues n'ont pas les
    mêmes habitudes d'espacement, et ce n'est pas ce qu'on mesure."""
    t = "".join(el.itertext())
    t = unicodedata.normalize("NFC", t)
    return re.sub(r"\s+", " ", t).strip()


def lire(chemin):
    """Rend (code, nom, {cle: texte}) pour une langue. La clé d'un article est
    `a<n>` — c'est l'unité d'alignement STABLE ; les paragraphes de préambule,
    eux, varient de 58 à 67 selon la traduction, donc on les indexe par rang et
    on assume le risque en le DISANT."""
    r = ET.parse(chemin).getroot()
    code = r.get("iso639-3") or r.get("key") or os.path.basename(chemin)
    nom = r.get("n") or code
    unites = {}
    for prem in r.findall(f"{NS}preamble"):
        for i, para in enumerate(prem.findall(f"{NS}para")):
            unites[f"preambule-{i:02d}"] = texte(para)
    for art in r.findall(f"{NS}article"):
        num = art.get("number") or art.get("n") or "?"
        paras = art.findall(f"{NS}para")
        if not paras:
            unites[f"article-{num}"] = texte(art)
        else:
            for i, para in enumerate(paras):
                unites[f"article-{num}-{i:02d}"] = texte(para)
    return code, nom, unites


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    dossier, sortie = sys.argv[1], sys.argv[2]
    mini = 50
    if "--min-langues" in sys.argv:
        mini = int(sys.argv[sys.argv.index("--min-langues") + 1])

    par_unite = {}
    langues = {}
    for f in sorted(glob.glob(os.path.join(dossier, "udhr_*.xml"))):
        try:
            code, nom, unites = lire(f)
        except Exception as e:
            print(f"  {os.path.basename(f)} : illisible ({e})")
            continue
        langues[code] = nom
        for cle, t in unites.items():
            if t:
                par_unite.setdefault(cle, {})[code] = t

    gardees = {c: n for c, n in sorted(par_unite.items()) if len(n) >= mini}
    with open(sortie, "w", encoding="utf-8") as out:
        for cle, tr in sorted(gardees.items()):
            out.write(json.dumps({"unite": cle, "n_langues": len(tr), "traductions": tr},
                                 ensure_ascii=False) + "\n")
    print(f"{len(langues)} langues lues · {len(par_unite)} unités vues · "
          f"{len(gardees)} unités gardées (≥ {mini} langues)")
    if gardees:
        ex = sorted(gardees.items())[0]
        print(f"  exemple — {ex[0]} en {len(ex[1])} langues :")
        for c in list(ex[1])[:3]:
            print(f"    {c} ({langues.get(c,'?')[:18]}) : {ex[1][c][:64]}…")
    print(f"  écrit dans {sortie}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
