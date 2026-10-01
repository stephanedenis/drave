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
#[derive(Clone)]
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

// NOTE : il n'y a délibérément AUCUN drapeau global « ce nœud est partiel ».
// Il y en a eu un, et il rendait la vérification d'exhaustivité intestable : un
// `OnceLock` ne se pose qu'une fois, tandis que les tests s'exécutent en
// parallèle dans un même processus. L'exhaustivité se vérifie à l'OUVERTURE du
// dossier, là où les fichiers sont sous la main ; les couches, elles, ne
// vérifient que la cohérence entre les trois projections d'experts.

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
    let gardes = gardes_du_milieu()?;
    ouvrir_interne(dossier, false, gardes.as_deref())
}

/// Ouvre un modèle en ne retenant QUE les clusters demandés.
///
/// C'est le mode « nœud partiel » : chaque nœud ne sert que ses experts. Le
/// paramètre est explicite pour que ce chemin soit **testable** — la variable
/// d'environnement, elle, est globale au processus et ne se prête pas à un test
/// qui s'exécute en parallèle d'autres.
pub fn ouvrir_sous_ensemble(dossier: &Path, clusters: Option<&[usize]>)
    -> std::io::Result<Modele> {
    ouvrir_interne(dossier, false, clusters)
}

/// `DRAVE_CLUSTERS=0,3` : les numéros demandés, ou `None` pour tous.
pub fn gardes_du_milieu() -> std::io::Result<Option<Vec<usize>>> {
    match std::env::var("DRAVE_CLUSTERS") {
        Ok(v) if !v.trim().is_empty() => Ok(Some(v.split(',')
            .map(|x| x.trim().parse::<usize>().map_err(|_| std::io::Error::new(
                std::io::ErrorKind::InvalidInput,
                format!("DRAVE_CLUSTERS : « {x} » n'est pas un numéro de cluster"))))
            .collect::<std::io::Result<Vec<usize>>>()?)),
        _ => Ok(None),
    }
}

/// Inventaire d'un dossier de clusters : mêmes vérifications, mais les poids ne
/// sont pas lus. Un modèle de 366 Go doit pouvoir être inspecté.
pub fn ouvrir_meta(dossier: &Path) -> std::io::Result<Modele> {
    let gardes = gardes_du_milieu()?;
    ouvrir_interne(dossier, true, gardes.as_deref())
}

