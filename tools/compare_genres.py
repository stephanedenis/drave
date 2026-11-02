#!/usr/bin/env python3
"""Le genre se mesure — encyclopédie, livres, documents, cours (2026-11-01).

Pour chaque corpus (les 10 Wikipédia, le PDF, les documents, l'OCR) :
- les caractères, les lignes, la longueur moyenne de ligne ;
- la part d'alphanumérique, de chiffres, de ponctuation ;
- le taux de lignes dupliquées (les en-têtes, les formules) ;
- la couverture lexicale sur un échantillon (types / tokens).

Usage : python3 tools/compare_genres.py [--sortie reports/corpus-genres.json]
"""
import json
import pathlib
import re
import sys

ECHANTILLON = 200_000_000  # 200 Mo par corpus


def lit_morceau(chemin, limite=ECHANTILLON):
    with open(chemin, 'rb') as f:
        return f.read(limite)


def mesure(chemin):
    donnees = lit_morceau(chemin)
    texte = donnees.decode('utf-8', errors='replace')
    lignes = texte.split('\n')
    n = len(texte)
    alpha = sum(c.isalpha() for c in texte) / max(n, 1)
    chiffres = sum(c.isdigit() for c in texte) / max(n, 1)
    espaces = sum(c.isspace() for c in texte) / max(n, 1)
    ponct = max(0.0, 1 - alpha - chiffres - espaces)
    vues = set()
    dup = 0
    for ligne in lignes:
        if ligne.strip() and ligne in vues:
            dup += 1
        vues.add(ligne)
    mots = re.findall(r"[a-zàâçéèêëîïôûùüÿñæœ]+", texte.lower())
    types = len(set(mots))
    tokens = len(mots)
    return {
        "caracteres": n, "lignes": len(lignes),
        "longueur_moyenne": round(n / max(len(lignes), 1), 1),
        "alpha": round(alpha, 3), "chiffres": round(chiffres, 3),
        "espaces": round(espaces, 3), "ponctuation": round(ponct, 3),
        "lignes_dupliquees": round(dup / max(len(lignes), 1), 4),
        "types": types, "tokens": tokens,
        "couverture": round(types / max(tokens, 1), 3),
    }


CORPUS = {
    "fr": "data/corpus_wiki_fr_texte/train.txt",
    "ar": "data/corpus_wiki_ar_texte/train.txt",
    "pt": "data/corpus_wiki_pt_texte/train.txt",
    "zh": "data/corpus_wiki_zh_texte/train.txt",
    "ja": "data/corpus_wiki_ja_texte/train.txt",
    "it": "data/corpus_wiki_it_texte/train.txt",
    "ru": "data/corpus_wiki_ru_texte/train.txt",
    "es": "data/corpus_wiki_es_texte/train.txt",
    "de": "data/corpus_wiki_de_texte/train.txt",
    "en": "data/corpus_wiki_en_texte/train.txt",
    "pdf": "data/corpus_pdf/train.txt",
    "documents": "data/corpus_pdf_documents/train.txt",
    "ocr": "data/corpus_ocr/train.txt",
}


def main():
    sortie = "reports/corpus-genres.json"
    for i, a in enumerate(sys.argv):
        if a == "--sortie" and i + 1 < len(sys.argv):
            sortie = sys.argv[i + 1]
    resultats = {}
    for nom, chemin in CORPUS.items():
        p = pathlib.Path(chemin)
        if not p.exists():
            continue
        r = mesure(chemin)
        resultats[nom] = r
        print(f"{nom:10s} {r['caracteres']:>12d} car · "
              f"{r['longueur_moyenne']:>6.1f} car/ligne · "
              f"dup {r['lignes_dupliquees']:.1%} · "
              f"cov {r['couverture']:.2f}")
    pathlib.Path(sortie).write_text(
        json.dumps(resultats, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"→ {sortie}")


if __name__ == "__main__":
    main()
