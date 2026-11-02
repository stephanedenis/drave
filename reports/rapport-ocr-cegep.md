# Le corpus OCR du CEGEP — 147 scans détectés, 91 uniques, 1 982 pages océrisées

**Date** : 2026-11-02 (détection 16 h 35–16 h 46, OCR 16 h 31–18 h 28) · **Ligne** : Données · **Session** : `fe3c05f0`
**Statut** : **fonds `.pdf` parcouru** — 91 scans uniques, **60 documents retenus** (1 982 p), 31 écartés (texte OCR < 300 car. ou doublon) ; 8 scans en `.PDF` hors parcours (limite nommée) ; manifeste `reports/ocr-pdf-cegep.json` ; le fonds CEGEP compte 2 681 PDF, dont 147 sans couche texte (2 701 p), 91 uniques (2 053 p).

## 1. Ce que c'est

Le corpus OCR des **documents sans couche texte** du fonds CEGEP (`archives/CEGEP`), océrisés page à page par `tesseract` (300 dpi, `fra+eng` ; reprise MicroPython à 150 dpi). Il complète le corpus des 20 livres scannés (`rapport-ocr-pdf.md`) et le corpus PDF natif (`corpus-pdf`). Les notes de cours sont des documents à droits réservés : usage local, non diffusé.

## 2. Le chiffre

| grandeur | valeur |
|---|---:|
| scans détectés (texte intégral) | **147** |
| dont doublons exacts (SHA-256) | **56** |
| scans uniques | **91** |
| pages des uniques | **2 053** |
| documents retenus (≥ 300 car.) | **60** |
| pages océrisées | **1 982** |
| caractères | **4 408 811** |
| mots estimés (car. / 6,2) | **711 098** |
| train / val / test (octets) | **4 430 959** / **12 536** / **10 524** |
| documents train / val / test | **53** / **4** / **3** |
| tronçons 8 Ko | **573** |
| temps mur | **118 min** |
| WER | **non mesurée** |

## 3. Le dispositif

1. **Détection intégrale** — `python3 tools/detecte_scans_pdf.py --racine CEGEP --sortie reports/ocr-pdf-cegep-detection.json --liste work/ocr/scans-uniques.txt` : `pdfinfo` + `pdftotext` **complet**, seuil **50 caractères natifs par page** (la règle de `extrait_pdf.py`), puis **SHA-256** des fichiers pour retirer les doublons exacts. 2 681 PDF → **147 scans** → **91 uniques**.
2. **OCR sur liste explicite** — `python3 tools/ocr_pdf.py --liste work/ocr/scans-uniques.txt --racine CEGEP --sortie data/corpus_ocr_cegep --manifeste reports/ocr-pdf-cegep.json --ouvriers 8` : `pdftoppm -r 300 -gray -png`, `tesseract -l fra+eng --psm 3`, huit pages en parallèle (`OMP_THREAD_LIMIT=1`, mesuré **1,5 s/page à 1 thread** contre **2,0 s à 2**). Dédup des documents par empreinte du texte OCR, puis des tronçons (train).
3. **La reprise MicroPython** — le PDF de 359 p dépasse le timeout `pdftoppm` de 1 800 s à 300 dpi ; il est repris à **150 dpi** (`python3 tools/ocr_pdf.py --liste work/ocr/micro.txt --racine CEGEP --sortie data/corpus_ocr_cegep_micro --manifeste work/ocr/micro-manifest.json --dpi 150 --ouvriers 8` : 359 p, 350 310 car., 23 min) ; ses splits sont concaténés au corpus et les compteurs du manifeste additionnés (`work/ocr/ajoute_micro.py`, non committé) ; le manifeste porte `dispositif.reprise_micropython`.
4. **Splits** : hash salé du chemin (`graine=1`) — 5 % val, 5 % test ; les mêmes règles que les autres corpus.

## 4. Le contrôle négatif

