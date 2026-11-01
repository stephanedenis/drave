# L'encodeur visuel — l'OCR comme bloc classique du lecteur

> **Ce que ce document est.** La **spécification** du bloc OCR de R4.4 : ce qu'il reçoit, ce
> qu'il rend, ce qu'il promet sur la provenance et la confiance, et la porte qui le vérifie.
> Le code est [`graphe_document_ocr.py`](../../tools/graphe_document_ocr.py) ; la mesure est
> [`mesurer_ocr.py`](../../tools/mesurer_ocr.py) ; la porte est
> [`porte-ocr.sh`](../../tools/porte-ocr.sh) ; les **chiffres** sont dans
> [`reports/`](../../reports/), jamais ici.
>
> **Chargement** : lire § 2 et § 4 pour coder contre le bloc ; le reste est la justification.

## 1. Le besoin

Une partie des documents n'existe qu'en **image** : photocopies, scans, pages de revue. R0.1
découpe le texte déjà extrait d'un PDF, d'un HTML, d'un DOCX ou d'un Markdown ; il ne sait pas
lire des pixels. Sans OCR, le lecteur s'arrête à la frontière du texte natif — et R4.4 était
**bloquée** par cette absence, pas par une idée à trouver.

Le bloc OCR ne remplace pas le lecteur : il produit des **régions**, et le lecteur les lit comme
les autres. C'est le principe des blocs de R4 : **classique d'abord**. Un OCR n'a pas besoin
d'être appris, il doit être **mesuré** — et dire son score.

## 2. Le contrat

| élément | contenu |
|---|---|
| **entrée** | une **image** (PNG/JPEG) d'une page, et la **langue** (`fra`, `eng`, `spa`, …) |
| **sortie** | des **blocs** typés (`titre`, `section`, `paragraphe`, `note`) avec leur texte, leur `y` et leur **confiance** |
| **coût** | linéaire en pages ; aucun GPU ; l'OCR est un sous-processus, pas un modèle chargé |
| **trace** | chaque bloc porte `prov.confiance` (moyenne des mots du bloc) et `prov.moteur` |
| **refus** | pas d'exécutable, langue absente, image vide → erreur **nommée**, jamais un texte vide silencieux |

Un bloc OCR n'est **pas** un bloc natif : sa provenance ne dit pas `offset` dans un fichier, elle
dit `page` et `y` dans l'image. Le manifeste le porte dans `extraction` :
`{"outil": "graphe_document_ocr.py", "moteur": "tesseract", "version_moteur": "…",
"langue": "fra"}`. C'est ce champ qui distingue une lecture OCR d'une lecture native dans un
rejeu.

## 3. Le chemin

| étape | ce qui se passe | où c'est vérifié |
|---|---|---|
| 1. **rendu** | `pdftoppm -r 300 -png -singlefile` rend **la** page demandée | la clé du cache porte l'empreinte du PDF : un PDF modifié ne relit pas l'ancienne page |
| 2. **OCR** | `tesseract image stdout -l <langue> --psm 3 -c tessedit_create_tsv=1` | le TSV est **explicite** : les configs `tsv`/`hocr` ne sont pas dans le paquet de données |
| 3. **mots → lignes** | les mots du TSV sont groupés par `(bloc, paragraphe, ligne)`, ordonnés par `y`, puis par `x` | l'ordre du TSV n'est pas garanti ; la géométrie, si |
| 4. **lignes → blocs** | hauteur de ligne, écart vertical, retrait — la même heuristique que le parseur PDF | les césures de fin de ligne se recollent comme en natif |
| 5. **blocs → manifeste** | `graphe_document.manifeste_de_blocs` : flux, offsets, partition, hash | `verifie()` refuse une partition trouée ou un span faux |

Le point important est l'étape 5 : **une seule construction du flux** pour le natif et pour
l'OCR. Deux constructions concurrentes feraient diverger les offsets d'un octet, et la
comparaison entre les deux lectures ne mesurerait plus l'OCR mais deux façons de compter.

## 4. La confiance

Tesseract donne une confiance **par mot** (0–100). Le bloc agrège une **moyenne pondérée par les
mots** : un bloc de dix mots pèse dix fois un titre d'un mot. La confiance est dans
`prov.confiance`, donc dans le manifeste, donc dans le rejeu — pas dans un journal à part.

