//! Mémoire épisodique adressable par contenu — capacité C6.
//!
//! POURQUOI CE MODULE (docs/plan-cerveau-complet.md, capacité C6). Le moteur sait
//! adresser une **position** (cache KV) et un **hachage** (`engram`), mais pas un
//! **contenu** : rien ne permet aujourd'hui de retrouver « ce qui s'est passé quand
//! l'état ressemblait à ceci ». C'est la fonction de l'hippocampe, et c'est ce qui
//! manque pour que le graphe ait une mémoire d'épisodes — pas seulement des poids.
//!
//! CE QUI EST IMPLÉMENTÉ, ET POURQUOI AINSI.
//!
//! - **La clé est creuse** : les `k` canaux de plus grande amplitude de l'état
//!   (k-WTA). Ce n'est pas une compression commode, c'est le mécanisme : en
//!   gardant peu de canaux, deux états différents deviennent **très** différents
//!   (séparation de motifs, le rôle du gyrus denté) tout en restant lisibles depuis
//!   une version partielle (complétion de motifs, le rôle de CA3).
//! - **La lecture est un plus proche voisin** par recouvrement de clés, et il est
//!   cherché dans un **index inversé** canal -> épisodes : on ne compare donc pas
//!   la clé à tous les épisodes, seulement à ceux qui partagent au moins un canal.
//!   Le coût rendu est celui RÉELLEMENT payé (candidats examinés, canaux lus), pas
//!   une estimation.
//! - **L'écriture est une seule passe** : aucun réentraînement, aucun ajustement
//!   des épisodes déjà écrits. C'est la propriété qui rend l'épisodique utile — un
//!   apprentissage en une fois, contrairement aux poids.
//!
//! CE QUE CE MODULE N'EST PAS, et il faut le dire : ce n'est pas un Hopfield, ni un
//! attracteur : la lecture est un **argmax sur le recouvrement**, sans dynamique de
//! relaxation. Et l'index inversé n'est pas une LSH approximative : il est **exact**
//! sur la génération des candidats (toute clé partageant un canal est vue). Si une
//! version approximative devient nécessaire à l'échelle, elle devra se mesurer
//! contre celle-ci, qui est la référence.

use std::collections::BTreeMap;

/// Un épisode : une clé creuse, sa valeur (l'état complet), et sa provenance.
#[derive(Debug, Clone, PartialEq)]
pub struct Episode {
    pub id: u64,
    /// Canaux retenus, **triés** — deux clés identiques ont la même représentation,
    /// ce qui rend l'égalité et le recouvrement triviaux à calculer.
    pub cle: Vec<u32>,
    /// L'état mémorisé, tel quel. C'est lui que la lecture doit rendre **au bit près**.
    pub valeur: Vec<f32>,
    pub region: String,
    pub pas: u32,
    pub t_abs: f64,
}

/// Ce qu'une lecture a coûté et ce qu'elle a trouvé.
#[derive(Debug, Clone, PartialEq)]
pub struct Lecture {
    pub id: u64,
    pub recouvrement: usize,
    /// Nombre d'épisodes effectivement EXAMINÉS (candidats de l'index).
    pub candidats: usize,
    /// Nombre de comparaisons de canaux payées.
    pub comparaisons: usize,
}

/// Le magasin. `k` est le nombre de canaux gardés par clé — le seul réglage, et
/// c'est lui qui arbitre entre séparation (k petit) et robustesse au bruit (k grand).
#[derive(Debug, Clone)]
pub struct Episodique {
    pub k: usize,
    pub dim: usize,
    episodes: Vec<Episode>,
    index: BTreeMap<u32, Vec<usize>>,
    prochain_id: u64,
}

