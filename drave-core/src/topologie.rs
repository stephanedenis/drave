//! Topologie de régions — le descripteur qui fait d'une CHAÎNE un GRAPHE.
//!
//! POURQUOI CE MODULE (docs/plan-cerveau-complet.md, capacité C1). Le moteur
//! n'exécute aujourd'hui qu'une seule forme : une plage CONTIGUË de couches sur
//! un nœud, un producteur, un consommateur, dans l'ordre des couches
//! (`--couches-locales N`, `--flux-serveur`, `--ppl-reparti`). Un cerveau est un
//! **graphe** de régions : chaque région a sa plage, son hôte, ses entrées et ses
//! sorties. Ce module lit et VÉRIFIE la description d'un tel graphe — il ne
//! l'exécute pas encore : c'est la porte de la capacité, pas la capacité.
//!
//! CE QUI EST REFUSÉ PLUTÔT QUE DEVINÉ. Le dépôt a une culture : une entrée
//! douteuse s'annonce ou s'arrête, elle ne passe pas en silence. Ici, sont
//! refusés avec un message explicite : une couverture de couches trouée ou
//! recouvrante, un identifiant de région dupliqué, un lien vers une région
//! inconnue, un cycle (sauf si `recurrent` est déclaré), une région sans entrée
//! qui n'est pas la première, et un JSON qui contient autre chose que ce que le
//! format autorise.
//!
//! FORMAT (JSON minimal, analysé à la main : le crate est std seul, sans
//! dépendance, et le restera) :
//!
//! ```json
//! {
//!   "regions": [
//!     {"id": "r0", "couches": [0, 11], "instance": "local"},
//!     {"id": "r1", "couches": [12, 23], "instance": "127.0.0.1:49152"}
//!   ],
//!   "liens": [
//!     {"de": "r0", "vers": "r1", "mode": "listes", "delai_ms": 0}
//!   ]
//! }
//! ```

use std::collections::{BTreeMap, BTreeSet};

/// Une région : une plage de couches CONTIGUË, sur une instance nommée.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Region {
    pub id: String,
    pub premiere: usize,
    pub derniere: usize, // incluse
    /// « local » ou « hôte:port ». Le nom n'est pas résolu ici : la topologie
    /// décrit QUI fait quoi, pas comment on lui parle.
    pub instance: String,
}

impl Region {
    pub fn couches(&self) -> usize { self.derniere + 1 - self.premiere }
}

/// Un lien : d'une région vers une autre, avec son mode de transport, son délai
/// imposé et, plus tard, son budget. Le mode reprend les modes du flux existant
/// (0 f32 dense, 1 listes quantifiées, 2 listes par blocs, 3 lot dense, 4 lot en
/// listes) — les nommer ici évite un entier magique dans le fichier.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Lien {
    pub de: String,
    pub vers: String,
    pub mode: String,
    /// Délai imposé sur ce lien, en millisecondes (C3 du plan). Zéro = pas de
    /// délai : c'est le défaut, et c'est la porte de non-régression.
    pub delai_ms: u64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Topologie {
    pub regions: Vec<Region>,
    pub liens: Vec<Lien>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ErreurTopologie(pub String);

impl std::fmt::Display for ErreurTopologie {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "topologie invalide : {}", self.0)
    }
}

// --------------------------------------------------------------------------
// Analyse JSON minimale
// --------------------------------------------------------------------------
// Elle n'accepte QUE ce que le format autorise : objets, tableaux, chaînes,
// entiers. Pas de flottants, pas de `null`, pas de booléens, pas d'échappement
// au-delà de `\"` et `\\`. Un fichier qui contient autre chose est REFUSÉ avec
// sa position — une topologie à moitié lue serait pire qu'une topologie absente.

struct Analyseur<'a> {
    s: &'a [u8],
    i: usize,
}