Une lecture OCR qui ne dit pas son score ne peut pas être auditée : quand un bloc répond faux, il
faut pouvoir dire s'il a été **mal lu** (confiance basse) ou **mal choisi** (confiance haute,
sélection fausse). C'est la distinction qui manque le plus souvent aux OCR « boîte noire ».

## 5. La parité, et comment on la mesure

La question de R4.4 n'est pas « l'OCR lit-il ? » mais « la page lue en OCR donne-t-elle la
**même réponse** que la page lue en texte natif ? ». La mesure est donc une **comparaison** :

1. le **WER mot à mot** contre le texte natif de la même page, avec **rappel** et **précision**
   de vocabulaire — une OCR qui invente du texte paie deux fois ;
2. la **parité de passage** : les questions du banc R0.3 dont le gold tombe sur la page, lues
   par le **même** lecteur extractif (R0.2) sur le manifeste natif et sur le manifeste OCR ; le
   passage choisi est le même si le **F1 mots ≥ 0,90** ;
3. la **parité de valeur** (le chiffre exact de la question est dans le passage choisi) : plus
   stricte, elle est **rapportée** et non portée par la porte, parce qu'elle dépend du layout
   (appels de note en exposant, en-têtes).

Le lecteur est **extractif** : cette parité mesure la **sélection**, pas la compréhension d'un
modèle. Un modèle externe sur le texte OCR serait une autre mesure, et elle n'est pas faite ici.

## 6. Les contrôles négatifs

Une mesure d'OCR sans contrôle négatif mesure la bonne volonté de l'OCR :

| contrôle | ce qu'il doit produire |
|---|---|
| **sans OCR** | un manifeste **vide** ; aucune réponse ne sort. Si une réponse sort, elle vient d'ailleurs |
| **page dégradée** | une **photo simulée** (définition réduite, flou, JPEG de mauvaise qualité, rotation légère) : le WER doit **monter** et la parité **baisser**. Une dégradation qui ne change rien ne prouve rien |
| **rejeu** | deux passes donnent le même agrégat et les mêmes questions — les rendus et l'OCR sont en cache, et la clé du cache porte l'empreinte du PDF |

## 7. La porte

`tools/porte-ocr.sh` appelle `tools/installer_ocr.sh --verifie` (environnementale : code 2 si
l'OCR manque, avec la commande qui l'installe) puis `tools/mesurer_ocr.py --porte`. Elle **écrit
zéro** : la mesure de la porte ne modifie pas la fiche JSON commitée. Ses seuils sont dans
`mesurer_ocr.py`, avec la mesure qui les a produits dans `reports/`.

Ce que la porte **ne vérifie pas** : les **scans réels**, les colonnes denses, les tableaux, les
exposants. Ce sont les étapes 2 et 3 de R4.4, et elles restent ouvertes.

## 7 bis. Le prétraitement : des étapes nommées, et deux pièges

`nettoyer_scan.py` applique des étapes **nommées** (`recadrage`, `eclairage`, `redressement`,
`echelle`, `lissage`, `median`, `sauvola`) et un diagnostic choisit (`auto`) : image binaire ?
éclairage inégal ? petite ? inclinée ? La trace des étapes appliquées est rendue avec l'image.

Deux leçons mesurées, contre-intuitives, sont dans le code :

1. **ne pas agrandir une image déjà propre** — passer une photocopie de 200 dpi à 2 500 px a
   doublé son WER ; tesseract lit mieux 200 dpi qu'un upscaling ;
2. **l'angle se mesure après le recadrage, et seulement s'il est franc** — sur la page entière,
   le bord et le vignettage biaisent le profil ; et redresser une page de 170 dpi de 0,75° la
   détruit. Le seuil est 1,5° **et** 2 000 px de large.

La **correction d'éclairage** (division par un fond estimé) est le levier principal : une photo
de téléphone passe de 55,9 % à 7,0 % de WER sur le corpus de R4.4. Une étape qui ne paie pas est
retirée : le prétraitement est mesuré, pas décoratif.

## 7 ter. Les exposants

Un appel de note est un **petit mot** (hauteur < 80 % de la ligne) fait de ponctuation : tesseract
le lit `!`, `!!`, `!?`. La passe ciblée recadre sa boîte, l'agrandit ×4, refait l'OCR avec une
liste blanche de chiffres (`--psm 10`) et ne remplace que si le résultat est un nombre court et
crédible (confiance ≥ 30). Elle est optionnelle (`exposants=True`) et versionnée
(`RECUPERATION_VERSION`) : changer la récupération invalide les caches de mesure.

