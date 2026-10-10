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
//! # drave trace globale v2 · <n> croisements
//! # source <qui a écrit ce fichier>
//! region  pas  lien  n  empreinte  ms  t_abs  mode
//! local   0    local->pair   896  0x1f3c...  0.412  1759999999.981  0
//! pair    0    pair->local   896  0x99ab...  5.107  1760000000.005  0
//! ```
//!
//! POURQUOI `t_abs` ET `mode` (C12bis). Une exécution répartie écrit plusieurs
//! fichiers — un par processus, un par machine. Les fusionner demande un temps
//! **commun aux deux horloges**, donc mural (epoch) et non une durée locale : `ms`
//! dit combien de temps a pris un croisement, `t_abs` dit QUAND il a eu lieu. Et
//! comparer les deux bouts d'un même lien n'a de sens que si l'encodage était
//! **sans perte** : en mode listes, le nœud reçoit une version quantifiée des
//! valeurs, donc deux empreintes différentes sont **normales** — `mode` permet de le
//! dire au lieu de crier à la divergence. Les traces v1 (6 champs) restent
//! lisibles : elles n'ont simplement pas d'horodatage, et la fusion REFUSE alors de
//! les ordonner plutôt que d'inventer un ordre.

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
    /// Heure murale (secondes epoch) — 0.0 pour une trace v1, qui n'en a pas.
    pub t_abs: f64,
    /// Mode d'encodage du lien : 0 = dense (sans perte), 1/2 = listes, 3/4 = lots.
    /// Une comparaison des deux bouts d'un lien n'a de sens qu'en mode 0.
    pub mode: u8,
}

/// L'heure murale en secondes epoch. POURQUOI PAS `Instant` : `Instant` n'est
/// comparable qu'à l'intérieur d'un processus. Deux nœuds sur deux machines n'ont
/// que l'horloge murale en commun — imparfaite, donc on la mesure au lieu de la
/// supposer (voir `derive_horloges`).
pub fn maintenant() -> f64 {
    std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.as_secs_f64())
        .unwrap_or(0.0)
}

#[derive(Debug, Default)]
pub struct TraceGlobale {
    lignes: Vec<Croisement>,
}

impl TraceGlobale {
    pub fn nouvelle() -> Self { TraceGlobale { lignes: Vec::new() } }

    pub fn enregistrer(&mut self, region: &str, pas: u32, lien: &str, valeurs: &[f32], ms: f64) {
        self.enregistrer_mode(region, pas, lien, valeurs, ms, 0);
    }

