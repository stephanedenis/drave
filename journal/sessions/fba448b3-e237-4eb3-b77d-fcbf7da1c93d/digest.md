# Session DSH — relecture

- identifiant : `fba448b3-e237-4eb3-b77d-fcbf7da1c93d`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-02 15:03:29
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM en Rust qui exécute les projections sous forme de listes d'activation creuses plutôt que de produits scalaires denses).

TÂCHE : dépouille EXHAUSTIVEMENT ces 20 fichiers Markdown :
reports/aiguille-30b.md
reports/aiguille-gpt-oss.md
reports/bilan-multi-materiel.md
reports/rapport-8bits.md
reports/rapport-aiguille.md
reports/rapport-aiguille-topk.md
reports/rapport-analyse-flux.md
reports/rapport-architecture-memoire.md
reports/rapport-attention-creuse.md
reports/rapport-attribution-kv.md
reports/rapport-campagne-parcimonie.md
reports/rapport-capteur-hebbien.md
reports/rapport-coherence-docs-2.md
reports/rapport-coherence-docs.md
reports/rapport-coherence-vision.md
reports/rapport-compacite-trace.md
reports/rapport-cpu-aer.md
reports/rapport-croisement-push-pull.md
reports/rapport-decoupage-moe.md
reports/rapport-drapeaux-ignores.md

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

⏵ Lecture exhaustive des 20 rapports Markdown pour construire l'inventaire

