//! Inférence Qwen2 en **mode listes d'événements** — std seul, sans GPU, sans
//! bibliothèque de tenseurs.
//!
//! Chaque matrice de poids est stockée en listes par source
//! (`PushMat` : écart de sortie en varint + valeur int8) et parcourue par le
//! moteur d'événements (`Pool`). Les activations sont quantifiées en int8 à la
//! volée, une échelle par vecteur : le produit est **entier**, l'échelle ne
//! revient qu'une fois par sortie.
//!
//! Seule exception : la tête de sortie (151 936 sorties) est calculée par
//! produits scalaires sur les lignes Q8_0 d'origine. En mode push il faudrait un
//! accumulateur de 151 936 × 8 octets **par worker** (36 Mo) et chaque sortie
//! serait écrite 896 fois : le déséquilibre est structurel, pas un compromis de
//! précision. Le reste du modèle — 99,7 % des poids — passe par les événements.

use crate::engine::{Pool, SparseVec};
use crate::gguf::Gguf;
use crate::list::{DenseQ8, PushMat};
use std::time::Instant;

// --------------------------------------------------------------------------- //
// Configuration
// --------------------------------------------------------------------------- //

pub struct Cfg {
    pub n_layer: usize,
    pub hidden: usize,
    pub n_head: usize,
    pub n_kv_head: usize,
    pub head_dim: usize,
    pub ffn: usize,
    pub eps: f32,
    pub rope_base: f32,
    pub vocab: usize,
}

/// Une projection, dans l'un des deux formats, plus son biais éventuel.
/// `m` = listes d'événements (architecture du projet) ;
/// `d` = matrice dense int8 (référence de comparaison, sans événements).
pub struct Proj {
    pub m: Option<PushMat>,
    pub d: Option<DenseQ8>,
    pub bias: Option<Vec<f32>>,
}

pub struct Layer {
    pub attn_norm: Vec<f32>,
    pub wq: Proj,
    pub wk: Proj,
    pub wv: Proj,
    pub wo: Proj,
    pub ffn_norm: Vec<f32>,
    pub wgate: Proj,
    pub wup: Proj,
    pub wdown: Proj,
}

pub struct Stats {
    pub events: u64,
    pub prompt_s: f64,
    pub gen_s: f64,
    pub n_prompt: usize,
    pub n_gen: usize,
}

// --------------------------------------------------------------------------- //
// Chargement
// --------------------------------------------------------------------------- //

impl Proj {
    fn load(g: &Gguf, name: &str, bias: Option<&str>, dense: bool) -> Self {
        let t = g.tensor(name).unwrap_or_else(|| panic!("tenseur {name} absent"));
        let n_out = t.dims[0] as usize;
        let n_in = t.dims[1] as usize;
        let w = g.dequant(name);
        let (m, d) = if dense {
            (None, Some(DenseQ8::build(&w, n_out, n_in)))
        } else {
            (Some(PushMat::build(&w, n_out, n_in)), None)
        };
        let bias = bias.map(|b| g.dequant(b));
        Proj { m, d, bias }
    }
}

pub struct Model {
    pub g: Gguf,
    pub cfg: Cfg,
    pub layers: Vec<Layer>,
    pub out_norm: Vec<f32>,
    pub pool: Pool,
    /// cache KV, par couche : `[n_kv_head × ctx × head_dim]`
    kv_k: Vec<Vec<f32>>,
    kv_v: Vec<Vec<f32>>,
    pub ctx: usize,
    pub events: u64,
    /// Nombre de niveaux de quantification des **activations** (127 pour int8,
    /// 32767 pour int16). Les poids restent int8 : c'est la précision de
    /// l'activation qui décide de la fidélité au modèle flottant.
    pub act_levels: f32,
    /// Token d'arrêt (EOS / <|im_end|>) : la génération s'interrompt dessus.
    pub stop_id: Option<u32>,
}

