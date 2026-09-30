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

### 🤖 Assistant

⏵ Lecture des structures `ChargeFlux`, `quant_scratch`, plafond

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1410,1620p' drave-core/src/main.rs", "description": "Read flux structs and verifier_taille"}`

  ```
/// En-tête commun : magie · version · mode · plage · position · n · échelle ·
/// **réglages d'activation** (niveaux, seuil, top-k, renorm).
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
    renorm: bool,
    /// Top-k par projection (q, k, v, o, gate, up, down) : « topk est une FRACTION
    /// de la dimension » (voir `quant_scratch`), donc ces valeurs décident de ce
    /// qui est calculé. Elles voyagent pour la même raison que le seuil.
    topk_proj: [u32; 7],
    attn_topk: u32,
    qk_topk: u32,
  
… [8166 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1907,1990p' drave-core/src/main.rs", "description": "Read rest of recevoir_flux"}`

  ```
let mut lg = [0u8; 4];
            s.read_exact(&mut lg)?;
            let longueur = u32::from_le_bytes(lg) as usize;
            verifier_taille(longueur, &format!("corps de {n} paires"))?;
            let mut corps = vec![0u8; longueur];
            s.read_exact(&mut corps)?;
            let (idx, val) = match decoder_paires_blocs(&corps, n) {
                Ok(v) => v,
                Err(e) => return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, e)),
            };
            let octets_corps = 4 + n_blocs * 4 + 4 + longueur;
            return Ok(Flux { n, debut, fin, pos, mode, act, octets_corps, charge:
                             ChargeFlux::Blocs { idx, val, echelles } });
        }
        _ => {}
    };
    verifier_taille(n.saturating_mul(4), &format!("flux de {n} valeurs"))?;
    let mut octets = vec![0u8; n * 4];
    s.read_exact(&mut octets)?;
    let charge = match mode {
        MODE_DENSE => ChargeFlux::Dense((0..n).map(|k| f32::from_le_bytes(
            [octets[k*4], octets[k*4+1], octets[k*4+2], octets[k*4+3]])).collect()),
        MODE_LISTE => {
            let mut idx = Vec::with_capacity(n);
            let mut val = Vec::with_capacity(n);
  
… [3427 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du chemin client `run_ppl_reparti` et `envoyer_flux`

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fn envoyer_flux\\|fn run_ppl_reparti\\|fn forward_lot\\|fn quant_scratch\" drave-core/src/main.rs drave-core/src/model.rs", "description": "Locate functions"}`

  ```
drave-core/src/main.rs:1652:fn envoyer_flux(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos: u32,
drave-core/src/main.rs:2057:fn run_ppl_reparti(opt: Options, pair: &str) {
drave-core/src/model.rs:1793:    fn quant_scratch(x: &[f32], levels: f32, thresh: f32, topk: usize, renorm: bool,
drave-core/src/model.rs:2320:    pub fn forward_lot(&mut self, toks: &[u32], pos0: usize) -> Vec<Vec<f32>> {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2100,2300p' drave-core/src/main.rs", "description": "Read run_ppl_reparti"}`

  ```
let hs = mdl.forward_lot(&ids[pos..pos + t], pos);
            let lgs = mdl.logits_lot(&hs);
            for i in 0..t {
                if pos + i + 1 < ids.len() {
                    nll_ref += nll_logits(&lgs[i], ids[pos + i + 1]);
                }
            }
            pos += t;
        }
    } else {
        for (pos, &t) in ids.iter().enumerate() {
            let last = mdl.forward(t, pos);
            if pos + 1 < ids.len() {
                nll_ref += nll_logits(&mdl.logits(&last), ids[pos + 1]);
            }
        }
    }
    let ppl_ref = (nll_ref / (ids.len() - 1) as f64).exp();
    println!("  référence locale  : perplexité {ppl_ref:.4}  ({:.1} s)", t0.elapsed().as_secs_f64());

    // 2. la même chose, coupée en deux nœuds
    let mut sock = std::net::TcpStream::connect(pair).expect("connexion au nœud moteur");
    sock.set_nodelay(true).expect("TCP_NODELAY");   // cf. le nœud moteur : Nagle coûte 6×
    mdl.couche_fin = couches_locales;
    let mut octets_envoyes = 0u64;
    let mut octets_recus = 0u64;
    let mut actifs_envoyes = 0u64;
    let mut flux_envoyes = 0u64;
    let mut jetons_envoyes = 0u64;   // Σt, pas `lot` : le dernier lot est partiel
    l
… [9273 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du serveur (boucle) et de `norme_finale`/`quant_scratch`

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1990,2057p' drave-core/src/main.rs", "description": "Read server loop rest"}`

  ```
// second faisait tomber un flux de listes dans le chemin « un seul
                // vecteur » et paniquait sur `en_dense` — attrapé au premier essai.
                if f.mode == MODE_LOT || f.mode == MODE_LOT_LISTES {
                    // Préremplissage réparti : N états d'un coup. Le nœud n'a pas
                    // les identifiants de jetons — il n'en a pas besoin, les
                    // états entrent directement dans SA première couche.
                    let t = f.n;
                    // Refus EXPLICITE plutôt qu'une boucle sans fin : au-delà de
                    // son contexte, `KvCache::assurer` ne peut pas agrandir et
                    // tournerait indéfiniment (relevé dans `docs/plan-prefill-reparti.md`).
                    if f.pos as usize + t > mdl.ctx {
                        println!("[flux] lot refusé : {t} états à partir de la position {} \
                                  dépassent le contexte {} de ce nœud",
                                 f.pos, mdl.ctx);
                        break;
                    }
                    mdl.emb_imposee_lot = Some(f.charge.plat().to_vec());
                    let hs = mdl.forward_lot(&vec![0u32; t]
… [2324 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"quant_scratch\" drave-core/src/model.rs | head -20 && echo \"---\" && sed -n '1780,1830p' drave-core/src/model.rs && echo \"=== norme_finale ===\" && grep -n \"fn norme_finale\" -A 25 drave-core/src/model.rs", "description" … [40 caractères tronqués]`

  ```
1793:    fn quant_scratch(x: &[f32], levels: f32, thresh: f32, topk: usize, renorm: bool,
1850:        let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
1929:            Self::quant_scratch(x, levels, thresh, topk, renorm, scratch)
1958:        let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
2408:        // Quantification d'un lot : mêmes règles que `quant_scratch`.
3077:                if let Some((sv, sx)) = Self::quant_scratch(&hn, self.act_levels, self.act_thresh,
3321:                if let Some((sv, sx)) = Self::quant_scratch(&hn, self.act_levels, self.act_thresh,
3506:            let (sv, sx) = match Self::quant_scratch(hi, self.act_levels, self.act_thresh,
3616:        match Self::quant_scratch(x, 32767.0, self.act_thresh, self.act_topk,
3680:        let (sv, sx) = match Self::quant_scratch(h, self.act_levels, self.act_thresh,
---
    // ----------------------------------------------------------------------- //
    // Briques de calcul
    // ----------------------------------------------------------------------- //

    /// Quantifie un vecteur (une échelle pour tout le vecteur).
    #[inline
… [4098 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche de `emb_imposee`, `rmsnorm`, et du chemin non-lot

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"emb_imposee\" drave-core/src/model.rs | head -30 && echo \"=== rmsnorm ===\" && grep -n \"fn rmsnorm\" -A 20 drave-core/src/model.rs", "description": "Read emb_imposee and rmsnorm"}`

  ```
921:    pub emb_imposee: Option<Vec<f32>>,
924:    /// C'est le pendant de `emb_imposee` pour le préremplissage réparti : un nœud
928:    pub emb_imposee_lot: Option<Vec<f32>>,
1775:            emb_imposee: None, emb_imposee_lot: None, lot: 1,
2326:        // relecture) — et consommé une seule fois, comme `emb_imposee` pour un
2328:        let impose = self.emb_imposee_lot.take();
2331:            if let Some(v) = impose { self.emb_imposee = Some(v); }
2333:            // `emb_imposee` et n'appelle jamais `token_embd`. `toks` peut donc
2995:                    attn_gpu_part, emb_imposee, .. } = self;
3006:        let mut x = match emb_imposee.take() {
=== rmsnorm ===
2200:    fn rmsnorm(x: &[f32], w: &[f32], eps: f32, out: &mut [f32]) {
2201-        let mut ss = 0f32;
2202-        for &v in x { ss += v * v; }
2203-        let inv = 1.0 / (ss / x.len() as f32 + eps).sqrt();
2204-        for i in 0..x.len() { out[i] = x[i] * inv * w[i]; }
2205-    }
2206-
2207-    /// k-WTA par tête : ne garder que la fraction demandée des composantes les
2208-    /// plus grandes de chaque tête. Appliqué à Q et K, il rend le produit
2209-    /// scalaire des scores creux.
2210-    fn creuse_tetes(v:
… [621 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls models/ && echo \"---\" && ls reports/ && echo \"--- tools ---\" && ls tools/", "description": "List models, reports, tools"}`

  ```
Qwen2.5-0.5B-Q4_0.gguf
Qwen2.5-0.5B-Q8_0.gguf
---
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
rapport-coherence-docs-2.md
rapport-coherence-docs.md
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
rapport-mode4-lot-listes.md
rapport-modele-reel.md
rapport-mode-listes.md
rapport-mur-memoire-4bits.md
rapport-optimisations.md
rapport-parcimonie-imposee.md
rapport-passage-a-l-echelle.md
rapport-phase3-reparti.md
rapport-placement-bits-kv.md
rapport-precision.md
rapport-prefill-par-lots.md
rapport-prefill-reparti.md
rapport-programme-evolutif.md
rapport-session-2026-09-30.md
rapport-transport-liste.md
rapport-travail-reel.md
rapport-valeur-unaire.md
--- tools ---
aiguille.py
analyse_flux.py
archive_sessions.py
colab_cote_local.sh
compare_logits.py
dif
… [261 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lancement des tests en tâche de fond et lecture des rapports

- **todo_write** `{"todos": [{"content": "Lire les diffs 998d409/f28c60a/0259bf1/b04dfd0/80ba3d6/0c56c35", "status": "in_progress"}, {"content": "Attaquer le refus n==0 et le chemin modes 1/2/0 (vecteur nul, dimensions)", "status": "pending"}, {"content": "Attaquer le plafond cumulatif (multi-flux, cumul mémoire)", " … [531 caractères tronqués]`

  ```
Updated todo list: 8 pending, 1 in progress, 0 completed.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls drave-core && cat drave-core/Cargo.toml && nproc", "description": "Inspect Cargo.toml and CPU count"}`

  ```
Cargo.lock
Cargo.toml
gpu
README.md
src
target
[package]
name = "drave-core"
version = "0.1.0"
edition = "2021"
description = "Drave — moteur d'exécution par listes d'activation (stream of logs) pour modèles quantifiés"

[[bin]]
name = "drave"
path = "src/main.rs"

[dependencies]
# aucune : std seul, pour rester sans dépendance réseau

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
panic = "abort"
40
  ```

### 🤖 Assistant

⏵ Compilation et tests release en tâche de fond (limités à 4 fils)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nice -n 5 cargo test --release -j 4 -- --test-threads=4 2>&1 | tail -40", "description": "Run release tests limited to 4 threads", "run_in_background": true}`

  ```
started background job bash-81
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show b04dfd0 --stat && echo \"=====\" && git show 80ba3d6 --stat && echo \"=====\" && git show 0c56c35 --stat", "description": "Show stats of KV policy commits"}`

  ```
commit b04dfd0fd6d581d93e2609da6d90cb226eab5469
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 17:01:23 2026 -0400

    La politique du cache KV selon le régime : le meilleur réglage en octets n'est pas le meilleur en temps
    
    Trois mesures de temps changent le conseil (banc `--banc-kv`, 262 144 clés) :
    
    - **les clés f16 coûtent 2,3× le temps CPU** des clés f32 (162 contre 70 ms par
      passe) : la conversion f16 → f32 se paie par élément, là où le f32 est une copie.
      Le réglage le plus économe en octets est le plus cher en temps ;
    - **le miroir VRAM exige une disposition homogène** : toute variante d'attribution
      le désactive (vérifié), alors qu'il divise le temps de l'attention par 40 ;
    - le noyau GPU, lui, est exact dans les trois cas (+3 à +4e-5).
    
    D'où une politique par régime, écrite dans le rapport et dans `contexte-long` :
    clés f16 + valeurs int8 à contexte court ou moyen sur CPU ; int8/int8 homogène dès
    qu'on veut le miroir ou qu'on est à très long contexte — parce que c'est le miroir
    qui décide du temps, pas la taille du cache.

 docs/contexte-long.md                              | 16 +++-
 journal/sessions/M
… [1967 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-81 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nice -n 5 cargo test --release -j 4 -- --test-threads=4 2>&1 | tail -40) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-81"}`

  ```
error: could not find `Cargo.toml` in `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` or any parent directory
[status: completed, exit code: 0]
  ```

### 🤖 Assistant

⏵ Relance des tests depuis drave-core

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && nice -n 5 cargo test --release -j 4 -- --test-threads=4 2>&1 | tail -45", "description": "Run release tests in drave-core", "run_in_background": true}`

  ```
started background job bash-82
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 0c56c35 -- REPRISE.md && echo \"======= b04dfd0 rapport =======\" && git show b04dfd0 -- reports/rapport-placement-bits-kv.md docs/contexte-long.md", "description": "Show KV report diffs"}`

  ```
commit 0c56c356b0e862b841621968bc27ec5fff45f889
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 17:02:39 2026 -0400

    REPRISE : la politique du cache KV complète (taille ET temps), et l'aiguille 9/9

diff --git a/REPRISE.md b/REPRISE.md
index 666fcf9..dcc5708 100644
--- a/REPRISE.md
+++ b/REPRISE.md
@@ -401,6 +401,15 @@ Réglage recommandé : **`DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1`** — 2,5× plus pet
 f32 pour deux centièmes de pour cent. Détail et reproduction :
 `reports/rapport-placement-bits-kv.md`.
 
+⚠️ **Mais le temps change le conseil** (mesuré au banc à 262 144 clés) : les clés
+f16 coûtent **2,3× le temps CPU** des clés f32 (162 contre 70 ms par passe), et le
+miroir VRAM — qui ramène l'attention à 1,7 ms par passe — **exige une disposition
+homogène**, donc toute variante d'attribution le désactive. Par régime : clés f16
+à contexte court ou moyen sur CPU ; **int8/int8 homogène** dès qu'on veut le miroir
+ou qu'on est à très long contexte. Et l'aiguille v2 retrouve **9/9** sondes dans
+les trois variantes, int8/int8 compris : la tâche est plus robuste que la
+perplexité ne le suggère.
+
 ### Le mode lot gagne sur les deux tableaux
 
 Chronométré sur 256 jetons, mac
… [5209 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-82 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && nice -n 5 cargo test --release -j 4 -- --test-threads=4 2>&1 | tail -45) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-82"}`

  ```
109 |     f_proj_warp: *mut c_void,
    |     ^^^^^^^^^^^

warning: method `kv_ecrire` is never used
   --> src/gpu.rs:416:12
    |
121 | impl Gpu {
    | -------- method in this implementation
...
416 |     pub fn kv_ecrire(&self, m: &mut KvGpu, kvh: usize, pos: usize,
    |            ^^^^^^^^^

warning: the `ids:` in this pattern is redundant
   --> src/main.rs:639:9
    |
639 |         ids: mut ids, ids_file, prompt, n: n_new, temp, top_p, topk, rep_pen, hist,
    |         ^^^^^^^^^^^^ help: use shorthand field pattern: `mut ids`
    |
    = note: `#[warn(non_shorthand_field_patterns)]` on by default

warning: `drave-core` (bin "drave" test) generated 18 warnings (run `cargo fix --bin "drave" -p drave-core --tests` to apply 9 suggestions)
    Finished `release` profile [optimized] target(s) in 0.01s
     Running unittests src/main.rs (target/release/deps/drave-9a06049b91b56c63)

running 17 tests
test list::tests_mxfp4::import_exact ... ok
test list::tests_q4::avx2_egale_scalaire ... ok
test list::tests_q6k::quarts_successifs ... ok
test model::tests_kv::aller_retour_kv ... ok
test tests_flux::entete_et_version_sont_ce_que_les_numeros_disent ... ok
test tests_flux::paires_blocs
… [904 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"DRAVE_KV_K_F32\\|DRAVE_KV_V_F32\\|DRAVE_KV_K_F16\\|DRAVE_KV_F16\" drave-core/src/ | head -40", "description": "Grep KV env vars"}`

  ```
drave-core/src/model.rs:806:    /// `DRAVE_KV_K_F32` ou `DRAVE_KV_K_F16` a réellement pris).
drave-core/src/model.rs:1059:    /// `DRAVE_KV_F16=1` : arrondir clés et valeurs en f16 avant quantification.
drave-core/src/model.rs:1061:    /// Attribution de l'écart int8 : `DRAVE_KV_K_F32=1` garde les CLÉS en f32
drave-core/src/model.rs:1062:    /// (l'erreur qui passe par les scores disparaît), `DRAVE_KV_V_F32=1` garde
drave-core/src/model.rs:1074:    /// `DRAVE_KV_K_F16=1` : les CLÉS sont stockées en f16, sans quantification
drave-core/src/model.rs:1101:        let (k_f32, v_f32) = (std::env::var("DRAVE_KV_K_F32").is_ok(),
drave-core/src/model.rs:1102:                              std::env::var("DRAVE_KV_V_F32").is_ok());
drave-core/src/model.rs:1103:        let k_f16 = bits < 32 && std::env::var("DRAVE_KV_K_F16").is_ok();
drave-core/src/model.rs:1105:                              f16_avant: std::env::var("DRAVE_KV_F16").is_ok(), k_f32, v_f32,
drave-core/src/model.rs:1209:        // `DRAVE_KV_F16=1` : clés et valeurs arrondies en demi-précision avant
  ```

### 🤖 Assistant

⏵ Lecture de la logique KV / miroir VRAM et de la condition d'homogénéité

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '780,830p' drave-core/src/model.rs && echo \"=====\" && sed -n '1050,1130p' drave-core/src/model.rs", "description": "Read KV config docs and parsing"}`

  ```
}
            self.servies += 1;
            return;
        }
        match self.listes.get(&cle) {
            Some((echelle, paires)) => {
                for v in dst.iter_mut() { *v = 0.0; }
                for &(i, q) in paires {
                    if (i as usize) < dst.len() { dst[i as usize] = q as f32 * *echelle; }
                }
                self.servies += 1;
            }
            None => self.manquantes += 1,
        }
    }
}

pub struct Model {
    pub g: Gguf,
    pub cfg: Cfg,
    pub layers: Vec<Layer>,
    pub out_norm: Vec<f32>,
    pub pool: Pool,
    /// cache KV, par couche : `[n_kv_head × ctx × head_dim]`, en f32 ou quantifié
    /// Caches KV, un par couche (pub : le tableau de bord `--options-actives`
    /// montre ce que le moteur utilise vraiment — et c'est là qu'on voit si
    /// `DRAVE_KV_K_F32` ou `DRAVE_KV_K_F16` a réellement pris).
    pub kv: Vec<KvCache>,
    pub ctx: usize,
    pub events: u64,
    /// Nombre de niveaux de quantification des **activations** (127 pour int8,
    /// 32767 pour int16). Les poids restent int8 : c'est la précision de
    /// l'activation qui décide de la fidélité au modèle flottant.
    pub act_levels: f32
… [5007 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1190,1290p' drave-core/src/model.rs", "description": "Read KV store selection"}`

  ```
#[inline]
    fn arrondi_f16(x: f32) -> f32 {
        let b = x.to_bits();
        if (b & 0x7F80_0000) >= 0x7F80_0000 { return x; }        // inf / NaN
        if (b & 0x7FFF_FFFF) < 0x3880_0000 { return 0.0 * x; }   // sous-normal f16
        f32::from_bits(b.wrapping_add(0x1000) & !0x1FFF)
    }

    /// Écrit un vecteur de clé et un de valeur à la position `pos`.
    #[inline]
    pub fn ecrire(&mut self, kvh: usize, pos: usize, k: &[f32], v: &[f32]) {
        if pos + 1 > self.cap { self.assurer(pos + 1); }
        let d = (kvh * self.cap + pos) * self.hd;
        if self.bits >= 32 {
            self.kf[d..d + self.hd].copy_from_slice(&k[..self.hd]);
            self.vf[d..d + self.hd].copy_from_slice(&v[..self.hd]);
            return;
        }
        let niv = if self.bits == 4 { 7.0 } else { 127.0 };
        // `DRAVE_KV_F16=1` : clés et valeurs arrondies en demi-précision avant
        // quantification (ce que fait llama.cpp pour son cache q8_0). L'arrondi
        // s'applique DANS les boucles : allouer des tampons ici fuirait à chaque
        // écriture (une par couche et par jeton).
        let f16a = self.f16_avant;
        let arr = |x: f32| if f16a { Self::arron
… [3885 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche du garde-fou « miroir VRAM » (les 4 variables)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"déporté désactivé\" drave-core/src/ | head && echo \"===\" && grep -n \"k_f16\\s*||\\|k_f32\\s*||\\|v_f32\\s*||\\|f16_avant\" drave-core/src/*.rs | head -40", "description": "Find mirror disable condition"}`

  ```
drave-core/src/model.rs:1652:                    println!("[gpu] KV déporté désactivé : les variantes d'attribution \
===
drave-core/src/main.rs:370:                 kv.f16_avant);
drave-core/src/model.rs:1060:    pub f16_avant: bool,
drave-core/src/model.rs:1105:                              f16_avant: std::env::var("DRAVE_KV_F16").is_ok(), k_f32, v_f32,
drave-core/src/model.rs:1213:        let f16a = self.f16_avant;
drave-core/src/model.rs:1650:                let mixte = caches_kv.iter().any(|c| c.k_f32 || c.v_f32 || c.k_f16);
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1600,1700p' drave-core/src/model.rs", "description": "Read KV mirror init"}`

  ```
// La tête N'EST PAS déportée en l'état : mesuré sur gpt-oss, elle passe
        // de 23 à 159 ms. Le noyau lit une ligne par fil, donc des adresses
        // distantes de 34 octets : chaque accès d'une même warp tombe dans une
        // ligne de cache différente. Il faut une warp par ligne avec réduction
        // — à écrire avant de réactiver.
        // Le noyau « une warp par ligne » rend le déport de la tête enfin
        // rentable : l'ancien lisait une ligne par fil (23 → 159 ms mesurés).
        // Opt-in : `DRAVE_GPU_TETE=1`.
        // Têtes liées de la famille Qwen en Q4_K_M : elles sont en **Q6_K**, pas
        // en Q8_0 — sans cette reconnaissance, `DRAVE_GPU_TETE=1` ne faisait rien
        // sur ces modèles (le noyau existait mais aucune tête ne lui était
        // présentée).
        let mut tete_gpu_q6k = false;
        let tete_gpu = if std::env::var("DRAVE_GPU_TETE").is_ok()
                          && crate::gpu::instance().is_some() {
            let machine = crate::gpu::instance();
            let charge = if let (Some(machine), Some((blocs, nb))) =
                (machine, g.q6k_blocks(&tete)) {
                tete_gpu_q6k = true;
                m
… [4804 caractères tronqués]
  ```

- **bash** `{"command": "nvidia-smi 2>&1 | head -15; echo \"---\"; ls /dev/dri 2>&1; echo \"---\"; ls ~/Data13TB/stephane/GitHub/Qtrinet/drave-core/gpu 2>/dev/null | head", "description": "Check GPU availability"}`

  ```
Wed Sep 30 17:04:10 2026       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.178.04             Driver Version: 580.178.04     CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  Quadro RTX 5000                On  |   00000000:03:00.0  On |                  Off |
| 33%   38C    P5             29W /  230W |    1399MiB /  16384MiB |     29%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
|   1  Quadro RTX 5000                On  |   00000000:04:00.0  On |                  Off |
| 33%   32C    P8             20W /  230W |     381MiB /  16384M
… [220 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de `forward`/`forward_lot` et de l'usage d'`emb_imposee`

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2985,3100p' drave-core/src/model.rs", "description": "Read forward with emb_imposee"}`

  ```
assert!(pos < self.ctx, "contexte dépassé ({pos} ≥ {})", self.ctx);
        self.jeton_trace += 1;
        // lus AVANT l'emprunt destructuré : la parcimonie par projection
        let tkp = self.act_topk_proj;
        let tkg = self.act_topk;
        let tk = |p: usize| if tkp[p] > 0 { tkp[p] } else { tkg };
        // Lus AVANT l'emprunt destructuré (comme la parcimonie par projection).
        let largeur_profil = self.cfg.ffn.max(self.cfg.ffn_exp);
        self.profil_jetons += 1;
        let Model { g, cfg, layers, out_norm, pool, kv, events, attn_events, kv_gpu,
                    attn_gpu_part, emb_imposee, .. } = self;
        let h = cfg.hidden;
        let hd = cfg.head_dim;
        let nh = cfg.n_head;
        let nkv = cfg.n_kv_head;
        let rep = nh / nkv;
        let ctx = self.ctx;

        // Injection : un vecteur imposé (embedding d'image) remplace la ligne
        // `token_embd` pour cet appel, et seulement pour lui — c'est le seul
        // ajout d'architecture que la vision demande au moteur.
        let mut x = match emb_imposee.take() {
            Some(v) => v,
            None => g.row_f32("token_embd.weight", tok as usize, h),
        };
        let
… [5322 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"R4\\|cumul\" docs/plan-prefill-reparti.md | head -40", "description": "Read R4 requirements in plan"}`

  ```
9:> disait, le code en écrivait quatre) ; et la règle R4 (plafond de 256 Mo) est
76:* **R4** — `n == 0` et `n × hidden × 4 > 256 Mo` sont refusés **avant**
322:  l'ordre des accumulations flottantes (mesuré 6e-5 à 4e-4 dans
395:   quoi l'ordre des accumulations diffère et l'écart vaut ~1e-4 pour un
  ```

### 🤖 Assistant

⏵ Lecture du rapport mode 4 et des commandes de reproduction

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mode4-lot-listes.md"}`

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
… [4587 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du rapport KV (placement des bits)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-placement-bits-kv.md"}`

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
… [8920 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du plan (règle R4) et du banc KV

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '60,100p' docs/plan-prefill-reparti.md && echo \"==== plan mode4 ====\" && grep -n \"R4\\|plafond\\|cumul\" docs/plan-mode4-lot-listes.md", "description": "Read R4 rule text"}`

  ```
```
corps = t × hidden × f32 LE, dans l'ordre des jetons
        l'état du jeton (position + j) commence à l'offset j × hidden × 4
```

Règles du corps :

* **R1** — `t = n ≥ 1`. Un lot d'un seul état est **accepté en réception**, mais
  l'émetteur DOIT utiliser le mode 0 pour un jeton seul : le chemin séquentiel de
  la génération reste ainsi intact, octet pour octet.
* **R2** — les positions sont **contiguës** : `position .. position + t`. Seule la
  base voyage ; c'est le contrat, et il est vérifié (§3).
* **R3** — la dimension n'est pas transmise : le récepteur lit `n × hidden × 4`
  octets avec SON `hidden`. Deux GGUF différents ne donnent pas une erreur au
  premier lot mais une désynchronisation (le message suivant échoue sur
  « magie de flux absente ») — le dire dans le message d'erreur.
* **R4** — `n == 0` et `n × hidden × 4 > 256 Mo` sont refusés **avant**
  l'allocation (`vec![0u8; …]` sur un en-tête corrompu est un OOM, pas une
  erreur de protocole).
* **R5** — la réponse est encodée **comme la demande** : même mode, même `n`,
  même `position`, mêmes `couche_debut`/`couche_fin`.

### 1.3 Compatibilité

* Un pair v2 et un pair v3 se refusent **au premier message**, su
… [2526 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"banc_kv\\|banc-kv\" drave-core/src/main.rs | head -20", "description": "Find banc-kv"}`

  ```
54:        (opt.banc_kv > 0, "--banc-kv"), (opt.gpu_banc, "--gpu-banc"),
67:    if opt.banc_kv > 0 { run_banc_kv(opt); return; }
398:    banc_kv: usize,
504:            "--banc-kv" => { o.banc_kv = suivant(i).parse().unwrap(); 2 }
2334:fn run_banc_kv(opt: Options) {
2348:    let n = opt.banc_kv;
  ```

### 🤖 Assistant

⏵ Lecture du §4 du plan et du banc KV

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '177,235p' docs/plan-mode4-lot-listes.md", "description": "Read plan section 4"}`

  ```
## 4. Le garde-fou de taille (R4) : champs et ordre exact

`PLAFOND_FLUX` vaut 256 Mo et `verifier_taille` est la seule porte. En mode 4,
**l'en-tête ne borne plus le corps** : `t` états peuvent annoncer chacun une
taille licite et faire, ensemble, n'importe quoi. Il faut donc deux niveaux.

Ordre de réception, **aucune allocation avant la vérification qui la couvre** :

1. Lire les 79 octets d'en-tête ; magie ; **version == 5** (refus immédiat,
   nommé) ; **mode == 4** (refus immédiat si inconnu, cf. §3).
2. `t = n` (offset 18). Refuser `t == 0` (« lot de listes vide »).
3. `verifier_taille(t·hidden·4, "lot de {t} états × {hidden} canaux")` — calculé
   avec `checked_mul(...).unwrap_or(usize::MAX)`, exactement comme le mode 3
   (main.rs:1743). C'est **la** borne de la mémoire vivante : le lot décodé est
   un `Vec<f32>` de `t·hidden`, alloué une seule fois juste après.
4. Allouer le lot plat `vec![0f32; t·hidden]` (remis à zéro : un état sans actif
   doit valoir zéro, pas du hasard).
5. Pour chaque état `j` de `0..t`, lire le préfixe de 12 octets puis, dans cet
   ordre :
   * `verifier_taille(a_j · 2, "état {j} : {a_j} paires")` — avant tout `Vec`
     d'indices/valeurs ; `sat
… [2293 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2334,2470p' drave-core/src/main.rs", "description": "Read run_banc_kv"}`

  ```
fn run_banc_kv(opt: Options) {
    use crate::model::{KvCache, Model};
    use std::time::Instant;
    let path = &modele_chemin();
    let g = Gguf::open(path).expect("ouverture du GGUF");
    let n_kv = g.cfg("attention.head_count_kv").and_then(|m| m.as_u64()).unwrap_or(1) as usize;
    let n_head = g.cfg("attention.head_count").and_then(|m| m.as_u64()).unwrap_or(1) as usize;
    let hidden = g.cfg("embedding_length").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
    let hd = match g.cfg("attention.key_length").and_then(|m| m.as_u64()) {
        Some(v) if v > 0 => v as usize,
        _ => hidden / n_head.max(1),
    };
    let n_layer = g.cfg("block_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
    let bits = std::env::var("DRAVE_KV_BITS").ok().and_then(|v| v.parse().ok()).unwrap_or(32u32);
    let n = opt.banc_kv;
    let rep = (n_head / n_kv.max(1)).max(1);
    let scale = 1.0 / (hd as f32).sqrt();
    println!("banc KV : {n} clés · {n_layer} couches · {n_kv} têtes KV × {hd} dim, {rep} têtes de requête par tête KV · KV {} bits",
             if bits >= 32 { "f32".to_string() } else { bits.to_string() });

    // 1. Cache CPU d'UNE couche, rempli de façon déterminis
… [5668 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de `vers_gpu`, `cle`/`valeur` et du support GPU des variantes

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1290,1420p' drave-core/src/model.rs", "description": "Read cle/valeur/vers_gpu"}`

  ```
pub fn vers_gpu(&self, machine: &crate::gpu::Gpu, m: &mut crate::gpu::KvGpu,
                    kvh: usize, pos: usize) -> bool {
        self.vers_gpu_tranche(machine, m, kvh, pos, 1)
    }

    /// Recopie vers la VRAM les `t` positions nouvellement écrites de la couche
    /// `l`. Silencieux quand aucun miroir n'est installé.
    pub fn miroir_gpu(miroirs: Option<&mut [(usize, crate::gpu::KvGpu)]>, l: usize,
                      kvc: &KvCache, pos0: usize, t: usize) {
        let Some((idx, m)) = miroirs.and_then(|v| v.get_mut(l)) else { return };
        let machines = crate::gpu::machines();
        let Some(machine) = machines.get(*idx) else { return };
        for kvh in 0..kvc.n_kv {
            kvc.vers_gpu_tranche(machine, m, kvh, pos0, t);
        }
    }

    /// Déquantifie la clé `(kvh, t)` dans `dst`.
    #[inline]
    pub fn cle(&self, kvh: usize, t: usize, dst: &mut [f32]) {
        let d = (kvh * self.cap + t) * self.hd;
        if self.bits >= 32 { dst[..self.hd].copy_from_slice(&self.kf[d..d + self.hd]); return; }
        if self.k_f32 {
            let d = (kvh * self.cap + t) * self.hd;
            dst[..self.hd].copy_from_slice(&self.kf[d..d + self.hd]);
 
… [5830 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fn kv_allouer\" -A 40 drave-core/src/gpu.rs", "description": "Read kv_allouer"}`

  ```
319:    pub fn kv_allouer(&self, n_kv: usize, ctx: usize, hd: usize, bits: u32) -> Option<KvGpu> {
320-        cu_ctx(self.ctx);
321-        let nb = hd.div_ceil(32).max(1);
322-        // Première tranche : de quoi couvrir un préremplissage courant. Le
323-        // reste s'ajoute par doublement, à la demande.
324-        let mut m = KvGpu { k: 0, v: 0, sk: 0, sv: 0, n_kv, ctx, capacite: 0, hd, nb, bits,
325-                            octets: 0, q_dev: 0, part_dev: 0, out_dev: 0, sinks_dev: 0,
326-                            q_cap: 0, part_cap: 0, out_cap: 0, sinks_cap: 0 };
327-        if !self.kv_assurer(&mut m, ctx.min(2048)) { return None; }
328-        Some(m)
329-    }
330-
331-    /// Garantit `besoin` positions allouées. Double la capacité (et COPIE ce qui
332-    /// était écrit : le cache est déjà rempli) jusqu'à couvrir la demande.
333-    pub fn kv_assurer(&self, m: &mut KvGpu, besoin: usize) -> bool {
334-        cu_ctx(self.ctx);
335-        if besoin <= m.capacite { return true; }
336-        let mut cap = m.capacite.max(1);
337-        while cap < besoin { cap = (cap * 2).min(m.ctx); }
338-        let pas = match m.bits { 32 => m.hd * 4, 8 => m.hd, 4 => m.hd / 2,
… [1357 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inventaire des options CLI pour les bancs répartis

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '30,120p' drave-core/src/main.rs && echo \"=== options ppl ===\" && grep -n '\"--ppl\"\\|\"--pair\"\\|\"--serveur-flux\"\\|\"--limit\"\\|\"--ctx\"\\|\"--ids\"\\|\"--dense\"\\|\"--flux-blocs\"\\|\"--lot\"\\|\"--flux-liste\"' dr … [86 caractères tronqués]`

  ```
eprintln!("usage: drave-core <modele.gguf> [--matrix NOM] [--threads N]");
        eprintln!("       drave-core <modele.gguf> --infer (--ids 1,2,3 | --prompt TEXTE)");
        eprintln!("                    [--n 32] [--temp 0] [--ctx 512] [--threads N]");
        std::process::exit(1);
    }
    // Une seule analyse, puis un aiguillage : `--plan`, `--tokenize`,
    // `--ppl`/`--ppl-texte` et `--infer` partagent désormais la même structure
    // d'options, donc les mêmes drapeaux.
    // Les variables d'environnement ont été renommées QT_* -> DRAVE_* : un
    // ancien nom encore présent dans un script ne ferait RIEN, en silence. On le
    // dit, plutôt que de laisser croire que l'option est active.
    if let Some((vieux, _)) = std::env::vars().find(|(k, _)| k.starts_with("QT_")) {
        eprintln!("[attention] {vieux} est l'ancien nom d'une variable d'environnement : \
elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.");
    }
    let opt = analyser(&args);
    let _ = MODELE.set(args[1].clone());
    // Plusieurs modes demandés : l'aiguillage en retient UN, dans un ordre
    // arbitraire, et le disait pas. On le dit.
    let modes: Vec<&str
… [4313 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche d'un fichier d'ids existant et du format attendu

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls data/ 2>/dev/null | head -20; ls /tmp/*.txt /tmp/ids* 2>/dev/null | head -20; echo \"---\"; grep -n \"fn lire_ids\\|ids_file\" drave-core/src/main.rs | head -20", "description": "Look for ids corpus files"}`

  ```
wikitext2_test.txt
wt2.json
/tmp/all_hunks.txt
/tmp/all_vars.txt
/tmp/attn512.txt
/tmp/bench_blk.0.attn_q.weight.txt
/tmp/bench_blk.0.ffn_down.weight.txt
/tmp/bench_gate.txt
/tmp/bras.txt
/tmp/cap_url.txt
/tmp/code_env.txt
/tmp/code_flags.txt
/tmp/code_vars.txt
/tmp/compB.txt
/tmp/ctrl_q2.txt
/tmp/ctrl_qr2.txt
/tmp/ctrl_question.txt
/tmp/ctrl_r2.txt
/tmp/ctrl_reponse.txt
/tmp/dc.txt
/tmp/description.txt
/tmp/dh.txt
---
437:    ids: Vec<u32>, ids_file: Option<String>, texte_file: Option<String>,
498:            "--ppl" => { o.ppl = true; o.ids_file = Some(suivant(i).clone()); 2 }
519:            "--ids-file" => { o.ids_file = Some(suivant(i).clone()); 2 }
639:        ids: mut ids, ids_file, prompt, n: n_new, temp, top_p, topk, rep_pen, hist,
768:    if let Some(f) = &ids_file {
3135:        ids_file: idfile, texte_file, ppl_texte: _, limit, depuis,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2057,2100p' drave-core/src/main.rs", "description": "Read start of run_ppl_reparti"}`

  ```
fn run_ppl_reparti(opt: Options, pair: &str) {
    use std::time::Instant;
    let chemin = modele_chemin();
    let ctx = if opt.ctx_impose { opt.ctx } else { 256 };
    let limite = opt.limit.max(1).min(ctx);
    let couches_locales = if opt.couches_locales > 0 { opt.couches_locales } else { 12 };
    // `--lot T` : préremplissage par LOTS sur le fil. La référence locale est
    // alors calculée avec le MÊME découpage — sinon l'écart mesurerait la
    // différence entre deux ordres de sommation, pas celle du découpage.
    let lot = opt.lot.max(1);
    let mut mdl = model::Model::load(&chemin, ctx, fils(&opt), true, opt.keep, false, 0, 0);
    appliquer_quantification(&mut mdl, &opt);
    if opt.options_actives { options_actives(&mdl, "pilote du flux", opt.ctx_impose, true, opt.keep); }
    let mode = if opt.flux_blocs { MODE_BLOCS }
               else if opt.flux_liste { MODE_LISTE }
               else { MODE_DENSE };
    // Le mode des LOTS est distinct : `--flux-blocs` donne le mode 4 (lot en
    // listes), tout le reste donne le mode 3 (lot dense f32). Déclaré ici pour
    // que l'affichage du transport, plus bas, le connaisse.
    let mode_lot = if mode == MODE_BLOCS {
… [1189 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du parseur d'options (noms exacts des drapeaux)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '480,600p' drave-core/src/main.rs", "description": "Read option parser"}`

  ```
};
    let cpu = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(8);
    o.ctx = 512;
    o.threads = (cpu * 3 / 4).max(1);
    let suivant = |i: usize| -> &String {
        args.get(i + 1).unwrap_or_else(|| panic!("{} attend une valeur", args[i]))
    };
    let mut i = 2;
    while i < args.len() {
        // CHAQUE branche rend le nombre d'arguments consommés (1 pour un
        // drapeau booléen, 2 pour un drapeau à valeur). Un `i += 2` global
        // sautait le drapeau suivant après un booléen : `--dense --threads 8
        // --ctx 128` perdait `--threads` ET `--ctx`, donc on mesurait 30 fils
        // sur un contexte de 256 en croyant mesurer 8 fils sur 128 — et la
        // barrière tournante partait en livelock. C'est la même classe de bug
        // que les boucles triplées, en pire : silencieuse.
        let pas = match args[i].as_str() {
            "--infer" => { o.infer = true; 1 }
            "--ppl" => { o.ppl = true; o.ids_file = Some(suivant(i).clone()); 2 }
            "--ppl-texte" => { o.ppl = true; o.ppl_texte = true;
                               o.texte_file = Some(suivant(i).clone()); 2 }
            "--plan" => { o.plan = true; 1 }
  
… [6709 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extraction des constantes du protocole

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"MAGIE_FLUX\\|VERSION_FLUX\\|const MODE_\" drave-core/src/main.rs | head -12 && echo \"=== envoyer_flux ===\" && sed -n '1652,1746p' drave-core/src/main.rs", "description": "Read protocol constants and envoyer_flux"}`

  ```
1372:const MAGIE_FLUX: u32 = 0x4452_5631;   // "DRV1"
1385:const VERSION_FLUX: u8 = 5;
1387:const MODE_DENSE: u8 = 0;
1391:const MODE_LISTE: u8 = 1;
1396:const MODE_BLOCS: u8 = 2;
1402:const MODE_LOT: u8 = 3;
1409:const MODE_LOT_LISTES: u8 = 4;
1572:    t.extend_from_slice(&MAGIE_FLUX.to_le_bytes());
1573:    t.push(VERSION_FLUX);
1752:    if u(0) != MAGIE_FLUX {
1758:    if version != VERSION_FLUX {
1761:            format!("flux en version {version}, cette build parle la {VERSION_FLUX} \
=== envoyer_flux ===
fn envoyer_flux(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos: u32,
                actifs: &[f32], mode: u8, mdl: Option<&model::Model>)
                -> std::io::Result<(usize, usize)> {
    use std::io::Write;
    let (n, echelle, corps): (usize, f32, Vec<u8>) = if mode == MODE_BLOCS {
        let (idx, val, echelles) = mdl.expect("modèle requis pour quantifier un flux")
                                      .flux_en_liste_blocs(actifs);
        // Indices par ÉCARTS : la liste est triée (les blocs sont parcourus dans
        // l'ordre), donc l'écart au neurone précédent tient sur un octet dans
        // l'immense majorité des cas — 255 est l'échappement vers 
… [3894 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Écriture des scripts hostiles dans /tmp

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/target/release/drave && mkdir -p /tmp/adv && echo ok", "description": "Check binary and create workdir"}`

  ```
-rwxr-xr-x. 2 stephane stephane 1603096 30 sep 16:01 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/target/release/drave
ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1560,1600p' drave-core/src/main.rs | head -5; grep -n \"fn decoder_paires_blocs\" -A 40 drave-core/src/main.rs", "description": "Read decoder_paires_blocs"}`

  ```
/// position, `n`, échelle, et le contrat d'activation.
///
/// **Une seule fonction pour les trois émetteurs**, et c'est délibéré : la
/// duplication de cette construction est exactement ce qui a produit l'en-tête
/// d'un octet trop long (40 écrits pour 39 lus), invisible pendant des flux
1616:fn decoder_paires_blocs(corps: &[u8], n: usize) -> Result<(Vec<u16>, Vec<i8>), String> {
1617-    // `n` vient de l'en-tête : deux `with_capacity(n)` sur 4 milliards de paires
1618-    // demandaient 12 Gio AVANT de découvrir que le corps était tronqué (mesuré :
1619-    // VmPeak 12 477 Mio). Le plafond s'applique donc ici aussi.
1620-    if n.saturating_mul(2) > PLAFOND_FLUX {
1621-        return Err(format!("{n} paires annoncées : au-delà du plafond de {} Mo",
1622-                           PLAFOND_FLUX >> 20));
1623-    }
1624-    let mut idx = Vec::with_capacity(n.min(1 << 20));
1625-    let mut val = Vec::with_capacity(n.min(1 << 20));
1626-    let mut prev = 0u32;
1627-    let mut lus = 0usize;
1628-    while idx.len() < n {
1629-        if lus + 1 >= corps.len() {
1630-            return Err(format!("corps de flux tronqué : {} paires lues sur {n}", idx.len()));
1631-        }
1632
… [1335 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Écriture du harnais hostile (serveur + client factice)

- **write** `{"file_path": "/tmp/adv/flux.py", "content": "#!/usr/bin/env python3\n\"\"\"Harnais adversarial pour le protocole de flux Drave (v5).\n\nNe modifie AUCUN fichier du depot : tout vit dans /tmp.\n\"\"\"\nimport os, socket, struct, subprocess, sys, time, signal\n\nREPO = \"/home/stephane/Data13TB/steph … [3409 caractères tronqués]`

  ```
<path>/tmp/adv/flux.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Test A : trames forgées contre le serveur (3 crashs candidats)

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Test A : le SERVEUR face a des trames forgees bien formees mais incoherentes.\"\"\"\nimport socket, struct, sys, time\nsys.path.insert(0, \"/tmp/adv\")\nfrom flux import *\n\nPORT = 5611\n\n\ndef essai(nom, trame, ctx=64, attendu=None):\n    p = lancer_serv … [2921 caractères tronqués]`

  ```
<path>/tmp/adv/testA_serveur.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Exécution du test A (trames forgées contre le serveur)

- **bash** `{"command": "cd /tmp/adv && sed -i 's/^PORT = 5611$/PORT = [5611]/; s/def essai(nom, trame, ctx=64, attendu=None):/def essai(nom, trame, ctx=64, attendu=None):\\n    global PORT\\n    PORT[0] += 1/; s/lancer_serveur(PORT, ctx=ctx)/lancer_serveur(PORT[0], ctx=ctx)/; s/create_connection((\"127.0.0.1\" … [175 caractères tronqués]`

  ```
=== mode 1 (LISTE) · n=1 · pos=100000 (ctx 64) ===
  envoi      : 83 octets
  reception  : reponse du serveur : 0 octets (mode=?, n=?)
  serveur    : code=-6 signal=6
    | [flux] client connecté : 127.0.0.1:27174
    | thread 'main' (760182) panicked at src/model.rs:2985:9:
    | contexte dépassé (100000 ≥ 64)
    | note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace

=== mode 1 (LISTE) · n=1 · fin=200 (24 couches) ===
  envoi      : 83 octets
  reception  : reponse du serveur : 0 octets (mode=?, n=?)
  serveur    : code=-6 signal=6
    | [flux] client connecté : 127.0.0.1:38908
    | thread 'main' (760221) panicked at src/model.rs:3046:30:
    | index out of bounds: the len is 24 but the index is 24
    | note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace

=== mode 0 (DENSE) · n=897 > hidden=896 ===
  envoi      : 3667 octets
  reception  : reponse du serveur : 0 octets (mode=?, n=?)
  serveur    : code=-6 signal=6
    | [flux] client connecté : 127.0.0.1:64848
    | thread 'main' (760300) panicked at src/model.rs:2204:53:
    | index out of bounds: the len is 896 but the index is 896
    | note: run with `RUST_BACKTRACE=1` env
… [1380 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Localisation des 3 sites de panique (mode 0, dimension)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '3300,3325p' drave-core/src/model.rs && echo \"=== 3036,3050 ===\" && sed -n '3036,3050p' drave-core/src/model.rs", "description": "Read panic sites"}`

  ```
for &t in iter { sc[t as usize] *= inv; }
                // somme pondérée : on accumule par clé dans le vecteur de sortie,
                // ce qui lit vc séquentiellement au lieu de le parcourir à stride.
                let out = &mut att[hh * hd..(hh + 1) * hd];
                for v in out.iter_mut() { *v = 0.0; }
                for &t in iter {
                    let w = sc[t as usize];
                    kvc.valeur(kvh, t as usize, &mut vd);
                    for (o, x) in out.iter_mut().zip(vd.iter()) { *o += w * x; }
                }
            }
            self.prof[2] += ta.elapsed().as_secs_f64();
            let tf = Instant::now();
            Self::matvec(pool, &lay.wo, &att, &mut o, events, self.act_levels, self.act_thresh, tk(3), self.act_renorm, &mut scratch, self.seuil_push);
            for i in 0..h { o[i] += x[i]; }
            Self::rmsnorm(&o, &lay.ffn_norm, cfg.eps, &mut hn);
            if let Some(r) = self.flux_force.as_mut() {
                let j = self.jeton_trace;
                r.appliquer(l + 1000, j as usize, &mut hn);
            } else if self.trace.is_some() {
                let mut tmp = Vec::with_capacity(h);
                if l
… [1359 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test B : réponses hostiles contre le client (chemin non-lot)

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Test B : le CLIENT (--ppl-reparti) face a un serveur factice hostile.\n\nLe client demande en mode 0 (dense) ; le serveur factice repond n'importe quoi.\n\"\"\"\nimport socket, struct, subprocess, sys, threading, time\nsys.path.insert(0, \"/tmp/adv\")\nfrom … [4261 caractères tronqués]`

  ```
<path>/tmp/adv/testB_client.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Exécution du test B (client vs serveur factice)

- **bash** `{"command": "cd /tmp/adv && timeout 900 python3 testB_client.py 2>&1 | tail -80", "description": "Run hostile response tests"}`

  ```
=== controle · reponse mode 0 · n=896 ===
  requetes recues par le faux serveur : [(0, 896), (0, 896), (0, 896), (0, 896), (0, 896)]
  client : code=0 signal=None
    |   deux nœuds        : perplexité 333160063.9550  (0.2 s)
    |   écart             : 3.25e6
    |   transport         : dense f32 · 3663 octets par flux (aller) · 3663 au retour · 100.0 % d'activité (896 neurones par flux) · 5 flux
    |   temps             : 23.8 ms par jeton en local · 0.3 ms à attendre le pair (son calcul + l'aller-retour) · soit 0.01× le calcul local seul
    | [attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
    | [modele] 24 couches chargées en 818.593986ms — listes 0.00 Go , 4 threads

=== rep. mode 0 · n=897 > hidden ===
  requetes recues par le faux serveur : [(0, 896)]
  client : code=-6 signal=6
    |   référence locale  : perplexité 102.6664  (0.4 s)
    | [attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
    | [modele] 24 couches chargées en 803.077723ms — listes 0.
… [3874 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des diffs f28c60a et 0259bf1

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show f28c60a --stat && git show f28c60a -- drave-core/src | head -80 && echo \"###############\" && git show 0259bf1 --stat", "description": "Show f28c60a and 0259bf1"}`

  ```
commit f28c60a5f633f6733add2a51e8dff2dfc43442b3
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 16:17:23 2026 -0400

    Mode 4 : le plafond cumulatif vérifié à l'octet près
    
    Le relecteur avait prouvé qu'il manquait ; voici la preuve qu'il marche : avec des
    états bien formés au maximum légal (896 actifs, 3 708 octets) et 74 898 états
    annoncés — donc une borne nominale qui passe —, le serveur refuse à l'état 72 393,
    exactement le point de franchissement des 256 Mo, en nommant le cumul.

 journal/sessions/MANIFEST.md                       |  4 +-
 .../bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md | 66 ++++++++++++++++++++++
 .../rapport.md                                     | 17 +++---
 reports/rapport-mode4-lot-listes.md                |  8 ++-
 4 files changed, 84 insertions(+), 11 deletions(-)
commit f28c60a5f633f6733add2a51e8dff2dfc43442b3
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 16:17:23 2026 -0400

    Mode 4 : le plafond cumulatif vérifié à l'octet près
    
    Le relecteur avait prouvé qu'il manquait ; voici la preuve qu'il marche : avec des
    états bien formés au maximum légal (896 actifs, 3 708 octets) et 74 898 états
    an
… [944 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show f28c60a -- reports/rapport-mode4-lot-listes.md && echo \"#############\" && git show 0259bf1 -- reports/rapport-prefill-reparti.md", "description": "Show report changes"}`

  ```
commit f28c60a5f633f6733add2a51e8dff2dfc43442b3
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 16:17:23 2026 -0400

    Mode 4 : le plafond cumulatif vérifié à l'octet près
    
    Le relecteur avait prouvé qu'il manquait ; voici la preuve qu'il marche : avec des
    états bien formés au maximum légal (896 actifs, 3 708 octets) et 74 898 états
    annoncés — donc une borne nominale qui passe —, le serveur refuse à l'état 72 393,
    exactement le point de franchissement des 256 Mo, en nommant le cumul.

diff --git a/reports/rapport-mode4-lot-listes.md b/reports/rapport-mode4-lot-listes.md
index f39966c..4c1bc7d 100644
--- a/reports/rapport-mode4-lot-listes.md
+++ b/reports/rapport-mode4-lot-listes.md
@@ -67,7 +67,13 @@ choses que le banc ne voyait pas :
 
 1. **le plafond R4 n'était pas cumulatif** : chaque état pouvait être légal et le
    total ne pas l'être — un pair annonçait 268 Mo par état sur 74 898 états
-   (~19 Po). La mémoire restait bornée (on décode état par état), le temps non ;
+   (~19 Po). La mémoire restait bornée (on décode état par état), le temps non.
+   **Vérifié après correction**, avec des états bien formés au maximum légal
+   (896 actifs, 3 708
… [1831 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test C : contrôle liste vide (mode 2, seuil 1.0) + comptabilité par lots

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Test C : serveur REEL + client REEL.\n\n1. --flux-blocs --act-thresh 1.0 (listes vides, l'ancienne session qui mourait)\n2. --lot 16 --limit 20 (comptabilite : 2 lots, 20 jetons)\n\"\"\"\nimport re, subprocess, sys, time\nsys.path.insert(0, \"/tmp/adv\")\nf … [2028 caractères tronqués]`

  ```
<path>/tmp/adv/testC_reel.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Exécution du test C (client/serveur réels)

- **bash** `{"command": "cd /tmp/adv && timeout 900 python3 testC_reel.py 2>&1 | tail -50", "description": "Run real client/server tests"}`

  ```
=== mode 2 · --act-thresh 1.0 (listes vides) (client en 2.1 s, code 0) ===
    |   référence locale  : perplexité 151936.0000  (0.9 s)
    |   deux nœuds        : perplexité 151936.0000  (0.4 s)
    |   écart             : 0.00e0
    |   transport         : listes à échelle par bloc (2 octets/actif, écarts) · 199 octets par flux (aller) · 199 au retour · 0.0 % d'activité (0 neurones par flux) · 19 flux
    |   temps             : 17.1 ms par jeton en local · 2.6 ms à attendre le pair (son calcul + l'aller-retour) · soit 0.15× le calcul local seul

=== --lot 16 · limit 20 (2 lots) (client en 3.0 s, code 0) ===
    |   référence locale  : perplexité 144.3267  (1.1 s)
    |   deux nœuds        : perplexité 886458700.4678  (1.1 s)
    |   écart             : 6.14e6
    |   transport         : lot dense f32 · lots de 16 jetons au plus · 35919 octets par lot (aller) · 3.5 ko par jeton · 2 lots pour 20 jetons
    |   temps             : 219.6 ms par LOT en local · 261.8 ms à attendre le pair · soit 1.19× le calcul local seul
  VERIF arithmetique : 35919 × 2 = 71838 octets ; 71838/20/1024 = 3.5077 ko/jeton (annonce 3.5)

=== --lot 1000 · limit 20 (1 lot) (client en 3.0 s, code 0) ===
    |
… [413 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification : le mode 3 donnerait 6e6 d'écart — lecture du rapport prefill

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' reports/rapport-prefill-reparti.md", "description": "Read prefill report"}`

  ```
# Phase 3.4 — le préremplissage par LOTS sur le fil

**En une ligne** : un préremplissage de 256 jetons traverse désormais le réseau en
**4 lots** (ou un seul) au lieu de 255 flux, et le calcul coupé redonne exactement
le calcul local — **écart 0,00e0**.

## Le problème

Le transport était séquentiel : un flux par jeton, donc un aller-retour par jeton.
Un préremplissage de N jetons payait N fois la latence, alors que la latence est
précisément le seul poste qui compte (`attente ≈ calcul distant + 3,2 × latence
par message`, mesuré dans `reports/rapport-transport-liste.md`). Avec 60 ms
d'aller-retour, 256 jetons coûtaient 15 secondes d'attente pure.

## Le mode 3 du protocole

```
en-tête   magie u32 · version u8 (4) · mode u8 (3 = LOT) · plage (2 × u32)
          position u32 (celle du PREMIER jeton) · n u32 (nombre d'ÉTATS)
          échelle f32 · et le contrat d'activation (niveaux, seuil, top-k,
          renorm, 7 top-k par projection, attn/qk/moe top-k)
corps     n × dimension × f32        ← la dimension ne voyage pas
```

`n` est le nombre d'**états**, pas de canaux : chaque nœud connaît la dimension
par son modèle, et les deux doivent charger le même GGUF. La réponse est enc
… [2506 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"o.keep\" drave-core/src/main.rs | head && echo \"=== forward_lot ===\" && sed -n '2320,2420p' drave-core/src/model.rs", "description": "Read keep default and forward_lot"}`

  ```
542:            "--keep" => { o.keep = suivant(i).parse().unwrap(); 2 }
=== forward_lot ===
    pub fn forward_lot(&mut self, toks: &[u32], pos0: usize) -> Vec<Vec<f32>> {
        let t = toks.len();
        // Lot IMPOSÉ (préremplissage réparti) : les états arrivent de l'autre
        // nœud, on ne repasse pas par `token_embd`. Lu avant tout le reste — y
        // compris avant le retour anticipé sur `t == 0`, sinon une trame vide
        // laissait l'état imposé en place pour le lot suivant (D7 de la
        // relecture) — et consommé une seule fois, comme `emb_imposee` pour un
        // jeton seul.
        let impose = self.emb_imposee_lot.take();
        if t == 0 { return Vec::new(); }
        if t == 1 {
            if let Some(v) = impose { self.emb_imposee = Some(v); }
            // Le jeton n'est PAS lu quand un état est imposé : `forward` prend
            // `emb_imposee` et n'appelle jamais `token_embd`. `toks` peut donc
            // être vide côté nœud distant, qui ne connaît que des états.
            //
            // Le raccourci sort AVANT l'avance du compteur : `forward` avance le
            // sien. Le faire avancer ici aussi doublait la clé à chaque jet
… [4045 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test : l'écart mode 3 est-il dû à mon `--keep 0` ?

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"keep\" drave-core/src/main.rs | grep -v \"^\\s*//\" | head -20 && echo \"=== struct default ===\" && grep -n \"impl Default for Options\" -A 25 drave-core/src/main.rs | head -30", "description": "Find keep default"}`

  ```
345:/// (`--keep` en perplexité, `--ffn-gain` en inférence, les top-k dans les modes
350:fn options_actives(mdl: &model::Model, mode: &str, ctx_impose: bool, dense: bool, keep: f32) {
352:    println!("[options] mode {mode} · contexte {} ({}) · dense {} · keep {:.3}",
353:             mdl.ctx, oui(ctx_impose), dense, keep);
448:    q4: u8, b6: u8, keep: f32, bits: u32, moe_topk: usize, pin: bool,
476:        hebb_out: String::from("hebb.bin"), keep: 1.0, abits: 8,
542:            "--keep" => { o.keep = suivant(i).parse().unwrap(); 2 }
593:                // `--xxx` bien sûr, mais aussi `-keep` (un seul tiret) : c'est une
642:        keep, attn_window, swa_pattern, sans_fenetre, attn_sinks, attn_topk, qk_topk,
654:    let mut mdl = model::Model::load(path, ctx, n_threads, dense, keep, auto, q4, b6);
708:        options_actives(&mdl, "inférence", ctx_impose, dense, keep);
1960:    let mut mdl = model::Model::load(&chemin, ctx, fils(&opt), true, opt.keep, false, 0, 0);
1962:    if opt.options_actives { options_actives(&mdl, "nœud moteur du flux", opt.ctx_impose, true, opt.keep); }
2067:    let mut mdl = model::Model::load(&chemin, ctx, fils(&opt), true, opt.keep, false, 0, 0);
2069:  
… [433 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/adv && python3 - <<'EOF' 2>&1 | tail -30\nimport sys, time, subprocess\nsys.path.insert(0,\"/tmp/adv\")\nfrom flux import *\nPORT=5850\nsrv = lancer_serveur(PORT, ctx=64)   # sans --keep\nlignes = attendre_ecoute(srv)\ncmd = [BIN, MODEL, \"--ppl-reparti\", f\"127.0.0.1:{PORT}\", … [372 caractères tronqués]`

  ```
code 0
 |   référence locale  : perplexité 144.3267  (1.0 s)
 |   deux nœuds        : perplexité 144.3267  (1.1 s)
 |   écart             : 0.00e0
 |   transport         : lot dense f32 · lots de 16 jetons au plus · 35919 octets par lot (aller) · 3.5 ko par jeton · 2 lots pour 20 jetons
  ```

### 🤖 Assistant

⏵ Vérification de la RAM disponible pour le test du plafond cumulatif

- **bash** `{"command": "free -g && echo \"---\" && nproc && ulimit -v", "description": "Check available memory"}`

  ```
total        used        free      shared  buff/cache   available
Mem:             125          10          56           1          61         114
Swap:             62          17          45
---
40
unlimited
  ```

### 🤖 Assistant

⏵ Test D : le plafond cumulatif se réinitialise-t-il à chaque flux ?

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Test D : le plafond R4 'cumulatif' du mode 4 face a PLUSIEURS flux.\n\nChaque flux reste sous 256 Mo ; le total depasse largement 256 Mo.\nOn lit aussi le VmRSS du serveur apres chaque flux (fuite de `plat` ?).\n\"\"\"\nimport os, socket, struct, subprocess … [2124 caractères tronqués]`

  ```
<path>/tmp/adv/testD_plafond.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Exécution du test D (8 flux mode 4, cap cumulatif)

- **bash** `{"command": "cd /tmp/adv && timeout 600 python3 testD_plafond.py 2>&1 | tail -30", "description": "Run cumulative cap test"}`

  ```
corps d'un flux : 37080000 octets (35.4 Mo) ; 8 flux = 282.9 Mo
Traceback (most recent call last):
  File "/tmp/adv/testD_plafond.py", line 50, in <module>
    b = s.recv(min(1 << 20, a_lire - lu))
TimeoutError: timed out
  ```

### 🤖 Assistant

⏵ Nettoyage et inspection des bornes de boucle de `forward_lot`

- **bash** `{"command": "pgrep -af \"drave.*flux-serveur\" | head; echo \"---\"; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"couche_debut\\|couche_fin\" drave-core/src/model.rs | head -20", "description": "Check leftover servers and loop bounds"}`

  ```
761832 bash -c pgrep -af "drave.*flux-serveur" | head; echo "---"; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n "couche_debut\|couche_fin" drave-core/src/model.rs | head -20
---
931:    pub couche_debut: usize,
932:    pub couche_fin: usize,
937:    /// flux (`couche_fin >= n_layer`) et le pilote le normait une SECONDE fois :
1773:            couche_debut: 0, couche_fin: n_layer_total, flux_brut: false,
2056:        for l in self.couche_debut..self.couche_fin {
2089:                for l in self.couche_debut..self.couche_fin {
2426:        for l in self.couche_debut..self.couche_fin {
2803:        if self.flux_brut || self.couche_fin < self.cfg.n_layer {
2881:        for l in self.couche_debut..self.couche_fin {
2960:        if self.couche_fin >= self.cfg.n_layer && !self.flux_brut {
3039:        // La plage PORTÉE par ce nœud (`couche_debut..couche_fin`), et non
3045:        for l in self.couche_debut..self.couche_fin {
3482:        if self.flux_brut || self.couche_fin < cfg.n_layer {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2780,2830p' drave-core/src/model.rs && echo \"=== fin de forward_lot ===\" && sed -n '2860,2900p' drave-core/src/model.rs", "description": "Read end of forward_lot"}`

  ```
}
                }
                for i in 0..t {
                    let g0 = gate[i * self.cfg.ffn..(i + 1) * self.cfg.ffn].to_vec();
                    let u0 = up[i * self.cfg.ffn..(i + 1) * self.cfg.ffn].to_vec();
                    let mut gg = g0;
                    Self::activation(&mut gg, &u0, self.cfg.ffn, self.cfg.ffn_act_oss);
                    gate[i * self.cfg.ffn..(i + 1) * self.cfg.ffn].copy_from_slice(&gg);
                }
                quantifier(&gate, &mut gi, &mut sg, self.act_levels, self.act_thresh);
                {
                    let d8 = self.layers[l].wdown.d.as_ref().expect("projection dense requise");
                    self.pool.gemm_dense_i8(d8, &gi, t, &sg, &mut yl[..d8.n_out * t]);
                }
                for i in 0..t {
                    for oo in 0..h {
                        down[i * h + oo] = yl[oo * t + i];
                        x[i * h + oo] = o[i * h + oo] + down[i * h + oo];
                    }
                }
            }
            self.prof[3] += t_ffn.elapsed().as_secs_f64();
        }
        if self.flux_brut || self.couche_fin < self.cfg.n_layer {
            // Nœud intermédiaire : on rend le f
… [3752 caractères tronqués]
  ```

- **bash** `{"command": "pgrep -af \"target/release/drave\" ; echo \"(fin pgrep)\"", "description": "Check for leftover drave processes"}`

  ```
761852 bash -c pgrep -af "target/release/drave" ; echo "(fin pgrep)"
(fin pgrep)
  ```

### 🤖 Assistant

⏵ Diagnostic du test D (réponse plus courte que prévu ?)

- **bash** `{"command": "cd /tmp/adv && python3 - <<'EOF' 2>&1 | tail -30\nimport socket, struct, subprocess, sys, time\nsys.path.insert(0,\"/tmp/adv\")\nfrom flux import *\nPORT=5905; T=2000; CTX=65536\npaires=(b\"\\xff\\x00\\x00\\x01\"+b\"\\xff\\xff\\xff\\x01\")*(896//2)\netat=struct.pack(\"<III\",896,28,3584 … [969 caractères tronqués]`

  ```
corps 7416000
ecoute: ['[flux] nœud moteur sur 127.0.0.1:5905 · 896 cachés · 24 couches · contexte 65536']
entete recue: 79 mode 4 n 2000
EXC TimeoutError('timed out')
serveur vivant ? None
[flux] client connecté : 127.0.0.1:58640
[flux] 896000 indice(s) hors dimension ignorés sur l'ensemble du lot (flux reçu de 896 canaux)
  ```

### 🤖 Assistant

⏵ Lecture de `flux_en_liste_blocs` (boucle pathologique sur vecteur nul ?)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '3630,3700p' drave-core/src/model.rs", "description": "Read flux_en_liste_blocs"}`

  ```
/// échelle UNIQUE par vecteur donne une erreur *absolue* constante — énorme
    /// en relatif sur les petits canaux (2,6 % de perplexité à 16 bits pleins,
    /// mesuré). Une échelle par bloc borne l'erreur relative à l'intérieur du
    /// bloc, ce qui permet de descendre la valeur à UN octet : moins d'octets
    /// par neurone actif ET une précision localement meilleure.
    ///
    /// Le seuil, lui, reste GLOBAL (fraction du maximum du vecteur) : c'est lui
    /// qui décide de la sparsité, donc de la taille sur le fil.
    pub fn flux_en_liste_blocs(&self, x: &[f32]) -> (Vec<u16>, Vec<i8>, Vec<f32>) {
        const BLOC: usize = 32;
        // La même garde que `flux_en_liste` : au-delà de 65 535 canaux, l'indice
        // u16 tronque EN SILENCE (les modes 2 et 4 en dépendent).
        assert!(x.len() <= u16::MAX as usize,
                "flux de {} canaux : l'indice u16 ne suffit pas", x.len());
        let n_blocs = x.len().div_ceil(BLOC);
        let mut echelles = vec![0f32; n_blocs];
        let mut mx = 0f32;
        for &v in x { let a = v.abs(); if a > mx { mx = a; } }
        let seuil = self.act_thresh * mx;
        let mut idx: Vec<u16> = Vec::new();
        l
… [2495 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Diagnostic live : état du serveur et de la socket pendant l'attente

- **bash** `{"command": "cd /tmp/adv && timeout 200 python3 - <<'EOF' 2>&1 | tail -40\nimport socket, struct, subprocess, sys, time, threading\nsys.path.insert(0,\"/tmp/adv\")\nfrom flux import *\nPORT=5907; T=2000; CTX=65536\npaires=(b\"\\xff\\x00\\x00\\x01\"+b\"\\xff\\xff\\xff\\x01\")*(896//2)\netat=struct.pa … [1117 caractères tronqués]`

  ```
recu 79 octets ; cpu u=0.8s s=0.2s ['VmHWM:\t  602300 kB\n', 'VmRSS:\t  583348 kB\n', 'Threads:\t5\n']
recu 128079 octets ; cpu u=0.8s s=0.2s ['VmHWM:\t  602300 kB\n', 'VmRSS:\t  575948 kB\n', 'Threads:\t5\n']
recu 196687 octets ; cpu u=0.8s s=0.2s ['VmHWM:\t  602300 kB\n', 'VmRSS:\t  575948 kB\n', 'Threads:\t5\n']
recu 252079 octets ; cpu u=0.8s s=0.2s ['VmHWM:\t  602300 kB\n', 'VmRSS:\t  575948 kB\n', 'Threads:\t5\n']
timeout apres 252079 octets
--- ss ---
92.168.1.101:22122   142.250.69.37:443   users:(("chrome",pid=3552690,fd=44))
ESTAB      0      0          127.0.0.1:5907        127.0.0.1:60680 users:(("drave",pid=762124,fd=4))
ESTAB      0      0      192.168.1.101:57160   172.67.74.152:443   users:(("chrome",pid=3552690,fd=58))
ESTAB      0      0      192.168.1.101:33260   173.194.71.94:443   users:(("chrome",pid=3552690,fd=96))
ESTAB      0      0      192.168.1.101:50396 136.243.173.177:443   users:(("node-MainThread",pid=11117,fd=25))
ESTAB      0      0      192.168.1.101:56680   107.170.69.11:443   users:(("chrome",pid=3552690,fd=59))
ESTAB      0      0      192.168.1.101:24678      31.13.80.6:443   users:(("chrome",pid=3552690,fd=24))
ESTAB      0      0      192.16
… [915 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Correction du lecteur de réponse mode 4 et relance du test D

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Test D (v2) : le plafond R4 'cumulatif' du mode 4 face a PLUSIEURS flux.\n\nChaque flux reste sous 256 Mo ; le total depasse 256 Mo.\nLa reponse du serveur est un corps MODE 4 (etats auto-delimites), pas du dense.\n\"\"\"\nimport os, socket, struct, subproc … [2212 caractères tronqués]`

  ```
<path>/tmp/adv/testD_plafond.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

### 🤖 Assistant

⏵ Exécution du test D v2 (8 flux × 35,4 Mo)

- **bash** `{"command": "cd /tmp/adv && timeout 600 python3 testD_plafond.py 2>&1 | tail -20", "description": "Run cumulative cap test v2"}`

  ```
corps d'un flux : 37080000 octets (35.4 Mo) ; 8 flux = 282.9 Mo
  flux 1/8 accepte (reponse mode 4 n=10000, 1260079 o) · total envoye 35.4 Mo > plafond 256 Mo : False · RSS 571220 kB pic 675816 kB
  flux 2/8 accepte (reponse mode 4 n=10000, 1260079 o) · total envoye 70.7 Mo > plafond 256 Mo : False · RSS 593140 kB pic 697828 kB
  flux 3/8 accepte (reponse mode 4 n=10000, 1260079 o) · total envoye 106.1 Mo > plafond 256 Mo : False · RSS 593140 kB pic 697828 kB
  flux 4/8 accepte (reponse mode 4 n=10000, 1260079 o) · total envoye 141.4 Mo > plafond 256 Mo : False · RSS 593140 kB pic 697828 kB
  flux 5/8 accepte (reponse mode 4 n=10000, 1260079 o) · total envoye 176.8 Mo > plafond 256 Mo : False · RSS 593140 kB pic 697828 kB
  flux 6/8 accepte (reponse mode 4 n=10000, 1260079 o) · total envoye 212.2 Mo > plafond 256 Mo : False · RSS 593140 kB pic 697828 kB
  flux 7/8 accepte (reponse mode 4 n=10000, 1260079 o) · total envoye 247.5 Mo > plafond 256 Mo : False · RSS 593140 kB pic 697828 kB
  flux 8/8 accepte (reponse mode 4 n=10000, 1260079 o) · total envoye 282.9 Mo > plafond 256 Mo : True · RSS 593140 kB pic 697828 kB
--- sortie du serveur ---
  | [flux] 4480000 indice(s) hors dimensi
… [230 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test E : reproduction du refus cumulatif annoncé (état 72393)

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Test E : reproduction a l'octet pres du refus cumulatif du rapport\n(reports/rapport-mode4-lot-listes.md : refus a l'etat 72 393, 258 Mo envoyes).\n\nt = 74 898 etats annonces (borne nominale 74 898 x 896 x 4 = 268 433 664 <= 256 MiB),\nchaque etat = 12 + 2 … [1753 caractères tronqués]`

  ```
<path>/tmp/adv/testE_refus.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp/adv && timeout 300 python3 testE_refus.py 2>&1 | tail -20", "description": "Run cumulative refusal reproduction"}`

  ```
corps annonce : 277721784 octets (264.9 Mo) ; t*hidden*4 = 268434432 <= 268435456 : True
connexion coupee apres 523856 octets : ConnectionResetError
octets pousses : 523856 (0.5 Mo) en 0.10 s (5 Mo/s)
etat correspondant au dernier octet : environ 141
cumul apres l'etat 72393 = 268436952 (plafond 268435456)
reponse du serveur : 0 octets
--- sortie du serveur ---
  | [flux] client connecté : 127.0.0.1:51808
  | [flux] arrêt : magie de flux absente
  | [flux] 0 flux servis
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"19,3885\\|19.3885\" --include=*.md . | head -10; echo \"=== ids files ===\"; grep -rn \"ids_qwen_long\\|ids_qwen\" --include=*.md --include=*.py --include=*.sh . | head -10", "description": "Find Qwen gate and ids corpus r … [11 caractères tronqués]`

  ```
./reports/rapport-gpt-oss-perplexite.md:175:complète. Le contrôle de non-régression Qwen ne bouge pas (19,3885).
./reports/rapport-prefill-par-lots.md:197:et la porte de non-régression Qwen contexte 256 reste à **19,3885**.
./reports/rapport-transport-liste.md:48:(19,3885), mais ici 16 bits coûtent 2,6 % : la différence n'est pas la précision,
./reports/rapport-compacite-trace.md:6:> **identique** (perplexité 19,3885 dans les deux cas), et la relecture par
./reports/rapport-compacite-trace.md:11:> silence avec une perplexité fausse (1958,72 au lieu de 19,3885).
./reports/rapport-compacite-trace.md:16:> **+0,074 % de perplexité au rejeu** (19,4029 contre 19,3885) et d'une erreur par
./reports/rapport-compacite-trace.md:234:   réinjecte, et le contrat est « mêmes logits » (perplexité **19,3885** avec et
./reports/rapport-session-2026-09-30.md:50:prouve pas qu'il mesure ce qu'on croit**. Mon premier « rejeu v3 = 19,3885 » était
./reports/rapport-session-2026-09-30.md:92:Qwen ctx 256 = **19,3885** · gpt-oss ctx 256 = **15,1757** · gpt-oss avec
./journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:23746:=== perplexité 19.3885 sur 510 tokens (0 événements, 16.4 s) ===
=== ids
… [2684 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test E corrigé : l'en-tête manquait dans mon envoi

- **bash** `{"command": "cd /tmp/adv && python3 - <<'EOF'\nimport re\np=\"/tmp/adv/testE_refus.py\"\ns=open(p).read()\ns=s.replace('CTX = 65536','CTX = 131072')\ns=s.replace(\"\"\"    morceau = corps[: 1 << 20]\n    reste = corps\"\"\",\"\"\"    reste = tete(MODE_LOT_LISTES, debut=0, fin=0, pos=0, n=T) + corps\ … [144 caractères tronqués]`

  ```
corps annonce : 277721784 octets (264.9 Mo) ; t*hidden*4 = 268434432 <= 268435456 : True
connexion coupee apres 270532608 octets : ConnectionResetError
octets pousses : 270532608 (258.0 Mo) en 10.43 s (26 Mo/s)
etat correspondant au dernier octet : environ 72959
cumul apres l'etat 72393 = 268436952 (plafond 268435456)
reponse du serveur : 0 octets
--- sortie du serveur ---
  | [flux] client connecté : 127.0.0.1:61414
  | [flux] arrêt : corps du lot en listes (cumul après l'état 72393) : 268436952 octets au-delà du plafond de 256 Mo — flux refusé                      (règle R4 de docs/plan-prefill-reparti.md)
  | [flux] 0 flux servis
  ```

### 🤖 Assistant

⏵ Recherche de la commande exacte de la porte Qwen ctx 256

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"porte\" REPRISE.md | head -20 && echo \"=== rapport-session 80-100 ===\" && sed -n '80,100p' reports/rapport-session-2026-09-30.md", "description": "Find gate command"}`

  ```
19:MoE, tient une conversation, et déporte au GPU ce qui y gagne. Il fait tourner du
35:> **19,3885** et gpt-oss ctx 256 = **15,1757**, `cargo test` **17/17**. La porte
160:| 5 | échelles par bloc pour `DenseQ8` | **fait, hypothèse réfutée** | 23,696 contre 23,612 : les échelles par bloc n'apportent rien ; l'avantage du 6 bits est son coût (25 % d'octets en moins à qualité égale) |
182:| porte gpt-oss selon l'ouverture du pilote | sans `DRAVE_GPU` : **15,1757** · avec `DRAVE_GPU=1` : **15,1667** — l'écart vient du déport automatique des projections Q8_0 (> 8 Mo), pas d'une régression |
241:| `DRAVE_GPU_TETE=1` | déporte la tête (Q8_0 ou Q6_K) | inutile sans `DRAVE_GPU` |
261:Une porte de non-régression se mesure **sans** `DRAVE_GPU` : la variable déporte à
291:`colab/` (notebook + `tools/preparer_colab.sh`) porte la recette de la phase 3.4.
330:**Le protocole est en version 5** et le contrat d'activation transporte
514:#    moteur déporte alors tout seul les projections Q8_0 de plus de 8 Mo — le
=== rapport-session 80-100 ===
- **Noyau GPU de top-k** (phase 1.1) : les trois heures sont allées au transport,
  aux formats et aux garde-fous. Les deux Quadro sont libres, le cadre exist
… [731 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"19,3885\\|19.3885\\|ctx 256\" reports/rapport-prefill-par-lots.md | head; echo \"===\"; sed -n '185,200p' reports/rapport-prefill-par-lots.md", "description": "Find gate reproduction line"}`

  ```
197:et la porte de non-régression Qwen contexte 256 reste à **19,3885**.
===
Un lot de `t` jetons ne le coûte plus qu'une fois par groupe de 16 (et une fois
par expert et par groupe pour un MoE) : le facteur à gagner est donc de l'ordre
de 16 sur la partie « projections », qui domine le préremplissage.

Mesuré, avec les deux suites de la §4 et le correctif de la §4.ter en place :

| machine / modèle | contexte | lot 1 | lot 512 | gain |
|---|---|---|---|---|
| Qwen2.5-0.5B Q8_0, `--dense`, 16 fils | 512 | 17,1 s | **13,6 s** | **−20 %** |
| gpt-oss-120b MXFP4, MoE groupé, 16 fils | 256 | ≈ 50 s | 34,4 s (lot 256) | **−31 %** |

Perplexité inchangée dans les deux cas (13,1368 → 13,1359 ; 13,7149 → 13,7205),
et la porte de non-régression Qwen contexte 256 reste à **19,3885**.

Ce qui reste sur la table, dans l'ordre de rentabilité : **le noyau de la tête**
(vectorisation AVX2 ou déport GPU — le lot n'y change rien, §4.bis), **l'attention
  ```

### 🤖 Assistant

⏵ Recherche de la commande de la porte dans le journal

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"19.3885\" -B 40 journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md | grep -E \"command|ppl|ids|limit|ctx\" | tail -20", "description": "Find gate command in journal"}`

  ```
25237-La simulation est déjà dans le moteur (`--bits N`) : la courbe est reproductible en une commande, et le noyau 6 bits n'aura plus qu'à confirmer ce que la simulation annonce.
25275-- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core\npython3 - <<'PY'\np='src/list.rs'; s=open(p,encoding='utf-8').read()\ns=s.replace('''q, sc, scale, plan6: None,\n                  plan6: None, src: Source::Propre''','''q, sc, scale, plan6: None,\n                  src: S … [1737 caractères tronqués]`
25282-- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core\npython3 - <<'PY'\np='src/main.rs'; s=open(p,encoding='utf-8').read(); o=s\ns=s.replace('''            \"--bits\" => {''','''            \"--bits-attn\" => {\n                let b: u32 = args[i + 1].parse().unwrap();\n     … [1447 caractères tronqués]`
25304-- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core\ngrep -n \"let mut b6\" src/main.rs\npython3 - <<'PY'\np='src/main.rs'; s=open(p,encoding='utf-8').read()\n# run_ppl : après la déclaration de moe_topk de run_ppl (contexte du fichier d'identifiants)\nold='''    let mut abi … [
… [3924 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -5 data/wikitext2_test.txt | cut -c1-200; echo \"---\"; wc -c data/wikitext2_test.txt; echo \"--- ppt-texte ---\"; sed -n '3135,3180p' drave-core/src/main.rs", "description": "Inspect corpus and ppl-texte path"}`

  ```
= Robert Boulter = 


 Robert Boulter is an English film , television and theatre actor . He had a guest @-@ starring role on the television series The Bill in 2000 . This was followed by a starring role in the play Herons
---
359041 data/wikitext2_test.txt
--- ppt-texte ---
        ids_file: idfile, texte_file, ppl_texte: _, limit, depuis,
        ctx: ctx_opt, threads: threads_opt, abits: abits_opt,
        ctx_impose, threads_impose, abits_impose,
        dense, auto, q4, b6, attn_window, swa_pattern,
        sans_fenetre, attn_sinks, attn_topk, qk_topk, act_thresh, act_topk, act_renorm,
        topk_proj, moe_topk, patch: patch_file, hebb_layer, hebb_q, hebb_out,
        ffn_gain, logits_bin, keep,
        ppl_profil, lot, profil_neurones, neurones_sortie, trace_flux, trace_couches, flux_forcer,
        harmony, harmony_contexte, sans_yarn, ..
    } = opt;
    let lot = lot.max(1);
    let path = &modele_chemin();
    // Défauts du mode PERPLEXITÉ : 256 jetons, trois quarts des cœurs, 16 bits
    // d'activation (la référence de non-régression en dépend).
    let cpu = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(8);
    let ctx = if ctx_impose { ctx_opt } el
… [1488 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche du générateur d'ids (tokenisation) et de la porte

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"ids_qwen\" --include=\"*\" . 2>/dev/null | grep -v \"^./journal\" | head -20; echo \"=== tokenize ===\"; grep -n \"fn run_tokenize\" -A 30 drave-core/src/main.rs | head -40", "description": "Find ids generator and tokenize … [7 caractères tronqués]`

  ```
./reports/rapport-attribution-kv.md:22:    --ppl /tmp/ids_qwen_long.txt --ctx 8192 --limit 8192 --dense --threads 16 --lot 512
./reports/rapport-placement-bits-kv.md:171:G="--ppl /tmp/ids_qwen_long.txt --ctx 8192 --limit 8192 --dense --threads 16 --lot 512"
./tools/ref_logits.md:37:  ./tools/ref_logits models/Qwen2.5-0.5B-Q8_0.gguf /tmp/ids_qwen.txt \
./tools/ref_logits.md:41:## Nombres obtenus (Qwen2.5-0.5B-Q8_0, 64 premiers ids de /tmp/ids_qwen.txt)
./REPRISE.md:52:    --tokenize --fichier /tmp/wt2_txt.txt --sortie /tmp/ids_qwen.txt
./REPRISE.md:507:./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt \
=== tokenize ===
2787:fn run_tokenize(opt: Options) {
2788-    let path = &modele_chemin();
2789-    let texte = opt.texte.clone().unwrap_or_default();
2790-    let fichier = opt.fichier.clone().unwrap_or_default();
2791-    let sortie = opt.sortie.clone().unwrap_or_default();
2792-    // En-tête seul : le décodage du vocabulaire n'a pas besoin des poids, et
2793-    // `open` lisait le fichier entier (62 Go pour gpt-oss) à chaque appel.
2794-    let g = Gguf::open_meta(path).expect("ouverture du GGUF");
2795-    let tk = build_tokenizer(&g);
2796-    if
… [1512 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '40,60p' REPRISE.md && echo \"=== 500-515 ===\" && sed -n '500,515p' REPRISE.md", "description": "Read REPRISE gate commands"}`

  ```
> changements) : gpt-oss avec `DRAVE_GPU=1` donne **15,1667**, la valeur attendue
> du pilote, et `--gpu-banc` retrouve l'exactitude des noyaux — 1,6 ms par ligne
> en warp-par-ligne contre 7,2 ms sur 30 fils CPU, **écart max 1,99e-7**.

Corpus : `/tmp/wt2_txt.txt` = 20 000 premiers octets de `data/wikitext2_test.txt`.
**Régénérable** (à refaire si `/tmp` a été vidé) :

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
head -c 20000 data/wikitext2_test.txt > /tmp/wt2_txt.txt
# les identifiants DOIVENT venir du tokenizer du modèle — jamais croisés
drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf \
    --tokenize --fichier /tmp/wt2_txt.txt --sortie /tmp/ids_qwen.txt
drave-core/target/release/drave /home/stephane/FastNVMe/models/gpt-oss-120b-MXFP4.gguf \
    --tokenize --fichier /tmp/wt2_txt.txt --sortie /tmp/ids_oss.txt
```

Le mode `--tokenize --fichier` **vérifie la réversibilité** (texte reconstruit
identique à la source) — les deux tokenizers la passent sur ce corpus.

| modèle | commande (abrégée) | perplexité attendue |
=== 500-515 ===

## 8. Premier pas suggéré pour la nouvelle session

```bash
# 1. l'état est-il vert ? (Qwen ne doit pas bouger : les corr
… [712 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Régénération du corpus et porte Qwen ctx 256

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -c 20000 data/wikitext2_test.txt > /tmp/wt2_txt.txt && timeout 300 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --tokenize --fichier /tmp/wt2_txt.txt --sortie /tmp/ids_qwen.txt 2>&1 | tail -3", "description":  … [24 caractères tronqués]`

  ```
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
4592 tokens écrits dans /tmp/ids_qwen.txt (vocabulaire du modèle : 151936)
réversibilité : texte reconstruit identique ✅ (20000 octets)
  ```

### 🤖 Assistant

⏵ Exécution de la porte (threads 8) puis 16

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time timeout 600 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt --ctx 256 --abits 16 --threads 8 --limit 512 --dense 2>&1 | grep -E \"perplexité|tokens|options\" | head -5", "description": "Ru … [24 caractères tronqués]`

  ```
/tmp/ids_qwen.txt : 512 tokens, fenêtres de 256
     255 tokens notés — perplexité cumulée 17.431  (26.7 tok/s)  [fenêtre 1 : 255 notés, PPL 17.431]
     510 tokens notés — perplexité cumulée 19.388  (26.8 tok/s)  [fenêtre 2 : 255 notés, PPL 21.565]
=== perplexité 19.3885 sur 510 tokens (0 événements, 19.0 s) ===
[stderr]

real	0m19,882s
user	3m8,383s
sys	0m0,664s
  ```

### 🤖 Assistant

⏵ Test F : fidélité mode 3 à 1 024 jetons (claim 0259bf1)

- **bash** `{"command": "cd /tmp/adv && python3 - <<'EOF' 2>&1 | tail -12\nimport sys, subprocess, time\nsys.path.insert(0,\"/tmp/adv\")\nfrom flux import *\nPORT=5950\nsrv=lancer_serveur(PORT, ctx=1024)\nattendre_ecoute(srv)\ncmd=[BIN,MODEL,\"--ppl-reparti\",f\"127.0.0.1:{PORT}\",\"--ctx\",\"1024\",\"--limit\" … [423 caractères tronqués]`

  ```
(no output)
[timed out after 60000ms]
[killed by signal: SIGTERM]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -c 40000 data/wikitext2_test.txt > /tmp/wt2_long.txt && ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --tokenize --fichier /tmp/wt2_long.txt --sortie /tmp/ids_qwen_long.txt 2>&1 | tail -2", "description": "Rege … [24 caractères tronqués]`

  ```
9261 tokens écrits dans /tmp/ids_qwen_long.txt (vocabulaire du modèle : 151936)
réversibilité : texte reconstruit identique ✅ (40000 octets)
  ```

### 🤖 Assistant

⏵ Relance du test 1 024 jetons en tâche de fond

- **bash** `{"command": "cd /tmp/adv && nohup python3 - > /tmp/adv/f1024.log 2>&1 <<'EOF' &\nimport sys, subprocess, time\nsys.path.insert(0,\"/tmp/adv\")\nfrom flux import *\nPORT=5951\nsrv=lancer_serveur(PORT, ctx=1024)\nattendre_ecoute(srv)\ncmd=[BIN,MODEL,\"--ppl-reparti\",f\"127.0.0.1:{PORT}\",\"--ctx\",\" … [504 caractères tronqués]`

  ```
lance
767133 bash -c cd /tmp/adv && nohup python3 - > /tmp/adv/f1024.log 2>&1 <<'EOF' & import sys, subprocess, time sys.path.insert(0,"/tmp/adv") from flux import * PORT=5951 srv=lancer_serveur(PORT, ctx=1024) attendre_ecoute(srv) cmd=[BIN,MODEL,"--ppl-reparti",f"127.0.0.1:{PORT}","--ctx","1024","--limit","1024","--threads","4","--lot","64"] t0=time.time(); r=subprocess.run(cmd,capture_output=True,text=True,timeout=1200); dt=time.time()-t0 srv.kill() print("code",r.returncode,"duree %.1f s"%dt) for l in (r.stdout+r.stderr).splitlines():     if any(k in l for k in ("perplexité","écart","transport","temps","pilote")): print(" |",l) EOF echo "lance"; sleep 1; pgrep -af "ppl-reparti" | head -2
767134 bash -c cd /tmp/adv && nohup python3 - > /tmp/adv/f1024.log 2>&1 <<'EOF' & import sys, subprocess, time sys.path.insert(0,"/tmp/adv") from flux import * PORT=5951 srv=lancer_serveur(PORT, ctx=1024) attendre_ecoute(srv) cmd=[BIN,MODEL,"--ppl-reparti",f"127.0.0.1:{PORT}","--ctx","1024","--limit","1024","--threads","4","--lot","64"] t0=time.time(); r=subprocess.run(cmd,capture_output=True,text=True,timeout=1200); dt=time.time()-t0 srv.kill() print("code",r.returncode,"duree %.1f s"%dt) for l
… [193 caractères tronqués]
  ```

- **bash** `{"command": "sleep 20; cat /tmp/adv/f1024.log 2>/dev/null; echo \"--- procs ---\"; pgrep -af \"python3 -\" | head -3; pgrep -af \"release/drave\" | head -3", "description": "Check background 1024 test progress"}`

  ```
--- procs ---
2241 /usr/local/bin/python3 -m uvicorn open_webui.main:app --host 0.0.0.0 --port 8080 --forwarded-allow-ips * --workers 1
767134 bash -c cd /tmp/adv && nohup python3 - > /tmp/adv/f1024.log 2>&1 <<'EOF' & import sys, subprocess, time sys.path.insert(0,"/tmp/adv") from flux import * PORT=5951 srv=lancer_serveur(PORT, ctx=1024) attendre_ecoute(srv) cmd=[BIN,MODEL,"--ppl-reparti",f"127.0.0.1:{PORT}","--ctx","1024","--limit","1024","--threads","4","--lot","64"] t0=time.time(); r=subprocess.run(cmd,capture_output=True,text=True,timeout=1200); dt=time.time()-t0 srv.kill() print("code",r.returncode,"duree %.1f s"%dt) for l in (r.stdout+r.stderr).splitlines():     if any(k in l for k in ("perplexité","écart","transport","temps","pilote")): print(" |",l) EOF echo "lance"; sleep 1; pgrep -af "ppl-reparti" | head -2
767136 python3 -
767138 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/target/release/drave /home/stephane/Data13TB/stephane/GitHub/Qtrinet/models/Qwen2.5-0.5B-Q8_0.gguf --flux-serveur 127.0.0.1:5951 --ctx 1024 --threads 4
767144 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/target/release/drave /home/stephane/Data13TB/stephane/GitHub/Qtrinet/
… [255 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test G : le miroir VRAM et les quatre variables d'attribution

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for cfg in \"aucune\" \"DRAVE_KV_K_F32=1\" \"DRAVE_KV_V_F32=1\" \"DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1\" \"DRAVE_KV_BITS=8 DRAVE_KV_F16=1\" \"DRAVE_KV_BITS=8\"; do echo \"### $cfg\"; env DRAVE_GPU_KV=1 $cfg timeout 200 ./drave-core/targe … [210 caractères tronqués]`

  ```
### aucune
### DRAVE_KV_K_F32=1
[config] cache KV : 32 bits, 0.00 Go pour 32 jetons
### DRAVE_KV_V_F32=1
[config] cache KV : 32 bits, 0.00 Go pour 32 jetons
### DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1
[config] cache KV : 8 bits, 0.00 Go pour 32 jetons
### DRAVE_KV_BITS=8 DRAVE_KV_F16=1
[config] cache KV : 8 bits, 0.00 Go pour 32 jetons
### DRAVE_KV_BITS=8
[config] cache KV : 8 bits, 0.00 Go pour 32 jetons
  ```

### 🤖 Assistant

⏵ Le miroir n'apparaît pas : vérification de l'activation GPU

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"pub fn machines\\|pub fn instance\\|DRAVE_GPU\" drave-core/src/gpu.rs | head -20 && sed -n \"$(grep -n 'pub fn machines' drave-core/src/gpu.rs | head -1 | cut -d: -f1),+18p\" drave-core/src/gpu.rs", "description": "Check GP … [15 caractères tronqués]`

  ```
778:/// Instance unique du processus. `DRAVE_GPU` active le déport ; sans lui, aucune
788:        if std::env::var("DRAVE_GPU").is_err() { return None; }
802:pub fn machines() -> &'static [&'static Gpu] {
811:pub fn instance() -> Option<&'static Gpu> {
813:        if std::env::var("DRAVE_GPU").is_err() { return None; }
pub fn machines() -> &'static [&'static Gpu] {
    MACHINES.get_or_init(|| {
        let mut v: Vec<&'static Gpu> = Vec::new();
        if let Some(a) = instance() { v.push(a); }
        if let Some(b) = second() { v.push(b); }
        v
    })
}

pub fn instance() -> Option<&'static Gpu> {
    INSTANCE.get_or_init(|| {
        if std::env::var("DRAVE_GPU").is_err() { return None; }
        Gpu::ouvrir_auto()
    }).as_ref()
}

unsafe impl Send for Gpu {}
unsafe impl Sync for Gpu {}
unsafe impl Send for MatriceGpu {}
  ```

### 🤖 Assistant

⏵ Test G relancé avec `DRAVE_GPU=1`

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for cfg in \"aucune\" \"DRAVE_KV_K_F32=1\" \"DRAVE_KV_V_F32=1\" \"DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1\" \"DRAVE_KV_BITS=8 DRAVE_KV_F16=1\" \"DRAVE_KV_BITS=8\"; do echo \"### $cfg\"; env DRAVE_GPU=1 DRAVE_GPU_KV=1 $cfg timeout 200 ./drav … [222 caractères tronqués]`

  ```
### aucune
### DRAVE_KV_K_F32=1
[config] cache KV : 32 bits, 0.00 Go pour 32 jetons
[gpu] KV déporté désactivé : les variantes d'attribution (clés ou valeurs en f32) supposent une disposition homogène
[gpu] KV déporté impossible sur 2 périphérique(s) : contexte 32 trop long pour la VRAM — cache KV gardé en RAM
### DRAVE_KV_V_F32=1
[config] cache KV : 32 bits, 0.00 Go pour 32 jetons
[gpu] KV déporté désactivé : les variantes d'attribution (clés ou valeurs en f32) supposent une disposition homogène
[gpu] KV déporté impossible sur 2 périphérique(s) : contexte 32 trop long pour la VRAM — cache KV gardé en RAM
### DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1
[config] cache KV : 8 bits, 0.00 Go pour 32 jetons
[gpu] KV déporté désactivé : les variantes d'attribution (clés ou valeurs en f32) supposent une disposition homogène
[gpu] KV déporté impossible sur 2 périphérique(s) : contexte 32 trop long pour la VRAM — cache KV gardé en RAM
### DRAVE_KV_BITS=8 DRAVE_KV_F16=1
[config] cache KV : 8 bits, 0.00 Go pour 32 jetons
[gpu] KV déporté : 12 couches sur GPU 1, 0.00 Go ici (16.17 Go libres)
[gpu] KV déporté : 12 couches sur GPU 0, 0.00 Go ici (15.12 Go libres)
### DRAVE_KV_BITS=8
[config] cache KV : 8 b
… [169 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Attente du test 1 024 jetons avant les mesures de temps

- **bash** `{"command": "sleep 45; cat /tmp/adv/f1024.log; echo \"--- encore en cours ? ---\"; pgrep -af \"ppl-reparti|flux-serveur\" | grep -c drave", "description": "Check 1024 test progress"}`

  ```
code 0 duree 132.9 s
 | [flux] pilote : 12 couches en local, 12 chez le pair, 1024 jetons
 |   référence locale  : perplexité 12883.6157  (65.8 s)
 |   deux nœuds        : perplexité 12883.6157  (66.3 s)
 |   écart             : 0.00e0
 |   transport         : lot dense f32 · lots de 64 jetons au plus · 229455 octets par lot (aller) · 3.5 ko par jeton · 16 lots pour 1024 jetons
 |   temps             : 1761.5 ms par LOT en local · 1748.8 ms à attendre le pair · soit 0.99× le calcul local seul
--- encore en cours ? ---
1
  ```

### 🤖 Assistant

⏵ Vérification des processus restants puis banc KV

- **bash** `{"command": "pgrep -af \"release/drave\" ; echo \"---\"; uptime", "description": "Check leftover drave processes"}`

  ```
768155 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo "commits du créneau 15h-18h : $(git log --oneline --since='2026-09-30 15:05' | wc -l)"; echo "commits du jour : $(git log --oneline --since='2026-09-30 00:00' | wc -l)"; echo "rapports : $(ls reports/*.md | wc -l) · documents : $(ls docs/*.md | wc -l) · outils : $(ls tools/*.py tools/*.sh | wc -l)"; echo "tests : $(cd drave-core && cargo test --release 2>&1 | grep -oE '[0-9]+ passed' | head -1)"; echo "--- portes ---"; ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt --ctx 256 --abits 16 --threads 16 --limit 512 --dense 2>&1 | grep -oE "perplexité [0-9.]+ sur [0-9]+ tokens"; date +"%H:%M:%S"
768227 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt --ctx 256 --abits 16 --threads 16 --limit 512 --dense
770836 bash -c pgrep -af "release/drave" ; echo "---"; uptime
---
 17:16:14  up 9 days  6:28,  2 users,  load average: 7,85, 6,82, 9,77
  ```

### 🤖 Assistant

⏵ Pendant ce temps : lecture de `tools/pair_factice.py` et des docs modifiés

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 998d409 -- tools/pair_factice.py docs/format-flux.md docs/plan-mode4-lot-listes.md", "description": "Show pair_factice and docs diff"}`

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
… [6787 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des « trois écarts volontaires » et de l'usage de pair_factice

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,40p' docs/plan-mode4-lot-listes.md", "description": "Read plan head"}`

  ```
# Spécification — mode 4 : le **lot en listes** (protocole v5)

> **État : ÉCRIT, mesuré et relu** (voir `reports/rapport-mode4-lot-listes.md`) — ce plan
> reste la référence de conception ; trois écarts volontaires y sont notés en tête. Ce document est la spécification à implémenter ; aucun
> fichier de code n'a été touché pour l'écrire. Il suppose connus
> `docs/format-flux.md` (protocole v4, modes 0–3) et `docs/plan-prefill-reparti.md`
> (le mode 3, mis en œuvre, et ses leçons). Les numéros de ligne sont ceux de
> l'arbre au moment de la rédaction (`VERSION_FLUX = 4`, `TAILLE_TETE = 79`,
> `MODE_LOT = 3`).

**En une ligne** : le mode 3 transporte `t` états en f32 dense — 3 589 octets par
jeton à `t = 16` pour Qwen2.5-0.5B ; le mode 4 transporte **les mêmes `t` états
encodés en listes à échelle par bloc de 32 canaux**, soit ≈ 1 530 octets par état
au seuil 0,01, **÷2,3 sur le fil**, au prix exact que le mode 2 paie déjà
(2,7e-2 d'écart à 256 jetons, 1,3e-2 à 1 024). Le mode 4 ne touche ni au calcul,
ni au cache KV, ni à la norme finale : il s'arrête au transport.

## 0. Décisions d'architecture (à ne pas rediscuter)

| question | décision | pourquoi |
|---|---|---|
| nouveau mode
… [2191 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,70p' tools/pair_factice.py && echo \"...\" && tail -40 tools/pair_factice.py", "description": "Read pair_factice usage"}`

  ```
#!/usr/bin/env python3
"""Pair factice du protocole de flux (v2) : il ÉCOUTE et DIT ce qu'il reçoit.

Pourquoi cet outil : un banc à deux nœuds qui « marche » peut cacher un
protocole faux — c'est exactement ce qui est arrivé avec un flux de 919 canaux
là où le modèle en a 896. Un pair qui parle le protocole sans calculer le modèle
rend visible ce que l'autre bout envoie vraiment : tailles, positions, modes,
réglages. Il répond un flux de la dimension demandée pour que le pilote continue.

    python3 tools/pair_factice.py <port> [dimension]
"""
import socket, struct, sys

MAGIE = 0x44525631
TETE = 79   # en-tête v4 : magie, version, mode, plage, position, n, échelle,
            # niveaux, seuil, top-k, renorm, 7 top-k par projection, 3 top-k globaux
MODES = {0: "dense f32", 1: "listes quantifiées", 2: "blocs (i8 + écarts)",
         3: "lot dense (t états × dimension)", 4: "lot en listes (mode 2 par état)"}


def lire_tout(sock, n):
    buf = b""
    while len(buf) < n:
        morceau = sock.recv(n - len(buf))
        if not morceau:
            raise EOFError("pair fermé")
        buf += morceau
    return buf


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 
… [4021 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test H : réponse de mode incohérent dans le chemin LOT (3↔4)

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Test H : chemin LOT — le client verifie-t-il le mode de la reponse ?\n\nLe client demande en mode 4 (--flux-blocs --lot 4) ; le faux serveur repond en\nmode 3, et reciproquement (demande mode 3, reponse mode 4).\n\"\"\"\nimport socket, struct, subprocess, s … [2936 caractères tronqués]`

  ```
<path>/tmp/adv/testH_lot_modes.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp/adv && timeout 400 python3 testH_lot_modes.py 2>&1 | tail -30", "description": "Run lot-path mode mismatch test"}`

  ```
(no output)
[timed out after 60000ms]
[killed by signal: SIGTERM]
  ```

### 🤖 Assistant

⏵ Diagnostic du test H (blocage) en tâche de fond

- **bash** `{"command": "cd /tmp/adv && nohup python3 -u testH_lot_modes.py > /tmp/adv/testH.log 2>&1 &\necho lance; sleep 50; cat /tmp/adv/testH.log; echo \"--- procs ---\"; pgrep -af \"release/drave\" | head -4", "description": "Run test H in background and inspect"}`

  ```
lance
Exception in thread Thread-1 (servir):
Traceback (most recent call last):
  File "/usr/lib64/python3.13/threading.py", line 1044, in _bootstrap_inner
    self.run()
    ~~~~~~~~^^
  File "/usr/lib64/python3.13/threading.py", line 995, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/adv/testH_lot_modes.py", line 48, in servir
    srv.bind(("127.0.0.1", port)); srv.listen(1)
    ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
OSError: [Errno 98] Address already in use
--- procs ---
776565 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/target/release/drave /home/stephane/Data13TB/stephane/GitHub/Qtrinet/models/Qwen2.5-0.5B-Q8_0.gguf --ppl-reparti 127.0.0.1:5961 --ctx 64 --limit 8 --threads 4 --flux-blocs --lot 4
776891 bash -c cd /tmp/adv && nohup python3 -u testH_lot_modes.py > /tmp/adv/testH.log 2>&1 & echo lance; sleep 50; cat /tmp/adv/testH.log; echo "--- procs ---"; pgrep -af "release/drave" | head -4
776892 bash -c cd /tmp/adv && nohup python3 -u testH_lot_modes.py > /tmp/adv/testH.log 2>&1 & echo lance; sleep 50; cat /tmp/adv/testH.log; echo "--- procs ---"; pgrep -af "release/drave" | head -4
776898 /home/stephane
… [224 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Nettoyage de mes processus bloqués puis correction du test H

- **bash** `{"command": "kill 776565 776898 2>/dev/null; sleep 1; pkill -f \"testH_lot_modes.py\" 2>/dev/null; sleep 1; pgrep -af \"release/drave\" | grep -v pgrep | head -5; echo \"(nettoyage fini)\"", "description": "Kill my leftover test processes"}`

  ```
(no output)
[killed by signal: SIGTERM]
  ```

- **bash** `{"command": "ps -eo pid,etimes,cmd | grep -E \"release/drave|testH\" | grep -v grep | head -10; echo \"(fin)\"", "description": "List leftover processes safely"}`

  ```
(fin)
  ```

### 🤖 Assistant

⏵ Réécriture robuste du test H

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Test H (v2) : chemin LOT — le client verifie-t-il le mode de la reponse ?\"\"\"\nimport socket, struct, subprocess, sys, threading, time\nsys.path.insert(0, \"/tmp/adv\")\nfrom flux import *\n\nBASE = 5970\n\n\ndef lire_flux(s):\n    h = b\"\"\n    while le … [2845 caractères tronqués]`

  ```
<path>/tmp/adv/testH_lot_modes.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "cd /tmp/adv && timeout 200 python3 -u testH_lot_modes.py 2>&1 | tail -30", "description": "Run fixed lot mode test", "timeoutMs": 220000}`

  ```
=== demande mode 4 · reponse mode 3 ===
  requetes vues : [(4, 4)]
  client : code=TIMEOUT signal=None
    | [flux] pilote : 12 couches en local, 12 chez le pair, 8 jetons
    |   référence locale  : perplexité 433.1166  (0.4 s)
    | [attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
    | [modele] 24 couches chargées en 756.672825ms — listes 0.00 Go , 4 threads

=== demande mode 3 · reponse mode 4 ===
  requetes vues : [(3, 4)]
  client : code=1 signal=None
    |   référence locale  : perplexité 433.1166  (0.5 s)
    | [attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
    | [modele] 24 couches chargées en 741.277699ms — listes 0.00 Go , 4 threads
    | [flux] le nœud moteur a répondu en mode 4 alors que la demande était en mode 3 — pair incompatible ? Rien n'a été calculé.

=== demande mode 4 · reponse mode 4 (controle) ===
  requetes vues : [(4, 4)]
  client : code=TIMEOUT signal=None
    | [flux] pilote : 12 couches en local, 12 chez le pair, 8 jetons
    |  
… [297 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Instrumentation du blocage du chemin lot (ss + journal serveur)

- **bash** `{"command": "cd /tmp/adv && cat > /tmp/adv/h2.py <<'EOF'\nimport socket, struct, subprocess, sys, threading, time\nsys.path.insert(0,\"/tmp/adv\")\nfrom flux import *\nPORT=5985\ndef lire_flux(s):\n    h=b\"\"\n    while len(h)<TAILLE_TETE:\n        b=s.recv(TAILLE_TETE-len(h))\n        if not b: re … [1820 caractères tronqués]`

  ```
[srv] entete recue mode 4 n 4
  [srv] etat 823 28 1646
  [srv] etat 1041934978 1093186142 1031658153
  [srv] etat 1024380564 1035016681 1049434079
  [srv] etat 1051932607 1026498797 1056403665
client vivant ? None
2690,fd=24))
ESTAB      0      0      192.168.1.101:28366      31.13.80.6:443   users:(("chrome",pid=3552690,fd=75))
ESTAB      0      0      192.168.1.101:41038      31.13.80.6:443   users:(("chrome",pid=3552690,fd=38))
ESTAB      0      0      192.168.1.101:42798      31.13.80.6:443   users:(("chrome",pid=3552690,fd=41))
CLOSE-WAIT 25     0      192.168.1.101:20108    18.239.6.122:443  
ESTAB      0      0      192.168.1.101:34528      31.13.80.8:443   users:(("chrome",pid=3552690,fd=25))
ESTAB      0      0      192.168.1.101:37158      31.13.80.8:443   users:(("chrome",pid=3552690,fd=35))

  [srv] corps lu 7390 / 15756304183
  [srv] envoi reponse mode 3 de m d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
[config] cache KV : 32 bits, 0.00 Go pour 64 jetons
[modele] 24 couches chargées en 773.216142ms — listes 0.00 Go , 4 threads
[config] 24 couches, hidden 896 · 
[config] puits appris sur 0/24 couch
… [295 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Correction du lecteur de trames mode 4 et relance du test H

- **bash** `{"command": "cd /tmp/adv && python3 - <<'PY'\np=\"/tmp/adv/testH_lot_modes.py\"\ns=open(p).read()\nold = \"\"\"    else:\n        a = 0\n        for _ in range(n):\n            p = b\"\"\n            while len(p) < 12:\n                p += s.recv(12 - len(p))\n            aa, nb, lg = struct.unpack … [1011 caractères tronqués]`

  ```
ok

=== demande mode 4 · reponse mode 3 ===
  requetes vues : [(4, 4)]
  client : code=1 signal=None
    |   référence locale  : perplexité 433.1166  (0.4 s)
    | [attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
    | [modele] 24 couches chargées en 756.490521ms — listes 0.00 Go , 4 threads
    | [flux] le nœud moteur a répondu en mode 3 alors que la demande était en mode 4 — pair incompatible ? Rien n'a été calculé.

=== demande mode 3 · reponse mode 4 ===
  requetes vues : [(3, 4)]
  client : code=1 signal=None
    |   référence locale  : perplexité 433.1166  (0.4 s)
    | [attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
    | [modele] 24 couches chargées en 735.325385ms — listes 0.00 Go , 4 threads
    | [flux] le nœud moteur a répondu en mode 4 alors que la demande était en mode 3 — pair incompatible ? Rien n'a été calculé.

=== demande mode 4 · reponse mode 4 (controle) ===
  requetes vues : [(4, 4), (4, 4)]
  client : code=0 signal=None
    |   transpor
… [487 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lancement des trois bancs KV en tâche de fond

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nohup bash -c 'for cfg in \"32\" \"8\" \"8 K_F16\"; do echo \"### DRAVE_KV_BITS=$cfg\"; if [ \"$cfg\" = \"8 K_F16\" ]; then env DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1 timeout 240 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.g … [328 caractères tronqués]`

  ```
lance
### DRAVE_KV_BITS=32
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
banc KV : 262144 clés · 24 couches · 2 têtes KV × 64 dim, 7 têtes de requête par tête KV · KV f32 bits
  CPU 8 fils :     94.7 ms par passe  (5.7 Go/s de KV, 94.7 ms × 24 couches = 2273 ms/jeton)
  GPU absent
### DRAVE_KV_BITS=8
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
banc KV : 262144 clés · 24 couches · 2 têtes KV × 64 dim, 7 têtes de requête par tête KV · KV 8 bits
  CPU 8 fils :    164.9 ms par passe  (0.9 Go/s de KV, 164.9 ms × 24 couches = 3957 ms/jeton)
  GPU absent
### DRAVE_KV_BITS=8 K_F16
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
banc KV : 262144 clés · 24 couches · 2 têtes KV × 64 dim, 7 têtes de requête par tête KV · KV 8 bits
  CPU 8 fils :    155.0 ms par passe  (1.0 Go/s de KV, 155.0 ms × 24 couches = 3719 ms/jeton)
  GPU absent
  ```

### 🤖 Assistant

⏵ Vérification de la charge puis répétition des temps f32/f16 au repos

- **bash** `{"command": "uptime; ps -eo pid,etimes,pcpu,cmd --sort=-pcpu | head -6", "description": "Check machine load"}`

  ```
17:21:39  up 9 days  6:33,  2 users,  load average: 2,32, 5,00, 8,20
    PID ELAPSED %CPU CMD
 778243       0 50.0 bash -c uptime; ps -eo pid,etimes,pcpu,cmd --sort=-pcpu | head -6
  11117  786051 33.9 node26 /home/stephane/Data13TB/stephane/GitHub/gods-eye-view/node_modules/.bin/vite
 710008  451521 26.3 node26 /home/stephane/.local/share/../bin/dsh --profile dsh-tui
   3770  786790 19.6 /usr/bin/plasmashell --no-respawn
 372484  597865  3.4 node /home/stephane/.local/share/../bin/dsh --profile dsh-tui
  ```

### 🤖 Assistant

⏵ Banc KV avec `DRAVE_GPU=1` (colonnes miroir et noyau)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nohup bash -c 'for cfg in \"32\" \"8\" \"8F16\"; do echo \"### cfg=$cfg\"; case $cfg in 32) env DRAVE_GPU=1 DRAVE_KV_BITS=32 timeout 240 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --banc-kv 262144 --threads 8 2>& … [495 caractères tronqués]`

  ```
lance
### cfg=32
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
banc KV : 262144 clés · 24 couches · 2 têtes KV × 64 dim, 7 têtes de requête par tête KV · KV f32 bits
  CPU 8 fils :     71.5 ms par passe  (7.5 Go/s de KV, 71.5 ms × 24 couches = 1715 ms/jeton)
  GPU 1 · KV d'une couche : 0.00 Go résidents, 16.17 Go libres
  recopie CPU → VRAM : 4.0 s (0.1 Go/s sur le bus)
  GPU 256 tranches :      1.8 ms par passe  (298.0 Go/s de KV, 1.8 ms × 24 couches = 43 ms/jeton)  écart max +3.23e-5
  gain par passe : ×39.7
### cfg=8
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
banc KV : 262144 clés · 24 couches · 2 têtes KV × 64 dim, 7 têtes de requête par tête KV · KV 8 bits
  CPU 8 fils :    145.5 ms par passe  (1.0 Go/s de KV, 145.5 ms × 24 couches = 3493 ms/jeton)
  GPU 1 · KV d'une couche : 0.00 Go résidents, 16.17 Go libres
  recopie CPU → VRAM : 8.0 s (0.0 Go/s sur le bus)
  GPU 256 tranches :      1.7 ms par passe  (89.4 Go/s de KV, 1.7 ms × 24 couches = 41 
… [680 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de la fin du banc KV et recherche des « trois écarts »

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2470,2530p' drave-core/src/main.rs", "description": "Read banc KV tail"}`

  ```
2.0 * octets as f64 / t1.elapsed().as_secs_f64() / 1e9);
    let nsplit = (n / 512).clamp(1, 256);
    let mut part = vec![0f32; nsplit * n_kv * rep * (hd + 2)];
    let mut out = vec![0f32; n_head * hd];
    let mut ms = f64::MAX;
    for passe in 0..3 {
        let t2 = Instant::now();
        if !machine.attn_kv(&mut m, &qs, n, scale, None, nsplit, &mut part, &mut out) {
            println!("  noyau d'attention en échec"); return;
        }
        let dt = t2.elapsed().as_secs_f64();
        if passe > 0 && dt < ms { ms = dt; }
    }
    let mut ecart = f32::NAN;
    if !gpu_seul {
        let mut echelle = 1e-9f32;
        for o in 0..n_head * hd { echelle = echelle.max(cpu[o].abs()); }
        ecart = 0f32;
        for o in 0..n_head * hd { ecart = ecart.max((out[o] - cpu[o]).abs() / echelle); }
    }
    println!("  GPU {nsplit} tranches : {:>8.1} ms par passe  ({:.1} Go/s de KV, {:.1} ms × {n_layer} couches = {:.0} ms/jeton)  écart max {:+.2e}",
             ms * 1e3, 2.0 * octets as f64 / ms / 1e9, ms * 1e3,
             ms * 1e3 * n_layer as f64, ecart);
    println!("  gain par passe : ×{:.1}", tc / ms);
    if std::env::var("DRAVE_BANC_KV_UNIT").is_ok() && hd >= 32 {
 
… [1798 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"écart\" docs/plan-mode4-lot-listes.md | head -20", "description": "Find deviations noted in plan"}`

  ```
4:> reste la référence de conception ; trois écarts volontaires y sont notés en tête. Ce document est la spécification à implémenter ; aucun
15:(2,7e-2 d'écart à 256 jetons, 1,3e-2 à 1 024). Le mode 4 ne touche ni au calcul,
25:| l'encodage des paires ? | **`encoder_paires_blocs` / `decoder_paires_blocs`, appelés tels quels** | ce couple a déjà été désaccordé une fois (quatre octets écrits, deux lus, invisible tant qu'aucun écart n'atteint 255) : on ne l'ouvre pas, on l'appelle |
62:                                       écart u8 · valeur i8, et 255 = échappement :
63:                                       écart u8=255 puis indice ABSOLU u16 LE puis valeur i8
85:  **vérifié** à chaque état, et un écart est refusé en nommant la cause probable
140:Alternatives écartées : table d'échelles partagée par le lot (perte
308:`1..256` donnent une perplexité bien plus haute que WikiText-2, l'écart seul
314:  écart             : 2,7e-2                <- du même ordre que 2a (critère : ≤ 1,5×)
326:* **Critère** : `écart(mode 4) ≤ 1,5 × écart(mode 2 par jeton)` à mêmes ids,
328:  s'écarte de 10×, c'est le placement des échelles ou l'ordre des états qui est
336:  la formule du §1.4 est vérifiée e
… [770 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"volontaire\\|assum\\|noté\\|écrit\" docs/plan-mode4-lot-listes.md | head -20; echo \"=== tete 30 lignes apres modif ===\"; sed -n '340,360p' docs/plan-mode4-lot-listes.md", "description": "Search deliberate deviations in pl … [4 caractères tronqués]`

  ```
4:> reste la référence de conception ; trois écarts volontaires y sont notés en tête. Ce document est la spécification à implémenter ; aucun
25:| l'encodage des paires ? | **`encoder_paires_blocs` / `decoder_paires_blocs`, appelés tels quels** | ce couple a déjà été désaccordé une fois (quatre octets écrits, deux lus, invisible tant qu'aucun écart n'atteint 255) : on ne l'ouvre pas, on l'appelle |
61:  +12+4·n_blocs_j longueur_j × u8      paires, telles que les écrit `encoder_paires_blocs` :
76:a été écrite avant que la règle R4 ne descende dans le code.
97:  seule autorité pour le décodage. L'émetteur écrit `longueur_j = paires.len()`
220:   (model.rs:1117 — noté 907 dans le plan du mode 3, l'arbre a bougé depuis)
237:   repli silencieux. Le message actuel « mode 4 non écrit » (main.rs:1987) doit
370:   (écrit sur quatre octets, lu sur deux) ; ici l'erreur ne casserait rien tant
400:11. **`TCP_NODELAY` et le nombre d'écritures** : l'en-tête puis le corps en deux
401:    `write_all`, jamais une écriture par état (Nagle retient les petites
402:    écritures ; mesuré 97,6 ms contre 15,6 ms de calcul).
417:| 7 | `reports/rapport-mode4-lot-listes.md`, `docs/format-flux.md`, `docs/plan-
… [1468 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test I : mode 1 avec n = 67 M (256 Mio pile) et mesure de la mémoire vive

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Test I : mode 1 (LISTE) avec n = 67 108 864 paires = 256 Mio pile.\n\nLe plafond R4 autorise n*4 == PLAFOND_FLUX (le refus est strictement >).\nOn mesure le pic memoire (VmHWM) du serveur : le corps brut + les deux Vec\n(idx u16, val i16) valent 2x la taill … [1813 caractères tronqués]`

  ```
<path>/tmp/adv/testI_mode1_256m.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp/adv && timeout 300 python3 -u testI_mode1_256m.py 2>&1 | tail -20", "description": "Run 256MiB mode-1 memory test", "timeoutMs": 320000}`

  ```
n = 67108864 paires · corps = 268435456 octets = 256 Mio (plafond 256 Mio)
corps envoye en 0.1 s (3469 Mo/s)
VmRSS 567164 kB · VmHWM 1090852 kB · VmPeak 1455048 kB
reponse : 79 octets ; mode 1 ; n 896
--- serveur ---
  | [flux] client connecté : 127.0.0.1:24336
  | [flux] arrêt : Connection reset by peer (os error 104)
  | [flux] 1 flux servis
  ```

### 🤖 Assistant

⏵ Lecture des branches `None` de `quant_scratch` (vecteur nul)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1845,1865p' drave-core/src/model.rs && echo \"---- 1950,1975 ----\" && sed -n '1950,1975p' drave-core/src/model.rs && echo \"---- 3500,3515 ----\" && sed -n '3500,3515p' drave-core/src/model.rs", "description": "Read quant_sc … [20 caractères tronqués]`

  ```
/// Produit matrice-vecteur **par événements** : les activations actives
    /// poussent leur contribution dans les sorties de leur liste.
    fn matvec(pool: &mut Pool, p: &Proj, x: &[f32], out: &mut [f32], events: &mut u64,
              levels: f32, thresh: f32, topk: usize, renorm: bool, scratch: &mut Vec<f32>,
              thresh_auto: f32) {
        let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
            for (o, v) in out.iter_mut().enumerate() {
                *v = p.bias.as_ref().map_or(0.0, |b| b[o]);
            }
            return;
        };
        // ---- choix de direction par mesure : sous le seuil, disperser (push) ;
        // au-dessus, le produit scalaire dense (pull) est plus rapide.
        // Forme 4 bits : pas d'événements du tout, un seul chemin.
        if let Some(q) = &p.q4 {
            let mut xd = vec![0i32; x.len()];
            for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { xd[i as usize] = v; }
            let y = pool.matvec_dense_q4(q, &xd, sx);
            for o in 0..q.n_out {
                out[o] = y[o] + p.bias.as_ref().map_or(0.0, |b| b[o]);
            }
---- 1950,1975 ----
        for
… [1969 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test J : les gardes du mode 4 (a > hidden, nb, lg) et n=0 refusé

- **bash** `{"command": "cd /tmp/adv && timeout 250 python3 -u - <<'EOF' 2>&1 | tail -40\nimport socket, struct, sys, time\nsys.path.insert(0,\"/tmp/adv\")\nfrom flux import *\nPORT=6000\ndef etat4(a,nb,lg,paires=b\"\"):\n    return struct.pack(\"<III\",a,nb,lg)+struct.pack(\"<%df\"%nb,*([1.0]*nb))+paires\ndef  … [1543 caractères tronqués]`

  ```
=== mode 4 · a=897 > 896 ===
  client: reset · serveur code=0 signal=None
   | [flux] arrêt : état 0 : 897 actifs pour 896 canaux — un encodeur légitime ne peut pas en produire autant

=== mode 4 · nb=27 ===
  client: reset · serveur code=0 signal=None
   | [flux] arrêt : état 0 : 27 blocs d'échelles pour 896 canaux (28 attendus) — les deux nœuds n'ont pas le même GGUF ?

=== mode 4 · lg=3588 > 4a ===
  client: reset · serveur code=0 signal=None
   | [flux] arrêt : état 0 : 3588 octets de paires pour 896 actifs — incohérent (attendu entre 1792 et 3584)

=== mode 4 · n=0 ===
  client: 0 octets · serveur code=0 signal=None
   | [flux] arrêt : flux de zéro état : refusé (R4 de docs/plan-prefill-reparti.md)

=== mode 3 · n=0 ===
  client: 0 octets · serveur code=0 signal=None
   | [flux] arrêt : flux de zéro état : refusé (R4 de docs/plan-prefill-reparti.md)

=== mode 4 · a=896 tous hors dimension ===
  client: 32 octets · serveur code=0 signal=None
   | [flux] arrêt : Connection reset by peer (os error 104)
  ```

### 🤖 Assistant

⏵ Tests de régression : modes 0/1/2 réels et ratio d'octets mode 4 vs mode 2

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Test K : modes 0, 1, 2 reels (WikiText-2, 256 jetons) + ratio d'octets mode 4/2.\"\"\"\nimport re, subprocess, sys, time\nsys.path.insert(0, \"/tmp/adv\")\nfrom flux import *\n\nPORT = 6100\n\n\ndef run(nom, extra, limite=256, ctx=256):\n    global PORT\n   … [1731 caractères tronqués]`

  ```
<path>/tmp/adv/testK_modes.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp/adv && nohup python3 -u testK_modes.py > /tmp/adv/testK.log 2>&1 & echo lance; sleep 45; cat /tmp/adv/testK.log", "description": "Launch real-mode regression runs"}`

  ```
lance

=== mode 0 (dense) · un flux par jeton (38 s, code 0) ===
   |   référence locale  : perplexité 17095.3708  (19.4 s)
   |   deux nœuds        : perplexité 17095.3708  (17.8 s)
   |   écart             : 0.00e0
   |   transport         : dense f32 · 3663 octets par flux (aller) · 3663 au retour · 100.0 % d'activité (896 neurones par flux) · 255 flux
  ```

### 🤖 Assistant

⏵ Recherche de la commande de campagne du plan (ids du client réparti)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"ppl-reparti\" docs/plan-mode4-lot-listes.md | head -10 && echo \"===\" && sed -n '280,320p' docs/plan-mode4-lot-listes.md", "description": "Read campaign command in plan"}`

  ```
299:./drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl-reparti 127.0.0.1:45733 \
303:./drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl-reparti 127.0.0.1:45733 \
===

### 5.3 La réponse

Encodée **comme la demande** (R5) : `envoyer_lot_listes` sur les `t` états
rendus par `forward_lot` (résidu brut, jamais normé), mêmes `t`, `position`,
plage et réglages. Le pilote la décode par le même `recevoir_flux`, retrouve un
`ChargeFlux::Lot` plat, garde son `assert_eq!(etats.len(), t*hidden)`, applique
`norme_finale` **une fois par état** puis `logits_lot`. Le coût du retour est du
même ordre que l'aller (÷2,3) ; c'est la ligne `octets_recus` qui le prouvera.

## 6. La vérification

### 6.1 Commande exacte (localhost, Qwen2.5-0.5B, 12 couches par nœud)

```bash
# terminal 1 — le nœud moteur : inchangé
./drave models/Qwen2.5-0.5B-Q8_0.gguf --flux-serveur 45733 --ctx 256

# terminal 2a — la référence PERDANTE : le mode 2, un flux par jeton (mêmes ids)
./drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl-reparti 127.0.0.1:45733 \
        --couches-locales 12 --limit 256 --ctx 256 --flux-blocs --act-thresh 0.01

# terminal 2b — le mode 4 : mêmes ids, même seuil, par lots
./drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl-re
… [790 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche de la commande réellement utilisée pour le rapport mode 4

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"ppl-reparti\" journal/sessions/*/digest.md 2>/dev/null | grep -i \"ids\\|wiki\" | head -8; echo \"=== toutes les commandes ppl-reparti du journal (extraits) ===\"; grep -rho \"ppl-reparti[^\\\\\\\\\\\"]*\" journal/sessions … [98 caractères tronqués]`

  ```
journal/sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/digest.md:504:"--abits" "--act-renorm" "--act-thresh" "--act-topk" "--attn-sinks" "--attn-topk" "--attn-window" "--auto" "--banc-kv" "--banc-mla" "--banc-vision" "--bits" "--bits-attn" "--bits-ffn" "--chat" "--couches-locales" "--ctx" "--dense" "--depuis" "--ffn-gain" "--fichier" "--flux" "--flux-blocs" "--flux-forcer" "--flux-liste" "--flux-serveur" "--gpu-banc" "--harmony" "--harmony-assistant" "--harmony-contexte" "--harmony-suite" "--harmony-user" "--hebbian" "--hebb-out" "--hebb-q" "--hist" "--ids" "--ids-file" "--infer" "--keep" "--limit" "--logits-bin" "--lot" "--matrix" "--moe-topk" "--n" "--neurones-sortie" "--patch" "--pin" "--plan" "--ppl" "--ppl-profil" "--ppl-reparti" "--ppl-texte" "--profil-neurones" "--prompt" "--push" "--q4" "--q4-attn" "--q4-ffn" "--q4-tout" "--qk-topk" "--rep-penalty" "--sans-fenetre" "--sans-yarn" "--session" "--sortie" "--swa-pattern" "--temp" "--tensors" "--texte" "--threads" "--tokenize" "--topk" "--topk-down" "--topk-gate" "--topk-k" "--topk-o" "--topk-q" "--topk-up" "--topk-v" "--top-p" "--trace-couches" "--trace-flux"
journal/sessions/5ce3f080-2d3d-467a-8ee1-df697f3f3e68/digest.md:881:- 
… [4987 caractères tronqués]
  ```

- **bash** `{"command": "sleep 30; cat /tmp/adv/testK.log", "description": "Check K progress"}`

  ```
=== mode 0 (dense) · un flux par jeton (38 s, code 0) ===
   |   référence locale  : perplexité 17095.3708  (19.4 s)
   |   deux nœuds        : perplexité 17095.3708  (17.8 s)
   |   écart             : 0.00e0
   |   transport         : dense f32 · 3663 octets par flux (aller) · 3663 au retour · 100.0 % d'activité (896 neurones par flux) · 255 flux

=== mode 1 (listes i16) · seuil 0,01 (38 s, code 0) ===
   |   référence locale  : perplexité 17446.1253  (19.4 s)
   |   deux nœuds        : perplexité 17503.6039  (18.0 s)
   |   écart             : 3.29e-3
   |   transport         : listes quantifiées · 3024 octets par flux (aller) · 2921 au retour · 82.2 % d'activité (736 neurones par flux) · 255 flux
  ```

### 🤖 Assistant

⏵ Attente des modes 2 et 4 du test K

- **bash** `{"command": "sleep 90; cat /tmp/adv/testK.log; echo \"=== git status ===\"; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain && git diff --stat journal/README.md | tail -2", "description": "Check K results and git status"}`

  ```
(no output)
[timed out after 60000ms]
[killed by signal: SIGTERM]
  ```

- **bash** `{"command": "cat /tmp/adv/testK.log; echo \"=== procs ===\"; ps -eo pid,etimes,cmd | grep -E \"ppl-reparti|flux-serveur|testK\" | grep -v grep | head -5", "description": "Check K log and processes"}`

  ```
=== mode 0 (dense) · un flux par jeton (38 s, code 0) ===
   |   référence locale  : perplexité 17095.3708  (19.4 s)
   |   deux nœuds        : perplexité 17095.3708  (17.8 s)
   |   écart             : 0.00e0
   |   transport         : dense f32 · 3663 octets par flux (aller) · 3663 au retour · 100.0 % d'activité (896 neurones par flux) · 255 flux

=== mode 1 (listes i16) · seuil 0,01 (38 s, code 0) ===
   |   référence locale  : perplexité 17446.1253  (19.4 s)
   |   deux nœuds        : perplexité 17503.6039  (18.0 s)
   |   écart             : 3.29e-3
   |   transport         : listes quantifiées · 3024 octets par flux (aller) · 2921 au retour · 82.2 % d'activité (736 neurones par flux) · 255 flux

=== mode 2 (blocs) · seuil 0,01 · lot 1 (38 s, code 0) ===
   |   référence locale  : perplexité 17446.1253  (19.6 s)
   |   deux nœuds        : perplexité 18430.7753  (18.0 s)
   |   écart             : 5.64e-2
   |   transport         : listes à échelle par bloc (2 octets/actif, écarts) · 1671 octets par flux (aller) · 1621 au retour · 82.2 % d'activité (736 neurones par flux) · 255 flux

=== mode 4 (lot en listes) · seuil 0,01 · lot 16 (36 s, code 0) ===
   |   référence locale  : 
… [410 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Dernières vérifications (git status, ids-file ignoré) puis rédaction

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain; echo \"--- diff journal/README.md ---\"; git diff --stat; echo \"--- ids_file dans run_ppl_reparti ? ---\"; sed -n '2057,2096p' drave-core/src/main.rs | grep -n \"ids\" ", "description": "Check git status and  … [14 caractères tronqués]`

  ```
M journal/README.md
 M journal/sessions/5185ccb1-be24-4716-89df-62621e790444/digest.md
 M journal/sessions/5185ccb1-be24-4716-89df-62621e790444/rapport.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md
 M journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md
--- diff journal/README.md ---
 journal/README.md                                  |  12 +-
 .../5185ccb1-be24-4716-89df-62621e790444/digest.md | 693 +++++++++++++++++++++
 .../rapport.md                                     |  52 +-
 journal/sessions/MANIFEST.md                       |   6 +-
 .../bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md |  29 +
 .../rapport.md                                     |  14 +-
 6 files changed, 785 insertions(+), 21 deletions(-)
--- ids_file dans run_ppl_reparti ? ---
24:    let ids: Vec<u32> = if opt.ids.is_empty() {
26:    } else { opt.ids.clone() };
27:    if ids.len() < 2 {
31:(le premier ne prédit rien) — reçu {}. Rien n'a été calculé.", ids.len());
35:             n_layer - couches_locales, ids.len());
  ```

### 🤖 Assistant

⏵ Nettoyage final de mes processus et vérification

- **bash** `{"command": "ps -eo pid,etimes,cmd | grep -E \"release/drave|adv/\" | grep -v grep | head; echo \"(fin liste)\"; uptime", "description": "Verify no leftover processes"}`

  ```
(fin liste)
 17:26:45  up 9 days  6:38,  2 users,  load average: 4,91, 5,40, 7,41
  ```

### 🤖 Assistant

⏵ Rédaction du rapport adversarial final

J'ai fini les vérifications. Voici le rapport.

---

# Relecture adversariale des correctifs du 30/09 (998d409 → 0c56c35)

**Verdict court : les dix correctifs de 998d409 sont réels et fonctionnent là où ils ont été posés — mais le durcissement s'arrête net à la frontière du chemin « lot ».** Le client reste tuable par un pair hostile en mode 1/2, le nœud moteur reste tuable par une trame de 83 octets, et trois affirmations des rapports ne sont pas reproductibles telles quelles. 17/17 tests, porte Qwen = **19,3885** exacte.

## 1. GRAVE — le contrôle de la réponse du pair n'existe QUE dans le chemin lot

`main.rs:2176-2196` : `if rep.mode != mode_lot` et `if rep.n != t` sont **à l'intérieur du `if lot > 1`**. Le chemin non-lot (modes 0/1/2, un flux par jeton) ne vérifie **rien** — ni le mode, ni la taille. Le commentaire du correctif (« le client vérifie le mode et la taille de la réponse au lieu d'abandonner en SIGABRT sur 83 octets hostiles ») est donc faux pour ce chemin.

Preuves (faux serveur sur `127.0.0.1`, client réel `--ppl-reparti --limit 6 --ctx 64`) :

| réponse forgée | résultat client |
|---|---|
| mode 4 (lot) alors que la demande est mode 0 | **SIGABRT** (signal 6) — `main.rs:1512` « un lot d'états n'est pas un vecteur dense » |
| mode 3 (lot dense) idem | **SIGABRT** — même site |
| mode 0, `n = 897 > hidden` | **SIGABRT** — `model.rs:2204` « index out of bounds: the len is 896 but the index is 896 » |
| mode 0, `n = 895 < hidden` | **silencieux**, code 0, perplexité 2,76e8 affichée comme un résultat |
| mode 1 `n=0` | **silencieux**, code 0, perplexité = 151936,0 = vocabulaire (logits nuls) |

Le chemin lot, lui, est correct : demande mode 4 → réponse mode 3 ⇒ `code 1` + « le nœud moteur a répondu en mode 3 alors que la demande était en mode 4 » ; inverse idem.

## 2. GRAVE — le nœud moteur est tué par des trames forgées de 83 octets

Aucun champ d'en-tête n'est validé côté récepteur : `debut`, `fin`, `pos` sont recopiés tels quels (`main.rs:2020-2023`). Trois trames bien formées, testées une par une :

| trame | panique serveur |
|---|---|
| mode 1, `n=1`, `pos=100000` (83 octets) | `model.rs:2985` `assert!(pos < self.ctx)` → **SIGABRT** |
| mode 1, `n=1`, `fin=200` pour 24 couches (83 octets) | `model.rs:3046` `&layers[l]` → **SIGABRT** |
| mode 0, `n=897` (et aussi `n=895`) | `model.rs:2204` / `model.rs:3314` → **SIGABRT** |

Le plan n'exige le contrôle de contexte que sur la branche lot (« le contrôle de contexte reste dans la boucle serveur, sur la branche commune aux modes 3 et 4 ») : c'est précisément le trou. Le mode 4 est, lui, bien gardé (voir §5). Le commentaire du code — « une trame FORGÉE ne doit pas tuer le nœud » — est violé sur le chemin jeton par jeton.

## 3. Le refus de `n == 0` est correct… mais incomplet en mode 0

- **Modes 1/2** : le correctif est bon et complet. Liste vide acceptée, `en_dense` rend `vec![0.0; hidden]`, `quant_scratch` rend `None` et **tous** ses appelants écrivent des zéros ou les biais (aucune division par zéro) : la session réelle `--flux-blocs --act-thresh 1.0 --lot 1` donne **0,00e0** (19 flux, « 0 neurones par flux »).
- **Mode 0** : zéro canal est bien illégitime, mais la seule règle appliquée est `n != 0`. Or `n` **doit** valoir `hidden` (c'est une dimension, R3). `n=895` et `n=897` tuent le serveur et/ou corrompent le client en silence. Le refus de `n==0` est donc *trop étroit*, pas trop large.

## 4. Le plafond cumulatif : exact au bit, mais par message — et la mémoire ne s'accumule pas

- **Reproduction exacte du rapport** (test E) : 74 898 états annoncés de 3 708 octets, `t·hidden·4 = 268 434 432 ≤ 256 Mio` (borne nominale qui passe). Le serveur refuse à l'état **72 393** :
  `corps du lot en listes (cumul après l'état 72393) : 268436952 octets au-delà du plafond de 256 Mo` — **258,0 Mo poussés** avant la coupure. Le chiffre du rapport est juste à l'octet.
- **Multi-flux** : le cumul repart de zéro à chaque `recevoir_flux` (`let mut lus = 0usize`), et le serveur boucle. **8 flux de 35,4 Mo = 282,9 Mo (total > 256 Mo) sont tous acceptés** et servis. La mémoire vive, elle, **ne s'accumule pas** : RSS stable à 593 Mo, pic 698 Mo du 2ᵉ au 8ᵉ flux (pas de fuite de `plat`). Le plafond R4 est donc une borne de message, pas de session ; c'est conforme au §4 du plan (qui ne parle que du cumul intra-message), mais la phrase du commit « le temps, non » reste vraie entre les messages.
- **Écart avec le plan** : le §4 exige la vérification du cumul **avant** de lire l'état fautif (« refuser sans lire l'état fautif ») ; le code lit et décode l'état, puis vérifie (`main.rs:1860-1866`). Conséquence bornée ici (≤ 1 état = 3 708 octets), mais c'est un écart textuel.
- **La borne « 256 Mo = mémoire vivante » est fausse d'un facteur 2** (test I) : une trame mode 1 de **256 Mio pile** (`n = 67 108 864`, `n·4 == PLAFOND_FLUX`, acceptée puisque le refus est strictement `>`) fait monter le serveur à **VmHWM 1,04 Gio** (delta ≈ +512 Mo : corps brut 256 Mo + `Vec<u16>` 128 Mo + `Vec<i16>` 128 Mo). Idem en mode 0 et 3 (double copie). Le décodeur ne peut pas être tué, mais il alloue 2× ce que le plafond annonce.

## 5. Ce qui est solide (vérifié, pas seulement lu)

- Gardes du mode 4 : `a=897 > hidden` → « état 0 : 897 actifs pour 896 canaux » ; `nb=27` → « 27 blocs … les deux nœuds n'ont pas le même GGUF ? » ; `lg=3588 > 4a` → refus nommé ; `n=0` en modes 3/4 → refus nommé. Sortie propre (code 0, pas de panique) dans les quatre cas.
- « Hors dimension dit une fois » : 4 480 000 indices ignorés → **une seule ligne par flux** (8 lignes pour 8 flux).
- Comptabilité : `--lot 16 --limit 20` → « 2 lots pour 20 jetons », 35 919 o/lot, et 35 919×2/20/1024 = 3,5077 → « 3.5 ko par jeton » (cohérent) ; `--lot 1000` → « 1 lots pour 20 jetons » ; à 1 024 jetons/64 → **16 lots pour 1 024 jetons, écart 0,00e0** (claim de 0259bf1 reproduit).
- Non-régression : `cargo test --release` **17/17** ; porte Qwen ctx 256 (`head -c 20000` + `--tokenize`, puis `--ppl /tmp/ids_qwen.txt --ctx 256 --abits 16 --limit 512 --dense`) = **19,3885** ; modes 0/1/2/3/4 de bout en bout : mode 0 **0,00e0**, mode 1 3,29e-3, mode 2 5,64e-2 (act-thresh 0,01), mode 3 **0,00e0** (1 024 jetons), mode 4 6,46e-2.
- **Miroir VRAM et les quatre variables** : `K_F32`, `V_F32`, `K_F16` (avec `BITS=8`) désactivent bien le miroir (`[gpu] KV déporté désactivé`) ; `DRAVE_KV_F16` **ne le désactive pas** — et c'est correct, puisque l'arrondi f16 s'applique *avant* quantification et que le miroir copie les octets déjà quantifiés. La formulation du rapport (« toute variante d'attribution ») est exacte mais n'énumère que 3 variables.
- Temps KV au repos, avec `DRAVE_GPU=1` : f32 **71,5 ms** (rapport 70,5) · f16 **163,6 ms** (162,1), soit **2,29×** (le 2,3× est reproduit) · int8 **145,5 ms** (rapport **174,0**, −16 %) ; miroir 1,8 ms / 1,7 ms, écarts noyau +3,23e-5 et +3,42e-5 (rapport +3,2/+3,4e-5). ⚠ Première passe faite sous charge (un autre job tournait) : 94,7 / 155,0 / 164,9 ms, ratio 1,64× — la mesure est sensible à la charge, non documentée.

## 6. Reproductibilité des rapports (défauts prouvés)

1. **`--banc-kv` n'applique pas la règle d'homogénéité** que la politique invoque : `run_banc_kv` appelle `machine.kv_allouer(...)` sans le test `mixte` de `model.rs:1650`. Avec `DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1`, le banc **installe le miroir** et affiche « GPU 1 · 1,7 ms … écart max +4,17e-5 » — alors que le moteur, lui, refuse ce miroir. La cellule « ❌ désactivé / — » du tableau ne sort **pas** de la commande du banc ; elle vient du chemin modèle. De plus, sans `DRAVE_GPU=1` (jamais écrit dans le rapport), le banc affiche « GPU absent » et **aucune** colonne miroir/noyau.
2. **Aucune commande pour la nouvelle section** (les trois lignes de temps, le miroir, les écarts noyau) ; la section « Reproductible » ne couvre que **3 des 9 lignes** du tableau ; `/tmp/ids_qwen_long.txt` n'est pas régénérable depuis le rapport (la recette est dans `REPRISE.md` §2 avec `head -c 20000` → 4 592 ids, insuffisant pour `--limit 8192` ; il m'a fallu inventer `head -c 40000` → 9 261 ids).
3. **Aiguille 9/9 invérifiable** : `models/` ne contient que Qwen2.5‑0.5B (Q4_0, Q8_0) ; le modèle 1.5B‑Instruct Q4_K_M du tableau est absent, aucune commande de téléchargement.
4. **`--ppl-reparti` ignore `--ids-file` (et `--ppl <fichier>`)** : `run_ppl_reparti` ne lit que `opt.ids` (ligne 2080). Le « corpus WikiText-2 » du rapport mode 4 n'est donc alimentable que par une liste `--ids` littérale (le journal montre `--ids $IDS`), et la commande du plan §6.1 mesure en réalité les ids 1..256.
5. **« ÷2,3 sur les octets » est trompeur** : le tableau « Mesuré » aligne mode 2 = 1 608 o/flux et mode 4 = 1,5 ko → **1,05×**, pas 2,3×. Le ÷2,3 n'est vrai que contre le mode 3 **dense** (3,5 ko/jeton), qui n'est pas dans le tableau. Ma mesure : mode 2 = 1 671 o/flux, mode 4 = 1,6 ko/jeton → **1,02×**.
6. **Docs** : `docs/plan-mode4-lot-listes.md` annonce « trois écarts volontaires y sont notés en tête » — **aucune liste de trois écarts n'existe dans le fichier** — et conserve « aucun fichier de code n'a été touché pour l'écrire », faux depuis l'implémentation et les dix correctifs.

## 7. Mineurs

- « 1 lots pour 20 jetons » (accord) ; `--banc-kv --threads N` affiche « N fils » alors que la passe CPU lance toujours `n_head` threads (`let _ = threads`).
- `tools/pair_factice.py` : le mode 2 renvoie `n_paires = 0` mais `mode in (3,4)` seulement pour le mode lot — cohérent ; à noter que son `elif mode == 2` vient APRÈS `mode == 4`, l'ordre est bon.
- L'arbre de travail n'est pas propre (`journal/README.md`, `journal/sessions/…/digest.md` et `rapport.md` modifiés) — écritures d'autres agents, pas de moi ; je n'ai touché **aucun** fichier du dépôt.

## 8. Non vérifié

Aiguille 9/9 (modèle 1.5B absent) ; les 6 lignes du tableau KV sans commande (25–28 min chacune) ; les portes gpt-oss (modèle absent de `models/`) ; les octets WikiText exacts du rapport mode 4 (mes runs utilisent les ids synthétiques, seuls reproductibles sans liste littérale).

---

**Résumé (10 lignes)**

1. **9 défauts réels prouvés** (6 de code, 3 de documentation/mesure), dont 2 graves.
2. **Grave n°1 — le client ne valide la réponse du pair que dans le chemin lot** : mode 3/4 en réponse à une demande mode 0 → SIGABRT (`main.rs:1512`) ; mode 0 `n=897` → SIGABRT (`model.rs:2204`) ; `n=895` ou mode 1 `n=0` → perplexité fausse acceptée en silence. Le lot, lui, est correct (3↔4 refusés proprement).
3. **Grave n°2 — le nœud moteur meurt sur 83 octets forgés** : `pos ≥ ctx` (assert `model.rs:2985`), `fin > n_layer` (`model.rs:3046`), et `n ≠ hidden` en mode 0 (`model.rs:2204`/`3314`) → SIGABRT. Le mode 0 ne contrôle que `n != 0`.
4. **Vérifié correct** : refus `n==0` en modes 0/3/4 et listes vides en 1/2 (session réelle `--act-thresh 1.0` → 0,00e0, `quant_scratch → None` sans division par zéro) ; gardes mode 4 (`a≤hidden`, `nb`, `lg`, une seule ligne « hors dimension ») ; comptabilité Σt (2 lots/20 jetons, 16 lots/1 024 jetons) ; mode 3 à 1 024 jetons 0,00e0 ; `cargo test` 17/17 ; porte Qwen **19,3885** ; modes 0–4 sans régression.
5. **Plafond cumulatif** : reproduit à l'octet (refus à l'état 72 393, 258,0 Mo poussés) mais **par message** : 8 flux de 35,4 Mo (282,9 Mo cumulés) passent ; la RAM ne s'accumule pas (RSS 593 Mo stable) ; la vérification est faite **après** lecture, contre le §4 du plan.
6. **La borne « 256 Mo de mémoire vivante » est fausse d'un facteur 2** : trame mode 1 de 256 Mio pile → VmHWM **1,04 Gio** (corps + `Vec<u16>` + `Vec<i16>`).
7. **Le banc KV n'applique pas l'homogénéité qu'il sert à justifier** : avec `K_F16` il installe le miroir et sort « écart +4,17e-5 », là où le rapport écrit « ❌ désactivé / — » ; sans `DRAVE_GPU=1`, « GPU absent ».
8. **Mesures KV** : f32 71,5 ms et f16 163,6 ms (2,29×) reproduits, miroir 1,8/1,7 ms et écarts +3,2/+3,4e-5 reproduits ; **int8 145,5 ms contre 174,0 annoncés** (−16 %).
9. **Reproductibilité** : pas de commande pour la section temps/miroir, 6 lignes du tableau KV sans commande, `/tmp/ids_qwen_long.txt` non régénérable depuis le rapport, aiguille 9/9 invérifiable (modèle 1.5B absent), `--ppl-reparti` ignore `--ids-file` ; « ÷2,3 sur les octets » contredit par le tableau lui-même (1,05×) et par ma mesure (1,02×).
10. **Non vérifié** : aiguille 9/9, 6 lignes KV, portes gpt-oss, octets WikiText exacts du mode 4. Aucun fichier du dépôt modifié ; tous mes processus arrêtés.

- **send_message** `{"agent_id": "bbd6969f-0f70-42b2-8951-64d1f2f36d2e", "message": "RELECTURE ADVERSARIALE des correctifs 998d409→0c56c35 : 9 défauts réels prouvés (6 code, 3 doc/mesure), 2 graves. Aucun fichier du dépôt modifié. cargo test 17/17 ; porte Qwen ctx 256 = 19,3885 reproduite.\n\nGRAVE 1 — le client ne val … [4122 caractères tronqués]`

  ```
message delivered to agent bbd6969f-0f70-42b2-8951-64d1f2f36d2e
  ```

### 🤖 Assistant

⏵ Clôture : rapport envoyé, aucun processus résiduel

Le rapport complet figure ci-dessus et le résumé auto-portant a été transmis au parent (`bbd6969f-…`) via `send_message` (livré). Aucun fichier du dépôt n'a été modifié (les `journal/…` modifiés dans `git status` sont les écritures d'autres agents) ; tous mes serveurs, clients factices et bancs sont arrêtés, aucun job de fond ne tourne.

