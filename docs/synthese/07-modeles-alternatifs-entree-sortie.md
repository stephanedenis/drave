# 7 — Les modèles alternatifs pour l'entrée et la sortie

> **Périmètre** : ce chapitre relève du programme **intelligence** ; la vision est dans [`docs/vision.md`](../vision.md), la roadmap dans [`docs/roadmap.md`](../roadmap.md).

> **Ce que ce chapitre est.** La **théorie** de l'étage entrée-sortie (nom historique : couche commune) : ce qu'il doit être, ce qu'on
> en sait, ce qui reste à prouver. Les **mesures** (67, avec leurs erratums et leurs pièges) sont dans
> [`reports/07-mesures-couche-commune.md`](../../reports/07-mesures-couche-commune.md).

## Le problème

Un modèle qui **lit et écrit** doit traiter **toutes les langues, dialectes et styles** sans que le **sens** qu'il
manipule dépende de la langue de surface. La question du chapitre : *la langue est-elle un **paramètre** de la
surface, et le contenu un **espace commun** ?*

## La représentation neutre n'est pas un jeton

L'architecture a trois pièces : un **module pré-linguistique** (texte → sens), une **représentation sémantique
neutre (RSN)**, et un **module post-linguistique** (sens → texte). La RSN est le **contrat** entre les deux.

**Ce que la RSN est** : une **structure multi-niveaux** — graphémique/phonologique, morphologique, syntaxique,
sémantique, discursif/pragmatique — **indépendante de la langue de surface**, et annotée de son bruit (confiance,
ambiguïtés non résolues, langues probables). Ses éléments sont des **unités de sens**, pas des fragments de chaîne.

**Ce qu'un jeton est** : l'unité de **tokenisation** d'un modèle, un découpage **technique** qui varie selon le
modèle et l'écriture. Il porte le calcul, pas le sens. Écrire « jeton » pour la RSN confondrait le **contrat** (le
sens) avec le **transport** (le tokeniseur) — et ferait croire que l'unité de sens est un fragment de chaîne de
caractères.

**Conséquence pour la mesure** : les métriques par jeton (bits/token, tokens coûteux, perplexité) sont des
**diagnostics d'instrument** ; elles dépendent du tokeniseur et ne sont **pas comparables entre écritures** (mesure
53). La mesure de la couche doit se faire par **unité grammaticale** (morphème, mot, syntagme, proposition, énoncé)
et par **niveau** de la RSN.

**La direction** : à mesure que les modules linguistiques s'approcheront de **grammaires formelles multi-niveaux**
représentant les entrées et les sorties en **compréhension totale**, l'unité de mesure à l'entrée et à la sortie
devra **s'éloigner du jeton traditionnel** : l'unité sera le **constituant grammatical** (et sa structure), pas le
fragment de tokeniseur. Le jeton restera un détail d'implémentation des modèles actuels, **pas l'unité du sens** ni
la cible de la mesure.

## Les cinq familles de solutions

