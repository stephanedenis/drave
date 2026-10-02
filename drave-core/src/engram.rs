//! L'**engram** de DeepSeek-V4.1 : deux tables de n-grammes adressées par hachage.
//!
//! Le moteur ne les *calcule* pas encore — il les **adresse**. Ce module porte
//! la partie qui décide **quelle rangée lire**, et rien d'autre : c'est la
//! « liste d'adresses » du plan, celle qu'on peut tracer, compter et comparer
//! avant de savoir lire les rangées.
//!
//! La référence est un portage 1:1 de `vllm/models/deepseek_v4_1/common/engram.py`
//! (`mudler/vllm.cpp`, `deepseek_v4_1_engram.cpp`) ; `tools/engram_reference.py`
//! en est la transcription Python, et le test de ce module les fait concorder.
//!
//! Trois détails portent tout le comportement, et aucun n'est devinable :
//!
//! 1. le repli se fait par **OU exclusif** (`^=`), pas par somme ;
//! 2. `blocked` est **collant** : dès qu'un n-gramme est cassé (recul avant le
//!    début, jeton mort), tous les reculs PLUS PROFONDS sont remplacés par le
//!    pad — sans quoi un 4-gramme à cheval sur une image hacherait comme si
//!    l'image n'existait pas ;
//! 3. le modulo se fait **par colonne**, avec le premier et l'offset de cette
//!    colonne — pas sur la table entière.
//!
//! Ce que le fichier apporte et qui n'est pas recalculé ici : les 48 premiers
//! (ils *sont* dans les métadonnées, et `tools/engram_reference.py` les
//! recalcule : ils concordent), les 8 multiplicateurs, et la table de
//! correspondance des jetons.

use crate::gguf::Gguf;

/// Le jeton « mort » : masqué (padding d'image, hors séquence). Ce n'est pas un
/// jeton ordinaire, c'est un trou — et il casse le n-gramme comme le ferait un
/// début de séquence.
pub const MORT: i32 = -1;

/// Les **48 premiers** du fichier de V4.1, tels quels. Ils ne sont pas
/// décoratifs : `tools/engram_reference.py` les RECALCULE (Miller-Rabin
/// (2, 7, 61) puis premier suivant non déjà vu, depuis `engram_vocab_size - 1`)
/// et obtient exactement cette liste.
pub const PREMIERS_V41: [i64; 48] = [
    16000057, 16000079, 16000081, 16000097, 16000121, 16000129,
    16000133, 16000183, 16000189, 16000207, 16000211, 16000253,
    16000277, 16000289, 16000307, 16000321, 16000339, 16000381,
    16000393, 16000399, 16000403, 16000409, 16000447, 16000463,
    16000477, 16000487, 16000499, 16000507, 16000511, 16000573,
    16000609, 16000627, 16000667, 16000669, 16000693, 16000697,
    16000711, 16000729, 16000759, 16000769, 16000781, 16000799,
    16000813, 16000819, 16000841, 16000877, 16000879, 16000889,
];


pub struct Engram {
    /// `engram.layer_ids` : les couches qui portent une table (1 et 14).
    pub couches: Vec<usize>,
    /// `engram.rows` : le nombre de rangées de chaque table.
    pub rangees: Vec<i64>,
    /// Les `n_layers × n_hash_cols` premiers, tels que le fichier les donne.
    pub primes: Vec<i64>,
    /// Somme préfixe EXCLUSIVE **dans chaque couche** : la rangée est
    /// `reste + offset`, donc les seaux d'une couche ne se chevauchent pas.
    pub offsets: Vec<i64>,
    /// Un multiplicateur par (couche, recul) : `n_layers × max_ngram`.
    pub multipliers: Vec<i64>,
    /// La correspondance jeton → identifiant compressé (`[0, compressed_vocab)`).
    pub token_map: Vec<i32>,
    pub max_ngram: usize,
    pub n_heads: usize,
    pub compressed_vocab: i64,
    /// Le pad **compressé** (`token_map[engram.pad_id]`) : c'est lui que le
    /// hachage emploie, pas l'identifiant du jeton de pad.
    pub pad: i32,
}

