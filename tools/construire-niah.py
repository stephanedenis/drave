#!/usr/bin/env python3
"""construire-niah.py — la botte de foin à aiguille, reconstruite et gardée sur l'array.

POURQUOI CE FICHIER EXISTE. Trois portes — `porte-greffe.sh`, `porte-indice.sh`,
`porte-melange.sh` — lisent `/tmp/campagne24/niah_4096_0.5.txt`, un **artefact de campagne**
du 8-10 octobre que `/tmp` emporte à chaque redémarrage. Le 12/10, les trois ont rendu
**code 2** (« modèle ou source absents ») dans la passe complète : une porte sautée n'est
pas une porte verte, et trois portes sautées pour le même fichier disparu, c'est le
prérequis qu'il faut rendre **régénérable**, pas la porte qu'il faut excuser.

Ce que la campagne construisait (`tools/aiguille.py` en porte la doctrine) : du remplissage
**varié** — `data/wikitext2_test.txt`, jamais la même phrase recopiée (un remplissage répété
ne teste rien : le modèle peut répondre en devinant la structure) — une **aiguille** plantée
à une profondeur donnée, et la question à la fin. Le code que les portes cherchent est
`ZQ-4471-KX` ; la phrase qui le porte est celle de `porte-indice.sh`.

usage :
    tools/construire-niah.py [--jetons 4096] [--profondeur 0.5] [--sortie CHEMIN]
    tools/construire-niah.py --verifier ~/IA/scratch/prerequis/niah_4096_0.5.txt
"""
import argparse
import os
import pathlib
import sys

CODE = "ZQ-4471-KX"
AIGUILLE = ("\nIMPORTANT : the vault access code is " + CODE + ". Remember it, it will be "
            "asked at the end.\n")
CORPUS = "data/wikitext2_test.txt"
# Le tokenizer fait ~3,5 caractères par jeton sur du texte anglais : on vise large, les
# portes ne lisent que les 6 000 premiers caractères avant l'aiguille.
CAR_PAR_JETON = 3.5


def corps(jetons, corpus=CORPUS, fenetre=1.0 / 3.0):
    """Le remplissage : une fenêtre VARIÉE du corpus, à `fenetre` de sa longueur.

    `--fenetre` existe pour une raison de MESURE, pas de confort : le critère des portes
    (`porte-indice`, `porte-melange`) — un indice extérieur tombe plus près de l'aiguille que
    le hasard — dépend du CONTENU du remplissage, et la botte de foin de la campagne n'a
    jamais été versionnée. Faire varier la fenêtre dit si le critère tient sur un texte ou
    s'il ne tient que sur celui qu'on a choisi.
    """
    texte = pathlib.Path(corpus).read_text(encoding="utf-8", errors="replace")
    besoin = int(jetons * CAR_PAR_JETON)
    if len(texte) < besoin + 1000:
        sys.exit(f"corpus trop court : {len(texte)} caractères pour {besoin} demandés")
    debut = int(len(texte) * min(max(fenetre, 0.0), 0.95))
    return texte[debut:debut + besoin]


def construire(jetons, profondeur, fenetre=1.0 / 3.0):
    b = corps(jetons, fenetre=fenetre)
    c = int(len(b) * profondeur)
    return b[:c] + AIGUILLE + b[c:] + "\nQuestion: What is the vault access code?\n"


def verifier(chemin):
    t = pathlib.Path(chemin).read_text(encoding="utf-8", errors="replace")
    n = t.count(CODE)
    avant = t.index(CODE) if n else -1
    ok = n == 1 and avant >= 6000
    print(f"{chemin} : {len(t)} caractères · {n} aiguille(s) · "
          f"l'aiguille est au caractère {avant} · "
          f"{'✅ utilisable par les trois portes' if ok else '❌ inutilisable'}")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jetons", type=int, default=4096)
    ap.add_argument("--profondeur", type=float, default=0.5)
    ap.add_argument("--fenetre", type=float, default=1.0 / 3.0,
                    help="position de la fenêtre de remplissage dans le corpus (0 → 1)")
    ap.add_argument("--sortie", default="")
    ap.add_argument("--verifier", default="")
    a = ap.parse_args()
    if a.verifier:
        return verifier(os.path.expanduser(a.verifier))
    sortie = os.path.expanduser(a.sortie or
                                f"~/IA/scratch/prerequis/niah_{a.jetons}_{a.profondeur}.txt")
    texte = construire(a.jetons, a.profondeur, a.fenetre)
    os.makedirs(os.path.dirname(sortie), exist_ok=True)
    pathlib.Path(sortie).write_text(texte, encoding="utf-8")
    print(f"{sortie} : {len(texte)} caractères écrits")
    return verifier(sortie)


if __name__ == "__main__":
    sys.exit(main())
