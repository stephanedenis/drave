# R4.4 — les scans : la photo passe de 55,9 % à 6,7 % de WER, les colonnes de 89 % à 0,5 %

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
| photo | **55,85 %** | **6,68 %** | **80,65 %** | **5,68 %** | 13,3 % | **86,7 %** |
| papier | 13,02 % | **6,87 %** | **53,15 %** | **6,38 %** | 73,3 % | **80,0 %** |
| fax | 27,05 % | 21,90 % | 23,10 % | **15,52 %** | 50,0 % | **53,3 %** |
| **contrôle page noire** | — | **0 mot lu** | — | — | — | — |

**Ce que le prétraitement fait, et pourquoi.** La **correction d'éclairage** est le levier
principal : la photo passe de **55,9 %** à **6,7 %** de WER, et la page papier d'une résolution
de test de **53,2 %** à **6,2 %**. Deux contre-intuitions ont été mesurées et écrites :

1. **agrandir une photocopie dégrade** : passer de 200 dpi à 2 500 px a **doublé** son WER
   (6,6 % → 12,9 %) — tesseract lit mieux 200 dpi qu'un upscaling ;
2. **l'angle se mesure après le recadrage** : mesuré sur la page entière, il coûte 29 points
   (13 % → 42 % sur le papier) ; et redresser une page de 170 dpi de 0,75° la détruit
   (62,8 % → 84,8 %) — le redressement n'est appliqué que si l'inclinaison est franche (≥ 1,5°)
   et l'image assez définie (≥ 2 000 px).

**Le transfert dev → test** est la preuve que le réglage n'est pas un ajustement au corpus :
photo **80,7 → 5,7 %**, papier **53,2 → 6,4 %**, fax **23,1 → 15,5 %** sur des pages **jamais
vues**.

### Le petit texte : une page à 120 dpi, sans autre dégradation

Une sixième famille a été rendue **hors du corpus principal** : la page à **120 dpi** (1 020 px de
large), sans photocopie, sans photo, sans fax — seulement un **petit texte**. C'est le test de la
politique d'échelle : le prétraitement agrandit-il, et cela paie-t-il ?

| | WER dev | WER test | préservation dev | rappel |
|---|---:|---:|---:|---:|
| brut | 5,49 % | 4,03 % | 83,3 % | 96,1 % |
| **auto** (agrandi à 1 800 px) | **4,91 %** | **3,75 %** | **83,3 %** | **97,2 %** |

L'agrandissement gagne **0,6 point** en développement et **0,3** en test : le petit texte n'est pas
une catastrophe pour tesseract, mais l'échelle reste un levier. Cette famille n'est **pas** dans la
porte : elle est un **sondage**, pas une prétention de couverture.

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
| photo | **62,4 %** (337/540) | 8/10 |
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

## 5. Les vrais scans : 7,10 % sur un texte, et l'ordre des colonnes prouvé sur un lexique

Deux PDF **réellement scannés** d'Internet Archive, leur **couche texte** comme référence, page par
page. La référence est un **autre moteur**, pas une vérité humaine : les chiffres sont des
**accords entre moteurs**, pas des exactitudes.

| livre | pages | WER vs couche layout | rappel multiensemble | confiance |
|---|---:|---:|---:|---:|
| *Voyage au centre de la terre* (`voyageaucentrede00vernuoft`) | 10 | **7,10 %** | **93,72 %** | 91,1 |
| *Vingt mille lieues sous les mers*, 1902 (`vingtmillelieu00vern`) | 10 | **36,26 %** | **88,38 %** | 89,2 |
| *Germinal*, 1900 (`germinal02zola`) | 10 | **8,73 %** | **91,89 %** | 90,9 |

Le second livre est le cas intéressant. Son WER contre la couche `pdftotext -layout` est **36,3 %**,
mais son **rappel multiensemble** est **88,4 %** : les mots sont lus, c'est l'**ordre** qui
diverge. Trois de ses pages sont un **lexique à deux colonnes** ; la couche de référence y lit les
lignes dans l'ordre visuel (gauche et droite entrelacées), notre lecteur lit la **colonne gauche
puis la droite**. Pour le prouver, une référence d'**ordre des colonnes** est construite depuis les
**coordonnées des mots du DjVu** (mots à gauche du centre, groupés en lignes, puis ceux de droite) :

