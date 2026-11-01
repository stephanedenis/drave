#!/usr/bin/env python3
"""extraire_evals_langues.py — les jeux d'évaluation **par langue**, ciblés.

POURQUOI. `verifie_contamination.py --eval` échantillonne quarante fenêtres dans le fichier
qu'on lui donne. Lui donner le TSV XNLI entier (quinze langues) ou l'UDHR entier (des centaines
de langues) mélange les langues et affaiblit le contrôle. Ce script extrait, **par langue**, les
phrases du XNLI (`sentence1` + `sentence2`) et les articles de l'UDHR (`texte`), dans
`work/dr/eval/` ; le vérificateur reçoit alors le fichier de la langue du corpus.

Usage :
  python3 tools/extraire_evals_langues.py                       # toutes les langues disponibles
  python3 tools/extraire_evals_langues.py --langue fr --langue en
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
XNLI = RACINE / "data/xnli/XNLI-1.0/xnli.dev.tsv"
UDHR = RACINE / "data/udhr/articles.jsonl"
SORTIE = RACINE / "work/dr/eval"
XNLI_LANGS = ("ar", "de", "en", "es", "fr", "ru", "zh")
UDHR_ISO = {"fr": "fra", "it": "ita", "ja": "jpn", "pt": "por"}


def xnli(langue: str) -> pathlib.Path | None:
    if not XNLI.exists():
        return None
    sortie = SORTIE / f"{langue}-xnli.txt"
    n = 0
    with XNLI.open(encoding="utf-8", newline="") as f, sortie.open("w", encoding="utf-8") as g:
        lecteur = csv.reader(f, delimiter="\t")
        entete = next(lecteur)
        i_lang = entete.index("language")
        i_s1 = entete.index("sentence1")
        i_s2 = entete.index("sentence2")
        for ligne in lecteur:
            if len(ligne) <= max(i_s1, i_s2) or ligne[i_lang] != langue:
                continue
            g.write(ligne[i_s1].strip() + "\n" + ligne[i_s2].strip() + "\n")
            n += 1
    return sortie if n else None


def udhr(langue: str) -> pathlib.Path | None:
    iso3 = UDHR_ISO.get(langue)
    if not iso3 or not UDHR.exists():
        return None
    sortie = SORTIE / f"{langue}-udhr.txt"
    n = 0
    with UDHR.open(encoding="utf-8") as f, sortie.open("w", encoding="utf-8") as g:
        for ligne in f:
            if not ligne.strip():
                continue
            d = json.loads(ligne)
            if d.get("iso3") == iso3:
                g.write(d.get("texte", "").strip() + "\n")
                n += 1
    return sortie if n else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--langue", action="append", default=[])
    args = ap.parse_args()
    langues = args.langue or list(dict.fromkeys(XNLI_LANGS + tuple(UDHR_ISO)))
    SORTIE.mkdir(parents=True, exist_ok=True)
    for langue in langues:
        for nom, fn in (("xnli", xnli), ("udhr", udhr)):
            p = fn(langue)
            if p:
                print(f"  {langue}-{nom}.txt : {p.stat().st_size} octets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
