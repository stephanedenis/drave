# Session bbc0b8e2 — Avis sur le dépôt GitHub Strata

| | |
|---|---|
| Identifiant | `bbc0b8e2-1c7f-4d43-b1e5-7b7b72bd6ccf` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-12 08:44 |
| Durée | 0.1 h |
| Tours | 2 |
| Messages | 22 |
| Appels d'outils | 32 |
| Fichiers touchés | 1 |
| Commandes | 8 |
| Sous-agents | 0 |
| Commits | 2 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — que penses-tu de https://github.com/Niko1221/Strata

**Tour 2** — ok, à suivre et on adopte les bonnes idées.

## 2. Déroulé, étape par étape

### Tour 1 — que penses-tu de https://github.com/Niko1221/Strata

*8 appels d'outils.* Actions notables :

- web_fetch
- web_search
- bash — List workspace and preview local README

**Synthèse produite :**

⏵ Rédaction de mon avis technique sur Strata, en regard de Drave

Voici ce que j'en pense, en séparant le fond technique, la santé du projet, et ce que ça dit pour **Drave** (ton moteur, qui attaque le même problème par un autre bout).

\## Le fond : c'est sérieux, et bien pensé

Strata fait tourner un MoE de 125 B (24 576 experts, ~10 actifs par token) sur une carte de 12 Go + 32-64 Go de RAM. L'architecture décrite dans [docs/HOW_IT_WORKS.md](https://github.com/Niko1221/Strata/blob/main/docs/HOW_IT_WORKS.md) est cohérente, pas magique :

- **Cache d'experts sur GPU qui apprend en cours de conversation** (profil de routage précalculé + adaptation), CPU qui calcule *en place* les experts manquants **en parallèle** du GPU au lieu d'attendre — c'est le vrai gain par rapport à un simple offload façon `--n-cpu-moe`.
- **Prefill par gros morceaux (8 192 tokens)** avec préchargement PCIe des experts de la couche suivante pendant que l'attention courante tourne.
- **Décodage spéculatif MTP** (la couche draft du modèle, 2,4-3,2 tokens acceptés par passe) + prompt-lookup *uniquement là où l'acceptation mesurée le justifie*. Le fait qu'ils désactivent le lookup quand il ne paie pas est un bon signe d'honnêteté.
- MIT, basé sur ggml/llama.cpp, crédits explicites (ISTA-DASLab, Unsloth, Splash, ninfer…).

C'est la lignée ktransformers / llama.cpp expert-offload, mais avec une ingénierie d'intégration nettement supérieure.

\## Le vrai tour de force : l'emballage

22 278 étoiles, 2 150 forks, **en ~18 jours** ([API repo](https://api.github.com/repos/Niko1221/Strata)). Ce n'est pas la technique qui a fait ça, c'est :

- un installeur double-clic (`START-HERE.bat` / `setup.sh`), un `BENCH` qui produit un rapport partageable ;
- **API OpenAI + Anthropic + Responses** sur localhost → Claude Code, Codex, Cursor marchent sans patch ;
- un **serveur MCP** pour que les agents installent/pilotent le moteur ;
- une doc en 7 langues, écrite pour des non-techniciens, avec les échecs nommés (« ça gèle au premier démarrage, c'est normal », « ton disque clignote = pas assez de RAM »).

C'est exactement ce qui transforme un moteur en adoption de masse.

\## Les réserves, et elles sont réelles

1. **Maturité.** 803 issues ouvertes, énormément de PR communautaires non mergées, `health_percentage` 71 % (pas de CONTRIBUTING, pas de templates d'issue). Plusieurs contributeurs mentionnent des **force-push / réécritures d'historique** ayant fermé leurs PR ([#1307](https://github.com/Niko1221/Str
… [3444 caractères tronqués]

### Tour 2 — ok, à suivre et on adopte les bonnes idées.

*24 appels d'outils.* Actions notables :

- read
- bash — Read clock, recent commits, journal tail
- grep
- bash — Read clock and check for existing note
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/strata-pour-drave.md`
- bash — Inspect git status and pre-commit hook
- bash — Commit the new note
- bash — List local models and check binary
- bash — Check commit state and stale processes
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/strata-pour-drave.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/strata-pour-drave.md`
- bash — Commit note in background
- job_output

**Synthèse produite :**

⏵ J'attends le commit et je relis la note finale

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/strata-pour-drave.md` | 1 | 2 |

### Commandes exécutées (échantillon)

- **T1** List workspace and preview local README
- **T2** Read clock, recent commits, journal tail
- **T2** Read clock and check for existing note
- **T2** Inspect git status and pre-commit hook
- **T2** Commit the new note
- **T2** List local models and check binary
- **T2** Check commit state and stale processes
- **T2** Commit note in background

## 4. Mesures et résultats marquants

- **T2** `[timed out after 60000ms]`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T2** : M journal/sessions/MANIFEST.md  M journal/sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/digest.md  M journal/sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/rapport.md ?? docs/strata-pour-drave.md --- h

## 6. Commits

- Docs : strata-pour-drave — S1-S6, M5 change de cahier des charges (le brouillon est une couche de la cible), S4 (prechargement ordonne) en premiere action" && g
- Docs : strata-pour-drave — S1-S6 ; M5 change de cahier des charges (le brouillon est une couche de la cible, V4.1 declare dspark_* 37-39), S4 (prechargement ord

