# Session DSH — relecture

- identifiant : `d04ed7a2-0988-4dfd-83c5-644695dc2f8f`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-08 09:18:41
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », drave-core/). LECTURE SEULE STRICTE : ne modifie aucun fichier, ne compile pas, ne lance aucun test ni binaire.

Objectif : inventorier le DÉCOUPAGE EN CLUSTERS et le DÉCOUPAGE PAR PLAGES DE COUCHES (répartition d'un même modèle sur plusieurs unités/processus).

À examiner :
- drave-core/src/clusters.rs (rôle, format, ce qui est chargé/relu, mmap ?, alignement, nombre de clusters, gestion des experts partagés)
- tools/convertir_clusters.py, tools/clusters_moe.py, tools/analyse_union_experts.py, tools/analyse_experts_statique.py, tools/localite_couches.py
- docs/format-clusters.md, reports/rapport-decoupage-moe.md, reports/rapport-decoupage-v41.md, reports/rapport-morcellement-experts.md, reports/rapport-clusters* s'ils existent
- la plage de couches dans le moteur : drave-core/src/main.rs options --couches / --couches-locales / --plage, drave-core/src/model.rs champs couche_debut/couche_fin
- la porte : tools/portes.sh section « Qwen3-30B en clusters » (valeur attendue 799,8557) et tout autre test de clusters dans drave-core/src (mod tests)

Rends un condensé FACTUEL en français, maximum 40 lignes :
1) Tableau : capacité, ce qu'elle fait, fichier source, état (vérifié par une porte / mesuré localement / non testé), chiffre mesuré.
2) Ce que le format clusters change concrètement (taille, nombre de fichiers, tenseurs partagés, jointure) et ce qui reste à faire.
3) La sémantique exacte de --couches a:b et --couches-locales N (bornes, inclusion/exclusion, refus si invalide) avec fichier:ligne.
4) Ce qui est mesuré vs déduit vs supposé.
Donne chemins et numéros de ligne.
Your parent agent id is "482522d1-31f1-43eb-ae9c-a681336404f7". Before you finish, send your result to that agent with send_message({ agent_id: "482522d1-31f1-43eb-ae9c-a681336404f7", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Inventaire lecture seule du découpage clusters et plages de couches

Je commence par repérer les fichiers concernés.

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet", "description": "List repository root"}`

  ```
total 308
drwxr-xr-x. 1 stephane stephane    612  7 oct 18:16 .
drwxr-xr-x. 1 stephane stephane   2374  3 oct 10:09 ..
drwxr-xr-x. 1 stephane stephane     40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane     56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane     96  1 oct 06:58 data
drwxr-xr-x. 1 stephane stephane   1130  5 oct 13:47 docs
drwxr-xr-x. 1 stephane stephane     82 28 sep 11:58 drave-core
drwxr-xr-x. 1 stephane stephane    164  8 oct 09:11 .git
-rw-r--r--. 1 stephane stephane    399 30 sep 10:01 .gitignore
drwxr-xr-x. 1 stephane stephane     34 27 sep 11:39 journal
drwxr-xr-x. 1 stephane stephane     88 25 sep 17:13 models
drwxr-xr-x. 1 stephane stephane    114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane   4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-------. 1 stephane stephane  36518  2 oct 10:21 README.md
drwxr-xr-x. 1 stephane stephane   4256  7 oct 18:22 reports
-rw-------. 1 stephane stephane 120322  5 oct 16:21 REPRISE.md
-rw-------. 1 stephane stephane   8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 stephane stephane  10507 30 sep 08:44 run_clusters.py
-rw-------. 1 stephane stephane  12507 30 sep 08:44 run_cpu.py
-rw-------. 1 stephan
… [708 caractères tronqués]
  ```

- **glob** `{"pattern": "**/*cluster*"}`

  ```
run_clusters.py
run_real_clusters.py
tools/clusters_moe.py
tools/__pycache__/convertir_clusters.cpython-313.pyc
drave-core/src/clusters.rs
docs/format-clusters.md
tools/convertir_clusters.py
  ```

### 🤖 Assistant

⏵ Lecture des sources principales (clusters.rs, docs, python)

- **bash** `{"command": "wc -l /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/clusters.rs /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/convertir … [521 caractères tronqués]`

  ```
506 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/clusters.rs
  5903 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs
  9237 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs
   586 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/convertir_clusters.py
   224 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/clusters_moe.py
   133 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_union_experts.py
   244 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_experts_statique.py
   268 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/localite_couches.py
   189 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-clusters.md
 17290 total
---
clusters.rs
engine.rs
engram.rs
formats.rs
gguf.rs
gpu.rs
kimi_k3.rs
list.rs
main.rs
materiel.rs
model.rs
tokenizer.rs
  ```

- **bash** `{"command": "ls /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/ | grep -iE \"cluster|decoup|morcel|expert|v41\" ", "description": "List relevant reports"}`

  ```
decoupage-v41-digest.txt
rapport-cache-experts-vram.md
rapport-decoupage-moe.md
rapport-decoupage-v41.md
rapport-execution-v41.md
rapport-mla-experts.md
rapport-morcellement-experts.md
rapport-prefill-par-experts.md
rapport-provenance-v41.md
rapport-reutilisation-experts.md
rapport-routage-experts.md
rapport-v41-mhc.md
rapport-vitesse-v41.md
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/clusters.rs"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/clusters.rs</path>
<type>file</type>
<content>
1: //! Format **clusters** : un fichier commun, N fichiers d'experts, un mapping.
2: //!
3: //! Le problème que ce format résout : un MoE range ses 128 experts dans trois
4: //! tenseurs 3D par couche, et un nœud qui n'en sert que 16 en lit quand même
5: //! 128 — soit 8 fois trop. Découpé, le nœud ne lit que son huitième.
6: //!
7: //! Trois pièces, et rien d'autre :
8: //!
9: //! * `commun.gguf` — tout ce qui n'est pas un expert : embeddings, attention,
10: //!   normes, ET le routeur (`ffn_gate_inp`), qui doit rester global puisque
11: //!   c'est lui qui désigne l'expert ;
12: //! * `cluster-XX.gguf` — les seuls `ffn_{gate,up,down}_exps` d'un sous-ensemble
13: //!   d'experts, aux mêmes décalages internes que dans le fichier d'origine ;
14: //! * `mapping.tsv` — pour chaque couche, où est chaque expert global.
15: //!
16: //! Le mapping est un **texte**, délibérément : le moteur est en Rust sans
17: //! dépendance, et un format binaire maison demanderait un lecteur de plus à
18: //! éprouver. Trois colonnes se lisent à l'œil, ce qui n'est pas un luxe quand
19: //!
… [25478 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des options --couches / --plage dans main.rs et model.rs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n -- \"--couches\\|couches_locales\\|couches-locales\\|plage\\|couche_debut\\|couche_fin\\|couches\\b\" main.rs model.rs | head -120", "description": "Grep couches options in main and model"}`

  ```
main.rs:147:    if opt.k3_essai { run_k3_essai(opt.couches); return; }
main.rs:185:    println!("architecture : {arch} · {n_layer} couches · hidden {hidden} · intermédiaire {inter}");
main.rs:423:/// **Sonde de plage** (`--tete-partielle`) : appliquer la tête de sortie à la
main.rs:424:/// fin d'une plage `--couches a:b`. Par défaut une plage partielle rend le flux
main.rs:426:/// jamais le jour : impossible de comparer des LOGITS par plage, et impossible
main.rs:427:/// de vérifier une réduction finale dont les couches suivantes ne tournent pas
main.rs:431:    eprintln!("[plage] `--tete-partielle` : la tête de sortie est appliquée à la fin de la \
main.rs:432:plage — le résultat est celui d'un modèle TRONQUÉ, pas du modèle entier");
main.rs:453:    println!("[options] couches {}..{} · flux brut {} · trace {} · rejeu {}",
main.rs:454:             mdl.couche_debut, mdl.couche_fin, mdl.flux_brut,
main.rs:456:    // `--tete-partielle` CHANGE ce que rend une plage : le dire ici, sinon un
main.rs:460:        println!("[options] plage : la TÊTE DE SORTIE est appliquée à la fin de la plage \
main.rs:553:    /// Phase 3 : nœud MOTEUR qui écoute et applique sa plage de couches.
main.rs:571:
… [9270 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "offset": 660, "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
660:         auto: true, limit: usize::MAX,
661:         matrix: String::from("blk.0.ffn_gate.weight"),
662:         ..Default::default()
663:     };
664:     let cpu = engine::coeurs_physiques();
665:     o.ctx = 512;
666:     o.threads = cpu.max(1);
667:     let suivant = |i: usize| -> &String {
668:         args.get(i + 1).unwrap_or_else(|| panic!("{} attend une valeur", args[i]))
669:     };
670:     let mut i = 2;
671:     while i < args.len() {
672:         // CHAQUE branche rend le nombre d'arguments consommés (1 pour un
673:         // drapeau booléen, 2 pour un drapeau à valeur). Un `i += 2` global
674:         // sautait le drapeau suivant après un booléen : `--dense --threads 8
675:         // --ctx 128` perdait `--threads` ET `--ctx`, donc on mesurait 30 fils
676:         // sur un contexte de 256 en croyant mesurer 8 fils sur 128 — et la
677:         // barrière tournante partait en livelock. C'est la même classe de bug
678:         // que les boucles triplées, en pire : silencieuse.
679:         let pas = match args[i].as_str() {
680:             "--infer" =
… [7418 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"couche_debut\\|couche_fin\" model.rs main.rs engine.rs | head -60", "description": "Grep couche_debut/couche_fin definitions"}`

  ```
model.rs:2553:    pub couche_debut: usize,
model.rs:2554:    pub couche_fin: usize,
model.rs:2559:    /// flux (`couche_fin >= n_layer`) et le pilote le normait une SECONDE fois :
model.rs:4368:            couche_debut: couches.map(|(a, _)| a).unwrap_or(0),
model.rs:4369:            couche_fin: couches.map(|(_, b)| b).unwrap_or(n_layer_total),
model.rs:4751:        for l in self.couche_debut..self.couche_fin {
model.rs:4784:                for l in self.couche_debut..self.couche_fin {
model.rs:5345:        for l in self.couche_debut..self.couche_fin {
model.rs:5740:        if self.flux_brut || (self.couche_fin < self.cfg.n_layer && !self.tete_partielle) {
model.rs:6562:        for l in self.couche_debut..self.couche_fin {
model.rs:6641:        if (self.couche_fin >= self.cfg.n_layer || self.tete_partielle) && !self.flux_brut {
model.rs:6779:        let reprend = self.couche_debut > 0;
model.rs:6787:        assert!(!(self.hc_retarde && self.flux_brut && self.couche_debut > 0 && !recue),
model.rs:6790:avec la copie 0 (faux, et muet)", self.couche_debut);
model.rs:6796:        if self.hc_retarde && self.couche_debut > 0 && !self.flux_brut
model.rs:6800:(convention de sonde, comme au t
… [564 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "offset": 2540, "limit": 40}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "offset": 4340, "limit": 50}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
2540:     /// d'injection des vecteurs d'image (ou de tout autre vecteur), le seul
2541:     /// ajout d'architecture que la vision demande au moteur — `forward` partait
2542:     /// toujours de `token_embd`.
2543:     pub emb_imposee: Option<Vec<f32>>,
2544:     /// États imposés pour un LOT entier (`forward_lot`) : `t × hidden`, aplati.
2545:     ///
2546:     /// C'est le pendant de `emb_imposee` pour le préremplissage réparti : un nœud
2547:     /// qui reçoit N états d'un coup — au lieu des N identifiants de jetons —
2548:     /// reprend le calcul à sa première couche sans repasser par les embeddings.
2549:     /// Sans ce champ, le transport devait payer un aller-retour PAR JETON.
2550:     pub emb_imposee_lot: Option<Vec<f32>>,
2551:     /// Première et dernière couche PORTÉES par ce modèle (exclue). Un nœud
2552:     /// distant ne charge que sa plage : c'est le découpage de la phase 3.
2553:     pub couche_debut: usize,
2554:     pub couche_fin: usize,
2555:     /// Nœud **intermédiaire** du transport : sa plage peut aller jusqu'à la
2556:     /// dernière cou
… [1756 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
4340:             act_topk_proj: [0; 7], attn_topk: 0, attn_events: 0, qk_topk: 0,
4341:             moe_topk: 0,
4342:             profil_neurones: None,
4343:             profil_experts: None,
4344:             // Trace de routage des experts : c'est la matière première du
4345:             // découpage en clusters (quels experts sont allumés ENSEMBLE). Le
4346:             // fichier est créé (tronqué) au chargement, tamponné, et fermé avec
4347:             // le modèle — une exécution = une trace.
4348:             trace_experts: std::env::var("DRAVE_TRACE_EXPERTS").ok().and_then(|c| {
4349:                 std::fs::File::create(&c).ok().map(|f| {
4350:                     println!("[moe] trace de routage des experts → {c}");
4351:                     std::io::BufWriter::new(f)
4352:                 })
4353:             }),
4354:             profil_jetons: 0,
4355:             attn_window: fenetre,
4356:             swa_pattern,
4357:             attn_sinks: if fenetre > 0 { 0 } else { 4 },
4358:             seuil_push: 0.22,
4359:             stop_id: None, stop_id
… [1817 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des validations de plage (bornes, refus)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"couche_debut\\s*>\\|couche_fin\\s*>\\|couche_debut\\s*<\\|plage invalide\\|couches_locales\\s*[<>=]\" model.rs main.rs | head -40", "description": "Grep range validation checks"}`

  ```
model.rs:2559:    /// flux (`couche_fin >= n_layer`) et le pilote le normait une SECONDE fois :
model.rs:6641:        if (self.couche_fin >= self.cfg.n_layer || self.tete_partielle) && !self.flux_brut {
model.rs:6779:        let reprend = self.couche_debut > 0;
model.rs:6787:        assert!(!(self.hc_retarde && self.flux_brut && self.couche_debut > 0 && !recue),
model.rs:6796:        if self.hc_retarde && self.couche_debut > 0 && !self.flux_brut
main.rs:705:            "--couches-locales" => { o.couches_locales = suivant(i).parse().unwrap(); 2 }
main.rs:3345:    let couches_locales = if opt.couches_locales > 0 { opt.couches_locales } else { 12 };
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '2120,2150p' main.rs; echo \"=== 3340-3470 ===\"; sed -n '3340,3470p' main.rs", "description": "Read plage/pilote sections"}`

  ```
}
                    return;
                }
                // ---- PLAGE ET RELAIS : c'est ici qu'un processus devient UN NŒUD.
                //
                // `--couches a:b` borne la plage. Le relais transporte ce que le
                // nœud suivant ne PEUT PAS recalculer : le flux résiduel et la
                // pile des entrées de banque. Sans la pile, `res_mix` mélangerait
                // un plateau incomplet et le résultat serait faux SANS ERREUR —
                // l'écueil exact de la `pre` reçue de V4.1.
                let (debut, fin) = plage.unwrap_or((0, n));
                if debut >= fin || fin > n {
                    println!("  plage {debut}:{fin} invalide pour {n} couche(s)");
                    return;
                }
                let entree = match std::env::var("DRAVE_K3_RELAIS_ENTREE") {
                    Ok(c) if !c.is_empty() => match kimi_k3::Relais::lire(&c) {
                        Ok(r) => Some(r),
                        Err(e) => { println!("  relais d'entrée illisible ({c}) : {e}"); return; }
                    },
                    _ => None,
                };
                println!("  plage : couches {debut}..{} 
… [7467 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du format documenté et de la porte clusters

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-clusters.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-clusters.md</path>
<type>file</type>
<content>
1: # Format — le modèle éclaté en clusters (un fichier par cluster)
2: 
3: **En une ligne** : un GGUF est converti en `commun.gguf` + `cluster-XX.gguf`, un
4: fichier **GGUF autonome par cluster d'experts**, avec un manifeste qui porte la
5: correspondance ; un nœud n'ouvre que ce qu'il sert — mesuré **3,20 Go au lieu de
6: 18,56** et **625 ms au lieu de 3,9 s** sur Qwen3-30B-A3B.
7: 
8: **Et c'est le mécanisme de placement** : ces grappes sont les neurones qu'on
9: répartit entre nœuds, et le flux d'activation se route de l'une à l'autre
10: (`docs/vision.md`, axes 2-3). Le découpage n'est donc pas qu'un rangement de
11: fichiers : c'est la carte des grappes entre composants et machines.
12: 
13: Outil : [`tools/convertir_clusters.py`](../tools/convertir_clusters.py).
14: 
15: ## Le problème
16: 
17: Un MoE publié en GGUF met **tous** les experts d'une couche dans un seul tenseur :
18: 
19: ```
20: blk.0.ffn_gate_exps.weight   [128, 768, 2048]   Q4_K
21: blk.0.ffn_up_exps.weight     [128, 768, 2048]   Q4_K
22: blk.0.ffn_down_exps.weight   [128, 2048, 768]   Q6_K
23: ```
… [9180 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -i \"cluster\" tools/portes.sh | head -60", "description": "Grep clusters in portes.sh"}`

  ```
55:# 3. Modèle en clusters, mêmes jetons que l'original.
56:A=/home/stephane/FastNVMe/artefacts/modeles-optimises/qwen3-30b-8clusters-v2
60:    compare "Qwen3-30B en clusters (origine : 799,8557)" "799.8557" "$v"
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,110p' tools/portes.sh", "description": "Read portes.sh head"}`

  ```
#!/bin/bash
# Les portes du dépôt, en une commande.
#
# Un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien :
# chaque porte est comparée à la valeur ATTENDUE, et le script sort en erreur si
# l'une diverge. Les valeurs sont celles publiées dans les rapports.
#
#   tools/portes.sh            toutes les portes
#   tools/portes.sh rapide     sans gpt-oss (le seul qui prenne ~20 min)

set -u
cd "$(dirname "$0")/.."
D=./drave-core/target/release/drave
RAPIDE=${1:-}
ECHEC=0

[ -x "$D" ] || { echo "compiler d'abord : (cd drave-core && cargo build --release)"; exit 2; }

compare() {  # nom, attendu, obtenu
    if [ "$2" = "$3" ]; then
        printf "  %-42s %s  ✅\n" "$1" "$3"
    else
        printf "  %-42s %s  ❌ (attendu %s)\n" "$1" "${3:-—}" "$2"
        ECHEC=1
    fi
}

# Attention : le moteur affiche AUSSI une perplexité cumulée par fenêtre, avant
# le total. Prendre la première occurrence du motif donnait 17,431 (fenêtre 1) au
# lieu de 19,3885 (total) — un instrument faux qui accuse le code.
valeur() { grep -oE "=== perplexité [0-9]+\.[0-9]+" | grep -oE "[0-9]+\.[0-9]+" | head -1; }

echo "=== Portes ==="

# 1. Tests unitaires. Le seuil (48) protège le NOMBR
… [4114 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Parallélisation : rapports délégués, outils Python lus localement

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && wc -l rapport-decoupage-moe.md rapport-decoupage-v41.md rapport-morcellement-experts.md decoupage-v41-digest.txt 2>&1; ls | wc -l", "description": "Check report sizes"}`

  ```
117 rapport-decoupage-moe.md
  180 rapport-decoupage-v41.md
   86 rapport-morcellement-experts.md
  311 decoupage-v41-digest.txt
  694 total
86
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -rn \"mod tests\" *.rs | head; echo \"=== clusters-related tests ===\"; grep -rn \"clusters\\|DRAVE_CLUSTERS\\|commun.gguf\" --include=*.rs . | grep -v \"^./clusters.rs\" | head -30", "description": "Find cluster- … [31 caractères tronqués]`

  ```
clusters.rs:300:mod tests {
engine.rs:943:mod tests_gemm {
engine.rs:990:mod tests_gemm_q4 {
engram.rs:292:mod tests {
formats.rs:2883:mod tests {
gguf.rs:1891:pub(crate) mod tests {
list.rs:1397:mod tests_q4 {
list.rs:1426:mod tests_mxfp4 {
list.rs:1497:mod tests_q6k {
list.rs:1537:mod tests_grille {
=== clusters-related tests ===
./gguf.rs:248:    /// `-00001-of-00003`, ou notre format en clusters) est une seule liste de
./gguf.rs:454:    /// GGUF découpé (`…-00001-of-00003.gguf`), soit notre format en clusters
./gguf.rs:455:    /// (`commun.gguf` + `cluster-XX.gguf`).
./gguf.rs:460:    ///   GGUF découpé les duplique sur chaque shard, un modèle en clusters ne
./gguf.rs:461:    ///   les met que dans `commun.gguf`, et le second shard de
./gguf.rs:476:    /// Sert au format en clusters : chaque fichier de cluster porte les MÊMES
./gguf.rs:627:    /// Un **dossier** qui contient `commun.gguf` est un modèle au format
./gguf.rs:628:    /// clusters : il s'ouvre comme les autres, sans option supplémentaire. Le
./gguf.rs:633:            if !p.join("commun.gguf").is_file() {
./gguf.rs:635:                    "{} est un dossier mais ne contient pas commun.gguf", p.display())));
./gguf.rs
… [1881 caractères tronqués]
  ```

- **subagent** `{"description": "Digest cluster reports", "prompt": "Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet. LECTURE SEULE STRICTE : ne modifie AUCUN fichier, ne compile pas, ne lance aucun test ni binaire. Utilise uniquement les outils de lecture (read, grep, glob, bash pour wc … [1240 caractères tronqués]`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/convertir_clusters.py", "limit": 300}`

  ```
started subagent a9e308b7-5d50-4bb3-8e31-4c8e6f261a6d
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/convertir_clusters.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Convertisseur GGUF → « modèle éclaté en clusters », un fichier par cluster.
3: 
4: **Pourquoi.** Notre mode d'opération ne lit que les experts qu'un jeton allume, et
5: les modèles MoE publient leurs experts dans UN tenseur par couche
6: (`blk.N.ffn_gate_exps.weight [n_experts, …]`). Un nœud qui n'héberge que 16 experts
7: sur 128 lit donc un fichier de 18 Go pour en utiliser un huitième. Ici, chaque
8: cluster devient un **fichier GGUF autonome** : on l'ouvre seul, en mmap, et on ne
9: lit que sa tranche.
10: 
11: **Ce que le convertisseur NE fait pas** : il ne requantifie rien. Les octets des
12: poids sont copiés tels quels (les blocs de quantification sont alignés sur l'axe
13: des experts, donc une tranche d'expert est une plage d'octets exacte). Aucune perte,
14: aucune conversion, aucun choix de format de rechange.
15: 
16: **Sortie** (dans un dossier) :
17: 
18:     commun.gguf          ce qui n'est pas un expert : embeddings, sortie, attention,
19:                          normes, routeur de chaque couche
20:     cluster-00.gg
… [11775 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/convertir_clusters.py", "offset": 300, "limit": 290}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/convertir_clusters.py</path>
<type>file</type>
<content>
300: def parcourir_kv(kv_brut):
301:     """→ (nombre de paires, architecture) en reparcourant le bloc brut."""
302:     class Faux:
303:         def __init__(self, b):
304:             self.b, self.p = b, 0
305: 
306:         def lire(self, n):
307:             v = self.b[self.p:self.p + n]
308:             self.p += n
309:             return v
310: 
311:         def u32(self):
312:             return struct.unpack("<I", self.lire(4))[0]
313: 
314:         def u64(self):
315:             return struct.unpack("<Q", self.lire(8))[0]
316: 
317:         def chaine(self):
318:             return self.lire(self.u64()).decode("utf-8", errors="replace")
319:     f = Faux(kv_brut)
320:     n, arch = 0, None
321:     while f.p < len(kv_brut):
322:         cle = f.chaine()
323:         t = f.u32()
324:         if cle == "general.architecture" and t == 8:
325:             arch = f.chaine()
326:         else:
327:             sauter_valeur(f, t)
328:         n += 1
329:     return n, arch
330: 
331: 
332: def ordre_experts(trace, couche, ne):
333:     """Ordre des experts par fr
… [14088 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des quatre outils d'analyse Python

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/clusters_moe.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/localite_couches.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/clusters_moe.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Découpage des MoE en clusters — à partir d'une trace de routage réelle.
3: 
4: Le moteur écrit une ligne par (couche, jeton) avec les experts retenus :
5: `DRAVE_TRACE_EXPERTS=/tmp/trace.txt drave <modele> --ppl <ids> --limit N --lot L`
6: 
7: Ce script répond à la question de placement : **quels experts s'allument
8: ENSEMBLE ?** Les compteurs d'usage disent quels experts sont chauds ; ils ne
9: disent pas lesquels sont chauds en même temps, et c'est pourtant ce qui décide si
10: un jeton peut être servi par UN nœud ou doit en interroger quatre.
11: 
12: Trois mesures, et une comparaison qui les rend honnêtes :
13: 
14: * **couverture** : part des k experts d'un jeton qui tiennent dans son meilleur
15:   cluster (1,0 = un seul nœud suffit) ;
16: * **ventilation** (fan-out) : nombre de clusters nécessaires pour couvrir 90 % des
17:   experts d'un jeton (1,0 = le meilleur cas possible) ;
18: * **équilibre** : taille des clusters (un cluster géant ne compte pas comme un
19:   bon découpage) ;
20: * **témoin** : les mêmes mesures avec des clust
… [9607 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/localite_couches.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """localite_couches.py — une couche doit-elle quelque chose au CONTEXTE, ou au jeton ?
3: 
4: LA QUESTION, ET ELLE DÉCIDE D'UNE ARCHITECTURE. Notre pont est RÉCURRENT :
5: `s_t = (1−a)·s_{t−1} + a·tanh(P·s_{t−1} + B·e_t)`. La récurrence n'a de sens que si la
6: cible dépend du contexte. Si la couche 8 d'un transformer n'était, à chaque position,
7: qu'une fonction du jeton courant, alors un simple réseau par position suffirait — et une
8: bonne partie de la machinerie du pont serait de la complexité inutile.
9: 
10: CE QUI EST MESURÉ. À chaque position p, on cherche à prédire `h_c(p)` — la couche c du
11: professeur — à partir d'une FENÊTRE de la couche 0 : `h_0(p), h_0(p−1), …, h_0(p−k)`.
12: Régression ridge, forme fermée. On lit :
13: 
14:     R²(0)        ce qu'explique le JETON COURANT seul
15:     R²(k)        ce qu'explique une fenêtre de k+1 jetons
16:     gain(k)      R²(k) − R²(0) : ce que le CONTEXTE ajoute
17: 
18: RÉSERVE, ET ELLE EST RÉELLE. C'est une mesure LINÉAIRE. Un professeur peut faire dépendre
19: `h_c(p)` du contexte 
… [12473 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_union_experts.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_experts_statique.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_union_experts.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """analyse_union_experts.py — ce que le REGROUPEMENT des jetons par expert
3: économise, calculé sur une trace de routage réelle.
4: 
5: Le fait : en préremplissage par lots (`--lot N`), les jetons d'un même lot qui
6: ont choisi le même expert partagent UNE lecture de sa matrice (`forward_lot`
7: appelle un seul `gemm_dense_q4` par expert non vide). Jeton par jetons, la même
8: matrice est relue autant de fois qu'elle a d'ayants droit.
9: 
10: Ce que le script mesure, par couche et globalement :
11: 
12:   - les **lectures d'experts** en mode jeton (`N_jetons × k`) et en mode groupe
13:     (`Σ_blocs |union des experts du bloc|`) — c'est le nombre exact de matrices
14:     lues, pas une estimation ;
15:   - le **rapport** entre les deux, en fonction de la taille de bloc N ;
16:   - les **octets** correspondants, pour une taille d'expert donnée ;
17:   - la **borne** : quand N → ∞ le mode groupe lit chaque expert une fois par
18:     couche, donc le coût par jeton tombe à `n_experts/N` experts-équivalents.
19:     Un modèle dont les ex
… [4515 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_experts_statique.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Analyse STATIQUE des experts d'un MoE : que portent les poids eux-mêmes.
3: 
4: Les traces de routage disent quels experts sont *appelés*. Ce script regarde ce
5: qu'ils *sont* : deux experts aux poids presque identiques sont redondants, et
6: l'un des deux peut disparaître — c'est une économie d'empreinte qu'aucune trace
7: ne peut révéler.
8: 
9:     python3 tools/analyse_experts_statique.py <modele.gguf> --couches 0,12,24,36
10: 
11: Trois mesures, et ce que chacune cherche :
12: 
13: * **similarité entre experts** (intra-couche) — des experts jumeaux ? Si deux
14:   experts d'une même couche font la même chose, n'en stocker qu'un divise leur
15:   empreinte par deux ;
16: * **profil de SOURCES** — la norme de chaque colonne d'entrée. Deux experts qui
17:   écoutent les mêmes dimensions d'entrée ont la même source ;
18: * **profil de DESTINATIONS** — la norme de chaque ligne de sortie. Deux experts
19:   qui écrivent dans les mêmes dimensions ont la même destination.
20: 
21: Un couple d'experts dont les sources ET les destina
… [11093 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des bornes/refus et de l'existence de --plage

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -rn -- '\"--plage\"' *.rs; echo \"exit=$?\"; echo \"=== invalide messages ===\"; grep -rn \"invalide\" *.rs | head -30", "description": "Check --plage flag and invalide messages"}`

  ```
exit=1
=== invalide messages ===
gpu.rs:745:            eprintln!("[topk] décalage {decalage} invalide (0, 8, 16 ou 24)");
main.rs:2132:                    println!("  plage {debut}:{fin} invalide pour {n} couche(s)");
main.rs:2655:            // programme, pas une donnée invalide — on le dit.
main.rs:3177:        Some((h, p)) => (h.to_string(), p.parse().expect("port invalide")),
main.rs:3178:        None => ("127.0.0.1".to_string(), adresse.parse().expect("port invalide")),
main.rs:3211:                    println!("[flux] flux refusé : plage de couches {}..{} invalide pour {} \
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '140,160p' main.rs; echo \"=== 860-880 ===\"; sed -n '860,880p' main.rs; echo \"=== 5110,5140 ===\"; sed -n '5110,5140p' main.rs", "description": "Read couches call sites in main.rs"}`

  ```
if let Some(adresse) = opt.flux_serveur.clone() { run_serveur_flux(opt, &adresse); return; }
    if let Some(pair) = opt.ppl_reparti.clone() { run_ppl_reparti(opt, &pair); return; }
    if opt.tensors { run_tensors(); return; }
    if let Some(f) = opt.banc_mla.clone() { run_banc_mla(opt, &f); return; }
    if opt.banc_kv > 0 { run_banc_kv(opt); return; }
    if opt.banc_topk > 0 { run_banc_topk(opt); return; }
    if opt.gpu_banc { run_gpu_banc(opt); return; }
    if opt.k3_essai { run_k3_essai(opt.couches); return; }
    if opt.plan { run_plan(opt); return; }
    if opt.tokenize { run_tokenize(opt); return; }
    if opt.ppl { run_ppl(opt); return; }
    if opt.infer { run_infer(opt); return; }
    let path = &args[1];
    let mut matrix = "blk.0.ffn_gate.weight".to_string();
    // Par défaut : les cœurs PHYSIQUES, pas les threads logiques. Mesuré au banc
    // sur 20 cœurs / 40 threads : 18 threads = 22,6 Go/s, 20 = 18,7 (bruité),
    // 15 = 19,9, 10 = 14,3. Le `× 3/4` d'avant visait à laisser un quart des CPU
    // au système, mais il comptait les threads logiques : il donnait 30 fils sur
    // 20 cœurs. Prendre les 20 cœurs laisse de toute façon leurs 20 hyperthreads
    /
… [2905 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"fn load_partiel\\|fn load(\\|couches: Option\\|couches:Option\\|fn new\\|pub fn load\" model.rs | head -20", "description": "Locate load functions in model.rs"}`

  ```
1483:    fn load(g: &Gguf, name: &str, bias: Option<&str>, dense: bool, auto: bool, keep: f32,
2584:    pub dump_couches: Option<String>,
2690:    pub fn load(path: &str) -> std::io::Result<Patch> {
2819:    pub fn new(layer: usize, n_out: usize, n_in: usize, eta: f32, clamp: f32) -> Self {
2881:    pub fn new(layer: usize, n_out: usize, n_in: usize, quantile: f32) -> Self {
2960:    pub fn new(bits: u32, n_kv: usize, ctx: usize, hd: usize) -> Self {
3296:    pub fn load(path: &str, ctx: usize, n_threads: usize, dense: bool, keep: f32,
3302:    pub fn load_partiel(path: &str, ctx: usize, n_threads: usize, dense: bool, keep: f32,
3303:                        auto: bool, q4: u8, b6: u8, couches: Option<(usize, usize)>) -> Model {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '3195,3250p' main.rs", "description": "Read flux server validation"}`

  ```
// une petite écriture en attendant l'acquittement de la précédente, et l'ACK
    // différé du pair la retarde encore. Mesuré sur localhost, 12 couches
    // distantes : **97,6 ms** d'attente contre 15,6 ms de calcul local — six fois
    // le calcul, payés par la seule latence du protocole.
    sock.set_nodelay(true).expect("TCP_NODELAY");
    println!("[flux] client connecté : {pair}");
    let mut servis = 0u64;
    loop {
        match recevoir_flux(&mut sock, hidden, hc_local) {
            Ok(f) => {
                // Un en-tête FORGÉ ne doit pas tuer le nœud : `debut`, `fin` et
                // `pos` venaient du réseau sans contrôle, et une trame de 83
                // octets suffisait à faire tomber le moteur (assert sur `pos`,
                // index hors `layers`, dimension fausse — relecture adversariale).
                let (n_layer_local, ctx_local) = (mdl.cfg.n_layer, mdl.ctx);
                if f.fin as usize > n_layer_local || f.debut >= f.fin {
                    println!("[flux] flux refusé : plage de couches {}..{} invalide pour {} \
couches — le nœud continue", f.debut, f.fin, n_layer_local);
                    continue;
                }
           
… [2320 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 60, "offset": 3290}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
3290:     /// `couches` : exécution **bornée** `[a, b)` — le harnais qui permet
3291:     /// d'exécuter et de COMPARER les couches qui n'ont pas besoin de ce qui
3292:     /// manque encore (les couches 0 et 1 de V4-Flash n'ont pas d'attention
3293:     /// compressée). Le reste du modèle reste déclaré non implémenté : on ne
3294:     /// lève pas un manque, on constate qu'il ne s'applique pas à ce qu'on
3295:     /// exécute — et on le dit.
3296:     pub fn load(path: &str, ctx: usize, n_threads: usize, dense: bool, keep: f32,
3297:                 auto: bool, q4: u8, b6: u8) -> Model {
3298:         Self::load_partiel(path, ctx, n_threads, dense, keep, auto, q4, b6, None)
3299:     }
3300: 
3301:     #[allow(clippy::too_many_arguments)]
3302:     pub fn load_partiel(path: &str, ctx: usize, n_threads: usize, dense: bool, keep: f32,
3303:                         auto: bool, q4: u8, b6: u8, couches: Option<(usize, usize)>) -> Model {
3304:         let t0 = Instant::now();
3305:         let g = Gguf::open_auto(path).expect("ouverture du GGUF");
3306:         let arch = g.
… [3364 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '6630,6650p' model.rs; echo \"=== 7735,7760 ===\"; sed -n '7735,7760p' model.rs; echo \"=== 612,660 ===\"; sed -n '612,665p' model.rs", "description": "Read couche_fin usage and charger_moe"}`

  ```
let mut g_t = vec![0f32; m.ffn];
            let mut u_t = vec![0f32; m.ffn];
            matvec_f32_fils(&m.gate, &hn, h, m.ffn, &mut g_t, n_fils);
            matvec_f32_fils(&m.up, &hn, h, m.ffn, &mut u_t, n_fils);
            let mut act = vec![0f32; m.ffn];
            Self::activation(&mut g_t, &u_t, m.ffn, false, 0.0);
            for i in 0..m.ffn { act[i] = g_t[i]; }
            let mut d = vec![0f32; h];
            matvec_f32_fils(&m.down, &act, m.ffn, h, &mut d, n_fils);
            for i in 0..h { x[i] += d[i]; }
        }
        if (self.couche_fin >= self.cfg.n_layer || self.tete_partielle) && !self.flux_brut {
            Self::rmsnorm(&x, &self.out_norm, eps, &mut hn);
            hn
        } else {
            x
        }
    }

    /// Logits d'un état caché avec une tête **liée en f32** (le harnais MLA n'a
    /// pas de blocs Q8_0 : `logits` ne s'applique pas).
=== 7735,7760 ===
|ffn| {:.4e} (dense)", n2.sqrt(), na.sqrt(), nd.sqrt());
            }
            self.prof[3] += tf.elapsed().as_secs_f64();
        }
        // **Coupure de grappe** : on rend le flux résiduel BRUT, tel qu'il est —
        // et pour un modèle à hyper-connexions, cela veut dire le
… [4599 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des bornes couches-locales et de l'accès aux couches

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"couches_locales\" main.rs; echo \"=== model.rs couches param (load_partiel) ===\"; awk 'NR>=3303 && NR<=4390 && /couches/ {print NR\": \"$0}' model.rs", "description": "Trace couches_locales and couches param … [2 caractères tronqués]`

  ```
572:    couches_locales: usize,
705:            "--couches-locales" => { o.couches_locales = suivant(i).parse().unwrap(); 2 }
3297:                // n'est émise par personne (le pilote envoie `couches_locales ≥ 1`),
3345:    let couches_locales = if opt.couches_locales > 0 { opt.couches_locales } else { 12 };
3397:    println!("[flux] pilote : {couches_locales} couches en local, {} chez le pair, {} jetons",
3398:             n_layer - couches_locales, ids.len());
3430:    mdl.couche_fin = couches_locales;
3457:                envoyer_lot_listes(&mut sock, couches_locales as u32, n_layer as u32,
3460:                envoyer_lot(&mut sock, couches_locales as u32, n_layer as u32,
3549:        let (o, a) = envoyer_flux(&mut sock, couches_locales as u32, n_layer as u32,
=== model.rs couches param (load_partiel) ===
3303:                         auto: bool, q4: u8, b6: u8, couches: Option<(usize, usize)>) -> Model {
3311:         // ressorti ici pour les couches compressées.
3485:         if let (Some((a, b)), true) = (couches, !manques.is_empty()) {
3491:             let ratios = g.couches_ratios();
3500:                     println!("[partiel] couches {a}..{b} : le compresseur (HCA ra
… [3471 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '4745,4760p' model.rs; echo \"=== 6890,6910 ===\"; sed -n '6890,6910p' model.rs", "description": "Read forward layer loops"}`

  ```
out.push_str(&format!("  neurones tirés {nom} du temps : {:>5.2} %\n",
                                  100.0 * chauds as f64 / n as f64));
        }
        // Dispersion entre couches : une localité qui ne tient que sur quelques
        // couches ne se place pas de la même façon.
        let mut par_couche: Vec<(f64, f64)> = Vec::new();
        for l in self.couche_debut..self.couche_fin {
            let t = &tirs[l * largeur..(l + 1) * largeur];
            let p = &poids[l * largeur..(l + 1) * largeur];
            let mut ip: Vec<usize> = (0..largeur).collect();
            ip.sort_by(|&a, &b| p[b].partial_cmp(&p[a]).unwrap());
            let k = (largeur / 10).max(1);
            let part: f64 = ip[..k].iter().map(|&i| p[i]).sum::<f64>()
                            / p.iter().sum::<f64>().max(1e-12);
            par_couche.push((t.iter().sum::<u64>() as f64 / n_tok as f64, 100.0 * part));
        }
=== 6890,6910 ===
            if actif {
                eprintln!("[engram] DRAVE_SANS_ENGRAM est actif : l'injection de l'engram \
est COUPÉE — le moteur calcule un autre modèle que V4.1, pour mesurer ce que l'engram \
change (vivacité). Ce chiffre ne vaut pas comme référence
… [1004 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"debut >= fin\\|a >= b\\|couche_debut >=\\|couche_fin >\\|fin > n\\b\" *.rs; echo \"--- 3480,3500 ---\"; sed -n '3480,3500p' model.rs", "description": "Check range guards"}`

  ```
main.rs:2131:                if debut >= fin || fin > n {
model.rs:2559:    /// flux (`couche_fin >= n_layer`) et le pilote le normait une SECONDE fois :
model.rs:6641:        if (self.couche_fin >= self.cfg.n_layer || self.tete_partielle) && !self.flux_brut {
--- 3480,3500 ---
        let map = crate::clusters::actif();
        let mut manques = manques_architecture(&g, &cfg, ctx, map.is_some());
        // Exécution bornée : le manque « attentions compressées » ne s'applique
        // que s'il tombe DANS la plage demandée. On le retire en le disant —
        // jamais en silence, et jamais au-delà de la plage.
        if let (Some((a, b)), true) = (couches, !manques.is_empty()) {
            // Ce qui reste non implémenté dans la compression, c'est le chemin
            // **CSA** (ratio 4 : compresseur à chevauchement + indexeur, P5).
            // HCA (ratio 128) est fait ; une plage qui ne contient que du HCA
            // est donc exécutable, et le dire couche par couche vaut mieux
            // qu'un « compressé / pas compressé » binaire.
            let ratios = g.couches_ratios();
            let compressees: Vec<usize> = ratios.iter().enumerate()
                .filt
… [466 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | grep -iE \"plage|couche\" ; echo \"---\"; grep -rn \"couches_locales\\|--couches\" README.md REPRISE.md 2>/dev/null | head -20", "description": "Look for plage docs in reports/README"}`

  ```
rapport-v4-couches-0-1.md
---
REPRISE.md:687:| Exécution bornée | `--couches a:b` : exécute une plage de couches pour comparer à la référence avant que le reste du modèle existe. Le manque retiré est **annoncé**, jamais silencieux |
REPRISE.md:1307:    --ppl-reparti 127.0.0.1:45999 --couches-locales 12 --limit 40 --ctx 256
REPRISE.md:1316:    --ppl-reparti 127.0.0.1:45760 --couches-locales 12 --limit 4 --ctx 256
REPRISE.md:1479:    --couches 0,6,12,24,36,47 --lignes 8
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -iE \"reparti|ppl-reparti|morcel|cluster|couches\" tools/portes.sh", "description": "Grep gates for reparti/clusters"}`

  ```
55:# 3. Modèle en clusters, mêmes jetons que l'original.
56:A=/home/stephane/FastNVMe/artefacts/modeles-optimises/qwen3-30b-8clusters-v2
60:    compare "Qwen3-30B en clusters (origine : 799,8557)" "799.8557" "$v"
106:#       V4-Flash : le modèle de la famille V4 tourne EN ENTIER (43 couches, les
128:        printf "  %-42s %s\n" "V4-Flash 43 couches ctx 32 (archivée)" "ARCHIVE=1 pour la lancer"
130:        # 8430,2968 -> 8430,4966 le 02/10 : la rotation des couches COMPRESSÉES est
143:        compare "V4-Flash 43 couches ctx 32" "8430.4966" "$p"
146:    printf "  %-42s %s\n" "V4-Flash 43 couches ctx 32" "modèle absent"
220:#          et un écart sous 1e-5. Une trace PARTIELLE (--trace-couches) laisse des
285:#   3 jetons sur 3 couches, et l'outil vérifie en plus que le Sinkhorn tient sa
292:    DRAVE_DUMP_COUCHES=/tmp/porte_hc timeout 900 $D "$V41_HC" --ppl /tmp/ids_v41_8.txt \
295:        sortie_hc=$(python3 tools/analyse_hc.py /tmp/porte_hc --couches 0,1,2 \
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"couches\\|cluster\" tools/portes.sh | head; echo \"=== REPRISE 1290-1340 ===\"; sed -n '1290,1340p' REPRISE.md", "description": "Read REPRISE distributed section"}`

  ```
55:# 3. Modèle en clusters, mêmes jetons que l'original.
56:A=/home/stephane/FastNVMe/artefacts/modeles-optimises/qwen3-30b-8clusters-v2
60:    compare "Qwen3-30B en clusters (origine : 799,8557)" "799.8557" "$v"
106:#       V4-Flash : le modèle de la famille V4 tourne EN ENTIER (43 couches, les
128:        printf "  %-42s %s\n" "V4-Flash 43 couches ctx 32 (archivée)" "ARCHIVE=1 pour la lancer"
130:        # 8430,2968 -> 8430,4966 le 02/10 : la rotation des couches COMPRESSÉES est
143:        compare "V4-Flash 43 couches ctx 32" "8430.4966" "$p"
146:    printf "  %-42s %s\n" "V4-Flash 43 couches ctx 32" "modèle absent"
220:#          et un écart sous 1e-5. Une trace PARTIELLE (--trace-couches) laisse des
285:#   3 jetons sur 3 couches, et l'outil vérifie en plus que le Sinkhorn tient sa
=== REPRISE 1290-1340 ===
#    moteur déporte alors tout seul les projections Q8_0 de plus de 8 Mo — le
#    chiffre devient 15,1667 (même calcul, ordre de sommation du noyau GPU).
./target/release/drave /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf \
    --ppl /tmp/ids_oss_512.txt --ctx 256 --dense --threads 16 --limit 512  # attendu 15,6017
#    (15,1757 avant le correctif 
… [2720 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"799\\|DRAVE_CLUSTERS\\|2,35\\|6,28\\|268786\\|268 786\\|15,2789\" REPRISE.md README.md reports/*.md docs/*.md 2>/dev/null | head -40", "description": "Grep measured cluster figures"}`

  ```
REPRISE.md:402:> **799,8557** · gpt-oss-120b MXFP4 ctx 256 = **15,6017** (**changée** par le
REPRISE.md:1339:    --ppl /tmp/ids_qwen.txt --ctx 64 --limit 64 --dense --threads 12 --lot 1   # 15,2789
REPRISE.md:1341:    --ppl /tmp/ids_qwen.txt --ctx 64 --limit 64 --dense --threads 12 --lot 1   # 15,2789
REPRISE.md:1351:DRAVE_CLUSTERS=0 ./drave-core/target/release/drave \
REPRISE.md:1622:| Qwen3-30B en clusters ctx 64, 8 jetons | **799,8557** | inchangée |
README.md:409:| **origine contre clusters** (mêmes 63 jetons) | **15,2789 = 15,2789** |
reports/rapport-coherence-docs.md:112:| 34 | `reports/rapport-transport-liste.md:3` | « en liste creuse (**871** octets au lieu de 3 623) » | son propre tableau donne **897** (listes i16, seuil 0,05) et 799 (blocs) ; 871 ne correspond à aucune ligne mesurée | CONTRADICTOIRE |
reports/rapport-coherence-vision.md:43:clusters que **rien ne mesure** (la mesure documentée est `origine 15,2789 ·
reports/rapport-coherence-vision.md:44:clusters 15,2789`). Elle a aussi confirmé, en scannant les **28 en-têtes GGUF** du
reports/rapport-coherence-vision.md:159:  `cargo test --release` **48**, Qwen **19,3885**, clusters **799,8557**,
reports/rapport-decoupage
… [3650 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extension de la délégation aux rapports clusters non listés

- **send_message** `{"agent_id": "a9e308b7-5d50-4bb3-8e31-4c8e6f261a6d", "message": "Complément : inclus AUSSI reports/rapport-lecteur-multifichiers.md (il traite le lecteur clusters/multifichiers, avec les chiffres 15,2789 / 268 786,62 / 799,8557 et les tableaux « nœud partiel ») et, si tu les trouves via grep « 799,8 … [431 caractères tronqués]`

  ```
message delivered to agent a9e308b7-5d50-4bb3-8e31-4c8e6f261a6d
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-lecteur-multifichiers.md", "limit": 120, "offset": 150}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-lecteur-multifichiers.md</path>
<type>file</type>
<content>
150: *Leçon : quand un correctif ne peut pas être testé, la question n'est pas
151: « comment écrire le test ? » mais « qu'est-ce qui manque pour le rendre
152: testable ? ». Ici, c'était un générateur de fichiers.*
153: 
154: ### Les modèles lourds, inventoriés par les en-têtes
155: 
156: `tools/inventaire_modeles_lourds.sh` confronte les poids annoncés par les
157: descripteurs GGUF aux tailles annoncées par HuggingFace. **La concordance porte
158: sur 984 Go** : DeepSeek-V4.1-Flash 365,70 = 365,7 · GLM-5.3 216,71 = 216,7 ·
159: Kimi-K2.7 303,90 = 303,9 · DeepSeek-V4-Flash 86,90 = 86,9 · GLM-5.3-Flash
160: 93,08 = 93,1 · Qwen3-235B 85,68 = 85,7. **La file de 1 138 Go est terminée**, et
161: chacun de ses modèles est complet : le lecteur refuse un découpage dont un shard
162: manque. Une seule entrée
163: fausse dans la table des types ggml donnerait un écart visible sur des centaines
164: de gigaoctets — c'est ainsi que `iq1_m` manquant avait fait annoncer 8,56 Go pour
165: 86,9 Go.
166: 
167: Les architectures sont lues (`deepseek41`, `deepseek2`, `de
… [5654 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification Moe::ou, biais d'experts et mmap

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"fn ou\\|biais\\|Biais\" model.rs clusters.rs | head -30; echo \"=== Moe::ou ===\"; grep -n \"impl Moe\" model.rs", "description": "Find Moe::ou and expert bias handling"}`

  ```
model.rs:36:    /// Top-k sur les logits **bruts** (plus le biais de sélection s'il existe),
model.rs:384:/// Elle existe parce que les deux chemins avaient divergé : le biais du routeur
model.rs:394:/// jeton. Le biais de sélection ne s'y applique pas (llama.cpp passe
model.rs:441:    // diffèrent pour gpt-oss, dont le biais ne départage que la sélection.
model.rs:442:    let biais = moe.routeur_biais.as_ref();
model.rs:453:            let s = match biais { Some(b) => p.iter().zip(b).map(|(a, c)| a + c).collect(), None => p.clone() };
model.rs:457:            let s = match biais { Some(b) => logits.iter().zip(b).map(|(a, c)| a + c).collect(), None => logits.clone() };
model.rs:462:            let s = match biais { Some(b) => p.iter().zip(b).map(|(a, c)| a + c).collect(), None => p.clone() };
model.rs:581:/// Une projection, dans l'un des deux formats, plus son biais éventuel.
model.rs:751:    let biais = |nom: &str| -> Option<Vec<f32>> {
model.rs:757:    // Biais de SÉLECTION, et il y en a deux sortes dans les GGUF :
model.rs:764:    // **Deux biais de routeur dans le fichier de V4.1** (`exp_probs_b.bias` et
model.rs:766:    // couche 0) et le biais DOMINE la sélection (les scores
… [1274 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"DRAVE_MMAP\\|mmap\\|Mmap\" gguf.rs | head -30", "description": "Check mmap handling in gguf.rs"}`

  ```
25:/// Le mmap ne lit rien : il rend une plage d'adresses, et le noyau lit les pages
41:    fn mmap(addr: *mut u8, len: usize, prot: i32, flags: i32, fd: i32, offset: i64) -> *mut u8;
58:/// utilisateur quand les poids sont mmappés : on ne peut pas lire soi-même sans
59:/// renoncer au mmap. Le noyau, lui, peut lancer plusieurs lectures de pages en
75:/// chargement. Le noyau parallélise ses lectures de pages, là où le mmap
78:/// Mesuré : charger 18,6 Go prend 6,8 s en mmap paresseux (2,7 Go/s) — proche du
106:        let p = unsafe { mmap(std::ptr::null_mut(), len, PROT_READ, MAP_PRIVATE, f.as_raw_fd(), 0) };
107:        // `mmap` rend `MAP_FAILED` (soit -1) en cas d'échec.
153:/// moins d'octets lus. `DRAVE_MMAP=0` force la lecture complète (utile pour
154:/// comparer, ou sur un système de fichiers qui refuse le mmap).
155:fn mmap_voulu() -> bool {
156:    match std::env::var("DRAVE_MMAP") {
166:    if mmap_voulu() {
169:            Err(e) => eprintln!("[gguf] mmap refusé sur {} ({e}) : lecture complète",
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 40, "offset": 1290}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
1290:     /// couche » ou si les experts rares comptent.
1291:     pub masque: Option<Vec<f32>>,
1292: }
1293: 
1294: impl Moe {
1295:     /// Où trouver l'expert GLOBAL `e` : `(vue, ligne locale)`. `None` signifie
1296:     /// que cet expert n'est pas dans ce nœud — ce n'est pas une erreur, c'est
1297:     /// le principe même du découpage.
1298:     #[inline]
1299:     pub fn ou(&self, e: usize) -> Option<(usize, usize)> {
1300:         match self.local {
1301:             None => if e < self.n_expert_global { Some((0, e)) } else { None },
1302:             Some(m) => {
1303:                 let (cluster, ligne) = m.ou(self.couche, e)?;
1304:                 // Le cluster de l'expert n'est pas forcément chargé ici : c'est
1305:                 // exactement ce que veut dire « nœud partiel », et ce n'est pas
1306:                 // une erreur.
1307:                 let k = self.numeros.iter().position(|c| *c == cluster)?;
1308:                 Some((k, ligne))
1309:             }
1310:         }
1311:     }
1312: }
1313: 
1314: /// `DRAVE_SANS_COMPRESSION=1` : le RATI
… [965 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '786,800p' model.rs; echo \"=== gguf 145,175 ===\"; sed -n '145,175p' gguf.rs", "description": "Read expert bias refusal and mmap choice"}`

  ```
} else if g.tensor(&p("ffn_gate_inp.bias")).is_some() {
        Some(g.dequant(&p("ffn_gate_inp.bias")))
    } else { None };
    let (bg, bu, bd) = (biais(&p("ffn_gate_exps.bias")), biais(&p("ffn_up_exps.bias")),
                        biais(&p("ffn_down_exps.bias")));
    // Un modèle en clusters peut avoir des biais par expert : ils sont alors
    // découpés eux aussi, et les indexer par l'expert GLOBAL lirait la mauvaise
    // ligne. Plutôt qu'un résultat faux et silencieux, on refuse.
    if map.is_some() && (bg.is_some() || bu.is_some() || bd.is_some()) {
        panic!("couche {l} : biais d'experts + clusters — le découpage des biais \
n'est pas implémenté, et les indexer par l'expert global serait faux");
    }
    // Routage par TABLE (couches `hash_layer_count` de DeepSeek-V4) : la
    // sélection des experts n'y dépend pas du routeur appris mais de
    // l'identifiant du jeton. Le tenseur est en I32, et l'ignorer ferait router
=== gguf 145,175 ===
}

impl Tampon {
    pub fn len(&self) -> usize { (**self).len() }
    pub fn is_empty(&self) -> bool { self.len() == 0 }
}

/// Faut-il mapper les fichiers ? Mappé par défaut : c'est moins de mémoire et
/// moins d'octets
… [856 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection de l'assemblage multi-fichiers et de l'alignement

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"fn open_avec_prefixes\\|fn open_meta_avec_prefixes\\|fn open_auto\\|fn nb_fichiers\\|alignment\\|alignement\" gguf.rs | head -30", "description": "Find multi-file open and alignment"}`

  ```
478:    pub fn open_avec_prefixes<P: AsRef<Path>>(chemins: &[P], prefixes: &[&str])
513:            // la même ; l'alignement n'est pas une propriété par fichier.
630:    pub fn open_auto<P: AsRef<Path>>(path: P) -> std::io::Result<Self> {
665:    pub fn open_meta_avec_prefixes<P: AsRef<Path>>(chemins: &[P], prefixes: &[&str])
833:    pub fn nb_fichiers(&self) -> usize { self.starts.len() }
916:        let align = meta.get("general.alignment").and_then(|m| m.as_u64()).unwrap_or(32) as usize;
1997:        s(&mut b, "general.alignment");
2048:        s(&mut b, "general.alignment");
2100:        s(&mut b, "general.alignment");
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '440,500p' gguf.rs; echo \"=== 620,660 ===\"; sed -n '620,660p' gguf.rs", "description": "Read multi-file documentation"}`

  ```
buf.truncate(lu);
            if let Some((meta, tensors, fin)) = Self::entete(&buf) {
                let data_start = Self::debut_donnees(&meta, fin);
                return Ok(Gguf { meta, tensors, bufs: Vec::new(), starts: vec![data_start] });
            }
            if lu < taille {
                return Err(std::io::Error::new(std::io::ErrorKind::UnexpectedEof,
                                               "en-tête GGUF incomplet"));
            }
            taille *= 4;
        }
    }

    /// Ouvre un modèle **éclaté en plusieurs fichiers** : soit les shards d'un
    /// GGUF découpé (`…-00001-of-00003.gguf`), soit notre format en clusters
    /// (`commun.gguf` + `cluster-XX.gguf`).
    ///
    /// Règles, toutes dictées par ce qu'on a observé sur les fichiers réels :
    ///
    /// * les métadonnées sont prises au **premier fichier qui en porte** — un
    ///   GGUF découpé les duplique sur chaque shard, un modèle en clusters ne
    ///   les met que dans `commun.gguf`, et le second shard de
    ///   DeepSeek-V4-Flash porte 784 tenseurs sans aucune métadonnée ;
    /// * les tenseurs sont concaténés **dans l'ordre des chemins**, chacun
    ///   gardant le numéro 
… [4017 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 55, "offset": 240}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
240:         eprintln!("[mla] attention MLA à rang faible : cache LATENT (c_kv + k_rope), pas de \
241: fenêtre glissante ni de YaRN sur ce chemin. Validée contre llama.cpp sur GLM-5.3 à la \
242: POSITION 0 : corrélation des logits 0,999024, top-1 3/3 ; l'écart croît ensuite \
243: (+0,009 / +0,372 / +0,611 puis +4,070 nat à la position 3 — voir reports/rapport-mla-experts.md §7).");
244:     }
245:     manques
246: }
247: 
248: #[allow(clippy::too_many_arguments)]
249: fn refus_architecture(g: &Gguf, cfg: &Cfg, ctx: usize, clusters: bool, manques: Vec<&str>)
250:     -> Result<(), String> {
251:     if !manques.is_empty() {
252:         return Err(format!(
253:             "architecture « {} » non implémentée par ce moteur : {}.\n  \
254: Ce modèle n'est donc pas calculé. Les chiffres publiés à son sujet ne viennent pas \
255: d'une passe avant COMPLÈTE : analyse statique des tenseurs (inventaire, empreinte, \
256: sonde mmap), ou passe bornée `--couches a:b` — annoncée comme telle.\n  \
257: Tenseurs présents : {}{}{}",
258:             g.meta.get("general.architectur
… [2269 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '75,95p' main.rs; echo \"=== 420,465 ===\"; sed -n '420,465p' main.rs", "description": "Read usage text and tete-partielle"}`

  ```
fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        eprintln!("usage: drave <modele.gguf|dossier-de-clusters> [--matrix NOM] [--threads N]");
        eprintln!("       drave <modele> --infer (--ids 1,2,3 | --prompt TEXTE | --ids-file F)");
        eprintln!("             [--n 32] [--temp 0] [--ctx 512] [--threads N]");
        eprintln!("       drave <modele> --ppl FICHIER-IDS [--ctx N] [--limit N] [--dense]");
        eprintln!("       drave <modele> --tensors      inventaire par les en-têtes seuls");
        eprintln!("       drave <modele> --materiel     détection matérielle et plan de");
        eprintln!("                                     configuration, AVEC la raison de chaque");
        eprintln!("                                     choix — ne charge pas le modèle");
        eprintln!("       drave <modele> --sonder-engram N   accès mmappé à une table d'engram");
        eprintln!("       drave <modele> --tete-restreinte F  génération CONTRAINTE : la tête ne");
        eprintln!("                                     calcule que les tokens de F. Change la");
        eprintln!("                                     sortie — re
… [3242 caractères tronqués]
  ```

### 👤 Utilisateur

Agent a9e308b7-5d50-4bb3-8e31-4c8e6f261a6d sent a message:
CONDENSÉ FACTUEL (lecture seule respectée ; aucun fichier modifié). Aucun fichier reports/*cluster* n'existe (glob + ls) — seuls moe/morcel existent.

LÉGENDE : moe=reports/rapport-decoupage-moe.md (117 l.) ; v41=reports/rapport-decoupage-v41.md (180 l.) ; morc=reports/rapport-morcellement-experts.md (86 l.) ; dig=reports/decoupage-v41-digest.txt (311 l.).

[1] moe — Objet : mesurer si regrouper les experts d'un MoE (fréquence vs co-activation) réduit le nombre de nœuds lus par jeton (moe:1-8).
Chiffres mesurés : Qwen3-30B-A3B, 128 experts, 8/jeton (moe:3) ; ~1 600 jetons, 48 couches (moe:37) ; clusters 4/8/16 → couverture 0,799/0,607/0,442, ventilation 1,94/3,08/4,46 ; témoin hasard 0,440/0,319/0,250 et 3,59/5,32/6,55, gain ×1,8-1,9 (moe:41-43) ; accord co-activation vs tri par fréquence = 1,000 (moe:47) ; 8 clusters : 3,08 nœuds au lieu de 5,32, ventilation ÷1,7 ; 4 nœuds : 1,94 (moe:58-60) ; conversion : 3,20 Go au lieu de 18,56, 625 ms au lieu de 3,9 s, 1 587 tenseurs vérifiés (moe:105-106).
MESURÉ vs DÉDUIT/SUPPOSÉ/À FAIRE : négatif mesuré « la co-activation n'ajoute rien » (moe:45-50) ; équilibrer par usage = « autre problème (et une autre mesure) » (moe:61-65) ; format = « esquisse, à confronter » (moe:67) ; gpt-oss « en cours de mesure », V4.1/Kimi/GLM « en téléchargement » (moe:86-89) ; usage pondéré non mesuré (moe:90-92) ; coût du déséquilibre « mesuré nulle part ici » (moe:95) ; 1 600 jetons insuffisants, trace 2 048 en cours (moe:96-98).
Plages/clusters : 48 couches (moe:37), index MoE « par couche » (moe:73), AUCUN découpage a:b de plages ; découpage = clusters d'EXPERTS (moe:24-32, 58, 76-79).

[2] v41 — Objet : prouver qu'un V4.1 découpé à la couche 20 rend un état identique au bit près à une passe complète, et innocenter l'instrument (v41:1-9).
Chiffres mesurés : DeepSeek-V4.1-Flash-Q2 365,71 Go, 40 couches (v41:3-4) ; écart en cause 7,05e-1 (v41:7) ; 514 722,06 vs 1 743 713,62 (v41:15) ; --ppl 208 411,867 en 16 bits (32 767 niveaux) vs 8 bits (127) (v41:16) ; avant correctif 629/953 différents (pos.1 : 319, pos.2 : 310, pos.0 : 0), après 0/953, moteur 0/945, référence 0/1 591 ; 2 544 fichiers dont 1 591 déterminisme et 953 couture (v41:26-39) ; réduction finale 0,000e+00 sur 5 120 valeurs ×3 positions (v41:50) ; transport 20 480 f32 (v41:57) ; après correctif ppl 1 743 713,6243 en 68,0 s (réf.) / 51,3 s (2 nœuds), écart 0.00e0, dense f32 82 016 o aller / 81 999 retour / 3 flux (v41:82-86) ; 82 016 = 79+1+16+20 480 f32, pré-mix 0,02 % (v41:88-89) ; V4-Flash déjà 0,00e0 (v41:96) ; --dense vs --ppl : 2 544 identiques, 208 411,8674 (v41:108) ; --abits 8 : 2 544 identiques, 1 743 713,6243 (v41:109) ; 16 vs 8 bits : 2 443 différents, 1er l_last-0-* = 1,793e-3 (v41:110) ; Qwen2.5-0.5B, 24 jetons, ctx 64, 12 couches locales, lot 4 : mode 3 0,00e0 / mode 4 4,45e-3 / mode 2 3,65e-2 (v41:134-141) ; digeste 2 544+945 tenseurs, somme 0,000e+00 (v41:168-169) ; porte 20 s sur 0,5 B (v41:175).
MESURÉ vs DÉDUIT/À FAIRE : cause identifiée + correctif mesuré 2× (v41:6-9, 79-86) ; « reste ouvert » : aucun test auto ne rejoue les 365 Go, passe manuelle (v41:171-176) ; masque jetons d'image = no-op (v41:177) ; YaRN >~1 024 positions : convention tranchée, « la mesure à contexte long reste à faire » (v41:178-180).
Plages/clusters : plages explicites couches 0-19 (pilote) / 20-39 (pair) (v41:26-28, 33, 153), 12 locales (v41:163), règle couche_debut > 0 (v41:62-63) ; transport « dense f32 » (v41:85), --ppl --dense (v41:108-112), mode 3 « lot dense f32 » (v41:139) ; AUCUN cluster d'experts (MoE cité seulement pour la quantification, v41:116-118).

[3] morc — Objet : tester sans entraînement si l'élagage par fréquence mesurée garde les qualités du modèle (« morcellement ») (morc:1-11).
Chiffres mesurés : Qwen3-30B-A3B 48 couches, 128 experts, 8/jeton (morc:14) ; scénario code, 384 jetons du dépôt (morc:15-16) ; trace 18 432 lignes (morc:18) ; 128 gardés → 100 % → ppl 9,584 ; 96 (75 %) → 99,6 % → 11,327 → +18,2 % ; 64 (50 %) → 94,3 % → 12,515 → +30,6 % ; 32 (25 %) → 74,2 % → 18,605 → +94,1 % (morc:26-31) ; 18 % de ppl pour 0,4 % de masse (morc:36-37) ; 99,6 %→+18 %, 74,2 %→+94 % (morc:40-42) ; GPU 2 × 16 Go PCIe (morc:74) ; K3 896 experts/couche (morc:82). Citation externe : Coder d'ISTA-DASLab 256/512, 91,3 % SWE-bench (morc:46-47).
MESURÉ vs DÉDUIT/À FAIRE : tableau = mesuré (morc:24-31) ; masque DRAVE_EXPERTS_GARDES = « un autre modèle » mesuré comme tel (morc:20-22) ; importance par retrait (leave-one-out) = proposition non mesurée (morc:52-61) ; « ce qu'il faut mesurer ensuite » (morc:78-84) ; Drave sélectionne, ne crée pas, distillation = projet GPU (morc:70-76) ; scénario par couche « à vérifier plutôt qu'à supposer » (morc:84-86).
Plages/clusters : raisonnement « couche par couche » / « à l'entrée d'une couche » (morc:3-4, 66-67, 84-85), élagage par couche (morc:19, 82) ; AUCUNE plage a:b ; AUCUN cluster : élagage d'experts par fréquence.

[4] dig — Objet : digeste tenseur par tenseur (famille, n comparés, n différents, écart max) des comparaisons de découpage V4.1 (dig:1-6).
Chiffres mesurés : 2 544 fichiers/passe, ~50 Mo, non versionnables (dig:4) ; 1 591 = déterminisme, 953 = couture (dig:12-16) ; 365,7 Go, ~4 min/passe (dig:19) ; ids 270,15301,6605,223 (dig:32-33) ; 16 bits/32 767 vs 8/127 (dig:37-38) ; après correctif : 953/0/0.000e+00 (dig:43), 1 591/0/0.000e+00 (dig:72), 945/0/0.000e+00 (dig:111) ; avant : 953/629/1.132e+02 (dig:143) ; --abits 8 vs réf. harnais : 2 544/0/0.000e+00 (dig:147) ; 16 vs 8 bits : 2 544/2 443/4.334e+03, ex. l-l_last 160 diff., max 6.137e+01 (dig:186, 218) ; --dense vs --ppl : 2 544/0/0.000e+00 (dig:225) ; DRAVE_SANS_ENGRAM=1 : 2 528/2 431/8.406e+03 (dig:264) ; réduction finale 0.000e+00 sur 5 120 valeurs (pos 0, 1, 2) (dig:304-306) ; 953 restent identiques (dig:311).
MESURÉ vs DÉDUIT : tout est mesuré ; avertissement d'attribution relevé par relecture adverse (dig:8-17) ; « Piège de comparaison, mesuré » (dig:37).
Plages/clusters : couches 0-19 (dig:42), référence 0-39 (dig:71), nœud 20-39 (dig:110), --couches-locales 20 (dig:30) ; --ppl --dense (dig:224) ; AUCUN cluster d'experts.

Recherche lexicale (suppos|déduit|hypothès|reste à|non testé|TODO) : 2 occurrences seulement — v41:180, morc:86.
VERIF: lus — 4 fichiers ci-dessus = 694 lignes ; glob reports/*cluster* → 0 fichier ; lecture seule, rien modifié/compilé/testé.

### 🤖 Assistant

⏵ Dernières vérifications : relais de plage et protocole pilote/pair

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 45, "offset": 6770}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
6770:         //
6771:         // La prendre ici la faisait consommer par le jeton SUIVANT : mesuré, le
6772:         // pilote V4.1 de `--ppl-reparti` gardait la `pre` du pair au titre du
6773:         // jeton 0, la réinjectait dans la chaîne du jeton 1, et rendait une
6774:         // perplexité de 514 722,06 au lieu de 1 743 713,62 — la position 0
6775:         // exacte au bit près, les suivantes fausses, sans un mot. Un défaut
6776:         // muet de plus, et il ne pouvait apparaître que sur un modèle à chaîne
6777:         // retardée (V4.1) : V4-Flash, dont la réduction finale est apprise,
6778:         // ignore ce champ et restait exact.
6779:         let reprend = self.couche_debut > 0;
6780:         let recue = reprend && self.hc_porte_imposee.is_some();
6781:         let mut hc_porte: Option<Vec<f32>> =
6782:             if reprend { self.hc_porte_imposee.take() } else { None };
6783:         // Un nœud qui REPREND à la couche k reçoit un flux brut : s'il ne porte
6784:         // pas ces coefficients (protocole < v6), V4.1 replierait avec la copie 0
6785: 
… [2151 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"fn envoyer_flux\\|fn envoyer_lot\\b\\|fn envoyer_lot(\" main.rs; echo \"=== 2495,2560 ===\"; sed -n '2495,2515p' main.rs", "description": "Check transport header carrying the range"}`

  ```
2802:fn envoyer_flux(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos: u32,
2883:fn envoyer_lot(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos0: u32,
=== 2495,2560 ===
    mdl.act_thresh = opt.act_thresh;
    mdl.act_topk = opt.act_topk;
    mdl.act_renorm = opt.act_renorm;
    // Les top-k étaient PUREMENT ignorés dans les modes flux (audit
    // `reports/rapport-drapeaux-ignores.md`, défaut n°1) : ils s'appliquent ici,
    // et ils voyagent dans l'en-tête pour que les deux nœuds fassent pareil.
    mdl.act_topk_proj = opt.topk_proj;
    mdl.attn_topk = opt.attn_topk;
    mdl.qk_topk = opt.qk_topk;
    mdl.moe_topk = opt.moe_topk;
}

/// ---- Phase 3 : le flux passe d'un nœud à l'autre ----------------------------
///
/// Cadriciel : `u32` magie, `u32` plage (debut, fin), `u32` position, `u32`
/// dimension, puis les activations en f32. C'est le même contenu que le format
/// de trace, réduit à ce qu'un nœud a besoin de recevoir pour continuer.
const MAGIE_FLUX: u32 = 0x4452_5631;   // "DRV1"
/// Version du protocole de flux. Elle est dans CHAQUE en-tête : un pair d'une
/// autre version est refusé avec un message qui dit laquelle il parle, plutôt
/// que de laisse
… [56 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des experts partagés (shexp) dans le découpage

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"shexp\\|partag\" drave-core/src/model.rs tools/convertir_clusters.py docs/format-clusters.md | head -30", "description": "Check shared expert handling"}`

  ```
drave-core/src/model.rs:27:/// implémentation partagée par le jeton seul et le lot (voir [`router`]).
drave-core/src/model.rs:193:    // **V4.1 : les ratios 1 et 2, et le cache compressé partagé.** Ce n'est plus
drave-core/src/model.rs:441:    // diffèrent pour gpt-oss, dont le biais ne départage que la sélection.
drave-core/src/model.rs:695:    // Vue d'un tenseur 3D NON découpé (l'expert partagé, qui reste dans le
drave-core/src/model.rs:697:    // Vue d'un tenseur NON découpé : l'expert partagé, qui reste dans le
drave-core/src/model.rs:699:    // refusait en silence, et l'expert partagé des modèles DeepSeek/GLM/Kimi
drave-core/src/model.rs:743:    // Expert partagé (Qwen3-MoE d'origine, DeepSeek) : toujours actif.
drave-core/src/model.rs:744:    let shexp = match (vue_unique(&p("ffn_gate_shexp.weight")),
drave-core/src/model.rs:745:                       vue_unique(&p("ffn_up_shexp.weight")),
drave-core/src/model.rs:746:                       vue_unique(&p("ffn_down_shexp.weight"))) {
drave-core/src/model.rs:814:        n_ff, gate, up, down, shexp, tid2eid,
drave-core/src/model.rs:1279:    /// Expert partagé, toujours actif (certains modèles seulement).
drave-core/src/model.rs:
… [1659 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"n_expert_shared\\|expert_shared\\|_shexp\" drave-core/src/*.rs tools/*.py | head -20", "description": "Grep shared expert fields"}`

  ```
drave-core/src/kimi_k3.rs:18://! | MoE (les autres) | `ffn_gate_inp`, `exp_probs_b`, `ffn_routed_down`, `ffn_routed_norm`, `ffn_routed_up`, `ffn_{gate,up,down}_exps`, `ffn_{gate,up,down}_shexp` |
drave-core/src/kimi_k3.rs:188:               "ffn_gate_shexp.weight", "ffn_up_shexp.weight", "ffn_down_shexp.weight"];
drave-core/src/kimi_k3.rs:551:    let n_shared = lire("kimi-k3.expert_shared_count", 2);
drave-core/src/kimi_k3.rs:621:        attendu(&mut ecarts, p("ffn_gate_shexp.weight"), vec![n_shared * n_ff_exp, h]);
drave-core/src/kimi_k3.rs:622:        attendu(&mut ecarts, p("ffn_down_shexp.weight"), vec![h, n_shared * n_ff_exp]);
drave-core/src/kimi_k3.rs:741:        let n_shared_ff = dims(&p("ffn_gate_shexp.weight"))?[0];
drave-core/src/kimi_k3.rs:753:            sh_gate: lu(&p("ffn_gate_shexp.weight"))?,
drave-core/src/kimi_k3.rs:754:            sh_up: lu(&p("ffn_up_shexp.weight"))?,
drave-core/src/kimi_k3.rs:755:            sh_down: lu(&p("ffn_down_shexp.weight"))?,
drave-core/src/model.rs:744:    let shexp = match (vue_unique(&p("ffn_gate_shexp.weight")),
drave-core/src/model.rs:745:                       vue_unique(&p("ffn_up_shexp.weight")),
drave-core/src/model.rs:746:    
… [735 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 45, "offset": 688}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
688:                 eprintln!("[moe] couche {l} : données de « {nom} » introuvables");
689:                 return None;
690:             };
691:             out.push(Vue4 { base: ptr, n_out, n_in, nb: n_in / bloc, src });
692:         }
693:         Some((numeros, out))
694:     };
695:     // Vue d'un tenseur 3D NON découpé (l'expert partagé, qui reste dans le
696:     // fichier commun) : aucune traduction d'index n'est nécessaire.
697:     // Vue d'un tenseur NON découpé : l'expert partagé, qui reste dans le
698:     // fichier commun. Il est en 2D (`[n_ff, hidden]`) — exiger 3 dimensions le
699:     // refusait en silence, et l'expert partagé des modèles DeepSeek/GLM/Kimi
700:     // n'était donc jamais calculé. Sa contribution n'est pas un détail : c'est
701:     // un FFN entier, toujours actif, ajouté à la sortie des experts routés.
702:     let vue_unique = |nom: &str| -> Option<Vue4> {
703:         let t = g.tensor(nom)?;
704:         let src = source_de(t.ttype)?;
705:         let (n_out, n_in) = match t.dims.len() {
706:             2 => (t.dims[0] as usize,
… [1686 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recensement final des tests liés (clusters.rs et gguf.rs)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && awk 'NR>=1891 {print NR\": \"$0}' gguf.rs | grep -E \"fn [a-z_]+\\(\\)\" | head -40", "description": "List test fn names in gguf.rs"}`

  ```
1899:     fn json_du_config_brut() {
2163:     fn multi_fichiers_egale_mono_fichier() {
2245:     fn prefixes_distinguent_les_homonymes() {
2278:     fn type_inconnu_ne_compte_pas_zero_en_silence() {
2295:     fn shards_reconnus_et_rassembles() {
2328:     fn multi_fichiers_refuse_les_doublons_divergents() {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && awk '/#\\[test\\]/{t=NR} /fn [a-z_0-9]+\\(\\)/{print NR\": \"$0}' clusters.rs", "description": "List cluster test names"}`

  ```
129: pub fn actif() -> Option<&'static Mapping> { ACTIF.get() }
167: pub fn gardes_du_milieu() -> std::io::Result<Option<Vec<usize>>> {
310:     fn mapping_lu_et_traduit() {
339:     fn mapping_refuse_les_doublons() {
356:     fn dossier_de_clusters_ouvre_et_apparie() {
419:     fn sous_ensemble_garde_les_numeros() {
476:     fn numerotation_des_clusters_exigee_continue() {
495:     fn mapping_partiel_est_permis() {
  ```

### 🤖 Assistant

⏵ Envoi du condensé à l'agent parent, puis réponse finale

- **send_message** `{"agent_id": "482522d1-31f1-43eb-ae9c-a681336404f7", "message": "CONDENSÉ — Découpage en clusters et par plages de couches (Qtrinet/Drave, lecture seule stricte, rien modifié/compilé/testé). État : P = vérifié par une porte, M = mesuré localement (rapport/REPRISE), D = déduit du code.\n\n1) TABLEAU\ … [6352 caractères tronqués]`

  ```
message delivered to agent 482522d1-31f1-43eb-ae9c-a681336404f7
  ```

### 🤖 Assistant

⏵ Condensé final — clusters et plages de couches (lecture seule respectée)

**1) Tableau** — état : P = vérifié par une porte, M = mesuré localement (rapport/REPRISE), D = déduit du code.

| capacité | ce qu'elle fait | fichier source | état | chiffre mesuré |
|---|---|---|---|---|
| Lecteur clusters | commun.gguf + cluster-XX.gguf réunis en un `Gguf` ; experts exposés sous `cl{c}/` ; `mapping.tsv` lu d'un bloc | `clusters.rs:150-297` · `gguf.rs:478-520` | P (porte 1 : 6 tests `clusters.rs:309-505` ; porte 3) | 9 fichiers · 1 587 tenseurs · 18,55 Go |
| Nœud partiel | `DRAVE_CLUSTERS=0,3` ne charge que ces clusters ; demandé-absent = erreur ; dossier incomplet refusé sans `DRAVE_CLUSTERS` | `clusters.rs:167-176, 239-273, 291-295` | M | 1 cl. 2,35 Go / 268 786,62 · 4 cl. 4,60 Go / 3 378,91 · 8 cl. 6,28 Go / 799,8557 |
| Porte clusters | dossier complet Qwen3-30B 8 clusters, mêmes jetons | `tools/portes.sh:55-61` | P | attendu 799.8557 (`--ctx 64 --limit 8 --dense --threads 8 --lot 1`) |
| Convertisseur experts | GGUF → commun + 8 `cluster-XX.gguf` + `mapping.tsv` + `manifeste.json`, copie d'octets sans requantification | `tools/convertir_clusters.py:402-582` | M | 435+8×144 = 1 587 tenseurs · 18,60 Go · 351,7 s · SHA-256 « TOUT CONCORDE » |
| Conversion par plages de couches | `--mode couches` : blocs `blk.N` en groupes contigus (dense), pas de `mapping.tsv` | `convertir_clusters.py:446-463, 520-529` | M | Qwen2.5-0.5B : commun + 4 fichiers × 6 couches · 290 tenseurs |
| mmap du dossier | N fichiers mappés, pages lues à la demande | `gguf.rs:153-170` · `clusters.rs:282-286` | M | 9,32 s / 6,35 Go contre 30,68 s / 19,20 Go (`DRAVE_MMAP=0`), ppl identique |
| Plage de couches moteur | `couche_debut..couche_fin` = [a,b) exécutée ; hors plage → flux résiduel brut | `model.rs:2551-2569, 4368-4369, 6641-6646, 6904-6905` | M (V4.1), aucune porte | V4.1 2 nœuds : écart 0,00e0 · 1 743 713,6243 (51,3 s contre 68,0 s) |
| Réparti pilote/pair | `--couches-locales N` : local [0,N), pair [N,n_layer), plage portée par l'en-tête | `main.rs:3345, 3430, 3457-3460, 3549, 3204-3213` | M | écart 0,00e0 dense (`REPRISE.md:1307-1316`) |
| Outils d'analyse | co-activation/ventilation MoE, union d'experts lus, jumeaux statiques, localité de couche (R²) | `tools/clusters_moe.py` · `analyse_union_experts.py` · `analyse_experts_statique.py` · `localite_couches.py` | M hors moteur | couverture 0,799/0,607/0,442 à 4/8/16 clusters ; hasard 0,440/0,319/0,250 |

**2) Ce que le format change / reste à faire**
- Fichiers : commun + N clusters + `mapping.tsv` + `manifeste.json` (9 GGUF) ; source 18,56 Go → commun 1,00 Go + cluster 2,20 Go ; surcoût = métadonnées dupliquées 8×~4 Mo = 0,2 % (`docs/format-clusters.md:80-89`).
- Partagé : routeur `ffn_gate_inp` (`clusters.rs:9-11`) ; expert partagé `ffn_*_shexp` (2D, ne matche pas « _exps. ») → `convertir_clusters.py:428`, `model.rs:695-713`. Biais d'experts + clusters = **refusé par panic** plutôt que mal indexé (`model.rs:791-796`).
- Jointure : TSV 4 colonnes (couche, local, global, cluster), 6 144 lignes pour 48×128 (`rapport-lecteur-multifichiers.md:240`) ; rangé en `local[couche][global]=cluster×65536+ligne` (`clusters.rs:103`), publié en `OnceLock` après ouverture réussie (`clusters.rs:291-295`) ; `Moe::ou` traduit puis cherche le n° parmi les vues chargées (`model.rs:1299-1311`) ; les 3 projections doivent porter les mêmes clusters (`model.rs:717-731`).
- À faire : sommer les contributions entre nœuds (`docs/format-clusters.md:175-178`) ; découper les biais ; équilibrer par charge (`:187-189`) ; manifeste binaire si un fichier par expert (`:185-186`).

**3) Sémantique exacte**
- `--couches a:b` : `main.rs:706-712` — exige « a:b » (sinon panic), `a`/`b` en `usize` par `parse().unwrap()` ; **aucun contrôle de bornes** à l'analyse. Report `model.rs:4368-4369` : `couche_debut=a`, `couche_fin=b` ; doc « dernière couche PORTÉE (exclue) » (`model.rs:2551-2554`) → **[a,b)** ; boucles `for l in couche_debut..couche_fin` (`model.rs:6904`, aussi 4751, 5345, 6562). a inclus, b exclu.
- `b == n_layer` → norme finale + tête (`model.rs:6641-6646`) ; `b < n_layer` → flux brut (`model.rs:5740, 7745-7752`), sauf `--tete-partielle` (modèle TRONQUÉ, annoncé, `main.rs:423-435`).
- Refus : `a>=b` et `b>n_layer` **ne sont pas refusés** par le moteur principal — `a>=b` = boucle vide silencieuse ; `b>n_layer` = `layers[l]` indexé directement (`model.rs:6905`) → panique d'index. Seuls gardes : `--k3-essai` (`main.rs:2131-2134`) et le serveur de flux (`main.rs:3210-3213`, flux refusé, nœud vivant).
- Reprise à `a>0` sans flux : V4.1 avertit « convention de sonde, copie 0 » (`model.rs:6791-6800`) ou assert si flux brut sans `pre` (`:6787-6790`) ; un manque d'architecture n'est retiré que dans [a,b) (`:3485-3500`).
- `--plage` **n'existe pas** comme option (grep `"--plage"` = 0) ; c'est le concept, `--k3-essai` réutilise `opt.couches` (`main.rs:147, 1899`).
- `--couches-locales N` : `main.rs:705`, défaut 12 si 0 (`:3345`) ; pilote `couche_fin=N`, `couche_debut` reste 0 (`:3430`) → [0,N) ; l'en-tête porte `debut=N, fin=n_layer` (`:3457-3460, 3549`) → pair exécute [N,n_layer), revalidé (`:3210`). Aucun contrôle `N ≤ n_layer` (D).

**4) Mesuré vs déduit vs supposé**
- Mesuré et gardé : 799,8557 (porte 3, dossier complet, ctx 64, 8 ids → 7 jetons) ; 6 tests unitaires `clusters.rs` via la porte 1 (`portes.sh:32-44`). **Aucune porte** ne couvre `DRAVE_CLUSTERS`, `--couches a:b` ni `--couches-locales` (grep `portes.sh` : néant).
- Mesuré une fois, non gardé : table nœud partiel 1/2/4/8 clusters (`rapport-lecteur-multifichiers.md:199-204`) ; 15,2789 = 15,2789 sur 63 jetons (`docs/format-clusters.md:116`) ; conversion, mmap, mesures Python.
- Déduit du code : absence de refus pour `a>=b`, `b>n_layer`, `N>n_layer` ; boucle vide silencieuse.
- Supposé/à faire : « la somme inter-nœuds rendrait 799,8557 pour 4,60 Go par nœud » est un calcul, pas une mesure (`rapport-lecteur-multifichiers.md:209-210`) ; biais refusés ; équilibrage par charge non fait.
- Aucun `reports/*cluster*` : les rapports réels sont `rapport-lecteur-multifichiers.md`, `rapport-decoupage-moe.md` (clusters d'experts, pas de plage a:b), `rapport-decoupage-v41.md` et `decoupage-v41-digest.txt` (plages 0-19/20-39, pas de clusters).

### 👤 Utilisateur

Agent a9e308b7-5d50-4bb3-8e31-4c8e6f261a6d sent a message:
CONDENSÉ ÉTENDU (≤55 l., lecture seule). Aucun reports/*cluster* (glob) ; DRAVE_CLUSTERS seulement dans lect:125,193.

LÉGENDE (sous reports/) : moe=rapport-decoupage-moe.md ; v41=rapport-decoupage-v41.md ; morc=rapport-morcellement-experts.md ; dig=decoupage-v41-digest.txt ; lect=rapport-lecteur-multifichiers.md ; rout=rapport-routage-experts.md ; opt=rapport-optimisations-auto.md ; port=rapport-portes-p0-p9.md ; coh=rapport-coherence-vision.md ; mla=rapport-mla-experts.md ; v4r=rapport-v4-reparti.md ; mat=rapport-materiel-disque-ou-cpu.md ; ph3=rapport-phase3-reparti.md ; k3=rapport-passe-k3-disque.md ; emp=rapport-empreinte-memoire.md.

[1] moe — Objet : regrouper les experts d'un MoE (fréquence vs co-activation) réduit-il les nœuds lus par jeton (moe:1-8). Chiffres : 128 experts, 8/jeton (moe:3) ; ~1 600 jetons, 48 couches (moe:37) ; 4/8/16 clusters → couverture 0,799/0,607/0,442, ventilation 1,94/3,08/4,46 ; hasard 0,440/0,319/0,250 et 3,59/5,32/6,55, gain ×1,8-1,9 (moe:41-43) ; accord co-activation vs tri fréquence 1,000 (moe:47) ; 3,08 au lieu de 5,32, ÷1,7 ; 4 nœuds 1,94 (moe:58-60) ; 3,20 Go au lieu de 18,56, 625 ms au lieu de 3,9 s, 1 587 tenseurs (moe:105-106). MESURÉ vs DÉDUIT/À FAIRE : négatif mesuré (moe:45-50) ; équilibrer par usage = « autre mesure » (moe:61-65) ; format « esquisse, à confronter » (moe:67) ; gpt-oss en cours, V4.1/Kimi/GLM en téléchargement (moe:86-89) ; coût déséquilibre « mesuré nulle part ici » (moe:95) ; traîne non couverte (moe:96-98). PLAGES vs CLUSTERS : 48 couches (moe:37), index par couche (moe:73), AUCUNE plage a:b ; clusters d'EXPERTS (moe:24-32, 58, 76-79).

[2] v41 — Objet : V4.1 découpé à la couche 20 = état identique au bit près (v41:1-9). Chiffres : 365,71 Go, 40 couches (v41:3-4) ; écart 7,05e-1 (v41:7) ; 514 722,06 vs 1 743 713,62 (v41:15) ; 208 411,867 en 16 bits (32 767) vs 8 bits (127) (v41:16) ; avant 629/953 (319+310+0), après 0/953, moteur 0/945, réf. 0/1 591 ; 2 544 = 1 591 + 953 (v41:26-39) ; 0,000e+00 sur 5 120 valeurs (v41:50) ; 20 480 f32 (v41:57) ; 1 743 713,6243 en 68,0/51,3 s, 82 016 o / 81 999 o / 3 flux (v41:82-86) ; pré-mix 0,02 % (v41:88-89) ; V4-Flash 0,00e0 (v41:96) ; 16 vs 8 bits : 2 443 diff., 1,793e-3 (v41:110) ; modes 3/4/2 = 0,00e0 / 4,45e-3 / 3,65e-2 (v41:134-141) ; porte 20 s sur 0,5 B (v41:175). MESURÉ vs À FAIRE : correctif mesuré 2× (v41:79-86) ; aucun test auto sur 365 Go (v41:171-176) ; YaRN, mesure contexte long « reste à faire » (v41:178-180). PLAGES vs CLUSTERS : PLAGES 0-19/20-39 (v41:26-28, 33, 153), 12 locales (v41:163), dense f32 (v41:85, 139), --dense (v41:108-112) ; AUCUN cluster d'experts (v41:116-118).

[3] morc — Objet : l'élagage par fréquence mesurée garde-t-il les qualités (morc:1-11). Chiffres : 48 couches, 128 experts, 8/jeton (morc:14) ; 384 jetons (morc:15-16) ; 18 432 lignes (morc:18) ; 128→100 %→9,584 ; 96→99,6 %→11,327→+18,2 % ; 64→94,3 %→12,515→+30,6 % ; 32→74,2 %→18,605→+94,1 % (morc:26-31) ; 18 % pour 0,4 % de masse (morc:36-37) ; 2 × 16 Go PCIe (morc:74) ; K3 896 experts/couche (morc:82) ; ISTA-DASLab 256/512, 91,3 % SWE-bench (morc:46-47). MESURÉ vs À FAIRE : leave-one-out proposé non mesuré (morc:52-61) ; « à mesurer ensuite » (morc:78-84) ; « à vérifier plutôt qu'à supposer » (morc:84-86). PLAGES vs CLUSTERS : couche par couche (morc:3-4, 66-67) ; AUCUNE plage a:b ; AUCUN cluster.

[4] dig — Objet : digeste tenseur par tenseur (dig:1-6). Chiffres : 2 544 fichiers/passe (dig:4) ; 953/629/1.132e+02 avant (dig:143) ; 953/0 et 1 591/0 et 945/0, 0.000e+00 (dig:43, 72, 111) ; 16 vs 8 bits : 2 544/2 443/4.334e+03 (dig:186) ; --dense 2 544/0 (dig:225) ; sans engram 2 528/2 431/8.406e+03 (dig:264) ; 0.000e+00 sur 5 120 valeurs (dig:304-306). MESURÉ : tout ; attribution par relecture adverse (dig:8-17). PLAGES vs CLUSTERS : 0-19 (dig:42), 0-39 (dig:71), 20-39 (dig:110), couches-locales 20 (dig:30), --dense (dig:224) ; AUCUN cluster d'experts.

[5] lect — Objet : modèle éclaté commun.gguf + 8 cluster-XX.gguf lu comme un seul (lect:1-11). Chiffres : origine 15,2789 (12,2 s) vs clusters 15,2789 (11,6 s), 63 jetons (lect:23-26) ; V4-Flash 86,9 Go/3 shards, 1 328 tenseurs 0/784/544, 54 ms (lect:32-40) ; 9 fichiers, 1 587 tenseurs, 18,55 Go, 48 couches/27,8 s, 48/48 MoE (lect:54-58) ; portes 19,3885 / 15,1757 / 15,2789 / 268 786,6218, 32 verts (lect:64-68) ; NaN et 3,19 Go pour 18,55 (lect:80, 92-93) ; mmap 9,32 s/6,35 Go vs 30,68 s/19,20 Go, ppl 799,8557 (lect:177-182) ; nœud partiel 1→268 786,62/2,35 Go/9,64 s ; 2→63 780,09/2,83 Go ; 4→3 378,91/4,60 Go ; 8→799,8557/6,28 Go/10,65 s (lect:199-204), 2,7× (lect:206, 212) ; 435+8×144=1 587, 18,60 Go, 351,7 s, mapping 6 144 entrées/48 couches/128 experts/8 clusters (lect:239-242) ; --lot 64 = 15,2736 vs 15,2789 (lect:263-264). À FAIRE : sommer les contributions entre nœuds (lect:259-262), mmap (lect:267-268), biais refusés (lect:269). PLAGES vs CLUSTERS : UNIQUEMENT clusters d'experts (DRAVE_CLUSTERS lect:125,193) ; AUCUNE plage de couches.

[6] Satellites, chiffres MESURÉS de clusters : rout:65 799,8557→799,8557 au bit près ; rout:75 799,8557→799,8152 (−0,005 %) ; opt:135 Qwen 19,3885 et clusters 799,8557 inchangées, 35 tests ; port:28 P6 « découpage en grappes » TENUE (799,8557 ; V4.1 0,00e0) ; coh:159 48 tests, 19,3885, clusters 799,8557, formats 17/0/0 ; coh:43-44 origine 15,2789 = clusters 15,2789 ; mla:98-100 19,3885 + 799,8557, 48 tests ; v4r:57-65 86,9 Go → commun + 8 clusters, 11 008 entrées (43 couches × 256 experts), 450 s, 8 430,2968 (111,8 s) vs 8 430,2968 (39,9 s), 2,8× (v4r:67-70) ; mat:72-75 86,9 Go, 11 008 entrées, --ppl-reparti 0,00e0. Tous = clusters d'experts/fichiers, AUCUNE plage de couches.

[7] Rapports documentant des PLAGES DE COUCHES mesurées : ph3 pilote 0..12 / moteur 12..24, Qwen2.5-0.5B ctx 256 : 144,8289 ; avant 1 621,7239 (×11,2) ; norme seule 693,4492 (×4,8) ; après plage 144,8289/144,8289/0,00e0 (ph3:42-46) ; 40/200/1 024 jetons, 1 023 flux, 9,5146 des deux côtés, 19,4 vs 19,7 ms/jeton (ph3:50-53) ; aucun cluster. k3 « un nœud = une plage de couches », --couches a:b (k3:409-416) ; coupe couche 13 : 0..12 / 13..25 / 0..25, B et C identiques au BIT, 4 jetons, 28 672 octets (k3:440-447) ; relais 114 688 o + pile 229 376 o (k3:431-432) ; loi octets(T)=79,0+31,9·T Gio, 3 nœuds 68,9 Gio/8,8 min, 11 nœuds 18,8 Gio/2,4 min (k3:457-467) ; aucun cluster. emp experts pour 90 % : couches 0-3 = 75 à 82, couches 16-30 = 42 à 49, +1,2 % au mieux (emp:372-373, 378).

[8] Homonymes « grappes » (grappes:1,4,18 ; modele-reel:49-51 ; programme-evolutif:38,47,95 ; inference:283 ; valeur-unaire:60 ; campagne-parcimonie:74 ; empreinte:15) = grappes de neurones/co-activation ou sous-modèles, pas de chiffre de clusters de fichiers MoE.

VERIF: lus intégralement — moe (117), v41 (180), morc (86), dig (311), lect (269) = 963 l. ; extraits grep/sed — rout (170), opt (135), port (77), coh (170), mla (237), v4r (92), mat (94), ph3 (66), k3 (490), emp (545), grappes (62), modele-reel (83), programme-evolutif (138), inference (344), valeur-unaire (104), campagne-parcimonie (91). Glob reports/*cluster* → 0. Aucun fichier modifié, rien compilé/testé.

### 🤖 Assistant

⏵ Vérification des nouvelles citations (v4-reparti, phase3, k3-disque)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && sed -n '55,72p' rapport-v4-reparti.md; echo \"=== PH3 40,55 ===\"; sed -n '40,55p' rapport-phase3-reparti.md", "description": "Verify v4-reparti and phase3 figures"}`

  ```
`tools/convertir_clusters.py` a découpé les 86,9 Go de V4-Flash en
`commun.gguf` + 8 `cluster-XX.gguf` (11 008 entrées de mapping : 43 couches ×
256 experts), en 450 s et **sans requantifier un octet**. Le moteur ouvre le
dossier, lit le manifeste, et retrouve **exactement** la perplexité de
l'original :

| | perplexité (4 jetons notés, ctx 32) | temps |
|---|---|---|
| original (3 tranches, 86,9 Go) | **8 430,2968** | 111,8 s |
| éclaté en 8 grappes | **8 430,2968** | **39,9 s** |

Le gain de temps n'est pas un effet de cache : chaque expert routé vit dans UN
fichier de grappe, donc le nœud ne lit que ce qu'il sert — c'est le mécanisme
décrit dans `docs/format-clusters.md`, et il vaut ici **2,8×** sur un modèle dont
les experts pèsent 80 % du fichier.

Trois bugs d'outillage ont été trouvés et corrigés pour y arriver (le
=== PH3 40,55 ===
## Les trois états, mesurés

| état | locale | répartie | écart |
|---|---|---|---|
| avant correction | 144,8289 | 1 621,7239 | ×11,2 |
| après la norme seule | 144,8289 | 693,4492 | ×4,8 |
| après la plage de couches | 144,8289 | **144,8289** | **0,00e0** |

Égalité exacte, et pas seulement petite : le transport est du f32, donc rien
n'est arro
… [386 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && sed -n '405,420p' rapport-passe-k3-disque.md; echo \"=== 438,470 ===\"; sed -n '438,470p' rapport-passe-k3-disque.md", "description": "Verify k3 range figures"}`

  ```
par une mesure plutôt que par une hypothèse.

---

## 12. Chantier 3 : un nœud = une plage de couches, et la porte est TENUE

### 12.1 Ce qu'il fallait transporter, et pourquoi c'était le point dur

`passe_complete` calculait toujours les couches `0..n`. Pour qu'un processus
devienne **un nœud**, il fallait deux choses :

1. **une plage** `debut..fin` — c'est fait, par le drapeau `--couches a:b` qui
   veut déjà dire « plage de couches » partout ailleurs dans ce moteur ;
2. **un relais** entre nœuds — et ce n'est PAS seulement le flux résiduel.

Le modèle empile une **banque** toutes les 12 couches : à chaque couche `l % 12 == 0`,
=== 438,470 ===
### 12.2 La porte : bit à bit, en traversant une banque

`tools/test-plage-k3.sh` coupe à la **couche 13** — donc **après** la banque de la
couche 12, là où un découpage naïf se trompe.

| étape | couches | ce qui est vérifié |
|---|---|---|
| **A** | 0..12 | écrit le relais : *« reprend à la couche 13 · 4 jetons × 7 168 canaux · 2 banque(s) »* |
| **B** | 13..25 | repart du relais A |
| **C** | 0..25 | le monolithe |
| **comparaison** | couche 25 | **B et C identiques au BIT, 4 jetons, 28 672 octets chacun** |

```
PORTE TENUE : le découp
… [708 caractères tronqués]
  ```

### 👤 Utilisateur

Background subagent a9e308b7-5d50-4bb3-8e31-4c8e6f261a6d finished and will do no further work unless you send it more.
Its closing message:
⏵ Complément livré au parent

Condensé étendu (≤55 lignes) fourni ci-dessus avec `fichier:ligne` partout, et transmis au parent. Points saillants du complément :

- `rapport-lecteur-multifichiers.md` : clusters d'experts/fichiers uniquement (15,2789 ; 268 786,62 ; 799,8557 ; table « nœud partiel » 1→8 clusters), **aucune** plage de couches ; « ce qui n'est pas fait » = sommer les contributions entre nœuds (lect:259-262).
- Satellites clusters mesurés : rout:65,75 ; opt:135 ; port:28 ; coh:43-44,159 ; mla:98-100 ; v4r:57-70 ; mat:72-75 — tous des clusters d'experts.
- Plages de couches réellement mesurées : ph3:42-53, k3:409-467 (`--couches a:b`, porte bit à bit à la couche 13), emp:372-378.
- `reports/*cluster*` : inexistant ; `DRAVE_CLUSTERS` seulement dans lect:125,193 ; les autres hits « grappes » sont un objet distinct (neurones/co-activation).
- VERIF incluse : 5 fichiers lus intégralement (963 l.) + 16 en extraits ciblés ; lecture seule respectée.

### 🤖 Assistant

⏵ Vérification du script de porte k3 et de son rattachement à portes.sh

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la tools/test-plage-k3.sh 2>&1; grep -n \"test-plage\\|plage\" tools/portes.sh | head; echo \"--- exit grep: $? ---\"; grep -n \"couches\\|relais\" tools/test-plage-k3.sh 2>/dev/null | head -20", "description": "Check k3 plage te … [18 caractères tronqués]`

  ```
-rwxr-xr-x. 1 stephane stephane 2331  7 oct 20:29 tools/test-plage-k3.sh
--- exit grep: 0 ---
9:#   A : couches 0..12   -> relais (flux + pile)
10:#   B : couches 13..25  <- relais A
11:#   C : couches 0..25   (monolithe)
20:R=/tmp/plage_relais.bin
24:echo "##### A : couches 0..12" | tee -a "$J"
26:    $D "$K" --k3-essai --couches 0:13 2>&1 | grep -E "plage|relais|passe " | tee -a "$J"
29:echo "##### B : couches 13..25, à partir du relais A" | tee -a "$J"
31:    $D "$K" --k3-essai --couches 13:26 2>&1 | grep -E "plage|relais|passe " | tee -a "$J"
34:echo "##### C : couches 0..25 (monolithe)" | tee -a "$J"
36:    $D "$K" --k3-essai --couches 0:26 2>&1 | grep -E "plage|passe " | tee -a "$J"
  ```

### 🤖 Assistant

⏵ Contrôle du point sensible : la porte 799,8557 après le correctif de routage

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '58,90p' reports/rapport-routage-experts.md", "description": "Read routing report gate impact"}`

  ```
biais de gpt-oss ne départage que la **sélection** et n'entre pas dans les poids.

## 3. Ce qui est mesuré, et ce qui a bougé

| porte | avant | après | verdict |
|---|---|---|---|
| Qwen2.5-0.5B Q8_0 ctx 256 (dense) | 19,3885 | **19,3885** | inchangée, au bit près |
| Qwen3-30B clusters ctx 64, 8 jetons | 799,8557 | **799,8557** | inchangée, au bit près |
| gpt-oss-120b ctx 256 | 15,1757 | **15,6017** | **changée** — voir ci-dessous |

Le changement de gpt-oss est le seul effet visible sur les portes, et il est
justifié par le code de référence : `build_moe_ffn` de llama.cpp met le biais
dans `selection_probs` (la sélection) mais prend les poids dans `probs`
(`softmax(logits[choisis])`, **sans** biais). L'ancien code laissait le biais
dans le softmax. **15,1757 était auto-cohérent, pas juste.**

Au passage, une leçon de méthode : réunir les deux chemins de routage a d'abord
déplacé la porte Qwen3-30B de 799,8557 à 799,8152 (−0,005 %). Cause : la
renormalisation était écrite `x / s` au lieu de `x * (1/s)`, ce qui n'est pas le
même flottant au dernier bit, et 48 couches l'amplifient. La comparaison
**ancien binaire / nouveau binaire sur le même modèle** (un `git worktree` sur
le com
… [443 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Complément transmis au parent (plages mesurées, porte K3 non câblée)

- **send_message** `{"agent_id": "482522d1-31f1-43eb-ae9c-a681336404f7", "message": "ADDENDUM au condensé (vérifié moi-même après le rapport étendu du sous-agent) — 4 points qui complètent, rien à corriger :\n1. Plages de couches réellement mesurées, en plus de V4.1 : reports/rapport-phase3-reparti.md:42-53 — pilote 0. … [1704 caractères tronqués]`

  ```
message delivered to agent 482522d1-31f1-43eb-ae9c-a681336404f7
  ```

### 🤖 Assistant

⏵ Condensé consolidé — clusters et plages de couches (lecture seule, rien modifié)

**1) Tableau** — état : P = vérifié par une porte, M = mesuré localement (rapport/REPRISE), D = déduit du code.

| capacité | ce qu'elle fait | fichier source | état | chiffre mesuré |
|---|---|---|---|---|
| Lecteur clusters + mmap | commun.gguf + cluster-XX.gguf réunis en un `Gguf` ; experts sous `cl{c}/` ; `mapping.tsv` lu d'un bloc ; fichiers mappés | `clusters.rs:150-297` · `gguf.rs:153-170, 478-520` | P (porte 1 : 6 tests `clusters.rs:309-505` ; porte 3) | 9 fichiers · 1 587 tenseurs · 18,55 Go ; mmap 9,32 s / 6,35 Go contre 30,68 s / 19,20 Go |
| Nœud partiel | `DRAVE_CLUSTERS=0,3` ; demandé-absent = erreur ; incomplet refusé sans `DRAVE_CLUSTERS` | `clusters.rs:167-176, 239-273, 291-295` | M | 1 cl. 2,35 Go / 268 786,62 · 4 cl. 4,60 Go / 3 378,91 · 8 cl. 6,28 Go / 799,8557 |
| Porte clusters | dossier complet Qwen3-30B 8 clusters, mêmes jetons | `tools/portes.sh:55-61` | P (799,8557 revérifié au bit près après le correctif de routage : `rapport-routage-experts.md:65-77`) | attendu 799.8557 |
| Convertisseur experts | GGUF → commun + 8 clusters + `mapping.tsv` + `manifeste.json`, copie d'octets sans requantification | `convertir_clusters.py:402-582` | M | Qwen3-30B : 435+8×144 = 1 587 tenseurs · 18,60 Go · 351,7 s · SHA-256 « TOUT CONCORDE » ; V4-Flash : 86,9 Go, 11 008 entrées, 450 s, 8 430,2968 = 8 430,2968 (39,9 s contre 111,8 s, 2,8×) |
| Conversion par plages de couches | `--mode couches` : blocs `blk.N` en groupes contigus (dense), sans `mapping.tsv` | `convertir_clusters.py:446-463, 520-529` | M | Qwen2.5-0.5B : commun + 4 fichiers × 6 couches · 290 tenseurs |
| Plage de couches moteur | `couche_debut..couche_fin` = [a,b) exécutée ; hors plage → flux brut | `model.rs:2551-2569, 4368-4369, 6641-6646, 6904-6905` | M (V4.1 + phase 3), aucune porte dans `portes.sh` | V4.1 : 0,00e0, 1 743 713,6243 (51,3 s / 68,0 s) ; phase 3 : 144,8289 = 144,8289, 0,00e0, 1 023 flux, 9,5146 |
| Porte de plage K3 | `--k3-essai --couches 0:13 / 13:26 / 0:26` ; coupe après la banque de la couche 12 | `tools/test-plage-k3.sh:1-36` · `main.rs:147, 2131-2134, 2144` | porte TENUE mais NON câblée dans `portes.sh` | B et C identiques au bit · 4 jetons · 28 672 octets |
| Réparti pilote/pair | `--couches-locales N` : local [0,N), pair [N,n_layer), plage dans l'en-tête | `main.rs:3345, 3430, 3457-3460, 3549, 3204-3213` | M | écart 0,00e0 dense (`REPRISE.md:1307-1316`) |
| Outils d'analyse | co-activation/ventilation MoE, union d'experts lus, jumeaux statiques, localité (R²) | `clusters_moe.py` · `analyse_union_experts.py` · `analyse_experts_statique.py` · `localite_couches.py` | M hors moteur | couverture 0,799/0,607/0,442 ; hasard 0,440/0,319/0,250 |

**2) Ce que le format change / reste à faire**
- Fichiers : commun + N clusters + `mapping.tsv` + `manifeste.json` ; source 18,56 Go → commun 1,00 Go + cluster 2,20 Go ; surcoût = métadonnées dupliquées 8×~4 Mo = 0,2 % (`docs/format-clusters.md:80-89`).
- Partagé : routeur `ffn_gate_inp` (`clusters.rs:9-11`) ; expert partagé `ffn_*_shexp` (2D, ne matche pas « _exps. ») → `convertir_clusters.py:428`, `model.rs:695-713`. Biais d'experts + clusters = **refusé par panic** (`model.rs:791-796`).
- Jointure : TSV 4 colonnes, 6 144 lignes pour 48×128 (`rapport-lecteur-multifichiers.md:240`) ; `local[couche][global]=cluster×65536+ligne` (`clusters.rs:103`), publié en `OnceLock` après ouverture réussie (`clusters.rs:291-295`) ; `Moe::ou` traduit puis cherche le n° parmi les vues chargées (`model.rs:1299-1311`) ; les 3 projections doivent porter les mêmes clusters (`model.rs:717-731`).
- À faire : sommer les contributions entre nœuds (`docs/format-clusters.md:175-178`) ; découper les biais ; équilibrer par charge (`:187-189`) ; manifeste binaire si un fichier par expert (`:185-186`).

**3) Sémantique exacte**
- `--couches a:b` : `main.rs:706-712` — exige « a:b » (sinon panic), `a`/`b` en `usize` par `parse().unwrap()` ; **aucun contrôle de bornes**. Report `model.rs:4368-4369` : `couche_debut=a`, `couche_fin=b` ; doc « dernière couche PORTÉE (exclue) » (`:2551-2554`) → **[a,b)** ; boucles `for l in couche_debut..couche_fin` (`model.rs:6904`, aussi 4751, 5345, 6562). a inclus, b exclu.
- `b == n_layer` → norme finale + tête (`model.rs:6641-6646`) ; `b < n_layer` → flux brut (`:5740, 7745-7752`), sauf `--tete-partielle` (modèle TRONQUÉ, annoncé, `main.rs:423-435`).
- Refus : `a>=b` et `b>n_layer` **ne sont pas refusés** par le moteur principal — `a>=b` = boucle vide silencieuse ; `b>n_layer` = `layers[l]` indexé directement (`model.rs:6905`) → panique d'index. Gardes existants : `--k3-essai` (`main.rs:2131-2134`, « plage {debut}:{fin} invalide pour {n} couche(s) ») et le serveur de flux (`main.rs:3210-3213`, flux refusé, nœud vivant).
- Reprise à `a>0` sans flux : V4.1 avertit « convention de sonde, copie 0 » (`model.rs:6791-6800`) ou assert si flux brut sans `pre` (`:6787-6790`) ; un manque d'architecture n'est retiré que dans [a,b) (`:3485-3500`).
- `--plage` **n'existe pas** comme option CLI (grep `"--plage"` = 0) ; c'est le concept, `--k3-essai` réutilise `opt.couches` (`main.rs:147, 1899`).
- `--couches-locales N` : `main.rs:705`, défaut 12 si 0 (`:3345`) ; pilote `couche_fin=N`, `couche_debut` reste 0 (`:3430`) → [0,N) ; l'en-tête porte `debut=N, fin=n_layer` (`:3457-3460, 3549`) → pair exécute [N,n_layer), revalidé (`:3210`). Aucun contrôle `N ≤ n_layer` (D).

**4) Mesuré / déduit / supposé**
- Mesuré et gardé : 799,8557 (porte 3, dossier complet, ctx 64, 8 ids → 7 jetons ; inchangée après le correctif de routage, épisode transitoire 799,8152 dû à `x/s` au lieu de `x*(1/s)`, `rapport-routage-experts.md:65-77`) ; 6 tests unitaires `clusters.rs` via la porte 1 (`portes.sh:32-44`). **Aucune porte dans `portes.sh`** ne couvre `DRAVE_CLUSTERS`, `--couches a:b` ni `--couches-locales` ; la porte de plage K3 (`tools/test-plage-k3.sh`) est un script séparé.
- Mesuré une fois, non gardé : nœud partiel 1/2/4/8 clusters (`rapport-lecteur-multifichiers.md:199-204`) ; 15,2789 = 15,2789 sur 63 jetons (`docs/format-clusters.md:116`) ; V4-Flash éclaté = 8 430,2968 (`rapport-v4-reparti.md:55-70`) ; phase 3 répartie 0,00e0 (`rapport-phase3-reparti.md:42-53`) ; conversion, mmap, mesures Python.
- Déduit du code, non mesuré : absence de refus pour `a>=b`, `b>n_layer`, `N>n_layer` ; boucle vide silencieuse.
- Supposé / à faire : « la somme inter-nœuds rendrait 799,8557 pour 4,60 Go par nœud » est un calcul, pas une mesure (`rapport-lecteur-multifichiers.md:209-210`) ; biais refusés ; équilibrage par charge non fait ; loi `octets(T)=79,0+31,9·T` Gio et projections 3/11 nœuds (`rapport-passe-k3-disque.md:457-467`) = extrapolation sur bande disque.
- Aucun `reports/*cluster*` : les rapports réels sont `rapport-lecteur-multifichiers.md`, `rapport-decoupage-moe.md` (clusters d'experts), `rapport-decoupage-v41.md`, `decoupage-v41-digest.txt`, `rapport-phase3-reparti.md` et `rapport-passe-k3-disque.md` (plages de couches). Les homonymes « grappes » (neurones/co-activation) sont un autre objet.