impl Model {
    pub fn load(path: &str, ctx: usize, n_threads: usize, dense: bool) -> Model {
        let t0 = Instant::now();
        let g = Gguf::open(path).expect("ouverture du GGUF");
        let cfg = Cfg {
            n_layer: g.cfg("block_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
            hidden: g.cfg("embedding_length").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
            n_head: g.cfg("attention.head_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
            n_kv_head: g.cfg("attention.head_count_kv").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
            ffn: g.cfg("feed_forward_length").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
            eps: g.cfg("attention.layer_norm_rms_epsilon").and_then(|m| m.as_f64()).unwrap_or(1e-6) as f32,
            rope_base: g.cfg("rope.freq_base").and_then(|m| m.as_f64()).unwrap_or(10000.0) as f32,
            vocab: g.tensor("token_embd.weight").map(|t| t.dims[0] as usize).unwrap_or(0),
            head_dim: 0,
        };
        let cfg = {
            let mut c = cfg;
            c.head_dim = c.hidden / c.n_head.max(1);
            c
        };
        assert_eq!(cfg.head_dim * cfg.n_head, cfg.hidden, "hidden doit être n_head × head_dim");
        let mut layers = Vec::with_capacity(cfg.n_layer);
        let mut bytes = 0u64;
        for l in 0..cfg.n_layer {
            let p = |s: &str| format!("blk.{l}.{s}");
            let lay = Layer {
                attn_norm: g.dequant(&p("attn_norm.weight")),
                wq: Proj::load(&g, &p("attn_q.weight"), Some(&p("attn_q.bias")), dense),
                wk: Proj::load(&g, &p("attn_k.weight"), Some(&p("attn_k.bias")), dense),
                wv: Proj::load(&g, &p("attn_v.weight"), Some(&p("attn_v.bias")), dense),
                wo: Proj::load(&g, &p("attn_output.weight"), None, dense),
                ffn_norm: g.dequant(&p("ffn_norm.weight")),
                wgate: Proj::load(&g, &p("ffn_gate.weight"), None, dense),
                wup: Proj::load(&g, &p("ffn_up.weight"), None, dense),
                wdown: Proj::load(&g, &p("ffn_down.weight"), None, dense),
            };
            for pj in [&lay.wq, &lay.wk, &lay.wv, &lay.wo, &lay.wgate, &lay.wup, &lay.wdown] {
                if let Some(m) = &pj.m { bytes += m.data.len() as u64; }
                if let Some(d) = &pj.d { bytes += d.q.len() as u64 + d.scale.len() as u64 * 4; }
            }
            layers.push(lay);
        }
        let out_norm = g.dequant("output_norm.weight");
        let kv = vec![0f32; cfg.n_kv_head * ctx * cfg.head_dim];
        let pool = Pool::new(n_threads, cfg.hidden);
        eprintln!("[modele] {} couches chargées en {:?} — listes {:.2} Go, {} threads",
                  cfg.n_layer, t0.elapsed(), bytes as f64 / 1e9, pool.threads());
        let n_layer = cfg.n_layer;
        Model {
            g, cfg, layers, out_norm, pool,
            kv_k: vec![kv.clone(); n_layer], kv_v: vec![kv; n_layer],
            ctx, events: 0, act_levels: 127.0, stop_id: None,
        }
    }

    // ----------------------------------------------------------------------- //
    // Briques de calcul
    // ----------------------------------------------------------------------- //

    /// Quantifie un vecteur (une échelle pour tout le vecteur).
    #[inline]
    fn quant(x: &[f32], levels: f32) -> Option<(SparseVec, f32)> {
        let mut mx = 0f32;
        for &v in x { let a = v.abs(); if a > mx { mx = a; } }
        if mx == 0.0 { return None; }
        let s = mx / levels;
        let inv = 1.0 / s;
        let mut sv = SparseVec { idx: Vec::with_capacity(x.len()), val: Vec::with_capacity(x.len()) };
        for (i, &v) in x.iter().enumerate() {
            let q = (v * inv).round();
            if q != 0.0 { sv.idx.push(i as u32); sv.val.push(q as i32); }
        }
        Some((sv, s))
    }

    /// Produit matrice-vecteur **par événements** : les activations actives
    /// poussent leur contribution dans les sorties de leur liste.
    fn matvec(pool: &mut Pool, p: &Proj, x: &[f32], out: &mut [f32], events: &mut u64, levels: f32) {
        let Some((sv, sx)) = Self::quant(x, levels) else {
            for (o, v) in out.iter_mut().enumerate() {
                *v = p.bias.as_ref().map_or(0.0, |b| b[o]);
            }
            return;
        };
        if let Some(d) = &p.d {
            // référence dense : pas d'événement, chaque sortie est un produit
            // scalaire complet sur la ligne de poids
            let mut xd = vec![0i32; x.len()];
            for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { xd[i as usize] = v; }
            let y = pool.matvec_dense_i8(d, &xd, sx);
            for o in 0..d.n_out {
                out[o] = y[o] + p.bias.as_ref().map_or(0.0, |b| b[o]);
            }
        } else {
            let m = p.m.as_ref().expect("projection sans format");
            for &i in &sv.idx { *events += m.row_ev[i as usize] as u64; }
            let acc = pool.accumulate_push(m, &sv);
            for o in 0..m.n_out {
                let mut y = acc[o] as f32 * (sx * m.scale[o]);
                if let Some(b) = &p.bias { y += b[o]; }
                out[o] = y;
            }
        }
    }

    fn rmsnorm(x: &[f32], w: &[f32], eps: f32, out: &mut [f32]) {
        let mut ss = 0f32;
        for &v in x { ss += v * v; }
        let inv = 1.0 / (ss / x.len() as f32 + eps).sqrt();
        for i in 0..x.len() { out[i] = x[i] * inv * w[i]; }
    }

    /// RoPE « neox » (Qwen2) : rotation des deux moitiés de chaque tête.
    fn rope(v: &mut [f32], n_head: usize, head_dim: usize, pos: usize, base: f32) {
        let half = head_dim / 2;
        for h in 0..n_head {
            let t = &mut v[h * head_dim..(h + 1) * head_dim];
            for i in 0..half {
                let freq = 1.0 / base.powf(2.0 * i as f32 / head_dim as f32);
                let (s, c) = (pos as f32 * freq).sin_cos();
                let a = t[i];
                let b = t[i + half];
                t[i] = a * c - b * s;
                t[i + half] = b * c + a * s;
            }
        }
    }

    /// Un token, une position. Retourne l'état caché après la dernière norme.
    pub fn forward(&mut self, tok: u32, pos: usize) -> Vec<f32> {
        assert!(pos < self.ctx, "contexte dépassé ({pos} ≥ {})", self.ctx);
        let Model { g, cfg, layers, out_norm, pool, kv_k, kv_v, events, .. } = self;
        let h = cfg.hidden;
        let hd = cfg.head_dim;
        let nh = cfg.n_head;
        let nkv = cfg.n_kv_head;
        let rep = nh / nkv;
        let ctx = self.ctx;

        let mut x = g.row_f32("token_embd.weight", tok as usize, h);
        let mut hn = vec![0f32; h];
        let mut q = vec![0f32; h];
        let mut k = vec![0f32; nkv * hd];
        let mut v = vec![0f32; nkv * hd];
        let mut att = vec![0f32; h];
        let mut o = vec![0f32; h];
        let mut gate = vec![0f32; cfg.ffn];
        let mut up = vec![0f32; cfg.ffn];
        let mut down = vec![0f32; h];
        let mut sc = vec![0f32; pos + 1];

        for l in 0..cfg.n_layer {
            let lay = &layers[l];
            Self::rmsnorm(&x, &lay.attn_norm, cfg.eps, &mut hn);
            Self::matvec(pool, &lay.wq, &hn, &mut q, events, self.act_levels);
            Self::matvec(pool, &lay.wk, &hn, &mut k, events, self.act_levels);
            Self::matvec(pool, &lay.wv, &hn, &mut v, events, self.act_levels);
            Self::rope(&mut q, nh, hd, pos, cfg.rope_base);
            Self::rope(&mut k, nkv, hd, pos, cfg.rope_base);
            // écriture du cache KV à la position courante
            {
                let kc = &mut kv_k[l];
                let vc = &mut kv_v[l];
                for hh in 0..nkv {
                    let dst = (hh * ctx + pos) * hd;
                    kc[dst..dst + hd].copy_from_slice(&k[hh * hd..(hh + 1) * hd]);
                    vc[dst..dst + hd].copy_from_slice(&v[hh * hd..(hh + 1) * hd]);
                }
            }
            // attention groupée
            let scale = 1.0 / (hd as f32).sqrt();
            let kc = &kv_k[l];
            let vc = &kv_v[l];
            for hh in 0..nh {
                let kvh = hh / rep;
                let qh = &q[hh * hd..(hh + 1) * hd];
                for t in 0..=pos {
                    let kt = &kc[(kvh * ctx + t) * hd..(kvh * ctx + t) * hd + hd];
                    let mut s = 0f32;
                    for d in 0..hd { s += qh[d] * kt[d]; }
                    sc[t] = s * scale;
                }
                // softmax stable
                let mut mx = f32::NEG_INFINITY;
                for t in 0..=pos { if sc[t] > mx { mx = sc[t]; } }
                let mut sum = 0f32;
                for t in 0..=pos { sc[t] = (sc[t] - mx).exp(); sum += sc[t]; }
                let inv = 1.0 / sum;
                for t in 0..=pos { sc[t] *= inv; }
                for d in 0..hd {
                    let mut s = 0f32;
                    for t in 0..=pos { s += sc[t] * vc[(kvh * ctx + t) * hd + d]; }
                    att[hh * hd + d] = s;
                }
            }
            Self::matvec(pool, &lay.wo, &att, &mut o, events, self.act_levels);
            for i in 0..h { o[i] += x[i]; }

            Self::rmsnorm(&o, &lay.ffn_norm, cfg.eps, &mut hn);
            Self::matvec(pool, &lay.wgate, &hn, &mut gate, events, self.act_levels);
            Self::matvec(pool, &lay.wup, &hn, &mut up, events, self.act_levels);
            for i in 0..cfg.ffn { gate[i] = (gate[i] / (1.0 + (-gate[i]).exp())) * up[i]; }
            Self::matvec(pool, &lay.wdown, &gate, &mut down, events, self.act_levels);
            for i in 0..h { x[i] = o[i] + down[i]; }
        }
        Self::rmsnorm(&x, out_norm, cfg.eps, &mut hn);
        hn
    }

    /// Tête de sortie : produits scalaires entiers sur les lignes Q8_0 du
    /// plafond d'embedding (poids liés). Parallélisé par tranches de vocabulaire.
    pub fn logits(&self, h: &[f32]) -> Vec<f32> {
        let (sv, sx) = match Self::quant(h, self.act_levels) {
            Some(v) => v,
            None => return vec![0f32; self.cfg.vocab],
        };
        // int16 : la troncature en i8 ruinerait une activation quantifiée sur
        // 32767 niveaux (le corps du modèle, lui, n'est pas concerné : il
        // transporte des i32 dans le vecteur creux).
        let mut qx = vec![0i16; h.len()];
        for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { qx[i as usize] = v as i16; }
        let vocab = self.cfg.vocab;
        let view = self.g.q8_view("token_embd.weight");
        let nt = self.pool.threads().max(1);
        let chunk = (vocab + nt - 1) / nt;
        let mut out = vec![0f32; vocab];
        let g = &self.g;
        let view = &view;
        std::thread::scope(|s| {
            for (ci, part) in out.chunks_mut(chunk).enumerate() {
                let qx = &qx;
                s.spawn(move || {
                    let base = ci * chunk;
                    for (j, o) in part.iter_mut().enumerate() {
                        *o = g.q8_dot_at(view, base + j, qx) * sx;
                    }
                });
            }
        });
        out
    }

    /// Génère `n_new` tokens après `ids`. `temp` ≤ 0 ⇒ glouton (déterministe).
    pub fn generate(&mut self, ids: &[u32], n_new: usize, temp: f32) -> (Vec<u32>, Stats) {
        let t0 = Instant::now();
        let mut last = Vec::new();
        let mut events0 = self.events;
        for (pos, &t) in ids.iter().enumerate() {
            last = self.forward(t, pos);
        }
        let prompt_s = t0.elapsed().as_secs_f64();
        let prompt_events = self.events - events0;
        let mut out = Vec::with_capacity(n_new);
        let t1 = Instant::now();
        for step in 0..n_new {
            let logits = self.logits(&last);
            let next = if temp <= 0.0 {
                let mut best = 0usize;
                for (i, &v) in logits.iter().enumerate() { if v > logits[best] { best = i; } }
                best as u32
            } else {
                sample(&logits, temp)
            };
            out.push(next);
            if Some(next) == self.stop_id { break; }
            let pos = ids.len() + step;
            last = self.forward(next, pos);
        }
        let gen_s = t1.elapsed().as_secs_f64();
        events0 = self.events - events0 - prompt_events;
        let _ = events0;
        let st = Stats {
            events: self.events,
            prompt_s, gen_s,
            n_prompt: ids.len(), n_gen: out.len(),
        };
        (out, st)
    }

    pub fn events_total(&self) -> u64 { self.events }
    pub fn reset_events(&mut self) { self.events = 0; }
}

/// Échantillonnage température + top-k (k = 40), avec un générateur xorshift
/// déterministe : pas de dépendance, pas d'entropie système.
fn sample(logits: &[f32], temp: f32) -> u32 {
    let mut idx: Vec<u32> = (0..logits.len() as u32).collect();
    idx.sort_unstable_by(|&a, &b| logits[b as usize].partial_cmp(&logits[a as usize]).unwrap());
    let k = 40.min(idx.len());
    let mx = logits[idx[0] as usize];
    let mut w = Vec::with_capacity(k);
    let mut sum = 0f32;
    for &i in &idx[..k] {
        let e = ((logits[i as usize] - mx) / temp).exp();
        w.push(e);
        sum += e;
    }
    let mut r = (rand_u64() as f64 / u64::MAX as f64) as f32 * sum;
    for (j, &e) in w.iter().enumerate() {
        r -= e;
        if r <= 0.0 { return idx[j]; }
    }
    idx[k - 1]
}

fn rand_u64() -> u64 {
    use std::sync::atomic::{AtomicU64, Ordering};
    static S: AtomicU64 = AtomicU64::new(0x9E3779B97F4A7C15);
    let mut x = S.load(Ordering::Relaxed);
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    S.store(x, Ordering::Relaxed);
    x
}
