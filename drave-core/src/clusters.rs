//! Format **clusters** : un fichier commun, N fichiers d'experts, un mapping.
//!
//! Le problème que ce format résout : un MoE range ses 128 experts dans trois
//! tenseurs 3D par couche, et un nœud qui n'en sert que 16 en lit quand même
//! 128 — soit 8 fois trop. Découpé, le nœud ne lit que son huitième.
//!
//! Trois pièces, et rien d'autre :
//!
//! * `commun.gguf` — tout ce qui n'est pas un expert : embeddings, attention,
//!   normes, ET le routeur (`ffn_gate_inp`), qui doit rester global puisque
//!   c'est lui qui désigne l'expert ;
//! * `cluster-XX.gguf` — les seuls `ffn_{gate,up,down}_exps` d'un sous-ensemble
//!   d'experts, aux mêmes décalages internes que dans le fichier d'origine ;
//! * `mapping.tsv` — pour chaque couche, où est chaque expert global.
//!
//! Le mapping est un **texte**, délibérément : le moteur est en Rust sans
//! dépendance, et un format binaire maison demanderait un lecteur de plus à
//! éprouver. Trois colonnes se lisent à l'œil, ce qui n'est pas un luxe quand
//! c'est la seule chose qui relie un expert global à sa ligne locale.

use crate::gguf::Gguf;
use std::path::{Path, PathBuf};

/// Où trouver chaque expert global.
pub struct Mapping {
    pub n_couches: usize,
    pub n_experts: usize,
    pub n_clusters: usize,
    pub par_cluster: usize,
    /// `local[couche][expert_global]` = `cluster × 65536 + ligne`, ou -1 si cet
    /// expert n'est pas dans ce nœud. Un `i32` unique plutôt qu'un `Option` :
    /// c'est consulté à chaque expert et à chaque jeton.
    local: Vec<Vec<i32>>,
}

impl Mapping {
    /// Lit `mapping.tsv`. Les lignes commençant par `#` sont des commentaires.
    pub fn lire(chemin: &Path) -> std::io::Result<Mapping> {
        let texte = std::fs::read_to_string(chemin)?;
        let mut n_couches = 0usize;
        let mut n_experts = 0usize;
        let mut n_clusters = 0usize;
        let mut par_cluster = 0usize;
        let mut entrees: Vec<(usize, usize, usize, usize)> = Vec::new();
        for (no, l) in texte.lines().enumerate() {
            let l = l.trim();
            if l.is_empty() { continue; }
            if let Some(c) = l.strip_prefix('#') {
                // « # n_couches 48 · n_experts 128 · clusters 8 · experts_par_cluster 16 »
                // Les séparateurs « · » sont là pour l'œil : on les retire avant
                // de découper, sinon le pas de deux tombe sur un séparateur et
                // les valeurs suivantes sont lues de travers (c'est arrivé).
                let champs: Vec<&str> = c.split_whitespace().filter(|w| *w != "·").collect();
                let mut i = 0;
                while i + 1 < champs.len() {
                    let v = champs[i + 1].parse::<usize>().unwrap_or(0);
                    match champs[i] {
                        "n_couches" => n_couches = v,
                        "n_experts" => n_experts = v,
                        "clusters" => n_clusters = v,
                        "experts_par_cluster" => par_cluster = v,
                        _ => {}
                    }
                    i += 2;
                }
                continue;
            }
            let f: Vec<&str> = l.split_whitespace().collect();
            if f.len() < 4 {
                return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, format!(
                    "{}:{} : quatre colonnes attendues (couche local global cluster), lues {}",
                    chemin.display(), no + 1, f.len())));
            }
            let n = |k: usize| f[k].parse::<usize>().map_err(|_| std::io::Error::new(
                std::io::ErrorKind::InvalidData,
                format!("{}:{} : « {} » n'est pas un entier", chemin.display(), no + 1, f[k])));
            entrees.push((n(0)?, n(1)?, n(2)?, n(3)?));
        }
        if n_couches == 0 || n_experts == 0 || n_clusters == 0 {
            return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, format!(
                "{} : en-tête de mapping incomplet (couches {}, experts {}, clusters {})",
                chemin.display(), n_couches, n_experts, n_clusters)));
        }
        if par_cluster == 0 { par_cluster = n_experts / n_clusters; }
        let mut local = vec![vec![-1i32; n_experts]; n_couches];
        for (couche, ligne, global, cluster) in entrees {
            if couche >= n_couches || global >= n_experts || cluster >= n_clusters {
                return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, format!(
                    "{} : entrée hors bornes (couche {couche}, expert {global}, cluster {cluster})",
                    chemin.display())));
            }
            if ligne >= par_cluster {
                return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, format!(
                    "{} : ligne locale {ligne} ≥ {par_cluster} experts par cluster",
                    chemin.display())));
            }
            if local[couche][global] >= 0 {
                return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, format!(
                    "{} : l'expert {global} de la couche {couche} est placé deux fois",
                    chemin.display())));
            }
            local[couche][global] = (cluster * 65536 + ligne) as i32;
        }
        Ok(Mapping { n_couches, n_experts, n_clusters, par_cluster, local })
    }

    /// `(cluster, ligne locale)` de l'expert global `e` de la couche `l`.
    #[inline]
    pub fn ou(&self, l: usize, e: usize) -> Option<(usize, usize)> {
        let v = *self.local.get(l)?.get(e)?;
        if v < 0 { return None; }
        Some(((v as usize) >> 16, (v as usize) & 0xFFFF))
    }

    /// Nombre d'experts présents localement pour une couche (diagnostic).
    pub fn presents(&self, l: usize) -> usize {
        self.local.get(l).map(|v| v.iter().filter(|x| **x >= 0).count()).unwrap_or(0)
    }
}

