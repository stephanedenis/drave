> Campagne : **toutes-langues** · expérience **17**
> Titre : 17. Le plateau du professeur est à la couche 8, PAS à la couche 10
> Date réelle : **2026-10-06 04:18 HAE** (source : commit `00b65d4`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 17. Le plateau du professeur est à la couche 8, PAS à la couche 10

Mesure sur le corpus parallèle *Romeo and Juliet*, invariance **segment par
segment** (24 scènes appariées) :

| couche | invariance moyenne | pire scène |
|---|---:|---:|
| 0 (plongement) | **0,1420** | **−0,0888** |
| 4 | 0,4483 | 0,1289 |
| **8** | **0,5985** | 0,1943 |
| 10 | 0,5703 | **0,2381** |

**Le plateau est à la couche 8** ; la couche 10 est déjà **en re-spécialisation**
vers la sortie (0,5703 contre 0,5985).

**Et ce n'est pas propre à ce corpus.** Sur l'UDHR propre (46 langues), je
mesurais **0,5471 à la couche 8 contre 0,5247 à la couche 10**. Les deux corpus
concordent.

### Ce que cela remet en cause

**Ma cible était mal choisie.** Depuis le début de ce travail, le pont émule la
**couche 10** — parce que la mesure initiale, faite sur l'article 1 de l'UDHR avec
quarante langues, plaçait le pic à 42 % de profondeur (couche 10 sur 24). Les deux
mesures d'aujourd'hui, sur des corpus et des panels différents, placent le pic
**deux crans plus haut**.

**Ce n'est pas une erreur de mesure, c'est une erreur de choix** : la couche 10
n'est pas la plus interlingue, et émuler une couche en re-spécialisation revient à
apprendre du détail linguistique qui coûte précisément l'invariance cherchée.

**Ce qu'il faudrait** : refaire la mesure du pont avec la couche 8 pour cible. Le
traçage de Romeo contient **déjà** la couche 8 (`--trace-couches 0,4,8,10`), donc
la comparaison est possible sans retracer.

### Le plongement, sur du texte littéraire

**0,1420 d'invariance à la couche 0, avec des scènes négatives** (jusqu'à −0,0888).
Sur du texte littéraire long, les plongements anglais et français sont **quasi
orthogonaux** — bien plus que sur l'UDHR (0,58 sur l'ancien panel). Cela quantifie
combien la couche d'entrée est propre à chaque langue, et donc **quel travail le
pont doit fournir**.


---
