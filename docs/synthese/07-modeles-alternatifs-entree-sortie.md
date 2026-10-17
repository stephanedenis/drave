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
