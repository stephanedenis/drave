# Session 599e9c0e — Tu travailles dans /home/stephane/Data13

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `599e9c0e-4252-43ca-a89a-3886d723c379` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 21:13 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 11 |
| Appels d'outils | 22 |
| Fichiers touchés | 0 |
| Commandes | 15 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état de N2 et de sa porte** — lecture seule, aucun code.  Contexte : `docs/pilotage/roadmap.md` (chantier N2), `docs/pilotage/en-cours.md` (session N2), `reports/rapport-n2-*.md`, `tools/eval_n2_propre.py`, `tools/entrainer_native.py`, `tools/native_model.py`, `tools/porte-*.sh`. A23 a noté : « `tools/po … [1529 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état de N2 et de sa porte … [1809 caractères tronqués]

*22 appels d'outils.* Actions notables :

- bash — Afficher branche, derniers commits, racine
- glob
- read
- bash — Lister le répertoire models et tailles
- bash — Inventorier les checkpoints .pt dans work
- bash — Chercher N2 dans la roadmap
- bash — Chercher N2 dans en-cours
- bash — Trouver tous les checkpoints .pt du dépôt
- bash — Lister work/n2ac
- bash — Vérifier corpus propre et corpus annexes
- bash — Vérifier GPU et environnement python
- bash — Localiser le registre des portes
- bash — Chercher les usages de eval_n2_propre et porte-n2
- bash — Lire le registre des portes le plus récent
- … et 4 autres

**Synthèse produite :**

⏵ Inventaire des checkpoints N2 et de la porte propre

Je commence par explorer le dépôt : checkpoints, rapports N2, et les outils cités.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Afficher branche, derniers commits, racine
- **T1** Lister le répertoire models et tailles
- **T1** Inventorier les checkpoints .pt dans work
- **T1** Chercher N2 dans la roadmap
- **T1** Chercher N2 dans en-cours
- **T1** Trouver tous les checkpoints .pt du dépôt
- **T1** Lister work/n2ac
- **T1** Vérifier corpus propre et corpus annexes
- **T1** Vérifier GPU et environnement python
- **T1** Localiser le registre des portes
- **T1** Chercher les usages de eval_n2_propre et porte-n2
- **T1** Lire le registre des portes le plus récent
- **T1** Lire mesures et chaîne de la porte propre
- **T1** Lire métadonnées des checkpoints récents et l'état git
- **T1** Lire la chaîne et le log du checkpoint récent

## 4. Mesures et résultats marquants

- **T1** `36:| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art.,`
- **T1** `112:[N2] lasts 4 days and is 30% complete and is colored in #b26a00`
- **T1** `197:| **N2** | la distillation : corpus, professeur, [curriculum](../theorie/glossaire/entrees/curriculum.md) | 🔬 | **N2.h** — corpus dédupliqué (**0 %** de fuite) : la chaîne propre vaut **3,0904**, `
- **T1** `205:   jeu **contaminé à 32,8 %** — voir [N2.d](../../reports/rapport-n2-budget.md)) ; **N2.h3** montre que le`
- **T1** `96:- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propr`
- **T1** `131:**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+ ; **S** — poursuivre la validation ; **N4** — consigne ; **B10.3** — `z` ; **B13** `
- **T1** `137:- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `Quadro RTX 5000, 16384 MiB, 154 MiB, 2 %`
- **T1** `Quadro RTX 5000, 16384 MiB, 4 MiB, 0 %`
- **T1** `[still running after 60000ms; moved to background job bash-3915]`
- **T1** `"recette": "RoPE 34,3 M, lot 8, lr 3e-4, graine 1, init base-wiki-45m, 33 Mo vus par bras",`
- **T1** `"val et test disjoints (0 % de fuite, N2.h)",`
- **T1** `# Corpus : data/corpus_propre (train 3,24 Mo, val 180 Ko, 0 % de fuite — N2.h).`
- **T1** `# Deux bras à OCTETS ÉGAUX (33 Mo vus), init base-wiki-45m, canal :`
- **T1** `#   1. fenêtre 512, 8 000 pas × 8 × 512`
- **T1** `#   2. fenêtre 256 (seq 128), 32 000 pas × 8 × 128`

