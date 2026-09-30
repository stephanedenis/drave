# Session DSH — relecture

- identifiant : `5ce3f080-2d3d-467a-8ee1-df697f3f3e68`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-09-30 15:32:10
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu es relecteur ADVERSARIAL dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM en Rust, `std` seul, binaire `drave`). Tout est en FRANÇAIS : écris en français. Ton rôle est de TROUVER DES DÉFAUTS, pas de valider.

CONTEXTE : le protocole de flux réseau vient de passer en **version 5** avec un cinquième mode, le **mode 4 « lot en listes »** (commit `8e132aa` et ses voisins immédiats). Un lot de N états est envoyé dans un seul flux ; chaque état est encodé comme le mode 2 (indices par écarts u8 avec échappement 255 vers u16 absolu, valeurs i8, une échelle f32 par bloc de 32 canaux) et **auto-délimité** par un préfixe de 12 octets : `a_j u32 · n_blocs_j u32 · longueur_j u32`. Le plan est `docs/plan-mode4-lot-listes.md` ; la spécification du protocole est `docs/format-flux.md`.

CE QU'IL FAUT ATTAQUER (dans `drave-core/src/main.rs` : `MODE_LOT_LISTES`, `encoder_etat_blocs`, `envoyer_lot_listes`, `tete_flux`, `encoder_paires_blocs`, `decoder_paires_blocs`, `verifier_taille`, `recevoir_flux`, la branche lot de `run_serveur_flux`, la boucle `lot > 1` de `run_ppl_reparti`, `ChargeFlux`) :

1. **Symétrie encodeur/décodeur** : les champs écrits par `encoder_etat_blocs` sont-ils EXACTEMENT ceux lus par `recevoir_flux`, dans le même ordre et la même largeur ? L'échappement d'indice (écart ≥ 255) est-il écrit et lu sur le même nombre d'octets ? Le préfixe de 12 octets est-il lu avant toute allocation ?
2. **Les garde-fous R4** : un état dont `a_j`, `n_blocs_j` ou `longueur_j` est énorme est-il refusé AVANT l'allocation correspondante ? Le cumul `12 + 4·n_blocs_j + longueur_j` est-il borné ? Un `n` (nombre d'états) énorme est-il borné avant la boucle ? Le refus de `n == 0` couvre-t-il tous les modes ?
3. **Les contrôles de cohérence** : `n_blocs_j == ⌈hidden/32⌉` et `2·a_j ≤ longueur_j ≤ 4·a_j` — sont-ils corrects pour tous les cas légitimes (état vide, tous les canaux actifs, échappements nombreux) ? Un état SANS aucun actif (a_j = 0) passe-t-il, et est-ce correct ?
4. **Les indices hors dimension** : le décodeur les ignore-t-il (comptés et dits) sans paniquer, comme le font les modes 1 et 2 ? Le décalage `plat[base + i]` peut-il sortir du vecteur ?
5. **Le contrat entre les deux nœuds** : le mode 4 est-il bien refusé par un pair en version 4, AVANT lecture (le refus d'un mode inconnu a été déplacé) ? La réponse est-elle encodée comme la demande ? Le mode 4 fonctionne-t-il quand `--lot` est plus grand que le nombre de jetons, ou quand le dernier lot est partiel ?
6. **Régressions** : les modes 0/1/2/3 fonctionnent-ils toujours (le commit a unifié la construction de l'en-tête dans `tete_flux` et ajouté un refus de mode inconnu) ?

MÉTHODE : lis les diffs (`git show 8e132aa`), prouve chaque défaut avec une commande exécutable, et **teste au moins un cas hostile** (une trame forgée : préfixe incohérent, `n_blocs` énorme, `a_j` énorme) en écrivant un client Python qui parle le protocole v5 — c'est la meilleure façon de trouver un décalage. `cargo test --release` est autorisé (14 tests). Les serveurs : autorisés, mais tue les tiens et pas plus de 2 minutes chacun. **Deux campagnes de mesure tournent** (`pgrep -x drave` : une sur le cache KV, une sur l'aiguille) : reste sous 8 fils et ne tue aucun processus qui n'est pas le tien.

INTERDIT : modifier un fichier du dépôt (rends ton rapport dans ta réponse).

Termine par un résumé de 10 lignes : nombre de défauts réels prouvés, les deux plus graves avec leur preuve, ce que tu as vérifié et trouvé correct, et ce que tu n'as pas pu vérifier.
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

⏵ Lecture des diffs du commit 8e132aa et du plan.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -8 && echo \"---\" && git show --stat 8e132aa", "description": "Show recent log and commit stat"}`

  ```
