# Session DSH — relecture

- identifiant : `7c876089-605c-4836-930e-925a66028509`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-09-30 13:10:29
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu es relecteur ADVERSARIAL dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM en Rust, `std` seul, binaire `drave`). Tout est en FRANÇAIS : écris en français. Ton rôle est de TROUVER DES DÉFAUTS dans des correctifs récents, pas de les valider.

CONTEXTE : une session a corrigé, entre 13h et 13h10, une série de défauts trouvés par une relecture précédente. Ces CORRECTIFS n'ont été relus par personne. Les commits à attaquer (du plus récent au plus ancien) :

- `01b7274` — un drapeau inconnu (`--keeep`) est désormais signalé
- `1bc0470` — plafond de 256 Mo sur les allocations pilotées par le réseau (règle R4)
- `1a4beb3` — tableau de bord `--options-actives`
- `901f28d` — six défauts corrigés (D2 compteur de rejeu aveugle, D3 clés de trace, D4 pair factice, D5 modes sparse ignorés en lot, D6 panique du client, D7/D8) + quatre tests unitaires
- `a9fff24` — `VERSION_FLUX` = 4 et échappement d'indice réseau sur 2 octets
- `86ddf12` — encodage des indices par écarts (disque)

CE QU'IL FAUT CHERCHER, en priorité :
1. **Régressions dans les correctifs eux-mêmes.** Le changement de clé de trace (`jeton_trace` avancé une fois par lot, 1-based) est-il cohérent avec TOUS les chemins qui écrivent ou lisent une trace (`forward`, `forward_lot`, `forward_mla`, `flux_lot`, `--trace-flux`, `--flux-forcer`, `--depuis`, le découpage en fenêtres) ? Une trace écrite à contexte 256 puis rejouée à contexte 512 (deux fenêtres) donne-t-elle les mêmes clés ? Et `forward_mla` (modèle MLA synthétique) ?
2. **Le plafond R4** : refuse-t-il des flux LÉGITIMES ? Un lot de 8 192 jetons × 8 192 canaux (268 Mo) passe-t-il ? Le plafond est-il appliqué avant CHAQUE allocation venue du réseau, y compris les échelles du mode blocs (`n_blocs × 4`) et la longueur des paires ?
3. **`--options-actives`** : peut-il paniquer sur un modèle sans cache KV (`mdl.kv` vide), sur un modèle MLA, ou dans un mode où `mdl` n'est pas encore chargé ? Affiche-t-il des valeurs d'AVANT application quelque part (le défaut exact qu'il est censé traquer) ?
4. **Les tests ajoutés** : testent-ils ce qu'ils prétendent ? Le test de troncature passe-t-il pour la bonne raison (refus) et non par chance ? Le test du plafond pourrait-il se bloquer ou paniquer sur une autre machine ?
5. **La détection de drapeau inconnu** : un drapeau connu dont la VALEUR commence par `--` (par exemple `--prompt "--bonjour"`) est-il pris pour un drapeau inconnu ? Un drapeau positionnel après un drapeau booléen est-il mal interprété ?

MÉTHODE : lis les diffs (`git show <sha>`), puis PROUVE chaque défaut avec une commande exécutable (`cargo test --release` est autorisé ; les exécutions du moteur avec `--limit 4` aussi ; `--flux-serveur`/`--ppl-reparti` autorisés mais tu DOIS tuer tes serveurs et ne pas dépasser 2 minutes par exécution). ATTENTION : une campagne de mesure tourne en ce moment (16 fils sur 40) — reste sous 8 fils et évite les commandes de plus de 3 minutes.

INTERDIT : modifier un fichier du dépôt (rends ton rapport dans ta réponse), lancer `cargo build` sur le chemin critique plus d'une fois, tuer un processus qui n'est pas le tien (les `drave` de la campagne en cours ne sont PAS à toi).

Termine par un résumé de 10 lignes : nombre de défauts réels prouvés, les deux plus graves avec leur preuve, et ce que tu n'as pas pu vérifier.
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

⏵ Démarrage de la relecture adversariale des correctifs récents

Je commence par inspecter le dépôt et les commits ciblés.

- **bash** `{"command": "git log --oneline -12 && echo \"---\" && ls", "description": "List recent commits and repo root", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
fc715e9 Portes revérifiées après la journée : 19,3885 · 15,1757 · 11 tests
5b2ec03 Rapport transport : l'en-tête dit maintenant ce que son tableau mesure
00dcebc Cohérence (suite) : le croisement push/pull, les comptes de lignes, et une erreur que j'avais écartée à tort
d0d0ede Cohérence : versions et comptes de flux remis d'aplomb partout
a2952f7 Handoff : les garde-fous de l'après-midi et deux lignes de mesures
d89e340 Cache KV : int4/int4 mesuré (+364 %), la courbe a ses six premiers points
01b7274 Un drapeau inconnu n'est plus avalé en silence
1a4beb3 `--options-actives` : le tableau de bord des réglages qui agissent
809763d Kit Colab vérifié de bout en bout (clonage, compilation 23 s, écart 0,00e0)
da6415b Colab : le mode lot chiffré dans la recette (2,6 s contre 47,6 s à 20 ms par message)
c2ff9a8 Mode lot sur un lien latent : 18× (2,6 s contre 47,6 s)
1bc0470 Règle R4 : plafond des allocations pilotées par le réseau (256 Mo)
---
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
run_real_
… [59 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat 01b7274 1bc0470 1a4beb3 901f28d a9fff24 86ddf12 | head -120", "description": "Show stats for target commits", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
commit 01b7274a5e562546ffdecf88a7f9db6a4fae221e
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 13:06:06 2026 -0400

    Un drapeau inconnu n'est plus avalé en silence
    
    `--keeep 0.05` (une faute de frappe) faisait tourner le modèle entier sans
    élagage et sans un mot. L'analyse retient maintenant les `--xxx` qu'elle ne
    reconnaît pas et les nomme, en renvoyant au tableau de bord `--options-actives`
    qui montre, lui, ce qui s'applique vraiment. Vérifié : la faute est signalée, et
    l'orthographe correcte ne produit aucun message.

 drave-core/src/main.rs                             |  18 ++-
 journal/sessions/MANIFEST.md                       |   4 +-
 .../bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md | 179 +++++++++++++++++++++
 .../rapport.md                                     |  17 +-
 4 files changed, 206 insertions(+), 12 deletions(-)

commit 1bc04702cb1ca06b15f60715ca3a215727fb25e0
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 12:57:35 2026 -0400

    Règle R4 : plafond des allocations pilotées par le réseau (256 Mo)
    
    La relecture adversariale avait relevé un soupçon qu'elle n'a pas voulu tester —
    « un `n` hostile fait deman
… [5636 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des diffs des six correctifs ciblés

- **bash** `{"command": "git show 901f28d -- drave-core/src/main.rs > /tmp/d901.diff; wc -l /tmp/d901.diff; sed -n '1,200p' /tmp/d901.diff", "description": "Show main.rs diff of 901f28d part 1", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
297 /tmp/d901.diff
commit 901f28dec59f3893901c15d8bc00127ad4ffbf52
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 12:46:20 2026 -0400

    Relecture adversariale : six défauts corrigés, et des tests qui les auraient attrapés
    
    `reports/`-style review, cette fois en attaquant mes propres commits. Six défauts
    réels, tous corrigés et vérifiés :
    
    - **D2 (le plus grave)** : dans le rejeu par LOTS, une clé absente des deux cartes
      n'était comptée NULLE PART — le garde-fou ajouté une heure plus tôt était aveugle
      dès `--lot > 1`, et une trace étrangère s'affichait « 0 manquante » avec une
      perplexité fausse. Vérifié : trace de la couche 0 seule → `8 servies, 376
      manquantes` + alerte.
    - **D3** : les clés de trace ne voulaient pas dire la même chose selon `--lot`. En
      lot, le compteur avançait de `t` à CHAQUE appel (deux par couche : familles
      attention et FFN) ; en `--lot 1`, il avançait deux fois par jeton (une fois par
      `forward_lot`, une fois par `forward` délégué) — les clés étaient 2, 4, 6… Une
      trace écrite dans un mode était illisible dans l'autre. Corrigé : une seule clé
      par lot, 1-based, avancée une fo
… [9154 caractères tronqués]
  ```

- **bash** `{"command": "git show a9fff24 > /tmp/da9.diff; git show 86ddf12 > /tmp/d86.diff; wc -l /tmp/da9.diff /tmp/d86.diff", "description": "Dump diffs a9fff24 and 86ddf12", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
1067 /tmp/da9.diff
  281 /tmp/d86.diff
 1348 total
  ```

- **bash** `{"command": "sed -n '200,300p' /tmp/d901.diff", "description": "Show rest of 901f28d main.rs diff", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
+            };
             t_pair += horloge.elapsed().as_secs_f64();
             octets_recus += TAILLE_TETE as u64 + rep.octets_corps as u64;
             let etats = rep.charge.plat().to_vec();
@@ -1881,7 +1916,14 @@ fn run_ppl_reparti(opt: Options, pair: &str) {
         octets_envoyes += o as u64;
         actifs_envoyes += a as u64;
         flux_envoyes += 1;
-        let rep = recevoir_flux(&mut sock, mdl.cfg.hidden).expect("réception du flux");
+        let rep = match recevoir_flux(&mut sock, mdl.cfg.hidden) {
+            Ok(r) => r,
+            Err(e) => {
+                eprintln!("[flux] le nœud moteur a fermé la connexion ({e}) — version du \
+protocole, réglages, ou contexte : il a dit pourquoi de son côté.");
+                std::process::exit(1);
+            }
+        };
         // Ce que coûte le découpage : le calcul local, et l'attente du pair
         // (son calcul + l'aller-retour réseau) — la latence, pas le débit.
         t_pair += horloge.elapsed().as_secs_f64();
@@ -3067,6 +3109,10 @@ fn run_ppl(opt: Options) {
                      "  ← la moitié au moins n'a pas servi : vérifier la trace"
                  } else { "" });
     }
+    if n == 
… [3240 caractères tronqués]
  ```

- **bash** `{"command": "git show 1bc0470 -- drave-core/src/main.rs", "description": "Show R4 cap diff", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
commit 1bc04702cb1ca06b15f60715ca3a215727fb25e0
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 12:57:35 2026 -0400

    Règle R4 : plafond des allocations pilotées par le réseau (256 Mo)
    
    La relecture adversariale avait relevé un soupçon qu'elle n'a pas voulu tester —
    « un `n` hostile fait demander jusqu'à 15 To au noyau, avant tout contrôle ». Elle
    avait raison de ne pas le tester, et le corriger coûte vingt lignes : les trois
    modes qui allouent sur une taille lue dans l'en-tête (dense, blocs, lot) passent
    par `verifier_taille`, qui refuse au-delà de 256 Mo en NOMMANT la règle.
    
    La règle R4 était écrite dans `docs/plan-prefill-reparti.md` sans être dans le
    code : elle y est maintenant, avec son test — un pair qui annonce 100 millions
    d'états reçoit un refus qui nomme le plafond, et rien n'est alloué. **11 tests
    passent** (4 sur le protocole, 1 sur le plafond, 6 préexistants).
    
    Au passage : la première version du test se bloquait pour toujours (le pair
    attendait une réponse que le client, ayant refusé, n'envoie jamais) — la suite de
    tests a un délai, elle l'a tué, et le commentaire explique pourquoi la lecture ne
… [5379 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Analyse du code source autour du plafond R4 et du décodeur

- **bash** `{"command": "grep -n \"MODE_LOT\\|MODE_BLOCS\\|MODE_DENSE\\|MODE_LISTE\\|fn recevoir_flux\\|verifier_taille\\|n_blocs\\|echelles\" drave-core/src/main.rs | head -80", "description": "Grep flux modes and caps", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
1360:const MODE_DENSE: u8 = 0;
1364:const MODE_LISTE: u8 = 1;
1369:const MODE_BLOCS: u8 = 2;
1375:const MODE_LOT: u8 = 3;
1450:fn verifier_taille(octets: usize, quoi: &str) -> std::io::Result<()> {
1464:    Blocs { idx: Vec<u16>, val: Vec<i8>, echelles: Vec<f32> },
1486:            ChargeFlux::Blocs { idx, val, echelles } => {
1489:                    x[i as usize] = v as f32 * echelles[i as usize / 32];
1567:    let (n, echelle, corps): (usize, f32, Vec<u8>) = if mode == MODE_BLOCS {
1568:        let (idx, val, echelles) = mdl.expect("modèle requis pour quantifier un flux")
1575:        let mut c = Vec::with_capacity(4 + echelles.len() * 4 + idx.len() * 2);
1576:        c.extend_from_slice(&(echelles.len() as u32).to_le_bytes());
1577:        for e in &echelles { c.extend_from_slice(&e.to_le_bytes()); }
1585:    } else if mode == MODE_LISTE {
1636:    tete.push(MODE_LOT);
1665:fn recevoir_flux(s: &mut std::net::TcpStream, hidden: usize) -> std::io::Result<Flux> {
1698:        MODE_LOT => {
1703:            verifier_taille(taille, &format!("lot de {n} états × {hidden} canaux"))?;
1711:        MODE_BLOCS => {
1715:            let n_blocs = u32::from_le_bytes(nb) as usize;
1716:     
… [1090 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"jeton_trace\\|trace\" drave-core/src/model.rs | head -60; echo \"===\"; grep -rn \"jeton_trace\" drave-core/src/*.rs | head -60", "description": "Grep trace key logic", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
489:/// f32 → f16 (IEEE 754 binary16), pour les échelles par bloc de la trace v3.
532:    /// Couches à tracer (toutes si vide).
658:/// Relit une trace de flux et rend, pour (couche, position), la liste
688:                                           "ce n'est pas une trace DRVF"));
693:                format!("trace DRVF en version {version} : ce lecteur lit la 1, la 2 et la 3")));
906:    /// Compteur de jetons tracés : `position` dans la trace est ce compteur, et
910:    pub jeton_trace: u64,
911:    /// Trace du flux d'activation (`--trace-flux`).
912:    pub trace: Option<TraceFlux>,
913:    /// Relecture d'une trace : les activations enregistrées REMPLACENT celles
956:    /// Capteur hebbien : accumule la trace de co-activation d'une projection
1517:        // relecture est LE mur du contexte long ; la trace le dit au chargement.
1774:            cache_experts, mla, mla_cache, jeton_trace: 0, trace: None, flux_force: None,
2338:            // (2, 4, 6…) — et une trace écrite en `--lot 1` n'était alors
2342:        // Clé de trace du lot : compteur global, 1-based, avancé une fois pour
2344:        let j0 = self.jeton_trace + 1;
2345:        self.jeton_trace += t as u64;
2434:
… [2055 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des chemins d'écriture de trace (forward_lot, forward, forward_mla, flux_lot)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "offset": 2290, "limit": 180}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "offset": 2810, "limit": 200}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
2290:         // `n_rot` = dimensions tournées ; les autres restent intactes. La
2291:         // rotation « neox » apparie `i` et `i + n_rot/2`.
2292:         let n_rot = if n_rot == 0 || n_rot > head_dim { head_dim } else { n_rot };
2293:         let half = n_rot / 2;
2294:         for h in 0..n_head {
2295:             let t = &mut v[h * head_dim..(h + 1) * head_dim];
2296:             for i in 0..half {
2297:                 let freq = 1.0 / base.powf(2.0 * i as f32 / head_dim as f32);
2298:                 let (s, c) = (pos as f32 * freq).sin_cos();
2299:                 let a = t[i];
2300:                 let b = t[i + half];
2301:                 t[i] = a * c - b * s;
2302:                 t[i + half] = b * c + a * s;
2303:             }
2304:         }
2305:     }
2306: 
2307:     /// **Préremplissage par lots** : `t` jetons d'un coup, aux positions
2308:     /// `pos0..pos0+t`.
2309:     ///
2310:     /// Toute la différence avec `forward` est dans les projections : elles
2311:     /// passent d'un produit matrice-vecteur par jeton à un produit
2312:     /// mat
… [9158 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
2810:         }
2811:         (0..t).map(|i| hn[i * h..(i + 1) * h].to_vec()).collect()
2812:     }
2813: 
2814:     /// Trace OU impose le flux d'un LOT : `xi` porte les entiers quantifiés du
2815:     /// lot (t × h) et `sx` une échelle par jeton. Sur ce chemin, le rejeu est
2816:     /// EXACT — on remplace les entiers et l'échelle, sans repasser par une
2817:     /// déquantification suivie d'une requantification.
2818:     #[allow(clippy::too_many_arguments)]
2819:     /// `j0` est la clé du PREMIER jeton du lot (compteur global, 1-based comme
2820:     /// sur le chemin jeton par jeton) : elle est calculée UNE fois par lot par
2821:     /// `forward_lot`, et non à chaque appel — `flux_lot` est appelé deux fois par
2822:     /// couche (famille attention, base 0, et famille FFN, base 1000) et les deux
2823:     /// doivent écrire les MÊMES clés. Avant, le compteur avançait de `t` à chaque
2824:     /// appel : une trace écrite avec `--lot N` n'était rejouable qu'avec le même N
2825:     /// (relecture adversariale, D3).
2826:     fn flux_lot(trace: &mut Option<Trace
… [10419 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Cartographie des chemins d'appel et du parseur d'options

- **bash** `{"command": "grep -n \"fn run_\\|fn options_actives\\|options_actives\\|forward_mla\\|forward_lot\\|\\.forward(\\|depuis\\|trace_flux\\|flux_force\\|FluxRelecteur\" drave-core/src/main.rs | head -100", "description": "Grep call sites in main.rs", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Q … [8 caractères tronqués]`

  ```
350:fn options_actives(mdl: &model::Model, mode: &str, ctx_impose: bool, dense: bool, keep: f32) {
360:             mdl.trace.is_some(), mdl.flux_force.is_some());
403:    trace_flux: Option<String>,
406:    flux_forcer: Option<String>,
412:    options_actives: bool,
435:    ppl_texte: bool, prompt: Option<String>, limit: usize, depuis: usize,
504:            "--trace-flux" => { o.trace_flux = Some(suivant(i).clone()); 2 }
505:            "--flux-forcer" => { o.flux_forcer = Some(suivant(i).clone()); 2 }
507:            "--options-actives" => { o.options_actives = true; 1 }
536:            "--depuis" => { o.depuis = suivant(i).parse().unwrap(); 2 }
617:fn run_infer(opt: Options) {
619:    let montre_options = opt.options_actives;
629:        trace_flux, trace_couches, ..
653:    if let Some(chemin) = trace_flux.as_deref() {
666:    // Appliqués en perplexité depuis toujours, oubliés ici : la déstructuration
681:        options_actives(&mdl, "inférence", ctx_impose, dense, keep);
747:        println!("ids depuis {f} : {} tokens", ids.len());
827:        for (pos, &t) in ids.iter().enumerate() { last = mdl.forward(t, pos); }
838:            last = mdl.forward(next, ids.len() + step);
… [2603 caractères tronqués]
  ```

- **bash** `{"command": "git show 1a4beb3 -- drave-core/src/main.rs drave-core/src/model.rs", "description": "Show options-actives diff", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
commit 1a4beb37cac44cb9938a8aaa619b0947678d28d7
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 13:04:20 2026 -0400

    `--options-actives` : le tableau de bord des réglages qui agissent
    
    Les deux relectures ont trouvé le même mode d'échec, et il n'est pas dans un
    calcul : **huit drapeaux « analysés mais jamais appliqués »** en une session, tous
    invisibles — la sortie ne disait nulle part quelle valeur agissait. Le tableau de
    bord lit le MODÈLE après toutes les affectations et imprime ce qu'il utilise
    vraiment :
    
    ```
    [options] mode perplexité · contexte 64 (imposé) · dense true · keep 0.050
    [options] activation : niveaux 127 · seuil 0 · k-WTA 0 · renorm false
    [options] top-k : attn 0 · q·k 0 · MoE 0 · par projection [0, 0, 0, 0, 0, 0, 0]
    [options] couches 0..24 · flux brut false · trace false · rejeu false
    [options] fenêtre 0 · motif 0 · seuil push 0.22 · lot 1 · ffn_gain Some((0, 4.0)) · hebb false
    [options] cache KV : 8 bits · clés en f16 · f16 avant false
    ```
    
    Un `--keep 0.05` qui n'aurait pas pris afficherait `keep 1.000` : le défaut saute
    aux yeux au lieu de se cacher dans un calcul. Branché dans
… [8061 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du tableau de bord en perplexité et du parseur de drapeaux

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "offset": 2889, "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
2889: fn run_ppl(opt: Options) {
2890:     let montre_options = opt.options_actives;
2891:     let Options {
2892:         ids_file: idfile, texte_file, ppl_texte: _, limit, depuis,
2893:         ctx: ctx_opt, threads: threads_opt, abits: abits_opt,
2894:         ctx_impose, threads_impose, abits_impose,
2895:         dense, auto, q4, b6, attn_window, swa_pattern,
2896:         sans_fenetre, attn_sinks, attn_topk, qk_topk, act_thresh, act_topk, act_renorm,
2897:         topk_proj, moe_topk, patch: patch_file, hebb_layer, hebb_q, hebb_out,
2898:         ffn_gain, logits_bin, keep,
2899:         ppl_profil, lot, profil_neurones, neurones_sortie, trace_flux, trace_couches, flux_forcer,
2900:         harmony, harmony_contexte, sans_yarn, ..
2901:     } = opt;
2902:     let lot = lot.max(1);
2903:     let path = &modele_chemin();
2904:     // Défauts du mode PERPLEXITÉ : 256 jetons, trois quarts des cœurs, 16 bits
2905:     // d'activation (la référence de non-régression en dépend).
2906:     let cpu = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(8);
2907:  
… [5619 caractères tronqués]
  ```

- **bash** `{"command": "git show 01b7274 -- drave-core/src/main.rs; echo \"=== parser ===\"; sed -n '470,600p' drave-core/src/main.rs", "description": "Show unknown flag diff and parser", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
commit 01b7274a5e562546ffdecf88a7f9db6a4fae221e
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 13:06:06 2026 -0400

    Un drapeau inconnu n'est plus avalé en silence
    
    `--keeep 0.05` (une faute de frappe) faisait tourner le modèle entier sans
    élagage et sans un mot. L'analyse retient maintenant les `--xxx` qu'elle ne
    reconnaît pas et les nomme, en renvoyant au tableau de bord `--options-actives`
    qui montre, lui, ce qui s'applique vraiment. Vérifié : la faute est signalée, et
    l'orthographe correcte ne produit aucun message.

diff --git a/drave-core/src/main.rs b/drave-core/src/main.rs
index fe513b6..7325169 100644
--- a/drave-core/src/main.rs
+++ b/drave-core/src/main.rs
@@ -410,6 +410,10 @@ struct Options {
     /// coûteux du dépôt — huit drapeaux « analysés mais jamais appliqués » en une
     /// seule session : une valeur affichée ici est une valeur qui agit.
     options_actives: bool,
+    /// Drapeaux `--xxx` que l'analyse n'a PAS reconnus. Ils étaient ignorés en
+    /// silence : `--keeep 0.05` (une faute de frappe) faisait tourner le modèle
+    /// entier sans élagage et sans un mot.
+    inconnus: Vec<String>,
     /// Adresse d'écoute d
… [9455 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du découpage en fenêtres et de la boucle de notation

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 150, "offset": 3009}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 130, "offset": 1690}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
3009:     if let Some(l) = hebb_layer {
3010:         let mut hb = model::Hebb::new(l, mdl.cfg.ffn, mdl.cfg.hidden, hebb_q);
3011:         hb.log_on = true;
3012:         mdl.hebb = Some(hb);
3013:         println!("journalisation : couche {l}, entrée FFN ({} dim)", mdl.cfg.hidden);
3014:     }
3015:     if profil_neurones {
3016:         mdl.activer_profil_neurones();
3017:         println!("profilage des neurones actif : un neurone compte comme actif si sa valeur \
3018:                   quantifiée n'est pas nulle (même critère que le chemin par événements)");
3019:     }
3020:     mdl.reset_events();
3021:     // Fenêtres d'évaluation : soit des tranches brutes de `ctx` jetons (mode
3022:     // historique, toutes notées), soit des tours harmony dont seuls les jetons
3023:     // de contenu sont notés.
3024:     let fenetres: Vec<(Vec<u32>, Vec<bool>)> = match &harmony {
3025:         None => {
3026:             // `--depuis N` : les fenêtres sont ancrées pour que le premier jeton
3027:             // NOTÉ ait un contexte complet (on recule de ctx-1 jetons, qui ne
302
… [7450 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1690:         topk: u(34),
1691:         renorm: tete[38] != 0,
1692:         topk_proj,
1693:         attn_topk: u(67),
1694:         qk_topk: u(71),
1695:         moe_topk: u(75),
1696:     };
1697:     let charge = match mode {
1698:         MODE_LOT => {
1699:             // `n` est le nombre d'ÉTATS, pas de canaux : la dimension vient du
1700:             // modèle du nœud qui reçoit, elle n'a pas à voyager.
1701:             let taille = n.checked_mul(hidden).and_then(|x| x.checked_mul(4))
1702:                          .unwrap_or(usize::MAX);
1703:             verifier_taille(taille, &format!("lot de {n} états × {hidden} canaux"))?;
1704:             let mut corps = vec![0u8; taille];
1705:             s.read_exact(&mut corps)?;
1706:             let etats = (0..n * hidden).map(|k| f32::from_le_bytes(
1707:                 [corps[k*4], corps[k*4+1], corps[k*4+2], corps[k*4+3]])).collect();
1708:             return Ok(Flux { n, debut, fin, pos, mode, act, octets_corps: corps.len(),
1709:                              charge: ChargeFlux::Lot(etats) });
1710:         }
… [6814 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection des écritures de trace dans `forward`, du rejeu et du banc MLA

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 70, "offset": 3040}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
3040:         // `0..n_layer` : un nœud qui reçoit un flux reprend à SA première couche.
3041:         // La boucle partait de zéro — le pilote calculait donc les 24 couches,
3042:         // envoyait l'état final, et le pair les recalculait toutes par-dessus :
3043:         // perplexité répartie 798,3 au lieu de 18,2. `forward_lot` et
3044:         // `forward_mla` respectaient déjà la plage ; `forward` était l'exception.
3045:         for l in self.couche_debut..self.couche_fin {
3046:             let lay = &layers[l];
3047:             // Fenêtre EFFECTIVE de cette couche : le motif déclaré (gpt-oss :
3048:             // une couche sur deux en attention complète) prime sur le réglage
3049:             // global. Lue en champs directs : `self` est déjà déstructuré.
3050:             let fen = if self.attn_window == 0 { 0 }
3051:                       else if self.swa_pattern <= 1 { self.attn_window }
3052:                       else if l % self.swa_pattern < self.swa_pattern - 1 { self.attn_window }
3053:                       else { 0 };
3054:             let tm = I
… [3588 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '2058,2095p' drave-core/src/main.rs; echo \"=== rejeu diag ===\"; sed -n '3159,3225p' drave-core/src/main.rs", "description": "Read banc MLA and replay diagnostics", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
fn run_banc_mla(opt: Options, sortie: &str) {
    use std::io::Write;
    let path = &modele_chemin();
    let mut mdl = model::Model::load(path, 4096, fils(&opt), opt.dense, opt.keep, false, 0, 0);
    if mdl.mla.is_none() {
        println!("pas un modèle MLA (attn_kv_a_mqa absent)");
        return;
    }
    let ids: Vec<u32> = if opt.ids.is_empty() {
        (1..=8u32).collect()
    } else { opt.ids.clone() };
    let vocab = mdl.cfg.vocab;
    let mut f = std::io::BufWriter::new(std::fs::File::create(sortie).expect("création"));
    let t0 = std::time::Instant::now();
    for (pos, &t) in ids.iter().enumerate() {
        let hn = mdl.forward_mla(t, pos);
        let lg = mdl.logits_f32(&hn);
        let mut tampon = Vec::with_capacity(vocab * 4);
        for v in lg.iter() { tampon.extend_from_slice(&v.to_le_bytes()); }
        f.write_all(&tampon).unwrap();
        println!("  position {pos} : logits[0..4] = {:?}",
                 &lg[..4.min(lg.len())].iter().map(|v| (v * 1e4).round() / 1e4).collect::<Vec<_>>());
    }
    println!("{} positions × {vocab} logits écrits dans {sortie} ({:.2} s)",
             ids.len(), t0.elapsed().as_secs_f64());
}

/// Banc du **KV déport
… [3949 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du binaire existant et des diffs a9fff24/86ddf12

- **bash** `{"command": "ls -la drave-core/ 2>/dev/null; ls -la drave-core/target/release/drave 2>/dev/null; ls -la target/release/drave 2>/dev/null; cat drave-core/Cargo.toml 2>/dev/null | head -20; ls models/ | head", "description": "Check build artifacts and models", "workdir": "/home/stephane/Data13TB/steph … [20 caractères tronqués]`

  ```
total 16
drwxr-xr-x. 1 stephane stephane   82 28 sep 11:58 .
drwxr-xr-x. 1 stephane stephane  598 30 sep 12:19 ..
-rw-r--r--. 1 stephane stephane  154 30 sep 08:44 Cargo.lock
-rw-r--r--. 1 stephane stephane  375 30 sep 08:44 Cargo.toml
drwxr-xr-x. 1 stephane stephane   94 30 sep 08:44 gpu
-rw-r--r--. 1 stephane stephane 4351 30 sep 08:44 README.md
drwxr-xr-x. 1 stephane stephane  112 30 sep 11:13 src
drwxr-xr-x. 1 stephane stephane   70 25 sep 18:32 target
-rwxr-xr-x. 2 stephane stephane 1591704 30 sep 13:05 drave-core/target/release/drave
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
Qwen2.5-0.5B-Q4_0.gguf
Qwen2.5-0.5B-Q8_0.gguf
  ```

- **bash** `{"command": "sed -n '1,120p' /tmp/da9.diff", "description": "Read a9fff24 diff head", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
commit a9fff24e8cb1681005b96d2e1c16c434cc441b6b
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 12:36:39 2026 -0400

    Deux bugs de protocole trouvés par la relecture, pas par un banc
    
    1. **`VERSION_FLUX` valait encore 3** alors que l'en-tête était passé à 79 octets
       et transportait les top-k : deux binaires « v3 » aux contrats différents se
       seraient crus compatibles et auraient divergé en silence — exactement le défaut
       que la version dans chaque en-tête existe pour empêcher. Elle vaut 4.
    2. **L'échappement d'indice, côté réseau, s'écrivait sur QUATRE octets** quand le
       décodeur en lisait DEUX (`c.extend_from_slice(&i.to_le_bytes())` au lieu de
       `[..2]`). Toute trame portant un écart ≥ 255 se désynchronisait. Vérifié
       maintenant dans les deux sens, avec un seuil de 0,6 qui ne laisse qu'un neurone
       actif par liste — donc des écarts énormes et des échappements à chaque flux.
    
    Les deux ont été trouvés par la relecture croisée des documents
    (`reports/rapport-coherence-docs.md`), pas par les bancs : les échappements sont
    rares (22 sur 8,79 M) et la version ne se voyait que dans le code.

diff --git a/drav
… [6720 caractères tronqués]
  ```

### 🤖 Assistant

⏵ État de compilation et fraîcheur du binaire

- **bash** `{"command": "git status --short; echo \"---\"; git log -1 --format='%H %ci %s'; echo \"---\"; ls -la --time-style=full-iso drave-core/src/*.rs drave-core/target/release/drave; echo \"---\"; git log --oneline -30 --format='%h %ci %s' | head -30", "description": "Check working tree and build freshness … [64 caractères tronqués]`

  ```
M journal/README.md
---
818028e3c3e8ec36889a05cd354b61849ec7c983 2026-09-30 13:12:35 -0400 Référence 6 bits re-mesurée (19,3045) plutôt que retirée
---
-rw-r--r--. 1 stephane stephane   45442 2026-09-29 13:49:27.030953906 -0400 drave-core/src/engine.rs
-rw-------. 1 stephane stephane   33061 2026-09-29 19:27:58.251471084 -0400 drave-core/src/gguf.rs
-rw-r--r--. 1 stephane stephane   39060 2026-09-30 08:44:18.353240461 -0400 drave-core/src/gpu.rs
-rw-------. 1 stephane stephane   67760 2026-09-29 07:30:58.442869846 -0400 drave-core/src/list.rs
-rw-r--r--. 1 stephane stephane  170857 2026-09-30 13:05:26.069280260 -0400 drave-core/src/main.rs
-rw-r--r--. 1 stephane stephane  205470 2026-09-30 13:02:34.097536091 -0400 drave-core/src/model.rs
-rw-------. 1 stephane stephane   20019 2026-09-28 14:34:17.944094400 -0400 drave-core/src/tokenizer.rs
-rwxr-xr-x. 2 stephane stephane 1591704 2026-09-30 13:05:49.569560823 -0400 drave-core/target/release/drave
---
818028e 2026-09-30 13:12:35 -0400 Référence 6 bits re-mesurée (19,3045) plutôt que retirée
7c6bd5d 2026-09-30 13:11:42 -0400 Format de flux : la taille par neurone actif, dense et creuse
b2767fe 2026-09-30 13:11:13 -0400 Feuille de rout
… [2890 caractères tronqués]
  ```

- **bash** `{"command": "cd drave-core && ./target/release/drave --modele models/Qwen2.5-0.5B-Q8_0.gguf --keeep 0.05 --limit 2 --ppl-texte /dev/null 2>&1 | head -20; echo \"exit=$?\"", "description": "Test whether binary reports unknown flag", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
[options] 1 drapeau(x) INCONNU(S), donc sans effet : --keeep
[options] (une faute de frappe suffit — `--options-actives` montre ce que le moteur applique vraiment)

thread 'main' (536779) panicked at src/model.rs:1368:34:
ouverture du GGUF: Os { code: 2, kind: NotFound, message: "No such file or directory" }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
exit=0
  ```

### 🤖 Assistant

⏵ Lecture de `main()` pour comprendre la position du chemin de modèle

- **bash** `{"command": "grep -n \"fn main\\|args\\[1\\]\\|MODELE.set\\|analyser(\" drave-core/src/main.rs | head -30; echo \"===\"; sed -n '/^fn main/,/^}/p' drave-core/src/main.rs | head -80", "description": "Read main function", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
27:fn main() {
45:    let opt = analyser(&args);
46:    let _ = MODELE.set(args[1].clone());
73:    let path = &args[1];
470:fn analyser(args: &[String]) -> Options {
===
fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
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
elles s'appellent maintenant DRAVE_* (voir
… [3468 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline -6 --format='%h %s' -- drave-core/src/main.rs drave-core/src/model.rs; echo \"---\"; git diff HEAD --stat -- drave-core/", "description": "Check which commits touched src", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
01b7274 Un drapeau inconnu n'est plus avalé en silence
1a4beb3 `--options-actives` : le tableau de bord des réglages qui agissent
1bc0470 Règle R4 : plafond des allocations pilotées par le réseau (256 Mo)
901f28d Relecture adversariale : six défauts corrigés, et des tests qui les auraient attrapés
a9fff24 Deux bugs de protocole trouvés par la relecture, pas par un banc
ae85043 DRVF v3 : −66 % de trace au total, pour +0,074 % de perplexité
---
  ```

### 🤖 Assistant

⏵ Test du tableau de bord en mode perplexité (valeurs avant application ?)

- **bash** `{"command": "printf 'Le chat dort sur le tapis rouge. Il reve encore.\\n' > /tmp/txt4.txt; cd drave-core && timeout 170 ./target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl-texte /tmp/txt4.txt --limit 6 --threads 4 --options-actives --attn-topk 3 --qk-topk 4 --moe-topk 2 --ffn-gain 0:2.0 --act … [245 caractères tronqués]`

  ```
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.

thread 'main' (545252) panicked at src/model.rs:1368:34:
ouverture du GGUF: Os { code: 2, kind: NotFound, message: "No such file or directory" }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
timeout: the monitored command dumped core
  ```

- **bash** `{"command": "cd drave-core && timeout 170 ./target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --infer --ids 1,2,3 --limit 2 --threads 4 --options-actives --attn-topk 3 --ffn-gain 0:2.0 --trace-flux /tmp/trace_inf.drvf --act-thresh 0.1 2>&1 | head -20", "description": "Run inference with dashboard", … [62 caractères tronqués]`

  ```
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.

thread 'main' (545293) panicked at src/model.rs:1368:34:
ouverture du GGUF: Os { code: 2, kind: NotFound, message: "No such file or directory" }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
timeout: the monitored command dumped core
  ```

### 🤖 Assistant

⏵ Correction des chemins et relance des deux modes

- **bash** `{"command": "M=/home/stephane/Data13TB/stephane/GitHub/Qtrinet; timeout 170 $M/drave-core/target/release/drave $M/models/Qwen2.5-0.5B-Q8_0.gguf --ppl-texte /tmp/txt4.txt --limit 6 --threads 4 --options-actives --attn-topk 3 --qk-topk 4 --moe-topk 2 --ffn-gain 0:2.0 --act-thresh 0.1 --act-topk 5 --ab … [217 caractères tronqués]`

  ```
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
[config] cache KV : 32 bits, 0.01 Go pour 256 jetons
[modele] 24 couches chargées en 6.883829865s — listes 0.71 Go , 4 threads
[config] 24 couches, hidden 896 · 
[config] puits appris sur 0/24 couches · n_rot 64 · ffn 4864 · experts 0
[config] rotation : RoPE simple (le modèle ne déclare pas YaRN)
[options] mode perplexité · contexte 256 (défaut) · dense false · keep 1.000
[options] activation : niveaux 127 · seuil 0 · k-WTA 0 · renorm false
[options] top-k : attn 0 · q·k 0 · MoE 0 · par projection [0, 0, 0, 0, 0, 0, 0]
[options] couches 0..24 · flux brut false · trace false · rejeu false
[options] fenêtre 0 · motif 0 · seuil push 0.22 · lot 1 · ffn_gain None · hebb false
[options] cache KV : 32 bits · f16 avant false
[trace] flux enregistré dans /tmp/trace_test.drvf
/tmp/txt4.txt : 6 jetons (tokenizer du modèle), fenêtres de 256
gain FFN : couche 0 x 2
parcimonie imposée : seuil 10.0 % du max, k-WTA k=5
       5 tokens notés — perplexité cumulée 328866.777  (48.0 tok/s)
[trace] 288 listes · 1296 neurones actifs · 0 Mo

==
… [595 caractères tronqués]
  ```

- **bash** `{"command": "M=/home/stephane/Data13TB/stephane/GitHub/Qtrinet; timeout 170 $M/drave-core/target/release/drave $M/models/Qwen2.5-0.5B-Q8_0.gguf --infer --ids 1,2,3 --threads 4 --options-actives --attn-topk 3 --ffn-gain 0:2.0 --trace-flux /tmp/trace_inf.drvf --act-thresh 0.1 2>&1 | head -20", "descri … [117 caractères tronqués]`

  ```
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
[config] cache KV : 32 bits, 0.01 Go pour 512 jetons
[modele] 24 couches chargées en 7.310773588s — listes 0.71 Go , 4 threads
[config] 24 couches, hidden 896 · 
[config] puits appris sur 0/24 couches · n_rot 64 · ffn 4864 · experts 0
[config] rotation : RoPE simple (le modèle ne déclare pas YaRN)
[trace] flux enregistré dans /tmp/trace_inf.drvf
gain FFN : couche 0 × 2
parcimonie imposée : k-WTA garde 0.0 %, seuil 10.0 %
[options] mode inférence · contexte 512 (défaut) · dense false · keep 1.000
[options] activation : niveaux 127 · seuil 0.1 · k-WTA 0 · renorm false
[options] top-k : attn 3 · q·k 0 · MoE 0 · par projection [0, 0, 0, 0, 0, 0, 0]
[options] couches 0..24 · flux brut false · trace true · rejeu false
[options] fenêtre 0 · motif 0 · seuil push 0.22 · lot 1 · ffn_gain Some((0, 2.0)) · hebb false
[options] cache KV : 32 bits · f16 avant false
Qwen2 · 24 couches · hidden 896 · 14 têtes / 2 KV · FFN 4864 · vocab 151936
tokens générés : [220, 220, 220, 264, 264, 220, 220, 220, 220, 264, 220, 220, 264, 220, 220, 220, 
… [151 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Preuve n°1 obtenue (tableau de bord périmé en perplexité) ; test du NaN et du k-WTA en lot

- **bash** `{"command": "M=/home/stephane/Data13TB/stephane/GitHub/Qtrinet; D=$M/drave-core/target/release/drave; MOD=$M/models/Qwen2.5-0.5B-Q8_0.gguf\necho \"=== E2: --limit 1 ===\"; timeout 170 $D $MOD --ppl-texte /tmp/txt4.txt --limit 1 --threads 4 2>&1 | grep -v \"^\\[attention\\]\" | tail -12", "descriptio … [92 caractères tronqués]`

  ```
=== E2: --limit 1 ===
[config] cache KV : 32 bits, 0.01 Go pour 256 jetons
[modele] 24 couches chargées en 6.870416944s — listes 0.71 Go , 4 threads
[config] 24 couches, hidden 896 · 
[config] puits appris sur 0/24 couches · n_rot 64 · ffn 4864 · experts 0
[config] rotation : RoPE simple (le modèle ne déclare pas YaRN)
/tmp/txt4.txt : 1 jetons (tokenizer du modèle), fenêtres de 256
       0 tokens notés — perplexité cumulée NaN  (0.0 tok/s)
aucun jeton noté (il en faut au moins deux : le premier ne prédit rien)
  ```

- **bash** `{"command": "M=/home/stephane/Data13TB/stephane/GitHub/Qtrinet; D=$M/drave-core/target/release/drave; MOD=$M/models/Qwen2.5-0.5B-Q8_0.gguf\nfor arg in \"--lot 1\" \"--lot 1 --act-topk 5\" \"--lot 4 --act-topk 5\" \"--lot 4\"; do\n  echo \"=== dense, $arg ===\"\n  timeout 170 $D $MOD --ppl-texte /tmp … [212 caractères tronqués]`

  ```
=== dense, --lot 1 ===
=== perplexité 410.7398 sur 5 tokens (0 événements, 0.5 s) ===
=== dense, --lot 1 --act-topk 5 ===
=== perplexité 54171.2701 sur 5 tokens (0 événements, 0.5 s) ===
=== dense, --lot 4 --act-topk 5 ===
=== perplexité 41524.7214 sur 5 tokens (0 événements, 0.5 s) ===
=== dense, --lot 4 ===
=== perplexité 410.9033 sur 5 tokens (0 événements, 0.4 s) ===
  ```

### 🤖 Assistant

⏵ Recensement de tous les sites d'écriture/lecture de trace

- **bash** `{"command": "grep -n \"\\.ecrire(\\|fn ecrire\\|fn lire\\|flux_lot(\\|jeton_trace\\|1000\" drave-core/src/model.rs", "description": "List trace write/read sites in model.rs", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
499:    m += 0x1000;                                   // arrondi au bit 13
566:    pub fn ecrire(&mut self, couche: usize, pos: usize, actifs: &[i32], echelle: f32) {
678:    pub fn lire(chemin: &str) -> std::io::Result<Self> {
910:    pub jeton_trace: u64,
1195:        f32::from_bits(b.wrapping_add(0x1000) & !0x1FFF)
1200:    pub fn ecrire(&mut self, kvh: usize, pos: usize, k: &[f32], v: &[f32]) {
1376:            rope_base: g.cfg("rope.freq_base").and_then(|m| m.as_f64()).unwrap_or(10000.0) as f32,
1774:            cache_experts, mla, mla_cache, jeton_trace: 0, trace: None, flux_force: None,
1811:            let k = (((topk as f32) / 1000.0) * x.len() as f32).round() as usize;
2108:    pub fn ecrire_neurones(&self, chemin: &str) -> std::io::Result<usize> {
2211:        let k = ((milliemes as f32 / 1000.0) * head_dim as f32).round() as usize;
2344:        let j0 = self.jeton_trace + 1;
2345:        self.jeton_trace += t as u64;
2434:            Self::flux_lot(&mut self.trace, &mut self.flux_force, j0,
2505:                        kvc.ecrire(hh, pos, &ki[hh * hd..(hh + 1) * hd],
2644:            Self::flux_lot(&mut self.trace, &mut self.flux_force, j0,
2645:                       
… [947 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '655,780p' drave-core/src/model.rs", "description": "Read FluxRelecteur", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
}
}

/// Relit une trace de flux et rend, pour (couche, position), la liste
/// enregistrée. C'est le pendant du `TraceFlux` : ce qu'un nœud distant devrait
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
        let mut f = std::fs::
… [5177 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture d'`envoyer_flux` (en-tête) et de la boucle du nœud moteur

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 130, "offset": 1550}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 45, "offset": 1820}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1550:         // juste après un échappement : sans elle, un corps coupé au mauvais octet
1551:         // paniquait au lieu d'être refusé (attrapé par le test de troncature).
1552:         if lus >= corps.len() { return Err("valeur manquante en fin de corps".into()); }
1553:         val.push(corps[lus] as i8); lus += 1;
1554:     }
1555:     Ok((idx, val))
1556: }
1557: 
1558: /// Envoie un flux et rend le nombre d'octets écrits (en-tête compris) — c'est ce
1559: /// que la phase 3 doit chiffrer : octets par jeton × latence.
1560: fn envoyer_flux(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos: u32,
1561:                 actifs: &[f32], mode: u8, mdl: Option<&model::Model>)
1562:                 -> std::io::Result<(usize, usize)> {
1563:     let act = mdl.map(Act::du_modele).unwrap_or(Act {
1564:         levels: 127.0, thresh: 0.0, topk: 0, renorm: false,
1565:         topk_proj: [0; 7], attn_topk: 0, qk_topk: 0, moe_topk: 0 });
1566:     use std::io::Write;
1567:     let (n, echelle, corps): (usize, f32, Vec<u8>) = if mode == MODE_BLOCS {
1568:         let (idx, v
… [6428 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1820:                         eprintln!("[debug] lot reçu : n={t} pos={} états={} plat={} corps={}",
1821:                                   f.pos, hs.len(), plat.len(), f.octets_corps);
1822:                     }
1823:                     if envoyer_lot(&mut sock, f.debut, f.fin, f.pos, &plat, t, &mdl).is_err() {
1824:                         break;
1825:                     }
1826:                     servis += 1;
1827:                     continue;
1828:                 }
1829:                 mdl.emb_imposee = Some(f.charge.en_dense(hidden));
1830:                 let sortie = mdl.forward(0, f.pos as usize);
1831:                 // La RÉPONSE est encodée comme la demande : un pair qui parle en
1832:                 // listes reçoit des listes, sans second réglage à faire tenir
1833:                 // cohérent entre les deux machines.
1834:                 if envoyer_flux(&mut sock, f.debut, f.fin, f.pos, &sortie, f.mode,
1835:                                 Some(&mdl)).is_err() {
1836:                     break;
1837:                 }
1838:                 servis
… [1244 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Préparation de la preuve R4 : pair factice contre le nœud moteur

- **bash** `{"command": "free -g; cat /proc/sys/vm/overcommit_memory; nproc; python3 -c \"print('ok')\"", "description": "Check memory and overcommit", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
total        used        free      shared  buff/cache   available
Mem:             125          64           0           1          62          60
Swap:             62          17          45
1
40
ok
  ```

- **bash** `{"command": "ls tools/ | head -30; echo ===; sed -n '1,60p' tools/pair_factice.py 2>/dev/null", "description": "Look at tools and pair_factice", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
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
===
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
         3: "lot (t états ×
… [1477 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Écriture du pair factice pour prouver les trous du plafond R4

- **write** `{"file_path": "/tmp/r4_probe.py", "content": "#!/usr/bin/env python3\n\"\"\"Sonde R4 : un pair annonce des tailles énormes SANS dépasser son en-tête.\n\nObjectif : montrer que `verifier_taille` n'est pas appliqué à toutes les\nallocations pilotées par le réseau dans `recevoir_flux` (mode BLOCS).\n\" … [3221 caractères tronqués]`

  ```
<path>/tmp/r4_probe.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Lancement du nœud moteur et injection du corps « échelles » (400 Mo)

- **bash** `{"command": "M=/home/stephane/Data13TB/stephane/GitHub/Qtrinet; D=$M/drave-core/target/release/drave; MOD=$M/models/Qwen2.5-0.5B-Q8_0.gguf\nrm -f /tmp/srv1.log\ntimeout 90 $D $MOD --flux-serveur 5611 --ctx 64 --threads 2 > /tmp/srv1.log 2>&1 &\nSRV=$!\nfor i in $(seq 1 60); do grep -q \"nœud moteur  … [516 caractères tronqués]`

  ```
serveur prêt (pid 546325)
[sonde] connecté ; avant : {'VmPeak': '5844 kB', 'VmSize': '5844 kB', 'VmRSS': '2440 kB'}
[sonde] après envoi (400 Mo d'échelles) : {'VmPeak': '5844 kB', 'VmSize': '5844 kB', 'VmRSS': '2440 kB'}
[sonde] réponse du nœud : mode=2 n=892 n_blocs=28 longueur=1784
[sonde] connexion fermée
--- log serveur ---
[config] rotation : RoPE simple (le modèle ne déclare pas YaRN)
[flux] nœud moteur sur 127.0.0.1:5611 · 896 cachés · 24 couches · contexte 64
[flux] client connecté : 127.0.0.1:28898
[flux] arrêt : failed to fill whole buffer
[flux] 1 flux servis
serveur tué
  ```

### 🤖 Assistant

⏵ Mesure correcte du PID réel : les trois scénarios R4

- **bash** `{"command": "M=/home/stephane/Data13TB/stephane/GitHub/Qtrinet; D=$M/drave-core/target/release/drave; MOD=$M/models/Qwen2.5-0.5B-Q8_0.gguf\nrun() {\n  port=$1; scen=$2\n  rm -f /tmp/srv_$port.log\n  $D $MOD --flux-serveur $port --ctx 64 --threads 2 > /tmp/srv_$port.log 2>&1 &\n  SRV=$!\n  for i in $ … [616 caractères tronqués]`

  ```
=== scénario echelles (pid 547503) ===
[sonde] connecté ; avant : {'VmPeak': '861052 kB', 'VmSize': '795540 kB', 'VmRSS': '566860 kB'}
[sonde] après envoi (400 Mo d'échelles) : {'VmPeak': '1576796 kB', 'VmSize': '1576796 kB', 'VmRSS': '1011704 kB'}
[sonde] réponse du nœud : mode=2 n=892 n_blocs=28 longueur=1784
[sonde] connexion fermée
--- log ---
[flux] client connecté : 127.0.0.1:14676
[flux] arrêt : failed to fill whole buffer
[flux] 1 flux servis
=== scénario paires (pid 550563) ===
[sonde] connecté ; avant : {'VmPeak': '926588 kB', 'VmSize': '795540 kB', 'VmRSS': '566680 kB'}
--- log ---
[flux] client connecté : 127.0.0.1:29868
[flux] arrêt : corps de flux tronqué : 0 paires lues sur 100000000
[flux] 0 flux servis
=== scénario geant (pid 550931) ===
[sonde] connecté ; avant : {'VmPeak': '861052 kB', 'VmSize': '795540 kB', 'VmRSS': '566804 kB'}
[sonde] après envoi (n_blocs=2^32-1) : {'VmPeak': '17572760 kB', 'VmSize': '17572760 kB', 'VmRSS': '566808 kB'}
[sonde] connexion fermée
--- log ---
[flux] client connecté : 127.0.0.1:53634
[flux] arrêt : failed to fill whole buffer
[flux] 0 flux servis
=== fin ===
547501 bash -c M=/home/stephane/Data13TB/stephane/GitHub/Qtrinet; D=$M/dr
… [1168 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Preuve n°2 du trou R4 : allocation `with_capacity(n)` suivie d'un long décodage

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Sonde R4 n°2 : `decoder_paires_blocs` alloue Vec::with_capacity(n) DEUX fois\navant de lire la moindre paire, et `n` vient de l'en-tête réseau (non plafonné).\n\nOn garde le serveur vivant assez longtemps pour lire son VmPeak : on lui donne\nune longueur de … [2880 caractères tronqués]`

  ```
<path>/tmp/r4_probe2.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "M=/home/stephane/Data13TB/stephane/GitHub/Qtrinet; timeout 150 python3 /tmp/r4_probe2.py $M/drave-core/target/release/drave $M/models/Qwen2.5-0.5B-Q8_0.gguf 5620; pgrep -af \"flux-serveur 5620\" || echo \"aucun serveur restant\"", "description": "Prove with_capacity(n) allocation hole", … [83 caractères tronqués]`

  ```
[sonde2] n = 4 000 000 000 paires annoncées ; longueur = 268435456 octets (au plafond)
[sonde2] VmPeak observé : VmSize max 12 Mio · VmRSS max 1 Mio
[sonde2] log serveur :
 , 2 threads
[config] 24 couches, hidden 896 · 
[config] puits appris sur 0/24 couches · n_rot 64 · ffn 4864 · experts 0
[config] rotation : RoPE simple (le modèle ne déclare pas YaRN)
[flux] nœud moteur sur 127.0.0.1:5620 · 896 cachés · 24 couches · contexte 64
[flux] client connecté : 127.0.0.1:42924
[flux] arrêt : corps de flux tronqué : 134217728 paires lues sur 4000000000
[flux] 0 flux servis
554374 bash -c M=/home/stephane/Data13TB/stephane/GitHub/Qtrinet; timeout 150 python3 /tmp/r4_probe2.py $M/drave-core/target/release/drave $M/models/Qwen2.5-0.5B-Q8_0.gguf 5620; pgrep -af "flux-serveur 5620" || echo "aucun serveur restant"
  ```

### 🤖 Assistant

⏵ Correction des unités et nouvelle mesure propre du pic mémoire

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport re\ns = open('/tmp/r4_probe2.py').read()\ns = s.replace('{maxi[\\'VmSize\\']/1048576:.0f} Mio · ', '{maxi[\\'VmSize\\']/1024:.0f} Mio · ')\ns = s.replace('{maxi[\\'VmRSS\\']/1048576:.0f} Mio', '{maxi[\\'VmRSS\\']/1024:.0f} Mio')\nopen('/tmp/r4_probe2 … [388 caractères tronqués]`

  ```
[sonde2] n = 4 000 000 000 paires annoncées ; longueur = 268435456 octets (au plafond)
[sonde2] VmPeak observé : VmSize max 12477 Mio · VmRSS max 1193 Mio
[sonde2] log serveur :
 , 2 threads
[config] 24 couches, hidden 896 · 
[config] puits appris sur 0/24 couches · n_rot 64 · ffn 4864 · experts 0
[config] rotation : RoPE simple (le modèle ne déclare pas YaRN)
[flux] nœud moteur sur 127.0.0.1:5621 · 896 cachés · 24 couches · contexte 64
[flux] client connecté : 127.0.0.1:18780
[flux] arrêt : corps de flux tronqué : 134217728 paires lues sur 4000000000
[flux] 0 flux servis
555634 bash -c cd /tmp && python3 - <<'EOF' import re s = open('/tmp/r4_probe2.py').read() s = s.replace('{maxi[\'VmSize\']/1048576:.0f} Mio · ', '{maxi[\'VmSize\']/1024:.0f} Mio · ') s = s.replace('{maxi[\'VmRSS\']/1048576:.0f} Mio', '{maxi[\'VmRSS\']/1024:.0f} Mio') open('/tmp/r4_probe2.py','w').write(s) EOF M=/home/stephane/Data13TB/stephane/GitHub/Qtrinet; timeout 150 python3 /tmp/r4_probe2.py $M/drave-core/target/release/drave $M/models/Qwen2.5-0.5B-Q8_0.gguf 5621; pgrep -af "flux-serveur 5621" || echo "aucun serveur restant"
  ```

### 🤖 Assistant

⏵ Lancement des 11 tests annoncés en arrière-plan, puis expérience de clés de trace

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && cargo test --release -- --test-threads 2 2>&1 | tail -40", "description": "Run the 11 tests in release", "run_in_background": true, "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
started background job bash-72
  ```

- **bash** `{"command": "sed -n '1,80p' tools/flux_codec.py", "description": "Read flux_codec.py", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
#!/usr/bin/env python3
"""Encodeur/décodeur de RÉFÉRENCE du flux d'activation (format DRVF v1 et v2).

Le format de trace et le contrat d'échange de la phase 3 sont le MÊME format :
une liste d'activation est ce qu'un nœud distant doit recevoir pour continuer le
calcul. Ce fichier est la deuxième implémentation de ce format — la première est
en Rust (`--trace-flux`) — et c'est ce qui permet de dire qu'il est sans
ambiguïté : deux implémentations indépendantes, un aller-retour identique.

Structure :
    en-tête   "DRVF" · u16 version · u32 n_layer · u32 hidden
    liste     u16 couche · u32 position · u32 n_actifs · f32 echelle
              puis n_actifs × ( u32 indice · i16 valeur )          [v1]
              puis n_actifs × ( u8 écart · i16 valeur )            [v2]
                   l'écart de 255 annonce l'indice ABSOLU sur u16
    fin       u16 0xFFFF

v2 : les indices sont écrits par ÉCARTS (la liste est triée). Mesuré sur une trace
réelle de 512 jetons : 132 396 736 octets en v1, **66 370 408** en v2 (−49,87 %),
à contenu identique — le rejeu redonne la même perplexité au chiffre près.

Usage :
    flux_codec.py <trace>            # vérifie l'aller-retour et mesure le débi
… [1970 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de pair_factice.py (mode lot) et du bloc D5 dans run_ppl_reparti

- **bash** `{"command": "sed -n '60,140p' tools/pair_factice.py", "description": "Read pair_factice lot handling", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
# Le corps dépend du MODE : dense et listes i16 font 4 octets par
        # élément, les blocs font 2 octets par actif plus les échelles et les
        # échappements. Un pair factice qui suppose une seule disposition mentirait
        # exactement là où on l'interroge.
        if mode == 3:
            # LOT : `n` est le nombre d'ÉTATS, le corps fait n × dimension × 4.
            # Lire n × 4 (comme avant) laissait le client BLOQUÉ dans read_exact
            # et tuait le pair — c'est pour cela que le mode lot n'avait jamais
            # été confronté à un pair indépendant (relecture adversariale, D4).
            corps = lire_tout(sock, n * dimension * 4)
        elif mode == 2:
            nb = struct.unpack("<I", lire_tout(sock, 4))[0]
            echelles = lire_tout(sock, nb * 4)
            longueur = struct.unpack("<I", lire_tout(sock, 4))[0]
            corps = echelles + lire_tout(sock, longueur)
        else:
            corps = lire_tout(sock, n * 4)
        if magie != MAGIE:
            print(f"[factice] MAGIE INCONNUE {magie:#x}", flush=True)
            break
        vus.append(n)
        if len(vus) <= 3 or len(vus) % 20 == 0:
            print(f"[factice] flux 
… [1669 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1908,1960p' drave-core/src/main.rs", "description": "Read D5 message placement", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
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
    let mut t_local = 0f64;
    let mut t_pair = 0f64;
    let t1 = Instant::now();
    let mut nll = 0f64;
    if lot > 1 {
        // PRÉREMPLISSAGE RÉPARTI : un lot par aller-retour au lieu d'un flux par
        // jeton. C'est ce que la phase 3.4 doit démontrer — le découpage doit
        // coûter la latence d'UN message par lot, pas 
… [1180 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-72 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && cargo test --release -- --test-threads 2 2>&1 | tail -40) finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Résultats des tests annoncés (« 11 tests »)

- **job_output** `{"job_id": "bash-72"}`

  ```
...
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
   --> src/main.rs:623:9
    |
623 |         ids: mut ids, ids_file, prompt, n: n_new, temp, top_p, topk, rep_pen, hist,
    |         ^^^^^^^^^^^^ help: use shorthand field pattern: `mut ids`
    |
    = note: `#[warn(non_shorthand_field_patterns)]` on by default

warning: `drave-core` (bin "drave" test) generated 17 warnings (run `cargo fix --bin "drave" -p drave-core --tests` to apply 8 suggestions)
    Finished `release` profile [optimized] target(s) in 12.10s
     Running unittests src/main.rs (target/release/deps/drave-9a06049b91b56c63)

running 11 tests
test engine::tests_gemm_q4::gemm_q4_egale_matvec ... ok
test list::tests_mxfp4::import_exact ... ok
test list::tests_q4::avx2_egale_scalaire ... ok
test list::tests_q6k::quarts_successifs ... ok
test model::tests_kv::aller_retour_kv ... ok
test tests_flux::entete_et_version_sont_c
… [491 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de `run_infer` : ordre du tableau de bord et flags appliqués

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 110, "offset": 617}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
617: fn run_infer(opt: Options) {
618:     // Lu AVANT la déstructuration, qui consomme `opt`.
619:     let montre_options = opt.options_actives;
620:     // Une seule analyse de la ligne de commande (voir `analyser`) : chaque mode
621:     // ne fait plus que déstructurer ce dont il a besoin.
622:     let Options {
623:         ids: mut ids, ids_file, prompt, n: n_new, temp, top_p, topk, rep_pen, hist,
624:         flux, session, chat, ctx: ctx_opt, threads: threads_opt, abits: abits_opt,
625:         ctx_impose, threads_impose, abits_impose, dense, auto, q4, b6,
626:         keep, attn_window, swa_pattern, sans_fenetre, attn_sinks, attn_topk, qk_topk,
627:         act_thresh, act_topk, act_renorm, topk_proj, moe_topk, patch: patch_file,
628:         hebb_layer, hebb_q, hebb_out, sans_yarn, lot, ffn_gain,
629:         trace_flux, trace_couches, ..
630:     } = opt;
631:     let path = &modele_chemin();
632:     // Défauts du mode INFÉRENCE : 512 jetons, la moitié des cœurs (l'attente
633:     // active de la barrière ne tolère pas la sursouscription), 8 bits.
634:     le
… [5257 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du décodeur de référence puis expérience clés/fenêtres

- **bash** `{"command": "sed -n '80,150p' tools/flux_codec.py; echo \"=== TraceFlux version ===\"; sed -n '530,600p' drave-core/src/model.rs", "description": "Read codec decoder and TraceFlux", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
echelles = []
            for _ in range(n_blocs):
                echelles.append(struct.unpack_from("<e", blob, off)[0])   # f16 natif
                off += 2
        for _ in range(n):
            if version == 3:
                d = blob[off]; off += 1
                if d == 255:
                    i = struct.unpack_from("<H", blob, off)[0]; off += 2
                else:
                    i = prev + d
                prev = i
                q = struct.unpack_from("<b", blob, off)[0]; off += 1
                actifs.append((i, q * echelles[i // 32]))
                continue
            if version == 1:
                i, v = PAIRE_V1.unpack_from(blob, off)
                off += PAIRE_V1.size
            else:
                d = blob[off]
                off += 1
                if d == 255:
                    i = struct.unpack_from("<H", blob, off)[0]
                    off += 2
                else:
                    i = prev + d
                prev = i
                v = struct.unpack_from("<h", blob, off)[0]
                off += 2
            actifs.append((i, v))
        listes.append((couche, pos, echelle, actifs))
    return n_layer, hidden, listes


def 
… [5092 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Expérience : trace écrite à contexte 64 puis à 512, mêmes jetons

- **bash** `{"command": "M=/home/stephane/Data13TB/stephane/GitHub/Qtrinet; D=$M/drave-core/target/release/drave; MOD=$M/models/Qwen2.5-0.5B-Q8_0.gguf\npython3 -c \"\nimport random\nrandom.seed(7)\nmots='le chat dort sur le tapis rouge et reve encore dans la maison calme du village ancien pres de la riviere fro … [500 caractères tronqués]`

  ```
=== ctx 64 ===
[trace] flux enregistré dans /tmp/W64.drvf
/tmp/long.txt : 130 jetons (tokenizer du modèle), fenêtres de 64
[trace] 6240 listes · 5587213 neurones actifs · 17 Mo
=== perplexité 345.5146 sur 127 tokens (0 événements, 61.0 s) ===
=== ctx 512 ===
[trace] flux enregistré dans /tmp/W512.drvf
/tmp/long.txt : 130 jetons (tokenizer du modèle), fenêtres de 512
[trace] 6240 listes · 5588199 neurones actifs · 17 Mo
=== perplexité 168.6228 sur 129 tokens (0 événements, 56.6 s) ===
  ```

### 🤖 Assistant

⏵ Comparaison des clés des deux traces (ctx 64 vs 512)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0, 'tools')\nimport flux_codec as fc\n\ndef charge(p):\n    n_layer, hidden, listes = fc.lire_rust(p)[:3]\n    return {(c, pos) for c, pos, _, _ in listes}, {pos for _, pos, _, _ in list … [798 caractères tronqués]`

  ```
W64  : listes 6240 clés (couche,pos) 6240 pos distincts 130 min 1 max 130
W512 : listes 6240 clés (couche,pos) 6240 pos distincts 130 min 1 max 130
clés identiques : True | diff 0
listes au contenu IDENTIQUE aux mêmes clés : 3138 / 6240
  ```

### 🤖 Assistant

⏵ Inspection du générateur de modèle MLA synthétique

- **bash** `{"command": "wc -l tools/mla_synthetique.py; sed -n '1,50p' tools/mla_synthetique.py; echo ...; grep -n \"def main\\|argparse\\|sys.argv\\|sortie\\|\\.gguf\" tools/mla_synthetique.py | head -20", "description": "Inspect MLA synthetic tool", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet … [2 caractères tronqués]`

  ```
250 tools/mla_synthetique.py
#!/usr/bin/env python3
"""Modèle MLA synthétique + référence numpy — le harnais du chantier 5.

MLA (attention latente, DeepSeek-V2/V3) n'est pas testable en l'état : aucun
modèle MLA en GGUF sur cette machine (le « deepseek-r1-distill » local est un
Qwen dense). Ce script fabrique donc un modèle minuscule dont les poids sont
aléatoires mais les FORMES correctes, l'écrit en GGUF, et calcule une référence
indépendante en numpy — c'est elle que le moteur devra retrouver.

Pourquoi c'est un vrai test : la référence est écrite à partir des formules, pas
du code Rust ; si les deux tombent d'accord sur un modèle dont le cache KV est
LATENT (une seule tête de 128 + 32 valeurs par jeton au lieu de n_head × 192),
alors l'implémentation est validée sur ce qu'elle a de spécifique.

Usage :
    mla_synthetique.py --sortie /tmp/mla_minuscule.gguf --dossier /tmp/mla_ref
"""
import argparse
import json
import os
import struct

import numpy as np

# ---------------------------------------------------------------------------
# Hyperparamètres du modèle jouet : assez petits pour être lisibles, assez
# généraux pour que le découpage qk_nope / qk_rope soit celui de DeepSee
… [1138 caractères tronqués]
  ```

- **bash** `{"command": "ls -la /tmp/*.gguf /tmp/mla* 2>/dev/null; find / -maxdepth 4 -name \"*mla*\" -newer /home/stephane/Data13TB/stephane/GitHub/Qtrinet/Cargo.toml 2>/dev/null | head; ls journal/ 2>/dev/null | head", "description": "Look for existing MLA model artifacts", "workdir": "/home/stephane/Data13TB … [26 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane       2048 29 sep 20:08 /tmp/mla_logits.bin
-rw-r--r--. 1 stephane stephane     480448 29 sep 20:07 /tmp/mla_minuscule.gguf
-rw-r--r--. 1 stephane stephane     480448 29 sep 20:07 /tmp/mla_minuscule.gguf
-rw-r--r--. 1 stephane stephane 3560416288 28 sep 07:35 /tmp/ref-f16.gguf

/tmp/mla_ref:
total 16
drwxr-xr-x.  2 stephane stephane   100 29 sep 20:03 .
drwxrwxrwt. 73 root     root     17040 30 sep 13:23 ..
-rw-r--r--.  1 stephane stephane   178 29 sep 20:07 forme.json
-rw-r--r--.  1 stephane stephane   192 29 sep 20:07 ids.npy
-rw-r--r--.  1 stephane stephane  4224 29 sep 20:07 logits.npy
README.md
sessions
  ```

### 🤖 Assistant

⏵ Preuve du silence MLA et des cas limites du parseur

- **bash** `{"command": "M=/home/stephane/Data13TB/stephane/GitHub/Qtrinet; D=$M/drave-core/target/release/drave\nrm -f /tmp/mla_trace.drvf /tmp/mla_out2.bin\necho \"=== --banc-mla avec --trace-flux et --flux-forcer ===\"\ntimeout 100 $D /tmp/mla_minuscule.gguf --banc-mla /tmp/mla_out2.bin --trace-flux /tmp/mla … [329 caractères tronqués]`

  ```
=== --banc-mla avec --trace-flux et --flux-forcer ===
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
[config] cache KV : 32 bits, 0.00 Go pour 4096 jetons
[modele] 2 couches chargées en 8.820276ms — listes 0.00 Go , 20 threads
[config] 2 couches, hidden 64 · 
[config] puits appris sur 0/2 couches · n_rot 16 · ffn 128 · experts 0
[config] rotation : RoPE simple (le modèle ne déclare pas YaRN)
[config] MLA : 2 couches · q_lora 32 · kv_lora 48 · qk_nope 16 + qk_rope 16 · v 16 · cache latente 64 valeurs par jeton (au lieu de 32)
  position 0 : logits[0..4] = [0.1797, 1.1595, 0.7848, 0.0933]
  position 1 : logits[0..4] = [-0.1069, 0.7312, 0.3862, -0.6178]
  position 2 : logits[0..4] = [0.7365, -0.4164, -0.8823, 0.1396]
  position 3 : logits[0..4] = [0.2173, -0.7516, -0.6551, -0.3991]
  position 4 : logits[0..4] = [0.0505, -1.1887, -1.1274, -0.0691]
  position 5 : logits[0..4] = [0.2406, -0.7627, -1.3326, -0.1739]
  position 6 : logits[0..4] = [0.3863, -0.1013, -0.9722, -0.5898]
  position 7 : logits[0..4] = [0.4916, -0.7828, -1.0495, -0.7294]
fichier de trace créé ? NON
-rw
… [61 caractères tronqués]
  ```

- **bash** `{"command": "M=/home/stephane/Data13TB/stephane/GitHub/Qtrinet; D=$M/drave-core/target/release/drave; MOD=$M/models/Qwen2.5-0.5B-Q8_0.gguf\necho \"=== 1. valeur qui commence par -- (--prompt \\\"--bonjour\\\") ===\"\ntimeout 100 $D $MOD --plan --prompt \"--bonjour\" 2>&1 | grep -iE \"inconnu|prompt\ … [558 caractères tronqués]`

  ```
=== 1. valeur qui commence par -- (--prompt "--bonjour") ===
(rien = pas de faux positif)
=== 2. booléen suivi d'un drapeau à valeur ===
[options] mode inférence · contexte 512 (défaut) · dense true · keep 0.500
=== 3. positionnel sans tirets (keep 0.05) ===
(rien = toujours avalé en silence)
  ```

### 🤖 Assistant

⏵ Vérification d'`en_dense` (mode blocs) : indices non bornés ?

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 60, "offset": 1455}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1455:     Ok(())
1456: }
1457: 
1458: /// Charge utile d'un flux : dense (f32), ou **liste creuse quantifiée**. Le
1459: /// réseau transporte alors exactement ce que le disque écrit déjà — deux octets
1460: /// d'indice, deux octets de valeur, une échelle par liste.
1461: enum ChargeFlux {
1462:     Dense(Vec<f32>),
1463:     Liste { idx: Vec<u16>, val: Vec<i16>, echelle: f32 },
1464:     Blocs { idx: Vec<u16>, val: Vec<i8>, echelles: Vec<f32> },
1465:     /// Lot d'états, aplati (`t × hidden`).
1466:     Lot(Vec<f32>),
1467: }
1468: 
1469: impl ChargeFlux {
1470:     /// Rend le vecteur dense : la déquantification a besoin de la dimension, que
1471:     /// seul le modèle connaît.
1472:     fn en_dense(&self, hidden: usize) -> Vec<f32> {
1473:         match self {
1474:             ChargeFlux::Dense(v) => v.clone(),
1475:             // Un lot n'a pas UN vecteur dense : c'est `plat()` qui le sert, et
1476:             // `forward_lot` qui le consomme. L'appeler ici serait une erreur de
1477:             // programme, pas une donnée invalide — on le dit.
1478:           
… [1882 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test : une trame LISTE avec un indice hors dimension fait-elle tomber le nœud ?

- **bash** `{"command": "cat > /tmp/dos_probe.py <<'EOF'\nimport os, socket, struct, subprocess, sys, time\nMAGIE = 0x44525631\ndef tete(mode, debut, fin, pos, n):\n    b = struct.pack(\"<IBBIIII\", MAGIE, 4, mode, debut, fin, pos, n)\n    b += struct.pack(\"<fff\", 0.0, 127.0, 0.0) + struct.pack(\"<IB\", 0, 0) … [1507 caractères tronqués]`

  ```
[dos] réponse reçue : 0 octets (pas de panique)
[dos] code de sortie : -6
0 Go , 2 threads
[config] 24 couches, hidden 896 · 
[config] puits appris sur 0/24 couches · n_rot 64 · ffn 4864 · experts 0
[config] rotation : RoPE simple (le modèle ne déclare pas YaRN)
[flux] nœud moteur sur 127.0.0.1:5631 · 896 cachés · 24 couches · contexte 64
[flux] client connecté : 127.0.0.1:62730

thread 'main' (567482) panicked at src/main.rs:1482:22:
index out of bounds: the len is 896 but the index is 5000
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
567477 bash -c cat > /tmp/dos_probe.py <<'EOF' import os, socket, struct, subprocess, sys, time MAGIE = 0x44525631 def tete(mode, debut, fin, pos, n):     b = struct.pack("<IBBIIII", MAGIE, 4, mode, debut, fin, pos, n)     b += struct.pack("<fff", 0.0, 127.0, 0.0) + struct.pack("<IB", 0, 0)     b += struct.pack("<7I", *([0]*7)) + struct.pack("<III", 0, 0, 0)     assert len(b) == 79     return b drave, modele, port = sys.argv[1], sys.argv[2], int(sys.argv[3]) logp = f"/tmp/dos_{port}.log" log = open(logp, "w") p = subprocess.Popen([drave, modele, "--flux-serveur", str(port), "--ctx", "64", "--threads", "2"],           
… [965 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification positive D4/D5 (mode lot avec pair factice) et D6 (pair qui ferme)

- **bash** `{"command": "M=/home/stephane/Data13TB/stephane/GitHub/Qtrinet; D=$M/drave-core/target/release/drave; MOD=$M/models/Qwen2.5-0.5B-Q8_0.gguf\nrm -f /tmp/fact.log\ntimeout 60 python3 $M/tools/pair_factice.py 5640 896 > /tmp/fact.log 2>&1 &\nF=$!\nsleep 1\ntimeout 150 $D $MOD --ppl-reparti 127.0.0.1:564 … [366 caractères tronqués]`

  ```
référence locale  : perplexité 261.1724  (1.3 s)
[flux] --flux-liste / --flux-blocs ne s'appliquent PAS aux lots (mode 4 non écrit) : le lot part en f32 dense. À --lot 1, le mode choisi s'applique.
  deux nœuds        : perplexité 151936.0000  (0.5 s)
--- pair factice ---
[factice] écoute sur 127.0.0.1:5640 · je réponds 896 canaux
[factice] client ('127.0.0.1', 38840)
[factice] flux 1 : couches 12..24 pos 0 · version 4 · mode lot (t états × dimension) · n=4 · échelle 0 · niveaux 127 seuil 0 topk 0 renorm 0 · corps 14336 octets
  ```

### 🤖 Assistant

⏵ Vérification positive D6 : pair qui ferme la connexion

- **bash** `{"command": "M=/home/stephane/Data13TB/stephane/GitHub/Qtrinet; D=$M/drave-core/target/release/drave; MOD=$M/models/Qwen2.5-0.5B-Q8_0.gguf\npython3 - <<'EOF' > /tmp/peer_close.log 2>&1 &\nimport socket\ns = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)\ns.bind((\"127.0.0.1 … [406 caractères tronqués]`

  ```
référence locale  : perplexité 994.2334  (2.1 s)

thread 'main' (569094) panicked at src/main.rs:2001:26:
envoi du flux: Os { code: 32, kind: BrokenPipe, message: "Broken pipe" }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
timeout: the monitored command dumped core
code=0
pair fermé
  ```

### 🤖 Assistant

⏵ Vérifications finales : lignes exactes, attribution, absence de délai de test

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; grep -n \"expect(\\\"envoi du\\|expect(\\\"réception\" drave-core/src/main.rs; echo \"=== .expect envoi ===\"; ls -a drave-core/.cargo .cargo 2>/dev/null; grep -rn \"timeout\" tools/*.sh 2>/dev/null | head -5; echo \"=== attribution en … [287 caractères tronqués]`

  ```
1952:                                pos as u32, &plat, t, &mdl).expect("envoi du lot");
2001:                        .expect("envoi du flux");
=== .expect envoi ===
=== attribution en_dense ===
5ea06f9 Phase 3 : échelles par bloc, TCP_NODELAY, et l'écart KV attribué aux clés
=== attribution quantifier topk ===
b97d129 Drave : renommage complet (crate, binaire, variables, documents)
  ```

### 🤖 Assistant

⏵ Nettoyage et vérification de l'état du dépôt

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; git status --short; echo \"--- mes processus drave restants ? ---\"; pgrep -af \"target/release/drave\" | grep -v \"campagne\" || echo \"aucun\"; echo \"--- fichiers du dépôt modifiés par moi ? ---\"; git diff --stat | tail -3", "descr … [58 caractères tronqués]`

  ```
M journal/README.md
--- mes processus drave restants ? ---
517405 timeout 5400 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen_long.txt --ctx 8192 --limit 8192 --dense --threads 16 --lot 512
517408 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen_long.txt --ctx 8192 --limit 8192 --dense --threads 16 --lot 512
555974 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --flux-serveur 46750 --ctx 1024
556007 timeout 1800 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl-reparti 127.0.0.1:46750 --couches-locales 12 --limit 40 --ctx 1024 --ids 198,284,8397,425,10965,465,284,14731,8397,425,10965,465,374,458,6364,4531,1154,12425,323,33496,12089,659,1260,1030,264,8640,569,12,31,39400,3476,389,279,12425,4013,576,8596,304,220,17,15,15,15,659,1096,572,8110,553,264,39400,3476,304,279,1486,6252,2382,5326,553,21315,75923,1154,892,572,10660,304,220,17,15,15,16,518,279,16194,7154,26221,659,1260,1030,264,8640,3476,304,279,12425,4013,20207,3757,1581,291,304,220,17,15,15,17,659,758,220,17,15,15,19,425,10965,465,26120,264,3476,438,330,28417,330,304,279,9234,330,70066,364,82,15106,330,315,279,12425,40
… [9180 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rédaction du rapport adversarial final

Relecture terminée. Aucun fichier du dépôt n'a été modifié (`git status` : seul `journal/README.md`, déjà modifié avant mon arrivée) ; tous mes serveurs sont tués ; la campagne en cours (pids 517408, 555974, 556009) n'a pas été touchée.

# Rapport adversarial — correctifs du 30/09 12h36–13h06

## Défaut 1 — GRAVE : `--options-actives` affiche des valeurs d'AVANT application en perplexité (le défaut exact qu'il devait traquer)

`run_ppl` (main.rs:2948-2950) appelle `options_actives` **avant** `--trace-flux` (2951), `--moe-topk` (2973), `--abits` (2974), `--ffn-gain` (2982), `--act-*` (2986-2991), `--attn-window`/`--sans-fenetre`/`--swa-pattern` (2995-2997), `--topk-*`. Le commit dit avoir appris la leçon (« en inférence, le tableau est placé EN DERNIER ») mais ne l'a pas appliquée au mode perplexité.

```
$ drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl-texte /tmp/txt4.txt --limit 6 --options-actives \
    --attn-topk 3 --qk-topk 4 --moe-topk 2 --ffn-gain 0:2.0 --act-thresh 0.1 --act-topk 5 \
    --abits 4 --act-renorm --attn-window 32 --topk-q 6 --trace-flux /tmp/trace_test.drvf
[options] activation : niveaux 127 · seuil 0 · k-WTA 0 · renorm false      ← 7, 0.1, 5, true
[options] top-k : attn 0 · q·k 0 · MoE 0 · par projection [0,0,0,0,0,0,0] ← 3, 4, 2, [6,…]
[options] … trace false · rejeu false                                    ← trace ACTIVE
[options] fenêtre 0 … · ffn_gain None …                                  ← 32, Some((0,2.0))
[trace] flux enregistré dans /tmp/trace_test.drvf
gain FFN : couche 0 x 2
parcimonie imposée : seuil 10.0 % du max, k-WTA k=5
```
Neuf champs faux. La même commande en `--infer` (tableau en dernier) affiche au contraire `attn 3`, `trace true`, `ffn_gain Some((0, 2.0))`, `seuil 0.1` — c'est bien un défaut d'ORDRE propre au mode perplexité. Correctif : déplacer l'appel après la ligne 3008, comme en inférence.

## Défaut 2 — GRAVE : la règle R4 ne couvre pas les échelles du mode blocs (`n_blocs`)

`recevoir_flux` (main.rs:1715-1719) lit `n_blocs` **dans le corps réseau** puis alloue `vec![0u8; n_blocs * 4]` **puis** un `Vec<f32>` de `n_blocs` échelles (800 Mo au total) sans jamais appeler `verifier_taille`. Contrairement à ce qu'annonce le message du commit (« les trois modes … passent par `verifier_taille` »).

Preuve (pair factice `/tmp/r4_probe.py` contre le vrai `--flux-serveur`, model Qwen, `--ctx 64`) :
```
[sonde] avant  : VmSize 795 540 ko · VmRSS 566 860 ko
[sonde] après envoi (400 Mo d'échelles) : VmSize 1 576 796 ko (+763 Mio) · VmRSS 1 011 704 ko
[sonde] réponse du nœud : mode=2 n=892 n_blocs=28 longueur=1784
--- log --- [flux] 1 flux servis          ← trame ACCEPTÉE, aucun refus
```
Et avec `n_blocs = 0xFFFFFFFF` (une seule trame de 83 octets) :
```
[sonde] après envoi : VmSize 17 572 760 ko (16,8 Gio) · VmRSS inchangé
```
C'est exactement la classe « un `n` hostile fait demander des To au noyau » que le commit prétend fermer : elle est encore ouverte par un champ voisin.

## Défaut 3 — GRAVE : `decoder_paires_blocs` alloue `n` avant toute lecture (mode blocs)

Le plafond porte sur `longueur`, mais le décodeur fait `Vec::with_capacity(n)` **deux fois** avec le `n` de l'en-tête (non borné en mode blocs) : `n = 4e9` ⇒ 8 Gio (u16) + 4 Gio (i8). Mesure (sonde n°2, corps à la longueur maximale autorisée 256 Mio) :
```
[sonde2] n = 4 000 000 000 paires ; longueur = 268 435 456 octets (au plafond)
[sonde2] VmPeak observé : VmSize max 12 477 Mio · VmRSS max 1 193 Mio
[flux] arrêt : corps de flux tronqué : 134217728 paires lues sur 4000000000
```
12,2 Gio de mémoire virtuelle pilotés par l'en-tête, sans un mot de la règle R4. Correctif : `verifier_taille(n * 2, …)` (et `n * 4` en mode liste) avant les `with_capacity`.

## Défaut 4 — GRAVE : une trame forgée fait tomber le nœud moteur (SIGABRT)

`ChargeFlux::en_dense` (main.rs:1482 et 1489) indexe `x[i as usize]` et `echelles[i/32]` sans borne. Une trame LISTE bien formée avec un indice ≥ `hidden` tue le processus (`panic = "abort"`) :
```
thread 'main' panicked at src/main.rs:1482:22:
index out of bounds: the len is 896 but the index is 5000
[dos] code de sortie : -6
```
Le mode blocs a le même défaut en double (indice et bloc). R4 protège la taille, pas les valeurs : le pair hostile reste un déni de service à une trame. (Code d'origine antérieure — `5ea06f9` — mais laissé ouvert par le correctif R4 qui visait ce modèle de menace.)

## Défaut 5 — MOYEN : D6 n'a corrigé que la RÉCEPTION ; le client panique encore à l'envoi

D6 a remplacé `expect("réception …")` par un message propre, mais `envoyer_flux(...).expect("envoi du flux")` (ligne 2001) et `envoi du lot` (1952) restent. Un pair qui ferme (précisément le cas « le nœud a refusé et il sort ») donne :
```
thread 'main' panicked at src/main.rs:2001:26:
envoi du flux: Os { code: 32, kind: BrokenPipe }  → core dumped
```
Le correctif est donc à moitié fait.

## Défaut 6 — MOYEN : D8 incomplet, `--limit 1` affiche toujours `NaN`

```
$ drave … --ppl-texte /tmp/txt4.txt --limit 1
       0 tokens notés — perplexité cumulée NaN  (0.0 tok/s)
aucun jeton noté (il en faut au moins deux : le premier ne prédit rien)
```
Le garde-fou `if n == 0` (main.rs:3193) est placé APRÈS le calcul et l'impression de `ppl` (3151) : la ligne « NaN » que D8 devait supprimer est toujours là.

## Défaut 7 — MOYEN : la détection de drapeau inconnu ne couvre que `--xxx`

Vérifié : pas de faux positif sur `--prompt "--bonjour"` (aucun message), et `--dense --keep 0.5` applique bien `keep 0.500` (le booléen ne mange pas le drapeau suivant). Mais `keep 0.05` et `-keep 0.05` (tirets oubliés — la faute de frappe type) restent **avalés en silence**, et `args[1]` (le chemin du modèle) n'est jamais analysé. `--flux-forcer` est de même ignoré sans mot en `--infer` et `--ppl-reparti`. Le correctif réduit la classe de bugs, il ne la ferme pas.

## Défaut 8 — FAIBLE : `forward_mla` et les modes MLA restent hors du contrat de trace

`forward_mla` (model.rs:2873) n'incrémente jamais `jeton_trace` et n'appelle jamais `flux_lot` ; `run_banc_mla` ne lit ni `trace_flux` ni `flux_forcer`. Preuve sur le modèle MLA synthétique :
```
$ drave /tmp/mla_minuscule.gguf --banc-mla /tmp/mla_out2.bin \
    --trace-flux /tmp/mla_trace.drvf --flux-forcer /tmp/W64.drvf --options-actives
… 8 positions calculées …
fichier de trace créé ? NON          (et aucun message sur les drapeaux ignorés)
```
La revendication D3 (« une seule clé par lot … tous les chemins ») ne couvre donc pas MLA ; la seule famille de clés y serait `0`, contraire à la convention 1-based.

## Ce que j'ai vérifié et qui tient

- **Clés de trace et fenêtres (question 1)** : trace écrite à `--ctx 64` (3 fenêtres) et à `--ctx 512` (1 fenêtre), mêmes 130 jetons → **clés identiques** : 6240 listes, positions 1..130, `diff 0` (décodage par `tools/flux_codec.py`). La clé est bien l'ordinal d'appel `forward`, 1-based, indépendant du découpage ; `forward_lot` (j0 = compteur+1, avancé une fois par lot, deux bases 0/1000) et le raccourci `t == 1` qui délègue à `forward` sont cohérents.
- **Tests** : `cargo test --release` → **11 passés, 0 échec** (4 protocole, 1 plafond, 6 antérieurs), en 0,12 s. Le test de troncature échoue par le bon chemin (garde « valeur manquante en fin de corps » après un échappement, pas par chance). Réserve : le test du plafond ne peut pas *échouer* proprement si le garde-fou disparaît — il se bloquerait dans `read_exact` sur ~358 Go ; il n'existe aucun délai configuré (pas de `.cargo/config.toml`, pas de harnais), contrairement à ce que dit le message du commit.
- **D4/D5/D6 (côté réception)** : avec `tools/pair_factice.py 5640 896` et `--ppl-reparti --lot 4 --flux-liste`, le pair lit bien `4 × 896 × 4 = 14336` octets, le pilote avertit que le mode creux ne s'applique pas aux lots, et D6 explique le refus.
- **Plafond et flux légitimes** : 8192 × 8192 × 4 = 268 435 456 = exactement `PLAFOND_FLUX`, donc accepté (`>` strict). En revanche le pic réel du receveur est ~2× le plafond (corps + `etats`), et un modèle de `hidden > 8192` avec 8192 jetons serait refusé — non mesuré faute de modèle.

## Non vérifié / limites

Pas de test de `--depuis` (clé = ordinal d'appel : le recouvrement d'un jeton entre fenêtres lui fait consommer DEUX clés, donc une trace `--depuis` n'est rejouable qu'à configuration identique — raisonnement sur le code, non exécuté) ; pas de test du mode LISTE côté plafond (couvert par `n × 4`) ; contenus de trace entre `--lot 1` et `--lot 4` non équivalents en valeur (54171 contre 41524 avec `--act-topk 5`) mais je n'ai pas pu attribuer l'écart (réordonnancement numérique ou chemin de code différent) — non retenu comme défaut ; `--banc-kv`, `--gpu-banc`, `--tensors`, `--tokenize`, `--plan` n'ont pas de tableau de bord (constat statique).

---

### Résumé (10 lignes)

1. **8 défauts réels prouvés** par exécution, tous dans le périmètre des correctifs relus.
2. Le plus grave — **`--options-actives` ment en perplexité** : appelé avant les affectations, il affiche 9 champs d'avant (`niveaux 127` au lieu de 7, `k-WTA 0` au lieu de 5, `trace false`, `ffn_gain None`, `attn 0` …) — le défaut exact qu'il devait dénoncer.
3. Second plus grave — **la règle R4 est contournable par deux champs voisins** : `n_blocs` (échelles) → 763 Mio alloués et trame servie, 16,8 Gio de VmSize avec `n_blocs = 0xFFFFFFFF` ; `n` des paires en mode blocs → **12 477 Mio de VmPeak** avec `n = 4e9`, avant toute lecture.
4. Troisième — une trame LISTE forgée **fait tomber le nœud** : `index out of bounds: the len is 896 but the index is 5000`, code de sortie −6.
5. Corrections partielles : D6 (le client panique encore à l'**envoi**, `BrokenPipe`, core dump), D8 (`--limit 1` imprime toujours `perplexité cumulée NaN`), drapeaux inconnus (`keep 0.05` et `-keep` toujours silencieux).
6. `forward_mla` n'écrit ni ne lit aucune trace et n'avance pas `jeton_trace` : `--trace-flux`/`--flux-forcer` sont ignorés en silence en `--banc-mla` (fichier non créé, vérifié).
7. Vérifié et solide : les clés de trace sont **identiques** entre contexte 64 (3 fenêtres) et 512 (1 fenêtre) — 6240 listes, positions 1..130, écart nul ; la question 1 du mandat a une réponse positive.
8. Vérifié et solide : les 11 tests passent (0,12 s) ; le test de troncature refuse par le bon chemin ; le plafond laisse passer 8192 × 8192 (limite exacte).
9. Le test du plafond ne peut pas échouer proprement si le garde-fou disparaît (blocage sur `read_exact` de ~358 Go) : `cargo test` n'a aucun délai, contrairement à ce qu'affirme le message du commit.
10. Non vérifié : `--depuis` en exécution, un lot légitime > 256 Mo sur `hidden > 8192`, l'attribution de l'écart de valeurs de trace entre `--lot 1` et `--lot 4`, et les modes sans tableau de bord (constat statique seulement).

- **send_message** `{"agent_id": "bbd6969f-0f70-42b2-8951-64d1f2f36d2e", "message": "RAPPORT ADVERSARIAL — correctifs 12h36–13h06 (dépôt Qtrinet, binaire release déjà compilé, aucun fichier du dépôt modifié, tous mes serveurs tués, campagne en cours intacte).\n\n8 DÉFAUTS RÉELS PROUVÉS :\n\n1. GRAVE — `--options-active … [4387 caractères tronqués]`

  ```
message delivered to agent bbd6969f-0f70-42b2-8951-64d1f2f36d2e
  ```

### 🤖 Assistant

⏵ Rapport transmis à l'agent parent

Le rapport complet (8 défauts prouvés, vérifications positives, limites) a été rendu ci-dessus et transmis à l'agent parent `bbd6969f`. Aucun fichier du dépôt n'a été touché, aucun processus de la campagne n'a été arrêté, et tous mes serveurs de test ont été tués.

