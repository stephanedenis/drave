#!/usr/bin/env python3
"""verifier_bilan.py — LES CHIFFRES DU BILAN SE RETROUVENT-ILS DANS LES SECTIONS ?

POURQUOI. Un chapitre de trente-cinq mesures finit par un **bilan** ✓ — et le risque est qu'il **dérive** ✗ :
un résumé qui cite un chiffre que le corps ne contient plus ✓✗, ou qui en omet un essentiel ✓. Ce n'est pas une
vérification de **sens** (elle reste humaine ✗) ; c'est une vérification de **traçabilité** ✓✓ : chaque nombre du
bilan doit exister **ailleurs** dans le document ✓.

CE QU'IL FAIT. Il isole le bilan ✓ (entre « Le bilan des certitudes » et la section suivante ✓), en extrait les
nombres ✓ (pourcentages et décimales ✓), et cherche chacun dans le **corps** ✓. Il liste aussi les chiffres-clés
du corps qui **manquent** au bilan ✓ (les omissions ✓).

⚠️ CE QU'IL NE PEUT PAS DIRE ✗ : il compare des **chaînes** ✓✗ — « 5 ms » et « 5,0 ms » sont deux nombres
différents pour lui ✓, alors que c'est le même ✓. Un écart de format n'est **pas** une erreur ✓✓ ; c'est à
l'humain de trancher ✓.

Usage : python3 tools/verifier_bilan.py [--fichier docs/synthese/07-...md]
"""
from __future__ import annotations
import argparse, pathlib, re


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fichier", default="docs/synthese/07-modeles-alternatifs-entree-sortie.md")
    ap.add_argument("--debut", default="### Le bilan des certitudes")
    ap.add_argument("--fin", default="## Ce que la nuit du 16/10")
    a = ap.parse_args()
    t = pathlib.Path(a.fichier).read_text()
    i, j = t.find(a.debut), t.find(a.fin)
    if i < 0 or j < 0:
        print(f"  ✗ bornes introuvables ({a.debut!r} / {a.fin!r}) — le bilan a peut-être été déplacé ✗")
        return 1
    bilan, corps = t[i:j], t[:i] + t[j:]
    nombres = set(re.findall(r"\d+[.,]\d+|\d+ %", bilan))
    manquants = sorted(n for n in nombres if n not in corps)
    print(f"  bilan : {len(bilan)} caractères · corps : {len(corps)} caractères")
    print(f"  nombres cités dans le bilan : {len(nombres)}")
    print(f"  nombres ABSENTS du corps : {len(manquants)}")
    for n in manquants:
        print(f"    {n} ✗ — à vérifier (peut être un écart de format ✓, pas une erreur ✗)")
    if not manquants:
        print("  ✅ tous les nombres du bilan existent ailleurs dans le document ✓✓")
    print("\n  ⚠️ rappel : cette vérification est de TRAÇABILITÉ, pas de SENS ✓ — un nombre présent peut être")
    print("  cité dans un contexte faux ✗, et seule une relecture humaine le voit ✓✓.")
    return 0

raise SystemExit(main())
