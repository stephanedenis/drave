#!/usr/bin/env python3
"""corpus_wikipedia.py — assembler un VRAI corpus d'entraînement depuis Wikipedia.

POURQUOI. Le banc `essai_decharge.py` tournait sur 1,3 million de caractères
(wikitext-2 + les 482 articles appariés) : assez pour voir une dynamique, pas
assez pour comparer deux architectures — les deux modèles sur-apprennent, et
c'est la vitesse de surapprentissage qu'on mesure, pas la qualité. Wikipedia
décompressée est sur le disque (34 Go pour l'anglais) et son format est trivial
(`articles[].text`). Ce script en fait un corpus plat, reproductible.

CE QU'IL GARANTIT :
  * reproductible : mêmes chapitres, même ordre, mêmes bornes ;
  * la validation vient d'un BLOC DE CHAPITRES CONTIGU, retiré de
    l'apprentissage — pas d'un tirage qui laisserait fuir du texte appris ;
  * l'alphabet est calculé sur l'apprentissage SEUL, et rapporté : c'est lui qui
    fixe la taille de l'embedding.

Usage :
    corpus_wikipedia.py --langue en --octets 100000000 --val-octets 2000000 \
        --sortie data/corpus_en.txt --validation data/corpus_en_val.txt
"""
import argparse
import glob
import json
import os
import sys

W = "/home/stephane/Data13TB/stephane/nipada/wikipedia_decompressed"


def ecrire(chapitres, sortie, limite, ecarte):
    """Écrit les articles jusqu'à `limite` caractères ; saute les chapitres
    écartés (ceux de la validation). Ne coupe pas un article au milieu."""
    n, articles = 0, 0
    with open(sortie, "w", encoding="utf-8") as f:
        for c in chapitres:
            if c in ecarte:
                continue
            try:
                d = json.load(open(c, encoding="utf-8", errors="replace"))
            except Exception:
                continue
            for a in d.get("articles", []):
                t = (a.get("text") or "").strip()
                if len(t) < 200:      # une ébauche ou un titre n'apprend rien
                    continue
                f.write(t)
                f.write("\n\n")
                n += len(t)
                articles += 1
                if n >= limite:
                    return n, articles
    return n, articles


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--langue", default="en")
    p.add_argument("--octets", type=int, default=100_000_000)
    p.add_argument("--val-octets", type=int, default=2_000_000)
    p.add_argument("--sortie", default="data/corpus_en.txt")
    p.add_argument("--validation", default="data/corpus_en_val.txt")
    a = p.parse_args()

    tous = sorted(glob.glob(os.path.join(W, a.langue, "*.json")))
    if not tous:
        sys.exit(f"aucun chapitre pour la langue {a.langue} dans {W}")
    print(f"# {a.langue} : {len(tous)} chapitres disponibles")

    # La validation est prise au MILIEU du corpus, sur des chapitres contigus,
    # et ces chapitres sont retirés de l'apprentissage.
    milieu = len(tous) // 2
    bloc_val = tous[milieu:milieu + 40]
    ecarte = set(bloc_val)
    n_val, art_val = ecrire(bloc_val, a.validation, a.val_octets, set())
    n, art = ecrire(tous, a.sortie, a.octets, ecarte)
    print(f"# apprentissage : {n} caractères · {art} articles → {a.sortie}")
    print(f"# validation    : {n_val} caractères · {art_val} articles → {a.validation} "
          f"({len(bloc_val)} chapitres écartés)")

    alpha = set()
    with open(a.sortie, encoding="utf-8") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            alpha |= set(b)
    print(f"# alphabet d'apprentissage : {len(alpha)} caractères")
    return 0


if __name__ == "__main__":
    sys.exit(main())
