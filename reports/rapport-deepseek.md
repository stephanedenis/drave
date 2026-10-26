# B9 — DeepSeek pour le langage, GPU pour le modèle natif

> Mesure du **26/10/2026**, sur `Hauru` (2 × RTX 5000 16 Go, Python 3.13) et l'API
> **`deepseek-flash`** (licence du propriétaire ; distillation et entraînement explicitement autorisés).
> La question : le **langage** peut-il sortir des GPU, et les GPU revenir au **modèle natif**
> `route` / `drave-core` ? Deux échelles : **60 prompts** (pilote) puis **310** (30 articles UDHR).
> JSON : [`deepseek-mesures.json`](deepseek-mesures.json) (60),
> [`deepseek-mesures-300.json`](deepseek-mesures-300.json) (310),
> [`deepseek-natif-300.json`](deepseek-natif-300.json) (distillation). Code :
> [`tools/llm/`](../tools/llm/), porte [`tools/porte-deepseek.sh`](../tools/porte-deepseek.sh).

## Ce qui est mesuré

1. **Le banc externe** : des prompts publics (traductions d'articles de la Déclaration universelle
   des droits de l'homme vers dix langues, questions de jeux) envoyés à `deepseek-flash` ; qualité
   **chrF** contre la traduction humaine officielle, avec le **plancher** source→référence, tokens,
   latence, cache.
2. **L'élève natif** : le corpus professeur est converti en `train/val` par identifiant, puis
   `route` (4,04 M paramètres, architecture du moteur) est entraîné sur **GPU** (`cuda`).
3. **Le contrôle de distillation** : mêmes prompts, réponses d'entraînement **mélangées**,
   validation **alignée** ; trois graines. Si l'élève aligné ne bat pas le mélangé, la
   distillation n'est **pas** établie.

## 1. Le banc DeepSeek

### Le pilote : 60 prompts

| mesure | valeur |
|---|---:|
| prompts | **60** |
| traductions | **50** (5 articles × 10 langues) |
| questions de jeux | **10** |
| modèle servi | **`deepseek-flash`** |
| tokens d'entrée | **5 552** |
| tokens de sortie | **10 857** |
| latence totale | **135,1 s** |
| latence moyenne | **2,252 s** / requête |
| cache (premier passage) | **0 / 60** |

### L'échelle : 310 prompts

| mesure | valeur |
|---|---:|
| prompts | **310** |
| traductions | **300** (30 articles × 10 langues) |
| questions de jeux | **10** |
| modèle servi | **`deepseek-flash`** |
| tokens d'entrée | **34 112** |
| tokens de sortie | **32 436** |
| latence totale | **511,1 s** |
| latence moyenne | **1,649 s** / requête |
| cache | **60 / 310** (les prompts du pilote) |

### La qualité des traductions à l'échelle

chrF (n-grammes de caractères, β = 2) contre la traduction humaine UDHR ; le **plancher** est le
même chrF entre la source anglaise et la référence, c'est-à-dire ce que vaut une **non-traduction**.

| langue | n | chrF | plancher | écart |
|---|---:|---:|---:|---:|
| espagnol | 30 | **99,28** | 27,70 | +71,58 |
| russe | 30 | **98,86** | 2,60 | +96,26 |
| français | 30 | **96,58** | 29,71 | +66,87 |
| italien | 30 | **92,87** | 27,51 | +65,36 |
| allemand | 30 | **90,50** | 20,58 | +69,92 |
| portugais | 30 | **88,35** | 27,52 | +60,83 |
| chinois mandarin | 30 | **77,70** | 0,26 | +77,44 |
| arabe | 30 | **70,80** | 2,90 | +67,90 |
| hindi | 30 | **58,45** | 2,74 | +55,71 |
| swahili | 30 | **54,83** | 14,90 | +39,93 |
| **moyenne** | **300** | **82,82** | **15,64** | **+67,18** |

La moyenne est **stable** entre le pilote (82,48 sur 5 articles) et l'échelle (82,82 sur 30), mais
les langues **bougent** : le pilote **surestimait** l'allemand (**99,42 → 90,50**) et le chinois
(**87,70 → 77,70**), et sous-estimait le portugais (**82,11 → 88,35**) et l'italien
(**81,92 → 92,87**). Les 5 articles n'étaient pas représentatifs : c'est le **30 articles** qui
fait foi. Le plancher dépend de la proximité des écritures ; le **chrF brut n'est pas comparable
entre langues**, c'est l'écart au plancher qui dit que le professeur traduit. Les deux langues les
plus basses, **hindi (58,45)** et **swahili (54,83)**, restent les négatifs nommés.

## 2. L'élève natif sur GPU

Le corpus professeur est découpé par **identifiant**. Le modèle `route` a **4,04 M paramètres**
(dim 192, 4 couches, 8 experts, k = 2) ; l'entraînement tourne sur **`cuda`**.

### Le pilote : 60 exemples, 50 pas

50 train / 10 val, 48 413 / 12 392 caractères.

| entraînement | graine | val (bits/octet) |
|---|---:|---:|
| réponses **alignées** | 1 | **3,7847** |
| réponses **alignées** | 2 | **3,8092** |
| réponses **alignées** | 3 | **3,8635** |
| réponses **mélangées** (contrôle) | 1 | **3,8530** |
| réponses **mélangées** (contrôle) | 2 | **3,8236** |
| réponses **mélangées** (contrôle) | 3 | **3,8316** |

Moyennes : **aligné 3,8191**, **mélangé 3,8361** — **0,017 bit/octet** (0,44 %), signes mitigés
(2 graines sur 3 pour l'aligné). À 60 exemples, ce n'est **pas** un effet établi : un smoke test.

### L'échelle : 310 exemples, 500 pas

271 train / 39 val, 231 730 / 35 897 caractères ; même modèle, même découpage par identifiant.

| entraînement | graine | val (bits/octet) |
|---|---:|---:|
| réponses **alignées** | 1 | **2,7690** |
| réponses **alignées** | 2 | **2,7370** |
| réponses **alignées** | 3 | **2,8066** |
| réponses **mélangées** (contrôle) | 1 | **2,7110** |
| réponses **mélangées** (contrôle) | 2 | **2,7669** |
| réponses **mélangées** (contrôle) | 3 | **2,7751** |

Moyennes : **aligné 2,7709**, **mélangé 2,7510** — le **contrôle est meilleur** de **0,0199
bit/octet** (0,72 %), et il gagne **2 graines sur 3**. À **4,04 M**, la distillation par séquences
**n'est pas établie**. Le contrôle par permutation fait exactement son travail : il empêche de
conclure sur une graine favorable.

### Le seuil de capacité : entre 4,04 M et 10,70 M

Même corpus, même découpage, même perte ; seule change la taille de `route`. Quatre tailles,
trois graines à chaque fois.

| modèle | paramètres | aligné (moyenne) | mélangé (contrôle) | écart | signe |
|---|---:|---:|---:|---:|---|
| dim 192, 4 couches | **4,04 M** | 2,7709 | **2,7510** | −0,0199 | **contrôle** (2/3) |
| dim 256, 6 couches | **10,70 M** | **2,7166** | 2,7622 | +0,0456 | **aligné 3/3** (1,65 %) |
| dim 320, 7 couches | **16,02 M** | **2,7210** | 2,7742 | +0,0532 | **aligné 3/3** (1,92 %) |
| dim 384, 8 couches | **22,54 M** | **2,6915** | 2,7393 | +0,0478 | **aligné 3/3** (1,74 %) |

Le **seuil est entre 4,04 M et 10,70 M** : le premier point positif est **10,70 M**, et les deux
suivants le confirment. Le grand modèle de 22,54 M fait **1,18 M** poids lus par jeton et par
couche, **2,95 M** stockés, **`cuda`**, 500 pas en **52–56 s**.

| entraînement | graine | val (bits/octet) |
|---|---:|---:|
| **22,54 M**, réponses alignées | 1 | **2,7234** |
| **22,54 M**, réponses alignées | 2 | **2,7030** |
| **22,54 M**, réponses alignées | 3 | **2,6482** |
| **22,54 M**, réponses mélangées | 1 | **2,7340** |
| **22,54 M**, réponses mélangées | 2 | **2,7730** |
| **22,54 M**, réponses mélangées | 3 | **2,7109** |

Le facteur qui change le signe est la **capacité**, pas la quantité de données (310 exemples dans
les deux cas). À 4,04 M, même la perte masquée ne renverse pas le contrôle ; à 10,70 M, le
transfert existe. Le seuil exact (entre 4,04 et 10,70) reste à localiser.

### La perte masquée : le prompt n'est pas le levier à 4,04 M

Le prompt est **lu** mais sa perte est **masquée** (`tools/llm/masque.py`,
`tools/llm/entrainer_masque.py`) : seule la réponse compte. Même corpus, même découpage, une graine.

| modèle | aligné | mélangé (contrôle) | écart | lecture |
|---|---:|---:|---:|---|
| **4,04 M** | 2,7708 | **2,7549** | −0,0159 | **contrôle meilleur** : le masque ne sauve pas le petit modèle |
| **10,70 M** | 2,8507 | 2,8486 | −0,0021 | **égal**, et les deux sont **au-dessus** du trainer (2,72) — banc non calibré |

À 4,04 M, la perte masquée **ne change pas la conclusion** : le contrôle reste meilleur. À 10,70 M,
le banc masqué n'est pas au niveau du trainer (pas de warmup ni de clipping, boucle séparée) : il
est **non concluant**, pas un négatif du principe. La prochaine étape est de calibrer ce banc avant
de conclure sur le masque.

Le **modèle natif** a aussi été essayé sur le corpus public (`data/corpus_en.txt`, 20 pas) :
**4,04 M paramètres**, **`cuda`**, val **4,4150** bits/octet. Ce n'est pas une mesure de qualité,
c'est la preuve que la chaîne GPU → modèle → export fonctionne **sans Qwen**.

## 3. Les contrôles

- **plancher chrF** : source→référence, **15,64** à l'échelle ; sans lui, 82,82 ne veut rien dire ;
- **permutation des réponses d'entraînement** : mêmes prompts, réponses mélangées, validation
  **alignée**, trois graines ; à **4,04 M**, le contrôle **bat** l'aligné de 0,72 % ; à **10,70 M**,
  **16,02 M** et **22,54 M**, l'aligné **gagne 3/3** (1,65 %, 1,92 %, 1,74 %) ;
- **perte masquée** : à 4,04 M, le contrôle bat encore l'aligné (2,7549 contre 2,7708) ; à 10,70 M,
  le banc masqué n'est pas calibré (2,85 contre 2,72 au trainer) — **non concluant**, pas un
  négatif du masque ;
- **correction d'un premier contrôle** : la première version mélangeait aussi la **validation** ;
  les deux pertes étaient **identiques**, ce qui l'a révélé. Corrigé, le contrôle garde la
  validation alignée et discrimine ;
- **dry-run** : l'adaptateur, le corpus professeur et la distillation ont un mode hors réseau ;
  `porte-deepseek` est **verte hors réseau** (**20 tests**, dry-run, 60 et 310 prompts, distillation ignorée) ;
- **secrets** : la clé n'est ni dans le dépôt, ni dans le cache, ni dans les erreurs ; elle est lue
  par `DEEPSEEK_API_KEY` / `DSH_API_KEY` ou un fichier `0600` (`*_KEY_FILE`).

## 4. Ce qui pourrait rendre ce résultat faux

- **Un seul modèle, une seule version** : `deepseek-flash` peut changer ; la mesure est datée.
- **Trente articles, dix langues** : c'est mieux que cinq, mais ce n'est pas un corpus de traduction
  général ; le hindi et le swahili restent bas.
- **chrF n'est pas un juge** : il mesure des n-grammes de caractères, pas le sens ; une paraphrase
  correcte peut baisser, une traduction littérale peut monter.
- **310 exemples de distillation** : le corpus reste petit ; 39 exemples de validation ; le seuil
  de capacité est mesuré entre **4,04 M** (négatif) et **10,70 M** (positif), pas au-delà ; le
  point exact n'est pas localisé.
- **La perte inclut les prompts** : le modèle apprend surtout la **distribution des réponses** ;
  c'est peut-être pourquoi le contrôle mélangé fait aussi bien. Une perte **masquée sur les
  prompts** est la prochaine expérience, avec un modèle plus grand.
- **Les réponses du professeur sont des données** : la licence autorise l'entraînement, mais le
  corpus n'est pas versionné (`data/` est gitignoré) ; seules ses empreintes SHA-256 sont dans les
  JSON.

## 5. Ce que ça n'autorise pas à dire

- que DeepSeek **remplace** les mesures d'états internes : il n'a ni poids ni activations ;
- que la distillation **marche** en général : elle est **négative à 4,04 M**, **positive à 10,70 M,
  16,02 M et 22,54 M** sur ce corpus ; le seuil est mesuré, pas expliqué ;
- que la qualité de traduction est **uniforme** : hindi et swahili sont bas ;
- que Qwen est **inutile** : il reste une **référence blanche** pour les portes historiques, tant
  que `route` ne les reprend pas.

## 6. Les fichiers

- adaptateur : [`tools/llm/deepseek.py`](../tools/llm/deepseek.py) ;
- prompts publics : [`prompts_publics.jsonl`](../tools/llm/prompts_publics.jsonl) (60) et
  [`prompts_publics_300.jsonl`](../tools/llm/prompts_publics_300.jsonl) (310), générés par
  [`prompts_publics.py`](../tools/llm/prompts_publics.py) ;
- corpus professeur : [`enseignant.py`](../tools/llm/enseignant.py) ; distillation :
  [`distillation.py`](../tools/llm/distillation.py) ; perte masquée :
  [`masque.py`](../tools/llm/masque.py), [`entrainer_masque.py`](../tools/llm/entrainer_masque.py) ;
  mesure : [`mesure.py`](../tools/llm/mesure.py) ;
- tests : [`tools/llm/tests/`](../tools/llm/tests/) (**20 tests**) ;
- porte : [`tools/porte-deepseek.sh`](../tools/porte-deepseek.sh) ;
- JSON : [`deepseek-mesures.json`](deepseek-mesures.json),
  [`deepseek-mesures-300.json`](deepseek-mesures-300.json),
  [`deepseek-natif-300.json`](deepseek-natif-300.json) ;
- données (gitignorées) : `data/deepseek/enseignant.jsonl` (60, SHA-256 `9989da0b…`),
  `data/deepseek/enseignant-300.jsonl` (310, SHA-256 `33e54aa6…`),
  `data/deepseek/distillation-300/` (271/39), `data/deepseek/distillation-300-controle/`.

## 7. La ligne de roadmap

**B9** — le banc externe et l'élève natif ; voir [`docs/roadmap.md`](../docs/roadmap.md).
B9.1 (adaptateur et porte) et B9.2 (corpus professeur, 310 prompts) sont mesurés ; B9.3
(distillation) est **négatif à 4,04 M**, **positif à 10,70 M, 16,02 M et 22,54 M** (3/3 graines,
1,65–1,92 %) et la perte masquée est **non concluante** ; B9.4 (répartition GPU/CPU) est **décidé** :
DeepSeek pour le langage, GPU pour `route` et les mesures blanches.