| famille | l'idée | ce qu'elle gagne | ce qu'elle coûte |
|---|---|---|---|
| **A. octets partagés** | un seul vocabulaire (UTF-8) | aucune langue dans l'entrée | séquences plus longues, abstraction de surface |
| **B. plongement partagé + étiquette** | un espace d'embedding, une étiquette de langue | simple, éprouvé (XLM-R, mBERT) | l'étiquette contamine l'état |
| **C. adversarial** | entraîner l'état à cacher la langue | contenu réellement neutre | instable, peut détruire de l'information |
| **D. interlingua** | une représentation sémantique explicite (Mel'čuk) | c'est l'idée visée | il faut la construire |
| **E. adaptateurs par langue** | noyau commun + un petit LoRA par langue | peu de paramètres, efficace | la neutralité du noyau n'est pas garantie |

## Ce qu'on sait (théorie établie par les mesures)

- **la langue est lisible partout** dans l'état d'un modèle entraîné (80 à 100 % dès la couche 1, sur 5 modèles
  d'octets et Qwen) — il n'y a **pas** de « noyau neutre » spontané ;
- **le sens est aligné malgré la langue** : le même article UDHR se retrouve d'une langue à l'autre à **96 %** sur
  les paires bien couvertes, **16 %** sur un échantillon stratifié de 100 langues, et **3,5×** le hasard dans un
  vivier ouvert ;
- **la restitution exacte** (même langue, à l'identique) est **parfaite pour un modèle spécialisé** (85 % de
  fragments exacts) et **s'effondre quand il partage 448 langues** (0,6 %) : la capacité ne se partage pas
  gratuitement ;
- **la hiérarchie des surfaces** : langues **96 %** > dialectes **52-97 %** > styles (traducteurs) **24 %** — et les
  trois sont **lues à 100 %**. *L'étage entrée-sortie n'efface aucune surface : il en aligne le sens.*
- **les paires doivent être du bon REGISTRE et du bon DOMAINE** : les paires **savantes ou sacrées** (Bible,
  encyclopédie) **dégradent** la traduction du pidgin, les paires **quotidiennes et narratives** (interface, contes)
  aident — *le registre et le domaine comptent plus que le **volume** et que la **modernité*** (mesures 95-106).
- **un banc peut mesurer la MÉMOIRE au lieu de la traduction** : sur un texte célèbre (l'UDHR), le modèle **récite**
  la traduction officielle au lieu de traduire ce qu'il lit — et le chrF **ne le voit pas** (77,8 sur l'UDHR contre
  75,7 sur un texte neuf) ✗✗. *Un score de surface ne distingue pas la mémoire de la traduction* : il faut un texte
  que le modèle n'a pas pu voir, et un test qui **change la source** ;
- **la qualité réelle de traducteur** (règlement européen postérieur à la coupure) : **54,7 → 75,7 de chrF** du 0,5
  au 7 B, **courbe lisse et monotone** ; le **littéraire** est le plus dur (47,7-49,8) et la **taille n'y aide
  presque pas** — *le levier est le domaine, pas les paramètres* ;
- **le bruit d'entrée est signalable** (fautes et langues mêlées : détection 100 %, AUC 1,00) **mais pas
  corrigeable** : la correction automatique **empire** le texte 8 fois sur 9, et la correction la plus **fluide**
  est la plus **fausse** ✗✗. *Le miroir doit valider le **sens**, pas la fluidité.*

## Découper par langue (principe MoE) : ce que les mesures autorisent

**La question.** Peut-on alléger l'étage entrée-sortie en découpant le modèle **par langue** (principe
*mixture-of-experts*) et ne charger que le pertinent ? Quatre faits mesurés répondent.

- **La langue est un petit paramètre** : **1,33 %** des poids (32 768 au dernier étage), bascule **5 ms**,
  **530 Ko** (mesures 3 et 7). Un module de langue peut donc être **petit** et **chargé à la demande**.
- **Le partage détruit la restitution** : **85 %** de fragments exacts pour un modèle spécialisé, **4 %** quand il
  partage **10 langues** (mesure 46). *La capacité ne se partage pas gratuitement* : la spécialisation par langue
  (ou par famille) est ce qui restaure la restitution.
- **Mais l'espace sémantique est partagé** : **96 %** de retrieval croisé sur les paires couvertes (mesure 39) ; le
  sens traverse les langues. *Découper le **noyau** détruirait ce qui marche.*
- **Et la couverture est une limite de données** : **+35,8** de marge pour les 13 langues annoncées, **+21,5** pour
  les 10 autres, et **la taille ne comble pas l'écart** (mesures 71-72). Un module par langue n'invente pas la
  donnée qui manque — il l'exploite mieux.

**Ce que cela autorise** : un **noyau partagé** (le sens, 96 %) + des **modules de surface par langue** (entrée et
sortie : embeddings, tête, adaptateurs), **routés par segment** et **chargés à la demande** (5 ms / 530 Ko). C'est
le principe MoE, mais appliqué à la **surface**, pas au noyau.

**Ce que cela n'autorise pas** : des **modèles entièrement séparés** par langue — on perd l'espace partagé, on n'a
pas les données pour les langues peu dotées, et le routage sur texte **court** ou **mêlé** est fragile (mesures 58
et 60) ; ni un **routage par document** (une entrée bilingue existe) : le routeur doit être **par segment**, avec
une **confiance** et un **repli** sur le noyau partagé.

**Le plan d'expérience** : (0) **d'abord un corpus d'entraînement par langue** — les 139 unités du banc sont pour
l'**évaluation**, pas pour l'entraînement (30 articles d'UDHR ou 139 paragraphes d'un règlement ne suffisent pas à
apprendre une langue) ; (1) noyau 3 B gelé + **adaptateur par langue** sur les 10 langues non couvertes, mesuré
sur le banc propre 24 langues ; (2) **adaptateur par famille** contre par langue (le transfert paie-t-il ?) ;
(3) **routeur par segment** (langue détectée + confiance) contre un routage par document, sur du texte mêlé ;
(4) **coût** : experts résidents contre *offload* (VRAM, latence, qualité) ; (5) **restitution** : modules par
langue contre modèle partagé 448 langues, pour répliquer 85 % → 4 %.

## Ce qui reste ouvert (et qui commande la suite)

1. **la qualité de traduction** du module entrée-sortie : le **juridique**, la **presse** et le **littéraire** sont
   mesurés sur des textes non mémorisables ; il reste le **technique**, le **quotidien parlé** et les **langues peu
   dotées** — c'est le juge de paix de l'étage. **Le passage à l'étage 2 exige les 20 langues les plus parlées**
   (Ethnologue 2026) **mesurées sur un texte neuf**, avec un **plafond humain** par écriture (le chrF n'est pas
   comparable entre écritures, 29ᵉ piège) : **aujourd'hui 19/20** (mesures 73-76) ; seul manque le
   **pidgin nigérian** (créole oral sans corpus parallèle post-cutoff) ;
2. **la restitution exacte à l'échelle** : au-delà de 10 langues partagées, elle meurt ; faut-il des modules
   spécialisés par famille, ou un modèle beaucoup plus grand ?
3. **le style** : il est lisible, mais le sens ne le traverse qu'à 24 % — comment l'augmenter sans perdre le style ?

*Tant que ces trois questions ne sont pas tranchées, le module de **pensée abstraite** attend : il ne peut pas être
bâti sur une entrée-sortie qui n'est pas fiable.*

## Le miroir de sortie : pourquoi la sortie est plus fiable que l'entrée

L'étage entrée-sortie n'est pas symétrique ✓✓. **Texte → sens** doit absorber les imperfections du réel (bruit,
orthographes multiples, langues mêlées, coquilles) ; **sens → texte** part d'un sens **propre** ✓. Il en découle
trois règles d'architecture :

1. **la sortie valide l'entrée** ✓✓ : ce que l'entrée a compris doit pouvoir être **reproduit** par la sortie —
   restitution à l'identique, ou **boucle** entrée → sortie → entrée ✓. *Si la sortie ne peut pas le redire,
   l'entrée a inventé ou perdu quelque chose* ✗✓ ;
2. **le signal se découple du bruit** ✓✓ : la sortie sert de **référence** ; on mesure l'écart entre ce que
   l'entrée a extrait et ce que la sortie sait reconstruire ✓ ;
3. **l'interface post-linguistique porte ses marqueurs de bruit** ✓✓ : confiance par token, ambiguïtés non résolues,
   langues détectées avec leur probabilité — *le module de pensée abstraite reçoit un sens **annoté de son bruit*** ✓✓.

**Conséquence pour la mesure** : toute mesure d'entrée se double d'une mesure de sortie ✓✓. Les séries précédentes
(restitution en flux, boucle de traduction) sont les deux faces du même miroir.
