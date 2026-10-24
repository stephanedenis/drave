# Le NLI français plus dur que XNLI : DACCORD +26,9, GQNLI +56,7 — et le 1,5 B bat le 3 B

> Mesures du 24/10/2026, Qwen2.5-**1.5B**-Instruct (fp16), couche 18, le protocole de `tools/nli_fr_dur.py` et
> `tools/xnli_latent.py` : sonde linéaire (ridge), découpage 70/30, **contrôle par étiquettes mélangées**, MLP.
> XNLI : 2 490 paires FR/EN (747 en test) ; DACCORD : 1 034 paires FR (311 en test) ; GQNLI-FR : 300 paires FR
> (90 en test).

## La question

XNLI est le seul jeu NLI français « courant ». DACCORD (les contradictions) et GQNLI-FR (les quantificateurs) ont
été construits pour être **plus durs que XNLI** (Skandalis et al., LREC-COLING 2024). La sonde linéaire lit-elle
encore la réponse dans l'état sur ces jeux — ou le 0,50 de XNLI était-il déjà le plafond du facile ?

## Les résultats

| jeu | classes | hasard | **sonde FR** | **marge** | contrôle (mélangé) | MLP |
|---|---:|---:|---:|---:|---:|---:|
| **XNLI** | 3 | 0,333 | 0,6921 | **+0,359** | 0,3253 | 0,7282 |
| **DACCORD** | 2 | 0,500 | 0,7685 | **+0,269** | 0,5498 | 0,8006 |
| **GQNLI-FR** | 3 | 0,333 | 0,9000 | **+0,567** | 0,4000 | 0,9444 |

- **Le jeu « plus dur » est lisible, mais sa marge est la plus faible** : le DACCORD fait **+26,9** au-dessus du
  hasard, contre **+35,9** pour XNLI — la difficulté annoncée se lit dans la **marge**, pas dans le hasard.
- **Les quantificateurs (GQNLI) sont les plus faciles** : +56,7, et 94,4 % au MLP — un motif **systématique**, donc
  très linéairement séparable.
- **Les contrôles sont propres partout** : les étiquettes mélangées ramènent au hasard (0,325 ; 0,550 ; 0,400).

## Le 3 B à travers ses couches : il décolle à la fin — la « décroissance » était le point de mesure

Mesure du 24/10 sur DACCORD, couche par couche (le même protocole) :

| couche | profondeur | sonde FR | MLP |
|---|---:|---:|---:|
| 12 | 33 % | 0,511 | 0,489 |
| 18 | 50 % | 0,592 | 0,543 |
| 24 | 67 % | 0,836 | 0,868 |
| **30** | **83 %** | **0,865** | **0,894** |

- **La couche 18 était un mauvais point, pas le modèle** : à la couche 30, le 3 B lit **0,865** — le **meilleur de
  la série**, devant le 1,5 B (0,692 à sa couche 18) et le 32 B (0,600 à sa couche 32).
- **Le confondant n'était pas la profondeur mais le point de mesure** : comparer à la même profondeur relative (50 %)
  est aussi arbitraire que comparer à la couche 18 — chaque modèle a **sa** couche, et elle est **tardive** (64 % pour
  le 1,5 B, 83 % pour le 3 B).
- **La leçon se corrige** : « la lisibilité n'est pas monotone avec la taille » était **l'effet du point de mesure** ;
  à leur meilleure couche, **le 3 B bat le 1,5 B** (0,865 contre 0,692) — la taille aide, à condition de regarder au
  bon endroit.

## Ce que ça change pour la carte

La carte du raisonnement doit être lue **par modèle, à sa meilleure couche** — ou avec **les deux bornes** (la
profondeur fixe et la meilleure couche). C'est la seule comparaison qui ne confond pas la taille avec le point de
mesure ; l'erreur a été faite deux fois aujourd'hui (la couche 18, puis la profondeur 50 %), et corrigée deux fois.

## Le pont au 1,5 B : 0,83, le meilleur mesuré

| modèle | sonde FR (XNLI) | pont EN→FR |
|---|---:|---:|
| **1,5 B** | **0,6921** | **0,8300** |
| 3 B (mesure 160) | 0,502 | 0,592 |
| 14 B (mesure 161) | 0,481 | 0,627 |

- **Le petit modèle bat les gros sur la sonde et sur le pont** : 0,692 contre 0,502 (3 B) et 0,481 (14 B) ; le pont
  à 0,83 contre 0,592 et 0,627. *La lisibilité linéaire n'est pas la capacité* : les représentations des grands
  modèles sont plus **distribuées**, donc moins accessibles à une sonde linéaire — un effet connu, que cette
  mesure retrouve.
- Le renversement n'invalide pas la carte du raisonnement (le synthétique tient au 3/7/14 B) : il dit que la
  **sonde linéaire** n'est pas une mesure monotone de la qualité.

> **Correction du 24/10 (le soir).** Les chiffres de cette fiche sont lus à la **couche 18**, dont la profondeur
> relative varie (64 % au 1,5 B, 50 % au 3 B, 37 % au 14 B) : le « renversement » **confond la taille et la
> profondeur**. La comparaison à profondeur relative fixe (les couches 14/18/24/32) est en file — voir
> [`rapport-32b-couche-confondant.md`](rapport-32b-couche-confondant.md). Le constat « la lisibilité linéaire n'est
> pas monotone avec la taille » reste une **hypothèse**, pas un résultat, tant que la profondeur n'est pas contrôlée.

## Ce que ce résultat ne dit pas

- **Un seul modèle** (1,5 B) pour les trois jeux ; le 3 B, le 7 B et le 32 B (l'extraction du 32 B tourne) diront si
  la marge du DACCORD remonte ou non avec la taille.
- **Les tâches n'ont pas le même nombre de classes** (2 contre 3) : la comparaison juste est la **marge** au-dessus
  du hasard, pas l'exactitude brute.
- **Le GQNLI n'a que 90 exemples de test** : ±5 points d'intervalle ; le 0,90 est une indication, pas un chiffre
  définitif.
- DACCORD et GQNLI mesurent la **contradiction** et les **quantificateurs**, pas la même inférence que XNLI ; la
  « difficulté » des auteurs porte sur la génération des modèles, la sonde ne mesure qu'une partie.
