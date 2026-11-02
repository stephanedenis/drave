# Le corpus OCR du CEGEP — 10 notes scannées, 2 519 507 caractères

**Date** : 2026-11-02 (pilote de 05 h 52 à 11 h 25) · **Ligne** : Données · **Session** : fe3c05f0
**Statut** : **pilote clos** — 10 scans océrisés, manifeste `reports/ocr-pdf-cegep.json` ; le fonds CEGEP compte 2 681 PDF, la détection n'en a examiné que 41 avant la coupure `--max-doc 5`.

## 1. Ce que c'est

Le corpus OCR des **notes de cours du CEGEP** : les PDF sans couche texte du fonds `archives/CEGEP`, océrisés page à page par `tesseract`. C'est le complément CEGEP du corpus OCR des livres (`reports/rapport-ocr-pdf.md`).

## 2. Le chiffre

| grandeur | valeur |
|---|---:|
| scans océrisés | **10** |
| PDF examinés / scannés | 41 / 5 |
| pages | **1596** |
| caractères | **2 519 507** |
| mots estimés (car. / 6 2) | **194 944** |
| train / val / test | **2 464 185 o** / **86 688 o** / 0 |
| documents (train / val / test) | 3 / 2 / 0 |
| pages / scan | 2 à 366 |
| langues | fra+eng |
| tronçons 8 Ko (manifeste) | 307 |
| fenêtres 8 Ko (contrôle) | **302** train · **11** val · 0 test |
| doublons entre splits (8 Ko) | **0** (val) · **0** (test) |
| recouvrement éval | `fr-xnli.txt` **0/40**, `fr-udhr.txt` **0/24**, `en-xnli.txt` **0/40** |
| temps mur | ~2 h |
| WER | **non mesurée** |

## 3. Le dispositif

`tools/ocr_pdf.py --racine CEGEP --max-doc 5` : `pdftoppm -r 300 -gray -png` puis `tesseract -l fra+eng --psm 3` par page ; tesseract 5.5.3 sans root ; sortie `data/corpus_ocr_cegep/` ; manifeste `reports/ocr-pdf-cegep.json`. L'option `--racine` est nouvelle (restreindre le parcours à une racine). Les dix scans : *Exercices de synthèse Excel 2010* 43 p ; *AMF-AO-Annexes 12 à 15* 121 p ; *AMF-AO-Annexes 16 — Gabarits* 60 p ; *inscription AQPC* 2 p ; *programme du colloque 2016 de l'AQPC* 66 p ; *Algorithms Illuminated (Part 2)* 221 p ; *Algorithms Illuminated (Part 3)* 226 p ; *Algorithms Illuminated (Part 4)* 274 p ; *Algorithms Illuminated Part 1* 217 p ; *Data Structures and Algorithms in C* 366 p.

## 4. Le contrôle négatif

`verifie_contamination.py --taille-troncon 8192` : **54 fenêtres de 8 Ko** en train, **11** en val, **0 duplication** entre splits. Recouvrement avec les évaluations **mesuré** : `fr-xnli.txt` **0/40**, `fr-udhr.txt` **0/24**, `en-xnli.txt` **0/40** — aucune fenêtre trouvée.

## 5. Ce qui pourrait être faux

- **Le WER n'est pas mesuré** : pas de vérité terrain sur ces notes.
- Le texte est **brut** : pas de nettoyage R4.4 (casse, accents, césures).
- **Le pilote est partiel** : 10 scans sur les 41 PDF examinés (les 2 681 du fonds n'ont pas été tous parcourus — la coupure `--max-doc 40` est tombée sur un PDF de plus de 1 000 pages (voir ci-dessous)).
- Les notes sont des **documents de cours** (droits réservés, usage local, non diffusé) : le corpus ne sort pas de la machine.

## 6. La suite

> **Note** : le manifeste a été reconstruit après l'arrêt à 10 notes à 11 h 25 ; `documents` (train/val/test) n'est pas recompté, les octets et les SHA-256 sont ceux du disque. **Le 11e PDF — l'*Encyclopedia of Algorithms* (Ming-Yang Kao, 1 000+ pages) — a dépassé le timeout `pdftoppm` de 1 800 s et fait tomber le run** (`subprocess.TimeoutExpired` non rattrapé). Limite de l'outil : rendre ces monstres avec `--max-pages` (ou un timeout plus grand).

Le **fonds CEGEP complet** (2 681 PDF, détection + OCR) ; le pipeline R4.4 ; la fusion dans le corpus OCR global.

## 7. Les fichiers

- `tools/ocr_pdf.py` — l'OCR (option `--racine`)
- `data/corpus_ocr_cegep/` — train, val, test (gitignoré)
- `reports/ocr-pdf-cegep.json` — le manifeste
- `reports/ocr-pdf-cegep-contamination.json` — le contrôle 8 Ko