/// La clé d'un état : les `k` canaux de plus grande amplitude, triés.
///
/// POURQUOI PAR AMPLITUDE ET NON PAR SEUIL : un seuil fixe ferait dépendre la
/// taille de la clé de l'échelle de l'état, qui varie d'une couche et d'un modèle à
/// l'autre. « Les k plus grands » donne une clé de taille **constante**, donc un
/// coût de lecture constant, et c'est ce qu'on veut pouvoir mesurer.
///
/// Les égalités sont départagées par l'indice : sans cela, deux exécutions
/// pourraient rendre deux clés différentes pour le même état (des amplitudes
/// exactement égales arrivent — canaux à zéro, notamment), et la porte de
/// round-trip échouerait une fois sur deux.
pub fn cle(v: &[f32], k: usize) -> Vec<u32> {
    let mut idx: Vec<u32> = (0..v.len() as u32).collect();
    idx.sort_by(|&a, &b| {
        let (xa, xb) = (v[a as usize].abs(), v[b as usize].abs());
        xb.partial_cmp(&xa).unwrap_or(std::cmp::Ordering::Equal).then(a.cmp(&b))
    });
    idx.truncate(k.min(v.len()));
    idx.sort_unstable();
    idx
}

/// Un mélange 64 bits déterministe (splitmix64) — la seule source d'aléa du module.
///
/// POURQUOI DÉTERMINISTE ET SANS DÉPENDANCE : l'expansion doit être la MÊME dans
/// deux exécutions, sur deux machines, sinon un épisode écrit ici serait illisible
/// là-bas — et une mémoire qu'on ne peut pas relire ailleurs n'est pas une mémoire.
/// Une table tirée au hasard ne conviendrait donc pas ; une fonction de hachage, si.
pub fn melange(x: u64) -> u64 {
    let mut z = x.wrapping_add(0x9E37_79B9_7F4A_7C15);
    z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
    z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
    z ^ (z >> 31)
}

/// EXPANSION à la manière du gyrus denté : `d` canaux de sortie, chacun recevant
/// `c` entrées tirées par hachage, avec un signe.
///
/// POURQUOI C'EST NÉCESSAIRE, ET PAS SEULEMENT BIOLOGIQUE. Mesuré : avec 64 canaux
/// sur 896, deux états différents d'un modèle de langue partagent **37 %** de leur
/// clé, si bien que toute clé d'indice recouvre tout le magasin et que l'index
/// inversé **n'élague rien** (300 candidats sur 300). L'arithmétique dit pourquoi :
/// 300 épisodes × 64 canaux = 19 200 entrées sur 896 canaux, soit ~21 par canal.
/// Pour éluder, il faut **plus de canaux** : à 4 096 canaux et k = 32, chaque canal
/// ne porte plus ~2,3 épisodes. C'est exactement ce que fait le gyrus denté — il
/// dilate (≈ 10× plus de cellules granulaires que d'entrées corticales) avant de
/// laisser CA3 faire l'association.
///
/// CE QU'ELLE COÛTE : `d × c` additions par état (32 768 pour 4 096 × 8), payées une
/// fois à l'écriture comme à la lecture — sans commune mesure avec le balayage
/// qu'elle évite.
///
/// CE QU'ELLE PERD, et il faut le dire : la valeur stockée est l'état **projeté**.
/// Retrouver l'état d'origine demanderait une reconstruction (pseudo-inverse,
/// relaxation), qui n'est **pas** implémentée ici.
pub fn expandre(v: &[f32], d: usize, c: usize) -> Vec<f32> {
    let mut out = vec![0.0f32; d];
    if v.is_empty() { return out; }
    for (j, o) in out.iter_mut().enumerate() {
        let mut h = melange(j as u64);
        let mut acc = 0.0f32;
        for _ in 0..c {
            h = melange(h);
            let i = (h % v.len() as u64) as usize;
            // Le signe vient du bit de poids fort : sans lui, une somme de `c`
            // entrées positivement corrélées garderait la composante commune que
            // l'expansion doit justement disperser.
            let signe = if (h >> 63) == 0 { 1.0f32 } else { -1.0 };
            acc += signe * v[i];
        }
        *o = acc;
    }
    out
}

impl Episodique {
    pub fn nouveau(k: usize, dim: usize) -> Self {
        Episodique { k, dim, episodes: Vec::new(), index: BTreeMap::new(), prochain_id: 0 }
    }

    pub fn len(&self) -> usize { self.episodes.len() }
    pub fn est_vide(&self) -> bool { self.episodes.is_empty() }
    pub fn episodes_pub(&self) -> &[Episode] { &self.episodes }

