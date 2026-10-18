# 7 — Les modèles alternatifs pour l'entrée et la sortie

> **Ce que ce chapitre est.** La **théorie** de la couche commune entrée-sortie : ce qu'elle doit être, ce qu'on
> sait d'elle, ce qui reste à prouver. Les **mesures** (48, avec leurs erratums et leurs pièges) sont dans
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
  trois sont **lues à 100 %**. *La couche commune n'efface aucune surface : elle en aligne le sens.*

## Ce qui reste ouvert (et qui commande la suite)

1. **la qualité de traduction** du module entrée-sortie : la retrouver sur des **domaines** (technique, juridique,
   littéraire) et des **langues peu dotées** — c'est le juge de paix de la couche ;
2. **la restitution exacte à l'échelle** : au-delà de 10 langues partagées, elle meurt ; faut-il des modules
   spécialisés par famille, ou un modèle beaucoup plus grand ?
3. **le style** : il est lisible, mais le sens ne le traverse qu'à 24 % — comment l'augmenter sans perdre le style ?

*Tant que ces trois questions ne sont pas tranchées, le module de **pensée abstraite** attend : il ne peut pas être
bâti sur une entrée-sortie qui n'est pas fiable.*
