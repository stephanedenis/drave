//! Détection du matériel et choix automatique de la configuration.
//!
//! Tout ce que ce module décide vient d'une **mesure**, pas d'une intuition.
//! Chaque heuristique porte le chiffre qui la justifie, et la commande
//! `--materiel` les affiche toutes avec leur raison — pour qu'un réglage
//! surprenant puisse être contesté.
//!
//! Les mesures de référence (session du 01/10, Xeon E5-2687W v3, 2 Quadro
//! RTX 5000, NVMe MAP1602) :
//!
//! | | |
//! |---|---|
//! | VRAM (noyau warp) | 84,9 Go/s |
//! | RAM, 20 cœurs physiques | 22,5 Go/s |
//! | RAM, 10 cœurs + leurs hyperthreads | 18,7 Go/s (+27 % sur 10 cœurs secs) |
//! | RAM, 20 cœurs + hyperthreads | 18,9 Go/s — **rien de plus** |
//! | NVMe, 1 lecteur | 5,4 Go/s |
//! | **NVMe, 16 lecteurs** | **31,1 Go/s** |

use std::path::Path;
use std::process::Command;

#[derive(Debug, Clone)]
pub struct Noeud {
    pub id: usize,
    pub cpus: Vec<usize>,
    pub memoire_go: f64,
}

#[derive(Debug, Clone)]
pub struct Cpu {
    pub physiques: usize,
    pub logiques: usize,
    /// Pour chaque cœur physique, ses threads logiques. Sert au placement :
    /// deux fils d'une même paire partagent L1 et L2, ce qui vaut +27 % quand
    /// les cœurs sont comptés.
    pub paires: Vec<Vec<usize>>,
    pub noeuds: Vec<Noeud>,
    pub l1_ko: usize,
    pub l2_ko: usize,
    pub l3_ko: usize,
}

#[derive(Debug, Clone)]
pub struct Gpu {
    pub ordinal: i32,
    pub nom: String,
    pub vram_libre_go: f64,
    pub vram_totale_go: f64,
    pub noeud: Option<usize>,
    /// Liens NVLink actifs : 25,8 Go/s sur cette machine, soit 2× le PCIe.
    pub liens_nvlink: usize,
}

#[derive(Debug, Clone)]
pub struct Disque {
    pub chemin: String,
    pub libre_go: f64,
    pub noeud: Option<usize>,
    /// Le disque est-il le support des artefacts (donc celui qu'on lira en
    /// flux) ? Sinon il ne sert qu'au stockage froid.
    pub artefact: bool,
}

pub struct Materiel {
    pub cpu: Cpu,
    pub gpus: Vec<Gpu>,
    pub ram_totale_go: f64,
    pub ram_libre_go: f64,
    pub disques: Vec<Disque>,
}

/// Ce que le moteur va utiliser, avec la raison de chaque choix.
#[derive(Debug, Clone)]
pub struct Plan {
    pub threads: usize,
    /// Placement explicite, quand le défaut ne suffit pas (nœud restreint).
    pub epinglage: Option<Vec<usize>>,
    pub lecteurs: usize,
    pub cache_experts_go: f64,
    pub kv_bits: u32,
    pub raisons: Vec<String>,
}

fn lire(chemin: &str) -> Option<String> {
    std::fs::read_to_string(chemin).ok().map(|s| s.trim().to_string())
}