    /// Écrit un épisode : **une seule passe**, et rien n'est modifié derrière.
    pub fn ecrire(&mut self, region: &str, pas: u32, valeur: &[f32], t_abs: f64) -> u64 {
        self.ecrire_avec_cle(region, pas, valeur, valeur, t_abs)
    }

    /// Écrit un épisode dont la **clé** vient d'un vecteur et la **valeur** d'un
    /// autre.
    ///
    /// POURQUOI LES SÉPARER. Avec l'expansion du gyrus denté, la clé vit dans un
    /// espace dilaté (16 384 canaux) tandis que l'état, lui, vit dans 896. Stocker
    /// l'état PROJETÉ multiplierait le magasin par 18 et perdrait l'information :
    /// on ne pourrait plus rendre l'état d'origine. Ici le magasin garde l'état
    /// exact et ne dilate que la clé — la mémoire paie la dilatation une fois par
    /// écriture, pas une fois par épisode stocké.
    pub fn ecrire_avec_cle(&mut self, region: &str, pas: u32, source_cle: &[f32],
                           valeur: &[f32], t_abs: f64) -> u64 {
        let id = self.prochain_id;
        self.prochain_id += 1;
        let cle = cle(source_cle, self.k);
        let i = self.episodes.len();
        for c in &cle {
            self.index.entry(*c).or_default().push(i);
        }
        self.episodes.push(Episode { id, cle, valeur: valeur.to_vec(),
                                     region: region.to_string(), pas, t_abs });
        id
    }

    /// Lit par le contenu : rend l'épisode dont la clé recouvre le mieux celle de
    /// l'indice, et le coût payé pour le trouver.
    ///
    /// Le décompte des candidats porte sur les épisodes **distincts** : un épisode
    /// qui partage cinq canaux avec l'indice ne doit pas être examiné cinq fois,
    /// sinon le coût annoncé serait faux dans le sens qui arrange.
    pub fn lire(&self, indice: &[f32]) -> Option<Lecture> {
        if self.episodes.is_empty() { return None; }
        let cible = cle(indice, self.k);
        let mut vus: BTreeMap<usize, usize> = BTreeMap::new();
        for c in &cible {
            if let Some(postes) = self.index.get(c) {
                for i in postes { *vus.entry(*i).or_insert(0) += 1; }
            }
        }
        // Aucun canal partagé : la lecture échoue. Elle ne rend PAS « le premier
        // épisode » ni « le plus proche au sens euclidien » : sans recouvrement de
        // clé, il n'y a pas de contenu commun, et rendre quelque chose quand même
        // serait exactement le genre de résultat qui a l'air d'un résultat.
        if vus.is_empty() { return None; }
        let candidats = vus.len();
        let mut meilleur: Option<(usize, usize)> = None;
        let mut comparaisons = 0usize;
        for (i, rec) in vus.iter() {
            comparaisons += self.episodes[*i].cle.len();
            match meilleur {
                // Départage par l'identifiant : deux recouvrements égaux ne doivent
                // pas dépendre de l'ordre d'itération d'une table.
                Some((_, r)) if *rec < r => {}
                Some((mi, r)) if *rec == r && self.episodes[mi].id <= self.episodes[*i].id => {}
                _ => meilleur = Some((*i, *rec)),
            }
        }
        let (i, rec) = meilleur?;
        Some(Lecture { id: self.episodes[i].id, recouvrement: rec, candidats, comparaisons })
    }

    /// L'épisode d'un identifiant — c'est ce que la lecture doit rendre, et la
    /// comparaison au bit près se fait sur `valeur`.
    pub fn par_id(&self, id: u64) -> Option<&Episode> {
        self.episodes.iter().find(|e| e.id == id)
    }

