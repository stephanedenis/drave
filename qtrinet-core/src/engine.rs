//! Moteur d'exécution par événements — version optimisée (4 optimisations).
//!
//! 1. **Réduction incrémentale** : chaque worker ne remet à zéro que les
//!    destinations qu'il a touchées, et le demandeur ne réduit que la fenêtre
//!    utile. Fini le memset de 114 Ko (16 × 896 × 8 o) par appel.
//! 2. **Traitement par blocs + décodage SWAR** : les écarts d'un octet sont
//!    décodés 8 à la fois dans un mot de 64 bits (`word & 0x8080…` = test
//!    vectoriel), et l'accumulation se fait sans contrôle de borne.
//! 3. **Vecteur d'activation creux explicite** (`SparseVec`) : indices et valeurs
//!    contigus, plus aucun test de zéro ni accès indirect au tableau dense.
//! 4. **Listes fusionnées** (`FusedSign`) : une seule liste triée par destination
//!    au lieu de deux (+, −) — l'accès à l'accumulateur devient **monotone**.
//!
//! Barrière par *spin* (atomiques) au lieu de canaux : le coût fixe d'un appel
//! passe de quelques dizaines de microsecondes à quelques microsecondes.

use crate::list::{DenseQ8, FusedSign, PushMat, SignedDelta};
use std::sync::atomic::{AtomicBool, AtomicPtr, AtomicUsize, Ordering};
use std::sync::Arc;

// --------------------------------------------------------------------------- //
// Vecteur creux d'activation (optimisation 3)
// --------------------------------------------------------------------------- //

/// Liste d'activations non nulles, construite en amont par la cascade.
/// Indices triés, valeurs contiguës : 8 octets par source active, aucune
/// indirection, aucun test de zéro dans la boucle chaude.
#[derive(Clone, Debug, Default)]
pub struct SparseVec {
    pub idx: Vec<u32>,
    pub val: Vec<i32>,
}

impl SparseVec {
    pub fn from_dense(x: &[i32]) -> Self {
        let mut idx = Vec::new();
        let mut val = Vec::new();
        for (i, &v) in x.iter().enumerate() {
            if v != 0 { idx.push(i as u32); val.push(v); }
        }
        SparseVec { idx, val }
    }
    pub fn len(&self) -> usize { self.idx.len() }
    pub fn is_empty(&self) -> bool { self.idx.is_empty() }
}

// --------------------------------------------------------------------------- //
// Décodage SWAR
// --------------------------------------------------------------------------- //

const HIGH_BITS: u64 = 0x8080_8080_8080_8080;

/// Décode jusqu'à 8 écarts d'un octet d'un coup. Retourne (valeurs, nb consommés).
///
/// Si les 8 octets ont leur bit de poids fort à zéro (test unique sur un u64),
/// les 8 valeurs sont extraites par décalages — pas de branche par élément.
#[inline(always)]
fn decode8(data: &[u8], p: usize, out: &mut [u32; 8]) -> usize {
    if p + 8 > data.len() { return 0; }
    let w = u64::from_le_bytes(unsafe { *(data.as_ptr().add(p) as *const [u8; 8]) });
    if w & HIGH_BITS != 0 { return 0; }         // au moins un varint multi-octet
    for k in 0..8 {
        out[k] = ((w >> (8 * k)) & 0xFF) as u32;
    }
    8
}

