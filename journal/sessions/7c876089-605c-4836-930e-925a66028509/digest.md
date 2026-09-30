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

