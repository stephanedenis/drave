# R4.4 — les scans : la photo passe de 55,9 % à 7,0 % de WER, les colonnes de 89 % à 0,5 %

> **Objet.** La ligne R4.4 était **partielle** : dix pages **rendues** lues, mais aucun scan.
> Ce programme fabrique cinq familles de dégradations, mesure ce qu'elles coûtent, ajoute le
> prétraitement, la récupération des exposants, l'ordre de lecture des colonnes et les cellules
> des tableaux — et valide la chaîne sur un **vrai scan** d'Internet Archive.
>
> **Ce que ce n'est pas.** Les scans sont **simulés** (il n'y a pas de scanner sur la machine) ;
> la validation réelle compare à la **couche OCR** d'Internet Archive, pas à une vérité humaine.
> Les deux limites sont dites, pas contournées.

## Dispositif

- **100 scans simulés** : 10 pages de développement (9 portent les 30 questions du banc R0.3) et
  10 pages de test, × **5 familles** : `propre` (contrôle), `photocopie` (200 dpi, flou, 1,2°,
  mouchetures, JPEG q45), `photo` (180 dpi, perspective, éclairage inégal + ombre, flou de
  mouvement, bruit, JPEG q25), `fax` (120 dpi, binarisation dure, sel-et-poivre), `papier`
  (170 dpi, texture, jaunissement, vignettage, taches, rotation).
- **OCR** : tesseract 5.5.3 sans root ([`installer_ocr.sh`](../tools/installer_ocr.sh)) ; blocs
  dans le graphe R0.1, confiance dans la provenance.
- **Prétraitement** : [`nettoyer_scan.py`](../tools/nettoyer_scan.py) — recadrage, correction
  d'éclairage, redressement (seulement si franc et défini), échelle, lissage des images binaires.
- **Exposants** : passe ciblée chiffres sur les petits mots du TSV
  ([`graphe_document_ocr.py`](../tools/graphe_document_ocr.py)).
- **Colonnes** : gouttière verticale, lecture colonne gauche entière puis droite.
- **Tableaux** : traits → grille régulière → rangement des mots en cellules
  ([`extraire_tableaux.py`](../tools/extraire_tableaux.py)).
- **Mesure** : [`mesurer_scans.py`](../tools/mesurer_scans.py), `mesurer_colonnes.py`,
  `mesurer_tables.py`, `mesurer_reel.py` ; JSON dans `reports/r44-*.json`.

> **Seuils pré-enregistrés ? Non — et c'est écrit.** Les planchers par famille ont été fixés
> **après** la première mesure. Ce sont des **bornes de non-régression**, pas des prédictions :
> un plancher choisi après coup protège des régressions, il ne prouve pas une généralité.

## 1. Les cinq familles, avant et après prétraitement

WER mot à mot contre le texte natif de la même page ; **préservation** = la part des réponses que
le lecteur R0.2 trouvait sur le texte natif et qu'il retrouve sur le scan (dev, 30 questions).

| famille | WER brut | WER **auto** | test brut | test **auto** | préservation brute | préservation **auto + exp** |
|---|---:|---:|---:|---:|---:|---:|
| propre (contrôle) | 4,46 % | 4,14 % | 2,84 % | **3,01 %** | 83,3 % | **90,0 %** |
| photocopie | 6,55 % | 6,34 % | 4,69 % | **4,69 %** | 83,3 % | **86,7 %** |
| photo | **55,85 %** | **7,00 %** | **80,65 %** | **5,27 %** | 13,3 % | **86,7 %** |
| papier | 13,02 % | 7,32 % | **53,15 %** | **6,22 %** | 73,3 % | **73,3 %** |
| fax | 27,05 % | 21,90 % | 23,10 % | **15,52 %** | 50,0 % | **53,3 %** |
| **contrôle page noire** | — | **0 mot lu** | — | — | — | — |

**Ce que le prétraitement fait, et pourquoi.** La **correction d'éclairage** est le levier
principal : la photo passe de **55,9 %** à **7,0 %** de WER, et la page papier d'une résolution
de test de **53,2 %** à **6,2 %**. Deux contre-intuitions ont été mesurées et écrites :

