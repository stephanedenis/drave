# Session 082fe8ca — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `082fe8ca-3e1e-4454-b91b-12586843e880` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 11:17 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 19 |
| Appels d'outils | 24 |
| Fichiers touchés | 0 |
| Commandes | 18 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer la fiabilité du produit hors gold** — le test « utilisateur » qui manque.  Contexte : `tools/drave.py` (CLI : `analyser`, `evaluer`, `rejouer`, `--version`), `tools/bloc_linguistique.py` (`Heuristique.analyser` → `Annotation`), la doc `docs/produit/README.md`. État mesuré : gold  … [1665 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer  … [1945 caractères tronqués]

*24 appels d'outils.* Actions notables :

- bash — Check working directory and git status
- bash — List repo root and reports directory
- bash — Count lines of key files
- bash — Check recent commits and reports status
- read
- bash — List classes and methods in bloc_linguistique.py
- bash — Read product test and gate
- bash — List linguistic tests and check CLI version
- bash — List product reports and inspect JSON format
- bash — Inspect recent report markdown styles
- bash — Check file timestamps and existing report summary
- bash — Inspect existing JSON structure
- bash — Probe CLI edge cases and exit codes
- bash — Probe URL tokenization and phrase spans
- … et 5 autres

**Synthèse produite :**

⏵ Sondage rapide des cas limites avant le harnais complet

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Check working directory and git status
- **T1** List repo root and reports directory
- **T1** Count lines of key files
- **T1** Check recent commits and reports status
- **T1** List classes and methods in bloc_linguistique.py
- **T1** Read product test and gate
- **T1** List linguistic tests and check CLI version
- **T1** List product reports and inspect JSON format
- **T1** Inspect recent report markdown styles
- **T1** Check file timestamps and existing report summary
- **T1** Inspect existing JSON structure
- **T1** Probe CLI edge cases and exit codes
- **T1** Probe URL tokenization and phrase spans
- **T1** Probe option-like and invalid-UTF-8 inputs
- **T1** Measure 10k-character input
- **T1** Test locale and stdout encoding failures
- **T1** Test broken pipe and phrase span whitespace
- **T1** Read existing report contract and fixes sections

## 4. Mesures et résultats marquants

- **T1** `6ef2a3f5 JOURNAL ET ROADMAP — LA VAGUE PRODUIT : DRAVE V0 DOCUMENTÉ, PORTE PRODUIT VERTE, AUTOTEST ×2,4, MASTER POUSSÉ (7f73c17f)`
- **T1** `| graphème, mot | ✅ | 0 crash, 0 span hors texte, `valeur = texte[debut:fin]` à **100 %**, couverture **49/50 à 100 %** (x46 : 95,14 %, newlines) |`
- **T1** `dash-- rc=0 out=langue=und script=Latn source=heuristique · 12 étiquettes · unités sémantiques=1 (66.7% du texte)`
- **T1** `**graphème** : 49/50 textes à 100 %, x46 à **95,14 %** (7 newlines, catégorie `Cc`, non couvertes).`
- **T1** `| **heuristique** | **1,08 ms** | **4,60 ms** | **19,43 ms** | 0,097 |`
- **T1** `| mock neuronal | 0,30 ms | 1,08 ms | 4,44 ms | 0,022 |`
- **T1** `| parallèle | 1,51 ms | 6,18 ms | 27,22 ms | 0,136 |`
- **T1** `| cascade | 1,51 ms | 6,25 ms | 29,64 ms | 0,148 |`
- **T1** `- **Coût des compositions** : +37 % (parallèle) et +45 % (cascade) à 200 mots **avec le mock** ;`
- **T1** `**99–113 ms** (import + première analyse), **27,4 Mio**.`
- **T1** `- **Passage à l'échelle** : 200 mots 19 ms (0,096 ms/mot), 500 mots 70 ms (0,139), 1 000 mots`
- **T1** `166 ms (0,166), 2 000 mots 482 ms (0,241), 4 000 mots **1 574 ms** (0,394). Le coût par mot`
- **T1** `| `valeur` | **surface** pour graphème/mot/pos/syntagme (100 %) ; **normalisée** pour morphème (126/134) ; **tronquée à 60** pour document (42/53) ; **catégorielle** pour phrase/pragmatique/discours ;`
- **T1** `| **P1-15** | **Réduire le coût superlinéaire au-delà de 200 mots** | 0,096 ms/mot à 200, **0,394** à 4 000 (4,1×), 1,57 s à 4 000 ; `_cible_proche` : **199 302** appels à `_est_adverbe_seul` | 800-85`
- **T1** `| **P2-16** | Couvrir les caractères de contrôle dans graphème | x46 : **7 newlines** non couverts, 95,14 % ; 49/50 à 100 % | 1020-1031 | **15 min** |`

