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

1. **Prompts publics** : 50 traductions de cinq articles de l'UDHR vers dix langues, 10 questions de
   jeux (`tools/llm/prompts_publics.jsonl`).
2. **Corpus professeur** : les réponses de `deepseek-flash` (JSONL, cache, tokens, latence) ;
   `tools/llm/enseignant.py`.
3. **Mesure** : chrF contre la traduction humaine officielle, avec le **plancher** source→référence ;
   `tools/llm/mesure.py`.
4. **Distillation** : découpage train/val **par identifiant**, texte byte-level pour
   `entrainer_moteur.py` ; `tools/llm/distillation.py`.
5. **Élève natif** : `route` sur GPU, export GGUF, PPL/flux par le moteur.

## Ce que la première mesure donne

- **60/60** prompts servis par `deepseek-flash` ; 5 552 tokens d'entrée, 10 857 de sortie, 135,1 s,
  2,252 s par requête.
- **chrF 82,48** contre un **plancher de 15,29** sur 50 traductions ; l'espagnol, l'allemand, le
  russe, le français et le chinois sont au-dessus de 87 ; le **hindi (56,17)** et le **swahili
  (46,89)** sont les négatifs nommés.
- **Élève natif** : `route` 4,04 M paramètres, `cuda`, 50 pas sur le corpus professeur ; aligné
  **3,8191** bits/octet contre mélangé **3,8361** sur trois graines — **0,44 %**, signes mitigés. À
  60 exemples, la distillation **n'est pas établie** : c'est un smoke test de pipeline.

## Les secrets et le cache

- clé : `DEEPSEEK_API_KEY` ou `DSH_API_KEY`, ou un fichier `0600` pointé par `DEEPSEEK_KEY_FILE` /
  `DSH_KEY_FILE` ; **jamais** dans le dépôt, le cache ou un message d'erreur ;
- endpoint/modèle : `DEEPSEEK_BASE_URL` / `DSH_BASE_URL`, `DEEPSEEK_MODEL` / `DSH_MODEL` ;
- cache : `data/deepseek/cache/<sha256>.json` (gitignoré), clé = modèle + messages + température +
  max_tokens, jamais la clé ;
- `--dry-run` : aucune requête, réponse déterministe ; la porte est **verte hors réseau**.

## Ce qui reste ouvert

- **la distillation à l'échelle** : 60 exemples ne suffisent pas ; il faut 300+ prompts, plus de pas
  et plusieurs graines ;
- **la qualité par langue** : hindi et swahili sont bas ; un juge humain ou un chrF par famille ne
  remplacent pas cinq articles ;
- **le modèle** : `deepseek-flash` peut changer ; la mesure est datée ;
- **les états internes** : DeepSeek ne les donne pas ; le natif reste seul pour cette mesure.

## Où vit le code

| module | rôle |
|---|---|
| [`tools/llm/deepseek.py`](../tools/llm/deepseek.py) | client API, cache, dry-run, clé par fichier |
| [`tools/llm/prompts_publics.jsonl`](../tools/llm/prompts_publics.jsonl) | 60 prompts publics |
| [`tools/llm/enseignant.py`](../tools/llm/enseignant.py) | corpus professeur |
| [`tools/llm/mesure.py`](../tools/llm/mesure.py) | chrF, plancher, tokens, latence |
| [`tools/llm/distillation.py`](../tools/llm/distillation.py) | train/val par identifiant, contrôle par permutation |
| [`tools/porte-deepseek.sh`](../tools/porte-deepseek.sh) | la porte hors réseau (16 tests, dry-run) |

**Vocabulaire** : le **professeur** est l'API ; l'**élève** est `route` ; la **distillation** est au
niveau des séquences, puisque l'API ne donne pas les logits. Voir la roadmap **B9**.
