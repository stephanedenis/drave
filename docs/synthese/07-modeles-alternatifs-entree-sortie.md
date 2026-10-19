# 7 — Les modèles alternatifs pour l'entrée et la sortie

> **Ce que ce chapitre est.** La **théorie** de l'étage entrée-sortie (nom historique : couche commune) : ce qu'il doit être, ce qu'on
> en sait, ce qui reste à prouver. Les **mesures** (67, avec leurs erratums et leurs pièges) sont dans
> [`reports/07-mesures-couche-commune.md`](../../reports/07-mesures-couche-commune.md).

## Le problème

Un modèle qui **lit et écrit** doit traiter **toutes les langues, dialectes et styles** sans que le **sens** qu'il
manipule dépende de la langue de surface. La question du chapitre : *la langue est-elle un **paramètre** de la
surface, et le contenu un **espace commun** ?*

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

## Ce qui reste ouvert (et qui commande la suite)

1. **la qualité de traduction** du module entrée-sortie : le **juridique** et le **littéraire** sont mesurés sur des
   textes non mémorisables ; il reste le **technique**, le **quotidien** et les **langues peu dotées** — c'est le
   juge de paix de l'étage ;
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
