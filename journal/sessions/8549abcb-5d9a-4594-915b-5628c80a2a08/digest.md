# Session DSH — relecture

- identifiant : `8549abcb-5d9a-4594-915b-5628c80a2a08`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-02 15:03:29
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM en Rust qui exécute les projections sous forme de listes d'activation creuses plutôt que de produits scalaires denses).

TÂCHE : dépouille EXHAUSTIVEMENT ces 20 fichiers Markdown :
reports/rapport-optimisations-auto.md
reports/rapport-optimisations.md
reports/rapport-p0-flux.md
reports/rapport-parcimonie-imposee.md
reports/rapport-passage-a-l-echelle.md
reports/rapport-phase3-reparti.md
reports/rapport-placement-bits-kv.md
reports/rapport-precision.md
reports/rapport-prefill-par-lots.md
reports/rapport-prefill-reparti.md
reports/rapport-programme-evolutif.md
reports/rapport-routage-experts.md
reports/rapport-session-2026-09-30.md
reports/rapport-tete-garantie.md
reports/rapport-tete-restreinte.md
reports/rapport-transport-liste.md
reports/rapport-travail-reel.md
reports/rapport-v4-couches-0-1.md
reports/rapport-v4-hca.md
reports/rapport-valeur-unaire.md

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

⏵ Reading the 20 report files to build a full vocabulary inventory