    /// La distribution des listes de l'index : (longueur moyenne, longueur maximale,
    /// part des entrées portées par les 1 % de canaux les plus longs).
    ///
    /// POURQUOI CETTE MESURE EXISTE. Un index inversé n'élude que si les listes sont
    /// **courtes et de taille comparable**. Si quelques canaux portent presque tout
    /// le magasin — des « canaux hub » —, alors toute clé d'indice tombe sur eux et
    /// l'index redevient un balayage complet, même avec beaucoup de canaux. C'est
    /// exactement ce qui est arrivé à l'expansion du gyrus denté : la séparation
    /// s'améliore (23,9 → 9,0 canaux partagés) et l'élagage reste faible (0 → 11 %).
    /// La cause n'était pas visible dans le nombre de canaux ; elle l'est ici.
    pub fn listes_canaux(&self) -> (f64, usize, f64) {
        if self.index.is_empty() { return (0.0, 0, 0.0); }
        let moy = self.index.values().map(|v| v.len()).sum::<usize>() as f64
                  / self.index.len() as f64;
        let maxi = self.index.values().map(|v| v.len()).max().unwrap_or(0);
        let mut longueurs: Vec<usize> = self.index.values().map(|v| v.len()).collect();
        longueurs.sort_unstable_by(|a, b| b.cmp(a));
        let haut = (longueurs.len() / 100).max(1);
        let total: usize = longueurs.iter().sum();
        let part = longueurs[..haut].iter().sum::<usize>() as f64 / total.max(1) as f64;
        (moy, maxi, part)
    }

    /// Combien de canaux de clé deux états partagent — la mesure de **séparation**.
    pub fn recouvrement_deux(&self, a: &[f32], b: &[f32]) -> usize {
        let (ca, cb) = (cle(a, self.k), cle(b, self.k));
        let (mut i, mut j, mut n) = (0, 0, 0);
        while i < ca.len() && j < cb.len() {
            match ca[i].cmp(&cb[j]) {
                std::cmp::Ordering::Equal => { n += 1; i += 1; j += 1; }
                std::cmp::Ordering::Less => i += 1,
                std::cmp::Ordering::Greater => j += 1,
            }
        }
        n
    }

    /// Écrit le magasin. Les valeurs sont écrites en **bits** (`0x…` sur les octets
    /// little-endian), pas en décimal : c'est ce qui rend le round-trip exact. Une
    /// écriture en décimal à 9 chiffres perdrait les derniers bits, et l'invariant
    /// « relire rend la valeur écrite » ne serait plus vérifiable.
    pub fn ecrire_fichier(&self, chemin: &str) -> std::io::Result<()> {
        use std::io::Write;
        let mut f = std::fs::File::create(chemin)?;
        writeln!(f, "# drave episodique v1 · k={} · dim={} · {} episodes",
                 self.k, self.dim, self.episodes.len())?;
        writeln!(f, "# id region pas n cle valeur_bits t_abs")?;
        for e in &self.episodes {
            let cle: Vec<String> = e.cle.iter().map(|c| c.to_string()).collect();
            let mut octets = Vec::with_capacity(e.valeur.len() * 4);
            for v in &e.valeur { octets.extend_from_slice(&v.to_le_bytes()); }
            let bits: String = octets.iter().map(|o| format!("{o:02x}")).collect();
            writeln!(f, "{} {} {} {} {} {} {:.6}",
                     e.id, e.region, e.pas, e.valeur.len(), cle.join(","), bits, e.t_abs)?;
        }
        f.flush()
    }

