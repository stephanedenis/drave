# Session DSH — relecture

- identifiant : `48ec07ab-ec9d-4297-a7bf-d84974667e61`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-08 09:18:07
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence Rust dans drave-core/, outils Python dans tools/, rapports dans reports/, sprints dans sprints/, journal des sessions dans journal/, reprise dans REPRISE.md).

MISSION : inventorier TOUT le travail « côté modèle » de ce dépôt — c'est-à-dire ce que le projet a lui-même entraîné, ajusté ou construit comme modèle/architecture, par opposition au travail « côté moteur » (exécuter des modèles existants).

CE QU'IL FAUT COUVRIR (liste à vérifier, pas exhaustive) :
- les « ponts » linguistico-sémantiques : tools/pont_recurrent.py, pont_fidele.py, pont_reservoir.py, pont_generatif.py, cache_pont.py, applique_pont.py, sonde_pont.py, compare_professeurs.py, rapport_du_pont.py, ancre_professeur.py ;
- les résultats de « plateau sémantique » et d'invariance inter-langue (tools/plateau_multilingue.py, lecture_plateau.py, invariance_*.py, cancellation_langue.py) ;
- les directions/discriminants (tools/discriminant_transfert.py, stabilite_directions.py, renforcement_directions.py, energie_du_contenu.py) ;
- tout autre modèle entraîné dans le dépôt (cherche les scripts d'entraînement, les .pt/.npz de poids, les boucles d'optimisation) ;
- les rapports correspondants : reports/rapport-pont-*.md, rapport-plateau-semantique.md, rapport-cycle-rapide.md, reports/recapitulatif.md, et les notes docs/note-un-pont-par-professeur.md, docs/note-cout-professeur.md, docs/note-regle-contrastive.md.

