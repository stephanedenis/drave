//! Le placement des opérateurs — la règle de coût, **mesurée**.
//!
//! La vision (axe 2) : « on place un opérateur là où son flux coûte le moins
//! cher ». Cet axe était réglé par des `if` codés en dur et des seuils choisis
//! à la main ; ce module porte la **règle** et ses constantes mesurées
//! (`reports/rapport-placement-kv-8k.md`) :
//!
//! | support | bande mesurée | ce qu'on y met |
//! |---|---:|---|
//! | VRAM | 84,9 Go/s | le KV au-delà de ~2-4 k jetons, l'attention, la tête |
//! | RAM | 22,5 Go/s | les poids (mmap, non copiés), le KV court |
//! | NVMe | 3,5 Go/s | les poids qui ne tiennent pas en RAM (streaming) |
//! | réseau | 0,25 Mbit/s | les activations seules (jamais les poids) |
//!
//! Le coût d'un opérateur est **ses octets lus par jeton divisés par la bande
//! du support** ; le placement est le minimum sous la contrainte de place. La
//! mesure du 24/10 valide la première ligne : le KV en VRAM donne ×1,93 sur le
//! préremplissage à 8 k et ×5,8 sur l'attention.

/// La bande passante mesurée de la VRAM (Go/s → octets/s).
pub const BANDE_VRAM: f64 = 84.9e9;
/// La bande passante mesurée de la RAM.
pub const BANDE_RAM: f64 = 22.5e9;
/// La bande passante mesurée du NVMe (lecture en flux).
pub const BANDE_NVME: f64 = 3.5e9;
/// Le débit mesuré du réseau (0,25 Mbit/s).
pub const BANDE_RESEAU: f64 = 0.25e6 / 8.0;
/// La réserve de VRAM à laisser libre (le contexte CUDA, les noyaux).
pub const RESERVE_VRAM: u64 = 1 << 30;

/// Les quatre supports de la règle, du plus rapide au plus lent.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Support {
    Vram,
    Ram,
    Nvme,
    Reseau,
}

impl Support {
    /// La bande passante mesurée du support, en octets par seconde.
    pub fn bande(self) -> f64 {
        match self {
            Support::Vram => BANDE_VRAM,
            Support::Ram => BANDE_RAM,
            Support::Nvme => BANDE_NVME,
            Support::Reseau => BANDE_RESEAU,
        }
    }

    /// Le nom du support, pour les messages.
    pub fn nom(self) -> &'static str {
        match self {
            Support::Vram => "VRAM",
            Support::Ram => "RAM",
            Support::Nvme => "NVMe",
            Support::Reseau => "réseau",
        }
    }
}

/// Le coût d'un opérateur sur un support : ses octets par jeton divisés par la
/// bande du support (en secondes par jeton).
pub fn cout(octets_par_jeton: u64, support: Support) -> f64 {
    octets_par_jeton as f64 / support.bande()
}

/// Les supports classés par coût croissant pour un opérateur donné.
pub fn classement(octets_par_jeton: u64) -> [Support; 4] {
    let mut s = [Support::Vram, Support::Ram, Support::Nvme, Support::Reseau];
    s.sort_by(|a, b| cout(octets_par_jeton, *a)
        .partial_cmp(&cout(octets_par_jeton, *b)).unwrap());
    s
}

/// Le cache KV va-t-il en VRAM ? Oui s'il y tient **avec la réserve** ; sinon il
/// reste en RAM. C'est la règle qui remplace le `if` muet : elle nomme ses
/// constantes et son critère, et la mesure du 24/10 lui donne sa première ligne.
pub fn kv_en_vram(octets_kv: u64, vram_libre: u64) -> bool {
    octets_kv.saturating_add(RESERVE_VRAM) <= vram_libre
}

