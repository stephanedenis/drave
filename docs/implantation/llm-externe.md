# Le banc externe — le professeur de langue, et l'élève natif

> **Décision du 26/10/2026.** Le **bloc de langue** (traduire, juger, générer, évaluer) reçoit son professeur et son
> juge de l'API **DeepSeek** ; les 2 × RTX 5000 et les CPU restent au **modèle natif** (`route`, `drave-core`) et aux
> mesures **boîte blanche** (perplexité, activations, flux, sondes). La licence autorise explicitement la
> **distillation** et l'**entraînement** à partir des sorties. Résultats :
> [`reports/rapport-deepseek.md`](../../reports/rapport-deepseek.md).

## La séparation

| plan | qui | quoi | où |
|---|---|---|---|
| **langue, boîte noire** | DeepSeek API | traduction, jugements, génération, évaluation, lecture | réseau + cache local |
| **natif, boîte blanche** | `route` + `drave-core` | entraînement, PPL, flux, sondes, rejeu | GPU et CPU locaux |
| **sémantique et jeux** | `tools/jeux` (B5–B8) | RSN, 71 langues, règles, recherche, maîtres | CPU, sans modèle |

**Ce que DeepSeek ne peut pas remplacer.** Une API ne donne ni les poids ni les activations : les mesures qui font la
thèse de Drave — perplexité, états internes, flux, top-k, rejeu — restent locales. DeepSeek est un **professeur** et
un **juge**, pas un banc d'états. C'est un **bloc externe** branché sur le bus : il rend du texte, pas des faits
internes.

## Le pipeline

1. **Prompts publics** : 300 traductions de 30 articles de l'UDHR vers dix langues, 10 questions de jeux ; extension
   à **610** (20 langues) et **910** (30 langues) pour la distillation.
2. **Corpus professeur** : les réponses de `deepseek-flash` (JSONL, cache, tokens, latence) ;
   `tools/llm/enseignant.py`.
3. **Mesure** : chrF contre la traduction humaine officielle, avec le **plancher** source→référence ;
   `tools/llm/mesure.py`.
4. **Distillation** : découpage train/val **par identifiant**, texte byte-level pour `entrainer_moteur.py` ;
   `tools/llm/distillation.py`.
5. **Élève natif** : `route` sur GPU, export vers le moteur, PPL/flux par `drave-core`.

## Ce que la mesure donne

| | |
|---|---|
| DeepSeek, 310 prompts | **310/310**, 34 112 / 32 436 tokens, 511,1 s, 1,649 s/requête |
| chrF, 310 | **82,82** contre un **plancher 15,64** |
| DeepSeek, extensions | **610/610** (20 langues) et **910/910** (30 langues), 0 échec |
| natif, 31,63 M / 610 | **4,40 %** (3/3) — le meilleur écart |
| natif, 610/20 | 3,71 % à 500 pas, **1,29 %** à 750, **−0,49 %** à 1 000 |
| natif, 910/30 | contrôle **+0,23 %** (1/3) : l'effet se dilue |
| masque calibré | 0,02 % à 4,04 M, 0,15 % à 10,70 M : pas de gain établi |

Les langues fortes sont l'espagnol, le russe, le français, l'italien et l'allemand ; l'hindi et le swahili restent
les négatifs nommés. Le **seuil** de capacité est une transition **9,23–9,96 M** ; la capacité ne paie **qu'avec les
données** (31,63 M / 310 : 0,27 % ; 31,63 M / 610 : 4,40 %).

## Les secrets et le cache

- clé : `DEEPSEEK_API_KEY` ou `DSH_API_KEY`, ou un fichier `0600` pointé par `DEEPSEEK_KEY_FILE` / `DSH_KEY_FILE` ;
  **jamais** dans le dépôt, le cache ou un message d'erreur ;
- endpoint/modèle : `DEEPSEEK_BASE_URL` / `DSH_BASE_URL`, `DEEPSEEK_MODEL` / `DSH_MODEL` ;
- cache : `data/deepseek/cache/<sha256>.json` (gitignoré), clé = modèle + messages + température + max_tokens ;
- `--dry-run` : aucune requête, réponse déterministe ; la porte est **verte hors réseau**.

## Ce qui reste ouvert

- **la fenêtre** : 500 pas est le point où le conditionnement se voit ; 750 et 1 000 l'effacent — il faut
  comprendre, pas seulement constater ;
- **la qualité par langue** : hindi et swahili sont bas ; un juge humain ou un chrF par famille ne remplacent pas
  cinq articles ;
- **le modèle** : `deepseek-flash` peut changer ; la mesure est datée ;
- **les états internes** : DeepSeek ne les donne pas ; le natif reste seul pour cette mesure.

## Où vit le code

| module | rôle |
|---|---|
| [`tools/llm/deepseek.py`](../../tools/llm/deepseek.py) | client API, cache, dry-run, clé par fichier |
| [`tools/llm/prompts_publics.jsonl`](../../tools/llm/prompts_publics.jsonl) | 60 prompts (pilote) et 310 (`prompts_publics_300.jsonl`) |
| [`tools/llm/enseignant.py`](../../tools/llm/enseignant.py) | corpus professeur |
| [`tools/llm/mesure.py`](../../tools/llm/mesure.py) | chrF, plancher, tokens, latence |
| [`tools/llm/distillation.py`](../../tools/llm/distillation.py) | train/val par identifiant, contrôle par permutation |
