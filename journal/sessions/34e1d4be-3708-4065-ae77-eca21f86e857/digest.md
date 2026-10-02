# Session DSH — relecture

- identifiant : `34e1d4be-3708-4065-ae77-eca21f86e857`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-02 09:52:01
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu es relecteur ADVERSE. Tu ne modifies AUCUN fichier : tu produis un rapport de constats, avec citations exactes et numéros de ligne.

Contexte : le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet contient un moteur d'inférence nommé **Drave**. Sa vision est définie dans `docs/vision.md` et `docs/programme-recherche.md` — lis-les ENTIER d'abord (ce sont les textes de référence), puis audite les documents ci-dessous.

Résumé de la vision à faire respecter :
- Drave conduit un **flux de listes d'activation** (AER, « push ») ; le coût suit l'ACTIVITÉ, pas la taille du modèle.
- Encodages : listes valuées **par source** (échelle par bloc de 32) ; **deux listes** (trinaire : le signe porté par l'appartenance aux listes « + » / « − », plus de valeur stockée) ; cas général **connexions pondérées** (source → destination, poids).
- Le cœur est de **router ces flux sur des grappes de neurones** réparties entre composants (CPU, GPU, FPGA) et entre **machines**.
- Le flux est un **journal** : tracer, rejouer, comparer, transporter — et il sert à **analyser le comportement du modèle pour adapter l'architecture à la tâche**.
- Le dense existe et gagne au-dessus d'environ 22 % de densité (mesuré) : la vision ne prétend pas que le sparse gagne toujours.
- Chaque chiffre publié a sa source ; un échec se documente.

Faits À JOUR au 02/10/2026 (toute divergence est une incohérence à signaler) :
- porte gpt-oss ctx 256 = **15,6017** (avant le 02/10 : 15,1757) ; Qwen2.5-0.5B ctx 256 = **19,3885** ; clusters Qwen3-30B = **799,8557** ; `cargo test --release` = **48 tests** ;
- protocole de transport des flux = **v5** (modes 0-4, dont « LOT en listes ») ;
- 18 formats lisibles, dont IQ1_S/IQ1_M/IQ2_XXS/IQ3_XXS/IQ4_XS/Q3_K/Q5_K/Q5_0, tous vérifiés contre libggml (`tools/portes_formats.sh`) ;
- les formats de super-bloc SANS noyau dédié (Q2_K, Q3_K, Q5_K, IQ*) sont lus par **déquantification puis produit f32** : juste, plus lent qu'un noyau — c'est un état assumé ;
- l'attention MLA à rang faible est validée contre llama.cpp (GLM-5.3, corrélation 0,999024) ; DeepSeek-V4.1 ne se calcule pas encore (hyper-connexions, sortie à rang faible, dé-rotation+puits, attentions compressées CSA/HCA) et llama.cpp ne connaît pas l'architecture `deepseek41` ;
- le plan V4.1 est `docs/plan-deepseek41-complet.md`, écrit « les flux d'abord ».

DOCUMENTS À AUDITER (lis-les en entier) :
1. docs/format-flux.md
2. docs/format-clusters.md
3. docs/convertisseur.md
4. docs/colab-reparti.md
5. docs/contexte-long.md

Ce que tu cherches, par ordre d'importance :
1. **Contradictions** entre ces documents et la vision, ou entre eux (par exemple : un document qui décrit le format de flux comme un simple format de trace alors qu'il sert aussi au rejeu et au transport ; un document qui décrit le découpage en grappes comme un simple rangement de fichiers alors que c'est le mécanisme de placement des neurones sur plusieurs machines).
2. **Chiffres périmés** (portes, tests, version de protocole, liste des formats).
3. **Cadrage qui dilue la vision** : passages qui présentent le moteur comme dense, ou qui font de llama.cpp la référence de valeur, ou qui traitent la sparsité comme une optimisation plutôt que comme le contrat.
4. **Absence de la finalité d'analyse** (les flux servent à comprendre et adapter l'architecture à la tâche) dans les documents qui décrivent le format ou le transport.
5. **Affirmations non sourcées** (chiffre sans renvoi à un rapport ou fichier).

Format de sortie, strictement : un tableau markdown

| fichier:ligne | citation exacte (≤ 25 mots) | problème | correction minimale proposée (texte de remplacement exact) | gravité |

puis une liste courte « ce qui est déjà cohérent et ne doit pas être touché », et une liste « points à trancher par l'humain » s'il y en a.

