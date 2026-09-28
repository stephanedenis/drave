//! Lecteur GGUF minimal (std seul).
//!
#![allow(dead_code)] // lecteur générique : tous les formats ne servent pas au moteur

//! Ne lit que ce dont le moteur a besoin : métadonnées, descripteurs de tenseurs,
//! et les niveaux quantifiés (Q8_0 / Q4_0) ou les flottants (F32 / F16).

use std::collections::HashMap;
use std::fs::File;
use std::io::Read;
use std::path::Path;

#[derive(Debug, Clone)]
pub enum Meta {
    U8(u8), I8(i8), U16(u16), I16(i16), U32(u32), I32(i32),
    F32(f32), Bool(bool), Str(String), Array(Vec<Meta>), U64(u64), I64(i64), F64(f64),
}

impl Meta {
    pub fn as_u64(&self) -> Option<u64> {
        match self {
            Meta::U32(v) => Some(*v as u64),
            Meta::U64(v) => Some(*v),
            Meta::I32(v) => Some(*v as u64),
            Meta::I64(v) => Some(*v as u64),
            _ => None,
        }
    }
    pub fn as_f64(&self) -> Option<f64> {
        match self {
            Meta::F32(v) => Some(*v as f64),
            Meta::F64(v) => Some(*v),
            _ => None,
        }
    }
    pub fn as_str(&self) -> Option<&str> {
        match self { Meta::Str(s) => Some(s), _ => None }
    }
}

#[derive(Debug, Clone)]
pub struct TensorInfo {
    pub name: String,
    pub dims: Vec<u64>,     // en convention numpy (le plus lent d'abord)
    pub ttype: u32,
    pub offset: u64,
}

impl TensorInfo {
    pub fn nelem(&self) -> usize { self.dims.iter().product::<u64>() as usize }
}

pub const GGML_F32: u32 = 0;
pub const GGML_F16: u32 = 1;
pub const GGML_Q4_0: u32 = 2;
pub const GGML_MXFP4: u32 = 39;
pub const GGML_Q4_K: u32 = 12;
pub const GGML_Q6_K: u32 = 14;

/// Octets par super-bloc : Q4_K = 2+2+12+128 (256 poids), Q6_K = 128+64+16+2.
pub const TAILLE_Q4K: usize = 144;
pub const TAILLE_Q6K: usize = 210;

/// Échelles et minima d'un sous-bloc Q4_K : huit paires de 6 bits tassées dans
/// douze octets. Les quatre premières paires sont dans les octets 0–7, les
/// quatre suivantes dans les octets 8–11, leurs deux bits hauts repris des
/// octets 0–7 — c'est le dépaquetage de `get_scale_min_k4` de ggml.
#[inline]
pub fn echelle_min_q4k(scales: &[u8], j: usize) -> (u8, u8) {
    if j < 4 {
        (scales[j] & 63, scales[j + 4] & 63)
    } else {
        ((scales[j + 4] & 0x0F) | ((scales[j - 4] >> 6) << 4),
         (scales[j + 4] >> 4) | ((scales[j] >> 6) << 4))
    }
}
pub const GGML_Q4_1: u32 = 3;
pub const GGML_Q8_0: u32 = 8;

/// Pointeur pré-résolu vers les lignes d'un tenseur quantifié (Q8_0 ou Q4_0).
pub struct Q8View {
    pub base: usize,
    pub n_cols: usize,
    pub nb: usize,
    pub q4: bool,
    /// Type ggml d'origine : la tête de sortie peut être Q8_0, Q4_0 ou Q4_K
    /// selon le modèle, et se lit **en place** dans les trois cas.
    pub ttype: u32,
}

pub struct Gguf {
    pub meta: HashMap<String, Meta>,
    pub tensors: Vec<TensorInfo>,
    buf: Vec<u8>,
    data_start: usize,
}

struct Cur<'a> { b: &'a [u8], p: usize }

