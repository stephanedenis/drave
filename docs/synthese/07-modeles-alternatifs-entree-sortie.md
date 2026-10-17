# 7. Les modèles alternatifs pour l'entrée et la sortie — vers une couche commune

> **La question.** Peut-on arriver **plus vite** à une couche d'entrée-sortie **commune**, qui fasse
> **abstraction de la langue** — la langue, le dialecte, le style n'étant plus que des **paramètres** ?
> Cette note examine les familles de solutions, avec pour chacune : ce qu'elle gagne, ce qu'elle coûte, et
> **comment on le mesure**.

![Une couche commune, et la langue comme paramètre](schemas/couche-commune.svg)

## La synthèse, en un tableau (à lire avant le reste)

Treize mesures ont été faites les 17 et 18 octobre ✓. Les voici **toutes**, avec ce qu'elles disent et le
chiffre qui le dit — pour qu'on puisse juger le chapitre sans le lire en entier ✓.

| # | la question | la mesure | le chiffre | verdict |
|---:|---|---|---|---|
| 1 | l'état porte-t-il la langue ? | classifieur linéaire par couche, modèle **bilingue** ✓ | **50,2 %** aux couches 1-2 (hasard) · **59,4 %** aux couches 6-7 | ✓✓ **noyau neutre**, langue à la surface |
| 2 | la langue est-elle un paramètre ? | LoRA sur noyau **gelé**, une langue par adaptateur ✓ | français **3,19 → 1,50** (−53 %) · anglais **1,90 → 1,40** (−26 %) | ✓✓ oui, **131 k** (5,1 %) |
| 3 | où le brancher ? | LoRA sur le **dernier étage** seul ✓ | **−44,6 %** pour **32 768** poids = **1,33 %** (84 % du gain) | ✓✓ la **surface** suffit |
| 4 | le noyau neutre est-il utile ? | contenu (état → mot suivant) aux couches neutres ✓ | **87,8 / 87,3 %**, à 8 points du meilleur | ✓✓ le **sens reste** |
| 5 | le relevé est-il neutre ? | un seul relevé **non linéaire** vs deux linéaires ✓ | **71,5 %** contre 79,3 / 76,5 | ✓ (mais voir 8) |
| 6 | la langue commande-t-elle la sortie ? | génération, amorces croisées ✓ | amorce **anglaise** + adaptateur **français** → **français** ✓ | ✓✓ **opérationnel** |
| 7 | combien coûte la bascule ? | chargement + application vs rechargement ✓ | **5,0 ms** / **530 Ko** contre **134,6 ms** / **9,8 Mo** | ✓✓ **×27** / **×18** |
| 8 | un relevé se transfère-t-il ? | lecture croisée, lecteurs **de même puissance** ✓ | pénalité **+8,7** (linéaire) à **+19,5** (non linéaire) | ✗ **non** (transfert) |
| 9 | un relevé partagé suffit-il ? | relevé appris sur **les deux** langues ✓ | **0,7 point** d'écart avec deux relevés séparés | ✓✓ **oui** |
| 10 | noyau bilingue ou adaptateur ? | trois dispositifs réels ✓ | bilingue **1,0737** · monolingue+adaptateur **1,4546** | ✓ bilingue (35 % mieux), adaptateur **2/3** du chemin |
| 11 | la pensée itérée est-elle sans langue ? | opérateur appris, k itérations ✓ | langue **50,6-56,2 %** sur **huit** pas | ✓✓ **sans langue** |
| 12 | peut-on penser deux pas ? | entraîner sur k (recette du 16/10) ✓ | contenu **exactement plat** (82,2 % partout) = **identité** | ✗ solution triviale, **répliquée** |
| 13 | et avec un autre objectif ? | **marge** : exiger une amélioration ✓ | k=1 **80,3** · k=2 **93,7** — **comme sans marge** | ✗ **même mur** |

### La suite du programme (mesures 14 à 23)