fn ouvrir_interne(dossier: &Path, meta_seule: bool, gardes: Option<&[usize]>)
    -> std::io::Result<Modele> {
    let commun = dossier.join("commun.gguf");
    if !commun.is_file() {
        return Err(std::io::Error::new(std::io::ErrorKind::NotFound,
            format!("{} : commun.gguf absent", dossier.display())));
    }
    // Le numéro de cluster est LU, jamais déduit du rang : un tri lexicographique
    // range « cluster-100 » avant « cluster-20 », et le préfixe `cl{c}/` porte ce
    // numéro. Confondre les deux ferait lire les experts d'un autre fichier —
    // mêmes formes, donc aucune erreur, juste un résultat faux.
    let mut clusters: Vec<(usize, PathBuf)> = Vec::new();
    for e in std::fs::read_dir(dossier)? {
        let p = e?.path();
        let n = p.file_name().and_then(|x| x.to_str()).unwrap_or("").to_string();
        let Some(num) = n.strip_prefix("cluster-")
                          .and_then(|r| r.strip_suffix(".gguf")) else { continue };
        let Ok(c) = num.parse::<usize>() else {
            return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, format!(
                "{} : « {n} » ne porte pas un numéro de cluster lisible", dossier.display())));
        };
        clusters.push((c, p));
    }
    clusters.sort();
    if clusters.is_empty() {
        return Err(std::io::Error::new(std::io::ErrorKind::NotFound,
            format!("{} : aucun cluster-*.gguf", dossier.display())));
    }
    let mapping = Mapping::lire(&dossier.join("mapping.tsv"))?;
    // Un dossier COMPLET doit porter tous les clusters annoncés, numérotés
    // 0..N-1 sans trou. Un dossier PARTIEL (un nœud qui ne possède que ses
    // fichiers) n'en porte qu'une partie — c'est le cas visé par le déploiement
    // distribué, et exiger la continuité l'interdisait.
    let complet = clusters.len() == mapping.n_clusters;
    if complet {
        for (attendu, (num, p)) in clusters.iter().enumerate() {
            if *num != attendu {
                return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, format!(
                    "{} : cluster {attendu} attendu, {} trouvé — un dossier complet doit \
être numéroté 0..{} sans trou", p.display(), num, mapping.n_clusters - 1)));
            }
        }
    }
    for (num, p) in &clusters {
        if *num >= mapping.n_clusters {
            return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, format!(
                "{} : cluster {num} au-delà des {} annoncés par mapping.tsv",
                p.display(), mapping.n_clusters)));
        }
    }
    // Un nœud peut ne porter qu'une PARTIE des clusters (`DRAVE_CLUSTERS=0,3`) :
    // c'est le mode « nœud partiel », où chaque nœud ne sert que ses experts et
    // où les contributions se somment entre nœuds. Le mapping, lui, reste
    // global : il dit où est chaque expert, pas ce que ce nœud-ci possède.
    let clusters: Vec<(usize, PathBuf)> = match gardes {
        None => clusters,
        Some(g) => {
            for c in g {
                if *c >= mapping.n_clusters {
                    return Err(std::io::Error::new(std::io::ErrorKind::InvalidInput,
                        format!("DRAVE_CLUSTERS : cluster {c} hors bornes ({} au total)",
                                mapping.n_clusters)));
                }
                // Un cluster DEMANDÉ mais absent du disque était ignoré en
                // silence : le nœud tournait avec moins d'experts que voulu, et
                // les contributions manquantes disparaissaient sans un mot.
                if !clusters.iter().any(|(n, _)| n == c) {
                    return Err(std::io::Error::new(std::io::ErrorKind::NotFound, format!(
                        "DRAVE_CLUSTERS demande le cluster {c}, absent de {}",
                        dossier.display())));
                }
            }
            clusters.into_iter().filter(|(c, _)| g.contains(c)).collect()
        }
    };
    // Un dossier incomplet n'est accepté que si on l'ASSUME. Sans cette règle,
    // `DRAVE_CLUSTERS` listant tous les clusters annoncés faisait passer un
    // artefact amputé pour complet — les contributions des experts absents
    // disparaissaient sans un mot (défaut trouvé par la revue adverse).
    if gardes.is_none() && !complet {
        return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, format!(
            "{} fichiers de cluster pour {} annoncés dans mapping.tsv : dossier incomplet \
(dites DRAVE_CLUSTERS pour assumer un nœud partiel)",
            clusters.len(), mapping.n_clusters)));
    }
    if clusters.is_empty() {
        return Err(std::io::Error::new(std::io::ErrorKind::InvalidInput,
            "DRAVE_CLUSTERS ne retient aucun cluster"));
    }
    let mut chemins: Vec<PathBuf> = vec![commun];
    chemins.extend(clusters.iter().map(|(_, p)| p.clone()));
    // Le préfixe porte le NUMÉRO du cluster, pas son rang dans la liste : c'est
    // ce numéro que `mapping.tsv` utilise pour dire où est chaque expert. Un
    // nœud qui ne charge que le cluster 3 doit exposer `cl3/`, pas `cl0/`.
    let mut prefixes: Vec<String> = vec![String::new()];
    prefixes.extend(clusters.iter().map(|(c, _)| format!("cl{c}/")));
    let refs: Vec<&str> = prefixes.iter().map(String::as_str).collect();
    let gguf = if meta_seule {
        Gguf::open_meta_avec_prefixes(&chemins, &refs)?
    } else {
        Gguf::open_avec_prefixes(&chemins, &refs)?
    };
    // Le mapping n'est publié qu'APRÈS une ouverture réussie. Le publier avant
    // laissait derrière lui le mapping d'un modèle qu'on venait de refuser : le
    // moteur aurait alors traduit les experts d'un autre modèle, en silence
    // (c'est un test qui l'a montré, pas une relecture).
    let _ = ACTIF.set(Mapping {
        n_couches: mapping.n_couches, n_experts: mapping.n_experts,
        n_clusters: mapping.n_clusters, par_cluster: mapping.par_cluster,
        local: mapping.local.clone(),
    });
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

    /// Le test qui manquait : un DOSSIER de clusters complet, ouvert de bout en
    /// bout. Aucun test n'exerçait `ouvrir` — donc rien ne vérifiait que les
    /// tenseurs préfixés arrivent bien, que le mapping est publié, ni que les
    /// fichiers sont appariés au bon numéro. Un défaut y ferait lire les experts
    /// d'un autre cluster, mêmes formes, sans la moindre erreur.
    #[test]
    fn dossier_de_clusters_ouvre_et_apparie() {
        use crate::gguf::tests::{ecrire, gguf_synth};
        let d = std::env::temp_dir().join("drave_dossier_clusters");
        let _ = std::fs::remove_dir_all(&d);
        std::fs::create_dir_all(&d).unwrap();
        // Le commun porte le routeur (n_experts global) et un tenseur partagé.
        let commun: Vec<(&str, Vec<u64>)> =
            vec![("blk.0.ffn_gate_inp.weight", vec![4, 3]), ("token_embd.weight", vec![8, 3])];
        std::fs::write(d.join("commun.gguf"), gguf_synth(&commun, 0, 1.0)).unwrap();
        // Deux clusters : chacun SON tenseur d'experts, à 2 lignes locales.
        // Les valeurs diffèrent d'un fichier à l'autre, donc une inversion se voit.
        for c in 0..2usize {
            let t: Vec<(&str, Vec<u64>)> =
                vec![("blk.0.ffn_gate_exps.weight", vec![2, 3, 3])];
            std::fs::write(d.join(format!("cluster-{c:02}.gguf")),
                           gguf_synth(&t, c * 10, 1.0)).unwrap();
        }
        // couche 0 : expert global 3 → cluster 0 ligne 1 ; global 0 → cluster 1 ligne 0
        std::fs::write(d.join("mapping.tsv"), "\
# n_couches 1 · n_experts 4 · clusters 2 · experts_par_cluster 2
0\t0\t3\t0
0\t1\t1\t0
0\t0\t0\t1
0\t1\t2\t1
").unwrap();

        let m = ouvrir(&d).expect("le dossier doit s'ouvrir");
        assert_eq!(m.chemins.len(), 3, "commun + deux clusters");
        assert_eq!(m.gguf.nb_fichiers(), 3);
        assert_eq!(m.mapping.n_clusters, 2);
        assert_eq!(m.mapping.par_cluster, 2);
        // On vérifie le mapping RENDU, pas le mapping publié : les tests
        // tournent en parallèle dans un même processus, et `ACTIF` est un
        // `OnceLock` qui ne se pose qu'une fois — le premier test arrivé
        // gagnerait. `charger_moe` lit le publié, mais il ne s'exécute que dans
        // le binaire, où un seul modèle est ouvert.
        // Le TSV dit : couche 0, local 0, global 3, cluster 0.
        assert_eq!(m.mapping.ou(0, 3), Some((0, 0)));
        assert_eq!(m.mapping.ou(0, 1), Some((0, 1)));
        assert_eq!(m.mapping.ou(0, 0), Some((1, 0)));
        assert_eq!(m.mapping.ou(0, 2), Some((1, 1)));
        // Le commun reste en clair, les experts sont préfixés.
        assert!(m.gguf.tensor("blk.0.ffn_gate_inp.weight").is_some());
        assert!(m.gguf.tensor("blk.0.ffn_gate_exps.weight").is_none(),
                "l'expert ne doit exister QUE sous son préfixe de cluster");
        for c in 0..2 {
            let nom = format!("cl{c}/blk.0.ffn_gate_exps.weight");
            let t = m.gguf.tensor(&nom).unwrap_or_else(|| panic!("{nom} absent"));
            assert_eq!(t.fichier, c + 1, "« {nom} » doit venir du fichier {}", c + 1);
            assert_eq!(t.dims[0], 2, "dimension locale d'experts");
        }
        // Les deux fichiers portent des valeurs distinctes.
        let v0 = m.gguf.dequant("cl0/blk.0.ffn_gate_exps.weight");
        let v1 = m.gguf.dequant("cl1/blk.0.ffn_gate_exps.weight");
        assert_ne!(v0, v1, "une inversion de cluster doit se voir");
        let _ = std::fs::remove_dir_all(&d);
    }

    /// Le nœud partiel : ne charger qu'une partie des clusters. Le préfixe doit
    /// porter le NUMÉRO du cluster, pas son rang — sinon un nœud qui ne charge
    /// que le cluster 3 exposerait `cl0/`, et `mapping.tsv` désignerait le
    /// mauvais fichier.
    #[test]
    fn sous_ensemble_garde_les_numeros() {
        use crate::gguf::tests::{ecrire, gguf_synth};
        let d = std::env::temp_dir().join("drave_sous_ensemble");
        let _ = std::fs::remove_dir_all(&d);
        std::fs::create_dir_all(&d).unwrap();
        let t: Vec<(&str, Vec<u64>)> =
            vec![("blk.0.ffn_gate_inp.weight", vec![4, 3])];
        std::fs::write(d.join("commun.gguf"), gguf_synth(&t, 0, 1.0)).unwrap();
        for c in 0..3usize {
            let t: Vec<(&str, Vec<u64>)> =
                vec![("blk.0.ffn_gate_exps.weight", vec![2, 3, 3])];
            std::fs::write(d.join(format!("cluster-{c:02}.gguf")),
                           gguf_synth(&t, c * 10, 1.0)).unwrap();
        }
        std::fs::write(d.join("mapping.tsv"), "\
# n_couches 1 · n_experts 6 · clusters 3 · experts_par_cluster 2
0\t0\t0\t0
0\t1\t1\t0
0\t0\t2\t1
0\t1\t3\t1
0\t0\t4\t2
0\t1\t5\t2
").unwrap();

        // Les trois clusters : le modèle est complet.
        let tous = ouvrir_sous_ensemble(&d, None).unwrap();
        assert_eq!(tous.gguf.nb_fichiers(), 4);
        assert!(tous.gguf.tensor("cl2/blk.0.ffn_gate_exps.weight").is_some());

        // Un seul cluster, le numéro 2 : c'est `cl2/` qui doit apparaître.
        let un = ouvrir_sous_ensemble(&d, Some(&[2])).unwrap();
        assert_eq!(un.gguf.nb_fichiers(), 2, "commun + un cluster");
        assert!(un.gguf.tensor("cl2/blk.0.ffn_gate_exps.weight").is_some(),
                "le préfixe porte le NUMÉRO (2), pas le rang (0)");
        assert!(un.gguf.tensor("cl0/blk.0.ffn_gate_exps.weight").is_none());
        assert!(un.gguf.tensor("cl1/blk.0.ffn_gate_exps.weight").is_none());
        assert_eq!(un.gguf.tensor("cl2/blk.0.ffn_gate_exps.weight").unwrap().fichier, 1);
        // Le mapping reste GLOBAL : l'expert 0 est dans le cluster 0, qui n'est
        // pas chargé — `ou` doit le dire, pas mentir.
        assert_eq!(un.mapping.ou(0, 0), Some((0, 0)));
        assert_eq!(un.mapping.ou(0, 4), Some((2, 0)));

        // Un numéro hors bornes est refusé avec un message qui dit lequel.
        let e = match ouvrir_sous_ensemble(&d, Some(&[0, 7])) {
            Ok(_) => panic!("un cluster hors bornes doit être refusé"),
            Err(e) => e,
        };
        assert!(e.to_string().contains("cluster 7"), "{e}");
        // Un sous-ensemble vide est refusé aussi.
        assert!(ouvrir_sous_ensemble(&d, Some(&[])).is_err());
        let _ = std::fs::remove_dir_all(&d);
    }

    /// Un numéro de cluster manquant doit être refusé, pas renuméroté : les
    /// préfixes `cl{c}/` sont attribués par position, donc un trou décalerait
    /// tous les experts suivants sans le moindre bruit.
    #[test]
    fn numerotation_des_clusters_exigee_continue() {
        let d = std::env::temp_dir().join("drave_clusters_trou");
        let _ = std::fs::remove_dir_all(&d);
        std::fs::create_dir_all(&d).unwrap();
        std::fs::write(d.join("commun.gguf"), b"GGUF").unwrap();
        for c in [0usize, 2] {
            std::fs::write(d.join(format!("cluster-{c:02}.gguf")), b"GGUF").unwrap();
        }
        std::fs::write(d.join("mapping.tsv"),
            "# n_couches 1 · n_experts 4 · clusters 3 · experts_par_cluster 2\n").unwrap();
        let e = match ouvrir(&d) { Ok(_) => panic!("un trou doit être refusé"), Err(e) => e };
        assert!(e.to_string().contains("cluster 1 attendu") || e.to_string().contains("incomplet"),
                "message inattendu : {e}");
        let _ = std::fs::remove_dir_all(&d);
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