/// Le mapping du modèle en cours, posé une fois à l'ouverture. Un processus
/// sert un seul modèle : c'est déjà vrai du moteur entier (le GGUF est ouvert
/// une fois et les poids vivent en variables globales).
static ACTIF: std::sync::OnceLock<Mapping> = std::sync::OnceLock::new();

/// Le mapping actif, s'il y en a un.
#[inline]
pub fn actif() -> Option<&'static Mapping> { ACTIF.get() }

/// Un modèle prêt à tourner : le GGUF assemblé et le mapping des experts.
pub struct Modele {
    pub gguf: Gguf,
    pub mapping: Mapping,
    pub chemins: Vec<PathBuf>,
}

/// Ouvre un dossier au format clusters.
///
/// Les tenseurs d'experts du cluster `c` sont exposés sous le préfixe `cl{c}/`,
/// ce qui permet de réunir les N fichiers dans un seul `Gguf` sans que les noms
/// se recouvrent.
pub fn ouvrir(dossier: &Path) -> std::io::Result<Modele> {
    ouvrir_interne(dossier, false)
}

/// Inventaire d'un dossier de clusters : mêmes vérifications, mais les poids ne
/// sont pas lus. Un modèle de 366 Go doit pouvoir être inspecté.
pub fn ouvrir_meta(dossier: &Path) -> std::io::Result<Modele> {
    ouvrir_interne(dossier, true)
}

