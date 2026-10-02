# Session DSH — relecture

- identifiant : `4e786d3f-0b66-4b23-8dc4-b452bc383bea`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-02 10:08:01
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu es un relecteur ADVERSARIAL. Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust nommé Drave). Tu ne dois MODIFIER AUCUN fichier : ta sortie est un rapport en markdown, rien d'autre. N'utilise que la lecture (read, grep, glob, bash en lecture seule). N'exécute aucun modèle (pas de forward, pas de --ppl) : les runs lourds sont déjà en cours.

CONTEXTE : une campagne de révision de cohérence documentaire vient d'être menée sur `docs/`, `REPRISE.md`, `tools/portes.sh` et `drave-core/src/model.rs`. Le diff non commité (`git diff`) contient toutes les corrections. Ta mission est de VÉRIFIER ces corrections, pas de les refaire.

Faits de référence à vérifier dans l'arbre (ne les crois pas sur parole : vérifie-les toi-même par grep/lecture) :
- protocole de flux : `VERSION_FLUX = 5`, 5 modes 0–4 (dont mode 4 « LOT en listes »), en-tête 79 octets — dans `drave-core/src/main.rs`.
- portes du dépôt : Qwen2.5-0.5B Q8_0 ctx 256 = 19,3885 ; Qwen3-30B en clusters ctx 64 limit 8 = 799,8557 ; gpt-oss-120b MXFP4 ctx 256 = 15,6017 (était 15,1757 avant le correctif de routage du 02/10) ; `cargo test --release` = 48 tests ; 18 formats lisibles / 17 vérifiés à la porte (`tools/portes_formats.sh` contre libggml).
- MLA à rang faible : validée contre llama.cpp sur GLM-5.3 à la position 0 (corrélation 0,999024), l'écart croît ensuite (+4,070 nat à la position 3) — `reports/rapport-mla-experts.md`.
- YaRN : le moteur ne bascule à l'interpolation qu'au-delà de 4 × la longueur déclarée — `drave-core/src/model.rs` (cherche `* 4.0`).
- KV : int8 = +1,5 % à 512 jetons et +3,0 % à 8 192 ; int4 = +219 % à 512 et +364 % à 8 192.
- préremplissage par lots : Qwen ctx 512 17,1 → 13,6 s (−20 %) ; gpt-oss ctx 256 ≈ 50 → 34,4 s (−31 %) — `reports/rapport-prefill-par-lots.md`.
- densité d'activation 17,9 % à seuil 5 % ; croisement push/pull à 22 % (`seuil_push = 0.22`) — `reports/rapport-localite-activation.md`, `reports/rapport-croisement-push-pull.md`.
- lecteur multi-shards fait : `Gguf::open_multi` dans `drave-core/src/gguf.rs`, `reports/rapport-lecteur-multifichiers.md`.

TÂCHES :
1. `git diff` puis `git diff -- docs/ REPRISE.md tools/portes.sh drave-core/src/model.rs` : lis toutes les corrections.
2. Pour CHAQUE correction, vérifie qu'elle est FACTUELLEMENT exacte et qu'elle ne crée pas une NOUVELLE incohérence (chiffre inventé, renvoi de fichier inexistant, contradiction avec un autre document, affirmation non mesurée présentée comme mesurée, tournure qui trahit la philosophie du projet).
3. Vérifie en particulier que chaque renvoi de fichier cité existe (`reports/...`, `docs/...`, `tools/...`) — teste-les par `ls`.
4. Vérifie que le diff de `drave-core/src/model.rs` ne casse rien : le correctif sépare `attn_derope` (vrai manque) de `attn_sinks` (implémenté). Cherche dans le code si `sinks` est bien utilisé dans le calcul d'attention, et si un modèle du parc autre que gpt-oss a `attn_sinks` sans `attn_derope` (ce qui changerait son verdict de calculabilité). Liste les fichiers GGUF disponibles dans /home/stephane/Data13TB/stephane/modeles/gguf/ et /home/stephane/FastNVMe/modeles-lourds/ et, pour ceux qui sont lisibles, dis lesquels contiennent `attn_sinks` (tu peux utiliser `grep -c attn_sinks` sur les en-têtes de fichiers GGUF, ou le binaire ./drave-core/target/release/drave <fichier> --config qui ne lit que les en-têtes et prend < 1 s).
5. Vérifie `tools/portes.sh` : le nouveau bloc gpt-oss (section 7) est-il syntaxiquement correct (`bash -n tools/portes.sh`) et logiquement cohérent (variables, fonction `valeur`, `compare`) ? Ne le lance pas.
6. Rends un tableau markdown : | fichier:ligne | citation exacte (≤ 25 mots) | problème | correction minimale (texte exact de remplacement) | gravité |. Si une correction est fausse, dis-le. Si tout est juste pour un fichier, dis-le explicitement dans une section « déjà cohérent, ne pas toucher ». Termine par les points à trancher par l'humain.

Sois précis et cite les lignes. Aucune flatterie, aucun résumé vague : des faits vérifiables.
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

⏵ Reading the uncommitted diff to inventory every documentation correction

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain && echo \"=== STAT ===\" && git diff --stat", "description": "Show git status and diff stat"}`

  ```
M REPRISE.md
 M docs/colab-reparti.md
 M docs/comparaison-spiking.md
 M docs/contexte-long.md
 M docs/convertisseur.md
 M docs/format-clusters.md
 M docs/format-flux.md
 M docs/plan-deepseek-v4-flash.md
 M docs/plan-deepseek41-complet.md
 M docs/plan-gpu-topk.md
 M docs/plan-mla-vision.md
 M docs/plan-mode4-lot-listes.md
 M docs/plan-modeles-lourds.md
 M docs/plan-prefill-reparti.md
 M docs/programme-recherche.md
 M docs/roadmap.md
 M docs/sprints.md
 M docs/vision.md
 M drave-core/src/model.rs
 M journal/README.md
 M tools/portes.sh
=== STAT ===
 REPRISE.md                      | 23 +++++++++++----
 docs/colab-reparti.md           |  7 ++++-
 docs/comparaison-spiking.md     | 23 ++++++++++++---
 docs/contexte-long.md           | 28 +++++++++++-------
 docs/convertisseur.md           | 55 +++++++++++++++++++++-------------
 docs/format-clusters.md         |  5 ++++
 docs/format-flux.md             | 13 ++++++---
 docs/plan-deepseek-v4-flash.md  | 58 +++++++++++++++++++++++-------------
 docs/plan-deepseek41-complet.md | 15 ++++++----
 docs/plan-gpu-topk.md           | 13 ++++++---
 docs/plan-mla-vision.md         | 25 +++++++++++-----
 docs/plan-mode4-lot-listes.md   | 30 +++++++++
… [549 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -5 && echo \"=== branch ===\" && git branch --show-current", "description": "Show recent git log and branch"}`

  ```
5a6ac96 Plan V4.1, version 2 : les flux d'abord — c'est ce qui distingue Drave
386c857 Plan pour exécuter DeepSeek-V4.1 : neuf phases, chacune avec sa porte
e3a802d Test d'exécution de DeepSeek-V4.1 : tout ce qui tourne est mesuré, la passe avant est refusée en 0,33 s
acc3498 L'écart naît APRÈS la couche 0 : 1,9 % / 1,3 % / 3,8 % / 4,0 % aux positions 0-3
9d20a8b Rapport MLA : annexe sur l'écart à la position 3 — ce qui est exclu, ce qui reste
=== branch ===
master
  ```

### 🤖 Assistant

⏵ Dumping the full diff, then verifying each claim against the tree

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- drave-core/src/model.rs tools/portes.sh REPRISE.md journal/README.md", "description": "Diff of model.rs, portes.sh, REPRISE.md"}`

  ```
diff --git a/REPRISE.md b/REPRISE.md
index e256ad6..3c5deda 100644
--- a/REPRISE.md
+++ b/REPRISE.md
@@ -36,6 +36,15 @@ cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && cargo build --r
 > gpt-oss était la seule que la relecture adversariale n'avait pas pu faire
 > tourner (bornes de temps) ; elle est verte.
 >
+> **Mise à jour du 02/10 — c'est ce bloc qui fait foi** : Qwen2.5-0.5B Q8_0
+> ctx 256 = **19,3885** (inchangée) · clusters Qwen3-30B ctx 64 limit 8 =
+> **799,8557** · gpt-oss-120b MXFP4 ctx 256 = **15,6017** (**changée** par le
+> correctif de routage : le biais `exp_probs_b` ne doit pas entrer dans le softmax
+> des poids — `reports/rapport-routage-experts.md`) · `cargo test --release` =
+> **48** · protocole **v5**, modes 0–4. Les lignes gpt-oss plus bas qui portent
+> encore 15,1757, 15,1667, 15,0757 ou 18,5803 datent d'AVANT ce correctif : à
+> revérifier avant de s'en servir comme porte.
+>
 > **Chemin GPU revérifié le même jour** (personne ne l'avait exercé depuis les
 > changements) : gpt-oss avec `DRAVE_GPU=1` donne **15,1667**, la valeur attendue
 > du pilote, et `--gpu-banc` retrouve l'exactitude des noyaux — 1,6 ms par ligne
@@ -67,7 +76,7 @@ ide
… [12922 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- docs/ > /tmp/diff_docs.txt && wc -l /tmp/diff_docs.txt && head -250 /tmp/diff_docs.txt", "description": "Diff of docs, first half"}`

  ```
969 /tmp/diff_docs.txt
diff --git a/docs/colab-reparti.md b/docs/colab-reparti.md
index eef963f..f6d13dc 100644
--- a/docs/colab-reparti.md
+++ b/docs/colab-reparti.md
@@ -3,6 +3,11 @@
 Objectif : deux machines qui se passent des **listes d'activation**, l'une sur le
 runtime Colab, l'autre en local, et **les mêmes logits** qu'en local.
 
+Ce flux est aussi le **journal** qu'on relit (`--trace-flux`, puis
+`tools/analyse_flux.py`, `profil_flux.py`, `diff_flux.py`) pour comprendre où
+travaille le modèle et adapter l'architecture à la tâche — la fidélité du
+transport n'est pas le seul enjeu (`docs/vision.md` §2).
+
 Ce document est la recette ; l'état du protocole et les chiffres qui la
 dimensionnent sont dans `docs/format-flux.md` et
 `reports/rapport-transport-liste.md`.
@@ -34,7 +39,7 @@ paie pas la latence 256 fois.
 
 ## Dimensionnement (mesuré)
 
-* **Débit** : 3 663 octets par flux en dense (en-tête v4 compris), ≈ 1 419 en
+* **Débit** : 3 663 octets par flux en dense (en-tête **v5** compris), ≈ 1 419 en
   listes à échelle par bloc à 68 % d'activité. En **lots** (`--lot 64`), c'est
   229 455 octets par lot de 64 jetons, soit **3,5 ko par jeton** — et surtout UN
   aller-r
… [16651 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the remaining docs diff before verifying claims

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '250,600p' /tmp/diff_docs.txt", "description": "Read docs diff lines 250-600"}`

  ```
+fichiers : c'est la carte des grappes entre composants et machines.
+
 Outil : [`tools/convertir_clusters.py`](../tools/convertir_clusters.py).
 
 ## Le problème
diff --git a/docs/format-flux.md b/docs/format-flux.md
index f56cc70..29569a4 100644
--- a/docs/format-flux.md
+++ b/docs/format-flux.md
@@ -1,15 +1,19 @@
 # Le format de flux (DRVF) — spécification
 
-Ce format sert **trois choses à la fois**, et c'est délibéré :
+Ce format sert **quatre choses à la fois**, et c'est délibéré :
 
 1. la **trace** d'exécution (`--trace-flux`) : ce qui s'est passé, couche par
    couche ;
 2. le **rejeu** (`--flux-forcer`) : on réinjecte les activations enregistrées et
    le calcul repart de là ;
 3. le **transport** (phase 3, `--flux-serveur` / `--ppl-reparti`) : ce qu'un nœud
-   distant reçoit pour continuer le calcul.
+   distant reçoit pour continuer le calcul ;
+4. l'**analyse** : les mêmes octets, relus par `tools/profil_flux.py`,
+   `tools/analyse_flux.py` et `tools/diff_flux.py`, disent quels neurones
+   travaillent — c'est la donnée qui permet d'adapter l'architecture à la tâche,
+   et c'est la finalité du projet (`docs/vision.md` §2).
 
-Un seul format pour les trois, parce q
… [22637 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the last part of the docs diff

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '600,969p' /tmp/diff_docs.txt", "description": "Read docs diff lines 600-969"}`

  ```
en-tête de 79 octets (mode 4, `n = t`, échelle 0, `Act::du_modele`), puis
    **un seul** `Vec<u8>` de corps construit ainsi :
@@ -290,7 +295,8 @@ même ordre que l'aller (÷2,3) ; c'est la ligne `octets_recus` qui le prouvera.
 
 ## 6. La vérification
 
-### 6.1 Commande exacte (localhost, Qwen2.5-0.5B, 12 couches par nœud)
+### 6.1 Commande exacte (localhost, Qwen2.5-0.5B, 12 couches par nœud ; la même
+campagne entre **deux machines** reste à faire — `docs/colab-reparti.md`)
 
 ```bash
 # terminal 1 — le nœud moteur : inchangé
diff --git a/docs/plan-modeles-lourds.md b/docs/plan-modeles-lourds.md
index d42bd01..452b2aa 100644
--- a/docs/plan-modeles-lourds.md
+++ b/docs/plan-modeles-lourds.md
@@ -19,13 +19,21 @@ publiés, sans les requantifier.
 
 | modèle | pourquoi lui | plus petit GGUF | contexte | état |
 |---|---|---|---|---|
