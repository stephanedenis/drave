# Session DSH — relecture

- identifiant : `da69b1fa-91b0-4c69-bb2b-58bf00e92e28`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-09-30 15:07:50
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM en Rust, `std` seul, binaire `drave`). Tout est en FRANÇAIS : écris en français.

CONTEXTE : le moteur sait faire tourner un modèle découpé sur deux machines qui se passent des « listes d'activation » (le cœur du projet). Le protocole de flux est en **version 4** et a quatre modes : 0 = dense f32, 1 = listes (indice u16 + valeur i16 + échelle), 2 = listes à échelle par bloc de 32 canaux (indice par écarts u8 + valeur i8), 3 = **lot** (N états d'un coup, en f32 dense). Le mode 3 est ce qui a permis le préremplissage réparti (256 jetons en 4 lots, écart local/réparti 0,00e0), mais il envoie du **f32 dense : 3,5 ko par jeton**, alors que le mode 2 fait ÷2,3 sur le fil.

TA MISSION : écrire la **spécification du mode 4 — « lot en listes »** — dans `docs/plan-mode4-lot-listes.md`. C'est le prochain chantier identifié ; il doit être implémentable sans réfléchir à l'architecture.

Lis d'abord, dans le dépôt : `docs/format-flux.md` (la spécification du protocole), `docs/plan-prefill-reparti.md` (le plan du mode 3, déjà mis en œuvre — il contient les leçons), `reports/rapport-prefill-reparti.md` (les mesures du mode 3), `drave-core/src/main.rs` (cherche `MODE_LOT`, `envoyer_lot`, `recevoir_flux`, `ChargeFlux`, `encoder_paires_blocs`, `decoder_paires_blocs`, `TAILLE_TETE`, `PLAFOND_FLUX`) et `drave-core/src/model.rs` (`flux_en_liste`, `flux_en_liste_blocs`, `emb_imposee_lot`, `forward_lot`).