57f0fc6 Corrections du second audit (2/2) : la journée au README, le mode 4 dans la recette Colab, le renvoi FPGA de la vision
64a86ca Corrections du second audit (1/2) : chiffres, époques, comptes, et la journée au README
ac7f593 Cache KV : la frontière tient à 4 096 comme à 8 192
6b6ac17 Documents : protocole v5 et mode 4 (lot en listes)
8e132aa Mode 4 : le lot en LISTES sur le fil — ÷2,3 sur les octets, écart tenu
a383cd7 Plan du noyau GPU de top-k (phase 1.1), chiffré, et la perplexité attendue du notebook
90a74a6 Colab clé en main : le nœud local, les trois tunnels, et un texte réel dans le notebook
6c1aecf REPRISE : la frontière du cache KV et les deux gains du mode lot
---
commit 8e132aad129ae4d8ae861470bf69a099c80e6019
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 15:29:29 2026 -0400

    Mode 4 : le lot en LISTES sur le fil — ÷2,3 sur les octets, écart tenu
    
    Le lot dense (mode 3) coûtait 3,5 ko par jeton ; le mode 4 enchaîne N états
    encodés comme le mode 2 (indices par écarts, valeurs i8, une échelle f32 par bloc
    de 32 canaux), chacun auto-délimité par `a_j · n_blocs_j · longueur_j` — les trois
    tailles se lisent AVANT toute allocation.
    
 
