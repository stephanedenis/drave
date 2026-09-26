#![allow(dead_code)] // catalogue d'encodages : les mesures n'en exercent qu'une partie

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

// --------------------------------------------------------------------------- //
// 5. Liste FUSIONNÉE : une seule liste triée + bits de signe
// --------------------------------------------------------------------------- //

/// Au lieu de deux listes (+, −) parcourues séparément, une **seule** liste
/// triée par destination, accompagnée d'un plan de signes (1 bit par événement).
///
/// Avantage décisif pour le moteur : l'accès à l'accumulateur devient
/// **monotone croissant**, donc séquentiel — au lieu de sauter entre deux
/// moitiés de la matrice.
pub struct FusedSign {
    pub n_rows: usize,
    pub n_cols: usize,
    pub row_start: Vec<usize>,
    pub data: Vec<u8>,          // varint(n_ev) puis les écarts triés
    pub signs: Vec<u64>,        // 1 bit par événement (1 = positif)
    pub sign_pos: Vec<u32>,     // index du premier bit de signe de chaque ligne
    pub n_events: usize,
}

impl FusedSign {
    pub fn build(levels: &[i8], n_rows: usize, n_cols: usize) -> Self {
        let mut data = Vec::with_capacity(n_rows * 24);
        let mut row_start = Vec::with_capacity(n_rows + 1);
        let mut sign_pos = Vec::with_capacity(n_rows + 1);
        let mut signs: Vec<u64> = Vec::with_capacity(n_rows * 4);
        let mut cur = 0u64;
        let mut nbits = 0u32;
        let mut n_events = 0usize;

        for r in 0..n_rows {
            row_start.push(data.len());
            sign_pos.push(n_events as u32);
            let row = &levels[r * n_cols..(r + 1) * n_cols];
            let n_ev = row.iter().filter(|&&v| v != 0).count();
            put_varint(&mut data, n_ev as u64);
            let mut prev = 0usize;
            for (c, &v) in row.iter().enumerate() {
                if v == 0 { continue; }
                put_varint(&mut data, (c - prev) as u64);
                prev = c;
                if v > 0 { cur |= 1u64 << nbits; }
                nbits += 1;
                n_events += 1;
                if nbits == 64 { signs.push(cur); cur = 0; nbits = 0; }
            }
        }
        if nbits > 0 { signs.push(cur); }
        row_start.push(data.len());
        sign_pos.push(n_events as u32);
        FusedSign { n_rows, n_cols, row_start, data, signs, sign_pos, n_events }
    }

    pub fn bits(&self) -> u64 {
        (self.data.len() as u64) * 8 + (self.signs.len() as u64) * 64
            + (self.row_start.len() as u64 + self.sign_pos.len() as u64) * 8
    }
    pub fn bits_per_weight(&self) -> f64 { self.bits() as f64 / (self.n_rows * self.n_cols) as f64 }

    /// Compte les événements d'une ligne (sans les accumuler).
    pub fn row_events_count(&self, r: usize, acc: &mut usize) {
        let mut p = self.row_start[r];
        let b0 = self.data[p];
        *acc += if b0 < 0x80 { b0 as usize } else {
            p += 1;
            let mut v = (b0 & 0x7F) as usize;
            let mut sh = 7;
            loop {
                let b = self.data[p]; p += 1;
                v |= ((b & 0x7F) as usize) << sh;
                if b < 0x80 { break; }
                sh += 7;
            }
            v
        };
    }
}

// --------------------------------------------------------------------------- //
// 4. Listes par SOURCE, valeur incluse (mode « push » du moteur d'inférence)
// --------------------------------------------------------------------------- //

/// Matrice quantifiée int8, transposée en **listes par source** : pour chaque
/// entrée `i`, la liste triée des sorties `o` qu'elle alimente, avec la valeur du
/// poids. Chaque événement est `varint(écart de sortie) + i8(valeur)` — soit
/// exactement ce que consommera le PE matériel : une adresse et une valeur.
///
/// L'échelle est **par sortie** (`scale[o]`) : la contribution d'un événement est
/// `q_poids × q_activation × scale[o] × scale_activation`.
pub struct PushMat {
    pub n_in: usize,
    pub n_out: usize,
    pub row_start: Vec<u32>,    // n_in + 1
    pub row_ev: Vec<u32>,       // événements par source
    pub data: Vec<u8>,
    pub scale: Vec<f32>,        // une par destination
    pub n_events: usize,
}

