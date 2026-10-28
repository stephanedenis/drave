//! Exécution native d'un `drave-n0` DRVM : les tenseurs sont lus dans le
//! conteneur, sans GGUF intermédiaire. C'est volontairement simple (f32, une
//! séquence, pas de cache KV) : le but est de prouver que le format natif
//! s'exécute, pas d'être rapide.

use std::collections::HashMap;

use crate::drvm::{Drvm, ErreurDrvm, Json};

#[derive(Debug, Clone)]
pub struct Cfg {
    pub vocab: usize,
    pub d: usize,
    pub n_blocks: usize,
    pub n_heads: usize,
    pub expert_hidden: usize,
    pub n_experts: usize,
    pub top_k: usize,
    pub kwta: f64,
    pub window: usize,
    pub thought_steps: usize,
}

fn champ<'a>(j: &'a Json, k: &str) -> Result<&'a Json, ErreurDrvm> {
    j.get(k).ok_or_else(|| ErreurDrvm(format!("architecture.{k} absent")))
}

fn u(j: &Json, k: &str) -> Result<usize, ErreurDrvm> {
    champ(j, k)?.as_u64().map(|x| x as usize).ok_or_else(|| ErreurDrvm(format!("architecture.{k} non entier")))
}

pub struct Native {
    cfg: Cfg,
    poids: HashMap<String, Vec<f32>>,
}

impl Native {
    pub fn open(d: &Drvm) -> Result<Self, ErreurDrvm> {
        let arch = d.manifeste.get("model").and_then(|m| m.get("architecture"))
            .ok_or_else(|| ErreurDrvm("model.architecture absent : DRVM non natif".into()))?;
        let cfg = Cfg {
            vocab: u(arch, "vocab")?, d: u(arch, "d_model")?, n_blocks: u(arch, "n_blocks")?,
            n_heads: u(arch, "n_heads")?, expert_hidden: u(arch, "expert_hidden")?,
            n_experts: u(arch, "n_experts")?, top_k: u(arch, "top_k")?,
            kwta: champ(arch, "kwta").ok().and_then(Json::as_f64).unwrap_or(0.25),
            window: u(arch, "window")?, thought_steps: u(arch, "thought_steps")?,
        };
        let mut poids = HashMap::new();
        for t in &d.tenseurs {
            let b = d.tenseur(&t.name).ok_or_else(|| ErreurDrvm(format!("tenseur absent : {}", t.name)))?;
            let mut v = Vec::with_capacity(b.len() / 4);
            for c in b.chunks_exact(4) {
                v.push(f32::from_le_bytes(c.try_into().unwrap()));
            }
            poids.insert(t.name.clone(), v);
        }
        Ok(Native { cfg, poids })
    }

    fn p(&self, n: &str) -> &[f32] {
        self.poids.get(n).unwrap_or_else(|| panic!("tenseur natif absent : {n}"))
    }

    fn matvec(&self, nom: &str, biais: &str, x: &[f32], o: usize) -> Vec<f32> {
        let w = self.p(nom); let bi = self.p(biais); let i = x.len();
        let mut y = vec![0.0f32; o];
        for r in 0..o {
            let mut s = bi[r];
            let base = r * i;
            for c in 0..i { s += w[base + c] * x[c]; }
            y[r] = s;
        }
        y
    }

    fn ln(&self, x: &[f32], nom: &str) -> Vec<f32> {
        let w = self.p(&format!("{nom}.weight")); let b = self.p(&format!("{nom}.bias"));
        let n = x.len() as f32; let m = x.iter().sum::<f32>() / n;
        let v = x.iter().map(|z| (z - m) * (z - m)).sum::<f32>() / n;
        let inv = 1.0 / (v + 1e-5).sqrt();
        (0..x.len()).map(|i| (x[i] - m) * inv * w[i] + b[i]).collect()
    }

    fn ffn(&self, x: &[f32], b: usize) -> Vec<f32> {
        let c = &self.cfg;
        let rout = self.matvec(&format!("blocks.{b}.ffn.router.weight"),
                              &format!("blocks.{b}.ffn.router.bias"), x, c.n_experts);
        let mut idx: Vec<usize> = (0..c.n_experts).collect();
        idx.sort_by(|&a, &z| rout[z].partial_cmp(&rout[a]).unwrap());
        idx.truncate(c.top_k);
        let mx = idx.iter().map(|&e| rout[e]).fold(f32::NEG_INFINITY, f32::max);
        let ex: Vec<f32> = idx.iter().map(|&e| (rout[e] - mx).exp()).collect();
        let se: f32 = ex.iter().sum();
        let g = self.matvec(&format!("blocks.{b}.ffn.gate.weight"),
                            &format!("blocks.{b}.ffn.gate.bias"), x, c.n_experts * c.expert_hidden);
        let u = self.matvec(&format!("blocks.{b}.ffn.up.weight"),
                            &format!("blocks.{b}.ffn.up.bias"), x, c.n_experts * c.expert_hidden);
        let mut h = vec![0.0f32; c.n_experts * c.expert_hidden];
        let k = ((c.expert_hidden as f64 * c.kwta).round() as usize).max(1);
        for (j, &e) in idx.iter().enumerate() {
            let base = e * c.expert_hidden;
            let mut v = vec![0.0f32; c.expert_hidden];
            for q in 0..c.expert_hidden {
                let z = g[base + q];
                v[q] = (z / (1.0 + (-z).exp())) * u[base + q];
            }
            let mut ord: Vec<usize> = (0..c.expert_hidden).collect();
            ord.sort_by(|&a, &z| v[z].partial_cmp(&v[a]).unwrap());
            let seuil = v[ord[k - 1]];
            for q in 0..c.expert_hidden {
                // Le modèle Python calcule les poids du routeur mais ne les
                // applique PAS à h (ils ne servent qu'au top-k). Les multiplier
                // ici créait l'écart de 0,88 sur les logits.
                if v[q] >= seuil { h[base + q] = v[q]; }
            }
        }
        self.matvec(&format!("blocks.{b}.ffn.down.weight"),
                    &format!("blocks.{b}.ffn.down.bias"), &h, c.d)
    }