/// Topologie CPU, lue dans `/sys`. C'est la seule source qui distingue un cœur
/// d'un thread logique : `available_parallelism` rend 40 pour 20 cœurs ici.
fn detecter_cpu() -> Cpu {
    let mut paires: Vec<(usize, usize, usize, Vec<usize>)> = Vec::new();  // (paquet, coeur, cpu, threads)
    let mut tous: Vec<usize> = Vec::new();
    if let Ok(entrees) = std::fs::read_dir("/sys/devices/system/cpu") {
        for e in entrees.flatten() {
            let p = e.path();
            let nom = match p.file_name().and_then(|n| n.to_str()) { Some(n) => n, None => continue };
            let Some(num) = nom.strip_prefix("cpu") else { continue };
            if num.is_empty() || !num.bytes().all(|c| c.is_ascii_digit()) { continue; }
            let Ok(id) = num.parse::<usize>() else { continue };
            let paquet = lire(p.join("topology/physical_package_id").to_str().unwrap_or(""))
                .and_then(|s| s.parse().ok()).unwrap_or(0);
            let coeur = lire(p.join("topology/core_id").to_str().unwrap_or(""))
                .and_then(|s| s.parse().ok()).unwrap_or(id);
            tous.push(id);
            match paires.iter_mut().find(|(a, b, _, _)| *a == paquet && *b == coeur) {
                Some(t) => t.3.push(id),
                None => paires.push((paquet, coeur, id, vec![id])),
            }
        }
    }
    tous.sort();
    let logiques = if tous.is_empty() { 1 } else { tous.len() };
    let physiques = if paires.is_empty() { logiques } else { paires.len() };
    let mut paires: Vec<Vec<usize>> = paires.into_iter().map(|(_, _, _, t)| t).collect();
    paires.sort();

    // Nœuds NUMA, d'après /sys/devices/system/node/node*/cpulist.
    let mut noeuds = Vec::new();
    if let Ok(entrees) = std::fs::read_dir("/sys/devices/system/node") {
        for e in entrees.flatten() {
            let p = e.path();
            let nom = match p.file_name().and_then(|n| n.to_str()) { Some(n) => n, None => continue };
            let Some(num) = nom.strip_prefix("node") else { continue };
            let Ok(id) = num.parse::<usize>() else { continue };
            let cpus = lire(p.join("cpulist").to_str().unwrap_or(""))
                .map(|s| liste_cpus(&s)).unwrap_or_default();
            // La mémoire d'un nœud est dans meminfo, en kilo-octets.
            let memoire_go = std::fs::read_to_string(p.join("meminfo")).ok()
                .and_then(|s| s.lines().next()
                          .and_then(|l| l.split_whitespace().nth(3))
                          .and_then(|k| k.parse::<f64>().ok()))
                .map(|ko| ko / 1e6).unwrap_or(0.0);
            noeuds.push(Noeud { id, cpus, memoire_go });
        }
    }
    noeuds.sort_by_key(|n| n.id);

    let cache = |n: &str| -> usize {
        std::fs::read_dir("/sys/devices/system/cpu/cpu0/cache")
            .ok()
            .and_then(|d| d.flatten().find_map(|e| {
                let p = e.path();
                let niveau = lire(p.join("level").to_str()?).and_then(|s| s.parse::<u32>().ok())?;
                let type_ = lire(p.join("type").to_str()?)?;
                let attendu = n.chars().filter(|c| c.is_ascii_digit()).collect::<String>();
                if niveau.to_string() == attendu && type_ != "Instruction" {
                    lire(p.join("size").to_str()?).and_then(|s| {
                        s.trim_end_matches('K').trim_end_matches('M').parse::<usize>().ok()
                    })
                } else { None }
            }))
            .unwrap_or(0)
    };
    Cpu { physiques, logiques, paires, noeuds,
          l1_ko: cache("L1d"), l2_ko: cache("L2"), l3_ko: cache("L3") }
}

/// « 0-9,20-29 » -> [0..9, 20..29]
fn liste_cpus(s: &str) -> Vec<usize> {
    let mut out = Vec::new();
    for part in s.split(',') {
        match part.split_once('-') {
            Some((a, b)) => {
                if let (Ok(a), Ok(b)) = (a.trim().parse::<usize>(), b.trim().parse::<usize>()) {
                    out.extend(a..=b);
                }
            }
            None => { if let Ok(v) = part.trim().parse() { out.push(v); } }
        }
    }
    out
}