    /// Comme `enregistrer`, mais en déclarant le mode d'encodage du lien.
    pub fn enregistrer_mode(&mut self, region: &str, pas: u32, lien: &str, valeurs: &[f32],
                            ms: f64, mode: u8) {
        self.lignes.push(Croisement {
            region: region.to_string(), pas, lien: lien.to_string(),
            n: valeurs.len(), empreinte: empreinte(valeurs), ms,
            t_abs: maintenant(), mode,
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
        self.ecrire_source(chemin, "local")
    }

    /// Écrit la trace en s'attribuant une **source** : c'est ce nom qui rendra la
    /// fusion lisible (« qui a vu ça, et quand »). Deux processus qui écrivent le
    /// même nom rendraient la fusion ambiguë, pas fausse : on le signale à la
    /// lecture, pas ici.
    pub fn ecrire_source(&self, chemin: &str, source: &str) -> std::io::Result<()> {
        let mut f = std::fs::File::create(chemin)?;
        writeln!(f, "# drave trace globale v2 · {} croisements", self.lignes.len())?;
        writeln!(f, "# source {source}")?;
        writeln!(f, "# region pas lien n empreinte ms t_abs mode")?;
        for c in &self.lignes {
            writeln!(f, "{} {} {} {} {:#018x} {:.3} {:.6} {}",
                     c.region, c.pas, c.lien, c.n, c.empreinte, c.ms, c.t_abs, c.mode)?;
        }
        f.flush()
    }

    /// Relit une trace et rend ses croisements. Une ligne illisible est une ERREUR :
    /// une trace à moitié lue ferait croire à une divergence qui n'existe pas.
    pub fn lire(chemin: &str) -> Result<Vec<Croisement>, String> {
        Ok(Self::lire_avec_source(chemin)?.1)
    }

    /// Relit une trace AVEC le nom de sa source (l'en-tête `# source`). Une trace
    /// v1 n'en a pas : elle prend le nom du fichier, ce qui reste vrai et vérifiable.
    pub fn lire_avec_source(chemin: &str) -> Result<(String, Vec<Croisement>), String> {
        let texte = std::fs::read_to_string(chemin)
            .map_err(|e| format!("trace : lecture de {chemin} impossible : {e}"))?;
        let mut source = chemin.to_string();
        let mut out = Vec::new();
        for (n, l) in texte.lines().enumerate() {
            let l = l.trim();
            if l.is_empty() { continue; }
            if let Some(reste) = l.strip_prefix('#') {
                if let Some(s) = reste.trim().strip_prefix("source ") {
                    source = s.trim().to_string();
                }
                continue;
            }
            let champs: Vec<&str> = l.split_whitespace().collect();
            // 6 champs = v1 (pas d'horodatage), 8 = v2. 7 est refusé : c'est une
            // trace tronquée, et deviner le champ manquant serait inventer.
            if champs.len() != 6 && champs.len() != 8 {
                return Err(format!("trace : ligne {} illisible (6 ou 8 champs attendus, {} \
trouvés) : « {l} »", n + 1, champs.len()));
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
                t_abs: if champs.len() == 8 { champs[6].parse().unwrap_or(0.0) } else { 0.0 },
                mode: if champs.len() == 8 { champs[7].parse().unwrap_or(0) } else { 0 },
            });
        }
        Ok((source, out))
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

/// Une ligne fusionnée : d'où elle vient, et ce qu'elle dit.
#[derive(Debug, Clone, PartialEq)]
pub struct Fusion {
    pub source: String,
    pub c: Croisement,
}

/// FUSIONNE plusieurs traces en UNE, ordonnée par le temps mural.
///
/// POURQUOI C'EST LA CAPACITÉ C12bis. Une exécution répartie produit un fichier de
/// trace par processus : jusqu'ici, savoir « quel nœud a vu quoi, et avant quoi »
/// demandait d'ouvrir trois fichiers côte à côte et de comparer des horloges de
/// machines différentes à l'œil. La fusion fait ce travail, et surtout elle REFUSE
/// de le faire quand elle ne peut pas : une trace sans horodatage (v1) ne peut pas
/// être ordonnée par le temps, et l'ordonner par numéro de pas donnerait un ordre
/// qui a l'air d'un ordre sans en être un.
pub fn fusionner(entrees: &[(String, Vec<Croisement>)]) -> Result<Vec<Fusion>, String> {
    if entrees.len() < 2 {
        return Err("fusion : il faut au moins DEUX traces — fusionner une seule trace \
n'apprend rien qu'elle ne dise déjà".to_string());
    }
    for (source, lignes) in entrees.iter() {
        if lignes.is_empty() {
            return Err(format!("fusion : la trace « {source} » est VIDE — une trace vide ne \
prouve pas qu'il ne s'est rien passé, elle prouve qu'on n'a rien enregistré"));
        }
        if lignes.iter().all(|c| c.t_abs == 0.0) {
            return Err(format!("fusion : la trace « {source} » n'a AUCUN horodatage (format \
v1) — on ne peut pas l'ordonner dans le temps, et l'ordonner par numéro de pas donnerait un \
faux ordre. Réécrivez-la avec la version qui horodate."));
        }
    }
    let mut out: Vec<Fusion> = Vec::new();
    for (source, lignes) in entrees.iter() {
        for c in lignes {
            out.push(Fusion { source: source.clone(), c: c.clone() });
        }
    }
    // Ordre TOTAL et déterministe : le temps d'abord, puis la source, puis le pas et
    // le lien. Sans les départages, deux croisements de même horodatage (fréquent :
    // l'horloge murale a une résolution de l'ordre de la microseconde, et deux nœuds
    // peuvent la partager) sortiraient dans un ordre qui dépendrait de l'ordre des
    // fichiers sur la ligne de commande — deux fusions du même ensemble donneraient
    // deux fichiers différents.
    out.sort_by(|a, b| a.c.t_abs.partial_cmp(&b.c.t_abs).unwrap_or(std::cmp::Ordering::Equal)
        .then_with(|| a.source.cmp(&b.source))
        .then_with(|| a.c.pas.cmp(&b.c.pas))
        .then_with(|| a.c.lien.cmp(&b.c.lien)));
    Ok(out)
}

/// Écrit une fusion, avec l'en-tête qui dit d'où viennent les lignes.
pub fn ecrire_fusion(fusion: &[Fusion], chemin: &str) -> std::io::Result<()> {
    let mut f = std::fs::File::create(chemin)?;
    let sources: Vec<&str> = {
        let mut v: Vec<&str> = fusion.iter().map(|x| x.source.as_str()).collect();
        v.sort();
        v.dedup();
        v
    };
    writeln!(f, "# drave trace fusionnee v2 · {} croisements de {} sources", fusion.len(),
             sources.len())?;
    writeln!(f, "# sources {}", sources.join(" "))?;
    writeln!(f, "# source region pas lien n empreinte ms t_abs mode")?;
    for x in fusion {
        writeln!(f, "{} {} {} {} {} {:#018x} {:.3} {:.6} {}",
                 x.source, x.c.region, x.c.pas, x.c.lien, x.c.n, x.c.empreinte, x.c.ms,
                 x.c.t_abs, x.c.mode)?;
    }
    f.flush()
}

/// La DÉRIVE D'HORLOGES entre sources : de combien leurs premières lignes diffèrent.
///
/// Ce n'est pas une correction, c'est une mesure. Deux machines n'ont pas la même
/// horloge, et une fusion qui prétend ordonner des événements distants sans dire de
/// combien les horloges divergent affirme plus qu'elle ne sait. Rend
/// `(source, derive_s)` pour chaque source après la première, la dérive étant
/// `min(t_abs) - min(t_abs) de la référence`.
pub fn derive_horloges(entrees: &[(String, Vec<Croisement>)]) -> Vec<(String, f64)> {
    let mut out = Vec::new();
    let reference = entrees.iter()
        .filter_map(|(s, l)| l.iter().map(|c| c.t_abs).filter(|t| *t > 0.0).fold(None, |a: Option<f64>, t| {
            Some(match a { Some(m) => m.min(t), None => t }) }).map(|m| (s.clone(), m)))
        .min_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal));
    let Some((ref_source, ref_t)) = reference else { return out };
    for (source, lignes) in entrees.iter() {
        if *source == ref_source { continue; }
        let m = lignes.iter().map(|c| c.t_abs).filter(|t| *t > 0.0)
            .fold(None, |a: Option<f64>, t| Some(match a { Some(m) => m.min(t), None => t }));
        if let Some(m) = m { out.push((source.clone(), m - ref_t)); }
    }
    out
}

/// CONFRONTE les deux bouts de chaque lien entre sources.
///
/// LA CONVENTION QUI REND CELA EXACT : un lien porte le MÊME nom aux deux bouts.
/// « local->pair » nomme le lien du pilote vers le nœud, et le nœud enregistre sous
/// ce nom ce qu'il a REÇU ; « pair->local » nomme le retour. Les deux bouts d'un même
/// croisement sont donc appariés par `(lien, pas, n)` — sans tolérance de temps, sans
/// seuil, sans deviner qui est l'émetteur : ce sont deux vues du même événement, et
/// elles DOIVENT porter la même empreinte.
///
/// CE QUI N'EST PAS VÉRIFIABLE EST DIT. En mode listes (1, 2) ou lots (3, 4), le
/// récepteur décode une version **quantifiée** de ce que l'émetteur a encodé : deux
/// empreintes différentes y sont le fonctionnement normal. Ces croisements sont donc
/// rendus NON VÉRIFIABLES avec leur mode — un lien non vérifié ne doit jamais passer
/// pour un lien vérifié.
pub struct ConstatLien {
    pub lien: String,
    pub pas: u32,
    pub source_a: String,
    pub source_b: String,
    pub verdict: VerdictLien,
}

pub enum VerdictLien {
    Identique,
    Divergent { attendu: u64, obtenu: u64 },
    NonVerifiable { mode: u8, raison: &'static str },
}

impl ConstatLien {
    pub fn ligne(&self) -> String {
        let quoi = format!("{} pas {} ({} / {})", self.lien, self.pas, self.source_a, self.source_b);
        match &self.verdict {
            VerdictLien::Identique => format!("{quoi} : identique"),
            VerdictLien::Divergent { attendu, obtenu } =>
                format!("{quoi} : DIVERGENT — {attendu:#018x} d'un côté, {obtenu:#018x} de l'autre"),
            VerdictLien::NonVerifiable { mode, raison } =>
                format!("{quoi} : non vérifiable (mode {mode} : {raison})"),
        }
    }
}

/// Confronte les deux bouts de chaque lien vu par au moins deux sources.
pub fn verifier_liens(entrees: &[(String, Vec<Croisement>)]) -> Vec<ConstatLien> {
    let mut out = Vec::new();
    for (i, (src_a, lignes_a)) in entrees.iter().enumerate() {
        for (src_b, lignes_b) in entrees.iter().skip(i + 1) {
            for a in lignes_a.iter() {
                for b in lignes_b.iter().filter(|b| b.lien == a.lien && b.pas == a.pas) {
                    // `n` différent = les deux bouts ne parlent pas du même objet :
                    // c'est un constat en soi, pas une comparaison d'empreintes.
                    if a.n != b.n {
                        out.push(ConstatLien { lien: a.lien.clone(), pas: a.pas,
                            source_a: src_a.clone(), source_b: src_b.clone(),
                            verdict: VerdictLien::NonVerifiable { mode: 0,
                                raison: "les deux bouts n'ont pas le même nombre de valeurs" } });
                        continue;
                    }
                    let verdict = if a.mode != 0 || b.mode != 0 {
                        VerdictLien::NonVerifiable { mode: a.mode.max(b.mode),
                            raison: "encodage avec perte, les deux bouts diffèrent par construction" }
                    } else if a.empreinte == b.empreinte {
                        VerdictLien::Identique
                    } else {
                        VerdictLien::Divergent { attendu: a.empreinte, obtenu: b.empreinte }
                    };
                    out.push(ConstatLien { lien: a.lien.clone(), pas: a.pas,
                        source_a: src_a.clone(), source_b: src_b.clone(), verdict });
                }
            }
        }
    }
    out
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

/// Comme `ecrire_si`, mais en s'attribuant une source : c'est ce que fait un nœud,
/// dont le nom de région est ce qui le distingue des autres dans la fusion.
pub fn ecrire_si_source(trace: &TraceGlobale, chemin: &Option<String>, source: &str) -> bool {
    match chemin {
        Some(f) => match trace.ecrire_source(f, source) {
            Ok(()) => { println!("[trace] {} croisements écrits dans {f} (source {source})",
                                 trace.len()); true }
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

    // ---- C12bis : fusion, horloges, confrontation des liens ------------------

    /// Fabrique un croisement horodaté : les tests d'ordre ne doivent pas dépendre
    /// de l'heure qu'il est.
    fn cro(region: &str, pas: u32, lien: &str, v: &[f32], t: f64, mode: u8) -> Croisement {
        Croisement { region: region.to_string(), pas, lien: lien.to_string(), n: v.len(),
                     empreinte: empreinte(v), ms: 0.0, t_abs: t, mode }
    }

    #[test]
    fn fusion_ordonne_par_le_temps_mural() {
        let a = ("pilote".to_string(), vec![cro("local", 0, "local->pair", &[1.0], 10.0, 0),
                                            cro("local", 1, "local->pair", &[2.0], 10.5, 0)]);
        let b = ("n1".to_string(), vec![cro("n1", 0, "pair->local", &[3.0], 10.2, 0),
                                        cro("n1", 1, "local->pair", &[4.0], 10.7, 0)]);
        let f = fusionner(&[a, b]).unwrap();
        let ts: Vec<f64> = f.iter().map(|x| x.c.t_abs).collect();
        assert_eq!(ts, vec![10.0, 10.2, 10.5, 10.7], "l'ordre doit être celui du temps mural");
        assert_eq!(f[1].source, "n1");
    }

    #[test]
    fn fusion_est_deterministe_a_horodatage_egal() {
        // Deux nœuds qui partagent la même horloge (ou la même milliseconde) : sans
        // départage explicite, l'ordre dépendrait de l'ordre des fichiers sur la
        // ligne de commande, donc deux fusions du même ensemble donneraient deux
        // fichiers différents.
        let a = ("aaa".to_string(), vec![cro("x", 0, "l", &[1.0], 5.0, 0)]);
        let b = ("bbb".to_string(), vec![cro("y", 0, "l", &[1.0], 5.0, 0)]);
        let f1 = fusionner(&[a.clone(), b.clone()]).unwrap();
        let f2 = fusionner(&[b, a]).unwrap();
        assert_eq!(f1, f2, "l'ordre des fichiers ne doit pas changer la fusion");
        assert_eq!(f1[0].source, "aaa");
    }

    #[test]
    fn fusion_refuse_une_trace_sans_horodatage() {
        let a = ("v1".to_string(), vec![Croisement { region: "local".into(), pas: 0,
            lien: "local->pair".into(), n: 1, empreinte: 7, ms: 0.0, t_abs: 0.0, mode: 0 }]);
        let b = ("v2".to_string(), vec![cro("local", 0, "local->pair", &[1.0], 9.0, 0)]);
        let e = fusionner(&[a, b]).unwrap_err();
        assert!(e.contains("AUCUN horodatage"), "{e}");
        assert!(e.contains("faux ordre"), "le refus doit dire POURQUOI : {e}");
    }

    #[test]
    fn fusion_refuse_une_seule_source_et_une_trace_vide() {
        let a = ("seule".to_string(), vec![cro("local", 0, "l", &[1.0], 1.0, 0)]);
        assert!(fusionner(&[a.clone()]).unwrap_err().contains("DEUX traces"));
        let vide = ("vide".to_string(), Vec::new());
        let e = fusionner(&[a, vide]).unwrap_err();
        assert!(e.contains("VIDE"), "{e}");
    }

    #[test]
    fn derive_horloges_mesure_l_ecart_sans_le_corriger() {
        let a = ("pilote".to_string(), vec![cro("local", 0, "l", &[1.0], 100.0, 0)]);
        let b = ("n1".to_string(), vec![cro("n1", 0, "l", &[1.0], 100.25, 0)]);
        let d = derive_horloges(&[a, b]);
        assert_eq!(d.len(), 1);
        assert_eq!(d[0].0, "n1");
        assert!((d[0].1 - 0.25).abs() < 1e-9, "dérive mesurée : {:?}", d);
        // La première source ne se compare pas à elle-même.
        assert!(derive_horloges(&[("a".into(), vec![cro("x", 0, "l", &[1.0], 1.0, 0)])]).is_empty());
    }

    #[test]
    fn liens_identiques_quand_les_deux_bouts_concordent() {
        let v = [1.0f32, 2.0];
        let a = ("pilote".to_string(), vec![cro("local", 3, "local->pair", &v, 10.0, 0)]);
        let b = ("n1".to_string(), vec![cro("n1", 3, "local->pair", &v, 10.4, 0)]);
        let c = verifier_liens(&[a, b]);
        assert_eq!(c.len(), 1);
        assert!(matches!(c[0].verdict, VerdictLien::Identique), "{}", c[0].ligne());
    }

    #[test]
    fn liens_divergents_detectes_en_mode_dense() {
        // Même lien, même pas, même nombre de valeurs — mais un bit de différence :
        // c'est ce que la fusion doit montrer, et c'est tout son intérêt.
        let a = ("pilote".to_string(), vec![cro("local", 7, "local->pair", &[1.0, 2.0], 1.0, 0)]);
        let mut faux = 2.0f32;
        faux = f32::from_bits(faux.to_bits() ^ 1);
        let b = ("n1".to_string(), vec![cro("n1", 7, "local->pair", &[1.0, faux], 1.3, 0)]);
        let c = verifier_liens(&[a, b]);
        assert_eq!(c.len(), 1);
        assert!(matches!(c[0].verdict, VerdictLien::Divergent { .. }), "{}", c[0].ligne());
        assert!(c[0].ligne().contains("DIVERGENT"));
    }

    #[test]
    fn lien_non_verifiable_en_encodage_avec_perte() {
        // En mode listes (2), le récepteur décode une version quantifiée : deux
        // empreintes différentes y sont NORMALES. Les confronter ferait crier au
        // loup à chaque pas ; les déclarer identiques serait pire.
        let a = ("pilote".to_string(), vec![cro("local", 1, "local->pair", &[1.0], 1.0, 2)]);
        let b = ("n1".to_string(), vec![cro("n1", 1, "local->pair", &[1.5], 1.2, 2)]);
        let c = verifier_liens(&[a, b]);
        assert_eq!(c.len(), 1);
        match c[0].verdict {
            VerdictLien::NonVerifiable { mode, .. } => assert_eq!(mode, 2),
            _ => panic!("un lien en mode listes ne doit pas être déclaré vérifiable : {}", c[0].ligne()),
        }
    }

    #[test]
    fn nombres_de_valeurs_differents_est_un_constat_pas_une_comparaison() {
        let a = ("pilote".to_string(), vec![cro("local", 2, "local->pair", &[1.0, 2.0], 1.0, 0)]);
        let b = ("n1".to_string(), vec![cro("n1", 2, "local->pair", &[1.0], 1.1, 0)]);
        let c = verifier_liens(&[a, b]);
        assert_eq!(c.len(), 1);
        match c[0].verdict {
            VerdictLien::NonVerifiable { raison, .. } =>
                assert!(raison.contains("nombre de valeurs"), "{raison}"),
            _ => panic!("{}", c[0].ligne()),
        }
    }

    #[test]
    fn la_v1_reste_lisible_et_perd_seulement_son_horodatage() {
        let f = std::env::temp_dir().join("essai_trace_v1.txt");
        std::fs::write(&f, "# drave trace globale v1 · 1 croisements\n# region pas lien n \
empreinte ms\nlocal 0 local->pair 3 0x0000000000000abc 0.412\n").unwrap();
        let (source, l) = TraceGlobale::lire_avec_source(f.to_str().unwrap()).unwrap();
        assert_eq!(l.len(), 1);
        assert_eq!(l[0].n, 3);
        assert_eq!(l[0].t_abs, 0.0, "une v1 n'a pas d'horodatage — et ne doit pas en inventer");
        assert_eq!(source, f.to_str().unwrap(), "sans en-tête, la source est le nom du fichier");
        let _ = std::fs::remove_file(&f);
    }

    #[test]
    fn aller_retour_v2_conserve_source_mode_et_horodatage() {
        let mut t = TraceGlobale::nouvelle();
        t.enregistrer_mode("local", 4, "local->pair", &[1.0, 2.0], 3.5, 2);
        let f = std::env::temp_dir().join("essai_trace_v2.txt");
        let chemin = f.to_str().unwrap().to_string();
        t.ecrire_source(&chemin, "pilote").unwrap();
        let (source, l) = TraceGlobale::lire_avec_source(&chemin).unwrap();
        assert_eq!(source, "pilote");
        assert_eq!(l[0].mode, 2);
        assert_eq!(l[0].n, 2);
        assert!(l[0].t_abs > 1.0, "l'horodatage doit être une heure epoch réelle");
        assert!((l[0].ms - 3.5).abs() < 1e-9);
        let _ = std::fs::remove_file(&chemin);
    }
}