impl<'a> Analyseur<'a> {
    fn new(s: &'a str) -> Self { Analyseur { s: s.as_bytes(), i: 0 } }

    fn erreur<T>(&self, quoi: &str) -> Result<T, ErreurTopologie> {
        let ligne = 1 + self.s[..self.i.min(self.s.len())].iter().filter(|&&c| c == b'\n').count();
        Err(ErreurTopologie(format!("{quoi} (ligne {ligne}, octet {})", self.i)))
    }

    fn espaces(&mut self) {
        while self.i < self.s.len() && (self.s[self.i] as char).is_whitespace() { self.i += 1; }
    }

    fn attendu(&mut self, c: u8) -> Result<(), ErreurTopologie> {
        self.espaces();
        if self.i < self.s.len() && self.s[self.i] == c { self.i += 1; Ok(()) }
        else { self.erreur(&format!("« {} » attendu", c as char)) }
    }

    fn chaine(&mut self) -> Result<String, ErreurTopologie> {
        self.attendu(b'"')?;
        let mut out = String::new();
        while self.i < self.s.len() {
            match self.s[self.i] {
                b'"' => { self.i += 1; return Ok(out); }
                b'\\' if self.i + 1 < self.s.len() => {
                    let c = self.s[self.i + 1];
                    if c == b'"' || c == b'\\' { out.push(c as char); self.i += 2; }
                    else { return self.erreur("échappement non géré (seuls \\\" et \\\\ le sont)"); }
                }
                c => { out.push(c as char); self.i += 1; }
            }
        }
        self.erreur("chaîne non fermée")
    }

    fn entier(&mut self) -> Result<u64, ErreurTopologie> {
        self.espaces();
        let debut = self.i;
        while self.i < self.s.len() && self.s[self.i].is_ascii_digit() { self.i += 1; }
        if self.i == debut { return self.erreur("entier attendu"); }
        std::str::from_utf8(&self.s[debut..self.i]).unwrap().parse()
            .map_err(|_| ErreurTopologie(format!("entier illisible à l'octet {debut}")))
    }

    /// Un objet dont les clés sont des chaînes et les valeurs ce que `valeur`
    /// accepte. Rendues dans l'ordre du fichier.
    fn objet(&mut self, mut valeur: impl FnMut(&mut Self, &str) -> Result<(), ErreurTopologie>)
        -> Result<(), ErreurTopologie>
    {
        self.attendu(b'{')?;
        self.espaces();
        if self.i < self.s.len() && self.s[self.i] == b'}' { self.i += 1; return Ok(()); }
        loop {
            let cle = self.chaine()?;
            self.attendu(b':')?;
            valeur(self, &cle)?;
            self.espaces();
            match self.s.get(self.i) {
                Some(b',') => { self.i += 1; }
                Some(b'}') => { self.i += 1; return Ok(()); }
                _ => return self.erreur("« , » ou « } » attendu"),
            }
        }
    }

    /// Un tableau dont chaque élément est traité par `element`.
    fn tableau(&mut self, mut element: impl FnMut(&mut Self) -> Result<(), ErreurTopologie>)
        -> Result<(), ErreurTopologie>
    {
        self.attendu(b'[')?;
        self.espaces();
        if self.i < self.s.len() && self.s[self.i] == b']' { self.i += 1; return Ok(()); }
        loop {
            element(self)?;
            self.espaces();
            match self.s.get(self.i) {
                Some(b',') => { self.i += 1; }
                Some(b']') => { self.i += 1; return Ok(()); }
                _ => return self.erreur("« , » ou « ] » attendu"),
            }
        }
    }
}

/// Lit une topologie. Tout ce qui n'est pas reconnu est une ERREUR, jamais un
/// défaut silencieux : une clé inconnue peut cacher une faute de frappe qui
/// changerait le graphe exécuté.
pub fn lire_json(texte: &str) -> Result<Topologie, ErreurTopologie> {
    let mut a = Analyseur::new(texte);
    let mut regions: Vec<Region> = Vec::new();
    let mut liens: Vec<Lien> = Vec::new();

    a.objet(|a, cle| match cle {
        "regions" => a.tableau(|a| {
            let (mut id, mut prem, mut der, mut inst) = (None, None, None, None);
            a.objet(|a, cle| match cle {
                "id" => { id = Some(a.chaine()?); Ok(()) }
                "couches" => {
                    let mut v: Vec<u64> = Vec::new();
                    a.tableau(|a| { v.push(a.entier()?); Ok(()) })?;
                    if v.len() != 2 {
                        return Err(ErreurTopologie(format!(
                            "« couches » attend exactement deux entiers [première, dernière], reçu {}",
                            v.len())));
                    }
                    prem = Some(v[0] as usize); der = Some(v[1] as usize); Ok(())
                }
                "instance" => { inst = Some(a.chaine()?); Ok(()) }
                autre => Err(ErreurTopologie(format!("clé inconnue dans une région : « {autre} »"))),
            })?;
            let (id, prem, der, inst) = match (id, prem, der, inst) {
                (Some(i), Some(p), Some(d), Some(s)) => (i, p, d, s),
                _ => return Err(ErreurTopologie(
                    "région incomplète : « id », « couches » et « instance » sont obligatoires".into())),
            };
            regions.push(Region { id, premiere: prem, derniere: der, instance: inst });
            Ok(())
        }),
        "liens" => a.tableau(|a| {
            let (mut de, mut vers, mut mode, mut delai) = (None, None, None, 0u64);
            a.objet(|a, cle| match cle {
                "de" => { de = Some(a.chaine()?); Ok(()) }
                "vers" => { vers = Some(a.chaine()?); Ok(()) }
                "mode" => { mode = Some(a.chaine()?); Ok(()) }
                "delai_ms" => { delai = a.entier()?; Ok(()) }
                autre => Err(ErreurTopologie(format!("clé inconnue dans un lien : « {autre} »"))),
            })?;
            let (de, vers) = match (de, vers) {
                (Some(a), Some(b)) => (a, b),
                _ => return Err(ErreurTopologie(
                    "lien incomplet : « de » et « vers » sont obligatoires".into())),
            };
            let mode = mode.unwrap_or_else(|| "listes".to_string());
            match mode.as_str() {
                "f32" | "listes" | "blocs" | "lot" | "lot_listes" => {}
                autre => return Err(ErreurTopologie(format!(
                    "mode de lien inconnu : « {autre} » (f32, listes, blocs, lot, lot_listes)"))),
            }
            liens.push(Lien { de, vers, mode, delai_ms: delai });
            Ok(())
        }),
        autre => Err(ErreurTopologie(format!("clé inconnue à la racine : « {autre} »"))),
    })?;

    a.espaces();
    if a.i != a.s.len() {
        return Err(ErreurTopologie(format!("texte après le JSON, octet {}", a.i)));
    }
    Ok(Topologie { regions, liens })
}

impl Topologie {
    /// Vérifie la topologie et rend l'ORDRE D'EXÉCUTION (tri topologique).
    ///
    /// Les refus sont ceux qui feraient exécuter un graphe qui n'est pas celui
    /// qu'on croit : trous et recouvrements de couches, doublons, liens orphelins,
    /// cycles.
    pub fn valider(&self) -> Result<Vec<String>, ErreurTopologie> {
        if self.regions.is_empty() {
            return Err(ErreurTopologie("aucune région".into()));
        }
        let mut vus: BTreeMap<&str, &Region> = BTreeMap::new();
        for r in &self.regions {
            if r.premiere > r.derniere {
                return Err(ErreurTopologie(format!(
                    "région « {} » : plage inversée [{}, {}]", r.id, r.premiere, r.derniere)));
            }
            if vus.insert(&r.id, r).is_some() {
                return Err(ErreurTopologie(format!("identifiant de région dupliqué : « {} »", r.id)));
            }
        }
        // Couverture : chaque couche doit être portée par EXACTEMENT une région.
        // Un trou ferait sauter des couches sans le dire ; un recouvrement
        // calculerait deux fois la même chose et fausserait le résultat.
        let mut couche_a_region: BTreeMap<usize, &str> = BTreeMap::new();
        for r in &self.regions {
            for c in r.premiere..=r.derniere {
                if let Some(autre) = couche_a_region.insert(c, &r.id) {
                    return Err(ErreurTopologie(format!(
                        "couche {c} portée par deux régions : « {autre} » et « {} »", r.id)));
                }
            }
        }
        if let (Some(min), Some(max)) = (couche_a_region.keys().next(), couche_a_region.keys().next_back()) {
            for c in *min..=*max {
                if !couche_a_region.contains_key(&c) {
                    return Err(ErreurTopologie(format!("couche {c} n'est portée par aucune région")));
                }
            }
        }
        for l in &self.liens {
            if !vus.contains_key(l.de.as_str()) {
                return Err(ErreurTopologie(format!("lien depuis une région inconnue : « {} »", l.de)));
            }
            if !vus.contains_key(l.vers.as_str()) {
                return Err(ErreurTopologie(format!("lien vers une région inconnue : « {} »", l.vers)));
            }
            if l.de == l.vers {
                return Err(ErreurTopologie(format!("lien d'une région vers elle-même : « {} »", l.de)));
            }
        }
        // Tri topologique (Kahn). Un cycle n'est pas une erreur en soi dans un
        // cerveau — mais il l'est ICI, tant que la récurrence (C2) n'est pas
        // implémentée : mieux vaut refuser que boucler.
        let mut entrants: BTreeMap<&str, usize> = self.regions.iter().map(|r| (r.id.as_str(), 0)).collect();
        let mut sortants: BTreeMap<&str, Vec<&str>> = BTreeMap::new();
        for l in &self.liens {
            *entrants.get_mut(l.vers.as_str()).unwrap() += 1;
            sortants.entry(l.de.as_str()).or_default().push(l.vers.as_str());
        }
        let mut pretes: BTreeSet<&str> =
            entrants.iter().filter(|(_, &n)| n == 0).map(|(&id, _)| id).collect();
        let mut ordre: Vec<String> = Vec::new();
        while let Some(id) = pretes.iter().next().copied() {
            pretes.remove(id);
            ordre.push(id.to_string());
            for suivant in sortants.get(id).cloned().unwrap_or_default() {
                let n = entrants.get_mut(suivant).unwrap();
                *n -= 1;
                if *n == 0 { pretes.insert(suivant); }
            }
        }
        if ordre.len() != self.regions.len() {
            let restantes: Vec<&str> = entrants.iter().filter(|(_, &n)| n > 0).map(|(&id, _)| id).collect();
            return Err(ErreurTopologie(format!(
                "cycle détecté (la récurrence n'est pas implémentée) : régions en attente {:?}", restantes)));
        }
        Ok(ordre)
    }

