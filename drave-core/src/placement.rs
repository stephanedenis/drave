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
    fn le_cout_est_proportionnel_aux_octets() {
        let a = cout(1 << 20, Support::Ram);
        let b = cout(2 << 20, Support::Ram);
        assert!((b - 2.0 * a).abs() < 1e-15);
    }
}
