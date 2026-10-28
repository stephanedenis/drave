# C3.2d — l'indo-européen à 14,7 % est un effet de composition

> **Objet.** L'indo-européen (98 langues) était la seule famille sous **30 %** en C3.2c (14,7 %).
> `data/udhr/genealogie.json` porte la **branche glottolog** : on découpe l'IE en **sous-familles**
> et on mesure chacune avec le même module de recopie.

## Résultats (8 textes, contrôle 0 %)

| sous-famille | langues | avant | après |
|---|---:|---:|---:|
| **indo-iranien** | 26 | 0,0 % | **100,0 %** |
| **baltique** | 15 | 12,5 % | **95,3 %** |
| **italique** | 29 | 11,4 % | **87,6 %** |
| **celtique** | 5 | 0,0 % | **79,9 %** |
| **germanique** | 20 | 0,0 % | **54,6 %** |
| *indo-européen entier* | *98* | *0,0 %* | ***14,7 %*** |

- **Toutes** les sous-familles dépassent **54 %** ; l'IE entier reste à **14,7 %**.
- Le **contrôle** est à **0 %** partout.

## Lecture

- Le **14,7 %** de l'IE n'est pas une incapacité du module : c'est un **effet de composition**.
  Les sous-familles apprennent **54,6 à 100 %**, mais un module **unique** entraîné sur 98 langues
  **mélange** des sous-familles très différentes et **perd** la recopie.
- La **germanique** est la plus basse (**54,6 %**) : c'est la sous-famille la plus **hétérogène**
  (anglais, allemand, néerlandais, langues scandinaves…).
- L'**indo-iranien** atteint **100 %** : sous-famille nombreuse mais **plus homogène**.
- La **taille** n'explique pas tout : le celtique (5 langues) est à **79,9 %**, la germanique
  (20 langues) à **54,6 %**.

## Verdict

**C3.2d explique C3.2c** : l'IE à 14,7 % est un **effet de composition**, pas une difficulté
intrinsèque. Un module **par sous-famille** est le bon grain ; un module **par famille** est trop
grossier pour l'IE.

## Limites

- **5 langues celtiques**, 150 articles ; l'échantillon est petit.
- Les 5 sous-familles utilisent un **point d'évaluation à mi-corpus** (corpus courts).
- **200 pas**, rang 8, un seul run par sous-famille.
- La branche glottolog est utilisée au **2ᵉ niveau** ; d'autres découpages sont possibles.

## Fichiers

- Données : `data/udhr/familles/ie_{italique,indo_iranien,germanique,baltique,celtique}.jsonl`.
- Outil : [`tools/lora_recopie.py`](../tools/lora_recopie.py).
- JSON : [`ie-sous-familles.json`](ie-sous-familles.json).
