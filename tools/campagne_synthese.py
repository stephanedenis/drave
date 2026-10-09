#!/usr/bin/env python3
"""campagne_synthese.py — transformer les journaux de campagne en tableaux.

POURQUOI. Une campagne de 24 h produit des dizaines de fichiers de sortie bruts
dans `/tmp/campagne24/`. Ce script les relit, en extrait les seules grandeurs
qui décident (perplexité, événements par jeton, tok/s, mémoire résidente, octets
lus) et rend un Markdown collable dans un rapport — avec, pour chaque ligne, la
charge de fond au moment de la mesure, parce qu'un temps mesuré sous charge 17
ne se compare pas à un temps mesuré sous charge 3.

Usage :
    campagne_synthese.py [--dir /tmp/campagne24] [--sortie rapport.md]
"""
import argparse
import glob
import math
import os
import re
import sys

RE_PPL = re.compile(r"perplexité ([0-9.]+) sur (\d+) tokens")
RE_EV = re.compile(r"\((\d+) événements")
RE_TS = re.compile(r"([0-9.]+) tok/s effectifs")
RE_LISTES = re.compile(r"dont en listes[^:]*: ([0-9.]+) M")
RE_PAIRES = re.compile(r"total ([0-9.]+) M")
RE_RSS = re.compile(r"Maximum resident set size \(kbytes\): (\d+)")
RE_LUS = re.compile(r"File system inputs: (\d+)")
RE_TEMPS = re.compile(r"Elapsed \(wall clock\) time[^:]*: ([0-9:.]+)")
RE_TOK_CORPUS = re.compile(r"(\d+) tokens écrits")


def lire(chemin):
    try:
        with open(chemin, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def bits_par_octet(ppl, jetons_corpus, octets_corpus):
    """La perplexité n'est comparable entre modèles QUE si le tokenizer est le
    même. Codestral (32 768 entrées) découpe le même texte en 288 554 jetons là où
    Qwen en fait 85 626 : son « PPL » ne se lit pas sur la même échelle. Le
    bits/octet, lui, se compare — c'est la seule unité commune entre tokenizers."""
    if not ppl or not jetons_corpus or not octets_corpus:
        return ""
    try:
        return f"{math.log2(float(ppl)) * jetons_corpus / octets_corpus:.3f}"
    except (ValueError, ZeroDivisionError):
        return ""


def mesure(prefixe, dossier):
    """Une ligne de tableau à partir d'un log et de son fichier de temps.

    Le fichier de temps ne suit pas toujours le nom du log : la campagne écrit
    `grille_<nom>_temps.log` pour un log `grille_<nom>_ppl.log`. On essaie les
    deux dispositions — un `_temps.log` vide veut dire « mesure en cours », et
    c'est une information, pas une absence.
    """
    log = os.path.join(dossier, prefixe + ".log")
    candidats = [os.path.join(dossier, prefixe + "_temps.log")]
    if prefixe.endswith("_ppl"):
        candidats.append(os.path.join(dossier, prefixe[:-4] + "_temps.log"))
    temps = next((c for c in candidats if os.path.exists(c)), candidats[0])
    texte = lire(log)
    if not texte:
        return None
    ppl = RE_PPL.search(texte)
    ev = RE_EV.search(texte)
    ts = RE_TS.search(texte)
    listes = RE_LISTES.search(texte)
    paires = RE_PAIRES.search(texte)
    t = lire(temps)
    rss = RE_RSS.search(t)
    lus = RE_LUS.search(t)
    duree = RE_TEMPS.search(t)
    # Le nombre de jetons du corpus vient du log de tokenisation du MÊME modèle.
    base = prefixe.split("_ppl")[0]
    tok_log = lire(os.path.join(dossier, base + "_tokenize.log"))
    mt = RE_TOK_CORPUS.search(tok_log)
    octets_corpus = 359041          # data/wikitext2_test.txt, mesuré une fois
    bpo = bits_par_octet(ppl.group(1) if ppl else "", int(mt.group(1)) if mt else 0,
                         octets_corpus)
    return {
        "etape": prefixe,
        "bits_octet": bpo,
        "ppl": ppl.group(1) if ppl else "",
        "jetons": ppl.group(2) if ppl else "",
        "evenements": ev.group(1) if ev else "",
        "tok_s": ts.group(1) if ts else "",
        "en_listes": listes.group(1) if listes else "",
        "paires": paires.group(1) if paires else "",
        "rss_go": f"{int(rss.group(1))/1e6:.2f}" if rss else "",
        "lus_go": f"{int(lus.group(1))*512/1e9:.2f}" if lus else "",
        "duree": duree.group(1) if duree else "",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="/tmp/campagne24")
    p.add_argument("--sortie", default="")
    a = p.parse_args()
    prefixes = sorted({os.path.basename(f)[:-4] for f in glob.glob(os.path.join(a.dir, "*.log"))
                       if not f.endswith("_temps.log")})
    lignes = [m for m in (mesure(x, a.dir) for x in prefixes) if m]
    # On ne garde que les lignes qui portent AU MOINS une mesure : les journaux
    # de tokenisation et les files d'attente n'ont rien à faire dans un tableau
    # de résultats.
    lignes = [l for l in lignes
              if l["ppl"] or l["tok_s"] or l["evenements"] or l["rss_go"]]
    if not lignes:
        print("aucune mesure trouvée", file=sys.stderr)
        return 1
    colonnes = ["etape", "ppl", "bits_octet", "jetons", "evenements", "tok_s",
                "en_listes", "paires", "rss_go", "lus_go", "duree"]
    titres = ["mesure", "perplexité", "bits/octet", "jetons", "événements", "tok/s",
              "en listes (M)", "paires (M)", "RSS (Go)", "lus (Go)", "durée"]
    out = ["| " + " | ".join(titres) + " |",
           "|" + "|".join(["---"] * len(titres)) + "|"]
    for l in lignes:
        out.append("| `" + "` | `".join(str(l[c]) for c in colonnes) + "` |")
    texte = "\n".join(out)
    print(texte)
    if a.sortie:
        with open(a.sortie, "w", encoding="utf-8") as f:
            f.write(texte + "\n")
        print(f"\n# écrit dans {a.sortie}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