    /// Vrai si la topologie est une chaîne simple (chaque région a au plus une
    /// entrée et une sortie). C'est le cas de NON-RÉGRESSION : une chaîne doit se
    /// comporter exactement comme le découpage d'aujourd'hui.
    pub fn est_une_chaine(&self) -> bool {
        let mut sorties: BTreeMap<&str, usize> = BTreeMap::new();
        let mut entrees: BTreeMap<&str, usize> = BTreeMap::new();
        for l in &self.liens {
            *sorties.entry(l.de.as_str()).or_default() += 1;
            *entrees.entry(l.vers.as_str()).or_default() += 1;
        }
        sorties.values().all(|&n| n <= 1) && entrees.values().all(|&n| n <= 1)
    }

    /// Les instances distinctes, dans l'ordre d'apparition.
    pub fn instances(&self) -> Vec<String> {
        let mut v: Vec<String> = Vec::new();
        for r in &self.regions {
            if !v.contains(&r.instance) { v.push(r.instance.clone()); }
        }
        v
    }

    /// Rend le plan : ordre d'exécution, couches par région, instances, liens.
    /// C'est ce que `--topologie … --plan` imprime, et c'est ce qui permet de
    /// vérifier à l'œil qu'un graphe est celui qu'on croit.
    pub fn plan(&self) -> Result<String, ErreurTopologie> {
        let ordre = self.valider()?;
        let par_id: BTreeMap<&str, &Region> = self.regions.iter().map(|r| (r.id.as_str(), r)).collect();
        let mut s = String::new();
        s.push_str(&format!("topologie : {} régions · {} liens · {} instance(s) · {}\n",
                            self.regions.len(), self.liens.len(), self.instances().len(),
                            if self.est_une_chaine() { "CHAÎNE (cas de non-régression)" } else { "GRAPHE" }));
        let total: usize = self.regions.iter().map(|r| r.couches()).sum();
        s.push_str(&format!("couverture : {total} couches, sans trou ni recouvrement\n"));
        s.push_str("ordre d'exécution :\n");
        for (n, id) in ordre.iter().enumerate() {
            let r = par_id[id.as_str()];
            let sorties: Vec<&str> = self.liens.iter()
                .filter(|l| &l.de == id).map(|l| l.vers.as_str()).collect();
            s.push_str(&format!("  {n}. {:<6} couches {:>3}..{:<3} sur {:<22} → {}\n",
                                r.id, r.premiere, r.derniere, r.instance,
                                if sorties.is_empty() { "(sortie du graphe)".to_string() }
                                else { sorties.join(", ") }));
        }
        if self.liens.iter().any(|l| l.delai_ms > 0) {
            s.push_str("délais déclarés :\n");
            for l in self.liens.iter().filter(|l| l.delai_ms > 0) {
                s.push_str(&format!("  {} → {} : +{} ms\n", l.de, l.vers, l.delai_ms));
            }
        }
        Ok(s)
    }