/// GPU vus par `nvidia-smi`. On passe par l'outil plutôt que par l'API CUDA :
/// le moteur n'ouvre le pilote que s'il en a besoin, et la détection doit
/// pouvoir se faire sans lui.
fn detecter_gpus() -> Vec<Gpu> {
    let sortie = Command::new("nvidia-smi")
        .args(["--query-gpu=index,name,memory.total,memory.free",
               "--format=csv,noheader,nounits"])
        .output();
    let Ok(sortie) = sortie else { return Vec::new() };
    let texte = String::from_utf8_lossy(&sortie.stdout);
    let mut gpus = Vec::new();
    for l in texte.lines() {
        let c: Vec<&str> = l.split(',').map(|x| x.trim()).collect();
        if c.len() < 4 { continue; }
        let ordinal: i32 = c[0].parse().unwrap_or(0);
        let total = c[2].parse::<f64>().unwrap_or(0.0) / 1024.0;
        let libre = c[3].parse::<f64>().unwrap_or(0.0) / 1024.0;
        // NVLink : `nvidia-smi nvlink -s` liste les liens actifs par GPU.
        let liens = Command::new("nvidia-smi")
            .args(["nvlink", "-s", "-i", &ordinal.to_string()])
            .output().ok()
            .map(|o| String::from_utf8_lossy(&o.stdout).matches("GB/s").count())
            .unwrap_or(0);
        // Le nœud NUMA d'une carte PCI se lit dans /sys, via son adresse.
        let noeud = lire(&format!("/sys/bus/pci/devices/0000:{:02x}:00.0/numa_node",
                                  ordinal as usize + 3))
            .and_then(|s| s.parse::<i32>().ok())
            .filter(|n| *n >= 0).map(|n| n as usize);
        gpus.push(Gpu { ordinal, nom: c[1].to_string(), vram_libre_go: libre,
                        vram_totale_go: total, noeud, liens_nvlink: liens });
    }
    gpus
}

/// RAM libre seule. `detecter()` lance `nvidia-smi` deux fois : le charger pour
/// connaître la mémoire disponible serait payer 100 ms au démarrage de chaque
/// modèle pour une information qui tient dans `/proc/meminfo`.
pub fn ram_libre_go() -> f64 {
    std::fs::read_to_string("/proc/meminfo").ok()
        .and_then(|s| s.lines().find(|l| l.starts_with("MemAvailable:"))
                 .and_then(|l| l.split_whitespace().nth(1))
                 .and_then(|k| k.parse::<f64>().ok()))
        .map(|ko| ko / 1e6)
        .unwrap_or(0.0)
}

fn detecter_ram() -> (f64, f64) {
    let mut total = 0.0; let mut dispo = 0.0;
    if let Ok(s) = std::fs::read_to_string("/proc/meminfo") {
        for l in s.lines() {
            let v: Vec<&str> = l.split_whitespace().collect();
            if v.len() < 2 { continue; }
            let ko: f64 = v[1].parse().unwrap_or(0.0);
            match v[0] {
                "MemTotal:" => total = ko / 1e6,
                "MemAvailable:" => dispo = ko / 1e6,
                _ => {}
            }
        }
    }
    (total, dispo)
}

/// Un disque et son nœud NUMA. Le nœud se lit **par disque**, en remontant du
/// point de montage à son périphérique bloc : attribuer le nœud du premier NVMe
/// trouvé à tous les disques donnait « nœud 0 » au disque mécanique, qui n'en a
/// aucun (il est en SATA).
fn detecter_disques() -> Vec<Disque> {
    let mut out = Vec::new();
    // L'array raid0 (4 NVMe, monté `~/IA`) est un **disque d'artefacts** comme
    // `FastNVMe` : c'est là que vivent les modèles réécrits et les traces. Il manquait
    // à cette liste jusqu'au 12/10 — `--materiel` ne le montrait pas, alors que le
    // § 7.2 de `docs/configuration-nvme-raid-amd.md` attend de le voir « sur le nœud 1 ».
    for (chemin, artefact) in [("/home/stephane/FastNVMe", true),
                               ("/home/stephane/IA", true),
                               ("/home/stephane/Data13TB", false)] {
        if !Path::new(chemin).is_dir() { continue; }
        // `df --output=avail` rend « 698G » : le suffixe doit être retiré.
        let libre_go = Command::new("df").args(["-B", "G", "--output=avail", chemin])
            .output().ok()
            .and_then(|o| String::from_utf8_lossy(&o.stdout).lines().nth(1)
                     .map(|l| l.trim().trim_end_matches('G').trim().to_string()))
            .and_then(|t| t.parse::<f64>().ok())
            .unwrap_or(0.0);
        // Le périphérique qui porte ce montage, puis son disque bloc.
        let source = Command::new("findmnt").args(["-no", "SOURCE", chemin])
            .output().ok()
            .map(|o| String::from_utf8_lossy(&o.stdout).trim().to_string())
            .unwrap_or_default();
        // /dev/nvme0n1p2 -> nvme0n1 ; /dev/mapper/system-root -> le disque sous-jacent.
        let base = source.trim_start_matches("/dev/").to_string();
        let bloc = if base.starts_with("nvme") {
            base.split('p').next().unwrap_or(&base).to_string()
        } else if base.starts_with("md") {
            // Un array n'a pas de `device/numa_node` (`md0` n'est pas un périphérique
            // PCI) : son nœud est celui de ses disques. `md0` -> `nvme0n1` -> nœud 1.
            premier_membre(&base).unwrap_or_else(|| base.clone())
        } else if base.starts_with("mapper/") || base.starts_with("sd") {
            // Un volume LVM : on prend le premier disque SATA, faute de mieux —
            // il n'a de toute façon pas de nœud NUMA.
            "sda".to_string()
        } else { base.clone() };
        let noeud = lire(&format!("/sys/block/{bloc}/device/numa_node"))
            .and_then(|s| s.parse::<i32>().ok()).filter(|n| *n >= 0).map(|n| n as usize);
        out.push(Disque { chemin: chemin.to_string(), libre_go, noeud, artefact });
    }
    out
}

