# Le corpus Documents — 7 496 PDF locaux, 2 992 documents, 845,7 M caractères

**Date** : 2026-11-01 · **Ligne** : Données · **Session** : fe3c05f0
**Statut** : **terminé** (7 459 PDF, manifeste `reports/corpus-pdf-documents.json`).

## 1. Ce que c'est

Le corpus des **documents personnels** : les 7 496 PDF du fonds `Documents/` (livres, manuels, articles, notes), lus un à un par `pdftotext`. C'est le volume le plus personnel de la campagne : il ne ressemble ni à une encyclopédie ni à un corpus scolaire, et c'est précisément ce qui le rend utile — le genre « documents personnels » est le troisième pilier de la comparaison de genres.

## 2. Le chiffre (au 1/11 23 h 12)

| grandeur | valeur |
|---|---:|
| PDF lus | **7 459** |
| pages | 803 817 |
| documents gardés | **3 384** |
| documents scannés | 1 017 |
| documents courts | 1 316 |
| doublons de documents | 1 742 |
| caractères | **871 972 648** |
| train / val / test | 803,0 Mo / 49,6 Mo / 34,4 Mo |
| tronçons 8 Ko | 107 976 (372 doublons) |
| licences | personnel — usage local, non diffusé |

## 3. Le dispositif

`tools/extrait_pdf.py` : `pdftotext -enc UTF-8` par PDF (délai **120 s** par fichier), détection des scannés (< 50 caractères/page), des courts (< 300 caractères), des doublons (BLAKE2b), split par hash salé du chemin (5 % val, 5 % test), tronçons de 8 192 caractères. Manifeste `reports/corpus-pdf-documents.json` (écrit à la fin).

## 4. Le contrôle négatif

Les doublons exacts et les tronçons : la mesure 8 Ko tranchera à la fin. Les évaluations locales (wikitext2) seront cherchées dans le corpus pour vérifier qu'aucun document ne recoupe une évaluation.

## 5. Ce qui pourrait être faux

- **45 % des PDF seulement** sont gardés (3 384 sur 7 459) : 1 017 sont des scans (sans couche texte), 1 316 trop courts, 1 742 doublons. Les scans iront à l'OCR.
- Les licences sont **personnelles** : usage local, non diffusé ; le corpus ne sortira pas du dépôt.
- Le texte extrait d'un PDF n'est pas du texte natif : les colonnes, les notes de bas de page et les formules peuvent être mélangés.

## 6. La suite

La mesure 8 Ko (en cours), les évaluations ; puis l'OCR des 1 017 scans du corpus Documents.

## 7. Les fichiers

- `tools/extrait_pdf.py` — l'extraction
- `data/corpus_pdf_documents/` — train, val, test (gitignoré)
- `reports/corpus-pdf-documents.json` — le manifeste (à la fin)
- `journal/2026-11-01/README.md` — le récit
