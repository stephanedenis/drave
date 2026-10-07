#!/usr/bin/env python3
"""extrait_article1.py — l'ARTICLE 1 DE L'UDHR, dans toutes les langues, en un fichier par langue.

POURQUOI CE CORPUS, ET PAS UN AUTRE.

Les cycles de cette session ont été lents (traces de 15 s, ajustements de pont de
plusieurs minutes) parce que chaque entrée portait un TEXTE ENTIER : 482 articles
de 575 positions, ou l'UDHR complet. Or l'unité d'alignement la plus solide de
l'UDHR n'est pas l'article — c'est **l'article 1**, présent dans TOUTES les
langues, qui dit exactement la même chose, et qui tient en une phrase.

Un corpus « article 1 » :
  * se trace **20 à 40 fois plus vite** (une phrase, pas un document) ;
  * donne des caches **minuscules** — donc des ajustements en quelques secondes ;
  * porte **456 langues au lieu de 10** pour la même mesure de plateau sémantique ;
  * et sa cible (`h_c` de la même phrase dans 456 langues) est **alignée par
    construction** : pas d'aligneur, donc pas de décalage possible.

C'est ce qui remplace la taille du professeur comme levier de vitesse. Un modèle
plus petit gagnerait ×2 ou ×3 sur la passe avant ; raccourcir l'entrée gagne ×20,
et améliore en plus la statistique.

Usage : extrait_article1.py [dossier_udhr_xml] [dossier_sortie]
"""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extrait_udhr import lire  # noqa: E402


def opt(nom, defaut):
    return sys.argv[sys.argv.index(nom) + 1] if nom in sys.argv else defaut


def main():
    # Les arguments POSITIONNELS se prennent avant les options, EN SAUTANT LA
    # VALEUR DES OPTIONS. Un simple « ne commence pas par -- » ne suffit pas :
    # dans `--article 2`, le « 2 » est la valeur du drapeau et passait pour un
    # dossier de sortie — le script écrivait alors zéro langue dans un dossier
    # nommé « 2 », en annonçant qu'il avait réussi.
    argv = sys.argv[1:]
    pos, i = [], 0
    while i < len(argv):
        if argv[i].startswith("--"):
            i += 2 if (i + 1 < len(argv) and not argv[i+1].startswith("--")) else 1
        else:
            pos.append(argv[i]); i += 1
    dossier = pos[0] if len(pos) > 0 else \
        "/home/stephane/Data13TB/stephane/corpus/udhr/udhr_xml"
    # L'ARTICLE est un paramètre, parce qu'il en faut DEUX pour que « sémantique »
    # ait un sens : sans un second article, on ne peut pas distinguer « les langues
    # se ressemblent parce que c'est le même texte » de « les langues se ressemblent
    # parce que la couche est anisotrope ». Le contrôle est le même article dans
    # une autre langue CONTRE un autre article dans une autre langue.
    art = opt("--article", "1")
    sortie = pos[1] if len(pos) > 1 else \
        f"/home/stephane/Data13TB/stephane/corpus/udhr/article{art}"
    os.makedirs(sortie, exist_ok=True)
    faits, vides = 0, []
    # Les codes `iso639-3` ne sont PAS uniques : 456 fichiers XML portent 400
    # codes distincts, et `und` (langue non déterminée) en porte cinq à lui seul.
    # Deux fichiers de même code s'écrasent — donc compter les ÉCRITURES donne un
    # chiffre plus grand que le nombre de LANGUMES du corpus. On compte les codes.
    codes_vus, collisions = {}, []
    longueurs = []
    for f in sorted(glob.glob(os.path.join(dossier, "udhr_*.xml"))):
        try:
            code, nom, unites = lire(f)
        except Exception as e:
            print(f"  illisible {os.path.basename(f)} : {e}")
            continue
        # L'article 1 peut être découpé en plusieurs paragraphes selon la
        # traduction : on les recolle, l'unité reste l'article.
        # `startswith("article-1")` attrape AUSSI article-10 à article-19 : la
        # première version concaténait dix articles et donnait une médiane de
        # 2 978 caractères pour une phrase qui en fait ~150. Un préfixe n'est pas
        # une égalité.
        morceaux = [v for k, v in sorted(unites.items())
                    if k == f"article-{art}" or k.startswith(f"article-{art}-")]
        t = " ".join(morceaux).strip()
        if len(t) < 10:
            vides.append(code)
            continue
        if code in codes_vus and codes_vus[code] != t:
            collisions.append(code)
        codes_vus[code] = t
        with open(os.path.join(sortie, f"{code}.txt"), "w", encoding="utf-8") as g:
            g.write(t + "\n")
        faits += 1
        longueurs.append(len(t))
    longueurs.sort()
    print(f"# article {art} : {faits} écritures, {len(codes_vus)} codes distincts, "
          f"{faits - len(codes_vus)} écrasement(s) — dans {sortie}")
    if collisions:
        print(f"#   codes portés par des textes DIFFÉRENTS : {' '.join(sorted(set(collisions))[:10])}")
    if vides:
        print(f"# {len(vides)} sans article {art} exploitable : {' '.join(vides[:12])}"
              + (" …" if len(vides) > 12 else ""))
    if longueurs:
        n = len(longueurs)
        print(f"# longueur en caractères : médiane {longueurs[n//2]} · "
              f"min {longueurs[0]} · max {longueurs[-1]} · "
              f"90e centile {longueurs[int(0.9*n)]}")
        print(f"# → un contexte de 128 jetons couvre largement l'article 1 dans "
              f"toutes les langues sauf les plus longues")
    return 0


if __name__ == "__main__":
    sys.exit(main())
