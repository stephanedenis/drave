# Session DSH — relecture

- identifiant : `5185ccb1-be24-4716-89df-62621e790444`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-09-30 17:03:05
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu es relecteur ADVERSARIAL dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM en Rust, `std` seul, binaire `drave`). Tout est en FRANÇAIS : écris en français. Ton rôle est de TROUVER DES DÉFAUTS, pas de valider.

CONTEXTE : la dernière heure a corrigé dix défauts trouvés par une relecture précédente du **mode 4 « lot en listes »** (protocole v5), puis a documenté une politique de cache KV. Ces correctifs n'ont été relus par personne. Les commits à attaquer (du plus récent au plus ancien, à partir de `998d409`) :

- `998d409` — plafond R4 cumulatif, refus de `n == 0` restreint aux modes 0/3/4, `a_j` borné par `hidden`, « hors dimension » dit une fois, contrôle de la réponse du pair, comptabilité par jeton réel, `tools/pair_factice.py` qui lit le mode 4 ;
- `f28c60a` — vérification du plafond cumulatif ;
- `0259bf1` — fidélité du mode 3 à 1 024 jetons ;
- `b04dfd0`, `80ba3d6`, `0c56c35` — la politique du cache KV (taille ET temps) et l'aiguille.

CE QU'IL FAUT ATTAQUER :
1. **Le refus de `n == 0` restreint** : est-il correct pour TOUS les modes ? En mode 0 (dense), `n` est une dimension : zéro canal est-il vraiment illégitime ? En modes 1/2, une liste vide est acceptée — le décodeur la traite-t-il correctement dans tous les chemins (mode 1 : `ChargeFlux::Liste` vide ; mode 2 : `ChargeFlux::Blocs` avec `idx` vide) ? Le vecteur qui en résulte est-il un vecteur NUL, et le moteur le traite-t-il sans division par zéro (`quant_scratch` rend `None` quand le max est nul → que fait l'appelant) ?
2. **Le plafond cumulatif** (`lus`) : est-il vérifié au bon endroit (avant ou après l'ajout) ? Peut-on le contourner avec plusieurs flux successifs (le cumul ne se réinitialise-t-il pas à chaque flux, alors que la mémoire vive, elle, s'accumule d'un flux à l'autre si le vecteur `plat` n'est pas libéré) ?
3. **La borne `a ≤ hidden`** : est-elle correcte pour un modèle dont `hidden` diffère de la dimension du flux (un cas légitime existe-t-il) ? Et pour le mode 1/2 en flux simple (`envoyer_flux`), la même borne s'applique-t-elle — ou un pair peut-il encore envoyer un indice énorme par ce chemin ?
4. **Le contrôle de la réponse du pair** : couvre-t-il le cas d'une réponse en mode 3 alors que la demande était en mode 4 (et l'inverse) ? Et le chemin NON-lot (mode 1/2) vérifie-t-il quelque chose ?
5. **La comptabilité** : `jetons_envoyes` et `octets_envoyes` sont-ils cohérents quand `--lot` dépasse le nombre de jetons, quand il y a un seul lot, ou quand le dernier lot est partiel ?
6. **Les mesures publiées** dans `reports/rapport-placement-bits-kv.md` (politique par régime, aiguille 9/9) et `reports/rapport-mode4-lot-listes.md` : sont-elles reproductibles ? Les commandes données suffisent-elles ? Les affirmations sur le miroir VRAM (« toute variante d'attribution le désactive ») sont-elles vraies pour les QUATRE variables (`DRAVE_KV_K_F32`, `DRAVE_KV_V_F32`, `DRAVE_KV_K_F16`, `DRAVE_KV_F16`) ?
7. **Régressions** : `cargo test --release` (17 tests) ; les modes 0 à 4 ; la porte Qwen ctx 256 = **19,3885**.

MÉTHODE : lis les diffs (`git show <sha>`), prouve chaque défaut par une commande, et **teste au moins un cas hostile** (trame forgée : mode 1 avec `n` énorme, réponse incohérente, cumul réparti sur plusieurs flux). `cargo test` autorisé ; serveurs autorisés mais tués après ≤ 2 minutes chacun ; **reste sous 8 fils** (la machine est libre, mais d'autres mesures peuvent démarrer). Tu ne dois tuer aucun processus qui n'est pas le tien.

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

⏵ Exploration du dépôt et des commits à attaquer

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -15 && echo \"---\" && ls && echo \"---\" && cargo --version && rustc --version", "description": "List commits and repo contents"}`

  ```
0c56c35 REPRISE : la politique du cache KV complète (taille ET temps), et l'aiguille 9/9
80ba3d6 Aiguille 9/9 dans les trois variantes de cache KV, et les vérifications de fin de journée
b04dfd0 La politique du cache KV selon le régime : le meilleur réglage en octets n'est pas le meilleur en temps
98402c6 REPRISE : dix-sept tests, et ce qu'ils verrouillent
0259bf1 Préremplissage par lots : fidélité vérifiée à 1 024 jetons (0,00e0, 16 lots)
f28c60a Mode 4 : le plafond cumulatif vérifié à l'octet près
1dd3952 Index : le mode 4, le protocole v5, le plan GPU et le décompte des relectures
5999469 Index de session : le créneau 15h-18h (mode 4, plan GPU, 32 défauts relevés)
e6d6ce9 Colab : les quatorze champs du contrat d'activation, pas quatre
d36f93e Documents : dernières mentions de la version 4 remplacées par la 5 (mode lot en listes)
998d409 Relecture du mode 4 : dix défauts, dont deux graves — corrigés, et le rapport écrit
621670b --options-strict : un drapeau inconnu devient une erreur, pour les scripts
b9e8ada README : la perplexité de gpt-oss était dans la colonne du débit
6929642 REPRISE : le créneau 15h-18h (mode 4, frontière KV confirmée, plan GPU écrit)
b9a3425 Cache KV à 4 0
… [449 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain && echo \"--- branches ---\" && git branch -a && echo \"--- head ---\" && git rev-parse HEAD", "description": "Check git status and HEAD"}`

  ```
M journal/README.md
--- branches ---
* master
--- head ---
0c56c356b0e862b841621968bc27ec5fff45f889
  ```

### 🤖 Assistant

⏵ Lecture du diff 998d409 (dix correctifs mode 4)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat 998d409 && echo \"=====\" && git show 998d409 -- src/ | head -600", "description": "Show stat and src diff of 998d409"}`

  ```
commit 998d4095ee84bc9e785e10e8e44f48b99a215751
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 16:03:52 2026 -0400

    Relecture du mode 4 : dix défauts, dont deux graves — corrigés, et le rapport écrit
    
    La relecture adversariale du mode 4 a trouvé ce que les bancs ne voyaient pas :
    
    1. **le plafond R4 n'était pas cumulatif** (le plan l'exigeait trois fois) : chaque
       état pouvait être légal sans que le total le soit — 268 Mo par état sur 74 898
       états. La mémoire restait bornée, le temps non.
    2. **le refus de `n == 0` était trop large**, et c'est un correctif de la journée
       qui l'avait introduit : en modes 1 et 2, `n` compte des PAIRES, et une liste
       vide est légitime (seuil au-dessus du maximum). `--flux-blocs --act-thresh 1.0
       --lot 1` mourait, et `tools/pair_factice.py` avec elle. Le refus ne vise plus que
       les modes où `n` est une dimension ou un nombre d'états — vérifié : la session
       qui mourait donne 0,00e0.
    3. `a_j` borné par `hidden` ; « hors dimension » dit UNE fois par message ;
       le client vérifie le mode et la taille de la réponse au lieu d'abandonner en
       SIGABRT sur 83 octets hostil
… [3187 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des diffs réels (drave-core/src)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 998d409 -- drave-core/src/main.rs drave-core/src/model.rs", "description": "Show main.rs and model.rs diff"}`

  ```
commit 998d4095ee84bc9e785e10e8e44f48b99a215751
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 16:03:52 2026 -0400

    Relecture du mode 4 : dix défauts, dont deux graves — corrigés, et le rapport écrit
    
    La relecture adversariale du mode 4 a trouvé ce que les bancs ne voyaient pas :
    
    1. **le plafond R4 n'était pas cumulatif** (le plan l'exigeait trois fois) : chaque
       état pouvait être légal sans que le total le soit — 268 Mo par état sur 74 898
       états. La mémoire restait bornée, le temps non.
    2. **le refus de `n == 0` était trop large**, et c'est un correctif de la journée
       qui l'avait introduit : en modes 1 et 2, `n` compte des PAIRES, et une liste
       vide est légitime (seuil au-dessus du maximum). `--flux-blocs --act-thresh 1.0
       --lot 1` mourait, et `tools/pair_factice.py` avec elle. Le refus ne vise plus que
       les modes où `n` est une dimension ou un nombre d'états — vérifié : la session
       qui mourait donne 0,00e0.
    3. `a_j` borné par `hidden` ; « hors dimension » dit UNE fois par message ;
       le client vérifie le mode et la taille de la réponse au lieu d'abandonner en
       SIGABRT sur 83 octets hostil
… [11144 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du code actuel autour de `recevoir_flux`

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fn recevoir_flux\" -A 160 drave-core/src/main.rs | head -220", "description": "Read recevoir_flux implementation"}`

  ```
1747:fn recevoir_flux(s: &mut std::net::TcpStream, hidden: usize) -> std::io::Result<Flux> {
1748-    use std::io::Read;
1749-    let mut tete = [0u8; TAILLE_TETE];
1750-    s.read_exact(&mut tete)?;
1751-    let u = |o: usize| u32::from_le_bytes([tete[o], tete[o+1], tete[o+2], tete[o+3]]);
1752-    if u(0) != MAGIE_FLUX {
1753-        return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
1754-                                       "magie de flux absente"));
1755-    }
1756-    let version = tete[4];
1757-    let mode = tete[5];
1758-    if version != VERSION_FLUX {
1759-        // Refus EXPLICITE : on ne devine pas la version du pair, on la nomme.
1760-        return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
1761-            format!("flux en version {version}, cette build parle la {VERSION_FLUX} \
1762-                     (pair incompatible : rien n'a été interprété)")));
1763-    }
1764-    let (debut, fin, pos) = (u(6), u(10), u(14));
1765-    let n = u(18) as usize;
1766-    let echelle = f32::from_le_bytes([tete[22], tete[23], tete[24], tete[25]]);
1767-    let mut topk_proj = [0u32; 7];
1768-    for (i, v) in topk_proj.iter_mut().enumerate() { *v = u
… [8789 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"verifier_taille\\|const TAILLE_TETE\\|fn decoder_une_trame\\|fn en_dense\\|fn plat\" drave-core/src/main.rs drave-core/src/model.rs | head -60", "description": "Locate helpers"}`

  ```
drave-core/src/main.rs:1420:const TAILLE_TETE: usize = 4 + 1 + 1 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 1
drave-core/src/main.rs:1484:fn verifier_taille(octets: usize, quoi: &str) -> std::io::Result<()> {
drave-core/src/main.rs:1506:    fn en_dense(&self, hidden: usize) -> Vec<f32> {
drave-core/src/main.rs:1554:    fn plat(&self) -> &[f32] {
drave-core/src/main.rs:1806:            verifier_taille(n.checked_mul(hidden).and_then(|x| x.checked_mul(4))
drave-core/src/main.rs:1819:                verifier_taille(a.saturating_mul(2), &format!("état {j} : {a} actifs"))?;
drave-core/src/main.rs:1820:                verifier_taille(nb.saturating_mul(4), &format!("état {j} : {nb} blocs"))?;
drave-core/src/main.rs:1821:                verifier_taille(lg, &format!("état {j} : {lg} octets de paires"))?;
drave-core/src/main.rs:1822:                verifier_taille(12usize.saturating_add(nb.saturating_mul(4)).saturating_add(lg),
drave-core/src/main.rs:1865:                verifier_taille(lus, &format!("corps du lot en listes (cumul après \
drave-core/src/main.rs:1885:            verifier_taille(taille, &format!("lot de {n} états × {hidden} canaux"))?;
drave-core/src/main.rs:1902:            verifier_ta
… [407 caractères tronqués]
  ```

