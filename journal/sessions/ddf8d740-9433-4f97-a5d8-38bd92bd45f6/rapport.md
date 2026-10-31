# Session ddf8d740 — Tâche autonome de mesure, dans

> **Journaux :** [le jour](../../2026-10-22/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `ddf8d740-9433-4f97-a5d8-38bd92bd45f6` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-22 08:28 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 17 |
| Appels d'outils | 14 |
| Fichiers touchés | 0 |
| Commandes | 10 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche autonome de mesure, dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet. GPU 0 UNIQUEMENT (CUDA_VISIBLE_DEVICES=0), interpréteur /home/stephane/IA/venv-drave/bin/python. N'utilise jamais le GPU 1 (un autre agent y travaille).  Objectif : tester si un plan TRANSFÉRABLE s'entraîne, en entraînant le LoRA contre les cibles du modèle FIGÉ (et non contre les cibles recalculées par le modèle en co … [1220 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche autonome de mesure, dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet. GPU 0 UNIQUEMENT (CUDA_VISIBLE_DEVICES=0 … [1500 caractères tronqués]

*14 appels d'outils.* Actions notables :

- bash — Check script existence and GPU state
- bash — Check repo cleanliness
- read
- bash — Check model cache and data file
- bash — Record repo fingerprint before run
- bash — Run frozen-target LoRA training on GPU 0
- bash — Check startup log and GPU memory
- bash — Check frozen-target caching progress
- bash — Read full training log and result JSON
- job_output
- job_kill
- bash — Verify repo unchanged and timings
- bash — Compute exact counts and binomial significance
- send_message

**Synthèse produite :**

⏵ Mesure terminée et transmise ; je rends la synthèse finale

\## Mesure terminée — exit 0, aucun OOM, dépôt inchangé

**Commande lancée telle quelle** (`--batch 3 --accum 3`, pas de repli nécessaire). Durée totale : **1 min 44 s** (08:28:43 → 08:30:27). GPU 1 jamais touché.

**Données** : 307 séries (et non 315 — seuls 307 blocs de 8 existent dans `data/alignement/verne_fr_en.json`), 214 entraînement / 93 test. Éval : 11 groupes × 8 candidats = **88 essais par horizon**, hasard **0,125**.

\### Résultats (`/tmp/plan-fige-1234.json`)

| | h1 | h2 | h3 |
|---|---|---|---|
| **avant** | 0,239 (21/88) | 0,205 (18/88) | 0,171 (15/88) |
| **apres** | 0,352 (31/88) | 0,227 (20/88) | 0,250 (22/88) |
| **apres_base** (cibles figées) | **0,352** (31/88) | **0,239** (21/88) | **0,239** (21/88) |

Perte d'entraînement : 2,81 → 0,82. Pic mémoire ≈ 10,3 Gio / 16 Gio.

\### Réponse : oui, le plan transférable monte au-dessus du modèle figé

- **Au-dessus du hasard** : 0,352 / 0,239 / 0,239 → z = 6,45 / 3,22 / 3,22, p binomial ≈ 1e-6 / 0,003 / 0,003. Les trois horizons sont significatifs.
- **Au-dessus du modèle figé (avant)** : +11,4 / +3,4 / +6,8 points (+10 / +3 / +6 évènements sur 88).
- **Geler les cibles ne coûte rien** : `apres` vs `apres_base` diffèrent d'au plus **1 évènement sur 88** → aucun signe de poursuite de cibles ni d'effondrement.

\### Réserves à porter dans toute fiche

1. **Le modèle figé est déjà au-dessus du hasard** avant entraînement (p = 0,003 en h1) : une part du retrieval vient de similarité lexicale/de contenu, pas du plan — le contrôle négatif `--melange` n'a pas été lancé ici.
2. **Seul h1 est solide** en gain sur « avant » (z = +1,65 en test non apparié) ; h2 (z = +0,54) et h3 (z = +1,12) restent dans le bruit avec 88 essais — il faudrait 2-3× plus de séries test, ou un test apparié par groupe.
3. In-batch à l'entraînement = 3 candidats, éval = 1 parmi 8 : la perte n'est pas comparable au retrieval.

**Incidents** : aucun. Le dépôt est identique avant/après (git status et sha256 de `tools/plan_entrainement.py` et du JSON de données inchangés) ; seul `/tmp` a été écrit. À signaler : `tools/plan_entrainement.py` était **déjà** marqué modifié (`M`) avant mon lancement — je n'y ai pas touché.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Check script existence and GPU state
- **T1** Check repo cleanliness
- **T1** Check model cache and data file
- **T1** Record repo fingerprint before run
- **T1** Run frozen-target LoRA training on GPU 0
- **T1** Check startup log and GPU memory
- **T1** Check frozen-target caching progress
- **T1** Read full training log and result JSON
- **T1** Verify repo unchanged and timings
- **T1** Compute exact counts and binomial significance

## 4. Mesures et résultats marquants

- **T1** `Loading weights:   0%|          | 0/434 [00:00<?, ?it/s]`
- **T1** `Loading weights:  20%|██        | 88/434 [00:00<00:00, 864.50it/s]`
- **T1** `Loading weights:  40%|████      | 175/434 [00:00<00:00, 863.07it/s]`
- **T1** `Loading weights:  63%|██████▎   | 274/434 [00:00<00:00, 919.83it/s]`
- **T1** `Loading weights:  85%|████████▍ | 367/434 [00:00<00:00, 896.17it/s]`
- **T1** `Loading weights: 100%|██████████| 434/434 [00:00<00:00, 897.17it/s]`
- **T1** `[still running after 60000ms; moved to background job bash-1442]`
- **T1** `cibles figées : 214 séries × 3 horizons mises en cache`
- **T1** `h1: avant 21/88 -> apres_base 31/88  delta=+10 évèn. (+0.114 pt, +47.6 %)`
- **T1** `h2: avant 18/88 -> apres_base 21/88  delta=+3 évèn. (+0.034 pt, +16.7 %)`
- **T1** `h3: avant 15/88 -> apres_base 21/88  delta=+6 évèn. (+0.068 pt, +40.0 %)`

