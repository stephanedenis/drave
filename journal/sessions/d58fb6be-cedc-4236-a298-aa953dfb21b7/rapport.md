# Session d58fb6be — Tu es dans /home/stephane/Data13TB/steph

> **Journaux :** [le jour](../../2026-10-29/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `d58fb6be-cedc-4236-a298-aa953dfb21b7` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-29 22:25 |
| Durée | 0.5 h |
| Tours | 1 |
| Messages | 40 |
| Appels d'outils | 54 |
| Fichiers touchés | 0 |
| Commandes | 42 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (dépôt Drave, Python + Rust). Tâche de RECHERCHE/PLAN, sans modifier en-cours/roadmap/AGENTS et sans commit.  Objectif R13.1 : entraîner un petit modèle natif BPE et comparer bits/octet au modèle octets. Lis tools/native_model.py (NativeConfig, NativeModel, exporter_drvm), tools/entrainer_native.py, tools/corpus_natif.py, tools/generer_nat … [1218 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (dépôt Drave, Python + Rust). Tâche de RECHERCHE/PLAN, sans m … [1498 caractères tronqués]

*54 appels d'outils.* Actions notables :

- bash — List and count lines of target files
- bash — List data directory and corpora
- read
- bash — Inspect python envs and tokenizer packages
- bash — Check GPU and git status
- bash — Check PATH, venv, pip list
- bash — List tools and find BPE-related scripts
- bash — Find how gpu-env python is invoked
- bash — Read vdc and find native trainer references
- bash — Inspect R13 artefacts and checkpoints
- bash — Read native training result JSONs
- bash — Find tokenizer library usage and artifacts
- bash — Count parameters per vocab size
- bash — Check drvm and Rust engine for 256 assumptions
- … et 30 autres

**Synthèse produite :**

⏵ Synthèse finale

**A

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List and count lines of target files
- **T1** List data directory and corpora
- **T1** Inspect python envs and tokenizer packages
- **T1** Check GPU and git status
- **T1** Check PATH, venv, pip list
- **T1** List tools and find BPE-related scripts
- **T1** Find how gpu-env python is invoked
- **T1** Read vdc and find native trainer references
- **T1** Inspect R13 artefacts and checkpoints
- **T1** Read native training result JSONs
- **T1** Find tokenizer library usage and artifacts
- **T1** Count parameters per vocab size
- **T1** Check drvm and Rust engine for 256 assumptions
- **T1** Check tokenizer coupling in engine and native scripts
- **T1** Validate UTF-8 corpora and count CPUs
- **T1** Train in-memory BPE and measure bytes/token
- **T1** Verify reversibility and batch encode speed
- **T1** Benchmark training step time by vocab and seq
- **T1** Check RAM and corpus loading cost
- **T1** Read corpus budget report and ppl baseline
- **T1** Find tests on native model
- **T1** Check which gates run native code
- **T1** Search for bits-per-byte precedent
- **T1** Check old checkpoint compatibility
- **T1** Find bits/byte formula implementations
- **T1** Read bits/byte precedent in entrainer_moteur
- **T1** Compute iso-parameter configurations
- **T1** Confirm hardcoded reshape failure mode
- **T1** Run in-memory pilot comparing bits/byte
- **T1** Recompute bytes per token with three methods
- **T1** Clean bytes/token and corrected pilot
- **T1** Exhaustive 256/bytes assumptions in native tools
- **T1** Check timestamps and git status of new file
- **T1** Find recently created files and gitignore status
- **T1** Check R13.1 artifact timestamps and git index flags
- **T1** Read R13.1 JSON and gate script
- **T1** Quantify global-ratio bias on published bits/byte
- **T1** Check for durable BPE artifacts
- **T1** Check R13.1 status in roadmap and state
- **T1** Inspect BPE checkpoint JSON and DRVM manifest
- … et 2 autres

## 4. Mesures et résultats marquants

- **T1** `drave-core/src/engine.rs:287:/// 256 Ko. S'en servir ne coûte pas grand-chose, mais les compter fait prendre`
- **T1** `data/corpus_fr_train.txt     vocab   512 · train    1.1 s ·  117,599 jetons · 1.89 o/jeton · enc   1.4 Mo/s · reversible=False · vocab_reel=512`
- **T1** `data/corpus_fr_train.txt     vocab  1024 · train    1.2 s ·   93,147 jetons · 2.39 o/jeton · enc   1.2 Mo/s · reversible=False · vocab_reel=1024`
- **T1** `data/corpus_en.txt           vocab   512 · train    2.2 s · 1,050,385 jetons · 1.90 o/jeton · enc   1.2 Mo/s · reversible=False · vocab_reel=512`
- **T1** `data/corpus_en.txt           vocab  1024 · train    2.8 s ·  860,600 jetons · 2.32 o/jeton · enc   1.0 Mo/s · reversible=False · vocab_reel=1024`
- **T1** `data/corpus_fr_train.txt v  512 | train   0.4s | 1.59 o/jeton | enc   5.0 Mo/s | reversible=True`
- **T1** `data/corpus_fr_train.txt v 1024 | train   0.6s | 1.85 o/jeton | enc   5.6 Mo/s | reversible=True`
- **T1** `data/corpus_fr_train.txt v 2048 | train   0.7s | 2.08 o/jeton | enc   6.1 Mo/s | reversible=True`
- **T1** `data/corpus_en.txt       v  512 | train   1.6s | 1.88 o/jeton | enc   7.8 Mo/s | reversible=True`
- **T1** `data/corpus_en.txt       v 1024 | train   2.0s | 2.29 o/jeton | enc   8.2 Mo/s | reversible=True`
- **T1** `data/corpus_en.txt       v 2048 | train   2.3s | 2.68 o/jeton | enc   8.1 Mo/s | reversible=True`
- **T1** `vocab  256 seq 128 lot 8 :   35.6 ms/pas ·   5.9 min pour 10k pas ·  28.7k jetons/s`
- **T1** `vocab  256 seq 256 lot 8 :   41.3 ms/pas ·   6.9 min pour 10k pas ·  49.5k jetons/s`
- **T1** `vocab 1024 seq 128 lot 8 :   42.3 ms/pas ·   7.1 min pour 10k pas ·  24.2k jetons/s`
- **T1** `vocab 1024 seq 256 lot 8 :   43.3 ms/pas ·   7.2 min pour 10k pas ·  47.3k jetons/s`
- **T1** `/dev/mapper/system-root   11T  8,9T  2,0T  82% /home/stephane/Data13TB`
- **T1** `--- temps list(b) sur 20 Mo`
- **T1** `list(b)  20 Mo : 2.1 s · 20,000,000 ids`
- **T1** `frombuffer 20 Mo: 0.03 s · identique=True`
- **T1** `- **Un seul corpus**, français, 4,63 Mo.`
- **T1** `./reports/archive/rapport-campagne-benefices.md:437:| dim | dense (val, bits/octet) | routé (val) | gain du routage | PPL moteur (8 × 128) |`
- **T1** `./reports/archive/rapport-campagne-benefices.md:461:| routé 512 | validation fp32 (bits/octet) | PPL moteur (8 × 128) | écart de quantification |`
- **T1** `./reports/campagne-benefices/008-05-les-modeles-entraines-ici-mesures-dans-l.md:68:| dim | dense (val, bits/octet) | routé (val) | gain du routage | PPL moteur (8 × 128) |`
- **T1** `./reports/campagne-benefices/008-05-les-modeles-entraines-ici-mesures-dans-l.md:92:| routé 512 | validation fp32 (bits/octet) | PPL moteur (8 × 128) | écart de quantification |`
- **T1** `à l'entraînement, perplexité 8 668 dans le moteur et **15 552** pour la référence`
- **T1** `vocab   512 {}                               : 12,448,136  ( +5.4 %)`
- **T1** `vocab   512 {'expert_hidden': 280}           : 12,189,320  ( +3.2 %)`
- **T1** `vocab  1024 {}                               : 13,714,824  (+16.1 %)`
- **T1** `vocab  1024 {'n_blocks': 5}                  : 11,727,008  ( -0.7 %)`
- **T1** `vocab  1024 {'d_model': 216}                 : 13,179,712  (+11.6 %)`
- **T1** `vocab  1024 {'expert_hidden': 256}           : 12,679,560  ( +7.3 %)`
- **T1** `delta   : -0.4465 bits/octet (-17.0 %) — a 1500 pas, 1 graine`
- **T1** `"controle": "mêmes graine/architecture/corpus ; octets 200→400 montre l'effet des données (3,818→3,689) ; BPE reste 11,9 % devant à octets égaux",`
- **T1** `"verdict": "le BPE natif gagne 11,9 % de bits/octet à budget d'octets égal",`
- **T1** `"le modèle BPE a 5,4 % de paramètres en plus"`
- **T1** `n_val 117,202 jetons · octets de la tranche val 229,366 (4.95 % du corpus)`
- **T1** `tokens/octet  global 0.505849 · tranche val 0.510982 (+1.01%)`
- **T1** `gain 11,9 % -> 11.0 % avec le ratio exact de la tranche`
- **T1** `0668ef4e R13.1 — LE BPE NATIF BAT L'OCTET : 3,249 CONTRE 3,689 BITS/OCTET, −11,9 % À OCTETS ÉGAUX`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : octets pas 500 · perte 2.5302 · 22s   octets pas 1000 · perte 2.0795 · 43s   octets pas 1500 · perte 1.8882 · 59s tokenizer 1024 : 0.6 s · vocab 1024 train 2.48 o/jeton · val 2.54 o/jeton   bpe1024 pa
- **T1** : ./reports/rapport-a80-portes-ppl.md ./reports/a80-porte-bus.json ./reports/rapport-a80-porte-bus.md ./reports/a80-porte-delais.json ./reports/rapport-a80-porte-delais.md ./reports/a80-porte-bus-socket