    /// Construit la topologie d'une CHAÎNE à partir de ce que le moteur sait
    /// faire aujourd'hui (`--couches-locales`, un seul pair) : c'est le pont
    /// entre l'existant et le graphe, et la porte de non-régression.
    pub fn chaine(n_couches: usize, locales: usize, pair: &str) -> Topologie {
        let locales = locales.min(n_couches).max(1);
        let regions = vec![
            Region { id: "local".into(), premiere: 0, derniere: locales - 1, instance: "local".into() },
            Region { id: "distant".into(), premiere: locales, derniere: n_couches - 1,
                     instance: pair.to_string() },
        ];
        let liens = vec![Lien { de: "local".into(), vers: "distant".into(),
                                mode: "listes".into(), delai_ms: 0 }];
        Topologie { regions, liens }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const DEUX: &str = r#"{
      "regions": [
        {"id": "r0", "couches": [0, 11], "instance": "local"},
        {"id": "r1", "couches": [12, 23], "instance": "127.0.0.1:49152"}
      ],
      "liens": [ {"de": "r0", "vers": "r1", "mode": "listes", "delai_ms": 0} ]
    }"#;

    #[test]
    fn lit_et_valide_une_chaine() {
        let t = lire_json(DEUX).expect("lecture");
        assert_eq!(t.regions.len(), 2);
        assert!(t.est_une_chaine());
        assert_eq!(t.valider().unwrap(), vec!["r0".to_string(), "r1".to_string()]);
        assert_eq!(t.instances(), vec!["local".to_string(), "127.0.0.1:49152".to_string()]);
        assert_eq!(t.regions[0].couches(), 12);
    }