I'll start by reading the files. Let me read them in batches.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-optimisations-auto.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-optimisations.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-optimisations-auto.md</path>
<type>file</type>
<content>
1: # Rapport — détection matérielle et configuration automatique
2: 
3: Session du 01/10 au 02/10. Ce qui a été **implémenté**, ce que chaque heuristique
4: s'appuie comme mesure, et ce qui a été retiré après essai.
5: 
6: ## Le module `materiel.rs`
7: 
8: `Materiel::detecter()` lit la machine sans charger de modèle :
9: 
10: | quoi | comment | pourquoi pas autrement |
11: |---|---|---|
12: | **cœurs physiques** | `/sys/devices/system/cpu/cpu*/topology/{core_id,physical_package_id}` | `available_parallelism` rend 40 threads logiques pour 20 cœurs |
13: | **paires hyperthread** | regroupement par `(paquet, cœur)` | il faut savoir quels threads partagent L1/L2 |
14: | **nœuds NUMA** | `/sys/devices/system/node/node*` | mémoire par nœud incluse |
15: | **caches** | `cpu0/cache/index*/{level,type,size}` | — |
16: | **GPU** | `nvidia-smi --query-gpu` | le pilote CUDA n'est ouvert que si on en a besoin |
17: | **NVLink** | `nvidia-smi nvlink -s` | 25,8 Go/s, 2× le PCIe |
18: | **RAM** | `/proc/meminfo` | — |
19: | **disques** | `df` + `findmnt` → périphérique blo
… [5603 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-optimisations.md</path>
<type>file</type>
<content>
1: # Moteur d'événements Rust — les 4 optimisations, et les 3 pièges
2: 
3: Moteur `drave-core` (Rust, **std seul**, zéro dépendance, 386 lignes de moteur).
4: Matrice réelle `blk.0.ffn_gate.weight` de Qwen2.5-0.5B-Q8_0 : 4864 entrées × 896
5: sorties, **4 303 745 événements** (ternaire issu des signes réels, densité 100 %).
6: Machine : 2 × Xeon E5-2687W v3 (20 cœurs / 40 CPU logiques), NUMA 2 nœuds.
7: 
8: ---
9: 
10: ## Les 4 optimisations
11: 
12: ### 1. Réduction incrémentale (fin du memset)
13: 
14: Chaque worker ne remet à zéro **que les destinations qu'il a touchées** ; le
15: demandeur ne réduit que la fenêtre réellement écrite. Coût d'un appel à vide :
16: **0,484 ms → 0,011 ms** (×44). C'est ce qui rend le débit *variable* exploitable :
17: un événement rare ne paie plus le prix d'un appel plein.
18: 
19: ### 2. Décodage SWAR par paquets de 8
20: 
21: Les écarts d'un octet (99,99 % des événements à forte densité) sont décodés **8 à
22: la fois dans un mot de 64 bits** : un seul test `w & 0x8080_8080_8080_8080` dit si
23: les 8 octets sont des varints 
… [7525 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Continuing with the next batch of reports

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-p0-flux.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-parcimonie-imposee.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-p0-flux.md</path>
<type>file</type>
<content>
1: # P0 — Le harnais de flux : compter ce qu'on paie, par provenance
2: 
3: **En une ligne** : les chemins **MLA** et **experts-IQ** annonçaient « 0
4: événement » alors qu'ils calculent des dizaines de milliards de produits par
5: jeton — le compteur manquait, pas le travail ; le moteur compte maintenant les
6: **paires** (poids × activation) par provenance (**attention / experts /
7: partagé**), et la première mesure dit une chose que la suite du plan doit
8: entendre : **sur ces deux chemins, le flux est dense** — 0 événement en listes,
9: la totalité des matrices est payée.
10: 
11: ## 1. Ce qui était muet, et pourquoi
12: 
13: `events_total()` ne comptait que le chemin **push** de `matvec` : `Σ row_ev[i]`
14: sur les sources actives, c'est-à-dire les poids **non nuls** réellement
15: multipliés. Trois chemins ne passaient jamais par là :
16: 
17: | chemin | ce qu'il fait | ce qu'il comptait |
18: |---|---|---|
19: | MLA (`attn_mla`) | projections de rang faible en **f32 plein** (`matvec_f32`) | rien — aucune liste n'est construite |
20: | experts **IQ** (`Source:
… [7212 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-parcimonie-imposee.md</path>
<type>file</type>
<content>
1: # Parcimonie imposée à l'inférence — la frontière mesurée
2: 
3: *Peut-on donner à un modèle **préentraîné** le débit variable d'un réseau à
4: décharge, sans rien réentraîner ?* Campagne mesurée sur Qwen2.5-0.5B Q8_0, avec
5: deux jeux de 1 024 tokens : **A** pour le réglage, **B** (jamais vu) pour la
6: vérification.
7: 
8: Tout est déterministe : mêmes tokens, même perplexité, au chiffre près. Les
9: comptes d'événements et les perplexités sont donc exacts ; seule la mesure de
10: **temps** est bruitée (la machine tournait sous une charge de 8 à 14).
11: 
12: ---
13: 
14: ## 1. Pourquoi cette campagne
15: 
16: Le cahier des charges promet un débit **variable** selon ce qui s'active. Nous
17: avons mesuré le contraire sur un LLM dense : **0,00 % d'activations nulles**, donc
18: un débit constant, et l'argument « on ne paie que ce qui s'active » restait
19: théorique. Deux moyens d'imposer la parcimonie à l'inférence, tous deux inspirés
20: des neurones à décharge, aucun ne demandant d'entraînement :
21: 
22: - **seuil** : écarter les activations sous u
… [5755 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading reports 5–6 of 20

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-passage-a-l-echelle.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-phase3-reparti.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-passage-a-l-echelle.md</path>
<type>file</type>
<content>
1: # Passer aux gros modèles : ce qui bloque, chiffré
2: 
3: > Question posée : que reste-t-il à améliorer sur le moteur événementiel pour
4: > faire tourner les plus gros modèles récents accessibles au public ?
5: > Réponse par les mesures, sur les modèles réellement présents sur cette machine.
6: 
7: ## 0. Le parc disponible, et ce que le moteur sait en ouvrir
8: 
9: | modèle | taille | types de tenseurs | lisible ? |
10: |---|---|---|---|
11: | Qwen2.5-0.5B Q8_0 | 0,53 Go | Q8_0 | ✅ |
12: | Qwen2.5-0.5B Q4_0 | 0,35 Go | Q4_0 | ✅ |
13: | Qwen2.5-VL-7B Q4_K_M | 4,5 Go | **Q4_K** 6,09 G + **Q6_K** 1,52 G | ❌ |
14: | DeepSeek-R1-Distill-14B Q4_K_M | 8,6 Go | Q4_K + Q6_K | ❌ |
15: | Qwen3-30B-**A3B** Q4_K_M (MoE) | 17,7 Go | Q4_K 25,35 G + Q6_K 5,17 G | ❌ |
16: | Qwen2.5-Coder-32B Q4_K_M | 18,9 Go | Q4_K 27,29 G + Q6_K 5,48 G | ❌ |
17: | **gpt-oss-120b MXFP4** (MoE) | 60,5 Go | **MXFP4** 114,66 G + Q8_0 2,11 G | ❌ |
18: 
19: Le moteur ne lit que `F32`, `F16`, `Q8_0` et `Q4_0`. **Aucun modèle récent ne
20: s'ouvre aujourd'hui** : l'écosystème public est en `Q
… [10876 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-phase3-reparti.md</path>
<type>file</type>
<content>
1: # Phase 3 — le calcul réparti redevient fidèle
2: 
3: **En une ligne** : deux processus qui se passent des flux calculent maintenant
4: **exactement** la même perplexité qu'un seul — écart **0,00e0** — après deux
5: corrections qui n'étaient pas celle que je croyais.
6: 
7: ## Le banc
8: 
9: Deux processus, localhost, modèle Qwen2.5-0.5B-Q8_0, 12 couches chacun, contexte
10: 256. Le pilote garde les couches 0..12, le nœud moteur applique 12..24 et renvoie
11: le flux ; le pilote norme, applique la tête et note la perplexité. La référence
12: est le même modèle calculé entièrement en local. Reproductible :
13: 
14: ```bash
15: ./drave models/Qwen2.5-0.5B-Q8_0.gguf --flux-serveur 45733 &
16: ./drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl-reparti 127.0.0.1:45733 \
17:         --couches-locales 12 --limit 40 --ctx 256
18: ```
19: 
20: 40 jetons suffisent à trancher : la locale vaut 144,8289, et un découpage fidèle
21: doit redonner ce chiffre, pas un chiffre « proche ».
22: 
23: ## Le défaut que je croyais, et le défaut réel
24: 
25: Je suis parti d'une hypothèse l
… [2502 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading reports 7–8 of 20

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-placement-bits-kv.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-precision.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-placement-bits-kv.md</path>
<type>file</type>
<content>
1: # Où mettre les bits du cache KV : la courbe complète
2: 
3: **En une ligne** : à taille ÉGALE, mettre les bits sur les **clés** plutôt que sur
4: les valeurs change l'erreur d'un facteur **130 à 840** — et les clés en f16
5: donnent 39 % de la taille f32 pour **+0,018 %**.
6: 
7: ## Le tableau
8: 
9: Qwen2.5-0.5B-Q8_0, 8 191 jetons notés, contexte 8 192. « Octets par élément » =
10: octets par position et par dimension de tête, pour la paire clé + valeur (échelle
11: par bloc de 32 comprise).
12: 
13: | clés | valeurs | octets/élément | % du f32 | perplexité | écart |
14: |---|---|---|---|---|---|
15: | f32 | f32 | 8 | 100 % | **14,2339** | référence |
16: | **f32** | **int8** | 5,125 | 64 % | **14,2372** | **+0,023 %** |
17: | **int8** | **f32** | 5,125 | 64 % | 14,6622 | **+3,01 %** |
18: | f32 | int4 | 4,625 | 58 % | 14,2994 | +0,46 % |
19: | int4 | f32 | 4,625 | 58 % | 69,0464 | **+385 %** |
20: | int8 | int8 | 2,25 | 28 % | 14,6667 | +3,04 % |
21: | **f16** | **int8** | **3,125** | **39 %** | **14,2365** | **+0,018 %** |
22: | int4 | int4 | 1,25 | 1
… [9067 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-precision.md</path>
<type>file</type>
<content>
1: # Drave — la sparsité peut-elle acheter de la précision ?
2: 
3: Modèle minimal (MLP 32→64→10, 2688 poids), référence float **76.07 %**.
4: 
5: Protocole : **prune → retrain (masque fixe) → quantize → refit d'échelle**.
6: 
7: ## Modèle de coût
8: 
9: Un poids ternaire non nul ne porte qu'un signe, donc un encodage creux coûte :
10: 
11: ```
12: bitmap (1 bit/poids) + k bits par non-nul   =   1 + k·d   bits/poids
13: ```
14: 
15: À densité donnée, **on peut dépenser les bits économisés en précision** au lieu
16: de les dépenser en zéros. C'est la forme utile de l'intuition « plus de nœuds ».
17: 
18: ## Résultats (triés par coût)
19: 
20: | Encodage | k | Densité | b/poids | Accuracy | tok/s 7B (1 carte) |
21: |---|---|---|---|---|---|
22: | creux 1 bits d=0.125 | 1 | 8.4 % | 1.08 | 60.06 % | 10.2 **◀** |
23: | creux 1 bits d=0.250 | 1 | 16.8 % | 1.17 | 64.84 % | 9.5 **◀** |
24: | creux 2 bits d=0.125 | 2 | 11.8 % | 1.24 | 65.04 % | 8.9 **◀** |
25: | creux 1 bits d=0.500 | 1 | 26.6 % | 1.27 | 48.63 % | 8.7 |
26: | creux 3 bits d=0.125 | 3 | 12.3 % | 1.37 | 67.29 
… [3032 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading reports 9–10 of 20

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-prefill-par-lots.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-prefill-reparti.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-prefill-par-lots.md</path>
<type>file</type>
<content>
1: # Préremplissage par lots : ce que le GEMM apporte vraiment
2: 
3: > Chantier 4 du plan de reprise. Le préremplissage est le mur n° 1 du contexte
4: > long (`docs/contexte-long.md` : 4,5 h à 32 k, 1 234 h à 1 M en séquentiel) : le
5: > moteur traitait **un jeton à la fois**, donc chaque matrice de poids était relue
6: > pour chaque jeton.
7: 
8: ## 1. Ce qui a été fait
9: 
10: | pièce | rôle |
11: |---|---|
12: | `Pool::gemm_dense_i8` | produit matrice-matrice int8 : une tranche de lignes par fil, tout le lot servi par la même lecture de ligne |
13: | `Pool::gemm_dense_q4` | même chose pour les matrices 4 bits (experts MXFP4 de gpt-oss, Q4_K de Qwen) |
14: | `Model::forward_lot` | un avant complet pour `t` jetons : projections en lot, attention toujours par jeton (elle est causale), FFN dense en lot |
15: | **regroupement des experts** | les jetons qui ont choisi le même expert sont traités ensemble : la matrice de l'expert est lue une fois pour le groupe |
16: | `--lot N` | taille du lot (1 = chemin historique jeton par jeton) |
17: 
18: ## 2. Justesse
19
… [10277 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-prefill-reparti.md</path>
<type>file</type>
<content>
1: # Phase 3.4 — le préremplissage par LOTS sur le fil
2: 
3: **En une ligne** : un préremplissage de 256 jetons traverse désormais le réseau en
4: **4 lots** (ou un seul) au lieu de 255 flux, et le calcul coupé redonne exactement
5: le calcul local — **écart 0,00e0**.
6: 
7: ## Le problème
8: 
9: Le transport était séquentiel : un flux par jeton, donc un aller-retour par jeton.
10: Un préremplissage de N jetons payait N fois la latence, alors que la latence est
11: précisément le seul poste qui compte (`attente ≈ calcul distant + 3,2 × latence
12: par message`, mesuré dans `reports/rapport-transport-liste.md`). Avec 60 ms
13: d'aller-retour, 256 jetons coûtaient 15 secondes d'attente pure.
14: 
15: ## Le mode 3 du protocole
16: 
17: ```
18: en-tête   magie u32 · version u8 (4) · mode u8 (3 = LOT) · plage (2 × u32)
19:           position u32 (celle du PREMIER jeton) · n u32 (nombre d'ÉTATS)
20:           échelle f32 · et le contrat d'activation (niveaux, seuil, top-k,
21:           renorm, 7 top-k par projection, attn/qk/moe top-k)
22: corps     n × dimension 
… [4590 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading reports 11–12 of 20

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-programme-evolutif.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-routage-experts.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-programme-evolutif.md</path>
<type>file</type>
<content>
1: # Programme « journaliser, faire évoluer » — ce que la mesure autorise
2: 
3: Évaluation du programme : *journaliser les flux d'activation, construire et
4: entraîner des versions concurrentes en parallèle sur les ressources inutilisées,
5: avec moins de couches, des grappes par expertise, des portions récursives, et un
6: apprentissage de nouveaux nœuds par rétroaction sur la couche antérieure.*
7: 
8: Tout ce qui suit est mesuré sur ce dépôt, ou explicitement marqué comme
9: raisonnement.
10: 
11: ---
12: 
13: ## 1. Journaliser : c'est fait, et c'est presque gratuit
14: 
15: | | Mesure |
16: |---|---|
17: | Capteur de co-activation branché sur une projection | **+3,0 %** (96,75 s → 99,64 s sur 1 025 tokens) |
18: | Journal complet des entrées d'une couche | 2048 × 896 × 4 o = **7 Mo pour 2 048 tokens** |
19: | Journal des activations de toutes les couches (24) | ~1,2 Mo/token, soit 19 Mo/s à 15,8 tok/s |
20: 
21: **La traçabilité totale ne demande pas de journaliser les événements.** Les poids
22: sont statiques et les événements en sont une fonction d
… [6412 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-routage-experts.md</path>
<type>file</type>
<content>
1: # Rapport — le routage des experts était faux pour quatre gros modèles sur cinq
2: 
3: Session du 01/10 au 02/10, en autonomie. Question posée au départ : « pourquoi
4: V4-Flash ne se charge-t-il pas ? » La réponse s'est révélée plus large.
5: 
6: ## 1. Ce qui a été trouvé
7: 
8: Le moteur routait **tous** les mélanges d'experts avec une seule convention,
9: choisie par un booléen : « softmax sur tous, top-k, renormalisation » — sauf
10: gpt-oss, « top-k sur les logits bruts, softmax sur les k ». Or les modèles de
11: cette machine en déclarent **quatre**, et deux d'entre eux ne se ramènent à
12: aucune des deux :
13: 
14: | modèle | arch | `expert_gating_func` | ce que le moteur faisait |
15: |---|---|---|---|
16: | Qwen3-30B-A3B | `qwen3moe` | absent → softmax | softmax ✓ |
17: | Qwen3-235B-A22B | `qwen3moe` | absent → softmax | softmax ✓ |
18: | gpt-oss-120b | `gpt-oss` | *(codé en dur)* | top-k brut + softmax, **biais compris** ✗ |
19: | Kimi-K2.7-Code | `deepseek2` | **2 — sigmoïde** | softmax ✗ |
20: | GLM-5.3 / -Flash | `glm-dsa`, `glm5next` | **2 — 
… [8920 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading reports 13–14 of 20

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-session-2026-09-30.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tete-garantie.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-session-2026-09-30.md</path>
<type>file</type>
<content>
1: # Session du 30/09 — index des chantiers
2: 
3: Trois créneaux : 10h06–11h42 (time-box de 2 h), 11h46–15h00 puis 15h07–18h00
4: (autonomie et parallélisme). Les commits, les campagnes de mesure lourdes et les
5: relectures déléguées sont comptés dans le journal ; ce document est l'index des
6: chantiers, pas le décompte. Chaque chiffre a son rapport ; ceci est l'index.
7: 
8: ## Ce qui est livré
9: 
10: | chantier | résultat | rapport |
11: |---|---|---|
12: | **Calcul réparti fidèle** | écart local/réparti **0,00e0** — 144,8289 des deux côtés à 40 jetons, 9,5146 à 1 024 | `rapport-phase3-reparti.md` |
13: | **Préremplissage par LOTS** (mode 3) | 256 jetons en **4 lots** (ou 1 seul) → 0,00e0 ; **18× plus rapide** qu'un flux par jeton sur un lien à 20 ms | `rapport-prefill-reparti.md` |
14: | **Transport en listes** | dense 3 663 octets → **1 629** par flux (÷2,3) pour 1,3 % d'écart à 1 024 jetons | `rapport-transport-liste.md` |
15: | **où mettre les bits du cache KV** | à taille ÉGALE : clés f32 + valeurs int8 **+0,023 %** contre **+3,01 %** pour l'inve
… [5806 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tete-garantie.md</path>
<type>file</type>
<content>
1: # Rapport — restriction de tête GARANTIE : exacte, et sans gain
2: 
3: Chantier 2 de la session. La question posée était précise : peut-on ne pas
4: calculer tous les logits **sans jamais changer la sortie**, en chargeant
5: dynamiquement les logits manquants, avec une borne de Cauchy-Schwarz sur les
6: lignes hors liste et une extension par paliers quand la borne ne conclut pas ?
7: 
8: **Réponse : oui, c'est implémenté et exact — et non, ça ne fait rien gagner.**
9: La borne est 12,6 fois plus lâche que le logit maximal sur les poids réels, donc
10: toutes les lignes restent candidates et le moteur finit par tout calculer.
11: 
12: ## 1. Ce qui est implémenté
13: 
14: `--tete-garantie <fichier>` (`logits_garanti`, `drave-core/src/model.rs`) :
15: 
16: 1. une passe unique calcule `||w_i||` pour les 151 936 lignes de la tête et les
17:    trie par norme décroissante ;
18: 2. à chaque jeton, les logits de la liste de candidats sont calculés ;
19: 3. toute ligne non calculée est bornée par `||w_i|| · ||h||` (Cauchy-Schwarz dans
20:    la même unité que le produ
… [4875 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading reports 15–16 of 20

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tete-restreinte.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-transport-liste.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tete-restreinte.md</path>
<type>file</type>
<content>
1: # Rapport — restreindre la tête de sortie : ce qui marche, ce qui ne marche pas
2: 
3: Session du 01/10 au 02/10. Question posée : peut-on calculer moins de logits que
4: tout le vocabulaire **sans jamais changer la sortie** — « charger dynamiquement
5: les logits manquants ou faire du JIT », à défaut d'y être explicitement
6: contraint ?
7: 
8: **Réponse : non, pas avec une garantie exacte.** Trois voies ont été explorées,
9: implémentées et mesurées. Une seule survit, et elle change la sortie — ce qui la
10: qualifie comme *génération contrainte*, pas comme optimisation.
11: 
12: ## Ce qui est mesuré d'abord : le vocabulaire utile
13: 
14: | jetons lus (français) | identifiants distincts | % du vocabulaire |
15: |---|---|---|
16: | 10 000 | 1 462 | 0,96 % |
17: | 100 000 | 4 659 | 3,07 % |
18: | 1 000 000 | 15 768 | 10,38 % |
19: | 3 050 991 | **19 793** | **13,03 %** |
20: 
21: Exposant de Heaps ≈ **0,21** : atteindre 50 % du vocabulaire demanderait des
22: milliards de jetons. **13 % est un plafond de fait.**
23: 
24: Et le rang du vrai token, seule mes
… [4781 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-transport-liste.md</path>
<type>file</type>
<content>
1: # Phase 3.2 — transporter la LISTE au lieu du vecteur
2: 
3: **En une ligne** : le flux peut voyager en liste creuse — **897 octets au lieu de
4: 3 623** à seuil 5 %, et **1 568** avec des indices par écarts — mais jeter des
5: canaux coûte cher (**×1,8 de perplexité** à ce seuil), et la courbe est là pour
6: dire où.
7: 
8: ## Le protocole, mesuré
9: 
10: Deux modes dans le même en-tête (39 octets à l'époque de ces mesures, **79** depuis que les top-k voyagent) — magie, version, mode, plage,
11: position, dimension, échelle, **et les réglages d'activation** :
12: 
13: | mode | contenu | octets par flux (Qwen2.5-0.5B, 896 canaux) |
14: |---|---|---|
15: | 0 · dense f32 | `896 × f32` | **3 623** (39 + 3 584) |
16: | 1 · listes | `n × (indice u16 · valeur i16)` | 39 + 4 × actifs |
17: 
18: Le mode 1 est le format du disque, à l'octet près. La réponse est encodée comme
19: la demande : un pair qui parle en listes reçoit des listes.
20: 
21: ## La courbe (40 jetons, 12 couches de chaque côté)
22: 
23: | seuil | activité | octets/flux (aller) | octets/flux (reto
… [11908 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading reports 17–18 of 20

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-travail-reel.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-v4-couches-0-1.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-travail-reel.md</path>
<type>file</type>
<content>
1: # Le moteur est-il prêt pour du vrai travail ?
2: 
3: > Deux tests réels, avec un modèle de 30,5 G paramètres (Qwen3-30B-A3B, MoE
4: > top-8, Q4_K_M) sur CPU, 16 fils, lecture en place — aucune copie.
5: 
6: ## Les deux tests
7: 
8: **1. Question en français, gabarit de conversation.**
9: 
10: ```
11: <|im_start|>user
12: Explique en trois phrases pourquoi le ciel est bleu.<|im_end|>
13: <|im_start|>assistant
14: Le ciel est bleu parce que les molécules de l'atmosphère diffusent la lumière
15: du soleil. La lumière bleue a une longueur d'onde plus courte que les autres
16: couleurs, donc elle est diffusée plus efficacement que les autres couleurs.
17: C'est cette diffusion de la lumière bleue dans toutes les directions qui fait
18: que nous voyons le ciel comme bleu.<|im_end|>
19: ```
20: 
21: Trois phrases, exactes, arrêt propre sur `<|im_end|>`. 89 jetons en 15,8 s
22: (**5,62 tok/s**), premier jeton en 166 ms.
23: 
24: **2. Génération de code, réponse vérifiable.**
25: 
26: ```
27: def mediane(liste):
28:     triee = sorted(liste)
29:     n = len(triee)
30:
… [4679 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-v4-couches-0-1.md</path>
<type>file</type>
<content>
1: # V4-Flash, couches 0 et 1 — la première comparaison étage par étage
2: 
3: **En une ligne** : les deux premières couches de **DeepSeek-V4-Flash** tournent
4: dans Drave et **concordent avec llama.cpp** — hyper-connexions à **1e-7**,
5: attention et sortie groupée à **0,99999** de corrélation — et cette comparaison a
6: trouvé **trois bugs** qu'aucun test interne n'aurait vus : un `attn_norm` manqué,
7: un puits mis à l'échelle, et la **mauvaise convention RoPE**.
8: 
9: ## 1. Pourquoi ces deux couches
10: 
11: `attention.compress_ratios` de V4-Flash : **21 couches CSA** (ratio 4),
12: **20 couches HCA** (ratio 128), **3 couches brutes** (0, 1, 43). Les couches 0 et
13: 1 n'ont donc **pas** besoin de la compression — ni de P4 ni de P5 — pour être
14: exécutées et comparées. C'est le seul endroit du modèle où la chaîne complète
15: (embarquement → hyper-connexions → MLA V4 → puits → dé-rotation → sortie groupée
16: → experts → hyper-connexions) peut être validée **avant** d'écrire la
17: compression.
18: 
19: ## 2. Le harnais
20: 
21: | pièce | ce qu'elle fai
… [4682 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading reports 19–20 of 20

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-v4-hca.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-valeur-unaire.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-v4-hca.md</path>
<type>file</type>
<content>
1: # Les compresseurs de DeepSeek-V4 (HCA et CSA), validés contre llama.cpp
2: 
3: **En une ligne** : la couche 3 de V4-Flash (première couche **compressée**, ratio
4: 128) tourne et **concorde avec llama.cpp** — corrélation **0,999992** sur la
5: sortie d'attention au 128ᵉ jeton, c'est-à-dire **au premier bloc compressé
6: complet** — et cette validation a trouvé **un quatrième bug** : la dé-rotation
7: utilisait la base RoPE des couches brutes au lieu de celle des couches
8: compressées.
9: 
10: ## 1. Ce qu'est HCA (ratio 128), d'après la référence
11: 
12: `attention.compress_ratios` de V4-Flash : 21 couches **CSA** (ratio 4), 20
13: couches **HCA** (ratio 128), 3 brutes (0, 1, 43). HCA est le régime simple :
14: 
15: 1. Chaque jeton produit une **valeur** (`attn_compressor_kv`) et une **porte**
16:    (`attn_compressor_gate`) de 512 dimensions.
17: 2. À la porte s'ajoute une **`ape`** — une ligne apprise par rang dans le bloc
18:    (`pos % ratio`), de forme `[512, 128]`.
19: 3. Quand un bloc de 128 jetons est complet, chaque **canal** fait son propre
20:    softma
… [7500 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-valeur-unaire.md</path>
<type>file</type>
<content>
1: # Drave — éliminer la valeur par répétition d'adresse ?
2: 
3: Modèle mesuré : **qwen2** quantifié **Q4_0** (166 matrices 2-D).
4: Les niveaux sont lus *tels que stockés* (−8..+7), avant mise à l'échelle.
5: 
6: ## 1. Distribution réelle des niveaux
7: 
8: - zéros : **12.9 %** des poids (densité 87.1 %)
9: - `E[|v|]` sur les non-nuls : **3.02**
10: - `E[popcount(|v|)]` : **1.39**
11: 
12: | \|v\| | Part des poids | Part des non-nuls |
13: |---|---|---|
14: | 1 | 23.72 % | 27.2 % |
15: | 2 | 19.54 % | 22.4 % |
16: | 3 | 14.84 % | 17.0 % |
17: | 4 | 10.53 % | 12.1 % |
18: | 5 | 7.06 % | 8.1 % |
19: | 6 | 4.54 % | 5.2 % |
20: | 7 | 3.84 % | 4.4 % |
21: | 8 | 3.05 % | 3.5 % |
22: 
23: ## 2. Coût par poids non nul
24: 
25: | Stratégie | Bits stockés | Opérations |
26: |---|---|---|
27: | positionnel (4 bits) | 4,00 | 1,00 |
28: | **unaire (répétition d'adresse)** | **2.02** | **3.02** |
29: | plans binaires (popcount) | 1.39 | 1.39 |
30: | **hybride (unaire pour \|v\|=1, puis plans)** | **1.12** | **1.12** |
31: 
32: ## 3. Seuil de bascule
33: 
34: L'unaire gagne 
… [3647 caractères tronqués]
  ```

### 🤖 Assistant

⏵ All 20 files read; now extracting exact first occurrences and repo paths via grep

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re,os\nfiles=\"\"\"reports/rapport-optimisations-auto.md\nreports/rapport-optimisations.md\nreports/rapport-p0-flux.md\nreports/rapport-parcimonie-imposee.md\nreports/rapport-passage-a-l-echelle.md\nreports/r … [2821 caractères tronqués]`

  ```
'AER'                        reports/rapport-optimisations.md:166  | AER) : le seul dédoublonnage justifié, pour le multi-cartes.
'KV'                         reports/rapport-optimisations-auto.md:51  | ### Cache KV : f32 tant qu'il tient, int8 au-delà
'MoE'                        reports/rapport-p0-flux.md:49  | | Qwen2.5-0.5B Q8_0 | experts | 0 | pas de MoE ✅ |
'MLA'                        reports/rapport-optimisations-auto.md:56  | Mesuré : le KV de MLA de V4.1 pèse **90 Ko par jeton en F16**, soit 96,6 Go à 1 M
'GGUF'                       reports/rapport-passage-a-l-echelle.md:204  | # types de tenseurs d'un GGUF (script de recensement)
'DRVF'                       ABSENT
'NLL'                        reports/rapport-routage-experts.md:114  | | | perplexité | corrélation des logits (pos. 0) | écart \|NLL\| moyen | accord top-1 |
'RSS'                        ABSENT
'VRAM'                       reports/rapport-optimisations-auto.md:67  | ### Cache d'experts VRAM : ce que la carte peut donner
'TLB'                        reports/rapport-passage-a-l-echelle.md:160  | TLB. Des pages de 2 Mo diviseraient ce coût par 512.
'NUMA'                       reports/rapport-optimisations-auto
… [19737 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -o -E '(`[^`]*\\.(md|rs|py|sh|cpp|toml|json|gguf|txt|bin)`)|((tools|src|docs|reports|drave-core|colab)/[A-Za-z0-9_./-]+)' reports/rapport-optimisations-auto.md reports/rapport-optimisations.md reports/rapport-p0-flux.md repor … [664 caractères tronqués]`

  ```
reports/rapport-optimisations-auto.md:118:`rapport-tete-restreinte.md`
reports/rapport-optimisations-auto.md:6:`materiel.rs`
reports/rapport-optimisations.md:159:`rapport-cpu-aer.md`
reports/rapport-p0-flux.md:118:`tools/portes.sh`
reports/rapport-passage-a-l-echelle.md:98:`gpt-oss-120b-MXFP4.gguf`
reports/rapport-placement-bits-kv.md:148:`tools/aiguille.py`
reports/rapport-placement-bits-kv.md:170:drave-core/target/release/drave
reports/rapport-precision.md:80:`run_precision.py`
reports/rapport-prefill-par-lots.md:152:src/engine.rs
reports/rapport-prefill-par-lots.md:168:`REPRISE.md`
reports/rapport-prefill-par-lots.md:4:`docs/contexte-long.md`
reports/rapport-prefill-reparti.md:102:`reports/rapport-transport-liste.md`
reports/rapport-prefill-reparti.md:12:`reports/rapport-transport-liste.md`
reports/rapport-prefill-reparti.md:53:`tools/proxy_latence.py`
reports/rapport-routage-experts.md:107:`tools/ref_logits.cpp`
reports/rapport-routage-experts.md:169:`tools/mla_synthetique.py`
reports/rapport-routage-experts.md:43:`drave-core/src/model.rs`
reports/rapport-session-2026-09-30.md:12:`rapport-phase3-reparti.md`
reports/rapport-session-2026-09-30.md:13:`rapport-prefill-reparti.md`
r
… [1332 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying key figures and checking a few remaining terms

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for p in '15,1757' '15,6017' '341 Go' '365 Go' '19,3045' '19,5633' '1 629' '1 589' '1 568' '3 663' '3 623' '96,6 Go' '90 Ko' '9,66 Go/s' '10,4 Go/s' '28,7' '42 617 589' '39,8' '41,6' '32 tok/s' '5,62 tok/s' '5,6 ' '11,5' '17 869' 'de … [889 caractères tronqués]`

  ```
=== 15,1757
reports/rapport-routage-experts.md:66:| gpt-oss-120b ctx 256 | 15,1757 | **15,6017** | **changée** — voir ci-dessous |
reports/rapport-routage-experts.md:72:dans le softmax. **15,1757 était auto-cohérent, pas juste.**
reports/rapport-session-2026-09-30.md:92:Qwen ctx 256 = **19,3885** · gpt-oss ctx 256 = **15,1757** · gpt-oss avec
=== 15,6017
reports/rapport-p0-flux.md:118:| `--config` annonce la bonne liste de manques | ✅ **franchie** — elle ne l'était pas : `attn_sinks` était compté comme un manque V4, donc gpt-oss répondait « calculable : NON » alors que sa porte (15,6017) tourne. Corrigé, et la porte est désormais **exécutée par `tools/portes.sh`** |
reports/rapport-routage-experts.md:66:| gpt-oss-120b ctx 256 | 15,1757 | **15,6017** | **changée** — voir ci-dessous |
reports/rapport-routage-experts.md:126:| drave, YaRN **à retardement** (le défaut) | **15,6017** |
reports/rapport-routage-experts.md:162:  elle doit confirmer ou contredire 15,6017. C'est la seule mesure qui tranche
=== 341 Go
reports/rapport-routage-experts.md:39:modèle de 341 Go pour un modèle **dense**, et l'exécutait sans un seul expert.
=== 365 Go
reports/rapport-optimisations-auto.md:95:le cache.
… [5583 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn -E 'IQ|Source::Dequant|déquantif|porte|valuée|valeur unaire|trames|trame|R1|NLL|DSA|HCA|CSA|indexeur|lightning' reports/rapport-p0-flux.md reports/rapport-passage-a-l-echelle.md reports/rapport-v4-hca.md reports/rapport-v4-c … [155 caractères tronqués]`

  ```
reports/rapport-p0-flux.md:3:**En une ligne** : les chemins **MLA** et **experts-IQ** annonçaient « 0
reports/rapport-p0-flux.md:20:| experts **IQ** (`Source::Dequant`) | **déquantification** du super-bloc puis produit f32 | rien |
reports/rapport-p0-flux.md:23:Un modèle MLA (GLM-5.3, Kimi-K2.7) ou à experts IQ annonçait donc
reports/rapport-p0-flux.md:25:sert à décider ce qu'on déporte, ce qu'on découpe et ce qu'on simplifie.
reports/rapport-p0-flux.md:38:branches : push, int8 dense, 4 bits, GPU), `matvec4_ou_iq` (déquantification IQ
reports/rapport-p0-flux.md:51:Et la porte du dépôt ne bouge pas : **Qwen2.5-0.5B ctx 256 = 19,3885**, la même
reports/rapport-p0-flux.md:69:   sur MLA et sur IQ, Drave ne conduit **aucune liste** aujourd'hui. La vision
reports/rapport-p0-flux.md:75:   sélectionné est payé **entier**, déquantifié en f32. C'est le poste où une
reports/rapport-p0-flux.md:76:   forme en listes rapporterait le plus.
reports/rapport-p0-flux.md:116:| porte du plan | état |
reports/rapport-p0-flux.md:118:| `--config` annonce la bonne liste de manques | ✅ **franchie** — elle ne l'était pas : `attn_sinks` était compté comme un manque V4, donc gpt-oss répondait « calculable : NO
… [4159 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking remaining terminology and project-specific jargon

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for p in 'nope' 'ape' 'dé-rotation' 'dé-tourn' 'latent' 'lightning' 'hebbien' 'k-moyennes' 'OpenBLAS' 'Pareto' 'LUT' 'MAC ' 'PE ' 'super-bloc' 'Q8_1' ' P4' ' P5' ' P6' ' P1' ' P2' 'R4' 'mode 2' 'protocole v5' 'phase 3' 'sparsité' 'to … [1796 caractères tronqués]`

  ```
nope  ==>  reports/rapport-v4-hca.md:52:tournée) alors que les **448 premières** (nope) étaient justes à 0,4 %. Signature
ape  ==>  reports/rapport-optimisations.md:156:   FPGA à 124 MHz × 32 PEs taperait 4 G év/s — la carte gagne par le watt, pas par
dé-rotation  ==>  reports/rapport-v4-couches-0-1.md:15:(embarquement → hyper-connexions → MLA V4 → puits → dé-rotation → sortie groupée
dé-tourn  ==>  reports/rapport-v4-couches-0-1.md:40:| `attn_derope` (sortie d'attention dé-tournée) | 0 | **0,999996** | 1,9e-2 |
latent  ==>  reports/rapport-p0-flux.md:79:   payé à **chaque** jeton. C'est structurel (le cache est latent, la remontée
lightning  ==>  reports/rapport-v4-hca.md:96:L'indexeur (« lightning indexer ») note chaque bloc compressé et n'en garde que
hebbien  ==>  reports/rapport-programme-evolutif.md:67:  des directions de la trace hebbienne, y compris son résidu non linéaire, sont
k-moyennes  ==>  reports/rapport-programme-evolutif.md:32:tokens de WikiText-2, k-moyennes sur les vecteurs d'entrée du FFN :
OpenBLAS  ==>  reports/rapport-programme-evolutif.md:112:sait *ajuster une lecture* (moindres carrés, algèbre linéaire, OpenBLAS à
Pareto  ==>  reports/rapport-precision.md:4
… [11380 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Final verification pass on remaining acronyms and symbols

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for p in 'CDC' 'harnais' 'banc' 'porte du dépôt' 'porte verte' 'non-régression' 'drapeau' 'options-strict' 'DRAVE_PRELIRE_TOUT' 'DRAVE_GPU' 'DRAVE_KV_V_F32' 'DRAVE_DEBUG_ETAT' 'ggml_soft_max_add_sinks' 'ggml_soft_max_ext' 'ggml_rope_ … [891 caractères tronqués]`

  ```
CDC  ==>  reports/rapport-optimisations.md:144:CPU le multiplieur gagne 45× ; **sur FPGA il n'existe pas**. La contrainte du CDC
harnais  ==>  reports/rapport-optimisations.md:57:(le harnais ne validait qu'une seule densité auparavant : c'est précisément la
banc  ==>  reports/rapport-optimisations.md:155:2. **3–5 G év/s sur un CPU de bureau**, soit ~1 événement par cycle. Un banc
porte du dépôt  ==>  reports/rapport-p0-flux.md:51:Et la porte du dépôt ne bouge pas : **Qwen2.5-0.5B ctx 256 = 19,3885**, la même
porte verte  ==>  reports/rapport-routage-experts.md:46:porte verte sur un seul des deux ne disait rien de l'autre.
non-régression  ==>  reports/rapport-prefill-par-lots.md:197:et la porte de non-régression Qwen contexte 256 reste à **19,3885**.
drapeau  ==>  reports/rapport-parcimonie-imposee.md:125:   perplexité. Le premier « gain de débit nul » mesurait donc un drapeau ignoré,
options-strict  ==>  reports/rapport-session-2026-09-30.md:61:`--options-strict` pour les scripts ; le **kit Colab** rendu clé en main
DRAVE_PRELIRE_TOUT  ==>  reports/rapport-optimisations-auto.md:100:des gains** : `DRAVE_PRELIRE=0` et `DRAVE_PRELIRE_TOUT=1` existent, et le jour où
DRAVE_GPU  ==>  rep
… [4790 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Writing the inventory, then sending it to the parent agent

I have all 20 files read and all line numbers verified. Here is the inventory.

---

## A. Termes et sigles

- **AER** (non développé dans le texte ; « réseau de combinaison façon routeur AER ») — réseau d'interconnexion par compartiments de destination servant au dédoublonnage multi-cartes ; utilisé pour la fusion par compartiments (`drave-core`) ; `reports/rapport-optimisations.md:166`
- **ALM** (Adaptive Logic Module) — brique logique du FPGA dont on compte le coût d'un PE ; `reports/rapport-precision.md:70`
- **AVX2** — jeu d'instructions SIMD x86 utilisé pour les noyaux de quantification (gather/scatter entier absents) ; `reports/rapport-optimisations.md:163`
- **CDC** (cahier des charges, non développé) — contrainte « aucun DSP » du projet ; `reports/rapport-optimisations.md:144`
- **CPU** — processeur hôte, opposé au FPGA/GPU dans les comparaisons de débit ; `reports/rapport-optimisations-auto.md:88`
- **CSA** (compresseur DeepSeek-V4, ratio 4) — attention à blocs compressés avec chevauchement, 21 couches de V4-Flash ; `reports/rapport-v4-couches-0-1.md:11`
- **CUDA** — pilote GPU ouvert seulement si `nvidia-smi` en signale le besoin ; `reports/rapport-optimisations-auto.md:16`
- **DDR3** — mémoire du banc FPGA, débit 9,66 Go/s qui fixe la saturation à 312 voies ; `reports/rapport-precision.md:63`
- **DDR4-2133** — mémoire des deux sockets Xeon, ~136 Go/s théoriques ; `reports/rapport-passage-a-l-echelle.md:152`
- **DSP** (Digital Signal Processor) — multiplieur matériel interdit par le cahier des charges ; `reports/rapport-optimisations.md:145`
- **E2M1** — format 4 bits des valeurs MXFP4 (magnitudes {0,½,1,1½,2,3,4,6}) ; `reports/rapport-passage-a-l-echelle.md:78`
- **E8M0** — échelle de bloc MXFP4 sur 1 octet, une puissance de deux ; `reports/rapport-passage-a-l-echelle.md:77`
- **FPGA** — cible matérielle du CDC (« aucun DSP », 124 MHz × 32 PEs, ALM comptés) ; `reports/rapport-optimisations.md:72`
- **GEMM** — produit matrice-matrice (par lots) opposé au produit matrice-vecteur jeton par jeton ; `reports/rapport-prefill-par-lots.md:1`
- **GGUF** — format de fichier des modèles llama.cpp, lu par le moteur (`Gguf::open`, `read_to_end`, métadonnées) ; `reports/rapport-passage-a-l-echelle.md:204`
- **GPU** — carte accélérant KV/tête, miroir VRAM, `DRAVE_GPU`, `DRAVE_GPU_KV`, `DRAVE_GPU_TETE` ; `reports/rapport-optimisations-auto.md:16`
- **GQA** (Grouped-Query Attention) — modèle à têtes KV partagées dont le cache KV dépasse les poids à 128 k ; `reports/rapport-passage-a-l-echelle.md:143`
- **HCA** (compresseur DeepSeek-V4, ratio 128) — résumé de bloc « par dimension » avec porte softmax, 20 couches de V4-Flash ; `reports/rapport-v4-couches-0-1.md:12`
- **JIT** — piste « charger dynamiquement les logits manquants ou faire du JIT », rejetée ; `reports/rapport-tete-restreinte.md:5`
- **KV** (cache clé-valeur) — état d'attention par couche, quantifié (f32/f16/int8/int4), déportable en VRAM ; `reports/rapport-optimisations-auto.md:51`
- **LUT** (table) — implémentation d'un MAC int4×int8 par 4 additions conditionnelles décalées ; `reports/rapport-precision.md:69`
- **MAC** — multiply-accumulate ; coûté en ALM pour int4×int8 vs PE ternaire ; `reports/rapport-precision.md:69`
- **MLA** (Multi-head Latent Attention) — attention à cache latent (rang faible) des modèles DeepSeek/GLM/Kimi ; `reports/rapport-optimisations-auto.md:56`
- **MoE** (Mixture of Experts) — modèle à experts routés, seule parcimonie structurelle qui rend l'événementiel rentable ; `reports/rapport-p0-flux.md:49`
- **MXFP4** — quantification 4 bits par blocs de 32 (E8M0 + nibbles E2M1), format de gpt-oss-120b, import « exact » ; `reports/rapport-passage-a-l-echelle.md:17`
- **NLL** (negative log-likelihood) — perte moyenne par jeton servant à comparer Drave à llama.cpp ; `reports/rapport-routage-experts.md:114`
- **NUMA** — topologie mémoire par nœud (2 nœuds), exploitable par `numactl` et premier-touch ; `reports/rapport-optimisations-auto.md:14`
- **NVLink** — lien GPU annoncé à 25,8 Go/s (« 2× le PCIe ») ; `reports/rapport-optimisations-auto.md:17`
- **NVMe** — disque rapide (FastNVMe) mesuré 5,37 Go/s à 1 lecteur, 31 Go/s à 16 ; `reports/rapport-optimisations-auto.md:19`
- **PCIe** — bus d'extension, 6,5 Go/s en x8 dans les comparaisons de transport ; `reports/rapport-optimisations-auto.md:17`
- **PE** (processing element) — unité de calcul du FPGA (312 voies, PE ternaire ~20 ALM) ; `reports/rapport-precision.md:62`
- **PPL** (perplexity) — métrique de qualité principale des campagnes (`--ppl`) ; `reports/rapport-parcimonie-imposee.md:47`
- **QPI** — lien inter-socket traversé par la moitié des accès quand les poids sont alloués sur un seul socket ; `reports/rapport-passage-a-l-echelle.md:156`
- **QSFP+** — lien réseau 4,8 Go/s cité comme protocole naturel du flux d'événements ; `reports/rapport-passage-a-l-echelle.md:179`
- **RMSNorm** (écrit `rmsnorm`, `norme RMS`) — normalisation d'entrée de couche, envoyée à tort au pair par `--flux-norme` ; `reports/rapport-transport-liste.md:67`
- **RoPE** (Rotary Position Embedding) — rotation positionnelle ; deux conventions opposées (`LLAMA_ROPE_TYPE_NORM` vs `NEOX`) ; `reports/rapport-v4-couches-0-1.md:7`
- **SiLU** (écrit `silu`) — activation du SwiGLU (`silu(gate)·up`) ; `reports/rapport-v4-hca.md:131`
- **SWAR** — décodage « SIMD within a register » de 8 varints dans un mot de 64 bits ; `reports/rapport-optimisations.md:19`
- **SwiGLU** — FFN à porte, dont le clamp (`swiglu_clamp_exp`) manquait ; `reports/rapport-v4-hca.md:125`
- **TCP_NODELAY** — désactivation de Nagle divisant par six l'attente du pair ; `reports/rapport-transport-liste.md:198`
- **TLB** — cache d'adresses ; 15 M de pages de 4 Ko pour 60 Go, pages de 2 Mo divisant le coût par 512 ; `reports/rapport-passage-a-l-echelle.md:160`
- **VRAM** — mémoire GPU ; cache d'experts, miroir KV déporté (1,7–1,8 ms) ; `reports/rapport-optimisations-auto.md:67`
- **YaRN** — extension de contexte RoPE, « à retardement » par défaut (au-delà de 4× la longueur vue) ou forcée par `DRAVE_YARN=1` ; `reports/rapport-routage-experts.md:126`
- **k-WTA** (k-winners-take-all) — inhibition latérale gardant les k plus grandes magnitudes, dix fois meilleur que le seuil ; `reports/rapport-parcimonie-imposee.md:24`
- **A3B** — suffixe Qwen3-30B-A3B : 3,3 G paramètres actifs sur 30 B (MoE top-8) ; `reports/rapport-passage-a-l-echelle.md:15`
- **Q8_0 / Q4_0 / Q4_K / Q4_K_M / Q6_K / Q8_1** — types de quantification GGUF ; Q8_1 est le format d'activation de ggml côté llama.cpp ; `reports/rapport-optimisations.md:4`, `reports/rapport-passage-a-l-echelle.md:13`, `reports/rapport-v4-couches-0-1.md:49`
- **f32 / f16 / int8 / int4** — précisions du cache KV et des flux (f32 dense de transport, clés f16, valeurs int8/int4) ; `reports/rapport-placement-bits-kv.md:4`
- **super-bloc** — unité de déquantification IQ (experts) et bloc de 256 poids pour Q4_K/Q6_K ; `reports/rapport-p0-flux.md:20`
- **paire** (poids × activation effectivement multiplié, ce qui est payé) — `Model::paires: [u64; 3]` par provenance ; `reports/rapport-p0-flux.md:36`
- **paire hyperthread** — couple de threads logiques partageant L1/L2, épinglés si la machine a moins de 8 cœurs ; `reports/rapport-optimisations-auto.md:13`
- **événement** — paire dont le poids est non nul ; coïncide avec la paire sur un chemin en listes ; `reports/rapport-p0-flux.md:31`
- **provenance** — étiquette du compteur de paires : 0 attention, 1 experts routés, 2 partagé ; `reports/rapport-p0-flux.md:36`
- **push / pull** — deux chemins de `matvec` : push = listes d'événements, pull = produit scalaire dense ligne par ligne ; `reports/rapport-p0-flux.md:13`
- **porte** (1 : porte de non-régression du dépôt, ex. Qwen 19,3885) — `reports/rapport-p0-flux.md:51`, `reports/rapport-optimisations-auto.md:134`
- **porte** (2 : porte d'un compresseur V4, `attn_compressor_gate`) — poids de softmax par canal dans HCA/CSA ; `reports/rapport-v4-hca.md:15`
- **porte de correction** — validation partielle d'une étape, opposée à une validation du modèle entier ; `reports/rapport-v4-couches-0-1.md:85`
- **mode 0 / mode 1 / mode 2 / mode 3 / mode 4** — modes du protocole de flux : dense f32, listes, blocs, LOT (lot dense), lot en listes ; `reports/rapport-transport-liste.md:15`, `reports/rapport-prefill-reparti.md:15`, `reports/rapport-prefill-reparti.md:107`
- **protocole v5** — cinq modes + contrat d'activation complet (14 champs), refus immédiat d'un pair incompatible ; `reports/rapport-session-2026-09-30.md:18`
- **en-tête / magie / TAILLE_TETE** — en-tête de flux passé de 39 à 79 octets (magie u32, version, mode, plage, position, dimension, échelle, réglages) ; `reports/rapport-transport-liste.md:10`, `reports/rapport-prefill-reparti.md:17`
- **indices par écarts** — codage des indices de liste par delta d'un octet, 255 = échappement absolu ; `reports/rapport-transport-liste.md:169`
- **échelle par bloc de 32** — quantification i8 + échelle f32 par bloc (`--flux-blocs`), erreur relative bornée ; `reports/rapport-transport-liste.md:100`
- **densité d'activation** — fraction des poids actifs ; seuil de bascule événementiel/dense à 22 % ; `reports/rapport-passage-a-l-echelle.md:39`
- **b/poids** (bits par poids) — unité de coût de stockage (1,98 pour un événement, 0,53 en 4 bits) ; `reports/rapport-optimisations.md:37`
- **G év/s** (milliards d'événements par seconde) — débit du moteur événementiel (3–5 G év/s sur CPU de bureau) ; `reports/rapport-optimisations.md:70`
- **Go/s, Mo, Ko, ms, Mbit/s, GFLOP/s** — débits et volumes mesurés (NVMe 31 Go/s, flux 0,25 Mbit/s, OpenBLAS 759 GFLOP/s) ; `reports/rapport-optimisations-auto.md:46`, `reports/rapport-transport-liste.md:183`, `reports/rapport-programme-evolutif.md:113`
- **perplexité / PPL** — mesure de qualité de référence de toutes les campagnes ; `reports/rapport-optimisations-auto.md:117`
- **tok/s, jetons/s, évaluations/h** — débits de génération et de banc (41,6 ; 5,62 ; ~100/h) ; `reports/rapport-passage-a-l-echelle.md:47`, `reports/rapport-travail-reel.md:22`, `reports/rapport-programme-evolutif.md:84`
- **latence / aller-retour** — poste dominant du calcul réparti (`attente ≈ calcul distant + 3,2 × latence`) ; `reports/rapport-prefill-reparti.md:12`
- **Nagle / ACK différé** — cause de 97,6 ms/jeton d'attente, corrigée par `set_nodelay(true)` ; `reports/rapport-transport-liste.md:196`
- **mmap / madvise(WILLNEED) / MADV / posix_fadvise(DONTNEED) / readahead / page cache** — mécanismes de prélecture et de forçage du froid, tous sans gain ; `reports/rapport-optimisations-auto.md:79`, `reports/rapport-tete-garantie.md:94`
- **premier-touch (first-touch)** — politique d'allocation NUMA à corriger (paralléliser l'allocation) ; `reports/rapport-passage-a-l-echelle.md:155`
- **mmap paresseux** — chargement atteignant 2,7 Go/s, proche du débit séquentiel du NVMe ; `reports/rapport-optimisations-auto.md:89`
- **SWAR/varint/décalages** — encodage et décodage du disque et du moteur ; `reports/rapport-optimisations.md:19`
- **bitmap** — encodage dense 1 bit/poids + signe (1,09 Mo, 1,99 b/poids) imposant un débit constant ; `reports/rapport-optimisations.md:38`
- **SparseVec** — vecteur d'activation creux explicite (indices triés + valeurs contiguës, 8 octets par source active) ; `reports/rapport-optimisations.md:26`
- **FusedSign** — liste unique triée par destination + plan de signe, accès accumulateur monotone ; `reports/rapport-optimisations.md:32`
- **PushMat / DenseQ8 / DenseQ4** — trois représentations de poids du moteur (listes, int8 dense, 4 bits) ; `reports/rapport-passage-a-l-echelle.md:39`
- **events_total() / row_ev[i] / touched / row_delta_into** — compteur d'événements et mécanique de réduction incrémentale ; `reports/rapport-p0-flux.md:13`, `reports/rapport-optimisations.md:93`
- **matvec / matvec_f32 / matvec4_ou_iq / attn_mla / logits / logits_lot / logits_garanti** — points de comptage et noyaux du moteur ; `reports/rapport-p0-flux.md:19`
- **forward / forward_lot / forward_mla** — passes avant jeton, par lots, MLA ; `reports/rapport-phase3-reparti.md:33`
- **Model::load / load_partiel / verifier_architecture / router / emb_imposee / emb_imposee_lot / flux_brut / couche_debut..couche_fin** — API interne citée comme lieu des correctifs ; `reports/rapport-passage-a-l-echelle.md:116`, `reports/rapport-routage-experts.md:43`, `reports/rapport-prefill-reparti.md:30`, `reports/rapport-phase3-reparti.md:28`
- **Pool::gemm_dense_i8 / gemm_dense_q4 / Pool::attendre / Shared::gs32 / Shared::morts / catch_unwind / AtomicPtr** — machinerie du pool de threads et du lot ; `reports/rapport-prefill-par-lots.md:12`, `reports/rapport-prefill-par-lots.md:170`
- **q4_blocks() / q8_view() / gguf::q8_dot_at** — lecture en place sans copie et noyau de la tête lié au calcul ; `reports/rapport-passage-a-l-echelle.md:121`, `reports/rapport-prefill-par-lots.md:133`
- **tuilage** — traitement par groupe de 16 jetons (8 en 4 bits) pour garder les activations en cache ; `reports/rapport-prefill-par-lots.md:63`
- **engram** — sonde d'accès disque par entrée de 264 octets ; `reports/rapport-optimisations-auto.md:103`
- **aiguille / Aiguille v2 / sonde** — test de récupération d'une information enfouie (`tools/aiguille.py`), 9/9 sondes trouvées ; `reports/rapport-placement-bits-kv.md:144`
- **hyper-connexion** — mélanges appris de copies de l'état (hc_attn_pre, hc_post, 24 mélanges, Sinkhorn 20 itérations) ; `reports/rapport-p0-flux.md:120`
- **Sinkhorn** — normalisation itérative (20 itérations) dans les hyper-connexions V4 ; `reports/rapport-v4-couches-0-1.md:55`
- **puits (attention sink)** — `attn_sinks` / `ggml_soft_max_add_sinks`, ajouté brut après l'échelle des scores ; `reports/rapport-v4-couches-0-1.md:7`
- **ape** — ligne apprise par rang dans le bloc (`pos % ratio`), forme `[512, 128]`, ajoutée à la porte HCA ; `reports/rapport-v4-hca.md:17`
- **indexeur / lightning indexer** — `ggml_lightning_indexer` : `relu(q·k)` pondéré par tête puis top-k des blocs ; `reports/rapport-v4-hca.md:96`
- **nope / dé-rotation (derope) / rope_norm** — parties non tournée et tournée de la tête, et l'inverse de RoPE ; `reports/rapport-v4-hca.md:52`, `reports/rapport-v4-couches-0-1.md:40`
- **fenêtre glissante / sliding_window / build_raw_tail** — fenêtre brute 128 de V4 et « queue » d'attention brute ; `reports/rapport-v4-couches-0-1.md:81`
- **compress_ratios / compress_rope_freq_base / n_visible** — métadonnées de compression V4 (21 CSA ratio 4, 20 HCA ratio 128, 3 brutes ; base RoPE compressée 160 000) ; `reports/rapport-v4-couches-0-1.md:11`, `reports/rapport-v4-hca.md:24`
- **routeur / top-k / renormalisation / expert partagé / scoring_func / expert_gating_func** — conventions de routage MoE corrigées (softmax, sigmoïde, softmax des poids, racine de softplus) ; `reports/rapport-routage-experts.md:14`
- **routed_scaling_factor (expert_weights_scale)** — facteur d'échelle post-renormalisation (1,5 ; 2,5 ; 2,827) ; `reports/rapport-routage-experts.md:26`
- **hash_layer_count / ffn_gate_tid2eid.weight** — routage par table des 3 premières couches de V4-Flash (tenseur I32 `[129 280 × 6]`) ; `reports/rapport-routage-experts.md:30`
- **architectures `qwen3moe`, `gpt-oss`, `deepseek2`, `glm-dsa`, `glm5next`, `deepseek4`, `deepseek41`** — identifiants d'arch déclarés par les GGUF et leur fonction de routage ; `reports/rapport-routage-experts.md:16`
- **grappe** — groupe d'activations corrélées (k-moyennes) ; usage « localité » retenu, usage « difficulté » rejeté ; `reports/rapport-programme-evolutif.md:5`
- **η² / R² / r** — statistiques des grappes (6,2 % ; +0,007 ; r = +0,573) ; `reports/rapport-programme-evolutif.md:36`
- **trace hebbienne / `--hebbian`** — journal de co-activation pour l'apprentissage de nouveaux nœuds ; `reports/rapport-programme-evolutif.md:67`
- **monômes quadratiques** — 401 856 produits `x_i·x_j` hors du span linéaire, espace « réellement neuf » ; `reports/rapport-programme-evolutif.md:72`
- **prune → retrain (masque fixe) → quantize → refit d'échelle** — protocole du banc de précision ; `reports/rapport-precision.md:5`
- **frontière de Pareto** — accuracy maximale à coût b/poids donné ; `reports/rapport-precision.md:43`
- **unaire (répétition d'adresse)** — encodage d'une valeur en répétant l'adresse v fois ; `reports/rapport-valeur-unaire.md:28`
- **plans binaires / popcount** — encodage par plans de bits et comptage de bits ; `reports/rapport-valeur-unaire.md:29`
- **inégalité de Kraft / entropie (b/poids)** — borne de décodabilité et plancher d'entropie (3,731 b/poids) ; `reports/rapport-valeur-unaire.md:51`
- **BitNet b1.58 / ternaire / listes signées** — cas où l'adresse seule porte la valeur (0,39 b/poids) ; `reports/rapport-valeur-unaire.md:86`
- **Heaps (exposant de)** — loi de croissance du vocabulaire observé (≈ 0,21) ; `reports/rapport-tete-restreinte.md:21`
- **jargon de banc** : harnais, banc, rejeu, trace, drapeau ignoré, porte verte, `--options-actives`, `--options-strict` ; `reports/rapport-optimisations.md:57`, `reports/rapport-session-2026-09-30.md:21`
- **Colab / notebook / tunnel** — kit de démonstration distante (`colab/README.md`, `tools/colab_cote_local.sh`) ; `reports/rapport-session-2026-09-30.md:20`
- **pilote / pair / nœud moteur / flux** — rôles du calcul réparti (le pilote garde les couches 0..12, le pair applique 12..24) ; `reports/rapport-phase3-reparti.md:9`
- **plafond cumulatif R4** — garde-fou mémoire réseau (refus à l'état 72 393, 256 Mo) ; `reports/rapport-session-2026-09-30.md:76`
- **P1–P6, P4, P5** — jalons du plan V4 (P4 = HCA, P5 = CSA + indexeur) ; `reports/rapport-p0-flux.md:72`, `reports/rapport-v4-couches-0-1.md:79`
- **SpikeGPT / R̂ = 0,15** — référence externe de taux d'activation d'un modèle entraîné à décharger (facteur 6,7×) ; `reports/rapport-parcimonie-imposee.md:116`
- **OpenBLAS / moindres carrés / autogradage / rétropropagation** — capacités présentes et manquantes de la pile (759 GFLOP/s, pas d'optimiseur) ; `reports/rapport-programme-evolutif.md:112`
- **plomberie** — le seul manque restant du programme évolutif (charger un modèle patché) ; `reports/rapport-programme-evolutif.md:128`
- **Termes attendus mais ABSENTS de ces 20 fichiers** : DRVF/DRVF v5, PTX, RSS, IQ2_XXS, HBM, M20K, greffon, liste valuée, shard, p50/p95, MTok/s, Gbit/s, bf16, Hadamard, LoRA, MTP, MMLU/MNIST.

## B. Chiffres et affirmations mesurées

**rapport-optimisations-auto.md**
- `:29` — « | 20 cœurs | **22,5** | »
- `:30` — « | 20 cœurs + hyperthreads (40 fils) | 18,9 | »
- `:31` — « | 10 cœurs | 14,7 | »
- `:32` — « | **10 cœurs + leurs hyperthreads** | **18,7** (+27 %) | »
- `:33` — « | 10 cœurs, 3 fils par cœur | 15,0 — régression | »
- `:17` — « | **NVLink** | `nvidia-smi nvlink -s` | 25,8 Go/s, 2× le PCIe | »
- `:38` — « défaut : `threads = cœurs physiques` — le moteur prenait `cpu × 3/4` = **30** fils sur 40 threads logiques, il en prend **20** »
- `:46` — « | Go/s | 5,37 | 9,68 | 18,08 | 28,29 | **31,08** | » (1/2/4/8/16 lecteurs)
- `:48` — « Vérifié sur 50,5 Go (parcours complet du disque) : 3,42 / 21,02 / 33,19. »
- `:49` — « **Le NVMe parallélisé dépasse la RAM** (31 contre 22 Go/s). »
- `:53` — « Le seuil est **un tiers de la RAM libre** »
- `:56` — « le KV de MLA de V4.1 pèse **90 Ko par jeton en F16**, soit 96,6 Go à 1 M — plus que les 71 Go d'experts. En int8, 48,3 Go. »
- `:62` — « ctx 4096 : [config] cache KV : 32 bits, 0.20 Go pour 4096 jetons »
- `:63` — « ctx 262144 : [config] cache KV en int8 : 51.5 Go en f32 pour 262144 jetons, soit plus du tiers de la RAM libre (116 Go) »
- `:69` — « `VRAM libre − 2 Go de réserve CUDA − le commun` »
- `:70` — « La VRAM lit à 84,9 Go/s contre 22,5 pour la RAM. »
- `:79` — « `madvise(WILLNEED)` après le routage (experts) | 25,73 s contre 25,80 | 0,3 % »
- `:80` — « `madvise` sur tout le fichier au chargement | 7,29 s contre 7,47 | −2 % »
- `:82` — « chargement : mmap contre lecture | **6,8 s contre 30,5 s** | le mmap est 4,5× mieux »
- `:84` — « le modèle de test (18,6 Go) tient dans les 115 Go de cache RAM »
- `:88` — « 7,10 s à 4 fils contre 6,80 s à 20 fils »
- `:89` — « Le mmap paresseux atteint déjà 2,7 Go/s, proche du débit séquentiel du NVMe (2,1 à 5,5 Go/s mesurés) »
- `:95` — « V4.1 (365 Go pour 115 Go de RAM) »
- `:104` — « la sonde d'engram sur le disque **mécanique** mesure 16 ms par entrée de 264 octets »
- `:110` — « **25,73 s avec, 25,80 sans, soit 0,3 %** »
- `:117` — « densité 5,1 % ⇒ perplexité ×107 »
- `:122` — « **`--tete-restreinte`** : +10,5 % (liste française) à +15 % (anglaise) »
- `:129` — « `TETE_ACTIFS / TETE_TOTAL / TETE_APPELS` : trois `fetch_add` par appel de tête »
- `:134` — « 35 tests verts (3 nouveaux sur la détection), portes **Qwen 19,3885** et **clusters 799,8557** inchangées »

**rapport-optimisations.md**
- `:4` — « Matrice réelle `blk.0.ffn_gate.weight` de Qwen2.5-0.5B-Q8_0 : 4864 entrées × 896 sorties, **4 303 745 événements** (ternaire issu des signes réels, densité 100 %) »
- `:6` — « Machine : 2 × Xeon E5-2687W v3 (20 cœurs / 40 CPU logiques), NUMA 2 nœuds. »
- `:16` — « **0,484 ms → 0,011 ms** (×44) »
- `:21` — « Les écarts d'un octet (99,99 % des événements à forte densité) sont décodés **8 à la fois dans un mot de 64 bits** »
- `:28` — « 8 octets par source active »
- `:37` — « Coût : 4,89 Mo (8,97 b/poids) contre 4,34 Mo (7,98 b/poids) pour les deux listes séparées. Le bitmap+signe reste à 1,09 Mo (1,99 b/poids) »
- `:47` — « | 0 % | 0 | 0,011 ms | 0,011 ms | »
- `:48` — « | 1 % | 43 560 | 0,14 G év/s | 0,42 G év/s | »
- `:49` — « | 5 % | 216 960 | 1,15 G év/s | 1,50 G év/s | »
- `:50` — « | 10 % | 430 359 | 1,81 G év/s | 2,30 G év/s | »
- `:51` — « | 25 % | 1 076 785 | 3,18 G év/s | 3,86 G év/s | »
- `:52` — « | 50 % | 2 152 648 | 4,14 G év/s | 4,89 G év/s | »
- `:53` — « | 100 % | 4 303 745 | **4,51 G év/s** (0,95 ms) | **5,44 G év/s** (0,79 ms) | »
- `:55` — « **Exactitude : 14 vérifications sur 14** »
- `:60` — « Le débit varie de **0,011 ms à 0,95 ms sur la même matrice** (rapport 86) »
- `:67` — « | Fusion (G év/s) | 0,41 | 0,75 | 1,45 | 2,75 | 4,45 | 4,35 | **4,84** | 2,04 ❌ | »
- `:68` — « | 2 listes (G év/s) | 0,42 | 0,78 | 1,49 | 2,83 | 4,37 | 5,24 | **5,78** | 2,59 ❌ | »
- `:70` — « **~0,15–0,18 G év/s par thread**, optimum vers 28–32 threads, soit ~0,8–1,3 événement par cycle CPU »
- `:71` — « Une carte à 124 MHz × 32 PEs = 4 G év/s vise donc **exactement un CPU 16–32 cœurs** »
- `:75` — « Mesures prises avec le bureau actif (load ~1,5–5) : ±20 % d'une passe à l'autre »
- `:77` — « Le moteur refuse désormais de dépasser `CPU − 1` et prend `3/4 × CPU` par défaut. »
- `:86` — « La première campagne annonçait « fusion DIVERGENTE au rang 0 : 3838 vs 3513 » et un chemin 2-listes à 7,53 G év/s. **Les deux chiffres étaient faux.** »
- `:105` — « chuter le débit de 3,09 à 0,97 G év/s (8 threads) »
- `:115` — « À **39 workers + le thread appelant sur 40 CPU logiques**, le débit s'effondre : **4,84 → 2,04 G év/s** »
- `:121` — « `yield_now()` après N tours — **a tout empiré** (0,97 G à 8 threads) »
- `:124` — « le pool est borné à `CPU − 1` et la valeur par défaut est `3/4 × CPU` »
- `:138` — « | multiplication i8×i8 | 2,5 ms | 4,36 M | »
- `:139` — « | **décalages + additions** | **112,3 ms** | 13,58 M (3,12 additions/poids) | »
- `:140` — « | rapport | **×44,9** | — | »
- `:141` — « | résultat | **identique** ✅ | — | »
- `:143` — « Les niveaux Q8_0 réels ont en moyenne 3,12 bits à 1 ⇒ ~3 additions par poids »
- `:156` — « **3–5 G év/s sur un CPU de bureau**, soit ~1 événement par cycle »

**rapport-p0-flux.md**
- `:9` — « **sur ces deux chemins, le flux est dense** — 0 événement en listes, la totalité des matrices est payée »
- `:36` — « `Model::paires: [u64; 3]` — 0 = attention, 1 = experts routés, 2 = partagé »
- `:47` — « | Qwen2.5-0.5B Q8_0 | attention | **44,2 M** | 24 couches × (896×896 + 896×128 + 896×128 + 896×896) = **44,04 M** ✅ | »
- `:48` — « | Qwen2.5-0.5B Q8_0 | partagé | **451,2 M** | 24 × 3×896×4864 = 313,7 M (FFN) + 896×151 936 = 136,1 M (tête) = 449,8 M ✅ (l'écart de 0,3 % est le jeton de tête non noté) | »
- `:49` — « | Qwen2.5-0.5B Q8_0 | experts | 0 | pas de MoE ✅ | »
- `:51` — « **Qwen2.5-0.5B ctx 256 = 19,3885** »
- `:55` — « Sur **GLM-5.3** (79 couches, MLA, 256 experts top-8, 216,7 Go) »
- `:60` — « | attention (MLA) | **21,9 G** | 37,7 % | »
- `:61` — « | experts routés | **30,6 G** | 52,6 % | »
- `:62` — « | partagé | **5,6 G** | 9,7 % | »
- `:63` — « | **total** | **58,2 G** | 100 % | »
- `:64` — « | dont en **listes** | **0** | **0 %** | »
- `:73` — « 8 experts sur 256, soit 3 % du modèle »
- `:78` — « **L'attention MLA coûte 21,9 G paires pour 4 positions de contexte** »
- `:91` — « `attn_k_b [64, 512, 192]`, `attn_v_b [64, 256, 512]`, `nh = 64`, 79 couches »
- `:92` — « le travail retiré vaut `vd × kvl` par (tête, position), soit **662,7 M paires** par passe avant, et **1 988,1 M** pour la passe complète d'un jeton noté »
- `:98` — « | perplexité | 14533,9920 | **14533,9920** — identique | »
- `:99` — « | paires d'attention / token | **29 224,8 M** | **27 236,7 M** | »
- `:100` — « | écart | — | **−1 988,1 M**, exactement la prédiction | »
- `:101` — « | total / token | 83 104,0 M | 81 115,9 M | »
- `:108` — « la seconde passe était **chaude** (41,8 s contre 215,7 s pour la première, page cache) »
- `:111` — « « attention 14 024 ms → 12 256 ms » serait malhonnête »
- `:118` — « gpt-oss répondait « calculable : NON » alors que sa porte (15,6017) tourne »
- `:119` — « ont servi à la validation MLA (corrélation 0,999024) »
- `:124` — « **jeton froid** (216,7 Go lus depuis le disque mécanique, 190 s de chargement, 147 s/jeton) »

**rapport-parcimonie-imposee.md**
- `:5` — « deux jeux de 1 024 tokens : **A** pour le réglage, **B** (jamais vu) »
- `:10` — « la machine tournait sous une charge de 8 à 14 »
- `:17` — « **0,00 % d'activations nulles** »
- `:28` — « Jeu de 512 tokens, référence 19,2647 pour 352,8 M événements »
- `:32` — « | 0,1 % | 343,8 M (−2,6 %) | 19,5750 | 1,02× | »
- `:34` — « | 0,5 % | 312,3 M (−11,5 %) | 20,1511 | 1,05× | »
- `:36` — « | 2,0 % | 230,8 M (−34,6 %) | 30,5837 | 1,59× | »
- `:37` — « | 5,0 % | 145,0 M (−58,9 %) | **2264,84** | **117×** | »
- `:39` — « Économiser 11 % d'événements coûte 5 % de perplexité, et au-delà de 2 % le modèle s'effondre »
- `:49` — « | 100 % | 354,3 M | 23,6125 | 26,2565 | »
- `:50` — « | 90 % | 319,1 M (−9,9 %) | 23,6790 (+0,28 %) | 26,2950 (+0,15 %) | »
- `:51` — « | 85 % | 301,5 M (−14,9 %) | 23,7468 (+0,57 %) | 26,5785 (+1,23 %) | »
- `:52` — « | 80 % | 283,7 M (−19,9 %) | 23,8251 (+0,90 %) | 26,8586 (+2,29 %) | »
- `:54` — « **À sparsité comparable, le k-WTA coûte dix fois moins que le seuil** »
- `:71` — « | **FFN complet à 85 %** | **308,0 M (−13,1 %)** | **−0,18 %** | **+0,46 %** | »
- `:72` — « | FFN complet à 80 % | 292,4 M (−17,5 %) | — | +1,57 % | »
- `:84` — « Résultat : **dégrade** (+0,2 % à 90 %, +1,2 % à 85 %, +3,6 % à 80 %) »
- `:96` — « | première campagne | modérée | **−12,7 %** de CPU | »
- `:97` — « | seconde campagne | load 8-14 | **−3,0 %** de CPU | »
- `:101` — « un `select_nth` par produit matriciel, 168 par token »
- `:104` — « **Fourchette honnête : entre 3 et 13 % de temps CPU pour 13-15 % d'événements économisés.** »
- `:110` — « ~13 % d'événements pour ~0,5 % de perplexité »
- `:116` — « **Ce n'est pas le facteur 6,7×** qu'obtiendrait un modèle réellement entraîné à décharger (R̂ = 0,15 chez SpikeGPT) »
- `:122` — « Symptôme : 3,8 M événements au lieu de 349 M »

**rapport-passage-a-l-echelle.md**
- `:11` — « | Qwen2.5-0.5B Q8_0 | 0,53 Go | Q8_0 | ✅ | »
- `:13` — « | Qwen2.5-VL-7B Q4_K_M | 4,5 Go | **Q4_K** 6,09 G + **Q6_K** 1,52 G | ❌ | »
- `:17` — « | **gpt-oss-120b MXFP4** (MoE) | 60,5 Go | **MXFP4** 114,66 G + Q8_0 2,11 G | ❌ | »
- `:19` — « Le moteur ne lit que `F32`, `F16`, `Q8_0` et `Q4_0`. **Aucun modèle récent ne s'ouvre aujourd'hui** »
- `:32` — « t = octets_actifs_par_jeton / bande_passante »
- `:39` — « | listes d'événements (`PushMat`) | **1,98** | densité d'activation < 22 % | »
- `:40` — « | int8 dense (`DenseQ8`) | 1,00 | densité > 22 % | »
- `:41` — « | **4 bits** (`DenseQ4`) | **0,53** | grosses matrices, au-delà du cache | »
- `:43` — « Bande passante atteinte sur cette machine : **20–25 Go/s** (théorique ≈ 68 Go/s par socket, 136 pour les deux) »
- `:46` — « 0,49 G poids × 0,53 o = 0,26 Go par jeton ÷ 20 Go/s = **13 ms/jeton = 41 tok/s**, contre **41,6 tok/s mesurés** »
- `:56` — « | Qwen2.5-0.5B (dense) | 0,49 G | 0,26 Go | 13 ms | **41,6** (mesuré) | »
- `:57` — « | Qwen2.5-VL-7B (dense) | 7 G | 3,7 Go | 185 ms | 5,4 | »
- `:59` — « | Qwen2.5-Coder-32B (dense) | 32 G | 17 Go | 850 ms | 1,2 | »
- `:60` — « | **Qwen3-30B-A3B** (MoE) | 3,3 G | 1,7 Go | 87 ms | **11,5** | »
- `:61` — « | **gpt-oss-120b** (MoE) | 5,1 G | 2,7 Go | 135 ms | **7,4** | »
- `:63` — « **Sans MoE, cette machine plafonne vers 7 B en usage interactif et 32 B en traitement de nuit.** »
- `:70` — « Le croisement mesuré à 22 % de densité »
- `:84` — « **Q4_K / Q6_K** : super-blocs de 256 poids, échelles et minima sur 6 bits »
- `:91` — « Bloc de 17 octets (exposant E8M0 + 16 octets de nibbles E2M1) »
- `:94` — « contrairement au passage par les f32 qui coûtait 12 % de perplexité sur Q4_0 »
- `:101` — « tenseur témoin : blk.0.ffn_down_exps.weight dims = (2880, 2880, 128) type 39 »
- `:102` — « exposants : min 119 max 121 médian 120 → 2^-8 … 2^-6 »
- `:103` — « |v|max / (6·2^(e−127)) : médian 1.000, min 0.667 »
- `:106` — « Un ratio médian de **1,000** signifie que le plus grand poids de chaque bloc atteint exactement la magnitude maximale du format »
- `:111` — « **128 experts empilés dans un tenseur 3D**. Nos `Proj` sont 2D. »
- `:120` — « Pour gpt-oss-120b : 60 Go de fichier + 61 Go de copie 4 bits = 121 Go sur 125. Ça ne passe pas. »
- `:145` — « l'attention mesurée croît exactement linéairement avec le contexte (0,88 / 1,91 / 3,20 ms à 64 / 128 / 256) »
- `:152` — « Nous atteignons 20–25 Go/s là où deux sockets DDR4-2133 en offrent ~136 »
- `:160` — « Des pages de 2 Mo diviseraient ce coût par 512 »
- `:165` — « Test NUMA préliminaire (8 threads, `numactl`) : repère 20,7 → **24,7 Go/s** en liant tout à un socket »
- `:175` — « un événement coûte 1,98 o, soit 3,7× un poids 4 bits ... ~1,5 o/événement »
- `:178` — « l'accumulateur décide du débit en régime creux (mesuré : ×1,7 entre 4 et 32 threads sur des événements épars) »
- `:179` — « QSFP+ 4,8 Go/s, NVLink 25,78 Go/s, PCIe x8 6,5 Go/s »

**rapport-phase3-reparti.md**
- `:9` — « Deux processus, localhost, modèle Qwen2.5-0.5B-Q8_0, 12 couches chacun, contexte 256 »
- `:20` — « la locale vaut 144,8289 »
- `:28` — « **1 621,7 → 693,4** — mais pas assez : le facteur restait 4,8 contre la référence »
- `:44` — « | avant correction | 144,8289 | 1 621,7239 | ×11,2 | »
- `:45` — « | après la norme seule | 144,8289 | 693,4492 | ×4,8 | »
- `:46` — « | après la plage de couches | 144,8289 | **144,8289** | **0,00e0** | »
- `:50` — « Vérifié à 40, 200 et **1 024 jetons** (1 023 flux servis ... perplexité **9,5146 des deux côtés**, écart 0,00e0) »
- `:53` — « 19,4 ms par jeton en local, 19,7 ms à attendre le pair »
- `:62` — « le flux voyage en **f32 dense, 3 663 octets par flux** (79 d'en-tête + 896 × 4) »
- `:64` — « alors que le disque sait déjà écrire la même information en **6 octets par neurone actif** »

**rapport-placement-bits-kv.md**
- `:4` — « mettre les bits sur les **clés** plutôt que sur les valeurs change l'erreur d'un facteur **130 à 840** »
- `:5` — « les clés en f16 donnent 39 % de la taille f32 pour **+0,018 %** »
- `:9` — « Qwen2.5-0.5B-Q8_0, 8 191 jetons notés, contexte 8 192 »
- `:15` — « | f32 | f32 | 8 | 100 % | **14,2339** | référence | »
- `:16` — « | **f32** | **int8** | 5,125 | 64 % | **14,2372** | **+0,023 %** | »
- `:17` — « | **int8** | **f32** | 5,125 | 64 % | 14,6622 | **+3,01 %** | »
- `:18` — « | f32 | int4 | 4,625 | 58 % | 14,2994 | +0,46 % | »
- `:19` — « | int4 | f32 | 4,625 | 58 % | 69,0464 | **+385 %** | »
- `:20` — « | int8 | int8 | 2,25 | 28 % | 14,6667 | +3,04 % | »
- `:21` — « | **f16** | **int8** | **3,125** | **39 %** | **14,2365** | **+0,018 %** | »
- `:22` — « | int4 | int4 | 1,25 | 16 % | 66,0369 | **+364 %** | »
- `:23` — « | f16 | int4 | 2,625 | 33 % | 14,3209 | +0,61 % | »
- `:30` — « 16 % int4/int4 ................ +364 % »
- `:33` — « 39 % clés f16 · valeurs int8 .. +0,018 % ← le meilleur point »
- `:39` — « Le point utile est à **39 %** : on divise la taille du cache par 2,5 pour deux centièmes de pour cent »
- `:47` — « À taille égale (5,125 octets), clés f32 + valeurs int8 coûte **+0,023 %** et clés int8 + valeurs f32 coûte **+3,01 %** — un facteur 130 »
- `:49` — « à 4,625 octets, clés f32 + valeurs int4 coûte +0,46 %, clés int4 + valeurs f32 coûte **+385 %** (perplexité 69 au lieu de 14,2). Même taille, même modèle, facteur **840** »
- `:52` — « le 4 bits des DEUX côtés (1,25 octet, 16 % du f32) coûte **+364 %** »
- `:58` — « Les clés en f16 sont le meilleur réglage mesuré : 3,125 octets par élément (39 % du f32) pour **+0,018 %** »
- `:61` — « l'écart entre eux n'est PAS significatif (8 191 jetons) »
- `:64` — « `DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1` donne un cache à **39 % de la taille f32** pour +0,018 %, là où l'int8 complet (28 %) coûte +3,04 % »
- `:67` — « son cache q8_0 coûte +0,8 % à la même longueur »
- `:78` — « Mesuré à 8 192 jetons : **+0,018 %** pour 3,125 octets par élément (**39 %** du f32), et à 4 096 : +0,011 % »
- `:87` — « | f32 · f32 (référence) | **12,2175** | — | 14,2339 | — | »
- `:88` — « | clés f16 · valeurs int8 | **12,2188** | **+0,011 %** | 14,2365 | +0,018 % | »
- `:89` — « | int8 · int8 | 12,4921 | **+2,25 %** | 14,6667 | +3,04 % | »
- `:90` — « | clés f32 · valeurs int8 | 12,2223 | +0,039 % | 14,2372 | +0,023 % | »
- `:113` — « Banc `--banc-kv`, 262 144 clés, 24 couches, 16 fils »
- `:117` — « | f32 | **70,5** | ✅ déporté (1,8 ms) | +3,2e-5 | »
- `:118` — « | **f16** | **162,1** (2,3×) | ❌ désactivé | »
- `:119` — « | int8 | 174,0 | ✅ déporté (1,7 ms) | +3,4e-5 | »
- `:123` — « **les clés f16 coûtent 2,3× le temps CPU des clés f32** (162 contre 70 ms par passe à 262 144 clés) »
- `:137` — « il divise le temps de l'attention par 40 (43 ms contre 1,7 s par jeton à 262 k clés) »
- `:148` — « Qwen2.5-1.5B-Instruct Q4_K_M, contexte 2 048, trois profondeurs (0,1 / 0,5 / 0,9) »
- `:152` — « | f32 (référence) | **3/3** | »
- `:153` — « | clés f16 + valeurs int8 | **3/3** | »
- `:154` — « | int8 · int8 | **3/3** | »
- `:157` — « l'int8 complet coûte +2,25 % de perplexité à ce contexte, et retrouve pourtant ses trois aiguilles »
- `:177` — « Chaque exécution prend 25 à 28 minutes à contexte 8 192 (trois passes de 8 191 jetons, dont une en f32 de référence) »

**rapport-precision.md**
- `:3` — « Modèle minimal (MLP 32→64→10, 2688 poids), référence float **76.07 %** »
- `:12` — « bitmap (1 bit/poids) + k bits par non-nul = 1 + k·d bits/poids »
- `:22` — « | creux 1 bits d=0.125 | 1 | 8.4 % | 1.08 | 60.06 % | 10.2 **◀** | »
- `:26` — « | creux 3 bits d=0.125 | 3 | 12.3 % | 1.37 | 67.29 % | 8.1 **◀** | »
- `:30` — « | creux 2 bits d=0.500 | 2 | 49.3 % | 1.99 | 72.17 % | 5.6 **◀** | »
- `:34` — « | dense 2 bits | 2 | 100.0 % | 2.00 | 73.44 % | 5.5 **◀** | »
- `:36` — « | creux 4 bits d=0.500 | 4 | 50.0 % | 3.00 | 76.07 % | 3.7 **◀** | »
- `:41` — « | dense 8 bits | 8 | 100.0 % | 8.00 | 76.37 % | 1.4 **◀** | »
- `:47` — « | 1.08 | creux 1 bits d=0.125 | 60.06 % | 10.2 | » (frontière de Pareto)
- `:58` — « | 8.00 | dense 8 bits | 76.37 % | 1.4 | »
- `:63` — « Le débit est fixé par la DDR3 (9,66 Go/s) ; 312 voies suffisent à la saturer »
- `:69` — « un MAC int4×int8 en LUT ... coûte ~30-35 ALM contre ~20 pour le PE ternaire »
- `:71` — « Pour 312 voies : ~11 000 ALM, soit **6 % du FPGA** au lieu de 4 % »
- `:76` — « c'est la **forme de la frontière** qui est transposable »

**rapport-prefill-par-lots.md**
- `:4` — « `docs/contexte-long.md` : 4,5 h à 32 k, 1 234 h à 1 M en séquentiel »
- `:24` — « perplexité mesurée **1 614 183** »
- `:26` — « l'entrée de la projection de sortie était dimensionnée sur `hidden` (2 880) au lieu de `n_têtes × dim_tête` (4 096) »
- `:31` — « le biais de `ffn_down_exps` était découpé par la largeur d'expert (`n_ff`) au lieu de la largeur de sortie (`h`) »
- `:33` — « sur Qwen3-MoE (768 contre 2 048) le biais aurait été lu au mauvais endroit »
- `:34` — « **Effet mesuré : nul** sur Qwen3-30B-A3B (7,6139 avant comme après) »
- `:40` — « | Qwen2.5-0.5B (dense) | 13,1368 | **13,1359** | »
- `:41` — « | gpt-oss-120b (MoE, regroupé) | 13,7149 | **13,7205** | »
- `:43` — « L'écart (6e-5 à 4e-4) est l'**ordre des accumulations flottantes** »
- `:52` — « | 1 | **16,6 s** | »
- `:53` — « | 4 | 23,2 s | »
- `:54` — « | 16 | 20,0 s | »
- `:55` — « | 64 | 18,1 s | »
- `:57` — « Le lot était donc **plus lent** que le jeton par jeton, alors que le noyau est 2,4× plus rapide isolément »
- `:60` — « 64 × 896 × 4 = 229 Ko — 4 864 relectures par projection »
- `:63` — « un groupe de 16 jetons (8 pour le 4 bits) est traité avant de passer à la ligne suivante »
- `:75` — « | projections d'attention | 3,05 ms | **1,49 ms** | le GEMM divise par 2 ✓ | »
- `:76` — « | attention | 4,05 ms | 8,90 ms | **×2,2** ✗ | »
- `:77` — « | FFN + projection de sortie | 25,31 ms | 20,92 ms | ÷1,2 seulement | »
- `:78` — « | **somme** | 33,14 ms | 31,31 ms | −5 % | »
- `:79` — « | tête + échantillonnage | 8,36 ms | 8,75 ms | inchangé | »
- `:80` — « | **total** | 41,5 ms | **40,1 ms** | **−3 %** | »
- `:88` — « le chemin *groupé* qui relit les clés une fois par groupe de têtes KV (`rep` = 7 sur Qwen) »
- `:89` — « **la tête de sortie reste calculée jeton par jeton** (145 Mo lus par jeton pour Qwen 0.5B) »
- `:96` — « sortie de 151 936 lignes, trente fois plus de travail que les projections d'attention »
- `:115` — « | projections d'attention (q, k, v) | 2,58 | **0,99** | ÷2,6 ✓ | »
- `:117` — « | attention | 2,78 | 5,59 | **×1,7** ✗ reste le point noir | »
- `:118` — « | projection de sortie + FFN | 20,75 | **14,54** | ÷1,43 | »
- `:119` — « | **somme** | 26,57 | **21,13** | ÷1,26 | »
- `:120` — « | tête de sortie seule | ~5,63 | **5,47** | ≈ inchangé | »
- `:122` — « | **total** | 34,5 | **28,2** | **−18 %** | »
- `:124` — « Bout en bout, sans profil ... : **17,1 s → 13,6 s, soit −20 %**, à perplexité identique (13,1368 → 13,1359) »
- `:126` — « Sur gpt-oss ... lot 1 ≈ 50 s, lots 64/128/256 = **33,7 / 33,9 / 34,4 s**, perplexité 13,7205 dans tous les cas »
- `:131` — « **La tête en lot ne gagne rien** (5,47 contre ~5,63 ms/jeton) »
- `:137` — « le déport GPU (`DRAVE_GPU_TETE=1`, déjà mesuré à 6,2 ms/jeton contre 15,6 pour tête + échantillonnage sur gpt-oss) »
- `:153` — « thread '<unnamed>' panicked at src/engine.rs:473:77: index out of bounds: the len is 90 but the index is 90 »
- `:156` — « `90` = nombre de blocs de 32 d'un jeton (2 880 / 32), pas le nombre de jetons du lot »
- `:168` — « dix minutes d'attente active au lieu d'une erreur (même classe de panne que le blocage de 27 minutes raconté dans `REPRISE.md`) »
- `:172` — « `tests_gemm_q4` fait tourner des lots de 1, 8, 9, 17 et 40 jetons sur une matrice de 256 colonnes — soit des lots **plus grands que le nombre de blocs (8)** »
- `:179` — « « un worker du pool est mort pendant le calcul (panique ci-dessus) » »
- `:187` — « le facteur à gagner est donc de l'ordre de 16 sur la partie « projections » »
- `:193` — « | Qwen2.5-0.5B Q8_0, `--dense`, 16 fils | 512 | 17,1 s | **13,6 s** | **−20 %** | »
- `:194` — « | gpt-oss-120b MXFP4, MoE groupé, 16 fils | 256 | ≈ 50 s | 34,4 s (lot 256) | **−31 %** | »
- `:197` — « la porte de non-régression Qwen contexte 256 reste à **19,3885** »

**rapport-prefill-reparti.md**
- `:5` — « un préremplissage de 256 jetons traverse désormais le réseau en **4 lots** (ou un seul) au lieu de 255 flux »
- `:12` — « `attente ≈ calcul distant + 3,2 × latence par message` »
- `:13` — « Avec 60 ms d'aller-retour, 256 jetons coûtaient 15 secondes d'attente pure »
- `:41` — « | 256 jetons en lots de 64 | 4 | **0,00e0** (18,0851 = 18,0851) | »
- `:42` — « | 256 jetons en UN lot de 917 583 octets | 1 | **0,00e0** | »
- `:43` — « | contrôle `--lot 1` (un flux par jeton) | 255 | **0,00e0** (18,0206 = 18,0206) | »
- `:44` — « | **1 024 jetons en lots de 64** | 16 | **0,00e0** (9,5939 = 9,5939), 16 lots pour 1 024 jetons | »
- `:48` — « le par-lots contre le jeton par jeton donne ~1e-4 sur Qwen »
- `:57` — « | **en UN lot de 64** | 1 | 1 145 ms | 1 488 ms | **2,6 s** | »
- `:59` — « | un flux par jeton | 63 | 350 ms/jeton | 394 ms/jeton | **47,6 s** | »
- `:61` — « Même calcul, même fidélité (0,00e0 des deux côtés) : **18×** »
- `:62` — « Chaque aller-retour coûte ~4 × 20 ms de latence pure, et le mode lot en supprime 62 sur 63 »
- `:73` — « | un flux par jeton | 116,7 ms | **116,7 ms** | »
- `:74` — « | lots de 16 | 358,0 ms | 22,4 ms | »
- `:75` — « | lots de 64 | 1 185,3 ms | 18,5 ms | »
- `:76` — « | **un seul lot de 256** | 4 255,6 ms | **16,6 ms** | »
- `:78` — « **7× plus rapide par jeton** »
- `:86` — « Le lot voyage en **f32 dense, 3 663 octets par jeton en mode dense** »
- `:89` — « À 20 jetons/s le débit demandé reste sous 1 Mbit/s. »
- `:93` — « `envoyer_lot` écrivait 40 octets pour un `TAILLE_TETE` de 39 »
- `:101` — « le banc de contrôle en mode dense l'a dit tout de suite : 5,61e0 au lieu de 0,00e0 »
- `:107` — « soit ÷2,3 sur le fil à 2,7 % d'écart — la même recette que le mode 2, répétée par état »

**rapport-programme-evolutif.md**
- `:17` — « **+3,0 %** (96,75 s → 99,64 s sur 1 025 tokens) »
- `:18` — « 2048 × 896 × 4 o = **7 Mo pour 2 048 tokens** »
- `:19` — « ~1,2 Mo/token, soit 19 Mo/s à 15,8 tok/s »
- `:23` — « 1,2 Mo/token au lieu de 706 Mo »
- `:27` — « l'inférence occupe 16 threads sur 40, une carte GPU sur deux, et 125 Go de RAM dont l'inférence n'utilise que 1,3 Go »
- `:36` — « η² (variance de perte expliquée par la grappe), apprentissage | 6,2 % »
- `:37` — « Écart grappe la plus dure / la plus facile | **7,1×** (perte 5,51 contre 0,77) »
- `:39` — « **R² hors échantillon (K=32)** | **+0,007** »
- `:40` — « **Corrélation des pertes par grappe, apprise → testée (K=32)** | **r = +0,573** »
- `:41` — « Même corrélation à K=128 | r = +0,232 »
- `:42` — « **R² < 0** à toute régularisation (−7,5 à −0,21) »
- `:53` — « **+30 % de débit à taux d'événements égal** (élagage contigu 17,91 tok/s contre dispersé 13,77) »
- `:64` — « **69,2 % des poids** sont dans des projections **saturées** ... `ffn_gate`, `ffn_up`, `attn_q`, `attn_output` »
- `:67` — « 100,00 % des directions de la trace hebbienne »
- `:69` — « **30,8 %** sont dans des projections **ouvertes** : `attn_k` (127/896), `attn_v` (128/896), `ffn_down` (896/4864) »
- `:72` — « **401 856 monômes quadratiques** `x_i·x_j` sont hors du span linéaire »
- `:84` — « | 4 | 366,8 s | 10 | **98 évaluations/h** | »
- `:85` — « | 8 | 215,5 s | 5 | 83 évaluations/h | »
- `:86` — « | 1 (extrapolé) | ~1 284 s | 40 | ~112 évaluations/h | »
- `:89` — « **~100 évaluations de modèle par heure**, en continu ... Soit 2 400 par jour »
- `:91` — « le moteur monte mal en charge au-delà de 8 threads »
- `:96` — « Un expert qui ne tire pas coûte **zéro octet** »
- `:98` — « Un modèle à 100 experts dont 2 tirent par token coûte donc, chez nous, le prix de 2 experts »
- `:102` — « Le moteur lit 706 Mo/token à 10,4 Go/s alors que la machine en offre 28,7 ... (2,8× de marge) »
- `:105` — « ~2,8 passes supplémentaires tiennent dans la bande passante actuelle »
- `:113` — « OpenBLAS à 759 GFLOP/s »
- `:137` — « -> /tmp/act_log.bin (2048 x 896 f32), /tmp/loss_log.bin (pertes par token) »

**rapport-routage-experts.md**
- `:19` — « | Kimi-K2.7-Code | `deepseek2` | **2 — sigmoïde** | softmax ✗ | »
- `:20` — « | GLM-5.3 / -Flash | `glm-dsa`, `glm5next` | **2 — sigmoïde** | softmax ✗ | »
- `:21` — « | DeepSeek-V4-Flash | `deepseek4` | **4 — racine de softplus** | softmax ✗ | »
- `:22` — « | DeepSeek-V4.1-Flash | `deepseek41` | *(dans le JSON `config`)* | **dense : `n_expert = 0`** ✗ | »
- `:26` — « `expert_weights_scale` (`routed_scaling_factor`) : **1,5** pour V4-Flash et V4.1, **2,5** pour GLM-5.3, **2,827** pour Kimi-K2.7 »
- `:30` — « `hash_layer_count` : les **trois premières couches** de V4-Flash ne routent pas par score mais par **table** »
- `:32` — « `ffn_gate_tid2eid.weight`, un tenseur I32 de `[129 280 × 6]` »
- `:39` — « il prenait ce modèle de 341 Go pour un modèle **dense** »
- `:64` — « | Qwen2.5-0.5B Q8_0 ctx 256 (dense) | 19,3885 | **19,3885** | inchangée, au bit près | »
- `:65` — « | Qwen3-30B clusters ctx 64, 8 jetons | 799,8557 | **799,8557** | inchangée, au bit près | »
- `:66` — « | gpt-oss-120b ctx 256 | 15,1757 | **15,6017** | **changée** ... | »
- `:72` — « **15,1757 était auto-cohérent, pas juste.** »
- `:75` — « réunir les deux chemins de routage a d'abord déplacé la porte Qwen3-30B de 799,8557 à 799,8152 (−0,005 %) »
- `:78` — « la renormalisation était écrite `x / s` au lieu de `x * (1/s)` ... et 48 couches l'amplifient »
- `:79` — « un `git worktree` sur le commit précédent, 28 s de compilation »
- `:91` — « | Kimi-K2.7-Code | 1 026 G | MLA à rang faible, hyper-connexions | »
- `:92` — « | GLM-5.3 | 754 G | MLA à rang faible, hyper-connexions, attention par index | »
- `:93` — « | DeepSeek-V4.1-Flash | 755 G | les trois + engram + sortie à rang faible | »
- `:94` — « | DeepSeek-V4-Flash | 284 G | MLA à rang faible, hyper-connexions, sortie à rang faible | »
- `:95` — « | GLM-5.3-Flash | 321 G | identique à GLM-5.3 | »
- `:99` — « aucun de ces cinq modèles n'a jamais été exécuté par ce moteur »
- `:116` — « | llama.cpp (référence) | **5420,40** | — | — | — | »
- `:117` — « | drave, biais **hors** des poids (nouveau) | **6443,13** | **0,989242** | 0,4364 | 2/4 | »
- `:118` — « | drave, biais **dans** le softmax (ancien) | 6625,80 | 0,989142 | 0,4134 | 2/4 | »
- `:125` — « | llama.cpp (`llama-perplexity -c 256 --chunks 2`) | **166,85** | »
- `:126` — « | drave, YaRN **à retardement** (le défaut) | **15,6017** | »
- `:127` — « | drave, YaRN **forcé** (`DRAVE_YARN=1`) | **84,07** | »
- `:132` — « à ctx 512, YaRN coûtait un facteur 9 : 174,34 contre 18,58 »
- `:136` — « La validation externe qui compte est celle de Qwen2.5-0.5B, **sans YaRN** : 19,3885 contre 18,9750 chez llama.cpp (2,2 %) »
- `:150` — « | llama.cpp (référence) | **4286,13** | — | — | »
- `:151` — « | drave | 42 617 589 | **−0,039** | **0/3** | »
- `:154` — « le moteur prédit le MÊME jeton (106880) aux trois positions »
- `:157` — « **La MLA à rang faible n'est donc pas validée** : elle est implémentée, elle tourne, elle est fausse quelque part »

**rapport-session-2026-09-30.md**
- `:3` — « 10h06–11h42 (time-box de 2 h), 11h46–15h00 puis 15h07–18h00 »
- `:12` — « écart local/réparti **0,00e0** — 144,8289 des deux côtés à 40 jetons, 9,5146 à 1 024 »
- `:13` — « 256 jetons en **4 lots** (ou 1 seul) → 0,00e0 ; **18× plus rapide** »
- `:14` — « dense 3 663 octets → **1 629** par flux (÷2,3) pour 1,3 % d'écart à 1 024 jetons »
- `:15` — « clés f32 + valeurs int8 **+0,023 %** contre **+3,01 %** ... (facteur **130**) ; 4 bits : +0,46 % contre **+385 %** (facteur **840**) »
- `:16` — « **Format de trace v2/v3** | 132 396 736 → **66 370 408** (sans perte) → **45 079 930** octets (+0,074 % de perplexité) »
- `:17` — « **Mode 4 — lot en listes** | **1,5 ko par jeton** au lieu de 3,5 (÷2,3) ; écart 3,03e-2 à 256 jetons »
- `:18` — « **Protocole v5** | cinq modes, contrat d'activation complet (14 champs) »
- `:19` — « 968 ms par couche à 1 M contre 13,2 ms avec le miroir VRAM »
- `:20` — « dépôt en un fichier (4,5 Mo), notebook (texte réel : perplexité ~20 au lieu de 17 869) »
- `:21` — « **46 sur 110** l'étaient dans au moins un mode ; neuf corrigés »
- `:22` — « 80 affirmations vérifiées, 38 périmées, 15 contradictoires »
- `:27` — « **vingt-sept n'ont pas été trouvés par un banc** mais par une relecture »
- `:31` — « trouvé en lisant, mesuré ensuite : ×11,2 »
- `:46` — « un plafond qui ne couvrait qu'une des quatre allocations pilotées par le réseau (16 Gio sur une trame de 83 octets) »
- `:52` — « Mon premier « rejeu v3 = 19,3885 » était un faux positif — la trace n'était pas chargée du tout »
- `:53` — « le chiffre 19,3045 de la table de non-régression ne s'est pas reproduit : il vaut 19,5633 »
- `:60` — « **quatre tests** de plus sur le protocole (17 au total) »
- `:63` — « la perplexité du banc passe de 17 869 à ~20, et l'écart reste 0,00e0 »
- `:68` — « **9/9 sondes trouvées** — même avec l'int8/int8 »
- `:70` — « l'attention coûte 70 ms par passe avec des clés f32, **162 ms avec des clés f16** ... et 174 ms en int8 »
- `:72` — « le miroir VRAM la ramène à 1,7 ms (43 ms par jeton sur 24 couches) »
- `:74` — « **Mode 3 (lot dense) à 1 024 jetons** : écart **0,00e0**, seize lots de 64. »
- `:76` — « vérifié à l'octet près sur 258 Mo d'états légaux (refus à l'état 72 393, le point de franchissement des 256 Mo) »
- `:92` — « Qwen ctx 256 = **19,3885** · gpt-oss ctx 256 = **15,1757** · gpt-oss avec `DRAVE_GPU=1` = **15,1667** »
- `:93` — « `cargo test` **13/13** · dépôt propre, quarante commits »

**rapport-tete-garantie.md**
- `:9` — « La borne est 12,6 fois plus lâche que le logit maximal sur les poids réels »
- `:17` — « une passe unique calcule `||w_i||` pour les 151 936 lignes de la tête et les trie par norme décroissante »
- `:31` — « sans : [512, 13309, 321, 1788, 12422, 84, 13, 356] »
- `:32` — « avec : [512, 13309, 321, 1788, 12422, 84, 13, 356] »
- `:39` — « Sur la vraie matrice de tête (Qwen2.5-0.5B, 151 936 × 896 en Q8_0, 2 048 lignes échantillonnées) »
- `:44` — « | logit maximal | **+1,4283** | »
- `:45` — « | borne globale `max ‖w_i‖·‖h‖` | 18,0381 — **×12,6** le logit max | »
- `:46` — « | borne par blocs de 32 ... | 17,6646 — ×12,4 | »
- `:47` — « | lignes encore candidates (globale) | **2 048 / 2 048 = 100 %** | »
- `:52` — « la boucle de paliers a effectivement calculé **151 936 lignes sur 151 936** à chaque jeton »
- `:54` — « le même verdict que la session précédente (borne « 5 à 20× trop lâche ») »
- `:70` — « | `--tete-restreinte` | ×7 sur la tête (13 % du vocabulaire suffit) | **changée** ... | »
- `:71` — « | `--tete-garantie` | **nul** (12,6× trop lâche) | identique, prouvé | »
- `:92` — « Le disque NVMe de cette machine a été mesuré à **5,37 Go/s avec un lecteur et 31 Go/s avec seize** »
- `:95` — « 120 blocs de 4 Mo — l'ordre de grandeur d'un expert »
- `:99` — « | disque mécanique (13 To) | 0,26 Go/s | 0,20 Go/s | **×0,78** | »
- `:100` — « | NVMe (FastNVMe) | 3,11 Go/s | 2,72 Go/s | **×0,88** | »
- `:107` — « le facteur 5,8 mesuré entre un et seize lecteurs valait pour des lectures explicites »
- `:109` — « C'est la cinquième fois qu'un mécanisme de prélecture est mesuré ici, et la cinquième fois qu'il ne donne rien »

**rapport-tete-restreinte.md**
- `:16` — « | 10 000 | 1 462 | 0,96 % | »
- `:17` — « | 100 000 | 4 659 | 3,07 % | »
- `:18` — « | 1 000 000 | 15 768 | 10,38 % | »
- `:19` — « | 3 050 991 | **19 793** | **13,03 %** | »
- `:21` — « Exposant de Heaps ≈ **0,21** ... **13 % est un plafond de fait.** »
- `:28` — « | médian | **3** | »
- `:29` — « | p90 | 250 | »
- `:30` — « | maximum | 4 319 | »
- `:32` — « Un vocabulaire de 16 384 tokens contient donc **100 %** des vrais jetons d'un corpus français. »
- `:41` — « | français | 13,0 % | 9,384 s | 8,400 s | **+10,5 %** | »
- `:42` — « | anglais | 5,8 % | 1,155 s | 0,982 s | **+15 %** | »
- `:52` — « | complète | `[6224, 1076, 330, 438, …]` — identique à sans ✅ | »
- `:53` — « | française | `[1129, 269, 330, 304, …]` puis **boucle** | »
- `:54` — « | anglaise | `[77455, 330, 279, …]` — différent | »
- `:67` — « précalcul de `‖W_o‖` pour chaque ligne (608 Ko pour 151 936 tokens) »
- `:72` — « en haute dimension, le cosinus typique est de 0,05 à 0,2, donc la borne est **5 à 20 fois** le logit réel »
- `:75` — « la génération ne terminait pas là où la tête entière prend 6,9 ms »
- `:80` — « `--tete-bornee` y était **silencieusement ignoré** »
- `:93` — « | 0 | 85,4 % | **19,3885** | référence | »
- `:94` — « | 0,01 | 61,5 % | 22,3563 | +15 % | »
- `:95` — « | 0,02 | 30,3 % | 28,7635 | +48 % | »
- `:96` — « | 0,05 | **5,1 %** | **2 073,80** | **×107** | »
- `:115` — « `--tete-bornee` a été **retirée du code** après mesure »

**rapport-transport-liste.md**
- `:4` — « **897 octets au lieu de 3 623** à seuil 5 %, et **1 568** avec des indices par écarts »
- `:6` — « jeter des canaux coûte cher (**×1,8 de perplexité** à ce seuil) »
- `:10` — « (39 octets à l'époque de ces mesures, **79** depuis que les top-k voyagent) »
- `:15` — « | 0 · dense f32 | `896 × f32` | **3 623** (39 + 3 584) | »
- `:25` — « | dense f32 | 100 % | 3 623 | 3 623 | 144,8289 | **144,8289** | **0,00e0** | »
- `:26` — « | listes 0,00 | 100,0 % (896) | 3 623 | 3 623 | 144,8289 | 141,0539 | 2,6e-2 | »
- `:27` — « | listes 0,02 | 60,4 % (541) | 2 203 | 2 677 | 203,8033 | 213,7739 | 4,9e-2 | »
- `:28` — « | listes 0,05 | 24,0 % (215) | 897 | 993 | 493,0344 | 893,1350 | 8,1e-1 | »
- `:29` — « | listes 0,10 | 36,5 % (327) | 1 347 | 216 | 35 483,0643 | 66 813,6606 | 8,8e-1 | »
- `:35` — « Sans eux : écart 0,69. »
- `:47` — « Le rejeu d'une trace quantifiée sur 16 bits redonnait la perplexité **exacte** (19,3885), mais ici 16 bits coûtent 2,6 % »
- `:69` — « **en mode dense, où le transport est exact, l'écart passe de 0,00e0 à 5,61e0** (perplexité 119 contre 18,02) »
- `:89` — « `flux en version 99, cette build parle la 5 (pair incompatible : rien n'a été interprété)` »
- `:92` — « Deux nœuds lancés avec des seuils différents calculaient deux choses différentes en silence (écart 0,69 mesuré) »
- `:95` — « le flux fait 896 canaux quand mon compteur en annonçait 919 (division par 39 au lieu de 40) »
- `:100` — « Trois octets par neurone actif (indice u16, valeur **i8**) plus une échelle f32 par bloc de 32 »
- `:105` — « | 0,00 | 98,1 % | 2 793 | 7,1e-2 | 3 622 octets · 2,6e-2 | »
- `:106` — « | 0,02 | 60,4 % | **1 778** | **2,2e-3** | 2 203 octets · 4,9e-2 | »
- `:107` — « | 0,05 | 24,0 % | 799 | 1,1e0 | 897 octets · 8,1e-1 | »
- `:122` — « `--flux-blocs --act-thresh 0.01`, soit **÷2,3 sur le fil pour 2,7 %** de perplexité »
- `:128` — « Mesuré sur **256 jetons de WikiText-2**, où la référence locale vaut 18,02 »
- `:132` — « | dense f32 | — | 100 % | 3 623 | **0,00e0** | »
- `:133` — « | blocs | 0,01 | 78,6 % | 2 268 | 2,7e-2 | »
- `:135` — « | listes i16 | 0,02 | 59,2 % | 2 159 | 1,6e-1 | »
- `:149` — « | 64 | 1,37e-1 | 2 249 | 77,9 % | »
- `:152` — « | **1 024** | **1,32e-2** | **1 589** | 79,8 % | »
- `:161` — « **÷2,3 sur le fil pour 1,3 % d'écart à 1 024 jetons** (2,7 % à 256, 13,7 % à 64) »
- `:170` — « l'écart au neurone actif précédent tient sur **un octet** dans l'immense majorité des cas ; 255 est l'échappement vers l'indice absolu »
- `:176` — « | dense f32 | 3 623 | 0,00e0 | 18,0206 | »
- `:178` — « | **blocs 0,01, indices par écarts** | **1 568** | **2,74e-2** | **21,8873** | »
- `:183` — « À 20 jetons/s, cela demande **0,25 Mbit/s**. »
- `:191` — « | calcul local (12 couches) | 15,6 ms/jeton | 15,9 ms/jeton | »
- `:192` — « | attente du pair | **97,6 ms/jeton** | **16,1 ms/jeton** | »
- `:193` — « | rapport attente/calcul | **6,26×** | **1,01×** | »
- `:194` — « | durée du banc réparti | 24,5 s | **8,3 s** (référence locale : 8,2 s) | »
- `:198` — « Le pilote écrit un en-tête de 39 octets puis un corps »
- `:200` — « Une ligne de code (`set_nodelay(true)`, des deux côtés) divise l'attente par six. »
- `:209` — « | 0 ms | 16,8 ms/jeton | 1,01× | 11,0 s | 0,00e0 | »
- `:210` — « | 5 ms | 33,0 ms/jeton | 1,99× | 15,1 s | 0,00e0 | »
- `:211` — « | 20 ms | 81,8 ms/jeton | 4,89× | 27,6 s | 0,00e0 | »
- `:217` — « attente ≈ calcul distant + 3,2 × (latence par message) »
- `:224` — « un aller-retour de 60 ms donne 16 + 3,2 × 30 ≈ **112 ms par jeton**, soit ~8 jetons/s au lieu de ~60 en local »
- `:231` — « le flux pèse 3 623 octets (dense) ou 1 989 (blocs à 68 % d'activité), et le calcul distant coûte 16 ms »
- `:232` — « le réseau demande donc **moins de 1 Mbit/s par flux de jetons à 20 jetons/s** »

**rapport-travail-reel.md**
- `:3` — « un modèle de 30,5 G paramètres (Qwen3-30B-A3B, MoE top-8, Q4_K_M) sur CPU, 16 fils, lecture en place — aucune copie »
- `:21` — « 89 jetons en 15,8 s (**5,62 tok/s**), premier jeton en 166 ms »
- `:36` — « **arrêt spontané après 67 jetons** au lieu des 200 demandés »
- `:43` — « | Famille Qwen (0,5 B → 30 B MoE), Q4_K / Q6_K / Q8_0 / Q4_0 / MXFP4 | ✅ | »
- `:44` — « | Lecture en place, zéro copie (30 B en 17,7 Go = taille du fichier) | ✅ | »
- `:48` — « | Débits mesurés | 0,5 B : 32 tok/s · 1,5 B : 17 · 30 B MoE : **5,6** · 7 B : 2,8 | »
- `:82` — « **Correct, cohérent, en 5,5 tok/s** sur un modèle de 117 G paramètres, 62 Go résidents, lecture en place »
- `:85` — « notre **perplexité de 39,8** sur du wikitext brut là où l'on attendrait de l'ordre de 6 »
- `:89` — « le tokenizer o200k a été vérifié sur sept chaînes pièges, pas sur les 4 424 jetons du corpus »
- `:108` — « attention en O(contexte), KV en f32 : 800 Mo à 8 k pour le 30 B, et +100 ms/jeton »
- `:117` — « 5,6 jetons par seconde sur un 30 B MoE »

**rapport-v4-couches-0-1.md**
- `:5` — « hyper-connexions à **1e-7**, attention et sortie groupée à **0,99999** de corrélation »
- `:11` — « `attention.compress_ratios` de V4-Flash : **21 couches CSA** (ratio 4) »
- `:12` — « **20 couches HCA** (ratio 128), **3 couches brutes** (0, 1, 43) »
- `:24` — « (`hc_attn_pre`, `qr`, `qr_norm`, `q_norm`, `kv_norm`, `attn_derope`, `attn_out`, `l_last`) »
- `:28` — « Le même texte (20 000 octets de WikiText-2) »
- `:36` — « | `hc_attn_pre` (mélange des 4 copies) | 0 | **1,000000** | **1,5e-8** | »
- `:37` — « | `qr` (descente q_a) | 0 | 0,999993 | 1,1e-3 | »
- `:40` — « | `attn_derope` (sortie d'attention dé-tournée) | 0 | **0,999996** | 1,9e-2 | »
- `:42` — « | `l_last` (état après `hc_post`) | 0 | 0,999811 – 0,999959 | 1,7e-2 | »
- `:46` — « sur les 16 384 valeurs de `l_last-0`, **49,5 % des écarts sont positifs** (50 % = bruit) »
- `:47` — « la médiane des erreurs relatives est de **0,1 %**, et l'écart absolu moyen de 1,0e-3 sur une dynamique de 0,9 »
- `:55` — « au Sinkhorn à 20 itérations »
- `:61` — « Corrélation `qr` **0,99866 → 0,999993** »
- `:69` — « position 0 juste, position 1 fausse de 30 % »
- `:79` — « Les couches 2 à 42 ne sont pas exécutées : il leur faut P4 (HCA) et P5 (CSA + indexeur) »
- `:82` — « La **fenêtre glissante** (`sliding_window` 128) »
- `:84` — « Le **cache KV quantifié** n'est pas exercé ici (32 bits) »
- `:91` — « **NLL moyenne 11,077944 · perplexité 64 727,68** »
- `:93` — « il remplace celui qui circulait (11,737136 / 125 133), mesuré sur un autre découpage »

**rapport-v4-hca.md**
- `:5` — « corrélation **0,999992** sur la sortie d'attention au 128ᵉ jeton »
- `:12` — « 21 couches **CSA** (ratio 4), 20 couches **HCA** (ratio 128), 3 brutes (0, 1, 43) »
- `:15` — « une **valeur** (`attn_compressor_kv`) et une **porte** (`attn_compressor_gate`) de 512 dimensions »
- `:18` — « une **`ape`** — une ligne apprise par rang dans le bloc (`pos % ratio`), de forme `[512, 128]` »
- `:24` — « tournée à la position de son **premier** jeton (`compress_rope_freq_base` = 160 000, pas 10 000) »
- `:26` — « `n_visible = (pos + 1) / ratio` »
- `:36` — « | `hc_attn_pre` | 1,000000 (1e-5) | **1,000000** (1e-5) | »
- `:37` — « | `attn_derope` | 0,99999 | **0,999992 – 0,999994** | »
- `:46` — « L'écart résiduel (0,02 sur une dynamique de 6,5, soit 0,3 %) »
- `:51` — « `attn_derope` était faux de 10 % dans ses **64 dernières dimensions** »
- `:52` — « alors que les **448 premières** (nope) étaient justes à 0,4 % »
- `:53` — « la corrélation globale restait à 0,996, donc « plausible » »
- `:64` — « il aurait dit le bug **avant** toute passe de 86 Go »
- `:70` — « la fenêtre d'un bloc est **2 × ratio** jetons »
- `:72` — « le projecteur fait **1024** valeurs par jeton »
- `:76` — « `attn_derope` **0,999990-0,999991**, `l_last` **0,99992-0,999994** »
- `:82` — « `dsv4_append_zero_row(score_state, /*neg_inf=*/true)` »
- `:84` — « corrélation **0,989** au lieu de 1,000000 — et **seulement au premier bloc** »
- `:86` — « L'hypothèse inverse (précédent = seconde moitié) donne 0,42 de corrélation ; « tout première moitié », 0,80 »
- `:90` — « qui, eux, concordaient déjà à 0,003 »
- `:105` — « | 4 | 1 | 3,2246 | 3,2279 | »
- `:110` — « Écart **0,1 à 0,3 %** »
- `:112` — « n'a d'effet qu'au-delà de `indexer.top_k` blocs, soit 2 048 jetons »
- `:120` — « `attention.indexer.top_k` (512) »
- `:127` — « V4-Flash déclare `swiglu_clamp_exp = 10.0` et `swiglu_clamp_shexp = 10.0` »

**rapport-valeur-unaire.md**
- `:3` — « Modèle mesuré : **qwen2** quantifié **Q4_0** (166 matrices 2-D) »
- `:4` — « Les niveaux sont lus *tels que stockés* (−8..+7), avant mise à l'échelle. »
- `:8` — « zéros : **12.9 %** des poids (densité 87.1 %) »
- `:9` — « `E[|v|]` sur les non-nuls : **3.02** »
- `:10` — « `E[popcount(|v|)]` : **1.39** »
- `:14` — « | 1 | 23.72 % | 27.2 % | »
- `:28` — « | **unaire (répétition d'adresse)** | **2.02** | **3.02** | »
- `:30` — « | **hybride (unaire pour \|v\|=1, puis plans)** | **1.12** | **1.12** | »
- `:45` — « Sur ce modèle Q4_0 réel : `E[|v|] = 3.02` → coût de la répétition 2.63 b/poids contre 4,00 en dense. »
- `:49` — « **Le ×2,17 annoncé ci-dessous est FAUX.** »
- `:51` — « un code de longueur `v−1` viole l'inégalité de Kraft (Σ2^−l ≈ 1,99 > 1) »
- `:55` — « l'encodage structurel retombe à ~3,5-4,4 b/poids, soit **pas mieux que le code 4 bits fixe** »
- `:57` — « **3,731 b/poids** pour ce Q4_0 (gain maximal ×1,07) »
- `:79` — « La répétition gagne alors **même à 4 bits** : 2.63 contre 4,00 b/poids. »
- `:83` — « **1.85 b/poids, soit ×2.17**, pour 0.98 opération par poids contre 0.87 en dense »
- `:89` — « l'encodage « listes signées » déjà mesuré à 0,39 b/poids »
- `:99` — « Q4_K_M, avec ses échelles de blocs plus fines, donnerait une distribution différente »

## C. Contradictions, chiffres périmés, affirmations douteuses

- `reports/rapport-optimisations-auto.md:38` — « le moteur prenait `cpu × 3/4` = **30** fils sur 40 threads logiques, il en prend **20** » — contredit frontalement `reports/rapport-optimisations.md:77` (« prend `3/4 × CPU` par défaut ») et `:124` (« la valeur par défaut est `3/4 × CPU` ») : les deux rapports décrivent des politiques de threads par défaut incompatibles.
- `reports/rapport-optimisations.md:105` — « chuter le débit de 3,09 à 0,97 G év/s (8 threads) » et `:121` — « `yield_now()` après N tours — **a tout empiré** (0,97 G à 8 threads) » — le même chiffre 0,97 G à 8 threads est attribué à deux causes différentes (barrière d'aliasing `&mut` au piège 2, `sched_yield` au piège 3) ; au moins une attribution est fausse.
- `reports/rapport-optimisations.md:86` — « La première campagne annonçait ... **Les deux chiffres étaient faux.** » — chiffres (3838 vs 3513 ; 7,53 G év/s) explicitement périmés par le texte.
- `reports/rapport-session-2026-09-30.md:92` — « gpt-oss ctx 256 = **15,1757** » — périmé : `reports/rapport-routage-experts.md:66` donne 15,1757 → **15,6017** et `:72` écrit « **15,1757 était auto-cohérent, pas juste.** » ; `reports/rapport-p0-flux.md:118` utilise 15,6017.
- `reports/rapport-session-2026-09-30.md:17` — « **Mode 4 — lot en listes** | **1,5 ko par jeton** au lieu de 3,5 (÷2,3) ; écart 3,03e-2 » — contredit par le même document `:82-83` : « **Mode 4 — lot en listes** ... Spécifié, pas écrit », et par `reports/rapport-prefill-reparti.md:107` (« le mode 4 décrit, non écrit »).
- `reports/rapport-session-2026-09-30.md:52` — « Mon premier « rejeu v3 = 19,3885 » était un faux positif — la trace n'était pas chargée du tout » ; `:53` — « le chiffre 19,3045 ... ne s'est pas reproduit : il vaut 19,5633 » — chiffres signalés faux/périmés par le texte.
- `reports/rapport-phase3-reparti.md:37` — « la classe « le drapeau est analysé mais jamais appliqué » que ce dépôt a déjà rencontré **cinq fois** » vs `reports/rapport-session-2026-09-30.md:43` — « la classe « analysé mais jamais appliqué », **huit fois** » vs `:21` — « **46 sur 110** l'étaient dans au moins un mode » : trois comptages incompatibles du même phénomène.
- `reports/rapport-optimisations-auto.md:134` — « **35 tests verts** » vs `reports/rapport-session-2026-09-30.md:93` — « `cargo test` **13/13** » (et `:60` « quatre tests de plus sur le protocole (17 au total) ») : trois totaux de tests différents, à dater.
- `reports/rapport-p0-flux.md:63` — « | **total** | **58,2 G** | 100 % | » vs `reports/rapport-p0-flux.md:101` — « | total / token | 83 104,0 M | 81 115,9 M | » — deux totaux incompatibles pour le même modèle (GLM-5.3) et le même rapport, sans réconciliation explicite (l'attention passe de 21,9 G à 29,2 G).
- `reports/rapport-p0-flux.md:120` — « GLM-5.3 exerce **les deux mêmes chemins** (MLA à rang faible + experts IQ), c'est donc lui qui porte la preuve aujourd'hui » vs `reports/rapport-routage-experts.md:92` — « | GLM-5.3 | 754 G | MLA à rang faible, hyper-connexions, attention par index | » et `:99` — « aucun de ces cinq modèles n'a jamais été exécuté par ce moteur » : GLM-5.3 ne peut pas à la fois porter une mesure de forward et être refusé faute de MLA à rang faible ; contradiction entre deux rapports de la même session.
- `reports/rapport-p0-flux.md:120` — « le forward de V4-Flash est refusé (hyper-connexions, sortie à rang faible) » vs `reports/rapport-v4-couches-0-1.md:3` — « les deux premières couches de **DeepSeek-V4-Flash** tournent dans Drave » : la formulation globale est périmée (seules les couches compressées manquent).
- `reports/rapport-routage-experts.md:161` — « La référence externe (llama.cpp) sur gpt-oss aux mêmes jetons est **lancée** ; elle doit confirmer ou contredire 15,6017 » vs `:123-127` du même fichier qui **donne déjà** les résultats (166,85 / 15,6017 / 84,07) : la section « ce qui reste ouvert » n'a pas été mise à jour après la §4bis (§5 est périmée dans le document).
- `reports/rapport-routage-experts.md:68` — « Le changement de gpt-oss est le seul effet visible sur les portes » vs `:75` — « réunir les deux chemins de routage a d'abord déplacé la porte Qwen3-30B de 799,8557 à 799,8152 » : la porte Qwen3 a bien bougé (corrigé ensuite) ; « au bit près » masque un aller-retour.
- `reports/rapport-passage-a-l-echelle.md:19` — « Le moteur ne lit que `F32`, `F16`, `Q8_0` et `Q4_0`. **Aucun modèle récent ne s'ouvre aujourd'hui** » — contredit dans le même fichier par `:89-96` (« **MXFP4 : fait, et vérifié sur le vrai fichier** ») et surtout par `reports/rapport-travail-reel.md:43-44` (« Q4_K / Q6_K / Q8_0 / Q4_0 / MXFP4 ✅ », « Lecture en place, zéro copie ... ✅ ») : état périmé.
- `reports/rapport-passage-a-l-echelle.md:79` — « Les 8 magnitudes valent `{0,1,2,3,4,6,8,12}` — donc, multipliées par 2, des **entiers** qui tiennent sur 4 bits » — incohérent avec `:91` du même fichier (« Les huit magnitudes du format sont `{0, ½, 1, 1½, 2, 3, 4, 6}` : **doublées**, ce sont les entiers `{0,1,2,3,4,6,8,12}` ») ; la première version est arithmétiquement fausse (doubler {0,1,2,3,4,6,8,12} ne tient pas sur 4 bits).
- `reports/rapport-passage-a-l-echelle.md:47` — « contre **41,6 tok/s mesurés** » (Qwen2.5-0.5B) vs `reports/rapport-travail-reel.md:48` — « 0,5 B : **32 tok/s** » : deux débits mesurés différents pour le même modèle.
- `reports/rapport-passage-a-l-echelle.md:60` — « | **Qwen3-30B-A3B** (MoE) | 3,3 G | 1,7 Go | 87 ms | **11,5** | » vs `reports/rapport-travail-reel.md:48` — « 30 B MoE : **5,6** » (et `:57` 7 B : 5,4 prédit vs 2,8 mesuré) : le modèle de coût prédit ~2× le débit réellement mesuré sur les gros modèles, sans que le rapport le signale.
- `reports/rapport-programme-evolutif.md:102` — « Le moteur lit 706 Mo/token à **10,4 Go/s** alors que la machine en offre **28,7** » vs `reports/rapport-passage-a-l-echelle.md:43` — « Bande passante atteinte sur cette machine : **20–25 Go/s** » et `reports/rapport-optimisations-auto.md:70` — « 22,5 pour la RAM » : le débit atteint par le moteur diffère d'un facteur 2 selon les rapports.
- `reports/rapport-optimisations-auto.md:46` vs `:48` — la table donne 16 lecteurs = **31,08 Go/s** et la vérification « 3,42 / 21,02 / **33,19** », puis la conclusion `:49` utilise « **31** contre 22 Go/s » : trois valeurs pour la même mesure, et le nombre de lecteurs des trois chiffres vérifiés n'est pas donné.
- `reports/rapport-optimisations-auto.md:44-49` — « Lecteurs disque = **16** » (recommandation) vs `reports/rapport-tete-garantie.md:102` — « **Les lecteurs parallèles n'apportent rien, et coûtent un peu** » (×0,78 et ×0,88) : deux conclusions opposées sur le parallélisme disque (lectures explicites vs défauts de page, mais le texte ne le dit qu'après coup).
- `reports/rapport-optimisations-auto.md:56` — « **90 Ko par jeton en F16**, soit **96,6 Go à 1 M** » — arithmétique incohérente : 90 Ko × 1 M = 90 Go (et ×1 048 576 = 94,4 Go), pas 96,6 ; 96,6 Go correspondrait à ~92 Ko/jeton.
- `reports/rapport-optimisations-auto.md:95` — « V4.1 (**365 Go** pour 115 Go de RAM) » vs `reports/rapport-routage-experts.md:39` — « ce modèle de **341 Go** » et `:93` — « DeepSeek-V4.1-Flash | 755 G » : deux tailles de fichier incompatibles pour le même modèle.
- `reports/rapport-placement-bits-kv.md:118` — « (la ligne GPU du banc ne vaut PAS pour le moteur : `--banc-kv` installe le miroir sans appliquer la règle d'homogénéité — relevé par un relecteur) » — mesure auto-déclarée invalide pour le moteur.
- `reports/rapport-placement-bits-kv.md:157` — « l'int8 complet coûte +2,25 % de perplexité **à ce contexte** » — le +2,25 % est mesuré à 4 096 (`:89`), alors que « ce contexte » désigne l'aiguille à 2 048 (`:148`) : attribution de mesure douteuse.
- `reports/rapport-precision.md:12` — « bitmap (1 bit/poids) + k bits par non-nul = **1 + k·d** bits/poids » vs `:22-31` — les valeurs b/poids de la table sont calculées avec la densité **réelle** (ex. « creux 1 bits d=0.125 » → densité 8.4 % → 1.08 ; « d=0.500 » → 26.6 % → 1.27), pas avec le `d` nominal : le modèle de coût affiché ne correspond pas à la table (et deux lignes de même `d` nominal ont des densités différentes : 8,4 % et 11,8 % pour d=0.125).
- `reports/rapport-prefill-par-lots.md:52` — « | 1 | **16,6 s** | » vs `:193` — « | Qwen2.5-0.5B Q8_0, `--dense`, 16 fils | 512 | **17,1 s** | » : deux temps différents pour le même lot 1 sur le même banc.
- `reports/rapport-prefill-par-lots.md:89` — « **la tête de sortie reste calculée jeton par jeton** (145 Mo lus par jeton) » puis `:95` — « il faut ... **traiter la tête comme un GEMM** » — explicitement réfuté plus loin par `:131-136` : « **La tête en lot ne gagne rien** ... L'argument de la §4 — « 145 Mo lus par jeton » — est un argument de *bande passante*, et il ne s'applique pas ». La conclusion de §4 est périmée.
- `reports/rapport-prefill-reparti.md:62` — « Chaque aller-retour coûte **~4 × 20 ms** de latence pure » vs `reports/rapport-transport-liste.md:217` — « attente ≈ calcul distant + **3,2 ×** (latence par message) » : deux facteurs différents pour le même banc ; et `reports/rapport-transport-liste.md:220-221` décrit « le flux et sa réponse, dans les deux sens » (4 messages) pour justifier 3,2.
- `reports/rapport-session-2026-09-30.md:14` — « dense 3 663 octets → **1 629** par flux (÷2,3) » vs `reports/rapport-transport-liste.md:152` — « | **1 024** | **1,32e-2** | **1 589** | » et `:178` — « **1 568** » : trois octets/flux différents pour des configurations proches, sans table de correspondance.
- `reports/rapport-transport-liste.md:10` — « (39 octets à l'époque de ces mesures, **79** depuis que les top-k voyagent) » — toutes les valeurs en octets/flux du rapport (3 623 ; 897 ; 1 568 ; 2 793...) sont donc périmées de 40 octets ; le rapport l'annonce mais ne les recalcule pas.
- `reports/rapport-transport-liste.md:29` — « | listes 0,10 | 36,5 % (327) | 1 347 | **216** | 35 483,0643 | 66 813,6606 | 8,8e-1 | » — activité qui **remonte** (24,0 % au seuil 0,05 → 36,5 % au seuil 0,10) et retour de 216 octets < aller 1 347 : anomalie reconnue (`:43` « la ligne 0,10 n'est donc pas comparable aux autres ») mais laissée dans la courbe.
- `reports/rapport-transport-liste.md:88` — « `flux en version 99, cette build parle la **5** » vs le titre du même ajout `:88` — « **Version dans chaque en-tête** (3.5) » vs `reports/rapport-session-2026-09-30.md:37` — « `VERSION_FLUX` restée à **3** avec un en-tête passé de 39 à 79 octets » : numérotation de version incohérente (3, 3.5, 5).
- `reports/rapport-tete-restreinte.md:32` — « Un vocabulaire de **16 384** tokens contient donc **100 %** des vrais jetons d'un corpus français » — contredit par la table juste au-dessus (`:19`) : **19 793** identifiants distincts observés (13,03 % d'un vocabulaire de 151 936), donc un vocabulaire de 16 384 ne peut pas les contenir tous ; l'affirmation ne vaut que pour le rang des tokens argmax (max 4 319), pas pour « les jetons du corpus ».
- `reports/rapport-valeur-unaire.md:49` — « **Le ×2,17 annoncé ci-dessous est FAUX** » vs `:83` — « **1.85 b/poids, soit ×2.17** » (verdict maintenu malgré le correctif) ; et `:30` (hybride = **1.12** b/poids, 1.12 op) vs `:83` (hybride = **1.85** b/poids, 0.98 op) : le tableau et le verdict donnent des chiffres différents pour la même stratégie.
- `reports/rapport-travail-reel.md:85` — « notre **perplexité de 39,8** sur du wikitext brut là où l'on attendrait de l'ordre de 6 » vs `reports/rapport-routage-experts.md:126` — « drave, YaRN à retardement (le défaut) | **15,6017** » et `:125` — llama.cpp 166,85 : trois régimes de perplexité gpt-oss non réconciliés (le rapport dit lui-même que le chiffre reste inexpliqué).
- `reports/rapport-v4-couches-0-1.md:93` — « il remplace celui qui circulait (**11,737136 / 125 133**), mesuré sur un autre découpage » — chiffre explicitement déclaré périmé.
- `reports/rapport-session-2026-09-30.md:20` — « perplexité ~20 au lieu de **17 869** » — l'ancien chiffre du banc Colab est périmé (le notebook utilise désormais du texte réel), comme le note `:63`.
- `reports/rapport-p0-flux.md:48` — « 313,7 M (FFN) + 136,1 M (tête) = **449,8 M** ✅ » — l'addition donne 449,9 M (313,79 + 136,13) ; écart d'arrondi de 0,1 M présenté comme une validation.
- `reports/rapport-programme-evolutif.md:27` — « l'inférence occupe **16 threads** sur 40 » vs `reports/rapport-optimisations-auto.md:38` — « il en prend **20** » (cœurs physiques) : le nombre de threads par défaut diffère selon les rapports.
- `reports/rapport-routage-experts.md:161-163` — « La comparaison à 510 jetons est lancée pour confirmer » (§4bis) puis « La référence externe (llama.cpp) sur gpt-oss aux mêmes jetons est **lancée** » (§5) : deux affirmations de « lancement » pour une mesure déjà présentée, signe de sections non relues.

## D. Fichiers du dépôt cités

- `reports/rapport-optimisations-auto.md` … `reports/rapport-valeur-unaire.md` — les 20 rapports eux-mêmes, cités entre eux (ex. `rapport-tete-restreinte.md`, `rapport-transport-liste.md`, `rapport-placement-bits-kv.md`, `rapport-phase3-reparti.md`, `rapport-prefill-reparti.md`).
- `reports/rapport-cpu-aer.md` — cité pour le « ni tri, ni dédoublonnage » de l'ordre naturel des écarts ; `reports/rapport-optimisations.md:159`.
- `reports/rapport-8bits.md` — cité pour l'encodage des niveaux quantifiés et les cas où la répétition d'adresse est optimale ; `reports/rapport-valeur-unaire.md:62`.
- `reports/rapport-compacite-trace.md` — format de trace v2/v3, 132 396 736 → 66 370 408 → 45 079 930 octets ; `reports/rapport-session-2026-09-30.md:16`.
- `reports/rapport-mode4-lot-listes.md` — mode 4 (lot en listes), 1,5 ko/jeton, écart 3,03e-2 ; `reports/rapport-session-2026-09-30.md:17`.
- `reports/rapport-drapeaux-ignores.md` — 46 drapeaux sur 110 ignorés dans au moins un mode, tableau `--options-actives` ; `reports/rapport-session-2026-09-30.md:21`.
- `reports/rapport-coherence-docs.md` — 80 affirmations vérifiées, 38 périmées, 15 contradictoires ; `reports/rapport-session-2026-09-30.md:22`.
- `format-flux.md` — spécification du protocole v5 (cinq modes, contrat d'activation à 14 champs, refus d'un pair incompatible) ; `reports/rapport-session-2026-09-30.md:18`.
- `plan-gpu-topk.md` — plan chiffré du noyau GPU de top-k (968 ms/lcouche à 1 M vs 13,2 ms avec miroir VRAM) ; `reports/rapport-session-2026-09-30.md:19`.
- `docs/contexte-long.md` — coût du préremplissage séquentiel (4,5 h à 32 k, 1 234 h à 1 M) ; `reports/rapport-prefill-par-lots.md:4`.
- `REPRISE.md` — journal du blocage de 27 minutes (worker mort sans rendre son jeton) ; `reports/rapport-prefill-par-lots.md:168`.
- `colab/README.md` — kit Colab en un fichier (4,5 Mo), notebook, trois voies de tunnel ; `reports/rapport-session-2026-09-30.md:20`.
- `drave-core/` — le moteur Rust `std` seul, zéro dépendance, 386 lignes de moteur ; `reports/rapport-optimisations.md:3`.
- `drave-core/src/model.rs` — `router` (routage MoE unique jeton/lot), `logits_garanti`, `Model::load`, `Model::load_partiel`, `verifier_architecture`, `forward`, `forward_lot`, `forward_mla`, `attn_mla`, `logits`, `logits_lot`, `emb_imposee(_lot)`, le commentaire sur `--tete-bornee` ; `reports/rapport-routage-experts.md:43`, `reports/rapport-tete-garantie.md:14`, `reports/rapport-tete-restreinte.md:116`, `reports/rapport-v4-couches-0-1.md:23`.
- `drave-core/src/engine.rs` — pool de threads, `Pool::gemm_dense_i8`, `gemm_dense_q4`, `Shared::gs32`, `Shared::morts`, `Pool::attendre`, `catch_unwind`, panique à `src/engine.rs:473:77` ; `reports/rapport-prefill-par-lots.md:12`, `:152`, `:170`, `:178`.
- `drave-core/target/release/drave` (binaire `./target/release/drave`) — commande de tous les bancs (`--ppl`, `--matrix`, `--lot`, `--q4`, `--hebbian`) ; `reports/rapport-placement-bits-kv.md:170`, `reports/rapport-passage-a-l-echelle.md:213`.
- `tools/aiguille.py` — Aiguille v2, test de récupération d'information enfouie (9/9 sondes) ; `reports/rapport-placement-bits-kv.md:148`.
- `tools/portes.sh` — exécute les portes de non-régression du dépôt, y compris la porte gpt-oss 15,6017 ; `reports/rapport-p0-flux.md:118`.
- `tools/ref_logits.cpp` (`ref_logits`, option `--tensors`, `REF_DUMP`) — référence llama.cpp : mêmes tenseurs nommés écrits en f32 pour comparaison étage par étage ; `reports/rapport-routage-experts.md:107`, `reports/rapport-p0-flux.md:119`, `reports/rapport-v4-couches-0-1.md:25`.
- `tools/compare_etats.py` — compare les vecteurs entiers Drave/llama.cpp (écart max, dynamique, corrélation) ; `reports/rapport-v4-couches-0-1.md:26`.
- `tools/proxy_latence.py` — relais ajoutant un délai par message (20 ms) pour les bancs de latence ; `reports/rapport-transport-liste.md:204`, `reports/rapport-prefill-reparti.md:53`.
- `tools/pair_factice.py` — faux pair parlant le protocole sans charger de modèle et disant ce qu'il reçoit ; `reports/rapport-transport-liste.md:93`.
- `tools/mla_synthetique.py` — modèle MLA jouet servant à exercer `forward_mla` ; `reports/rapport-routage-experts.md:169`.
- `tools/mesurer_lecture_experts.py` — rejoue la mesure de lecture d'experts (froid forcé, 120 blocs de 4 Mo) ; `reports/rapport-tete-garantie.md:114`.
- `tools/lire_meta_gguf.py --tenseur` — lit les métadonnées/tenseurs GGUF hors du moteur (reconstruction de la compression CSA) ; `reports/rapport-v4-hca.md:92`.
- `tools/colab_cote_local.sh` — script du kit Colab côté local ; `reports/rapport-session-2026-09-30.md:62`.
- `run_precision.py` — génère `rapport-precision.md` (banc prune/retrain/quantize) ; `reports/rapport-precision.md:80`.
- `run_value_encoding.py` — génère `rapport-valeur-unaire.md` (distribution des niveaux Q4_0) ; `reports/rapport-valeur-unaire.md:104`.
- `gguf` (module) : `gguf::q8_dot_at` — noyau Q8_0 de la tête, « lié au calcul » et non à la mémoire ; `reports/rapport-prefill-par-lots.md:133`.
- `models/` — `models/Qwen2.5-0.5B-Q8_0.gguf`, `../models/Qwen2.5-0.5B-Q8_0.gguf`, `models/Qwen2.5-0.5B-Q4_0.gguf`, `gpt-oss-120b-MXFP4.gguf`, Qwen2.5-1.5B-Instruct Q4_K_M, Qwen3-30B-A3B Q4_K_M : modèles de tous les bancs ; `reports/rapport-phase3-reparti.md:15`, `reports/rapport-passage-a-l-echelle.md:98`, `reports/rapport-placement-bits-kv.md:148`.
- Tenseurs GGUF cités comme points d'entrée : `blk.0.ffn_gate.weight`, `blk.0.ffn_down_exps.weight` (dims (2880, 2880, 128), type 39), `ffn_gate_tid2eid.weight` ([129 280 × 6], I32), `attn_k_b [64, 512, 192]`, `attn_v_b [64, 256, 512]` ; `reports/rapport-optimisations.md:4`, `reports/rapport-passage-a-l-echelle.md:101`, `reports/rapport-routage-experts.md:32`, `reports/rapport-p0-flux.md:91`.
- Fichiers temporaires de banc (hors dépôt) : `/tmp/wt2_a.txt`, `/tmp/wt2_ids.txt`, `/tmp/ids_qwen_long.txt`, `/tmp/act_log.bin`, `/tmp/loss_log.bin` ; `reports/rapport-parcimonie-imposee.md:134`, `reports/rapport-programme-evolutif.md:137`.
- Référence externe (pas le dépôt) : `llama.cpp/src/llama-graph.cpp` (`build_moe_ffn`, `selection_probs`, `ggml_soft_max_ext`, `ggml_soft_max_add_sinks`, `ggml_rope_ext_back`, `dsv4_append_zero_row`, `lid_score_masked`) ; `reports/rapport-v4-hca.md:129`, `reports/rapport-routage-experts.md:69`.

Now sending this to the parent in two messages.

- **send_message** `{"agent_id": "3d5618a0-4e3a-45bb-943d-a72c753fb7da", "message": "INVENTAIRE DRAVE — 20 rapports de reports/ — PARTIE 1/2 (sections A et B). Aucun fichier modifié.\n\n## A. Termes et sigles\n- **AER** (non développé dans le texte ; « réseau de combinaison façon routeur AER ») — réseau d'interconnexio … [31632 caractères tronqués]`

  ```
message delivered to agent 3d5618a0-4e3a-45bb-943d-a72c753fb7da
  ```

### 🤖 Assistant

⏵ Sending part 2 (contradictions and cited files) to the parent

- **send_message** `{"agent_id": "3d5618a0-4e3a-45bb-943d-a72c753fb7da", "message": "INVENTAIRE DRAVE — 20 rapports de reports/ — PARTIE 2/2 (sections C et D).\n\n## C. Contradictions, chiffres périmés, affirmations douteuses\n- `reports/rapport-optimisations-auto.md:38` — « le moteur prenait `cpu × 3/4` = **30** fils  … [16286 caractères tronqués]`

  ```
message delivered to agent 3d5618a0-4e3a-45bb-943d-a72c753fb7da
  ```

### 🤖 Assistant

⏵ Inventory complete and delivered to the parent agent

The exhaustive inventory of the 20 reports is complete (no repo file modified — reads and greps only), and both halves were sent to `3d5618a0-4e3a-45bb-943d-a72c753fb7da`:

- **Partie 1/2** — `## A. Termes et sigles` (~130 entrées, chacune avec définition, usage/outil, première occurrence `reports/fichier.md:ligne`) et `## B. Chiffres et affirmations mesurées` (une ligne par mesure, citation exacte, ~280 entrées).
- **Partie 2/2** — `## C. Contradictions, chiffres périmés, affirmations douteuses` (35 entrées) et `## D. Fichiers du dépôt cités` (~35 chemins + tenseurs GGUF + fichiers temporaires + référence externe llama.cpp).

Points saillants remontés au parent :

1. **Faux départs auto-signalés** : `19,3045 → 19,5633`, « rejeu v3 = 19,3885 » faux positif, chiffres périmés `11,737136 / 125 133` (remplacés par 11,077944 / 64 727,68), `×2,17` de l'unaires déclaré FAUX mais réaffirmé.
2. **Contradictions inter-rapports** : porte gpt-oss 15,1757 vs 15,6017 ; V4.1 = 341 Go vs 365 Go ; débit atteint 10,4 vs 20–25 Go/s ; Qwen 0.5B 32 vs 41,6 tok/s ; prédictions tok/s ~2× les mesures ; GLM-5.3 « exécuté » (p0-flux) vs « jamais exécuté, MLA à rang faible manquante » (routage-experts) ; mode 4 livré vs « spécifié, pas écrit » ; « cinq fois » vs « huit fois » vs « 46 sur 110 » ; 13/13 vs 35 tests.
3. **Incohérences internes** : totaux GLM-5.3 58,2 G vs 83,1 G dans le même rapport ; défaut de threads `3/4 × CPU` vs cœurs physiques ; 0,97 G év/s attribué à deux causes ; E2M1 `{0,1,2,3,4,6,8,12}` vs `{0,½,1,1½,2,3,4,6}` ; 90 Ko/jeton ≠ 96,6 Go à 1 M ; 1 629 vs 1 589 vs 1 568 octets/flux ; vocabulaire 16 384 ne pouvant contenir 19 793 identifiants distincts.
4. **Termes attendus mais absents** des 20 fichiers : DRVF/DRVF v5, PTX, RSS, IQ2_XXS, HBM, M20K, greffon, liste valuée, shard, p50/p95, MTok/s, Gbit/s, bf16, Hadamard, LoRA, MTP.