impl<'a> Cur<'a> {
    fn u8(&mut self) -> u8 { let v = self.b[self.p]; self.p += 1; v }
    fn u32(&mut self) -> u32 { let v = u32::from_le_bytes(self.b[self.p..self.p+4].try_into().unwrap()); self.p += 4; v }
    fn u64(&mut self) -> u64 { let v = u64::from_le_bytes(self.b[self.p..self.p+8].try_into().unwrap()); self.p += 8; v }
    fn i8(&mut self) -> i8 { let v = self.b[self.p] as i8; self.p += 1; v }
    fn u16(&mut self) -> u16 { let v = u16::from_le_bytes(self.b[self.p..self.p+2].try_into().unwrap()); self.p += 2; v }
    fn i16(&mut self) -> i16 { let v = i16::from_le_bytes(self.b[self.p..self.p+2].try_into().unwrap()); self.p += 2; v }
    fn i32(&mut self) -> i32 { let v = i32::from_le_bytes(self.b[self.p..self.p+4].try_into().unwrap()); self.p += 4; v }
    fn f32(&mut self) -> f32 { let v = f32::from_le_bytes(self.b[self.p..self.p+4].try_into().unwrap()); self.p += 4; v }
    fn f64(&mut self) -> f64 { let v = f64::from_le_bytes(self.b[self.p..self.p+8].try_into().unwrap()); self.p += 8; v }
    fn i64(&mut self) -> i64 { let v = i64::from_le_bytes(self.b[self.p..self.p+8].try_into().unwrap()); self.p += 8; v }
    fn string(&mut self) -> String {
        let n = self.u64() as usize;
        let s = String::from_utf8_lossy(&self.b[self.p..self.p + n]).to_string();
        self.p += n;
        s
    }
    fn value(&mut self, vt: u32) -> Meta {
        match vt {
            0 => Meta::U8(self.u8()),
            1 => Meta::I8(self.i8()),
            2 => Meta::U16(self.u16()),
            3 => Meta::I16(self.i16()),
            4 => Meta::U32(self.u32()),
            5 => Meta::I32(self.i32()),
            6 => Meta::F32(self.f32()),
            7 => Meta::Bool(self.u8() != 0),   // 1 octet, pas 4 !
            8 => Meta::Str(self.string()),
            9 => {
                let et = self.u32();
                let n = self.u64() as usize;
                Meta::Array((0..n).map(|_| self.value(et)).collect())
            }
            10 => Meta::U64(self.u64()),
            11 => Meta::I64(self.i64()),
            12 => Meta::F64(self.f64()),
            _ => panic!("type de métadonnée inconnu : {vt}"),
        }
    }
}

impl Gguf {
    pub fn open<P: AsRef<Path>>(path: P) -> std::io::Result<Self> {
        let mut buf = Vec::new();
        File::open(path)?.read_to_end(&mut buf)?;
        assert_eq!(&buf[0..4], b"GGUF", "ce n'est pas un fichier GGUF");
        let mut c = Cur { b: &buf, p: 4 };
        let version = c.u32();
        assert!(version >= 2, "version GGUF {version} non gérée");
        let n_tensors = c.u64() as usize;
        let n_kv = c.u64() as usize;

        let mut meta = HashMap::new();
        for _ in 0..n_kv {
            let k = c.string();
            let vt = c.u32();
            meta.insert(k, c.value(vt));
        }
        let mut tensors = Vec::with_capacity(n_tensors);
        for _ in 0..n_tensors {
            let name = c.string();
            let nd = c.u32() as usize;
            let mut dims: Vec<u64> = (0..nd).map(|_| c.u64()).collect();
            dims.reverse();                       // ggml stocke à l'envers
            let ttype = c.u32();
            let offset = c.u64();
            tensors.push(TensorInfo { name, dims, ttype, offset });
        }
        let align = meta.get("general.alignment").and_then(|m| m.as_u64()).unwrap_or(32) as usize;
        let data_start = (c.p + align - 1) / align * align;
        Ok(Gguf { meta, tensors, buf, data_start })
    }

