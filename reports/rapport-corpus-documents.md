# Le corpus Documents — 7 496 PDF locaux, 2 992 documents, 845,7 M caractères

**Date** : 2026-11-01 · **Ligne** : Données · **Session** : fe3c05f0
**Statut** : en cours (6 000 PDF sur 7 496 au 1/11 23 h 12) ; les chiffres finaux seront ajoutés à la clôture.

## 1. Ce que c'est

Le corpus des **documents personnels** : les 7 496 PDF du fonds `Documents/` (livres, manuels, articles, notes), lus un à un par `pdftotext`. C'est le volume le plus personnel de la campagne : il ne ressemble ni à une encyclopédie ni à un corpus scolaire, et c'est précisément ce qui le rend utile — le genre « documents personnels » est le troisième pilier de la comparaison de genres.

## 2. Le chiffre (au 1/11 23 h 12)

| grandeur | valeur |
|---|---:|
| PDF lus | 6 000 / 7 496 |
| documents gardés | 2 992 |
| caractères | 845,7 M |
| train / val / test | 789,9 Mo / 49,3 Mo / 32,7 Mo |
| tronçons 8 Ko | à la fin |
| doublons 8 Ko | à la fin |
| licences | personnel — usage local, non diffusé |

## 3. Le dispositif

`tools/extrait_pdf.py` : `pdftotext -enc UTF-8` par PDF (délai **120 s** par fichier), détection des scannés (< 50 caractères/page), des courts (< 300 caractères), des doublons (BLAKE2b), split par hash salé du chemin (5 % val, 5 % test), tronçons de 8 192 caractères. Manifeste `reports/corpus-pdf-documents.json` (écrit à la fin).

## 4. Le contrôle négatif

Les doublons exacts et les tronçons : la mesure 8 Ko tranchera à la fin. Les évaluations locales (wikitext2) seront cherchées dans le corpus pour vérifier qu'aucun document ne recoupe une évaluation.

## 5. Ce qui pourrait être faux

- Le corpus est **partiel** : les PDF lourds (plus de 120 s) sont coupés par le délai et comptés « courts » ; leur part exacte sera dans le manifeste.
- Les licences sont **personnelles** : usage local, non diffusé ; le corpus ne sortira pas du dépôt.
- Le texte extrait d'un PDF n'est pas du texte natif : les colonnes, les notes de bas de page et les formules peuvent être mélangés.

## 6. La suite

Les 1 496 PDF restants ; puis la mesure 8 Ko, les évaluations et la fiche finale (les chiffres du § 2 seront figés).

## 7. Les fichiers

- `tools/extrait_pdf.py` — l'extraction
- `data/corpus_pdf_documents/` — train, val, test (gitignoré)
- `reports/corpus-pdf-documents.json` — le manifeste (à la fin)
- `journal/2026-11-01/README.md` — le récit