1. **agrandir une photocopie dégrade** : passer de 200 dpi à 2 500 px a **doublé** son WER
   (6,6 % → 12,9 %) — tesseract lit mieux 200 dpi qu'un upscaling ;
2. **l'angle se mesure après le recadrage** : mesuré sur la page entière, il coûte 29 points
   (13 % → 42 % sur le papier) ; et redresser une page de 170 dpi de 0,75° la détruit
   (62,8 % → 84,8 %) — le redressement n'est appliqué que si l'inclinaison est franche (≥ 1,5°)
   et l'image assez définie (≥ 2 000 px).

**Le transfert dev → test** est la preuve que le réglage n'est pas un ajustement au corpus :
photo **80,7 → 5,3 %**, papier **53,2 → 6,2 %**, fax **23,1 → 15,5 %** sur des pages **jamais
vues**.

## 2. Les exposants : le plafond du texte propre monte de 83,3 % à 90,0 %

Les appels de note sont lus `!`, `!!`, `!?` : ce sont des **petits mots** (hauteur < 80 % de la
ligne) faits de ponctuation. La passe ciblée recadre la boîte, l'agrandit ×4 et refait l'OCR avec
une liste blanche de chiffres ; elle ne remplace que si le résultat est un nombre court et
crédible (confiance ≥ 30).

| | sans passe | avec passe |
|---|---:|---:|
| pages propres, exactitude OCR | 83,3 % | **90,0 %** |
| photocopie, préservation | 83,3 % | **86,7 %** |
| photo, préservation | 83,3 % | **86,7 %** |
| fax, préservation | 50,0 % | **53,3 %** |

Le plafond du texte **propre** est 90 % : les trois échecs restants sont un exposant **fusionné**
dans son mot (« développement 10, » — la boîte a une confiance nulle, non récupérée) et deux
**en-têtes** dont la découpe de phrase diffère. Ils sont nommés, pas cachés.

## 3. Les colonnes : 89 % de WER sans gouttière, 0,5 % avec

Corpus : 10 pages à **deux colonnes** dont la vérité terrain est la lecture colonne gauche puis
droite, et 10 pages **mono-colonne** de contrôle.

| version | famille | lecture brute | lecture **colonnes** |
|---|---|---:|---:|
| deux colonnes | propre | **89,44 %** | **0,54 %** |
| deux colonnes | photocopie | **90,11 %** | **1,03 %** |
| deux colonnes | photo | **88,32 %** | **6,52 %** |
| mono (contrôle) | propre | 0,29 % | 0,29 % |
| mono (contrôle) | photocopie | 0,93 % | 0,93 % |
| mono (contrôle) | photo | 6,14 % | 6,14 % |

La gouttière (une bande verticale sans encre entre 15 % et 85 % de la largeur) ne change **rien**
sur une page mono-colonne — c'est le contrôle qui compte : un détecteur qui « trouve » une
gouttière partout serait un détecteur qui casse les pages simples.

## 4. Les tableaux : 92,6 % des cellules exactes sur un rendu, 69,1 % sur une photocopie

Corpus : 10 tableaux 6×9 à vérité connue, une grille à traits. La chaîne : traits → grille
régulière → mots rangés en cellules. Deux contrôles : sans redressement, et le **texte à plat**.

| famille | cellules exactes | grilles de bonne forme |
|---|---:|---:|
| propre | **92,6 %** (500/540) | 10/10 |
| photocopie | **69,1 %** (373/540) | 10/10 |
| photo | **53,7 %** (261/486) | 6/10 |
| photocopie **sans redressement** | **0 %** | 0/10 |
| **texte à plat** (contrôle) | **0 cellule localisée** | — |

Le contrôle du texte à plat est le plus important : les mots du tableau sont **présents** dans la
lecture linéaire (53,7 % des valeurs), mais **aucune** n'est localisée — une cellule n'existe que
si la grille existe. Et sans redressement, la photocopie tombe à **0 %** : un tableau supporte
mal 1,2° d'inclinaison.

