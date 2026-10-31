# R4.4 — l'OCR lit dix pages à 4,48 % de WER, parité 90 %, et la page « photo » tombe à 26,7 %

> **Objet.** La ligne R4.4 était **bloquée** par une ressource absente, pas par une question
> ouverte : « aucun OCR installé (ni tesseract ni pytesseract) ». Ce pilote installe l'OCR sans
> root, le branche sur le graphe de document de R0.1 et mesure ce qu'il vaut : WER contre le
> texte natif de la **même page**, parité des réponses sur les questions du banc R0.3, et deux
> contrôles négatifs. **Il ne clôt pas R4.4** : les pages sont des **rendus propres**, pas des
> scans — le contrôle dégradé mesure exactement ce qui manque encore.

## Dispositif

- **Dix pages** rendues à **300 dpi** depuis **6 PDF** du corpus gelé, **3 langues** (fr, en, es) :
  les 9 pages qui portent les **30 questions** du banc `bench-complet.json` (type juridique) et
  une page de plus (`A_RES_80_1-en` p2) pour le WER.
- **OCR** : tesseract **5.5.3** (leptonica 1.87.0), langues `fra`, `eng`, `spa`, installé **sans
  root** par [`tools/installer_ocr.sh`](../tools/installer_ocr.sh) dans `work/ocr/root`.
- **Lecture** : sortie TSV de tesseract (mots, boîtes, **confiance**) → blocs
  ([`graphe_document_ocr.py`](../tools/graphe_document_ocr.py)) → **même** manifeste que le PDF
  natif ([`graphe_document.manifeste_de_blocs`](../tools/graphe_document.py)) : offsets, partition
  et provenance identiques. Le même lecteur extractif R0.2 lit les deux côtés.
- **Mesure** : [`tools/mesurer_ocr.py`](../tools/mesurer_ocr.py) ; JSON
  [`r44-ocr-pilote.json`](r44-ocr-pilote.json) ; porte [`tools/porte-ocr.sh`](../tools/porte-ocr.sh).

## Résultat — le texte

| page | langue | mots natifs | WER | rappel | confiance | questions |
|---|---|---:|---:|---:|---:|---:|
| A_RES_80_10-fr p2 | fra | 558 | **2,15 %** | 97,85 % | 94,3 | 5 |
| A_RES_80_10-en p2 | eng | 546 | **1,10 %** | 98,90 % | 94,8 | 4 |
| A_RES_80_10-es p2 | spa | 577 | **2,08 %** | 98,09 % | 94,5 | 4 |
| A_RES_80_1-en p1 | eng | 294 | 4,76 % | 98,30 % | 93,5 | 3 |
| A_RES_80_1-es p1 | spa | 326 | 5,52 % | 98,77 % | 92,9 | 3 |
| A_RES_80_1-fr p1 | fra | 315 | 4,44 % | 99,68 % | 90,5 | 3 |
| A_RES_80_10-en p1 | eng | 316 | 9,18 % | 93,04 % | 91,5 | 3 |
| A_RES_80_10-es p1 | spa | 284 | 9,15 % | 94,72 % | 92,1 | 3 |
| A_RES_80_10-fr p1 | fra | 305 | 12,13 % | 92,79 % | 89,4 | 2 |
| A_RES_80_1-en p2 | eng | 250 | 0,40 % | 99,60 % | 95,7 | 0 |

**Agrégat** : **3 771 mots**, **169 éditions** → **WER 4,48 %** · rappel **97,37 %** ·
précision **97,82 %** · confiance moyenne pondérée par les mots **93,2**.

Le WER est mot à mot (Levenshtein sur les jetons), pas caractère à caractère : c'est le mot que
les questions du banc manipulent. Le rappel est le multiensemble des mots natifs retrouvés ; la
précision, la part des mots OCR qui existent dans le natif — une OCR qui invente du texte paie
donc deux fois. La **confiance** de chaque bloc est dans la provenance (`prov.confiance`) : une
lecture qui ne dit pas son score ne serait pas une lecture.