impl Engram {
    /// Lit l'engram des métadonnées, ou `None` si le modèle n'en a pas.
    pub fn depuis_gguf(g: &Gguf) -> Option<Engram> {
        let couches: Vec<usize> = g.cfg_ou(&["engram.layer_ids"])
            .and_then(|m| m.as_liste_i64())?
            .into_iter().map(|v| v as usize).collect();
        if couches.is_empty() { return None; }
        let rangees = g.cfg_ou(&["engram.rows"]).and_then(|m| m.as_liste_i64())?;
        let primes = g.cfg_ou(&["engram.primes"]).and_then(|m| m.as_liste_i64())?;
        let multipliers = g.cfg_ou(&["engram.multipliers"]).and_then(|m| m.as_liste_i64())?;
        let token_map: Vec<i32> = g.cfg_ou(&["engram.token_map"])
            .and_then(|m| m.as_liste_i64())?
            .into_iter().map(|v| v as i32).collect();
        let max_ngram = g.cfg_ou(&["engram.max_ngram_size"])
            .and_then(|m| m.as_u64()).map(|v| v as usize)
            .or_else(|| g.json_nombre("engram_max_ngram_size").map(|v| v as usize))
            .unwrap_or(4);
        let n_heads = g.cfg_ou(&["engram.n_heads"])
            .and_then(|m| m.as_u64()).map(|v| v as usize)
            .or_else(|| g.json_nombre("engram_n_heads").map(|v| v as usize))
            .unwrap_or(8);
        let compressed_vocab = g.cfg_ou(&["engram.compressed_vocab_size"])
            .and_then(|m| m.as_u64()).map(|v| v as i64)
            .or_else(|| g.json_nombre("engram_compressed_vocab_size").map(|v| v as i64))
            .unwrap_or(0);
        let pad_id = g.cfg_ou(&["engram.pad_id"]).and_then(|m| m.as_u64())
            .map(|v| v as usize)
            .or_else(|| g.json_nombre("engram_pad_token_id").map(|v| v as usize))
            .unwrap_or(0);
        let pad = *token_map.get(pad_id)?;
        // Les offsets : somme préfixe exclusive DANS chaque couche.
        let n_hash_cols = (max_ngram - 1) * n_heads;
        let mut offsets = Vec::with_capacity(primes.len());
        for l in 0..couches.len() {
            let mut courant = 0i64;
            for col in 0..n_hash_cols {
                let idx = l * n_hash_cols + col;
                offsets.push(courant);
                courant += *primes.get(idx)?;
            }
        }
        if primes.len() != couches.len() * n_hash_cols
            || multipliers.len() != couches.len() * max_ngram {
            return None;
        }
        Some(Engram { couches, rangees, primes, offsets, multipliers, token_map,
                      max_ngram, n_heads, compressed_vocab, pad })
    }

    pub fn n_hash_cols(&self) -> usize { (self.max_ngram - 1) * self.n_heads }

    /// **La liste d'adresses** : pour chaque jeton, `n_layers × n_hash_cols`
    /// indices de rangée — un par (couche, groupe de recul, tête).
    ///
    /// `positions[i]` est la position du jeton `ids[i]`. Une séquence complète
    /// dans un seul lot (le cas du préremplissage) suffit : le palier
    /// « historique » de la référence ne sert qu'aux décodages incrémentaux.
    pub fn adresses(&self, ids: &[u32], positions: &[usize], morts: &[bool]) -> Vec<i32> {
        let nl = self.couches.len();
        let nhc = self.n_hash_cols();
        let debut = positions.first().copied().unwrap_or(0);
        let mut sortie = vec![0i32; ids.len() * nl * nhc];
        for (token, (&id, &position)) in ids.iter().zip(positions.iter()).enumerate() {
            let mut rolling = vec![0i64; nl];
            let mut blocked = false;
            for shift in 0..self.max_ngram {
                let recul = position as i64 - shift as i64;
                let mut source = self.pad;
                if recul >= debut as i64 {
                    // Le jeton du RECUL, pas le courant : `lookback = position -
                    // shift`, donc l'indice `token - shift`. Lire le jeton
                    // courant (ou retomber sur lui) donne des adresses
                    // parfaitement plausibles — et fausses dès le 2ᵉ jeton.
                    if let Some(i) = token.checked_sub(shift) {
                        let mort = morts.get(i).copied().unwrap_or(false);
                        source = if mort { MORT } else {
                            match ids.get(i).and_then(|j| self.token_map.get(*j as usize)) {
                                Some(v) => *v,
                                None => self.pad,
                            }
                        };
                    }
                }
                // COLLANT, et c'est tout l'intérêt : un 4-gramme à cheval sur un
                // trou vaut le pad, pas « le trou disparaît ».
                blocked = blocked || recul < 0 || source == MORT;
                let valeur = if blocked { self.pad as i64 } else { source as i64 };
                for layer in 0..nl {
                    rolling[layer] ^= valeur * self.multipliers[layer * self.max_ngram + shift];
                    if shift == 0 { continue; }
                    for head in 0..self.n_heads {
                        let col = (shift - 1) * self.n_heads + head;
                        let idx = layer * nhc + col;
                        let rangee = rolling[layer] % self.primes[idx] + self.offsets[idx];
                        sortie[(token * nl + layer) * nhc + col] = rangee as i32;
                    }
                }
            }
        }
        sortie
    }
}