- **La détection à deux pages sur-classifie 5,5×** : la même règle appliquée aux deux premières pages donne **807 candidats** (179 426 p) ; le texte intégral en confirme **147** (2 701 p). Les 660 faux positifs sont des livres natifs dont la couverture et la page de titre n'ont pas de texte. Sur les **10 notes du pilote**, **9** sont des livres natifs (463 à 1 706 car/p : *Algorithms Illuminated* 1–4, *Data Structures in C*, Excel, AMF-AO) ; **seul *inscription AQPC* (2 p, 0 car.) est un scan**.
- **Doublons** : 56 fichiers identiques retirés avant OCR (648 p), dont une seconde copie du *Tesla* de 499 p et les documents de révision dupliqués.
- **8 Ko** : `verifie_contamination.py --taille-troncon 8192` — **542** fenêtres en train, **2** en val, **2** en test, **0** duplication entre splits. Le contrôle des **lignes exactes** trouve **5 lignes courtes** du val dans le train (6,5 % des 77 lignes ; en-têtes de formulaires, pas des fenêtres de 8 Ko).
- **Évaluations** : recouvrement mesuré — `fr-xnli.txt` **0/40**, `fr-udhr.txt` **0/24**, `en-xnli.txt` **0/40**.

## 5. Ce qui pourrait être faux

- **La WER n'est pas mesurée** : pas de vérité terrain sur ces scans ; le chiffre est un volume, pas une fidélité.
- L'OCR est **brut** : rotation, contraste, colonnes et césures ne sont pas traités (le pipeline R4.4 les traite).
- **MicroPython à 150 dpi** : le rendu à 300 dpi dépasse le timeout ; la reprise est moins fine (WER non mesurée).
- **`--min-chars 300`** : les photos et formulaires courts sont détectés mais **non retenus** (31 documents sur 91, 71 p) ; le corpus privilégie le texte, pas l'exhaustivité des images.
- **30 PDF en `.PDF`** (majuscules) échappent à `rglob("*.pdf")` : 8 scans, 58 p (6 uniques) — mesuré, **hors corpus**, à reprendre avec un parcours insensible à la casse.
- La détection dépend de `pdftotext` : un PDF protégé ou illisible peut être classé scan ou écarté (timeout 120 s).

## 6. L'erratum du pilote

Le pilote du 02/11 (05 h 52–11 h 25) avait océrisé **10 « notes »**, 1 596 pages, 2 519 507 caractères, sur la détection à deux pages. Le contrôle intégral montre que **neuf** de ces dix PDF ont une couche texte native : l'OCR y était **redondant** avec le corpus PDF natif. Le corpus du pilote est archivé localement (`data/corpus_ocr_cegep_pilote-2pages/`) et **n'entre pas** dans le corpus ; `data/corpus_ocr_cegep/` est refait sur les 91 scans uniques. **Leçon** : une détection d'OCR se mesure sur la couche texte **intégrale**, jamais sur deux pages ; et une reprise écrit dans une **sortie séparée** (leçon du run `--deja 41`).

## 7. Les fichiers

- `tools/detecte_scans_pdf.py` — la détection intégrale, la déduplication, la liste.
- `tools/ocr_pdf.py` — l'OCR (`--liste`, `--ouvriers`, date du manifeste corrigée).
- `reports/ocr-pdf-cegep-detection.json` — 2 681 PDF, 147 scans, 91 uniques, 2 053 p.
- `reports/ocr-pdf-cegep.json` — le manifeste du corpus.
- `reports/ocr-pdf-cegep-contamination.json` — le contrôle 8 Ko et évaluations.
- `data/corpus_ocr_cegep/` — train, val, test (gitignoré) ; `data/corpus_ocr_cegep_pilote-2pages/` — archive du pilote.

## 8. La suite

L'OCR des **8 scans `.PDF`** (58 p, parcours insensible à la casse) ; le **pipeline R4.4** (nettoyage) ; la **WER** quand une vérité terrain existera ; la fusion avec les 20 livres et le corpus natif.