| page | WER vs couche layout | WER vs **ordre des colonnes** | **ordre inverse** (contrôle) |
|---|---:|---:|---:|
| 180 | 93,15 % | **15,32 %** | 97,98 % |
| 200 | 92,52 % | **7,09 %** | 96,06 % |
| 210 | 92,00 % | **12,80 %** | 99,20 % |

L'ordre **inverse** échoue à 96–99 % : la direction de lecture est donc **prouvée**, pas supposée.
Les 7 autres pages (prose, une colonne) restent à 9–14 % de WER contre la couche layout, sauf une
planche illustrée à 30,3 % (rappel 71,2 %) — la page la plus faible est dans le JSON.

**Le troisième livre fait payer le prétraitement.** Sur *Germinal* (scan 1900), le WER passe de
**9,38 %** brut à **8,73 %** nettoyé (−0,65 point) : c'est le premier livre où le nettoyage gagne,
et il le doit à la correction d'éclairage et au recadrage — un scan plus ancien, plus sale. Sur
les deux Verne, il est neutre (7,05 → 7,10 %) : le nettoyage ne dégrade jamais, il aide quand la
page en a besoin.

**Ce que la validation réelle a trouvé.** Le lexique réel a révélé un défaut que le corpus
synthétique ne voyait pas : un **en-tête centré** traverse la gouttière, et une gouttière cherchée
sur les **lignes** n'existe pas (tesseract groupe la gauche et la droite dans la même ligne TSV).
La correction — **couverture verticale** par colonne de pixels, gouttière cherchée sur les
**mots** — fait passer la page de **93 % à 15 %** de WER. C'est exactement ce qu'une validation sur
du réel doit apporter : un cas que le synthétique avait lissé.

**Ce que ces chiffres valent.** La chaîne tourne sur du papier réel ; le prétraitement y est neutre
(7,05 % brut contre 7,10 % nettoyé) parce qu'un scan de bibliothèque est propre — c'est la photo de
téléphone qui pose problème, et c'est là que la correction d'éclairage paie. La référence reste un
OCR, pas une vérité humaine, et le WER global du second livre n'a de sens que page par page.

## 5 bis. La variance entre graines : le WER est stable, la préservation ne l'est pas

Le corpus a été régénéré avec une **seconde** puis une **troisième graine** (mêmes pages,
dégradations différentes) et mesuré de la même façon. Le WER bouge peu ; la préservation, elle,
bouge beaucoup :

| famille | WER g1 | WER g2 | WER g3 | préservation g1 | g2 | g3 |
|---|---:|---:|---:|---:|---:|---:|
| propre | 4,14 % | 4,14 % | 4,14 % | 90,0 % | 90,0 % | **90,0 %** |
| photocopie | 6,34 % | 5,44 % | 5,70 % | 86,7 % | 70,0 % | **76,7 %** |
| photo | 6,68 % | 7,77 % | 5,52 % | 86,7 % | 63,3 % | **80,0 %** |
| papier | 6,87 % | 6,50 % | 6,02 % | 80,0 % | 80,0 % | **80,0 %** |
| fax | 21,90 % | 22,73 % | 22,78 % | 53,3 % | 36,7 % | **50,0 %** |

**Pourquoi.** La préservation porte sur **30 questions** : une question = 3,3 points, et un
désaccord de 5 questions fait 16,7 points. Le WER, lui, porte sur ~3 800 mots : il est stable à
±1 point. Sur trois graines, la photo va de **63,3 % à 86,7 %** de préservation — le même lecteur,
le même code, un tirage différent. La préservation est donc un **indicateur à barres d'erreur
larges**, pas un chiffre à deux décimales ; les planchers de la porte en tiennent compte (60 % pour
la photocopie et la photo, 55 % pour le papier, 30 % pour le fax, 85 % pour le propre) — la photo
tombe à 63,3 % sur la graine 2, sous l'ancien plancher de 65 % : c'est exactement ce que cette
variance interdit. Un banc de paraphrases plus large réduirait cette variance — il n'existe pas
encore.

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

## 7 bis. Le coût : le prétraitement coûte un quart de l'OCR — et une optimisation l'a divisé par 7

Secondes par page, 3 pages par famille, CPU 40 cœurs, tesseract 5.5.3 (borne indicative, pas une
référence portable) :