## 7 quater. Les colonnes

`bande_vide` cherche une **gouttière** — une bande verticale sans encre entre 15 % et 85 % de la
largeur, avec au moins 20 % des lignes de chaque côté — et `ordre_de_lecture` lit alors la
colonne gauche entière, puis la droite. Sans gouttière, l'ordre reste `(y, x)`. Sur une page
mono-colonne, la détection ne change rien (contrôle : écart 0,00 pt) ; sur une page à deux
colonnes, elle fait passer le WER de 89 % à 0,5 %.

## 7 quinquies. Les tableaux

`extraire_tableaux.py` lit la **grille**, pas les mots seuls : les traits horizontaux et verticaux
sont détectés par **continuité** (la plus longue suite de pixels d'un trait — une ligne de texte
ne l'est pas), filtrés par une **suite arithmétique** (les traits sont régulièrement espacés, le
texte non), puis chaque mot est rangé dans la cellule qui contient son centre. Deux préalables
mesurés : redresser le tableau (l'angle est estimé sur le masque binaire, pas sur le gris) et
**effacer les traits avant l'OCR** (sinon tesseract saute une ligne sur deux : 56 mots au lieu de
86). Sans traits, l'outil **refuse** de deviner des colonnes.

## 8. Ce que le bloc ne fait pas

- **Pas de modèle de layout** : hauteur, écart, retrait et **gouttière**. Une page à deux
  colonnes est lue correctement si la gouttière est nette ; une colonne dense, un tableau sans
  traits ou une mise en page irrégulière ne sont pas revendiqués.
- **Pas de scans réels de bout en bout** : la validation externe existe (un PDF d'Internet
  Archive, comparé à sa couche OCR), mais elle n'est pas une vérité humaine et ne remplace pas
  un corpus de photocopies.
- **Pas d'exposants** : un appel de note `10` peut devenir `!`. C'est nommé dans la fiche du
  pilote ; la correction (nettoyage typographique, seconde passe ciblée) n'est pas faite.
- **Pas de tableaux** : un tableau non balisé est du texte, comme en PDF natif (R4.1 le traite).
- **Pas de langue non latine** : `fra`, `eng`, `spa` sont installés pour le corpus ; le choix
  n'est pas mesuré au-delà.

## 9. Installation et reproductibilité

`tools/installer_ocr.sh` télécharge les RPM openSUSE de tesseract 5.5.3 (binaire, bibliothèques,
données `fra`/`eng`/`spa`/`osd`), les extrait dans **`work/ocr/root`** (gitignoré) et **ne touche
à rien d'autre** : ni `sudo`, ni paquet système, ni `~/.local`. `--verifie` dit ce qui est là
sans rien télécharger. Le nom des paquets et les versions sont **dans le script** : une
installation qui ne dit pas sa version n'est pas reproductible.

## 10. Les chemins

| quoi | où |
|---|---|
| installation sans root | [`tools/installer_ocr.sh`](../../tools/installer_ocr.sh) |
| OCR → blocs → manifeste | [`tools/graphe_document_ocr.py`](../../tools/graphe_document_ocr.py) |
| manifeste commun (natif et OCR) | [`tools/graphe_document.py`](../../tools/graphe_document.py) |
| mesure (WER, parité, contrôles) | [`tools/mesurer_ocr.py`](../../tools/mesurer_ocr.py) |
| porte | [`tools/porte-ocr.sh`](../../tools/porte-ocr.sh) |
| résultat du pilote (pages rendues) | [`reports/rapport-r44-ocr-pilote.md`](../../reports/rapport-r44-ocr-pilote.md) |
| résultat des scans (5 familles, colonnes, tableaux, réel) | [`reports/rapport-r44-scans.md`](../../reports/rapport-r44-scans.md) |
| corpus de scans simulés | [`simuler_scan.py`](../../tools/simuler_scan.py) |
| prétraitement | [`nettoyer_scan.py`](../../tools/nettoyer_scan.py) |
| colonnes et tableaux | [`extraire_tableaux.py`](../../tools/extraire_tableaux.py) |
| porte des scans | [`porte-ocr-scans.sh`](../../tools/porte-ocr-scans.sh) |