    pub fn cfg(&self, key: &str) -> Option<&Meta> {
        let arch = self.meta.get("general.architecture")?.as_str()?;
        self.meta.get(&format!("{arch}.{key}"))
    }

    pub fn tensor(&self, name: &str) -> Option<&TensorInfo> {
        self.tensors.iter().find(|t| t.name == name)
    }

    pub fn f16_to_f32(h: u16) -> f32 {
        let sign = ((h >> 15) & 1) as u32;
        let exp = ((h >> 10) & 0x1F) as u32;
        let man = (h & 0x3FF) as u32;
        let bits = if exp == 0 {
            if man == 0 { sign << 31 } else {
                // dénormal
                let mut e = 127 - 15 + 1;
                let mut m = man;
                while m & 0x400 == 0 { m <<= 1; e -= 1; }
                (sign << 31) | ((e as u32) << 23) | ((m & 0x3FF) << 13)
            }
        } else if exp == 31 {
            (sign << 31) | (0xFF << 23) | (man << 13)
        } else {
            (sign << 31) | ((exp + 127 - 15) << 23) | (man << 13)
        };
        f32::from_bits(bits)
    }

    /// Niveaux entiers bruts (avant mise à l'échelle) pour Q4_0 / Q8_0.
    pub fn raw_levels(&self, name: &str) -> Vec<i8> {
        let t = self.tensor(name).expect("tenseur absent");
        let base = self.data_start + t.offset as usize;
        let n = t.nelem();
        let mut out = Vec::with_capacity(n);
        match t.ttype {
            GGML_Q8_0 => {
                let nb = n / 32;
                for b in 0..nb {
                    let p = base + b * 34;
                    for j in 0..32 { out.push(self.buf[p + 2 + j] as i8); }
                }
            }
            GGML_Q4_0 => {
                let nb = n / 32;
                for b in 0..nb {
                    let p = base + b * 18;
                    for j in 0..16 {
                        let q = self.buf[p + 2 + j];
                        out.push(((q & 0x0F) as i16 - 8) as i8);
                    }
                    for j in 0..16 {
                        let q = self.buf[p + 2 + j];
                        out.push(((q >> 4) as i16 - 8) as i8);
                    }
                }
            }
            other => panic!("raw_levels : type {other} non géré"),
        }
        out
    }

