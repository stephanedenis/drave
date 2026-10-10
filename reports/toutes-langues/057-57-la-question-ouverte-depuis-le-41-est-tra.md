> Campagne : **toutes-langues** · expérience **57**
> Titre : 57. LA question ouverte depuis le §41 est tranchée : notre sortie ÉCRASE la distinction contenu / langue
> Date réelle : **2026-10-06 19:45 HAE** (source : commit `83cd425`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 57. LA question ouverte depuis le §41 est tranchée : notre sortie ÉCRASE la distinction contenu / langue

### 57.1 La question, et pourquoi elle traînait

Depuis le §41, un même fait revient : **notre sortie est beaucoup plus invariante
entre langues que la représentation du professeur qu'elle imite** — 0,95 contre 0,65
sur l'UDHR, **0,928 contre 0,347** sur le corpus Wikipedia multi-domaine (§56).
Deux lectures, et rien ne les départageait :

1. **C'est la mission.** Un pont linguistico-sémantique veut l'invariance.
2. **C'est de l'appauvrissement.** Une sortie qui ne dépend presque plus de l'entrée
   est invariante pour la mauvaise raison : elle a effacé le contenu avec la langue.

### 57.2 Le test, et il ne demande aucun corpus nouveau

Mesurer la **même** similarité sur les **deux** axes, sur les **mêmes** entrées, pour
notre sortie **et** pour le professeur :

- `S_langue` — **même article, langues différentes** : ce qu'on veut **garder** ;
- `S_domaine` — **même langue, articles différents** : ce qu'il faut **distinguer**.

Si `S_domaine ≈ S_langue`, la sortie ne distingue plus les contenus. Si
`S_domaine ≪ S_langue`, elle distingue les contenus **et** rapproche les langues.

### 57.3 Le résultat, sur deux corpus et deux pooling

**Corpus Wikipedia multi-domaine** (3 langues apprises, 3 en test, 85 articles) :

| pooling | | S_langue | S_domaine | écart | rapport |
|---|---|---:|---:|---:|---:|
| dernière position | **NOTRE SORTIE** | 0,7491 | 0,7495 | **−0,0005** | **1,00** |
| dernière position | professeur | 0,2337 | 0,2163 | **+0,0174** | 1,08 |
| moyenne | **NOTRE SORTIE** | 0,9835 | 0,9866 | **−0,0031** | **1,00** |
| moyenne | professeur | 0,9454 | 0,8937 | **+0,0517** | 1,06 |

**Ce n'est pas un artefact de position** : les deux pooling donnent le même verdict.
**Notre sortie ne sépare plus les deux axes du tout, et le professeur, si** — dans le
sens du CONTENU, sur les deux pooling.

**Contrôle sur l'UDHR** (unités alignées, 300 langues apprises, 230 unités de test) :

| | S_langue | S_domaine | écart | rapport |
|---|---:|---:|---:|---:|
| **NOTRE SORTIE** | 0,8824 | 0,9907 | **−0,1083** | **0,89** |
| professeur | 0,6939 | 0,9421 | **−0,2482** | 0,74 |

### 57.4 La conclusion honnête, et elle n'est ni tout noir ni tout blanc

Sur **les deux** corpus, **notre pont sépare moins le contenu de la langue que le
professeur** :

| corpus | séparation du professeur | séparation de notre sortie | retenue |
|---|---:|---:|---:|
| UDHR | −0,2482 | −0,1083 | **44 %** |
| Wikipedia (3 langues) | **+0,0517** | **−0,0031** | **0 %**, et le SIGNE s'inverse |

**Sur l'UDHR, notre pont conserve 44 % de la séparation du professeur** — imparfait,
mais réel. **Sur Wikipedia, il n'en conserve rien et change de signe** : là où le
professeur préfère le contenu, notre sortie est indifférente.

### 57.5 Ce que cela change dans tout le rapport

**Tous les chiffres d'invariance de ce rapport doivent être lus avec cette
qualification.** Une invariance de 0,90-0,96 n'est pas, à elle seule, la preuve d'un
pont réussi : elle mélange deux choses qui n'ont pas été séparées jusqu'ici —
**rapprocher les langues** et **effacer les différences**. Le test ci-dessus est le
seul qui les sépare, et il n'avait jamais été fait.

**Ce n'est PAS la pénalité μ qui cause l'écrasement** : mesuré à μ = 0 et μ = 0,1 sur
Wikipedia, le rapport vaut **1,00 dans les deux cas**. L'écrasement existe déjà sans
contrainte. μ le dégrade très légèrement (les deux similarités montent de +0,0036),
mais il n'en est pas la cause.

**Ce qui reste à faire, et c'est désormais précis** : l'objectif de la lecture doit
être réécrit pour **favoriser explicitement l'axe contenu** — non pas « rapprocher les
langues », mais « rapprocher les langues **à contenu égal** et **éloigner les contenus
à langue égale** ». Les deux termes sont quadratiques en `W`, donc la solution reste en
forme fermée ; c'est la même mécanique que le §48, appliquée au bon objectif.


---