RENDS un rapport en français, structuré ainsi :
1. TABLEAU des dispositifs entraînés : nom, ce que c'est (architecture, taille, paramètres), corpus utilisé, coût d'entraînement, et RÉSULTAT CHIFFRÉ (fidélité d'entraînement, fidélité de TEST, invariance, pire paire, taille du réseau), avec le fichier source de chaque chiffre.
2. Ce qui a MARCHÉ : les résultats positifs reproductibles, avec leurs chiffres et leurs conditions.
3. Ce qui a ÉCHOUÉ ou a été RÉFUTÉ : les hypothèses tombées, avec les chiffres qui les ont fait tomber (par exemple le résultat négatif du pont génératif sur données propres).
4. Les CORPUS disponibles dans le dépôt et sur la machine (UDHR, Wikipedia, Gutenberg…) : où ils sont, leur taille, et les outils qui les produisent (tools/extrait_article1.py, tools/ingestion*.py, etc.).
5. CE QUI MANQUE : ce que le dépôt n'a jamais entraîné ni essayé.

CONTRAINTES : ne modifie AUCUN fichier, ne lance aucun entraînement. Distingue « mesuré », « déduit », « supposé ». Rapport final : 150 lignes maximum, dense en chiffres et en chemins de fichiers.
Your parent agent id is "d31b3d9b-58e4-4d34-85fa-381b6f6a6a76". Before you finish, send your result to that agent with send_message({ agent_id: "d31b3d9b-58e4-4d34-85fa-381b6f6a6a76", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Inventaire du travail « côté modèle » : exploration du dépôt Qtrinet.

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet", "description": "List repo root"}`

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
… [708 caractères tronqués]
  ```

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs 2>&1 | head -200", "description": "List tools, reports, docs"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs:
total 644
drwxr-xr-x. 1 stephane stephane   1130  5 oct 13:47 .
drwxr-xr-x. 1 stephane stephane    612  7 oct 18:16 ..
-rw-------. 1 stephane stephane  19350  3 oct 18:05 architecture-kimi-k3.md
-rw-r--r--. 1 stephane stephane   7041  2 oct 10:05 colab-reparti.md
-rw-------. 1 stephane stephane   9537  2 oct 10:21 comparaison-spiking.md
-rw-------. 1 stephane stephane  33243  2 oct 15:32 contexte-long.md
-rw-------. 1 stephane stephane  17286  2 oct 10:21 convertisseur.md
-rw-------. 1 stephane stephane   9593  2 oct 10:21 format-clusters.md
-rw-r--r--. 1 stephane stephane  12731  3 oct 01:20 format-flux.md
-rw-------. 1 stephane stephane 142853  6 oct 23:51 glossaire.md
-rw-------. 1 stephane stephane   4360 30 sep 13:08 histoire.md
-rw-r--r--. 1 stephane stephane  15275  5 oct 10:15 note-cancellation-evenementielle.md
-rw-r--r--. 1 stephane stephane   3928  5 oct 08:52 note-corpus-panini.md
-rw-r--r--. 1 stephane stephane   5247  5 oct 11:47 note-cout-professeur.md
-rw-r--r--. 1 stephane stephane   4532  5 oct 09:08 note-ingestion-corpus.md
-rw-r--r--. 1 stephane stephane   7730  5 oct 10:19 note-regle-contrastive.md
-rw-r--r-
… [13284 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des répertoires tools/data/models/colab et des scripts du pont.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la tools | tail -40; echo \"=== DATA ===\"; ls -laR data | head -80; echo \"=== MODELS ===\"; ls -laR models | head -60; echo \"=== COLAB ===\"; ls -laR colab | head -60", "description": "List remaining tools and data dirs"}`

  ```
-rw-r--r--. 1 stephane stephane   1900 30 sep 11:37 proxy_latence.py
drwxr-xr-x. 1 stephane stephane   1414  7 oct 21:10 __pycache__
-rw-------. 1 stephane stephane   5538  7 oct 10:56 rapport_du_pont.py
-rw-------. 1 stephane stephane   4531  1 oct 23:26 ref_ggml_bloc.c
-rwxr-xr-x. 1 stephane stephane 207032  4 oct 00:42 ref_logits
-rw-------. 1 stephane stephane  16486  4 oct 00:42 ref_logits.cpp
-rwxr-xr-x. 1 stephane stephane 207032  4 oct 00:42 ref_logits_k3
-rw-------. 1 stephane stephane   4629  3 oct 15:58 ref_logits.md
-rw-------. 1 stephane stephane  11887  7 oct 02:34 renforcement_directions.py
-rw-------. 1 stephane stephane   7683  7 oct 00:15 renforcement.py
-rw-r--r--. 1 stephane stephane   2062  2 oct 19:55 rope_yarn_temoin.py
-rw-------. 1 stephane stephane   4283  6 oct 12:08 saturation.py
-rwx--x--x. 1 stephane stephane  14316 27 sep 11:40 session_report.py
-rwxr-xr-x. 1 stephane stephane   8674  7 oct 16:54 sonde-passe-k3.sh
-rwxr-xr-x. 1 stephane stephane   4449  5 oct 10:48 sonde_pont.py
-rw-r--r--. 1 stephane stephane   3992  5 oct 17:26 sous_ensemble_actif.py
-rw-------. 1 stephane stephane   7091  6 oct 22:04 sous_espace_du_contenu.py
-rwxr-xr-x. 1 stephane
… [2547 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in tools/pont_recurrent.py tools/pont_fidele.py tools/pont_reservoir.py tools/pont_generatif.py tools/cache_pont.py; do echo \"##### $f\"; wc -l \"$f\" 2>&1; done; echo; ls -la tools | grep -i pont", "description": "Check pont  … [19 caractères tronqués]`

  ```
##### tools/pont_recurrent.py
211 tools/pont_recurrent.py
##### tools/pont_fidele.py
135 tools/pont_fidele.py
##### tools/pont_reservoir.py
137 tools/pont_reservoir.py
##### tools/pont_generatif.py
1041 tools/pont_generatif.py
##### tools/cache_pont.py
86 tools/cache_pont.py

-rwxr-xr-x. 1 stephane stephane   2995  5 oct 10:44 applique_pont.py
-rw-r--r--. 1 stephane stephane   3437  5 oct 22:15 cache_pont.py
-rw-------. 1 stephane stephane   6758  6 oct 08:21 leviers_pont.py
-rw-------. 1 stephane stephane   5635  6 oct 22:04 objectif_du_pont.py
-rwxr-xr-x. 1 stephane stephane   5586  5 oct 11:11 pont_fidele.py
-rw-r--r--. 1 stephane stephane  55157  6 oct 19:46 pont_generatif.py
-rw-r--r--. 1 stephane stephane   7024  6 oct 09:18 pont_parallele.py
-rwxr-xr-x. 1 stephane stephane   9574  5 oct 10:47 pont_recurrent.py
-rw-r--r--. 1 stephane stephane   5890  5 oct 12:44 pont_reglages.py
-rwxr-xr-x. 1 stephane stephane   5779  5 oct 12:45 pont_reservoir.py
-rw-r--r--. 1 stephane stephane   5348  6 oct 18:52 pont_unites.py
-rw-------. 1 stephane stephane   5538  7 oct 10:56 rapport_du_pont.py
-rwxr-xr-x. 1 stephane stephane   4449  5 oct 10:48 sonde_pont.py
  ```

### 🤖 Assistant

⏵ Je lance deux explorations parallèles (corpus, scripts d'entraînement) et je lis les rapports clés.

- **subagent** `{"description": "Inventaire corpus dépôt", "prompt": "Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave, moteur d'inférence Rust + outils Python). MISSION STRICTEMENT EN LECTURE : n'écris, ne modifie et ne lance AUCUN fichier/entraînement. Tu peux seulement li … [1660 caractères tronqués]`
- **subagent** `{"description": "Inventaire poids et entraînements", "prompt": "Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave : moteur d'inférence Rust dans drave-core/, outils Python dans tools/, rapports dans reports/). MISSION STRICTEMENT EN LECTURE : n'écris, ne modif … [2533 caractères tronqués]`

  ```
started subagent a4277668-3825-4797-bf0b-d7addcbb569d
  ```


  ```
started subagent ee19a880-cc76-4c5c-9fe0-5972bd73b533
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l reports/rapport-pont-generatif.md reports/rapport-pont-semantique.md reports/rapport-plateau-semantique.md reports/rapport-cycle-rapide.md reports/recapitulatif.md docs/note-un-pont-par-professeur.md docs/note-cout-professeur.m … [180 caractères tronqués]`

  ```
456 reports/rapport-pont-generatif.md
   355 reports/rapport-pont-semantique.md
   137 reports/rapport-plateau-semantique.md
   268 reports/rapport-cycle-rapide.md
   806 reports/recapitulatif.md
   119 docs/note-un-pont-par-professeur.md
   107 docs/note-cout-professeur.md
   147 docs/note-regle-contrastive.md
   302 docs/note-cancellation-evenementielle.md
    98 docs/note-ingestion-corpus.md
    82 docs/note-corpus-panini.md
  2877 total
  ```

### 🤖 Assistant

⏵ Lecture du rapport du pont sémantique et du plateau.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pont-semantique.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pont-semantique.md</path>
<type>file</type>
<content>
1: # Rapport — le pont linguistique-sémantique, mesuré
2: 
3: **Mission** (clarifiée par Stéphane) : émuler **en boîte noire** le premier niveau
4: abstrait des gros modèles — celui où la représentation cesse d'être dominée par la
5: langue — pour avoir **notre propre pont linguistique-sémantique brut**. Il ne
6: s'agit pas de reproduire le gros modèle couche par couche, mais d'avoir un modèle
7: capable de **répondre à ce premier niveau abstrait**, pour n'importe quelle langue.
8: 
9: **Le professeur est une boîte noire** : on ne prend que son entrée et sa sortie.
10: `--trace-flux` les donne toutes les deux — la **couche 0 est la plongée du jeton**,
11: la **couche L est la cible**.
12: 
13: ## Protocole
14: 
15: - **Corpus** : article 1 de l'UDHR, `tools/extrait_udhr.py`.
16: - **Entraînement** : 8 langues — deu, eng, fra, ita, nld, por, rus, spa
17:   (7 écritures latines + le cyrillique).
18: - **Test** : 6 langues **jamais vues** — ell (grec), heb (hébreu), hin
19:   (devanagari), jpn (japonais), kor (coréen), tha (thaï). **Six écritures non
20:   latine
… [18228 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du plateau sémantique et du cycle rapide.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-plateau-semantique.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cycle-rapide.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-plateau-semantique.md</path>
<type>file</type>
<content>
1: # Rapport — le plateau sémantique, mesuré sur un corpus multilingue réel
2: 
3: **But** (Stéphane) : faire produire au moteur des réponses qui **émulent les
4: réponses sémantiques des modèles haut de gamme** sur nos corpus multilingues.
5: 
6: **Ce que ça exige d'abord** : un endroit où la représentation ne dépend plus de la
7: langue. Sans lui, il n'y a rien à émuler. On le mesure par l'**invariance à la
8: forme de surface** — deux textes de même sens dans deux langues doivent se
9: ressembler.
10: 
11: ## Corpus et méthode
12: 
13: **Article 1 de la Déclaration universelle des droits de l'homme**, dans **10
14: langues de familles et d'écritures différentes** : deu, eng, nld (germaniques),
15: fra, ita, por, spa (romanes), rus (cyrillique), hin (devanagari), jpn (japonais).
16: 
17: `tools/plateau_multilingue.py` : pour chaque couche, la similarité cosinus
18: **moyenne des 45 paires**, sur la représentation de l'énoncé entier, relevée par
19: `--trace-flux` et lue en DRVF.
20: 
21: ## Résultat 1 — le plateau existe, et il est au même endroit relatif
… [5796 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cycle-rapide.md</path>
<type>file</type>
<content>
1: # Le cycle rapide : l'article 1 de l'UDHR dans 399 langues
2: 
3: > 07/10. Réponse à une demande précise : *« peut-on refaire nos exercices sur un
4: > très petit modèle afin de faire des cycles de tests plus rapides entre les
5: > couches d'entrée et première couche sémantique ? »*
6: >
7: > La réponse est oui, mais **le modèle n'est pas le bon levier** — et c'est
8: > mesuré, pas supposé.
9: 
10: ---
11: 
12: ## 1. D'où venait la lenteur, chiffres en main
13: 
14: | poste | ce qui coûtait |
15: |---|---|
16: | traçage d'une entrée | **~16 s** sur Wikipedia (un article entier, `ctx 1024`, 9 couches) |
17: | taille d'une entrée | **~575 positions** (l'article entier, moyenné) |
18: | ajustement d'un pont | **5 à 10 min** sur 1 446 entrées × 575 positions, parce que la Grammaire `AᵀA` coûte `n·d²` avec `d = 1 792` |
19: 
20: Le coût d'un ajustement est en `n · d²` : **n** = nombre total de positions,
21: **d** = 2 × dimension cachée. Les deux termes sont attaquables, mais pas au même
22: prix :
23: 
24: - **diviser `d` par 1,5** (un modèle de 576 cachés au lieu
… [12727 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du rapport du pont génératif (résultats négatifs).

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pont-generatif.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pont-generatif.md</path>
<type>file</type>
<content>
1: # Le pont GÉNÉRATIF : le réseau naît, l'attrition le RÉDUIT
2: 
3: > **Le titre de ce rapport a été corrigé.** Il annonçait « l'attrition le fait
4: > généraliser » — ce que ce rapport même **dément** au §13 : mesurée sur la
5: > meilleure configuration, l'attrition fait **décroître la fidélité de test de
6: > façon monotone** (80 neurones : 0,6383 → 60 : 0,6356 → 20 : 0,6248 → 1 : 0,6169).
7: > Elle **réduit la taille à coût faible**, elle ne généralise rien. Le §16 ajoute
8: > qu'un seuil mal réglé la faisait même descendre jusqu'à un neurone. Un titre se
9: > lit plus que le corps : il ne doit pas promettre ce que le corps réfute.
10: 
11: `tools/pont_generatif.py` — deux phases, et c'est l'apprentissage qui décide des
12: tailles. Aucune rétropropagation : A et B restent aléatoires et **gelés**, seule la
13: lecture `W` s'ajuste par moindres carrés ridgés.
14: 
15: Perimètre : 40 langues d'entraînement (dont 4 ou 10 tenues pour la VALIDATION),
16: 6 langues de TEST jamais vues — `ell heb hin jpn kor tha`, écritures non latines.
17: Professeur : Qwen2.5-0
… [22207 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des notes de conception et des scripts du pont.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/note-un-pont-par-professeur.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/note-cout-professeur.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/note-regle-contrastive.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/note-un-pont-par-professeur.md</path>
<type>file</type>
<content>
1: # Un pont par professeur — il n'y a pas de couche sémantique universelle
2: 
3: Correction de cap, énoncée par Stéphane, et elle invalide une comparaison que
4: j'avais commise :
5: 
6: ## 1. Chaque modèle a sa propre représentation sémantique interne
7: 
8: On travaille sur une **couche interne**. Cette couche n'a de sens que *dans* le
9: modèle qui la produit : elle est exprimée dans SA base, SA métrique, SA façon de
10: répartir l'information. **Il n'existe pas, à ce jour, de représentation
11: universelle d'une couche sémantique.**
12: 
13: Conséquences directes :
14: 
15: - La cible change avec le professeur. Ce n'est pas la même chose à approximer.
16: - Il faut donc **une version de notre modèle par professeur** — `pont_0.5B`,
17:   `pont_30B`, etc. Ce ne sont pas des variantes d'un même objet, ce sont des
18:   objets distincts, chacun ajusté contre SA cible.
19: - **Comparer les invariances de deux ponts ajustés sur deux professeurs
20:   différents n'a pas de sens** : les deux nombres appartiennent à deux espaces de
21:   représentation différent
… [5476 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/note-cout-professeur.md</path>
<type>file</type>
<content>
1: # Le coût du professeur : ce qu'on calcule pour rien
2: 
3: Constat de départ : nos traces contiennent **toutes** les couches du professeur.
4: La mission s'arrête au premier niveau abstrait — couche 10 sur 24 pour Qwen2.5-0.5B,
5: couche 17 sur 48 pour Qwen3-30B-A3B. Tout ce qui suit est calculé, écrit, stocké,
6: et jamais lu.
7: 
8: ## 1. Le gaspillage, mesuré sur les traces existantes
9: 
10: | trace | professeur | couches stockées | profondeur utile | **gaspillé** |
11: |---|---|---|---|---|
12: | `vaste/eng.drvf` | Qwen2.5-0.5B | 0..23 + 1000..1023 | 0..10 | **77,4 %** |
13: | `langues30b/deu.drvf` | Qwen3-30B-A3B | 0..47 + 1000..1047 | 0..17 | **82,6 %** |
14: 
15: Les couches `1000+k` sont les sous-couches de la couche `k` : le traçage enregistre
16: les deux, donc 48 entrées de couche pour un modèle de 24.
17: 
18: ## 2. Ce que `--couches a:b` rattrape
19: 
20: Texte complet de l'UDHR en anglais (42 unités, 10 412 caractères), `--lot 1` :
21: 
22: | | couches tracées | enregistrements | taille | temps |
23: |---|---:|---:|---:|---:|
24: | sans `--couches
… [4508 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/note-regle-contrastive.md</path>
<type>file</type>
<content>
1: # Note — la règle contrastive : ce qu'il faut construire, et pourquoi c'est elle
2: 
3: > 06/10. Suite directe des trois négatifs mesurés (`rapport-plateau-semantique.md`
4: > et `note-cancellation-evenementielle.md` §9). Ce document dit **quoi faire**, pas
5: > ce qui a été fait.
6: 
7: ## 1. Le constat qui commande tout
8: 
9: | fait mesuré | conséquence |
10: |---|---|
11: | le plateau sémantique existe, à 35-42 % de la profondeur | il y a un endroit à viser |
12: | un modèle haut de gamme converge mieux (pire paire 0,471 contre 0,280) | il y a un écart à combler |
13: | **la lecture ne rattrape rien** (0,6027 au mieux, combiner dilue) | l'écart est **dans les poids** |
14: | **une règle locale non ciblée ne transfère pas** et dégrade les langues non vues | il faut une règle **ciblée** |
15: 
16: **Pourquoi la règle actuelle échoue, en une phrase** : `D += η·Δy⊗Δx` accumule les
17: statistiques de transition de **ce qu'elle voit**. Rien dans son écriture ne
18: distingue ce qui est **partagé** entre les cas de ce qui est **propre** à chacun.
19: Elle apprend
… [7059 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des résultats « directions/discriminants » et du récapitulatif.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"discriminant\\|direction\\|renforcement\\|énergie\\|energie\\|transfert\\|ridge\" reports/recapitulatif.md | head -60", "description": "Grep recapitulatif for direction work"}`

  ```
120:| **50 % de l'énergie** | **34** | **4 %** |
121:| 90 % de l'énergie | 293 | 33 % |
122:| 99 % de l'énergie | 599 | 67 % |
130:l'énergie) et son sous-ensemble actif est **partiellement propre à chaque
205:- Le sous-ensemble actif (34 canaux pour 50 % de l'énergie ; 24 % de canaux non
217:- Exploiter le sous-ensemble actif : viser les ~34 canaux qui portent l'énergie,
315:| énergie gardée | canaux | constante | **fid TEST** | écart | invariance | pire paire |
365:| énergie 90 % | 645 | 0,4945 | 0,5137 | **+0,0192** | 0,9530 | 0,8440 |
366:| énergie 75 % | 424 | 0,5319 | 0,5505 | **+0,0186** | 0,9575 | 0,8566 |
367:| énergie 50 % | 157 | 0,6140 | 0,6346 | **+0,0206** | **0,9653** | **0,8893** |
395:C'est le meilleur compromis mesuré : le critère d'**énergie** bat celui de
399:énergie qui portent la structure partagée.
424:| énergie 90 % | 645 | 0,5357 | 0,5137 | 0,959 |
425:| énergie 75 % | 424 | 0,5605 | 0,5505 | 0,982 |
426:| énergie 50 % | 157 | 0,6030 | 0,6346 | 1,052 |
563:Puisque l'écart est un écart de transfert, on standardise les états langue par
576:| langues d'apprentissage | fid TEST | oracle | **écart de transfert** |
613:0,62. **Le goulot est bien le transfert, même
… [1015 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^#\\{1,3\\} \" reports/rapport-toutes-langues.md | head -120", "description": "List headings of rapport-toutes-langues"}`

  ```
1:# Extension à toutes les langues, puis aux grands corpus
12:## 1. Le périmètre, inventorié
30:## 2. La convention de traçage, unique et vérifiée
53:## 3. Le découpage : stratifié par écriture, déduit du texte
73:## 4. Les cinq phases, chaînées
90:## 5. Mesure : l'invariance à dix points
103:## 6. Deux erreurs de méthode, et ce qu'elles ont coûté
121:## 7. Signal précoce : PLUS DE LANGUES AIDENT
158:## 8. La courbe de dose complète : elle NE sature PAS
170:### Ce que la courbe dit
187:### Réserve, toujours la même
197:## 9. Dimensionnement de l'analyse finale, mesuré
230:## 10. Signal précoce sur le panel STRATIFIÉ : l'écart de transfert était un artefact
250:### Ce que cela établit
262:### Réserve explicite
272:## 11. Mon seuil de couche par défaut était TROP STRICT
288:### Ce que cela dit du seuil
298:### Et un bug trouvé au passage
313:## 12. L'optimum du seuil de couche : 0,25, et c'est un maximum INTÉRIEUR
332:### Le réglage retenu
346:## 13. Le plateau sur 392 langues, et un effet de panel qui corrige une mesure antérieure
358:### Ce qui tient, et ce qui s'effondre
375:### Et l'écart test/validation, à pleine échelle
396:## 14. LE LIVRABLE DE LA PHASE 2 : le pont sur 301 lan
… [5689 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Poursuite de l'inventaire des chapitres du rapport « toutes langues ».

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^#\\{1,3\\} \" reports/rapport-toutes-langues.md | tail -80; echo \"TOTAL LINES:\"; wc -l reports/rapport-toutes-langues.md", "description": "Tail headings of big report"}`

  ```
5014:### 81.1 La lacune
5021:### 81.2 Les 50 tirages
5036:### 81.3 Et la comparaison honnête, sur le même panel
5044:### 81.4 Ce qui est corrigé
5061:### 81.5 Ce que la sélection Monte-Carlo apporte, chiffré
5078:### 81.6 La leçon, la troisième du même genre
5090:## 82. LA CIBLE DU PROJET ÉTAIT UN EFFET DE PANEL
5092:### 82.1 Ce qui a mis la puce à l'oreille
5106:### 82.2 Le même professeur, trois panels
5125:### 82.3 Pourquoi les langues romanes gonflent le rapport
5135:### 82.4 Et la couche 0, pour situer
5149:## 83. LA PIRE PAIRE : de–en, 1,494 — huit fois moins que la meilleure
5187:### 83.1 Ce que cela fait au « nous sommes à 2,487 »
5197:## 84. LE PROFIL EN PROFONDEUR : la séparation se fait entre les couches 3 et 5
5241:### 84.1 Le pooling : deux sondes, deux mondes
5263:## 85. NOTRE PONT SUR LA PIRE PAIRE : 14 à 23 % du professeur, et jusqu'à 62 % sur de–fr
5270:### 85.1 Deux sens croisés, tous deux HORS VIVIER
5278:### 85.2 Paire par paire
5289:### 85.3 Ce que ces chiffres disent, et ce qu'ils ne disent pas
5314:### 85.4 Ce qui reste ouvert après cette mesure
5328:## 86. LE DISCRIMINANT TRANSFÈRE — mais il perd l'essentiel en changeant de panel
5330:### 86.1 La question, p
… [3646 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^#\\{1,3\\} \" reports/recapitulatif.md", "description": "Headings of recapitulatif"}`

  ```
1:# Récapitulatif — méthode appliquée et résultats
25:## 1. La méthode
27:### 1.1 Boîte noire
34:### 1.2 Le pont
45:### 1.3 Architecture à couches RÉELLES
59:### 1.4 Phase générative
76:### 1.5 Attrition
89:## 2. Les résultats
91:### 2.1 La loi qui gouverne tout
114:### 2.2 Le sous-ensemble actif de la couche de référence
135:### 2.3 Le professeur contre lui-même
142:### 2.4 Architecture : ce qui a été départagé
157:## 3. Les corrections, et ce qu'elles ont invalidé
161:### 3.1 Un pont par professeur
171:### 3.2 L'extérieur du professeur
178:### 3.3 La troncature
185:### 3.4 Deux fautes contre moi-même
192:### 3.5 Les chiffres ronds
201:## 4. Ce qui est solide, ce qui ne l'est pas
226:## 5. Le déclencheur de couche, révisé — et ce qu'il mesure
228:### 5.1 La règle
246:### 5.2 Et l'ajout déclenche une RELECTURE du corpus
254:### 5.3 Ce que la mesure a donné, et il faut le dire tel quel
283:## 6. Le sous-ensemble actif : la piste qui monte la droite
285:### 6.1 Le déclencheur, corrigé une seconde fois
301:### 6.2 Une erreur que j'ai commise et corrigée
310:### 6.3 Le résultat, mesuré sur le même jeu
341:### 6.4 Ce que ça laisse ouvert
353:## 7. L'invariant : le pont apporte +0,020, q
… [1515 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de l'existence des fichiers cités dans la mission.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in tools/pont_recurrent.py tools/pont_fidele.py tools/pont_reservoir.py tools/pont_generatif.py tools/cache_pont.py tools/applique_pont.py tools/sonde_pont.py tools/compare_professeurs.py tools/rapport_du_pont.py tools/ancre_pr … [713 caractères tronqués]`

  ```
OK   tools/pont_recurrent.py
OK   tools/pont_fidele.py
OK   tools/pont_reservoir.py
OK   tools/pont_generatif.py
OK   tools/cache_pont.py
OK   tools/applique_pont.py
OK   tools/sonde_pont.py
OK   tools/compare_professeurs.py
OK   tools/rapport_du_pont.py
OK   tools/ancre_professeur.py
OK   tools/plateau_multilingue.py
OK   tools/lecture_plateau.py
OK   tools/invariance_semantique.py
OK   tools/invariance_ou_appauvrissement.py
OK   tools/invariance_unites.py
OK   tools/cancellation_langue.py
OK   tools/discriminant_transfert.py
OK   tools/stabilite_directions.py
OK   tools/renforcement_directions.py
OK   tools/energie_du_contenu.py
OK   tools/extrait_article1.py
OK   tools/premiere_couche_semantique.py
OK   tools/pont_parallele.py
OK   tools/pont_reglages.py
OK   tools/pont_unites.py
OK   tools/leviers_pont.py
OK   tools/objectif_du_pont.py
OK   tools/transfert_ridge.py
OK   tools/discriminant_contenu.py
OK   tools/renforcement.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -lat reports/ | head -25; echo \"=== tools récents ===\"; ls -lat tools/*.py | head -25", "description": "List most recent reports and tools"}`

  ```
total 1256
-rw-r--r--. 1 stephane stephane  24096  7 oct 20:29 rapport-passe-k3-disque.md
-rw-r--r--. 1 stephane stephane  12913  7 oct 19:34 rapport-cycle-rapide.md
drwxr-xr-x. 1 stephane stephane   4256  7 oct 18:22 .
drwxr-xr-x. 1 stephane stephane    612  7 oct 18:16 ..
-rw-r--r--. 1 stephane stephane 302658  7 oct 14:03 rapport-toutes-langues.md
-rw-------. 1 stephane stephane  36740  6 oct 04:44 recapitulatif.md
-rw-r--r--. 1 stephane stephane  21771  6 oct 04:43 rapport-pont-generatif.md
-rw-r--r--. 1 stephane stephane   6425  6 oct 04:42 rapport-plateau-semantique.md
-rw-r--r--. 1 stephane stephane  18223  5 oct 12:52 rapport-pont-semantique.md
-rw-r--r--. 1 stephane stephane   4424  5 oct 08:02 rapport-morcellement-experts.md
-rw-r--r--. 1 stephane stephane   4211  4 oct 10:43 rapport-cache-experts-vram.md
-rw-------. 1 stephane stephane   5941  3 oct 14:26 rapport-prefill-par-experts.md
-rw-------. 1 stephane stephane   6080  3 oct 11:51 rapport-reutilisation-experts.md
-rw-------. 1 stephane stephane   5096  3 oct 11:50 rapport-budget-kimi-k3.md
-rw-------. 1 stephane stephane   6772  3 oct 11:04 rapport-gpu-tandem-nvlink.md
-rw-------. 1 stephane stephane   8224  3 oct 
… [2647 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des sections « directions/discriminant » du grand rapport.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-toutes-langues.md", "offset": 5263, "limit": 400}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-toutes-langues.md</path>
<type>file</type>
<content>
5263: ## 85. NOTRE PONT SUR LA PIRE PAIRE : 14 à 23 % du professeur, et jusqu'à 62 % sur de–fr
5264: 
5265: Toutes les mesures du §82 portaient sur le professeur. Reste la question qui compte : **nous,
5266: sur ces mêmes paires ?** `rapport_du_pont.py` mesure les deux sur le même panel, avec le
5267: protocole de référence du dépôt (masque des canaux vivants ≥ 0,5, 120 neurones, lecture
5268: quadratique, ride 0,03, graine 5).
5269: 
5270: ### 85.1 Deux sens croisés, tous deux HORS VIVIER
5271: 
5272: | apprentissage | évaluation | fidélité TEST | notre rapport | professeur | **part** |
5273: |---|---|---:|---:|---:|---:|
5274: | de/en/fr | **es/it/pt** | 0,4780 | 1,676 | 12,001 | **14,0 %** |
5275: | es/it/pt | **de/en/fr** | 0,4652 | 0,301 | 1,316 | **22,9 %** |
5276: | de/en/fr | de/en/fr *(in-sample pour nous)* | 0,5067 | 0,193 | 1,316 | 14,6 % |
5277: 
5278: ### 85.2 Paire par paire
5279: 
5280: | évaluation | paire | notre P_lang | notre P_cont | **notre rapport** | professeur | **part** |
5281: |---|---|---:|---:|---:|---:|---:|
5282: | es/it/pt | es–it
… [22453 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de la fin du rapport (tableau de bord §91, directions §92-95).

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-toutes-langues.md", "limit": 400, "offset": 5663}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-toutes-langues.md</path>
<type>file</type>
<content>
5663: **Conséquence pour la conception** : la récurrence **n'est pas décorative**, mais elle n'est
5664: pas non plus ce qui porte la plus grosse part. Le résultat utile est le contraste entre les
5665: couches : **1 → 8, la dépendance au contexte augmente et la dépendance au jeton diminue**,
5666: ce qui est cohérent avec le profil du §84 (la séparation contenu/langue se construit entre
5667: les couches 3 et 5, exactement là où le gain contextuel culmine).
5668: 
5669: ### 89.4 Un piège de mesure à consigner, et il est de la même famille
5670: 
5671: La première version de cette mesure, lancée sur **8 articles anglais** (3 674 positions),
5672: donnait `R²(0) = 0,5632` et `R²(fenêtre) = 0,8689` — un gain de **+70 %** au lieu de +11,7 %.
5673: Le chiffre était quatre fois trop grand.
5674: 
5675: **La cause : 2 688 variables pour 3 674 points.** Dans ce régime, un R² **calculé sur les
5676: données d'ajustement** est gonflé par la capacité du modèle à interpoler. Le passage à
5677: 164 775 positions rend la mesure honnête. Il n'y avait aucun bug : seulement un
… [21977 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des tout derniers paragraphes (rang 1/2/3, portée du contexte).

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-toutes-langues.md", "offset": 6063, "limit": 130}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-toutes-langues.md</path>
<type>file</type>
<content>
6063: axe, parfaitement reproductible — donnerait-il l'essentiel du gain ? C'est la mesure la plus
6064: simple qui reste à faire, et elle est décisive pour un déploiement : **un axe stable et
6065: calculable en forme fermée vaut mieux qu'un plan dont la moitié dépend d'un tirage.**
6066: 
6067: ---
6068: 
6069: ## 94. RANG 1, 2 OU 3 : le meilleur rang n'est pas celui du meilleur chiffre
6070: 
6071: ### 94.1 L'hypothèse que je m'étais faite, et sa réfutation
6072: 
6073: Le §93.4 terminait sur une hypothèse, écrite noir sur blanc : *« le premier axe est stable, le
6074: second ne l'est pas — un discriminant de **rang 1** donnerait-il l'essentiel du gain ? Un axe
6075: stable et calculable en forme fermée vaut mieux qu'un plan dont la moitié dépend d'un
6076: tirage. »*
6077: 
6078: **C'était plausible, et c'est faux.** Six graines, même protocole, même panel que le §93,
6079: rangs 1, 2 et 3 :
6080: 
6081: | rang | moyenne | écart-type | **min** | max | étalement |
6082: |---|---:|---:|---:|---:|---:|
6083: | **1** | 112,3 % | 19,7 % | **75,2 %** | 135,0 % | 
… [6343 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des résultats liés à renforcement/stabilité/énergie.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"stabilite_directions\\|renforcement_directions\\|energie_du_contenu\\|discriminant_transfert\\|ancre_professeur\\|compare_professeurs\\|premiere_couche_semantique\" reports/ docs/ sprints/ REPRISE.md journal/ 2>/dev/null | … [64 caractères tronqués]`

  ```
reports/rapport-toutes-langues.md:5431:C'est la prochaine mesure. Les outils sont en place : `discriminant_transfert.py` prend trois
reports/rapport-cycle-rapide.md:100:`tools/premiere_couche_semantique.py` la mesure **avec les deux poolings**
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:6673:**La méthode** — naissance d'un neurone à la fois, un neurone ajouté ne lit que la couche précédente (et sa propre couche) ; attrition par **redondance** avec **recalcul** des trajectoires des survivants et réajustement de la lecture ; `A` et `B` aléatoires et gelés, seule la lecture s'ajuste en forme fermée. Outil : `tools/pont_generatif.py` (41 ko), plus `cache_pont.py`, `compare_professeurs.py`, `sous_ensemble_actif.py`.
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:9801:- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/renforcement_directions.py`
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:10762:| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/renforcement_directions.py` | 1 | 0 |
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:10764:| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/anc
… [5441 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la sprints/ | head -50; echo \"=== JOURNAL ===\"; ls -la journal/", "description": "List sprints and journal"}`

  ```
total 356
drwxr-xr-x. 1 stephane stephane  2624  3 oct 15:38 .
drwxr-xr-x. 1 stephane stephane   612  7 oct 18:16 ..
-rw-r--r--. 1 stephane stephane 11248 30 sep 19:41 01-premier-des-trois-noyaux-gpu-du-top-k-le.md
-rw-r--r--. 1 stephane stephane  8829 30 sep 21:49 02-fusionner-la-cha-ne-du-top-k-d-port-desc.md
-rw-r--r--. 1 stephane stephane 10153 30 sep 23:44 03-qualit-de-l-attention-creuse-long-contex.md
-rw-r--r--. 1 stephane stephane  7931  1 oct 01:37 04-le-k-de-l-attention-creuse-l-chec-au-mil.md
-rw-r--r--. 1 stephane stephane  7358  1 oct 03:37 05-refaire-la-grille-avec-de-vraies-fenetres.md
-rw-r--r--. 1 stephane stephane  6232  1 oct 05:39 06-le-taux-de-recuperation.md
-rw-r--r--. 1 stephane stephane 10564  1 oct 07:40 07-cloture-de-la-nuit.md
-rw-------. 1 stephane stephane 18635  1 oct 12:35 08-un-modele-eclate-se-lit-comme-un-seul.md
-rw-------. 1 stephane stephane  6233  1 oct 17:43 09-empreinte-memoire-ce-qui-reduit-vraiment.md
-rw-------. 1 stephane stephane 11649  2 oct 18:56 10-v41-la-chaine-retardee-et-le-compresseur.md
-rw-------. 1 stephane stephane  6396  2 oct 19:18 11-v41-la-passe-complete.md
-rw-------. 1 stephane stephane  8218  2 oct 20:33 12-la-rotation
… [2088 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection des sessions récentes du journal.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -lat journal/sessions/ | head -15; echo \"=== taille des rapports récents ===\"; ls -la journal/sessions/*/ 2>/dev/null | head -40", "description": "List recent journal sessions"}`

  ```
total 4
drwxr-xr-x. 1 stephane stephane   74  8 oct 09:17 d31b3d9b-58e4-4d34-85fa-381b6f6a6a76
-rw-r--r--. 1 stephane stephane 3832  8 oct 09:17 MANIFEST.md
drwxr-xr-x. 1 stephane stephane 3428  8 oct 09:17 .
drwxr-xr-x. 1 stephane stephane   74  2 oct 21:17 e14c26ae-6d52-41f9-a72f-6ebdcef172d5
drwxr-xr-x. 1 stephane stephane   74  2 oct 20:04 7f3f463f-9213-4721-b9a7-82858ef93f8c
drwxr-xr-x. 1 stephane stephane   74  2 oct 20:04 31f26a6e-65f5-480d-be32-36b9f425b3dd
drwxr-xr-x. 1 stephane stephane   74  2 oct 20:04 1820cf6b-c8a4-411c-894c-31195b9ff7a8
drwxr-xr-x. 1 stephane stephane   74  2 oct 18:17 8734fc13-aeb8-4cdf-b005-c182f77be0dc
drwxr-xr-x. 1 stephane stephane   74  2 oct 15:17 fba448b3-e237-4eb3-b77d-fcbf7da1c93d
drwxr-xr-x. 1 stephane stephane   74  2 oct 15:17 f2de810a-b765-444d-b3cc-d8fce1ba2105
drwxr-xr-x. 1 stephane stephane   74  2 oct 15:17 dcaa24d6-0017-4382-be21-8244c0fb9b7a
drwxr-xr-x. 1 stephane stephane   74  2 oct 15:17 b13a6032-4f62-4e86-aa1f-03864a455c83
drwxr-xr-x. 1 stephane stephane   74  2 oct 15:17 8549abcb-5d9a-4594-915b-5628c80a2a08
drwxr-xr-x. 1 stephane stephane   74  2 oct 15:17 56879594-1434-4e34-83cc-de42cdf192a1
=== taille des rapports récents ==
… [1860 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de l'état des sous-agents d'inventaire.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/ && grep -n \"^#\\{1,2\\} \" journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md | head -60", "description": "Inspect main pont session report"}`

  ```
total 65556
drwxr-xr-x. 1 stephane stephane       74 28 sep 15:19 .
drwxr-xr-x. 1 stephane stephane     3428  8 oct 09:17 ..
-rw-r--r--. 1 stephane stephane  9404457  8 oct 09:17 digest.md
-rw-r--r--. 1 stephane stephane   839537  8 oct 09:17 rapport.md
-rw-------. 1 stephane stephane 56879838  7 oct 21:14 session.jsonl.zstd
1:# Session bbd6969f — Continue avec REPRISE.md
18:## Objectifs déclarés
59:## 1. Ce qui a été demandé
471:## 2. Déroulé, étape par étape
10545:## 3. Travail accompli
10851:## 4. Mesures et résultats marquants
10975:## 5. Erreurs rencontrées
10995:## 6. Commits
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/recapitulatif.md", "limit": 230}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/recapitulatif.md</path>
<type>file</type>
<content>
1: # Récapitulatif — méthode appliquée et résultats
2: 
3: État au 06/10. Un seul professeur : **Qwen2.5-0.5B**.
4: 
5: > **DEUX AVERTISSEMENTS POUR LIRE CE DOCUMENT.**
6: >
7: > **1. La couche cible a changé.** Tout ce document émule la **couche 10**. Des
8: > mesures postérieures (Romeo et UDHR) montrent que le plateau du professeur est à
9: > la **couche 8** : 0,5985 contre 0,5703 sur Romeo, 0,5471 contre 0,5247 sur
10: > l'UDHR. Viser la couche 8 fait gagner **+0,0213 de fidélité transférée**. Les
11: > chiffres ci-dessous restent exacts — ils portent sur la couche 10 — mais ils ne
12: > décrivent pas le meilleur pont possible. Voir `rapport-toutes-langues.md` §17-19.
13: >
14: > **2. Le §7 est corrigé au §15.** Le §7 annonce « l'invariant : le pont apporte
15: > +0,020, **quelle que soit la cible** ». Le §15 montre que c'est une **plage de
16: > +0,020 à +0,032** : les sept périmètres qui donnaient +0,0197 ± 0,0009
17: > partageaient le **même panel de 46 langues**. Les deux sections sont conservées
18: > — la correction fait partie du travail — mais ne les lisez p
… [9472 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des sections « sous-ensemble actif » et « lecture non linéaire » du récapitulatif.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/recapitulatif.md", "limit": 240, "offset": 283}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/recapitulatif.md</path>
<type>file</type>
<content>
283: ## 6. Le sous-ensemble actif : la piste qui monte la droite
284: 
285: ### 6.1 Le déclencheur, corrigé une seconde fois
286: 
287: Trois conditions **simultanées**, et la première manquait :
288: 
289: 1. **la couche courante est ÉPUISÉE** — les derniers neurones n'apportent plus
290:    rien. Tant qu'un neurone de plus paie, c'est lui qu'il faut : couvrir une
291:    activation manquante est un travail de **neurone**, pas de couche ;
292: 2. **des concepts communs existent** — il y a de la structure partagée à composer ;
293: 3. **la lecture doit soustraire** — c'est le « OU exclusif ».
294: 
295: Sans la condition 1, le critère déclenchait à **chaque pas** : 9 couches pour
296: 72 neurones, mesuré. Avec elle :
297: 
298: **80 neurones en 5 couches [41, 15, 8, 8, 8]** — la moitié de la croissance au
299: premier niveau, la composition ensuite, et aucun chiffre rond.
300: 
301: ### 6.2 Une erreur que j'ai commise et corrigée
302: 
303: J'ai d'abord annoncé que **la restriction aux canaux actifs faisait émerger les
304: concepts communs** (`communs` passant de +0,07
… [11283 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"Hebb\\|hebb\" reports/ docs/ | head -20; echo \"=== mentions DRAVE_HEBB ===\"; grep -rn \"DRAVE_HEBB\" drave-core/ tools/ 2>/dev/null | head -10", "description": "Find Hebb-related reports and code"}`

  ```
reports/rapport-capteur-hebbien.md
reports/rapport-programme-evolutif.md
reports/rapport-greffon.md
reports/rapport-localite-activation.md
reports/rapport-drapeaux-ignores.md
reports/rapport-plateau-semantique.md
reports/rapport-toutes-langues.md
docs/programme-recherche.md
docs/roadmap.md
docs/vision.md
docs/glossaire.md
docs/note-cancellation-evenementielle.md
docs/note-regle-contrastive.md
=== mentions DRAVE_HEBB ===
drave-core/src/main.rs:73:    if let Ok(c) = std::env::var("DRAVE_HEBB_SAUVER") { hd.sauver(&c); }
drave-core/src/main.rs:1040:        if let Ok(c) = std::env::var("DRAVE_HEBB_CHARGER") { hd.charger(&c); }
drave-core/src/model.rs:2822:                   seuil: std::env::var("DRAVE_HEBB_SEUIL").ok()
drave-core/src/model.rs:2824:                   signe: std::env::var("DRAVE_HEBB_SIGNE").map(|v| v != "0" && !v.is_empty())
drave-core/src/model.rs:2826:                   decroi: std::env::var("DRAVE_HEBB_DECROI").ok()
  ```

### 🤖 Assistant

⏵ Lecture du résultat négatif de la règle locale (note cancellation §9).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^#\\{1,3\\} \" docs/note-cancellation-evenementielle.md", "description": "Headings of cancellation note"}`

  ```
1:# Note — la voie événementielle : prédire une couche pour ne transporter que l'imprévu
7:## 1. Ce que le moteur a déjà, et qui n'est pas un détour
21:## 2. La question préalable, et elle est mesurable sans rien changer au modèle
34:## 3. Comment le mesurer, par couche
60:## 4. État au 06/10
81:## 5. La limite, dite franchement
90:## 6. Le bloc 0-9 est-il approximable ? Première borne (06/10)
131:## 7. L'apprentissage hebbien différentiel — implémenté et mesuré (06/10)
133:### Ce qui existait
139:### Ce qui a été ajouté : `HebbDiff`
168:### Les mesures
193:### 8. Le test hors échantillon N'A PAS TOURNÉ — et pourquoi
223:### Ce qui reste à mesurer, et c'est le seul test qui compte
231:## 9. Le verdict hors échantillon : la règle locale NE TRANSFÈRE PAS (06/10, 10h50)
236:### Test 1 — un autre texte
241:### Test 2 — un corpus multilingue
247:### Test 3 — l'invariance inter-langue, et l'apparence d'un succès
272:### Ce que ça établit
285:### Ce qu'il faudrait, et ce n'est plus la même règle
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"renforcement\\|Hebb\\|hebb\" reports/rapport-toutes-langues.md | head -30", "description": "Grep Hebb mentions in big report"}`

  ```
4160:## 72. Le dernier mécanisme sanctionné par le mandat — renforcement/atrophie — échoue aussi
4172:> par renforcement/atrophie (pas de backprop). »*
4206:J'ai testé **la forme de renforcement implémentée dans le dépôt**, appliquée comme le
4207:mandat la décrit. **D'autres formes existent** — un renforcement portant sur les poids
4208:d'entrée `B` plutôt que sur l'échelle globale, un renforcement compétitif entre
4221:| **renforcement/atrophie** | **§72** | **+1,7 % du chemin nécessaire** |
4230:linéaire ne les improvise pas ; un renforcement local ne les découvre pas.
4262:renforcement est impuissant, mais parce que **sa forme implémentée produit une
4266:n'écartait pas « le renforcement », il écartait « le renforcement **par mise à
4286:chaque neurone ne reçoit qu'une direction. C'est de la règle de Hebb appliquée à
4327:**1. Le renforcement n'est pas impuissant — sa forme par mise à l'échelle l'était.** Le
4396:| mise à l'échelle du renforcement (§72) | oui | 1,312 — **forcé par l'identité du §67** | 317,0 |
4495:| 72 | le renforcement par mise à l'échelle est **forcé à l'échec** par le §67 | 1,312 |
4739:(§69, bornée à 64 %), ni le renforcement/atrophie (§72, +1,7 % du chemi
… [14 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des échecs du renforcement (§72) et du verdict hors échantillon.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/note-cancellation-evenementielle.md", "offset": 231, "limit": 72}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-toutes-langues.md", "offset": 4160, "limit": 150}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/note-cancellation-evenementielle.md</path>
<type>file</type>
<content>
231: ## 9. Le verdict hors échantillon : la règle locale NE TRANSFÈRE PAS (06/10, 10h50)
232: 
233: Trois tests, du plus faible au plus fort. **Les trois sont négatifs**, et le
234: troisième est le plus instructif.
235: 
236: ### Test 1 — un autre texte
237: 
238: `D` appris sur un texte A, noté sur un texte B : **29,151 contre 29,151** —
239: identique au chiffre près. Aucun transfert.
240: 
241: ### Test 2 — un corpus multilingue
242: 
243: `D` appris sur l'article 1 de l'UDHR en 40 langues (‖D‖ = 3,65), noté sur un
244: article 2 en breton, langue absente : **1116,532 contre 1116,532**. Aucun
245: transfert non plus.
246: 
247: ### Test 3 — l'invariance inter-langue, et l'apparence d'un succès
248: 
249: `D` appris sur l'article 1 en 40 langues, puis **re-mesure du plateau** sur 10
250: langues :
251: 
252: | | sans adaptateur | avec |
253: |---|---:|---:|
254: | pic de convergence | 0,649 | **0,7247** |
255: 
256: **+11,7 %, au-dessus du 30B (0,693).** Un résultat qui avait l'air d'un succès.
257: 
258: **Il n'en était pas un** : les 10 langues de t
… [2549 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-toutes-langues.md</path>
<type>file</type>
<content>
4160: ## 72. Le dernier mécanisme sanctionné par le mandat — renforcement/atrophie — échoue aussi
4161: 
4162: ### 72.1 Pourquoi c'était le dernier recours
4163: 
4164: Les §57-§71 ont écarté, par neuf mesures, tous les moyens de **post-traiter** la sortie.
4165: Le §70 a montré que la transformation qui **crée** la séparation contenu/langue entre la
4166: couche 0 et la couche 8 (rapport 10,912 contre 1,698) n'est pas reproduite par un
4167: réservoir à poids aléatoires gelés.
4168: 
4169: Restait **un** mécanisme, et il est explicitement sanctionné par le mandat :
4170: 
4171: > *« L'ajout d'une couche suppose donc une relecture du corpus pour réajuster les poids
4172: > par renforcement/atrophie (pas de backprop). »*
4173: 
4174: C'est le seul ajustement de poids autorisé en dehors de la lecture, et il n'avait
4175: **jamais** été testé sur l'axe contenu/langue.
4176: 
4177: ### 72.2 Le mécanisme, tel qu'il est implémenté
4178: 
4179: `Pont.renforce` : on ajuste la lecture, on calcule le **résidu** `R = Y − (φ(X)·W + mt)`,
4180: puis pour chaque neurone on m
… [6936 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Consultation des deux sous-agents d'inventaire.

- **list_agents** `{}`

  ```
a4277668-3825-4797-bf0b-d7addcbb569d [running] — Inventaire corpus dépôt
ee19a880-cc76-4c5c-9fe0-5972bd73b533 [running] — Inventaire poids et entraînements
  ```

### 🤖 Assistant

⏵ Recherche directe des artefacts de poids sur la machine.

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/corpus/ 2>&1 | head -30; echo \"=== udhr ===\"; ls -la /home/stephane/Data13TB/stephane/corpus/udhr/ 2>&1 | head -30", "description": "Inspect corpus dir near repo"}`

  ```
total 0
drwxr-xr-x. 1 stephane stephane    108  6 oct 14:51 .
drwxr-xr-x. 1 stephane stephane   2342  6 oct 09:23 ..
drwxr-xr-x. 1 stephane stephane    876  6 oct 15:26 parallele_crime
drwxr-xr-x. 1 stephane stephane    960  6 oct 03:40 parallele_rj
drwxr-xr-x. 1 stephane stephane    742  7 oct 18:39 udhr
drwxr-xr-x. 1 stephane stephane 108760  7 oct 09:13 wiki_apparie
drwxr-xr-x. 1 stephane stephane  10560  6 oct 06:47 wiki_traces
=== udhr ===
total 8992
drwxr-xr-x. 1 stephane stephane     742  7 oct 18:39 .
drwxr-xr-x. 1 stephane stephane     108  6 oct 14:51 ..
drwxr-xr-x. 1 stephane stephane      70  5 oct 10:07 appr
drwxr-xr-x. 1 stephane stephane     640  5 oct 12:03 appr10
drwxr-xr-x. 1 stephane stephane     640  5 oct 15:14 appr10c
drwxr-xr-x. 1 stephane stephane     640  5 oct 11:14 appr40
drwxr-xr-x. 1 stephane stephane       0  5 oct 11:46 appr42
drwxr-xr-x. 1 stephane stephane    5586  7 oct 17:52 article1
drwxr-xr-x. 1 stephane stephane    6384  7 oct 18:39 article1_traces
drwxr-xr-x. 1 stephane stephane    5586  7 oct 18:16 article2
drwxr-xr-x. 1 stephane stephane    6384  7 oct 19:27 article2_traces
-rw-r--r--. 1 stephane stephane     415  5 oct 09:47 ids_test.txt
-r
… [1098 caractères tronqués]
  ```

- **bash** `{"command": "find /home/stephane/Data13TB/stephane -maxdepth 4 \\( -name \"*.npz\" -o -name \"*.pt\" -o -name \"*.npy\" \\) 2>/dev/null | head -40; echo \"=== tailles ===\"; du -sh /home/stephane/Data13TB/stephane/corpus 2>/dev/null", "description": "Find weight artifacts"}`

  ```
/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique.npz
/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz
/home/stephane/Data13TB/stephane/pont_semantique.npz
=== tailles ===
35G	/home/stephane/Data13TB/stephane/corpus
  ```

### 🤖 Assistant

⏵ Vérification de ce que les scripts du pont sauvegardent réellement.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"savez\\|savez_compressed\\|np.save\\|\\.npz\\|\\.pt\\b\" tools/pont_reservoir.py tools/pont_generatif.py tools/pont_fidele.py tools/pont_recurrent.py tools/pont_parallele.py tools/pont_reglages.py tools/pont_unites.py tools … [311 caractères tronqués]`

  ```
tools/pont_generatif.py:24:  pont_generatif.py <train.npz> <test.npz> [--a 0.2] [--ride 0.3] [--val 4]
tools/pont_recurrent.py:189:    #     et pas seulement une mesure. `pont_semantique.npz` porte les trois pièces
tools/pont_recurrent.py:191:    chemin = os.environ.get("DRAVE_PONT_SORTIE", "pont_semantique.npz")
tools/pont_recurrent.py:192:    np.savez(chemin, P=P, moy=moy, W0=W0, couche=c, rang=rang,
tools/pont_parallele.py:19:Usage : pont_parallele.py <cache_A.npz> <cache_B.npz> [--couche 10] [--canaux 0.5]
tools/pont_reglages.py:12:Usage : pont_reglages.py <train.npz> <test.npz> [--levier fuite|rayon|neurones|ensemble|saut|tous]
tools/pont_unites.py:17:Usage : pont_unites.py <train.npz> <test.npz> [--canaux 0.5] [--lecture quadratique]
tools/cache_pont.py:8:Usage : cache_pont.py <dossier> <sortie.npz> [--couche 10] [--hidden 896]
tools/cache_pont.py:79:    np.savez_compressed(sortie, cles=np.array(cles), hidden=hidden,
tools/applique_pont.py:4:Le pont est un artefact : trois matrices ajustées une fois (`pont_semantique.npz`),
tools/applique_pont.py:12:Usage : applique_pont.py <pont.npz> <trace.drvf> [--sortie abstrait.npy]
tools/applique_pont.py:76:        np.save(sys.argv[sys.
… [656 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport numpy as np\nfor p in ['/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique.npz','/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz','/home/stephane/Data13TB/stephane/pont_semantique.n … [230 caractères tronqués]`

  ```
/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique.npz {'P': ((896, 128), 'float32'), 'moy': ((896,), 'float32'), 'W0': ((896, 128), 'float64'), 'couche': ((), 'int64'), 'rang': ((), 'int64'), 'langues_train': ((20,), '<U3'), 'langues_test': ((20,), '<U3')}
/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz {'P': ((896, 1), 'float32'), 'moy': ((896,), 'float32'), 'W0': ((896, 1), 'float64'), 'couche': ((), 'int64'), 'rang': ((), 'int64'), 'langues_train': ((20,), '<U3'), 'langues_test': ((20,), '<U3')}
/home/stephane/Data13TB/stephane/pont_semantique.npz {'P': ((896, 128), 'float32'), 'moy': ((896,), 'float32'), 'W0': ((896, 128), 'float64'), 'couche': ((), 'int64'), 'rang': ((), 'int64'), 'langues_train': ((20,), '<U3'), 'langues_test': ((20,), '<U3')}
  ```

### 🤖 Assistant

⏵ Recherche des caches d'activations utilisés pour l'ajustement.

- **bash** `{"command": "find /home/stephane/Data13TB/stephane -maxdepth 3 -name \"cache*.npz\" 2>/dev/null | head -20; echo \"=== tous npz hors repo ===\"; find /home/stephane/Data13TB/stephane -maxdepth 3 -name \"*.npz\" 2>/dev/null | head -30; echo \"=== dans repo ===\"; find /home/stephane/Data13TB/stephane … [115 caractères tronqués]`

  ```
=== tous npz hors repo ===
/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique.npz
/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz
/home/stephane/Data13TB/stephane/pont_semantique.npz
=== dans repo ===
  ```

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/corpus/wiki_apparie/ 2>/dev/null | head -15; echo \"=== taille wiki_apparie ===\"; du -sh /home/stephane/Data13TB/stephane/corpus/wiki_apparie /home/stephane/Data13TB/stephane/corpus/wiki_traces /home/stephane/Data13TB/stephane/corpus/parallele_rj … [113 caractères tronqués]`

  ```
total 11568
drwxr-xr-x. 1 stephane stephane 108760  7 oct 09:13 .
drwxr-xr-x. 1 stephane stephane    108  6 oct 14:51 ..
-rw-r--r--. 1 stephane stephane   2019  6 oct 13:54 de_Aaliyah.txt
-rw-r--r--. 1 stephane stephane   2050  6 oct 13:54 de_Aarhus.txt
-rw-r--r--. 1 stephane stephane   1058  6 oct 13:54 de_Aaron.txt
-rw-r--r--. 1 stephane stephane   2023  6 oct 13:54 de_ABBA.txt
-rw-r--r--. 1 stephane stephane   2027  6 oct 13:54 de_ABC.txt
-rw-r--r--. 1 stephane stephane   2022  6 oct 13:54 de_Abel_Tasman.txt
-rw-r--r--. 1 stephane stephane   1126  6 oct 13:54 de_Abel.txt
-rw-r--r--. 1 stephane stephane   2029  6 oct 13:54 de_Aberdeenshire.txt
-rw-r--r--. 1 stephane stephane   2037  6 oct 13:54 de_Aberdeen.txt
-rw-r--r--. 1 stephane stephane   2048  6 oct 13:54 de_AbiWord.txt
-rw-r--r--. 1 stephane stephane   2019  6 oct 13:54 de_Abner_Doubleday.txt
-rw-r--r--. 1 stephane stephane   2054  6 oct 13:54 de_Abner.txt
=== taille wiki_apparie ===
12G	/home/stephane/Data13TB/stephane/corpus/wiki_apparie
1,8G	/home/stephane/Data13TB/stephane/corpus/wiki_traces
988M	/home/stephane/Data13TB/stephane/corpus/parallele_rj
261M	/home/stephane/Data13TB/stephane/corpus/parallele_crime
  ```

### 🤖 Assistant

⏵ Lecture du pont à l'échelle (301 langues) et de la correction de cible couche 8.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-toutes-langues.md", "limit": 60, "offset": 396}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-toutes-langues.md", "limit": 140, "offset": 526}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-toutes-langues.md</path>
<type>file</type>
<content>
396: ## 14. LE LIVRABLE DE LA PHASE 2 : le pont sur 301 langues
397: 
398: | | |
399: |---|---:|
400: | apprentissage / validation | **301 / 50 langues** |
401: | test | **41 langues · 22 écritures** |
402: | réseau | **40 neurones · 1 couche** |
403: | fidélité apprentissage | 0,7459 |
404: | fidélité VALIDATION | 0,7505 |
405: | **fidélité TEST** | **0,7430** (constante 0,7207) |
406: | **invariance TEST** | **0,9827** |
407: | **pire paire** | **0,9165** |
408: | oracle TEST | 0,7653 — écart **+0,0223** |
409: | oracle VALIDATION | 0,7563 — écart **+0,0058** |
410: | **écart à la constante** | **+0,0223** |
411: 
412: ### Les trois choses qui tiennent, à pleine échelle
413: 
414: **1. L'écart test/validation est de 1,01** (0,7505 / 0,7430), contre **2,58** sur
415: l'ancien panel uniquement non latin. Le diagnostic de typologie est **confirmé sur
416: le panel complet**, et pas seulement sur le signal précoce.
417: 
418: **2. L'écart de transfert tombe à +0,0223** (oracle test), contre **+0,0693** sur
419: l'ancien panel — **3,1× plus petit**. Là encore, ce 
… [1860 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-toutes-langues.md</path>
<type>file</type>
<content>
526: ## 17. Le plateau du professeur est à la couche 8, PAS à la couche 10
527: 
528: Mesure sur le corpus parallèle *Romeo and Juliet*, invariance **segment par
529: segment** (24 scènes appariées) :
530: 
531: | couche | invariance moyenne | pire scène |
532: |---|---:|---:|
533: | 0 (plongement) | **0,1420** | **−0,0888** |
534: | 4 | 0,4483 | 0,1289 |
535: | **8** | **0,5985** | 0,1943 |
536: | 10 | 0,5703 | **0,2381** |
537: 
538: **Le plateau est à la couche 8** ; la couche 10 est déjà **en re-spécialisation**
539: vers la sortie (0,5703 contre 0,5985).
540: 
541: **Et ce n'est pas propre à ce corpus.** Sur l'UDHR propre (46 langues), je
542: mesurais **0,5471 à la couche 8 contre 0,5247 à la couche 10**. Les deux corpus
543: concordent.
544: 
545: ### Ce que cela remet en cause
546: 
547: **Ma cible était mal choisie.** Depuis le début de ce travail, le pont émule la
548: **couche 10** — parce que la mesure initiale, faite sur l'article 1 de l'UDHR avec
549: quarante langues, plaçait le pic à 42 % de profondeur (couche 10 sur 24). Les deux
550: mesures d
… [5845 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection rapide des producteurs de corpus, en parallèle des sous-agents.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in tools/extrait_udhr.py tools/extrait_article1.py tools/extrait_wikipedia.py tools/extrait_gutenberg.py tools/extrait_crime.py tools/wiki_apparie.py; do echo \"##### $f\"; head -22 \"$f\" | sed -n '1,22p'; echo; done 2>&1 | he … [60 caractères tronqués]`

  ```
##### tools/extrait_udhr.py
#!/usr/bin/env python3
"""extrait_udhr.py — l'UDHR en unités alignées, prêtes à passer dans le moteur.

L'UDHR est le premier corpus parce que l'alignement y est **par construction** :
les 30 articles existent dans les 456 langues, et c'est le même énoncé. Aucun
aligneur, donc aucun décalage possible — le contraire d'un corpus apparié à la
main.

Sortie : un JSON par unité `(article, paragraphe)`, et un index. Chaque unité
porte le texte de CHAQUE langue, pour qu'on puisse la faire passer dans les
couches d'entrée langue par langue et comparer les activations.

Usage :
    extrait_udhr.py <dossier_udhr_xml> <sortie.jsonl> [--min-langues 50]
"""
import glob
import json
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET

##### tools/extrait_article1.py
#!/usr/bin/env python3
"""extrait_article1.py — l'ARTICLE 1 DE L'UDHR, dans toutes les langues, en un fichier par langue.

POURQUOI CE CORPUS, ET PAS UN AUTRE.

Les cycles de cette session ont été lents (traces de 15 s, ajustements de pont de
plusieurs minutes) parce que chaque entrée portait un TEXTE ENTIER : 482 articles
de 575 positions, ou l'UDHR complet. Or l'unité d'al
… [5410 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mesure des corpus sur disque (UDHR, Wikipedia, Gutenberg).

- **bash** `{"command": "du -sh /home/stephane/Data13TB/stephane/nipada/wikipedia_decompressed 2>/dev/null; ls /home/stephane/Data13TB/stephane/nipada/wikipedia_decompressed 2>/dev/null | head; echo \"=== data/wikipedia ===\"; du -sh /home/stephane/Data13TB/stephane/data/wikipedia 2>/dev/null; ls -la /home/step … [248 caractères tronqués]`

  ```
81G	/home/stephane/Data13TB/stephane/nipada/wikipedia_decompressed
de
en
es
fr
it
ru
=== data/wikipedia ===
132G	/home/stephane/Data13TB/stephane/data/wikipedia
total 68722292
drwxr-xr-x. 1 stephane stephane         940  6 oct 13:51 .
drwxr-xr-x. 1 stephane stephane          14 25 mai 14:39 ..
-rw-r--r--. 1 stephane stephane  3505520640 26 mai 10:48 arwiki_v14.db
-rw-r--r--. 1 stephane stephane       32768  6 oct 13:51 arwiki_v14.db-shm
-rw-r--r--. 1 stephane stephane           0  6 oct 13:49 arwiki_v14.db-wal
-rw-r--r--. 1 stephane stephane  9424920576 25 mai 21:35 dewiki_v14.db
-rw-r--r--. 1 stephane stephane       32768  6 oct 13:51 dewiki_v14.db-shm
-rw-r--r--. 1 stephane stephane           0  6 oct 13:49 dewiki_v14.db-wal
-rw-r--r--. 1 stephane stephane 19540979712 26 mai 06:09 enwiki_v14.db
-rw-r--r--. 1 stephane stephane       32768  6 oct 13:51 enwiki_v14.db-shm
-rw-r--r--. 1 stephane stephane           0  6 oct 13:49 enwiki_v14.db-wal
-rw-r--r--. 1 stephane stephane  5506088960 26 mai 12:37 eswiki_v14.db
-rw-r--r--. 1 stephane stephane       32768  6 oct 13:51 eswiki_v14.db-shm
-rw-r--r--. 1 stephane stephane           0  6 oct 13:51 eswiki_v14.db-wal
=== gutenberg ===
/ho
… [1064 caractères tronqués]
  ```

- **bash** `{"command": "du -sh /home/stephane/Data13TB/stephane/udhr_xml 2>/dev/null; find /home/stephane/Data13TB/stephane -maxdepth 3 -iname \"*udhr*\" -type d 2>/dev/null | head -10; echo \"=== counts ===\"; ls /home/stephane/Data13TB/stephane/udhr_xml 2>/dev/null | wc -l; ls /home/stephane/Data13TB/stephan … [300 caractères tronqués]`

  ```
/home/stephane/Data13TB/stephane/corpus/udhr
/home/stephane/Data13TB/stephane/corpus/udhr/udhr_xml
/home/stephane/Data13TB/stephane/corpus/udhr/udhr392
/home/stephane/Data13TB/stephane/corpus/udhr/udhr392_c8
=== counts ===
0
399
399
399
399
  ```

### 🤖 Assistant

⏵ Mesure des bases UDHR XML et Gutenberg.

- **bash** `{"command": "du -sh /home/stephane/Data13TB/stephane/corpus/udhr/udhr_xml /home/stephane/Data13TB/stephane/corpus/udhr/udhr392 /home/stephane/Data13TB/stephane/corpus/udhr/udhr392_c8 2>/dev/null; ls /home/stephane/Data13TB/stephane/corpus/udhr/udhr_xml | wc -l; echo \"=== gutenberg db ===\"; find /h … [352 caractères tronqués]`

  ```
9,8M	/home/stephane/Data13TB/stephane/corpus/udhr/udhr_xml
2,7G	/home/stephane/Data13TB/stephane/corpus/udhr/udhr392
4,0G	/home/stephane/Data13TB/stephane/corpus/udhr/udhr392_c8
459
=== gutenberg db ===
=== parallele_rj ===
en_01.drvf
en_02.drvf
en_03.drvf
en_04.drvf
en_05.drvf
48
  ```

### 🤖 Assistant

⏵ Derniers comptages de corpus et état des sous-agents.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/corpus && ls parallele_crime | wc -l; ls wiki_apparie | wc -l; ls wiki_traces | wc -l; ls wiki_apparie | sed 's/_.*//' | sort | uniq -c; echo \"=== drvf total ===\"; find /home/stephane/Data13TB/stephane/corpus -name \"*.drvf\" | wc -l; echo \"=== gut … [183 caractères tronqués]`

  ```
49
2894
480
    482 de
    482 en
    482 es
    482 fr
    482 it
    482 pt
      2 traces
=== drvf total ===
5972
=== gutenberg plus large ===
/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_en.db
/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_fr.db
/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_de.db
/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_es.db
/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_en.db-wal
/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_en.db-shm
/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_fr.db-wal
/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_fr.db-shm
  ```

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_{en,fr,de,es}.db 2>/dev/null | awk '{printf \"%s %.1f Mo\\n\",$9,$5/1048576}'; du -sh /home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion 2>/dev/null", "descripti … [32 caractères tronqués]`

  ```
/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_de.db 9.4 Mo
/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_en.db 21.1 Mo
/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_es.db 11.2 Mo
/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_fr.db 6.7 Mo
1,3G	/home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion
  ```

### 🤖 Assistant

⏵ Lecture des sections « plafond/transfert » du récapitulatif.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/recapitulatif.md", "limit": 180, "offset": 523}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/recapitulatif.md</path>
<type>file</type>
<content>
523: 
524: Le plafond de +0,024 pouvait venir du réservoir (gelé, aléatoire) ou d'ailleurs.
525: Quatre expériences, quatre réponses.
526: 
527: ### 10.1 Le réservoir n'est pas le goulot
528: 
529: Le **gain d'entrée** — *le* réglage critique du calcul réservoir, à 1,0 depuis le
530: début sans avoir jamais été balayé — et le **seuil par neurone** :
531: 
532: | gain | seuil | fid TEST | écart | invariance | pire paire |
533: |---|---:|---:|---:|---:|---:|
534: | 0,3 | non | 0,6381 | +0,0241 | 0,9672 | 0,8909 |
535: | 0,3 | oui | 0,6352 | +0,0212 | 0,9655 | **0,9063** |
536: | 1,0 | non | **0,6383** | **+0,0243** | 0,9648 | 0,8821 |
537: | 1,0 | oui | 0,6364 | +0,0224 | 0,9625 | 0,9038 |
538: | 3,0 | non | 0,6355 | +0,0215 | **0,9680** | **0,9074** |
539: 
540: **Tout tient dans 0,003 de fidélité.** Ces deux leviers ne sont pas le goulot. Le
541: seuil, lui, **échange** de la fidélité contre la pire paire — la loi d'échange
542: encore une fois.
543: 
544: ### 10.2 L'expérience décisive : un readout ORACLE
545: 
546: On ajuste la lecture **sur le test lui-même** et on l
… [7603 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture directe de pont_reservoir.py et pont_fidele.py pour l'architecture.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pont_reservoir.py"}`

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

- **list_agents** `{}`

  ```
a4277668-3825-4797-bf0b-d7addcbb569d [ready] — Inventaire corpus dépôt
ee19a880-cc76-4c5c-9fe0-5972bd73b533 [running] — Inventaire poids et entraînements
  ```

### 👤 Utilisateur

Agent a4277668-3825-4797-bf0b-d7addcbb569d sent a message:
RAPPORT CORPUS (mission lecture seule, aucune écriture) — dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet
Convention : [VU]=mesuré sur disque, [REF]=référencé/attendu par un script. Tailles du 8 oct.

A. SCRIPTS PRODUCTEURS DE TEXTE (tools/)
1. /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/extrait_udhr.py — [VU] src = dossier UDHR XML (ns unhchr, udhr_*.xml, 456 langues) ; sortie JSONL, 1 ligne/unité (preambule-NN, article-N-PP) portant les traductions de TOUTES les langues ; args positionnels <dossier_xml> <sortie.jsonl>, --min-langues 50 ; aucun défaut.
2. tools/extrait_article1.py — [VU] importe lire() de extrait_udhr ; défauts : dossier=/home/stephane/Data13TB/stephane/corpus/udhr/udhr_xml, sortie=/home/stephane/Data13TB/stephane/corpus/udhr/article{art}, --article 1 ; 1 .txt par code iso639-3 (456 XML → 399 fichiers : collisions de codes + langues sans article).
3. tools/extrait_wikipedia.py — [VU] src EN DUR /home/stephane/Data13TB/stephane/nipada/wikipedia_decompressed/<lg>/*.json ; sortie défaut /tmp/wiki_{lg}.jsonl (1 JSON/article, clés titre/texte) ; défauts --articles 200 --min 800 --max 6000.
4. tools/extrait_gutenberg.py — [VU] src SQLite --db table backlog(title,raw_text) ; sortie <sortie.txt>, 1 segment/ligne (découpe regex --motif, filtre LIKE --titre) ; pas de chemin par défaut.
5. tools/extrait_crime.py — [VU] src EN DUR /home/stephane/Data13TB/stephane/GitHub/Panini-Research/data/mass_ingestion/backlog_gutenberg_{en,es}.db (lecture seule) ; sortie <dir>/{en,es}_NN.txt ; défauts --max-car 26000 --min-car 4000 ; alignement par index de chapitre.
6. tools/wiki_apparie.py — [VU] src EN DUR /home/stephane/Data13TB/stephane/data/wikipedia/db/{en,fr,de,es,it,pt}wiki_v14.db (table articles(title,title_lower,summary)) ; sortie <dir>/{L}_{slug}.txt ; défauts --n 3000 --langues en,fr,de,es,it,pt ; appariement par titre identique.
7. tools/decoupe_langues.py — [VU] src = dossier de .txt ; classifie l'écriture par blocs Unicode ; sortie EN DUR /tmp/decoupe392.json ; défauts --test 20 --val 40 --graine 5.
8. tools/corpus_neuf.py — [VU] ne produit pas de texte : consomme un cache .npz (Wikipedia non aligné vs UDHR aligné).
9. tools/ingestion*.py : AUCUN. Seul tools/telecharger_modeles.py (modèles, pas corpus).

B. CORPUS TEXTE VUS SUR DISQUE (mesuré)
10. [VU] /home/stephane/Data13TB/stephane/corpus/udhr/udhr_xml — 9,8 Mo — 459 fichiers dont 456 udhr_*.xml (source UDHR) + index/schemas — producteur : téléchargement amont (udhr.zip) — 5 oct 09:07.
11. [VU] .../corpus/udhr/unites.jsonl — 5 470 507 o, 42 lignes (unités ≥50 langues) — extrait_udhr.py — 5 oct 09:18.
12. [VU] .../corpus/udhr/article1 — 1,6 Mo, 399 .txt (1 phrase/langue, 92 124 car.) — extrait_article1.py — 7 oct 17:52 ; article2 idem 399 .txt, 271 958 car., 7 oct 18:16.
13. [VU] .../corpus/udhr/langues (30 fichiers = 10 langues × txt/ids/drvf, 71 Mo), langues_train (8), langues_adapt (10), langues30b (10), vaste (120 = 40 langues, 378 Mo), vaste_train/test (20 chacun) — extraits UDHR multi-langues pour le panel stratifié.
14. [VU] .../corpus/udhr/udhr392 (392 .drvf, 2,7 Go, 6 oct) et udhr392_c8 (392 .drvf, 4,0 Go, 6 oct) — traces d'activations, pas du texte ; source texte intermédiaire [VU] /tmp/udhr10_toutes (392 .txt, 1,9 Mo).
15. [VU] .../corpus/udhr/unites (400 .drvf, 491 Mo, 6 oct) — traces par unité alignée ; source [VU] /tmp/unites_texte (400 .txt) depuis unites.jsonl.
16. [VU] .../corpus/udhr/article1_traces (399 .drvf, 2,1 Go) et article2_traces (399 .drvf, 4,7 Go) — traces couches 0..23.
17. [VU] .../corpus/parallele_crime — 261 Mo — 24 en_NN.txt + 24 es_NN.txt (1 183 204 car.) + traces/ (8 .drvf seulement, 260 Mo) — extrait_crime.py puis /tmp/trace_crime.sh — 6 oct 14:51/15:26.
18. [VU] .../corpus/parallele_rj — 988 Mo — 48 .drvf (24 en + 24 fr, 1 Go) ; AUCUN .txt source dans ce dossier : les textes sont [VU] /tmp/parallele/en.txt (140 382 o) et fr.txt (212 826 o) — extrait_gutenberg.py puis /tmp/trace_rj.sh — 5-6 oct.
19. [VU] .../corpus/wiki_apparie — 12 Go — 2 892 .txt = 482 titres × 6 langues (en,fr,de,es,it,pt ; 5 755 428 car.) + traces/ 2 892 .drvf (7,8 Go) — wiki_apparie.py puis /tmp/trace_wiki_apparie.sh — 7 oct 09:13.
20. [VU] .../corpus/wiki_traces — 1,8 Go — 480 .drvf (240 en + 240 fr) — Wikipedia NON apparié — extrait_wikipedia.py + /tmp/trace_wiki.sh (morceaux 3 000 car.) — 6 oct 06:47.
21. [VU] .../corpus/udhr/appr10 (2,1 Go, 40 drvf), appr10c, appr40, appr, tenus10 (292 Mo), tenus*, vaste* — sous-corpus d'entraînement/test dérivés de l'UDHR. Total corpus = 35 Go, 3 804 .txt, 5 972 .drvf.
22. [VU] /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/wikitext2_test.txt — 359 041 o, 1 995 lignes (WikiText-2 anglais) + .ids 398 564 o + wt2.json 30 005 o — utilisé par tools/aiguille.py, tools/portes.sh, tools/porte-flux.sh, run_harness.py.
23. Sources amont [VU] : .../stephane/data/wikipedia/db/*wiki_v14.db — 132 Go, 10 bases (ar,de,en,es,fr,it,ja,pt,ru,zh), 26-28 mai ; .../stephane/nipada/wikipedia_decompressed — 81 Go, chunks JSON pour de(14G),en(34G),es(8,2G),fr(11G),it(2,4G),ru(13G) ; Panini-Research/data/mass_ingestion — backlog_gutenberg_{en,fr,de,es}.db (22/7/11,7/9,8 Mo) + full_texts 1,2 Go/2 269 fichiers.
24. /home/stephane/corpus n'existe PAS (le corpus est sous .../Data13TB/stephane/corpus) ; ~/.cache/huggingface ne contient aucun dataset texte de corpus.

C. BINAIRES DE CORPUS (.npz / traces = activations, pas du texte)
25. [VU] /tmp/cache_rj_{en,fr}.npz (83,9 / 139,7 Mo) et cache_rj8_* — Romeo couche 10 ; /tmp/cache_wiki_{en,fr,de,es,it,pt}.npz (73,8–94,2 Mo) — wiki_apparie ; /tmp/cache_wikit{rain,est}.npz (311/324 Mo) — Wikipedia non aligné.
26. [VU] /tmp/cache392{,_c8}_{train,test}.npz (0,15–0,99 Go), cache_unites*_*.npz, cache_6l{,_train,_test}.npz (0,18–0,53 Go), cache_vf_{train,test}.npz (1,75/1,83 Go, 7 oct 05:21-05:52).
27. [VU] /tmp/pcs_a1.{moyenne,derniere}.npz (26,8/11,6 Mo) et pcs_a2.* (29,7/11,6 Mo), 7 oct 19:02-19:33 — directions/discriminants article1 vs article2 ; /tmp/p_*.npz (p_1…p_128), /tmp/pont_semantique*.npz.
28. [VU] .../corpus/udhr/pont_semantique.npz (1 382 064 o) et pont_semantique_r1.npz (16 560 o), 5 oct — ponts sémantiques.

D. RÉFÉRENCÉ MAIS ABSENT / INCOMPLET (déduit)
29. [REF][ABSENT] /tmp/wiki_{de,es,it,pt}.jsonl : extrait_wikipedia.py ne les a produits que pour en et fr (en 1 590 928 o, fr 1 620 100 o [VU]).
30. [REF][ABSENT] dumps nipada wikipedia_decompressed/{ar,ja,pt,zh} : absents (seuls de,en,es,fr,it,ru) — n'affecte pas wiki_apparie.py qui lit les .db de data/wikipedia/db.
31. [REF][ABSENT] .../corpus/udhr/udhr_xml.zip et udhr_txt.zip : 196 o, ce sont des pages HTML « 404 Not Found » (téléchargements ratés) ; udhr.zip (2 237 381 o) est un JAR valide.
32. [REF][INCOMPLET] parallele_crime/traces : 8 .drvf sur 48 attendus (en_01..04, es_01..04) — traçage interrompu ; parallele_rj n'a pas de .txt source conservé dans le corpus.
33. [REF][ABSENT] .../corpus/udhr/appr42, tenus42, tenus10c, appr10c : dossiers vides ou partiels (appr42 et tenus42 = 0 fichier) malgré les scripts /tmp correspondants.
34. [REF][DÉDUIT] extrait_article1.py annonce 456 langues ; 399 fichiers seulement (57 codes en collision/écrasés ou sans article 1) — documenté dans le script lui-même.
35. [INFO] Aucun script du dépôt ne référence en dur parallele_rj, parallele_crime, wiki_apparie ou wiki_traces : les producteurs de traces sont des scripts /tmp/*.sh (trace_rj.sh, trace_crime.sh, trace_wiki_apparie.sh, trace_wiki.sh, trace392.sh, trace_article1.sh, trace_unites.sh), non versionnés.

SYNTHÈSE : 6 corpus texte réellement présents (UDHR XML + unites.jsonl + article1/2, Romeo /tmp, Crime en-es, wiki_apparie 482×6, Wikipedia en/fr non apparié, WikiText-2) ; tout le reste sur disque est binaire (traces .drvf 5 972 fichiers, caches .npz ~40) ; les manques réels sont les zips UDHR 404, le traçage Crime incomplet (8/48) et les jsonl Wikipedia hors en/fr.

### 👤 Utilisateur

Background subagent a4277668-3825-4797-bf0b-d7addcbb569d finished and will do no further work unless you send it more.
Its closing message:
Rapport envoyé au parent. Synthèse de l'inventaire (mission strictement en lecture, aucune écriture) :

**Scripts producteurs (tools/)** — 8 identifiés : `extrait_udhr.py` (XML UDHR → JSONL multi-langues), `extrait_article1.py` (1 .txt/langue), `extrait_wikipedia.py` (chunks nipadia → `/tmp/wiki_{lg}.jsonl`), `extrait_gutenberg.py` (SQLite backlog → segments), `extrait_crime.py` (Panini Gutenberg en/es → 24 chapitres appariés), `wiki_apparie.py` (bases Wikipedia → 482 titres × 6 langues), `decoupe_langues.py` (panel stratifié par écriture → `/tmp/decoupe392.json`), `corpus_neuf.py` (consommateur de cache). **Aucun `ingestion*.py`** dans le dépôt.

**Vu sur disque** : 35 Go sous `/home/stephane/Data13TB/stephane/corpus` (3 804 .txt, 5 972 .drvf) — UDHR XML (456 langues), `unites.jsonl`, article1/2, udhr392, unites ; `parallele_rj` (48 drvf, sources dans `/tmp/parallele/`), `parallele_crime` (48 txt + 8 drvf), `wiki_apparie` (2 892 txt + 2 892 drvf, 12 Go), `wiki_traces` (480 drvf) ; plus WikiText-2 dans `data/` et les sources amont (132 Go de bases Wikipedia, 81 Go de chunks nipadia, 1,8 Go de bases Panini).

**Binaires** : ~40 caches `.npz` d'activations dans `/tmp` (rj, wiki, 392, 6l, vf, pcs_a1/a2) et les 5 972 traces `.drvf`.

**Absent/incomplet** : `wiki_{de,es,it,pt}.jsonl`, dumps nipadia ar/ja/pt/zh, `udhr_xml.zip`/`udhr_txt.zip` (pages 404 de 196 o), traçage Crime limité à 8/48, dossiers `appr42`/`tenus42` vides, et 399 fichiers sur 456 langues annoncées.

### 🤖 Assistant

⏵ Lecture de pont_fidele.py pendant la fin de l'inventaire des entraînements.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,45p' tools/pont_fidele.py; echo \"=== RECURRENT ===\"; sed -n '1,35p' tools/pont_recurrent.py", "description": "Read headers of pont_fidele and pont_recurrent"}`

  ```
#!/usr/bin/env python3
"""pont_fidele.py — émuler le professeur LE PLUS FIDÈLEMENT POSSIBLE, à moindre coût.

Correction d'une faute de mesure : `pont_recurrent.py` comparait la fidélité DANS
LE SOUS-ESPACE du rang courant. Comparer un rang 1 et un rang 64 ainsi revient à
comparer deux espaces différents — les chiffres ne sont pas comparables, et c'est
ce qui faisait « baisser » la fidélité quand on ajoutait des neurones.

Ici tout est mesuré **dans l'espace complet de 896 canaux**, contre la sortie
réelle du professeur. Les modèles sont comparés à coût égal et à coût libre :

  - LINÉAIRE de rang r        : y = (e·U)·Vᵀ + moy            (r neurones)
  - DEUX COUCHES (ELM)        : y = tanh(e·R)·W              (H neurones cachés)
    R est ALÉATOIRE et GELÉ ; seul W s'ajuste, par moindres carrés — aucune
    rétropropagation, et R n'a pas besoin d'être distribué de la même façon que W.

Usage : pont_fidele.py <dossier_train> <dossier_test> [--couche 10]
"""
import glob, os, struct, sys
import numpy as np


def lire(chemin):
    def paires(f, n, version, bloc=32):
        ech = None
        if version == 3:
            nb, = struct.unpack("<I", f.read(4))
            ech = [struct.u
… [2098 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des en-têtes des outils « directions/discriminants ».

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in tools/discriminant_transfert.py tools/stabilite_directions.py tools/energie_du_contenu.py tools/ancre_professeur.py; do echo \"##### $f\"; sed -n '1,32p' \"$f\"; echo; done", "description": "Read headers of direction tools"}`

  ```
##### tools/discriminant_transfert.py
#!/usr/bin/env python3
"""discriminant_transfert.py — les directions apprises sur un panel servent-elles sur un autre ?

LA QUESTION, ET ELLE EST NEUVE. Le §80 a mesuré qu'un discriminant linéaire appris portait
le rapport contenu/langue à **105 % du professeur**. Mais ce résultat a été obtenu SUR LE
PANEL ROMAN (es/it/pt) et mesuré SUR CE MÊME PANEL. Or le §83 vient d'établir que le
professeur lui-même vaut 12,001 sur ce panel et **1,494 sur sa pire paire (de–en)**.

Un projecteur appris à séparer l'espagnol, l'italien et le portugais sait-il séparer
l'allemand de l'anglais ? Rien ne l'assure : le discriminant maximise `C_cont/C_lang`, et
`C_lang` est estimé sur LES LANGUES DU PANEL D'APPRENTISSAGE. Si l'axe de langue appris est
« l'axe roman », il peut être orthogonal à « l'axe germanique ».

CE QUI EST MESURÉ. Trois caches, quatre cas. Le pont est appris sur `--appr` ; le
discriminant sur `--disc` ; la mesure sur `--eval`. Les cas se lisent deux à deux :
dans-panel contre transfert, dans les deux sens.

    appris      discriminant   évalué        ce que ça dit
    de/en/fr    es/it/pt       es/it/pt      le §80 (référence, dans-panel)
    d
… [6150 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Attente du second inventaire (entraînements/poids) avant rédaction.

- **list_agents** `{}`

  ```
a4277668-3825-4797-bf0b-d7addcbb569d [ready] — Inventaire corpus dépôt
ee19a880-cc76-4c5c-9fe0-5972bd73b533 [running] — Inventaire poids et entraînements
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,30p' tools/plateau_multilingue.py; echo \"=== invariance_semantique ===\"; sed -n '1,22p' tools/invariance_semantique.py; echo \"=== cancellation_langue ===\"; sed -n '1,25p' tools/cancellation_langue.py", "description": "R … [41 caractères tronqués]`

  ```
#!/usr/bin/env python3
"""plateau_multilingue.py — à quelle profondeur les langues se rejoignent-elles ?

Étend `invariance_semantique.py` d'une paire à N langues : pour chaque couche, la
similarité cosinus MOYENNE de toutes les paires de langues, sur la dernière
position (la représentation de l'énoncé entier).

Ce que ça mesure, et pourquoi c'est la base de toute émulation sémantique : un
modèle qui « répond la même chose » dans dix langues doit avoir, quelque part,
une représentation qui ne dépend plus de la langue. La couche où la similarité
est maximale est cette couche-là — et c'est là qu'un adaptateur a un sens.

Usage : plateau_multilingue.py <dossier de traces .drvf> [--base 0]
"""
import glob
import os
import struct
import sys
from itertools import combinations


def lire(chemin):
    def paires(f, n, version, bloc=32):
        ech = None
        if version == 3:
            nb, = struct.unpack("<I", f.read(4))
            ech = [struct.unpack("<e", f.read(2))[0] for _ in range(nb)]
        out, prev = [], 0
        for _ in range(n):
            if version == 1:
=== invariance_semantique ===
#!/usr/bin/env python3
"""invariance_semantique.py — à quelle profondeur la repré
… [2051 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des « résultats marquants » de la session principale.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md", "limit": 125, "offset": 10851}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md</path>
<type>file</type>
<content>
10851: ## 4. Mesures et résultats marquants
10852: 
10853: - **T1** `// scalaire dense (pull). Le croisement mesuré est à 10 %.`
10854: - **T1** `part de l'attention dans le flux d'événements : 100.0 %`
10855: - **T1** `255 tokens notés — perplexité cumulée 17.431  (31.9 tok/s)`
10856: - **T1** `510 tokens notés — perplexité cumulée 19.388  (31.8 tok/s)`
10857: - **T1** `=== perplexité 19.3885 sur 510 tokens (0 événements, 16.1 s) ===`
10858: - **T1** `0  1.00000000e+00  1.00000000e+00    0.000 %`
10859: - **T1** `1  6.89044306e-01  6.89044306e-01    0.000 %`
10860: - **T1** `2  4.74782055e-01  4.74782055e-01    0.000 %`
10861: - **T1** `3  3.27145872e-01  3.27145872e-01    0.000 %`
10862: - **T1** `4  2.25418000e-01  2.25418000e-01    0.000 %`
10863: - **T1** `5  1.55322989e-01  1.55322989e-01    0.000 %`
10864: - **T1** `6  1.07024421e-01  1.07024421e-01    0.000 %`
10865: - **T1** `7  7.37445682e-02  7.37445682e-02    0.000 %`
10866: - **T1** `8  5.08132748e-02  5.08132748e-02    0.000 %`
10867: - **T1** `9  3.17056962e-02  3.1
… [8836 caractères tronqués]
  ```

- **list_agents** `{}`

  ```
a4277668-3825-4797-bf0b-d7addcbb569d [ready] — Inventaire corpus dépôt
ee19a880-cc76-4c5c-9fe0-5972bd73b533 [running] — Inventaire poids et entraînements
  ```

### 🤖 Assistant

⏵ Inventaire personnel des boucles d'optimisation dans tools/.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -ln \"np.linalg.solve\\|np.linalg.lstsq\\|torch.optim\\|Ridge(\\|LinearRegression\\|\\.fit(\\|eigvals\\|svd(\" tools/*.py | tr '\\n' ' '; echo; echo \"=== ridge/moindres carrés ===\"; grep -c \"solve(\" tools/*.py 2>/dev/null |  … [86 caractères tronqués]`

  ```
tools/blanchiment_entree.py tools/controle_capacite.py tools/corpus_neuf.py tools/discriminant_contenu.py tools/discriminant_transfert.py tools/energie_du_contenu.py tools/essai_decharge.py tools/etats_sans_langue.py tools/grand_et_entree.py tools/lecture_locale.py tools/leviers_pont.py tools/localite_couches.py tools/ou_entre_la_langue.py tools/ou_est_le_contenu.py tools/pont_fidele.py tools/pont_generatif.py tools/pont_parallele.py tools/pont_recurrent.py tools/pont_reglages.py tools/pont_reservoir.py tools/pont_unites.py tools/profil_couches.py tools/profil_langues.py tools/renforcement_directions.py tools/sonde_pont.py tools/sous_espace_du_contenu.py tools/stabilite_directions.py tools/stabilite_evenements.py tools/transfert_ridge.py 
=== ridge/moindres carrés ===
tools/archive_sessions.py:2 tools/blanchiment_entree.py:1 tools/controle_capacite.py:1 tools/corpus_neuf.py:1 tools/discriminant_contenu.py:1 tools/discriminant_transfert.py:1 tools/energie_du_contenu.py:1 tools/etats_sans_langue.py:1 tools/grand_et_entree.py:1 tools/lecture_locale.py:1 tools/leviers_pont.py:1 tools/localite_couches.py:3 tools/ou_entre_la_langue.py:1 tools/ou_est_le_contenu.py:2 tools/pont_fidele.py:2
… [320 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"import torch\\|from torch\" tools/ *.py src/ 2>/dev/null | head; echo \"(vide = aucun torch)\"; grep -rln \"backward()\\|optimizer\" tools/ 2>/dev/null | head; echo \"(vide = aucune rétroprop)\"", "description": "Confirm  … [22 caractères tronqués]`

  ```
tools/trace_gpu.py
tools/essai_decharge.py
(vide = aucun torch)
tools/essai_decharge.py
(vide = aucune rétroprop)
  ```

### 🤖 Assistant

⏵ Vérification des deux scripts utilisant torch.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"### essai_decharge.py\"; head -30 tools/essai_decharge.py; echo; echo \"### torch usage\"; grep -n \"torch\" tools/essai_decharge.py | head -20; echo; echo \"### trace_gpu.py\"; head -18 tools/trace_gpu.py; grep -n \"torch\" t … [76 caractères tronqués]`

  ```
### essai_decharge.py
#!/usr/bin/env python3
"""essai_decharge.py — la parcimonie ENTRAÎNÉE, mesurée contre un jumeau dense.

POURQUOI CE BANC. Le dépôt a mesuré deux choses qui se tiennent par la main :

  * un LLM dense n'a JAMAIS d'activation exactement nulle (**0,00 % de zéros**) :
    le débit est donc constant, et « on ne paie que ce qui s'active » reste une
    promesse théorique (`reports/rapport-parcimonie-imposee.md`) ;
  * imposer la parcimonie APRÈS l'entraînement plafonne à **−15 % d'événements
    pour +0,6 à +1,2 % de perplexité** — et le seuil absolu est pire encore
    (`reports/rapport-campagne-parcimonie.md`).

La conclusion était déjà écrite dans `docs/programme-recherche.md` §2 ter :
**« la parcimonie ne s'impose pas, elle s'entraîne »**. Ce script est le premier
essai de cette phrase — un modèle dont les activations sont discrètes **par
construction** (Heaviside après normalisation par lot), entraîné au **gradient de
substitution**, contre un jumeau **dense** de mêmes paramètres et de même budget.

CE QUI EST MESURÉ, ET POURQUOI CES GRANDEURS

  * **bits/caractère** sur une validation tenue à l'écart — la qualité ;
  * **R̂**, la fraction d'unités actives, sit
… [3285 caractères tronqués]
  ```

### 👤 Utilisateur

Agent ee19a880-cc76-4c5c-9fe0-5972bd73b533 sent a message:
INVENTAIRE ENTRAÎNEMENT/POIDS — Qtrinet (mission lecture seule ; aucun fichier écrit, aucun script exécuté). Tout est MESURÉ (code lu + ls/unzip/md5) sauf mention « supposé ».

== A. LE SEUL POIDS ENTRAÎNÉ ET PERSISTÉ DU PROJET ==
· /home/stephane/Data13TB/stephane/pont_semantique.npz — 1 382 064 o, 05/10 10:45, md5 325a5583… ; copie byte-identique /home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique.npz (10:47). Écrit par tools/pont_recurrent.py L191-193 (`DRAVE_PONT_SORTIE`, défaut ./pont_semantique.npz). Contenu (en-têtes npy vérifiés) : P f4 (896,128), moy f4 (896,), W0 f8 (896,128), couche, rang, langues_train/test. Lu par tools/applique_pont.py L58 (`abstrait=(e·W0)·Pᵀ+moy`) et tools/sonde_pont.py L85.
· /home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz — 16 560 o, 05/10 11:02 : P f4 (896,1), W0 f8 (896,1), moy f4 (896). Version rang-1 (rang contenu dans le fichier) ; « produit par --rang 1 » = supposé (le défaut du script est 64).
· AUCUN .pt/.pth/.safetensors/.pkl/.ckpt/.bin de poids dans le dépôt (find = 0) ; models/ = 2 GGUF téléchargés (Qwen2.5-0.5B Q4_0 353 Mo, Q8_0 531 Mo) → inférence seule.

== B. PONT (point 3) — tous ajustent la LECTURE en forme fermée, sans rétropropagation ==
Base : cible = couche 10 du professeur (896 canaux) ; entrée = plongée couche 0 (T,896).
· tools/pont_recurrent.py — 2 régressions crête : (1) récurrence s_t=A·s_{t−1}+B·e_t dans un sous-espace de rang r (SVD de Y, défaut r=64) ; (2) témoin W0 : y=(e_t·W0)·Pᵀ+moy. Loss ‖XW−Y‖²+λ‖W‖², λ=1e-2·n ; np.linalg.solve, AUCUNE itération ; rayon spectral de A ramené à 0,95. ÉCRIT pont_semantique.npz (ci-dessus).
· tools/pont_generatif.py (moteur principal, 1041 l.) — réseau récurrent qui CROÎT puis subit une ATTRITION. Neurone : s=(1−a)s+a·tanh(W_par·x_{c−1}+W_self·s+B·e_t), a=0,2 (ou 120 constantes log-étalées a∈[0,02;0,8]), B/W_self ALÉATOIRES GELÉS (graine 5) ; seule la lecture W s'ajuste : W=solve(XᵀX+ride·n·I, Xᵀ(Y−mt)), ride=0,3 ; lecture quadratique optionnelle φ=[X,X²] (240 col.). Objectif enrichi : ‖XW−Y‖² + μ_lang·P_lang − μ_cont·P_cont. Défauts : 3 cycles × 3 couches, naissance 1,1,2,4… (cycle 1) puis +n/4, plafond 256 neurones, patience 12, seuil d'attrition 0,02 (retrait de 25 % des neurones par redondance 1−1/((G⁻¹)_jj·G_jj) ou contribution), retour au meilleur passage ; `renforce()` local η=0,6. N'ÉCRIT AUCUN poids (résultat imprimé seulement).
· tools/pont_reservoir.py — réservoir N=256 gelé (A rayon 0,9 ; B~N(0,1/√896)), fuite a=0,2, seule W s'ajuste (solve, ride 3e-1). Aucune écriture.
· tools/pont_fidele.py — familles comparées : linéaire rang 1→128 et ELM tanh(E·R) avec R gelé H∈{64,256,1024,4096}, W par solve (ride 1e-2 / 1e-1). Aucune écriture.
· tools/pont_unites.py — croissance par `Pont.nait` jusqu'à 120 neurones (patience 8, gain_min 5e-4) ; W ridge ride=1,0. Aucune écriture.
· tools/pont_parallele.py — Pont 1 couche, a=0,5, ride=1,0, graine 5 (corpus apparié). Aucune écriture.
· tools/pont_reglages.py — balayage fuite/rayon/neurones/ensemble/saut ; W ridge. Aucune écriture.
· tools/leviers_pont.py — 4 variantes : A 40 neurones 1 couche quadratique ; B + entrée directe ; C entrée seule ; D 20+20 ; a=0,2, ride=0,3, graine 5. Aucune écriture.
· tools/objectif_du_pont.py — balayage (μ_lang, μ_cont), solve fermé. Aucune écriture.
· tools/cache_pont.py — PAS d'apprentissage : écrit les caches d'activations np.savez_compressed(cles, hidden, E_i couche 0, Y_i couche c) → /tmp/cache*.npz.
· tools/applique_pont.py, sonde_pont.py (sonde ridge λ=1e-2 prédisant la plongée t+1), compare_professeurs.py, ancre_professeur.py — mesure/inférence (seul sonde_pont ajuste une sonde, non persistée).
· tools/rapport_du_pont.py — réentraîne la référence éphémère : 120 neurones, lecture quadratique, ride 0,03, graine 5.
· tools/pont_fidele/pont_reglages/leviers/objectif = apprentissages NON persistés (RAM).

== C. DIRECTIONS/DISCRIMINANTS (point 4) — communes : Pont 1 couche 120 neurones (quadratique 240 col.), 896 canaux, W=solve(XᵀX+ride·n·I, Xᵀ(Y−mt)), ride 0,03, graine 5, AUCUNE écriture ==
· discriminant_contenu.py / discriminant_transfert.py / stabilite_directions.py — LDA de Fisher : eigh(solve(C_lang+λI, C_cont)), λ=1e-2·tr(C_lang)/ncan, rangs 2/5/10/20/40 ; stabilite = 6 ponts réentraînés (graines 5→10) et angles principaux.
· renforcement.py — renforcement/atrophie local : cap_j=|corr(act_j, résidu)|, f=1+η(2cap−1), η∈{0,02;0,1}, passes=8.
· renforcement_directions.py — apprend les POIDS D'ENTRÉE : G=Eᵀ·R, SVD(G), b_j←U[:,j%k]·‖b_j‖ (Hebb local), mélange=1,0, passes=5, ride 0,03.
· energie_du_contenu.py (4 variantes convexes, alphas 0,25→1) ; transfert_ridge.py (balayage ride 0,03→30, 40 neurones) ; blanchiment_entree.py (blanchiment covariance par langue + readout direct [E,E²] 1792 col.) ; sous_espace_du_contenu.py (SVD des offsets de contenu, projecteur Π 896×896, gammas 1→5) ; covariance_cible.py (A=CY^½·CO^−½ par eigh) ; decomposition.py et amplification.py = MESURES pures ; calibre_modes.py = AUCUN apprentissage (lance 2× par langue le binaire drave-core/target/release/drave, écrit /tmp/calibre/*.drvf : 16 fichiers, 58 Mo).

== D. HORS tools/ (point 2) ==
· /home/stephane/Data13TB/stephane/GitHub/Qtrinet/src/tiny_model.py — SEUL apprentissage hors tools : MLP 32→64→10 (ReLU+softmax), corpus SYNTHÉTIQUE (gaussiennes 32 d, 10 classes), professeur = MLP aléatoire FIGÉ (teacher_seed 1234) = vrai teacher ; loss cross-entropy, gradient manuel, SGD lr=0,05 batch=128 epochs=300 ; masques = prune→retrain. AUCUN poids écrit. Appelé par run_quantify.py (300 ép.), run_clusters.py (400), run_sparsity.py (400), run_precision.py (retrain 150, lr 0,02), run_encoding.py (retrain 150).
· run_real_clusters.py : k-means maison (30 itérations, seed 0) sur les experts d'un GGUF = ajustement non supervisé de centroïdes, sortie = liste texte, pas de poids.
· tools/mla_synthetique.py, mhc_v41_synthetique.py, v41_*.py : poids ALÉATOIRES aux bonnes formes écrits en GGUF (/tmp/mla_minuscule.gguf, 480 448 o, 02/10) pour tester le moteur — PAS entraînés.
· Aucun torch/Adam/backward/lbfgs dans le dépôt (trace_gpu.py et mhc_v41_synthetique.py ne font que comparer un noyau vLLM) ; drave-core/ (Rust) = inférence.

== E. FICHIERS TROUVÉS (point 1) ==
· Dépôt : 0 fichier de poids.
· Voisins : /tmp/cache*.npz = 41 fichiers, 9,5 Go (activations E/Y, écrits par cache_pont.py ; ex. /tmp/cache_vf_train.npz 1 747 348 718 o 07/10 05:21 ; /tmp/cache392_train.npz 985 580 685 o). /tmp/drave* = 11 573 fichiers, 557 Mo : DUMPS D'ACTIVATIONS/ÉTATS (q_rope, qr_norm, attn_brut, comp, l, hc, idx) produits par l'outillage de traçage — PAS des poids. /tmp/calibre/ = 16 .drvf (58 Mo).
· /home/stephane/Data13TB/stephane/ (maxdepth 4) : hors pont_semantique*, rien de ML (model.pkl trombinoscope, dump_state.bin llama.cpp). ~/.cache/drave* : inexistant.

== F. PROFESSEUR / DISTILLATION / CALIBRATION (point 5) ==
· « Professeur » = Qwen2.5-0.5B (GGUF), JAMAIS entraîné ici : lu en boîte noire (couche 0 → couche 10, 896 canaux) ; hidden=896 cohérent avec Qwen2.5-0.5B (supposé).
· Aucune distillation entraînée : seule mention tools/approximabilite_bloc.py L5 (« question préalable à toute distillation ») et reports/rapport-morcellement-experts.md (projet non réalisé).
· « Calibration » = mesure : calibre_modes.py (dense vs événementiel) et trace_gpu.py --calibrer (cosinus), aucun paramètre appris.
· CONCLUSION : tout apprentissage « modèle » est ÉPHÉMÈRE (RAM) sauf le pont rang-128/rang-1 (3 .npz, ~1,4 Mo) ; 4 mécanismes d'ajustement non-gradient : ridge forme fermée, croissance+attrition, renforcement/atrophie local, SVD/Hebb des directions — plus le MLP synthétique SGD de src/tiny_model.py.

### 🤖 Assistant

⏵ Rédaction du rapport final (150 lignes max) et envoi au parent.

Les deux inventaires sont revenus. Je rédige le rapport consolidé.

- **send_message** `{"agent_id": "d31b3d9b-58e4-4d34-85fa-381b6f6a6a76", "message": "RAPPORT — INVENTAIRE DU TRAVAIL « CÔTÉ MODÈLE » DE QTRINET/DRAVE\n(Lecture seule : aucun fichier modifié, aucun entraînement lancé. [M]=mesuré dans un rapport/artefact, [D]=déduit du code, [S]=supposé.)\n\n## 1. TABLEAU DES DISPOSITIFS … [16631 caractères tronqués]`

  ```
message delivered to agent d31b3d9b-58e4-4d34-85fa-381b6f6a6a76
  ```

### 👤 Utilisateur

Background subagent ee19a880-cc76-4c5c-9fe0-5972bd73b533 finished and will do no further work unless you send it more.
Its closing message:
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

### 🤖 Assistant

⏵ Livraison du rapport final.

Rapport envoyé au parent. Le voici (lecture seule ; aucun fichier modifié, aucun entraînement lancé) :

# Inventaire du travail « côté modèle » — Qtrinet / Drave
[M] = mesuré (rapport ou artefact) · [D] = déduit du code · [S] = supposé.

## 1. TABLEAU DES DISPOSITIFS ENTRAÎNÉS
Professeur = Qwen2.5-0.5B GGUF (24 couches, 896 canaux), **jamais entraîné ici**, lu en boîte noire (couche 0 → couche 10). Tout apprentissage est en **forme fermée, numpy seul** : aucun torch, aucun `backward` dans `tools/` [M].

| Dispositif | Architecture / taille | Corpus | Coût | Fid. appr. | Fid. TEST | Invariance | Pire paire | Source |
|---|---|---|---|---|---|---|---|---|
| Pont linéaire rang 1 (`pont_recurrent.py`, `pont_fidele.py`) | y=(e·W0)·Pᵀ+moy ; 1 792–2 688 nombres ; artefact `pont_semantique_r1.npz` 16 560 o | UDHR art.1, 20 langues apprises / 20 jamais vues | 1 inversion ridge, 3 254 pas | 0,6677 | — | **0,9492** | **0,7762** | `reports/rapport-pont-semantique.md` §5 |
| Pont linéaire rang 128 (`pont_semantique.npz`, 1,38 Mo) | P,W0 896×128 = 230 400 param. | UDHR art.1, 40 langues → 6 tenues | idem | 0,8444 | **0,3691** | 0,2812 | — | idem §7 |
| ELM 2 couches (R aléatoire gelé + tanh, W ajusté) | H=64 : 114 688 p. ; H=256 : 458 752 ; H=4096 : 7 340 032 | idem | 1 inversion | 0,7278 / 0,7753 / 0,8947 | 0,5725 / 0,5795 / 0,5557 | 0,8882 / 0,7855 / 0,6048 | — | idem §7 |
| Réservoir 1 couche récurrente (`pont_reservoir.py`), réglé a=0,2 ride 3·10⁻¹, N=64 | s=(1−a)s+a·tanh(A·s+B·e) ; A,B gelés ; W ajusté ; 118 784 p. | UDHR art.1, 40 langues → 6 non latines | 1 inversion | — | **0,5921** (1 unité) / **0,4767** (10 unités) | **0,9772** / 0,9797 | **0,9576** / 0,9606 | `rapport-pont-semantique.md` §8-10 ; `rapport-pont-generatif.md` §13 |
| Réservoir variantes | N=256 ; N=8 ; ride 10 ; ensemble K=2 ; saut e_t ; rayon 0,7→1,2 | idem | idem | — | 0,5868 / 0,5671 / 0,5653 / 0,6010 / 0,3792 / 0,5924 | 0,8187 / 0,9884 / 0,9989 / 0,8563 / 0,2757 / 0,9076 | 0,6918 / 0,9777 / 0,9978 / 0,7938 / −0,0693 / 0,844 | idem §8-10 |
| Cascade générative + attrition (`pont_generatif.py`) : naissance 1 neurone à la fois, couches réelles, a=0,5 ride 1,0 | 256 neurones · 11 couches ; 1 neurone ; 128 | données PROPRES, 40 langues → 6, 10 unités | Gram recalculée par naissance | 0,7330 (256) | 0,4734 → 0,5059 → **0,5186** | 0,9983 → 0,9327 → 0,8874 | 0,6738 | `rapport-pont-generatif.md` §11-14 |
| Cascade sur données contaminées (comparaison) | 256/9 couches ; attrition→192 ; 2 cycles 108/10 couches ; 512/14 couches ; attrition→384 | ctx 1024 + 32 jetons générés | idem | — | 0,6056 / 0,6078 / 0,6079 / 0,5026 / **0,5035** | 0,9128 (128 n.) | 0,7719 | idem §1-9 |
| Loi fidélité/invariance | fid ≈ 0,3856·(1−invariance)+0,4752 | 11 points, données propres | — | r=0,9920, err. max 0,0047 | — | — | — | `rapport-pont-generatif.md` §14 ; `recapitulatif.md` §2.1 |
| Sous-ensemble actif + lecture quadratique | 157 canaux / 896 (18 %), 80 neurones · 8 couches [30,8,8,8,8,8,8,2] ; 34 canaux = 50 % de l'énergie | 40 langues → 6 tenues, masque lu sur l'apprentissage seul | 1 inversion | — | **0,6383** (const. 0,6140) | 0,9648 | 0,8821 | `recapitulatif.md` §6-9 |
| Discriminant de Fisher rang k (`discriminant_contenu.py`, `discriminant_transfert.py`, `stabilite_directions.py`) | eigh(solve(C_lang+λI, C_cont)), λ=1e-2·tr/ncan ; pont 120 neurones quadratique ride 0,03 graine 5 | 6 langues, 47 articles appris / 24 test | 1 eigh | — | — | rapport 1,474 = **136,4 %** du prof (rang 2) ; 0,910 (rang 5) | de–en 486 % du prof | `rapport-toutes-langues.md` §86-94 |
| Renforcement/atrophie local (`renforcement.py`) | cap_j=|corr(act, résidu)| = 0,018 ; f=1+η(2cap−1), η=0,1, 8 passes | caches Wikipedia | 8 passes | — | — | rapport P_cont/P_lang 1,290 → **1,312** (cible 10,912) | — | `rapport-toutes-langues.md` §72-73 |
| Renforcement des DIRECTIONS (`renforcement_directions.py`) | G=EᵀR, SVD(G), b_j←U[:,j] (Hebb sur l'entrée) ; 5 passes | idem | 1 SVD/passe | 0,4766 → 0,4667 | — | — | P_cont 318,7→**438,5** ▲, P_lang 247,1→**181,9** ▼ | idem §73 |
| MLP synthétique `src/tiny_model.py` | 32→64→10, ReLU+softmax, SGD lr 0,05, batch 128, 300-400 epochs, professeur = MLP gelé (teacher_seed 1234) | gaussiennes synthétiques 32 d / 10 classes | quelques min CPU | — | — | — | — | code + `run_quantify.py`, `run_clusters.py`, `run_sparsity.py` |
| Sonde linéaire (`sonde_pont.py`) ridge 1e-2 | prédit la plongée de t+1 depuis l'état | idem | 1 inversion | prof 0,7088 / pont 0,2599 / témoin 0,6600 | **−1,7411 / 0,0066 / −3,3080** (échec) | — | — | `rapport-pont-semantique.md` §6 |
| k-means experts (`run_real_clusters.py`) | 30 itérations, seed 0, centroïdes sur experts GGUF | GGUF qwen | — | sortie texte, aucun poids | — | — | — | code |

Coût d'un cycle [M] : traçage 3,7 s/langue (art.1 ; `--dense` 1,94 s vs 8,00 s défaut) ; ajustement **5-10 min → ~15 s** (24 000 lignes de Gram au lieu de 147 000-830 000 ; coût en n·d², d=1 792) ; 399 langues × 24 couches = 26 min (art.1) + 48 min (art.2) — `reports/rapport-cycle-rapide.md`.
Poids persistés [M] : `pont_semantique.npz` (1,38 Mo) et `pont_semantique_r1.npz` (16 560 o) sous `/home/stephane/Data13TB/stephane/corpus/udhr/` (+ copie dans `.../stephane/`). **Aucun .pt/.pth/.safetensors/.ckpt dans le dépôt** ; le reste des ajustements est éphémère (RAM).

## 2. CE QUI A MARCHÉ (positifs reproductibles)
1. **Le pont est un projecteur du partagé, sans récurrence ni gradient** : une seule application linéaire rend une sortie plus invariante que la couche qu'elle émule — 0,6965/0,5487 (pont) vs 0,6027/0,4269 (prof, couche 4) ; 0,6357/0,3828 vs 0,5464/0,2790 (couche 10), sur 6 écritures jamais vues (`rapport-pont-semantique.md` §3). Validé 20/20 : 0,7343 / 0,4421 (+17 % / +35 %) (§4).
2. **Un seul neurone suffit** : invariance 0,9492, pire paire 0,7762, 1 792 nombres (§5). Au-delà, la fidélité monte mais l'invariance baisse monotonement (0,9492 → 0,7658 de 1 à 64 neurones).
3. **Le réglage du réservoir est gratuit** : a 0,5→0,2 + ride 3·10⁻¹ → fidélité identique (0,5921 vs 0,5923), **+7,0 pts d'invariance, +11,4 pts de pire paire** ; répliqué sur 10 unités (+4,8 / +8,6) (§9-10). Le rayon spectral 0,7→1,2 est un **knob mort** (±3·10⁻⁴).
4. **Ajouter une COUCHE aide ; ajouter des NEURONES à un linéaire nuit** : linéaire 1→128 neurones, fid TEST 0,4752 → 0,3691 (surajustement pur) ; ELM 64 : 0,5725 / invariance 0,8882 (§7).
5. **La LOI** : fidélité et invariance sont les deux axes d'une droite (r=0,9920) ; la droite est une propriété du professeur, les deux architectures la parcourent (`rapport-pont-generatif.md` §14).
6. **Le sous-ensemble actif monte la cible** : 157 canaux/896 → +14 pts de fidélité, +1,7 d'invariance, +5,7 de pire paire ; contribution propre du pont **+0,0197 ± 0,0009** sur 7 périmètres (896→89 canaux). Lecture **quadratique** : +0,020 → +0,024 (+18 %), sans coût d'invariance (`recapitulatif.md` §6-9). Confirmé par Romeo : 0,6532 (canaux énergétiques) vs 0,5703 (896) (`rapport-toutes-langues.md` §18).
7. **Bande sémantique 10-15 / 24 couches (42-62 %)** confirmée sur **398 langues** : pic couche 13 (pooling moyenne, +0,0344), couche 10 (dernière position, +0,0397) ; couche 0 → +0,001. Effet réel mais petit (fond anisotrope 0,75-0,87) (`rapport-cycle-rapide.md` §7-8).
8. **Localité** : le jeton immédiat précédent porte les 2/3 du gain contextuel (+0,0866 sur +0,108 à la couche 3) ; gain divisé par 2 à chaque doublement de distance (`rapport-toutes-langues.md` §89, §95).
9. **Centrer la cible** : gain de fidélité **répliqué** +0,0092 puis +0,0062 (5-7 σ) (§88.5, §90).
10. **Transfert hors UDHR** : Romeo en→fr sans réapprentissage 0,6660 → 0,5802 ; viser la **couche 8** au lieu de 10 gagne **+0,0213** de fidélité transférée (§17-20).
11. **À l'échelle** : 301 langues apprises / 41 test, 40 neurones · 1 couche : fid TEST **0,7430**, invariance **0,9827**, pire paire **0,9165** (§14).

## 3. CE QUI A ÉCHOUÉ OU A ÉTÉ RÉFUTÉ
1. **Récurrence linéaire** s_t=A·s_{t−1}+B·e_t : fidélité en un pas 0,49-0,58, **boucle libre 0,0016 à 0,1266** ; le témoin « linéaire de e_t seul » fait **0,90-0,92** — la récurrence est deux fois moins bonne (`rapport-pont-semantique.md` §1-2).
2. **La profondeur en cascade n'apporte rien sur données PROPRES** : à 256 neurones, cascade 0,5186 vs réservoir plat 0,5145 (+0,41 pt) ; médiane 4 graines 0,5155 vs 0,5145 ; à 64 neurones **le plat gagne** (0,4998 vs 0,4940). L'attrition 256→192 fait **baisser** le test (0,5186 → 0,5161) alors qu'elle le faisait monter sur données contaminées. **Les +37 % à +70 % annoncés venaient des défauts de traçage** (32 jetons générés, troncature ctx 1024) (`rapport-pont-generatif.md` §13 ; `docs/note-un-pont-par-professeur.md` §3, §6).
3. **L'attrition ne généralise pas** : −0,003 pour −25 % de neurones, −0,021 pour 99 % ; critère de validation trop indulgent (seuil 0,005) (`recapitulatif.md` §11).
4. **La règle hebbienne locale ne transfère pas** : 29,151 vs 29,151 (autre texte), 1 116,532 vs 1 116,532 (autre article, breton) ; test tenu à l'écart 0,6027 → **0,5461**, et **dégrade de 5 à 10 %** les langues non vues (`docs/note-cancellation-evenementielle.md` §9). Le +11,7 % apparent venait de langues de test présentes dans l'entraînement.
5. **Renforcement/atrophie par mise à l'échelle : forcé à l'échec.** Capture réelle 0,018 (le 0,5 avait été *déduit*, corrigé au §73) → atrophie uniforme = identité du §67 : +1,7 % du chemin nécessaire (1,290 → 1,312 vs cible 10,912) (§72-73).
6. **Normalisation par langue** : invariance 0,9648 → 0,8823, pire paire 0,8821 → 0,6464 (`recapitulatif.md` §10.3).
7. **Plus de langues ne réduit pas l'écart de transfert** : 0,132-0,141 constant de 20 à 36 langues ; écart TEST +0,0693 (dont +0,0269 générique, +0,0424 de typologie) (§10.4, §13).
8. **Comparer deux professeurs est vide** : « notre pont bat le 30B » (0,9425 vs 0,9014) ne classe rien — deux espaces ; **il faut un pont par professeur** (`docs/note-un-pont-par-professeur.md`).
9. **Les énergies absolues ne mesurent rien** : l'échelle est gratuite (×5,40 ramène P_cont à 100 % sans changer le rapport) ; le critère §62.3 se réduit au rapport (`rapport-toutes-langues.md` §88, §91.6).
10. **Centrer la cible** : gain de rapport non répliqué (×8,1 à 47 articles → **×0,81** à 482) (§90).
11. **Sonde prédictive** : R² de test négatif pour les trois états (prof −1,7411, pont 0,0066, témoin −3,3080) — échec de protocole (`rapport-pont-semantique.md` §6).
12. **Discriminant : perd 4 à 7× en transfert de panel** (31,2 % roman→germanique, 55,1 % inverse, vs 211-320 % dans-panel) ; **rang 1 pire que tout** (112,3 %, min 75,2 %) ; rang 3 = seul à ne jamais perdre (min 104,7 %, σ 12,2) ; le classement des difficultés ne survit pas à la projection (§86-87, §93-94).
13. **Cancellation de langue = oracle, non déployable** : pire paire 0,2790 → 0,3779 (+35 %), δ calculé sur les langues de test ; témoin δ aléatoire même norme → 0,2296 (`docs/note-regle-contrastive.md` §1bis).
14. **Localité linéaire insuffisante** : 66,9 % de la variance de la couche 8 inexpliqués par jeton + 3 voisins (R² 0,3313) (§89).
15. **La cible initiale était mal choisie** : couche 10 déjà en re-spécialisation ; pic couche 8 (0,5985 Romeo / 0,5471 UDHR vs 0,5703 / 0,5247) (§17-20).

## 4. CORPUS DISPONIBLES
| Corpus | Chemin | Taille | Producteur |
|---|---|---|---|
| UDHR XML (456 langues) | `/home/stephane/Data13TB/stephane/corpus/udhr/udhr_xml` | 9,8 Mo, 456 XML | amont ; lu par `tools/extrait_udhr.py` |
| UDHR unités alignées | `.../corpus/udhr/unites.jsonl` | 5,47 Mo, 42 unités | `tools/extrait_udhr.py` |
| UDHR article 1 / article 2 | `.../corpus/udhr/article1` (399 .txt, 92 124 car.) / `article2` (271 958 car.) | 1,6 Mo | `tools/extrait_article1.py` |
| Traces UDHR | `article1_traces` 399 .drvf/2,1 Go ; `article2_traces` 4,7 Go ; `udhr392` 2,7 Go ; `udhr392_c8` 4,0 Go ; `unites` 491 Mo | 14 Go | moteur `--trace-flux` via `/tmp/trace_*.sh` (non versionnés) |
| Wikipedia apparié | `.../corpus/wiki_apparie` | 12 Go : 2 892 .txt + 2 892 .drvf = 482 titres × 6 langues | `tools/wiki_apparie.py` ← `data/wikipedia/db/*wiki_v14.db` (132 Go, 10 bases) |
| Wikipedia non apparié | `/tmp/wiki_{en,fr}.jsonl` ; traces `corpus/wiki_traces` 480 .drvf/1,8 Go | 1,8 Go | `tools/extrait_wikipedia.py` ← `.../nipada/wikipedia_decompressed` (81 Go, de/en/es/fr/it/ru) |
| Gutenberg parallèle | `Panini-Research/data/mass_ingestion/backlog_gutenberg_{en,fr,de,es}.db` (21,1/6,7/9,4/11,2 Mo) | 1,3 Go | `tools/extrait_gutenberg.py` (Romeo en↔fr, 48 .drvf), `tools/extrait_crime.py` (Crime en↔es, 48 .txt, traçage 8/48) |
| WikiText-2 | `data/wikitext2_test.txt` (+ .ids, wt2.json) | 359 ko | amont ; `tools/aiguille.py`, `run_harness.py` |
| Caches d'activations | `/tmp/cache_*.npz` | 41 fichiers, 9,5 Go (`cache_vf_{train,test}.npz` 1,75/1,83 Go = 482 art. × 6 langues ; `cache392*`, `cache_wiki_*`, `cache_rj_*`, `pcs_a1/a2`) | `tools/cache_pont.py` |
| Poids appris | `.../corpus/udhr/pont_semantique{,_r1}.npz` | 1,38 Mo + 16 560 o | `tools/pont_recurrent.py` |
| Découpage stratifié | `/tmp/decoupe392.json` (20 test / 40 val, graine 5) | — | `tools/decoupe_langues.py` |

Totaux [M] : `.../stephane/corpus` = **35 Go**, 3 804 .txt, 5 972 .drvf. `models/` = 2 GGUF Qwen2.5-0.5B (353 Mo / 531 Mo) téléchargés, jamais entraînés. **Aucun `tools/ingestion*.py`** n'existe.

## 5. CE QUI MANQUE (jamais entraîné ni essayé)
1. **Aucun transformer entraîné de bout en bout** : zéro rétropropagation dans `tools/` ; seul apprentissage par gradient = MLP 32→64→10 sur gaussiennes (`src/tiny_model.py`), aucun poids écrit.
2. **Aucune distillation** : mentionnée (`tools/approximabilite_bloc.py` L5, `reports/rapport-morcellement-experts.md`), jamais réalisée.
3. **Le test qui dirait si le pont jette de l'information utile n'a jamais été fait** : brancher le pont devant les couches suivantes du professeur et mesurer la perplexité (`rapport-pont-semantique.md`, réserves §1).
4. **La règle contrastive anti-hebbienne n'a jamais été apprise** : `D −= η·Δy⊗Δx` entre langues, avec alignement au jeton et terme de partage — seuls l'oracle de cancellation et la règle NON contrastive ont été mesurés (`docs/note-regle-contrastive.md`).
5. **La trace élargie portant la sortie de la porte FFN** (nécessaire à `HebbDiff` ciblé) n'existe pas.
6. **Aucun vrai arrêt anticipé moteur** : `--couches a:b` borne l'exécution mais charge les 24 couches ; **77 à 83 %** du calcul du professeur est jeté (`docs/note-cout-professeur.md` §6).
7. **Stabilité du sous-espace de rang 3, fidélité TEST et pire paire par rang** : nommées, non faites (`rapport-toutes-langues.md` §94.4).
8. **Aucune récurrence NON LINÉAIRE entraînée** autre que le réservoir gelé (DeltaNet du moteur, vérifié sur K3, jamais appliqué au pont).
9. **Un seul professeur** : le 30B est abandonné ; aucun `pont_30B`, alors que la règle est « un pont par professeur ».
10. **Alignement au jeton absent** (UDHR aligné par article : 33 jetons en anglais, 174 en hindi) ; seuls 2 des 30 articles alignés utilisés, ~3 % du corpus UDHR.
11. **Le pont n'est jamais branché dans le moteur** : `tools/applique_pont.py` est un applicateur hors ligne sur un `.drvf`.
12. **Parcimonie entraînée** : un seul essai sur le MLP synthétique ; jamais sur le pont ni un vrai modèle.
13. **Attrition sur réseau né librement, seuil de restriction (50/75 %), examen des 218 canaux propres à certaines langues** : ouverts (`recapitulatif.md` §6.4).
14. **Manques matériels** : `udhr_xml.zip`/`udhr_txt.zip` = pages 404 (196 o) ; traçage Crime 8/48 ; `wiki_{de,es,it,pt}.jsonl` absents ; `appr42`/`tenus42` vides ; 399 fichiers pour 456 langues annoncées (collisions ISO).

**Note de fiabilité** : les chiffres marqués [M] proviennent des rapports cités, qui documentent eux-mêmes leurs corrections successives (§81-§95 de `rapport-toutes-langues.md` listent sept chiffres antérieurs invalidés par un choix non déclaré : graine, panel, pooling, ajustement, échelle, ratio variables/points, réplication). Les résultats « couche 10 » antérieurs au 6 octobre sont à lire avec les réserves de troncature et de contamination ; les chiffres « données propres » sont ceux du §13-14 de `rapport-pont-generatif.md`.

