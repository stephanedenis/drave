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
    /// Produit scalaire avec accumulation i32 par tranches de 256, reportée en
    /// i64 entre tranches. L'accumulation i64 sur toute la ligne empêchait
    /// LLVM de vectoriser (conversion i8→i64 à chaque produit) ; la borne de
    /// 256 garantit qu'aucune tranche ne débordé (127 × 32767 × 256 = 1,07e9).
    #[inline]
    pub fn dot_chunked(&self, o: usize, x: &[i32]) -> i64 {
        let row = &self.q[o * self.n_in..(o + 1) * self.n_in];
        let mut s = 0i64;
        for (offset, bloc) in row.chunks(256).enumerate() {
            let xb = &x[offset * 256..offset * 256 + bloc.len()];
            // HUIT accumulateurs indépendants, et non un seul : avec une seule
            // chaîne `a += ...`, chaque addition attend la précédente et le
            // noyau plafonne à ~1 multiplication par cycle — mesuré 0,54.
            // Huit chaînes donnent au processeur de quoi remplir ses ports, et
            // dérouler par 8 expose le motif que LLVM transforme en `vpmaddwd`
            // (élargissement i8→i16, produits appariés, somme des paires).
            // Débordement : 32 termes par tranche de 256 et par chaîne, soit
            // 32 × 127 × 32767 = 1,3e8 < 2^31. Sûr pour toutes les `abits`.
            let n = bloc.len();
            let mut a = [0i32; 8];
            let mut i = 0usize;
            while i + 8 <= n {
                for k in 0..8 { a[k] += bloc[i + k] as i32 * xb[i + k]; }
                i += 8;
            }
            let mut t = 0i32;
            for k in 0..8 { t += a[k]; }
            while i < n { t += bloc[i] as i32 * xb[i]; i += 1; }
            s += t as i64;
        }
        s
    }

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

// --------------------------------------------------------------------------- //
// 6. Matrice dense 4 bits (0,5 octet/poids + échelles de bloc)
// --------------------------------------------------------------------------- //

/// Taille des blocs d'échelle. 32 est le compromis standard (Q4_0) : assez fin
/// pour que chaque bloc ait une dynamique resserrée, assez gros pour que le
/// coût des échelles reste marginal.
pub const BLOC_Q4: usize = 32;

/// Grille int4 symétrique : le nibble `n` vaut `n − 8`.
pub const LUT_INT4: [i8; 16] = [-8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7];

/// Table E2M1 du format MXFP4, magnitudes **doublées** pour rester entières.
/// Le bit de poids fort est le signe ; l'échelle de bloc (une puissance de
/// deux) est divisée par deux en compensation — l'import est donc exact.
pub const LUT_MXFP4: [i8; 16] = [0, 1, 2, 3, 4, 6, 8, 12, 0, -1, -2, -3, -4, -6, -8, -12];

/// Matrice quantifiée sur 4 bits, rangée par ligne de sortie.
///
/// Mesuré : le produit scalaire dense lit ses poids à 14–27 Go/s, soit le mur
/// de la bande passante mémoire de cette machine (repère : ~19 Go/s). Le
/// vectoriser davantage ne sert donc à rien — **seul le nombre d'octets par
/// poids compte**. D'où la forme 4 bits : 0,5 octet/poids, plus une échelle
/// `u8` par bloc de 32 (8/32 = 0,25 bit) → **4,25 bits/poids**, soit ×1,88
/// moins d'octets que l'int8.
///
/// Échelles : chaque bloc a sa propre échelle `s_b = max|w| / 7`, stockée
/// relativement à l'échelle de ligne (u8 sur 255). Sans échelle de bloc, une
/// ligne de 4864 poids n'aurait qu'une seule dynamique et les petits poids
/// seraient écrasés à zéro.
/// Origine des poids d'une matrice 4 bits.
///
/// `Propre` : les nibbles sont entrelacés dans `q` (octet k = poids 2k et
/// 2k+1), disposition qui permet à `vpmaddwd` de traiter 32 poids d'un coup.
/// Les deux autres lisent les blocs **tels quels dans le fichier** : Q4_0 range
/// les poids 0–15 dans les nibbles bas et 16–31 dans les hauts, MXFP4 fait de
/// même avec un exposant E8M0 en tête. Dans les deux cas les 16 activations à
/// apparier sont **contiguës** — l'entrelacement était une commodité, pas une
/// nécessité.
#[derive(Clone, Copy, PartialEq, Eq)]
pub enum Source { Propre, Q4_0, Mxfp4, Q4_K }

