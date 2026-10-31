# Session DSH — relecture

- identifiant : `ddf8d740-9433-4f97-a5d8-38bd92bd45f6`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-22 08:28:19
- agent : standard


## Tour 1

### 👤 Utilisateur

Tâche autonome de mesure, dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet. GPU 0 UNIQUEMENT (CUDA_VISIBLE_DEVICES=0), interpréteur /home/stephane/IA/venv-drave/bin/python. N'utilise jamais le GPU 1 (un autre agent y travaille).

Objectif : tester si un plan TRANSFÉRABLE s'entraîne, en entraînant le LoRA contre les cibles du modèle FIGÉ (et non contre les cibles recalculées par le modèle en cours d'entraînement).

Commande (attends la fin) :
CUDA_VISIBLE_DEVICES=0 OMP_NUM_THREADS=10 /home/stephane/IA/venv-drave/bin/python tools/plan_entrainement.py --par-serie 8 --series 315 --prompt 4 --horizons 1,2,3 --pas 300 --batch 3 --accum 3 --graine 1234 --cibles-figees --sortie /tmp/plan-fige-1234.json

Règles : ne modifie AUCUN fichier du dépôt (pas de git, pas de docs, pas de tools, pas de data) ; le script n'écrit que dans /tmp. Si OOM, relance avec --batch 2 --accum 4 et note-le.

