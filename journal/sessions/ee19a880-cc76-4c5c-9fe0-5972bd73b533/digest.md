# Session DSH — relecture

- identifiant : `ee19a880-cc76-4c5c-9fe0-5972bd73b533`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-08 09:18:22
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave : moteur d'inférence Rust dans drave-core/, outils Python dans tools/, rapports dans reports/). MISSION STRICTEMENT EN LECTURE : n'écris, ne modifie et ne lance AUCUN fichier ni entraînement. Uniquement read/grep/glob et commandes bash de lecture (ls, wc, du, file, head) — jamais rien qui écrive ou télécharge.

Objectif : trouver TOUT ce que le dépôt a lui-même ENTRAÎNÉ ou ajusté côté modèle (poids, boucles d'optimisation, fits), par opposition au travail « moteur » (exécuter des modèles existants GGUF).

À faire :
1. Chercher tous les fichiers de poids/sauvegardes produits localement : *.pt, *.pth, *.npz, *.npy, *.safetensors, *.bin, *.pkl — dans le dépôt et aux emplacements voisins plausibles (~/Data13TB/**, /tmp/drave*, ~/.cache/drave*). Donne chemin, taille, date, et à quoi ils correspondent si un script les lit/écrit.
2. Chercher dans tools/ et à la racine tous les scripts contenant une BOUCLE D'OPTIMISATION ou un APPRENTISSAGE : mots-clés `torch.optim`, `Adam`, `SGD`, `loss.backward`, `lbfgs`, `ridge`, `Ridge(`, `LinearRegression`, `LogisticRegression`, `fit(`, `np.linalg.lstsq`, `gradient`, `epoch`, `entrain`, `train`, `apprend`, `calibre`, `regression`. Pour chaque script trouvé : nom, ce qu'il entraîne (architecture, dimension d'entrée/sortie), corpus/activations utilisées, fonction de coût, nombre d'itérations/epochs, et où il sauvegarde.
3. Priorité absolue aux scripts du « pont » : tools/pont_recurrent.py, pont_fidele.py, pont_reservoir.py, pont_generatif.py, pont_parallele.py, pont_reglages.py, pont_unites.py, cache_pont.py, applique_pont.py, sonde_pont.py, compare_professeurs.py, rapport_du_pont.py, ancre_professeur.py, leviers_pont.py, objectif_du_pont.py. Pour chacun : lis le fichier et décris l'architecture exacte (couches, dimensions, activation, nombre de paramètres si calculable), la cible, la loss, l'optimiseur, le nombre d'itérations par défaut, et le format de sauvegarde.
4. Idem pour les directions/discriminants : discriminant_transfert.py, discriminant_contenu.py, stabilite_directions.py, renforcement_directions.py, renforcement.py, energie_du_contenu.py, transfert_ridge.py, blanchiment_entree.py, sous_espace_du_contenu.py, covariance_cible.py, decomposition.py, amplification.py, calibre_modes.py.
5. Signale tout entraînement de type « professeur » (teacher), distillation, ou calibration de modes.

Rends un tableau/liste dense en français (≤ 70 lignes) : script — type d'apprentissage — entrée/sortie et dimension — cible/loss — optimiseur/itérations par défaut — fichier de poids écrit (chemin, taille si existant). Distingue « lu dans le code » (mesuré) de « supposé ». Inclus les chemins absolus.
Your parent agent id is "48ec07ab-ec9d-4297-a7bf-d84974667e61". Before you finish, send your result to that agent with send_message({ agent_id: "48ec07ab-ec9d-4297-a7bf-d84974667e61", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Inventaire lecture-seule des entraînements et poids locaux du dépôt Drave

Je commence par cartographier le dépôt et chercher les fichiers de poids.

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet | head -60; echo \"---TOOLS---\"; ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools | head -200", "description": "List repo root and tools directory"}`

  ```
total 308
drwxr-xr-x. 1 stephane stephane    612  7 oct 18:16 .
drwxr-xr-x. 1 stephane stephane   2374  3 oct 10:09 ..
drwxr-xr-x. 1 stephane stephane     40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane     56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane     96  1 oct 06:58 data
drwxr-xr-x. 1 stephane stephane   1130  5 oct 13:47 docs
drwxr-xr-x. 1 stephane stephane     82 28 sep 11:58 drave-core
drwxr-xr-x. 1 stephane stephane    164  8 oct 09:11 .git
-rw-r--r--. 1 stephane stephane    399 30 sep 10:01 .gitignore
drwxr-xr-x. 1 stephane stephane     34 27 sep 11:39 journal
drwxr-xr-x. 1 stephane stephane     88 25 sep 17:13 models
drwxr-xr-x. 1 stephane stephane    114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane   4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-------. 1 stephane stephane  36518  2 oct 10:21 README.md
drwxr-xr-x. 1 stephane stephane   4256  7 oct 18:22 reports
-rw-------. 1 stephane stephane 120322  5 oct 16:21 REPRISE.md
-rw-------. 1 stephane stephane   8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 stephane stephane  10507 30 sep 08:44 run_clusters.py
-rw-------. 1 stephane stephane  12507 30 sep 08:44 run_cpu.py
-rw-------. 1 stephan
… [10102 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && find . -type f \\( -name '*.pt' -o -name '*.pth' -o -name '*.npz' -o -name '*.npy' -o -name '*.safetensors' -o -name '*.bin' -o -name '*.pkl' -o -name '*.ckpt' -o -name '*.onnx' -o -name '*.h5' -o -name '*.joblib' \\) -printf '%s\\t% … [119 caractères tronqués]`

  ```
(no output)
  ```

### 🤖 Assistant

⏵ Recherche des poids hors dépôt et des mots-clés d'optimisation

- **bash** `{"command": "echo \"=== models/ ===\"; ls -laR /home/stephane/Data13TB/stephane/GitHub/Qtrinet/models 2>/dev/null | head -40; echo \"=== data/ ===\"; ls -laR /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data 2>/dev/null | head -40; echo \"=== colab/ ===\"; ls -laR /home/stephane/Data13TB/stephane … [305 caractères tronqués]`

  ```
=== models/ ===
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/models:
total 863324
drwxr-xr-x. 1 stephane stephane        88 25 sep 17:13 .
drwxr-xr-x. 1 stephane stephane       612  7 oct 18:16 ..
-rw-r--r--. 1 stephane stephane 352972352 25 sep 17:13 Qwen2.5-0.5B-Q4_0.gguf
-rw-r--r--. 1 stephane stephane 531068480 25 sep 16:52 Qwen2.5-0.5B-Q8_0.gguf
=== data/ ===
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/data:
total 776
drwxr-xr-x. 1 stephane stephane     96  1 oct 06:58 .
drwxr-xr-x. 1 stephane stephane    612  7 oct 18:16 ..
-rw-r--r--. 1 stephane stephane 359041 25 sep 18:02 wikitext2_test.txt
-rw-r--r--. 1 stephane stephane 398564  1 oct 07:37 wikitext2_test.txt.ids
-rw-r--r--. 1 stephane stephane  30005 25 sep 17:53 wt2.json
=== colab/ ===
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/colab:
total 16
drwxr-xr-x. 1 stephane stephane   56 30 sep 12:20 .
drwxr-xr-x. 1 stephane stephane  612  7 oct 18:16 ..
-rw-r--r--. 1 stephane stephane 8858 30 sep 15:11 Drave-reparti.ipynb
-rw-r--r--. 1 stephane stephane 3625 30 sep 13:01 README.md
=== src/ ===
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/src:
total 56
drwxr-xr-x. 1 stephane stephane  208 25 sep 17:41 .
drwxr-xr-
… [1881 caractères tronqués]
  ```

- **bash** `{"command": "echo \"=== Data13TB top (maxdepth 2) ===\"; ls -la /home/stephane/Data13TB/ 2>/dev/null | head -40; echo \"=== /tmp drave* ===\"; ls -lad /tmp/drave* 2>/dev/null; ls -la /tmp/ 2>/dev/null | head -40; echo \"=== ~/.cache/drave* ===\"; ls -lad ~/.cache/drave* 2>/dev/null; ls -la ~/.cache  … [82 caractères tronqués]`

  ```
w-r--r--. 1 stephane stephane    4096  2 oct 15:28 /tmp/drave_prof-qr_norm-24-1.bin
-rw-r--r--. 1 stephane stephane    4096  2 oct 15:29 /tmp/drave_prof-qr_norm-24-2.bin
-rw-r--r--. 1 stephane stephane    4096  2 oct 15:29 /tmp/drave_prof-qr_norm-24-3.bin
-rw-r--r--. 1 stephane stephane    4096  2 oct 15:29 /tmp/drave_prof-qr_norm-24-4.bin
-rw-r--r--. 1 stephane stephane    4096  2 oct 15:29 /tmp/drave_prof-qr_norm-24-5.bin
-rw-r--r--. 1 stephane stephane    4096  2 oct 15:29 /tmp/drave_prof-qr_norm-24-6.bin
-rw-r--r--. 1 stephane stephane    4096  2 oct 15:29 /tmp/drave_prof-qr_norm-24-7.bin
-rw-r--r--. 1 stephane stephane    4096  2 oct 15:29 /tmp/drave_prof-qr_norm-24-8.bin
-rw-r--r--. 1 stephane stephane    4096  2 oct 15:30 /tmp/drave_prof-qr_norm-24-9.bin
-rw-r--r--. 1 stephane stephane    4096  2 oct 15:29 /tmp/drave_prof-qr_norm-2-4.bin
-rw-r--r--. 1 stephane stephane    4096  2 oct 15:28 /tmp/drave_prof-qr_norm-25-0.bin
-rw-r--r--. 1 stephane stephane    4096  2 oct 15:28 /tmp/drave_prof-qr_norm-25-1.bin
-rw-r--r--. 1 stephane stephane    4096  2 oct 15:29 /tmp/drave_prof-qr_norm-25-2.bin
-rw-r--r--. 1 stephane stephane    4096  2 oct 15:29 /tmp/drave_prof-qr_norm-25-3.bin
… [48789 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inventaire ciblé des poids et grep des mots-clés d'optimisation

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet 2>/dev/null; echo \"=== poids DANS le dépôt (hors .git) ===\"; find . -path ./.git -prune -o -type f \\( -name '*.pt' -o -name '*.pth' -o -name '*.npz' -o -name '*.npy' -o -name '*.safetensors' -o -name '*.pkl' -o -name '*.ckpt' -o -nam … [419 caractères tronqués]`

  ```
=== poids DANS le dépôt (hors .git) ===
(fin)

=== .bin dans le dépôt (hors .git, hors binaires ELF) ===
(fin)
  ```

- **bash** `{"command": "echo \"=== comptage /tmp/drave* ===\"; ls /tmp/drave* 2>/dev/null | wc -l; du -shc /tmp/drave* 2>/dev/null | tail -3; echo \"=== familles /tmp/drave* (préfixe) ===\"; ls /tmp/ 2>/dev/null | grep -o '^drave[a-zA-Z0-9_-]*' | sed 's/-[0-9]*-[0-9]*\\.bin$//; s/-[0-9]*\\.bin$//; s/\\.bin$//; … [802 caractères tronqués]`

  ```
=== comptage /tmp/drave* ===
11573
128K	/tmp/drave_prof-q_rope-9-9.bin
4,5M	/tmp/drave_v4_logits.bin
557M	total
=== familles /tmp/drave* (préfixe) ===
     33 drave_prof-q_rope--9
     33 drave_prof-q_rope--8
     33 drave_prof-q_rope--7
     33 drave_prof-q_rope--6
     33 drave_prof-q_rope--5
     33 drave_prof-q_rope--4
     33 drave_prof-q_rope--3
     33 drave_prof-q_rope--2
     33 drave_prof-q_rope--1
     33 drave_prof-q_rope--0
     33 drave_prof-qr_norm--9
     33 drave_prof-qr_norm--8
     33 drave_prof-qr_norm--7
     33 drave_prof-qr_norm--6
     33 drave_prof-qr_norm--5
     33 drave_prof-qr_norm--4
     33 drave_prof-qr_norm--3
     33 drave_prof-qr_norm--2
     33 drave_prof-qr_norm--1
     33 drave_prof-qr_norm--0
=== autres poids hors dépôt: Data13TB (maxdepth 4) ===
1382064	2026-10-05	/home/stephane/Data13TB/stephane/pont_semantique.npz
1382064	2026-10-05	/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique.npz
91596	2026-02-27	/home/stephane/Data13TB/stephane/GitHub/equipment-hauru/.face-encodings-references.pkl
31541	2026-02-26	/home/stephane/Data13TB/stephane/GitHub/equipment-hauru/.face-encodings-raw.pkl
16560	2026-10-05	/home/stephane/Data13TB/stepha
… [106 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Grep des boucles d'optimisation et localisation des scripts écrivant pont_semantique.npz

- **grep** `{"pattern": "torch\\.optim|Adam|SGD|loss\\.backward|lbfgs|LBFGS|Ridge\\(|LinearRegression|LogisticRegression|np\\.linalg\\.lstsq|lstsq|ridge|gradient|epoch|entrain|apprend|calibr|regress|\\.fit\\(|savez|np\\.save|torch\\.save|state_dict", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tool … [22 caractères tronqués]`

  ```
Found 49 matches

tools/vision_mtmd.py
Line 45:                     "libggml-cpu-sandybridge.so"):

tools/trace_gpu.py
Line 14: discipline que la calibration dense/événementiel (`tools/calibre_modes.py`), et
Line 15: `--calibrer` le fait : il trace les mêmes textes dans les deux et rend le cosinus
Line 29:                      [--ctx 256] [--lot 32] [--calibrer dossier_moteur]
Line 139:     if opt("--calibrer", ""):
Line 140:         calibre(sortie, opt("--calibrer", ""), noms)
Line 144: def calibre(gpu_dir, moteur_dir, noms=None):
Line 158:         print("# aucune langue commune : rien à calibrer")
Line 162:     # hors de la calibration d'un modèle qui en a 28.

tools/premiere_couche_semantique.py
Line 107:     np.savez_compressed(sortie, langues=np.array(langues),

tools/mla_synthetique.py
Line 237:     np.save(os.path.join(args.dossier, "logits.npy"), logits)
Line 238:     np.save(os.path.join(args.dossier, "ids.npy"), np.array(ids, np.int64))

tools/calibre_modes.py
Line 2: """calibre_modes.py — le mode DENSE trace-t-il la même chose que le mode ÉVÉNEMENTIEL ?
Line 21: Usage : calibre_modes.py <dossier_textes> <sortie_temp> [--langues eng,fra,deu]

tools/stabilite_directions.py
… [3239 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== qui lit/écrit pont_semantique ===\"; grep -rn \"pont_semantique\\|savez\\|np\\.save\\|\\.npz\" --include=*.py --include=*.sh --include=*.md . 2>/dev/null | grep -v '^\\./\\.git' | head -40", "description": "Find references … [25 caractères tronqués]`

  ```
=== qui lit/écrit pont_semantique ===
./reports/rapport-pont-semantique.md:161:**Artefact** : `/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz`
./reports/rapport-pont-semantique.md:162:**Applicateur** : `python3 tools/applique_pont.py <pont.npz> <trace.drvf>`
./reports/rapport-toutes-langues.md:1565:| **2. Cache** (`cache_pont.py`) | lit les `.drvf` en `.npz` | 16 s |
./reports/rapport-toutes-langues.md:5118:depuis le cache `cache_vf_test.npz` et depuis les traces elles-mêmes. Le chiffre n'était
./reports/rapport-toutes-langues.md:5189:Le 2,487 du §79 avait été mesuré sur `cache_vf_test.npz` — c'est-à-dire sur **es/it/pt**.
./reports/rapport-toutes-langues.md:5445:Les six caches par langue `cache_wiki_{de,en,es,fr,it,pt}.npz` — couche 8, 71 articles
./reports/rapport-toutes-langues.md:5713:`cache_vf_train.npz` → `cache_vf_test.npz` : **1 446 entrées d'apprentissage, 1 446 de test,
./reports/rapport-toutes-langues.md:5781:482 articles, couche 8, **moyenne sur les positions**, 896 canaux, `cache_vf_*.npz` :
./tools/mla_synthetique.py:237:    np.save(os.path.join(args.dossier, "logits.npy"), logits)
./tools/mla_synthetique.py:238:    np.save(os.path.join(args.dossi
… [3158 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des scripts du pont (architecture, cible, loss, sauvegarde)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pont_recurrent.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pont_reservoir.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pont_fidele.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pont_unites.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pont_recurrent.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """pont_recurrent.py — notre pont linguistique-sémantique, appris en BOÎTE NOIRE.
3: 
4: MISSION (clarifiée par Stéphane) : **pas** reproduire le gros modèle couche par
5: couche. Construire un modèle **récurrent à n couches** qui rend, pour n'importe
6: quelle langue, **le premier niveau abstrait** du gros modèle — celui où la
7: représentation cesse d'être dominée par la langue.
8: 
9: Le gros modèle est une BOÎTE NOIRE : on ne prend que son entrée et sa sortie.
10: `--trace-flux` les donne toutes les deux — la couche 0 EST la plongée du jeton,
11: et la couche L EST la cible.
12: 
13:   s_t = A·s_{t−1} + B·e_t        état récurrent (le « pont »)
14:   ŷ_t = s_t                       la sortie visée est l'état abstrait
15: 
16: Ajustement par MOINDRES CARRÉS (crête, forme fermée) — pas de rétropropagation,
17: pas de gradient. Puis essai en BOUCLE FERMÉE : on part de zéro et on laisse la
18: récurrence courir, sans jamais lui donner l'état du professeur.
19: 
20: Usage : pont_recurrent.py <dossier_train> <dossier_test> [--couche 10] [--rang
… [9351 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pont_reservoir.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """pont_reservoir.py — ajouter une COUCHE RÉCURRENTE sans rétropropagation.
3: 
4: Le diagnostic du rapport : sans contexte, le pont plafonne à 0,57 de fidélité,
5: parce que la couche 10 du professeur **agrège tout le préfixe** — un seul jeton ne
6: peut pas la prédire. Il faut donc du contexte.
7: 
8: La réponse qui respecte la contrainte (« pas de rétropropagation ») est un
9: **réservoir** : une couche récurrente **aléatoire et gelée**, dont seule la lecture
10: s'ajuste par moindres carrés.
11: 
12:     s_t = (1−a)·s_(t−1) + a·tanh(A·s_(t−1) + B·e_t)      A, B ALÉATOIRES, GELÉS
13:     y_t = W·s_t + moy                                     W ajusté, forme fermée
14: 
15: C'est « ajouter des couches et des neurones » au sens exact : la taille du
16: réservoir est le nombre de neurones, et la récurrence est la couche ajoutée. Rien
17: ne se rétropropage, et le réservoir n'a besoin d'aucune coordination entre nœuds —
18: il est **distribuable** par construction.
19: 
20: Usage : pont_reservoir.py <train> <test> [--couche 10] [--n 256]
21: ""
… [5235 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pont_fidele.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """pont_fidele.py — émuler le professeur LE PLUS FIDÈLEMENT POSSIBLE, à moindre coût.
3: 
4: Correction d'une faute de mesure : `pont_recurrent.py` comparait la fidélité DANS
5: LE SOUS-ESPACE du rang courant. Comparer un rang 1 et un rang 64 ainsi revient à
6: comparer deux espaces différents — les chiffres ne sont pas comparables, et c'est
7: ce qui faisait « baisser » la fidélité quand on ajoutait des neurones.
8: 
9: Ici tout est mesuré **dans l'espace complet de 896 canaux**, contre la sortie
10: réelle du professeur. Les modèles sont comparés à coût égal et à coût libre :
11: 
12:   - LINÉAIRE de rang r        : y = (e·U)·Vᵀ + moy            (r neurones)
13:   - DEUX COUCHES (ELM)        : y = tanh(e·R)·W              (H neurones cachés)
14:     R est ALÉATOIRE et GELÉ ; seul W s'ajuste, par moindres carrés — aucune
15:     rétropropagation, et R n'a pas besoin d'être distribué de la même façon que W.
16: 
17: Usage : pont_fidele.py <dossier_train> <dossier_test> [--couche 10]
18: """
19: import glob, os, struct, sys
20: import numpy as np
… [5044 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pont_unites.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """pont_unites.py — notre pont, mesuré PAR UNITÉ.
3: 
4: Pendant de `invariance_unites.py`, qui mesure le professeur. Ici on entraîne le
5: pont sur les unités des langues d'apprentissage, on le transporte sur les langues
6: tenues à l'écart, et on mesure :
7: 
8:   - la fidélité (le pont contre la couche du professeur) ;
9:   - l'invariance PAR UNITÉ de notre sortie : pour chaque unité k, la similarité
10:     entre les langues, à contenu égal — dix points de mesure au lieu d'un ;
11:   - la même chose pour le professeur, sur le même panel, pour référence ;
12:   - le diagnostic oracle, sur les deux panneaux.
13: 
14: Les entrées des caches doivent être nommées `<langue>_<k>` (c'est ce que produit
15: le traçage par unité).
16: 
17: Usage : pont_unites.py <train.npz> <test.npz> [--canaux 0.5] [--lecture quadratique]
18: """
19: import sys
20: import numpy as np
21: sys.path.insert(0, "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools")
22: from pont_generatif import Pont, charge, cos_lignes  # noqa: E402
23: 
24: 
25: def inv_par_unite(noms
… [4754 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Fan-out : délégation des scripts « directions/discriminants » et de la racine, pendant que je lis pont_generatif.py

- **subagent** `{"description": "Analyser scripts directions/discriminants", "prompt": "MISSION STRICTEMENT EN LECTURE SEULE. Tu ne dois RIEN écrire, RIEN modifier, RIEN exécuter qui écrive ou télécharge. Uniquement read/grep/glob et commandes bash de lecture (ls, wc, file, head). Tu ne dois PAS lancer les scripts  … [2167 caractères tronqués]`
- **subagent** `{"description": "Chercher entraînements hors tools", "prompt": "MISSION STRICTEMENT EN LECTURE SEULE. Tu ne dois RIEN écrire, RIEN modifier, RIEN exécuter qui écrive ou télécharge. Uniquement read/grep/glob et commandes bash de lecture (ls, wc, du, file, head). N'exécute AUCUN script Python du dépôt … [2273 caractères tronqués]`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pont_generatif.py", "limit": 160}`

  ```
started subagent f3ca67c4-b171-4eee-9e14-29f9dd1c8c23
  ```


  ```
started subagent 67637ea9-78c6-4c20-a77c-0f90ee2a9ddc
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pont_generatif.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """pont_generatif.py — le réseau NAÎT, puis subit une ATTRITION qui le fait généraliser.
3: 
4: Deux phases, dans cet ordre, et c'est l'apprentissage qui décide des tailles.
5: 
6: PHASE GÉNÉRATIVE. On part d'un seul neurone. Chaque pas de croissance ajoute une
7: COUCHE de neurones. Une couche nouvelle ne lit que les couches ANTÉRIEURES (plus
8: elle-même) : jamais l'inverse. Conséquence exacte, et c'est ce qui rend la
9: croissance gratuite — les trajectoires déjà calculées ne sont PAS perturbées, on
10: ne calcule que la couche qui naît. Le coût total de la croissance vaut donc à peu
11: près celui du réseau final, pas la somme de tous les états intermédiaires.
12: 
13: PHASE D'ATTRITION. Périodiquement, on retire les neurones REDONDANTS — ceux dont
14: la trajectoire se reconstruit à partir des autres — puis on RÉAJUSTE la lecture
15: sur les survivants. C'est le réajustement qui fait généraliser : la capacité
16: retirée doit être réabsorbée par les unités qui restent, ce qui remplace des
17: détecteurs particuliers par des concepts plus
… [7663 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des méthodes de fit et de la boucle d'attrition de pont_generatif.py

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && grep -n \"    def \\|^def \\|np.linalg.solve\\|np.linalg.lstsq\\|savez\\|np.save\\|while \\|for .* in range(\\|attrition\\|patience\\|max_couches\\|seuil\\|ride\\|mu_inv\\|mu_cont\" pont_generatif.py | head -120", "description" … [48 caractères tronqués]`

  ```
24:  pont_generatif.py <train.npz> <test.npz> [--a 0.2] [--ride 0.3] [--val 4]
25:                    [--attrition 1] [--seuil 0.02] [--max-couches 9] [--graine 5]
32:def charge(p):
35:    E = [z[f"E{i}"].astype(np.float32) for i in range(len(cles))]
36:    Y = [z[f"Y{i}"].astype(np.float32) for i in range(len(cles))]
40:def cos_lignes(A, B):
46:def inv(V):
76:    def __init__(self, donnees, a, graine, H, decal=0):
85:        # retirés. Sans elle, une attrition ne réduit rien — elle masque.
111:        self.mu_inv = 0.0
116:        self.mu_cont = 0.0
135:    def debut_couche(self, c):
138:    def taille_couche(self, c):
142:    def nait(self, k, nouvelle_couche=True):
180:        for d in range(0, len(ordre), LC):
194:            for t in range(Tmax):
206:        for r in range(k):
217:    def _norm(self, X):
223:    def phi(self, X):
230:    def ajuste(self, idx, ride, mt, quel=slice(None)):
263:        # définie positive : on le SIGNALE au lieu de le taire, et le ride garantit
269:        mu_lang = getattr(self, "mu_inv", 0.0)
270:        mu_cont = getattr(self, "mu_cont", 0.0)
271:        if mu_lang > 0.0 or mu_cont > 0.0:
279:            if mu_cont > 0.0:
295:                  
… [4063 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && wc -l pont_generatif.py && sed -n '160,340p' pont_generatif.py", "description": "Read pont_generatif lines 160-340"}`

  ```
1041 pont_generatif.py
        B = self.rng.randn(k, self.H) / np.sqrt(self.H) * self.gain_entree
        # constante de temps de chaque nouveau-né (multi-échelle si `a_min` posé)
        if self.a_min is None:
            a_n = np.full(k, self.a)
        else:
            a_n = np.exp(np.linspace(np.log(self.a_min), np.log(self.a_max), k))

        # ---------------------------------------------------------------- BLOCS
        #
        # POURQUOI DES BLOCS. La boucle ci-dessus est `pour chaque langue : pour
        # chaque pas`, soit 472 472 itérations d'interpréteur Python — 28 s PAR
        # NAISSANCE, et une naissance par neurone en mode libre. Or **les langues
        # sont indépendantes** : seule la récurrence en `t` est séquentielle. On
        # regroupe donc les langues par longueurs voisines et on boucle sur `t`,
        # toutes les langues du bloc d'un coup. Les itérations Python passent de
        # 472 472 à la somme des longueurs maximales de chaque bloc, soit environ
        # 472 472 / LC. Le CALCUL EST LE MÊME — c'est une vectorisation, pas un
        # changement d'algorithme.
        LC = int(getattr(self, "bloc_langues", 16))
        ordre = sorted(range(l
… [8042 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && echo \"=== save/écriture dans tools/*.py ===\"; grep -rn \"np\\.save\\|savez\\|torch\\.save\\|open(.*['\\\"]w\\|pickle\\.dump\\|joblib\\.dump\" *.py | grep -v \"^ref_logits\" | head -40; echo; echo \"=== options pont_generatif  … [151 caractères tronqués]`

  ```
=== save/écriture dans tools/*.py ===
aiguille.py:206:        with open(args.journal, "w", encoding="utf-8") as f:
applique_pont.py:76:        np.save(sys.argv[sys.argv.index("--sortie") + 1], A)
cache_pont.py:79:    np.savez_compressed(sortie, cles=np.array(cles), hidden=hidden,
clusters_moe.py:218:        json.dump(resultat, open(args.json, "w"), indent=1)
controle_capacite.py:140:    with open(csv, "w") as fh:
convertir_clusters.py:200:    with open(chemin, "wb") as f:
convertir_clusters.py:391:    with open(chemin, "w", encoding="utf-8") as fo:
convertir_clusters.py:531:    with open(os.path.join(args.dossier, "manifeste.json"), "w", encoding="utf-8") as f:
decoupe_langues.py:69:              open("/tmp/decoupe392.json", "w"), indent=1)
engram_reference.py:195:        with open(f, "w") as g:
extrait_article1.py:89:        with open(os.path.join(sortie, f"{code}.txt"), "w", encoding="utf-8") as g:
extrait_crime.py:86:            open(p, "w", encoding="utf-8").write(S[i])
extrait_gutenberg.py:36:    with open(sortie, "w") as f:
extrait_udhr.py:81:    with open(sortie, "w", encoding="utf-8") as out:
extrait_wikipedia.py:41:    with open(sortie, "w") as s:
harmony_canonique.py:27: 
… [4816 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && sed -n '760,800p' pont_generatif.py; echo \"======= 880-1041 =======\"; sed -n '880,1041p' pont_generatif.py", "description": "Read pont_generatif main loop and end"}`

  ```
Yte_a = np.vstack(Yte)
    base = cos_lignes(np.tile(mt, (len(Yte_a), 1)), Yte_a)
    print(f"# constante témoin sur le TEST : {base:.4f}")

    # valeur de repli complète : sans elle, un réseau que l'attrition n'améliore
    # jamais faisait planter le résumé final APRÈS des heures de calcul
    # sous-ensemble FIXE pour le diagnostic d'apprentissage (voir plus bas)
    itr_diag = itr[::8]
    meilleur = {"f_va": -1.0, "f_te": -1.0, "neur": 0, "couch": 0,
                "f_tr": 0.0, "inv": 0.0, "pire": 0.0, "etape": "aucune"}
    for cycle in range(1, cycles+1):
        # ------------------------------------------------------- CROISSANCE
        print(f"\n########## CYCLE {cycle} — CROISSANCE ##########")
        print(f"{'après':<30} {'neur.':>6} {'couch.':>7} {'fid appr':>9} {'fid VAL':>8} "
              f"{'fid TEST':>9} {'invar.':>8} {'pire':>7}")
        # ------------------------------------------------------------ NAISSANCE
        #
        # `--naissance libre` : UN neurone à la fois. Aucun chiffre rond ne doit
        # sortir d'ici — 1, 2, 4, 8, … 256 étaient MON calendrier et MON plafond,
        # pas une découverte. Un compte rond est le signe qu'on a choisi la tai
… [10548 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des autres scripts du pont et des artefacts .npz écrits

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && for f in cache_pont.py applique_pont.py sonde_pont.py compare_professeurs.py ancre_professeur.py; do echo \"########## $f ##########\"; cat -n \"$f\" | head -95; echo; done", "description": "Read 5 pont helper scripts"}`

  ```
########## cache_pont.py ##########
     1	#!/usr/bin/env python3
     2	"""cache_pont.py — parse UNE fois les traces, puis toutes les expériences sont rapides.
     3	
     4	Le goulot de `pont_reservoir.py` n'est pas le réservoir (64 neurones, quelques
     5	milliers de pas) mais la LECTURE : 2,1 Go de DRVF en Python pur, ~10 min par
     6	essai. Hors de question de balayer des réglages à ce prix.
     7	
     8	Usage : cache_pont.py <dossier> <sortie.npz> [--couche 10] [--hidden 896]
     9	"""
    10	import glob, os, struct, sys
    11	import numpy as np
    12	
    13	
    14	def lire(chemin):
    15	    def paires(f, n, version, bloc=32):
    16	        ech = None
    17	        if version == 3:
    18	            nb, = struct.unpack("<I", f.read(4))
    19	            ech = [struct.unpack("<e", f.read(2))[0] for _ in range(nb)]
    20	        out, prev = [], 0
    21	        for _ in range(n):
    22	            if version == 1:
    23	                i, = struct.unpack("<I", f.read(4))
    24	            else:
    25	                e, = struct.unpack("<B", f.read(1))
    26	                i = struct.unpack("<H", f.read(2))[0] if e == 255 else prev + e
    27	           
… [19099 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && echo \"##### leviers_pont.py #####\"; sed -n '1,60p' leviers_pont.py; echo \"##### objectif_du_pont.py #####\"; sed -n '1,60p' objectif_du_pont.py; echo \"##### rapport_du_pont.py #####\"; sed -n '1,45p' rapport_du_pont.py; ech … [200 caractères tronqués]`

  ```
##### leviers_pont.py #####
#!/usr/bin/env python3
"""QUATRE LEVIERS POUR LES LANGUES NON SERVIES — mesurés sur le MÊME vivier.

ÉTABLI (§27) : l'apport propre du pont (`fidélité − témoin constant`) vaut +0,0885
sur `dzo` mais +0,0014 sur `heb`. Sur `deu`, `jpn`, `kor`, `heb`, `srp`, ni la
constante ni le pont ne servent à grand-chose. Et un ajustement PRIVÉ (l'oracle)
ne les sauve pas non plus : deu 0,539, jpn 0,575. Le goulot est donc dans les
CARACTÉRISTIQUES, pas dans le partage.

Quatre candidats, à nombre de neurones constant quand c'est possible :

  A. référence    — 1 couche de 40 neurones, lecture quadratique
  B. + entrée     — la lecture voit AUSSI le jeton courant `e_t` (connexion directe)
  C. entrée seule — la lecture ne voit QUE `e_t`, aucun neurone. C'est le TÉMOIN qui
                    dit si le réservoir sert à quelque chose : si C ≈ A, tout le
                    travail est déjà fait par la couche 0.
  D. 2 couches    — 20 + 20 neurones. Même budget, composition en plus. C'est la
                    question de la mission : une couche de plus achète-t-elle
                    quelque chose que des neurones en plus n'achètent pas ?

MÉMOIRE. Les variantes B et
… [9258 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection des artefacts .npz sur disque et des autres scripts écrivant des poids

- **bash** `{"command": "for f in /home/stephane/Data13TB/stephane/pont_semantique.npz /home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique.npz /home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz; do echo \"=== $f ===\"; ls -la \"$f\" 2>/dev/null; file \"$f\" 2>/dev/null; echo \"--- en-t … [331 caractères tronqués]`

  ```
=== /home/stephane/Data13TB/stephane/pont_semantique.npz ===
-rw-r--r--. 1 stephane stephane 1382064  5 oct 10:45 /home/stephane/Data13TB/stephane/pont_semantique.npz
/home/stephane/Data13TB/stephane/pont_semantique.npz: Zip archive data, made by v4.5 UNIX, extract using at least v4.5, last modified Jan 01 1980 00:00:00, uncompressed size 458880, method=store
--- en-tête (noms/shapes des tableaux) ---
P.npy
NUMPY
{'descr': '<f4', 'fortran_order': True, 'shape': (896, 128), }                                                       
(m<7
$<,q
.|=o@-
X;|J
9j$!
G<%1
	=ex
;0}<
!<@5Y
>IB<
]g(=
a<O=
;h1Q
<J,?
;KvJ
0X,<
7<yX=
v]:O.
<s02;
XM<l=
>k)v<
<$i(

=== /home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique.npz ===
-rw-r--r--. 1 stephane stephane 1382064  5 oct 10:47 /home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique.npz
/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique.npz: Zip archive data, made by v4.5 UNIX, extract using at least v4.5, last modified Jan 01 1980 00:00:00, uncompressed size 458880, method=store
--- en-tête (noms/shapes des tableaux) ---
P.npy
NUMPY
{'descr': '<f4', 'fortran_order': True, 'shape': (896, 128), }                               
… [1124 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== premiere_couche_semantique.py (artefact) ===\"; sed -n '1,30p;95,120p;200,230p' tools/premiere_couche_semantique.py; echo; echo \"=== git: fichiers poids supprimés/jamais commités ===\"; git log --oneline -8 2>/dev/null; e … [273 caractères tronqués]`

  ```
=== premiere_couche_semantique.py (artefact) ===
#!/usr/bin/env python3
"""premiere_couche_semantique.py — À QUELLE COUCHE la langue cesse-t-elle de dominer ?

POURQUOI DEUX ARTICLES, ET PAS UN. La similarité entre les représentations d'une
même phrase dans 399 langues monte forcément avec la profondeur — mais elle monte
AUSSI si la couche devient simplement anisotrope, c'est-à-dire si tous les
vecteurs se ressemblent pour une raison qui n'a rien de sémantique. Un chiffre qui
monte ne prouve donc rien à lui seul.

Le contrôle est donc : **le même article dans deux langues** contre **un autre
article dans deux autres langues**. Ce que la couche sait du SENS est ce qui
sépare les deux, et c'est cette SÉPARATION qu'on suit couche par couche :

    même(c)      = cos( art1 langue i , art1 langue j )     i ≠ j
    autre(c)     = cos( art1 langue i , art2 langue j )     i ≠ j
    séparation   = même(c) − autre(c)

La couche où la séparation culmine est la **première couche sémantique** : celle
où le modèle a fini de traduire et commence à raisonner. C'est la cible naturelle
d'un pont, et savoir où elle est évite de viser une couche au hasard.

DEUX POOLINGS, PARCE QUE LE §84 A MONTRÉ QUE
… [4876 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche de l'origine des fichiers /tmp/drave_prof-*.bin et des lecteurs du pont

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== qui écrit /tmp/drave_prof ===\"; grep -rn \"drave_prof\\|drave_v4_logits\" --include=* . 2>/dev/null | grep -v '^\\./\\.git' | head -20; echo \"(fin)\"; echo; echo \"=== qui lit pont_semantique.npz ===\"; grep -rn \"pont_s … [355 caractères tronqués]`

  ```
=== qui écrit /tmp/drave_prof ===
(fin)

=== qui lit pont_semantique.npz ===
./reports/rapport-pont-semantique.md:131:jeton suivant depuis l'état (`tools/sonde_pont.py`).
./reports/rapport-pont-semantique.md:161:**Artefact** : `/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz`
./reports/rapport-pont-semantique.md:162:**Applicateur** : `python3 tools/applique_pont.py <pont.npz> <trace.drvf>`
./tools/pont_recurrent.py:189:    #     et pas seulement une mesure. `pont_semantique.npz` porte les trois pièces
./tools/pont_recurrent.py:191:    chemin = os.environ.get("DRAVE_PONT_SORTIE", "pont_semantique.npz")
./tools/pont_recurrent.py:195:    print(f"#   usage : python3 tools/applique_pont.py {chemin} <trace.drvf>")
./tools/applique_pont.py:2:"""applique_pont.py — le pont s'applique à N'IMPORTE QUELLE trace, langue inconnue.
./tools/applique_pont.py:4:Le pont est un artefact : trois matrices ajustées une fois (`pont_semantique.npz`),
./tools/applique_pont.py:12:Usage : applique_pont.py <pont.npz> <trace.drvf> [--sortie abstrait.npy]
./tools/sonde_pont.py:2:"""sonde_pont.py — le pont garde-t-il l'information PRÉDICTIVE du professeur ?
./tools/sonde_pont.py:19:Usage : son
… [3000 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== mentions professeur/distillation/teacher dans tools+rapports (comptage) ===\"; grep -rlic \"distillation\\|teacher\\|professeur\" tools/*.py 2>/dev/null | head -5; echo \"--- fichiers tools mentionnant 'professeur' ---\";  … [266 caractères tronqués]`

  ```
=== mentions professeur/distillation/teacher dans tools+rapports (comptage) ===
tools/amplification.py
tools/ancre_professeur.py
tools/applique_pont.py
tools/approximabilite_bloc.py
tools/blanchiment_entree.py
--- fichiers tools mentionnant 'professeur' ---
tools/amplification.py
tools/ancre_professeur.py
tools/applique_pont.py
tools/blanchiment_entree.py
tools/compare_professeurs.py
tools/covariance_cible.py
tools/decomposition.py
tools/discriminant_contenu.py
tools/discriminant_transfert.py
tools/energie_du_contenu.py
tools/etats_sans_langue.py
tools/extrait_article1.py
tools/extrait_wikipedia.py
tools/invariance_ou_appauvrissement.py
tools/lecture_invariante.py
tools/localite_couches.py
tools/objectif_du_pont.py
tools/ou_entre_la_langue.py
tools/ou_est_le_contenu.py
tools/pont_fidele.py
tools/pont_generatif.py
tools/pont_recurrent.py
tools/pont_reservoir.py
tools/pont_unites.py
tools/profil_couches.py
tools/profil_langues.py
tools/rapport_du_pont.py
tools/renforcement_directions.py
tools/renforcement.py
tools/sonde_pont.py

=== distillation / teacher explicite ===
tools/approximabilite_bloc.py:5:Question préalable à toute distillation (idée de Stéphane : distiller les couches
to
… [352 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de l'origine des dumps .bin et lecture du rapport du pont

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 'drave_' dans sources C++/sh (dumps) ===\"; grep -rn \"drave_\\|\\.bin\" tools/ref_logits.cpp tools/sonde-passe-k3.sh tools/test-plage-k3.sh 2>/dev/null | head -25; echo \"(fin)\"; echo; echo \"=== taille rapport-pont-sema … [286 caractères tronqués]`

  ```
=== 'drave_' dans sources C++/sh (dumps) ===
tools/ref_logits.cpp:3:// Usage : ref_logits <modele.gguf> <ids.txt> <sortie.bin> [n_max]
tools/ref_logits.cpp:8://   - écrit <sortie.bin> en petit-boutiste :
tools/ref_logits.cpp:68:        std::fprintf(stderr, "usage: %s <modele.gguf> <ids.txt> <sortie.bin> [n_max] [--sans-yarn]\n", argv[0]);
tools/ref_logits.cpp:246:                    std::snprintf(chemin, sizeof(chemin), "%s-%s.bin", dump, nom.c_str());
tools/test-plage-k3.sh:20:R=/tmp/plage_relais.bin
tools/test-plage-k3.sh:42:    b=/tmp/pl_B-l_out-25-$i.bin; c=/tmp/pl_C-l_out-25-$i.bin
(fin)

=== taille rapport-pont-semantique.md ===
355 reports/rapport-pont-semantique.md
=== extraits clés ===
26:Un étudiant `s_t = A·s_{t-1} + B·e_t` ajusté par moindres carrés (crête, forme
31:| rang 32 | 0,5822 | 0,0447 |
32:| rang 64 | 0,5380 | 0,0016 |
33:| rang 128 | 0,4912 | 0,0579 |
34:| rang 256 | 0,5654 | 0,1266 |
38:1,424 à 0,70** — ce n'est donc pas une divergence, c'est que *l'ajustement local
57:## Résultat 3 — LE PONT : une matrice 896×896 qui rend la langue invisible
59:Le même ajustement linéaire, jugé non plus sur sa fidélité mais sur
74:C'est un **projecteur sur le partagé**, obte
… [1766 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '100,175p' reports/rapport-pont-semantique.md", "description": "Read pont-semantique report conclusion"}`

  ```
Intuition de Stéphane : commencer avec **un neurone par sortie**, puis itérer en
ajoutant des neurones pour les exclusivités — l'apprentissage est **hyper-rapide au
début**. C'est exactement le **rang** du pont. Courbe mesurée, 20 langues
d'entraînement → 20 langues jamais vues :

| neurones | fidélité au professeur | **invariance inter-langue** | **pire paire** |
|---|---:|---:|---:|
| **1** | 0,6677 | **0,9492** | **0,7762** |
| 2 | 0,7170 | 0,9347 | 0,8252 |
| 4 | 0,7479 | 0,9139 | 0,7769 |
| 8 | 0,7467 | 0,8847 | 0,6739 |
| 16 | 0,7262 | 0,8431 | 0,5189 |
| 64 | 0,6816 | 0,7658 | 0,4842 |

**Un seul neurone donne 0,9492 d'invariance** — contre **0,6284** pour le
professeur, et **0,471** pour le plateau d'un modèle de **30 B**. Sa pire paire,
**0,7762**, écrase le 0,3281 du professeur.

**Et la courbe dit pourquoi** : le premier neurone capte la **direction partagée,
indépendante de la langue** — c'est le pont brut au sens exact. Les neurones
suivants ajoutent du **détail propre à chaque langue** : la fidélité au professeur
monte (0,668 → 0,748) mais **l'invariance baisse, monotonement** (0,949 → 0,766).

**Il y a donc un compromis, et il est net** : si l'on veut copier le profe
… [2466 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recensement systématique des scripts ajustant une lecture par forme fermée

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && echo \"=== scripts avec np.linalg.solve/lstsq/pinv (ajustement forme fermée) ===\"; grep -l \"np\\.linalg\\.solve\\|np\\.linalg\\.lstsq\\|np\\.linalg\\.pinv\" *.py | while read f; do n=$(grep -c \"np\\.linalg\\.solve\\|np\\.lin … [503 caractères tronqués]`

  ```
=== scripts avec np.linalg.solve/lstsq/pinv (ajustement forme fermée) ===
blanchiment_entree.py : 1
controle_capacite.py : 1
corpus_neuf.py : 1
discriminant_contenu.py : 1
discriminant_transfert.py : 1
energie_du_contenu.py : 1
etats_sans_langue.py : 1
grand_et_entree.py : 1
lecture_locale.py : 1
leviers_pont.py : 1
localite_couches.py : 3
ou_entre_la_langue.py : 1
ou_est_le_contenu.py : 2
pont_fidele.py : 2
pont_generatif.py : 3
pont_parallele.py : 1
pont_recurrent.py : 2
pont_reglages.py : 1
pont_reservoir.py : 1
pont_unites.py : 1
profil_langues.py : 2
renforcement_directions.py : 1
sonde_pont.py : 1
stabilite_directions.py : 1
transfert_ridge.py : 3

=== scripts avec .fit( ou sklearn ===
(fin)

=== scripts avec torch ===
mhc_v41_synthetique.py
trace_gpu.py
(fin)

=== scripts avec backward/optim ===
(fin)
  ```

- **bash** `{"command": "command -v unzip >/dev/null && for f in /home/stephane/Data13TB/stephane/pont_semantique.npz /home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz; do echo \"=== $f ===\"; unzip -l \"$f\" 2>/dev/null; done || echo \"unzip absent\"; echo \"=== extrait REPRISE.md sur l'artef … [149 caractères tronqués]`

  ```
=== /home/stephane/Data13TB/stephane/pont_semantique.npz ===
Archive:  /home/stephane/Data13TB/stephane/pont_semantique.npz
  Length      Date    Time    Name
---------  ---------- -----   ----
   458880  1980-01-01 00:00   P.npy
     3712  1980-01-01 00:00   moy.npy
   917632  1980-01-01 00:00   W0.npy
      136  1980-01-01 00:00   couche.npy
      136  1980-01-01 00:00   rang.npy
      368  1980-01-01 00:00   langues_train.npy
      368  1980-01-01 00:00   langues_test.npy
---------                     -------
  1381232                     7 files
=== /home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz ===
Archive:  /home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz
  Length      Date    Time    Name
---------  ---------- -----   ----
     3712  1980-01-01 00:00   P.npy
     3712  1980-01-01 00:00   moy.npy
     7296  1980-01-01 00:00   W0.npy
      136  1980-01-01 00:00   couche.npy
      136  1980-01-01 00:00   rang.npy
      368  1980-01-01 00:00   langues_train.npy
      368  1980-01-01 00:00   langues_test.npy
---------                     -------
    15728                     7 files
=== extrait REPRISE.md sur l'artefact ===
> | 4 | 0,748 | 
… [1191 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de l'en-tête de W0.npy et recensement des fits ridge restants

- **bash** `{"command": "for f in /home/stephane/Data13TB/stephane/pont_semantique.npz /home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz; do echo \"=== $f ===\"; for e in P.npy moy.npy W0.npy couche.npy rang.npy; do printf '%-10s ' \"$e\"; unzip -p \"$f\" \"$e\" 2>/dev/null | head -c 200 | str … [93 caractères tronqués]`

  ```
=== /home/stephane/Data13TB/stephane/pont_semantique.npz ===
P.npy      NUMPY {'descr': '<f4', 'fortran_order': True, 'shape': (896, 128), }                                                        (m<7 
moy.npy    NUMPY {'descr': '<f4', 'fortran_order': False, 'shape': (896,), }                                                           Y?<<d@r 
W0.npy     NUMPY {'descr': '<f8', 'fortran_order': False, 'shape': (896, 128), }                                                       
couche.npy NUMPY {'descr': '<i8', 'fortran_order': False, 'shape': (), }                                                               
rang.npy   NUMPY {'descr': '<i8', 'fortran_order': False, 'shape': (), }                                                               
=== /home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz ===
P.npy      NUMPY {'descr': '<f4', 'fortran_order': False, 'shape': (896, 1), }                                                         (m<7 
moy.npy    NUMPY {'descr': '<f4', 'fortran_order': False, 'shape': (896,), }                                                           Y?<<d@r 
W0.npy     NUMPY {'descr': '<f8', 'fortran_order': False, 'shape': (896, 1), }       
… [269 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && for f in localite_couches.py lecture_locale.py lecture_invariante.py sous_ensemble_actif.py ou_est_le_contenu.py ou_entre_la_langue.py etats_sans_langue.py grand_et_entree.py controle_capacite.py corpus_neuf.py profil_langues.p … [342 caractères tronqués]`

  ```
--- localite_couches.py ---
12:Régression ridge, forme fermée. On lit :
29:                            [--langues en] [--ride 1.0] [--max-articles 50]
100:    ride = float(opt("--ride", 1.0))
115:    print(f"# {len(retenus)} traces · fenêtre {K} · ride {ride} · "
188:                # Le symptome etait une colonne d=0 a 0,005 la ou la meme quantite
211:                W = np.linalg.solve(g + ride*npts[d]*np.eye(1792), dd)
--- lecture_locale.py ---
10:solution en forme fermée (ridge), et c'est ELLE qui impose la Gram dense.
13:solution : les moindres carrés moyens normalisés (NLMS) —
20:LA QUESTION MESURÉE : cette règle atteint-elle la fidélité du ridge ?
24:PRÉDICTION, ÉCRITE AVANT LA MESURE : NLMS doit approcher le ridge sur le panneau
49:    graine, ride = 5, 0.03
50:    etas = [float(x) for x in opt("--etas", "0.01,0.05,0.2,0.5,1.0").split(",")]
--- lecture_invariante.py ---
16:    (XᵀX + μ·C + ride·I) W = Xᵀ(Y − mt),   C = Σ_i n_i (M_i − M̄)ᵀ(M_i − M̄)
54:    ride, graine = 0.03, 5
94:        W = P.ajuste(idx, ride, mt, iap)
--- sous_ensemble_actif.py ---
--- ou_est_le_contenu.py ---
81:    ride, graine = 0.03, 5
136:        W = np.linalg.solve(G + ride*ntot*np.eye(G.shape[0]),
… [2303 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des scripts « synthétiques » (torch) et statut des sous-agents

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && for f in mhc_v41_synthetique.py mla_synthetique.py trace_gpu.py v41_compresseur_reference.py v41_experts_reference.py pair_factice.py engram_reference.py clusters_moe.py; do echo \"--- $f ---\"; grep -n \"torch\\.\\|apprend\\|e … [231 caractères tronqués]`

  ```
--- mhc_v41_synthetique.py ---
11:  * `vllm/model_executor/kernels/mhc/torch.py` → `mhc_pre_delayed_torch`
--- mla_synthetique.py ---
--- trace_gpu.py ---
61:    dev = "cuda" if torch.cuda.is_available() else "cpu"
62:    if dev == "cuda" and torch.cuda.device_count() > 1:
65:        libre = [torch.cuda.mem_get_info(i)[0] for i in range(torch.cuda.device_count())]
68:    mdl = AutoModel.from_pretrained(modele, dtype=torch.float32).to(dev).eval()
95:        with torch.no_grad():
--- v41_compresseur_reference.py ---
--- v41_experts_reference.py ---
--- pair_factice.py ---
--- engram_reference.py ---
--- clusters_moe.py ---

=== mla_synthetique: que fait-il ? ===
#!/usr/bin/env python3
"""Modèle MLA synthétique + référence numpy — le harnais du chantier 5.

MLA (attention latente, DeepSeek-V2/V3) n'est pas testable en l'état : aucun
modèle MLA en GGUF sur cette machine (le « deepseek-r1-distill » local est un
Qwen dense). Ce script fabrique donc un modèle minuscule dont les poids sont
aléatoires mais les FORMES correctes, l'écrit en GGUF, et calcule une référence
indépendante en numpy — c'est elle que le moteur devra retrouver.

Pourquoi c'est un vrai test : la référence est écrite à 
… [379 caractères tronqués]
  ```

- **list_agents** `{}`

  ```
f3ca67c4-b171-4eee-9e14-29f9dd1c8c23 [running] — Analyser scripts directions/discriminants
67637ea9-78c6-4c20-a77c-0f90ee2a9ddc [running] — Chercher entraînements hors tools
  ```

### 🤖 Assistant

⏵ Vérification des scripts de clustering d'experts (k-means = ajustement non supervisé)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== kmeans/centroides/clustering (tout le dépôt, scripts) ===\"; grep -rln \"kmeans\\|KMeans\\|k_means\\|centroide\\|centroid\\|cluster\" --include=*.py . 2>/dev/null | grep -v '^\\./\\.git' | head -20; echo; for f in tools/cl … [313 caractères tronqués]`

  ```
=== kmeans/centroides/clustering (tout le dépôt, scripts) ===
./run_clusters.py
./run_real_clusters.py
./tools/clusters_moe.py
./tools/convertir_clusters.py
./tools/analyse_empreinte.py
./tools/analyse_experts_statique.py

--- tools/clusters_moe.py (extrait) ---
156:          f"{len(next(iter(par_couche.values()))[0])} par jeton")
--- tools/convertir_clusters.py (extrait) ---
436:        premier = next(iter(experts.values()))[0]
--- tools/analyse_experts_statique.py (extrait) ---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== scripts racine: apprentissage ? ===\"; for f in run_*.py; do echo \"--- $f ---\"; grep -n \"fit(\\|solve\\|lstsq\\|optim\\|backward\\|train\\|epoch\\|apprend\" \"$f\" | head -3; done 2>/dev/null | head -50", "description": … [31 caractères tronqués]`

  ```
=== scripts racine: apprentissage ? ===
--- run_8bit_perfection.py ---
--- run_clusters.py ---
5:Question : peut-on optimiser le modèle *à la conversion* pour créer des grappes
19:Usage :  python3 run_clusters.py [--epochs 400] [--groups 4]
87:def run_config(cross: float, groups: int, epochs: int, verbose: bool = True):
--- run_cpu.py ---
261:         "> d'un noyau optimisé (SIMD, multi-thread, accumulateurs par banc) peut aller",
--- run_encoding.py ---
17:Usage :  python3 run_encoding.py [--epochs 400] [--retrain 150]
33:from run_quantify import build_and_train  # noqa: E402
84:def measure(model, Xtr, ytr, Xte, yte, W1_0, W2_0, masks, k, retrain):
--- run_harness.py ---
--- run_list_mode.py ---
137:          "   même la bonne réponse à la contrainte « aucun DSP » du cahier des charges.",
149:          "5. **Conséquence majeure** : la contrainte « pas de DSP » **n'exige pas** des poids",
--- run_precision.py ---
20:Protocole : recette standard prune → retrain → quantize (le réentraînement à masque
21:fixe est indispensable, sinon on mesure surtout la casse du post-training).
23:Usage :  python3 run_precision.py [--epochs 400] [--retrain 150]
--- run_quantify.py ---
14:Usage :  pyt
… [707 caractères tronqués]
  ```

### 👤 Utilisateur

Agent 67637ea9-78c6-4c20-a77c-0f90ee2a9ddc sent a message:
RÉSULTAT (lecture seule, aucun script exécuté). Entraînement hors tools/ dans Qtrinet :

1) SEUL code d'apprentissage réel hors tools/ : src/tiny_model.py (115 l., numpy pur, zéro dépendance ML).
- Architecture : MLP 2 couches 32→64→10 (LU l.22, 55 ; docstring l.8 « l'élève (MLP 32→64→10) »), ReLU + softmax.
- Corpus : SYNTHÉTIQUE, pas de texte — vecteurs gaussiens 32 dims étiquetés en 10 classes par un « professeur » MLP aléatoire FIGÉ (teacher_seed=1234, LU l.30-40).
- Loss : cross-entropy softmax, gradient calculé à la main (LU l.97-104, 110) — pas de torch, pas de loss.backward().
- Optimiseur : SGD manuel `p -= lr*g` (LU l.105-106). Défauts : epochs=300, lr=0.05, batch=128 (LU l.81). Masques (mask1,mask2) appliqués après chaque pas = « prune → retrain à masque fixe » (LU l.83-84, 107-109).
- POIDS ÉCRITS : AUCUN. Grep exhaustif np.save/savez/torch.save/state_dict/pickle.dump/.npz/.npy/.pt/.pth/safetensors sur tout le dépôt hors tools/ = 0 occurrence.

2) Scripts RACINE qui appellent cet entraînement (tous sortent des .md, jamais des poids) :
- run_quantify.py : build_and_train() l.40-47 (train epochs=300 défaut l.291, lr 0.05) ; constantes D_IN,D_HID,N_CLASS=32,64,10 l.36 ; N_TRAIN,N_TEST=4096,1024 l.37.
- run_clusters.py : m.train(..., l.95 (avec masques de grappes) et l.140, --epochs défaut 400 l.116.
- run_precision.py : build_and_train + model.train(epochs=args.retrain, lr=0.02) l.105, --retrain défaut 150 l.71.
- run_encoding.py : retrain masqué epochs=retrain, lr=0.02 l.88, --retrain défaut 150 l.121.
- run_sparsity.py : via build_and_train, --epochs défaut 400 l.35.

3) INFÉRENCE/MESURE SEULEMENT (pas d'apprentissage) : run_8bit_perfection.py, run_cpu.py (AER CPU), run_harness.py (perplexité WikiText-2), run_list_mode.py, run_real_clusters.py (k-means + spécialisation sur GGUF), run_value_encoding.py ; src/bpe_np.py, src/encoding.py, src/gguf_min.py, src/roofline.py, src/sparsity.py, src/ternary.py, src/transformer_np.py (forward seul) ; colab/Drave-reparti.ipynb (pilote réparti Colab : perplexité/écart, aucun .fit/train) ; drave-core/ (Rust) : AUCUN backward/gradient/optimiseur — « optimisation » = perf (main.rs l.1, engine.rs l.1) et loss_log.bin = mesure de perte en inférence (main.rs l.5417) ; bench/*.c = benchs SSE/AVX ; sprints/ = 31 .md, docs/reports/journal = .md/.txt, aucun .py ; data/, models/ = données + 2 GGUF d'inférence.

4) FICHIERS DE POIDS (tous existent) :
- /home/stephane/Data13TB/stephane/pont_semantique.npz : 1 382 064 o, 2026-10-05 10:45, md5 325a5583dd8b03535b0de2c2c9e85162.
- /home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique.npz : 1 382 064 o, 2026-10-05 10:47, MÊME md5 → copie.
- /home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz : 16 560 o, 2026-10-05 11:02.
- Écrit par tools/pont_recurrent.py l.192 np.savez(chemin, P, moy, W0, couche, rang, ...), chemin = env DRAVE_PONT_SORTIE sinon "pont_semantique.npz" relatif au cwd (LU l.191) ; ajustement moindres carrés crête forme fermée, « pas de rétropropagation, pas de gradient » (docstring LU l.15-16, l.95-100). Contenu : P 896×rang, W0 896×rang, moy 896 (rapport-pont-semantique.md l.155-160).
- r1 : --rang 1 (défaut 64, LU l.87) ; SUPPOSÉ, aucun script dédié — grep « pont_semantique_r1 » ne trouve que des docs (reports/rapport-pont-semantique.md l.161, REPRISE.md l.184, journal/.../rapport.md l.6166).
- Lu par tools/applique_pont.py l.58 (np.load(sys.argv[1])). AUCUN script hors tools/ ne lit ni n'écrit ces .npz.
- Producer/consumer = tools/ donc HORS périmètre de la question « entraînement hors tools », mais c'est bien un ajustement par ridge/lstsq.

5) *.npz/.npy/.pt/.pth/.pkl/.safetensors/.bin dans /home/stephane/Data13TB/stephane/ (maxdepth 4) : 19 fichiers, aucun .npy/.pt/.pth/.safetensors hors les 3 pont_semantique*. Notables : GitHub/trombinoscope/face-references/model.pkl 1 417 902 o 2026-03-09 ; GitHub/llama.cpp/build/dump_state.bin 686 057 o 2026-08-12 ; equipment-hauru/.face-encodings-*.pkl ; le reste .bin applicatifs/système (Downloads, .cache, firmware storey-peak 33 Mo).

6) /tmp/drave* : 11 573 entrées, 557 Mo au total. Familles : 11 563 .bin d'activations/états produits par drave-core (dump profiling, PAS des poids) — paires prof/fin : attn_brut 1290×2, comp 904×2, q/kv/qr 860×2 chacune, l/hc 430×2, idx 147×2 — plus drave_config_json.gguf (420 o, 7 oct 20:38), drave.bundle (4 878 204 o, 30 sep 13:00), drave-fige..fige6 (~1,88 Mo, 1 oct 11:39-11:49), drave_avant_iq1m (2 280 616 o, 2 oct 23:55), drave_avec_vb_jeté (2 121 280 o, 2 oct 10:45), drave_v4_logits. 3 exemples : /tmp/drave_prof-attn_brut-0-0.bin 131 072 o 2 oct 15:28 ; /tmp/drave_fin-attn_brut-0-0.bin 131 072 o 2 oct 15:23 ; /tmp/drave-fige 1 881 632 o 1 oct 11:39.

CONCLUSION : hors tools/, le seul apprentissage réel = le MLP synthétique 32→64→10 de src/tiny_model.py, via 5 run_*.py racine, sans aucune persistance de poids. Tout le reste (src/, racine, colab/, drave-core/, bench/, sprints/, docs/, reports/, data/, models/) est inférence, benchmark, k-means/statistique ou documentation. Aucun torch/Adam/backward/lbfgs dans le dépôt hors tools/.

### 🤖 Assistant

⏵ Vérification du k-means « réel » (run_real_clusters) et de sa persistance

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== run_real_clusters.py : kmeans ? ===\"; grep -n \"kmeans\\|KMeans\\|centroide\\|centroid\\|iter\\|converge\\|save\\|np\\.save\\|write\\|\\.bin\" run_real_clusters.py | head -20; echo; echo \"=== run_clusters.py : formation  … [332 caractères tronqués]`

  ```
=== run_real_clusters.py : kmeans ? ===
39:def kmeans(X: np.ndarray, k: int, iters: int = 30, seed: int = 0) -> np.ndarray:
49:    for _ in range(iters):
141:        lab = kmeans(F, G, seed=0)
142:        sizes = np.bincount(lab, minlength=G)
172:    lab = kmeans(F, G, seed=0)
239:    args.out.write_text("\n".join(x for x in L if x != ""), encoding="utf-8")

=== run_clusters.py : formation des grappes ===
3:Drave — grappes afférentes/efférentes : imposer la structure à la conversion.
5:Question : peut-on optimiser le modèle *à la conversion* pour créer des grappes
10:  1. **trafic inter-cartes** : les arêtes hors grappe doivent traverser le ring ;
11:  2. **coût d'encodage** : dans une grappe, les destinations sont confinées à une
16:l'entraînement, pas appliquée après coup), pour un taux d'arêtes inter-grappes
19:Usage :  python3 run_clusters.py [--epochs 400] [--groups 4]
41:def group_ids(n: int, groups: int) -> np.ndarray:
42:    """Affectation contiguë des indices aux grappes (comme un découpage par blocs)."""
46:def cluster_mask(d_in: int, d_out: int, groups: int, cross: float,
48:    """Masque afférent/efférent : arêtes autorisées dans la grappe, plus une
49:    fraction `cro
… [1437 caractères tronqués]
  ```

### 👤 Utilisateur

Background subagent 67637ea9-78c6-4c20-a77c-0f90ee2a9ddc finished and will do no further work unless you send it more.
Its closing message:
⏵ Résultat livré ; synthèse finale

**MISSION lecture seule respectée** : aucun script exécuté, seuls `ls/find/du/file/grep/sed/md5sum`.

**1) Seul apprentissage réel hors tools/ — `src/tiny_model.py`** (115 l., numpy pur)
- MLP 32→64→10 (LU l.22, 55), ReLU+softmax ; corpus **synthétique** : gaussiens 32 dims étiquetés en 10 classes par un professeur MLP **figé** (teacher_seed=1234, LU l.30-40).
- Loss = cross-entropy softmax, gradients à la main (LU l.97-104, 110) — **pas de torch/backward**.
- Optimiseur = SGD manuel `p -= lr*g` (LU l.105-106) ; défauts **epochs=300, lr=0.05, batch=128** (LU l.81) ; masques = « prune → retrain à masque fixe » (LU l.83-84, 107-109).
- **Aucun poids écrit** (grep np.save/savez/torch.save/state_dict/.npz/.pt hors tools = 0).

**2) Scripts racine qui l'appellent** (sortie = .md, jamais de poids) : `run_quantify.py` (l.40-47, 300 ép.), `run_clusters.py` (l.95, 140 ; 400 ép.), `run_precision.py` (l.105, retrain 150, lr 0.02), `run_encoding.py` (l.88, retrain 150), `run_sparsity.py` (build_and_train, 400 ép.).

**3) Inférence/mesure seulement** : run_8bit_perfection, run_cpu, run_harness, run_list_mode, run_real_clusters, run_value_encoding ; src/{bpe_np,encoding,gguf_min,roofline,sparsity,ternary,transformer_np}.py ; colab/Drave-reparti.ipynb (pilote réparti) ; drave-core/ (Rust : aucun backward/gradient/optimiseur, « optimisation » = perf, loss_log.bin = mesure) ; bench/*.c, sprints/ (31 .md), docs/reports/journal/data/models.

**4) Poids** : `…/stephane/pont_semantique.npz` 1 382 064 o 05-10 10:45 et `corpus/udhr/pont_semantique.npz` 1 382 064 o 05-10 10:47 (md5 **identiques**) ; `corpus/udhr/pont_semantique_r1.npz` 16 560 o 05-10 11:02. Écrits par `tools/pont_recurrent.py` l.192 (env `DRAVE_PONT_SORTIE`, ridge forme fermée), lus par `tools/applique_pont.py` l.58 ; r1 = `--rang 1` (**SUPPOSÉ**, seulement cité dans docs).

**5) /home/stephane/Data13TB/stephane/ maxdepth 4** : 19 fichiers, hors pont_semantique* rien de ML (model.pkl trombinoscope, dump_state.bin llama.cpp, .pkl equipment-hauru, .bin système).

**6) /tmp/drave*** : **11 573** entrées, **557 Mo** ; 11 563 .bin d'activations prof/fin (attn_brut 1290×2, comp 904×2, q/kv/qr 860×2, l/hc 430×2, idx 147×2) = dumps drave-core, pas des poids ; ex. `/tmp/drave_prof-attn_brut-0-0.bin` 131 072 o 02-10 15:28, `/tmp/drave_fin-attn_brut-0-0.bin` idem 15:23, `/tmp/drave-fige` 1 881 632 o 01-10 11:39 ; + drave.bundle 4,88 Mo, drave-fige2..6, drave_avant_iq1m, drave_avec_vb_jeté, drave_v4_logits, config .gguf 420 o.

**Conclusion** : hors tools/, l'unique apprentissage est le MLP synthétique de `src/tiny_model.py` (5 run_*.py), sans persistance de poids ; tout le reste est inférence/benchmark/documentation.

### 🤖 Assistant

⏵ Lecture directe de renforcement.py et renforcement_directions.py en attendant le dernier sous-agent

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && echo \"##### renforcement.py #####\"; sed -n '1,40p' renforcement.py; echo \"--- fit/solve ---\"; grep -n \"solve\\|ridge\\|ride\\|for \\|while \\|epoch\\|etape\\|renforce\\|save\" renforcement.py | head -20", "description": "R … [21 caractères tronqués]`

  ```
##### renforcement.py #####
#!/usr/bin/env python3
"""renforcement.py — le mécanisme du mandat peut-il produire la transformation ?

LA QUESTION OUVERTE, APRÈS LES §57-§71. Le professeur crée, entre sa couche 0 et sa
couche 8, une séparation contenu/langue d'un facteur **10,912** — que sa propre couche 0
n'a pas (**1,698** au mieux). Un réservoir à poids **aléatoires gelés** ne la produit
pas : mesuré, il l'**abaisse** à 1,354 (§70).

LA CONTRAINTE DU PROJET est explicite : *« A et B aléatoires et gelés, seule la lecture
s'ajuste en forme fermée »* — **mais** elle sanctionne aussi, mot pour mot :
*« L'ajout d'une couche suppose donc une relecture du corpus pour réajuster les poids
par renforcement/atrophie (pas de backprop). »*

**Le renforcement/atrophie est donc le seul mécanisme d'ajustement autorisé** — et il
n'a JAMAIS été testé sur l'axe contenu/langue. C'est ce que fait ce script.

LE MÉCANISME, tel qu'il est implémenté dans `Pont.renforce` :
  1. on ajuste la lecture, puis on calcule le **résidu** `R = Y − (φ(X)·W + mt)` ;
  2. pour chaque neurone, on mesure sa **capture** du résidu —
     `cap = |corrélation entre sa trace et le résidu|`, normalisée dans [0, 1] ;
  3. on m
… [2217 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && echo \"##### renforcement_directions.py #####\"; sed -n '1,45p' renforcement_directions.py; echo \"--- fit/solve/itérations ---\"; grep -n \"solve\\|lstsq\\|ridge\\|ride\\|for \\|while \\|norm\\|direction\\|save\" renforcement_ … [76 caractères tronqués]`

  ```
##### renforcement_directions.py #####
#!/usr/bin/env python3
"""renforcement_directions.py — la réserve du §72 : apprendre QUOI LIRE.

LA SEULE RÉSERVE QUI RESTAIT. Le §72 a testé **la forme de renforcement implémentée
dans le dépôt** — mettre à l'échelle les poids d'un neurone selon sa capture du résidu —
et elle échoue : +1,7 % du chemin nécessaire, plateau dès la deuxième passe. La raison
était nette : la capture moyenne vaut ≈ 0,5, **aucun neurone ne capte le résidu mieux
que le hasard**, donc aucun n'est franchement renforcé.

**Mais mettre à l'échelle ne change PAS ce qu'un neurone lit** — seulement l'amplitude
de ce qu'il lit déjà. Or si aucun neurone ne capte le résidu, c'est peut-être qu'aucun
ne lit la bonne direction de l'entrée.

LA FORME DIFFÉRENTE, testée ici. On apprend à chaque neurone **la direction de l'entrée
qui prédit le résidu**, par corrélation seule :

    G = Eᵀ·R          (H × canaux) — covariance croisée entrée / résidu
    SVD(G) = U·S·Vᵀ   — les colonnes de U sont les directions de l'entrée
                        les plus prédictives du résidu
    B_j ← U[:, j]     — chaque neurone reçoit SA direction

**Aucune rétropropagation** : `G` est une corréla
… [2604 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extraction compacte des 11 scripts « directions/discriminants » en parallèle du sous-agent

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools && for f in discriminant_transfert.py discriminant_contenu.py stabilite_directions.py energie_du_contenu.py transfert_ridge.py blanchiment_entree.py sous_espace_du_contenu.py covariance_cible.py decomposition.py amplification.py c … [346 caractères tronqués]`

  ```
######## discriminant_transfert.py ########
"""discriminant_transfert.py — les directions apprises sur un panel servent-elles sur un autre ?  LA QUESTION, ET ELLE EST NEUVE. Le §80 a mesuré qu'un discriminant linéaire appris portait le rapport contenu/langue à **105 % du professeur**. Mais ce résultat a été obtenu SUR LE PANEL ROMAN (es/it/pt) et mesuré SUR CE MÊME PANEL. Or le §83 vient d'établir que le professeur lui-même vaut 12,001 sur ce panel et **1,494 sur sa pire paire (de–en)**.  

  [fit]
30:                                  [--neur 120] [--rangs 0,2,5,10,20,40] [--paires]
51:        par_l.setdefault(L, []).append(i)
52:        par_c.setdefault(k, []).append(i)
101:    return np.vstack([(P.phi(P._norm(X[k])) @ W + mt).mean(0) for k in range(len(E))])
110:    n_neur = int(opt("--neur", 120))
159:        pl.setdefault(L, []).append(i)
160:        pc.setdefault(k, []).append(i)
172:    w, V = np.linalg.eigh(np.linalg.solve(Cl + lam*np.eye(ncan), Cc))

######## discriminant_contenu.py ########
"""discriminant_contenu.py — maximiser le rapport contenu/langue par les DIRECTIONS.  CE QUI MÈNE ICI, en trois étapes établies :   §67 — le rapport `P_cont/P_lang` est INVARIANT D'ÉCHE
… [9270 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des caches .npz sur disque et statut du dernier sous-agent

- **bash** `{"command": "echo \"=== .npz/.npy dans /tmp et /home (récents, hors dépôt) ===\"; find /tmp /home/stephane -maxdepth 4 -name '*.npz' -o -maxdepth 4 -name '*.npy' 2>/dev/null | grep -v '/\\.git/' | head -30; echo \"(fin)\"; echo; echo \"=== caches cités dans les rapports ===\"; grep -rho \"cache_[a-z … [207 caractères tronqués]`

  ```
=== .npz/.npy dans /tmp et /home (récents, hors dépôt) ===
/tmp/pcs_a2.derniere.npz
/tmp/pcs_a1.derniere.npz
/tmp/pcs_a2.moyenne.npz
/tmp/pcs_a1.moyenne.npz
/tmp/cache_6l_test.npz
/tmp/cache_6l_train.npz
/tmp/cache_6l.npz
/tmp/cache_vf_test.npz
/tmp/cache_vf_train.npz
/tmp/cache_wikitest.npz
/tmp/cache_wikitrain.npz
/tmp/cache_wiki_pt.npz
/tmp/cache_wiki_it.npz
/tmp/cache_wiki_es.npz
/tmp/cache_wiki_de.npz
/tmp/cache392c8_test.npz
/tmp/cache392c8_train.npz
/tmp/cache_unites8_test.npz
/tmp/cache_unites8_train.npz
/tmp/cache_unites_test.npz
/tmp/cache_unites_train.npz
/tmp/cache_wiki_fr.npz
/tmp/cache_wiki_en.npz
/tmp/cache_rj8_fr.npz
/tmp/cache_rj8_en.npz
/tmp/cache_rj_fr.npz
/tmp/cache_rj_en.npz
/tmp/cache392_test.npz
/tmp/cache392_train.npz
/tmp/cache_str_test.npz
(fin)

=== caches cités dans les rapports ===
      3 cache_vf_test.npz
      1 /home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz
      1 cache_vf_train.npz
  ```

- **list_agents** `{}`

  ```
f3ca67c4-b171-4eee-9e14-29f9dd1c8c23 [ready] — Analyser scripts directions/discriminants
67637ea9-78c6-4c20-a77c-0f90ee2a9ddc [ready] — Chercher entraînements hors tools
  ```

### 👤 Utilisateur

Agent f3ca67c4-b171-4eee-9e14-29f9dd1c8c23 sent a message:
MISSION LECTURE SEULE — 13 scripts Qtrinet/tools. Aucun script exécuté ; seuls read/grep/glob/ls/wc/od/unzip (lecture). Notations : L=n° de ligne ; « LU » = lu dans le code ; « SUP » = supposé/inféré.

BASE COMMUNE (12 des 13 scripts importent tools/pont_generatif.py) — LU : `P.nait(n_neur, True)` crée UNE couche de 120 neurones (défaut --neur 120 ; transfert_ridge : 40) ; `P.quadratique=True` ⇒ phi(X)=[X,X²] ⇒ readout 240 colonnes (pont_generatif L223-228) ; `a_min,a_max=0.02,0.8` ⇒ 120 constantes de temps log-étalées (L165) ; réservoir = tanh + fuite s=(1-a)s+a·tanh(drive+E·Bᵀ), B=randn(120,H)/√H, W_self=randn(120,120)/√120, GELÉS (L157-160,197-199) ; lecture seule ajustée en forme fermée : W=solve(XᵀX+ride·n·I, Xᵀ(Y-mt)) (L302). Canaux : E et Y = (positions,896) float32, hidden=896 (LU : cache_pont.py L8/56 + en-tête npy des caches réels) ; `garde` = canaux dont (y≠0)≥5 % des positions dans ≥50 % des entrées (part=0.5, ex. discriminant_contenu L98-104). Dimensions : W=(240, ncan) ; si ncan=896 ⇒ 215 040 coefficients ; poids aléatoires gelés = B 120×896=107 520 + W_self 14 400 + 120 constantes a. RÉSERVE LU : ces scripts passent `len(garde)` comme H à Pont (ex. discriminant_contenu L113, energie L77) alors que E[i] fait 896 colonnes ⇒ ne tourne que si garde=896 (les rapports affichent « 896 canaux » 28×) ; « H » renvoyé par charge() est ignoré ou non utilisé pour Pont.

1. /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/discriminant_transfert.py — apprentissage : (a) ridge forme fermée du readout W=P.ajuste(idx,0.03,mt,itr) L150 ; (b) LDA/vecteurs propres généralisés `eigh(solve(Cl+λI, Cc))` L172, λ=1e-2·trace(Cl)/ncan L171. Entrée : moyennes par entrée des sorties du pont (240→ncan) ; sortie : projection sur r directions, r∈{0,2,5,10,20,40} L111 ; cible = ratio P_cont/P_lang (Fisher). Optimiseur : 2 formes fermées, aucune itération ; graine 5, ride 0,03, quadratique. Écriture disque : AUCUNE.
2. tools/discriminant_contenu.py — idem : ridge ride=0,03, graine=5, part=0,5 L92 ; LDA L135-139 avec plancher λ=--plancher(1e-2)·trace(Cl)/ncan L132 ; rang/alphas L93-94 ; amplifications vers P_cont 1000 et 4356,4 L169. Aucune écriture.
3. tools/stabilite_directions.py — boucle de 6 apprentissages complets (graines 5..10 L74) : pour chaque graine Pont neuf + ridge 0,03 + LDA ; mesure d'angles principaux par SVD de V_iᵀV_j L67. Aucune écriture.
4. tools/renforcement_directions.py — VRAI apprentissage des poids d'entrée (pas seulement de la lecture) : G=Eᵀ(R-R̄) (H×canaux) L144, SVD(G) L145, puis b_j ← (1-mélange)·b_j + mélange·U[:,j%k]·‖b_j‖ L150 ; passes=5 L74, mélange=1,0 L75 ; ridge 0,03 réajusté à chaque passe L153 ; LDA final L190-193. Sans rétropropagation (règle de Hebb locale). Aucune écriture.
5. tools/renforcement.py — apprentissage par renforcement/atrophie locale : cap_j=|corr(act_j, résidu)| L144, f=1+η(2cap−1) L146, poids de j multipliés par f L148 ; η∈{0,02,0,1} L77, passes=8 L76 ; ridge 0,03 réajusté chaque passe L129/157. N'utilise PAS Pont.renforce (pont_generatif L524, η=0,6) : réimplémentation par lot. Aucune écriture.
6. tools/energie_du_contenu.py — 4 variantes convexes forme fermée : A référence, B cible centrée, C lignes normées, D blanchiment α de la cible ; toutes par `np.linalg.solve(G+ride·n·I, D)` L109 ; ACP de la cible par eigh L93 ; ride=0,03 L61, alphas=0,25/0,5/0,75/1,0 L62 (α=0⇒T=I L153). Aucune écriture.
7. tools/transfert_ridge.py — apprentissage : ridge seule, balayage rides=0,03/0,1/0,3/1/3/10/30 L44, --neur 40 L41 ; Gram calculée une fois L86-95 ; oracle ajusté par panneau L105-106 ; validation itr[::7] L60. Aucune écriture.
8. tools/blanchiment_entree.py — apprentissage : blanchiment par langue T[L]=(V·w^(−α/2))Vᵀ depuis eigh de la covariance de l'entrée L98-100, plancher 1e-3·trace(C)/d L69/99 ; puis AUCUN neurone : readout linéaire-quadratique direct [E,E²]=1792 colonnes, solve ridge 0,03 L115/124. alphas=0/0,25/0,5/1 L68. Aucune écriture.
9. tools/sous_espace_du_contenu.py — apprentissage une fois : offsets de contenu E=(contenus×canaux) L116, SVD L117, projecteur Π=Vᵀ_rV_r L120 (896×896) ; ridge 0,03 L99 ; gammas=1/1,5/2/3/5 L74. Aucune écriture.
10. tools/covariance_cible.py — apprentissage : A=CY^(1/2)·CO^(−1/2) par eigh, plancher 1e-3·trace(CO)/ncan L118-119 ; mélanges 0/0,25/0,5/0,75/1 L79 ; ridge 0,03 L104. Aucune écriture.
11. tools/decomposition.py — MESURE PURE (ANOVA P_lang/P_cont/P_res L40-62) ; le seul ajustement est le readout ridge 0,03 L104 ; balayages β (0..30) L154 et γ (0..5) L187 = diagnostics non appris ; option --mu-lang pose P.mu_inv (terme quadratique d'invariance, pont_generatif L269-278). Aucune écriture.
12. tools/amplification.py — MESURE PURE : α=0,5..3 L84/142 appliqué à une sortie fixe ; readout ridge 0,03 L112 ; aucun paramètre appris. Aucune écriture.
13. tools/calibre_modes.py — AUCUN apprentissage, aucun fit numpy : appelle 2× par langue le binaire ./drave-core/target/release/drave (--trace-flux, événementiel puis --dense) L85-92, relit le DRVF L37-81, calcule cosinus/normes L126-137. Défauts : langues eng,fra,deu,spa,rus,ell,jpn,tha L98, modèle models/Qwen2.5-0.5B-Q8_0.gguf, ctx 256, couches 0:24. ÉCRITURE : os.makedirs(tmp) L101 + 2 fichiers traces <tmp>/<L>.ev.drvf et <L>.de.drvf par langue.

ARTEFACTS : (a) aucun des 13 scripts ne contient np.save/np.savez/savez_compressed/open(...,'wb')/pickle — grep exhaustif = 0 occurrence ⇒ AUCUN fichier de poids n'est écrit ; W, P.poids, Π, A, T[L], V restent en RAM. (b) Seule écriture disque réelle : calibre_modes.py via le binaire (ci-dessus). (c) EXISTE sur disque : /tmp/calibre/ = 16 .drvf (8 langues × {ev,de}, 1,9–10,6 Mo), datés 7 oct 18:18-18:22 = artefacts de calibre_modes.py. (d) Entrées des 12 autres (écrites par tools/cache_pont.py L79, PAS par ces scripts) : /tmp/cache_wiki_{de,en,es,fr,it,pt}.npz (couche 8, E0/Y0 (N,896) f32, hidden=896 vérifié) ; /tmp/cache_6l{,_train,_test}.npz ; /tmp/cache392{,_train,_test}.npz ; /tmp/cache_wikitrain/test.npz ; /tmp/cache_unites*.npz ; /tmp/cache_appr10/10c/40.npz. (e) Aucun .npz/.npy dans le dépôt Qtrinet (find). (f) /home/stephane/Data13TB/stephane/pont_semantique.npz, pont_semantique_r1.npz et corpus/udhr/pont_semantique.npz existent mais sont écrits par tools/pont_recurrent.py (L191-193, np.savez) — hors périmètre. Conclusion : la chaîne de ces 13 outils n'a AUCUNE persistance de poids ; tout modèle appris est éphémère et reconstruit à chaque exécution depuis les caches .npz.

### 👤 Utilisateur

Background subagent f3ca67c4-b171-4eee-9e14-29f9dd1c8c23 finished and will do no further work unless you send it more.
Its closing message:
⏵ Résultat transmis au parent ; synthèse finale

**Méthode** : lecture intégrale des 13 fichiers + `pont_generatif.py` (Pont/nait/phi/ajuste) + `cache_pont.py` ; en-têtes npy des caches réels lus via `unzip/od` ; aucun script exécuté, aucune écriture. Notation : L=n° de ligne, « LU » = lu dans le code, « SUP » = supposé.

**BASE COMMUNE (LU, 12/13 scripts importent tools/pont_generatif.py)** — `P.nait(n_neur,True)` = UNE couche de 120 neurones (défaut `--neur 120` ; transfert_ridge : 40) ; `P.quadratique=True` ⇒ φ(X)=[X,X²] ⇒ readout 240 colonnes (L223-228) ; `a_min,a_max=0.02,0.8` ⇒ 120 constantes de temps log-étalées (L165) ; réservoir tanh+fuite s=(1−a)s+a·tanh(drive+E·Bᵀ), B=randn(120,H)/√H, W_self=randn(120,120)/√120, **gelés** (L157-160,197-199) ; seule la lecture s'ajuste : `W=solve(XᵀX+ride·n·I, Xᵀ(Y−mt))` (L302). Canaux : E et Y = (positions,**896**) float32, hidden=896 (cache_pont.py L8/56 + en-tête npy vérifié) ; `garde` = canaux dont (y≠0)≥5 % des positions dans ≥50 % des entrées (part=0,5). Dim. : W=(240,ncan) ; ncan=896 ⇒ 215 040 coeffs ; aléatoires gelés = 107 520 (B) + 14 400 (W_self) + 120 constantes a. **RÉSERVE LU** : les scripts passent `len(garde)` comme H à Pont (ex. discriminant_contenu L113, energie L77) alors que E[i] fait 896 colonnes ⇒ ne tourne que si garde=896 (les rapports affichent « 896 canaux » 28×) ; le H renvoyé par `charge()` n'est pas utilisé pour Pont.

1. `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/discriminant_transfert.py` — ridge forme fermée L150 (ride 0,03) + **LDA** `eigh(solve(Cl+λI,Cc))` L172, λ=1e-2·trace(Cl)/ncan L171 ; entrée = moyennes par entrée des sorties du pont (ncan dim) ; rangs 0,2,5,10,20,40 L111 ; ratio P_cont/P_lang (Fisher) ; graine 5 ; aucune écriture.
2. `tools/discriminant_contenu.py` — ridge ride=0,03/graine=5/part=0,5 L91-92 ; LDA L135-139, plancher 1e-2·trace(Cl)/ncan L132 ; cibles d'amplification 1000 et 4356,4 L169 ; aucune écriture.
3. `tools/stabilite_directions.py` — 6 apprentissages complets (graines 5..10 L74), ridge 0,03 + LDA par graine ; mesure = angles principaux par SVD de V_iᵀV_j L67 ; aucune écriture.
4. `tools/renforcement_directions.py` — **apprend les poids d'entrée** : G=Eᵀ(R−R̄) L144, SVD(G) L145, b_j←(1−mélange)·b_j+mélange·U[:,j%k]·‖b_j‖ L150 ; passes=5 L74, mélange=1,0 L75 ; ridge 0,03 réajusté chaque passe L153 ; LDA final L190-193 ; Hebb local, sans rétroprop.
5. `tools/renforcement.py` — renforcement/atrophie locale : cap_j=|corr(act_j,résidu)| L144, f=1+η(2cap−1) L146, poids de j ×f L148 ; η∈{0,02;0,1} L77, passes=8 L76 ; ridge 0,03 chaque passe L129/157 ; n'utilise PAS `Pont.renforce` (pont_generatif L524, η=0,6).
6. `tools/energie_du_contenu.py` — 4 variantes forme fermée A/B/C/D (`solve(G+ride·n·I,D)` L109) ; ACP cible par eigh L93 ; ride=0,03 L61, alphas 0,25/0,5/0,75/1,0 L62.
7. `tools/transfert_ridge.py` — ridge seule, balayage rides 0,03→30 L44, `--neur 40` L41 ; Gram calculée une fois L86-95 ; oracle par panneau L105-106 ; validation itr[::7] L60.
8. `tools/blanchiment_entree.py` — blanchiment par langue T[L]=(V·w^(−α/2))Vᵀ, eigh L98-100, plancher 1e-3·trace(C)/d L69 ; **aucun neurone** : readout direct [E,E²]=1792 colonnes, solve ridge 0,03 L115/124 ; alphas 0/0,25/0,5/1 L68.
9. `tools/sous_espace_du_contenu.py` — SVD des offsets de contenu L116-117, projecteur Π=Vᵀ_rV_r (896×896) L120 appris une fois ; ridge 0,03 L99 ; gammas 1/1,5/2/3/5 L74.
10. `tools/covariance_cible.py` — A=CY^½·CO^(−½) par eigh, plancher 1e-3·trace(CO)/ncan L118-119 ; mélanges 0/0,25/0,5/0,75/1 L79 ; ridge 0,03 L104.
11. `tools/decomposition.py` — **mesure pure** (ANOVA P_lang/P_cont/P_res L40-62) ; seul ajustement = readout ridge 0,03 L104 ; β(0..30) L154 et γ(0..5) L187 = diagnostics non appris ; `--mu-lang` pose `P.mu_inv` (pont_generatif L269-278).
12. `tools/amplification.py` — **mesure pure** : α=0,5..3 L84/142 sur sortie fixe ; readout ridge 0,03 L112 ; aucun paramètre appris.
13. `tools/calibre_modes.py` — **aucun apprentissage** : 2 appels par langue au binaire `./drave-core/target/release/drave` (--trace-flux, événementiel puis --dense) L85-92, relecture DRVF L37-81, cosinus/normes L126-137 ; défauts langues 8, modèle Qwen2.5-0.5B-Q8_0.gguf, ctx 256, couches 0:24 ; **écrit** `os.makedirs(tmp)` L101 + `<tmp>/<L>.ev.drvf` et `.de.drvf`.

**ARTEFACTS** — (a) **aucun des 13 ne contient np.save/np.savez/open(...,'wb')/pickle** (grep = 0) ⇒ aucun fichier de poids ; W, P.poids, Π, A, T[L], V restent en RAM. (b) Seule écriture réelle : calibre_modes.py via le binaire. (c) **Existe sur disque** : `/tmp/calibre/` = **16 .drvf** (8 langues × {ev,de}, 1,9–10,6 Mo), 7 oct 18:18-18:22 = artefacts de calibre_modes.py. (d) Entrées des 12 autres, écrites par `cache_pont.py` L79 (pas par ces scripts) : `/tmp/cache_wiki_{de,en,es,fr,it,pt}.npz` (couche 8, E0/Y0 (N,896) f32, hidden=896 vérifié), `/tmp/cache_6l{,_train,_test}.npz`, `/tmp/cache392{,_train,_test}.npz`, `/tmp/cache_wikitrain|test.npz`, `cache_unites*.npz`, `cache_appr10/10c/40.npz`. (e) **Aucun .npz/.npy dans le dépôt**. (f) `/home/stephane/Data13TB/stephane/pont_semantique.npz`, `pont_semantique_r1.npz`, `corpus/udhr/pont_semantique.npz` existent mais sont écrits par `tools/pont_recurrent.py` (L191-193) — hors périmètre. **Conclusion : aucune persistance de poids dans cette chaîne ; tout modèle appris est éphémère et reconstruit à chaque run depuis les caches .npz.**

### 🤖 Assistant

⏵ Dernières vérifications de tailles et de GGUF synthétiques avant synthèse

- **bash** `{"command": "echo \"=== caches .npz principaux ===\"; ls -la /tmp/cache_6l_train.npz /tmp/cache_6l_test.npz /tmp/cache_vf_train.npz /tmp/cache_vf_test.npz /tmp/cache_wiki_en.npz /tmp/cache392_train.npz 2>/dev/null; echo \"=== total /tmp/cache*.npz ===\"; ls /tmp/cache*.npz 2>/dev/null | wc -l; du -s … [308 caractères tronqués]`

  ```
=== caches .npz principaux ===
-rw-r--r--. 1 stephane stephane  985580685  6 oct 02:55 /tmp/cache392_train.npz
-rw-r--r--. 1 stephane stephane  182822069  7 oct 11:49 /tmp/cache_6l_test.npz
-rw-r--r--. 1 stephane stephane  347112339  7 oct 11:48 /tmp/cache_6l_train.npz
-rw-r--r--. 1 stephane stephane 1834865780  7 oct 05:52 /tmp/cache_vf_test.npz
-rw-r--r--. 1 stephane stephane 1747348718  7 oct 05:21 /tmp/cache_vf_train.npz
-rw-r--r--. 1 stephane stephane   73802158  6 oct 18:15 /tmp/cache_wiki_en.npz
=== total /tmp/cache*.npz ===
41
9,5G	total
=== GGUF synthétiques (poids aléatoires) ===
-rw-r--r--. 1 stephane stephane   35441  2 oct 17:36 /tmp/mhc_tl2.py
-rw-r--r--. 1 stephane stephane   67579  2 oct 17:36 /tmp/mhc_tl.py
-rw-r--r--. 1 stephane stephane    9146  2 oct 17:32 /tmp/mhc_triton.py
-rw-r--r--. 1 stephane stephane    9044  2 oct 17:52 /tmp/mhc_v41_witness.txt
-rw-r--r--. 1 stephane stephane    2048  2 oct 02:58 /tmp/mla_ancien.bin
-rw-r--r--. 1 stephane stephane      15  2 oct 02:58 /tmp/mla_ids.txt
-rw-r--r--. 1 stephane stephane    2048 29 sep 20:08 /tmp/mla_logits.bin
-rw-r--r--. 1 stephane stephane  480448  2 oct 02:58 /tmp/mla_minuscule.gguf
-rw-r--r--. 1 stephane 
… [162 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Synthèse finale et envoi au parent

- **send_message** `{"agent_id": "48ec07ab-ec9d-4297-a7bf-d84974667e61", "message": "INVENTAIRE ENTRAÎNEMENT/POIDS — Qtrinet (mission lecture seule ; aucun fichier écrit, aucun script exécuté). Tout est MESURÉ (code lu + ls/unzip/md5) sauf mention « supposé ».\n\n== A. LE SEUL POIDS ENTRAÎNÉ ET PERSISTÉ DU PROJET ==\n· … [7508 caractères tronqués]`

  ```
message delivered to agent 48ec07ab-ec9d-4297-a7bf-d84974667e61
  ```

### 🤖 Assistant

⏵ Résultat livré au parent ; synthèse finale

**MISSION LECTURE SEULE respectée** : aucun fichier écrit, aucune commande d'écriture/téléchargement, aucun script exécuté. Tout est *mesuré* (code lu, `ls`/`unzip`/`md5`), sauf mention « supposé ».

## A. Le seul poids entraîné et persisté du projet
| Chemin absolu | Taille / date | Ce que c'est |
|---|---|---|
| `/home/stephane/Data13TB/stephane/pont_semantique.npz` | 1 382 064 o · 05/10 10:45 · md5 `325a5583…` | Écrit par `tools/pont_recurrent.py` L191-193 (env `DRAVE_PONT_SORTIE`). Contenu vérifié : `P` f4 (896,128), `moy` f4 (896), `W0` f8 (896,128), `couche`, `rang`, `langues_train/test`. Lu par `tools/applique_pont.py` L58 et `tools/sonde_pont.py` L85. |
| `/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique.npz` | 1 382 064 o · 05/10 10:47 | Copie **byte-identique** (même md5). |
| `/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz` | 16 560 o · 05/10 11:02 | Rang 1 : `P` (896,1), `W0` (896,1) f8, `moy` (896). « `--rang 1` » = supposé (défaut du script : 64). |

Aucun `.pt/.pth/.safetensors/.pkl/.ckpt/.bin` de poids dans le dépôt (`find` = 0). `models/` = 2 GGUF téléchargés (Qwen2.5-0.5B Q4_0 353 Mo, Q8_0 531 Mo) → inférence seule.

## B. Pont (point 3) — ajustement de la lecture en forme fermée, sans rétropropagation
Base : entrée = plongée couche 0 (T,896) ; cible = couche 10 du professeur (896).
- `tools/pont_recurrent.py` — 2 régressions crête : récurrence `s_t=A·s_{t−1}+B·e_t` dans un sous-espace de rang r (SVD de Y, défaut 64) + témoin `W0`. Loss `‖XW−Y‖²+λ‖W‖²`, λ=1e-2·n, `np.linalg.solve`, **0 itération** ; rayon spectral de A ramené à 0,95. **ÉCRIT `pont_semantique.npz`**.
- `tools/pont_generatif.py` (moteur, 1041 l.) — réseau récurrent qui **croît puis subit une attrition**. Neurone : `s=(1−a)s+a·tanh(W_par·x_{c−1}+W_self·s+B·e_t)`, a=0,2 (ou 120 constantes log-étalées [0,02;0,8]), B/W_self **aléatoires gelés** (graine 5) ; seule W s'ajuste (`solve`, ride=0,3) ; lecture quadratique `[X,X²]` optionnelle (240 col.). Objectif `‖XW−Y‖² + μ_lang·P_lang − μ_cont·P_cont`. Défauts : 3 cycles × 3 couches, naissance 1,1,2,4… puis +n/4, plafond 256 neurones, patience 12, seuil d'attrition 0,02 (retrait de 25 % par redondance `1−1/((G⁻¹)_jj·G_jj)` ou contribution), retour au meilleur passage, `renforce()` local η=0,6. **N'écrit aucun poids.**
- `pont_reservoir.py` — réservoir N=256 gelé (rayon 0,9), fuite a=0,2, W seule (ride 3e-1). `pont_fidele.py` — linéaire rangs 1→128 et ELM `tanh(E·R)` R gelé H∈{64…4096}. `pont_unites.py` — croissance ≤120 neurones (patience 8), ride=1,0. `pont_parallele.py` — 1 couche, a=0,5, ride=1,0. `pont_reglages.py` — balayages. `leviers_pont.py` — A 40 neurones / B +entrée / C entrée seule / D 20+20, ride=0,3. `objectif_du_pont.py` — balayage (μ_lang, μ_cont). **Tous : 0 poids écrit.**
- `cache_pont.py` — pas d'apprentissage : écrit `/tmp/cache*.npz` (activations `E` couche 0, `Y` couche c). `applique_pont.py`, `compare_professeurs.py`, `ancre_professeur.py` = mesure ; `sonde_pont.py` ajuste une sonde ridge (λ=1e-2) non persistée ; `rapport_du_pont.py` réentraîne la référence éphémère (120 neurones, quadratique, ride 0,03, graine 5).

## C. Directions / discriminants (point 4)
Base commune (12/13 scripts) : `Pont` 1 couche de 120 neurones, lecture quadratique 240 col., 896 canaux, `W=solve(XᵀX+ride·n·I, Xᵀ(Y−mt))`, **ride=0,03, graine 5**, aucune écriture.
- `discriminant_contenu.py` / `discriminant_transfert.py` / `stabilite_directions.py` — LDA de Fisher `eigh(solve(C_lang+λI, C_cont))`, λ=1e-2·tr(C_lang)/ncan, rangs 2/5/10/20/40 ; stabilité = 6 ponts réentraînés (graines 5→10).
- `renforcement.py` — renforcement/atrophie local : `cap_j=|corr(act_j, résidu)|`, `f=1+η(2cap−1)`, η∈{0,02;0,1}, **passes=8**.
- `renforcement_directions.py` — apprend les **poids d'entrée** : `G=EᵀR`, `SVD(G)`, `b_j←U[:,j%k]·‖b_j‖` (Hebb local), mélange=1,0, **passes=5**.
- `energie_du_contenu.py` (4 variantes convexes, α 0,25→1) · `transfert_ridge.py` (ride 0,03→30, 40 neurones) · `blanchiment_entree.py` (blanchiment covariance par langue + readout direct `[E,E²]` 1792 col.) · `sous_espace_du_contenu.py` (SVD des offsets de contenu, projecteur Π 896×896, γ 1→5) · `covariance_cible.py` (`A=CY^½·CO^−½`) · `decomposition.py` et `amplification.py` = **mesures pures** · `calibre_modes.py` = **aucun apprentissage** (lance 2× par langue `drave-core/target/release/drave`, écrit `/tmp/calibre/*.drvf` : 16 fichiers, 58 Mo).

## D. Hors `tools/` (point 2)
- `src/tiny_model.py` — **seul apprentissage hors tools** : MLP 32→64→10 (ReLU+softmax), corpus **synthétique**, professeur = MLP aléatoire **figé** (`teacher_seed=1234`) ; loss cross-entropy, gradient manuel, SGD lr=0,05 batch=128 **epochs=300** ; masques = prune→retrain. **Aucun poids écrit.** Appelé par `run_quantify.py` (300 ép.), `run_clusters.py` (400), `run_sparsity.py` (400), `run_precision.py` (retrain 150, lr 0,02), `run_encoding.py` (retrain 150).
- `run_real_clusters.py` — k-means maison (30 itérations, seed 0) sur les experts d'un GGUF = ajustement non supervisé de centroïdes, sortie texte, pas de poids.
- `mla_synthetique.py`, `mhc_v41_synthetique.py`, `v41_*.py` — poids **aléatoires** aux bonnes formes écrits en GGUF (`/tmp/mla_minuscule.gguf`, 480 448 o, 02/10) pour tester le moteur : **pas entraînés**.
- **Aucun `torch.optim`/`Adam`/`SGD`/`loss.backward`/`lbfgs` dans le dépôt** ; `drave-core/` (Rust) = inférence.

## E. Fichiers trouvés (point 1)
Dépôt : **0**. Voisins : `/tmp/cache*.npz` = **41 fichiers, 9,5 Go** (activations E/Y, ex. `/tmp/cache_vf_train.npz` 1 747 348 718 o 07/10 05:21) ; `/tmp/drave*` = **11 573 fichiers, 557 Mo** — dumps d'activations/états (q_rope, qr_norm, attn_brut, comp, l, hc, idx), **pas des poids** ; `/tmp/calibre/` 16 `.drvf`. `/home/stephane/Data13TB/stephane/` (maxdepth 4) : hors `pont_semantique*`, rien de ML. `~/.cache/drave*` : inexistant.

## F. Professeur / distillation / calibration (point 5)
- « Professeur » = **Qwen2.5-0.5B (GGUF), jamais entraîné ici** : boîte noire couche 0 → couche 10, 896 canaux (hidden=896 cohérent, supposé).
- **Aucune distillation entraînée** : seules mentions `tools/approximabilite_bloc.py` L5 et `reports/rapport-morcellement-experts.md` (projet non réalisé).
- « Calibration » = mesure (`calibre_modes.py`, `trace_gpu.py --calibrer`), aucun paramètre appris.

**Conclusion** : tout apprentissage « modèle » est **éphémère (RAM)** sauf le pont (`pont_semantique*.npz`, ~1,4 Mo) ; quatre mécanismes non-gradient (ridge forme fermée, croissance+attrition, renforcement/atrophie local, SVD/Hebb des directions) plus le MLP synthétique SGD de `src/tiny_model.py`, qui n'écrit rien.

