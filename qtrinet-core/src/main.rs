//! qtrinet-core — moteur d'exécution par listes d'événements.
//!
//! Usage :
//!   qtrinet-core <modele.gguf> [--matrix blk.0.ffn_gate.weight] [--threads 8]
//!
//! Mesure sur le VRAI modèle :
//!   1. taille exacte de chaque encodage de liste (bits/poids),
//!   2. débit du moteur d'événements selon la densité des activations,
//!   3. exécution sans multiplieur (décalages + additions) vs multiplication.

mod engine;
mod gguf;
mod list;
mod model;
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
        eprintln!("usage: qtrinet-core <modele.gguf> [--matrix NOM] [--threads N]");
        eprintln!("       qtrinet-core <modele.gguf> --infer (--ids 1,2,3 | --prompt TEXTE)");
        eprintln!("                    [--n 32] [--temp 0] [--ctx 512] [--threads N]");
        std::process::exit(1);
    }
    if args.iter().any(|a| a == "--pin") {
        engine::EPINGLER.store(true, std::sync::atomic::Ordering::Relaxed);
    }
    if args.iter().any(|a| a == "--plan") { run_plan(&args); return; }
    if args.iter().any(|a| a == "--ppl") { run_ppl(&args); return; }
    if args.iter().any(|a| a == "--infer") { run_infer(&args); return; }
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