À la fin, lis /tmp/plan-fige-1234.json et rends : "avant", "apres" et surtout "apres_base" (cibles figées) pour h1/h2/h3, le temps total, et tout incident. Compare apres_base à avant : est-ce que le plan transférable monte au-dessus du modèle figé (hasard 0,125) ?
Your parent agent id is "d629d7d7-e122-4596-8757-f4264a2b15cf". Before you finish, send your result to that agent with send_message({ agent_id: "d629d7d7-e122-4596-8757-f4264a2b15cf", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

### 👤 Utilisateur

<system-reminder>
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

Instructions from: AGENTS.md

# Directives de l'agent — Drave Natif

> **Porte d'entrée.** Lis ce fichier en entier (2 min) : il porte la mission, les règles non négociables et le
> **routage** vers le document de chaque tâche. Le détail n'est pas ici : il est dans [`docs/agent/`](docs/agent/)
> (tableau § 3). L'**état courant** est dans [`docs/en-cours.md`](docs/en-cours.md) ; le récit daté dans
> [`journal/`](journal/).

## 1. La mission (l'essentiel)

Deux **étages** d'architecture, dans cet ordre, et **on ne passe pas au suivant tant que le précédent est perfectible** :

1. **Les modules d'ENTRÉE et de SORTIE linguistiques** — priorité absolue. Ils doivent lire et produire **toutes**
   les langues, dialectes et styles, dans les registres **techniques, littéraires, juridiques, quotidiens**. On les
   juge en **qualité de traducteur** (restitution à l'identique, et traduction du sens). On ne « déclare complet »
   que sur des **chiffres** qui couvrent langues, dialectes, styles et domaines.
2. **Le module de pensée abstraite, indépendant de la langue** — **seulement après**. Il ne peut pas être bâti sur
   une entrée-sortie qui n'est pas fiable.

**Le temps est un plancher, pas un plafond** (*carpe diem*) : on s'arrête quand l'étage est **fait, mesuré et
écrit**, pas quand une échéance passe. Détail : [`docs/agent/mission.md`](docs/agent/mission.md).

**Vocabulaire** : *couche* = **couche de neurones** (couche 1, 2…, un réseau) ; *étage* = **niveau d'architecture**
(étage 1 entrée-sortie, étage 2 pensée) ; *jeton* = **unité du tokeniseur** d'un modèle, **jamais** la
**représentation sémantique neutre (RSN)**, dont les éléments sont des **unités de sens**. Le nom historique
« couche commune entrée-sortie » se lit « étage entrée-sortie ». Voir [`docs/glossaire.md`](docs/glossaire.md).

## 2. Les règles non négociables

1. **Rangement** : `docs/` = état, vision, concepts (ce qui reste vrai quand les chiffres changent) ; `reports/` =
   résultats mesurés, fiches, JSON ; `journal/` = récit daté ; `data/` = corpus. *Un résultat qui traîne dans
   `docs/` **déménage**.* → [`docs/agent/rangement.md`](docs/agent/rangement.md)
2. **Un résultat** porte le chiffre, la mesure, le dispositif, un **contrôle négatif**, et **ce qui pourrait le
   rendre faux** — puis un **commit**, la **fiche** dans `reports/`, le **récit** dans `journal/`, l'**état** dans
   `docs/en-cours.md`. *Sans contrôle négatif, ce n'est pas un résultat.* →
   [`docs/agent/resultats.md`](docs/agent/resultats.md)
3. **Les portes** : `bash tools/toutes-les-portes.sh` ; le registre est dans `$JOURNAUX/registre.txt` (affiché au
   lancement) et le verdict se lit par `awk '$2 != 0'` — **jamais** par les marqueurs ni à travers un tube. Rouges
   structurelles tolérées : **`porte-indice`** et **`porte-melange`** ; toute autre est une régression. →
   [`docs/agent/portes.md`](docs/agent/portes.md)
4. **La revue de documentation** avant chaque commit de clôture : `python3 tools/revue_documentation.py` (et
   `tools/porte-tableaux.sh`) ; **corriger** ce qu'elle signale. → [`docs/agent/rangement.md`](docs/agent/rangement.md)
5. **Panini et Nipada** à chaque cycle : lire ce qui a bougé chez eux, confronter ; la théorie va dans
   [`docs/genealogie-des-langues.md`](docs/genealogie-des-langues.md), **jamais** les chiffres. Leur avertissement :
   la surface capte **l'époque** (β +0,138) bien plus que la **filiation** (β +0,049) — contrôler la date dans tout
   test de style, la surface dans tout test de famille. → [`docs/agent/panini-nipada.md`](docs/agent/panini-nipada.md)
6. **Le miroir entrée/sortie** : toute mesure d'entrée se double d'une mesure de **sortie** (restitution, boucle) ;
   la **fluidité n'est pas la fidélité**. → [`docs/agent/miroir.md`](docs/agent/miroir.md)
7. **Ne jamais bloquer** sur une question humaine : la consolider dans `docs/en-cours.md` et **continuer** ;
   répondre soi-même si ce n'est pas la vision ou la philosophie. → [`docs/agent/ressources.md`](docs/agent/ressources.md)

## 3. Routage : lire le document de sa tâche, pas les autres

| si la tâche est… | lire |
|---|---|
| comprendre la mission, les priorités, la philosophie | [`docs/agent/mission.md`](docs/agent/mission.md) |
| écrire un résultat (fiche, JSON, commit, journal) | [`docs/agent/resultats.md`](docs/agent/resultats.md) |
| ranger un fichier, revue de documentation, synthèse | [`docs/agent/rangement.md`](docs/agent/rangement.md) |
| lancer ou lire les portes | [`docs/agent/portes.md`](docs/agent/portes.md) |
| étudier Panini/Nipada, la généalogie | [`docs/agent/panini-nipada.md`](docs/agent/panini-nipada.md) |
| concevoir un test d'entrée/sortie, corriger | [`docs/agent/miroir.md`](docs/agent/miroir.md) |
| planifier une campagne, le matériel, carpe diem | [`docs/agent/ressources.md`](docs/agent/ressources.md) |
| **l'état courant** (synthèse + chantiers + questions) | [`docs/en-cours.md`](docs/en-cours.md) |
| le **vocabulaire** (couche vs étage, termes du dépôt) | [`docs/glossaire.md`](docs/glossaire.md) |
| la carte de la documentation | [`docs/README.md`](docs/README.md) |

## 4. Le minimum avant de conclure

- l'état est à jour dans [`docs/en-cours.md`](docs/en-cours.md) (synthèse, chantiers, questions en attente) ;
- la fiche est dans `reports/`, le récit dans `journal/`, le commit porte le chiffre ;
- les portes sont vertes, **hors les deux rouges structurelles connues** ;
- la revue de documentation passe, et les liens résolvent.

</system-reminder>

### 👤 Utilisateur

Current runtime context. This snapshot supersedes earlier runtime-context snapshots.

Current DSH file policy: danger-full-access. The DSH file sandbox does not restrict file modifications by available operations.

Approval prompts are disabled in this session: actions that require approval are rejected automatically — do not request sandbox escalation (do not set `sandbox_permissions`).

You are a delegated subagent: your permission scope was fixed when you were started and cannot be widened from inside this session — operations that require approval are rejected automatically. When the task needs access beyond that scope, do not retry the denied operation; state the limitation in your reply so the delegating agent can handle it.

### 👤 Utilisateur

<system-reminder>
A skill is a reusable set of task-specific instructions. The following skills are available in this session:

<available_skills>
- `microsoft-foundry`: Deploy, evaluate, fine-tune, and manage Foundry agents end-to-end with azd: hosted agent scaffold/run/deploy, prompt agent create, batch eval, continuous eval, prompt optimizer, Agent Optimizer scaffold, agent.yaml, dataset curation from traces, model fine-tuning (SFT/DPO/RFT). USE FOR: azd ai agent, azd provision/deploy, deploy agent, hosted agent, create agent, add tool to agent, invoke agent, evaluate agent, continuous eval, continuous monitoring, agent CI/CD, optimize prompt, improve prom...
</available_skills>

If the user names a skill, or the task clearly matches a skill's description, call the `skill` tool with the exact skill name before taking task actions. Load all applicable skills, then follow their full instructions. This catalog contains summaries only; do not infer or follow a skill's instructions until it has been loaded.
A user may also invoke a skill directly; its <skill_content> block then appears in this conversation. Follow it, and do not call the `skill` tool again for that skill.
</system-reminder>

### 🤖 Assistant

⏵ Je vérifie le script et l'environnement GPU avant de lancer l'entraînement

- **bash** `{"command": "ls -la tools/plan_entrainement.py 2>&1; echo \"---\"; nvidia-smi --query-gpu=index,name,memory.used,memory.total --format=csv 2>&1", "description": "Check script existence and GPU state", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
-rw-------. 1 stephane stephane 9988 22 oct 08:27 tools/plan_entrainement.py
---
index, name, memory.used [MiB], memory.total [MiB]
0, Quadro RTX 5000, 1 MiB, 16384 MiB
1, Quadro RTX 5000, 1 MiB, 16384 MiB
  ```

- **bash** `{"command": "git status --porcelain 2>&1 | head -20; echo \"--- branch:\"; git rev-parse --abbrev-ref HEAD 2>&1", "description": "Check repo cleanliness", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
M tools/plan_entrainement.py
--- branch:
master
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/plan_entrainement.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/plan_entrainement.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """plan_entrainement.py — ÉTAGE 2 : peut-on ENTRAÎNER le plan dans le modèle (et non le lire après coup) ?
3: 
4: POURQUOI ✓✓. Les mesures 113-118 ont montré que les états **figés** portent la phrase et la langue, pas le plan ✗✗ :
5: l'opérateur linéaire prédit la moyenne, le MLP mémorise, le contexte ne porte pas le contenu, un code de 32 dimensions
6: ne dépasse la moyenne que de +0,02, et la position n'est pas décodable quand la langue l'est à 1,00. La question de la
7: phase suivante : un **objectif de plan** entraîné dans le modèle peut-il faire mieux ? ✓✓
8: 
9: LE TEST ✓✓ : sur les séries Verne FR (8 phrases), on donne au modèle les **4 premières phrases** et on lui demande de
10: produire un **état de plan** (le dernier état caché de l'invite) qui retrouve l'état de la **5ᵉ phrase** parmi
11: **8 candidats non vus** d'autres séries (hasard 12,5 %) ✓✓. Le modèle est un 3 B + LoRA, entraîné par **InfoNCE**
12: (contrastif) ; on compare le retrieval **avant** et **après** ✓✓.
13: 
14: CE QUE CHAQUE ISSUE VEUT DIRE ✓✓ :
15:   · retriev
… [9644 caractères tronqués]
  ```

- **bash** `{"command": "ls -d ~/.cache/huggingface/hub/models--Qwen--Qwen2.5-3B-Instruct 2>&1; du -sh ~/.cache/huggingface/hub/models--Qwen--Qwen2.5-3B-Instruct 2>&1; echo \"--- data:\"; ls -la data/alignement/verne_fr_en.json", "description": "Check model cache and data file", "workdir": "/home/stephane/Data1 … [29 caractères tronqués]`

  ```
/home/stephane/.cache/huggingface/hub/models--Qwen--Qwen2.5-3B-Instruct
5,8G	/home/stephane/.cache/huggingface/hub/models--Qwen--Qwen2.5-3B-Instruct
--- data:
-rw-r--r--. 1 stephane stephane 1356554 19 oct 14:34 data/alignement/verne_fr_en.json
  ```

### 🤖 Assistant

⏵ L'environnement est prêt ; je fige l'empreinte du dépôt puis je lance la commande en arrière-plan

- **bash** `{"command": "mkdir -p /tmp/plan-fige-run && { git status --porcelain; echo \"---\"; sha256sum tools/plan_entrainement.py data/alignement/verne_fr_en.json; } > /tmp/plan-fige-run/empreinte-avant.txt 2>&1; cat /tmp/plan-fige-run/empreinte-avant.txt", "description": "Record repo fingerprint before run" … [63 caractères tronqués]`

  ```
M tools/plan_entrainement.py
---
d6c1621bfa8e08498d90e637ea5302cbc39d9a24174f4c78e0baa0bf4459a2a1  tools/plan_entrainement.py
19a9df64f5b752522d55cb09e1799a7b824f93a40c73c7cbc34aa8b4811f81ba  data/alignement/verne_fr_en.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=0 OMP_NUM_THREADS=10 /home/stephane/IA/venv-drave/bin/python tools/plan_entrainement.py --par-serie 8 --series 315 --prompt 4 --horizons 1,2,3 --pas 300 --batch 3 --accum 3 --graine 1234 --cibles-figees --sortie  … [189 caractères tronqués]`

  ```
started background job bash-1440
  ```

### 🤖 Assistant

⏵ Suivi du démarrage (chargement du modèle 3B, construction des séries)

- **bash** `{"command": "sleep 45; echo \"=== log ===\"; cat /tmp/plan-fige-run/sortie.txt; echo \"=== gpu ===\"; nvidia-smi --query-gpu=index,memory.used --format=csv,noheader", "description": "Check startup log and GPU memory"}`

  ```
=== log ===
  307 séries · 214 entraînement · 93 test
Loading weights:   0%|          | 0/434 [00:00<?, ?it/s]Loading weights:  20%|██        | 88/434 [00:00<00:00, 864.50it/s]Loading weights:  40%|████      | 175/434 [00:00<00:00, 863.07it/s]Loading weights:  63%|██████▎   | 274/434 [00:00<00:00, 919.83it/s]Loading weights:  85%|████████▍ | 367/434 [00:00<00:00, 896.17it/s]Loading weights: 100%|██████████| 434/434 [00:00<00:00, 897.17it/s]
=== gpu ===
0, 10262 MiB
1, 10188 MiB
  ```

### 🤖 Assistant

⏵ Modèle chargé (307 séries) ; je surveille le cache des cibles figées et le retrieval « avant »

- **bash** `{"command": "sleep 90; echo \"=== log ===\"; tail -c 3000 /tmp/plan-fige-run/sortie.txt; echo; echo \"=== gpu0 ===\"; nvidia-smi --query-gpu=index,memory.used --format=csv,noheader", "description": "Check frozen-target caching progress"}`

  ```
[still running after 60000ms; moved to background job bash-1442]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

### 👤 Utilisateur

background job bash-1440 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=0 OMP_NUM_THREADS=10 /home/stephane/IA/venv-drave/bin/python tools/plan_entrainement.py --par-serie 8 --series 315 --prompt 4 --horizons 1,2,3 --pas 300 --batch 3 --accum 3 --graine 1234 --cibles-figees --sortie /tmp/plan-fige-1234.json > /tmp/plan-fige-run/sortie.txt 2>&1; echo "EXIT=$?") finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ L'entraînement est terminé ; je lis le journal complet et le JSON produit

- **bash** `{"command": "echo \"=== log complet ===\"; cat /tmp/plan-fige-run/sortie.txt; echo; echo \"=== json ===\"; cat /tmp/plan-fige-1234.json", "description": "Read full training log and result JSON"}`

  ```
=== log complet ===
  307 séries · 214 entraînement · 93 test
Loading weights:   0%|          | 0/434 [00:00<?, ?it/s]Loading weights:  20%|██        | 88/434 [00:00<00:00, 864.50it/s]Loading weights:  40%|████      | 175/434 [00:00<00:00, 863.07it/s]Loading weights:  63%|██████▎   | 274/434 [00:00<00:00, 919.83it/s]Loading weights:  85%|████████▍ | 367/434 [00:00<00:00, 896.17it/s]Loading weights: 100%|██████████| 434/434 [00:00<00:00, 897.17it/s]
  cibles figées : 214 séries × 3 horizons mises en cache
  AVANT : h1 0.239 · h2 0.205 · h3 0.170
    pas    0 · perte 2.813
    pas   50 · perte 2.311
    pas  100 · perte 1.318
    pas  150 · perte 1.161
    pas  200 · perte 0.998
    pas  250 · perte 0.823
  APRÈS : h1 0.352 · h2 0.227 · h3 0.250
  APRÈS (cibles du modèle figé) : h1 0.352 · h2 0.239 · h3 0.239
  → /tmp/plan-fige-1234.json

=== json ===
{
 "hf": "Qwen/Qwen2.5-3B-Instruct",
 "n_series": 307,
 "n_train": 214,
 "n_test": 93,
 "couche": 18,
 "prompt": 4,
 "horizons": [
  1,
  2,
  3
 ],
 "pas": 300,
 "batch": 3,
 "accum": 3,
 "lr": 0.0001,
 "graine": 1234,
 "cibles_figees": true,
 "avant": {
  "1": 0.2386,
  "2": 0.2045,
  "3": 0.1705
 },
 "apres": {
  "1": 0.3523,
 
… [132 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-1442"}`

  ```
(no new output)
[status: running]
  ```

### 🤖 Assistant

⏵ Résultat obtenu sans OOM ; je vérifie l'intégrité du dépôt, les temps et la significativité

- **job_kill** `{"job_id": "bash-1442", "reason": "Surveillance obsolète, l'entraînement est terminé"}`

  ```
requested cancellation of job bash-1442
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"=== empreinte après ===\"; { git status --porcelain; echo \"---\"; sha256sum tools/plan_entrainement.py data/alignement/verne_fr_en.json; } 2>&1\necho \"=== comparaison ===\"; diff /tmp/plan-fige-run/empreinte-avant.txt <({ git  … [410 caractères tronqués]`

  ```
=== empreinte après ===
 M tools/plan_entrainement.py
---
d6c1621bfa8e08498d90e637ea5302cbc39d9a24174f4c78e0baa0bf4459a2a1  tools/plan_entrainement.py
19a9df64f5b752522d55cb09e1799a7b824f93a40c73c7cbc34aa8b4811f81ba  data/alignement/verne_fr_en.json
=== comparaison ===
IDENTIQUE : dépôt inchangé
=== temps ===
/tmp/plan-fige-run/sortie.txt  naissance=2026-10-22 08:28:43.623117663 -0400  modif=2026-10-22 08:30:27.626673524 -0400
/tmp/plan-fige-1234.json  naissance=2026-10-22 08:30:27.558672507 -0400  modif=2026-10-22 08:30:27.560056120 -0400
=== tailles ===
-rw-r--r--. 1 stephane stephane 464 22 oct 08:30 /tmp/plan-fige-1234.json
-rw-r--r--. 1 stephane stephane 923 22 oct 08:30 /tmp/plan-fige-run/sortie.txt
  ```

### 🤖 Assistant

⏵ Calcul des effectifs exacts et des p-values binomiales contre le hasard

- **bash** `{"command": "/home/stephane/IA/venv-drave/bin/python - <<'EOF'\nimport json, math\nd=json.load(open(\"/tmp/plan-fige-1234.json\"))\nn_te=93\ntot=len(range(0,n_te-7,8))*8\nprint(\"essais par horizon :\", tot, \" groupes :\", tot//8)\ndef binom_p(k,n,p):\n    # p-value bilatérale exacte (loi binomiale … [1347 caractères tronqués]`

  ```
essais par horizon : 88  groupes : 11
             k/   taux      z  p_binom
avant      h1  21/88  0.239   3.22   0.0031
avant      h2  18/88  0.204   2.26   0.0342
avant      h3  15/88  0.171   1.29   0.1967
apres      h1  31/88  0.352   6.45   0.0000
apres      h2  20/88  0.227   2.90   0.0087
apres      h3  22/88  0.250   3.55   0.0011
apres_base h1  31/88  0.352   6.45   0.0000
apres_base h2  21/88  0.239   3.22   0.0031
apres_base h3  21/88  0.239   3.22   0.0031

h1: avant 21/88 -> apres_base 31/88  delta=+10 évèn. (+0.114 pt, +47.6 %)
h2: avant 18/88 -> apres_base 21/88  delta=+3 évèn. (+0.034 pt, +16.7 %)
h3: avant 15/88 -> apres_base 21/88  delta=+6 évèn. (+0.068 pt, +40.0 %)

h1: z_gain=+1.65
h2: z_gain=+0.54
h3: z_gain=+1.12

apres vs apres_base (mêmes requêtes, cibles recalculées vs figées) :
  h1: 31/88 vs 31/88  (+0 évèn.)
  h2: 20/88 vs 21/88  (+1 évèn.)
  h3: 22/88 vs 21/88  (-1 évèn.)
  ```

### 🤖 Assistant

⏵ Résultat complet et vérifié ; j'envoie la synthèse à l'agent parent

- **send_message** `{"agent_id": "d629d7d7-e122-4596-8757-f4264a2b15cf", "message": "MESURE TERMINÉE — plan transférable (LoRA vs cibles FIGÉES), GPU 0 uniquement, exit 0, pas d'OOM.\n\nCommande exacte lancée (sans modification) :\nCUDA_VISIBLE_DEVICES=0 OMP_NUM_THREADS=10 /home/stephane/IA/venv-drave/bin/python tools/ … [2585 caractères tronqués]`

  ```
message delivered to agent d629d7d7-e122-4596-8757-f4264a2b15cf
  ```

### 🤖 Assistant

⏵ Mesure terminée et transmise ; je rends la synthèse finale

## Mesure terminée — exit 0, aucun OOM, dépôt inchangé

**Commande lancée telle quelle** (`--batch 3 --accum 3`, pas de repli nécessaire). Durée totale : **1 min 44 s** (08:28:43 → 08:30:27). GPU 1 jamais touché.

**Données** : 307 séries (et non 315 — seuls 307 blocs de 8 existent dans `data/alignement/verne_fr_en.json`), 214 entraînement / 93 test. Éval : 11 groupes × 8 candidats = **88 essais par horizon**, hasard **0,125**.

### Résultats (`/tmp/plan-fige-1234.json`)

| | h1 | h2 | h3 |
|---|---|---|---|
| **avant** | 0,239 (21/88) | 0,205 (18/88) | 0,171 (15/88) |
| **apres** | 0,352 (31/88) | 0,227 (20/88) | 0,250 (22/88) |
| **apres_base** (cibles figées) | **0,352** (31/88) | **0,239** (21/88) | **0,239** (21/88) |

Perte d'entraînement : 2,81 → 0,82. Pic mémoire ≈ 10,3 Gio / 16 Gio.

### Réponse : oui, le plan transférable monte au-dessus du modèle figé

- **Au-dessus du hasard** : 0,352 / 0,239 / 0,239 → z = 6,45 / 3,22 / 3,22, p binomial ≈ 1e-6 / 0,003 / 0,003. Les trois horizons sont significatifs.
- **Au-dessus du modèle figé (avant)** : +11,4 / +3,4 / +6,8 points (+10 / +3 / +6 évènements sur 88).
- **Geler les cibles ne coûte rien** : `apres` vs `apres_base` diffèrent d'au plus **1 évènement sur 88** → aucun signe de poursuite de cibles ni d'effondrement.

### Réserves à porter dans toute fiche

1. **Le modèle figé est déjà au-dessus du hasard** avant entraînement (p = 0,003 en h1) : une part du retrieval vient de similarité lexicale/de contenu, pas du plan — le contrôle négatif `--melange` n'a pas été lancé ici.
2. **Seul h1 est solide** en gain sur « avant » (z = +1,65 en test non apparié) ; h2 (z = +0,54) et h3 (z = +1,12) restent dans le bruit avec 88 essais — il faudrait 2-3× plus de séries test, ou un test apparié par groupe.
3. In-batch à l'entraînement = 3 candidats, éval = 1 parmi 8 : la perte n'est pas comparable au retrieval.

**Incidents** : aucun. Le dépôt est identique avant/après (git status et sha256 de `tools/plan_entrainement.py` et du JSON de données inchangés) ; seul `/tmp` a été écrit. À signaler : `tools/plan_entrainement.py` était **déjà** marqué modifié (`M`) avant mon lancement — je n'y ai pas touché.