    /// Déquantifie une ligne d'un tenseur 2D, en f32.
    pub fn row_f32(&self, name: &str, row: usize, n_cols: usize) -> Vec<f32> {
        let t = self.tensor(name).expect("tenseur absent");
        let base = self.data_start + t.offset as usize;
        let mut out = Vec::with_capacity(n_cols);
        match t.ttype {
            GGML_F32 => {
                let p = base + row * n_cols * 4;
                for i in 0..n_cols {
                    out.push(f32::from_le_bytes(self.buf[p + 4*i..p + 4*i + 4].try_into().unwrap()));
                }
            }
            GGML_F16 => {
                let p = base + row * n_cols * 2;
                for i in 0..n_cols {
                    out.push(Self::f16_to_f32(u16::from_le_bytes(self.buf[p + 2*i..p + 2*i + 2].try_into().unwrap())));
                }
            }
            GGML_Q8_0 => {
                let nb = n_cols / 32;
                for b in 0..nb {
                    let p = base + (row * nb + b) * 34;
                    let d = Self::f16_to_f32(u16::from_le_bytes(self.buf[p..p+2].try_into().unwrap()));
                    for j in 0..32 { out.push(d * (self.buf[p + 2 + j] as i8) as f32); }
                }
            }
            GGML_Q4_0 => {
                let nb = n_cols / 32;
                for b in 0..nb {
                    let p = base + (row * nb + b) * 18;
                    let d = Self::f16_to_f32(u16::from_le_bytes(self.buf[p..p+2].try_into().unwrap()));
                    for j in 0..16 { out.push(d * ((self.buf[p + 2 + j] & 0x0F) as i16 - 8) as f32); }
                    for j in 0..16 { out.push(d * ((self.buf[p + 2 + j] >> 4) as i16 - 8) as f32); }
                }
            }
            GGML_Q4_K => {
                let ns = n_cols / 256;
                for sup in 0..ns {
                    let p = base + (row * ns + sup) * TAILLE_Q4K;
                    let d = Self::f16_to_f32(u16::from_le_bytes(self.buf[p..p+2].try_into().unwrap()));
                    let dmin = Self::f16_to_f32(u16::from_le_bytes(self.buf[p+2..p+4].try_into().unwrap()));
                    let sc = &self.buf[p + 4..p + 16];
                    let qs = &self.buf[p + 16..p + 144];
                    for g in 0..4 {
                        let (s0, m0) = echelle_min_q4k(sc, 2 * g);
                        let (s1, m1) = echelle_min_q4k(sc, 2 * g + 1);
                        let (d0, n0) = (d * s0 as f32, dmin * m0 as f32);
                        let (d1, n1) = (d * s1 as f32, dmin * m1 as f32);
                        for l in 0..32 { out.push(d0 * (qs[g*32 + l] & 0x0F) as f32 - n0); }
                        for l in 0..32 { out.push(d1 * (qs[g*32 + l] >> 4) as f32 - n1); }
                    }
                }
            }
            GGML_Q6_K => {
                let ns = n_cols / 256;
                for sup in 0..ns {
                    let p = base + (row * ns + sup) * TAILLE_Q6K;
                    let ql = &self.buf[p..p + 128];
                    let qh = &self.buf[p + 128..p + 192];
                    let sc = &self.buf[p + 192..p + 208];
                    let d = Self::f16_to_f32(u16::from_le_bytes(self.buf[p+208..p+210].try_into().unwrap()));
                    for moitie in 0..2 {
                        let (ql, qh, sc) = (&ql[moitie*64..], &qh[moitie*32..], &sc[moitie*8..]);
                        let mut tmp = [0f32; 128];
                        for l in 0..32 {
                            let is = l / 16;
                            let q1 = ((ql[l] & 0x0F) | ((qh[l] & 3) << 4)) as i16 - 32;
                            let q2 = ((ql[l + 32] & 0x0F) | (((qh[l] >> 2) & 3) << 4)) as i16 - 32;
                            let q3 = ((ql[l] >> 4) | (((qh[l] >> 4) & 3) << 4)) as i16 - 32;
                            let q4 = ((ql[l + 32] >> 4) | (((qh[l] >> 6) & 3) << 4)) as i16 - 32;
                            let s = |k: usize| d * (sc[is + k] as i8) as f32;
                            tmp[l] = s(0) * q1 as f32;
                            tmp[l + 32] = s(2) * q2 as f32;
                            tmp[l + 64] = s(4) * q3 as f32;
                            tmp[l + 96] = s(6) * q4 as f32;
                        }
                        out.extend_from_slice(&tmp);
                    }
                }
            }
            GGML_Q4_1 => {
                let nb = n_cols / 32;
                for b in 0..nb {
                    let p = base + (row * nb + b) * 20;
                    let d = Self::f16_to_f32(u16::from_le_bytes(self.buf[p..p+2].try_into().unwrap()));
                    let m = Self::f16_to_f32(u16::from_le_bytes(self.buf[p+2..p+4].try_into().unwrap()));
                    for j in 0..16 { out.push(d * (self.buf[p + 4 + j] & 0x0F) as f32 + m); }
                    for j in 0..16 { out.push(d * (self.buf[p + 4 + j] >> 4) as f32 + m); }
                }
            }
            other => panic!("row_f32 : type {other} non géré"),
        }
        out
    }