pub struct DenseQ4 {
    pub n_in: usize,
    pub n_out: usize,
    /// Table des 16 nibbles → valeur entière signée. Par défaut `n − 8`
    /// (grille symétrique int4) ; l'import MXFP4 y met les magnitudes E2M1
    /// doublées, `±{0,1,2,3,4,6,8,12}`, qui sont exactement les valeurs du
    /// format une fois l'échelle ramenée à une puissance de deux.
    pub lut: [i8; 16],
    /// Vrai si `sc` porte l'octet d'exposant E8M0 du format MXFP4 au lieu
    /// d'une échelle relative sur 16 bits signés.
    pub e8m0: bool,
    pub q: Vec<u8>,        // n_out × ⌈n_in/2⌉ — vide si `src != Propre`
    /// n_out × ⌈n_in/BLOC_Q4⌉ échelles de bloc (vide si `src != Propre`),
    /// **relatives et signées**
    /// (i16 stocké en u16). Le signe compte : Q4_0 écrit `d = max/−8` où `max`
    /// est la valeur signée de plus grande amplitude, donc `d` est négatif dès
    /// que le poids extrême du bloc est positif. Prendre la valeur absolue
    /// donnait PPL 3 550 569 au lieu de 19,86.
    pub sc: Vec<u16>,
    /// Vide si `src != Propre`.
    pub scale: Vec<f32>,
    /// Origine des poids. Hors `Propre`, la matrice ne possède **rien** : elle
    /// pointe dans le tampon du GGUF, sans copie ni réarrangement.
    pub src: Source,
    /// Premier octet du tenseur dans le tampon du GGUF.
    ///
    /// # Sûreté
    /// Le tampon doit vivre plus longtemps que la matrice. `Model` déclare `g`
    /// **avant** `layers`, et déplacer un `Vec<u8>` ne déplace pas son
    /// allocation : les pointeurs restent valides. Aucun `Drop` ne déréférence
    /// `base`.
    pub base: *const u8,
    /// Blocs de 32 poids par ligne de sortie (0 si `Propre`).
    pub nb_ligne: usize,
}

// La matrice ne fait que prêter des octets : la partager entre threads est sûr
// dès lors que le tampon emprunté l'est (invariant ci-dessus).
unsafe impl Send for DenseQ4 {}
unsafe impl Sync for DenseQ4 {}

impl DenseQ4 {
    pub fn build(w: &[f32], n_out: usize, n_in: usize) -> Self {
        assert_eq!(w.len(), n_out * n_in);
        let half = n_in.div_ceil(2);
        let n_bloc = n_in.div_ceil(BLOC_Q4);
        let mut q = vec![0u8; n_out * half];
        let mut sc = vec![1u16; n_out * n_bloc];
        let mut scale = vec![1f32; n_out];
        for o in 0..n_out {
            let row = &w[o * n_in..(o + 1) * n_in];
            let mut sb = vec![1f32; n_bloc];
            for (b, s) in sb.iter_mut().enumerate() {
                let (lo, hi) = (b * BLOC_Q4, ((b + 1) * BLOC_Q4).min(n_in));
                let mut mx = 0f32;
                for &v in &row[lo..hi] { let a = v.abs(); if a > mx { mx = a; } }
                // Bloc entièrement nul : l'échelle n'a pas d'importance, la
                // valeur reconstruite sera 0 de toute façon.
                *s = if mx > 0.0 { mx / 7.0 } else { 1.0 };
            }
            let rs = sb.iter().cloned().fold(0f32, f32::max);
            let rs = if rs > 0.0 { rs } else { 1.0 };
            scale[o] = rs;
            for b in 0..n_bloc {
                // Échelle relative sur 16 bits, et non 8 : avec 255 niveaux, un
                // bloc dix fois plus faible que le maximum de la ligne n'était
                // décrit qu'à 4 % près — mesuré PPL 17,10 contre 14,70 en int8,
                // un coût de qualité qui n'a rien à voir avec les 4 bits eux-mêmes.
                let u = (32767.0 * sb[b] / rs).round().clamp(1.0, 32767.0);
                sc[o * n_bloc + b] = u as u16;
                let inv = 1.0 / sb[b];
                let (lo, hi) = (b * BLOC_Q4, ((b + 1) * BLOC_Q4).min(n_in));
                for i in lo..hi {
                    let r = (row[i] * inv).round().clamp(-8.0, 7.0) as i32;
                    let nib = (r + 8) as u8;          // 0..15, biaisé
                    let idx = o * half + i / 2;
                    if i % 2 == 0 { q[idx] |= nib; } else { q[idx] |= nib << 4; }
                }
            }
        }
        DenseQ4 { n_in, n_out, lut: LUT_INT4, e8m0: false, q, sc, scale,
                  src: Source::Propre, base: std::ptr::null(), nb_ligne: 0 }
    }

