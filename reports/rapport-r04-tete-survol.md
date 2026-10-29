# R0.4 — la tête de survol perd contre BM25 (0,601 contre 0,836), et gagne sur le juridique

> **Ligne de roadmap** : R0.4 · **Date** : 2026-10-29 · **Verdict** : ❌ **la tête ne bat jamais le
> scoreur classique** — v1 0,601 contre 0,836 ; v2 0,448 contre 0,811 ; **v3 (498 paires) 0,575
> contre 0,745**. La donnée paie (+13 points), mais une sonde linéaire ne rattrape pas BM25. ✅ le contrôle des étiquettes mélangées (**0,467**) montre que le
> signal est réel mais faible, pas une fuite.
>
> **Dispositif** : 114 paires (question, passage) — 19 questions du banc durci × (1 gold +
> 5 négatifs du même document) ; **états précoces** après les 4 premières couches de
> Qwen2.5-0.5B (896 valeurs, capturés par le moteur) ; tête logistique ridge ; partage
> **leave-one-document-out** ; JSON bruts [`r04-tete-survol.json`](r04-tete-survol.json) et
> [`r04-tete-survol-v2.json`](r04-tete-survol-v2.json) (version 2 : couches 8–11, négatifs durs).

## La question

Le contrôleur de R0.2 décide avec BM25 : il partage le scoreur du lecteur extractif et ne sait
pas ce qu'est une paraphrase. R0.4 demande une **tête apprise** : lire la question et le début
d'un passage, et prédire s'il vaut la peine d'être lu. La fiche est explicite : **la tête
bat-elle le scoreur classique à budget égal ?**

## Le dispositif

- **l'état précoce** : le moteur capture 896 valeurs après les **4 premières couches**
  (`--couches 0:3 --tete-partielle --etat-sortie`), au dernier jeton du prompt
  « Question : … / Passage : … » ; 2,2 s par paire, 114 paires en ~4 min ;
- **les négatifs** : 5 passages du **même document**, tirés au sort (graine fixe) — la tête ne
  peut pas apprendre « ce document est le bon » ;
- **le partage** : leave-one-document-out ; aucun passage du test n'est vu à l'entraînement ;
- **la référence** : BM25 sur les mêmes 6 candidats, AUC sur les mêmes paires ;
- **le contrôle** : mêmes états, **étiquettes d'entraînement mélangées**. Si la tête garde son
  AUC, elle lit une fuite (longueur, type, ordre) et non la pertinence.

## Ce qui est mesuré

| document | type | n test | AUC tête | AUC BM25 | AUC étiquettes mélangées |
|---|---|---:|---:|---:|---:|
| A_RES_80_1-fr.pdf | juridique | 18 | **0,956** | 0,622 | 0,200 |
| format-flux.md | technique | 24 | 0,588 | 0,800 | 0,500 |
| portes.md | code | 24 | 0,450 | 0,794 | 0,575 |
| roadmap.md | tableau | 24 | 0,550 | 1,000 | 0,412 |
| vision.md | prose | 24 | 0,463 | 0,963 | 0,650 |
| **moyenne** | | 114 | **0,601** | **0,836** | **0,467** |

**La tête perd 4 fois sur 5.** Le contrôle à 0,467 (≈ hasard) dit que les états ne portent pas
de fuite : les 0,601 sont un signal faible mais réel, pas un artefact.

**Et elle gagne là où BM25 est faible** : sur le **juridique** (0,956 contre 0,622), c'est-à-dire
sur les questions paraphrases où le recouvrement ne suffit pas. C'est exactement le régime que
R0.3 durci avait identifié — et le seul endroit où une tête mérite d'être poursuivie.

## Pourquoi elle perd — quatre raisons nommées

1. **Peu de données pour la dimension** : 90 paires d'entraînement par pli pour 896 dimensions ;
   la tête apprend le style des documents d'entraînement, pas la pertinence.
2. **Quatre couches, c'est très tôt** : l'état précoce encode la forme, pas encore le contenu
   de la question ; R0.4 parle d'« états précoces », pas de « première couche ».
3. **Les négatifs sont faciles** : 5 passages au hasard contre 1 gold — BM25 les sépare sans
   peine (0,836). Une tête utile doit être jugée sur des **négatifs difficiles** (même section,
   même vocabulaire).
4. **La tâche est un reranking, pas une recherche** : ici BM25 classe 6 candidats, alors que sa
   faiblesse mesurée en R0.3 (0,33 sur le juridique) portait sur la recherche dans **tout le
   document** — deux tâches différentes, et la fiche ne les distingue pas.

## La version 2 (états 8–11, négatifs durs) : pire

Deux changements, ceux que la fiche demandait : des **négatifs durs** (passages de la **même
section** que le gold, donc même vocabulaire) et des **états plus profonds** (après la couche 11
au lieu de 4).