    /// Vue pré-résolue sur un tenseur Q8_0 : évite de rechercher le tenseur
    /// (parcours linéaire des 290 descripteurs) à chaque ligne. La tête de
    /// sortie appelle cela 151 936 fois par token.
    pub fn q8_view(&self, name: &str) -> Q8View {
        let t = self.tensor(name).expect("tenseur absent");
        let q4 = match t.ttype {
            GGML_Q8_0 => false,
            GGML_Q4_0 => true,
            GGML_Q4_K | GGML_Q6_K => true,
            other => panic!("q8_view : type {other} non géré"),
        };
        let n_cols = t.dims[1] as usize;
        let bloc = if t.ttype == GGML_Q4_K || t.ttype == GGML_Q6_K { 256 } else { 32 };
        Q8View { base: self.data_start + t.offset as usize, n_cols, nb: n_cols / bloc,
                 q4, ttype: t.ttype }
    }

    /// Super-blocs **Q4_K** bruts : `(octets, nb de super-blocs de 256 poids par
    /// ligne)`. C'est le format de toute la famille Qwen/Llama en `Q4_K_M`.
    pub fn q4k_blocks(&self, name: &str) -> Option<(&[u8], usize)> {
        let t = self.tensor(name)?;
        if t.ttype != GGML_Q4_K { return None; }
        Some((&self.buf[self.data_start + t.offset as usize..], t.dims[1] as usize / 256))
    }

    /// Super-blocs **Q6_K** bruts (quelques tenseurs des mélanges `Q4_K_M`).
    pub fn q6k_blocks(&self, name: &str) -> Option<(&[u8], usize)> {
        let t = self.tensor(name)?;
        if t.ttype != GGML_Q6_K { return None; }
        Some((&self.buf[self.data_start + t.offset as usize..], t.dims[1] as usize / 256))
    }

    /// Blocs **MXFP4** bruts : `(octets à partir du premier bloc, nb de blocs
    /// par ligne)`. Bloc de 17 octets : un exposant E8M0 puis 16 octets de
    /// nibbles E2M1. C'est le format de gpt-oss-120b.
    pub fn mxfp4_blocks(&self, name: &str) -> Option<(&[u8], usize)> {
        let t = self.tensor(name)?;
        if t.ttype != GGML_MXFP4 { return None; }
        let nb = t.dims[1] as usize / 32;
        Some((&self.buf[self.data_start + t.offset as usize..], nb))
    }

    /// Blocs Q4_0 bruts d'un tenseur : `(octets à partir du premier bloc, nb de
    /// blocs par ligne)`. Permet d'importer les poids **tels quels**, sans les
    /// déquantifier puis les requantifier — le double arrondi coûtait +18 % de
    /// perplexité sur Qwen2.5-0.5B (19,86 → 21,98).
    pub fn q4_blocks(&self, name: &str) -> Option<(&[u8], usize)> {
        let t = self.tensor(name)?;
        if t.ttype != GGML_Q4_0 { return None; }
        let nb = t.dims[1] as usize / 32;
        Some((&self.buf[self.data_start + t.offset as usize..], nb))
    }