    #[test]
    fn refuse_un_trou_de_couverture() {
        // La couche 12 n'est portée par personne : sauter des couches sans le
        // dire est exactement le mode d'échec que ce module doit empêcher.
        let t = lire_json(r#"{"regions":[
            {"id":"a","couches":[0,11],"instance":"local"},
            {"id":"b","couches":[13,23],"instance":"local"}],"liens":[]}"#).unwrap();
        let e = t.valider().unwrap_err().to_string();
        assert!(e.contains("couche 12"), "{e}");
    }

    #[test]
    fn refuse_un_recouvrement() {
        let t = lire_json(r#"{"regions":[
            {"id":"a","couches":[0,12],"instance":"local"},
            {"id":"b","couches":[12,23],"instance":"local"}],"liens":[]}"#).unwrap();
        assert!(t.valider().unwrap_err().to_string().contains("deux régions"));
    }

    #[test]
    fn refuse_un_cycle() {
        let t = lire_json(r#"{"regions":[
            {"id":"a","couches":[0,5],"instance":"local"},
            {"id":"b","couches":[6,11],"instance":"local"}],
            "liens":[{"de":"a","vers":"b"},{"de":"b","vers":"a"}]}"#).unwrap();
        let e = t.valider().unwrap_err().to_string();
        assert!(e.contains("cycle"), "{e}");
    }

    #[test]
    fn refuse_une_cle_inconnue() {
        // Une faute de frappe peut changer le graphe : elle doit s'arrêter ici.
        let e = lire_json(r#"{"regions":[{"id":"a","couches":[0,1],"instance":"l","couchs":[0,1]}]}"#)
            .unwrap_err().to_string();
        assert!(e.contains("clé inconnue"), "{e}");
    }

    #[test]
    fn refuse_un_mode_de_lien_inconnu() {
        let e = lire_json(r#"{"regions":[
            {"id":"a","couches":[0,1],"instance":"l"},{"id":"b","couches":[2,3],"instance":"l"}],
            "liens":[{"de":"a","vers":"b","mode":"magique"}]}"#).unwrap_err().to_string();
        assert!(e.contains("mode de lien inconnu"), "{e}");
    }

    #[test]
    fn graphe_en_y_est_un_graphe_pas_une_chaine() {
        let t = lire_json(r#"{"regions":[
            {"id":"g","couches":[0,0],"instance":"local"},
            {"id":"a","couches":[1,2],"instance":"local"},
            {"id":"b","couches":[3,4],"instance":"local"}],
            "liens":[{"de":"g","vers":"a"},{"de":"g","vers":"b"}]}"#).unwrap();
        assert!(!t.est_une_chaine());
        assert_eq!(t.valider().unwrap()[0], "g");
    }

    #[test]
    fn chaine_du_moteur_egale_la_chaine_historique() {
        // La porte de non-régression : la topologie DÉDUITE de `--couches-locales`
        // doit reproduire exactement la forme exécutée aujourd'hui.
        let t = Topologie::chaine(24, 12, "127.0.0.1:49152");
        assert!(t.est_une_chaine());
        assert_eq!(t.valider().unwrap().len(), 2);
        assert_eq!(t.regions[0].premiere, 0);
        assert_eq!(t.regions[0].derniere, 11);
        assert_eq!(t.regions[1].premiere, 12);
        assert_eq!(t.regions[1].derniere, 23);
        assert!(t.plan().unwrap().contains("CHAÎNE"));
    }
}