    /// Importe des blocs **Q4_0 verbatim** (18 octets : une échelle f16 puis
    /// 16 octets de nibbles) dans la disposition interne.
    ///
    /// Q4_0 range le poids `j` dans le nibble bas de l'octet `j` et le poids
    /// `j+16` dans le nibble haut du même octet ; ici les nibbles sont
    /// entrelacés (octet `k` = poids `2k` et `2k+1`). Les échelles f16 sont
    /// réencodées en u16 relatif (erreur 1/65535, négligeable).
    ///
    /// C'est ce qui rend le chemin 4 bits **fidèle** : importer n'ajoute aucune
    /// erreur de quantification, là où déquantifier en f32 puis requantizer en
    /// ajoutait une seconde couche.
    pub fn import_q4_0(buf: &[u8], n_out: usize, n_in: usize, nb_ligne: usize) -> Self {
        let half = n_in.div_ceil(2);
        let n_bloc = n_in.div_ceil(BLOC_Q4);
        let mut q = vec![0u8; n_out * half];
        let mut sc = vec![1u16; n_out * n_bloc];
        let mut scale = vec![1f32; n_out];
        let mut dbloc = vec![0f32; n_bloc];
        for o in 0..n_out {
            let mut rs = 0f32;
            for b in 0..n_bloc.min(nb_ligne) {
                let p = (o * nb_ligne + b) * 18;
                let d = crate::gguf::Gguf::f16_to_f32(
                    u16::from_le_bytes([buf[p], buf[p + 1]]));
                dbloc[b] = d;
                if d.abs() > rs { rs = d.abs(); }
            }
            if rs <= 0.0 { rs = 1.0; }
            scale[o] = rs;
            for b in 0..n_bloc.min(nb_ligne) {
                // Signe conservé : `d` peut être négatif (cf. Q4_0).
                let u = (32767.0 * dbloc[b] / rs).round();
                let u = if u.abs() < 1.0 { if dbloc[b] < 0.0 { -1.0 } else { 1.0 } } else { u };
                sc[o * n_bloc + b] = u.clamp(-32767.0, 32767.0) as i16 as u16;
                let p = (o * nb_ligne + b) * 18 + 2;
                let lo = b * BLOC_Q4;
                let hi = ((b + 1) * BLOC_Q4).min(n_in);
                for i in lo..hi {
                    let src = if i < lo + 16 { buf[p + (i - lo)] & 0x0F } else { buf[p + (i - lo) - 16] >> 4 };
                    let idx = o * half + i / 2;
                    if i % 2 == 0 { q[idx] |= src; } else { q[idx] |= src << 4; }
                }
            }
        }
        DenseQ4 { n_in, n_out, lut: LUT_INT4, e8m0: false, q, sc, scale,
                  src: Source::Propre, base: std::ptr::null(), nb_ligne: 0 }
    }

    /// **Prête** des super-blocs Q4_K (144 octets pour 256 poids) lus dans le
    /// fichier. Format de toute la famille Qwen/Llama en `Q4_K_M`.
    ///
    /// # Sûreté
    /// `base` doit pointer sur le premier super-bloc et rester valide.
    pub unsafe fn emprunter_q4k(base: *const u8, n_out: usize, n_in: usize,
                                nb_super: usize) -> Self {
        DenseQ4 {
            n_in, n_out, lut: LUT_INT4, e8m0: false,
            q: Vec::new(), sc: Vec::new(), scale: Vec::new(),
            src: Source::Q4_K, base, nb_ligne: nb_super,
        }
    }