| document | type | AUC tête | AUC BM25 | mélangé |
|---|---|---:|---:|---:|
| A_RES_80_1-fr.pdf | juridique | 0,400 | 0,600 | 0,667 |
| format-flux.md | technique | 0,338 | 0,694 | 0,350 |
| portes.md | code | 0,637 | 0,800 | 0,388 |
| roadmap.md | tableau | 0,438 | 1,000 | 0,575 |
| vision.md | prose | 0,425 | 0,963 | 0,800 |
| **moyenne** | | **0,448** | **0,811** | **0,556** |

**La tête décroche** (0,448, sous le hasard) et ne gagne plus **aucun** document. Le contrôle à
0,556 est du bruit d'échantillon, pas une fuite.

**Pourquoi c'est pire, et pourquoi c'est utile** : les négatifs faciles de la version 1
aidaient BM25 (0,836) *et* la tête (0,601) ; les négatifs durs retirent cette béquille, et la
tête — 90 paires pour 896 dimensions — s'effondre. Les états plus profonds n'y changent rien :
le problème n'est pas la couche, c'est le **nombre de paires**.

**Conclusion des deux versions** : une **sonde linéaire** sur les états d'un 0,5 B, avec 114
paires, ne bat pas BM25. Ce n'est pas « R0.4 est impossible » — c'est « R0.4 demande des
**centaines ou des milliers** de paires, et sans doute un encodeur **ajusté**, pas une sonde ».
La victoire juridique de la version 1 était du bruit : la version 2 la retourne (0,400 contre
0,600).

## La version 3 (498 paires, 84 questions) : la donnée paie, mais ne suffit pas

Avec le banc élargi (84 questions × 6 paires = 504, 498 après écart d'un gold déplacé), la tête
dispose de **~450 paires d'entraînement par pli** au lieu de 90. Mêmes états (couches 8–11),
mêmes négatifs durs.

| type | AUC tête | AUC BM25 | mélangé |
|---|---:|---:|---:|
| prose | 0,684 | 0,882 | 0,603 |
| tableau | 0,605 | 0,728 | 0,505 |
| technique | 0,583 | 0,705 | 0,553 |
| code | 0,581 | 0,762 | 0,517 |
| juridique | 0,422 | 0,646 | 0,559 |
| **moyenne** | **0,575** | **0,745** | **0,548** |

**La tendance est bonne** : 0,448 (114 paires) → **0,575** (498 paires), et la tête gagne
6 documents sur 28. **Mais elle reste 17 points sous BM25**, et le contrôle des étiquettes
mélangées (0,548) est si proche de la tête que son avantage est, sur plusieurs types, du bruit
— sur le juridique, le contrôle (0,559) fait **mieux** que la tête (0,422).

**Ce que ça dit** : la donnée est bien le facteur limitant (×5,5 de paires → +13 points d'AUC),
mais une **sonde linéaire** sur les états d'un 0,5 B ne rattrapera pas BM25 avec 500 paires.
Il faudrait des **milliers** de paires et/ou un encodeur **ajusté**. La porte R0.4 reste
ouverte, avec ce chemin nommé.

## Ce qui pourrait le rendre faux

- **Petit N** : 114 paires, 5 plis de 18–24 ; une AUC à ±0,1 par pli.
- **Une seule tête linéaire** : une petite MLP ou une régression sur des états plus profonds
  peut changer la conclusion — c'est un négatif **de ce dispositif**, pas de l'idée.
- **Un seul format de prompt** : « Question / Passage » n'est pas la seule façon d'apparier.
- **Négatifs aléatoires** : le résultat dit « la tête ne bat pas BM25 sur des négatifs
  faciles », pas « la tête est inutile ».
- **États d'un modèle de 0,5 B** : les états précoces d'un modèle plus grand encodent sans doute
  plus de contenu.

## Ce que ça change

1. **La porte de R0.4 n'est pas atteinte** : la fiche reste ouverte, avec un chemin nommé —
   plus de paires, des états plus profonds, des négatifs difficiles, une tête non linéaire.
2. **Le seul signal positif est le régime paraphrase** : la tête gagne là où BM25 est faible.
   Si elle doit exister, c'est pour ce régime — pas pour remplacer BM25 partout.
3. **La leçon de méthode** : une tête jugée sur des négatifs faciles est une tête jugée sur un
   banc qui ne peut pas perdre. Le prochain jeu doit tirer ses négatifs dans le même voisinage
   lexical que le gold.

## Fichiers

- `tools/tete_survol.py` — capture des états, tête ridge, partage par document, contrôle.
- `reports/r04-tete-survol.json` — les mesures brutes.
- `tools/tests/documents/bench-durci.json` — les 19 questions et leurs golds.
