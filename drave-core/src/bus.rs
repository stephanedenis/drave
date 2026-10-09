//! Bus de MODULATION — des scalaires diffusés, pas des données.
//!
//! POURQUOI CE MODULE (docs/plan-cerveau-complet.md, capacité C5). Dans un cerveau,
//! quelques dizaines de milliers de neurones (noradrénaline, dopamine, sérotonine,
//! acétylcholine) modifient le **gain** de milliards d'autres : c'est un scalaire
//! diffus, pas un chemin de données. Le plan en fait la capacité C5, et nos mesures
//! lui ont donné une raison précise : notre seule règle d'apprentissage locale a été
//! réfutée **faute de signal de valeur**, et moduler `η` par la nouveauté *dégrade*.
//!
//! CE QUE CE MODULE EST, ET CE QU'IL N'EST PAS. Il porte des canaux nommés et leurs
//! valeurs ; il ne décide pas de leur effet — **chaque région décide** de ce qu'elle
//! en fait (c'est la définition biologique du neuromodulateur). Le premier
//! consommateur câblé ici est le **gain de région** : `gain` neutre = 1,0, et un gain
//! neutre doit laisser la sortie **identique au bit près** — c'est la porte de la
//! capacité, et elle a des dents : un gain non neutre *change* la sortie.
//!
//! VALEUR NEUTRE PAR CANAL, et c'est ce qui rend la porte vérifiable : `gain` vaut
//! 1,0 par défaut (multiplier par 1 ne change rien), les autres canaux valent 0,0
//! (ajouter 0 ne change rien). Un canal absent est neutre.

use std::collections::BTreeMap;

#[derive(Debug, Clone)]
pub struct Bus {
    canaux: BTreeMap<String, f32>,
}

impl Default for Bus { fn default() -> Self { Bus::nouveau() } }

impl Bus {
    pub fn nouveau() -> Self { Bus { canaux: BTreeMap::new() } }

    /// La valeur NEUTRE d'un canal : ce qui, appliqué, ne change rien.
    pub fn neutre(canal: &str) -> f32 {
        match canal { "gain" => 1.0, _ => 0.0 }
    }

    /// La valeur d'un canal — neutre s'il n'est pas posé.
    pub fn lire(&self, canal: &str) -> f32 {
        *self.canaux.get(canal).unwrap_or(&Self::neutre(canal))
    }

    pub fn poser(&mut self, canal: &str, valeur: f32) { self.canaux.insert(canal.to_string(), valeur); }

    pub fn canaux(&self) -> Vec<(String, f32)> {
        self.canaux.iter().map(|(k, v)| (k.clone(), *v)).collect()
    }

    pub fn est_neutre(&self) -> bool {
        self.canaux.iter().all(|(k, v)| (*v - Self::neutre(k)).abs() < f32::EPSILON)
    }

    /// Analyse `canal=valeur`, répétable. Une entrée illisible est une ERREUR : un
    /// bus mal orthographié qui passerait en silence ferait croire à une mesure.
    pub fn analyser(specs: &[String]) -> Result<Bus, String> {
        let mut b = Bus::nouveau();
        for s in specs {
            let (nom, val) = s.split_once('=')
                .ok_or_else(|| format!("bus : « {s} » n'est pas `canal=valeur`"))?;
            let v: f32 = val.parse()
                .map_err(|_| format!("bus : valeur illisible dans « {s} »"))?;
            if !v.is_finite() {
                return Err(format!("bus : valeur non finie dans « {s} »"));
            }
            b.poser(nom, v);
        }
        Ok(b)
    }

    /// Le gain à appliquer à l'état d'une région — 1,0 si le canal est absent.
    pub fn gain(&self) -> f32 { self.lire("gain") }

    /// Applique le gain à un état, s'il n'est pas neutre. Rend `true` s'il a agi :
    /// c'est ce que le moteur annonce, pour qu'un bus silencieux ne le reste pas.
    pub fn appliquer_gain(&self, etat: &mut [f32]) -> bool {
        let g = self.gain();
        if (g - 1.0).abs() < f32::EPSILON { return false; }
        for v in etat.iter_mut() { *v *= g; }
        true
    }

    /// Ligne de contrôle, pour diffuser un bus vers une autre instance :
    /// `MODULATION gain 1.5` — un message de contrôle, pas une donnée.
    pub fn ligne(&self, canal: &str) -> String {
        format!("MODULATION {canal} {}\n", self.lire(canal))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn un_canal_absent_est_neutre() {
        let b = Bus::nouveau();
        assert_eq!(b.gain(), 1.0, "un gain absent vaut 1 : multiplier par 1 ne change rien");
        assert_eq!(b.lire("recompense"), 0.0);
        assert!(b.est_neutre());
    }

    #[test]
    fn un_gain_neutre_ne_touche_pas_l_etat() {
        let b = Bus::nouveau();
        let mut etat = vec![1.5f32, -2.0, 0.25];
        let avant = etat.clone();
        assert!(!b.appliquer_gain(&mut etat), "un gain neutre ne doit rien faire");
        assert_eq!(etat, avant, "l'état doit être identique — c'est la porte de C5");
    }

    #[test]
    fn un_gain_non_neutre_change_l_etat() {
        let mut b = Bus::nouveau();
        b.poser("gain", 2.0);
        let mut etat = vec![1.5f32, -2.0, 0.25];
        assert!(b.appliquer_gain(&mut etat));
        assert_eq!(etat, vec![3.0, -4.0, 0.5]);
        assert!(!b.est_neutre());
    }

    #[test]
    fn analyse_accepte_et_refuse() {
        let b = Bus::analyser(&["gain=1.5".into(), "recompense=-0.25".into()]).unwrap();
        assert_eq!(b.gain(), 1.5);
        assert_eq!(b.lire("recompense"), -0.25);
        assert!(Bus::analyser(&["gain".into()]).is_err(), "sans « = » c'est une erreur");
        assert!(Bus::analyser(&["gain=abc".into()]).is_err());
        assert!(Bus::analyser(&["gain=inf".into()]).is_err());
    }

    #[test]
    fn la_ligne_de_controle_nomme_le_canal() {
        let mut b = Bus::nouveau();
        b.poser("gain", 1.25);
        assert_eq!(b.ligne("gain"), "MODULATION gain 1.25\n");
    }
}