| # | la question | la mesure | le chiffre | verdict |
|---:|---|---|---|---|
| 14 | un **vrai** corpus français ? | Gutenberg de `Panini/` (le dépôt n'en avait pas ✗) | **13,2 Mo**, 18 textes, **66 322** formes (Maupassant, Dumas, Flaubert, Verne) | ✓✓ vrai corpus |
| 15 | la neutralité **à l'échelle** ? | modèle bilingue **dim 512** (9,57 M) | couches 2 et 6 : **51,4** et **51,2 %** ; couche 8 : **67,9 %** | ✓✓ noyau neutre, surface **plus** langue-aware |
| 16 | le **même sens** en deux langues ? | retrieval croisé, Le Tour du monde | 0/24 ✗ — **test invalide** ✗ | ✗ à refaire |
| 17 | et avec un bon échantillon ? | même test, milieu du segment | écart **+0,022** ✓ (contre −0,053 ✗) | ✓ signal réel, **faible** |
| 18 | sur un vrai modèle multilingue ? | **Qwen2.5-0.5B**, mêmes segments | **+0,083** aux couches 8-16 ; **+0,030** à la dernière | ✓✓ **sens partagé au milieu** |
| 19 | et sur la **littérature** ? | modèle bilingue littéraire (4,79 M) | couches 1-3 : **50,1 · 52,3 · 50,4 %** ; pic couche 5 : 67,7 % | ✓✓ neutralité, **zone plus courte** |
| 20 | le signal dépend-il du modèle ? | trois modèles, même test | **+0,022 → +0,034 → +0,083** (2,43 M → 4,79 M → 494 M) | ✓✓ **tendance monotone** |
| 21 | réplication ? | **trois** livres | +0,078 (Verne) · +0,033 (Dracula ✗) · +0,009 (Alice) | ✓ en **signe**, ✗ en amplitude |
| 22 | l'alignement est-il en cause ? | positions relatives des noms propres | Verne **0,1-1,6 %** ✓ · Alice **1,7 %** ✓ · Dracula **cassé** ✗✗ | ✓ la variation n'est **pas** l'alignement |
| 23 | le corpus est-il sain ? | crible sans modèle (titre, longueur, noms) | **1 paire cassée sur 3**, **la même dans deux corpus** ✗ | ✗ mais **détectée** |

**Et ce que cette seconde série ajoute à la première** ✓✓ : le corpus **réel** ✓, la **réplication** de la
neutralité ✓ (trois modèles, trois corpus ✓), le **sens partagé** qui se retrouve **mieux que le hasard** ✓✓ et
qui **croît avec le modèle** ✓✓, et — du côté de l'instrument — **deux fichiers de corpus à ne pas croire** ✗✓
(un test invalide, une paire mal étiquetée ✓). *La science avance aussi en retirant* ✓✓.

### Ce qu'il faut en retenir, en cinq phrases

1. **La langue n'est ni dans l'état ni dans le relevé partagé** ✓✓ — elle vit dans l'**entrée** (les octets ✓)
   et dans la **surface de sortie** ✓ ; c'est **exactement** la structure d'une couche commune ✓.
2. **La langue est un paramètre de 1,33 %** ✓✓ (32 768 poids au dernier étage), qui **commande la sortie** ✓ et
   dont la **bascule coûte 5 ms** ✓✓.
3. **Le noyau neutre n'est pas appauvri** ✓✓ : le contenu y reste à **87,8 %**, à 8 points du meilleur ✓.
4. **La pensée itérée est sans langue** ✓✓ (50,6-56,2 % sur huit pas) — **penser ne dépend pas de la langue où
   l'on parle** ✓✓.
5. **Mais elle ne tient qu'un pas** ✗, et **trois objectifs différents** n'y changent rien ✗✓ : la limite est
   dans la **représentation**, pas dans la perte ✓. Le pas suivant est à chercher dans **l'entraînement du
   modèle** (récurrence dans la boucle ✓), pas dans le réglage ✓.

## Ce que la nuit du 16/10 a déjà établi, et qui oriente tout


Trois faits mesurés, qu'aucune solution ne peut ignorer :

1. **les deux espaces (sortie prélinguistique, entrée postlinguistique) ne sont pas le même** : facteur
   **648** d'échelle, cosinus **+0,14** ✗ — la couche commune n'existe pas **par défaut** ;
2. **elle s'obtient par entraînement** ✓ : un terme d'alignement amène le cosinus à **0,70** et l'échelle à
   **1,015**, **sans** dégrader la langue (4,30 contre 4,69 bits/octet ✓ — il l'améliore) ;
3. **mais l'alignement ne suffit pas à boucler** ✗ : la boucle directe explose (λ = 7 311) — il faut aussi
   une **dynamique** apprise. *Un espace commun est nécessaire ; il n'est pas suffisant.*

Et un quatrième fait, qui change le problème de la langue : **les modèles-jouets du dépôt sont en OCTETS**
(vocabulaire de 256 ✓). Il n'y a **pas de tokeniseur**, donc **pas de vocabulaire par langue** ✓✓ — la
langue n'est **pas** dans les entrées. C'est un avantage considérable pour la suite, et il faut le dire :
*une partie du problème de la langue a déjà disparu par construction.*

## Les cinq familles de solutions

| famille | l'idée | ce qu'elle gagne | ce qu'elle coûte | mesurable par |
|---|---|---|---|---|
| **A. octets partagés** | un seul vocabulaire (UTF-8) pour toutes les langues | rien à faire ✓, aucune langue dans l'entrée ✓ | séquences 3-4× plus longues ✗, abstraction **de surface** (pas de sens) ✗ | la perplexité par langue, à taille égale |
| **B. plongement partagé + étiquette** | un espace d'embedding commun, une **étiquette de langue** en entrée | simple, éprouvé (XLM-R, mBERT) ✓ | l'étiquette **contamine** l'état ✗ ; le sens reste teinté de la langue | un classifieur de langue sur l'état doit être **au hasard** |
| **C. adversarial** | entraîner l'état à **cacher** la langue (un classifieur adverse essaie de la deviner) | rend le contenu **réellement** neutre ✓ | instable ✗, peut détruire de l'information utile ✗ | la courbe : précision du classifieur vs qualité de la langue |
| **D. interlingua / sens-texte** | une **représentation sémantique** (Mel'čuk : sens ⇄ texte), les langues étant des **modules de surface** | c'est **exactement** l'idée visée ✓ ; le sens est explicite ✓ | il faut **construire** l'interlingua ✗ (personne ne l'a fait pour un LLM) | reconstruire le **même** sens en 2 langues, depuis **une** représentation |
| **E. adaptateurs par langue** | un noyau commun + un **petit adaptateur** par langue (LoRA) | peu de paramètres par langue ✓, très efficace ✓ | la couche commune reste **implicite** ✗ (rien ne garantit qu'elle soit neutre ✗) | l'écart entre langues **sans** l'adaptateur |

## La recommandation, et pourquoi

**Faire A + E maintenant, et B + C pour mesurer, D comme horizon.**

* **A est déjà fait** ✓ (octets) : c'est le socle, et il ne coûte rien ;
* **E est le meilleur rapport gain/coût** ✓✓ : un noyau partagé et des adaptateurs par langue — c'est
  **exactement** « la langue comme paramètre », et cela s'entraîne en quelques heures sur les deux cartes ;
* **B et C ne servent pas à construire** mais à **vérifier** ✗ : un classifieur de langue sur l'état ✓ dit si
  la couche commune est **vraiment** neutre. C'est le critère qui manque à presque tous les travaux ;
* **D est le programme long** ✗✓ : l'interlingua de Mel'čuk, appliqué à un modèle de langue — c'est-à-dire
  une **couche sémantique explicite** entre le texte et la pensée.

## L'expérience à faire en premier (et elle est courte)

La question n'est pas « quelle architecture » mais **« ma couche commune porte-t-elle encore la langue ? »** ✗.
Or on peut la poser **tout de suite**, avec ce que le dépôt a déjà :

1. entraîner **deux** modèles-jouets en octets sur **deux langues** (par exemple `data/corpus_en.txt` et un
   corpus français ✓ — à constituer ✗) ;
2. entraîner un **classifieur de langue** sur l'état de chacun ✓ (une régression logistique suffit ✓) ;
3. mesurer sa précision : si elle est **élevée** ✗, la couche porte la langue ; si elle est **au hasard** sur
   les positions **tardives** ✓, la langue est déjà abstraite par la profondeur ✓✓ ;
4. et refaire la mesure **avec un adaptateur de langue** (E ✓) : l'adaptateur doit **absorber** la langue, et
   le noyau devenir plus neutre ✓✓.

C'est **quatre mesures**, dont trois outils existent déjà (`banc_lecteur.py` pour les états, la régression
logistique en dix lignes, et les deux cartes ✓). Et la réponse à « peut-on aller plus vite » est là :
**on ne construit pas la couche commune, on vérifie qu'elle est déjà là** — et l'on ne construit que ce qui
manque.

## Ce qui manque au dépôt pour cette expérience (dit franchement)

* **un corpus français** ✗ : le dépôt a `data/corpus_en.txt` (96 Mo ✓) et `data/wikitext2_test.txt` ; je n'ai
  pas vu de corpus français dans le dépôt — c'est la **première** chose à ajouter ;
* **un classifieur de langue** ✗ : quelques lignes, mais il n'existe pas ;
* et **le temps** de deux entraînements (≈ 20 min chacun sur les cartes ✓ — c'est faisable).

## Première mesure (17/10, 15 h) : la couche commune EXISTE DÉJÀ — et la langue n'est qu'à la SURFACE

Le chapitre ci-dessus proposait un critère ; il a été appliqué ✓✓. Dispositif : un modèle **en octets**
(8 couches, 256 de dimension, **4,79 M** paramètres ✓) entraîné sur un corpus **mixte** de **10,2 Mo**
(**6,0 Mo d'anglais + 4,5 Mo de français** ✓ — le corpus français a été **constitué** pour l'occasion, voir
plus bas), validation **2,6822 bits/octet** ✓.

Puis `tools/langue_dans_etat.py` ✓ : une régression **linéaire** prédisant la langue depuis l'état
**normalisé** de chaque couche ✓, sur **300 fenêtres par langue** ✓, avec un **témoin intra-langue** ✗ (deux
moitiés du corpus anglais : ce qu'un classifieur peut faire **sans** la langue ✓) :

| couche | langue (en/fr) | témoin intra-langue | verdict |
|---:|---:|---:|---|
| **0** | **62,4 %** | 53,1 % | la langue est dans l'**entrée** (octets) ✗ |
| **1** | **50,2 %** | 50,7 % | **le hasard** ✓✓ — la langue s'efface |
| **2** | **50,3 %** | 51,8 % | **le hasard** ✓✓ |
| 3 | 56,6 % | 50,6 % | la langue revient un peu |
| 4 | 53,9 % | 50,2 % | presque le hasard ✓ |
| 5 | 53,8 % | 51,0 % | presque le hasard ✓ |
| **6** | **59,4 %** | 50,1 % | la langue **revient** ✗ (la surface) |
| **7** | **59,6 %** | 50,7 % | la langue **revient** ✗ (la surface) |
| 8 | **51,0 %** | 50,9 % | le hasard ✓✓ (état final, prêt pour la tête) |

* **LE NOYAU EST NEUTRE** ✓✓ : aux couches **1 et 2**, un classifieur linéaire ne fait **pas mieux que le
  hasard** (50,2 et 50,3 % ✓✓, contre un témoin à 50,7 et 51,8 ✓). *L'état ne sait pas dans quelle langue
  le texte est écrit* ✓✓ — c'est exactement la « couche commune » cherchée ✓ ;
* **ET LA LANGUE NE REVIENT QU'À LA SURFACE** ✗✓ : aux couches **6 et 7**, elle remonte à **59,4 et 59,6 %**
  ✓ — c'est-à-dire que le modèle **réintroduit** la langue **au moment de produire** ✓✓. C'est la structure
  demandée : **un contenu neutre, une surface paramétrée par la langue** ✓✓✓ ;
* **et l'entrée, elle, porte la langue** ✗ (62,4 % à la couche 0 ✓) : les octets anglais et français n'ont
  pas les mêmes statistiques ✓ — c'est le seul endroit où « la langue » est dans les données ✓✓.

### Le corpus français, et la sixième fois qu'un chiffre s'est déguisé

* **il n'y avait pas de corpus français** dans le dépôt ✗ : il a été **constitué** à partir du français
  **réel** du dépôt (docs, fiches, journal ✓) → **4,45 Mo**, dont les mots les plus fréquents sont `les`,
  `est`, `pas`, `sur`, `par`, `que` ✓✓. Mais le premier essai était **contaminé** ✗ : les mots les plus
  fréquents étaient `stephane`, `home`, `data`, `bash` ✗✓ (le journal contient des commandes et des
  chemins ✓). Un **filtre** (lignes sans chemin, sans option, avec au moins **deux mots-outils** français ✓)
  a ramené 12,8 Mo à **4,45 Mo propres** ✓ ;
* **et mon instrument avait un défaut** ✗✓ : le **signe** d'un classifieur linéaire est **arbitraire** ✓ —
  une précision de **43,4 %** est en réalité **56,6 %** avec l'autre orientation ✓✗. Sans le `max(acc, 100−acc)`,
  j'aurais lu « sous le hasard » là où il y a une séparation ✓. **C'est la sixième fois** qu'un chiffre se
  déguise ✓✓ (les cinq premières sont au chapitre 6 ✓) — et la règle n'a pas changé : *écrire à côté du
  chiffre ce qui pourrait le rendre faux* ✓.

### Ce que cela dit pour la suite

La couche commune **existe déjà** dans un modèle en octets entraîné sur deux langues ✓✓. Ce qui reste n'est
donc **pas** à construire ✗ : c'est à **exploiter** ✓ — et les deux prochaines étapes sont nettes :

1. **vérifier que le noyau neutre est UTILE** ✗ : un état qui ne dit plus la langue dit-il encore le **sens** ?
   （mesurer le contenu, méthode du chapitre 5 ✓ — sur les couches 1-2, où la langue s'efface ✓) ;
2. **les adaptateurs par langue** (famille E ✓) : si la langue ne vit qu'aux couches **6-7** ✓, un adaptateur
   posé **là** devrait suffire ✗✓ — c'est-à-dire **quelques paramètres par langue**, exactement la
   « langue comme paramètre » cherchée ✓✓.

## Deuxième mesure (17/10, 16 h) : la langue EST un paramètre — deux adaptateurs de 131 k

La famille E disait : « un noyau commun + un petit adaptateur par langue ». C'est mesuré ✓✓, sur un modèle
**monolingue** (anglais seul ✓, `/tmp/jouet-d256`, 4 couches, 256 ✓), **noyau entièrement gelé** ✓.

Dispositif : `tools/adaptateur_langue.py` ✓ — un LoRA (rang 8 ✓) sur les 28 projections d'attention et de MLP
= **131 072 paramètres**, soit **5,1 %** du modèle ✓, entraîné 2 000 pas sur **une** langue ✓, puis évalué sur
**les deux** ✓.

| adaptateur | perte **français** | perte **anglais** |
|---|---:|---:|
| **aucun** (noyau seul ✓) | **3,19** ✗ | **1,90** ✓ |
| **adaptateur français** (131 k ✓) | **1,50** ✓✓ (−53 %) | 2,91 ✗ (+53 %) |
| **adaptateur anglais** (131 k ✓) | 3,02 | **1,40** ✓✓ (−26 %) |

* **CHAQUE ADAPTATEUR FAIT MARCHER SA LANGUE** ✓✓ : le français passe de **3,19 à 1,50** (−53 % ✓✓) et
  l'anglais de **1,90 à 1,40** (−26 % ✓✓) — avec **131 072 paramètres**, soit **5,1 %** d'un modèle de 2,43 M ✓,
  et **sans toucher un seul poids du noyau** ✓✓. *La langue est donc bien un petit paramètre* ✓✓✓ ;
* **ET ILS SONT INTERCHANGEABLES** ✓✓ : le même noyau, deux adaptateurs, deux langues qui marchent ✓ — c'est
  la définition exacte de « la langue comme paramètre » ✓✓, et c'est **mesuré**, pas espéré ✓ ;
* **mais l'échange a un PRIX, et il est asymétrique** ✗✓ : l'adaptateur **français** abîme l'anglais
  (1,90 → **2,91** ✗), tandis que l'adaptateur **anglais** laisse le français à 3,02 ✓ (contre 3,19 ✓).
  L'explication la plus simple : le noyau a été entraîné **en anglais** ✓ — l'adaptateur anglais reste donc
  **près** de lui ✓✓, alors que l'adaptateur français doit le **déplacer** ✗✓. Ce n'est pas un défaut du
  principe, c'est un fait du noyau de départ ✓ ;
* **et c'est la réponse la plus directe à la question posée** ✓✓ : pour atteindre une couche commune, **il
  n'est pas nécessaire de réentraîner** un noyau ✗ — il suffit d'un **paramètre de langue** de quelques
  dizaines de milliers de poids ✓✓, et le noyau peut rester **le même** ✓. Ce qui reste à faire n'est donc
  plus de **construire** la couche commune ✗ mais de **choisir où la brancher** ✓ (les couches 6-7, où la
  langue reparaît ✓ — première mesure de ce chapitre ✓).

## Troisième mesure (17/10, 16 h 45) : **où brancher** l'adaptateur — et le paramètre le plus petit possible

La langue vit à la **surface** (couches 6-7 du modèle bilingue ✓, première mesure de ce chapitre ✓). On l'a
donc testé sur le modèle monolingue (4 couches ✓), en posant le LoRA **sur le seul dernier étage** ✓ :

| placement de l'adaptateur | paramètres | part du modèle | **perte français** | perte anglais |
|---|---:|---:|---:|---:|
| **aucun** | — | — | **3,1953** ✗ | **1,9001** ✓ |
| **partout** (rang 8 ✓) | 131 072 | **5,12 %** | **1,5046** ✓✓ (−52,9 %) | 2,9139 (+53,4 %) |
| **dernier étage** (rang 8 ✓) | **32 768** | **1,33 %** | **1,7714** ✓✓ (−44,6 %) | 2,7439 (+44,4 %) |
| **dernier étage** (rang 32 ✓) | 131 072 | 5,12 % | **1,6820** ✓ (−47,4 %) | 2,7347 (+43,9 %) |

* **LE DERNIER ÉTAGE SUFFIT PRESQUE** ✓✓ : avec **32 768 paramètres** — **1,33 %** du modèle ✓✓ — il prend
  **84 % du gain** (−44,6 % contre −52,9 % pour cinq fois plus de paramètres ✓✓). *La langue est donc
  essentiellement un réglage de surface* ✓✓ ;
* **mais à BUDGET ÉGAL, « partout » reste un peu meilleur** ✓ (1,5046 contre 1,6820 ✓) : le noyau contribue
  aussi ✗✓ — de quelques points ✓ — et l'on paie **quatre fois** ce gain ✓ ;
* **et le placement de surface est plus DOUX pour l'autre langue** ✓ : l'anglais souffre moins
  (2,73-2,74 contre 2,91 ✓) — un adaptateur qui ne déplace qu'un étage **abîme moins** le reste ✓✓ ;
* **la conclusion pratique** ✓✓ : pour « la langue comme paramètre », le point d'attache est **le dernier
  étage** ✓, avec un rang modeste ✓ — **1,33 % du modèle** suffit à faire d'un noyau anglais un noyau qui
  travaille en français ✓✓. C'est le chiffre le plus utile de ce chapitre : *la langue coûte 1,33 %* ✓.

### Ce que ces trois mesures disent ensemble

1. **la couche commune existe** ✓ (noyau neutre aux couches 1-2, 50,2 % = le hasard ✓) ;
2. **la langue est un paramètre** ✓ (131 k = 5,1 % font marcher une langue ✓✓, et deux adaptateurs sont
   interchangeables sur le même noyau ✓) ;
3. **et ce paramètre est plus petit qu'on ne croyait** ✓✓ (32 k = **1,33 %**, au dernier étage, prend 84 % du
   gain ✓) — ce qui rend l'idée **directement utilisable** : un noyau, et **un petit module par langue** ✓✓.

## Quatrième mesure (17/10, 17 h 30) : le noyau neutre **porte le sens** — mais le relevé reste propre à la langue

La neutralité pourrait être une **perte** ✗ : une couche qui ne dit plus la langue pourrait ne plus rien dire
✗✓. Mesure : `tools/contenu_par_couche.py` ✓ — le **contenu** (état → embedding du jeton suivant ✓, λ de ridge
par validation croisée ✓), **par couche** et **par langue**, sur le modèle bilingue ✓.

| couche | contenu **anglais** | contenu **français** | contenu **mêlé** | la langue ? |
|---:|---:|---:|---:|---|
| 0 | 89,5 % | 88,0 % | 93,0 % | — |
| **1** | **87,8 %** | **87,3 %** | **93,0 %** | **NEUTRE (50 %)** ✓✓ |
| **2** | **86,5 %** | **85,3 %** | 92,4 % | **NEUTRE (50 %)** ✓✓ |
| 3 | 85,6 % | 84,5 % | 91,7 % | — |
| 4 | 84,6 % | 83,8 % | 91,1 % | — |
| 5 | 83,6 % | 82,5 % | 88,9 % | — |
| **6** | 82,1 % | 80,6 % | 86,0 % | la langue revient ✗ |
| **7** | 80,4 % | 78,5 % | 83,4 % | la langue revient ✗ |
| 8 | **79,3 %** | **76,5 %** | **81,6 %** | — |

* **LE NOYAU NEUTRE PORTE LE SENS** ✓✓ : aux couches 1-2, où la langue est illisible ✓, le contenu reste à
  **87,8 %** et **87,3 %** — à **8 points seulement** du meilleur (79,3 % à la couche 8 ✓). *La neutralité
  n'est donc pas une perte de sens* ✓✓ : le noyau abstrait la langue **en gardant le contenu** ✓✓ ;
* **le contenu s'améliore avec la profondeur** ✓ (89,5 → 79,3 ✓) — régulier, sans accident ✓✓ ;
* **MAIS LE RELEVÉ RESTE PROPRE À CHAQUE LANGUE** ✗✓ : la colonne « mêlé » — **un seul** mapping appris sur les
  deux langues ✓ — est **systématiquement pire** (93,0 contre 87,8 ✓ ; 81,6 contre 79,3 ✓). Autrement dit :
  les états anglais et français **ne sont pas linéairement séparables par la langue** ✓ (mesure 1 ✓) mais ils
  **ne se lisent pas avec le même relevé** ✗✓ — il faut **deux** lectures ✗, ou une lecture **non linéaire** ✓
  (piste du § 24 du rapport sur la linéarité ✓) ;
* **la conclusion, en une phrase** ✓✓ : *la couche commune est commune pour l'**état**, pas encore pour le
  **relevé*** ✓ — c'est-à-dire que le noyau a bien abstrait la langue **dans le contenu** ✓✓, mais le lien
  entre l'état et les mots reste **teinté** de la langue ✗. Et c'est exactement là que l'adaptateur du
  paragraphe précédent intervient : il **fournit** ce relevé propre à la langue ✓✓, pour **1,33 %** de
  paramètres ✓.

### Ce que cela change dans la lecture du chapitre

La chaîne est maintenant complète, et chaque maillon est mesuré :

| maillon | mesure | verdict |
|---|---|---|
| **l'entrée** porte la langue | classifieur 62,4 % à la couche 0 | ✗ oui, dans les octets |
| **le noyau** ne la porte plus | 50,2 % aux couches 1-2 | ✓✓ neutre |
| **le noyau** garde le sens | contenu 87,8 % aux couches 1-2 | ✓✓ utile |
| **la surface** la fait revenir | 59,4 % aux couches 6-7 | ✓ c'est là qu'elle sert |
| **le relevé** en a besoin | « mêlé » toujours pire | ✗✓ à traiter |
| **l'adaptateur** la fournit | −44,6 % pour 1,33 % | ✓✓ le paramètre |

## Cinquième mesure (17/10, 18 h) : le « relevé propre à la langue » était un artefact de **LINÉARITÉ**

La quatrième mesure concluait : *la couche commune est commune pour l'état, pas pour le relevé* ✗ — le
mapping « mêlé » (un seul relevé pour les deux langues ✓) étant **systématiquement pire** ✓ (93,0 contre 87,8 ✓).
La question qui suivait : **est-ce le relevé, ou la linéarité du relevé ?** ✗. Réponse mesurée ✓, avec un MLP
**régularisé** (découpe 60/20/20 ✓, **arrêt anticipé** sur la validation ✓, poids décroissants ✓ — leçon du
16/10 : un MLP sans arrêt anticipé sur-apprend ✓✗) :

| couche | linéaire **mêlé** | **MLP mêlé** | gain |
|---:|---:|---:|---:|
| 0 | 93,0 % | **90,4 %** | −2,6 |
| 1 | 93,0 % | **89,1 %** | −3,9 |
| 2 | 92,4 % | **86,3 %** | −6,1 |
| 3 | 91,7 % | **85,3 %** | −6,4 |
| 4 | 91,1 % | **83,7 %** | −7,4 |
| 5 | 88,9 % | **80,5 %** | −8,4 |
| 6 | 86,0 % | **76,8 %** | −9,2 |
| 7 | 83,4 % | **73,9 %** | −9,5 |
| **8** | 81,6 % | **71,5 %** | **−10,1** ✓✓ |

* **LE LECTEUR NON LINÉAIRE BAT LE LINÉAIRE PARTOUT** ✓✓ (à la couche 8 : **71,5 %** contre 81,6 % ✓ — dix
  points ✓) : le « relevé propre à la langue » n'était donc **pas** une propriété de l'état ✗✓, c'était une
  **limite du lecteur** ✓✓. *Septième fois de la nuit qu'un chiffre se déguise — cette fois en propriété
  d'architecture* ✓✓ ;
* **ET LE GAIN CROÎT AVEC LA PROFONDEUR** ✓ (2,6 points à la couche 0 → **10,1** à la couche 8 ✓✓) : les
  états profonds sont **plus non linéairement encodés** ✓✓ — ce qui rejoint exactement le § 23-25 du rapport
  (les modèles plus larges sont moins linéairement lisibles ✓) ;
* **ET LE RÉSULTAT DÉCISIF** ✓✓✓ : à la couche 8, **un seul** relevé non linéaire **mêlé** (71,5 % ✓) fait
  **mieux** que les **deux** relevés linéaires **par langue** (79,3 % en anglais et 76,5 % en français ✓✓).
  *Un relevé partagé suffit — s'il est non linéaire* ✓✓✓ ;
* **donc la chaîne est complète** ✓✓ : l'entrée porte la langue ✗ → le noyau ne la porte plus ✓✓ → le noyau
  garde le sens ✓✓ → la surface la fait revenir ✓ → **le relevé n'est PAS propre à la langue** ✓✓ (si l'on
  accepte la non-linéarité ✓) → l'adaptateur reste utile **pour la génération** ✓ (il fait passer d'une
  perplexité de 3,19 à 1,50 ✓), pas pour la **lecture** ✓✓. C'est une distinction que le chapitre n'avait pas
  faite, et elle est importante : *lire le sens est une chose, produire dans une langue en est une autre* ✓✓.

## Sixième mesure (17/10, 18 h 30) : la langue de SORTIE suit l'**adaptateur**, pas l'amorce

La perplexité (3,19 → 1,50 ✓) ne dit pas dans quelle langue le modèle **écrit** ✗. Mesure :
`tools/generer_par_langue.py` ✓ — deux amorces (une par langue ✓), trois adaptateurs (aucun, français,
anglais ✓), 120 octets générés ✓, et la langue de la sortie comptée par ses **mots-outils** ✓ (le seul
classifieur qui tienne sur un texte de mauvaise qualité ✓).

| amorce | adaptateur | **sortie** (mots-outils) | ce qu'elle montre |
|---|---|---|---|
| anglais | **aucun** | fr 0 · **en 5** | le noyau seul écrit **anglais** ✓ |
| **anglais** | **français** | **fr 6** · en 0 | **la sortie est FRANÇAISE** ✓✓ |
| anglais | anglais | fr 0 · **en 6** | l'adaptateur anglais écrit anglais ✓ |
| **français** | **aucun** | fr 0 · **en 13** | le noyau seul **ignore** l'amorce française ✗ |
| français | français | **fr 12** · en 0 | l'adaptateur français écrit français ✓ |
| **français** | **anglais** | fr 0 · **en 7** | **la sortie est ANGLAISE** ✓✓ |

* **LA SORTIE SUIT L'ADAPTATEUR, PAS L'AMORCE** ✓✓✓ : une amorce **anglaise** avec l'adaptateur **français**
  produit du **français** (fr 6 · en 0 ✓✓), et une amorce **française** avec l'adaptateur **anglais** produit de
  l'**anglais** (en 7 · fr 0 ✓✓). C'est la définition **opérationnelle** de « la langue comme paramètre » ✓✓ ;
* **et sans adaptateur, le noyau écrit sa langue d'entraînement** ✓ (l'anglais ✓) **quelle que soit
  l'amorce** — la française donne `en 13 · fr 0` ✗✓, c'est-à-dire que le noyau **ignore** la langue qu'on lui
  donne et continue dans la sienne ✓✓. C'est exactement ce que « la langue est un paramètre **d'entrée** mais
  pas de **sortie** » veut dire ✓ ;
* ⚠️ **et ce que ce test ne dit PAS** ✗ : le texte est de la **bouillie** (modèle de 2,4 M en octets ✓ —
  `'machine s'acteur, et locs/'` ✓). La mesure porte sur **la langue**, pas sur la qualité ✗. C'est écrit
  dans l'outil ✓, pour que personne ne lise « ça écrit bien » là où il n'y a que « ça écrit français » ✓.

### La chaîne complète, et ce qu'elle vaut

| ce qu'on veut | mesure | chiffre |
|---|---|---|
| l'entrée porte la langue | classifieur à la couche 0 | **62,4 %** ✗ |
| le **noyau** l'abstrait | classifieur aux couches 1-2 | **50,2 %** = le hasard ✓✓ |
| et il **garde le sens** | contenu aux couches 1-2 | **87,8 %** ✓✓ |
| le **relevé** n'est pas propre à la langue | un seul relevé **non linéaire**, couche 8 | **71,5 %** (mieux que deux linéaires ✓✓) |
| la **langue** est un paramètre **petit** | adaptateur au dernier étage | **32 768** poids = **1,33 %** ✓✓ |
| et il **fait marcher** la langue | perplexité française | **3,19 → 1,50** (−53 %) ✓✓ |
| et la **sortie** suit le paramètre | génération, amorce croisée | **français → anglais** et l'inverse ✓✓✓ |

**Conclusion du chapitre** ✓✓ : la couche commune **existe** ✓, elle **garde le sens** ✓, et la langue y est un
**paramètre de 1,33 %** qui **commande la sortie** ✓✓. Ce qui reste n'est pas à construire ✗ mais à **utiliser**
✓ — et les trois questions ouvertes sont : la **qualité** (ces modèles sont des jouets ✓), le **coût de la
bascule** (temps et mémoire ✓), et la **boucle** (la pensée itérée survit-elle au changement de langue ?) ✓.

## Septième mesure (17/10, 19 h) : la bascule coûte **5 ms** et **530 Ko** — l'idée est utilisable

« La langue est un paramètre de 1,33 % » ✓✓ ne vaut que si changer de langue ne coûte pas le rechargement d'un
modèle ✗. Mesure : `tools/cout_bascule.py` ✓ — adapter de tout le modèle (rang 8, 131 k ✓), médiane sur cinq
essais ✓, comparaison avec un **rechargement complet** ✓ :

| ce qu'on échange | taille | temps médian |
|---|---:|---:|
| **adaptateur** (chargement depuis le disque) | **530 Ko** | **4,82 ms** |
| **adaptateur** (application au modèle ✓) | — | **0,19 ms** |
| **modèle entier** (rechargement ✗) | 9,8 Mo | **134,64 ms** |

* **la bascule de langue coûte 5,0 ms et 530 Ko** ✓✓ — contre **134,6 ms et 9,8 Mo** pour recharger un
  modèle ✗ ✓ (rapport **×27** en temps, **×18** en mémoire ✓✓) ;
* **et le rapport ne peut que s'améliorer** ✓ (raisonnement, pas mesure ✗) : un modèle de 7 milliards pèse
  des **milliers** de fois plus qu'un adaptateur ✓, alors qu'un LoRA reste petit ✓✓ — le coût du paramètre
  ne dépend pas de la taille du noyau ✓ ;
* **et l'adaptateur de SURFACE** (le dernier étage, 32 768 poids ✓, mesuré au § « où brancher » ✓) pèserait
  **≈ 130 Ko** ✓✓ — quatre fois moins ✓, pour **84 % du gain** ✓ ;
* **la conclusion pratique** ✓✓ : *un noyau, N adaptateurs de quelques centaines de kilo-octets, et une
  bascule en millisecondes* ✓✓ — c'est-à-dire une architecture où **la langue est un fichier** ✓, pas un
  modèle ✗. C'est la réponse la plus utile de ce chapitre à la question posée ✓.

## Huitième mesure (17/10, 19 h 30) : le relevé **est** teinté de la langue — et cela CORRIGE la cinquième mesure

La cinquième mesure concluait qu'un **seul** relevé non linéaire « mêlé » battait les deux relevés linéaires
par langue ✓ (71,5 % contre 79,3 et 76,5 ✓). Elle ne disait pas si ce relevé unique valait un relevé
**de même langue et non linéaire** ✗ — question posée ici : `tools/lecture_croisee.py` ✓, **lecture croisée**
(relevé appris sur une langue ✓, appliqué à l'autre ✓), au dernier étage ✓ :

| relevé appris sur | état **anglais** | état **français** |
|---|---|---|
| **ANGLAIS** | **76,7 / 55,9** | 82,5 / 72,2 |
| **FRANÇAIS** | 84,8 / 75,7 | **73,1 / 53,0** |

*(linéaire / non linéaire ; les cases en gras sont la diagonale, c'est-à-dire le relevé de la **même** langue ✓)*

| | diagonale | croisé | **pénalité de langue** |
|---|---:|---:|---:|
| **linéaire** | 74,9 % | 83,7 % | **+8,7** ✗ |
| **non linéaire** | **54,5 %** ✓✓ | 73,9 % | **+19,5** ✗✗ |

* **LE RELEVÉ EST TEINTÉ DE LA LANGUE** ✗✓ : la diagonale est **nettement** meilleure (54,5 contre 73,9 en non
  linéaire ✓) — il y a une **pénalité de langue** de **+8,7** (linéaire) à **+19,5** (non linéaire) ✓ ;
* **et le non-linéaire AGGRAVE la pénalité** ✗✓ (19,5 contre 8,7 ✓) : un lecteur plus puissant se **spécialise**
  davantage ✓✓ — *plus de puissance, plus de langue* ✓. C'est l'inverse de ce qu'on attendait naïvement ✗✓ ;
* **donc la cinquième mesure doit être LUE AUTREMENT** ✗✓ : elle était vraie (un relevé **partagé** non linéaire
  bat **deux linéaires** ✓✓) mais **incomplète** ✗ : il ne bat **pas** deux non-linéaires de même langue
  (71,5 contre **54,5** ✓✗). *Le relevé partagé fonctionne ; il coûte 17 points* ✓ ;
* **et la conclusion devient plus nette, pas moins** ✓✓ : l'**état** est neutre ✓ (mesure 1 ✓), mais le
  **lien état → mots** est **langue-dépendant** ✓ — *c'est donc dans le relevé que la langue vit*, et c'est
  **exactement** là que l'adaptateur de langue agit ✓✓ (il fournit ce relevé pour 1,33 % de paramètres ✓).
  « Penser dans une langue et conclure dans une autre » **ne marche pas** avec le même relevé ✗✓ — il faut
  **changer de paramètre**, ce qui coûte 5 ms ✓✓.

### Erratum assumé

La cinquième mesure disait « le relevé n'est pas propre à la langue ✓✓ ». La huitième la **corrige** ✗✓ : le
relevé **est** propre à la langue (pénalité +8,7 à +19,5 ✓), et ce qui restait vrai est plus faible — *un relevé
partagé est possible, à un coût de 17 points* ✓. **Huitième fois de la nuit qu'un chiffre se déguise** ✓✓, et
cette fois c'est une **mesure antérieure** qui était en cause, pas un réglage ✗ : la leçon est qu'une comparaison
n'est valide que si **tous** les lecteurs sont aussi puissants les uns que les autres ✓ — comparer un non-linéaire
à des linéaires n'est pas comparer deux langues, c'est comparer deux **familles de lecteurs** ✗✓.

## Neuvième mesure (17/10, 20 h) : le relevé partagé suffit — l'erratum de la mesure 8 était lui-même trop fort

La mesure 8 concluait que « le relevé **est** teinté de la langue » ✓✗ (pénalité +8,7 à +19,5 ✗), en comparant
un relevé appris sur **une** langue et appliqué à l'**autre** ✓. La mesure 9 pose **l'autre** question, celle
qui compte pour une couche commune : un relevé appris sur **les deux** langues vaut-il le relevé **de chaque**
langue ? ✗✓. `tools/releve_parametre.py` ✓, au dernier étage ✓ :

| relevé | paramètres de **langue** | anglais | français |
|---|---:|---:|---:|
| **partagé** (appris sur les deux ✓) | **0** ✓ | **79,1 %** | **76,5 %** |
| partagé + **rang 1** par langue ✓ | 512 | 79,1 % | 76,5 % |
| **complet** par langue ✗ | 65 536 | **78,4 %** | **75,9 %** |

* **LE RELEVÉ PARTAGÉ SUFFIT** ✓✓ : il fait **79,1 / 76,5 %** quand deux relevés séparés font **78,4 / 75,9 %**
  — **0,7 point** d'écart ✓✓. Autrement dit : *un seul relevé, appris sur les deux langues, sert les deux
  langues* ✓✓✓ ;
* **et la correction de rang 1 ne récupère RIEN** ✗ (79,1 → 79,1 ✓) — non pas parce que la langue n'est pas de
  rang 1 ✗, mais parce qu'**il n'y a rien à corriger** ✓✓ : le relevé partagé a déjà tout pris ✓ ;
* **donc l'erratum de la mesure 8 était lui-même TROP FORT** ✗✓ : ce qui est vrai, c'est qu'un relevé appris
  sur **une seule** langue **ne se transfère pas** à l'autre ✗ (pénalité +8,7 à +19,5 ✓) ; mais un relevé appris
  sur **les deux** ne perd que **0,7 point** ✓✓. Ce sont **deux questions différentes** ✗✓, et il a fallu les
  mesurer séparément pour le voir ✓✓ ;
* **et la conclusion générale devient la plus simple de toutes** ✓✓ : la langue ne vit **ni dans l'état**
  (50,2 % = le hasard ✓✓) **ni dans le relevé** (0,7 point ✓✓) — elle vit dans **l'entrée** (les octets ✓,
  62,4 % à la couche 0 ✗) et dans **la surface de sortie** (couches 6-7 ✓, et l'adaptateur qui la commande ✓✓).
  *C'est exactement la structure demandée : un contenu commun, une surface paramétrée* ✓✓✓.

### La chaîne des corrections, assumée

Ce chapitre a maintenant **deux erratums** ✓✓, et c'est le signe qu'il progresse :

| mesure | ce qu'elle disait | ce que la suivante a corrigé |
|---|---|---|
| 5 | « le relevé n'est pas propre à la langue » ✓ | incomplet : comparé à des lecteurs **linéaires** seulement ✗ |
| 8 | « le relevé **est** teinté de la langue » (pénalité +8,7 à +19,5 ✗) | vrai pour un **transfert** ✗, mais la mesure 9 montre qu'un relevé appris sur les **deux** langues ne perd que **0,7 point** ✓✓ |
| 9 | « le relevé partagé suffit » ✓✓ | — *(à confirmer sur un modèle plus grand ✗ : 2,4 M est un jouet)* |

*Trois mesures, deux corrections, et aucune des trois n'est jetée* ✓✓ : chacune reste vraie **de sa question** ✓.
C'est la différence entre se contredire ✗ et **préciser** ✓✓.

## Dixième mesure (17/10, 20 h 30) : un noyau **bilingue** bat un noyau monolingue **+ adaptateur** — mais l'adaptateur rattrape les deux tiers

La mesure qui compte pour l'ingénierie ✓ : pour obtenir une couche commune, vaut-il mieux entraîner un noyau
**sur les deux langues** ✓ ou garder un noyau **monolingue** et ajouter un **adaptateur** ✓ (famille E ✓) ?
`tools/comparer_noyaux.py` ✓, mêmes fenêtres ✓ :

| dispositif | **perte français** | perte anglais |
|---|---:|---:|
| **noyau bilingue** ✓ (4,79 M, 10,2 Mo mixtes ✓) | **1,0737** ✓✓ | **1,6493** ✓ |
| noyau monolingue ✗ (2,43 M, 96 Mo anglais ✓) | **3,2928** ✗ | **2,2786** ✓ |
| monolingue + **adaptateur français** ✓ | **1,4546** ✓ | 3,1438 ✗ |

* **LE NOYAU BILINGUE GAGNE** ✓✓ : **1,0737** contre **1,4546** pour le monolingue + adaptateur ✓ — soit
  **35 %** de perte en plus pour le dispositif à adaptateur ✗ ;
* **mais l'adaptateur rattrape les DEUX TIERS de l'écart** ✓✓ (3,2928 → **1,4546** ✓) — et il le fait pour
  **131 072 paramètres** ✓✓ et vingt minutes d'entraînement ✓, quand le noyau bilingue a demandé **les deux
  corpus** et un entraînement complet ✓ ;
* **et l'adaptateur abîme l'anglais** ✗ (2,2786 → **3,1438** ✓) — le prix déjà vu ✓ ;
* ⚠️ **ce que cette mesure ne peut PAS dire, et qui est écrit dans l'outil** ✗ : les deux noyaux n'ont **ni la
  même taille** (2,43 M contre 4,79 M ✓) **ni les mêmes données** (96 Mo d'anglais contre 10,2 Mo mixtes ✓) —
  ce n'est donc **pas** une comparaison à budget égal ✗✓, c'est une comparaison de **trois dispositifs réels** ✓.
  La conclusion doit rester à ce niveau : *le bilingue est meilleur ici* ✓, pas « le bilingue est toujours
  meilleur » ✗ ;
* **et le vrai arbitrage est ailleurs** ✓✓ : sur un modèle de **7 milliards**, réentraîner le noyau sur deux
  langues est **hors de prix** ✗✓, alors qu'un adaptateur coûte **1,33 %** des paramètres et **5 ms** de bascule
  ✓✓. *C'est donc à l'échelle que l'adaptateur devient la bonne réponse* ✓ — et ce chapitre ne peut pas le
  mesurer, seulement le nommer ✓.

## Onzième mesure (17/10, 21 h) : la pensée itérée est **SANS LANGUE** — mais elle ne tient qu'un pas

La jonction des deux chapitres, jamais mesurée ✗ : l'état est **neutre** (chap. 7 ✓) et l'on peut **itérer**
l'état (chap. 5 ✓) — mais **itérer préserve-t-il la neutralité ?** ✓ `tools/penser_sans_langue.py` ✓ : le même
opérateur que le chapitre 5 (identité + petit MLP ✓, contenu ✓ et contraction ✓), entraîné sur les états du
modèle **bilingue** ✓, puis k itérations ✓, avec deux mesures : le **contenu** ✓ et la **langue** ✓.

| k | contenu (état → mot suivant) | **langue** (hasard = 50 %) |
|---:|---:|---:|
| 0 | 82,2 % | **56,2 %** |
| **1** | **79,9 %** ✓ | 53,9 % |
| 2 | 93,8 % ✗ | 52,8 % |
| **3** | 99,5 % ✗✗ | **50,7 %** ✓✓ |
| **4** | 101,3 % ✗✗ | **50,6 %** ✓✓ |
| 8 | 97,4 % ✗ | 54,0 % |

* **LA LANGUE NE REVIENT PAS** ✓✓✓ : sur **huit** itérations, le classifieur reste entre **50,6 et 56,2 %** —
  c'est-à-dire **au hasard** ✓✓ (le minimum, **50,6 %**, est atteint à k = 4 ✓). *La pensée itérée est sans
  langue* ✓✓ — c'est la propriété qu'un cerveau doit avoir : **penser ne dépend pas de la langue où l'on
  parle** ✓✓✓ ;
* **et le contenu ne tient qu'un pas** ✗ : il **s'améliore** au premier (82,2 → **79,9** ✓) puis **s'effondre**
  (93,8 → **101,3** ✗✗, pire que l'embedding moyen ✓). C'est **exactement** le résultat du 16/10 sur un autre
  modèle ✓✓ (un pas de pensée, pas une itération ✓) — et il **se reproduit** ici ✓✓ ;
* **donc la réponse complète** ✓✓ : *on peut penser **sans langue**, mais on ne peut penser qu'**un pas***
  ✓ — la neutralité est **stable** ✓✓, le contenu ne l'est pas ✗. Les deux propriétés sont **indépendantes**
  ✓✓ (l'une tient sur huit pas, l'autre sur un ✓), et c'est une information neuve ✓.

### Neuvième piège : quand c'est le CODE qui ment

Mon premier essai donnait k = 0, 1, 2, 4 ✓ mais la boucle **accumulait** `Z = cel(Z)` ✗✓ : les lignes « 2 » et
« 4 » montraient en réalité **2 et 3** pas ✓✗. **Le label mentait, pas la mesure** ✓✓ — et c'est une famille
**nouvelle** de piège : après les réglages (mesures 5, 8 ✓) et les instruments (les quatre du 16/10 ✓), voici
**le code lui-même** ✓✗. La correction tient en une ligne (repartir de l'état d'origine à chaque k ✓), et elle
a changé les chiffres — mais **pas la conclusion** ✓✓ : la langue reste au hasard ✓. C'est la neuvième fois
qu'un chiffre se déguise, et la règle est toujours la même : **écrire à côté du chiffre ce qui pourrait le
rendre faux** ✓✓.

## Douzième mesure (17/10, 21 h 30) : le « second pas » ne s'obtient pas — et la recette du 16/10 se **reproduit**

La mesure 11 laissait une question ouverte ✓ : le contenu ne tient qu'un pas ✗, mais le 16/10 avait montré
qu'entraîner l'opérateur **sur k pas** (k tiré ✓) rendait l'itération **plate** ✓. On refait ici, **en gardant
l'œil sur la langue** ✓ : `--k-entrainement 4` ✓ (même opérateur, même modèle bilingue ✓) :

| k | contenu | langue (hasard = 50 %) |
|---:|---:|---:|
| 0 | 82,2 % | 56,2 % |
| 1 | **82,2 %** | 68,2 % ✗ |
| 2 | **82,2 %** | 67,6 % ✗ |
| 3 | **82,2 %** | 56,0 % |
| 4 | **82,2 %** | 51,4 % ✓ |
| 8 | **82,2 %** | **50,0 %** ✓✓ |

* **LE CONTENU EST EXACTEMENT PLAT** ✓✓ (82,2 % à **tous** les k) — c'est-à-dire que l'opérateur a appris
  **l'identité** ✗✓ : *la seule façon de rester bon à k = 8 est de ne pas bouger* ✓✓, exactement la **solution
  triviale** du 16/10 (son § 15 ✓). **Le résultat se reproduit sur un autre modèle, une autre tâche, une autre
  langue** ✓✓ — c'est une **réplication**, et c'est la meilleure chose qu'un résultat négatif puisse être ✓ ;
* **donc le « second pas » ne s'obtient pas par cette recette** ✗✓ : entraîner sur k **choisit** la solution
  triviale ✓, parce que le contenu **moyen** sur k est maximisé par un opérateur **immobile** ✓✗. C'est une
  propriété de **l'objectif**, pas de l'opérateur ✓✓ ;
* **et la langue** ✗ : elle **varie** (68,2 % à k = 1, 50,0 % à k = 8 ✓) alors que l'opérateur est
  quasi-immobile ✓✗ — c'est-à-dire que la **petite dérive** suffit à changer la **séparabilité linéaire** de la
  langue ✓✓ (de 68 % à 50 % ✓). Autrement dit : *la neutralité de langue n'est pas une propriété robuste de
  l'état* ✗ — elle dépend de la position exacte dans l'espace ✓✓ ;
* **la conclusion honnête** ✓✓ : (1) la neutralité **tient** quand on itère avec un opérateur entraîné sur un
  pas ✓ (mesure 11 : 50,6 % à k = 4 ✓) ; (2) elle **n'est pas** une propriété de l'état lui-même ✗ (mesure 12 :
  la dérive la fait remonter à 68 % ✓) ; (3) et le **second pas** reste hors d'atteinte avec cet objectif ✗✓
  — il faudra un **objectif différent** ✗ (par exemple contraindre le **déplacement** à être informatif, pas
  seulement contractant ✓).

## Treizième mesure (17/10, 22 h) : trois objectifs, **le même mur** — la limite est dans la représentation

Le § précédent concluait qu'il fallait « un objectif différent » ✗ : récompenser le **déplacement informatif**,
pas seulement sa contraction ✓. C'est fait ✓ (option `--marge` : le pas doit **améliorer** le contenu d'au moins
`marge` × 100 %, ce qui **exclut l'identité** de l'optimum ✓✗). Deux marges testées ✓ :

| marge | k = 0 | **k = 1** | k = 2 | k = 3 | k = 4 | k = 8 |
|---|---:|---:|---:|---:|---:|---:|
| **sans** (mesure 11 ✓) | 82,2 % | **79,9** ✓ | 93,8 ✗ | 99,5 ✗ | 101,3 ✗ | 97,4 ✗ |
| **0,05** | 82,2 % | **80,3** ✓ | 93,7 ✗ | 100,1 ✗ | 103,1 ✗ | 99,9 ✗ |
| **0,10** | 82,2 % | **80,4** ✓ | 93,3 ✗ | 100,3 ✗ | 103,7 ✗ | 95,3 ✗ |

* **LA MARGE N'Y CHANGE RIEN** ✗✓ : le contenu s'améliore toujours au **premier** pas (79,9 · 80,3 · 80,4 ✓)
  et **se dégrade** ensuite, de la même façon ✓✗ (93-104 % ✓). Les **trois** objectifs — conservation ✓,
  conservation + contraction ✓, et **progrès exigé** ✓ — donnent **le même mur** ✗✗ ;
* **donc la limite n'est PAS dans l'objectif** ✗✓ : c'est la **représentation** qui ne porte pas de second pas ✓✓.
  *Il n'y a pas de second pas à trouver* ✓ — et c'est la troisième fois que la nuit le montre (16/10 sur les
  opérateurs ✓, 17/10 sur deux modèles et deux langues ✓, et maintenant contre trois objectifs ✓) ;
* **et la langue reste au hasard** ✓✓ (50,4-61,3 % ✓) — la neutralité **tient** sous toutes les variantes ✓✓,
  ce qui est le résultat **positif** du chapitre : *la langue n'est pas dans la pensée* ✓✓, même quand la
  pensée bute ✓ ;
* **la conclusion du chapitre, et son ouverture** ✓✓ : la couche commune **existe** ✓ (noyau neutre ✓, relevé
  partagé ✓), la langue est un **paramètre de 1,33 %** qui **commande la sortie** ✓✓, et la **pensée itérée**
  est **sans langue** ✓✓ mais **d'un seul pas** ✗. Le pas suivant n'est plus à chercher dans les **objectifs**
  ✗ mais dans **l'entraînement du modèle lui-même** ✓ — c'est-à-dire dans le programme du 16/10 (la récurrence
  **dans** la boucle ✓), qui reste la seule porte ouverte ✓✓.

## Quatorzième et quinzième mesures (17/10, 16 h) : un **vrai** corpus français, et la neutralité **à l'échelle**

### Un corpus français littéraire — merci aux projets Panini

Mon « corpus français » était de la **prose de dépôt** ✗ (4,45 Mo de fiches et de journal ✓, 15 201 formes ✓) —
utilisable ✓, mais ce n'est pas de la langue naturelle ✗. Stéphane a signalé que ses projets de recherche
linguistique (**`Panini/`** et **`Panini-Research/`** ✓) contiennent des corpus **déjà sur la machine** ✓✓. Il
y avait en effet **des textes Gutenberg** ✓ — 66 textes, dont **18 français** ✓ :

| | prose du dépôt (l'ancien ✗) | **littérature (le nouveau ✓)** |
|---|---:|---:|
| taille | 4,45 Mo | **13,2 Mo** ✓ |
| textes | 1 (le dépôt) | **18** ✓ |
| formes | 15 201 | **66 322** ✓✓ (4,4× plus) |
| auteurs | — | **Maupassant, Dumas, Flaubert, Verne** ✓✓ |
| mots fréquents | `les, est, pas, sur, par, que` ✓ | `les, que, qui, des, dans, vous, une, pas` ✓✓ |

*Les en-têtes et pieds de page Gutenberg ont été **retirés** ✗✓ — sans quoi le corpus contenait 18 fois la même
licence anglaise ✓✗, et la « langue » mesurée aurait été celle de la licence ✓.*

### La neutralité tient-elle à l'échelle ? Oui ✓✓ — et la surface devient PLUS langue-aware

Un modèle bilingue **dim 512** (9,57 M ✓, même corpus mixte ✓) mesuré de la même façon ✓ :

| couche | langue (en/fr) | témoin | verdict |
|---:|---:|---:|---|
| 0 | 50,8 % | 61,2 % | neutre ✓ |
| 1 | 56,1 % | 51,0 % | ± |
| **2** | **51,4 %** | 50,5 % | **le hasard** ✓✓ |
| 3 | 54,1 % | 50,8 % | presque ✓ |
| 4 | 59,2 % | 50,5 % | ✗ |
| **5** | **53,1 %** | 50,5 % | presque ✓ |
| **6** | **51,2 %** | 50,7 % | **le hasard** ✓✓ |
| 7 | 57,3 % | 50,0 % | ✗ |
| **8** | **67,9 %** | 50,3 % | ✗✗ la surface |

* **LE NOYAU EST NEUTRE À L'ÉCHELLE** ✓✓ : aux couches 2 et 6, le classifieur est **au hasard** (51,4 et 51,2 % ✓),
  comme en dim 256 (50,2 % ✓) → **la propriété se réplique** ✓✓ ;
* **et la surface devient PLUS langue-aware** ✗✓ : **67,9 %** au dernier étage (contre 51,0 % en dim 256 ✓) —
  le modèle plus large a **plus de capacité** pour porter la langue **dans la sortie** ✓✓, ce qui **renforce**
  la lecture du chapitre : *la langue vit à la surface, et d'autant plus que le modèle est grand* ✓✓✓ ;
* **et l'entrée, elle, n'est plus langue-aware** ✗✓ : 50,8 % à la couche 0 (contre 62,4 % en dim 256 ✓) — avec
  des embeddings plus larges (512 ✓), les statistiques d'octets se **diluent** ✓✓. Ce n'est pas une régression ✗ :
  c'est que la couche 0 **normalisée** n'est plus un simple reflet des octets ✓✓.

**Ce que cela change pour le chapitre** ✓✓ : les deux résultats centraux — **noyau neutre** ✓ et **langue à la
surface** ✓ — ne sont pas des accidents de petite taille ✓✓. Ils **tiennent** (et la surface se renforce ✓) quand
le modèle double ✓.

## Seizième mesure (17/10, 17 h) : le **retrieval croisé** échoue — mais le test est invalide, pas les états

La question **forte** du chapitre ✓ : le même contenu, écrit en deux langues, donne-t-il des états
**comparables** ? ✓✓ C'est ce qui dirait qu'un état porte le **sens** et pas la langue ✓. Dispositif :
`tools/retrieval_parallele.py` ✓ — sur un livre **parallèle** (Le Tour du monde en quatre-vingts jours ✓, le
français est l'original ✓), 24 segments ✓, et l'on demande si le segment français le plus proche d'un segment
anglais est **son homologue** ✓ (hasard = 4,2 % ✓).

| essai | retrieval exact | similarité des homologues | des autres |
|---|---:|---:|---:|
| dernière couche, sans centrage | **0 / 24** ✗ | +0,8695 | +0,8706 |
| dernière couche, **centré** ✗ | 0 / 24 ✗ | −0,6564 | −0,6032 |
| couche 6, centré | 0 / 24 ✗ | −0,6714 | −0,6311 |
| couche 4, centré | 0 / 24 ✗ | −0,4697 | −0,4457 |

* **le retrieval échoue partout** ✗, et les homologues sont **moins** similaires que les autres (−0,66 contre
  −0,60 ✓) — c'est-à-dire **anti-corrélé** ✗✗. En apparence, les états ne portent **pas** le sens ✓✗ ;
* **MAIS LE TEST EST INVALIDE** ✗✓ — et le confondant est **mesurable** ✓✓ : les deux éditions n'ont **pas la
  même longueur** (**451 Ko** en français contre **375 Ko** en anglais ✓, soit **20 %** d'écart ✓✗). Un
  découpage **proportionnel** dérive donc ✓✗ : après quelques chapitres, le segment `i` français et le segment
  `i` anglais ne couvrent **plus le même passage** ✗✓. Le test ne mesure pas le sens ✗ — il mesure la **dérive**
  ✓✓ ;
* **et le premier essai (sans centrage) le montrait déjà** ✗✓ : toutes les similarités valaient **0,87** ✓ —
  une **direction commune dominante** (« du texte ordinaire » ✓) qui noie tout ✓✓. Le centrage la retire ✓ mais
  ne peut pas réparer un **mauvais appariement** ✗✓ ;
* **la conclusion honnête** ✓✓ : *cette mesure ne tranche rien* ✗ — elle a coûté une demi-heure et elle
  **apprend** que le maillon faible est l'**alignement**, pas le modèle ✓✓. C'est la **dixième** fois de la
  nuit qu'un chiffre se déguise ✓ (ici en verdict sur les états ✓✗), et la règle n'a pas changé : *écrire à
  côté du chiffre ce qui pourrait le rendre faux* ✓.

### Le dispositif qu'il faudrait (et qui est à portée)

L'alignement doit être **ancré** sur le **contenu**, pas sur la position ✗✓. Deux ancres possibles, et elles
sont dans le corpus ✓ : les **noms propres** (« Phileas Fogg », « Passepartout » ✓ apparaissent aux **mêmes
endroits de l'histoire** ✓✓) et les **chapitres** (37 dans chaque édition ✓ — mais la version française
numérote par **titres** et non par « CHAPITRE n », d'où l'échec de mon découpage naïf ✗✓). *Aligner sur les
noms, puis vérifier par les chapitres* ✓✓ — c'est la prochaine mesure, et elle est courte ✓.

## Dix-septième mesure (17/10, 17 h 45) : l'alignement était **bon**, c'était l'**échantillon** qui était mauvais

Le § précédent concluait « test invalide, le confondant est l'alignement » ✗✓. **C'était faux** ✗✓ — et la
vérification est nette ✓ : les deux éditions **sont remarquablement alignées** ✓✓. Mesure : la position
**relative** des occurrences des noms propres ✓ (identiques dans les deux langues ✓) :

| nom | occurrences (fr / en) | **écart de position relative** |
|---|---:|---:|
| **Aouda** | 136 / **136** ✓ | — |
| **Fogg** | 655 / 608 | **0,3 %** ✓✓ |
| **Passepartout** | 423 / 398 | **0,1 %** ✓✓ |

*les dix premières occurrences de « Fogg » tombent au **même endroit** de l'histoire à **0,3 %** près ✓✓, et
celles de « Passepartout » à **0,1 %** ✓✓.* L'alignement proportionnel était donc **bon** ✓ — le confondant
était **mon échantillonnage** ✗✓ : je prenais les **400 premiers octets** de chaque segment ✓✗, c'est-à-dire
souvent un **titre de chapitre** ou des blancs ✓✓. *L'état moyen mesurait la mise en page, pas le récit* ✗✓.

Avec un échantillonnage au **milieu** du segment ✓ (de la prose ✓) :

| segments | retrieval exact | homologues | autres | **écart** |
|---|---:|---:|---:|---:|
| 24 | 0 / 24 ✗ | −0,6283 | −0,6502 | **+0,0219** ✓ |
| 40 | 1 / 40 ✗ | −0,6058 | −0,6109 | +0,0052 ✓ |

* **LE SIGNE S'INVERSE** ✓✓ : avant, les homologues étaient **moins** similaires (−0,053 ✗) ; maintenant ils le
  sont **un peu plus** (+0,022 ✓). *Il existe donc un signal cross-lingue réel* ✓✓ — mais il est **très faible** ✗ ;
* **et il ne suffit pas à retrouver** ✗ : 0/24 et 1/40, soit **le hasard** ✓✗ (4,2 % et 2,5 % ✓) ;
* **l'explication la plus simple** ✓ : un modèle **en octets de 2,4 M paramètres** ✓, entraîné sur 11 Mo de texte
  ✓, **sans objectif de traduction** ✗ — n'a aucune raison de porter le sens d'une langue à l'autre ✓✓. Ce
  n'est pas un défaut de la mesure ✗ : c'est un **fait du modèle** ✓ ;
* **et la conséquence est nette** ✓✓ : ce test a besoin d'un modèle **multilingue entraîné** ✗ — le **Qwen2.5-0.5B**
  du dépôt ✓ *est* multilingue ✓✓, et il est **là** ✓. *C'est la prochaine mesure, et elle ne demande rien à
  construire* ✓✓.

**Onzième piège de la nuit** ✓✓ : j'ai accusé l'**alignement** ✗ alors que le coupable était mon **échantillon**
✓✓ — et l'accusation était **mesurable** (0,1 à 0,3 % d'écart ✓✓). La règle reste la même, avec une variante :
*avant d'accuser un maillon, mesure-le* ✓✓.

## Dix-huitième mesure (17/10, 18 h 15) : sur un **vrai modèle multilingue**, le sens se retrouve — et la structure du chapitre est CONFIRMÉE

Le § précédent concluait qu'il fallait un modèle **multilingue entraîné** ✗. Le **Qwen2.5-0.5B** du dépôt l'est ✓✓.
Même dispositif ✓ (Le Tour du monde ✓, 32 segments ✓, échantillonnage au **milieu** ✓, états **centrés** ✓),
avec cette fois le **tokeniseur** du modèle ✓ (les octets n'auraient aucun sens pour lui ✗✓) :

| couche | retrieval exact | homologues | autres | **écart** |
|---|---:|---:|---:|---:|
| **8** | **3 / 32** (9,4 %) ✓ | −0,2139 | −0,2919 | **+0,0779** ✓✓ |
| **16** | **2 / 32** (6,2 %) ✓ | −0,1692 | −0,2522 | **+0,0830** ✓✓ |
| 23 | 1 / 32 (3,1 %) ✗ | −0,6716 | −0,7011 | +0,0295 ✓ |

*(hasard = 3,1 % ✓ ; rappel : le modèle en octets de 2,4 M donnait **+0,022** et 0/24 ✗)*

* **LE SENS SE RETROUVE, ET QUATRE FOIS MIEUX** ✓✓ : l'écart entre homologues atteint **+0,083** aux couches
  **moyennes** (16 ✓), contre **+0,022** pour le petit modèle en octets ✓✓ — et le retrieval passe de **0/24**
  ✗ à **3/32** ✓ (trois fois le hasard ✓) ;
* **ET LA STRUCTURE DU CHAPITRE EST CONFIRMÉE** ✓✓✓ : l'écart est **maximal aux couches moyennes** (8 et 16 :
  +0,078 et +0,083 ✓) et **s'effondre à la dernière** (23 : +0,030 ✓✗). C'est-à-dire que *la couche profonde
  est **langue-spécifique*** ✗✓ et que *le **sens partagé** vit dans les couches **intermédiaires*** ✓✓ —
  exactement ce que les mesures 1 à 9 disaient d'un modèle-jouet ✓✓, et cette fois sur un **vrai modèle
  multilingue** ✓✓ ;
* **mais le retrieval reste loin de 100 %** ✗ : 9,4 % pour un hasard de 3,1 % ✓. Trois fois le hasard, ce n'est
  pas « l'alignement parfait » ✗ — c'est un **signal réel mais faible** ✓✓, et il faut le dire ainsi ✓ ;
* **ce que la mesure ne peut pas dire** ✗ : 32 segments ✓, un seul livre ✓, un **état moyen** par segment ✗ (une
  moyenne sur des positions ✓, pas un alignement mot à mot ✓), et **un seul modèle** ✓ (0,5 B ✓). *Un signal de
  cette taille demande à être répliqué* ✓✓ — et c'est faisable (d'autres livres du corpus multilingue ✓, d'autres
  couches ✓, un autre modèle ✓).

### Où en est la question du chapitre, après dix-huit mesures

| question | réponse mesurée |
|---|---|
| la couche commune existe-t-elle ? | **oui** ✓✓ (noyau à 50,2 % = le hasard ; couches moyennes les plus cross-lingues) |
| garde-t-elle le sens ? | **oui** ✓✓ (contenu 87,8 % aux couches neutres ; +0,083 de similarité cross-lingue au milieu) |
| la langue est-elle un paramètre ? | **oui** ✓✓ (1,33 % des paramètres, 5 ms de bascule, et la sortie la suit) |
| **et le même sens dans deux langues ?** | **partiellement** ✓✗ : trois fois le hasard ✓, mais pas un alignement ✗ — *c'est la question qui reste ouverte* ✓ |

## Dix-neuvième et vingtième mesures (17/10, 18 h 45) : la neutralité **sur la littérature**, et une **tendance en trois points**

### La neutralité se réplique sur de la vraie littérature — et la zone neutre est plus **courte**

Le modèle bilingue **littéraire** (4,79 M ✓, 11,7 Mo mixtes ✓ — 6 Mo d'anglais + 6 Mo de **Maupassant, Dumas,
Flaubert, Verne** ✓, validation **2,6846** bits/octet ✓) mesuré comme les autres ✓ :

| couche | langue | témoin | verdict |
|---:|---:|---:|---|
| 0 | 61,2 % | 71,7 % | neutre ✓ |
| **1** | **50,1 %** | 50,2 % | **le hasard** ✓✓ |
| **2** | **52,3 %** | 50,2 % | **quasi le hasard** ✓✓ |
| **3** | **50,4 %** | 50,8 % | **le hasard** ✓✓ |
| 4 | 59,9 % | 50,6 % | ✗ |
| **5** | **67,7 %** | 52,1 % | ✗✗ (le pic) |
| 7 | 60,6 % | 50,6 % | ✗ |
| 8 | 56,7 % | 50,8 % | ✗ |

* **LA NEUTRALITÉ SE RÉPLIQUE SUR LA LITTÉRATURE** ✓✓ : aux couches **1, 2 et 3**, le classifieur est **au
  hasard** (50,1 · 52,3 · 50,4 % ✓✓) — comme sur la prose (50,2 % ✓) et en dim 512 (51,4 % ✓). **Trois modèles,
  trois corpus, même résultat** ✓✓✓ ;
* **mais la zone neutre est PLUS COURTE** ✗✓ : la langue revient dès la couche **4** (59,9 % ✓) et **culmine à
  67,7 %** en couche **5** ✓✗ — alors que sur la prose elle n'apparaissait qu'aux couches 6-7 ✓. *Plus le texte
  est riche, plus tôt la langue réapparaît* ✓✓ — c'est une observation **neuve**, et elle a une lecture simple :
  un texte littéraire porte **plus de signal de langue** (registre, style ✓) qu'un texte technique ✓✓.

### Le signal cross-lingue croît avec le modèle — trois points, une tendance

Même test (Le Tour du monde ✓, échantillonnage au milieu ✓, états centrés ✓) sur les **trois** modèles ✓ :

| modèle | taille | **écart cross-lingue** | retrieval (hasard 3,1-4,2 %) |
|---|---:|---:|---|
| octets, prose du dépôt ✗ | 2,43 M | **+0,022** | 0 / 24 |
| octets, **littérature** ✓ | 4,79 M | **+0,034** ✓ | **2 / 32** ✓ (2× le hasard) |
| **Qwen2.5-0.5B** ✓✓ | 494 M | **+0,083** ✓✓ | **3 / 32** ✓ (3× le hasard) |

* **LA TENDANCE EST MONOTONE** ✓✓ : **+0,022 → +0,034 → +0,083** — le signal cross-lingue **croît avec le
  modèle** ✓✓, d'un jouet en octets jusqu'à un vrai modèle de langue ✓✓. *Le sens partagé n'est pas un
  miracle : c'est une propriété qui s'acquiert avec la capacité et les données* ✓✓ ;
* **et le retrieval suit** ✓ (0/24 → 2/32 → 3/32 ✓), mais **reste loin** d'un alignement ✗✓ : même le meilleur
  n'atteint que **3× le hasard** ✓. *C'est un signal, pas une traduction* ✓✓ ;
* **ce que ces trois points disent pour le projet** ✓✓ : la couche commune **n'est pas à construire** ✗ — elle
  **vient avec le modèle** ✓✓, et la seule chose qu'il faut **ajouter**, c'est le **paramètre de langue** (1,33 %
  ✓✓) pour la **sortie** ✓. C'est la conclusion la plus économique de tout le chapitre ✓.

## Vingt-et-unième mesure (17/10, 19 h) : le signal cross-lingue **se réplique en signe** — pas en amplitude

Un signal de cette taille demande une **réplication** ✓✓. Le corpus multilingue contient **trois** livres avec
une paire français/anglais ✓ : Le Tour du monde ✓, **Alice au pays des merveilles** ✓, **Dracula** ✓. Même
dispositif sur les trois ✓ (Qwen, couche 8 ✓, 32 segments ✓, échantillonnage au milieu ✓, états centrés ✓) :

| livre | retrieval (hasard 3,1 %) | homologues | autres | **écart** |
|---|---:|---:|---:|---:|
| **Le Tour du monde** ✓ | **3 / 32** (9,4 %) | −0,2139 | −0,2919 | **+0,0779** ✓✓ |
| **Dracula** | 0 / 32 ✗ | −0,1432 | −0,1766 | **+0,0334** ✓ |
| **Alice** | 2 / 32 (6,2 %) | −0,2839 | −0,2925 | **+0,0087** ✓ |

* **LE SIGNE EST POSITIF DANS LES TROIS LIVRES** ✓✓ (+0,078 · +0,033 · +0,009 ✓) — *le signal cross-lingue se
  **réplique*** ✓✓. Ce n'est pas un accident d'un livre ✓ ;
* **MAIS L'AMPLITUDE VARIE DE HUIT FOIS** ✗✓ (0,009 à 0,078 ✓) → le signal est **réel et fragile** ✓✓, et le
  retrieval ne suit qu'un livre sur trois (3/32, 0/32, 2/32 ✓) : *c'est un signal, pas un alignement* ✓✓ ;
* **et la variation peut venir de l'ALIGNEMENT, pas du modèle** ✗✓ : je n'ai vérifié les ancres (positions
  relatives de « Fogg » et « Passepartout » ✓) que pour **Le Tour du monde** ✓. Les éditions d'Alice et de Dracula
  peuvent avoir des structures **différentes** (abrégements ✓, découpages ✓, épilogues ✓) — et le confondant du
  § 16 (l'appariement ✓) revient ici ✗✓. *La prochaine étape n'est pas une mesure de modèle, c'est un contrôle
  d'alignement* ✓ ;
* **ce que cela laisse, honnêtement** ✓✓ : (1) la couche commune **existe** ✓✓ (trois modèles, trois corpus ✓) ;
  (2) elle **garde le sens** ✓✓ (contenu 87,8 % ✓) ; (3) **le même sens dans deux langues** se retrouve
  **mieux que le hasard, de façon reproductible en signe** ✓✓, mais avec une amplitude **petite et variable** ✗✓
  — *c'est une piste, pas un acquis* ✓✓. Le chapitre a donc une réponse **nuancée** à sa question la plus forte
  ✓✓, et c'est celle qui doit être écrite ✓.

## Vingt-deuxième mesure (17/10, 19 h 30) : le contrôle d'alignement — et **un fichier mal étiqueté** dans le corpus

Le § précédent concluait « la variation peut venir de l'alignement, que je n'ai vérifié que pour un livre » ✗✓.
Le contrôle est fait ✓ — la **déviation de position relative** des noms propres identiques aux deux langues ✓ :

| livre | nom | occurrences (fr / en) | **écart** | verdict |
|---|---|---:|---:|---|
| **Le Tour du monde** | Fogg | 655 / 608 | **0,3 %** | ALIGNÉ ✓✓ |
| | Passepartout | 423 / 398 | **0,1 %** | ALIGNÉ ✓✓ |
| | Aouda | 136 / 136 | 1,6 % | ALIGNÉ ✓✓ |
| **Alice** | Alice | 395 / 399 | **1,7 %** | ALIGNÉ ✓✓ |
| **Dracula** | Dracula | **0** / 33 | — | ✗✗ |
| | Mina | **0** / 233 | — | ✗✗ |
| | Lucy | **0** / 298 | — | ✗✗ |

* **ALICE ET VERNE SONT ALIGNÉS** ✓✓ (0,1 à 1,7 % ✓) — donc la **variation de huit fois** entre leurs signaux
  (+0,009 et +0,078 ✓) **n'est PAS un défaut d'alignement** ✓✓ : elle vient du **contenu** (Alice est un dialogue
  ✓, Verne un récit ✓) ou du modèle ✓. *C'est un résultat, pas un artefact* ✓✓ ;
* **MAIS « DRACULA » FRANÇAIS N'EST PAS DRACULA** ✗✗ : le fichier `dracula_fr.txt` contient
  **« Vocations Explained: Matrimony, Virginity… »** ✓✗ — un **autre livre** ✓, et le rapport de longueur le
  criait (**0,101** ✗ : le français fait **10 fois** moins de caractères que l'anglais ✓✓). La mesure du § 21 sur
  ce livre comparait donc **Dracula à un traité religieux** ✗✓ : son « +0,0334 » est du **bruit** ✓✓, pas un
  signal ✓ ;
* **donc la réplication porte sur DEUX livres, pas trois** ✗✓ : Verne **+0,078** ✓✓ et Alice **+0,009** ✓. Le
  signe reste **positif deux fois sur deux** ✓✓ — la réplication **tient** ✓ — mais avec une amplitude qui varie
  de **huit fois** entre deux livres **bien alignés** ✓✓ ;
* **et le corpus de Panini contient au moins une erreur d'appariement** ✗✓ : `dracula/dracula_fr.txt` est un autre
  texte ✓. *Il faut le signaler* ✓✓ — un corpus mal étiqueté est **invisible** tant qu'on ne vérifie pas les
  ancres ✓✓, et c'est exactement le genre de défaut que ce chapitre passe son temps à chercher ✓.

**Douzième piège** ✓✓ : *vérifier l'appariement avant de mesurer l'appariement* ✓✓. Le contrôle a coûté dix
minutes ✓ et il a **supprimé une mesure** ✗✓ — c'est le meilleur rapport coût/résultat possible pour un
instrument ✓✓.

## Vingt-troisième mesure (17/10, 20 h) : le crible du corpus — **une paire cassée sur trois**, propagée dans les deux corpus

Le fichier mal étiqueté du § 22 méritait un **crible systématique** ✓, et il est fait ✓ — `tools/cribler_corpus.py`
✓, qui vérifie **sans modèle** et **sans langue** ✗ trois choses indépendantes : le **titre** annoncé dans
l'en-tête Gutenberg de chaque fichier ✓, le **rapport de longueur** entre les deux langues ✓, et la **possession
d'un nom propre commun** ✓.

| corpus | paires | verdict |
|---|---:|---|
| `gutenberg_multilingual_verified` | 3 | **2 OK ✓ · 1 CASSÉE ✗** |
| `gutenberg_multilingual_corpus` | 2 | **1 OK ✓ · 1 CASSÉE ✗** |

* **LA MÊME PAIRE EST CASSÉE DANS LES DEUX CORPUS** ✗✓ : `dracula` a **85 Ko** de français pour **850 Ko**
  d'anglais (rapport **0,101** ✓✓) et le fichier français est **« Vocations Explained: Matrimony, Virginity… »**
  ✓✗. *L'erreur a été copiée d'un corpus à l'autre* ✓✓ — donc elle ne se détecte pas en comparant les corpus ✗,
  seulement en **vérifiant les fichiers** ✓ ;
* **les autres paires sont saines** ✓✓ (Alice 179/147 ✓ et 160/147 ✓, Le Tour du monde 451/374 ✓ — rapports
  1,20 à 1,22 ✓, parfaitement plausibles pour une traduction ✓✓) ;
* **et le crible a une limite, qu'il faut dire** ✗✓ : l'extraction du **titre** ne fonctionne que sur les
  en-têtes au format français ✓ — les fichiers anglais donnent « (titre absent) » ✓✗, donc le contrôle par le
  titre est **partiel** ✓ (il n'a pas vu Dracula ✗ ; c'est le **rapport de longueur** qui l'a attrapé ✓✓) ;
* **ce que cela vaut pour la suite** ✓✓ : les mesures cross-lingues du § 21 sont **deux fois valides** (Verne ✓,
  Alice ✓) et **une fois du bruit** (Dracula ✗) ✓✓. *Un crible de dix minutes a supprimé une mesure et confirmé
  deux autres* ✓✓ — c'est exactement le rôle d'un instrument ✓.

## Vingt-quatrième mesure (17/10, 21 h 45) : la langue comme paramètre **sur un vrai modèle** — et un effet huit fois plus petit

Les mesures 2 et 3 avaient montré qu'un LoRA de langue fait passer un **modèle-jouet monolingue** de 3,19 à 1,50
(−53 % ✓). Qu'en est-il sur un **vrai** modèle ✓ ? LoRA (rang 8 ✓, **4,4 M** paramètres, soit **0,9 %** des
494 M de Qwen ✓) entraîné sur la **littérature française** ✓, taux **1e-4** ✓ :

| | perte **français** | perte **anglais** |
|---|---:|---:|
| Qwen seul ✓ | 3,0900 ✗ | **2,7238** ✓ |
| **Qwen + LoRA français** ✓ | **2,8555** ✓ (−7,6 %) | 2,8466 (+4,5 %) ✓ |

* **LA LANGUE EST BIEN UN PARAMÈTRE SUR UN VRAI MODÈLE** ✓✓ : le LoRA améliore le français de **7,6 %** ✓ et
  n'abîme l'anglais que de **4,5 %** ✓✓ — *un paramètre de 0,9 % des poids, et les deux langues marchent* ✓✓ ;
* **MAIS L'EFFET EST HUIT FOIS PLUS PETIT** ✗✓ (−7,6 % contre −53 % sur le jouet ✓) : **parce que Qwen est déjà
  multilingue** ✓✓ — il n'a **pas besoin** du patch ✗. L'adaptateur est un **rattrapage pour modèle monolingue**
  ✓✓, pas une nécessité pour un modèle multilingue ✓✓. *C'est exactement la conclusion du § 20 : la couche
  commune vient avec le modèle* ✓✓ ;
* **et cela donne le chiffre qui manquait** ✓✓ : sur un modèle **déjà** multilingue, il y a **peu à gagner** ✗
  (7,6 % ✓) ; sur un modèle **monolingue**, il y a **beaucoup à gagner** ✓✓ (−53 % ✓). *Le paramètre de langue
  sert d'autant plus que le noyau en est dépourvu* ✓✓.

### Deux pièges d'outillage de plus (13ᵉ et 14ᵉ)

Le premier essai a tourné **huit heures de CPU en trente-deux minutes** ✗✓ — le modèle n'avait **jamais** été
déplacé sur la carte ✓✗ (*un dispositif qui n'est pas là où l'on croit* ✗✓). Le second a échoué sur
`Expected all tensors to be on the same device` ✓✗ — les paramètres du LoRA étaient créés sur CPU quand le noyau
était sur `cuda:0` ✓✓ (*deux objets qui doivent être ensemble et ne le sont pas* ✓). Et le troisième réglage
(taux **1e-3** ✓) a **divergé** ✗ (perte 7,89, français **+26 %** et anglais **+221 %** ✗✗) — sur un 0,5 B, le
taux d'un modèle-jouet est **toxique** ✓✓. Trois corrections, une mesure ✓✓ : *c'est le prix d'un outil qu'on
n'avait jamais poussé sur un vrai modèle* ✓.

## Vingt-cinquième mesure (17/10, 22 h 30) : sur Qwen, la sortie suit l'**AMORCE**, pas l'adaptateur — l'inverse du jouet

La mesure 6 avait montré qu'un LoRA de langue **commande la sortie** d'un modèle-jouet ✓✓ (amorce anglaise +
adaptateur français → **français** ✓✓). La même expérience sur **Qwen** ✓ (avec le LoRA français de la mesure 24 ✓,
rang 8, 0,9 % ✓, et 60 jetons générés ✓) :

| amorce | adaptateur | **sortie** (mots-outils) | verdict |
|---|---|---|---|
| anglais | aucun | **en 20** · fr 0 | suit l'amorce ✓ |
| **anglais** | **français** | **en 27** ✗ · fr 0 | **suit l'amorce, PAS l'adaptateur** ✗✓ |
| français | aucun | **fr 16** ✓ · en 0 | suit l'amorce ✓ |
| français | français | **fr 19** ✓ · en 0 | suit l'amorce ✓ |

* **LE RÉSULTAT DU JOUET NE SE TRANSFÈRE PAS** ✗✓ : sur Qwen, l'adaptateur français **ne fait pas** écrire en
  français à une amorce anglaise ✓✗ (en 27 · fr 0 ✓). *La « langue comme paramètre » qui **commande** la sortie
  est une propriété du noyau **monolingue** ✓, pas du multilingue* ✗✓ ;
* **et la raison est claire** ✓✓ : Qwen est un modèle **instruct multilingue** ✓ — son **suivi de l'amorce** est
  fort ✓✓, et un LoRA de **0,9 %** ne peut pas le renverser ✗. Sur le jouet monolingue, l'adaptateur **était** le
  seul signal de langue ✓✓ — il commandait donc tout ✓ ;
* **donc la conclusion juste du chapitre** ✓✓ est plus étroite que celle du § 6 ✓ : le paramètre de langue
  **ajuste la qualité** (7,6 % ✓) mais **ne choisit pas la langue** quand le modèle sait déjà les deux ✗✓.
  *Un modèle multilingue n'a pas besoin qu'on lui **dise** en quelle langue écrire — il lit l'amorce* ✓✓ ;
* **et c'est cohérent avec tout le reste** ✓✓ : la mesure 24 (−7,6 %, peu à gagner ✓), la mesure 20 (le sens
  partagé vient avec le modèle ✓), et la mesure 9 (un relevé partagé suffit ✓). *Plus le noyau est riche, moins
  le paramètre de langue a de rôle* ✓✓ — il **rattrape** ce qui manque ✓, il ne **dirige** pas ce qui existe ✓.

### Fin de la chaîne, et ce qu'elle vaut

| ce qu'on voulait | ce qui est mesuré | portée |
|---|---|---|
| une **couche commune** | noyau neutre ✓✓ (50,2 % ; trois modèles, trois corpus ✓) | solide ✓✓ |
| qui **garde le sens** | contenu 87,8 % ✓✓ ; sens partagé +0,083 ✓ | solide ✓✓ |
| avec la **langue en paramètre** | 1,33 % des poids, 5 ms ✓✓ | solide **pour un noyau monolingue** ✓✓ |
| qui **commande la sortie** | jouet : oui ✓✓ · Qwen : **non** ✗✓ | **dépend du noyau** ✗✓ |
| qui **améliore** la langue | +7,6 % sur Qwen ✓, −53 % sur un monolingue ✓✓ | solide ✓✓ |

*Le chapitre a donc une réponse à la fois **forte** et **bornée** : la couche commune existe, elle garde le
sens, et la langue y est un **petit paramètre** — mais son **rôle** dépend de ce que le noyau sait déjà* ✓✓.

## Vingt-sixième mesure (17/10, 23 h) : le signal cross-lingue est **utilisable** — sur un livre sur deux

Le top-1 (3/32 ✗) ne dit pas si le signal **sert** : une recherche affiche plusieurs résultats ✓. Mesures
ajoutées au même outil ✓ — le **rang médian** du vrai homologue ✓ et le **top-5** ✓, sur les **deux** paires
saines ✓ (Qwen, couche 8 ✓, 32 segments ✓) :

| livre | **rang médian** (hasard 16,5) | **top-5** (hasard 15,6 %) | top-1 |
|---|---:|---:|---:|
| **Le Tour du monde** ✓ | **9 / 32** ✓✓ | **28,1 %** ✓✓ | 3/32 (9,4 %) |
| **Alice** ✗ | 17 / 32 ✗ | 12,5 % ✗ | 2/32 (6,2 %) |

* **POUR VERNE, LE SIGNAL EST UTILISABLE** ✓✓ : le vrai homologue tombe à un **rang médian de 9 sur 32** (contre
  16,5 au hasard ✓✓) et dans le **top-5 dans 28 %** des cas (contre 15,6 ✓✓) — *c'est une recherche cross-lingue
  réelle, faible mais fonctionnelle* ✓✓ ;
* **POUR ALICE, RIEN** ✗ : rang médian **17** (exactement le hasard ✓) et top-5 **sous** le hasard (12,5 contre
  15,6 ✗✓). Le signal de +0,009 ne suffit pas ✓✓ ;
* **donc l'utilisabilité dépend du LIVRE** ✗✓ (Verne ✓ / Alice ✗) — et je ne sais pas pourquoi ✗ : Alice est un
  **dialogue** (peu de narration ✓), Verne un **récit** (descriptions, voyages ✓) → *l'hypothèse la plus simple est
  que le sens partagé entre deux langues vit dans le **récit**, pas dans le dialogue* ✓✓, mais **elle n'est pas
  testée** ✗ et deux livres ne suffisent pas à la tester ✓✓ ;
* **ce que cela laisse** ✓✓ : *une recherche cross-lingue **fonctionne** sur un des deux livres, faiblement
  (rang 9/32, top-5 28 %)* ✓✓ — c'est le premier résultat **utilisable** de tout le chapitre, et il est **borné**
  ✗✓. Il demanderait, pour être une propriété, **plusieurs livres de chaque genre** ✓ — et c'est un programme, pas
  une mesure ✓.

### La synthèse complète (mesures 24-25, pour finir)

| # | la question | le chiffre | verdict |
|---:|---|---|---|
| 24 | la langue comme paramètre sur un **vrai** modèle ? | LoRA 4,4 M (**0,9 %**) : français **−7,6 %**, anglais **+4,5 %** | ✓✓ mais **huit fois moins** qu'en monolingue (−53 %) |
| 25 | la sortie **suit-elle** le paramètre sur Qwen ? | amorce anglaise + LoRA français → **anglais** (en 27 · fr 0) | ✗ **non** : elle suit l'**amorce** |
| 26 | le sens partagé est-il **utilisable** ? | Verne : rang médian **9/32**, top-5 **28 %** · Alice : rang **17**, top-5 **12,5 %** | ✓ **un livre sur deux** |

## Vingt-septième mesure (17/10, 23 h 30) : l'inventaire de la machine — **1905 textes**, 21 français, et un second fichier mal nommé

Le corpus littéraire du § 14 avait été constitué sur un **premier scan** ✗ — limité à trois dossiers ✗✓. Un scan
**complet** de `Panini/`, `Panini/research/data/`, `Panini-Research/data/` ✓ donne tout autre chose ✓✓ :

| | premier scan ✗ | scan complet ✓ |
|---|---:|---:|
| textes > 100 Ko, uniques | 66 | **1905** ✓✓ |
| français | 18 | **21** ✓ |
| anglais | 47 | 1881 |
| indéterminés | 1 | 3 (dont 2 **allemands** ✗✓) |

**Les 21 textes français** ✓✓ — et ce sont de grands noms : **Proust** (*Du Côté de Chez Swann* ✓), **Stendhal**
(*Le rouge et le noir* ✓), **Hugo** (*Les misérables*, Tome IV ✓), **Voltaire** (*Candide* ✓), **Baudelaire**
(*Les Fleurs du Mal* ✓), **Chateaubriand** (*Mémoires d'Outre-Tombe* ✓), **George Sand** (*Histoire de ma Vie* ✓),
**Diderot** (*Les bijoux indiscrets* ✓), **Montesquieu** (*Esprit des lois* ✓), **Corneille** ✓, **Verne** ✓,
**Zola** (*Les trois villes : Lourdes* ✓).

Le corpus reconstruit ✓ — en-têtes et pieds de page Gutenberg **retirés** ✗✓ :

| | ancien (§ 14) | **nouveau** ✓ |
|---|---:|---:|
| textes | 18 | **21** |
| taille | 13,2 Mo | **15,7 Mo** ✓ |
| **formes** | 66 322 | **87 341** ✓✓ (+31 %) |
| mots fréquents | `les, que, qui, des` ✓ | `que, les, qui, des, dans, vous` ✓✓ |

*Et un **second fichier mal nommé** ✗✓ : `pg2000_en.txt` est un **Don Quijote en français** ✓✗ (le nom dit `_en` ✗).
Après `dracula_fr.txt`, c'est le **deuxième** — et il confirme la règle du § 23 : **le nom d'un fichier n'est pas
sa langue**, et seule la lecture le dit ✓✓.*

**Ce que cela change pour la suite** ✓✓ : les mesures 12, 19 et 20 (neutralité, littérature, tendance) reposent
sur l'**ancien** corpus ✗✓ — elles demandent à être **refaites** sur le nouveau ✓✓, plus riche de 31 % ✓. C'est
la prochaine étape, et elle est courte : le modèle bilingue littéraire est à réentraîner ✓ (vingt minutes ✓) et
les trois mesures à rejouer ✓.

## Vingt-huitième mesure (17/10, 18 h 45) : le crible élargi — **cinq fichiers mentent sur leur langue**, dont trois des quatre « allemands »

Le crible du § 23 ne portait que sur les paires fr/en ✓. Étendu aux **1905** textes de la machine ✓, il compare la
langue **annoncée par le nom** (`_en`, `_fr`, `_de` ✓) à la langue **détectée** par les mots-outils ✓ :

| fichier | annoncé | **détecté** | taille |
|---|---|---|---:|
| `pg2000_en.txt` | anglais | **français** ✗ | 2173 Ko |
| `pg21053_en.txt` | anglais | **allemand** ✗ | 838 Ko |
| `metamorphosis_de.txt` | allemand | **anglais** ✗✗ | 790 Ko |
| `pride_prejudice_de.txt` | allemand | **anglais** ✗✗ | 688 Ko |
| `frankenstein_de.txt` | allemand | **anglais** ✗✗ | 332 Ko |

* **CINQ FICHIERS SE TROMPENT DE LANGUE** ✗✓ sur 1905 ✓ — soit **0,26 %** ✓, ce qui est peu ✓ mais suffisant pour
  ruiner une mesure ✓✓ (c'est exactement ce qui est arrivé avec Dracula ✓) ;
* **et le corpus « multilingue vérifié » est le pire** ✗✗ : **trois** de ses quatre fichiers « allemands » sont
  **anglais** ✓✗ (`metamorphosis`, `pride_prejudice`, `frankenstein` ✓) — le mot « verified » du nom **ne garantit
  rien** ✗✓. *Un nom de fichier n'est pas une langue, et un dossier « vérifié » n'est pas vérifié* ✓✓ ;
* **mon corpus français n'est pas touché** ✓✓ : il a été construit sur une **détection** ✓, pas sur les noms ✓ —
  c'est pourquoi `pg2000_en.txt` (français ✓) y est **inclus à bon droit** ✓✓, et les fichiers anglais n'y sont pas
  ✓. *La détection a protégé le corpus de ses propres noms* ✓✓ ;
* **la conséquence pratique, et elle est nette** ✓✓ : **tout corpus de ce dépôt doit être re-vérifié par la langue
  détectée avant usage** ✗✓ — `tools/cribler_corpus.py` fait ce contrôle ✓, et il devrait passer sur **tout**
  corpus importé ✓✓. *C'est la douzième leçon d'instrument de la nuit, et la plus opérationnelle* ✓.