/// Le premier disque d'un array : `md0` -> `/sys/block/md0/md/dev-nvme0n1` -> `nvme0n1`.
///
/// Rend `None` si le dossier n'existe pas (ce n'est pas un array) — l'appelant garde
/// alors le nom tel quel et le nœud restera inconnu, ce qui est la vérité.
fn premier_membre(md: &str) -> Option<String> {
    let mut noms: Vec<String> = std::fs::read_dir(format!("/sys/block/{md}/md")).ok()?
        .filter_map(|e| e.ok())
        .filter_map(|e| e.file_name().into_string().ok())
        .filter_map(|n| n.strip_prefix("dev-").map(|s| s.to_string()))
        .collect();
    noms.sort();
    noms.into_iter().next()
}

impl Materiel {
    pub fn detecter() -> Materiel {
        let cpu = detecter_cpu();
        let gpus = detecter_gpus();
        let (ram_totale_go, ram_libre_go) = detecter_ram();
        let disques = detecter_disques();
        Materiel { cpu, gpus, ram_totale_go, ram_libre_go, disques }
    }

    /// Le plan de configuration, avec la raison de chaque choix.
    ///
    /// `ctx` et `taille_modele_go` orientent deux décisions : la quantification
    /// du cache KV et la répartition entre mémoire et disque.
    pub fn plan(&self, ctx: usize, taille_modele_go: f64, n_experts: usize,
                mo_par_expert: f64) -> Plan {
        let mut raisons = Vec::new();

        // --- threads : les cœurs PHYSIQUES, et les paires HT si on est pauvre.
        //
        // Mesuré : 20 cœurs = 22,5 Go/s, 20 cœurs + HT = 18,9 (rien de plus,
        // la bande passante sature) ; mais 10 cœurs = 14,7 contre 18,7 avec
        // leurs hyperthreads (+27 %, la latence mémoire est masquée et le L2
        // de 256 Ko est partagé). Trois fils par cœur régresse (15,0).
        let threads = self.cpu.physiques;
        raisons.push(format!(
            "threads = {} cœurs physiques ({} logiques détectés) — au-delà, la \
bande passante mémoire sature : 20 cœurs = 22,5 Go/s, 20 cœurs + hyperthreads = 18,9",
            self.cpu.physiques, self.cpu.logiques));

        // Si la machine est petite (moins de 8 cœurs), les paires HT valent le
        // coup : +27 % mesuré à dix cœurs.
        let epinglage = if self.cpu.physiques < 8 && self.cpu.logiques > self.cpu.physiques {
            let mut l = Vec::new();
            for p in &self.cpu.paires { l.extend(p.iter().copied()); }
            raisons.push(format!(
                "épinglage sur les {} paires hyperthread : à {} cœurs, les jumeaux \
rendent +27 % (14,7 -> 18,7 Go/s) en masquant la latence mémoire",
                self.cpu.paires.len(), self.cpu.physiques));
            Some(l)
        } else {
            None
        };

        // --- lecteurs disque : le parallélisme multiplie le débit.
        //
        // Mesuré : 1 lecteur = 5,4 Go/s, 16 = 31,1. La courbe ne est pas plate
        // entre 8 et 16 (28,3 -> 31,1), donc on prend large, borné par les cœurs.
        let lecteurs = 16.min(self.cpu.physiques.max(4));
        raisons.push(format!(
            "lecteurs disque = {} — le NVMe passe de 5,4 Go/s (1 lecteur) à \
31,1 (16), soit ×6 ; c'est ce qui rend le chargement à la demande viable", lecteurs));

        // --- cache d'experts en VRAM : ce qui reste après le commun.
        let vram: f64 = self.gpus.iter().map(|g| g.vram_libre_go).sum();
        let reserve = 2.0;                       // contexte CUDA, tampons, KV
        let commun_go = 8.0;                     // tête + attention + embeddings (V4.1)
        let cache_experts_go = (vram - reserve - commun_go).max(0.0);
        if vram > 0.0 {
            raisons.push(format!(
                "cache d'experts VRAM = {:.1} Go — {:.1} Go libres moins {:.0} de \
réserve CUDA et {:.0} pour le commun ; la VRAM lit à 84,9 Go/s contre 22,5 pour la RAM",
                cache_experts_go, vram, reserve, commun_go));
        }
        if self.gpus.iter().any(|g| g.liens_nvlink > 0) {
            raisons.push("NVLink détecté (25,8 Go/s, 2× le PCIe) : les échanges \
entre cartes passent par lui sans réglage".to_string());
        }

        // --- quantification du KV : elle dépend du contexte, pas d'un goût.
        //
        // Mesuré sur V4.1 : le KV de MLA fait 90,0 Ko par jeton en F16, soit
        // 96,6 Go à 1 M de jetons — plus que les 71 Go d'experts. En int8,
        // 48,3 Go. Au-delà de 0,77 M en F16, il ne reste plus de place.
        let kv_par_jeton_f16 = 90_000.0;         // octets, 40 couches MLA
        let kv_go = kv_par_jeton_f16 * ctx as f64 / 1e9;
        let kv_bits = if kv_go > 0.35 * self.ram_libre_go { 8 } else { 32 };
        raisons.push(format!(
            "cache KV en {} bits — à {} jetons il pèse {:.1} Go en F16, soit {:.0} % \
de la RAM libre ({:.0} Go)",
            kv_bits, ctx, kv_go, 100.0 * kv_go / self.ram_libre_go.max(1.0), self.ram_libre_go));

        // --- ce qui doit rester en mémoire, et ce qui peut rester sur le disque.
        let experts_go = n_experts as f64 * mo_par_expert / 1000.0;
        let pour_ram = self.ram_libre_go - commun_go - kv_go.max(0.0);
        if experts_go > pour_ram && pour_ram > 0.0 {
            let part = pour_ram / experts_go;
            raisons.push(format!(
                "experts : {:.0} Go au total, {:.0} Go de place en RAM ({:.0} % de \
l'empreinte) ; le reste se lit à la demande — mesuré, 90 % des appels tiennent dans \
46 % de l'empreinte", experts_go, pour_ram, 100.0 * part));
        }
        if taille_modele_go > 0.0 {
            raisons.push(format!(
                "modèle de {:.0} Go : mmap obligatoire, la RAM ne peut pas en garder \
une copie", taille_modele_go));
        }

        Plan { threads, epinglage, lecteurs, cache_experts_go, kv_bits, raisons }
    }