    /// Produit scalaire **Q4_K en place** (noyau AVX2).
    ///
    /// Q4_K est **asymétrique** : chaque sous-bloc de 32 poids a une échelle
    /// *et* un minimum, `y = d·sc·q − dmin·m`. La somme se scinde donc en deux
    /// parties entières exactes :
    /// `Σ y·x = d·sc·Σ q·x − dmin·m·Σ x`.
    /// `Σ x` par sous-bloc est précalculé une fois par appel (`sx32`), ce qui
    /// évite de le refaire pour chaque ligne de sortie — 4 864 fois pour un FFN.
    #[cfg(target_arch = "x86_64")]
    #[target_feature(enable = "avx2")]
    unsafe fn dot16_q4k_avx2(&self, o: usize, x: &[i16], sx32: &[i32]) -> f32 {
        use std::arch::x86_64::*;
        let xp = x.as_ptr();
        let mut sum = 0f32;
        for sup in 0..self.nb_ligne {
            let p = self.base.add((o * self.nb_ligne + sup) * crate::gguf::TAILLE_Q4K);
            let d = crate::gguf::Gguf::f16_to_f32(u16::from_le_bytes([*p, *p.add(1)]));
            let dmin = crate::gguf::Gguf::f16_to_f32(u16::from_le_bytes([*p.add(2), *p.add(3)]));
            let sc = std::slice::from_raw_parts(p.add(4), 12);
            let qs = p.add(16);
            for g in 0..4usize {
                let (s0, m0) = crate::gguf::echelle_min_q4k(sc, 2 * g);
                let (s1, m1) = crate::gguf::echelle_min_q4k(sc, 2 * g + 1);
                let octets = _mm_loadu_si128(qs.add(g * 32) as *const __m128i);
                let bas = _mm_and_si128(octets, _mm_set1_epi8(0x0f));
                let haut = _mm_and_si128(_mm_srli_epi16(octets, 4), _mm_set1_epi8(0x0f));
                let octets2 = _mm_loadu_si128(qs.add(g * 32 + 16) as *const __m128i);
                let bas2 = _mm_and_si128(octets2, _mm_set1_epi8(0x0f));
                let haut2 = _mm_and_si128(_mm_srli_epi16(octets2, 4), _mm_set1_epi8(0x0f));
                // poids 64g..64g+31 (nibbles bas) puis 64g+32..64g+63 (hauts)
                let x0 = xp.add(sup * 256 + g * 64);
                let x1 = xp.add(sup * 256 + g * 64 + 32);
                let sq0 = somme_produits(bas, bas2, x0);
                let sq1 = somme_produits(haut, haut2, x1);
                let sx0 = *sx32.get_unchecked(sup * 8 + 2 * g) as f32;
                let sx1 = *sx32.get_unchecked(sup * 8 + 2 * g + 1) as f32;
                sum += d * s0 as f32 * sq0 as f32 - dmin * m0 as f32 * sx0;
                sum += d * s1 as f32 * sq1 as f32 - dmin * m1 as f32 * sx1;
            }
        }
        sum
    }

    /// Importe des blocs **MXFP4 verbatim** (17 octets : un exposant E8M0 puis
    /// 16 octets de nibbles E2M1).
    ///
    /// Le format stocke des flottants, mais ses huit magnitudes sont
    /// `{0, ½, 1, 1½, 2, 3, 4, 6}` : doublées, ce sont les **entiers**
    /// `{0,1,2,3,4,6,8,12}`, et l'échelle de bloc est une puissance de deux.
    /// L'import est donc **exact** — aucune requantification.
    pub fn import_mxfp4(buf: &[u8], n_out: usize, n_in: usize, nb_ligne: usize) -> Self {
        let half = n_in.div_ceil(2);
        let n_bloc = n_in.div_ceil(BLOC_Q4);
        let mut q = vec![0u8; n_out * half];
        let mut sc = vec![1u16; n_out * n_bloc];
        let scale = vec![1f32; n_out];
        for o in 0..n_out {
            for b in 0..n_bloc.min(nb_ligne) {
                let p = (o * nb_ligne + b) * 17;
                let e = buf[p];
                // e = 0 ou 255 : bloc dégénéré (2^-127, NaN) → zéro.
                sc[o * n_bloc + b] = if e == 0 || e == 255 { 0 } else { e as u16 };
                let lo = b * BLOC_Q4;
                let hi = ((b + 1) * BLOC_Q4).min(n_in);
                for i in lo..hi {
                    // Même disposition que Q4_0 : nibble bas = poids j,
                    // nibble haut = poids j + 16.
                    let src = if i < lo + 16 { buf[p + 1 + (i - lo)] & 0x0F }
                              else { buf[p + 1 + (i - lo) - 16] >> 4 };
                    let idx = o * half + i / 2;
                    if i % 2 == 0 { q[idx] |= src; } else { q[idx] |= src << 4; }
                }
            }
        }
        DenseQ4 { n_in, n_out, lut: LUT_MXFP4, e8m0: true, q, sc, scale,
                  src: Source::Propre, base: std::ptr::null(), nb_ligne: 0 }
    }

    /// **Prête** des blocs Q4_0 ou MXFP4 déjà présents dans le fichier : aucune
    /// copie, aucun réarrangement, chargement instantané. C'est ce qui rend un
    /// modèle de 60 Go possible — le recopier dans notre disposition doublerait
    /// la mémoire exigée (60 Go de fichier + 61 Go de copie sur 108 Go libres).
    ///
    /// # Sûreté
    /// `base` doit pointer sur le premier bloc du tenseur et rester valide
    /// aussi longtemps que la matrice.
    pub unsafe fn emprunter(base: *const u8, n_out: usize, n_in: usize,
                            nb_ligne: usize, mxfp4: bool) -> Self {
        let (lut, e8m0) = if mxfp4 { (LUT_MXFP4, true) } else { (LUT_INT4, false) };
        DenseQ4 {
            n_in, n_out, lut, e8m0,
            q: Vec::new(), sc: Vec::new(), scale: Vec::new(),
            src: if mxfp4 { Source::Mxfp4 } else { Source::Q4_0 },
            base, nb_ligne,
        }
    }

