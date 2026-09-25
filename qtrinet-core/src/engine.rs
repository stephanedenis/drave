//! Moteur d'exécution par événements — version optimisée.
//!
//! Deux gains par rapport à la première version :
//!
//! 1. **Pool de threads persistant** : threads créés une fois, accumulateurs
//!    conservés d'un appel à l'autre. La version précédente payait 0,48 ms par
//!    appel en création de threads et en réduction — ce qui écrasait tout le
//!    régime creux, précisément celui qui nous intéresse.
//! 2. **Décodeurs rapides** : chemin direct pour les varints d'un octet (cas
//!    dominant), et décodage de bitmap par mots de 64 bits (`trailing_zeros`)
//!    qui traite 64 poids par itération.

use crate::list::{BitmapSign, SignedDelta};
use std::sync::mpsc::{channel, Receiver, Sender};

// --------------------------------------------------------------------------- //
// Décodeurs
// --------------------------------------------------------------------------- //

/// Accumule les événements d'une ligne en listes signées (varints).
#[inline]
pub fn row_delta_into(lists: &SignedDelta, r: usize, xv: i64, acc: &mut [i64]) -> usize {
    let data = &lists.data;
    let mut p = lists.row_start[r];
    let n_out = lists.n_cols;

    #[inline(always)]
    fn vi(data: &[u8], p: &mut usize) -> usize {
        let b0 = data[*p];
        if b0 < 0x80 {                       // chemin rapide : 1 octet
            *p += 1;
            b0 as usize
        } else {
            let mut v = (b0 & 0x7F) as usize;
            let mut sh = 7;
            *p += 1;                          // consommer le premier octet !
            loop {
                let b = data[*p];
                *p += 1;
                v |= ((b & 0x7F) as usize) << sh;
                if b < 0x80 { break; }
                sh += 7;
            }
            v
        }
    }

    let np = vi(data, &mut p);
    let nn = vi(data, &mut p);
    let mut c = 0usize;
    for _ in 0..np {
        c += vi(data, &mut p);
        if c < n_out { acc[c] += xv; }
    }
    let mut c = 0usize;
    for _ in 0..nn {
        c += vi(data, &mut p);
        if c < n_out { acc[c] -= xv; }
    }
    np + nn
}

/// Accumule une ligne en bitmap + signes, mot de 64 bits par itération.
#[inline]
pub fn row_bitmap_into(bm: &BitmapSign, r: usize, xv: i64, acc: &mut [i64]) -> usize {
    let n_cols = bm.n_cols;
    let base = r * n_cols;
    let mut events = 0usize;
    let mut wi = base / 64;
    let last = (base + n_cols - 1) / 64;
    let mut sb = bm.sign_pos[r];
    while wi <= last {
        let mut w = bm.mask[wi];
        while w != 0 {
            let col = wi * 64 + w.trailing_zeros() as usize;
            if col < base + n_cols {
                let positive = (bm.signs[(sb / 64) as usize] >> (sb % 64)) & 1 == 1;
                acc[col - base] += if positive { xv } else { -xv };
                events += 1;
            }
            sb += 1;
            w &= w - 1;                       // efface le bit le plus faible
        }
        wi += 1;
    }
    events
}

// --------------------------------------------------------------------------- //
// Pool persistant
// --------------------------------------------------------------------------- //

/// Enveloppe Send pour un pointeur brut. Sûreté assurée par le protocole du
/// pool : le demandeur bloque jusqu'au dernier compte rendu, donc les données
/// pointées restent vivantes pendant tout le traitement.
struct SendPtr<T>(*const T);
impl<T> Clone for SendPtr<T> { fn clone(&self) -> Self { *self } }
impl<T> Copy for SendPtr<T> {}
unsafe impl<T> Send for SendPtr<T> {}

struct Job {
    lists: SendPtr<SignedDelta>,
    x: SendPtr<i32>,
    active: SendPtr<usize>,
    n_active: usize,
    n_in: usize,
    offset: usize,
    stride: usize,
    acc: Vec<i64>,
    use_bitmap: Option<SendPtr<BitmapSign>>,
}

enum Msg { Job(Job), Stop }

pub struct Pool {
    senders: Vec<Sender<Msg>>,
    done: Receiver<(usize, Vec<i64>, usize)>,
    handles: Vec<std::thread::JoinHandle<()>>,
    n: usize,
    n_out: usize,
    /// accumulateurs détenus par le demandeur entre deux appels (un par worker)
    accs: Vec<Vec<i64>>,
}

impl Pool {
    pub fn new(n: usize, n_out: usize) -> Self {
        let mut senders = Vec::with_capacity(n);
        let mut handles = Vec::with_capacity(n);
        let (dtx, drx) = channel();
        for id in 0..n {
            let (tx, rx): (Sender<Msg>, Receiver<Msg>) = channel();
            let dtx = dtx.clone();
            handles.push(std::thread::spawn(move || {
                while let Ok(msg) = rx.recv() {
                    match msg {
                        Msg::Stop => break,
                        Msg::Job(mut job) => {
                            let lists = unsafe { &*job.lists.0 };
                            let x = unsafe { std::slice::from_raw_parts(job.x.0, job.n_in) };
                            let active = unsafe { std::slice::from_raw_parts(job.active.0, job.n_active) };
                            for a in job.acc.iter_mut() { *a = 0; }
                            let mut ev = 0usize;
                            let mut i = job.offset;
                            while i < job.n_active {
                                let src = active[i];
                                let xv = x[src] as i64;
                                if xv != 0 {
                                    ev += match job.use_bitmap {
                                        Some(p) => row_bitmap_into(unsafe { &*p.0 }, src, xv, &mut job.acc),
                                        None => row_delta_into(lists, src, xv, &mut job.acc),
                                    };
                                }
                                i += job.stride;
                            }
                            let _ = dtx.send((id, job.acc, ev));
                        }
                    }
                }
            }));
            senders.push(tx);
        }
        Pool { senders, done: drx, handles, n, n_out, accs: vec![vec![0i64; n_out]; n] }
    }

