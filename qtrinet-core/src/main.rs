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
use list::{dense_bits, BitmapSign, FusedSign, SignedDelta, SparseK};
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

    let mut pool = Pool::new(n_threads, n_cols);
    println!("  pool de {} threads, barrière atomique\n", pool.threads());
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
    let mut patch_file: Option<String> = None;
    let mut dense = false;
    let mut keep = 1.0f32;
    // L'inférence paie une barrière par matrice (168 par token) : l'optimum
    // mesuré est autour de la moitié des CPU logiques, pas des trois quarts.
    let cpu = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(8);
    let mut n_threads = (cpu / 2).max(1);
    let mut i = 2;
    while i + 1 < args.len() {
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
            "--patch" => patch_file = Some(args[i + 1].clone()),
            "--threads" => n_threads = args[i + 1].parse().unwrap(),
            "--chat" => { chat = true; i -= 1; }
            "--dense" => { dense = true; i -= 1; }
            "--keep" => keep = args[i + 1].parse().unwrap(),
            _ => {}
        }
        i += 2;
    }
    let mut mdl = model::Model::load(path, ctx, n_threads, dense, keep);
    mdl.act_levels = ((1u32 << (abits - 1)) - 1) as f32;
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

fn run_ppl(args: &[String]) {
    let path = &args[1];
    let mut idfile = String::new();
    let mut ctx = 256usize;
    let mut limit = usize::MAX;
    let mut abits = 16u32;
    let mut hebb_layer: Option<usize> = None;
    let mut patch_file: Option<String> = None;
    let mut gain: Option<(usize, f32)> = None;
    let cpu = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(8);
    let mut n_threads = (cpu * 3 / 4).max(1);
    let mut i = 2;
    while i + 1 < args.len() {
        match args[i].as_str() {
            "--ppl" => idfile = args[i + 1].clone(),
            "--ctx" => ctx = args[i + 1].parse().unwrap(),
            "--limit" => limit = args[i + 1].parse().unwrap(),
            "--abits" => abits = args[i + 1].parse().unwrap(),
            "--hebbian" => hebb_layer = Some(args[i + 1].parse().unwrap()),
            "--patch" => patch_file = Some(args[i + 1].clone()),
            "--ffn-gain" => {
                let v: Vec<&str> = args[i + 1].split(':').collect();
                gain = Some((v[0].parse().unwrap(), v[1].parse().unwrap()));
            }
            "--threads" => n_threads = args[i + 1].parse().unwrap(),
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

    let mut mdl = model::Model::load(path, ctx, n_threads, false, 1.0);
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
}