## Résultat — la parité

**30 questions** du banc R0.3 (juridique), lues par **le même** lecteur extractif sur le
manifeste natif et sur le manifeste OCR de la **même page** :

| mesure | natif | OCR |
|---|---:|---:|
| la **valeur** de la question est dans le passage choisi | **30/30 (100 %)** | **25/30 (83,33 %)** |
| le **passage** choisi est le même (F1 mots ≥ 0,90) | — | **27/30 (90,00 %)** |
| F1 médian du passage choisi | — | **1,000** |
| contrôle **sans OCR** (manifeste vide) | — | **0/30 (0,00 %)** |

Les **3** échecs de la parité de passage, nommés :

| page | valeur | F1 | cause |
|---|---|---:|---|
| A_RES_80_1-fr p1 | 13 | 0,214 | **découpage** : la valeur est dans l'en-tête OCR (`Point 13`), mais le bloc est découpé autrement ; le lecteur choisit « social et dans les domaines connexes » |
| A_RES_80_10-es p1 | 13 | 0,143 | **découpage** : même cause (`Tema 13`), le lecteur choisit « esferas conexas » |
| A_RES_80_10-es p1 | 2200 | 0,800 | **lecture** : `XXI` lu `XXD` dans « resolución 2200 A (XXI) » ; la valeur 2200, elle, est trouvée des deux côtés |

Les **5** échecs de la valeur stricte ajoutent les **appels de note en exposant**, que tesseract
lit `!`, `!!` ou pas du tout :

| page | valeur | natif | OCR |
|---|---|---:|---|
| A_RES_80_10-fr p2 | `10` | ✓ | ✗ — l'appel de note de « … et le développement 10 , » disparaît |
| A_RES_80_10-fr p2 | `2030 11` | ✓ | ✗ — « … à l'horizon 2030 11 et » devient « … 2030!! et » |
| A_RES_80_10-fr p2 | `12` | ✓ | ✗ — « … des femmes 12 et » perd l'appel |
| A_RES_80_1-fr p1 | `13` | ✓ | ✗ — découpage (même cas que ci-dessus) |
| A_RES_80_10-es p1 | `13` | ✓ | ✗ — découpage (même cas que ci-dessus) |

**Ce que la parité mesure, et ce qu'elle ne mesure pas.** Le critère du backlog — « 10 pages
scannées donnent la même réponse que le texte natif » — est tenu au niveau du **passage lu**
(27/30), pas au niveau du **chiffre exact** (25/30). Les deux écarts de découpage et les trois
exposants sont la même famille : le **layout**, pas la reconnaissance des mots. C'est le
prochain chantier de R4.4, et il est nommé.

## Les contrôles négatifs

| contrôle | ce qu'il devait faire | ce qu'il fait |
|---|---|---|
| **sans OCR** (manifeste vide) | aucune réponse | **0/30** |
| **page dégradée** (photo simulée : 0,35× la définition, flou, JPEG q20, 0,8° de travers) | le WER monte, la parité baisse | **WER 17,08 %** contre 4,48 % · exactitude **12/30 (40 %)** · parité de passage **8/30 (26,67 %)** · confiance **83,7** contre 93,2 |
| **rejeu** | le même chiffre deux fois | **aucun écart** d'agrégat ni de question entre deux passes (rendus et OCR en cache) |

Le contrôle dégradé est le plus important : **la parité tombe de 90 % à 26,7 %**. C'est la
mesure de ce que R4.4 n'a pas encore : la **robustesse aux scans**. Un rendu vectoriel à 300 dpi
est un document parfait ; une photo de téléphone ne l'est pas.

## Ce qui n'est pas tenu (et qui reste ouvert)