/// Le support choisi pour un opérateur : le **moins cher où il tient**.
///
/// C'est la règle de l'axe 2 appliquée à un opérateur quelconque (le KV, les
/// experts, la tête) : on parcourt les supports par coût croissant et on prend
/// le premier qui a la place. `octets_par_jeton` est la lecture par jeton (ce
/// qui décide du coût), `octets_total` ce qu'il faut loger (ce qui décide de la
/// place).
pub fn choisir(octets_par_jeton: u64, octets_total: u64,
               libre_vram: u64, libre_ram: u64) -> Support {
    for s in classement(octets_par_jeton) {
        let tient = match s {
            Support::Vram => octets_total.saturating_add(RESERVE_VRAM) <= libre_vram,
            Support::Ram => octets_total <= libre_ram,
            Support::Nvme | Support::Reseau => true,
        };
        if tient {
            return s;
        }
    }
    Support::Nvme
}

/// Une précision et **son coût mesuré** : les octets par valeur et la perte de
/// perplexité observée (en %). Les trois chiffres viennent des mesures du 24/10.
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Precision {
    pub nom: &'static str,
    pub octets_par_valeur: f64,
    pub perte_ppl: f64,
}

/// Le f32 : la référence, aucune perte.
pub const F32: Precision = Precision { nom: "f32", octets_par_valeur: 4.0, perte_ppl: 0.0 };
/// L'int8 sur les couches **tardives** : **+0,03 %** (mesuré sur le 0,5 B, 255 jetons).
pub const INT8_TARDIF: Precision = Precision { nom: "int8 tardif", octets_par_valeur: 1.0, perte_ppl: 0.03 };
/// L'int4 sur les couches **tardives** : **+2,7 %** (elles tolèrent le 8, pas le 4).
pub const INT4_TARDIF: Precision = Precision { nom: "int4 tardif", octets_par_valeur: 0.5, perte_ppl: 2.7 };
/// La **tête** en 4 bits : **+10 %** de PPL — mesuré, puis **reverté**. Elle
/// « tenait » en VRAM : la place n'est pas la qualité.
pub const TETE_4BIT: Precision = Precision { nom: "tête 4 bits", octets_par_valeur: 0.5, perte_ppl: 10.0 };
/// L'int4 **global** : **+364 %** — hors de tout budget raisonnable.
pub const INT4_GLOBAL: Precision = Precision { nom: "int4 global", octets_par_valeur: 0.5, perte_ppl: 364.0 };

/// Les précisions connues, de la plus chère (en octets) à la moins chère.
pub const PRECISIONS: [Precision; 5] = [F32, INT8_TARDIF, INT4_TARDIF, TETE_4BIT, INT4_GLOBAL];

/// Choisit **(support, précision)** : le moins cher **dont la perte tient dans
/// le budget** et qui a la place.
///
/// C'est la leçon de la tête, en code : `choisir` seul répond à « où ça tient » ;
/// ici on répond à « où ça tient **sans payer plus que `perte_max`** ». Un 4 bits
/// qui tient en VRAM mais coûte +10 % de PPL est **refusé** si le budget est plus
/// bas — c'est la décision que le 24/10 a dû prendre à la main, puis reverte.
pub fn choisir_avec_perte(
    octets_par_jeton_f32: u64,
    octets_total_f32: u64,
    libre_vram: u64,
    libre_ram: u64,
    perte_max: f64,
) -> Option<(Support, Precision)> {
    let mut meilleur: Option<(Support, Precision, f64)> = None;
    for p in PRECISIONS {
        if p.perte_ppl > perte_max {
            continue;
        }
        let f = p.octets_par_valeur / 4.0;
        let octets_par_jeton = (octets_par_jeton_f32 as f64 * f) as u64;
        let octets_total = (octets_total_f32 as f64 * f) as u64;
        let sup = choisir(octets_par_jeton, octets_total, libre_vram, libre_ram);
        let c = cout(octets_par_jeton, sup);
        if meilleur.map_or(true, |(_, _, cm)| c < cm) {
            meilleur = Some((sup, p, c));
        }
    }
    meilleur.map(|(s, p, _)| (s, p))
}