    /// Produit scalaire d'une ligne via une vue pré-résolue (Q8_0 ou Q4_0).
    #[inline]
    pub fn q8_dot_at(&self, v: &Q8View, row: usize, qx: &[i16]) -> f32 {
        let mut acc = 0f32;
        if v.ttype == GGML_Q6_K {
            // Q6_K : quants signés sur 6 bits, une échelle signée par 16 poids,
            // aucune asymétrie — donc pas de terme de minimum.
            let ns = v.nb;
            for sup in 0..ns {
                let p = v.base + (row * ns + sup) * TAILLE_Q6K;
                let ql = &self.buf[p..p + 128];
                let qh = &self.buf[p + 128..p + 192];
                let sc = &self.buf[p + 192..p + 208];
                let d = Self::f16_to_f32(
                    u16::from_le_bytes(self.buf[p+208..p+210].try_into().unwrap()));
                for moitie in 0..2usize {
                    let (ql, qh, sc) = (&ql[moitie*64..], &qh[moitie*32..], &sc[moitie*8..]);
                    let b = sup * 256 + moitie * 128;
                    // Les huit groupes de 16 poids d'une moitié ont chacun leur
                    // échelle et occupent des positions CONTIGUËS : on accumule
                    // donc en entier par groupe, et on ne paie qu'une
                    // multiplication flottante par 16 poids au lieu de quatre
                    // opérations flottantes par poids (mesuré : 137 ms par jeton
                    // pour la seule tête d'un 7B, soit 42 % du temps).
                    let mut part = [0i32; 8];
                    for l in 0..32usize {
                        let is = l / 16;
                        let q1 = ((ql[l] & 0x0F) | ((qh[l] & 3) << 4)) as i32 - 32;
                        let q2 = ((ql[l+32] & 0x0F) | (((qh[l] >> 2) & 3) << 4)) as i32 - 32;
                        let q3 = ((ql[l] >> 4) | (((qh[l] >> 4) & 3) << 4)) as i32 - 32;
                        let q4 = ((ql[l+32] >> 4) | (((qh[l] >> 6) & 3) << 4)) as i32 - 32;
                        part[is] += q1 * qx[b + l] as i32;
                        part[2 + is] += q2 * qx[b + l + 32] as i32;
                        part[4 + is] += q3 * qx[b + l + 64] as i32;
                        part[6 + is] += q4 * qx[b + l + 96] as i32;
                    }
                    for (g, &p) in part.iter().enumerate() {
                        acc += d * (sc[g] as i8) as f32 * p as f32;
                    }
                }
            }
            return acc;
        }
        if v.ttype == GGML_Q4_K {
            // Tête Q4_K : même arithmétique que le noyau des projections,
            // mais scalaire — la tête est bornée par la mémoire, pas par le
            // calcul (130 Mo lus par jeton sur un 1,5B).
            let ns = v.nb;
            for sup in 0..ns {
                let p = v.base + (row * ns + sup) * TAILLE_Q4K;
                let d = Self::f16_to_f32(u16::from_le_bytes(self.buf[p..p+2].try_into().unwrap()));
                let dmin = Self::f16_to_f32(u16::from_le_bytes(self.buf[p+2..p+4].try_into().unwrap()));
                let sc = &self.buf[p + 4..p + 16];
                let qs = &self.buf[p + 16..p + 144];
                for g in 0..4usize {
                    let (s0, m0) = echelle_min_q4k(sc, 2 * g);
                    let (s1, m1) = echelle_min_q4k(sc, 2 * g + 1);
                    let mut sq0 = 0i32; let mut sx0 = 0i32;
                    let mut sq1 = 0i32; let mut sx1 = 0i32;
                    for l in 0..32 {
                        let octet = qs[g * 32 + l] as i32;
                        let x0 = qx[sup * 256 + g * 64 + l] as i32;
                        let x1 = qx[sup * 256 + g * 64 + 32 + l] as i32;
                        sq0 += (octet & 15) * x0; sx0 += x0;
                        sq1 += (octet >> 4) * x1; sx1 += x1;
                    }
                    acc += d * s0 as f32 * sq0 as f32 - dmin * m0 as f32 * sx0 as f32;
                    acc += d * s1 as f32 * sq1 as f32 - dmin * m1 as f32 * sx1 as f32;
                }
            }
            return acc;
        }
        if v.q4 {
            // bloc Q4_0 : 2 octets d'échelle + 16 octets = 32 niveaux (4 bits)
            // les 16 premiers sont les nibbles BAS, les 16 suivants les HAUTS
            for b in 0..v.nb {
                let p = v.base + (row * v.nb + b) * 18;
                let d = Self::f16_to_f32(u16::from_le_bytes(self.buf[p..p+2].try_into().unwrap()));
                let w = &self.buf[p + 2..p + 18];
                let x = &qx[b * 32..b * 32 + 32];
                let mut s = 0i32;
                for j in 0..16 {
                    s += (((w[j] & 0x0F) as i32) - 8) * (x[j] as i32);
                    s += (((w[j] >> 4) as i32) - 8) * (x[j + 16] as i32);
                }
                acc += d * s as f32;
            }
        } else {
            for b in 0..v.nb {
                let p = v.base + (row * v.nb + b) * 34;
                let d = Self::f16_to_f32(u16::from_le_bytes(self.buf[p..p+2].try_into().unwrap()));
                let w = &self.buf[p + 2..p + 34];
                let x = &qx[b * 32..b * 32 + 32];
                let mut s = 0i32;
                for j in 0..32 {
                    s += (w[j] as i8 as i32) * (x[j] as i32);
                }
                acc += d * s as f32;
            }
        }
        acc
    }

