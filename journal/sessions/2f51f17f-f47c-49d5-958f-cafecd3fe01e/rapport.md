# Session 2f51f17f — Tâche autonome de mesure, dans

> **Journaux :** [le jour](../../2026-10-22/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `2f51f17f-f47c-49d5-958f-cafecd3fe01e` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-22 08:14 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 18 |
| Appels d'outils | 17 |
| Fichiers touchés | 0 |
| Commandes | 9 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche autonome de mesure, dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet. Tu utilises UNIQUEMENT le GPU 0 (variable CUDA_VISIBLE_DEVICES=0) et l'interpréteur /home/stephane/IA/venv-drave/bin/python. N'utilise jamais le GPU 1 (un autre agent y travaille).  Objectif : reproduire le résultat de la mesure 120 (plan entraîné sur des séries de 8 phrases, horizons 1-3) avec une AUTRE grain … [1639 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche autonome de mesure, dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet. Tu utilises UNIQUEMENT le GPU 0 … [1919 caractères tronqués]

*17 appels d'outils.* Actions notables :

- bash — Check tool exists and GPU state
- bash — Check repo clean state and timestamp
- bash — List CLI arguments of the training tool
- read
- bash — Run training seed 5678 on GPU 0
- job_output
- bash — Run mixed-target control seed 5678 on GPU 0
- bash — Read timings and verify repo untouched
- bash — Inspect git log and file state read-only
- bash — Convert timestamps and compare script hashes
- bash — Collect timings and verify deliverables
- send_message

**Synthèse produite :**

⏵ Bilan final présenté

Les deux mesures sont terminées, séquentielles, sur GPU 0 seul, sans OOM. Résumé.

\## Configuration (identique à la mesure 120, graine changée)
Qwen2.5-3B-Instruct + LoRA, couche 18, prompt 4, séries de 8 phrases, horizons 1-3, 300 pas, batch 3 × accum 3, lr 1e-4. Données : 307 séries (le sous-échantillonnage rend 307, pas 315) → 214 entraînement / 93 test = **88 essais de retrieval** (1 coup = 0,0114 ; hasard 0,125).

\## Graine 5678 — `/tmp/plan-seed5678.json`

| horizon | avant | après | après_base (cibles figées) |
|---|---|---|---|
| h1 | 0,170 (15/88) | **0,409** (36/88) | 0,250 (22/88) |
| h2 | 0,227 (20/88) | **0,330** (29/88) | 0,227 (20/88) |
| h3 | 0,159 (14/88) | **0,352** (31/88) | 0,227 (20/88) |

Perte : 1,19 → 0,92 (pas 100) → 0,38 (pas 200) → 0,88 (pas 250), plancher log 3 ≈ 1,10.

\## Contrôle à cibles mélangées, même graine — `/tmp/plan-seed5678-melange.json`

| horizon | avant | après | (après_base) |
|---|---|---|---|
| h1 | 0,170 | 0,227 (20/88) | 0,114 (10/88) |
| h2 | 0,227 | 0,205 (18/88) | 0,148 (13/88) |
| h3 | 0,159 | 0,170 (15/88) | 0,159 (14/88) |

Perte du contrôle bloquée à 1,02–1,55 (≈ log 3) : rien ne s'apprend.

\## Lecture
Le gain se reproduit, plus faible qu'avec la graine 1234, et **ne se reproduit pas à cibles mélangées** : ce n'est donc pas un effet générique de fine-tuning. La part portée par les cibles figées (le « vrai » plan) est +0,125/+0,102/+0,102 au-dessus du hasard, contre +0,193/+0,125/+0,091 pour la mesure 121 — à h1, une plus grande part du gain de cette graine est adaptation de l'espace cible. Moyenne des deux graines (découpages différents, donc échantillons de test différents) : après 0,426/0,312/0,347 ; après_base 0,284/0,239/0,221.

Réserves honnêtes : le contrôle mélangé à h1 vaut 20/88, soit +2,9 σ au-dessus du hasard (σ ≈ 3,1 coups) ; c'est attendu en partie car avec batch 3 une permutation aléatoire est l'identité avec p = 1/6 — la comparaison utile reste 36/88 contre 20/88. Les « avant » diffèrent entre graines (0,170 vs 0,239 à h1) par simple effet de découpage.

\## Temps et incidents
- **Total 554 s** (9 min 14) : commande 1 = 274 s (08:14:48 → 08:19:22), commande 2 = 276 s (08:19:26 → 08:24:02). Aucune OOM, aucun repli `--batch 2 --accum 4`.
- Incident sans impact : le dépôt avait ` M tools/plan_entrainement.py` à mon arrivée (édits mesure 121 non commités) et l'autre agent a commité `0e89f1c5` à 08:16:01, donc HEAD a bougé pendant la mesure. Le contenu du script n'a pas 
… [386 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Check tool exists and GPU state
- **T1** Check repo clean state and timestamp
- **T1** List CLI arguments of the training tool
- **T1** Run training seed 5678 on GPU 0
- **T1** Run mixed-target control seed 5678 on GPU 0
- **T1** Read timings and verify repo untouched
- **T1** Inspect git log and file state read-only
- **T1** Convert timestamps and compare script hashes
- **T1** Collect timings and verify deliverables