fn ouvrir_interne(dossier: &Path, meta_seule: bool) -> std::io::Result<Modele> {
    let commun = dossier.join("commun.gguf");
    if !commun.is_file() {
        return Err(std::io::Error::new(std::io::ErrorKind::NotFound,
            format!("{} : commun.gguf absent", dossier.display())));
    }
    let mut clusters: Vec<PathBuf> = Vec::new();
    for e in std::fs::read_dir(dossier)? {
        let p = e?.path();
        let n = p.file_name().and_then(|x| x.to_str()).unwrap_or("").to_string();
        if n.starts_with("cluster-") && n.ends_with(".gguf") { clusters.push(p); }
    }
    clusters.sort();
    if clusters.is_empty() {
        return Err(std::io::Error::new(std::io::ErrorKind::NotFound,
            format!("{} : aucun cluster-*.gguf", dossier.display())));
    }
    let mapping = Mapping::lire(&dossier.join("mapping.tsv"))?;
    if clusters.len() != mapping.n_clusters {
        return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, format!(
            "{} fichiers de cluster pour {} annoncés dans mapping.tsv",
            clusters.len(), mapping.n_clusters)));
    }
    let mut chemins: Vec<PathBuf> = vec![commun];
    chemins.extend(clusters.iter().cloned());
    let mut prefixes: Vec<String> = vec![String::new()];
    prefixes.extend((0..clusters.len()).map(|c| format!("cl{c}/")));
    // Le mapping est publié AVANT que les poids ne soient lus : c'est lui qui
    // dit à `charger_moe` où sont les experts.
    let _ = ACTIF.set(Mapping {
        n_couches: mapping.n_couches, n_experts: mapping.n_experts,
        n_clusters: mapping.n_clusters, par_cluster: mapping.par_cluster,
        local: mapping.local.clone(),
    });
    let refs: Vec<&str> = prefixes.iter().map(String::as_str).collect();
    let gguf = if meta_seule {
        Gguf::open_meta_avec_prefixes(&chemins, &refs)?
    } else {
        Gguf::open_avec_prefixes(&chemins, &refs)?
    };
    Ok(Modele { gguf, mapping, chemins })
}

#[cfg(test)]
mod tests {
    use super::*;

    fn ecrire(nom: &str, contenu: &str) -> PathBuf {
        let p = std::env::temp_dir().join(nom);
        std::fs::write(&p, contenu).unwrap();
        p
    }

    #[test]
    fn mapping_lu_et_traduit() {
        let p = ecrire("drave_mapping_ok.tsv", "\
# drave-clusters-mapping v1
# n_couches 2 · n_experts 4 · clusters 2 · experts_par_cluster 2
# couche\tlocal\tglobal\tcluster
0\t0\t3\t0
0\t1\t1\t0
0\t0\t0\t1
0\t1\t2\t1
1\t0\t2\t0
1\t1\t0\t0
1\t0\t1\t1
1\t1\t3\t1
");
        let m = Mapping::lire(&p).unwrap();
        assert_eq!((m.n_couches, m.n_experts, m.n_clusters, m.par_cluster), (2, 4, 2, 2));
        assert_eq!(m.ou(0, 3), Some((0, 0)));
        assert_eq!(m.ou(0, 1), Some((0, 1)));
        assert_eq!(m.ou(0, 0), Some((1, 0)));
        assert_eq!(m.ou(0, 2), Some((1, 1)));
        assert_eq!(m.ou(1, 3), Some((1, 1)));
        assert_eq!(m.presents(0), 4);
        assert_eq!(m.ou(1, 9), None, "un expert hors bornes n'est pas une panique");
        let _ = std::fs::remove_file(&p);
    }

    /// Un expert placé deux fois est une faute du convertisseur : la refuser est
    /// le seul moyen de ne pas exécuter un modèle silencieusement amputé.
    #[test]
    fn mapping_refuse_les_doublons() {
        let p = ecrire("drave_mapping_dup.tsv", "\
# n_couches 1 · n_experts 2 · clusters 1 · experts_par_cluster 2
0\t0\t1\t0
0\t1\t1\t0
");
        let e = match Mapping::lire(&p) { Ok(_) => panic!("doublon accepté"), Err(e) => e };
        assert!(e.to_string().contains("deux fois"), "{e}");
        let _ = std::fs::remove_file(&p);
    }

    /// Un cluster partiel est le cas NORMAL en nœud unique : la couche ne doit
    /// pas être déclarée incomplète, seulement partielle.
    #[test]
    fn mapping_partiel_est_permis() {
        let p = ecrire("drave_mapping_partiel.tsv", "\
# n_couches 1 · n_experts 4 · clusters 4 · experts_par_cluster 1
0\t0\t2\t1
");
        let m = Mapping::lire(&p).unwrap();
        assert_eq!(m.presents(0), 1);
        assert_eq!(m.ou(0, 2), Some((1, 0)));
        assert_eq!(m.ou(0, 0), None);
        let _ = std::fs::remove_file(&p);
    }
}