    /// Déquantification en f32 (F32 / F16 / Q8_0 / Q4_0).
    pub fn dequant(&self, name: &str) -> Vec<f32> {
        let t = self.tensor(name).expect("tenseur absent");
        let base = self.data_start + t.offset as usize;
        let n = t.nelem();
        let mut out = Vec::with_capacity(n);
        match t.ttype {
            GGML_F32 => {
                for i in 0..n {
                    out.push(f32::from_le_bytes(self.buf[base + 4*i..base + 4*i + 4].try_into().unwrap()));
                }
            }
            GGML_F16 => {
                for i in 0..n {
                    out.push(Self::f16_to_f32(u16::from_le_bytes(self.buf[base + 2*i..base + 2*i + 2].try_into().unwrap())));
                }
            }
            GGML_Q8_0 => {
                let nb = n / 32;
                for b in 0..nb {
                    let p = base + b * 34;
                    let d = Self::f16_to_f32(u16::from_le_bytes(self.buf[p..p+2].try_into().unwrap()));
                    for j in 0..32 { out.push(d * (self.buf[p + 2 + j] as i8) as f32); }
                }
            }
            GGML_Q4_0 => {
                let nb = n / 32;
                for b in 0..nb {
                    let p = base + b * 18;
                    let d = Self::f16_to_f32(u16::from_le_bytes(self.buf[p..p+2].try_into().unwrap()));
                    for j in 0..16 { out.push(d * ((self.buf[p + 2 + j] & 0x0F) as i16 - 8) as f32); }
                    for j in 0..16 { out.push(d * ((self.buf[p + 2 + j] >> 4) as i16 - 8) as f32); }
                }
            }
            GGML_Q4_1 => {
                // bloc de 20 octets : échelle f16, décalage f16, 16 octets de nibbles
                // valeur = d · q + m, q ∈ 0..15 (pas de niveau zéro central)
                let nb = n / 32;
                for b in 0..nb {
                    let p = base + b * 20;
                    let d = Self::f16_to_f32(u16::from_le_bytes(self.buf[p..p+2].try_into().unwrap()));
                    let m = Self::f16_to_f32(u16::from_le_bytes(self.buf[p+2..p+4].try_into().unwrap()));
                    for j in 0..16 { out.push(d * (self.buf[p + 4 + j] & 0x0F) as f32 + m); }
                    for j in 0..16 { out.push(d * (self.buf[p + 4 + j] >> 4) as f32 + m); }
                }
            }
            GGML_MXFP4 => {
                // 17 octets par bloc de 32 : exposant E8M0 puis nibbles E2M1.
                // L'échelle vaut 2^(e−127) ; e = 0 et e = 255 sont dégénérés.
                const KV: [f32; 16] = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0,
                                       0.0, -0.5, -1.0, -1.5, -2.0, -3.0, -4.0, -6.0];
                let nb = n / 32;
                for b in 0..nb {
                    let p = base + b * 17;
                    let e = self.buf[p] as u32;
                    let d = if e == 0 || e == 255 { 0.0 } else { f32::from_bits((e - 1) << 23) };
                    for j in 0..16 { out.push(KV[(self.buf[p + 1 + j] & 0x0F) as usize] * d); }
                    for j in 0..16 { out.push(KV[(self.buf[p + 1 + j] >> 4) as usize] * d); }
                }
            }
            GGML_Q4_K => {
                const KV: [f32; 16] = [0.0; 16];
                let _ = KV;
                let nb = n / 256;
                for b in 0..nb {
                    let p = base + b * TAILLE_Q4K;
                    let d = Self::f16_to_f32(u16::from_le_bytes(self.buf[p..p+2].try_into().unwrap()));
                    let dmin = Self::f16_to_f32(u16::from_le_bytes(self.buf[p+2..p+4].try_into().unwrap()));
                    let sc = &self.buf[p + 4..p + 16];
                    let qs = &self.buf[p + 16..p + 144];
                    for g in 0..4 {
                        let (s0, m0) = echelle_min_q4k(sc, 2 * g);
                        let (s1, m1) = echelle_min_q4k(sc, 2 * g + 1);
                        let (d0, n0) = (d * s0 as f32, dmin * m0 as f32);
                        let (d1, n1) = (d * s1 as f32, dmin * m1 as f32);
                        for l in 0..32 { out.push(d0 * (qs[g * 32 + l] & 0x0F) as f32 - n0); }
                        for l in 0..32 { out.push(d1 * (qs[g * 32 + l] >> 4) as f32 - n1); }
                    }
                }
            }
            GGML_Q6_K => {
                let nb = n / 256;
                for b in 0..nb {
                    let p = base + b * TAILLE_Q6K;
                    let ql = &self.buf[p..p + 128];
                    let qh = &self.buf[p + 128..p + 192];
                    let sc = &self.buf[p + 192..p + 208];
                    let d = Self::f16_to_f32(u16::from_le_bytes(self.buf[p+208..p+210].try_into().unwrap()));
                    for moitie in 0..2 {
                        let (ql, qh, sc) = (&ql[moitie*64..], &qh[moitie*32..], &sc[moitie*8..]);
                        // ggml écrit les quatre quants en QUARTS SUCCESSIFS :
                        // q1 remplit [0,32), q2 [32,64), q3 [64,96), q4 [96,128).
                        // Les entrelacer par `l` donne des poids faux — écart 0,10
                        // sur une échelle de 0,08, mesuré contre une référence F16.
                        let mut tmp = [0f32; 128];
                        for l in 0..32 {
                            let is = l / 16;
                            let q1 = ((ql[l] & 0x0F) | ((qh[l] & 3) << 4)) as i16 - 32;
                            let q2 = ((ql[l + 32] & 0x0F) | (((qh[l] >> 2) & 3) << 4)) as i16 - 32;
                            let q3 = ((ql[l] >> 4) | (((qh[l] >> 4) & 3) << 4)) as i16 - 32;
                            let q4 = ((ql[l + 32] >> 4) | (((qh[l] >> 6) & 3) << 4)) as i16 - 32;
                            let s = |k: usize| d * (sc[is + k] as i8) as f32;
                            tmp[l] = s(0) * q1 as f32;
                            tmp[l + 32] = s(2) * q2 as f32;
                            tmp[l + 64] = s(4) * q3 as f32;
                            tmp[l + 96] = s(6) * q4 as f32;
                        }
                        out.extend_from_slice(&tmp);
                    }
                }
            }
            other => panic!("dequant : type {other} non géré"),
        }
        out
    }
}
