#!/usr/bin/env python3
"""nettoyer_corpus.py — le nettoyage du plein texte Wikipédia (balisage, titres, tables).

POURQUOI CE FICHIER EXISTE. Le 19/11, le val tiers (wikitext2) a montré que le corpus
v2 (6,90 Go, plein texte dédupliqué) perd 3,2 % face à v1 (1 Go propre) : v2 garde
`]]` 2 631 fois par 20 Mo (légendes, liens), des titres `==` isolés et des résidus
de tableaux. Le volume ne paie pas s'il est sale. Ce nettoyage est **en flux** (ligne
à ligne) : il tient en mémoire bornée, contrairement au `corpus_propre.py` des bancs.

Usage :
  python3 tools/nettoyer_corpus.py --entree data/wiki_mix_v2/train.txt \\
      --sortie work/clean/train.txt --json work/clean/nettoyage.json
  python3 tools/nettoyer_corpus.py --autotest
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# Le balisage Wikipédia qui survit à l'extraction.
LIEN = re.compile(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]")     # [[cible|libellé]] → libellé
MODELE = re.compile(r"\{\{[^{}]*\}\}")                    # {{modèle}} (une passe)
TABLE = re.compile(r"\{\|.*?\|\}", re.S)                  # {| ... |} (tableaux)
REF = re.compile(r"<ref[^>]*>.*?</ref>", re.S)            # <ref>…</ref>
BALISE = re.compile(r"</?[a-zA-Z][^>]{0,60}>")            # <br/>, <small>, <gallery>…
TITRE = re.compile(r"^\s*=+[^=\n]+=+\s*$")                # == Titre ==
ITAL = re.compile(r"'{2,5}")                             # '''gras''' / ''italique''
ORPHELIN = re.compile(r"\[\[|\]\]")                       # liens cassés restants
ENTITES = re.compile(r"&(nbsp|amp|lt|gt|quot);")


def nettoyer_ligne(ligne: str) -> str | None:
    """Rend la ligne nettoyée, ou None si la ligne est un titre (à jeter)."""
    if TITRE.match(ligne):
        return None
    l = TABLE.sub(" ", ligne)
    l = REF.sub(" ", l)
    l = LIEN.sub(r"\1", l)
    for _ in range(3):
        l2 = MODELE.sub(" ", l)
        if l2 == l:
            break
        l = l2
    l = BALISE.sub(" ", l)
    l = ITAL.sub("", l)
    l = ORPHELIN.sub("", l)
    l = ENTITES.sub(" ", l)
    l = re.sub(r"[ \t]{2,}", " ", l)          # les substitutions laissent des espaces doubles
    return l.rstrip()


def autotest() -> int:
    cas = [
        ("[[Antoine Meillet|Meillet]] est un linguiste.", "Meillet est un linguiste.", "lien"),
        ("== Biographie ==", None, "titre"),
        ("{{Infobox|nom=X}} Texte.", " Texte.", "modèle"),
        ("{| class=wikitable\n| a || b\n|} Texte.", " Texte.", "tableau"),
        ("<ref name=x>source</ref> Texte.", " Texte.", "référence"),
        ("du ''texte'' '''gras'''.", "du texte gras.", "italique"),
        ("Texte [[cassé.", "Texte cassé.", "lien cassé"),
    ]
    ok = 0
    for entree, attendu, nom in cas:
        obtenu = nettoyer_ligne(entree)
        if obtenu != attendu:
            print(f"  ❌ {nom} : {obtenu!r} ≠ {attendu!r}")
            return 1
        ok += 1
    print(f"  ✅ autotest : {ok}/{len(cas)} cas (lien, titre, modèle, tableau, référence, italique, lien cassé)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--entree", default="", help="corpus à nettoyer")
    ap.add_argument("--sortie", default="", help="corpus nettoyé")
    ap.add_argument("--json", default="")
    ap.add_argument("--autotest", action="store_true")
    a = ap.parse_args()
    if a.autotest:
        return autotest()
    if not a.entree or not a.sortie:
        ap.error("--entree et --sortie sont requis (sauf --autotest)")
    src = pathlib.Path(a.entree)
    dst = pathlib.Path(a.sortie)
    dst.parent.mkdir(parents=True, exist_ok=True)
    lignes_in = lignes_out = octets_in = octets_out = vides = 0
    with src.open("r", encoding="utf-8", errors="replace") as f, dst.open("w", encoding="utf-8") as g:
        precedent_vide = False
        for ligne in f:
            lignes_in += 1
            octets_in += len(ligne.encode("utf-8"))
            l = nettoyer_ligne(ligne.rstrip("\n"))
            if l is None:
                continue
            if not l.strip():
                if precedent_vide:
                    continue
                vides += 1
                precedent_vide = True
                g.write("\n")
                continue
            precedent_vide = False
            g.write(l + "\n")
            lignes_out += 1
            octets_out += len(l.encode("utf-8")) + 1
    res = {"entree": str(src), "sortie": str(dst), "lignes_in": lignes_in, "lignes_out": lignes_out,
           "octets_in": octets_in, "octets_out": octets_out, "vides_gardes": vides,
           "pct_octets_retires": round(100 * (1 - octets_out / max(1, octets_in)), 3)}
    print(json.dumps(res, ensure_ascii=False, indent=1))
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
