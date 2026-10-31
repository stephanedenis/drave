# Session 15d4e6f4 — Tâche autonome de mesure, dans

> **Journaux :** [le jour](../../2026-10-22/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `15d4e6f4-b2ba-44c7-8c0e-03c141280f9b` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-22 08:28 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 23 |
| Appels d'outils | 18 |
| Fichiers touchés | 0 |
| Commandes | 12 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche autonome de mesure, dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet. GPU 1 UNIQUEMENT (CUDA_VISIBLE_DEVICES=1), interpréteur /home/stephane/IA/venv-drave/bin/python. N'utilise jamais le GPU 0 (un autre agent y travaille).  Objectif : tester si un plan TRANSFÉRABLE s'entraîne, en entraînant le LoRA contre les cibles du modèle FIGÉ, avec un second découpage (graine 5678).  Commande (atten … [1183 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche autonome de mesure, dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet. GPU 1 UNIQUEMENT (CUDA_VISIBLE_DEVICES=1 … [1463 caractères tronqués]

*18 appels d'outils.* Actions notables :

- bash — Vérifie script et état GPU
- grep
- bash — Entraîne le LoRA contre cibles figées
- job_output
- bash — Affiche le JSON et horodatage
- job_list
- bash — Cherche variables DSH et logs récents
- bash — Inspecte logs de session dsh
- bash — Extrait horodatages du journal de session
- bash — Calcule durée approximative du run
- bash — Lit sortie sauvegardée et logs de lancement
- read
- bash — Vérifie GPU, processus et fichiers modifiés
- bash — Vérifie pycache et gitignore
- … et 3 autres

**Synthèse produite :**

⏵ Résumé final du run et de l'interprétation

**Run terminé** — `tools/plan_entrainement.py`, graine 5678, cibles figées, GPU 1 seul, **aucun OOM** (batch 3 / accum 3 conservés). Sortie : `/tmp/plan-fige-5678.json`, aucun fichier du dépôt touché.

**Contexte de mesure** : 307 séries → 214 entraînement / 93 test ; retrieval top-1 parmi 8 candidats non vus (hasard **0,125**) sur 88 items → 1 item = 1,14 pp.

| | avant | apres | **apres_base** (figé) |
|---|---|---|---|
| h1 | 0,1705 | 0,3182 | **0,2955** |
| h2 | 0,2273 | 0,2955 | **0,3068** |
| h3 | 0,1591 | 0,2614 | **0,1932** |

**apres_base − avant** (même cache de candidats, comparaison directe) : h1 **+12,5 pp** (×1,73 ; +11 items, z≈2,0), h2 **+7,9 pp** (×1,35 ; +7 items, z≈1,2), h3 **+3,4 pp** (×1,21 ; +3 items, z≈0,6).

**Est-ce que le plan transférable monte au-dessus du figé ?** Oui, aux trois horizons, et le signe est **reproduit sur le découpage graine 1234** (+11,4 / +3,4 / +6,8 pp). Mais seul h1 est statistiquement solide ; h3 est dans le bruit. À noter : `apres` (cibles ré-encodées par le modèle entraîné) est en partie une mesure d'auto-cohérence — la mesure honnête du transfert est bien `apres_base` vs `avant`.

**Temps total** : ≈107 s (1 min 47 s) du lancement à l'écriture du JSON. **Incidents** : aucun ; perte 1,194 → 0,583 puis 1,193 au pas 250 (bruit d'un lot de 3, pas de divergence) ; GPU 1 libéré en fin de run, GPU 0 jamais utilisé.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Vérifie script et état GPU
- **T1** Entraîne le LoRA contre cibles figées
- **T1** Affiche le JSON et horodatage
- **T1** Cherche variables DSH et logs récents
- **T1** Inspecte logs de session dsh
- **T1** Extrait horodatages du journal de session
- **T1** Calcule durée approximative du run
- **T1** Lit sortie sauvegardée et logs de lancement
- **T1** Vérifie GPU, processus et fichiers modifiés
- **T1** Vérifie pycache et gitignore
- **T1** Lit le JSON parallèle graine 1234
- **T1** Calcule écarts et erreurs-types

## 4. Mesures et résultats marquants

- **T1** `Loading weights:   0%|          | 0/434 [00:00<?, ?it/s]`
- **T1** `Loading weights:  20%|██        | 88/434 [00:00<00:00, 864.50it/s]`
- **T1** `Loading weights:  40%|████      | 175/434 [00:00<00:00, 863.07it/s]`
- **T1** `Loading weights:  63%|██████▎   | 274/434 [00:00<00:00, 919.83it/s]`
- **T1** `Loading weights:  85%|████████▍ | 367/434 [00:00<00:00, 896.17it/s]`
- **T1** `Loading weights: 100%|██████████| 434/434 [00:00<00:00, 897.17it/s]`
- **T1** `cibles figées : 214 séries × 3 horizons mises en cache`
- **T1** `0, 1 MiB, 0 %`
- **T1** `1, 1 MiB, 0 %`