// --- La tête : son format est celui du fichier, pas une requantification -----
//
// La mesure du 18/11 (`reports/rapport-a2.6-reconnaissance.md` § 3.4) : la tête
// Q8_0 du fichier, posée en VRAM, donne la **même** perplexité qu'en RAM
// (56,7642 = 56,7642) et passe de 7,43 à 1,80 ms/jeton. Ce n'est pas un choix de
// précision : le fichier est déjà quantifié, on ne choisit que la **place**. La
// table `PRECISIONS` reste donc la carte des **requantifications** d'un opérateur
// f32 (budget nul ⇒ f32) ; la tête a ses entrées à part, à perte nulle.

/// La tête **telle que le fichier la stocke**, en Q8_0 : 34 octets par bloc de
/// 32 poids (une échelle f16 + 32 quants), soit **1,0625 octet par valeur**.
/// Mesurée en VRAM à perte nulle (voir ci-dessus) : aucune requantification.
pub const TETE_Q8_0: Precision = Precision {
    nom: "tête Q8_0",
    octets_par_valeur: 34.0 / 32.0,
    perte_ppl: 0.0,
};

/// La tête en **Q6_K** : 210 octets par super-bloc de 256 poids (128 + 64 + 16
/// quants, 2 octets d'échelle), soit **0,8203 octet par valeur**. C'est le format
/// des têtes liées des Qwen en Q4_K_M (`model.rs:4855`) ; le gain VRAM n'a été
/// mesuré qu'en Q8_0 — Q6_K est à **rejouer** avant d'être cité comme mesuré.
pub const TETE_Q6_K: Precision = Precision {
    nom: "tête Q6_K",
    octets_par_valeur: 210.0 / 256.0,
    perte_ppl: 0.0,
};

/// La précision de la tête lue du **type ggml** du tenseur (`GGML_F32`,
/// `GGML_Q8_0`, `GGML_Q6_K`). Ces entrées décrivent le **format du fichier** :
/// placer ne requantifie pas, d'où la perte nulle. `None` pour un type **sans
/// entrée** : la règle ne devine ni les octets ni la perte, l'appelant garde son
/// défaut. La **requantification** 4 bits, elle, reste `TETE_4BIT` (+10 % mesurés).
#[allow(dead_code)] // pas encore branché : le câblage est la tâche A2.6 suivante
pub fn precision_tete(type_ggml: u32) -> Option<Precision> {
    use crate::gguf::{GGML_F32, GGML_Q6_K, GGML_Q8_0};
    match type_ggml {
        GGML_F32 => Some(F32),
        GGML_Q8_0 => Some(TETE_Q8_0),
        GGML_Q6_K => Some(TETE_Q6_K),
        _ => None,
    }
}

/// Place la **tête dans le format du fichier** : le support le moins cher où elle
/// tient, à condition que sa perte tienne dans `perte_max` (0 = exiger une tête
/// qui ne coûte rien à la PPL). La tête est lue **en entier** à chaque jeton, un
/// seul lecteur : ses octets par jeton valent ses octets totaux.
///
/// Un `perte_max` **négatif** refuse la tête, même sans perte : le budget est un
/// plafond, jamais un plancher implicite. C'est la garde qui empêche un appelant
/// de « gagner » une place en payant une perte qu'il n'a pas déclarée.
#[allow(dead_code)] // pas encore branché : le câblage est la tâche A2.6 suivante
pub fn choisir_tete(
    type_ggml: u32,
    nb_valeurs: u64,
    libre_vram: u64,
    libre_ram: u64,
    perte_max: f64,
) -> Option<(Support, Precision)> {
    let p = precision_tete(type_ggml)?;
    if p.perte_ppl > perte_max {
        return None;
    }
    let octets = (nb_valeurs as f64 * p.octets_par_valeur) as u64;
    Some((choisir(octets, octets, libre_vram, libre_ram), p))
}