-| **DeepSeek-V4.1-Flash** | le plus lourd des ouverts, MoE, agentique | **365,7 Go** (Q2) | — | **en cours** (26 % à 09h36) |
+
+> **Où en est ce plan (02/10)** : les 24 fichiers sont arrivés ; le lecteur
+> multi-fichiers, les métadonnées et le tokenizer sont **faits** ;
+> `deepseek2` (Kimi-K2.7) et `glm-dsa` (GLM-5.3) **se calculent** ; restent
+> `de
… [26158 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying protocol facts, gate values, and file references in the tree

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"VERSION_FLUX\\|TAILLE_TETE\\|MODE_LOT\\|MODE_DENSE\\|MODE_LISTE\\|MODE_BLOCS\\|MODE_PREFILL\" drave-core/src/main.rs | head -40", "description": "Check flux protocol constants"}`

  ```
1862:const VERSION_FLUX: u8 = 5;
1864:const MODE_DENSE: u8 = 0;
1868:const MODE_LISTE: u8 = 1;
1873:const MODE_BLOCS: u8 = 2;
1879:const MODE_LOT: u8 = 3;
1886:const MODE_LOT_LISTES: u8 = 4;
1897:const TAILLE_TETE: usize = 4 + 1 + 1 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 1
2048:    let mut t = Vec::with_capacity(TAILLE_TETE);
2050:    t.push(VERSION_FLUX);
2065:    assert_eq!(t.len(), TAILLE_TETE,
2066:               "en-tête de flux de {} octets pour {TAILLE_TETE}", t.len());
2133:    let (n, echelle, corps): (usize, f32, Vec<u8>) = if mode == MODE_BLOCS {
2151:    } else if mode == MODE_LISTE {
2169:    Ok((TAILLE_TETE + corps.len(), n))
2180:    let tete = tete_flux(MODE_LOT, debut, fin, pos0, t, 0.0, Some(mdl));
2186:    Ok(TAILLE_TETE + corps.len())
2216:    let tete = tete_flux(MODE_LOT_LISTES, debut, fin, pos0, t, 0.0, Some(mdl));
2220:    Ok(TAILLE_TETE + corps.len())
2226:    let mut tete = [0u8; TAILLE_TETE];
2235:    if version != VERSION_FLUX {
2238:            format!("flux en version {version}, cette build parle la {VERSION_FLUX} \
2265:    if n == 0 && matches!(mode, MODE_DENSE | MODE_LOT | MODE_LOT_LISTES) {
2268:                    if mode == MODE_DENSE { "canal" } else
… [982 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"\\* 4\\.0\\|4\\.0 \\*\\|yarn\" drave-core/src/model.rs | head -30", "description": "Check YaRN 4x threshold in model.rs"}`

  ```
429:    pub yarn: Option<(f32, f32, f32, f32, bool)>,
2151:            //   `DRAVE_YARN_NON=1`  jamais de YaRN (ce que fait `--sans-yarn`) ;
2168:            yarn: {
2170:                    Some("yarn") => Some((
2172:                        g.cfg("rope.scaling.yarn_beta_fast").and_then(|m| m.as_f64()).unwrap_or(32.0) as f32,
2173:                        g.cfg("rope.scaling.yarn_beta_slow").and_then(|m| m.as_f64()).unwrap_or(1.0) as f32,
2203:                    Some(y) if !jamais && ctx as f32 > y.3 * 4.0 => Some(y),
2397:                 if cfg.yarn.is_some() { "yarn " } else { "" },
2417:                 cfg.yarn.map(|y| format!(" · yarn ×{}", y.0)).unwrap_or_default());
2447:        match (cfg.yarn, g.cfg("rope.scaling.original_context_length").and_then(|m| m.as_u64()),
2881:    pub fn cfg_yarn_off(&mut self) { self.cfg.yarn = None; }
3136:    /// RoPE avec étirement **YaRN** (`rope.scaling.type = yarn`).
3145:    fn rope_yarn(v: &mut [f32], n_head: usize, head_dim: usize, pos: usize, base: f32,
3419:                match self.cfg.yarn {
3421:                        Self::rope_yarn(qi, nh, hd, pos, self.cfg.rope_base, f, bf, bl, orig, ms, self.cfg.n_rot);
3422:                
… [424 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"seuil_push\\|0\\.22\\|17,9\\|0,179\" reports/rapport-localite-activation.md reports/rapport-croisement-push-pull.md 2>/dev/null | head -30", "description": "Check activation density and push/pull crossover"}`

  ```
reports/rapport-localite-activation.md:24:| opérateurs creux par neurone | chemin par **listes d'événements** (`SparseVec`, push) | bascule push/pull mesurée à **22 % de densité** (`seuil_push = 0.22`) |
reports/rapport-localite-activation.md:43:| densité d'activation (seuil 5 % du max) | **17,9 %** des neurones par jeton (82 % ne font rien) |
reports/rapport-croisement-push-pull.md:48:Le seuil de bascule `seuil_push` est passé de 0,15 à **0,22**.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | head -80 && echo \"=== count ===\" && ls reports/ | wc -l", "description": "List reports directory"}`

  ```
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
rapport-coherence-vision.md
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
rapport-lecteur-multifichiers.md
rapport-localite-activation.md
rapport-logits-gpu-vs-cpu.md
rapport-minimal.md
rapport-mla-experts.md
rapport-mode4-lot-listes.md
rapport-modele-reel.md
rapport-mode-listes.md
rapport-mur-memoire-4bits.md
rapport-optimisations-auto.md
rapport-optimisations.md
rapport-parcimonie-imposee.md
rapport-passage-a-l-echelle.md
rapport-phase3-reparti.md
rapport-placement-bits-kv.md
rapport-precision.md
rapport-prefi
… [273 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Computing header size and testing every file reference added by the diff

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1890,1905p' drave-core/src/main.rs && echo \"=== test ===\" && grep -n \"TAILLE_TETE\" drave-core/src/main.rs | tail -5", "description": "Read TAILLE_TETE definition"}`

  ```
///
/// Les réglages voyagent parce qu'ils CHANGENT LES CHIFFRES : deux nœuds lancés
/// avec des `--act-thresh` différents ne calculent pas la même chose, et la
/// divergence serait silencieuse. Mesuré : 0,69 d'écart de perplexité avec un
/// seuil 0,05 d'un côté et 0,00 de l'autre, sur le même modèle.
// magie · version · mode · plage · position · n · échelle · niveaux · seuil ·
// top-k · renorm · attn_topk · qk_topk · moe_topk · topk_proj[7]
const TAILLE_TETE: usize = 4 + 1 + 1 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 1
                            + 4 + 4 + 4 + 7 * 4;

/// Réglages d'activation d'un nœud : ils font partie du contrat d'échange.
#[derive(Clone, Copy)]
struct Act {
    levels: f32,
    thresh: f32,
    topk: u32,
=== test ===
2757:        octets_recus += TAILLE_TETE as u64 + rep.octets_corps as u64;
4629:        assert_eq!(TAILLE_TETE, 79, "l'en-tête de flux doit faire 79 octets");
4678:        assert_eq!(octets, TAILLE_TETE + 32,
4711:        assert_eq!(t.len(), TAILLE_TETE);
4898:            assert_eq!(tete.len(), TAILLE_TETE);
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -U0 | grep '^+' | grep -v '^+++' | grep -oE '`[^`]+\\.(md|rs|py|sh|txt|gguf|tsv)`' | tr -d '`' | sort -u > /tmp/refs.txt; wc -l /tmp/refs.txt; while read -r f; do if [ ! -e \"$f\" ]; then echo \"MISSING: $f\"; fi; done < /tm … [72 caractères tronqués]`

  ```
40 /tmp/refs.txt
MISSING: diff_flux.py
MISSING: model.rs
MISSING: profil_flux.py
  ```

### 🤖 Assistant

⏵ Checking markdown links and non-backticked path references too

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -U0 | grep '^+' | grep -v '^+++' | grep -oE '\\((reports|docs|tools|journal)/[^)]+\\)' | tr -d '()' | sort -u > /tmp/links.txt; wc -l /tmp/links.txt; while read -r f; do [ -e \"$f\" ] || echo \"MISSING LINK: $f\"; done < /tm … [129 caractères tronqués]`

  ```
0 /tmp/links.txt
---
analyse_empreinte.py
analyse_experts_statique.py
analyse_flux.py
diff_flux.py
flux_codec.py
profil_flux.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in docs/histoire.md docs/plan-deepseek41-complet.md docs/plan-mla-vision.md docs/contexte-long.md docs/plan-gpu-topk.md docs/vision.md docs/format-clusters.md docs/format-flux.md reports/rapport-mla-experts.md reports/rapport-p … [877 caractères tronqués]`

  ```
OK docs/histoire.md
OK docs/plan-deepseek41-complet.md
OK docs/plan-mla-vision.md
OK docs/contexte-long.md
OK docs/plan-gpu-topk.md
OK docs/vision.md
OK docs/format-clusters.md
OK docs/format-flux.md
OK reports/rapport-mla-experts.md
OK reports/rapport-prefill-par-lots.md
OK reports/rapport-lecteur-multifichiers.md
OK reports/rapport-routage-experts.md
OK reports/rapport-mode4-lot-listes.md
OK reports/rapport-aiguille.md
OK reports/rapport-inference.md
OK reports/rapport-attention-creuse.md
OK reports/rapport-localite-activation.md
OK reports/bilan-multi-materiel.md
OK reports/rapport-croisement-push-pull.md
OK reports/rapport-placement-bits-kv.md
OK reports/rapport-programme-evolutif.md
OK reports/rapport-analyse-flux.md
OK reports/rapport-capteur-hebbien.md
OK reports/rapport-encodage.md
OK reports/rapport-execution-v41.md
OK reports/rapport-transport-liste.md
OK reports/rapport-gpt-oss-perplexite.md
OK reports/rapport-session-2026-09-30.md
OK reports/rapport-gpu-topk-selection.md
OK reports/rapport-gpu-scores.md
OK reports/rapport-8bits.md
  ```

### 🤖 Assistant

⏵ Cross-checking every quoted number against its source report

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== MLA ===\" && grep -n \"0,999024\\|0.999024\\|4,070\\|4.070\\|0,611\\|0,372\\|0,009\\|position 3\\|§7\" reports/rapport-mla-experts.md | head -30 && echo \"=== sections ===\" && grep -n \"^#\" reports/rapport-mla-experts.md … [59 caractères tronqués]`

  ```
=== MLA ===
112:| corrélation des logits (pos. 0) | **0,999024** |
178:| écart de NLL (nous − référence) | **+0,009** | +0,372 | +0,611 | **+4,070** | +3,118 | +2,041 | +1,583 |
180:Le saut est à la position 3, pas une dérive progressive : c'est le signe d'un
206:## Annexe — l'écart à la position 3 : ce qui est déjà exclu
=== sections ===
1:# Rapport — MLA à rang faible et formats sans noyau : GLM-5.3 et Kimi deviennent calculables
8:## 1. Les quatre verrous, dans l'ordre où ils sont tombés
20:## 2. Attention MLA (`attn_mla`)
53:## 3. Formats de super-bloc sans noyau
77:## 4. Deux bugs trouvés en chemin, tous deux dans du code déjà publié
90:## 5. Ce qui est mesuré
102:## 6. GLM-5.3 tourne, et son résultat est validé
135:## 6bis. Le bug, et comment il a été trouvé
151:## 6ter. Kimi-K2.7 : 1 026 G poids, premier calcul
170:## 7. Ce qui reste ouvert, et qui est le plus important
172:### La validation s'arrête à la position 2, et c'est mesuré
206:## Annexe — l'écart à la position 3 : ce qui est déjà exclu
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== PREFILL ===\" && grep -n \"17,1\\|13,6\\|34,4\\|50 \\|−20\\|-20 %\\|31 %\" reports/rapport-prefill-par-lots.md | head -25", "description": "Verify prefill report figures"}`

  ```
=== PREFILL ===
124:Bout en bout, sans profil (qui ajoute ses propres horloges) : **17,1 s → 13,6 s,
125:soit −20 %**, à perplexité identique (13,1368 → 13,1359). Sur gpt-oss (MoE
126:regroupé par expert, contexte 256, 255 jetons) : lot 1 ≈ 50 s, lots 64/128/256 =
127:**33,7 / 33,9 / 34,4 s**, perplexité 13,7205 dans tous les cas.
193:| Qwen2.5-0.5B Q8_0, `--dense`, 16 fils | 512 | 17,1 s | **13,6 s** | **−20 %** |
194:| gpt-oss-120b MXFP4, MoE groupé, 16 fils | 256 | ≈ 50 s | 34,4 s (lot 256) | **−31 %** |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== ROUTAGE ===\" && grep -n \"15,6017\\|15.6017\\|15,1757\\|exp_probs_b\" reports/rapport-routage-experts.md | head -20 && echo \"=== GPTOSS PPL ===\" && grep -n \"39,80\\|39.80\\|20,84\\|20.84\\|63 jetons\" reports/rapport-g … [86 caractères tronqués]`

  ```
=== ROUTAGE ===
66:| gpt-oss-120b ctx 256 | 15,1757 | **15,6017** | **changée** — voir ci-dessous |
72:dans le softmax. **15,1757 était auto-cohérent, pas juste.**
126:| drave, YaRN **à retardement** (le défaut) | **15,6017** |
162:  elle doit confirmer ou contredire 15,6017. C'est la seule mesure qui tranche
=== GPTOSS PPL ===
12:(39,8 à 63 jetons, 129,9 à 511). Trois hypothèses étaient en lice : le gabarit
24:Mesure, 63 jetons, tout le reste identique :
26:| | perplexité (63 jetons) |
28:| avant (biais O ignoré) | **39,80** |
29:| après (biais O chargé) | **20,84** |
72:| 63 jetons, YaRN (la configuration déclarée par le modèle) | **38,37** | **41,11** |
82:63 jetons et 169,7 à 511. gpt-oss est un modèle de raisonnement entraîné en
89:| configuration | 63 jetons | 511 jetons (une fenêtre) |
91:| RoPE simple (défaut du moteur) | **20,84** | **18,58** |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== KV 219 ===\" && grep -rn \"219\\|384\\|364\\|1,5 %\\|3,0 %\" reports/rapport-placement-bits-kv.md reports/rapport-attribution-kv.md 2>/dev/null | head -25", "description": "Verify KV int4 219% figure"}`

  ```
=== KV 219 ===
reports/rapport-placement-bits-kv.md:22:| int4 | int4 | 1,25 | 16 % | 66,0369 | **+364 %** |
reports/rapport-placement-bits-kv.md:30:16 %  int4/int4 ................ +364 %
reports/rapport-placement-bits-kv.md:52:   Et le 4 bits des DEUX côtés (1,25 octet, 16 % du f32) coûte **+364 %** : c'est
reports/rapport-attribution-kv.md:35:l'int8 complet (28 %, soit 2,25 octets) coûte +3,0 %. C'est le
  ```

### 🤖 Assistant

⏵ Hunting the +219 % int4 figure and other loose numbers

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"219\" reports/*.md docs/*.md REPRISE.md 2>/dev/null | head -25", "description": "Search for 219 percent claim"}`

  ```
reports/rapport-drapeaux-ignores.md:90:| `--act-thresh` `--act-topk` `--act-renorm` (et `--abits`→niveaux) | I (553-556) · P (2752-2754) · FS (1576→1216-1219) · PR (1676→1216-1219) | Corrigé récemment : ces quatre-là sont bien appliqués dans les modes flux | ✅ |
reports/rapport-execution-v41.md:18:| sonde engram (`--sonder-engram 10000`) | mmap, 16 lecteurs | table 1 : 10 000 entrées en **524 ms** (2,6 Mo touchés sur 101,4 Go) · table 2 : **219 ms** · RSS max **120 Mo** pour 365,7 Go adressés |
docs/contexte-long.md:103:| E3 | **KV int4** | **fait** (nibbles empaquetés) | 1 M tient en RAM (9,7 Go) et en VRAM | mesuré : **+219 %** à 512 jetons, **+364 % à 8 192** — llama.cpp q4_0 : +411 % puis +494 % ; à réserver aux cas où la mémoire manque |
docs/contexte-long.md:144:| int4 | 63,6107 (+384 %) | **41,9442 (+219 %)** | **49,9438 (+287 %)** |
docs/contexte-long.md:287:| 4 096 | CPU | 12,2177 | **22,16** | 219,4 s |
docs/plan-deepseek41-complet.md:70:| tables d'engram | 10 000 entrées en **219–524 ms**, 2,6 Mo touchés par table, **120 Mo de RSS** pour 365,7 Go |
REPRISE.md:189:| KV int4, échelles par bloc | +219 % (512) et +287 % (4 591) — était +384 % et +450 % |
REPRISE.md:194:| KV 
… [254 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"0,8 %\\|+0,8\\|0.8 %\" reports/rapport-placement-bits-kv.md reports/rapport-attribution-kv.md REPRISE.md | head -20 && echo \"=== E2/E3 in contexte-long ===\" && sed -n '95,115p' docs/contexte-long.md", "description": "Che … [53 caractères tronqués]`

  ```
reports/rapport-placement-bits-kv.md:5:donnent 39 % de la taille f32 pour **+0,018 %**.
reports/rapport-placement-bits-kv.md:21:| **f16** | **int8** | **3,125** | **39 %** | **14,2365** | **+0,018 %** |
reports/rapport-placement-bits-kv.md:33:39 %  clés f16 · valeurs int8 .. +0,018 %   ← le meilleur point
reports/rapport-placement-bits-kv.md:59:   (39 % du f32) pour **+0,018 %** — contre 5,125 octets (64 %) pour les clés f32
reports/rapport-placement-bits-kv.md:65:   taille f32** pour +0,018 %, là où l'int8 complet (28 %) coûte +3,04 %.
reports/rapport-placement-bits-kv.md:67:5. **La perspective llama.cpp** : son cache q8_0 coûte +0,8 % à la même longueur.
reports/rapport-placement-bits-kv.md:77:8 192 jetons : **+0,018 %** pour 3,125 octets par élément (**39 %** du f32), et à
reports/rapport-placement-bits-kv.md:88:| clés f16 · valeurs int8 | **12,2188** | **+0,011 %** | 14,2365 | +0,018 % |
reports/rapport-placement-bits-kv.md:100:+0,018 % contre +0,023 % à 8 192) — pour **moitié moins d'octets**. On ne prétend
reports/rapport-placement-bits-kv.md:136:| contexte court ou moyen, CPU | **clés f16 + valeurs int8** (39 % du f32, +0,018 %) | le meilleur compromis taille/qualité, et le 
… [3843 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading contexte-long §4.bis to resolve the int4 219 % vs 384 % question

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '114,160p' docs/contexte-long.md", "description": "Read contexte-long KV table"}`

  ```
## 4.bis KV quantifié : mesuré, et le 4 bits est cher

Cache KV en 8 puis 4 bits, échelle par vecteur (tête, position), nibbles
empaquetés en 4 bits — `DRAVE_KV_BITS=8` ou `4`, `[config] cache KV` dit ce qui est
alloué. Banc d'essai : Qwen2.5-0.5B Q8_0, 511 jetons, contexte 512, comparé à
llama.cpp sur le même texte.

| KV | nous (512 jetons) | llama.cpp (512) | nous (~4 600 jetons) | llama.cpp (8 192) |
|---|---|---|---|---|
| f32 / f16 | 13,14 | 14,24 | 12,91 | 16,59 |
| **int8** | **14,07** (+7,1 %) | 14,68 (+3,1 %) | **13,58** (+5,2 %) | 16,73 (+0,8 %) |
| **int4** | **63,61** (+384 %) | 72,80 (+411 %) | **71,05** (+450 %) | 98,53 (+494 %) |

Trois choses :

1. **L'int8 coûte quelques pour cent, à contexte court comme à 4 600 jetons** :
   le coût ne grandit pas avec la longueur, donc le KV int8 est un bon défaut
   pour le contexte long (et c'est lui qui fait tenir 128 k en mémoire).
2. **Le 4 bits détruit la perplexité d'un facteur 5**, chez les deux moteurs. Il
   reste implémenté — c'est lui qui fait tenir 1 M en RAM (9,7 Go) et en VRAM —
   mais il ne doit pas être le défaut, et il se valide modèle par modèle.
3. **Notre int8 était plus cher que celui de llama.cpp** (+5,2 
… [1248 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '180,200p' REPRISE.md", "description": "Read REPRISE KV rows"}`

  ```
| noyau GPU Q4_K warp (Qwen 1.5B, 7,7 Mo) | 0,5 ms contre 1,2 ms CPU (×2,2), écart 4e-7 |
| noyau GPU Q6_K warp (tête liée Qwen 1.5B, 191,4 Mo) | **3,6 ms** contre 8,3 ms CPU 16 fils (23,2 → 53,6 Go/s), écart 3,3e-7 |
| noyau GPU Q6_K warp (ffn_down Qwen 1.5B, 11,3 Mo) | **0,3 ms** contre 1,5 ms CPU (×5), écart 7,1e-7 |
| tête Q6_K déportée (Qwen 1.5B Q4_K_M, ctx 256, 510 jetons) | 7,58 → **3,60 ms/jeton** ; bout en bout 44,4 → 41,4 s (−7 %) ; lot 512 : 36,0 → 34,0 s ; **perplexité identique** (13,6877 / 13,6864) |
| préremplissage par lots (Qwen, ctx 512) | lot 1 = **17,1 s** · lot 512 = **13,6 s** → **−20 %** (perplexité 13,1368 → 13,1359) |
| préremplissage par lots (gpt-oss, ctx 256, MoE groupé) | ≈ 50 s à lot 1 · **34,4 s** à lot 256 (13,7205 dans tous les cas) |
| tête de sortie en lot | **aucun gain** (5,47 contre 5,63 ms/jeton) : noyau lié au calcul — il faut AVX2 ou le GPU |
| attente du pool après panique d'un worker | **échoue en clair** au lieu de boucler (constaté : 10 min d'attente active) |
| KV int8, échelles par bloc | +1,5 % (512 jetons) et +3,4 % (4 591) — était +7,1 % et +5,2 % |
| KV int4, échelles par bloc | +219 % (512) et +287 % (4 591) — était +384 % et +45
… [1638 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking whether attn_sinks is actually wired into attention in model.rs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"sink\" drave-core/src/*.rs | head -40", "description": "Grep sinks usage across drave-core"}`

  ```
drave-core/src/gpu.rs:124:    pub sinks_dev: u64,
drave-core/src/gpu.rs:128:    pub sinks_cap: usize,
drave-core/src/gpu.rs:432:                            octets: 0, q_dev: 0, part_dev: 0, out_dev: 0, sinks_dev: 0,
drave-core/src/gpu.rs:433:                            q_cap: 0, part_cap: 0, out_cap: 0, sinks_cap: 0 };
drave-core/src/gpu.rs:965:    /// `sinks` est indexé par ligne, comme le moteur. `bits` doit valoir 8
drave-core/src/gpu.rs:969:                           hd: usize, rep: usize, sinks: Option<&[f32]>,
drave-core/src/gpu.rs:998:        let mut p_sinks: u64 = 0;
drave-core/src/gpu.rs:999:        if let Some(si) = sinks {
drave-core/src/gpu.rs:1003:                if m.sinks_cap < besoin {
drave-core/src/gpu.rs:1004:                    if m.sinks_dev != 0 { cuMemFree_v2(m.sinks_dev); }
drave-core/src/gpu.rs:1005:                    m.sinks_dev = 0;
drave-core/src/gpu.rs:1006:                    m.sinks_cap = 0;
drave-core/src/gpu.rs:1007:                    if cuMemAlloc_v2(&mut m.sinks_dev, besoin) != 0 { return false; }
drave-core/src/gpu.rs:1008:                    m.sinks_cap = besoin;
drave-core/src/gpu.rs:1010:                if cuMemcpyHtoD_v2(m.sinks_dev, si.as_
… [2336 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"manques_architecture\" -A 30 drave-core/src/model.rs | sed -n '1,60p'", "description": "Read manques_architecture context"}`

  ```
87:pub fn manques_architecture(g: &Gguf, cfg: &Cfg, ctx: usize, clusters: bool) -> Vec<&'static str> {
88-    // Le test porte sur TOUTES les couches, pas sur la couche 0 : GLM-5.3 a
89-    // trois couches denses puis des couches MLA, et regarder la première
90-    // laissait passer le modèle jusqu'au panic « attn_q absent » de la couche 3.
91-    let quelque_part = |suffixe: &str| g.tensors.iter().any(|t| t.name.ends_with(suffixe));
92-    let a = |n: &str| g.tensor(n).is_some();
93-    let mut manques: Vec<&str> = Vec::new();
94-    if quelque_part("hc_attn_fn.weight") || quelque_part("hc_ffn_fn.weight") {
95-        manques.push("hyper-connexions (hc_attn_fn, hc_ffn_fn, hc_mult)");
96-    }
97-    // Attention par index (DSA) : l'indexeur choisit les clés gardées. Il ne
98-    // sert QUE si la séquence dépasse `index_topk` — en deçà, llama.cpp garde
99-    // toutes les clés et l'indexeur n'est pas appelé. On refuse donc seulement
100-    // les contextes où il changerait le résultat.
101-    if quelque_part("indexer.") {
102-        let topk = g.cfg("index_topk").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
103-        if topk == 0 || ctx > topk {
104-            manques.
… [2728 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Grep found no "sink" in model.rs — verifying how sinks enter the attention math

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"attn_sinks\\|puits\" drave-core/src/*.rs | head -40", "description": "Grep attn_sinks and puits in sources"}`

  ```
drave-core/src/gpu.rs:962:    /// aucun aller-retour par l'hôte. Les puits comptent dans le dénominateur,
drave-core/src/gpu.rs:1250:                // puits était silencieusement ignoré. Relevé par un relecteur.
drave-core/src/main.rs:532:    attn_sinks: usize, attn_topk: usize, qk_topk: usize,
drave-core/src/main.rs:649:            "--attn-sinks" => { o.attn_sinks = suivant(i).parse().unwrap(); 2 }
drave-core/src/main.rs:752:        keep, attn_window, swa_pattern, sans_fenetre, attn_sinks, attn_topk, qk_topk,
drave-core/src/main.rs:800:    if attn_sinks > 0 { mdl.attn_sinks = attn_sinks; }
drave-core/src/main.rs:3102:    // noyau 3. Les puits comptent dans le dénominateur, jamais au numérateur —
drave-core/src/main.rs:3103:    // c'est le piège que le plan signale, et il est testé ici avec des puits
drave-core/src/main.rs:3105:    // Le moteur passe `None` pour les modèles SANS puits (Qwen, la plupart) : ce
drave-core/src/main.rs:3107:    let avec_puits = std::env::var("DRAVE_BANC_SANS_PUITS").is_err();
drave-core/src/main.rs:3109:    let sinks_opt: Option<&[f32]> = if avec_puits { Some(&sinks) } else { None };
drave-core/src/main.rs:3190:                    // La référence doit 
… [2916 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspecting the attention paths to see if every path honours lay.sinks

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '3450,3540p' drave-core/src/model.rs", "description": "Read attention softmax with sinks"}`

  ```
let kvc = &self.kv[l];
                let n = pos + 1;
                let lo = if fen > 0 && n > fen { n - fen } else { 0 };
                // Chemin GROUPÉ dès que possible : `rep` têtes de requête
                // partagent une tête KV, donc la clé (et la valeur) ne doivent
                // être déquantifiées qu'UNE fois par groupe. Le chemin par tête
                // les relisait `rep` fois — mesuré ×2,2 sur ce poste.
                let groupe = fen == 0 && self.attn_topk == 0 && rep > 1;
                // ---- KV déporté : la même attention, calculée en VRAM (E4) ----
                let mut fait_en_gpu = false;
                if groupe && self.kv_gpu.is_some() && nkv * rep == nh && n > 1 {
                    let nsplit = (n / 256).clamp(1, 128);
                    let besoin = nsplit * nkv * rep * (hd + 2);
                    if self.attn_gpu_part.len() < besoin { self.attn_gpu_part.resize(besoin, 0.0); }
                    let puits: Option<Vec<f32>> = lay.sinks.as_ref()
                        .map(|s| (0..nh).map(|h| s[h]).collect());
                    let part = &mut self.attn_gpu_part;
                    // Copie des requêtes du jeton : `qi` emprunte `q
… [4105 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la /home/stephane/Data13TB/stephane/modeles/gguf/ 2>/dev/null | head -60; echo \"=== NVME ===\"; ls -la /home/stephane/FastNVMe/modeles-lourds/ 2>/dev/null | head -60", "description": "List available GGUF model files"}`

  ```
total 150826352
drwxr-xr-x. 1 stephane stephane        1206  1 oct 09:46 .
drwxr-xr-x. 1 stephane stephane          26  1 oct 08:59 ..
-rw-r--r--. 1 stephane stephane  1157671200 12 sep 19:02 bge-m3-FP16.gguf
-rw-r--r--. 1 stephane stephane 13341237600 13 aoû 07:27 codestral-22b-v0.1-q4_k_m.gguf
-rw-r--r--. 1 stephane stephane  8988109984 13 aoû 07:26 deepseek-r1-distill-qwen-14b-q4_k_m.gguf
-rw-r--r--. 1 stephane stephane  1117320800 24 sep 10:44 deepseek-r1-distill-qwen-1.5b-q4_k_m.gguf
drwxr-xr-x. 1 stephane stephane         118  1 oct 10:26 DeepSeek-V4.1-Flash-Q2
drwxr-xr-x. 1 stephane stephane         492  1 oct 10:48 DeepSeek-V4-Flash-UD-IQ1_M
-rw-r--r--. 1 stephane stephane   849103296 24 sep 13:15 eagle3-gpt-oss-120b-Q8_0.gguf
drwxr-xr-x. 1 stephane stephane         252  1 oct 12:42 GLM-5.3-Flash-UD-IQ1_S
drwxr-xr-x. 1 stephane stephane         432  1 oct 12:10 GLM-5.3-UD-IQ1_S
-rw-r--r--. 1 stephane stephane 63387346208 24 sep 13:14 gpt-oss-120b-MXFP4.gguf
drwxr-xr-x. 1 stephane stephane         688  1 oct 11:35 Kimi-K2.7-Code-UD-IQ1_M
drwxr-xr-x. 1 stephane stephane         134  1 oct 12:14 MiniMax-H3
-rw-r--r--. 1 stephane stephane  1354162912 10 sep 14:31 mmproj-Qwen2.5
… [1059 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading tools/portes.sh fully to audit section 7 and the helper functions

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/portes.sh"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/portes.sh</path>
<type>file</type>
<content>
1: #!/bin/bash
2: # Les portes du dépôt, en une commande.
3: #
4: # Un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien :
5: # chaque porte est comparée à la valeur ATTENDUE, et le script sort en erreur si
6: # l'une diverge. Les valeurs sont celles publiées dans les rapports.
7: #
8: #   tools/portes.sh            toutes les portes
9: #   tools/portes.sh rapide     sans gpt-oss (le seul qui prenne ~20 min)
10: 
11: set -u
12: cd "$(dirname "$0")/.."
13: D=./drave-core/target/release/drave
14: RAPIDE=${1:-}
15: ECHEC=0
16: 
17: [ -x "$D" ] || { echo "compiler d'abord : (cd drave-core && cargo build --release)"; exit 2; }
18: 
19: compare() {  # nom, attendu, obtenu
20:     if [ "$2" = "$3" ]; then
21:         printf "  %-42s %s  ✅\n" "$1" "$3"
22:     else
23:         printf "  %-42s %s  ❌ (attendu %s)\n" "$1" "${3:-—}" "$2"
24:         ECHEC=1
25:     fi
26: }
27: 
28: # Attention : le moteur affiche AUSSI une perplexité cumulée par fenêtre, avant
29: # le total. Prendre la première occurrence du motif donnait 17,431 (fenêtre 1) au
30: # lieu de 19,3885 (t
… [5309 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying --config output text, valeur() format and tokenize flags

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/github/Qtrinet 2>/dev/null || cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; grep -rn \"calculable\" drave-core/src/*.rs | head -20; echo \"=== perplexite print ===\"; grep -rn \"perplexité\" drave-core/src/main.rs | head -20", "description": "Gr … [37 caractères tronqués]`

  ```
drave-core/src/main.rs:1646:/// à savoir si l'architecture est calculable — deux choses qui n'étaient
drave-core/src/main.rs:1687:        println!("calculable    : oui (passe avant implémentée)");
drave-core/src/main.rs:1689:        println!("calculable    : NON — il manque : {}", manques.join(", "));
drave-core/src/model.rs:127:    // Les ranger dans le même manque faisait répondre « calculable : NON » à un
=== perplexite print ===
61:        eprintln!("                                     sortie — refusé en perplexité.");
397:/// (`--keep` en perplexité, `--ffn-gain` en inférence, les top-k dans les modes
466:/// Les modes (inférence, perplexité, plan, tokenize) la remplissent par la MÊME
526:    /// diffèrent selon le mode (256 jetons et 16 bits en perplexité, 512 et
553:    /// ceux-là. **Génération seulement** — une perplexité calculée sur un
802:    // perplexité — une trace est un enregistrement du flux, elle n'a rien de
803:    // spécifique à la mesure de perplexité.
822:    // `--ffn-gain` était appliqué en perplexité et JAMAIS déstructuré ici : la
828:    // Appliqués en perplexité depuis toujours, oubliés ici : la déstructuration
1885:/// de perplexité. Plan : `docs/pla
… [903 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '\"--tokenize\"\\|\"--fichier\"\\|\"--sortie\"\\|tokenize' drave-core/src/main.rs | head -20; echo \"=== data ===\"; ls -la data/ | head; echo \"=== models ===\"; ls -la models/ 2>/dev/null | head -20", "description": "Check … [39 caractères tronqués]`

  ```
36:mod tokenizer;
66:    // Une seule analyse, puis un aiguillage : `--plan`, `--tokenize`,
98:        (opt.plan, "--plan"), (opt.tokenize, "--tokenize"),
118:    if opt.tokenize { run_tokenize(opt); return; }
466:/// Les modes (inférence, perplexité, plan, tokenize) la remplissent par la MÊME
475:    infer: bool, ppl: bool, plan: bool, tokenize: bool, gpu_banc: bool,
569:    // --- tokenize / plan
604:            "--tokenize" => { o.tokenize = true; 1 }
625:            "--fichier" => { o.fichier = Some(suivant(i).clone()); 2 }
626:            "--sortie" => { o.sortie = Some(suivant(i).clone()); 2 }
846:        mdl.stop_id = build_tokenizer(&mdl.g).special_id("<|im_end|>");
854:        let tk = build_tokenizer(&mdl.g);
938:        let tks = build_tokenizer(&mdl.g);
1019:        let tk = build_tokenizer(&mdl.g);
1035:        let tk = build_tokenizer(&mdl.g);
1106:fn build_tokenizer(g: &Gguf) -> tokenizer::Tokenizer {
1107:    let pre = g.meta.get("tokenizer.ggml.pre").and_then(|m| m.as_str()).unwrap_or("").to_string();
1108:    tokenizer::Tokenizer::new(
1109:        meta_strings(g, "tokenizer.ggml.tokens"),
1110:        meta_strings(g, "tokenizer.ggml.merges"),
=== data ===
total 7
… [617 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Locating the exact perplexity output line that valeur() greps

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '\"===' drave-core/src/*.rs | head -20; echo \"=== fenetre ===\"; grep -n \"fenêtre\\|fenetre\" drave-core/src/main.rs | grep -i \"ppl\\|perplex\\|println\" | head -20", "description": "Find === perplexite print statements"}`

  ```
drave-core/src/main.rs:158:    println!("=== 1. Taille exacte des encodages (mesurée sur les niveaux réels) ===");
=== fenetre ===
413:    println!("[options] fenêtre {} · motif {} · seuil push {} · lot {} · ffn_gain {:?} · hebb {}",
4040:        println!("  couches à fenêtre glissante : {n_fenetrees}/{n_layer} \
4096:/// Construit les fenêtres de perplexité en **format harmony** (gpt-oss).
4181:                eprintln!("[harmony] fenêtre {} : {} jetons, {} notés · |{}|",
4226:            eprintln!("[harmony] fenêtre {} : {} jetons, {} notés · |{}|",
4286:        println!("{idfile} : {} tokens, fenêtres de {ctx}", ids.len());
4316:        println!("{f} : {} jetons (tokenizer du modèle), fenêtres de {ctx}", ids.len());
4348:        println!("fenêtre : {} · motif {} (imposé par la ligne de commande)",
4418:            println!("harmony ({mode}{}) : {} fenêtres, {notes} jetons de contenu notés \
4510:        // La perplexité PROPRE à la fenêtre dit où le modèle décroche : une
4520:                     format!("  [fenêtre {} : {} notés, PPL {:.3}]",
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"perplexité\" drave-core/src/model.rs | head -20; echo \"=== ppl print in main ===\"; grep -n \"ppl_total\\|ppl_cum\\|println!(\\\"\" drave-core/src/main.rs | grep -i \"ppl\\|perpl\" | head -20", "description": "Find ppl to … [11 caractères tronqués]`

  ```
288:/// rien de visible : la perplexité monte de quelques pour cent, et les experts
397:    /// défaut donne une perplexité de 1 396 au lieu de la bonne.
405:    /// rien de visible : la perplexité monte de quelques pour cent et les
614:    // d'autre : la perplexité part en vrille sans qu'aucun tenseur ne manque.
1540:    /// de la table d'embedding ; lire la mauvaise donne une perplexité de
1577:    /// **Ne s'applique pas à la perplexité** : le softmax normalise sur tout le
1579:    /// dénominateur — mesuré, la perplexité *baisse* artificiellement (24,31
1596:    /// rejouait la mauvaise — mesuré : perplexité 356 694 au lieu de 17,43.
1625:    /// perplexité répartie **798,3** au lieu de **18,2**. La norme finale est
1635:    /// Le préremplissage par lots n'était branché que sur la perplexité : une
1774:    /// ce qui explique l'écart mesuré avec llama.cpp (+5,2 % de perplexité
1885:    /// perplexité contre notre +3,0 % (à 8 192 jetons).
1923:        // perplexité contre +0,8 % pour son cache q8_0).
2093:// modèle (densité 5,1 % ⇒ perplexité ×107 ; 30,3 % ⇒ +48 % ; 61,5 % ⇒ +15 %).
2145:                // REFUTÉE : 185 -> 1 095 de perplexité. La tête est tournée en
2181:     
… [1622 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Listing all GGUF files and scanning their headers for attn_sinks / attn_derope

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/modeles/gguf/*/*.gguf 2>/dev/null | head -60; echo \"=== count ===\"; ls /home/stephane/Data13TB/stephane/modeles/gguf/*/*.gguf 2>/dev/null | wc -l", "description": "List sharded GGUF files"}`

  ```
-rw-r--r--. 1 stephane stephane 365713686528  1 oct 10:26 /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4.1-Flash-Q2/DeepSeek-V4.1-Flash-Q2.gguf
-rw-r--r--. 1 stephane stephane      5256864  1 oct 10:48 /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf
-rw-r--r--. 1 stephane stephane  49971881124  1 oct 09:47 /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00002-of-00003.gguf
-rw-r--r--. 1 stephane stephane  36924175168  1 oct 07:34 /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00003-of-00003.gguf
-rw-r--r--. 1 stephane stephane      9429859  1 oct 12:28 /home/stephane/Data13TB/stephane/modeles/gguf/GLM-5.3-Flash-UD-IQ1_S/GLM-5.3-Flash-UD-IQ1_S-00001-of-00003.gguf
-rw-r--r--. 1 stephane stephane  49621122496  1 oct 12:35 /home/stephane/Data13TB/stephane/modeles/gguf/GLM-5.3-Flash-UD-IQ1_S/GLM-5.3-Flash-UD-IQ1_S-00002-of-00003.gguf
-rw-r--r--. 1 stephane stephane  43456692608  1 oct 12:42 /home/stephane/Data13TB/stephane/modeles/gguf/GLM-5.3-Flash-UD-IQ1_S/GLM-5.3-Flash-UD-IQ1_S-00003-of-00003.gguf
-
… [2998 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"attn_derope\\|de_rope\\|derope\" drave-core/src/*.rs tools/*.py docs/*.md 2>/dev/null | head -20", "description": "Grep attn_derope references"}`

  ```
drave-core/src/model.rs:119:    // `attn_derope` renvoie la sortie d'attention dans le repère non tourné et
drave-core/src/model.rs:129:    if quelque_part("attn_derope") {
docs/plan-deepseek41-complet.md:138:- Dé-rotation (`attn_derope`), puits par tête (`attn_sinks`), sortie groupée
  ```

### 🤖 Assistant

⏵ Scanning every GGUF header for attn_sinks and attn_derope

- **bash** `{"command": "cd /tmp && for f in /home/stephane/Data13TB/stephane/modeles/gguf/*.gguf /home/stephane/Data13TB/stephane/modeles/gguf/*/*.gguf /home/stephane/FastNVMe/modeles-lourds/*.gguf; do\n  [ -f \"$f\" ] || continue\n  s=$(head -c 33554432 \"$f\" | grep -c \"attn_sinks\" 2>/dev/null)\n  d=$(head … [234 caractères tronqués]`

  ```
sinks=0 derope=0  Data13TB/stephane/modeles/gguf/bge-m3-FP16.gguf
sinks=0 derope=0  Data13TB/stephane/modeles/gguf/codestral-22b-v0.1-q4_k_m.gguf
sinks=0 derope=0  Data13TB/stephane/modeles/gguf/deepseek-r1-distill-qwen-14b-q4_k_m.gguf
sinks=0 derope=0  Data13TB/stephane/modeles/gguf/deepseek-r1-distill-qwen-1.5b-q4_k_m.gguf
sinks=0 derope=0  Data13TB/stephane/modeles/gguf/eagle3-gpt-oss-120b-Q8_0.gguf
sinks=36 derope=0  Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf
sinks=0 derope=0  Data13TB/stephane/modeles/gguf/mmproj-Qwen2.5-VL-7B-Instruct-f16.gguf
sinks=0 derope=0  Data13TB/stephane/modeles/gguf/Muse-Glimmer-30B-AD-Q4_K_M.gguf
sinks=0 derope=0  Data13TB/stephane/modeles/gguf/qwen2.5-0.5b-instruct-q4_k_m.gguf
sinks=0 derope=0  Data13TB/stephane/modeles/gguf/qwen2.5-1.5b-instruct-q4_k_m.gguf
sinks=0 derope=0  Data13TB/stephane/modeles/gguf/qwen2.5-coder-0.5b-instruct-q4_k_m.gguf
sinks=0 derope=0  Data13TB/stephane/modeles/gguf/qwen2.5-coder-32b-instruct-q4_k_m.gguf
sinks=0 derope=0  Data13TB/stephane/modeles/gguf/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf
sinks=0 derope=0  Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf
sinks=40 derope=0  Data13TB/stephan
… [2845 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Asking the engine (--config, header-only) for verdicts on sinks-bearing models

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la drave-core/target/release/drave 2>/dev/null && timeout 60 ./drave-core/target/release/drave /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf --config 2>&1 | head -40", "description": "Run --config on gpt-o … [4 caractères tronqués]`

  ```
-rwxr-xr-x. 2 stephane stephane 2118816  2 oct 10:02 drave-core/target/release/drave
modèle        : /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf
architecture  : gpt-oss
couches       : 36 · cachés 2880
experts       : 128 par couche, 4 par jeton · FFN expert 2880
routage       : top-k brut + softmax (source : défaut du moteur) · renormalisation non · échelle aucune
calculable    : oui (passe avant implémentée)
  ```

### 🤖 Assistant

⏵ Confirming which mode actually prints the “puits appris sur 36/36” line

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2395,2425p' drave-core/src/model.rs && echo \"=== who calls ===\" && grep -n \"fn charger\\|pub fn new\\|fn ouvre\\|sinks_vus\" drave-core/src/model.rs | head -20", "description": "Read context of puits appris print"}`

  ```
// sur un modèle de 60 Go.
        let ligne_echelle = if cfg.n_expert > 0 && cfg.expert_scale != 0.0 && cfg.expert_scale != 1.0 {
            format!("échelle {:.2} ", cfg.expert_scale) } else { String::new() };
        println!("[config] {} couches, hidden {} · {}{}{}{}{}{}{}{}",
                 cfg.n_layer, cfg.hidden,
                 if cfg.yarn.is_some() { "yarn " } else { "" },
                 if cfg.ffn_act_oss { "activation-oss " } else { "" },
                 if cfg.n_expert > 0 { cfg.gating.nom() } else { "" },
                 ligne_echelle,
                 if cfg.hash_layers > 0 { "routage-table " } else { "" },
                 if cfg.n_expert > 0 { "moe " } else { "" },
                 if cfg.n_expert > 0 { "" } else { "" },
                 if cfg.head_dim > 0 { "" } else { "" });
        if cfg.n_expert > 0 {
            println!("[config] mélanges d'experts chargés : {moe_vus}/{n_layer} couches · \
mapping {}",
                     match map {
                         None => "absent (experts en clair dans le fichier)".to_string(),
                         Some(m) => format!("actif : {} clusters × {} experts",
                                            m.n_c
… [1332 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"affiche_config\\|fn affiche\\|--config\" drave-core/src/main.rs | head -20", "description": "Find --config handler in main.rs"}`

  ```
96:        (opt.gpu_banc, "--gpu-banc"), (opt.materiel, "--materiel"), (opt.config, "--config"),
684:            "--config" => { o.config = true; 1 }
1642:/// **Ce que le moteur comprend d'un modèle** (`--config`), sans le charger.
  ```

### 🤖 Assistant

⏵ Identifying the enclosing loader function to name the correct diagnostic path

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk 'NR>=2200 && NR<=2420 && /^    (pub )?fn |^    impl |^impl /{print NR\": \"$0}' drave-core/src/model.rs | tail -8; echo \"=== 2350-2390 ===\"; grep -n \"fn charger\\|fn ouvrir\\|fn depuis_gguf\\|fn nouveau\\|impl Modele\\|impl Mo … [99 caractères tronqués]`

  ```
=== 2350-2390 ===
468:fn charger_moe(g: &Gguf, l: usize, n_expert: usize, map: Option<&'static crate::clusters::Mapping>)
1050:    pub fn nouveau(budget: usize) -> Self {
1191:    pub fn nouveau(chemin: &str, couches: Vec<usize>, hidden: usize, n_layer: usize)
2102:impl Model {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1642,1700p' drave-core/src/main.rs", "description": "Read --config implementation"}`

  ```
/// **Ce que le moteur comprend d'un modèle** (`--config`), sans le charger.
///
/// Le mode ne lit que l'en-tête du GGUF : quelques dizaines de millisecondes,
/// même sur 341 Go. Il sert à voir la décision de ROUTAGE et sa provenance, et
/// à savoir si l'architecture est calculable — deux choses qui n'étaient
/// visibles qu'après un chargement complet, c'est-à-dire jamais pour les gros
/// modèles.
///
/// Il est né d'un constat : trois des cinq plus gros modèles de cette machine
/// n'avaient jamais été exécutés, et rien ne le disait avant la panne.
fn run_config() {
    let g = Gguf::open_meta_auto(&modele_chemin()).expect("ouverture du GGUF (en-tête)");
    let arch = g.meta.get("general.architecture").and_then(|m| m.as_str()).unwrap_or("?");
    println!("modèle        : {}", modele_chemin());
    println!("architecture  : {arch}");
    let n_layer = model::dim_gguf(&g, &["block_count", "num_hidden_layers"], "num_hidden_layers")
                      .unwrap_or(0);
    let hidden = model::dim_gguf(&g, &["embedding_length", "hidden_size"], "hidden_size")
                     .unwrap_or(0);
    println!("couches       : {n_layer} · cachés {hidden}");
    let r = model::routag
… [1930 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking verdict changes on the sinks-bearing big models

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && D=./drave-core/target/release/drave; M=/home/stephane/Data13TB/stephane/modeles/gguf; for f in \"$M/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf\" \"$M/DeepSeek-V4-Flash-UD-IQ1_M\" \"$M/DeepSeek-V4.1-Flas … [161 caractères tronqués]`

  ```
### /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf
routage       : racine de softplus (source : expert_gating_func) · renormalisation oui · échelle 1.500
routage table : 3/43 premières couches par `ffn_gate_tid2eid`
[mla] attention MLA à rang faible : cache LATENT (c_kv + k_rope), pas de fenêtre glissante ni de YaRN sur ce chemin. Validée contre llama.cpp sur GLM-5.3 : corrélation des logits 0,999024, top-1 3/3 (voir reports/rapport-mla-experts.md).
calculable    : NON — il manque : hyper-connexions (hc_attn_fn, hc_ffn_fn, hc_mult), projection de sortie à rang faible groupée (attn_output_a/attn_output_b, o_groups)
### /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M
thread 'main' (354480) panicked at src/main.rs:1653:52:
ouverture du GGUF (en-tête): Custom { kind: NotFound, error: "/home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M : commun.gguf absent" }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
timeout: the monitored command dumped core
### /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4.1-Flash-Q2/DeepSeek-V4.1-Flash
… [641 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && D=./drave-core/target/release/drave; M=/home/stephane/Data13TB/stephane/modeles/gguf; for f in \"$M/GLM-5.3-UD-IQ1_S/GLM-5.3-UD-IQ1_S-00001-of-00006.gguf\" \"$M/Kimi-K2.7-Code-UD-IQ1_M/Kimi-K2.7-Code-UD-IQ1_M-00001-of-00008.gguf\" \" … [223 caractères tronqués]`

  ```
### GLM-5.3-UD-IQ1_S-00001-of-00006.gguf
routage       : sigmoïde (source : expert_gating_func) · renormalisation oui · échelle 2.500
[mla] attention MLA à rang faible : cache LATENT (c_kv + k_rope), pas de fenêtre glissante ni de YaRN sur ce chemin. Validée contre llama.cpp sur GLM-5.3 : corrélation des logits 0,999024, top-1 3/3 (voir reports/rapport-mla-experts.md).
calculable    : oui (passe avant implémentée)
### Kimi-K2.7-Code-UD-IQ1_M-00001-of-00008.gguf
routage       : sigmoïde (source : expert_gating_func) · renormalisation oui · échelle 2.827
[mla] attention MLA à rang faible : cache LATENT (c_kv + k_rope), pas de fenêtre glissante ni de YaRN sur ce chemin. Validée contre llama.cpp sur GLM-5.3 : corrélation des logits 0,999024, top-1 3/3 (voir reports/rapport-mla-experts.md).
calculable    : oui (passe avant implémentée)
### Qwen3-235B-A22B-Instruct-2507-Q2_K-00001-of-00002.gguf
experts       : 128 par couche, 8 par jeton · FFN expert 1536
routage       : softmax (source : défaut du moteur) · renormalisation oui · échelle aucune
calculable    : oui (passe avant implémentée)
  ```

### 🤖 Assistant

⏵ Checking whether the release binary predates the model.rs edit

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && stat -c '%y %n' drave-core/src/model.rs drave-core/src/main.rs drave-core/target/release/drave && echo \"=== git diff mtime of uncommitted ===\" && git diff --stat | tail -3", "description": "Compare source and binary mtimes"}`

  ```
2026-10-02 10:09:14.914461796 -0400 drave-core/src/model.rs
2026-10-02 08:49:40.877924736 -0400 drave-core/src/main.rs
2026-10-02 10:02:55.042210962 -0400 drave-core/target/release/drave
=== git diff mtime of uncommitted ===
 tools/analyse_flux.py           |  2 +-
 tools/portes.sh                 | 29 +++++++++++++++--
 23 files changed, 362 insertions(+), 163 deletions(-)
  ```

### 🤖 Assistant

⏵ The tree changed under me — re-checking the diff and new files

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain && echo \"=== STAT ===\" && git diff --stat && echo \"=== NEW MODEL.RS DIFF ===\" && git diff -- drave-core/src/model.rs", "description": "Re-check git status and model.rs diff"}`

  ```
M README.md
 M REPRISE.md
 M docs/colab-reparti.md
 M docs/comparaison-spiking.md
 M docs/contexte-long.md
 M docs/convertisseur.md
 M docs/format-clusters.md
 M docs/format-flux.md
 M docs/plan-deepseek-v4-flash.md
 M docs/plan-deepseek41-complet.md
 M docs/plan-gpu-topk.md
 M docs/plan-mla-vision.md
 M docs/plan-mode4-lot-listes.md
 M docs/plan-modeles-lourds.md
 M docs/plan-prefill-reparti.md
 M docs/programme-recherche.md
 M docs/roadmap.md
 M docs/sprints.md
 M docs/vision.md
 M drave-core/src/model.rs
 M journal/README.md
 M tools/analyse_flux.py
 M tools/portes.sh
?? reports/rapport-coherence-vision.md
=== STAT ===
 README.md                       |  4 +++
 REPRISE.md                      | 23 +++++++++----
 docs/colab-reparti.md           |  7 +++-
 docs/comparaison-spiking.md     | 23 ++++++++++---
 docs/contexte-long.md           | 28 +++++++++-------
 docs/convertisseur.md           | 55 +++++++++++++++++++------------
 docs/format-clusters.md         |  5 +++
 docs/format-flux.md             | 13 +++++---
 docs/plan-deepseek-v4-flash.md  | 58 +++++++++++++++++++++------------
 docs/plan-deepseek41-complet.md | 15 +++++----
 docs/plan-gpu-topk.md           | 13 +++++---

… [4872 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Snapshotting the current revision and reviewing the newest hunks

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff > /tmp/full_now.diff && md5sum /tmp/full_now.diff && git rev-parse HEAD && date && echo \"=== README + analyse_flux ===\" && git diff -- README.md tools/analyse_flux.py", "description": "Snapshot diff and read README/analyse … [15 caractères tronqués]`

  ```
f8fe1dd324fa3b8819ff6eeada793ad1  /tmp/full_now.diff
5a6ac96324db4dacf0394773acf057237486c987
ven 02 oct 2026 10:10:39 EDT
=== README + analyse_flux ===
diff --git a/README.md b/README.md
index 4f5585b..ee2c1e0 100644
--- a/README.md
+++ b/README.md
@@ -365,6 +365,10 @@ tools/portes_formats.sh                   # 17 formats × 2 blocs, contre libggm
 tools/extraire_tables_ggml.sh verifier    # les tables embarquées = celles de ggml
 ```
 
+**18 formats lisibles, 17 vérifiés à la porte** : `Q5_1` est lu par la même
+branche que `Q5_0` (`drave-core/src/gguf.rs`) mais n'est pas dans la batterie
+comparée bloc par bloc.
+
 | modèle | format | perplexité | débit | mémoire |
 |---|---|---|---|---|
 | Qwen2.5-0.5B | Q4_0 | 21,01 | 39 tok/s | 0,41 Go |
diff --git a/tools/analyse_flux.py b/tools/analyse_flux.py
index 7447363..4f994ce 100755
--- a/tools/analyse_flux.py
+++ b/tools/analyse_flux.py
@@ -5,7 +5,7 @@ neurone par neurone », mais chiffré par couche et sans exécuter le moteur.
 Ce que l'outil répond, et pourquoi ces questions-là :
 
 * **quelle couche est creuse** ? C'est la décision push/pull du projet (le
-  croisement mesuré est à ~10 % de densité) — mais elle se prend PAR COUCHE,
… [265 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"seuil_push\" drave-core/src/model.rs drave-core/src/main.rs | head -20; echo \"=== rapport croisement ===\"; sed -n '1,60p' reports/rapport-croisement-push-pull.md", "description": "Verify seuil_push value and crossover rep … [5 caractères tronqués]`

  ```
drave-core/src/model.rs:948:        // (`seuil_push = 0.22`, `reports/rapport-croisement-push-pull.md`).
drave-core/src/model.rs:1529:    pub seuil_push: f32,
drave-core/src/model.rs:2629:            seuil_push: 0.22,
drave-core/src/model.rs:3390:                                     self.act_renorm, &mut scratch, self.seuil_push);
drave-core/src/model.rs:4175:                Self::matvec(pool, &lay.wq, &hn, &mut q, events, self.act_levels, self.act_thresh, tk(0), self.act_renorm, &mut scratch, self.seuil_push);
drave-core/src/model.rs:4176:                Self::matvec(pool, &lay.wk, &hn, &mut k, events, self.act_levels, self.act_thresh, tk(1), self.act_renorm, &mut scratch, self.seuil_push);
drave-core/src/model.rs:4177:                Self::matvec(pool, &lay.wv, &hn, &mut v, events, self.act_levels, self.act_thresh, tk(2), self.act_renorm, &mut scratch, self.seuil_push);
drave-core/src/model.rs:4539:            Self::matvec(pool, &lay.wo, &att[..n_att.min(att.len())], &mut o, events, self.act_levels, self.act_thresh, tk(3), self.act_renorm, &mut scratch, self.seuil_push);
drave-core/src/model.rs:4673:            Self::matvec(pool, &lay.wgate, &hn, &mut gate, events, self.act_level
… [3340 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying the Q5_1 claim and the 17/18 format count

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Q5_0\\|Q5_1\\|5_0\\|5_1\" drave-core/src/gguf.rs | head -20; echo \"=== portes_formats ===\"; grep -n \"Q5\\|formats\\|FORMATS\" tools/portes_formats.sh | head -30", "description": "Verify Q5_1 decode branch and format gate … [7 caractères tronqués]`

  ```
243:/// Bloc **Q5_0** (22 octets, 32 poids) et **Q5_1** (24 octets, 32 poids) :
244:/// échelle f16 (+ minimum f16 pour Q5_1), 4 octets de bits hauts, 16 octets de
245:/// quants 4 bits. Q5_0 est le type de `token_embd` et des `ffn_gate/up` de
248:pub const GGML_Q5_0: u32 = 6;
249:pub const GGML_Q5_1: u32 = 7;
762:            0 => "F32", 1 => "F16", 2 => "Q4_0", 3 => "Q4_1", 6 => "Q5_0", 7 => "Q5_1",
1029:    /// Déquantifie un bloc **Q5_0** (22 octets, 32 poids).
1036:    pub fn dequant_q5_0(bloc: &[u8]) -> Vec<f32> {
1037:        assert!(bloc.len() >= 22, "bloc Q5_0 trop court : {}", bloc.len());
1041:    /// Déquantifie un bloc **Q5_1** (24 octets, 32 poids) : identique à Q5_0
1043:    pub fn dequant_q5_1(bloc: &[u8]) -> Vec<f32> {
1044:        assert!(bloc.len() >= 24, "bloc Q5_1 trop court : {}", bloc.len());
1345:            GGML_Q5_0 | GGML_Q5_1 => {
1346:                let (taille, f): (usize, fn(&[u8]) -> Vec<f32>) = if t.ttype == GGML_Q5_0 {
1347:                    (22, Self::dequant_q5_0)
1349:                    (24, Self::dequant_q5_1)
1641:            GGML_Q5_0 | GGML_Q5_1 => {
1642:                let (taille, f): (usize, fn(&[u8]) -> Vec<f32>) = if t.ttype == GGML
… [697 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- docs/vision.md | head -120", "description": "Read current vision.md diff"}`

  ```
diff --git a/docs/vision.md b/docs/vision.md
index ca2c9a3..ae3ebe9 100644
--- a/docs/vision.md
+++ b/docs/vision.md
@@ -46,8 +46,11 @@ Le projet ne prétend pas que la sparsité gagne toujours. Le croisement a été
 **mesuré** : en dessous d'environ **22 % de densité**, le push (listes) bat le
 pull (matvec dense) ; au-dessus, le dense gagne
 (`reports/rapport-croisement-push-pull.md`). C'est pourquoi le moteur garde **les
-deux chemins** et choisit par la mesure, pas par principe — `--dense` existe, et
-les portes de non-régression tournent sur les deux.
+deux chemins** et choisit par la mesure, pas par principe — `--dense` existe, les
+portes de non-régression tournent en dense (`tools/portes.sh`), et le chemin par
+listes a les siennes : **le rejeu d'une trace redonne la même perplexité à
++0,074 % près** (19,4029 contre 19,3885) et l'écart d'activation entre le calcul
+et la trace est de **1,5e-5** (`REPRISE.md` §3, `DRAVE_FLUX_VERIF=1`).
 
 La densité observée, elle, dépend du modèle et de la couche : **17,9 %** sur
 Qwen2.5-0.5B à 512 jetons, mais les FFN denses de certaines familles ne sont pas
@@ -75,9 +78,12 @@ Ce que ces mesures ont appris, et qui n'aurait pas été visible a
… [6464 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying the new vision.md claims and the format-gate count

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"19,4029\\|19.4029\\|1,5e-5\\|1.5e-5\\|DRAVE_FLUX_VERIF\\|0,074\" REPRISE.md | head -20; echo \"=== 1608 / 0,25 Mbit ===\"; grep -rn \"1 608\\|1608\\|0,25 Mbit\\|0.25 Mbit\" REPRISE.md docs/roadmap.md docs/format-flux.md | h … [63 caractères tronqués]`

  ```
265:| `DRAVE_TRACE_BLOCS=1` | trace DRVF **v3** : valeurs i8, échelle f16 par bloc de 32 | 45 079 930 o contre 66 370 408 en v2 (−32 %), rejeu 19,4029 contre 19,3885 (+0,074 %) |
266:| `DRAVE_FLUX_VERIF=1` | vérifie l'écart entre l'activation calculée et celle que la trace impose | 1,5e-5 en v2 ; **muet dès que `--lot > 1`** (le rejeu par lots passe par `flux_lot`) |
358:| rejeu `--flux-forcer` | 19,3885 | 19,3885 | 19,4029 (+0,074 %) |
=== 1608 / 0,25 Mbit ===
REPRISE.md:315:| listes à échelle par bloc, seuil 0,01 | 1 608 | 2,7e-2 |
REPRISE.md:325:0,25 Mbit/s suffisent. Un aller-retour Colab de 60 ms donnerait ~8 jetons/s
docs/roadmap.md:56:| 3.2 | **Granularité** : par couche, par bloc de canaux, par expert | ✅ | listes i16, **échelles par bloc (i8)** et **indices par écarts** (1 608 octets par flux à 256 jetons) ; **mode 4 « lot en listes »** : 1,5 ko par jeton contre 3,5 en dense (÷2,3) pour 3,03e-2 d'écart ; reste le cas MoE |
docs/roadmap.md:57:| 3.3 | **Seuil de rentabilité** : à partir de quel débit réseau le découpage gagne | 🔬 | mesuré jusqu'à 20 ms de latence par message (`tools/proxy_latence.py`) : **attente ≈ calcul distant + 3,2 × latence**, soit 1,01× le calcul local
… [108 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk '/^  \"/{n++} END{print \"lignes formats:\", n}' tools/portes_formats.sh; grep -c '^  \"' tools/portes_formats.sh; echo \"=== liste ===\"; grep -oE '^  \"[A-Z0-9_]+' tools/portes_formats.sh | tr -d ' \"' | tr '\\n' ' '", "descrip … [44 caractères tronqués]`

  ```
lignes formats: 17
17
=== liste ===
F32 F16 Q4_0 Q5_0 Q8_0 Q2_K Q3_K Q4_K Q5_K Q6_K IQ2_XXS IQ3_XXS IQ1_S IQ4_XS IQ1_M BF16 MXFP4
  ```

### 🤖 Assistant

⏵ Counting truly readable formats in gguf.rs (Q4_1 vs Q5_1)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"GGML_Q4_1\\|GGML_Q4_0\\|GGML_Q5_0\\|GGML_Q5_1\\|GGML_IQ4_XS\\|GGML_IQ1_M\\|GGML_IQ1_S\\|GGML_BF16\\|GGML_MXFP4\\|GGML_IQ3_XXS\\|GGML_IQ2_XXS\" drave-core/src/gguf.rs | head -40", "description": "List supported GGML types in … [10 caractères tronqués]`

  ```
237:pub const GGML_Q4_0: u32 = 2;
238:pub const GGML_MXFP4: u32 = 39;
240:pub const GGML_BF16: u32 = 30;
248:pub const GGML_Q5_0: u32 = 6;
249:pub const GGML_Q5_1: u32 = 7;
255:pub const GGML_IQ2_XXS: u32 = 16;
258:pub const GGML_IQ3_XXS: u32 = 18;
260:pub const GGML_IQ1_S: u32 = 19;
263:pub const GGML_IQ4_XS: u32 = 23;
264:pub const GGML_IQ1_M: u32 = 29;
291:pub const GGML_Q4_1: u32 = 3;
981:            GGML_Q4_0 => {
1246:            GGML_BF16 => {
1272:            GGML_Q4_0 => {
1283:            GGML_Q2_K | GGML_Q3_K | GGML_Q5_K | GGML_IQ2_XXS | GGML_IQ3_XXS
1284:            | GGML_IQ1_S | GGML_IQ4_XS | GGML_IQ1_M => {
1289:                    GGML_IQ2_XXS => (66, crate::formats::dequant_iq2xxs),
1290:                    GGML_IQ3_XXS => (98, crate::formats::dequant_iq3xxs),
1291:                    GGML_IQ1_S => (50, crate::formats::dequant_iq1s),
1292:                    GGML_IQ4_XS => (136, crate::formats::dequant_iq4xs),
1345:            GGML_Q5_0 | GGML_Q5_1 => {
1346:                let (taille, f): (usize, fn(&[u8]) -> Vec<f32>) = if t.ttype == GGML_Q5_0 {
1356:            GGML_MXFP4 => {
1363:            GGML_Q4_1 => {
1385:            GGML_Q4_0 => true,
1433:        if t
… [879 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1330,1380p' drave-core/src/gguf.rs", "description": "Read dequant dispatch"}`

  ```
let is = l / 16;
                            let q1 = ((ql[l] & 0x0F) | ((qh[l] & 3) << 4)) as i16 - 32;
                            let q2 = ((ql[l + 32] & 0x0F) | (((qh[l] >> 2) & 3) << 4)) as i16 - 32;
                            let q3 = ((ql[l] >> 4) | (((qh[l] >> 4) & 3) << 4)) as i16 - 32;
                            let q4 = ((ql[l + 32] >> 4) | (((qh[l] >> 6) & 3) << 4)) as i16 - 32;
                            let s = |k: usize| d * (sc[is + k] as i8) as f32;
                            tmp[l] = s(0) * q1 as f32;
                            tmp[l + 32] = s(2) * q2 as f32;
                            tmp[l + 64] = s(4) * q3 as f32;
                            tmp[l + 96] = s(6) * q4 as f32;
                        }
                        out.extend_from_slice(&tmp);
                    }
                }
            }
            GGML_Q5_0 | GGML_Q5_1 => {
                let (taille, f): (usize, fn(&[u8]) -> Vec<f32>) = if t.ttype == GGML_Q5_0 {
                    (22, Self::dequant_q5_0)
                } else {
                    (24, Self::dequant_q5_1)
                };
                let nb = n_cols / 32;
                for b in 0..nb {
                    ou
… [1246 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading portes_formats.sh in full to confirm the covered type list

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/portes_formats.sh"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/portes_formats.sh</path>
<type>file</type>
<content>
1: #!/usr/bin/env bash
2: # Portes des FORMATS : chaque déquantificateur comparé à libggml, bloc par bloc.
3: #
4: #   tools/portes_formats.sh [type ...]
5: #
6: # Pourquoi : nos déquantificateurs sont écrits d'après le C de ggml, et les cinq
7: # premiers essais se sont tous trompés (IQ2_XXS : pas de 8 octets sur `qs` ;
8: # IQ1_M : échelles lues en premier alors qu'elles sont en DERNIER ; Q2_K : indice
9: # d'échelle ; Q5_K : bits hauts relus au lieu d'avancés ; Q6_K : quants
10: # entrelacés au lieu de groupés). Aucun n'a été trouvé par relecture : tous l'ont
11: # été par comparaison à la bibliothèque. Cette porte rend la comparaison
12: # reproductible, et refuse de « passer » si le témoin a disparu du disque — un
13: # test qui saute est un test qui ne dit rien.
14: #
15: # La référence est liée à libggml (voir tools/ref_ggml_bloc.c).
16: set -u
17: cd "$(dirname "$0")/.."
18: RACINE=$PWD
19: MODELES=${DRAVE_MODELES:-/home/stephane/Data13TB/stephane/modeles/gguf}
20: LLAMA=${DRAVE_LLAMA:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}
21: REF=${REF_GGML_BLOC:-/t
… [3983 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Counting the declared type names to see where “18” comes from

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '755,780p' drave-core/src/gguf.rs; echo \"=== row_f32 arms ===\"; awk 'NR>=960 && NR<=1400 && /^            GGML_|^            other =>/{print NR\": \"$0}' drave-core/src/gguf.rs", "description": "Read type name table and row_ … [10 caractères tronqués]`

  ```
Some(n / bloc * octets)
    }

    /// Nom lisible d'un type ggml. Rend `« type 29 »` pour un type inconnu
    /// plutôt que `?` : un point d'interrogation ne dit pas lequel.
    pub fn nom_type(ttype: u32) -> String {
        let n = match ttype {
            0 => "F32", 1 => "F16", 2 => "Q4_0", 3 => "Q4_1", 6 => "Q5_0", 7 => "Q5_1",
            8 => "Q8_0", 9 => "Q8_1", 10 => "Q2_K", 11 => "Q3_K", 12 => "Q4_K",
            13 => "Q5_K", 14 => "Q6_K", 15 => "Q8_K",
            16 => "IQ2_XXS", 17 => "IQ2_XS", 18 => "IQ3_XXS", 19 => "IQ1_S",
            20 => "IQ4_NL", 21 => "IQ3_S", 22 => "IQ2_S", 23 => "IQ4_XS",
            24 => "I8", 25 => "I16", 26 => "I32", 27 => "I64", 28 => "F64",
            29 => "IQ1_M", 30 => "BF16", 34 => "TQ1_0", 35 => "TQ2_0",
            39 => "MXFP4", 40 => "NVFP4",
            41 => "Q1_0", 42 => "Q2_0", 43 => "Q6_0", 44 => "Q6_1",
            45 => "Q3_0", 46 => "Q3_1", 47 => "Q2_0S", 48 => "Q2_1",
            _ => return format!("type {ttype}"),
        };
        n.to_string()
    }

    /// Somme des tailles de données annoncées par les descripteurs.
    pub fn octets_poids(&self) -> u64 {
        self.tensors.iter().map(Self::octets_tensor).
… [855 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"18 formats\\|17 formats\\|formats lisibles\" README.md REPRISE.md docs/*.md tools/*.sh 2>/dev/null | head -20", "description": "Find all format-count claims"}`

  ```
README.md:364:tools/portes_formats.sh                   # 17 formats × 2 blocs, contre libggml
README.md:368:**18 formats lisibles, 17 vérifiés à la porte** : `Q5_1` est lu par la même
REPRISE.md:1013:| `tools/portes_formats.sh` | **17 formats × 2 blocs** | tous exacts contre libggml |
REPRISE.md:1100:tools/portes_formats.sh          # 17 formats × 2 blocs, contre libggml
REPRISE.md:1120:   avec la grille doublée). 18 formats lisibles, 17 vérifiés contre libggml.
docs/plan-deepseek41-complet.md:201:     clusters 799,8557, 18 formats lisibles dont 17 vérifiés à la porte,
  ```

### 🤖 Assistant

⏵ Checking IQ1_M and F32/F16 handling to pin the exact readable count

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1283,1300p' drave-core/src/gguf.rs; echo \"=== 1240-1275 ===\"; sed -n '1240,1276p' drave-core/src/gguf.rs", "description": "Read IQ1_M and F32/F16 arms"}`

  ```
GGML_Q2_K | GGML_Q3_K | GGML_Q5_K | GGML_IQ2_XXS | GGML_IQ3_XXS
            | GGML_IQ1_S | GGML_IQ4_XS | GGML_IQ1_M => {
                let (taille, f): (usize, fn(&[u8]) -> Vec<f32>) = match t.ttype {
                    GGML_Q2_K => (84, Self::dequant_q2k),
                    GGML_Q3_K => (110, Self::dequant_q3k),
                    GGML_Q5_K => (TAILLE_Q5K, Self::dequant_q5k),
                    GGML_IQ2_XXS => (66, crate::formats::dequant_iq2xxs),
                    GGML_IQ3_XXS => (98, crate::formats::dequant_iq3xxs),
                    GGML_IQ1_S => (50, crate::formats::dequant_iq1s),
                    GGML_IQ4_XS => (136, crate::formats::dequant_iq4xs),
                    _ => (56, crate::formats::dequant_iq1m),
                };
                let ns = n_cols / 256;
                for sup in 0..ns {
                    out.extend_from_slice(&f(&buf[(row * ns + sup) * taille..]));
                }
            }
            GGML_Q4_K => {
=== 1240-1275 ===

    pub fn row_f32(&self, name: &str, row: usize, n_cols: usize) -> Vec<f32> {
        let t = self.tensor(name).unwrap_or_else(|| panic!("tenseur {name} absent"));
        let buf = self.tbuf(t);
        let 
… [1382 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking the block-size table to see if Q4_1 is reachable in practice

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '700,760p' drave-core/src/gguf.rs", "description": "Read octets/TABLE type mapping"}`

  ```
if debut + besoin > b.len() {
            return Err(std::io::Error::new(std::io::ErrorKind::UnexpectedEof, format!(
                "tenseur « {} » : {besoin} octets annoncés, {} disponibles dans le fichier {}",
                t.name, b.len() - debut, t.fichier)));
        }
        Ok(&b[debut..debut + besoin])
    }

    /// Taille en octets des données d'un tenseur, d'après son type ggml.
    /// `nelem()` compte des POIDS ; les types quantifiés rangent 32 ou 256
    /// poids par bloc, donc la taille n'est pas `nelem × taille d'un poids`.
    ///
    /// La table est celle de ggml, **relevée** et non devinée : un petit
    /// programme lié à `libggml` imprime `ggml_blck_size`/`ggml_type_size` pour
    /// chaque type (voir `docs/format-clusters.md`). Une taille inventée ferait
    /// un inventaire faux, et c'est exactement ainsi que l'inventaire de
    /// DeepSeek-V4-Flash a annoncé 8,56 Go pour 86,9 Go de fichiers : les
    /// tenseurs d'experts en `iq1_m` n'étaient pas dans la table.
    pub fn octets_tensor(t: &TensorInfo) -> u64 {
        if let Some(v) = Self::octets_tensor_opt(t) { return v; }
        // Un type hors table est compté zéro : le total serait faux, et 
… [2156 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"18 formats\\|dix-huit\" reports/*.md REPRISE.md journal/ 2>/dev/null | head -10; echo \"=== git log Q4_1 ===\"; git log --oneline -S \"GGML_Q4_1\" -- drave-core/src/gguf.rs | head -5", "description": "Find origin of 18-for … [11 caractères tronqués]`

  ```
REPRISE.md:1120:   avec la grille doublée). 18 formats lisibles, 17 vérifiés contre libggml.
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:4029:- **T2** `// pas 20 — dix-huit mille tranches de 900 Ko dispersées sur 18 Go`
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:4352:- README : 18 formats lisibles, portes de formats, et le diagnostic DRAVE_DEBUG_ETAT  - La liste des formats passe de 7 à 18, avec la distinction entre noyau dédi
journal/sessions/c25f97d1-9a4d-41da-b983-004f793afe43/digest.md:1811:        // pas 20 — dix-huit mille tranches de 900 Ko dispersées sur 18 Go
journal/sessions/c25f97d1-9a4d-41da-b983-004f793afe43/rapport.md:156:- **T1** `// pas 20 — dix-huit mille tranches de 900 Ko dispersées sur 18 Go`
=== git log Q4_1 ===
b97d129 Drave : renommage complet (crate, binaire, variables, documents)
  ```

### 🤖 Assistant

⏵ Reading the journal context that established the 18-format list

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '4340,4360p' journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md", "description": "Read journal context on 18 formats"}`

  ```
- Prelecture : quatrieme mecanisme mesure, quatrieme fois sans effet  - madvise sur les experts apres le routage : 25,73 contre 25,80 s (0,3 %) ; - madvise sur to
- Q2_K : dequantification implementee et verifiee contre ggml  Q2_K, c'est 59 Go des ffn_down_exps de DeepSeek-V4.1 -- sans lui, cette part du modele restait illi
- IQ2_XXS : 93 Go de V4.1 debloques, et un bug que la lecture n'aurait pas vu  Tables de grille EXTRAITES de ggml-common.h par un programme C (GGML_COMMON_IMPL_C)
- IQ1_M : 61 Go de DeepSeek-V4-Flash debloques (ecart 0,00e+00 avec ggml)  Troisieme format a grille. La grille IQ1_S (2048 codes signes) est extraite de ggml-com
- BF16 : lu et verifie (le f32 tronque a ses 16 bits de poids fort, exactement)  Deux modeles lourds l'utilisent (V4-Flash pour ses routeurs, MiniMax-H3). Verifie
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add drave-core/src/gguf.rs drave-core/src/formats.rs drave-core/src/main.rs tools/extraire_tables_ggml
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A drave-core/src && git commit -q -F - <<'EOF' routage des experts : quatre conventions, facteur 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git
… [2222 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"Q4_1\" README.md REPRISE.md docs/*.md reports/*.md 2>/dev/null | head -20", "description": "Search Q4_1 mentions in docs"}`

  ```
reports/rapport-inference.md:244:| | Q8_0 | Q4_0/Q4_1 | écart |
reports/rapport-inference.md:328:# modèle 4 bits (le fichier est mixte Q4_0/Q4_1) et élagage
  ```

### 🤖 Assistant

⏵ Reading README’s format inventory section for its own enumeration

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '330,375p' README.md", "description": "Read README format inventory"}`

  ```
ce qui s'active » est vérifié à l'échelle du moteur.

**Montée en charge** (densité 100 %, meilleur de 3 passes) : 1 thread 0,41 G év/s →
8 threads 2,75 → 16 threads 4,45 → **32 threads 4,84** → 39 threads **2,04** ❌.
L'attente active ne tolère aucune sursouscription : le pool est borné à `CPU − 1`
et vaut `3/4 × CPU` par défaut.

**Sans multiplieur** : décalages + additions donnent le résultat exact en 112,3 ms
contre 2,5 ms pour i8×i8 (×44,9 sur CPU) — mais **sur FPGA le multiplieur n'existe
pas**, et la contrainte du CDC est satisfaite sans réentraînement ni élagage.

> ⚠️ Trois pièges ont coûté une campagne de mesures fausses chacun : un état
> partagé avec **deux contrats de nettoyage** (d'où une « divergence » fantôme et
> un débit surestimé à 7,53 G év/s), un `&mut` dans la boucle chaude (barrière
> d'aliasing : 3,09 → 0,97 G év/s), et la **sursouscription** de l'attente active
> (39+1 threads sur 40 CPU : effondrement ×2,4 — et le `yield_now()` censé le
> corriger a tout empiré). Détail dans le rapport.

---

## Formats et modèles réellement lisibles

Le moteur lit **Q4_K, Q6_K, Q4_0, Q5_0, Q5_1, Q8_0, Q2_K, Q3_K, Q5_K, MXFP4,
IQ1_S, IQ1_M, IQ2_XXS, IQ3_XXS, IQ4_XS, BF16, F
… [1087 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"formats\" journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md | grep -i \"18\\|sept\\|liste\" | head -10", "description": "Find journal line about format list"}`

  ```
1818:- **§6 Axe 5 — formats, matériels, énergie** : trois matériels (SIMD, PTX, FPGA), et l'argument énergétique — *on ne lit que ce qui parle* ;
1855:5. **formats, matériels, énergie** — trois matériels (SIMD, PTX, FPGA), et l'argument *on ne lit que ce qui parle*.
4352:- README : 18 formats lisibles, portes de formats, et le diagnostic DRAVE_DEBUG_ETAT  - La liste des formats passe de 7 à 18, avec la distinction entre noyau dédi
  ```

### 🤖 Assistant

⏵ Reading the V4.1 inventory table about formats and the I8 claim

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '55,95p' docs/plan-deepseek41-complet.md", "description": "Read V4.1 inventory table"}`

  ```
**Trois de ces flux n'existent dans aucun moteur connu** (le gate du compresseur,
la sélection de candidats, le mélange HC). Les tracer est notre apport, pas un
détail d'implémentation.

---

## 3. Le point de départ, mesuré

### 3.1 Ce qui marche déjà sur V4.1 (365,71 Go, NVMe)

| capacité | mesure |
|---|---|
| en-têtes + inventaire | 1 046 tenseurs, 365,70 Go en **63,8 ms** (mmap) |
| description | **74 ms** : 40 couches, 384 experts top-6, racine de softplus ×1,5, routage par table des 3 premières couches |
| tables d'engram | 10 000 entrées en **219–524 ms**, 2,6 Mo touchés par table, **120 Mo de RSS** pour 365,7 Go |
| formats | IQ2_XXS, Q2_K, Q8_0, F16, F32, **I8** (engram) — déquantificateurs **vérifiés contre libggml** (aucun I32 dans ce fichier, vérifié sur les deux copies) |
| MLA à rang faible | **validée à la position 0** contre llama.cpp sur GLM-5.3 (corrélation 0,999024 ; l'écart croît ensuite — `reports/rapport-mla-experts.md` §7) |
| grappes | `commun.gguf` + `cluster-XX.gguf` + `mapping.tsv`, nœuds partiels |
| transport | protocole v5, modes 0-4 (dont **lot en listes**) |

### 3.2 Trois faits vérifiés le 02/10, qui commandent l'ordre

1. **llama.cpp ne connaît pa
… [843 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1585,1665p' drave-core/src/gguf.rs | grep -n \"fn \\|GGML_\" | head -20", "description": "Identify dequant function arms"}`

  ```
6:    pub fn dequant(&self, name: &str) -> Vec<f32> {
12:            GGML_BF16 => {
18:            GGML_F32 => {
23:            GGML_F16 => {
28:            GGML_Q8_0 => {
36:            GGML_Q4_0 => {
45:            GGML_Q4_1 => {
57:            GGML_Q5_0 | GGML_Q5_1 => {
58:                let (taille, f): (usize, fn(&[u8]) -> Vec<f32>) = if t.ttype == GGML_Q5_0 {
66:            GGML_MXFP4 => {
73:            GGML_Q4_K => {
  ```

### 🤖 Assistant

⏵ Parsing the V4.1 GGUF headers directly to check the I8/I32 and format claims

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport struct\nNOMS={0:'F32',1:'F16',2:'Q4_0',3:'Q4_1',6:'Q5_0',7:'Q5_1',8:'Q8_0',9:'Q8_1',10:'Q2_K',11:'Q3_K',12:'Q4_K',13:'Q5_K',14:'Q6_K',15:'Q8_K',16:'IQ2_XXS',17:'IQ2_XS',18:'IQ3_XXS',19:'IQ1_S',20:'IQ4_NL',21:'IQ3_S',22:'IQ2_S',23:'IQ4_XS',24:'I8',25:' … [2494 caractères tronqués]`

  ```
(no output)
[timed out after 60000ms]
[killed by signal: SIGTERM]
  ```

### 🤖 Assistant

⏵ Fixing the GGUF parser desync and re-running with a timeout

- **bash** `{"command": "cd /tmp && timeout 280 python3 - <<'PY'\nimport struct\nNOMS={0:'F32',1:'F16',2:'Q4_0',3:'Q4_1',6:'Q5_0',7:'Q5_1',8:'Q8_0',9:'Q8_1',10:'Q2_K',11:'Q3_K',12:'Q4_K',13:'Q5_K',14:'Q6_K',15:'Q8_K',16:'IQ2_XXS',17:'IQ2_XS',18:'IQ3_XXS',19:'IQ1_S',20:'IQ4_NL',21:'IQ3_S',22:'IQ2_S',23:'IQ4_XS', … [2535 caractères tronqués]`

  ```
### gguf/V4.1
 magic b'GGUF' ver 3 tenseurs 1046 kv 67 arch deepseek41
 types: {'F16': 110, 'F32': 493, 'I8': 2, 'IQ2_XXS': 80, 'Q2_K': 40, 'Q8_0': 321}
 I32: 0  I8: 2
 sinks: 40  derope: 0  output_hc: 0
### NVMe/V4.1
 magic b'GGUF' ver 3 tenseurs 1046 kv 67 arch deepseek41
 types: {'F16': 110, 'F32': 493, 'I8': 2, 'IQ2_XXS': 80, 'Q2_K': 40, 'Q8_0': 321}
 I32: 0  I8: 2
 sinks: 40  derope: 0  output_hc: 0
  ```

### 🤖 Assistant

⏵ Hunting for new internal contradictions in the edited prose

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== programme-recherche ===\" && grep -n \"trois propriétés\\|quatre propriétés\\|Ces trois\\|Ces quatre\" docs/programme-recherche.md; echo \"=== contexte-long sections ===\" && grep -n \"^#\\{2,4\\} \" docs/contexte-long.md; … [170 caractères tronqués]`

  ```
=== programme-recherche ===
24:L'architecture événementielle défendue ici possède quatre propriétés
47:Ces trois propriétés ne sont pas des opinions : elles sont mesurées, et elles
=== contexte-long sections ===
8:## 1. Ce que les modèles déclarent
21:## 2. Le budget, mesuré
39:## 3. Les trois murs, dans l'ordre où ils frappent
41:### a. Le préremplissage — le mur n° 1, et de très loin
61:### b. La bande passante du KV — le mur du décodage
75:### c. La portée de la rotation — le mur discret, et la température qui n'aide pas
97:## 4. Plan par étapes
114:## 4.bis KV quantifié : mesuré, et le 4 bits est cher
151:### 4.bis.2 À 8 192 jetons, la longueur exacte de la comparaison llama.cpp
176:### 4.bis.3 OÙ mettre les bits : les clés, pas les valeurs (30/09)
212:## 4.ter KV déporté en VRAM (E4) : le noyau, et ce qu'il donne
226:### Courbe mesurée (Qwen2.5-0.5B, une couche, 16 fils CPU, `--banc-kv`)
252:### Comment le noyau a été validé (et les trois bugs qu'il a fallu sortir)
272:### Dans le moteur (`DRAVE_GPU=1 DRAVE_GPU_KV=1`)
299:### Le PRÉREMPLISSAGE aussi : 286,6 s → 63,8 s sur un prompt de 3 961 jetons
321:### Pagination du miroir : la VRAM suit l'usage, pas le contexte
336:### Le 
… [1090 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '170,205p' reports/rapport-mla-experts.md; echo \"=== plan-mla-vision jeton 7 ===\"; grep -n \"jeton 7\\|4,07\\|position 2\" docs/plan-mla-vision.md", "description": "Compare MLA report table with plan-mla-vision claim"}`

  ```
## 7. Ce qui reste ouvert, et qui est le plus important

### La validation s'arrête à la position 2, et c'est mesuré

Comparaison à 7 jetons notés (llama.cpp : perplexité 890,4559) :

| position | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| écart de NLL (nous − référence) | **+0,009** | +0,372 | +0,611 | **+4,070** | +3,118 | +2,041 | +1,583 |

Le saut est à la position 3, pas une dérive progressive : c'est le signe d'un
mécanisme qui s'enclenche, pas d'une accumulation d'arrondis. Une piste écartée
en la testant : la quantification des activations lisait le tampon entier au
lieu de la tranche utile (elle pouvait donc dépendre de valeurs périmées de la
position précédente) — corrigé, **et l'écart n'a pas bougé d'un chiffre**
(4 807,76 contre 4 807,07). La piste est donc ailleurs, et le prochain pas est
maintenant outillé : `ref_logits --tensors 'ffn_moe_out-3'` d'un côté,
`DRAVE_DEBUG_MLA=1`/`DRAVE_DEBUG_ETAT=1` de l'autre, à comparer À LA POSITION 3.

1. **La validation MLA ne porte que sur 3 jetons et une position de référence.**
   La corrélation de 0,999 et le top-1 3/3 sont solides, mais ils ne disent rien
   de la tenue sur une séquence longue (le cache la
… [894 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying remaining claims: sessions, tests count, 24 files, mode4 5,6×

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== session dir ===\"; ls -d journal/sessions/8b6d46ab-6ad0-4648-92a8-0bec40a02526 2>&1; ls journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/ 2>/dev/null | head; echo \"=== tests ===\"; grep -rc \"#\\[test\\]\" drave-core … [258 caractères tronqués]`

  ```
=== session dir ===
journal/sessions/8b6d46ab-6ad0-4648-92a8-0bec40a02526
digest.md
rapport.md
session.jsonl.zstd
=== tests ===
unit #[test]: 48
integration: 
[exit code: 2]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== mode4 5,6x ===\"; grep -n \"5,6\\|20 jetons\\|1,5 fois\" reports/rapport-mode4-lot-listes.md | head -20; echo \"=== 24 fichiers ===\"; grep -rn \"24 fichiers\\|24 file\\|manifeste\" docs/plan-modeles-lourds.md | head -10", … [55 caractères tronqués]`

  ```
=== mode4 5,6x ===
45:| 20 | 2,30e-1 | 4,09e-2 | **5,6×** |
48:| 256 | 6,46e-2 | 5,64e-2 | 1,15× |
53:  (5,6× à vingt jetons) ; sur une séquence longue, elle se dilue comme toute erreur
92:6. la comptabilité « par jeton » divisait par `lot` au lieu de Σt : à 20 jetons en
=== 24 fichiers ===
13:de format (disposition des experts, manifeste multi-shards, index de routage) n'ont
23:> **Où en est ce plan (02/10)** : les 24 fichiers sont arrivés ; le lecteur
49:`tools/telecharger_modeles.py` + `tools/manifeste_modeles_lourds.json` :
76:   * **manifeste multi-shards** (`MANIFEST.json`) : indispensable de toute façon,
109:| 5 | **format** : manifeste + index + disposition contiguë | ✅ **écrit et mesuré sur Qwen3-30B-A3B** : `commun.gguf` + 8 `cluster-XX.gguf`, un nœud charge **3,20 Go au lieu de 18,56** et 625 ms au lieu de 3,9 s, 1 587 tenseurs vérifiés par empreinte — [`docs/format-clusters.md`](format-clusters.md) |
154:1 137,9 Go annoncés pour 24 fichiers, **tous arrivés à 12h40** : DeepSeek-V4.1
  ```

### 🤖 Assistant

⏵ Checking the manifest count and the converter's measured claims

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json;d=json.load(open('tools/manifeste_modeles_lourds.json'))\nprint(type(d), list(d)[:5] if isinstance(d,dict) else len(d))\n\" 2>&1 | head -5; echo \"=== count files in manifest ===\"; python3 - <<'PY'\nimport … [421 caractères tronqués]`

  ```
<class 'list'> 24
=== count files in manifest ===
gguf entries: 24
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== pin 23,2 27,6 ===\"; grep -rn \"23,2\\|27,6\" REPRISE.md docs/convertisseur.md | head -10; echo \"=== 2,73 / 0,81 / 921 / 566 ===\"; grep -rn \"2,73\\|0,81 s\\|921\\|566\" REPRISE.md docs/convertisseur.md | head -10; echo  … [127 caractères tronqués]`

  ```
=== pin 23,2 27,6 ===
REPRISE.md:135:| Épinglage NUMA | **perd** (23,2 → 25,5 s sur le 30 B) ; `--pin` déconseillé |
REPRISE.md:181:| noyau GPU Q6_K warp (tête liée Qwen 1.5B, 191,4 Mo) | **3,6 ms** contre 8,3 ms CPU 16 fils (23,2 → 53,6 Go/s), écart 3,3e-7 |
docs/convertisseur.md:173:| 5 | placement : épinglage NUMA, threads par couche | ✅ mesuré, **perdant** (`--pin` : 23,2 → 27,6 s) | 20,7 → 24,7 Go/s mesuré au banc |
docs/convertisseur.md:192:| 4 bis | **épinglage NUMA** (`--pin`) | ✅ mesuré, **négatif** | 23,2 → 25,5 s (cœurs physiques) et → 27,6 s (un socket) sur le 30B MoE |
docs/convertisseur.md:239:23,2 → 27,6 s sur le 30B MoE. Lier les seize fils à dix cœurs physiques met deux
docs/convertisseur.md:258:> mesuré **perdant** : 23,2 → 27,6 s sur le 30B MoE, voir plus haut) et le
=== 2,73 / 0,81 / 921 / 566 ===
docs/convertisseur.md:174:| 6 | **Q8_0 en place** (projections) | ✅ **fait** | chargement 2,73 → 0,81 s, mémoire 921 → 566 Mo |
docs/convertisseur.md:193:| 5 | **Q8_0 en place** (projections) | ✅ | chargement 2,73 → 0,81 s, mémoire 921 → 566 Mo |
docs/convertisseur.md:199:| Qwen2.5-0.5B | Q8_0 | 19,3885 | 32 | **0,81 s** | **0,57 Go** |
docs/convertisseur.md:259:> **Q8
… [634 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking the format-clusters.md:176 reference and whether mmap is really done

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/gitHub/Qtrinet 2>/dev/null; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"mmap\" docs/format-clusters.md; echo \"=== line 175-178 exact ===\"; awk 'NR>=174 && NR<=178{printf \"%d: %s\\n\", NR, $0}' docs/format-clusters.md; echo \"=== … [151 caractères tronqués]`

  ```
80:| fichier | en-tête (mmap) | lecture totale | octets |
181:* **Le mmap** : FAIT. `read_to_end` dupliquait le modèle (18,55 Go sur le tas en
=== line 175-178 exact ===
174: 
175:   **Ce qui manque** : la somme des contributions entre nœuds. Le moteur saute
176:   déjà un expert absent, mais rien n'additionne encore ce que deux nœuds calculent
177:   chacun de leur côté. Avec elle, deux nœuds à quatre clusters rendraient
178:   799,8557 pour 4,60 Go chacun — moins que les 6,28 Go d'un nœud complet.
=== code mmap ===
drave-core/src/gguf.rs:25:/// Le mmap ne lit rien : il rend une plage d'adresses, et le noyau lit les pages
drave-core/src/gguf.rs:41:    fn mmap(addr: *mut u8, len: usize, prot: i32, flags: i32, fd: i32, offset: i64) -> *mut u8;
drave-core/src/gguf.rs:58:/// utilisateur quand les poids sont mmappés : on ne peut pas lire soi-même sans
drave-core/src/gguf.rs:59:/// renoncer au mmap. Le noyau, lui, peut lancer plusieurs lectures de pages en
drave-core/src/gguf.rs:75:/// chargement. Le noyau parallélise ses lectures de pages, là où le mmap
drave-core/src/gguf.rs:78:/// Mesuré : charger 18,6 Go prend 6,8 s en mmap paresseux (2,7 Go/s) — proche du
drave-core/src/gguf.rs:106
… [804 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extracting and validating every file:line reference in the new text

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -oE '[A-Za-z0-9_./-]+\\.(md|rs|sh|py):[0-9]+' /tmp/full_now.diff | sort -u | while IFS=: read -r f l; do\n  # strip leading + or context chars\n  f=$(echo \"$f\" | sed 's/^[+ ]*//')\n  if [ ! -f \"$f\" ]; then echo \"FILE MISSIN … [280 caractères tronqués]`

  ```
docs/format-clusters.md:176                   ->   déjà un expert absent, mais rien n'additionne encore ce que deux nœuds calculent
FILE MISSING: main.rs:1987
  ```

### 🤖 Assistant

⏵ Confirming the stale line reference caused by the diff's own insertion

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"HEAD:176 ->\" && git show HEAD:docs/format-clusters.md | sed -n '176p' && echo \"WORK:181 ->\" && sed -n '181p' docs/format-clusters.md && echo \"=== added lines at top ===\" && git diff -- docs/format-clusters.md | head -20", … [61 caractères tronqués]`

  ```
HEAD:176 ->
* **Le mmap** : FAIT. `read_to_end` dupliquait le modèle (18,55 Go sur le tas en
WORK:181 ->
* **Le mmap** : FAIT. `read_to_end` dupliquait le modèle (18,55 Go sur le tas en
=== added lines at top ===
diff --git a/docs/format-clusters.md b/docs/format-clusters.md
index 6bf9f57..47270a5 100644
--- a/docs/format-clusters.md
+++ b/docs/format-clusters.md
@@ -5,6 +5,11 @@ fichier **GGUF autonome par cluster d'experts**, avec un manifeste qui porte la
 correspondance ; un nœud n'ouvre que ce qu'il sert — mesuré **3,20 Go au lieu de
 18,56** et **625 ms au lieu de 3,9 s** sur Qwen3-30B-A3B.
 
+**Et c'est le mécanisme de placement** : ces grappes sont les neurones qu'on
+répartit entre nœuds, et le flux d'activation se route de l'une à l'autre
+(`docs/vision.md`, axe 3). Le découpage n'est donc pas qu'un rangement de
+fichiers : c'est la carte des grappes entre composants et machines.
+
 Outil : [`tools/convertir_clusters.py`](../tools/convertir_clusters.py).
 
 ## Le problème
  ```

### 🤖 Assistant

⏵ Verifying the “puits” contradiction and remaining numeric claims

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 41-complet 130-145 ===\" && awk 'NR>=128 && NR<=148{printf \"%d: %s\\n\", NR, $0}' docs/plan-deepseek41-complet.md; echo \"=== REPRISE section 5 ===\" && grep -n \"^## \" REPRISE.md | head -12", "description": "Read V4.1 o … [36 caractères tronqués]`

  ```
=== 41-complet 130-145 ===
128:   modèle — et elle est exploitable (si 12 des 16 sont négligeables, la couche se
129:   simplifie).
130: - **Porte de correction** : `hc_attn_pre-0` puis `hc_attn_post-0` concordent.
131: - **Porte Drave** : la trace des 24 poids par jeton est écrite, relue, et un
132:   outil (`tools/analyse_hc.py`) dit la sparsité et la stabilité.
133: - **Interdit** : « les 4 copies sans le Sinkhorn ». Une HC approximative ne se
134:   voit pas — les quatre copies restent plausibles.
135: 
136: ### P2 — Épilogue d'attention : puits, dé-rotation, sortie groupée (≈ 3 h)
137: 
138: - Dé-rotation (`attn_derope`), puits par tête (`attn_sinks`), sortie groupée
139:   (`attn_output_a` → `attn_output_b`, `o_groups = 8`).
140: - **Porte de correction** : `kqv_out-0`, `attn_out-0`.
141: - **Porte Drave** : rien de nouveau à tracer ici, mais l'activation d'entrée de
142:   `attn_output_a` doit être **la même liste** que celle qui sort de l'attention —
143:   c'est le contrat du flux.
144: - **Interdit** : fusionner `attn_output_a/b` en une matrice dense.
145: 
146: ### P3 — Les couches brutes, de bout en bout (≈ 2 h)
147: 
148: - La couche 0 et la couche 1 de V4.1 (ratio 0) 
… [673 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== GLM couches ===\" && timeout 120 ./drave-core/target/release/drave /home/stephane/Data13TB/stephane/modeles/gguf/GLM-5.3-UD-IQ1_S/GLM-5.3-UD-IQ1_S-00001-of-00006.gguf --config 2>&1 | head -8; echo \"=== roadmap f16 int4 == … [201 caractères tronqués]`

  ```
=== GLM couches ===
modèle        : /home/stephane/Data13TB/stephane/modeles/gguf/GLM-5.3-UD-IQ1_S/GLM-5.3-UD-IQ1_S-00001-of-00006.gguf
architecture  : glm-dsa
couches       : 79 · cachés 6144
experts       : 256 par couche, 8 par jeton · FFN expert 2048
routage       : sigmoïde (source : expert_gating_func) · renormalisation oui · échelle 2.500
[mla] attention MLA à rang faible : cache LATENT (c_kv + k_rope), pas de fenêtre glissante ni de YaRN sur ce chemin. Validée contre llama.cpp sur GLM-5.3 : corrélation des logits 0,999024, top-1 3/3 (voir reports/rapport-mla-experts.md).
calculable    : oui (passe avant implémentée)
=== roadmap f16 int4 ===
30:| 1.4 | **Écart int8 résiduel** (+3,0 % contre +0,8 % chez llama.cpp à 8 192) | ✅ | **attribué** : tout l'écart est dans les CLÉS (clés f32 + valeurs int8 = +0,023 % ; l'inverse = +3,01 %) ; **courbe du placement des bits faite** (`reports/rapport-placement-bits-kv.md`) — à taille égale, mettre les bits sur les clés change l'erreur d'un facteur 130 à 840. Suite FAITE : **clés f16 = +0,018 % pour 39 % de la taille f32** — le meilleur réglage mesuré (`DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1`) |
94:`DRAVE_TRACE_BLOCS=1` (valeurs i8, échelle f16
… [1770 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Pinning which REPRISE sections actually hold the cited measurements

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk 'NR<=700 && /^## /{printf \"%d: %s\\n\", NR, $0}' REPRISE.md; echo \"=== enclosing for 265,135,187-195 ===\"; for l in 135 186 187 194 195 265 266; do sec=$(awk -v L=$l 'NR<=L && /^## /{s=$0} END{print s}' REPRISE.md); printf \"% … [91 caractères tronqués]`

  ```
14: ## 1. En une phrase
31: ## 2. Références de non-régression
99: ## 3. Ce qui est implémenté et vérifié
127: ## 4. Pièges de l'environnement (tous rencontrés)
142: ## 5. Règles de méthode (chacune a coûté une erreur)
161: ## 6. Les huit chantiers : où ils en sont
282: ## 6bis. Session « Drave » — le calcul réparti tient debout
637: ## 7. Carte du dépôt
665: ## 8. Premier pas suggéré pour la nouvelle session
=== enclosing for 265,135,187-195 ===
135 -> ## 4. Pièges de l'environnement (tous rencontrés)
186 -> ## 6. Les huit chantiers : où ils en sont
187 -> ## 6. Les huit chantiers : où ils en sont
194 -> ## 6. Les huit chantiers : où ils en sont
195 -> ## 6. Les huit chantiers : où ils en sont
265 -> ## 6. Les huit chantiers : où ils en sont
266 -> ## 6. Les huit chantiers : où ils en sont
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '99,126p' REPRISE.md | head -30; echo \"=== session-2026-09-30 report ===\"; grep -n \"+6 %\\|0,03 Go\\|25,77\\|MXFP4\" reports/rapport-session-2026-09-30.md | head -15", "description": "Check REPRISE section 3 and session rep … [13 caractères tronqués]`

  ```
## 3. Ce qui est implémenté et vérifié

| domaine | état |
|---|---|
| Formats lus **en place** | Q4_K, Q6_K, Q4_0, Q8_0, MXFP4, F16, F32 |
| MoE | routeur + biais de routeur, biais par expert, top-k, expert partagé, tranches contiguës |
| Architectures | q/k-norm (Qwen3), `post_attention_norm` (gpt-oss), sinks appris, fenêtre glissante, YaRN (défaut **off**), RoPE simple et partiel, `head_dim` déclaré |
| Tête de sortie | `output.weight` si non lié (bug corrigé), sinon `token_embd` |
| Tokenizers | Qwen2 **et** o200k (gpt-4o), tous deux lus du GGUF, sélectionnés par `tokenizer.ggml.pre` |
| Échantillonnage | température, top-k 40, top-p, **pénalité de répétition** (`--rep-penalty`, fenêtre `--hist`) |
| Génération | **sortie en flux** (`--flux`), **session multi-tours** (`--session`), arrêt sur fin de tour |
| Encodages | listes d'événements (push), dense int8 par ligne, dense 4 bits par bloc, **6 bits empaqueté par bloc** |
| GPU | noyaux PTX + API pilote, tête et projections opt-in (`DRAVE_GPU=1`) |
| Outils | `--ppl`, `--plan` (placement), `--tokenize`, `--bits N` (simulation de précision) |
| Mesure | `--ppl-texte F` (identifiants du tokenizer du modèle), `--depuis N` (ne note
… [1513 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Searching for stale YaRN-threshold prose the campaign may have missed

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"1,25 ×\\|1,25 x\\|5 120\\|au-delà de 4 096\\|dépasse la longueur\\|tient dans la longueur\" REPRISE.md README.md docs/*.md tools/*.sh 2>/dev/null | head -30", "description": "Find stale YaRN threshold statements"}`

  ```
REPRISE.md:166:| 2 | seuil de rotation YaRN | **fait, seuil à 4 × la longueur déclarée** | comparaison appariée (mêmes 512 jetons) : contexte 128→1536, RoPE simple 39,52/49,79/49,93/298,56 contre interpolation 42,13/82,02/82,15/578,86 → le simple gagne partout. **Au-delà du seuil** (5 120 jetons, corpus de 17 k maintenant disponible) : simple **9,6986** contre interpolation seule **1 269,1777** → le seuil de 4 096 était **trop bas**, puis celui de 1,25 × mesuré insuffisant ; le moteur ne bascule qu'à **4 × la longueur déclarée** (16 384 pour gpt-oss) — `docs/contexte-long.md` §5.quater. Au-delà (131 k) : non mesuré |
REPRISE.md:202:| rotation, comparaison appariée | RoPE simple gagne à TOUTES les longueurs mesurées : 128 à 1 536 (39,5 → 298,6), 5 120 (**9,70 contre 1 269,18**), 16 384 (**35,18 contre 1 133,02**) |
REPRISE.md:226:4. ~~**Rotation au-delà de 5 120 jetons.**~~ **MESURÉ À 16 k** : RoPE simple
docs/contexte-long.md:458:- ~~au-delà de 4 096, la mesure manque~~ **MESURÉ DEPUIS** : voir §5.ter.
docs/contexte-long.md:464:contexte 5 120, protocole apparié `--depuis` :
docs/contexte-long.md:471:**L'interpolation dégrade encore au-delà de 4 096** — d'un facteur 131 — alors
docs
… [506 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Rotation\" REPRISE.md | head; echo \"=== exact ===\"; awk 'NR>=110 && NR<=122{printf \"%d: %s\\n\", NR, substr($0,1,220)}' REPRISE.md", "description": "Read REPRISE section 3 rotation row"}`

  ```
114:| Rotation | **YaRN à retardement** : RoPE simple tant que `--ctx` tient dans `rope.scaling.original_context_length` (4 096), **interpolation YaRN seule au-delà** (la température `mscale` est la moitié nuisible : divise la perplexité par 8,9 à 512 jetons). `DRAVE_YARN=1` = YaRN complet des références, `DRAVE_YARN_NON=1` (ou `--sans-yarn`) = jamais, `DRAVE_YARN_MSCALE=0/1` = température seule. La trace `[config] rotation` dit lequel est actif |
226:4. ~~**Rotation au-delà de 5 120 jetons.**~~ **MESURÉ À 16 k** : RoPE simple
=== exact ===
110: | Encodages | listes d'événements (push), dense int8 par ligne, dense 4 bits par bloc, **6 bits empaqueté par bloc** |
111: | GPU | noyaux PTX + API pilote, tête et projections opt-in (`DRAVE_GPU=1`) |
112: | Outils | `--ppl`, `--plan` (placement), `--tokenize`, `--bits N` (simulation de précision) |
113: | Mesure | `--ppl-texte F` (identifiants du tokenizer du modèle), `--depuis N` (ne noter qu'à partir du jeton N, contexte ancré — les mêmes jetons deviennent comparables à 512, 1 024, 4 096… de contexte), `--ppl-profil` 
114: | Rotation | **YaRN à retardement** : RoPE simple tant que `--ctx` tient dans `rope.scaling.original_context_length
… [840 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading §5.quater and parsing rope/hc metadata for gpt-oss and V4.1

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '455,500p' docs/contexte-long.md", "description": "Read contexte-long 5.ter/5.quater"}`

  ```
- le **saut à ~1 500 jetons de contexte** est commun aux deux régimes : il vient
  du contenu AJOUTÉ (non contrôlé par le protocole), pas forcément de la
  longueur ;
- ~~au-delà de 4 096, la mesure manque~~ **MESURÉ DEPUIS** : voir §5.ter.

### 5.ter Au-delà du seuil : la bascule à 4 096 était trop basse

Le corpus de 16 455 jetons (gpt-oss) permet enfin de franchir la longueur
d'origine déclarée. Mêmes 512 jetons notés (**positions 4 608 à 5 119**),
contexte 5 120, protocole apparié `--depuis` :

| régime | perplexité |
|---|---|
| **RoPE simple** (`DRAVE_YARN_NON=1`) | **9,6986** |
| interpolation seule (`DRAVE_YARN=1 DRAVE_YARN_MSCALE=0`) | 1 269,1777 |

**L'interpolation dégrade encore au-delà de 4 096** — d'un facteur 131 — alors
que c'est exactement la zone où le moteur basculait. Le seuil « longueur
d'origine déclarée » n'est donc pas le bon : il ne bascule plus qu'à **1,25 ×**
cette longueur (5 120 pour gpt-oss), la plus grande longueur où le RoPE simple
ait été mesuré gagnant. Plus haut (16 k, 131 k), c'est une extrapolation non
mesurée : une passe à 16 384 jetons de contexte coûte environ une heure par
régime sur cette machine, et le corpus s'arrête à 17 k jetons.

### 5
… [1050 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && timeout 200 python3 - <<'PY'\nimport struct\ndef kv(path, keys):\n    f=open(path,'rb'); f.read(4); struct.unpack('<I',f.read(4)); nt=struct.unpack('<Q',f.read(8))[0]; nk=struct.unpack('<Q',f.read(8))[0]\n    def rdstr():\n        n=struct.unpack('<Q',f.read(8))[0]; return f. … [1011 caractères tronqués]`

  ```
gpt-oss: {'gpt-oss.context_length': b'\x00\x00\x02\x00', 'gpt-oss.rope.scaling.type': 'yarn', 'gpt-oss.rope.scaling.factor': b'\x00\x00\x00B', 'gpt-oss.rope.scaling.original_context_length': b'\x00\x10\x00\x00', 'gpt-oss.rope.scaling.yarn_beta_fast': b'\x00\x00\x00B', 'gpt-oss.rope.scaling.yarn_beta_slow': b'\x00\x00\x80?', 'gpt-oss.attention.sliding_window': b'\x80\x00\x00\x00'}
V4.1: {'deepseek41.hc_mult': b'\x04\x00\x00\x00', 'deepseek41.compress_ratios': None}
  ```

### 🤖 Assistant

⏵ Checking the tokenize→ppl pipeline format used by the new gate block

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fn run_tokenize\" -A 40 drave-core/src/main.rs | head -60", "description": "Read run_tokenize"}`

  ```
3888:fn run_tokenize(opt: Options) {
3889-    let path = &modele_chemin();
3890-    let texte = opt.texte.clone().unwrap_or_default();
3891-    let fichier = opt.fichier.clone().unwrap_or_default();
3892-    let sortie = opt.sortie.clone().unwrap_or_default();
3893-    // En-tête seul : le décodage du vocabulaire n'a pas besoin des poids, et
3894-    // `open` lisait le fichier entier (62 Go pour gpt-oss) à chaque appel.
3895-    let g = Gguf::open_meta_auto(path).expect("ouverture du GGUF");
3896-    let tk = build_tokenizer(&g);
3897-    if !fichier.is_empty() {
3898-        // Encoder un corpus ENTIER avec le tokenizer du modèle : chaque modèle
3899-        // a le sien, et nourrir un modèle avec les identifiants d'un autre
3900-        // donne une perplexité qui ne mesure que l'absurdité de l'entrée.
3901-        let texte = std::fs::read_to_string(&fichier).expect("fichier illisible");
3902-        let ids = tk.encode(&texte);
3903-        let cible = if sortie.is_empty() { format!("{fichier}.ids") } else { sortie };
3904-        let corps: Vec<String> = ids.iter().map(|i| i.to_string()).collect();
3905-        std::fs::write(&cible, corps.join(",")).expect("écriture impossib
… [1273 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -3 /tmp/ids_oss_512.txt 2>/dev/null && wc -l /tmp/ids_oss_512.txt 2>/dev/null; echo \"=== ids_qwen head ===\"; head -c 60 /tmp/ids_qwen.txt 2>/dev/null | od -c | head -3; echo \"=== how ppl reads ids ===\"; grep -n \"fn lire_ids … [143 caractères tronqués]`

  ```
198
314
13169
512 /tmp/ids_oss_512.txt
=== ids_qwen head ===
0000000   1   9   8   ,   2   8   4   ,   8   3   9   7   ,   4   2   5
0000020   ,   1   0   9   6   5   ,   4   6   5   ,   2   8   4   ,   1
0000040   4   7   3   1   ,   8   3   9   7   ,   4   2   5   ,   1   0
=== how ppl reads ids ===
668:            "--bits-attn" => { if suivant(i).parse::<u32>().unwrap() == 6 { o.b6 |= 2; } 2 }
669:            "--bits-ffn" => { if suivant(i).parse::<u32>().unwrap() == 6 { o.b6 |= 1; } 2 }
774:                if let Ok(v) = x.trim().parse::<u32>() { ids.push(v); }
1124:            if let Ok(v) = x.trim().parse::<u32>() { ids.push(v); }
  ```

### 🤖 Assistant

⏵ Testing the head -c 20000 UTF-8 cut and the ppl id parser

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nd=open('data/wikitext2_test.txt','rb').read(20000)\ntry:\n    d.decode('utf-8'); print('20000 octets: UTF-8 valide')\nexcept UnicodeDecodeError as e:\n    print('20000 octets: COUPURE INVALIDE ->', e)\n\"; echo \"=== p … [268 caractères tronqués]`

  ```
20000 octets: UTF-8 valide
=== ppl reader 1115-1130 ===
1116: /// Charge une liste d'identifiants et la pose sur le modèle.
1117: ///
1118: /// Rend `false` si le fichier est vide ou illisible — auquel cas la tête reste
1119: /// complète, ce qui est le comportement sûr.
1120: fn poser_tete_restreinte(mdl: &mut model::Model, fichier: &str) -> bool {
1121:     let mut ids: Vec<u32> = Vec::new();
1122:     if let Ok(t) = std::fs::read_to_string(fichier) {
1123:         for x in t.split(|c: char| c == ',' || c.is_whitespace()) {
1124:             if let Ok(v) = x.trim().parse::<u32>() { ids.push(v); }
1125:         }
1126:     }
1127:     ids.sort_unstable();
1128:     ids.dedup();
1129:     if ids.is_empty() {
1130:         eprintln!("[tete] {fichier} ne contient aucun identifiant utilisable : tête complète");
=== 768-780 ===
768:         poser_tete_restreinte(&mut mdl, f);
769:     }
770:     if let Some(f) = &opt.tete_garantie {
771:         let mut ids: Vec<u32> = Vec::new();
772:         if let Ok(t) = std::fs::read_to_string(f) {
773:             for x in t.split(|c: char| c == ',' || c.is_whitespace()) {
774:                 if let Ok(v) = x.trim().parse::<u32>() { ids.push(v);
… [225 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying ppl id loading, README value, session report and multi-shard report

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fn lire_ids\\|fn ids_de\\|fn charge_ids\" drave-core/src/main.rs; grep -n \"15.6017\\|15,6017\" README.md | head -5; echo \"=== session report headings ===\"; grep -n \"^#\\|^## \" reports/rapport-session-2026-09-30.md | he … [64 caractères tronqués]`

  ```
378:| **gpt-oss-120b** (MoE, MXFP4) | MXFP4 | **15,6017** (ctx 256) | blocs lus | 60 Go |
=== session report headings ===
1:# Session du 30/09 — index des chantiers
8:## Ce qui est livré
24:## Les défauts trouvés, et par qui
55:## Le créneau 15h07 → 18h00, en plus court
65:## Les vérifications de fin de journée
78:## Ce qui n'a pas été fait
90:## Portes, à l'heure d'écrire
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== multifichiers ===\"; grep -n \"1 328\\|1328\\|86,90\\|86.90\" reports/rapport-lecteur-multifichiers.md | head -10; echo \"=== open_multi ===\"; grep -n \"fn open_multi\" drave-core/src/gguf.rs; echo \"=== histoire QTNT === … [125 caractères tronqués]`

  ```
=== multifichiers ===
37:| annoncé par les descripteurs | **86,90 Go** |
38:| somme des fichiers sur disque | **86,90 Go** |
39:| tenseurs | 1 328 (shard 1 : 0, shard 2 : 784, shard 3 : 544) |
159:Kimi-K2.7 303,90 = 303,9 · DeepSeek-V4-Flash 86,90 = 86,9 · GLM-5.3-Flash
=== open_multi ===
447:    pub fn open_multi<P: AsRef<Path>>(chemins: &[P]) -> std::io::Result<Self> {
611:    pub fn open_multi_meta<P: AsRef<Path>>(chemins: &[P]) -> std::io::Result<Self> {
=== histoire QTNT ===
  ```

### 🤖 Assistant

⏵ Checking histoire.md for the QTNT rename and the session report for table sources

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== histoire ===\"; grep -n \"renomm\\|Renomm\\|Drave\\|30/09\" docs/histoire.md | head -20; echo \"--- size ---\"; wc -l docs/histoire.md", "description": "Search histoire.md for rename"}`

  ```
=== histoire ===
1:# Histoire du projet, et le renommage
4:changé de nom, partout, d'un coup.** Renommer efface des traces ; ce fichier est
13:| **Drave** (aujourd'hui) | le moteur Rust qui exploite cette représentation sur CPU, GPU et FPGA, avec le contexte long (KV paginé, MLA, vision) et la distribution en ligne de mire | `docs/vision.md` |
20:**Drave** : *stream of logs* — le flux des listes. Et, en français d'ici, la
36:| « Qtrinet » dans les rapports et les documents | « Drave » |
73:Le renommage a été fait « tout, tout de suite », y compris dans les rapports
--- size ---
78 docs/histoire.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,30p' reports/rapport-session-2026-09-30.md; echo \"=== KV/cache mentions ===\"; grep -n \"KV\\|cache\\|experts\\|pagination\" reports/rapport-session-2026-09-30.md | head -20", "description": "Read session report content"}`

  ```
# Session du 30/09 — index des chantiers

Trois créneaux : 10h06–11h42 (time-box de 2 h), 11h46–15h00 puis 15h07–18h00
(autonomie et parallélisme). Les commits, les campagnes de mesure lourdes et les
relectures déléguées sont comptés dans le journal ; ce document est l'index des
chantiers, pas le décompte. Chaque chiffre a son rapport ; ceci est l'index.

## Ce qui est livré

| chantier | résultat | rapport |
|---|---|---|
| **Calcul réparti fidèle** | écart local/réparti **0,00e0** — 144,8289 des deux côtés à 40 jetons, 9,5146 à 1 024 | `rapport-phase3-reparti.md` |
| **Préremplissage par LOTS** (mode 3) | 256 jetons en **4 lots** (ou 1 seul) → 0,00e0 ; **18× plus rapide** qu'un flux par jeton sur un lien à 20 ms | `rapport-prefill-reparti.md` |
| **Transport en listes** | dense 3 663 octets → **1 629** par flux (÷2,3) pour 1,3 % d'écart à 1 024 jetons | `rapport-transport-liste.md` |
| **où mettre les bits du cache KV** | à taille ÉGALE : clés f32 + valeurs int8 **+0,023 %** contre **+3,01 %** pour l'inverse (facteur **130**) ; 4 bits : +0,46 % contre **+385 %** (facteur **840**) | `rapport-placement-bits-kv.md` |
| **Format de trace v2/v3** | 132 396 736 → **66 370 408** (sans p
… [1975 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Auditing the vision axe-2 table rows against their claimed sources

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk 'NR>=100 && NR<=126{printf \"%d: %s\\n\", NR, $0}' docs/vision.md", "description": "Read vision axe-2 table"}`

  ```
100: architecture qui se règle sur ces mesures n'est plus choisie une fois pour
101: toutes. C'est la finalité d'un moteur qui conduit des listes : le journal n'est
102: pas un sous-produit, c'est l'instrument de réglage.
103: 
104: ---
105: 
106: ## 3. Axe 2 — Répartir sur les composants d'une machine
107: 
108: C'est l'axe le plus avancé, et il est **mesuré** :
109: 
110: | ce qui est réparti | où | gain mesuré |
111: |---|---|---|
112: | cache KV d'une couche | VRAM (paginée, sur **deux** cartes) | attention à 1 M de clés : 968 → **13,2 ms** par couche |
113: | attention complète | noyau GPU, décodage **et** préremplissage | 22,16 → **3,29 ms/jeton** (÷6,7) ; préremplissage **×2,8** |
114: | projections Q8_0 (> 8 Mo) | GPU, opt-in | tête : 15,6 → 6,2 ms/jeton |
115: | tête Q6_K | GPU | 7,58 → **3,60 ms/jeton** |
116: | experts MXFP4 | cache VRAM LRU | **+6 %** — mesuré, verdict : ne pas activer tel quel |
117: | cache KV (hôte) | pagination à la demande | contexte 1 M : **0,03 Go** au lieu de 25,77 Go |
118: 
119: Sources de ce tableau : `docs/contexte-long.md` (KV paginé, attention GPU),
120: `reports/rapport-session-2026-09-30.md`, `REPRISE.md` §5.
121: 
122: La leçon de cet a
… [384 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,40p' docs/histoire.md", "description": "Read histoire.md renaming table"}`

  ```
# Histoire du projet, et le renommage

Ce document est là pour une raison précise : **le 30 septembre 2026, le projet a
changé de nom, partout, d'un coup.** Renommer efface des traces ; ce fichier est
la trace qu'on ne voulait pas perdre.

## 1. Le projet a eu trois âges

| âge | ce qu'il était | où c'est écrit |
|---|---|---|
| **Qtrinet** (origine) | inférence de LLM en ternaire / multi-bits sur un cluster de cartes **Stratix V** (Microsoft Storey Peak), 100 % logique, sans DSP. Le cahier des charges d'origine est **conservé tel quel** : [`Qtrinet-bootstrap.md`](../Qtrinet-bootstrap.md) — c'est un document daté, il n'est pas réécrit | `Qtrinet-bootstrap.md`, `README.md` §« Écarts avec le CDC » |
| **le virage événementiel** | l'idée qui a tout changé : ne plus multiplier des matrices, mais **pousser des listes d'activation** vers leurs destinations (AER, *Address Event Representation*). Le prototype C mesure **7,79 G événements/s**, le croisement push/pull est mesuré à **~22 % de densité** | `reports/rapport-cpu-aer.md`, `reports/rapport-croisement-push-pull.md`, `reports/rapport-encodage.md` |
| **Drave** (aujourd'hui) | le moteur Rust qui exploite cette représentation sur CPU, 
… [1225 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Sourcing the 15,6→6,2 row and locating the §3 citation line

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"15,6\\|15.6 →\\|6,2 ms\" REPRISE.md docs/contexte-long.md docs/vision.md | head -10; echo \"=== vision cite lines ===\"; grep -n \"REPRISE.md\" docs/vision.md", "description": "Source the projections row and list vision ci … [9 caractères tronqués]`

  ```
REPRISE.md:41:> **799,8557** · gpt-oss-120b MXFP4 ctx 256 = **15,6017** (**changée** par le
REPRISE.md:79:| gpt-oss-120b MXFP4 | `--dense --limit 512`, ids_oss | **15,6017** (510 jetons, deux fenêtres) — était 15,1757 avant le correctif de routage du 02/10 |
REPRISE.md:221:   un noyau AVX2 (le déport GPU Q8_0 existe déjà : 15,6 → 6,2 ms/jeton sur
REPRISE.md:681:    --ppl /tmp/ids_oss_512.txt --ctx 256 --dense --threads 16 --limit 512  # attendu 15,6017
REPRISE.md:1011:| gpt-oss-120b MXFP4 ctx 256 | **15,6017** | **changée** (15,1757 avant) — voir ci-dessous |
REPRISE.md:1115:   lot ; quatre tests unitaires les encodent. Porte gpt-oss : 15,1757 → 15,6017,
docs/vision.md:114:| projections Q8_0 (> 8 Mo) | GPU, opt-in | tête : 15,6 → 6,2 ms/jeton |
docs/vision.md:181:  gpt-oss ctx 256 = **15,6017**) sont l'application minimale de cette idée :
=== vision cite lines ===
53:et la trace est de **1,5e-5** (`REPRISE.md` §3, `DRAVE_FLUX_VERIF=1`).
120:`reports/rapport-session-2026-09-30.md`, `REPRISE.md` §5.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"QTNT\" --include=*.md --include=*.rs --include=*.py --include=*.sh . 2>/dev/null | grep -v \"^./journal/\" | head -20", "description": "Find remaining QTNT references"}`

  ```
./reports/rapport-coherence-vision.md:40:| `convertisseur.md` | **corrigé, 7 sites** | « Ordre de marche » remis à l'état réel (mmap, NUMA, Q8_0, routeur MoE, lecteur Q4_K/Q6_K étaient **faits**) ; hypothèses « suspects restants » remplacées par ce qui a été **testé le jour même** ; conteneur renommé (ex-`QTNT`) ; « calque » → « couche » |
./docs/convertisseur.md:111:## 5. Format proposé : conteneur **Drave** (ex-`QTNT`), adossé au format de flux `DRVF`
./docs/convertisseur.md:113:> Le sigle `QTNT` porte l'ancien nom du projet ; le renommage du 30/09 est « fait
./docs/convertisseur.md:172:| 4 | conteneur **Drave** (ex-`QTNT`) + index de placement | index de placement ✅ (`--plan`) ; le conteneur reste **proposé** | plan CPU/GPU/NUMA lisible avant les poids |
  ```

### 🤖 Assistant

⏵ Verifying spiking energy, cluster-original PPL, and Kimi MLA figures

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== nJ ===\"; grep -rn \"8,3 nJ\\|57 nJ\\|6,9 ×\\|6,9×\\|4,83 G\" reports/*.md docs/*.md | head -12; echo \"=== 30B origine ===\"; grep -n \"799,8557\\|799.8557\\|original\" docs/format-clusters.md | head -12", "description":  … [46 caractères tronqués]`

  ```
=== nJ ===
reports/bilan-multi-materiel.md:46:| CPU (16 threads) | **5,3 G évts/s** mesuré | ~57 nJ |
reports/bilan-multi-materiel.md:47:| FPGA (1 carte, 51 voies) | 4,83 G évts/s *projeté* (limite DDR3) | **~8,3 nJ** |
reports/bilan-multi-materiel.md:109:Une carte = 4,83 G évts/s = **un CPU 20 cœurs**, pour 41 % de la logique et 41 %
reports/bilan-multi-materiel.md:111:(8,3 nJ contre 57 pour le CPU, soit 7×) et l'absence de multiplieur. Face au GPU
reports/bilan-multi-materiel.md:117:le CPU (12,7 contre 57 nJ), et il consomme les mêmes listes. **Il n'y a pas de
reports/rapport-coherence-vision.md:49:| `comparaison-spiking.md` | **corrigé, 4 sites** | encadré : le spike est un **moyen** d'obtenir la parcimonie, le cœur de Drave (grappes + lecture des flux) n'est pas en cause ; sources internes citées ; 8,3 nJ **projeté** ; densité mesurée **17,9 %** sous le croisement de 22 % |
docs/comparaison-spiking.md:63:| Énergie par opération | E_AC = 0,9 pJ contre E_MAC = 4,5 pJ (Horowitz) | 8,3 nJ/événement (FPGA, **projeté** : 4,83 G évts/s, limite DDR3) contre 57 nJ (CPU, **mesuré**) — rapport 6,9× |
docs/comparaison-spiking.md:157:  Notre chiffre, lui, donne 6,9× entre CPU et FPGA, du mê
… [153 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== Kimi 1026 ===\"; grep -n \"1 026\\|73 s\\|§6ter\" reports/rapport-mla-experts.md | head -10; echo \"=== V4.1 365 ===\"; grep -n \"365,71\\|365,7\" reports/rapport-execution-v41.md | head -5", "description": "Check Kimi and … [15 caractères tronqués]`

  ```
=== Kimi 1026 ===
96:- **Kimi-K2.7 (1 026 G poids)** : `--config` annonce « calculable : oui »,
151:## 6ter. Kimi-K2.7 : 1 026 G poids, premier calcul
157:| chargement | **161 s** (mmap, 1 026 G poids sur le NVMe) |
158:| 2 jetons notés | **146 s** (73 s/jeton) |
166:Aucune référence externe n'a été calculée pour Kimi (1 026 G, deux chargements de
=== V4.1 365 ===
4:(365,71 Go, 1 046 tenseurs, 40 couches, 384 experts dont 6 par jeton).
15:| en-têtes seuls (`--tensors`) | mmap, aucune copie | 1 046 tenseurs, **365,70 Go** lus en **63,8 ms** |
18:| sonde engram (`--sonder-engram 10000`) | mmap, 16 lecteurs | table 1 : 10 000 entrées en **524 ms** (2,6 Mo touchés sur 101,4 Go) · table 2 : **219 ms** · RSS max **120 Mo** pour 365,7 Go adressés |
22:mmap sans copie (365,7 Go adressés, 120 Mo résidents), parallélisme des lecteurs
  ```

### 🤖 Assistant

⏵ Reading the clusters table header and the trinaire source

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk 'NR>=160 && NR<=174{printf \"%d: %s\\n\", NR, $0}' docs/format-clusters.md; echo \"=== trinaire ===\"; grep -n \"trinaire\\|deux listes\\|signe\" reports/rapport-encodage.md | head -12", "description": "Read clusters table and tr … [15 caractères tronqués]`

  ```
160: ## Ce qui reste
161: 
162: * **Le nœud partiel** : `DRAVE_CLUSTERS=0,3` ne charge que ces clusters — et un
163:   cluster **demandé mais absent du disque est une erreur**, pas un silence : sans
164:   cela, un artefact amputé passait pour complet et les contributions manquantes
165:   disparaissaient sans un mot. Mesuré
166:   sur Qwen3-30B, mêmes 7 jetons :
167: 
168:   | clusters | perplexité | mémoire |
169:   |---|---|---|
170:   | 1 | 268 786,62 | **2,35 Go** |
171:   | 2 | 63 780,09 | 2,83 Go |
172:   | 4 | 3 378,91 | 4,60 Go |
173:   | 8 | **799,8557** | 6,28 Go |
174: 
=== trinaire ===
3:Idée testée : remplacer `(position, valeur)` par **deux listes triées de
4:destinations** (les « + » et les « − »). Le signe est porté par l'appartenance
12:| Motif | k | Densité | Accuracy | bitmap+signe | **listes signées** | CSR | dense | entropie | écart moyen |
49:| Densité | bitmap + signe | **listes signées** | gain | tok/s 7B | vs dense 2 b |
59:**Bascule vers 20 % de densité** : au-dessus, le bitmap + signe gagne (les
67:   l'appartenance à la liste porte le signe, et il ne reste que des **positions**.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '35,55p' reports/rapport-mode4-lot-listes.md", "description": "Read mode4 report table"}`

  ```
du mode 2 (le critère posé était 1,5×).

### Ce que le ratio vaut selon la longueur (relecture adversariale)

Un relecteur a refait la mesure avec des identifiants synthétiques et des
longueurs variées ; le rapport entre l'écart du mode 4 et celui du mode 2 **n'est
pas constant** :

| jetons | mode 4 | mode 2 | ratio |
|---|---|---|---|
| 20 | 2,30e-1 | 4,09e-2 | **5,6×** |
| 40 | 1,11e-1 | — | — |
| 64 | 1,86e-2 | 3,70e-2 | 0,50× |
| 256 | 6,46e-2 | 5,64e-2 | 1,15× |

Deux choses à en tirer, et une à ne pas en tirer :

* sur une **courte** séquence, la quantification du lot coûte cher en relatif
  (5,6× à vingt jetons) ; sur une séquence longue, elle se dilue comme toute erreur
  stationnaire (1,15× à 256, 0,50× à 64) ;
* le **découpage en lots partiels est innocent** : `--limit 20 --lot 20` et
  ```

### 🤖 Assistant

⏵ Checking where the Qwen3-30B original 799,8557 value is established

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"799,8557\\|799.8557\" REPRISE.md reports/*.md docs/*.md tools/*.sh | head -20", "description": "Find all 799,8557 occurrences"}`

  ```
REPRISE.md:41:> **799,8557** · gpt-oss-120b MXFP4 ctx 256 = **15,6017** (**changée** par le
REPRISE.md:1010:| Qwen3-30B en clusters ctx 64, 8 jetons | **799,8557** | inchangée |
reports/rapport-lecteur-multifichiers.md:177:(799,8557 dans les deux cas) :
reports/rapport-lecteur-multifichiers.md:204:| **8** | **799,8557** | 6,28 Go | 10,65 s |
reports/rapport-lecteur-multifichiers.md:209:Deux nœuds à quatre clusters rendraient 799,8557 pour 4,60 Go chacun, soit moins
reports/rapport-mla-experts.md:99:  aiguillage : Qwen2.5-0.5B **19,3885**, Qwen3-30B en clusters **799,8557**.
reports/rapport-optimisations-auto.md:135:**clusters 799,8557** inchangées, génération identique au token près.
reports/rapport-routage-experts.md:65:| Qwen3-30B clusters ctx 64, 8 jetons | 799,8557 | **799,8557** | inchangée, au bit près |
reports/rapport-routage-experts.md:75:déplacé la porte Qwen3-30B de 799,8557 à 799,8152 (−0,005 %). Cause : la
docs/format-clusters.md:173:  | 8 | **799,8557** | 6,28 Go |
docs/format-clusters.md:178:  799,8557 pour 4,60 Go chacun — moins que les 6,28 Go d'un nœud complet.
docs/plan-deepseek41-complet.md:201:     clusters 799,8557, 18 formats lisibles dont 17 vérifiés à la po
… [303 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"30B\" reports/rapport-grappes.md 2>/dev/null | head -10; echo \"=== decoupage-moe ===\"; grep -rn \"799\\|original\\|identique\" reports/rapport-decoupage-moe.md 2>/dev/null | head -15", "description": "Look for cluster-vs … [20 caractères tronqués]`

  ```
=== decoupage-moe ===
41:| 4 | **0,799** | **1,94** | 0,440 | 3,59 | ×1,8 |
46:et celle qui se contente de **trier les experts par fréquence** sont **identiques**
  ```

### 🤖 Assistant

⏵ Reading the multi-shard report's “both cases” line and the routing report's caveat

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk 'NR>=168 && NR<=212{printf \"%d: %s\\n\", NR, $0}' reports/rapport-lecteur-multifichiers.md", "description": "Read multifichiers cluster table"}`

  ```
168: aucune n'a encore de `forward`. Kimi est en huit fichiers, GLM en six : le lecteur
169: les rassemble à partir d'un seul chemin.
170: 
171: ### Le mmap : 3,3× plus rapide, 3× moins de mémoire
172: 
173: `read_to_end` lisait tout le fichier et en gardait une copie dans le tas, **en
174: plus** du cache de pages du noyau — deux fois la taille du modèle en mémoire
175: physique. Les fichiers sont maintenant **mappés** (le noyau lit les pages à la
176: demande). Sur Qwen3-30B-A3B en clusters, mêmes 7 jetons, perplexité identique
177: (799,8557 dans les deux cas) :
178: 
179: | | chargement + passe | mémoire maximale (RSS) |
180: |---|---|---|
181: | mappé (défaut) | **9,32 s** | **6,35 Go** |
182: | lu en entier (`DRAVE_MMAP=0`) | 30,68 s | 19,20 Go |
183: 
184: Les 19,20 Go sont exactement la taille du modèle : la copie complète. Le mappé
185: n'en touche que 6,35 Go — les pages réellement lues. Un modèle dont on
186: n'utiliserait qu'un huitième des experts ne lirait qu'un huitième des octets.
187: 
188: Portes revérifiées dans les deux modes : Qwen2.5-0.5B ctx 256 = **19,3885** avec
189: et sans mmap.
190: 
191: ### Le nœud partiel : un huitième des experts pour un huitième de 
… [1159 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk 'NR>=60 && NR<=85{printf \"%d: %s\\n\", NR, $0}' reports/rapport-routage-experts.md", "description": "Read routing report gate table"}`

  ```
60: ## 3. Ce qui est mesuré, et ce qui a bougé
61: 
62: | porte | avant | après | verdict |
63: |---|---|---|---|
64: | Qwen2.5-0.5B Q8_0 ctx 256 (dense) | 19,3885 | **19,3885** | inchangée, au bit près |
65: | Qwen3-30B clusters ctx 64, 8 jetons | 799,8557 | **799,8557** | inchangée, au bit près |
66: | gpt-oss-120b ctx 256 | 15,1757 | **15,6017** | **changée** — voir ci-dessous |
67: 
68: Le changement de gpt-oss est le seul effet visible sur les portes, et il est
69: justifié par le code de référence : `build_moe_ffn` de llama.cpp met le biais
70: dans `selection_probs` (la sélection) mais prend les poids dans `probs`
71: (`softmax(logits[choisis])`, **sans** biais). L'ancien code laissait le biais
72: dans le softmax. **15,1757 était auto-cohérent, pas juste.**
73: 
74: Au passage, une leçon de méthode : réunir les deux chemins de routage a d'abord
75: déplacé la porte Qwen3-30B de 799,8557 à 799,8152 (−0,005 %). Cause : la
76: renormalisation était écrite `x / s` au lieu de `x * (1/s)`, ce qui n'est pas le
77: même flottant au dernier bit, et 48 couches l'amplifient. La comparaison
78: **ancien binaire / nouveau binaire sur le même modèle** (un `git worktree` sur
79: le commit
… [301 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Looking for a direct original-vs-clusters measurement for Qwen3-30B

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"Qwen3-30B\" REPRISE.md reports/*.md | grep -i \"origine\\|original\\|dense\\|7,61\\|ctx 64\" | head -20", "description": "Search original 30B measurement"}`

  ```
REPRISE.md:40:> ctx 256 = **19,3885** (inchangée) · clusters Qwen3-30B ctx 64 limit 8 =
REPRISE.md:77:| Qwen3-30B-A3B MoE | `--dense --limit 128` | **7,6139** |
REPRISE.md:1010:| Qwen3-30B en clusters ctx 64, 8 jetons | **799,8557** | inchangée |
reports/rapport-prefill-par-lots.md:33:endroit. **Effet mesuré : nul** sur Qwen3-30B-A3B (7,6139 avant comme après — ce
reports/rapport-routage-experts.md:65:| Qwen3-30B clusters ctx 64, 8 jetons | 799,8557 | **799,8557** | inchangée, au bit près |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"identique à l'original\\|sans changer un chiffre\\|mêmes chiffres\\|identique au modèle\" REPRISE.md reports/*.md docs/*.md | head -20", "description": "Find identity claims between clusters and original"}`

  ```
reports/rapport-attention-creuse.md:140:➡️ **Divisée par deux**, gratuitement, sans changer un chiffre de la perplexité.
docs/contexte-long.md:35:Sans la fenêtre par couche, les mêmes chiffres doublent (154,6 Go en f32 à 1 M).
docs/programme-recherche.md:45:   sans changer un chiffre (Qwen3-30B : **799,8557**, identique à l'original).
  ```

### 🤖 Assistant

⏵ Searching for evidence of the original Qwen3-30B baseline

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1000,1015p' REPRISE.md; echo \"=== cherche baseline ===\"; grep -rn \"modèle entier\\|modèle original\\|l'original\\|non découpé\\|18,56 Go\" docs/format-clusters.md reports/rapport-grappes.md reports/rapport-decoupage-moe.md … [88 caractères tronqués]`

  ```
---

## Session « routage, MLA et formats » (01/10 22 h → 02/10) — ce qui était faux, et ce qui bloque encore

### Les portes, revérifiées

| porte | valeur | état |
|---|---|---|
| Qwen2.5-0.5B Q8_0 ctx 256 (dense) | **19,3885** | inchangée |
| Qwen3-30B en clusters ctx 64, 8 jetons | **799,8557** | inchangée |
| gpt-oss-120b MXFP4 ctx 256 | **15,6017** | **changée** (15,1757 avant) — voir ci-dessous |
| `cargo test --release` | **48** | 41 avant |
| `tools/portes_formats.sh` | **17 formats × 2 blocs** | tous exacts contre libggml |

**Pourquoi gpt-oss a changé.** Le moteur mettait le biais du routeur dans le
=== cherche baseline ===
docs/format-clusters.md:78:## Mesures (Qwen3-30B-A3B-Instruct Q4_K_M, 18,56 Go, 48 couches, 128 experts)
docs/format-clusters.md:84:| le modèle entier | 0,9 ms | **3 906,4 ms** | **18,56 Go** |
  ```

### 🤖 Assistant

⏵ Reading the clusters measurement table for the whole-model baseline

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk 'NR>=78 && NR<=105{printf \"%d: %s\\n\", NR, $0}' docs/format-clusters.md", "description": "Read clusters measurements"}`

  ```
78: ## Mesures (Qwen3-30B-A3B-Instruct Q4_K_M, 18,56 Go, 48 couches, 128 experts)
79: 
80: | fichier | en-tête (mmap) | lecture totale | octets |
81: |---|---|---|---|
82: | `commun.gguf` | 1,4 ms | 201,6 ms | 1,00 Go |
83: | `cluster-00.gguf` | 1,8 ms | 423,3 ms | 2,20 Go |
84: | le modèle entier | 0,9 ms | **3 906,4 ms** | **18,56 Go** |
85: 
86: Un nœud qui sert le cluster 0 charge **3,20 Go au lieu de 18,56 (5,8× moins)** et
87: **625 ms au lieu de 3,9 s (6,2× plus vite)**. Avec huit nœuds, chacun ne lit que
88: son cluster ; le surcoût est la duplication des métadonnées (8 × ~4 Mo, soit
89: 0,2 % du modèle).
90: 
91: ## Conversion
92: 
93: ```bash
94: # trace de routage (facultative mais recommandée : elle ordonne les experts)
95: DRAVE_TRACE_EXPERTS=/tmp/routage.txt ./drave-core/target/release/drave <modele.gguf> \
96:     --ppl <ids.txt> --ctx 2048 --limit 2048 --lot 64 --threads 16
97: 
98: # conversion : un cluster = 16 experts ; --mode couches pour un modèle dense
99: python3 tools/convertir_clusters.py <modele.gguf> <dossier> \
100:     --clusters 8 --trace /tmp/routage.txt --verifier
101: ```
102: 
103: `--mode couches` découpe un modèle **dense** en groupes de couches 
… [183 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"3 906,4\\|3906,4\\|799\" reports/rapport-grappes.md | head -10; echo \"=== rapport-grappes head ===\"; head -40 reports/rapport-grappes.md", "description": "Check grappes report"}`

  ```
=== rapport-grappes head ===
# Drave — grappes afférentes/efférentes et découpage en sous-modèles

Modèle : MLP 32→64→10, structure **imposée à l'entraînement**
(masque à 4 grappes + une fraction d'arêtes inter-grappes).

## Coût de la structure imposée

| Couplage | Accuracy | Non-nuls | Densité | Arêtes hors grappe | Écart moyen | Positions (b/poids) |
|---|---|---|---|---|---|---|
| 0.0 % | 74.12 % | 346 | 12.9 % | 0.0 % | 2.40 | 0.39 |
| 1.0 % | 73.34 % | 346 | 12.9 % | 2.7 % | 3.26 | 0.39 |
| 5.0 % | 74.02 % | 373 | 13.9 % | 12.0 % | 4.14 | 0.69 |
| 20.0 % | 75.78 % | 459 | 17.1 % | 35.9 % | 6.69 | 0.85 |
| 100.0 % | 76.07 % | 708 | 26.3 % | 75.0 % | 3.43 | 0.79 |

**Comparaison à budget égal** (346 non-nuls) :

- modèle en grappes pures : **74.12 %**
- meilleur modèle dense de même budget (32→7→10, 311 paramètres) : **74.12 %**

## Trafic ring (découpage en 4 sous-modèles, 7B type)

**Ce qui traverse le ring, ce sont les activations, pas les poids** (ceux-ci
restent résidents sur leur carte).

| Couplage | Activations traversantes | Ko/token | µs sur le ring |
|---|---|---|---|
| 0.0 % | 0.0 % | 0.0 | 0.0 |
| 1.0 % | 27.7 % | 72.5 | 15.1 |
| 5.0 % | 37.0 % | 97.1 | 20.2 |
| 2
… [295 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading REPRISE §2 gate table for a 30B baseline statement

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk 'NR>=60 && NR<=98{printf \"%d: %s\\n\", NR, substr($0,1,200)}' REPRISE.md", "description": "Read REPRISE section 2 gates"}`

  ```
60: drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf \
61:     --tokenize --fichier /tmp/wt2_txt.txt --sortie /tmp/ids_qwen.txt
62: drave-core/target/release/drave /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf \
63:     --tokenize --fichier /tmp/wt2_txt.txt --sortie /tmp/ids_oss.txt
64: ```
65: 
66: Le mode `--tokenize --fichier` **vérifie la réversibilité** (texte reconstruit
67: identique à la source) — les deux tokenizers la passent sur ce corpus.
68: 
69: | modèle | commande (abrégée) | perplexité attendue |
70: |---|---|---|
71: | Qwen2.5-0.5B Q8_0 | `--dense --limit 512` | **19,3885** |
72: | Qwen2.5-0.5B Q4_0 | `--q4 --limit 512` | **21,0110** |
73: | Qwen2.5-0.5B Q8_0, 6 bits | `--dense --bits-attn 6 --bits-ffn 6 --limit 512` (ctx 256) | **19,5633** ← bat l'int8 (19,8059), mais de moins loin qu'annoncé : la valeur **19,3045** qui figurait ici n'
74: | Qwen2.5-0.5B Q8_0, 4 bits | `--dense --q4 --limit 512` | **23,1323** |
75: | Qwen2.5-1.5B Q4_K_M | `--q4 --limit 256` | **12,9228** |
76: | Qwen2.5-VL-7B Q4_K_M | défaut, `--limit 128` | **10,9947** |
77: | Qwen3-30B-A3B MoE | `--dense --limit 128` | **7,6139** |
78: | gpt-oss-120b MXFP4 | 
… [1435 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"799,8557\" journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md | head -8", "description": "Search journal for the 30B baseline"}`

  ```
3576:| Qwen3-30B en clusters | **799,8557** (inchangée) |
  ```

### 🤖 Assistant

⏵ Running bash -n on portes.sh and checking vision headings

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash -n tools/portes.sh && echo \"bash -n: OK\" ; command -v shellcheck >/dev/null && shellcheck -S warning tools/portes.sh | head -30 || echo \"(shellcheck absent)\"; echo \"=== vision headings ===\"; grep -n \"^## \" docs/vision.md … [68 caractères tronqués]`

  ```
bash -n: OK
(shellcheck absent)
=== vision headings ===
21:## 1. Le cœur : des listes, pas des matrices
62:## 2. Axe 1 — Voir et régler le modèle, neurone par neurone
106:## 3. Axe 2 — Répartir sur les composants d'une machine
134:## 4. Axe 3 — Répartir sur plusieurs machines
176:## 5. Axe 4 — Rejouer, comparer, ne pas régresser
198:## 6. Axe 5 — Formats, matériels, énergie
230:## 7. Ce que la vision n'est pas
248:## 8. Feuille de route par axes
260:## 9. Le nom
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"axes 3-4\\|axe 3\\|§2\\|§3-§4\" docs/vision.md docs/comparaison-spiking.md docs/format-clusters.md docs/colab-reparti.md docs/format-flux.md docs/plan-mode4-lot-listes.md docs/plan-gpu-topk.md | head -20", "description": "V … [31 caractères tronqués]`

  ```
docs/vision.md:239:* **ce n'est pas « distribuer, c'est gratuit »** : l'axe 3 est **engagé** (le
docs/comparaison-spiking.md:8:machines** (`docs/vision.md`, axes 3-4) et **lire ces flux pour adapter
docs/comparaison-spiking.md:9:l'architecture à la tâche** (§2) restent les deux dimensions structurantes. Le
docs/format-clusters.md:10:(`docs/vision.md`, axe 3). Le découpage n'est donc pas qu'un rangement de
docs/colab-reparti.md:9:transport n'est pas le seul enjeu (`docs/vision.md` §2).
docs/format-flux.md:14:   et c'est la finalité du projet (`docs/vision.md` §2).
docs/plan-mode4-lot-listes.md:22:(`docs/vision.md` §2).
docs/plan-mode4-lot-listes.md:33:| où est l'échelle ? | **une par état, dans l'état** (§2) | la dynamique d'un résidu change à chaque jeton ; un tableau partagé ferait dépendre les états l'un de l'autre |
docs/plan-mode4-lot-listes.md:122:sont conservées telles quelles (§2).
  ```

### 🤖 Assistant

⏵ Checking that the top-k attention path also honours the learned sinks

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fn attn_topk\\|attn_topk(\" drave-core/src/model.rs | head -10; echo \"=== sinks near topk ===\"; awk 'NR>=4700 && NR<=4900 && /sink|puits/{printf \"%d: %s\\n\", NR, $0}' drave-core/src/model.rs | head -20", "description":  … [33 caractères tronqués]`

  ```
=== sinks near topk ===
  ```

### 🤖 Assistant

⏵ Locating the top-k attention implementation and its sink handling

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"attn_topk\" drave-core/src/model.rs | head -20", "description": "Grep attn_topk in model.rs"}`

  ```
1484:    pub attn_topk: usize,
2611:            act_topk_proj: [0; 7], attn_topk: 0, attn_events: 0, qk_topk: 0,
3257:        if self.attn_topk > 0 && t > 1 && !LOT_TOPK_IGNORE.swap(true, std::sync::atomic::Ordering::Relaxed) {
3259:l'attention par lots est DENSE. Utiliser --lot 1 pour l'attention creuse.", self.attn_topk);
3457:                let groupe = fen == 0 && self.attn_topk == 0 && rep > 1;
4238:                let groupe = fen == 0 && self.attn_topk == 0 && rep > 1;
4309:                // Le miroir VRAM était interdit dès que `attn_topk > 0` : la
4330:                let topk_gpu_possible = self.attn_topk > 0 && self.attn_topk.min(n) <= 1024
4335:                    let k = self.attn_topk.min(n);
4350:                                ok = machine.attn_topk_tout(m, nh, n, k, hd, rep, puits.as_deref(),
4366:                            ok = machine.attn_topk_histo(m, nh, n, dec, &pref, &mut hist);
4380:                            ok = machine.attn_topk_collecte(m, nh, n, k, &pref, &besoin, &mut sel);
4391:                            ok = machine.attn_topk_somme(m, nh, n, k, hd, rep, puits.as_deref(),
4437:                    let k = if self.attn_topk > 0 { self.attn_topk.mi
… [18 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking whether removing the sinks test left an unused closure or a warning

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk 'NR>=87 && NR<=150' drave-core/src/model.rs | grep -n \"a(\" ; echo \"=== deny warnings? ===\"; grep -rn \"deny(warnings)\\|#!\\[deny\\|#!\\[warn\" drave-core/src/main.rs drave-core/src/lib.rs 2>/dev/null | head; ls drave-core/sr … [61 caractères tronqués]`

  ```
=== deny warnings? ===
clusters.rs
engine.rs
formats.rs
gguf.rs
gpu.rs
list.rs
main.rs
materiel.rs
model.rs
tokenizer.rs
  ```

### 🤖 Assistant

⏵ Printing manques_architecture to confirm the closure is now dead

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "offset": 87, "limit": 60}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
87: pub fn manques_architecture(g: &Gguf, cfg: &Cfg, ctx: usize, clusters: bool) -> Vec<&'static str> {
88:     // Le test porte sur TOUTES les couches, pas sur la couche 0 : GLM-5.3 a
89:     // trois couches denses puis des couches MLA, et regarder la première
90:     // laissait passer le modèle jusqu'au panic « attn_q absent » de la couche 3.
91:     let quelque_part = |suffixe: &str| g.tensors.iter().any(|t| t.name.ends_with(suffixe));
92:     let a = |n: &str| g.tensor(n).is_some();
93:     let mut manques: Vec<&str> = Vec::new();
94:     if quelque_part("hc_attn_fn.weight") || quelque_part("hc_ffn_fn.weight") {
95:         manques.push("hyper-connexions (hc_attn_fn, hc_ffn_fn, hc_mult)");
96:     }
97:     // Attention par index (DSA) : l'indexeur choisit les clés gardées. Il ne
98:     // sert QUE si la séquence dépasse `index_topk` — en deçà, llama.cpp garde
99:     // toutes les clés et l'indexeur n'est pas appelé. On refuse donc seulement
100:     // les contextes où il changerait le résultat.
101:     if quelque_part("indexer.") {
102:         let topk = g.cf
… [2984 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Confirming which model.rs wording predates the diff

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show HEAD:drave-core/src/model.rs | awk 'NR>=112 && NR<=140{printf \"%d: %s\\n\", NR, $0}'", "description": "Show HEAD version of the MLA comment"}`

  ```
112:         || g.cfg("engram.layer_ids").is_some() || g.json_brut("engram_layer_ids").is_some() {
113:         // informatif seulement : voir `--sonder-engram`
114:     }
115:     if quelque_part("attn_output_a.weight") {
116:         manques.push("projection de sortie à rang faible groupée (attn_output_a/attn_output_b, o_groups)");
117:     }
118:     // DeepSeek-V4 : l'attention n'est pas la MLA « simple » de GLM/Kimi.
119:     // `attn_derope` renvoie la sortie d'attention dans le repère non tourné,
120:     // les sinks sont des logits appris par tête, et surtout `compress_ratios`
121:     // fait cohabiter TROIS attentions dans le même modèle : compressée à
122:     // candidats (CSA/LID), compressée simple (HCA) et brute. Les implémenter à
123:     // moitié donnerait des nombres faux sans rien casser — c'est exactement ce
124:     // que ce contrôle doit empêcher.
125:     if quelque_part("attn_derope") || a("blk.0.attn_sinks.weight") {
126:         manques.push("attention V4 : dé-rotation de sortie et puits par tête");
127:     }
128:     if g.cfg("compress_ratios").is_some() || g.json_brut("compress_ratios").is_some() {
129:         manques.push("attentions compressées CS
… [712 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Final checks: dead closure impact, +3,0 % trace source, and diff scope

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- drave-core/src/model.rs | grep -n \"^[+-].*seuil_push\" ; echo \"=== 1,2 Mo +3,0% ===\"; grep -rn \"1,2 Mo\\|+3,0 %\\|3,0 %\" reports/rapport-programme-evolutif.md | head -8; echo \"=== report exists ===\"; wc -l reports/ … [97 caractères tronqués]`

  ```
50:+        // (`seuil_push = 0.22`, `reports/rapport-croisement-push-pull.md`).
=== 1,2 Mo +3,0% ===
17:| Capteur de co-activation branché sur une projection | **+3,0 %** (96,75 s → 99,64 s sur 1 025 tokens) |
19:| Journal des activations de toutes les couches (24) | ~1,2 Mo/token, soit 19 Mo/s à 15,8 tok/s |
23:les *listes d'activations* suffit à rejouer intégralement le calcul. 1,2 Mo/token
118:1. **Journaliser** pendant l'inférence (+3,0 %).
=== report exists ===
138 reports/rapport-programme-evolutif.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"calculable\" reports/*.md docs/*.md REPRISE.md README.md | grep -i \"NON\\|refus\" | head -15", "description": "Find stale calculable-NON statements"}`

  ```
reports/rapport-coherence-vision.md:83:   « **calculable : NON — il manque : attention V4…** » pour un modèle dont la
reports/rapport-coherence-vision.md:86:   gpt-oss → « calculable : oui » ; V4.1 → « calculable : NON — il manque :
reports/rapport-mla-experts.md:96:- **Kimi-K2.7 (1 026 G poids)** : `--config` annonce « calculable : oui »,
  ```

### 🤖 Assistant

⏵ Broadening the reference check to all path-like tokens in added lines

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -U0 | grep '^+' | grep -v '^+++' | grep -oE '[A-Za-z0-9_][A-Za-z0-9_./-]*\\.(md|rs|py|sh|json|txt|c|h|cu|ptx|tsv)' | sed 's/^[`(]*//' | sort -u | while read -r f; do\n  case \"$f\" in\n    main.rs|model.rs|gguf.rs|lib.rs|gpu … [343 caractères tronqués]`

  ```
MISSING: api-docs.deepseek.c
MISSING: deepseek.c
MISSING: llama.c
MISSING: plan-deepseek41-complet.md
MISSING: sessions/8b6d46ab-6ad0-4648-92a8-0bec40a02526/rapport.md
MISSING: sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md
MISSING: tmp/ids_oss_512.txt
MISSING: tmp/wt2_txt.txt
MISSING: vision.md
MISSING: www.deepseek.c
--- done ---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for d in colab FPGA-Stratix-V docs reports tools journal; do [ -e \"$d\" ] && echo \"DIR OK: $d\" || echo \"DIR MISSING: $d\"; done; ls tools/ | grep -E \"proxy_latence|convertir_clusters|analyse_hc|verifier_formats|extraire_tables\" … [56 caractères tronqués]`

  ```
DIR OK: colab
DIR MISSING: FPGA-Stratix-V
DIR OK: docs
DIR OK: reports
DIR OK: tools
DIR OK: journal
convertir_clusters.py
extraire_tables_ggml.c
extraire_tables_ggml.sh
proxy_latence.py
verifier_formats.py
  ```

### 🤖 Assistant

⏵ Checking the FPGA sibling path and finishing evidence collection

- **bash** `{"command": "ls /home/stephane/Data13TB/stephane/GitHub/ | head -20; echo \"=== FPGA ===\"; find /home/stephane/Data13TB/stephane/GitHub -maxdepth 1 -iname \"*FPGA*\" 2>/dev/null; echo \"=== pre-existing? ===\"; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -U0 -- docs/vision.md | g … [137 caractères tronqués]`

  ```
915-SPO (1).com
915-SPO.com
915-SPO.com-2
Ai_Docs
arduino-i2c-scanner
Arduino-IRremote
ArduinoNunchuk
Biblio
Biblio-2
blue-pill-quickstart
bohemian-lab
copilotage
copilotage-shared
DeDRM_tools
emails
equipement-kindle
equipment-cam-IP-PTZ
equipment-dvr-coax
equipment-hauru
equipment-kamaji
=== FPGA ===
/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V
=== pre-existing? ===
FPGA-Stratix NOT in diff (pre-existing)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 15,1667 / 15,0757 / 18,5803 lines ===\"; grep -n \"15,1667\\|15,0757\\|18,5803\" REPRISE.md | head -10", "description": "Locate remaining stale gpt-oss values"}`

  ```
=== 15,1667 / 15,0757 / 18,5803 lines ===
45:> encore 15,1757, 15,1667, 15,0757 ou 18,5803 datent d'AVANT ce correctif : à
49:> changements) : gpt-oss avec `DRAVE_GPU=1` donne **15,1667**, la valeur attendue
80:| gpt-oss-120b MXFP4 | `--ppl-texte`, `--limit 512` (mêmes jetons) | **15,0757** (509 jetons) |
81:| gpt-oss-120b MXFP4 | `--dense --ctx 512 --limit 512`, ids_oss | **18,5803** (511 jetons, une fenêtre) |
191:| porte gpt-oss selon l'ouverture du pilote | sans `DRAVE_GPU` : **15,1757** · avec `DRAVE_GPU=1` : **15,1667** — l'écart vient du déport automatique des projections Q8_0 (> 8 Mo), pas d'une régression |
280:0,06 % (15,1757 → 15,1667 sur gpt-oss).
679:#    chiffre devient 15,1667 (même calcul, ordre de sommation du noyau GPU).
  ```

### 🤖 Assistant

⏵ Final reference checks before writing the report

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/docs/rapport-pe-evenementiel.md 2>&1 | head -2; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^### P6\\|^### P7\\|^### P2\" docs/plan-deepseek41-complet.md | head", "description": "Check FPGA link target and … [15 caractères tronqués]`

  ```
-rw-------. 1 stephane stephane 7517 26 sep 08:10 /home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/docs/rapport-pe-evenementiel.md
136:### P2 — Épilogue d'attention : puits, dé-rotation, sortie groupée (≈ 3 h)
188:### P6 — V4-Flash complet, en listes, et **sur plusieurs grappes** (≈ 1 journée)
204:### P7 — Adaptation à V4.1, et la question de provenance (≈ ½ journée + action externe)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Q4_1\\|Q5_1\" README.md | head; echo \"=== README enumeration lines ===\"; awk 'NR>=346 && NR<=356{printf \"%d: %s\\n\", NR, $0}' README.md", "description": "Read README format enumeration"}`

  ```
352:Le moteur lit **Q4_K, Q6_K, Q4_0, Q5_0, Q5_1, Q8_0, Q2_K, Q3_K, Q5_K, MXFP4,
368:**18 formats lisibles, 17 vérifiés à la porte** : `Q5_1` est lu par la même
=== README enumeration lines ===
346: > corriger a tout empiré). Détail dans le rapport.
347: 
348: ---
349: 
350: ## Formats et modèles réellement lisibles
351: 
352: Le moteur lit **Q4_K, Q6_K, Q4_0, Q5_0, Q5_1, Q8_0, Q2_K, Q3_K, Q5_K, MXFP4,
353: IQ1_S, IQ1_M, IQ2_XXS, IQ3_XXS, IQ4_XS, BF16, F16 et F32** — soit tout ce que
354: l'écosystème public distribue — **sans copie ni requantification** : les blocs
355: sont lus tels quels dans le fichier, et les experts d'un MoE sont des tranches
356: contiguës adressées par un pointeur et un pas. Les formats de super-bloc sans
  ```

### 🤖 Assistant

⏵ Checking the MLA path for sink handling before finalizing

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fn attn_mla\" drave-core/src/model.rs; grep -n \"sinks\" drave-core/src/model.rs", "description": "Locate MLA path and all sinks uses"}`

  ```
3793:    fn attn_mla(m: &Mla, cache: &mut (Vec<f32>, Vec<f32>), hn: &[f32], pos: usize,
125:    // Les puits par tête (`attn_sinks.weight`), eux, SONT implémentés : gpt-oss
857:    pub sinks: Option<Vec<f32>>,
1494:    /// clés, plus `attn_sinks` jetons puits au début de la séquence.
1523:    pub attn_sinks: usize,
1544:    pub sinks_vus: usize,
2325:                sinks: if g.tensor(&p("attn_sinks.weight")).is_some() {
2326:                    Some(g.dequant(&p("attn_sinks.weight"))) } else { None },
2386:        let sinks_vus = layers.iter().filter(|l| l.sinks.is_some()).count();
2417:        println!("[config] puits appris sur {sinks_vus}/{n_layer} couches · n_rot {} · ffn {} · experts {}{}",
2628:            attn_sinks: if fenetre > 0 { 0 } else { 4 },
2635:            sinks_vus, kv_gpu, attn_gpu_part: Vec::new(),
3464:                    let puits: Option<Vec<f32>> = lay.sinks.as_ref()
3497:                            let puits = lay.sinks.as_ref().map(|s| s[hh]);
3526:                    let puits = lay.sinks.as_ref().map(|s| s[hh]);
4247:                    let puits: Option<Vec<f32>> = lay.sinks.as_ref()
4280:                            let puits = lay.sinks.as_ref().map(|
… [408 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Testing whether any park model mixes the MLA path with learned sinks

- **bash** `{"command": "for f in /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4.1-Flash-Q2/DeepSeek-V4.1-Flash-Q2.gguf /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00002-of-00003.gguf /home/stephane/Data13TB/stephane/modeles/gguf/GLM-5.3-UD-IQ1_ … [477 caractères tronqués]`

  ```
### DeepSeek-V4.1-Flash-Q2.gguf
  attn_kv_a_mqa: 0
  attn_q_a: 80
  attn_sinks: 40
  attn_derope: 0
### DeepSeek-V4-Flash-UD-IQ1_M-00002-of-00003.gguf
  attn_kv_a_mqa: 0
  attn_q_a: 52
  attn_sinks: 26
  attn_derope: 0
### GLM-5.3-UD-IQ1_S-00001-of-00006.gguf
  attn_kv_a_mqa: 0
  attn_q_a: 0
  attn_sinks: 0
  attn_derope: 0
  ```

### 🤖 Assistant

⏵ Verifying MLA-path selection vs sinks across the remaining shards

- **bash** `{"command": "for f in /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/*.gguf /home/stephane/Data13TB/stephane/modeles/gguf/Kimi-K2.7-Code-UD-IQ1_M/Kimi-K2.7-Code-UD-IQ1_M-00002-of-00008.gguf /home/stephane/Data13TB/stephane/modeles/gguf/GLM-5.3-UD-IQ1_S/GLM-5.3-UD-IQ1_S-0000 … [257 caractères tronqués]`

  ```
DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf  mla=0 sinks=0
DeepSeek-V4-Flash-UD-IQ1_M-00002-of-00003.gguf  mla=0 sinks=26
DeepSeek-V4-Flash-UD-IQ1_M-00003-of-00003.gguf  mla=0 sinks=17
Kimi-K2.7-Code-UD-IQ1_M-00002-of-00008.gguf  mla=11 sinks=0
GLM-5.3-UD-IQ1_S-00002-of-00006.gguf  mla=21 sinks=0
  ```

### 🤖 Assistant

⏵ Collecting exact line numbers for the report

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"format-clusters.md:176\" docs/convertisseur.md; grep -n \"les deux valeurs restent\" docs/plan-gpu-topk.md; grep -n \"dé-rotation + puits\" docs/plan-modeles-lourds.md; grep -n \"puits par tête\" docs/plan-deepseek41-comple … [285 caractères tronqués]`

  ```
175:| 7 | mmap (appel système direct) | ✅ **fait** | grosses pages, partage entre processus (`docs/format-clusters.md:176`) |
101:| 6 | porte de non-régression : les deux valeurs restent 19,3885 et 15,6017 | ✅ **inchangées**, mesurées sur le binaire final : Qwen 19,3885 (CPU **et** avec `DRAVE_GPU_KV`) · gpt-oss 15,6017 (CPU) — 15,1757 était la valeur d'avant la correction du biais de routage du 02/10, voir `reports/rapport-routage-experts.md` |
91:| DeepSeek-V4 / V4-Flash | `deepseek4` (43 couches, 256 experts top-6, 1 M ctx) ; V4.1-Flash : `deepseek41` (40 couches, 384 experts top-6) | lecture des métadonnées et du tokenizer ✅ ; **lecteur multi-shards** ✅ ; MoE 128/top-8 ; attention MLA à rang faible **validée contre llama.cpp** (0,999024 sur GLM-5.3) | le forward `deepseek4`/`deepseek41` : hyper-connexions, sortie à rang faible, dé-rotation + puits, attentions compressées CSA/HCA |
138:- Dé-rotation (`attn_derope`), puits par tête (`attn_sinks`), sortie groupée
35:| **MiniMax-H3** | famille différente (vision+langage) | 22,8 Go au total (2 × 11,42 Go, Q4_K) | — | ✅ arrivé |
45:   sans changer un chiffre (Qwen3-30B : **799,8557**, identique à l'original).
118:    echo "  (portes 
… [29 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Writing the adversarial verification report

Findings are complete. Here is the report.

---

# Rapport de vérification adversariale — campagne de cohérence documentaire (02/10)

**Périmètre** : diff non commité au 02/10 10:10 EDT, `HEAD = 5a6ac96`, empreinte du diff revu : `md5 f8fe1dd324fa3b8819ff6eeada793ad1` (23 fichiers suivis + 1 rapport non suivi). ⚠️ **L'arbre a été modifié pendant la relecture** (le diff est passé de 21 à 23 fichiers entre 10:04 et 10:10 : `README.md`, `tools/analyse_flux.py`, et deux hunks de plus dans `model.rs` sur `seuil_push`). Les numéros de ligne ci-dessous sont ceux de cet instantané — le ficher `reports/rapport-coherence-vision.md` (non suivi) est apparu pendant la session.

**Méthode** : `git diff` intégral, lecture des rapports cités, scan des 28 en-têtes GGUF (32 Mo chacun) pour `attn_sinks`/`attn_derope`, `--config` (en-tête seul, jamais de forward ni de `--ppl`), `bash -n`, parsing GGUF direct en Python. Aucun fichier du dépôt n'a été modifié.

## 1. Faits de référence — vérifiés

| fait | verdict | preuve |
|---|---|---|
| `VERSION_FLUX = 5`, modes 0–4, en-tête 79 o | ✅ | `main.rs:1862`, `1864-1886`, `TAILLE_TETE` somme à 79, test `assert_eq!(TAILLE_TETE, 79)` en `main.rs:4629` |
| Qwen2.5-0.5B Q8_0 ctx 256 = 19,3885 | ✅ | `portes.sh:43`, `REPRISE.md:71` |
| Qwen3-30B clusters ctx 64 limit 8 = 799,8557 | ✅ | `portes.sh:50`, `rapport-routage-experts.md:65` (avant/après identiques) |
| gpt-oss ctx 256 = 15,6017 (était 15,1757) | ✅ | `rapport-routage-experts.md:66` (« 15,1757 était auto-cohérent, pas juste ») |
| `cargo test --release` = 48 | ✅ | 48 `#[test]` comptés dans `drave-core/src/*.rs` ; `portes.sh:37` |
| 17 formats vérifiés à la porte | ✅ | `portes_formats.sh:27-45` = 17 entrées × 2 blocs |
| 18 formats lisibles | ⚠️ | **19 types ont un chemin de lecture** (`row_f32`/`dequant`) : voir ligne 12 du tableau |
| MLA : 0,999024, +4,070 à la position 3 | ✅ | `rapport-mla-experts.md:112,178` ; le §7 existe bien |
| YaRN : bascule à `* 4.0` (16 384 pour gpt-oss) | ✅ | `model.rs:2203` ; `original_context_length = 4096` (parsé dans le GGUF) |
| KV int8 +1,5 % (512) / +3,0 % (8192) ; int4 +219 % / +364 % | ✅ | `contexte-long.md:145,152` |
| préremplissage 17,1→13,6 s ; ≈50→34,4 s | ✅ | `rapport-prefill-par-lots.md:124-127,193-194` |
| densité 17,9 % à seuil 5 % ; croisement 22 %, `seuil_push = 0.22` | ✅ | `rapport-localite-activation.md:43`, `rapport-croisement-push-pull.md:48`, `model.rs:2629` |
| `Gguf::open_multi` + 1 328 tenseurs / 86,90 Go | ✅ | `gguf.rs:447`, `rapport-lecteur-multifichiers.md:37-39` |

**Tous les renvois de fichiers cités existent** (40 backticks + liens testés un par un ; seul `FPGA-Stratix-V` est hors dépôt, cf. §4).

## 2. Corrections fausses ou incomplètes

| fichier:ligne | citation exacte (≤ 25 mots) | problème | correction minimale | gravité |
|---|---|---|---|---|
| `drave-core/src/model.rs:126` | « en a et sa porte tourne (`--config` affiche « puits appris sur 36/36 ») » | **Faux** : `--config` ne charge pas le modèle (`main.rs:1642` « sans le charger ») et n'imprime aucune ligne `[config]`. Vérifié en exécutant `--config` sur gpt-oss : pas de ligne « puits ». Elle vient du chargement (`model.rs:2417`). | remplacer `` (`--config` affiche « puits appris sur 36/36 ») `` par `` (`--config` répond « calculable : oui » ; le chargement affiche « puits appris sur 36/36 ») `` | **moyenne** |
| `drave-core/src/model.rs:92` | « let a = \|n: &str\| g.tensor(n).is_some(); » | Closure **morte** : son seul appel (`a("blk.0.attn_sinks.weight")`) a été supprimé par ce diff. `cargo build` émettra `warning: unused variable: a` (pas d'erreur : aucun `deny(warnings)`). | supprimer la ligne 92 | faible |
| `drave-core/src/model.rs:137-139` | « elle n'a jamais été validée contre une référence sur cette machine » | Contredit le message que ce même bloc imprime maintenant (l. 141-143 : « Validée contre llama.cpp sur GLM-5.3 à la POSITION 0 »). Contradiction déjà présente dans HEAD, mais le diff a réécrit la phrase juste en dessous sans toucher ce commentaire. | remplacer par « elle est validée à la position 0 (GLM-5.3), l'écart croît ensuite — » | **moyenne** |
| `REPRISE.md:114` | « RoPE simple tant que `--ctx` tient dans `rope.scaling.original_context_length` (4 096), **interpolation YaRN seule au-delà** » | **Politique périmée** d'un facteur 4. Le code bascule à `4 ×` (`model.rs:2203`), le même fichier a été corrigé ailleurs (l. 166, ~275, ~684) ; §3 est la table « ce qui est implémenté ». | remplacer par « RoPE simple tant que `--ctx` ne dépasse pas **4 ×** `rope.scaling.original_context_length` (16 384 pour gpt-oss), **interpolation YaRN seule au-delà** » | **haute** |
| `docs/programme-recherche.md:47` | « Ces trois propriétés ne sont pas des opinions : elles sont mesurées » | Le diff a fait passer l'annonce à « **quatre** propriétés » (l. 24) et ajouté un 4ᵉ item ; la phrase de clôture dit encore « trois ». | remplacer « Ces trois propriétés » par « Ces quatre propriétés » | moyenne |
| `docs/plan-mla-vision.md:89-90` | « où l'écart à llama.cpp atteint 4,07 nats au jeton 7 » | Faux : le rapport place **+4,070 à la position 3** (table positions 0–6, `rapport-mla-experts.md:178`), et `model.rs:143` dit « position 3 ». « 7 » est le nombre de jetons notés. | remplacer « au jeton 7 » par « à la position 3 » | **moyenne** |
| `docs/convertisseur.md:175` | « partage entre processus (`docs/format-clusters.md:176`) » | Le renvoi était juste contre HEAD, mais **ce même diff a inséré 5 lignes** en tête de `format-clusters.md` : la ligne 176 est devenue « déjà un expert absent… » ; le mmap est en **181**. | remplacer `docs/format-clusters.md:176` par `docs/format-clusters.md:181` | moyenne |
| `docs/vision.md:53` | « (`REPRISE.md` §3, `DRAVE_FLUX_VERIF=1`) » | Les valeurs citées (19,4029 ; 1,5e-5) sont en **§6** (`REPRISE.md:265-266`) ; §3 « Ce qui est implémenté et vérifié » ne les contient pas. | remplacer « §3 » par « §6 » | faible |
| `docs/vision.md:120` | « `reports/rapport-session-2026-09-30.md`, `REPRISE.md` §5. » | Les lignes du tableau (15,6→6,2 ; +6 % ; 0,03 vs 25,77 Go) sont en **§6** (`REPRISE.md:186-195,221`) ; §5 = « Règles de méthode ». Le rapport de session, index de la journée, ne porte aucun de ces chiffres. | remplacer par « `reports/rapport-session-2026-09-30.md` (index), `REPRISE.md` §6. » | faible |
| `README.md:368` | « **18 formats lisibles, 17 vérifiés à la porte** : `Q5_1` est lu par la même branche que `Q5_0` » | **`Q4_1` est aussi lisible et non vérifié** : `gguf.rs:1363` (`row_f32`), `:1629` (`dequant`), table des tailles `:734` (type 3) ; la batterie de 17 types ne contient ni 3 ni 7. Donc **19 lisibles, 2 non vérifiés** (un modèle mixte Q4_0/Q4_1 existe, `rapport-inference.md:328`). | remplacer par « **19 formats lisibles, 17 vérifiés à la porte** : `Q4_1` et `Q5_1` sont lus par les mêmes branches que leurs voisins `Q4_0`/`Q5_0` » | moyenne |
| `docs/plan-deepseek41-complet.md:70` | « IQ2_XXS, Q2_K, Q8_0, F16, F32, **I8** (engram) — déquantificateurs **vérifiés contre libggml** » | Le passage I32→**I8** est **juste** (j'ai parsé les deux copies : `I8` ×2, `I32` ×0). Mais `I8` n'a **aucun bras** dans `row_f32`/`dequant` et n'est pas dans `portes_formats.sh` : il est inventorié/adressé, pas déquantifié ni vérifié à la porte. | remplacer par « IQ2_XXS, Q2_K, Q8_0, F16, F32, **I8** (engram, adressé — pas de déquantificateur) — les autres **vérifiés contre libggml** » | faible |
| `docs/plan-modeles-lourds.md:91` et `docs/plan-deepseek41-complet.md:138` | « dé-rotation + puits, attentions compressées CSA/HCA » / « Dé-rotation (`attn_derope`), puits par tête (`attn_sinks`), sortie groupée » | Contredit le correctif du même diff : les puits **sont** implémentés et appliqués (chemins décodage, groupé, GPU, top-k), et `--config` sur V4-Flash/V4.1 ne les liste plus comme manquants. **Aucun** fichier du parc n'a `attn_derope`. | remplacer « dé-rotation + puits » par « dé-rotation ; puits par tête : implémentés, à brancher sur le chemin V4 » ; et « puits par tête (`attn_sinks`) » par « puits par tête (`attn_sinks`, implémentés — à brancher ici) » | faible |
| `docs/plan-gpu-topk.md:101` | « les deux valeurs restent 19,3885 et 15,6017 \| ✅ **inchangées**, mesurées sur le binaire final » | La même ligne reconnaît que 15,1757 est la valeur d'avant le correctif : la porte gpt-oss a donc **changé**. « inchangées » est faux pour l'une des deux. | remplacer « ✅ **inchangées**, mesurées sur le binaire final : Qwen 19,3885 … » par « ✅ **vertes** : Qwen 19,3885 (CPU **et** avec `DRAVE_GPU_KV`) · gpt-oss 15,6017 (CPU, valeur post-correctif ; 15,1757 datait d'avant la correction du biais de routage du 02/10, voir `reports/rapport-routage-experts.md`) » | faible |
| `docs/comparaison-spiking.md:8` | « (`docs/vision.md`, axes 3-4) » | Le routage « entre composants et machines » = **Axe 2 (§3) + Axe 3 (§4)** ; « axes 3-4 » désigne machines + rejeu. `vision.md` titre « Axe 2 » en §3 et « Axe 3 » en §4. | remplacer « axes 3-4 » par « axes 2-3 » | faible |
| `docs/plan-modeles-lourds.md:35` | « 22,8 Go au total (2 × 11,42 Go, Q4_K) » | Les deux fichiers font 11,42 et **11,38** Go (total 22,80 ✅). | remplacer par « (2 × 11,42 et 11,38 Go, Q4_K) » | cosmétique |
| `docs/convertisseur.md:113` | « le renommage du 30/09 est « fait partout » (`docs/histoire.md`) » | La citation entre guillemets n'existe pas telle quelle ; `histoire.md:4,31` dit « changé de nom, partout » / « Changé, partout ». | remplacer « est « fait partout » » par « a été fait « partout » » | cosmétique |
| `tools/portes.sh:118` | « echo "  (portes de formats : voir section 5)" » | En mode normal, la section 5 **a déjà tourné** (et affiché) ; en mode `rapide`, cette ligne est sautée (mais la section 5 dit elle-même qu'elle est ignorée). Message au mieux redondant. | supprimer la ligne 118 | cosmétique |

## 3. `tools/portes.sh` — section 7 : correcte

`bash -n` passe. La logique est saine : `v=$($D "$O" --config … | grep -oE "calculable +: .*")` capte bien la sortie réelle (`main.rs:1687` imprime « calculable    : oui (passe avant implémentée) ») et le `case *": oui"*` matche ; sinon `v` est vide et `ECHEC=1`. `compare` et `valeur` sont inchangés et corrects — `valeur` filtre sur `=== perplexité`, motif que seule la ligne **totale** porte (`main.rs:4586`) ; les fenêtres s'écrivent « perplexité cumulée » (`main.rs:4517`), donc plus de piège 17,431. La commande de perplexité est identique à la recette de `REPRISE.md:681`. Régénération des identifiants : `--tokenize --fichier --sortie` écrit des ids séparés par des virgules, ce que le lecteur `--ppl` accepte (`split(',' | whitespace)`) ; `head -c 20000 data/wikitext2_test.txt` tombe sur une frontière UTF-8 valide (vérifié) et le fichier a bien ≥ 512 jetons. `timeout 2400` > 20 min annoncées. **Aucun défaut de logique trouvé** (seule la ligne 118 est cosmétique).

## 4. Déjà cohérent, ne pas toucher

- **`docs/format-flux.md`** : 4 fonctions, mode 4 (1,5 ko/jeton, critère ≤ 1,5 × à 256 jetons = 1,15 ×, 5,6 × à 20 jetons) — tout est dans `rapport-mode4-lot-listes.md:35-53`.
- **`docs/contexte-long.md`** : E1/E2/E3 exacts (219 % à 512 = table « par bloc de 32 » l. 145 ; 364 % à 8 192 = §4.bis.2) ; §5.ter/§5.quater existent et §5.quater énonce bien la bascule à 4 × ; l'avertissement du §6 est cohérent avec `plan-gpu-topk.md`.
- **`docs/roadmap.md`** : « Six phases » = Phase 0…5 (6 sections) ; v5 ; clés f16 + valeurs int4 = +0,61 % à 33 % exactement comme `rapport-placement-bits-kv.md:23`.
- **`docs/sprints.md`**, **`docs/colab-reparti.md`** (l'en-tête v4 faisait déjà 79 o, donc « 3 663 octets, en-tête v5 compris » reste juste), **`docs/format-clusters.md`** (axe 3 correct), **`docs/plan-prefill-reparti.md`** (79 o/v5), **`docs/plan-deepseek-v4-flash.md`** (`open_multi`, 1 328 tenseurs/86,90 Go, `hc_mult=4` déclaré et `output_hc_*` absents — vérifié par parsing des deux copies), **`docs/plan-mode4-lot-listes.md`** (`envoyer_lot_listes` en `main.rs:2216`, refus du mode inconnu avant le corps en `main.rs:2271-2275`), **`journal/README.md`** (le dossier `sessions/8b6d46ab-…` existe), **`tools/analyse_flux.py`** (22 %).
- **`REPRISE.md`** : le nouveau bloc du 02/10 est exact (19,3885 / 799,8557 / 15,6017 / 48 / v5 modes 0–4) et l'avertissement sur les anciennes valeurs gpt-oss est honnête — **sauf** la ligne 114 (§2, ligne 4 du tableau ci-dessus).
- **`docs/programme-recherche.md`** : les 4 items sont mesurés (`rapport-programme-evolutif.md:17-19` pour 1,2 Mo/jeton et +3,0 %) — **sauf** « Ces trois » (ligne 5 du tableau) et « identique à l'original » (ci-dessous).

## 5. Réponse à la question 4 (`attn_sinks` / `attn_derope`)

- `sinks` **est bien utilisé** dans le calcul : chargé en `model.rs:2325-2326`, puis ajouté au dénominateur du softmax dans le chemin décodage groupé (l. 3494-3498), par tête (l. 3523-3529), GPU (l. 3461-3473) et top-k CPU/GPU (l. 4277-4281, 4338, 4350, 4391, 4450, 4507). Le correctif ne casse rien.
- **Scan des 28 en-têtes GGUF** (32 Mo chacun) : `attn_sinks` présent dans **gpt-oss-120b** (36), **DeepSeek-V4.1-Flash-Q2** (40, les deux copies), **DeepSeek-V4-Flash** (26+17 = 43 ; le shard 1 n'a aucun tenseur) ; **0 partout ailleurs**. `attn_derope` : **0 dans tous les fichiers**.
- **Aucun verdict de calculabilité ne bascule à tort** : `--config` (binaire post-correctif, construit à 10:02, logique identique à l'arbre actuel) donne gpt-oss **oui**, V4-Flash et V4.1 **NON** (hyper-connexions, sortie à rang faible, `compress_ratios`) ; GLM-5.3, Kimi-K2.7 et Qwen3-235B **oui**.
- ⚠️ **Risque latent** (pas un bug aujourd'hui) : aucun modèle du parc ne combine `attn_kv_a_mqa` (qui sélectionne le chemin MLA, `model.rs:2231`) **et** `attn_sinks`. Or `attn_mla` (`model.rs:3793`) n'utilise jamais `lay.sinks` : un tel modèle dirait maintenant « calculable : oui » et calculerait sans ses puits. L'ancien test (`a("blk.0.attn_sinks.weight")`) refusait ce cas — avec un message faux. Le correctif étroit serait de ne signaler `attn_sinks` que lorsque `attn_kv_a_mqa` est présent.

## 6. Points à trancher par l'humain

1. **REPRISE.md:114** (§3) : à corriger (ligne 4 du tableau) ou à marquer comme historique — c'est la doc de reprise, la contradiction avec le code y est la plus coûteuse.
2. **« 19 formats lisibles »** : faut-il corriger le compte (README §2, `REPRISE.md:1120`, `plan-deepseek41-complet.md:201`), ou ajouter `Q4_1` à `portes_formats.sh` (ce qui redonnerait 18/18) ?
3. **`docs/programme-recherche.md:45`** : « (Qwen3-30B : 799,8557, **identique à l'original**) ». Aucun rapport ne mesure le modèle 30B **non découpé** à ctx 64 / limit 8 ; on ne documente que l'artefact 8 clusters égal à lui-même (mmap, correctif de routage). Soit citer la mesure d'origine, soit écrire « la porte en clusters reproduit 799,8557 ». — *affirmation à confirmer avant publication*.
4. **Puits vs chemin MLA** : garder la suppression sèche du test `attn_sinks` (assumé : aucun modèle concerné) ou le restreindre au chemin MLA (cf. §5) ?
5. **Valeurs gpt-oss périmées** : `REPRISE.md:80-81` (15,0757 ; 18,5803) restent dans la table « Références de non-régression » sans marqueur en ligne (l'avertissement est 35 lignes plus haut). À re-mesurer (elles devraient bouger du même ordre que 15,1757 → 15,6017) ou à annoter.
6. **Lien préexistant cassé** (hors diff) : `docs/vision.md:125` pointe `../FPGA-Stratix-V/docs/rapport-pe-evenementiel.md` — depuis `docs/`, il faudrait `../../FPGA-Stratix-V/…` ; le fichier existe bien à côté du dépôt.

- **send_message** `{"agent_id": "bbd6969f-0f70-42b2-8951-64d1f2f36d2e", "message": "RAPPORT DE VÉRIFICATION ADVERSARIALE — campagne cohérence docs (02/10). Diff revu : md5 f8fe1dd324fa3b8819ff6eeada793ad1, HEAD 5a6ac96, instantané 10:10 EDT. ⚠️ L'arbre a changé pendant la relecture (21→23 fichiers ; README.md, tools/a … [6544 caractères tronqués]`

  ```
message delivered to agent bbd6969f-0f70-42b2-8951-64d1f2f36d2e
  ```

### 🤖 Assistant

Le rapport complet est ci-dessus et a été transmis au parent (`bbd6969f…`) sous forme autonome. Résumé en trois lignes, sans flatterie :

- **14 corrections problématiques** documentées avec citation exacte, correctif textuel et gravité, dont **une haute** : `REPRISE.md:114` affirme encore la politique YaRN périmée (bascule à 1× la longueur déclarée) que le moteur n'applique plus (4×, `model.rs:2203`) et que le reste du même fichier a été mis à jour.
- **Le correctif `model.rs` est fonctionnellement sain** : `sinks` est bien consommé dans tous les chemins d'attention, aucun modèle du parc ne combine chemin MLA et `attn_sinks`, et `--config` donne gpt-oss = oui / V4-Flash et V4.1 = NON pour d'autres raisons. Deux résidus : une closure morte (l. 92) et un commentaire (l. 137-139) qui dit le contraire du message réécrit juste en dessous ; plus une affirmation fausse sur `--config` (l. 126).
- **`tools/portes.sh` section 7 : rien à redire** sur le fond (`bash -n` OK, `valeur`/`compare` cohérents, commande identique à la recette) — seule la ligne 118 est cosmétique.

Les six points à trancher (dont « 19 ou 18 formats lisibles » et l'affirmation « identique à l'original » non mesurée) sont en fin de rapport.