impl PushMat {
    /// Quantifie en int8 une matrice f32 `[n_out × n_in]` (row-major) et la
    /// transpose en listes par source. Les zéros ne produisent aucun événement.
    pub fn build(w: &[f32], n_out: usize, n_in: usize) -> Self {
        assert_eq!(w.len(), n_out * n_in);
        let mut scale = vec![0f32; n_out];
        let cap = (n_out as f32 * 1.02) as usize + 4;
        let mut lists: Vec<Vec<u8>> = (0..n_in).map(|_| Vec::with_capacity(cap)).collect();
        let mut last_o = vec![0usize; n_in];
        let mut row_ev = vec![0u32; n_in];
        let mut n_events = 0usize;
        for o in 0..n_out {
            let row = &w[o * n_in..(o + 1) * n_in];
            let mut mx = 0f32;
            for &v in row { let a = v.abs(); if a > mx { mx = a; } }
            // échelle de la ligne de sortie : 127 niveaux signés
            let s = if mx > 0.0 { mx / 127.0 } else { 1.0 };
            scale[o] = s;
            let inv = 1.0 / s;
            for (i, &v) in row.iter().enumerate() {
                let q = (v * inv).round();
                if q == 0.0 { continue; }
                let q = if q > 127.0 { 127i8 } else if q < -127.0 { -127i8 } else { q as i8 };
                let l = &mut lists[i];
                put_varint(l, (o - last_o[i]) as u64);
                l.push(q as u8);
                last_o[i] = o;
                row_ev[i] += 1;
                n_events += 1;
            }
        }
        let mut data = Vec::with_capacity(n_events * 2 + n_in);
        let mut row_start = Vec::with_capacity(n_in + 1);
        for i in 0..n_in {
            row_start.push(data.len() as u32);
            data.extend_from_slice(&lists[i]);
        }
        row_start.push(data.len() as u32);
        PushMat { n_in, n_out, row_start, row_ev, data, scale, n_events }
    }

    /// Taille occupée par les listes, en bits par poids de la matrice d'origine.
    pub fn bits(&self) -> u64 { self.data.len() as u64 * 8 }

    pub fn bits_per_weight(&self) -> f64 {
        self.data.len() as f64 * 8.0 / (self.n_in as f64 * self.n_out as f64)
    }
}


// --------------------------------------------------------------------------- //
// 5. Matrice dense int8 par ligne de sortie (référence « sans événements »)
// --------------------------------------------------------------------------- //

/// Même quantification que `PushMat` (int8, une échelle par sortie), mais
/// conservée **en clair, ligne par ligne** : le produit scalaire se fait alors
/// par ligne de sortie, sans dispersion ni réduction. C'est la référence contre
/// laquelle mesurer ce que coûte l'architecture événementielle sur CPU.
pub struct DenseQ8 {
    pub n_in: usize,
    pub n_out: usize,
    pub q: Vec<i8>,        // n_out × n_in, row-major
    pub scale: Vec<f32>,   // une par sortie
}

impl DenseQ8 {
    pub fn build(w: &[f32], n_out: usize, n_in: usize) -> Self {
        let mut q = vec![0i8; n_out * n_in];
        let mut scale = vec![0f32; n_out];
        for o in 0..n_out {
            let row = &w[o * n_in..(o + 1) * n_in];
            let mut mx = 0f32;
            for &v in row { let a = v.abs(); if a > mx { mx = a; } }
            let s = if mx > 0.0 { mx / 127.0 } else { 1.0 };
            scale[o] = s;
            let inv = 1.0 / s;
            for (i, &v) in row.iter().enumerate() {
                let r = (v * inv).round();
                q[o * n_in + i] = if r > 127.0 { 127 } else if r < -127.0 { -127 } else { r as i8 };
            }
        }
        DenseQ8 { n_in, n_out, q, scale }
    }

    /// Produit scalaire d'une ligne. Déroulé 4× avec quatre accumulateurs :
    /// une seule chaîne d'accumulation i64 coûte ~3 cycles par élément et
    /// domine tout le reste (mesuré : 8,5 tok/s contre 10,7 pour le moteur
    /// d'événements avant déroulage).
    #[inline]
    pub fn dot(&self, o: usize, x: &[i32]) -> i64 {
        let row = &self.q[o * self.n_in..(o + 1) * self.n_in];
        let n = self.n_in;
        let (mut a0, mut a1, mut a2, mut a3) = (0i64, 0i64, 0i64, 0i64);
        let mut i = 0usize;
        while i + 4 <= n {
            a0 += row[i] as i64 * x[i] as i64;
            a1 += row[i + 1] as i64 * x[i + 1] as i64;
            a2 += row[i + 2] as i64 * x[i + 2] as i64;
            a3 += row[i + 3] as i64 * x[i + 3] as i64;
            i += 4;
        }
        let mut s = a0 + a1 + a2 + a3;
        while i < n { s += row[i] as i64 * x[i] as i64; i += 1; }
        s
    }
}
