//! Trace GLOBALE d'une exécution répartie — ce qui a traversé chaque lien, pas à pas.
//!
//! POURQUOI CE MODULE (docs/plan-cerveau-complet.md, capacité C12). Une exécution
//! répartie n'est aujourd'hui observable que par ce que chaque processus imprime :
//! quand un graphe de régions donnera un résultat faux, il n'y aura aucun moyen de
//! savoir **quel pas et quel lien** ont divergé. La trace globale est ce moyen, et
//! sa porte est une égalité : **rejouer l'exécution doit retrouver la trace, pas à
//! pas** — toute divergence est signalée avec son pas et son lien.
//!
//! CE QUI EST ENREGISTRÉ, ET CE QUI NE L'EST PAS. Par croisement : la région, le pas,
//! le lien, le nombre de valeurs, une **empreinte** des valeurs (FNV-1a sur leurs
//! octets, donc **au bit près** — pas d'epsilon, pas d'arrondi) et l'horodatage.
//! Les VALEURS elles-mêmes ne sont pas stockées : une trace de 128 pas × 2 liens ×
//! 896 flottants ferait 900 Ko pour un 0,5 B, et des gigaoctets pour un modèle de
//! production. La trace dit **où** regarder ; le rejeu recompte et compare.
//!
//! FORMAT (texte, une ligne par croisement, diffable et lisible) :
//!
//! ```text
//! # drave trace globale v1 · <date>
//! region  pas  lien  n  empreinte  ms
//! local   0    local->pair   896  0x1f3c...  0.412
//! pair    0    pair->local   896  0x99ab...  5.107
//! ```

use std::io::Write;
use std::path::Path;

/// FNV-1a 64 bits sur les octets d'un tableau de `f32`.
///
/// POURQUOI FNV ET PAS UN HACHAGE CRYPTOGRAPHIQUE : la trace n'a pas à résister à
/// un adversaire, elle doit être **déterministe, exacte et sans dépendance** (le
/// crate est std seul). FNV-1a suffit à distinguer deux états qui diffèrent d'un
/// bit, et c'est tout ce qu'on lui demande.
pub fn empreinte(valeurs: &[f32]) -> u64 {
    let mut h: u64 = 0xcbf2_9ce4_8422_2325;
    for v in valeurs {
        for o in v.to_le_bytes() {
            h ^= o as u64;
            h = h.wrapping_mul(0x100_0000_01b3);
        }
    }
    h
}

#[derive(Debug, Clone, PartialEq)]
pub struct Croisement {
    pub region: String,
    pub pas: u32,
    pub lien: String,
    pub n: usize,
    pub empreinte: u64,
    pub ms: f64,
}

#[derive(Debug, Default)]
pub struct TraceGlobale {
    lignes: Vec<Croisement>,
}

impl TraceGlobale {
    pub fn nouvelle() -> Self { TraceGlobale { lignes: Vec::new() } }

    pub fn enregistrer(&mut self, region: &str, pas: u32, lien: &str, valeurs: &[f32], ms: f64) {
        self.lignes.push(Croisement {
            region: region.to_string(), pas, lien: lien.to_string(),
            n: valeurs.len(), empreinte: empreinte(valeurs), ms,
        });
    }

    pub fn len(&self) -> usize { self.lignes.len() }
    /// Les croisements enregistrés — pour comparer une exécution fraîche à une
    /// trace relue, sans passer par un fichier intermédiaire.
    pub fn lignes_pub(&self) -> Vec<Croisement> { self.lignes.clone() }
    pub fn est_vide(&self) -> bool { self.lignes.is_empty() }

    /// Écrit la trace. Le fichier porte son en-tête : une trace sans sa version ni
    /// sa date ne se relit pas six mois plus tard.
    pub fn ecrire(&self, chemin: &str) -> std::io::Result<()> {
        let mut f = std::fs::File::create(chemin)?;
        writeln!(f, "# drave trace globale v1 · {} croisements", self.lignes.len())?;
        writeln!(f, "# region pas lien n empreinte ms")?;
        for c in &self.lignes {
            writeln!(f, "{} {} {} {} {:#018x} {:.3}",
                     c.region, c.pas, c.lien, c.n, c.empreinte, c.ms)?;
        }
        f.flush()
    }

    /// Relit une trace et rend ses croisements. Une ligne illisible est une ERREUR :
    /// une trace à moitié lue ferait croire à une divergence qui n'existe pas.
    pub fn lire(chemin: &str) -> Result<Vec<Croisement>, String> {
        let texte = std::fs::read_to_string(chemin)
            .map_err(|e| format!("trace : lecture de {chemin} impossible : {e}"))?;
        let mut out = Vec::new();
        for (n, l) in texte.lines().enumerate() {
            let l = l.trim();
            if l.is_empty() || l.starts_with('#') { continue; }
            let champs: Vec<&str> = l.split_whitespace().collect();
            if champs.len() != 6 {
                return Err(format!("trace : ligne {} illisible (6 champs attendus, {} trouvés) : \
« {l} »", n + 1, champs.len()));
            }
            let nombre = |s: &str, quoi: &str| -> Result<u64, String> {
                s.parse::<u64>().map_err(|_| format!("trace : {quoi} illisible ligne {} : « {s} »", n + 1))
            };
            out.push(Croisement {
                region: champs[0].to_string(),
                pas: nombre(champs[1], "pas")? as u32,
                lien: champs[2].to_string(),
                n: nombre(champs[3], "n")? as usize,
                empreinte: u64::from_str_radix(champs[4].trim_start_matches("0x"), 16)
                    .map_err(|_| format!("trace : empreinte illisible ligne {}", n + 1))?,
                ms: champs[5].parse().unwrap_or(0.0),
            });
        }
        Ok(out)
    }

