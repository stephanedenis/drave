//! Moteur d'exécution par événements.
//!
//! Deux modes mesurés côte à côte :
//!
//! * **liste** — pour chaque source active (activation non nulle), on pousse sa
//!   valeur vers les destinations de sa liste. Les poids se lisent en flux
//!   séquentiel ; le nombre d'événements dépend des activations, donc le débit
//!   est *variable*.
//! * **dense** — produit matrice-vecteur classique en entiers, pour comparaison.
//!
//! Le moteur « liste » utilise un accumulateur par thread puis une réduction, ce
//! qui évite toute contention (mesuré : la dispersion sature vers 8 threads).

use crate::list::SignedDelta;
use std::sync::atomic::{AtomicUsize, Ordering};

pub struct BenchResult {
    pub events: usize,
    pub seconds: f64,
}

impl BenchResult {
    pub fn events_per_s(&self) -> f64 { self.events as f64 / self.seconds }
}

/// Accumulation par listes signées, multi-thread.
///
/// `x` : activations (i32). `active` : sources non nulles (indices triés).
/// Chaque événement fait `acc[dest] += signe * x[src]`.
pub fn accumulate_lists(
    lists: &SignedDelta,
    x: &[i32],
    active: &[usize],
    n_threads: usize,
) -> (Vec<i64>, usize) {
    let n_out = lists.n_cols;
    let n_threads = n_threads.max(1);
    let mut partials: Vec<Vec<i64>> = Vec::with_capacity(n_threads);
    let events = AtomicUsize::new(0);

    std::thread::scope(|s| {
        let mut handles = Vec::with_capacity(n_threads);
        for t in 0..n_threads {
            let chunk: Vec<usize> = active
                .iter()
                .copied()
                .skip(t)
                .step_by(n_threads)
                .collect();
            let ev = &events;
            handles.push(s.spawn(move || {
                let mut acc = vec![0i64; n_out];
                let mut n = 0usize;
                for &src in &chunk {
                    let xv = x[src] as i64;
                    if xv == 0 { continue; }
                    lists.row_events(src, |dst, sign| {
                        // sécurité : un varint corrompu ne doit pas sortir du tableau
                        if dst < n_out {
                            acc[dst] += if sign > 0 { xv } else { -xv };
                        }
                    });
                    n += lists.n_events;   // borne supérieure (pas le compte exact)
                }
                ev.fetch_add(n, Ordering::Relaxed);
                acc
            }));
        }
        for h in handles {
            partials.push(h.join().unwrap());
        }
    });

    // réduction
    let mut acc = vec![0i64; n_out];
    for p in &partials {
        for (a, b) in acc.iter_mut().zip(p.iter()) { *a += *b; }
    }
    (acc, events.load(Ordering::Relaxed))
}

/// Produit matrice-vecteur dense en i8×i8 → i32 (référence).
pub fn matvec_dense(w: &[i8], x: &[i32], n_out: usize, n_in: usize) -> Vec<i64> {
    let mut y = vec![0i64; n_out];
    // w est row-major (n_in, n_out) : y[j] = somme_i w[i][j] * x[i]
    for i in 0..n_in {
        let xv = x[i] as i64;
        if xv == 0 { continue; }
        let row = &w[i * n_out..(i + 1) * n_out];
        for j in 0..n_out {
            y[j] += row[j] as i64 * xv;
        }
    }
    y
}

/// Produit matrice-vecteur **sans multiplieur** : décalages et additions.
///
/// w·x = Σ_b (bit b de |w|) ? (x << b) : 0, avec le signe appliqué.
/// Coût : popcount(|w|) additions par poids — aucun DSP, aucune multiplication.
pub fn matvec_shift_add(w: &[i8], x: &[i32], n_out: usize, n_in: usize) -> (Vec<i64>, u64) {
    let mut y = vec![0i64; n_out];
    let mut ops: u64 = 0;
    for i in 0..n_in {
        let xv = x[i] as i64;
        let row = &w[i * n_out..(i + 1) * n_out];
        if xv == 0 { continue; }
        for j in 0..n_out {
            let v = row[j];
            if v == 0 { continue; }
            let neg = v < 0;
            let mut m = (v as i16).unsigned_abs() as u32;
            let mut b = 0u32;
            while m != 0 {
                if m & 1 == 1 {
                    let contrib = xv << b;
                    y[j] += if neg { -contrib } else { contrib };
                    ops += 1;
                }
                m >>= 1;
                b += 1;
            }
        }
    }
    (y, ops)
}
