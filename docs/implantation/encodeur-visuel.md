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

## 8. Ce que le bloc ne fait pas

- **Pas de modèle de layout** : hauteur, écart et retrait. Un scan de travers ou une page à deux
  colonnes denses ne sont pas revendiqués ; le parseur PDF de R0.1, lui, cherche une bande vide
  verticale pour les colonnes — l'OCR n'a pas encore cet équivalent.
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
| résultat du pilote | [`reports/rapport-r44-ocr-pilote.md`](../../reports/rapport-r44-ocr-pilote.md) |
