# Session ebd3d5a2 — Tâche autonome de mesure, dans

> **Journaux :** [le jour](../../2026-10-22/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `ebd3d5a2-7099-469e-b46d-dafe807d1a06` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-22 08:14 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 19 |
| Appels d'outils | 14 |
| Fichiers touchés | 0 |
| Commandes | 12 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche autonome de mesure, dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet. Tu utilises UNIQUEMENT le GPU 1 (variable CUDA_VISIBLE_DEVICES=1) et l'interpréteur /home/stephane/IA/venv-drave/bin/python. N'utilise jamais le GPU 0 (un autre agent y travaille).  Objectif : mesurer jusqu'où l'état de plan porte, sur des séries de 16 phrases consécutives (les mesures 119-120 ont montré 3 pas … [1404 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche autonome de mesure, dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet. Tu utilises UNIQUEMENT le GPU 1 … [1684 caractères tronqués]

*14 appels d'outils.* Actions notables :

- bash — Check script exists and GPU memory
- bash — List script arguments
- read
- bash — Run plan_entrainement measure on GPU 1
- bash — Read result JSON and timestamp
- bash — Find recent files to bracket run start
- bash — Inspect DSH env vars and measurement dir
- bash — Look for session logs with timestamps
- bash — Look for session transcript files
- bash — Locate my session transcript file
- bash — Extract timestamps from session transcript
- bash — Inspect transcript format
- bash — Extract tool call timestamps from transcript
- send_message

**Synthèse produite :**

⏵ Résultat consolidé et envoyé au parent

\## Mesure `plan-16` — terminée

**Invocation** (inchangée, GPU 1 uniquement, `CUDA_VISIBLE_DEVICES=1`) : `--par-serie 16 --series 320 --prompt 4 --horizons 1,2,3,4,5,6,7 --pas 300 --batch 3 --accum 3 --graine 1234 --sortie /tmp/plan-16.json`
Aucun OOM, aucune erreur, aucune relance. Aucun fichier du dépôt modifié (seule écriture : `/tmp/plan-16.json`).

\### Nombre de séries
**144 séries** (100 entraînement / 44 test) — et non 320. C'est un **incident à noter** : à `--par-serie 16`, le corpus Verne ne contient que 144 blocs de 16 ; `--series 320` est plafonné par la donnée. Le test ne comporte donc que **5 groupes de 8 = 40 items par horizon** (résolution 2,5 pts, bruit binomial ±5,2 pts à 1σ) : tout écart inférieur à ~5 pts est du bruit.

\### Avant / après, par horizon (hasard 0,125)

| h | avant | après | Δ | avant / hasard | après / hasard |
|---|---|---|---|---|---|
| h1 | 0,250 | 0,350 | +0,100 | 2,0× | 2,8× |
| h2 | 0,200 | 0,375 | +0,175 | 1,6× | 3,0× |
| h3 | 0,250 | 0,275 | +0,025 | 2,0× | 2,2× |
| h4 | 0,100 | 0,250 | +0,150 | 0,8× | 2,0× |
| h5 | 0,225 | 0,275 | +0,050 | 1,8× | 2,2× |
| h6 | 0,150 | 0,100 | −0,050 | 1,2× | 0,8× |
| h7 | 0,150 | 0,150 | 0,000 | 1,2× | 1,2× |

**Moyenne des 7 horizons : 0,189 → 0,254** (1,51× → 2,03× le hasard). Perte d'entraînement : 2,159 → 0,342.

\### Contrôle `apres_base` (cibles du modèle figé) — le point décisif
h1 0,250 · h2 0,225 · h3 0,200 · h4 0,100 · h5 0,150 · h6 0,250 · h7 0,175 → moyenne **0,193**, soit **aucun gain**. Le progrès mesuré « après » n'apparaît que face aux cibles recalculées par le modèle entraîné ; il ne se transfère pas à des cibles figées. Signature d'une dérive conjointe de l'espace des cibles plutôt que d'un état de plan appris (h6 : 0,250 en cibles figées vs 0,100 en cibles réentraînées).

\### Tendance avec l'horizon
Pas de décroissance propre. Après entraînement, la zone au-dessus du hasard va de h1 à h5 (essentiellement h2 et h4, ~3σ), h6 et h7 retombent au hasard — compatible avec « ~3–4 pas utiles », comme aux mesures 119-120, mais non démontré à 16 phrases compte tenu du bruit et de l'échec du contrôle.

\### Temps total
**8 min 36 s** (08:14:43 → 08:23:19, imports + chargement du 3 B + entraînement + évaluations).

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Check script exists and GPU memory
- **T1** List script arguments
- **T1** Run plan_entrainement measure on GPU 1
- **T1** Read result JSON and timestamp
- **T1** Find recent files to bracket run start
- **T1** Inspect DSH env vars and measurement dir
- **T1** Look for session logs with timestamps
- **T1** Look for session transcript files
- **T1** Locate my session transcript file
- **T1** Extract timestamps from session transcript
- **T1** Inspect transcript format
- **T1** Extract tool call timestamps from transcript

## 4. Mesures et résultats marquants

- **T1** `Loading weights:   0%|          | 0/434 [00:00<?, ?it/s]`
- **T1** `Loading weights:  21%|██        | 89/434 [00:00<00:00, 883.67it/s]`
- **T1** `Loading weights:  42%|████▏     | 181/434 [00:00<00:00, 904.67it/s]`
- **T1** `Loading weights:  63%|██████▎   | 272/434 [00:00<00:00, 903.96it/s]`
- **T1** `Loading weights:  84%|████████▎ | 363/434 [00:00<00:00, 895.87it/s]`
- **T1** `Loading weights: 100%|██████████| 434/434 [00:00<00:00, 921.64it/s]`

