# Le corpus OCR — les livres scannés, 20 livres, 15,4 M caractères

**Date** : 2026-11-01 (run de nuit ; 20e livre clos le 2/11 à 05 h 08) · **Ligne** : Données · **Session** : fe3c05f0
**Statut** : **clos** — 20 livres océrisés, manifeste `reports/ocr-pdf.json` ; les 159 scans restent la suite nommée.

## 1. Ce que c'est

Le corpus des **livres scannés** : les PDF sans couche texte, océrisés page à page par `tesseract`. C'est le complément des documents natifs : là où `pdftotext` ne trouve rien, l'OCR lit l'image.

## 2. Le chiffre

| grandeur | valeur |
|---|---:|
| livres océrisés | **20** |
| PDF examinés / scannés | 22 / 22 |
| pages | **7 381** |
| caractères | **15 356 972** |
| mots estimés (car. / 6,2) | **2 476 930** |
| train / val / test | **14 596 847 o** / **934 044 o** / 0 |
| documents (train / val / test) | 19 / 1 / 0 |
| pages / livre | 86 à 1 264 |
| langues | fra+eng |
| tronçons 8 Ko (manifeste) | 1 885 |
| fenêtres 8 Ko (contrôle) | **1 784** train (113 060 lignes) · **115** val · 0 test |
| doublons entre splits (8 Ko) | **0** (val) · **0** (test) |
| recouvrement éval | `fr-xnli.txt` **0/40**, `fr-udhr.txt` **0/24**, `en-xnli.txt` **0/40** |
| temps mur | 8.4 h |
| WER | **non mesurée** |

## 3. Le dispositif

`tools/ocr_pdf.py --max-doc 20` : `pdftoppm -r 300 -gray -png` (300 dpi, gris) puis `tesseract -l fra+eng --psm 3` par page ; tesseract 5.5.3 installé sans root (`work/ocr/root/usr/bin/tesseract`) ; sortie `data/corpus_ocr/` ; manifeste `reports/ocr-pdf.json`. **20 livres océrisés sur 22 examinés** : un `metapatterns` (373 p) était le doublon exact d'un autre — rejeté par la déduplication par empreinte (après OCR), et un PDF a été sauté faute de pages lisibles.

## 4. Le contrôle négatif

`verifie_contamination.py --taille-troncon 8192` : **1784 fenêtres de 8 Ko** en train, **115** en val, **0 duplication** entre splits (le val porte un livre, le test aucun). Recouvrement avec les évaluations **mesuré** : `fr-xnli.txt` **0/40**, `fr-udhr.txt` **0/24**, `en-xnli.txt` **0/40** — aucune fenêtre trouvée.

## 5. Ce qui pourrait être faux

- **Le WER n'est pas mesuré** : on ne sait pas la qualité de l'OCR (le R4.4 a posé le pipeline de mesure, pas encore appliqué à ce corpus).
- Le texte est **brut** : pas de nettoyage R4.4 (la casse, les accents, les césures peuvent être faux).
- Les livres choisis sont les **premiers** du fonds `Biblio_large` dans l'ordre du parcours, pas un échantillon aléatoire.
- **Un seul livre en val, aucun en test** : la mesure de généralisation est faible (115 fenêtres) ; les doublons exacts sont seuls détectés, pas les quasi-doublons.
- **Les doublons paient l'OCR** : la déduplication est par empreinte du texte, donc après coup (~15 min par copie).

## 6. La suite

Les **159 PDF scannés** du corpus PDF (le run `--max-doc 20` est un pilote) ; le pipeline R4.4 (nettoyage + WER) ; la fiche finale.

## 7. Les fichiers

- `tools/ocr_pdf.py` — l'OCR
- `data/corpus_ocr/` — train, val, test (gitignoré)
- `reports/ocr-pdf.json` — le manifeste
- `reports/ocr-pdf-contamination.json` — le contrôle 8 Ko
- `journal/2026-11-01/README.md` — le récit
