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
