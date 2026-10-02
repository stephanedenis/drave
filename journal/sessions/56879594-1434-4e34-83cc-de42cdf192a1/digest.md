# Session DSH — relecture

- identifiant : `56879594-1434-4e34-83cc-de42cdf192a1`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-02 15:03:29
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM en Rust qui exécute les projections sous forme de listes d'activation creuses plutôt que de produits scalaires denses).

TÂCHE : dépouille EXHAUSTIVEMENT ces 20 fichiers Markdown :
reports/rapport-empreinte-memoire.md
reports/rapport-encodage.md
reports/rapport-eparsite.md
reports/rapport-execution-v41.md
reports/rapport-gpt-oss-perplexite.md
reports/rapport-gpu-scores.md
reports/rapport-gpu-topk-selection.md
reports/rapport-grappes.md
reports/rapport-greffon.md
reports/rapport-harnais.md
reports/rapport-inference.md
reports/rapport-lecteur-multifichiers.md
reports/rapport-localite-activation.md
reports/rapport-logits-gpu-vs-cpu.md
reports/rapport-minimal.md
reports/rapport-mla-experts.md
reports/rapport-mode4-lot-listes.md
reports/rapport-modele-reel.md
reports/rapport-mode-listes.md
reports/rapport-mur-memoire-4bits.md

Lis-les avec l'outil read (lecture complète, pas d'extrait). Tu dois produire un INVENTAIRE DE VOCABULAIRE, pas un résumé.

LIVRABLE, structuré exactement ainsi :

## A. Termes et sigles
Une entrée par ligne, au format :
- **TERME** (forme développée si elle apparaît) — définition en une phrase, telle qu'utilisée dans ces rapports ; où c'est utilisé (outil/fichier du dépôt cité dans le texte, ex. `tools/aiguille.py`) ; première occurrence `reports/fichier.md:ligne`.

