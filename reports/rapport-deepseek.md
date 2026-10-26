# B9 — DeepSeek pour le langage, GPU pour le modèle natif

> Mesure du **26/10/2026**, sur `Hauru` (2 × RTX 5000 16 Go, Python 3.13) et l'API
> **`deepseek-flash`** (licence du propriétaire ; distillation et entraînement explicitement autorisés).
> La question : le **langage** peut-il sortir des GPU, et les GPU revenir au **modèle natif**
> `route` / `drave-core` ? JSON : [`deepseek-mesures.json`](deepseek-mesures.json). Code :
> [`tools/llm/`](../tools/llm/), porte [`tools/porte-deepseek.sh`](../tools/porte-deepseek.sh).

## Ce qui est mesuré

1. **Le banc externe** : 60 prompts publics (50 traductions de cinq articles de la Déclaration
   universelle des droits de l'homme vers dix langues, 10 questions de jeux), envoyés à
   `deepseek-flash` ; qualité **chrF** contre la traduction humaine officielle, avec le
   **plancher** source→référence, tokens, latence, cache.
2. **L'élève natif** : le corpus professeur est converti en `train/val` par identifiant, puis
   `route` (4,04 M paramètres, architecture du moteur) est entraîné sur **GPU** (`cuda`).
3. **Le contrôle de distillation** : mêmes prompts, réponses d'entraînement **mélangées**,
   validation **alignée** ; trois graines. Si l'élève aligné ne bat pas le mélangé, la
   distillation n'est **pas** établie.

## 1. Le banc DeepSeek

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

### La qualité des traductions

chrF (n-grammes de caractères, β = 2) contre la traduction humaine UDHR ; le **plancher** est le
même chrF entre la source anglaise et la référence, c'est-à-dire ce que vaut une **non-traduction**.

| langue | n | chrF | plancher | écart |
|---|---:|---:|---:|---:|
| espagnol | 5 | **99,90** | 28,11 | +71,79 |
| allemand | 5 | **99,42** | 22,37 | +77,05 |
| russe | 5 | **99,35** | 2,85 | +96,50 |
| français | 5 | **98,49** | 28,14 | +70,35 |
| chinois mandarin | 5 | **87,70** | 0,19 | +87,51 |
| portugais | 5 | **82,11** | 25,67 | +56,44 |
| italien | 5 | **81,92** | 25,79 | +56,13 |
| arabe | 5 | **72,86** | 2,69 | +70,17 |
| hindi | 5 | **56,17** | 2,94 | +53,23 |
| swahili | 5 | **46,89** | 14,18 | +32,71 |
| **moyenne** | **50** | **82,48** | **15,29** | **+67,19** |

Le plancher dépend de la proximité des écritures : il est haut pour l'espagnol, l'allemand, le
français, le portugais et l'italien, bas pour le russe, l'arabe, le chinois et le hindi. Le
**chrF brut n'est donc pas comparable entre langues** ; c'est l'**écart au plancher** qui dit que
le professeur traduit. Les deux langues les plus basses, **hindi (56,17)** et **swahili (46,89)**,
sont un **négatif nommé** : la licence et le modèle ne garantissent pas la parité.

## 2. L'élève natif sur GPU

Le corpus professeur (60 exemples) est découpé par **identifiant** : **50 train / 10 val**,
48 413 / 12 392 caractères. Le modèle `route` a **4,04 M paramètres** (dim 192, 4 couches,
8 experts, k = 2) ; l'entraînement tourne sur **`cuda`**, 50 pas en **3–4 s**.

| entraînement | graine | val (bits/octet) |
|---|---:|---:|
| réponses **alignées** | 1 | **3,7847** |
| réponses **alignées** | 2 | **3,8092** |
| réponses **alignées** | 3 | **3,8635** |
| réponses **mélangées** (contrôle) | 1 | **3,8530** |
| réponses **mélangées** (contrôle) | 2 | **3,8236** |
| réponses **mélangées** (contrôle) | 3 | **3,8316** |

Moyennes : **aligné 3,8191**, **mélangé 3,8361** — un écart de **0,017 bit/octet** (0,44 %).
Les signes sont **mitigés** : l'aligné gagne 2 graines sur 3, le mélangé gagne la troisième. À
**60 exemples**, **50 pas** et **4,04 M paramètres**, la distillation n'est **pas établie** : c'est
un **smoke test de pipeline**, pas un résultat de transfert. Le contrôle fait son travail : il
interdit de conclure sur une graine favorable.

Le **modèle natif** a aussi été essayé sur le corpus public (`data/corpus_en.txt`, 20 pas) :
**4,04 M paramètres**, **`cuda`**, val **4,4150** bits/octet. Ce n'est pas une mesure de qualité,
c'est la preuve que la chaîne GPU → modèle → export fonctionne sans Qwen.

## 3. Les contrôles

- **plancher chrF** : source→référence, 15,29 en moyenne ; sans lui, 82,48 ne veut rien dire ;
- **permutation des réponses d'entraînement** : mêmes prompts, réponses mélangées, validation
  **alignée**, trois graines ; l'écart moyen est de 0,44 %, avec des signes mitigés ;
- **dry-run** : l'adaptateur, le corpus professeur et la distillation ont un mode hors réseau ;
  `porte-deepseek` est **verte hors réseau** (16 tests, dry-run, 60 prompts, distillation ignorée) ;
- **secrets** : la clé n'est ni dans le dépôt, ni dans le cache, ni dans les erreurs ; elle est lue
  par `DEEPSEEK_API_KEY` / `DSH_API_KEY` ou un fichier `0600` (`*_KEY_FILE`).

## 4. Ce qui pourrait rendre ce résultat faux

- **Un seul modèle, une seule version** : `deepseek-flash` peut changer ; la mesure est datée.
- **Cinq articles par langue** : la moyenne par langue porte sur **5** phrases ; le hindi et le
  swahili sont fragiles.
- **chrF n'est pas un juge** : il mesure des n-grammes de caractères, pas le sens ; une paraphrase
  correcte peut baisser, une traduction littérale peut monter.
- **60 exemples de distillation** : le corpus est **trop petit** pour conclure ; les 10 exemples de
  validation sont eux-mêmes peu nombreux.
- **4,04 M paramètres** : `route` est un petit modèle byte-level ; la distillation à cette échelle
  ne dit rien de ce qu'un modèle plus grand apprendrait.
- **Les réponses du professeur sont des données** : la licence autorise l'entraînement, mais le
  corpus n'est pas versionné (`data/` est gitignoré) ; seule son empreinte SHA-256 est dans le JSON.

## 5. Ce que ça n'autorise pas à dire

- que DeepSeek **remplace** les mesures d'états internes : il n'a ni poids ni activations ;
- que la distillation **marche** : à 60 exemples, le contrôle ne la distingue pas ;
- que la qualité de traduction est **uniforme** : hindi et swahili sont bas ;
- que Qwen est **inutile** : il reste une **référence blanche** pour les portes historiques, tant
  que `route` ne les reprend pas.

## 6. Les fichiers

- adaptateur : [`tools/llm/deepseek.py`](../tools/llm/deepseek.py) ;
- prompts publics : [`tools/llm/prompts_publics.jsonl`](../tools/llm/prompts_publics.jsonl)
  (60 prompts, générés par [`prompts_publics.py`](../tools/llm/prompts_publics.py)) ;
- corpus professeur : [`enseignant.py`](../tools/llm/enseignant.py) ; distillation :
  [`distillation.py`](../tools/llm/distillation.py) ; mesure :
  [`mesure.py`](../tools/llm/mesure.py) ;
- tests : [`tools/llm/tests/`](../tools/llm/tests/) (**16 tests**) ;
- porte : [`tools/porte-deepseek.sh`](../tools/porte-deepseek.sh) ;
- JSON : [`deepseek-mesures.json`](deepseek-mesures.json) ;
- données (gitignorées) : `data/deepseek/enseignant.jsonl` (60 réponses, SHA-256
  `9989da0b…`), `data/deepseek/distillation/` (50/10), `data/deepseek/distillation-controle/`.

## 7. La ligne de roadmap

**B9** — le banc externe et l'élève natif ; voir [`docs/roadmap.md`](../docs/roadmap.md).
B9.1 (adaptateur et porte) et B9.2 (corpus professeur, 60 prompts) sont mesurés ; B9.3
(distillation) est un **smoke test négatif** à cette échelle ; B9.4 (répartition GPU/CPU) est
**décidé** : DeepSeek pour le langage, GPU pour `route` et les mesures blanches.