    /// Ce que coûtera un jeton, d'après les débits **mesurés** sur cette machine.
    ///
    /// Ce n'est pas une prédiction de performance : c'est la somme des trafics
    /// divisée par les débits, pour voir où passe le temps et ce qu'un
    /// déplacement changerait. Les débits viennent du banc (`--gpu-banc`) et des
    /// mesures de disque, pas d'une fiche technique.
    pub fn cout_par_jeton(&self, plan: &Plan, go_experts_par_jeton: f64,
                          go_tete: f64, go_commun: f64) -> String {
        const VRAM: f64 = 84.9;
        const RAM: f64 = 22.5;
        const NVME: f64 = 31.0;      // 16 lecteurs parallèles, mesuré
        // Taux de succès du cache d'experts : mesuré, 25 % de l'empreinte sert
        // 80 % des appels. On l'applique au trafic, pas à la place occupée.
        const SUCCES: f64 = 0.80;

        let vram_totale: f64 = self.gpus.iter().map(|g| g.vram_libre_go).sum();
        // Le commun et la tête sont RELUS à chaque jeton : ils restent en VRAM.
        let fixes = go_commun + go_tete;
        let cache = (vram_totale - fixes).max(0.0);
        // Ce qui manque au cache se lit sur le disque, en parallèle.
        let experts_disque = go_experts_par_jeton * (1.0 - SUCCES);
        let experts_cache = go_experts_par_jeton - experts_disque;

        let ms = 1000.0 * (fixes / VRAM + experts_cache / VRAM + experts_disque / NVME);
        format!(
            "coût par jeton estimé : {ms:.0} ms — commun + tête {fixes:.1} Go en VRAM \
({:.0} ms) · {experts_cache:.2} Go d'experts servis par le cache de {cache:.1} Go \
({:.0} ms) · {experts_disque:.2} Go lus sur NVMe à {NVME:.0} Go/s ({:.0} ms)",
            1000.0 * fixes / VRAM,
            1000.0 * experts_cache / VRAM,
            1000.0 * experts_disque / NVME)
    }