    /// Pas et décalage des blocs dans la source empruntée. (Q4_K a son propre
    /// noyau : ses sous-blocs ne se lisent pas comme des nibbles appariés.)
    fn dot_source_q4k(&self, o: usize, x: &[i32]) -> f32 {
        let t = crate::gguf::TAILLE_Q4K;
        let mut sum = 0f32;
        for sup in 0..self.nb_ligne {
            let p = unsafe { self.base.add((o * self.nb_ligne + sup) * t) };
            let b = unsafe { std::slice::from_raw_parts(p, t) };
            let d = crate::gguf::Gguf::f16_to_f32(u16::from_le_bytes([b[0], b[1]]));
            let dmin = crate::gguf::Gguf::f16_to_f32(u16::from_le_bytes([b[2], b[3]]));
            for g in 0..4usize {
                let (s0, m0) = crate::gguf::echelle_min_q4k(&b[4..16], 2 * g);
                let (s1, m1) = crate::gguf::echelle_min_q4k(&b[4..16], 2 * g + 1);
                for &(sc, mn, decal) in &[(s0, m0, 0usize), (s1, m1, 32usize)] {
                    let base_x = sup * 256 + g * 64 + decal;
                    let mut sq = 0i32;
                    let mut sx = 0i32;
                    for l in 0..32 {
                        let octet = b[16 + g * 32 + l] as i32;
                        let q = if decal == 0 { octet & 15 } else { octet >> 4 };
                        sq += q * x[base_x + l];
                        sx += x[base_x + l];
                    }
                    sum += d * sc as f32 * sq as f32 - dmin * mn as f32 * sx as f32;
                }
            }
        }
        sum
    }

    /// Pas et décalage des blocs dans la source empruntée.
    #[inline]
    fn pas_source(&self) -> (usize, usize) {
        match self.src {
            Source::Q4_0 => (18, 2),
            Source::Mxfp4 => (17, 1),
            Source::Q4_K | Source::Propre => (0, 0),
        }
    }

    /// Échelle d'un bloc **source** (lue dans le fichier).
    ///
    /// MXFP4 : l'exposant E8M0 donne `2^(e−127)` ; la table E2M1 étant
    /// doublée, le multiplicateur est `2^(e−128)`. Q4_0 : une demi-précision
    /// classique, appliquée telle quelle à la grille `n − 8`.
    #[inline]
    unsafe fn echelle_source(&self, p: *const u8) -> f32 {
        if self.src == Source::Mxfp4 {
            match *p {
                0 => f32::from_bits(0x0020_0000),
                255 => 0.0,
                e => f32::from_bits(((e as u32) - 1) << 23),
            }
        } else {
            crate::gguf::Gguf::f16_to_f32(u16::from_le_bytes([*p, *p.add(1)]))
        }
    }

    /// Produit scalaire sur une matrice **empruntée** au fichier.
    fn dot_source(&self, o: usize, x: &[i32]) -> f32 {
        let (pas, decal) = self.pas_source();
        let mut sum = 0f32;
        for b in 0..self.nb_ligne {
            let p = unsafe { self.base.add((o * self.nb_ligne + b) * pas) };
            let d = unsafe { self.echelle_source(p) };
            let qs = unsafe { std::slice::from_raw_parts(p.add(decal), 16) };
            let lo = b * BLOC_Q4;
            let hi = ((b + 1) * BLOC_Q4).min(self.n_in);
            let mut a = 0i32;
            for j in 0..(hi - lo) {
                let octet = qs[j % 16] as usize;
                let nib = if j < 16 { octet & 15 } else { octet >> 4 };
                a += self.lut[nib] as i32 * x[lo + j];
            }
            sum += a as f32 * d;
        }
        sum
    }

