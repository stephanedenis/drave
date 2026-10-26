# Le banc externe — DeepSeek pour le langage, les GPU pour le natif

> **Décision du 26/10/2026.** Le langage (traduire, juger, générer, évaluer) sort des GPU et passe
> par l'API **DeepSeek** ; les 2 × RTX 5000 et les CPU restent au **modèle natif Drave** (`route`,
> `drave-core`) et aux mesures **boîte blanche** (perplexité, activations, flux, sondes). La
> licence autorise explicitement la **distillation** et l'**entraînement** à partir des sorties.
> Résultat : [`reports/rapport-deepseek.md`](../reports/rapport-deepseek.md).

## La séparation

| plan | qui | quoi | où |
|---|---|---|---|
| **langage, boîte noire** | DeepSeek API | traduction, jugements, génération, évaluation, lecture | réseau + cache local |
| **modèle natif, boîte blanche** | `route` + `drave-core` | entraînement, PPL, flux, sondes, rejeu | GPU et CPU locaux |
| **sémantique et jeux** | `tools/jeux` (B5–B8) | RSN, 71 langues, règles, recherche, maîtres | CPU, sans modèle |

**Ce que DeepSeek ne peut pas remplacer.** Une API ne donne ni les poids ni les activations : les
mesures qui font la thèse de Drave — perplexité, états internes, flux, top-k, rejeu — restent
locales. DeepSeek est un **professeur** et un **juge**, pas un banc d'états.

## Le pipeline

1. **Prompts publics** : 300 traductions de 30 articles de l'UDHR vers dix langues, 10 questions de
   jeux (`tools/llm/prompts_publics_300.jsonl`).
2. **Corpus professeur** : les réponses de `deepseek-flash` (JSONL, cache, tokens, latence) ;
   `tools/llm/enseignant.py`.
3. **Mesure** : chrF contre la traduction humaine officielle, avec le **plancher** source→référence ;
   `tools/llm/mesure.py`.
4. **Distillation** : découpage train/val **par identifiant**, texte byte-level pour
   `entrainer_moteur.py` ; `tools/llm/distillation.py`.
5. **Élève natif** : `route` sur GPU, export GGUF, PPL/flux par le moteur.

## Ce que la mesure donne

- **310/310** prompts servis par `deepseek-flash` ; 34 112 tokens d'entrée, 32 436 de sortie,
  511,1 s, 1,649 s par requête (60 cache).
- **chrF 82,82** contre un **plancher de 15,64** sur 300 traductions ; l'espagnol (99,28), le russe
  (98,86), le français (96,58), l'italien (92,87) et l'allemand (90,50) sont au-dessus de 90 ; le
  **hindi (58,45)** et le **swahili (54,83)** sont les négatifs nommés. Le pilote à 60 prompts
  surestimait l'allemand (99,42) et le chinois (87,70) : c'est le 30 articles qui fait foi.
- **Élève natif** : `route` de **4,04 M** à **22,54 M** paramètres, `cuda`, 310 exemples (271/39),
  500 pas, trois graines. À 4,04 M, le contrôle mélangé bat l'aligné (**2,7510** contre **2,7709**) ;
  à **9,23 M**, la moyenne penche pour l'aligné mais **1 graine/3** ; à **9,96 M**, **10,70 M**,
  **16,02 M**, **22,54 M** et **26,99 M**, l'aligné gagne 3/3 (1,76 %, 1,65 %, 1,92 %, 1,74 %,
  **2,93 %**). À **31,63 M**, 500 pas ne paient pas (0,27 %), 1 000 pas donnent 1,41 % (3/3) mais
  moins que le 27 M. La distillation a une **transition entre 9,23 M et 9,96 M** ; l'écart **croît**
  jusqu'à 27 M, puis la taille ne suffit plus. La **perte masquée calibrée** à 4,04 M est quasi égale
  (2,7335 contre 2,7340) : pas de gain établi.

## Les secrets et le cache

- clé : `DEEPSEEK_API_KEY` ou `DSH_API_KEY`, ou un fichier `0600` pointé par `DEEPSEEK_KEY_FILE` /
  `DSH_KEY_FILE` ; **jamais** dans le dépôt, le cache ou un message d'erreur ;
- endpoint/modèle : `DEEPSEEK_BASE_URL` / `DSH_BASE_URL`, `DEEPSEEK_MODEL` / `DSH_MODEL` ;
- cache : `data/deepseek/cache/<sha256>.json` (gitignoré), clé = modèle + messages + température +
  max_tokens, jamais la clé ;
- `--dry-run` : aucune requête, réponse déterministe ; la porte est **verte hors réseau**.

## Ce qui reste ouvert

- **la transition** : entre 9,23 M et 9,96 M ; il faut la resserrer (dim 232/6) et porter le masque
  dans le trainer pour une comparaison propre ;
- **la qualité par langue** : hindi et swahili sont bas ; un juge humain ou un chrF par famille ne
  remplacent pas cinq articles ;
- **le modèle** : `deepseek-flash` peut changer ; la mesure est datée ;
- **les états internes** : DeepSeek ne les donne pas ; le natif reste seul pour cette mesure.

## Où vit le code

| module | rôle |
|---|---|
| [`tools/llm/deepseek.py`](../tools/llm/deepseek.py) | client API, cache, dry-run, clé par fichier |
| [`tools/llm/prompts_publics.jsonl`](../tools/llm/prompts_publics.jsonl) | 60 prompts (pilote) et 310 (`prompts_publics_300.jsonl`) |
| [`tools/llm/enseignant.py`](../tools/llm/enseignant.py) | corpus professeur |
| [`tools/llm/mesure.py`](../tools/llm/mesure.py) | chrF, plancher, tokens, latence |
| [`tools/llm/distillation.py`](../tools/llm/distillation.py) | train/val par identifiant, contrôle par permutation |
| [`tools/porte-deepseek.sh`](../tools/porte-deepseek.sh) | la porte hors réseau (20 tests, dry-run) |

**Vocabulaire** : le **professeur** est l'API ; l'**élève** est `route` ; la **distillation** est au
niveau des séquences, puisque l'API ne donne pas les logits. Voir la roadmap **B9**.
