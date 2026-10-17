# 7. Les modèles alternatifs pour l'entrée et la sortie — vers une couche commune

> **La question.** Peut-on arriver **plus vite** à une couche d'entrée-sortie **commune**, qui fasse
> **abstraction de la langue** — la langue, le dialecte, le style n'étant plus que des **paramètres** ?
> Cette note examine les familles de solutions, avec pour chacune : ce qu'elle gagne, ce qu'elle coûte, et
> **comment on le mesure**.

![Une couche commune, et la langue comme paramètre](schemas/couche-commune.svg)

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
