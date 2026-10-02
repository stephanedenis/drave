# Session DSH — relecture

- identifiant : `8b315bb2-abba-4033-b3d4-177d04b4f194`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-02 09:51:51
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu es relecteur ADVERSE. Tu ne modifies AUCUN fichier : tu produis un rapport de constats, avec citations exactes et numéros de ligne.

Contexte : le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet contient un moteur d'inférence nommé **Drave**. Sa vision est définie dans `docs/vision.md` et `docs/programme-recherche.md` — lis-les ENTIER d'abord, ce sont les textes de référence.

Résumé de la vision à faire respecter :
- Drave n'est PAS un moteur qui lit des matrices : c'est un moteur qui **conduit un flux de listes d'activation** (AER, « push »). Le coût suit l'ACTIVITÉ, pas la taille du modèle.
- Encodages : listes valuées **par source** (échelle par bloc de 32) ; **deux listes** (trinaire : le signe est porté par l'appartenance à la liste des « + » ou des « − », plus de valeur stockée) ; cas général : **connexions pondérées** (source → destination, poids).
- Le cœur du projet est de **router ces flux sur des grappes de neurones** réparties entre composants (CPU, GPU, FPGA) et entre **machines**.
- Le flux est aussi un **journal** : tracer, rejouer, comparer, transporter — et il sert à **analyser le comportement du modèle pour adapter l'architecture à la tâche**.
- Le chemin dense existe et gagne au-dessus d'environ 22 % de densité (mesuré) : la vision ne prétend pas que le sparse gagne toujours.
- Chaque chiffre publié doit avoir sa source ; une erreur ou un échec se documente au lieu de disparaître.

Faits À JOUR au 02/10/2026 (si un document dit autre chose, c'est une incohérence à signaler) :
- la porte gpt-oss ctx 256 vaut **15,6017** (elle valait 15,1757 avant le 02/10 : le biais du routeur était mis dans le softmax des poids) ;
- la porte Qwen2.5-0.5B ctx 256 vaut **19,3885** ; Qwen3-30B en clusters **799,8557** ; `cargo test --release` = **48 tests** ;
- le protocole de transport des flux est en **v5** (et non v4) ;
- 18 formats sont lisibles, dont IQ1_S/IQ1_M/IQ2_XXS/IQ3_XXS/IQ4_XS/Q3_K/Q5_K/Q5_0, tous vérifiés contre libggml (`tools/portes_formats.sh`) ;
- l'attention MLA à rang faible est implémentée et validée contre llama.cpp sur GLM-5.3 (corrélation 0,999024) ; GLM-5.3 et Kimi-K2.7 se calculent ; DeepSeek-V4.1 ne se calcule pas encore (hyper-connexions, sortie à rang faible, dé-rotation+puits, attentions compressées CSA/HCA) ;
- llama.cpp ne connaît PAS l'architecture `deepseek41` ; il exécute `deepseek4` (V4-Flash) ;
- le plan du chantier V4.1 est `docs/plan-deepseek41-complet.md`, écrit « les flux d'abord ».

DOCUMENTS À AUDITER (lis-les en entier) :
1. docs/vision.md
2. docs/roadmap.md
3. docs/programme-recherche.md
4. docs/sprints.md
5. docs/histoire.md

Ce que tu cherches, par ordre d'importance :
1. **Contradictions internes ou entre documents** (exemple connu : `vision.md` §8 dit de l'axe « répartir sur machines » qu'il n'y a « rien », alors que son §4 dit que le transport existe et que c'est l'axe le plus avancé — vérifie et signale toute contradiction de ce genre).
2. **Chiffres périmés** par rapport à la liste ci-dessus (portes, nombre de tests, version de protocole, formats).
3. **Cadrage qui dilue la vision** : un passage qui présente Drave comme « un moteur d'inférence local rapide », comme « une alternative à llama.cpp », ou qui fait du dense la référence de valeur.
4. **Absence de la dimension grappes/machines** dans un document qui décrit pourtant le but du moteur.
5. **Absence de la finalité d'analyse** (les flux servent à comprendre le modèle et adapter l'architecture à la tâche).
6. **Affirmations non sourcées** (un chiffre sans renvoi à un rapport ou à un fichier).

Format de sortie, strictement : un tableau markdown

| fichier:ligne | citation exacte (≤ 25 mots) | problème | correction minimale proposée (texte de remplacement exact) | gravité |

puis, sous le tableau, une liste courte « ce qui est déjà cohérent et ne doit pas être touché » (pour éviter qu'une révision ultérieure abîme ce qui va bien), et une liste « points à trancher par l'humain » s'il y en a.

Règles : ne propose QUE des corrections minimales (remplacer une phrase, corriger un chiffre, ajouter une phrase de cadrage) — pas de réécriture de document. Ne signale pas de faux positifs : cite la ligne exacte. Si un document est cohérent, dis-le en une ligne. Maximum 25 constats au total.
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

⏵ Reading the five reference documents in full before auditing.

- **bash** `{"command": "wc -l docs/vision.md docs/roadmap.md docs/programme-recherche.md docs/sprints.md docs/histoire.md 2>&1", "description": "Count lines of documents to audit", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
247 docs/vision.md
  309 docs/roadmap.md
  212 docs/programme-recherche.md
   74 docs/sprints.md
   78 docs/histoire.md
  920 total
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

⏵ Reading roadmap, programme-recherche, sprints and histoire in full.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/roadmap.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/programme-recherche.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/roadmap.md</path>
<type>file</type>
<content>
1: # Roadmap
2: 
3: > Suite de [`docs/vision.md`](vision.md). Cinq phases, de ce qui se fait **tout de
4: > suite sur cette machine** à ce qui demande une infra (Colab, FPGA). Chaque
5: > phase a un critère de succès **mesurable**, et l'état de chaque chantier est
6: > marqué : ✅ fait · 🔬 en cours · ⏳ à faire · 🧱 bloqué par une infra absente.
7: 
8: ## Phase 0 — La drave observable (aucune infra)
9: 
10: **Objectif** : faire du flux de listes un objet de première classe, qu'on
11: enregistre et qu'on compare. Sans cela, tout le reste se débugue à l'aveugle.
12: 
13: | # | chantier | état | critère de succès |
14: |---|---|---|---|
15: | 0.1 | **Format de trace du flux** : par (couche, position), la liste des neurones actifs (indice + valeur), l'échelle, le nombre | ✅ | écrit et relu sans perte ; **132 Mo pour 512 jetons** (258 ko/jeton), **+8 % de temps** — mesuré |
16: | 0.2 | **Diff par couche** (`tools/diff_flux.py`) : où deux exécutions divergent, à quel jeton, quels neurones | ✅ | démontré : KV f32 contre int8 → première divergence **couche 1, jeton 0**, 896 neurones, 2,9e-
… [21857 caractères tronqués]
  ```


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

### 🤖 Assistant

⏵ Reading sprints and histoire, then cross-checking facts against the repo.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/sprints.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/histoire.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/sprints.md</path>
<type>file</type>
<content>
1: # Les sprints de 2 h — charte
2: 
3: Ce document dit **comment on travaille**, pas ce qu'on fait (ça, c'est
4: `docs/roadmap.md` et les sprints eux-mêmes, dans `sprints/`).
5: 
6: ## Le boxing
7: 
8: Un sprint dure **2 h**, chronométrées (`tools/sprint.sh`, qui lit l'heure du
9: système — pas une estimation). Le temps est réel : quand la boîte est pleine, on
10: s'arrête, même si la dernière chose est presque finie. Ce qui reste va au planning
11: du sprint suivant, écrit noir sur blanc.
12: 
13: ```bash
14: tools/sprint.sh start "l'objectif, en une phrase mesurable"
15: tools/sprint.sh status     # à chaque itération : temps restant, commits du sprint
16: tools/sprint.sh close      # écrit la trame de cérémonie dans sprints/NN-*.md
17: ```
18: 
19: ## La cérémonie, APRÈS la boîte
20: 
21: Trois parties, dans cet ordre, écrites dans le fichier du sprint :
22: 
23: 1. **Revue** — ce qui est livré, avec les chiffres mesurés. Pas d'intention : des
24:    résultats, et pour chacun le rapport ou la commande qui le porte. Ce qui n'est
25:    pas fini est dit comme tel (un demi-chan
… [2611 caractères tronqués]
  ```


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

⏵ Verifying the stale figures against reports, scripts and code in the repo.

- **bash** `{"command": "ls docs/ ; echo \"---- plan41 ----\"; ls -la docs/plan-deepseek41-complet.md 2>&1; echo \"---- reports ----\"; ls reports/ 2>&1 | head -60", "description": "List docs and reports", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

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
---- plan41 ----
-rw-------. 1 stephane stephane 17742  2 oct 09:17 docs/plan-deepseek41-complet.md
---- reports ----
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
rapport-encodage.md
rapport-eparsite.md
rapport-execution-v41.md
rapport-gpt-oss-perplexite.md
rapport-gpu-scores.md
rapport-gpu-topk-selection.md
rapport-grappes.md
rapport-greffon.md
rapport-harnais.md
rapport-inference.md
rapport-lecteur-m
… [682 caractères tronqués]
  ```

- **grep** `{"pattern": "15,6017|15\\.6017|15,1757|15\\.1757|19,3885|19\\.3885|799,8557|799\\.8557", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
Found 250 of 699 matches

docs/plan-deepseek41-complet.md
Line 17: | **listes d'activation** | `(indice, valeur)` par vecteur, encodage DRVF v1/v2/v3 ; v2 = **3 octets par neurone actif** | trace dense 512 jetons : 66,4 Mo, rejeu **identique** (19,3885) |
Line 200:   4. les portes du dépôt vertes (48 tests, Qwen 19,3885, clusters 799,8557,

docs/format-clusters.md
Line 168:   | 8 | **799,8557** | 6,28 Go |
Line 173:   799,8557 pour 4,60 Go chacun — moins que les 6,28 Go d'un nœud complet.

docs/sprints.md
Line 38: - les portes de non-régression sont intactes : **Qwen ctx 256 = 19,3885**,
Line 39:   gpt-oss ctx 256 = **15,1757** (sans `DRAVE_GPU`), et le banc réparti donne

docs/plan-gpu-topk.md
Line 96: | 6 | porte de non-régression : les deux valeurs restent 19,3885 et 15,1757 | ✅ **inchangées**, mesurées sur le binaire final : Qwen 19,3885 (CPU **et** avec `DRAVE_GPU_KV`) · gpt-oss 15,1757 (CPU) et 15,1667 (`DRAVE_GPU`) · `cargo test` 17/17 |

docs/format-flux.md
Line 48: | rejeu (`--flux-forcer`) | 19,3885 | **19,3885 — identique** |
Line 59: | rejeu `--flux-forcer` | 19,3885 | **19,4029 (+0,074 %)** |
Line 176: | un rejeu redonne le même résultat | `--flux-forcer` : perplexité 
… [39272 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Cross-checking each figure in the five docs against reports and code.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"=== 17,9 / localite ===\"; grep -rn \"17,9\\|17\\.9\" reports/rapport-localite-activation.md reports/rapport-analyse-flux.md 2>/dev/null | head -20\necho \"=== 33,1 ===\"; grep -rln \"33,1\" reports/ | head\necho \"=== 0,08 chau … [309 caractères tronqués]`

  ```
=== 17,9 / localite ===
reports/rapport-localite-activation.md:43:| densité d'activation (seuil 5 % du max) | **17,9 %** des neurones par jeton (82 % ne font rien) |
=== 33,1 ===
reports/rapport-localite-activation.md
reports/rapport-prefill-par-lots.md
reports/rapport-compacite-trace.md
reports/rapport-coherence-docs.md
reports/rapport-architecture-memoire.md
reports/rapport-optimisations-auto.md
=== 0,08 chauds ===
reports/rapport-analyse-flux.md:32:et c'est cohérent avec la mesure d'activation du projet (0,08 % « chauds » plus
reports/rapport-architecture-memoire.md:374:| **DeepSeek-V4.1-Flash** | **365,70 Go** | **0,08 s** | **47 Mo** |
reports/rapport-compacite-trace.md:17:> valeur de **0,085 % RMS** du max de la liste — la prévision de ce rapport était
reports/rapport-compacite-trace.md:18:> 0,077-0,081 %, elle tient. La v3 est avec perte, donc la v2 reste le défaut.
reports/rapport-compacite-trace.md:193:   pour une erreur RMS de 0,08 % du max de la liste. Le seuil, lui, reste global :
reports/rapport-compacite-trace.md:236:   **normée** ; l'erreur mesurée ici (0,08 % du max) plaide pour, mais c'est le
reports/rapport-empreinte-memoire.md:138:| Jaccard | **0,499** | 0,088 | 
… [3091 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"=== 1,2 Mo ===\"; grep -rn \"1,2 Mo\\|1.2 Mo\\|258 ko\\|ko/jeton\" reports/*.md docs/*.md | head -20\necho \"=== +3,0 % journalisation ===\"; grep -rn \"journalisation\\|Journalisation\" reports/*.md docs/*.md | head -20\necho \ … [334 caractères tronqués]`

  ```
=== 1,2 Mo ===
reports/rapport-capteur-hebbien.md:34:sa copie coûte 7 Ko par matrice, 1,2 Mo par token, soit 19 Mo/s à 15,8 tok/s.
reports/rapport-coherence-docs.md:97:| 41 | `docs/roadmap.md:107` | trace 512 jetons = « **12 288 listes** · 132 Mo · 6 octets par neurone actif » | 24 576 listes pour 512 jetons × 24 couches × 2 points ; 12 288 = la valeur pour **256 jetons** | PÉRIMÉ |
reports/rapport-compacite-trace.md:61:Ce sont les deux traces citées par le projet (« 132 Mo pour 512 jetons, 53 Mo en
reports/rapport-compacite-trace.md:129:## 5. La trace dense (132 Mo, 512 jetons)
reports/rapport-compacite-trace.md:154:   pas un artefact d'échantillon. Les 132 Mo de i16/u32 peu corrélés ne
reports/rapport-compacite-trace.md:221:* **La sentinelle 0xFFFF et la lecture des traces v1.** Les 132 Mo et 53 Mo
reports/rapport-inference.md:301:1,2 Mo d'accumulateurs, qui débordent le cache L2 de chaque cœur : chaque écriture
reports/rapport-programme-evolutif.md:19:| Journal des activations de toutes les couches (24) | ~1,2 Mo/token, soit 19 Mo/s à 15,8 tok/s |
reports/rapport-programme-evolutif.md:23:les *listes d'activations* suffit à rejouer intégralement le calcul. 1,2 Mo/token
docs/forma
… [2389 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking version strings, clusters, MLA validation and "analysis purpose" wording.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"=== versions in the 5 docs ===\"; grep -n \"version\\|protocole\\| v1\\| v2\\| v3\\| v4\\| v5\" docs/vision.md docs/roadmap.md docs/programme-recherche.md docs/sprints.md docs/histoire.md\necho \"=== grappe/machine/reparti in 5  … [684 caractères tronqués]`

  ```
=== versions in the 5 docs ===
docs/vision.md:87:diffuser et comparer entre deux versions d'un modèle ou deux configurations du
docs/vision.md:121:Deux processus se passent des flux (protocole v4 : version, modes dense / listes /
docs/vision.md:136:   versionné ;
docs/vision.md:243:La table de conversion des anciens noms — variables `QT_*`, chemins — est dans
docs/roadmap.md:17:| 0.3 | **Le format EST le contrat d'échange** (phase 3) : versionné, en-tête + paires | ✅ | codec de référence (`tools/flux_codec.py`) : aller-retour **identique** sur 132 Mo ; **et le rejeu dans le moteur redonne les mêmes logits** (`--flux-forcer`) |
docs/roadmap.md:55:| 3.1 | **Contrat d'échange v1** : tranche de liste = en-tête (couche, source, échelle, bits) + paires (destination, valeur) | ✅ | format écrit, relu, rejoué sans perte (phase 0.3/0.3bis) ; **transport TCP en place et FIDÈLE** (`--flux-serveur`, `--ppl-reparti`) — écart local/réparti **0,00e0** sur 40 et 200 jetons (39 et 199 flux : le dernier n'a rien à prédire), après correction de deux défauts (plage de couches ignorée par `forward`, norme finale appliquée deux fois) |
docs/roadmap.md:59:| 3.5 | **Sûreté** : version du format, refus des 
… [6827 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"=== portes.sh ===\"; cat tools/portes.sh 2>/dev/null | head -60\necho \"=== gpt-oss 15,6017 source ===\"; grep -rn \"15,6017\" reports/*.md REPRISE.md | head -20\necho \"=== portes_formats ===\"; ls tools/portes_formats.sh && gr … [136 caractères tronqués]`

  ```
=== portes.sh ===
#!/bin/bash
# Les portes du dépôt, en une commande.
#
# Un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien :
# chaque porte est comparée à la valeur ATTENDUE, et le script sort en erreur si
# l'une diverge. Les valeurs sont celles publiées dans les rapports.
#
#   tools/portes.sh            toutes les portes
#   tools/portes.sh rapide     sans gpt-oss (le seul qui prenne ~20 min)

set -u
cd "$(dirname "$0")/.."
D=./drave-core/target/release/drave
RAPIDE=${1:-}
ECHEC=0

[ -x "$D" ] || { echo "compiler d'abord : (cd drave-core && cargo build --release)"; exit 2; }

compare() {  # nom, attendu, obtenu
    if [ "$2" = "$3" ]; then
        printf "  %-42s %s  ✅\n" "$1" "$3"
    else
        printf "  %-42s %s  ❌ (attendu %s)\n" "$1" "${3:-—}" "$2"
        ECHEC=1
    fi
}

# Attention : le moteur affiche AUSSI une perplexité cumulée par fenêtre, avant
# le total. Prendre la première occurrence du motif donnait 17,431 (fenêtre 1) au
# lieu de 19,3885 (total) — un instrument faux qui accuse le code.
valeur() { grep -oE "=== perplexité [0-9]+\.[0-9]+" | grep -oE "[0-9]+\.[0-9]+" | head -1; }

echo "=== Portes ==="

# 1. Tests unitaires.
n=$( (cd dra
… [2518 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the reports behind the vision tables and the density figures.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"=== rapport-analyse-flux density ===\"; grep -n \"densité\\|%\\|56\\|20 \" reports/rapport-analyse-flux.md | head -40", "description": "Read density figures in analyse-flux report"}`

  ```
=== rapport-analyse-flux density ===
7:Modèle : Qwen2.5-0.5B Q8_0, contexte 256, 256 jetons, 24 couches, 896 cachés,
14:Le croisement push/pull du projet est mesuré à **~10 % de densité**. Ce qui
15:manquait était la densité **par couche** — or elle varie du simple au triple :
17:| couche | densité | couche | densité |
19:| **9** | **20,1 %** | 6 | 40,5 % |
20:| 0 | 25,9 % | 5 | 45,6 % |
21:| 4 | 26,7 % | **1** | **56,3 %** |
22:| 3 | 28,8 % | 8 | 29,2 % |
30:Neurones actifs dans au moins 90 % des jetons, par couche : **0,89 % à 1,90 %**
32:et c'est cohérent avec la mesure d'activation du projet (0,08 % « chauds » plus
33:de 90 % du temps sur un autre modèle et un autre seuil).
37:Par couche, les **10 % de neurones les plus forts portent 26 % à 67 %** de la
38:magnitude, et le 1 % le plus fort en porte 5 % à 16 %. La couche 9 est la plus
39:concentrée (67 % pour 10 %), la couche 1 la moins (26 %) — et c'est aussi la plus
46:**28 % à 86 %**. Les couches 5 à 8 se partagent 84-86 % de leurs neurones
48:partage que 28 %.
56:Le croisement push/pull mesuré du projet est à ~10 % de densité. Avec les densités
59:| couche (densité) | régime attendu | raison |
61:| 9 (20,1 %), 0 (25,9 %), 4 
… [280 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"=== 968 / 13,2 ===\"; grep -rn \"968\\|13,2 ms\" reports/*.md | head -10\necho \"=== 22,16 / 3,29 ===\"; grep -rn \"22,16\\|3,29\" reports/*.md | head -10\necho \"=== 15,6 / 6,2 tête ===\"; grep -rn \"15,6 →\\|15,6 à\\|6,2 ms\"  … [347 caractères tronqués]`

  ```
=== 968 / 13,2 ===
reports/rapport-coherence-docs-2.md:135:| 66 | `docs/plan-gpu-topk.md` (apparu pendant l'audit) | ×73 pour le KV en VRAM, 968 ms CPU, 1,99e-7, 12,4 → 12,5 ms en top-k CPU | ces chiffres sont ceux de `REPRISE.md:163-164,184,224` et de la mesure GPU du jour ; rien de contradictoire relevé | OK |
reports/rapport-gpu-topk-selection.md:344:| 5 | mesure 1 M de clés : ms/couche avec et sans top-k | ✅ **fait au niveau des noyaux** : chaîne complète **3,90 ms** pour 14 lignes × 1 M clés contre 539,9 ms d'attention complète CPU (×138) et 13,2 ms en VRAM (0,3× le complet, critère 2×) |
reports/rapport-session-2026-09-30.md:19:| **Plan du noyau GPU de top-k** | chiffré : le mode creux retombe sur le CPU (968 ms par couche à 1 M contre 13,2 ms avec le miroir VRAM) — le prochain chantier, écrit et non bâclé | `plan-gpu-topk.md` |
=== 22,16 / 3,29 ===
=== 15,6 / 6,2 tête ===
reports/rapport-prefill-par-lots.md:137:   le déport GPU (`DRAVE_GPU_TETE=1`, déjà mesuré à 6,2 ms/jeton contre 15,6 pour
=== 7,58 / 3,60 ===
=== 25,77 ===
=== 13,6 / 7,0 ms / 308 Go/s ===
reports/rapport-capteur-hebbien.md:8:création de nœuds par Hebb n'ajoute rien sur 69 % des poids du modèle, pour une
re
… [485 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Pinning down the crossing figure and remaining vision-table sources.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"=== croisement 22 ===\"; grep -rn \"croisement\" reports/rapport-croisement-push-pull.md | head -20\necho \"=== 3,29 / 22,1 ===\"; grep -rn \"3,29\\|22,1\\|×6,7\\|2,8\" reports/rapport-*.md | grep -i \"attention\\|préremplissage … [182 caractères tronqués]`

  ```
=== croisement 22 ===
15:> ⚠️ **Corrigé le 27/09** : le tableau de croisement de la section 1 mesurait
24:## 1. Le croisement
52:| fait mesuré | densité d'activation | côté du croisement |
60:d'activation.** Un LLM dense se place exactement du mauvais côté du croisement,
110:   accumulateur en BRAM, dispersion dans un banc privé. Le croisement y est
124:# le croisement
=== 3,29 / 22,1 ===
reports/rapport-coherence-docs.md:55:| 9 | `docs/plan-prefill-reparti.md:14,22,103` | « `VERSION_FLUX` vaut encore **2** », « la version change : 2 → 3 » | 3 (le plan décrit un travail déjà fait) | PÉRIMÉ |
reports/rapport-mla-experts.md:97:  61 couches MLA, routage sigmoïde ×2,827, 384 experts dont 8 par jeton.
=== 25,77 / 0,03 ===
reports/bilan-multi-materiel.md:8:RTX 5000 (16 Go, NVLink 25,78 Go/s), 1 carte Stratix V GS (Storey Peak,
reports/bilan-multi-materiel.md:97:| « Le FPGA n'a pas NVLink / les RTX 5000 non plus » | **Corrigée** — l'utilisateur avait raison, 25,78 Go/s mesurés par lien |
reports/rapport-architecture-memoire.md:224:| **GPU 0 ↔ GPU 1** | | | **NVLink, 25,78 Go/s** |
reports/rapport-architecture-memoire.md:226:**Le NVLink est là, et il vaut 2× le PCIe** (25,78 contre ~12 Go/
… [622 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"=== prior audit of these docs ===\"; grep -n \"vision.md\\|roadmap.md\\|programme-recherche.md\\|sprints.md\\|histoire.md\" reports/rapport-coherence-docs-2.md | head -40\necho; echo \"=== 5,3 G ev/s ===\"; grep -rn \"5,3 G\\|5, … [302 caractères tronqués]`

  ```
=== prior audit of these docs ===
52:| 3 | `REPRISE.md:284-291`, `docs/roadmap.md:94-97`, `docs/vision.md:121`, `docs/colab-reparti.md:23-24` | protocole v4, quatre modes, version dans chaque en-tête | conforme au code | OK |
76:| 22 | `docs/roadmap.md:56` | critère 3.2 : « **3 623 → 1 589** octets par flux (÷2,3) pour 1,3 % d'écart à 1 024 jetons » | avec l'en-tête v4 : **3 663 → 1 629** ; le ÷2,3 et le 1,3 % restent vrais, mais ce sont les chiffres d'avant les top-k | PÉRIMÉ |
77:| 23 | `docs/roadmap.md:254-266` | tableaux : dense 3 623 · listes 0,00 = 3 622 · listes 0,05 = 897 · blocs 2 268 → 1 568 | valeurs de l'époque des 39 octets, non datées, alors que le même document dit 79 octets « aujourd'hui » (`:96`, `:112`) et que `docs/format-flux.md:145-148` met justement en garde contre la comparaison de deux époques | CONTRADICTOIRE |
81:| 27 | `docs/format-flux.md:47`, `reports/rapport-compacite-trace.md:4-5`, `docs/roadmap.md:108` | trace dense 512 jetons : 132 396 736 → **66 370 408** (−49,87 %) | cohérent partout (le rapport explique les 2 octets de sentinelle, `:75`, `:134`) | OK |
82:| 28 | `docs/format-flux.md:58-61`, `REPRISE.md:248,340-341`, `docs/roadmap.md:94` | v3 : **
… [4270 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Locating exact report sources for the unsourced figures in vision.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nfor n in \"22,16\" \"3,29 ms\" \"7,58\" \"3,60 ms\" \"25,77\" \"968\" \"13,6 → 7,0\" \"308 Go/s\" \"+1,5 %\" \"364\" \"33,1\" \"7,79 G\" \"×2,8\"; do\n  echo \"=== $n ===\"; grep -rn --exclude-dir=journal --exclude-dir=.git -- \"$n\" r … [116 caractères tronqués]`

  ```
=== 22,16 ===
docs/contexte-long.md:287:| 4 096 | CPU | 12,2177 | **22,16** | 219,4 s |
docs/vision.md:100:| attention complète | noyau GPU, décodage **et** préremplissage | 22,16 → **3,29 ms/jeton** (÷6,7) ; préremplissage **×2,8** |
REPRISE.md:185:| KV déporté dans le moteur (`DRAVE_GPU_KV=1`, ctx 4 096) | attention **22,16 → 3,29 ms/jeton** (÷6,7) · balayage 219,4 → **136,2 s** · perplexité 12,2177 → 12,2175 |
=== 3,29 ms ===
docs/vision.md:100:| attention complète | noyau GPU, décodage **et** préremplissage | 22,16 → **3,29 ms/jeton** (÷6,7) ; préremplissage **×2,8** |
REPRISE.md:185:| KV déporté dans le moteur (`DRAVE_GPU_KV=1`, ctx 4 096) | attention **22,16 → 3,29 ms/jeton** (÷6,7) · balayage 219,4 → **136,2 s** · perplexité 12,2177 → 12,2175 |
=== 7,58 ===
docs/vision.md:102:| tête Q6_K | GPU | 7,58 → **3,60 ms/jeton** |
REPRISE.md:162:| 7 | noyaux GPU | **fait, quatre formats** | warp par ligne : tête **Q8_0** (1,6 ms contre 7,3 CPU, écart 2e-7), **MXFP4** (0,1 ms, écart **0,00e0** — bit à bit), **Q4_K** (0,5 contre 1,2 ms, 4e-7), **Q6_K** (3,6 contre 8,3 ms sur la tête liée de 191 Mo, 3,3e-7 ; ×5 sur un tenseur de 11 Mo). **Tête Q6_K branchée** dans le moteur : `DRAVE_GPU
… [6929 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"=== FPGA link exists? ===\"; ls -la ../FPGA-Stratix-V/docs/rapport-pe-evenementiel.md 2>&1 | head -3\necho \"=== +6 % experts ===\"; grep -rn --exclude-dir=journal \"6 %\" reports/*.md | grep -i \"expert\" | head -8\necho \"===  … [444 caractères tronqués]`

  ```
=== FPGA link exists? ===
-rw-------. 1 stephane stephane 7517 26 sep 08:10 ../FPGA-Stratix-V/docs/rapport-pe-evenementiel.md
=== +6 % experts ===
reports/rapport-architecture-memoire.md:427:  384 experts et top-6 (rapport 1,6 % au lieu de 6,25 %) — la concentration y est
reports/rapport-empreinte-memoire.md:8:non pas en découpant les experts mais parce que **56 % du modèle (203 Go) est une
reports/rapport-empreinte-memoire.md:507:experts, mais parce que **56 % du modèle est une table creuse par nature** que
=== 15,8 tok/s / 24,90 ===
reports/rapport-inference.md:66:| numpy float32 (OpenBLAS) | 25,0004 |
reports/rapport-inference.md:251:| **Perplexité WikiText-2** | **24,90** | **27,83** | **+12 %** |
reports/bilan-multi-materiel.md:103:15,8 tok/s sur un 0,5 B quantifié, en arithmétique entière, sans BLAS, sans GPU,
reports/rapport-attention-creuse.md:30:| 8 | 24,9071 (+5,5 %) | — | — |
reports/rapport-capteur-hebbien.md:34:sa copie coûte 7 Ko par matrice, 1,2 Mo par token, soit 19 Mo/s à 15,8 tok/s.
reports/rapport-coherence-docs.md:114:| 53 | `README.md:388` | perplexité WikiText-2 : 24,90 contre 25,00 numpy | `rapport-inference.md:66,251` : 24,90 contre 25,0004 | OK |
reports/ra
… [1481 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking the gates script, the top-k claim, and the "analysis purpose" wording.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"=== portes.sh rest ===\"; sed -n '60,140p' tools/portes.sh", "description": "Read rest of gates script"}`

  ```
=== portes.sh rest ===
# 5. Portes de FORMATS : chaque déquantificateur contre libggml.
if [ "$RAPIDE" = "rapide" ]; then
    echo "  (portes de formats : ignorées en mode rapide)"
else
    if command -v gcc >/dev/null && [ -f tools/portes_formats.sh ]; then
        r=$(timeout 1800 bash tools/portes_formats.sh 2>&1 | tail -1)
        case "$r" in
            *"0 divergence(s), 0 absent(s)"*)
                printf "  %-42s %s  ✅\n" "formats contre libggml" "${r#formats : }" ;;
            *)  printf "  %-42s %s  ❌\n" "formats contre libggml" "$r"; ECHEC=1 ;;
        esac
    fi
fi

# 6. Convention de routage annoncée : elle doit correspondre à ce que le GGUF
#    déclare. C'est la porte qui manquait quand quatre modèles sur cinq étaient
#    routés avec la convention d'un cinquième.
route() {  # nom, modele, motif attendu
    [ -f "$2" ] || { printf "  %-42s %s\n" "$1" "absent"; return; }
    v=$($D "$2" --config 2>/dev/null | grep -oE "routage +: .*" | head -1)
    case "$v" in
        *"$3"*) printf "  %-42s %s  ✅\n" "$1" "$3" ;;
        *)      printf "  %-42s %s  ❌ (attendu %s)\n" "$1" "${v:-—}" "$3"; ECHEC=1 ;;
    esac
}
M=/home/stephane/Data13TB/stephane/modeles/gguf
route 
… [755 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"=== plan-gpu-topk 80-100 ===\"; sed -n '80,100p' docs/plan-gpu-topk.md\necho \"=== contexte-long 550-565 ===\"; sed -n '552,565p' docs/contexte-long.md\necho \"=== 'à la tâche' / adapter ===\"; grep -rn --exclude-dir=journal --e … [133 caractères tronqués]`

  ```
=== plan-gpu-topk 80-100 ===
2. **la sortie** : écart max relatif sur le vecteur d'attention, attendu ≤ 1e-6
   hors ex æquo.

Puis, à l'échelle du modèle : la perplexité de `--attn-topk 256` à contexte 2 048
doit rester **234,88** (la valeur CPU mesurée) à la tolérance près, et le banc 1 M
doit montrer l'effet cherché : **968 ms → quelques dizaines de ms par couche**.

## Le plan, en étapes

| # | étape | critère de succès |
|---|---|---|
| 1 | `attn_scores` + FFI + banc `--banc-topk` sur 4 k de contexte | ✅ **fait** : écart **1,6 à 2,3e-7** de 4 096 à 262 144 clés (clés distinctes — la valeur de 1,03e-7 venait d'un banc dégénéré), **26,7 à 40× plus rapide** que le CPU ; c'est la re-mesure du 30/09 au soir qui fait foi dans `reports/rapport-gpu-scores.md` |
| 2 | `attn_topk_select` (radix, 3 noyaux) | ✅ **fait** : ensemble retenu identique au CPU, 14/14 lignes (différence symétrique 0) — `reports/rapport-gpu-topk-selection.md` |
| 3 | `attn_topk_somme` (softmax sur k + puits) | ✅ **fait** : 1,0–4,8e-7 à toutes les tailles (critère 1e-6) — `reports/rapport-gpu-topk-selection.md` |
| 4 | branchement dans `model.rs` (autoriser le GPU quand `attn_topk > 0` **et** que le noyau rend `tr
… [2351 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Final checks: GPU model, formats, and the memory-margin source.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"=== Quadro vs RTX ===\"; grep -rn --exclude-dir=journal \"Quadro\\|RTX 5000\\|RTX\" docs/vision.md docs/roadmap.md docs/programme-recherche.md docs/sprints.md docs/histoire.md REPRISE.md scripts 2>/dev/null | head -15\necho \"== … [351 caractères tronqués]`

  ```
=== Quadro vs RTX ===
docs/vision.md:184:pour **trois matériels** (SIMD x86, PTX sur Quadro, logique FPGA).
REPRISE.md:611:   demande du travail GPU *neuf* ; les deux Quadro sont libres et le cadre existe
=== formats in 5 docs ===
docs/vision.md:86:un format de trace stable, par couche et par neurone, qu'on puisse rejouer,
docs/vision.md:173:Ce que cela demande : un format de trace stable, un coût d'écriture acceptable
docs/vision.md:181:La représentation par listes valuées impose ses formats, et ils sont déjà là :
docs/vision.md:193:  format est bien lu, la mémoire cesse d'être le mur ;
docs/vision.md:220:| **1. Observer/régler par neurone** | outils en place, mesures faites | format de trace stable + diff par couche |
docs/vision.md:224:| **5. Formats/matériels/énergie** | trois matériels, formats au point | politique de quantification par bloc *choisie* par la mesure, pas par défaut |
docs/roadmap.md:17:| 0.3 | **Le format EST le contrat d'échange** (phase 3) : versionné, en-tête + paires | ✅ | codec de référence (`tools/flux_codec.py`) : aller-retour **identique** sur 132 Mo ; **et le rejeu dans le moteur redonne les mêmes logits** (`--flux-forcer`) |
docs/roadmap.md:50:entre l
… [2739 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"=== plan41 head ===\"; sed -n '1,40p' docs/plan-deepseek41-complet.md\necho \"=== REPRISE gates ===\"; sed -n '995,1010p' REPRISE.md", "description": "Read V4.1 plan intro and gate list"}`

  ```
=== plan41 head ===
# Plan — exécuter DeepSeek-V4.1 **dans** Drave : les flux d'abord

**État au 02/10 10h00.** Version 2 de ce plan. La première version traitait le
sujet comme « faire passer le forward de V4.1 » — c'est-à-dire comme llama.cpp.
C'était une erreur de cadre : la raison d'être de Drave n'est pas de recalculer un
forward dense, c'est de **conduire des listes d'activation** sur des **grappes de
neurones** qui peuvent vivre sur des composants ou des machines différentes, et de
**lire ces flux** pour comprendre et adapter le modèle. Ce plan est réécrit
là-dessus : la conformité à llama.cpp devient une *porte de correction*, pas le but.

---

## 1. Ce que Drave fait, et que ce plan doit préserver

| pilier | ce que c'est dans le dépôt | mesure |
|---|---|---|
| **listes d'activation** | `(indice, valeur)` par vecteur, encodage DRVF v1/v2/v3 ; v2 = **3 octets par neurone actif** | trace dense 512 jetons : 66,4 Mo, rejeu **identique** (19,3885) |
| **deux listes (trinaire)** | le signe porté par l'appartenance à la liste des « + » ou des « − » : plus de valeur à stocker | `reports/rapport-encodage.md`, `rapport-optimisations.md` |
| **connexions pondérées** | le cas général
… [2374 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying every referenced path exists and counting formats in the gate script.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"=== referenced files existence ===\"\nfor f in tools/diff_flux.py tools/flux_codec.py tools/profil_flux.py tools/proxy_latence.py tools/sprint.sh tools/archive_sessions.py tools/portes_formats.sh docs/format-flux.md docs/colab-r … [728 caractères tronqués]`

  ```
=== referenced files existence ===
OK   tools/diff_flux.py
OK   tools/flux_codec.py
OK   tools/profil_flux.py
OK   tools/proxy_latence.py
OK   tools/sprint.sh
OK   tools/archive_sessions.py
OK   tools/portes_formats.sh
OK   docs/format-flux.md
OK   docs/colab-reparti.md
OK   reports/rapport-analyse-flux.md
OK   reports/rapport-placement-bits-kv.md
OK   reports/rapport-attribution-kv.md
OK   reports/rapport-transport-liste.md
OK   reports/rapport-cpu-aer.md
OK   reports/rapport-croisement-push-pull.md
OK   reports/rapport-localite-activation.md
OK   reports/rapport-capteur-hebbien.md
OK   reports/bilan-multi-materiel.md
OK   reports/rapport-session-2026-09-30.md
OK   docs/plan-deepseek41-complet.md
OK   colab
OK   Qtrinet-bootstrap.md
=== formats in portes_formats.sh ===
0
39:  "IQ3_XXS    | $MODELES/Kimi-K2.7-Code-UD-IQ1_M/Kimi-K2.7-Code-UD-IQ1_M-00002-of-00008.gguf | blk.1.ffn_down_exps.weight       | 18"
  ```

### 🤖 Assistant

⏵ Counting the formats actually gated and confirming 17 vs 18.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nsed -n '1,60p' tools/portes_formats.sh", "description": "Read formats gate script header"}`

  ```
#!/usr/bin/env bash
# Portes des FORMATS : chaque déquantificateur comparé à libggml, bloc par bloc.
#
#   tools/portes_formats.sh [type ...]
#
# Pourquoi : nos déquantificateurs sont écrits d'après le C de ggml, et les cinq
# premiers essais se sont tous trompés (IQ2_XXS : pas de 8 octets sur `qs` ;
# IQ1_M : échelles lues en premier alors qu'elles sont en DERNIER ; Q2_K : indice
# d'échelle ; Q5_K : bits hauts relus au lieu d'avancés ; Q6_K : quants
# entrelacés au lieu de groupés). Aucun n'a été trouvé par relecture : tous l'ont
# été par comparaison à la bibliothèque. Cette porte rend la comparaison
# reproductible, et refuse de « passer » si le témoin a disparu du disque — un
# test qui saute est un test qui ne dit rien.
#
# La référence est liée à libggml (voir tools/ref_ggml_bloc.c).
set -u
cd "$(dirname "$0")/.."
RACINE=$PWD
MODELES=${DRAVE_MODELES:-/home/stephane/Data13TB/stephane/modeles/gguf}
LLAMA=${DRAVE_LLAMA:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}
REF=${REF_GGML_BLOC:-/tmp/ref_ggml_bloc}
VERIF=tools/verifier_formats.py
IFS=$'\n'

ok=0; ko=0; abs=0
# libellé | fichier | tenseur | type ggml
BATTERIE=(
  "F32        | $MODELES/codestral-22b-v0.1-q4_k_m.gguf 
… [2834 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying the f16/int4 measurement before writing the report.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"=== placement-bits lines 14-30 ===\"; sed -n '14,30p' reports/rapport-placement-bits-kv.md\necho \"=== REPRISE 365-368 ===\"; sed -n '363,370p' REPRISE.md\necho \"=== roadmap 181-186 ===\"; sed -n '181,187p' docs/roadmap.md", "d … [47 caractères tronqués]`

  ```
=== placement-bits lines 14-30 ===
|---|---|---|---|---|---|
| f32 | f32 | 8 | 100 % | **14,2339** | référence |
| **f32** | **int8** | 5,125 | 64 % | **14,2372** | **+0,023 %** |
| **int8** | **f32** | 5,125 | 64 % | 14,6622 | **+3,01 %** |
| f32 | int4 | 4,625 | 58 % | 14,2994 | +0,46 % |
| int4 | f32 | 4,625 | 58 % | 69,0464 | **+385 %** |
| int8 | int8 | 2,25 | 28 % | 14,6667 | +3,04 % |
| **f16** | **int8** | **3,125** | **39 %** | **14,2365** | **+0,018 %** |
| int4 | int4 | 1,25 | 16 % | 66,0369 | **+364 %** |
| f16 | int4 | 2,625 | 33 % | 14,3209 | +0,61 % |

## Ce que la courbe dit

**La frontière, du plus petit au plus gros** (8 191 jetons, ctx 8 192) :

```
16 %  int4/int4 ................ +364 %
=== REPRISE 365-368 ===
`--trace-flux` en inférence (muet), les modes multiples (silencieux). Restent :
`--banc-vision` (ne reçoit aucune `Options`), `--bits` du noyau GPU, et la
recommandation de fond — un `--options-actives` qui imprime les réglages
réellement en vigueur.

### Créneau 15h07 → 18h00 : le mode 4, et la frontière KV confirmée

**Le protocole est en version 5** avec un cinquième mode : le **mode 4 « lot en
=== roadmap 181-186 ===
coûte +0,023 % là où clés int8 + v
… [417 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Re-reading the exact lines I will quote, to avoid transcription errors.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nawk 'NR==76||NR==79||NR==85||NR==86||NR==87||NR==88||NR==89||NR==99||NR==121||NR==122||NR==125||NR==126||NR==147||NR==151||NR==163||NR==166||NR==181||NR==188||NR==209||NR==222 {printf \"vision:%d: %s\\n\", NR, $0}' docs/vision.md\necho … [383 caractères tronqués]`

  ```
vision:76: * **top 10 % des neurones portent 33,1 % de la magnitude** ; seuls **0,08 %** sont
vision:79: * `--attn-topk 256` **améliore** la perplexité (234,88 contre 298,56 à contexte
vision:85: **Ce que la vision ajoute** : faire du flux un **objet de première classe** —
vision:86: un format de trace stable, par couche et par neurone, qu'on puisse rejouer,
vision:87: diffuser et comparer entre deux versions d'un modèle ou deux configurations du
vision:88: moteur. Le débogage cesse d'être « la perplexité a bougé de 0,01 » pour devenir
vision:89: « la couche 23 a changé de régime au jeton 4 096 ».
vision:99: | cache KV d'une couche | VRAM (paginée, sur **deux** cartes) | attention à 1 M de clés : 968 → **13,2 ms** par couche |
vision:121: Deux processus se passent des flux (protocole v4 : version, modes dense / listes /
vision:122: blocs / **lot**, contrat d'activation complet), le découpage est fidèle au bit
vision:125: reste : le lot en listes, l'ordonnanceur de placement, le flux de poids depuis le
vision:126: NVMe. La
vision:147: 5. **les mesures à faire** : débit d'un flux sérialisé, latence aller-retour,
vision:151: Cette section est une **hypothèse de travail**, pas un résul
… [2146 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying every line number with grep before writing the table (read-tool numbering differs from prior notes).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"### ROADMAP\"\ngrep -n \"Cinq phases\" docs/roadmap.md\ngrep -n \"Contrat d'échange v1\" docs/roadmap.md\ngrep -n \"234,88 contre 298,56\" docs/roadmap.md\ngrep -n \"La mesure clés f16 + valeurs int4 est en cours\" docs/roadmap. … [1196 caractères tronqués]`

  ```
### ROADMAP
3:> Suite de [`docs/vision.md`](vision.md). Cinq phases, de ce qui se fait **tout de
55:| 3.1 | **Contrat d'échange v1** : tranche de liste = en-tête (couche, source, échelle, bits) + paires (destination, valeur) | ✅ | format écrit, relu, rejoué sans perte (phase 0.3/0.3bis) ; **transport TCP en place et FIDÈLE** (`--flux-serveur`, `--ppl-reparti`) — écart local/réparti **0,00e0** sur 40 et 200 jetons (39 et 199 flux : le dernier n'a rien à prédire), après correction de deux défauts (plage de couches ignorée par `forward`, norme finale appliquée deux fois) |
27:| 1.1 | **Top-k dans le noyau d'attention GPU** — `--attn-topk 256` améliore la perplexité (234,88 contre 298,56 à 2 048) mais retombe sur le CPU | ⏳ | plus aucun repli CPU dans le chemin long contexte |
186:La mesure clés f16 + valeurs int4 est en cours.
250:Le protocole, lui, n'a pas changé d'un octet : c'est le moteur qui était faux.
307:lots** (mode 3 : 256 jetons en 4 lots, écart 0,00e0). Ce qui reste : le lot en
### VISION
76:* **top 10 % des neurones portent 33,1 % de la magnitude** ; seuls **0,08 %** sont
79:* `--attn-topk 256` **améliore** la perplexité (234,88 contre 298,56 à contexte
85:**Ce que la vis
… [1438 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Confirming mode 4 is implemented before flagging it as done.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"=== mode 4 report ===\"; sed -n '1,20p' reports/rapport-mode4-lot-listes.md\necho \"=== code mode 4 ===\"; grep -rn \"MODE_LOT_LISTES\\|mode 4\\|Mode::LotListes\\|lot_listes\" drave-core/src/*.rs | head -8\necho \"=== roadmap 30 … [114 caractères tronqués]`

  ```
=== mode 4 report ===
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
=== code mode 4 ===
drave-core/src/engine.rs:247:    /// mêmes activations en i16, pour le noyau AVX2 du mode 4
drave-core/src/engine.rs:638:    /// Produit matrice-vecteur avec des poids **4 bits** (mode 4).
d
… [859 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Last source check on the vision-module figures, then I write the report.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngrep -rn --exclude-dir=journal \"5,4e-7\\|1,7e-6\" reports/*.md docs/*.md REPRISE.md | head -8", "description": "Find vision module validation sources"}`

  ```
docs/plan-mla-vision.md:229:Mesure : **écart max relatif 5,4e-7** — le bruit de virgule flottante du moteur,
docs/plan-mla-vision.md:416:tranches du chemin image sont validées contre numpy (5,4e-7, 1,8e-6, 1,7e-6), la
docs/plan-mla-vision.md:545:   comparables — embedding de patchs et projecteur — le restent (5,4e-7 et
docs/plan-mla-vision.md:546:   1,7e-6), et l'outil le dit au lieu de planter.
docs/plan-mla-vision.md:568:| embedding de patchs, projecteur | **validés** contre numpy (5,4e-7 et 1,7e-6, à 28 × 28) |
docs/vision.md:166:  indépendante** (MLA à **5,2e-7** contre numpy ; vision : patchs 5,4e-7,
docs/vision.md:167:  projecteur 1,7e-6) montrent la méthode : une seconde implémentation de la même
REPRISE.md:225:   validées contre numpy : patchs 5,4e-7, projecteur 1,7e-6, une couche 1,8e-6.
  ```

### 🤖 Assistant

⏵ Writing the audit report and sending it to the parent agent.

- **send_message** `{"agent_id": "bbd6969f-0f70-42b2-8951-64d1f2f36d2e", "message": "RAPPORT DE RELECTURE ADVERSARIALE — docs/vision.md, roadmap.md, programme-recherche.md, sprints.md, histoire.md (aucun fichier modifié ; 24 constats, tous les numéros de ligne revérifiés par grep le 02/10/2026).\n\n| fichier:ligne | ci … [10283 caractères tronqués]`

  ```
message delivered to agent bbd6969f-0f70-42b2-8951-64d1f2f36d2e
  ```

### 🤖 Assistant

⏵ Rapport terminé : 24 constats, envoyés au parent.

Relecture adverse des cinq documents. Aucun fichier modifié. Tous les numéros de ligne ont été revérifiés par `grep` sur l'état courant du dépôt (attention : certaines références de l'audit précédent, `reports/rapport-coherence-docs-2.md`, pointent des lignes qui ont bougé — elles ont été recalculées ici).

| fichier:ligne | citation exacte (≤ 25 mots) | problème | correction minimale proposée (texte de remplacement exact) | gravité |
|---|---|---|---|---|
| docs/vision.md:222 | `\| **3. Répartir sur machines** \| **rien** — hypothèse écrite \|` | Contredit vision.md:120 (« Le transport existe, et c'est l'axe où le projet a le plus avancé depuis ») et roadmap.md:55-59 (3.1 ✅ transport TCP fidèle 0,00e0, 3.2 ✅ mode 4, 3.5 ✅). | `\| **3. Répartir sur machines** \| **transport en place et fidèle** (0,00e0) ; restent l'ordonnanceur et Colab \|` | ÉLEVÉE |
| docs/vision.md:151 | « Cette section est une **hypothèse de travail**, pas un résultat. » | Le §4 juste au-dessus donne des acquis mesurés ; la même formule revient en §7 (vision.md:209-210). | « Cette section mêle un **acquis** (le transport, fidèle à 0,00e0) et une **hypothèse de travail** (placement, granularité). » | MOYENNE |
| docs/vision.md:147 | « 5. **les mesures à faire** : débit d'un flux sérialisé, latence aller-retour, » | Déjà mesurées : roadmap.md:57 (latence jusqu'à 20 ms, 0,25 Mbit/s) et :112 (1 608 octets/flux). | « 5. **les mesures faites** : 1 608 octets par flux à 256 jetons, 0,25 Mbit/s, attente ≈ calcul distant + 3,2 × latence (`docs/roadmap.md`) ; » | MOYENNE |
| docs/vision.md:209-210 | « l'axe 3 est une hypothèse, avec ses mesures à faire » | Même dérive : les mesures existent (roadmap.md:57, :112, :119). | « l'axe 3 est **engagé** (transport fidèle), avec ses mesures faites (latence, débit, taille des tranches) » | MOYENNE |
| docs/vision.md:121 | « Deux processus se passent des flux (protocole v4 : version, modes dense / listes / » | Protocole en **v5** à cinq modes (roadmap.md:96-97) ; la liste en omet un. | « (protocole v5 : version, modes dense / listes / blocs / **lot dense** / **lot en listes**, contrat d'activation complet) » | MOYENNE |
| docs/vision.md:79 | « `--attn-topk 256` **améliore** la perplexité (234,88 contre 298,56 à contexte » | Chiffre sans source, déclaré non reproductible par docs/plan-gpu-topk.md:94 (« 234,88 ne correspond à aucun réglage reproductible »). | « `--attn-topk 256` **améliore** la perplexité (234,88 / 298,56 non reproductibles — `docs/plan-gpu-topk.md`) » | MOYENNE |
| docs/vision.md:163 | « gpt-oss ctx 256 = **15,1757**) sont l'application minimale de cette idée : » | Porte périmée : **15,6017** depuis le 02/10 (REPRISE.md:1000 ; reports/rapport-routage-experts.md:66). | « gpt-oss ctx 256 = **15,6017**) sont l'application minimale de cette idée : » | MOYENNE |
| docs/sprints.md:39 | « gpt-oss ctx 256 = **15,1757** (sans `DRAVE_GPU`), et le banc réparti donne » | Même porte périmée : la definition of done valide un chiffre faux. | « gpt-oss ctx 256 = **15,6017** (sans `DRAVE_GPU`), et le banc réparti donne » | MOYENNE |
| docs/roadmap.md:3 | « Suite de [`docs/vision.md`](vision.md). Cinq phases, de ce qui se fait **tout de » | Le document compte **six** phases (0 à 5). | « Suite de [`docs/vision.md`](vision.md). Six phases, de ce qui se fait **tout de » | FAIBLE |
| docs/roadmap.md:27 | « `--attn-topk 256` améliore la perplexité (234,88 contre 298,56 à 2 048) mais retombe sur le CPU » | docs/plan-gpu-topk.md:94 : ce critère chiffré « était faux d'avance ». | « `--attn-topk 256` améliore la perplexité (234,88 non reproductible — `docs/plan-gpu-topk.md`) mais retombe sur le CPU » | MOYENNE |
| docs/roadmap.md:186 | « La mesure clés f16 + valeurs int4 est en cours. » | Mesure faite : +0,61 % à 33 % de la taille f32 (reports/rapport-placement-bits-kv.md:23). | « Clés f16 + valeurs int4 : **+0,61 %** à 33 % de la taille f32 (`reports/rapport-placement-bits-kv.md`). » | MOYENNE |
| docs/roadmap.md:250 | « Le protocole, lui, n'a pas changé d'un octet : c'est le moteur qui était faux. » | Faux comme phrase de page : l'en-tête est passé de 39 à 79 octets (roadmap.md:96, :112). | « Le protocole, lui, n'a pas changé **pour cette correction** : c'est le moteur qui était faux. » | MOYENNE |
| docs/roadmap.md:308 | « listes (mode 4), l'ordonnanceur de placement, et la démonstration sur Colab, dont » | Le mode 4 est fait et mesuré (roadmap.md:56 ✅ 1,5 ko/jeton, 3,03e-2 ; :118 ; `MODE_LOT_LISTES`, main.rs:1886). | « l'ordonnanceur de placement, et la démonstration sur Colab, dont » | MOYENNE |
| docs/vision.md:125 | « reste : le lot en listes, l'ordonnanceur de placement, le flux de poids depuis le » | Même liste périmée : le lot en listes (mode 4) est fait (roadmap.md:56, :118). | « reste : l'ordonnanceur de placement, le flux de poids depuis le » | MOYENNE |
| docs/roadmap.md:55 | « \| 3.1 \| **Contrat d'échange v1** : tranche de liste = en-tête (couche, source, échelle, bits) » | « v1 » face au protocole v5 annoncé en roadmap.md:96 : piège de lecture. | « \| 3.1 \| **Contrat d'échange** (protocole v5) : tranche de liste = en-tête (couche, source, échelle, bits) » | FAIBLE |
| docs/vision.md:166 | « indépendante** (MLA à **5,2e-7** contre numpy ; vision : patchs 5,4e-7, » | Ne cite que la validation numpy synthétique ; la validation courante est contre llama.cpp sur GLM-5.3 (0,999024 — rapport-mla-experts.md:112). | « indépendante** (MLA à **5,2e-7** contre numpy et **0,999024** contre llama.cpp sur GLM-5.3 ; vision : patchs 5,4e-7, » | FAIBLE |
| docs/programme-recherche.md:24 | « L'architecture événementielle défendue ici possède trois propriétés structurelles » | Aucune des trois ne dit que le flux se route entre composants et machines (cœur de la vision §3-§4 ; plan-deepseek41-complet.md:6-8). | « …possède **quatre** propriétés structurelles » + 4ᵉ puce : « **Le flux se route.** Une liste est une unité de travail autonome, plaçable sur un composant (CPU, GPU, FPGA) ou une autre machine, là où son coût est le plus faible. » | MOYENNE |
| docs/programme-recherche.md:46 | « \| Inférence 0,5 B quantifié, CPU seul, sans GPU ni BLAS \| **15,8 tok/s**, perplexité 24,90 (référence float32 : 25,00) \| » | Ouvre le « point de départ mesuré » sur le débit dense, sans métrique d'activité ni renvoi (table :46-53 entièrement non sourcée). | « \| Inférence 0,5 B quantifié, CPU seul, sans GPU ni BLAS \| **15,8 tok/s** (et **5,3 G événements/s** : le coût suit l'activité), perplexité 24,90 (référence float32 : 25,00) — `reports/rapport-inference.md`, `reports/bilan-multi-materiel.md` \| » | MOYENNE |
| docs/vision.md:89 | « « la couche 23 a changé de régime au jeton 4 096 ». » | La finalité « lire ces flux pour comprendre le modèle et adapter l'architecture à la tâche » (plan-deepseek41-complet.md:8,33) n'est écrite nulle part dans la vision. | Ajouter après la ligne 89 : « Et, au-delà du débogage : **lire ces flux pour comprendre le modèle et adapter l'architecture à la tâche**. » | MOYENNE |
| docs/vision.md:181 | « La représentation par listes valuées impose ses formats, et ils sont déjà là : » | La vision n'énonce ni les **deux listes** (trinaire) ni les **connexions pondérées** (source → destination, poids), piliers du plan V4.1:16-19. | Ajouter après la ligne 184 : « Le cas général est la **connexion pondérée** (source → destination, poids) ; le cas trinaire se passe de valeur — **deux listes**, le signe est porté par l'appartenance à celle des « + » ou des « − ». » | MOYENNE |
| docs/vision.md:99 | « \| cache KV d'une couche \| VRAM (paginée, sur **deux** cartes) \| attention à 1 M de clés : 968 → **13,2 ms** par couche \| » | Le tableau §3 (99-104) ne renvoie à aucun rapport, alors que la vision promet un renvoi par mesure (l.10-11). | Ajouter après la ligne 104 : « Sources : `docs/contexte-long.md` (KV paginé, attention GPU), `reports/rapport-session-2026-09-30.md`, `REPRISE.md` §5. » | FAIBLE |
| docs/vision.md:188 | « l'int8 sur le cache KV coûte **+1,5 %** de perplexité à 512 jetons et » | Les chiffres du §6 (188-193) ne portent aucun renvoi. | « …**où sont les échelles** (`reports/rapport-placement-bits-kv.md`) ; » | FAIBLE |
| docs/vision.md:76 | « **top 10 % des neurones portent 33,1 % de la magnitude** ; seuls **0,08 %** sont » | Deux chiffres clés sans source (source : reports/rapport-localite-activation.md:44-45). | « alors qu'un cache dynamique, si (`reports/rapport-localite-activation.md`) ; » | FAIBLE |
| docs/programme-recherche.md:29 | « nommées. Journaliser les listes d'activations (1,2 Mo/token, **+3,0 %**) » | Chiffres sans renvoi ; sources : reports/rapport-programme-evolutif.md:19 et :118. | « les événements en sont une fonction déterministe (`reports/rapport-programme-evolutif.md`). » | FAIBLE |

**Ce qui est déjà cohérent et ne doit pas être touché**
- `vision.md` §1 (21-55) : listes valuées par source, push/AER, coût ∝ activité — et l'honnêteté du croisement ~22 % avec conservation du chemin dense ; §7 (200-212), les quatre refus ; §9 (228-247), nom, renommage, trois préservations.
- `roadmap.md` 89-101 (format-flux.md source unique, DRVF v2/v3, protocole v5) et le journal daté 104-120 avec ses corrections écrites ; 235-250 (les deux défauts de fidélité) et 277-295 (réfutation de l'entrée normée, 5,61e0).
- `programme-recherche.md` §1 « règle du programme », §3 « ce que la mesure interdit d'espérer », §6 méthode.
- `histoire.md` : cohérent de bout en bout, chaque affirmation porte son renvoi — **rien à corriger**.
- `sprints.md` hors la porte gpt-oss : charte saine (definition of done, « tout chiffre a sa source », relecture déléguée).

**Points à trancher par l'humain**
1. `sprints.md:38-40` ne liste que Qwen, gpt-oss et le banc réparti ; `tools/portes.sh` porte aussi Qwen3-30B clusters (**799,8557**), ≥ 48 tests, formats et routage — aligner la definition of done sur le script ?
2. `vision.md:49-50` affirme que les portes tournent « sur les deux » chemins ; `tools/portes.sh` ne lance Qwen et clusters qu'avec `--dense` — ajouter une porte listes, ou corriger la phrase ?
3. La roadmap ne mentionne ni GLM-5.3 / Kimi-K2.7 / DeepSeek-V4.1 ni `docs/plan-deepseek41-complet.md` (« les flux d'abord ») : ajouter une phase/chantier ?
4. Formats : la référence dit **18** formats lisibles ; `tools/portes_formats.sh` en teste **17** et `REPRISE.md:1002` écrit « 17 formats × 2 blocs » — à réconcilier.
5. `reports/rapport-analyse-flux.md:14` dit le croisement « mesuré à ~10 % de densité » alors que vision/roadmap/histoire disent ~22 % (`rapport-croisement-push-pull.md:96`) ; `roadmap.md:28` cite ce rapport — trancher.
6. Les valeurs 234,88 / 298,56 vivent aussi dans `docs/contexte-long.md:559-560` : les retirer partout, ou les encadrer d'un avertissement ?

