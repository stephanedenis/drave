# Le corpus OCR — les livres scannés, 6 livres, 3,8 M caractères

**Date** : 2026-11-01 · **Ligne** : Données · **Session** : fe3c05f0
**Statut** : en cours (6 livres océrisés au 1/11 23 h 12) ; les chiffres finaux seront ajoutés à la clôture.

## 1. Ce que c'est

Le corpus des **livres scannés** : les PDF sans couche texte, océrisés page à page par `tesseract`. C'est le complément des documents natifs : là où `pdftotext` ne trouve rien, l'OCR lit l'image.

## 2. Le chiffre (au 1/11 23 h 12)

| grandeur | valeur |
|---|---:|
| livres océrisés | 6 |
| caractères | 3,8 M |
| train / val / test | 3,8 Mo / … / … |
| pages / livre | 225 à 376 |
| langues | fra+eng |
| WER | **non mesurée** |

## 3. Le dispositif

`tools/ocr_pdf.py` : `pdftoppm -r 300 -gray -png` (300 dpi, gris) puis `tesseract -l fra+eng --psm 3` par page ; tesseract 5.5.3 installé sans root (`work/ocr/root/usr/bin/tesseract`) ; sortie `data/corpus_ocr/` ; manifeste `reports/ocr-pdf.json` (à la fin).

## 4. Le contrôle négatif

Aucun recouvrement avec les évaluations (wikitext2) ne sera mesuré ici : le corpus OCR est un corpus de **livres**, pas de Wikipédia. La mesure 8 Ko tranchera à la fin.

## 5. Ce qui pourrait être faux

- **Le WER n'est pas mesuré** : on ne sait pas encore la qualité de l'OCR (le R4.4 a posé le pipeline de mesure, pas encore appliqué à ce corpus).
- Le texte est **brut** : pas de nettoyage R4.4 (la casse, les accents, les césures peuvent être faux).
- Les livres choisis sont les **premiers** du fonds `Biblio_large`, pas un échantillon aléatoire.

## 6. La suite

Les 159 PDF scannés du corpus PDF ; le pipeline R4.4 (nettoyage + WER) ; la fiche finale.

## 7. Les fichiers

- `tools/ocr_pdf.py` — l'OCR
- `data/corpus_ocr/` — train, val, test (gitignoré)
- `reports/ocr-pdf.json` — le manifeste (à la fin)
- `journal/2026-11-01/README.md` — le récit
