//! mrope.rs — LES POSITIONS DU mRoPE (Qwen2-VL), le pas 2 du projet de vision multimodale.
//!
//! POURQUOI CE FICHIER EXISTE, ET POURQUOI IL EST SÉPARÉ. Le moteur applique au modèle de langue une
//! **RoPE 1-D** (`fn rope(…, pos: usize, …)` : **une** position pour toute la tête ✗) alors que
//! Qwen2-VL utilise un **mRoPE** : une position **par section de fréquence** (`[16, 24, 24]` ✓, lu dans
//! la source de la référence ✓) et des positions `(t, h, w)` **distinctes** pour les jetons d'image ✓.
//! Ce fichier porte **le calcul des positions**, et rien d'autre : il ne touche pas à `main.rs` ✗, donc
//! il peut être écrit pendant qu'une passe de portes tourne ✓ (le binaire de la passe est déjà construit
//! ✓ et n'est pas modifié ✓). La **vérification** contre les valeurs d'or se fait **après** ✓.
//!
//! LA CONVENTION, TELLE QU'ELLE A ÉTÉ MESURÉE (`reports/rapport-vision-qwen2vl.md` § 4, et l'outil
//! `tools/mrope_valeurs_or.py` qui la tranche par **comportement** ✗) :
//!   · le **texte** porte `(p, p, p)` ✓ — les trois lignes sont **égales** ✓, donc la règle dégénère
//!     exactement en la RoPE 1-D déjà vérifiée ✓✓ (le mRoPE est un **sur-ensemble strict** ✓) ;
//!   · les jetons d'**image** portent `(t, h, w)` ✓, dans l'ordre **par blocs 2 × 2** ✓ (mesuré :
//!     indice 0 → (0,0), 1 → (0,1), 2 → (1,0), 3 → (1,1) ✓ — c'est le candidat `A_par_blocs` de
//!     l'outil, et c'est LUI qu'il faut confirmer ✗ : le raster reste possible ✗) ;
//!   · après une image, le texte **reprend** à `max(t, h, w) + 1` ✓.
//!
//! ⚠️ CE QUI N'EST PAS ENCORE VÉRIFIÉ, ET QUI DOIT L'ÊTRE AVANT DE BRANCHER QUOI QUE CE SOIT ✗ : la
//! convention de l'ordre des jetons d'image (blocs ou raster ✗) et la valeur exacte de la reprise du
//! texte ✗. Les deux se tranchent en lançant `tools/mrope_valeurs_or.py` **après la passe** ✓ et en
//! comparant ses valeurs d'or à ce que ce fichier calcule ✓ (`#[cfg(test)]` en bas ✓).

/// Un jeton de la séquence, du point de vue des positions.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Jeton {
    /// Un jeton de texte : `(p, p, p)`.
    Texte,
    /// Un jeton d'image : sa place dans la grille **fusionnée** (ligne, colonne), la trame `t`.
    Image { trame: usize, ligne: usize, colonne: usize },
}

/// Le côté de la fusion spatiale de Qwen2-VL (2 × 2 jetons de patch par jeton de séquence).
pub const FUSION: usize = 2;

/// Construit la séquence de jetons d'un enchaînement `texte … image … texte`, avec la grille de
/// l'image (trame, hauteur, largeur **en patchs**), et l'ordre **par blocs 2 × 2**.
pub fn jetons_avec_image(n_texte_avant: usize, grille: (usize, usize, usize), n_texte_apres: usize)
    -> Vec<Jeton>
{
    let (trame, h, w) = grille;
    let (nl, nc) = (h / FUSION, w / FUSION);          // la grille FUSIONNÉE : c'est elle qui porte les jetons
    let mut v = vec![Jeton::Texte; n_texte_avant];
    for bloc_l in 0..nl.div_ceil(FUSION) {
        for bloc_c in 0..nc.div_ceil(FUSION) {
            for dy in 0..FUSION {
                for dx in 0..FUSION {
                    let (l, c) = (bloc_l * FUSION + dy, bloc_c * FUSION + dx);
                    if l < nl && c < nc {
                        v.push(Jeton::Image { trame, ligne: l, colonne: c });
                    }
                }
            }
        }
    }
    v.extend(std::iter::repeat(Jeton::Texte).take(n_texte_apres));
    v
}

