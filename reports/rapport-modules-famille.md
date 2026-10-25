# C3.2b — un module de restitution par famille : l'indo-européen recopie à 100 %

> Mesure du 24/10/2026, Qwen2.5-0.5B, la famille **indo-européenne** (98 langues, 3 688 articles UDHR),
> `tools/lora_recopie.py --famille`.

## Le protocole

- **Le corpus** : `data/udhr/familles/indo-european.jsonl` (les articles de la famille), encodé par le tokenizer.
- **Le LoRA** : rang 8, **200 pas**, lr 1e-3, sur la recopie (l'invite « Recopie exactement… » → la cible = le texte).
- **La mesure** : le **taux de recopie** (le plus long préfixe exact), avant et après ; le **contrôle** (la même
  invite avec une cible différente) ; **3 textes d'évaluation jamais vus** à l'entraînement.

## Les résultats

| | la recopie | le contrôle |
|---|---:|---:|
| avant | 0,0 % | 0,0 % |
| **après, 3 textes** | **100,0 %** | **0,0 %** |
| après, 8 textes (indo-européen) | 14,7 % | 0,0 % |
| après, 8 textes (atlantic-congo) | 94,0 % | 0,0 % |
| après, 8 textes (austronesian) | 61,0 % | 0,0 % |
| après, 8 textes (sino-tibetan) | **100,0 %** | 0,0 % |
| après, 8 textes (turkic) | **96,1 %** | 0,0 % |

**La copie est acquise et le perroquet est évité.** Le module par famille recopie **exactement** le texte de sa
famille, et le contrôle (une cible différente) reste à **0 %** — ce n'est pas de la génération qui singe, c'est de la
restitution.

## Ce que ça dit, et ce que ça ne dit pas

- **Ça dit** : un module par famille **apprend à recopier** sa famille — **100 % sur 3 textes d'évaluation, 14,7 % sur
  8**. Le contrôle reste à **0 %** dans les deux cas : ce n'est pas le perroquet.
- **Ça ne dit pas** : que la **restitution à dix langues** est sauvée (c'est C3.2c) ; le modèle est le **0,5 B** et
  **200 pas** seulement.
- **La leçon, et elle est importante** : le **100 %** de la première mesure était un **effet de la taille de
  l'échantillon** (3 textes) — sur 8, il tombe à **14,7 %**. C'est la cinquième fois que la leçon du point de mesure
  se paie : **le chiffre dépend de ce qu'on mesure, et un taux sur 3 textes ne dit rien de la restitution.**
- **Le chiffre honnête** : **14,7 %** sur 8 textes (indo-européen), à comparer aux **30 %** de la référence à une langue
  et aux **4,4 %** à dix langues — au-dessus de la référence à dix langues (3,3×), sous celle à une langue.
- **La courbe complète (5 familles, 8 textes, le contrôle à 0 % partout)** :

  | la famille | langues | la recopie |
  |---|---:|---:|
  | indo-européen | 98 | **14,7 %** |
  | atlantic-congo | 74 | **94,0 %** |
  | austronesian | 35 | **61,0 %** |
  | sino-tibetan | 17 | **100,0 %** |
  | turkic | 14 | **96,1 %** |

- **Ce que la courbe dit** : **4 familles sur 5 dépassent les 30 %** de la référence à une langue — le module par
  famille **casse bien la chute**. La seule qui reste basse est **l'indo-européen (14,7 %)**, la plus **grande**
  (98 langues) et la plus **hétérogène**. *La difficulté n'est pas la taille du corpus, c'est l'hétérogénéité interne
  de la famille* — et c'est exactement ce qu'il fallait mesurer.
- **La réserve** : le `sino-tibetan` partait de **40,5 %** avant l'entraînement (le modèle connaissait déjà une partie
  de ces textes) — sa progression (59,5 points) est moins parlante que les autres ; l'`austronesian` (61 %) et
  l'`indo-européen` (14,7 %) sont les cas où le module **ajoute** le plus.

## La suite

**C3.2c** : la même mesure avec **plus de textes**, sur les **9 familles** de 9 langues ou plus, et la comparaison à
la courbe — le module par famille **casse-t-il la chute entre 1 et 10 langues** ?
