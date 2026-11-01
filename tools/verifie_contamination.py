#!/usr/bin/env python3
"""verifie_contamination.py — les fuites entre splits et entre corpus, mesurées.

POURQUOI CE FICHIER. Un corpus d'entraînement sans contrôle de fuite est un corpus qui mentira
sur son évaluation. Ce script vérifie deux choses, avec des chiffres :

1. **les doublons de tronçons entre splits** : chaque ligne des fichiers (tronçon de 8 Ko écrit
   par `corpus_wikipedia.py`) est hachée ; un tronçon qui apparaît dans deux splits est une fuite
   exacte (les quasi-doublons ne sont pas détectés — c'est dit). Pour le **texte intégral**
   (`corpus_wikipedia_texte.py`), l'unité est la **fenêtre** de 8 Ko coupée au mot
   (`--taille-troncon 8192`), parce que les tronçons contiennent des retours à la ligne ;
2. **le recouvrement avec les jeux d'évaluation** : des fenêtres de `--fenetre` octets,
   échantillonnées dans chaque fichier d'évaluation, sont cherchées dans l'entraînement par
   `mmap.find` — une fenêtre trouvée est une fuite.

Ce n'est pas un détecteur de paraphrase : deux textes reformulés passent. C'est un contrôle
d'**exactitude**, celui qui doit être à zéro avant d'entraîner.

Usage :
  python3 tools/verifie_contamination.py --train data/corpus_wiki_fr/train.txt \
      --val data/corpus_wiki_fr/val.txt --test data/corpus_wiki_fr/test.txt \
      --eval data/corpus_propre/test.txt --eval data/wikitext2_test.txt
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mmap
import pathlib
import sys


def hache(bloc: bytes) -> str:
    return hashlib.blake2b(bloc, digest_size=16).hexdigest()


def troncons(chemin: pathlib.Path, taille: int):
    """Les unités de comparaison : les lignes (défaut), ou des fenêtres de `taille` octets.

    Le corpus de résumés écrit un tronçon par ligne ; le corpus de texte intégral écrit des
    tronçons de 8 192 caractères qui contiennent des retours à la ligne (les paragraphes). Pour
    ce dernier, l'unité de comparaison est la **fenêtre** de 8 Ko coupée au mot, pas la ligne —
    sinon les titres de sections répétés (« Biographie », etc.) font un faux taux de 5 %.
    """
    if taille <= 0:
        with chemin.open("rb") as f:
            for ligne in f:
                ligne = ligne.strip()
                if len(ligne) >= 64:
                    yield ligne
        return
    with chemin.open("rb") as f:
        buf = b""
        while True:
            bloc = f.read(1 << 20)
            if not bloc:
                break
            buf += bloc
            while len(buf) >= taille:
                coupe = buf.rfind(b" ", taille // 2, taille)
                fin = coupe if coupe > 0 else taille
                m = buf[:fin].strip()
                if len(m) >= 64:
                    yield m
                buf = buf[fin:]
        m = buf.strip()
        if len(m) >= 64:
            yield m


def doublons_entre(train: pathlib.Path, autres: list[pathlib.Path], taille: int = 0) -> dict:
    vus: set[str] = set()
    n_train = 0
    for t in troncons(train, taille):
        vus.add(hache(t))
        n_train += 1
    resultat = {"train_troncons": n_train, "par_split": {}}
    for autre in autres:
        n = 0
        dup = 0
        for t in troncons(autre, taille):
            n += 1
            if hache(t) in vus:
                dup += 1
        resultat["par_split"][autre.name] = {"troncons": n, "doublons": dup,
                                             "taux": round(dup / max(n, 1), 6)}
    return resultat


def recouvrement(train: pathlib.Path, eval_: pathlib.Path, fenetre: int,
                 pas: int, echantillon: int) -> dict:
    with eval_.open("rb") as f:
        texte = f.read()
    if len(texte) <= fenetre:
        return {"fichier": eval_.name, "fenetres": 0, "trouvees": 0, "taux": 0.0}
    positions = list(range(0, len(texte) - fenetre, pas))
    if echantillon and len(positions) > echantillon:
        pas_ech = max(len(positions) // echantillon, 1)
        positions = positions[::pas_ech][:echantillon]
    trouvees = 0
    with train.open("rb") as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
        for p in positions:
            if mm.find(texte[p:p + fenetre]) != -1:
                trouvees += 1
    return {"fichier": eval_.name, "fenetre": fenetre, "fenetres": len(positions),
            "trouvees": trouvees, "taux": round(trouvees / max(len(positions), 1), 4)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--train", type=pathlib.Path, required=True)
    ap.add_argument("--val", type=pathlib.Path)
    ap.add_argument("--test", type=pathlib.Path)
    ap.add_argument("--eval", type=pathlib.Path, action="append", default=[])
    ap.add_argument("--fenetre", type=int, default=128)
    ap.add_argument("--pas", type=int, default=512)
    ap.add_argument("--echantillon", type=int, default=40)
    ap.add_argument("--taille-troncon", type=int, default=0,
                    help="0 = lignes ; 8192 = fenêtres de 8 Ko (texte intégral)")
    ap.add_argument("--sortie", type=pathlib.Path)
    args = ap.parse_args()
    autres = [p for p in (args.val, args.test) if p and p.exists()]
    resultat = {"train": args.train.as_posix(),
                "doublons_entre_splits": doublons_entre(args.train, autres),
                "recouvrement_eval": [recouvrement(args.train, p, args.fenetre, args.pas,
                                                   args.echantillon)
                                      for p in args.eval if p.exists()]}
    if args.taille_troncon > 0:
        resultat["taille_troncon"] = args.taille_troncon
        resultat["doublons_entre_splits_troncon"] = doublons_entre(args.train, autres,
                                                                   args.taille_troncon)
    print(json.dumps(resultat, ensure_ascii=False, indent=1))
    if args.sortie:
        args.sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n",
                               encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
