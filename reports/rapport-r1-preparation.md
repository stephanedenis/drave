# La préparation de R1.1/R1.2 — ce qui est prêt, ce qui bloque

**Date** : 2026-11-02 · **Ligne** : Données · **Session** : fe3c05f0

## 1. Ce que R1.1/R1.2 demandent

R1.1 et R1.2 sont les mesures du **lecteur** sur les corpus préparés : la politique de lecture (fenêtre, mémoire, restitution) appliquée à des documents réels, puis la **hiérarchie** qui décide quoi lire. La préparation D/R/A consiste à fournir les corpus, les évaluations et les contrôles — pas à exécuter la hiérarchie, qui est portée par N2.

## 2. Ce qui est prêt (D/R/A)

- Les **dix corpus Wikipédia en texte intégral** : 20,53 M articles, 67,73 G caractères, 81,2 Go, **8 Ko 0** partout.
- Le **corpus PDF** : 1 927 documents, 322 Mo, 8 Ko 0.
- Le **corpus Documents** : 3 384 documents, 872 M caractères, **8 Ko 2,07 %** (les tronçons dupliqués).
- Le **corpus OCR** : 8 livres, 4,2 M caractères (le 8e en cours).
- Les **évaluations locales** : XNLI (ar/de/en/es/fr/ru/zh), UDHR (fra/ita/jpn/por), wikitext2 — et leurs contrôles de contamination.
- La **comparaison des genres** : l'encyclopédie 103–147 car/ligne, les livres et documents 32–37, les lignes dupliquées 8,7–24 % (l'OCR 4,8 %).

## 3. Ce qui bloque

- La **hiérarchie de lecture** (R1.1/R1.2) est portée par **N2** : c'est N2 qui a la hiérarchie et le `drave-n0`. La préparation D/R/A est faite ; l'exécution attend N2.
- Les **GPU de N2** ne sont pas touchés par cette session.

## 4. La suite

Dès que N2 livre sa hiérarchie, R1.1/R1.2 se mesurent sur les corpus préparés : les documents, le PDF, l'OCR et les dix corpus Wikipédia sont les entrées ; les évaluations et les contrôles 8 Ko sont les garde-fous.

## 5. Les fichiers

- `reports/rapport-corpus-wiki-texte.md` — les dix corpus
- `reports/rapport-corpus-documents.md` — les documents
- `reports/rapport-ocr-pdf.md` — l'OCR
- `reports/rapport-genres.md` — les genres
- `reports/corpus-wiki-*-texte-contamination.json` — les contrôles 8 Ko
