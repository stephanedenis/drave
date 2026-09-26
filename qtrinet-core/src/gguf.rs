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
pub const GGML_Q8_0: u32 = 8;

/// Pointeur pré-résolu vers les lignes d'un tenseur Q8_0.
pub struct Q8View { pub base: usize, pub n_cols: usize, pub nb: usize }

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
            other => panic!("row_f32 : type {other} non géré"),
        }
        out
    }

    /// Vue pré-résolue sur un tenseur Q8_0 : évite de rechercher le tenseur
    /// (parcours linéaire des 290 descripteurs) à chaque ligne. La tête de
    /// sortie appelle cela 151 936 fois par token.
    pub fn q8_view(&self, name: &str) -> Q8View {
        let t = self.tensor(name).expect("tenseur absent");
        assert_eq!(t.ttype, GGML_Q8_0, "q8_view : tenseur non Q8_0");
        let n_cols = t.dims[1] as usize;
        Q8View { base: self.data_start + t.offset as usize, n_cols, nb: n_cols / 32 }
    }

    /// Produit scalaire d'une ligne via une vue pré-résolue.
    #[inline]
    pub fn q8_dot_at(&self, v: &Q8View, row: usize, qx: &[i16]) -> f32 {
        let mut acc = 0f32;
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
            other => panic!("dequant : type {other} non géré"),
        }
        out
    }
}