… [2012 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l docs/plan-mode4-lot-listes.md docs/format-flux.md drave-core/src/main.rs && ls", "description": "Count lines of relevant docs"}`

  ```
445 docs/plan-mode4-lot-listes.md
   182 docs/format-flux.md
  3650 drave-core/src/main.rs
  4277 total
bench
colab
data
docs
drave-core
journal
models
__pycache__
Qtrinet-bootstrap.md
README.md
reports
REPRISE.md
run_8bit_perfection.py
run_clusters.py
run_cpu.py
run_encoding.py
run_harness.py
run_list_mode.py
run_precision.py
run_quantify.py
run_real_clusters.py
run_sparsity.py
run_value_encoding.py
src
tools
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 8e132aa -- drave-core/src/main.rs", "description": "Show main.rs diff for commit"}`

  ```
commit 8e132aad129ae4d8ae861470bf69a099c80e6019
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 15:29:29 2026 -0400

    Mode 4 : le lot en LISTES sur le fil — ÷2,3 sur les octets, écart tenu
    
    Le lot dense (mode 3) coûtait 3,5 ko par jeton ; le mode 4 enchaîne N états
    encodés comme le mode 2 (indices par écarts, valeurs i8, une échelle f32 par bloc
    de 32 canaux), chacun auto-délimité par `a_j · n_blocs_j · longueur_j` — les trois
    tailles se lisent AVANT toute allocation.
    
    Mesuré, 256 jetons, 16 jetons par lot, seuil 0,01 :
    
    | | octets par jeton | écart |
    |---|---|---|
    | mode 2, un flux par jeton (référence) | 1 608 par flux | 2,74e-2 |
    | **mode 4, lot en listes de 16** | **1,5 ko** | **3,03e-2** |
    
    ÷2,3 sur les octets, et l'écart reste sous le critère (1,5 × celui du mode 2). Le
    protocole passe en **version 5** — un pair v4 lirait `4t` octets d'un corps qui en
    fait ~1 500 par état — et le refus d'un mode inconnu devient IMMÉDIAT, avant tout
    octet de corps (il se produisait après lecture, donc désynchronisé et muet sur la
    cause).
    
    Trois choses apprises en le faisant :
    - la construction de l'
… [20407 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-flux.md"}`

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
… [10173 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du code en place : `verifier_taille`, `recevoir_flux`, `ChargeFlux`.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fn verifier_taille\\|fn recevoir_flux\\|enum ChargeFlux\\|fn decoder_paires_blocs\\|fn encoder_paires_blocs\\|fn encoder_etat_blocs\\|fn envoyer_lot_listes\\|fn tete_flux\\|fn run_serveur_flux\\|fn run_ppl_reparti\\|TAILLE_ … [119 caractères tronqués]`

  ```
1411:const TAILLE_TETE: usize = 4 + 1 + 1 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 1
1472:const PLAFOND_FLUX: usize = 256 << 20;
1475:fn verifier_taille(octets: usize, quoi: &str) -> std::io::Result<()> {
1476:    if octets > PLAFOND_FLUX {
1478:            format!("{quoi} : {octets} octets au-delà du plafond de {} Mo — flux refusé                      (règle R4 de docs/plan-prefill-reparti.md)", PLAFOND_FLUX >> 20)));
1486:enum ChargeFlux {
1557:fn tete_flux(mode: u8, debut: u32, fin: u32, pos: u32, n: usize, echelle: f32,
1562:    let mut t = Vec::with_capacity(TAILLE_TETE);
1579:    assert_eq!(t.len(), TAILLE_TETE,
1580:               "en-tête de flux de {} octets pour {TAILLE_TETE}", t.len());
1589:fn encoder_paires_blocs(idx: &[u16], val: &[i8]) -> Vec<u8> {
1607:fn decoder_paires_blocs(corps: &[u8], n: usize) -> Result<(Vec<u16>, Vec<i8>), String> {
1611:    if n.saturating_mul(2) > PLAFOND_FLUX {
1613:                           PLAFOND_FLUX >> 20));
1683:    Ok((TAILLE_TETE + corps.len(), n))
1700:    Ok(TAILLE_TETE + corps.len())
1708:fn encoder_etat_blocs(mdl: &model::Model, etat: &[f32]) -> Vec<u8> {
1721:fn envoyer_lot_listes(s: &mut std::net::TcpStream, debut: u32, fin: u32, p
… [682 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "offset": 1400, "limit": 120}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "offset": 1557, "limit": 200}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1400: const MODE_LOT_LISTES: u8 = 4;
1401: 
1402: /// En-tête commun : magie · version · mode · plage · position · n · échelle ·
1403: /// **réglages d'activation** (niveaux, seuil, top-k, renorm).
1404: ///
1405: /// Les réglages voyagent parce qu'ils CHANGENT LES CHIFFRES : deux nœuds lancés
1406: /// avec des `--act-thresh` différents ne calculent pas la même chose, et la
1407: /// divergence serait silencieuse. Mesuré : 0,69 d'écart de perplexité avec un
1408: /// seuil 0,05 d'un côté et 0,00 de l'autre, sur le même modèle.
1409: // magie · version · mode · plage · position · n · échelle · niveaux · seuil ·
1410: // top-k · renorm · attn_topk · qk_topk · moe_topk · topk_proj[7]
1411: const TAILLE_TETE: usize = 4 + 1 + 1 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 1
1412:                             + 4 + 4 + 4 + 7 * 4;
1413: 
1414: /// Réglages d'activation d'un nœud : ils font partie du contrat d'échange.
1415: #[derive(Clone, Copy)]
1416: struct Act {
1417:     levels: f32,
1418:     thresh: f32,
1419:     topk: u32,
1420:     renorm: bool,
1421:     /// Top-k par projection 
… [5025 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1557: fn tete_flux(mode: u8, debut: u32, fin: u32, pos: u32, n: usize, echelle: f32,
1558:              mdl: Option<&model::Model>) -> Vec<u8> {
1559:     let act = mdl.map(Act::du_modele).unwrap_or(Act {
1560:         levels: 127.0, thresh: 0.0, topk: 0, renorm: false,
1561:         topk_proj: [0; 7], attn_topk: 0, qk_topk: 0, moe_topk: 0 });
1562:     let mut t = Vec::with_capacity(TAILLE_TETE);
1563:     t.extend_from_slice(&MAGIE_FLUX.to_le_bytes());
1564:     t.push(VERSION_FLUX);
1565:     t.push(mode);
1566:     t.extend_from_slice(&debut.to_le_bytes());
1567:     t.extend_from_slice(&fin.to_le_bytes());
1568:     t.extend_from_slice(&pos.to_le_bytes());
1569:     t.extend_from_slice(&(n as u32).to_le_bytes());
1570:     t.extend_from_slice(&echelle.to_le_bytes());
1571:     t.extend_from_slice(&act.levels.to_le_bytes());
1572:     t.extend_from_slice(&act.thresh.to_le_bytes());
1573:     t.extend_from_slice(&act.topk.to_le_bytes());
1574:     t.push(act.renorm as u8);
1575:     for k in act.topk_proj { t.extend_from_slice(&k.to_le_bytes()); }
1576:     t.extend_fr
… [9602 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 170, "offset": 1756}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1756:     let n = u(18) as usize;
1757:     let echelle = f32::from_le_bytes([tete[22], tete[23], tete[24], tete[25]]);
1758:     let mut topk_proj = [0u32; 7];
1759:     for (i, v) in topk_proj.iter_mut().enumerate() { *v = u(39 + i * 4); }
1760:     let act = Act {
1761:         levels: f32::from_le_bytes([tete[26], tete[27], tete[28], tete[29]]),
1762:         thresh: f32::from_le_bytes([tete[30], tete[31], tete[32], tete[33]]),
1763:         topk: u(34),
1764:         renorm: tete[38] != 0,
1765:         topk_proj,
1766:         attn_topk: u(67),
1767:         qk_topk: u(71),
1768:         moe_topk: u(75),
1769:     };
1770:     // Le mode est vérifié AVANT de lire le moindre octet de corps : un mode
1771:     // inconnu se refusait après avoir lu `n × 4` octets et s'être désynchronisé,
1772:     // en disant « mode inconnu » — exact, tardif, et muet sur la cause.
1773:     // Règle R4, première moitié : un flux à ZÉRO élément est un bug du pair, pas
1774:     // une donnée — le plan l'annonçait, le code ne le vérifiait pas (relevé par le
1775:     // second audit de 
… [9309 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de la branche serveur « lot » et de la boucle `lot > 1`.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 150, "offset": 1926}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 150, "offset": 2085}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1926:     let chemin = modele_chemin();
1927:     // Le contexte du nœud moteur suit `--ctx` : figé à 4096, il faisait payer au
1928:     // pair des tampons d'attention seize fois plus grands que le banc (mesuré :
1929:     // 4,8 s contre 1,7 s pour le même calcul, à contexte 256).
1930:     let ctx = if opt.ctx_impose { opt.ctx } else { 4096 };
1931:     let mut mdl = model::Model::load(&chemin, ctx, fils(&opt), true, opt.keep, false, 0, 0);
1932:     appliquer_quantification(&mut mdl, &opt);
1933:     if opt.options_actives { options_actives(&mdl, "nœud moteur du flux", opt.ctx_impose, true, opt.keep); }
1934:     let hidden = mdl.cfg.hidden;
1935:     let ecoute = std::net::TcpListener::bind((hote.as_str(), port)).expect("écoute");
1936:     println!("[flux] nœud moteur sur {hote}:{port} · {hidden} cachés · {} couches · contexte {ctx}",
1937:              mdl.cfg.n_layer);
1938:     let (mut sock, pair) = ecoute.accept().expect("connexion");
1939:     // TCP_NODELAY, et ce n'est pas un détail de confort : sans lui, Nagle garde
1940:     // une petite écriture en atte
… [8126 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
2085:             }
2086:         }
2087:     }
2088:     let ppl_ref = (nll_ref / (ids.len() - 1) as f64).exp();
2089:     println!("  référence locale  : perplexité {ppl_ref:.4}  ({:.1} s)", t0.elapsed().as_secs_f64());
2090: 
2091:     // 2. la même chose, coupée en deux nœuds
2092:     let mut sock = std::net::TcpStream::connect(pair).expect("connexion au nœud moteur");
2093:     sock.set_nodelay(true).expect("TCP_NODELAY");   // cf. le nœud moteur : Nagle coûte 6×
2094:     mdl.couche_fin = couches_locales;
2095:     let mut octets_envoyes = 0u64;
2096:     let mut octets_recus = 0u64;
2097:     let mut actifs_envoyes = 0u64;
2098:     let mut flux_envoyes = 0u64;
2099:     let mut t_local = 0f64;
2100:     let mut t_pair = 0f64;
2101:     let t1 = Instant::now();
2102:     let mut nll = 0f64;
2103:     if lot > 1 {
2104:         // PRÉREMPLISSAGE RÉPARTI : un lot par aller-retour au lieu d'un flux par
2105:         // jeton. C'est ce que la phase 3.4 doit démontrer — le découpage doit
2106:         // coûter la latence d'UN message par lot, pas par jeton.
2107:     
… [7647 caractères tronqués]
  ```