#[cfg(test)]
mod tests {
    //! Concordance avec `tools/engram_reference.py`, transcription du portage
    //! 1:1 de `vllm/models/deepseek_v4_1/common/engram.py`.
    use super::*;

    // Valeurs GÉNÉRÉES par la référence Python — ne pas les retoucher à la main.
    const MULT: [i64; 8] = [3, 5, 7, 11, 13, 17, 19, 23];
    const IDS: [u32; 5] = [5, 6, 7, 8, 9];
    const ADRESSES: [i32; 240] = [
        5, 16000062, 32000141, 48000222, 64000319, 80000440, 96000569, 112000702, 128000891, 144001080, 160001287, 176001498, 192001751, 208002028, 224002317, 240002624, 256002963, 272003302, 288003683, 304004076, 320004475, 336004878, 352005287, 368005734, 99, 16000576, 32001063, 48001562, 64002069, 80002580, 96003153, 112003762, 128004359, 144005026, 160005695, 176006388, 192007085, 208007796, 224008525, 240009284, 256010091, 272010872, 288011671, 304012484, 320013303, 336014144, 352015021, 368015900 ,
        11, 16000068, 32000147, 48000228, 64000325, 80000446, 96000575, 112000708, 128000885, 144001074, 160001281, 176001492, 192001745, 208002022, 224002311, 240002618, 256002953, 272003292, 288003673, 304004066, 320004465, 336004868, 352005277, 368005724, 27, 16000504, 32000991, 48001490, 64001997, 80002508, 96003081, 112003690, 128004351, 144005018, 160005687, 176006380, 192007077, 208007788, 224008517, 240009276, 256010003, 272010784, 288011583, 304012396, 320013215, 336014056, 352014933, 368015812 ,
        11, 16000068, 32000147, 48000228, 64000325, 80000446, 96000575, 112000708, 128000920, 144001109, 160001316, 176001527, 192001780, 208002057, 224002346, 240002653, 256002996, 272003335, 288003716, 304004109, 320004508, 336004911, 352005320, 368005767, 61, 16000538, 32001025, 48001524, 64002031, 80002542, 96003115, 112003724, 128004388, 144005055, 160005724, 176006417, 192007114, 208007825, 224008554, 240009313, 256010060, 272010841, 288011640, 304012453, 320013272, 336014113, 352014990, 368015869 ,
        59, 16000116, 32000195, 48000276, 64000373, 80000494, 96000623, 112000756, 128000897, 144001086, 160001293, 176001504, 192001757, 208002034, 224002323, 240002630, 256002972, 272003311, 288003692, 304004085, 320004484, 336004887, 352005296, 368005743, 31, 16000508, 32000995, 48001494, 64002001, 80002512, 96003085, 112003694, 128004399, 144005066, 160005735, 176006428, 192007125, 208007836, 224008565, 240009324, 256010014, 272010795, 288011594, 304012407, 320013226, 336014067, 352014944, 368015823 ,
        51, 16000108, 32000187, 48000268, 64000365, 80000486, 96000615, 112000748, 128000882, 144001071, 160001278, 176001489, 192001742, 208002019, 224002308, 240002615, 256002998, 272003337, 288003718, 304004111, 320004510, 336004913, 352005322, 368005769, 253, 16000730, 32001217, 48001716, 64002223, 80002734, 96003307, 112003916, 128004410, 144005077, 160005746, 176006439, 192007136, 208007847, 224008576, 240009335, 256010226, 272011007, 288011806, 304012619, 320013438, 336014279, 352015156, 368016035 ,
    ];

