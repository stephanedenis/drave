# Session bbc0b8e2 — Avis sur le dépôt GitHub Strata

| | |
|---|---|
| Identifiant | `bbc0b8e2-1c7f-4d43-b1e5-7b7b72bd6ccf` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-12 08:44 |
| Durée | 0.2 h |
| Tours | 2 |
| Messages | 38 |
| Appels d'outils | 52 |
| Fichiers touchés | 2 |
| Commandes | 21 |
| Sous-agents | 0 |
| Commits | 3 |
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

*44 appels d'outils.* Actions notables :

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
- bash — Check mounts and locate large GGUF files
- … et 16 autres

**Synthèse produite :**

⏵ Je commite la fiche et la note, et je te demande quel chantier ouvrir

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/strata-pour-drave.md` | 1 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-v41-couches-brouillon.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** List workspace and preview local README
- **T2** Read clock, recent commits, journal tail
- **T2** Read clock and check for existing note
- **T2** Inspect git status and pre-commit hook
- **T2** Commit the new note
- **T2** List local models and check binary
- **T2** Check commit state and stale processes
- **T2** Commit note in background
- **T2** Check mounts and locate large GGUF files
- **T2** Locate any large GGUF and see disk usage
- **T2** Search Data13TB properly for models
- **T2** List model inventory and tool usage
- **T2** Read V4.1 dspark keys and draft tensors
- **T2** Find config key and test tensors listing
- **T2** Check core dump and extract dspark config keys
- **T2** List draft-layer tensors in V4.1 and check K3
- **T2** Verify draft layers present in V4.1 and K3 config
- **T2** Check MTP head tensors and K3 metadata keys
- **T2** Sum draft layer weights and confirm K3 config presence
- **T2** List distinct metadata keys for K3 and V4.1
- **T2** Commit report and note update

## 4. Mesures et résultats marquants

- **T2** `[timed out after 60000ms]`
- **T2** `/dev/nvme1n1p2           828G  801G   27G  97% /`
- **T2** `efivarfs                 256K  103K  149K  41% /sys/firmware/efi/efivars`
- **T2** `none                     1,0M     0  1,0M   0% /run/credentials/systemd-journald.service`
- **T2** `/dev/nvme1n1p2           828G  801G   27G  97% /.snapshots`
- **T2** `/dev/nvme1n1p2           828G  801G   27G  97% /opt`
- **T2** `/dev/nvme1n1p2           828G  801G   27G  97% /home`
- **T2** `/dev/nvme1n1p2           828G  801G   27G  97% /root`
- **T2** `/dev/nvme1n1p2  828G  801G   27G  97% /`
- **T2** `deepseek41 · 1 fichiers · 1046 tenseurs · 365.70 Go de poids · en-têtes lus en 66.247237ms`
- **T2** `deepseek41 · 1 fichiers · 1046 tenseurs · 365.70 Go de poids · en-têtes lus en 66.605738ms`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T2** : M journal/sessions/MANIFEST.md  M journal/sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/digest.md  M journal/sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/rapport.md ?? docs/strata-pour-drave.md --- h
- **T2** : === cles contenant config === deepseek41.config = {"architectures":["DeepseekV41ForCausalLM"],"bos_token_id":0,"dtype":"bfloat16","eos_token_id":1,"im === --tensors fonctionne-t-il sur ce fichier ? ==

## 6. Commits

- Docs : strata-pour-drave — S1-S6, M5 change de cahier des charges (le brouillon est une couche de la cible), S4 (prechargement ordonne) en premiere action" && g
- Docs : strata-pour-drave — S1-S6 ; M5 change de cahier des charges (le brouillon est une couche de la cible, V4.1 declare dspark_* 37-39), S4 (prechargement ord
- Rapport : le brouillon de V4.1 est dans le fichier (3 couches declarees, 75 tenseurs, 41 263 M poids) ; K3 n'en declare aucun (64 cles verifiees) — S1 de strata

