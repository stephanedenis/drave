# Le corpus OCR — les livres scannés, 8 livres, 7,7 M caractères

**Date** : 2026-11-01 (run de nuit ; 8e livre clos le 2/11 à 01 h 16) · **Ligne** : Données · **Session** : fe3c05f0
**Statut** : en cours (8 livres océrisés au 2/11 01 h 16 ; le 9e — CSS — est en OCR ; la clôture figera les chiffres).

## 1. Ce que c'est

Le corpus des **livres scannés** : les PDF sans couche texte, océrisés page à page par `tesseract`. C'est le complément des documents natifs : là où `pdftotext` ne trouve rien, l'OCR lit l'image.

## 2. Le chiffre (au 2/11 01 h 16)

| grandeur | valeur |
|---|---:|
| livres océrisés | **8** |
| pages | **2 815** |
| caractères | **7 688 789** |
| train / val / test | **7 776 329 o** / 0 / 0 |
| pages / livre | 16 à 1 264 |
| langues | fra+eng |
| fenêtres 8 Ko (train) | **951** (54 249 lignes) |
| doublons entre splits (8 Ko) | **0** (val/test vides) |
| WER | **non mesurée** |

Les huit livres : 3dprintingandreprap 134 p ; Bioinformatics for beginners 225 p ; metapatterns 373 p ; Brown 2015 376 p ; Dictionnaire des… 249 p ; La maison de A à… 178 p ; Product Manual(F7) 16 p ; **Sprenger 2025, inflammationcycling 1 264 p**.

## 3. Le dispositif

`tools/ocr_pdf.py --max-doc 20` : `pdftoppm -r 300 -gray -png` (300 dpi, gris) puis `tesseract -l fra+eng --psm 3` par page ; tesseract 5.5.3 installé sans root (`work/ocr/root/usr/bin/tesseract`) ; sortie `data/corpus_ocr/` ; manifeste `reports/ocr-pdf.json` (à la fin).

## 4. Le contrôle négatif

`verifie_contamination.py --taille-troncon 8192` : **951 fenêtres de 8 Ko** en train, 0 duplication entre splits. **Le contrôle croisé est trivialement nul** : le hash salé du chemin a placé les 8 documents en train, val/test sont vides — c'est une limite, pas une preuve. Aucun recouvrement avec les évaluations (wikitext2, XNLI, UDHR) n'a été cherché ici : le corpus OCR est un corpus de livres, pas de Wikipédia.

## 5. Ce qui pourrait être faux

- **Le WER n'est pas mesuré** : on ne sait pas la qualité de l'OCR (le R4.4 a posé le pipeline de mesure, pas encore appliqué à ce corpus).
- Le texte est **brut** : pas de nettoyage R4.4 (la casse, les accents, les césures peuvent être faux).
- Les livres choisis sont les **premiers** du fonds `Biblio_large`, pas un échantillon aléatoire.
- **val/test vides** : les 8 documents sont tous en train ; le prochain lot (les 20 scannés) doit en placer, sinon la mesure de généralisation n'existe pas.

## 6. La suite

Les 159 PDF scannés du corpus PDF (le 9e — CSS — est en OCR) ; le pipeline R4.4 (nettoyage + WER) ; la fiche finale.

## 7. Les fichiers

- `tools/ocr_pdf.py` — l'OCR
- `data/corpus_ocr/` — train, val, test (gitignoré)
- `reports/ocr-pdf.json` — le manifeste (à la fin)
- `reports/ocr-pdf-contamination.json` — le contrôle 8 Ko du lot
- `journal/2026-11-01/README.md` — le récit