    /// Vérifie une trace : compare les croisements enregistrés à ceux d'une
    /// exécution fraîche, dans l'ordre. Rend `Ok(nb)` si tout concorde, et l'écart
    /// **avec son pas et son lien** sinon — c'est tout l'intérêt : savoir OÙ.
    pub fn verifier(reference: &[Croisement], fraiche: &[Croisement]) -> Result<usize, String> {
        if reference.len() != fraiche.len() {
            return Err(format!("rejeu : {} croisements attendus, {} obtenus — l'exécution \
n'a pas suivi le même chemin (régions ou liens différents)",
                                reference.len(), fraiche.len()));
        }
        for (i, (a, b)) in reference.iter().zip(fraiche.iter()).enumerate() {
            if a.region != b.region || a.pas != b.pas || a.lien != b.lien || a.n != b.n {
                return Err(format!("rejeu : divergence au croisement {i} — attendu {} pas {} \
sur « {} » ({} valeurs), obtenu {} pas {} sur « {} » ({} valeurs)",
                                   a.region, a.pas, a.lien, a.n, b.region, b.pas, b.lien, b.n));
            }
            if a.empreinte != b.empreinte {
                return Err(format!("rejeu : DIVERGENCE AU BIT PRÈS au croisement {i} — \
région « {} », pas {}, lien « {} » : empreinte {:#018x} attendue, {:#018x} obtenue",
                                   a.region, a.pas, a.lien, a.empreinte, b.empreinte));
            }
        }
        Ok(reference.len())
    }
}

/// Écrit la trace si un chemin est donné, et ne dit rien sinon.
pub fn ecrire_si(trace: &TraceGlobale, chemin: &Option<String>) -> bool {
    match chemin {
        Some(f) => match trace.ecrire(f) {
            Ok(()) => { println!("[trace] {} croisements écrits dans {f}", trace.len()); true }
            Err(e) => { eprintln!("[trace] écriture de {f} impossible : {e}"); false }
        },
        None => false,
    }
}

/// Vrai si le chemin existe et est lisible — utilisé par le mode vérification.
pub fn existe(chemin: &str) -> bool { Path::new(chemin).is_file() }

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn empreinte_change_avec_un_bit() {
        let a = [1.0f32, 2.0];
        let mut b = a;
        b[1] = f32::from_bits(2.0f32.to_bits() ^ 1); // un seul bit de différence
        assert_ne!(empreinte(&a), empreinte(&b), "un bit doit suffire à changer l'empreinte");
        assert_eq!(empreinte(&a), empreinte(&a));
    }

    #[test]
    fn allez_retour_ecriture_lecture() {
        let mut t = TraceGlobale::nouvelle();
        t.enregistrer("local", 0, "local->pair", &[1.0, 2.0, 3.0], 0.4);
        t.enregistrer("pair", 0, "pair->local", &[4.0, 5.0], 5.1);
        let f = std::env::temp_dir().join("essai_trace_globale.txt");
        let chemin = f.to_str().unwrap().to_string();
        t.ecrire(&chemin).unwrap();
        let relu = TraceGlobale::lire(&chemin).unwrap();
        assert_eq!(relu.len(), 2);
        assert_eq!(relu[0].region, "local");
        assert_eq!(relu[0].n, 3);
        assert_eq!(relu[1].lien, "pair->local");
        assert_eq!(relu[0].empreinte, empreinte(&[1.0, 2.0, 3.0]));
        let _ = std::fs::remove_file(&chemin);
    }

    #[test]
    fn verifier_detecte_la_divergence_et_la_nomme() {
        let mut a = TraceGlobale::nouvelle();
        a.enregistrer("local", 0, "local->pair", &[1.0, 2.0], 0.0);
        a.enregistrer("local", 1, "local->pair", &[3.0, 4.0], 0.0);
        let mut b = TraceGlobale::nouvelle();
        b.enregistrer("local", 0, "local->pair", &[1.0, 2.0], 0.0);
        b.enregistrer("local", 1, "local->pair", &[3.0, 4.5], 0.0); // un pas différent
        let e = TraceGlobale::verifier(&a.lignes, &b.lignes).unwrap_err();
        assert!(e.contains("DIVERGENCE AU BIT PRÈS"), "{e}");
        assert!(e.contains("pas 1"), "{e}");
        assert!(e.contains("local->pair"), "{e}");
        // et l'égalité stricte passe
        assert_eq!(TraceGlobale::verifier(&a.lignes, &a.lignes).unwrap(), 2);
    }

    #[test]
    fn refuse_une_trace_tronquee_ou_bruitee() {
        let f = std::env::temp_dir().join("essai_trace_bruitee.txt");
        std::fs::write(&f, "# en-tête\nlocal 0 local->pair 3\n").unwrap();
        let e = TraceGlobale::lire(f.to_str().unwrap()).unwrap_err();
        assert!(e.contains("illisible"), "{e}");
        let _ = std::fs::remove_file(&f);
    }

    #[test]
    fn refuse_un_chemin_different() {
        let mut a = TraceGlobale::nouvelle();
        a.enregistrer("local", 0, "local->pair", &[1.0], 0.0);
        let mut b = TraceGlobale::nouvelle();
        b.enregistrer("local", 0, "local->pair", &[1.0], 0.0);
        b.enregistrer("pair", 0, "pair->local", &[2.0], 0.0);
        let e = TraceGlobale::verifier(&a.lignes, &b.lignes).unwrap_err();
        assert!(e.contains("n'a pas suivi le même chemin"), "{e}");
    }
}