    /// Relit un magasin. Une ligne illisible est une ERREUR (comme la trace) : un
    /// magasin à moitié lu ferait croire à un défaut de rappel qui n'existe pas.
    pub fn lire_fichier(chemin: &str) -> Result<Episodique, String> {
        let texte = std::fs::read_to_string(chemin)
            .map_err(|e| format!("episodique : lecture de {chemin} impossible : {e}"))?;
        let mut k = 0usize;
        let mut dim = 0usize;
        let mut episodes: Vec<Episode> = Vec::new();
        for (n, l) in texte.lines().enumerate() {
            let l = l.trim();
            if l.is_empty() { continue; }
            if let Some(reste) = l.strip_prefix('#') {
                for champ in reste.split('·') {
                    let champ = champ.trim();
                    if let Some(v) = champ.strip_prefix("k=") { k = v.trim().parse().unwrap_or(0); }
                    if let Some(v) = champ.strip_prefix("dim=") { dim = v.trim().parse().unwrap_or(0); }
                }
                continue;
            }
            let ch: Vec<&str> = l.split_whitespace().collect();
            if ch.len() != 7 {
                return Err(format!("episodique : ligne {} illisible (7 champs attendus, {} \
trouvés) : « {l} »", n + 1, ch.len()));
            }
            let nombre = |s: &str, quoi: &str| -> Result<u64, String> {
                s.parse::<u64>().map_err(|_| format!("episodique : {quoi} illisible ligne {} : \
« {s} »", n + 1))
            };
            let mut cle = Vec::new();
            if !ch[4].is_empty() {
                for c in ch[4].split(',') {
                    cle.push(nombre(c, "canal de clé")? as u32);
                }
            }
            let octets = ch[5].trim_start_matches("0x");
            if octets.len() % 8 != 0 {
                return Err(format!("episodique : valeur de {} octets ligne {} — elle doit être \
un multiple de 4 (des f32)", octets.len() / 2, n + 1));
            }
            let mut valeur = Vec::with_capacity(octets.len() / 8);
            let brut: Vec<u8> = (0..octets.len() / 2)
                .map(|i| u8::from_str_radix(&octets[i * 2..i * 2 + 2], 16))
                .collect::<Result<Vec<u8>, _>>()
                .map_err(|_| format!("episodique : bits illisibles ligne {}", n + 1))?;
            for q in brut.chunks_exact(4) {
                valeur.push(f32::from_le_bytes([q[0], q[1], q[2], q[3]]));
            }
            episodes.push(Episode {
                id: nombre(ch[0], "id")?,
                region: ch[1].to_string(),
                pas: nombre(ch[2], "pas")? as u32,
                cle,
                valeur,
                t_abs: ch[6].parse().unwrap_or(0.0),
            });
        }
        if episodes.is_empty() {
            return Err(format!("episodique : {chemin} ne contient aucun épisode"));
        }
        let dim_reelle = episodes[0].valeur.len();
        if dim == 0 { dim = dim_reelle; }
        if dim_reelle != dim {
            return Err(format!("episodique : en-tête annonce dim={dim}, le premier épisode en \
porte {dim_reelle}"));
        }
        if k == 0 { k = episodes[0].cle.len().max(1); }
        // L'index est RECONSTRUIT à la lecture : il n'est pas stocké, parce qu'il est
        // entièrement déductible des clés. Stocker les deux serait stocker deux fois
        // la même information, et laisser la porte ouverte à un index qui contredit
        // les clés.
        let mut m = Episodique { k, dim, episodes: Vec::new(), index: BTreeMap::new(),
                                 prochain_id: 0 };
        for e in episodes {
            let i = m.episodes.len();
            for c in &e.cle { m.index.entry(*c).or_default().push(i); }
            m.prochain_id = m.prochain_id.max(e.id + 1);
            m.episodes.push(e);
        }
        Ok(m)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Un générateur déterministe : les mesures de rappel doivent être reproductibles
    /// à l'octet près, sinon elles ne veulent rien dire.
    struct Alea(u64);
    impl Alea {
        fn nouveau(g: u64) -> Self { Alea(g) }
        fn suivant(&mut self) -> f32 {
            // xorshift64*, puis ramené dans [-1, 1).
            self.0 ^= self.0 >> 12;
            self.0 ^= self.0 << 25;
            self.0 ^= self.0 >> 27;
            let x = self.0.wrapping_mul(0x2545_F491_4F6C_DD1D);
            ((x >> 40) as f32 / 8_388_608.0) - 1.0
        }
        fn vecteur(&mut self, n: usize) -> Vec<f32> {
            (0..n).map(|_| self.suivant()).collect()
        }
    }

    #[test]
    fn la_cle_est_triee_et_de_taille_k() {
        let v = vec![0.1f32, -3.0, 2.0, -0.5, 0.0];
        let c = cle(&v, 2);
        assert_eq!(c, vec![1, 2], "les deux plus grandes amplitudes : -3.0 et 2.0");
        assert_eq!(cle(&v, 99).len(), 5, "k plus grand que dim ne doit pas paniquer");
    }

    #[test]
    fn deux_etats_egaux_ont_la_meme_cle_meme_avec_des_ex_aequo() {
        // Trois canaux à zéro : sans départage par l'indice, deux appels pourraient
        // retenir des canaux différents.
        let v = vec![0.0f32; 8];
        assert_eq!(cle(&v, 3), cle(&v, 3));
        let mut w = v.clone();
        w[5] = 1.0;
        assert!(cle(&w, 3).contains(&5));
    }

    #[test]
    fn round_trip_exact() {
        let mut m = Episodique::nouveau(4, 8);
        let v: Vec<f32> = (0..8).map(|i| (i as f32) * 0.37 - 1.5).collect();
        let id = m.ecrire("local", 3, &v, 123.5);
        let l = m.lire(&v).expect("la même clé doit se retrouver");
        assert_eq!(l.id, id);
        assert_eq!(l.recouvrement, 4, "la clé identique recouvre k canaux");
        let e = m.par_id(id).unwrap();
        assert_eq!(e.valeur, v, "la valeur relue doit être identique AU BIT PRÈS");
    }

    #[test]
    fn round_trip_par_fichier_conserve_les_bits() {
        let mut m = Episodique::nouveau(3, 6);
        // Des valeurs dont la représentation décimale courte serait trompeuse.
        let v = vec![0.1f32, 1.0 / 3.0, -1e-30, f32::MIN_POSITIVE, 1e30, -0.0];
        m.ecrire("d", 12, &v, 7.25);
        let f = std::env::temp_dir().join("essai_episodique.txt");
        let chemin = f.to_str().unwrap().to_string();
        m.ecrire_fichier(&chemin).unwrap();
        let relu = Episodique::lire_fichier(&chemin).unwrap();
        assert_eq!(relu.len(), 1);
        assert_eq!(relu.k, 3);
        assert_eq!(relu.dim, 6);
        assert_eq!(relu.episodes_pub()[0].valeur, v,
                   "les valeurs doivent survivre au fichier sans perdre un bit");
        assert_eq!(relu.par_id(0).unwrap().region, "d");
        // et l'index relu sait lire
        assert_eq!(relu.lire(&v).unwrap().id, 0);
        let _ = std::fs::remove_file(&chemin);
    }

    #[test]
    fn une_lecture_sans_recouvrement_ne_rend_rien() {
        let mut m = Episodique::nouveau(2, 4);
        m.ecrire("a", 0, &[9.0, 9.0, 0.0, 0.0], 0.0);
        // Un indice dont les deux plus grands canaux sont 2 et 3 : aucun recouvrement.
        assert!(m.lire(&[0.0, 0.0, 5.0, 6.0]).is_none(),
                "sans contenu commun, la lecture doit ÉCHOUER, pas rendre un voisin");
    }

    #[test]
    fn ecrire_une_fois_puis_relire_cent_fois() {
        // L'écriture est UNE passe : écrire un épisode ne doit rien changer aux
        // précédents. C'est la propriété qui distingue l'épisodique des poids.
        let mut a = Alea::nouveau(1);
        let mut m = Episodique::nouveau(8, 64);
        let v = a.vecteur(64);
        let id = m.ecrire("x", 0, &v, 0.0);
        let avant = m.par_id(id).unwrap().clone();
        for i in 0..100 { m.ecrire("x", i, &a.vecteur(64), i as f64); }
        assert_eq!(m.par_id(id).unwrap(), &avant, "un épisode écrit ne doit plus bouger");
    }

    #[test]
    fn la_completion_de_motif_retrouve_l_episode() {
        let mut a = Alea::nouveau(7);
        let mut m = Episodique::nouveau(16, 256);
        let mut etats = Vec::new();
        for i in 0..50 {
            let v = a.vecteur(256);
            m.ecrire("local", i, &v, 0.0);
            etats.push(v);
        }
        // Indice PARTIEL : on ne garde que la moitié des canaux de la clé.
        let cible = cle(&etats[17], 16);
        let mut indice = etats[17].clone();
        for (n, c) in cible.iter().enumerate() {
            if n % 2 == 0 { indice[*c as usize] = 0.0; }
        }
        let l = m.lire(&indice).expect("un recouvrement partiel doit suffire");
        assert_eq!(l.id, 17, "l'épisode doit être retrouvé depuis la moitié de sa clé");
    }

    #[test]
    fn l_expansion_est_deterministe_et_disperse() {
        let mut a = Alea::nouveau(11);
        let v = a.vecteur(64);
        assert_eq!(expandre(&v, 256, 8), expandre(&v, 256, 8),
                   "deux exécutions doivent donner la MÊME expansion, sinon un épisode écrit ici serait illisible ailleurs");
        // Une entrée constante ne doit pas donner une sortie constante : sinon
        // l'expansion ne ferait que recopier la composante commune.
        let plat = vec![1.0f32; 64];
        let e = expandre(&plat, 256, 8);
        assert!(e.iter().any(|x| *x > 0.0) && e.iter().any(|x| *x < 0.0),
                "avec des signes, une entrée constante doit donner des sorties des deux signes");
    }

    #[test]
    fn la_cle_peut_venir_d_un_autre_vecteur_que_la_valeur() {
        // La clé est dilatée, la valeur reste l'état d'origine : la lecture doit
        // rendre l'ÉTAT, pas sa projection.
        let etat = vec![0.3f32, -1.2, 0.7, 0.0, 2.5, -0.1, 0.9, 0.2];
        let cle_dilatee = expandre(&etat, 64, 4);
        let mut m = Episodique::nouveau(4, 8);
        let id = m.ecrire_avec_cle("local", 0, &cle_dilatee, &etat, 0.0);
        let l = m.lire(&cle_dilatee).expect("la clé dilatée doit retrouver l'épisode");
        assert_eq!(l.id, id);
        assert_eq!(m.par_id(id).unwrap().valeur, etat,
                   "la valeur stockée doit être l'état d'origine, pas sa projection");
        assert_eq!(m.par_id(id).unwrap().cle.len(), 4);
    }

    #[test]
    fn les_listes_de_canaux_sont_mesurees() {
        let mut m = Episodique::nouveau(2, 8);
        for i in 0..10 { m.ecrire("x", i, &[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, i as f32], 0.0); }
        let (moy, maxi, part) = m.listes_canaux();
        assert!(maxi >= 10, "le canal 0 est dans toutes les clés : max {maxi}");
        assert!(moy > 1.0);
        assert!(part > 0.0 && part <= 1.0, "part des 1 % les plus longs : {part}");
    }

    #[test]
    fn l_expansion_fait_eluder_l_index() {
        // Le point de l'expansion : avec des clés plus creuses dans un espace plus
        // grand, une lecture ne doit plus examiner tout le magasin.
        let mut a = Alea::nouveau(13);
        let n = 400usize;
        let etats: Vec<Vec<f32>> = (0..n).map(|_| a.vecteur(896)).collect();
        let mut sans = Episodique::nouveau(64, 896);
        let mut avec = Episodique::nouveau(32, 4096);
        for e in etats.iter() {
            sans.ecrire("x", 0, e, 0.0);
            avec.ecrire("x", 0, &expandre(e, 4096, 8), 0.0);
        }
        let l_sans = sans.lire(&etats[7]).unwrap();
        let l_avec = avec.lire(&expandre(&etats[7], 4096, 8)).unwrap();
        assert!(l_avec.candidats < l_sans.candidats,
                "l'expansion doit réduire les candidats examinés : {} contre {}",
                l_avec.candidats, l_sans.candidats);
    }

    #[test]
    fn le_cout_annonce_est_le_cout_paye() {
        let mut a = Alea::nouveau(3);
        let mut m = Episodique::nouveau(8, 1024);
        for i in 0..200 { m.ecrire("local", i, &a.vecteur(1024), 0.0); }
        let l = m.lire(&a.vecteur(1024)).unwrap();
        assert!(l.candidats <= 200, "on ne peut pas examiner plus d'épisodes qu'il n'en existe");
        assert!(l.candidats < 200,
                "l'index doit écarter des candidats : {} examinés sur 200", l.candidats);
        assert_eq!(l.comparaisons, l.candidats * 8,
                   "chaque candidat coûte la comparaison de sa clé entière");
    }
}
