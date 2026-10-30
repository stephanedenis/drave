//! Exécution native d'un `drave-n0` DRVM : les tenseurs sont lus dans le
//! conteneur, sans GGUF intermédiaire. C'est volontairement simple (f32, une
//! séquence, pas de cache KV) : le but est de prouver que le format natif
//! s'exécute, pas d'être rapide.

use std::collections::HashMap;
use std::sync::atomic::{AtomicUsize, Ordering};

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
    /// Nombre de positions du tenseur `pos.weight` (lu au chargement, plus de 2047 en dur).
    pub max_pos: usize,
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
    // N3.3c — compteurs de sparsité réelle, remis à zéro à chaque chargement.
    appels_ffn: AtomicUsize,
    experts_actifs: AtomicUsize,
    canaux_actifs: AtomicUsize,
}

impl Native {
    pub fn open(d: &Drvm) -> Result<Self, ErreurDrvm> {
        let arch = d.manifeste.get("model").and_then(|m| m.get("architecture"))
            .ok_or_else(|| ErreurDrvm("model.architecture absent : DRVM non natif".into()))?;
        let mut cfg = Cfg {
            vocab: u(arch, "vocab")?, d: u(arch, "d_model")?, n_blocks: u(arch, "n_blocks")?,
            n_heads: u(arch, "n_heads")?, expert_hidden: u(arch, "expert_hidden")?,
            n_experts: u(arch, "n_experts")?, top_k: u(arch, "top_k")?,
            kwta: champ(arch, "kwta").ok().and_then(Json::as_f64).unwrap_or(0.25),
            window: u(arch, "window")?, thought_steps: u(arch, "thought_steps")?,
            max_pos: 0,
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
        cfg.max_pos = poids.get("pos.weight").map(|p| p.len() / cfg.d).unwrap_or(2048).max(1);
        Ok(Native { cfg, poids, appels_ffn: AtomicUsize::new(0),
                    experts_actifs: AtomicUsize::new(0), canaux_actifs: AtomicUsize::new(0) })
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
        self.appels_ffn.fetch_add(1, Ordering::Relaxed);
        let rout = self.matvec(&format!("blocks.{b}.ffn.router.weight"),
                              &format!("blocks.{b}.ffn.router.bias"), x, c.n_experts);
        let mut idx: Vec<usize> = (0..c.n_experts).collect();
        idx.sort_by(|&a, &z| rout[z].partial_cmp(&rout[a]).unwrap());
        idx.truncate(c.top_k);
        self.experts_actifs.fetch_add(idx.len(), Ordering::Relaxed);
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
            let mut actifs = 0usize;
            for q in 0..c.expert_hidden {
                // Le modèle Python calcule les poids du routeur mais ne les
                // applique PAS à h (ils ne servent qu'au top-k). Les multiplier
                // ici créait l'écart de 0,88 sur les logits.
                if v[q] >= seuil { h[base + q] = v[q]; actifs += 1; }
            }
            self.canaux_actifs.fetch_add(actifs, Ordering::Relaxed);
        }
        self.matvec(&format!("blocks.{b}.ffn.down.weight"),
                    &format!("blocks.{b}.ffn.down.bias"), &h, c.d)
    }

