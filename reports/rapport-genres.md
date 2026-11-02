# Le genre se mesure — encyclopédie, livres, documents, cours

**Date** : 2026-11-01 · **Ligne** : Données · **Session** : fe3c05f0

## 1. Ce que c'est

La comparaison des **genres** : les 10 corpus Wikipédia (l'encyclopédie), le corpus PDF (les livres et manuels), le corpus Documents (les documents personnels) et le corpus OCR (les livres scannés). Les **200 premiers Mo** de chaque train, mesurés par `tools/compare_genres.py` : la longueur de ligne, la part de lignes dupliquées, la couverture lexicale.

## 2. Le chiffre

| corpus | car/ligne | lignes dup. | couverture |
|---|---:|---:|---:|
| en (wiki) | 146,8 | 9,6 % | 0,01 |
| es (wiki) | 127,4 | 10,7 % | 0,01 |
| pt (wiki) | 116,9 | 15,1 % | 0,01 |
| de (wiki) | 115,8 | 8,7 % | 0,03 |
| it (wiki) | 113,1 | 18,4 % | 0,02 |
| fr (wiki) | 111,1 | 15,1 % | 0,01 |
| ru (wiki) | 107,2 | 13,5 % | 0,14 |
| ar (wiki) | 103,1 | 16,2 % | 0,22 |
| ja (wiki) | 42,0 | 11,8 % | 0,09 |
| zh (wiki) | 40,8 | 13,5 % | 0,12 |
| pdf (livres) | 37,2 | 23,8 % | 0,01 |
| documents | 37,5 | 22,1 % | 0,01 |
| ocr (scannés) | 32,1 | 4,8 % | 0,07 |

## 3. Le constat

- **La longueur de ligne sépare les genres** : l'encyclopédie écrit des paragraphes longs (103 à 147 caractères), les livres et documents des lignes courtes (32 à 37) — c'est la mise en page, pas le contenu.
- **Les lignes dupliquées** : le PDF et les documents ont le plus de répétitions (22 à 24 % : les en-têtes, les numéros de page, les formules), l'OCR le moins (4,8 %) ; l'encyclopédie est entre les deux (8,7 à 18,4 %).
- **La couverture lexicale** (types/tokens sur 200 Mo) est écrasée par la taille de l'échantillon : 0,01 pour les grands corpus, 0,22 pour l'arabe (les formes fléchies), 0,07 pour l'OCR (peu de texte).

## 4. Ce qui pourrait être faux

- L'échantillon est **tronqué à 200 Mo** : les corpus plus grands sont sous-représentés en couverture.
- La couverture lexicale dépend de la **langue** (l'arabe et le russe ont plus de formes fléchies que l'anglais) — elle ne mesure pas le genre.
- Le corpus OCR est **petit** (3,7 M) : ses chiffres bougeront avec les 159 scans.
- Le corpus Documents est **partiel** (6 000/7 496 PDF) : ses chiffres bougeront à la clôture.

## 5. La suite

Les 159 PDF scannés (l'OCR complet) ; la comparaison des **trigrammes** (le style) ; puis les tests de **genre** sur le modèle (R1.1/R1.2).

## 6. Les fichiers

- `tools/compare_genres.py` — l'outil
- `reports/corpus-genres.json` — les chiffres