    /// Même chose en AVX2. Les nibbles bas d'un bloc source sont les poids
    /// 0–15 et les hauts les poids 16–31 : les deux groupes d'activations à
    /// apparier sont **contigus**, donc aucun réentrelacement n'est nécessaire.
    /// Les sommes par paires sont identiques à celles du chemin entrelacé, et
    /// le résultat reste **bit à bit identique**.
    #[cfg(target_arch = "x86_64")]
    #[target_feature(enable = "avx2")]
    unsafe fn dot16_source_avx2(&self, o: usize, x: &[i16]) -> f32 {
        use std::arch::x86_64::*;
        let (pas, decal) = self.pas_source();
        let table = _mm_loadu_si128(self.lut.as_ptr() as *const __m128i);
        let masque = _mm_set1_epi8(0x0f);
        let xp = x.as_ptr();
        let mut sum = 0f32;
        let mut tmp = [0i32; 8];
        for b in 0..self.nb_ligne {
            let p = self.base.add((o * self.nb_ligne + b) * pas);
            let d = self.echelle_source(p);
            let octets = _mm_loadu_si128(p.add(decal) as *const __m128i);
            let w0 = _mm256_cvtepi8_epi16(_mm_shuffle_epi8(table, _mm_and_si128(octets, masque)));
            let w1 = _mm256_cvtepi8_epi16(_mm_shuffle_epi8(
                table, _mm_and_si128(_mm_srli_epi16(octets, 4), masque)));
            let x0 = _mm256_loadu_si256(xp.add(b * BLOC_Q4) as *const __m256i);
            let x1 = _mm256_loadu_si256(xp.add(b * BLOC_Q4 + 16) as *const __m256i);
            let v = _mm256_add_epi32(_mm256_madd_epi16(w0, x0), _mm256_madd_epi16(w1, x1));
            _mm256_storeu_si256(tmp.as_mut_ptr() as *mut __m256i, v);
            let a = (tmp[0] + tmp[1] + tmp[2] + tmp[3]
                   + tmp[4] + tmp[5] + tmp[6] + tmp[7]) as f32;
            sum += a * d;
        }
        sum
    }

    /// Échelle d'un bloc, selon la convention de la matrice.
    #[inline]
    fn echelle_bloc(&self, o: usize, b: usize, n_bloc: usize) -> f32 {
        let s = self.sc[o * n_bloc + b];
        if self.e8m0 {
            // Mêmes conventions que ggml : e = 0 vaut 2^-127 (sous-normal),
            // e ≥ 255 est dégénéré et traité comme un bloc nul.
            match s {
                0 => f32::from_bits(0x0020_0000),
                255 => 0.0,
                e => f32::from_bits(((e as u32) - 1) << 23),
            }
        } else {
            self.scale[o] * (s as i16 as f32) * (1.0 / 32767.0)
        }
    }

    /// Octets réellement occupés, en bits par poids d'origine.
    pub fn bits_per_weight(&self) -> f64 {
        let octets = match self.src {
            Source::Propre => self.q.len() + self.sc.len() * 2,
            Source::Q4_0 => self.n_out * self.nb_ligne * 18,
            Source::Mxfp4 => self.n_out * self.nb_ligne * 17,
            Source::Q4_K => self.n_out * self.nb_ligne * crate::gguf::TAILLE_Q4K,
        };
        octets as f64 * 8.0 / (self.n_out * self.n_in) as f64
    }

    /// Produit scalaire d'une ligne. Accumulation **entière par bloc** (32
    /// termes au plus : 32 × 8 × 32767 < 2^31), puis une seule mise à
    /// l'échelle flottante par bloc — la conversion en flottant ne coûte donc
    /// rien et l'essentiel du travail reste entier.
    #[inline]
    pub fn dot(&self, o: usize, x: &[i32]) -> f32 {
        if self.src == Source::Q4_K { return self.dot_source_q4k(o, x); }
        if self.src != Source::Propre { return self.dot_source(o, x); }
        let half = self.n_in.div_ceil(2);
        let n_bloc = self.n_in.div_ceil(BLOC_Q4);
        let row = &self.q[o * half..(o + 1) * half];
        let mut sum = 0f32;
        for b in 0..n_bloc {
            let (lo, hi) = (b * BLOC_Q4, ((b + 1) * BLOC_Q4).min(self.n_in));
            let mut a = 0i32;
            let mut i = lo;
            while i + 1 < hi {
                let byte = row[i / 2] as usize;
                a += self.lut[byte & 15] as i32 * x[i];
                a += self.lut[byte >> 4] as i32 * x[i + 1];
                i += 2;
            }
            if i < hi { a += self.lut[row[i / 2] as usize & 15] as i32 * x[i]; }
            sum += a as f32 * self.echelle_bloc(o, b, n_bloc);
        }
        sum
    }
}