/// Accumule une ligne en liste fusionnée (écarts triés + bits de signe).
/// Optimisations 1, 2 et 4 : parcours monotone, décodage par paquets de 8,
/// aucune remise à zéro globale.
#[inline]
pub fn row_fused_into(f: &FusedSign, r: usize, xv: i64, acc: &mut [i64],
                      touched: &mut Vec<u32>, cap: usize,
                      span: &mut (usize, usize)) -> usize {
    let data = &f.data;
    let n_out = f.n_cols;
    let mut p = f.row_start[r];
    // nombre d'événements de la ligne (toujours un varint, souvent 1 octet)
    let n_ev = {
        let b0 = data[p];
        if b0 < 0x80 { p += 1; b0 as usize } else {
            p += 1;
            let mut v = (b0 & 0x7F) as usize;
            let mut sh = 7;
            loop {
                let b = data[p]; p += 1;
                v |= ((b & 0x7F) as usize) << sh;
                if b < 0x80 { break; }
                sh += 7;
            }
            v
        }
    };
    let mut sb = f.sign_pos[r] as usize;
    let mut col = 0usize;
    let mut done = 0usize;
    let mut buf = [0u32; 8];
    // Étendue de la ligne, tenue en registres : écrite dans `span` une seule
    // fois, à la sortie. Passer par le pointeur à chaque événement créait une
    // barrière d'aliasing avec `acc` et coûtait ×3 sur le débit.
    let mut first = usize::MAX;
    let mut last = 0usize;
    while done < n_ev {
        let got = if n_ev - done >= 8 { decode8(data, p, &mut buf) } else { 0 };
        if got == 8 {
            p += 8;
            for k in 0..8 {
                col += buf[k] as usize;
                if col < n_out {
                    let positive = (f.signs[sb >> 6] >> (sb & 63)) & 1 == 1;
                    unsafe {
                        let slot = acc.get_unchecked_mut(col);
                        *slot += if positive { xv } else { -xv };
                    }
                    if touched.len() < cap { touched.push(col as u32); }
                    if first == usize::MAX { first = col; }
                    last = col;
                }
                sb += 1;
            }
            done += 8;
        } else {
            // chemin général (varint multi-octets)
            let b0 = data[p];
            let d = if b0 < 0x80 { p += 1; b0 as usize } else {
                p += 1;
                let mut v = (b0 & 0x7F) as usize;
                let mut sh = 7;
                loop {
                    let b = data[p]; p += 1;
                    v |= ((b & 0x7F) as usize) << sh;
                    if b < 0x80 { break; }
                    sh += 7;
                }
                v
            };
            col += d;
            if col < n_out {
                let positive = (f.signs[sb >> 6] >> (sb & 63)) & 1 == 1;
                unsafe {
                    let slot = acc.get_unchecked_mut(col);
                    *slot += if positive { xv } else { -xv };
                }
                if touched.len() < cap { touched.push(col as u32); }
                if first == usize::MAX { first = col; }
                last = col;
            }
            sb += 1;
            done += 1;
        }
    }
    if first != usize::MAX {
        if first < span.0 { span.0 = first; }
        if last + 1 > span.1 { span.1 = last + 1; }
    }
    n_ev
}

/// Accumule une ligne en **listes par source avec valeur** (mode push).
/// Chaque événement est `varint(écart de sortie) + i8(valeur)` ; la contribution
/// vaut `q_activation × q_poids`. C'est le chemin qu'empruntera le matériel :
/// une adresse, une valeur, un accumulateur.
#[inline]
pub fn row_val_into(m: &PushMat, r: usize, xq: i64, acc: &mut [i64],
                    touched: &mut Vec<u32>, cap: usize,
                    span: &mut (usize, usize)) -> usize {
    let data = &m.data;
    let n_out = m.n_out;
    let mut p = m.row_start[r] as usize;
    let end = m.row_start[r + 1] as usize;
    let mut col = 0usize;
    let mut n_ev = 0usize;
    let mut first = usize::MAX;
    let mut last = 0usize;
    while p < end {
        // chemin rapide : écart d'un octet (le cas de très loin le plus fréquent)
        let b0 = data[p];
        if b0 < 0x80 {
            col += b0 as usize;
            let q = data[p + 1] as i8 as i64;
            p += 2;
            if col < n_out {
                unsafe { *acc.get_unchecked_mut(col) += xq * q; }
                if touched.len() < cap { touched.push(col as u32); }
                if first == usize::MAX { first = col; }
                last = col;
            }
        } else {
            p += 1;
            let mut d = (b0 & 0x7F) as usize;
            let mut sh = 7;
            loop {
                let b = data[p]; p += 1;
                d |= ((b & 0x7F) as usize) << sh;
                if b < 0x80 { break; }
                sh += 7;
            }
            col += d;
            let q = data[p] as i8 as i64;
            p += 1;
            if col < n_out {
                unsafe { *acc.get_unchecked_mut(col) += xq * q; }
                if touched.len() < cap { touched.push(col as u32); }
                if first == usize::MAX { first = col; }
                last = col;
            }
        }
        n_ev += 1;
    }
    if first != usize::MAX {
        if first < span.0 { span.0 = first; }
        if last + 1 > span.1 { span.1 = last + 1; }
    }
    n_ev
}