/// La perte **mesurée** de l'int8 sur le KV selon la couche (A5.3, 0,5 B, 255 jetons) :
/// **+2,28 %** sur les premières, **+0,03 %** sur les dernières. La frontière mesurée
/// est la moitié du réseau (les couches 0-11 contre 12-23 sur 24).
pub fn perte_kv_int8(couche: usize, n_layer: usize) -> f64 {
    if n_layer == 0 || couche * 2 < n_layer { 2.28 } else { 0.03 }
}

/// La précision du KV choisie par la règle **place et perte** : l'int8 si sa perte
/// mesurée tient dans le budget (`budget_pct` en %), le f32 sinon. C'est
/// `DRAVE_KV_BITS_COUCHES="12-23:8"` **calculé** au lieu d'être écrit — la leçon de
/// la tête (le 4 bits « qui tient » coûte +10 % de PPL) appliquée au KV.
pub fn kv_precision(couche: usize, n_layer: usize, budget_pct: f64) -> (u32, f64) {
    let perte = perte_kv_int8(couche, n_layer);
    if perte <= budget_pct { (8, perte) } else { (32, 0.0) }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn la_vram_est_le_support_le_moins_cher_pour_un_gros_lecteur() {
        // Un KV de 1 M de jetons sur un 0,5 B : ~100 Mo lus par jeton.
        let octets = 100 * 1024 * 1024u64;
        let c = classement(octets);
        assert_eq!(c[0], Support::Vram);
        assert_eq!(c[3], Support::Reseau);
        assert!(cout(octets, Support::Vram) < cout(octets, Support::Ram));
    }

    #[test]
    fn le_kv_tient_si_la_reserve_est_respectee() {
        assert!(kv_en_vram(4 << 30, 8 << 30));
        assert!(kv_en_vram(7 << 30, 8 << 30));      // 7 + 1 = 8 : la réserve tient juste
        assert!(!kv_en_vram(8 << 30, 8 << 30));     // 8 + 1 > 8
        assert!(!kv_en_vram((7 << 30) + 1, 8 << 30));
    }

    #[test]
    fn choisir_respecte_la_place() {
        // Le KV d'un contexte de 1 M (~25 Go) ne tient pas en VRAM (16 Go) : RAM.
        assert_eq!(choisir(25 << 30, 25 << 30, 16 << 30, 64 << 30), Support::Ram);
        // Un petit KV (100 Mo) va en VRAM.
        assert_eq!(choisir(100 << 20, 100 << 20, 4 << 30, 64 << 30), Support::Vram);
        // Rien ne tient (200 Go pour 64 Go de RAM) : le NVMe.
        assert_eq!(choisir(1 << 30, 200 << 30, 16 << 30, 64 << 30), Support::Nvme);
    }

    #[test]
    fn la_perte_decide_aussi() {
        // Le KV tardif : l'int8 (+0,03 %) passe un budget de 1 % ; l'int4 (+2,7 %) non.
        let (_, p8) = choisir_avec_perte(100 << 20, 100 << 20, 4 << 30, 64 << 30, 1.0).unwrap();
        assert_eq!(p8.nom, "int8 tardif");
        let (_, p4) = choisir_avec_perte(100 << 20, 100 << 20, 4 << 30, 64 << 30, 5.0).unwrap();
        assert_eq!(p4.nom, "int4 tardif");
        assert!(p4.octets_par_valeur < p8.octets_par_valeur);
    }

    #[test]
    fn un_budget_nul_interdit_toute_quantification() {
        let (_, p0) = choisir_avec_perte(100 << 20, 100 << 20, 4 << 30, 64 << 30, 0.0).unwrap();
        assert_eq!(p0.nom, "f32");
    }

    #[test]
    fn la_tete_en_4_bits_est_refusee_par_un_budget_de_5_pour_cent() {
        // +10 % de PPL : elle « tient », mais la place n'est pas la qualité.
        let choisi = choisir_avec_perte(100 << 20, 100 << 20, 4 << 30, 64 << 30, 5.0).unwrap();
        assert_ne!(choisi.1.nom, "tête 4 bits");
        // Et l'int4 global (+364 %) ne passe aucun budget raisonnable.
        let encore = choisir_avec_perte(100 << 20, 100 << 20, 4 << 30, 64 << 30, 10.0).unwrap();
        assert_ne!(encore.1.nom, "int4 global");
    }

    #[test]
    fn la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle() {
        // La mesure de la reconnaissance (18/11, § 3.4) : tête Q8_0 en VRAM, même
        // PPL qu'en RAM (56,7642 = 56,7642), 7,43 → 1,80 ms/jeton. La règle ne doit
        // donc pas déplacer la tête Q8_0 : elle la pose où le f32 se poserait.
        let n = 151_936u64 * 896;               // la tête d'un 0,5 B (vocab × caché)
        let octets_f32 = n * 4;

        // La référence : le f32 à budget nul, par la règle générique.
        let (sup_f32, p_f32) = choisir_avec_perte(octets_f32, octets_f32, 16 << 30, 64 << 30, 0.0)
            .unwrap();
        assert_eq!(p_f32, F32);

        // En f32, le nouveau chemin rend EXACTEMENT la réponse du chemin générique :
        // il ne réinvente pas le placement.
        assert_eq!(
            choisir_tete(crate::gguf::GGML_F32, n, 16 << 30, 64 << 30, 0.0),
            choisir_avec_perte(octets_f32, octets_f32, 16 << 30, 64 << 30, 0.0)
        );

        // La tête Q8_0 : la même place que la référence, perte nulle, et le bon
        // format du fichier (8 bits utiles + l'échelle de bloc).
        let (sup_q8, p_q8) =
            choisir_tete(crate::gguf::GGML_Q8_0, n, 16 << 30, 64 << 30, 0.0).unwrap();
        assert_eq!(p_q8, TETE_Q8_0);
        assert_eq!(p_q8.perte_ppl, 0.0);
        assert_eq!(sup_q8, sup_f32);
        assert_eq!(p_q8.octets_par_valeur, 34.0 / 32.0);

        // Q6_K : encore moins d'octets, même perte déclarée — le format des têtes
        // liées des Qwen en Q4_K_M.
        assert_eq!(TETE_Q6_K.octets_par_valeur, 210.0 / 256.0);
        assert!(TETE_Q6_K.octets_par_valeur < TETE_Q8_0.octets_par_valeur);

        // Un budget négatif refuse la tête, même sans perte : le plafond est un
        // plafond. Sans cette garde, `perte_max = -0.1` gagnerait de la place.
        assert_eq!(
            choisir_tete(crate::gguf::GGML_Q8_0, n, 16 << 30, 64 << 30, -0.1),
            None
        );

        // Contrôle négatif : un type sans entrée (Q4_K) rend None — la règle
        // ne devine pas les octets d'un format qu'elle ne porte pas.
        assert_eq!(
            choisir_tete(crate::gguf::GGML_Q4_K, n, 16 << 30, 64 << 30, 0.0),
            None
        );
    }

    #[test]
    fn la_regle_place_perte_choisit_le_kv_par_couche() {
        // 24 couches : l'int8 passe sur les 12-23 (+0,03 %), pas sur les 0-11 (+2,28 %).
        assert_eq!(kv_precision(0, 24, 1.0).0, 32);
        assert_eq!(kv_precision(11, 24, 1.0).0, 32);
        assert_eq!(kv_precision(12, 24, 1.0).0, 8);
        assert_eq!(kv_precision(23, 24, 1.0).0, 8);
        // Un budget de 3 % laisse passer les deux.
        assert_eq!(kv_precision(0, 24, 3.0).0, 8);
        // Un budget nul interdit tout.
        assert_eq!(kv_precision(23, 24, 0.0).0, 32);
    }

    #[test]
    fn le_cout_est_proportionnel_aux_octets() {
        let a = cout(1 << 20, Support::Ram);
        let b = cout(2 << 20, Support::Ram);
        assert!((b - 2.0 * a).abs() < 1e-15);
    }
}
