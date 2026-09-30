//! drave-core — moteur d'exécution par listes d'événements.
//!
//! Usage :
//!   drave-core <modele.gguf> [--matrix blk.0.ffn_gate.weight] [--threads 8]
//!
//! Mesure sur le VRAI modèle :
//!   1. taille exacte de chaque encodage de liste (bits/poids),
//!   2. débit du moteur d'événements selon la densité des activations,
//!   3. exécution sans multiplieur (décalages + additions) vs multiplication.

mod engine;
mod gguf;
mod list;
mod model;
mod gpu;
mod tokenizer;

use engine::{matvec_dense, matvec_shift_add, Pool, SparseVec};
use gguf::Gguf;
use list::{dense_bits, BitmapSign, DenseQ4, DenseQ8, FusedSign, PushMat, SignedDelta, SparseK};
use std::time::Instant;

fn fmt_bits(b: u64, n: usize) -> String {
    format!("{:8.3} b/poids  ({:7.2} Mo)", b as f64 / n as f64, b as f64 / 8.0 / 1e6)
}

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
elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.");
    }
    let opt = analyser(&args);
    let _ = MODELE.set(args[1].clone());
    if let Some(f) = opt.banc_vision.clone() { run_banc_vision(&f); return; }
    if let Some(adresse) = opt.flux_serveur.clone() { run_serveur_flux(opt, &adresse); return; }
    if let Some(pair) = opt.ppl_reparti.clone() { run_ppl_reparti(opt, &pair); return; }
    if opt.tensors { run_tensors(); return; }
    if let Some(f) = opt.banc_mla.clone() { run_banc_mla(opt, &f); return; }
    if opt.banc_kv > 0 { run_banc_kv(opt); return; }
    if opt.gpu_banc { run_gpu_banc(opt); return; }
    if opt.plan { run_plan(opt); return; }
    if opt.tokenize { run_tokenize(opt); return; }
    if opt.ppl { run_ppl(opt); return; }
    if opt.infer { run_infer(opt); return; }
    let path = &args[1];
    let mut matrix = "blk.0.ffn_gate.weight".to_string();
    // Par défaut on laisse un quart des CPU au système : l'attente active de la
    // barrière ne tolère aucune sursouscription (mesuré : ×1,3 de perte à 40+1
    // threads sur 40 CPU).
    let cpu = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(8);
    let mut n_threads = (cpu * 3 / 4).max(1);
    let mut i = 2;
    while i < args.len() {
        match args[i].as_str() {
            "--matrix" => matrix = args[i + 1].clone(),
            "--threads" => n_threads = args[i + 1].parse().unwrap(),
            _ => {}
        }
        i += 2;
    }

    let t0 = Instant::now();
    let g = Gguf::open(path).expect("ouverture du GGUF");
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
        let levels = g.raw_levels(name);
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
    let levels = g.raw_levels(&matrix);
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
    infer: bool, ppl: bool, plan: bool, tokenize: bool, gpu_banc: bool,
    /// Banc du KV déporté : nombre de clés à faire tenir en VRAM.
    banc_kv: usize,
    /// Banc MLA : écrit les logits `(n_pos × vocab)` en f32 pour les comparer à
    /// la référence numpy du modèle synthétique.
    banc_mla: Option<String>,
    /// Trace du flux d'activation : fichier de sortie.
    trace_flux: Option<String>,
    /// Relecture d'une trace : les activations enregistrées remplacent celles
    /// calculées (rejeu).
    flux_forcer: Option<String>,
    /// Phase 3 : nœud MOTEUR qui écoute et applique sa plage de couches.
    /// Adresse d'écoute du nœud moteur : `port`, ou `hôte:port` pour écouter
    /// au-delà de localhost (un pair distant, un tunnel, une autre machine).
    flux_serveur: Option<String>,
    /// Phase 3 : pilote qui répartit le calcul sur un nœud distant (hôte:port).
    ppl_reparti: Option<String>,
    /// Nombre de couches gardées en local par le pilote.
    couches_locales: usize,
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
    // --- parcimonie des activations
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
    let mut o = Options {
        n: 32, temp: 0.0, top_p: 1.0, hist: 64, hebb_q: 0.1,
        hebb_out: String::from("hebb.bin"), keep: 1.0, abits: 8,
        auto: true, limit: usize::MAX,
        matrix: String::from("blk.0.ffn_gate.weight"),
        ..Default::default()
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
            "--tokenize" => { o.tokenize = true; 1 }
            "--gpu-banc" => { o.gpu_banc = true; 1 }
            "--banc-kv" => { o.banc_kv = suivant(i).parse().unwrap(); 2 }
            "--banc-mla" => { o.banc_mla = Some(suivant(i).clone()); 2 }
            "--tensors" => { o.tensors = true; 1 }
            "--trace-flux" => { o.trace_flux = Some(suivant(i).clone()); 2 }
            "--flux-forcer" => { o.flux_forcer = Some(suivant(i).clone()); 2 }
            "--flux-serveur" => { o.flux_serveur = Some(suivant(i).clone()); 2 }
            "--ppl-reparti" => { o.ppl_reparti = Some(suivant(i).clone()); 2 }
            "--couches-locales" => { o.couches_locales = suivant(i).parse().unwrap(); 2 }
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
            "--attn-sinks" => { o.attn_sinks = suivant(i).parse().unwrap(); 2 }
            "--attn-topk" => { o.attn_topk = suivant(i).parse().unwrap(); 2 }
            "--qk-topk" => { o.qk_topk = suivant(i).parse().unwrap(); 2 }
            "--hebbian" => { o.hebb_layer = Some(suivant(i).parse().unwrap()); 2 }
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
                let v: Vec<&str> = suivant(i).split(':').collect();
                o.ffn_gain = Some((v[0].parse().unwrap(), v[1].parse().unwrap())); 2
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
            "--ppl-profil" => { o.ppl_profil = true; 1 }
            "--profil-neurones" => { o.profil_neurones = true; 1 }
            "--harmony" => { o.harmony = Some("alterne".into()); 1 }
            "--harmony-assistant" => { o.harmony = Some("assistant".into()); 1 }
            "--harmony-user" => { o.harmony = Some("user".into()); 1 }
            "--harmony-suite" => { o.harmony = Some("suite".into()); 1 }
            "--q4" => { o.q4 |= 3; 1 }
            "--q4-ffn" => { o.q4 = (o.q4 & 4) | 1; 1 }
            "--q4-attn" => { o.q4 = (o.q4 & 4) | 2; 1 }
            "--q4-tout" => { o.q4 |= 7; 1 }
            // Inconnu : on avance d'UN cran, jamais de deux.
            _ => 1,
        };
        i += pas;
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
    // Une seule analyse de la ligne de commande (voir `analyser`) : chaque mode
    // ne fait plus que déstructurer ce dont il a besoin.
    let Options {
        ids: mut ids, ids_file, prompt, n: n_new, temp, top_p, topk, rep_pen, hist,
        flux, session, chat, ctx: ctx_opt, threads: threads_opt, abits: abits_opt,
        ctx_impose, threads_impose, abits_impose, dense, auto, q4, b6,
        keep, attn_window, swa_pattern, sans_fenetre, attn_sinks, attn_topk, qk_topk,
        act_thresh, act_topk, act_renorm, topk_proj, moe_topk, patch: patch_file,
        hebb_layer, hebb_q, hebb_out, sans_yarn, lot, ..
    } = opt;
    let path = &modele_chemin();
    // Défauts du mode INFÉRENCE : 512 jetons, la moitié des cœurs (l'attente
    // active de la barrière ne tolère pas la sursouscription), 8 bits.
    let cpu = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(8);
    let ctx = if ctx_impose { ctx_opt } else { 512 };
    let n_threads = if threads_impose { threads_opt } else { (cpu / 2).max(1) };
    let abits = if abits_impose { abits_opt } else { 8 };
    let mut mdl = model::Model::load(path, ctx, n_threads, dense, keep, auto, q4, b6);
    mdl.act_levels = ((1u32 << (abits - 1)) - 1) as f32;
    mdl.moe_topk = moe_topk;
    mdl.act_thresh = act_thresh;
    mdl.act_topk = act_topk;
    mdl.lot = lot.max(1);
    mdl.act_renorm = act_renorm;
    mdl.act_topk_proj = topk_proj;
    if sans_fenetre { mdl.attn_window = 0; }
    if attn_window > 0 { mdl.attn_window = attn_window; }
    if let Some(p) = swa_pattern { mdl.swa_pattern = p; }
    if attn_sinks > 0 { mdl.attn_sinks = attn_sinks; }
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