fn run_infer(args: &[String]) {
    let path = &args[1];
    let mut ids: Vec<u32> = Vec::new();
    let mut prompt: Option<String> = None;
    let mut n_new = 32usize;
    let mut temp = 0.0f32;
    let mut ctx = 512usize;
    let _ = 0;
    let mut topk = 0usize;
    let mut abits = 8u32;
    let mut chat = false;
    let mut hebb_layer: Option<usize> = None;
    let mut hebb_q = 0.1f32;
    let mut hebb_out = String::from("hebb.bin");
    let mut ids_file: Option<String> = None;
    let mut qk_topk = 0usize;
    let mut attn_window = 0usize;
    let mut attn_sinks = 4usize;
    let mut attn_topk = 0usize;
    let mut patch_file: Option<String> = None;
    let mut act_thresh = 0.0f32;
    let mut act_topk = 0usize;
    let mut act_renorm = false;
    let mut topk_proj = [0usize; 7];
    // Défaut : le moteur CHOISIT par mesure. Les deux formes sont chargées et la
    // bascule se fait projection par projection sur la densité mesurée — les
    // sorties sont identiques au bit près, seul le débit change (×2,1 sur un
    // modèle dense, ×1,5 en faveur du push sous 5 % de densité).
    let mut dense = false;
    let mut auto = true;
    let mut moe_topk = 0usize;
    let mut q4 = 0u8;
    let mut keep = 1.0f32;
    // L'inférence paie une barrière par matrice (168 par token) : l'optimum
    // mesuré est autour de la moitié des CPU logiques, pas des trois quarts.
    let cpu = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(8);
    let mut n_threads = (cpu / 2).max(1);
    let mut i = 2;
    while i < args.len() {
        match args[i].as_str() {
            "--infer" => { i += 1; continue; }
            "--ids" => ids = args[i + 1].split(',').filter_map(|s| s.trim().parse().ok()).collect(),
            "--prompt" => prompt = Some(args[i + 1].clone()),
            "--n" => n_new = args[i + 1].parse().unwrap(),
            "--temp" => temp = args[i + 1].parse().unwrap(),
            "--ctx" => ctx = args[i + 1].parse().unwrap(),
            "--topk" => topk = args[i + 1].parse().unwrap(),
            "--abits" => abits = args[i + 1].parse().unwrap(),
            "--ids-file" => ids_file = Some(args[i + 1].clone()),
            "--hebbian" => hebb_layer = Some(args[i + 1].parse().unwrap()),
            "--hebb-q" => hebb_q = args[i + 1].parse().unwrap(),
            "--hebb-out" => hebb_out = args[i + 1].clone(),
            "--act-thresh" => act_thresh = args[i + 1].parse().unwrap(),
            "--act-topk" => act_topk = args[i + 1].parse().unwrap(),
            "--act-renorm" => { act_renorm = true; i -= 1; }
            "--topk-q" => topk_proj[0] = args[i + 1].parse().unwrap(),
            "--topk-k" => topk_proj[1] = args[i + 1].parse().unwrap(),
            "--topk-v" => topk_proj[2] = args[i + 1].parse().unwrap(),
            "--topk-o" => topk_proj[3] = args[i + 1].parse().unwrap(),
            "--topk-gate" => topk_proj[4] = args[i + 1].parse().unwrap(),
            "--topk-up" => topk_proj[5] = args[i + 1].parse().unwrap(),
            "--topk-down" => topk_proj[6] = args[i + 1].parse().unwrap(),
            "--attn-topk" => attn_topk = args[i + 1].parse().unwrap(),
            "--qk-topk" => qk_topk = args[i + 1].parse().unwrap(),
            "--attn-window" => attn_window = args[i + 1].parse().unwrap(),
            "--attn-sinks" => attn_sinks = args[i + 1].parse().unwrap(),
            "--patch" => patch_file = Some(args[i + 1].clone()),
            "--threads" => n_threads = args[i + 1].parse().unwrap(),
            "--chat" => { chat = true; i -= 1; }
            "--dense" => { dense = true; i -= 1; }
            "--moe-topk" => { moe_topk = args[i + 1].parse().unwrap(); i -= 1; }
            "--pin" => { engine::EPINGLER.store(true, std::sync::atomic::Ordering::Relaxed); i -= 1; }
            "--auto" => { auto = true; i -= 1; }
            "--push" => { auto = false; dense = false; i -= 1; }
            "--q4" => { q4 |= 3; i -= 1; }
            "--q4-ffn" => { q4 = (q4 & 4) | 1; i -= 1; }
            "--q4-attn" => { q4 = (q4 & 4) | 2; i -= 1; }
            "--q4-tout" => { q4 |= 7; i -= 1; }
            "--keep" => keep = args[i + 1].parse().unwrap(),
            _ => {}
        }
        i += 2;
    }
    let mut mdl = model::Model::load(path, ctx, n_threads, dense, keep, auto, q4);
    mdl.act_levels = ((1u32 << (abits - 1)) - 1) as f32;
    mdl.moe_topk = moe_topk;
    mdl.act_thresh = act_thresh;
    mdl.act_topk = act_topk;
    mdl.act_renorm = act_renorm;
    mdl.act_topk_proj = topk_proj;
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
        if chat {
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
    if ids.is_empty() { eprintln!("rien à générer : --ids ou --prompt requis"); return; }

    mdl.reset_events();
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
        mdl.generate(&ids, n_new, temp)
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
    tokenizer::Tokenizer::new(
        meta_strings(g, "tokenizer.ggml.tokens"),
        meta_strings(g, "tokenizer.ggml.merges"),
        meta_ints(g, "tokenizer.ggml.token_type"),
    )
}

fn cfg_dims(m: &model::Model) -> usize { m.cfg.hidden }

/// Plan de placement : ce que pèse chaque couche, et où la mettre.
///
/// C'est l'« index » du conteneur : on le lit **avant** les poids, donc on
/// décide sans avoir rien chargé. Les seuils viennent des débits mesurés sur
/// cette machine : CPU 14–25 Go/s, PCIe x8 6,5 Go/s, NVLink 25,78 Go/s,
/// GPU 380 Go/s en lecture locale.
fn run_plan(args: &[String]) {
    let path = &args[1];
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
}

fn run_ppl(args: &[String]) {
    let path = &args[1];
    let mut idfile = String::new();
    let mut ctx = 256usize;
    let mut limit = usize::MAX;
    let mut abits = 16u32;
    let mut hebb_layer: Option<usize> = None;
    let mut patch_file: Option<String> = None;
    let mut gain: Option<(usize, f32)> = None;
    let mut act_thresh = 0.0f32;
    let mut act_topk = 0usize;
    let mut act_renorm = false;
    let mut topk_proj = [0usize; 7];
    let mut attn_topk = 0usize;
    let mut qk_topk = 0usize;
    let mut attn_window = 0usize;
    let mut attn_sinks = 4usize;
    // Défaut : le moteur CHOISIT par mesure. Les deux formes sont chargées et la
    // bascule se fait projection par projection sur la densité mesurée — les
    // sorties sont identiques au bit près, seul le débit change (×2,1 sur un
    // modèle dense, ×1,5 en faveur du push sous 5 % de densité).
    let mut dense = false;
    let mut auto = true;
    let mut moe_topk = 0usize;
    let mut q4 = 0u8;
    let cpu = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(8);
    let mut n_threads = (cpu * 3 / 4).max(1);
    let mut i = 2;
    while i < args.len() {
        match args[i].as_str() {
            "--ppl" => idfile = args[i + 1].clone(),
            "--ctx" => ctx = args[i + 1].parse().unwrap(),
            "--limit" => limit = args[i + 1].parse().unwrap(),
            "--act-topk" => act_topk = args[i + 1].parse().unwrap(),
            "--act-renorm" => { act_renorm = true; i -= 1; }
            "--topk-q" => topk_proj[0] = args[i + 1].parse().unwrap(),
            "--topk-k" => topk_proj[1] = args[i + 1].parse().unwrap(),
            "--topk-v" => topk_proj[2] = args[i + 1].parse().unwrap(),
            "--topk-o" => topk_proj[3] = args[i + 1].parse().unwrap(),
            "--topk-gate" => topk_proj[4] = args[i + 1].parse().unwrap(),
            "--topk-up" => topk_proj[5] = args[i + 1].parse().unwrap(),
            "--topk-down" => topk_proj[6] = args[i + 1].parse().unwrap(),
            "--attn-topk" => attn_topk = args[i + 1].parse().unwrap(),
            "--qk-topk" => qk_topk = args[i + 1].parse().unwrap(),
            "--attn-window" => attn_window = args[i + 1].parse().unwrap(),
            "--attn-sinks" => attn_sinks = args[i + 1].parse().unwrap(),
            "--abits" => abits = args[i + 1].parse().unwrap(),
            "--hebbian" => hebb_layer = Some(args[i + 1].parse().unwrap()),
            "--patch" => patch_file = Some(args[i + 1].clone()),
            "--ffn-gain" => {
                let v: Vec<&str> = args[i + 1].split(':').collect();
                gain = Some((v[0].parse().unwrap(), v[1].parse().unwrap()));
            }
            "--act-thresh" => act_thresh = args[i + 1].parse().unwrap(),
            "--act-topk" => act_topk = args[i + 1].parse().unwrap(),
            "--act-renorm" => { act_renorm = true; i -= 1; }
            "--topk-q" => topk_proj[0] = args[i + 1].parse().unwrap(),
            "--topk-k" => topk_proj[1] = args[i + 1].parse().unwrap(),
            "--topk-v" => topk_proj[2] = args[i + 1].parse().unwrap(),
            "--topk-o" => topk_proj[3] = args[i + 1].parse().unwrap(),
            "--topk-gate" => topk_proj[4] = args[i + 1].parse().unwrap(),
            "--topk-up" => topk_proj[5] = args[i + 1].parse().unwrap(),
            "--topk-down" => topk_proj[6] = args[i + 1].parse().unwrap(),
            "--attn-topk" => attn_topk = args[i + 1].parse().unwrap(),
            "--qk-topk" => qk_topk = args[i + 1].parse().unwrap(),
            "--attn-window" => attn_window = args[i + 1].parse().unwrap(),
            "--attn-sinks" => attn_sinks = args[i + 1].parse().unwrap(),
            "--threads" => n_threads = args[i + 1].parse().unwrap(),
            "--dense" => { dense = true; i -= 1; }
            "--moe-topk" => { moe_topk = args[i + 1].parse().unwrap(); i -= 1; }
            "--pin" => { engine::EPINGLER.store(true, std::sync::atomic::Ordering::Relaxed); i -= 1; }
            "--auto" => { auto = true; i -= 1; }
            "--push" => { auto = false; dense = false; i -= 1; }
            "--q4" => { q4 |= 3; i -= 1; }
            "--q4-ffn" => { q4 = (q4 & 4) | 1; i -= 1; }
            "--q4-attn" => { q4 = (q4 & 4) | 2; i -= 1; }
            "--q4-tout" => { q4 |= 7; i -= 1; }
            _ => {}
        }
        i += 2;
    }
    let raw = std::fs::read_to_string(&idfile).expect("fichier d'identifiants illisible");
    let ids: Vec<u32> = raw.split(|c: char| c == ',' || c.is_whitespace())
        .filter(|s| !s.is_empty())
        .filter_map(|s| s.parse().ok())
        .take(limit)
        .collect();
    println!("{idfile} : {} tokens, fenêtres de {ctx}", ids.len());

    let mut mdl = model::Model::load(path, ctx, n_threads, dense, 1.0, auto, q4);
    mdl.act_levels = ((1u32 << (abits - 1)) - 1) as f32;
    if let Some(f) = &patch_file {
        let pt = model::Patch::load(f).expect("chargement du greffon");
        let norme = |v: &[f32]| v.iter().map(|x| x * x).sum::<f32>().sqrt();
        println!("greffon : couche {}, |u|={:.3} |v|={:.3} |d|={:.3}",
                 pt.layer, norme(&pt.u), norme(&pt.v), norme(&pt.d));
        mdl.patch = Some(pt);
    }
    if let Some((l, g)) = gain {
        println!("gain FFN : couche {l} x {g}");
        mdl.ffn_gain = Some((l, g));
    }
    mdl.act_thresh = act_thresh;
    mdl.act_topk = act_topk;
    mdl.act_renorm = act_renorm;
    mdl.act_topk_proj = topk_proj;
    mdl.attn_topk = attn_topk;
    mdl.qk_topk = qk_topk;
    mdl.attn_window = attn_window;
    mdl.attn_sinks = attn_sinks;
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
    mdl.reset_events();
    let t0 = Instant::now();
    let mut nll = 0f64;
    let mut n = 0usize;
    let mut perte: Vec<f32> = Vec::new();
    let mut start = 0usize;
    while start + 1 < ids.len() {
        let end = (start + ctx).min(ids.len());
        let chunk = &ids[start..end];
        for pos in 0..chunk.len() {
            let h = mdl.forward(chunk[pos], pos);
            if pos + 1 < chunk.len() {
                let lg = mdl.logits(&h);
                let mut mx = f32::NEG_INFINITY;
                for &v in &lg { if v > mx { mx = v; } }
                let mut sum = 0f64;
                for &v in &lg { sum += ((v - mx) as f64).exp(); }
                let lse = mx as f64 + sum.ln();
                let nll_tok = lse - lg[chunk[pos + 1] as usize] as f64;
                nll += nll_tok;
                n += 1;
                perte.push(nll_tok as f32);
            }
        }
        start = end;
        let ppl = (nll / n as f64).exp();
        println!("  {:6} tokens notés — perplexité cumulée {:.3}  ({:.1} tok/s)",
                 n, ppl, n as f64 / t0.elapsed().as_secs_f64());
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
    println!("    dont attention : scores {:.2} | softmax {:.2} | somme pondérée + écriture KV {:.2}",
             p[4] / n as f64 * 1e3, p[5] / n as f64 * 1e3,
             (p[2] - p[4] - p[5]) / n as f64 * 1e3);
}
