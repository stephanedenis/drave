//! drave-core — moteur d'exécution par listes d'événements.
//!
//! Usage :
//!   drave-core <modele.gguf> [--matrix blk.0.ffn_gate.weight] [--threads 8]
//!
//! Mesure sur le VRAI modèle :
//!   1. taille exacte de chaque encodage de liste (bits/poids),
//!   2. débit du moteur d'événements selon la densité des activations,
//!   3. exécution sans multiplieur (décalages + additions) vs multiplication.

/// Variables d'environnement que le moteur lit, **sans** le préfixe `DRAVE_`.
///
/// Sert à traduire un ancien nom `QT_*` resté dans un script, et à rien d'autre.
/// Le test `les_vars_lues_sont_completes` vérifie cette liste contre le source :
/// une variable lue mais absente d'ici rendrait le message muet, et une variable
/// listée mais jamais lue annoncerait une option qui n'existe pas.
const VARS_LUES: &[&str] = &[
    "BANC_KV_DEBUG", "BANC_KV_GPU_SEUL", "BANC_KV_GRAD", "BANC_KV_K0",
    "BANC_KV_KUNIT", "BANC_KV_UNIT", "BANC_KV_V1", "BANC_SANS_PUITS",
    "CLUSTERS", "DEBUG_ETAT", "DEBUG_FLUX", "DEBUG_MLA", "DEBUG_FUSION", "DEBUG_YARN",
    "DUMP_COUCHES",
    "ETAT_ENTREE",
    "FLUX_VERIF", "GPU", "GPU_EXPERTS",
    "GPU_EXPERTS_GO", "GPU_KV", "GPU_TETE", "GPU_TOPK", "HARMONY_TRACE",
    "KV_BITS", "KV_F16", "KV_K_F16", "KV_K_F32", "KV_V_F32", "MMAP",
    "BIAIS_VL", "EXPERTS_RAM", "PRELIRE", "PRELIRE_TOUT", "Q8_BLOCS", "SANS_ENGRAM",
    "SANS_EMPRUNT",
    // S4 (docs/strata-pour-drave.md) : la prélecture des experts. `PRELIRE` coupe tout
    // (c'est le bras « à la demande » de `tools/porte-prechargement.sh`) ; `PRELIRE_FILS`
    // choisit le nombre de fils qui entrent les pages (0 = l'ancien `madvise`) ;
    // `PRELIRE_TRANCHE` garde l'ancienne granularité pour refaire la mesure qui a montré
    // qu'elle ne changeait rien ; `PRELIRE_DENSE` rallume la prélecture de la couche
    // suivante, mesurée sans gain (le témoin reste pour pouvoir la re-mesurer).
    "PRELIRE_FILS", "PRELIRE_TRANCHE", "PRELIRE_DENSE",
    // 12/10 : la lecture SÉQUENTIELLE dans nos tampons (directive « granularité fine de MoE,
    // allocation intelligente au lieu de virtualiser »). `TAMPONS` l'allume, `TAMPONS_FILS`
    // choisit le nombre de fils de lecture.
    "TAMPONS", "TAMPONS_FILS",
    // 13/10 : la forme « listes » est construite À LA DEMANDE (6,1 s à 19,3 s gagnés par
    // chargement) ; `PUSH_TOT` rallume l'ancien comportement pour refaire la mesure.
    "PUSH_TOT", "PUSH_FAUX",
    // M9 : rallume un compteur d'occupation PARTIEL (l'attention seule) — c'est le défaut que la
    // ligne « occupation des poids » répare, et la porte doit pouvoir le voir.
    "OCCUPATION_ATTENTION_SEULE",
    "POIDS_CREUX", "CREUX_SANS_EFFET", "CREUX_DEBUG",
    "TRACE_BLOCS", "TUILE_LOT", "K3_COUCHES", "K3_SANS_ETAT", "K3_PASSE", "K3_TETE", "K3_LOGITS", "K3_GEN", "K3_MXFP4", "K3_TRACE_EXPERTS", "K3_IDS", "K3_DENSE_FIGE", "K3_STATS_EXPERTS", "K3_RELAIS_ENTREE", "K3_RELAIS_SORTIE", "HEBB_SEUIL", "HEBB_SIGNE", "HEBB_DECROI", "HEBB_SAUVER", "HEBB_CHARGER",
    // E7/E8 (docs/impulsion-pure-apprenant.md) : modulation par nouveauté,
    // décorrélation anti-Hebbienne, et la persistance de `D` sans laquelle le
    // test hors échantillon n'est pas possible. Le test qui exige cette liste
    // a d'ailleurs attrapé les deux dernières à la première compilation.
    "HEBB_MODULE", "HEBB_DECORRELE", "HEBB_D_CHARGE", "HEBB_D_SAUVE",
    "HEBB_MODULATEUR_FICHIER", "HEBB_BETA", "K3_PRELIRE_UNION", "EXPERTS_GARDES", "K3_IMPOSE",
    "SANS_BLOCS", "SANS_COMPRESSION", "SIMD_DOT", "TRACE_EXPERTS", "V41_SANS_RETARD",
    "V41_TETE_COPIE0",
    "VISION_TEXTE",
    "YARN",
    "YARN_MSCALE", "YARN_NON",
    "YARN_RAMPE",
];

mod clusters;
mod kimi_k3;
mod engine;
mod engram;
mod formats;
mod gguf;
mod list;
mod materiel;
mod model;
mod gpu;
mod tokenizer;
mod topologie;
mod trace_globale;
mod episodique;
mod bus;

use engine::{matvec_dense, matvec_shift_add, Pool, SparseVec};
use gguf::Gguf;
use list::{dense_bits, BitmapSign, DenseQ4, DenseQ8, FusedSign, PushMat, SignedDelta, SparseK};
use std::time::Instant;

fn fmt_bits(b: u64, n: usize) -> String {
    format!("{:8.3} b/poids  ({:7.2} Mo)", b as f64 / n as f64, b as f64 / 8.0 / 1e6)
}


/// **Le rapport de l'adaptateur hebbien différentiel, en UN SEUL endroit.**
///
/// Il était posé dans `run_infer` seulement : en `--ppl` il ne s'imprimait pas,
/// donc `D` n'était jamais sauvé, donc le test hors échantillon chargeait un
/// adaptateur NUL et rendait deux perplexités identiques. Un moteur à deux
/// chemins qui doivent porter la même chose finit par n'en porter qu'un — et le
/// défaut est silencieux. Cette fonction est la réponse : les deux modes
/// l'appellent, et il n'y a plus deux endroits à tenir d'accord.
fn rapport_hebb_diff(mdl: &model::Model) {
    let Some(hd) = mdl.hebb_diff.as_ref() else { return };
    let norme: f64 = hd.d.iter().map(|v| (*v as f64) * (*v as f64)).sum::<f64>().sqrt();
    let part = 100.0 * hd.n_evenements as f64 / hd.n_canaux.max(1) as f64;
    println!("[hebb-diff] couche {} : {} pas · ‖D‖ = {:.4e} · somme des ‖ΔD‖ = {:.4e} · \
{} canaux-événements sur {} vus ({:.2} %)",
             hd.layer, hd.pas, norme, hd.norme_maj, hd.n_evenements, hd.n_canaux, part);
    if let Ok(c) = std::env::var("DRAVE_HEBB_SAUVER") { hd.sauver(&c); }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        eprintln!("usage: drave <modele.gguf|dossier-de-clusters> [--matrix NOM] [--threads N]");
        eprintln!("       drave <modele> --infer (--ids 1,2,3 | --prompt TEXTE | --ids-file F)");
        eprintln!("             [--n 32] [--temp 0] [--ctx 512] [--threads N]");
        eprintln!("       drave <modele> --ppl FICHIER-IDS [--ctx N] [--limit N] [--dense]");
        eprintln!("       drave --fusionner-trace T1 T2 [...] [--fusion-sortie F]");
        eprintln!("                                     fusionne des traces de plusieurs processus,");
        eprintln!("                                     ordonnées par le TEMPS MURAL, mesure la");
        eprintln!("                                     dérive des horloges et confronte les deux");
        eprintln!("                                     bouts de chaque lien. Ne charge aucun");
        eprintln!("                                     modèle.");
        eprintln!("       drave <modele> --reflexe-essai N [--ids-file F]");
        eprintln!("                                     RÉFLEXE (C8) : un modèle TRONQUÉ à L");
        eprintln!("                                     couches, tête appliquée à la fin de la");
        eprintln!("                                     plage. Mesure l'accord de sa décision avec");
        eprintln!("                                     celle du modèle entier, par profondeur :");
        eprintln!("                                     combien de couches pour qu'un réflexe");
        eprintln!("                                     tombe d'accord ?");
        eprintln!("       drave <modele> --episodique-essai N [--episodique-k K]");
        eprintln!("             [--episodique-fichier F] [--ids-file F]");
        eprintln!("                                     mémoire ÉPISODIQUE (C6) : collecte N états");
        eprintln!("                                     réels du modèle, les écrit une fois, puis");
        eprintln!("                                     mesure le rappel par contenu selon le nombre");
        eprintln!("                                     d'épisodes et la dégradation de l'indice.");
        eprintln!("       drave <modele> --entree signal:F --sortie G [--delai N] [--recurent]");
        eprintln!("             [--entree-canal K] [--entree-gain X] [--entree-jeton N]");
        eprintln!("             [--entree-memoire K] [--memoire K --sortie-memoire H]");
        eprintln!("             [--recurrence α]");
        eprintln!("                                     PÉRIPHÉRIE (C8) : une région frontière");
        eprintln!("                                     reçoit un SIGNAL (une valeur par ligne) au lieu");
        eprintln!("                                     d'un jeton, et écrit l'état de chaque pas. Le");
        eprintln!("                                     délai est DANS le moteur (`v[t-N]`), `--recurent`");
        eprintln!("                                     garde l'historique (positions croissantes),");
        eprintln!("                                     `--entree-memoire K` pose les K dernières valeurs");
        eprintln!("                                     sur les canaux suivants (un signal VECTEUR),");
        eprintln!("                                     `--memoire K --sortie-memoire H` retient les K");
        eprintln!("                                     derniers signaux HORS du réseau (exact, gratuit en");
        eprintln!("                                     paires), et `--recurrence α` réinjecte la sortie");
        eprintln!("                                     du pas précédent (C2 : mesuré NUISIBLE non");
        eprintln!("                                     entraînée — reports/rapport-c2-recurrence.md).");
        eprintln!("                                     Affiche les paires (poids × activation) par");
        eprintln!("                                     DÉCISION : la métrique du plan.");
        eprintln!("       drave <modele> --tensors      inventaire par les en-têtes seuls");
        eprintln!("       drave <modele> --materiel     détection matérielle et plan de");
        eprintln!("                                     configuration, AVEC la raison de chaque");
        eprintln!("                                     choix — ne charge pas le modèle");
        eprintln!("       drave <modele> --sonder-engram N   accès mmappé à une table d'engram");
        eprintln!("       drave <modele> --tete-restreinte F  génération CONTRAINTE : la tête ne");
        eprintln!("                                     calcule que les tokens de F. Change la");
        eprintln!("                                     sortie — refusé en perplexité.");
        eprintln!("       (un dossier contenant commun.gguf EST un modèle ; DRAVE_CLUSTERS=0,3");
        eprintln!("        ne charge que certains clusters ; DRAVE_MMAP=0 lit au lieu de mapper)");
        std::process::exit(1);
    }
    // Une seule analyse, puis un aiguillage : `--plan`, `--tokenize`,
    // `--ppl`/`--ppl-texte` et `--infer` partagent désormais la même structure
    // d'options, donc les mêmes drapeaux.
    // Les variables d'environnement ont été renommées QT_* -> DRAVE_* : un
    // ancien nom encore présent dans un script ne ferait RIEN, en silence. On le
    // dit, plutôt que de laisser croire que l'option est active.
    //
    // Ce qu'on ne fait PLUS : chercher un nom qui « commence par QT_ ». C'était
    // faux — Qt pose `QT_IM_MODULE=xim` et `QT_IM_SWITCHER=imsw-multi` dans
    // toute session graphique, donc le binaire avertissait à CHAQUE lancement
    // d'une variable qui n'a jamais été à nous, et `find` n'en rendant qu'une, un
    // vrai nom hérité passait inaperçu derrière. On ne signale que la traduction
    // exacte d'une variable que le moteur lit vraiment.
    let vieux_nom = std::env::vars().map(|(k, _)| k).find(|k| {
        k.strip_prefix("QT_").map(|s| VARS_LUES.contains(&s)).unwrap_or(false)
    });
    if let Some(vieux) = vieux_nom {
        eprintln!("[attention] {vieux} est l'ancien nom d'une variable d'environnement : \
il faut écrire DRAVE_{} (voir docs/histoire.md). Rien n'a été appliqué.", &vieux[3..]);
    }
    // ---- C12bis : la FUSION de traces passe avant tout le reste elle aussi, et
    // pour la même raison que la topologie : elle ne touche à AUCUN modèle. Exiger
    // un fichier de poids pour relire trois traces ferait mentir la commande.
    if let Some(pos) = args.iter().position(|a| a == "--fusionner-trace") {
        run_fusion_traces(&args[pos + 1..]);
    }
    // ---- C1 : la TOPOLOGIE passe AVANT tout le reste, et avant même le chemin
    // du modèle. Un descripteur de régions ne décrit pas des poids : exiger un
    // fichier GGUF pour lire un graphe obligerait à en inventer un, et la
    // commande mentirait sur ce qu'elle fait. `--topologie F` imprime le plan
    // VÉRIFIÉ et sort ; l'exécution d'un graphe viendra après (capacité C1b).
    // …mais PAS si la topologie est là pour DÉCRIRE une exécution : le pilote
    // réparti (`--ppl-reparti`) et le nœud relais (`--flux-serveur`, `--region`)
    // l'exécutent, ils ne la lisent pas. Sans cette condition, les deux
    // imprimaient le plan et sortaient — arrivé deux fois, dont une pendant la
    // mise au point du relais.
    let topologie_executee = args.iter().any(|a| a == "--ppl-reparti")
        || args.iter().any(|a| a == "--flux-serveur")
        || args.iter().any(|a| a == "--region");
    if !topologie_executee {
    if let Some(pos) = args.iter().position(|a| a == "--topologie") {
        let f = match args.get(pos + 1) {
            Some(f) => f.clone(),
            None => { eprintln!("--topologie attend un fichier"); std::process::exit(2); }
        };
        let texte = match std::fs::read_to_string(&f) {
            Ok(t) => t,
            Err(e) => { eprintln!("topologie : lecture de {f} impossible : {e}"); std::process::exit(2); }
        };
        match topologie::lire_json(&texte).and_then(|t| t.plan()) {
            Ok(plan) => { print!("{plan}"); std::process::exit(0); }
            Err(e) => { eprintln!("{e}"); std::process::exit(3); }
        }
    }
    }
    let mut opt = analyser(&args);
    if opt.episodique_k == 0 { opt.episodique_k = 64; }
    if opt.episodique_pas == 0 { opt.episodique_pas = 1; }
    if opt.episodique_connexions == 0 { opt.episodique_connexions = 8; }
    if opt.episodique_cycles == 0 { opt.episodique_cycles = 1; }
    if opt.episodique_cycles_seuil == 0 { opt.episodique_cycles_seuil = 4; }
    let _ = MODELE.set(args[1].clone());
    // Plusieurs modes demandés : l'aiguillage en retient UN, dans un ordre
    // arbitraire, et le disait pas. On le dit.
    let modes: Vec<&str> = [
        (opt.banc_vision.is_some(), "--banc-vision"),
        (opt.flux_serveur.is_some(), "--flux-serveur"),
        (opt.ppl_reparti.is_some(), "--ppl-reparti"),
        (opt.tensors, "--tensors"), (opt.banc_mla.is_some(), "--banc-mla"),
        (opt.banc_kv > 0, "--banc-kv"), (opt.banc_topk > 0, "--banc-topk"),
        (opt.gpu_banc, "--gpu-banc"), (opt.materiel, "--materiel"), (opt.config, "--config"),
        (opt.sonder_engram > 0, "--sonder-engram"),
        (opt.episodique_essai > 0, "--episodique-essai"),
        (opt.reflexe_essai > 0, "--reflexe-essai"),
        (opt.plan, "--plan"), (opt.tokenize, "--tokenize"),
        (opt.ppl, "--ppl"), (opt.infer, "--infer"),
    ].iter().filter(|(v, _)| *v).map(|(_, n)| *n).collect();
    if modes.len() > 1 {
        eprintln!("[modes] {} modes demandés ({}) : c'est {} qui s'exécute — les autres \
sont ignorés", modes.len(), modes.join(", "), modes[0]);
    }
    if opt.entree.is_some() {
        // le chemin du modèle est le premier argument restant, comme partout ailleurs
        let chemin = modele_chemin();
        std::process::exit(run_peripherie(&chemin, &opt));
    }
    if opt.materiel { run_materiel(&opt); return; }
    if opt.config { run_config(); return; }
    if opt.sonder_engram > 0 { run_sonder_engram(opt.sonder_engram); return; }
    if opt.episodique_essai > 0 { run_episodique_essai(opt); return; }
    if opt.reflexe_essai > 0 { run_reflexe_essai(opt); return; }
    if let Some(f) = opt.engram_adresses.clone() { run_engram_adresses(&f, &opt); return; }
    if let Some(b) = opt.bloc.clone() { run_bloc(&b); return; }
    if let Some(f) = opt.banc_vision.clone() { run_banc_vision(&f); return; }
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
    // au système, et l'attente active de la barrière ne tolère aucune
    // sursouscription (mesuré : ×1,3 de perte à 40+1 threads sur 40 CPU).
    let cpu = engine::coeurs_physiques();
    let mut n_threads = cpu.max(1);
    // Pas de 2 SEULEMENT devant un drapeau qui prend une valeur : un pas de 2
    // aveugle sautait `--threads 4` dès qu'un drapeau booléen le précédait
    // (`--dense --threads 4` annonçait 30 fils). C'est exactement le bug corrigé
    // dans `analyser` — il en restait une copie ici.
    let mut i = 2;
    while i < args.len() {
        match args[i].as_str() {
            "--matrix" if i + 1 < args.len() => { matrix = args[i + 1].clone(); i += 2; }
            "--threads" if i + 1 < args.len() => {
                n_threads = args[i + 1].parse().unwrap_or(n_threads); i += 2;
            }
            _ => i += 1,
        }
    }

    let t0 = Instant::now();
    let g = Gguf::open_auto(path).expect("ouverture du GGUF");
    println!("GGUF ouvert en {:?} — {} tenseurs", t0.elapsed(), g.tensors.len());
    let arch = g.meta.get("general.architecture").and_then(|m| m.as_str()).unwrap_or("?");
    let n_layer = g.cfg("block_count").and_then(|m| m.as_u64()).unwrap_or(0);
    let hidden = g.cfg("embedding_length").and_then(|m| m.as_u64()).unwrap_or(0);
    let inter = g.cfg("feed_forward_length").and_then(|m| m.as_u64()).unwrap_or(0);
    println!("architecture : {arch} · {n_layer} couches · hidden {hidden} · intermédiaire {inter}");
    println!("threads : {n_threads}\n");

    // ---------------------------------------------------------------- tailles
    println!("=== 1. Taille exacte des encodages (mesurée sur les niveaux réels) ===");
    let mats = [
        "blk.0.ffn_gate.weight",
        "blk.0.ffn_down.weight",
        "blk.0.attn_q.weight",
        "blk.0.attn_output.weight",
    ];
    for name in mats {
        let Some(t) = g.tensor(name) else { continue };
        let Some(levels) = g.raw_levels(name) else { continue };
        let n = t.nelem();
        let n_rows = t.dims[0] as usize;
        let n_cols = t.dims[1] as usize;
        let nz = levels.iter().filter(|&&v| v != 0).count();
        let dens = nz as f64 / n as f64;

        let sd = SignedDelta::build(&levels, n_rows, n_cols);
        let bs = BitmapSign::build(&levels, n_rows, n_cols);
        let sk8 = SparseK::build(&levels, n_rows, n_cols, 8);
        let sk4 = SparseK::build(&levels, n_rows, n_cols, 4);
        let sk1 = SparseK::build(&levels, n_rows, n_cols, 1);

        println!("\n{name}  [{n_rows} × {n_cols}]  densité {:.1} %", dens * 100.0);
        println!("  dense 8 bits            {}", fmt_bits(dense_bits(n, 8), n));
        println!("  bitmap + signe          {}", fmt_bits(bs.bits(), n));
        println!("  creux k=1 (signe seul)  {}", fmt_bits(sk1.bits(), n));
        println!("  creux k=4               {}", fmt_bits(sk4.bits(), n));
        println!("  creux k=8               {}", fmt_bits(sk8.bits(), n));
        println!("  listes signées + écarts {}", fmt_bits(sd.bits(), n));
        println!("  (varint : {} événements, {:.1} écart moyen)",
                 sd.n_events, n_cols as f64 / (nz as f64 / n_rows as f64).max(1.0));
    }

    // -------------------------------------------------- moteur d'événements
    println!("\n=== 2. Moteur d'événements optimisé (4 optimisations) ===");
    println!("     réduction incrémentale · décodage SWAR · vecteur creux · listes fusionnées");
    let t = g.tensor(&matrix).expect("matrice absente");
    let Some(levels) = g.raw_levels(&matrix) else {
        println!("\n=== 2. Moteur d'événements — SAUTÉ : la matrice {matrix} n'est pas en \
Q8_0/Q4_0, et ce banc ne sait lire que ces deux formats.");
        return;
    };
    let n_rows = t.dims[0] as usize;
    let n_cols = t.dims[1] as usize;
    let n = n_rows * n_cols;
    let tern: Vec<i8> = levels.iter().map(|&v| v.signum()).collect();

    let fused = FusedSign::build(&tern, n_rows, n_cols);
    let old = SignedDelta::build(&tern, n_rows, n_cols);
    let bitmap = BitmapSign::build(&tern, n_rows, n_cols);
    println!("  {matrix} : {n_rows} entrées × {n_cols} sorties, {} événements", fused.n_events);
    println!("  listes fusionnées {:.2} Mo ({:.2} b/poids) | anciennes {:.2} Mo ({:.2}) | bitmap {:.2} Mo ({:.2})\n",
             fused.bits() as f64 / 8.0 / 1e6, fused.bits_per_weight(),
             old.bits() as f64 / 8.0 / 1e6, old.bits_per_weight(),
             bitmap.bits() as f64 / 8.0 / 1e6, bitmap.bits_per_weight());

    let mut x = vec![0i32; n_rows];
    for (i, v) in x.iter_mut().enumerate() { *v = ((i * 2654435761usize) % 200) as i32 - 100; }

    // ---- croisement push/pull sur la MÊME arithmétique ----
    // Comparer le ternaire (FusedSign) au dense int8 n'aurait aucun sens : les
    // deux ne calculent pas la même chose. `PushMat` et `DenseQ8` partagent au
    // contraire la quantification exacte (int8, une échelle par sortie), donc
    // l'écart mesuré est un pur effet de la DISPERSION contre le PRODUIT
    // SCALAIRE. La transposée est nécessaire : PushMat/DenseQ8 sont rangés par
    // ligne de sortie, le tenseur GGUF par ligne d'entrée.
    let wf: Vec<f32> = levels.iter().map(|&v| v as f32).collect();
    let mut wt = vec![0f32; n_rows * n_cols];
    for i in 0..n_rows { for o in 0..n_cols { wt[o * n_rows + i] = wf[i * n_cols + o]; } }
    let pm = PushMat::build(&wt, n_cols, n_rows);
    let dl = DenseQ8::build(&wt, n_cols, n_rows);
    println!("  push int8 : {:.2} b/poids, {} événements | pull int8 : {:.2} b/poids",
             pm.bits_per_weight(), pm.n_events, 8.0);

    // ---- repère de bande passante mémoire, mesuré MAINTENANT ----
    // Sans ce chiffre, on ne peut pas distinguer « noyau mal écrit » de
    // « noyau déjà au bout de la mémoire ». La charge de fond de cette machine
    // fait varier les durées du simple au double : le repère est pris dans les
    // mêmes conditions que les mesures qui suivent.
    let bp_bytes = 64usize << 20;
    let bp = vec![1u8; bp_bytes];
    let t0 = Instant::now();
    let bp_sum: u64 = std::thread::scope(|sc| {
        let hs: Vec<_> = (0..n_threads).map(|k| {
            let b = &bp[..];
            let lo = k * (bp_bytes / n_threads);
            let hi = if k + 1 == n_threads { bp_bytes } else { (k + 1) * (bp_bytes / n_threads) };
            sc.spawn(move || {
                // Lecture par mots de 64 bits : sommer octet par octet mesure la
                // latence de la chaîne d'addition, pas la mémoire. Le repère doit
                // être un vrai plafond de débit, sinon on conclut à tort qu'un
                // noyau est « au mur » alors qu'il est simplement mal écrit.
                let mut a = 0u64;
                for c in b[lo..hi].chunks_exact(8) {
                    a = a.wrapping_add(u64::from_ne_bytes(c.try_into().unwrap()));
                }
                a
            })
        }).collect();
        hs.into_iter().map(|h| h.join().unwrap()).sum()
    });
    let bp_dt = t0.elapsed().as_secs_f64();
    let bp_gbs = bp_bytes as f64 / bp_dt / 1e9;
    println!("  bande passante mémoire mesurée : {:.1} Go/s ({} Mo lus, {} threads, somme {} )",
             bp_gbs, bp_bytes >> 20, n_threads, bp_sum % 1000);
    drop(bp);

    let d4 = DenseQ4::build(&wt, n_cols, n_rows);
    println!("  4 bits : {:.2} b/poids", d4.bits_per_weight());

    let mut pool = Pool::new(n_threads, n_cols);
    println!("  pool de {} threads, barrière atomique\n", pool.threads());
    {
        // Le noyau AVX2 et le noyau scalaire doivent donner le MÊME résultat
        // (les sommes entières par bloc sont exactes quelle que soit l'ordre).
        let xv: Vec<i32> = x.clone();
        let x16: Vec<i16> = xv.iter().map(|&v| v as i16).collect();
        let mut pire = (0usize, 0f32);
        for o in 0..n_cols {
            let a = d4.dot(o, &xv);
            let b = d4.dot16(o, &x16, &list::sommes32(&x16));
            if a.to_bits() != b.to_bits() {
                let e = (a - b).abs() / a.abs().max(1.0);
                if e > pire.1 { pire = (o, e); }
            }
        }
        println!("  noyau 4 bits : scalaire vs AVX2 → {}",
                 if pire.1 == 0.0 { "BIT À BIT IDENTIQUE ✅".to_string() }
                 else { format!("DIVERGENT rang {} (écart relatif {:.3}) ❌", pire.0, pire.1) });
        let y4 = pool.matvec_dense_q4(&d4, &xv, 1.0);
        let mut pire = (0usize, 0f32);
        for o in 0..n_cols {
            let a = d4.dot(o, &xv);
            if (a - y4[o]).abs() > pire.1 { pire = (o, (a - y4[o]).abs() / a.abs().max(1.0)); }
        }
        println!("  pool 4 bits vs scalaire : {}",
                 if pire.1 == 0.0 { "IDENTIQUE ✅".to_string() }
                 else { format!("DIVERGENT rang {} (écart relatif {:.3}) ❌", pire.0, pire.1) });
    }
    println!("  {:>8}  {:>12}  {:>14}  {:>12}  {:>10}",
             "densité", "événements", "G év/s", "ms/appel", "M év/s/thread");
    for dens in [0.0, 0.01, 0.05, 0.10, 0.25, 0.50, 1.00] {
        let mut xa = x.clone();
        for i in 0..n_rows {
            if (i as f64 * 0.6180339887).fract() >= dens { xa[i] = 0; }
        }
        let sv = SparseVec::from_dense(&xa);
        let reps = if dens == 0.0 { 50 } else { 30 };
        let (out, _) = pool.accumulate(&fused, &sv);
        let t0 = Instant::now();
        for _ in 0..reps { let _ = pool.accumulate(&fused, &sv); }
        let dt = t0.elapsed().as_secs_f64() / reps as f64;
        let (out_d, _) = pool.accumulate_delta(&old, &sv);
        let t0 = Instant::now();
        for _ in 0..reps { let _ = pool.accumulate_delta(&old, &sv); }
        let dt_d = t0.elapsed().as_secs_f64() / reps as f64;
        let mut ev = 0usize;
        for &s in &sv.idx { fused.row_events_count(s as usize, &mut ev); }
        println!("  {:>7.1}%  {:>12}  fusion {:>6.2} G ({:.4} ms) | 2-listes {:>6.2} G ({:.4} ms)",
                 dens * 100.0, ev, ev as f64 / dt / 1e9, dt * 1e3,
                 ev as f64 / dt_d / 1e9, dt_d * 1e3);
        // Exactitude vérifiée à TOUTES les densités, pas seulement à une seule :
        // c'est la remise à zéro incrémentale et la fenêtre de réduction qui
        // sont en cause, et elles dépendent de la densité.
        {
            let y_ref = matvec_dense(&tern, &xa, n_cols, n_rows);
            let rep = |lbl: &str, got: &[i64]| {
                match got.iter().zip(y_ref.iter()).position(|(a, b)| a != b) {
                    None => println!("           → {lbl} : IDENTIQUE ✅"),
                    Some(i) => println!("           → {lbl} : DIVERGENT au rang {i} : {} vs {}",
                                        got[i], y_ref[i]),
                }
            };
            rep("fusion", &out);
            rep("2-listes", &out_d);
        }
        // ---- même arithmétique int8, deux modes d'exécution
        let acc = pool.accumulate_push(&pm, &sv);
        let t0 = Instant::now();
        for _ in 0..reps { let _ = pool.accumulate_push(&pm, &sv); }
        let dt_push = t0.elapsed().as_secs_f64() / reps as f64;
        let t0 = Instant::now();
        let mut yd = Vec::new();
        for _ in 0..reps { yd = pool.matvec_dense_i8(&dl, &xa, 1.0); }
        let dt_pull = t0.elapsed().as_secs_f64() / reps as f64;
        let mut ev_push = 0usize;
        for &s in &sv.idx { ev_push += pm.row_ev[s as usize] as usize; }
        // Les sommes entières sont exactes des deux côtés : si les deux modes
        // donnent le même f32 bit à bit, alors changer de mode ne peut pas
        // changer un seul token du modèle.
        let mut div = None;
        for o in 0..n_cols {
            let yp = acc[o] as f32 * pm.scale[o];
            if yp.to_bits() != yd[o].to_bits() { div = Some((o, yp, yd[o])); break; }
        }
        let poids_mo = (n_rows * n_cols) as f64 / 1e6;
        println!("           push int8 {:>7.2} matvec/s ({:.3} ms, {} év) | pull {:>7.2} matvec/s ({:.3} ms) | push/pull = ×{:.2}",
                 1.0 / dt_push, dt_push * 1e3, ev_push, 1.0 / dt_pull, dt_pull * 1e3, dt_push / dt_pull);
        println!("           pull : {:.1} Go/s de poids lus ({:.1} Mo), soit {:.0} % du repère mémoire",
                 poids_mo / dt_pull / 1e3, poids_mo, 100.0 * (poids_mo / dt_pull / 1e3) / bp_gbs);
        match div {
            None => println!("           → push vs pull (même arithmétique) : BIT À BIT IDENTIQUE ✅"),
            Some((o, a, b)) => println!("           → push vs pull : DIVERGENT au rang {o} : {a:e} vs {b:e} ❌"),
        }
    }
    pool.shutdown();

    // ------------------------------------------- exécution sans multiplieur
    println!("\n=== 3. Exécution sans multiplieur (décalages + additions) ===");
    let xd: Vec<i32> = x.clone();
    let t0 = Instant::now();
    let y_mul = matvec_dense(&levels, &xd, n_cols, n_rows);
    let t_mul = t0.elapsed().as_secs_f64();
    let t0 = Instant::now();
    let (y_sa, ops) = matvec_shift_add(&levels, &xd, n_cols, n_rows);
    let t_sa = t0.elapsed().as_secs_f64();
    let same = y_mul.iter().zip(y_sa.iter()).all(|(a, b)| a == b);
    let adds_per_weight = ops as f64 / n as f64;
    println!("  multiplication i8×i8 : {:8.1} ms", t_mul * 1e3);
    println!("  décalages + additions : {:8.1} ms  ({:.2} additions/poids, {} ops)",
             t_sa * 1e3, adds_per_weight, ops);
    println!("  rapport : ×{:.2}", t_sa / t_mul);
    println!("  résultat identique    : {}", if same { "OUI ✅" } else { "NON ❌" });
    println!("\n  → aucun DSP, aucune multiplication : la contrainte du cahier des charges");
    println!("    est satisfaite pour un modèle 8 bits, sans réentraînement ni élagage.");
}


// --------------------------------------------------------------------------- //
// Mode inférence : génération autorégressive en listes d'événements
// --------------------------------------------------------------------------- //


/// Chemin du modèle, posé une fois par `main` : les modes n'ont plus à fouiller
/// `argv` ni à supposer que le modèle est en position 1.
static MODELE: std::sync::OnceLock<String> = std::sync::OnceLock::new();
fn modele_chemin() -> String { MODELE.get().cloned().unwrap_or_default() }

/// **Sonde de plage** (`--tete-partielle`) : appliquer la tête de sortie à la
/// fin d'une plage `--couches a:b`. Par défaut une plage partielle rend le flux
/// résiduel brut — ce qu'un nœud de grappe doit expédier — donc la tête ne voit
/// jamais le jour : impossible de comparer des LOGITS par plage, et impossible
/// de vérifier une réduction finale dont les couches suivantes ne tournent pas
/// encore (V4.1, dont la compression est refusée).
/// C2/C6 : applique la capture et l'injection d'état sur un modèle chargé.
///
/// POURQUOI UNE FONCTION, ET PAS TROIS LIGNES DANS CHAQUE MODE : la fusion d'états
/// doit vouloir dire la MÊME chose en perplexité, en inférence et en réparti. Trois
/// copies, c'est trois occasions d'en corriger une seule.
fn appliquer_fusion(mdl: &mut model::Model, fusion_etat: Option<String>, fusion_alpha: f32,
                    fusion_pos: usize, etat_sortie: Option<String>, etat_pos: Vec<usize>) {
    if let Some(f) = fusion_etat.as_ref() {
        let brut = std::fs::read(f)
            .unwrap_or_else(|e| { eprintln!("fusion : lecture de {f} impossible : {e}");
                                  std::process::exit(2) });
        if brut.len() % 4 != 0 {
            eprintln!("fusion : {f} fait {} octets, ce n'est pas un multiple de 4 — un état \
s'écrit en f32 little-endian", brut.len());
            std::process::exit(2);
        }
        let v: Vec<f32> = brut.chunks_exact(4)
            .map(|q| f32::from_le_bytes([q[0], q[1], q[2], q[3]])).collect();
        println!("  fusion            : {} valeurs injectées, poids {}{}", v.len(),
                 fusion_alpha,
                 if fusion_alpha == 0.0 { " (poids NUL : aucun effet, c'est le témoin)" }
                 else { "" });
        mdl.fusion_etat = Some(v);
        mdl.fusion_alpha = fusion_alpha;
        mdl.fusion_pos = fusion_pos;
    } else if fusion_alpha != 1.0 {
        eprintln!("fusion : --fusion-alpha sans --fusion-etat n'a aucun effet");
    }
    if let Some(f) = etat_sortie.as_ref() {
        println!("  capture d'état    : position(s) {:?} écrite(s) dans {f}.*", etat_pos);
        mdl.etat_sortie = Some((f.clone(), etat_pos));
    }
}

fn poser_tete_partielle(mdl: &mut model::Model) {
    mdl.tete_partielle = true;
    eprintln!("[plage] `--tete-partielle` : la tête de sortie est appliquée à la fin de la \
plage — le résultat est celui d'un modèle TRONQUÉ, pas du modèle entier");
}

/// **Tableau de bord des réglages en vigueur** (`--options-actives`), lus sur le
/// MODÈLE après toutes les affectations.
///
/// Pourquoi il existe : le défaut le plus coûteux de ce dépôt n'est pas un calcul
/// faux, c'est un drapeau qui ne fait rien. Huit ont été corrigés en une session
/// (`--keep` en perplexité, `--ffn-gain` en inférence, les top-k dans les modes
/// flux, `--trace-flux` en inférence, `--threads` figé…), et chacun était
/// INVISIBLE : la sortie ne disait nulle part quelle valeur agissait. Ici, elle
/// le dit — et une valeur qu'on ne voit pas bouger est une valeur qui ne sert à
/// rien.
/// `--attn-sinks` SANS fenêtre active : le réglage est inerte, et il le dit.
///
/// Le compteur n'est lu QUE dans la branche à fenêtre de `forward()`
/// (`model.rs:7472` et `:7490`, `let ns = if lo > 0 { self.attn_sinks.min(lo) } else { 0 }`) :
/// sans fenêtre, `lo` vaut toujours 0 et le nombre de puits n'est jamais consulté. Ce n'est donc
/// PAS un drapeau mort — mesuré : à fenêtre 32, 0 puits → **29,0206** et 24 puits → **27,4439**,
/// un gain réel — mais il ne peut rien faire SANS fenêtre, et c'est exactement ce que le §46 bis
/// avait mal lu : la mesure d'inertie avait été faite dans la seule configuration où l'inertie
/// est ATTENDUE.
fn avertir_puits_inertes(mdl: &model::Model, impose: bool) {
    if impose && mdl.attn_sinks > 0 && mdl.attn_window == 0 {
        eprintln!("[attention] --attn-sinks {} SANS fenêtre active : les puits ne sont notés que \
dans la branche à fenêtre (`model.rs:7472`), donc ce réglage est INERTE ici. Avec fenêtre 32 : \
0 puits → 29,0206, 24 puits → 27,4439. Ajouter `--attn-window N` (N < séquence) pour qu'il agisse.",
                 mdl.attn_sinks);
    }
}

fn options_actives(mdl: &model::Model, mode: &str, ctx_impose: bool, dense: bool, keep: f32,
                   attn_sinks_impose: bool) {
    let oui = |b: bool| if b { "imposé" } else { "défaut" };
    println!("[options] mode {mode} · contexte {} ({}) · dense {} · keep {:.3}",
             mdl.ctx, oui(ctx_impose), dense, keep);
    println!("[options] activation : niveaux {:.0} · seuil {} · k-WTA {} · renorm {}",
             mdl.act_levels, mdl.act_thresh, mdl.act_topk, mdl.act_renorm);
    println!("[options] top-k : attn {} · q·k {} · MoE {} · par projection {:?}",
             mdl.attn_topk, mdl.qk_topk, mdl.moe_topk, mdl.act_topk_proj);
    println!("[options] couches {}..{} · flux brut {} · trace {} · rejeu {}",
             mdl.couche_debut, mdl.couche_fin, mdl.flux_brut,
             mdl.trace.is_some(), mdl.flux_force.is_some());
    // `--tete-partielle` CHANGE ce que rend une plage : le dire ici, sinon un
    // tableau de bord qui existe pour rendre les drapeaux visibles cache le seul
    // drapeau qui décide si la tête est appliquée.
    if mdl.tete_partielle {
        println!("[options] plage : la TÊTE DE SORTIE est appliquée à la fin de la plage \
(`--tete-partielle`) — résultat d'un modèle TRONQUÉ");
    }
    println!("[options] fenêtre {} · motif {} · seuil push {} · lot {} · ffn_gain {:?} · hebb {}",
             mdl.attn_window, mdl.swa_pattern, mdl.seuil_push, mdl.lot,
             mdl.ffn_gain, mdl.hebb.is_some());
    // Le nombre de PUITS était le seul réglage de l'attention qu'aucune ligne
    // n'affichait — et c'est précisément lui qui a fait conclure à tort qu'il était
    // mort : deux mesures égales (0 et 4) parce que le défaut vaut 4 et que `0`
    // était avalé. Une valeur qu'on ne voit pas est une valeur dont on ne peut rien
    // dire. Elle s'affiche donc TOUJOURS, avec sa portée : les puits ne sont notés
    // que dans la branche à fenêtre (`model.rs:7472`), donc sans fenêtre ils sont
    // inertes — et le tableau le dit au lieu de laisser croire qu'ils agissent.
    println!("[options] puits d'attention {} ({}){}",
             mdl.attn_sinks,
             if attn_sinks_impose { "imposé" } else { "défaut" },
             if mdl.attn_window == 0 { " · INERTES : aucune fenêtre active" } else { "" });
    // `--lot N > 1` n'est PAS une simple affaire de vitesse : le chemin par lots
    // réordonne les sommes de la même façon sur tous les modèles, mais il
    // change les derniers bits, et un routeur au voisinage d'une égalité peut
    // choisir un autre expert. Mesuré (Qwen3-30B-A3B, invite de 192 jetons) :
    // perplexité 19,143 contre 19,172, argmax identique sur 191/191 positions,
    // et pourtant une génération gloutonne qui diverge au 3e jeton. Le dire
    // ici, une fois, plutôt que de laisser croire que le lot est neutre.
    if mdl.lot > 1 {
        println!("[options] lot {} : le préremplissage par lots n'est PAS identique bit à bit \
au chemin jeton par jeton (sommes réordonnées ; un routeur à égalité peut changer d'expert). \
Mesuré sur Qwen3-30B-A3B : PPL 19,143 contre 19,172, argmax identique sur 191/191 positions \
d'invite, mais une génération gloutonne peut diverger après quelques jetons. Le débit, lui, \
change : ×1,58 mesuré de lot 1 à lot 192 (invite de 192 jetons, 16 fils).",
                 mdl.lot);
    }
    if let Some(kv) = mdl.kv.first() {
        println!("[options] cache KV : {} bits{} · f16 avant {}",
                 kv.bits,
                 if kv.k_f32 { " · CLÉS en f32" }
                 else if kv.k_f16 { " · clés en f16" }
                 else if kv.v_f32 { " · VALEURS en f32" } else { "" },
                 kv.f16_avant);
    }
    // Le top-k déporté est un mode, pas un détail : c'est ici qu'on voit s'il
    // s'applique VRAIMENT à cette configuration, et pourquoi sinon. La ligne
    // existe parce que huit drapeaux « analysés mais jamais appliqués » ont coûté
    // une session entière — et parce que `DRAVE_GPU_TOPK=1` posé sans
    // `DRAVE_GPU_KV` ne faisait rien en silence.
    if std::env::var("DRAVE_GPU_TOPK").map(|v| v != "0" && !v.is_empty()).unwrap_or(false) {
        let bits = mdl.kv.first().map(|k| k.bits).unwrap_or(32);
        let k = mdl.attn_topk;
        let motif = if k == 0 {
            "inactif : --attn-topk n'est pas donné"
        } else if k > 1024 {
            "inactif : k > 1024 (limite du noyau 3)"
        } else if bits != 8 && bits != 32 {
            "inactif : valeurs KV 4 bits (le noyau 3 n'en gère que 8 ou 32)"
        } else if mdl.attn_window > 0 {
            "inactif : la fenêtre garde le chemin CPU"
        } else if mdl.lot > 1 {
            "inactif en mode lot : l'attention par lots est DENSE"
        } else if std::env::var("DRAVE_GPU").is_err() {
            "inactif : DRAVE_GPU n'est pas posé (rien ne va au GPU)"
        } else if std::env::var("DRAVE_GPU_KV").is_err() {
            "inactif : DRAVE_GPU_KV n'est pas posé (pas de miroir VRAM à interroger)"
        } else {
            "ACTIF"
        };
        println!("[options] top-k déporté (DRAVE_GPU_TOPK) : {motif}");
    }
}

/// Fils de calcul d'un mode SECONDAIRE : `--threads` s'il est donné, sinon la
/// moitié des cœurs. Ces modes étaient figés à 16 fils, ce qui ignorait
/// `--threads` en silence (relevé par `reports/rapport-drapeaux-ignores.md`).
fn fils(opt: &Options) -> usize {
    if opt.threads_impose { opt.threads.max(1) }
    else {
        let cpu = engine::coeurs_physiques();
        cpu.max(1)
    }
}

/// **Toutes** les options de la ligne de commande, dans une seule structure.
///
/// Les modes (inférence, perplexité, plan, tokenize) la remplissent par la MÊME
/// boucle : c'est la seule façon d'éviter qu'un drapeau fonctionne dans un mode
/// et pas dans l'autre. Le bug est arrivé quatre fois — `--pin`, `--moe-topk`,
/// `--attn-window` et `--attn-sinks` ont chacun été « analysés mais jamais
/// appliqués » dans un mode au moins, et un drapeau en dernière position était
/// ignoré à cause du pas de deux.
#[derive(Default)]
struct Options {
    // --- sélection du mode
    infer: bool, ppl: bool, plan: bool, tokenize: bool, gpu_banc: bool, k3_essai: bool,
    /// C1 — descripteur de topologie de régions (docs/plan-cerveau-complet.md).
    topologie: Option<String>,
    /// C1b — identifiant de MA région, sur un nœud relais.
    region: Option<String>,
    /// C6 : combien d'épisodes collecter pour l'essai de mémoire épisodique.
    episodique_essai: usize,
    /// C6 : nombre de canaux par clé (k-WTA). Le seul réglage du magasin.
    episodique_k: usize,
    /// C6 : où écrire le magasin (round-trip par fichier, vérifié).
    episodique_fichier: Option<String>,
    /// C6 : retirer la moyenne des états avant de calculer les clés (décorrélation).
    episodique_decorreler: bool,
    /// C6 : expansion à la manière du gyrus denté — nombre de canaux de sortie.
    /// 0 = pas d'expansion.
    episodique_expansion: usize,
    /// C6 : entrées reçues par canal expansé.
    episodique_connexions: usize,
    /// C6 : égaliser l'usage des canaux (centrer et réduire PAR CANAL sur le magasin)
    /// avant de choisir la clé — contre les canaux « hub ».
    episodique_normaliser: bool,
    /// C8 : combien de positions mesurer pour l'essai de RÉFLEXE (sortie précoce).
    reflexe_essai: usize,
    /// C6 : état EXTÉRIEUR servant d'indice de lecture (f32 bruts). S'il est donné,
    /// l'indice sémantique est cet état et non celui de la dernière position — c'est ce
    /// qui rend la mesure honnête, car un indice pris DANS le magasin s'y retrouve
    /// lui-même (recouvrement 64/64) et ne teste donc rien.
    episodique_indice: Option<String>,
    /// C6/C2 : écrire l'état RETROUVÉ par la lecture (f32 bruts), prêt à être injecté
    /// ailleurs par `--fusion-etat`. C'est le dernier maillon : la mémoire rend un
    /// épisode, et cet épisode doit pouvoir ENTRER dans un autre calcul. Si la mémoire
    /// est décorrélée, la moyenne est rajoutée — sinon on injecterait un état centré,
    /// qui n'est l'état d'aucun moment vécu.
    episodique_extraire: Option<String>,
    /// C6 : largeur de la FENÊTRE qui forme la clé d'un épisode. 1 = la position seule.
    ///
    /// POURQUOI CETTE EXPÉRIENCE DÉCOULE DU MÉCANISME MESURÉ. La clé est un k-WTA : les
    /// 64 plus grands canaux sur 16 384. Une petite variation de l'état fait donc ENTRER
    /// ET SORTIR des canaux, et deux jetons VOISINS peuvent rendre des épisodes à 1 006
    /// et 50 jetons de l'aiguille (mesuré). Si cette explication est la bonne, former la
    /// clé sur la MOYENNE de W positions voisines doit LISSER la clé et réduire
    /// l'hypersensibilité ; sinon l'explication est incomplète. Prédiction falsifiable.
    episodique_fenetre: usize,
    /// C6 : position connue d'une information plantée (l'« aiguille »). Sert à mesurer
    /// la distance entre l'épisode RENDU par la mémoire et l'endroit où l'information
    /// se trouve VRAIMENT — c'est la seule façon de savoir si la mémoire retrouve le
    /// bon passage, et pas seulement un épisode quelconque.
    episodique_aiguille: Option<usize>,
    /// C2/C6 : état BRUT à injecter à la fin des couches (fichier de f32 bruts).
    fusion_etat: Option<String>,
    /// C11 (découverte) : fichier de registre `region hote:port`, pour que les topologies
    /// nomment les régions au lieu de coder des adresses.
    registre: Option<String>,
    /// C2/C6 : poids de l'état injecté.
    fusion_alpha: f32,
    /// C2/C6 : où écrire l'état brut, et à quelles positions.
    etat_sortie: Option<String>,
    etat_pos: Vec<usize>,
    /// C2/C6 : capturer l'état à la K-ième position depuis la FIN de l'invite
    /// (1 = la dernière). C'est la seule façon FIABLE de nommer « la fin » : les
    /// positions ne se devinent pas (`--tokenize` et `--prompt` ne comptent pas les
    /// mêmes jetons pour un texte qui finit par un saut de ligne — 17 contre 16,
    /// mesuré), et s'y tromper a fait échouer deux mesures avant que ce drapeau existe.
    etat_fin: Option<(String, Vec<usize>)>,
    /// C2/C6 : à quelle position INJECTER l'état. `usize::MAX` = partout, ce qui
    /// n'est presque jamais ce qu'on veut : on rappelle un souvenir au moment de
    /// répondre, pas à chaque jeton de la question.
    fusion_pos: usize,
    /// C2/C6 : injecter à la DERNIÈRE position de l'invite, quelle qu'elle soit.
    ///
    /// POURQUOI CETTE VALEUR SYMBOLIQUE EXISTE. Compter les jetons de l'invite pour
    /// écrire `--fusion-pos 15` s'est trompé D'UN JETON : la tokenisation de
    /// `--prompt` ne fait pas exactement celle de `--tokenize` (l'espace initial),
    /// et la greffe ne mordait donc pas — la position 15 était un jeton du MILIEU de
    /// la question. Une position qui se calcule doit être calculée par celui qui
    /// connaît la longueur, pas devinée par celui qui écrit la commande.
    fusion_dernier: bool,
    /// C7 : nombre de CYCLES de consolidation par rejeu (>1 pour la consolidation
    /// répétée : ce que la mémoire devient quand on la rejoue).
    episodique_cycles: usize,
    /// C7 : seuil de fusion (canaux partagés) des cycles de consolidation.
    episodique_cycles_seuil: usize,
    /// C9/C10 : nombre de FIBRES du pont entre la région locale et la région
    /// distante. 0 = pont entier (aucun écrêtage). Ne garder que les K plus grandes
    /// amplitudes de l'état échangé, c'est limiter la bande passante du lien — la
    /// question du corps calleux, et celle d'une distribution sur lien lent.
    pont_k: usize,
    /// C6 : documents (fichiers de TEXTE brut, séparés par des virgules) d'où
    /// collecter les épisodes. Chaque document repart d'un cache neuf.
    episodique_textes: Option<String>,
    /// C6 : écart entre deux états collectés. 1 = états consécutifs du même texte ;
    /// plus grand = des moments éloignés du texte, donc des contenus moins corrélés.
    /// C'est LA condition qui décide si les clés se recouvrent.
    episodique_pas: usize,
    /// C12 — trace globale : où écrire ce qui traverse chaque lien.
    trace_globale: Option<String>,
    /// C12 — vérification : rejouer et comparer à cette trace.
    verifier_globale: Option<String>,
    /// C5 — bus de modulation : `canal=valeur`, répétable.
    bus: Vec<String>,
    /// C5bis — port d'écoute du BUS (réservé : la diffusion passe par le fichier).
    bus_serveur: Option<u16>,
    /// C4 — borne de PAS par région : au-delà, l'exécution s'arrête et le DIT,
    /// plutôt que de rendre un résultat partiel qui aurait l'air complet.
    pas_max: Option<u64>,
    /// C5bis — FICHIER DE CONTRÔLE : le bus y est relu avant chaque trame, donc un
    /// autre processus (ou une autre machine, par un montage partagé) peut changer
    /// un canal PENDANT l'exécution — c'est ce qui en fait un bus et non un réglage
    /// de démarrage. Le transport par socket viendra quand l'ordre du nœud sera
    /// revu (le fil doit être posé AVANT l'accept, sinon il n'écoute que pendant
    /// qu'un client est connecté).
    bus_fichier: Option<String>,
    /// Banc du KV déporté : nombre de clés à faire tenir en VRAM.
    banc_kv: usize,
    /// Banc des SCORES d'attention : nombre de clés à noter (noyau 1 du top-k).
    banc_topk: usize,
    /// Banc MLA : écrit les logits `(n_pos × vocab)` en f32 pour les comparer à
    /// la référence numpy du modèle synthétique.
    banc_mla: Option<String>,
    /// Trace du flux d'activation : fichier de sortie.
    trace_flux: Option<String>,
    /// Relecture d'une trace : les activations enregistrées remplacent celles
    /// calculées (rejeu).
    flux_forcer: Option<String>,
    /// Phase 3 : nœud MOTEUR qui écoute et applique sa plage de couches.
    /// `--options-actives` : imprime, APRÈS toutes les affectations, les réglages
    /// que le moteur utilise réellement. C'est la réponse au mode d'échec le plus
    /// coûteux du dépôt — huit drapeaux « analysés mais jamais appliqués » en une
    /// seule session : une valeur affichée ici est une valeur qui agit.
    options_actives: bool,
    /// Drapeaux `--xxx` que l'analyse n'a PAS reconnus. Ils étaient ignorés en
    /// silence : `--keeep 0.05` (une faute de frappe) faisait tourner le modèle
    /// entier sans élagage et sans un mot.
    inconnus: Vec<String>,
    /// `--options-strict` : un drapeau inconnu n'est plus un avertissement mais une
    /// ERREUR. Pour les scripts : une faute de frappe ne doit pas passer.
    options_strict: bool,
    /// Adresse d'écoute du nœud moteur : `port`, ou `hôte:port` pour écouter
    /// au-delà de localhost (un pair distant, un tunnel, une autre machine).
    flux_serveur: Option<String>,
    /// Phase 3 : pilote qui répartit le calcul sur un nœud distant (hôte:port).
    ppl_reparti: Option<String>,
    /// Nombre de couches gardées en local par le pilote.
    couches_locales: usize,
    /// Exécution **bornée** `a:b` — le harnais qui exécute les couches dont les
    /// mécanismes sont implémentés, pour les comparer à la référence avant que
    /// le reste du modèle existe.
    couches: Option<(usize, usize)>,
    /// Couches à tracer (vide = toutes).
    trace_couches: Vec<usize>,
    /// Banc vision : embedding de patchs, écrit en binaire pour comparaison
    /// avec la référence numpy.
    banc_vision: Option<String>,
    /// `--tensors` : liste les tenseurs du fichier (nom, dimensions, type) et
    /// s'arrête. Sert à préparer un chemin qu'on ne sait pas encore lire — le
    /// projecteur de vision, par exemple.
    tensors: bool,
    // --- source des jetons
    ids: Vec<u32>, ids_file: Option<String>, texte_file: Option<String>,
    ppl_texte: bool, prompt: Option<String>, limit: usize, depuis: usize,
    // --- génération
    n: usize, temp: f32, top_p: f32, topk: usize, rep_pen: f32, hist: usize,
    flux: bool, session: bool, chat: bool, flux_liste: bool, flux_blocs: bool,
    // --- moteur
    ctx: usize, threads: usize, abits: u32, dense: bool, auto: bool,
    /// Vrai si `--ctx`, `--threads` ou `--abits` ont été donnés : leurs défauts
    /// diffèrent selon le mode (256 jetons et 16 bits en perplexité, 512 et
    /// 8 bits en inférence, la moitié des cœurs contre les trois quarts).
    ctx_impose: bool, threads_impose: bool, abits_impose: bool,
    q4: u8, b6: u8, keep: f32, bits: u32, moe_topk: usize, pin: bool,
    // --- attention
    attn_window: usize, swa_pattern: Option<usize>, sans_fenetre: bool,
    attn_sinks: usize, attn_topk: usize, qk_topk: usize,
    /// Vrai si `--attn-sinks` a été DONNÉ. Sans ce drapeau, `0` était
    /// inexprimable : l'application était gardée par `if attn_sinks > 0`, donc
    /// `--attn-sinks 0` était AVALÉ et la valeur restait au défaut — 4 puits
    /// (model.rs:4492, `if fenetre > 0 { 0 } else { 4 }`). Mesuré : `0` et `4`
    /// rendent le MÊME chiffre (29,0206), ce qui avait fait conclure à tort que
    /// le drapeau était mort. Il ne l'était pas : c'est le ZÉRO qui n'existait pas.
    attn_sinks_impose: bool,
    // --- parcimonie des activations
    act_thresh: f32, act_topk: usize, act_renorm: bool, topk_proj: [usize; 7],
    // --- mesure
    logits_bin: Option<String>, ppl_profil: bool,
    /// **Périphérie (C8)** : le flux d'entrée (`signal:F`), le canal où poser la valeur, le
    /// gain de l'injection, le délai en pas, et le fichier de sortie (réutilise `--sortie`).
    entree: Option<String>, entree_canal: usize, entree_gain: f32, delai: usize,
    entree_jeton: usize, recurent: bool, entree_memoire: usize,
    /// **Mémoire de la région frontière** : nombre de signaux retenus hors du réseau, et le
    /// fichier où la valeur retenue est écrite pas à pas (f32 brut, une valeur par pas).
    memoire: usize, sortie_memoire: Option<String>,
    /// **C2 — récurrence** : poids de la sortie du pas précédent réinjectée dans l'entrée du pas
    /// courant (`0.0` = pas de récurrence, et c'est la valeur par défaut).
    recurrence: f32,
    config: bool,
    /// Profilage des neurones « chauds » (idée de PowerInfer) et fichier de
    /// sortie du classement.
    profil_neurones: bool, neurones_sortie: Option<String>,
    /// Détection du matériel et plan de configuration, sans charger de modèle.
    materiel: bool,
    /// Sonde d'accès mmappé à la table d'engram : combien d'entrées lire, à des
    /// indices dispersés. Démontre qu'une table de 101 Go s'adresse sans se
    /// charger.
    sonder_engram: usize,
    /// **Sonde de plage** : avec `--couches a:b`, appliquer AUSSI la tête de
    /// sortie. Par défaut une plage partielle rend le flux résiduel brut (ce
    /// qu'un nœud de grappe expédie) ; ce drapeau dit « je veux les logits d'un
    /// modèle tronqué », ce qui est la seule façon de vérifier une réduction
    /// finale dont les couches suivantes ne tournent pas encore.
    tete_partielle: bool,
    /// `--engram-adresses F` : écrit la **liste d'adresses** de l'engram
    /// (un entier par jeton et par colonne de hachage) et imprime ce qu'elle
    /// coûte — rangées distinctes, recouvrement entre jetons consécutifs.
    engram_adresses: Option<String>,
    /// `TENSEUR:INDEX` : déquantifie UN bloc et l'imprime. Sert à confronter
    /// notre déquantification à celle de ggml sur un bloc réel, sans dépendre
    /// d'une réimplémentation en script — c'est le code du moteur qu'on veut
    /// éprouver, pas une copie.
    bloc: Option<String>,
    /// Fichier d'identifiants de tokens : la tête de sortie ne calcule que
    /// ceux-là. **Génération seulement** — une perplexité calculée sur un
    /// vocabulaire restreint n'est comparable à rien.
    tete_restreinte: Option<String>,
    /// `--tete-garantie <fichier>` : liste de candidats pour une restriction de
    /// tête **prouvée exacte** (Cauchy-Schwarz + extension par paliers). La
    /// sortie est identique au calcul complet ; ce qui change est le nombre de
    /// lignes lues.
    tete_garantie: Option<String>,
    /// Taille du lot de préremplissage : 1 = jeton par jeton (défaut).
    lot: usize,
    harmony: Option<String>, harmony_contexte: Option<String>,
    // --- rotation
    sans_yarn: bool,
    // --- expériences
    patch: Option<String>, hebb_layer: Option<usize>, hebb_q: f32,
    hebb_diff: Option<usize>, hebb_eta: f32, hebb_clamp: f32,
    hebb_out: String, ffn_gain: Option<Vec<(usize, f32)>>, matrix: String,
    // --- tokenize / plan
    texte: Option<String>, fichier: Option<String>, sortie: Option<String>,
}

/// Analyse la ligne de commande UNE fois. Les drapeaux à valeur consomment
/// l'argument suivant (`i += 2`) ; les drapeaux booléens non (`i += 1`).
fn analyser(args: &[String]) -> Options {
    let mut o = Options {
        n: 32, temp: 0.0, top_p: 1.0, hist: 64, hebb_q: 0.1,
        hebb_out: String::from("hebb.bin"), keep: 1.0, abits: 8,
        hebb_diff: None, hebb_eta: 1e-4, hebb_clamp: 1.0,
        // Ces deux valeurs ne peuvent PAS venir de `Default` : `f32::default()` vaut
        // 0,0 et `usize::default()` vaut 0, donc un `--fusion-etat` sans
        // `--fusion-alpha` aurait injecté un vecteur multiplié par ZÉRO (aucun effet,
        // en silence) et `--fusion-pos` absent aurait injecté à la SEULE position 0.
        // C'est le défaut le plus coûteux du dépôt — un drapeau qui ne fait rien.
        fusion_alpha: 1.0, fusion_pos: usize::MAX,
        auto: true, limit: usize::MAX,
        entree: None, entree_canal: usize::MAX, entree_gain: 1.0, delai: 0, entree_jeton: 0,
        recurent: false, entree_memoire: 0, memoire: 0, sortie_memoire: None, recurrence: 0.0,
        matrix: String::from("blk.0.ffn_gate.weight"),
        ..Default::default()
    };
    let cpu = engine::coeurs_physiques();
    o.ctx = 512;
    o.threads = cpu.max(1);
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
            "--topologie" => { o.topologie = Some(suivant(i).clone()); 2 }
            // C1b : le nœud RELAIS dit QUI il est dans la topologie ; c'est la
            // topologie, et elle seule, qui dit à qui il transmet ensuite.
            "--region" => { o.region = Some(suivant(i).clone()); 2 }
            // C12 : la trace globale, et sa vérification par rejeu.
            "--trace-globale" => { o.trace_globale = Some(suivant(i).clone()); 2 }
            "--verifier-globale" => { o.verifier_globale = Some(suivant(i).clone()); 2 }
            "--episodique-essai" => { o.episodique_essai = suivant(i).parse().unwrap_or(0); 2 }
            "--episodique-k" => { o.episodique_k = suivant(i).parse().unwrap_or(64); 2 }
            "--episodique-fichier" => { o.episodique_fichier = Some(suivant(i).clone()); 2 }
            "--episodique-pas" => { o.episodique_pas = suivant(i).parse().unwrap_or(1).max(1); 2 }
            "--episodique-decorreler" => { o.episodique_decorreler = true; 1 }
            "--episodique-expansion" => { o.episodique_expansion = suivant(i).parse().unwrap_or(0); 2 }
            "--episodique-connexions" => { o.episodique_connexions = suivant(i).parse().unwrap_or(8); 2 }
            "--episodique-normaliser" => { o.episodique_normaliser = true; 1 }
            "--episodique-textes" => { o.episodique_textes = Some(suivant(i).clone()); 2 }
            "--pont-k" => { o.pont_k = suivant(i).parse().unwrap_or(0); 2 }
            "--reflexe-essai" => { o.reflexe_essai = suivant(i).parse().unwrap_or(0); 2 }
            "--registre" => { o.registre = Some(suivant(i).clone()); 2 }
            "--fusion-etat" => { o.fusion_etat = Some(suivant(i).clone()); 2 }
            "--fusion-alpha" => { o.fusion_alpha = suivant(i).parse().unwrap_or(1.0); 2 }
            "--fusion-pos" => {
                let v = suivant(i).clone();
                if v == "dernier" || v == "-1" { o.fusion_dernier = true; }
                else { o.fusion_pos = v.parse().unwrap_or(usize::MAX); }
                2
            }
            "--etat-sortie" => { o.etat_sortie = Some(suivant(i).clone()); 2 }
            // Une LISTE de positions : « 2248,4151 ». Deux prélevements d'un même
            // contexte tiennent alors en une seule passe.
            "--etat-fin" => {
                let f = suivant(i).clone();
                // PLUSIEURS positions depuis la fin (« 1,2,4,8 ») : un seul parcours
                // suffit pour prélever une FAMILLE d'indices. C'est ce qui rend
                // mesurable la question « le rappel rate-t-il à cause de l'indice
                // choisi, ou de la mémoire ? » — sans cela, huit indices coûtaient
                // huit parcours de 70 s.
                // La liste des positions est l'argument SUIVANT le fichier : `suivant(i)`
                // rend toujours args[i+1], et l'appeler deux fois relisait le fichier
                // (attrapé : huit positions demandées, une seule écrite).
                let ks: Vec<usize> = args.get(i + 2).map(|x| x.split(',')
                    .filter_map(|y| y.trim().parse().ok()).collect())
                    .unwrap_or_default();
                o.etat_fin = Some((f, if ks.is_empty() { vec![1] } else { ks }));
                3
            }
            "--etat-pos" => {
                o.etat_pos = suivant(i).split(',')
                    .filter_map(|x| x.trim().parse().ok()).collect();
                2
            }
            "--episodique-fenetre" => { o.episodique_fenetre = suivant(i).parse().unwrap_or(1).max(1); 2 }
            "--episodique-extraire" => { o.episodique_extraire = Some(suivant(i).clone()); 2 }
            "--episodique-indice" => { o.episodique_indice = Some(suivant(i).clone()); 2 }
            "--episodique-aiguille" => { o.episodique_aiguille = suivant(i).parse().ok(); 2 }
            "--episodique-cycles" => { o.episodique_cycles = suivant(i).parse().unwrap_or(1); 2 }
            "--episodique-cycles-seuil" => { o.episodique_cycles_seuil = suivant(i).parse().unwrap_or(4); 2 }
            // C5 : le bus de modulation, canal par canal.
            "--bus" => { o.bus.push(suivant(i).clone()); 2 }
            "--bus-serveur" => { o.bus_serveur = suivant(i).parse().ok(); 2 }
            "--bus-fichier" => { o.bus_fichier = Some(suivant(i).clone()); 2 }
            "--pas-max" => { o.pas_max = suivant(i).parse().ok(); 2 }
            "--tokenize" => { o.tokenize = true; 1 }
            "--gpu-banc" => { o.gpu_banc = true; 1 }
            // Test de fumée de la couche 0 de Kimi-K3, **sur un modèle même
            // incomplet** (les tenseurs de la couche 0 arrivent tôt) : c'est ce
            // qui permet de déboguer la structure avant la fin d'un transfert de
            // 1,5 To. Ce n'est PAS une vérification (la référence ne tourne pas
            // sur un modèle incomplet) — juste : ça charge, ça calcule, ça sort
            // des valeurs finies et plausibles.
            "--k3-essai" => { o.k3_essai = true; 1 }
            "--banc-kv" => { o.banc_kv = suivant(i).parse().unwrap(); 2 }
            "--banc-topk" => { o.banc_topk = suivant(i).parse().unwrap(); 2 }
            "--banc-mla" => { o.banc_mla = Some(suivant(i).clone()); 2 }
            "--tensors" => { o.tensors = true; 1 }
            "--trace-flux" => { o.trace_flux = Some(suivant(i).clone()); 2 }
            "--flux-forcer" => { o.flux_forcer = Some(suivant(i).clone()); 2 }
            "--flux-serveur" => { o.flux_serveur = Some(suivant(i).clone()); 2 }
            "--options-actives" => { o.options_actives = true; 1 }
            "--options-strict" => { o.options_strict = true; 1 }
            "--tete-partielle" => { o.tete_partielle = true; 1 }
            "--ppl-reparti" => { o.ppl_reparti = Some(suivant(i).clone()); 2 }
            "--couches-locales" => { o.couches_locales = suivant(i).parse().unwrap(); 2 }
            "--couches" => {
                let v = suivant(i);
                let (a, b) = v.split_once(':').unwrap_or_else(||
                    panic!("--couches attend `a:b` (reçu « {v} »)"));
                o.couches = Some((a.parse().unwrap(), b.parse().unwrap()));
                2
            }
            "--trace-couches" => { o.trace_couches = suivant(i).split(',')
                                     .filter_map(|x| x.trim().parse().ok()).collect(); 2 }
            "--banc-vision" => { o.banc_vision = Some(suivant(i).clone()); 2 }
            "--ids" => { o.ids = suivant(i).split(',')
                            .filter_map(|s| s.trim().parse().ok()).collect(); 2 }
            "--ids-file" => { o.ids_file = Some(suivant(i).clone()); 2 }
            "--prompt" => { o.prompt = Some(suivant(i).clone()); 2 }
            "--texte" => { o.texte = Some(suivant(i).clone()); 2 }
            "--fichier" => { o.fichier = Some(suivant(i).clone()); 2 }
            "--sortie" => { o.sortie = Some(suivant(i).clone()); 2 }
            // ---- PÉRIPHÉRIE (C8) : une région frontière reçoit un SIGNAL et rend une SORTIE.
            // Le type est explicite (`signal:`) parce qu'un banc vision viendra peut-être
            // ensuite — et un type inconnu doit être REFUSÉ, pas ignoré.
            "--entree" => { o.entree = Some(suivant(i).clone()); 2 }
            "--entree-canal" => { o.entree_canal = suivant(i).parse().unwrap(); 2 }
            "--entree-gain" => { o.entree_gain = suivant(i).parse().unwrap(); 2 }
            "--delai" => { o.delai = suivant(i).parse().unwrap(); 2 }
            "--entree-jeton" => { o.entree_jeton = suivant(i).parse().unwrap(); 2 }
            // MÉMOIRE DE LA RÉGION FRONTIÈRE (C8, suite) : les K derniers signaux injectés sont
            // retenus HORS DU RÉSEAU. La mesure a montré pourquoi : l'état de sortie porte le
            // signal courant (R² 0,992) et pas celui d'il y a 8 pas (R² −0,681), mais un tampon
            // lu directement le rend EXACTEMENT (1,000). `--memoire 0` est accepté et vaut
            // « pas de mémoire » (l'absence doit être exprimable, cf. la leçon `--attn-sinks`).
            "--memoire" => { o.memoire = suivant(i).parse().unwrap(); 2 }
            "--sortie-memoire" => { o.sortie_memoire = Some(suivant(i).clone()); 2 }
            // RÉCURRENT : la boucle avance les positions (0, 1, 2, …) au lieu de repartir à 0.
            // Sans lui, chaque pas est une DÉCISION INDÉPENDANTE : l'état ne dépend que de la
            // valeur injectée, et « poursuivre un signal » n'a pas de sens (le délai est alors
            // fait par l'interface, pas par le modèle). Avec lui, l'historique est dans le cache
            // KV, et la mémoire du signal devient une question mesurable.
            "--recurent" => { o.recurent = true; 1 }
            // RÉCURRENCE (C2) : la région consomme sa PROPRE sortie du pas précédent, avec un
            // poids déclaré : x0(t) += alpha · h(t−1). C'est la boucle que le plan décrit
            // (« une région peut consommer sa propre sortie du pas précédent ») et que le
            // validateur de topologie refuse encore dans un graphe (cycle) — ici elle est
            // explicite, bornée, et mesurable dans la région frontière.
            "--recurrence" => { o.recurrence = suivant(i).parse().unwrap(); 2 }
            // TAMPON explicite : les K derniers valeurs sont injectées sur les canaux suivants.
            // C'est la STRUCTURE dont la fiche `rapport-c8-peripherie.md` § 2 ter montre l'absence :
            // une récurrence qui fuit ne retient pas (R² 0,104), un tampon retient exactement.
            "--entree-memoire" => { o.entree_memoire = suivant(i).parse().unwrap(); 2 }
            "--matrix" => { o.matrix = suivant(i).clone(); 2 }
            "--logits-bin" => { o.logits_bin = Some(suivant(i).clone()); 2 }
            "--neurones-sortie" => { o.neurones_sortie = Some(suivant(i).clone()); 2 }
            "--harmony-contexte" => { o.harmony_contexte = Some(suivant(i).clone()); 2 }
            "--patch" => { o.patch = Some(suivant(i).clone()); 2 }
            "--n" => { o.n = suivant(i).parse().unwrap(); 2 }
            "--temp" => { o.temp = suivant(i).parse().unwrap(); 2 }
            "--top-p" => { o.top_p = suivant(i).parse().unwrap(); 2 }
            "--topk" => { o.topk = suivant(i).parse().unwrap(); 2 }
            "--rep-penalty" => { o.rep_pen = suivant(i).parse().unwrap(); 2 }
            "--hist" => { o.hist = suivant(i).parse().unwrap(); 2 }
            "--ctx" => { o.ctx = suivant(i).parse().unwrap(); o.ctx_impose = true; 2 }
            "--threads" => { o.threads = suivant(i).parse().unwrap(); o.threads_impose = true; 2 }
            "--abits" => { o.abits = suivant(i).parse().unwrap(); o.abits_impose = true; 2 }
            "--bits" => { o.bits = suivant(i).parse().unwrap(); 2 }
            "--limit" => { o.limit = suivant(i).parse().unwrap(); 2 }
            "--depuis" => { o.depuis = suivant(i).parse().unwrap(); 2 }
            "--lot" => { o.lot = suivant(i).parse().unwrap(); 2 }
            "--keep" => { o.keep = suivant(i).parse().unwrap(); 2 }
            "--moe-topk" => { o.moe_topk = suivant(i).parse().unwrap(); 2 }
            "--attn-window" => { o.attn_window = suivant(i).parse().unwrap(); 2 }
            "--swa-pattern" => { o.swa_pattern = Some(suivant(i).parse().unwrap()); 2 }
            "--attn-sinks" => { o.attn_sinks = suivant(i).parse().unwrap(); o.attn_sinks_impose = true; 2 }
            "--attn-topk" => { o.attn_topk = suivant(i).parse().unwrap(); 2 }
            "--qk-topk" => { o.qk_topk = suivant(i).parse().unwrap(); 2 }
            "--hebbian" => { o.hebb_layer = Some(suivant(i).parse().unwrap()); 2 }
            "--hebb-diff" => { o.hebb_diff = Some(suivant(i).parse().unwrap()); 2 }
            "--hebb-eta" => { o.hebb_eta = suivant(i).parse().unwrap(); 2 }
            "--hebb-clamp" => { o.hebb_clamp = suivant(i).parse().unwrap(); 2 }
            "--hebb-q" => { o.hebb_q = suivant(i).parse().unwrap(); 2 }
            "--hebb-out" => { o.hebb_out = suivant(i).clone(); 2 }
            "--act-thresh" => { o.act_thresh = suivant(i).parse().unwrap(); 2 }
            "--act-topk" => { o.act_topk = suivant(i).parse().unwrap(); 2 }
            "--topk-q" => { o.topk_proj[0] = suivant(i).parse().unwrap(); 2 }
            "--topk-k" => { o.topk_proj[1] = suivant(i).parse().unwrap(); 2 }
            "--topk-v" => { o.topk_proj[2] = suivant(i).parse().unwrap(); 2 }
            "--topk-o" => { o.topk_proj[3] = suivant(i).parse().unwrap(); 2 }
            "--topk-gate" => { o.topk_proj[4] = suivant(i).parse().unwrap(); 2 }
            "--topk-up" => { o.topk_proj[5] = suivant(i).parse().unwrap(); 2 }
            "--topk-down" => { o.topk_proj[6] = suivant(i).parse().unwrap(); 2 }
            "--ffn-gain" => {
                // « L:V » ou « L:V,L:V,… » : un PROFIL, pas seulement un réglage isolé. Le
                // profil mesuré n'est pas plat (couche 0 à 0,75, couche 1 à 0,5), et la
                // question « les gains se composent-ils ? » demande de les poser ensemble.
                let spec = suivant(i).clone();
                let mut paires: Vec<(usize, f32)> = Vec::new();
                for morceau in spec.split(',') {
                    let v: Vec<&str> = morceau.split(':').collect();
                    if v.len() != 2 {
                        eprintln!("--ffn-gain attend « couche:valeur » ou « c:v,c:v » — reçu \
« {morceau} »");
                        std::process::exit(2);
                    }
                    match (v[0].parse::<usize>(), v[1].parse::<f32>()) {
                        (Ok(c), Ok(g)) => paires.push((c, g)),
                        _ => {
                            eprintln!("--ffn-gain : « {morceau} » n'est pas « couche:valeur »");
                            std::process::exit(2);
                        }
                    }
                }
                o.ffn_gain = Some(paires);
                2
            }
            "--bits-attn" => { if suivant(i).parse::<u32>().unwrap() == 6 { o.b6 |= 2; } 2 }
            "--bits-ffn" => { if suivant(i).parse::<u32>().unwrap() == 6 { o.b6 |= 1; } 2 }
            // --- drapeaux booléens : UN argument
            "--flux" => { o.flux = true; 1 }
            "--flux-liste" => { o.flux_liste = true; 1 }
            "--flux-blocs" => { o.flux_blocs = true; 1 }
            "--session" => { o.session = true; o.flux = true; 1 }
            "--chat" => { o.chat = true; 1 }
            "--dense" => { o.dense = true; 1 }
            "--auto" => { o.auto = true; 1 }
            "--push" => { o.auto = false; o.dense = false; 1 }
            "--pin" => { o.pin = true; 1 }
            "--sans-fenetre" => { o.sans_fenetre = true; 1 }
            "--sans-yarn" => { o.sans_yarn = true; 1 }
            "--act-renorm" => { o.act_renorm = true; 1 }
            "--materiel" => { o.materiel = true; 1 }
            "--config" => { o.config = true; 1 }
            "--sonder-engram" => { o.sonder_engram = suivant(i).parse().unwrap_or(1000); 2 }
            "--engram-adresses" => { o.engram_adresses = Some(suivant(i).clone()); 2 }
            "--bloc" if i + 1 < args.len() => { o.bloc = Some(suivant(i).clone()); 2 }
            "--tete-garantie" if i + 1 < args.len() => {
                o.tete_garantie = Some(suivant(i).clone()); 2 }
            "--tete-restreinte" if i + 1 < args.len() => {
                o.tete_restreinte = Some(suivant(i).clone()); 2 }
            "--profil-neurones" => { o.profil_neurones = true; 1 }
            // Le profil de perplexité PAR PROFONDEUR (tranches de 256 positions)
            // existait dans le code — seaux, affichage, commentaires — mais
            // AUCUN drapeau ne l'activait : `ppl_profil` restait faux, et la
            // ligne « une perplexité qui MONTE avec la position ne dit pas la
            // même chose qu'une perplexité uniformément mauvaise » ne pouvait
            // jamais s'imprimer. Relevé au bloc 19, en cherchant à lire le profil
            // d'une passe de 1 024 jetons (`--ppl-profil` était inconnu).
            "--ppl-profil" => { o.ppl_profil = true; 1 }
            "--harmony" => { o.harmony = Some("alterne".into()); 1 }
            "--harmony-assistant" => { o.harmony = Some("assistant".into()); 1 }
            "--harmony-user" => { o.harmony = Some("user".into()); 1 }
            "--harmony-suite" => { o.harmony = Some("suite".into()); 1 }
            "--q4" => { o.q4 |= 3; 1 }
            "--q4-ffn" => { o.q4 = (o.q4 & 4) | 1; 1 }
            "--q4-attn" => { o.q4 = (o.q4 & 4) | 2; 1 }
            "--q4-tout" => { o.q4 |= 7; 1 }
            // Inconnu : on avance d'UN cran, jamais de deux — et on le RETIENT,
            // pour le dire à la fin plutôt que de l'avaler.
            _ => {
                // `--xxx` bien sûr, mais aussi `-keep` (un seul tiret) : c'est une
                // faute de frappe, pas un nombre négatif — un `-5` n'a pas de
                // lettre après le tiret.
                let a = &args[i];
                let lettre = a.len() > 1 && a.as_bytes()[1].is_ascii_alphabetic();
                if a.starts_with("--") || (a.starts_with('-') && lettre) {
                    o.inconnus.push(a.clone());
                }
                1
            }
        };
        i += pas;
    }
    if !o.inconnus.is_empty() {
        eprintln!("[options] {} drapeau(x) INCONNU(S), donc sans effet : {}",
                  o.inconnus.len(), o.inconnus.join(" "));
        eprintln!("[options] (une faute de frappe suffit — `--options-actives` montre \
ce que le moteur applique vraiment)");
        if o.options_strict {
            eprintln!("[options] --options-strict : arrêt (un script ne doit pas \
continuer avec un drapeau qui n'existe pas)");
            std::process::exit(2);
        }
    }
    if o.pin { engine::EPINGLER.store(true, std::sync::atomic::Ordering::Relaxed); }
    if o.bits > 0 { list::BITS_POIDS.store(o.bits, std::sync::atomic::Ordering::Relaxed); }
    o
}

/// Ce que le cache d'experts a réellement attrapé : sans ce chiffre, un gain de
/// débit ne dit pas si c'est le cache ou le hasard du routage.
fn stats_experts(mdl: &model::Model) {
    if let Some(c) = mdl.cache_experts.as_ref() {
        println!("[gpu] experts : {} demandes, {} manques (succès {:.1} %), {} évictions, \
{:.2} Go montés sur le bus, {:.2} Go résidents",
                 c.demandes, c.manques, c.taux(), c.evictions,
                 c.octets_envoyes as f64 / 1e9, c.octets as f64 / 1e9);
    }
}

fn run_infer(opt: Options) {
    // Lu AVANT la déstructuration, qui consomme `opt`.
    let montre_options = opt.options_actives;
    // Une seule analyse de la ligne de commande (voir `analyser`) : chaque mode
    // ne fait plus que déstructurer ce dont il a besoin.
    let Options {
        ids: mut ids, ids_file, prompt, n: n_new, temp, top_p, topk, rep_pen, hist,
        flux, session, chat, ctx: ctx_opt, threads: threads_opt, abits: abits_opt,
        ctx_impose, threads_impose, abits_impose, dense, auto, q4, b6, attn_sinks_impose,
        keep, attn_window, swa_pattern, sans_fenetre, attn_sinks, attn_topk, qk_topk,
        act_thresh, act_topk, act_renorm, topk_proj, moe_topk, patch: patch_file,
        hebb_layer, hebb_q, hebb_out, hebb_diff, hebb_eta, hebb_clamp, sans_yarn, lot, ffn_gain,
        trace_flux, trace_couches, flux_forcer, ..
    } = opt;
    let path = &modele_chemin();
    // Défauts du mode INFÉRENCE : 512 jetons, la moitié des cœurs (l'attente
    // active de la barrière ne tolère pas la sursouscription), 8 bits. On prend
    // tous les cœurs physiques : mesuré, 10 threads rendent 14,3 Go/s contre
    // 22,5 à 20 — le `cpu / 2` laissait 36 % sur la table.
    let cpu = engine::coeurs_physiques();
    let ctx = if ctx_impose { ctx_opt } else { 512 };
    let n_threads = if threads_impose { threads_opt } else { cpu.max(1) };
    let abits = if abits_impose { abits_opt } else { 8 };
    let mut mdl = model::Model::load_partiel(path, ctx, n_threads, dense, keep, auto, q4, b6,
                                             opt.couches);
    if opt.tete_partielle {
        poser_tete_partielle(&mut mdl);
    }
    if let Some(f) = &opt.tete_restreinte {
        poser_tete_restreinte(&mut mdl, f);
    }
    // C2/C6 : la fusion d'états doit vouloir dire la MÊME chose en inférence qu'en
    // perplexité — c'est ici qu'on génère, donc c'est ici que la greffe se voit.
    appliquer_fusion(&mut mdl, opt.fusion_etat.clone(), opt.fusion_alpha, opt.fusion_pos,
                     opt.etat_sortie.clone(), opt.etat_pos);
    if let Some(f) = &opt.tete_garantie {
        let mut ids: Vec<u32> = Vec::new();
        if let Ok(t) = std::fs::read_to_string(f) {
            for x in t.split(|c: char| c == ',' || c.is_whitespace()) {
                if let Ok(v) = x.trim().parse::<u32>() { ids.push(v); }
            }
        }
        ids.sort_unstable();
        ids.dedup();
        if ids.is_empty() {
            eprintln!("[tete-garantie] {f} ne contient aucun identifiant : rien à faire");
        } else {
            mdl.tete_garantie = Some(ids);
            mdl.preparer_normes_tete();
            println!("[tete-garantie] {} candidats sur {} ({:.1} %) — la sortie reste \
IDENTIQUE, seule la lecture change", mdl.tete_garantie.as_ref().unwrap().len(),
                     mdl.cfg.vocab, 100.0 * mdl.tete_garantie.as_ref().unwrap().len() as f64
                     / mdl.cfg.vocab as f64);
        }
    }
    poser_niveaux(&mut mdl, abits, "inférence");
    mdl.moe_topk = moe_topk;
    mdl.act_thresh = act_thresh;
    mdl.act_topk = act_topk;
    mdl.lot = lot.max(1);
    mdl.act_renorm = act_renorm;
    mdl.act_topk_proj = topk_proj;
    if sans_fenetre { mdl.attn_window = 0; }
    if attn_window > 0 { mdl.attn_window = attn_window; }
    if let Some(p) = swa_pattern { mdl.swa_pattern = p; }
    // `impose` et non `> 0` : c'est ce qui rend `--attn-sinks 0` capable
    // d'ÉTEINDRE les puits (le défaut vaut 4 quand le modèle ne déclare pas de
    // fenêtre). Un garde `> 0` transformait « zéro puits » en « laisse le défaut ».
    if attn_sinks_impose { mdl.attn_sinks = attn_sinks; }
    avertir_puits_inertes(&mdl, attn_sinks_impose);
    // `--trace-flux` était ignoré en inférence : on le branche, comme en
    // perplexité — une trace est un enregistrement du flux, elle n'a rien de
    // spécifique à la mesure de perplexité.
    if let Some(chemin) = trace_flux.as_deref() {
        match model::TraceFlux::nouveau(chemin, trace_couches.clone(), mdl.cfg.hidden,
                                        mdl.cfg.n_layer) {
            Ok(t) => { println!("[trace] flux enregistré dans {chemin}"); mdl.trace = Some(t); }
            Err(e) => eprintln!("[trace] impossible d'écrire {chemin} : {e}"),
        }
    }
    // Le REJEU aussi : `--flux-forcer` était ignoré en inférence, sans un mot.
    if let Some(chemin) = flux_forcer.as_deref() {
        match model::FluxRelecteur::lire(chemin) {
            Ok(r) => {
                println!("[flux] rejeu depuis {chemin} : {} listes enregistrées",
                         r.listes.len() + r.listes_blocs.len());
                mdl.flux_force = Some(r);
            }
            Err(e) => eprintln!("[flux] lecture impossible de {chemin} : {e}"),
        }
    }
    // `--ffn-gain` était appliqué en perplexité et JAMAIS déstructuré ici : la
    // sortie était rigoureusement identique avec et sans le drapeau.
    if let Some(gs) = ffn_gain {
        let liste: Vec<String> = gs.iter().map(|(l, g)| format!("couche {l} × {g}")).collect();
        println!("gain FFN : {}", liste.join(" · "));
        mdl.ffn_gain = Some(gs);
    }
    // Appliqués en perplexité depuis toujours, oubliés ici : la déstructuration
    // unique les rend visibles (le compilateur signale tout champ non lu).
    mdl.attn_topk = attn_topk;
    mdl.qk_topk = qk_topk;
    if sans_yarn { mdl.cfg_yarn_off(); }
    if act_topk > 0 || act_thresh > 0.0 {
        println!("parcimonie imposée : k-WTA garde {:.1} %{}",
                 act_topk as f32 / 10.0,
                 if act_thresh > 0.0 { format!(", seuil {:.1} %", act_thresh * 100.0) } else { String::new() });
    }
    // Le tableau de bord vient EN DERNIER : il doit montrer l'état FINAL. Placé
    // plus haut, il affichait `ffn_gain None` alors que `--ffn-gain` venait
    // d'être appliqué trois lignes plus bas — un tableau de bord qui ment sur
    // l'ordre des affectations ne vaut pas mieux que pas de tableau du tout.
    if montre_options {
        options_actives(&mdl, "inférence", ctx_impose, dense, keep, attn_sinks_impose);
    }
    if chat {
        mdl.stop_id = build_tokenizer(&mdl.g).special_id("<|im_end|>");
    }
    let cfg = &mdl.cfg;
    let _ = &prompt;
    println!("Qwen2 · {} couches · hidden {} · {} têtes / {} KV · FFN {} · vocab {}",
             cfg.n_layer, cfg.hidden, cfg.n_head, cfg.n_kv_head, cfg.ffn, cfg.vocab);

    if let Some(p) = &prompt {
        let tk = build_tokenizer(&mdl.g);
        // Le gabarit de conversation n'est appliqué que si le modèle possède
        // les jetons correspondants. gpt-oss utilise un autre format
        // (<|start|>user<|message|>…) : faute de l'implémenter, mieux vaut une
        // invite brute qu'une panique.
        let gabarit_qwen = chat && tk.special_id("<|im_start|>").is_some()
                                  && tk.special_id("<|im_end|>").is_some();
        if chat && !gabarit_qwen {
            eprintln!("[chat] gabarit inconnu pour ce modèle : invite brute");
        }
        // Gabarit **harmony** (gpt-oss) : canaux et marqueurs dédiés. Le modèle
        // est entraîné dessus ; une invite brute le fait répondre, mais hors de
        // sa distribution.
        let gabarit_harmony = chat
            && tk.special_id("<|start|>").is_some()
            && tk.special_id("<|message|>").is_some();
        if gabarit_harmony {
            let deb = tk.special_id("<|start|>").unwrap();
            let msg = tk.special_id("<|message|>").unwrap();
            let fin = tk.special_id("<|end|>").unwrap();
            for (role, texte) in [("system", "You are a helpful assistant."), ("user", p.as_str())] {
                ids.push(deb);
                ids.extend(tk.encode(role));
                ids.push(msg);
                ids.extend(tk.encode(texte));
                ids.push(fin);
            }
            ids.push(deb);
            ids.extend(tk.encode("assistant"));
            mdl.stop_id = tk.special_id("<|return|>");
            mdl.stop_id2 = Some(fin);
            eprintln!("[chat] gabarit HARMONY appliqué (gpt-oss)");
        }
        if gabarit_qwen {
            // gabarit Qwen2.5-Instruct, tokens spéciaux insérés tels quels
            let im_start = tk.special_id("<|im_start|>").unwrap();
            let im_end = tk.special_id("<|im_end|>").unwrap();
            ids.push(im_start);
            ids.extend(tk.encode("user\n"));
            ids.extend(tk.encode(p));
            ids.push(im_end);
            ids.extend(tk.encode("\n"));
            ids.push(im_start);
            ids.extend(tk.encode("assistant\n"));
        } else {
            ids = tk.encode(p);
        }
        println!("prompt : {} tokens", ids.len());
    }
    if let Some(f) = &ids_file {
        ids = std::fs::read_to_string(f).unwrap_or_default()
            .split(|c: char| c == ',' || c.is_whitespace())
            .filter(|t| !t.is_empty())
            .filter_map(|t| t.parse().ok())
            .collect();
        println!("ids depuis {f} : {} tokens", ids.len());
    }
    if let Some(f) = &patch_file {
        let pt = model::Patch::load(f).expect("chargement du greffon");
        let norme = |v: &[f32]| v.iter().map(|x| x * x).sum::<f32>().sqrt();
        println!("greffon : couche {}, |u|={:.3} |v|={:.3} |d|={:.3}",
                 pt.layer, norme(&pt.u), norme(&pt.v), norme(&pt.d));
        mdl.patch = Some(pt);
    }
    if let Some(l) = hebb_layer {
        let n_out = mdl.cfg.ffn;
        let n_in = mdl.cfg.hidden;
        mdl.hebb = Some(model::Hebb::new(l, n_out, n_in, hebb_q));
        println!("capteur hebbien : couche {l}, projection gate ({n_out} x {n_in}), \
                  quantile {hebb_q} -> {hebb_out}");
    }
    if let Some(l) = hebb_diff {
        let (n_out, n_in) = (mdl.cfg.ffn, mdl.cfg.hidden);
        let mut hd = model::HebbDiff::new(l, n_out, n_in, hebb_eta, hebb_clamp);
        if let Ok(c) = std::env::var("DRAVE_HEBB_CHARGER") { hd.charger(&c); }
        mdl.hebb_diff = Some(hd);
        // **Il CHANGE la sortie : il le dit, et il dit comment.** L'adaptateur
        // `D` s'ajoute à la projection, donc la matrice effective devient `W + D`
        // (voir `HebbDiff`). Rien n'est écrit dans le fichier du modèle.
        println!("[hebb-diff] ADAPTATEUR ACTIF — couche {l}, gate ({n_out}×{n_in}), \
eta {hebb_eta:e}, écrêtage ±{hebb_clamp}. La règle est LOCALE et forward-only : \
Δx = x(t)−x(t−1), Δy = y(t)−y(t−1), D += η·Δy⊗Δx, et y' = y + D·x. La matrice \
effective est W+D : ce modèle N'EST PLUS celui du fichier, et il se mesure comme tel.");
    }
    if ids.is_empty() && !session {
        eprintln!("rien à générer : --ids ou --prompt requis");
        return;
    }

    mdl.reset_events();

    // ---------------------------------------------------------------- session
    // Boucle interactive : chaque tour est ajouté à la conversation et
    // retraité en entier. L'invite complète repasse donc par le modèle à chaque
    // tour (coût quadratique en nombre de tours), mais c'est exact, et le cache
    // KV n'a pas à être découpé par tour.
    if session {
        let tks = build_tokenizer(&mdl.g);
        let mut conversation = String::new();
        let mut n_tour = 0usize;
        loop {
            eprint!("vous> ");
            let _ = std::io::Write::flush(&mut std::io::stderr());
            let mut ligne = String::new();
            if std::io::stdin().read_line(&mut ligne).unwrap_or(0) == 0 { break; }
            let q = ligne.trim();
            if q.is_empty() { continue; }
            if q == "/quit" || q == "/q" { break; }
            conversation.push_str(&format!(
                "<|im_start|>user\n{q}<|im_end|>\n<|im_start|>assistant\n"));
            let ids = tks.encode(&conversation);
            // Garde-fou : la conversation doit tenir dans le contexte, avec de
            // quoi générer. On garde la fin, on jette le début.
            let ids = if ids.len() + n_new + 8 > ctx {
                let garde = ctx.saturating_sub(n_new + 8);
                let mut tronque = tks.encode("<|im_start|>system\n[conversation tronquée]<|im_end|>\n");
                tronque.extend_from_slice(&ids[ids.len().saturating_sub(garde)..]);
                tronque
            } else { ids };
            print!("assistant> ");
            let _ = std::io::Write::flush(&mut std::io::stdout());
            let mut accumules: Vec<u32> = Vec::new();
            let mut deja = String::new();
            let mut affiche = |t: u32| {
                accumules.push(t);
                let texte = tks.decode(&accumules);
                if texte.len() > deja.len() {
                    print!("{}", &texte[deja.len()..]);
                    let _ = std::io::Write::flush(&mut std::io::stdout());
                    deja = texte;
                }
            };
            let (out, st) = mdl.generate(&ids, n_new, temp, top_p, rep_pen, hist,
                                         Some(&mut affiche));
            println!();
            eprintln!("  [{:.1} tok/s, {} jetons]", st.n_gen as f64 / st.gen_s.max(1e-9), st.n_gen);
            conversation.push_str(&tks.decode(&out));
            conversation.push('\n');
            n_tour += 1;
            if n_tour >= 50 { break; }
        }
        return;
    }

    // Le mode `--topk` (diagnostic) appelle `forward` position par position SANS
    // passer par `generate` : il lui faut la même borne de contexte, sinon
    // l'assertion de `forward` fait tomber le processus (relevé par la relecture
    // de clôture : `--infer --topk` avec une invite trop longue).
    let ids: Vec<u32> = if ids.len() + n_new + 8 > ctx {
        let garde = ctx.saturating_sub(n_new + 8).max(1);
        println!("[contexte] invite de {} jetons > {} (ctx {} − {} de génération) : \
troncature aux {} derniers", ids.len(), garde, ctx, n_new, garde);
        ids[ids.len().saturating_sub(garde)..].to_vec()
    } else { ids };
    // La position « dernière » se résout ICI, APRÈS la troncature : la résoudre avant
    // viserait un jeton que la troncature a retiré, et la greffe tomberait à côté —
    // exactement l'erreur d'un jeton qui avait été commise à la main.
    // La capture se résout ICI AUSSI, dans la numérotation de l'inférence : c'est la
    // même longueur d'invite qui sert au calcul et à la capture, donc plus de décalage.
    if let Some((f, ks)) = opt.etat_fin.as_ref() {
        if !ids.is_empty() {
            let positions: Vec<usize> = ks.iter()
                .map(|k| ids.len() - (*k).clamp(1, ids.len())).collect();
            println!("  capture d'état    : position(s) {positions:?} (depuis la fin d'une invite \
de {} jetons) écrite(s) dans {f}", ids.len());
            mdl.etat_sortie = Some((f.clone(), positions));
        }
    }
    if opt.fusion_dernier && !ids.is_empty() {
        mdl.fusion_pos = ids.len() - 1;
        println!("  fusion            : position DERNIÈRE de l'invite = {} (invite de {} \
jetons, comptée ici et non devinée)", mdl.fusion_pos, ids.len());
    }
    let (out, st) = if topk > 0 {
        // pas-à-pas : utile pour confronter les logits à la référence numpy
        let t0 = Instant::now();
        let mut last = Vec::new();
        for (pos, &t) in ids.iter().enumerate() { last = mdl.forward(t, pos); }
        let mut out = Vec::with_capacity(n_new);
        for step in 0..n_new {
            let lg = mdl.logits(&last);
            let mut rank: Vec<u32> = (0..lg.len() as u32).collect();
            rank.sort_unstable_by(|&a, &b| lg[b as usize].partial_cmp(&lg[a as usize]).unwrap());
            print!("  pas {step:2} : ");
            for &i in &rank[..topk] { print!("{i}({:.4}) ", lg[i as usize]); }
            println!();
            let next = rank[0];
            out.push(next);
            last = mdl.forward(next, ids.len() + step);
        }
        let dt = t0.elapsed().as_secs_f64();
        let st = model::Stats { events: mdl.events_total(), prompt_s: dt / 2.0, gen_s: dt / 2.0,
                                n_prompt: ids.len(), n_gen: out.len() };
        (out, st)
    } else {
        // Sortie en flux : on décode le texte produit jusqu'ici et on n'imprime
        // que le delta — c'est ce qui évite de couper un caractère multi-octets.
        let tk = build_tokenizer(&mdl.g);
        let mut accumules: Vec<u32> = Vec::new();
        let mut deja = String::new();
        let mut affiche = |t: u32| {
            accumules.push(t);
            let texte = tk.decode(&accumules);
            if texte.len() > deja.len() {
                print!("{}", &texte[deja.len()..]);
                let _ = std::io::Write::flush(&mut std::io::stdout());
                deja = texte;
            }
        };
        let cb: Option<&mut dyn FnMut(u32)> = if flux { Some(&mut affiche) } else { None };
        mdl.generate(&ids, n_new, temp, top_p, rep_pen, hist, cb)
    };
    if prompt.is_some() {
        let tk = build_tokenizer(&mdl.g);
        let mut all: Vec<u32> = ids.clone();
        all.extend(all_ids_of(&out));
        println!("--- texte ---");
        print!("{}", tk.decode(&all));
        println!("\n--- ids générés : {:?}", &out);
    } else {
        println!("tokens générés : {:?}", &out);
    }
    println!("\n--- mesure ---");
    println!("prompt  : {} tokens en {:.3} s  ({:.1} tok/s, TTFT {:.1} ms)",
             st.n_prompt, st.prompt_s, st.n_prompt as f64 / st.prompt_s,
             st.prompt_s * 1e3 / st.n_prompt.max(1) as f64);
    println!("généré  : {} tokens en {:.3} s  ({:.2} tok/s)",
             st.n_gen, st.gen_s, st.n_gen as f64 / st.gen_s);
    stats_experts(&mdl);
    println!("événements : {} au total, {:.1} par token",
             st.events, st.events as f64 / (st.n_prompt + st.n_gen) as f64);
    let pa = mdl.paires;
    let ng = (st.n_prompt + st.n_gen).max(1) as f64;
    println!("paires (poids × activation) : {} au total, {:.1} M par token — attention {:.1} M · experts {:.1} M · partagé {:.1} M",
             pa.iter().sum::<u64>(), pa.iter().sum::<u64>() as f64 / ng / 1e6,
             pa[0] as f64 / ng / 1e6, pa[1] as f64 / ng / 1e6, pa[2] as f64 / ng / 1e6);
    rapport_hebb_diff(&mdl);
    // SAUVEGARDE de `D` après une passe d'adaptation : c'est ce qui rend le
    // test hors échantillon possible (adapter sur A, évaluer sur B).
    if let (Ok(f), Some(hd)) = (std::env::var("DRAVE_HEBB_D_SAUVE"), mdl.hebb_diff.as_ref()) {
        use std::io::Write;
        let mut fic = std::fs::File::create(&f).expect("écriture de D");
        for v in &hd.d { fic.write_all(&v.to_le_bytes()).unwrap(); }
        eprintln!("[hebb-diff] D sauvé dans {f} : {} valeurs", hd.d.len());
    }
    if let Some(hb) = mdl.hebb.as_ref() {
        use std::io::Write;
        let mut f = std::fs::File::create(&hebb_out).expect("création du fichier hebbien");
        for v in &hb.h { f.write_all(&v.to_le_bytes()).unwrap(); }
        f.flush().unwrap();
        let hb_ms = 0.0;   // le coût est mesuré à part
        let _ = hb_ms;
        println!("capteur hebbien : {} activations sur {} tokens, trace écrite dans {} ({:.1} Mo)",
                 hb.n_fire, hb.n_token,
                 hebb_out, (hb.h.len() * 4) as f64 / 1e6);
    }
    let n_tok = (st.n_prompt + st.n_gen) as f64;
    let p = mdl.prof;
    println!("postes (ms/token) : matvec-attn {:.1} | rope {:.1} | attention {:.1} | matvec+mlp {:.1} | total mesuré {:.1}",
             p[0] / n_tok * 1e3, p[1] / n_tok * 1e3, p[2] / n_tok * 1e3, p[3] / n_tok * 1e3,
             (p[0] + p[1] + p[2] + p[3]) / n_tok * 1e3);

    {
        use std::sync::atomic::Ordering;
        let a = model::TETE_ACTIFS.load(Ordering::Relaxed);
        let t = model::TETE_TOTAL.load(Ordering::Relaxed);
        let n = model::TETE_APPELS.load(Ordering::Relaxed);
        if n > 0 && t > 0 {
            let pc = 100.0 * a as f64 / t as f64;
            println!("[tete] densite de l'entree : {:.1} % de coordonnees vivantes sur {n} jetons", pc);
            println!("[tete] -> un stockage par COLONNES ne lirait que ces coordonnees : \
{:.1} % de la matrice au lieu de 100 %", pc);
        }
    }

}


// --------------------------------------------------------------------------- //
// Perplexité : mesure standard de qualité, à travers le moteur d'événements
// --------------------------------------------------------------------------- //

fn all_ids_of(v: &[u32]) -> Vec<u32> { v.to_vec() }

fn meta_strings(g: &Gguf, key: &str) -> Vec<String> {
    match g.meta.get(key) {
        Some(gguf::Meta::Array(a)) => a.iter().map(|m| m.as_str().unwrap_or("").to_string()).collect(),
        _ => Vec::new(),
    }
}

fn meta_ints(g: &Gguf, key: &str) -> Vec<i32> {
    match g.meta.get(key) {
        Some(gguf::Meta::Array(a)) => a.iter().map(|m| m.as_u64().unwrap_or(0) as i32).collect(),
        _ => Vec::new(),
    }
}

fn build_tokenizer(g: &Gguf) -> tokenizer::Tokenizer {
    let pre = g.meta.get("tokenizer.ggml.pre").and_then(|m| m.as_str()).unwrap_or("").to_string();
    tokenizer::Tokenizer::new(
        meta_strings(g, "tokenizer.ggml.tokens"),
        meta_strings(g, "tokenizer.ggml.merges"),
        meta_ints(g, "tokenizer.ggml.token_type"),
        &pre,
    )
}

/// Charge une liste d'identifiants et la pose sur le modèle.
///
/// Rend `false` si le fichier est vide ou illisible — auquel cas la tête reste
/// complète, ce qui est le comportement sûr.
fn poser_tete_restreinte(mdl: &mut model::Model, fichier: &str) -> bool {
    let mut ids: Vec<u32> = Vec::new();
    if let Ok(t) = std::fs::read_to_string(fichier) {
        for x in t.split(|c: char| c == ',' || c.is_whitespace()) {
            if let Ok(v) = x.trim().parse::<u32>() { ids.push(v); }
        }
    }
    ids.sort_unstable();
    ids.dedup();
    if ids.is_empty() {
        eprintln!("[tete] {fichier} ne contient aucun identifiant utilisable : tête complète");
        return false;
    }
    println!("[tete] restreinte à {} tokens sur {} ({:.1} %) — le routeur, lui, reste global",
             ids.len(), mdl.cfg.vocab, 100.0 * ids.len() as f64 / mdl.cfg.vocab as f64);
    mdl.tete_restreinte = Some(ids);
    true
}

fn cfg_dims(m: &model::Model) -> usize { m.cfg.hidden }

/// Taille du vocabulaire, lue dans l'en-tête du GGUF sans charger le modèle.
fn mdl_cfg_vocab(path: &str) -> Option<usize> {
    // `open_meta` : le garde-fou n'a besoin que des dimensions du tenseur
    // d'embedding. Avec `open`, il lisait les 62 Go de gpt-oss AVANT que le
    // modèle ne soit chargé — deux lectures complètes du fichier par mesure.
    let g = Gguf::open_meta_auto(path).ok()?;
    g.tensor("token_embd.weight").map(|t| t.dims[0] as usize)
}

/// Tokenise un texte et imprime les identifiants — sert à vérifier le
/// pré-découpage contre une implémentation de référence.

/// Banc d'essai des noyaux GPU : la MÊME tête, trois chemins.
///
/// Il existe parce que le déport de la tête a été refusé une fois sur une
/// mesure (23 → 159 ms) : sans un banc isolé, on ne sait pas si un changement
/// de noyau aide, la mesure par jeton mélangeant tête, attention et
/// échantillonnage.
/// Erreur de Gauss, approximation d'Abramowitz-Stegun 7.1.26 (|erreur| < 1,5e-7,
/// ce qui suffit pour un GELU comparé à 1e-5 près).
fn erf(x: f32) -> f32 {
    let signe = if x < 0.0 { -1.0 } else { 1.0 };
    let x = x.abs();
    let t = 1.0 / (1.0 + 0.3275911 * x);
    let y = 1.0 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
                    - 0.284496736) * t + 0.254829592) * t * (-x * x).exp();
    signe * y
}

/// **Première tranche du chemin image** : l'embedding de patchs.
///
/// Le ViT de Qwen2.5-VL commence par une convolution 14 × 14 sur une image
/// 28 × 28 (deux patchs par côté, la taille minimale d'une fusion 2 × 2). Cette
/// tranche est isolée à dessein : si l'embedding de patchs est faux, tout ce qui
/// suit l'est aussi, et le comparer seul évite d'attribuer au modèle une erreur
/// de découpage.
fn run_banc_vision(sortie: &str) {
    use std::io::Write;
    let path = &modele_chemin();
    let g = Gguf::open_auto(path).expect("ouverture du GGUF");
    let Some(t) = g.tensor("v.patch_embd.weight") else {
        println!("pas de v.patch_embd.weight dans ce fichier");
        return;
    };
    // dims du moteur : (sortie, entrée, ky, kx)
    let (cout, cin, ky, kx) = (t.dims[0] as usize, t.dims[1] as usize,
                               t.dims[2] as usize, t.dims[3] as usize);
    let mut proj: Option<(Vec<f32>, Vec<f32>)> = None;
    println!("v.patch_embd.weight : sortie {cout} · entrée {cin} · noyau {ky}×{kx}");
    let w = g.dequant("v.patch_embd.weight");
    let mut tour: Option<Vec<f32>> = None;
    assert_eq!(w.len(), cout * cin * ky * kx, "poids de patch inattendus");
    // Image 28 × 28 déterministe : dégradé + carré central, pour que la
    // référence numpy puisse la reconstruire sans lire de fichier.
    let (cote, cotes) = (224usize, 8usize);
    let mut img = vec![0f32; cin * cote * cote];
    for y in 0..cote {
        for x in 0..cote {
            let carre = x >= 10 && x < 18 && y >= 10 && y < 18;
            for ic in 0..cin {
                let v = if carre { 1.0 }
                        else { (x as f32 + y as f32 + ic as f32) / (2.0 * cote as f32) };
                img[(ic * cote + y) * cote + x] = v;
            }
        }
    }
    // Convolution : une sortie par position de patch, sans rembourrage.
    let n_patch_cote = (cote - ky) / kx + 1;
    let n_patch = n_patch_cote * n_patch_cote;
    let mut out = vec![0f32; n_patch * cout];
    for py in 0..n_patch_cote {
        for px in 0..n_patch_cote {
            let p = py * n_patch_cote + px;
            for c in 0..cout {
                let mut acc = 0f32;
                for ic in 0..cin {
                    for yy in 0..ky {
                        for xx in 0..kx {
                            let v = img[(ic * cote + py * ky + yy) * cote + px * kx + xx];
                            acc += w[((c * cin + ic) * ky + yy) * kx + xx] * v;
                        }
                    }
                }
                out[p * cout + c] = acc;
            }
        }
    }

    let mut f = std::io::BufWriter::new(std::fs::File::create(sortie).expect("création"));
    f.write_all(&(n_patch as i32).to_le_bytes()).unwrap();
    f.write_all(&(cout as i32).to_le_bytes()).unwrap();
    for v in out.iter() { f.write_all(&v.to_le_bytes()).unwrap(); }
    if let Some((_, y)) = proj.as_ref() {
        f.write_all(&(y.len() as i32).to_le_bytes()).unwrap();
        for v in y.iter() { f.write_all(&v.to_le_bytes()).unwrap(); }
    }
    // Les poids partent à côté : la référence numpy refait le CALCUL, pas
    // l'extraction du GGUF (la lecture des tenseurs est vérifiée par --tensors).
    {
        let mut fp = std::io::BufWriter::new(
            std::fs::File::create(format!("{sortie}.poids")).expect("création des poids"));
        for v in [(cout as i32), (cin as i32), (ky as i32), (kx as i32)] {
            fp.write_all(&v.to_le_bytes()).unwrap();
        }
        for v in w.iter() { fp.write_all(&v.to_le_bytes()).unwrap(); }
    }
    // ---- Corps de la tour : LES 32 COUCHES, sans rotation 2-D ni fenêtre
    // locale (les deux points dont la convention n'est pas encore tranchée).
    // Ce qui est mesuré ici : la PLOMBERIE répétée 32 fois, plus v.post_ln.
    if g.tensor("v.blk.0.attn_q.weight").is_some() {
        let e = cout;
        let eps = g.cfg("vision.attention.layer_norm_epsilon")
            .and_then(|m| m.as_f64()).unwrap_or(1e-6) as f32;
        let n_layer = g.cfg("vision.block_count")
            .and_then(|m| m.as_u64()).unwrap_or(0) as usize;
        let norme_ln = |v: &[f32], w: &[f32], dst: &mut [f32]| {
            let moy: f32 = v.iter().sum::<f32>() / v.len() as f32;
            let var: f32 = v.iter().map(|a| (a - moy) * (a - moy)).sum::<f32>() / v.len() as f32;
            let inv = 1.0 / (var + eps).sqrt();
            for i in 0..v.len() { dst[i] = (v[i] - moy) * inv * w[i]; }
        };
        let proj_l = |x: &[f32], w: &[f32], b: &[f32], n_in: usize, n_out: usize| {
            let mut y = vec![0f32; n_out];
            for o in 0..n_out {
                let mut acc = b[o];
                for i in 0..n_in { acc += w[o * n_in + i] * x[i]; }
                y[o] = acc;
            }
            y
        };
        let mut x = out.clone();
        let mut xn = vec![0f32; e];
        let mut poids_bloc: Vec<Vec<f32>> = Vec::new();
        for l in 0..n_layer {
            let p = |n: &str| format!("v.blk.{l}.{n}");
            let ln1 = g.dequant(&p("ln1.weight"));
            let ln2 = g.dequant(&p("ln2.weight"));
            let wq = g.dequant(&p("attn_q.weight"));
            let bq = g.dequant(&p("attn_q.bias"));
            let wk = g.dequant(&p("attn_k.weight"));
            let bk = g.dequant(&p("attn_k.bias"));
            let wv = g.dequant(&p("attn_v.weight"));
            let bv = g.dequant(&p("attn_v.bias"));
            let wo = g.dequant(&p("attn_out.weight"));
            let bo = g.dequant(&p("attn_out.bias"));
            let wg = g.dequant(&p("ffn_gate.weight"));
            let bg = g.dequant(&p("ffn_gate.bias"));
            let wu = g.dequant(&p("ffn_up.weight"));
            let bu = g.dequant(&p("ffn_up.bias"));
            let wd = g.dequant(&p("ffn_down.weight"));
            let bd = g.dequant(&p("ffn_down.bias"));
            let nff = wg.len() / e;
            let (mut qq, mut kk, mut vv) = (Vec::new(), Vec::new(), Vec::new());
            for pi in 0..n_patch {
                norme_ln(&x[pi * e..(pi + 1) * e], &ln1, &mut xn);
                qq.extend(proj_l(&xn, &wq, &bq, e, e));
                kk.extend(proj_l(&xn, &wk, &bk, e, e));
                vv.extend(proj_l(&xn, &wv, &bv, e, e));
            }
            // Rotation 2-D (mRoPE) : quatre blocs de la dimension de tête, lus
            // dans clip.cpp — le tenseur `positions` y est rempli (ligne,
            // colonne, ligne, colonne), donc les blocs 0 et 2 tournent selon la
            // LIGNE et les blocs 1 et 3 selon la COLONNE. Chaque couple d'un
            // bloc est (i, i + quart/2), la convention « moitié tournée ».
            // Convention exacte, lue dans ggml_mrope_cache_init :
            //   * les paires sont CONSÉCUTIVES : (i0, i0+1) ;
            //   * le secteur vaut (i0/2) % sect_dims, avec quatre sections de
            //     hd/4 dimensions — donc les hd/4 premières paires (la moitié
            //     « ligne » de la tête) tournent selon la LIGNE, les suivantes
            //     selon la COLONNE ;
            //   * l'échelle de fréquences CONTINUE d'un bloc à l'autre
            //     (theta *= theta_scale), donc l'exposant suit l'indice de paire
            //     GLOBAL sur toute la tête.
            let nh_t = 16usize;                       // vision.head_count du mmproj
            let hd_t = e / nh_t;
            let n_cote = (cote - kx) / kx + 1;
            let base_rot = 10000.0f32;
            let tourner = |v: &mut [f32], ligne: f32, colonne: f32| {
                let paires = hd_t / 2;
                for i in 0..paires {
                    let pos = if i < paires / 2 { ligne } else { colonne };
                    let theta = pos * base_rot.powf(-2.0 * i as f32 / hd_t as f32);
                    let (c, sn) = (theta.cos(), theta.sin());
                    let a = v[2 * i];
                    let b = v[2 * i + 1];
                    v[2 * i] = a * c - b * sn;
                    v[2 * i + 1] = a * sn + b * c;
                }
            };
            // Permutation « colonne-majeur » des couches FENÊTRÉES : clip.cpp
            // transpose la grille des unités de fusion avant d'empaqueter les
            // positions (`idx_col[u_col] = u_row`), si bien qu'un patch (r, c)
            // reçoit les positions de (c, r). Ce n'est donc pas qu'un masque :
            // la fenêtre change aussi l'ordre des positions.
            let complete_rot = (l + 1) % 8 == 0;
            for pi in 0..n_patch {
                let (ligne, colonne) = if complete_rot {
                    ((pi / n_cote) as f32, (pi % n_cote) as f32)
                } else {
                    ((pi % n_cote) as f32, (pi / n_cote) as f32)
                };
                for hh in 0..nh_t {
                    let deb = pi * e + hh * hd_t;
                    let v = &mut qq[deb..deb + hd_t];
                    tourner(v, ligne, colonne);
                    let vk = &mut kk[deb..deb + hd_t];
                    tourner(vk, ligne, colonne);
                }
            }
            let scale = 1.0 / (e as f32).sqrt();
            let mut att = vec![0f32; n_patch * e];
            let mut sc = vec![0f32; n_patch];
            // Fenêtre locale : Qwen2.5-VL a une couche COMPLÈTE toutes les huit
            // (indices 7, 15, 23, 31) et des couches LOCALES ailleurs ; la
            // fenêtre est un bloc de 4 × 4 jetons fusionnés, soit 8 × 8 patchs.
            let complete = complete_rot;
            let n_cote_grille = (n_patch as f64).sqrt().round() as usize;
            for pi in 0..n_patch {
                let q = &qq[pi * e..(pi + 1) * e];
                for t in 0..n_patch {
                    if !complete {
                        let (ly, lx) = (pi / n_cote_grille, pi % n_cote_grille);
                        let (ty, tx) = (t / n_cote_grille, t % n_cote_grille);
                        let (w, h) = (4usize, 4usize);
                        if (ly / (2 * h)) != (ty / (2 * h)) || (lx / (2 * w)) != (tx / (2 * w)) {
                            sc[t] = f32::NEG_INFINITY;
                            continue;
                        }
                    }
                    let mut acc = 0f32;
                    for i in 0..e { acc += q[i] * kk[t * e + i]; }
                    sc[t] = acc * scale;
                }
                let mx = sc.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
                let mut somme = 0f32;
                for v in sc.iter_mut() { let z = (*v - mx).exp(); *v = z; somme += z; }
                for t in 0..n_patch {
                    let w = sc[t] / somme;
                    for i in 0..e { att[pi * e + i] += w * vv[t * e + i]; }
                }
            }
            for pi in 0..n_patch {
                let o = proj_l(&att[pi * e..(pi + 1) * e], &wo, &bo, e, e);
                for i in 0..e { x[pi * e + i] += o[i]; }
                norme_ln(&x[pi * e..(pi + 1) * e], &ln2, &mut xn);
                let g_t = proj_l(&xn, &wg, &bg, e, nff);
                let u_t = proj_l(&xn, &wu, &bu, e, nff);
                let mut act = vec![0f32; nff];
                for i in 0..nff {
                    let z = g_t[i];
                    act[i] = (z / (1.0 + (-z).exp())) * u_t[i];
                }
                let d_t = proj_l(&act, &wd, &bd, nff, e);
                for i in 0..e { x[pi * e + i] += d_t[i]; }
            }
            if l == 0 { poids_bloc = vec![ln1, ln2, wq, bq, wk, bk, wv, bv, wo, bo,
                                         wg, bg, wu, bu, wd, bd]; }
        }
        let post_ln = g.dequant("v.post_ln.weight");
        for pi in 0..n_patch {
            norme_ln(&x[pi * e..(pi + 1) * e], &post_ln, &mut xn);
            x[pi * e..(pi + 1) * e].copy_from_slice(&xn);
        }
        {
            let mut fb = std::io::BufWriter::new(
                std::fs::File::create(format!("{sortie}.bloc")).expect("création"));
            for v in [(n_patch as i32), (e as i32), (n_layer as i32)] {
                fb.write_all(&v.to_le_bytes()).unwrap();
            }
            for v in x.iter() { fb.write_all(&v.to_le_bytes()).unwrap(); }
        }
        tour = Some(x.clone());
        println!("tour : {n_layer} couches × {n_patch} patchs × {e} · |sortie| = {:.4} · 4 premières {:?}",
                 x.iter().map(|v| v * v).sum::<f32>().sqrt(),
                 &x[..4].iter().map(|v| (v * 1e4).round() / 1e4).collect::<Vec<_>>());
        let _ = poids_bloc;
    }

    // ---- Projecteur : fusion 2 × 2 des patchs puis mm.0 → GELU → mm.2.
    // La fusion est en ordre RASTER (les quatre patchs d'un groupe de 2 × 2
    // concaténés ligne par ligne) : c'est la convention de llama.cpp, et c'est
    // la seule hypothèse non vérifiable ici — elle ne se confirmerait qu'en
    // comparant la SORTIE complète à une implémentation de référence.
    if let (Some(t0), Some(t2)) = (g.tensor("mm.0.weight"), g.tensor("mm.2.weight")) {
        let (n0, n1) = (t0.dims[0] as usize, t0.dims[1] as usize);
        let (n2, n3) = (t2.dims[0] as usize, t2.dims[1] as usize);
        let w0 = g.dequant("mm.0.weight");
        let b0 = g.dequant("mm.0.bias");
        let w2 = g.dequant("mm.2.weight");
        let b2 = g.dequant("mm.2.bias");
        println!("projecteur : mm.0 {n1}→{n0} · mm.2 {n3}→{n2}");
        // GELU exact (erf), comme dans la tour de vision.
        let gelu = |x: f32| 0.5 * x * (1.0 + erf(x / std::f32::consts::SQRT_2));
        // Un groupe de fusion 2 × 2 = quatre patchs concaténés (4 × 1280 = 5120),
        // puis mm.0 → GELU → mm.2 → 3584 valeurs PAR GROUPE. Sur une image de
        // 224 px il y a 64 groupes : la version qui ne traitait qu'un groupe
        // (celle du banc 28 × 28) ne veut plus rien dire.
        let n_cote_p = (n_patch as f64).sqrt().round() as usize;
        let n_groupe = (n_cote_p / 2) * (n_cote_p / 2);
        let mut y = vec![0f32; n_groupe * n2];
        let source = tour.clone().unwrap_or_else(|| out.clone());
        let mut fusion = vec![0f32; n1];
        for g in 0..n_groupe {
            let (gy, gx) = (2 * (g / (n_cote_p / 2)), 2 * (g % (n_cote_p / 2)));
            for dy in 0..2 {
                for dx in 0..2 {
                    let p = (gy + dy) * n_cote_p + (gx + dx);
                    fusion[(dy * 2 + dx) * cout..(dy * 2 + dx + 1) * cout]
                        .copy_from_slice(&source[p * cout..(p + 1) * cout]);
                }
            }
            let mut h = vec![0f32; n0];
            for o in 0..n0 {
                let mut acc = b0[o];
                for i in 0..n1 { acc += w0[o * n1 + i] * fusion[i]; }
                h[o] = gelu(acc);
            }
            for o in 0..n2 {
                let mut acc = b2[o];
                for i in 0..n3 { acc += w2[o * n3 + i] * h[i]; }
                y[g * n2 + o] = acc;
            }
        }
        {
            let mut f2 = std::io::BufWriter::new(
                std::fs::File::create(format!("{sortie}.projecteur")).expect("création"));
            for v in [(n0 as i32), (n1 as i32), (n2 as i32), (n3 as i32)] {
                f2.write_all(&v.to_le_bytes()).unwrap();
            }
            for v in w0.iter().chain(b0.iter()).chain(w2.iter()).chain(b2.iter()) {
                f2.write_all(&v.to_le_bytes()).unwrap();
            }
        }
        println!("projecteur : {n_groupe} groupes × {n2} valeurs, |sortie| = {:.4}, 4 premières {:?}",
                 y.iter().map(|v| v * v).sum::<f32>().sqrt(),
                 &y[..4].iter().map(|v| (v * 1e4).round() / 1e4).collect::<Vec<_>>());
        proj = Some((Vec::new(), y));
    }

    // ---- Injection : le moteur consomme-t-il un embedding d'image ?
    // `DRAVE_VISION_TEXTE=<modele.gguf>` charge le modèle de texte et lui impose le
    // PREMIER jeton d'image via `Model::emb_imposee` — le chemin qui manquait
    // (« forward partait toujours de token_embd »). C'est un contrôle de
    // PLOMBERIE : le moteur ne panique pas, il rend des logits d'échelle
    // normale. La qualité, elle, demanderait la comparaison complète.
    if let Some((_, y)) = proj.as_ref() {
        let n_emb = 3584usize;
        let n_tok = y.len() / n_emb;
        println!("injection : {n_tok} jetons × {n_emb} disponibles");
        let chemin = std::env::var("DRAVE_VISION_TEXTE").unwrap_or_default();
        if !chemin.is_empty() {
            let mut mdl = model::Model::load(&chemin, 512, 16, true, 1.0, false, 0, 0);
            mdl.emb_imposee = Some(y[..n_emb].to_vec());
            let hn = mdl.forward(0, 0);
            let lg = mdl.logits(&hn);
            let mut best = 0usize;
            for (i, &v) in lg.iter().enumerate() { if v > lg[best] { best = i; } }
            let moy: f32 = lg.iter().sum::<f32>() / lg.len() as f32;
            let var: f32 = lg.iter().map(|v| (v - moy) * (v - moy)).sum::<f32>() / lg.len() as f32;
            println!("  moteur : {} logits · argmax {best} · moyenne {moy:.3} · écart-type {:.3}",
                     lg.len(), var.sqrt());
        }
    }
    let norme: f32 = out.iter().map(|v| v * v).sum::<f32>().sqrt();
    println!("{n_patch} patchs × {cout} canaux écrits dans {sortie} (|sortie| = {norme:.4})");
    println!("premier patch, 4 premiers canaux : {:?}",
             &out[..4.min(out.len())].iter().map(|v| (v * 1e5).round() / 1e5).collect::<Vec<_>>());
    let _ = cotes;
}

/// Liste les tenseurs d'un GGUF : nom, dimensions, type, taille. Utile pour
/// écrire un chemin de lecture (vision) sans deviner les noms.
/// Déquantifie **un bloc** d'un tenseur et l'imprime, une valeur par ligne.
///
/// Sert à confronter notre déquantification à celle de ggml sur un bloc réel.
/// Un test qui réimplémenterait la formule en script ne prouverait rien sur le
/// code du moteur — c'est le code qu'on veut éprouver.
fn run_bloc(spec: &str) {
    let (nom, index) = match spec.rsplit_once(':') {
        Some((n, i)) => (n.to_string(), i.parse::<usize>().unwrap_or(0)),
        None => (spec.to_string(), 0),
    };
    let g = Gguf::open_auto(&modele_chemin()).expect("ouverture du GGUF");
    let t = g.tensor(&nom).unwrap_or_else(|| panic!("tenseur « {nom} » absent"));
    // Rangée = dernière dimension (convention numpy : la plus rapide en
    // dernier). `dims[1]` ne convient que pour un tenseur 2D : sur un tenseur
    // d'experts 3D, c'est `n_out` et la lecture partait au mauvais endroit.
    let n_cols = *t.dims.last().unwrap() as usize;
    let n_lignes = t.nelem() / n_cols.max(1);
    // Le bloc est une fenêtre de 256 POIDS consécutifs dans l'ordre du fichier,
    // pas « 256 valeurs de la même rangée » : Qwen2.5-0.5B a des rangées de 896
    // poids (28 blocs Q5_0 de 32), donc une fenêtre en chevauche deux.
    let debut_poids = index * 256;
    assert!(debut_poids < t.nelem(), "bloc {index} hors du tenseur ({} poids)", t.nelem());
    let mut vals: Vec<f32> = Vec::with_capacity(256);
    let (mut ligne, mut col) = (debut_poids / n_cols, debut_poids % n_cols);
    while vals.len() < 256 && ligne < n_lignes {
        let rangee = g.row_f32(&nom, ligne, n_cols);
        let fin = (col + (256 - vals.len())).min(n_cols);
        vals.extend_from_slice(&rangee[col..fin]);
        ligne += 1;
        col = 0;
    }
    // On déquantifie par `row_f32` — le MÊME chemin que le chargement du modèle.
    // Un outil de vérification qui déquantifie à part peut être juste pendant que
    // le moteur est faux : c'est arrivé avec `q8_dot_at`, dont l'offset fautif
    // vivait dans le chemin de production, pas dans le déquantificateur.
    println!("tenseur {nom} · type {} · bloc {index} (poids {}..{}, {} rangées)",
             Gguf::nom_type(t.ttype), debut_poids, debut_poids + vals.len(), n_lignes);
    for x in &vals { println!("{x:.7}"); }
}

/// Sonde d'accès mmappé à la table d'engram.
///
/// `blk.N.engram_embd.weight` pèse 101,4 Go par couche sur DeepSeek-V4.1 — plus
/// que tous les experts réunis. Ce n'est pourtant **pas un tenseur de poids** :
/// c'est une table de hachage de n-grammes, et un jeton n'en lit que quelques
/// entrées de 264 octets. La charger serait une faute ; il faut l'**adresser**.
///
/// Cette sonde le démontre : elle ouvre le fichier entier en mmap, lit `n`
/// entrées dispersées, et affiche le temps comme la mémoire. Le noyau ne lit que
/// les pages touchées.
/// **La liste d'adresses de l'engram** (P8) : quelles rangées le modèle irait
/// lire pour une séquence de jetons.
///
/// Elle se calcule **sans charger le modèle** — les métadonnées suffisent (48
/// premiers, 8 multiplicateurs, la table de correspondance des jetons) — et
/// c'est tout l'intérêt : on peut la comparer à la référence
/// (`tools/engram_reference.py`) sur un fichier de 365 Go sans lire un poids.
fn run_engram_adresses(sortie: &str, opt: &Options) {
    use std::io::Write;
    let path = modele_chemin();
    let g = Gguf::open_meta_auto(&path).expect("ouverture des métadonnées");
    let Some(e) = engram::Engram::depuis_gguf(&g) else {
        println!("ce modèle n'a pas d'engram (pas d'`engram.layer_ids`)");
        return;
    };
    let n_hash_cols = e.n_hash_cols();
    println!("engram : {} couches {:?} · {} rangées · {n_hash_cols} colonnes de hachage \
              ({} reculs × {} têtes) · vocabulaire compressé {}",
             e.couches.len(), e.couches, e.rangees.iter().sum::<i64>(),
             e.max_ngram - 1, e.n_heads, e.compressed_vocab);
    let ids: Vec<u32> = if opt.ids.is_empty() {
        // Séquence d'essai DÉTERMINISTE, dans les bornes de la table de
        // correspondance : ce qui compte ici est la forme du flux, pas le texte.
        (0..10_000u32).map(|i| (i * 7919) % 129_000).collect()
    } else { opt.ids.clone() };
    let positions: Vec<usize> = (0..ids.len()).collect();
    let morts = vec![false; ids.len()];
    let t0 = std::time::Instant::now();
    let a = e.adresses(&ids, &positions, &morts);
    let duree = t0.elapsed();
    let mut f = std::io::BufWriter::new(std::fs::File::create(sortie)
        .unwrap_or_else(|e| panic!("création de {sortie} : {e}")));
    for v in &a { f.write_all(&v.to_le_bytes()).unwrap(); }
    f.flush().unwrap();
    // Ce que la liste COÛTE et ce qu'elle dit : c'est la porte Drave de la phase.
    let total = a.len();
    let distinctes = {
        let mut v = a.clone(); v.sort_unstable(); v.dedup(); v.len()
    };
    let mut recouvrement = 0usize;
    for jeton in 1..ids.len() {
        for layer in 0..e.couches.len() {
            for col in 0..n_hash_cols {
                let i = (jeton * e.couches.len() + layer) * n_hash_cols + col;
                let j = ((jeton - 1) * e.couches.len() + layer) * n_hash_cols + col;
                if a[i] == a[j] { recouvrement += 1; }
            }
        }
    }
    println!("{} jetons × {} couches × {n_hash_cols} colonnes = {total} adresses en {:?}",
             ids.len(), e.couches.len(), duree);
    println!("rangées DISTINCTES : {distinctes} ({:.1} % du total) — {:.2} % des {} rangées \
              de la table sont adressées",
             100.0 * distinctes as f64 / total as f64,
             100.0 * distinctes as f64 / e.rangees.iter().sum::<i64>() as f64,
             e.rangees.iter().sum::<i64>());
    println!("recouvrement entre jetons consécutifs : {recouvrement} adresses identiques \
              ({:.1} %)", 100.0 * recouvrement as f64 / total as f64);
    println!("adresses écrites dans {sortie} (i32, {} octets)", total * 4);
    // ---- les rangées ADRESSÉES : on les lit et on en écrit les valeurs.
    // C'est la chaîne complète de l'adressage — la liste dit quoi lire, la
    // lecture dit ce qu'on y trouve — et elle se vérifie contre la référence
    // sans charger un poids du reste du modèle.
    // `open` (mmap) et non `open_meta_auto` : lire une rangée demande les
    // DONNÉES, pas seulement les métadonnées — l'ouverture « méta » ne mappe pas
    // les tenseurs, et `octets_tenseur` y rend `None` (constaté : 0 rangée lue
    // sur 2000). Le mmap ne lit rien tant qu'on ne touche pas aux pages.
    let g2 = Gguf::open(&path).expect("ouverture du GGUF en mmap");
    let n_lire = total.min(2000);
    let mut valeurs: Vec<f32> = Vec::with_capacity(n_lire * engram::VALEURS_PAR_RANGEE);
    let mut lues = 0usize;
    let mut somme = 0f64;
    for k in 0..n_lire {
        let jeton = k / (e.couches.len() * n_hash_cols);
        let couche = e.couches[(k / n_hash_cols) % e.couches.len()];
        let rangee = a[k] as i64;
        if let Some(v) = engram::lire_rangee(&g2, couche, rangee) {
            for x in &v { somme += *x as f64; }
            valeurs.extend_from_slice(&v);
            lues += 1;
        }
    }
    let chemin_valeurs = format!("{sortie}.valeurs");
    {
        use std::io::Write;
        let mut f = std::io::BufWriter::new(std::fs::File::create(&chemin_valeurs).unwrap());
        for v in &valeurs { f.write_all(&v.to_le_bytes()).unwrap(); }
        f.flush().unwrap();
    }
    let mini = valeurs.iter().cloned().fold(f32::INFINITY, f32::min);
    let maxi = valeurs.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
    let rms = (valeurs.iter().map(|x| (*x as f64) * (*x as f64)).sum::<f64>()
               / valeurs.len().max(1) as f64).sqrt();
    println!("rangées LUES : {lues} sur {n_lire} adresses (couches {:?}) · {:?} valeurs · \
              min {mini:.6} · max {maxi:.6} · RMS {rms:.6} · somme {somme:.6}",
             e.couches, valeurs.len());
    println!("valeurs écrites dans {chemin_valeurs} (f32)");
}

fn run_sonder_engram(n: usize) {
    let path = modele_chemin();
    let t0 = Instant::now();
    let g = Gguf::open(&path).expect("ouverture du GGUF en mmap");
    println!("mmap du fichier en {:?} ({} fichiers, {:.1} Go adressés)",
             t0.elapsed(), g.nb_fichiers(), g.octets_charges() as f64 / 1e9);
    // Les tables d'engram, par couche.
    let tables: Vec<(String, usize)> = g.tensors.iter()
        .filter(|t| t.name.contains("engram_embd"))
        .map(|t| (t.name.clone(), t.nelem()))
        .collect();
    if tables.is_empty() {
        println!("aucun tenseur engram_embd dans ce modèle");
        return;
    }
    for (nom, nelem) in &tables {
        let t = g.tensor(nom).unwrap();
        let lignes = t.dims[0];
        let largeur = if t.dims.len() > 1 { t.dims[1] } else { 1 };
        println!("  {nom} : {lignes} entrées × {largeur} octets = {:.1} Go",
                 *nelem as f64 / 1e9);
        // Lectures dispersées, déterministes : ce sont les entrées qu'un texte
        // irait chercher, une par n-gramme.
        let octets_ligne = largeur as usize;
        // Lectures **en parallèle** : sur un NVMe, le débit passe de 5,4 Go/s à un
        // lecteur à 31 Go/s à seize (mesuré). Une table à accès aléatoire est
        // exactement le cas où le parallélisme paie — à condition que le support
        // en soit capable, ce qu'un disque mécanique n'est pas.
        let threads = std::thread::available_parallelism().map(|p| p.get()).unwrap_or(8).min(16);
        // `*const u8` n'est pas `Send` : on transporte l'adresse en `usize`.
        let ptr = g.data_ptr(nom).map(|p| p as usize);
        let t1 = Instant::now();
        let mut sommes = vec![0u64; threads];
        std::thread::scope(|sc| {
            for (ti, somme) in sommes.iter_mut().enumerate() {
                let ptr = ptr;
                sc.spawn(move || {
                    let Some(base) = ptr.map(|a| a as *const u8) else { return };
                    let mut etat = 12345u64.wrapping_add(ti as u64 * 7919);
                    let part = n / threads + usize::from(ti < n % threads);
                    for _ in 0..part {
                        etat = etat.wrapping_mul(6364136223846793005)
                                   .wrapping_add(1442695040888963407);
                        let idx = (etat >> 16) % lignes;
                        // Une lecture par entrée : c'est le geste réel d'un accès
                        // par n-gramme, et c'est la latence qu'on veut connaître.
                        let p = unsafe { base.add(idx as usize * octets_ligne) };
                        let tranche = unsafe { std::slice::from_raw_parts(p, octets_ligne) };
                        *somme = somme.wrapping_add(tranche[octets_ligne - 1] as u64);
                    }
                });
            }
        });
        let d = t1.elapsed();
        let somme: u64 = sommes.iter().fold(0u64, |a, b| a.wrapping_add(*b));
        println!("    {n} entrées lues en {d:?} à {threads} lecteurs \
({:.2} ms par entrée, {:.1} Mo touchés)",
                 d.as_secs_f64() * 1e3 / n as f64,
                 (n * octets_ligne) as f64 / 1e6);
        println!("    débit : {:.0} entrées/s · {:.1} Mo/s utiles",
                 n as f64 / d.as_secs_f64(),
                 (n * octets_ligne) as f64 / 1e6 / d.as_secs_f64());
        println!("    somme de contrôle : {somme}");
    }
    // La mémoire résidente, lue dans /proc : c'est elle qui prouve qu'on n'a
    // rien chargé.
    if let Ok(s) = std::fs::read_to_string("/proc/self/status") {
        for l in s.lines() {
            if l.starts_with("VmRSS") || l.starts_with("VmSize") {
                println!("  {l}");
            }
        }
    }
}

/// Détection du matériel et plan de configuration, **sans charger de modèle**.
///
/// Chaque ligne du plan porte le chiffre qui la justifie : un réglage
/// surprenant doit pouvoir être contesté, pas subi.
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
/// Ouvre un GGUF **en-tête seul**, en tolérant un modèle **en cours de
/// téléchargement** : l'inventaire est alors partiel, et c'est DIT — sur la
/// sortie d'erreur, avant tout le reste. Sans ce chemin, il fallait attendre la
/// fin d'un transfert de plusieurs heures pour seulement savoir ce que le
/// fichier contient (métadonnées, vocabulaire, architecture, manques).
fn ouvrir_meta_tolerant(chemin: &str, qui: &str) -> Gguf {
    match Gguf::shards_presents(std::path::Path::new(chemin)) {
        Some((p, t)) if p < t => {
            eprintln!("⚠️  {qui} : modèle INCOMPLET ({p} shards sur {t}) — lecture de \
l'en-tête du premier shard présent ; tout « manque » peut n'être qu'un shard non téléchargé.");
            Gguf::open_meta(chemin).expect("ouverture de l'en-tête du premier shard présent")
        }
        _ => Gguf::open_meta_auto(chemin).expect("ouverture du GGUF (en-tête)"),
    }
}

/// Test de fumée de la couche 0 de Kimi-K3 (voir `--k3-essai`).
fn run_k3_essai(plage: Option<(usize, usize)>) {
    let chemin = modele_chemin();
    let chemin = std::path::Path::new(&chemin);
    // Les shards PRÉSENTS, dans l'ordre — un transfert en cours en laisse
    // quelques-uns, et la couche 0 est dans les premiers.
    let dossier = chemin.parent().unwrap_or_else(|| std::path::Path::new("."));
    let nom = chemin.file_name().and_then(|n| n.to_str()).unwrap_or("");
    let tete = nom.rsplit_once("-of-").map(|(t, _)| t.rsplit_once('-').map(|(p, _)| p.to_string()));
    let mut shards: Vec<std::path::PathBuf> = Vec::new();
    if let Some(Some(pref)) = tete {
        if let Ok(rd) = std::fs::read_dir(dossier) {
            for e in rd.flatten() {
                let n = e.file_name().to_string_lossy().to_string();
                if n.starts_with(pref.as_str()) && n.ends_with(".gguf") { shards.push(e.path()); }
            }
        }
        shards.sort();
    }
    if shards.is_empty() { eprintln!("aucun shard trouvé"); return; }
    eprintln!("[k3-essai] {} shard(s) présents", shards.len());
    // Un shard EN COURS d'écriture a un en-tête incomplet : on l'écarte en le
    // disant, plutôt que de tomber (même tolérance que `--config`).
    let mut lisibles: Vec<std::path::PathBuf> = Vec::new();
    for p in &shards {
        match Gguf::open_meta(p) {
            Ok(_) => lisibles.push(p.clone()),
            Err(_) => eprintln!("[k3-essai] {} : en-tête incomplet (shard en cours), écarté",
                                p.file_name().unwrap_or_default().to_string_lossy()),
        }
    }
    if lisibles.is_empty() { eprintln!("[k3-essai] aucun shard lisible"); return; }
    let g = Gguf::open_multi(&lisibles).expect("ouverture des shards lisibles");
    let mut c0 = match kimi_k3::Couche0::charge(&g) {
        Ok(c) => c,
        Err(e) => { eprintln!("[k3-essai] chargement impossible : {e}"); return; }
    };
    // Contrôle des dimensions sur quatre couches types AVANT tout calcul :
    // 0 (dense), 1 (MoE+KDA), 3 (MoE+MLA), 4 (KDA). C'est ce qui attrape une
    // dimension lue du mauvais côté, qui ne se voit ni à la compilation ni à la
    // relecture.
    for l in [0usize, 1, 3, 4] {
        let e = kimi_k3::verifie_dims(&g, l);
        if e.is_empty() {
            println!("  couche {l} : dimensions conformes");
        } else {
            println!("  couche {l} : {} écart(s)", e.len());
            for x in e.iter().take(6) { println!("      {x}"); }
        }
    }
    // Le MoE latent d'une couche (1) : chargement + un jeton, pour vérifier la
    // chaîne complète (routeur → 16 experts déquantifiés un par un → norme
    // latente → remontée → partagés).
    match kimi_k3::MoeK3::charge(&g, 1) {
        Ok(moe) => {
            let embd = g.dequant("token_embd.weight");
            let h = c0.hauteur();
            let t = 3638usize;
            let x = &embd[t * h..(t + 1) * h];
            let t0 = std::time::Instant::now();
            match moe.avant(x) {
                Ok(y) => {
                    let n: f32 = y.iter().map(|v| v * v).sum::<f32>().sqrt();
                    let finis = y.iter().all(|v| v.is_finite());
                    println!("  MoE couche 1 : |sortie| = {n:.4} · finis : {finis} · {} ms",
                             t0.elapsed().as_millis());
                }
                Err(e) => println!("  MoE couche 1 : {e}"),
            }
        }
        Err(e) => println!("  MoE couche 1 : chargement impossible ({e})"),
    }
    // La couche MLA (3) : trois jetons à la suite, cache compris.
    match kimi_k3::MlaK3::charge(&g, 3) {
        Ok(mut mla) => {
            let embd = g.dequant("token_embd.weight");
            let h = c0.hauteur();
            for (i, t) in [3638usize, 275, 1309].iter().enumerate() {
                let x = &embd[t * h..(t + 1) * h];
                // l'entrée normalisée que lit la porte de sortie
                let mut xn = vec![0f32; h];
                let mut carre = 0f64;
                for v in x { carre += (*v as f64) * (*v as f64); }
                let inv = 1.0 / ((carre / h as f64 + 1e-5).sqrt() as f32);
                for j in 0..h { xn[j] = x[j] * inv; }
                let t0 = std::time::Instant::now();
                match mla.avant(x, &xn, i) {
                    Ok(y) => {
                        let n: f32 = y.iter().map(|v| v * v).sum::<f32>().sqrt();
                        let finis = y.iter().all(|v| v.is_finite());
                        println!("  MLA couche 3, jeton {i} : |sortie| = {n:.4} · finis : {finis} · {} ms",
                                 t0.elapsed().as_millis());
                    }
                    Err(e) => { println!("  MLA couche 3 : {e}"); break; }
                }
            }
        }
        Err(e) => println!("  MLA couche 3 : chargement impossible ({e})"),
    }
    // **La composition** : quatre couches enchaînées (0 dense, 1 MoE, 2 MoE,
    // 3 MLA), avec l'attention résiduelle et la banque. C'est ce qui vérifie la
    // CHAÎNE — les pièces étaient déjà vérifiées séparément.
    // Combien de couches composer. Quatre exercent la chaîne (dense, deux MoE,
    // MLA) mais **ne franchissent aucune banque** : la première est la couche 0,
    // la suivante la 12. `DRAVE_K3_COUCHES=13` est donc le premier essai qui
    // teste le REDÉMARRAGE du flux résiduel et un `res_mix` à deux points de
    // contrôle — deux mécanismes que quatre couches ne touchent pas.
    let n_k3: usize = std::env::var("DRAVE_K3_COUCHES").ok()
        .and_then(|v| v.parse::<usize>().ok()).filter(|n| *n >= 1).unwrap_or(4);
    println!("  composition : {n_k3} couche(s) — banques aux couches {}",
             (0..n_k3).step_by(12).map(|l| l.to_string())
                 .collect::<Vec<_>>().join(", "));
    match kimi_k3::PetitesK3::charge(&g, n_k3) {
        Ok(mut petites) => {
            let embd = g.dequant("token_embd.weight");
            let h = petites.h;
            let t0 = std::time::Instant::now();
            let mut ok = true;
            for (i, t) in [3638usize, 275, 1309, 3140].iter().enumerate() {
                let x = &embd[t * h..(t + 1) * h];
                match petites.avant(x, i) {
                    Ok(y) => {
                        let n: f32 = y.iter().map(|v| v * v).sum::<f32>().sqrt();
                        let finis = y.iter().all(|v| v.is_finite());
                        println!("  composition 0-{}, jeton {i} : |l_out| = {n:.4} · finis : {finis}",
                                 n_k3 - 1);
                        if !finis { ok = false; }
                        if let Ok(prefixe) = std::env::var("DRAVE_DUMP_COUCHES") {
                            if !prefixe.is_empty() {
                                use std::io::Write;
                                if let Ok(mut f) = std::fs::File::create(
                                        format!("{prefixe}-l_out-{}-{i}.bin", n_k3 - 1)) {
                                    let mut o = Vec::with_capacity(y.len() * 4);
                                    for v in &y { o.extend_from_slice(&v.to_le_bytes()); }
                                    let _ = f.write_all(&o);
                                }
                            }
                        }
                    }
                    Err(e) => { println!("  composition 0-3 : {e}"); ok = false; break; }
                }
            }
            if ok { println!("  composition : {} ms au total", t0.elapsed().as_millis()); }
        }
        Err(e) => println!("  composition 0-3 : chargement impossible ({e})"),
    }
    // **LA PASSE COMPLÈTE, UNE COUCHE À LA FOIS.** `DRAVE_K3_PASSE=N` calcule
    // les N premières couches en ne gardant QU'UNE couche en mémoire : c'est ce
    // qui rend les 93 couches possibles (une couche ≈ 2,2 Go au lieu de ~220 Go
    // pour toutes). Quand il est posé, on saute la composition `PetitesK3`, qui
    // garde tout — elle sert à vérifier l'enchaînement, pas à aller loin.
    if let Ok(v) = std::env::var("DRAVE_K3_PASSE") {
        if let Ok(n) = v.parse::<usize>() {
            if n >= 1 {
                // `DRAVE_K3_IDS=1,2,3` : la séquence à faire passer. Sert à
                // tracer le routage sur un VRAI texte plutôt que sur quatre
                // jetons de démonstration — une trace de quatre jetons ne dit
                // rien d'un cache.
                let ids4: Vec<u32> = match std::env::var("DRAVE_K3_IDS").ok() {
                    Some(v) => v.split(',').filter_map(|x| x.trim().parse().ok()).collect(),
                    None => vec![3638u32, 275, 1309, 3140],
                };
                if ids4.is_empty() { eprintln!("[k3] DRAVE_K3_IDS vide"); return; }
                // `DRAVE_K3_TETE=1` : on rend les LOGITS au lieu de `l_out`.
                // C'est le critère de la porte de correction du dépôt
                // (corrélation par position, top-1), appliqué au plus gros
                // modèle du parc — un état caché ne se compare qu'à un état
                // caché, des logits se comparent à ceux de llama.cpp.
                let tete = std::env::var("DRAVE_K3_TETE")
                    .map(|v| v != "0" && !v.is_empty()).unwrap_or(false);
                println!("  passe complète : {n} couche(s), une seule en mémoire à la fois{}",
                         if tete { " · TÊTE (logits)" } else { "" });
                let t0 = std::time::Instant::now();
                // `DRAVE_K3_GEN=N` : PREFILL puis N jetons engendrés en
                // glouton, l'état récurrent persistant d'un jeton au suivant.
                // C'est « faire tourner le modèle » au sens plein, et la
                // référence donne déjà de quoi vérifier : ses logits sur la
                // séquence [3638, 275, 1309, 3140] disent que la position 1 doit
                // choisir 1309 et la position 2, 3140.
                let gen = std::env::var("DRAVE_K3_GEN").ok()
                    .and_then(|v| v.parse::<usize>().ok()).unwrap_or(0);
                if gen > 0 {
                    let mut etats: Vec<kimi_k3::EtatCouche> = Vec::new();
                    let mut suite: Vec<u32> = vec![3638, 275];
                    for pas in 0..=gen {
                        let t0 = std::time::Instant::now();
                        let lgs = match kimi_k3::passe_complete(
                                &g, &suite, n, pas == 0, true,
                                suite.len() - 1,
                                Some(&mut etats)) {
                            Ok(v) => v,
                            Err(e) => { println!("  génération : {e}"); return; }
                        };
                        let dernier = lgs.last().unwrap();
                        let (mut imax, mut vmax) = (0usize, f32::NEG_INFINITY);
                        for (i, &v) in dernier.iter().enumerate() {
                            if v > vmax { vmax = v; imax = i; }
                        }
                        // L'attendu est le top-1 de la RÉFÉRENCE à la même
                        // position, pas le jeton cible : llama.cpp choisit 1103
                        // après [3638, 275], et 3140 après [3638, 275, 1309].
                        // Confondre les deux m'a fait imprimer un ❌ sur un pas
                        // qui était juste — le tableau d'attente était faux, pas
                        // le moteur.
                        let attendu = [1103u32, 3140, 0][pas.min(2)];
                        println!("  pas {pas} : {} jeton(s) en entrée ({} s) → argmax {imax}{}",
                                 suite.len(), t0.elapsed().as_secs(),
                                 if attendu != 0 {
                                     if imax as u32 == attendu { " ✅ (référence)".to_string() }
                                     else { format!(" ❌ (référence : {attendu})") }
                                 } else { String::new() });
                        if pas == gen { break; }
                        // `DRAVE_K3_IMPOSE=1309,3140` force la suite du texte
                        // au lieu de laisser le moteur choisir : c'est ce qui
                        // permet de vérifier un pas d'APRÈS que la référence ait
                        // publié ses logits, et de tester la PERSISTANCE de
                        // l'état entre deux appels (le 2e appel ne voit qu'un
                        // jeton nouveau, l'état vient du 1er).
                        let impose: Vec<u32> = std::env::var("DRAVE_K3_IMPOSE").ok()
                            .map(|v| v.split(',').filter_map(|x| x.trim().parse().ok()).collect())
                            .unwrap_or_default();
                        suite.push(impose.get(pas).copied().unwrap_or(imax as u32));
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
                println!("  plage : couches {debut}..{} · relais d'entrée : {}", fin - 1,
                         if entree.is_some() { "oui" } else { "non (départ de la plongée)" });
                match kimi_k3::passe_plage(&g, &ids4, debut, fin, true, tete, 0, None,
                                           entree.as_ref()) {
                    Ok((flux, relais)) => {
                        if let Ok(c) = std::env::var("DRAVE_K3_RELAIS_SORTIE") {
                            if !c.is_empty() {
                                match relais.ecrire(&c) {
                                    Ok(()) => println!("  relais : {c} — reprend à la couche \
{} · {} jetons × {} canaux · {} banque(s)", relais.debut, relais.flux.len(),
                                        relais.flux.first().map(|v| v.len()).unwrap_or(0),
                                        relais.pile.len()),
                                    Err(e) => println!("  relais NON écrit ({c}) : {e}"),
                                }
                            }
                        }
                        if tete {
                            // Les logits vont dans un fichier binaire au format de
                            // `--logits-bin` : int32 vocab, int32 n_pos, puis
                            // n_pos × vocab f32.
                            let vocab = flux.first().map(|v| v.len()).unwrap_or(0);
                            let chemin = std::env::var("DRAVE_K3_LOGITS")
                                .unwrap_or_else(|_| "/tmp/k3_logits.bin".to_string());
                            use std::io::Write;
                            if let Ok(mut f) = std::fs::File::create(&chemin) {
                                let npos = (flux.len().saturating_sub(1)) as i32;
                                let _ = f.write_all(&(vocab as i32).to_le_bytes());
                                let _ = f.write_all(&npos.to_le_bytes());
                                // position p prédit le jeton p+1, comme `--logits-bin`
                                for p in 0..npos as usize {
                                    let mut o = Vec::with_capacity(vocab * 4);
                                    for v in &flux[p] { o.extend_from_slice(&v.to_le_bytes()); }
                                    let _ = f.write_all(&o);
                                }
                                println!("  logits : {chemin} — {npos} positions × {vocab} valeurs");
                            }
                        } else {
                        for (i, y) in flux.iter().enumerate() {
                            let nor: f32 = y.iter().map(|v| v * v).sum::<f32>().sqrt();
                            let finis = y.iter().all(|v| v.is_finite());
                            println!("  passe {debut}-{}, jeton {i} : |l_out| = {nor:.4} · finis : {finis}",
                                     fin - 1);
                            if let Ok(prefixe) = std::env::var("DRAVE_DUMP_COUCHES") {
                                if !prefixe.is_empty() {
                                    use std::io::Write;
                                    if let Ok(mut f) = std::fs::File::create(
                                            format!("{prefixe}-l_out-{}-{i}.bin", fin - 1)) {
                                        let mut o = Vec::with_capacity(y.len() * 4);
                                        for v in y { o.extend_from_slice(&v.to_le_bytes()); }
                                        let _ = f.write_all(&o);
                                    }
                                }
                            }
                        }
                        }
                        println!("  passe complète : {} ms au total", t0.elapsed().as_millis());
                    }
                    Err(e) => println!("  passe {debut}..{fin} : {e}"),
                }
                return;
            }
        }
    }
    // L'entrée de la couche 0 est l'embarquement du jeton.
    let ids = vec![3638u32, 275, 1309];      // « Le ciel est… » (tokenizer du modèle)
    let embd = g.dequant("token_embd.weight");
    let h = c0.hauteur();
    // `DRAVE_K3_SANS_ETAT=1` remet l'état (convolution + delta) à zéro AVANT
    // chaque jeton. C'est un essai de DISCRIMINATION, pas un mode : si les
    // positions 1 et 2 se rapprochent de la référence avec un état neuf, c'est
    // que la référence traite ces jetons indépendamment ; si rien ne bouge, le
    // défaut est ailleurs. Le drapeau change la sortie, donc il le DIT.
    let sans_etat = std::env::var("DRAVE_K3_SANS_ETAT")
        .map(|v| v != "0" && !v.is_empty()).unwrap_or(false);
    if sans_etat {
        eprintln!("[k3-essai] DRAVE_K3_SANS_ETAT : état remis à zéro avant CHAQUE jeton \
(essai de discrimination — la sortie change)");
    }
    for (i, &t) in ids.iter().enumerate() {
        let d = t as usize * h;
        let x = &embd[d..d + h];
        if sans_etat { c0.remise_a_zero(); }
        match c0.avant(x) {
            Ok(y) => {
                let n: f32 = y.iter().map(|v| v * v).sum::<f32>().sqrt();
                let finis = y.iter().all(|v| v.is_finite());
                println!("  jeton {i} (id {t}) : |l_out| = {n:.4} · finis : {finis} · \
premiers : {:.5} {:.5} {:.5}", y[0], y[1], y[2]);
                // Vidage au format du moteur (`<préfixe>-<nom>-<couche>-<position>.bin`),
                // pour que `tools/compare_etats.py` puisse comparer à `l_out-0` de
                // la référence dès qu'elle tournera sur le modèle complet.
                if let Ok(prefixe) = std::env::var("DRAVE_DUMP_COUCHES") {
                    if !prefixe.is_empty() {
                        use std::io::Write;
                        let chemin = format!("{prefixe}-l_out-0-{i}.bin");
                        if let Ok(mut f) = std::fs::File::create(&chemin) {
                            let mut o = Vec::with_capacity(y.len() * 4);
                            for v in &y { o.extend_from_slice(&v.to_le_bytes()); }
                            let _ = f.write_all(&o);
                            println!("      vidé : {chemin}");
                        }
                    }
                }
            }
            Err(e) => { eprintln!("[k3-essai] jeton {i} : {e}"); return; }
        }
    }
}

fn run_config() {
    // Un modèle **en cours de téléchargement** doit pouvoir être interrogé : sans
    // ce chemin, l'ouverture refusait le fichier (« 32 shards annoncés, 5
    // présents ») et il fallait attendre la fin du transfert pour savoir ce que
    // le modèle contient. L'inventaire est alors PARTIEL — et il le dit, en
    // haut, avant tout le reste.
    let chemin = modele_chemin();
    let g = ouvrir_meta_tolerant(&chemin, "--config");
    let arch = g.meta.get("general.architecture").and_then(|m| m.as_str()).unwrap_or("?");
    println!("modèle        : {}", modele_chemin());
    println!("architecture  : {arch}");
    let n_layer = model::dim_gguf(&g, &["block_count", "num_hidden_layers"], "num_hidden_layers")
                      .unwrap_or(0);
    let hidden = model::dim_gguf(&g, &["embedding_length", "hidden_size"], "hidden_size")
                     .unwrap_or(0);
    println!("couches       : {n_layer} · cachés {hidden}");
    if arch == "kimi-k3" {
        // L'inventaire des tenseurs, vérifié contre le fichier : c'est ce qui
        // empêche un tenseur attendu d'être chargé VIDE (défaut silencieux).
        match kimi_k3::inventorie(std::path::Path::new(&chemin)) {
            Ok(inv) => println!("{}", inv.rapport()),
            Err(e) => println!("inventaire    : illisible ({e})"),
        }
    }
    let r = model::routage_du_gguf(&g);
    println!("experts       : {} par couche, {} par jeton · FFN expert {}",
             r.n_expert, r.n_expert_used, r.ffn_exp);
    if r.n_expert > 0 {
        println!("routage       : {} (source : {}) · renormalisation {} · échelle {}",
                 r.gating.nom(), r.source,
                 if r.norm { "oui" } else { "non" },
                 if r.echelle == 0.0 { "aucune".to_string() } else { format!("{:.3}", r.echelle) });
        if r.hash_layers > 0 {
            println!("routage table : {}/{} premières couches par `ffn_gate_tid2eid`",
                     r.hash_layers, n_layer);
        }
    }
    // Régimes d'attention compressée : les MONTRER, parce que c'est ce qu'on
    // avait cessé de lire — la clé est `attention.compress_ratios`, et la
    // chercher sous `compress_ratios` faisait dire « calculable » à V4-Flash
    // (41 couches compressées sur 44).
    if let Some(m) = g.cfg_ou(&["attention.compress_ratios", "compress_ratios"]) {
        let ratios: Vec<i64> = m.as_liste_i64().unwrap_or_default();
        if !ratios.is_empty() {
            let n = |v: i64| ratios.iter().filter(|x| **x == v).count();
            let brutes: Vec<usize> = ratios.iter().enumerate()
                .filter(|(_, v)| **v == 0).map(|(i, _)| i).collect();
            println!("attn compress.: {} couches · {} CSA (ratio 4) · {} HCA (ratio 128) · \
                     brutes aux couches {:?}",
                     ratios.len(), n(4), n(128), brutes);
        }
    }
    // Hyper-connexions : les montrer même quand le modèle n'est pas encore
    // calculable — c'est un chiffre du modèle, pas une promesse du moteur.
    if g.tensor("blk.0.hc_attn_fn.weight").is_some() {
        match g.hc_params() {
            Some((mult, iters, eps)) => println!(
                "hyper-conn.   : {mult} copies · {} mélanges par couche (pre/post/comb) · \
                 Sinkhorn {iters} itérations · eps {eps:e}",
                2 * mult + mult * mult),
            None => println!("hyper-conn.   : présentes, mais `hc_mult` introuvable"),
        }
    }
    // Ce que le moteur ne sait pas calculer, dit avant la panne — par la MÊME
    // fonction que le refus à l'ouverture : deux listes divergentes ont déjà
    // annoncé deux manques là où la passe avant en refusait trois.
    let c = model::Cfg {
        n_layer: n_layer as usize, hidden: hidden as usize, n_head: 0, n_kv_head: 0,
        head_dim: 0, ffn: 0, eps: 1e-6, rope_base: 10000.0, vocab: 0,
        n_expert: r.n_expert, n_expert_used: r.n_expert_used, ffn_exp: r.ffn_exp,
        ffn_act_oss: false, gating: r.gating, expert_norm: r.norm, expert_scale: r.echelle,
        hash_layers: r.hash_layers, n_rot: 0, yarn: None,
        yarn_declare: None,
    };
    let manques = model::manques_architecture(&g, &c, 0, false);
    if manques.is_empty() {
        println!("calculable    : oui (passe avant implémentée)");
    } else {
        println!("calculable    : NON — il manque : {}", manques.join(", "));
    }
}

fn run_materiel(opt: &Options) {
    let m = materiel::Materiel::detecter();
    print!("{}", m.resume());
    let ctx = opt.ctx;
    // Si un modèle est donné, le plan s'appuie sur SES dimensions au lieu de
    // celles de V4.1 par défaut : un plan générique n'aide personne.
    let (taille_go, n_experts, mo_expert, arch) = match Gguf::open_meta_auto(&modele_chemin()) {
        Ok(g) => {
            let arch = g.meta.get("general.architecture").and_then(|v| v.as_str())
                          .unwrap_or("?").to_string();
            // Le nombre d'experts est DÉCLARÉ par la plupart des modèles, mais
            // pas par DeepSeek-V4.1 (il n'est que dans sa config imbriquée). On
            // le déduit alors de la première dimension du tenseur d'experts —
            // c'est la source qui ne peut pas mentir.
            let n_exp = g.cfg("expert_count").and_then(|v| v.as_u64()).unwrap_or(0) as usize;
            let n_exp = if n_exp > 0 { n_exp } else {
                ["blk.0.ffn_gate_exps.weight", "cl0/blk.0.ffn_gate_exps.weight"].iter()
                    .find_map(|n| g.tensor(n)).map(|t| t.dims[0] as usize).unwrap_or(0)
            };
            // Un expert : gate + up (n_ff × n_embd) + down (n_embd × n_ff).
            let ffn = g.cfg("expert_feed_forward_length").and_then(|v| v.as_u64()).unwrap_or(0);
            let embd = g.cfg("embedding_length").and_then(|v| v.as_u64()).unwrap_or(0);
            let couches = g.cfg("block_count").and_then(|v| v.as_u64()).unwrap_or(0);
            // Taille d'un expert : on la LIT sur les tenseurs réels plutôt que de
            // la supposer. Un expert vaut gate + up (n_ff × n_embd) + down
            // (n_embd × n_ff), chacun à son propre type de quantification.
            // Un modèle en clusters préfixe ses tenseurs (`cl0/blk.0.…`) : on
            // cherche les deux formes, sinon la taille tombe à zéro en silence.
            let trouve = |base: &str| {
                g.tensor(base).or_else(|| g.tensor(&format!("cl0/{base}")))
            };
            let mo = ["ffn_gate_exps.weight", "ffn_up_exps.weight", "ffn_down_exps.weight"]
                .iter()
                .filter_map(|s| trouve(&format!("blk.0.{s}")))
                // On divise par le nombre d'experts RÉELS du tenseur : dans un
                // fichier de cluster il n'y en a qu'une fraction (16 sur 128),
                // et diviser par le total donnait 0,38 Mo au lieu de 3,05.
                .map(|t| Gguf::octets_tensor(t) as f64 / (t.dims[0].max(1)) as f64)
                .sum::<f64>() / 1e6;
            if mo <= 0.0 {
                eprintln!("[materiel] taille d'expert introuvable (couche 0) : le plan \
utilisera 9,95 Mo par expert, valeur de DeepSeek-V4.1");
            }
            let mo = if mo > 0.0 { mo } else { 9.95 };
            let _ = (ffn, embd);
            let total = g.octets_poids() as f64 / 1e9;
            let _ = couches;
            if n_exp > 0 {
                println!("Modèle : {} · {:.1} Go · {} experts de {:.2} Mo\n",
                         arch, total, n_exp, mo);
            } else {
                println!("Modèle : {} · {:.1} Go · dense (aucun expert)\n", arch, total);
            }
            (total, n_exp, mo, arch)
        }
        Err(_) => (0.0, 384, 9.95, String::from("DeepSeek-V4.1 (défaut)")),
    };
    let _ = arch;
    let plan = m.plan(ctx, taille_go, n_experts, mo_expert);
    println!();
    println!("Plan pour un contexte de {ctx} jetons, d'après les dimensions du modèle :");
    println!("  threads          : {}", plan.threads);
    if let Some(e) = &plan.epinglage {
        println!("  épinglage        : {} processeurs ({})", e.len(),
                 if e.len() > 8 { format!("{}..{}", e[0], e[e.len()-1]) } else {
                     e.iter().map(|c| c.to_string()).collect::<Vec<_>>().join(",") });
    }
    println!("  lecteurs disque  : {}", plan.lecteurs);
    println!("  cache experts    : {:.1} Go en VRAM", plan.cache_experts_go);
    println!("  cache KV         : {} bits", plan.kv_bits);
    println!();
    for r in &plan.raisons { println!("  · {r}"); }
    println!();
    // Ce que coûtera un jeton, d'après les débits mesurés sur cette machine.
    if n_experts > 0 && mo_expert > 0.0 {
        // Les experts relus par jeton : top-k × couches. On lit le top-k déclaré,
        // à défaut 6.
        let topk = 6.0;
        let couches = 40.0;
        let go = topk * couches * mo_expert / 1000.0;
        // La tête : vocabulaire × dimension × octets par poids (Q4_K ≈ 0,56).
        let tete_go = 1.32;
        println!("  {}", m.cout_par_jeton(&plan, go, tete_go, 8.0));
    }
    println!();
    println!("Ces valeurs sont des DÉFAUTS : tout drapeau explicite les emporte.");
}

fn run_tensors() {
    let path = &modele_chemin();
    // `open_meta_auto` : l'inventaire ne lit que les en-têtes. Avec `open`, un
    // modèle de 366 Go devait tenir en mémoire pour qu'on lise sa liste de
    // tenseurs — c'est-à-dire qu'on ne pouvait PAS l'inventorier.
    let t0 = Instant::now();
    let g = Gguf::open_meta_auto(path).expect("ouverture de l'en-tête GGUF");
    let duree = t0.elapsed();
    let arch = g.meta.get("general.architecture").and_then(|m| m.as_str()).unwrap_or("?");
    println!("{} · {} fichiers · {} tenseurs · {:.2} Go de poids · en-têtes lus en {:?}",
             arch, g.nb_fichiers(), g.tensors.len(),
             g.octets_poids() as f64 / 1e9, duree);
    if g.nb_fichiers() > 1 {
        let mut par_fichier = vec![0usize; g.nb_fichiers()];
        let mut octets = vec![0u64; g.nb_fichiers()];
        for t in &g.tensors {
            par_fichier[t.fichier] += 1;
            octets[t.fichier] += Gguf::octets_tensor(t);
        }
        for (i, (n, o)) in par_fichier.iter().zip(&octets).enumerate() {
            println!("  fichier {i} : {n:5} tenseurs · {:.2} Go", *o as f64 / 1e9);
        }
    }
    // Les métadonnées d'architecture, celles qu'on relit à chaque fois.
    for k in ["block_count", "embedding_length", "feed_forward_length", "attention.head_count",
              "attention.head_count_kv", "expert_count", "expert_used_count",
              "context_length", "vocab_size"] {
        if let Some(v) = g.cfg(k) {
            let s = v.as_u64().map(|x| x.to_string())
                .or_else(|| v.as_f64().map(|x| format!("{x}")))
                .or_else(|| v.as_str().map(str::to_string))
                .unwrap_or_else(|| format!("{v:?}"));
            print!(" · {k} {s}");
        }
    }
    println!();
    for t in &g.tensors {
        let poids: u64 = t.dims.iter().product();
        println!("  {:8} {:38} {:?} · {:.1} M poids · fichier {}",
                 Gguf::nom_type(t.ttype), t.name, t.dims, poids as f64 / 1e6, t.fichier);
    }
}

/// Applique les réglages de quantification de la ligne de commande à un modèle
/// des chemins FLUX. Ils étaient ignorés dans `--flux-serveur` et
/// `--ppl-reparti` : un `--act-thresh 0,05` n'y changeait rien, et le mode
/// « listes » transportait donc une liste PLEINE au lieu d'une liste creuse —
/// le défaut « le drapeau est analysé mais jamais appliqué », déjà vu cinq fois.
/// Niveaux d'activation pour `--abits N`, **bornés à ce que le stockage accepte**.
///
/// Les activations quantifiées circulent en `i16` (les noyaux d'experts prennent
/// `&[i16]`) et les conversions saturent à ±32 767. Au-delà de 16 bits, les
/// valeurs quantifiées dépassent cette borne : elles étaient SILENCIEUSEMENT
/// ramenées à 32 767, ce qui revient à diviser l'activation par 2^(abits−16) —
/// mesuré sur V4.1 : `--abits 16` donne 12 889 de perplexité, `--abits 24` en
/// donne 127 496 (10× pire), sans un mot. On borne donc, et on le DIT.
fn niveaux_activation(abits: u32) -> f32 {
    let abits = abits.clamp(1, 16);
    ((1u32 << (abits - 1)) - 1) as f32
}

/// Applique `--abits` en le bornant, en ANNONÇANT la borne.
fn poser_niveaux(mdl: &mut model::Model, abits: u32, source: &str) {
    if abits > 16 {
        eprintln!("[activation] --abits {abits} demandé ({source}) : borné à 16 (32 767 \
niveaux), la borne du stockage i16 des activations quantifiées. Au-delà, les valeurs \
étaient silencieusement saturées et le calcul faux d'un facteur 2^(abits-16).");
    }
    mdl.act_levels = niveaux_activation(abits);
}

fn appliquer_quantification(mdl: &mut model::Model, opt: &Options) {
    let abits = if opt.abits_impose { opt.abits } else { 8 };
    poser_niveaux(mdl, abits, "modes flux");
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
/// que de laisser lire des octets qui ne veulent pas dire la même chose.
/// Version 4 : le bloc de réglages transporte AUSSI les top-k (par projection,
/// attention, q·k, MoE). En version 3, deux nœuds lancés avec des `--topk-*`
/// différents calculaient deux choses différentes en silence — le même défaut que
/// les niveaux et le seuil, dont le correctif était resté incomplet.
///
/// Version 3 : ajoute le mode LOT. Le passage à 3 n'est pas cosmétique — un pair
/// en version 2 lirait `n × 4` octets d'un corps qui en fait `n × hidden × 4`,
/// se désynchroniserait, puis dirait « mode inconnu » : un refus exact mais tardif
/// et muet sur la cause. Ici il est immédiat et nommé.
const VERSION_FLUX: u8 = 8;
/// Vecteur dense en f32 : 4 octets par canal, toute la dimension.
const MODE_DENSE: u8 = 0;
/// LISTE creuse quantifiée : indice u16 + valeur i16, plus une échelle. C'est le
/// même encodage que la trace sur le disque — la mise en réseau ne réinvente
/// rien, elle réutilise le format de la phase 0.
const MODE_LISTE: u8 = 1;
/// LISTE à **échelle par bloc de 32 canaux** : indice u16, valeur i8, et une
/// échelle f32 par bloc — 3 octets par neurone actif au lieu de 4, avec une
/// erreur relative bornée DANS le bloc (le résidu brut a une dynamique trop
/// large pour une échelle unique).
const MODE_BLOCS: u8 = 2;
/// **LOT** : `n` états de `hidden` canaux chacun, en f32 dense, dans UN SEUL flux.
///
/// C'est le mode du préremplissage réparti : sans lui, un lot de 256 jetons
/// payait 256 allers-retours. Le corps fait `n × hidden × 4` octets ; la
/// dimension n'est pas dans l'en-tête, chaque nœud la connaît par son modèle.
const MODE_LOT: u8 = 3;
/// **LOT EN LISTES** : `n` états, chacun encodé comme le mode 2 (indices par
/// écarts, valeurs i8, une échelle f32 par bloc de 32 canaux), enchaînés dans un
/// seul flux. Le lot dense coûte 3 589 octets par jeton ; celui-ci ≈ 1 530
/// (÷2,3) au prix de la quantification — c'est le mode que le préremplissage
/// réparti utilise quand la bande passante compte plus que le dernier centième
/// de perplexité. Plan : `docs/plan-mode4-lot-listes.md`.
const MODE_LOT_LISTES: u8 = 4;

/// En-tête commun : magie · version · mode · plage · position · n · échelle ·
/// **réglages d'activation** (niveaux, seuil, top-k, renorm).
///
/// Les réglages voyagent parce qu'ils CHANGENT LES CHIFFRES : deux nœuds lancés
/// avec des `--act-thresh` différents ne calculent pas la même chose, et la
/// divergence serait silencieuse. Mesuré : 0,69 d'écart de perplexité avec un
/// seuil 0,05 d'un côté et 0,00 de l'autre, sur le même modèle.
// magie · version · mode · plage · position · n · échelle · niveaux · seuil ·
// top-k · renorm · attn_topk · qk_topk · moe_topk · topk_proj[7]
/// v8 : ce que le PAIR annonce avoir calculé, cumulé sur la session. Un compteur global plutôt
/// qu'un champ de `Flux` : `recevoir_flux` a quatre points de sortie, et ajouter un champ à la
/// structure aurait demandé de tous les toucher — pour une valeur que seul le PILOTE lit.
static PAIRES_DU_PAIR: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);

const TAILLE_TETE: usize = 4 + 1 + 1 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 1
                            + 4 + 4 + 4 + 7 * 4
                            // v7 : attn_window (79), swa_pattern (83), attn_sinks (87)
                            + 4 + 4 + 4
                            // v8 : paires du nœud (91), un u64 — les paires dépassent 2³²
                            + 8;

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
    moe_topk: u32,
    // PROTOCOLE v7 : trois réglages qui ne voyageaient pas, et sans lesquels le pilote et le
    // nœud calculaient DEUX MODÈLES DIFFÉRENTS SOUS LE MÊME NOM (mesuré : 195,5685 contre
    // 50,3829 avec une fenêtre de 64). L'en-tête était plein (79 octets) : ces champs le
    // portent à 91, et la version passe à 7.
    attn_window: u32,
    swa_pattern: u32,
    attn_sinks: u32,
}

impl Act {
    fn du_modele(m: &model::Model) -> Self {
        let mut topk_proj = [0u32; 7];
        for (i, v) in m.act_topk_proj.iter().enumerate() { topk_proj[i] = *v as u32; }
        Act { levels: m.act_levels, thresh: m.act_thresh, topk: m.act_topk as u32,
              renorm: m.act_renorm, topk_proj,
              attn_topk: m.attn_topk as u32, qk_topk: m.qk_topk as u32,
              moe_topk: m.moe_topk as u32,
              attn_window: m.attn_window as u32, swa_pattern: m.swa_pattern as u32,
              attn_sinks: m.attn_sinks as u32 }
    }
    fn appliquer(&self, m: &mut model::Model) {
        m.act_levels = self.levels;
        m.act_thresh = self.thresh;
        m.act_topk = self.topk as usize;
        m.act_renorm = self.renorm;
        for (i, v) in self.topk_proj.iter().enumerate() { m.act_topk_proj[i] = *v as usize; }
        m.attn_topk = self.attn_topk as usize;
        m.qk_topk = self.qk_topk as usize;
        m.moe_topk = self.moe_topk as usize;
        // v7 : ces trois réglages arrivent ENFIN jusqu'au nœud.
        m.attn_window = self.attn_window as usize;
        m.swa_pattern = self.swa_pattern as usize;
        m.attn_sinks = self.attn_sinks as usize;
    }
}

/// Tout ce qu'un flux transporte : sa plage, sa position, son mode, ses
/// réglages d'activation et sa charge utile.
struct Flux {
    /// Nombre du mode : canaux (dense, listes), actifs (blocs) ou ÉTATS (lot).
    n: usize,
    debut: u32,
    fin: u32,
    pos: u32,
    mode: u8,
    act: Act,
    charge: ChargeFlux,
    /// Octets du corps effectivement lus sur le câble (en-tête exclu) : la
    /// comptabilité du banc doit être la taille RÉELLE, pas une formule par mode.
    octets_corps: usize,
    /// **La `pre` portée** par le dernier raccord FFN du nœud émetteur (protocole
    /// v6, V4.1) : `hc` valeurs par jeton, ou vide. C'est le maillon que la chaîne
    /// retardée ne peut pas recalculer chez le destinataire.
    premix: Vec<f32>,
}

/// Plafond d'une allocation pilotée par le RÉSEAU (règle R4 de
/// `docs/plan-prefill-reparti.md`). Sans lui, un pair — hostile ou bogué — qui
/// annonce `n = 4 milliards` fait allouer `n × dimension × 4` octets AVANT tout
/// contrôle : jusqu'à ~15 To demandés au noyau. 256 Mo couvrent largement un lot
/// de 8 192 jetons × 8 192 canaux (268 Mo... soit un lot par fenêtre maximale).
const PLAFOND_FLUX: usize = 256 << 20;

/// Refuse une taille de corps au-delà du plafond, en le DISANT.
fn verifier_taille(octets: usize, quoi: &str) -> std::io::Result<()> {
    if octets > PLAFOND_FLUX {
        return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
            format!("{quoi} : {octets} octets au-delà du plafond de {} Mo — flux refusé                      (règle R4 de docs/plan-prefill-reparti.md)", PLAFOND_FLUX >> 20)));
    }
    Ok(())
}

/// Charge utile d'un flux : dense (f32), ou **liste creuse quantifiée**. Le
/// réseau transporte alors exactement ce que le disque écrit déjà — deux octets
/// d'indice, deux octets de valeur, une échelle par liste.
enum ChargeFlux {
    Dense(Vec<f32>),
    Liste { idx: Vec<u16>, val: Vec<i16>, echelle: f32 },
    Blocs { idx: Vec<u16>, val: Vec<i8>, echelles: Vec<f32> },
    /// Lot d'états, aplati (`t × hidden`).
    Lot(Vec<f32>),
}

impl ChargeFlux {
    /// Rend le vecteur dense : la déquantification a besoin de la dimension, que
    /// seul le modèle connaît.
    fn en_dense(&self, hidden: usize) -> Vec<f32> {
        match self {
            ChargeFlux::Dense(v) => v.clone(),
            // Un lot n'a pas UN vecteur dense : c'est `plat()` qui le sert, et
            // `forward_lot` qui le consomme. L'appeler ici serait une erreur de
            // programme, pas une donnée invalide — on le dit.
            ChargeFlux::Lot(_) => panic!("un lot d'états n'est pas un vecteur dense"),
            ChargeFlux::Liste { idx, val, echelle } => {
                let mut x = vec![0f32; hidden];
                let mut hors = 0usize;
                for (&i, &v) in idx.iter().zip(val.iter()) {
                    // Une trame FORGÉE ne doit pas tuer le nœud : un indice hors
                    // dimension était un `index out of bounds` → SIGABRT (mesuré
                    // par la relecture adversariale, trame LISTE n=1 indice 5000).
                    if (i as usize) < hidden { x[i as usize] = v as f32 * echelle; }
                    else { hors += 1; }
                }
                if hors > 0 {
                    eprintln!("[flux] {hors} indice(s) hors dimension ignorés (flux reçu \
de {hidden} canaux) — pair bogué ou hostile ?");
                }
                x
            }
            ChargeFlux::Blocs { idx, val, echelles } => {
                let mut x = vec![0f32; hidden];
                let mut hors = 0usize;
                for (&i, &v) in idx.iter().zip(val.iter()) {
                    let b = i as usize / 32;
                    if (i as usize) < hidden && b < echelles.len() {
                        x[i as usize] = v as f32 * echelles[b];
                    } else { hors += 1; }
                }
                if hors > 0 {
                    eprintln!("[flux] {hors} indice(s) hors dimension ignorés (flux reçu \
de {hidden} canaux, {} blocs d'échelles)", echelles.len());
                }
                x
            }
        }
    }
    fn actifs(&self) -> usize {
        match self {
            ChargeFlux::Dense(v) => v.len(),
            ChargeFlux::Liste { idx, .. } | ChargeFlux::Blocs { idx, .. } => idx.len(),
            ChargeFlux::Lot(v) => v.len(),
        }
    }
    /// Le lot aplati, pour le nœud qui doit le rendre à `forward_lot`.
    fn plat(&self) -> &[f32] {
        match self { ChargeFlux::Lot(v) => v, _ => &[] }
    }
}

/// Construit l'en-tête d'un flux (79 octets) : magie, version, mode, plage,
/// position, `n`, échelle, et le contrat d'activation.
///
/// **Version 6** : le corps commence par un octet `np` (nombre de `pre` portées)
/// suivi de `np × hc` f32. C'est ce qui permet à la chaîne mHC *retardée* de V4.1
/// de traverser un découpage — 16 octets par jeton sur les 65 615 que coûte déjà
/// un état en `hc` copies, soit 0,02 %. Sans elle, un nœud qui reprend au milieu
/// du modèle replierait son premier raccord avec la copie 0 : faux, et muet.
///
/// **Une seule fonction pour les trois émetteurs**, et c'est délibéré : la
/// duplication de cette construction est exactement ce qui a produit l'en-tête
/// d'un octet trop long (40 écrits pour 39 lus), invisible pendant des flux
/// entiers parce qu'il ne décalait le corps que d'un octet.
fn tete_flux(mode: u8, debut: u32, fin: u32, pos: u32, n: usize, echelle: f32,
             mdl: Option<&model::Model>) -> Vec<u8> {
    let act = mdl.map(Act::du_modele).unwrap_or(Act {
        levels: 127.0, thresh: 0.0, topk: 0, renorm: false,
        topk_proj: [0; 7], attn_topk: 0, qk_topk: 0, moe_topk: 0,
        attn_window: 0, swa_pattern: 0, attn_sinks: 0 });
    let mut t = Vec::with_capacity(TAILLE_TETE);
    t.extend_from_slice(&MAGIE_FLUX.to_le_bytes());
    t.push(VERSION_FLUX);
    t.push(mode);
    t.extend_from_slice(&debut.to_le_bytes());
    t.extend_from_slice(&fin.to_le_bytes());
    t.extend_from_slice(&pos.to_le_bytes());
    t.extend_from_slice(&(n as u32).to_le_bytes());
    t.extend_from_slice(&echelle.to_le_bytes());
    t.extend_from_slice(&act.levels.to_le_bytes());
    t.extend_from_slice(&act.thresh.to_le_bytes());
    t.extend_from_slice(&act.topk.to_le_bytes());
    t.push(act.renorm as u8);
    for k in act.topk_proj { t.extend_from_slice(&k.to_le_bytes()); }
    t.extend_from_slice(&act.attn_topk.to_le_bytes());
    t.extend_from_slice(&act.qk_topk.to_le_bytes());
    t.extend_from_slice(&act.moe_topk.to_le_bytes());
    t.extend_from_slice(&act.attn_window.to_le_bytes());   // offset 79
    t.extend_from_slice(&act.swa_pattern.to_le_bytes());   // offset 83
    t.extend_from_slice(&act.attn_sinks.to_le_bytes());    // offset 87
    // v8 : le compte de paires du NŒUD (0 côté pilote — champ DIRECTIONNEL).
    let paires_a_dire = mdl.map(|x| x.paires_flux).unwrap_or(0);
    t.extend_from_slice(&paires_a_dire.to_le_bytes());     // offset 91, u64
    assert_eq!(t.len(), TAILLE_TETE,
               "en-tête de flux de {} octets pour {TAILLE_TETE}", t.len());
    t
}

/// Encode les paires d'une liste à échelle par bloc : **écart sur un octet**
/// (255 = échappement, les DEUX octets suivants portent l'indice absolu), puis la
/// valeur i8. Le décodeur est juste en dessous, et les deux sont testés ensemble
/// parce que ce couple a déjà été désaccordé une fois (quatre octets écrits, deux
/// lus) — un désaccord qui ne casse rien tant qu'aucun écart n'atteint 255.
fn encoder_paires_blocs(idx: &[u16], val: &[i8]) -> Vec<u8> {
    let mut paires = Vec::with_capacity(idx.len() * 2);
    let mut prev = 0u32;
    for (&i, &v) in idx.iter().zip(val.iter()) {
        let ecart = i as u32 - prev;
        if ecart < 255 {
            paires.push(ecart as u8);
        } else {
            paires.push(255);
            paires.extend_from_slice(&i.to_le_bytes()[..2]);
        }
        prev = i as u32;
        paires.push(v as u8);
    }
    paires
}

/// Décode `n` paires écrites par `encoder_paires_blocs`.
fn decoder_paires_blocs(corps: &[u8], n: usize) -> Result<(Vec<u16>, Vec<i8>), String> {
    // `n` vient de l'en-tête : deux `with_capacity(n)` sur 4 milliards de paires
    // demandaient 12 Gio AVANT de découvrir que le corps était tronqué (mesuré :
    // VmPeak 12 477 Mio). Le plafond s'applique donc ici aussi.
    if n.saturating_mul(2) > PLAFOND_FLUX {
        return Err(format!("{n} paires annoncées : au-delà du plafond de {} Mo",
                           PLAFOND_FLUX >> 20));
    }
    let mut idx = Vec::with_capacity(n.min(1 << 20));
    let mut val = Vec::with_capacity(n.min(1 << 20));
    let mut prev = 0u32;
    let mut lus = 0usize;
    while idx.len() < n {
        if lus + 1 >= corps.len() {
            return Err(format!("corps de flux tronqué : {} paires lues sur {n}", idx.len()));
        }
        let d = corps[lus]; lus += 1;
        let absolu = if d == 255 {
            if lus + 1 >= corps.len() { return Err("échappement tronqué".into()); }
            let a = u16::from_le_bytes([corps[lus], corps[lus + 1]]) as u32;
            lus += 2;
            a
        } else { prev + d as u32 };
        prev = absolu;
        idx.push(absolu as u16);
        // La garde doit porter sur CHAQUE lecture, y compris celle de la valeur
        // juste après un échappement : sans elle, un corps coupé au mauvais octet
        // paniquait au lieu d'être refusé (attrapé par le test de troncature).
        if lus >= corps.len() { return Err("valeur manquante en fin de corps".into()); }
        val.push(corps[lus] as i8); lus += 1;
    }
    Ok((idx, val))
}

/// Envoie un flux et rend le nombre d'octets écrits (en-tête compris) — c'est ce
/// que la phase 3 doit chiffrer : octets par jeton × latence.
fn envoyer_flux(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos: u32,
                actifs: &[f32], mode: u8, mdl: Option<&model::Model>)
                -> std::io::Result<(usize, usize)> {
    use std::io::Write;
    let (n, echelle, corps): (usize, f32, Vec<u8>) = if mode == MODE_BLOCS {
        let (idx, val, echelles) = mdl.expect("modèle requis pour quantifier un flux")
                                      .flux_en_liste_blocs(actifs);
        // Indices par ÉCARTS : la liste est triée (les blocs sont parcourus dans
        // l'ordre), donc l'écart au neurone précédent tient sur un octet dans
        // l'immense majorité des cas — 255 est l'échappement vers l'indice absolu.
        // Deux octets par neurone actif au lieu de trois, à quantification
        // IDENTIQUE : c'est du rangement, pas de la perte.
        let mut c = Vec::with_capacity(4 + echelles.len() * 4 + idx.len() * 2);
        c.extend_from_slice(&(echelles.len() as u32).to_le_bytes());
        for e in &echelles { c.extend_from_slice(&e.to_le_bytes()); }
        let paires = encoder_paires_blocs(&idx, &val);
        // La longueur est écrite : avec les échappements, elle n'est pas
        // déductible du nombre de paires, et un décodeur qui la suppose lit
        // hors du tampon.
        c.extend_from_slice(&(paires.len() as u32).to_le_bytes());
        c.extend_from_slice(&paires);
        (idx.len(), 0f32, c)
    } else if mode == MODE_LISTE {
        let (idx, val, ech) = mdl.expect("modèle requis pour quantifier un flux")
                                 .flux_en_liste(actifs);
        let mut c = Vec::with_capacity(idx.len() * 4);
        for (&i, &v) in idx.iter().zip(val.iter()) {
            c.extend_from_slice(&i.to_le_bytes());
            c.extend_from_slice(&v.to_le_bytes());
        }
        (idx.len(), ech, c)
    } else {
        let mut c = Vec::with_capacity(actifs.len() * 4);
        for v in actifs { c.extend_from_slice(&v.to_le_bytes()); }
        (actifs.len(), 0f32, c)
    };
    let tete = tete_flux(mode, debut, fin, pos, n, echelle, mdl);
    // **La `pre` portée** (v6) : un octet de compte, puis `np × hc` f32. Les
    // modes 0-2 envoient UN jeton, les modes 3-4 un LOT d'états — et un modèle à
    // hyper-connexions ne prend jamais le chemin des lots (il est refusé), donc
    // `np` vaut 0 ou 1 en pratique ; l'écrire par état laisse la porte ouverte.
    let charge = corps;
    let mut corps = prefixe_premix(mdl, 1);
    corps.extend_from_slice(&charge);
    // UNE SEULE ÉCRITURE, et ce n'est pas de la cosmétique : le protocole écrivait la trame en
    // DEUX fois (en-tête puis corps), donc un pas coûtait QUATRE messages sur un lien qui facture
    // par message — mesuré par la pente délai → pas médian : 4,24 à 2 ms, 4,01 à 5 ms. Une trame,
    // un envoi : le pas retombe à ~2 messages, soit −29 % de sa durée sur un lien à 5 ms/message,
    // sans toucher ni au calcul ni aux octets.
    let mut trame = Vec::with_capacity(tete.len() + corps.len());
    trame.extend_from_slice(&tete);
    trame.extend_from_slice(&corps);
    s.write_all(&trame)?;
    s.flush()?;
    Ok((TAILLE_TETE + corps.len(), n))
}

/// Le préfixe de corps du protocole v6 : un octet `np`, puis `np × hc` f32.
///
/// Un SEUL encodeur pour les trois émetteurs (jeton, lot dense, lot en listes).
/// Ils écrivaient le même en-tête mais un seul avait reçu ce préfixe : les modes
/// 3 et 4 (lots) envoyaient donc un corps que le décodeur v6 lisait de travers —
/// le premier octet du premier état passait pour le compte `np`, et la suite
/// était décalée de 4 octets. Un mode entier, faux et muet.
///
/// `t` est le nombre d'états du flux : la `pre` portée appartient à UN état, donc
/// un lot de plus d'un état ne peut pas en porter une (et n'en porte pas : le
/// chemin des lots refuse les modèles à hyper-connexions).
fn prefixe_premix(mdl: Option<&model::Model>, t: usize) -> Vec<u8> {
    let premix: Vec<f32> = mdl.and_then(|m| m.hc_porte_flux.clone()).unwrap_or_default();
    let hc = mdl.map(|m| m.hc.as_ref().map(|v| v[0].0.hc).unwrap_or(1)).unwrap_or(1);
    assert!(t == 1 || premix.is_empty(),
            "un flux de {t} états ne peut pas porter la `pre` d'un seul : le préremplissage \
réparti est refusé aux modèles à chaîne mHC retardée");
    let np: u8 = if premix.is_empty() { 0 } else { 1 };
    assert!(premix.len() == np as usize * hc,
            "pré-mix de {} valeurs pour {np} état(s) × {hc} copies", premix.len());
    let mut p = Vec::with_capacity(1 + premix.len() * 4);
    p.push(np);
    for v in &premix { p.extend_from_slice(&v.to_le_bytes()); }
    p
}

/// Envoie un LOT d'états (`t × hidden`, aplati) dans un seul flux.
///
/// Le lot voyage en f32 dense : c'est le mode de la phase 3.4 (préremplissage
/// réparti), où la latence domine tout — le quantifier est la suite, et il faudra
/// alors une liste PAR ÉTAT, ce que ce cadriciel ne sait pas encore décrire.
fn envoyer_lot(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos0: u32,
               etats: &[f32], t: usize, mdl: &model::Model) -> std::io::Result<usize> {
    use std::io::Write;
    let tete = tete_flux(MODE_LOT, debut, fin, pos0, t, 0.0, Some(mdl));
    // Le préfixe v6 (`np` + `pre`) manquait ICI : le décodeur du pair le lisait
    // dans le premier état du lot et décalait tout le reste de quatre octets.
    let prefixe = prefixe_premix(Some(mdl), t);
    let mut corps = Vec::with_capacity(prefixe.len() + etats.len() * 4);
    corps.extend_from_slice(&prefixe);
    for v in etats { corps.extend_from_slice(&v.to_le_bytes()); }
    // UNE SEULE ÉCRITURE, et ce n'est pas de la cosmétique : le protocole écrivait la trame en
    // DEUX fois (en-tête puis corps), donc un pas coûtait QUATRE messages sur un lien qui facture
    // par message — mesuré par la pente délai → pas médian : 4,24 à 2 ms, 4,01 à 5 ms. Une trame,
    // un envoi : le pas retombe à ~2 messages, soit −29 % de sa durée sur un lien à 5 ms/message,
    // sans toucher ni au calcul ni aux octets.
    let mut trame = Vec::with_capacity(tete.len() + corps.len());
    trame.extend_from_slice(&tete);
    trame.extend_from_slice(&corps);
    s.write_all(&trame)?;
    s.flush()?;
    Ok(TAILLE_TETE + corps.len())
}

/// **Un état** encodé comme le mode 2 : `a_j · n_blocs_j · longueur_j`, puis les
/// échelles f32 par bloc de 32 canaux, puis les paires (écart u8, valeur i8).
///
/// L'ordre est délibéré : les trois tailles se lisent d'un `read_exact` de 12
/// octets AVANT toute allocation, et un état est sautable sans lire le reste.
fn encoder_etat_blocs(mdl: &model::Model, etat: &[f32]) -> Vec<u8> {
    let (idx, val, echelles) = mdl.flux_en_liste_blocs(etat);
    let paires = encoder_paires_blocs(&idx, &val);
    let mut c = Vec::with_capacity(12 + echelles.len() * 4 + paires.len());
    c.extend_from_slice(&(idx.len() as u32).to_le_bytes());
    c.extend_from_slice(&(echelles.len() as u32).to_le_bytes());
    c.extend_from_slice(&(paires.len() as u32).to_le_bytes());
    for e in &echelles { c.extend_from_slice(&e.to_le_bytes()); }
    c.extend_from_slice(&paires);
    c
}

/// Envoie un LOT d'états **en listes** (mode 4).
fn envoyer_lot_listes(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos0: u32,
                      etats: &[f32], t: usize, mdl: &model::Model)
                      -> std::io::Result<usize> {
    use std::io::Write;
    let h = mdl.cfg.hidden;
    let prefixe = prefixe_premix(Some(mdl), t);
    let mut corps: Vec<u8> = Vec::with_capacity(prefixe.len() + t * 64);
    corps.extend_from_slice(&prefixe);
    for i in 0..t {
        corps.extend_from_slice(&encoder_etat_blocs(mdl, &etats[i * h..(i + 1) * h]));
    }
    let tete = tete_flux(MODE_LOT_LISTES, debut, fin, pos0, t, 0.0, Some(mdl));
    // UNE SEULE ÉCRITURE, et ce n'est pas de la cosmétique : le protocole écrivait la trame en
    // DEUX fois (en-tête puis corps), donc un pas coûtait QUATRE messages sur un lien qui facture
    // par message — mesuré par la pente délai → pas médian : 4,24 à 2 ms, 4,01 à 5 ms. Une trame,
    // un envoi : le pas retombe à ~2 messages, soit −29 % de sa durée sur un lien à 5 ms/message,
    // sans toucher ni au calcul ni aux octets.
    let mut trame = Vec::with_capacity(tete.len() + corps.len());
    trame.extend_from_slice(&tete);
    trame.extend_from_slice(&corps);
    s.write_all(&trame)?;
    s.flush()?;
    Ok(TAILLE_TETE + corps.len())
}

/// Reçoit un flux : `(debut, fin, pos, mode, charge utile)`.
fn recevoir_flux(s: &mut std::net::TcpStream, hidden: usize, hc_destinataire: usize)
                -> std::io::Result<Flux> {
    use std::io::Read;
    let mut tete = [0u8; TAILLE_TETE];
    s.read_exact(&mut tete)?;
    let u = |o: usize| u32::from_le_bytes([tete[o], tete[o+1], tete[o+2], tete[o+3]]);
    if u(0) != MAGIE_FLUX {
        return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
                                       "magie de flux absente"));
    }
    let version = tete[4];
    let mode = tete[5];
    if version != VERSION_FLUX {
        // Refus EXPLICITE : on ne devine pas la version du pair, on la nomme.
        return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
            format!("flux en version {version}, cette build parle la {VERSION_FLUX} \
                     (pair incompatible : rien n'a été interprété)")));
    }
    let (debut, fin, pos) = (u(6), u(10), u(14));
    let n = u(18) as usize;
    let echelle = f32::from_le_bytes([tete[22], tete[23], tete[24], tete[25]]);
    let mut topk_proj = [0u32; 7];
    for (i, v) in topk_proj.iter_mut().enumerate() { *v = u(39 + i * 4); }
    // v8 : le compte de paires du pair (0 si c'est le pilote qui a parlé).
    let paires_du_pair = u64::from_le_bytes([tete[91], tete[92], tete[93], tete[94],
                                             tete[95], tete[96], tete[97], tete[98]]);
    // v7/v8 : le nœud annonce ce qu'il a calculé ; le pilote le cumule. Un pilote qui reçoit
    // reçoit TOUJOURS, et un nœud qui répond met son compte — le champ est directionnel.
    // Le compteur du nœud est CUMULATIF depuis le premier pas : l'additionner à chaque trame
    // comptait donc les premiers pas une fois par trame — mesuré : 4 293,9 M par pas là où le
    // modèle entier en vaut 358 M, soit ~24× trop (47 pas, la somme des cumuls vaut N²/2).
    // On garde le DERNIER, qui est le total.
    PAIRES_DU_PAIR.fetch_max(paires_du_pair, std::sync::atomic::Ordering::Relaxed);
    let act = Act {
        attn_window: u(79), swa_pattern: u(83), attn_sinks: u(87),
        levels: f32::from_le_bytes([tete[26], tete[27], tete[28], tete[29]]),
        thresh: f32::from_le_bytes([tete[30], tete[31], tete[32], tete[33]]),
        topk: u(34),
        renorm: tete[38] != 0,
        topk_proj,
        attn_topk: u(67),
        qk_topk: u(71),
        moe_topk: u(75),
    };
    // Le mode est vérifié AVANT de lire le moindre octet de corps : un mode
    // inconnu se refusait après avoir lu `n × 4` octets et s'être désynchronisé,
    // en disant « mode inconnu » — exact, tardif, et muet sur la cause.
    // Un flux à zéro élément n'est illégitime que là où `n` est une DIMENSION
    // (mode 0) ou un nombre d'ÉTATS (modes 3 et 4). En modes 1 et 2, `n` est un
    // nombre de PAIRES : une liste VIDE est légitime — un vecteur d'activation
    // peut n'avoir aucun actif (seuil au-dessus du maximum, état exactement nul),
    // et c'est même ce que répond le pair factice du dépôt. Refuser n == 0 partout
    // tuait ces sessions (relevé par la relecture adversariale du mode 4).
    if n == 0 && matches!(mode, MODE_DENSE | MODE_LOT | MODE_LOT_LISTES) {
        return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
            format!("flux de zéro {} : refusé (R4 de docs/plan-prefill-reparti.md)",
                    if mode == MODE_DENSE { "canal" } else { "état" })));
    }
    match mode {
        MODE_DENSE | MODE_LISTE | MODE_BLOCS | MODE_LOT | MODE_LOT_LISTES => {}
        autre => return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
            format!("mode de flux inconnu : {autre} (cette build parle les modes 0 à \
{MODE_LOT_LISTES}, protocole v{VERSION_FLUX})"))),
    }
    // Le plafond du mode LOT se vérifie AVANT de lire quoi que ce soit du corps :
    // sinon un en-tête forgé faisait lire un octet de pré-mix sur une trame
    // tronquée et rendait « failed to fill whole buffer » au lieu du refus qui
    // nomme le plafond (test `un_lot_dement_grand_est_refuse_avant_allocation`).
    if mode == MODE_LOT {
        verifier_taille(n.checked_mul(hidden).and_then(|x| x.checked_mul(4))
                          .unwrap_or(usize::MAX),
                        &format!("lot de {n} états × {hidden} canaux"))?;
    }
    // **La `pre` portée** (v6) ouvre le corps : un octet de compte puis
    // `np × hc` f32. Le `hc` du DESTINATAIRE fait foi — c'est son modèle qui
    // décide de la largeur, comme pour les états (`hidden` vient de lui).
    let hc = hc_destinataire;
    let mut premix: Vec<f32> = Vec::new();
    let mut np = [0u8; 1];
    s.read_exact(&mut np)?;
    let np = np[0] as usize;
    if np > 0 {
        // Plafond AVANT d'allouer : `np` vient du réseau.
        verifier_taille(np.checked_mul(hc).and_then(|x| x.checked_mul(4)).unwrap_or(usize::MAX),
                        &format!("pré-mix de {np} état(s) × {hc} copies"))?;
        let mut octets = vec![0u8; np * hc * 4];
        s.read_exact(&mut octets)?;
        premix = octets.chunks_exact(4)
            .map(|c| f32::from_le_bytes(c.try_into().unwrap())).collect();
    }
    // Ce préfixe fait partie du CORPS : l'émetteur le compte dans ses octets
    // envoyés, donc l'omettre ici faisait paraître le retour plus court de
    // `1 + 4·np·hc` octets — 17 sur un flux V4.1, d'où un « 81 999 au retour »
    // publié pour 82 016 réels (relevé par la relecture adverse du bloc 13).
    let octets_prefixe = 1 + np * hc * 4;
    let charge = match mode {
        MODE_LOT_LISTES => {
            // `n` = nombre d'ÉTATS. Chaque état est auto-délimité :
            // `a_j · n_blocs_j · longueur_j`, puis les échelles f32 par bloc de 32,
            // puis les paires (écart u8, valeur i8). Les trois tailles se lisent
            // AVANT toute allocation, et le corps entier n'est plus borné par
            // l'en-tête : chaque taille passe donc par le plafond R4.
            verifier_taille(n.checked_mul(hidden).and_then(|x| x.checked_mul(4))
                              .unwrap_or(usize::MAX),
                            &format!("lot en listes de {n} états × {hidden} canaux"))?;
            let attendu = hidden.div_ceil(32);
            let mut plat: Vec<f32> = Vec::with_capacity(n * hidden);
            let mut lus = 0usize;
            let mut hors_total = 0usize;
            for j in 0..n {
                let mut p = [0u8; 12];
                s.read_exact(&mut p)?;
                let a = u32::from_le_bytes([p[0], p[1], p[2], p[3]]) as usize;
                let nb = u32::from_le_bytes([p[4], p[5], p[6], p[7]]) as usize;
                let lg = u32::from_le_bytes([p[8], p[9], p[10], p[11]]) as usize;
                verifier_taille(a.saturating_mul(2), &format!("état {j} : {a} actifs"))?;
                verifier_taille(nb.saturating_mul(4), &format!("état {j} : {nb} blocs"))?;
                verifier_taille(lg, &format!("état {j} : {lg} octets de paires"))?;
                verifier_taille(12usize.saturating_add(nb.saturating_mul(4)).saturating_add(lg),
                                &format!("état {j}"))?;
                if a > hidden {
                    return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
                        format!("état {j} : {a} actifs pour {hidden} canaux — un \
encodeur légitime ne peut pas en produire autant")));
                }
                if nb != attendu {
                    return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
                        format!("état {j} : {nb} blocs d'échelles pour {hidden} canaux \
({attendu} attendus) — les deux nœuds n'ont pas le même GGUF ?")));
                }
                if lg < a.saturating_mul(2) || lg > a.saturating_mul(4).max(4) {
                    return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
                        format!("état {j} : {lg} octets de paires pour {a} actifs — \
incohérent (attendu entre {} et {})", a * 2, a * 4)));
                }
                let mut eb = vec![0u8; nb * 4];
                s.read_exact(&mut eb)?;
                let echelles: Vec<f32> = (0..nb).map(|k| f32::from_le_bytes(
                    [eb[k*4], eb[k*4+1], eb[k*4+2], eb[k*4+3]])).collect();
                let mut corps = vec![0u8; lg];
                s.read_exact(&mut corps)?;
                let (idx, val) = match decoder_paires_blocs(&corps, a) {
                    Ok(v) => v,
                    Err(e) => return Err(std::io::Error::new(
                        std::io::ErrorKind::InvalidData, format!("état {j} : {e}"))),
                };
                let base = plat.len();
                plat.resize(base + hidden, 0.0);
                let mut hors = 0usize;
                for (&i, &v) in idx.iter().zip(val.iter()) {
                    let b = i as usize / 32;
                    if (i as usize) < hidden && b < echelles.len() {
                        plat[base + i as usize] = v as f32 * echelles[b];
                    } else { hors += 1; }
                }
                hors_total += hors;
                lus += 12 + nb * 4 + lg;
                // Le plan l'exige et le code ne le faisait pas : chaque état peut
                // être légal et le TOTAL ne pas l'être — un pair annonçait
                // 268 Mo par état sur 74 898 états. La mémoire reste bornée (on
                // décode état par état), le TEMPS non.
                verifier_taille(lus, &format!("corps du lot en listes (cumul après \
l'état {j})"))?;
            }
            if hors_total > 0 {
                // UNE ligne par message : une trame forgée de 200 états en
                // produisait 200 (le plan demandait déjà l'inverse).
                eprintln!("[flux] {hors_total} indice(s) hors dimension ignorés sur \
l'ensemble du lot (flux reçu de {hidden} canaux)");
            }
            // Octets réellement lus SUR LE FIL : c'est ce que le banc doit
            // afficher, pas la taille du vecteur dense reconstruit en mémoire.
            let octets_corps = octets_prefixe + lus;
            return Ok(Flux { n, debut, fin, pos, mode, act, premix: premix.clone(), octets_corps,
                             charge: ChargeFlux::Lot(plat) });
        }
        MODE_LOT => {
            // `n` est le nombre d'ÉTATS, pas de canaux : la dimension vient du
            // modèle du nœud qui reçoit, elle n'a pas à voyager.
            let taille = n.checked_mul(hidden).and_then(|x| x.checked_mul(4))
                         .unwrap_or(usize::MAX);
            verifier_taille(taille, &format!("lot de {n} états × {hidden} canaux"))?;
            let mut corps = vec![0u8; taille];
            s.read_exact(&mut corps)?;
            let etats = (0..n * hidden).map(|k| f32::from_le_bytes(
                [corps[k*4], corps[k*4+1], corps[k*4+2], corps[k*4+3]])).collect();
            return Ok(Flux { n, debut, fin, pos, mode, act, premix: premix.clone(), octets_corps: octets_prefixe + corps.len(),
                             charge: ChargeFlux::Lot(etats) });
        }
        MODE_BLOCS => {
            // corps : nombre de blocs u32 · blocs × f32 · n × (u16 · i8)
            let mut nb = [0u8; 4];
            s.read_exact(&mut nb)?;
            let n_blocs = u32::from_le_bytes(nb) as usize;
            // Le plafond vaut pour TOUTE taille lue dans l'en-tête : `n_blocs`
            // autant que `longueur`. Sans cette ligne, une trame de 83 octets
            // annonçant 4 milliards de blocs faisait allouer 16 Gio (mesuré par la
            // relecture adversariale : VmSize 17 572 760 ko sur une seule trame).
            verifier_taille(n_blocs.saturating_mul(4), &format!("{n_blocs} blocs d'échelles"))?;
            let mut eb = vec![0u8; n_blocs * 4];
            s.read_exact(&mut eb)?;
            let echelles = (0..n_blocs).map(|k| f32::from_le_bytes(
                [eb[k*4], eb[k*4+1], eb[k*4+2], eb[k*4+3]])).collect();
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
            let octets_corps = octets_prefixe + 4 + n_blocs * 4 + 4 + longueur;
            return Ok(Flux { n, debut, fin, pos, mode, act, premix: premix.clone(), octets_corps, charge:
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
            for k in 0..n {
                idx.push(u16::from_le_bytes([octets[k*4], octets[k*4+1]]));
                val.push(i16::from_le_bytes([octets[k*4+2], octets[k*4+3]]));
            }
            ChargeFlux::Liste { idx, val, echelle }
        }
        autre => return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
            format!("mode de flux inconnu : {autre}"))),
    };
    Ok(Flux { n, debut, fin, pos, mode, act, premix, octets_corps: octets_prefixe + octets.len(), charge })
}

/// Le NŒUD MOTEUR : charge le modèle, écoute, applique SA plage de couches au
/// flux reçu et renvoie le flux résultant. Un seul client à la fois — c'est un
/// banc d'essai, pas un service.
/// C5ter : le BUS par le réseau.
///
/// POURQUOI. C5bis savait diffuser un réglage par un FICHIER relu à chaque pas, ce
/// qui suppose un système de fichiers partagé — donc pas deux machines. Un bus qui
/// n'atteint pas la deuxième machine n'est pas un bus distribué, c'est un fichier de
/// configuration.
///
/// CE QUI EST BORNÉ, ET POURQUOI. Un modulateur qui se connecte et n'envoie rien ne
/// doit pas empêcher les autres de parler (d'où un fil par connexion) ; mais des
/// connexions sans fin ne doivent pas non plus créer des fils sans fin (d'où la
/// borne de 8, au-delà de laquelle on REFUSE en le disant). Un canal n'est appliqué
/// qu'après validation complète de la ligne : une valeur non finie ferait diverger
/// silencieusement toute l'exécution.
///
/// CE QUE ÇA COÛTE : le verrou du bus est pris UNE fois par ligne reçue, pas par pas
/// de calcul. Une ligne de contrôle coûte donc un aller-retour réseau, et rien au
/// calcul.
fn demarrer_bus_serveur(port: u16, bus: std::sync::Arc<std::sync::Mutex<bus::Bus>>) {
    use std::io::Write;
    let ecoute = match std::net::TcpListener::bind(("0.0.0.0", port)) {
        Ok(l) => l,
        Err(e) => {
            eprintln!("[bus] écoute sur le port {port} impossible : {e} — ce processus \
n'est pilotable que par fichier");
            return;
        }
    };
    println!("[bus] écoute sur 0.0.0.0:{port} · « MODULATION canal valeur », une ligne par \
réglage. Sur TOUTES les interfaces : un bus qu'on ne peut pas piloter à distance n'est pas \
un bus distribué — si la machine est exposée, c'est un choix à faire en connaissance.");
    std::thread::spawn(move || {
        let actifs = std::sync::Arc::new(std::sync::atomic::AtomicUsize::new(0));
        for flux in ecoute.incoming() {
            let mut sock = match flux { Ok(s) => s, Err(_) => continue };
            let n = actifs.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            if n >= 8 {
                actifs.fetch_sub(1, std::sync::atomic::Ordering::SeqCst);
                let _ = writeln!(sock, "bus : trop de modulateurs connectés (8 au plus)");
                continue;
            }
            let bus = std::sync::Arc::clone(&bus);
            let actifs = std::sync::Arc::clone(&actifs);
            let lecteur = match sock.try_clone() {
                Ok(s) => std::io::BufReader::new(s),
                Err(_) => { actifs.fetch_sub(1, std::sync::atomic::Ordering::SeqCst); continue; }
            };
            std::thread::spawn(move || {
                use std::io::BufRead;
                for ligne in lecteur.lines() {
                    let ligne = match ligne { Ok(l) => l, Err(_) => break };
                    if ligne.trim().is_empty() { continue; }
                    // UN SEUL verrou, et la valeur relue DANS le même : `match
                    // bus.lock()…` garderait le garde jusqu'à la fin du match, et le
                    // second `lock()` de la branche se bloquerait lui-même.
                    let res = {
                        let mut b = bus.lock().unwrap();
                        b.appliquer_ligne(&ligne).map(|canal| {
                            let v = b.lire(&canal);
                            (canal, v)
                        })
                    };
                    match res {
                        Ok((canal, v)) => {
                            println!("[bus] {canal} = {v} (reçu par le réseau)");
                            let _ = writeln!(sock, "OK {canal} {v}");
                        }
                        Err(e) => {
                            eprintln!("[bus] {e}");
                            let _ = writeln!(sock, "ERREUR {e}");
                        }
                    }
                }
                actifs.fetch_sub(1, std::sync::atomic::Ordering::SeqCst);
            });
        }
    });
}

/// Relit le fichier de contrôle du bus, si un chemin est donné.
///
/// POURQUOI UNE FONCTION : le pilote et le nœud faisaient la même chose à deux
/// endroits — et c'est le genre de duplication où l'un des deux finit par accepter
/// ce que l'autre refuse. Ici, une seule définition de ce qu'est une ligne de bus.
fn rafraichir_bus_fichier(bus: &std::sync::Arc<std::sync::Mutex<bus::Bus>>, fichier: &Option<String>) {
    let Some(bf) = fichier else { return };
    let Ok(contenu) = std::fs::read_to_string(bf) else { return };
    for ligne in contenu.lines() {
        if ligne.trim().is_empty() || ligne.starts_with('#') { continue; }
        if let Err(e) = bus.lock().unwrap().appliquer_ligne(ligne) {
            eprintln!("[bus] {e}");
        }
    }
}

fn run_serveur_flux(opt: Options, adresse: &str) {
    if opt.tete_partielle {
        eprintln!("[plage] `--tete-partielle` est sans effet sur un SERVEUR de flux : ce \
nœud rend un flux résiduel BRUT par contrat (la tête appartient au nœud qui la possède)");
    }
    // `port` reste localhost ; `hôte:port` écoute sur l'interface nommée
    // (« 0.0.0.0:5599 » pour un pair distant). Le pair distant est le cas de la
    // phase 3.4 : un nœud Colab, ou une autre machine du réseau.
    let (hote, port) = match adresse.rsplit_once(':') {
        Some((h, p)) => (h.to_string(), p.parse().expect("port invalide")),
        None => ("127.0.0.1".to_string(), adresse.parse().expect("port invalide")),
    };
    let chemin = modele_chemin();
    // Le contexte du nœud moteur suit `--ctx` : figé à 4096, il faisait payer au
    // pair des tampons d'attention seize fois plus grands que le banc (mesuré :
    // 4,8 s contre 1,7 s pour le même calcul, à contexte 256).
    let ctx = if opt.ctx_impose { opt.ctx } else { 4096 };
    let mut mdl = model::Model::load(&chemin, ctx, fils(&opt), true, opt.keep, false, 0, 0);
    appliquer_quantification(&mut mdl, &opt);
    if opt.options_actives { options_actives(&mdl, "nœud moteur du flux", opt.ctx_impose, true, opt.keep, true); }
    let hidden = mdl.cfg.hidden;
    let hc_local = mdl.hc.as_ref().map(|v| v[0].0.hc).unwrap_or(1);
    // C5 : le bus du NŒUD, créé ICI — avant l'écoute, et donc avant `accept()`.
    // L'ordre n'est pas cosmétique : placé après `accept()`, le nœud restait
    // bloqué en attente du pilote et son bus n'écoutait pas encore, donc une ligne
    // envoyée « avant le premier pas » arrivait en réalité dans le vide
    // (ConnectionRefused — trouvé par la porte C5ter). Un bus qui ne s'ouvre
    // qu'après la connexion ne peut pas moduler le premier pas, et le premier pas
    // est justement celui qu'on veut moduler.
    let bus0 = bus::Bus::analyser(&opt.bus).unwrap_or_else(|e| {
        eprintln!("{e}"); std::process::exit(2) });
    // C5bis : le bus est PARTAGÉ et un fil d'écoute le met à jour par le réseau.
    // Une diffusion doit pouvoir changer un canal PENDANT l'exécution — sinon ce
    // n'est pas un bus, c'est un réglage de démarrage.
    let bus = std::sync::Arc::new(std::sync::Mutex::new(bus0));
    if let Some(p) = opt.bus_serveur { demarrer_bus_serveur(p, std::sync::Arc::clone(&bus)); }
    if !bus.lock().unwrap().est_neutre() {
        println!("[bus] canaux actifs sur ce nœud : {}",
                 bus.lock().unwrap().canaux().iter().map(|(k, v)| format!("{k}={v}")).collect::<Vec<_>>().join(" "));
    }
    let ecoute = std::net::TcpListener::bind((hote.as_str(), port)).expect("écoute");
    println!("[flux] nœud moteur sur {hote}:{port} · {hidden} cachés · {} couches · contexte {ctx}",
             mdl.cfg.n_layer);
    let (mut sock, pair) = ecoute.accept().expect("connexion");
    // TCP_NODELAY, et ce n'est pas un détail de confort : sans lui, Nagle garde
    // une petite écriture en attendant l'acquittement de la précédente, et l'ACK
    // différé du pair la retarde encore. Mesuré sur localhost, 12 couches
    // distantes : **97,6 ms** d'attente contre 15,6 ms de calcul local — six fois
    // le calcul, payés par la seule latence du protocole.
    // ---- C1b : LE RELAIS. Un nœud du milieu applique SA plage (celle que la
    // trame lui donne) puis transmet à son successeur, au lieu de répondre à son
    // appelant. Le découpage voyage DÉJÀ dans la trame (`f.debut`, `f.fin`) : le
    // relais n'a donc qu'à réexpédier une trame portant la plage du successeur.
    // Le retour se fait de proche en proche — le pilote n'a pas à connaître le
    // nombre de relais.
    let mut successeur: Option<(std::net::TcpStream, u32, u32)> = None;
    let mut delai_relais: u64 = 0;
    match (&opt.topologie, &opt.region) {
        (None, None) => {}
        (Some(_), None) => {
            eprintln!("--topologie sur un nœud exige --region : sans identifiant, le nœud ne \
sait ni sa plage ni à qui transmettre"); std::process::exit(2);
        }
        (None, Some(_)) => {
            eprintln!("--region sans --topologie : la plage et le successeur viennent du \
fichier de topologie"); std::process::exit(2);
        }
        (Some(f), Some(moi)) => {
            let texte = std::fs::read_to_string(f).unwrap_or_else(|e| {
                eprintln!("topologie : lecture de {f} impossible : {e}"); std::process::exit(2) });
            let t = topologie::lire_json(&texte).unwrap_or_else(|e| {
                eprintln!("{e}"); std::process::exit(3) });
            t.valider().unwrap_or_else(|e| { eprintln!("{e}"); std::process::exit(3) });
            let ma = t.region(moi).unwrap_or_else(|| {
                eprintln!("topologie : aucune région « {moi} » — le nœud s'arrête plutôt que \
d'appliquer une plage inventée"); std::process::exit(3) }).clone();
            println!("[relais] région « {} » : couches {}..{}", ma.id, ma.premiere, ma.derniere);
            match t.successeur(moi) {
                Ok(None) => println!("[relais] sortie du graphe : ce nœud rend son état à son appelant"),
                Ok(Some(lien)) => {
                    if mdl.hc.is_some() {
                        eprintln!("[relais] refusé : un modèle à hyper-connexions fait voyager une \
`pre` que le relais ne transporte pas encore (v6) — mieux vaut refuser que mesurer autre chose");
                        std::process::exit(3);
                    }
                    if lien.delai_ms > 0 {
                        println!("[delais] lien {} → {} : +{} ms par trame (le résultat ne \
doit pas changer)", ma.id, lien.vers, lien.delai_ms);
                    }
                    delai_relais = lien.delai_ms;
                    let cible = t.region(&lien.vers).unwrap().clone();
                    // C11 : même résolution côté nœud, pour la même raison — sans elle, un
                    // relais ne saurait pas joindre un successeur nommé.
                    let adresse_succ = resoudre_instance(&cible.instance, &opt.registre);
                    let mut sc = std::net::TcpStream::connect(&adresse_succ).unwrap_or_else(|e| {
                        eprintln!("[relais] connexion au successeur « {} » ({}) impossible : {e}",
                                  cible.id, cible.instance); std::process::exit(1) });
                    sc.set_nodelay(true).expect("TCP_NODELAY");
                    println!("[relais] successeur : « {} » sur {} (couches {}..{})",
                             cible.id, cible.instance, cible.premiere, cible.derniere);
                    // Fin EXCLUSIVE ici aussi (voir le pilote).
                    successeur = Some((sc, cible.premiere as u32, (cible.derniere + 1) as u32));
                }
                Err(e) => { eprintln!("{e}"); std::process::exit(3); }
            }
        }
    }
    // C5 : le bus du NŒUD. Chaque région décide de ce qu'elle fait du canal ; ici
    // le gain s'applique à l'état que le nœud produit, avant de le rendre.
    sock.set_nodelay(true).expect("TCP_NODELAY");
    println!("[flux] client connecté : {pair}");
    let mut servis = 0u64;
    // C12bis : la trace du NŒUD. Jusqu'ici le pilote traçait seul, donc une
    // divergence sur un lien n'était visible que d'un bout — impossible de dire si
    // c'est l'envoi ou la réception qui avait dérivé. Le nœud enregistre donc les
    // DEUX sens sous les MÊMES noms de lien que le pilote : « local->pair » pour ce
    // qu'il reçoit, « pair->local » pour ce qu'il rend. C'est cette convention —
    // et non une tolérance de temps — qui rend la fusion capable de confronter les
    // deux bouts d'un même croisement.
    let region_trace = opt.region.clone().unwrap_or_else(|| "pair".to_string());
    let mut trace = trace_globale::TraceGlobale::nouvelle();
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
                // Largeur attendue : `cachés` — ou `hc × cachés` pour un modèle
                // à **hyper-connexions**, dont l'état résiduel voyage en `hc`
                // copies (les réduire au point de coupure change le modèle :
                // perplexité répartie 8 311 → 34 159). Le protocole accepte donc
                // les deux largeurs, et c'est le MODÈLE des deux côtés qui dit
                // laquelle est légitime.
                let hc_mult = mdl.hc.as_ref().map(|v| v[0].0.hc).unwrap_or(1);
                let largeur_etat = hidden * hc_mult;
                if f.mode == MODE_DENSE && f.n != hidden && f.n != largeur_etat {
                    println!("[flux] flux refusé : {} canaux annoncés, {hidden} (ou \
{largeur_etat} avec hyper-connexions) attendus — le nœud continue", f.n);
                    continue;
                }
                if f.pos as usize >= ctx_local
                   && !(f.mode == MODE_LOT || f.mode == MODE_LOT_LISTES) {
                    println!("[flux] flux refusé : position {} au-delà du contexte {} — le \
nœud continue", f.pos, ctx_local);
                    continue;
                }
                // Les réglages du client s'appliquent ICI : les deux nœuds
                // doivent quantifier les activations pareil, sinon ils ne
                // calculent pas la même chose.
                f.act.appliquer(&mut mdl);
                mdl.couche_debut = f.debut as usize;
                mdl.couche_fin = f.fin as usize;
                // Le nœud moteur rend TOUJOURS un flux résiduel brut : la norme
                // finale appartient au nœud qui a la tête de sortie, et à lui
                // seul. C'est ce qui manquait — 798,3 au lieu de 18,2.
                mdl.flux_brut = true;
                // Les DEUX modes de lot : 3 (dense f32) et 4 (listes). Oublier le
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
                        // `continue` et non `break` : le nœud doit continuer à
                        // servir les lots suivants (le message le disait déjà, le
                        // code faisait l'inverse — relevé par la relecture de
                        // clôture).
                        println!("[flux] lot refusé : {t} états à partir de la position {} \
                                  dépassent le contexte {} de ce nœud — lot ignoré, le nœud \
continue", f.pos, mdl.ctx);
                        continue;
                    }
                    let mut recu_lot = f.charge.plat().to_vec();
                    // Le pont s'applique PAR ÉTAT : la largeur d'un état est
                    // `largeur_etat`, pas la longueur du lot entier.
                    if opt.pont_k > 0 {
                        for q in recu_lot.chunks_mut(largeur_etat) {
                            pont_sparsifier(q, opt.pont_k);
                        }
                    }
                    trace.enregistrer_mode(&region_trace, f.pos as u32, "local->pair",
                                           &recu_lot, 0.0, f.mode);
                    mdl.emb_imposee_lot = Some(recu_lot);
                    let hs = mdl.forward_lot(&vec![0u32; t], f.pos as usize);
                    let mut plat: Vec<f32> = hs.concat();
                    if opt.pont_k > 0 {
                        for q in plat.chunks_mut(largeur_etat) {
                            pont_sparsifier(q, opt.pont_k);
                        }
                    }
                    if std::env::var("DRAVE_DEBUG_FLUX").is_ok() {
                        eprintln!("[debug] lot reçu : n={t} pos={} états={} plat={} corps={}",
                                  f.pos, hs.len(), plat.len(), f.octets_corps);
                    }
                    mdl.paires_flux = mdl.paires.iter().sum();
                    trace.enregistrer_mode(&region_trace, f.pos as u32, "pair->local",
                                           &plat, 0.0, f.mode);
                    let reponse = if f.mode == MODE_LOT_LISTES {
                        envoyer_lot_listes(&mut sock, f.debut, f.fin, f.pos, &plat, t, &mdl)
                    } else {
                        envoyer_lot(&mut sock, f.debut, f.fin, f.pos, &plat, t, &mdl)
                    };
                    if reponse.is_err() { break; }
                    servis += 1;
                    continue;
                }
                // Largeur de DÉCODAGE : celle du modèle (4096, ou 16 384 avec
                // hyper-connexions) — jamais `f.n`, qui vaut le nombre de
                // CANAUX en mode dense mais le nombre de PAIRES en modes 1 et 2.
                // Les confondre donnait un état de 16 362 valeurs au lieu de
                // 16 384, et `Hc::melanger` sortait de la tranche.
                let mut recu = f.charge.en_dense(largeur_etat);
                // C9/C10 : le pont, côté nœud. Le même réglage que le pilote, sinon le
                // lien n'est limité que dans UN sens — et la mesure le montrait :
                // 1 096 octets à l'aller contre 1 959 au retour, parce que le nœud
                // renvoyait tout. Un corps calleux à moitié coupé n'est pas un pont.
                if opt.pont_k > 0 { pont_sparsifier(&mut recu, opt.pont_k); }
                trace.enregistrer_mode(&region_trace, f.pos as u32, "local->pair",
                                       &recu, 0.0, f.mode);
                mdl.emb_imposee = Some(recu);
                // **La `pre` portée** (v6) : sans elle, la chaîne retardée de V4.1
                // replierait son premier raccord avec la copie 0 — faux, et muet.
                // Le moteur REFUSE ce cas (`forward`), donc un pair en v5 ne peut
                // pas non plus passer par surprise.
                //
                // **Elle n'a de sens que si ce nœud REPREND au milieu du modèle.**
                // Une trame qui demande `debut = 0` fait entrer l'état imposé par
                // la couche 0 : la chaîne du modèle y commence, la `pre` d'un
                // raccord précédent n'existe pas, et l'ignorer en silence serait
                // exactement le défaut qu'on vient de corriger. Une trame pareille
                // n'est émise par personne (le pilote envoie `couches_locales ≥ 1`),
                // donc la refuser ne coûte rien et ferme le cas.
                if !f.premix.is_empty() && f.debut == 0 {
                    println!("[flux] flux refusé : la trame porte une `pre` (v6) mais demande \
de reprendre à la couche 0 — la chaîne mHC retardée commence là, cette `pre` n'a pas de \
raccord précédent où s'appliquer et l'ignorer serait muet. Le nœud continue");
                    continue;
                }
                mdl.hc_porte_imposee = if f.premix.is_empty() { None } else { Some(f.premix.clone()) };
                // C5bis : le bus est RELU avant chaque trame — un canal peut donc
                // changer en cours d'exécution, ce qui est la définition d'un bus.
                rafraichir_bus_fichier(&bus, &opt.bus_fichier);
                let mut sortie = mdl.forward(0, f.pos as usize);
                bus.lock().unwrap().appliquer_gain(&mut sortie);
                // La RÉPONSE est encodée comme la demande : un pair qui parle en
                // listes reçoit des listes, sans second réglage à faire tenir
                // cohérent entre les deux machines.
                // C1b : si un successeur est déclaré, l'état calculé ici part chez
                // lui, et c'est SA réponse qui remonte à l'appelant.
                let a_rendre = match successeur.as_mut() {
                    None => sortie,
                    Some((sc, d, fi)) => {
                        if delai_relais > 0 {
                            std::thread::sleep(std::time::Duration::from_millis(delai_relais));
                        }
                        if envoyer_flux(sc, *d, *fi, f.pos, &sortie, f.mode, Some(&mdl)).is_err() {
                            println!("[relais] le successeur a fermé la connexion");
                            break;
                        }
                        match recevoir_flux(sc, hidden, hc_mult) {
                            Ok(r) => {
                                if r.mode != f.mode {
                                    println!("[relais] le successeur a répondu en mode {} au lieu \
de {} — flux refusé", r.mode, f.mode);
                                    break;
                                }
                                r.charge.en_dense(largeur_etat)
                            }
                            Err(e) => { println!("[relais] réponse du successeur illisible : {e}"); break; }
                        }
                    }
                };
                let mut a_rendre = a_rendre;
                if opt.pont_k > 0 { pont_sparsifier(&mut a_rendre, opt.pont_k); }
                // v8 : le compte de paires ACCOMPLIES par ce nœud voyage avec sa réponse.
                mdl.paires_flux = mdl.paires.iter().sum();
                trace.enregistrer_mode(&region_trace, f.pos as u32, "pair->local",
                                       &a_rendre, 0.0, f.mode);
                if envoyer_flux(&mut sock, f.debut, f.fin, f.pos, &a_rendre, f.mode,
                                Some(&mdl)).is_err() {
                    break;
                }
                servis += 1;
            }
            Err(e) => {
                // Un pair incompatible doit s'entendre dire POURQUOI : sans cela,
                // la session se termine sur « 0 flux servi » et rien d'autre.
                println!("[flux] arrêt : {e}");
                break;
            }
        }
    }
    match opt.pas_max {
        Some(b) if servis > b => println!("[horloge] borne de pas dépassée sur ce nœud : \
{servis} pas servis pour une borne de {b} — le nœud s'arrête"),
        Some(b) => println!("[horloge] {servis} pas servis (borne {b})"),
        None => println!("[horloge] {servis} pas servis"),
    }
    println!("[flux] {servis} flux servis");
    // Écrite APRÈS la boucle, donc aussi quand la session s'est mal terminée : une
    // trace qui n'existerait que pour les sessions réussies ne servirait à rien,
    // puisque ce sont les autres qu'on veut comprendre.
    trace_globale::ecrire_si_source(&trace, &opt.trace_globale, &region_trace);
}

/// C12bis : fusionne des traces écrites par plusieurs processus.
///
/// POURQUOI UN MODE À PART, ET PAS UN DRAPEAU DE PLUS SUR UNE EXÉCUTION. Fusionner
/// des traces ne calcule rien : c'est un travail de LECTURE, qui doit pouvoir se
/// faire après coup, sur une autre machine, sans le modèle ni les nœuds. Le mettre
/// derrière un mode existant aurait obligé à relancer une exécution pour relire ce
/// qu'on a déjà.
///
/// CE QUE LA FUSION REFUSE DE FAIRE, et c'est le cœur : ordonner des traces sans
/// horodatage (format v1), et présenter un lien comme vérifié quand son encodage
/// était avec perte. Dans les deux cas elle le DIT et sort en erreur plutôt que de
/// rendre un résultat qui aurait l'air d'un résultat.
fn run_fusion_traces(args: &[String]) {
    let mut fichiers: Vec<String> = Vec::new();
    let mut sortie: Option<String> = None;
    let mut i = 0;
    while i < args.len() {
        let a = &args[i];
        if a == "--fusion-sortie" {
            match args.get(i + 1) {
                Some(f) => { sortie = Some(f.clone()); i += 2; continue; }
                None => { eprintln!("--fusion-sortie attend un fichier"); std::process::exit(2); }
            }
        }
        if a.starts_with("--") {
            eprintln!("fusion : option inconnue « {a} » — rien n'a été fusionné");
            std::process::exit(2);
        }
        fichiers.push(a.clone());
        i += 1;
    }
    if fichiers.len() < 2 {
        eprintln!("fusion : il faut AU MOINS DEUX traces (reçu {}). En fusionner une seule \
n'apprend rien qu'elle ne dise déjà — et surtout, ce qui se vérifie ici, c'est que deux \
processus ont vu la MÊME chose.", fichiers.len());
        std::process::exit(2);
    }
    let mut entrees: Vec<(String, Vec<trace_globale::Croisement>)> = Vec::new();
    for f in &fichiers {
        match trace_globale::TraceGlobale::lire_avec_source(f) {
            Ok(e) => entrees.push(e),
            Err(e) => { eprintln!("{e}"); std::process::exit(2); }
        }
    }
    // Deux sources du même nom : la fusion serait ambiguë (on ne saurait plus de qui
    // vient une ligne). Les noms viennent de l'en-tête `# source`, donc d'une
    // décision — on la signale au lieu de la contourner.
    {
        let mut noms: Vec<&str> = entrees.iter().map(|(s, _)| s.as_str()).collect();
        noms.sort();
        let avant = noms.len();
        noms.dedup();
        if noms.len() != avant {
            eprintln!("fusion : deux traces portent la MÊME source — la fusion serait \
ambiguë (impossible de dire de quel processus vient une ligne). Donnez des noms distincts \
(le nœud prend son nom de région).");
            std::process::exit(2);
        }
    }
    let fusion = match trace_globale::fusionner(&entrees) {
        Ok(f) => f,
        Err(e) => { eprintln!("{e}"); std::process::exit(2); }
    };
    let derives = trace_globale::derive_horloges(&entrees);
    let constats = trace_globale::verifier_liens(&entrees);
    let identiques = constats.iter().filter(|c| matches!(c.verdict,
        trace_globale::VerdictLien::Identique)).count();
    let non_verif = constats.iter().filter(|c| matches!(c.verdict,
        trace_globale::VerdictLien::NonVerifiable { .. })).count();
    let divergents: Vec<&trace_globale::ConstatLien> = constats.iter().filter(|c| matches!(
        c.verdict, trace_globale::VerdictLien::Divergent { .. })).collect();
    println!("  fusion            : {} croisements de {} sources", fusion.len(), entrees.len());
    for (s, _) in entrees.iter() {
        let n = fusion.iter().filter(|x| &x.source == s).count();
        let (t0, t1) = fusion.iter().filter(|x| &x.source == s).fold(
            (f64::MAX, f64::MIN), |(a, b), x| (a.min(x.c.t_abs), b.max(x.c.t_abs)));
        if t0 <= t1 {
            println!("  {s:<17} : {n} croisements, de {:.3} à {:.3} (epoch)", t0, t1);
        } else {
            println!("  {s:<17} : {n} croisements");
        }
    }
    if derives.is_empty() {
        println!("  horloges          : une seule source horodatée — aucune dérive à mesurer");
    } else {
        for (s, d) in derives.iter() {
            println!("  dérive d'horloge  : {s} commence {d:+.6} s après la première source \
(mesurée, PAS corrigée : une fusion qui recolle des horloges sans le dire affirme plus \
qu'elle ne sait)");
        }
    }
    println!("  liens confrontés  : {identiques} identiques, {} divergents, {non_verif} non \
vérifiables (encodage avec perte)", divergents.len());
    for c in divergents.iter().take(10) { println!("  {}", c.ligne()); }
    if divergents.len() > 10 {
        println!("  … et {} autres divergences", divergents.len() - 10);
    }
    let mut non_verif_dits = 0;
    for c in constats.iter() {
        if matches!(c.verdict, trace_globale::VerdictLien::NonVerifiable { .. })
           && non_verif_dits < 5 {
            println!("  {}", c.ligne());
            non_verif_dits += 1;
        }
    }
    match &sortie {
        Some(f) => match trace_globale::ecrire_fusion(&fusion, f) {
            Ok(()) => println!("  trace fusionnée   : {} lignes écrites dans {f}", fusion.len()),
            Err(e) => { eprintln!("fusion : écriture de {f} impossible : {e}");
                        std::process::exit(2); }
        },
        None => {
            // Sans fichier de sortie, la fusion part sur la sortie standard, prête à
            // être redirigée : c'est ce qu'on veut pour diffuser ou archiver.
            for x in fusion.iter() {
                println!("{} {} {} {} {} {:#018x} {:.3} {:.6} {}", x.source, x.c.region, x.c.pas,
                         x.c.lien, x.c.n, x.c.empreinte, x.c.ms, x.c.t_abs, x.c.mode);
            }
        }
    }
    if !divergents.is_empty() {
        eprintln!("fusion : {} lien(s) DIVERGENT(S) — les deux bouts d'un même croisement ne \
portent pas la même empreinte. C'est exactement ce que cette fusion existe pour montrer.",
                  divergents.len());
        std::process::exit(3);
    }
    // SORTIR ICI, et pas « rendre la main » : la fusion est un mode complet, mais
    // elle ne passe pas par `analyser`, donc le programme continuait vers le chemin
    // du modèle — et mourait sur « ouverture du GGUF: No such file » APRÈS avoir
    // imprimé une fusion juste. Trouvé au premier essai de la porte.
    std::process::exit(0);
}

/// C11 (découverte) : le REGISTRE des régions — un fichier partagé qui donne
/// `region hote:port`, pour que les topologies ne codent plus les adresses en dur.
///
/// POURQUOI. Une topologie qui écrit `127.0.0.1:50001` décrit UN déploiement ; la même
/// topologie sur trois machines demande trois fichiers. Le plan (§3.2) prévoit un
/// registre statique puis dynamique ; voici le statique, et il tient en une fonction.
///
/// CE QUI EST RÉSOLU, ET CE QUI NE L'EST PAS : une `instance` qui contient déjà un `:`
/// est une adresse et n'est pas touchée (les topologies existantes continuent de marcher,
/// au caractère près) ; sinon elle est cherchée dans le registre, et une région ABSENTE
/// est refusée en la nommant — un repli silencieux sur `localhost` ferait parler le
/// moteur à la mauvaise machine.
fn resoudre_instance(instance: &str, registre: &Option<String>) -> String {
    if instance.contains(':') { return instance.to_string(); }
    let Some(f) = registre.as_ref() else {
        eprintln!("topologie : l'instance « {instance} » n'est pas une adresse (pas de « : ») \
et aucun --registre n'est donné — rien n'est résolu, et deviner l'adresse serait pire que \
de s'arrêter.");
        std::process::exit(2);
    };
    let texte = std::fs::read_to_string(f).unwrap_or_else(|e| {
        eprintln!("registre : lecture de {f} impossible : {e}"); std::process::exit(2) });
    for ligne in texte.lines() {
        let l = ligne.trim();
        if l.is_empty() || l.starts_with('#') { continue; }
        let mut ch = l.split_whitespace();
        let (nom, adresse) = (ch.next().unwrap_or(""), ch.next().unwrap_or(""));
        if nom == instance {
            if adresse.is_empty() || !adresse.contains(':') {
                eprintln!("registre : « {instance} » est déclarée sans adresse valide \
(« hote:port » attendu) dans {f}");
                std::process::exit(2);
            }
            return adresse.to_string();
        }
    }
    eprintln!("registre : la région « {instance} » est ABSENTE de {f}. Refusé : un repli \
silencieux ferait parler le moteur à la mauvaise machine.");
    std::process::exit(2);
}

/// C11 : la PANNE d'un lien, nommée. Ce que la politique déclarée décide, et ce
/// qu'elle ne décide PAS.
///
/// POURQUOI « best-effort » N'EST PAS « SAUTER LA RÉGION ». Le plan prévoyait de sauter
/// une région perdue et d'annoncer l'écart. Mais un modèle dont on saute douze couches ne
/// calcule pas une version approchée du même résultat : il calcule un AUTRE modèle, et
/// l'« écart » annoncé serait un écart entre deux choses différentes. La seule conduite
/// honnête est donc de S'ARRÊTER en disant tout : quel lien, quel pas, combien d'octets
/// avaient passé, et qu'aucun résultat ne sera rendu. C'est la même règle que C4 (borne de
/// pas), C9 (pont) et C10 (budget) — s'arrêter et le dire.
///
/// Le code de sortie est DISTINCT (7) : un script doit pouvoir distinguer « le pair est
/// mort » de « la borne de pas » (5) et de « le budget est dépassé » (6).
fn panne_de_lien(region: &str, pas: u64, octets: u64, quoi: &str) -> ! {
    eprintln!("[pannes] PANNE sur le lien local → {region} : {quoi}. L'exécution s'arrête au \
pas {pas} ({octets} octets échangés jusque-là). AUCUNE perplexité n'est rendue : elle \
porterait sur un modèle incomplet — un graphe amputé d'une région n'est pas une version \
approchée du même calcul, c'est un autre calcul. Politique déclarée : requis (défaut) ; \
voir docs/plan-cerveau-complet.md §3.2.");
    std::process::exit(7);
}

/// C9/C10 : le PONT à fibres limitées.
///
/// POURQUOI CE N'EST PAS QU'UN RÉGLAGE DE DÉBIT. Un lien entre deux régions — entre
/// deux hémisphères, ou entre deux machines — n'a pas une bande passante infinie. La
/// question n'est pas « peut-on compresser ? » mais **« combien de fibres faut-il
/// pour ne rien perdre ? »**, et elle se répond en mesurant : on garde les K plus
/// grandes amplitudes de l'état échangé, on jette le reste, et on regarde ce que la
/// perplexité en dit. Le résultat est une courbe qualité ↔ octets par pas, et une
/// courbe est ce qui permet de choisir.
///
/// CE QUE ÇA COÛTE : un tri partiel de la largeur de l'état (896 canaux) par pas, et
/// **rien** d'autre — le calcul des couches ne change pas, seule change la largeur de
/// ce qui traverse le lien. C'est la même économie que la parcimonie apprise du
/// moteur (paires = poids non nuls × activations vivantes), appliquée au lien au lieu
/// des poids.
fn pont_sparsifier(etat: &mut [f32], k: usize) {
    if k == 0 || k >= etat.len() { return; }
    let mut idx: Vec<u32> = (0..etat.len() as u32).collect();
    // Départage par l'indice : deux exécutions doivent garder les MÊMES canaux, sans
    // quoi la courbe mesurerait aussi le hasard du tri.
    idx.sort_by(|&x, &y| {
        let (a, b) = (etat[x as usize].abs(), etat[y as usize].abs());
        b.partial_cmp(&a).unwrap_or(std::cmp::Ordering::Equal).then(x.cmp(&y))
    });
    for &i in idx.iter().skip(k) { etat[i as usize] = 0.0; }
}

/// Le PILOTE : garde les premières couches, envoie le flux au nœud moteur,
/// reçoit l'état final, et note la perplexité — qu'on compare à celle du même
/// modèle calculé ENTIÈREMENT en local.
/// NLL d'un jeton : log-sum-exp des logits, moins le logit de la cible. Une
/// seule définition — elle était recopiée cinq fois dans ce fichier.
fn nll_logits(lg: &[f32], cible: u32) -> f64 {
    let mut mx = f32::NEG_INFINITY;
    for &v in lg { if v > mx { mx = v; } }
    let mut somme = 0f64;
    for &v in lg { somme += ((v - mx) as f64).exp(); }
    (mx as f64 + somme.ln()) - lg[cible as usize] as f64
}

/// Le nombre de couches d'un modèle, lu dans son EN-TÊTE seul — la topologie se
/// vérifie sans charger les poids (62 Go pour gpt-oss).
fn n_layer_total(chemin: &str) -> usize {
    let g = Gguf::open_auto(chemin).expect("ouverture du GGUF (en-tête)");
    g.cfg("block_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize
}

fn run_ppl_reparti(opt: Options, pair: &str) {
    use std::time::Instant;
    let chemin = modele_chemin();
    let ctx = if opt.ctx_impose { opt.ctx } else { 256 };
    let limite = opt.limit.max(1).min(ctx);
    // ---- C1 : la TOPOLOGIE, si elle est donnée, DIT la plage locale et le pair.
    // C'est la porte de non-régression du graphe : la chaîne décrite par le
    // fichier doit reproduire exactement ce que `--couches-locales` faisait.
    // Toute incohérence entre le fichier et la ligne de commande est REFUSÉE —
    // mesurer un découpage qui n'est pas celui qu'on croit serait pire que ne
    // rien mesurer.
    let (couches_locales, pair_cli, tp_debut, tp_fin, tp_region_distante) = if let Some(f) = opt.topologie.clone() {
        let texte = std::fs::read_to_string(&f).unwrap_or_else(|e| {
            eprintln!("topologie : lecture de {f} impossible : {e}"); std::process::exit(2) });
        let t = topologie::lire_json(&texte).unwrap_or_else(|e| {
            eprintln!("{e}"); std::process::exit(3) });
        t.valider().unwrap_or_else(|e| { eprintln!("{e}"); std::process::exit(3) });
        let locales: Vec<&topologie::Region> =
            t.regions.iter().filter(|r| r.instance == "local").collect();
        if locales.len() != 1 {
            eprintln!("topologie : le pilote exige exactement UNE région locale (trouvé {})",
                      locales.len());
            std::process::exit(3);
        }
        let l = locales[0];
        // Les régions DISTANTES sont maintenant une CHAÎNE : la première est le
        // pair direct, les suivantes sont atteintes par relais. On vérifie qu'elles
        // forment bien une suite contiguë qui reprend juste après la région locale
        // — un trou ici ferait sauter des couches en silence.
        let ordre = t.valider().unwrap_or_else(|e| { eprintln!("{e}"); std::process::exit(3) });
        let distantes: Vec<&topologie::Region> = ordre.iter()
            .filter_map(|id| t.region(id))
            .filter(|r| r.instance != "local").collect();
        if distantes.is_empty() {
            eprintln!("topologie : aucune région distante — rien à répartir");
            std::process::exit(3);
        }
        let d = distantes[0];
        let mut attendue = l.derniere + 1;
        for r in &distantes {
            if r.premiere != attendue {
                eprintln!("topologie : la chaîne distante n'est pas contiguë — « {} » commence à \
{} alors que la couche attendue est {attendue}", r.id, r.premiere);
                std::process::exit(3);
            }
            attendue = r.derniere + 1;
        }
        if attendue != n_layer_total(&chemin) {
            eprintln!("topologie : la chaîne s'arrête à la couche {} alors que le modèle en a {}",
                      attendue - 1, n_layer_total(&chemin));
            std::process::exit(3);
        }
        if distantes.len() > 1 {
            println!("[topologie] chaîne de {} régions distantes : la première est le pair direct, \
les autres seront atteintes par relais", distantes.len());
        }
        if l.premiere != 0 {
            eprintln!("topologie : la région locale doit commencer à la couche 0 (elle est {}..{}) \
— le pilote lit les jetons, il porte donc la première région", l.premiere, l.derniere);
            std::process::exit(3);
        }
        // La RÉSOLUTION PRÉCÈDE LE CONTRÔLE : sinon une topologie qui NOMME ses régions
        // (« d ») était refusée comme contradictoire avec `--ppl-reparti` (« hôte:port »),
        // alors que les deux disent la même chose — l'une par son nom, l'autre par son
        // adresse. Trouvé en écrivant la porte du registre, qui échouait en code 3.
        let instance_resolue = resoudre_instance(&d.instance, &opt.registre);
        if instance_resolue != pair {
            eprintln!("topologie : la première région distante est sur « {instance_resolue} » mais \
`--ppl-reparti` dit « {pair} » — deux sources pour la même chose, et elles se contredisent");
            std::process::exit(3);
        }
        println!("[topologie] chaîne vérifiée : local 0..{} → {} {}..{}",
                 l.derniere, instance_resolue, d.premiere, d.derniere);
        // C11 : l'instance peut être un NOM de région, résolu par le registre — une
        // topologie qui écrit « 127.0.0.1:50001 » décrit UN déploiement, et la même
        // topologie sur trois machines en demanderait trois.
        (l.couches(), instance_resolue, d.premiere, d.derniere, d.id.clone())
    } else {
        (if opt.couches_locales > 0 { opt.couches_locales } else { 12 }, pair.to_string(),
         0usize, 0usize, String::from("pair"))
    };
    let pair: &str = &pair_cli;
    let pair_region = tp_region_distante.clone();
    // La plage du pair : celle de la topologie s'il y en a une, sinon « tout ce
    // qui reste après les couches locales » — le comportement historique, intact.
    // Le nombre de couches vient de l'EN-TÊTE : à cet endroit le modèle n'est pas
    // encore chargé (et le charger pour compter des couches coûterait 62 Go sur
    // gpt-oss).
    let n_layer = n_layer_total(&chemin);
    // LA FIN DE PLAGE EST EXCLUSIVE : le nœud fait `couche_fin = f.fin` et exécute
    // `debut..fin`. Envoyer `derniere` au lieu de `derniere + 1` saute la dernière
    // couche de la région — et ça ne se voit QUE sur les modes non-lot, ce qui a
    // rendu le diagnostic pénible (modes 0, 1 et 2 cassés, 3 et 4 intacts).
    // ---- C3 : LES DÉLAIS PAR LIEN. La topologie les déclare ; le moteur les
    // APPLIQUE en retardant chaque trame de ce lien. L'invariant est net et c'est
    // la porte : un délai change le TEMPS, jamais le résultat — il ne doit pas
    // toucher un chiffre.
    let delai_ms: u64 = if let Some(f) = opt.topologie.clone() {
        std::fs::read_to_string(&f).ok()
            .and_then(|t| topologie::lire_json(&t).ok())
            .and_then(|t| t.lien_entre("local", &tp_region_distante).map(|l| l.delai_ms))
            .unwrap_or(0)
    } else { 0 };
    if delai_ms > 0 {
        println!("[delais] lien local → {} : +{} ms par trame · le résultat ne doit pas \
changer (seul le temps change) — c'est la porte de C3", tp_region_distante, delai_ms);
    }
    // C10 : le BUDGET du lien. Déclaré dans la topologie, il se compare à ce qui passe
    // réellement — la taille d'un flux dépend de l'activité, pas du mode (1 951 octets à
    // 97,7 % d'activité en listes par blocs, 1 096 à 50 %), donc un contrôle au démarrage
    // ne pourrait comparer qu'à une valeur nominale inventée.
    let budget_octets: Option<u64> = if let Some(f) = opt.topologie.clone() {
        std::fs::read_to_string(&f).ok()
            .and_then(|t| topologie::lire_json(&t).ok())
            .and_then(|t| t.lien_entre("local", &tp_region_distante).and_then(|l| l.budget_octets))
    } else { None };
    if let Some(b) = budget_octets {
        println!("[budget] lien local → {tp_region_distante} : {b} octets par pas AU PLUS \
(déclaré dans la topologie) — dépassement = arrêt, jamais un résultat partiel");
    }
    // C10 (suite) : le budget de LATENCE. La loi du dépôt est 3,4 ms par jeton et par ms
    // de RTT : un lien déclaré lent qui répond vite, ou l'inverse, n'est pas le lien qu'on
    // croit — et le savoir au premier pas vaut mieux qu'à la fin.
    let budget_ms: Option<u64> = if let Some(f) = opt.topologie.clone() {
        std::fs::read_to_string(&f).ok()
            .and_then(|t| topologie::lire_json(&t).ok())
            .and_then(|t| t.lien_entre("local", &tp_region_distante).and_then(|l| l.budget_ms))
    } else { None };
    // C10 (3e volet) : le budget de PAIRES du pair — bornable depuis le transport du compte
    // (protocole v8). C'est le coût qui compte dans ce moteur.
    let budget_paires: Option<u64> = if let Some(f) = opt.topologie.clone() {
        std::fs::read_to_string(&f).ok()
            .and_then(|t| topologie::lire_json(&t).ok())
            .and_then(|t| t.lien_entre("local", &tp_region_distante).and_then(|l| l.budget_paires))
    } else { None };
    if let Some(b) = budget_paires {
        println!("[budget] lien local → {tp_region_distante} : {b} paires par pas AU PLUS \
(compte annoncé par le nœud) — dépassement = arrêt, aucune perplexité");
    }
    if let Some(b) = budget_ms {
        println!("[budget] lien local → {tp_region_distante} : {b} ms par pas AU PLUS \
(allé-retour mesuré) — dépassement = arrêt");
    }
    // C4 : le compteur de pas de la région locale.
    let mut pas_servis: u64 = 0;
    // C5 : le BUS DE MODULATION. Un canal neutre ne change RIEN (c'est la porte),
    // un canal non neutre change la sortie — sans quoi le bus ne serait pas
    // branché. Chaque région décide de ce qu'elle en fait : ici, le gain.
    let bus0 = bus::Bus::analyser(&opt.bus).unwrap_or_else(|e| {
        eprintln!("{e}"); std::process::exit(2) });
    // C5ter : le pilote aussi a un bus, et il doit pouvoir être modulé à distance —
    // sans quoi une région locale ne serait réglable que par son propre fichier.
    let bus = std::sync::Arc::new(std::sync::Mutex::new(bus0));
    if let Some(p) = opt.bus_serveur { demarrer_bus_serveur(p, std::sync::Arc::clone(&bus)); }
    // Le verrou n'est pris QUE pour lire l'état initial, jamais gardé : le garder
    // pendant l'exécution bloquerait définitivement le fil d'écoute réseau — le bus
    // ne serait modulable qu'avant le premier pas, c'est-à-dire pas modulable.
    {
        let b = bus.lock().unwrap();
        if !b.est_neutre() {
            println!("[bus] canaux actifs : {} · gain de région appliqué à la région locale",
                     b.canaux().iter().map(|(k, v)| format!("{k}={v}")).collect::<Vec<_>>().join(" "));
        }
    }
    // C12 : la trace globale — créée ici, écrite (ou vérifiée) à la fin.
    let mut trace = trace_globale::TraceGlobale::nouvelle();
    let (debut_pair, fin_pair) = if tp_fin > 0 {
        (tp_debut, tp_fin + 1)
    } else {
        (couches_locales, n_layer)
    };
    // `--lot T` : préremplissage par LOTS sur le fil. La référence locale est
    // alors calculée avec le MÊME découpage — sinon l'écart mesurerait la
    // différence entre deux ordres de sommation, pas celle du découpage.
    let lot = opt.lot.max(1);
    let mut mdl = model::Model::load(&chemin,
                                     ctx, fils(&opt), true, opt.keep, false, 0, 0);
    appliquer_quantification(&mut mdl, &opt);

    // C2/E4 : le gain de la FFN. Il était câblé dans `run_infer` et `run_ppl`, et PAS ici :
    // dans le chemin RÉPARTI, `--ffn-gain` ne faisait donc RIEN, en silence — mesuré :
    // 42,5477 avec et sans le drapeau. C'est la famille de défauts que ce dépôt traque (un
    // drapeau qui ne fait rien), et celui-ci comptait double : le sprint porte sur la
    // distribution, où le réglage fin doit survivre.
    // v7 : le refus qui suivait ici a été RETIRÉ — les trois réglages voyagent maintenant
    // dans la trame, donc le pilote ET le nœud appliquent la même fenêtre.
    // LES TROIS CHAMPS QUE LE v7 TRANSPORTE, ENFIN APPLIQUÉS PAR LE PILOTE.
    //
    // Le round 28 concluait « les deux moitiés appliquent la même fenêtre » sur la foi de deux
    // nombres égaux (18,5520 = 18,5520). C'était faux, et la vérification tenait en une ligne :
    // ces trois champs n'étaient assignés NULLE PART ici. Le v7 les faisait voyager jusqu'au nœud,
    // mais le pilote gardait ses défauts — le réglage était INERTE DES DEUX CÔTÉS, et c'est pour
    // cela que les deux nombres s'accordaient.
    //
    // LEÇON, écrite là où elle servira : deux nombres égaux ne prouvent pas qu'ils mesurent la
    // même chose. Avant de conclure à un accord, vérifier POURQUOI ils sont égaux.
    mdl.attn_window = opt.attn_window;
    mdl.swa_pattern = opt.swa_pattern.unwrap_or(0);
    // même règle qu'ailleurs : `0` doit pouvoir ÉTEINDRE (cf. `attn_sinks_impose`)
    if opt.attn_sinks_impose { mdl.attn_sinks = opt.attn_sinks; }
    avertir_puits_inertes(&mdl, opt.attn_sinks_impose);
    if opt.attn_window > 0 || opt.swa_pattern.is_some() || opt.attn_sinks > 0 {
        println!("[attention] fenêtre {} · motif {} · puits {} — appliqués aux couches LOCALES et \
TRANSPORTÉS au nœud (protocole v7) : les deux moitiés calculent le même modèle",
                 opt.attn_window, opt.swa_pattern.unwrap_or(0), opt.attn_sinks);
    }
    if let Some(gs) = opt.ffn_gain.clone() {
        let liste: Vec<String> = gs.iter().map(|(l, g)| format!("couche {l} × {g}")).collect();
        println!("gain FFN : {}", liste.join(" · "));
        mdl.ffn_gain = Some(gs);
    }
    // Le `hc` du PILOTE : c'est SON modèle qui décide de la largeur du pré-mix
    // qu'il envoie et de celle de celui qu'il reçoit (le pair valide le sien).
    let hc_pilote = mdl.hc.as_ref().map(|v| v[0].0.hc).unwrap_or(1);
    // `--tete-partielle` n'a pas d'objet ici : la « plage » de ce mode est le
    // découpage entre les DEUX nœuds, et le modèle local est le modèle entier.
    // Le taire serait exactement le défaut que `--options-actives` combat.
    if opt.tete_partielle {
        eprintln!("[plage] `--tete-partielle` est sans effet en `--ppl-reparti` : la plage \
y est le découpage entre nœuds (voir `--couches-locales`), pas un `--couches a:b`");
    }
    if opt.options_actives { options_actives(&mdl, "pilote du flux", opt.ctx_impose, true, opt.keep, opt.attn_sinks_impose); }
    let mode = if opt.flux_blocs { MODE_BLOCS }
               else if opt.flux_liste { MODE_LISTE }
               else { MODE_DENSE };
    // Le mode des LOTS est distinct : `--flux-blocs` donne le mode 4 (lot en
    // listes), tout le reste donne le mode 3 (lot dense f32). Déclaré ici pour
    // que l'affichage du transport, plus bas, le connaisse.
    // Un modèle à **hyper-connexions** transporte son état en `hc` copies
    // (16 384 canaux pour V4-Flash au lieu de 4 096) : le protocole accepte les
    // deux largeurs depuis que le nœud distant les valide contre SON modèle, et
    // le nœud qui possède la tête fait la réduction une seule fois
    // (`norme_finale`). Ce que ça coûte est mesuré plus bas, pas supposé.
    let mode_lot = if mode == MODE_BLOCS { MODE_LOT_LISTES } else { MODE_LOT };
    println!("[flux] quantification : {} niveaux, seuil {}, top-k {}, renorm {}",
             mdl.act_levels, mdl.act_thresh, mdl.act_topk, mdl.act_renorm);
    let n_layer = mdl.cfg.n_layer;
    // Les jetons viennent de `--ids`, SINON de `--ids-file`. Le fichier était
    // ignoré ici : le mode réparti retombait sur des jetons synthétiques et
    // mesurait donc un AUTRE texte que la référence, sans le dire — un écart de
    // perplexité de 3,7× attribué au découpage alors que le découpage était
    // exact à 0,00e0.
    let mut ids: Vec<u32> = if !opt.ids.is_empty() {
        opt.ids.clone()
    } else if let Some(f) = opt.ids_file.as_deref().filter(|f| !f.is_empty()) {
        let raw = std::fs::read_to_string(f).expect("fichier d'identifiants illisible");
        raw.split(|c: char| c == ',' || c.is_whitespace())
            .filter(|s| !s.is_empty())
            .filter_map(|s| s.parse().ok())
            .collect()
    } else {
        // Jetons synthétiques : ils doivent RESTER dans le vocabulaire. Une suite
        // `1..=limite` en sort dès que `limite > vocab` (modèle à 256 entrées,
        // limite 256) et fait paniquer l'indexation des logits — panique qui
        // accuse le modèle alors que c'est l'appelant.
        let vocab = mdl.cfg.vocab.max(1);
        (1..=limite).map(|i| (i % vocab) as u32).collect()
    };
    if ids.len() > limite {
        println!("[flux] {} jetons fournis > limite {} (ctx {}) : troncature aux {} derniers",
                 ids.len(), limite, ctx, limite);
        ids = ids[ids.len() - limite..].to_vec();
    }
    if ids.len() < 2 {
        // La perplexité est une moyenne sur `len - 1` jetons notés : avec un seul
        // jeton elle vaut NaN, et un NaN affiché comme un résultat ne dit rien.
        println!("[flux] il faut au moins DEUX jetons pour noter une perplexité \
(le premier ne prédit rien) — reçu {}. Rien n'a été calculé.", ids.len());
        return;
    }
    println!("[flux] pilote : {couches_locales} couches en local, {} chez le pair, {} jetons",
             n_layer - couches_locales, ids.len());

    // 1. référence locale, tout le modèle (même découpage que le chemin réparti)
    let t0 = Instant::now();
    let mut nll_ref = 0f64;
    if lot > 1 {
        let mut pos = 0usize;
        while pos < ids.len() {
            let t = lot.min(ids.len() - pos);
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
    // C11 : un pair ABSENT est une PANNE, pas une panique. Le pilote avait déjà calculé
    // sa référence locale (10 s sur 256 jetons) avant d'essayer de se connecter : un
    // `expect` ici faisait tomber le processus sur un code 134 illisible, alors que la
    // conduite utile est de nommer le lien et de ne rien rendre.
    let mut sock = match std::net::TcpStream::connect(pair) {
        Ok(s) => s,
        Err(e) => {
            eprintln!("[pannes] PANNE : le pair local → {pair} est INJOIGNABLE ({e}). Aucune \
perplexité n'est rendue — un graphe amputé d'une région n'est pas une version approchée du \
même calcul. Vérifiez que le nœud écoute (--flux-serveur {pair}).");
            std::process::exit(7);
        }
    };
    sock.set_nodelay(true).expect("TCP_NODELAY");   // cf. le nœud moteur : Nagle coûte 6×
    mdl.couche_fin = couches_locales;
    let mut octets_envoyes = 0u64;
    let mut octets_recus = 0u64;
    let mut actifs_envoyes = 0u64;
    let mut flux_envoyes = 0u64;
    let mut jetons_envoyes = 0u64;   // Σt, pas `lot` : le dernier lot est partiel
    let mut t_local = 0f64;
    let mut t_pair = 0f64;
    let t1 = Instant::now();
    let mut nll = 0f64;
    if lot > 1 {
        // PRÉREMPLISSAGE RÉPARTI : un lot par aller-retour au lieu d'un flux par
        // jeton. C'est ce que la phase 3.4 doit démontrer — le découpage doit
        // coûter la latence d'UN message par lot, pas par jeton.
        if mode == MODE_LISTE {
            eprintln!("[flux] --flux-liste ne s'applique pas aux lots (seul --flux-blocs a un \
mode de lot, le 4) : le lot part en f32 dense. À --lot 1, le mode choisi s'applique.");
        }
        let mut pos = 0usize;
        while pos + 1 < ids.len() {
            let t = lot.min(ids.len() - pos);
            let horloge = Instant::now();
            let hs = mdl.forward_lot(&ids[pos..pos + t], pos);
            let plat: Vec<f32> = hs.concat();
            t_local += horloge.elapsed().as_secs_f64();
            let horloge = Instant::now();
            let o = match (if mode_lot == MODE_LOT_LISTES {
                envoyer_lot_listes(&mut sock, couches_locales as u32, n_layer as u32,
                                   pos as u32, &plat, t, &mdl)
            } else {
                envoyer_lot(&mut sock, couches_locales as u32, n_layer as u32,
                            pos as u32, &plat, t, &mdl)
            }) {
                            Ok(o) => o,
                            Err(e) => {
                                eprintln!("[flux] le nœud moteur a fermé la connexion \
pendant l'envoi du lot ({e}) — version, réglages ou contexte : il a dit pourquoi \
de son côté.");
                                std::process::exit(1);
                            }
                        };
            if let Some(b) = budget_octets {
                if o as u64 > b {
                    eprintln!("[budget] DÉPASSEMENT sur le lien local → {tp_region_distante} : \
{o} octets pour un budget de {b} — l'exécution s'arrête ICI, au pas {pos}. Aucune \
perplexité n'est rendue : elle porterait sur un transport qui n'est pas celui qui a été \
déclaré.");
                    std::process::exit(6);
                }
            }
            octets_envoyes += o as u64;
            actifs_envoyes += (t * mdl.cfg.hidden) as u64;
            jetons_envoyes += t as u64;
            flux_envoyes += 1;
            let rep = match recevoir_flux(&mut sock, mdl.cfg.hidden, hc_pilote) {
                Ok(r) => r,
                Err(e) => {
                    eprintln!("[flux] le nœud moteur a fermé la connexion ({e}).\
\n       Cause la plus probable : il a REFUSÉ le lot (son contexte est plus petit \
que --ctx ici : {ctx}). Il l'a dit de son côté.");
                    std::process::exit(1);
                }
            };
            t_pair += horloge.elapsed().as_secs_f64();
            octets_recus += TAILLE_TETE as u64 + rep.octets_corps as u64;
            // Un pair hostile tue le client avec 83 octets si l'on ne vérifie pas
            // ce qu'il répond : mode différent, ou nombre d'états différent. Le
            // profil release est en `panic = "abort"`, donc une assertion est un
            // SIGABRT — on préfère un message et une sortie propre.
            if rep.mode != mode_lot {
                eprintln!("[flux] le nœud moteur a répondu en mode {} alors que la \
demande était en mode {mode_lot} — pair incompatible ? Rien n'a été calculé.",
                          rep.mode);
                std::process::exit(1);
            }
            if rep.n != t {
                eprintln!("[flux] le nœud moteur a répondu {} états pour un lot de {t} \
— pair incohérent. Rien n'a été calculé.", rep.n);
                std::process::exit(1);
            }
            // **Le chemin des LOTS ne sait pas appliquer la `pre` reçue** : il
            // réduit chaque état par `norme_finale` sur un état de largeur
            // `hidden` — où la réduction de V4.1 n'a pas de sens — et n'affecte
            // jamais `hc_porte_imposee` depuis la réponse. Aujourd'hui
            // inatteignable (`forward_lot` refuse les modèles à hyper-connexions
            // au-delà d'un jeton, et eux seuls portent une `pre`), mais un pair
            // qui en enverrait une serait ignoré en silence : c'est le défaut
            // qu'on vient de corriger, en voici la porte. Relevé par la relecture
            // adverse.
            if !rep.premix.is_empty() {
                eprintln!("[flux] le nœud moteur a renvoyé une `pre` portée (v6) sur un LOT \
de {t} états : ce chemin ne sait pas l'appliquer (la réduction finale y est par état, et \
un lot de plus d'un état n'a pas UNE `pre`). Rien n'a été calculé.");
                std::process::exit(1);
            }
            let etats = rep.charge.plat().to_vec();
            assert_eq!(etats.len(), t * mdl.cfg.hidden,
                       "lot reçu de {} valeurs pour {t} jetons de {} canaux",
                       etats.len(), mdl.cfg.hidden);
            // La norme finale reste au nœud qui a la tête, et la tête se fait par
            // lots : le lot reçu ne redescend pas jeton par jeton.
            let mut hn: Vec<Vec<f32>> = Vec::with_capacity(t);
            for i in 0..t {
                hn.push(mdl.norme_finale(&etats[i * mdl.cfg.hidden..(i + 1) * mdl.cfg.hidden],
                                         pos + i));
            }
            let lgs = mdl.logits_lot(&hn);
            for i in 0..t {
                if pos + i + 1 < ids.len() {
                    nll += nll_logits(&lgs[i], ids[pos + i + 1]);
                }
            }
            pos += t;
        }
    } else {
    for (pos, &t) in ids.iter().enumerate() {
        let dernier = pos + 1 == ids.len();
        // Le DERNIER jeton n'a rien à prédire : lui demander un aller-retour
        // distant, c'est payer un calcul complet — des deux côtés — pour un état
        // que personne ne lit. On sort donc ici, AVANT le calcul local aussi.
        // La référence locale, elle, calcule encore ce dernier jeton pour rien
        // (1 sur N : négligeable, mais écrit ici pour que personne ne s'étonne
        // d'un écart de temps entre les deux chemins).
        if dernier { break; }
        let horloge = Instant::now();
        let etat = mdl.forward(t, pos);
        t_local += horloge.elapsed().as_secs_f64();
        let horloge = Instant::now();
        // C1b : la plage confiée au pair est celle de SA région (la première
        // région distante), pas « tout ce qui reste » : avec un relais, « ce qui
        // reste » appartient à plusieurs nœuds, et le premier calculerait le
        // travail des autres.
        // Le gain de région s'applique à l'état que la région PRODUIT (C5).
        let mut etat = etat;
        // C5ter : le réglage peut arriver PAR LE RÉSEAU à tout moment, donc le bus
        // est relu à chaque pas — c'est ce qui fait d'un bus un bus, et non un
        // réglage de démarrage. Le verrou n'est tenu que le temps d'un pas.
        rafraichir_bus_fichier(&bus, &opt.bus_fichier);
        bus.lock().unwrap().appliquer_gain(&mut etat);
        // C9/C10 : le pont. Appliqué APRÈS le bus (la modulation est locale au
        // processus) et AVANT la trace, pour que la trace enregistre ce qui a
        // réellement traversé le lien — une trace qui montrerait l'état d'avant le
        // pont ne servirait à rien pour comprendre une divergence de lien.
        if opt.pont_k > 0 { pont_sparsifier(&mut etat, opt.pont_k); }
        trace.enregistrer("local", pos as u32, "local->pair", &etat, 0.0);
        if delai_ms > 0 {
            std::thread::sleep(std::time::Duration::from_millis(delai_ms));
        }
        // C4 : la borne de PAS. Une région qui dépasse sa borne s'arrête et le dit ;
        // elle ne rend pas un résultat partiel qui aurait l'air d'un résultat.
        pas_servis += 1;
        if let Some(b) = opt.pas_max {
            if pas_servis > b {
                eprintln!("[horloge] borne de pas atteinte : {b} pas (région locale). \
L'exécution s'arrête ICI — aucune perplexité n'est rendue, parce qu'elle porterait sur \
{} jetons seulement.", pas_servis - 1);
                std::process::exit(5);
            }
        }
        let (o, a) = envoyer_flux(&mut sock, debut_pair as u32, fin_pair as u32,
                                  pos as u32, &etat, mode, Some(&mdl))
                        .unwrap_or_else(|e| {
                            let _ = e;
                            panne_de_lien(&pair_region, pas_servis, octets_envoyes,
                                          "le pair a fermé pendant l'envoi du flux");
                        });
        if let Some(b) = budget_octets {
            if o as u64 > b {
                eprintln!("[budget] DÉPASSEMENT sur le lien local → {tp_region_distante} : \
{o} octets pour un budget de {b} — l'exécution s'arrête ICI, au pas {pos}. Aucune \
perplexité n'est rendue : elle porterait sur un transport qui n'est pas celui qui a été \
déclaré.");
                std::process::exit(6);
            }
        }
        octets_envoyes += o as u64;
        actifs_envoyes += a as u64;
        flux_envoyes += 1;
        let rep = match recevoir_flux(&mut sock, mdl.cfg.hidden, hc_pilote) {
            Ok(r) => r,
            Err(e) => {
                let _ = e;
                panne_de_lien(&pair_region, pas_servis, octets_envoyes,
                              "le pair a fermé avant de rendre son état (version du \
protocole, réglages ou contexte — il a dit pourquoi de son côté)");
            }
        };
        // Ce que coûte le découpage : le calcul local, et l'attente du pair
        // (son calcul + l'aller-retour réseau) — la latence, pas le débit.
        // LE CONTRÔLE EST ICI, DANS LA BOUCLE — et c'est la leçon du round précédent : placé
        // après elle, il laissait CALCULER ET AFFICHER la perplexité avant de refuser, soit
        // exactement le résultat partiel que ce dépôt refuse. La porte l'a dit avant moi.
        // Le compte du nœud est cumulatif : le plafond après k pas vaut k × le budget.
        if let Some(b) = budget_paires {
            let pp = PAIRES_DU_PAIR.load(std::sync::atomic::Ordering::Relaxed);
            let plafond = b.saturating_mul(pas_servis.max(1));
            if pp > plafond {
                eprintln!("[budget] PAIRES DÉPASSÉES sur le lien local → {tp_region_distante} : \
{pp} paires annoncées par le pair pour un budget de {b} par pas sur {pas_servis} pas (plafond \
{plafond}) — l'exécution s'arrête ICI, au pas {pos}. Aucune perplexité n'est rendue.");
                std::process::exit(9);
            }
        }
        let ms_pas = horloge.elapsed().as_secs_f64() * 1e3;
        t_pair += horloge.elapsed().as_secs_f64();
        if let Some(b) = budget_ms {
            if ms_pas > b as f64 {
                eprintln!("[budget] LATENCE DÉPASSÉE sur le lien local → {tp_region_distante} : \
{ms_pas:.1} ms pour un budget de {b} ms, au pas {pos}. L'exécution s'arrête ICI — une \
perplexité calculée sur un lien plus lent que celui qui a été déclaré ne serait pas le \
résultat annoncé.");
                std::process::exit(8);
            }
        }
        octets_recus += TAILLE_TETE as u64 + rep.octets_corps as u64;
        // Une réponse de pair hostile ne doit ni tuer le client ni être prise
        // pour un résultat : hors lot, elle n'était pas vérifiée du tout — un
        // vecteur de 895 canaux passait en silence et affichait une perplexité de
        // 2,76e8 comme si c'en était une (relecture adversariale).
        if rep.mode != mode {
            eprintln!("[flux] le nœud moteur a répondu en mode {} alors que la demande \
était en mode {mode} — pair incompatible ? Rien n'a été calculé.", rep.mode);
            std::process::exit(1);
        }
        // Le pair rend l'état BRUT de SA dernière couche : `cachés` canaux, ou
        // `hc × cachés` pour un modèle à hyper-connexions (c'est `norme_finale`
        // qui réduit, une seule fois, sur le nœud qui possède la tête).
        let hc_mult = mdl.hc.as_ref().map(|v| v[0].0.hc).unwrap_or(1);
        let largeur_etat = mdl.cfg.hidden * hc_mult;
        if rep.mode == MODE_DENSE && rep.n != mdl.cfg.hidden && rep.n != largeur_etat {
            eprintln!("[flux] le nœud moteur a renvoyé {} canaux pour {} (ou {}) \
attendus — pair incohérent. Rien n'a été calculé.", rep.n, mdl.cfg.hidden, largeur_etat);
            std::process::exit(1);
        }
        let mut final_ = rep.charge.en_dense(largeur_etat);
        // Le pont est le MÊME dans les deux sens : un corps calleux n'est pas
        // asymétrique par construction, et utiliser deux largeurs différentes
        // demanderait de dire laquelle est laquelle — ce qu'aucune mesure ne
        // justifierait aujourd'hui.
        if opt.pont_k > 0 { pont_sparsifier(&mut final_, opt.pont_k); }
        trace.enregistrer(&pair_region, pos as u32, "pair->local", &final_, t_pair * 1e3);
        // La réponse porte la `pre` de la DERNIÈRE FFN du pair (v6) : c'est elle
        // que la réduction finale du pilote doit employer — il ne peut pas la
        // recalculer, il n'a pas exécuté ces couches.
        mdl.hc_porte_imposee = if rep.premix.is_empty() { None } else { Some(rep.premix.clone()) };
        if pos + 1 < ids.len() {
            // Deux temps : la réduction CONSOMME la `pre` reçue (V4.1), donc elle
            // emprunte le modèle en écriture, et la tête le reprend ensuite. Les
            // imbriquer ne compilerait pas — et c'est tant mieux : l'ordre
            // (réduire, puis noter) reste ainsi visible.
            let reduit = mdl.norme_finale(&final_, pos);
            nll += nll_logits(&mdl.logits(&reduit), ids[pos + 1]);
        }
    }
    }
    let ppl = (nll / (ids.len() - 1) as f64).exp();
    // Largeur de l'état échangé : elle sert au rapport du pont (et à lui seul).
    let largeur_etat_max = mdl.cfg.hidden
        * mdl.hc.as_ref().map(|v| v[0].0.hc).unwrap_or(1);
    println!("  deux nœuds        : perplexité {ppl:.4}  ({:.1} s)", t1.elapsed().as_secs_f64());
    // v8 : ce que le PAIR a calculé, annoncé par lui — la première fois que le pilote sait ce
    // que coûte la moitié distante, au lieu de le déduire de son propre travail.
    let paires_pair = PAIRES_DU_PAIR.load(std::sync::atomic::Ordering::Relaxed);
    if paires_pair > 0 {
        let par_pas = paires_pair as f64 / pas_servis.max(1) as f64;
        println!("  paires du pair    : {paires_pair} au total, {:.1} M par pas (annoncées par le \
nœud dans chaque trame — protocole v8)", par_pas / 1e6);
    }
    if opt.pont_k > 0 {
        let octets = opt.pont_k * 4;
        println!("  pont              : {} fibres sur {largeur_etat_max} canaux gardées par pas ⇒ \
{octets} octets par sens et par pas, {octets} octets de plus par pas dans l'autre sens \
(dense f32 ; les modes 1 et 2 encodent autrement, et leur qualité est mesurée à part)",
                 opt.pont_k.min(largeur_etat_max));
    }
    // C12 : la trace est écrite, ou vérifiée par rejeu. La vérification compare
    // les empreintes AU BIT PRÈS : toute divergence est nommée avec son pas et
    // son lien, et le processus sort en erreur.
    if let Some(f) = opt.verifier_globale.clone() {
        match trace_globale::TraceGlobale::lire(&f) {
            Ok(reference) => match trace_globale::TraceGlobale::verifier(&reference, &trace.lignes_pub()) {
                Ok(n) => println!("  rejeu global      : {n} croisements, AUCUNE divergence ✅"),
                Err(e) => { eprintln!("  {e}"); std::process::exit(4); }
            },
            Err(e) => { eprintln!("  {e}"); std::process::exit(3); }
        }
    } else {
        trace_globale::ecrire_si(&trace, &opt.trace_globale);
    }
    println!("  horloge           : région locale {} pas servis{}", pas_servis,
             match opt.pas_max { Some(b) => format!(" (borne {b})"), None => String::new() });
    println!("  écart             : {:.2e}", (ppl - ppl_ref).abs() / ppl_ref);
    // Divisor : le nombre de flux RÉELLEMENT envoyés (un par jeton, le dernier
    // compris) et non le nombre de jetons NOTÉS — l'erreur d'un facteur 40/39
    // faisait apparaître un flux de « 919 canaux » pour un modèle qui en a 896.
    let nflux = flux_envoyes.max(1);
    if lot > 1 {
        // « par jeton » divise par les jetons RÉELLEMENT envoyés (Σt) : le dernier
        // lot est presque toujours partiel, et diviser par `lot` sous-estimait le
        // coût (0,9 ko annoncés contre 1,45 réels à 20 jetons en lots de 16).
        println!("  transport         : {} · lots de {lot} jetons au plus · {:.0} octets \
                  par lot (aller) · {:.1} ko par jeton · {} lots pour {} jetons",
                 if mode_lot == MODE_LOT_LISTES { "lot en LISTES" } else { "lot dense f32" },
                 octets_envoyes as f64 / nflux as f64,
                 octets_envoyes as f64 / jetons_envoyes.max(1) as f64 / 1024.0,
                 nflux, jetons_envoyes);
        println!("  temps             : {:.1} ms par LOT en local · {:.1} ms à attendre le pair · \
                  soit {:.2}× le calcul local seul",
                 1000.0 * t_local / nflux as f64, 1000.0 * t_pair / nflux as f64,
                 t_pair / t_local.max(1e-9));
    } else {
    println!("  transport         : {} · {:.0} octets par flux (aller) · {:.0} au retour · \
              {:.1} % d'activité ({:.0} neurones par flux) · {} flux",
             match mode { MODE_BLOCS => "listes à échelle par bloc (2 octets/actif, écarts)",
                          MODE_LISTE => "listes quantifiées",
                          _ => "dense f32" },
             octets_envoyes as f64 / nflux as f64, octets_recus as f64 / nflux as f64,
             100.0 * actifs_envoyes as f64 / (nflux as f64 * mdl.cfg.hidden as f64),
             actifs_envoyes as f64 / nflux as f64, nflux);
    println!("  temps             : {:.1} ms par jeton en local · {:.1} ms à attendre le pair \
              (son calcul + l'aller-retour) · soit {:.2}× le calcul local seul",
             1000.0 * t_local / nflux as f64, 1000.0 * t_pair / nflux as f64,
             t_pair / t_local.max(1e-9));
    }
}

/// Banc **des scores d'attention** (`--banc-topk N`) : le premier des trois noyaux
/// du plan `docs/plan-gpu-topk.md`. Il compare les scores calculés en VRAM à la
/// référence CPU — même clé, même requête, même échelle — et chronomètre les deux.
///
/// C'est le banc qui doit dire **1e-6** avant qu'on écrive la sélection : sans lui,
/// le noyau 2 s'appuierait sur des scores qu'on n'a jamais relus.
fn run_banc_topk(opt: Options) {
    use std::time::Instant;
    let path = &modele_chemin();
    let g = Gguf::open_auto(path).expect("ouverture du GGUF");
    let n_kv = g.cfg("attention.head_count_kv").and_then(|m| m.as_u64()).unwrap_or(1) as usize;
    let n_head = g.cfg("attention.head_count").and_then(|m| m.as_u64()).unwrap_or(1) as usize;
    let hd = g.cfg("attention.key_length").and_then(|m| m.as_u64()).unwrap_or(64) as usize;
    let bits = std::env::var("DRAVE_KV_BITS").ok().and_then(|v| v.parse().ok()).unwrap_or(8u32);
    let n = opt.banc_topk;
    let rep = (n_head / n_kv.max(1)).max(1);
    let scale = 1.0 / (hd as f32).sqrt();
    println!("banc top-k : {n} clés · {n_kv} têtes KV × {hd} dim · {rep} têtes de requête \
par tête KV · KV {bits} bits");

    // Un cache KV rempli de valeurs déterministes, puis son miroir VRAM.
    let mut cache = model::KvCache::new(bits, n_kv, n, hd);
    let mut etat = 987654321u64;
    let mut suivant = move || {
        etat ^= etat << 13; etat ^= etat >> 7; etat ^= etat << 17;
        ((etat >> 11) as f64 / (1u64 << 53) as f64) as f32 * 2.0 - 1.0
    };
    // Une clé PROPRE à chaque position. La version d'avant réutilisait le même
    // vecteur partout : tous les scores d'une ligne étaient alors EXACTEMENT
    // égaux, l'histogramme n'avait qu'un seul seau non vide et la descente radix
    // n'était jamais exercée — le banc aurait validé un cas dégénéré en ayant
    // l'air de valider la sélection. Trouvé en relisant le banc, pas en le
    // faisant échouer.
    for pos in 0..n {
        for kvh in 0..n_kv {
            let kp: Vec<f32> = (0..n_kv * hd).map(|_| suivant()).collect();
            let vp: Vec<f32> = (0..n_kv * hd).map(|_| suivant()).collect();
            cache.ecrire(kvh, pos, &kp, &vp);
        }
    }
    let machine = match crate::gpu::machines().first() {
        Some(m) => m,
        None => { println!("GPU absent : banc terminé"); return; }
    };
    let mut miroir = match machine.kv_allouer(n_kv, n, hd, bits) {
        Some(m) => m,
        None => { println!("allocation VRAM impossible : banc terminé"); return; }
    };
    for kvh in 0..n_kv {
        for pos in 0..n {
            cache.vers_gpu(machine, &mut miroir, kvh, pos);
        }
    }
    // La requête : `rep` têtes, déterministes elles aussi.
    let q: Vec<f32> = (0..n_kv * rep * hd).map(|_| suivant() * 0.5).collect();

    // Référence CPU : un produit scalaire par (tête KV, tête de requête, clé).
    let mut attendu = vec![0f32; n_kv * rep * n];
    let t0 = Instant::now();
    let mut kd = vec![0f32; hd];
    for kvh in 0..n_kv {
        for t in 0..n {
            cache.cle(kvh, t, &mut kd);
            for r in 0..rep {
                let qh = &q[(kvh * rep + r) * hd..(kvh * rep + r + 1) * hd];
                let mut s = 0f32;
                for i in 0..hd { s += qh[i] * kd[i]; }
                attendu[(kvh * rep + r) * n + t] = s * scale;
            }
        }
    }
    let t_cpu = t0.elapsed().as_secs_f64();

    let mut obtenu = vec![0f32; n_kv * rep * n];
    let t1 = Instant::now();
    if !machine.attn_scores(&mut miroir, &q, n, scale, &mut obtenu) {
        println!("le noyau a refusé la configuration");
        return;
    }
    let t_gpu = t1.elapsed().as_secs_f64();

    let mut mx = 0f32;
    let mut dyn_ = 0f32;
    for (a, b) in attendu.iter().zip(obtenu.iter()) {
        mx = mx.max((a - b).abs());
        dyn_ = dyn_.max(a.abs());
    }
    println!("  CPU  {} fils : {:8.2} ms", fils(&opt), t_cpu * 1e3);
    println!("  GPU  scores  : {:8.2} ms  ({:.1}× plus rapide)", t_gpu * 1e3,
             t_cpu / t_gpu.max(1e-9));
    println!("  écart max {mx:.3e} sur une dynamique de {dyn_:.3e} (relatif {:.2e})",
             mx / dyn_.max(1e-9));
    if mx / dyn_.max(1e-9) < 1e-6 {
        println!("  → conforme au critère du plan (1e-6) : la sélection peut s'appuyer dessus");
    } else {
        println!("  → AU-DESSUS du critère du plan (1e-6) : ne pas écrire la sélection avant \
d'avoir compris");
    }

    // ------------------------------------------- noyau 2a : le seuil du top-k
    // La sélection est un radix select : quatre passes de 8 bits sur les scores
    // transformés en entiers monotones. Ici on ne collecte pas encore les
    // indices — on vérifie que la descente HÔTE trouve, ligne par ligne, le
    // k-ième score EXACT et le bon nombre de scores au-dessus. La référence est
    // un tri des scores rendus PAR LE GPU : le critère porte ainsi sur le noyau
    // 2a et sur lui seul (l'écart du noyau 1 est mesuré juste au-dessus).
    let k = if opt.attn_topk > 0 { opt.attn_topk } else { 256 };
    if k == 0 || k > n {
        println!("  k = {k} hors de [1, {n}] : pas de top-k");
        return;
    }
    let lignes = n_kv * rep;
    let t2 = Instant::now();
    let mut seuils = vec![0f32; lignes];
    let mut sup_cpu = vec![0usize; lignes];
    let mut eq_cpu = vec![0usize; lignes];
    for l in 0..lignes {
        let ligne = &obtenu[l * n..(l + 1) * n];
        let mut tri = ligne.to_vec();
        tri.sort_unstable_by(|a, b| b.partial_cmp(a).unwrap());
        let sk = tri[k - 1];
        seuils[l] = sk;
        for &x in ligne {
            if x > sk { sup_cpu[l] += 1; } else if x == sk { eq_cpu[l] += 1; }
        }
    }
    let t_cpu_k = t2.elapsed().as_secs_f64();

    let mut hist = vec![0u32; lignes * 256];
    let mut prefixes = vec![0u32; lignes];
    let mut au_dessus = vec![0usize; lignes];
    let mut egaux = vec![0usize; lignes];
    let t3 = Instant::now();
    let mut passes = 0;
    let mut ok = true;
    for decalage in [24i32, 16, 8, 0] {
        if !machine.attn_topk_histo(&mut miroir, lignes, n, decalage, &prefixes, &mut hist) {
            println!("  le noyau d'histogramme a refusé la configuration");
            ok = false;
            break;
        }
        passes += 1;
        for l in 0..lignes {
            let h = &hist[l * 256..(l + 1) * 256];
            let mut cum = au_dessus[l];
            let mut b = 256usize;
            while b > 0 && cum < k {
                b -= 1;
                cum += h[b] as usize;
            }
            au_dessus[l] = cum - h[b] as usize;
            if decalage == 0 { egaux[l] = h[b] as usize; }
            prefixes[l] = (prefixes[l] << 8) | b as u32;
        }
    }
    let t_gpu_k = t3.elapsed().as_secs_f64();
    if !ok { return; }

    // Le même entier monotone que le noyau, calculé côté hôte.
    fn monotone(f: f32) -> u32 {
        let b = f.to_bits();
        if b & 0x8000_0000 != 0 { !b } else { b | 0x8000_0000 }
    }
    let mut exacts = 0usize;
    let mut comptes = 0usize;
    let mut encadre = 0usize;
    let mut pire = 0i64;
    for l in 0..lignes {
        let attendu_l = monotone(seuils[l]);
        if prefixes[l] == attendu_l { exacts += 1; }
        pire = pire.max((prefixes[l] as i64 - attendu_l as i64).abs());
        if au_dessus[l] == sup_cpu[l] && egaux[l] == eq_cpu[l] { comptes += 1; }
        if au_dessus[l] < k && k <= au_dessus[l] + egaux[l] { encadre += 1; }
    }
    // Combien de lignes ont un k-ième score qui CHANGE entre les scores CPU et
    // ceux du GPU : là seulement, l'égalité au bit près n'est pas attendue.
    let mut bouge = 0usize;
    for l in 0..lignes {
        let mut tri: Vec<f32> = attendu[l * n..(l + 1) * n].to_vec();
        tri.sort_unstable_by(|a, b| b.partial_cmp(a).unwrap());
        if monotone(tri[k - 1]) != monotone(seuils[l]) { bouge += 1; }
    }
    println!("  top-k k = {k} :");
    println!("    CPU  tri + comptage : {:8.2} ms", t_cpu_k * 1e3);
    println!("    GPU  {passes} passes d'histogramme : {:8.2} ms  ({:.1}× plus rapide)",
             t_gpu_k * 1e3, t_cpu_k / t_gpu_k.max(1e-9));
    println!("    k-ième score identique au bit près : {exacts}/{lignes} lignes (écart entier max \
{pire})");
    println!("    comptes « strictement au-dessus » et « égaux » : {comptes}/{lignes} lignes");
    println!("    encadrement au_dessus < k ≤ au_dessus+égaux : {encadre}/{lignes} lignes");
    println!("    k-ième score qui change entre scores CPU et GPU : {bouge}/{lignes} lignes \
(attendu : noyau 1 à {:.0e})", mx);
    if exacts == lignes && comptes == lignes && encadre == lignes {
        println!("    → la descente trouve le seuil EXACT : la collecte peut être écrite");
    } else {
        println!("    → ÉCART : ne pas écrire la collecte avant d'avoir compris");
    }

    // ---------------------------------------- noyaux 2b : la collecte des k indices
    // Référence : tri complet par (score décroissant, index croissant) puis
    // troncature à k. C'est le départage que les noyaux doivent reproduire —
    // ensemble identique, ordre des indices croissant, donc reproductible.
    let besoin: Vec<i32> = (0..lignes).map(|l| (k - au_dessus[l]) as i32).collect();
    let t4 = Instant::now();
    let mut idx_cpu = vec![-1i32; lignes * k];
    for l in 0..lignes {
        let ligne = &obtenu[l * n..(l + 1) * n];
        let mut ord: Vec<u32> = (0..n as u32).collect();
        ord.sort_unstable_by(|&a, &b| {
            ligne[b as usize].partial_cmp(&ligne[a as usize]).unwrap().then(a.cmp(&b))
        });
        ord.truncate(k);
        ord.sort_unstable();
        for (i, &v) in ord.iter().enumerate() { idx_cpu[l * k + i] = v as i32; }
    }
    let t_cpu_col = t4.elapsed().as_secs_f64();

    let mut sortie = vec![-1i32; lignes * k];
    let t5 = Instant::now();
    if !machine.attn_topk_collecte(&mut miroir, lignes, n, k, &prefixes, &besoin, &mut sortie) {
        println!("  la collecte a refusé la configuration");
        return;
    }
    let t_gpu_col = t5.elapsed().as_secs_f64();

    // Trois vérifications distinctes, parce qu'elles peuvent échouer
    // séparément : l'ENSEMBLE (le contrat du plan), l'ORDRE (le GPU écrit les
    // scores au-dessus du seuil puis les égaux, chaque groupe par indices
    // croissants — ce n'est PAS l'ordre croissant global, qui entrelace les deux
    // groupes), et l'absence de doublon ou d'indice hors borne.
    let mut set_ok = 0usize;
    let mut ordre_ok = 0usize;
    let mut cases_vides = 0usize;
    let mut diff_sym = 0usize;
    let mut doublons = 0usize;
    let mut hors_bornes = 0usize;
    for l in 0..lignes {
        let (a, b) = (&idx_cpu[l * k..(l + 1) * k], &sortie[l * k..(l + 1) * k]);
        cases_vides += b.iter().filter(|&&v| v < 0).count();
        hors_bornes += b.iter().filter(|&&v| v < 0 || v as usize >= n).count();
        // différence symétrique des deux ensembles (indépendante de l'ordre)
        let (mut sa, mut sb) = (a.to_vec(), b.to_vec());
        sa.sort_unstable(); sb.sort_unstable();
        if sb.windows(2).any(|w| w[0] == w[1]) { doublons += 1; }
        if sa == sb { set_ok += 1; }
        let (mut i, mut j) = (0usize, 0usize);
        while i < sa.len() && j < sb.len() {
            match sa[i].cmp(&sb[j]) {
                std::cmp::Ordering::Equal => { i += 1; j += 1; }
                std::cmp::Ordering::Less => { diff_sym += 1; i += 1; }
                std::cmp::Ordering::Greater => { diff_sym += 1; j += 1; }
            }
        }
        diff_sym += (sa.len() - i) + (sb.len() - j);
        // L'ordre documenté : [au-dessus, indices croissants] puis [égaux,
        // indices croissants], et chaque indice dans le bon groupe.
        let dep = au_dessus[l];
        let seuil = seuils[l];
        let mut ok = true;
        for (i, &v) in b.iter().enumerate() {
            if i > 0 && i != dep && b[i - 1] >= v { ok = false; }
            let s = obtenu[l * n + v.max(0) as usize];
            if i < dep { if !(s > seuil) { ok = false; } }
            else if s != seuil { ok = false; }
        }
        if ok { ordre_ok += 1; }
    }
    println!("    collecte GPU {:8.2} ms · CPU tri complet {:8.2} ms ({:.1}× plus rapide)",
             t_gpu_col * 1e3, t_cpu_col * 1e3, t_cpu_col / t_gpu_col.max(1e-9));
    println!("    ensembles identiques au CPU : {set_ok}/{lignes} lignes · différence symétrique \
{diff_sym} indices");
    println!("    ordre documenté (au-dessus puis égaux, croissants) : {ordre_ok}/{lignes} lignes · \
doublons {doublons} · hors bornes {hors_bornes} · cases non écrites {cases_vides}");
    if set_ok == lignes && diff_sym == 0 && doublons == 0 && hors_bornes == 0 && cases_vides == 0 {
        println!("    → l'ensemble retenu est le MÊME que celui du CPU, et l'ordre est celui qui \
est écrit dans le noyau");
        if ordre_ok != lignes {
            println!("    → (l'ordre croissant GLOBAL n'est pas garanti : le tri CPU ci-dessus \
l'entrelace — c'est le seul écart attendu)");
        }
    } else {
        println!("    → ÉCART sur la sélection");
    }

    // ------------------------------- noyau 3 : softmax sur les k, puis Σ w·V
    // La référence CPU consomme les MÊMES indices (ceux rendus par le GPU) et
    // les MÊMES scores (ceux du GPU) : le seul écart possible vient donc du
    // noyau 3. Les puits comptent dans le dénominateur, jamais au numérateur —
    // c'est le piège que le plan signale, et il est testé ici avec des puits
    // différents par ligne.
    // Le moteur passe `None` pour les modèles SANS puits (Qwen, la plupart) : ce
    // chemin n'était exercé par aucun banc. `DRAVE_BANC_SANS_PUITS=1` le teste.
    let avec_puits = std::env::var("DRAVE_BANC_SANS_PUITS").is_err();
    let sinks: Vec<f32> = (0..lignes).map(|l| -1.0 + 0.001 * l as f32).collect();
    let sinks_opt: Option<&[f32]> = if avec_puits { Some(&sinks) } else { None };
    let mut att_gpu = vec![0f32; lignes * hd];
    let t8 = Instant::now();
    // Un refus du noyau 3 (k > 1024, valeurs 4 bits) ne doit pas interrompre le
    // banc : les blocs suivants (noyau fusionné, second passage) restent
    // mesurables, et c'est justement là qu'on veut voir le repli.
    let ok3 = machine.attn_topk_somme(&mut miroir, lignes, n, k, hd, rep, Some(&sinks),
                                      &mut att_gpu);
    if !ok3 {
        println!("    le noyau 3 a refusé la configuration (k = {k} ?) — suites du banc \
poursuivies");
    }
    let t_somme = t8.elapsed().as_secs_f64();
    let t9 = Instant::now();
    let mut att_cpu = vec![0f32; lignes * hd];
    {
        let mut vd = vec![0f32; hd];
        for l in 0..lignes {
            let sel = &sortie[l * k..(l + 1) * k];
            let kvh = l / rep;
            let mut m = sinks[l];
            for &j in sel { m = m.max(obtenu[l * n + j as usize]); }
            let mut den = (sinks[l] - m).exp();
            let mut w = vec![0f32; k];
            for (i, &j) in sel.iter().enumerate() {
                let e = (obtenu[l * n + j as usize] - m).exp();
                w[i] = e;
                den += e;
            }
            for i in 0..k {
                cache.valeur(kvh, sel[i] as usize, &mut vd);
                for d in 0..hd { att_cpu[l * hd + d] += w[i] * vd[d]; }
            }
            for d in 0..hd { att_cpu[l * hd + d] /= den; }
        }
    }
    let t_cpu_somme = t9.elapsed().as_secs_f64();
    let mut mx3 = 0f32;
    let mut dyn3 = 0f32;
    if ok3 {
        for (a, b) in att_cpu.iter().zip(att_gpu.iter()) {
            mx3 = mx3.max((a - b).abs());
            dyn3 = dyn3.max(a.abs());
        }
    }
    println!("    noyau 3 (softmax sur k + Σ w·V) : GPU {:.2} ms · CPU {:.2} ms · écart max \
{mx3:.3e} sur {dyn3:.3e} (relatif {:.2e})",
             t_somme * 1e3, t_cpu_somme * 1e3, mx3 / dyn3.max(1e-9));
    if ok3 && mx3 / dyn3.max(1e-9) < 1e-6 {
        println!("    → conforme au critère du plan pour la sortie (1e-6)");
    } else if ok3 {
        println!("    → AU-DESSUS du critère de 1e-6 : ne pas brancher dans le moteur");
    }

    // ---------------- noyau 4 : tout le top-k d'une ligne en UN lancement
    // Même vérification que la chaîne séparée, mais par le noyau fusionné : les
    // indices ne sortent plus de la VRAM, donc la comparaison porte sur la
    // SORTIE (le vecteur d'attention) et non sur l'ensemble des indices.
    {
        let mut att4 = vec![0f32; lignes * hd];
        let t10 = Instant::now();
        let ok4 = machine.attn_scores_sans_relecture(&mut miroir, &q, n, scale)
            && machine.attn_topk_tout(&mut miroir, lignes, n, k, hd, rep, sinks_opt,
                                      &mut att4);
        let t_tout = t10.elapsed().as_secs_f64();
        if !ok4 {
            println!("    noyau 4 : refusé (repli sur la chaîne séparée)");
        } else {
            // Référence : les mêmes k indices que le noyau 4 doit choisir, et les
            // mêmes valeurs — recalculés ici depuis le cache hôte.
            let mut att_ref = vec![0f32; lignes * hd];
            {
                let mut vd = vec![0f32; hd];
                for l in 0..lignes {
                    let ligne = &obtenu[l * n..(l + 1) * n];
                    let mut ord: Vec<u32> = (0..n as u32).collect();
                    ord.sort_unstable_by(|&a, &b| {
                        ligne[b as usize].partial_cmp(&ligne[a as usize]).unwrap().then(a.cmp(&b))
                    });
                    ord.truncate(k);
                    let kvh = l / rep;
                    // La référence doit consommer LES MÊMES puits que le noyau,
                    // sinon elle compare deux calculs différents : sans cette
                    // ligne, le passage `DRAVE_BANC_SANS_PUITS=1` annonçait un
                    // écart de 1,02e-3 qui n'était que celui du banc.
                    let puits_l = sinks_opt.map(|s| s[l]);
                    let mut m = puits_l.unwrap_or(f32::NEG_INFINITY);
                    for &j in ord.iter() { m = m.max(ligne[j as usize]); }
                    let mut den = match puits_l { Some(s) => (s - m).exp(), None => 0.0 };
                    let mut w = vec![0f32; k];
                    for (i, &j) in ord.iter().enumerate() {
                        let e = (ligne[j as usize] - m).exp();
                        w[i] = e;
                        den += e;
                    }
                    for i in 0..k {
                        cache.valeur(kvh, ord[i] as usize, &mut vd);
                        for d in 0..hd { att_ref[l * hd + d] += w[i] * vd[d]; }
                    }
                    for d in 0..hd { att_ref[l * hd + d] /= den; }
                }
            }
            let mut mx4 = 0f32;
            let mut dyn4 = 0f32;
            for (a, b) in att_ref.iter().zip(att4.iter()) {
                mx4 = mx4.max((a - b).abs());
                dyn4 = dyn4.max(a.abs());
            }
            println!("    noyau 4 (UN lancement) : {:.2} ms · écart max {mx4:.3e} sur {dyn4:.3e} \
(relatif {:.2e})", t_tout * 1e3, mx4 / dyn4.max(1e-9));
            if mx4 / dyn4.max(1e-9) < 1e-6 {
                println!("    → conforme au critère du plan (1e-6), en UN lancement au lieu de huit");
            } else {
                println!("    → AU-DESSUS du critère de 1e-6 : ne pas brancher le noyau 4");
            }
        }
    }

    // ------------------- étape 5 : ce que coûtera le chemin du MOTEUR à 1 M
    // Le moteur n'a pas besoin de relire les scores : la sélection se fait en
    // VRAM. On mesure donc la chaîne complète SANS relecture, et on la compare à
    // l'attention complète sur CPU (toutes les clés notées, softmax, somme
    // pondérée) — la référence que le plan cite : 968 ms par couche à 1 M de clés.
    // Seuil de mesure : 4 096 clés suffisent à comparer les deux chemins, et le
    // point de croisement entre le noyau fusionné et la chaîne séparée est
    // justement ce qu'on cherche (mesuré : 65 536 pour le premier, 262 144 pour
    // la seconde).
    if n >= 4096 {
        let mut pref5 = vec![0u32; lignes];
        let mut dessus5 = vec![0usize; lignes];
        let mut hist5 = vec![0u32; lignes * 256];
        let t10 = Instant::now();
        let mut ok5 = machine.attn_scores_sans_relecture(&mut miroir, &q, n, scale);
        for decalage in [24i32, 16, 8, 0] {
            if !ok5 { break; }
            ok5 = machine.attn_topk_histo(&mut miroir, lignes, n, decalage, &pref5, &mut hist5);
            if !ok5 { break; }
            for l in 0..lignes {
                let h = &hist5[l * 256..(l + 1) * 256];
                let mut cum = dessus5[l];
                let mut b = 256usize;
                while b > 0 && cum < k { b -= 1; cum += h[b] as usize; }
                dessus5[l] = cum - h[b] as usize;
                pref5[l] = (pref5[l] << 8) | b as u32;
            }
        }
        let besoin5: Vec<i32> = (0..lignes).map(|l| (k - dessus5[l]) as i32).collect();
        let mut sel5 = vec![-1i32; lignes * k];
        let mut att5 = vec![0f32; lignes * hd];
        if ok5 {
            ok5 = machine.attn_topk_collecte(&mut miroir, lignes, n, k, &pref5, &besoin5,
                                             &mut sel5);
        }
        if ok5 {
            ok5 = machine.attn_topk_somme(&mut miroir, lignes, n, k, hd, rep, Some(&sinks),
                                          &mut att5);
        }
        let t_chaine = t10.elapsed().as_secs_f64();
        if !ok5 {
            println!("    étape 5 : chaîne complète refusée");
        } else {
            // Référence : l'attention COMPLÈTE sur CPU, une ligne par fil.
            let t11 = Instant::now();
            let mut att_full = vec![0f32; lignes * hd];
            std::thread::scope(|sp| {
                for (l, dst) in att_full.chunks_mut(hd).enumerate() {
                    let cache = &cache;
                    let q = &q;
                    let sinks = &sinks;
                    sp.spawn(move || {
                        let kvh = l / rep;
                        let r = l % rep;
                        let qh = &q[(kvh * rep + r) * hd..(kvh * rep + r + 1) * hd];
                        let (mut kd, mut vd) = (vec![0f32; hd], vec![0f32; hd]);
                        let mut sc = vec![0f32; n];
                        let mut m = sinks[l];
                        for t in 0..n {
                            cache.cle(kvh, t, &mut kd);
                            let mut s = 0f32;
                            for i in 0..hd { s += qh[i] * kd[i]; }
                            s *= scale;
                            sc[t] = s;
                            m = m.max(s);
                        }
                        let mut den = (sinks[l] - m).exp();
                        for t in 0..n { den += (sc[t] - m).exp(); }
                        for t in 0..n {
                            let w = (sc[t] - m).exp();
                            cache.valeur(kvh, t, &mut vd);
                            for i in 0..hd { dst[i] += w * vd[i]; }
                        }
                        for i in 0..hd { dst[i] /= den; }
                    });
                }
            });
            let t_full = t11.elapsed().as_secs_f64();
            println!("    étape 5 — {lignes} lignes × {n} clés :");
            println!("      chaîne top-k GPU sans relecture des scores : {:8.2} ms", t_chaine * 1e3);
            println!("      attention COMPLÈTE sur CPU ({lignes} fils)   : {:8.2} ms  (×{:.1})",
                     t_full * 1e3, t_full / t_chaine.max(1e-9));
            println!("      coût de la relecture des scores (banc seul) : {:8.2} ms",
                     t_gpu * 1e3 - t_chaine * 1e3);
        }
    }

    // Second passage avec un k PLUS GRAND, dans le MÊME processus : c'est le
    // seul chemin qui réutilise les tampons de la collecte avec une taille de
    // sortie différente. Défaut trouvé à la relecture (pas par ce banc) : le
    // tampon de sortie n'était réalloué que si (lignes, tranches) grandissait,
    // donc un k plus grand écrivait AU-DELÀ du tampon.
    //
    // ⚠️ Ce passage VÉRIFIE la réutilisation, il ne prouve pas qu'un
    // débordement serait visible : `cuMemAlloc` arrondit à la granule du
    // pilote (≥ 64 ko), donc 14 ko d'écriture hors bornes peuvent passer
    // inaperçus. Ce qui l'empêche, c'est le garde piloté par les CAPACITÉS
    // dans `attn_topk_collecte` — pas ce banc (relevé par le relecteur).
    if 2 * k <= n {
        let k2 = 2 * k;
        let mut prefixes2 = vec![0u32; lignes];
        let mut dessus2 = vec![0usize; lignes];
        let mut ok2 = true;
        let t7 = Instant::now();
        for decalage in [24i32, 16, 8, 0] {
            if !machine.attn_topk_histo(&mut miroir, lignes, n, decalage, &prefixes2, &mut hist) {
                ok2 = false;
                break;
            }
            for l in 0..lignes {
                let h = &hist[l * 256..(l + 1) * 256];
                let mut cum = dessus2[l];
                let mut b = 256usize;
                while b > 0 && cum < k2 { b -= 1; cum += h[b] as usize; }
                dessus2[l] = cum - h[b] as usize;
                prefixes2[l] = (prefixes2[l] << 8) | b as u32;
            }
        }
        let t2_k2 = t7.elapsed().as_secs_f64();
        let besoin2: Vec<i32> = (0..lignes).map(|l| (k2 - dessus2[l]) as i32).collect();
        let mut sortie2 = vec![-1i32; lignes * k2];
        let t6 = Instant::now();
        let fait = ok2
            && machine.attn_topk_collecte(&mut miroir, lignes, n, k2, &prefixes2, &besoin2,
                                          &mut sortie2);
        let t_k2 = t6.elapsed().as_secs_f64();
        if fait {
            let mut ok_lignes = 0usize;
            let mut vides = 0usize;
            for l in 0..lignes {
                // Même référence que le premier passage : tri (score décroissant,
                // indice croissant) puis troncature à k2. Un simple filtre
                // « ≥ seuil » ramasserait TOUS les égaux au k2-ième score — plus
                // de k2 indices — et le banc accuserait la réutilisation des
                // tampons alors que le noyau aurait raison (relevé par le
                // relecteur).
                let ligne = &obtenu[l * n..(l + 1) * n];
                let mut att: Vec<u32> = (0..n as u32).collect();
                att.sort_unstable_by(|&a, &b| {
                    ligne[b as usize].partial_cmp(&ligne[a as usize]).unwrap().then(a.cmp(&b))
                });
                att.truncate(k2);
                att.sort_unstable();
                let mut set: Vec<u32> = sortie2[l * k2..(l + 1) * k2]
                    .iter().map(|&v| v as u32).collect();
                vides += set.iter().filter(|&&v| v == u32::MAX).count();
                set.sort_unstable();
                if set == att { ok_lignes += 1; }
            }
            // ⚠️ `t_k2` et `t2_k2` sont en SECONDES : les afficher avec l'unité « ms »
            // sans convertir a fait croire à un noyau 1 500× trop rapide — un
            // affichage mal étiqueté est un affichage qui ment.
            println!("    second passage k = {k2}, mêmes tampons : {ok_lignes}/{lignes} lignes · \
{:.2} ms ({:.2} ms de seuil) · cases non écrites {vides}", t_k2 * 1e3, t2_k2 * 1e3);
            if ok_lignes != lignes || vides != 0 {
                println!("    → ÉCART : la réutilisation des tampons avec un k plus grand est \
suspecte");
            }
        } else {
            println!("    second passage k = {k2} : REFUSÉ (la réutilisation des tampons est \
cassée)");
        }
    }
}

/// Banc **MLA** : passe avant du modèle synthétique, logits écrits en binaire
/// pour être comparés à `logits.npy` (référence numpy indépendante).
fn run_banc_mla(opt: Options, sortie: &str) {
    use std::io::Write;
    // Le chemin MLA est un banc de comparaison avec numpy (`forward_mla` part des
    // embeddings et n'appelle ni `flux_lot` ni le compteur de jeton global) : la
    // trace et le rejeu n'y sont pas branchés, et le dire vaut mieux que de laisser
    // croire qu'ils le sont (relevé par la relecture adversariale).
    if opt.trace_flux.is_some() || opt.flux_forcer.is_some() {
        eprintln!("[banc-mla] ni --trace-flux ni --flux-forcer ne s'appliquent à ce \
banc : il écrit des logits pour la comparaison numpy, sans passer par le flux.");
    }
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

/// Banc du **KV déporté** (étape E4) : le cache d'une couche tient en VRAM, une
/// passe d'attention est calculée par le noyau, et le résultat est comparé au
/// chemin du moteur (mêmes `cle`/`valeur`, même `dot8`, même softmax).
///
/// Ce banc mesure ce que le plan 1 M annonce : à 1 M de contexte, l'attention
/// n'est plus bornée par la RAM (20 Go/s) mais par la VRAM (≈ 450 Go/s).
fn run_banc_kv(opt: Options) {
    use crate::model::{KvCache, Model};
    use std::time::Instant;
    let path = &modele_chemin();
    let g = Gguf::open_auto(path).expect("ouverture du GGUF");
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

    // 1. Cache CPU d'UNE couche, rempli de façon déterministe.
    let mut cache = KvCache::new(bits, n_kv, n, hd);
    let mut etat = 12345u64;
    let mut suivant = move || {
        etat = etat.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        ((etat >> 33) as f32 / (1u64 << 31) as f32) - 1.0
    };
    // Deux cas dégénérés pour isoler une erreur du noyau : clés nulles (poids
    // uniformes) et valeurs constantes (la sortie vaut 1 quelle que soit la
    // softmax). Les deux doivent être reproduits EXACTEMENT.
    let k_nul = std::env::var("DRAVE_BANC_KV_K0").is_ok();
    let v_un = std::env::var("DRAVE_BANC_KV_V1").is_ok();
    // Troisième cas : valeurs « une chaude » par position — la sortie devient
    // alors le poids de chaque clé, ce qui montre si les poids sont appariés à
    // la BONNE ligne de valeurs.
    let v_unitaire = std::env::var("DRAVE_BANC_KV_UNIT").is_ok();
    // Cas « pente » : une seule composante de requête non nulle et des clés
    // croissantes sur cette composante. La softmax se concentre alors sur la
    // DERNIÈRE clé, et la sortie doit valoir sa ligne de valeurs : le test le
    // plus lisible de l'appariement poids ↔ valeurs.
    let pente = std::env::var("DRAVE_BANC_KV_GRAD").is_ok();
    // Clés « une chaude » : la clé k ne parle qu'à la composante k. Avec une
    // requête e_0, seule la clé 0 a un score non nul — signature nette.
    let k_unitaire = std::env::var("DRAVE_BANC_KV_KUNIT").is_ok();
    let (mut k, mut v) = (vec![0f32; hd], vec![0f32; hd]);
    for pos in 0..n {
        for kvh in 0..n_kv {
            for i in 0..hd {
                suivant();
                suivant();
                k[i] = if k_nul { 0.0 }
                       else if k_unitaire { if i == pos % hd { 1.0 } else { 0.0 } }
                       else if pente { if i == 0 { pos as f32 * 100.0 } else { 0.0 } }
                       else { suivant() };
                v[i] = if v_un { 1.0 }
                       else if v_unitaire { if i == pos % hd { 1.0 } else { 0.0 } }
                       else { suivant() };
            }
            cache.ecrire(kvh, pos, &k, &v);
        }
    }
    let mut qs: Vec<f32> = (0..n_head * hd).map(|_| suivant()).collect();
    if pente {
        for hh in 0..n_head {
            for i in 0..hd { qs[hh * hd + i] = if i == 0 { 1.0 } else { 0.0 }; }
        }
    }

    // 2. Référence CPU : le chemin exact du moteur, une tête par fil.
    //    `DRAVE_BANC_KV_GPU_SEUL=1` la saute : à 1 M de clés elle coûte 3 à 16
    //    minutes pour un chiffre (la vitesse du noyau) qui n'en a pas besoin.
    let gpu_seul = std::env::var("DRAVE_BANC_KV_GPU_SEUL").is_ok();
    let threads = if opt.threads_impose { opt.threads } else {
        engine::coeurs_physiques().max(1)
    };
    let t0 = Instant::now();
    let mut cpu = vec![0f32; n_head * hd];
    {
        let cache = &cache;
        let qs = &qs;
        std::thread::scope(|sp| {
            for (hh, dst) in cpu.chunks_mut(hd).enumerate() {
                sp.spawn(move || {
                    let kvh = hh / rep;
                    let qh = &qs[hh * hd..(hh + 1) * hd];
                    let (mut kd, mut vd) = (vec![0f32; hd], vec![0f32; hd]);
                    let mut sc = vec![0f32; n];
                    let mut mx = f32::NEG_INFINITY;
                    for tt in 0..n {
                        cache.cle(kvh, tt, &mut kd);
                        let s = Model::dot8(qh, &kd) * scale;
                        sc[tt] = s;
                        if s > mx { mx = s; }
                    }
                    let mut somme = 0f32;
                    for tt in 0..n { let e = (sc[tt] - mx).exp(); sc[tt] = e; somme += e; }
                    let inv = 1.0 / somme;
                    for val in dst.iter_mut() { *val = 0.0; }
                    for tt in 0..n {
                        let w = sc[tt] * inv;
                        cache.valeur(kvh, tt, &mut vd);
                        for (o, x) in dst.iter_mut().zip(vd.iter()) { *o += w * x; }
                    }
                });
            }
        });
    }
    let tc = t0.elapsed().as_secs_f64();
    let octets = cache.octets();
    let _ = threads;
    if gpu_seul {
        println!("  CPU non mesuré (DRAVE_BANC_KV_GPU_SEUL) · {:.2} Go de KV, une couche", octets as f64 / 1e9);
    } else {
        println!("  CPU {threads} fils : {:>8.1} ms par passe  ({:.1} Go/s de KV, {:.1} ms × {n_layer} couches = {:.0} ms/jeton)",
                 tc * 1e3, 2.0 * octets as f64 / tc / 1e9, tc * 1e3,
                 tc * 1e3 * n_layer as f64);
    }

    let Some(machine) = gpu::instance() else { println!("  GPU absent"); return };
    let Some(mut m) = machine.kv_allouer(n_kv, n, hd, bits) else {
        println!("  KV déporté impossible : {:.2} Go demandés pour une couche, {:.2} Go libres",
                 (2 * cache.octets() / 8) as f64 / 1e9, machine.memoire_libre as f64 / 1e9);
        return;
    };
    println!("  {} · KV d'une couche : {:.2} Go résidents, {:.2} Go libres", machine.nom,
             m.octets as f64 / 1e9, machine.memoire_libre as f64 / 1e9);
    // 3. Recopie du cache CPU vers la VRAM, vecteur par vecteur (les octets sont
    //    déjà dans la disposition du noyau : aucune conversion).
    let t1 = Instant::now();
    for pos in 0..n {
        for kvh in 0..n_kv {
            if !cache.vers_gpu(machine, &mut m, kvh, pos) { println!("  recopie en échec"); return; }
        }
    }
    println!("  recopie CPU → VRAM : {:.1} s ({:.1} Go/s sur le bus)",
             t1.elapsed().as_secs_f64(),
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
        let c = &cpu[..8];
        let o = &out[..8];
        println!("  poids CPU 0..8 : {}", c.iter().map(|v| format!("{v:.4}")).collect::<Vec<_>>().join(" "));
        println!("  poids GPU 0..8 : {}", o.iter().map(|v| format!("{v:.4}")).collect::<Vec<_>>().join(" "));
        println!("  somme CPU {:.4} · somme GPU {:.4}", c.iter().sum::<f32>(), o.iter().sum::<f32>());
    }
    if std::env::var("DRAVE_BANC_KV_DEBUG").is_ok() {
        let ech = |v: &[f32]| v.iter().fold(1e-9f32, |a, &b| a.max(b.abs()));
        for hh in 0..n_head {
            let c = &cpu[hh * hd..(hh + 1) * hd];
            let o = &out[hh * hd..(hh + 1) * hd];
            let e = (0..hd).fold(0f32, |a, i| a.max((o[i] - c[i]).abs())) / ech(c);
            print!("  tête {hh:2} écart {e:.2e} | cpu[0..3] {:.4} {:.4} {:.4} | gpu[0..3] {:.4} {:.4} {:.4}\n",
                   c[0], c[1], c[2], o[0], o[1], o[2]);
        }
    }
}

fn run_gpu_banc(opt: Options) {
    use std::time::Instant;
    let path = &modele_chemin();
    let threads = if opt.threads_impose { opt.threads } else {
        engine::coeurs_physiques().max(1)
    };
    let g = Gguf::open_auto(path).expect("ouverture du GGUF");
    // Le banc porte sur la tête Q8_0, ou sur le tenseur nommé (`--matrix`) quand
    // c'est une matrice d'experts MXFP4 — c'est le poste dominant de gpt-oss.
    let mx = g.mxfp4_blocks(&opt.matrix).is_some();
    let nom_q6k = opt.matrix.clone();
    if !mx && g.q6k_blocks(&nom_q6k).is_some() {
        return banc_q6k(opt, &g, &nom_q6k, threads);
    }
    let nom_q4k = opt.matrix.clone();
    if !mx && nom_q4k != "output.weight" && nom_q4k != "token_embd.weight"
        && g.q4k_blocks(&nom_q4k).is_some() {
        return banc_q4k(opt, &g, &nom_q4k, threads);
    }
    let nom = if mx { opt.matrix.clone() } else if g.tensor("output.weight").is_some() {
        "output.weight".to_string()
    } else { "token_embd.weight".to_string() };
    let nom = nom.as_str();
    let t = g.tensor(nom).unwrap();
    if mx {
        return banc_mxfp4(opt, &g, nom, threads);
    }
    let (blocs, nb) = g.q8_blocks(nom).expect("tête Q8_0 requise pour ce banc");
    let (n_out, n_in) = (t.dims[0] as usize, t.dims[1] as usize);
    // Taille RÉELLE des poids de la tête (`blocs` couvre la fin du fichier).
    let octets = n_out * nb * 34;
    println!("tête {nom} : {n_out} × {n_in} · {:.1} Mo · {} blocs de 32",
             octets as f64 / 1e6, nb);

    // Activations de test, quantifiées comme dans le moteur. Les noyaux de TÊTE
    // ne multiplient PAS par l'échelle d'activation (c'est `proj_q8` qui le
    // fait) : la comparaison doit donc se faire sans `sx`, sinon l'écart
    // mesuré n'est que le facteur oublié (constaté : 2,5e2).
    let xi: Vec<i32> = (0..n_in).map(|i| ((i * 2654435761usize) % 255) as i32 - 127).collect();

    // 1. CPU : le chemin de référence.
    let d = unsafe { DenseQ8::emprunter_q8(blocs.as_ptr(), n_out, n_in, nb) };
    let t0 = Instant::now();
    let mut cpu = vec![0f32; n_out];
    let chunk = n_out.div_ceil(threads);
    let (dref, xiref) = (&d, &xi);
    std::thread::scope(|sc| {
        for (ci, part) in cpu.chunks_mut(chunk).enumerate() {
            let base = ci * chunk;
            sc.spawn(move || {
                for (j, o) in part.iter_mut().enumerate() {
                    *o = dref.dot_q8_source(base + j, xiref);
                }
            });
        }
    });
    let tc = t0.elapsed().as_secs_f64();
    println!("  CPU  {threads} fils : {:>7.1} ms  ({:>6.1} Go/s)", tc * 1e3, octets as f64 / tc / 1e9);

    // 2 et 3. GPU : ancien noyau (une ligne par fil) puis warp par ligne.
    let Some(machine) = gpu::instance() else {
        println!("  GPU absent : banc terminé");
        return;
    };
    println!("  {}", machine.nom);
    // `--limit N` plafonne le nombre de lignes : c'est ce qui permet de
    // distinguer un noyau qui boucle d'un transfert qui bloque.
    let n_out = if opt.limit < n_out { opt.limit } else { n_out };
    eprintln!("[banc] allocation de {:.1} Mo sur le GPU", (n_out * nb * 34) as f64 / 1e6);
    let Some(m) = machine.charger_tete(&blocs[..n_out * nb * 34], n_out, n_in, nb) else {
        println!("  allocation GPU impossible");
        return;
    };
    eprintln!("[banc] poids montés, premier lancement");
    for (nom_noyau, warp) in [("ligne par fil", false), ("warp par ligne", true)] {
        // Deux passes : la première paie le transfert, la seconde mesure.
        let mut ms = f64::MAX;
        let mut dernier: Vec<f32> = Vec::new();
        for passe in 0..3 {
            let t1 = Instant::now();
            let r = if warp { machine.tete_warp(&m, &xi) } else { machine.tete(&m, &xi) };
            let dt = t1.elapsed().as_secs_f64();
            let Some(r) = r else { println!("  {nom_noyau} : échec"); break; };
            if passe > 0 && dt < ms { ms = dt; }
            dernier = r;
        }
        if dernier.is_empty() { continue; }
        // Accord avec le CPU : les sommes ne sont pas dans le même ordre, donc
        // seuls les derniers bits changent. L'écart est rapporté à la PLUS
        // GRANDE valeur, pas à chaque valeur : une sortie proche de zéro
        // donnerait sinon un écart relatif absurde.
        let mut ecart_max = 0f32;
        let mut echelle = 1e-9f32;
        for o in 0..n_out { echelle = echelle.max(cpu[o].abs()); }
        for o in 0..n_out {
            let e = (dernier[o] - cpu[o]).abs() / echelle;
            if e > ecart_max { ecart_max = e; }
        }
        println!("  GPU  {nom_noyau:<14} : {:>7.1} ms  ({:>6.1} Go/s)  écart max {:+.2e} (relatif au plus grand logit)",
                 ms * 1e3, octets as f64 / ms / 1e9, ecart_max);
    }
}


/// Banc d'essai du noyau **MXFP4** (experts de gpt-oss) contre le CPU.
///
/// Le format est celui des experts : blocs de 17 octets. Le noyau est « une warp
/// par ligne », comme les noyaux Q8_0 — c'est le même correctif d'accès mémoire,
/// appliqué au format qui porte les 120 milliards de paramètres de gpt-oss.
/// **Le transfert VRAM, par expert** — la mesure qui manquait pour décider du dessin.
///
/// Le cache d'experts du GPU téléverse **un expert à la fois** (`charger_mxfp4` sur les
/// trois matrices), et c'est ce qui a été mesuré comme perdant (×1,09). Mais *pourquoi* :
/// est-ce le noyau, ou le transfert ? Ce banc monte N experts **un par un** (granularité
/// fine) et publie le débit et le temps par expert, séparément du noyau — sans quoi on ne
/// saurait pas s'il faut streamer (double tampon, transferts recouverts) ou cesser de
/// transférer.
fn banc_transfert(machine: &crate::gpu::Gpu, blocs: &[u8], n_experts: usize, lignes: usize,
                  nb: usize, octets_expert: usize, mxfp4: bool, etiquette: &str) {
    use std::time::Instant;
    // `lignes` = le nombre de lignes d'UN expert (`n_out` de la vue). La première version
    // passait 1 : elle allouait 1 152 octets au lieu de 0,88 Mo et annonçait « 42 Go/s » —
    // un chiffre impossible sur un lien PCIe, ce qui est exactement ce qui l'a dénoncé.
    assert_eq!(lignes * nb * if mxfp4 { 17 } else { 144 }, octets_expert);
    let n = n_experts.min(16);
    if n <= 1 { return; }
    if blocs.len() < n * octets_expert { return; }
    let mut gardees = Vec::with_capacity(n);
    let t0 = Instant::now();
    for e in 0..n {
        let bloc = &blocs[e * octets_expert..(e + 1) * octets_expert];
        let m = if mxfp4 { machine.charger_mxfp4(bloc, lignes, nb) }
                else { machine.charger_q4k(bloc, lignes, nb) };
        match m { Some(m) => gardees.push(m), None => break }
    }
    let dt = t0.elapsed().as_secs_f64();
    let octets = (gardees.len() * octets_expert) as f64;
    if gardees.is_empty() || dt <= 0.0 { return; }
    println!("  transfert {etiquette} : {} experts × {:.2} Mo en {:.1} ms → {:.2} Go/s \
({:.3} ms/expert) [allocation + copie]",
             gardees.len(), octets_expert as f64 / 1e6, dt * 1e3, octets / dt / 1e9,
             dt * 1e3 / gardees.len() as f64);
    // LE MÊME TRANSFERT SANS ALLOCATION : un tampon réutilisé. C'est la question du dessin —
    // « granularité fine » n'oblige pas à allouer à chaque fois.
    if let Some(premiere) = gardees.first() {
        let t1 = Instant::now();
        let mut fait = 0usize;
        // La borne vient du NOMBRE D'EXPERTS, pas d'un compteur qui vient d'être mis à zéro :
        // la première version écrivait `1..=n.min(...)` après `let mut n = 0` — zéro tour, et
        // la ligne ne s'imprimait pas du tout (un silence qui ressemble à un succès).
        for e in 1..=n_experts.min(gardees.len().saturating_sub(1)) {
            let bloc = &blocs[e * octets_expert..(e + 1) * octets_expert];
            if machine.recopier(premiere, bloc) { fait += 1; }
        }
        let dt1 = t1.elapsed().as_secs_f64();
        if fait > 0 && dt1 > 0.0 {
            let o1 = (fait * octets_expert) as f64;
            println!("  transfert {etiquette} : {fait} experts dans UN tampon réutilisé → \
{:.2} Go/s ({:.3} ms/expert) [copie seule]",
                     o1 / dt1 / 1e9, dt1 * 1e3 / fait as f64);
        }
    }
}

fn banc_mxfp4(opt: Options, g: &Gguf, nom: &str, threads: usize) {
    use std::time::Instant;
    let (blocs, nb) = g.mxfp4_blocks(nom).expect("matrice MXFP4");
    let t = g.tensor(nom).unwrap();
    // Un tenseur d'experts est 3D : on mesure le PREMIER expert.
    let (n_out, n_in) = (t.dims[1] as usize, t.dims[2] as usize);
    let octets = n_out * nb * 17;
    println!("matrice MXFP4 {nom} (expert 0) : {n_out} × {n_in} · {:.1} Mo · {} blocs de 32",
             octets as f64 / 1e6, nb);
    let xi: Vec<i32> = (0..n_in).map(|i| ((i * 2654435761usize) % 255) as i32 - 127).collect();
    let d = unsafe { DenseQ4::emprunter(blocs.as_ptr(), n_out, n_in, nb, true) };
    // Chemin AVX2 de PRODUCTION (celui de `matvec_q4`) : activations en i16 et
    // sommes par bloc de 32 précalculées. Comparer au chemin scalaire donnait un
    // facteur flatteur qui ne dit rien du régime réel.
    let x16: Vec<i16> = xi.iter().map(|&v| v.clamp(-32767, 32767) as i16).collect();
    let sx32 = crate::list::sommes32(&x16);
    let t0 = Instant::now();
    let mut cpu = vec![0f32; n_out];
    let chunk = n_out.div_ceil(threads);
    let dref = &d;
    let (x16ref, sxref) = (&x16, &sx32);
    std::thread::scope(|sc| {
        for (ci, part) in cpu.chunks_mut(chunk).enumerate() {
            let base = ci * chunk;
            sc.spawn(move || {
                for (j, o) in part.iter_mut().enumerate() {
                    *o = dref.dot16(base + j, x16ref, sxref);
                }
            });
        }
    });
    let tc = t0.elapsed().as_secs_f64();
    println!("  CPU  {threads} fils : {:>7.1} ms  ({:>6.1} Go/s)", tc * 1e3, octets as f64 / tc / 1e9);
    let Some(machine) = gpu::instance() else { println!("  GPU absent"); return };
    banc_transfert(machine, blocs, t.dims[0] as usize, n_out, nb, n_out * nb * 17, true,
                   "MXFP4, par expert");
    println!("  {}", machine.nom);
    let Some(m) = machine.charger_mxfp4(blocs, n_out, nb) else {
        println!("  allocation GPU impossible"); return;
    };
    let mut ms = f64::MAX;
    let mut dernier: Vec<f32> = Vec::new();
    for passe in 0..3 {
        let t1 = Instant::now();
        let Some(r) = machine.proj_mxfp4(&m, &xi, 1.0) else { println!("  noyau en échec"); return };
        let dt = t1.elapsed().as_secs_f64();
        if passe > 0 && dt < ms { ms = dt; }
        dernier = r;
    }
    let mut echelle = 1e-9f32;
    for o in 0..n_out { echelle = echelle.max(cpu[o].abs()); }
    let mut ecart = 0f32;
    for o in 0..n_out { ecart = ecart.max((dernier[o] - cpu[o]).abs() / echelle); }
    println!("  GPU  warp par ligne : {:>7.1} ms  ({:>6.1} Go/s)  écart max {:+.2e}",
             ms * 1e3, octets as f64 / ms / 1e9, ecart);
    let _ = opt;
}


/// Banc d'essai du noyau **Q4_K** (toute la famille Qwen en Q4_K_M) contre le
/// chemin AVX2 du CPU.
/// Banc du noyau **Q6_K** : c'est le format des têtes liées et de quelques
/// tenseurs des mélanges `Q4_K_M`. Même protocole que les autres bancs — chemin
/// CPU AVX2 en référence, trois passes GPU, écart relatif au maximum des sorties.
fn banc_q6k(opt: Options, g: &Gguf, nom: &str, threads: usize) {
    use std::time::Instant;
    let Some((blocs, nb)) = g.q6k_blocks(nom) else { println!("pas une matrice Q6_K"); return };
    let t = g.tensor(nom).unwrap();
    let (n_out, n_in) = (t.dims[0] as usize, t.dims[1] as usize);
    let octets = n_out * nb * crate::gguf::TAILLE_Q6K;
    println!("matrice Q6_K {nom} : {n_out} × {n_in} · {:.1} Mo · {} super-blocs de 256",
             octets as f64 / 1e6, nb);
    let xi: Vec<i32> = (0..n_in).map(|i| ((i * 2654435761usize) % 255) as i32 - 127).collect();
    let x16: Vec<i16> = xi.iter().map(|&v| v.clamp(-32767, 32767) as i16).collect();
    let d = unsafe { DenseQ4::emprunter_q6k(blocs.as_ptr(), n_out, n_in, nb) };
    let t0 = Instant::now();
    let mut cpu = vec![0f32; n_out];
    let chunk = n_out.div_ceil(threads);
    let dref = &d;
    let xref = &x16;
    std::thread::scope(|sc| {
        for (ci, part) in cpu.chunks_mut(chunk).enumerate() {
            let base = ci * chunk;
            sc.spawn(move || {
                for (j, o) in part.iter_mut().enumerate() {
                    *o = dref.dot16(base + j, xref, &[]);
                }
            });
        }
    });
    let tc = t0.elapsed().as_secs_f64();
    println!("  CPU  {threads} fils : {:>7.1} ms  ({:>6.1} Go/s)", tc * 1e3, octets as f64 / tc / 1e9);
    let Some(machine) = gpu::instance() else { println!("  GPU absent"); return };
    println!("  {}", machine.nom);
    let Some(m) = machine.charger_q6k(blocs, n_out, nb) else {
        println!("  allocation GPU impossible"); return;
    };
    let mut ms = f64::MAX;
    let mut dernier: Vec<f32> = Vec::new();
    for passe in 0..3 {
        let t1 = Instant::now();
        let Some(r) = machine.proj_q6k(&m, &xi, 1.0) else { println!("  noyau en échec"); return };
        let dt = t1.elapsed().as_secs_f64();
        if passe > 0 && dt < ms { ms = dt; }
        dernier = r;
    }
    let mut echelle = 1e-9f32;
    for o in 0..n_out { echelle = echelle.max(cpu[o].abs()); }
    let mut ecart = 0f32;
    for o in 0..n_out { ecart = ecart.max((dernier[o] - cpu[o]).abs() / echelle); }
    println!("  GPU  warp par ligne : {:>7.1} ms  ({:>6.1} Go/s)  écart max {:+.2e}",
             ms * 1e3, octets as f64 / ms / 1e9, ecart);
    let _ = opt;
}

fn banc_q4k(opt: Options, g: &Gguf, nom: &str, threads: usize) {
    use std::time::Instant;
    let Some((blocs, _)) = g.q4k_blocks(nom) else { println!("pas une matrice Q4_K"); return };
    let t = g.tensor(nom).unwrap();
    // UN TENSEUR D'EXPERTS EST 3D, ET `q4k_blocks` NE LE SAIT PAS : il rend
    // `dims[1]/256`, ce qui est juste pour une matrice 2D de projections (`dims[1]`
    // y est `n_in`) et FAUX pour un tenseur d'experts, où `dims[1]` est `n_out` —
    // mesuré : « 128 × 768 · 0,1 Mo · 3 super-blocs » pour un tenseur dont chaque
    // expert fait 0,88 Mo et 8 super-blocs par ligne. Le chemin de PRODUCTION ne
    // s'y trompe pas (`charger_moe` calcule son pas lui-même) ; c'est le banc qui
    // lisait de travers, et il annonçait un débit pour la mauvaise taille.
    let (n_experts, n_out, n_in) = if t.dims.len() >= 3 {
        (t.dims[0] as usize, t.dims[1] as usize, t.dims[2] as usize)
    } else {
        (1usize, t.dims[0] as usize, t.dims[1] as usize)
    };
    let nb = n_in / 256;
    let octets = n_out * nb * 144;
    println!("matrice Q4_K {nom} : {n_out} × {n_in} · {:.1} Mo · {} super-blocs de 256",
             octets as f64 / 1e6, nb);
    let xi: Vec<i32> = (0..n_in).map(|i| ((i * 2654435761usize) % 255) as i32 - 127).collect();
    let x16: Vec<i16> = xi.iter().map(|&v| v.clamp(-32767, 32767) as i16).collect();
    let sx32 = crate::list::sommes32(&x16);
    let d = unsafe { DenseQ4::emprunter_q4k(blocs.as_ptr(), n_out, n_in, nb) };
    let t0 = Instant::now();
    let mut cpu = vec![0f32; n_out];
    let chunk = n_out.div_ceil(threads);
    let dref = &d;
    let (x16ref, sxref) = (&x16, &sx32);
    std::thread::scope(|sc| {
        for (ci, part) in cpu.chunks_mut(chunk).enumerate() {
            let base = ci * chunk;
            sc.spawn(move || {
                for (j, o) in part.iter_mut().enumerate() {
                    *o = dref.dot16(base + j, x16ref, sxref);
                }
            });
        }
    });
    let tc = t0.elapsed().as_secs_f64();
    println!("  CPU  {threads} fils : {:>7.1} ms  ({:>6.1} Go/s)", tc * 1e3, octets as f64 / tc / 1e9);
    let Some(machine) = gpu::instance() else { println!("  GPU absent"); return };
    println!("  {}", machine.nom);
    // Le transfert PAR EXPERT (granularité fine) est mesuré AVANT le reste : c'est lui qui
    // décide si le streaming vaut la peine, et il ne doit pas être noyé dans le noyau.
    if n_experts > 1 {
        banc_transfert(machine, blocs, n_experts, n_out, nb, n_out * nb * 144, false,
                       "Q4_K, par expert");
    }
    let Some(m) = machine.charger_q4k(blocs, n_out, nb) else {
        println!("  allocation GPU impossible"); return;
    };
    let mut ms = f64::MAX;
    let mut dernier: Vec<f32> = Vec::new();
    for passe in 0..3 {
        let t1 = Instant::now();
        let Some(r) = machine.proj_q4k(&m, &xi, 1.0) else { println!("  noyau en échec"); return };
        let dt = t1.elapsed().as_secs_f64();
        if passe > 0 && dt < ms { ms = dt; }
        dernier = r;
    }
    let mut echelle = 1e-9f32;
    for o in 0..n_out { echelle = echelle.max(cpu[o].abs()); }
    let mut ecart = 0f32;
    for o in 0..n_out { ecart = ecart.max((dernier[o] - cpu[o]).abs() / echelle); }
    println!("  GPU  warp par ligne : {:>7.1} ms  ({:>6.1} Go/s)  écart max {:+.2e}",
             ms * 1e3, octets as f64 / ms / 1e9, ecart);
    let _ = opt;
}

fn run_tokenize(opt: Options) {
    let path = &modele_chemin();
    let texte = opt.texte.clone().unwrap_or_default();
    let fichier = opt.fichier.clone().unwrap_or_default();
    let sortie = opt.sortie.clone().unwrap_or_default();
    // En-tête seul : le décodage du vocabulaire n'a pas besoin des poids, et
    // `open` lisait le fichier entier (62 Go pour gpt-oss) à chaque appel.
    // Tolérant au modèle en cours de téléchargement (le vocabulaire vit dans le
    // shard 1) : c'est ce qui permet de vérifier le tokenizer AVANT la fin du
    // transfert — et de comparer à llama.cpp ensuite.
    let g = ouvrir_meta_tolerant(path, "--tokenize");
    let tk = build_tokenizer(&g);
    if !fichier.is_empty() {
        // Encoder un corpus ENTIER avec le tokenizer du modèle : chaque modèle
        // a le sien, et nourrir un modèle avec les identifiants d'un autre
        // donne une perplexité qui ne mesure que l'absurdité de l'entrée.
        let texte = std::fs::read_to_string(&fichier).expect("fichier illisible");
        let ids = tk.encode(&texte);
        let cible = if sortie.is_empty() { format!("{fichier}.ids") } else { sortie };
        let corps: Vec<String> = ids.iter().map(|i| i.to_string()).collect();
        std::fs::write(&cible, corps.join(",")).expect("écriture impossible");
        println!("{} tokens écrits dans {cible} (vocabulaire du modèle : {})",
                 ids.len(), tk.vocab_size());
        // Contrôle de réversibilité : si le texte reconstruit diffère de la
        // source, l'encodage a perdu de l'information — et une perplexité
        // calculée sur ce flux ne mesurerait plus le texte.
        //
        // UNE EXCEPTION, ET UNE SEULE : la convention `add_dummy_prefix` de
        // SentencePiece. `encode` préfixe le texte d'un espace de mot (sinon le
        // premier mot ne se découpe pas comme un mot), `decode` le rend — donc la
        // comparaison stricte signalait « DIVERGE à l'octet 0 » sur tout modèle
        // SPM (Mistral, Codestral, Llama, Gemma) pour **un** espace de
        // convention, noyant le vrai signal. On nomme l'écart au lieu de le
        // tolérer en silence : un octet de plus, en tête, et rien d'autre.
        let retour = tk.decode(&ids);
        let convention_spm = retour.len() == texte.len() + 1
            && retour.starts_with(' ')
            && retour[1..] == texte;
        if retour == texte {
            println!("réversibilité : texte reconstruit identique ✅ ({} octets)", texte.len());
        } else if convention_spm {
            println!("réversibilité : identique, à l'espace de tête de la convention \
SentencePiece près ✅ ({} octets + le préfixe de mot)", texte.len());
        } else {
            let pos = retour.bytes().zip(texte.bytes()).position(|(a, b)| a != b)
                .unwrap_or(retour.len().min(texte.len()));
            println!("réversibilité : DIVERGE à l'octet {pos} — {} vs {} octets",
                     retour.len(), texte.len());
            println!("  source  : {:?}", &texte[pos.saturating_sub(40)..(pos + 40).min(texte.len())]);
            println!("  retour  : {:?}", &retour[pos.saturating_sub(40)..(pos + 40).min(retour.len())]);
        }
        return;
    }
    let ids = tk.encode(&texte);
    println!("{} tokens", ids.len());
    for id in &ids {
        print!("{id} ");
    }
    println!();
    println!("recolle : {:?}", tk.decode(&ids));
}

/// Plan de placement : ce que pèse chaque couche, et où la mettre.
///
/// C'est l'« index » du conteneur : on le lit **avant** les poids, donc on
/// décide sans avoir rien chargé. Les seuils viennent des débits mesurés sur
/// cette machine : CPU 14–25 Go/s, PCIe x8 6,5 Go/s, NVLink 25,78 Go/s,
/// GPU 380 Go/s en lecture locale.
fn run_plan(opt: Options) {
    let path = &modele_chemin();
    let g = Gguf::open_auto(path).expect("ouverture du GGUF");
    let arch = g.meta.get("general.architecture").and_then(|m| m.as_str()).unwrap_or("?");
    let n_layer = g.cfg("block_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
    let n_expert = g.cfg("expert_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
    let n_used = g.cfg("expert_used_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
    // octets par poids, par type ggml
    let octets = |t: u32| -> f64 {
        match t {
            0 => 4.0, 1 => 2.0, 2 => 18.0/32.0, 8 => 34.0/32.0,
            12 => 144.0/256.0, 14 => 210.0/256.0, 39 => 17.0/32.0,
            _ => 4.0,
        }
    };
    println!("plan de placement — {arch}, {n_layer} couches{}",
             if n_expert > 0 { format!(", {n_expert} experts (top-{n_used})") } else { String::new() });
    println!("\n  {:>5}  {:>12}  {:>12}  {:>12}  {:>13}  {}",
             "couche", "attention", "ffn", "experts", "cumul", "placement");
    let mut cumul = 0f64;
    let mut total = 0f64;
    let mut actifs = 0f64;
    for l in 0..n_layer {
        let mut attn = 0f64;
        let mut ffn = 0f64;
        let mut exp = 0f64;
        let mut exp_actif = 0f64;
        for t in &g.tensors {
            let Some(reste) = t.name.strip_prefix(&format!("blk.{l}.")) else { continue };
            let oct = octets(t.ttype) * t.nelem() as f64;
            if reste.starts_with("attn") { attn += oct; }
            else if reste.contains("_exps") {
                exp += oct;
                // un tenseur d'experts est 3D : la part active est
                // n_used / n_expert de son volume
                exp_actif += oct * (n_used as f64 / n_expert.max(1) as f64);
            } else if reste.starts_with("ffn") { ffn += oct; }
        }
        cumul += attn + ffn + exp;
        total += attn + ffn + exp;
        actifs += attn + ffn + exp_actif;
        // Placement : on conseille le GPU seulement quand la couche ne tient
        // pas confortablement, et NVLink quand deux GPU se partagent le modèle.
        let placement = if exp + ffn + attn < 512.0 * 1e6 { "CPU" }
                        else if n_expert > 0 { "CPU (MoE creux)" }
                        else { "GPU (PCIe 6,5 Go/s)" };
        println!("  {:>5}  {:>9.1} Mo  {:>9.1} Mo  {:>9.1} Mo  {:>10.2} Go  {}",
                 l, attn / 1e6, ffn / 1e6, exp / 1e6, cumul / 1e9, placement);
    }
    println!("\n  total du fichier      : {:.2} Go", total / 1e9);
    println!("  lu par jeton (actifs) : {:.2} Go", actifs / 1e9);
    for (nom, debit) in [("CPU 16 fils", 20.0), ("PCIe x8", 6.5), ("NVLink", 25.78), ("GPU local", 380.0)] {
        println!("  à {:>9.1} Go/s ({nom}) : {:>7.2} tok/s", debit, debit / (actifs / 1e9));
    }
    if n_expert > 0 {
        // Mesuré sur le 30B-A3B : les tranches d'experts sont lues à 8 Go/s,
        // pas 20 — dix-huit mille tranches de 900 Ko dispersées sur 18 Go
        // coûtent en TLB et en localité ce que la lecture séquentielle ne paie
        // pas. Le plan doit chiffrer le régime réel, pas le régime idéal.
        println!("  à       8.0 Go/s (MoE épars, mesuré) : {:>7.2} tok/s",
                 8.0 / (actifs / 1e9));
    }
    let libre = std::fs::read_to_string("/proc/meminfo").ok()
        .and_then(|t| t.lines().find(|l| l.starts_with("MemAvailable")).map(|l| l.to_string()))
        .unwrap_or_default();
    println!("  {}", libre.trim());
    println!("  → {}", if total / 1e9 < 100.0 { "le modèle tient en mémoire, sans copie" }
                      else { "le modèle DÉPASSE la mémoire : il faut un découpage par couche" });

    // ------------------------------------------------------- contexte long
    // Le mur du contexte n'est pas le même que celui des poids : le KV croît
    // LINÉAIREMENT avec la longueur et se relit EN ENTIER à chaque jeton. À
    // 1 M, c'est ce trafic qui décide de tout — d'où ce chiffrage, séparé en
    // f32 / int8 / int4 et tenant compte des couches à fenêtre glissante, qui
    // n'ont jamais besoin de plus de `fenetre` entrées.
    let ctx_demande = if opt.ctx_impose && opt.ctx > 0 {
        opt.ctx
    } else {
        // Sans `--ctx`, on chiffre le contexte DÉCLARÉ par le modèle : le défaut
        // 512 du mode masquait les 32 768 de Qwen (relevé par l'audit).
        g.cfg("context_length").and_then(|m| m.as_u64()).unwrap_or(4096) as usize
    };
    let n_kv = g.cfg("attention.head_count_kv").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
    let head_dim = {
        let d = g.cfg("attention.key_length").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
        if d > 0 { d } else {
            let h = g.cfg("embedding_length").and_then(|m| m.as_u64()).unwrap_or(1) as usize;
            let nh = g.cfg("attention.head_count").and_then(|m| m.as_u64()).unwrap_or(1) as usize;
            h / nh.max(1)
        }
    };
    let fenetre = g.cfg("attention.sliding_window").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
    let motif = if fenetre > 0 && arch == "gpt-oss" { 2 } else { 0 };
    let n_fenetrees = if fenetre > 0 && motif > 1 {
        (0..n_layer).filter(|&l| l % motif < motif - 1).count()
    } else if fenetre > 0 { n_layer } else { 0 };
    let n_pleines = n_layer - n_fenetrees;
    println!("\n=== contexte : {} jetons ===", ctx_demande);
    println!("  KV par jeton et par couche : {} têtes KV × {} dim × 2 (K et V)",
             n_kv, head_dim);
    if n_fenetrees > 0 {
        println!("  couches à fenêtre glissante : {n_fenetrees}/{n_layer} \
                  (leur KV s'arrête à {fenetre} entrées) · pleines : {n_pleines}");
    }
    let par_jeton = |b: f64| (n_kv * head_dim) as f64 * b * 2.0;
    for (nom, b) in [("f32", 4.0), ("int8", 1.0), ("int4", 0.5)] {
        let complet = par_jeton(b) * n_layer as f64 * ctx_demande as f64;
        let econome = par_jeton(b) * n_pleines as f64 * ctx_demande as f64
                    + par_jeton(b) * n_fenetrees as f64 * fenetre.min(ctx_demande) as f64;
        println!("  KV {nom:<4} : {:>7.2} Go en attention complète partout · \
                  {:>7.2} Go avec la fenêtre", complet / 1e9, econome / 1e9);
    }
    // Trafic de relecture à chaque jeton : c'est lui qui fixe le débit de
    // décodage, pas les poids.
    let trafic = |b: f64| par_jeton(b) * n_pleines as f64 * ctx_demande as f64
                           + par_jeton(b) * n_fenetrees as f64 * fenetre.min(ctx_demande) as f64;
    print!("  relecture du KV par jeton :");
    for (nom, b) in [("f32", 4.0), ("int8", 1.0), ("int4", 0.5)] {
        print!(" {nom} {:.2} Go ·", trafic(b) / 1e9);
    }
    println!();
    println!("  → décodage (KV seul, poids non compris) :");
    for (nom, debit) in [("RAM 20 Go/s", 20.0), ("PCIe 6,5", 6.5), ("NVLink 25,8", 25.78),
                         ("1 GPU 380", 380.0), ("2 GPU 760", 760.0)] {
        let t = trafic(4.0) / 1e9 / debit;
        let t8 = trafic(1.0) / 1e9 / debit;
        let t4 = trafic(0.5) / 1e9 / debit;
        println!("     {nom:<12} f32 {:>7.1} ms · int8 {:>6.1} ms · int4 {:>6.1} ms par jeton",
                 t * 1e3, t8 * 1e3, t4 * 1e3);
    }
    // Préremplissage : notre moteur traite UN jeton à la fois, donc remplir la
    // fenêtre coûte ce que coûterait la génération de la même longueur.
    let par_jeton_ms = trafic(4.0) / 1e9 / 20.0 * 1e3 + actifs / 1e9 / 8.0 * 1e3;
    let prefill_h = ctx_demande as f64 * par_jeton_ms / 1000.0 / 3600.0;
    println!("  préremplissage SÉQUENTIEL estimé : {:.1} h (le moteur ne fait pas de lot ; \
              l'attention y est en O(N) par jeton)", prefill_h);
    // Portée de la rotation : au-delà de `initial_context_length`, il faut
    // l'étirement — et au-delà de `max_position_embeddings`, plus rien n'est
    // garanti par l'entraînement.
    let initial = g.cfg("rope.scaling.original_context_length").and_then(|m| m.as_u64());
    let facteur = g.cfg("rope.scaling.factor").and_then(|m| m.as_f64());
    let max_pos = g.cfg("context_length").and_then(|m| m.as_u64()).unwrap_or(0);
    println!("  rotation : base {} · initial {} · facteur déclaré {} · max_position_embeddings {}",
             g.cfg("rope.freq_base").and_then(|m| m.as_f64()).unwrap_or(10000.0),
             initial.map(|v| v.to_string()).unwrap_or_else(|| "—".into()),
             facteur.map(|v| format!("×{v}")).unwrap_or_else(|| "—".into()),
             max_pos);
    if ctx_demande as u64 > max_pos && max_pos > 0 {
        println!("  → AU-DELÀ du contexte entraîné : extrapolation, qualité non garantie");
    }
    if let (Some(i), Some(f)) = (initial, facteur) {
        let couvert = i as f64 * f;
        println!("  → YaRN couvre {} jetons ({i} × {f}) ; à {ctx_demande}, il faudrait un facteur ×{:.0}",
                 couvert as u64, ctx_demande as f64 / i as f64);
    }
}

/// Construit les fenêtres de perplexité en **format harmony** (gpt-oss).
///
/// Le texte est le même qu'en mode brut, au découpage près : seuls les
/// marqueurs de tour changent. C'est la façon la plus directe de tester
/// l'hypothèse « le modèle est décalibré hors de son gabarit » sans toucher aux
/// poids — si la perplexité s'effondre, c'est l'habillage qui était en cause,
/// pas le calcul.
///
/// Seuls les jetons de contenu sont notés (`masque[i] = true`) : prédire
/// `<|end|>` ou `<|start|>` mesure la familiarité du gabarit, pas la qualité du
/// modèle sur le texte. Le premier jeton d'un message, lui, EST noté : il est
/// prédit après `<|message|>`, ce qui est exactement la tâche posée.
///
/// `mode` : `alterne` (user/assistant), `assistant` (tout en canal final),
/// `user` (tout en rôle user), `suite` (une consigne courte en rôle user, puis
/// le texte entier en canal assistant — la présentation la plus proche de
/// l'usage réel : le modèle *écrit* le texte).
fn fenetres_harmony(tk: &tokenizer::Tokenizer, ids: &[u32], ctx: usize, mode: &str,
                    contexte: Option<&str>)
    -> Vec<(Vec<u32>, Vec<bool>)>
{
    let deb = tk.special_id("<|start|>").expect("<|start|> absent du vocabulaire");
    let msg = tk.special_id("<|message|>").expect("<|message|> absent du vocabulaire");
    let fin = tk.special_id("<|end|>").expect("<|end|> absent du vocabulaire");
    let canal = tk.special_id("<|channel|>");
    // Préambule système, identique à celui de l'inférence : c'est le gabarit
    // réellement utilisé par le modèle en conversation.
    let systeme = {
        let mut v = vec![deb];
        v.extend(tk.encode("system"));
        v.push(msg);
        v.extend(tk.encode("You are a helpful assistant."));
        v.push(fin);
        v
    };
    let entete = |role: &str| -> Vec<u32> {
        let mut v = vec![deb];
        v.extend(tk.encode(role));
        // Un tour d'assistant porte son canal avant le message.
        if role == "assistant" {
            if let Some(c) = canal { v.push(c); }
            v.extend(tk.encode("final"));
        }
        v.push(msg);
        v
    };
    let mut fenetres = Vec::new();
    // ---------------------------------------------------------------- suite
    // Le texte est la RÉPONSE : consigne courte, puis le texte en canal
    // assistant final. C'est le seul montage où le modèle est dans la position
    // exacte qu'il a apprise (écrire de la prose après une demande).
    if mode == "suite" {
        let consigne = {
            let mut v = systeme.clone();
            v.extend(entete("user"));
            // Le contexte (si fourni) remplace la consigne générique : c'est le
            // seul montage où le modèle *continue* un texte qu'il a sous les
            // yeux, donc le seul où sa perplexité est comparable à celle du mode
            // brut sans lui demander de deviner le texte à l'aveugle.
            match contexte {
                Some(c) => v.extend(tk.encode(c)),
                None => v.extend(tk.encode("Continue the text below, reproducing it exactly.")),
            }
            v.push(fin);
            v
        };
        let tete = entete("assistant");
        let budget = ctx.saturating_sub(consigne.len() + tete.len() + 1).max(16);
        let mut i = 0usize;
        while i < ids.len() {
            let n = budget.min(ids.len() - i);
            let mut w = consigne.clone();
            let mut m = vec![false; consigne.len()];
            w.extend_from_slice(&tete);
            m.extend(std::iter::repeat(false).take(tete.len()));
            w.extend_from_slice(&ids[i..i + n]);
            m.extend(std::iter::repeat(true).take(n));
            w.push(fin);
            m.push(false);
            fenetres.push((w, m));
            i += n;
        }
        if std::env::var("DRAVE_HARMONY_TRACE").is_ok() {
            for (i, (w, m)) in fenetres.iter().enumerate() {
                let apercu: String = tk.decode(w).chars().take(110).collect();
                eprintln!("[harmony] fenêtre {} : {} jetons, {} notés · |{}|",
                          i + 1, w.len(), m.iter().filter(|&&b| b).count(), apercu);
            }
        }
        return fenetres;
    }
    // Deux messages par fenêtre, pour que la conversation ressemble à une
    // conversation et non à un seul tour monstre. La marge de 16 couvre les
    // en-têtes (`<|start|>` + rôle + `<|channel|>final` + `<|message|>`) et le
    // `<|end|>` : sans elle, le second message ne tenait jamais et chaque
    // fenêtre se réduisait à UN tour — ce que la première mesure a montré.
    let piece = ((ctx.saturating_sub(systeme.len() + 16)) / 2).max(16);
    let mut cur = systeme.clone();
    let mut masque = vec![false; systeme.len()];
    let (mut i, mut tour) = (0usize, 0usize);
    while i < ids.len() {
        let role = match mode {
            "assistant" => "assistant",
            "user" => "user",
            _ => if tour % 2 == 0 { "user" } else { "assistant" },
        };
        let e = entete(role);
        let n = piece.min(ids.len() - i);
        // Fenêtre pleine : on la ferme AVANT d'ajouter un tour qui déborderait.
        if cur.len() + e.len() + n + 1 > ctx && cur.len() > systeme.len() {
            fenetres.push((std::mem::take(&mut cur), std::mem::take(&mut masque)));
            cur = systeme.clone();
            masque = vec![false; systeme.len()];
        }
        cur.extend_from_slice(&e);
        masque.extend(std::iter::repeat(false).take(e.len()));
        cur.extend_from_slice(&ids[i..i + n]);
        masque.extend(std::iter::repeat(true).take(n));
        cur.push(fin);
        masque.push(false);
        i += n;
        tour += 1;
    }
    if cur.len() > systeme.len() { fenetres.push((cur, masque)); }
    // Trace : sans elle, on ne sait pas ce qui a RÉELLEMENT été présenté au
    // modèle (les identifiants spéciaux sont insérés à la main, une erreur
    // d'ordre ne se voit nulle part ailleurs).
    if std::env::var("DRAVE_HARMONY_TRACE").is_ok() {
        for (i, (w, m)) in fenetres.iter().enumerate() {
            let apercu: String = tk.decode(w).chars().take(110).collect();
            eprintln!("[harmony] fenêtre {} : {} jetons, {} notés · |{}|",
                      i + 1, w.len(), m.iter().filter(|&&b| b).count(), apercu);
        }
    }
    fenetres
}

/// L'indice de la plus grande valeur. Les égalités sont départagées par l'indice le
/// plus PETIT : sans cela, deux exécutions pourraient rendre deux jetons différents
/// pour deux logits exactement égaux, et la mesure d'accord porterait sur ce hasard.
fn argmax(valeurs: &[f32]) -> u32 {
    let mut best = 0usize;
    for (i, v) in valeurs.iter().enumerate() {
        if *v > valeurs[best] { best = i; }
    }
    best as u32
}

/// L'indice du maximum et les cinq meilleurs — l'accord « top-5 » dit si la bonne
/// réponse était dans le voisinage immédiat du réflexe, ce qui n'est pas la même
/// chose que de la donner du premier coup.
fn argmax_et_top5(valeurs: &[f32]) -> (u32, Vec<u32>) {
    let mut idx: Vec<u32> = (0..valeurs.len() as u32).collect();
    idx.sort_by(|&a, &b| valeurs[b as usize].partial_cmp(&valeurs[a as usize])
                         .unwrap_or(std::cmp::Ordering::Equal).then(a.cmp(&b)));
    idx.truncate(5);
    (idx[0], idx)
}

/// C8 : le RÉFLEXE, mesuré comme une sortie précoce.
///
/// POURQUOI CETTE FORME. Un réflexe médullaire ne remonte pas au cortex : il répond
/// par un chemin COURT, et il répond bien pour un stimulus stéréotypé. Dans le
/// moteur, ce chemin court existe déjà — `--couches 0,L` tronque le modèle et
/// `--tete-partielle` applique la tête à la fin de la plage. La question mesurable
/// n'est donc pas « peut-on faire un réflexe ? » mais **« à partir de quelle
/// profondeur un réflexe tombe-t-il d'accord avec le modèle entier ? »**, et c'est
/// une courbe accord ↔ profondeur.
///
/// CE QU'ELLE SERT À DIRE, ET CE QU'ELLE NE DIT PAS. Elle dit à quelle profondeur
/// l'information décidée est déjà là — utile pour un chemin rapide, pour un premier
/// avis, ou pour distribuer le travail. Elle ne dit PAS que le réflexe est aussi
/// BON : un accord élevé sur le jeton le plus probable ne dit rien de la
/// distribution entière, et la perplexité d'un modèle tronqué n'est pas mesurée ici.
fn run_reflexe_essai(opt: Options) {
    let path = modele_chemin();
    let n = opt.reflexe_essai;
    let idfile = opt.ids_file.clone().unwrap_or_default();
    if idfile.is_empty() {
        eprintln!("--reflexe-essai a besoin de --ids-file : le réflexe se mesure sur un texte réel, pas sur des jetons inventés.");
        std::process::exit(2);
    }
    let brut = std::fs::read_to_string(&idfile).expect("fichier d'identifiants illisible");
    let ids: Vec<u32> = brut.split(|c: char| c == ',' || c.is_whitespace())
        .filter(|s| !s.is_empty()).filter_map(|s| s.parse().ok()).take(n).collect();
    if ids.len() < 4 {
        eprintln!("--reflexe-essai : {} jetons seulement — il en faut au moins 4", ids.len());
        std::process::exit(2);
    }
    let cpu = engine::coeurs_physiques();
    let n_threads = if opt.threads_impose { opt.threads } else { cpu.max(1) };
    let ctx = if opt.ctx_impose { opt.ctx } else { (ids.len() + 8).max(256) };
    let t0 = std::time::Instant::now();
    let mut mdl = model::Model::load_partiel(&path, ctx, n_threads, false, 1.0, false, 0, 0, None);
    let n_layer = mdl.cfg.n_layer;
    println!("  modèle            : {path} · {n_layer} couches · {} jetons", ids.len());
    // Le modèle ENTIER : c'est la référence, et la même fonction sert au réflexe le
    // plus profond — sinon la comparaison porterait sur deux calculs différents.
    let mut reference: Vec<u32> = Vec::with_capacity(ids.len());
    // Les états du modèle entier sont gardés : sans eux, l'échec d'un réflexe serait
    // constaté sans être expliqué, et « 0 % d'accord » ne dit pas si le réflexe se
    // trompe de peu ou s'il calcule autre chose.
    let mut etats_entiers: Vec<Vec<f32>> = Vec::with_capacity(ids.len());
    let mut t_entier = 0.0f64;
    for (pos, &t) in ids.iter().enumerate() {
        let h0 = std::time::Instant::now();
        let h = mdl.forward(t, pos);
        t_entier += h0.elapsed().as_secs_f64();
        reference.push(argmax(&mdl.logits(&h)));
        etats_entiers.push(h);
    }
    let cos = |a: &[f32], b: &[f32]| -> f64 {
        let (mut p, mut na, mut nb) = (0.0f64, 0.0f64, 0.0f64);
        for (x, y) in a.iter().zip(b.iter()) {
            p += *x as f64 * *y as f64; na += (*x as f64).powi(2); nb += (*y as f64).powi(2);
        }
        if na <= 0.0 || nb <= 0.0 { return 0.0; }
        p / (na.sqrt() * nb.sqrt())
    };
    println!("  référence         : modèle entier, {:.1} ms par jeton",
             1000.0 * t_entier / ids.len() as f64);
    println!();
    println!("  {:>9}  {:>10}  {:>12}  {:>10}  {:>14}  {:>12}", "couches", "accord",
             "accord top-5", "cos(final)", "ms/jeton", "temps/entier");
    // Les profondeurs mesurées : on va jusqu'à la DERNIÈRE, parce qu'un réflexe aussi
    // profond que le modèle DOIT être le modèle — c'est l'invariant de ce mode.
    let mut profondeurs: Vec<usize> = vec![1, 2, 4, 6, 8, 12, 16, 20, 24, 32]
        .into_iter().filter(|l| *l < n_layer).collect();
    profondeurs.push(n_layer);
    let mut mesures: Vec<(usize, f64)> = Vec::new();
    for l in profondeurs {
        let mut m = model::Model::load_partiel(&path, ctx, n_threads, false, 1.0, false, 0, 0,
                                               Some((0, l)));
        poser_tete_partielle(&mut m);
        let mut accord = 0usize; let mut accord5 = 0usize; let mut t_refl = 0.0f64;
        let mut cumul_cos = 0.0f64;
        for (pos, &t) in ids.iter().enumerate() {
            let h0 = std::time::Instant::now();
            let h = m.forward(t, pos);
            t_refl += h0.elapsed().as_secs_f64();
            // La COSINUS entre l'état tronqué et l'état final dit si le réflexe se
            // trompe de peu ou s'il calcule dans une autre direction — deux échecs
            // qui n'appellent pas la même conclusion.
            cumul_cos += cos(&h, &etats_entiers[pos]);
            let lg = m.logits(&h);
            let (a, c5) = argmax_et_top5(&lg);
            if a == reference[pos] { accord += 1; }
            if c5.contains(&reference[pos]) { accord5 += 1; }
        }
        let pa = 100.0 * accord as f64 / ids.len() as f64;
        let p5 = 100.0 * accord5 as f64 / ids.len() as f64;
        let ms = 1000.0 * t_refl / ids.len() as f64;
        println!("  {l:>9}  {pa:>9.1} %  {p5:>11.1} %  {:>9.3}  {ms:>13.1}  {:>11.2}×",
                 cumul_cos / ids.len() as f64, t_entier / t_refl);
        mesures.push((l, pa));
    }
    println!();
    println!("  ce que la courbe ne dit PAS : la sortie précoce est mesurée SANS tête dédiée — la tête du modèle est celle de sa DERNIÈRE couche, et rien ne dit qu'elle lit un état intermédiaire. Une tête entraînée pour la couche L changerait la réponse, et n'est pas mesurée ici. Et l'accord porte sur le jeton de plus forte probabilité. Un réflexe d'accord élevé peut être très mal calibré (distribution entière différente), et la perplexité d'un modèle tronqué n'est pas mesurée ici.");
    let (lf, pf) = *mesures.last().unwrap();
    if (pf - 100.0).abs() > 1e-9 && lf == n_layer {
        eprintln!("  ❌ un réflexe aussi profond que le modèle ({lf} couches) donne {pf:.1} % d'accord au lieu de 100 % : la troncature ne rend pas le modèle entier");
        std::process::exit(1);
    }
    println!("  temps total       : {:.1} s", t0.elapsed().as_secs_f64());
}

/// C6 : mémoire épisodique sur des états RÉELS du modèle.
///
/// POURQUOI UN ESSAI PLUTÔT QU'UN TEST UNITAIRES. Les tests du module montrent que
/// la mécanique est juste sur des vecteurs tirés au hasard ; ils ne disent RIEN de
/// ce qui compte : les états d'un vrai modèle sont-ils assez **séparables** pour
/// qu'une clé creuse les distingue ? Un état de langue naturelle n'est pas un
/// vecteur aléatoire — il vit sur une variété de petite dimension, et c'est
/// précisément là que la séparation de motifs peut échouer. Le seul moyen de le
/// savoir est de le mesurer sur les états du modèle, et c'est ce que fait cet essai.
///
/// CE QUI EST MESURÉ, ET CONTRE QUOI. Le rappel est comparé à la **ligne de base
/// nulle** (1/N : le hasard) — sans elle, « 60 % de rappel » ne dit pas si la
/// mémoire sert à quelque chose. Et le coût est celui qui est **payé** (candidats
/// examinés, comparaisons), pas une estimation.
///
/// LA DÉGRADATION DE L'INDICE est un sous-ensemble **déterministe** des canaux de la
/// clé (un hachage du numéro de canal), jamais « les premiers » : prendre les
/// premiers canaux corrélerait la dégradation avec l'ordre des indices, et les
/// canaux de plus grande amplitude ne sont pas répartis au hasard dans l'état.
fn run_episodique_essai(opt: Options) {
    let path = modele_chemin();
    let n_voulu = opt.episodique_essai;
    let k = opt.episodique_k;
    let pas = opt.episodique_pas.max(1);
    let cpu = engine::coeurs_physiques();
    let n_threads = if opt.threads_impose { opt.threads } else { cpu.max(1) };
    // DEUX SOURCES D'ÉPISODES : un fichier d'identifiants (donc UN texte), ou
    // PLUSIEURS documents en texte brut, chacun repartant d'un **cache neuf**.
    // La seconde existe pour lever une condition précise : toutes les premières
    // mesures portaient sur 300 états consécutifs d'un même texte. Un magasin qui ne
    // fonctionne que sur un seul document ne serait pas une mémoire — ce serait un
    // index.
    let documents: Vec<String> = opt.episodique_textes.as_ref().map(|l| {
        l.split(',').map(|s| s.trim().to_string()).filter(|s| !s.is_empty()).collect()
    }).unwrap_or_default();
    let idfile = opt.ids_file.clone().unwrap_or_default();
    if documents.is_empty() && idfile.is_empty() {
        eprintln!("--episodique-essai a besoin de --ids-file ou de --episodique-textes : les \
épisodes sont des états RÉELS du modèle sur un texte, pas des vecteurs de synthèse.");
        std::process::exit(2);
    }
    // Par document, on calcule `par_document × pas` jetons et on garde un état sur
    // `pas` : les positions doivent rester celles du texte (RoPE en dépend), donc on
    // paie les jetons intermédiaires.
    let par_document = if documents.is_empty() { 0 } else {
        (n_voulu / documents.len()).max(2)
    };
    let t0 = std::time::Instant::now();
    let mut etats: Vec<Vec<f32>> = Vec::with_capacity(n_voulu + 8);
    let mut dim = 0usize;
    // Le nombre de jetons RÉELLEMENT calculés : c'est lui qui explique le temps, et
    // il vaut `états × pas` — sauf quand un document est plus court que demandé.
    let mut jetons_calcules = 0usize;
    if documents.is_empty() {
        let brut = std::fs::read_to_string(&idfile).expect("fichier d'identifiants illisible");
        let ids: Vec<u32> = brut.split(|c: char| c == ',' || c.is_whitespace())
            .filter(|s| !s.is_empty()).filter_map(|s| s.parse().ok())
            .take(n_voulu.saturating_mul(pas)).collect();
        if ids.len() < 2 {
            eprintln!("--episodique-essai : {} jetons seulement dans {idfile} — il en faut au \
moins 2", ids.len());
            std::process::exit(2);
        }
        let ctx = if opt.ctx_impose { opt.ctx } else { (ids.len() + 8).max(256) };
        let mut mdl = model::Model::load_partiel(&path, ctx, n_threads, false, 1.0, false, 0, 0,
                                                 None);
        jetons_calcules = ids.len();
        for (pos, id) in ids.iter().enumerate() {
            let s = mdl.forward(*id, pos);
            if pos % pas == 0 { etats.push(s); }
        }
        dim = etats[0].len();
    } else {
        for (d, doc) in documents.iter().enumerate() {
            let ctx = if opt.ctx_impose { opt.ctx } else { (par_document * pas + 8).max(256) };
            let mut mdl = model::Model::load_partiel(&path, ctx, n_threads, false, 1.0, false,
                                                     0, 0, None);
            let brut = std::fs::read_to_string(doc)
                .unwrap_or_else(|e| { eprintln!("--episodique-textes : {doc} illisible : {e}");
                                      std::process::exit(2) });
            let tk = build_tokenizer(&mdl.g);
            let mut ids = tk.encode(&brut);
            ids.truncate(par_document * pas);
            let mut n = 0usize;
            jetons_calcules += ids.len();
            for (pos, id) in ids.iter().enumerate() {
                let s = mdl.forward(*id, pos);
                if pos % pas == 0 { etats.push(s); n += 1; }
            }
            if dim == 0 && !etats.is_empty() { dim = etats[0].len(); }
            println!("  document {} de {} : {} jetons calculés, {n} états", d + 1,
                     documents.len(), ids.len());
        }
    }
    if etats.len() < 2 {
        eprintln!("--episodique-essai : {} états seulement — il en faut au moins 2", etats.len());
        std::process::exit(2);
    }
    // DÉCORRÉLATION (facultative) : retirer la moyenne des états. Ce n'est pas un
    // détail de mise en forme — c'est le geste de séparation de motifs du gyrus
    // denté, et il a une raison mesurable ici : deux états différents d'un modèle de
    // langue partagent ~37 % de leur clé, très au-dessus du hasard (k²/dim = 4,6/64),
    // parce qu'ils portent tous une forte composante commune. Tant qu'elle est là,
    // toute clé recouvre tout le magasin et l'index inversé n'élague rien.
    // La moyenne est GARDÉE : sans elle, impossible de reconstruire l'état d'un moment
    // vécu à partir d'une valeur décorrélée — et c'est exactement ce qu'il faut pour
    // injecter un épisode retrouvé.
    let mut moyenne_etats: Option<Vec<f32>> = None;
    if opt.episodique_decorreler && etats.len() > 1 {
        let mut moy = vec![0.0f64; dim];
        for e in etats.iter() { for (i, x) in e.iter().enumerate() { moy[i] += *x as f64; } }
        let n = etats.len() as f64;
        for m in moy.iter_mut() { *m /= n; }
        for e in etats.iter_mut() { for (i, x) in e.iter_mut().enumerate() { *x -= moy[i] as f32; } }
        moyenne_etats = Some(moy.iter().map(|x| *x as f32).collect());
        println!("  décorrélation     : moyenne des {} états retirée (les valeurs stockées sont \
donc les états centrés ; la moyenne est GARDÉE en mémoire pour reconstruire un état vécu)", etats.len());
    }
    // EXPANSION (facultative), après la décorrélation : elle dilate l'état dans un
    // espace plus grand où les clés peuvent être plus creuses — c'est ce qui donne à
    // l'index inversé une chance d'éluder. Mesuré : sans elle, 300 candidats sur 300.
    // LES CLÉS SONT SÉPARÉES DES VALEURS : la clé peut vivre dans un espace dilaté
    // et égalisé, la valeur reste l'état exact du modèle. C'est ce qui permet de
    // dilater sans perdre l'état — et de rendre, à la lecture, l'état d'origine.
    let mut cles: Vec<Vec<f32>> = etats.clone();
    let mut dim_cle = dim;
    if opt.episodique_expansion > 0 {
        let d = opt.episodique_expansion;
        let c = opt.episodique_connexions;
        cles = cles.iter().map(|e| episodique::expandre(e, d, c)).collect();
        dim_cle = d;
        println!("  expansion         : {dim} → {d} canaux de clé ({c} entrées par canal, signes \
par hachage) ; les VALEURS restent les états exacts de dimension {dim}", dim = dim);
    }
    // ÉGALISATION DE L'USAGE DES CANAUX. Un k-WTA choisit les plus grandes
    // amplitudes : si un canal est systématiquement grand (parce que la projection
    // l'a rendu sensible à une direction commune), il entre dans presque toutes les
    // clés et sa liste d'index devient un « hub » — l'index ne peut plus éluder.
    // Centrer et réduire PAR CANAL retire cet avantage. Les statistiques viennent du
    // magasin : en déploiement, elles se stockent avec lui (et il faut alors les
    // recalculer quand le magasin grandit — ce n'est pas mesuré ici).
    if opt.episodique_normaliser && cles.len() > 1 {
        let mut moy = vec![0.0f64; dim_cle];
        let mut var = vec![0.0f64; dim_cle];
        for e in cles.iter() { for (i, x) in e.iter().enumerate() { moy[i] += *x as f64; } }
        let n = cles.len() as f64;
        for m in moy.iter_mut() { *m /= n; }
        for e in cles.iter() {
            for (i, x) in e.iter().enumerate() { let d = *x as f64 - moy[i]; var[i] += d * d; }
        }
        let mut ecarts = vec![1.0f32; dim_cle];
        let mut nuls = 0usize;
        for i in 0..dim_cle {
            let v = (var[i] / n).sqrt();
            if v > 1e-12 { ecarts[i] = v as f32; } else { nuls += 1; }
        }
        for e in cles.iter_mut() {
            for (i, x) in e.iter_mut().enumerate() { *x = (*x - moy[i] as f32) / ecarts[i]; }
        }
        println!("  égalisation       : chaque canal de clé centré et réduit sur le magasin\
{} — un canal systématiquement grand n'entre plus dans toutes les clés",
                 if nuls > 0 { format!(" ({nuls} canal(aux) de variance nulle laissés tels quels)") }
                 else { String::new() });
    }
    // LA FENÊTRE : la clé d'un épisode est formée sur la MOYENNE de W positions voisines.
    // `cles` est l'espace des clés (les valeurs vivent dans `etats`, intactes) : on le
    // transforme donc EN PLACE, et tout ce qui suit — écriture, lecture, séparation,
    // courbes — emploie la même clé. C'est la définition même de ce qu'on mesure.
    if opt.episodique_fenetre > 1 {
        let w = opt.episodique_fenetre;
        let n = cles.len();
        let mut lisse: Vec<Vec<f32>> = Vec::with_capacity(n);
        for i in 0..n {
            let fin = (i + w).min(n);
            let m = (fin - i) as f32;
            let mut acc = vec![0.0f32; cles[i].len()];
            for j in i..fin {
                for (x, y) in acc.iter_mut().zip(cles[j].iter()) { *x += y / m; }
            }
            lisse.push(acc);
        }
        cles = lisse;
        println!("  fenêtre de clé    : {w} positions — la clé est le k-WTA de la MOYENNE de \
{w} états voisins, ce qui doit LISSER l'hypersensibilité mesurée (deux jetons voisins \
donnaient 1 006 et 50 jetons)");
    }

    // Le coût de l'expansion, dit en clair : c'est ce qu'on paie PAR LECTURE, et il
    // ne dépend pas de la taille du magasin — alors que le balayage qu'elle évite,
    // lui, croît avec N. Le seuil de rentabilité se calcule.
    if opt.episodique_expansion > 0 {
        let cout = (opt.episodique_expansion * opt.episodique_connexions) as f64;
        let seuil = cout / k as f64;
        println!("  coût de l'expansion : {:.0} additions par lecture (fixe) · le balayage \
évité coûte N × {k} comparaisons · l'expansion est donc rentable au-delà de N ≈ {seuil:.0} \
épisodes — EN DESSOUS, le balayage complet est MOINS cher", cout);
    }
    println!("  modèle            : {path}");
    println!("  épisodes          : {} états réels de dimension {dim} ({} en {:.1} s)",
             etats.len(),
             if documents.is_empty() { idfile.clone() } else { format!("{} documents", documents.len()) },
             t0.elapsed().as_secs_f64());
    if pas > 1 {
        println!("  espacement        : un état tous les {pas} jetons — {} jetons calculés pour \
{} épisodes : des moments ÉLOIGNÉS du texte, donc des contenus moins corrélés que des états \
consécutifs", jetons_calcules, etats.len());
    }
    println!("  clé               : {k} canaux sur {dim_cle} (densité {:.2} %), valeurs de \
dimension {dim}", 100.0 * k as f64 / dim_cle as f64);

    // --- 0. COLLISIONS DE CLÉS, mesurées AVANT le round-trip parce qu'elles
    // l'expliquent. Deux états distincts qui ont la MÊME clé sont indiscernables :
    // aucune lecture, si savante soit-elle, ne peut rendre les deux. Le round-trip
    // exact n'est donc possible que si les clés sont deux à deux distinctes — ce
    // n'est pas une propriété du code, c'est une propriété du COUPLE (données, k),
    // et c'est pour cela qu'elle se mesure.
    let mut vues: std::collections::BTreeMap<Vec<u32>, usize> = std::collections::BTreeMap::new();
    for e in cles.iter() { *vues.entry(episodique::cle(e, k)).or_insert(0) += 1; }
    let multiples: usize = vues.values().filter(|m| **m > 1).map(|m| m - 1).sum();
    let pire_cle = vues.values().cloned().max().unwrap_or(0);
    println!("  clés distinctes   : {}/{} (pire multiplicité {pire_cle}){}", vues.len(),
             etats.len(),
             if multiples > 0 { format!(" — {multiples} état(s) partagent la clé d'un autre, \
donc INDISCERNABLES par le contenu") } else { String::new() });

    // --- 1. round-trip : la même clé doit rendre la valeur écrite, AU BIT PRÈS
    let mut m = episodique::Episodique::nouveau(k, dim);
    for (i, e) in etats.iter().enumerate() {
        m.ecrire_avec_cle("local", i as u32, &cles[i], e, trace_globale::maintenant());
    }
    let mut exacts = 0usize;
    for (i, e) in cles.iter().enumerate() {
        if let Some(l) = m.lire(e) {
            if l.id == i as u64
               && m.par_id(l.id).map(|x| x.valeur == etats[i]).unwrap_or(false) {
                exacts += 1;
            }
        }
    }
    let manquants = etats.len() - exacts;
    println!("  round-trip        : {exacts}/{} épisodes relus AU BIT PRÈS avec leur propre clé",
             etats.len());
    if manquants > 0 {
        let par_collision = manquants.min(multiples);
        println!("  échecs expliqués  : {par_collision} par COLLISION de clés (deux états \
indiscernables), {} par ÉGALITÉ de recouvrement (clés distinctes, même nombre de canaux \
partagés — départagées par l'identifiant le plus petit)", manquants - par_collision);
    }

    // --- 2. séparation : recouvrement entre clés d'états DIFFÉRENTS
    let mut paires = 0usize; let mut cumul = 0usize; let mut pire = 0usize;
    let pas = (etats.len() / 64).max(1);
    let mut i = 0;
    while i + pas < etats.len() {
        let r = m.recouvrement_deux(&cles[i], &cles[i + pas]);
        cumul += r; pire = pire.max(r); paires += 1;
        i += pas;
    }
    println!("  séparation        : recouvrement moyen {:.2}/{k} entre états différents \
(pire {pire}/{k}, {paires} paires)",
             if paires > 0 { cumul as f64 / paires as f64 } else { 0.0 });

    // --- 2bis. LA DISTRIBUTION DES LISTES DE L'INDEX.
    // C'est elle qui décide si l'index peut éluder : quelques canaux qui portent
    // presque tout le magasin (des « hubs ») et l'élagage disparaît, quelle que soit
    // la séparation par ailleurs.
    {
        let (moy, maxi, part) = m.listes_canaux();
        println!("  listes de l'index : {:.1} épisodes par canal en moyenne, {maxi} au plus ; \
les 1 % de canaux les plus longs portent {:.0} % des entrées", moy, 100.0 * part);
        if maxi as f64 > 4.0 * moy.max(1.0) {
            println!("  ⚠️  canaux HUB : le plus long porte {:.0}× la moyenne — l'index ne peut \
pas éluder par eux", maxi as f64 / moy.max(1.0));
        }
    }

    // --- 3. le fichier : écrit puis relu, et le rappel doit être identique
    if let Some(f) = &opt.episodique_fichier {
        match m.ecrire_fichier(f) {
            Ok(()) => match episodique::Episodique::lire_fichier(f) {
                Ok(relu) => {
                    let mut identiques = 0usize;
                    for (i, e) in cles.iter().enumerate() {
                        let avant = m.lire(e).map(|l| l.id);
                        let apres = relu.lire(e).map(|l| l.id);
                        if avant == apres && avant == Some(i as u64) { identiques += 1; }
                    }
                    println!("  fichier           : {f} → relu, {identiques}/{} lectures \
identiques après passage par le disque", etats.len());
                }
                Err(e) => { eprintln!("  {e}"); std::process::exit(2); }
            },
            Err(e) => { eprintln!("  épisodique : écriture de {f} impossible : {e}"); std::process::exit(2); }
        }
    }

    // --- 3bis. NOUVEAUTÉ : le magasin sait-il dire « je ne connais pas ça » ?
    //
    // POURQUOI C'EST LA QUESTION LA PLUS IMPORTANTE DU MODULE. Un magasin qui rend
    // toujours son meilleur candidat a l'air de marcher — il rend un épisode à chaque
    // lecture. Ce qui décide de son utilité, c'est de savoir REFUSER : un indice
    // jamais écrit doit donner un moins bon recouvrement qu'un indice écrit, sinon la
    // mémoire ne distingue pas « je me souviens » de « ça ressemble ». On garde donc
    // les derniers 20 % des états HORS du magasin, et on confronte les deux
    // distributions.
    let coupe = (etats.len() * 4) / 5;
    if coupe >= 2 && etats.len() - coupe >= 2 {
        let mut connus = episodique::Episodique::nouveau(k, dim);
        for (i, e) in etats.iter().enumerate().take(coupe) {
            connus.ecrire_avec_cle("local", i as u32, &cles[i], e, 0.0);
        }
        let mut rec_connu = 0usize; let mut n_connu = 0usize;
        for e in cles.iter().take(coupe) {
            if let Some(l) = connus.lire(e) { rec_connu += l.recouvrement; n_connu += 1; }
        }
        let mut rec_nouveau = 0usize; let mut n_nouveau = 0usize; let mut pire_nouveau = 0usize;
        for e in cles.iter().skip(coupe) {
            if let Some(l) = connus.lire(e) {
                rec_nouveau += l.recouvrement; pire_nouveau = pire_nouveau.max(l.recouvrement);
                n_nouveau += 1;
            }
        }
        if n_connu > 0 && n_nouveau > 0 {
            let mc = rec_connu as f64 / n_connu as f64;
            let mn = rec_nouveau as f64 / n_nouveau as f64;
            println!("  nouveauté         : recouvrement moyen {mc:.1}/{k} pour un épisode \
CONNU, {mn:.1}/{k} pour un épisode JAMAIS écrit (pire des nouveaux : {pire_nouveau}/{k})");
            if mn >= mc {
                println!("  ⚠️  un indice jamais écrit obtient un recouvrement AUSSI BON qu'un \
indice connu : ce magasin ne sait pas refuser, il rend toujours son meilleur candidat.");
            }
        }
    }

    // --- 4. LA COURBE : rappel selon le nombre d'épisodes et la dégradation
    println!();
    println!("  rappel par contenu (ligne de base nulle entre parenthèses, Δ = erreur MOYENNE");
    println!("  en jetons entre l'épisode rendu et l'épisode interrogé) :");
    println!("  {:>7}  {:>10}  {:>10}  {:>10}  {:>10}  {:>10}", "N", "indice 0 %", "10 %",
             "25 %", "50 %", "75 %");
    let tailles: Vec<usize> = {
        let mut v: Vec<usize> = [10usize, 40, 160, 640, 2560].iter().cloned()
            .filter(|t| *t <= etats.len()).collect();
        if !v.contains(&etats.len()) { v.push(etats.len()); }
        v
    };
    for taille in tailles {
        let mut s = episodique::Episodique::nouveau(k, dim);
        for (i, e) in etats.iter().enumerate().take(taille) {
            s.ecrire_avec_cle("local", i as u32, &cles[i], e, 0.0);
        }
        let mut ligne = format!("  {taille:>7}");
        for frac in [0.0f64, 0.10, 0.25, 0.50, 0.75] {
            let mut succes = 0usize; let mut essais = 0usize;
            let mut cand = 0usize; let mut comp = 0usize;
            // L'ERREUR EN JETONS. Savoir si la mémoire rend l'épisode EXACT est une
            // chose ; savoir à quelle DISTANCE elle se trompe en est une autre, et
            // c'est celle qui décide de l'usage : un épisode voisin de trois jetons
            // situe le passage, un épisode à cinq cents jetons ne situe rien. Les
            // épisodes sont numérotés dans l'ordre du texte, donc la distance entre
            // identifiants EST une distance en jetons.
            let mut distance = 0usize;
            for q in 0..taille {
                let cible = episodique::cle(&cles[q], k);
                let mut indice = cles[q].clone();
                for c in cible.iter() {
                    // Hachage déterministe du canal : la dégradation ne doit pas
                    // dépendre de l'ordre des indices.
                    let h = (*c as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15) >> 32;
                    if ((h % 1000) as f64) < frac * 1000.0 { indice[*c as usize] = 0.0; }
                }
                match s.lire(&indice) {
                    Some(l) => {
                        if l.id == q as u64 { succes += 1; }
                        distance += (l.id as i64 - q as i64).unsigned_abs() as usize;
                        cand += l.candidats;
                        comp += l.comparaisons;
                    }
                    None => { distance += taille; }
                }
                essais += 1;
            }
            ligne.push_str(&format!("  {:>6.1} % ({:.2}) Δ{:.0}",
                                    100.0 * succes as f64 / essais as f64,
                                    100.0 / taille as f64,
                                    distance as f64 / essais as f64));
            if frac == 0.0 {
                ligne.push_str(&format!("  coût {:.0} cand. ({:.0} % du magasin) / {:.0} comp.",
                                        cand as f64 / essais as f64,
                                        100.0 * cand as f64 / essais as f64 / taille as f64,
                                        comp as f64 / essais as f64));
            }
        }
        println!("{ligne}");
    }
    // --- 4bis. CONSOLIDATION RÉPÉTÉE (plusieurs cycles de rejeu).
    // Un seul cycle dit ce qu'une fusion coûte ; plusieurs cycles disent ce que la
    // mémoire devient quand on la rejoue — et c'est la question du sommeil : le rejeu
    // consolidant est-il neutre, ou use-t-il le souvenir ? Le point délicat est le
    // RAPPEL : après deux cycles, les identifiants des prototypes sont ceux du premier
    // magasin, pas ceux des épisodes d'origine. Il faut donc composer les
    // appartenances, sinon on mesurerait la fidélité au magasin intermédiaire au lieu
    // de la fidélité aux épisodes RÉELLEMENT vécus.
    if opt.episodique_cycles > 1 {
        println!();
        println!("  consolidation RÉPÉTÉE (mode exemplaire, seuil {}) :", opt.episodique_cycles_seuil);
        println!("  {:>7}  {:>11}  {:>12}  {:>10}  {:>18}", "cycle", "prototypes",
                 "compression", "rappel", "erreur");
        let mut courant = m.clone();
        // `origine[i]` = les épisodes d'origine absorbés par le prototype i du magasin
        // courant. Au premier cycle, c'est la liste des membres ; ensuite, on compose.
        let mut origine: Vec<Vec<u64>> = (0..courant.len()).map(|i| vec![i as u64]).collect();
        for cycle in 1..=opt.episodique_cycles {
            let (suivant, rap) = courant.consolider_mode(opt.episodique_cycles_seuil,
                                                        episodique::Prototype::Exemplaire);
            let mut nouvelle: Vec<Vec<u64>> = Vec::with_capacity(suivant.len());
            for membres in rap.membres.iter() {
                let mut v: Vec<u64> = Vec::new();
                for old in membres {
                    if let Some(l) = origine.get(*old as usize) { v.extend_from_slice(l); }
                }
                v.sort_unstable();
                v.dedup();
                nouvelle.push(v);
            }
            origine = nouvelle;
            courant = suivant;
            // Le rappel d'appartenance est mesuré contre les épisodes D'ORIGINE.
            let mut ok = 0usize;
            for (i, e) in cles.iter().enumerate() {
                if let Some(l) = courant.lire(e) {
                    if origine.get(l.id as usize).map(|v| v.contains(&(i as u64)))
                        .unwrap_or(false) { ok += 1; }
                }
            }
            println!("  {cycle:>7}  {:>11}  {:>11.1} %  {:>9.1} %  {:>17.2e}", courant.len(),
                     100.0 * courant.len() as f64 / cles.len() as f64,
                     100.0 * ok as f64 / cles.len() as f64, rap.erreur_moyenne);
        }
    }

    // --- 5. CONSOLIDATION PAR REJEU (C7, premier pas).
    // Rejouer les épisodes et fusionner ceux dont les clés co-activent : deux
    // souvenirs que le même indice rappelle n'en sont qu'un. Ce qui se mesure est le
    // PRIX de cette abstraction : le taux de compression, le rappel d'appartenance
    // (l'épisode d'origine se retrouve-t-il dans le prototype que la lecture rend ?)
    // et l'erreur de reconstruction.
    println!();
    println!("  consolidation par rejeu (fusion des épisodes qui co-activent) :");
    for (nom, mode) in [("MOYENNE (un point abstrait)", episodique::Prototype::Moyenne),
                        ("EXEMPLAIRE (un cas réel)", episodique::Prototype::Exemplaire)] {
        println!("  prototype {nom} :");
        println!("  {:>7}  {:>11}  {:>12}  {:>10}  {:>18}", "seuil", "prototypes", "compression",
                 "rappel", "erreur de reconstr.");
        for seuil in [1usize, 2, 4, 8, 16, 32] {
            let (c, rap) = m.consolider_mode(seuil, mode);
            let mut ok = 0usize;
            for (i, e) in cles.iter().enumerate() {
                if let Some(l) = c.lire(e) {
                    if rap.contient(l.id as usize, i as u64) { ok += 1; }
                }
            }
            println!("  {seuil:>7}  {:>11}  {:>11.1} %  {:>9.1} %  {:>17.2e}", rap.apres,
                     100.0 * rap.taux(), 100.0 * ok as f64 / cles.len() as f64,
                     rap.erreur_moyenne);
        }
    }
    println!("  le rappel est celui de l'APPARTENANCE : la lecture doit rendre le prototype \
qui contient l'épisode interrogé, pas un prototype voisin. Le seuil se compte en CANAUX \
PARTAGÉS entre les clés.");

    // --- 4ter. L'INDICE SÉMANTIQUE : la mémoire retrouve-t-elle le BON passage ?
    //
    // POURQUOI CETTE MESURE EST DIFFÉRENTE DES PRÉCÉDENTES. Tout ce qui précède interroge
    // la mémoire avec un indice qui vient de l'épisode cherché (une version dégradée de
    // sa propre clé) : c'est de la complétion de motif, et elle réussit. Ici l'indice est
    // l'état de la QUESTION — un contenu DIFFÉRENT de celui qu'on cherche. La question
    // est : la mémoire retrouve-t-elle le passage qui contient la réponse, alors que rien
    // dans son indice ne ressemble au passage ? C'est la question du rappel sémantique,
    // et la réponse n'est pas acquise : une mémoire adressée par le CONTENU ne fait pas
    // de sémantique.
    if let Some(aiguille) = opt.episodique_aiguille {
        if aiguille < cles.len() {
            let q = cles.len() - 1;   // la dernière position : la question
            // L'INDICE. Par défaut l'état de la question — mais s'il vient du magasin,
            // il s'y retrouve lui-même et la mesure ne dit rien. Un indice EXTÉRIEUR
            // (la même question posée dans un contexte qui n'a PAS l'aiguille) est un
            // vrai indice : il n'est pas dans le magasin, et ce que la mémoire en rend
            // est donc une réponse, pas un écho.
            let (indice, origine) = match opt.episodique_indice.as_ref() {
                Some(f) => {
                    let brut = std::fs::read(f).unwrap_or_else(|e| {
                        eprintln!("indice : lecture de {f} impossible : {e}"); std::process::exit(2) });
                    let v: Vec<f32> = brut.chunks_exact(4)
                        .map(|q| [q[0], q[1], q[2], q[3]]).map(f32::from_le_bytes).collect();
                    let v = if opt.episodique_expansion > 0 {
                        episodique::expandre(&v, opt.episodique_expansion, opt.episodique_connexions)
                    } else { v };
                    (v, format!("EXTÉRIEUR ({f}, {} valeurs) — il n'est PAS dans le magasin",
                                brut.len() / 4))
                }
                None => (cles[q].clone(), format!("l'état de la question, position {q}")),
            };
            println!();
            println!("  indice SÉMANTIQUE : {origine}, aiguille en {aiguille} :");
            match m.lire(&indice) {
                Some(l) => {
                    let d = (l.id as i64 - aiguille as i64).unsigned_abs();
                    // Ligne de base : la distance MOYENNE d'un épisode tiré au hasard.
                    let base: f64 = (0..cles.len())
                        .map(|i| (i as i64 - aiguille as i64).unsigned_abs() as f64)
                        .sum::<f64>() / cles.len() as f64;
                    println!("    épisode rendu : {} · recouvrement {}/{} · distance à \
l'aiguille : {d} jetons", l.id, l.recouvrement, k);
                    // LE MAILLON FINAL : l'épisode retrouvé sort du magasin, prêt à être
                    // injecté dans un autre calcul. C'est ce qui fait d'une mémoire un
                    // organe plutôt qu'un index.
                    if let Some(f) = opt.episodique_extraire.as_ref() {
                        if let Some(e) = m.par_id(l.id) {
                            let mut v = e.valeur.clone();
                            if let Some(moy) = moyenne_etats.as_ref() {
                                for (i, x) in v.iter_mut().enumerate() { *x += moy[i]; }
                            }
                            let mut octets = Vec::with_capacity(v.len() * 4);
                            for x in v.iter() { octets.extend_from_slice(&x.to_le_bytes()); }
                            match std::fs::write(f, &octets) {
                                Ok(()) => {
                                    let norme: f32 = v.iter().map(|x| x * x).sum::<f32>().sqrt();
                                    println!("    état extrait  : {} valeurs (norme {norme:.2}) \
écrites dans {f} — un état VÉCU, pas une valeur décorrélée", v.len());
                                }
                                Err(e) => eprintln!("    extraction impossible : {e}"),
                            }
                        }
                    }
                    println!("    hasard        : {base:.0} jetons en moyenne sur {} épisodes", cles.len());
                    if (d as f64) < base / 2.0 {
                        println!("    ⇒ la mémoire a retrouvé le VOISINAGE de l'aiguille");
                    } else {
                        println!("    ⇒ la mémoire n'a PAS retrouvé l'aiguille : un indice qui \
ne ressemble pas au contenu cherché ne le retrouve pas. C'est une limite du rappel par \
le contenu — il n'est pas sémantique —, et elle est mesurée, pas supposée.");
                    }
                }
                None => println!("    aucun épisode ne partage de canal avec la question : la \
mémoire ne rend RIEN (et c'est le comportement honnête)."),
            }
        }
    }

    println!();
    println!("  ce que la courbe ne dit PAS : elle porte sur {} états consécutifs d'un seul \
texte. Le rappel sur des épisodes venus de textes différents, ou après consolidation, n'est \
pas mesuré ici.", etats.len());
}

/// **PÉRIPHÉRIE (C8)** : une entrée (un signal), une sortie (un état par pas), un délai.
///
/// POURQUOI. Le plan (`docs/plan-cerveau-complet.md` § C8) demande des **régions frontière** :
/// une entrée à horloge propre, un effecteur avec délai, et des **réflexes** qui court-circuitent
/// le centre. Le réflexe est mesuré (fiches `reports/rapport-c8-*.md`) ; les frontières
/// manquaient — « rien ne sort » était écrit dans le plan, et c'était vrai.
///
/// CE QUE FAIT CETTE BOUCLE, ET RIEN DE PLUS. Pour chaque pas `t` :
///   · le signal injecté est `v[t - delai]` (0 avant `delai`) — le DÉLAI est donc dans le
///     moteur, pas dans le harnais, et il est vérifiable ;
///   · l'état d'entrée est `token_embd(--entree-jeton)`, avec `gain × v` AJOUTÉ sur
///     `--entree-canal` :
///     une région frontière reçoit une VALEUR, pas un jeton ;
///   · la pile de couches tourne (la plage `--couches` si elle est donnée, donc un réflexe
///     possible), et l'état final est ÉCRIT tel quel (f32, `hidden` valeurs par pas).
///
/// L'analyse (poursuite de consigne, erreur, paires par décision) se fait HORS du moteur : ici on
/// produit le flux, on ne juge pas. Les invariants que la porte vérifie sont le déterminisme
/// (deux exécutions identiques ⇒ sortie identique AU BIT PRÈS) et le délai (les valeurs injectées
/// sont décalées d'exactement N pas).
fn run_peripherie(chemin: &str, opt: &Options) -> i32 {
    let entree = match opt.entree.as_deref() {
        Some(e) => e,
        None => return 2,
    };
    // Le TYPE est explicite, et un type inconnu est REFUSÉ : un `--entree image:…` silencieusement
    // ignoré ferait croire que le banc vision existe.
    let fichier = match entree.split_once(':') {
        Some(("signal", f)) => f.to_string(),
        Some((type_, _)) => {
            eprintln!("[peripherie] REFUS : type d'entrée « {type_} » inconnu — le seul implémenté \
est `signal:<fichier>` (une valeur par ligne). Rien n'a été calculé.");
            return 2;
        }
        None => {
            eprintln!("[peripherie] REFUS : `--entree` attend `type:fichier` (reçu « {entree} »).");
            return 2;
        }
    };
    let sortie = match opt.sortie.as_deref() {
        Some(f) => f.to_string(),
        None => {
            eprintln!("[peripherie] REFUS : `--entree` sans `--sortie` — un effecteur sans fichier \
de sortie ne produit rien, et une région frontière qui ne sort rien n'est pas une frontière.");
            return 2;
        }
    };
    let texte = match std::fs::read_to_string(&fichier) {
        Ok(t) => t,
        Err(e) => {
            eprintln!("[peripherie] REFUS : lecture de {fichier} impossible : {e}");
            return 2;
        }
    };
    let valeurs: Vec<f32> = texte
        .lines()
        .map(|l| l.split('#').next().unwrap_or("").trim())
        .filter(|l| !l.is_empty())
        .filter_map(|l| l.parse::<f32>().ok())
        .collect();
    if valeurs.is_empty() {
        eprintln!("[peripherie] REFUS : {fichier} ne contient aucune valeur numérique lisible.");
        return 2;
    }

    let ctx = if opt.ctx_impose { opt.ctx } else { 8 };
    // `--couches a:b` et `--tete-partielle` : c'est ce qui permet un RÉFLEXE dans la périphérie
    // (une plage courte qui rend la décision). Sans eux, la boucle chargeait le modèle entier et
    // le « réflexe » coûtait exactement le même prix — mesuré, et affiché comme tel.
    let mut mdl = model::Model::load_partiel(chemin, ctx, fils(opt), true, opt.keep, false, 0, 0,
                                             opt.couches);
    if opt.tete_partielle { poser_tete_partielle(&mut mdl); }
    appliquer_quantification(&mut mdl, opt);
    if opt.attn_window > 0 { mdl.attn_window = opt.attn_window; }
    if opt.attn_sinks_impose { mdl.attn_sinks = opt.attn_sinks; }
    let hidden = mdl.cfg.hidden;
    let canal = if opt.entree_canal == usize::MAX { 0 } else { opt.entree_canal };
    if canal >= hidden {
        eprintln!("[peripherie] REFUS : `--entree-canal {canal}` hors du modèle (hidden = {hidden}). \
Un canal inexistant ne recevrait rien : refuser vaut mieux qu'écrire dans le vide.");
        return 2;
    }
    // Pas de jeton BOS dans ce crate (il n'en a jamais eu besoin : les chemins de flux IMPOSENT
    // un état). Le jeton de base est donc un paramètre — `--entree-jeton`, défaut 0 — et sa
    // validité est vérifiée : un indice hors vocabulaire lirait n'importe quoi.
    if opt.entree_jeton >= mdl.cfg.vocab {
        eprintln!("[peripherie] REFUS : `--entree-jeton {}` hors vocabulaire ({} jetons).",
                  opt.entree_jeton, mdl.cfg.vocab);
        return 2;
    }
    let bos = opt.entree_jeton as u32;
    let base = mdl.entree_du_jeton(bos);
    if opt.recurent && valeurs.len() > mdl.ctx {
        eprintln!("[peripherie] REFUS : {} pas en mode récurrent pour un contexte de {} — la \
boucle avancerait au-delà du cache KV. Donner `--ctx {}` (ou plus).", valeurs.len(), mdl.ctx,
                  valeurs.len());
        return 2;
    }
    if opt.memoire > valeurs.len() {
        eprintln!("[peripherie] REFUS : `--memoire {}` dépasse le nombre de pas ({}) — une mémoire \
plus longue que la séquence ne retiendrait jamais rien de complet.", opt.memoire, valeurs.len());
        return 2;
    }
    if !(0.0..=8.0).contains(&opt.recurrence) {
        eprintln!("[peripherie] REFUS : `--recurrence {}` hors des bornes [0, 8] — une récurrence \
de poids négatif ou absurde ne converge pas, et la refuser vaut mieux que de rendre un chiffre \
qui n'en est pas un.", opt.recurrence);
        return 2;
    }
    if opt.memoire > 0 && opt.sortie_memoire.is_none() {
        eprintln!("[peripherie] REFUS : `--memoire {}` sans `--sortie-memoire F` — une mémoire qui \
n'écrit rien ne se vérifie pas, et une mémoire invérifiable ne vaut pas mieux que pas de mémoire.",
                  opt.memoire);
        return 2;
    }
    let t0 = std::time::Instant::now();
    let mut octets: Vec<u8> = Vec::with_capacity(valeurs.len() * hidden * 4);
    let mut injectees: Vec<f32> = Vec::with_capacity(valeurs.len());
    // LA MÉMOIRE : les K derniers signaux INJECTÉS, hors du réseau. C'est un tampon, pas un
    // approximateur — et c'est ce que la fiche `rapport-c8-peripherie.md` § 2 ter oppose à une
    // récurrence qui fuit (0,104) comme à l'état du réseau (−0,681).
    let mut retenues: Vec<u8> = Vec::new();
    // La sortie du pas précédent, pour la récurrence (C2). `None` au premier pas : une boucle
    // n'a rien à consommer avant d'avoir produit.
    let mut etat_precedent: Option<Vec<f32>> = None;
    for t in 0..valeurs.len() {
        let v = if t >= opt.delai { valeurs[t - opt.delai] } else { 0.0 };
        let mut x = base.clone();
        x[canal] += opt.entree_gain * v;
        // C2 — RÉCURRENCE : ce que la région a produit au pas précédent entre dans l'entrée du
        // pas courant. `alpha = 0` laisse le calcul EXACTEMENT comme sans le drapeau (le zéro
        // est exprimable), et c'est ce que la porte vérifie.
        if opt.recurrence != 0.0 {
            if let Some(h) = etat_precedent.as_ref() {
                for (xi, hi) in x.iter_mut().zip(h.iter()) { *xi += opt.recurrence * hi; }
            }
        }
        // LE TAMPON : les K valeurs précédentes sur les canaux suivants. Sans lui, le passé
        // n'existe nulle part dans l'entrée ; avec lui, il y est PAR CONSTRUCTION — et c'est la
        // différence entre « le modèle ne retient pas » et « on lui donne de quoi retenir ».
        for k in 1..=opt.entree_memoire {
            if canal + k >= hidden {
                eprintln!("[peripherie] REFUS : le tampon de {} pas déborde du modèle (canal {} + {} ≥ {hidden}). Choisir un canal plus bas.", opt.entree_memoire, canal, opt.entree_memoire);
                return 2;
            }
            if t >= k { x[canal + k] += opt.entree_gain * valeurs[t - k]; }
        }
        mdl.emb_imposee = Some(x);
        // position : `t` en récurrent (l'historique reste dans le cache KV), 0 sinon (chaque pas
        // est une décision indépendante).
        let pos = if opt.recurent { t } else { 0 };
        let etat = mdl.forward(bos, pos);
        if opt.recurrence != 0.0 { etat_precedent = Some(etat.clone()); }
        for val in etat.iter() { octets.extend_from_slice(&val.to_le_bytes()); }
        injectees.push(v);
        if opt.memoire > 0 {
            let retenue = if t >= opt.memoire { injectees[t - opt.memoire] } else { 0.0 };
            retenues.extend_from_slice(&retenue.to_le_bytes());
        }
        eprintln!("[peripherie] pas {t} : entrée {v}");
    }
    if let Err(e) = std::fs::write(&sortie, &octets) {
        eprintln!("[peripherie] écriture de {sortie} impossible : {e}");
        return 2;
    }
    // LA MÉTRIQUE DU PLAN : les paires (poids × activation) par DÉCISION. C'est la seule unité
    // qui se compare entre architectures, et elle est déjà instrumentée par le moteur.
    if let Some(f) = opt.sortie_memoire.as_deref() {
        if let Err(e) = std::fs::write(f, &retenues) {
            eprintln!("[peripherie] écriture de {f} impossible : {e}");
            return 2;
        }
    }
    let paires: u64 = mdl.paires.iter().sum();
    let norme: f32 = injectees.iter().map(|v| v * v).sum::<f32>().sqrt();
    println!("  périphérie        : {} pas · canal {canal} · gain {} · délai {} · {} · sortie \
{sortie} (états de {hidden} canaux)", valeurs.len(), opt.entree_gain, opt.delai,
             if opt.recurent { "RÉCURRENT" } else { "pas indépendants" });
    println!("  signal injecté    : {:.4} de norme L2 · {:.1} s", norme, t0.elapsed().as_secs_f64());
    if opt.entree_memoire > 0 {
        println!("  tampon d'entrée   : {} pas (canaux {}..{})", opt.entree_memoire, canal + 1,
                 canal + opt.entree_memoire);
    }
    if opt.recurrence != 0.0 {
        println!("  RÉCURRENCE (C2)   : la sortie du pas précédent entre dans l'entrée, poids {} \
(le plan : « une région peut consommer sa propre sortie du pas précédent »)", opt.recurrence);
    }
    if opt.memoire > 0 {
        println!("  MÉMOIRE           : {} pas retenus hors du réseau ({} valeurs écrites dans {}) — \
elle ne passe par AUCUNE couche, donc elle ne coûte aucune paire", opt.memoire,
                 retenues.len() / 4, opt.sortie_memoire.as_deref().unwrap_or("—"));
    }
    println!("  paires par pas    : {:.1} M (la métrique du plan : poids × activation par décision)",
             paires as f64 / valeurs.len().max(1) as f64 / 1e6);
    println!("  dont attention    : {:.1} M · FFN/experts {:.1} M", 
             mdl.paires[0] as f64 / valeurs.len().max(1) as f64 / 1e6,
             (mdl.paires[1] + mdl.paires[2]) as f64 / valeurs.len().max(1) as f64 / 1e6);
    0
}

fn run_ppl(opt: Options) {
    // La restriction de la tête n'a pas de sens ici : le softmax normalise sur
    // tout le vocabulaire, et retirer des termes en retire aussi de la masse au
    // dénominateur. Mesuré, la perplexité BAISSE alors artificiellement (24,31
    // contre 25,37) — elle n'est plus comparable à rien.
    if let Some(f) = &opt.tete_restreinte {
        eprintln!("[tete] --tete-restreinte ignore en perplexite ({f}) : une perplexite \
calculee sur un vocabulaire restreint n'est comparable a rien. Utilisez --infer.");
    }
    let montre_options = opt.options_actives;
    // Capturés AVANT la déstructuration : `let Options { .. } = opt` déplace les
    // champs un à un, et `&opt` n'existe plus après (attrapé à la compilation).
    let (f_etat, f_alpha, f_pos, e_sortie, e_pos) =
        (opt.fusion_etat.clone(), opt.fusion_alpha, opt.fusion_pos,
         opt.etat_sortie.clone(), opt.etat_pos);
    let Options {
        ids_file: idfile, texte_file, ppl_texte: _, limit, depuis,
        ctx: ctx_opt, threads: threads_opt, abits: abits_opt,
        ctx_impose, threads_impose, abits_impose,
        dense, auto, q4, b6, attn_window, swa_pattern,
        sans_fenetre, attn_sinks, attn_sinks_impose, attn_topk, qk_topk, act_thresh, act_topk, act_renorm,
        topk_proj, moe_topk, patch: patch_file, hebb_layer, hebb_q, hebb_out, hebb_diff, hebb_eta, hebb_clamp,
        ffn_gain, logits_bin, keep,
        ppl_profil, lot, profil_neurones, neurones_sortie, trace_flux, trace_couches, flux_forcer,
        harmony, harmony_contexte, sans_yarn, ..
    } = opt;
    let lot = lot.max(1);
    let path = &modele_chemin();
    // Défauts du mode PERPLEXITÉ : 256 jetons, trois quarts des cœurs, 16 bits
    // d'activation (la référence de non-régression en dépend).
    let cpu = engine::coeurs_physiques();
    let ctx = if ctx_impose { ctx_opt } else { 256 };
    let n_threads = if threads_impose { threads_opt } else { cpu.max(1) };
    let abits = if abits_impose { abits_opt } else { 16 };
    let idfile = idfile.unwrap_or_default();
    let mut ids: Vec<u32> = if idfile.is_empty() {
        Vec::new()
    } else {
        let raw = std::fs::read_to_string(&idfile).expect("fichier d'identifiants illisible");
        raw.split(|c: char| c == ',' || c.is_whitespace())
            .filter(|s| !s.is_empty())
            .filter_map(|s| s.parse().ok())
            // `--depuis N` : on charge N jetons de plus que la limite, pour que
            // le premier jeton noté ait un contexte complet (voir plus bas).
            .take(limit.saturating_add(depuis))
            .collect()
    };
    // Garde-fou : des identifiants hors vocabulaire signifient qu'on nourrit le
    // modèle avec le découpage d'un AUTRE modèle. La perplexité ne mesurerait
    // alors que l'absurdité de l'entrée — vérifié : 42 127 au lieu de 11.
    let vocab = mdl_cfg_vocab(path);
    if let Some(v) = vocab {
        if let Some(&mauvais) = ids.iter().find(|&&i| i as usize >= v) {
            panic!("identifiant {mauvais} ≥ vocabulaire du modèle ({v}) : \
                    ce fichier de jetons vient d'un autre tokenizer");
        }
    }
    if !idfile.is_empty() {
        println!("{idfile} : {} tokens, fenêtres de {ctx}", ids.len());
    }

    let mut mdl = model::Model::load_partiel(path, ctx, n_threads, dense, keep, auto, q4, b6,
                                             opt.couches);
    if opt.tete_partielle { poser_tete_partielle(&mut mdl); }
    appliquer_fusion(&mut mdl, f_etat, f_alpha, f_pos, e_sortie, e_pos);
    if let Some(chemin) = flux_forcer.as_deref() {
        match model::FluxRelecteur::lire(chemin) {
            Ok(r) => {
                println!("[flux] rejeu depuis {chemin} : {} listes enregistrées",
                         r.listes.len() + r.listes_blocs.len());
                mdl.flux_force = Some(r);
            }
            Err(e) => eprintln!("[flux] lecture impossible de {chemin} : {e}"),
        }
    }
    if let Some(chemin) = trace_flux.as_deref() {
        match model::TraceFlux::nouveau(chemin, trace_couches.clone(), mdl.cfg.hidden,
                                        mdl.cfg.n_layer) {
            Ok(t) => { println!("[trace] flux enregistré dans {chemin}"); mdl.trace = Some(t); }
            Err(e) => eprintln!("[trace] impossible d'écrire {chemin} : {e}"),
        }
    }
    // Texte brut : les identifiants viennent du tokenizer du modèle, donc du
    // même découpage que celui qui a servi à l'entraîner. `--limit` compte les
    // jetons de contenu, comme pour un fichier d'identifiants.
    if let Some(f) = &texte_file {
        let brut = std::fs::read_to_string(f).expect("texte illisible");
        let tk = build_tokenizer(&mdl.g);
        ids = tk.encode(&brut);
        let voulu = limit.saturating_add(depuis);
        if ids.len() > voulu { ids.truncate(voulu); }
        println!("{f} : {} jetons (tokenizer du modèle), fenêtres de {ctx}", ids.len());
    }
    if depuis > 0 {
        println!("notation à partir du jeton {depuis} : les jetons précédents servent de contexte, \
                  les mêmes jetons sont donc comparables à contexte 512, 1 024, 4 096…");
    }
    mdl.moe_topk = moe_topk;
    poser_niveaux(&mut mdl, abits, "perplexité");
    if let Some(f) = &patch_file {
        let pt = model::Patch::load(f).expect("chargement du greffon");
        let norme = |v: &[f32]| v.iter().map(|x| x * x).sum::<f32>().sqrt();
        println!("greffon : couche {}, |u|={:.3} |v|={:.3} |d|={:.3}",
                 pt.layer, norme(&pt.u), norme(&pt.v), norme(&pt.d));
        mdl.patch = Some(pt);
    }
    if let Some(gs) = ffn_gain {
        let liste: Vec<String> = gs.iter().map(|(l, g)| format!("couche {l} × {g}")).collect();
        println!("gain FFN : {}", liste.join(" · "));
        mdl.ffn_gain = Some(gs);
    }
    mdl.act_thresh = act_thresh;
    mdl.act_topk = act_topk;
    mdl.act_renorm = act_renorm;
    mdl.act_topk_proj = topk_proj;
    mdl.attn_topk = attn_topk;
    mdl.qk_topk = qk_topk;
    if sans_yarn { mdl.cfg_yarn_off(); }
    // MÊME précédence qu'en inférence (sans-fenetre d'abord, puis la fenêtre
    // explicite) : l'ordre était inversé entre les deux modes.
    if sans_fenetre { mdl.attn_window = 0; }
    if attn_window > 0 { mdl.attn_window = attn_window; }
    if let Some(p) = swa_pattern { mdl.swa_pattern = p; }
    if sans_fenetre || swa_pattern.is_some() {
        println!("fenêtre : {} · motif {} (imposé par la ligne de commande)",
                 if mdl.attn_window == 0 { "aucune".to_string() } else { mdl.attn_window.to_string() },
                 mdl.swa_pattern);
    }
    // `impose` et non `> 0` : c'est ce qui rend `--attn-sinks 0` capable
    // d'ÉTEINDRE les puits (le défaut vaut 4 quand le modèle ne déclare pas de
    // fenêtre). Un garde `> 0` transformait « zéro puits » en « laisse le défaut ».
    if attn_sinks_impose { mdl.attn_sinks = attn_sinks; }
    avertir_puits_inertes(&mdl, attn_sinks_impose);
    if act_thresh > 0.0 || act_topk > 0 {
        println!("parcimonie imposée : seuil {:.1} % du max{}",
                 act_thresh * 100.0,
                 if act_topk > 0 { format!(", k-WTA k={act_topk}") } else { String::new() });
    }
    // Le tableau de bord vient EN DERNIER, après la trace, les top-k, les seuils,
    // la fenêtre et le gain FFN : sa première version, placée plus haut, affichait
    // « niveaux 127 · seuil 0 · trace false · ffn_gain None » alors que la ligne de
    // commande demandait 4 bits, un seuil de 0,1, une trace et un gain FFN — un
    // tableau de bord qui montre l'état d'avant les affectations est pire que pas
    // de tableau du tout, puisque c'est exactement ce qu'il est censé démasquer.
    if montre_options {
        options_actives(&mdl, "perplexité", ctx_impose, dense, keep, attn_sinks_impose);
    }
    if let Some(l) = hebb_diff {
        let (n_out, n_in) = (mdl.cfg.ffn, mdl.cfg.hidden);
        mdl.hebb_diff = Some(model::HebbDiff::new(l, n_out, n_in, hebb_eta, hebb_clamp));
        println!("[hebb-diff] ADAPTATEUR ACTIF — couche {l}, gate ({n_out}×{n_in}), \
eta {hebb_eta:e}, écrêtage ±{hebb_clamp}. Règle LOCALE et forward-only : \
Δx = x(t)−x(t−1), Δy = y(t)−y(t−1), D += η·Δy⊗Δx, y' = y + D·x. La matrice \
effective est W+D : ce modèle N'EST PLUS celui du fichier. Exige --lot 1.");
    }
    if let Some(l) = hebb_layer {
        let mut hb = model::Hebb::new(l, mdl.cfg.ffn, mdl.cfg.hidden, hebb_q);
        hb.log_on = true;
        mdl.hebb = Some(hb);
        println!("journalisation : couche {l}, entrée FFN ({} dim)", mdl.cfg.hidden);
    }
    if profil_neurones {
        mdl.activer_profil_neurones();
        println!("profilage des neurones actif : un neurone compte comme actif si sa valeur \
                  quantifiée n'est pas nulle (même critère que le chemin par événements)");
    }
    mdl.reset_events();
    // Fenêtres d'évaluation : soit des tranches brutes de `ctx` jetons (mode
    // historique, toutes notées), soit des tours harmony dont seuls les jetons
    // de contenu sont notés.
    let fenetres: Vec<(Vec<u32>, Vec<bool>)> = match &harmony {
        None => {
            // `--depuis N` : les fenêtres sont ancrées pour que le premier jeton
            // NOTÉ ait un contexte complet (on recule de ctx-1 jetons, qui ne
            // sont pas notés). Sans décalage, le protocole historique est
            // conservé au chiffre près (`chunks`).
            if depuis == 0 {
                ids.chunks(ctx).map(|c| (c.to_vec(), vec![true; c.len()])).collect()
            } else {
                // Avec décalage, les fenêtres se recouvrent d'UN jeton : chaque
                // jeton du corpus est ainsi noté exactement une fois, sans le
                // trou d'un jeton par frontière du découpage en tranches.
                let deb = depuis.saturating_sub(ctx.saturating_sub(1));
                let mut fen = Vec::new();
                let mut base = deb.min(ids.len());
                loop {
                    let fin = (base + ctx).min(ids.len());
                    let c = &ids[base..fin];
                    let masque: Vec<bool> = (0..c.len()).map(|j| base + j >= depuis).collect();
                    let dernier = fin == ids.len();
                    fen.push((c.to_vec(), masque));
                    if dernier || fin < 2 { break; }
                    base = fin - 1;
                }
                fen
            }
        }
        Some(mode) => {
            let tk = build_tokenizer(&mdl.g);
            // Le contexte est lu ICI : sans cela, c'est le CHEMIN du fichier qui
            // part dans le tour « user » — mesuré, et cela ne se voit que dans
            // la trace décodée.
            let texte_contexte: Option<String> = harmony_contexte.as_ref()
                .map(|f| std::fs::read_to_string(f).expect("contexte harmony illisible"));
            let f = fenetres_harmony(&tk, &ids, ctx, mode, texte_contexte.as_deref());
            let notes: usize = f.iter().map(|(_, m)| m.iter().filter(|&&b| b).count()).sum();
            println!("harmony ({mode}{}) : {} fenêtres, {notes} jetons de contenu notés \
                      sur {} (les marqueurs ne sont pas notés)",
                     if harmony_contexte.is_some() { ", avec contexte" } else { "" },
                     f.len(), ids.len());
            f
        }
    };
    let t0 = Instant::now();
    let mut nll = 0f64;
    let mut n = 0usize;
    let mut perte: Vec<f32> = Vec::new();
    // Journal de logits : écrit à la volée (une matrice de vocabulaire fait
    // 800 Mo sur gpt-oss, la garder en mémoire serait absurde).
    let mut journal = match &logits_bin {
        Some(f) => {
            use std::io::Write;
            let mut w = std::io::BufWriter::new(
                std::fs::File::create(f).expect("création du fichier de logits"));
            w.write_all(&(mdl.cfg.vocab as i32).to_le_bytes()).unwrap();
            w.write_all(&0i32.to_le_bytes()).unwrap();   // n_pos, réécrit à la fin
            Some(w)
        }
        None => None,
    };
    let mut n_logits = 0i32;
    let mut tampon: Vec<u8> = Vec::new();
    // Profil par profondeur : la perte moyenne par tranche de 256 positions.
    // Une perplexité qui MONTE avec la position ne dit pas du tout la même
    // chose qu'une perplexité uniformément mauvaise — et à 4 096 jetons, la
    // moyenne seule ne permet pas de trancher.
    let profil = ppl_profil;
    let mut seaux: Vec<(f64, usize)> = vec![(0.0, 0); ctx.div_ceil(256)];
    // Deux postes que le profil du moteur ne voit pas : la tête de sortie
    // (la plus grosse matrice du modèle) et la notation log-sum-exp. Sans eux,
    // « reste » les mélangeait et on ne pouvait pas dire si la tête par lots
    // avait servi à quelque chose.
    let (mut t_tete, mut t_note) = (0f64, 0f64);
    for (i_f, (chunk, masque)) in fenetres.iter().enumerate() {
        let (mut nll_f, mut n_f) = (0f64, 0usize);
        // Préremplissage par lots : `lot` jetons d'un coup. `lot == 1` emprunte
        // exactement le chemin historique jeton par jeton.
        let mut pos = 0usize;
        while pos < chunk.len() {
            let t = lot.min(chunk.len() - pos);
            let hs = mdl.forward_lot(&chunk[pos..pos + t], pos);
            // Tête par lots : la matrice la plus lourde du modèle est lue une
            // fois pour le groupe au lieu d'une fois par jeton.
            let marque = Instant::now();
            let lgs = if t > 1 { Some(mdl.logits_lot(&hs)) } else { None };
            t_tete += marque.elapsed().as_secs_f64();
            for (i, h) in hs.iter().enumerate() {
            let pos = pos + i;
            if pos + 1 < chunk.len() && masque[pos + 1] {
                // Tête au fil du jeton (lot 1) : chronométrée à part, sinon son
                // coût se cachait dans « notation log-sum-exp » et la
                // comparaison avec la tête par lots n'avait plus de sens.
                let lg = match &lgs {
                    Some(v) => v[i].clone(),
                    None => {
                        let mt = Instant::now();
                        let r = mdl.logits(h);
                        t_tete += mt.elapsed().as_secs_f64();
                        r
                    }
                };
                let marque = Instant::now();
                let mut mx = f32::NEG_INFINITY;
                for &v in &lg { if v > mx { mx = v; } }
                let mut sum = 0f64;
                for &v in &lg { sum += ((v - mx) as f64).exp(); }
                let lse = mx as f64 + sum.ln();
                let nll_tok = lse - lg[chunk[pos + 1] as usize] as f64;
                nll += nll_tok;
                nll_f += nll_tok;
                n += 1;
                n_f += 1;
                // M1 — LE BUS DE VALEUR. Le modulateur n'est pas la perte
                // (c'est de la surprise, et la surprise dégrade : mesuré), c'est
                // l'AMÉLIORATION : ce jeton s'est-il mieux passé que la moyenne
                // courante ? Le signal est diffusé à toutes les couches par ce
                // scalaire, comme un noyau neuromodulateur — et il est en retard
                // d'un jeton, puisque la modulation biologique l'est aussi.
                if let Some(hd) = mdl.hebb_diff.as_mut() {
                    let moy = nll / n.max(1) as f64;
                    let gain = if moy > 1e-9 { (moy - nll_tok) / moy } else { 0.0 };
                    hd.modulateur = (1.0 + 2.0 * gain as f32).clamp(0.25, 4.0);
                }
                let b = (pos + 1) / 256;
                if b < seaux.len() { seaux[b].0 += nll_tok; seaux[b].1 += 1; }
                perte.push(nll_tok as f32);
                t_note += marque.elapsed().as_secs_f64();
                if let Some(w) = journal.as_mut() {
                    use std::io::Write;
                    tampon.clear();
                    for &v in &lg { tampon.extend_from_slice(&v.to_le_bytes()); }
                    w.write_all(&tampon).unwrap();
                    n_logits += 1;
                }
            }
            }
            pos += t;
        }
        let ppl = (nll / n as f64).exp();
        // La perplexité PROPRE à la fenêtre dit où le modèle décroche : une
        // première fenêtre à 900 et les suivantes à 15 ne racontent pas du tout
        // la même histoire qu'une dégradation régulière.
        if n == 0 {
            println!("  aucun jeton noté (il en faut au moins deux : le premier ne \
prédit rien) — la perplexité cumulée n'a pas de sens ici");
        } else {
        println!("  {:6} tokens notés — perplexité cumulée {:.3}  ({:.1} tok/s){}",
                 n, ppl, n as f64 / t0.elapsed().as_secs_f64(),
                 if fenetres.len() > 1 {
                     format!("  [fenêtre {} : {} notés, PPL {:.3}]",
                             i_f + 1, n_f, (nll_f / n_f.max(1) as f64).exp())
                 } else { String::new() });
        }
    }
    if let (Some(w), Some(f)) = (journal, &logits_bin) {
        use std::io::{Seek, SeekFrom, Write};
        let mut fic = w.into_inner().expect("vidage du journal de logits");
        fic.seek(SeekFrom::Start(4)).unwrap();
        fic.write_all(&n_logits.to_le_bytes()).unwrap();
        fic.sync_all().unwrap();
        println!("logits exportés : {f} — {n_logits} positions × {} valeurs", mdl.cfg.vocab);
    }
    if profil {
        println!("profil par profondeur (perplexité par tranche de 256 positions) :");
        for (i, (s, c)) in seaux.iter().enumerate() {
            if *c == 0 { continue; }
            println!("    {:>6}-{:<6} : {:>9.3}  ({} jetons notés)",
                     i * 256, i * 256 + 255, (s / *c as f64).exp(), c);
        }
    }
    if let Some(rapport) = mdl.rapport_neurones() {
        println!("\n{rapport}");
        if let Some(f) = &neurones_sortie {
            match mdl.ecrire_neurones(f) {
                Ok(n) => println!("classement de {n} neurones écrit dans {f}"),
                Err(e) => println!("écriture du classement impossible : {e}"),
            }
        }
    }
    let ppl = (nll / n as f64).exp();
    // Un rejeu doit DIRE ce qu'il a servi. Sans ces deux compteurs, une trace
    // dont les clés ne correspondent plus (par exemple écrite avant le passage
    // au compteur de jeton GLOBAL : la première clé valait 0, elle vaut 1
    // maintenant) se rejouait en silence en donnant une perplexité fausse —
    // 1958,72 au lieu de 19,3885 sur l'ancienne trace de /tmp, constaté ici.
    if let Some(r) = mdl.flux_force.as_ref() {
        println!("  rejeu             : {} listes servies, {} manquantes{}",
                 r.servies, r.manquantes,
                 if r.manquantes > 0 && r.servies == 0 {
                     "  ← AUCUNE liste utilisée : la trace ne correspond pas à ce calcul"
                 } else if r.manquantes > r.servies {
                     "  ← la moitié au moins n'a pas servi : vérifier la trace"
                 } else { "" });
    }
    if n == 0 {
        println!("aucun jeton noté (il en faut au moins deux : le premier ne prédit rien)");
        return;
    }
    rapport_hebb_diff(&mdl);
    // SAUVEGARDE de `D` : adapter sur A puis évaluer sur B n'est possible
    // que si la matrice apprise survit à la passe (cf. verdict hors échantillon).
    if let (Ok(f), Some(hd)) = (std::env::var("DRAVE_HEBB_D_SAUVE"), mdl.hebb_diff.as_ref()) {
        use std::io::Write;
        let mut fic = std::fs::File::create(&f).expect("écriture de D");
        for v in &hd.d { fic.write_all(&v.to_le_bytes()).unwrap(); }
        eprintln!("[hebb-diff] D sauvé dans {f} : {} valeurs", hd.d.len());
    }
    if let Some(hb) = mdl.hebb.as_ref() {
        if hb.log_on {
            use std::io::Write;
            let mut fa = std::fs::File::create(&hebb_out).unwrap();
            for v in &hb.log { fa.write_all(&v.to_le_bytes()).unwrap(); }
            let mut fl = std::fs::File::create(format!("{hebb_out}.perte")).unwrap();
            for v in &perte { fl.write_all(&v.to_le_bytes()).unwrap(); }
            println!("journal : {} vecteurs de {} dim, {} pertes (act_log.bin, loss_log.bin)",
                     hb.log.len() / cfg_dims(&mdl), cfg_dims(&mdl), perte.len());
        }
    }
    if let Some(t) = mdl.trace.as_mut() {
        t.terminer();
        println!("[trace] {} listes · {} neurones actifs · {:.0} Mo",
                 t.enregistrements, t.actifs, t.octets as f64 / 1e6);
    }
    stats_experts(&mdl);
    println!("\n=== perplexité {:.4} sur {} tokens ({} événements, {:.1} s) ===",
             ppl, n, mdl.events_total(), t0.elapsed().as_secs_f64());
    println!("    {:.1} tok/s effectifs (avant + tête)", n as f64 / t0.elapsed().as_secs_f64());
    let ae = mdl.attn_events as f64 / n.max(1) as f64;
    let fe = mdl.events_total() as f64 / n.max(1) as f64;
    println!("    attention : {:.2} M paires (requête, clé) par token", ae / 1e6);
    println!("    projections : {:.1} M événements par token", fe / 1e6);
    // Le flux par provenance : la question que la vision pose au modèle est
    // « d'où vient le flux », parce que la réponse dit ce qu'on peut déporter,
    // découper ou simplifier. Les paires sont ce qui est PAYÉ ; les événements
    // sont ce qui est payé sur un chemin en listes. Un modèle MLA ou IQ
    // n'affichait que des zéros avant ce compteur.
    let pa = mdl.paires;
    // Les scores d'attention (paires requête-clé) ne sont pas dans `paires` :
    // ils sont comptés par `attn_events` depuis toujours. Le flux TOTAL d'un
    // jeton est donc la somme des deux, sinon la part de l'attention serait
    // fausse — et c'est la ligne qui dit où porter l'effort.
    let scores = mdl.attn_events;
    let pt: u64 = pa.iter().sum::<u64>() + scores;
    // Les scores sont souvent des ordres de grandeur sous les projections :
    // « 0.0 M » n'est pas une mesure, donc on les donne en kilo-paires.
    println!("    paires (poids × activation) par token : attention {:.1} M · experts {:.1} M · partagé {:.1} M · scores {:.0} K · total {:.1} M",
             pa[0] as f64 / n as f64 / 1e6, pa[1] as f64 / n as f64 / 1e6,
             pa[2] as f64 / n as f64 / 1e6, scores as f64 / n as f64 / 1e3,
             pt as f64 / n as f64 / 1e6);
    // OCCUPATION DES POIDS — LA COLONNE QUI MANQUAIT (manque M9). La ligne ci-dessus mesure le
    // travail d'un noyau DENSE : `n_in × n_out`, que les poids soient nuls ou pas. Ce qui suit dit
    // ce qui est STOCKÉ, et ce qu'un format creux lirait — sous une hypothèse écrite à l'écran.
    {
        let occ = mdl.occupation_poids();
        let (na, ta, ua) = occ[0];
        let (ne, te, ue) = occ[1];
        let (np, tp, _) = occ[2];
        let (nnz, tot) = (na + ne + np, ta + te + tp);
        if tot > 0 {
            let dens = nnz as f64 / tot as f64;
            // L'ESTIMATION NE PORTE QUE SUR LES PROJECTIONS : les paires `k` sont, dans
            // l'ordre, celles de l'attention et celles des experts — la table d'entrée et la tête
            // ne sont pas dans la ligne de paires, et les inclure dans l'occupation fausserait le
            // rapport.
            let po: f64 = pa.iter().enumerate()
                .map(|(k, v)| {
                    let (n, t, _) = occ[k.min(2)];
                    if t == 0 { *v as f64 } else { *v as f64 * (n as f64 / t as f64) }
                }).sum();
            println!("    occupation des poids : {:.1} % de non-nuls ({} sur {}) — attention {:.1} % · experts {:.1} %",
                     100.0 * dens, nnz, tot,
                     100.0 * if ta > 0 { na as f64 / ta as f64 } else { 0.0 },
                     100.0 * if te > 0 { ne as f64 / te as f64 } else { 0.0 });
            println!("    ⇒ si la représentation était CREUSE (non-nuls × activations vivantes, hypothèse) : {:.1} M paires par token au lieu de {:.1} M (÷{:.2})",
                     po / n as f64 / 1e6, pa.iter().sum::<u64>() as f64 / n as f64 / 1e6,
                     if po > 0.0 { pa.iter().sum::<u64>() as f64 / po } else { 1.0 });
            if ue > 0 {
                println!("    ⚠ {} poids d'experts NON comptés (format 4 bits sans décodeur d'occupation) : le chiffre est PARTIEL",
                         ue);
            }
        }
    }
    println!("    dont en listes (une paire y est un événement) : {:.1} M — le reste est dense (déquantifié ou f32)",
             mdl.events_total() as f64 / n as f64 / 1e6);
    if pt > 0 {
        println!("    part de l'attention dans le flux total : {:.1} %",
                 100.0 * (pa[0] + scores) as f64 / pt as f64);
    }
    // Où passe VRAIMENT le temps du token : sans ce découpage, on optimise à
    // l'aveugle. Le poste non compté contient la tête de sortie (151 936 × 896
    // poids, la plus grosse matrice du modèle) et l'échantillonnage.
    let sec = t0.elapsed().as_secs_f64();
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
    // **Attention V4 (`attn_v4`) : le poste ci-dessus la compte EN ENTIER** —
    // ses sous-compteurs `scores`/`softmax` appartiennent à l'autre chemin (MLA
    // de V3) et restent donc à zéro ici, ce qui faisait croire que l'attention
    // de V4.1 ne coûtait rien (relevé au bloc 15 : 12,4 s par jeton). Ces quatre
    // sous-postes disent où elles passent.
    {
        use std::sync::atomic::Ordering;
        let v: Vec<f64> = model::PROF_V4.iter()
            .map(|c| c.load(Ordering::Relaxed) as f64 / 1e6 / n as f64).collect();
        if v.iter().any(|x| *x > 0.0) {
            println!("    dont attention V4 (attn_v4) : projets q/kv {:.2} | compresseur {:.2} | indexeur {:.2} | scores + softmax + somme {:.2} | dé-rotation + sortie groupée {:.2}",
                     v[0], v[1], v[2], v[3], v[4]);
        }
    }
}

#[cfg(test)]
mod tests_niveaux {
    //! `--abits` : la borne du stockage i16. Au-delà de 16 bits, les valeurs
    //! quantifiées étaient ramenées à 32 767 par les conversions (et *enroulées*
    //! là où la conversion n'était pas bornée) : mesuré sur V4.1, `--abits 24`
    //! donnait 127 496 de perplexité au lieu de 12 889, sans un mot.
    use super::*;

    #[test]
    fn les_niveaux_sont_bornes_par_le_stockage() {
        assert_eq!(niveaux_activation(8), 127.0);
        assert_eq!(niveaux_activation(16), 32767.0);
        // au-delà de 16 bits, on borne (et `poser_niveaux` le DIT)
        assert_eq!(niveaux_activation(24), 32767.0);
        assert_eq!(niveaux_activation(32), 32767.0);
        // et jamais zéro ni négatif : `1 << (abits-1)` avec abits = 0 paniquait
        assert_eq!(niveaux_activation(0), 0.0);
        assert_eq!(niveaux_activation(1), 0.0);
    }
}

#[cfg(test)]
mod tests_flux {
    //! Les tests du PROTOCOLE et du CODEC. Ils manquaient : les deux bugs les
    //! plus coûteux de la session (un en-tête d'un octet trop long, un
    //! échappement d'indice écrit sur quatre octets et lu sur deux) étaient
    //! invisibles pour les six tests existants, qui ne couvraient que le cache KV.
    use super::*;
    use std::net::{TcpListener, TcpStream};

    #[test]
    fn entete_et_version_sont_ce_que_les_numeros_disent() {
        assert_eq!(TAILLE_TETE, 99, "l'en-tête de flux doit faire 99 octets (v8 : les paires)");
        // La version suit l'en-tête : 4 quand les top-k sont entrés dans le
        // contrat, 5 quand le mode 4 (lot en listes) est apparu, 6 quand le
        // pré-mix porté de V4.1 a été ajouté en tête de corps. Ce test a
        // d'ailleurs échoué au premier coup, exactement pour ça — et il a
        // resservi à la v6.
        assert_eq!(VERSION_FLUX, 8, "le compte de paires transporté impose la version 8");
    }

    #[test]
    fn paires_blocs_aller_retour_avec_echappement() {
        // Écarts successifs : 3 (direct), 297 (échappement), 1 (direct),
        // 255 (échappement — c'est le cas LIMITE, 255 est réservé).
        let idx: Vec<u16> = vec![3, 300, 301, 556];
        let val: Vec<i8> = vec![7, -3, 0, 127];
        let octets = encoder_paires_blocs(&idx, &val);
        assert_eq!(octets.len(), 2 * 2 + 2 * 4, "2 paires directes et 2 échappements");
        let (i2, v2) = decoder_paires_blocs(&octets, idx.len()).unwrap();
        assert_eq!(i2, idx);
        assert_eq!(v2, val);
    }

    #[test]
    fn paires_blocs_tronquees_sont_refusees() {
        let idx: Vec<u16> = vec![3, 300];
        let val: Vec<i8> = vec![1, 2];
        let octets = encoder_paires_blocs(&idx, &val);
        assert!(decoder_paires_blocs(&octets[..octets.len() - 1], 2).is_err(),
                "une paire coupée doit être refusée, pas lue au hasard");
        assert!(decoder_paires_blocs(&[255], 1).is_err(),
                "un échappement sans ses deux octets doit être refusé");
    }

    #[test]
    fn flux_dense_aller_retour_par_la_vraie_mise_en_trame() {
        let ecoute = TcpListener::bind("127.0.0.1:0").unwrap();
        let adresse = ecoute.local_addr().unwrap();
        let valeurs: Vec<f32> = (0..8).map(|i| i as f32 * 0.5 - 1.0).collect();
        let attendu = valeurs.clone();
        let serveur = std::thread::spawn(move || {
            let (mut sock, _) = ecoute.accept().unwrap();
            let f = recevoir_flux(&mut sock, 8, 1).unwrap();
            assert_eq!(f.mode, MODE_DENSE);
            assert_eq!(f.n, 8);
            // 33 et non 32 : le compte des octets REÇUS inclut désormais le
            // préfixe de corps de la v6 (`np`, ici 0). Il l'omettait, et un V4.1
            // découpé annonçait donc 81 999 octets au retour pour 82 016 réels.
            assert_eq!(f.octets_corps, 33);
            assert_eq!(f.charge.en_dense(8), attendu);
        });
        let mut client = TcpStream::connect(adresse).unwrap();
        let (octets, n) = envoyer_flux(&mut client, 12, 24, 0, &valeurs,
                                       MODE_DENSE, None).unwrap();
        assert_eq!(n, 8);
        assert_eq!(octets, TAILLE_TETE + 1 + 32,
                   "l'octet d'en-tête en trop faisait exactement cette différence \
(+1 depuis la v6 : le compte `np` en tête de corps)");
        serveur.join().unwrap();
    }
}

#[cfg(test)]
mod tests_plafond {
    //! Le plafond des allocations pilotées par le réseau (règle R4). Sans lui, un
    //! pair qui annonce `n = 4 milliards` fait demander ~15 To au noyau AVANT tout
    //! contrôle — la relecture adversariale l'avait relevé comme soupçon, faute de
    //! pouvoir le tester sans risquer la machine. Le test ne risque rien : le
    //! refus a lieu avant l'allocation.
    use super::*;
    use std::io::Write;
    use std::net::{TcpListener, TcpStream};

    /// En-tête v4 complet, prêt à compléter par un corps.
    fn entete(mode: u8, n: u32) -> Vec<u8> {
        let mut t: Vec<u8> = Vec::new();
        t.extend_from_slice(&MAGIE_FLUX.to_le_bytes());
        t.push(VERSION_FLUX);
        t.push(mode);
        t.extend_from_slice(&12u32.to_le_bytes());
        t.extend_from_slice(&24u32.to_le_bytes());
        t.extend_from_slice(&0u32.to_le_bytes());
        t.extend_from_slice(&n.to_le_bytes());
        t.extend_from_slice(&0f32.to_le_bytes());
        t.extend_from_slice(&127f32.to_le_bytes());
        t.extend_from_slice(&0f32.to_le_bytes());
        t.extend_from_slice(&0u32.to_le_bytes());
        t.push(0);
        // Le remplissage se CALCULE à partir de TAILLE_TETE : il valait 10 mots (les
        // top-k et les sept top-k par projection), et il aurait fallu le passer à 13 au
        // moment du protocole v7 — c'est exactement le genre de littéral qui casse un test
        // pour une raison qui n'est pas celle qu'il mesure. Compté, il ne casse plus.
        while t.len() < TAILLE_TETE { t.extend_from_slice(&0u32.to_le_bytes()); }
        assert_eq!(t.len(), TAILLE_TETE,
                   "TAILLE_TETE doit être un multiple de 4 au-delà de l'en-tête fixe");
        t
    }

    /// Le corps est envoyé puis la connexion fermée : le décodeur ne doit ni
    /// paniquer ni bloquer.
    fn decoder_une_trame(mode: u8, n: u32, corps: Vec<u8>, hidden: usize) -> std::io::Result<Flux> {
        let ecoute = TcpListener::bind("127.0.0.1:0").unwrap();
        let adresse = ecoute.local_addr().unwrap();
        let serveur = std::thread::spawn(move || {
            let (mut sock, _) = ecoute.accept().unwrap();
            sock.write_all(&entete(mode, n)).unwrap();
            // Protocole v6 : le corps commence par `np` (aucun pré-mix ici).
            sock.write_all(&[0u8]).unwrap();
            sock.write_all(&corps).unwrap();
        });
        let mut client = TcpStream::connect(adresse).unwrap();
        // Délai de lecture : si un garde-fou disparaissait, le test doit ÉCHOUER,
        // pas pendre — sans lui il attendrait les 358 Go du corps annoncé
        // (relevé par la relecture : le test ne pouvait pas rater proprement).
        client.set_read_timeout(Some(std::time::Duration::from_secs(5))).unwrap();
        let r = recevoir_flux(&mut client, hidden, 1);
        serveur.join().unwrap();
        r
    }

    #[test]
    fn une_trame_a_premix_porte_est_lue_et_comptee() {
        // `np = 1` n'était exercé par AUCUN test : les trames forgées des tests
        // écrivaient `np = 0` en dur (le helper `decoder_une_trame` ajoute cet
        // octet lui-même), la porte du découpage tourne sur un modèle sans
        // hyper-connexions (`np = 0` des deux côtés), et le seul chemin qui en
        // envoie un est V4.1 — 365 Go, quatre minutes (relevé par la relecture
        // adverse du bloc 13). Ici : 4 copies × 1 pré-mix, trame montée à la
        // main, et le compte d'octets du corps doit inclure le préfixe.
        let hc = 4usize;
        let premix: [f32; 4] = [0.25, 0.5, 0.75, 1.0];
        let ecoute = TcpListener::bind("127.0.0.1:0").unwrap();
        let adresse = ecoute.local_addr().unwrap();
        let serveur = std::thread::spawn(move || {
            let (mut sock, _) = ecoute.accept().unwrap();
            sock.write_all(&entete(MODE_DENSE, 1)).unwrap();
            sock.write_all(&[1u8]).unwrap();                 // np = 1
            for v in premix { sock.write_all(&v.to_le_bytes()).unwrap(); }
            sock.write_all(&0f32.to_le_bytes()).unwrap();    // un canal nul
        });
        let mut client = TcpStream::connect(adresse).unwrap();
        client.set_read_timeout(Some(std::time::Duration::from_secs(5))).unwrap();
        let f = recevoir_flux(&mut client, 8, hc).unwrap();
        serveur.join().unwrap();
        assert_eq!(f.premix, premix.to_vec(), "le pré-mix porté doit être relu tel quel");
        assert_eq!(f.octets_corps, 1 + hc * 4 + 4,
                   "le compte des octets REÇUS inclut le préfixe de corps (np + pré-mix), \
comme celui de l'émission — il l'omettait (81 999 annoncés pour 82 016 réels)");
        assert_eq!(f.charge.en_dense(1), vec![0.0]);
    }

    #[test]
    fn une_trame_liste_hors_dimension_ne_tue_pas_le_noeud() {
        // n = 1 paire, indice 5000 pour 896 canaux : c'était un `index out of
        // bounds` → SIGABRT (relecture adversariale, trame forgée).
        let mut corps = Vec::new();
        corps.extend_from_slice(&5000u16.to_le_bytes());
        corps.extend_from_slice(&7i16.to_le_bytes());
        let f = decoder_une_trame(MODE_LISTE, 1, corps, 896).unwrap();
        let x = f.charge.en_dense(896);          // ne doit pas paniquer
        assert_eq!(x.len(), 896);
        assert!(x.iter().all(|v| *v == 0.0), "un indice hors dimension est ignoré");
    }

    /// Un état du mode 4, forgé à la main : `a · n_blocs · longueur`, les échelles,
    /// puis les paires (écart u8, valeur i8).
    fn etat_forge(paires: &[(u16, i8)], n_blocs: u32, echelles: &[f32]) -> Vec<u8> {
        let mut p: Vec<u8> = Vec::new();
        let mut prev = 0u32;
        for &(i, v) in paires {
            let e = i as u32 - prev;
            if e < 255 { p.push(e as u8); } else { p.push(255); p.extend_from_slice(&i.to_le_bytes()[..2]); }
            prev = i as u32;
            p.push(v as u8);
        }
        let mut c: Vec<u8> = Vec::new();
        c.extend_from_slice(&(paires.len() as u32).to_le_bytes());
        c.extend_from_slice(&n_blocs.to_le_bytes());
        c.extend_from_slice(&(p.len() as u32).to_le_bytes());
        for e in echelles { c.extend_from_slice(&e.to_le_bytes()); }
        c.extend_from_slice(&p);
        c
    }

    #[test]
    fn mode4_un_etat_se_decode_comme_le_mode2() {
        // 28 blocs (896 canaux / 32), une seule paire non nulle : canal 40, +3,
        // échelle du bloc 1 (canaux 32..63) = 0,5 → la valeur attendue est 1,5.
        let mut echelles = vec![0f32; 28];
        echelles[1] = 0.5;
        let corps = etat_forge(&[(40, 3)], 28, &echelles);
        let f = decoder_une_trame(MODE_LOT_LISTES, 1, corps, 896).unwrap();
        let x = f.charge.plat().to_vec();
        assert_eq!(x.len(), 896, "un état = une ligne de `hidden` canaux");
        assert!((x[40] - 1.5).abs() < 1e-6, "canal 40 = 3 × 0,5 = 1,5, vu {}", x[40]);
        assert!(x.iter().enumerate().all(|(i, v)| i == 40 || *v == 0.0));
    }

    #[test]
    fn mode4_deux_etats_dans_un_flux() {
        let mut e1 = vec![0f32; 28];
        e1[0] = 1.0;
        let mut e2 = vec![0f32; 28];
        e2[0] = 2.0;
        let mut corps = etat_forge(&[(5, 7)], 28, &e1);
        corps.extend_from_slice(&etat_forge(&[(6, -7)], 28, &e2));
        let f = decoder_une_trame(MODE_LOT_LISTES, 2, corps, 896).unwrap();
        let x = f.charge.plat().to_vec();
        assert_eq!(x.len(), 2 * 896);
        assert!((x[5] - 7.0).abs() < 1e-6, "premier état : {}", x[5]);
        assert!((x[896 + 6] + 14.0).abs() < 1e-6, "second état : {}", x[896 + 6]);
    }

    #[test]
    fn mode4_prefixe_incoherent_est_refuse() {
        // Le nombre de blocs doit être ⌈hidden/32⌉ : 27 au lieu de 28 signale deux
        // nœuds qui n'ont pas le même GGUF, et c'est mieux que de lire au hasard.
        let corps = etat_forge(&[(5, 7)], 27, &vec![1.0f32; 27]);
        let r = decoder_une_trame(MODE_LOT_LISTES, 1, corps, 896);
        assert!(r.is_err(), "27 blocs pour 896 canaux doivent être refusés");
        // Une longueur de paires incohérente avec le nombre d'actifs aussi.
        let mut corps = etat_forge(&[(5, 7)], 28, &vec![1.0f32; 28]);
        corps[8..12].copy_from_slice(&100u32.to_le_bytes());   // longueur = 100 pour 1 actif
        let r = decoder_une_trame(MODE_LOT_LISTES, 1, corps, 896);
        assert!(r.is_err(), "100 octets de paires pour 1 actif doivent être refusés");
    }

    #[test]
    fn zero_element_est_refuse_seulement_ou_c_est_une_dimension() {
        // Mode 0 : zéro CANAL n'a pas de sens. Modes 3 et 4 : zéro ÉTAT non plus.
        for mode in [MODE_DENSE, MODE_LOT] {
            let r = decoder_une_trame(mode, 0, Vec::new(), 896);
            assert!(r.is_err(), "mode {mode} : un flux de zéro élément doit être refusé");
            let msg = format!("{}", r.err().unwrap());
            assert!(msg.contains("zéro"), "le refus doit dire pourquoi : {msg}");
        }
        // Modes 1 et 2 : `n` est un nombre de PAIRES, et une liste VIDE est
        // légitime — un vecteur d'activation peut n'avoir aucun actif (seuil
        // au-dessus du maximum), et c'est ce que répond le pair factice du dépôt.
        // Refuser n == 0 partout tuait ces sessions (relecture adversariale du
        // mode 4 : `--flux-blocs --act-thresh 1.0 --lot 1` mourait).
        for mode in [MODE_LISTE, MODE_BLOCS] {
            let corps = if mode == MODE_LISTE { Vec::new() } else {
                etat_forge(&[], 28, &vec![0f32; 28])
            };
            let r = decoder_une_trame(mode, 0, corps, 896);
            assert!(r.is_ok(), "mode {mode} : une liste vide doit être ACCEPTÉE");
            assert!(r.unwrap().charge.en_dense(896).iter().all(|v| *v == 0.0));
        }
    }

    /// Le livelock du contexte : `KvCache::assurer(besoin)` avec `besoin > ctx`
    /// bouclait SANS FIN (`while cap < besoin { cap = (cap * 2).min(self.ctx) }`).
    /// Un test qui boucle est un test qui pend : celui-ci doit rendre la main.
    #[test]
    fn assurer_ne_boucle_pas_au_dela_du_contexte() {
        let mut c = model::KvCache::new(32, 2, 16, 8);   // ctx = 16 positions
        c.assurer(1000);          // 1000 >> 16 : la boucle doit se terminer
        assert!(c.cap <= 16, "capacité {} au-delà du contexte 16", c.cap);
        c.assurer(8);
        assert!(c.cap <= 16);
        // Et la BOUCLE elle-même, pas seulement le plafond : un cache de 4096
        // positions démarre à 1024 (`new` assure `ctx.min(1024)`), donc
        // `assurer(3000)` exécute vraiment les doublements, puis `assurer(10000)`
        // dépasse le contexte et doit rendre la main.
        let mut grand = model::KvCache::new(32, 2, 4096, 8);
        assert!(grand.cap < 3000);
        grand.assurer(3000);
        assert!(grand.cap >= 3000 && grand.cap <= 4096);
        grand.assurer(10_000);
        assert!(grand.cap <= 4096, "capacité {} au-delà du contexte 4096", grand.cap);
        // L'invariant du chemin d'écriture : au-delà du contexte, on ne corrompt
        // pas le bloc de la tête KV suivante.
        let mut c2 = model::KvCache::new(32, 2, 4, 8);
        let (k, v) = (vec![1.0f32; 8], vec![2.0f32; 8]);
        c2.ecrire(0, 3, &k, &v);
        c2.ecrire(0, 99, &k, &v);   // hors contexte : ignoré, pas de panique
        c2.ecrire(1, 99, &k, &v);
    }

    #[test]
    fn un_nombre_de_blocs_dement_grand_est_refuse() {
        // mode blocs : `n_blocs` vient de l'en-tête et servait à allouer
        // `n_blocs × 4` octets + un Vec<f32> (mesuré : 16 Gio sur une trame de
        // 83 octets). Le plafond doit refuser AVANT d'allouer.
        let mut corps = Vec::new();
        corps.extend_from_slice(&100_000_000u32.to_le_bytes());
        let r = decoder_une_trame(MODE_BLOCS, 1, corps, 896);
        assert!(r.is_err(), "100 millions de blocs doivent être refusés");
        let msg = format!("{}", r.err().unwrap());
        assert!(msg.contains("plafond"), "le refus doit nommer le plafond : {msg}");
    }

    #[test]
    fn un_lot_dement_grand_est_refuse_avant_allocation() {
        let ecoute = TcpListener::bind("127.0.0.1:0").unwrap();
        let adresse = ecoute.local_addr().unwrap();
        let serveur = std::thread::spawn(move || {
            let (mut sock, _) = ecoute.accept().unwrap();
            // en-tête v4 complet, mode lot, n = 100 millions d'états
            let mut tete: Vec<u8> = Vec::new();
            tete.extend_from_slice(&MAGIE_FLUX.to_le_bytes());
            tete.push(VERSION_FLUX);
            tete.push(MODE_LOT);
            tete.extend_from_slice(&12u32.to_le_bytes());
            tete.extend_from_slice(&24u32.to_le_bytes());
            tete.extend_from_slice(&0u32.to_le_bytes());
            tete.extend_from_slice(&100_000_000u32.to_le_bytes());
            tete.extend_from_slice(&0f32.to_le_bytes());
            tete.extend_from_slice(&127f32.to_le_bytes());
            tete.extend_from_slice(&0f32.to_le_bytes());
            tete.extend_from_slice(&0u32.to_le_bytes());
            tete.push(0);
            while tete.len() < TAILLE_TETE { tete.extend_from_slice(&0u32.to_le_bytes()); }
            assert_eq!(tete.len(), TAILLE_TETE);
            sock.write_all(&tete).unwrap();
            // Pas de lecture ici : le client refuse AVANT de lire le corps, donc
            // il ne renverra rien — l'ancienne version de ce test se bloquait
            // pour toujours sur cette lecture (et le test ne finissait jamais).
        });
        let mut client = TcpStream::connect(adresse).unwrap();
        client.set_read_timeout(Some(std::time::Duration::from_secs(5))).unwrap();
        let r = recevoir_flux(&mut client, 896, 1);
        assert!(r.is_err(), "un lot de 100 millions d'états doit être refusé");
        let msg = format!("{}", r.err().unwrap());
        assert!(msg.contains("plafond"), "le refus doit nommer le plafond : {msg}");
        serveur.join().unwrap();
    }
}

#[cfg(test)]
mod tests_vars {
    use super::VARS_LUES;

    /// Le source de `src/`, concaténé, pour y chercher les noms lus.
    fn source() -> String {
        let mut tout = String::new();
        for e in std::fs::read_dir("src").expect("src/ lisible depuis drave-core") {
            let c = e.unwrap().path();
            if c.extension().map(|x| x == "rs").unwrap_or(false) {
                tout.push_str(&std::fs::read_to_string(&c).unwrap());
                tout.push('\n');
            }
        }
        tout
    }

    /// Tout nom `DRAVE_*` cité dans le source doit être dans `VARS_LUES`, et
    /// réciproquement. Sans ce test la liste pourrit en silence : c'est
    /// exactement ce qui a produit le faux avertissement `QT_IM_MODULE`.
    #[test]
    fn les_vars_lues_sont_completes() {
        let src = source();
        let mut citees: Vec<String> = Vec::new();
        let mut reste = src.as_str();
        while let Some(p) = reste.find("DRAVE_") {
            let apres = &reste[p + "DRAVE_".len()..];
            let fin = apres.find(|c: char| !(c.is_ascii_uppercase() || c.is_ascii_digit() || c == '_'))
                .unwrap_or(apres.len());
            let nom = &apres[..fin];
            if !nom.is_empty() && !citees.iter().any(|c| c == nom) {
                citees.push(nom.to_string());
            }
            reste = &apres[fin..];
        }
        for c in &citees {
            assert!(VARS_LUES.contains(&c.as_str()),
                    "DRAVE_{c} est lu dans le source mais absent de VARS_LUES : \
un ancien nom QT_{c} resterait muet");
        }
        for v in VARS_LUES {
            assert!(citees.iter().any(|c| c == v),
                    "VARS_LUES annonce {v} mais aucune lecture DRAVE_{v} dans le source");
        }
    }

    /// Le piège qui a motivé ce module : les variables de Qt ne sont pas les
    /// nôtres, et ne doivent jamais être signalées comme des noms hérités.
    #[test]
    fn les_vars_qt_ne_sont_pas_des_notres() {
        for piege in ["QT_IM_MODULE", "QT_IM_SWITCHER", "QT_QPA_PLATFORM",
                      "QT_SCALE_FACTOR", "QT_AUTO_SCREEN_SCALE_FACTOR"] {
            let suffixe = piege.strip_prefix("QT_").unwrap();
            assert!(!VARS_LUES.contains(&suffixe),
                    "{piege} appartient à Qt, pas au moteur : le signaler ferait \
un avertissement à chaque lancement en session graphique");
        }
    }
}