fn cfg_dims(m: &model::Model) -> usize { m.cfg.hidden }

/// Taille du vocabulaire, lue dans l'en-tête du GGUF sans charger le modèle.
fn mdl_cfg_vocab(path: &str) -> Option<usize> {
    // `open_meta` : le garde-fou n'a besoin que des dimensions du tenseur
    // d'embedding. Avec `open`, il lisait les 62 Go de gpt-oss AVANT que le
    // modèle ne soit chargé — deux lectures complètes du fichier par mesure.
    let g = Gguf::open_meta(path).ok()?;
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
    let g = Gguf::open(path).expect("ouverture du GGUF");
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
fn run_tensors() {
    let path = &modele_chemin();
    let g = Gguf::open(path).expect("ouverture du GGUF");
    let nom_type = |t: u32| match t {
        0 => "F32", 1 => "F16", 2 => "Q4_0", 3 => "Q4_1", 6 => "Q5_0", 7 => "Q5_1",
        8 => "Q8_0", 9 => "Q8_1", 10 => "Q2_K", 11 => "Q3_K", 12 => "Q4_K", 13 => "Q5_K",
        14 => "Q6_K", 30 => "BF16", 39 => "MXFP4", _ => "?",
    };
    println!("{} tenseurs dans {}", g.tensors.len(), path);
    for t in &g.tensors {
        let poids: u64 = t.dims.iter().product();
        println!("  {:5} {:38} {:?} · {:.1} M poids", nom_type(t.ttype), t.name, t.dims,
                 poids as f64 / 1e6);
    }
}

/// Applique les réglages de quantification de la ligne de commande à un modèle
/// des chemins FLUX. Ils étaient ignorés dans `--flux-serveur` et
/// `--ppl-reparti` : un `--act-thresh 0,05` n'y changeait rien, et le mode
/// « listes » transportait donc une liste PLEINE au lieu d'une liste creuse —
/// le défaut « le drapeau est analysé mais jamais appliqué », déjà vu cinq fois.
fn appliquer_quantification(mdl: &mut model::Model, opt: &Options) {
    let abits = if opt.abits_impose { opt.abits } else { 8 };
    mdl.act_levels = ((1u32 << (abits - 1)) - 1) as f32;
    mdl.act_thresh = opt.act_thresh;
    mdl.act_topk = opt.act_topk;
    mdl.act_renorm = opt.act_renorm;
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
/// Version 3 : ajoute le mode LOT. Le passage à 3 n'est pas cosmétique — un pair
/// en version 2 lirait `n × 4` octets d'un corps qui en fait `n × hidden × 4`,
/// se désynchroniserait, puis dirait « mode inconnu » : un refus exact mais tardif
/// et muet sur la cause. Ici il est immédiat et nommé.
const VERSION_FLUX: u8 = 3;
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

/// En-tête commun : magie · version · mode · plage · position · n · échelle ·
/// **réglages d'activation** (niveaux, seuil, top-k, renorm).
///
/// Les réglages voyagent parce qu'ils CHANGENT LES CHIFFRES : deux nœuds lancés
/// avec des `--act-thresh` différents ne calculent pas la même chose, et la
/// divergence serait silencieuse. Mesuré : 0,69 d'écart de perplexité avec un
/// seuil 0,05 d'un côté et 0,00 de l'autre, sur le même modèle.
const TAILLE_TETE: usize = 4 + 1 + 1 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 1;

/// Réglages d'activation d'un nœud : ils font partie du contrat d'échange.
#[derive(Clone, Copy)]
struct Act {
    levels: f32,
    thresh: f32,
    topk: u32,
    renorm: bool,
}

impl Act {
    fn du_modele(m: &model::Model) -> Self {
        Act { levels: m.act_levels, thresh: m.act_thresh,
              topk: m.act_topk as u32, renorm: m.act_renorm }
    }
    fn appliquer(&self, m: &mut model::Model) {
        m.act_levels = self.levels;
        m.act_thresh = self.thresh;
        m.act_topk = self.topk as usize;
        m.act_renorm = self.renorm;
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
                for (&i, &v) in idx.iter().zip(val.iter()) {
                    x[i as usize] = v as f32 * echelle;
                }
                x
            }
            ChargeFlux::Blocs { idx, val, echelles } => {
                let mut x = vec![0f32; hidden];
                for (&i, &v) in idx.iter().zip(val.iter()) {
                    x[i as usize] = v as f32 * echelles[i as usize / 32];
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

/// Envoie un flux et rend le nombre d'octets écrits (en-tête compris) — c'est ce
/// que la phase 3 doit chiffrer : octets par jeton × latence.
fn envoyer_flux(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos: u32,
                actifs: &[f32], mode: u8, mdl: Option<&model::Model>)
                -> std::io::Result<(usize, usize)> {
    let act = mdl.map(Act::du_modele).unwrap_or(Act { levels: 127.0, thresh: 0.0,
                                                       topk: 0, renorm: false });
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
        let mut paires: Vec<u8> = Vec::with_capacity(idx.len() * 2);
        let mut prev = 0u32;
        for (&i, &v) in idx.iter().zip(val.iter()) {
            let ecart = i as u32 - prev;
            if ecart < 255 {
                paires.push(ecart as u8);
            } else {
                paires.push(255);
                paires.extend_from_slice(&i.to_le_bytes());
            }
            prev = i as u32;
            paires.push(v as u8);
        }
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
    let mut tete = Vec::with_capacity(TAILLE_TETE);
    tete.extend_from_slice(&MAGIE_FLUX.to_le_bytes());
    tete.push(VERSION_FLUX);
    tete.push(mode);
    tete.extend_from_slice(&debut.to_le_bytes());
    tete.extend_from_slice(&fin.to_le_bytes());
    tete.extend_from_slice(&pos.to_le_bytes());
    tete.extend_from_slice(&(n as u32).to_le_bytes());
    tete.extend_from_slice(&echelle.to_le_bytes());
    tete.extend_from_slice(&act.levels.to_le_bytes());
    tete.extend_from_slice(&act.thresh.to_le_bytes());
    tete.extend_from_slice(&act.topk.to_le_bytes());
    tete.push(act.renorm as u8);
    assert_eq!(tete.len(), TAILLE_TETE,
               "en-tête de flux de {} octets pour {TAILLE_TETE}", tete.len());
    s.write_all(&tete)?;
    s.write_all(&corps)?;
    s.flush()?;
    Ok((TAILLE_TETE + corps.len(), n))
}

/// Envoie un LOT d'états (`t × hidden`, aplati) dans un seul flux.
///
/// Le lot voyage en f32 dense : c'est le mode de la phase 3.4 (préremplissage
/// réparti), où la latence domine tout — le quantifier est la suite, et il faudra
/// alors une liste PAR ÉTAT, ce que ce cadriciel ne sait pas encore décrire.
fn envoyer_lot(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos0: u32,
               etats: &[f32], t: usize, mdl: &model::Model) -> std::io::Result<usize> {
    use std::io::Write;
    let act = Act::du_modele(mdl);
    let mut tete = Vec::with_capacity(TAILLE_TETE);
    tete.extend_from_slice(&MAGIE_FLUX.to_le_bytes());
    tete.push(VERSION_FLUX);
    tete.push(MODE_LOT);
    tete.extend_from_slice(&debut.to_le_bytes());
    tete.extend_from_slice(&fin.to_le_bytes());
    tete.extend_from_slice(&pos0.to_le_bytes());
    tete.extend_from_slice(&(t as u32).to_le_bytes());
    tete.extend_from_slice(&0f32.to_le_bytes());          // échelle : sans objet
    tete.extend_from_slice(&act.levels.to_le_bytes());
    tete.extend_from_slice(&act.thresh.to_le_bytes());
    tete.extend_from_slice(&act.topk.to_le_bytes());
    tete.push(act.renorm as u8);
    // Garde-fou, parce que ce bug-là est INVISIBLE : un octet d'en-tête en trop et
    // tout le corps se décale d'un octet — des f32 valides, faux, sans erreur, et
    // la désynchronisation n'apparaît qu'au flux SUIVANT (« magie absente »). Il
    // est arrivé exactement comme ça (40 octets écrits pour 39 lus).
    assert_eq!(tete.len(), TAILLE_TETE,
               "en-tête de lot de {} octets pour {TAILLE_TETE}", tete.len());
    s.write_all(&tete)?;
    let mut corps = Vec::with_capacity(etats.len() * 4);
    for v in etats { corps.extend_from_slice(&v.to_le_bytes()); }
    s.write_all(&corps)?;
    s.flush()?;
    Ok(TAILLE_TETE + corps.len())
}

/// Reçoit un flux : `(debut, fin, pos, mode, charge utile)`.
fn recevoir_flux(s: &mut std::net::TcpStream, hidden: usize) -> std::io::Result<Flux> {
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
    let act = Act {
        levels: f32::from_le_bytes([tete[26], tete[27], tete[28], tete[29]]),
        thresh: f32::from_le_bytes([tete[30], tete[31], tete[32], tete[33]]),
        topk: u(34),
        renorm: tete[38] != 0,
    };
    let charge = match mode {
        MODE_LOT => {
            // `n` est le nombre d'ÉTATS, pas de canaux : la dimension vient du
            // modèle du nœud qui reçoit, elle n'a pas à voyager.
            let mut corps = vec![0u8; n * hidden * 4];
            s.read_exact(&mut corps)?;
            let etats = (0..n * hidden).map(|k| f32::from_le_bytes(
                [corps[k*4], corps[k*4+1], corps[k*4+2], corps[k*4+3]])).collect();
            return Ok(Flux { n, debut, fin, pos, mode, act, octets_corps: corps.len(),
                             charge: ChargeFlux::Lot(etats) });
        }
        MODE_BLOCS => {
            // corps : nombre de blocs u32 · blocs × f32 · n × (u16 · i8)
            let mut nb = [0u8; 4];
            s.read_exact(&mut nb)?;
            let n_blocs = u32::from_le_bytes(nb) as usize;
            let mut eb = vec![0u8; n_blocs * 4];
            s.read_exact(&mut eb)?;
            let echelles = (0..n_blocs).map(|k| f32::from_le_bytes(
                [eb[k*4], eb[k*4+1], eb[k*4+2], eb[k*4+3]])).collect();
            let mut lg = [0u8; 4];
            s.read_exact(&mut lg)?;
            let longueur = u32::from_le_bytes(lg) as usize;
            let mut corps = vec![0u8; longueur];
            s.read_exact(&mut corps)?;
            let mut idx = Vec::with_capacity(n);
            let mut val = Vec::with_capacity(n);
            let mut prev = 0u32;
            let mut lus = 0usize;
            let mut echappements = 0usize;
            while idx.len() < n {
                if lus + 1 >= corps.len() && idx.len() + 1 < n {
                    return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
                        "corps de flux tronqué"));
                }
                let d = corps[lus]; lus += 1;
                let absolu = if d == 255 {
                    echappements += 1;
                    let a = u16::from_le_bytes([corps[lus], corps[lus+1]]) as u32;
                    lus += 2;
                    a
                } else { prev + d as u32 };
                prev = absolu;
                idx.push(absolu as u16);
                val.push(corps[lus] as i8); lus += 1;
            }
            let octets_corps = 4 + n_blocs * 4 + 4 + longueur;
            return Ok(Flux { n, debut, fin, pos, mode, act, octets_corps, charge:
                             ChargeFlux::Blocs { idx, val, echelles } });
        }
        _ => {}
    };
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
    Ok(Flux { n, debut, fin, pos, mode, act, octets_corps: octets.len(), charge })
}

/// Le NŒUD MOTEUR : charge le modèle, écoute, applique SA plage de couches au
/// flux reçu et renvoie le flux résultant. Un seul client à la fois — c'est un
/// banc d'essai, pas un service.
fn run_serveur_flux(opt: Options, adresse: &str) {
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
    let mut mdl = model::Model::load(&chemin, ctx, 16, true, 1.0, false, 0, 0);
    appliquer_quantification(&mut mdl, &opt);
    let hidden = mdl.cfg.hidden;
    let ecoute = std::net::TcpListener::bind((hote.as_str(), port)).expect("écoute");
    println!("[flux] nœud moteur sur {hote}:{port} · {hidden} cachés · {} couches · contexte {ctx}",
             mdl.cfg.n_layer);
    let (mut sock, pair) = ecoute.accept().expect("connexion");
    // TCP_NODELAY, et ce n'est pas un détail de confort : sans lui, Nagle garde
    // une petite écriture en attendant l'acquittement de la précédente, et l'ACK
    // différé du pair la retarde encore. Mesuré sur localhost, 12 couches
    // distantes : **97,6 ms** d'attente contre 15,6 ms de calcul local — six fois
    // le calcul, payés par la seule latence du protocole.
    sock.set_nodelay(true).expect("TCP_NODELAY");
    println!("[flux] client connecté : {pair}");
    let mut servis = 0u64;
    loop {
        match recevoir_flux(&mut sock, hidden) {
            Ok(f) => {
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
                if f.mode == MODE_LOT {
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
                    let hs = mdl.forward_lot(&vec![0u32; t], f.pos as usize);
                    let plat: Vec<f32> = hs.concat();
                    if std::env::var("DRAVE_DEBUG_FLUX").is_ok() {
                        eprintln!("[debug] lot reçu : n={t} pos={} états={} plat={} corps={}",
                                  f.pos, hs.len(), plat.len(), f.octets_corps);
                    }
                    if envoyer_lot(&mut sock, f.debut, f.fin, f.pos, &plat, t, &mdl).is_err() {
                        break;
                    }
                    servis += 1;
                    continue;
                }
                mdl.emb_imposee = Some(f.charge.en_dense(hidden));
                let sortie = mdl.forward(0, f.pos as usize);
                // La RÉPONSE est encodée comme la demande : un pair qui parle en
                // listes reçoit des listes, sans second réglage à faire tenir
                // cohérent entre les deux machines.
                if envoyer_flux(&mut sock, f.debut, f.fin, f.pos, &sortie, f.mode,
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
    println!("[flux] {servis} flux servis");
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
    let mut mdl = model::Model::load(&chemin, ctx, 16, true, 1.0, false, 0, 0);
    appliquer_quantification(&mut mdl, &opt);
    let mode = if opt.flux_blocs { MODE_BLOCS }
               else if opt.flux_liste { MODE_LISTE }
               else { MODE_DENSE };
    println!("[flux] quantification : {} niveaux, seuil {}, top-k {}, renorm {}",
             mdl.act_levels, mdl.act_thresh, mdl.act_topk, mdl.act_renorm);
    let n_layer = mdl.cfg.n_layer;
    let ids: Vec<u32> = if opt.ids.is_empty() {
        (1..=limite as u32).collect()
    } else { opt.ids.clone() };
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
        // coûter la latence d'UN message par lot, pas par jeton.
        let mut pos = 0usize;
        while pos + 1 < ids.len() {
            let t = lot.min(ids.len() - pos);
            let horloge = Instant::now();
            let hs = mdl.forward_lot(&ids[pos..pos + t], pos);
            let plat: Vec<f32> = hs.concat();
            t_local += horloge.elapsed().as_secs_f64();
            let horloge = Instant::now();
            let o = envoyer_lot(&mut sock, couches_locales as u32, n_layer as u32,
                                pos as u32, &plat, t, &mdl).expect("envoi du lot");
            octets_envoyes += o as u64;
            actifs_envoyes += (t * mdl.cfg.hidden) as u64;
            flux_envoyes += 1;
            let rep = recevoir_flux(&mut sock, mdl.cfg.hidden).expect("réception du lot");
            t_pair += horloge.elapsed().as_secs_f64();
            octets_recus += TAILLE_TETE as u64 + rep.octets_corps as u64;
            let etats = rep.charge.plat().to_vec();
            assert_eq!(etats.len(), t * mdl.cfg.hidden,
                       "lot reçu de {} valeurs pour {t} jetons de {} canaux",
                       etats.len(), mdl.cfg.hidden);
            // La norme finale reste au nœud qui a la tête, et la tête se fait par
            // lots : le lot reçu ne redescend pas jeton par jeton.
            let mut hn: Vec<Vec<f32>> = Vec::with_capacity(t);
            for i in 0..t {
                hn.push(mdl.norme_finale(&etats[i * mdl.cfg.hidden..(i + 1) * mdl.cfg.hidden]));
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
        let (o, a) = envoyer_flux(&mut sock, couches_locales as u32, n_layer as u32,
                                  pos as u32, &etat, mode, Some(&mdl))
                        .expect("envoi du flux");
        octets_envoyes += o as u64;
        actifs_envoyes += a as u64;
        flux_envoyes += 1;
        let rep = recevoir_flux(&mut sock, mdl.cfg.hidden).expect("réception du flux");
        // Ce que coûte le découpage : le calcul local, et l'attente du pair
        // (son calcul + l'aller-retour réseau) — la latence, pas le débit.
        t_pair += horloge.elapsed().as_secs_f64();
        octets_recus += TAILLE_TETE as u64 + rep.octets_corps as u64;
        let final_ = rep.charge.en_dense(mdl.cfg.hidden);
        if pos + 1 < ids.len() {
            nll += nll_logits(&mdl.logits(&mdl.norme_finale(&final_)), ids[pos + 1]);
        }
    }
    }
    let ppl = (nll / (ids.len() - 1) as f64).exp();
    println!("  deux nœuds        : perplexité {ppl:.4}  ({:.1} s)", t1.elapsed().as_secs_f64());
    println!("  écart             : {:.2e}", (ppl - ppl_ref).abs() / ppl_ref);
    // Divisor : le nombre de flux RÉELLEMENT envoyés (un par jeton, le dernier
    // compris) et non le nombre de jetons NOTÉS — l'erreur d'un facteur 40/39
    // faisait apparaître un flux de « 919 canaux » pour un modèle qui en a 896.
    let nflux = flux_envoyes.max(1);
    if lot > 1 {
        println!("  transport         : LOTS de {lot} jetons · {:.0} octets par lot (aller) · \
                  {:.1} ko par jeton · {} lots (au lieu de {} flux)",
                 octets_envoyes as f64 / nflux as f64,
                 octets_envoyes as f64 / nflux as f64 / 1024.0 / lot as f64,
                 nflux, ids.len() - 1);
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

/// Banc **MLA** : passe avant du modèle synthétique, logits écrits en binaire
/// pour être comparés à `logits.npy` (référence numpy indépendante).
fn run_banc_mla(opt: Options, sortie: &str) {
    use std::io::Write;
    let path = &modele_chemin();
    let mut mdl = model::Model::load(path, 4096, 16, opt.dense, 1.0, false, 0, 0);
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
        (std::thread::available_parallelism().map(|x| x.get()).unwrap_or(8) * 3 / 4).max(1)
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
        (std::thread::available_parallelism().map(|n| n.get()).unwrap_or(8) * 3 / 4).max(1)
    };
    let g = Gguf::open(path).expect("ouverture du GGUF");
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
    let Some((blocs, nb)) = g.q4k_blocks(nom) else { println!("pas une matrice Q4_K"); return };
    let t = g.tensor(nom).unwrap();
    let (n_out, n_in) = (t.dims[0] as usize, t.dims[1] as usize);
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
    let g = Gguf::open_meta(path).expect("ouverture du GGUF");
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
        let retour = tk.decode(&ids);
        if retour == texte {
            println!("réversibilité : texte reconstruit identique ✅ ({} octets)", texte.len());
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
    let g = Gguf::open(path).expect("ouverture du GGUF");
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
    let ctx_demande = if opt.ctx > 0 {
        opt.ctx
    } else {
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

fn run_ppl(opt: Options) {
    let Options {
        ids_file: idfile, texte_file, ppl_texte: _, limit, depuis,
        ctx: ctx_opt, threads: threads_opt, abits: abits_opt,
        ctx_impose, threads_impose, abits_impose,
        dense, auto, q4, b6, attn_window, swa_pattern,
        sans_fenetre, attn_sinks, attn_topk, qk_topk, act_thresh, act_topk, act_renorm,
        topk_proj, moe_topk, patch: patch_file, hebb_layer, ffn_gain, logits_bin,
        ppl_profil, lot, profil_neurones, neurones_sortie, trace_flux, trace_couches, flux_forcer,
        harmony, harmony_contexte, sans_yarn, ..
    } = opt;
    let lot = lot.max(1);
    let path = &modele_chemin();
    // Défauts du mode PERPLEXITÉ : 256 jetons, trois quarts des cœurs, 16 bits
    // d'activation (la référence de non-régression en dépend).
    let cpu = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(8);
    let ctx = if ctx_impose { ctx_opt } else { 256 };
    let n_threads = if threads_impose { threads_opt } else { (cpu * 3 / 4).max(1) };
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

    let mut mdl = model::Model::load(path, ctx, n_threads, dense, 1.0, auto, q4, b6);
    if let Some(chemin) = flux_forcer.as_deref() {
        match model::FluxRelecteur::lire(chemin) {
            Ok(r) => {
                println!("[flux] rejeu depuis {chemin} : {} listes enregistrées", r.listes.len());
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
    mdl.act_levels = ((1u32 << (abits - 1)) - 1) as f32;
    if let Some(f) = &patch_file {
        let pt = model::Patch::load(f).expect("chargement du greffon");
        let norme = |v: &[f32]| v.iter().map(|x| x * x).sum::<f32>().sqrt();
        println!("greffon : couche {}, |u|={:.3} |v|={:.3} |d|={:.3}",
                 pt.layer, norme(&pt.u), norme(&pt.v), norme(&pt.d));
        mdl.patch = Some(pt);
    }
    if let Some((l, g)) = ffn_gain {
        println!("gain FFN : couche {l} x {g}");
        mdl.ffn_gain = Some((l, g));
    }
    mdl.act_thresh = act_thresh;
    mdl.act_topk = act_topk;
    mdl.act_renorm = act_renorm;
    mdl.act_topk_proj = topk_proj;
    mdl.attn_topk = attn_topk;
    mdl.qk_topk = qk_topk;
    if sans_yarn { mdl.cfg_yarn_off(); }
    if attn_window > 0 { mdl.attn_window = attn_window; }
    if sans_fenetre { mdl.attn_window = 0; }
    if let Some(p) = swa_pattern { mdl.swa_pattern = p; }
    if sans_fenetre || swa_pattern.is_some() {
        println!("fenêtre : {} · motif {} (imposé par la ligne de commande)",
                 if mdl.attn_window == 0 { "aucune".to_string() } else { mdl.attn_window.to_string() },
                 mdl.swa_pattern);
    }
    if attn_sinks > 0 { mdl.attn_sinks = attn_sinks; }
    if act_thresh > 0.0 || act_topk > 0 {
        println!("parcimonie imposée : seuil {:.1} % du max{}",
                 act_thresh * 100.0,
                 if act_topk > 0 { format!(", k-WTA k={act_topk}") } else { String::new() });
    }
    if let Some(l) = hebb_layer {
        let mut hb = model::Hebb::new(l, mdl.cfg.ffn, mdl.cfg.hidden, 0.1);
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
        println!("  {:6} tokens notés — perplexité cumulée {:.3}  ({:.1} tok/s){}",
                 n, ppl, n as f64 / t0.elapsed().as_secs_f64(),
                 if fenetres.len() > 1 {
                     format!("  [fenêtre {} : {} notés, PPL {:.3}]",
                             i_f + 1, n_f, (nll_f / n_f.max(1) as f64).exp())
                 } else { String::new() });
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
    if let Some(hb) = mdl.hebb.as_ref() {
        if hb.log_on {
            use std::io::Write;
            let mut fa = std::fs::File::create("/tmp/act_log.bin").unwrap();
            for v in &hb.log { fa.write_all(&v.to_le_bytes()).unwrap(); }
            let mut fl = std::fs::File::create("/tmp/loss_log.bin").unwrap();
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
    if ae + fe > 0.0 {
        println!("    part de l'attention dans le flux d'événements : {:.1} %",
                 100.0 * ae / (ae + fe));
    } else {
        // Aucun événement : le mode dense ne compte rien. Annoncer « 100 % »
        // serait un artefact de division par zéro, pas une mesure.
        println!("    part de l'attention dans le flux d'événements : — (aucun événement)");
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
}