    pub fn resume(&self) -> String {
        let mut s = String::new();
        s.push_str(&format!(
            "CPU  {} cœurs physiques · {} threads logiques · {} sockets NUMA · \
caches L1 {} Ko · L2 {} Ko · L3 {} Ko\n",
            self.cpu.physiques, self.cpu.logiques, self.cpu.noeuds.len(),
            self.cpu.l1_ko, self.cpu.l2_ko, self.cpu.l3_ko));
        for n in &self.cpu.noeuds {
            s.push_str(&format!("     nœud {} : {} CPU · {:.0} Go\n",
                                n.id, n.cpus.len(), n.memoire_go));
        }
        s.push_str(&format!("RAM  {:.0} Go au total · {:.0} Go disponibles\n",
                            self.ram_totale_go, self.ram_libre_go));
        if self.gpus.is_empty() {
            s.push_str("GPU  aucun (nvidia-smi muet ou absent)\n");
        }
        for g in &self.gpus {
            s.push_str(&format!(
                "GPU  {} · {} · {:.1}/{:.1} Go libres · {} lien(s) NVLink\n",
                g.ordinal, g.nom, g.vram_libre_go, g.vram_totale_go, g.liens_nvlink));
        }
        for d in &self.disques {
            s.push_str(&format!("DISQ {} · {:.0} Go libres · nœud {}\n",
                                d.chemin, d.libre_go,
                                d.noeud.map(|n| n.to_string()).unwrap_or_else(|| "?".into())));
        }
        s
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn liste_cpus_lit_les_plages() {
        assert_eq!(liste_cpus("0-3"), vec![0, 1, 2, 3]);
        assert_eq!(liste_cpus("0-1,5,7-8"), vec![0, 1, 5, 7, 8]);
        assert_eq!(liste_cpus(""), Vec::<usize>::new());
    }

    /// La détection doit rendre quelque chose de cohérent sur n'importe quelle
    /// machine, y compris sans GPU ni /sys complet.
    #[test]
    fn detection_coherente() {
        let m = Materiel::detecter();
        assert!(m.cpu.physiques >= 1);
        assert!(m.cpu.logiques >= m.cpu.physiques,
                "il ne peut pas y avoir moins de threads que de cœurs");
        assert_eq!(m.cpu.paires.len(), m.cpu.physiques,
                   "une paire par cœur physique");
        let total: usize = m.cpu.paires.iter().map(|p| p.len()).sum();
        assert_eq!(total, m.cpu.logiques,
                   "les paires doivent couvrir tous les threads logiques");
    }

    /// Le plan doit tenir debout : threads bornés, lecteurs bornés, KV cohérent.
    #[test]
    fn plan_dans_les_bornes() {
        let m = Materiel::detecter();
        let p = m.plan(512, 1.0, 128, 3.05);
        assert!(p.threads >= 1 && p.threads <= m.cpu.logiques.max(1));
        assert!(p.lecteurs >= 1);
        assert!(p.kv_bits == 8 || p.kv_bits == 32);
        assert!(!p.raisons.is_empty(), "chaque choix doit être justifié");
        // Un contexte énorme doit faire basculer le KV en 8 bits.
        let grand = m.plan(1_048_576, 365.7, 384, 9.95);
        assert_eq!(grand.kv_bits, 8,
                   "à 1 M de jetons, le KV en F16 dépasse 96 Go : il doit passer en int8");
    }
}