impl DenseQ4 {
    /// Même produit scalaire, mais à partir d'activations déjà converties en
    /// i16 (fait **une fois par appel** et non une fois par ligne) : le noyau
    /// AVX2 peut alors charger poids et activations sans réordonnancement.
    ///
    /// Les sommes entières par bloc sont exactes et indépendantes de l'ordre,
    /// donc le résultat est **bit à bit identique** au chemin scalaire — ce
    /// n'est pas une approximation, c'est le même calcul.
    #[inline]
    pub fn dot16(&self, o: usize, x: &[i16], sx32: &[i32]) -> f32 {
        #[cfg(target_arch = "x86_64")]
        {
            if std::is_x86_feature_detected!("avx2") {
                if self.src == Source::Q4_K && sx32.len() * BLOC_Q4 >= self.n_in {
                    return unsafe { self.dot16_q4k_avx2(o, x, sx32) };
                }
                if self.src != Source::Propre && self.src != Source::Q4_K {
                    return unsafe { self.dot16_source_avx2(o, x) };
                }
                if self.n_in % BLOC_Q4 == 0 && x.len() >= self.n_in {
                    return unsafe { self.dot16_avx2(o, x) };
                }
            }
        }
        let xi: Vec<i32> = x[..self.n_in].iter().map(|&v| v as i32).collect();
        self.dot(o, &xi)
    }

    /// Noyau AVX2 : 32 poids (16 octets) par itération.
    ///
    /// Le chemin scalaire coûtait ~5 cycles par poids (dépaquetage, masquage,
    /// décalage, deux chaînes d'accumulation) : mesuré ×1,4 plus LENT que
    /// l'int8 alors qu'il lit deux fois moins d'octets. Ici 16 poids tiennent
    /// dans un `vpmaddwd`, soit ~0,5 opération par poids.
    #[cfg(target_arch = "x86_64")]
    #[target_feature(enable = "avx2")]
    unsafe fn dot16_avx2(&self, o: usize, x: &[i16]) -> f32 {
        use std::arch::x86_64::*;
        let half = self.n_in / 2;
        let n_bloc = self.n_in / BLOC_Q4;
        let row = self.q.as_ptr().add(o * half);
        let xp = x.as_ptr();
        let masque = _mm_set1_epi8(0x0f);
        // La conversion nibble → valeur passe par une table de 16 octets
        // (`pshufb`), ce qui sert les deux formats : `n − 8` pour la grille
        // int4, les magnitudes E2M1 doublées pour MXFP4.
        let table = _mm_loadu_si128(self.lut.as_ptr() as *const __m128i);
        let mut sum = 0f32;
        let mut tmp = [0i32; 8];
        for b in 0..n_bloc {
            let octets = _mm_loadu_si128(row.add(b * 16) as *const __m128i);
            let lo = _mm_shuffle_epi8(table, _mm_and_si128(octets, masque));
            let hi = _mm_shuffle_epi8(table, _mm_and_si128(_mm_srli_epi16(octets, 4), masque));
            // `lo` contient les poids PAIRS (0,2,4…) et `hi` les impairs : il
            // faut les réentrelacer AVANT d'élargir, sinon `vpmaddwd` apparie
            // le poids 2k avec l'activation k (bug trouvé par le test :
            // scalaire 132,3 contre avx2 −2,5).
            let w0 = _mm256_cvtepi8_epi16(_mm_unpacklo_epi8(lo, hi));  // poids 0..15
            let w1 = _mm256_cvtepi8_epi16(_mm_unpackhi_epi8(lo, hi));  // poids 16..31
            let x0 = _mm256_loadu_si256(xp.add(b * BLOC_Q4) as *const __m256i);
            let x1 = _mm256_loadu_si256(xp.add(b * BLOC_Q4 + 16) as *const __m256i);
            let p = _mm256_add_epi32(_mm256_madd_epi16(w0, x0), _mm256_madd_epi16(w1, x1));
            _mm256_storeu_si256(tmp.as_mut_ptr() as *mut __m256i, p);
            let a = (tmp[0] + tmp[1] + tmp[2] + tmp[3]
                   + tmp[4] + tmp[5] + tmp[6] + tmp[7]) as f32;
            // `echelle_bloc` est un appel par bloc (152 par ligne de 4 864) :
            // le coût est négligeable devant les 32 multiplications.
            sum += a * self.echelle_bloc(o, b, n_bloc);
        }
        sum
    }
}

#[cfg(test)]
mod tests_q4 {
    use super::*;

    fn melange(n: usize, graine: u64) -> Vec<f32> {
        let mut s = graine;
        (0..n).map(|_| {
            s = s.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
            ((s >> 33) as f64 / (1u64 << 31) as f64 - 1.0) as f32
        }).collect()
    }

