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

use crate::list::{DenseQ4, DenseQ8, FusedSign, PushMat, SignedDelta, BLOC_Q4};
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
    #[allow(dead_code)] pub fn len(&self) -> usize { self.idx.len() }
    #[allow(dead_code)] pub fn is_empty(&self) -> bool { self.idx.is_empty() }
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
pub fn row_val_into(m: &PushMat, r: usize, xq: i64, acc: &mut [i32],
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
                unsafe { *acc.get_unchecked_mut(col) += (xq * q) as i32; }
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
                unsafe { *acc.get_unchecked_mut(col) += (xq * q) as i32; }
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
    dense4: AtomicPtr<DenseQ4>,
    /// activation dense pour le mode 3 (produit scalaire par ligne de sortie)
    xv: AtomicPtr<i32>,
    /// mêmes activations en i16, pour le noyau AVX2 du mode 4
    xv16: AtomicPtr<i16>,
    /// sommes des activations par bloc de 32 (terme de minimum de Q4_K)
    xs32: AtomicPtr<i32>,
    sx: AtomicUsize,
    outs: AtomicPtr<Vec<Vec<f32>>>,
    /// 0 = listes signées, 1 = listes fusionnées, 2 = listes par source valuées
    mode: AtomicUsize,
    sv_idx: AtomicPtr<u32>,
    sv_val: AtomicPtr<i32>,
    n_active: AtomicUsize,
    accs: AtomicPtr<Vec<Vec<i32>>>,
    accs64: AtomicPtr<Vec<Vec<i64>>>,
    spans: AtomicPtr<Vec<(usize, usize)>>,
    dirty: AtomicPtr<Vec<usize>>,
}

/// Épingle-t-on les workers ? Réglé une fois par le programme principal.
pub static EPINGLER: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);

/// Épingle le fil courant sur un processeur logique.
///
/// `std` n'expose pas `sched_setaffinity` : on passe par l'appel système
/// direct (numéro 203 sur x86-64). Le masque fait 128 octets, soit 1 024
/// processeurs — la taille maximale que le noyau accepte.
///
/// Intérêt mesuré : les poids sont alloués par le fil principal, donc sur le
/// nœud NUMA 0. Un worker qui tourne sur l'autre socket paie chaque accès au
/// QPI. Au banc : 20,7 Go/s en laissant l'ordonnanceur placer les fils,
/// **24,7 Go/s** en les liant à un socket.
#[cfg(all(target_arch = "x86_64", target_os = "linux"))]
pub fn epingler(cpu: usize) -> bool {
    if cpu >= 1024 { return false; }
    let mut masque = [0u64; 16];
    masque[cpu / 64] |= 1u64 << (cpu % 64);
    let ret: i64;
    unsafe {
        std::arch::asm!(
            "syscall",
            inlateout("rax") 203i64 => ret,   // SYS_sched_setaffinity
            in("rdi") 0usize,                 // 0 = fil courant
            in("rsi") 128usize,               // taille du masque en octets
            in("rdx") masque.as_ptr(),
            lateout("rcx") _,
            lateout("r11") _,
            options(nostack)
        );
    }
    ret == 0
}

/// Processeurs du premier nœud NUMA, cœurs physiques puis frères SMT.
/// Repli : la numérotation linéaire si la topologie n'est pas reconnue.
fn cibles_locales(n: usize) -> Vec<usize> {
    // Chaque nœud liste d'abord ses cœurs physiques, puis leurs frères SMT
    // (`0-9,20-29` pour un Xeon 10 cœurs). On garde la première moitié de
    // chaque nœud : les cœurs physiques des DEUX sockets.
    //
    // Mesuré : lier les seize fils au seul nœud 0 coûte 16 % de débit
    // (23,8 -> 27,6 s sur le 30B MoE). Le gain de localité mémoire ne compense
    // pas la contention SMT — deux fils d'un même cœur se disputent les ports
    // d'émission, et nos ouvriers en attente active en souffrent doublement.
    let mut v = Vec::new();
    for noeud in 0..8 {
        let chemin = format!("/sys/devices/system/node/node{noeud}/cpulist");
        let Ok(txt) = std::fs::read_to_string(&chemin) else { break };
        let mut cpus = Vec::new();
        for morceau in txt.trim().split(',') {
            if let Some((a, b)) = morceau.split_once('-') {
                if let (Ok(a), Ok(b)) = (a.parse::<usize>(), b.parse::<usize>()) {
                    cpus.extend(a..=b);
                }
            } else if let Ok(a) = morceau.parse::<usize>() { cpus.push(a); }
        }
        let physiques = cpus.len() / 2;
        v.extend_from_slice(&cpus[..physiques.max(1)]);
    }
    if v.is_empty() { v = (0..n).collect(); }
    v
}

