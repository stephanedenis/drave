# C3.2c — les 9 familles : 7 sur 9 au-dessus de 30 %

> **Objet.** Étendre la mesure des modules par famille aux **9 familles** de 9 langues ou plus
> (C3.2c). Les 5 premières étaient mesurées ; les 4 nouvelles sont **afro-asiatic**, **quechuan**,
> **mayan** et **uralic**.

## Résultats (8 textes, contrôle 0 %)

| famille | langues | avant | après | contrôle |
|---|---:|---:|---:|---:|
| indo-européen | 98 | 0,0 % | **14,7 %** | 0,0 % |
| atlantic-congo | 74 | — | **94,0 %** | 0,0 % |
| **quechuan** | 11 | 33,3 % | **88,2 %** | 0,0 % |
| **mayan** | 9 | 8,9 % | **64,4 %** | 0,0 % |
| **afro-asiatic** | 12 | 0,0 % | **60,2 %** | 0,5 % |
| austronesian | 35 | — | **61,0 %** | 0,0 % |
| **uralic** | 9 | 31,0 % | **46,7 %** | 0,0 % |
| turkic | 14 | — | **96,1 %** | 0,0 % |
| sino-tibetan | 17 | 40,5 % | **100,0 %** | 0,0 % |

- **Moyenne des 9** : **69,5 %** ; **médiane** : **64,4 %**.
- **7 familles sur 9** dépassent **30 %** ; **1 seule** (indo-européen) est sous **30 %**.
- Le **contrôle** reste **≤ 0,5 %** partout.

## Lecture

- La **taille** n'explique pas tout : l'**indo-européen** (98 langues) est **dernier** à **14,7 %**,
  tandis que le **quechuan** (11 langues) est à **88,2 %**.
- L'**hétérogénéité interne** reste la variable : l'indo-européen mélange des familles internes très
  différentes ; l'uralic (9 langues) reste à **46,7 %** malgré sa petite taille.
- **4 nouvelles familles** : **3 sur 4** au-dessus de **60 %** ; l'**uralic** est le négatif.
- Le **contrôle** à 0 % montre que le module **recopie** sa famille, sans perroquet.

## Limites

- Les 4 nouvelles familles utilisent un **point d'évaluation à mi-corpus** (le corpus est plus court
  que 60 000 tokens), tandis que les 5 premières évaluent après 60 000 : le protocole n'est **pas
  identique**.
- **200 pas**, rang 8, 8 textes ; un seul run par famille.
- L'**indo-européen** et l'**uralic** restent les cas à instruire (hétérogénéité interne).
- Le **sino-tibetan** partait de **40,5 %** avant entraînement (connaissance préalable).

## Verdict

**C3.2c est close sur les 9 familles** : **7/9 > 30 %**, moyenne **69,5 %**, contrôle **0 %**. Le
module par famille **casse la chute** pour la majorité, mais l'**indo-européen** (14,7 %) et
l'**uralic** (46,7 %) montrent que l'**hétérogénéité interne** est le vrai facteur.

## Fichiers

- Outil : [`tools/lora_recopie.py`](../tools/lora_recopie.py) (`--eval-debut`).
- JSON : [`familles-9.json`](familles-9.json).
