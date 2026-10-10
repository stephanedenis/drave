> Campagne : **toutes-langues** · expérience **76**
> Titre : 76. La réserve du §75.4 est mesurée, et elle tranche : la structure s'obtient, la fidélité ne suit pas
> Date réelle : **2026-10-07 02:33 HAE** (source : commit `c535276`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 76. La réserve du §75.4 est mesurée, et elle tranche : la structure s'obtient, la fidélité ne suit pas

Le §75.4 laissait une mesure à faire : **le point amplifié à la magnitude du professeur
garde-t-il sa fidélité ?** Non.

| rang | α | **fidélité amplifiée** | P_lang | P_cont |
|---:|---:|---:|---:|---:|
| **2** | 10,78 | **0,2512** | **407,6** | **4 356,4** |
| 5 | 8,82 | 0,2675 | 692,6 | 4 356,4 |
| | | *0,4298 (non amplifié)* | *professeur 399,2* | *professeur 4 356,4* |

**Le rapport est à 98 % de la cible, les deux énergies sont aux magnitudes du professeur
— et la fidélité tombe à 0,2512**, contre 0,4298 sans amplification et 0,4703 pour le
point de départ.

### 76.1 La frontière, maintenant entièrement tracée

| point de fonctionnement | fidélité | rapport | P_cont |
|---|---:|---:|---:|
| rien | **0,4766** | 1,29 | 318,7 |
| apprendre quoi lire | 0,4667 | 2,41 | 438,5 |
| quoi lire + discriminant | 0,4378 | 5,83 | 280,5 |
| discriminant seul | 0,4341 | 6,96 | 30,2 |
| **les trois, non amplifié** | 0,4298 | **10,69** | 37,5 |
| **les trois, amplifié aux magnitudes du professeur** | **0,2512** | 10,69 | **4 356,4** |

**L'avant-dernière ligne est le résultat** : le rapport du professeur est atteint à 98 %
pour **0,047** de fidélité. **La dernière ligne est la limite** : amener les énergies aux
magnitudes du professeur coûte **0,18** de plus.

### 76.2 Pourquoi la dernière étape coûte si cher

Le rapport est invariant d'échelle (§67) — mais **la fidélité ne l'est pas**, parce
qu'il y a un **décalage additif** : la sortie est `ma + (écart)`, et l'amplification porte
sur l'écart seul. En le multipliant par 10,8, on garde la direction de l'écart mais on
éloigne la sortie de sa cible en norme. Le cosinus, lui, voit les deux.

**C'est exactement le rétrécissement du §60.1, retourné** : notre sortie était 3,4 fois
trop petite ; la remettre à l'échelle **corrige la norme** mais **casse la direction**, et
le cosinus ne pardonne que la seconde.

### 76.3 Ce qui est établi, et ce qui ne l'est pas

**Établi :**
1. la structure contenu/langue du professeur **est atteignable à 98 %** par trois
   mécanismes déployables, en forme fermée, sans rétropropagation (§75) ;
2. cette structure **ne coûte que 0,047 de fidélité** — c'est bon marché (§75) ;
3. **mais l'amener aux magnitudes du professeur coûte 0,18 de plus** (§76) ;
4. l'identité du §67 explique exactement pourquoi : le rapport est insensible à
   l'échelle, la fidélité ne l'est pas.

**Non établi :** si un point intermédiaire — une amplification partielle, ou un autre
rang — donne un meilleur compromis. La courbe n'a été échantillonnée qu'à deux rangs et
une seule amplitude cible.

### 76.4 Où en est la traque

**Seize moyens mesurés.** Dix écartés, chacun par une mesure et souvent par une
**identité** (§67). Deux retenus séparément (§64, §66). Un troisième qui fait les deux
mouvements opposés (§73). Une combinaison qui domine (§74). **Une composition qui atteint
la cible en structure (§75) et en montre le prix en fidélité (§76).**

**Le pont sait maintenant reproduire la structure contenu/langue de son professeur. Il
ne sait pas encore la reproduire en même temps que le contenu lui-même.** C'est la
frontière, elle est mesurée des deux côtés, et c'est la première fois de la session
qu'elle est tracée avec ses deux extrémités.


---