- **bash** `{"command": "wc -l reports/aiguille-30b.md reports/aiguille-gpt-oss.md reports/bilan-multi-materiel.md reports/rapport-8bits.md reports/rapport-aiguille.md reports/rapport-aiguille-topk.md reports/rapport-analyse-flux.md reports/rapport-architecture-memoire.md reports/rapport-attention-creuse.md rep … [500 caractères tronqués]`

  ```
8 reports/aiguille-30b.md
     8 reports/aiguille-gpt-oss.md
   153 reports/bilan-multi-materiel.md
    60 reports/rapport-8bits.md
   103 reports/rapport-aiguille.md
   322 reports/rapport-aiguille-topk.md
    68 reports/rapport-analyse-flux.md
   428 reports/rapport-architecture-memoire.md
   165 reports/rapport-attention-creuse.md
    54 reports/rapport-attribution-kv.md
    91 reports/rapport-campagne-parcimonie.md
   125 reports/rapport-capteur-hebbien.md
   241 reports/rapport-coherence-docs-2.md
   229 reports/rapport-coherence-docs.md
   170 reports/rapport-coherence-vision.md
   263 reports/rapport-compacite-trace.md
    69 reports/rapport-cpu-aer.md
   129 reports/rapport-croisement-push-pull.md
   117 reports/rapport-decoupage-moe.md
   255 reports/rapport-drapeaux-ignores.md
  3058 total
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/aiguille-30b.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/aiguille-gpt-oss.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/bilan-multi-materiel.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/aiguille-30b.md</path>
<type>file</type>
<content>
1: # aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf
2: lot 256, 40 jetons de réponse, 16 fils
3: 
4: | contexte | profondeur | trouvé | secondes | détail |
5: |---|---|---|---|---|
6: | 2048 | 0.1 | **oui** | 667.6 | prompt 2147 jetons |
7: | 2048 | 0.5 | **oui** | 690.5 | prompt 2147 jetons |
8: | 2048 | 0.9 | **oui** | 651.5 | prompt 2147 jetons |

(End of file - total 8 lines)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/aiguille-gpt-oss.md</path>
<type>file</type>
<content>
1: # aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf
2: lot 512, 40 jetons de réponse, 16 fils
3: 
4: | contexte | profondeur | trouvé | secondes | détail |
5: |---|---|---|---|---|
6: | 4096 | 0.1 | **oui** | 653.2 | prompt 3944 jetons |
7: | 4096 | 0.5 | **oui** | 566.7 | prompt 3944 jetons |
8: | 4096 | 0.9 | **oui** | 559.3 | prompt 3944 jetons |

(End of file - total 8 lines)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/bilan-multi-materiel.md</path>
<type>file</type>
<content>
1: # Bilan multi-matériel — CPU, FPGA, GPU
2: 
3: État au terme des trois implémentations. Tous les chiffres marqués **mesuré** ont
4: été pris sur cette machine, avec le code de ce dépôt ; ceux marqués *projeté* ou
5: *déduit* le sont explicitement, avec leur base.
6: 
7: Machine : 2 × Xeon E5-2687W v3 (20 cœurs / 40 threads, 125 Go), 2 × Quadro
8: RTX 5000 (16 Go, NVLink 25,78 Go/s), 1 carte Stratix V GS (Storey Peak,
9: DDR3 9,66 Go/s, PCIe Gen3 ×8 6,5 Go/s, QSFP+ 4,8 Go/s).
10: 
11: Modèle de référence pour toutes les comparaisons : **Qwen2.5-0.5B-Instruct Q8_0**,
12: 494 M de poids, 4 864 dimensions cachées, 24 couches. Un token = **352,8 M
13: d'événements** (0,7 Go de listes lues).
14: 
15: ---
16: 
17: ## 1. Ce qui a été construit
18: 
19: | Cible | Livrable | Taille | Vérification |
20: |---|---|---|---|
21: | **CPU** | `drave-core` — moteur d'événements, tokenizer BPE, forward Qwen2, génération, perplexité | **2 547 lignes de Rust, `std` seul, 0 dépendance** | tokens identiques à la référence numpy ; perplexité identique ; 14/14 au banc des décodeurs |

… [8481 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-8bits.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-aiguille.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-analyse-flux.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-8bits.md</path>
<type>file</type>
<content>
1: # Drave — 8 bits : la perfection est-elle atteignable ?
2: 
3: Modèle : **qwen2** en Q8_0, 494.0 M poids analysés.
4: 
5: ## 1. Distribution des niveaux
6: 
7: - densité : **99.2 %**
8: - niveaux distincts : **256** (sur 256 possibles)
9: - `E[|v|]` : **42.79**
10: - `E[popcount(|v|)]` : **3.13**
11: - niveaux les plus fréquents : `127` (1.6 %), `-127` (1.6 %), `2` (0.8 %), `-1` (0.8 %), `1` (0.8 %), `3` (0.8 %), `0` (0.8 %), `-2` (0.8 %)
12: 
13: ## 2. Bits réellement nécessaires (sans perte)
14: 
15: | Codage | bits/poids | Gain |
16: |---|---|---|
17: | positionnel fixe | 8,000 | ×1,000 |
18: | **entropie de la source** | **7.648** | **×1.046** |
19: | **code de Huffman réel** | **7.671** | **×1.043** |
20: 
21: ## 3. Encodages structurels
22: 
23: | Stratégie | bits/poids | opérations/poids |
24: |---|---|---|
25: | positionnel (8 bits) | 8,00 | 0.99 |
26: | plans denses (7 plans + signe) | 8,00 | 3.10 |
27: | unaire (répétition) | 42.45 | 42.45 |
28: | **Huffman (sans perte)** | **7.67** | 0.99 |
29: 
30: ## 4. Sur le modèle entier
31: 
32: | | Taille des niveau
… [1590 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-aiguille.md</path>
<type>file</type>
<content>
1: # L'aiguille dans la botte de foin : où en est la mesure de qualité
2: 
3: La perplexité ne dit **pas** si un modèle retrouve une information. Ce rapport
4: raconte la remise en route de la seule mesure qui le dise, et ce qu'elle a
5: immédiatement appris.
6: 
7: ## 1. Ce qui n'allait pas dans la v1
8: 
9: La v1 (`tools/aiguille.py`, conservée dans l'historique) plantait un code dans un
10: contexte dont le remplissage était **la même phrase recopiée** jusqu'à la
11: longueur voulue, posait la question, et n'accordait que **8 jetons** de réponse.
12: Résultat : 6 sondes sur 6 échouaient sur Qwen2.5-0.5B, et 9,6 minutes pour un
13: échec sur Qwen3-30B-A3B. Le test a été arrêté à l'époque, faute de budget.
14: 
15: Trois défauts, tous de protocole :
16: 
17: 1. **remplissage répété** : un modèle peut répondre en devinant la structure du
18:    texte, et la sonde ne teste plus la mémoire mais la régularité ;
19: 2. **réponse trop courte** : un code peut sortir au deuxième ou troisième jeton
20:    d'une réponse ; s'arrêter à 8 jetons fait échouer des sondes que le mo
… [4400 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-analyse-flux.md</path>
<type>file</type>
<content>
1: # Analyse du flux, couche par couche
2: 
3: Première analyse **pure** : aucune exécution du moteur, seulement une trace relue
4: (`tools/analyse_flux.py`). Ce qu'elle apporte, et pourquoi ces questions-là ont
5: été posées plutôt que d'autres.
6: 
7: Modèle : Qwen2.5-0.5B Q8_0, contexte 256, 256 jetons, 24 couches, 896 cachés,
8: trace enregistrée avec `--abits 8 --act-thresh 0.05` (réglage de COÛT, pas de
9: qualité : la perplexité de cette configuration est de 2 445 — ce qui suit décrit
10: la forme du flux, pas la qualité du modèle).
11: 
12: ## Densité : où le push paie, où le pull paie
13: 
14: Le croisement push/pull du projet est mesuré à **~10 % de densité**. Ce qui
15: manquait était la densité **par couche** — or elle varie du simple au triple :
16: 
17: | couche | densité | couche | densité |
18: |---|---|---|---|
19: | **9** | **20,1 %** | 6 | 40,5 % |
20: | 0 | 25,9 % | 5 | 45,6 % |
21: | 4 | 26,7 % | **1** | **56,3 %** |
22: | 3 | 28,8 % | 8 | 29,2 % |
23: 
24: Autrement dit : la décision « listes ou matrice dense » n'est pas une propriété du
25:
… [2379 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-aiguille-topk.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-attribution-kv.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-aiguille-topk.md</path>
<type>file</type>
<content>
1: # Rapport — l'attention creuse perd-elle l'information ? (aiguille × `--attn-topk`)
2: 
3: **En une ligne** : à 4 096 clés, l'attention à **256 clés (6,25 %)** des 24 jetons
4: de DÉCODAGE retrouve l'information placée **au début** (profondeur 0,1) et **à la
5: fin** (0,9), mais **pas au milieu** (0,5) — là où l'attention complète la retrouve.
6: CPU et GPU se comportent pareil, ce qui est aussi un contrôle croisé des deux
7: implémentations.
8: 
9: ⚠️ **Portée exacte de la mesure** : avec `--lot 256` (le réglage de cette grille),
10: le moteur **ignore `--attn-topk` au préremplissage** — il l'imprime lui-même
11: (« l'attention par lots est DENSE »). Le k = 256 ne s'applique donc qu'aux 24 jetons
12: générés (0,58 % des passes), ce qui est bien le moment où le modèle doit regarder
13: en arrière — mais la phrase « une attention qui ne garde que 256 clés » décrit le
14: DÉCODAGE, pas le passage entier. Une grille en `--lot 1` lèverait l'ambiguïté ; elle
15: est au planning (le message d'avertissement du moteur n'est pas lu par
16: `aiguille.py`, qui ne lit la
… [19309 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-attribution-kv.md</path>
<type>file</type>
<content>
1: # Phase 1.4 — l'écart du cache KV int8 est ENTIÈREMENT dû aux clés
2: 
3: **En une ligne** : à 8 192 jetons, les **valeurs** en int8 ne coûtent rien
4: (1 % de l'écart) et les **clés** coûtent tout (99 %) — l'expérience était écrite
5: dans la feuille de route, la voici faite.
6: 
7: ## Les quatre mesures
8: 
9: Qwen2.5-0.5B-Q8_0, 8 191 jetons notés, contexte 8 192, `--dense --lot 512` :
10: 
11: | configuration | perplexité | écart au f32 | part de l'écart |
12: |---|---|---|---|
13: | cache f32 (référence) | **14,2339** | — | — |
14: | cache int8 complet | 14,6667 | +3,04 % | 100 % |
15: | **clés f32** · valeurs int8 | **14,2372** | **+0,023 %** | **99,2 % expliqué** |
16: | clés int8 · **valeurs f32** | 14,6622 | +3,01 % | 1,0 % seulement |
17: 
18: Reproductible :
19: 
20: ```bash
21: DRAVE_KV_BITS=8 DRAVE_KV_K_F32=1 ./drave models/Qwen2.5-0.5B-Q8_0.gguf \
22:     --ppl /tmp/ids_qwen_long.txt --ctx 8192 --limit 8192 --dense --threads 16 --lot 512
23: ```
24: 
25: ## Ce que ça veut dire
26: 
27: Les deux moitiés du cache n'ont pas du tout le même rôle : u
… [1623 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-architecture-memoire.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-architecture-memoire.md</path>
<type>file</type>
<content>
1: # Rapport — architecture mémoire : ce qui va en VRAM, en RAM, et sur le disque
2: 
3: Session du 01/10. Cible : DeepSeek-V4.1-Flash (365,7 Go, 40 couches, 384 experts,
4: top-6). Machine : 2 × Quadro RTX 5000 (**32 Go** de VRAM), **125 Go** de RAM,
5: 40 CPU, NVMe de 828 Go.
6: 
7: Chaque chiffre de débit est **mesuré**, pas supposé.
8: 
9: ## 1. Les débits, mesurés
10: 
11: | niveau | débit | comment |
12: |---|---|---|
13: | **VRAM** (noyau `warp par ligne`) | **84,9 Go/s** | banc GPU, tête de 144,6 Mo en 1,7 ms |
14: | VRAM (noyau `ligne par fil`) | 41,9 Go/s | même banc, 3,4 ms |
15: | **RAM** (CPU, 30 fils) | **20,9 Go/s** | même banc, 6,9 ms |
16: | **NVMe**, aléatoire, blocs 4 Mo | 5,5 Go/s | mesuré, cache chaud |
17: | **PCIe** 3.0 ×16 | ~12 Go/s | théorique 15,75 ; le lien monte à gen 3 sous charge |
18: 
19: Surprise utile : le `warp par ligne` est **4× plus rapide que le CPU** (84,9 contre
20: 20,9). Le déport n'est donc pas un gain marginal — c'est un facteur 4 sur chaque
21: octet lu en VRAM.
22: 
23: *(Le lien PCIe reste à gen 1 quand les
… [20600 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-attention-creuse.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-campagne-parcimonie.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-attention-creuse.md</path>
<type>file</type>
<content>
1: # Attention creuse — le trou se referme, et par le haut
2: 
3: Le point faible identifié dans nos bilans : l'attention n'est **pas exprimable en
4: listes d'événements**, parce que ses poids sortent d'un softmax calculé à
5: l'exécution, et son coût croît **linéairement avec le contexte** (2,0 ms à 64
6: tokens, 12,7 ms à 512, ~200 ms extrapolé à 8 192).
7: 
8: Une seule modification, à l'inférence, sans réentraînement : **ne garder que les
9: k plus grands scores par requête** avant le softmax. Les autres sont masqués
10: (`-∞`), le softmax renormalise sur les k retenus.
11: 
12: *Ce n'est pas une importation : c'est la même question que pour les activations —
13: imposer une parcimonie à un modèle préentraîné et mesurer ce qu'elle coûte. La
14: réponse, ici, est qu'elle **rapporte**.*
15: 
16: ---
17: 
18: ## 1. Résultat
19: 
20: Deux jeux de 1 024 tokens, réglage sur A, vérification sur B.
21: 
22: | k (clés gardées) | PPL (A) | PPL (B) | 2 040 tokens | ctx 512 |
23: |---|---|---|---|---|---|
24: | **dense** (référence) | 23,6125 | 26,2565 | 24,8995 | 1
… [7215 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-campagne-parcimonie.md</path>
<type>file</type>
<content>
1: # Campagne « parcimonie imposée » — synthèse
2: 
3: *Peut-on exécuter un modèle **préentraîné** de façon radicalement plus creuse,
4: sans rien réentraîner ?* Campagne complète sur Qwen2.5-0.5B Q8_0, deux jeux de
5: 1 024 tokens (A pour le réglage, **B tenu à l'écart** pour la vérification), plus
6: un contrôle en contexte 512 et sur 2 040 tokens.
7: 
8: Toutes les mesures de perplexité et de comptes d'événements sont **déterministes**
9: — mêmes tokens, même résultat au chiffre près. Seules les mesures de **temps**
10: sont bruitées (la machine tournait sous une charge de 8 à 22).
11: 
12: ---
13: 
14: ## 1. Ce qui survit à la coupure, et ce qui n'y survit pas
15: 
16: | où l'on coupe | tolérance mesurée | verdict |
17: |---|---|---|
18: | **poids d'attention** (top-k clés) | **améliore** de 0,5 à 1,2 % | ✅ à garder |
19: | activations du FFN (k-WTA 90 %) | +0,15 à +0,28 % | ✅ acceptable |
20: | activations du FFN (k-WTA 85 %) | +0,5 à +1,2 % | ⚠️ selon le budget |
21: | entrée des projections d'attention (90 %) | +0,06 % | ✅ quasi gratuit |
22: | **Q 
… [3777 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-capteur-hebbien.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cpu-aer.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-capteur-hebbien.md</path>
<type>file</type>
<content>
1: # Capteur hebbien — apprendre des logs d'activation
2: 
3: *Réponse mesurée à : « peut-on avoir un flux de listes d'activations
4: post-traité sur une autre ressource pour apprendre de ces logs, et créer de
5: nouveaux nœuds par un principe hebbien ? »*
6: 
7: **Réponse courte : le capteur est presque gratuit et il fonctionne — mais la
8: création de nœuds par Hebb n'ajoute rien sur 69 % des poids du modèle, pour une
9: raison mathématique vérifiée sur les données.**
10: 
11: ---
12: 
13: ## 1. Le capteur, et ce qu'il coûte
14: 
15: `drave-core --hebbian L --hebb-q Q --hebb-out F` branche un accumulateur sur
16: une projection : `H[o][i] += y[o] · x[i]`, **uniquement pour les sorties qui
17: « déchargent »** (|y| au-dessus du quantile Q). C'est le principe neuromorphique :
18: seuls les neurones qui tirent apprennent. Il ne modifie jamais le calcul.
19: 
20: Mesure sur 1 025 tokens de WikiText-2, couche 12, projection `ffn_gate`
21: (4 864 × 896), quantile 0,1 :
22: 
23: | | Temps |
24: |---|---|
25: | sans capteur | 96,75 s |
26: | avec capteur | 99,64 s |
… [4908 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cpu-aer.md</path>
<type>file</type>
<content>
1: # Drave — l'architecture « push » (AER) sur CPU
2: 
3: ## L'architecture
4: 
5: Au lieu de **tirer** les activations à des indices arbitraires (gather), on
6: **pousse** : chaque source active émet un événement, sa liste de destinations se
7: lit **séquentiellement**, et on disperse `acc[dest] += signe · x[src]`.
8: 
9: - la liste d'activation se construit **en cascade** (compaction des non-nuls) ;
10: - l'accès aléatoire se déplace de l'entrée (activation, large) vers la sortie
11:   (accumulateur, 4096 × 24 bits = **12 Kio**, tient dans les M20K) ;
12: - les poids se lisent en **flux séquentiel** : plus aucun gather.
13: 
14: ## Mesures sur ce bi-Xeon E5-2687W v3
15: 
16: - bande passante lecture séquentielle : **11.5 Go/s**
17: - dispersion (`np.bincount`) : **183999808.87 G événements/s**
18: - dispersion (`np.add.at`) : 364797216.41 G événements/s
19: 
20: ## Limites mesurées du CPU (bench/cpu_aer.c, 16 threads)
21: 
22: | Test | 1 th | 8 th | 16 th | 32 th |
23: |---|---|---|---|---|
24: | Lecture séquentielle | 4,1 Go/s | 23,4 | **28,7** | 28,2 |
25: | Dispe
… [2395 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md</path>
<type>file</type>
<content>
1: # Cohérence des documents avec le code — audit
2: 
3: **En une ligne** : **80 affirmations** vérifiées une par une contre le code (et
4: contre les traces réelles du disque) ; **38 sont fausses (PÉRIMÉ)**, **15 se
5: contredisent entre documents (CONTRADICTOIRE)**, **10 existent dans le code et
6: manquent aux documents (MANQUANT)**, **17 tiennent (OK)** — les trois plus graves
7: touchent la **version du protocole de flux** (deux binaires « v3 » aux contrats
8: différents se croient compatibles), un **échappement d'indice écrit sur 4 octets et
9: lu sur 2** en mode blocs, et `REPRISE.md` §6bis (pourtant écrit il y a une heure)
10: déjà faux sur quatre points.
11: 
12: ## Révision auditée, méthode, réserves
13: 
14: | | |
15: |---|---|
16: | Commit de référence | `ae85043` (2026-09-30 12:30) |
17: | `drave-core/src/main.rs` | sha256 `d5e90136…` · 3 112 lignes |
18: | `drave-core/src/model.rs` | sha256 `3e5dde2d…` · 3 872 lignes |
19: | Traces relues | `/tmp/flux_v2.bin` (66 370 408 o, en-tête `DRVF` version **2**), `/tmp/flux_v3.bin` (version **3**) |
20: 
2
… [26190 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md</path>
<type>file</type>
<content>
1: # Cohérence des documents avec le code — second passage
2: 
3: **En une ligne** : **66 affirmations** revérifiées contre le code et les rapports
4: **après** les changements du 30/09 ; **27 tiennent**, **17 sont périmées**, **14 se
5: contredisent** et **8 manquent** — les deux plus graves sont le **chiffre vedette du
6: cache KV** (« 75 % / 50 % » contre « 64 % / 28 % » dans le rapport qui l'a mesuré) et
7: la règle **R4** dont la moitié (`n == 0` refusé) n'est **pas** dans le code alors que
8: le plan affirme le contraire.
9: 
10: ## Révision auditée, méthode, réserves
11: 
12: | | |
13: |---|---|
14: | Commit de référence | `a383cd7` (2026-09-30 15:11) |
15: | `drave-core/src/main.rs` | sha256 `bc53a66ad757faa6…` · 3 508 lignes |
16: | `drave-core/src/model.rs` | sha256 `61582adb8ded0f25…` · 3 928 lignes |
17: | Total `.rs` du moteur | **11 901 lignes** (7 fichiers) |
18: | Arbre au moment d'écrire | `journal/` modifié, `docs/plan-mode4-lot-listes.md` non suivi ; **73 commits** dans la journée |
19: 
20: Trois réserves, parce qu'elles changent la portée
… [29138 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-vision.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-compacite-trace.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-vision.md</path>
<type>file</type>
<content>
1: # Cohérence des `docs/` avec la vision Drave — révision du 02/10
2: 
3: **En une ligne** : les **18 documents** de `docs/` (4 870 lignes) ont été relus par
4: **cinq relectures adverses** puis corrigés un par un — **88 sites de correction**
5: dans `docs/` (95 avec `REPRISE.md`, comptés dans le diff), plus une **sixième
6: relecture adverse du diff lui-même**, qui a trouvé 13 défauts de plus (dont un
7: faux que j'avais introduit) ; le verdict est que **la
8: vision est tenue partout, mais qu'elle était muette dans quatre documents** (le
9: format, le transport, les grappes et le découpage en clusters ne disaient nulle
10: part qu'ils servent à *router des flux sur des grappes réparties* ni à *lire ces
11: flux pour adapter l'architecture*) — c'est la seule incohérence **de fond**
12: trouvée, et elle est corrigée. Le reste est de la **péremption datée** : des
13: chiffres ou des états de statut qui décrivaient l'état d'hier et contredisaient le
14: code d'aujourd'hui.
15: 
16: ## 1. Méthode
17: 
18: | étape | ce qui a été fait |
19: |---|---|
20: | 1. cad
… [14046 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-compacite-trace.md</path>
<type>file</type>
<content>
1: # Compacité de la trace — le disque paie trois fois le câble
2: 
3: > **Fait depuis (même jour).** La variante « écarts » est **implémentée et
4: > mesurée** dans le moteur (DRVF v2, lecteur rétrocompatible v1) : trace dense de
5: > 512 jetons **132 396 736 → 66 370 408 octets (−49,87 %)**, rejeu `--flux-forcer`
6: > **identique** (perplexité 19,3885 dans les deux cas), et la relecture par
7: > `tools/flux_codec.py` — l'implémentation indépendante — donne exactement les
8: > mêmes 24 576 listes et 22 008 776 neurones actifs. Le rejeu annonce maintenant
9: > ses compteurs (`N listes servies, M manquantes`), ce qui a mis au jour une
10: > trace ancienne dont les clés étaient décalées d'un jeton : elle se rejouait en
11: > silence avec une perplexité fausse (1958,72 au lieu de 19,3885).
12: >
13: > **Et la v3 est faite** (`DRAVE_TRACE_BLOCS=1`) : valeurs i8 + échelle f16 par
14: > bloc de 32 canaux. Mesuré sur la même trace dense : **45 079 930 octets**
15: > (−65,9 % par rapport à la v1, −32,1 % par rapport à la v2), au prix de
16: > **+0,074 % de perplexité 
… [15264 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-croisement-push-pull.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-decoupage-moe.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-croisement-push-pull.md</path>
<type>file</type>
<content>
1: # Croisement push / pull — quand l'architecture événementielle est-elle justifiée ?
2: 
3: Deux façons d'exécuter le même modèle quantifié :
4: 
5: - **push** (notre architecture) : pour chaque source active, on *disperse* ses
6:   poids dans un accumulateur (`acc[dest] += x·w`). Le flux est indexé par
7:   source, un événement = écart + valeur, 2 octets.
8: - **pull** (le noyau dense ordinaire) : pour chaque sortie, on *lit* sa ligne de
9:   poids et on fait un produit scalaire. 1 octet par poids, aucune dispersion.
10: 
11: Elles donnent **exactement le même résultat** — vérifié : perplexité 19,2647 au
12: chiffre près sur 510 jetons, tokens identiques, en écrivant les deux chemins avec
13: le même ordre d'opérations (les sommes entières sont exactes des deux côtés).
14: 
15: > ⚠️ **Corrigé le 27/09** : le tableau de croisement de la section 1 mesurait
16: > « push » contre « dense » alors que le drapeau `--dense`, placé en dernier
17: > argument, n'était jamais lu (`while i + 1 < args.len()`), et le mode dense
18: > sommait des tranches périmées. Le
… [5667 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-decoupage-moe.md</path>
<type>file</type>
<content>
1: # Rapport — découpage des MoE en clusters, pour notre mode d'opération
2: 
3: **En une ligne** : sur Qwen3-30B-A3B (128 experts, 8 par jeton), regrouper les
4: experts par **fréquence d'usage** suffit à diviser par ~1,8 la ventilation d'un
5: jeton (3,08 nœuds au lieu de 5,32 au hasard, à 8 clusters) — et la co-activation,
6: qui devait faire mieux, donne **exactement la même partition** (accord 1,000). Le
7: découpage n'a donc pas besoin d'un algorithme de graphes : il a besoin d'un
8: **ordre**, et d'un format qui le respecte.
9: 
10: ## Pourquoi cette question
11: 
12: Notre mode d'opération est événementiel et réparti : un jeton ne lit que les
13: experts qu'il allume, et si les experts sont sur des nœuds différents, il faut
14: autant d'allers-retours que de nœuds concernés. Les compteurs d'usage existants
15: disaient quels experts sont **chauds** ; ils ne disaient pas lesquels sont chauds
16: **ensemble**. C'est cette seconde information qui décide du placement.
17: 
18: ## La chaîne de mesure
19: 
20: 1. **Trace de routage dans le moteur** — `DRAVE_TR
… [5929 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md</path>
<type>file</type>
<content>
1: # Drapeaux et variables « analysés mais jamais appliqués » — audit systématique
2: > **Addendum (mêmes jour, après l'audit).** Les défauts n°1 (top-k non transportés
3: > ni appliqués dans les modes flux), n°2 (`--keep` en `--ppl`), n°3 (`--ffn-gain`
4: > en `--infer`) et la moitié basse du tableau (`--threads` en FS/PR/BM, `--hebb-q`,
5: > `--hebb-out`, `--plan` sans `--ctx`, précédence de fenêtre, pas de 2 du mode par
6: > défaut) ont été **corrigés** dans les commits `7522289` et le suivant. Le
7: > protocole de flux est passé en **version 4** (puis 5, avec le mode « lot en
8: > listes ») : le contrat d'activation transporte
9: > désormais aussi les sept top-k par projection, `--attn-topk`, `--qk-topk` et
10: > `--moe-topk`. Les sections ci-dessous décrivent l'état AVANT correction — elles
11: > restent la référence de ce qui a été trouvé, et la liste de ce qui reste
12: > (`--banc-vision` sans `Options`, `--bits` du noyau GPU, etc.).
13: >
14: > **Addendum 2 (même jour, 15h).** La recommandation principale de ce rapport est
15: > FAITE : `--options-act
… [20355 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification par grep des termes rares et des premières occurrences

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && for t in Sinkhorn Hadamard SwiGLU LoRA MTP TLB AVX2 HBM greffon MTok \"p50\" \"p95\" \"p90\" SIMD OpenMP PTX Numba OpenBLAS BPE NuMA O_DIRECT zstd DMA pread madvise HMB UPI NVLink QSFP JTAG ALM M20K CDC QUESTA Questa iverilog … [666 caractères tronqués]`

  ```
=== Sinkhorn
=== Hadamard
=== SwiGLU
=== LoRA
=== MTP
=== TLB
=== AVX2
=== HBM
=== greffon
=== MTok
=== p50
=== p95
=== p90
rapport-aiguille-topk.md:133:| `--lot 256` | 13,1359 | **0,0007** (médiane 0,0003, p90 0,0017, max 0,0068) | **511/511** |
rapport-aiguille-topk.md:136:(max 6,8e-3, p90 1,7e-3), et le jeton choisi est le même PARTOUT : ce n'est pas un chemin faux, c'est une
=== SIMD
rapport-cpu-aer.md:63:> d'un noyau optimisé (SIMD, multi-thread, accumulateurs par banc) peut aller
=== OpenMP
rapport-cpu-aer.md:64:> plus vite que `np.bincount` ; à confirmer avec un noyau C/OpenMP avant de
=== PTX
rapport-coherence-docs-2.md:117:| 53 | `REPRISE.md:446` | carte du dépôt : `gpu/drave_gpu.cu + .ptx` | les noyaux sont dans **`drave-core/gpu/`** (`include_str!("../gpu/drave_gpu.ptx")`) ; la ligne est placée sous un bloc titré `drave-core/src/`, donc elle se lit `drave-core/src/gpu/…` — le correctif de l'audit n°1 a déplacé la ligne sans lever l'ambiguïté | PÉRIMÉ |
rapport-coherence-docs.md:143:| 72 | `REPRISE.md:323` | carte du dépôt : `gpu/drave_gpu.cu + .ptx` | les noyaux sont dans `drave-core/gpu/drave_gpu.{cu,ptx}` (chargés par `include_str!("../gpu/drave_gpu.ptx")`) | PÉRIMÉ |

… [8838 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && for t in grappe paire shard engram \"porte\" \"hyper-connexion\" \"valuée\" DRVF \"mode 4\" Mbit \"Q4_1\" \"Q5_1\" \"I8\" \"I32\" \"hc_mult\" \"output_hc\" \"attn_sinks\" \"attn_mla\" \"glm-dsa\" \"deepseek2\" \"SpikeGPT\" \" … [697 caractères tronqués]`

  ```
=== grappe
rapport-architecture-memoire.md:56:## 4. La règle de placement, par couche et par grappe
rapport-architecture-memoire.md:70:**Par grappe** : les experts d'un même cluster doivent être **contigus sur le
rapport-campagne-parcimonie.md:74:   avec moins de couches, faire des grappes, récurser » suppose un modèle qui a
rapport-coherence-vision.md:9:format, le transport, les grappes et le découpage en clusters ne disaient nulle
=== paire
rapport-aiguille.md:98:3. **Sondes par paires** : la même information à deux profondeurs différentes
rapport-architecture-memoire.md:249:### Les paires hyperthread : utiles quand les cœurs manquent
rapport-architecture-memoire.md:265:cœurs seuls, parce que deux fils d'une même paire masquent mutuellement la
rapport-architecture-memoire.md:273:dix cœurs devrait prendre **vingt fils sur les paires HT** — soit `--pin` avec un
=== shard
rapport-architecture-memoire.md:373:| DeepSeek-V4-Flash (3 shards) | 86,90 Go | 0,07 s | 35 Mo |
rapport-coherence-vision.md:68:| `plan-deepseek-v4-flash.md` | **corrigé, 11 sites** | bandeau : lecteur multi-shards **fait**, V4.1-Flash a un **GGUF Q2** (365,71 Go), MLA **faite** ; gpt-oss = 128 experts **top-4** (e
… [8127 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rédaction du livrable : section A (termes et sigles)

- **send_message** `{"agent_id": "3d5618a0-4e3a-45bb-943d-a72c753fb7da", "message": "INVENTAIRE — partie 1/3 (section A). Les 20 rapports ont été lus intégralement. Aucun fichier modifié.\n\n## A. Termes et sigles\n\n**Architecture événementielle / matériel**\n- **aiguille (test de l'aiguille, « l'aiguille dans la bott … [19406 caractères tronqués]`

  ```
message delivered to agent 3d5618a0-4e3a-45bb-943d-a72c753fb7da
  ```

### 🤖 Assistant

⏵ Rédaction du livrable : section B (chiffres et mesures)

- **send_message** `{"agent_id": "3d5618a0-4e3a-45bb-943d-a72c753fb7da", "message": "INVENTAIRE — partie 2/3 (section B). Citations exactes entre guillemets.\n\n## B. Chiffres et affirmations mesurées\n\n**reports/aiguille-30b.md**\n- `:2` — « lot 256, 40 jetons de réponse, 16 fils »\n- `:6` — « | 2048 | 0.1 | **oui**  … [40888 caractères tronqués]`

  ```
message delivered to agent 3d5618a0-4e3a-45bb-943d-a72c753fb7da
  ```

### 🤖 Assistant

⏵ Rédaction du livrable : sections C (contradictions) et D (fichiers cités)

- **send_message** `{"agent_id": "3d5618a0-4e3a-45bb-943d-a72c753fb7da", "message": "INVENTAIRE — partie 3/3 (sections C et D).\n\n## C. Contradictions, chiffres périmés, affirmations douteuses\n\n- `reports/bilan-multi-materiel.md:96` — « il est **8 % plus rapide** que le dense (15,8 contre 14,7 tok/s) » — contredit ` … [23102 caractères tronqués]`

  ```
message delivered to agent 3d5618a0-4e3a-45bb-943d-a72c753fb7da
  ```

### 🤖 Assistant

⏵ Livrable livré en 3 messages au parent ; récapitulatif final

Inventaire terminé : les 20 fichiers ont été lus intégralement (3 058 lignes), aucun fichier du dépôt n'a été modifié. Le livrable complet (sections A, B, C, D) a été transmis au parent en 3 messages :

1. **A. Termes et sigles** — ~150 entrées (AER, PE, ALM, M20K, CDC, NVLink, UPI, HMB, MLA, CSA/HCA, DRVF, mode 0-4, k-WTA, PTQ, engram, hyper-connexion, seuil_push, KvCache::assurer, toutes les `DRAVE_*` et les familles de drapeaux, outils…) avec définition, usage et première occurrence `reports/fichier.md:ligne`. Absents vérifiés par grep : Sinkhorn, Hadamard, SwiGLU, LoRA, MTP, TLB, AVX2, HBM, MTok/s, p50/p95, « greffon ».
2. **B. Chiffres et affirmations mesurées** — ~230 mesures citées entre guillemets avec `fichier:ligne`, fichier par fichier.
3. **C. Contradictions / périmés / douteux** — ~85 entrées ; **D. Fichiers du dépôt cités** — ~80 chemins avec leur rôle.

Points saillants pour la détection de contradictions :
- **×2,17** revendiqué comme gain mesuré en `rapport-8bits.md:56` alors que `bilan-multi-materiel.md:92` le déclare **retiré** (inégalité de Kraft violée).
- **Croisement push/pull** : « ~10 % » (`rapport-analyse-flux.md:14`) contre « ~22 %, pas à 10 % » (`rapport-croisement-push-pull.md:43`) — contradiction interne au corpus.
- **« Le mode liste bat le dense »** : `bilan-multi-materiel.md:96,103` reproduit exactement l'affirmation que `rapport-croisement-push-pull.md:66-77` démontre fausse (15,8/14,7 contre 15,59/36,43 tok/s).
- **FPGA** : PCIe Gen3 ×8 6,5 Go/s (`bilan:8`) contre « USB seulement, 625 Mo/s » (`rapport-architecture-memoire.md:385`), qui se contredit aussi avec « Pas de FPGA dans cette machine » (`:246`).
- **KV à 1 M** : 82 Ko/82 Go (`rapport-architecture-memoire.md:418`) contre 90 Ko/96,6 Go (`:96`) dans le même document.
- **Cache KV** : 64 %/28 % (`rapport-attribution-kv.md:33-35`) contre 75 %/50 % dans REPRISE/roadmap (relevé par `rapport-coherence-docs-2.md:97`).
- **k = 32** : 23,3302 dans le tableau de `rapport-attention-creuse.md:27` contre 23,3279 aux lignes 95/126 et dans `rapport-campagne-parcimonie.md:36`.
- Chiffres manifestement faux et signalés comme tels : dispersion `1.8e17 évts/s` (`rapport-cpu-aer.md:17-18`), 5,3 G évts/s attribué à 16 puis 32 fils (`bilan:46` vs `:54`), « 8 % plus rapide » (`bilan:96`), 11 440 vs 11 901 lignes, en-tête 39/26/79 octets, 3 623/3 663, 1 589/1 629, 1 989/≈1 419.
- Les trois rapports de cohérence sont **datés** (`ae85043` 12:30 → `a383cd7` 15:11 → révision du 02/10) et se corrigent mutuellement : VERSION_FLUX 3→4→5, 13→48 tests, 11 440→11 901 lignes.