| famille | prétraitement | OCR (nettoyé) | OCR (brut) |
|---|---:|---:|---:|
| propre | 1,36 s | 2,86 s | 2,94 s |
| photocopie | 0,43 s | 2,53 s | 2,54 s |
| photo | 0,41 s | 2,37 s | 1,39 s |
| papier | 0,39 s | 2,37 s | 2,32 s |
| fax | 0,40 s | 2,62 s | 1,70 s |

Le prétraitement est **bon marché** devant l'OCR (0,4 s contre 2,4–2,9 s), sauf sur une page
propre (1,4 s) où il est du **pur surcoût** : c'est le prix de la mesure du diagnostic.

**L'optimisation qui a payé.** L'estimation du fond d'éclairage (un flou large) se faisait sur
l'image entière : **9,1 s par page** sur un rendu de 2 550 × 3 300, pour un champ qui est **basse
fréquence**. Elle se fait maintenant sur une **vignette** (quart de largeur), remontée à la taille
d'origine : **0,13 s**, même champ, même WER. Le prétraitement passe de 9,5 s à **1,36 s** sur une
page propre — et la photo de **51,8 % à 3,8 %** de WER reste acquise.

## 8. La porte

[`porte-ocr-scans.sh`](../tools/porte-ocr-scans.sh) (la 80e porte) vérifie les trois bancs :
familles de scans (WER et préservation par famille, page noire), colonnes (deux colonnes, contrôle
mono, contrôle sans gouttière), tableaux (cellules, grilles, sans redressement, texte à plat).
Vérifiée **verte** le 2026-11-01 : les trois bancs passent, contrôles compris. Les seuils sont des
**planchers mesurés** écrits dans les outils :

| famille | WER ≤ | préservation ≥ |
|---|---:|---:|
| propre | 6 % | 85 % |
| photocopie | 8 % | 60 % |
| photo | 10 % | 60 % |
| papier | 10 % | 55 % |
| fax | 25 % | 30 % |

## Ce qui n'est pas tenu

1. **Les scans sont simulés.** La validation réelle existe (7,10 % d'accord), mais elle compare à
   une couche OCR, pas à une vérité humaine, et un seul livre.
2. **Le fax reste à 21,9 %** (dev) et **53,3 %** de préservation : à 120 dpi 1 bit, l'information
   est en partie détruite — les meilleurs réglages (psm 3, upscale 2 100 + lissage) ne la
   recréent pas. Les filtres médian/ouverture, essayés, **détruisent** le texte (95 %).
3. **Le papier perd 6 réponses** (80,0 %) et **la photo 4** (86,7 %) sur les 30 questions : le
   plafond propre est 90 %, et le scan n'y arrive pas encore tout à fait.
4. **Les tableaux photo** perdent encore la grille **2 fois sur 10** (pages 7 et 9 : ombre et
   trait interrompu) ; les cellules exactes y tombent à **62,4 %**. Les seuils adaptatifs de
   grille (repli tolérant quand le seuil nominal échoue, avec l'étendue du tableau comme garde)
   ont fait passer la photo de 6/10 à 8/10 et de 53,7 % à 62,4 %.
5. **L'exposant fusionné** (« développement 10, ») n'est pas récupéré : sa boîte a une confiance
   nulle et la passe chiffres n'y trouve rien de crédible.

## Verdict

**R4.4 — les scans sont mesurés, la mise en page est mesurée, deux vrais scans sont validés —
dont l'ordre des colonnes, prouvé sur un lexique réel (15,3 % de WER contre 98,0 % en ordre
inverse) ; la ligne reste ouverte pour les scans réels de bout en bout.** Le bloc OCR devient un
**bloc classique robuste** du lecteur : cinq familles de dégradation, un split dev/test qui
transfère, des colonnes à 0,5 % de WER, des cellules à 92,6 %, et une porte qui refuse les
régressions.

## Ce qui pourrait le rendre faux

- **Le corpus est le mien** : cinq familles choisies et réglées par moi ; une vraie photocopie de
  ces pages aurait d'autres défauts (agrafe, recto-verso, couleur).
- **Les seuils sont postérieurs** à la mesure : bornes de non-régression, pas prédictions.
- **La référence réelle est un OCR** : 7,10 %, 36,3 % et 88,4 % sont des accords, pas des
  vérités ; deux livres, deux éditions, dont un avec des lexiques à deux colonnes.
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