// --------------------------------------------------------------------------- //
// Pool à barrière atomique
// --------------------------------------------------------------------------- //

struct Shared {
    gen: AtomicUsize,
    done: AtomicUsize,
    stop: AtomicBool,
    lists: AtomicPtr<FusedSign>,
    delta: AtomicPtr<SignedDelta>,
    push: AtomicPtr<PushMat>,
    dense: AtomicPtr<DenseQ8>,
    /// activation dense pour le mode 3 (produit scalaire par ligne de sortie)
    xv: AtomicPtr<i32>,
    sx: AtomicUsize,
    outs: AtomicPtr<Vec<Vec<f32>>>,
    /// 0 = listes signées, 1 = listes fusionnées, 2 = listes par source valuées
    mode: AtomicUsize,
    sv_idx: AtomicPtr<u32>,
    sv_val: AtomicPtr<i32>,
    n_active: AtomicUsize,
    accs: AtomicPtr<Vec<Vec<i64>>>,
    touched: AtomicPtr<Vec<Vec<u32>>>,
    spans: AtomicPtr<Vec<(usize, usize)>>,
}

pub struct Pool {
    shared: Arc<Shared>,
    handles: Vec<std::thread::JoinHandle<()>>,
    n: usize,
    n_out: usize,
    accs: Vec<Vec<i64>>,
    touched: Vec<Vec<u32>>,
    /// étendue EXACTE des destinations écrites par chaque worker au dernier
    /// appel : la réduction ne balaie que l'union de ces fenêtres.
    spans: Vec<(usize, usize)>,
    outs: Vec<Vec<f32>>,
    sx_bits: u32,
}