La détection de grille par **continuité** (plus longue suite de pixels d'un trait) puis par
**suite arithmétique** (les traits sont régulièrement espacés, le texte non) est ce qui permet de
la trouver sur un scan bruité ; un simple comptage de pixels sombres prenait les lignes de texte
denses pour des traits et décalait toutes les lignes (mesuré : 56 mots lus au lieu de 86).

## 5. Les vrais scans : 7,10 % sur un texte, 88,5 % de mots retrouvés sur un second

Deux PDF **réellement scannés** d'Internet Archive, leur **couche texte** comme référence, page par
page, même page. La référence est un **autre moteur**, pas une vérité humaine : les chiffres sont
des **accords entre moteurs**, pas des exactitudes.

| livre | pages | WER | rappel multiensemble | confiance |
|---|---:|---:|---:|---:|
| *Voyage au centre de la terre* (`voyageaucentrede00vernuoft`) | 10 | **7,10 %** | **93,72 %** | 91,1 |
| *Vingt mille lieues sous les mers*, 1902 (`vingtmillelieu00vern`) | 10 | **23,27 %** | **88,53 %** | 89,2 |

Le second livre est le cas intéressant : son WER est **23,3 %** mais son **rappel multiensemble**
est **88,5 %** — les mots sont lus, c'est l'**ordre** qui diffère. La raison est nommée : plusieurs
pages sont des **lexiques à deux colonnes** ; la couche OCR de référence lit les lignes
**entrelacées** (ordre visuel), notre lecteur lit la **colonne gauche puis la droite**. Le WER
compte ce désaccord d'ordre, le rappel ne le compte pas. C'est la capacité « colonnes » qui
fonctionne — contre une référence qui, elle, ne la fait pas. Les deux chiffres sont publiés
ensemble, et la page la plus faible (rappel 71,2 %, une planche illustrée) est dans le JSON.

**Ce que ces chiffres valent.** La chaîne tourne sur du papier réel ; le prétraitement y est neutre
(7,05 % brut contre 7,10 % nettoyé) parce qu'un scan de bibliothèque est propre — c'est la photo de
téléphone qui pose problème, et c'est là que la correction d'éclairage paie. Un seul des deux
livres est de la prose pure : le second prouve la lecture par colonnes, pas la reconnaissance sur
des pages illustrées.

## 6. Le second moteur : un contrôle, pas un candidat

RapidOCR (ONNX, CPU, modèles par défaut chinois+anglais) sur 4 images, même page, même vérité :

| image | tesseract | RapidOCR |
|---|---:|---:|
| propre | **2,15 %** | 14,87 % |
| photocopie | **6,55 %** | 23,84 % |
| photo (brut) | 55,85 % | 26,34 % |
| photo (auto) | **7,29 %** | — |
| fax | **27,05 %** | 66,67 % |

Le moteur par défaut perd 3 à 10× sur le français (accents, césures) ; il n'a pas été réglé avec
un modèle latin. Ce n'est pas un verdict sur RapidOCR, c'est un **contrôle** : le gain du
prétraitement n'est pas un artefact d'un seul moteur, et changer de moteur ne dispense pas de
mesurer la langue.

## 7. Les contrôles négatifs, tous ensemble

| contrôle | ce qu'il devait faire | ce qu'il fait |
|---|---|---|
| page **noire** | aucun mot | **0 mot, 0 région** |
| page **mono-colonne** | la gouttière ne doit rien changer | écart **0,00 pt** sur 3 familles |
| **sans redressement** (tableaux) | échouer | **0 %** de cellules |
| **texte à plat** (tableaux) | ne rien localiser | **0/54** cellules localisées, 53,7 % des valeurs présentes |
| **sans OCR** (pilote) | aucune réponse | 0/30 |
| **rejeu** | les mêmes chiffres | agrégat et questions identiques |

## 8. La porte

[`porte-ocr-scans.sh`](../tools/porte-ocr-scans.sh) (la 80e porte) vérifie les trois bancs :
familles de scans (WER et préservation par famille, page noire), colonnes (deux colonnes, contrôle
mono, contrôle sans gouttière), tableaux (cellules, grilles, sans redressement, texte à plat).
Les seuils sont des **planchers mesurés** écrits dans les outils :

| famille | WER ≤ | préservation ≥ |
|---|---:|---:|
| propre | 6 % | 85 % |
| photocopie | 8 % | 80 % |
| photo | 10 % | 80 % |
| papier | 10 % | 70 % |
| fax | 25 % | 45 % |

## Ce qui n'est pas tenu

1. **Les scans sont simulés.** La validation réelle existe (7,10 % d'accord), mais elle compare à
   une couche OCR, pas à une vérité humaine, et un seul livre.
2. **Le fax reste à 21,9 %** (dev) et **53,3 %** de préservation : à 120 dpi 1 bit, l'information
   est en partie détruite — les meilleurs réglages (psm 3, upscale 2 100 + lissage) ne la
   recréent pas. Les filtres médian/ouverture, essayés, **détruisent** le texte (95 %).
3. **Le papier perd 4 réponses** (73,3 %) et **la photo 4** (86,7 %) sur les 30 questions : le
   plafond propre est 90 %, et le scan n'y arrive pas encore tout à fait.
4. **Les tableaux photo** perdent la grille 4 fois sur 10 (ombre et perspectives) ; les cellules
   exactes tombent à 53,7 %.
5. **L'exposant fusionné** (« développement 10, ») n'est pas récupéré : sa boîte a une confiance
   nulle et la passe chiffres n'y trouve rien de crédible.

## Verdict

**R4.4 — les scans sont mesurés, la mise en page est mesurée, un vrai scan est validé ; la ligne
reste ouverte pour les scans réels de bout en bout.** Le bloc OCR devient un **bloc classique
robuste** du lecteur : cinq familles de dégradation, un split dev/test qui transfère, des colonnes
à 0,5 % de WER, des cellules à 92,6 %, et une porte qui refuse les régressions.

## Ce qui pourrait le rendre faux

- **Le corpus est le mien** : cinq familles choisies et réglées par moi ; une vraie photocopie de
  ces pages aurait d'autres défauts (agrafe, recto-verso, couleur).
- **Les seuils sont postérieurs** à la mesure : bornes de non-régression, pas prédictions.
- **La référence réelle est un OCR** : 7,10 % et 88,5 % sont des accords, pas des vérités ; deux
  livres, deux éditions, dont un avec des lexiques à deux colonnes.
- **Les questions sont gabarits** (le premier nombre du passage) : les appels de note y jouent un
  rôle démesuré ; un banc de paraphrases dirait autre chose.
- **Les tableaux synthétiques** ont des traits nets : un tableau sans traits (aligné par espaces)
  n'est pas traité — l'outil le dit et refuse, il n'invente pas de colonnes.
- **Un seul moteur réglé** : tesseract+fra ; RapidOCR n'a pas eu son modèle latin.

## Fichiers

- Corpus : [`simuler_scan.py`](../tools/simuler_scan.py), [`fabriquer_colonnes.py`](../tools/fabriquer_colonnes.py),
  [`fabriquer_tables.py`](../tools/fabriquer_tables.py).
- Lecture : [`nettoyer_scan.py`](../tools/nettoyer_scan.py), [`graphe_document_ocr.py`](../tools/graphe_document_ocr.py),
  [`extraire_tableaux.py`](../tools/extraire_tableaux.py).
- Mesures : [`mesurer_scans.py`](../tools/mesurer_scans.py), [`mesurer_colonnes.py`](../tools/mesurer_colonnes.py),
  [`mesurer_tables.py`](../tools/mesurer_tables.py), [`mesurer_reel.py`](../tools/mesurer_reel.py).
- Porte : [`porte-ocr-scans.sh`](../tools/porte-ocr-scans.sh).
- JSON : [`r44-scans.json`](r44-scans.json) · [`r44-colonnes.json`](r44-colonnes.json) ·
  [`r44-tableaux.json`](r44-tableaux.json) · [`r44-reel.json`](r44-reel.json) ·
  [`r44-reel-second.json`](r44-reel-second.json).
- Spécification : [`docs/implantation/encodeur-visuel.md`](../docs/implantation/encodeur-visuel.md).
- Ligne de roadmap : **R4.4** (programme R).
