//! Encodages de listes pour matrices quantifiées + mesure exacte de leur taille.
//!
//! Trois familles, toutes **sans perte** par rapport aux niveaux quantifiés :
//!
//! 1. `SignedDelta` — deux listes triées de positions (+, −) par ligne, écarts en
//!    varint. La valeur est portée par l'appartenance à la liste : **zéro bit de
//!    valeur** (idéal pour le binaire/ternaire).
//! 2. `BitmapSign` — un bitmap des non-nuls (1 bit/poids) + un bit de signe par
//!    non-nul. Gagne sur les matrices plutôt denses.
//! 3. `SparseK` — bitmap (1 bit/poids) + k bits par non-nul : les valeurs gardent
//!    leur précision, les zéros ne coûtent rien. C'est la forme générale.
//!
//! La taille est **calculée sur les données réelles**, pas estimée.

/// Écrit un entier en varint LEB128 (7 bits par octet).
#[inline]
pub fn put_varint(out: &mut Vec<u8>, mut v: u64) {
    loop {
        let mut b = (v & 0x7F) as u8;
        v >>= 7;
        if v != 0 { b |= 0x80; }
        out.push(b);
        if v == 0 { break; }
    }
}

#[inline]
pub fn get_varint(buf: &[u8], p: &mut usize) -> u64 {
    let mut v = 0u64;
    let mut shift = 0;
    loop {
        let b = buf[*p];
        *p += 1;
        v |= ((b & 0x7F) as u64) << shift;
        if b & 0x80 == 0 { break; }
        shift += 7;
    }
    v
}

// --------------------------------------------------------------------------- //
// 1. Listes signées avec écarts
// --------------------------------------------------------------------------- //

pub struct SignedDelta {
    pub n_rows: usize,
    pub n_cols: usize,
    pub data: Vec<u8>,          // par ligne : varint(len_pos), varint(len_neg), puis les écarts
    pub n_events: usize,
    pub row_start: Vec<usize>,
}

impl SignedDelta {
    /// Construit les deux listes signées d'une matrice de niveaux (row-major).
    pub fn build(levels: &[i8], n_rows: usize, n_cols: usize) -> Self {
        let mut data = Vec::with_capacity(n_rows * 32);
        let mut row_start = Vec::with_capacity(n_rows + 1);
        let mut n_events = 0usize;
        for r in 0..n_rows {
            row_start.push(data.len());
            let row = &levels[r * n_cols..(r + 1) * n_cols];
            let pos: Vec<usize> = (0..n_cols).filter(|&c| row[c] > 0).collect();
            let neg: Vec<usize> = (0..n_cols).filter(|&c| row[c] < 0).collect();
            n_events += pos.len() + neg.len();
            put_varint(&mut data, pos.len() as u64);
            put_varint(&mut data, neg.len() as u64);
            let mut prev = 0usize;
            for &c in &pos { put_varint(&mut data, (c - prev) as u64); prev = c; }
            let mut prev = 0usize;
            for &c in &neg { put_varint(&mut data, (c - prev) as u64); prev = c; }
        }
        row_start.push(data.len());
        SignedDelta { n_rows, n_cols, data, n_events, row_start }
    }

    pub fn bits(&self) -> u64 { (self.data.len() as u64) * 8 }
    pub fn bits_per_weight(&self) -> f64 { self.bits() as f64 / (self.n_rows * self.n_cols) as f64 }
    pub fn events_per_row(&self) -> f64 { self.n_events as f64 / self.n_rows as f64 }

    /// Itère les événements d'une ligne : (colonne, signe).
    pub fn row_events<F: FnMut(usize, i32)>(&self, r: usize, mut f: F) {
        let mut p = self.row_start[r];
        let np = get_varint(&self.data, &mut p) as usize;
        let nn = get_varint(&self.data, &mut p) as usize;
        let mut c = 0usize;
        for _ in 0..np { c += get_varint(&self.data, &mut p) as usize; f(c, 1); }
        let mut c = 0usize;
        for _ in 0..nn { c += get_varint(&self.data, &mut p) as usize; f(c, -1); }
    }
}

// --------------------------------------------------------------------------- //
// 2. Bitmap + signes
// --------------------------------------------------------------------------- //

pub struct BitmapSign {
    pub n_rows: usize,
    pub n_cols: usize,
    pub mask: Vec<u64>,        // 1 bit par poids
    pub signs: Vec<u64>,       // 1 bit par non-nul, dans l'ordre du bitmap
    pub n_events: usize,
    /// index du premier bit de signe de chaque ligne (pour un décodage direct)
    pub sign_pos: Vec<u32>,
}

impl BitmapSign {
    pub fn build(levels: &[i8], n_rows: usize, n_cols: usize) -> Self {
        let n = n_rows * n_cols;
        let mut mask = vec![0u64; (n + 63) / 64];
        let mut signs = Vec::with_capacity(n / 8);
        let mut cur = 0u64;
        let mut nbits = 0u32;
        let mut n_events = 0usize;
        let mut sign_pos = Vec::with_capacity(n_rows + 1);
        for (i, &v) in levels.iter().enumerate() {
            if i % n_cols == 0 { sign_pos.push(n_events as u32); }
            if v != 0 {
                mask[i / 64] |= 1u64 << (i % 64);
                if v > 0 { cur |= 1u64 << nbits; }
                nbits += 1;
                n_events += 1;
                if nbits == 64 { signs.push(cur); cur = 0; nbits = 0; }
            }
        }
        if nbits > 0 { signs.push(cur); }
        sign_pos.push(n_events as u32);
        BitmapSign { n_rows, n_cols, mask, signs, n_events, sign_pos }
    }

    pub fn bits(&self) -> u64 {
        (self.mask.len() as u64 + self.signs.len() as u64) * 64
    }
    pub fn bits_per_weight(&self) -> f64 { self.bits() as f64 / (self.n_rows * self.n_cols) as f64 }
}

// --------------------------------------------------------------------------- //
// 3. Bitmap + k bits par non-nul
// --------------------------------------------------------------------------- //

pub struct SparseK {
    pub n_rows: usize,
    pub n_cols: usize,
    pub k: u32,
    pub n_events: usize,
    pub n_weights: usize,
    pub sign_bits: u64,        // 1 bit par non-nul (signe)
    pub value_bits: u64,       // (k-1) bits de magnitude par non-nul
    pub bitmap_bits: u64,      // 1 bit par poids
}

impl SparseK {
    /// k = largeur totale en bits par non-nul (1 = signe seul = ternaire/binaire).
    pub fn build(levels: &[i8], n_rows: usize, n_cols: usize, k: u32) -> Self {
        let n = n_rows * n_cols;
        let mut n_events = 0usize;
        for &v in levels { if v != 0 { n_events += 1; } }
        SparseK {
            n_rows, n_cols, k, n_events, n_weights: n,
            sign_bits: n_events as u64,
            value_bits: n_events as u64 * (k.saturating_sub(1)) as u64,
            bitmap_bits: n as u64,
        }
    }
    pub fn bits(&self) -> u64 { self.bitmap_bits + self.sign_bits + self.value_bits }
    pub fn bits_per_weight(&self) -> f64 { self.bits() as f64 / self.n_weights as f64 }
}

// --------------------------------------------------------------------------- //
// 4. Référence : dense k bits
// --------------------------------------------------------------------------- //

pub fn dense_bits(n_weights: usize, k: u32) -> u64 { n_weights as u64 * k as u64 }