pub struct Pool {
    shared: Arc<Shared>,
    handles: Vec<std::thread::JoinHandle<()>>,
    n: usize,
    n_out: usize,
    accs: Vec<Vec<i32>>,
    accs64: Vec<Vec<i64>>,
    /// étendue EXACTE des destinations écrites par chaque worker au dernier
    /// appel : la réduction ne balaie que l'union de ces fenêtres.
    spans: Vec<(usize, usize)>,
    /// Borne haute CUMULATIVE des écritures depuis le dernier effacement
    /// complet, par worker. Remettre à zéro la seule fenêtre du travail
    /// précédent ne suffit pas : si elle rétrécit, des valeurs plus anciennes
    /// survivent au-delà (bug trouvé par le banc : divergence au rang 895).
    dirty: Vec<usize>,
    outs: Vec<Vec<f32>>,
    /// Mode du dernier appel : la réduction doit lire l'accumulateur qui a
    /// réellement servi (i32 pour le mode push, i64 pour fusion et 2-listes).
    last_mode: usize,
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
            dense4: AtomicPtr::new(std::ptr::null_mut()),
            xv: AtomicPtr::new(std::ptr::null_mut()),
            xv16: AtomicPtr::new(std::ptr::null_mut()),
            xs32: AtomicPtr::new(std::ptr::null_mut()),
            sx: AtomicUsize::new(0),
            outs: AtomicPtr::new(std::ptr::null_mut()),
            mode: AtomicUsize::new(1),
            sv_idx: AtomicPtr::new(std::ptr::null_mut()),
            sv_val: AtomicPtr::new(std::ptr::null_mut()),
            n_active: AtomicUsize::new(0),
            accs: AtomicPtr::new(std::ptr::null_mut()),
            accs64: AtomicPtr::new(std::ptr::null_mut()),
            spans: AtomicPtr::new(std::ptr::null_mut()),
            dirty: AtomicPtr::new(std::ptr::null_mut()),
        });
        let mut handles = Vec::with_capacity(n);
        let epingle = EPINGLER.load(Ordering::Relaxed);
        let cibles = if epingle { cibles_locales(n) } else { Vec::new() };
        for id in 0..n {
            let sh = Arc::clone(&shared);
            let cpu = if epingle && !cibles.is_empty() {
                Some(cibles[id % cibles.len()])
            } else { None };
            handles.push(std::thread::spawn(move || {
                if let Some(c) = cpu { epingler(c); }
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
                    if mode == 4 {
                        // Mode 4 bits : même découpage que le mode 3, mais les
                        // poids tiennent sur un demi-octet — c'est le seul
                        // levier qui reste quand le noyau est au mur mémoire.
                        let d = unsafe { &*sh.dense4.load(Ordering::Acquire) };
                        let xv = unsafe { std::slice::from_raw_parts(
                            sh.xv16.load(Ordering::Acquire), d.n_in) };
                        let xs = unsafe { std::slice::from_raw_parts(
                            sh.xs32.load(Ordering::Acquire), d.n_in / BLOC_Q4 + 1) };
                        let sx = f32::from_bits(sh.sx.load(Ordering::Relaxed) as u32);
                        let outs = unsafe { &mut *sh.outs.load(Ordering::Acquire) };
                        let per = (d.n_out + n - 1) / n;
                        let lo = id * per;
                        let hi = (lo + per).min(d.n_out);
                        let dst = &mut outs[id];
                        if dst.len() < d.n_out { dst.resize(d.n_out, 0.0); }
                        for v in dst[..lo].iter_mut() { *v = 0.0; }
                        for v in dst[hi..].iter_mut() { *v = 0.0; }
                        for o in lo..hi { dst[o] = d.dot16(o, xv, xs) * sx; }
                        sh.done.fetch_add(1, Ordering::Release);
                        continue;
                    }
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
                        // Hors de sa tranche, ce worker doit laisser des ZÉROS :
                        // `matvec_dense_i8` somme les vecteurs de TOUS les
                        // workers, et une case non écrite garderait la valeur du
                        // travail précédent (bug mesuré : PPL 4 361 879 au lieu de
                        // 19,26 — chaque sortie recevait n-1 restes périmés).
                        for v in dst[..lo].iter_mut() { *v = 0.0; }
                        for v in dst[hi..].iter_mut() { *v = 0.0; }
                        for o in lo..hi {
                            // Même ordre d'opérations que le chemin par
                            // événements : `acc × (échelle_poids × échelle_act)`.
                            // Les sommes entières étant exactes des deux côtés,
                            // cette seule parenthèse rend les deux modes
                            // **bit à bit identiques** — changer de mode
                            // d'exécution ne change plus un seul token.
                            dst[o] = match d.src {
                                // Blocs du fichier : l'échelle est déjà celle du
                                // bloc, il ne reste que celle de l'activation.
                                crate::list::Source8::Q8_0 => d.dot_q8_source(o, xv) * sx,
                                // Échelles par bloc construites par nous.
                                crate::list::Source8::PropreBloc => d.dot_blocs(o, xv) * sx,
                                crate::list::Source8::Propre =>
                                    d.dot_chunked(o, xv) as f32 * (d.scale[o] * sx),
                            };
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
                    let accs64 = unsafe { &mut *sh.accs64.load(Ordering::Acquire) };
                    let spans = unsafe { &mut *sh.spans.load(Ordering::Acquire) };
                    let dirty = unsafe { &mut *sh.dirty.load(Ordering::Acquire) };
                    let acc = &mut accs[id];
                    let acc64 = &mut accs64[id];
                    // Remise à zéro par FENÊTRE : les spans du travail précédent
                    // donnent exactement les adresses écrites. Tenir une liste des
                    // destinations touchées coûtait six micro-opérations par
                    // événement pour économiser 0,2 % du temps de token — mesuré :
                    // 92 ms -> 51 ms sur le MLP, +48 % de débit.
                    // Les deux accumulateurs sont balayés : selon le mode, c'est
                    // l'un ou l'autre qui a servi au travail précédent.
                    let hi_prev = dirty[id];
                    if hi_prev > 0 {
                        for a in acc[0..hi_prev].iter_mut() { *a = 0; }
                        for a in acc64[0..hi_prev].iter_mut() { *a = 0; }
                    }
                    let mut span = (usize::MAX, 0usize);
                    let mut i = id;
                    while i < idx.len() {
                        let src = idx[i] as usize;
                        let xv = val[i] as i64;
                        match mode {
                            1 => { row_fused_into(f, src, xv, acc64, &mut span); }
                            2 => { row_val_into(pm, src, xv, acc, &mut span); }
                            _ => { row_delta_into(dl, src, xv, acc64, &mut span); }
                        }
                        i += n;
                    }
                    spans[id] = span;
                    if span.1 > dirty[id] { dirty[id] = span.1; }
                    sh.done.fetch_add(1, Ordering::Release);
                }
            }));
        }
        Pool { shared, handles, n, n_out, accs: vec![vec![0i32; n_out]; n], accs64: vec![vec![0i64; n_out]; n],
               spans: vec![(usize::MAX, 0usize); n],
               dirty: vec![0usize; n],
               outs: vec![Vec::new(); n], last_mode: 1 }
    }

    pub fn threads(&self) -> usize { self.n }

    /// Produit matrice-vecteur **dense** (référence sans événements).
    /// Produit matrice-vecteur avec des poids **4 bits** (mode 4).
    pub fn matvec_dense_q4(&mut self, d: &DenseQ4, x: &[i32], sx: f32) -> Vec<f32> {
        self.ensure_width(d.n_out);
        let sh = &self.shared;
        sh.mode.store(4, Ordering::Relaxed);
        sh.dense4.store(d as *const _ as *mut _, Ordering::Relaxed);
        // Conversion i32 → i16 faite UNE fois par appel : les noyaux la
        // referaient sinon pour chaque ligne de sortie (4 864 fois).
        let xi: Vec<i16> = x.iter().map(|&v| v.clamp(-32767, 32767) as i16).collect();
        let xs = crate::list::sommes32(&xi);
        sh.xv16.store(xi.as_ptr() as *mut i16, Ordering::Relaxed);
        sh.xs32.store(xs.as_ptr() as *mut i32, Ordering::Relaxed);
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

    /// Produit **matrice-matrice** int8 : `t` jetons contre la même matrice.
    ///
    /// C'est tout le préremplissage par lots : un produit matrice-vecteur relit
    /// la matrice entière pour CHAQUE jeton, alors qu'ici chaque ligne de poids
    /// est lue une fois et sert à tout le lot. Le décodage reste au matvec (il
    /// n'a qu'un jeton), le préremplissage passe par ici.
    ///
    /// `x` est le lot d'activations (t × n_in), `sx` les t échelles, `out` reçoit
    /// t × n_out en disposition jeton-majeur.
    pub fn gemm_dense_i8(&self, d: &DenseQ8, x: &[i32], t: usize, sx: &[f32], out: &mut [f32]) {
        /// Jeton par groupe : assez pour amortir la lecture d'une ligne de poids,
        /// assez peu pour que les activations du groupe restent en L1.
        const TUILE: usize = 16;
        use crate::list::Source8;
        let n_out = d.n_out;
        let n_in = d.n_in;
        let nt = self.n.max(1);
        let par = n_out.div_ceil(nt);
        // Chaque fil prend une tranche de LIGNES et parcourt tout le lot : la
        // ligne reste chaude, le poids n'est lu qu'une fois.
        std::thread::scope(|sc| {
            let mut reste = out;
            let mut base = 0usize;
            for _ in 0..nt {
                let lo = base;
                let hi = (base + par).min(n_out);
                if lo >= hi { break; }
                // Disposition en sortie : ligne-majeur (n_out × t), donc la
                // tranche de lignes d'un fil est contiguë.
                let (morceau, suite) = reste.split_at_mut((hi - lo) * t);
                reste = suite;
                sc.spawn(move || {
                    // Tuilage : un groupe de `TUILE` jetons tient dans le cache
                    // pendant qu'on parcourt les lignes. Sans cela, chaque ligne
                    // relit TOUT le lot d'activations (mesuré : le lot était plus
                    // LENT que le jeton par jeton, 23 s contre 16,6).
                    for i0 in (0..t).step_by(TUILE) {
                        let i1 = (i0 + TUILE).min(t);
                        for (j, o) in (lo..hi).enumerate() {
                            for i in i0..i1 {
                                let xi = &x[i * n_in..(i + 1) * n_in];
                                let v = match d.src {
                                    Source8::Q8_0 => d.dot_q8_source(o, xi),
                                    Source8::PropreBloc => d.dot_blocs(o, xi),
                                    Source8::Propre => d.dot_chunked(o, xi) as f32 * d.scale[o],
                                };
                                morceau[j * t + i] = v * sx[i];
                            }
                        }
                    }
                });
                base = hi;
            }
        });
    }

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

    /// Produit **matrice-matrice** sur une matrice 4 bits (experts MXFP4 de
    /// gpt-oss, poids Q4_K de la famille Qwen).
    ///
    /// Même principe que `gemm_dense_i8` : une tranche de lignes par fil, et
    /// toute la ligne de poids sert à tout le lot — c'est ce qui amortit la
    /// lecture des 128 matrices d'experts d'une couche MoE.
    ///
    /// `x16` est le lot d'activations en i16, `s32[i]` les sommes par bloc de 32
    /// du jeton i (précalculées une fois : le noyau les referait 4 864 fois),
    /// `sx[i]` l'échelle d'activation du jeton i. Sortie en (n_out × t).
    pub fn gemm_dense_q4(&self, d: &crate::list::DenseQ4, x16: &[i16], t: usize,
                         s32: &[Vec<i32>], sx: &[f32], out: &mut [f32]) {
        /// Même tuilage que le chemin int8 : les sommes par bloc de 32 du groupe
        /// restent au chaud pendant la lecture des lignes.
        const TUILE_Q4: usize = 8;
        let n_out = d.n_out;
        let n_in = d.n_in;
        let nt = self.n.max(1);
        let par = n_out.div_ceil(nt);
        std::thread::scope(|sc| {
            let mut reste = out;
            let mut base = 0usize;
            while base < n_out {
                let hi = (base + par).min(n_out);
                let (morceau, suite) = reste.split_at_mut((hi - base) * t);
                reste = suite;
                sc.spawn(move || {
                    for i0 in (0..t).step_by(TUILE_Q4) {
                        let i1 = (i0 + TUILE_Q4).min(t);
                        for (j, o) in (base..hi).enumerate() {
                            for i in i0..i1 {
                                let xi = &x16[i * n_in..(i + 1) * n_in];
                                morceau[j * t + i] = d.dot16(o, xi, &s32[i]) * sx[i];
                            }
                        }
                    }
                });
                base = hi;
            }
        });
    }

    /// Accumulation par **listes par source valuées** : le mode de l'inférence.
    pub fn accumulate_push(&mut self, m: &PushMat, sv: &SparseVec) -> Vec<i64> {
        self.ensure_width(m.n_out);
        self.last_mode = 2;
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
        for a in self.accs64.iter_mut() { a.clear(); a.resize(n_out, 0); }
        for d in self.dirty.iter_mut() { *d = 0; }
        for sp in self.spans.iter_mut() { *sp = (usize::MAX, 0); }
        for d in self.dirty.iter_mut() { *d = 0; }
    }

    pub fn accumulate_delta(&mut self, d: &SignedDelta, sv: &SparseVec) -> (Vec<i64>, usize) {
        self.last_mode = 0;
        self.shared.mode.store(0, Ordering::Relaxed);
        self.shared.delta.store(d as *const _ as *mut _, Ordering::Relaxed);
        self.accumulate_common(sv)
    }

    pub fn accumulate(&mut self, f: &FusedSign, sv: &SparseVec) -> (Vec<i64>, usize) {
        self.ensure_width(f.n_cols);
        self.last_mode = 1;
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
        sh.accs.store(&mut self.accs as *mut Vec<Vec<i32>>, Ordering::Relaxed);
        sh.accs64.store(&mut self.accs64 as *mut Vec<Vec<i64>>, Ordering::Relaxed);
        sh.spans.store(&mut self.spans as *mut Vec<(usize, usize)>, Ordering::Relaxed);
        sh.dirty.store(&mut self.dirty as *mut Vec<usize>, Ordering::Relaxed);
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
        if self.last_mode == 2 {
            for a in &self.accs {
                for (o, v) in out[lo..hi].iter_mut().zip(a[lo..hi].iter()) { *o += *v as i64; }
            }
        } else {
            for a in &self.accs64 {
                for (o, v) in out[lo..hi].iter_mut().zip(a[lo..hi].iter()) { *o += *v; }
            }
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
            if first == usize::MAX { first = c; }
            last = c;
        }
    }
    c = 0;
    for _ in 0..nn {
        c += vi(data, &mut p);
        if c < n_out {
            acc[c] -= xv;
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

#[cfg(test)]
mod tests_gemm {
    use super::*;
    use crate::list::DenseQ8;

    /// Le préremplissage par lots ne vaut que si le poids est lu UNE fois pour
    /// tout le lot. On le vérifie au noyau : T produits matrice-vecteur contre
    /// un produit matrice-matrice de T jetons, sur une matrice de taille réelle.
    #[test]
    fn gemm_bat_le_matvec() {
        let (n_out, n_in, t) = (4864usize, 896usize, 16usize);
        let w: Vec<f32> = (0..n_out * n_in)
            .map(|k| ((k * 2654435761) % 1000) as f32 / 500.0 - 1.0).collect();
        let d = DenseQ8::build(&w, n_out, n_in);
        let mut pool = Pool::new(8, n_in);
        let x: Vec<i32> = (0..t * n_in).map(|k| ((k * 7919) % 61) as i32 - 30).collect();
        let sx: Vec<f32> = (0..t).map(|i| 0.001 * (i + 1) as f32).collect();

        let t0 = std::time::Instant::now();
        for _ in 0..4 {
            for i in 0..t {
                let xi = &x[i * n_in..(i + 1) * n_in];
                let _ = pool.matvec_dense_i8(&d, xi, sx[i]);
            }
        }
        let par_matvec = t0.elapsed().as_secs_f64() / 4.0;

        let mut out = vec![0f32; n_out * t];
        let t1 = std::time::Instant::now();
        for _ in 0..4 {
            pool.gemm_dense_i8(&d, &x, t, &sx, &mut out);
        }
        let par_gemm = t1.elapsed().as_secs_f64() / 4.0;
        println!("{t} jetons : matvec {:.1} ms · gemm {:.1} ms · gain ×{:.2}",
                 par_matvec * 1e3, par_gemm * 1e3, par_matvec / par_gemm);
        // Les deux doivent donner le MÊME résultat (aux arrondis près).
        for i in 0..t {
            let xi = &x[i * n_in..(i + 1) * n_in];
            let r = pool.matvec_dense_i8(&d, xi, sx[i]);
            for o in 0..n_out {
                assert!((r[o] - out[o * t + i]).abs() <= 1e-3 * r[o].abs().max(1.0),
                        "ligne {o} jeton {i} : {} contre {}", r[o], out[o * t + i]);
            }
        }
    }
}

#[cfg(test)]
mod tests_gemm_q4 {
    use super::*;
    use crate::list::DenseQ4;

    /// Le produit matrice-matrice 4 bits doit rendre EXACTEMENT ce que rendent
    /// les produits matrice-vecteur qu'il remplace (mêmes sommes entières, même
    /// ordre par ligne).
    #[test]
    fn gemm_q4_egale_matvec() {
        // Matrice 4 bits construite par `build` : 4 bits propres, échelle par ligne.
        let (n_out, n_in, t) = (128usize, 256usize, 8usize);
        let w: Vec<f32> = (0..n_out * n_in)
            .map(|k| (((k * 1103515245 + 12345) % 2000) as f32 / 1000.0) - 1.0).collect();
        let d = DenseQ4::build(&w, n_out, n_in);
        let pool = Pool::new(4, n_in);
        let x: Vec<i32> = (0..t * n_in).map(|k| ((k * 7919) % 101) as i32 - 50).collect();
        let x16: Vec<Vec<i16>> = (0..t).map(|i| {
            x[i * n_in..(i + 1) * n_in].iter().map(|&v| v as i16).collect()
        }).collect();
        let s32: Vec<Vec<i32>> = x16.iter().map(|v| crate::list::sommes32(v)).collect();
        let sx: Vec<f32> = (0..t).map(|i| 0.002 * (i + 1) as f32).collect();
        let plat: Vec<i16> = x16.concat();
        let mut out = vec![0f32; n_out * t];
        pool.gemm_dense_q4(&d, &plat, t, &s32, &sx, &mut out);
        for i in 0..t {
            for o in 0..n_out {
                let attendu = d.dot16(o, &x16[i], &s32[i]) * sx[i];
                assert!((out[o * t + i] - attendu).abs() <= 1e-4 * attendu.abs().max(1.0),
                        "ligne {o} jeton {i} : {} contre {}", out[o * t + i], attendu);
            }
        }
    }
}