Le document doit contenir, concis et sans remplissage :
1. **Le corps du message** : comment enchaîner N états encodés en listes dans UN SEUL flux, sachant que chaque état a un nombre d'actifs différent. Propose une disposition auto-délimitée (par exemple : pour chaque état, son compte puis ses données) et donne le tableau d'octets exact, en réutilisant `encoder_paires_blocs` (ne réinvente pas un encodage : le projet a déjà payé deux bugs sur ce couple).
2. **L'échelle par état** : le mode 2 transporte une échelle par bloc de 32 canaux ; décide où elle se place dans un lot et dis pourquoi.
3. **La compatibilité** : faut-il une version 5 du protocole ? Que se passe-t-il si un pair v4 reçoit un mode 4 ? (le refus doit être immédiat et nommé — c'est le critère 3.5 de la feuille de route).
4. **Le garde-fou de taille** : la règle R4 plafonne toute allocation pilotée par le réseau à 256 Mo (`PLAFOND_FLUX`). Dis exactement quels champs du mode 4 doivent passer par `verifier_taille`, et donne l'ordre des vérifications (avant toute allocation).
5. **Les deux côtés** : ce que le pilote doit faire (encoder N états), ce que le nœud moteur doit faire (décoder N états, les rendre à `forward_lot` via `emb_imposee_lot`), et comment la réponse est encodée.
6. **La vérification** : le mode 4 est AVEC PERTE (i8 + échelle par bloc : 2,7e-2 d'écart mesuré en flux simple). Donne la commande exacte et le résultat attendu, et dis quel écart est acceptable — en le comparant à ce que le mode 2 coûte déjà.
7. **Les pièges** : reprends ceux déjà payés (un octet d'en-tête en trop décale tout le corps et ne se voit qu'au flux suivant, les réglages d'activation voyagent, la clé de trace est un compteur global, `n` change de sens selon le mode, le dernier jeton n'a rien à prédire).
8. **Le plan d'implémentation** en 5 à 8 étapes ordonnées, chacune avec le fichier concerné et son critère de succès.

INTERDIT : modifier un fichier autre que `docs/plan-mode4-lot-listes.md`. Aucune compilation, aucune exécution du moteur (une campagne de mesure tourne : `pgrep -x drave` doit rester le seul juge de la machine). Tu écris une spécification, tu ne mesures rien.
Termine par un résumé de 10 lignes : les décisions d'architecture prises et les deux ou trois points laissés à l'implémenteur.
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

⏵ Lecture des documents de référence du dépôt avant d'écrire la spécification.

Je commence par lire les fichiers demandés.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-flux.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-prefill-reparti.md"}`

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
20:           version      u16          = 1
21:           n_couches    u32
22:           cachés       u32
23: liste     couche       u16          < 1000 : entrée d'attention
24:                                     >= 1000 : entrée de FFN (couche - 1000)
25:           jeton        u32          COMPTEUR GLOBAL de jeton, pas la position
26:        
… [9294 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-prefill-reparti.md</path>
<type>file</type>
<content>
1: # Plan — le préremplissage par lots sur le fil (phase 3.4)
2: 
3: > **État (30/09, après mise en œuvre).** Ce plan a été suivi : le mode 3 existe,
4: > le préremplissage par lots est fidèle (écart **0,00e0** en 4 lots de 64 comme en
5: > un seul lot) et `reports/rapport-prefill-reparti.md` consigne les mesures. Trois
6: > écarts au plan, tous volontaires : la version du protocole est passée à **4** (et
7: > non 3) parce que le contrat d'activation transporte désormais aussi les top-k ;
8: > l'échappement d'indice du mode blocs s'écrit sur **deux** octets (le plan le
9: > disait, le code en écrivait quatre) ; et la règle R4 (plafond de 256 Mo) est
10: > maintenant DANS le code, avec son test. Les sections ci-dessous restent le plan
11: > d'origine — elles ne sont pas réécrites, pour qu'on puisse comparer.
12: 
13: **En une ligne** : aujourd'hui un flux = un jeton, donc un préremplissage de N
14: jetons paie N allers-retours ; on ajoute un **mode 3** qui transporte N états
15: dans **un seul** message, et le banc réparti doit rendre **0,00e0**.
16: 
17: Ce document
… [23745 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-prefill-reparti.md"}`

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
… [4487 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l drave-core/src/main.rs drave-core/src/model.rs && grep -n \"MODE_LOT\\|MODE_BLOCS\\|VERSION_FLUX\\|TAILLE_TETE\\|PLAFOND_FLUX\\|encoder_paires_blocs\\|decoder_paires_blocs\\|fn envoyer_lot\\|fn envoyer_flux\\|fn recevoir_flux\\ … [136 caractères tronqués]`

  ```
3508 drave-core/src/main.rs
  3928 drave-core/src/model.rs
  7436 total
1376:const VERSION_FLUX: u8 = 4;
1387:const MODE_BLOCS: u8 = 2;
1393:const MODE_LOT: u8 = 3;
1404:const TAILLE_TETE: usize = 4 + 1 + 1 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 1
1446:struct Flux {
1465:const PLAFOND_FLUX: usize = 256 << 20;
1468:fn verifier_taille(octets: usize, quoi: &str) -> std::io::Result<()> {
1469:    if octets > PLAFOND_FLUX {
1471:            format!("{quoi} : {octets} octets au-delà du plafond de {} Mo — flux refusé                      (règle R4 de docs/plan-prefill-reparti.md)", PLAFOND_FLUX >> 20)));
1479:enum ChargeFlux {
1548:fn encoder_paires_blocs(idx: &[u16], val: &[i8]) -> Vec<u8> {
1565:/// Décode `n` paires écrites par `encoder_paires_blocs`.
1566:fn decoder_paires_blocs(corps: &[u8], n: usize) -> Result<(Vec<u16>, Vec<i8>), String> {
1570:    if n.saturating_mul(2) > PLAFOND_FLUX {
1572:                           PLAFOND_FLUX >> 20));
1602:fn envoyer_flux(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos: u32,
1609:    let (n, echelle, corps): (usize, f32, Vec<u8>) = if mode == MODE_BLOCS {
1620:        let paires = encoder_paires_blocs(&idx, &val);
1641:    let mut tete = Ve
… [2206 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "offset": 1360, "limit": 260}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "offset": 1620, "limit": 300}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1360: /// Cadriciel : `u32` magie, `u32` plage (debut, fin), `u32` position, `u32`
1361: /// dimension, puis les activations en f32. C'est le même contenu que le format
1362: /// de trace, réduit à ce qu'un nœud a besoin de recevoir pour continuer.
1363: const MAGIE_FLUX: u32 = 0x4452_5631;   // "DRV1"
1364: /// Version du protocole de flux. Elle est dans CHAQUE en-tête : un pair d'une
1365: /// autre version est refusé avec un message qui dit laquelle il parle, plutôt
1366: /// que de laisser lire des octets qui ne veulent pas dire la même chose.
1367: /// Version 4 : le bloc de réglages transporte AUSSI les top-k (par projection,
1368: /// attention, q·k, MoE). En version 3, deux nœuds lancés avec des `--topk-*`
1369: /// différents calculaient deux choses différentes en silence — le même défaut que
1370: /// les niveaux et le seuil, dont le correctif était resté incomplet.
1371: ///
1372: /// Version 3 : ajoute le mode LOT. Le passage à 3 n'est pas cosmétique — un pair
1373: /// en version 2 lirait `n × 4` octets d'un corps qui en fait `n × hidden × 4`,
1374: /// se dé
… [12983 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1620:         let paires = encoder_paires_blocs(&idx, &val);
1621:         // La longueur est écrite : avec les échappements, elle n'est pas
1622:         // déductible du nombre de paires, et un décodeur qui la suppose lit
1623:         // hors du tampon.
1624:         c.extend_from_slice(&(paires.len() as u32).to_le_bytes());
1625:         c.extend_from_slice(&paires);
1626:         (idx.len(), 0f32, c)
1627:     } else if mode == MODE_LISTE {
1628:         let (idx, val, ech) = mdl.expect("modèle requis pour quantifier un flux")
1629:                                  .flux_en_liste(actifs);
1630:         let mut c = Vec::with_capacity(idx.len() * 4);
1631:         for (&i, &v) in idx.iter().zip(val.iter()) {
1632:             c.extend_from_slice(&i.to_le_bytes());
1633:             c.extend_from_slice(&v.to_le_bytes());
1634:         }
1635:         (idx.len(), ech, c)
1636:     } else {
1637:         let mut c = Vec::with_capacity(actifs.len() * 4);
1638:         for v in actifs { c.extend_from_slice(&v.to_le_bytes()); }
1639:         (actifs.len(), 0f32, c)
1640:    
… [16199 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 220, "offset": 1920}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1920:     let lot = opt.lot.max(1);
1921:     let mut mdl = model::Model::load(&chemin, ctx, fils(&opt), true, opt.keep, false, 0, 0);
1922:     appliquer_quantification(&mut mdl, &opt);
1923:     if opt.options_actives { options_actives(&mdl, "pilote du flux", opt.ctx_impose, true, opt.keep); }
1924:     let mode = if opt.flux_blocs { MODE_BLOCS }
1925:                else if opt.flux_liste { MODE_LISTE }
1926:                else { MODE_DENSE };
1927:     println!("[flux] quantification : {} niveaux, seuil {}, top-k {}, renorm {}",
1928:              mdl.act_levels, mdl.act_thresh, mdl.act_topk, mdl.act_renorm);
1929:     let n_layer = mdl.cfg.n_layer;
1930:     let ids: Vec<u32> = if opt.ids.is_empty() {
1931:         (1..=limite as u32).collect()
1932:     } else { opt.ids.clone() };
1933:     if ids.len() < 2 {
1934:         // La perplexité est une moyenne sur `len - 1` jetons notés : avec un seul
1935:         // jeton elle vaut NaN, et un NaN affiché comme un résultat ne dit rien.
1936:         println!("[flux] il faut au moins DEUX jetons pour noter une perplexit
… [11403 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"flux_en_liste\\|emb_imposee_lot\\|fn forward_lot\\|pub fn forward\\b\\|fn norme_finale\\|fn logits_lot\\|TAILLE_TETE\\|MODE_LOT\\|MODE_LISTE\\|MODE_BLOCS\\|flux_brut\" drave-core/src/model.rs | head -60", "description": "Re … [34 caractères tronqués]`

  ```
928:    pub emb_imposee_lot: Option<Vec<f32>>,
940:    pub flux_brut: bool,
1773:            couche_debut: 0, couche_fin: n_layer_total, flux_brut: false,
1775:            emb_imposee: None, emb_imposee_lot: None, lot: 1,
2320:    pub fn forward_lot(&mut self, toks: &[u32], pos0: usize) -> Vec<Vec<f32>> {
2328:        let impose = self.emb_imposee_lot.take();
2803:        if self.flux_brut || self.couche_fin < self.cfg.n_layer {
2960:        if self.couche_fin >= self.cfg.n_layer && !self.flux_brut {
2984:    pub fn forward(&mut self, tok: u32, pos: usize) -> Vec<f32> {
3482:        if self.flux_brut || self.couche_fin < cfg.n_layer {
3495:    pub fn logits_lot(&mut self, hs: &[Vec<f32>]) -> Vec<Vec<f32>> {
3607:    pub fn flux_en_liste(&self, x: &[f32]) -> (Vec<u16>, Vec<i16>, f32) {
3638:    pub fn flux_en_liste_blocs(&self, x: &[f32]) -> (Vec<u16>, Vec<i8>, Vec<f32>) {
3666:    pub fn norme_finale(&self, x: &[f32]) -> Vec<f32> {
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 120, "offset": 2315}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 100, "offset": 3595}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
2315:     ///
2316:     /// L'attention reste par jeton (elle est causale : le jeton i doit voir le
2317:     /// cache écrit par les jetons < i), mais elle réutilise les Q, K, V calculés
2318:     /// en lot. Les modèles à experts retombent sur le chemin jeton par jeton :
2319:     /// leur regroupement par expert est l'étape suivante.
2320:     pub fn forward_lot(&mut self, toks: &[u32], pos0: usize) -> Vec<Vec<f32>> {
2321:         let t = toks.len();
2322:         // Lot IMPOSÉ (préremplissage réparti) : les états arrivent de l'autre
2323:         // nœud, on ne repasse pas par `token_embd`. Lu avant tout le reste — y
2324:         // compris avant le retour anticipé sur `t == 0`, sinon une trame vide
2325:         // laissait l'état imposé en place pour le lot suivant (D7 de la
2326:         // relecture) — et consommé une seule fois, comme `emb_imposee` pour un
2327:         // jeton seul.
2328:         let impose = self.emb_imposee_lot.take();
2329:         if t == 0 { return Vec::new(); }
2330:         if t == 1 {
2331:             if let Some(v) = impose { self.
… [5808 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
3595:         if self.tete_gpu_q6k {
3596:             machine.proj_q6k(m, xd, sx)
3597:         } else {
3598:             machine.tete_warp(m, xd).map(|y| y.iter().map(|v| v * sx).collect())
3599:         }
3600:     }
3601: 
3602:     /// **Encode un flux pour le réseau** : la même quantification que la trace
3603:     /// (mêmes `act_levels`, `act_thresh`, `act_topk`, `act_renorm`), donc les
3604:     /// mêmes octets que sur le disque — indice `u16`, valeur `i16`, une échelle
3605:     /// par liste. Transporter la LISTE au lieu du vecteur dense est le sujet de
3606:     /// la phase 3 : « des listes, pas des matrices » vaut aussi sur le câble.
3607:     pub fn flux_en_liste(&self, x: &[f32]) -> (Vec<u16>, Vec<i16>, f32) {
3608:         assert!(x.len() <= u16::MAX as usize,
3609:                 "flux de {} canaux : l'indice u16 ne suffit pas", x.len());
3610:         let mut scratch = Vec::with_capacity(x.len());
3611:         // Le champ de valeur du fil fait 16 bits : on quantifie donc sur 32 767
3612:         // niveaux, PAS sur `act_levels`. C'est gratuit — deu
… [4867 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls docs reports && grep -rn \"3\\.5\" docs/*.md | head -20", "description": "Liste docs/reports et cherche le critère 3.5"}`

  ```
docs:
colab-reparti.md
comparaison-spiking.md
contexte-long.md
convertisseur.md
format-flux.md
histoire.md
plan-mla-vision.md
plan-prefill-reparti.md
programme-recherche.md
roadmap.md
vision.md

reports:
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
docs/
… [640 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' reports/rapport-transport-liste.md", "description": "Lit le début du rapport transport liste"}`

  ```
# Phase 3.2 — transporter la LISTE au lieu du vecteur

**En une ligne** : le flux peut voyager en liste creuse — **897 octets au lieu de
3 623** à seuil 5 %, et **1 568** avec des indices par écarts — mais jeter des
canaux coûte cher (**×1,8 de perplexité** à ce seuil), et la courbe est là pour
dire où.

## Le protocole, mesuré

Deux modes dans le même en-tête de 39 octets — magie, version, mode, plage,
position, dimension, échelle, **et les réglages d'activation** :

| mode | contenu | octets par flux (Qwen2.5-0.5B, 896 canaux) |
|---|---|---|
| 0 · dense f32 | `896 × f32` | **3 623** (39 + 3 584) |
| 1 · listes | `n × (indice u16 · valeur i16)` | 39 + 4 × actifs |

Le mode 1 est le format du disque, à l'octet près. La réponse est encodée comme
la demande : un pair qui parle en listes reçoit des listes.

## La courbe (40 jetons, 12 couches de chaque côté)

| seuil | activité | octets/flux (aller) | octets/flux (retour) | perplexité locale | perplexité répartie | écart |
|---|---|---|---|---|---|---|
| dense f32 | 100 % | 3 623 | 3 623 | 144,8289 | **144,8289** | **0,00e0** |
| listes 0,00 | 100,0 % (896) | 3 623 | 3 623 | 144,8289 | 141,0539 | 2,6e-2 |
| listes 0,02 | 60,4 % (541)
… [3010 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"2,7e-2\\|2.7e-2\\|mode 4\\|mode4\" docs reports drave-core/src | head -30 && echo ---- && sed -n '40,80p' docs/roadmap.md", "description": "Cherche les mentions du mode 4 et du critère"}`

  ```
docs/roadmap.md:306:listes (mode 4), l'ordonnanceur de placement, et la démonstration sur Colab, dont
docs/format-flux.md:117:f32 dense (3,5 ko par jeton) ; le lot en listes est le mode 4, pas encore écrit.
docs/plan-prefill-reparti.md:31:| quels modes dans le lot ? | **dense f32 seulement** | c'est le seul transport **sans perte**, donc le seul qui puisse exiger 0,00e0 ; un lot de listes est un mode 4 (voir §7) |
docs/plan-prefill-reparti.md:343:l'écart serait au contraire du même ordre que le chemin par jeton (2,7e-2 pour
docs/plan-prefill-reparti.md:414:* **Le lot en listes** : c'est le mode 4, à écrire quand le débit gênera. Corps
docs/plan-prefill-reparti.md:418:  d'actifs en tête. Gain attendu : ÷2,3 sur le fil pour ~2,7e-2 d'écart
reports/rapport-transport-liste.md:133:| blocs | 0,01 | 78,6 % | 2 268 | 2,7e-2 |
reports/rapport-coherence-docs.md:75:| 24 | `docs/format-flux.md:96`, `docs/plan-prefill-reparti.md:21` | « le lot en listes est le **mode 4**, pas encore écrit » | les modes du code sont 0, 1, 2, 3 ; aucun mode 4 n'existe ni n'est réservé dans `recevoir_flux` | MANQUANT |
reports/rapport-coherence-docs.md:169:   (14 champs), et retirer la mention du mode 4.
reports/r
… [4656 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '100,175p' reports/rapport-transport-liste.md", "description": "Lit la section blocs du rapport transport"}`

  ```
Trois octets par neurone actif (indice u16, valeur **i8**) plus une échelle f32
par bloc de 32. Le seuil reste global — c'est lui qui décide de la sparsité.

| seuil | activité | octets/flux | écart | à comparer aux listes i16 |
|---|---|---|---|---|
| 0,00 | 98,1 % | 2 793 | 7,1e-2 | 3 622 octets · 2,6e-2 |
| 0,02 | 60,4 % | **1 778** | **2,2e-3** | 2 203 octets · 4,9e-2 |
| 0,05 | 24,0 % | 799 | 1,1e0 | 897 octets · 8,1e-1 |

**En régime creux, l'échelle par bloc gagne sur les deux tableaux** : à seuil
0,02, ÷1,24 d'octets *et* une fidélité vingt fois meilleure (2,2e-3 contre
4,9e-2). C'est cohérent : une échelle unique par vecteur donne une erreur
*absolue* constante, donc catastrophique en relatif sur les canaux faibles ; une
échelle par bloc borne l'erreur *relative*, ce qui autorise des valeurs à un
octet.

À pleine densité, en revanche, l'i16 avec une échelle globale est plus fidèle
(2,6e-2 contre 7,1e-2) — mais à pleine densité il n'y a rien à gagner : 2 793
octets contre 3 623, et les deux modes sont de toute façon « taille du dense ».
**Le régime qui compte est le régime creux, et c'est là que les blocs gagnent.**

Configuration utilisable aujourd'hui : `--flux-blocs --ac
… [2491 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '3320,3508p' drave-core/src/main.rs", "description": "Lit les tests flux existants"}`

  ```
let p = mdl.prof;
    let tot = p[0] + p[1] + p[2] + p[3];
    println!("    postes (ms/token) : projets-attn {:.2} | rope {:.2} | attention {:.2} | proj+mlp {:.2} | somme {:.2} | reste (tête + échantillonnage) {:.2}",
             p[0] / n as f64 * 1e3, p[1] / n as f64 * 1e3, p[2] / n as f64 * 1e3,
             p[3] / n as f64 * 1e3, tot / n as f64 * 1e3,
             (sec - tot) / n as f64 * 1e3);
    println!("    dont tête de sortie {:.2} | notation log-sum-exp {:.2} (le reste du « reste » n'est pas chronométré)",
             t_tete / n as f64 * 1e3, t_note / n as f64 * 1e3);
    println!("    dont attention : scores {:.2} | softmax {:.2} | somme pondérée + écriture KV {:.2}",
             p[4] / n as f64 * 1e3, p[5] / n as f64 * 1e3,
             (p[2] - p[4] - p[5]) / n as f64 * 1e3);
}

#[cfg(test)]
mod tests_flux {
    //! Les tests du PROTOCOLE et du CODEC. Ils manquaient : les deux bugs les
    //! plus coûteux de la session (un en-tête d'un octet trop long, un
    //! échappement d'indice écrit sur quatre octets et lu sur deux) étaient
    //! invisibles pour les six tests existants, qui ne couvraient que le cache KV.
    use super::*;
    use std::net::{TcpListener, Tc
… [7938 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"flux_blocs\\|flux_liste\\|opt.lot\\|DRAVE_FLUX_VERIF\\|actifs()\" drave-core/src/main.rs | head -40", "description": "Repère les options et usages liés aux flux"}`

  ```
438:    flux: bool, session: bool, chat: bool, flux_liste: bool, flux_blocs: bool,
565:            "--flux-liste" => { o.flux_liste = true; 1 }
566:            "--flux-blocs" => { o.flux_blocs = true; 1 }
1920:    let lot = opt.lot.max(1);
1924:    let mode = if opt.flux_blocs { MODE_BLOCS }
1925:               else if opt.flux_liste { MODE_LISTE }
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"flux_blocs\\|flux_liste\\|lot:\" drave-core/src/main.rs | head -30 && echo ==== && grep -n \"flux_lot(\\|jeton_trace\" drave-core/src/model.rs | head -30", "description": "Repère les options CLI et le compteur de trace"}`

  ```
438:    flux: bool, session: bool, chat: bool, flux_liste: bool, flux_blocs: bool,
457:    lot: usize,
565:            "--flux-liste" => { o.flux_liste = true; 1 }
566:            "--flux-blocs" => { o.flux_blocs = true; 1 }
1924:    let mode = if opt.flux_blocs { MODE_BLOCS }
1925:               else if opt.flux_liste { MODE_LISTE }
====
910:    pub jeton_trace: u64,
1774:            cache_experts, mla, mla_cache, jeton_trace: 0, trace: None, flux_force: None,
2344:        let j0 = self.jeton_trace + 1;
2345:        self.jeton_trace += t as u64;
2434:            Self::flux_lot(&mut self.trace, &mut self.flux_force, j0,
2644:            Self::flux_lot(&mut self.trace, &mut self.flux_force, j0,
2826:    fn flux_lot(trace: &mut Option<TraceFlux>, force: &mut Option<FluxRelecteur>,
2986:        self.jeton_trace += 1;
3062:                let j = self.jeton_trace;
3081:                    let j = self.jeton_trace;
3317:                let j = self.jeton_trace;
3325:                    let j = self.jeton_trace;
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"DRAVE_FLUX_VERIF\" drave-core/src | head -5 && echo ==== && grep -rn \"\\.actifs()\" drave-core/src | head -5 && echo ==== && sed -n '450,470p' drave-core/src/main.rs && echo ==== && sed -n '2426,2445p' drave-core/src/mode … [138 caractères tronqués]`

  ```
drave-core/src/model.rs:3060:                let verif = std::env::var("DRAVE_FLUX_VERIF").is_ok();
====
====
    act_thresh: f32, act_topk: usize, act_renorm: bool, topk_proj: [usize; 7],
    // --- mesure
    logits_bin: Option<String>, ppl_profil: bool,
    /// Profilage des neurones « chauds » (idée de PowerInfer) et fichier de
    /// sortie du classement.
    profil_neurones: bool, neurones_sortie: Option<String>,
    /// Taille du lot de préremplissage : 1 = jeton par jeton (défaut).
    lot: usize,
    harmony: Option<String>, harmony_contexte: Option<String>,
    // --- rotation
    sans_yarn: bool,
    // --- expériences
    patch: Option<String>, hebb_layer: Option<usize>, hebb_q: f32,
    hebb_out: String, ffn_gain: Option<(usize, f32)>, matrix: String,
    // --- tokenize / plan
    texte: Option<String>, fichier: Option<String>, sortie: Option<String>,
}

/// Analyse la ligne de commande UNE fois. Les drapeaux à valeur consomment
/// l'argument suivant (`i += 2`) ; les drapeaux booléens non (`i += 1`).
fn analyser(args: &[String]) -> Options {
====
        for l in self.couche_debut..self.couche_fin {
            let lay = &self.layers[l];
            // 1. norme d'en
… [2701 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"\\-\\-lot\\|\\-\\-flux-blocs\\|\\-\\-flux-liste\" drave-core/src/main.rs | head -20 && echo ==== && grep -rn \"même commit\\|version\" docs/colab-reparti.md | head -10", "description": "Cherche l'aide CLI et la règle Colab" … [1 caractères tronqués]`

  ```
537:            "--lot" => { o.lot = suivant(i).parse().unwrap(); 2 }
565:            "--flux-liste" => { o.flux_liste = true; 1 }
566:            "--flux-blocs" => { o.flux_blocs = true; 1 }
1917:    // `--lot T` : préremplissage par LOTS sur le fil. La référence locale est
1987:            eprintln!("[flux] --flux-liste / --flux-blocs ne s'appliquent PAS aux lots \
1988:(mode 4 non écrit) : le lot part en f32 dense. À --lot 1, le mode choisi s'applique.");
====
23:| version du protocole | ✅ dans chaque en-tête ; un pair incompatible est refusé en le disant |
116:1. **Même build des deux côtés** : la version est dans chaque en-tête, un
117:   désaccord est refusé avec un message clair — mais autant cloner le même commit.
119:   différent (quantification, version) donne des calculs différents.
[stderr]
grep: warning: stray \ before -
grep: warning: stray \ before -
grep: warning: stray \ before -
grep: warning: stray \ before -
grep: warning: stray \ before -
  ```

