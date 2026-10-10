> Campagne : **campagne-benefices** · expérience **31**
> Titre : 31. Clé de FENÊTRE : la prédiction est RÉFUTÉE, et elle confirme la leçon du §24 quater
> Date réelle : **2026-10-10 05:44 HAE** (source : commit `892acfd`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 31. Clé de FENÊTRE : la prédiction est RÉFUTÉE, et elle confirme la leçon du §24 quater

Le §30 avait identifié le mécanisme de l'hypersensibilité du rappel : la clé est un
**k-WTA** (64 canaux sur 16 384), donc une petite variation de l'état fait entrer et
sortir des canaux et **la clé saute** — deux jetons voisins donnaient 1 006 et 50 jetons.
Prédiction falsifiable qui en découle : **former la clé sur la moyenne de W positions
voisines doit lisser la clé et réduire l'hypersensibilité**. Mesuré (magasin de 1 750
états, aiguille au jeton 740, hasard 448) avec les deux indices extrêmes :

| fenêtre de clé | indice « only » (le bon) | indice « code » (le mauvais) | **séparation** |
|---|---|---|---|
| **1** (position seule) | **50** | 1 006 | **1,31/64** |
| 4 | 653 | 1 005 | 1,73/64 |
| 16 | 573 | 1 004 | 4,58/64 |
| 64 | **449** (= le hasard) | 1 004 | **19,94/64** |

**La prédiction est réfutée, et proprement :**

1. le lissage **ne réduit pas** l'hypersensibilité — il **détruit le bon indice**, qui
   passe de 50 jetons (9× mieux que le hasard) à **449**, c'est-à-dire exactement le
   hasard, pendant que le mauvais reste mauvais (1 006 → 1 004) ;
2. la **séparation s'effondre** : de 1,31 à **19,94 canaux partagés sur 64** — la clé
   d'une moyenne ressemble à celle de tout le monde, donc elle ne distingue plus rien.

**Et cela confirme, par une troisième voie indépendante, la leçon du §24 quater** : dans
cette mémoire, **abstraire par moyennage détruit la rappelabilité**. Le prototype moyen
était mal rappelé (22 % contre 87 % pour l'exemplaire), la clé moyenne ne retrouve pas le
bon passage, et la fenêtre moyenne fait tomber le meilleur indice au hasard. Trois
mesures, trois mécanismes différents, une seule conclusion : **la sélectivité de cette
mémoire EST la netteté de sa clé**, et l'hypersensibilité à l'indice en est le prix.

**Conséquence pour la suite, et elle change de direction** : puisque le lissage est exclu,
et puisque le choix de l'indice n'est pas devinable (§30), le rappel par le contenu n'est
pas la bonne primitive pour retrouver un passage depuis une question. Ce qui reste
défendable est ce qui a été mesuré comme solide : la **complétion de motif** depuis une
clé dégradée (Δ = 2 jetons à 50 % de dégradation à N = 300, 11 jetons à N = 2 048), la
localisation en jetons, et l'**injection** d'un état retrouvé. Retrouver un passage depuis
une question demande autre chose — des jetons (RAG ordinaire) ou une clé apprise.