impl Pool {
    /// Crée un pool de `n` workers. `n` est **borné** à `CPU logiques − 1` :
    /// le thread appelant participe à l'attente active, et une machine
    /// sursouscrite effondre le débit (cf. commentaire dans la boucle d'attente).
    pub fn new(n: usize, n_out: usize) -> Self {
        let cpu = std::thread::available_parallelism().map(|p| p.get()).unwrap_or(1);
        let n = n.max(1).min(cpu.saturating_sub(1).max(1));
        let shared = Arc::new(Shared {
            gen: AtomicUsize::new(0),
            done: AtomicUsize::new(0),
            stop: AtomicBool::new(false),
            lists: AtomicPtr::new(std::ptr::null_mut()),
            delta: AtomicPtr::new(std::ptr::null_mut()),
            push: AtomicPtr::new(std::ptr::null_mut()),
            dense: AtomicPtr::new(std::ptr::null_mut()),
            xv: AtomicPtr::new(std::ptr::null_mut()),
            sx: AtomicUsize::new(0),
            outs: AtomicPtr::new(std::ptr::null_mut()),
            mode: AtomicUsize::new(1),
            sv_idx: AtomicPtr::new(std::ptr::null_mut()),
            sv_val: AtomicPtr::new(std::ptr::null_mut()),
            n_active: AtomicUsize::new(0),
            accs: AtomicPtr::new(std::ptr::null_mut()),
            touched: AtomicPtr::new(std::ptr::null_mut()),
            spans: AtomicPtr::new(std::ptr::null_mut()),
        });
        let mut handles = Vec::with_capacity(n);
        for id in 0..n {
            let sh = Arc::clone(&shared);
            handles.push(std::thread::spawn(move || {
                let mut last = 0usize;
                loop {
                    // Attente active d'une nouvelle génération. La barrière
                    // par *spin* n'est tenable que si le nombre de threads
                    // tournants reste inférieur au nombre de CPU logiques :
                    // au-delà, l'ordonnanceur préempte des workers qui tournent
                    // et le débit s'effondre (mesuré : ×3,3 de perte à 40+1
                    // threads sur 40 CPU). `Pool::new` borne donc la taille.
                    loop {
                        let g = sh.gen.load(Ordering::Acquire);
                        if g != last { last = g; break; }
                        if sh.stop.load(Ordering::Relaxed) { return; }
                        std::hint::spin_loop();
                    }
                    // Le réveil peut coïncider avec l'arrêt du pool : sans ce
                    // test, un worker lirait des pointeurs nuls (les champs ne
                    // sont publiés qu'avant un vrai travail).
                    if sh.stop.load(Ordering::Acquire) { return; }
                    let mode = sh.mode.load(Ordering::Relaxed);
                    if mode == 3 {
                        // Mode dense : chaque worker calcule une tranche
                        // contiguë de sorties, sans dispersion ni réduction.
                        let d = unsafe { &*sh.dense.load(Ordering::Acquire) };
                        let xv = unsafe { std::slice::from_raw_parts(
                            sh.xv.load(Ordering::Acquire), d.n_in) };
                        let sx = f32::from_bits(sh.sx.load(Ordering::Relaxed) as u32);
                        let outs = unsafe { &mut *sh.outs.load(Ordering::Acquire) };
                        let per = (d.n_out + n - 1) / n;
                        let lo = id * per;
                        let hi = (lo + per).min(d.n_out);
                        let dst = &mut outs[id];
                        if dst.len() < d.n_out { dst.resize(d.n_out, 0.0); }
                        for o in lo..hi {
                            let mut s = 0i64;
                            let row = &d.q[o * d.n_in..(o + 1) * d.n_in];
                            for i in 0..d.n_in { s += row[i] as i64 * xv[i] as i64; }
                            dst[o] = s as f32 * d.scale[o] * sx;
                        }
                        sh.done.fetch_add(1, Ordering::Release);
                        continue;
                    }
                    let f = unsafe { &*sh.lists.load(Ordering::Acquire) };
                    let dl = unsafe { &*sh.delta.load(Ordering::Acquire) };
                    let pm = unsafe { &*sh.push.load(Ordering::Acquire) };
                    let idx = unsafe { std::slice::from_raw_parts(sh.sv_idx.load(Ordering::Acquire), sh.n_active.load(Ordering::Relaxed)) };
                    let val = unsafe { std::slice::from_raw_parts(sh.sv_val.load(Ordering::Acquire), sh.n_active.load(Ordering::Relaxed)) };
                    let accs = unsafe { &mut *sh.accs.load(Ordering::Acquire) };
                    let touched = unsafe { &mut *sh.touched.load(Ordering::Acquire) };
                    let spans = unsafe { &mut *sh.spans.load(Ordering::Acquire) };
                    let acc = &mut accs[id];
                    let tch = &mut touched[id];
                    let cap = acc.len();         // au-delà, on repasse au memset
                    // Remise à zéro INCRÉMENTALE. Si le suivi a débordé (plus de
                    // `cap` destinations distinctes touchées), un memset complet est
                    // moins cher que de tenir la liste.
                    // Les deux chemins tiennent la même comptabilité de destinations
                    // touchées : si elle a débordé, un memset complet est plus sûr.
                    if tch.len() >= cap {
                        for a in acc.iter_mut() { *a = 0; }
                    } else {
                        for &c in tch.iter() { acc[c as usize] = 0; }
                    }
                    tch.clear();
                    let mut span = (usize::MAX, 0usize);
                    let mut i = id;
                    while i < idx.len() {
                        let src = idx[i] as usize;
                        let xv = val[i] as i64;
                        match mode {
                            1 => { row_fused_into(f, src, xv, acc, tch, cap, &mut span); }
                            2 => { row_val_into(pm, src, xv, acc, tch, cap, &mut span); }
                            _ => { row_delta_into(dl, src, xv, acc, tch, cap, &mut span); }
                        }
                        i += n;
                    }
                    spans[id] = span;
                    sh.done.fetch_add(1, Ordering::Release);
                }
            }));
        }
        Pool { shared, handles, n, n_out, accs: vec![vec![0i64; n_out]; n],
               touched: vec![Vec::new(); n], spans: vec![(usize::MAX, 0usize); n],
               outs: vec![Vec::new(); n], sx_bits: 0f32.to_bits() }
    }