    pub fn threads(&self) -> usize { self.n }

    pub fn shutdown(self) { drop(self) }

    fn run(&mut self, lists: &SignedDelta, bm: Option<&BitmapSign>, x: &[i32], active: &[usize]) -> (Vec<i64>, usize) {
        let lp = SendPtr(lists as *const _);
        let xp = SendPtr(x.as_ptr());
        let ap = SendPtr(active.as_ptr());
        let bp = bm.map(|b| SendPtr(b as *const _));
        for t in 0..self.n {
            let job = Job {
                lists: lp, x: xp, active: ap, n_active: active.len(), n_in: x.len(),
                offset: t, stride: self.n,
                acc: std::mem::take(&mut self.accs[t]),
                use_bitmap: bp,
            };
            self.senders[t].send(Msg::Job(job)).expect("worker disparu");
        }
        let mut events = 0usize;
        for _ in 0..self.n {
            let (id, acc, ev) = self.done.recv().expect("worker disparu");
            self.accs[id] = acc;
            events += ev;
        }
        let mut out = vec![0i64; self.n_out];
        for a in &self.accs {
            for (o, v) in out.iter_mut().zip(a.iter()) { *o += *v; }
        }
        (out, events)
    }

    pub fn accumulate_lists(&mut self, lists: &SignedDelta, x: &[i32], active: &[usize]) -> (Vec<i64>, usize) {
        self.run(lists, None, x, active)
    }

    pub fn accumulate_bitmap(&mut self, bm: &BitmapSign, x: &[i32], active: &[usize]) -> (Vec<i64>, usize) {
        // une matrice vide sert de support au champ `lists` du job
        let dummy = SignedDelta { n_rows: 1, n_cols: bm.n_cols, data: vec![0, 0], n_events: 0, row_start: vec![0, 2] };
        self.run(&dummy, Some(bm), x, active)
    }
}

impl Drop for Pool {
    fn drop(&mut self) {
        for s in self.senders.iter() { let _ = s.send(Msg::Stop); }
        for h in self.handles.drain(..) { let _ = h.join(); }
    }
}

// --------------------------------------------------------------------------- //
// Références (non optimisées) pour comparaison
// --------------------------------------------------------------------------- //

/// Produit matrice-vecteur dense en i8×i8 → i64 (référence vectorisable).
pub fn matvec_dense(w: &[i8], x: &[i32], n_out: usize, n_in: usize) -> Vec<i64> {
    let mut y = vec![0i64; n_out];
    for i in 0..n_in {
        let xv = x[i] as i64;
        if xv == 0 { continue; }
        let row = &w[i * n_out..(i + 1) * n_out];
        for j in 0..n_out { y[j] += row[j] as i64 * xv; }
    }
    y
}

/// Produit matrice-vecteur **sans multiplieur** : décalages et additions.
pub fn matvec_shift_add(w: &[i8], x: &[i32], n_out: usize, n_in: usize) -> (Vec<i64>, u64) {
    let mut y = vec![0i64; n_out];
    let mut ops: u64 = 0;
    for i in 0..n_in {
        let xv = x[i] as i64;
        if xv == 0 { continue; }
        let row = &w[i * n_out..(i + 1) * n_out];
        for j in 0..n_out {
            let v = row[j];
            if v == 0 { continue; }
            let neg = v < 0;
            let mut m = (v as i16).unsigned_abs() as u32;
            let mut b = 0u32;
            while m != 0 {
                if m & 1 == 1 {
                    let c = xv << b;
                    y[j] += if neg { -c } else { c };
                    ops += 1;
                }
                m >>= 1;
                b += 1;
            }
        }
    }
    (y, ops)
}

/// Ancienne version (threads créés à chaque appel) — pour mesurer le gain.
pub fn accumulate_scoped(lists: &SignedDelta, x: &[i32], active: &[usize], n_threads: usize) -> (Vec<i64>, usize) {
    let n_out = lists.n_cols;
    let mut parts: Vec<Vec<i64>> = Vec::with_capacity(n_threads);
    let events = std::sync::atomic::AtomicUsize::new(0);
    std::thread::scope(|s| {
        let mut hs = Vec::with_capacity(n_threads);
        for t in 0..n_threads {
            let chunk: Vec<usize> = active.iter().copied().skip(t).step_by(n_threads).collect();
            let ev = &events;
            hs.push(s.spawn(move || {
                let mut acc = vec![0i64; n_out];
                let mut n = 0usize;
                for &src in &chunk {
                    let xv = x[src] as i64;
                    if xv != 0 { n += row_delta_into(lists, src, xv, &mut acc); }
                }
                ev.fetch_add(n, std::sync::atomic::Ordering::Relaxed);
                acc
            }));
        }
        for h in hs { parts.push(h.join().unwrap()); }
    });
    let mut acc = vec![0i64; n_out];
    for p in &parts { for (a, b) in acc.iter_mut().zip(p.iter()) { *a += *b; } }
    (acc, events.load(std::sync::atomic::Ordering::Relaxed))
}