Inclus TOUT ce qui n'est pas du français courant : sigles (AER, KV, MoE, MLA, GGUF, DRVF, NLL, RSS, VRAM, TLB, NUMA, AVX2, PTX, MXFP4, Q4_K, IQ2_XXS...), noms d'algorithmes (Sinkhorn, Hadamard, RoPE, YaRN, softmax, top-k, RMSNorm, SiLU, SwiGLU, LoRA, MTP, DSA, CSA, HCA...), vocabulaire matériel (FPGA, DSP, ALM, M20K, DDR3, PCIe, HBM...), vocabulaire du projet (paire, grappe, shard, push, pull, porte, porte de correction, densité d'activation, liste valuée, engram, hyper-connexion, greffon, aiguille, mode 3/mode 4, DRVF v5...), unités et métriques (perplexité, NLL, débit, GFLOPS, Gbit/s, MTok/s, latence, p50/p95...), formats de fichiers et outils.

## B. Chiffres et affirmations mesurées
Liste des mesures chiffrées importantes avec `fichier:ligne` et la citation exacte (entre guillemets). Une ligne par mesure. Sois exhaustif : c'est ce qui me servira à détecter les contradictions entre documents.

## C. Contradictions, chiffres périmés, affirmations douteuses
Tout ce qui te semble se contredire DANS ces 20 fichiers, ou être signalé comme périmé par le texte lui-même (« périmé », « obsolète », « ne plus utiliser », « remplacé par », « faux », « corrigé »). Format : `fichier:ligne` — citation — pourquoi c'est douteux/périmé.

## D. Fichiers du dépôt cités
Liste des chemins de fichiers du dépôt cités dans ces rapports (docs/, reports/, tools/, src/, drave-core/, etc.), avec ce qu'ils font d'après le texte.

Sois dense et exhaustif ; pas d'introduction ni de conclusion. Cite les chemins exacts. Ne modifie AUCUN fichier.
Your parent agent id is "3d5618a0-4e3a-45bb-943d-a72c753fb7da". Before you finish, send your result to that agent with send_message({ agent_id: "3d5618a0-4e3a-45bb-943d-a72c753fb7da", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Reading the 20 reports to build the vocabulary inventory.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l reports/rapport-empreinte-memoire.md reports/rapport-encodage.md reports/rapport-eparsite.md reports/rapport-execution-v41.md reports/rapport-gpt-oss-perplexite.md reports/rapport-gpu-scores.md reports/rapport-gpu-topk-selectio … [474 caractères tronqués]`

  ```
545 reports/rapport-empreinte-memoire.md
    88 reports/rapport-encodage.md
    75 reports/rapport-eparsite.md
    81 reports/rapport-execution-v41.md
   254 reports/rapport-gpt-oss-perplexite.md
    82 reports/rapport-gpu-scores.md
   360 reports/rapport-gpu-topk-selection.md
    62 reports/rapport-grappes.md
    73 reports/rapport-greffon.md
    72 reports/rapport-harnais.md
   344 reports/rapport-inference.md
   269 reports/rapport-lecteur-multifichiers.md
    81 reports/rapport-localite-activation.md
    96 reports/rapport-logits-gpu-vs-cpu.md
    89 reports/rapport-minimal.md
   237 reports/rapport-mla-experts.md
   105 reports/rapport-mode4-lot-listes.md
    83 reports/rapport-modele-reel.md
    61 reports/rapport-mode-listes.md
   238 reports/rapport-mur-memoire-4bits.md
  3295 total
  ```

### 🤖 Assistant

⏵ Reading the largest reports first.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empreinte-memoire.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gpu-topk-selection.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empreinte-memoire.md</path>
<type>file</type>
<content>
1: # Rapport — l'empreinte mémoire : ce qui réduit vraiment ce qu'il faut charger
2: 
3: Session du 01/10, de 10 h 47 à 17 h 35. Modèle d'étude : Qwen3-30B-A3B
4: (48 couches, 128 experts, top-8), dont on sait produire les traces de routage.
5: Cible : DeepSeek-V4.1-Flash (40 couches, **384 experts**, top-6, 365,7 Go).
6: 
7: **Résultat principal** : l'empreinte de V4.1 tombe de 365,7 Go à **50–80 Go**,
8: non pas en découpant les experts mais parce que **56 % du modèle (203 Go) est une
9: table d'engram creuse par nature**, qu'il suffit de mmapper. Une session de
10: 10 000 jetons n'en touche que **4,6 Mo**.
11: 
12: ## La question
13: 
14: Un modèle de 365 Go ne tient pas dans 125 Go de RAM. Que peut-on **ne pas
15: charger** ? Et parmi les pistes — découpage plus fin, grappes par langue, cache,
16: restriction du vocabulaire — lesquelles paient réellement ?
17: 
18: Toutes les mesures qui suivent viennent de traces de routage réelles
19: (`DRAVE_TRACE_EXPERTS`), pas d'estimations.
20: 
21: ## 1. La granularité : la courbe s'arrête à l'expert
22: 
23: Volu
… [23249 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gpu-topk-selection.md</path>
<type>file</type>
<content>
1: # Rapport — la sélection top-k et la somme sur GPU (noyaux 2 et 3 du plan)
2: 
3: **En une ligne** : la sélection du top-k de l'attention tourne maintenant sur GPU en
4: **quatre passes d'histogramme + deux noyaux de collecte**, elle rend le **même
5: ensemble d'indices que le CPU** (14/14 lignes, différence symétrique 0 à toutes les
6: tailles testées) et coûte **0,89 ms** là où le tri CPU en coûte **497 ms** à
7: 262 144 clés. Le **noyau 3** (softmax sur les k retenus + puits, puis Σ w·V) est
8: écrit et vérifié à **2,7–4,8e-7** — sous le critère de 1e-6 du plan.
9: 
10: Plan suivi : [`docs/plan-gpu-topk.md`](../docs/plan-gpu-topk.md), étape 2.
11: Noyau 1 (les scores) : [`reports/rapport-gpu-scores.md`](rapport-gpu-scores.md).
12: 
13: ## Ce qui a été écrit
14: 
15: Trois noyaux dans `drave-core/gpu/drave_gpu.cu` (le fichier passe de 10 à 13
16: noyaux avec la sélection, puis à **14** avec le noyau 3 — 956 lignes) :
17: 
18: | noyau | rôle |
19: |---|---|
20: | `attn_topk_histo` | histogramme d'un OCTET des scores, pour les seuls scores dont les octet
… [21231 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading more reports in parallel.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-inference.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-lecteur-multifichiers.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gpt-oss-perplexite.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-inference.md</path>
<type>file</type>
<content>
1: # Inférence complète en Rust — Qwen2.5-0.5B sans GPU, sans BLAS, sans dépendance
2: 
3: **2 319 lignes de Rust, `std` seul, zéro dépendance.** Le modèle Qwen2.5-0.5B-Instruct
4: quantifié Q8_0 (507 Mo, 494 M de poids) tourne en **mode listes d'événements** sur le
5: CPU de cette machine (2 × Xeon E5-2687W v3), et génère du texte correct :
6: 
7: ```
8: $ drave-core qwen2.5-0.5b-q8_0.gguf --infer --chat \
9:       --prompt "Explain in one sentence why the sky is blue."
10: 
11: <|im_start|>user
12: Explain in one sentence why the sky is blue.<|im_end|>
13: <|im_start|>assistant
14: The sky is blue because it reflects sunlight, which contains colors such as
15: red, orange, yellow, green, blue, and indigo, which are all visible in the
16: spectrum.<|im_end|>
17: 
18: généré  : 38 tokens en 3.86 s  (9.85 tok/s)
19: ```
20: 
21: Aucun GPU. Aucune bibliothèque de tenseurs, aucune BLAS, aucun crate : le lecteur
22: GGUF, le tokenizer BPE, le moteur d'événements et le forward Qwen2 sont écrits ici.
23: 
24: ---
25: 
26: ## 1. Ce qui a été construit
27: 
28: | Fichier | 
… [16521 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-lecteur-multifichiers.md</path>
<type>file</type>
<content>
1: # Rapport — un modèle éclaté se lit comme un seul
2: 
3: Sprint 08 · 11:13 → 13:13 · binaire `drave-core` (release), commit à venir.
4: 
5: ## La question
6: 
7: Un modèle trop gros pour un nœud, ou un MoE dont un nœud ne sert qu'un huitième
8: des experts, doit pouvoir être lu **par morceaux** — sans requantification, sans
9: recopier les poids, et sans que le moteur ait à savoir que le modèle est découpé.
10: Le sprint précédent a produit le format (convertisseur, 1 587 tenseurs vérifiés
11: par SHA-256) ; celui-ci devait le rendre **lisible**, et le prouver.
12: 
13: ## Ce qui a été mesuré
14: 
15: ### L'épreuve décisive : origine contre clusters
16: 
17: Mêmes jetons, même contexte, même quantification, chemin par jeton. Le modèle
18: d'origine (18,56 Go, un fichier, sur le disque mécanique) contre le même modèle
19: éclaté en `commun.gguf` + 8 × `cluster-XX.gguf` (sur le NVMe) :
20: 
21: | | perplexité | temps |
22: |---|---|---|
23: | modèle d'origine | **15,2789** | 12,2 s |
24: | modèle en clusters | **15,2789** | 11,6 s |
25: 
26: **Identique
… [13104 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gpt-oss-perplexite.md</path>
<type>file</type>
<content>
1: # Perplexité de gpt-oss : deux bugs réels, une prémisse fausse
2: 
3: > Session du 28/09 (reprise de `REPRISE.md` §6.a). Tous les chiffres de ce
4: > rapport sont **mesurés** sur cette machine, avec le corpus
5: > `/tmp/wt2_txt.txt` (20 000 premiers octets de `data/wikitext2_test.txt`),
6: > gpt-oss-120b MXFP4, `--ctx 256 --dense --threads 16`, sauf mention contraire.
7: 
8: ## 1. Ce qu'on croyait
9: 
10: `REPRISE.md` §6.a annonçait : perplexité **39,8** « au lieu de l'ordre de 6 »,
11: génération correcte, et une perplexité qui **croît avec la fenêtre**
12: (39,8 à 63 jetons, 129,9 à 511). Trois hypothèses étaient en lice : le gabarit
13: harmony, un codage de position faux (YaRN), et un bug de calcul restant.
14: 
15: ## 2. Ce qui était réellement cassé
16: 
17: ### a. Le biais de la projection de sortie d'attention était ignoré
18: 
19: gpt-oss déclare `attention_bias = true` : ses projections Q, K, V **et O** ont un
20: biais. Le chargeur passait bien les biais de Q, K et V, mais `None` pour
21: `attn_output` — un décalage constant ajouté à la sortie
… [12390 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the smaller reports in batches.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mur-memoire-4bits.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mla-experts.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mode4-lot-listes.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-logits-gpu-vs-cpu.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mur-memoire-4bits.md</path>
<type>file</type>
<content>
1: # Le mur mémoire, et ce que les 4 bits achètent vraiment
2: 
3: > Suite de `rapport-croisement-push-pull.md`. Trois bugs de mesure corrigés, une
4: > mesure de bande passante, et un chemin 4 bits écrit puis mesuré.
5: 
6: ## 1. Trois bugs qui faussaient les conclusions
7: 
8: | bug | symptôme | cause |
9: |---|---|---|
10: | **drapeau final ignoré** | `--dense` « donnait exactement le même résultat que push » | `while i + 1 < args.len()` : un drapeau en **dernière** position n'était jamais lu |
11: | **tranches périmées en mode dense** | PPL **4 361 879** au lieu de 19,26 | chaque worker n'écrivait que sa tranche ; la somme des 16 vecteurs récupérait les restes du travail précédent |
12: | **parenthesage flottant** | pull et push divergeaient d'un token | `(dot×s)×sx` contre `acc×(sx×s)` — deux arrondis différents sur des sommes entières pourtant exactes |
13: 
14: Le troisième n'était pas un bug mais une occasion : en écrivant les deux chemins
15: avec **le même ordre d'opérations**, et parce que les sommes entières sont
16: exactes des deux côtés, on ob
… [11438 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mla-experts.md</path>
<type>file</type>
<content>
1: # Rapport — MLA à rang faible et formats sans noyau : GLM-5.3 et Kimi deviennent calculables
2: 
3: Session du 02/10, en autonomie, suite du [rapport sur le
4: routage](rapport-routage-experts.md). Le point de départ était un refus : le
5: moteur ne savait pas calculer DeepSeek-V4-Flash. Le trajet, lui, a traversé
6: quatre verrous qui accusaient tous le fichier alors que c'était le moteur.
7: 
8: ## 1. Les quatre verrous, dans l'ordre où ils sont tombés
9: 
10: | ce qui échouait | ce que le moteur disait | ce qui manquait vraiment |
11: |---|---|---|
12: | V4-Flash, V4.1 | `tenseur blk.3.attn_q.weight absent` | attention MLA à rang faible |
13: | GLM-5.3, Kimi | `mélanges d'experts chargés : 0/79` | formats d'experts IQ sans noyau |
14: | GLM-5.3 | `projection sans aucun format` | FFN dense des 3 premières couches |
15: | V4, GLM-Flash | *(rien : ça tournait)* | hyper-connexions, index, sortie à rang faible |
16: 
17: Aucun de ces messages ne nommait la cause. Un GGUF de 216 Go ne perd pas ses
18: tenseurs : c'est le moteur qui ne les lisait pas.
19: 
20: ## 2
… [12111 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mode4-lot-listes.md</path>
<type>file</type>
<content>
1: # Mode 4 — le lot en listes : ÷2,3 sur les octets, et ce qu'il coûte
2: 
3: **En une ligne** : un préremplissage de N états peut voyager en **listes creuses**
4: au lieu de f32 dense — 1,5 ko par jeton contre 3,5 — au prix d'une quantification
5: dont l'effet **dépend de la longueur du lot**, ce que ce rapport chiffre au lieu de
6: le cacher.
7: 
8: ## Ce que le mode ajoute
9: 
10: Le mode 3 (lot dense) envoie `t × dimension × f32` : simple, sans perte, et c'est
11: lui qui a rendu le préremplissage réparti fidèle (0,00e0). Le mode 4 envoie le même
12: lot **en listes** : chaque état est encodé comme le mode 2 (indices par écarts u8
13: avec échappement vers u16, valeurs i8, une échelle f32 par bloc de 32 canaux) et
14: **auto-délimité** par un préfixe de 12 octets — `a_j · n_blocs_j · longueur_j` —
15: dont les trois tailles se lisent avant toute allocation.
16: 
17: Le mode est **avec perte**, comme le mode 2. Le critère n'est donc pas l'égalité
18: mais la comparaison à ce que le mode 2 coûte déjà.
19: 
20: ## Mesuré
21: 
22: Corpus WikiText-2, 256 jeto
… [4991 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-logits-gpu-vs-cpu.md</path>
<type>file</type>
<content>
1: # Rapport — pourquoi le déport des projections change (ou non) la perplexité
2: 
3: **En une ligne** : sur un modèle **dense**, le déport des projections donne des
4: logits **identiques** au CPU (écart moyen 0,0000, fichiers bit à bit égaux) ; sur un
5: **MoE**, il les décale de **0,038 nat** en moyenne — **497 jetons sur 511 gardent le
6: même top-1** (14 divergent), et cela suffit à déplacer la perplexité de 1,2 %. L'hypothèse la plus simple, fortement étayée par ce contraste, est que de
7: minuscules écarts numériques **changent le routage des experts** (top-8 sur 128).
8: 
9: ## Le doute, et d'où il vient
10: 
11: Au sprint 2, gpt-oss-120b MXFP4 à `--ctx 1024`, 511 jetons :
12: 
13: | chemin | perplexité | écart vs CPU |
14: |---|---|---|
15: | CPU | 18,5803 | — |
16: | GPU, miroir KV seul (`DRAVE_GPU_KV`) | 18,3074 | −1,47 % |
17: | GPU, projections seules (`DRAVE_GPU`) | 18,3538 | −1,22 % |
18: 
19: Ajouter le miroir KV aux projections ne pèse que **0,25 % de plus** : l'essentiel
20: (1,22 %) vient du déport des **projections** lui-même. Or les noy
… [4212 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the remaining eleven reports.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-encodage.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-eparsite.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-execution-v41.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gpu-scores.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grappes.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-greffon.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-encodage.md</path>
<type>file</type>
<content>
1: # Drave — encodage de structure : éliminer la valeur
2: 
3: Idée testée : remplacer `(position, valeur)` par **deux listes triées de
4: destinations** (les « + » et les « − »). Le signe est porté par l'appartenance
5: à la liste : **plus aucun bit de valeur n'est stocké**, il ne reste que de la
6: position. Coûts mesurés sur les matrices réelles, pas estimés.
7: 
8: Modèle : MLP 32→64→10 (2688 poids), référence float 76.07 %.
9: 
10: ## Coûts réels (bits/poids)
11: 
12: | Motif | k | Densité | Accuracy | bitmap+signe | **listes signées** | CSR | dense | entropie | écart moyen |
13: |---|---|---|---|---|---|---|---|---|---|
14: | non structuré | 1 | 26.9 % | 45.02 % | 1.27 | **3.52** | 10.03 | 2.00 | 0.90 | 3.6 |
15: | non structuré | 2 | 49.6 % | 72.46 % | 1.50 | **5.02** | 18.02 | 2.00 | 1.22 | 2.0 |
16: | non structuré | 1 | 18.0 % | 64.55 % | 1.18 | **3.24** | 7.08 | 2.00 | 0.71 | 5.5 |
17: | non structuré | 2 | 24.6 % | 65.53 % | 1.25 | **3.95** | 9.52 | 2.00 | 0.85 | 4.1 |
18: | non structuré | 1 | 9.0 % | 59.18 % | 1.09 | **2.88** | 4.13 | 2.00 | 0.44 | 11.0
… [4273 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-eparsite.md</path>
<type>file</type>
<content>
1: # Drave — élagage et approche par événement
2: 
3: Modèle minimal (MLP 32→64→10), accuracy float **76.07 %**, ternaire (non élagué) **49.71 %**.
4: 
5: ## 1. Densité naturelle du ternaire
6: 
7: - poids non nuls : **26.3 %** (densité d = 0.263)
8: - activations non nulles après ReLU : **52.8 %**
9: - événements réels (poids ∧ activation) : **13.9 %**
10: 
11: ## 2. Coût des encodages (bits par poids)
12: 
13: | Encodage | Coût | À d = 50 % | À d = 25 % |
14: |---|---|---|---|
15: | dense 2 bits | 2,00 | 2,00 | 2,00 |
16: | **bitmap + signe** | **1 + d** | **1,50** | **1,25** |
17: | CSR bloc 16 b | 17·d | 8,50 | 4,25 |
18: | CSR plat 32 b | 33·d | 16,50 | 8,25 |
19: | N:M structuré (2:4) | (m+n)/m | 1,50 | — |
20: 
21: > Un poids ternaire non nul ne porte **qu'un signe**. Le bitmap dit *où* sont
22: > les non-nuls, le signe dit *lequel*. C'est pourquoi « bitmap + signe » est
23: > toujours ≤ au code dense 2 bits, et strictement meilleur dès qu'il y a un zéro.
24: 
25: ## 3. Frontière précision ↔ bits/poids (mesurée)
26: 
27: | Gardés | Densité | Accuracy | dense |
… [3509 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-execution-v41.md</path>
<type>file</type>
<content>
1: # Rapport — test d'exécution locale de DeepSeek-V4.1-Flash, avec toutes les optimisations
2: 
3: 02/10, sur la copie NVMe `/home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf`
4: (365,71 Go, 1 046 tenseurs, 40 couches, 384 experts dont 6 par jeton).
5: 
6: **Verdict en une ligne : ce que le moteur sait faire de ce modèle marche et est
7: mesuré ; la passe avant est refusée en 0,33 s avec la liste exacte de ce qui
8: manque. Aucun chiffre de calcul sur V4.1 n'existe, ici ou ailleurs dans ce
9: dépôt — uniquement des mesures statiques.**
10: 
11: ## 1. Ce qui tourne, avec les optimisations
12: 
13: | test | commande | résultat mesuré |
14: |---|---|---|
15: | en-têtes seuls (`--tensors`) | mmap, aucune copie | 1 046 tenseurs, **365,70 Go** lus en **63,8 ms** |
16: | configuration (`--config`) | en-tête seul | **74 ms** au total, aucune donnée lue |
17: | plan matériel (`--materiel`) | détection + heuristiques | 20 threads, 16 lecteurs disque, cache experts 19,5 Go, cache KV 32 bits |
18: | sonde engram (`--sonder-engram 10000`) | mmap, 16 lecteur
… [4402 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gpu-scores.md</path>
<type>file</type>
<content>
1: # Noyau GPU de scores d'attention — le premier des trois du top-k
2: 
3: **En une ligne** : les scores d'attention se calculent maintenant **en VRAM**, avec
4: un écart de **1,6 à 2,3e-7** sur la référence CPU et **40× plus vite** à 262 144 clés —
5: c'est la brique qui manquait pour que le mode creux (`--attn-topk`) cesse de
6: retomber sur le CPU au long contexte.
7: 
8: ## Ce que le noyau fait
9: 
10: `attn_scores` (dans `drave-core/gpu/drave_gpu.cu`) reprend la tuile de clés du noyau
11: d'attention complet — chargement coopératif de 32 clés, déquantification int8/int4/
12: f32, produit scalaire par tête de requête — mais **écrit les scores** `rep × n` au
13: lieu de les consommer dans une softmax en ligne. Une grille de `n_kv × nsplit`
14: blocs : le découpage en tranches est celui du noyau complet, et c'est lui qui fait
15: la différence de débit.
16: 
17: `--banc-topk N` compare les deux chemins sur des clés et une requête
18: déterministes (même générateur que le banc KV), et chronomètre les deux.
19: 
20: ## Mesuré
21: 
22: Qwen2.5-0.5B (2 têtes KV × 64
… [3455 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-grappes.md</path>
<type>file</type>
<content>
1: # Drave — grappes afférentes/efférentes et découpage en sous-modèles
2: 
3: Modèle : MLP 32→64→10, structure **imposée à l'entraînement**
4: (masque à 4 grappes + une fraction d'arêtes inter-grappes).
5: 
6: ## Coût de la structure imposée
7: 
8: | Couplage | Accuracy | Non-nuls | Densité | Arêtes hors grappe | Écart moyen | Positions (b/poids) |
9: |---|---|---|---|---|---|---|
10: | 0.0 % | 74.12 % | 346 | 12.9 % | 0.0 % | 2.40 | 0.39 |
11: | 1.0 % | 73.34 % | 346 | 12.9 % | 2.7 % | 3.26 | 0.39 |
12: | 5.0 % | 74.02 % | 373 | 13.9 % | 12.0 % | 4.14 | 0.69 |
13: | 20.0 % | 75.78 % | 459 | 17.1 % | 35.9 % | 6.69 | 0.85 |
14: | 100.0 % | 76.07 % | 708 | 26.3 % | 75.0 % | 3.43 | 0.79 |
15: 
16: **Comparaison à budget égal** (346 non-nuls) :
17: 
18: - modèle en grappes pures : **74.12 %**
19: - meilleur modèle dense de même budget (32→7→10, 311 paramètres) : **74.12 %**
20: 
21: ## Trafic ring (découpage en 4 sous-modèles, 7B type)
22: 
23: **Ce qui traverse le ring, ce sont les activations, pas les poids** (ceux-ci
24: restent résidents sur leur carte).
25: 
26: | C
… [1809 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-greffon.md</path>
<type>file</type>
<content>
1: # Greffon : plomberie d'apprentissage
2: 
3: Première brique de la boucle d'apprentissage : **charger un modèle augmenté de
4: nœuds, sans réentraînement**, et mesurer la perplexité avant/après. C'est ce qui
5: rend l'étape A du [programme de recherche](../docs/programme-recherche.md)
6: exécutable.
7: 
8: ---
9: 
10: ## 1. Le mécanisme
11: 
12: Un greffon ajoute **un neurone** à une couche, à la forme SwiGLU du réseau :
13: 
14: ```
15: a = silu(u · x) · (v · x)          contribution ajoutée au flux résiduel : a · d
16: ```
17: 
18: `--patch <fichier.bin>` charge `(u, v, d)` pour une couche. Format binaire :
19: `QPAT | version | couche | n | u[n] | v[n] | d[n]`, en f32 little-endian.
20: 
21: Pourquoi c'est intéressant malgré le verdict hebbien : **le produit de deux
22: formes linéaires est quadratique.** Prendre `u` sur une ligne existante de `gate`
23: et `v` sur une **autre** ligne de `up` fabrique une caractéristique que le réseau
24: n'a jamais calculée — les 4 864 neurones d'origine n'apparient que `gate[i]` avec
25: `up[i]`. Le produit croisé `gate[i] · u
… [2370 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the final five reports.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-harnais.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-localite-activation.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-minimal.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-modele-reel.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mode-listes.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-harnais.md</path>
<type>file</type>
<content>
1: # Drave — harnais de test : qualité et débit variable
2: 
3: Modèle : **qwen2 Q8_0** · corpus : WikiText-2 test (4080 tokens évalués).
4: 
5: ## 1. Qualité — perplexité
6: 
7: **PPL = 24.77** sur 4080 tokens.
8: 
9: Référence : un Qwen2.5-0.5B correct tourne autour de 15-25 sur WikiText-2 ;
10: cette valeur valide l'implémentation numpy (aucune bibliothèque ML).
11: 
12: ## 2. Événements par couche
13: 
14: | Couche | Activations nulles (MLP) | Nulles (après SiLU) | Événements MLP | Événements attention |
15: |---|---|---|---|---|
16: | 0 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
17: | 1 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
18: | 2 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
19: | 3 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
20: | 4 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
21: | 5 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
22: | 6 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
23: | 7 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
24: | 8 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
25: | 9 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
26: | 10 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
27: | 11 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |
28
… [2060 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-localite-activation.md</path>
<type>file</type>
<content>
1: # Localité d'activation : ce que PowerInfer apporte, et ce qu'on en garde
2: 
3: > Étude demandée du dépôt [SJTU-IPADS/PowerInfer](https://github.com/SJTU-IPADS/PowerInfer)
4: > (miroir `Tiiny-AI/PowerInfer`), confrontée à nos propres mesures. Tout ce qui
5: > suit est mesuré sur cette machine ; les chiffres de PowerInfer viennent de leur
6: > README et de l'article SOSP 2024.
7: 
8: ## 1. Leur idée
9: 
10: La distribution des activations d'un LLM suit une **loi de puissance** : une
11: petite partie des neurones est active presque toujours (« chauds »), le reste
12: dépend de l'entrée (« froids »). PowerInfer en tire un moteur hybride CPU/GPU
13: **à la granularité du neurone** : les chauds résident sur le GPU, les froids sont
14: calculés sur le CPU, ce qui réduit à la fois la VRAM nécessaire et le trafic
15: PCIe. S'y ajoutent un **prédicteur** (un petit MLP qui devine l'ensemble actif
16: pour précharger) et des **opérateurs creux conscients des neurones**. Leur modèle
17: TurboSparse (≈ 90 % de creux) est *entraîné* ainsi, précisément parce
18: qu'
… [4077 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-minimal.md</path>
<type>file</type>
<content>
1: # Drave — test de principe : modèle minimal en ternaire / multi-bits
2: 
3: Modèle : MLP 32→64→10, entraîné sur 4096 exemples synthétiques, évalué sur 1024.
4: 
5: ## 1. Fidélité de la quantification
6: 
7: | Format des poids | b/poids | Accuracy | Δ vs float |
8: |---|---|---|---|
9: | float32 (référence) | 32.00 | 76.07 % | +0.00 pt |
10: | int8 (signe-magnitude) | 8.00 | 76.27 % | +0.20 pt |
11: | int4 (signe-magnitude) | 4.00 | 74.12 % | -1.95 pt |
12: | ternaire 1,58 b (dense 2 b) | 2.00 | 49.71 % | -26.37 pt |
13: | multi 2 plans ternaires | 4.00 | 73.44 % | -2.64 pt |
14: | multi 3 plans ternaires | 6.00 | 74.12 % | -1.95 pt |
15: | multi 4 plans ternaires | 8.00 | 75.98 % | -0.10 pt |
16: 
17: ### Chemin entier (ce que fera le FPGA : add/sub, aucun DSP)
18: 
19: | Mesure | Valeur |
20: |---|---|
21: | Exactitude arithmétique — couche 1 (entier vs flottant, mêmes entrées) | 4.233e-07 |
22: | Exactitude arithmétique — couche 2 | 1.861e-06 |
23: | Erreur de quantification des activations — couche 1 | 1.089e-01 |
24: | Erreur de quantification des activations —
… [4096 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-modele-reel.md</path>
<type>file</type>
<content>
1: # Drave — le modèle réel expose-t-il ses grappes ?
2: 
3: Modèle analysé : **qwen2**, 24 couches, hidden 896, intermédiaire 4864, 14 têtes / 2 KV (GQA).
4: 
5: ## 1. Parcimonie intrinsèque
6: 
7: | Tenseur (couche 0) | \|w\|<5 % max | <10 % | <20 % |
8: |---|---|---|---|
9: | blk.0.attn_norm.weight | 19.0 % | 77.9 % | 92.2 % |
10: | blk.0.ffn_down.weight | 62.5 % | 91.1 % | 99.7 % |
11: | blk.0.ffn_gate.weight | 73.8 % | 96.3 % | 99.9 % |
12: | blk.0.ffn_up.weight | 56.5 % | 87.5 % | 99.7 % |
13: | blk.0.ffn_norm.weight | 0.0 % | 0.0 % | 0.0 % |
14: | blk.0.attn_k.weight | 68.5 % | 87.7 % | 96.8 % |
15: | blk.0.attn_output.weight | 95.9 % | 99.7 % | 100.0 % |
16: | blk.0.attn_q.weight | 79.3 % | 94.3 % | 99.1 % |
17: | blk.0.attn_v.weight | 45.2 % | 74.6 % | 95.7 % |
18: 
19: ## 2. Spécialisation afférente de la dimension cachée
20: 
21: Part de la masse d'entrée d'un neurone venant de sa grappe dominante.
22: **1/G = pas de structure, 1 = blocs disjoints.**
23: 
24: | Grappes G | Couche 0 (apprise) | Couches 1+ (test) | Grappes aléatoires | Test/aléatoire |
25
… [2900 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mode-listes.md</path>
<type>file</type>
<content>
1: # Drave — « mode listes » : exécuter sans GPU
2: 
3: Objectif : **pas** de compresser le modèle, mais l'exécuter avec des opérations
4: purement structurelles (compter, décaler, additionner) — donc **sans multiplieur,
5: sans cœur tensoriel, sans GPU**.
6: 
7: Mesures sur **qwen2 Q8_0** (494.0 M poids, densité 99.2 %).
8: 
9: ## Deux façons d'exprimer la valeur
10: 
11: | Mode | Principe | Décodeur |
12: |---|---|---|
13: | **unaire** | la valeur est la longueur de la suite de zéros (≤ 127) | un compteur |
14: | **décalage-addition** | valeur positionnelle, une addition par bit à 1 | un décalage + un compteur |
15: 
16: ## 1. Coût par poids
17: 
18: | Mode | additions/poids | bits de flux/poids |
19: |---|---|---|
20: | multiplieur (référence GPU) | 0.99 | 8,00 |
21: | **décalage-addition (popcount)** | **3.10** | 8,00 |
22: | **unaire (suites de zéros)** | **42.45** | **42.45** |
23: 
24: ➡️ L'unaire coûte **13.7× plus** d'opérations *et* de flux, pour le
25: même résultat exact.
26: 
27: ## 2. Projection sur 7 G poids
28: 
29: | Support | 8 bits positionnel |
… [1777 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Harvesting repo file paths cited across the 20 reports.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && grep -ohE '`[^`]*\\.(py|rs|sh|cpp|cu|h|md|gguf|tsv|bin|txt|json|toml)`' rapport-empreinte-memoire.md rapport-encodage.md rapport-eparsite.md rapport-execution-v41.md rapport-gpt-oss-perplexite.md rapport-gpu-scores.md rapport … [406 caractères tronqués]`

  ```
`bpe_np.py`
`cluster-00.gguf`
`cluster-100.gguf`
`cluster-20.gguf`
`cluster-XX.gguf`
`commun.gguf`
`compare_logits.py`
`config.json`
`cuda_stub.h`
`data/wikitext2_test.txt`
`docs/contexte-long.md`
`docs/plan-gpu-topk.md`
`drave-core/gpu/drave_gpu.cu`
`gpt_oss/torch/model.py`
`/home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf`
`llama.cpp`
`llama.cpp/src/models/deepseek4.cpp`
`mapping.tsv`
`model.rs`
`models/Qwen2.5-0.5B-Q4_0.gguf`
`rapport-croisement-push-pull.md`
`reports/rapport-gpu-scores.md`
`reports/rapport-gpu-topk-selection.md`
`REPRISE.md`
`run_clusters.py`
`run_encoding.py`
`run_harness.py`
`run_list_mode.py`
`run_quantify.py`
`run_real_clusters.py`
`run_sparsity.py`
`src/bpe_np.py`
`src/engine.rs`
`src/gguf.rs`
`src/list.rs`
`src/main.rs`
`src/model.rs`
`src/tokenizer.rs`
`src/transformer_np.py`
`/tmp/ids_qwen_long.txt`
`/tmp/wt2_txt.txt`
`tools/analyse_experts_statique.py`
`tools/compare_logits.py`
`tools/inventaire_modeles_lourds.sh`
`tools/mla_synthetique.py`
`tools/pair_factice.py`
`tools/portes_formats.sh`
`tools/*.py`
`tools/ref_logits.cpp`
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && grep -ohE '(\\[)?`?(docs|reports|tools|src|drave-core|models|data|journal|gpu)/[A-Za-z0-9_./*-]+' rapport-empreinte-memoire.md rapport-encodage.md rapport-eparsite.md rapport-execution-v41.md rapport-gpt-oss-perplexite.md rap … [436 caractères tronqués]`

  ```
`data/wikitext2_test.txt
`docs/contexte-long.md
[`docs/plan-gpu-topk.md
`docs/plan-gpu-topk.md
docs/plan-gpu-topk.md
docs/programme-recherche.md
drave-core/Cargo.toml
`drave-core/gpu/drave_gpu.cu
drave-core/target/release/drave
`models/Qwen2.5-0.5B-Q4_0.gguf
models/Qwen2.5-0.5B-Q4_0.gguf
models/Qwen2.5-0.5B-Q8_0.gguf
[`reports/rapport-gpu-scores.md
`reports/rapport-gpu-topk-selection.md
`src/bpe_np.py
`src/engine.rs
`src/gguf.rs
`src/list.rs
`src/main.rs
`src/model.rs
src/models/deepseek4.cpp
`src/tokenizer.rs
`src/transformer_np.py
`tools/analyse_experts_statique.py
`tools/compare_logits.py
tools/compare_logits.py
tools/convertir_clusters.py
`tools/inventaire_modeles_lourds.sh
tools/make_patch.py
`tools/mla_synthetique.py
`tools/pair_factice.py
`tools/portes_formats.sh
`tools/*.py
`tools/ref_logits.cpp
  ```

### 🤖 Assistant

⏵ Building first-occurrence line numbers for the term list.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && cat > /tmp/files.txt <<'EOF'\nrapport-empreinte-memoire.md\nrapport-encodage.md\nrapport-eparsite.md\nrapport-execution-v41.md\nrapport-gpt-oss-perplexite.md\nrapport-gpu-scores.md\nrapport-gpu-topk-selection.md\nrapport-grap … [2354 caractères tronqués]`

  ```
AER                          ABSENT
KV                           rapport-empreinte-memoire.md:246
MoE                          rapport-empreinte-memoire.md:242
MLA                          rapport-empreinte-memoire.md:243
GGUF                         rapport-inference.md:22
DRVF                         ABSENT
NLL                          rapport-gpt-oss-perplexite.md:76
RSS                          rapport-execution-v41.md:18
VRAM                         rapport-empreinte-memoire.md:473
TLB                          ABSENT
NUMA                         rapport-mur-memoire-4bits.md:48
AVX2                         rapport-inference.md:120
AVX-512                      rapport-mur-memoire-4bits.md:205
PTX                          rapport-gpu-topk-selection.md:113
MXFP4                        rapport-gpt-oss-perplexite.md:6
Q4_K                         rapport-mla-experts.md:55
Q6_K                         rapport-mla-experts.md:55
IQ2_XXS                      rapport-empreinte-memoire.md:527
IQ1_S                        rapport-mla-experts.md:61
IQ3_XXS                      rapport-mla-experts.md:61
IQ4_XS                       rapport-mla-experts.md:63
Q3_K                         rappo
… [8647 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Locating environment variables and remaining terms.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && for t in DRAVE_TRACE_EXPERTS DRAVE_GPU_TOPK DRAVE_GPU_KV DRAVE_GPU DRAVE_MMAP DRAVE_CLUSTERS DRAVE_PRELIRE_TOUT DRAVE_YARN_MSCALE DRAVE_YARN DRAVE_DEBUG_MLA DRAVE_DEBUG_ETAT 'noaux_tc' 'IQ1_M' 'O_DIRECT' 'vpmaddwd' 'atom.shar … [382 caractères tronqués]`

  ```
DRAVE_TRACE_EXPERTS    rapport-decoupage-moe.md:20:1. **Trace de routage dans le moteur** — `DRAVE_TRACE_EXPERTS=<chemin>` écrit une
DRAVE_GPU_TOPK         rapport-gpu-topk-selection.md:169:`DRAVE_GPU_TOPK=1` (opt-in) qui enchaîne les quatre noyaux sur le miroir et ne
DRAVE_GPU_KV           rapport-architecture-memoire.md:228:`DRAVE_GPU_KV` — qui répartit le cache KV sur les deux cartes — en bénéficie sans
DRAVE_GPU              rapport-architecture-memoire.md:228:`DRAVE_GPU_KV` — qui répartit le cache KV sur les deux cartes — en bénéficie sans
DRAVE_MMAP             rapport-lecteur-multifichiers.md:182:| lu en entier (`DRAVE_MMAP=0`) | 30,68 s | 19,20 Go |
DRAVE_CLUSTERS         rapport-lecteur-multifichiers.md:125:Défaut **bloquant et silencieux**, trouvé par la revue déléguée : `DRAVE_CLUSTERS`
DRAVE_PRELIRE_TOUT     rapport-execution-v41.md:19:| passe avant (`--ppl`) | `DRAVE_PRELIRE_TOUT=1 DRAVE_GPU=1` | **refusée en 0,33 s**, RSS 47 Mo |
DRAVE_YARN_MSCALE      rapport-drapeaux-ignores.md:116:| `DRAVE_YARN` · `DRAVE_YARN_NON` · `DRAVE_YARN_MSCALE` | `Model::load` (1218-1224) | — (prioritaires sur `--sans-yarn`, qui s'applique après le chargement) | ✅ |
DRAVE_YARN             r
… [4477 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Re-checking those terms only within the 20 target files.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && F=$(cat /tmp/files.txt | tr '\\n' ' ') && for t in DRAVE_TRACE_EXPERTS DRAVE_GPU_TOPK DRAVE_GPU_KV DRAVE_GPU DRAVE_MMAP DRAVE_CLUSTERS DRAVE_PRELIRE_TOUT DRAVE_YARN_MSCALE DRAVE_YARN DRAVE_DEBUG_MLA DRAVE_DEBUG_ETAT noaux_tc  … [447 caractères tronqués]`

  ```
DRAVE_TRACE_EXPERTS    rapport-empreinte-memoire.md:19:(`DRAVE_TRACE_EXPERTS`), pas d'estimations.
DRAVE_GPU_TOPK         rapport-gpu-topk-selection.md:169:`DRAVE_GPU_TOPK=1` (opt-in) qui enchaîne les quatre noyaux sur le miroir et ne
DRAVE_GPU_KV           rapport-gpu-topk-selection.md:179:| **GPU** (`DRAVE_GPU=1 DRAVE_GPU_KV=1 DRAVE_GPU_TOPK=1`) | **9,4162** | 41,45 s |
DRAVE_GPU              rapport-execution-v41.md:19:| passe avant (`--ppl`) | `DRAVE_PRELIRE_TOUT=1 DRAVE_GPU=1` | **refusée en 0,33 s**, RSS 47 Mo |
DRAVE_MMAP             rapport-lecteur-multifichiers.md:182:| lu en entier (`DRAVE_MMAP=0`) | 30,68 s | 19,20 Go |
DRAVE_CLUSTERS         rapport-lecteur-multifichiers.md:125:Défaut **bloquant et silencieux**, trouvé par la revue déléguée : `DRAVE_CLUSTERS`
DRAVE_PRELIRE_TOUT     rapport-execution-v41.md:19:| passe avant (`--ppl`) | `DRAVE_PRELIRE_TOUT=1 DRAVE_GPU=1` | **refusée en 0,33 s**, RSS 47 Mo |
DRAVE_YARN_MSCALE      rapport-gpt-oss-perplexite.md:187:maintenant les activer séparément (`DRAVE_YARN_MSCALE`).
DRAVE_YARN             rapport-gpt-oss-perplexite.md:187:maintenant les activer séparément (`DRAVE_YARN_MSCALE`).
DRAVE_DEBUG_MLA        rapport-mla-expert
… [4980 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying exact wording of the key contradictory lines.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && for spec in \"rapport-empreinte-memoire.md:7,10\" \"rapport-empreinte-memoire.md:200,210\" \"rapport-empreinte-memoire.md:295,297\" \"rapport-empreinte-memoire.md:369,379\" \"rapport-empreinte-memoire.md:437,439\" \"rapport-e … [979 caractères tronqués]`

  ```
=== rapport-empreinte-memoire.md [7,10]
**Résultat principal** : l'empreinte de V4.1 tombe de 365,7 Go à **50–80 Go**,
non pas en découpant les experts mais parce que **56 % du modèle (203 Go) est une
table d'engram creuse par nature**, qu'il suffit de mmapper. Une session de
10 000 jetons n'en touche que **4,6 Mo**.
=== rapport-empreinte-memoire.md [200,210]
**Aucune différence.** Cibler « les extrêmes » n'apporte rien. Une exception,
mais à la sortie seulement :

| couche | 90 % | 99 % |
|---|---|---|
| **47** | **36** | 64 |
| 0 | 74 | 108 |

**Le top-k minimal d'un cache utile est le top-k du routeur** : en dessous de 8
experts, un cache ne sert **à rien** (0 % de succès — un jeton consomme ses 8
experts d'un coup).
=== rapport-empreinte-memoire.md [295,297]
**Facteur 4 à 8 sur le hasard.** Un cache « experts du jeton précédent » — 8
entrées, prédiction gratuite — sert 27 à 52 % des appels. Mais un LRU de 32 fait
**78 %** : la localité temporelle est réelle et insuffisante.
=== rapport-empreinte-memoire.md [369,379]
Et la réductibilité n'est pas répartie uniformément :

| | experts pour 90 % |
|---|---|
| couches 0-3 (**entrée**) | **75 à 82** — les moins réductibles |
| couche
… [9331 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Final spot-checks before writing the inventory.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && sed -n '12,15p;57,67p' rapport-mla-experts.md && echo \"--- mla 92-100\" && sed -n '92,100p' rapport-mla-experts.md && echo \"--- gpu-topk 59,63\" && sed -n '59,63p' rapport-gpu-topk-selection.md && echo \"--- empreinte 282,2 … [209 caractères tronqués]`

  ```
| V4-Flash, V4.1 | `tenseur blk.3.attn_q.weight absent` | attention MLA à rang faible |
| GLM-5.3, Kimi | `mélanges d'experts chargés : 0/79` | formats d'experts IQ sans noyau |
| GLM-5.3 | `projection sans aucun format` | FFN dense des 3 premières couches |
| V4, GLM-Flash | *(rien : ça tournait)* | hyper-connexions, index, sortie à rang faible |
mélange quatre sur cinq couches :

| couche | `ffn_down_exps` | `ffn_gate_exps` |
|---|---|---|
| 53 couches | IQ3_XXS | IQ1_S |
| 22 couches | IQ3_XXS | IQ2_XXS |
| 4 couches | **IQ4_XS** | IQ1_S |
| 1 couche | **Q3_K** | IQ2_XXS |

D'où « 71/79 » : les 5 couches fautives étaient exactement celles qui
introduisaient IQ4_XS et Q3_K, et rien ne le disait.
--- mla 92-100
- **GLM-5.3 (216 Go)** : 79 couches MLA, 76/79 mélanges d'experts chargés (les
  3 autres sont denses, c'est le modèle), ~85 Go de RSS au chargement, dont
  ~52 Go de tenseurs MLA déquantifiés en f32 — un coût réel, pas un détail :
  ces huit tenseurs par couche ne sont pas empruntés au fichier.
- **Kimi-K2.7 (1 026 G poids)** : `--config` annonce « calculable : oui »,
  61 couches MLA, routage sigmoïde ×2,827, 384 experts dont 8 par jeton.
- **Portes inchangées au bit près
… [1772 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Writing the inventory, then sending it to the parent agent.

## A. Termes et sigles

**Sigles, modèles, algorithmes**

- **ALM** (Adaptive Logic Module) — brique logique élémentaire du FPGA Stratix V, comptée pour dimensionner les voies MAC ; utilisé dans `rapport-eparsite.md`/`rapport-minimal.md` (projection carte) ; première occurrence `reports/rapport-eparsite.md:64`.
- **AVX2** (Advanced Vector Extensions 2) — jeu d'instructions SIMD x86 utilisé par les noyaux `q8_dot_avx2` et le noyau 4 bits ; `src/engine.rs`/`src/gguf.rs` ; première occurrence `reports/rapport-inference.md:120`.
- **AVX-512** — extension SIMD évoquée comme noyau futur qui « paierait mieux » le 4 bits ; `reports/rapport-mur-memoire-4bits.md:205`.
- **BitNet b1.58** — modèle ternaire *entraîné* (et non quantifié après coup), cité comme référence de densité 50-70 % de non-nuls ; `reports/rapport-eparsite.md:70`.
- **BLAS** — bibliothèque d'algèbre linéaire ; le moteur revendique « sans BLAS » ; `reports/rapport-inference.md:1`.
- **BPE** (Byte Pair Encoding) — algorithme du tokenizer Qwen2 réimplémenté en Rust (`src/tokenizer.rs`) ; `reports/rapport-inference.md:22`.
- **CDC** — sigle non développé dans les rapports, associé à un encodage « CSR/plan » et à la « référence CDC » (dense ternaire) ; `reports/rapport-encodage.md:42`.
- **CSA** (Compressed Sparse Attention) — une des trois attentions compressées de V4.1 (`build_csa_lid_attention`), sélection de candidats par blocs ; `reports/rapport-execution-v41.md:37`.
- **CSR** (Compressed Sparse Row) — encodage creux indexé, disqualifié par la mesure (« piège chiffré ») ; `src/list.rs` ; `reports/rapport-encodage.md:12`.
- **CUDA** — API GPU NVIDIA ; `drave-core/gpu/drave_gpu.cu`, `cuda_stub.h` ; `reports/rapport-gpu-scores.md:70`.
- **DDR3** — mémoire de la carte FPGA mesurée à 9,66 Go/s, goulot du projet ; `reports/rapport-minimal.md:59`.
- **DSA** — indexeur d'attention creuse de DeepSeek (architecture `glm-dsa`), inactif sous `index_topk = 2048` ; `reports/rapport-mla-experts.md:124`.
- **DSP** (Digital Signal Processor / bloc multiplieur dur) — bloc matériel que le projet s'interdit (« aucun DSP ») ; `reports/rapport-encodage.md:74`.
- **DenseQ4** — forme interne 4 bits (nibbles signés biaisés, échelle `u16` par bloc de 32) ; `reports/rapport-mur-memoire-4bits.md:87`.
- **DenseQ8** — noyau dense int8 avec échelles par bloc, évoqué comme chantier d'échelles ; `reports/rapport-gpt-oss-perplexite.md:252`.
- **FPGA** — cible matérielle du projet (Stratix V GS D5) ; `reports/rapport-eparsite.md:64`.
- **Gini** — indice de concentration du routage d'experts par couche ; `reports/rapport-empreinte-memoire.md:194`.
- **GQA** (Grouped-Query Attention) — attention groupée de Qwen2 (14 têtes de requête / 2 KV, groupement 7:1) ; `src/model.rs` ; `reports/rapport-inference.md:34`.
- **HCA** — attention compressée simple de V4.1 (`build_hca_attention`) ; `reports/rapport-execution-v41.md:37`.
- **IQ1_M / IQ1_S / IQ2_XXS / IQ3_XXS / IQ4_XS / Q3_K / Q4_K / Q6_K** — types de super-blocs ggml quantifiés (256 poids) que le moteur doit déquantifier ; `Source::Dequant`, `tools/portes_formats.sh` ; première occurrence `reports/rapport-empreinte-memoire.md:527` (IQ1_M/IQ2_XXS), `reports/rapport-mla-experts.md:55` (Q4_K/Q6_K).
- **Jaccard** — indice de recouvrement d'ensembles d'experts entre couches, langues ou occurrences d'un token ; `reports/rapport-empreinte-memoire.md:114`.
- **KV** (clé/valeur) — cache d'attention ; miroir VRAM `DRAVE_GPU_KV`, compresseur/indexeur KV ; `reports/rapport-empreinte-memoire.md:246`.
- **LID** — variante « à candidats » de la CSA (`candidate_topk_blocks = 2048`) ; `reports/rapport-execution-v41.md:37`.
- **LRU** (Least Recently Used) — politique d'éviction du cache d'experts (32 entrées → 78 % de succès) ; `reports/rapport-empreinte-memoire.md:296`.
- **LUT** (Look-Up Table) — ressource logique du FPGA ; l'activation à index arbitraire coûte « ~21 LUT pour un 64:1 » ; `reports/rapport-encodage.md:73`.
- **MAC** (Multiply-Accumulate) — voie de calcul ; « ~312 voies de MAC » saturent la DDR3 ; `reports/rapport-minimal.md:61`.
- **M20K** — banc de mémoire interne du FPGA, point dur de la collecte d'activation irrégulière ; `reports/rapport-encodage.md:77`.
- **MLA** (Multi-head Latent Attention) — attention à quatre projections de rang faible et cache latent (DeepSeek/GLM/Kimi) ; `src/model.rs` ; `reports/rapport-empreinte-memoire.md:243`.
- **MoE** (Mixture of Experts) — mélange d'experts routé par top-k ; `reports/rapport-empreinte-memoire.md:242`.
- **MTok/s / GFLOPS / Gbit/s** — absents des 20 fichiers.
- **MXFP4** — format microscaling 4 bits de gpt-oss, noyau GPU « warp par ligne » bit à bit identique au CPU ; `reports/rapport-gpt-oss-perplexite.md:6`.
- **NLL** (Negative Log-Likelihood) — perte par position, en nats, utilisée pour comparer deux moteurs ; `tools/compare_logits.py` ; `reports/rapport-gpt-oss-perplexite.md:76`.
- **N:M structuré (2:4)** — motif d'élagage matériellement supporté (2 non-nuls sur 4) ; `reports/rapport-eparsite.md:19`.
- **NUMA** — effet d'architecture mémoire invoqué pour expliquer une mesure de pull bruyante ; `reports/rapport-mur-memoire-4bits.md:48`.
- **PE** (Processing Element) — unité de calcul du FPGA ; « ses 14 blocs » vs « 1 792 blocs » côté GPU, et « un banc FPGA à 124 MHz × 32 PEs » ; `reports/rapport-empreinte-memoire.md:19` / `reports/rapport-inference.md:194`.
- **PPL** — abréviation de perplexité utilisée dans les tableaux ; `reports/rapport-gpu-topk-selection.md:271`.
- **PTX** — assembleur virtuel NVIDIA, généré par `cuda_stub.h` (absence de `__float_as_uint` → plus de PTX) ; `reports/rapport-gpu-topk-selection.md:113`.
- **PushMat** — encodage de liste « écart + valeur int8 » de `src/list.rs` (mode push) ; `reports/rapport-inference.md:31`.
- **ReLU** — activation à zéro franc utilisée par PowerInfer/TurboSparse, opposée au SiLU du projet ; `reports/rapport-eparsite.md:8`.
- **RMSNorm** — normalisation par racine du carré moyen (Qwen2, hyper-connexions de V4.1) ; `src/model.rs` ; `reports/rapport-execution-v41.md:34`.
- **RoPE** (Rotary Position Embedding) — rotation positionnelle ; `rope_yarn`, `attn_derope` ; `reports/rapport-gpt-oss-perplexite.md:91`.
- **RSS** (Resident Set Size) — mémoire résidente maximale mesurée ; `reports/rapport-execution-v41.md:18`.
- **SHA-256** — empreinte servant à vérifier les 1 587 tenseurs convertis ; `tools/convertir_clusters.py` ; `reports/rapport-lecteur-multifichiers.md:11`.
- **SiLU** — activation lisse (`silu`) du greffon et du MLP Qwen ; `reports/rapport-harnais.md:14`.
- **SIGABRT** — signal de mort du client réseau sur réponse de mode/taille différents ; `reports/rapport-mode4-lot-listes.md:90`.
- **Sinkhorn** — normalisation itérative (20 itérations) des hyper-connexions de V4.1 ; `build_hc_sinkhorn` ; `reports/rapport-execution-v41.md:34`.
- **SparseGPT / Wanda** — méthodes d'élagage *one-shot* citées pour situer la limite des 50-60 % ; `reports/rapport-eparsite.md:71`.
- **SWAR** (SIMD Within A Register) — décodeurs d'écarts de `src/engine.rs` ; `reports/rapport-inference.md:32`.
- **SwiGLU** — forme de MLP (gate × up) utilisée pour le greffon `a = silu(u·x)·(v·x)` ; `src/model.rs` ; `reports/rapport-greffon.md:12`.
- **TLB** — absent des 20 fichiers.
- **top-k / top-1 / top-8 / top-6 / top-40** — sélection des k plus grands scores : routage d'experts, sélection d'attention, échantillonnage ; `--attn-topk`, `--act-topk` ; première occurrence `reports/rapport-empreinte-memoire.md:208` ; top-40 à `reports/rapport-inference.md:39`.
- **TurboSparse** — modèle PowerInfer entraîné à ≈ 90 % de creux ; `reports/rapport-localite-activation.md:17`.
- **TTFT** (Time To First Token) — 74–95 ms mesurés ; `reports/rapport-inference.md:83`.
- **varint** — encodage d'écart à longueur variable des listes d'événements ; `reports/rapport-inference.md:112`.
- **VRAM** — mémoire des cartes ; miroirs KV/top-k, cache d'experts ; `reports/rapport-empreinte-memoire.md:473`.
- **warp** — unité d'exécution GPU (noyau MXFP4 « warp par ligne »), et index de tête dans `attn_kv_recombine` ; `reports/rapport-gpu-topk-selection.md:219`.
- **YaRN** — extension de contexte RoPE avec interpolation basse fréquence + température `mscale = 1 + 0,1·ln f` ; `rope_yarn` ; `reports/rapport-gpt-oss-perplexite.md:13`.

**Formats, fichiers, artefacts**

- **cluster-XX.gguf / commun.gguf** — artefacts du format « modèle éclaté » (métadonnées + 8 clusters d'experts) ; `tools/convertir_clusters.py` ; `reports/rapport-lecteur-multifichiers.md:19`.
- **GGUF** — format de conteneur de modèle lu par `src/gguf.rs` (`Gguf::open`, `Gguf::open_meta`) ; `reports/rapport-inference.md:22`.
- **mapping.tsv** — table `expert global → (fichier, ligne locale)` produite par le convertisseur (6 144 entrées) ; `reports/rapport-lecteur-multifichiers.md:226` (et `:240`).
- **mmap** — mappage mémoire des poids (défaut, `DRAVE_MMAP=0` pour revenir à `read_to_end`) ; `reports/rapport-empreinte-memoire.md:9`.
- **QPAT** — en-tête binaire du fichier greffon `QPAT | version | couche | n | u[n] | v[n] | d[n]` ; `tools/make_patch.py`, `--patch` ; `reports/rapport-greffon.md:19`.
- **shard** — fichier d'un GGUF découpé (V4-Flash en 3 shards, Kimi en 8, GLM en 6) ; `reports/rapport-lecteur-multifichiers.md:30`.
- **Q4_0 / Q4_1 / Q8_0 / F16 / F32 / I8** — types de tenseurs ggml déquantifiés/importés verbatim ; `src/gguf.rs` ; première occurrence `reports/rapport-gpu-topk-selection.md:45` (Q4_0) et `reports/rapport-empreinte-memoire.md:251` (I8).
- **O_DIRECT** — ouverture directe échouant ici (errno 29), donc régime froid non mesuré ; `reports/rapport-empreinte-memoire.md:494`.
- **pread** — lecture positionnelle dont le retour non vérifié a produit le faux 2 211 Go/s ; `reports/rapport-empreinte-memoire.md:493`.
- **JSON `<arch>.config`** — bloc de configuration lu dans le GGUF (40 couches, 384 experts de V4.1) ; `reports/rapport-execution-v41.md:47`.

**Matériel et machines**

- **DDR3 / PCIe x8 / fmax 124 MHz** — débits et fréquence mesurés de la carte Stratix V GS D5 ; `reports/rapport-minimal.md:59`.
- **NVMe** — support de chargement à la demande (aléatoire 5,5 Go/s), seul retenu ; `reports/rapport-empreinte-memoire.md:299`.
- **Quadro RTX 5000 / RTX 5000** — cartes GPU de mesure (« 2 Quadro, 32 Go » vs « deux RTX 5000, 32 Go ») ; `reports/rapport-empreinte-memoire.md:473` et `reports/rapport-localite-activation.md:62`.
- **Stratix V GS D5** — FPGA cible ; `reports/rapport-minimal.md:57`.
- **Xeon E5-2687W v3** — CPU de mesure (2 ×, 20 cœurs / 40 CPU logiques) ; `reports/rapport-inference.md:5`.
- **HBM** — absent des 20 fichiers.

**Vocabulaire du projet**

- **aiguillage** — remplacement de `matvec_q4` par un dispatch par format ; `reports/rapport-mla-experts.md:99`.
- **capteur hebbien / hebbien** — profileur de co-activations entrée→sortie (`--hebbian`), dont la conclusion est qu'un nœud linéaire est redondant ; `reports/rapport-greffon.md:21`.
- **densité d'activation** — proportion de neurones « tirés » (seuil à 5 % du max) ; `--profil-neurones` ; `reports/rapport-localite-activation.md:43`.
- **débit variable** — débit qui dépend du nombre d'événements par token (quasi constant sur un transformer dense) ; `reports/rapport-harnais.md:41`.
- **DRVF v5** — absent des 20 fichiers (seul « mode 4 = protocole v5 » n'apparaît pas ici).
- **engram** — table creuse à accès aléatoire par n-grammes (`blk.N.engram_embd.weight`), 203,4 Go de V4.1, destinée au mmap ; `reports/rapport-empreinte-memoire.md:9`.
- **expert partagé (shexp)** — FFN toujours actif (`ffn_*_shexp.weight`) qui n'était jamais calculé ; `vue_unique` ; `reports/rapport-mla-experts.md:128-131`.
- **grappe** — groupe de destinations/experts (grappes afférentes/efférentes), unité de chargement et de découpage ; `reports/rapport-empreinte-memoire.md:15`.
- **greffon** — neurone ajouté à une couche sans réentraînement (`--patch`) ; `reports/rapport-greffon.md:12`.
- **hyper-connexion** — état résiduel en `hc = 4` copies mélangées par Sinkhorn, non implémenté ; `hc_mult`, `hc_sinkhorn_iters` ; `reports/rapport-execution-v41.md:34`.
- **liste valuée / aiguille** — absents des 20 fichiers (l'encodage équivalent est ici `PushMat` / listes signées).
- **mode 2** — un flux par jeton, encodage « listes » avec perte (1 608 octets/flux) ; `reports/rapport-mode4-lot-listes.md:12`.
- **mode 3** — lot dense `t × dimension × f32`, sans perte (3 663 octets/jeton) ; `reports/rapport-mode4-lot-listes.md:10`.
- **mode 4** — lot en listes auto-délimitées par préfixe de 12 octets `a_j · n_blocs_j · longueur_j` ; `reports/rapport-mode4-lot-listes.md:11`.
- **n-gramme** — motif jusqu'à 4 tokens indexant l'engram (hâchage à 48 nombres premiers, vocabulaire comprimé 99 092) ; `reports/rapport-empreinte-memoire.md:259`.
- **paire** — un flux/destination d'événement : en modes 1 et 2, `n` compte des PAIRES (indice + valeur) ; `tools/pair_factice.py` ; `reports/rapport-mode4-lot-listes.md:82`.
- **poids aberrants** — hétérogénéité massive de magnitude (95,9 % des poids d'`attn_output` sous 5 % du max) ; levier de SparseGPT, pas de la clustérisation ; `reports/rapport-modele-reel.md:64`.
- **porte / porte de correction / porte de non-régression** — valeur de perplexité de référence servant de test (19,3885 ; 15,1757 ; 15,2789 ; 799,8557 ; 268 786,6218) ; `reports/rapport-empreinte-memoire.md:45`.
- **pull** — mode d'exécution qui parcourt les lignes de la matrice (produit scalaire), opposé au push ; `seuil_push = 0,22` ; `reports/rapport-inference.md:32`.
- **push** — mode d'exécution par dispersion d'événements dans un accumulateur ; `reports/rapport-inference.md:32`.
- **SparseVec** — vecteur creux du chemin par listes d'événements ; `reports/rapport-localite-activation.md:24`.

**Variables d'environnement et drapeaux**

- **DRAVE_TRACE_EXPERTS** — écrit les traces de routage réelles d'experts ; `reports/rapport-empreinte-memoire.md:19`.
- **DRAVE_GPU / DRAVE_GPU_KV / DRAVE_GPU_TOPK** — déport des projections, miroir KV en VRAM, top-k d'attention déporté (opt-in) ; `reports/rapport-execution-v41.md:19`, `reports/rapport-gpu-topk-selection.md:179`, `:169`.
- **DRAVE_MMAP=0** — désactive le mmap au profit de `read_to_end` ; `reports/rapport-lecteur-multifichiers.md:182`.
- **DRAVE_CLUSTERS** — restreint les clusters chargés (nœud partiel) ; `reports/rapport-lecteur-multifichiers.md:125`.
- **DRAVE_PRELIRE_TOUT=1** — active la prélecture de tous les poids ; `reports/rapport-execution-v41.md:19`.
- **DRAVE_YARN_MSCALE / DRAVE_YARN=1** — activation séparée de la température YaRN / retour au YaRN de référence ; `reports/rapport-gpt-oss-perplexite.md:187`, `:209`.
- **DRAVE_DEBUG_MLA=1 / DRAVE_DEBUG_ETAT=1** — impression étagée des tenseurs MLA et de l'état ; `reports/rapport-mla-experts.md:146`, `:187`.
- **--dense / --q4 / --q4-attn / --q4-tout / --q4-ffn / --keep / --lot / --flux-blocs / --limit / --logits-bin / --ppl-profil / --infer / --pbl / --banc-topk / --attn-topk / --act-thresh / --abits / --threads / --ctx / --patch / --tensor(s) / --config / --materiel / --sonder-engram** — drapeaux CLI cités ; première occurrence dispersée, ex. `--q4` à `reports/rapport-mur-memoire-4bits.md:198`, `--logits-bin` à `reports/rapport-logits-gpu-vs-cpu.md:27`, `--ppl-profil` à `reports/rapport-gpt-oss-perplexite.md:215`.

**Absents des 20 fichiers (demandés mais non trouvés)** : AER, DRVF/v5, TLB, HBM, LoRA, MTP, Hadamard, GFLOPS, Gbit/s, MTok/s, « liste valuée », « aiguille »/`tools/aiguille.py`, TSV (seul `mapping.tsv` existe), FIM.

## B. Chiffres et affirmations mesurées

**reports/rapport-empreinte-memoire.md**
- `reports/rapport-empreinte-memoire.md:3-5` — «Modèle d'étude : Qwen3-30B-A3B (48 couches, 128 experts, top-8) [...] Cible : DeepSeek-V4.1-Flash (40 couches, **384 experts**, top-6, 365,7 Go)».
- `reports/rapport-empreinte-memoire.md:7-10` — «l'empreinte de V4.1 tombe de 365,7 Go à **50–80 Go** [...] **56 % du modèle (203 Go) est une table d'engram creuse par nature** [...] Une session de 10 000 jetons n'en touche que **4,6 Mo**».
- `reports/rapport-empreinte-memoire.md:27-30` — «| 64 experts | 59,64 | 51,69 | 5,31 | [...] | **1 expert** | **0,40** | **0,21** | **0,04** |» (volume lu par appel utile, Go, selon cache 16/32/64).
- `reports/rapport-empreinte-memoire.md:36-46` — «| 0 (référence) | **7,6139** | — | [...] | 0,25 | 727 099,03 | ×95 500 |» ; «Seulement 12,5 % des neurones tirent, et les 10 % les plus lourds portent 82 à 86 % de la masse».
- `reports/rapport-empreinte-memoire.md:49-50` — «« projections : 0,0 M événements par token ». La sparsité est calculée et jetée.»
- `reports/rapport-empreinte-memoire.md:54-65` — «Tokenisation de 8,3 Mo de français (3 050 991 jetons) [...] | 3 050 991 | **19 793** | **13,03 %** |» ; «Exposant de Heaps ≈ **0,21**».
- `reports/rapport-empreinte-memoire.md:71-76` — «| complète (151 936 tokens) | **25,3748** | [...] | restreinte aux 19 793 tokens français | **24,3108** |».
- `reports/rapport-empreinte-memoire.md:82-90` — «| rang médian du vrai token | **3** | [...] | p90 | 250 | [...] | maximum | 4 319 |» ; «| **top-16 384** | **100,0 %** |».
- `reports/rapport-empreinte-memoire.md:94-104` — «Sur 127 positions d'un texte français : **top-1 français dans 126 cas (99,2 %)**. Masse hors vocabulaire français : médiane **0,44 %**, mais maximum 40,4 %» ; «| 0 | 1 087 | **20 212** | 50 999 | [...] | 126 | 1 | **2** | 4 |».
- `reports/rapport-empreinte-memoire.md:116-127` — «| français / anglais | 0,752 | **r = 0,102** | [...] | **français / français** (référence interne) | **0,805** | r = 0,995 |» ; «Experts « propres » à une langue : **1,7 à 3,1 %**» ; «un classifieur par plus proche voisin reconnaît le corpus d'origine dans **79,8 %** des cas».
- `reports/rapport-empreinte-memoire.md:136-142` — «| couche | 0 | 8 | 20 | 36 | [...] | Jaccard | **0,499** | 0,088 | 0,056 | 0,065 |».
- `reports/rapport-empreinte-memoire.md:148-152` — «| couches extrêmes (0-3, 44-47) | **0,259** | [...] | couches médianes (20-27) | **0,056** |» ; «**Facteur 4,6** [...] L'entrée est plus marquée que la sortie (0,499 contre 0,349).»
- `reports/rapport-empreinte-memoire.md:158-163` — «| 0 / 47 | 0,030 | [...] | 1 / 46 | 0,028 | [...] | voisines (l, l+1) | 0,034 |».
- `reports/rapport-empreinte-memoire.md:169-184` — «| 1 à 11 | ~0,035 | [...] | **12** | **0,323** | [...] | **24** | **0,210** |» ; «16/28 : 0.549 [...] 19/31 : 0.461» ; «**32–55 %**».
- `reports/rapport-empreinte-memoire.md:196-210` — «| couches extrêmes | 60,0 | 92,2 | 0,575 |» ; «| **47** | **36** | 64 | / | 0 | 74 | 108 |» ; «en dessous de 8 experts, un cache ne sert **à rien** (0 % de succès)».
- `reports/rapport-empreinte-memoire.md:216-221` — «| 16 | 2,34 Go | 59,6 % | 59,6 % | −0,0 % | [...] | 48 | 7,03 Go | 89,4 % | 90,6 % | +1,2 % |».
- `reports/rapport-empreinte-memoire.md:227-231` — «| aucun (à froid) | 77,9 % | 78,5 % |» ; «Le cache atteint son régime en **32 jetons** (59 % à 8 jetons, 80,5 % à 32)».
- `reports/rapport-empreinte-memoire.md:241-251` — «| **engram** | **203,4** | **55,6 %** | / experts (MoE) | 152,9 | 41,8 % | / attention (MLA) | 5,4 | 1,5 % |» ; «**`blk.N.engram_embd.weight`, à 101,4 Go par couche** [...] en I8, de forme `[384 006 168, 264]`».
- `reports/rapport-empreinte-memoire.md:257-264` — «| entrées | 384 006 168 par couche | [...] | taille d'une entrée | 264 octets | [...] | hâchage | 48 nombres premiers | [...] | vocabulaire comprimé | 99 092 |».
- `reports/rapport-empreinte-memoire.md:272-280` — «| 10 000 | 1 462 | 3 953 | 5 596 | 6 265 | 17 276 | 4,6 Mo | [...] | 3 050 991 | 19 793 | 227 495 | 556 188 | 880 394 | 1 683 870 | **444,5 Mo** |» ; «Le rapport est de 1 pour 22 000».
- `reports/rapport-empreinte-memoire.md:290-297` — «| 12 | **49,8 %** | 6,2 % | [...] | 47 | **51,9 %** | 6,2 % |» ; «Un cache « experts du jeton précédent » — 8 entrées [...] sert 27 à 52 % des appels. Mais un LRU de 32 fait **78 %**».
- `reports/rapport-empreinte-memoire.md:303-314` — «| 47 | **30,8** | 99,6 |» ; «Sur NVMe [...] lire 8 experts dispersés coûte exactement ce qu'ils pèsent» ; «(0,06 Go/s en aléatoire)».
- `reports/rapport-empreinte-memoire.md:318-321` — «Le calcul d'une couche coûte **0,6 ms**, sa lecture **10,9 ms** : un rapport de **18×** [...] ne masquerait que **6 %** de l'attente.»
- `reports/rapport-empreinte-memoire.md:325-348` — «Les 28 sessions du `journal/` (59 Mo, 2,5 M jetons)» ; «| **journal** (notre usage) | 16,9 | 30,8 | 41,6 | **58,1** | 92,5 |» ; «| **anglais** | **11,4** | **23,0** | **31,6** | **44,5** | **72,7** |» ; «l'anglais demande **44,5 experts pour 90 %** contre 59,3 pour le français [...] **18 Go d'écart**».
- `reports/rapport-empreinte-memoire.md:352-367` — «| **47** | **50** | **36** | 52 | / | **moyenne** | **58,1** | 59,3 | **44,5** |» ; «Il s'en écarte surtout aux **dernières couches** (+14 à la couche 47)».
- `reports/rapport-empreinte-memoire.md:371-379` — «| couches 0-3 (**entrée**) | **75 à 82** — les moins réductibles | / | couches 16-30 (milieu) | **42 à 49** — les plus réductibles |».
- `reports/rapport-empreinte-memoire.md:383-392` — «| **2 510 800** (tout le journal) | 1 470 860 | **388 Mo** | **0,38 %** |» ; «le vocabulaire de ce corpus fait **19 228 tokens (12,66 %)**».
- `reports/rapport-empreinte-memoire.md:404-417` — «| 0 | gate | 0,185 | 0,001 | 0 | [...] | 47 | gate | 0,187 | 0,011 | 0 |» ; «~**78 % des colonnes** portent 80 % du poids».
- `reports/rapport-empreinte-memoire.md:425-441` — «| 12/24 | **+0,343** | [...] | 18/30 | **+0,389** | [...] | 24/36 | **+0,312** |» ; «maximum mesuré : 0,49».
- `reports/rapport-empreinte-memoire.md:448-455` — «stocker W(L+12) comme W(L) + résidu | **non** — le résidu porte 88 % de l'énergie |» ; «**piste ouverte** — 35 % de variance partagée à extraire, rang inconnu».
- `reports/rapport-empreinte-memoire.md:461-476` — «experts (top-6 × 40 couches × 9,95 Mo) | **2,39 Go** |» ; «engram (accès par n-gramme) | **~2 Ko** |» ; «tête de sortie (129 280 × 5120, F16) | **1,32 Go — 36 % du trafic** |» ; «base | 3,71 Go |» ; «cache d'experts 25 % (32 par couche) | 1,82 Go |» ; «tête restreinte à la langue | **0,70 Go** |» ; «3 200 experts = 21 % du total | `CacheExperts` existe» ; «un jeton relit 551 424 experts pour 6 144 distincts — **un facteur 90 de relecture**».
- `reports/rapport-empreinte-memoire.md:480-490` — «| VRAM (2 GPU) | ~750 Go/s | 9,7 Go en 13 ms |» ; «| RAM | ~20 Go/s |» ; «| NVMe, aléatoire, blocs 4 Mo | **5,5 Go/s** |» ; «| NVMe, séquentiel | 2,1 Go/s |» ; «| **disque mécanique, aléatoire** | **0,06 Go/s** | 62,9 Go en 1 098 s — **3,5× pire** |» ; «2,39 Go par jeton y coûteraient 40 s».
- `reports/rapport-empreinte-memoire.md:493-495` — «a chronométré ce disque à **2 211 Go/s** [...] `O_DIRECT` échoue par ailleurs ici (errno 29)».
- `reports/rapport-empreinte-memoire.md:499-508` — «| engram (2 couches) | 202,8 Go | **0,4 Go** | **1 / 500** |» ; «| **total** | **365,7 Go** | **~50 à 80 Go** | **1 / 5 à 1 / 7** |».
- `reports/rapport-empreinte-memoire.md:518` — «**Adapter l'empreinte à la langue** : 53 Go en anglais contre 71 en français.»
- `reports/rapport-empreinte-memoire.md:526` — «**La tête restreinte par langue** : −30 % de trafic, le top-1 y est toujours.»
- `reports/rapport-empreinte-memoire.md:534-536` — «un disque mécanique à 2 211 Go/s, une allocation de cache à 4,1 % partout, un total de 4 231 Go».
- `reports/rapport-empreinte-memoire.md:538-540` — «la perplexité restreinte qui *baisse* de 25,37 à 24,31».

**reports/rapport-encodage.md**
- `reports/rapport-encodage.md:8` — «Modèle : MLP 32→64→10 (2688 poids), référence float 76.07 %».
- `reports/rapport-encodage.md:14-29` — tableau des coûts réels b/poids : «| non structuré | 1 | 26.9 % | 45.02 % | 1.27 | **3.52** | 10.03 | 2.00 | 0.90 | 3.6 |».
- `reports/rapport-encodage.md:35-42` — frontière de Pareto : «| 1.04 | 42.87 % | 10.6 | [...] | 1.50 | 72.46 % | 7.4 | [...] | 2.00 | 4971.00 % | 5.5 | dense ternaire (référence CDC) |».
- `reports/rapport-encodage.md:51-57` — coût exact N = 4096 : «| 100.0 % | 2.000 | **2.282** | 0.88× | 4.8 | ×0.88 | [...] | 1.0 % | 1.010 | **0.151** | ×6.71 | 73.3 | ×13.28 |».
- `reports/rapport-encodage.md:59-61` — «**Bascule vers 20 % de densité** [...] (×4,2 à 5 %, ×13 face au dense 2 bits à 1 %)».
- `reports/rapport-encodage.md:69-70` — «~×1,3 à 12,5 %, ×2,2 à 5 %, ×13 face au dense ternaire à 1 %».
- `reports/rapport-encodage.md:78-80` — «à 5 %, l'entropie des positions vaut 0,288 b/poids contre 0,476 pour les listes — il reste un facteur 1,65».
- `reports/rapport-encodage.md:83-84` — «sur un LLM réel, 5-12 % de densité demande un réentraînement lourd».

**reports/rapport-eparsite.md**
- `reports/rapport-eparsite.md:3` — «Modèle minimal (MLP 32→64→10), accuracy float **76.07 %**, ternaire (non élagué) **49.71 %**».
- `reports/rapport-eparsite.md:7-9` — «poids non nuls : **26.3 %** [...] activations non nulles après ReLU : **52.8 %** [...] événements réels (poids ∧ activation) : **13.9 %**».
- `reports/rapport-eparsite.md:13-19` — «| **bitmap + signe** | **1 + d** | **1,50** | **1,25** |» ; «| CSR bloc 16 b | 17·d | 8,50 | 4,25 |».
- `reports/rapport-eparsite.md:29-36` — «| 100.0 % | 26.3 % | 49.71 % | 2.00 | 1.26 | [...] | 3.1 % | 0.9 % | 47.66 % | 2.00 | 1.01 |» ; «| 2:4 struct. | 24.0 % | 48.73 % |».
- `reports/rapport-eparsite.md:40-46` — «| csr32 vs dense2 | 6.1 % | csr32 | [...] | csr16 vs bitmap | 6.2 % | csr16 |».
- `reports/rapport-eparsite.md:50-57` — «| 100.0 % | 5.5 | 5.5 | 0.6 | 0.3 | 7.4 |» ; «| 6.2 % | 5.5 | 10.4 | 10.4 | 5.4 | 7.4 |».
- `reports/rapport-eparsite.md:64` — «~21 LUT pour un 64:1, soit ≈ 3 400 ALM pour 312 voies (**2 % du FPGA**)».
- `reports/rapport-eparsite.md:65` — «Le saut de blocs entièrement nuls (1 bit par bloc de 64) est le premier pas, à 1,6 % de surcoût.»
- `reports/rapport-eparsite.md:69` — «Les variations observées (±4 pt) sont dans le bruit d'un jeu de test de 1 024 exemples — **on ne peut pas conclure**».
- `reports/rapport-eparsite.md:70-71` — «BitNet b1.58 tourne plutôt autour de 50-70 % de non-nuls : le gain du bitmap y serait de ×1,2 à ×1,4» ; «l'élagage non structuré *one-shot* des LLM à 50-60 % [...] **Au-delà de ~90 % de zéros, un LLM généraliste s'effondre**».

**reports/rapport-execution-v41.md**
- `reports/rapport-execution-v41.md:3-4` — «365,71 Go, 1 046 tenseurs, 40 couches, 384 experts dont 6 par jeton».
- `reports/rapport-execution-v41.md:8-9` — «**la passe avant est refusée en 0,33 s** [...] **Aucun chiffre de calcul sur V4.1 n'existe, ici ou ailleurs dans ce dépôt — uniquement des mesures statiques.**»
- `reports/rapport-execution-v41.md:15` — «1 046 tenseurs, **365,70 Go** lus en **63,8 ms**».
- `reports/rapport-execution-v41.md:16` — «**74 ms** au total, aucune donnée lue».
- `reports/rapport-execution-v41.md:17` — «20 threads, 16 lecteurs disque, cache experts 19,5 Go, cache KV 32 bits».
- `reports/rapport-execution-v41.md:18` — «table 1 : 10 000 entrées en **524 ms** (2,6 Mo touchés sur 101,4 Go) · table 2 : **219 ms** · RSS max **120 Mo** pour 365,7 Go adressés».
- `reports/rapport-execution-v41.md:19` — «**refusée en 0,33 s**, RSS 47 Mo».
- `reports/rapport-execution-v41.md:30` — «`llama.cpp/src/models/deepseek4.cpp` (1 253 lignes)».
- `reports/rapport-execution-v41.md:34-37` — «**hc = 4** copies [...] un **Sinkhorn** à 20 itérations» ; «`o_groups = 8`» ; «`candidate_topk_blocks = 2048`».
- `reports/rapport-execution-v41.md:49` — «l'**attention MLA à rang faible** validée contre llama.cpp sur GLM-5.3 (corrélation 0,999024)».
- `reports/rapport-execution-v41.md:70` — «Le moteur refuse donc, et le refuse en 74 ms.»
- `reports/rapport-execution-v41.md:79` — «# 203 Go de tables adressées, 5 Mo touchés».

**reports/rapport-gpt-oss-perplexite.md**
- `reports/rapport-gpt-oss-perplexite.md:3-6` — «corpus `/tmp/wt2_txt.txt` (20 000 premiers octets de `data/wikitext2_test.txt`), gpt-oss-120b MXFP4, `--ctx 256 --dense --threads 16`».
- `reports/rapport-gpt-oss-perplexite.md:10` — «perplexité **39,8** « au lieu de l'ordre de 6 » [...] (39,8 à 63 jetons, 129,9 à 511)».
- `reports/rapport-gpt-oss-perplexite.md:28-29` — «| avant (biais O ignoré) | **39,80** | / | après (biais O chargé) | **20,84** |».
- `reports/rapport-gpt-oss-perplexite.md:44-51` — «| fenêtre une couche sur deux (motif 2, corrigé) | **15,08** |» ; «`[config] fenêtre glissante 128 sur 18/36 couches (motif 2 alterné)`».
- `reports/rapport-gpt-oss-perplexite.md:60` — «20,8361 avant, 20,8361 après, au chiffre près».
- `reports/rapport-gpt-oss-perplexite.md:72-78` — «| 63 jetons, YaRN | **38,37** | **41,11** |» ; «| 511 jetons, YaRN, une seule fenêtre de 512 | **169,67** | **174,34** |» ; «corrélation des logits **0,999976** [...] \|ΔNLL\| médian 0,076, max 1,49».
- `reports/rapport-gpt-oss-perplexite.md:91-92` — «| RoPE simple (défaut du moteur) | **20,84** | **18,58** | / | YaRN ×32 | 41,11 | 174,34 |».
- `reports/rapport-gpt-oss-perplexite.md:99` — «**0,27 % d'écart au plus sur une fréquence, aucun sur les 18 autres**».
- `reports/rapport-gpt-oss-perplexite.md:105` — «la concentration `0,1·ln(32)+1`».
- `reports/rapport-gpt-oss-perplexite.md:127-134` — «| `analysis` | **0,9999** | / | `final` | 0,0001 |» ; «NLL 13,4 pour une uniforme à 12,2».
- `reports/rapport-gpt-oss-perplexite.md:137-144` — «| **montage canonique** [...] | **26,0** | / | même montage, `analysis` retiré | 9 625 | / | **texte brut, même contexte** | **13,7** |».
- `reports/rapport-gpt-oss-perplexite.md:150` — «le facteur 370 entre les deux».
- `reports/rapport-gpt-oss-perplexite.md:152-153` — «fait passer le même montage de 9 625 à 677 321 — le modèle prédit « Chat » avec p = 0,77».
- `reports/rapport-gpt-oss-perplexite.md:162-163` — «Les 4 424 identifiants produits par notre tokenizer [...] **identiques un à un** à ceux de `llama-tokenize` (0 écart)».
- `reports/rapport-gpt-oss-perplexite.md:174-175` — «`--tokenize` passe de ~60 s à **0,385 s** [...] Le contrôle de non-régression Qwen ne bouge pas (19,3885)».
- `reports/rapport-gpt-oss-perplexite.md:191-194` — «| 512 | **18,58** | 19,65 | 174,34 | [...] | 4 096 | **170,78** | 400,13 | — |».
- `reports/rapport-gpt-oss-perplexite.md:196-200` — «Retirer la température divise la perplexité par **8,9** à 512 jetons, 5,9 à 1 024, 3,8 à 2 048».
- `reports/rapport-gpt-oss-perplexite.md:219-221` — «0-255 : 13,715 [...] 3584-3839 : 542,885».
- `reports/rapport-gpt-oss-perplexite.md:227-230` — «(jetons 1400-1659) donne 59,36 **à la position 0**, contre 13,94 [...] un facteur ~7 de plus».
- `reports/rapport-gpt-oss-perplexite.md:233-234` — «llama.cpp [...] donne 714,83 ; notre moteur 722,56 (1,1 % d'écart) [...] les 3 à 7 % mesurés à 63 et 512 jetons».
- `reports/rapport-gpt-oss-perplexite.md:246-247` — «sans YaRN : « Canberra. » ; avec : « The capital city of Australia is Canberra. »».

**reports/rapport-gpu-scores.md**
- `reports/rapport-gpu-scores.md:3-4` — «un écart de **1,6 à 2,3e-7** sur la référence CPU et **40× plus vite** à 262 144 clés».
- `reports/rapport-gpu-scores.md:22-23` — «Qwen2.5-0.5B (2 têtes KV × 64, 7 têtes de requête par tête KV), KV int8, un Quadro RTX 5000».
- `reports/rapport-gpu-scores.md:40-43` — mesure d'origine : «| 256 | 0,25 ms | 0,07 ms | 3,8× | 1,03e-7 |» ; «| **262 144** | 257,9 ms | **6,36 ms** | **40,6×** | 1,03e-7 |».
- `reports/rapport-gpu-scores.md:50-52` — re-mesure : «| 4 096 | 3,88 ms | **0,12 ms** | **31,6×** | 1,60e-7 | [...] | **262 144** | 243,82 ms | **6,09 ms** | **40,0×** | 2,25e-7 |».
- `reports/rapport-gpu-scores.md:59-62` — «avec une grille de `n_kv` blocs, le GPU tournait à 1,2 Go/s» ; «(une tranche ≈ 256 clés, plafonnée à 128 tranches)».
- `reports/rapport-gpu-scores.md:68-73` — «`_Z11attn_scoresPKvPKfS2_Pfiiiiiif`» ; «écart relatif **1,24**».

**reports/rapport-gpu-topk-selection.md**
- `reports/rapport-gpu-topk-selection.md:3-8` — «**quatre passes d'histogramme + deux noyaux de collecte** [...] **0,89 ms** là où le tri CPU en coûte **497 ms** à 262 144 clés [...] vérifié à **2,7–4,8e-7**».
- `reports/rapport-gpu-topk-selection.md:15-16` — «le fichier passe de 10 à 13 noyaux avec la sélection, puis à **14** avec le noyau 3 — 956 lignes».
- `reports/rapport-gpu-topk-selection.md:45-48` — «k = 256, 2 têtes KV × 64 dim, 7 têtes de requête par tête KV (**14 lignes**), cache KV 8 bits».
- `reports/rapport-gpu-topk-selection.md:51-56` — «Les TEMPS de ce rapport varient de ±50 % selon la charge de la machine [...] 0,45 ms puis 0,30 ms de collecte à 262 144 clés».
- `reports/rapport-gpu-topk-selection.md:60-62` — «| 4 096 | [...] | 0,14 ms (9×) | 1,31 ms | 0,13 ms (35×) | 4,33 ms |» ; «| 262 144 | [...] | 0,44 ms (224×) | 97,88 ms | 0,45 ms (896×) | 399,21 ms |».
- `reports/rapport-gpu-topk-selection.md:68-70` — «n = 1 avec k = 1 ; n = 100 avec k = 3 ; n = 4 097 et n = 5 000 [...] n = 8 191 avec k = 4 096».
- `reports/rapport-gpu-topk-selection.md:81-84` — «l'écart du **noyau 1** n'est plus 1,03e-7 mais **1,60 à 2,25e-7** [...] elle reste 4× sous le critère de 1e-6».
- `reports/rapport-gpu-topk-selection.md:88-93` — «le k-ième score **change** entre les scores calculés par le CPU et ceux calculés par le GPU sur 5 à 7 des 14 lignes».
- `reports/rapport-gpu-topk-selection.md:98-103` — «**14/14 lignes identiques**, 0,45 ms de collecte et 0,27 ms de seuil à 262 144 clés» ; «un débordement en VRAM silencieux».
- `reports/rapport-gpu-topk-selection.md:117` — «un préfixe scalaire aurait obligé à relancer le noyau une fois par tête (56 lancements au lieu de 4)».
- `reports/rapport-gpu-topk-selection.md:125-127` — «≈1 100× trop rapide pour la collecte et ≈900× pour le seuil (0,0004 ms au lieu de 0,45 ms)».
- `reports/rapport-gpu-topk-selection.md:142-145` — «| 100 | 3 | 0,03 ms | 0,02 ms | **1,04e-7** | [...] | 262 144 | 256 | 0,07 ms | 0,98 ms | **2,70e-7** |».
- `reports/rapport-gpu-topk-selection.md:147-153` — «Le temps GPU est **constant** (0,07 ms de 4 k à 262 k clés)» ; «**Limite** : k ≤ 1 024 [...] valeurs 8 ou 32 bits».
- `reports/rapport-gpu-topk-selection.md:159` — «dénominateur ×45,7 et sortie 55× trop petite à k = 1 ; écart relatif 2,05e-1».
- `reports/rapport-gpu-topk-selection.md:167` — «`groupe = fen == 0 && self.attn_topk == 0 && rep > 1`, `model.rs:3150`».
- `reports/rapport-gpu-topk-selection.md:178-179` — «| CPU (`--attn-topk 256`) | 9,4167 | 41,59 s | / | **GPU** [...] | **9,4162** | 41,45 s |».
- `reports/rapport-gpu-topk-selection.md:192-194` — «| 2 048 | 511 | 255 | **4,21** | 7,68 | 13,1358 / 13,1355 | 18,1 / 20,4 s |» ; «| **16 384** | 4 095 | **2 047** | 19,58 | **7,59** | [...] | **203,7 / 155,5 s (−24 %)** |».
- `reports/rapport-gpu-topk-selection.md:202-207` — «**Le croisement en clés est donc entre 255 et 2 047 clés** [...] (~4 000 clés d'après `docs/contexte-long.md`)» ; «17 434 jetons sont disponibles dans `/tmp/ids_qwen_long.txt`».
- `reports/rapport-gpu-topk-selection.md:209-211` — «« les tampons alloués à chaque appel : 24,5 ms/jeton au lieu de 2,9 », `docs/contexte-long.md` §4.ter» ; «~74 000 lancements pour ces 511 jetons».
- `reports/rapport-gpu-topk-selection.md:222-225` — «(64 têtes de requête, 8 têtes KV, puits allant de −1,95 à +3,38) [...] avec jusqu'à **4,65 logit** d'écart — un facteur 105».
- `reports/rapport-gpu-topk-selection.md:231-234` — «| avant correction | **17,6531** | / | après correction | **15,1786** | / | référence CPU (sans miroir VRAM) | 15,1757 |».
- `reports/rapport-gpu-topk-selection.md:253-262` — «| 4 096 | **0,13 ms** | 0,22 ms | 7,19e-7 | [...] | 262 144 | 1,58 ms | **1,35 ms** | 7,01e-7 |» ; «ses 14 blocs (un par ligne) saturent moins bien la VRAM que les 1 792 blocs de la chaîne. Le seuil de bascule est donc **mesuré** (131 072)».
- `reports/rapport-gpu-topk-selection.md:273-283` — «| 511 | 255 | **4,26** | 4,53 | 13,1358 / 13,1355 | [...] | 8 191 | 4 095 | 38,84 | **4,97** | — |» ; «**Le croisement est à ~300 clés** [...] à 4 095 clés il est **7,8× plus rapide**» ; «(+0,0043 ms par clé et par jeton)» ; «La perplexité est identique à 2e-5 près».
- `reports/rapport-gpu-topk-selection.md:294-297` — «la valeur du chemin top-k déporté (15,1666) est celle du chemin GPU dense (15,1667), l'écart de 6,6e-5 avec le CPU (15,1757)».
- `reports/rapport-gpu-topk-selection.md:304-308` — «| CPU, dense | 18,5803 | [...] | CPU, top-k 256 | 19,0740 | **+2,66 %** | [...] | GPU, top-k 256 (`DRAVE_GPU_TOPK`) | 18,8391 | **+2,90 %** | [...] | GPU sans miroir KV (`DRAVE_GPU` seul) | 18,3538 | −1,22 % vs CPU |».
- `reports/rapport-gpu-topk-selection.md:313-317` — «**l'écart CPU/GPU de 1,2 à 1,5 % n'est PAS le miroir KV** [...] soit −0,25 % pour le miroir» ; «un effet de 0,06 % à ctx 256 sur le même modèle».
- `reports/rapport-gpu-topk-selection.md:325-329` — «`monotone(-0,0) = 0x7FFFFFFF` et `monotone(+0,0) = 0x80000000`».
- `reports/rapport-gpu-topk-selection.md:340-345` — «| 1 | `attn_scores` | ✅ 1,6–2,3e-7 · 26,7–40× |» ; «| 5 | [...] chaîne complète **3,90 ms** pour 14 lignes × 1 M clés contre 539,9 ms d'attention complète CPU (×138) et 13,2 ms en VRAM (0,3× le complet, critère 2×) |».
- `reports/rapport-gpu-topk-selection.md:347-349` — «Le top-k GPU n'est donc **pas encore branché dans le moteur** [...] l'attention creuse continue de passer par le CPU jusqu'à l'étape 3.»

**reports/rapport-grappes.md**
- `reports/rapport-grappes.md:10-14` — «| 0.0 % | 74.12 % | 346 | 12.9 % | 0.0 % | 2.40 | 0.39 | [...] | 100.0 % | 76.07 % | 708 | 26.3 % | 75.0 % | 3.43 | 0.79 |».
- `reports/rapport-grappes.md:18-19` — «modèle en grappes pures : **74.12 %** [...] meilleur modèle dense de même budget (32→7→10, 311 paramètres) : **74.12 %**».
- `reports/rapport-grappes.md:26-32` — «| 1.0 % | 27.7 % | 72.5 | 15.1 | [...] | 100.0 % | 100.0 % | 262.1 | 54.6 |».
- `reports/rapport-grappes.md:42-43` — «l'élagage en blocs perdait 11 points à densité égale dans `run_encoding.py`».
- `reports/rapport-grappes.md:57` — «Mesures sur un MLP de 2 688 poids».

**reports/rapport-greffon.md**
- `reports/rapport-greffon.md:15` — «a = silu(u · x) · (v · x)          contribution ajoutée au flux résiduel : a · d».
- `reports/rapport-greffon.md:23-26` — «les 4 864 neurones d'origine n'apparient que `gate[i]` avec `up[i]`».
- `reports/rapport-greffon.md:33-42` — «Perplexité sur 1 020 tokens de WikiText-2, couche 12, greffon croisé `gate[0] × up[7]`» ; «| **aucun** (référence) | **23,6125** | — | / | **nul** (`u = v = d = 0`) | **23,6125** | **0,0000** | / | croisé, échelle 5,0 | 23,6253 | +0,0128 |».
- `reports/rapport-greffon.md:58-59` — «le banc à 100 évaluations/heure [...] 2 400 évaluations par jour».

**reports/rapport-harnais.md**
- `reports/rapport-harnais.md:3-7` — «Modèle : **qwen2 Q8_0** · corpus : WikiText-2 test (4080 tokens évalués) [...] **PPL = 24.77** sur 4080 tokens».
- `reports/rapport-harnais.md:9` — «un Qwen2.5-0.5B correct tourne autour de 15-25 sur WikiText-2».
- `reports/rapport-harnais.md:17-18` — «| 0 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |» (×24 couches).
- `reports/rapport-harnais.md:45-50` — «| Moyenne | 354.88 M | / | Médiane (p50) | 354.88 M | / | p95 | 354.88 M | / | p99 | 354.88 M | / | Écart-type / moyenne | 0.0 % |».
- `reports/rapport-harnais.md:67-68` — «⚠️ Mesure faite sur une seule fenêtre de tokens pour les statistiques d'événements».

**reports/rapport-inference.md**
- `reports/rapport-inference.md:3-5` — «**2 319 lignes de Rust, `std` seul, zéro dépendance.** [...] quantifié Q8_0 (507 Mo, 494 M de poids) [...] (2 × Xeon E5-2687W v3)».
- `reports/rapport-inference.md:18` — «généré  : 38 tokens en 3.86 s  (9.85 tok/s)».
- `reports/rapport-inference.md:30-35` — «| `src/gguf.rs` | [...] | 332 | [...] | `src/list.rs` | 4 encodages de listes, dont `PushMat` | 321 | [...] | `src/engine.rs` | [...] | 510 | [...] | `src/tokenizer.rs` | [...] | 371 | [...] | `src/model.rs` | [...] | 403 | [...] | `src/main.rs` | [...] | 382 |».
- `reports/rapport-inference.md:51-57` — «**16/16 identiques.** [...] | 0 | 358 (17,3063) | 358 (17,0202) |».
- `reports/rapport-inference.md:62-70` — «Perplexité WikiText-2 (2 040 tokens, fenêtres de 256)» ; «| numpy float32 (OpenBLAS) | 25,0004 | / | **moteur d'événements (int16)** | **24,8995** |» ; «Écart : **−0,4 %** [...] la valeur absolue plus élevée que les 20,29 du harnais précédent».
- `reports/rapport-inference.md:78-84` — «| Chargement du modèle [...] | 6,3 s | / | Mémoire résidente | **1,27 Go** (dont 0,71 Go de listes) | / | Événements par token | **352,8 M** | / | **Débit de génération** | **10,5 tok/s** (int16) · 10,6 (int8) · **11,4 en dense** | / | Temps par token | 100 ms = 90 ms de forward + 10 ms de tête | / | TTFT | 74–95 ms | / | Débit pendant le forward | **3,9 G événements/s** |».
- `reports/rapport-inference.md:88-94` — «| tok/s | 1,51 | 8,22 | **10,52** | 10,15 | 9,83 |» ; «un token paie **168 barrières** (7 matrices × 24 couches)».
- `reports/rapport-inference.md:96-98` — «la référence numpy + OpenBLAS (40 threads) faisait 132 ms par token, soit 7,6 tok/s. **Le moteur d'événements est 38 % plus rapide que numpy+BLAS**».
- `reports/rapport-inference.md:108-111` — «| **Listes d'événements** [...] | 0,71 Go — **1,44 o/poids** | **10,52** | / | Matrice dense int8 [...] | 0,49 Go — **1,06 o/poids** | **11,42** |» ; «**L'architecture événementielle coûte 8 % sur CPU** [...] elle lit 36 % de mémoire en plus».
- `reports/rapport-inference.md:116-118` — «le dense a d'abord été 20 % plus **lent** (8,5 tok/s) [...] Déroulée 4× [...] elle passe à 11,4 tok/s».
- `reports/rapport-inference.md:131` — «un accumulateur de 151 936 × 8 octets **par worker** (36 Mo) et chaque sortie serait écrite 896 fois».
- `reports/rapport-inference.md:135` — «Coût : 10 ms sur 100, soit 10 % du token.»
- `reports/rapport-inference.md:146-151` — «| int8 (127 niveaux) | 299 M | 3 tokens sur 6 [...] | 10,3 | / | **int16 (32 767 niveaux)** | 353 M | **16 sur 16** | 10,0 |» ; «quand deux tokens sont à 0,26 de logit».
- `reports/rapport-inference.md:157-170` — «**737 cas sur 737**, plus 13 468 cas de fuzz» ; «les identifiants produits diffèrent dans **5,2 % des cas** (38 sur 737)».
- `reports/rapport-inference.md:172-174` — «la valeur absolue publiée précédemment (20,29) a été calculée avec le tokenizer approximatif et devra être reprise».
- `reports/rapport-inference.md:184-186` — «Elle est **30 % plus rapide que numpy + OpenBLAS** sur le même modèle [...] avec 20 threads au lieu de 40.»
- `reports/rapport-inference.md:193-197` — «3,9 G événements/s sur 20 cœurs ≈ 1 événement par cycle et par cœur. Un banc FPGA à 124 MHz × 32 PEs vise la même cadence.» ; «0,71 Go de listes pour 494 M de poids, soit 1,44 octet par poids — contre 1,06 pour Q8_0 dense».
- `reports/rapport-inference.md:201-204` — «Le moteur lisait 706 Mo par token en 95 ms, soit **7,4 Go/s sur les 28,7 Go/s mesurés** [...] (13,7)».
- `reports/rapport-inference.md:210` — «Or vider l'accumulateur entier par fenêtre coûte… 0,2 % du temps de token.»
- `reports/rapport-inference.md:214-219` — «| liste des destinations touchées | 10,96 | 92,2 ms | [...] | **sans la liste (borne haute cumulative)** | **14,74** | **69,4 ms** |» ; «**+35 %**, perplexité **identique au chiffre près** (24,8995) [...] de 3,6 à **5,3 G év/s**».
- `reports/rapport-inference.md:225-230` — «« DIVERGENT au rang 0 : 0 vs 3513 »» ; «C'est ce que le banc signalait au rang 895.»
- `reports/rapport-inference.md:232-235` — «10,4 Go/s utilisés sur 28,7 → **2,8× avant d'être borné par la mémoire** [...] plus rapide que le noyau dense int8 (11,4 tok/s)».
- `reports/rapport-inference.md:244-262` — «| Fichier GGUF | 506 Mo | 337 Mo | **−33 %** | / | Listes en mémoire | 0,71 Go | 0,63 Go | **−11 %** | / | Événements par token | 352,7 M | 312,5 M | −12 % | / | RSS | 1,27 Go | 1,02 Go | −20 % | / | Débit | 10,33 tok/s | 11,78 tok/s | +14 % | / | **Perplexité WikiText-2** | **24,90** | **27,83** | **+12 %** |» ; «le format liste reste 2,7× plus gros».
- `reports/rapport-inference.md:269-276` — «| 100 % | 352,7 M | 10,33 | 3,56 G év/s | [...] | 10 % | 35,6 M | 21,40 | 0,88 G év/s |» ; «**10× moins d'événements ne donnent que 2× de vitesse.**»
- `reports/rapport-inference.md:285-288` — «| dispersé (magnitude) | 89,5 M | 66,1 ms | 13,77 | / | **contigu (fenêtre)** | 85,8 M | **50,1 ms** | **17,91** |» ; «un élagage **contigu** [...] est **30 % plus rapide à taux égal**».
- `reports/rapport-inference.md:296-303` — «| matvec, 100 % de poids | 186,6 ms | 120,6 ms | 99,1 ms | **90,4 ms** | / | matvec, 10 % de poids | **31,3 ms** | 35,7 ms | 40,6 ms | 52,9 ms ❌ |» ; «À 32 workers il faut 1,2 Mo d'accumulateurs».

**reports/rapport-lecteur-multifichiers.md**
- `reports/rapport-lecteur-multifichiers.md:10-11` — «(convertisseur, 1 587 tenseurs vérifiés par SHA-256)».
- `reports/rapport-lecteur-multifichiers.md:17-24` — «Le modèle d'origine (18,56 Go, un fichier, sur le disque mécanique) contre le même modèle éclaté en `commun.gguf` + 8 × `cluster-XX.gguf`» ; «| modèle d'origine | **15,2789** | 12,2 s | / | modèle en clusters | **15,2789** | 11,6 s |».
- `reports/rapport-lecteur-multifichiers.md:32-44` — «DeepSeek-V4-Flash-UD-IQ1_M (86,9 Go, 3 shards)» ; «| annoncé par les descripteurs | **86,90 Go** | / | somme des fichiers sur disque | **86,90 Go** | / | tenseurs | 1 328 (shard 1 : 0, shard 2 : 784, shard 3 : 544) | / | temps de lecture des en-têtes | 54 ms |».
- `reports/rapport-lecteur-multifichiers.md:52-58` — «| fichiers | 9 (commun + 8 clusters) | / | tenseurs | **1 587** | / | poids | **18,55 Go** | / | chargement complet du modèle | 48 couches en 27,8 s | / | mélanges d'experts chargés | **48/48 couches** |».
- `reports/rapport-lecteur-multifichiers.md:63-68` — «| Qwen2.5-0.5B ctx 256 `--dense` | 19,3885 | **19,3885** | / | gpt-oss-120b ctx 256 [...] | 15,1757 | **15,1757** | / | `cargo test --release` | vert | **32 verts** (20 au début du sprint) | / | modèle en clusters | 15,2789 | **15,2789** | / | nœud partiel (cluster 0 seul) | 268 786,6218 | **268 786,6218** |».
- `reports/rapport-lecteur-multifichiers.md:87` — «(`ligne 0 : 2181034 au lieu de 271`)».
- `reports/rapport-lecteur-multifichiers.md:93` — «Symptôme : **3,19 Go annoncés pour 18,55**».
- `reports/rapport-lecteur-multifichiers.md:112-113` — «`cluster-100.gguf` se range avant `cluster-20.gguf`» ; «Au-delà de 99 clusters».
- `reports/rapport-lecteur-multifichiers.md:120-121` — «l'incident `iq1_m` (8,56 Go annoncés pour 86,9)».
- `reports/rapport-lecteur-multifichiers.md:158-165` — «**La concordance porte sur 984 Go** : DeepSeek-V4.1-Flash 365,70 = 365,7 · GLM-5.3 216,71 = 216,7 · Kimi-K2.7 303,90 = 303,9 · DeepSeek-V4-Flash 86,90 = 86,9 · GLM-5.3-Flash 93,08 = 93,1 · Qwen3-235B 85,68 = 85,7. **La file de 1 138 Go est terminée**».
- `reports/rapport-lecteur-multifichiers.md:167-169` — «Les architectures sont lues (`deepseek41`, `deepseek2`, `deepseek4`, `glm-dsa`) [...] Kimi est en huit fichiers, GLM en six».
- `reports/rapport-lecteur-multifichiers.md:171-186` — «Le mmap : 3,3× plus rapide, 3× moins de mémoire» ; «| mappé (défaut) | **9,32 s** | **6,35 Go** | / | lu en entier (`DRAVE_MMAP=0`) | 30,68 s | 19,20 Go |».
- `reports/rapport-lecteur-multifichiers.md:199-204` — «| 1 | 268 786,62 | **2,35 Go** | 9,64 s | [...] | **8** | **799,8557** | 6,28 Go | 10,65 s |» ; «**2,7× moins pour un nœud à un cluster que pour le modèle entier**».
- `reports/rapport-lecteur-multifichiers.md:221` — «`index out of bounds: the len is 1 but the index is 6`».
- `reports/rapport-lecteur-multifichiers.md:239-242` — «| conversion | 435 + 8 × 144 = **1 587 tenseurs**, 18,60 Go, 351,7 s | / | `mapping.tsv` écrit par le convertisseur | 6 144 entrées · 48 couches · 128 experts · 8 clusters | / | vérification par empreintes | **1 587 tenseurs · TOUT CONCORDE** | / | exécution du modèle converti | **15,2789** |».
- `reports/rapport-lecteur-multifichiers.md:263-264` — «`--lot 64` rend 15,2736 contre 15,2789 par jeton».

**reports/rapport-localite-activation.md**
- `reports/rapport-localite-activation.md:17` — «Leur modèle TurboSparse (≈ 90 % de creux) est *entraîné* ainsi».
- `reports/rapport-localite-activation.md:24` — «bascule push/pull mesurée à **22 % de densité** (`seuil_push = 0.22`)».
- `reports/rapport-localite-activation.md:27` — «déport GPU | matrices entières, seuil de rentabilité mesuré (8 Mo)».
- `reports/rapport-localite-activation.md:37` — «le critère « valeur quantifiée non nulle » laissait passer 100 % des neurones à 16 bits (mesuré : densité de 51 104 %)».
- `reports/rapport-localite-activation.md:43-47` — «densité d'activation (seuil 5 % du max) | **17,9 %** [...] (82 % ne font rien)» ; «12,3 % / **33,1 %** / 74,2 %» ; «neurones tirés **> 90 %** du temps | **0,08 %**» ; «> 50 % du temps | 2,82 %» ; «173 à 1 579 tirs par jeton (×9) ; part des 10 % les plus lourds : 16,7 à 51,1 %».
- `reports/rapport-localite-activation.md:59-64` — «gpt-oss active 4 experts sur 128 par couche et par jeton» ; «un cache d'experts chauds en VRAM (32 Go sur les deux RTX 5000, pour un modèle de 62 Go)» ; «le noyau MXFP4 « warp par ligne » tourne maintenant à 42 Go/s avec un résultat **bit à bit identique** au CPU».

**reports/rapport-logits-gpu-vs-cpu.md**
- `reports/rapport-logits-gpu-vs-cpu.md:6-7` — «sur un **MoE**, il les décale de **0,038 nat** en moyenne — **497 jetons sur 511 gardent le même top-1** (14 divergent), et cela suffit à déplacer la perplexité de 1,2 % [...] (top-8 sur 128)».
- `reports/rapport-logits-gpu-vs-cpu.md:13-17` — «| CPU | 18,5803 | — | / | GPU, miroir KV seul (`DRAVE_GPU_KV`) | 18,3074 | −1,47 % | / | GPU, projections seules (`DRAVE_GPU`) | 18,3538 | −1,22 % |».
- `reports/rapport-logits-gpu-vs-cpu.md:19-22` — «Ajouter le miroir KV aux projections ne pèse que **0,25 % de plus**» ; «(2e-7 sur la tête Q8_0, **0,00e0** bit à bit sur un expert MXFP4)».
- `reports/rapport-logits-gpu-vs-cpu.md:33-35` — «| perplexité | 17,4315 | 17,4315 | / | écart moyen \|ΔNLL\| | — | **0,0000** (max 0,0000) |».
- `reports/rapport-logits-gpu-vs-cpu.md:40-44` — «| perplexité | 18,5803 | 18,3538 | / | écart moyen \|ΔNLL\| | — | **0,0379** (médiane 0,0123, p90 0,0836, max 1,3708) | / | accord du top-1 | — | **497/511** (14 positions divergentes) | / | corrélation des logits (position 0) | — | 1,000000 |».
- `reports/rapport-logits-gpu-vs-cpu.md:46-52` — «6× plus grand en moyenne que les autres (0,198 contre 0,033) [...] (1,3708 nat, position 284) [...] seules 3 des 14 sont dans le top-14 des écarts» ; «(511/511 annoncé, **497/511** mesuré)».
- `reports/rapport-logits-gpu-vs-cpu.md:65-68` — «l'écart de 0,06 % mesuré à `--ctx 256` [...] 14 positions sur 511 changent de jeton» ; «La perplexité GPU est MEILLEURE (18,35 contre 18,58)».
- `reports/rapport-logits-gpu-vs-cpu.md:83-84` — «les portes du dépôt (15,1757 CPU / 15,1667 GPU à ctx 256)».

**reports/rapport-minimal.md**
- `reports/rapport-minimal.md:3` — «MLP 32→64→10, entraîné sur 4096 exemples synthétiques, évalué sur 1024».
- `reports/rapport-minimal.md:9-15` — «| float32 (référence) | 32.00 | 76.07 % | [...] | int4 [...] | 4.00 | 74.12 % | -1.95 pt | / | ternaire 1,58 b (dense 2 b) | 2.00 | 49.71 % | -26.37 pt | / | multi 4 plans ternaires | 8.00 | 75.98 % | -0.10 pt |».
- `reports/rapport-minimal.md:21-27` — «| Exactitude arithmétique — couche 1 [...] | 4.233e-07 |» ; «| Erreur de quantification des activations — couche 2 | 6.322e-01 |» ; «| Accuracy chemin entier [...] | 49.22 % |» ; «| Accumulateur max (doit tenir en int32) | 488 |».
- `reports/rapport-minimal.md:33-47` — «| float32 | 32.00 | 10.5 Kio | [...] | ternaire en CSR (CDC) | 10.10 | 3.3 Kio |».
- `reports/rapport-minimal.md:53-55` — «| 2 bits | 50.9 % | 27.5 % | / | 3 bits | 51.3 % | 44.1 % | 27.5 % | / | 4 bits | 51.5 % | 48.1 % | 42.8 % | 27.5 % |».
- `reports/rapport-minimal.md:59` — «DDR3 9,66 Go/s · PCIe x8 6,5 Go/s · fmax actuel 124 MHz».
- `reports/rapport-minimal.md:63-73` — «| 7B — ternaire 2 b | 1750.0 Mo | 181.159 | 5.5 | 312 | 9360 | [...] | 70B — ternaire CSR | 148750.0 Mo | 15398.551 | 0.1 | 37 | 1110 |».
- `reports/rapport-minimal.md:80-81` — «10.1 b/poids pour le ternaire et 61.8 b/poids pour 4 plans [...] soit 5 à 15× plus de trafic» ; «~312 voies de MAC (≈ 9 400 ALM, 5 % du FPGA) [...] 96 % du device reste disponible».
- `reports/rapport-minimal.md:83` — «Ses chiffres de débit (§3, premières lignes) ne veulent rien dire».

**reports/rapport-mla-experts.md**
- `reports/rapport-mla-experts.md:12-15` — «| V4-Flash, V4.1 | `tenseur blk.3.attn_q.weight absent` |» ; «| GLM-5.3, Kimi | `mélanges d'experts chargés : 0/79` |».
- `reports/rapport-mla-experts.md:31-33` — «Pour GLM-5.3 : 576 valeurs par jeton au lieu de 448 par tête dense (28 672 pour 64 têtes)».
- `reports/rapport-mla-experts.md:59-66` — «| 53 couches | IQ3_XXS | IQ1_S | / | 22 couches | IQ3_XXS | IQ2_XXS | / | 4 couches | **IQ4_XS** | IQ1_S | / | 1 couche | **Q3_K** | IQ2_XXS |» ; «D'où « 71/79 » : les 5 couches fautives».
- `reports/rapport-mla-experts.md:71-74` — «les huit déquantificateurs concernés sont comparés à libggml au bit près (`tools/portes_formats.sh`)».
- `reports/rapport-mla-experts.md:79-82` — «Faux pour GLM-5.3 (3 couches denses puis 76) et pour Kimi (1 puis 60)».
- `reports/rapport-mla-experts.md:92-100` — «**GLM-5.3 (216 Go)** : 79 couches MLA, 76/79 mélanges d'experts chargés [...] ~85 Go de RSS au chargement, dont ~52 Go de tenseurs MLA déquantifiés en f32» ; «**Kimi-K2.7 (1 026 G poids)** [...] 61 couches MLA, routage sigmoïde ×2,827, 384 experts dont 8 par jeton» ; «**48 tests** (46 avant, +2 [...] )».
- `reports/rapport-mla-experts.md:106-113` — «| chargement | 379 à 553 s |» ; «| mémoire de pointe | ~90 Go de RSS |» ; «| débit, première mesure | **253 s par jeton** |» ; «| débit, après suppression des allocations par bloc | **53 s par jeton** (dont 20 s d'attention) |» ; «| perplexité, 3 jetons froids | **5 966** contre **4 286** chez llama.cpp |» ; «| corrélation des logits (pos. 0) | **0,999024** |» ; «| accord du top-1 | **3/3** |».
- `reports/rapport-mla-experts.md:118` — «Le chemin a d'abord été faux (7,3 M de perplexité, corrélation −0,04)».
- `reports/rapport-mla-experts.md:121-126` — «(`qk_nope = 192`, `qk_rope = 64`, `v = 256`, `kv_lora = 512`)» ; «`rope.freq_base = 8e6`» ; «`index_topk = 2048` [...] un contexte de 16 jetons».
- `reports/rapport-mla-experts.md:155-160` — «| chargement | **161 s** (mmap, 1 026 G poids sur le NVMe) | / | 2 jetons notés | **146 s** (73 s/jeton) | / | perplexité (2 jetons froids, ses propres jetons) | 81 384 | / | perplexité avec les jetons de GLM (erreur de ma part) | 1 236 804 |».
- `reports/rapport-mla-experts.md:174-188` — «llama.cpp : perplexité 890,4559» ; «| écart de NLL [...] | **+0,009** | +0,372 | +0,611 | **+4,070** | +3,118 | +2,041 | +1,583 |» ; «(4 807,76 contre 4 807,07)».
- `reports/rapport-mla-experts.md:217` — «| ‖nous − llama.cpp‖ / ‖llama.cpp‖ | **1,9 %** | **1,3 %** | **3,8 %** | **4,0 %** |».
- `reports/rapport-mla-experts.md:227` — «un bug de disposition donnait 5e-4 au lieu de 1,5e-3 sur `kqv_out`, soit 300 %».
- `reports/rapport-mla-experts.md:235-236` — «Valeurs de référence conservées dans `/tmp/ref_glm_8p.log` ; le moteur met ~190 s par jeton».

**reports/rapport-mode4-lot-listes.md**
- `reports/rapport-mode4-lot-listes.md:3-15` — «1,5 ko par jeton contre 3,5» ; «`a_j · n_blocs_j · longueur_j`» ; «(indices par écarts u8 avec échappement vers u16, valeurs i8, une échelle f32 par bloc de 32 canaux)».
- `reports/rapport-mode4-lot-listes.md:26-35` — «| mode 2, un flux par jeton (référence) | 1 608 par flux | 2,74e-2 | / | **mode 4, lots de 16** | **1,5 ko** (contre 3,5 en lot dense) | **3,03e-2** |» ; «**÷2,2 sur les octets** [...] 3 663 octets par jeton en lot DENSE (mode 3), 1 608 en mode 2 par jeton, **1 500 en mode 4**» ; «un relecteur a mesuré 1 671 contre 1 600, soit 1,02×» ; «à 1,11× celui du mode 2 (le critère posé était 1,5×)».
- `reports/rapport-mode4-lot-listes.md:44-48` — «| 20 | 2,30e-1 | 4,09e-2 | **5,6×** | [...] | 64 | 1,86e-2 | 3,70e-2 | 0,50× | / | 256 | 6,46e-2 | 5,64e-2 | 1,15× |».
- `reports/rapport-mode4-lot-listes.md:56` — «`--limit 20 --lot 20` et `--limit 20 --lot 16` (16 + 4) donnent la **même** perplexité (157,3415)».
- `reports/rapport-mode4-lot-listes.md:73-80` — «un pair annonçait 268 Mo par état sur 74 898 états (~19 Po)» ; «(896 actifs, 3 708 octets chacun, 74 898 états annoncés [...] )» ; «le serveur refuse à l'état **72 393** [...] `corps du lot en listes (cumul après l'état 72393) : 268436952 octets au-delà du plafond de 256 Mo` — 258 Mo envoyés en 1,4 s».
- `reports/rapport-mode4-lot-listes.md:88-93` — «« hors dimension » s'imprimait une fois PAR ÉTAT (200 lignes pour une trame de 200 états)» ; «83 octets d'un pair hostile suffisaient» ; «à 20 jetons en lots de 16, elle annonçait 0,9 ko par jeton pour 1,45 réels».

**reports/rapport-modele-reel.md**
- `reports/rapport-modele-reel.md:3` — «**qwen2**, 24 couches, hidden 896, intermédiaire 4864, 14 têtes / 2 KV (GQA)».
- `reports/rapport-modele-reel.md:9-17` — «| blk.0.attn_norm.weight | 19.0 % | 77.9 % | 92.2 % | [...] | blk.0.attn_output.weight | 95.9 % | 99.7 % | 100.0 % |».
- `reports/rapport-modele-reel.md:24-27` — «| 4 | 27.4 % | 27.5 % | 27.5 % | **1.00×** | / | 8 | 15.3 % | 15.2 % | 15.1 % | **1.00×** |».
- `reports/rapport-modele-reel.md:31-38` — «| blk.0.ffn_gate.weight | 5 % | 5.0 % | 42.01 | 44.97 | 0.93× | [...] | blk.0.ffn_down.weight | 20 % | 20.0 % | 5.42 | 5.42 | 1.00× |».
- `reports/rapport-modele-reel.md:42-44` — «`attn_q` : (896, 896), 14 têtes de 64 dimensions» ; «énergie par tête : 1.4 % à 28.5 % (uniforme = 7.1 %)» ; «similarité entre têtes : 0.020 en moyenne».
- `reports/rapport-modele-reel.md:51-58` — «**27,5 % contre 27,5 % pour une partition aléatoire (1,00×)**» ; «Mon premier test était **circulaire** [...] laissait croire à un effet de 1,56×».
- `reports/rapport-modele-reel.md:64` — «dans `attn_output`, **95,9 %** des poids sont sous 5 % du maximum ; 73,8 % dans `ffn_gate`».
- `reports/rapport-modele-reel.md:75-77` — «(74,12 % contre 74,12 % pour le meilleur dense à budget égal) [...] (0,39 contre 0,79 b/poids)».

**reports/rapport-mode-listes.md**
- `reports/rapport-mode-listes.md:7` — «**qwen2 Q8_0** (494.0 M poids, densité 99.2 %)».
- `reports/rapport-mode-listes.md:19-24` — «| multiplieur (référence GPU) | 0.99 | 8,00 | / | **décalage-addition (popcount)** | **3.10** | 8,00 | / | **unaire (suites de zéros)** | **42.45** | **42.45** |» ; «L'unaire coûte **13.7× plus**».
- `reports/rapport-mode-listes.md:29-33` — «| 1 carte FPGA (9,66 Go/s) | 1.4 tok/s | 0.26 tok/s | / | 4 cartes FPGA | 5.5 tok/s | 1.04 tok/s | / | CPU (28,7 Go/s) | 4.1 tok/s | 0.77 tok/s |».
- `reports/rapport-mode-listes.md:40-45` — «`E[|v|] = 42,79` pour un Q8_0» ; «**Le décalage-addition donne le même résultat pour 3,13 additions par poids** (mesuré : `E[popcount] = 3,13`)».
- `reports/rapport-mode-listes.md:48-49` — «on paie 3,13× en opérations [...] sur un FPGA où 95 % des ALM dorment».

**reports/rapport-mur-memoire-4bits.md**
- `reports/rapport-mur-memoire-4bits.md:3` — «Suite de `rapport-croisement-push-pull.md`.»
- `reports/rapport-mur-memoire-4bits.md:11` — «| **tranches périmées en mode dense** | PPL **4 361 879** au lieu de 19,26 |».
- `reports/rapport-mur-memoire-4bits.md:19-21` — «PPL 19,2647 au chiffre près sur 510 jetons, 24 jetons identiques, et 0 contre 180,7 G événements».
- `reports/rapport-mur-memoire-4bits.md:33-43` — «`blk.0.ffn_gate.weight` — 4 864 × 896, 4,36 M poids» ; «| 0 % | 0,004 | 0,167 | 0,03 | [...] | 100 % | 0,801 | 0,171 | **4,69** |».
- `reports/rapport-mur-memoire-4bits.md:45-53` — «croisement à **24 %**» ; «croisement vers **33–45 %** (mesure bruyante : le temps du pull y passe de 0,342 à 0,192 ms)» ; «**Le croisement est à ~22 %, pas à 10 %** [...] `seuil_push` passe de 0,15 à **0,22**» ; «À 10 % de densité le push est ×2,1 plus rapide ; à 1 %, ×8,3».
- `reports/rapport-mur-memoire-4bits.md:66-67` — «bande passante mémoire mesurée : 19–22 Go/s (charge de fond : 4–8) / pull : 4,4 Mo lus à 14,1–26,9 Go/s, soit 62–136 % du repère».
- `reports/rapport-mur-memoire-4bits.md:72-80` — «Il lit ses poids à 14 Go/s quand la mémoire en donne 20» ; «passe de 26 Go/s à 14 Go/s» ; «**gain nul** (21,98 ms contre 21,94)».
- `reports/rapport-mur-memoire-4bits.md:87-92` — «`w = (nibble−8)·s_bloc`, une échelle `u16` **relative** par bloc de 32 (précision 1/65535, et non 1/255 — essayé : PPL 17,09 contre 17,10 [...] )» ; «**4,5 bits/poids effectifs** (4 + 16/32) [...] ×1,78 moins d'octets».
- `reports/rapport-mur-memoire-4bits.md:96-103` — «~5 cycles par poids» ; «(16 poids par `vpmaddwd`)» ; «scalaire 132,331 contre AVX2 −2,495» ; «4 864 × 896».
- `reports/rapport-mur-memoire-4bits.md:111-126` — «| int8 partout | **17,4092** | — | 28,3 | 22,1 | / | 4 bits **attention** | 18,3503 | +5,4 % | 24,5 | 27,0 | / | 4 bits **FFN** | 21,6082 | +24,1 % | 37,0 | 14,1 | / | 4 bits corps entier | 21,9118 | +25,9 % | **39,2** | 13,1 |» ; «×1,22 **plus lent**» ; «×1,57 plus rapide» ; «**×1,39** (28,3 → 39,2 tok/s) pour **+26 % de perplexité**».
- `reports/rapport-mur-memoire-4bits.md:141-149` — «| Qwen2.5-0.5B **Q8_0** | int8 | **19,2647** | — | 18,0 | 28,3 | / | Qwen2.5-0.5B **Q4_0** | int8 (requantifié) | 21,1971 | +10,0 % | 18,0 | 28,3 | / | Qwen2.5-0.5B **Q4_0** | **4 bits verbatim** | **21,0116** | **+9,1 %** | **13,1** | **38,9** | / | Qwen2.5-0.5B **Q4_0** | 4 bits + tête 4 bits | 21,7431 | +12,9 % | 12,0 | **42,5** |» ; «(255 jetons donnaient 19,86 / 19,67 / 19,88 [...] )».
- `reports/rapport-mur-memoire-4bits.md:153-164` — «**Le prix réel des 4 bits sur ce modèle est +9,1 % de perplexité**» ; «21,01 contre 21,20 de perplexité [...] et 13,2 contre 18,2 s» ; «en Q4_0 l'échelle de bloc est **signée** (`d = max/−8` [...] )» ; «a donné PPL 3 550 569 avant correction».
- `reports/rapport-mur-memoire-4bits.md:168-172` — «3,1 ms/jeton pour l'attention à contexte 256, pour seulement ~0,5 M de multiplications» ; «n'a rien changé (3,20 → 3,27 ms)».
- `reports/rapport-mur-memoire-4bits.md:176-192` — «| scores `q·k` | **2,10 ms** | **0,65 ms** | / | softmax | 0,28 | 0,27 | / | somme pondérée + écriture KV | 0,71 | 0,65 | / | **total** | **3,09** | **1,57** |» ; «Huit accumulateurs indépendants n'ont rien donné non plus (2,10 → 2,16 ms)» ; «En AVX2 + FMA, 32 éléments par tour : **×3,3**» ; «(21,0116 → 21,0131)».
- `reports/rapport-mur-memoire-4bits.md:199-207` — «×1,34 de débit **et** une perplexité légèrement meilleure que l'int8» ; «requantifier en 4 bits coûte +26 % de perplexité» ; «`--q4-attn` et `--q4-tout` sont conservés comme **résultats négatifs**».

## C. Contradictions, chiffres périmés, affirmations douteuses

- `reports/rapport-gpu-topk-selection.md:347-349` — «Le top-k GPU n'est donc **pas encore branché dans le moteur** [...] l'attention creuse continue de passer par le CPU jusqu'à l'étape 3.» — contredit frontalement `:164-171` («La condition est complétée par une branche `DRAVE_GPU_TOPK=1` (opt-in)»), `:343` («✅ **fait** (opt-in `DRAVE_GPU_TOPK=1`)») et `:195` («l'attention GPU top-k»). Conclusion périmée laissée en fin de rapport.
- `reports/rapport-gpu-topk-selection.md:7-8` — «coûte **0,89 ms** là où le tri CPU en coûte **497 ms** à 262 144 clés» — aucun de ces deux chiffres n'existe dans les tableaux du même rapport : à 262 144 clés on lit «0,44 ms (224×) [...] 97,88 ms [...] 0,45 ms (896×) [...] 399,21 ms» (`:62`) ; 0,89 ms est la valeur de la chaîne à 131 072 clés (`:256`). Chiffres d'intro non traçables.
- `reports/rapport-gpu-topk-selection.md:204` vs `:243` vs `:251` — «8 lancements et 17 transferts par couche et par jeton» (`:204`), puis «**six lancements et cinq recopies** par couche et par jeton» (`:210`), puis «La chaîne séparée coûtait 8 lancements» (`:243`) et «chaîne (9 lancements)» (`:251`). Trois comptages différents (8, 6, 9) pour la même chaîne.
- `reports/rapport-gpu-topk-selection.md:295-296` — «l'écart de 6,6e-5 avec le CPU (15,1757)» — l'écart relatif entre 15,1666/15,1667 et 15,1757 vaut ≈ 6e-4 (0,06 %), comme le dit le même rapport à `:316` («un effet de 0,06 % à ctx 256») ; le 6,6e-5 est faux d'un ordre de grandeur.
- `reports/rapport-gpu-scores.md:27-34` et `:36` — «**Correction du 30/09** : les écarts de 1,03e-7 ci-dessous ont été mesurés avec [...] **la même clé** — un banc dégénéré» ; «la ligne « 65 536 » ci-dessous datait d'AVANT le découpage en tranches (7,4 ms, 8,9×) ; re-mesurée après, elle vaut **2,36 ms et 26,7×**» — le tableau « d'origine » (`:40-43`) est explicitement périmé et conservé pour traçabilité seulement.
- `reports/rapport-gpu-topk-selection.md:81-84` — «l'écart du **noyau 1** n'est plus 1,03e-7 mais **1,60 à 2,25e-7** [...] Le rapport du noyau 1 est corrigé dans le même commit.» — chiffre publié remplacé.
- `reports/rapport-gpu-topk-selection.md:72-79` — «**Le banc mentait** [...] la même clé pour toutes les positions [...] le banc validait un cas dégénéré» — les 14/14 « verts » initiaux ne prouvaient rien.
- `reports/rapport-gpu-topk-selection.md:100-103` — «un débordement en VRAM silencieux (`t.k < k` est entré dans la condition)» — bug de tampon non détecté par les bancs.
- `reports/rapport-gpu-topk-selection.md:123-127` — «les deux temps du second passage étaient affichés sans conversion et annonçaient un noyau ≈1 100× trop rapide [...] Un affichage mal étiqueté est un affichage qui ment».
- `reports/rapport-gpu-topk-selection.md:219-239` — «un défaut dans un noyau **plus ancien**, `attn_kv_recombine` [...] avec jusqu'à **4,65 logit** d'écart — un facteur 105 [...] seul ce noyau était faux» ; «la porte de 19,3885 ne pouvait pas voir ce défaut» — la porte historique était aveugle à ce bug.
- `reports/rapport-gpu-topk-selection.md:313-318` vs `reports/rapport-logits-gpu-vs-cpu.md:6-7, 58-63` — deux explications concurrentes du même écart CPU/GPU de 1,2 % : «Il vient du déport des PROJECTIONS Q8_0/MXFP4, dont l'ordre de sommation diffère [...] C'est un doute à instruire, pas une explication» contre «l'hypothèse la plus simple [...] est que de minuscules écarts numériques **changent le routage des experts**». Non tranché dans ces 20 fichiers.
- `reports/rapport-logits-gpu-vs-cpu.md:49-54` — «`compare_logits.py` n'imprimait qu'un ÉCHANTILLON de positions [...] (511/511 annoncé, **497/511** mesuré). L'outil imprime maintenant l'accord GLOBAL — un affichage partiel qui a l'air complet est un affichage qui ment.» — chiffre 511/511 explicitement faux et corrigé.
- `reports/rapport-empreinte-memoire.md:190-200` vs `:369-379` — «## 7. La réductibilité est uniforme [...] **Aucune différence.** Cibler « les extrêmes » n'apporte rien.» contredit «Et la réductibilité n'est pas répartie uniformément : [...] couches 0-3 [...] **75 à 82** — les moins réductibles / couches 16-30 [...] **42 à 49** — les plus réductibles». Deux conclusions opposées dans le même rapport.
- `reports/rapport-empreinte-memoire.md:208-210` vs `:295-297` — «en dessous de 8 experts, un cache ne sert **à rien** (0 % de succès — un jeton consomme ses 8 experts d'un coup)» contredit «Un cache « experts du jeton précédent » — 8 entrées [...] sert 27 à 52 % des appels».
- `reports/rapport-empreinte-memoire.md:7` vs `:471` vs `:504` — l'empreinte de V4.1 est donnée tour à tour comme «**50–80 Go**», «**45 à 78 Go**» et «**~50 à 80 Go**» selon la ligne.
- `reports/rapport-empreinte-memoire.md:437-439` — «**elle est bornée aux couches 6–39** (trois cycles de 12). Les couches 0–5 et **30–47** n'en montrent aucune trace» — «30–47» recouvre la plage 30–39 déclarée porteuse du signal (et le tableau `:429-430` donne bien +0,003 pour 30/42 et 33/45) : intervalle probablement mal écrit (40–47 attendu).
- `reports/rapport-empreinte-memoire.md:282` et `:478` — deux sections numérotées « ## 9. » («9. Trois dernières pistes» puis «9. Les mesures d'infrastructure») après un «## 12» (`:457`) : numérotation de sections incohérente.
- `reports/rapport-empreinte-memoire.md:523` et `:526` — deux entrées numérotées « 2. » dans la liste « Ce qui reste à faire » («Le cache d'experts adossé au disque» puis «La tête restreinte par langue»).
- `reports/rapport-empreinte-memoire.md:492-495` — «mon premier test de disque froid ne vérifiait pas le retour de `pread` et a chronométré ce disque à **2 211 Go/s** [...] `O_DIRECT` échoue par ailleurs ici (errno 29), donc le régime réellement froid n'est pas mesuré proprement.» — mesure invalide assumée.
- `reports/rapport-empreinte-memoire.md:534-536` — «un disque mécanique à 2 211 Go/s, une allocation de cache à 4,1 % partout, un total de 4 231 Go» — trois chiffres absurdes reconnus comme artefacts de mesure.
- `reports/rapport-empreinte-memoire.md:71-76` vs `:538-540` — la perplexité restreinte qui *baisse* («25,3748» → «24,3108») est désignée comme un faux gain : «Elle aurait suffi à annoncer un gain inexistant.»
- `reports/rapport-empreinte-memoire.md:48-50` — «`matvec_q4` calcule une liste creuse puis **reconstruit un vecteur dense** avant le produit [...] La sparsité est calculée et jetée.» — décrit un chemin inefficient (et `matvec_q4` a ensuite été remplacé par un aiguillage, cf. `rapport-mla-experts.md:98-99`).
- `reports/rapport-lecteur-multifichiers.md:267-268` — «Le **mmap** : `read_to_end` charge tout le fichier. DeepSeek-V4.1-Flash fait 366 Go, il restera hors de portée sans lui.» — contredit `:171-186` («Le mmap : 3,3× plus rapide, 3× moins de mémoire [...] Les fichiers sont maintenant **mappés**») et `:182` (`DRAVE_MMAP=0`). Reste d'une version antérieure du rapport.
- `reports/rapport-lecteur-multifichiers.md:66` vs `:142` — «`cargo test --release` | vert | **32 verts** (20 au début du sprint)» contre «laissait **les trente tests verts**» : 32 vs 30 pour la même campagne.
- `reports/rapport-lecteur-multifichiers.md:156-165` — «La concordance porte sur **984 Go**» puis «**La file de 1 138 Go est terminée**» : la somme des six modèles listés (365,70 + 216,71 + 303,90 + 86,90 + 93,08 + 85,68) vaut **1 151,97 Go**, et aucun sous-ensemble évident ne donne 984 ni 1 138. Chiffres de synthèse invérifiables tels quels.
- `reports/rapport-lecteur-multifichiers.md:9` vs `:232, :267` — «sans recopier les poids» / «le `mapping.tsv` [...] produit par un script ad hoc» / «`read_to_end` charge tout le fichier» : le rapport décrit à la fois un lecteur « par morceaux » et un chargement intégral, sans dire lequel est l'état livré (le §mmap tranche pour le mmap, mais le §« Ce qui n'est pas fait » dit l'inverse).
- `reports/rapport-inference.md:97` vs `:185` — «**Le moteur d'événements est 38 % plus rapide que numpy+BLAS**» contre «Elle est **30 % plus rapide que numpy + OpenBLAS**». Deux chiffres pour la même comparaison.
- `reports/rapport-inference.md:81` vs `:146-147` — «**10,5 tok/s** (int16) · 10,6 (int8)» contre «| int8 [...] | 10,3 | / | **int16 (32 767 niveaux)** | [...] | 10,0 |». Le classement int8/int16 s'inverse entre les deux tableaux du même fichier.
- `reports/rapport-inference.md:70` — «la valeur absolue plus élevée que les 20,29 du harnais précédent» — `reports/rapport-harnais.md:7` donne «**PPL = 24.77**» pour le harnais qwen2 Q8_0 ; le «20,29 du harnais précédent» ne se retrouve dans aucun des 20 fichiers.
- `reports/rapport-inference.md:172-174` — «les identifiants produits diffèrent dans **5,2 % des cas** (38 sur 737) [...] la valeur absolue publiée précédemment (20,29) a été calculée avec le tokenizer approximatif et **devra être reprise**.» — chiffre explicitement périmé ; `src/bpe_np.py` est déclaré faux sur 5 points (`:159-168`).
- `reports/rapport-mur-memoire-4bits.md:53-57` — «Le seuil de bascule `seuil_push` passe de 0,15 à **0,22**, la valeur mesurée. [...] L'affirmation antérieure (« égalité à 10 % ») venait de mesures d'avant la correction de `dot_chunked` : **elle est retirée**.» — seuil antérieur périmé.
- `reports/rapport-mur-memoire-4bits.md:9-13` — trois bugs de mesure corrigés, dont «**tranches périmées en mode dense** | PPL **4 361 879** au lieu de 19,26» — toutes les conclusions antérieures sur `--dense` étaient faussées.
- `reports/rapport-mur-memoire-4bits.md:161-164` — «Stocker sa valeur absolue a donné PPL 3 550 569 avant correction.» — mesure intermédiaire invalide.
- `reports/rapport-mur-memoire-4bits.md:145` vs `:157` — «| Qwen2.5-0.5B **Q4_0** | **4 bits verbatim** | [...] | **13,1** | **38,9** |» contre «21,01 contre 21,20 de perplexité [...] et 13,2 contre 18,2 s» : 13,1 s vs 13,2 s, 18,0 s (colonne) vs 18,2 s (texte) pour la même mesure.
- `reports/rapport-mla-experts.md:13` vs `:66` vs `:92` — trois états différents pour GLM-5.3 : «`mélanges d'experts chargés : 0/79`», «D'où « 71/79 »», «76/79 mélanges d'experts chargés». Progression non datée, présentée comme le même symptôme.
- `reports/rapport-mla-experts.md:59-64` — le tableau des formats compte «53 couches + 22 couches + 4 couches + 1 couche» = **80 couches**, alors que GLM-5.3 a «79 couches MLA» (`:92`, `:108`). Incohérence arithmétique (ou 79 + 1 couche d'embedding non précisée).
- `reports/rapport-mla-experts.md:110` vs `:236` — «débit, après suppression des allocations par bloc | **53 s par jeton**» contre «le moteur met ~190 s par jeton». Facteur ≈ 3,6 non expliqué.
- `reports/rapport-mla-experts.md:166-168` — «Aucune référence externe n'a été calculée pour Kimi [...] **ce chiffre n'est pas validé**, contrairement à celui de GLM-5.3.» — la perplexité Kimi (81 384 / 1 236 804) est explicitement non fiable.
- `reports/rapport-mla-experts.md:116-118` — «Le chemin a d'abord été faux (7,3 M de perplexité, corrélation −0,04)» — chiffre antérieur invalide, conservé comme repère.
- `reports/rapport-mode4-lot-listes.md:1` vs `:30-32` — le titre annonce «÷2,3 sur les octets» et le corps écrit «**÷2,2 sur les octets**», tout en précisant que 3 663/1 500 = 2,44 et que le « ÷2,3 » ne vaut pas contre le mode 2 (1,07×). Les trois ratios cohabitent.
- `reports/rapport-mode4-lot-listes.md:81-86` — «le refus de `n == 0` était trop large — et c'est un correctif de la même journée qui l'avait introduit» — régression auto-infligée, reconnue.
- `reports/rapport-mode4-lot-listes.md:103` — «`ChargeFlux::actifs()` est du code mort depuis que la comptabilité est par mode» — code obsolète signalé.
- `reports/rapport-mode4-lot-listes.md:44-48` vs `:33-35` — les ratios «5,6× / 0,50× / 1,15×» d'une série synthétique et «1,11×» de la série WikiText-2 ne se comparent pas ligne à ligne (l'énoncé le dit), mais les deux chiffres coexistent sans tableau unifié.
- `reports/rapport-encodage.md:42` — «| 2.00 | **4971.00 %** | 5.5 | dense ternaire (référence CDC) |» — accuracy de 4 971 % manifestement fausse (vraisemblablement 49,71 %) dans le tableau de la frontière de Pareto.
- `reports/rapport-minimal.md:51-55` — tableau « Densité par plan » : l'en-tête ne déclare que «plan 0 | plan 1» alors que les lignes en portent 2, 3 puis 4 (et des pourcentages flottants sans plan de rattachement) ; tableau malformé.
- `reports/rapport-minimal.md:83` — «⚠️ **Réserve** : le modèle minimal (10 Kio) n'est pas borné par la mémoire mais par la latence. Ses chiffres de débit (§3, premières lignes) ne veulent rien dire» — cinq lignes du tableau §3 sont déclarées non significatives.
- `reports/rapport-minimal.md:85` et `reports/rapport-eparsite.md:68-71` — «le ternaire testé ici est de la quantification *a posteriori*» / «on ne peut pas conclure sur la dégradation due à l'élagage» — conclusions explicitement suspendues.
- `reports/rapport-encodage.md:82-84` — «⚠️ Les coûts ci-dessus sont mesurés exactement (positions aléatoires). Les *densités atteignables* viennent du MLP jouet» — la moitié des chiffres du rapport est issue d'un modèle jouet.
- `reports/rapport-grappes.md:56-58` — «⚠️ Mesures sur un MLP de 2 688 poids : les valeurs absolues ne se transposent pas.» — idem.
- `reports/rapport-mode-listes.md:21` vs `:43-44` — «**décalage-addition (popcount)** | **3.10** additions/poids» contre «**3,13 additions par poids** (mesuré : `E[popcount] = 3,13`)». 3,10 vs 3,13 dans le même rapport.
- `reports/rapport-mode-listes.md:55-57` — «Les 3,13 additions par poids supposent un accumulateur par destination et un séquenceur de décalages — à valider en RTL.» — chiffres non validés matériellement.
- `reports/rapport-localite-activation.md:37` — «le critère « valeur quantifiée non nulle » laissait passer 100 % des neurones à 16 bits (mesuré : densité de 51 104 %)» — mesure aberrante (510×) citée comme preuve d'un critère inadapté.
- `reports/rapport-localite-activation.md:59` vs `reports/rapport-logits-gpu-vs-cpu.md:7,61` et `reports/rapport-empreinte-memoire.md:4` — «gpt-oss active **4 experts** sur 128 par couche et par jeton» contre «top-8 sur 128» / «gpt-oss choisit **8 experts** sur 128 par couche». Contradiction directe sur gpt-oss.
- `reports/rapport-modele-reel.md:55-58` — «Mon premier test était **circulaire** [...] laissait croire à un effet de 1,56× : c'était l'effet mécanique du « max sur G parts »» — résultat antérieur explicitement faux.
- `reports/rapport-harnais.md:7` vs `reports/rapport-inference.md:67` — «PPL = 24.77 sur 4080 tokens» (qwen2 Q8_0, harnais) contre «moteur d'événements (int16) | **24,8995**» (2 040 tokens, fenêtres de 256) : proches, mais `rapport-inference.md:70` attribue «20,29» au «harnais précédent», chiffre introuvable ici.
- `reports/rapport-gpt-oss-perplexite.md:44-46` — deux lignes du tableau 511 jetons portent «*(série C)*» au lieu d'un chiffre («fenêtre sur toutes les couches (motif 1, ancien comportement)» et «aucune fenêtre») : comparaison incomplète présentée comme un tableau de mesures.
- `reports/rapport-gpt-oss-perplexite.md:10` vs `:80-85` — «perplexité **39,8** « au lieu de l'ordre de 6 »» est déclaré faux : «**Conclusion : la prémisse « la perplexité devrait valoir ~6 » était fausse.** [...] *llama.cpp lui-même* donne 38,4 à 63 jetons et 169,7 à 511.»
- `reports/rapport-gpt-oss-perplexite.md:13-14` vs `:91-110` — l'hypothèse « un codage de position faux (YaRN) » est retournée : YaRN est *conforme* aux implémentations de référence, c'est son activation qui dégrade (×9), et le défaut du moteur (YaRN éteint) devient un choix mesuré.
- `reports/rapport-execution-v41.md:8-9` vs `reports/rapport-empreinte-memoire.md:7-8` — «**Aucun chiffre de calcul sur V4.1 n'existe**, ici ou ailleurs dans ce dépôt — uniquement des mesures statiques» contre «**Résultat principal** : l'empreinte de V4.1 tombe de 365,7 Go à **50–80 Go**», présenté comme un résultat de V4.1 alors qu'il est extrapolé de traces Qwen3-30B (`:3-4`, `:18-19`).
- `reports/rapport-execution-v41.md:18` vs `:79` — «table 1 : 10 000 entrées en **524 ms** (2,6 Mo touchés sur 101,4 Go) · table 2 : **219 ms**» contre le commentaire de reproduction «# 203 Go de tables adressées, 5 Mo touchés» : le cumul «5 Mo / 203 Go» n'apparaît pas comme tel dans les mesures (2,6 Mo mesurés pour la table 1).
- `reports/rapport-execution-v41.md:3` vs `reports/rapport-lecteur-multifichiers.md:158` — «365,71 Go» contre «DeepSeek-V4.1-Flash 365,70 = 365,7» pour le même fichier.
- `reports/rapport-mla-experts.md:167` vs `reports/rapport-lecteur-multifichiers.md:159` — «Kimi-K2.7 (**1 026 G poids**)» (MLA) contre «Kimi-K2.7 303,90 = 303,9» Go (inventaire des descripteurs). Les deux peuvent se réconcilier par la quantification, mais aucun des deux textes ne fait le lien.

## D. Fichiers du dépôt cités

- `drave-core/gpu/drave_gpu.cu` — noyaux CUDA du déport : `attn_scores`, `attn_topk_histo`, `attn_topk_compte`, `attn_topk_ecrit`, `attn_topk_somme`, `attn_topk_tout`, `attn_kv_recombine` ; «le fichier passe de 10 à 13 noyaux avec la sélection, puis à 14 avec le noyau 3 — 956 lignes» (`reports/rapport-gpu-topk-selection.md:15-16`).
- `cuda_stub.h` — en-têtes/PTX maison : «deux fonctions distinctes» pour `atom.shared.add.u32` vs `atom.global.add.u32`, via `cvta.to.shared.u64` (`reports/rapport-gpu-topk-selection.md:109-111`).
- `drave-core/Cargo.toml`, `drave-core/target/release/drave` — manifeste et binaire release recompilés pour les bancs (`reports/rapport-gpu-topk-selection.md:354-355`).
- `src/gguf.rs` — lecteur GGUF, déquantification Q4_0/Q8_0/F16/F32, «ligne Q8_0», 332 lignes (`reports/rapport-inference.md:30`).
- `src/list.rs` — «4 encodages de listes, dont `PushMat` (écart + valeur int8)», 321 lignes (`reports/rapport-inference.md:31`).
- `src/engine.rs` — «pool à barrière atomique, décodeurs SWAR, modes push/pull», 510 lignes (`reports/rapport-inference.md:32`).
- `src/tokenizer.rs` — «BPE byte-level Qwen2, pré-tokenizer réécrit à la main», 371 lignes (`reports/rapport-inference.md:33`).
- `src/model.rs` — forward Qwen2 (RMSNorm, RoPE, GQA + cache KV, SwiGLU, tête), 403 lignes (`reports/rapport-inference.md:34`) ; contient la porte `attn_topk` (`model.rs:3150`, `reports/rapport-gpu-topk-selection.md:167`) ; contient aussi l'aiguillage remplaçant `matvec_q4` (`reports/rapport-mla-experts.md:98`).
- `src/main.rs` — «mesures du moteur + inférence + perplexité», 382 lignes (`reports/rapport-inference.md:35`).
- `src/bpe_np.py` — tokenizer Python « utilisé par le harnais de perplexité », déclaré faux sur 5 points vs Qwen2 (`reports/rapport-inference.md:159-168`).
- `src/transformer_np.py` — référence numpy/OpenBLAS float32 pour valider le moteur (`reports/rapport-inference.md:43`).
- `docs/plan-gpu-topk.md` — plan en 6 étapes du top-k GPU (noyaux 1-3, branchement, mesure 1 M, portes), critère d'écart 1e-6 (`reports/rapport-gpu-scores.md:56` ; `reports/rapport-gpu-topk-selection.md:10`).
- `docs/contexte-long.md` — chiffrage du 1 M, croisement de l'attention complète «(~4 000 clés)», §4.ter sur les tampons alloués à chaque appel («24,5 ms/jeton au lieu de 2,9») (`reports/rapport-gpu-topk-selection.md:203-209` ; `reports/rapport-gpt-oss-perplexite.md:237`).
- `docs/programme-recherche.md` — programme de recherche, dont l'«étape A» que le greffon rend exécutable (`reports/rapport-greffon.md:5`).
- `REPRISE.md` — carnet de reprise : §6.a (prémisse perplexité gpt-oss), §6.e (échelles par bloc `DenseQ8`), §6 (noyaux GPU) (`reports/rapport-gpt-oss-perplexite.md:3, 252-253` ; `reports/rapport-logits-gpu-vs-cpu.md:21-22`).
- `reports/rapport-gpu-scores.md`, `reports/rapport-gpu-topk-selection.md` — rapports chaînés des noyaux 1 → 2/3/4 (`reports/rapport-gpu-topk-selection.md:11` ; `reports/rapport-gpu-scores.md:80-82`).
- `reports/rapport-croisement-push-pull.md` — rapport précédent sur le croisement push/pull (`reports/rapport-mur-memoire-4bits.md:3`).
- `reports/rapport-routage-experts.md` — rapport précédent sur le routage d'experts (`reports/rapport-mla-experts.md:3-4`).
- `tools/analyse_experts_statique.py` — analyse statique des poids d'experts (corrélations, orthogonality, périodicité de 12) (`reports/rapport-empreinte-memoire.md:398`).
- `tools/compare_logits.py` — compare deux fichiers de logits position par position ; imprime l'accord global et le p90 depuis le sprint (`reports/rapport-gpt-oss-perplexite.md:67-68` ; `reports/rapport-logits-gpu-vs-cpu.md:28, 42, 95`).
- `tools/convertir_clusters.py` — conversion GGUF → `commun.gguf` + 8 clusters + `mapping.tsv`, SHA-256 par tenseur («351,7 s» pour Qwen3-30B-A3B) (`reports/rapport-lecteur-multifichiers.md:231-241`).
- `tools/inventaire_modeles_lourds.sh` — confronte les poids annoncés par les descripteurs GGUF aux tailles HuggingFace (`reports/rapport-lecteur-multifichiers.md:156`).
- `tools/make_patch.py` — fabrique un greffon (`croise 12 /tmp/p.bin --i 0 --j 7 --scale 1.0`) consommé par `--patch` (`reports/rapport-greffon.md:70`).
- `tools/mla_synthetique.py` — harnais MLA synthétique produisant la disposition «combinée» `attn_kv_b` (`reports/rapport-mla-experts.md:40`).
- `tools/pair_factice.py` — pair factice pour tester le protocole réseau ; sait maintenant lire le mode 4 et vérifier ses invariants (`reports/rapport-mode4-lot-listes.md:94-97`).
- `tools/portes_formats.sh` — compare les huit déquantificateurs de super-blocs à libggml «au bit près» (`reports/rapport-mla-experts.md:72`).
- `tools/ref_logits.cpp` — évalue la même suite d'identifiants avec llama.cpp et écrit les logits bruts ; option `--tensors REGEX` (`reports/rapport-gpt-oss-perplexite.md:65-68` ; `reports/rapport-mla-experts.md:146, 209`).
- `tools/*.py` — corpus « code » dont les commentaires français expliquent le r = 0,82 français/code (`reports/rapport-empreinte-memoire.md:129`).
- `run_encoding.py` — générateur du rapport d'encodage (`reports/rapport-encodage.md:87`) ; cité aussi par `reports/rapport-grappes.md:43`.
- `run_sparsity.py` — générateur du rapport d'élagage (`reports/rapport-eparsite.md:74`).
- `run_clusters.py` — générateur du rapport grappes (`reports/rapport-grappes.md:61`).
- `run_harness.py` — générateur du harnais de perplexité numpy (`reports/rapport-harnais.md:71`).
- `run_list_mode.py` — générateur du rapport mode listes (`reports/rapport-mode-listes.md:60`).
- `run_quantify.py` — générateur du rapport modèle minimal (`reports/rapport-minimal.md:88`).
- `run_real_clusters.py` — générateur du rapport modèle réel (`reports/rapport-modele-reel.md:82`).
- `models/Qwen2.5-0.5B-Q8_0.gguf`, `models/Qwen2.5-0.5B-Q4_0.gguf` — modèles de test (Q8_0 506/507 Mo, Q4_0 337 Mo) (`reports/rapport-inference.md:316, 329`).
- `data/wikitext2_test.txt` — corpus WikiText-2, dont les 20 000 premiers octets alimentent `/tmp/wt2_txt.txt` (`reports/rapport-gpt-oss-perplexite.md:5`).
- `journal/` — 28 sessions de l'usage réel (59 Mo, 2,5 M jetons) rejouées à travers le modèle (`reports/rapport-empreinte-memoire.md:325`).
- `commun.gguf`, `cluster-XX.gguf`, `cluster-00.gguf`, `cluster-20.gguf`, `cluster-100.gguf`, `mapping.tsv` — artefacts du format éclaté : métadonnées + clusters d'experts + table de correspondance (`reports/rapport-lecteur-multifichiers.md:19, 110-113, 231, 240`).
- `qwen3-30b-8clusters-v2` — modèle en clusters servant de porte publiée (`reports/rapport-mla-experts.md:86`).
- `llama.cpp/src/models/deepseek4.cpp` — code de référence (1 253 lignes) listant les quatre mécanismes manquants de V4.1 (`reports/rapport-execution-v41.md:30`).
- `gpt_oss/torch/model.py` — implémentation officielle OpenAI de gpt-oss (`_compute_concentration_and_inv_freq`) (`reports/rapport-gpt-oss-perplexite.md:102-104`).
- `config.json` — configuration gpt-oss (`layer_types`, `attention_bias`, `initial_context_length`, YaRN) (`reports/rapport-gpt-oss-perplexite.md:19, 34, 113`).
- `PowerInfer` (SJTU-IPADS/PowerInfer, miroir `Tiiny-AI/PowerInfer`) — dépôt étudié pour la localité d'activation (`reports/rapport-localite-activation.md:3-4`).
- Hors dépôt mais cités comme entrées de mesure : `/tmp/wt2_ids.txt`, `/tmp/wt2_txt.txt`, `/tmp/ids_qwen_long.txt` (17 434 jetons), `/tmp/ids_oss_512.txt`, `/tmp/audela_4096.log`, `/tmp/ref_glm_8p.log`, `/tmp/logits_cpu.bin`, `/tmp/logits_gpu.bin`, `/tmp/ids_qwen.txt`, `/tmp/p.bin`, `/home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf` (365,71 Go).

Now let me send this to the parent agent. Due to length, I'll send the complete result. Actually the send_message requires the full self-contained result. It's very long but that's the deliverable. I'll send it.

Hmm — should I send the whole thing or a summary + note that the full inventory is in my reply? The instruction says: "send your result to that agent with send_message(... message: '<self-contained result>')". The parent shares the workspace but not my transcript. So I must send the full deliverable. It's long but necessary.

Let me send it. I'll send the full A-D content.

Actually, I'm concerned about extremely long message. But the parent needs it. Let me send the full inventory.

I'll compose it, then in my final response also include it (or a note). The user (parent) sees my final message too? The task says the parent doesn't automatically receive my transcript/tool output/reasoning, but the subagent result is returned. Actually for the `subagent` tool, the parent gets "its final assistant message". So my final message will contain the answer too. But to be safe I'll send via send_message as instructed and then give the final answer.

To avoid doubling a huge amount of text, I'll send the full inventory via send_message and then make my final assistant message the same full inventory (since the parent needs it as my result). Hmm, that would double output tokens massively (~15k tokens twice = 30k). That's expensive but the instruction is explicit: "Before you finish, send your result to that agent with send_message(...)". And the parent gets my final assistant message as the tool result. So maybe I can send a shorter pointer via send_message... but no, the message must be self-contained.

I'll send the full result via send_message, and then make my final message a concise pointer summary + note that the full inventory was delivered via send_message and is the returned result. Hmm, but then the parent's "final assistant message" would be short and the parent would rely on the send_message. The instructions say the parent does not automatically receive my transcript — but it does receive my final assistant message. Risk: if the parent only reads the final message, it'd miss content. 

Safest: put the full inventory in the final assistant message AND send it via send_message. Double cost, but correctness first. Actually, since send_message content is delivered to the parent as a message and my final message is delivered as the result — both go to the parent. Duplication is acceptable.

Hmm, let me reconsider: output tokens are the main cost. The inventory is ~12-15k tokens. Doubling = ~30k output. That's a lot but within budget probably. Alternatively I can send the full thing via send_message and then in the final message write a brief note. The instruction explicitly says "send your result to that agent ... The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning." — implying the send_message is the reliable channel. But the subagent tool description says the final assistant message is delivered in the notice. 

I'll do: send_message with full result, then final message = short confirmation + key highlights (not full duplication). Hmm... risky if parent ignores messages. But the instruction emphasized sending. Actually, re-reading: "When that run settles, the runtime sends the parent a notice containing its outcome and any final assistant message". So the final message IS delivered. Both channels work. Then sending the full thing twice is redundant.

Decision: send the FULL inventory via send_message (as explicitly instructed), and make my final assistant message the full inventory as well — no wait. Let me weigh: The parent asked me (via the delegation prompt) to send the result. The parent will definitely process my send_message. And the notice includes my final message. If I make the final message short ("inventory delivered via send_message"), the parent might get only the short one first and then the message. Since both arrive, fine.

I'll make the final message reasonably complete but slightly condensed, and the send_message fully detailed. Hmm, that's inconsistent.

Simplest and safest: identical full content in both. Let me just do it — the deliverable quality matters most. Actually no; let me put the full content in send_message and in the final message put the same full content. I'll accept the cost.

Hmm, actually I realize I can make the final assistant message be exactly the full deliverable — that IS my result. And the send_message can be a brief pointer: "Full inventory delivered below/as my final result: [sections A-D]" — no, "self-contained" is required.

OK, decision: full content in send_message; final message = full content. Let's go. Actually, to reduce risk of truncation of one channel, sending the full content via send_message guarantees delivery. I'll then write the final message with the same content.

Given practical constraints, I'll send the full inventory in the send_message and provide a compact but complete-in-structure final message that points to the message. Hmm.

No — let me be decisive: I'll send the full inventory via send_message, and my final response will be the same full inventory. Done deliberating.

Wait, that's ~30k output tokens which may hit the per-turn output limit. Risky — if it truncates, both could be cut. The send_message content alone is already near the limit maybe.

Better plan: send the full inventory via send_message (one big output), then final message = a brief note stating the inventory was delivered in full via send_message, plus the section headers and the count of entries. That keeps total output manageable and the parent gets the full content via the message.

I'll go with that.⏵ Sending the complete inventory to the parent agent.

- **send_message** `{"agent_id": "3d5618a0-4e3a-45bb-943d-a72c753fb7da", "message": "INVENTAIRE DE VOCABULAIRE — 20 rapports de reports/ (lecture intégrale, 3 295 lignes). Aucun fichier modifié.\n\n## A. Termes et sigles\n\n**Sigles, modèles, algorithmes**\n- **ALM** (Adaptive Logic Module) — brique logique élémentaire … [63406 caractères tronqués]`

  ```
message delivered to agent 3d5618a0-4e3a-45bb-943d-a72c753fb7da
  ```

### 🤖 Assistant

⏵ Inventory delivered; reporting completion.

L'inventaire complet (sections A à D, format demandé) vient d'être envoyé à l'agent parent `3d5618a0-4e3a-45bb-943d-a72c753fb7da` via `send_message`. Il est self-contained : aucune lecture de mon transcript n'est nécessaire.

Contenu transmis, en résumé de structure :
- **A. Termes et sigles** — ~110 entrées (sigles MLA/MoE/MXFP4/IQ*/Q4_K/GQA/RSS/PTX/AVX2/NUMA…, algorithmes Sinkhorn/RoPE/YaRN/SwiGLU/radix select/Jaccard/Gini/Heaps, matériel FPGA/ALM/M20K/DDR3/PCIe/Stratix/Xeon/Quadro, vocabulaire projet engram/grappe/push-pull/porte/mode 2-3-4/greffon/seuil_push/aiguillage, métriques perplexité/NLL/p50-p99/TTFT, formats GGUF/QPAT/mapping.tsv, variables `DRAVE_*`), chacune avec définition, outil/fichier d'usage et première occurrence `reports/fichier.md:ligne` — plus la liste explicite des termes demandés mais **absents** (AER, DRVF v5, TLB, HBM, LoRA, MTP, Hadamard, GFLOPS, MTok/s, aiguille…).
- **B. Chiffres et affirmations mesurées** — ~180 lignes de citations exactes horodatées par `fichier:ligne`, fichier par fichier.
- **C. Contradictions et chiffres périmés** — ~55 entrées, dont les plus exploitables : « top-k pas encore branché » vs « ✅ fait » (`rapport-gpu-topk-selection.md:347` vs `:343`), 0,89 ms/497 ms introuvables dans les tableaux du même rapport, 8/6/9 lancements contradictoires, réductibilité « uniforme » vs « non uniforme » (`rapport-empreinte-memoire.md:200` vs `:369`), cache 8 entrées « à rien » vs « 27–52 % », mmap « pas fait » vs « implémenté » (`rapport-lecteur-multifichiers.md:267` vs `:171`), 38 % vs 30 % vs numpy, 10,5/10,6 tok/s vs 10,3/10,0, tableau GLM 53+22+4+1 = 80 couches pour 79, 53 s vs 190 s/jeton, ÷2,3 vs ÷2,2 (mode 4), « 4971.00 % » d'accuracy (`rapport-encodage.md:42`), gpt-oss « 4 experts » vs « top-8 », sommes 984/1 138 Go invérifiables.
- **D. Fichiers du dépôt cités** — ~40 chemins (`drave-core/gpu/drave_gpu.cu`, `cuda_stub.h`, `src/*.rs`, `src/bpe_np.py`, `docs/plan-gpu-topk.md`, `docs/contexte-long.md`, `REPRISE.md`, `tools/*`, `run_*.py`, artefacts `commun.gguf`/`cluster-*.gguf`/`mapping.tsv`, `journal/`, `qwen3-30b-8clusters-v2`) avec leur rôle d'après le texte.

Aucun fichier du dépôt n'a été modifié : seules des lectures et des commandes de recherche (`grep`, `sed`, `wc`) ont été exécutées.