    #[test]
    fn avx2_egale_scalaire() {
        for &(n_out, n_in) in &[(4usize, 64usize), (7, 96), (3, 32), (5, 160)] {
            let w = melange(n_out * n_in, 12345);
            let d = DenseQ4::build(&w, n_out, n_in);
            let x: Vec<i32> = (0..n_in).map(|i| ((i * 37) % 255) as i32 - 127).collect();
            let x16: Vec<i16> = x.iter().map(|&v| v as i16).collect();
            for o in 0..n_out {
                let a = d.dot(o, &x);
                let b = d.dot16(o, &x16);
                assert_eq!(a.to_bits(), b.to_bits(),
                           "rang {o} ({n_out}×{n_in}) : scalaire {a} vs avx2 {b}");
            }
        }
    }
}

#[cfg(test)]
mod tests_mxfp4 {
    use super::*;

    /// Le format MXFP4 doit s'importer **exactement** : les magnitudes E2M1
    /// doublées sont entières et l'échelle de bloc est une puissance de deux.
    /// Toute erreur ici serait une requantification déguisée.
    #[test]
    fn import_exact() {
        let (n_out, n_in) = (3usize, 64usize);
        let nl = n_in / 32;                     // 2 blocs par ligne
        let mut buf = vec![0u8; n_out * nl * 17];
        let mut attendu = vec![0f64; n_out * n_in];
        let kv = [0.0f64, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0,
                  0.0, -0.5, -1.0, -1.5, -2.0, -3.0, -4.0, -6.0];
        for o in 0..n_out {
            for b in 0..nl {
                let p = (o * nl + b) * 17;
                let e = 120 + ((o + b) % 12) as u8;   // exposants variés
                buf[p] = e;
                let d = (2f64).powi(e as i32 - 127);
                for j in 0..16 {
                    let bas = ((o * n_out + 0) as u8).wrapping_add((j * 7 + o * 3 + b * 5) as u8);
                    let lo = bas & 0x0F;
                    let hi = (bas >> 1) & 0x0F;
                    buf[p + 1 + j] = lo | (hi << 4);
                    attendu[o * n_in + b * 32 + j] = kv[lo as usize] * d;
                    attendu[o * n_in + b * 32 + 16 + j] = kv[hi as usize] * d;
                }
            }
        }
        let d4 = DenseQ4::import_mxfp4(&buf, n_out, n_in, nl);
        let x: Vec<i32> = (0..n_in).map(|i| ((i * 29) % 200) as i32 - 100).collect();
        let x16: Vec<i16> = x.iter().map(|&v| v as i16).collect();
        for o in 0..n_out {
            let ref_sum: f64 = (0..n_in).map(|i| attendu[o * n_in + i] * x[i] as f64).sum();
            let got = d4.dot(o, &x) as f64;
            let rel = (got - ref_sum).abs() / ref_sum.abs().max(1e-9);
            assert!(rel < 1e-5, "rang {o} : {got} contre {ref_sum} (rel {rel:e})");
            assert_eq!(d4.dot(o, &x).to_bits(), d4.dot16(o, &x16, &sommes32(&x16)).to_bits(),
                       "AVX2 et scalaire doivent être identiques au rang {o}");
        }
    }
}

/// Sommes des activations par bloc de 32, calculées une fois par appel : le
/// terme de minimum de Q4_K en a besoin pour **chaque ligne de sortie**, donc
/// le recalculer dans le noyau coûterait 4 864 fois le même travail.
pub fn sommes32(x: &[i16]) -> Vec<i32> {
    x.chunks(BLOC_Q4).map(|c| c.iter().map(|&v| v as i32).sum()).collect()
}

/// Somme des produits de 32 valeurs 8 bits **non signées** par 32 i16.
/// `a` porte les valeurs 0–15, `b` les 16 suivantes.
#[cfg(target_arch = "x86_64")]
#[inline]
#[target_feature(enable = "avx2")]
unsafe fn somme_produits(a: std::arch::x86_64::__m128i,
                         b: std::arch::x86_64::__m128i,
                         x: *const i16) -> i32 {
    use std::arch::x86_64::*;
    let va = _mm256_cvtepu8_epi16(a);
    let vb = _mm256_cvtepu8_epi16(b);
    let xa = _mm256_loadu_si256(x as *const __m256i);
    let xb = _mm256_loadu_si256(x.add(16) as *const __m256i);
    let p = _mm256_add_epi32(_mm256_madd_epi16(va, xa), _mm256_madd_epi16(vb, xb));
    let mut t = [0i32; 8];
    _mm256_storeu_si256(t.as_mut_ptr() as *mut __m256i, p);
    t[0] + t[1] + t[2] + t[3] + t[4] + t[5] + t[6] + t[7]
}
