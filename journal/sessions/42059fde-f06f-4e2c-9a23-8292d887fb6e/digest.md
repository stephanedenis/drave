# Session DSH — relecture

- identifiant : `42059fde-f06f-4e2c-9a23-8292d887fb6e`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-09-30 12:20:44
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu es vérificateur de documentation dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM en Rust, `std` seul, binaire `drave`). Tout est en FRANÇAIS : écris en français.

MISSION : traquer les **contradictions entre les documents et l'état réel du code**, et les **chiffres périmés**. Ce dépôt se veut rigoureux : chaque affirmation est censée être mesurée, et une affirmation fausse y est un défaut de premier ordre (la session qui vient de finir a dû corriger DEUX fois de suite le même chiffre dans ses propres rapports).

CE QU'IL FAUT FAIRE :
1. Inventorie les documents de référence : `README.md`, `REPRISE.md`, `docs/*.md` (surtout `format-flux.md`, `roadmap.md`, `vision.md`, `contexte-long.md`, `histoire.md`, `colab-reparti.md`, `plan-prefill-reparti.md`) et `reports/*.md`. Le dossier `journal/` est un journal automatique : IGNORE-LE.
2. Cherche les incohérences de FAIT, par exemple :
   - des versions de protocole ou de format annoncées (v1/v2/v3/v4) qui ne correspondent plus au code (`VERSION_FLUX` dans `drave-core/src/main.rs`, la version écrite par `TraceFlux::nouveau` dans `model.rs`) ;
   - des tailles d'en-tête, des dispositions de champs, des noms de modes (dense/listes/blocs/lot) divergents entre documents ;
   - des chiffres clés cités à plusieurs endroits avec des valeurs différentes (perplexités de référence, octets par flux, octets par neurone actif, tailles de trace, accélérations) ;
   - des variables d'environnement ou des drapeaux documentés qui n'existent plus (ou l'inverse : un drapeau du code absent de la documentation) ;
   - des chemins de fichiers qui n'existent pas, ou des renvois vers des documents inexistants ;
   - des affirmations « vérifié » qui contredisent un autre document.
   Pour chaque chiffre ou nom, va voir le code ou le rapport d'origine (`grep`) plutôt que de comparer les documents entre eux.
3. Vérifie en particulier que les documents récents disent la même chose que les rapports qu'ils citent : `docs/format-flux.md` vs `reports/rapport-transport-liste.md` vs `reports/rapport-compacite-trace.md` vs `reports/rapport-phase3-reparti.md`, et que `REPRISE.md` §6bis (écrit il y a une heure) n'est pas déjà périmé par les commits suivants.

LIVRABLE : `reports/rapport-coherence-docs.md`, en français, avec un tableau `| document | affirmation | ce que dit le code/la mesure | verdict |` — verdicts : PÉRIMÉ (chiffre faux), CONTRADICTOIRE (deux documents s'opposent), MANQUANT (le code a une chose que les docs ignorent), OK. Termine par la liste ordonnée des corrections à faire (les 10 plus importantes), et NE LES APPLIQUE PAS : un autre agent s'en chargera.

INTERDIT : modifier un autre fichier que `reports/rapport-coherence-docs.md`. Pas de `cargo build`. Les exécutions du moteur sont autorisées si elles sont courtes (`--limit 4`) et sans serveur (`--flux-serveur`/`--ppl-reparti` interdits).
Termine ta réponse par un résumé de 10 lignes : nombre d'affirmations vérifiées, nombre de problèmes par verdict, et les trois corrections les plus urgentes.
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

⏵ Inventaire du dépôt et des documents de référence

Je commence par explorer la structure du dépôt.

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet", "description": "Lister la racine du dépôt"}`

  ```
total 208
drwxr-xr-x. 1 stephane stephane   598 30 sep 12:19 .
drwxr-xr-x. 1 stephane stephane  2350 25 sep 11:55 ..
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane    52 25 sep 17:53 data
drwxr-xr-x. 1 stephane stephane   394 30 sep 11:53 docs
drwxr-xr-x. 1 stephane stephane    82 28 sep 11:58 drave-core
drwxr-xr-x. 1 stephane stephane   146 30 sep 12:20 .git
-rw-r--r--. 1 stephane stephane   399 30 sep 10:01 .gitignore
drwxr-xr-x. 1 stephane stephane    34 27 sep 11:39 journal
drwxr-xr-x. 1 stephane stephane    88 25 sep 17:13 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-------. 1 stephane stephane 26646 30 sep 08:44 README.md
drwxr-xr-x. 1 stephane stephane  1686 30 sep 11:59 reports
-rw-------. 1 stephane stephane 28339 30 sep 11:39 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 stephane stephane 10507 30 sep 08:44 run_clusters.py
-rw-------. 1 stephane stephane 12507 30 sep 08:44 run_cpu.py
-rw-------. 1 stephane stephane 11462 30
… [619 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -20 && echo \"---\" && git status --short | head -30", "description": "Voir l'historique git récent"}`

  ```
a0687b9 Colab : notebook prêt à ouvrir + script de préparation
25c42c3 Deux silences de plus, relevés par l'audit : trace en inférence, modes concurrents
6b3b53f DRVF v2 sur le disque : −49,87 % de trace, rejeu identique
d59d061 Protocole v4 : les top-k voyagent aussi (défaut n°1 de l'audit)
7522289 Plomberie : huit drapeaux qui ne faisaient rien, d'après l'audit délégué
cda3162 Phase 3.4 : préremplissage par LOTS sur le fil — écart 0,00e0
2184fc5 Banc réparti : plus de flux pour le dernier jeton
1cf4714 REPRISE et journal : la formule de latence et la validation à 1 024 jetons
e80ceb1 Phase 3.3 : le coût du découpage en fonction de la latence, mesuré
af18f29 Transport en listes à 1 024 jetons : ÷2,3 pour 1,3 % d'écart
86ddf12 Le CODE de l'encodage par écarts, oublié dans le commit précédent
3ae3f45 Découpage fidèle à 1 024 jetons : 0,00e0 sur 1 024 flux
f4bce59 tools/pair_factice.py : les trois modes, et plusieurs clients
9fe0c80 Feuille de route : les cinq mesures de la session au journal
cb37c83 Transport : indices par écarts — 3 623 → 1 568 octets par flux, à quantification identique
976cb81 Transport : l'écart DÉCROÎT avec la longueur (la courbe le dit, pas moi)
4396f25 REPRIS
… [348 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la docs/ && echo \"=== REPORTS ===\" && ls -lat reports/ | head -60", "description": "Lister docs et reports"}`

  ```
total 200
drwxr-xr-x. 1 stephane stephane   394 30 sep 11:53 .
drwxr-xr-x. 1 stephane stephane   598 30 sep 12:19 ..
-rw-r--r--. 1 stephane stephane  5948 30 sep 12:20 colab-reparti.md
-rw-------. 1 stephane stephane  8505 30 sep 08:44 comparaison-spiking.md
-rw-------. 1 stephane stephane 28812 30 sep 08:44 contexte-long.md
-rw-------. 1 stephane stephane 16030 28 sep 11:57 convertisseur.md
-rw-r--r--. 1 stephane stephane  7957 30 sep 12:17 format-flux.md
-rw-------. 1 stephane stephane  4359 30 sep 08:45 histoire.md
-rw-------. 1 stephane stephane 38716 30 sep 08:44 plan-mla-vision.md
-rw-------. 1 stephane stephane 22668 30 sep 11:53 plan-prefill-reparti.md
-rw-------. 1 stephane stephane 11951 27 sep 16:09 programme-recherche.md
-rw-------. 1 stephane stephane 20255 30 sep 12:02 roadmap.md
-rw-------. 1 stephane stephane   108 30 sep 10:34 .roadmap.md.kate-swp
-rw-------. 1 stephane stephane 12615 30 sep 08:45 vision.md
=== REPORTS ===
total 296
drwxr-xr-x. 1 stephane stephane   598 30 sep 12:19 ..
-rw-------. 1 stephane stephane 14969 30 sep 12:17 rapport-compacite-trace.md
-rw-------. 1 stephane stephane 20218 30 sep 12:11 rapport-drapeaux-ignores.md
drwxr-xr-x. 1 stephane st
… [2585 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la drave-core/src/ && echo \"=== tools ===\" && ls tools/ && echo \"=== colab ===\" && ls colab/", "description": "Lister le code source"}`

  ```
total 560
drwxr-xr-x. 1 stephane stephane    112 30 sep 11:13 .
drwxr-xr-x. 1 stephane stephane     82 28 sep 11:58 ..
-rw-r--r--. 1 stephane stephane  45442 29 sep 13:49 engine.rs
-rw-------. 1 stephane stephane  33061 29 sep 19:27 gguf.rs
-rw-r--r--. 1 stephane stephane  39060 30 sep 08:44 gpu.rs
-rw-------. 1 stephane stephane  67760 29 sep 07:30 list.rs
-rw-r--r--. 1 stephane stephane 157973 30 sep 12:18 main.rs
-rw-r--r--. 1 stephane stephane 194294 30 sep 12:12 model.rs
-rw-------. 1 stephane stephane  20019 28 sep 14:34 tokenizer.rs
=== tools ===
aiguille.py
analyse_flux.py
archive_sessions.py
compare_logits.py
diff_flux.py
flux_codec.py
harmony_canonique.py
make_patch.py
mla_synthetique.py
pair_factice.py
preparer_colab.sh
profil_flux.py
proxy_latence.py
__pycache__
ref_logits
ref_logits.cpp
ref_logits.md
session_report.py
trace_compacite.py
vision_mtmd.py
vision_ref.py
=== colab ===
Drave-reparti.ipynb
README.md
  ```

- **grep** `{"pattern": "VERSION_FLUX|VERSION_|DRVF|v1|v2|v3|v4", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs"}`

  ```
Found 5 matches

drave-core/src/main.rs
Line 1295: const VERSION_FLUX: u8 = 3;
Line 1484:     tete.push(VERSION_FLUX);
Line 1518:     tete.push(VERSION_FLUX);
Line 1559:     if version != VERSION_FLUX {
Line 1562:             format!("flux en version {version}, cette build parle la {VERSION_FLUX} \
  ```

- **grep** `{"pattern": "Fn nouveau|fn nouveau|TraceFlux|DRVF", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs"}`

  ```
Found 13 matches

drave-core/src/model.rs
Line 411:     pub fn nouveau(budget: usize) -> Self {
Line 493: pub struct TraceFlux {
Line 502: impl TraceFlux {
Line 503:     pub fn nouveau(chemin: &str, couches: Vec<usize>, hidden: usize, n_layer: usize)
Line 507:         f.write_all(b"DRVF")?;
Line 514:         Ok(TraceFlux { fichier: f, couches, octets: 14, enregistrements: 0, actifs: 0 })
Line 529:         // **Indices par écarts** (DRVF v2) : la liste est triée, donc l'écart au
Line 559: /// enregistrée. C'est le pendant du `TraceFlux` : ce qu'un nœud distant devrait
Line 578:         if &entete[0..4] != b"DRVF" {
Line 580:                                            "ce n'est pas une trace DRVF"));
Line 585:                 format!("trace DRVF en version {version} : ce lecteur lit la 1 et la 2")));
Line 760:     pub trace: Option<TraceFlux>,
Line 2626:     fn flux_lot(trace: &mut Option<TraceFlux>, force: &mut Option<FluxRelecteur>,
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "offset": 1270, "limit": 140}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "offset": 490, "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1270:     // et ils voyagent dans l'en-tête pour que les deux nœuds fassent pareil.
1271:     mdl.act_topk_proj = opt.topk_proj;
1272:     mdl.attn_topk = opt.attn_topk;
1273:     mdl.qk_topk = opt.qk_topk;
1274:     mdl.moe_topk = opt.moe_topk;
1275: }
1276: 
1277: /// ---- Phase 3 : le flux passe d'un nœud à l'autre ----------------------------
1278: ///
1279: /// Cadriciel : `u32` magie, `u32` plage (debut, fin), `u32` position, `u32`
1280: /// dimension, puis les activations en f32. C'est le même contenu que le format
1281: /// de trace, réduit à ce qu'un nœud a besoin de recevoir pour continuer.
1282: const MAGIE_FLUX: u32 = 0x4452_5631;   // "DRV1"
1283: /// Version du protocole de flux. Elle est dans CHAQUE en-tête : un pair d'une
1284: /// autre version est refusé avec un message qui dit laquelle il parle, plutôt
1285: /// que de laisser lire des octets qui ne veulent pas dire la même chose.
1286: /// Version 4 : le bloc de réglages transporte AUSSI les top-k (par projection,
1287: /// attention, q·k, MoE). En version 3, deux nœuds lancés avec des `--topk-*`
1288:
… [6300 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
490: /// neurones actifs — indice, valeur — avec son échelle. C'est le cœur de la
491: /// vision mis sur disque : on peut rejouer, comparer, et c'est aussi le format
492: /// qu'un nœud distant devrait recevoir pour continuer le calcul.
493: pub struct TraceFlux {
494:     pub fichier: std::io::BufWriter<std::fs::File>,
495:     /// Couches à tracer (toutes si vide).
496:     pub couches: Vec<usize>,
497:     pub octets: u64,
498:     pub enregistrements: u64,
499:     pub actifs: u64,
500: }
501: 
502: impl TraceFlux {
503:     pub fn nouveau(chemin: &str, couches: Vec<usize>, hidden: usize, n_layer: usize)
504:         -> std::io::Result<Self> {
505:         use std::io::Write;
506:         let mut f = std::io::BufWriter::new(std::fs::File::create(chemin)?);
507:         f.write_all(b"DRVF")?;
508:         // Version 2 : les indices sont écrits par ÉCARTS (voir `ecrire`).
509:         f.write_all(&2u16.to_le_bytes())?;
510:         f.write_all(&(n_layer as u32).to_le_bytes())?;
511:         f.write_all(&(hidden as u32).to_le_bytes())?;
512:         // 14 octets d'en-t
… [5333 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 140, "offset": 1450}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-flux.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1450:         let mut prev = 0u32;
1451:         for (&i, &v) in idx.iter().zip(val.iter()) {
1452:             let ecart = i as u32 - prev;
1453:             if ecart < 255 {
1454:                 paires.push(ecart as u8);
1455:             } else {
1456:                 paires.push(255);
1457:                 paires.extend_from_slice(&i.to_le_bytes());
1458:             }
1459:             prev = i as u32;
1460:             paires.push(v as u8);
1461:         }
1462:         // La longueur est écrite : avec les échappements, elle n'est pas
1463:         // déductible du nombre de paires, et un décodeur qui la suppose lit
1464:         // hors du tampon.
1465:         c.extend_from_slice(&(paires.len() as u32).to_le_bytes());
1466:         c.extend_from_slice(&paires);
1467:         (idx.len(), 0f32, c)
1468:     } else if mode == MODE_LISTE {
1469:         let (idx, val, ech) = mdl.expect("modèle requis pour quantifier un flux")
1470:                                  .flux_en_liste(actifs);
1471:         let mut c = Vec::with_capacity(idx.len() * 4);
1472:         for (
… [6389 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-flux.md</path>
<type>file</type>
<content>
1: # Le format de flux (DRVF v1) — spécification
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
20:           version      u16          = 1
21:           n_couches    u32
22:           cachés       u32
23: liste     couche       u16          < 1000 : entrée d'attention
24:                                     >= 1000 : entrée de FFN (couche - 1000)
25:           jeton        u32          COMPTEUR GLOBAL de jeton, pas la position
26:     
… [7278 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-transport-liste.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-compacite-trace.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-transport-liste.md</path>
<type>file</type>
<content>
1: # Phase 3.2 — transporter la LISTE au lieu du vecteur
2: 
3: **En une ligne** : le flux peut voyager en liste creuse (871 octets au lieu de
4: 3 623), mais à seuil 5 % le découpage coûte **×1,8 de perplexité** — la courbe
5: est là, avec le seuil où ça casse.
6: 
7: ## Le protocole, mesuré
8: 
9: Deux modes dans le même en-tête de 39 octets — magie, version, mode, plage,
10: position, dimension, échelle, **et les réglages d'activation** :
11: 
12: | mode | contenu | octets par flux (Qwen2.5-0.5B, 896 canaux) |
13: |---|---|---|
14: | 0 · dense f32 | `896 × f32` | **3 623** (39 + 3 584) |
15: | 1 · listes | `n × (indice u16 · valeur i16)` | 39 + 4 × actifs |
16: 
17: Le mode 1 est le format du disque, à l'octet près. La réponse est encodée comme
18: la demande : un pair qui parle en listes reçoit des listes.
19: 
20: ## La courbe (40 jetons, 12 couches de chaque côté)
21: 
22: | seuil | activité | octets/flux (aller) | octets/flux (retour) | perplexité locale | perplexité répartie | écart |
23: |---|---|---|---|---|---|---|
24: | dense f32 | 100 % | 3 623 | 
… [11783 caractères tronqués]
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
13: > Restent à faire, tels quels : les valeurs i8 à échelle par bloc (−60,9 %), les
14: > échelles f16 (−63,5 %) et l'emballage zstd (−79 %).
15: 
16: **En une ligne** : la trace DRVF v1 coûte **6,04 octets par neurone actif** quand
17: le transport en coûte ~2 ; les **i
… [14649 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-phase3-reparti.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-analyse-flux.md"}`

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
… [2437 caractères tronqués]
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

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md</path>
<type>file</type>
<content>
1: # Reprise — état du projet et mode d'emploi pour une nouvelle session
2: 
3: > Rédigé à la fin d'une session longue. Tout ce qui suit est **mesuré**, pas
4: > déduit. Les valeurs de perplexité sont des **références de non-régression** :
5: > si une modification les change, c'est qu'elle a changé le calcul.
6: >
7: > **Nom** : le projet s'appelle **Drave** (binaire `drave`, paquet `drave-core`,
8: > variables `DRAVE_*`, histoire du renommage dans `docs/histoire.md`). Le dossier
9: > de travail, lui, s'appelle encore `Qtrinet` — les chemins ci-dessous sont ceux
10: > qui existent.
11: 
12: ---
13: 
14: ## 1. En une phrase
15: 
16: `drave-core` est un moteur d'inférence Rust (~5 000 lignes, `std` seul) qui
17: charge les GGUF **en place** (aucune copie, aucune requantification), exécute les
18: projections soit en listes d'événements, soit en produit scalaire dense, gère les
19: MoE, tient une conversation, et déporte au GPU ce qui y gagne. Il fait tourner du
20: 0,5 B au 120 B sur le CPU de cette machine.
21: 
22: ```bash
23: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-
… [28191 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -oE '\"--[a-z0-9-]+\"' drave-core/src/main.rs | sort -u | tr '\\n' ' '", "description": "Extraire les drapeaux CLI du code"}`

  ```
"--abits" "--act-renorm" "--act-thresh" "--act-topk" "--attn-sinks" "--attn-topk" "--attn-window" "--auto" "--banc-kv" "--banc-mla" "--banc-vision" "--bits" "--bits-attn" "--bits-ffn" "--chat" "--couches-locales" "--ctx" "--dense" "--depuis" "--ffn-gain" "--fichier" "--flux" "--flux-blocs" "--flux-forcer" "--flux-liste" "--flux-serveur" "--gpu-banc" "--harmony" "--harmony-assistant" "--harmony-contexte" "--harmony-suite" "--harmony-user" "--hebbian" "--hebb-out" "--hebb-q" "--hist" "--ids" "--ids-file" "--infer" "--keep" "--limit" "--logits-bin" "--lot" "--matrix" "--moe-topk" "--n" "--neurones-sortie" "--patch" "--pin" "--plan" "--ppl" "--ppl-profil" "--ppl-reparti" "--ppl-texte" "--profil-neurones" "--prompt" "--push" "--q4" "--q4-attn" "--q4-ffn" "--q4-tout" "--qk-topk" "--rep-penalty" "--sans-fenetre" "--sans-yarn" "--session" "--sortie" "--swa-pattern" "--temp" "--tensors" "--texte" "--threads" "--tokenize" "--topk" "--topk-down" "--topk-gate" "--topk-k" "--topk-o" "--topk-q" "--topk-up" "--topk-v" "--top-p" "--trace-couches" "--trace-flux"
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -oE 'DRAVE_[A-Z0-9_]+' drave-core/src/*.rs | sed 's/.*://' | sort -u | tr '\\n' ' '", "description": "Extraire les variables d'environnement du code"}`

  ```
DRAVE_BANC_KV_DEBUG DRAVE_BANC_KV_GPU_SEUL DRAVE_BANC_KV_GRAD DRAVE_BANC_KV_K0 DRAVE_BANC_KV_KUNIT DRAVE_BANC_KV_UNIT DRAVE_BANC_KV_V1 DRAVE_DEBUG_FLUX DRAVE_FLUX_VERIF DRAVE_GPU DRAVE_GPU_EXPERTS DRAVE_GPU_EXPERTS_GO DRAVE_GPU_KV DRAVE_GPU_TETE DRAVE_HARMONY_TRACE DRAVE_KV_BITS DRAVE_KV_F16 DRAVE_KV_K_F32 DRAVE_KV_V_F32 DRAVE_Q8_BLOCS DRAVE_SANS_EMPRUNT DRAVE_TRACE_BLOCS DRAVE_VISION_TEXTE DRAVE_YARN DRAVE_YARN_MSCALE DRAVE_YARN_NON DRAVE_YARN_RAMPE
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -ohE -- '--[a-z0-9-]{2,}' docs/*.md README.md REPRISE.md reports/*.md tools/*.md 2>/dev/null | sort | uniq -c | sort -rn | head -80", "description": "Recenser les drapeaux cités dans la documentation"}`

  ```
48 --threads
     48 --ctx
     34 --limit
     31 --dense
     31 --abits
     28 --ppl
     27 --infer
     21 --lot
     18 --release
     17 --attn-topk
     15 --ppl-reparti
     14 --ids
     14 --flux-serveur
     13 --plan
     13 --keep
     11 --q4
     11 --act-thresh
     10 --flux-blocs
      9 --tokenize
      9 --depuis
      8 --flux-forcer
      8 --ffn-gain
      8 --couches-locales
      8 --act-topk
      7 --tensors
      7 --ppl-texte
      7 --pin
      7 --patch
      7 --chat
      7 --attn-window
      6 --sans-yarn
      6 --rep-penalty
      6 --flux
      5 --trace-flux
      5 --temp
      5 --qk-topk
      5 --prompt
      5 --ppl-profil
      5 --moe-topk
      5 --hist
      5 --hebbian
      5 --bits
      5 --banc-vision
      5 --banc-kv
      4 --top-p
      4 --topk-q
      4 --sans-fenetre
      4 --hebb-q
      4 --hebb-out
      4 --fichier
      4 ----------
      3 --topk-gate
      3 --topk
      3 --sortie
      3 --session
      3 --q4-tout
      3 --q4-attn
      3 --push
      3 --profil-neurones
      3 --neurones-sortie
      3 --matrix
      3 --harmony
      3 --gpu-banc
      3 --flux-liste
      3 --banc-mla
      3 --auto
     
… [284 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in docs/*.md README.md REPRISE.md reports/*.md; do grep -oE -- '--[a-z0-9-]{2,}' \"$f\"; done | sort -u > /tmp/doc_flags.txt; grep -oE '\"--[a-z0-9-]+\"' drave-core/src/main.rs | tr -d '\"' | sort -u > /tmp/code_flags.txt; echo … [248 caractères tronqués]`

  ```
=== drapeaux dans docs absents du code ===
------
-------
--------
---------
----------
-----------------
--act-
--allow-requantize
--epochs
--flow
--flux-norme
--gpu
--gpu-kv
--journal
--options-actives
--options-strict
--out
--profil-experts
--release
--scale
--sources
--url
--xxx
=== drapeaux du code absents des docs ===
--n
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn -- '--flux-norme' docs/ README.md REPRISE.md reports/ | head -20", "description": "Chercher le drapeau flux-norme retiré"}`

  ```
reports/rapport-transport-liste.md:65:sur 16 bits redonne la perplexité exacte. Un drapeau `--flux-norme` a donc été
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn -- '--allow-requantize\\|--profil-experts\\|--options-strict\\|--options-actives\\|--journal' docs/ README.md REPRISE.md reports/ | head -30", "description": "Chercher autres drapeaux obsolètes"}`

  ```
docs/convertisseur.md:212:2. **`llama-quantize --allow-requantize … F16`** fabrique une référence des
docs/vision.md:69:| `--profil-experts` | quels experts sont choisis (MoE), et à quel point le routage est concentré |
reports/rapport-aiguille.md:39:* journal markdown (`--journal`) pour citer les chiffres sans les recopier.
reports/rapport-drapeaux-ignores.md:196:## 8. Recommandation : un tableau de bord `--options-actives`, et trois garde-fous
reports/rapport-drapeaux-ignores.md:198:**L'idée simple** : un drapeau `--options-actives` (et `--options-strict`) qui imprime, au
reports/rapport-drapeaux-ignores.md:211:comparaison finale `argv` ↔ registre. `--options-strict` transforme les manquants en erreur.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in README.md REPRISE.md docs/format-flux.md docs/roadmap.md docs/vision.md docs/contexte-long.md docs/histoire.md docs/colab-reparti.md docs/plan-prefill-reparti.md reports/rapport-drapeaux-ignores.md; do echo \"########## $f\" … [144 caractères tronqués]`

  ```
########## README.md
########## REPRISE.md
111:| **CUDA 13 : les symboles non versionnés du pilote échouent** (`cuMemAlloc` → erreur 201 alors que le contexte est courant) | utiliser partout les `_v2` |
145:| 1 | protocole de perplexité longue | **fait** | `--depuis N` note les mêmes jetons à contexte variable ; `--depuis 256 --ctx 256` redonne exactement la fenêtre 2 historique (21,565) |
179:| aiguille v2 (12 sondes) | **12/12 trouvées** : 1,5B 512/2048, 30B 2048, gpt-oss 4096, profondeurs 0,1/0,5/0,9 |
188:l'aiguille v2, le dépaquetage vectorisé du noyau d'attention, les experts MXFP4
262:**Le protocole de flux est en v2** (`docs/format-flux.md`) : en-tête de 39 octets
263:avec version, mode et **réglages d'activation** — deux nœuds réglés différemment
265:d'une autre version est refusé en le disant. `--flux-serveur` accepte
372:#    protocole sans charger de modèle et DIT ce qu'il reçoit (tailles, modes,
########## docs/format-flux.md
1:# Le format de flux (DRVF v1) — spécification
19:en-tête   "DRVF"                    4 octets
20:          version      u16          = 1
28:          puis n_actifs × ( indice u32 · valeur i16 )           [version 1]
29:          puis n_actifs × 
… [5666 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '3 623\\|3 663\\|3 604\\|3 622\\|1 568\\|1 589\\|2 268\\|2 793\\|2 159\\|2 203\\|1 778' docs/*.md README.md REPRISE.md reports/*.md | head -60", "description": "Comparer les octets par flux cités"}`

  ```
docs/colab-reparti.md:36:* **Débit** : 3 623 octets par flux en dense, 1 989 en listes à échelle par bloc
docs/plan-prefill-reparti.md:88:| un jeton, mode 0 | 39 + 4·hidden | 3 623 octets, 3 623 par jeton |
docs/roadmap.md:56:| 3.2 | **Granularité** : par couche, par bloc de canaux, par expert | 🔬 | livrés et mesurés : listes i16, **échelles par bloc de 32 canaux (valeurs i8)** et **indices par écarts** — `--flux-blocs --act-thresh 0.01` : **3 623 → 1 589 octets par flux (÷2,3) pour 1,3 % d'écart à 1 024 jetons** (2,7 % à 256, 13,7 % à 64) ; reste le cas MoE |
docs/roadmap.md:111:| 2026-09-30 | protocole de flux v2, deux processus, localhost | en-tête de 39 octets (version, mode, réglages d'activation) · dense f32 **3 623 octets/flux** · listes i16 2 159 · **blocs + indices par écarts 1 568 (÷2,3)** pour 2,7 % d'écart à 256 jetons de vrai texte |
docs/roadmap.md:243:| dense f32 | 3 623 | **0,00e0** |
docs/roadmap.md:244:| listes, seuil 0,00 | 3 622 | 2,6e-2 |
docs/roadmap.md:245:| listes, seuil 0,02 | 2 203 | 4,9e-2 |
docs/roadmap.md:250:**1 745 octets contre 2 159** pour la liste i16, et 14 % d'écart contre 16 % —
docs/roadmap.md:253:échappement) : 2 268 → **1 568 octets** à écart
… [2427 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '39 octets\\|26 octets\\|79 octets\\|20 d.en-tête\\|40 octets\\|39 d.en-tête\\|TAILLE_TETE' docs/*.md README.md REPRISE.md reports/*.md | head -40", "description": "Comparer les tailles d'en-tête citées"}`

  ```
docs/format-flux.md:66:en-tête (26 octets, identique à l'aller et au retour)
docs/format-flux.md:144:| l'en-tête fait exactement `TAILLE_TETE` octets | `assert_eq!` dans les deux émetteurs — un octet de trop décale tout le corps en silence et ne se voit qu'au flux suivant |
docs/plan-prefill-reparti.md:12:priorité : `envoyer_lot` écrit **40** octets d'en-tête pour un `TAILLE_TETE` de
docs/plan-prefill-reparti.md:20:| nouveau mode ou champ `t` ? | **mode 3** (`MODE_LOT`), pas de champ | le corps dense d'un lot est `t × hidden × 4` : `n` (offset 18) porte déjà le compte, l'en-tête reste **39 octets**, tous les offsets existants sont stables |
docs/plan-prefill-reparti.md:28:### 1.1 En-tête (39 octets, identique à l'aller et au retour)
docs/plan-prefill-reparti.md:78:* L'ordre de lecture compte : `recevoir_flux` lit les **39 octets** de l'en-tête
docs/plan-prefill-reparti.md:105:| `TAILLE_TETE` | 1251 | **inchangée** (39) |
docs/plan-prefill-reparti.md:140:Même contrat qu'`envoyer_flux` : construit l'en-tête de 39 octets (mode 3, `n = t`,
docs/plan-prefill-reparti.md:148:debug_assert_eq!(tete.len(), TAILLE_TETE, "en-tête de {} octets, il en faut {TAILLE_TETE}", tete.len());
docs/plan-
… [1564 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/colab-reparti.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-prefill-reparti.md", "limit": 120}`

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
… [5168 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-prefill-reparti.md</path>
<type>file</type>
<content>
1: # Plan — le préremplissage par lots sur le fil (phase 3.4)
2: 
3: **En une ligne** : aujourd'hui un flux = un jeton, donc un préremplissage de N
4: jetons paie N allers-retours ; on ajoute un **mode 3** qui transporte N états
5: dans **un seul** message, et le banc réparti doit rendre **0,00e0**.
6: 
7: Ce document est une spécification d'implémentation : chaque étape dit le fichier,
8: le point d'insertion et le critère de succès. Les numéros de ligne cités sont
9: ceux du commit `2184fc5` ; l'arbre de travail contient déjà une implémentation
10: partielle non commitée (`Model::emb_imposee_lot`, `MODE_LOT`, `envoyer_lot`) —
11: **la relire avant d'éditer**, elle bouge. Deux écarts connus à corriger en
12: priorité : `envoyer_lot` écrit **40** octets d'en-tête pour un `TAILLE_TETE` de
13: **39** (le dernier `tete.push(0)` décale tout le corps d'un octet, §2.3 et §6.2),
14: et `VERSION_FLUX` vaut encore **2** (§1.3).
15: 
16: ## 0. Décisions d'architecture (à ne pas rediscuter)
17: 
18: | question | décision | pourquoi |
19: |---|---|---|
20: | nouveau mode ou cha
… [5887 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --format='%h %ad %s' --date=format:'%m-%d %H:%M' -15", "description": "Voir les dates des commits récents"}`

  ```
a0687b9 09-30 12:20 Colab : notebook prêt à ouvrir + script de préparation
25c42c3 09-30 12:19 Deux silences de plus, relevés par l'audit : trace en inférence, modes concurrents
6b3b53f 09-30 12:17 DRVF v2 sur le disque : −49,87 % de trace, rejeu identique
d59d061 09-30 12:11 Protocole v4 : les top-k voyagent aussi (défaut n°1 de l'audit)
7522289 09-30 12:05 Plomberie : huit drapeaux qui ne faisaient rien, d'après l'audit délégué
cda3162 09-30 12:02 Phase 3.4 : préremplissage par LOTS sur le fil — écart 0,00e0
2184fc5 09-30 11:41 Banc réparti : plus de flux pour le dernier jeton
1cf4714 09-30 11:39 REPRISE et journal : la formule de latence et la validation à 1 024 jetons
e80ceb1 09-30 11:39 Phase 3.3 : le coût du découpage en fonction de la latence, mesuré
af18f29 09-30 11:37 Transport en listes à 1 024 jetons : ÷2,3 pour 1,3 % d'écart
86ddf12 09-30 11:34 Le CODE de l'encodage par écarts, oublié dans le commit précédent
3ae3f45 09-30 11:34 Découpage fidèle à 1 024 jetons : 0,00e0 sur 1 024 flux
f4bce59 09-30 11:30 tools/pair_factice.py : les trois modes, et plusieurs clients
9fe0c80 09-30 11:29 Feuille de route : les cinq mesures de la session au journal
cb37c83 09-30 11:29 Transp
… [84 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --format='%h %ad %s' --date=format:'%m-%d %H:%M' -3 -- docs/colab-reparti.md docs/format-flux.md REPRISE.md docs/roadmap.md", "description": "Voir la dernière modif des docs clés"}`

  ```
a0687b9 09-30 12:20 Colab : notebook prêt à ouvrir + script de préparation
6b3b53f 09-30 12:17 DRVF v2 sur le disque : −49,87 % de trace, rejeu identique
d59d061 09-30 12:11 Protocole v4 : les top-k voyagent aussi (défaut n°1 de l'audit)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'envoyer_lot\\|MODE_LOT\\|--lot\\|opt.lot\\|lot >' drave-core/src/main.rs | head -40", "description": "Vérifier l'usage du mode LOT"}`

  ```
493:            "--lot" => { o.lot = suivant(i).parse().unwrap(); 2 }
1312:const MODE_LOT: u8 = 3;
1512:fn envoyer_lot(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos0: u32,
1519:    tete.push(MODE_LOT);
1581:        MODE_LOT => {
1696:                if f.mode == MODE_LOT {
1717:                    if envoyer_lot(&mut sock, f.debut, f.fin, f.pos, &plat, t, &mdl).is_err() {
1764:    // `--lot T` : préremplissage par LOTS sur le fil. La référence locale est
1767:    let lot = opt.lot.max(1);
1785:    if lot > 1 {
1821:    if lot > 1 {
1833:            let o = envoyer_lot(&mut sock, couches_locales as u32, n_layer as u32,
1897:    if lot > 1 {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in REPRISE.md docs/roadmap.md docs/format-flux.md; do echo \"== $f\"; git log -1 --format='%h %ad %s' --date=format:'%m-%d %H:%M' -- $f; done", "description": "Dernière modification par fichier"}`

  ```
== REPRISE.md
1cf4714 09-30 11:39 REPRISE et journal : la formule de latence et la validation à 1 024 jetons
== docs/roadmap.md
cda3162 09-30 12:02 Phase 3.4 : préremplissage par LOTS sur le fil — écart 0,00e0
== docs/format-flux.md
6b3b53f 09-30 12:17 DRVF v2 sur le disque : −49,87 % de trace, rejeu identique
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -ohE '`[A-Za-z0-9_./-]+\\.(md|py|rs|sh|ipynb|cpp|toml|json|bin|txt|gguf|ptx|cu)`' README.md REPRISE.md docs/*.md reports/*.md | tr -d '`' | sort -u > /tmp/refs.txt; while read -r p; do case \"$p\" in /*) continue;; esac; if [ !  … [132 caractères tronqués]`

  ```
MANQUANT: bpe_np.py
MANQUANT: clip.cpp
MANQUANT: comparaison-spiking.md
MANQUANT: config.json
MANQUANT: flux_codec.py
MANQUANT: ggml/src/ggml-cpu/ops.cpp
MANQUANT: gpt-oss-120b-MXFP4.gguf
MANQUANT: gpt_oss/torch/model.py
MANQUANT: gpu/drave_gpu.cu
MANQUANT: gpu/qtrinet_gpu.cu
MANQUANT: gpu.rs
MANQUANT: llama.cpp
MANQUANT: main.rs
MANQUANT: mmproj-Qwen2.5-VL-7B-Instruct-f16.gguf
MANQUANT: Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf
MANQUANT: rapport-campagne-parcimonie.md
MANQUANT: rapport-cpu-aer.md
MANQUANT: rapport-croisement-push-pull.md
MANQUANT: rapport-localite-activation.md
MANQUANT: rapport-mur-memoire-4bits.md
MANQUANT: reports/rapport-lecteur-ddr3.md
MANQUANT: reports/rapport-pe-evenementiel.md
MANQUANT: reports/rapport-prefill-reparti.md
MANQUANT: src/engine.rs
MANQUANT: src/gguf.rs
MANQUANT: src/list.rs
MANQUANT: src/main.rs
MANQUANT: src/model.rs
MANQUANT: src/tokenizer.rs
MANQUANT: tools/mtmd/clip.cpp
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '356 694\\|356694\\|17,43\\|17\\.43\\|1958\\|1 958' README.md REPRISE.md docs/*.md reports/*.md | head -30", "description": "Traquer les chiffres 356694 / 17,43"}`

  ```
docs/format-flux.md:58:et le rejeu rejouait la mauvaise : perplexité **356 694** au lieu de 17,43. Le
docs/plan-prefill-reparti.md:255:   donné 356 694 de perplexité.
docs/roadmap.md:203:**356 694** au lieu de 17,43. La clé est maintenant `(couche, compteur de jeton
reports/rapport-compacite-trace.md:11:> silence avec une perplexité fausse (1958,72 au lieu de 19,3885).
reports/rapport-compacite-trace.md:206:  perplexité de **356 694** au lieu de 17,43 quand on y avait mis la position.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la reports/rapport-prefill-reparti.md docs/comparaison-spiking.md; echo \"---\"; grep -n 'comparaison-spiking\\|rapport-prefill-reparti' /tmp/refs.txt | cat -A | head", "description": "Vérifier les faux positifs de renvois"}`

  ```
-rw-------. 1 stephane stephane 8505 30 sep 08:44 docs/comparaison-spiking.md
---
5:comparaison-spiking.md$
9:docs/comparaison-spiking.md$
67:reports/rapport-prefill-reparti.md$
[stderr]
ls: cannot access 'reports/rapport-prefill-reparti.md': No such file or directory
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'rapport-prefill-reparti\\|comparaison-spiking' README.md REPRISE.md docs/*.md reports/*.md | head -20", "description": "Voir qui cite ces fichiers"}`

  ```
README.md:37:| **Comparaison Spiking (SpikeGPT / Spikformer / Spikingformer)** | ✅ → [`docs/comparaison-spiking.md`](docs/comparaison-spiking.md) |
docs/plan-prefill-reparti.md:346:| 7 | `reports/rapport-prefill-reparti.md`, `docs/format-flux.md` | chiffres mesurés, tableau du protocole v3 (mode 3) | les nombres du rapport sont ceux de l'étape 5, commande recopiée telle quelle |
docs/programme-recherche.md:57:Comparaison détaillée dans [`comparaison-spiking.md`](comparaison-spiking.md).
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | grep -i prefill | cat -A", "description": "Inspecter le nom exact du rapport prefill"}`

  ```
rapport-prefill-par-lots.md$
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for c in cda3162 d59d061 6b3b53f 25c42c3 a0687b9 7522289; do echo \"=== $c $(git log -1 --format=%s $c)\"; git show --stat --format='' $c | head -20; done", "description": "Fichiers touchés par les commits récents"}`

  ```
=== cda3162 Phase 3.4 : préremplissage par LOTS sur le fil — écart 0,00e0
 docs/format-flux.md                                |   24 +-
 docs/plan-prefill-reparti.md                       |  414 ++++
 docs/roadmap.md                                    |    2 +-
 drave-core/src/main.rs                             |  215 +-
 drave-core/src/model.rs                            |   35 +-
 .../15fd322f-7e9e-48c0-a970-f36335eb622a/digest.md | 1192 ++++++++++
 .../rapport.md                                     |  146 ++
 .../7d0d2578-0048-4998-8494-7d2daef56769/digest.md | 1270 +++++++++++
 .../rapport.md                                     |  110 +
 journal/sessions/MANIFEST.md                       |    7 +-
 .../bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md |  894 ++++++++
 .../rapport.md                                     |   88 +-
 .../c25f97d1-9a4d-41da-b983-004f793afe43/digest.md | 2297 ++++++++++++++++++++
 .../rapport.md                                     |  157 ++
 reports/rapport-compacite-trace.md                 |  242 +++
 reports/rapport-drapeaux-ignores.md                |  234 ++
 tools/trace_compacite.py                           |  432 ++++
 17 files changed, 7712 ins
… [2651 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md</path>
<type>file</type>
<content>
1: # Drave
2: 
3: *Anciennement `Drave`.* **La drave**, c'est le flux qu'on conduit : ici, celui
4: des **listes d'activation** (*stream of logs*) — le moteur ne lit pas des
5: matrices, il pousse des faits valués vers leurs destinations. La vision complète
6: est dans [`docs/vision.md`](docs/vision.md).
7: 
8: Origine du projet : inférence de LLM en **ternaire / multi-bits** sur un cluster
9: de cartes **Stratix V** (Microsoft Storey Peak) — 100 % logique, sans DSP.
10: Le cahier des charges d'origine est dans [`Qtrinet-bootstrap.md`](Qtrinet-bootstrap.md)
11: ⚠️ **il a été audité et corrigé** : voir la section « Écarts avec le CDC » ci-dessous.
12: Le nom du crate et du binaire (`drave-core`, variables `DRAVE_*`) changera dans un
13: commit dédié ; le journal de sessions, archivé, n'est pas réécrit.
14: 
15: ---
16: 
17: ## État du projet
18: 
19: | Étape | État |
20: |-------|------|
21: | Audit du cahier des charges | ✅ (corrections ci-dessous) |
22: | **Test de principe : quantification d'un modèle minimal** | ✅ **fait** → [`reports/rapport-minimal.md`](reports/rapport-minimal.md
… [26962 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/roadmap.md"}`

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
… [19779 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 2184fc5 --stat --format='%s' | head -10 && git show 2184fc5 -- drave-core/src/main.rs | head -60", "description": "Inspecter le commit du compteur de flux"}`

  ```
Banc réparti : plus de flux pour le dernier jeton

 drave-core/src/main.rs                             |   8 ++
 journal/sessions/MANIFEST.md                       |   2 +-
 .../bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md | 111 +++++++++++++++++++++
 .../rapport.md                                     |  17 ++--
 4 files changed, 129 insertions(+), 9 deletions(-)
commit 2184fc52298048d0a9f3cb4cf72231a648ec66a2
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 11:41:18 2026 -0400

    Banc réparti : plus de flux pour le dernier jeton
    
    Le dernier jeton n'a rien à prédire, et le banc lui demandait quand même un
    aller-retour complet : le pilote calculait ses 12 couches, les envoyait, le pair
    calculait les siennes et renvoyait un état que personne ne lisait. C'était 1/40
    du travail à 40 jetons et un aller-retour de plus par exécution.
    
    Vérifié après la correction : écart **0,00e0** inchangé, perplexité 18,0206 des
    deux côtés, et 255 flux au lieu de 256. La référence locale, elle, calcule encore
    ce dernier jeton — c'est écrit dans le commentaire pour que l'écart de temps
    entre les deux chemins ne surprenne personne.

diff --git a/drave-cor
… [968 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'profil-experts\\|profil-neurones' docs/vision.md README.md REPRISE.md docs/*.md | head", "description": "Vérifier profil-experts dans vision"}`

  ```
docs/vision.md:68:| `--profil-neurones`, `--neurones-sortie` | quels neurones s'allument, à quelle fréquence, avec quelle magnitude |
docs/vision.md:69:| `--profil-experts` | quels experts sont choisis (MoE), et à quel point le routage est concentré |
docs/vision.md:68:| `--profil-neurones`, `--neurones-sortie` | quels neurones s'allument, à quelle fréquence, avec quelle magnitude |
docs/vision.md:69:| `--profil-experts` | quels experts sont choisis (MoE), et à quel point le routage est concentré |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'flux servis\\|servies\\|n_flux\\|nb_flux\\|flux)\\|flux envoyés\\|flux envoy' drave-core/src/main.rs | head -30", "description": "Trouver l'affichage du nombre de flux"}`

  ```
1742:    println!("[flux] {servis} flux servis");
1899:                  {:.1} ko par jeton · {} lots (au lieu de {} flux)",
1909:              {:.1} % d'activité ({:.0} neurones par flux) · {} flux",
1915:             actifs_envoyes as f64 / nflux as f64, nflux);
3057:        println!("  rejeu             : {} listes servies, {} manquantes{}",
3058:                 r.servies, r.manquantes,
3059:                 if r.manquantes > 0 && r.servies == 0 {
3061:                 } else if r.manquantes > r.servies {
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 120, "offset": 1600}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1600:             let mut lg = [0u8; 4];
1601:             s.read_exact(&mut lg)?;
1602:             let longueur = u32::from_le_bytes(lg) as usize;
1603:             let mut corps = vec![0u8; longueur];
1604:             s.read_exact(&mut corps)?;
1605:             let mut idx = Vec::with_capacity(n);
1606:             let mut val = Vec::with_capacity(n);
1607:             let mut prev = 0u32;
1608:             let mut lus = 0usize;
1609:             let mut echappements = 0usize;
1610:             while idx.len() < n {
1611:                 if lus + 1 >= corps.len() && idx.len() + 1 < n {
1612:                     return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
1613:                         "corps de flux tronqué"));
1614:                 }
1615:                 let d = corps[lus]; lus += 1;
1616:                 let absolu = if d == 255 {
1617:                     echappements += 1;
1618:                     let a = u16::from_le_bytes([corps[lus], corps[lus+1]]) as u32;
1619:                     lus += 2;
1620:                     a
1621:               
… [6126 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 220, "offset": 1720}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1720:                     servis += 1;
1721:                     continue;
1722:                 }
1723:                 mdl.emb_imposee = Some(f.charge.en_dense(hidden));
1724:                 let sortie = mdl.forward(0, f.pos as usize);
1725:                 // La RÉPONSE est encodée comme la demande : un pair qui parle en
1726:                 // listes reçoit des listes, sans second réglage à faire tenir
1727:                 // cohérent entre les deux machines.
1728:                 if envoyer_flux(&mut sock, f.debut, f.fin, f.pos, &sortie, f.mode,
1729:                                 Some(&mdl)).is_err() {
1730:                     break;
1731:                 }
1732:                 servis += 1;
1733:             }
1734:             Err(e) => {
1735:                 // Un pair incompatible doit s'entendre dire POURQUOI : sans cela,
1736:                 // la session se termine sur « 0 flux servi » et rien d'autre.
1737:                 println!("[flux] arrêt : {e}");
1738:                 break;
1739:             }
1740:         }
1741:     }
1742:     println!("
… [11107 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 60, "offset": 1410}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/vision.md", "limit": 80, "offset": 50}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1410:                     x[i as usize] = v as f32 * echelles[i as usize / 32];
1411:                 }
1412:                 x
1413:             }
1414:         }
1415:     }
1416:     fn actifs(&self) -> usize {
1417:         match self {
1418:             ChargeFlux::Dense(v) => v.len(),
1419:             ChargeFlux::Liste { idx, .. } | ChargeFlux::Blocs { idx, .. } => idx.len(),
1420:             ChargeFlux::Lot(v) => v.len(),
1421:         }
1422:     }
1423:     /// Le lot aplati, pour le nœud qui doit le rendre à `forward_lot`.
1424:     fn plat(&self) -> &[f32] {
1425:         match self { ChargeFlux::Lot(v) => v, _ => &[] }
1426:     }
1427: }
1428: 
1429: /// Envoie un flux et rend le nombre d'octets écrits (en-tête compris) — c'est ce
1430: /// que la phase 3 doit chiffrer : octets par jeton × latence.
1431: fn envoyer_flux(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos: u32,
1432:                 actifs: &[f32], mode: u8, mdl: Option<&model::Model>)
1433:                 -> std::io::Result<(usize, usize)> {
1434:     let act = mdl.map(Act::du_modele).u
… [2179 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/vision.md</path>
<type>file</type>
<content>
50: les portes de non-régression tournent sur les deux.
51: 
52: La densité observée, elle, dépend du modèle et de la couche : **17,9 %** sur
53: Qwen2.5-0.5B à 512 jetons, mais les FFN denses de certaines familles ne sont pas
54: creux du tout (`reports/rapport-localite-activation.md`). Une vision honnête dit
55: où elle s'applique — et où elle ne s'applique pas.
56: 
57: ---
58: 
59: ## 2. Axe 1 — Voir et régler le modèle, neurone par neurone
60: 
61: Un flux de listes est **observable par construction** : on peut compter, tracer,
62: comparer, sans rien reconstruire.
63: 
64: Ce qui existe déjà, et qui a servi :
65: 
66: | outil | ce qu'il donne |
67: |---|---|
68: | `--profil-neurones`, `--neurones-sortie` | quels neurones s'allument, à quelle fréquence, avec quelle magnitude |
69: | `--profil-experts` | quels experts sont choisis (MoE), et à quel point le routage est concentré |
70: | `[config]` sur chaque exécution | quel chemin est **réellement** actif (rotation, cache KV, MLA, experts…) |
71: | `--ppl-profil` | le temps par poste (projections, rope, attention, FFN, tête) 
… [3348 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/vision.md", "limit": 115, "offset": 129}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/vision.md", "limit": 50}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/vision.md</path>
<type>file</type>
<content>
129:    échelle, bits) + des paires (destination, valeur). Compact, vérifiable,
130:    versionné ;
131: 2. **la granularité** : par couche ? par bloc de canaux ? par expert ? La mesure
132:    dira où le coût de sérialisation rattrape le gain de parallélisme — le
133:    croisement push/pull à 10 % donne déjà l'ordre de grandeur de ce qu'on
134:    transporte ;
135: 3. **le placement** : la même règle qu'à l'axe 2, appliquée entre machines — un
136:    opérateur va là où son entrée est déjà, ou là où elle coûte le moins à
137:    amener ;
138: 4. **ce qui ne se parallélise pas** : le décodage est **séquentiel** (un jeton
139:    dépend du précédent) ; c'est le **préremplissage** qui est parallèle par
140:    nature, et c'est donc là qu'il faut commencer ;
141: 5. **les mesures à faire** : débit d'un flux sérialisé, latence aller-retour,
142:    taille moyenne d'une tranche par couche, et le point où le réseau coûte plus
143:    que le calcul économisé.
144: 
145: Cette section est une **hypothèse de travail**, pas un résultat. Elle est écrite
146: ici parce qu'aucun autre moteur
… [5312 caractères tronqués]
  ```


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
14: Le projet s'appelait `Drave`, du nom de son origine : un cahier des charges
15: d'inférence ternaire sur un cluster de cartes Stratix V
16: (`Qtrinet-bootstrap.md`). Ce cahier des charges reste l'acte de naissance ; le
17: nom, lui, ne dit plus ce que le projet est devenu. **Drave** le dit.
18: 
19: ---
20: 
21: ## 1. Le cœur : des listes, pas des matrices
22: 
23: Un moteur 
… [1687 caractères tronqués]
  ```

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
12: | **le virage événementiel** | l'idée qui a tout changé : ne plus multiplier des matrices, mais **pousser des listes d'activation** vers leurs destinations (AER, *Address Event Representation*). Le prototype C mesure **7,79 G événements/s**, le croisement push/pull est mesuré à **10 % de densité** | `reports/rapport-cpu-aer.md`, `reports/rapport-
… [3502 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline --all | grep -i 'renom\\|nom' | head -10", "description": "Trouver le commit de renommage"}`

  ```
b97d129 Drave : renommage complet (crate, binaire, variables, documents)
15c4c8c Drave : document de vision, et le nom dans le README
095e093 REPRISE : l'item 5 reflète l'état final (chaîne vision démontrée, réserves nommées)
a42ebb3 REPRISE : MLA et vision tous deux faits, avec leurs réserves nommées
93b5e6d vision : l'API de mtmd est connue (en-tête récupéré), le blocage est nommé
2d173f1 vision : relevé du projecteur mmproj (paramètres et nommage réels)
f57e151 REPRISE.md : base de reprise autonome
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '22 %\\|22%\\|10 % de densité\\|10% de densité\\|croisement' README.md REPRISE.md docs/*.md reports/rapport-croisement-push-pull.md | head -30", "description": "Comparer le chiffre du croisement push/pull"}`

  ```
README.md:34:| **Croisement push/pull à 10 % de densité** | ✅ mesuré → [`reports/rapport-croisement-push-pull.md`](reports/rapport-croisement-push-pull.md) |
README.md:185:arbitraire → croisement ou réplication de bancs M20K). Le décodeur, lui, reste LUT-only :
README.md:376:| **pull** (`--dense`) | densité d'activation > 22 % — le cas d'un LLM dense | 29,5 tok/s |
README.md:377:| **push** (`--push`) | densité < 22 % — réseau creux, k-WTA, ReLU | 13,6 tok/s à 100 %, 20,6 à 5 % |
README.md:389:| Croisement push/pull | **~22 %** de densité d'activation, mesuré — pas 10 % (voir [`reports/rapport-croisement-push-pull.md`](reports/rapport-croisement-push-pull.md)) |
REPRISE.md:124:1. **Mesurer avant de conclure.** Le croisement push/pull était annoncé à 10 %,
REPRISE.md:125:   il est à 22 %. Dérouler un noyau « évident » n'a rien donné : le chemin était
REPRISE.md:180:| KV déporté, ctx 512 (point de croisement) | attention 2,91 (CPU) contre 3,22 ms (GPU) : le noyau ne paie qu'au-delà de ~4 000 clés |
docs/contexte-long.md:256:à 1 M à ≈ 5,7 s. Le point de croisement est vers **4 000 clés** (en dessous, les
docs/contexte-long.md:456:   croisement mesuré : c'est une décision d'ingénierie p
… [2102 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md"}`

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
7: > protocole de flux passe en **version 4** : le contrat d'activation transporte
8: > désormais aussi les sept top-k par projection, `--attn-topk`, `--qk-topk` et
9: > `--moe-topk`. Les sections ci-dessous décrivent l'état AVANT correction — elles
10: > restent la référence de ce qui a été trouvé, et la liste de ce qui reste
11: > (`--banc-vision` sans `Options`, `--bits` du noyau GPU, etc.).
12: 
13: 
14: **Révision auditée** : `drave-core/src/main.rs` sha256 `1726f9ac3665c3ce…` (2 999 lignes),
15: `drave-core/src/model.rs` sha256 `1d7eacc506db6cab…` (3 675 li
… [19599 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'Model::load' drave-core/src/main.rs | head -30", "description": "Vérifier les appels Model::load"}`

  ```
582:    let mut mdl = model::Model::load(path, ctx, n_threads, dense, keep, auto, q4, b6);
1220:            let mut mdl = model::Model::load(&chemin, 512, 16, true, 1.0, false, 0, 0);
1668:    let mut mdl = model::Model::load(&chemin, ctx, fils(&opt), true, opt.keep, false, 0, 0);
1768:    let mut mdl = model::Model::load(&chemin, ctx, fils(&opt), true, opt.keep, false, 0, 0);
1928:    let mut mdl = model::Model::load(path, 4096, fils(&opt), opt.dense, opt.keep, false, 0, 0);
2803:    let mut mdl = model::Model::load(path, ctx, n_threads, dense, keep, auto, q4, b6);
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'ffn_gain\\|opt.keep\\|fils(&opt)\\|opt.threads' drave-core/src/main.rs | head -40", "description": "Vérifier les corrections de drapeaux"}`

  ```
344:    if opt.threads_impose { opt.threads.max(1) }
420:    hebb_out: String, ffn_gain: Option<(usize, f32)>, matrix: String,
515:                o.ffn_gain = Some((v[0].parse().unwrap(), v[1].parse().unwrap())); 2
572:        hebb_layer, hebb_q, hebb_out, sans_yarn, lot, ffn_gain,
606:    if let Some((l, g)) = ffn_gain {
607:        mdl.ffn_gain = Some((l, g));
1668:    let mut mdl = model::Model::load(&chemin, ctx, fils(&opt), true, opt.keep, false, 0, 0);
1768:    let mut mdl = model::Model::load(&chemin, ctx, fils(&opt), true, opt.keep, false, 0, 0);
1928:    let mut mdl = model::Model::load(path, 4096, fils(&opt), opt.dense, opt.keep, false, 0, 0);
2030:    let threads = if opt.threads_impose { opt.threads } else {
2140:    let threads = if opt.threads_impose { opt.threads } else {
2764:        ffn_gain, logits_bin, keep,
2845:    if let Some((l, g)) = ffn_gain {
2847:        mdl.ffn_gain = Some((l, g));
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l drave-core/src/*.rs", "description": "Compter les lignes du moteur"}`

  ```
976 drave-core/src/engine.rs
   721 drave-core/src/gguf.rs
   821 drave-core/src/gpu.rs
  1440 drave-core/src/list.rs
  3112 drave-core/src/main.rs
  3863 drave-core/src/model.rs
   507 drave-core/src/tokenizer.rs
 11440 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '9,1\\|+8,4\\|28,3\\|41,6\\|perplexité' reports/rapport-mur-memoire-4bits.md | head -20", "description": "Vérifier le +9,1 % du README"}`

  ```
111:| int8 partout | **17,4092** | — | 28,3 | 22,1 |
126:3. Le gain de bout en bout est **×1,39** (28,3 → 39,2 tok/s) pour **+26 % de
127:   perplexité**. Sur un modèle de 0,5 G, c'est le prix connu des petits modèles en
143:| Qwen2.5-0.5B **Q8_0** | int8 | **19,2647** | — | 18,0 | 28,3 |
144:| Qwen2.5-0.5B **Q4_0** | int8 (requantifié) | 21,1971 | +10,0 % | 18,0 | 28,3 |
145:| Qwen2.5-0.5B **Q4_0** | **4 bits verbatim** | **21,0116** | **+9,1 %** | **13,1** | **38,9** |
153:1. **Le prix réel des 4 bits sur ce modèle est +9,1 % de perplexité** — pas les
155:   vrai coupable : elle coûtait 12 % de perplexité *en plus* du format.
157:   poids** : 21,01 contre 21,20 de perplexité (il ne requantifie pas) et 13,2
191:montré. La perplexité bouge au 4ᵉ chiffre (21,0116 → 21,0131) : la somme n'est
199:  choix sans hésitation : ×1,34 de débit **et** une perplexité légèrement
201:- **Pour un modèle 8 bits**, requantifier en 4 bits coûte +26 % de perplexité :
222:     --threads 16 --limit 512 $f | grep "perplexité"
228:     --threads 16 --limit 256 $f | grep "perplexité"
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '41,6\\|41\\.6\\|44 tok\\|44,0\\|39,2' README.md reports/rapport-mur-memoire-4bits.md reports/rapport-inference.md | head -20", "description": "Vérifier le 41,6 tok/s du README"}`

  ```
README.md:170:| 2 % | 1,020 | 0,251 | ×4,06 | 44,0 | ×7,96 |
README.md:378:| **4 bits** (`--q4`, `--q4-tout`) | modèle 4 bits existant (Q4_0) ou débit prioritaire | **41,6 – 44 tok/s** |
README.md:394:requantification), fait tourner un vrai Qwen2.5-0.5B **Q4_0** à **41,6 tok/s**
reports/rapport-mur-memoire-4bits.md:114:| 4 bits corps entier | 21,9118 | +25,9 % | **39,2** | 13,1 |
reports/rapport-mur-memoire-4bits.md:126:3. Le gain de bout en bout est **×1,39** (28,3 → 39,2 tok/s) pour **+26 % de
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '24,90\\|25,00\\|2 040' README.md reports/rapport-inference.md | head -10", "description": "Vérifier la perplexité 24,90 du README"}`

  ```
README.md:388:| Perplexité WikiText-2 | **24,90** sur 2 040 jetons contre **25,00** pour numpy + OpenBLAS |
reports/rapport-inference.md:62:### Perplexité WikiText-2 (2 040 tokens, fenêtres de 256)
reports/rapport-inference.md:66:| numpy float32 (OpenBLAS) | 25,0004 |
reports/rapport-inference.md:251:| **Perplexité WikiText-2** | **24,90** | **27,83** | **+12 %** |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '41,6\\|41\\.6' reports/*.md docs/*.md REPRISE.md | head -20", "description": "Chercher 41,6 partout"}`

  ```
reports/rapport-compacite-trace.md:145:   (50,1 Mo contre 41,6 Mo). Vérifié sur quatre segments du fichier : ce n'est
reports/rapport-passage-a-l-echelle.md:47:par jeton ÷ 20 Go/s = **13 ms/jeton = 41 tok/s**, contre **41,6 tok/s mesurés**.
reports/rapport-passage-a-l-echelle.md:56:| Qwen2.5-0.5B (dense) | 0,49 G | 0,26 Go | 13 ms | **41,6** (mesuré) |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '2 319\\|2319\\|386 lignes\\|5 000 lignes\\|11 440' README.md REPRISE.md docs/*.md reports/*.md | head -20", "description": "Vérifier les comptes de lignes cités"}`

  ```
README.md:280:le moteur tient en 386 lignes). Détail complet :
README.md:354:BLAS, sans aucune dépendance : **2 319 lignes de Rust, `std` seul**. Détail :
REPRISE.md:16:`drave-core` est un moteur d'inférence Rust (~5 000 lignes, `std` seul) qui
reports/rapport-inference.md:3:**2 319 lignes de Rust, `std` seul, zéro dépendance.** Le modèle Qwen2.5-0.5B-Instruct
reports/rapport-optimisations.md:3:Moteur `drave-core` (Rust, **std seul**, zéro dépendance, 386 lignes de moteur).
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '9,5146\\|17,43\\|19,3885\\|15,1757\\|144,8289\\|132 Mo\\|53 Mo\\|1 024\\|5 120\\|4 096\\|8 192' docs/contexte-long.md | head -50", "description": "Relever les chiffres de contexte-long"}`

  ```
12:| gpt-oss-120b | 131 072 | 4 096 | ×32 | ×8 au-delà du déclaré → extrapolation |
77:YaRN ×32 couvre **exactement** 131 072 jetons (4 096 × 32), c'est-à-dire le
121:| KV | nous (512 jetons) | llama.cpp (512) | nous (~4 600 jetons) | llama.cpp (8 192) |
151:### 4.bis.2 À 8 192 jetons, la longueur exacte de la comparaison llama.cpp
156:| KV | nous, 8 191 jetons notés | Δ | llama.cpp (8 192) | Δ | durée de la passe |
194:| f32 | 4 096 | 1,3 | **0,3** | ×4 | 5,1e-6 |
251:| 4 096 | CPU | 12,2177 | **22,16** | 219,4 s |
252:| 4 096 | **KV déporté** | **12,2175** | **3,29** | **136,2 s** (−38 %) |
286:Qwen2.5-0.5B, contexte 4 096, 4 095 jetons notés, `--lot 512` :
322:scalaire **au bit près**, ce que la perplexité confirme (19,3885 et 13,1359
331:Même mécanisme côté hôte : `KvCache` démarre à 1 024 positions et **double à la
335:19,3885.
341:à 2 048 jetons). L'écart de +3,0 % contre +0,8 % à 8 192 vient donc d'ailleurs :
350:(4 096 pour gpt-oss), interpolation YaRN au-delà — sans la mise à l'échelle de
359:> 8 192 jetons on ne note pas les mêmes tranches qu'à 512, et le même corpus va
372:| 1 024 | **46,94** | 71,35 | 417,65 |
374:| 4 096 | **170,78** | 400,13 | — |
386:| 1 024 | **49,9
… [1102 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'à faire\\|fait\\|✅\\|⏳\\|🔬' docs/contexte-long.md | head -40", "description": "Relever les statuts de contexte-long"}`

  ```
23:`--plan --ctx N` chiffre le KV pour trois précisions et tient compte du fait que
101:| E1 | **Préremplissage par lots** | **fait** : `gemm_dense_i8` et `gemm_dense_q4` (produits matrice-matrice par tranches), `forward_lot` juste sur dense **et** sur MoE avec regroupement des jetons par expert ; débit bout en bout à chiffrer | 32 k utilisable ; TTFT | le noyau est là ; reste à mesurer et à élargir les tranches |
102:| E2 | **KV int8** | **fait** (échelle par vecteur, dequantification à la lecture) | ÷4 sur le KV ; 128 k confortable | mesuré : +7,1 % de perplexité (llama.cpp q8_0 : +3,1 %) |
103:| E3 | **KV int4** | **fait** (nibbles empaquetés) | 1 M tient en RAM (9,7 Go) et en VRAM | mesuré : **+384 %** — llama.cpp q4_0 : +411 % ; à réserver aux cas où la mémoire manque |
104:| E4 | **KV déporté sur les 2 GPU** (pagination, préchargement) | **fait** : noyau `attn_kv_*` (tuiles de 32 clés en mémoire partagée, une passe par (tête KV, tranche), recombinaison + puits), miroir VRAM du cache (`DRAVE_GPU_KV=1`) — mesuré **×12 à ×73** sur l'attention selon le format, PPL identique ; voir §4.ter | décodage à 1 M borné par la VRAM et non par la RAM | moyen |
105:| E5 | **Attention creuse*
… [738 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md", "limit": 45, "offset": 474}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md</path>
<type>file</type>
<content>
474: ## 6. Ce qui se mesure tout de suite
475: 
476: 1. **Aiguille dans la botte de foin** (`tools/aiguille.py`) : la perplexité ne dit
477:    pas si le modèle RETROUVE une information. Le script plante un code à une
478:    profondeur donnée et vérifie qu'il ressort ; c'est la mesure de qualité qui
479:    manque au plan. Premier essai sur Qwen2.5-0.5B : **6 sondes sur 6 échouent**
480:    (1 024 et 2 048 jetons, profondeurs 0,1 / 0,5 / 0,9) — le demi-milliard de
481:    paramètres ne sait pas retrouver un code, donc ce modèle ne peut pas servir de
482:    référence ; l'essai est relancé sur Qwen3-30B-A3B. Ce n'est pas un défaut du
483:    moteur : c'est la limite du modèle, et il valait mieux la mesurer que la
484:    supposer. Second essai sur Qwen3-30B-A3B : **9,6 minutes pour une seule
485:    sonde** (1 024 jetons de contexte) et un échec — le remplissage, répété à
486:    l'identique, ne fait pas un banc d'essai valable, et le préremplissage
487:    séquentiel rend chaque sonde hors de prix (1,8 jeton/s). Le test est donc
488:    **arrêté** : il faudra un remplissa
… [1723 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'E5\\b' REPRISE.md docs/*.md reports/*.md | head -20", "description": "Comparer le statut de E5"}`

  ```
REPRISE.md:152:| 8 | suite du plan 1 M | **fait pour E4/E5** | **E4 KV déporté en VRAM** : noyaux `attn_kv_*` (tuiles de 32 clés, softmax en ligne, recombinaison + puits), miroir du cache **paginé** (capacité doublée à la demande : 0,05 Go de VRAM à ctx 1 M après 512 jetons) et `DRAVE_GPU_KV=1` — à 1 M de clés l'attention passe de 968 ms à **13,2 ms** par couche (int4, ×73) et, dans le moteur à 4 096 de contexte, de **22,2 à 3,3 ms/jeton** (−38 % de bout en bout) à perplexité identique (12,2177 → 12,2175). **E5 attention creuse** : mesurée (`--attn-topk 256` : 234,9 contre 298,6). MLA et vision restent non testables (aucun modèle MLA ici ; le projecteur `mmproj` est là mais rien ne lit les patchs) |
docs/contexte-long.md:105:| E5 | **Attention creuse** | à faire — `--attn-topk` et `--attn-window` existent et se mesurent au protocole `--depuis` | casse le O(N) du décodage | moyen |
docs/contexte-long.md:111:quelques minutes), puis E4/E5 selon l'usage (décodage long ou préremplissage
docs/plan-mla-vision.md:349:  E5 v3 = haswell) ;
reports/bilan-multi-materiel.md:7:Machine : 2 × Xeon E5-2687W v3 (20 cœurs / 40 threads, 125 Go), 2 × Quadro
reports/rapport-cpu-aer.md:14:## Mesures sur 
… [344 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -ohE 'DRAVE_[A-Z0-9_]+' README.md REPRISE.md docs/*.md reports/*.md | sort -u > /tmp/doc_env.txt; grep -ohE 'DRAVE_[A-Z0-9_]+' drave-core/src/*.rs | sort -u > /tmp/code_env.txt; echo \"=== dans docs, absents du code ===\"; comm  … [183 caractères tronqués]`

  ```
=== dans docs, absents du code ===
DRAVE_BANC_KV_
DRAVE_FLUX_POS
=== dans le code, absents des docs ===
DRAVE_BANC_KV_DEBUG
DRAVE_BANC_KV_GRAD
DRAVE_BANC_KV_KUNIT
DRAVE_BANC_KV_UNIT
DRAVE_BANC_KV_V1
DRAVE_TRACE_BLOCS
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'DRAVE_' README.md | head -20", "description": "Voir les variables dans le README"}`

  ```
12:Le nom du crate et du binaire (`drave-core`, variables `DRAVE_*`) changera dans un
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'DRAVE_FLUX_POS\\|DRAVE_TRACE_BLOCS\\|DRAVE_Q8_BLOCS\\|DRAVE_SANS_EMPRUNT' README.md REPRISE.md docs/*.md reports/*.md drave-core/src/*.rs | head -20", "description": "Localiser DRAVE_FLUX_POS et DRAVE_TRACE_BLOCS"}`

  ```
docs/plan-prefill-reparti.md:256:3. *En diagnostic* : `DRAVE_FLUX_POS=1` fait imprimer `[flux] lot pos .. pos+t-1`
reports/rapport-drapeaux-ignores.md:108:| `DRAVE_Q8_BLOCS` · `DRAVE_SANS_EMPRUNT` | `DenseQ8::build` (285) · `Proj::load` (345, 352) | — | ✅ |
drave-core/src/model.rs:279:/// Construit une matrice int8 : **une échelle par bloc de 32** (`DRAVE_Q8_BLOCS=1`,
drave-core/src/model.rs:285:    if std::env::var("DRAVE_Q8_BLOCS").is_ok() && n_in % 32 == 0 {
drave-core/src/model.rs:343:            // `DRAVE_SANS_EMPRUNT=1` force la reconstruction : c'est ce qui permet
drave-core/src/model.rs:345:            let emprunt = keep >= 1.0 && std::env::var("DRAVE_SANS_EMPRUNT").is_err();
drave-core/src/model.rs:352:            let emprunt = keep >= 1.0 && std::env::var("DRAVE_SANS_EMPRUNT").is_err();
drave-core/src/model.rs:526:    /// 3 (`DRAVE_TRACE_BLOCS=1` : valeurs i8 et une échelle f16 par bloc de 32
drave-core/src/model.rs:546:        // Version 3 sur `DRAVE_TRACE_BLOCS=1` : en plus, valeurs i8 et une échelle
drave-core/src/model.rs:549:        let version: u16 = if std::env::var("DRAVE_TRACE_BLOCS").is_ok() { 3 } else { 2 };
drave-core/src/model.rs:2786:s'applique pas — utilise
… [53 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short && ls -la drave-core/src/model.rs && sed -n '500,560p' drave-core/src/model.rs", "description": "Vérifier si model.rs a changé"}`

  ```
M drave-core/src/main.rs
 M drave-core/src/model.rs
 M journal/README.md
-rw-r--r--. 1 stephane stephane 201831 30 sep 12:21 drave-core/src/model.rs
    if m & 0x0080_0000 != 0 { m = 0; e += 1; if e >= 31 { return s | 0x7c00; } }
    s | ((e as u16) << 10) | ((m >> 13) as u16)
}

/// f16 → f32, l'inverse exact de la fonction ci-dessus (dénormalisés compris).
pub fn f32_depuis_f16(h: u16) -> f32 {
    let s = ((h >> 15) & 1) as u32;
    let e = ((h >> 10) & 0x1f) as u32;
    let m = (h & 0x3ff) as u32;
    let bits = if e == 0 {
        if m == 0 { s << 31 } else {
            let (mut e2, mut m2) = (127 - 15 + 1i32, m);
            while m2 & 0x400 == 0 { m2 <<= 1; e2 -= 1; }
            (s << 31) | ((e2 as u32) << 23) | ((m2 & 0x3ff) << 13)
        }
    } else if e == 31 { (s << 31) | 0x7f80_0000 | (m << 13) }
    else { (s << 31) | ((e + 127 - 15) << 23) | (m << 13) };
    f32::from_bits(bits)
}

/// Trace du **flux d'activation** : par (couche, position), la liste des
/// neurones actifs — indice, valeur — avec son échelle. C'est le cœur de la
/// vision mis sur disque : on peut rejouer, comparer, et c'est aussi le format
/// qu'un nœud distant devrait recevoir pour continuer l
… [1778 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'VERSION_FLUX\\|const TAILLE_TETE' drave-core/src/main.rs | head && git diff --stat && sha256sum drave-core/src/main.rs drave-core/src/model.rs", "description": "Vérifier VERSION_FLUX et l'état du diff"}`

  ```
1295:const VERSION_FLUX: u8 = 3;
1323:const TAILLE_TETE: usize = 4 + 1 + 1 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 1
1484:    tete.push(VERSION_FLUX);
1518:    tete.push(VERSION_FLUX);
1559:    if version != VERSION_FLUX {
1562:            format!("flux en version {version}, cette build parle la {VERSION_FLUX} \
 drave-core/src/main.rs  |   3 +-
 drave-core/src/model.rs | 165 +++++++++++++++++++++++++++++++++++++++++++++---
 journal/README.md       |   5 +-
 3 files changed, 162 insertions(+), 11 deletions(-)
d5e901368718f14fd34a8664631a08f090150ff12df4b7592cf3dcdc919f87cb  drave-core/src/main.rs
0a0856cc9e2bcff72efe27b622afe04e94d9ab83fada91ab294d05620f18dc06  drave-core/src/model.rs
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- drave-core/src/main.rs", "description": "Voir le diff de main.rs"}`

  ```
diff --git a/drave-core/src/main.rs b/drave-core/src/main.rs
index 2adf53b..f9d6fab 100644
--- a/drave-core/src/main.rs
+++ b/drave-core/src/main.rs
@@ -2804,7 +2804,8 @@ fn run_ppl(opt: Options) {
     if let Some(chemin) = flux_forcer.as_deref() {
         match model::FluxRelecteur::lire(chemin) {
             Ok(r) => {
-                println!("[flux] rejeu depuis {chemin} : {} listes enregistrées", r.listes.len());
+                println!("[flux] rejeu depuis {chemin} : {} listes enregistrées",
+                         r.listes.len() + r.listes_blocs.len());
                 mdl.flux_force = Some(r);
             }
             Err(e) => eprintln!("[flux] lecture impossible de {chemin} : {e}"),
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat -- reports/ && ls -la reports/ | tail -5 && ls -la reports/rapport-coherence-docs.md 2>/dev/null", "description": "Vérifier si un rapport de cohérence existe déjà"}`

  ```
-rw-------. 1 stephane stephane 10689 30 sep 08:44 rapport-prefill-par-lots.md
-rw-------. 1 stephane stephane  7101 30 sep 08:44 rapport-programme-evolutif.md
-rw-r--r--. 1 stephane stephane 12143 30 sep 11:39 rapport-transport-liste.md
-rw-r--r--. 1 stephane stephane  5372 28 sep 13:59 rapport-travail-reel.md
-rw-r--r--. 1 stephane stephane  4425 30 sep 08:44 rapport-valeur-unaire.md
[exit code: 2]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== renvois reports/xxx.md cassés ===\"; grep -ohE 'reports/[A-Za-z0-9_.-]+\\.md' README.md REPRISE.md docs/*.md reports/*.md | sort -u | while read -r p; do [ -e \"$p\" ] || echo \"CASSÉ: $p\"; done; echo \"=== renvois docs/x … [423 caractères tronqués]`

  ```
=== renvois reports/xxx.md cassés ===
CASSÉ: reports/rapport-lecteur-ddr3.md
CASSÉ: reports/rapport-pe-evenementiel.md
CASSÉ: reports/rapport-prefill-reparti.md
=== renvois docs/xxx.md cassés ===
=== renvois tools/xxx cassés ===
CASSÉ: tools/mtmd
CASSÉ: tools/pack_lists.py
CASSÉ: tools/quartus_env.sh
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'pack_lists\\|quartus_env\\|tools/mtmd' README.md REPRISE.md docs/*.md reports/*.md | head", "description": "Localiser les renvois tools cassés"}`

  ```
docs/plan-mla-vision.md:461:`tools/mtmd/clip.cpp` (320 ko) a été récupéré et dépouillé. Ce qui s'y lit, pour
reports/bilan-multi-materiel.md:149:python3 tools/pack_lists.py <modele.gguf> blk.0.ffn_gate.weight --sources 64 --out sim
reports/bilan-multi-materiel.md:152:source tools/quartus_env.sh && quartus_sh --flow compile syn/reader/event_reader
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | wc -l && ls reports/ | head -50 && echo \"=== tools existants ===\" && ls tools/*.py tools/*.sh 2>/dev/null | head -30", "description": "Lister reports et tools"}`

  ```
36
aiguille-30b.md
aiguille-gpt-oss.md
bilan-multi-materiel.md
rapport-8bits.md
rapport-aiguille.md
rapport-analyse-flux.md
rapport-attention-creuse.md
rapport-attribution-kv.md
rapport-campagne-parcimonie.md
rapport-capteur-hebbien.md
rapport-compacite-trace.md
rapport-cpu-aer.md
rapport-croisement-push-pull.md
rapport-drapeaux-ignores.md
rapport-encodage.md
rapport-eparsite.md
rapport-gpt-oss-perplexite.md
rapport-grappes.md
rapport-greffon.md
rapport-harnais.md
rapport-inference.md
rapport-localite-activation.md
rapport-minimal.md
rapport-modele-reel.md
rapport-mode-listes.md
rapport-mur-memoire-4bits.md
rapport-optimisations.md
rapport-parcimonie-imposee.md
rapport-passage-a-l-echelle.md
rapport-phase3-reparti.md
rapport-precision.md
rapport-prefill-par-lots.md
rapport-programme-evolutif.md
rapport-transport-liste.md
rapport-travail-reel.md
rapport-valeur-unaire.md
=== tools existants ===
tools/aiguille.py
tools/analyse_flux.py
tools/archive_sessions.py
tools/compare_logits.py
tools/diff_flux.py
tools/flux_codec.py
tools/harmony_canonique.py
tools/make_patch.py
tools/mla_synthetique.py
tools/pair_factice.py
tools/preparer_colab.sh
tools/profil_flux.py
tools/proxy_latence.py
too
… [86 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '871' README.md REPRISE.md docs/*.md reports/*.md | head -20", "description": "Chercher le chiffre 871"}`

  ```
README.md:168:| **12,5 %** | 1,125 | **0,871** | **×1,29** | 12,7 | **×2,30** |
reports/rapport-encodage.md:54:| 12.5 % | 1.125 | **0.871** | ×1.29 | 12.7 | ×2.30 |
reports/rapport-transport-liste.md:3:**En une ligne** : le flux peut voyager en liste creuse (871 octets au lieu de
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '1 989\\|1989' README.md REPRISE.md docs/*.md reports/*.md | head", "description": "Chercher 1 989"}`

  ```
docs/colab-reparti.md:36:* **Débit** : 3 623 octets par flux en dense, 1 989 en listes à échelle par bloc
reports/rapport-transport-liste.md:230:ou 1 989 (blocs à 68 % d'activité), et le calcul distant coûte 16 ms : le réseau
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '17,4294\\|17\\.4294\\|9,5146\\|9\\.5146\\|18,0206\\|18\\.0206\\|21,8873' README.md REPRISE.md docs/*.md reports/*.md | head -20", "description": "Traquer les perplexités de rejeu"}`

  ```
REPRISE.md:251:**9,5146 des deux côtés à 1 024 jetons** (1 024 flux, texte réel), le banc
docs/format-flux.md:138:| un rejeu redonne le même résultat | `--flux-forcer` : perplexité **19,3885** avec et sans rejeu (chemin par jeton), **17,4294** (chemin par lots) |
docs/roadmap.md:116:| 2026-09-30 | découpage fidèle à **1 024 jetons** (1 024 flux, texte réel) | perplexité **9,5146** des deux côtés, écart **0,00e0** · 19,4 ms en local contre 19,7 ms à attendre le pair |
reports/rapport-phase3-reparti.md:51:perplexité **9,5146 des deux côtés**, écart 0,00e0), et à chaque fois le banc
reports/rapport-transport-liste.md:175:| dense f32 | 3 623 | 0,00e0 | 18,0206 |
reports/rapport-transport-liste.md:176:| blocs 0,01, indices u16 | 2 268 | 2,74e-2 | 21,8873 |
reports/rapport-transport-liste.md:177:| **blocs 0,01, indices par écarts** | **1 568** | **2,74e-2** | **21,8873** |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '18,0851\\|18,02\\|798,3\\|1 621,7\\|693,4' README.md REPRISE.md docs/*.md reports/*.md | head -20", "description": "Traquer d'autres chiffres de perplexité"}`

  ```
docs/format-flux.md:131:découpage (798,3 au lieu de 18,2).
docs/format-flux.md:142:| un lot ne change pas le résultat non plus | 256 jetons en 4 lots de 64 : écart **0,00e0** (18,0851 = 18,0851) ; en 1 lot de 256 : **0,00e0** (918 ko sur le fil) |
docs/plan-prefill-reparti.md:224:sur `0..n_layer`, perplexité répartie 798,3) : on ne réintroduit pas une seconde
docs/plan-prefill-reparti.md:377:   `flux_brut` dans la branche lot, c'est refaire 798,3 au lieu de 18,2.
docs/plan-prefill-reparti.md:382:   donné la perplexité répartie 798,3.
docs/roadmap.md:285:| avant correction | 144,8289 | 1 621,7239 | ×11,2 |
docs/roadmap.md:286:| après la norme seule | 144,8289 | 693,4492 | ×4,8 |
reports/rapport-phase3-reparti.md:28:`flux_brut`) a bien amélioré les choses — **1 621,7 → 693,4** — mais pas assez :
reports/rapport-phase3-reparti.md:44:| avant correction | 144,8289 | 1 621,7239 | ×11,2 |
reports/rapport-phase3-reparti.md:45:| après la norme seule | 144,8289 | 693,4492 | ×4,8 |
reports/rapport-transport-liste.md:69:contre 18,02). Ce n'est pas une perte de précision, c'est un calcul faux.
reports/rapport-transport-liste.md:127:sur **256 jetons de WikiText-2**, où la référence locale vaut 1
… [86 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '18,0851\\|18\\.0851\\|917 543\\|917543\\|918 ko' README.md REPRISE.md docs/*.md reports/*.md | head", "description": "Chercher les chiffres du mode lot"}`

  ```
docs/format-flux.md:94:de la même façon), ou en **1 seul lot de 917 543 octets** — un aller-retour pour
docs/format-flux.md:142:| un lot ne change pas le résultat non plus | 256 jetons en 4 lots de 64 : écart **0,00e0** (18,0851 = 18,0851) ; en 1 lot de 256 : **0,00e0** (918 ko sur le fil) |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show cda3162 -- docs/format-flux.md | head -80", "description": "Voir le diff format-flux du commit phase 3.4"}`

  ```
commit cda31629420aa92c7313a81d3d102328371faed4
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 12:02:39 2026 -0400

    Phase 3.4 : préremplissage par LOTS sur le fil — écart 0,00e0
    
    Le transport était séquentiel : un flux par jeton, donc un aller-retour par jeton.
    Le mode 3 « lot » envoie N états d'un coup (`n` = nombre d'ÉTATS, corps de
    `n × dimension × f32`, la dimension ne voyage pas) :
    
    | découpage | lots | écart local/réparti |
    |---|---|---|
    | 256 jetons en lots de 64 | 4 | **0,00e0** (18,0851 = 18,0851) |
    | 256 jetons en UN lot | 1 | **0,00e0** (917 543 octets sur le fil) |
    | contrôle `--lot 1` | 255 | **0,00e0** (18,0206 = 18,0206) |
    
    Côté modèle : `emb_imposee_lot` (états imposés pour tout un lot, aplatis), le
    pendant de `emb_imposee` pour un jeton seul. Le critère de la phase 3.4 est
    atteint localement ; il reste à le faire tourner sur le runtime Colab.
    
    **Le bug que ce commit corrige, et qui ne se voyait pas** : `envoyer_lot` écrivait
    40 octets d'en-tête pour un `TAILLE_TETE` de 39 — un `push(0)` hérité d'une
    expérience annulée plus tôt dans la session. Tout le corps se décalait d'un octet

… [3228 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 6b3b53f -- docs/format-flux.md", "description": "Voir le diff DRVF v2 de format-flux"}`

  ```
commit 6b3b53f0724f77c4923713c07d60e35af238bdf4
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 12:17:39 2026 -0400

    DRVF v2 sur le disque : −49,87 % de trace, rejeu identique
    
    L'étude de compacité déléguée disait où était le gras : **66 % du fichier est fait
    d'indices u32** alors que la liste est triée, donc que l'écart au neurone
    précédent tient sur un octet dans 99,9997 % des cas (22 échappements sur 8,79 M
    mesurés). La version 2 du format écrit ces écarts — et c'est du rangement :
    
    | | v1 | v2 |
    |---|---|---|
    | trace dense, 512 jetons | 132 396 736 o | **66 370 408 o (−49,87 %)** |
    | rejeu `--flux-forcer` | 19,3885 | **19,3885**, identique |
    | listes · actifs | 24 576 · 22 008 776 | identiques |
    
    Le lecteur lit la 1 ET la 2 (une version inconnue est refusée en la nommant), et
    l'implémentation Python indépendante (`tools/flux_codec.py`) relit la trace v2
    écrite par Rust avec exactement les mêmes comptes — l'invariant « deux
    implémentations, un aller-retour identique » tient pour la v2.
    
    **Ce que le rejeu silencieux cachait** : le rejeu annonce maintenant ses compteurs
    (`N listes servies, M m
… [3288 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'PLAFOND_LOT\\|PLAFOND' drave-core/src/main.rs | head", "description": "Vérifier le plafond du lot"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'flux_brut\\|--flux-norme\\|DRAVE_FLUX_VERIF' README.md REPRISE.md docs/*.md | head -20", "description": "Vérifier flux_brut et DRAVE_FLUX_VERIF dans docs"}`

  ```
REPRISE.md:260:   maintenant portée par un drapeau explicite, `flux_brut`.
docs/format-flux.md:128:moteur le déclare par un drapeau explicite (`flux_brut`) plutôt que de le déduire
docs/format-flux.md:139:| la fidélité de l'encodage est chiffrée | `DRAVE_FLUX_VERIF=1` : écart relatif **1,5e-5**, soit la quantification 16 bits |
docs/plan-prefill-reparti.md:160:`mdl.flux_brut = true`. Puis, avant le chemin « un jeton » (ligne 1532) :
docs/plan-prefill-reparti.md:179:plage va jusqu'à la dernière couche (`flux_brut`). La norme appartient au nœud qui
docs/plan-prefill-reparti.md:375:6. **La norme finale, une seule fois** — le serveur garde `flux_brut = true` ; le
docs/plan-prefill-reparti.md:377:   `flux_brut` dans la branche lot, c'est refaire 798,3 au lieu de 18,2.
docs/plan-prefill-reparti.md:380:   `flux_brut || couche_fin < n_layer` (model.rs:2544). Ne pas ajouter de boucle
docs/roadmap.md:196:Identique. Et le diagnostic (`DRAVE_FLUX_VERIF=1`) chiffre la fidélité de
docs/roadmap.md:231:   par un drapeau explicite, `flux_brut` : un nœud intermédiaire rend TOUJOURS un
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 80, "offset": 1200}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1200:             }
1201:         }
1202:         println!("projecteur : {n_groupe} groupes × {n2} valeurs, |sortie| = {:.4}, 4 premières {:?}",
1203:                  y.iter().map(|v| v * v).sum::<f32>().sqrt(),
1204:                  &y[..4].iter().map(|v| (v * 1e4).round() / 1e4).collect::<Vec<_>>());
1205:         proj = Some((Vec::new(), y));
1206:     }
1207: 
1208:     // ---- Injection : le moteur consomme-t-il un embedding d'image ?
1209:     // `DRAVE_VISION_TEXTE=<modele.gguf>` charge le modèle de texte et lui impose le
1210:     // PREMIER jeton d'image via `Model::emb_imposee` — le chemin qui manquait
1211:     // (« forward partait toujours de token_embd »). C'est un contrôle de
1212:     // PLOMBERIE : le moteur ne panique pas, il rend des logits d'échelle
1213:     // normale. La qualité, elle, demanderait la comparaison complète.
1214:     if let Some((_, y)) = proj.as_ref() {
1215:         let n_emb = 3584usize;
1216:         let n_tok = y.len() / n_emb;
1217:         println!("injection : {n_tok} jetons × {n_emb} disponibles");
1218:         let chemin 
… [3557 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '2 300\\|~2 30\\|2 159' README.md REPRISE.md docs/*.md reports/*.md | head", "description": "Chercher le chiffre ~2 300 de REPRISE"}`

  ```
REPRISE.md:274:| listes i16, seuil 0,01 | ~2 300 | 2,7e-2 |
docs/roadmap.md:111:| 2026-09-30 | protocole de flux v2, deux processus, localhost | en-tête de 39 octets (version, mode, réglages d'activation) · dense f32 **3 623 octets/flux** · listes i16 2 159 · **blocs + indices par écarts 1 568 (÷2,3)** pour 2,7 % d'écart à 256 jetons de vrai texte |
docs/roadmap.md:250:**1 745 octets contre 2 159** pour la liste i16, et 14 % d'écart contre 16 % —
reports/rapport-inference.md:181:2. Elle tient dans **2 300 lignes de Rust sans aucune dépendance** — pas de BLAS, pas
reports/rapport-transport-liste.md:134:| listes i16 | 0,02 | 59,2 % | 2 159 | 1,6e-1 |
reports/rapport-transport-liste.md:137:toujours les listes à sparsité égale (1 745 contre 2 159 octets, et 14 % contre
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '97,6\\|16,1\\|15,9\\|8,3 s\\|24,5' README.md REPRISE.md docs/*.md reports/*.md | head -20", "description": "Vérifier les chiffres Nagle"}`

  ```
REPRISE.md:277:`TCP_NODELAY` a divisé l'attente du pair par six (**97,6 → 16,1 ms** par jeton,
docs/colab-reparti.md:25:| latence | ✅ `TCP_NODELAY` : 16,1 ms d'attente contre 15,9 ms de calcul local (97,6 ms avant) |
docs/contexte-long.md:260:appel — 24 couches × 6 appels CUDA par jeton, mesuré **24,5 ms/jeton** à 512
docs/plan-prefill-reparti.md:355:   différé du pair la retarde : **97,6 ms d'attente contre 15,6 ms de calcul**,
docs/roadmap.md:112:| 2026-09-30 | `TCP_NODELAY` sur le banc réparti, 200 jetons | attente du pair **97,6 → 16,1 ms** par jeton (calcul local : 15,9 ms) · banc complet 24,5 → **8,3 s**, soit le temps du calcul local (8,2 s), à logits identiques |
docs/roadmap.md:263:de 12 couches prend 15,9 ms par jeton, l'attente du pair 16,1 ms — soit **1,01×**.
docs/roadmap.md:264:Le banc réparti entier (8,3 s) prend le temps du calcul local (8,2 s), à logits
docs/roadmap.md:265:identiques. Avant `TCP_NODELAY`, cette attente était de 97,6 ms (6,26×) : le
reports/rapport-mur-memoire-4bits.md:112:| 4 bits **attention** | 18,3503 | +5,4 % | 24,5 | 27,0 |
reports/rapport-transport-liste.md:190:| calcul local (12 couches) | 15,6 ms/jeton | 15,9 ms/jeton |
reports/rapport-tran
… [310 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 45, "offset": 40}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
40:     // dit, plutôt que de laisser croire que l'option est active.
41:     if let Some((vieux, _)) = std::env::vars().find(|(k, _)| k.starts_with("QT_")) {
42:         eprintln!("[attention] {vieux} est l'ancien nom d'une variable d'environnement : \
43: elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.");
44:     }
45:     let opt = analyser(&args);
46:     let _ = MODELE.set(args[1].clone());
47:     // Plusieurs modes demandés : l'aiguillage en retient UN, dans un ordre
48:     // arbitraire, et le disait pas. On le dit.
49:     let modes: Vec<&str> = [
50:         (opt.banc_vision.is_some(), "--banc-vision"),
51:         (opt.flux_serveur.is_some(), "--flux-serveur"),
52:         (opt.ppl_reparti.is_some(), "--ppl-reparti"),
53:         (opt.tensors, "--tensors"), (opt.banc_mla.is_some(), "--banc-mla"),
54:         (opt.banc_kv > 0, "--banc-kv"), (opt.gpu_banc, "--gpu-banc"),
55:         (opt.plan, "--plan"), (opt.tokenize, "--tokenize"),
56:         (opt.ppl, "--ppl"), (opt.infer, "--infer"),
57:     ].iter().filter(|(v, _)| *v).
… [1764 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'i += \\|i +=2\\|avale\\|pas de 2\\|defaut' drave-core/src/main.rs | head -20", "description": "Vérifier la boucle par défaut"}`

  ```
80:    // Pas de 2 SEULEMENT devant un drapeau qui prend une valeur : un pas de 2
87:            "--matrix" if i + 1 < args.len() => { matrix = args[i + 1].clone(); i += 2; }
89:                n_threads = args[i + 1].parse().unwrap_or(n_threads); i += 2;
91:            _ => i += 1,
426:/// l'argument suivant (`i += 2`) ; les drapeaux booléens non (`i += 1`).
444:        // drapeau booléen, 2 pour un drapeau à valeur). Un `i += 2` global
545:        i += pas;
2699:            i += n;
2739:        i += n;
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 45, "offset": 1590}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1590:         }
1591:         MODE_BLOCS => {
1592:             // corps : nombre de blocs u32 · blocs × f32 · n × (u16 · i8)
1593:             let mut nb = [0u8; 4];
1594:             s.read_exact(&mut nb)?;
1595:             let n_blocs = u32::from_le_bytes(nb) as usize;
1596:             let mut eb = vec![0u8; n_blocs * 4];
1597:             s.read_exact(&mut eb)?;
1598:             let echelles = (0..n_blocs).map(|k| f32::from_le_bytes(
1599:                 [eb[k*4], eb[k*4+1], eb[k*4+2], eb[k*4+3]])).collect();
1600:             let mut lg = [0u8; 4];
1601:             s.read_exact(&mut lg)?;
1602:             let longueur = u32::from_le_bytes(lg) as usize;
1603:             let mut corps = vec![0u8; longueur];
1604:             s.read_exact(&mut corps)?;
1605:             let mut idx = Vec::with_capacity(n);
1606:             let mut val = Vec::with_capacity(n);
1607:             let mut prev = 0u32;
1608:             let mut lus = 0usize;
1609:             let mut echappements = 0usize;
1610:             while idx.len() < n {
1611:                 if lus + 1 >= co
… [1199 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'to_le_bytes()\\[..2\\]\\|extend_from_slice(&i.to_le_bytes())' drave-core/src/*.rs", "description": "Comparer les échappements écrits"}`

  ```
drave-core/src/main.rs:1457:                paires.extend_from_slice(&i.to_le_bytes());
drave-core/src/main.rs:1473:            c.extend_from_slice(&i.to_le_bytes());
drave-core/src/model.rs:605:                    c.extend_from_slice(&i.to_le_bytes()[..2]);
drave-core/src/model.rs:621:                    c.extend_from_slice(&i.to_le_bytes());
drave-core/src/model.rs:628:                        c.extend_from_slice(&i.to_le_bytes()[..2]);
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 80, "offset": 558}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
558: 
559:     /// Une liste : ce qui est réellement poussé dans la couche.
560:     ///
561:     /// Le corps est construit AVANT l'en-tête, parce que chaque version a son
562:     /// compte : `n` est le nombre d'entiers i16 (v1/v2) ou de valeurs i8 (v3), et
563:     /// la v3 ajoute ses échelles de bloc. Écrire l'en-tête d'abord obligeait à
564:     /// connaître les deux comptes — et la première version de ce code les
565:     /// écrivait tous les deux, décalant tout le fichier de huit octets.
566:     pub fn ecrire(&mut self, couche: usize, pos: usize, actifs: &[i32], echelle: f32) {
567:         use std::io::Write;
568:         if !self.couches.is_empty() && !self.couches.contains(&couche) { return; }
569: 
570:         let (n, ech_liste, corps): (u32, f32, Vec<u8>) = if self.version == 3 {
571:             // v3 : une échelle f16 par bloc de 32 canaux, valeurs i8. L'échelle
572:             // par bloc borne l'erreur RELATIVE (celle par vecteur borne l'absolue,
573:             // catastrophique sur les canaux faibles) et permet un octet par valeur.
574:         
… [3105 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'version != 1\\|lit la\\|version == 3\\|listes_blocs' drave-core/src/model.rs | head -20", "description": "Vérifier le lecteur de trace v3"}`

  ```
570:        let (n, ech_liste, corps): (u32, f32, Vec<u8>) = if self.version == 3 {
642:        let octets_par_actif = if self.version == 3 { 2 } else if self.version == 1 { 6 } else { 3 };
643:        let octets_echelles = if self.version == 3 {
672:    pub listes_blocs: std::collections::HashMap<(u16, u32), Vec<(u32, f32)>>,
691:        if version != 1 && version != 2 && version != 3 {
693:                format!("trace DRVF en version {version} : ce lecteur lit la 1, la 2 et la 3")));
696:        let mut listes_blocs = std::collections::HashMap::new();
708:            if version == 3 {
736:                listes_blocs.insert((couche, pos), paires3);
769:        Ok(FluxRelecteur { listes, listes_blocs, servies: 0, manquantes: 0 })
776:        if let Some(paires) = self.listes_blocs.get(&cle) {
1240:    /// miroir VRAM. Aucune conversion : le noyau lit la même disposition que le
2789:                } else if r.listes_blocs.contains_key(&((base + l) as u16, j0 as u32)) {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '660,760p' drave-core/src/model.rs", "description": "Lire la suite du lecteur de flux"}`

  ```
/// recevoir pour continuer le calcul, on sait déjà l'écrire — ici, on apprend à
/// le RELIRE et à repartir de là.
pub struct FluxRelecteur {
    /// (couche, position) -> (échelle, indices/valeurs)
    /// (couche, jeton global) → (échelle, paires) pour les versions 1 et 2 : les
    /// ENTIERS d'origine sont conservés, parce que le rejeu par LOTS les réinjecte
    /// tels quels (chemin exact, sans déquantifier-requantifier).
    pub listes: std::collections::HashMap<(u16, u32), (f32, Vec<(u32, i16)>)>,
    /// Version 3 : les valeurs sont des f32 (i8 × échelle f16 de bloc), il n'y a
    /// plus d'entiers d'origine. Le rejeu JETON PAR JETON les accepte ; le rejeu
    /// par lots, non — et il le dira au lieu de compter des listes manquantes
    /// sans explication.
    pub listes_blocs: std::collections::HashMap<(u16, u32), Vec<(u32, f32)>>,
    pub servies: u64,
    pub manquantes: u64,
}

impl FluxRelecteur {
    pub fn lire(chemin: &str) -> std::io::Result<Self> {
        use std::io::Read;
        let mut f = std::fs::File::open(chemin)?;
        // En-tête : magie (4) + version (2) + n_layer (4) + hidden (4) = 14 octets.
        // Lire 16 décalait tout de deux octets et 
… [4143 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show b97d129 -- README.md | head -60", "description": "Voir le diff du renommage sur README"}`

  ```
commit b97d1290302a9b3fb0e428d06a7918eada883072
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 08:48:19 2026 -0400

    Drave : renommage complet (crate, binaire, variables, documents)
    
    Le projet s'appelait Qtrinet du nom de son origine — inférence ternaire sur un
    cluster de cartes Stratix V. Ce nom racontait le premier âge ; le projet est
    devenu autre chose : un moteur qui pousse des listes d'activation.
    
    * crate `qtrinet-core/` -> `drave-core/`, paquet `drave-core`, binaire **`drave`** ;
    * noyaux `gpu/qtrinet_gpu.{cu,ptx}` -> `gpu/drave_gpu.{cu,ptx}` ;
    * variables d'environnement `QT_*` -> **`DRAVE_*`**, SANS alias — mais le moteur
      prévient quand il voit un ancien nom au lieu de laisser croire qu'une option
      est active ;
    * « Qtrinet » -> « Drave » dans les rapports et les documents (61 fichiers de
      contenu), chemins de scripts compris.
    
    PRÉSERVÉ volontairement : le journal de sessions (un journal réécrit n'est plus un
    journal), `Qtrinet-bootstrap.md` (le cahier des charges d'origine, pièce datée), et
    l'historique Git.
    
    `docs/histoire.md` porte l'histoire des trois âges du projet et la table de
 
… [1736 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"Anciennement\\|s'appelait\\|changera dans un commit\\|ancien nom\" README.md REPRISE.md docs/*.md reports/*.md | head -20", "description": "Traquer les phrases cassées par le renommage"}`

  ```
README.md:3:*Anciennement `Drave`.* **La drave**, c'est le flux qu'on conduit : ici, celui
docs/histoire.md:77:question « pourquoi ce projet s'appelait-il Qtrinet ? » ait une réponse, et pour
docs/vision.md:14:Le projet s'appelait `Drave`, du nom de son origine : un cahier des charges
reports/rapport-drapeaux-ignores.md:114:| `QT_*` (anciens noms) | Avertissement main.rs:41-44 | **Faux positif** : toute variable d'environnement commençant par `QT_` (ex. `QT_IM_SWITCHER`, présent dans l'environnement de test) déclenche « ancien nom d'une variable : rien n'a été appliqué » | 🟡 |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'Qtrinet' README.md docs/*.md REPRISE.md reports/*.md | head -20", "description": "Voir les mentions restantes de Qtrinet"}`

  ```
README.md:10:Le cahier des charges d'origine est dans [`Qtrinet-bootstrap.md`](Qtrinet-bootstrap.md)
README.md:449:Qtrinet-bootstrap.md    cahier des charges d'origine (à lire avec les écarts ci-dessus)
docs/histoire.md:11:| **Qtrinet** (origine) | inférence de LLM en ternaire / multi-bits sur un cluster de cartes **Stratix V** (Microsoft Storey Peak), 100 % logique, sans DSP. Le cahier des charges d'origine est **conservé tel quel** : [`Qtrinet-bootstrap.md`](../Qtrinet-bootstrap.md) — c'est un document daté, il n'est pas réécrit | `Qtrinet-bootstrap.md`, `README.md` §« Écarts avec le CDC » |
docs/histoire.md:15:Le nom **Qtrinet** appartenait au premier âge : il évoquait un réseau ternaire, une
docs/histoire.md:36:| « Qtrinet » dans les rapports et les documents | « Drave » |
docs/histoire.md:42:* `Qtrinet-bootstrap.md` — le cahier des charges d'origine, tel quel ;
docs/histoire.md:77:question « pourquoi ce projet s'appelait-il Qtrinet ? » ait une réponse, et pour
docs/vision.md:16:(`Qtrinet-bootstrap.md`). Ce cahier des charges reste l'acte de naissance ; le
docs/vision.md:235:`Qtrinet-bootstrap.md` (une pièce datée), et l'**historique Git**.
docs/vision.md:239:Qtrinet ternaire d
… [318 caractères tronqués]
  ```

- **bash** `{"command": "ls -d /home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V 2>/dev/null; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --all --oneline --diff-filter=D -- 'reports/rapport-pe-evenementiel.md' 'reports/rapport-lecteur-ddr3.md' | head; git log --all --oneline -- 'reports/r … [106 caractères tronqués]`

  ```
/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'pe-evenementiel\\|lecteur-ddr3\\|pack_lists' README.md docs/*.md reports/*.md | head", "description": "Voir tous les renvois vers ces rapports"}`

  ```
README.md:29:| **PE événementiel vérifié et synthétisé (Stratix V)** | ✅ **fait** → [`reports/rapport-pe-evenementiel.md`](reports/rapport-pe-evenementiel.md) |
README.md:30:| **Lecteur DDR3 vérifié de bout en bout** | ✅ **fait** → [`reports/rapport-lecteur-ddr3.md`](reports/rapport-lecteur-ddr3.md) |
docs/vision.md:109:(`reports/rapport-pe-evenementiel.md`), et le bilan multi-matériel
reports/bilan-multi-materiel.md:149:python3 tools/pack_lists.py <modele.gguf> blk.0.ffn_gate.weight --sources 64 --out sim
  ```

- **bash** `{"command": "ls /home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V 2>/dev/null | head -20; find /home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V -name 'rapport-pe-evenementiel.md' -o -name 'rapport-lecteur-ddr3.md' 2>/dev/null | head", "description": "Chercher les rapports dans le dépôt FP … [4 caractères tronqués]`

  ```
device
docs
qsf
README.md
rtl
sim
syn
tb
tools
/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/docs/rapport-pe-evenementiel.md
/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/docs/rapport-lecteur-ddr3.md
  ```

- **bash** `{"command": "ls -la /tmp/flux_*.bin /tmp/wt2_txt.txt /tmp/ids_qwen.txt /tmp/ids_oss.txt 2>&1 | head -20", "description": "Vérifier les artefacts de mesure cités"}`

  ```
-rw-r--r--. 1 stephane stephane  66197668 30 sep 10:11 /tmp/flux_256.bin
-rw-r--r--. 1 stephane stephane   5497746 30 sep 10:00 /tmp/flux_c8.bin
-rw-r--r--. 1 stephane stephane 132396736 30 sep 09:59 /tmp/flux_f32.bin
-rw-r--r--. 1 stephane stephane 132396736 30 sep 10:12 /tmp/flux_g.bin
-rw-r--r--. 1 stephane stephane 132396464 30 sep 08:57 /tmp/flux_i8.bin
-rw-r--r--. 1 stephane stephane  66198208 30 sep 10:16 /tmp/flux_lot.bin
-rw-r--r--. 1 stephane stephane  53092562 30 sep 09:01 /tmp/flux_sparse.bin
-rw-r--r--. 1 stephane stephane  66370408 30 sep 12:25 /tmp/flux_v2b.bin
-rw-r--r--. 1 stephane stephane  66370408 30 sep 12:13 /tmp/flux_v2.bin
-rw-r--r--. 1 stephane stephane  16318016 30 sep 12:25 /tmp/flux_v3.bin
-rw-r--r--. 1 stephane stephane     21489 28 sep 11:32 /tmp/ids_oss.txt
-rw-r--r--. 1 stephane stephane     21380 28 sep 11:30 /tmp/ids_qwen.txt
-rw-r--r--. 1 stephane stephane     20000 28 sep 11:30 /tmp/wt2_txt.txt
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls drave-core/target/release/drave 2>/dev/null && ls models/ 2>/dev/null && ls data/ 2>/dev/null", "description": "Vérifier le binaire et les modèles"}`

  ```
drave-core/target/release/drave
Qwen2.5-0.5B-Q4_0.gguf
Qwen2.5-0.5B-Q8_0.gguf
wikitext2_test.txt
wt2.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport sys\nsys.path.insert(0,'tools')\nimport flux_codec\nd=open('/tmp/flux_v2.bin','rb').read(14)\nprint('magie',d[:4],'version',int.from_bytes(d[4:6],'little'),'n_layer',int.from_bytes(d[6:10],'little'),'hidden',int … [375 caractères tronqués]`

  ```
magie b'DRVF' version 2 n_layer 24 hidden 896
taille 66370408
magie b'DRVF' version 3 n_layer 24 hidden 896
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'def lire\\|def lire_listes\\|version' tools/flux_codec.py | head -20", "description": "Voir l'API de flux_codec"}`

  ```
11:    en-tête   "DRVF" · u16 version · u32 n_layer · u32 hidden
39:def encoder(n_layer, hidden, listes, version=VERSION):
41:    out = bytearray(ENTETE.pack(MAGIE, version, n_layer, hidden))
46:            if version == 1:
60:    magie, version, n_layer, hidden = ENTETE.unpack_from(blob, 0)
62:    assert version in (1, 2), f"version {version} inconnue (ce lecteur lit la 1 et la 2)"
76:            if version == 1:
95:def lire_rust(chemin):
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 120 python3 -c \"\nimport sys; sys.path.insert(0,'tools')\nimport flux_codec\nr=flux_codec.lire_rust('/tmp/flux_v2.bin')\nif isinstance(r,dict):\n    n=len(r); act=sum(len(v[1]) for v in r.values())\n    print('listes',n,'act … [152 caractères tronqués]`

  ```
<class 'tuple'> 4
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '90,130p' tools/flux_codec.py", "description": "Lire la fonction lire_rust"}`

  ```
actifs.append((i, v))
        listes.append((couche, pos, echelle, actifs))
    return n_layer, hidden, listes


def lire_rust(chemin):
    """Lit le fichier écrit par le moteur, sans le ré-encoder."""
    with open(chemin, "rb") as f:
        blob = f.read()
    n_layer, hidden, listes = decoder(blob)
    return n_layer, hidden, listes, blob


def main():
    chemin = sys.argv[1]
    n_layer, hidden, listes, blob = lire_rust(chemin)
    n_actifs = sum(len(a) for _, _, _, a in listes)
    jetons = len({p for _, p, _, _ in listes})
    print(f"{chemin}")
    print(f"  {len(listes)} listes · {jetons} jetons · {n_layer} couches · {hidden} cachés")
    print(f"  {len(blob)} octets · {len(blob)/max(1,jetons)/1024:.1f} ko par jeton "
          f"· {len(blob)/max(1,n_actifs):.2f} octet par neurone actif")

    t0 = time.time()
    blob2 = encoder(n_layer, hidden, listes)
    t_enc = time.time() - t0
    t0 = time.time()
    n2, h2, listes2 = decoder(blob2)
    t_dec = time.time() - t0
    identique = (blob2 == blob) and (listes2 == listes)
    print(f"  aller-retour : {'IDENTIQUE' if identique else 'DIFFÉRENT'} "
          f"({len(blob2)} octets réencodés)")
    mb = len(blob) / 1e6
    p
… [284 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 180 python3 tools/flux_codec.py /tmp/flux_v2.bin 2>&1 | head -8", "description": "Valider les comptes de la trace v2"}`

  ```
(no output)
[timed out after 60000ms]
[killed by signal: SIGTERM]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '411\\|494\\|364\\|384\\|450\\|287\\|219' REPRISE.md docs/contexte-long.md reports/rapport-attribution-kv.md reports/rapport-passage-a-l-echelle.md 2>/dev/null | grep -i 'llama\\|int4\\|%' | head -25", "description": "Compar … [25 caractères tronqués]`

  ```
REPRISE.md:147:| 3 | KV int8 puis int4 | **fait, jusqu'à 8 192** | **échelles par bloc de 32** : int8 +**1,5 %** à 512 (était +7,1 %), **+3,0 % à 8 192** (llama.cpp +0,8 %) ; int4 **+364 % à 8 192** contre +494 % pour llama.cpp — meilleur que la référence, et 1 M tient en int4 (9,7 Go). Prix caché : la passe coûte 864 s (f32) / 1 144 (int8) / 1 461 (int4), la déquantification par élément — c'est ce que le noyau GPU de E4 supprime |
REPRISE.md:169:| KV int4, échelles par bloc | +219 % (512) et +287 % (4 591) — était +384 % et +450 % |
REPRISE.md:170:| KV à 8 192 jetons (longueur de la référence llama.cpp) | f32 **14,2339** · int8 **14,6667 (+3,0 %)** contre +0,8 % chez llama.cpp · int4 **66,0369 (+364 %)** contre +494 % chez llama.cpp |
REPRISE.md:233:| `DRAVE_KV_BITS=8` ou `4` | quantifie le cache KV (défaut f32) | le 4 bits coûte +364 % de perplexité à 8 192 |
docs/contexte-long.md:103:| E3 | **KV int4** | **fait** (nibbles empaquetés) | 1 M tient en RAM (9,7 Go) et en VRAM | mesuré : **+384 %** — llama.cpp q4_0 : +411 % ; à réserver aux cas où la mémoire manque |
docs/contexte-long.md:125:| **int4** | **63,61** (+384 %) | 72,80 (+411 %) | **71,05** (+450 %) | 98,53 (+494 %) |
doc
… [294 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '19,3045\\|19.3045\\|19,3885\\|21,0110\\|12,9228\\|10,9947\\|7,6139\\|20,8361\\|15,1757\\|174,3375\\|15,0757\\|18,5803' REPRISE.md reports/*.md README.md docs/*.md | grep -v '^REPRISE.md:5[0-9]:\\|^REPRISE.md:6[0-9]:' | head … [62 caractères tronqués]`

  ```
REPRISE.md:171:| porte gpt-oss selon l'ouverture du pilote | sans `DRAVE_GPU` : **15,1757** · avec `DRAVE_GPU=1` : **15,1667** — l'écart vient du déport automatique des projections Q8_0 (> 8 Mo), pas d'une régression |
REPRISE.md:242:0,06 % (15,1757 → 15,1667 sur gpt-oss).
REPRISE.md:347:    --ctx 256 --abits 16 --threads 16 --limit 512 --dense   # attendu 19,3885
REPRISE.md:356:    --ppl /tmp/ids_oss.txt --ctx 256 --dense --threads 16 --limit 512   # attendu 15,1757
reports/rapport-compacite-trace.md:6:> **identique** (perplexité 19,3885 dans les deux cas), et la relecture par
reports/rapport-compacite-trace.md:11:> silence avec une perplexité fausse (1958,72 au lieu de 19,3885).
reports/rapport-compacite-trace.md:226:   réinjecte, et le contrat est « mêmes logits » (perplexité **19,3885** avec et
reports/rapport-gpt-oss-perplexite.md:60:gpt-oss** : 20,8361 avant, 20,8361 après, au chiffre près. Elle protégera les
reports/rapport-gpt-oss-perplexite.md:175:complète. Le contrôle de non-régression Qwen ne bouge pas (19,3885).
reports/rapport-prefill-par-lots.md:33:endroit. **Effet mesuré : nul** sur Qwen3-30B-A3B (7,6139 avant comme après — ce
reports/rapport-prefill-par-lots.md:197:
… [1760 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn '19,30\\|19\\.30\\|6 bits' reports/rapport-8bits.md reports/rapport-precision.md REPRISE.md docs/convertisseur.md 2>/dev/null | head -15", "description": "Chercher la source du 6 bits 19,3045"}`

  ```
REPRISE.md:53:| Qwen2.5-0.5B Q8_0, 6 bits | `--dense --bits-attn 6 --bits-ffn 6 --limit 512` | **19,3045** ← bat l'int8 |
REPRISE.md:90:| Encodages | listes d'événements (push), dense int8 par ligne, dense 4 bits par bloc, **6 bits empaqueté par bloc** |
REPRISE.md:129:   réel donne 19,30.
REPRISE.md:149:| 5 | échelles par bloc pour `DenseQ8` | **fait, hypothèse réfutée** | 23,696 contre 23,612 : les échelles par bloc n'apportent rien ; l'avantage du 6 bits est son coût (25 % d'octets en moins à qualité égale) |
docs/convertisseur.md:24:sur 16 bits relatifs (erreur 1/32767), l'emprunt lit l'échelle d'origine. **La
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -30 reports/rapport-8bits.md", "description": "Lire le rapport 8 bits"}`

  ```
# Drave — 8 bits : la perfection est-elle atteignable ?

Modèle : **qwen2** en Q8_0, 494.0 M poids analysés.

## 1. Distribution des niveaux

- densité : **99.2 %**
- niveaux distincts : **256** (sur 256 possibles)
- `E[|v|]` : **42.79**
- `E[popcount(|v|)]` : **3.13**
- niveaux les plus fréquents : `127` (1.6 %), `-127` (1.6 %), `2` (0.8 %), `-1` (0.8 %), `1` (0.8 %), `3` (0.8 %), `0` (0.8 %), `-2` (0.8 %)

## 2. Bits réellement nécessaires (sans perte)

| Codage | bits/poids | Gain |
|---|---|---|
| positionnel fixe | 8,000 | ×1,000 |
| **entropie de la source** | **7.648** | **×1.046** |
| **code de Huffman réel** | **7.671** | **×1.043** |

## 3. Encodages structurels

| Stratégie | bits/poids | opérations/poids |
|---|---|---|
| positionnel (8 bits) | 8,00 | 0.99 |
| plans denses (7 plans + signe) | 8,00 | 3.10 |
| unaire (répétition) | 42.45 | 42.45 |
| **Huffman (sans perte)** | **7.67** | 0.99 |

## 4. Sur le modèle entier
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln 'bits-attn\\|bits-ffn' reports/ docs/ README.md REPRISE.md | head; echo \"---\"; grep -rn 'bits-attn' reports/*.md docs/*.md | head -10", "description": "Chercher les mesures 6 bits"}`

  ```
reports/rapport-drapeaux-ignores.md
REPRISE.md
---
reports/rapport-drapeaux-ignores.md:58:| `--q4` `--q4-ffn` `--q4-attn` `--q4-tout` `--bits-attn` `--bits-ffn` | I (550) · P (2707) · BM : `--dense` seul (1835) | **FS (1575) et PR (1675)** passent `dense=true, auto=false, q4=0, b6=0` en dur : `--q4 --ppl-reparti` mesure un modèle non quantifié en 4 bits | 🔴 |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls src/ && ls bench/ && ls data/ && ls gpu 2>/dev/null", "description": "Vérifier les chemins de la structure du README"}`

  ```
bpe_np.py
encoding.py
gguf_min.py
__pycache__
roofline.py
sparsity.py
ternary.py
tiny_model.py
transformer_np.py
cpu_aer.c
cpu_merge.c
wikitext2_test.txt
wt2.json
[exit code: 2]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'gpu/drave_gpu\\|src/ternary.py\\|src/tiny_model.py\\|src/roofline.py\\|bench/cpu_aer.c\\|bench/cpu_merge.c' README.md REPRISE.md docs/*.md reports/*.md | head -15", "description": "Vérifier les renvois de structure"}`

  ```
README.md:194:## Architecture « push » (AER) et exécution CPU (`run_cpu.py`, `bench/cpu_aer.c`)
README.md:206:**Mesures C/OpenMP sur ce bi-Xeon (`bench/cpu_aer.c`, 16 threads) :**
README.md:241:## Tri et dédoublonnage des contributions (`bench/cpu_merge.c`)
README.md:450:src/ternary.py          quantification ternaire/multi-bits, plans, encodages, MAC entier
README.md:451:src/tiny_model.py       MLP minimal + entraînement numpy (aucune dépendance ML)
README.md:452:src/roofline.py         projection matérielle (constantes mesurées de la carte)
REPRISE.md:323:gpu/drave_gpu.cu + .ptx    noyaux, compilés par clang
docs/histoire.md:34:| noyaux `gpu/qtrinet_gpu.cu` / `.ptx` | `gpu/drave_gpu.cu` / `.ptx` |
reports/rapport-cpu-aer.md:20:## Limites mesurées du CPU (bench/cpu_aer.c, 16 threads)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && find . -name 'drave_gpu*' -o -name '*.cu' -o -name '*.ptx' 2>/dev/null | grep -v target | head", "description": "Localiser les noyaux GPU"}`

  ```
./drave-core/gpu/drave_gpu.cu
./drave-core/gpu/drave_gpu.ptx
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'drave_gpu\\|include_str!\\|\\.ptx' drave-core/src/gpu.rs | head -10", "description": "Voir comment gpu.rs charge les noyaux"}`

  ```
38:/// PTX compilé depuis `gpu/drave_gpu.cu` par clang.
39:const PTX: &str = include_str!("../gpu/drave_gpu.ptx");
  ```

- **bash** `{"command": "ls /home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/ 2>/dev/null | head -20; find /home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V -name 'pack_lists.py' -o -name 'quartus_env.sh' 2>/dev/null | head", "description": "Chercher les outils FPGA cités"}`

  ```
fetch_reference_design.sh
gen_events.py
host_check.sh
install_license.sh
jtag_program_svf.sh
jtag_scan.sh
pack_lists.py
quartus_env.sh
setup_compat_libs.sh
/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/quartus_env.sh
/home/stephane/Data13TB/stephane/GitHub/FPGA-Stratix-V/tools/pack_lists.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'sources 64\\|pack_lists' reports/bilan-multi-materiel.md | head -5 && sed -n '140,155p' reports/bilan-multi-materiel.md", "description": "Voir le contexte des outils FPGA"}`

  ```
149:python3 tools/pack_lists.py <modele.gguf> blk.0.ffn_gate.weight --sources 64 --out sim
# CPU
cd drave-core && cargo build --release
./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf \
    --infer --ids 9707,0 --n 16 --threads 16 --abits 16
./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf --threads 16   # banc des décodeurs

# FPGA (aucune licence)
export PATH=$HOME/iverilog/bin:$PATH
cd ../FPGA-Stratix-V
python3 tools/pack_lists.py <modele.gguf> blk.0.ffn_gate.weight --sources 64 --out sim
iverilog -g2012 -o /tmp/sim_rd rtl/event_reader.sv rtl/event_pe.sv tb/ddr3_model.sv tb/tb_event_reader.sv
vvp /tmp/sim_rd
source tools/quartus_env.sh && quartus_sh --flow compile syn/reader/event_reader
```
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 25c42c3 | head -80", "description": "Voir le commit sur les silences"}`

  ```
commit 25c42c3857c615fa78583f10af3ccc39fb53d1aa
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 12:19:13 2026 -0400

    Deux silences de plus, relevés par l'audit : trace en inférence, modes concurrents
    
    1. **`--trace-flux` en `--infer`** ne produisait rien, sans un mot. Il est
       maintenant branché comme en perplexité (une trace est un enregistrement du
       flux, elle n'a rien de spécifique à la mesure) — vérifié : 775 850 octets
       écrits pour deux jetons.
    2. **Plusieurs modes demandés** : l'aiguillage en retenait un seul, dans un ordre
       arbitraire, en silence. Il le dit maintenant :
       `[modes] 2 modes demandés (--tensors, --ppl) : c'est --tensors qui s'exécute`.
    
    Porte Qwen après coup : 19,3885, inchangée.

diff --git a/drave-core/src/main.rs b/drave-core/src/main.rs
index f4c7f71..2adf53b 100644
--- a/drave-core/src/main.rs
+++ b/drave-core/src/main.rs
@@ -44,6 +44,21 @@ elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été app
     }
     let opt = analyser(&args);
     let _ = MODELE.set(args[1].clone());
+    // Plusieurs modes demandés : l'aiguillage en retient UN, dans un ordre
+    // arbitraire, et 
… [3335 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -oE '\"--[a-zA-Z0-9-]+\"' drave-core/src/main.rs | sort -u | wc -l", "description": "Compter les drapeaux du code"}`

  ```
84
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\n# Vérifications arithmétiques pour le rapport\nprint(\"TAILLE_TETE:\", 4+1+1+4+4+4+4+4+4+4+4+1+4+4+4+7*4)\nprint(\"dense 79 + 896*4 =\", 79+896*4)\nprint(\"lot 256:\", 79+256*896*4)\nprint(\"lot 256 (39):\", 39+256 … [226 caractères tronqués]`

  ```
TAILLE_TETE: 79
dense 79 + 896*4 = 3663
lot 256: 917583
lot 256 (39): 917543
blocs 68% ecarts: 1419
blocs 68% u16: 1989
1 568 + 40 = 1608
1 989 + 40 = 2029
  ```

### 🤖 Assistant

⏵ Rédaction du rapport de cohérence documentaire

J'ai terminé les vérifications. J'écris maintenant le livrable.

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "content": "# Cohérence des documents avec le code — audit\n\n**En une ligne** : 56 affirmations vérifiées une par une contre le code (et contre les\ntraces réelles du disque) ; **13 sont fausses (PÉRI … [23937 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -c '^| [0-9]' reports/rapport-coherence-docs.md; echo \"--- par verdict ---\"; for v in PÉRIMÉ CONTRADICTIOIRE MANQUANT OK; do printf \"%s: \" \"$v\"; grep -c \"| $v\" reports/rapport-coherence-docs.md; done; echo \"--- OK avec  … [128 caractères tronqués]`

  ```
80
--- par verdict ---
PÉRIMÉ: 37
CONTRADICTIOIRE: 10
MANQUANT: 13
OK: 15
--- OK avec précision ---
63:| 18 | `docs/format-flux.md:86` | mode 2 = `n_blocs u32 · n_blocs × f32 · longueur u32 · paires` | conforme à l'émetteur (main.rs:1446-1466) et au récepteur (1591-1628) | OK |
64:| 19 | `docs/format-flux.md:87` | mode 3 = `n × dimension × f32`, `n` = états | conforme (`envoyer_lot`, main.rs:1512-1544) | OK |
70:| 25 | `docs/format-flux.md:124-131` | règle « qui applique la norme finale » (`flux_brut`) | `flux_brut` existe et le serveur le pose (main.rs:1695) | OK |
71:| 26 | `docs/colab-reparti.md:26`, `REPRISE.md:265` | `--flux-serveur` accepte `hôte:port` | `rsplit_once(':')` (main.rs:1659-1662) | OK |
87:| 37 | `docs/format-flux.md:142` | « 1 lot de 256 : 0,00e0 (**918 ko** sur le fil) » | 917 583 o ≈ 918 ko (arrondi décimal) | OK |
88:| 38 | `docs/format-flux.md:45`, `reports/rapport-compacite-trace.md:5,92` | trace dense 512 j : 132 396 736 → **66 370 408** (−49,87 %) | `/tmp/flux_v2.bin` = exactement 66 370 408 octets, version 2 | OK |
89:| 39 | `reports/rapport-compacite-trace.md:79,126` | « écarts + i16 = **66 370 406** » | 66 370 408 avec la sentinelle de fin (2 o), 406 s
… [1697 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -oE '\\| (PÉRIMÉ|CONTRADICTIOIRE|MANQUANT|OK)( \\([^)]*\\))? \\|$' reports/rapport-coherence-docs.md | sed 's/| //; s/ |//' | sort | uniq -c | sort -rn", "description": "Compter les verdicts en fin de ligne"}`

  ```
37 PÉRIMÉ
     13 OK
     12 MANQUANT
     10 CONTRADICTIOIRE
      1 OK (source)
      1 OK (2 o)
      1 MANQUANT (précision)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -nE '^\\[?[0-9]+ \\|' reports/rapport-coherence-docs.md | grep -vE '\\| (PÉRIMÉ|CONTRADICTIOIRE|MANQUANT|OK)' | head -20; echo \"=== lignes numérotées ===\"; grep -cE '^\\| [0-9]+ \\|' reports/rapport-coherence-docs.md", "descri … [42 caractères tronqués]`

  ```
=== lignes numérotées ===
80
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk -F'|' '/^\\| [0-9]+ \\|/ {v=$(NF-1); gsub(/^ +| +$/,\"\",v); print v}' reports/rapport-coherence-docs.md | sort | uniq -c | sort -rn", "description": "Compter les verdicts avec awk"}`

  ```
37 PÉRIMÉ
     13 OK
     12 MANQUANT
     10 CONTRADICTIOIRE
      5 CONTRADICTOIRE
      1 OK (source)
      1 OK (2 o)
      1 MANQUANT (précision)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -i 's/CONTRADICTIOIRE/CONTRADICTOIRE/g' reports/rapport-coherence-docs.md && awk -F'|' '/^\\| [0-9]+ \\|/ {v=$(NF-1); gsub(/^ +| +$/,\"\",v); print v}' reports/rapport-coherence-docs.md | sort | uniq -c | sort -rn", "description" … [35 caractères tronqués]`

  ```
37 PÉRIMÉ
     15 CONTRADICTOIRE
     13 OK
     12 MANQUANT
      1 OK (source)
      1 OK (2 o)
      1 MANQUANT (précision)
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "old_string": "**En une ligne** : 56 affirmations vérifiées une par une contre le code (et contre les\ntraces réelles du disque) ; **13 sont fausses (PÉRIMÉ)**, **11 se contredisent entre\ndocuments (C … [919 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "limit": 15}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md</path>
<type>file</type>
<content>
1: # Cohérence des documents avec le code — audit
2: 
3: **En une ligne** : 56 affirmations vérifiées une par une contre le code (et contre les
4: traces réelles du disque) ; **13 sont fausses (PÉRIMÉ)**, **11 se contredisent entre
5: documents (CONTRADICTOIRE)**, **9 existent dans le code et manquent aux documents
6: (MANQUANT)** — les trois plus graves touchent la **version du protocole de flux**,
7: un **échappement d'indice écrit sur 4 octets et lu sur 2**, et `REPRISE.md` §6bis
8: (pourtant écrit il y a une heure) déjà faux sur quatre points.
9: 
10: ## Révision auditée, méthode, réserves
11: 
12: | | |
13: |---|---|
14: | Commit de référence | `a0687b9` (2026-09-30 12:20) |
15: | `drave-core/src/main.rs` | sha256 `d5e90136…` · 3 112 lignes · **3 lignes modifiées non commitées** |

(Showing lines 1-15 of 209. Use offset=16 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "new_string": "**En une ligne** : **80 affirmations** vérifiées une par une contre le code (et\ncontre les traces réelles du disque) ; **37 sont fausses (PÉRIMÉ)**, **15 se\ncontredisent entre document … [919 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "offset": 146, "limit": 65}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md</path>
<type>file</type>
<content>
146: | 79 | `docs/roadmap.md:18` | `tools/profil_flux.py` | présent dans `tools/` | OK |
147: | 80 | `reports/bilan-multi-materiel.md:149,152` | `tools/pack_lists.py`, `tools/quartus_env.sh` | présents dans `../FPGA-Stratix-V/tools/`, après le `cd ../FPGA-Stratix-V` du même bloc : chemins valides | OK |
148: 
149: ---
150: 
151: ## Les 10 corrections à faire, dans l'ordre
152: 
153: 1. **Incrémenter `VERSION_FLUX` à 4** (`main.rs:1295`), ou supprimer le commentaire
154:    « Version 4 » : aujourd'hui deux binaires parlant « 3 » peuvent transporter des
155:    contrats d'activation **différents** (l'un sans les top-k, l'autre avec) et se
156:    croient compatibles — le silence exact que la phase 3.5 et le
157:    `rapport-drapeaux-ignores.md` §8.2 voulaient empêcher.
158: 2. **Corriger l'échappement d'indice du mode blocs réseau** (`main.rs:1457` :
159:    écrire `&i.to_le_bytes()[..2]` comme le fait le disque en `model.rs:605`) : le
160:    récepteur en lit deux octets, l'émetteur en écrit quatre ; toute trame avec un
161:    écart ≥ 255 se désynchronise, et c
… [3767 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "limit": 10, "offset": 204}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md</path>
<type>file</type>
<content>
204:   invalident les chiffres publiés, mais la valeur mesurée reste à produire par
205:   l'agent qui corrigera les documents.
206: * Le contenu de `journal/` (ignoré par consigne) et les documents
207:   `docs/comparaison-spiking.md`, `docs/plan-mla-vision.md`,
208:   `docs/programme-recherche.md`, `docs/convertisseur.md` (survolés par grep
209:   seulement) ; `convertisseur.md:225` est du bon côté du croisement (22 %).
210: * La qualité des réponses du mode vision, qui n'a pas de référence locale
211:   (réserve déjà écrite dans `REPRISE.md` §6).

(End of file - total 211 lines)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "new_string": "* La qualité des réponses du mode vision, qui n'a pas de référence locale\n  (réserve déjà écrite dans `REPRISE.md` §6).\n\n## Récapitulatif\n\n| verdict | nombre | dont les plus visible … [871 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk -F'|' '/^\\| [0-9]+ \\|/ {n=$2; v=$(NF-1); gsub(/^ +| +$/,\"\",v); gsub(/ /,\"\",n); printf \"%s %s\\n\", n, v}' reports/rapport-coherence-docs.md", "description": "Lister chaque affirmation et son verdict"}`

  ```
1 CONTRADICTOIRE
2 CONTRADICTOIRE
3 CONTRADICTOIRE
4 PÉRIMÉ
5 PÉRIMÉ
6 PÉRIMÉ
7 PÉRIMÉ
8 PÉRIMÉ
9 PÉRIMÉ
10 MANQUANT
11 MANQUANT
12 PÉRIMÉ
13 PÉRIMÉ
14 PÉRIMÉ
15 PÉRIMÉ
16 PÉRIMÉ
17 MANQUANT
18 OK
19 OK
20 CONTRADICTOIRE
21 MANQUANT
22 MANQUANT
23 CONTRADICTOIRE
24 MANQUANT
25 OK
26 OK
27 PÉRIMÉ
28 PÉRIMÉ
29 CONTRADICTOIRE
30 PÉRIMÉ
31 PÉRIMÉ
32 PÉRIMÉ
33 PÉRIMÉ
34 CONTRADICTOIRE
35 PÉRIMÉ
36 PÉRIMÉ
37 OK
38 OK
39 OK (2 o)
40 OK (source)
41 PÉRIMÉ
42 MANQUANT (précision)
43 MANQUANT
44 PÉRIMÉ
45 CONTRADICTOIRE
46 CONTRADICTOIRE
47 PÉRIMÉ
48 PÉRIMÉ
49 PÉRIMÉ
50 CONTRADICTOIRE
51 PÉRIMÉ
52 MANQUANT
53 OK
54 OK
55 MANQUANT
56 OK
57 PÉRIMÉ
58 PÉRIMÉ
59 PÉRIMÉ
60 PÉRIMÉ
61 CONTRADICTOIRE
62 PÉRIMÉ
63 PÉRIMÉ
64 CONTRADICTOIRE
65 PÉRIMÉ
66 PÉRIMÉ
67 PÉRIMÉ
68 PÉRIMÉ
69 MANQUANT
70 MANQUANT
71 PÉRIMÉ
72 PÉRIMÉ
73 CONTRADICTOIRE
74 CONTRADICTOIRE
75 CONTRADICTOIRE
76 OK
77 OK
78 MANQUANT
79 OK
80 OK
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "new_string": "## Récapitulatif\n\n| verdict | nombre | principaux foyers |\n|---|---:|---|\n| PÉRIMÉ | **37** | version du format de flux et du disque (6) · nombre de flux à 40 et 1 024 jetons (2) · e … [2153 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "limit": 50}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md</path>
<type>file</type>
<content>
1: # Cohérence des documents avec le code — audit
2: 
3: **En une ligne** : **80 affirmations** vérifiées une par une contre le code (et
4: contre les traces réelles du disque) ; **37 sont fausses (PÉRIMÉ)**, **15 se
5: contredisent entre documents (CONTRADICTOIRE)**, **13 existent dans le code et
6: manquent aux documents (MANQUANT)**, **15 tiennent (OK)** — les trois plus graves
7: touchent la **version du protocole de flux** (deux binaires « v3 » aux contrats
8: différents se croient compatibles), un **échappement d'indice écrit sur 4 octets et
9: lu sur 2** en mode blocs, et `REPRISE.md` §6bis (pourtant écrit il y a une heure)
10: déjà faux sur quatre points.
11: 
12: ## Révision auditée, méthode, réserves
13: 
14: | | |
15: |---|---|
16: | Commit de référence | `a0687b9` (2026-09-30 12:20) |
17: | `drave-core/src/main.rs` | sha256 `d5e90136…` · 3 112 lignes · **3 lignes modifiées non commitées** |
18: | `drave-core/src/model.rs` | sha256 `0a0856cc…` · 3 872 lignes · **165 lignes ajoutées non commitées** (trace v3) |
19: | Traces relues | `/tmp/flux_v2.bin`
… [2981 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short && echo \"---\" && wc -l reports/rapport-coherence-docs.md", "description": "Vérifier l'état git et le fichier livré"}`

  ```
M journal/README.md
?? reports/rapport-coherence-docs.md
---
223 reports/rapport-coherence-docs.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -3 && git show --stat --format='%h %s' HEAD | head -12 && echo \"--- valeurs clés ---\" && grep -n 'const VERSION_FLUX' drave-core/src/main.rs && grep -n 'let version: u16' drave-core/src/model.rs && grep -n 'paires … [126 caractères tronqués]`

  ```
ae85043 DRVF v3 : −66 % de trace au total, pour +0,074 % de perplexité
a0687b9 Colab : notebook prêt à ouvrir + script de préparation
25c42c3 Deux silences de plus, relevés par l'audit : trace en inférence, modes concurrents
ae85043 DRVF v3 : −66 % de trace au total, pour +0,074 % de perplexité

 docs/format-flux.md                                |   16 +
 drave-core/src/main.rs                             |    3 +-
 drave-core/src/model.rs                            |  224 +-
 .../42059fde-f06f-4e2c-9a23-8292d887fb6e/digest.md | 2643 ++++++++++++++++++++
 .../rapport.md                                     |  232 ++
 journal/sessions/MANIFEST.md                       |    6 +-
 .../bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md |  288 +++
 .../rapport.md                                     |   25 +-
 .../bcfe0b97-1795-4610-8e8b-b598ca1ba6cb/digest.md | 1865 ++++++++++++++
 .../rapport.md                                     |  172 ++
--- valeurs clés ---
1295:const VERSION_FLUX: u8 = 3;
549:        let version: u16 = if std::env::var("DRAVE_TRACE_BLOCS").is_ok() { 3 } else { 2 };
1457:                paires.extend_from_slice(&i.to_le_bytes());
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show ae85043 -- docs/format-flux.md", "description": "Voir la mise à jour de format-flux par le commit v3"}`

  ```
commit ae850435f8640f60446f17c46205e52582343db6
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 12:30:38 2026 -0400

    DRVF v3 : −66 % de trace au total, pour +0,074 % de perplexité
    
    `DRAVE_TRACE_BLOCS=1` écrit des valeurs i8 avec une échelle **f16 par bloc de 32
    canaux** — l'échelle par bloc borne l'erreur relative, ce qui autorise un octet
    par valeur. Mesuré sur la même trace dense de 512 jetons :
    
    | | v1 | v2 | v3 |
    |---|---|---|---|
    | octets | 132 396 736 | 66 370 408 | **45 079 930** |
    | rejeu `--flux-forcer` | 19,3885 | 19,3885 | **19,4029** |
    | erreur par valeur | — | nulle | RMS 0,085 % du max |
    
    Soit −65,9 % depuis la v1 pour +0,074 % de perplexité. La v3 est AVEC PERTE, donc
    la v2 reste le défaut ; la v3 est pour les traces qu'on garde longtemps.
    
    Deux choses apprises en la faisant, et écrites dans le code :
    - l'écrivain construisait le corps APRÈS l'en-tête, et écrivait donc deux fois le
      compte (`liste.len()` puis `idx.len()`) : tout le fichier se décalait de huit
      octets et le lecteur refusait la trace. Pire : mon premier « rejeu v3 = 19,3885 »
      était un FAUX POSITIF — la trace n'
… [3086 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'version in' tools/flux_codec.py && sha256sum drave-core/src/main.rs drave-core/src/model.rs && git log -1 --format='%h %ad' --date=format:'%H:%M' && grep -n 'Le lecteur lit' docs/format-flux.md && grep -n 'version' docs/form … [76 caractères tronqués]`

  ```
62:    assert version in (1, 2, 3), f"version {version} inconnue (ce lecteur lit la 1, la 2 et la 3)"
d5e901368718f14fd34a8664631a08f090150ff12df4b7592cf3dcdc919f87cb  drave-core/src/main.rs
3e5dde2d10a4e83dfd710b6c98e7f411a05769a9cec22fbeeb67d583809a72ec  drave-core/src/model.rs
ae85043 12:30
64:Le lecteur lit **les deux versions** ; une version inconnue est refusée en la
20:          version      u16          = 1
28:          puis n_actifs × ( indice u32 · valeur i16 )           [version 1]
29:          puis n_actifs × ( écart u8 · valeur i16 )             [version 2]
43:| | version 1 | version 2 |
54:| | version 2 | version 3 |
64:Le lecteur lit **les deux versions** ; une version inconnue est refusée en la
83:          version      u8           4   (refusée si différente, en le disant)
120:La version est dans **chaque** en-tête, et un pair d'une autre version est refusé
121:avec un message qui nomme les deux versions :
124:[flux] arrêt : flux en version 99, cette build parle la 4 (pair incompatible : rien n'a été interprété)
127:Le passage de la version 2 à la 3 n'est pas cosmétique : un pair en version 2 qui
156:| une version inconnue est refusée | v1/v2/v3 lues, toute autre r
… [81 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "limit": 30, "offset": 52}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md</path>
<type>file</type>
<content>
52: | 10 | `docs/format-flux.md:49` | « Le lecteur lit **les deux versions** [1 et 2] » | le lecteur lit **1, 2 et 3** (model.rs:691-693, version non commitée) — la v3 n'est documentée nulle part | MANQUANT |
53: | 11 | `docs/format-flux.md:137` (invariant « deux implémentations ») | Rust et Python lisent le même fichier | `tools/flux_codec.py:62` refuse encore la v3 (`version in (1, 2)`) : l'invariant ne tient plus pour la trace que le code commence à écrire | MANQUANT |
54: | 12 | `docs/format-flux.md:141` et `docs/roadmap.md:55` | « 40 puis **199 flux** » à 40 et 200 jetons | depuis `2184fc5`, les flux envoyés valent N−1 (le dernier jeton est sauté) : **39** à 40 jetons, 199 à 200 | PÉRIMÉ |
55: | 13 | `REPRISE.md:251`, `docs/roadmap.md:116`, `reports/rapport-phase3-reparti.md:51` | « 1 024 jetons (**1 024 flux**) » | le même correctif `2184fc5` (11:41, **après** ces trois textes) donne **1 023 flux** ; le message du commit dit lui-même « 255 flux au lieu de 256 » à 256 jetons | PÉRIMÉ |
56: 
57: ## 2. En-tête, champs, modes
58: 
59: | # | document | affirma
… [3787 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '100,112p' reports/rapport-coherence-docs.md", "description": "Voir les lignes 100-112 du rapport"}`

  ```
| # | document | affirmation | ce que dit le code / la mesure | verdict |
|---|---|---|---|---|
| 45 | `README.md:34` | « Croisement push/pull à **10 %** de densité ✅ mesuré » | `reports/rapport-croisement-push-pull.md:43` : « **~22 %** … pas à 10 » ; le README lui-même le dit ligne 389 | CONTRADICTOIRE |
| 46 | `docs/vision.md:46,133,198` et `docs/histoire.md:12` | croisement « mesuré » à **10 %** | 22 % (rapport de référence + REPRISE §5.1 + `docs/convertisseur.md:225`) | CONTRADICTOIRE |
| 47 | `README.md:280` | « le moteur tient en **386 lignes** » | 11 440 lignes aujourd'hui (main.rs 3 112, model.rs 3 872) ; 386 était l'état initial (`rapport-optimisations.md:3`) | PÉRIMÉ |
| 48 | `README.md:354` | « **2 319 lignes** de Rust » | idem : chiffre de `rapport-inference.md:3`, dépassé (11 440) | PÉRIMÉ |
| 49 | `REPRISE.md:16` | « ~**5 000** lignes » | 11 440 lignes de `.rs` (dont 6 984 pour main+model) | PÉRIMÉ |
| 50 | `docs/contexte-long.md:103` | E5 attention creuse « **à faire** » | le même document donne les résultats §6 (234,88 contre 298,56) et `REPRISE.md:152` la classe « fait pour E4/E5 » | CONTRADICTOIRE |
| 51 | `docs/contexte-long.md:103` | KV int4 « mesuré : **+384 %*
… [798 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '95,100p' reports/rapport-coherence-docs.md && echo \"===\" && sed -n '130,140p' reports/rapport-coherence-docs.md", "description": "Voir les lignes 44 et 69"}`

  ```
| 43 | `docs/format-flux.md:143` | « `--topk-q 900` contre `--topk-q 4` → 0,00e0 (vérifié) » | la vérification date d'**avant** `d59d061` : à l'époque les top-k n'étaient ni appliqués ni transportés dans les modes flux (`rapport-drapeaux-ignores.md:72`), donc l'égalité était tautologique. Jamais re-mesurée depuis | MANQUANT |
| 44 | `reports/rapport-compacite-trace.md:13-14` | « restent à faire : valeurs i8 (−60,9 %), échelles f16 (−63,5 %), zstd (−79 %) » | la v3 non commitée implémente déjà i8 + échelles f16 par bloc (`model.rs:570-610`) | PÉRIMÉ |

## 4. Autres chiffres (perplexités, densité, tailles)

| # | document | affirmation | ce que dit le code / la mesure | verdict |
===
## 6. Drapeaux, variables, renvois et phrases cassées

| # | document | affirmation | ce que dit le code / la mesure | verdict |
|---|---|---|---|---|
| 67 | `docs/vision.md:69` | `--profil-experts` « quels experts sont choisis (MoE) » | ce drapeau **n'existe pas** ; seuls `--profil-neurones` et `--neurones-sortie` existent | PÉRIMÉ |
| 68 | `docs/plan-prefill-reparti.md:256` | `DRAVE_FLUX_POS=1` imprime `[flux] lot pos …` | variable absente du code | PÉRIMÉ |
| 69 | `model.rs:526,549`, `main.rs` | `DRAV
… [1084 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l drave-core/src/*.rs | tail -3 && wc -l drave-core/src/main.rs drave-core/src/model.rs && git status --short", "description": "Mesurer les fichiers après le commit v3"}`

  ```
3872 drave-core/src/model.rs
   507 drave-core/src/tokenizer.rs
 11449 total
  3112 drave-core/src/main.rs
  3872 drave-core/src/model.rs
  6984 total
 M journal/README.md
?? reports/rapport-coherence-docs.md
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "new_string": "| | |\n|---|---|\n| Commit de référence | `ae85043` (2026-09-30 12:30) |\n| `drave-core/src/main.rs` | sha256 `d5e90136…` · 3 112 lignes |\n| `drave-core/src/model.rs` | sha256 `3e5dde2d … [2560 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "new_string": "| 10 | `docs/format-flux.md:64` | « Le lecteur lit **les deux versions** » | le lecteur lit **1, 2 et 3** (model.rs:691-693) — et le même document l'écrit correctement ligne 156 (« v1/v2 … [803 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "new_string": "| 44 | `reports/rapport-compacite-trace.md:13-14` | « restent à faire : valeurs i8 (−60,9 %), échelles f16 (−63,5 %), zstd (−79 %) » | i8 + échelles f16 par bloc sont **faits et commités … [390 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "new_string": "| 69 | `model.rs:526,549` | `DRAVE_TRACE_BLOCS` (trace v3) | documentée depuis `ae85043` dans `docs/format-flux.md:49` (tableau v2/v3 et invariant ligne 156) — encore absente de `REPRISE … [284 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk -F'|' '/^\\| [0-9]+ \\|/ {v=$(NF-1); gsub(/^ +| +$/,\"\",v); print v}' reports/rapport-coherence-docs.md | sort | uniq -c | sort -rn", "description": "Recompter les verdicts"}`

  ```
38 PÉRIMÉ
     15 OK
     15 CONTRADICTOIRE
      9 MANQUANT
      1 OK (source)
      1 OK (2 o)
      1 MANQUANT (précision)
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "new_string": "**En une ligne** : **80 affirmations** vérifiées une par une contre le code (et\ncontre les traces réelles du disque) ; **38 sont fausses (PÉRIMÉ)**, **15 se\ncontredisent entre document … [1032 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "new_string": "| verdict | nombre | principaux foyers |\n|---|---:|---|\n| PÉRIMÉ | **38** | version du format de flux et du disque (7) · nombre de flux à 40 et 1 024 jetons (2) · en-têtes 26 et 39 oct … [2877 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "new_string": "| PÉRIMÉ | **38** | version du format de flux et du disque (7) · nombre de flux à 40 et 1 024 jetons (2) · en-têtes 26 et 39 octets (3) · octets par flux, par lot et par neurone actif (8 … [648 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "new_string": "10. **Documenter les variables qui restent dans l'ombre** : `DRAVE_BANC_KV_UNIT`,\n    `_V1`, `_GRAD`, `_KUNIT`, `_DEBUG` ne sont décrites nulle part,\n    `DRAVE_FLUX_VERIF` est muet en … [890 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "new_string": "* Les performances et les perplexités « en vol » : aucune exécution du moteur n'a été\n  autorisée ici, donc les chiffres **recalculables** (3 663, 917 583, 1 419, 1 023)\n  sont des **c … [728 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk -F'|' '/^\\| [0-9]+ \\|/ {v=$(NF-1); gsub(/^ +| +$/,\"\",v); print v}' reports/rapport-coherence-docs.md | sort | uniq -c | sort -rn && echo \"--- total lignes numérotées ---\" && grep -cE '^\\| [0-9]+ \\|' reports/rapport-cohere … [130 caractères tronqués]`

  ```
38 PÉRIMÉ
     15 OK
     15 CONTRADICTOIRE
      9 MANQUANT
      1 OK (source)
      1 OK (2 o)
      1 MANQUANT (précision)
--- total lignes numérotées ---
80
226 reports/rapport-coherence-docs.md
 M drave-core/src/model.rs
 M journal/README.md
?? reports/rapport-coherence-docs.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat && git diff -- drave-core/src/model.rs | head -40", "description": "Vérifier le nouveau diff de model.rs"}`

  ```
drave-core/src/model.rs | 31 ++++++++++++++++++++++++++++++-
 journal/README.md       |  7 ++++++-
 2 files changed, 36 insertions(+), 2 deletions(-)
diff --git a/drave-core/src/model.rs b/drave-core/src/model.rs
index acdca9e..268a75f 100644
--- a/drave-core/src/model.rs
+++ b/drave-core/src/model.rs
@@ -1068,6 +1068,14 @@ pub struct KvCache {
     pub hd: usize,
     kf: Vec<f32>,
     vf: Vec<f32>,
+    /// `DRAVE_KV_K_F16=1` : les CLÉS sont stockées en f16, sans quantification
+    /// par bloc. Deux octets par valeur — plus que l'int8 (1,125 avec son échelle)
+    /// mais bien moins que le f32 (4) — et une précision RELATIVE de 2⁻¹¹ par
+    /// valeur, là où l'int8 à échelle par bloc a une erreur ABSOLUE de bloc/254
+    /// qui écrase les petits canaux. C'est le « meilleur quantificateur de clés »
+    /// que la feuille de route appelle, sans rotation ni échelle par tête.
+    kp: Vec<u16>,
+    pub k_f16: bool,
     /// Quantifié : un octet par valeur en 8 bits, **deux nibbles par octet en
     /// 4 bits** (même disposition que Q4_0/MXFP4 : nibble bas = indice pair).
     kq: Vec<u8>,
@@ -1089,8 +1097,10 @@ impl KvCache {
         let nb = hd.div_ceil(32).max(1);
       
… [1111 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md", "new_string": "1. **L'arbre de travail a bougé pendant l'audit.** Quand il a commencé, HEAD était\n   `a0687b9` avec 165 lignes de `model.rs` non commitées (trace v3) ; le commit\n   `ae85043` (12:30)  … [1009 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '^#' reports/rapport-coherence-docs.md && echo \"---\" && awk -F'|' '/^\\| [0-9]+ \\|/ {v=$(NF-1); gsub(/^ +| +$/,\"\",v); print v}' reports/rapport-coherence-docs.md | sort | uniq -c | sort -rn && wc -l reports/rapport-coher … [54 caractères tronqués]`

  ```
1:# Cohérence des documents avec le code — audit
12:## Révision auditée, méthode, réserves
43:## 1. Version du protocole et du format
61:## 2. En-tête, champs, modes
79:## 3. Chiffres de transport et de trace
102:## 4. Autres chiffres (perplexités, densité, tailles)
119:## 5. Statuts et affirmations « vérifié »
134:## 6. Drapeaux, variables, renvois et phrases cassées
155:## Les 10 corrections à faire, dans l'ordre
203:## Ce que cet audit n'a pas vérifié
219:## Récapitulatif
---
     38 PÉRIMÉ
     15 OK
     15 CONTRADICTOIRE
      9 MANQUANT
      1 OK (source)
      1 OK (2 o)
      1 MANQUANT (précision)
229 reports/rapport-coherence-docs.md
  ```

- **send_message** `{"agent_id": "bbd6969f-0f70-42b2-8951-64d1f2f36d2e", "message": "Livrable : reports/rapport-coherence-docs.md (229 lignes). Seul fichier créé/modifié par moi. Révision auditée : HEAD ae85043 (12:30), main.rs sha d5e90136, model.rs sha 3e5dde2d ; l'arbre a bougé pendant l'audit (v3 disque commitée à  … [2074 caractères tronqués]`

  ```
message delivered to agent bbd6969f-0f70-42b2-8951-64d1f2f36d2e
  ```

### 🤖 Assistant

⏵ Audit terminé, livrable écrit et transmis au parent

Livrable : `reports/rapport-coherence-docs.md` (229 lignes, seul fichier que j'ai créé ; aucun autre fichier modifié, pas de `cargo build`, aucune exécution de serveur).

1. Révision auditée : HEAD `ae85043` (12:30) + 31 lignes non commitées de `model.rs` en fin d'audit ; 80 affirmations vérifiées contre le code et les traces réelles.
2. Verdicts : **38 PÉRIMÉ**, **15 CONTRADICTOIRE**, **10 MANQUANT**, **17 OK**.
3. Correction la plus urgente : `VERSION_FLUX = 3` (main.rs:1295) alors que le code, le commit « Protocole v4 » et le rapport d'audit annoncent une v4 qui transporte les top-k — deux binaires « v3 » aux contrats différents se croient compatibles et divergent en silence.
4. Deuxième urgence : en mode blocs, l'échappement d'indice est écrit sur **4 octets** (main.rs:1457) et lu sur **2** (main.rs:1618) ; toute trame avec un écart ≥ 255 se désynchronise, et la spec dit « deux octets ».
5. Troisième urgence : `REPRISE.md` §6bis est déjà périmé sur quatre points (protocole v2/39 octets, 1 024 flux, lots « prochain chantier », écart qui croît) — comme `docs/colab-reparti.md`, qui dit encore « lots ❌ » et cite 3 623/1 989 octets.
6. Les chiffres de transport publiés sont tous faux avec l'en-tête actuel de **79 octets** : 3 623 → 3 663, 1 989 → ≈ 1 419, 917 543 → 917 583, 1 589 → 1 629.
7. `docs/format-flux.md` se contredit seul : titre v3, « version u8 = 4 », message « parle la 4 », en-tête « 26 octets ».
8. Contradictions documentaires fortes : 10 % contre 22 % de densité (README, vision, histoire), README « Anciennement Drave » et « le nom changera dans un commit dédié », E5 « à faire » contre mesuré, « ÷2 pour 0,2 % » déjà réfuté par le rapport cité.
9. Renvois cassés : `reports/rapport-prefill-reparti.md` (jamais écrit — la phase 3.4 n'a pas de rapport), `rapport-pe-evenementiel.md` et `rapport-lecteur-ddr3.md` (existent dans `../FPGA-Stratix-V/docs/`), `gpu/drave_gpu.cu` (réel : `drave-core/gpu/`).
10. Manques côté doc : ~10 champs d'activation transportés en plus des 4 documentés, plafond R4 du lot absent du code, mode 4 fantôme, `--profil-experts` et `DRAVE_FLUX_POS` inexistants, `DRAVE_TRACE_BLOCS` documentée seulement depuis `ae85043` — les 10 corrections ordonnées sont dans le rapport, non appliquées.