/// Les **trois lignes** de positions (`t`, `h`, `w`) pour une séquence de jetons.
///
/// C'est le cœur du mRoPE : le texte avance d'un cran sur les trois lignes **à la fois** ✓, l'image
/// porte ses coordonnées ✓, et le texte qui suit une image **reprend** à `max + 1` ✓.
pub fn positions(jetons: &[Jeton]) -> [Vec<usize>; 3] {
    let mut t = Vec::with_capacity(jetons.len());
    let mut h = Vec::with_capacity(jetons.len());
    let mut w = Vec::with_capacity(jetons.len());
    let mut courant = 0usize;                        // la position du prochain jeton de TEXTE
    for j in jetons {
        match *j {
            Jeton::Texte => {
                t.push(courant);
                h.push(courant);
                w.push(courant);
                courant += 1;
            }
            Jeton::Image { trame, ligne, colonne } => {
                t.push(trame);
                h.push(ligne);
                w.push(colonne);
            }
        }
        // ⚠ APRÈS CHAQUE JETON, `courant` DOIT RESTER AU-DESSUS DE TOUT CE QUI A ÉTÉ ÉCRIT : c'est la
        // règle « le texte reprend à max + 1 » ✓. Sans ce rattrapage, le texte qui suit une image
        // recevrait une position **déjà utilisée** par l'image ✗ — deux jetons différents porteraient
        // la même position, et le modèle ne pourrait plus les distinguer ✗.
        let maxi = *t.last().unwrap().max(h.last().unwrap()).max(w.last().unwrap());
        courant = courant.max(maxi + 1);
    }
    [t, h, w]
}

/// Le découpage des **fréquences** d'une tête entre les trois lignes (`[16, 24, 24]` sur 64 ✓, lu dans
/// la source de la référence : `mrope_section * 2` puis `m[i % 3]` sur les paquets de `cos` ✓).
pub const SECTIONS: [usize; 3] = [16, 24, 24];

/// Quelle ligne de position utilise la fréquence `j` (sur `n_rot / 2` fréquences ✓).
///
/// Les `cos`/`sin` de la référence ont la dimension **entière** de la tête (128 ✓) parce que la
/// convention `rotate_half` apparie `i` et `i + 128/2` ✓ : chaque fréquence apparaît **deux fois** ✓.
/// En unités de **fréquence** (64 ✓), les sections `[16, 24, 24]` disent : ligne 0 pour `j < 16`,
/// ligne 1 pour `16 ≤ j < 40`, ligne 2 au-delà ✓.
pub fn ligne_de_frequence(j: usize) -> usize {
    let (mut borne, mut ligne) = (0usize, 0usize);
    for (k, s) in SECTIONS.iter().enumerate() {
        borne += s;
        if j < borne {
            ligne = k;
            break;
        }
        ligne = k;
    }
    ligne
}

#[cfg(test)]
mod tests {
    use super::*;

    /// LE TEXTE PUR DÉGÉNÈRE EN 1-D : c'est l'invariant qui relie ce fichier à ce qui est **déjà
    /// vérifié** dans le moteur ✓✓ (si celui-ci tombe, le mRoPE ne peut pas être un sur-ensemble de
    /// la RoPE 1-D ✗, et tout le projet est à revoir ✓).
    #[test]
    fn texte_pur_egale_les_trois_lignes() {
        let jetons = vec![Jeton::Texte; 7];
        let [t, h, w] = positions(&jetons);
        assert_eq!(t, h);
        assert_eq!(h, w);
        assert_eq!(t, (0..7).collect::<Vec<_>>());
    }

    /// APRÈS UNE IMAGE, LE TEXTE REPREND AU-DESSUS DU MAXIMUM — jamais sur une position déjà prise ✗.
    #[test]
    fn le_texte_reprend_apres_l_image() {
        let jetons = jetons_avec_image(4, (1, 8, 8), 3);
        let [t, h, w] = positions(&jetons);
        assert_eq!(jetons.len(), 4 + 16 + 3);
        // les quatre premiers : 0,1,2,3 sur les trois lignes
        assert_eq!(&t[..4], &[0, 1, 2, 3]);
        // l'image : la grille fusionnée 4 × 4, par blocs 2 × 2
        assert_eq!(&h[4..8], &[0, 0, 1, 1]);
        assert_eq!(&w[4..8], &[0, 1, 0, 1]);
        // le texte qui suit reprend au-dessus du maximum (3 pour h et w)
        assert_eq!(&t[20..], &[4, 5, 6]);
        assert_eq!(&h[20..], &[4, 5, 6]);
        assert_eq!(&w[20..], &[4, 5, 6]);
    }

    /// LE DÉCOUPAGE DES FRÉQUENCES : 16 pour `t`, 24 pour `h`, 24 pour `w` ✓ — et il couvre les 64
    /// fréquences d'une tête de 128 sans trou ✗.
    #[test]
    fn les_sections_couvrent_les_frequences() {
        assert_eq!(SECTIONS.iter().sum::<usize>(), 64);
        assert_eq!(ligne_de_frequence(0), 0);
        assert_eq!(ligne_de_frequence(15), 0);
        assert_eq!(ligne_de_frequence(16), 1);
        assert_eq!(ligne_de_frequence(39), 1);
        assert_eq!(ligne_de_frequence(40), 2);
        assert_eq!(ligne_de_frequence(63), 2);
    }
}