    pub fn threads(&self) -> usize { self.n }

    /// Produit matrice-vecteur **dense** (référence sans événements).
    pub fn matvec_dense_i8(&mut self, d: &DenseQ8, x: &[i32], sx: f32) -> Vec<f32> {
        self.ensure_width(d.n_out);
        let sh = &self.shared;
        sh.mode.store(3, Ordering::Relaxed);
        sh.dense.store(d as *const _ as *mut _, Ordering::Relaxed);
        sh.xv.store(x.as_ptr() as *mut i32, Ordering::Relaxed);
        sh.sx.store(sx.to_bits() as usize, Ordering::Relaxed);
        sh.outs.store(&mut self.outs as *mut Vec<Vec<f32>>, Ordering::Relaxed);
        sh.done.store(0, Ordering::Relaxed);
        sh.gen.fetch_add(1, Ordering::Release);
        while sh.done.load(Ordering::Acquire) != self.n { std::hint::spin_loop(); }
        let mut out = vec![0f32; d.n_out];
        for w in &self.outs {
            for (o, &v) in out.iter_mut().zip(w.iter()) { *o += v; }
        }
        out
    }

    /// Accumulation par **listes par source valuées** : le mode de l'inférence.
    pub fn accumulate_push(&mut self, m: &PushMat, sv: &SparseVec) -> Vec<i64> {
        self.ensure_width(m.n_out);
        self.shared.mode.store(2, Ordering::Relaxed);
        self.shared.push.store(m as *const _ as *mut _, Ordering::Relaxed);
        self.accumulate_common(sv).0
    }

    /// Réajuste la largeur des accumulateurs quand la matrice change de forme
    /// (896, 128, 4864, …). Les listes de destinations touchées deviennent
    /// caduques : on repart d'accumulateurs vides.
    pub fn ensure_width(&mut self, n_out: usize) {
        if n_out == self.n_out { return; }
        self.n_out = n_out;
        for a in self.accs.iter_mut() { a.clear(); a.resize(n_out, 0); }
        for t in self.touched.iter_mut() { t.clear(); }
        for sp in self.spans.iter_mut() { *sp = (usize::MAX, 0); }
    }

    pub fn accumulate_delta(&mut self, d: &SignedDelta, sv: &SparseVec) -> (Vec<i64>, usize) {
        self.shared.mode.store(0, Ordering::Relaxed);
        self.shared.delta.store(d as *const _ as *mut _, Ordering::Relaxed);
        self.accumulate_common(sv)
    }

    pub fn accumulate(&mut self, f: &FusedSign, sv: &SparseVec) -> (Vec<i64>, usize) {
        self.ensure_width(f.n_cols);
        self.shared.mode.store(1, Ordering::Relaxed);
        self.shared.lists.store(f as *const _ as *mut _, Ordering::Relaxed);
        self.accumulate_common(sv)
    }