    pub fn forward(&self, ids: &[u32]) -> Vec<f32> {
        let c = &self.cfg;
        let mut x = vec![0.0f32; c.d];
        for (pos, &id) in ids.iter().enumerate() {
            let e = self.p("embed.weight"); let pe = self.p("pos.weight");
            for k in 0..c.d { x[k] = e[id as usize * c.d + k] + pe[pos.min(2047) * c.d + k]; }
        }
        // Pour cette version, on exécute la dernière position seulement, avec
        // les positions précédentes comme contexte.
        let s = ids.len();
        let mut h = vec![vec![0.0f32; c.d]; s];
        for (pos, &id) in ids.iter().enumerate() {
            let e = self.p("embed.weight"); let pe = self.p("pos.weight");
            for k in 0..c.d { h[pos][k] = e[id as usize * c.d + k] + pe[pos.min(2047) * c.d + k]; }
        }
        for b in 0..c.n_blocks {
            let mut nh = vec![vec![0.0f32; c.d]; s];
            // q/k/v de TOUTES les positions : l'attention d'une position lit les
            // précédentes. Calculer le qkv dans la boucle de position ne donnait
            // que le jeton courant (range out of bounds, attrapé).
            let qkv_all: Vec<Vec<f32>> = (0..s).map(|pos| {
                let z = self.ln(&h[pos], &format!("blocks.{b}.ln1"));
                self.matvec(&format!("blocks.{b}.qkv.weight"),
                            &format!("blocks.{b}.qkv.bias"), &z, 3 * c.d)
            }).collect();
            for pos in 0..s {
                let qkv = &qkv_all[pos];
                let dh = c.d / c.n_heads;
                let mut att = vec![0.0f32; c.d];
                for t in 0..c.n_heads {
                    let q = &qkv[t * dh..(t + 1) * dh];
                    let mut sc = Vec::new(); let mut js = Vec::new();
                    for j in (0..=pos).rev() {
                        if pos - j >= c.window { break; }
                        let k = &qkv_all[j][c.d + t * dh..c.d + (t + 1) * dh];
                        let mut d = 0.0f32;
                        for qq in 0..dh { d += q[qq] * k[qq]; }
                        sc.push(d / (dh as f32).sqrt()); js.push(j);
                    }
                    let mx = sc.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
                    let ex: Vec<f32> = sc.iter().map(|v| (v - mx).exp()).collect();
                    let se: f32 = ex.iter().sum();
                    for (jj, &j) in js.iter().enumerate() {
                        let v = &qkv_all[j][2 * c.d + t * dh..2 * c.d + (t + 1) * dh];
                        for qq in 0..dh { att[t * dh + qq] += ex[jj] / se * v[qq]; }
                    }
                }
                let y = self.matvec(&format!("blocks.{b}.out.weight"),
                                    &format!("blocks.{b}.out.bias"), &att, c.d);
                let z2 = self.ln(&(0..c.d).map(|k| h[pos][k] + y[k]).collect::<Vec<_>>(),
                                 &format!("blocks.{b}.ln2"));
                let f = self.ffn(&z2, b);
                for k in 0..c.d { nh[pos][k] = h[pos][k] + y[k] + f[k]; }
            }
            h = nh;
            if b == c.n_blocks / 2 - 1 {
                for pos in 0..s {
                    let br = self.matvec("bridge.weight", "bridge.bias", &h[pos], c.d);
                    for k in 0..c.d { h[pos][k] += br[k]; }
                }
            }
        }
        let mut out = vec![0.0f32; c.d];
        for pos in 0..s {
            let mut z = h[pos].clone();
            let h0 = z.clone();
            for _ in 0..c.thought_steps {
                let a = self.matvec("thought.weight", "thought.bias", &z, c.d);
                let b = self.matvec("thought_in.weight", "thought_in.bias", &h0, c.d);
                for k in 0..c.d { z[k] = (a[k] + b[k]).tanh(); }
            }
            out = z;
        }
        self.matvec("head_byte.weight", "head_byte.bias", &out, c.vocab)
    }
}
