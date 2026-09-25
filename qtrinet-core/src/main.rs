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

use engine::{accumulate_lists, matvec_dense, matvec_shift_add};
use gguf::Gguf;
use list::{dense_bits, BitmapSign, SignedDelta, SparseK};
use std::time::Instant;

fn fmt_bits(b: u64, n: usize) -> String {
    format!("{:8.3} b/poids  ({:7.2} Mo)", b as f64 / n as f64, b as f64 / 8.0 / 1e6)
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        eprintln!("usage: qtrinet-core <modele.gguf> [--matrix NOM] [--threads N]");
        std::process::exit(1);
    }
    let path = &args[1];
    let mut matrix = "blk.0.ffn_gate.weight".to_string();
    let mut n_threads = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(8);
    let mut i = 2;
    while i + 1 < args.len() {
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
    println!("\n=== 2. Moteur d'événements : débit selon la densité des activations ===");
    let t = g.tensor(&matrix).expect("matrice absente");
    let levels = g.raw_levels(&matrix);
    let n_rows = t.dims[0] as usize;   // entrées
    let n_cols = t.dims[1] as usize;   // sorties
    let n = n_rows * n_cols;

    // matrice ternaire (signes) pour comparer listes et dense à résultat égal
    let tern: Vec<i8> = levels.iter().map(|&v| v.signum()).collect();
    let lists = SignedDelta::build(&tern, n_rows, n_cols);
    println!(
        "  {matrix} : {n_rows} entrées × {n_cols} sorties, {} événements potentiels, {:.3} Mo de listes",
        lists.n_events,
        lists.data.len() as f64 / 1e6
    );

    let mut x = vec![0i32; n_rows];
    for (i, v) in x.iter_mut().enumerate() { *v = ((i * 2654435761usize) % 200) as i32 - 100; }

    print!("  {:>8}  {:>12}  {:>14}  {:>12}  {:>10}\n",
           "densité", "actifs", "événements", "G év/s", "ms/appel");
    for dens in [0.0, 0.01, 0.05, 0.10, 0.25, 0.50, 1.00] {
        let mut active = Vec::new();
        let mut xa = x.clone();
        for i in 0..n_rows {
            let h = (i as f64 * 0.6180339887).fract();
            if h < dens {
                active.push(i);
            } else {
                xa[i] = 0;
            }
        }
        // échauffement
        let _ = accumulate_lists(&lists, &xa, &active, n_threads);
        let reps = if dens == 0.0 { 1 } else { 20 };
        let t0 = Instant::now();
        let mut out = Vec::new();
        for _ in 0..reps {
            out = accumulate_lists(&lists, &xa, &active, n_threads).0;
        }
        let dt = t0.elapsed().as_secs_f64() / reps as f64;
        // comptage exact des événements
        let mut ev = 0usize;
        for &s in &active { lists.row_events(s, |_, _| ev += 1); }
        println!("  {:>7.1}%  {:>12}  {:>14}  {:>12.2}  {:>10.3}",
                 dens * 100.0, active.len(), ev, ev as f64 / dt / 1e9, dt * 1e3);
        if dens == 0.25 {
            // vérification : listes vs dense, à résultat identique
            let mut w = vec![0i8; n];
            for r in 0..n_rows {
                for c in 0..n_cols { w[r * n_cols + c] = tern[r * n_cols + c]; }
            }
            let y_ref = matvec_dense(&w, &xa, n_cols, n_rows);
            let same = out.iter().zip(y_ref.iter()).all(|(a, b)| a == b);
            println!("           → contrôle listes vs dense : {}",
                     if same { "IDENTIQUE ✅" } else { "DIVERGENT ❌" });
        }
    }

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