Règles : corrections MINIMALES uniquement (une phrase à remplacer, un chiffre à corriger, une phrase de cadrage à ajouter) — jamais de réécriture. Aucun faux positif : cite la ligne exacte. Si un document est cohérent, dis-le en une ligne. Maximum 25 constats.
Your parent agent id is "bbd6969f-0f70-42b2-8951-64d1f2f36d2e". Before you finish, send your result to that agent with send_message({ agent_id: "bbd6969f-0f70-42b2-8951-64d1f2f36d2e", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Reading the two reference documents first, then the five audited docs.

- **bash** `{"command": "ls /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/ && wc -l /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/*.md", "description": "List docs and count lines"}`

  ```
colab-reparti.md
comparaison-spiking.md
contexte-long.md
convertisseur.md
format-clusters.md
format-flux.md
histoire.md
plan-deepseek41-complet.md
plan-deepseek-v4-flash.md
plan-gpu-topk.md
plan-mla-vision.md
plan-mode4-lot-listes.md
plan-modeles-lourds.md
plan-prefill-reparti.md
programme-recherche.md
roadmap.md
sprints.md
vision.md
   127 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/colab-reparti.md
   145 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/comparaison-spiking.md
   580 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md
   317 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/convertisseur.md
   184 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-clusters.md
   183 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-flux.md
    78 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/histoire.md
   303 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-deepseek41-complet.md
    80 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-deepseek-v4-flash.md
   134 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-gpu-topk.md
   725 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mla-visio
… [564 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/vision.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/vision.md</path>
<type>file</type>
<content>
1: # Drave — la vision
2: 
3: > *« Stream of logs »* : le flux des listes. Et, en français d'ici, **la drave** —
4: > ces billots qu'on confiait à la rivière au printemps, qu'on guidait de
5: > l'estacade jusqu'à la scierie. Le nom dit exactement ce que fait ce moteur :
6: > il ne lit pas des matrices, il conduit un flux.
7: 
8: Ce document est la **vision** du projet : ce qu'il cherche, pourquoi la
9: représentation qu'il a choisie change la nature des problèmes, et ce que cela
10: ouvre sur chaque axe. Il ne remplace pas les rapports — chaque affirmation
11: mesurée renvoie à celui qui la porte — et il distingue partout ce qui est
12: **mesuré**, ce qui est **raisonné**, et ce qui est **à faire**.
13: 
14: Le projet s'appelait `Qtrinet`, du nom de son origine : un cahier des charges
15: d'inférence ternaire sur un cluster de cartes Stratix V
16: (`Qtrinet-bootstrap.md`). Ce cahier des charges reste l'acte de naissance ; le
17: nom, lui, ne dit plus ce que le projet est devenu. **Drave** le dit.
18: 
19: ---
20: 
21: ## 1. Le cœur : des listes, pas des matrices
22: 
23: Un moteu
… [12746 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vision lue ; lecture du programme de recherche puis des cinq documents audités.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/programme-recherche.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-flux.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/programme-recherche.md</path>
<type>file</type>
<content>
1: # Programme de recherche — vers une intelligence locale
2: 
3: **Objet.** Définir une feuille de route vérifiable vers un système capable
4: d'apprendre et d'évoluer *localement*, sur du matériel qu'une personne possède,
5: sans centre de données. Ce document ne promet pas l'AGI : il définit des paliers
6: **mesurables** et nomme ce qui, aujourd'hui, n'est pas démontré.
7: 
8: **Règle du programme.** Chaque affirmation est mesurée, chaque erreur est
9: consignée. Sept affirmations de ce projet ont déjà été retirées ou corrigées
10: (encodage ×2,17 retiré pour violation de Kraft, divergence fantôme, tokenizer
11: non conforme, roofline corrigée, coût du mode liste inversé, 4 bits sans gain).
12: C'est la méthode, pas un accident : **une trace de recherche qui ne contient pas
13: ses erreurs ne vaut rien.**
14: 
15: ---
16: 
17: ## 1. Thèse
18: 
19: Une intelligence locale doit être **traçable**, **incrémentale**, **bornée en
20: énergie** et **capable d'évoluer sans salle machine**. Les piles denses
21: généralistes optimisent une seule de ces dimensions — le débit
… [11362 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-flux.md</path>
<type>file</type>
<content>
1: # Le format de flux (DRVF) — spécification
2: 
3: Ce format sert **trois choses à la fois**, et c'est délibéré :
4: 
5: 1. la **trace** d'exécution (`--trace-flux`) : ce qui s'est passé, couche par
6:    couche ;
7: 2. le **rejeu** (`--flux-forcer`) : on réinjecte les activations enregistrées et
8:    le calcul repart de là ;
9: 3. le **transport** (phase 3, `--flux-serveur` / `--ppl-reparti`) : ce qu'un nœud
10:    distant reçoit pour continuer le calcul.
11: 
12: Un seul format pour les trois, parce que ce sont les mêmes octets : une liste
13: d'activation est une liste d'activation, qu'elle aille sur le disque ou sur le
14: réseau.
15: 
16: ## Fichier (trace, `.bin`)
17: 
18: ```
19: en-tête   "DRVF"                    4 octets
20:           version      u16          = 2 (défaut) ou 3 (`DRAVE_TRACE_BLOCS=1`)
21:           n_couches    u32
22:           cachés       u32
23: liste     couche       u16          < 1000 : entrée d'attention
24:                                     >= 1000 : entrée de FFN (couche - 1000)
25:           jeton        u32          COMPTEUR GLOBAL
… [10223 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des quatre autres documents audités.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-clusters.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/convertisseur.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-clusters.md</path>
<type>file</type>
<content>
1: # Format — le modèle éclaté en clusters (un fichier par cluster)
2: 
3: **En une ligne** : un GGUF est converti en `commun.gguf` + `cluster-XX.gguf`, un
4: fichier **GGUF autonome par cluster d'experts**, avec un manifeste qui porte la
5: correspondance ; un nœud n'ouvre que ce qu'il sert — mesuré **3,20 Go au lieu de
6: 18,56** et **625 ms au lieu de 3,9 s** sur Qwen3-30B-A3B.
7: 
8: Outil : [`tools/convertir_clusters.py`](../tools/convertir_clusters.py).
9: 
10: ## Le problème
11: 
12: Un MoE publié en GGUF met **tous** les experts d'une couche dans un seul tenseur :
13: 
14: ```
15: blk.0.ffn_gate_exps.weight   [128, 768, 2048]   Q4_K
16: blk.0.ffn_up_exps.weight     [128, 768, 2048]   Q4_K
17: blk.0.ffn_down_exps.weight   [128, 2048, 768]   Q6_K
18: ```
19: 
20: Un nœud qui n'héberge que 16 experts sur 128 lit donc 18 Go pour en utiliser un
21: huitième — et notre mode d'opération lit les poids **en flux à chaque jeton** :
22: c'est le chemin le plus chaud du moteur.
23: 
24: ## Ce que produit le convertisseur
25: 
26: ```
27: modele/
28:   commun.gguf          em
… [8858 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/convertisseur.md</path>
<type>file</type>
<content>
1: # Convertisseur et chargement : ce que la mesure dit de faire
2: 
3: > Directive : « un convertisseur de modèle haute fidélité afin d'avoir un
4: > chargement optimal : abolition des zéros, identification des clusters et MoE,
5: > tuning CPU/hyperthread/core pour les calques sur CPU et similaires pour les
6: > calques sur GPU avec optimisation des calques en fonction des routes PCIe ».
7: >
8: > Ce document confronte chacun de ces quatre points à la mesure, puis propose le
9: > format et l'ordre de marche.
10: 
11: ## 1. Ce que « chargement optimal » veut dire, mesuré
12: 
13: Le chargement d'un modèle passait par une **copie complète** : déquantifier les
14: f32, puis reconstruire les poids dans notre disposition. Mesuré sur le 0,5B
15: Q4_0 :
16: 
17: | | avant (copie) | après (emprunt) |
18: |---|---|---|
19: | chargement des 24 couches | 2,70 s | **0,845 s** |
20: | mémoire crête (fichier 353 Mo) | ~700 Mo | **413 Mo** |
21: | perplexité (510 jetons) | 21,0116 | **21,0110** |
22: 
23: Le gain de perplexité n'est pas un bruit : l'import réencodait l'échelle de bloc
2
… [15942 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des deux derniers documents : colab-réparti et contexte-long.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/colab-reparti.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/colab-reparti.md</path>
<type>file</type>
<content>
1: # Répétition Colab — la phase 3.4, pas à pas
2: 
3: Objectif : deux machines qui se passent des **listes d'activation**, l'une sur le
4: runtime Colab, l'autre en local, et **les mêmes logits** qu'en local.
5: 
6: Ce document est la recette ; l'état du protocole et les chiffres qui la
7: dimensionnent sont dans `docs/format-flux.md` et
8: `reports/rapport-transport-liste.md`.
9: 
10: ## Mise en place, concrètement
11: 
12: `tools/preparer_colab.sh` produit le dépôt en **un fichier** (`drave.bundle`, 4,5 Mo
13: avec tout l'historique) et affiche l'empreinte SHA-256 du modèle — les deux nœuds
14: doivent charger le même GGUF, la dimension ne voyage pas. `colab/README.md` donne
15: la marche à suivre (tunnel, téléversements) et `colab/Drave-reparti.ipynb` est le
16: notebook prêt à ouvrir, avec la vérification d'empreinte et la lecture du résultat.
17: 
18: ## Ce qui est déjà vérifié, et ce qui ne l'est pas
19: 
20: | point | état |
21: |---|---|
22: | fidélité du découpage | ✅ écart **0,00e0** entre local et deux nœuds (40 et 200 jetons) |
23: | version du protocole | ✅ d
… [5997 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/ && ls reports/ | head -80", "description": "List tools and reports"}`

  ```
aiguille.py
analyse_empreinte.py
analyse_experts_statique.py
analyse_flux.py
archive_sessions.py
clusters_moe.py
colab_cote_local.sh
compare_logits.py
convertir_clusters.py
diff_flux.py
extraire_tables_ggml.c
extraire_tables_ggml.sh
flux_codec.py
harmony_canonique.py
inventaire_modeles_lourds.sh
make_patch.py
manifeste_modeles_lourds.json
mesurer_lecture_experts.py
mla_synthetique.py
pair_factice.py
portes_formats.sh
portes.sh
preparer_colab.sh
profil_flux.py
proxy_latence.py
__pycache__
ref_ggml_bloc.c
ref_logits
ref_logits.cpp
ref_logits.md
session_report.py
sprint.sh
telecharger_modeles.py
trace_compacite.py
verifier_formats.py
verifier_table_types.sh
vision_mtmd.py
vision_ref.py
aiguille-30b.md
aiguille-gpt-oss.md
bilan-multi-materiel.md
rapport-8bits.md
rapport-aiguille.md
rapport-aiguille-topk.md
rapport-analyse-flux.md
rapport-architecture-memoire.md
rapport-attention-creuse.md
rapport-attribution-kv.md
rapport-campagne-parcimonie.md
rapport-capteur-hebbien.md
rapport-coherence-docs-2.md
rapport-coherence-docs.md
rapport-compacite-trace.md
rapport-cpu-aer.md
rapport-croisement-push-pull.md
rapport-decoupage-moe.md
rapport-drapeaux-ignores.md
rapport-empreinte-memoire.md
rapp
… [920 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de contexte-long.md (580 lignes).

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md</path>
<type>file</type>
<content>
1: # Contexte long : ce que 1 M veut dire, et par où ça casse
2: 
3: > Tous les chiffres de budget viennent de `drave-core <modele> --plan --ctx N`,
4: > qui les calcule depuis les métadonnées du GGUF. Les bandes passantes sont
5: > celles mesurées sur cette machine (deux Quadro RTX 5000 16 Go, 125 Go de RAM,
6: > NVMe à ~3,5 Go/s, 20 cœurs Haswell AVX2).
7: 
8: ## 1. Ce que les modèles déclarent
9: 
10: | modèle | contexte entraîné | initial | facteur YaRN | 1 M, c'est… |
11: |---|---|---|---|---|
12: | gpt-oss-120b | 131 072 | 4 096 | ×32 | ×8 au-delà du déclaré → extrapolation |
13: | Qwen3-30B-A3B | 262 144 | — | — | ×4 au-delà du déclaré |
14: | Qwen2.5-VL-7B | 32 768 | — | — | ×32 au-delà |
15: 
16: Autrement dit : **le moteur peut être prêt pour 1 M, aucun modèle d'ici ne l'est.**
17: Le travail d'ingénierie (mémoire, débit, rotation) est faisable et mesurable ; la
18: qualité à 1 M, elle, se mesurerait par récupération (« aiguille dans la botte de
19: foin »), pas par perplexité, et n'a de sens qu'avec un modèle entraîné pour.
20: 
21: ## 2. Le budget, mesuré
22: 

… [32889 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des chiffres dans les rapports et le code (portes, tests, protocole, formats).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 15,6017 / 15.6017 ===\" && grep -rn \"15,6017\\|15\\.6017\" --include=*.md --include=*.rs --include=*.sh . | head -20; echo \"=== 15,1757 ===\"; grep -rn \"15,1757\\|15\\.1757\" --include=*.md . | head -20; echo \"=== 48 t … [258 caractères tronqués]`

  ```
=== 15,6017 / 15.6017 ===
./reports/rapport-routage-experts.md:66:| gpt-oss-120b ctx 256 | 15,1757 | **15,6017** | **changée** — voir ci-dessous |
./reports/rapport-routage-experts.md:126:| drave, YaRN **à retardement** (le défaut) | **15,6017** |
./reports/rapport-routage-experts.md:162:  elle doit confirmer ou contredire 15,6017. C'est la seule mesure qui tranche
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:3577:| gpt-oss ctx 256 | **15,6017** (15,1757 avant — changement justifié par le code de llama.cpp) |
./REPRISE.md:1000:| gpt-oss-120b MXFP4 ctx 256 | **15,6017** | **changée** (15,1757 avant) — voir ci-dessous |
./REPRISE.md:1104:   lot ; quatre tests unitaires les encodent. Porte gpt-oss : 15,1757 → 15,6017,
./drave-core/src/model.rs:5538:    /// 15,1757 à 15,6017 — l'ancien code le laissait dans le softmax.
./README.md:374:| **gpt-oss-120b** (MoE, MXFP4) | MXFP4 | **15,6017** (ctx 256) | blocs lus | 60 Go |
=== 15,1757 ===
./reports/rapport-coherence-docs.md:116:| 55 | `README.md:344` | gpt-oss-120b : perplexité « **—** » | 15,1757 (REPRISE §2) et 20,8361 à 63 jetons : le chiffre existe | MANQUANT |
./reports/rapport-session-2026-09-30.md:92:Qwen ctx 2
… [5368 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== portes_formats ===\"; grep -rn \"portes_formats\" --include=*.md --include=*.sh . | head -20; echo \"=== verifier_table_types ===\"; grep -rn \"verifier_table_types\" --include=*.md --include=*.sh . | head -20; echo \"===  … [247 caractères tronqués]`

  ```
=== portes_formats ===
./reports/rapport-mla-experts.md:72:(`tools/portes_formats.sh`) — et parallélisée par lignes de sortie. Elle ne
./tools/portes.sh:64:    if command -v gcc >/dev/null && [ -f tools/portes_formats.sh ]; then
./tools/portes.sh:65:        r=$(timeout 1800 bash tools/portes_formats.sh 2>&1 | tail -1)
./tools/portes_formats.sh:4:#   tools/portes_formats.sh [type ...]
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:3832:| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/portes_formats.sh` | 1 | 0 |
./REPRISE.md:1002:| `tools/portes_formats.sh` | **17 formats × 2 blocs** | tous exacts contre libggml |
./REPRISE.md:1089:tools/portes_formats.sh          # 17 formats × 2 blocs, contre libggml
./README.md:364:tools/portes_formats.sh                   # 17 formats × 2 blocs, contre libggml
=== verifier_table_types ===
./tools/verifier_table_types.sh:13:#   tools/verifier_table_types.sh [chemin de llama.cpp]
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:3819:| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_table_types.sh` | 1 | 0 |
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:4300:- La tab
… [1401 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche ciblée des chiffres périmés dans les cinq documents audités.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs && for f in format-flux.md format-clusters.md convertisseur.md colab-reparti.md contexte-long.md; do echo \"=== $f ===\"; grep -n \"15,1757\\|15,6017\\|19,3885\\|799,8557\\|test\\|protocole v\\|version 4\\|version 5\\|v4\\|v5\\|lla … [85 caractères tronqués]`

  ```
=== format-flux.md ===
48:| rejeu (`--flux-forcer`) | 19,3885 | **19,3885 — identique** |
59:| rejeu `--flux-forcer` | 19,3885 | **19,4029 (+0,074 %)** |
84:## Transport (phase 3, TCP) — protocole v5
158:de **39 octets** (protocole v3, avant les top-k) : ajouter 40 octets par flux pour
176:| un rejeu redonne le même résultat | `--flux-forcer` : perplexité **19,3885** avec et sans rejeu (chemin par jeton), **17,4294** (chemin par lots) |
=== format-clusters.md ===
168:  | 8 | **799,8557** | 6,28 Go |
173:  799,8557 pour 4,60 Go chacun — moins que les 6,28 Go d'un nœud complet.
=== convertisseur.md ===
33:test unitaire).
76:   égal — c'est l'effet de l'accumulateur. À retester sur les grosses couches
146:La fidélité n'est pas une intention, c'est un test. Trois niveaux, du plus fort
193:| Qwen2.5-0.5B | Q8_0 | 19,3885 | 32 | **0,81 s** | **0,57 Go** |
206:`llama.cpp` est installé sur la machine (`llama-cli`, `llama-perplexity`,
211:   ce qui a rendu le bug incontestable.
270:Le **tokenizer o200k** est vérifié : identique à celui de llama.cpp sur 7 cas
315:Chaque hypothèse se teste maintenant en **une** exécution, et la trace de
=== colab-reparti.md ===
26:| au-delà de localhost | ✅ t
… [2136 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mla-experts.md"}`

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

### 🤖 Assistant

⏵ Vérification des affirmations vision (patchs/projecteur) et des rapports de cohérence existants.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 5,4e-7 / projecteur ===\"; grep -rn \"5,4e-7\\|1,7e-6\" --include=*.md . | head -20; echo \"=== vision report ===\"; ls reports/ | grep -i \"vision\\|mmproj\\|patch\"; echo \"=== mmproj ===\"; grep -rln \"mmproj\\|vision_m … [103 caractères tronqués]`

  ```
=== 5,4e-7 / projecteur ===
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:18800:⏵ Embedding de patchs validé : 5,4e-7 contre la référence numpy
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:18806:2ca9e0d Vision : l'embedding de patchs est fait et validé (5,4e-7 contre numpy)
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:18817:**écart max relatif 5,4e-7**, le bruit de virgule flottante du moteur.
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:18831:| 5 | MLA ✅ validé (5,2e-7) · vision ⏳ embedding de patchs validé (5,4e-7), tour à finir | en cours |
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:18982:c165fcf Vision : le projecteur est validé aussi (1,7e-6) — les deux extrémités du chemin image tiennent
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:19035:c165fcf Vision : le projecteur est validé aussi (1,7e-6) — les deux extrémités du chemin image tiennent
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:19036:2ca9e0d Vision : l'embedding de patchs est fait et validé (5,4e-7 contre numpy)
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.
… [3031 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,60p' reports/rapport-coherence-docs-2.md && echo \"...\" && grep -n \"docs/format\\|docs/convertisseur\\|docs/colab\\|docs/contexte\\|docs/format-clusters\" reports/rapport-coherence-docs-2.md | head -40", "description": "R … [28 caractères tronqués]`

  ```
# Cohérence des documents avec le code — second passage

**En une ligne** : **66 affirmations** revérifiées contre le code et les rapports
**après** les changements du 30/09 ; **27 tiennent**, **17 sont périmées**, **14 se
contredisent** et **8 manquent** — les deux plus graves sont le **chiffre vedette du
cache KV** (« 75 % / 50 % » contre « 64 % / 28 % » dans le rapport qui l'a mesuré) et
la règle **R4** dont la moitié (`n == 0` refusé) n'est **pas** dans le code alors que
le plan affirme le contraire.

## Révision auditée, méthode, réserves

| | |
|---|---|
| Commit de référence | `a383cd7` (2026-09-30 15:11) |
| `drave-core/src/main.rs` | sha256 `bc53a66ad757faa6…` · 3 508 lignes |
| `drave-core/src/model.rs` | sha256 `61582adb8ded0f25…` · 3 928 lignes |
| Total `.rs` du moteur | **11 901 lignes** (7 fichiers) |
| Arbre au moment d'écrire | `journal/` modifié, `docs/plan-mode4-lot-listes.md` non suivi ; **73 commits** dans la journée |

Trois réserves, parce qu'elles changent la portée des constats :

1. **L'arbre a bougé pendant l'audit.** Deux documents sont apparus en cours de
   route : `docs/plan-mode4-lot-listes.md` (15:12, non commité) et
   `docs/plan-gpu-topk.md` (15:1
… [12013 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des cadrages « dense/optimisation » et vérification du code (version de protocole, modes).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== code: VERSION_FLUX / modes / TAILLE_TETE ===\"; grep -rn \"VERSION_FLUX\\|TAILLE_TETE *:\\|MODE_LOT\\|MODE_LISTES\\|MODE_BLOCS\\|MODE_DENSE\" drave-core/src/main.rs | head -30", "description": "Check protocol version const … [14 caractères tronqués]`

  ```
=== code: VERSION_FLUX / modes / TAILLE_TETE ===
1862:const VERSION_FLUX: u8 = 5;
1864:const MODE_DENSE: u8 = 0;
1873:const MODE_BLOCS: u8 = 2;
1879:const MODE_LOT: u8 = 3;
1886:const MODE_LOT_LISTES: u8 = 4;
1897:const TAILLE_TETE: usize = 4 + 1 + 1 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 1
2050:    t.push(VERSION_FLUX);
2133:    let (n, echelle, corps): (usize, f32, Vec<u8>) = if mode == MODE_BLOCS {
2180:    let tete = tete_flux(MODE_LOT, debut, fin, pos0, t, 0.0, Some(mdl));
2216:    let tete = tete_flux(MODE_LOT_LISTES, debut, fin, pos0, t, 0.0, Some(mdl));
2235:    if version != VERSION_FLUX {
2238:            format!("flux en version {version}, cette build parle la {VERSION_FLUX} \
2265:    if n == 0 && matches!(mode, MODE_DENSE | MODE_LOT | MODE_LOT_LISTES) {
2268:                    if mode == MODE_DENSE { "canal" } else { "état" })));
2271:        MODE_DENSE | MODE_LISTE | MODE_BLOCS | MODE_LOT | MODE_LOT_LISTES => {}
2274:{MODE_LOT_LISTES}, protocole v{VERSION_FLUX})"))),
2277:        MODE_LOT_LISTES => {
2357:        MODE_LOT => {
2370:        MODE_BLOCS => {
2404:        MODE_DENSE => ChargeFlux::Dense((0..n).map(|k| f32::from_le_bytes(
2466:                if f.mode == MODE
… [691 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs && echo \"=== dense ===\"; grep -n \"dense\" format-flux.md format-clusters.md convertisseur.md colab-reparti.md contexte-long.md; echo; echo \"=== optimisation/optimiser ===\"; grep -n \"optimis\\|accélé\\|variante\\|rangement\" f … [139 caractères tronqués]`

  ```
=== dense ===
format-flux.md:35:trace **dense** : **6,02 octets par neurone actif** en v1, **3,01** en v2 ; sur une
format-flux.md:47:| trace dense, 512 jetons | 132 396 736 o | **66 370 408 o (−49,87 %)** |
format-flux.md:58:| trace dense, 512 jetons | 66 370 408 o | **45 079 930 o (−32,1 %)** |
format-flux.md:90:          mode         u8           0 = f32 dense · 1 = liste quantifiée
format-flux.md:91:                                    2 = listes à échelle par bloc · 3 = LOT dense
format-flux.md:128:f32 dense (3,5 ko par jeton) ; le lot en LISTES est le mode 4 (1,5 ko par jeton,
format-flux.md:133:vecteur dense, c'est le sujet même de la phase 3 — « des listes, pas des
format-flux.md:152:Le mode dense coûte **3 663 octets par flux** (79 d'en-tête + 896 × 4) pour
format-clusters.md:93:# conversion : un cluster = 16 experts ; --mode couches pour un modèle dense
format-clusters.md:98:`--mode couches` découpe un modèle **dense** en groupes de couches (un fichier par
convertisseur.md:27:➡️ **Conséquence de conception : dans le chemin dense, le convertisseur est
convertisseur.md:50:| zéros | dense 4 bits | masque + valeurs | gain |
convertisseur.md:59:➡️ **Le seuil est à 25 %, et MXFP
… [1424 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des mesures de format-clusters.md contre les rapports.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 3,20 / 625 ms ===\"; grep -rn \"3,20 Go\\|625 ms\\|18,56\" reports/*.md | head -20; echo; echo \"=== 15,2789 ===\"; grep -rn \"15,2789\\|15\\.2789\" reports/*.md REPRISE.md | head -10; echo; echo \"=== 3,08 / 5,32 ===\"; g … [194 caractères tronqués]`

  ```
=== 3,20 / 625 ms ===
reports/rapport-decoupage-moe.md:105:Qwen3-30B-A3B : **3,20 Go chargés au lieu de 18,56** pour un nœud qui sert un
reports/rapport-decoupage-moe.md:106:cluster, 625 ms au lieu de 3,9 s, 1 587 tenseurs vérifiés — le format est décrit
reports/rapport-lecteur-multifichiers.md:18:d'origine (18,56 Go, un fichier, sur le disque mécanique) contre le même modèle

=== 15,2789 ===
reports/rapport-lecteur-multifichiers.md:23:| modèle d'origine | **15,2789** | 12,2 s |
reports/rapport-lecteur-multifichiers.md:24:| modèle en clusters | **15,2789** | 11,6 s |
reports/rapport-lecteur-multifichiers.md:67:| modèle en clusters | 15,2789 | **15,2789** |
reports/rapport-lecteur-multifichiers.md:234:                                          drave <dossier> ──► 15,2789
reports/rapport-lecteur-multifichiers.md:242:| exécution du modèle converti | **15,2789** — exactement l'original |
reports/rapport-lecteur-multifichiers.md:264:  contre 15,2789 par jeton — l'écart connu entre les deux ordres de sommation.
REPRISE.md:716:    --ppl /tmp/ids_qwen.txt --ctx 64 --limit 64 --dense --threads 12 --lot 1   # 15,2789
REPRISE.md:718:    --ppl /tmp/ids_qwen.txt --ctx 64 --limit 64 --dense --thr
… [1015 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 41 types / table ggml ===\"; grep -rn \"absents du moteur\\|types confondus\\|41 \" reports/*.md REPRISE.md | head -20; echo; echo \"=== QTNT / calque ===\"; grep -rn \"QTNT\" --include=*.md . | grep -v journal | head -20; … [193 caractères tronqués]`

  ```
=== 41 types / table ggml ===
reports/bilan-multi-materiel.md:54:| CPU | 1 thread 0,41 G → 8 : 2,75 → 16 : 4,45 → **32 : 5,3** G évts/s ; effondrement à 39+ |
reports/bilan-multi-materiel.md:95:| « 27 PE suffisent, 3 % de la logique » | **Corrigée** — en comptant le lecteur : 51 voies, 41 % de la logique et 41 % de la M20K |
reports/bilan-multi-materiel.md:109:Une carte = 4,83 G évts/s = **un CPU 20 cœurs**, pour 41 % de la logique et 41 %
reports/rapport-architecture-memoire.md:240:| **lecture NVMe** (8 lecteurs) | 22,41 | 21,45 | 22,57 Go/s |
reports/rapport-coherence-docs-2.md:100:| 41 | `docs/contexte-long.md:101-102` (E2) | KV int8 « **fait** (échelle par vecteur) », « mesuré : **+7,1 %** (llama.cpp : +3,1 %) » | le même document §4.bis (`:143-145`) dit « corrigé, échelles par bloc de 32 : **+1,5 %** à 512, **+3,0 %** à 8 192 » ; la ligne E2 n'a pas suivi | PÉRIMÉ |
reports/rapport-coherence-docs.md:97:| 41 | `docs/roadmap.md:107` | trace 512 jetons = « **12 288 listes** · 132 Mo · 6 octets par neurone actif » | 24 576 listes pour 512 jetons × 24 couches × 2 points ; 12 288 = la valeur pour **256 jetons** | PÉRIMÉ |
reports/rapport-compacite-trace.md:137:| zstd niv. 3 sur l'ac
… [2233 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification dans le code : seuil YaRN, drapeaux CLI, chargement du modèle, état vision.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== seuil yarn ===\"; grep -rn \"SEUIL\\|seuil_bascule\\|4 \\*\\|125\\|yarn_seuil\\|bascul\" drave-core/src/*.rs | grep -i \"yarn\\|seuil\\|bascul\" | head -30; echo; echo \"=== act-thresh / seuil-act ===\"; grep -rn \"act-thr … [133 caractères tronqués]`

  ```
=== seuil yarn ===
drave-core/src/materiel.rs:473:        // Un contexte énorme doit faire basculer le KV en 8 bits.
drave-core/src/model.rs:1006:        const SEUIL_GPU: usize = 8 << 20;
drave-core/src/model.rs:1010:                   && n_out * d8.nb_ligne * 34 >= SEUIL_GPU => {
drave-core/src/model.rs:1518:    /// Seuil de bascule push/pull, en fraction de sources actives. Mesuré : les
drave-core/src/model.rs:1519:    /// deux architectures se croisent à 10 % de densité ; on bascule un peu
drave-core/src/model.rs:2187:                // Seuil de bascule : mesuré au protocole apparié (`--depuis`,
drave-core/src/model.rs:2894:    /// Seuil d'activation du profilage : une activation vaut `SEUIL_PROFIL` du
drave-core/src/model.rs:2900:    const SEUIL_PROFIL: f32 = 0.05;
drave-core/src/model.rs:2909:        let seuil = Self::SEUIL_PROFIL * mx;
drave-core/src/model.rs:2933:                              100.0 * Self::SEUIL_PROFIL, n_tok, largeur, n));
drave-core/src/model.rs:4314:                // mesure pour un A/B qui ne bascule que par la variable.
drave-core/src/model.rs:4338:                        const SEUIL_NOYAU4: usize = 131_072;
drave-core/src/model.rs:4339:                
… [1494 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"vision\\|Vision\\|mmproj\\|patchs\" README.md | head -30; echo \"=== REPRISE vision ===\"; grep -n \"vision\\|Vision\" REPRISE.md | head -30", "description": "Check README/REPRISE vision status"}`

  ```
5:matrices, il pousse des faits valués vers leurs destinations. La vision complète
6:est dans [`docs/vision.md`](docs/vision.md).
=== REPRISE vision ===
163:| 8 | suite du plan 1 M | **fait pour E4/E5** | **E4 KV déporté en VRAM** : noyaux `attn_kv_*` (tuiles de 32 clés, softmax en ligne, recombinaison + puits), miroir du cache **paginé** (capacité doublée à la demande : 0,05 Go de VRAM à ctx 1 M après 512 jetons) et `DRAVE_GPU_KV=1` — à 1 M de clés l'attention passe de 968 ms à **13,2 ms** par couche (int4, ×73) et, dans le moteur à 4 096 de contexte, de **22,2 à 3,3 ms/jeton** (−38 % de bout en bout) à perplexité identique (12,2177 → 12,2175). **E5 attention creuse** : mesurée (`--attn-topk 256` : 234,9 contre 298,6). MLA et vision restent non testables (aucun modèle MLA ici ; le projecteur `mmproj` est là mais rien ne lit les patchs) |
220:4. ~~**MLA et vision.**~~ **TOUS DEUX FAITS.** MLA : modèle synthétique + référence
221:   numpy, écart **5,2e-7**. Vision : chaîne COMPLÈTE et démontrée de bout en bout
229:   testées). Tout est dans `docs/plan-mla-vision.md`.
364:`--banc-vision` (ne reçoit aucune `Options`), `--bits` du noyau GPU, et la
  ```

### 🤖 Assistant

⏵ Recherche du seuil YaRN dans le code et du croisement push/pull dans les cinq docs.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== YARN code ===\"; grep -rn \"yarn\\|YARN\" drave-core/src/*.rs | head -40; echo; echo \"=== seuil bascule yarn ===\"; grep -rn \"bascul\\|seuil\" drave-core/src/model.rs | sed -n '1,20p'", "description": "Find YaRN threshol … [11 caractères tronqués]`

  ```
=== YARN code ===
drave-core/src/main.rs:24:    "TRACE_EXPERTS", "VISION_TEXTE", "YARN", "YARN_MSCALE", "YARN_NON",
drave-core/src/main.rs:25:    "YARN_RAMPE",
drave-core/src/main.rs:565:    sans_yarn: bool,
drave-core/src/main.rs:681:            "--sans-yarn" => { o.sans_yarn = true; 1 }
drave-core/src/main.rs:754:        hebb_layer, hebb_q, hebb_out, sans_yarn, lot, ffn_gain,
drave-core/src/main.rs:832:    if sans_yarn { mdl.cfg_yarn_off(); }
drave-core/src/main.rs:1683:        hash_layers: r.hash_layers, n_rot: 0, yarn: None,
drave-core/src/main.rs:4252:        harmony, harmony_contexte, sans_yarn, ..
drave-core/src/main.rs:4341:    if sans_yarn { mdl.cfg_yarn_off(); }
drave-core/src/model.rs:424:    pub yarn: Option<(f32, f32, f32, f32, bool)>,
drave-core/src/model.rs:2144:            //   `DRAVE_YARN=1`      YaRN à toutes les positions, comme HF, llama.cpp
drave-core/src/model.rs:2146:            //   `DRAVE_YARN_NON=1`  jamais de YaRN (ce que fait `--sans-yarn`) ;
drave-core/src/model.rs:2163:            yarn: {
drave-core/src/model.rs:2165:                    Some("yarn") => Some((
drave-core/src/model.rs:2167:                        g.cfg("rope.scaling.yarn_beta_fast").and_
… [3885 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs && echo \"=== croisement 22/10 % ===\"; grep -n \"22 %\\|22%\\|10 %\\|croisement\" format-flux.md format-clusters.md convertisseur.md colab-reparti.md contexte-long.md", "description": "Check density crossing figures in docs"}`

  ```
=== croisement 22/10 % ===
convertisseur.md:225:dessous du croisement mesuré à 22 % de densité : le régime où l'architecture
contexte-long.md:292:à 1 M à ≈ 5,7 s. Le point de croisement est vers **4 000 clés** (en dessous, les
contexte-long.md:514:   croisement mesuré : c'est une décision d'ingénierie prudente (au-delà de la
  ```

### 🤖 Assistant

⏵ Lecture des commentaires du code sur le seuil YaRN et le croisement push/pull.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "offset": 2140, "limit": 65}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "offset": 1510, "limit": 20}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
2140:             },
2141:             // ------------------------------------------------ rotation (RoPE)
2142:             // Trois régimes, choisis **par mesure** :
2143:             //
2144:             //   `DRAVE_YARN=1`      YaRN à toutes les positions, comme HF, llama.cpp
2145:             //                    et l'implémentation officielle d'OpenAI ;
2146:             //   `DRAVE_YARN_NON=1`  jamais de YaRN (ce que fait `--sans-yarn`) ;
2147:             //   défaut           **YaRN à retardement** : RoPE simple tant que le
2148:             //                    contexte demandé tient dans la longueur initiale
2149:             //                    du modèle (4 096 pour gpt-oss), YaRN au-delà.
2150:             //
2151:             // Mesuré sur gpt-oss à contexte 512 : YaRN ×32 coûte un facteur 9
2152:             // (174,34 contre 18,58). Mais l'étirement est indispensable pour
2153:             // dépasser les 4 096 positions vues à l'entraînement initial : le
2154:             // retardement garde les deux propriétés.
2155:             //
2156:           
… [3529 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
1510:     /// Période du motif fenêtre/plein : la couche `l` est fenêtrée si
1511:     /// `l % motif < motif - 1`. gpt-oss déclare 128 de fenêtre sur **une couche
1512:     /// sur deux** (`layer_types` alterne sliding_attention / full_attention,
1513:     /// et llama.cpp pose `set_swa_pattern(2)`) : appliquer la fenêtre aux
1514:     /// 36 couches supprimait toute information au-delà de 128 jetons dans la
1515:     /// moitié du réseau. 0 ou 1 = toutes les couches fenêtrées.
1516:     pub swa_pattern: usize,
1517:     pub attn_sinks: usize,
1518:     /// Seuil de bascule push/pull, en fraction de sources actives. Mesuré : les
1519:     /// deux architectures se croisent à 10 % de densité ; on bascule un peu
1520:     /// au-dessus pour absorber la marge d'erreur.
1521:     pub seuil_push: f32,
1522:     /// Token d'arrêt (EOS / <|im_end|>) : la génération s'interrompt dessus.
1523:     pub stop_id: Option<u32>,
1524:     /// Second jeton d'arrêt : gpt-oss termine par `<|return|>` **ou**
1525:     /// `<|end|>` selon le canal.
1526:     pub stop_id2: Option<u32>,
1527
… [247 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de REPRISE.md (état MLA/vision) et du rapport de croisement push/pull.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md", "limit": 80, "offset": 155}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md</path>
<type>file</type>
<content>
155: |---|---|---|---|
156: | 1 | protocole de perplexité longue | **fait** | `--depuis N` note les mêmes jetons à contexte variable ; `--depuis 256 --ctx 256` redonne exactement la fenêtre 2 historique (21,565) |
157: | 2 | seuil de rotation YaRN | **fait, seuil à 4 × la longueur déclarée** | comparaison appariée (mêmes 512 jetons) : contexte 128→1536, RoPE simple 39,52/49,79/49,93/298,56 contre interpolation 42,13/82,02/82,15/578,86 → le simple gagne partout. **Au-delà du seuil** (5 120 jetons, corpus de 17 k maintenant disponible) : simple **9,6986** contre interpolation seule **1 269,1777** → le seuil de 4 096 était **trop bas** ; le moteur ne bascule plus qu'à 1,25 × la longueur déclarée. Au-delà (16 k, 131 k) : non mesuré, une passe à 16 k coûte une heure |
158: | 3 | KV int8 puis int4 | **fait, jusqu'à 8 192** | **échelles par bloc de 32** : int8 +**1,5 %** à 512 (était +7,1 %), **+3,0 % à 8 192** (llama.cpp +0,8 %) ; int4 **+364 % à 8 192** contre +494 % pour llama.cpp — meilleur que la référence, et 1 M tient en int4 (9,7 Go). Prix caché : la passe coûte 864 s (f32) / 1 144 
… [9113 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,40p' reports/rapport-croisement-push-pull.md", "description": "Read push/pull crossing report header"}`

  ```
# Croisement push / pull — quand l'architecture événementielle est-elle justifiée ?

Deux façons d'exécuter le même modèle quantifié :

- **push** (notre architecture) : pour chaque source active, on *disperse* ses
  poids dans un accumulateur (`acc[dest] += x·w`). Le flux est indexé par
  source, un événement = écart + valeur, 2 octets.
- **pull** (le noyau dense ordinaire) : pour chaque sortie, on *lit* sa ligne de
  poids et on fait un produit scalaire. 1 octet par poids, aucune dispersion.

Elles donnent **exactement le même résultat** — vérifié : perplexité 19,2647 au
chiffre près sur 510 jetons, tokens identiques, en écrivant les deux chemins avec
le même ordre d'opérations (les sommes entières sont exactes des deux côtés).

> ⚠️ **Corrigé le 27/09** : le tableau de croisement de la section 1 mesurait
> « push » contre « dense » alors que le drapeau `--dense`, placé en dernier
> argument, n'était jamais lu (`while i + 1 < args.len()`), et le mode dense
> sommait des tranches périmées. Les chiffres ci-dessous sont ceux du banc
> instrumenté, à arithmétique identique. Voir
> `rapport-mur-memoire-4bits.md`.

---

## 1. Le croisement

Temps CPU pour 24 tokens, meilleur de 2, mesu
… [562 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de l'état actuel du test « aiguille » (le doc le dit arrêté).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,45p' reports/rapport-aiguille.md; echo \"=== aiguille-topk ===\"; sed -n '1,25p' reports/rapport-aiguille-topk.md", "description": "Read needle test reports"}`

  ```
# L'aiguille dans la botte de foin : où en est la mesure de qualité

La perplexité ne dit **pas** si un modèle retrouve une information. Ce rapport
raconte la remise en route de la seule mesure qui le dise, et ce qu'elle a
immédiatement appris.

## 1. Ce qui n'allait pas dans la v1

La v1 (`tools/aiguille.py`, conservée dans l'historique) plantait un code dans un
contexte dont le remplissage était **la même phrase recopiée** jusqu'à la
longueur voulue, posait la question, et n'accordait que **8 jetons** de réponse.
Résultat : 6 sondes sur 6 échouaient sur Qwen2.5-0.5B, et 9,6 minutes pour un
échec sur Qwen3-30B-A3B. Le test a été arrêté à l'époque, faute de budget.

Trois défauts, tous de protocole :

1. **remplissage répété** : un modèle peut répondre en devinant la structure du
   texte, et la sonde ne teste plus la mémoire mais la régularité ;
2. **réponse trop courte** : un code peut sortir au deuxième ou troisième jeton
   d'une réponse ; s'arrêter à 8 jetons fait échouer des sondes que le modèle
   savait résoudre ;
3. **préremplissage séquentiel** : le moteur ne batchait que la perplexité, donc
   chaque sonde payait son contexte jeton par jeton.

## 2. La v2

`tools/aiguill
… [2343 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"12/12\\|12 sondes\\|aiguille v2\" reports/*.md REPRISE.md | head -15", "description": "Confirm 12/12 needle result"}`

  ```
reports/aiguille-30b.md:1:# aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf
reports/aiguille-gpt-oss.md:1:# aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf
reports/rapport-aiguille.md:74:**12 sondes sur 12** trouvées, à toutes les profondeurs — y compris à 90 % de la
REPRISE.md:190:| aiguille v2 (12 sondes) | **12/12 trouvées** : 1,5B 512/2048, 30B 2048, gpt-oss 4096, profondeurs 0,1/0,5/0,9 |
REPRISE.md:199:l'aiguille v2, le dépaquetage vectorisé du noyau d'attention, les experts MXFP4
REPRISE.md:564:ou qu'on est à très long contexte. Et l'aiguille v2 retrouve **9/9** sondes dans
  ```

### 🤖 Assistant

⏵ Recherche de la finalité d'analyse (observer/adapter) dans les cinq docs.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs && for f in format-flux.md format-clusters.md convertisseur.md colab-reparti.md contexte-long.md; do echo \"=== $f ===\"; grep -n \"analys\\|observer\\|comportement\\|adapter l'architecture\\|diagnostic\\|débog\\|comprendre\" $f; d … [53 caractères tronqués]`

  ```
=== format-flux.md ===
=== format-clusters.md ===
=== convertisseur.md ===
316:configuration dit ce qui est actif — c'est ce qui manquait pour déboguer un
=== colab-reparti.md ===
=== contexte-long.md ===
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs && echo \"=== router/machine/nœud clusters ===\"; grep -n \"router\\|routage\\|machine\\|nœud\\|répart\" format-clusters.md | head -30; echo; echo \"=== flux/routage in convertisseur ===\"; grep -n \"flux\\|DRVF\\|trace\\|événement … [106 caractères tronqués]`

  ```
=== router/machine/nœud clusters ===
5:correspondance ; un nœud n'ouvre que ce qu'il sert — mesuré **3,20 Go au lieu de
20:Un nœud qui n'héberge que 16 experts sur 128 lit donc 18 Go pour en utiliser un
63:une trace de routage (`--trace`, produite par `DRAVE_TRACE_EXPERTS`) — et non par
64:index. C'est ce qui fait que `cluster-00.gguf` est le cluster qu'un nœud veut
71:(3,08 nœuds au lieu de 5,32 à 8 clusters).
81:Un nœud qui sert le cluster 0 charge **3,20 Go au lieu de 18,56 (5,8× moins)** et
82:**625 ms au lieu de 3,9 s (6,2× plus vite)**. Avec huit nœuds, chacun ne lit que
89:# trace de routage (facultative mais recommandée : elle ordonne les experts)
90:DRAVE_TRACE_EXPERTS=/tmp/routage.txt ./drave-core/target/release/drave <modele.gguf> \
95:    --clusters 8 --trace /tmp/routage.txt --verifier
99:groupe), ce qui sert au même usage : un nœud ne charge que sa tranche. Mesuré sur
157:* **Le nœud partiel** : `DRAVE_CLUSTERS=0,3` ne charge que ces clusters — et un
170:  **Ce qui manque** : la somme des contributions entre nœuds. Le moteur saute
171:  déjà un expert absent, mais rien n'additionne encore ce que deux nœuds calculent
172:  chacun de leur côté. Avec elle, deux nœuds à q
… [895 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des dates de dernière modification des cinq documents et de quelques chiffres restants.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log -1 --format=\"%h %ad %s\" --date=short -- docs/format-flux.md docs/format-clusters.md docs/convertisseur.md docs/colab-reparti.md docs/contexte-long.md; echo \"---- par fichier ----\"; for f in format-flux format-clusters con … [187 caractères tronqués]`

  ```
d8700ae 2026-10-01 Chaîne complète par les outils du dépôt : convertisseur -> clusters -> 15,2789
---- par fichier ----
format-flux: 998d409 2026-09-30 Relecture du mode 4 : dix défauts, dont deux graves — corrigés, et le rapport écrit
format-clusters: d8700ae 2026-10-01 Chaîne complète par les outils du dépôt : convertisseur -> clusters -> 15,2789
convertisseur: fb44671 2026-09-28 gpt-oss : perplexite 42 127 -> 39,8 en cinq etapes mesurees
colab-reparti: e6d6ce9 2026-09-30 Colab : les quatorze champs du contrat d'activation, pas quatre
contexte-long: 1425c79 2026-10-01 Revue du sprint 4 : « trois fenêtres » étaient trois fois la même invite, et la portée du k était surestimée
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 351,7 ===\"; grep -rn \"351,7\" reports/*.md | head -5; echo \"=== 30,68 ===\"; grep -rn \"30,68\\|19,20 Go\" reports/*.md | head -5; echo \"=== 1 587 ===\"; grep -rn \"1 587\" reports/*.md | head -5; echo \"=== git status … [90 caractères tronqués]`

  ```
=== 351,7 ===
reports/rapport-lecteur-multifichiers.md:232:                 (351,7 s, SHA-256 sur chaque tenseur)          │
reports/rapport-lecteur-multifichiers.md:239:| conversion | 435 + 8 × 144 = **1 587 tenseurs**, 18,60 Go, 351,7 s |
=== 30,68 ===
reports/rapport-lecteur-multifichiers.md:182:| lu en entier (`DRAVE_MMAP=0`) | 30,68 s | 19,20 Go |
reports/rapport-lecteur-multifichiers.md:184:Les 19,20 Go sont exactement la taille du modèle : la copie complète. Le mappé
=== 1 587 ===
reports/rapport-decoupage-moe.md:106:cluster, 625 ms au lieu de 3,9 s, 1 587 tenseurs vérifiés — le format est décrit
reports/rapport-lecteur-multifichiers.md:10:Le sprint précédent a produit le format (convertisseur, 1 587 tenseurs vérifiés
reports/rapport-lecteur-multifichiers.md:55:| tenseurs | **1 587** = le compte de la conversion |
reports/rapport-lecteur-multifichiers.md:239:| conversion | 435 + 8 × 144 = **1 587 tenseurs**, 18,60 Go, 351,7 s |
reports/rapport-lecteur-multifichiers.md:241:| vérification par empreintes | **1 587 tenseurs · TOUT CONCORDE** |
=== git status ===
 M journal/README.md
  ```

### 🤖 Assistant

⏵ Lecture de histoire.md pour la table de renommage (QTNT, calque).

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/histoire.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/histoire.md</path>
<type>file</type>
<content>
1: # Histoire du projet, et le renommage
2: 
3: Ce document est là pour une raison précise : **le 30 septembre 2026, le projet a
4: changé de nom, partout, d'un coup.** Renommer efface des traces ; ce fichier est
5: la trace qu'on ne voulait pas perdre.
6: 
7: ## 1. Le projet a eu trois âges
8: 
9: | âge | ce qu'il était | où c'est écrit |
10: |---|---|---|
11: | **Qtrinet** (origine) | inférence de LLM en ternaire / multi-bits sur un cluster de cartes **Stratix V** (Microsoft Storey Peak), 100 % logique, sans DSP. Le cahier des charges d'origine est **conservé tel quel** : [`Qtrinet-bootstrap.md`](../Qtrinet-bootstrap.md) — c'est un document daté, il n'est pas réécrit | `Qtrinet-bootstrap.md`, `README.md` §« Écarts avec le CDC » |
12: | **le virage événementiel** | l'idée qui a tout changé : ne plus multiplier des matrices, mais **pousser des listes d'activation** vers leurs destinations (AER, *Address Event Representation*). Le prototype C mesure **7,79 G événements/s**, le croisement push/pull est mesuré à **~22 % de densité** | `reports/rapport-cpu-aer.md`, `reports/rapport
… [3503 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du mode 4 dans le rapport dédié et dans le code.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,60p' reports/rapport-mode4-lot-listes.md", "description": "Read mode 4 report"}`

  ```
# Mode 4 — le lot en listes : ÷2,3 sur les octets, et ce qu'il coûte

**En une ligne** : un préremplissage de N états peut voyager en **listes creuses**
au lieu de f32 dense — 1,5 ko par jeton contre 3,5 — au prix d'une quantification
dont l'effet **dépend de la longueur du lot**, ce que ce rapport chiffre au lieu de
le cacher.

## Ce que le mode ajoute

Le mode 3 (lot dense) envoie `t × dimension × f32` : simple, sans perte, et c'est
lui qui a rendu le préremplissage réparti fidèle (0,00e0). Le mode 4 envoie le même
lot **en listes** : chaque état est encodé comme le mode 2 (indices par écarts u8
avec échappement vers u16, valeurs i8, une échelle f32 par bloc de 32 canaux) et
**auto-délimité** par un préfixe de 12 octets — `a_j · n_blocs_j · longueur_j` —
dont les trois tailles se lisent avant toute allocation.

Le mode est **avec perte**, comme le mode 2. Le critère n'est donc pas l'égalité
mais la comparaison à ce que le mode 2 coûte déjà.

## Mesuré

Corpus WikiText-2, 256 jetons, 16 jetons par lot, seuil 0,01, deux processus
locaux :

| | octets par jeton | écart local/réparti |
|---|---|---|
| mode 2, un flux par jeton (référence) | 1 608 par flux | 2,74e-2 |
| **mode 4, lots
… [1670 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"sans_emprunt\\|SANS_EMPRUNT\\|emprunt\" drave-core/src/model.rs | head -20; echo \"=== borrow types ===\"; grep -n \"Source::\\|enum Source\" drave-core/src/model.rs | head -20", "description": "Check borrowed formats in co … [4 caractères tronqués]`

  ```
758:    /// Matrice 4 bits de l'expert `e`, **empruntée** au fichier.
764:                    crate::list::DenseQ4::emprunter_q4k(base, self.n_out, self.n_in, self.nb),
766:                    crate::list::DenseQ4::emprunter_q6k(base, self.n_out, self.n_in, self.nb),
768:                    crate::list::DenseQ4::emprunter(base, self.n_out, self.n_in, self.nb, true),
769:                _ => crate::list::DenseQ4::emprunter(base, self.n_out, self.n_in, self.nb, false),
960:                (None, None, Some(unsafe { DenseQ4::emprunter_q6k(buf.as_ptr(), n_out, n_in, nb) }))
964:                (None, None, Some(unsafe { DenseQ4::emprunter_q4k(buf.as_ptr(), n_out, n_in, nb) }))
966:                (None, None, Some(unsafe { DenseQ4::emprunter(buf.as_ptr(), n_out, n_in, nb, true) }))
968:                (None, None, Some(unsafe { DenseQ4::emprunter(buf.as_ptr(), n_out, n_in, nb, false) }))
976:            // `DRAVE_SANS_EMPRUNT=1` force la reconstruction : c'est ce qui permet
977:            // de comparer nos deux schémas d'échelle à la référence empruntée.
978:            let emprunt = keep >= 1.0 && std::env::var("DRAVE_SANS_EMPRUNT").is_err();
979:            match (emprunt, g.q8_blo
… [1232 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des artefacts Colab (bundle, notebook, script).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls colab/ 2>/dev/null; echo \"---\"; sed -n '1,40p' tools/preparer_colab.sh; echo \"--- taille dépôt ---\"; du -sh .git 2>/dev/null", "description": "Check colab artifacts and repo size"}`

  ```
Drave-reparti.ipynb
README.md
---
#!/bin/bash
# Prépare la répétition Colab : le dépôt en UN fichier, l'empreinte du modèle,
# et les commandes des deux côtés. Rien n'est envoyé nulle part — c'est vous qui
# téléversez, et le script vous dit quoi vérifier.
#
#   tools/preparer_colab.sh [modèle.gguf] [port]
set -u
cd "$(dirname "$0")/.."
MODELE=${1:-models/Qwen2.5-0.5B-Q8_0.gguf}
PORT=${2:-5599}
BUNDLE=/tmp/drave.bundle

echo "=== 1. le dépôt, en un fichier ==="
git bundle create "$BUNDLE" --all >/dev/null 2>&1 || { echo "échec du bundle"; exit 1; }
git bundle verify "$BUNDLE" 2>&1 | tail -1
echo "    $BUNDLE : $(stat -c%s "$BUNDLE") octets ($(du -h "$BUNDLE" | cut -f1))"
echo "    commit : $(git log --oneline -1)"

echo
echo "=== 2. le modèle (le MÊME des deux côtés) ==="
if [ -f "$MODELE" ]; then
    TAILLE=$(stat -c%s "$MODELE")
    EMPREINTE=$(sha256sum "$MODELE" | cut -c1-24)
    echo "    $MODELE : $((TAILLE / 1048576)) Mo"
    echo "    sha256 (24 premiers) : $EMPREINTE"
    echo "    → à coller dans la cellule 4 du notebook (constante ATTENDU)"
else
    echo "    $MODELE introuvable"
fi

echo
echo "=== 3. côté MACHINE LOCALE (le nœud moteur) ==="
cat <<COMMANDES
    cd $(pwd
… [495 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Estimation de la taille réelle du bundle Colab (le doc annonce 4,5 Mo).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git count-objects -vH && echo \"--- .gitignore ---\" && cat .gitignore 2>/dev/null | head -20 && echo \"--- tracked size estimate ---\" && git ls-files | wc -l", "description": "Estimate git packed size"}`

  ```
count: 1318
size: 112.50 MiB
in-pack: 4608
packs: 2
size-pack: 6.59 MiB
prune-packable: 0
garbage: 0
size-garbage: 0 bytes
--- .gitignore ---
__pycache__/
*.pyc
reports/*.tmp
models/
data/
qtrinet-core/target/

# Traces de session : la copie brute reste sur disque (volumineuse, binaire),
# le digest markdown est versionné.
journal/sessions/*/session.jsonl.zstd
journal/sessions/archive.log

# Outil de référence : la source est versionnée, le binaire se recompile
# (commande exacte dans tools/ref_logits.md).
tools/ref_logits
target/
--- tracked size estimate ---
219
  ```

### 🤖 Assistant

⏵ Vérification des outils d'analyse de flux (analyse/diff/profil) pour étayer la finalité manquante.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -12 tools/analyse_flux.py; echo \"=== diff_flux ===\"; head -8 tools/diff_flux.py; echo \"=== profil_flux ===\"; head -8 tools/profil_flux.py; echo \"=== rapport-analyse-flux ===\"; head -12 reports/rapport-analyse-flux.md", "de … [42 caractères tronqués]`

  ```
#!/usr/bin/env python3
"""Analyse PURE d'une trace de flux : ce que la vision appelle « voir le modèle
neurone par neurone », mais chiffré par couche et sans exécuter le moteur.

Ce que l'outil répond, et pourquoi ces questions-là :

* **quelle couche est creuse** ? C'est la décision push/pull du projet (le
  croisement mesuré est à ~10 % de densité) — mais elle se prend PAR COUCHE, pas
  pour le modèle entier ;
* **quels neurones sont PERSISTANTS** (actifs dans presque tous les jetons) ?
  Ceux-là ne bénéficient d'aucune sparsité : les compter dit combien de
  « toujours là » porte le modèle ;
=== diff_flux ===
#!/usr/bin/env python3
"""Diff de deux traces de **flux d'activation** (format DRVF).

C'est l'outil qui manquait à la vision : deux exécutions du même modèle, et on
veut savoir non pas « la perplexité a bougé » mais **où** le flux diverge, à
quelle couche, à quel jeton, et de combien.

Usage : diff_flux.py <traceA> <traceB> [--top 8]
=== profil_flux ===
#!/usr/bin/env python3
"""Profilage par neurone à partir d'une trace de flux (format DRVF).

Ce que la vision demande, rendu calculable : « quels neurones s'allument, à
quelle fréquence, avec quelle magnitude » — par couche
… [736 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Dernières vérifications de chiffres (17,4294 ; 1,3 % ; 0,845 s ; vocabulaire « calque »).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 17,4294 ===\"; grep -rn \"17,4294\" reports/*.md docs/*.md REPRISE.md | head; echo \"=== 1,3 % transport ===\"; grep -rn \"1,3 %\" reports/rapport-transport-liste.md reports/rapport-mode4-lot-listes.md | head; echo \"=== 0 … [257 caractères tronqués]`

  ```
=== 17,4294 ===
reports/rapport-coherence-docs.md:117:| 56 | `docs/format-flux.md:138` | rejeu par lots : **17,4294** | cohérent avec les mesures de rejeu ; la valeur 18,0851 du mode lot est, elle, employée dans `REPRISE.md` sans source de rapport (le rapport de la phase 3.4 n'a jamais été écrit) | OK |
reports/rapport-coherence-docs.md:226:| OK | **17** | formats des modes 2 et 3 · `flux_brut` · `hôte:port` · trace dense 66 370 408 o (fichier réellement relu) · 66 370 406 hors sentinelle · 24 576 listes / 22 008 776 actifs (source) · 918 ko · 24,90 / 25,00 · +9,1 % · rejeu 17,4294 · corrections de l'audit drapeaux · table `DRAVE_*` de REPRISE · `profil_flux.py` · outils FPGA · `flux_codec.py` lit la v3 · `DRAVE_TRACE_BLOCS` documentée |
docs/format-flux.md:176:| un rejeu redonne le même résultat | `--flux-forcer` : perplexité **19,3885** avec et sans rejeu (chemin par jeton), **17,4294** (chemin par lots) |
=== 1,3 % transport ===
reports/rapport-transport-liste.md:161:ci-dessous — **÷2,3 sur le fil pour 1,3 % d'écart à 1 024 jetons** (2,7 % à 256,
=== 0,845 ===
reports/rapport-capteur-hebbien.md:44:| Énergie expliquée par `W · C` (prédiction linéaire) | **R² = 0,845** |
=== calqu
… [5 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des sources des chiffres de chargement de convertisseur.md.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 413 Mo / 21,0110 / 353 Mo ===\"; grep -rn \"413 Mo\\|21,0110\\|353 Mo\\|21,0116\" reports/*.md REPRISE.md | head -10; echo \"=== 0,845 / 2,70 ===\"; grep -rn \"845 ms\\|2,70\\|2.70\" reports/*.md | head -10; echo \"=== rap … [131 caractères tronqués]`

  ```
=== 413 Mo / 21,0110 / 353 Mo ===
reports/rapport-coherence-docs.md:115:| 54 | `README.md:397` | Q4_0 : +9,1 % contre Q8_0 | 21,0116 contre 19,2647 = +9,07 % (`rapport-mur-memoire-4bits.md:143-145`) | OK |
reports/rapport-mur-memoire-4bits.md:145:| Qwen2.5-0.5B **Q4_0** | **4 bits verbatim** | **21,0116** | **+9,1 %** | **13,1** | **38,9** |
reports/rapport-mur-memoire-4bits.md:191:montré. La perplexité bouge au 4ᵉ chiffre (21,0116 → 21,0131) : la somme n'est
REPRISE.md:63:| Qwen2.5-0.5B Q4_0 | `--q4 --limit 512` | **21,0110** |
=== 0,845 / 2,70 ===
reports/rapport-gpu-topk-selection.md:145:| 262 144 | 256 | 0,07 ms | 0,98 ms | **2,70e-7** |
reports/rapport-inference.md:167:| `(?i:)` absent | 4 | `we'D` : `6 35` → `27705` |
=== rapport-modele-reel head ===
# Drave — le modèle réel expose-t-il ses grappes ?

Modèle analysé : **qwen2**, 24 couches, hidden 896, intermédiaire 4864, 14 têtes / 2 KV (GQA).

## 1. Parcimonie intrinsèque

| Tenseur (couche 0) | \|w\|<5 % max | <10 % | <20 % |
|---|---|---|---|
| blk.0.attn_norm.weight | 19.0 % | 77.9 % | 92.2 % |
| blk.0.ffn_down.weight | 62.5 % | 91.1 % | 99.7 % |
| blk.0.ffn_gate.weight | 73.8 % | 96.3 % | 99.9 % |
| blk.0.ffn_up.weight 
… [579 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du rapport gpt-oss (source des chiffres de convertisseur.md) et de la latence Colab.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 42 127 / 39,8 ===\"; grep -rn \"42 127\\|39,8\" reports/rapport-gpt-oss-perplexite.md | head -10; echo \"=== 195 ms / 62,2 ===\"; grep -rn \"195 ms\\|62,2 Go\" reports/*.md | head -10; echo \"=== 97,6 / 16,1 ===\"; grep -r … [104 caractères tronqués]`

  ```
=== 42 127 / 39,8 ===
10:`REPRISE.md` §6.a annonçait : perplexité **39,8** « au lieu de l'ordre de 6 »,
12:(39,8 à 63 jetons, 129,9 à 511). Trois hypothèses étaient en lice : le gabarit
28:| avant (biais O ignoré) | **39,80** |
=== 195 ms / 62,2 ===
=== 97,6 / 16,1 ===
reports/rapport-transport-liste.md:192:| attente du pair | **97,6 ms/jeton** | **16,1 ms/jeton** |
reports/rapport-transport-liste.md:196:L'attente de 97,6 ms n'était ni le calcul distant ni le débit : c'était **Nagle
  ```

### 🤖 Assistant

⏵ Lecture du résumé du rapport gpt-oss pour cadrer les chiffres de convertisseur.md.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,60p' reports/rapport-gpt-oss-perplexite.md", "description": "Read gpt-oss perplexity report summary"}`

  ```
# Perplexité de gpt-oss : deux bugs réels, une prémisse fausse

> Session du 28/09 (reprise de `REPRISE.md` §6.a). Tous les chiffres de ce
> rapport sont **mesurés** sur cette machine, avec le corpus
> `/tmp/wt2_txt.txt` (20 000 premiers octets de `data/wikitext2_test.txt`),
> gpt-oss-120b MXFP4, `--ctx 256 --dense --threads 16`, sauf mention contraire.

## 1. Ce qu'on croyait

`REPRISE.md` §6.a annonçait : perplexité **39,8** « au lieu de l'ordre de 6 »,
génération correcte, et une perplexité qui **croît avec la fenêtre**
(39,8 à 63 jetons, 129,9 à 511). Trois hypothèses étaient en lice : le gabarit
harmony, un codage de position faux (YaRN), et un bug de calcul restant.

## 2. Ce qui était réellement cassé

### a. Le biais de la projection de sortie d'attention était ignoré

gpt-oss déclare `attention_bias = true` : ses projections Q, K, V **et O** ont un
biais. Le chargeur passait bien les biais de Q, K et V, mais `None` pour
`attn_output` — un décalage constant ajouté à la sortie de chaque couche, donc
amplifié 36 fois.

Mesure, 63 jetons, tout le reste identique :

| | perplexité (63 jetons) |
|---|---|
| avant (biais O ignoré) | **39,80** |
| après (biais O chargé) | **20,84*
… [1395 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Relecture exacte des lignes à citer dans contexte-long.md.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md", "offset": 404, "limit": 12}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md", "offset": 532, "limit": 20}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md</path>
<type>file</type>
<content>
404: ## 5. YaRN à retardement : ce que la mesure a dit
405: 
406: Politique implémentée (`[config] rotation` le dit à chaque chargement) : **RoPE
407: simple tant que le contexte demandé tient dans la longueur initiale déclarée
408: (4 096 pour gpt-oss), interpolation YaRN au-delà — sans la mise à l'échelle de
409: température** ; `DRAVE_YARN=1` force le YaRN complet des implémentations de
410: référence, `DRAVE_YARN_NON=1` jamais, `DRAVE_YARN_MSCALE=0/1` tranche sur la
411: température seule. Décision **par séquence**, pas par position : la structure de
412: position relative ne survit que si toutes les clés partagent le même jeu de
413: fréquences.
414: 
415: > **Protocole.** Les courbes ci-dessous ont été mesurées « par longueur »

(Showing lines 404-415 of 580. Use offset=416 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md</path>
<type>file</type>
<content>
532: ## 6. Ce qui se mesure tout de suite
533: 
534: 1. **Aiguille dans la botte de foin** (`tools/aiguille.py`) : la perplexité ne dit
535:    pas si le modèle RETROUVE une information. Le script plante un code à une
536:    profondeur donnée et vérifie qu'il ressort ; c'est la mesure de qualité qui
537:    manque au plan. Premier essai sur Qwen2.5-0.5B : **6 sondes sur 6 échouent**
538:    (1 024 et 2 048 jetons, profondeurs 0,1 / 0,5 / 0,9) — le demi-milliard de
539:    paramètres ne sait pas retrouver un code, donc ce modèle ne peut pas servir de
540:    référence ; l'essai est relancé sur Qwen3-30B-A3B. Ce n'est pas un défaut du
541:    moteur : c'est la limite du modèle, et il valait mieux la mesurer que la
542:    supposer. Second essai sur Qwen3-30B-A3B : **9,6 minutes pour une seule
543:    sonde** (1 024 jetons de contexte) et un échec — le remplissage, répété à
544:    l'identique, ne fait pas un banc d'essai valable, et le préremplissage
545:    séquentiel rend chaque sonde hors de prix (1,8 jeton/s). Le test est donc
546:    **arrêté** : il faudra un remplissa
… [412 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des chiffres du préremplissage par lots (rapport dédié).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"17,1\\|13,6\\|34,4\\|50 s\" reports/rapport-prefill-par-lots.md | head -15; echo \"=== head ===\"; head -12 reports/rapport-prefill-par-lots.md", "description": "Verify prefill-by-lots figures"}`

  ```
124:Bout en bout, sans profil (qui ajoute ses propres horloges) : **17,1 s → 13,6 s,
126:regroupé par expert, contexte 256, 255 jetons) : lot 1 ≈ 50 s, lots 64/128/256 =
127:**33,7 / 33,9 / 34,4 s**, perplexité 13,7205 dans tous les cas.
193:| Qwen2.5-0.5B Q8_0, `--dense`, 16 fils | 512 | 17,1 s | **13,6 s** | **−20 %** |
194:| gpt-oss-120b MXFP4, MoE groupé, 16 fils | 256 | ≈ 50 s | 34,4 s (lot 256) | **−31 %** |
=== head ===
# Préremplissage par lots : ce que le GEMM apporte vraiment

> Chantier 4 du plan de reprise. Le préremplissage est le mur n° 1 du contexte
> long (`docs/contexte-long.md` : 4,5 h à 32 k, 1 234 h à 1 M en séquentiel) : le
> moteur traitait **un jeton à la fois**, donc chaque matrice de poids était relue
> pour chaque jeton.

## 1. Ce qui a été fait

| pièce | rôle |
|---|---|
| `Pool::gemm_dense_i8` | produit matrice-matrice int8 : une tranche de lignes par fil, tout le lot servi par la même lecture de ligne |
  ```

### 🤖 Assistant

⏵ Impression des lignes exactes à citer pour éviter toute erreur de citation.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs && echo \"###### contexte-long\"; sed -n '101,103p;106,107p;406,408p;545,548p' contexte-long.md | cat -n; echo; echo \"###### format-flux 3-4 + 117-119\"; sed -n '3,4p;117,119p' format-flux.md; echo; echo \"###### format-clusters 1 … [163 caractères tronqués]`

  ```
###### contexte-long
     1	| E1 | **Préremplissage par lots** | **fait** : `gemm_dense_i8` et `gemm_dense_q4` (produits matrice-matrice par tranches), `forward_lot` juste sur dense **et** sur MoE avec regroupement des jetons par expert ; débit bout en bout à chiffrer | 32 k utilisable ; TTFT | le noyau est là ; reste à mesurer et à élargir les tranches |
     2	| E2 | **KV int8** | **fait** (échelle par vecteur, dequantification à la lecture) | ÷4 sur le KV ; 128 k confortable | mesuré : +7,1 % de perplexité (llama.cpp q8_0 : +3,1 %) |
     3	| E3 | **KV int4** | **fait** (nibbles empaquetés) | 1 M tient en RAM (9,7 Go) et en VRAM | mesuré : **+384 %** à 512 jetons, **+364 % à 8 192** — llama.cpp q4_0 : +411 % puis +494 % ; à réserver aux cas où la mémoire manque |
     4	| E6 | **MLA** (DeepSeek) | **non testable ici** : aucun modèle MLA en GGUF sur cette machine (le « deepseek-r1-distill » local est un Qwen dense) | compression structurelle du KV | gros |
     5	| E7 | **Vision** | **non testable ici sans le chemin image** : le projecteur `mmproj` est présent, mais rien ne lit les patchs | images | gros |
     6	Politique implémentée (`[config] rotation` le dit à chaque chargeme
… [1449 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs && echo \"###### convertisseur 111,116,164-169,247-252\"; sed -n '111p;116p;164,169p;247,252p' convertisseur.md; echo; echo \"###### convertisseur 296-313\"; sed -n '296,313p' convertisseur.md", "description": "Print converter line … [16 caractères tronqués]`

  ```
###### convertisseur 111,116,164-169,247-252
## 5. Format proposé : `QTNT`
en-tête      magie, version, nb_calques, nb_tenseurs, alignement (2 Mo), graine
| 2 | lecteur **Q4_K / Q6_K** | à faire | ouvre 7B → 32B |
| 3 | **routeur MoE** + tranches par expert | à faire | gpt-oss-120b : 61 Go/jeton → 2,7 Go/jeton |
| 4 | conteneur `QTNT` + index de placement | à faire | plan CPU/GPU/NUMA lisible avant les poids |
| 5 | placement : épinglage NUMA, threads par calque | à faire | 20,7 → 24,7 Go/s mesuré au banc |
| 6 | **Q8_0 en place** (le noyau `q8_dot_at` existe déjà pour la tête) | à faire | supprime la dernière copie du chemin int8 |
| 7 | mmap (appel système direct) | à faire | grosses pages, partage entre processus |
2. **Épinglage NUMA** : 20 % mesurés, mais `sched_setaffinity` n'est pas dans
   `std` — il faut un appel système direct.
3. **Q8_0 en place** pour les projections (la tête le fait déjà).
4. **gpt-oss-120b** : le routeur MoE fonctionne (top-4 sur 128) mais le modèle
   pèse 60 Go et son encodage d'expert est en MXFP4 avec des tenseurs Q8_0 ;
   c'est l'étape suivante naturelle.

###### convertisseur 296-313
| 2 | **185** | **activation gpt-oss** : `g·σ(1,702·g)·(u+1)`
… [897 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle final : « calque » dans tout le dépôt et numéros de ligne de la vision.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"calque\" . 2>/dev/null | grep -v \"^./journal\" | grep -v \"^./.git\" | head -10; echo \"--- fin ---\"; grep -n \"axe 3\\|router des listes\\|adapt\" docs/vision.md | head", "description": "Final check on calque and vision … [8 caractères tronqués]`

  ```
./docs/convertisseur.md:5:> tuning CPU/hyperthread/core pour les calques sur CPU et similaires pour les
./docs/convertisseur.md:6:> calques sur GPU avec optimisation des calques en fonction des routes PCIe ».
./docs/convertisseur.md:116:en-tête      magie, version, nb_calques, nb_tenseurs, alignement (2 Mo), graine
./docs/convertisseur.md:119:               calque, rang d'expert, dimensions,
./docs/convertisseur.md:139:   peut décider où charger chaque calque sans avoir lu le modèle.
./docs/convertisseur.md:167:| 5 | placement : épinglage NUMA, threads par calque | à faire | 20,7 → 24,7 Go/s mesuré au banc |
--- fin ---
94:Et, au-delà du débogage : **lire ces flux pour comprendre le modèle et adapter
143:dépendance (les poids d'une couche). Distribuer, c'est router des listes.
236:* **ce n'est pas « distribuer, c'est gratuit »** : l'axe 3 est **engagé** (le
  ```

### 🤖 Assistant

⏵ vision.md a changé pendant l'audit ; relecture de l'état courant.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short docs/ && git diff --stat docs/ && echo \"=== md5 ===\" && md5sum docs/vision.md && wc -l docs/vision.md && ls -l --time-style=full-iso docs/vision.md docs/format-flux.md docs/contexte-long.md", "description": "Chec … [32 caractères tronqués]`

  ```
M docs/vision.md
 docs/vision.md | 65 ++++++++++++++++++++++++++++++++++++++++++----------------
 1 file changed, 47 insertions(+), 18 deletions(-)
=== md5 ===
d343bb3d04d96afad89ec0536963e6e0  docs/vision.md
276 docs/vision.md
-rw-------. 1 stephane stephane 32210 2026-10-01 01:07:34.563447827 -0400 docs/contexte-long.md
-rw-r--r--. 1 stephane stephane 10788 2026-09-30 16:03:52.032159336 -0400 docs/format-flux.md
-rw-------. 1 stephane stephane 15135 2026-10-02 09:59:01.079465777 -0400 docs/vision.md
  ```

### 🤖 Assistant

⏵ Lecture de la vision mise à jour (276 lignes) pour recaler l'audit.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/vision.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/vision.md</path>
<type>file</type>
<content>
1: # Drave — la vision
2: 
3: > *« Stream of logs »* : le flux des listes. Et, en français d'ici, **la drave** —
4: > ces billots qu'on confiait à la rivière au printemps, qu'on guidait de
5: > l'estacade jusqu'à la scierie. Le nom dit exactement ce que fait ce moteur :
6: > il ne lit pas des matrices, il conduit un flux.
7: 
8: Ce document est la **vision** du projet : ce qu'il cherche, pourquoi la
9: représentation qu'il a choisie change la nature des problèmes, et ce que cela
10: ouvre sur chaque axe. Il ne remplace pas les rapports — chaque affirmation
11: mesurée renvoie à celui qui la porte — et il distingue partout ce qui est
12: **mesuré**, ce qui est **raisonné**, et ce qui est **à faire**.
13: 
14: Le projet s'appelait `Qtrinet`, du nom de son origine : un cahier des charges
15: d'inférence ternaire sur un cluster de cartes Stratix V
16: (`Qtrinet-bootstrap.md`). Ce cahier des charges reste l'acte de naissance ; le
17: nom, lui, ne dit plus ce que le projet est devenu. **Drave** le dit.
18: 
19: ---
20: 
21: ## 1. Le cœur : des listes, pas des matrices
22: 
23: Un moteu
… [14894 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de la réserve A/B sur l'attention creuse (plan-gpu-topk).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"234,88\\|298,56\\|reproduit\\|A/B\" docs/plan-gpu-topk.md | head -20", "description": "Check plan-gpu-topk on A/B figures"}`

  ```
88:(234,88, gpt-oss, contexte 2 048, mêmes 512 jetons notés : `docs/contexte-long.md`
89:§6) dépend des réglages et n'a pas été reproduit par ce binaire — et le banc 1 M
99:| 4 | branchement dans `model.rs` (autoriser le GPU quand `attn_topk > 0` **et** que le noyau rend `true`, garder le repli CPU sinon) | ✅ **fait**, en opt-in (`DRAVE_GPU_TOPK=1`) : PPL à ctx 2 048 = **9,4162** contre **9,4167** au CPU (le critère chiffré d'origine (234,88, `docs/contexte-long.md` §6) n'est pas reproduit par ce binaire — c'est la comparaison A/B qui fait foi) · ⚠️ le gain de TEMPS n'est pas là à 2 048 clés : six lancements et cinq recopies par couche et par jeton — la fusion des quatre passes est la prochaine étape |
  ```

### 🤖 Assistant

⏵ Rédaction du rapport adverse et envoi au parent.

J'ai terminé l'audit (vision relue deux fois — elle a été modifiée pendant l'audit, je me suis recalé sur sa version courante). Le rapport est ci-dessous, puis envoyé au parent.

| fichier:ligne | citation exacte (≤ 25 mots) | problème | correction minimale proposée (texte de remplacement exact) | gravité |
|---|---|---|---|---|
| docs/format-flux.md:3 | « Ce format sert **trois choses à la fois**, et c'est délibéré : » | Le format/transport ne nomme jamais la finalité d'analyse de la vision (« comprendre le modèle et adapter l'architecture à la tâche », vision.md:94-99), alors que les outils existent (`tools/analyse_flux.py`, `profil_flux.py`, `diff_flux.py`) et que la vision fait du journal « l'instrument de réglage ». | Remplacer par « Ce format sert **quatre choses à la fois**, et c'est délibéré : » puis ajouter après l'item 3 (ligne 10) : « 4. l'**analyse** : les mêmes octets, relus par `tools/profil_flux.py`, `tools/analyse_flux.py` et `tools/diff_flux.py`, disent quels neurones travaillent — la donnée qui adapte l'architecture à la tâche. » | moyenne |
| docs/format-flux.md:119 | « est qu'il ne coûte pas plus de 1,5 fois celui-ci. » | Le critère des 1,5× n'est vérifié qu'à 256 jetons ; `reports/rapport-mode4-lot-listes.md` (tableau « selon la longueur ») mesure **5,6× à 20 jetons** et 0,50× à 64 : la réserve n'est pas portée. | « est qu'il ne coûte pas plus de 1,5 fois celui-ci **à 256 jetons** (5,6× à 20 jetons — `reports/rapport-mode4-lot-listes.md`). » | basse |
| docs/format-clusters.md:5-6 | « un nœud n'ouvre que ce qu'il sert — mesuré **3,20 Go au lieu de 18,56** et **625 ms au lieu de 3,9 s** » | Les grappes sont cadrées comme un rangement de fichiers et un gain de chargement, alors que la vision en fait l'unité de **placement** des neurones entre machines (axe 3, vision.md:131-143) — le document ne dit jamais que les flux se routent entre grappes. | Ajouter après la ligne 6 : « **Et c'est le mécanisme de placement** : ces grappes sont les neurones qu'on répartit entre nœuds, et le flux d'activation se route de l'une à l'autre (vision, axe 3). » | moyenne |
| docs/convertisseur.md:111 | « ## 5. Format proposé : `QTNT` » | `QTNT` porte l'ancien nom du projet (Qtrinet) alors que le renommage du 30/09 est « fait partout » (`docs/histoire.md:28-36`, vision.md:264-266) ; aucun autre fichier du dépôt ne l'emploie, et le conteneur n'est jamais relié au format de flux réellement implémenté (`DRVF`). | « ## 5. Format proposé : conteneur **Drave** (ex-`QTNT`), adossé au format de flux `DRVF` » — même remplacement du jeton à la ligne 166 (« conteneur **Drave** (ex-`QTNT`) + index de placement »). | basse |
| docs/convertisseur.md:116 | « en-tête      magie, version, nb_calques, nb_tenseurs, alignement (2 Mo), graine » | « calque » n'apparaît nulle part ailleurs dans le dépôt hors ce document (le moteur dit « couche ») ; reste du vocabulaire d'avant le renommage (la citation de la directive, ligne 6, est une pièce datée et n'est pas visée). | « en-tête      magie, version, nb_couches, nb_tenseurs, alignement (2 Mo), graine » (idem « calque » → « couche », lignes 119, 139, 167). | basse |
| docs/convertisseur.md:167 | « \| 7 \| mmap (appel système direct) \| à faire \| » | Contredit `docs/format-clusters.md:176-179` (« Le mmap : **FAIT** », 9,32 s / 6,35 Go contre 30,68 s / 19,20 Go). | « \| 7 \| mmap (appel système direct) \| **fait** \| grosses pages, partage entre processus (`docs/format-clusters.md:176`) \| » | basse |
| docs/convertisseur.md:247 | « 2. **Épinglage NUMA** : 20 % mesurés, mais `sched_setaffinity` n'est pas dans » | Le drapeau `--pin` existe et a été mesuré **perdant** (ligne 186 : « ✅ mesuré, **négatif** », et § « L'épinglage NUMA ne paie pas ») : l'item « reste à faire » est périmé. | « 2. **Épinglage NUMA** : **fait** (`--pin`), mesuré **perdant** — 23,2 → 27,6 s sur le 30B MoE (ligne 186). » | moyenne |
| docs/convertisseur.md:249 | « 3. **Q8_0 en place** pour les projections (la tête le fait déjà). » | Contredit le tableau « Ce qui est fait » du même document (ligne 187 : « Q8_0 en place (projections) ✅ — chargement 2,73 → 0,81 s, mémoire 921 → 566 Mo »). | « 3. **Q8_0 en place** pour les projections : **fait** — chargement 2,73 → 0,81 s, mémoire 921 → 566 Mo (ligne 187). » | moyenne |
| docs/convertisseur.md:250 | « 4. **gpt-oss-120b** : le routeur MoE fonctionne (top-4 sur 128) mais le modèle » | Périmé : le même document dit plus bas qu'il « charge et tourne » (5 tok/s) et c'est une porte publiée — **15,6017** à ctx 256 (`README.md:374`, `reports/rapport-routage-experts.md:66`). | « 4. **gpt-oss-120b** : **charge et tourne** (voir ci-dessous) ; porte de non-régression **15,6017** à ctx 256 — `README.md:374`. » | moyenne |
| docs/convertisseur.md:311-313 | « Les suspects restants sont donc plus fins : le facteur d'échelle de l'attention, l'ordre exact des normes, ou la rampe YaRN » | Hypothèse réfutée le jour même : le biais de `attn_output` était ignoré et la fenêtre s'appliquait à 36/36 couches — 39,80 → **20,84** à 63 jetons (`reports/rapport-gpt-oss-perplexite.md` §2.a-b). | « Les suspects restants ont été testés le jour même : biais de `attn_output` (ignoré) et fenêtre sur 36/36 couches — 39,80 → **20,84** à 63 jetons (`reports/rapport-gpt-oss-perplexite.md`). » | moyenne |
| docs/colab-reparti.md:37 | « **Débit** : 3 663 octets par flux en dense (en-tête v4 compris) » | Version de protocole périmée : le protocole courant est **v5** (modes 0-4, dont « LOT en listes ») — `docs/format-flux.md:84-89`, `drave-core/src/main.rs:1862` ; la taille d'en-tête (79 o) est inchangée, le chiffre reste bon. | « **Débit** : 3 663 octets par flux en dense (en-tête **v5** compris) » | moyenne |
| docs/colab-reparti.md:3-4 | « Objectif : deux machines qui se passent des **listes d'activation**, l'une sur le runtime Colab, l'autre en local » | Le document de transport cadre le flux comme une pure recette de fidélité ; la finalité d'analyse de la vision (vision.md:94-99) est absente des documents de format et de transport. | Ajouter après la ligne 4 : « Ce flux est aussi le **journal** qu'on relit (`--trace-flux`, `tools/analyse_flux.py`) pour comprendre le modèle et adapter l'architecture à la tâche. » | moyenne |
| docs/contexte-long.md:101 | « débit bout en bout à chiffrer » | Mesuré depuis : 17,1 → 13,6 s (−20 %) sur Qwen ctx 512 et ≈50 → 34,4 s (−31 %) sur gpt-oss ctx 256 (`reports/rapport-prefill-par-lots.md:193-194`) ; la fin de la ligne (« reste à mesurer ») est du même tonneau. | Remplacer par « débit bout en bout **mesuré** (Qwen ctx 512 : 17,1 → 13,6 s, −20 % ; gpt-oss ctx 256 : ≈50 → 34,4 s, −31 %) — `reports/rapport-prefill-par-lots.md` ». | moyenne |
| docs/contexte-long.md:102 | « mesuré : +7,1 % de perplexité (llama.cpp q8_0 : +3,1 %) » | Périmé : le même document (§4.bis) mesure **+1,5 %** à 512 et **+3,0 %** à 8 192 depuis les échelles par bloc de 32 ; « échelle par vecteur » (même ligne) ne décrit plus le code (vision.md:215-217, `REPRISE.md:179`). | « \| E2 \| **KV int8** \| **fait** (échelle **par bloc de 32**, dequantification à la lecture) \| ÷4 sur le KV ; 128 k confortable \| mesuré : **+1,5 %** à 512 jetons, **+3,0 %** à 8 192 (llama.cpp q8_0 : +0,8 %) \| » | moyenne |
| docs/contexte-long.md:103 | « mesuré : **+384 %** à 512 jetons, **+364 % à 8 192** » | Le +384 % est la mesure d'avant les échelles par bloc de 32 ; la valeur courante à 512 est **+219 %** (`REPRISE.md:180` : « était +384 % et +450 % » ; même document §4.bis). | « mesuré : **+219 %** à 512 jetons, **+364 % à 8 192** » | basse |
| docs/contexte-long.md:106 | « **non testable ici** : aucun modèle MLA en GGUF sur cette machine » | Périmé au 02/10 : MLA validée contre llama.cpp — GLM-5.3 corrélation **0,999024**, Kimi-K2.7 calculable (`reports/rapport-mla-experts.md:99-118`, `docs/plan-deepseek41-complet.md`) ; seule V4.1 reste bloquée. | « **validée** contre llama.cpp (GLM-5.3, corrélation **0,999024** ; Kimi-K2.7 calculable) — V4.1 encore bloquée (hyper-connexions, sortie à rang faible) ; `reports/rapport-mla-experts.md` » | haute |
| docs/contexte-long.md:107 | « **non testable ici sans le chemin image** : le projecteur `mmproj` est présent, mais rien ne lit les patchs » | Périmé : chaîne image complète démontrée (patchs **5,4e-7**, projecteur **1,7e-6**, une couche 1,8e-6) — `REPRISE.md:220-229`, `docs/plan-mla-vision.md`. | « **faite** : chaîne complète démontrée (patchs **5,4e-7**, projecteur **1,7e-6**) — `docs/plan-mla-vision.md` » | haute |
| docs/contexte-long.md:407-408 | « simple tant que le contexte demandé tient dans la longueur initiale déclarée (4 096 pour gpt-oss), interpolation YaRN au-delà » | Décrit l'ancienne politique : le code bascule à `ctx > original × 4` (`drave-core/src/model.rs:2198`) et le §5.quater du même document fixe le seuil à **4 ×** (16 384 pour gpt-oss). | « simple tant que le contexte demandé ne dépasse pas **4 ×** la longueur initiale déclarée (16 384 pour gpt-oss, §5.quater), interpolation YaRN au-delà » | moyenne |
| docs/contexte-long.md:545-546 | « Le test est donc **arrêté** : il faudra un remplissage varié (du vrai texte) » | Périmé : l'aiguille v2 (remplissage WikiText-2, réponses de 40 jetons, préremplissage par lots) trouve **12/12** — `reports/rapport-aiguille.md:74`, `REPRISE.md:190`. | « Le test a depuis été relancé (v2 : remplissage Wikitext-2, réponses de 40 jetons, préremplissage par lots) et **12 sondes sur 12** sont trouvées — `reports/rapport-aiguille.md` » | moyenne |
| docs/contexte-long.md:560 | « \| **top-256 clés par requête** (`--attn-topk 256`) \| **234,88** ← *meilleure* \| » | Les valeurs absolues de ce tableau ne sont pas reproduites par le binaire actuel : la vision (vision.md:79-83) et `docs/plan-gpu-topk.md:88-89,99` disent que seul l'écart A/B fait foi (ctx 2 048 : 9,4162 GPU contre 9,4167 CPU). | Ajouter après la ligne 561 : « (valeurs du 30/09, non reproduites depuis — l'écart A/B fait foi : `docs/plan-gpu-topk.md:88-89`) ». | basse |

**Ce qui est déjà cohérent et ne doit pas être touché**

- `docs/format-flux.md` : protocole **v5** et cinq modes, dont le mode 4 « LOT en listes » (l.84-120) ; les trois usages posés d'emblée (l.3-14) ; « des listes, pas des matrices » jusque sur le câble (l.133-136) ; l'avertissement sur les 39 octets d'époque (l.157-160) ; la règle de la norme finale (l.162-169).
- `docs/format-clusters.md` : porte clusters **799,8557** / 6,28 Go (l.168) conforme aux faits ; § « Le nœud partiel » et la somme des contributions manquante **entre nœuds** (l.157-173), qui suppose bien la répartition ; ordre des experts par trace de routage mesurée (l.60-71) ; chiffres adossés à `rapport-decoupage-moe.md` et `rapport-lecteur-multifichiers.md`.
- `docs/convertisseur.md` : les résultats négatifs assumés (seuil d'abolition des zéros à 25 %, l.47-59 ; épinglage NUMA perdant, l.231-236 ; plan qui surestime les MoE d'un facteur 2, l.238-242) ; la fidélité par emprunt (l.27-33 et l.144-157) ; aucune porte périmée (Qwen 0,5B = 19,3885, l.193).
- `docs/colab-reparti.md` : les 14 champs du contrat d'activation (l.24) ; l'aveu que les deux nœuds chargent le modèle entier (l.27, 30-33) ; le critère d'écart `0,00e0` (l.22, 104-112) ; modes 3 et 4 avec leurs chiffres (l.28).
- `docs/contexte-long.md` : la campagne de placement des bits et le réglage recommandé `DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1` (l.176-210) ; §5.quater (seuil à 4 ×) ; les chiffres du noyau KV GPU (l.226-250, 299-353) ; le rappel de méthode final (l.574-580).
- Global : dans les cinq documents, **aucune porte périmée** (19,3885 et 799,8557 exacts), aucun compte de tests ni liste de formats périmés, et les renvois aux rapports sont présents partout sauf `convertisseur.md` (qui est le porteur de ses propres mesures).

**Points à trancher par l'humain**

1. **Nom du conteneur `QTNT`** : le renommer (quel nom ? le document ne doit pas inventer d'acronyme) ou supprimer la section au profit du format de flux `DRVF` — décision de nommage, pas de contenu.
2. **Tableaux « Ordre de marche » / « Reste à faire » de `convertisseur.md`** (daté du 28/09) : à garder comme journal daté ou à mettre à jour ? Les constats mmap / NUMA / Q8_0 / gpt-oss en découlent.
3. **Séries KV canoniques** : `contexte-long.md` porte côte à côte les mesures « par vecteur » (§4.bis, tableau E) et « par bloc de 32 » (§4.bis.3) — choisir la série qui fait référence dans le tableau E.
4. **DRVF et les deux cas de la vision** (vision.md:202-211) : faut-il spécifier dans le format le cas général « connexion pondérée » et le cas trinaire « deux listes » (le signe porté par l'appartenance), aujourd'hui absents du document de format ?
5. **Hors des cinq documents (code)** : le commentaire `drave-core/src/model.rs:1518-1519` dit que le croisement push/pull est à « 10 % de densité » (repris par `tools/analyse_flux.py`) alors que `seuil_push = 0.22` (model.rs:2621) et que le rapport/la vision disent **~22 %** — à aligner.

- **send_message** `{"agent_id": "bbd6969f-0f70-42b2-8951-64d1f2f36d2e", "message": "RAPPORT DE RELECTURE ADVERSE — 5 documents (aucun fichier modifié). Note : docs/vision.md a été modifié pendant mon audit (02/10 09:59) ; je me suis recalé sur sa version courante (v5, gpt-oss 15,6017, finalité d'analyse l.94-99, conne … [12262 caractères tronqués]`

  ```
message delivered to agent bbd6969f-0f70-42b2-8951-64d1f2f36d2e
  ```

### 🤖 Assistant

| fichier:ligne | citation exacte (≤ 25 mots) | problème | correction minimale proposée (texte de remplacement exact) | gravité |
|---|---|---|---|---|
| docs/format-flux.md:3 | « Ce format sert **trois choses à la fois**, et c'est délibéré : » | Le format/transport ne nomme jamais la finalité d'analyse de la vision (« comprendre le modèle et adapter l'architecture à la tâche », vision.md:94-99), alors que les outils existent (`tools/analyse_flux.py`, `profil_flux.py`, `diff_flux.py`) et que la vision fait du journal « l'instrument de réglage ». | Remplacer par « Ce format sert **quatre choses à la fois**, et c'est délibéré : » puis ajouter après l'item 3 (ligne 10) : « 4. l'**analyse** : les mêmes octets, relus par `tools/profil_flux.py`, `tools/analyse_flux.py` et `tools/diff_flux.py`, disent quels neurones travaillent — la donnée qui adapte l'architecture à la tâche. » | moyenne |
| docs/format-flux.md:119 | « est qu'il ne coûte pas plus de 1,5 fois celui-ci. » | Le critère des 1,5× n'est vérifié qu'à 256 jetons ; `reports/rapport-mode4-lot-listes.md` (tableau « selon la longueur ») mesure **5,6× à 20 jetons** et 0,50× à 64 : la réserve n'est pas portée. | « est qu'il ne coûte pas plus de 1,5 fois celui-ci **à 256 jetons** (5,6× à 20 jetons — `reports/rapport-mode4-lot-listes.md`). » | basse |
| docs/format-clusters.md:5-6 | « un nœud n'ouvre que ce qu'il sert — mesuré **3,20 Go au lieu de 18,56** et **625 ms au lieu de 3,9 s** » | Les grappes sont cadrées comme un rangement de fichiers et un gain de chargement, alors que la vision en fait l'unité de **placement** des neurones entre machines (axe 3, vision.md:131-143) — le document ne dit jamais que les flux se routent entre grappes. | Ajouter après la ligne 6 : « **Et c'est le mécanisme de placement** : ces grappes sont les neurones qu'on répartit entre nœuds, et le flux d'activation se route de l'une à l'autre (vision, axe 3). » | moyenne |
| docs/convertisseur.md:111 | « ## 5. Format proposé : `QTNT` » | `QTNT` porte l'ancien nom du projet (Qtrinet) alors que le renommage du 30/09 est « fait partout » (`docs/histoire.md:28-36`, vision.md:264-266) ; aucun autre fichier du dépôt ne l'emploie, et le conteneur n'est jamais relié au format de flux réellement implémenté (`DRVF`). | « ## 5. Format proposé : conteneur **Drave** (ex-`QTNT`), adossé au format de flux `DRVF` » — même remplacement du jeton à la ligne 166 (« conteneur **Drave** (ex-`QTNT`) + index de placement »). | basse |
| docs/convertisseur.md:116 | « en-tête      magie, version, nb_calques, nb_tenseurs, alignement (2 Mo), graine » | « calque » n'apparaît nulle part ailleurs dans le dépôt hors ce document (le moteur dit « couche ») ; reste du vocabulaire d'avant le renommage (la citation de la directive, ligne 6, est une pièce datée et n'est pas visée). | « en-tête      magie, version, nb_couches, nb_tenseurs, alignement (2 Mo), graine » (idem « calque » → « couche », lignes 119, 139, 167). | basse |
| docs/convertisseur.md:167 | « \| 7 \| mmap (appel système direct) \| à faire \| » | Contredit `docs/format-clusters.md:176-179` (« Le mmap : **FAIT** », 9,32 s / 6,35 Go contre 30,68 s / 19,20 Go). | « \| 7 \| mmap (appel système direct) \| **fait** \| grosses pages, partage entre processus (`docs/format-clusters.md:176`) \| » | basse |
| docs/convertisseur.md:247 | « 2. **Épinglage NUMA** : 20 % mesurés, mais `sched_setaffinity` n'est pas dans » | Le drapeau `--pin` existe et a été mesuré **perdant** (ligne 186 : « ✅ mesuré, **négatif** », et § « L'épinglage NUMA ne paie pas ») : l'item « reste à faire » est périmé. | « 2. **Épinglage NUMA** : **fait** (`--pin`), mesuré **perdant** — 23,2 → 27,6 s sur le 30B MoE (ligne 186). » | moyenne |
| docs/convertisseur.md:249 | « 3. **Q8_0 en place** pour les projections (la tête le fait déjà). » | Contredit le tableau « Ce qui est fait » du même document (ligne 187 : « Q8_0 en place (projections) ✅ — chargement 2,73 → 0,81 s, mémoire 921 → 566 Mo »). | « 3. **Q8_0 en place** pour les projections : **fait** — chargement 2,73 → 0,81 s, mémoire 921 → 566 Mo (ligne 187). » | moyenne |
| docs/convertisseur.md:250 | « 4. **gpt-oss-120b** : le routeur MoE fonctionne (top-4 sur 128) mais le modèle » | Périmé : le même document dit plus bas qu'il « charge et tourne » (5 tok/s) et c'est une porte publiée — **15,6017** à ctx 256 (`README.md:374`, `reports/rapport-routage-experts.md:66`). | « 4. **gpt-oss-120b** : **charge et tourne** (voir ci-dessous) ; porte de non-régression **15,6017** à ctx 256 — `README.md:374`. » | moyenne |
| docs/convertisseur.md:311-313 | « Les suspects restants sont donc plus fins : le facteur d'échelle de l'attention, l'ordre exact des normes, ou la rampe YaRN » | Hypothèse réfutée le jour même : le biais de `attn_output` était ignoré et la fenêtre s'appliquait à 36/36 couches — 39,80 → **20,84** à 63 jetons (`reports/rapport-gpt-oss-perplexite.md` §2.a-b). | « Les suspects restants ont été testés le jour même : biais de `attn_output` (ignoré) et fenêtre sur 36/36 couches — 39,80 → **20,84** à 63 jetons (`reports/rapport-gpt-oss-perplexite.md`). » | moyenne |
| docs/colab-reparti.md:37 | « **Débit** : 3 663 octets par flux en dense (en-tête v4 compris) » | Version de protocole périmée : le protocole courant est **v5** (modes 0-4, dont « LOT en listes ») — `docs/format-flux.md:84-89`, `drave-core/src/main.rs:1862` ; la taille d'en-tête (79 o) est inchangée, le chiffre reste bon. | « **Débit** : 3 663 octets par flux en dense (en-tête **v5** compris) » | moyenne |
| docs/colab-reparti.md:3-4 | « Objectif : deux machines qui se passent des **listes d'activation**, l'une sur le runtime Colab, l'autre en local » | Le document de transport cadre le flux comme une pure recette de fidélité ; la finalité d'analyse de la vision (vision.md:94-99) est absente des documents de format et de transport. | Ajouter après la ligne 4 : « Ce flux est aussi le **journal** qu'on relit (`--trace-flux`, `tools/analyse_flux.py`) pour comprendre le modèle et adapter l'architecture à la tâche. » | moyenne |
| docs/contexte-long.md:101 | « débit bout en bout à chiffrer » | Mesuré depuis : 17,1 → 13,6 s (−20 %) sur Qwen ctx 512 et ≈50 → 34,4 s (−31 %) sur gpt-oss ctx 256 (`reports/rapport-prefill-par-lots.md:193-194`) ; la fin de la ligne (« reste à mesurer ») est du même tonneau. | Remplacer par « débit bout en bout **mesuré** (Qwen ctx 512 : 17,1 → 13,6 s, −20 % ; gpt-oss ctx 256 : ≈50 → 34,4 s, −31 %) — `reports/rapport-prefill-par-lots.md` ». | moyenne |
| docs/contexte-long.md:102 | « mesuré : +7,1 % de perplexité (llama.cpp q8_0 : +3,1 %) » | Périmé : le même document (§4.bis) mesure **+1,5 %** à 512 et **+3,0 %** à 8 192 depuis les échelles par bloc de 32 ; « échelle par vecteur » (même ligne) ne décrit plus le code (vision.md:215-217, `REPRISE.md:179`). | « \| E2 \| **KV int8** \| **fait** (échelle **par bloc de 32**, dequantification à la lecture) \| ÷4 sur le KV ; 128 k confortable \| mesuré : **+1,5 %** à 512 jetons, **+3,0 %** à 8 192 (llama.cpp q8_0 : +0,8 %) \| » | moyenne |
| docs/contexte-long.md:103 | « mesuré : **+384 %** à 512 jetons, **+364 % à 8 192** » | Le +384 % est la mesure d'avant les échelles par bloc de 32 ; la valeur courante à 512 est **+219 %** (`REPRISE.md:180` : « était +384 % et +450 % » ; même document §4.bis). | « mesuré : **+219 %** à 512 jetons, **+364 % à 8 192** » | basse |
| docs/contexte-long.md:106 | « **non testable ici** : aucun modèle MLA en GGUF sur cette machine » | Périmé au 02/10 : MLA validée contre llama.cpp — GLM-5.3 corrélation **0,999024**, Kimi-K2.7 calculable (`reports/rapport-mla-experts.md:99-118`, `docs/plan-deepseek41-complet.md`) ; seule V4.1 reste bloquée. | « **validée** contre llama.cpp (GLM-5.3, corrélation **0,999024** ; Kimi-K2.7 calculable) — V4.1 encore bloquée (hyper-connexions, sortie à rang faible) ; `reports/rapport-mla-experts.md` » | haute |
| docs/contexte-long.md:107 | « **non testable ici sans le chemin image** : le projecteur `mmproj` est présent, mais rien ne lit les patchs » | Périmé : chaîne image complète démontrée (patchs **5,4e-7**, projecteur **1,7e-6**, une couche 1,8e-6) — `REPRISE.md:220-229`, `docs/plan-mla-vision.md`. | « **faite** : chaîne complète démontrée (patchs **5,4e-7**, projecteur **1,7e-6**) — `docs/plan-mla-vision.md` » | haute |
| docs/contexte-long.md:407-408 | « simple tant que le contexte demandé tient dans la longueur initiale déclarée (4 096 pour gpt-oss), interpolation YaRN au-delà » | Décrit l'ancienne politique : le code bascule à `ctx > original × 4` (`drave-core/src/model.rs:2198`) et le §5.quater du même document fixe le seuil à **4 ×** (16 384 pour gpt-oss). | « simple tant que le contexte demandé ne dépasse pas **4 ×** la longueur initiale déclarée (16 384 pour gpt-oss, §5.quater), interpolation YaRN au-delà » | moyenne |
| docs/contexte-long.md:545-546 | « Le test est donc **arrêté** : il faudra un remplissage varié (du vrai texte) » | Périmé : l'aiguille v2 (remplissage WikiText-2, réponses de 40 jetons, préremplissage par lots) trouve **12/12** — `reports/rapport-aiguille.md:74`, `REPRISE.md:190`. | « Le test a depuis été relancé (v2 : remplissage Wikitext-2, réponses de 40 jetons, préremplissage par lots) et **12 sondes sur 12** sont trouvées — `reports/rapport-aiguille.md` » | moyenne |
| docs/contexte-long.md:560 | « \| **top-256 clés par requête** (`--attn-topk 256`) \| **234,88** ← *meilleure* \| » | Les valeurs absolues de ce tableau ne sont pas reproduites par le binaire actuel : la vision (vision.md:79-83) et `docs/plan-gpu-topk.md:88-89,99` disent que seul l'écart A/B fait foi (ctx 2 048 : 9,4162 GPU contre 9,4167 CPU). | Ajouter après la ligne 561 : « (valeurs du 30/09, non reproduites depuis — l'écart A/B fait foi : `docs/plan-gpu-topk.md:88-89`) ». | basse |

**Ce qui est déjà cohérent et ne doit pas être touché**

- `docs/format-flux.md` : protocole **v5** et cinq modes, dont le mode 4 « LOT en listes » (l.84-120) ; les trois usages posés d'emblée (l.3-14) ; « des listes, pas des matrices » jusque sur le câble (l.133-136) ; l'avertissement sur les 39 octets d'époque (l.157-160) ; la règle de la norme finale (l.162-169).
- `docs/format-clusters.md` : porte clusters **799,8557** / 6,28 Go (l.168) conforme aux faits ; § « Le nœud partiel » et la somme des contributions manquante **entre nœuds** (l.157-173) ; ordre des experts par trace de routage mesurée (l.60-71) ; chiffres adossés à `rapport-decoupage-moe.md` et `rapport-lecteur-multifichiers.md`.
- `docs/convertisseur.md` : les résultats négatifs assumés (seuil d'abolition des zéros à 25 %, l.47-59 ; épinglage NUMA perdant, l.231-236 ; plan qui surestime les MoE d'un facteur 2, l.238-242) ; la fidélité par emprunt (l.27-33 et l.144-157) ; aucune porte périmée (Qwen 0,5B = 19,3885, l.193).
- `docs/colab-reparti.md` : les 14 champs du contrat d'activation (l.24) ; l'aveu que les deux nœuds chargent le modèle entier (l.27, 30-33) ; le critère d'écart `0,00e0` (l.22, 104-112) ; modes 3 et 4 avec leurs chiffres (l.28).
- `docs/contexte-long.md` : la campagne de placement des bits et le réglage recommandé `DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1` (l.176-210) ; §5.quater (seuil à 4 ×) ; les chiffres du noyau KV GPU (l.226-250, 299-353) ; le rappel de méthode final (l.574-580).
- Global : dans les cinq documents, **aucune porte périmée** (19,3885 et 799,8557 exacts), aucun compte de tests ni liste de formats périmés, et les renvois aux rapports sont présents partout sauf `convertisseur.md` (qui est le porteur de ses propres mesures).

**Points à trancher par l'humain**

1. **Nom du conteneur `QTNT`** : le renommer (quel nom ? le document ne doit pas inventer d'acronyme) ou supprimer la section au profit du format de flux `DRVF` — décision de nommage, pas de contenu.
2. **Tableaux « Ordre de marche » / « Reste à faire » de `convertisseur.md`** (daté du 28/09) : à garder comme journal daté ou à mettre à jour ? Les constats mmap / NUMA / Q8_0 / gpt-oss en découlent.
3. **Séries KV canoniques** : `contexte-long.md` porte côte à côte les mesures « par vecteur » (§4.bis, tableau E) et « par bloc de 32 » (§4.bis.3) — choisir la série qui fait référence dans le tableau E.
4. **DRVF et les deux cas de la vision** (vision.md:202-211) : faut-il spécifier dans le format le cas général « connexion pondérée » et le cas trinaire « deux listes » (le signe porté par l'appartenance), aujourd'hui absents du document de format ?
5. **Hors des cinq documents (code)** : le commentaire `drave-core/src/model.rs:1518-1519` dit que le croisement push/pull est à « 10 % de densité » (repris par `tools/analyse_flux.py`) alors que `seuil_push = 0.22` (model.rs:2621) et que le rapport/la vision disent **~22 %** — à aligner.

Note de méthode : `docs/vision.md` a été modifié pendant l'audit (02/10, 09:59) ; je me suis recalé sur sa version courante (v5, gpt-oss 15,6017, finalité d'analyse l.94-99, connexion pondérée/trinaire l.202-211) et aucun des cinq documents audités n'a bougé pendant l'audit. Rapport transmis au parent (`bbd6969f-0f70-42b2-8951-64d1f2f36d2e`).

