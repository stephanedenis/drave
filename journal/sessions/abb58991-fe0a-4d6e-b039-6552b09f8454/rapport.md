# Session abb58991 — Reprise session L/B13 et mise à jour plan

> **Journaux :** [le jour](../../2026-11-02/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `abb58991-fe0a-4d6e-b039-6552b09f8454` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-02 16:15 |
| Durée | 0.4 h |
| Tours | 1 |
| Messages | 75 |
| Appels d'outils | 112 |
| Fichiers touchés | 6 |
| Commandes | 91 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu reprends la session L/B13 `e181ce02-cd50-488a-a6be-e84b79d40dcc`. Lis son plan, AGENTS.md  et docs/pilotage/en-cours.md. Remets `- **État** : actif` et `- **Heartbeat** : <maintenant>`  dans son plan, puis vérifie `python3 tools/sessions.py --check --strict`. Le cycle 140/140  (gold 432, 116 liens) est committé. Prochaine action : gold neuronal (qualifier un modèle  local) ; DRVM/native est blo … [114 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu reprends la session L/B13 `e181ce02-cd50-488a-a6be-e84b79d40dcc`. Lis son plan, AGENTS.md  et docs/pilotage/en-cours. … [394 caractères tronqués]

*112 appels d'outils.* Actions notables :

- bash — Show repo state and recent commits
- bash — List root and sessions tool help
- bash — List session dirs and locate the session id
- bash — Show session status
- read
- bash — Count lines of target docs
- bash — Get current local and Montreal time
- bash — Inspect heartbeat parsing and strict checks
- bash — Get fresh timestamp for heartbeat
- bash — Timestamp for the heartbeat
- edit `/home/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md`
- edit `/home/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md`
- bash — Run strict session plan check
- bash — Inspect the unlisted active plan
- … et 86 autres

**Synthèse produite :**

⏵ Test de la vraie `Cascade` avec un tagger cached à confiance 0,6 (POS résiduel)

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md` | 0 | 2 |
| `/tmp/qualif_proto.py` | 1 | 0 |
| `/tmp/qualif_proto_srv.py` | 1 | 0 |
| `/tmp/qualif_proto_srv2.py` | 1 | 0 |
| `/tmp/qualif_7b.py` | 1 | 0 |
| `/tmp/qualif_7b_180.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Show repo state and recent commits
- **T1** List root and sessions tool help
- **T1** List session dirs and locate the session id
- **T1** Show session status
- **T1** Count lines of target docs
- **T1** Get current local and Montreal time
- **T1** Inspect heartbeat parsing and strict checks
- **T1** Get fresh timestamp for heartbeat
- **T1** Timestamp for the heartbeat
- **T1** Run strict session plan check
- **T1** Inspect the unlisted active plan
- **T1** Status and references of the extra session
- **T1** Check git status and file mtimes
- **T1** Inspect newly created session dirs
- **T1** Inspect uncommitted changes
- **T1** List active DSH/gate processes
- **T1** Search hub digest for N2 integration
- **T1** List pensee tools and gold reports
- **T1** Look for local models and taggers
- **T1** Re-run strict check after concurrent integration
- **T1** Find neuronal refusal details in gold report
- **T1** Inspect linguistic test scripts
- **T1** Read neuronal refusal section
- **T1** Read NeuronalLLM adapter code
- **T1** Smoke-test llama-cli with local Qwen model
- **T1** Check llama-cli version and options
- **T1** Check GPU and CPU resources
- **T1** Test llama-cli single-turn generation
- **T1** List ollama and heavy model manifest
- **T1** Check grammar/JSON options in llama-cli
- **T1** Find local GGUF models
- **T1** Re-check strict status and git state
- **T1** Inspect gold JSON structure
- **T1** Test exact prompt with JSON constraint
- **T1** Test exact prompt single-turn without grammar
- **T1** Smoke-test Qwen3-0.6B local model
- **T1** Check installed NLP libraries
- **T1** Look for installed spaCy/stanza models
- **T1** Inspect eval entry points
- **T1** Find B13/R0.7 backlog cards
- … et 51 autres

## 4. Mesures et résultats marquants

- **T1** `3510:- Vérifie `nvidia-smi` avant N2 : les deux cartes sont saines (1 Mio, 0 %), mais l'incident est récent.`
- **T1** `> **1,0/1,0/0,994/0,889**, cascade **67,1 %**, **attachement par tête couverture 1,0 / top-1 0,957 / top-k 1,0** (span 0,323/0,338), hasard 0,015 ; **36 cibles ambiguës annotées en double lecture**. ⚠`
- **T1** `couvre **67,1 %** du texte en unités sémantiques.`
- **T1** `- **L'attachement par tête couvre 100 %**, mais le gold ne donne **qu'une** lecture des`
- **T1** `ambiguïtés (le GP au verbe) ; le 40 % des réels est un **désaccord de lecture**, pas seulement`
- **T1** `Quadro RTX 5000, 1 MiB, 0 %`
- **T1** `[still running after 60000ms; moved to background job bash-38]`
- **T1** `/dev/mapper/system-root   11T  9,0T  2,0T  83% /home/stephane/Data13TB`

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : Error: could not connect to ollama server, run 'ollama serve' to start it --- total 1656188 drwxr-xr-x. 1 stephane stephane       138 15 oct 09:02 . drwxr-xr-x. 1 stephane stephane       100 15 oct 09
- **T1** : > Tu es un étiqueteur linguistique. Réponds UNIQUEMENT par un objet JSON valide, sans texte autour. Schéma : {"langue":"fr","script":"Latn","etiquettes":[{"niveau":"phrase|pragmatique|syntagme|pos","t
- **T1** : Error: Failed to initialize samplers: std::exception  [ Prompt: 0,0 t/s | Generation: 0,0 t/s ]   Exiting... EXIT=0