    pub fn forward(&self, ids: &[u32]) -> Vec<f32> {
        let c = &self.cfg;
        let mut x = vec![0.0f32; c.d];
        for (pos, &id) in ids.iter().enumerate() {
            let e = self.p("embed.weight"); let pe = self.p("pos.weight");
            for k in 0..c.d { x[k] = e[id as usize * c.d + k] + pe[pos.min(c.max_pos.saturating_sub(1)) * c.d + k]; }
        }
        // Pour cette version, on exécute la dernière position seulement, avec
        // les positions précédentes comme contexte.
        let s = ids.len();
        let mut h = vec![vec![0.0f32; c.d]; s];
        for (pos, &id) in ids.iter().enumerate() {
            let e = self.p("embed.weight"); let pe = self.p("pos.weight");
            for k in 0..c.d { h[pos][k] = e[id as usize * c.d + k] + pe[pos.min(c.max_pos.saturating_sub(1)) * c.d + k]; }
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
            if c.n_blocks >= 2 && b == c.n_blocks / 2 - 1 {
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

#[derive(Default)]
pub struct Cache {
    k: Vec<Vec<Vec<f32>>>,
    v: Vec<Vec<Vec<f32>>>,
}

impl Cache {
    fn assurer(&mut self, n_blocks: usize, n_heads: usize) {
        if self.k.is_empty() {
            self.k = vec![vec![Vec::new(); n_heads]; n_blocks];
            self.v = vec![vec![Vec::new(); n_heads]; n_blocks];
        }
    }
}

impl Native {
    /// Un jeton, avec cache KV : les clés/valeurs des positions précédentes ne
    /// sont pas recalculées. C'est le chemin de génération.
    pub fn pas(&self, id: u32, pos: usize, cache: &mut Cache) -> Vec<f32> {
        let env = std::env::var("DRAVE_NATIVE_PROFONDEUR").ok()
            .and_then(|v| v.parse::<usize>().ok())
            .unwrap_or(self.cfg.n_blocks)
            .clamp(1, self.cfg.n_blocks);
        self.pas_profondeur(id, pos, cache, env)
    }

    /// Entrée d'une région : embedding + position. Seul endroit qui lit
    /// `embed.weight` et `pos.weight` ; la région aval ne ré-embedde jamais.
    fn entree(&self, id: u32, pos: usize) -> Vec<f32> {
        let c = &self.cfg;
        let e = self.p("embed.weight"); let pe = self.p("pos.weight");
        let mut x = vec![0.0f32; c.d];
        for k in 0..c.d {
            x[k] = e[id as usize * c.d + k] + pe[pos.min(c.max_pos.saturating_sub(1)) * c.d + k];
        }
        x
    }

    /// Traverse les blocs `blocs` (indices ABSOLUS) en écrivant K/V dans
    /// `cache[b]`. Ni embedding, ni tête. Le pont est appliqué à l'indice
    /// absolu : une seule des deux régions le porte.
    fn traverser(&self, x: &mut [f32], pos: usize, blocs: std::ops::Range<usize>, cache: &mut Cache) {
        let c = &self.cfg;
        let dh = c.d / c.n_heads;
        cache.assurer(c.n_blocks, c.n_heads);
        for b in blocs {
            let z = self.ln(x, &format!("blocks.{b}.ln1"));
            let qkv = self.matvec(&format!("blocks.{b}.qkv.weight"),
                                  &format!("blocks.{b}.qkv.bias"), &z, 3 * c.d);
            let mut att = vec![0.0f32; c.d];
            for t in 0..c.n_heads {
                let q = &qkv[t * dh..(t + 1) * dh];
                cache.k[b][t].extend_from_slice(&qkv[c.d + t * dh..c.d + (t + 1) * dh]);
                cache.v[b][t].extend_from_slice(&qkv[2 * c.d + t * dh..2 * c.d + (t + 1) * dh]);
                let debut = pos.saturating_sub(c.window - 1);
                let mut sc = Vec::new();
                for j in debut..=pos {
                    let k = &cache.k[b][t][j * dh..(j + 1) * dh];
                    let mut d = 0.0f32;
                    for qq in 0..dh { d += q[qq] * k[qq]; }
                    sc.push(d / (dh as f32).sqrt());
                }
                let mx = sc.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
                let ex: Vec<f32> = sc.iter().map(|v| (v - mx).exp()).collect();
                let se: f32 = ex.iter().sum();
                for (jj, j) in (debut..=pos).enumerate() {
                    let v = &cache.v[b][t][j * dh..(j + 1) * dh];
                    for qq in 0..dh { att[t * dh + qq] += ex[jj] / se * v[qq]; }
                }
            }
            let y = self.matvec(&format!("blocks.{b}.out.weight"),
                                &format!("blocks.{b}.out.bias"), &att, c.d);
            let z2 = self.ln(&(0..c.d).map(|k| x[k] + y[k]).collect::<Vec<_>>(),
                             &format!("blocks.{b}.ln2"));
            let f = self.ffn(&z2, b);
            for k in 0..c.d { x[k] = x[k] + y[k] + f[k]; }
            if c.n_blocks >= 2 && b == c.n_blocks / 2 - 1 {
                let br = self.matvec("bridge.weight", "bridge.bias", x, c.d);
                for k in 0..c.d { x[k] += br[k]; }
            }
        }
    }

    /// Tête terminale : thought_steps puis head_byte. Une seule fois, dans la
    /// dernière région.
    fn tete(&self, x: &[f32]) -> Vec<f32> {
        let c = &self.cfg;
        let mut z = x.to_vec();
        let h0 = x.to_vec();
        for _ in 0..c.thought_steps {
            let a = self.matvec("thought.weight", "thought.bias", &z, c.d);
            let b = self.matvec("thought_in.weight", "thought_in.bias", &h0, c.d);
            for k in 0..c.d { z[k] = (a[k] + b[k]).tanh(); }
        }
        self.matvec("head_byte.weight", "head_byte.bias", &z, c.vocab)
    }

    /// N3.2b0 — un pas à profondeur imposée ; N3.2b1 l'utilise pour les deux caches.
    fn pas_profondeur(&self, id: u32, pos: usize, cache: &mut Cache, profondeur: usize) -> Vec<f32> {
        let p = profondeur.clamp(1, self.cfg.n_blocks);
        let mut x = self.entree(id, pos);
        self.traverser(&mut x, pos, 0..p, cache);
        self.tete(&x)
    }

    /// Région AMONT : blocs `0..k`, hidden de frontière. `k == 0` est légitime.
    pub fn pas_amont(&self, id: u32, pos: usize, cache: &mut Cache, k: usize) -> Vec<f32> {
        let k = k.min(self.cfg.n_blocks);
        let mut x = self.entree(id, pos);
        self.traverser(&mut x, pos, 0..k, cache);
        x
    }

    /// Région AVAL : blocs `k..n`, puis tête. La frontière a déjà traversé k blocs.
    pub fn pas_aval(&self, frontiere: &[f32], pos: usize, cache: &mut Cache, k: usize) -> Vec<f32> {
        let k = k.min(self.cfg.n_blocks);
        let mut x = frontiere.to_vec();
        self.traverser(&mut x, pos, k..self.cfg.n_blocks, cache);
        self.tete(&x)
    }

    /// Génération SANS cache : refait toute la passe avant à chaque octet.
    /// Sert de témoin pour mesurer le gain du cache.
    pub fn generer_complet(&self, prompt: &[u8], n: usize) -> Vec<u8> {
        let mut ids: Vec<u8> = prompt.to_vec();
        for _ in 0..n {
            let u: Vec<u32> = ids.iter().map(|&b| b as u32).collect();
            let logits = self.forward(&u);
            let suivant = logits.iter().enumerate()
                .max_by(|a, b| a.1.partial_cmp(b.1).unwrap()).map(|(i, _)| i as u8).unwrap_or(32);
            ids.push(suivant);
            if suivant == b'\n' { break; }
        }
        ids
    }

    /// Perplexité d'un texte octet, avec cache KV. Chaque position est notée
    /// une seule fois ; le cache évite la passe O(s²).
    pub fn perplexite(&self, octets: &[u8]) -> (f64, usize) {
        let mut cache = Cache::default();
        let mut somme = 0.0f64;
        for pos in 0..octets.len().saturating_sub(1) {
            let logits = self.pas(octets[pos] as u32, pos, &mut cache);
            let mx = logits.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
            let se: f32 = logits.iter().map(|v| (v - mx).exp()).sum();
            let cible = octets[pos + 1] as usize;
            let lp = (logits[cible] - mx) - se.ln();
            somme -= lp as f64;
        }
        let n = octets.len().saturating_sub(1);
        ((somme / n.max(1) as f64).exp(), n)
    }

    pub fn generer(&self, prompt: &[u8], n: usize) -> Vec<u8> {
        let mut cache = Cache::default();
        let mut ids: Vec<u8> = prompt.to_vec();
        let mut logits = vec![0.0f32; self.cfg.vocab];
        for (pos, &id) in ids.clone().iter().enumerate() {
            logits = self.pas(id as u32, pos, &mut cache);
        }
        for _ in 0..n {
            let suivant = logits.iter().enumerate()
                .max_by(|a, b| a.1.partial_cmp(b.1).unwrap()).map(|(i, _)| i as u8).unwrap_or(32);
            ids.push(suivant);
            let pos = ids.len() - 1;
            logits = self.pas(suivant as u32, pos, &mut cache);
            if suivant == b'\n' { break; }
        }
        ids
    }

    /// N3.2b1 — décision à seuil : pour chaque jeton, calcule le chemin court et le
    /// chemin plein, garde le jeton du court si sa confiance (softmax max) atteint le
    /// seuil, sinon celui du plein. Les deux caches sont entretenus : aucun saut de
    /// calcul (le court ET le plein sont calculés) ; la porte mesure la DÉCISION.
    pub fn generer_seuil(&self, prompt: &[u8], n: usize, profondeur: usize, seuil: f32)
        -> (Vec<u8>, usize, usize) {
        let profondeur = profondeur.clamp(1, self.cfg.n_blocks.saturating_sub(1).max(1));
        let mut ce = Cache::default();
        let mut cf = Cache::default();
        let mut ids: Vec<u8> = prompt.to_vec();
        let mut logits_e = vec![0.0f32; self.cfg.vocab];
        let mut logits_f = vec![0.0f32; self.cfg.vocab];
        for (pos, &id) in ids.clone().iter().enumerate() {
            logits_e = self.pas_profondeur(id as u32, pos, &mut ce, profondeur);
            logits_f = self.pas_profondeur(id as u32, pos, &mut cf, self.cfg.n_blocks);
        }
        let (mut anticipe, mut complet) = (0usize, 0usize);
        for _ in 0..n {
            let (ie, ce_max) = argmax_conf(&logits_e);
            let (ifull, _) = argmax_conf(&logits_f);
            let suivant = if ce_max >= seuil {
                anticipe += 1; ie
            } else {
                complet += 1; ifull
            };
            ids.push(suivant);
            let pos = ids.len() - 1;
            logits_e = self.pas_profondeur(suivant as u32, pos, &mut ce, profondeur);
            logits_f = self.pas_profondeur(suivant as u32, pos, &mut cf, self.cfg.n_blocks);
            if suivant == b'\n' { break; }
        }
        (ids, anticipe, complet)
    }
}

fn argmax_conf(logits: &[f32]) -> (u8, f32) {
    let mx = logits.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
    let se: f32 = logits.iter().map(|v| (v - mx).exp()).sum();
    let (i, _) = logits.iter().enumerate()
        .max_by(|a, b| a.1.partial_cmp(b.1).unwrap()).unwrap_or((0, &0.0));
    (i as u8, 1.0 / se.max(1e-30))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn execute_une_petite_fixture_drvm() {
        let chemin = concat!(env!("CARGO_MANIFEST_DIR"), "/tests/fixtures/tiny_n0.drvm");
        let d = Drvm::open(chemin).expect("fixture DRVM");
        let n = Native::open(&d).expect("ouverture native");
        let l = n.forward(&[65, 66, 67]);
        assert_eq!(l.len(), 256);
        assert!(l.iter().all(|x| x.is_finite()), "logits non finis");
        let g = n.generer(b"AB", 4);
        assert!(g.len() >= 6);
    }

    #[test]
    fn split_amont_aval_egal_pas() {
        let chemin = concat!(env!("CARGO_MANIFEST_DIR"), "/tests/fixtures/tiny_n0.drvm");
        let d = Drvm::open(chemin).expect("fixture DRVM");
        let n = Native::open(&d).expect("ouverture native");
        for k in 0..=n.cfg.n_blocks {
            let (mut ca, mut cv, mut cp) = (Cache::default(), Cache::default(), Cache::default());
            for pos in 0..6usize {
                let id = b"abcdef"[pos] as u32;
                let attendu = n.pas(id, pos, &mut cp);
                let h = n.pas_amont(id, pos, &mut ca, k);
                let got = n.pas_aval(&h, pos, &mut cv, k);
                assert_eq!(attendu, got, "k={k} pos={pos}");
            }
        }
    }
}

/// Service HTTP minimal, std seul : `GET /sante`, `POST /generer` (corps = prompt,
/// `?n=32`). Le cache KV est recréé par requête ; le modèle reste chargé.
pub fn servir(chemin: &str, port: u16) -> std::io::Result<()> {
    use std::io::{Read, Write};
    use std::net::TcpListener;
    let d = crate::drvm::Drvm::open(chemin).map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidData, e.to_string()))?;
    let n = Native::open(&d).map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidData, e.to_string()))?;
    let l = TcpListener::bind(("127.0.0.1", port))?;
    eprintln!("[drvm-serve] http://127.0.0.1:{port} · 11 M natif, cache par requête");
    for flux in l.incoming() {
        let mut s = match flux { Ok(s) => s, Err(_) => continue };
        // N3.2b0 — lire la requête ENTIÈRE, pas un seul `read` : le corps peut arriver
        // dans un second segment TCP. Le service perdait alors le prompt (corps vide)
        // et la même requête donnait une génération différente — mesuré par la porte
        // N3.2b0 avant ce correctif.
        let mut buf: Vec<u8> = Vec::new();
        let mut tmp = [0u8; 8192];
        loop {
            match s.read(&mut tmp) {
                Ok(0) => break,
                Ok(n) => buf.extend_from_slice(&tmp[..n]),
                Err(_) => break,
            }
            if buf.len() > 64 * 1024 { break; }
            let texte = String::from_utf8_lossy(&buf);
            if let Some(p) = texte.find("\r\n\r\n") {
                let cl = texte[..p].lines()
                    .find_map(|l| l.to_ascii_lowercase().strip_prefix("content-length:")
                        .and_then(|v| v.trim().parse::<usize>().ok()))
                    .unwrap_or(0);
                if buf.len() >= p + 4 + cl { break; }
            }
        }
        let req = String::from_utf8_lossy(&buf);
        let ligne = req.lines().next().unwrap_or("");
        let auth_ok = std::env::var("DRAVE_TOKEN").ok().map(|t| req.contains(&format!("Authorization: Bearer {t}")))
            .unwrap_or(true);
        let (code, corps) = if !auth_ok {
            (401, "{\"erreur\":\"jeton requis\"}".to_string())
        } else if ligne.starts_with("GET /sante") {
            (200, format!("{{\"ok\":true,\"parametres\":{}}}", n.nb_parametres()))
        } else if ligne.starts_with("POST /generer") {
            let n_max: usize = ligne.split("n=").nth(1).and_then(|x| x.split(|c: char| !c.is_ascii_digit()).next()).and_then(|x| x.parse().ok()).unwrap_or(32).min(256);
            let corps = req.split("\r\n\r\n").nth(1).unwrap_or("");
            let seuil = ligne.split("seuil=").nth(1).and_then(|x| x.split(|c: char| c == '&' || c.is_whitespace()).next()).and_then(|x| x.parse::<f32>().ok());
            let profondeur = ligne.split("profondeur=").nth(1).and_then(|x| x.split(|c: char| c == '&' || c.is_whitespace()).next()).and_then(|x| x.parse::<usize>().ok());
            let t = std::time::Instant::now();
            let (b, anticipe, complet) = match (seuil, profondeur) {
                (Some(s), Some(p)) => n.generer_seuil(corps.as_bytes(), n_max, p, s),
                _ => (n.generer(corps.as_bytes(), n_max), 0, 0),
            };
            let texte = String::from_utf8_lossy(&b).replace('\\', "\\\\").replace('"', "\\\"");
            (200, format!("{{\"octets\":{},\"ms\":{:.1},\"choix_anticipe\":{},\"choix_complet\":{},\"texte\":\"{}\"}}",
                          b.len(), t.elapsed().as_secs_f64() * 1000.0, anticipe, complet, texte.replace('\n', "\\n")))
        } else { (404, "{\"erreur\":\"chemin inconnu\"}".to_string()) };
        let rep = format!("HTTP/1.1 {code} OK\r\nContent-Type: application/json\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{corps}", corps.len());
        let _ = s.write_all(rep.as_bytes());
    }
    Ok(())
}

impl Native {
    pub fn nb_parametres(&self) -> usize { self.poids.values().map(|v| v.len()).sum() }

    pub fn cfg_n_blocks(&self) -> usize { self.cfg.n_blocks }
    pub fn cfg_d(&self) -> usize { self.cfg.d }
    pub fn vocab_size(&self) -> usize { self.cfg.vocab }

    /// N3.3c — compteurs réels : (appels ffn, experts retenus, canaux actifs).
    pub fn sparsite(&self) -> (usize, usize, usize) {
        (self.appels_ffn.load(Ordering::Relaxed),
         self.experts_actifs.load(Ordering::Relaxed),
         self.canaux_actifs.load(Ordering::Relaxed))
    }

}