    fn accumulate_common(&mut self, sv: &SparseVec) -> (Vec<i64>, usize) {
        let sh = &self.shared;
        sh.done.store(0, Ordering::Relaxed);
        sh.sv_idx.store(sv.idx.as_ptr() as *mut _, Ordering::Relaxed);
        sh.sv_val.store(sv.val.as_ptr() as *mut _, Ordering::Relaxed);
        sh.n_active.store(sv.idx.len(), Ordering::Relaxed);
        sh.accs.store(&mut self.accs as *mut Vec<Vec<i64>>, Ordering::Relaxed);
        sh.touched.store(&mut self.touched as *mut Vec<Vec<u32>>, Ordering::Relaxed);
        sh.spans.store(&mut self.spans as *mut Vec<(usize, usize)>, Ordering::Relaxed);
        sh.gen.fetch_add(1, Ordering::Release);       // libère les workers

        while sh.done.load(Ordering::Acquire) != self.n {
            std::hint::spin_loop();
        }
        // Réduction sur l'union des étendues RÉELLEMENT écrites par les workers :
        // la fenêtre est exacte, quel que soit le décodeur, et ne dépend pas de
        // la liste des destinations touchées (qui peut avoir débordé).
        let (mut lo, mut hi) = (usize::MAX, 0usize);
        for &(a, b) in &self.spans {
            if a == usize::MAX { continue; }
            if a < lo { lo = a; }
            if b > hi { hi = b; }
        }
        if lo >= hi { return (vec![0i64; self.n_out], 0); }
        let mut out = vec![0i64; self.n_out];
        for a in &self.accs {
            for (o, v) in out[lo..hi].iter_mut().zip(a[lo..hi].iter()) { *o += *v; }
        }
        (out, sv.idx.len())
    }

    pub fn shutdown(self) { drop(self) }
}

impl Drop for Pool {
    fn drop(&mut self) {
        self.shared.stop.store(true, Ordering::Relaxed);
        self.shared.gen.fetch_add(1, Ordering::Release);
        for h in self.handles.drain(..) { let _ = h.join(); }
    }
}

// --------------------------------------------------------------------------- //
// Références non optimisées (comparaison)
// --------------------------------------------------------------------------- //

#[inline]
pub fn row_delta_into(lists: &SignedDelta, r: usize, xv: i64, acc: &mut [i64],
                      touched: &mut Vec<u32>, cap: usize,
                      span: &mut (usize, usize)) -> usize {
    let data = &lists.data;
    let mut p = lists.row_start[r];
    let n_out = lists.n_cols;
    #[inline(always)]
    fn vi(data: &[u8], p: &mut usize) -> usize {
        let b0 = data[*p];
        if b0 < 0x80 { *p += 1; b0 as usize }
        else {
            let mut v = (b0 & 0x7F) as usize;
            let mut sh = 7;
            *p += 1;
            loop {
                let b = data[*p]; *p += 1;
                v |= ((b & 0x7F) as usize) << sh;
                if b < 0x80 { break; }
                sh += 7;
            }
            v
        }
    }
    let np = vi(data, &mut p);
    let nn = vi(data, &mut p);
    let mut first = usize::MAX;
    let mut last = 0usize;
    let mut c = 0usize;
    for _ in 0..np {
        c += vi(data, &mut p);
        if c < n_out {
            acc[c] += xv;
            if touched.len() < cap { touched.push(c as u32); }
            if first == usize::MAX { first = c; }
            last = c;
        }
    }
    c = 0;
    for _ in 0..nn {
        c += vi(data, &mut p);
        if c < n_out {
            acc[c] -= xv;
            if touched.len() < cap { touched.push(c as u32); }
            if first == usize::MAX { first = c; }
            last = c;
        }
    }
    if first != usize::MAX {
        if first < span.0 { span.0 = first; }
        if last + 1 > span.1 { span.1 = last + 1; }
    }
    np + nn
}

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

#[allow(dead_code)]
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