    fn engram_de_test() -> Engram {
        // La table de correspondance d'essai est l'identité sur [0, 99 092) :
        // dense, comme celle du fichier (99 092 = compressed_vocab_size).
        let token_map: Vec<i32> = (0..99_092).collect();
        let mut primes = vec![0i64; 48];
        let mut offsets = vec![0i64; 48];
        // Les 48 premiers du fichier (recalculés par la référence, vérifiés
        // identiques) — recopiés ici pour que le test ne dépende pas du GGUF.
        let vrais = PREMIERS_V41;
        primes.copy_from_slice(&vrais);
        for l in 0..2 {
            let mut courant = 0i64;
            for col in 0..24 {
                offsets[l * 24 + col] = courant;
                courant += primes[l * 24 + col];
            }
        }
        Engram { couches: vec![1, 14], rangees: vec![384_006_168, 384_016_682],
                 primes, offsets, multipliers: MULT.to_vec(), token_map,
                 max_ngram: 4, n_heads: 8, compressed_vocab: 99_092, pad: 2 }
    }

    #[test]
    fn adressage_conforme_a_la_reference() {
        let e = engram_de_test();
        let positions: Vec<usize> = (0..IDS.len()).collect();
        let morts = vec![false; IDS.len()];
        let a = e.adresses(&IDS, &positions, &morts);
        assert_eq!(a.len(), ADRESSES.len(), "un jeton × 2 couches × 24 colonnes");
        for (i, (x, y)) in a.iter().zip(ADRESSES.iter()).enumerate() {
            assert_eq!(x, y, "adresse {i} : {x} contre {y}");
        }
    }

    /// Chaque adresse tombe dans le seau de SA colonne : entre l'offset de la
    /// colonne et cet offset plus son premier. C'est ce qui rend les colonnes
    /// lisibles indépendamment — et ce qu'un modulo global casserait.
    #[test]
    fn les_adresses_tombent_dans_leur_seau() {
        let e = engram_de_test();
        let positions: Vec<usize> = (0..IDS.len()).collect();
        let a = e.adresses(&IDS, &positions, &vec![false; IDS.len()]);
        let nhc = e.n_hash_cols();
        for jeton in 0..IDS.len() {
            for layer in 0..2 {
                for col in 0..nhc {
                    let idx = layer * nhc + col;
                    let v = a[(jeton * 2 + layer) * nhc + col] as i64;
                    assert!(v >= e.offsets[idx] && v < e.offsets[idx] + e.primes[idx],
                            "jeton {jeton} couche {layer} col {col} : {v} hors du seau");
                }
            }
        }
    }

    /// **Le repli est COLLANT** : un jeton mort au recul 1 met le pad partout
    /// au-delà, mais laisse le recul 0 intact. Sans cela, un 4-gramme à cheval
    /// sur un trou hacherait comme si le trou n'existait pas.
    #[test]
    fn le_repli_est_collant() {
        let e = engram_de_test();
        let ids = [5u32, 6, 7, 8];
        let pos = [0usize, 1, 2, 3];
        let sans = e.adresses(&ids, &pos, &[false; 4]);
        let avec = e.adresses(&ids, &pos, &[false, true, false, false]);
        // Le jeton 2 (recul 0 intact, recul 1 mort) : ses adresses changent.
        assert_ne!(&sans[2 * 48..3 * 48], &avec[2 * 48..3 * 48]);
        // Et le jeton 0, deux rangs avant le trou, ne bouge pas : le repli ne
        // remonte pas le temps.
        assert_eq!(&sans[0..48], &avec[0..48]);
    }
}
