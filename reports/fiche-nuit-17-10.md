# La nuit du 17 au 18 octobre : la couche commune entrée-sortie

**État au 17/10, 21 h 00.** Le chapitre complet est dans
[`docs/synthese/07-modeles-alternatifs-entree-sortie.md`](../docs/synthese/07-modeles-alternatifs-entree-sortie.md) ;
les notes heure par heure dans [`journal/2026-10-17.md`](../journal/2026-10-17.md) ; l'état courant sur la page
d'accueil.

## La question

Une **couche commune entrée-sortie** qui abstrait la langue : l'état d'un modèle peut-il porter le **sens** sans
porter la **langue**, la langue redevenant un **paramètre** à la sortie ? Trente-huit mesures, cinq modèles-jouets
en octets, un vrai modèle multilingue (Qwen 0,5 B), un corpus français reconstruit, et **trois relations retirées
en route**.

## Ce qui tient (avec les chiffres)

| ce qui tient | le chiffre | les mesures |
|---|---|---|
| **le noyau est neutre** — un classifieur de langue y est au hasard | **50,1 à 53,6 %**, **cinq** réplications, plan **2×2** complet (prose/littérature × 256/512) | 1, 15, 19, 29, 36 |
| **le noyau garde le sens** | contenu **87,7 / 86,5 %**, à **9 points** du meilleur | 4, 30 |
| **la langue vit aux extrémités** | **58-68 %** en surface, 50 % au milieu | 1, 15, 19, 24 |
| **le sens partagé est au milieu** | **+0,083** aux couches 8-16 de Qwen, **+0,030** à la dernière | 18 |
| **la langue est un petit paramètre** | **1,33 %** des poids (**32 768**), **5 ms** de bascule, **530 Ko** | 2, 3, 7 |
| **il améliore d'autant plus que le noyau est faible** | **−53 %** (modèle faible) → **−4,7 %** (bon jouet) → **−7,6 %** (Qwen) | 2, 24, 38 |
| **le même sens dans deux langues se retrouve** | **trois livres sur cinq** au-dessus du hasard ; top-5 **37,5 %** (Proust) | 25, 26, 31 |
| **on peut penser sans langue** | **50,6-56,2 %** sur **huit** itérations | 11 |

## Ce qui a été retiré

| ce qui a été retiré | la mesure qui l'a tué |
|---|---|
| « le relevé est teinté par la langue » | **9** — un relevé partagé suffit (0,7 point) |
| « la langue comme paramètre **commande** la sortie » | **25** — sur Qwen, c'est l'**amorce** qui commande |
| « le sens partagé vit dans le **récit** » | **31** — Don Quijote (récit) fait aussi mal qu'Alice |
| « la **part de dialogue** l'explique » | **32-33** — relation **spurieuse** (la typographie de l'édition) |
| « l'**alignement** explique la variation » | **22** — les quatre livres sont alignés à 0,1-1,7 % |

## Ce qui reste ouvert

1. **pourquoi le signal cross-lingue varie de 17×** entre des paires texte-traduction bien alignées (+0,007 à
   +0,116) — **sept** candidats ont échoué (genre, taille, dialogue, alignement, fidélité, richesse, entropie) ;
2. **peut-on penser deux pas** — trois objectifs différents donnent le même mur ; le pas suivant est dans
   l'**entraînement**, pas dans la perte ;
3. **le signal est-il utilisable à l'échelle** — trois livres sur cinq, top-5 37,5 % au mieux.

## Le corpus français

`data/corpus_fr_litterature.txt` — **21 textes**, **15,7 Mo**, **87 341 formes** : Proust, Stendhal, Hugo, Voltaire,
Baudelaire, Chateaubriand, George Sand, Diderot, Montesquieu, Corneille, Verne, Zola. Tous trouvés dans les projets
`Panini/` et `Panini-Research/` de Stéphane (merci à lui), et **reconstruits avec les en-têtes Gutenberg retirés**.

⚠️ **Trois avertissements sur ces corpus** : `dracula/dracula_fr.txt` contient **« Vocations Explained »** (un autre
livre), `pg2000_en.txt` est un **Don Quijote français**, et **trois des quatre fichiers « allemands »** du corpus
« multilingue vérifié » sont **anglais**. *Un nom de fichier n'est pas une langue, et un dossier « vérifié » n'est
pas vérifié.* L'outil `tools/cribler_corpus.py` refait ce contrôle.

## La santé du dépôt

**Passage complet des 46 portes, terminé à 21 h 00** : **44 vertes, 2 rouges** — et les deux rouges sont
**exactement les mêmes** qu'au passage du matin (`porte-indice` 860 s contre 817, `porte-melange` 102 contre 101).
*Rien n'a cassé.*

## Les outils écrits cette nuit

`langue_dans_etat.py` (classifieur de langue par couche) · `contenu_par_couche.py` (contenu du noyau) ·
`adaptateur_langue.py` (LoRA par langue) · `generer_par_langue.py` (test de la sortie) · `cout_bascule.py`
(coût de la bascule) · `lecture_croisee.py` · `releve_parametre.py` · `comparer_noyaux.py` · `penser_sans_langue.py`
(itération) · `retrieval_parallele.py` (sens partagé) · `cribler_corpus.py` (santé d'un corpus) ·
`verifier_bilan.py` (traçabilité d'un résumé).