1. **Les scans réels.** Le dispositif part du **PDF vectoriel** ; il n'y a pas de corpus de
   photocopies. Le contrôle dégradé simule, il ne remplace pas.
2. **Les exposants** (appels de note) : 3/30 des valeurs du banc sont des appels de note choisis
   comme valeurs par le générateur de questions (il prend le premier nombre du passage). Un
   défaut du **banc** autant que de l'OCR — et il est maintenant visible.
3. **Le layout** : deux découpages d'en-tête différents suffisent à changer le passage choisi.
   Pas de colonnes, pas de tableaux, pas de rotation réelle dans ce pilote.
4. **La langue** : trois langues latines, pas de cyrillique ni de CJK ; `spa` a été installé
   pour le corpus, pas parce que le choix est mesuré.

## Lecture

- L'OCR **lit le français, l'anglais et l'espagnol** d'un PDF propre à **4,48 %** de WER, avec une
  confiance **93,2** : le texte est là, et il est là **au bon endroit** (rappel 97,4 %).
- La **parité de passage à 90 %** dit que le lecteur extractif de R0.2 se comporte presque
  pareil sur les deux lectures ; les trois écarts sont nommés et n'invalident pas la lecture.
- Le **contrôle dégradé** dit que ce n'est pas encore un lecteur de **scans** : 26,7 % de parité
  sur une photo simulée. C'est la ligne suivante.
- Le bloc OCR est un **bloc classique** : il rend des blocs au bus, comme le parseur de tableaux
  ou de code. Il n'a pas besoin d'être appris, et il dit sa confiance.

## Verdict

**R4.4 — le blocage est levé, la porte du pilote est tenue, R4.4 reste ouverte.**
Le critère « aucun OCR installé » n'existe plus ; les trois conditions du pilote sont mesurées
(WER, parité, scores tracés) ; les contrôles négatifs échouent comme prévu. La **porte de la
roadmap** (dix pages **scannées**) n'est pas atteinte : la page dégradée le dit (26,7 %).

## Ce qui pourrait le rendre faux

- **Les questions sont gabarits** : le banc prend le premier nombre d'un passage ; trois des
  cinq écarts sont des **appels de note**, pas du sens. Un banc de paraphrases changerait la
  parité, dans un sens ou dans l'autre.
- **Le rendu est parfait** : partir du PDF vectoriel favorise l'OCR. Un scan réel ajoute du
  grain, du papier, de la perspective — le contrôle dégradé est une **simulation**.
- **Le choix des pages** : les 9 pages qui portent des questions sont choisies par le banc, pas
  au hasard ; une page dense en tableaux n'est pas dans l'échantillon.
- **Le lecteur est extractif** (BM25) : la parité mesure la sélection, pas la compréhension d'un
  modèle. Le modèle externe de R0.3 n'est pas dans cette boucle.
- **Les seuils ont été fixés après la première mesure** (WER 10 %, parité de passage 90 %) :
  c'est un **plancher de non-régression**, pas une prédiction. Le rejeu est identique, mais un
  seuil choisi après coup est une borne, pas une preuve.

## Fichiers

- Installation : [`tools/installer_ocr.sh`](../tools/installer_ocr.sh) — sans root, `work/ocr/`.
- Lecture : [`tools/graphe_document_ocr.py`](../tools/graphe_document_ocr.py) — TSV → blocs →
  manifeste ; la confiance est dans `prov`.
- Mesure : [`tools/mesurer_ocr.py`](../tools/mesurer_ocr.py) — WER, parité, contrôles.
- Porte : [`tools/porte-ocr.sh`](../tools/porte-ocr.sh) — code 0 seulement si les neuf critères
  tiennent (dont les deux contrôles).
- JSON : [`r44-ocr-pilote.json`](r44-ocr-pilote.json).
- Spécification du bloc : [`docs/implantation/encodeur-visuel.md`](../docs/implantation/encodeur-visuel.md).
- Ligne de roadmap : **R4.4** (programme R).
