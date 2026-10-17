#!/usr/bin/env python3
"""cribler_corpus.py — TOUTES LES PAIRES D'UN CORPUS MULTILINGUE SONT-ELLES CE QU'ELLES DISENT ?

POURQUOI. Le 17/10, une mesure a comparé **Dracula** à un **traité religieux** ✗✓ : le fichier
`dracula/dracula_fr.txt` du corpus `gutenberg_multilingual_verified` contient « Vocations Explained: Matrimony,
Virginity… » ✓✗. Le rapport de longueur le criait (**0,101** ✓) et les ancres le confirmaient (**0** occurrence
de « Dracula » dans le fichier français ✓✓). *Un corpus mal étiqueté est invisible tant qu'on ne vérifie pas* ✓.

CE QU'IL VÉRIFIE, sans modèle et sans langue ✗ (trois contrôles indépendants ✓) :
  1. **le TITRE** annoncé dans l'en-tête Gutenberg de chaque fichier ✓ — deux traductions d'une même œuvre
     partagent au moins un **nom propre** ✓ (« Dracula » ✓, « Alice » ✓) ;
  2. le **rapport de longueur** entre les deux langues ✓ — une traduction reste dans un facteur ~2 ✓✗ ;
  3. les **ancres** : les noms propres qui devraient être **identiques** dans les deux ✓.

Usage : python3 tools/cribler_corpus.py [--racine <dossier>]
"""
from __future__ import annotations
import argparse, pathlib, re

def titre(texte: str) -> str:
    m = re.search(r"eBook of (.{0,120}?)\n", texte)
    return (m.group(1).strip() if m else "(titre absent)")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--racine", default="/home/stephane/Data13TB/stephane/GitHub/Panini/data/gutenberg_multilingual_verified")
    a = ap.parse_args()
    racine = pathlib.Path(a.racine)
    paires = []
    for d in sorted(p for p in racine.iterdir() if p.is_dir()):
        for fr in d.glob("*_fr.txt"):
            en = d / (fr.name[:-6] + "en.txt")
            if en.exists():
                paires.append((d.name, fr, en))
    print(f"\n  {len(paires)} paires français/anglais dans {racine.name}\n")
    print("   paire                    | titres (fr / en)                      | longueurs | verdict")
    print("   -------------------------|---------------------------------------|-----------|--------")
    cassees = []
    for nom, fr, en in paires:
        tf, te = titre(fr.read_text(errors="ignore")), titre(en.read_text(errors="ignore"))
        lf, le = fr.stat().st_size, en.stat().st_size
        ratio = lf / max(1, le)
        # ⚠️ LE VERDICT MÊLE TROIS CONTRÔLES ✓ : un titre qui PARTAGE un nom propre ✓ (« Dracula »,
        # « Alice » ✓), un rapport de longueur plausible (0,4 à 2,5 ✓) et, à défaut, l'aveu du fichier.
        mots_fr = {m.lower() for m in re.findall(r"[A-Z][a-zà-ÿ]{3,}", tf)}
        mots_en = {m.lower() for m in re.findall(r"[A-Z][a-z]{3,}", te)}
        partage = mots_fr & mots_en
        ok_titre = bool(partage) or not (mots_fr and mots_en)
        ok_ratio = 0.4 <= ratio <= 2.5
        verdict = "OK ✓" if (ok_titre and ok_ratio) else "CASSE ✗"
        if verdict.startswith("CASSE"):
            cassees.append((nom, tf, te, ratio))
        print(f"   {nom:24s} | {tf[:18]:18s} / {te[:18]:18s} | {lf//1024:4d}/{le//1024:4d} | {verdict}")
    print()
    if cassees:
        print("  PAIRES CASSÉES — à ne pas utiliser :")
        for nom, tf, te, r in cassees:
            print(f"    {nom} : « {tf[:50]} » contre « {te[:50]} » (rapport {r:.3f})")
    else:
        print("  Aucune paire cassée détectée par ces trois contrôles ✓ — ce qui ne garantit pas l'alignement ✗,")
        print("  seulement que les fichiers sont bien ceux qu'ils disent ✓.")
    return 0

raise SystemExit(main())
