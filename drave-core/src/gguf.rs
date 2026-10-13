//! Lecteur GGUF minimal (std seul).
//!
#![allow(dead_code)] // lecteur générique : tous les formats ne servent pas au moteur

//! Ne lit que ce dont le moteur a besoin : métadonnées, descripteurs de tenseurs,
//! et les niveaux quantifiés (Q8_0 / Q4_0) ou les flottants (F32 / F16).

use std::collections::HashMap;
use std::fs::File;
use std::io::{Read, Seek, SeekFrom};
use std::ops::Deref;
use std::path::Path;

/// Résultat empruntant à `self`. Écrit à la main parce qu'un tenseur peut vivre
/// dans n'importe lequel des fichiers de l'assemblage.
type io_result<'a> = std::io::Result<&'a [u8]>;

/// Fichier **mappé** en mémoire plutôt que lu.
///
/// `read_to_end` fait deux choses coûteuses : il lit tout le fichier (18,55 Go
/// pour Qwen3-30B, 366 Go pour DeepSeek-V4.1-Flash) et il en garde une copie
/// dans le tas, en plus du cache de pages du noyau — soit deux fois la taille du
/// modèle en mémoire physique au premier accès.
///
/// Le mmap ne lit rien : il rend une plage d'adresses, et le noyau lit les pages
/// à la demande. Un modèle qu'on inspecte coûte quelques mégaoctets ; un modèle
/// dont on n'utilise qu'un huitième des experts ne lit qu'un huitième des
/// octets. Les pages touchées sont partagées avec le cache de pages, donc pas
/// dupliquées.
pub struct Mappe {
    ptr: *mut u8,
    len: usize,
}

// Le noyau ne déplace jamais une page mappée : ces deux implémentations sont
// sûres, et sans elles le moteur ne pourrait pas envoyer un `Gguf` à un fil.
unsafe impl Send for Mappe {}
unsafe impl Sync for Mappe {}

extern "C" {
    fn mmap(addr: *mut u8, len: usize, prot: i32, flags: i32, fd: i32, offset: i64) -> *mut u8;
    fn munmap(addr: *mut u8, len: usize) -> i32;
}

const PROT_READ: i32 = 1;
const MAP_PRIVATE: i32 = 2;

extern "C" {
    fn madvise(addr: *mut u8, len: usize, advice: i32) -> i32;
}

/// `MADV_WILLNEED` : « je vais lire cette plage, lance les lectures ».
const MADV_WILLNEED: i32 = 3;

/// Taille d'une demande de prélecture : **1 Mio**.
///
/// Mesuré le 12/10 (`tools/banc-experts.py`, 24 plages de 4 Mio dispersées, pages
/// parcourues dans l'ordre du calcul, array raid0, cache évincé entre les bras) :
///
/// | demande | plage entière | **par tranches de 1 Mio** | 8 fils en `pread` |
/// |---|---|---|---|
/// | 1 126 Mo/s | 1 191 Mo/s (**×1,06**) | **2 797 Mo/s (×2,5)** | 3 995 Mo/s (×3,5) |
///
/// Une demande sur la plage ENTIÈRE ne sert donc à rien : le noyau ne traite
/// qu'une fenêtre de lecture en avance par appel et le reste attend. Découpée en
/// tranches d'un mégaoctet, chaque appel porte sur une fenêtre entière — d'où le
/// facteur 2,5, sans une ligne de calcul en plus.
const TRANCHE_PRELECTURE: usize = 1 << 20;

/// Demande au noyau de **lancer en avance** les lectures d'une plage mappée.
///
/// C'est la seule forme de parallélisme de lecture accessible depuis l'espace
/// utilisateur quand les poids sont mmappés : on ne peut pas lire soi-même sans
/// renoncer au mmap. Le noyau, lui, peut lancer plusieurs lectures de pages en
/// parallèle — et c'est ce qui compte, parce que le NVMe passe de 5,4 Go/s à un
/// lecteur à **31 Go/s à seize**.
///
/// **Par tranches d'un mégaoctet** (voir `TRANCHE_PRELECTURE`) : la demande est
/// un appel par tranche, pas un appel pour la plage entière — mesuré, c'est le
/// facteur 2,5. `DRAVE_PRELIRE_TRANCHE=0` rend l'ancien comportement (une seule
/// demande), ce qui permet de refaire la mesure.
///
/// Ne fait rien si la plage n'est pas mappée (modèle lu en mémoire) : l'appel
/// est alors sans objet, pas faux.
pub fn prelire(ptr: *const u8, octets: usize) {
    if ptr.is_null() || octets == 0 { return; }
    // `DRAVE_PRELIRE=0` la désactive : sans ce témoin, on ne pourrait pas dire
    // si un gain vient d'elle ou du cache qui se réchauffe d'un passage à
    // l'autre.
    if !prelire_active() { return; }
    if !tranches_voulues() {
        unsafe { madvise(ptr as *mut u8, octets, MADV_WILLNEED); }
        return;
    }
    let mut fait = 0usize;
    while fait < octets {
        let n = TRANCHE_PRELECTURE.min(octets - fait);
        unsafe { madvise(ptr.add(fait) as *mut u8, n, MADV_WILLNEED); }
        fait += n;
    }
}

/// `DRAVE_PRELIRE_TRANCHE=0` : une seule demande pour la plage entière (l'ancien
/// comportement, gardé pour refaire la mesure qui a montré ×2,5).
fn tranches_voulues() -> bool {
    match std::env::var("DRAVE_PRELIRE_TRANCHE") {
        Ok(v) => !(v == "0" || v.eq_ignore_ascii_case("non") || v.eq_ignore_ascii_case("false")),
        Err(_) => true,
    }
}

/// Touche une adresse par page d'une plage : c'est ce qui **fait entrer les pages**.
///
/// `read_volatile` et non `read` : le compilateur a le droit de supprimer une lecture
/// dont personne ne lit le résultat, et il ne s'en prive pas — la prélecture
/// disparaîtrait alors du binaire sans que rien ne le dise.
unsafe fn toucher(addr: usize, octets: usize) {
    let p = addr as *const u8;
    let mut i = 0usize;
    while i < octets {
        std::ptr::read_volatile(p.add(i));
        i += 4096;
    }
}

/// `DRAVE_PRELIRE=0` coupe AUSSI la prélecture parallèle : sans cela, le bras témoin
/// « à la demande » ne serait plus à la demande, et la porte ne comparerait plus rien.
pub fn prelecture_active() -> bool { prelire_active() }

/// `DRAVE_PRELIRE_DENSE=1` : prélecturer aussi les poids **denses** de la couche suivante.
///
/// **Défaut : non — mesuré sans gain, et c'est un résultat.** Implémenté le 12/10 d'après
/// la lecture de Strata (« lire la couche suivante pendant que l'attention tourne »), puis
/// mesuré sur la même passe à 8 jetons, mêmes jetons, cache évincé entre les bras :
///
/// | bras | temps mural | octets lus | défauts majeurs |
/// |---|---|---|---|
/// | experts seuls (défaut) | **30,47 s** | 10,00 Go | 4 202 |
/// | experts + denses | 32,05 s | 10,00 Go | 4 229 |
///
/// La prélecture dense n'ajoute **rien** : le préchargement synchrone ne se recouvre pas
/// avec le calcul (il faut un fil dédié pour cela, et il faudra le mesurer à son tour), et
/// les octets lus sont les mêmes. Le témoin reste, parce qu'un « ça n'apporte rien »
/// mesuré vaut mieux qu'un « ça devrait aider » : c'est `DRAVE_PRELIRE_DENSE=1` qui
/// rejouera la mesure.
pub fn prelecture_dense_voulue() -> bool {
    matches!(std::env::var("DRAVE_PRELIRE_DENSE").as_deref(), Ok("1") | Ok("oui") | Ok("true"))
}

/// `DRAVE_PRELIRE_FILS` : nombre de fils de prélecture (défaut 8, `0` la remplace par
/// l'ancienne demande `madvise`).
pub fn fils_prelecture() -> usize {
    match std::env::var("DRAVE_PRELIRE_FILS") {
        Ok(v) => v.parse().unwrap_or(8),
        Err(_) => 8,
    }
}

/// Prélecture **parallèle** : `fils` fils entrent les pages des plages données.
///
/// POURQUOI PAS `madvise`. Mesuré le 12/10 (`tools/banc-experts.py` : 24 plages de 4 Mio
/// dispersées, pages parcourues dans l'ordre du calcul, cache évincé entre les bras) :
///
/// | demande (défauts de page) | `madvise` plage entière | `madvise` par tranches | **fils qui touchent** |
/// |---|---|---|---|
/// | 1 126 Mo/s | 1 191 Mo/s (×1,06) | 2 797 Mo/s (×2,5) | **3 995 Mo/s (×3,5)** |
///
/// Et dans le moteur, la granularité de `madvise` ne change rien du tout (31 s dans les
/// trois cas) : le noyau ne parallélise pas une demande de prélecture comme il parallélise
/// des défauts de page **simultanés**. Ici, ce sont donc les fils qui les lancent — c'est
/// la seule forme de parallélisme de lecture accessible sans renoncer au mmap.
///
/// Les adresses voyagent en `usize` : un pointeur brut n'est pas `Send`, et le dépôt a
/// déjà ce motif (`kimi_k3.rs`). Les plages viennent d'un mapping valable toute la vie du
/// processus : les toucher est sûr, et n'écrit rien.
pub fn prelecture_parallele(plages: &[(usize, usize)], fils: usize) {
    if plages.is_empty() || fils <= 1 {
        if let Some(&(addr, octets)) = plages.first() {
            unsafe { toucher(addr, octets); }
        }
        return;
    }
    let par_fil = plages.len().div_ceil(fils);
    std::thread::scope(|s| {
        for groupe in plages.chunks(par_fil) {
            s.spawn(move || {
                for &(addr, octets) in groupe {
                    unsafe { toucher(addr, octets); }
                }
            });
        }
    });
}

/// Demande au noyau de lancer la lecture du fichier ENTIER, une fois, au
/// chargement. Le noyau parallélise ses lectures de pages, là où le mmap
/// paresseux les déclenche une par une au fil des accès.
///
/// Mesuré : charger 18,6 Go prend 6,8 s en mmap paresseux (2,7 Go/s) — proche du
/// débit séquentiel du NVMe, et 4,5× mieux qu'une lecture complète (30,5 s).
/// Cette demande vise le débit parallèle, 31 Go/s.
///
/// Désactivée par défaut : sur un modèle plus gros que la RAM, elle chargerait
/// tout ce qu'on cherche justement à ne pas charger.
pub fn prelire_tout(ptr: *const u8, octets: usize) {
    if ptr.is_null() || octets == 0 { return; }
    unsafe { madvise(ptr as *mut u8, octets, MADV_WILLNEED); }
}

/// `DRAVE_PRELIRE_TOUT=1` : demander le fichier entier au chargement.
pub fn prelire_tout_voulu() -> bool {
    matches!(std::env::var("DRAVE_PRELIRE_TOUT").as_deref(), Ok("1") | Ok("oui") | Ok("true"))
}

fn prelire_active() -> bool {
    match std::env::var("DRAVE_PRELIRE") {
        Ok(v) => !(v == "0" || v.eq_ignore_ascii_case("non") || v.eq_ignore_ascii_case("false")),
        Err(_) => true,
    }
}

impl Mappe {
    /// Mappe le fichier entier en lecture seule.
    fn ouvrir(f: &File, len: usize) -> std::io::Result<Mappe> {
        use std::os::unix::io::AsRawFd;
        if len == 0 { return Ok(Mappe { ptr: std::ptr::null_mut(), len: 0 }); }
        let p = unsafe { mmap(std::ptr::null_mut(), len, PROT_READ, MAP_PRIVATE, f.as_raw_fd(), 0) };
        // `mmap` rend `MAP_FAILED` (soit -1) en cas d'échec.
        if p as isize == -1 {
            return Err(std::io::Error::last_os_error());
        }
        Ok(Mappe { ptr: p, len })
    }
}

impl Deref for Mappe {
    type Target = [u8];
    #[inline]
    fn deref(&self) -> &[u8] {
        if self.len == 0 { return &[]; }
        unsafe { std::slice::from_raw_parts(self.ptr, self.len) }
    }
}

impl Drop for Mappe {
    fn drop(&mut self) {
        if self.len > 0 { unsafe { munmap(self.ptr, self.len); } }
    }
}

/// Les octets d'un fichier, lus ou mappés.
///
/// Le reste du lecteur ne fait pas la différence : les deux variantes se
/// déréférencent en `&[u8]`. Le choix se fait une fois, à l'ouverture.
pub enum Tampon {
    Lu(Vec<u8>),
    Mappe(Mappe),
}

impl Deref for Tampon {
    type Target = [u8];
    #[inline]
    fn deref(&self) -> &[u8] {
        match self { Tampon::Lu(v) => v, Tampon::Mappe(m) => m }
    }
}

impl Tampon {
    pub fn len(&self) -> usize { (**self).len() }
    pub fn is_empty(&self) -> bool { self.len() == 0 }
}

// ------------------------------------------------------- lire dans NOS tampons
//
// POURQUOI. Mesuré le 12/10 : sur un motif d'experts, la lecture **à la demande** (défauts de
// page) rend 1 126 Mo/s, la prélecture par `madvise` ×1,06, des fils qui entrent les pages
// ×3,5 — et un `pread` explicite depuis huit fils **3 995 Mo/s** (`tools/banc-experts.py`).
// La différence n'est pas le parallélisme (les deux en ont) mais le **chemin** : un défaut de
// page fait une lecture par page, `pread` lit des plages entières dans une mémoire à nous.
//
// Ce que la direction du 12/10 demande : « favoriser une granularité fine de MoE en lecture
// séquentielle par allocation intelligente au lieu de virtualiser une grande mémoire en
// lecture aléatoire ». C'est ce que fait ce module : les plages des experts RETENUS, triées
// par **offset de fichier** (donc lues en séquentiel), lues en parallèle dans des tampons
// réutilisables — et le calcul lit ces tampons.
//
// Pour cela il faut savoir, pour une adresse mappée, **de quel fichier et de quel offset**
// elle vient. D'où ce registre, rempli à l'ouverture de chaque mapping : il évite d'ajouter
// deux champs à `Vue4` (et de toucher tous ses constructeurs).

struct MappeInscrite { base: usize, len: usize, chemin: std::path::PathBuf }

fn registre() -> &'static std::sync::Mutex<Vec<MappeInscrite>> {
    static R: std::sync::OnceLock<std::sync::Mutex<Vec<MappeInscrite>>> = std::sync::OnceLock::new();
    R.get_or_init(|| std::sync::Mutex::new(Vec::new()))
}

fn inscrire_mappe(base: usize, len: usize, chemin: &std::path::Path) {
    if let Ok(mut v) = registre().lock() {
        v.push(MappeInscrite { base, len, chemin: chemin.to_path_buf() });
    }
}

/// `(chemin du fichier, offset)` d'une adresse mappée — `None` si elle n'est pas mappée
/// (modèle lu en RAM : il n'y a alors rien à lire, tout est déjà là).
pub fn localiser(addr: usize) -> Option<(std::path::PathBuf, u64)> {
    let v = registre().lock().ok()?;
    v.iter()
        .find(|m| addr >= m.base && addr < m.base + m.len)
        .map(|m| (m.chemin.clone(), (addr - m.base) as u64))
}

/// Un descripteur par fichier, ouvert une fois : `pread` sur un descripteur déjà ouvert ne
/// paie ni `open` ni la résolution de chemin.
fn descripteurs() -> &'static std::sync::Mutex<std::collections::HashMap<std::path::PathBuf, std::fs::File>> {
    static D: std::sync::OnceLock<std::sync::Mutex<std::collections::HashMap<std::path::PathBuf, std::fs::File>>> =
        std::sync::OnceLock::new();
    D.get_or_init(|| std::sync::Mutex::new(std::collections::HashMap::new()))
}

fn descripteur(chemin: &std::path::Path) -> Option<std::fs::File> {
    let mut d = descripteurs().lock().ok()?;
    if let Some(f) = d.get(chemin) { return f.try_clone().ok(); }
    let f = std::fs::File::open(chemin).ok()?;
    d.insert(chemin.to_path_buf(), f.try_clone().ok()?);
    Some(f)
}

/// `DRAVE_TAMPONS=1` : lire les experts retenus en séquentiel dans des tampons, et faire
/// calculer le moteur **sur ces tampons** au lieu du mapping.
pub fn tampons_voulus() -> bool {
    matches!(std::env::var("DRAVE_TAMPONS").as_deref(), Ok("1") | Ok("oui") | Ok("true"))
}

/// Nombre de fils de lecture des tampons (`DRAVE_TAMPONS_FILS`, défaut : `DRAVE_PRELIRE_FILS`).
pub fn fils_tampons() -> usize {
    match std::env::var("DRAVE_TAMPONS_FILS") {
        Ok(v) => v.parse().unwrap_or(8),
        Err(_) => fils_prelecture().max(1),
    }
}

/// Lit des plages mappées dans des tampons **à nous**, en parallèle, **dans l'ordre du
/// fichier**. Rend un tampon par plage, dans l'ordre d'entrée (`None` si la plage n'est pas
/// mappée ou n'est pas lisible — l'appelant retombe alors sur le mapping).
pub fn lire_en_tampons(plages: &[(usize, usize)], fils: usize) -> Vec<Option<Box<[u8]>>> {
    let mut sortie: Vec<Option<Box<[u8]>>> = (0..plages.len()).map(|_| None).collect();
    // 1. résoudre chaque plage en (index, chemin, offset, octets)
    let mut taches: Vec<(usize, std::path::PathBuf, u64, usize)> = Vec::with_capacity(plages.len());
    for (i, &(addr, octets)) in plages.iter().enumerate() {
        if octets == 0 { continue; }
        if let Some((chemin, offset)) = localiser(addr) {
            taches.push((i, chemin, offset, octets));
        }
    }
    if taches.is_empty() { return sortie; }
    // 2. trier par (fichier, offset) : c'est ce qui rend la lecture SÉQUENTIELLE
    taches.sort_by(|a, b| a.1.cmp(&b.1).then(a.2.cmp(&b.2)));
    // 3. lire par tranches contiguës de la liste triée, un fil par tranche
    let par_fil = taches.len().div_ceil(fils.max(1));

    let resultats: std::sync::Mutex<Vec<(usize, Box<[u8]>)>> = std::sync::Mutex::new(Vec::new());
    let echecs = std::sync::atomic::AtomicUsize::new(0);
    std::thread::scope(|s| {
        for tranche in taches.chunks(par_fil) {
            let resultats = &resultats;
            let echecs = &echecs;
            s.spawn(move || {
                use std::os::unix::fs::FileExt;
                let mut fd: Option<(std::path::PathBuf, std::fs::File)> = None;
                for (i, chemin, offset, octets) in tranche {
                    if fd.as_ref().map(|(c, _)| c != chemin).unwrap_or(true) {
                        match descripteur(chemin) {
                            Some(f) => fd = Some((chemin.clone(), f)),
                            None => { echecs.fetch_add(1, std::sync::atomic::Ordering::Relaxed); continue; }
                        }
                    }
                    let f = &fd.as_ref().unwrap().1;
                    let mut buf = vec![0u8; *octets].into_boxed_slice();
                    // `read_exact_at` : pas de position partagée, donc pas de course entre fils
                    match f.read_exact_at(&mut buf, *offset) {
                        Ok(()) => { if let Ok(mut r) = resultats.lock() { r.push((*i, buf)); } }
                        Err(_) => { echecs.fetch_add(1, std::sync::atomic::Ordering::Relaxed); }
                    }
                }
            });
        }
    });
    for (i, buf) in resultats.into_inner().unwrap_or_default() {
        sortie[i] = Some(buf);
    }
    if echecs.load(std::sync::atomic::Ordering::Relaxed) > 0 {
        eprintln!("[tampons] {} plage(s) non lues — repli sur le mapping",
                  echecs.load(std::sync::atomic::Ordering::Relaxed));
    }
    sortie
}

/// Faut-il mapper les fichiers ? Mappé par défaut : c'est moins de mémoire et
/// moins d'octets lus. `DRAVE_MMAP=0` force la lecture complète (utile pour
/// comparer, ou sur un système de fichiers qui refuse le mmap).
fn mmap_voulu() -> bool {
    match std::env::var("DRAVE_MMAP") {
        Ok(v) => !(v == "0" || v.eq_ignore_ascii_case("non") || v.eq_ignore_ascii_case("false")),
        Err(_) => true,
    }
}

/// Ouvre un fichier entier, mappé ou lu.
fn ouvrir_tampon(chemin: &Path) -> std::io::Result<Tampon> {
    let f = File::open(chemin)?;
    let len = f.metadata()?.len() as usize;
    if mmap_voulu() {
        match Mappe::ouvrir(&f, len) {
            // On inscrit le mapping : c'est ce qui permet, plus tard, de retrouver le
            // FICHIER et l'OFFSET d'une adresse (lecture en tampons, `lire_en_tampons`).
            Ok(m) => { inscrire_mappe(m.ptr as usize, len, chemin); return Ok(Tampon::Mappe(m)) }
            Err(e) => eprintln!("[gguf] mmap refusé sur {} ({e}) : lecture complète",
                                chemin.display()),
        }
    }
    let mut buf = Vec::with_capacity(len);
    let mut f = f;
    f.read_to_end(&mut buf)?;
    Ok(Tampon::Lu(buf))
}

#[derive(Debug, Clone)]
pub enum Meta {
    U8(u8), I8(i8), U16(u16), I16(i16), U32(u32), I32(i32),
    F32(f32), Bool(bool), Str(String), Array(Vec<Meta>), U64(u64), I64(i64), F64(f64),
}

impl Meta {
    /// Une liste de métadonnées en entiers — `attention.compress_ratios` est une
    /// liste par couche, et c'est une **décision d'architecture** : quelles
    /// couches sont compressées, et à quel ratio. La lire comme un scalaire
    /// donnait `None`, donc « pas d'attention compressée ».
    pub fn as_liste_i64(&self) -> Option<Vec<i64>> {
        match self {
            Meta::Array(v) => v.iter().map(|m| m.as_u64().map(|x| x as i64)
                                           .or_else(|| match m { Meta::I64(x) => Some(*x), _ => None }))
                                  .collect(),
            _ => None,
        }
    }

    /// Une liste de métadonnées en flottants — `swiglu_clamp_exp` est une liste
    /// par couche, et la lire comme un scalaire donnerait « pas de clamp ».
    pub fn as_liste_f32(&self) -> Option<Vec<f32>> {
        match self {
            Meta::Array(v) => v.iter().map(|m| m.as_f64().map(|x| x as f32)
                .or_else(|| m.as_u64().map(|x| x as f32))).collect(),
            _ => None,
        }
    }

    pub fn as_u64(&self) -> Option<u64> {
        match self {
            Meta::U32(v) => Some(*v as u64),
            Meta::U64(v) => Some(*v),
            Meta::I32(v) => Some(*v as u64),
            Meta::I64(v) => Some(*v as u64),
            _ => None,
        }
    }
    pub fn as_bool(&self) -> Option<bool> {
        match self {
            Meta::Bool(v) => Some(*v),
            // Certains convertisseurs écrivent 0/1 là où le type GGUF est
            // BOOL : refuser ces fichiers ferait retomber sur le défaut, en
            // silence, une option que le modèle déclare explicitement.
            Meta::U8(v) => Some(*v != 0),
            Meta::U32(v) => Some(*v != 0),
            _ => None,
        }
    }
    pub fn as_f64(&self) -> Option<f64> {
        match self {
            Meta::F32(v) => Some(*v as f64),
            Meta::F64(v) => Some(*v),
            _ => None,
        }
    }
    pub fn as_str(&self) -> Option<&str> {
        match self { Meta::Str(s) => Some(s), _ => None }
    }
}

#[derive(Debug, Clone)]
pub struct TensorInfo {
    pub name: String,
    pub dims: Vec<u64>,     // en convention numpy (le plus lent d'abord)
    pub ttype: u32,
    pub offset: u64,
    /// Index du fichier qui porte ce tenseur. Un modèle « éclaté » (shards
    /// `-00001-of-00003`, ou notre format en clusters) est une seule liste de
    /// tenseurs répartie sur plusieurs fichiers : sans ce champ, `offset`
    /// désignerait le mauvais octet.
    pub fichier: usize,
}

impl TensorInfo {
    pub fn nelem(&self) -> usize { self.dims.iter().product::<u64>() as usize }
}

pub const GGML_F32: u32 = 0;
pub const GGML_F16: u32 = 1;
pub const GGML_Q4_0: u32 = 2;
pub const GGML_MXFP4: u32 = 39;
pub const GGML_Q2_K: u32 = 10;
pub const GGML_BF16: u32 = 30;
pub const GGML_Q3_K: u32 = 11;
pub const GGML_Q4_K: u32 = 12;
/// Bloc **Q5_0** (22 octets, 32 poids) et **Q5_1** (24 octets, 32 poids) :
/// échelle f16 (+ minimum f16 pour Q5_1), 4 octets de bits hauts, 16 octets de
/// quants 4 bits. Q5_0 est le type de `token_embd` et des `ffn_gate/up` de
/// Qwen2.5-0.5B en Q4_K_M — 62 % des poids de ce fichier : sans lui, le modèle
/// ne se charge pas du tout.
pub const GGML_Q5_0: u32 = 6;
pub const GGML_Q5_1: u32 = 7;
pub const GGML_Q5_K: u32 = 13;
pub const GGML_Q6_K: u32 = 14;
/// Types des experts de DeepSeek : IQ2_XXS (V4.1), IQ1_M (V4-Flash).
/// Sans ces constantes, `--bloc` les appelait « type 16 » et le lecteur les
/// refusait — un numéro en clair ne dit pas de quel encodage il s'agit.
pub const GGML_IQ2_XXS: u32 = 16;
/// IQ3_XXS : 98 octets par super-bloc de 256 poids (30 % des poids de Kimi,
/// GLM-5.3 et V4-Flash).
pub const GGML_IQ3_XXS: u32 = 18;
/// IQ1_S : 50 octets par super-bloc de 256 poids (42 à 45 % des poids de GLM).
pub const GGML_IQ1_S: u32 = 19;
/// IQ4_XS : 136 octets par super-bloc de 256 poids (2 % de GLM-5.3, mais un
/// seul type manquant suffit à refuser le modèle entier).
pub const GGML_IQ4_XS: u32 = 23;
pub const GGML_IQ1_M: u32 = 29;

/// BF16 : un f32 dont on ne garde que les 16 bits de poids fort. Le convertir
/// n'est pas une approximation — c'est exactement ce que le format stocke.
#[inline]
pub fn bf16_to_f32(h: u16) -> f32 { f32::from_bits((h as u32) << 16) }

/// Octets par super-bloc : Q4_K = 2+2+12+128 (256 poids), Q6_K = 128+64+16+2.
pub const TAILLE_Q4K: usize = 144;
pub const TAILLE_Q6K: usize = 210;
/// Bloc **Q5_K** : 2+2 octets (d, dmin) + 12 d'échelles + 32 de bits hauts
/// + 128 de quants 4 bits.
pub const TAILLE_Q5K: usize = 176;

/// Échelles et minima d'un sous-bloc Q4_K : huit paires de 6 bits tassées dans
/// douze octets. Les quatre premières paires sont dans les octets 0–7, les
/// quatre suivantes dans les octets 8–11, leurs deux bits hauts repris des
/// octets 0–7 — c'est le dépaquetage de `get_scale_min_k4` de ggml.
#[inline]
pub fn echelle_min_q4k(scales: &[u8], j: usize) -> (u8, u8) {
    if j < 4 {
        (scales[j] & 63, scales[j + 4] & 63)
    } else {
        ((scales[j + 4] & 0x0F) | ((scales[j - 4] >> 6) << 4),
         (scales[j + 4] >> 4) | ((scales[j] >> 6) << 4))
    }
}
pub const GGML_Q4_1: u32 = 3;
pub const GGML_Q8_0: u32 = 8;
/// I32 : entiers signés 32 bits, sans quantification. Utilisé par la table de
/// routage `ffn_gate_tid2eid` de DeepSeek-V4.
pub const GGML_I32: u32 = 26;

/// Pointeur pré-résolu vers les lignes d'un tenseur quantifié (Q8_0 ou Q4_0).
pub struct Q8View {
    /// Fichier qui porte le tenseur (un modèle éclaté en a plusieurs).
    pub fichier: usize,
    pub base: usize,
    pub n_cols: usize,
    pub nb: usize,
    pub q4: bool,
    /// Type ggml d'origine : la tête de sortie peut être Q8_0, Q4_0 ou Q4_K
    /// selon le modèle, et se lit **en place** dans les trois cas.
    pub ttype: u32,
}

pub struct Gguf {
    pub meta: HashMap<String, Meta>,
    pub tensors: Vec<TensorInfo>,
    /// Un tampon par fichier. Un GGUF ordinaire en a un seul ; un modèle
    /// découpé en porte autant que de morceaux. Les données ne sont jamais
    /// recopiées d'un fichier à l'autre : chaque tenseur reste chez lui.
    bufs: Vec<Tampon>,
    /// Début des données de chaque fichier (après l'en-tête, aligné).
    starts: Vec<usize>,
}

struct Cur<'a> { b: &'a [u8], p: usize, deborde: bool }

impl<'a> Cur<'a> {
    // Toutes les lectures sont bornées : un en-tête lu dans une tranche trop
    // courte doit être SIGNALÉ, pas provoquer une panique d'indexation. C'est
    // ce qui permet à `open_meta` de relire une tranche plus grande.
    fn reste(&self, n: usize) -> bool { self.p + n <= self.b.len() }
    fn u8(&mut self) -> u8 {
        if !self.reste(1) { self.deborde = true; return 0; }
        let v = self.b[self.p]; self.p += 1; v
    }
    fn u32(&mut self) -> u32 {
        if !self.reste(4) { self.deborde = true; return 0; }
        let v = u32::from_le_bytes(self.b[self.p..self.p+4].try_into().unwrap()); self.p += 4; v
    }
    fn u64(&mut self) -> u64 {
        if !self.reste(8) { self.deborde = true; return 0; }
        let v = u64::from_le_bytes(self.b[self.p..self.p+8].try_into().unwrap()); self.p += 8; v
    }
    fn i8(&mut self) -> i8 { self.u8() as i8 }
    fn u16(&mut self) -> u16 {
        if !self.reste(2) { self.deborde = true; return 0; }
        let v = u16::from_le_bytes(self.b[self.p..self.p+2].try_into().unwrap()); self.p += 2; v
    }
    fn i16(&mut self) -> i16 { self.u16() as i16 }
    fn i32(&mut self) -> i32 { self.u32() as i32 }
    fn f32(&mut self) -> f32 { f32::from_bits(self.u32()) }
    fn f64(&mut self) -> f64 { f64::from_bits(self.u64()) }
    fn i64(&mut self) -> i64 { self.u64() as i64 }
    fn string(&mut self) -> String {
        let n = self.u64() as usize;
        if !self.reste(n) { self.deborde = true; return String::new(); }
        let s = String::from_utf8_lossy(&self.b[self.p..self.p + n]).to_string();
        self.p += n;
        s
    }
    fn value(&mut self, vt: u32) -> Meta {
        match vt {
            0 => Meta::U8(self.u8()),
            1 => Meta::I8(self.i8()),
            2 => Meta::U16(self.u16()),
            3 => Meta::I16(self.i16()),
            4 => Meta::U32(self.u32()),
            5 => Meta::I32(self.i32()),
            6 => Meta::F32(self.f32()),
            7 => Meta::Bool(self.u8() != 0),   // 1 octet, pas 4 !
            8 => Meta::Str(self.string()),
            9 => {
                let et = self.u32();
                let n = self.u64() as usize;
                Meta::Array((0..n).map(|_| self.value(et)).collect())
            }
            10 => Meta::U64(self.u64()),
            11 => Meta::I64(self.i64()),
            12 => Meta::F64(self.f64()),
            _ => panic!("type de métadonnée inconnu : {vt}"),
        }
    }
}

impl Gguf {
    pub fn open<P: AsRef<Path>>(path: P) -> std::io::Result<Self> {
        let buf = ouvrir_tampon(path.as_ref())?;
        let (meta, tensors, fin) = Self::entete(&buf).ok_or_else(|| {
            std::io::Error::new(std::io::ErrorKind::UnexpectedEof, "en-tête GGUF incomplet")
        })?;
        let data_start = Self::debut_donnees(&meta, fin);
        if prelire_tout_voulu() {
            if let Some(t) = buf.deref().first() {
                let _ = t;
            }
            prelire_tout(buf.deref().as_ptr(), buf.len());
        }
        Ok(Gguf { meta, tensors, bufs: vec![buf], starts: vec![data_start] })
    }

    /// Ouvre un GGUF en ne lisant QUE l'en-tête (métadonnées et descripteurs de
    /// tenseurs) : `open` lit tout le fichier, soit **62 Go de lecture et de
    /// mémoire** pour gpt-oss. Le décodage du vocabulaire (`--tokenize`) et le
    /// garde-fou de vocabulaire de `--ppl` n'ont besoin que de l'en-tête.
    ///
    /// Les données de tenseurs ne sont PAS chargées : tout accès aux poids
    /// paniquera (bruyamment, c'est voulu) — ce constructeur ne sert qu'aux
    /// métadonnées.
    pub fn open_meta<P: AsRef<Path>>(path: P) -> std::io::Result<Self> {
        let mut f = File::open(&path)?;
        let mut taille = 4usize << 20;              // 4 Mo : l'en-tête usuel tient
        loop {
            f.seek(SeekFrom::Start(0))?;
            let mut buf = vec![0u8; taille];
            let mut lu = 0usize;
            while lu < taille {
                let n = f.read(&mut buf[lu..])?;
                if n == 0 { break; }
                lu += n;
            }
            buf.truncate(lu);
            if let Some((meta, tensors, fin)) = Self::entete(&buf) {
                let data_start = Self::debut_donnees(&meta, fin);
                return Ok(Gguf { meta, tensors, bufs: Vec::new(), starts: vec![data_start] });
            }
            if lu < taille {
                return Err(std::io::Error::new(std::io::ErrorKind::UnexpectedEof,
                                               "en-tête GGUF incomplet"));
            }
            taille *= 4;
        }
    }

    /// Ouvre un modèle **éclaté en plusieurs fichiers** : soit les shards d'un
    /// GGUF découpé (`…-00001-of-00003.gguf`), soit notre format en clusters
    /// (`commun.gguf` + `cluster-XX.gguf`).
    ///
    /// Règles, toutes dictées par ce qu'on a observé sur les fichiers réels :
    ///
    /// * les métadonnées sont prises au **premier fichier qui en porte** — un
    ///   GGUF découpé les duplique sur chaque shard, un modèle en clusters ne
    ///   les met que dans `commun.gguf`, et le second shard de
    ///   DeepSeek-V4-Flash porte 784 tenseurs sans aucune métadonnée ;
    /// * les tenseurs sont concaténés **dans l'ordre des chemins**, chacun
    ///   gardant le numéro du fichier qui le porte (les offsets sont relatifs
    ///   au début des données de CE fichier) ;
    /// * un nom de tenseur présent deux fois est **refusé**, sauf si les deux
    ///   copies sont identiques en tout point : c'est le symptôme d'un
    ///   assemblage incohérent, et un doublon silencieux ferait lire les poids
    ///   du mauvais fichier sans que rien ne le signale.
    pub fn open_multi<P: AsRef<Path>>(chemins: &[P]) -> std::io::Result<Self> {
        let vides: Vec<&str> = vec![""; chemins.len()];
        Self::open_avec_prefixes(chemins, &vides)
    }

    /// Comme [`Gguf::open_multi`], en préfixant les tenseurs de chaque fichier.
    /// Sert au format en clusters : chaque fichier de cluster porte les MÊMES
    /// noms de tenseurs d'experts, et le préfixe est ce qui les distingue.
    pub fn open_avec_prefixes<P: AsRef<Path>>(chemins: &[P], prefixes: &[&str])
        -> std::io::Result<Self> {
        assert_eq!(chemins.len(), prefixes.len(), "un préfixe par fichier");
        if chemins.is_empty() {
            return Err(std::io::Error::new(std::io::ErrorKind::InvalidInput,
                                           "open_multi : aucun fichier"));
        }
        let mut meta: Option<HashMap<String, Meta>> = None;
        let mut tous: Vec<TensorInfo> = Vec::new();
        let mut bufs: Vec<Tampon> = Vec::with_capacity(chemins.len());
        let mut starts: Vec<usize> = Vec::with_capacity(chemins.len());
        let mut arch_ref: Option<String> = None;
        for (i, c) in chemins.iter().enumerate() {
            let buf = ouvrir_tampon(c.as_ref())?;
            let (m, ts, fin) = Self::entete_de(&buf, i, prefixes[i]).ok_or_else(|| {
                std::io::Error::new(std::io::ErrorKind::UnexpectedEof,
                    format!("en-tête GGUF incomplet : {}", c.as_ref().display()))
            })?;
            if m.contains_key("general.architecture") {
                match &arch_ref {
                    None => arch_ref = m.get("general.architecture")
                        .and_then(|v| v.as_str()).map(str::to_string),
                    Some(a) => {
                        let ici = m.get("general.architecture").and_then(|v| v.as_str());
                        if ici != Some(a.as_str()) {
                            return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
                                format!("architectures divergentes : {a} puis {ici:?} dans {}",
                                        c.as_ref().display())));
                        }
                    }
                }
                if meta.is_none() { meta = Some(m); }
            }
            // Tant qu'aucun fichier n'a donné ses métadonnées, on aligne sur la
            // valeur par défaut de GGUF (32). Les fichiers réels partagent tous
            // la même ; l'alignement n'est pas une propriété par fichier.
            let ds = match &meta {
                Some(m) => Self::debut_donnees(m, fin),
                None => Self::debut_donnees(&HashMap::new(), fin),
            };
            starts.push(ds);
            bufs.push(buf);
            for t in ts {
                if let Some(v) = tous.iter().find(|u| u.name == t.name) {
                    // Tolérance voulue : un même tenseur recopié à l'identique
                    // (certains découpages dupliquent les petits tenseurs) n'est
                    // pas une faute. Deux contenus différents, si.
                    let meme = v.dims == t.dims && v.ttype == t.ttype
                        && Self::octets_de(&bufs, &starts, &t)?
                            == Self::octets_de(&bufs, &starts, v)?;
                    if !meme {
                        return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
                            format!("tenseur « {} » présent deux fois, contenu différent \
                                     ({} et {})", t.name, v.fichier, t.fichier)));
                    }
                    continue;
                }
                tous.push(t);
            }
        }
        let meta = meta.ok_or_else(|| std::io::Error::new(std::io::ErrorKind::InvalidData,
            "aucun fichier ne porte de métadonnées (general.architecture absent partout)"))?;
        Ok(Gguf { meta, tensors: tous, bufs, starts })
    }

    /// Reconnaît un nom de shard `…-00002-of-00007.gguf`.
    ///
    /// Rend `(préfixe, numéro, total)`. Le numéro doit être un groupe de
    /// chiffres : un modèle dont le nom contiendrait « -of- » par hasard ne doit
    /// pas être pris pour un découpage.
    pub fn shard_de(nom: &str) -> Option<(String, usize, usize)> {
        let base = nom.strip_suffix(".gguf")?;
        let (avant, apres) = base.rsplit_once("-of-")?;
        let total: usize = apres.parse().ok()?;
        let (prefixe, num) = avant.rsplit_once('-')?;
        if num.is_empty() || !num.bytes().all(|c| c.is_ascii_digit()) { return None; }
        let n: usize = num.parse().ok()?;
        if n == 0 || total == 0 { return None; }
        Some((prefixe.to_string(), n, total))
    }

    /// Liste des fichiers d'un modèle : un seul, ou tous les shards dans l'ordre.
    ///
    /// C'est ce qui permet de désigner un modèle découpé par **n'importe lequel**
    /// de ses morceaux — on écrit le chemin du shard 1 comme avant, et le moteur
    /// va chercher les autres. Un shard manquant est une **erreur**, pas un
    /// silence : sans lui, des tenseurs seraient absents et le moteur
    /// paniquerait bien plus loin, sur un message qui ne dirait pas pourquoi.
    pub fn chemins_du_modele(path: &Path) -> std::io::Result<Vec<std::path::PathBuf>> {
        let nom = path.file_name().and_then(|n| n.to_str()).unwrap_or("");
        let Some((prefixe, _, total)) = Self::shard_de(nom) else {
            return Ok(vec![path.to_path_buf()]);
        };
        // `parent()` d'un nom nu rend `Some("")`, et `read_dir("")` échoue : le
        // fichier existe pourtant, dans le dossier courant.
        let dir = match path.parent() {
            Some(d) if !d.as_os_str().is_empty() => d,
            _ => Path::new("."),
        };
        let mut trouves: Vec<(usize, std::path::PathBuf)> = Vec::new();
        for e in std::fs::read_dir(dir)? {
            let p = e?.path();
            let n = p.file_name().and_then(|n| n.to_str()).unwrap_or("").to_string();
            if let Some((pref, num, tot)) = Self::shard_de(&n) {
                if pref == prefixe && tot == total { trouves.push((num, p)); }
            }
        }
        trouves.sort();
        if trouves.len() != total {
            return Err(std::io::Error::new(std::io::ErrorKind::NotFound, format!(
                "modèle découpé incomplet dans {} : {total} shards annoncés, {} présents",
                dir.display(), trouves.len())));
        }
        for (attendu, (num, p)) in trouves.iter().enumerate() {
            if *num != attendu + 1 {
                return Err(std::io::Error::new(std::io::ErrorKind::NotFound, format!(
                    "shard {} manquant (trouvé {}) dans {}", attendu + 1, p.display(), dir.display())));
            }
        }
        Ok(trouves.into_iter().map(|(_, p)| p).collect())
    }

    /// Combien de shards d'un modèle découpé sont **présents** : `(présents, total)`.
    /// `None` si le chemin n'est pas un shard numéroté.
    ///
    /// Sert à `--config` : un modèle **en cours de téléchargement** doit pouvoir
    /// être interrogé — sinon il faut attendre la fin du transfert (des heures
    /// pour 1,5 To) pour savoir seulement ce que le fichier contient. La liste
    /// rendue est alors PARTIELLE, et l'appelant doit le dire.
    pub fn shards_presents(path: &Path) -> Option<(usize, usize)> {
        let nom = path.file_name().and_then(|n| n.to_str())?;
        let (prefixe, _, total) = Self::shard_de(nom)?;
        let dir = match path.parent() {
            Some(d) if !d.as_os_str().is_empty() => d,
            _ => Path::new("."),
        };
        let mut presents = 0usize;
        for e in std::fs::read_dir(dir).ok()? {
            let p = e.ok()?.path();
            let n = p.file_name().and_then(|n| n.to_str()).unwrap_or("").to_string();
            if let Some((pref, _, tot)) = Self::shard_de(&n) {
                if pref == prefixe && tot == total { presents += 1; }
            }
        }
        Some((presents, total))
    }

    /// Ouvre un modèle, découpé ou non : la même commande marche pour les deux.
    ///
    /// Un **dossier** qui contient `commun.gguf` est un modèle au format
    /// clusters : il s'ouvre comme les autres, sans option supplémentaire. Le
    /// mapping est publié au passage, c'est lui qui dira où sont les experts.
    pub fn open_auto<P: AsRef<Path>>(path: P) -> std::io::Result<Self> {
        let p = path.as_ref();
        if p.is_dir() {
            if !p.join("commun.gguf").is_file() {
                return Err(std::io::Error::new(std::io::ErrorKind::NotFound, format!(
                    "{} est un dossier mais ne contient pas commun.gguf", p.display())));
            }
            return Ok(crate::clusters::ouvrir(p)?.gguf);
        }
        let chemins = Self::chemins_du_modele(p)?;
        if chemins.len() > 1 { Self::open_multi(&chemins) } else { Self::open(path) }
    }

    /// Idem, sans lire les poids.
    pub fn open_meta_auto<P: AsRef<Path>>(path: P) -> std::io::Result<Self> {
        let p = path.as_ref();
        if p.is_dir() {
            return Ok(crate::clusters::ouvrir_meta(p)?.gguf);
        }
        let chemins = Self::chemins_du_modele(p)?;
        if chemins.len() > 1 { Self::open_multi_meta(&chemins) } else { Self::open_meta(path) }
    }

    /// Même chose que [`Gguf::open_multi`], mais **sans lire les poids** : seuls
    /// les en-têtes sont lus, par tranches croissantes.
    ///
    /// C'est ce qui rend un modèle de 366 Go inspectable : l'inventaire des
    /// tenseurs et des métadonnées coûte quelques mégaoctets de lecture au lieu
    /// de la totalité du fichier. Aucun accès aux poids ne doit suivre.
    pub fn open_multi_meta<P: AsRef<Path>>(chemins: &[P]) -> std::io::Result<Self> {
        let vides: Vec<&str> = vec![""; chemins.len()];
        Self::open_meta_avec_prefixes(chemins, &vides)
    }

    /// Comme [`Gguf::open_avec_prefixes`], mais sans lire les poids.
    pub fn open_meta_avec_prefixes<P: AsRef<Path>>(chemins: &[P], prefixes: &[&str])
        -> std::io::Result<Self> {
        assert_eq!(chemins.len(), prefixes.len(), "un préfixe par fichier");
        if chemins.is_empty() {
            return Err(std::io::Error::new(std::io::ErrorKind::InvalidInput,
                                           "open_multi_meta : aucun fichier"));
        }
        let mut meta: Option<HashMap<String, Meta>> = None;
        let mut tous: Vec<TensorInfo> = Vec::new();
        let mut starts: Vec<usize> = Vec::new();
        let mut arch_ref: Option<String> = None;
        for (i, c) in chemins.iter().enumerate() {
            let mut f = File::open(c.as_ref())?;
            let mut taille = 4usize << 20;
            let (m, ts, fin) = loop {
                f.seek(SeekFrom::Start(0))?;
                let mut buf = vec![0u8; taille];
                let mut lu = 0usize;
                while lu < taille {
                    let n = f.read(&mut buf[lu..])?;
                    if n == 0 { break; }
                    lu += n;
                }
                buf.truncate(lu);
                if let Some(r) = Self::entete_de(&buf, i, prefixes[i]) { break r; }
                if lu < taille {
                    return Err(std::io::Error::new(std::io::ErrorKind::UnexpectedEof,
                        format!("en-tête GGUF incomplet : {}", c.as_ref().display())));
                }
                taille *= 4;
            };
            if m.contains_key("general.architecture") {
                match &arch_ref {
                    None => arch_ref = m.get("general.architecture")
                        .and_then(|v| v.as_str()).map(str::to_string),
                    Some(a) => {
                        let ici = m.get("general.architecture").and_then(|v| v.as_str());
                        if ici != Some(a.as_str()) {
                            return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
                                format!("architectures divergentes : {a} puis {ici:?} dans {}",
                                        c.as_ref().display())));
                        }
                    }
                }
                if meta.is_none() { meta = Some(m); }
            }
            starts.push(match &meta {
                Some(m) => Self::debut_donnees(m, fin),
                None => Self::debut_donnees(&HashMap::new(), fin),
            });
            for t in ts {
                // Doublon : en mode en-tête seul on ne peut pas comparer les
                // octets. On compare ce qu'on a — dimensions et type — et on
                // SIGNALE une divergence au lieu de l'avaler.
                if let Some(v) = tous.iter().find(|u| u.name == t.name) {
                    if v.dims != t.dims || v.ttype != t.ttype {
                        return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
                            format!("tenseur « {} » présent deux fois, dimensions ou type \
différents ({} et {})", t.name, v.fichier, t.fichier)));
                    }
                    continue;
                }
                tous.push(t);
            }
        }
        let meta = meta.ok_or_else(|| std::io::Error::new(std::io::ErrorKind::InvalidData,
            "aucun fichier ne porte de métadonnées (general.architecture absent partout)"))?;
        Ok(Gguf { meta, tensors: tous, bufs: Vec::new(), starts })
    }

    /// Octets d'un tenseur décrit par `t`, dans un assemblage en cours de
    /// construction (le `Gguf` n'existe pas encore).
    fn octets_de<'a>(bufs: &'a [Tampon], starts: &[usize], t: &TensorInfo) -> io_result<'a> {
        let besoin = Self::octets_tensor(t) as usize;
        let debut = starts[t.fichier] + t.offset as usize;
        let b = &bufs[t.fichier];
        // Le DÉBUT doit être borné aussi : un décalage aberrant ne doit pas
        // paniquer sur une tranche, mais se dire « assemblage incohérent ».
        if debut > b.len() {
            return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, format!(
                "tenseur « {} » : début {debut} au-delà du fichier {} ({} octets)",
                t.name, t.fichier, b.len())));
        }
        if debut + besoin > b.len() {
            return Err(std::io::Error::new(std::io::ErrorKind::UnexpectedEof, format!(
                "tenseur « {} » : {besoin} octets annoncés, {} disponibles dans le fichier {}",
                t.name, b.len() - debut, t.fichier)));
        }
        Ok(&b[debut..debut + besoin])
    }

    /// Taille en octets des données d'un tenseur, d'après son type ggml.
    /// `nelem()` compte des POIDS ; les types quantifiés rangent 32 ou 256
    /// poids par bloc, donc la taille n'est pas `nelem × taille d'un poids`.
    ///
    /// La table est celle de ggml, **relevée** et non devinée : un petit
    /// programme lié à `libggml` imprime `ggml_blck_size`/`ggml_type_size` pour
    /// chaque type (voir `docs/format-clusters.md`). Une taille inventée ferait
    /// un inventaire faux, et c'est exactement ainsi que l'inventaire de
    /// DeepSeek-V4-Flash a annoncé 8,56 Go pour 86,9 Go de fichiers : les
    /// tenseurs d'experts en `iq1_m` n'étaient pas dans la table.
    pub fn octets_tensor(t: &TensorInfo) -> u64 {
        if let Some(v) = Self::octets_tensor_opt(t) { return v; }
        // Un type hors table est compté zéro : le total serait faux, et c'est
        // ainsi qu'un inventaire a annoncé 8,56 Go pour 86,9 Go de fichiers
        // (les tenseurs d'experts en `iq1_m` n'étaient pas dans la table). On le
        // dit, une fois par type, plutôt que de rendre un chiffre trop petit.
        static SIGNALES: std::sync::Mutex<Vec<u32>> = std::sync::Mutex::new(Vec::new());
        if let Ok(mut v) = SIGNALES.lock() {
            if !v.contains(&t.ttype) {
                v.push(t.ttype);
                eprintln!("[gguf] type {} inconnu (tenseur « {} ») : sa taille compte pour \
zéro, l'inventaire sera sous-évalué", t.ttype, t.name);
            }
        }
        0
    }

    /// Taille d'un tenseur, ou `None` si son type n'est pas dans la table.
    pub fn octets_tensor_opt(t: &TensorInfo) -> Option<u64> {
        let n = t.nelem() as u64;
        let (bloc, octets) = match t.ttype {
            0 => (1u64, 4u64), 1 => (1, 2), 2 => (32, 18), 3 => (32, 20),
            6 => (32, 22), 7 => (32, 24), 8 => (32, 34), 9 => (32, 36),
            10 => (256, 84), 11 => (256, 110), 12 => (256, TAILLE_Q4K as u64),
            13 => (256, 176), 14 => (256, TAILLE_Q6K as u64), 15 => (256, 292),
            16 => (256, 66), 17 => (256, 74), 18 => (256, 98), 19 => (256, 50),
            20 => (32, 18), 21 => (256, 110), 22 => (256, 82), 23 => (256, 136),
            24 => (1, 1), 25 => (1, 2), 26 => (1, 4), 27 => (1, 8), 28 => (1, 8),
            29 => (256, 56), 30 => (1, 2), 34 => (256, 54), 35 => (256, 66),
            39 => (32, 17), 40 => (64, 36),
            // Types ajoutés à ggml après NVFP4. Noms lus dans `ggml.h`, tailles
            // relevées par `tools/verifier_table_types.sh` — qui les liste aussi
            // longtemps qu'ils manquent ici.
            41 => (128, 18), 42 => (64, 18), 43 => (32, 26), 44 => (32, 28),
            45 => (32, 14), 46 => (32, 16), 47 => (32, 10), 48 => (32, 12),
            _ => return None,
        };
        Some(n / bloc * octets)
    }

    /// Nom lisible d'un type ggml. Rend `« type 29 »` pour un type inconnu
    /// plutôt que `?` : un point d'interrogation ne dit pas lequel.
    pub fn nom_type(ttype: u32) -> String {
        let n = match ttype {
            0 => "F32", 1 => "F16", 2 => "Q4_0", 3 => "Q4_1", 6 => "Q5_0", 7 => "Q5_1",
            8 => "Q8_0", 9 => "Q8_1", 10 => "Q2_K", 11 => "Q3_K", 12 => "Q4_K",
            13 => "Q5_K", 14 => "Q6_K", 15 => "Q8_K",
            16 => "IQ2_XXS", 17 => "IQ2_XS", 18 => "IQ3_XXS", 19 => "IQ1_S",
            20 => "IQ4_NL", 21 => "IQ3_S", 22 => "IQ2_S", 23 => "IQ4_XS",
            24 => "I8", 25 => "I16", 26 => "I32", 27 => "I64", 28 => "F64",
            29 => "IQ1_M", 30 => "BF16", 34 => "TQ1_0", 35 => "TQ2_0",
            39 => "MXFP4", 40 => "NVFP4",
            41 => "Q1_0", 42 => "Q2_0", 43 => "Q6_0", 44 => "Q6_1",
            45 => "Q3_0", 46 => "Q3_1", 47 => "Q2_0S", 48 => "Q2_1",
            _ => return format!("type {ttype}"),
        };
        n.to_string()
    }

    /// Somme des tailles de données annoncées par les descripteurs.
    pub fn octets_poids(&self) -> u64 {
        self.tensors.iter().map(Self::octets_tensor).sum()
    }

    /// Nombre de fichiers de l'assemblage. `starts` fait foi et non `bufs` :
    /// en mode en-tête seul (`--tensors`), les tampons ne sont pas chargés mais
    /// le découpage, lui, est connu.
    pub fn nb_fichiers(&self) -> usize { self.starts.len() }

    /// Octets de poids effectivement lus (somme des fichiers).
    pub fn octets_charges(&self) -> u64 { self.bufs.iter().map(|b| b.len() as u64).sum() }

    /// Les fichiers sont-ils mappés (vrai) ou lus en mémoire (faux) ?
    pub fn est_mappe(&self) -> bool { self.bufs.iter().any(|b| matches!(b, Tampon::Mappe(_))) }

    /// Analyse l'en-tête d'UN fichier ; `fichier` marque l'origine des tenseurs.
    fn entete(buf: &[u8]) -> Option<(HashMap<String, Meta>, Vec<TensorInfo>, usize)> {
        Self::entete_de(buf, 0, "")
    }

    /// Idem, en préfixant les noms de tenseurs. C'est ce qui permet de réunir
    /// des fichiers de clusters : huit clusters portent chacun un tenseur nommé
    /// `blk.0.ffn_gate_exps.weight` (16 experts chacun), et sans préfixe ils
    /// seraient huit fois le même nom.
    fn entete_de(buf: &[u8], fichier: usize, prefixe: &str)
        -> Option<(HashMap<String, Meta>, Vec<TensorInfo>, usize)> {
        if buf.len() < 4 || &buf[0..4] != b"GGUF" { return None; }
        let mut c = Cur { b: buf, p: 4, deborde: false };
        let version = c.u32();
        assert!(version >= 2, "version GGUF {version} non gérée");
        let n_tensors = c.u64() as usize;
        let n_kv = c.u64() as usize;
        if c.deborde { return None; }

        let mut meta = HashMap::new();
        for _ in 0..n_kv {
            let k = c.string();
            let vt = c.u32();
            let v = c.value(vt);
            if c.deborde { return None; }
            meta.insert(k, v);
        }
        let mut tensors = Vec::with_capacity(n_tensors);
        for _ in 0..n_tensors {
            let name = c.string();
            let nd = c.u32() as usize;
            let mut dims: Vec<u64> = (0..nd).map(|_| c.u64()).collect();
            dims.reverse();                       // ggml stocke à l'envers
            let ttype = c.u32();
            let offset = c.u64();
            if c.deborde { return None; }
            let name = if prefixe.is_empty() { name } else { format!("{prefixe}{name}") };
            tensors.push(TensorInfo { name, dims, ttype, offset, fichier });
        }
        Some((meta, tensors, c.p))
    }

    /// Tranche d'octets d'un tenseur, exposée pour les outils de vérification
    /// (`--bloc`), qui doivent lire exactement ce que lit le moteur.
    pub fn tranche_publique(&self, nom: &str) -> Option<&[u8]> {
        self.tensor(nom).map(|t| self.tbuf(t))
    }

    /// Tranche d'octets d'un tenseur, à partir de son premier octet.
    ///
    /// C'est le SEUL point d'accès aux poids : rendre le fichier explicite ici
    /// plutôt que de le laisser implicite est ce qui permet de servir un modèle
    /// éclaté sans dupliquer le code de lecture.
    #[inline]
    /// Les octets d'un tenseur, par son nom — la même vue que `tbuf`, exposée
    /// pour les lecteurs qui ne déquantifient pas (l'engram lit ses rangées de
    /// 264 octets telles quelles).
    pub fn octets_tenseur(&self, nom: &str) -> Option<&[u8]> {
        let t = self.tensor(nom)?;
        let buf = self.bufs.get(t.fichier)?;
        let debut = self.starts[t.fichier] + t.offset as usize;
        let n = t.nelem();
        buf.get(debut..debut + n)
    }

    fn tbuf(&self, t: &TensorInfo) -> &[u8] {
        match self.bufs.get(t.fichier) {
            Some(b) => &b[self.starts[t.fichier] + t.offset as usize..],
            None => panic!(
                "données de « {} » absentes : GGUF ouvert en mode en-tête seul (--meta)",
                t.name),
        }
    }

    fn debut_donnees(meta: &HashMap<String, Meta>, fin_entete: usize) -> usize {
        let align = meta.get("general.alignment").and_then(|m| m.as_u64()).unwrap_or(32) as usize;
        (fin_entete + align - 1) / align * align
    }

    pub fn cfg(&self, key: &str) -> Option<&Meta> {
        let arch = self.meta.get("general.architecture")?.as_str()?;
        self.meta.get(&format!("{arch}.{key}"))
    }

    /// Première clef PRÉSENTE parmi plusieurs noms possibles.
    ///
    /// Deux conventions de nommage coexistent dans les GGUF de cette machine :
    /// les clefs normalisées de llama.cpp (`expert_count`, `expert_used_count`)
    /// et les noms d'origine de DeepSeek, recopiés tels quels par le
    /// convertisseur (`n_routed_experts`, `num_experts_per_tok`). Lire une seule
    /// convention ne donne pas une erreur : cela donne `n_expert = 0`, donc un
    /// modèle **sans experts** — un V4.1 qui tourne en dense et dont la
    /// perplexité ne veut plus rien dire.
    pub fn cfg_ou(&self, cles: &[&str]) -> Option<&Meta> {
        cles.iter().find_map(|c| self.cfg(c))
    }

    /// Les ratios de compression, **couche par couche** (0 = brute).
    pub fn couches_ratios(&self) -> Vec<i64> {
        self.cfg_ou(&["attention.compress_ratios", "compress_ratios"])
            .and_then(|m| m.as_liste_i64())
            .unwrap_or_default()
    }

    /// **Quelles couches ont une attention compressée** (`attention.compress_ratios`
    /// ≠ 0). C'est ce qui décide si une exécution BORNÉE est légitime : les
    /// couches 0 et 1 de V4-Flash n'en ont pas, donc on peut les exécuter —
    /// et les comparer à la référence — avant que la compression existe.
    pub fn couches_compressees(&self) -> Vec<usize> {
        self.cfg_ou(&["attention.compress_ratios", "compress_ratios"])
            .and_then(|m| m.as_liste_i64())
            .map(|v| v.iter().enumerate().filter(|(_, r)| **r != 0).map(|(i, _)| i).collect())
            .unwrap_or_default()
    }

    /// Les trois hyper-paramètres des **hyper-connexions** de DeepSeek-V4 :
    /// `(hc_mult, sinkhorn_iterations, epsilon)`.
    ///
    /// Deux sources, et il faut les DEUX : V4-Flash les déclare en clés GGUF
    /// normalisées (`deepseek4.hyper_connection.*`), V4.1 seulement dans le
    /// `config.json` recopié sous `deepseek41.config` (`hc_mult`,
    /// `hc_sinkhorn_iters`, `hc_eps`). N'en lire qu'une donne « pas
    /// d'hyper-connexions » sur un modèle qui en a — un silence, pas une erreur.
    pub fn hc_params(&self) -> Option<(usize, usize, f32)> {
        let entier = |cles: &[&str], json: &str| -> Option<usize> {
            self.cfg_ou(cles).and_then(|m| m.as_u64()).map(|v| v as usize)
                .or_else(|| self.json_nombre(json).map(|v| v as usize))
        };
        let mult = entier(&["hyper_connection.count"], "hc_mult")?;
        let iters = entier(&["hyper_connection.sinkhorn_iterations"], "hc_sinkhorn_iters")
            .unwrap_or(20);
        let eps = self.cfg_ou(&["hyper_connection.epsilon"]).and_then(|m| m.as_f64())
            .map(|v| v as f32)
            .or_else(|| self.json_nombre("hc_eps").map(|v| v as f32))
            .unwrap_or(1e-6);
        Some((mult, iters, eps))
    }

    /// Chaîne du bloc `<arch>.config` — le JSON d'origine, recopié par le
    /// convertisseur. Dernier recours quand ni les clefs normalisées ni les noms
    /// DeepSeek ne sont présents.
    fn config_brut(&self) -> Option<&str> {
        self.cfg("config")?.as_str()
    }

    /// Valeur d'une clef du JSON `<arch>.config`.
    ///
    /// Analyseur minuscule et volontairement limité (nombre, booléen, chaîne) :
    /// le JSON n'est pas là pour être interprété, seulement pour retrouver six
    /// scalaires que le convertisseur a recopiés. Il évite d'inventer des
    /// valeurs par défaut pour un modèle qu'on ne sait pas décrire.
    pub fn json_brut(&self, cle: &str) -> Option<String> {
        let texte = self.config_brut()?;
        let motif = format!("\"{cle}\"");
        let mut depuis = 0usize;
        while let Some(p) = texte[depuis..].find(&motif) {
            let apres = depuis + p + motif.len();
            let reste = texte[apres..].trim_start();
            let Some(reste) = reste.strip_prefix(':') else {
                // `"cle"` apparaît ailleurs (dans une chaîne) : on continue.
                depuis = apres;
                continue;
            };
            let reste = reste.trim_start();
            let fin = |pred: &dyn Fn(char) -> bool| reste.find(|c: char| !pred(c));
            if let Some(r) = reste.strip_prefix('"') {
                let f = r.find('"')?;
                return Some(r[..f].to_string());
            }
            if reste.starts_with("true") { return Some("true".into()); }
            if reste.starts_with("false") { return Some("false".into()); }
            let f = fin(&|c: char| c.is_ascii_digit() || "+-.eE".contains(c)).unwrap_or(reste.len());
            if f == 0 { return None; }
            return Some(reste[..f].to_string());
        }
        None
    }

    pub fn json_nombre(&self, cle: &str) -> Option<f64> {
        self.json_brut(cle).and_then(|v| v.parse().ok())
    }

    pub fn json_texte(&self, cle: &str) -> Option<String> { self.json_brut(cle) }

    pub fn json_bool(&self, cle: &str) -> Option<bool> {
        self.json_brut(cle).map(|v| v == "true")
    }

    pub fn tensor(&self, name: &str) -> Option<&TensorInfo> {
        self.tensors.iter().find(|t| t.name == name)
    }

    /// Conversion f32 → f16 (arrondi au plus proche pair). Sert aux tests qui
    /// fabriquent des blocs quantifiés ; le moteur, lui, ne fait que l'inverse.
    pub fn f32_to_f16(f: f32) -> u16 {
        let bits = f.to_bits();
        let signe = ((bits >> 16) & 0x8000) as u16;
        let exp = ((bits >> 23) & 0xFF) as i32 - 127 + 15;
        let man = bits & 0x7F_FFFF;
        if exp <= 0 { return signe; }                       // dénormal vers zéro
        if exp >= 31 { return signe | 0x7C00; }             // infini
        let mut h = signe | ((exp as u16) << 10) | ((man >> 13) as u16);
        if man & 0x1FFF > 0x1000 || (man & 0x1FFF == 0x1000 && (h & 1) == 1) { h += 1; }
        h
    }

    pub fn f16_to_f32(h: u16) -> f32 {
        let sign = ((h >> 15) & 1) as u32;
        let exp = ((h >> 10) & 0x1F) as u32;
        let man = (h & 0x3FF) as u32;
        let bits = if exp == 0 {
            if man == 0 { sign << 31 } else {
                // dénormal
                let mut e = 127 - 15 + 1;
                let mut m = man;
                while m & 0x400 == 0 { m <<= 1; e -= 1; }
                (sign << 31) | ((e as u32) << 23) | ((m & 0x3FF) << 13)
            }
        } else if exp == 31 {
            (sign << 31) | (0xFF << 23) | (man << 13)
        } else {
            (sign << 31) | ((exp + 127 - 15) << 23) | (man << 13)
        };
        f32::from_bits(bits)
    }

    /// Niveaux entiers bruts (avant mise à l'échelle) pour Q4_0 / Q8_0.
    /// Les niveaux quantifiés d'un tenseur — `None` si le format n'est pas
    /// couvert par le BANC.
    ///
    /// Le banc des encodages (« drave <modele> », la première ligne de l'aide)
    /// ne connaît que Q8_0 et Q4_0 : sur tout modèle en super-blocs (Q4_K,
    /// Q6_K, MXFP4, IQ*), il PANIQUAIT — « raw_levels : type 12 non géré ».
    /// Or ces formats sont la majorité de ce qui tourne ici (gpt-oss, codestral,
    /// 14B, 30B-A3B). La commande documentée plantait donc sur la plupart des
    /// modèles. On refuse proprement, en le disant, au lieu de paniquer.
    pub fn raw_levels(&self, name: &str) -> Option<Vec<i8>> {
        let t = self.tensor(name).unwrap_or_else(|| panic!("tenseur {name} absent"));
        let buf = self.tbuf(t);
        let n = t.nelem();
        let mut out = Vec::with_capacity(n);
        match t.ttype {
            GGML_Q8_0 => {
                let nb = n / 32;
                for b in 0..nb {
                    let p = b * 34;
                    for j in 0..32 { out.push(buf[p + 2 + j] as i8); }
                }
            }
            GGML_Q4_0 => {
                let nb = n / 32;
                for b in 0..nb {
                    let p = b * 18;
                    for j in 0..16 {
                        let q = buf[p + 2 + j];
                        out.push(((q & 0x0F) as i16 - 8) as i8);
                    }
                    for j in 0..16 {
                        let q = buf[p + 2 + j];
                        out.push(((q >> 4) as i16 - 8) as i8);
                    }
                }
            }
            other => {
                eprintln!("[banc] {name} : quantification de type {other} — le banc des \
encodages ne couvre que Q8_0 (8) et Q4_0 (2) ; ce tenseur est ignoré, les autres \
quantifications ayant leurs propres noyaux. Rien n'est faux, mais tout n'est pas montré.");
                return None;
            }
        }
        Some(out)
    }

    /// Déquantifie un bloc **MXFP4** (17 octets, 32 poids) : un octet d'exposant
    /// E8M0 puis 16 octets de nibbles E2M1, moitié basse puis moitié haute.
    pub fn dequant_mxfp4(bloc: &[u8]) -> Vec<f32> {
        assert!(bloc.len() >= 17, "bloc MXFP4 trop court : {}", bloc.len());
        const KV: [f32; 16] = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0,
                               0.0, -0.5, -1.0, -1.5, -2.0, -3.0, -4.0, -6.0];
        let d = Self::echelle_e8m0(bloc[0]);
        let mut out = vec![0f32; 32];
        for j in 0..16 {
            out[j] = KV[(bloc[1 + j] & 0x0F) as usize] * d;
            out[j + 16] = KV[(bloc[1 + j] >> 4) as usize] * d;
        }
        out
    }

    /// Échelle **E8M0** d'un bloc MXFP4, telle que `ggml_e8m0_to_fp32`.
    ///
    /// `e = 0` est dénormalisé et vaut 2^−127 ; tout autre `e` vaut 2^(e−127)
    /// (`e << 23`). Le piège mesuré : ggml multiplie la grille E2M1 **doublée**
    /// (entiers 0..12) par `2^(e−128)`, et notre table est la vraie grille — la
    /// moitié de ces entiers. Mélanger les deux conventions donne des poids
    /// **deux fois trop petits**, sans rien casser d'autre : la perplexité monte
    /// un peu, et rien ne le dit. Comparé à libggml, l'écart était exactement
    /// d'un facteur 2 sur les 256 poids du bloc.
    #[inline]
    pub fn echelle_e8m0(e: u8) -> f32 {
        if e == 0 { f32::from_bits(0x0040_0000) } else { f32::from_bits((e as u32) << 23) }
    }

    /// Déquantifie un bloc **Q5_0** (22 octets, 32 poids).
    ///
    /// Le cinquième bit n'est pas rangé par sous-bloc comme en Q5_K : les 32
    /// bits vivent dans un mot de 32 bits, le bit `j` servant le poids `j` et le
    /// bit `j+16` le poids `j+16`. Les 16 premiers poids occupent donc les
    /// nibbles BAS et les 16 suivants les nibbles HAUTS — pas deux moitiés
    /// contiguës comme en Q4_0.
    pub fn dequant_q5_0(bloc: &[u8]) -> Vec<f32> {
        assert!(bloc.len() >= 22, "bloc Q5_0 trop court : {}", bloc.len());
        Self::dequant_q5(bloc, false)
    }

    /// Déquantifie un bloc **Q5_1** (24 octets, 32 poids) : identique à Q5_0
    /// avec un minimum, et sans recentrage sur 16.
    pub fn dequant_q5_1(bloc: &[u8]) -> Vec<f32> {
        assert!(bloc.len() >= 24, "bloc Q5_1 trop court : {}", bloc.len());
        Self::dequant_q5(bloc, true)
    }

    fn dequant_q5(bloc: &[u8], avec_min: bool) -> Vec<f32> {
        let d = Self::f16_to_f32(u16::from_le_bytes([bloc[0], bloc[1]]));
        let (m, base_qh, base_qs) = if avec_min {
            (Self::f16_to_f32(u16::from_le_bytes([bloc[2], bloc[3]])), 4usize, 8usize)
        } else {
            (0.0, 2usize, 6usize)
        };
        let qh = u32::from_le_bytes([bloc[base_qh], bloc[base_qh + 1],
                                     bloc[base_qh + 2], bloc[base_qh + 3]]);
        let qs = &bloc[base_qs..base_qs + 16];
        let mut out = vec![0f32; 32];
        for j in 0..16usize {
            let xh0 = (((qh >> j) << 4) & 0x10) as u8;
            let xh1 = ((qh >> (j + 12)) & 0x10) as u8;
            let q0 = (qs[j] & 0x0F) | xh0;
            let q1 = (qs[j] >> 4) | xh1;
            out[j] = if avec_min { d * q0 as f32 + m }
                     else { d * (q0 as i32 - 16) as f32 };
            out[j + 16] = if avec_min { d * q1 as f32 + m }
                          else { d * (q1 as i32 - 16) as f32 };
        }
        out
    }

    /// Déquantifie un bloc **Q5_K** (176 octets, 256 poids).
    ///
    /// Même structure que Q4_K — d, dmin, 12 octets d'échelles, 128 octets de
    /// quants 4 bits — plus **32 octets de bits hauts** : chaque poids a 5 bits.
    /// Les bits hauts sont lus avec des masques qui se décalent de deux bits à
    /// chaque tranche de 64 poids.
    /// Version qui alloue, pour les appelants qui veulent un `Vec`.
    pub fn dequant_q5k(bloc: &[u8]) -> Vec<f32> {
        let mut v = vec![0f32; 256];
        Self::dequant_q5k_dans(bloc, &mut v);
        v
    }

    pub fn dequant_q5k_dans(bloc: &[u8], out: &mut [f32]) {
        assert!(bloc.len() >= 176, "bloc Q5_K trop court : {}", bloc.len());
        let d = Self::f16_to_f32(u16::from_le_bytes([bloc[0], bloc[1]]));
        let dmin = Self::f16_to_f32(u16::from_le_bytes([bloc[2], bloc[3]]));
        let sc = &bloc[4..16];
        let qh = &bloc[16..48];
        let ql = &bloc[48..176];
        assert!(out.len() >= 256, "tampon de sortie trop court");
        let (mut u1, mut u2) = (1u8, 2u8);
        for tranche in 0..4usize {
            // Les 32 octets de bits hauts sont **relus** à chaque tranche : le
            // masque (`u1` puis `u2`, décalé de deux bits par tranche) désigne
            // les deux bits de poids fort de la tranche. Seul `ql` avance.
            for k in 0..2usize {
                let (haut, u) = if k == 0 { (false, u1) } else { (true, u2) };
                let (s_, m_) = echelle_min_q4k(sc, 2 * tranche + k);
                let dl = d * s_ as f32;
                let ml = dmin * m_ as f32;
                for l in 0..32usize {
                    let q4 = if haut { ql[tranche * 32 + l] >> 4 } else { ql[tranche * 32 + l] & 0x0F };
                    let bit = if qh[l] & u != 0 { 16 } else { 0 };
                    out[tranche * 64 + k * 32 + l] = dl * (q4 + bit) as f32 - ml;
                }
            }
            u1 <<= 2;
            u2 <<= 2;
        }
        
    }
    /// Déquantifie un bloc **Q3_K** (110 octets, 256 poids) : 32 octets de bits
    /// hauts, 64 octets de quants 2 bits, 12 octets portant **16 échelles de
    /// 6 bits**, puis l'échelle de super-bloc en f16.
    ///
    /// Trois pièges, tous dans la disposition et aucun dans l'arithmétique :
    /// les 12 octets d'échelles ne sont pas 12 échelles (il y en a 16, dont les
    /// deux bits de poids fort vivent dans les trois derniers octets) ; un octet
    /// de quants sert **quatre** poids (un par champ de 2 bits, à 32 poids
    /// d'écart) ; et le bit haut **retire 4** quand il est ABSENT, la valeur
    /// signée allant de −4 à 3. C'est le type de 33,5 % des poids de
    /// Qwen3-235B-A22B.
    /// Version qui alloue, pour les appelants qui veulent un `Vec`.
    pub fn dequant_q3k(bloc: &[u8]) -> Vec<f32> {
        let mut v = vec![0f32; 256];
        Self::dequant_q3k_dans(bloc, &mut v);
        v
    }

    pub fn dequant_q3k_dans(bloc: &[u8], out: &mut [f32]) {
        assert!(bloc.len() >= 110, "bloc Q3_K trop court : {}", bloc.len());
        let hm = &bloc[0..32];
        let qs = &bloc[32..96];
        let sc = &bloc[96..108];
        let d_all = Self::f16_to_f32(u16::from_le_bytes([bloc[108], bloc[109]]));
        // Dépaquetage des échelles, mot pour mot comme ggml : chaque octet des
        // trois premiers mots porte une échelle de 4 bits, le troisième mot
        // porte les deux bits hauts des seize.
        const KMASK1: u32 = 0x0303_0303;
        const KMASK2: u32 = 0x0f0f_0f0f;
        let mut aux = [0u32; 4];
        for i in 0..3 {
            aux[i] = u32::from_le_bytes([sc[4*i], sc[4*i+1], sc[4*i+2], sc[4*i+3]]);
        }
        let tmp = aux[2];
        aux[2] = ((aux[0] >> 4) & KMASK2) | (((tmp >> 4) & KMASK1) << 4);
        aux[3] = ((aux[1] >> 4) & KMASK2) | (((tmp >> 6) & KMASK1) << 4);
        aux[0] = (aux[0] & KMASK2) | ((tmp & KMASK1) << 4);
        aux[1] = (aux[1] & KMASK2) | (((tmp >> 2) & KMASK1) << 4);
        let mut scales = [0i8; 16];
        for (i, valeur) in scales.iter_mut().enumerate() {
            *valeur = aux[i / 4].to_le_bytes()[i % 4] as i8;
        }
        assert!(out.len() >= 256, "tampon de sortie trop court");
        let mut is = 0usize;
        for n in 0..2usize {
            for j in 0..4usize {
                let shift = 2 * j;
                let m = 1u8 << (4 * n + j);
                for g in 0..2usize {
                    let dl = d_all * (scales[is] as i32 - 32) as f32;
                    is += 1;
                    for l in 0..16usize {
                        let octet = qs[n * 32 + g * 16 + l];
                        let q2 = ((octet >> shift) & 3) as i32;
                        let haut = hm[g * 16 + l] & m != 0;
                        out[n * 128 + j * 32 + g * 16 + l] =
                            dl * (q2 - if haut { 0 } else { 4 }) as f32;
                    }
                }
            }
        }
        
    }
    /// Déquantifie un bloc **Q2_K** (84 octets, 256 poids).
    ///
    /// Structure : 16 octets d'échelles (4 bits d'échelle, 4 bits de minimum par
    /// sous-bloc de 16 poids), 64 octets de quants 2 bits, puis d et dmin en f16.
    /// `x = d·sc·q − dmin·m`. C'est le type des `ffn_down_exps` de
    /// DeepSeek-V4.1 — sans lui, 59 Go du modèle restent illisibles.
    /// Version qui alloue, pour les appelants qui veulent un `Vec`.
    pub fn dequant_q2k(bloc: &[u8]) -> Vec<f32> {
        let mut v = vec![0f32; 256];
        Self::dequant_q2k_dans(bloc, &mut v);
        v
    }

    /// Déquantification Q2_K **vectorisée**, identique AU BIT PRÈS à la version
    /// scalaire : chaque valeur reçoit les mêmes opérations dans le même ordre
    /// (`(d·sc)·quant`, puis soustraction de `dmin·m`), aucune n'est réassociée
    /// — l'AVX2 ne fait que les traiter huit par huit. **Pas de FMA** :
    /// `fma(a, b, −c)` n'a pas le même arrondi que `a·b − c`, et le noyau
    /// changerait des bits pour un gain de vitesse qui n'en vaut pas la peine.
    ///
    /// La conversion codebook → f32 est une fonction pure, valeur par valeur :
    /// c'est le seul endroit du chemin des experts où le SIMD est gratuit en
    /// exactitude (le produit scalaire, lui, réassocierait la somme).
    #[cfg(target_arch = "x86_64")]
    #[target_feature(enable = "avx2")]
    pub unsafe fn dequant_q2k_avx2(bloc: &[u8], out: &mut [f32]) {
        use std::arch::x86_64::*;
        assert!(bloc.len() >= 84, "bloc Q2_K trop court : {}", bloc.len());
        assert!(out.len() >= 256, "tampon de sortie trop court");
        let scales = &bloc[0..16];
        let qs = &bloc[16..80];
        let d = Self::f16_to_f32(u16::from_le_bytes([bloc[80], bloc[81]]));
        let dmin = Self::f16_to_f32(u16::from_le_bytes([bloc[82], bloc[83]]));
        let masque = _mm256_set1_epi32(3);
        for moitie in 0..2usize {
            let q = &qs[moitie * 32..moitie * 32 + 32];
            for k in 0..4usize {
                let decal = _mm256_set1_epi32((2 * k) as i32);
                for demi in 0..2usize {
                    let is = moitie * 8 + k * 2 + demi;
                    let sc = (scales[is] & 0x0F) as f32;
                    let m = (scales[is] >> 4) as f32;
                    let dsc = _mm256_set1_ps(d * sc);
                    let dm = _mm256_set1_ps(dmin * m);
                    let base = moitie * 128 + k * 32 + demi * 16;
                    let src = q.as_ptr().add(demi * 16);
                    let dst = out.as_mut_ptr().add(base);
                    for paquet in 0..2usize {
                        // huit octets → huit entiers 32 bits → huit f32
                        let huit = _mm_loadl_epi64(src.add(paquet * 8) as *const __m128i);
                        let q32 = _mm256_cvtepu8_epi32(huit);
                        let qm = _mm256_and_si256(_mm256_srlv_epi32(q32, decal), masque);
                        let qf = _mm256_cvtepi32_ps(qm);
                        let r = _mm256_sub_ps(_mm256_mul_ps(dsc, qf), dm);
                        _mm256_storeu_ps(dst.add(paquet * 8), r);
                    }
                }
            }
        }
    }

    pub fn dequant_q2k_dans(bloc: &[u8], out: &mut [f32]) {
        assert!(bloc.len() >= 84, "bloc Q2_K trop court : {}", bloc.len());
        let scales = &bloc[0..16];
        let qs = &bloc[16..80];
        let d = Self::f16_to_f32(u16::from_le_bytes([bloc[80], bloc[81]]));
        let dmin = Self::f16_to_f32(u16::from_le_bytes([bloc[82], bloc[83]]));
        assert!(out.len() >= 256, "tampon de sortie trop court");
        // Quatre passes de 64 poids : chaque octet porte quatre quants 2 bits,
        // lus aux décalages 0, 2, 4 et 6.
        // Le parcours est celui du code ggml : moitié, puis décalage (k), puis
        // les deux sous-groupes de 16 valeurs — et l'échelle ne change qu'à ce
        // dernier niveau. La calculer une fois par groupe de 16 au lieu d'une
        // fois par valeur est **identique au bit près** : les mêmes opérations
        // (`(d·sc)·quant`, `dmin·m`, soustraction) dans le même ordre, juste
        // moins répétées. Mesuré (bloc 18) : la déquantification pesait 25 % de
        // la passe et 45 % du poste d'experts.
        for moitie in 0..2usize {
            let q = &qs[moitie * 32..moitie * 32 + 32];
            for k in 0..4usize {
                let decal = 2 * k;
                for demi in 0..2usize {
                    // L'ordre des échelles suit le parcours du code ggml :
                    // moitié, puis décalage, puis les deux sous-groupes de 16.
                    let is = moitie * 8 + k * 2 + demi;
                    let sc = (scales[is] & 0x0F) as f32;
                    let m = (scales[is] >> 4) as f32;
                    let dsc = d * sc;
                    let dm = dmin * m;
                    let base = moitie * 128 + k * 32 + demi * 16;
                    for l in 0..16usize {
                        let quant = ((q[demi * 16 + l] >> decal) & 3) as f32;
                        out[base + l] = dsc * quant - dm;
                    }
                }
            }
        }
        
    }
    /// Déquantifie une ligne d'un tenseur 2D, en f32.
    /// Déquantifie un tenseur **s'il existe**, sinon `None`.
    ///
    /// Sert aux tenseurs d'une architecture dont une partie seulement est
    /// présente : les modèles MLA à experts n'ont pas de FFN dense, et exiger
    /// `ffn_gate.weight` pour construire la couche refusait le modèle entier.
    pub fn dequant_optionnel(&self, name: &str) -> Option<Vec<f32>> {
        if self.tensor(name).is_some() { Some(self.dequant(name)) } else { None }
    }

    /// Lit un tenseur **I32** (entiers 32 bits signés), tel quel.
    ///
    /// Un seul usage dans les modèles de cette machine : la table
    /// `ffn_gate_tid2eid` de DeepSeek-V4, qui donne les experts d'un jeton par
    /// son identifiant. La passer par des f32 serait une perte de temps et une
    /// occasion d'arrondi ; la convertir en f32 puis la relire en entier serait
    /// pire.
    pub fn dequant_i32(&self, name: &str) -> Vec<i32> {
        let t = self.tensor(name).unwrap_or_else(|| panic!("tenseur {name} absent"));
        assert_eq!(t.ttype, GGML_I32, "tenseur {name} : type {} au lieu d'I32",
                   Self::nom_type(t.ttype));
        let buf = self.tbuf(t);
        let n = t.nelem();
        (0..n).map(|i| i32::from_le_bytes([buf[4*i], buf[4*i+1], buf[4*i+2], buf[4*i+3]])).collect()
    }

    pub fn row_f32(&self, name: &str, row: usize, n_cols: usize) -> Vec<f32> {
        let t = self.tensor(name).unwrap_or_else(|| panic!("tenseur {name} absent"));
        let buf = self.tbuf(t);
        let mut out = Vec::with_capacity(n_cols);
        match t.ttype {
            GGML_BF16 => {
                for i in 0..n_cols {
                    out.push(bf16_to_f32(u16::from_le_bytes(
                        buf[2 * i..2 * i + 2].try_into().unwrap())));
                }
            }
            GGML_F32 => {
                let p = row * n_cols * 4;
                for i in 0..n_cols {
                    out.push(f32::from_le_bytes(buf[p + 4*i..p + 4*i + 4].try_into().unwrap()));
                }
            }
            GGML_F16 => {
                let p = row * n_cols * 2;
                for i in 0..n_cols {
                    out.push(Self::f16_to_f32(u16::from_le_bytes(buf[p + 2*i..p + 2*i + 2].try_into().unwrap())));
                }
            }
            GGML_Q8_0 => {
                let nb = n_cols / 32;
                for b in 0..nb {
                    let p = (row * nb + b) * 34;
                    let d = Self::f16_to_f32(u16::from_le_bytes(buf[p..p+2].try_into().unwrap()));
                    for j in 0..32 { out.push(d * (buf[p + 2 + j] as i8) as f32); }
                }
            }
            GGML_Q4_0 => {
                let nb = n_cols / 32;
                for b in 0..nb {
                    let p = (row * nb + b) * 18;
                    let d = Self::f16_to_f32(u16::from_le_bytes(buf[p..p+2].try_into().unwrap()));
                    for j in 0..16 { out.push(d * ((buf[p + 2 + j] & 0x0F) as i16 - 8) as f32); }
                    for j in 0..16 { out.push(d * ((buf[p + 2 + j] >> 4) as i16 - 8) as f32); }
                }
            }
            // Super-blocs de 256 poids : le déquantificateur rend les 256
            // valeurs d'un coup, donc la boucle avance par super-bloc.
            GGML_Q2_K | GGML_Q3_K | GGML_Q5_K | GGML_IQ2_XXS | GGML_IQ3_XXS
            | GGML_IQ1_S | GGML_IQ4_XS | GGML_IQ1_M => {
                let (taille, f): (usize, fn(&[u8]) -> Vec<f32>) = match t.ttype {
                    GGML_Q2_K => (84, Self::dequant_q2k),
                    GGML_Q3_K => (110, Self::dequant_q3k),
                    GGML_Q5_K => (TAILLE_Q5K, Self::dequant_q5k),
                    GGML_IQ2_XXS => (66, crate::formats::dequant_iq2xxs),
                    GGML_IQ3_XXS => (98, crate::formats::dequant_iq3xxs),
                    GGML_IQ1_S => (50, crate::formats::dequant_iq1s),
                    GGML_IQ4_XS => (136, crate::formats::dequant_iq4xs),
                    _ => (56, crate::formats::dequant_iq1m),
                };
                let ns = n_cols / 256;
                for sup in 0..ns {
                    out.extend_from_slice(&f(&buf[(row * ns + sup) * taille..]));
                }
            }
            GGML_Q4_K => {
                let ns = n_cols / 256;
                for sup in 0..ns {
                    let p = (row * ns + sup) * TAILLE_Q4K;
                    let d = Self::f16_to_f32(u16::from_le_bytes(buf[p..p+2].try_into().unwrap()));
                    let dmin = Self::f16_to_f32(u16::from_le_bytes(buf[p+2..p+4].try_into().unwrap()));
                    let sc = &buf[p + 4..p + 16];
                    let qs = &buf[p + 16..p + 144];
                    for g in 0..4 {
                        let (s0, m0) = echelle_min_q4k(sc, 2 * g);
                        let (s1, m1) = echelle_min_q4k(sc, 2 * g + 1);
                        let (d0, n0) = (d * s0 as f32, dmin * m0 as f32);
                        let (d1, n1) = (d * s1 as f32, dmin * m1 as f32);
                        for l in 0..32 { out.push(d0 * (qs[g*32 + l] & 0x0F) as f32 - n0); }
                        for l in 0..32 { out.push(d1 * (qs[g*32 + l] >> 4) as f32 - n1); }
                    }
                }
            }
            GGML_Q6_K => {
                let ns = n_cols / 256;
                for sup in 0..ns {
                    let p = (row * ns + sup) * TAILLE_Q6K;
                    let ql = &buf[p..p + 128];
                    let qh = &buf[p + 128..p + 192];
                    let sc = &buf[p + 192..p + 208];
                    let d = Self::f16_to_f32(u16::from_le_bytes(buf[p+208..p+210].try_into().unwrap()));
                    for moitie in 0..2 {
                        let (ql, qh, sc) = (&ql[moitie*64..], &qh[moitie*32..], &sc[moitie*8..]);
                        let mut tmp = [0f32; 128];
                        for l in 0..32 {
                            let is = l / 16;
                            let q1 = ((ql[l] & 0x0F) | ((qh[l] & 3) << 4)) as i16 - 32;
                            let q2 = ((ql[l + 32] & 0x0F) | (((qh[l] >> 2) & 3) << 4)) as i16 - 32;
                            let q3 = ((ql[l] >> 4) | (((qh[l] >> 4) & 3) << 4)) as i16 - 32;
                            let q4 = ((ql[l + 32] >> 4) | (((qh[l] >> 6) & 3) << 4)) as i16 - 32;
                            let s = |k: usize| d * (sc[is + k] as i8) as f32;
                            tmp[l] = s(0) * q1 as f32;
                            tmp[l + 32] = s(2) * q2 as f32;
                            tmp[l + 64] = s(4) * q3 as f32;
                            tmp[l + 96] = s(6) * q4 as f32;
                        }
                        out.extend_from_slice(&tmp);
                    }
                }
            }
            GGML_Q5_0 | GGML_Q5_1 => {
                let (taille, f): (usize, fn(&[u8]) -> Vec<f32>) = if t.ttype == GGML_Q5_0 {
                    (22, Self::dequant_q5_0)
                } else {
                    (24, Self::dequant_q5_1)
                };
                let nb = n_cols / 32;
                for b in 0..nb {
                    out.extend_from_slice(&f(&buf[(row * nb + b) * taille..]));
                }
            }
            GGML_MXFP4 => {
                // 17 octets par bloc de 32 : exposant E8M0 puis nibbles E2M1.
                let nb = n_cols / 32;
                for b in 0..nb {
                    out.extend_from_slice(&Self::dequant_mxfp4(&buf[(row * nb + b) * 17..]));
                }
            }
            GGML_Q4_1 => {
                let nb = n_cols / 32;
                for b in 0..nb {
                    let p = (row * nb + b) * 20;
                    let d = Self::f16_to_f32(u16::from_le_bytes(buf[p..p+2].try_into().unwrap()));
                    let m = Self::f16_to_f32(u16::from_le_bytes(buf[p+2..p+4].try_into().unwrap()));
                    for j in 0..16 { out.push(d * (buf[p + 4 + j] & 0x0F) as f32 + m); }
                    for j in 0..16 { out.push(d * (buf[p + 4 + j] >> 4) as f32 + m); }
                }
            }
            other => panic!("row_f32 : type {other} non géré"),
        }
        out
    }

    /// Vue pré-résolue sur un tenseur Q8_0 : évite de rechercher le tenseur
    /// (parcours linéaire des 290 descripteurs) à chaque ligne. La tête de
    /// sortie appelle cela 151 936 fois par token.
    pub fn q8_view(&self, name: &str) -> Q8View {
        let t = self.tensor(name).unwrap_or_else(|| panic!("tenseur {name} absent"));
        let q4 = match t.ttype {
            GGML_Q8_0 => false,
            GGML_Q4_0 => true,
            GGML_Q4_K | GGML_Q6_K => true,
            other => panic!("q8_view : type {other} non géré"),
        };
        let n_cols = t.dims[1] as usize;
        let bloc = if t.ttype == GGML_Q4_K || t.ttype == GGML_Q6_K { 256 } else { 32 };
        Q8View { fichier: t.fichier, base: t.offset as usize, n_cols, nb: n_cols / bloc,
                 q4, ttype: t.ttype }
    }

    /// Pointeur sur le premier octet des données d'un tenseur.
    pub fn data_ptr(&self, name: &str) -> Option<*const u8> {
        let t = self.tensor(name)?;
        Some(self.tbuf(t).as_ptr())
    }

    /// Type ggml d'un tenseur.
    pub fn type_de(&self, name: &str) -> Option<u32> {
        self.tensor(name).map(|t| t.ttype)
    }

    /// Blocs **Q8_0** bruts : `(octets, nb de blocs de 32 par ligne)`.
    pub fn q8_blocks(&self, name: &str) -> Option<(&[u8], usize)> {
        let t = self.tensor(name)?;
        if t.ttype != GGML_Q8_0 { return None; }
        Some((self.tbuf(t), t.dims[1] as usize / 32))
    }

    /// Super-blocs **Q4_K** bruts : `(octets, nb de super-blocs de 256 poids par
    /// ligne)`. C'est le format de toute la famille Qwen/Llama en `Q4_K_M`.
    pub fn q4k_blocks(&self, name: &str) -> Option<(&[u8], usize)> {
        let t = self.tensor(name)?;
        if t.ttype != GGML_Q4_K { return None; }
        Some((self.tbuf(t), t.dims[1] as usize / 256))
    }

    /// Super-blocs **Q6_K** bruts (quelques tenseurs des mélanges `Q4_K_M`).
    pub fn q6k_blocks(&self, name: &str) -> Option<(&[u8], usize)> {
        let t = self.tensor(name)?;
        if t.ttype != GGML_Q6_K { return None; }
        Some((self.tbuf(t), t.dims[1] as usize / 256))
    }

    /// Blocs **MXFP4** bruts : `(octets à partir du premier bloc, nb de blocs
    /// par ligne)`. Bloc de 17 octets : un exposant E8M0 puis 16 octets de
    /// nibbles E2M1. C'est le format de gpt-oss-120b.
    pub fn mxfp4_blocks(&self, name: &str) -> Option<(&[u8], usize)> {
        let t = self.tensor(name)?;
        if t.ttype != GGML_MXFP4 { return None; }
        let nb = t.dims[1] as usize / 32;
        Some((self.tbuf(t), nb))
    }

    /// Blocs Q4_0 bruts d'un tenseur : `(octets à partir du premier bloc, nb de
    /// blocs par ligne)`. Permet d'importer les poids **tels quels**, sans les
    /// déquantifier puis les requantifier — le double arrondi coûtait +18 % de
    /// perplexité sur Qwen2.5-0.5B (19,86 → 21,98).
    pub fn q4_blocks(&self, name: &str) -> Option<(&[u8], usize)> {
        let t = self.tensor(name)?;
        if t.ttype != GGML_Q4_0 { return None; }
        let nb = t.dims[1] as usize / 32;
        Some((self.tbuf(t), nb))
    }

    /// Produit scalaire d'une ligne via une vue pré-résolue (Q8_0 ou Q4_0).
    #[inline]
    pub fn q8_dot_at(&self, v: &Q8View, row: usize, qx: &[i16]) -> f32 {
        let mut acc = 0f32;
        let buf = &self.bufs[v.fichier][self.starts[v.fichier]..];
        if v.ttype == GGML_Q6_K {
            // Q6_K : quants signés sur 6 bits, une échelle signée par 16 poids,
            // aucune asymétrie — donc pas de terme de minimum.
            let ns = v.nb;
            for sup in 0..ns {
                let p = v.base + (row * ns + sup) * TAILLE_Q6K;
                let ql = &buf[p..p + 128];
                let qh = &buf[p + 128..p + 192];
                let sc = &buf[p + 192..p + 208];
                let d = Self::f16_to_f32(
                    u16::from_le_bytes(buf[p+208..p+210].try_into().unwrap()));
                for moitie in 0..2usize {
                    let (ql, qh, sc) = (&ql[moitie*64..], &qh[moitie*32..], &sc[moitie*8..]);
                    let b = sup * 256 + moitie * 128;
                    // Les huit groupes de 16 poids d'une moitié ont chacun leur
                    // échelle et occupent des positions CONTIGUËS : on accumule
                    // donc en entier par groupe, et on ne paie qu'une
                    // multiplication flottante par 16 poids au lieu de quatre
                    // opérations flottantes par poids (mesuré : 137 ms par jeton
                    // pour la seule tête d'un 7B, soit 42 % du temps).
                    let mut part = [0i32; 8];
                    for l in 0..32usize {
                        let is = l / 16;
                        let q1 = ((ql[l] & 0x0F) | ((qh[l] & 3) << 4)) as i32 - 32;
                        let q2 = ((ql[l+32] & 0x0F) | (((qh[l] >> 2) & 3) << 4)) as i32 - 32;
                        let q3 = ((ql[l] >> 4) | (((qh[l] >> 4) & 3) << 4)) as i32 - 32;
                        let q4 = ((ql[l+32] >> 4) | (((qh[l] >> 6) & 3) << 4)) as i32 - 32;
                        part[is] += q1 * qx[b + l] as i32;
                        part[2 + is] += q2 * qx[b + l + 32] as i32;
                        part[4 + is] += q3 * qx[b + l + 64] as i32;
                        part[6 + is] += q4 * qx[b + l + 96] as i32;
                    }
                    for (g, &p) in part.iter().enumerate() {
                        acc += d * (sc[g] as i8) as f32 * p as f32;
                    }
                }
            }
            return acc;
        }
        if v.ttype == GGML_Q4_K {
            // Tête Q4_K : même arithmétique que le noyau des projections,
            // mais scalaire — la tête est bornée par la mémoire, pas par le
            // calcul (130 Mo lus par jeton sur un 1,5B).
            let ns = v.nb;
            for sup in 0..ns {
                let p = v.base + (row * ns + sup) * TAILLE_Q4K;
                let d = Self::f16_to_f32(u16::from_le_bytes(buf[p..p+2].try_into().unwrap()));
                let dmin = Self::f16_to_f32(u16::from_le_bytes(buf[p+2..p+4].try_into().unwrap()));
                let sc = &buf[p + 4..p + 16];
                let qs = &buf[p + 16..p + 144];
                for g in 0..4usize {
                    let (s0, m0) = echelle_min_q4k(sc, 2 * g);
                    let (s1, m1) = echelle_min_q4k(sc, 2 * g + 1);
                    let mut sq0 = 0i32; let mut sx0 = 0i32;
                    let mut sq1 = 0i32; let mut sx1 = 0i32;
                    for l in 0..32 {
                        let octet = qs[g * 32 + l] as i32;
                        let x0 = qx[sup * 256 + g * 64 + l] as i32;
                        let x1 = qx[sup * 256 + g * 64 + 32 + l] as i32;
                        sq0 += (octet & 15) * x0; sx0 += x0;
                        sq1 += (octet >> 4) * x1; sx1 += x1;
                    }
                    acc += d * s0 as f32 * sq0 as f32 - dmin * m0 as f32 * sx0 as f32;
                    acc += d * s1 as f32 * sq1 as f32 - dmin * m1 as f32 * sx1 as f32;
                }
            }
            return acc;
        }
        if v.q4 {
            // bloc Q4_0 : 2 octets d'échelle + 16 octets = 32 niveaux (4 bits)
            // les 16 premiers sont les nibbles BAS, les 16 suivants les HAUTS
            for b in 0..v.nb {
                let p = v.base + (row * v.nb + b) * 18;
                let d = Self::f16_to_f32(u16::from_le_bytes(buf[p..p+2].try_into().unwrap()));
                let w = &buf[p + 2..p + 18];
                let x = &qx[b * 32..b * 32 + 32];
                let mut s = 0i32;
                for j in 0..16 {
                    s += (((w[j] & 0x0F) as i32) - 8) * (x[j] as i32);
                    s += (((w[j] >> 4) as i32) - 8) * (x[j + 16] as i32);
                }
                acc += d * s as f32;
            }
        } else {
            #[cfg(target_arch = "x86_64")]
            if std::is_x86_feature_detected!("avx2") {
                return unsafe { self.q8_dot_avx2(v, row, qx) };
            }
            for b in 0..v.nb {
                let p = v.base + (row * v.nb + b) * 34;
                let d = Self::f16_to_f32(u16::from_le_bytes(buf[p..p+2].try_into().unwrap()));
                let w = &buf[p + 2..p + 34];
                let x = &qx[b * 32..b * 32 + 32];
                let mut s = 0i32;
                for j in 0..32 {
                    s += (w[j] as i8 as i32) * (x[j] as i32);
                }
                acc += d * s as f32;
            }
        }
        acc
    }

    /// Même produit scalaire, 32 niveaux par instruction. La somme du bloc est
    /// ENTIÈRE et exacte (`vpmaddwd` sur des i16), donc le résultat est identique
    /// au chemin scalaire **au bit près** : seul l'ordre des additions change, et
    /// sur des entiers cela ne change rien. C'est ce qui permet de remplacer le
    /// noyau sans toucher à la perplexité.
    #[cfg(target_arch = "x86_64")]
    #[target_feature(enable = "avx2")]
    unsafe fn q8_dot_avx2(&self, v: &Q8View, row: usize, qx: &[i16]) -> f32 {
        use std::arch::x86_64::*;
        let mut acc = 0f32;
        let buf = &self.bufs[v.fichier][self.starts[v.fichier]..];
        for b in 0..v.nb {
            let p = v.base + (row * v.nb + b) * 34;
            let d = Self::f16_to_f32(u16::from_le_bytes(buf[p..p+2].try_into().unwrap()));
            let w = buf[p + 2..p + 34].as_ptr();
            let x = qx.as_ptr().add(b * 32);
            let q = _mm256_loadu_si256(w as *const __m256i);              // 32 × i8
            let bas = _mm256_cvtepi8_epi16(_mm256_castsi256_si128(q));    // 16 × i16
            let haut = _mm256_cvtepi8_epi16(_mm256_extracti128_si256(q, 1));
            let x0 = _mm256_loadu_si256(x as *const __m256i);
            let x1 = _mm256_loadu_si256(x.add(16) as *const __m256i);
            let s = _mm256_add_epi32(_mm256_madd_epi16(bas, x0),
                                     _mm256_madd_epi16(haut, x1));
            let s128 = _mm_add_epi32(_mm256_castsi256_si128(s),
                                     _mm256_extracti128_si256(s, 1));
            let s64 = _mm_add_epi32(s128, _mm_shuffle_epi32(s128, 0b0000_1110));
            let s32 = _mm_add_epi32(s64, _mm_shuffle_epi32(s64, 0b0000_0001));
            acc += d * _mm_cvtsi128_si32(s32) as f32;
        }
        acc
    }

    /// Déquantification en f32 (F32 / F16 / Q8_0 / Q4_0).
    pub fn dequant(&self, name: &str) -> Vec<f32> {
        let t = self.tensor(name).unwrap_or_else(|| panic!("tenseur {name} absent"));
        let buf = self.tbuf(t);
        let n = t.nelem();
        let mut out = Vec::with_capacity(n);
        match t.ttype {
            GGML_BF16 => {
                for i in 0..n {
                    out.push(bf16_to_f32(u16::from_le_bytes(
                        buf[2 * i..2 * i + 2].try_into().unwrap())));
                }
            }
            GGML_F32 => {
                for i in 0..n {
                    out.push(f32::from_le_bytes(buf[4*i..4*i + 4].try_into().unwrap()));
                }
            }
            GGML_F16 => {
                for i in 0..n {
                    out.push(Self::f16_to_f32(u16::from_le_bytes(buf[2*i..2*i + 2].try_into().unwrap())));
                }
            }
            GGML_Q8_0 => {
                let nb = n / 32;
                for b in 0..nb {
                    let p = b * 34;
                    let d = Self::f16_to_f32(u16::from_le_bytes(buf[p..p+2].try_into().unwrap()));
                    for j in 0..32 { out.push(d * (buf[p + 2 + j] as i8) as f32); }
                }
            }
            GGML_Q4_0 => {
                let nb = n / 32;
                for b in 0..nb {
                    let p = b * 18;
                    let d = Self::f16_to_f32(u16::from_le_bytes(buf[p..p+2].try_into().unwrap()));
                    for j in 0..16 { out.push(d * ((buf[p + 2 + j] & 0x0F) as i16 - 8) as f32); }
                    for j in 0..16 { out.push(d * ((buf[p + 2 + j] >> 4) as i16 - 8) as f32); }
                }
            }
            GGML_Q4_1 => {
                // bloc de 20 octets : échelle f16, décalage f16, 16 octets de nibbles
                // valeur = d · q + m, q ∈ 0..15 (pas de niveau zéro central)
                let nb = n / 32;
                for b in 0..nb {
                    let p = b * 20;
                    let d = Self::f16_to_f32(u16::from_le_bytes(buf[p..p+2].try_into().unwrap()));
                    let m = Self::f16_to_f32(u16::from_le_bytes(buf[p+2..p+4].try_into().unwrap()));
                    for j in 0..16 { out.push(d * (buf[p + 4 + j] & 0x0F) as f32 + m); }
                    for j in 0..16 { out.push(d * (buf[p + 4 + j] >> 4) as f32 + m); }
                }
            }
            GGML_Q5_0 | GGML_Q5_1 => {
                let (taille, f): (usize, fn(&[u8]) -> Vec<f32>) = if t.ttype == GGML_Q5_0 {
                    (22, Self::dequant_q5_0)
                } else {
                    (24, Self::dequant_q5_1)
                };
                let nb = n / 32;
                for b in 0..nb { out.extend_from_slice(&f(&buf[b * taille..])); }
            }
            GGML_MXFP4 => {
                // 17 octets par bloc de 32 : exposant E8M0 puis nibbles E2M1.
                let nb = n / 32;
                for b in 0..nb {
                    out.extend_from_slice(&Self::dequant_mxfp4(&buf[b * 17..]));
                }
            }
            GGML_Q4_K => {
                const KV: [f32; 16] = [0.0; 16];
                let _ = KV;
                let nb = n / 256;
                for b in 0..nb {
                    let p = b * TAILLE_Q4K;
                    let d = Self::f16_to_f32(u16::from_le_bytes(buf[p..p+2].try_into().unwrap()));
                    let dmin = Self::f16_to_f32(u16::from_le_bytes(buf[p+2..p+4].try_into().unwrap()));
                    let sc = &buf[p + 4..p + 16];
                    let qs = &buf[p + 16..p + 144];
                    for g in 0..4 {
                        let (s0, m0) = echelle_min_q4k(sc, 2 * g);
                        let (s1, m1) = echelle_min_q4k(sc, 2 * g + 1);
                        let (d0, n0) = (d * s0 as f32, dmin * m0 as f32);
                        let (d1, n1) = (d * s1 as f32, dmin * m1 as f32);
                        for l in 0..32 { out.push(d0 * (qs[g * 32 + l] & 0x0F) as f32 - n0); }
                        for l in 0..32 { out.push(d1 * (qs[g * 32 + l] >> 4) as f32 - n1); }
                    }
                }
            }
            GGML_Q6_K => {
                let nb = n / 256;
                for b in 0..nb {
                    let p = b * TAILLE_Q6K;
                    let ql = &buf[p..p + 128];
                    let qh = &buf[p + 128..p + 192];
                    let sc = &buf[p + 192..p + 208];
                    let d = Self::f16_to_f32(u16::from_le_bytes(buf[p+208..p+210].try_into().unwrap()));
                    for moitie in 0..2 {
                        let (ql, qh, sc) = (&ql[moitie*64..], &qh[moitie*32..], &sc[moitie*8..]);
                        // ggml écrit les quatre quants en QUARTS SUCCESSIFS :
                        // q1 remplit [0,32), q2 [32,64), q3 [64,96), q4 [96,128).
                        // Les entrelacer par `l` donne des poids faux — écart 0,10
                        // sur une échelle de 0,08, mesuré contre une référence F16.
                        let mut tmp = [0f32; 128];
                        for l in 0..32 {
                            let is = l / 16;
                            let q1 = ((ql[l] & 0x0F) | ((qh[l] & 3) << 4)) as i16 - 32;
                            let q2 = ((ql[l + 32] & 0x0F) | (((qh[l] >> 2) & 3) << 4)) as i16 - 32;
                            let q3 = ((ql[l] >> 4) | (((qh[l] >> 4) & 3) << 4)) as i16 - 32;
                            let q4 = ((ql[l + 32] >> 4) | (((qh[l] >> 6) & 3) << 4)) as i16 - 32;
                            let s = |k: usize| d * (sc[is + k] as i8) as f32;
                            tmp[l] = s(0) * q1 as f32;
                            tmp[l + 32] = s(2) * q2 as f32;
                            tmp[l + 64] = s(4) * q3 as f32;
                            tmp[l + 96] = s(6) * q4 as f32;
                        }
                        out.extend_from_slice(&tmp);
                    }
                }
            }
            GGML_Q2_K | GGML_Q3_K | GGML_Q5_K | GGML_IQ2_XXS | GGML_IQ3_XXS
            | GGML_IQ1_S | GGML_IQ4_XS | GGML_IQ1_M => {
                let (taille, f): (usize, fn(&[u8]) -> Vec<f32>) = match t.ttype {
                    GGML_Q2_K => (84, Self::dequant_q2k),
                    GGML_Q3_K => (110, Self::dequant_q3k),
                    GGML_Q5_K => (TAILLE_Q5K, Self::dequant_q5k),
                    GGML_IQ2_XXS => (66, crate::formats::dequant_iq2xxs),
                    GGML_IQ3_XXS => (98, crate::formats::dequant_iq3xxs),
                    GGML_IQ1_S => (50, crate::formats::dequant_iq1s),
                    GGML_IQ4_XS => (136, crate::formats::dequant_iq4xs),
                    _ => (56, crate::formats::dequant_iq1m),
                };
                let nb = n / 256;
                for b in 0..nb { out.extend_from_slice(&f(&buf[b * taille..])); }
            }
            other => panic!("dequant : type {other} non géré"),
        }
        out
    }
}

#[cfg(test)]
pub(crate) mod tests {
    use super::*;
    use std::io::Write;

    /// L'analyseur du bloc `<arch>.config` : sur un JSON réel de DeepSeek-V4.1,
    /// réduit à ce qui sert. Vérifie aussi le piège de la clef qui apparaît
    /// d'abord dans une chaîne (« scoring_func » dans `architectures`).
    #[test]
    fn json_du_config_brut() {
        let corps = concat!(
            r#"{"architectures":["DeepseekV41ForCausalLM"],"hidden_size":5120,"#,
            r#""scoring_func":"sqrtsoftplus","norm_topk_prob":true,"dtype":"bfloat16","#,
            r#""routed_scaling_factor":1.5,"n_routed_experts":384,"num_experts_per_tok":6,"#,
            r#""rope_theta":10000,"rope_scaling":{"beta_fast":32,"factor":16},"#,
            r#""use_cache":false,"sliding_window":128}"#);
        // GGUF minimal contenant une chaîne de métadonnée `essai.config`.
        let mut b: Vec<u8> = Vec::new();
        let mut s = |b: &mut Vec<u8>, v: &str| {
            b.extend_from_slice(&(v.len() as u64).to_le_bytes());
            b.extend_from_slice(v.as_bytes());
        };
        b.extend_from_slice(b"GGUF");
        b.extend_from_slice(&3u32.to_le_bytes());
        b.extend_from_slice(&0u64.to_le_bytes());
        b.extend_from_slice(&2u64.to_le_bytes());
        s(&mut b, "general.architecture");
        b.extend_from_slice(&8u32.to_le_bytes());
        s(&mut b, "essai");
        s(&mut b, "essai.config");
        b.extend_from_slice(&8u32.to_le_bytes());
        s(&mut b, corps);
        b.extend_from_slice(&32u64.to_le_bytes());
        let chemin = std::env::temp_dir().join("drave_config_json.gguf");
        std::fs::File::create(&chemin).unwrap().write_all(&b).unwrap();
        let g = Gguf::open(chemin.to_str().unwrap()).unwrap();
        assert_eq!(g.json_texte("scoring_func").as_deref(), Some("sqrtsoftplus"));
        assert_eq!(g.json_bool("norm_topk_prob"), Some(true));
        assert_eq!(g.json_bool("use_cache"), Some(false));
        assert_eq!(g.json_nombre("routed_scaling_factor"), Some(1.5));
        assert_eq!(g.json_nombre("n_routed_experts"), Some(384.0));
        assert_eq!(g.json_nombre("rope_theta"), Some(10000.0));
        assert_eq!(g.json_nombre("sliding_window"), Some(128.0));
        assert_eq!(g.json_nombre("clef_absente"), None);
        // Les clefs normalisées d'abord, les noms DeepSeek ensuite.
        assert_eq!(g.cfg_ou(&["expert_count", "n_routed_experts"]).and_then(|m| m.as_u64()), None,
                   "les noms DeepSeek ne sont PAS des clefs GGUF : ils vivent dans le JSON");
    }

    /// L'échelle E8M0 de MXFP4, cas par cas, valeurs recopiées de
    /// `ggml_e8m0_to_fp32` (ggml-impl.h) : c'est la convention qui va avec la
    /// VRAIE grille E2M1. La convention jumelle (grille doublée) utilise
    /// `2^(e−128)` et se trompe d'un facteur 2 si on la mélange.
    #[test]
    fn echelle_e8m0_comme_ggml() {
        assert_eq!(Gguf::echelle_e8m0(0), f32::from_bits(0x0040_0000)); // 2^−127
        assert_eq!(Gguf::echelle_e8m0(1), 2f32.powi(-126));
        assert_eq!(Gguf::echelle_e8m0(2), 2f32.powi(-125));
        assert_eq!(Gguf::echelle_e8m0(127), 1.0);
        assert_eq!(Gguf::echelle_e8m0(128), 2.0);
        assert_eq!(Gguf::echelle_e8m0(255), f32::INFINITY);
        // Et le rapport exact qui a trahi le bug : la moitié de la convention
        // doublée vaut 2^(e−128).
        for e in 2..200u8 {
            assert_eq!(Gguf::echelle_e8m0(e), 2.0 * f32::from_bits(((e as u32) - 1) << 23));
        }
    }

    /// Un bloc MXFP4 complet : `e = 127` (échelle 1,0) et des nibbles connus,
    /// comparé aux valeurs de la table E2M1. Sans cela, seule la comparaison à
    /// libggml attrape le facteur 2 — et elle demande un modèle de 60 Go.
    #[test]
    fn mxfp4_bloc_dun_facteur_deux() {
        // 17 octets : e, puis 16 octets de nibbles.
        let mut bloc = vec![127u8];
        for j in 0..16u8 { bloc.push(j | (15 - j) << 4); }
        let v = Gguf::dequant_mxfp4(&bloc);
        // Grille E2M1 telle qu'elle est écrite dans le code, pour que le test
        // porte sur la VALEUR et pas sur une seconde copie de la même erreur.
        let kv: [f32; 16] = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0,
                             0.0, -0.5, -1.0, -1.5, -2.0, -3.0, -4.0, -6.0];
        for j in 0..16usize {
            assert_eq!(v[j], kv[j], "nibble bas du poids {j}");
            assert_eq!(v[j + 16], kv[15 - j], "nibble haut du poids {}", j + 16);
        }
        // Une échelle de 2^(e−128) donnerait la moitié, une échelle annulée
        // pour e = 255 donnerait zéro : les deux sont refusées ici.
        assert_eq!(Gguf::echelle_e8m0(255), f32::INFINITY);
    }

    /// Fabrique un GGUF minimal : `general.architecture` plus des tenseurs F32
    /// dont la valeur de chaque poids est son indice global. Un GGUF de labo,
    /// écrit à la main, uniquement pour éprouver le lecteur.
    pub(crate) fn gguf_synth(tensors: &[(&str, Vec<u64>)], depart: usize, valeur0: f32) -> Vec<u8> {
        let mut b = Vec::new();
        let mut s = |b: &mut Vec<u8>, v: &str| {
            b.extend_from_slice(&(v.len() as u64).to_le_bytes());
            b.extend_from_slice(v.as_bytes());
        };
        b.extend_from_slice(b"GGUF");
        b.extend_from_slice(&3u32.to_le_bytes());
        b.extend_from_slice(&(tensors.len() as u64).to_le_bytes());
        b.extend_from_slice(&2u64.to_le_bytes());        // deux métadonnées
        // Ordre GGUF : clef, type (u32), valeur.
        s(&mut b, "general.architecture");
        b.extend_from_slice(&8u32.to_le_bytes());        // GGUF_TYPE_STRING
        s(&mut b, "essai");
        s(&mut b, "general.alignment");
        b.extend_from_slice(&4u32.to_le_bytes());        // GGUF_TYPE_UINT32
        b.extend_from_slice(&32u32.to_le_bytes());

        // Les décalages sont relatifs au début du bloc de données de CE fichier.
        let mut offsets = Vec::new();
        let mut cur = 0u64;
        for (_, dims) in tensors {
            offsets.push(cur);
            cur += dims.iter().product::<u64>() * 4;
        }
        for ((nom, dims), off) in tensors.iter().zip(&offsets) {
            s(&mut b, nom);
            b.extend_from_slice(&(dims.len() as u32).to_le_bytes());
            for d in dims.iter().rev() {                  // ggml écrit à l'envers
                b.extend_from_slice(&d.to_le_bytes());
            }
            b.extend_from_slice(&GGML_F32.to_le_bytes());
            b.extend_from_slice(&off.to_le_bytes());
        }
        while b.len() % 32 != 0 { b.push(0); }
        for (i, (_, dims)) in tensors.iter().enumerate() {
            let n = dims.iter().product::<u64>();
            for k in 0..n {
                let v = valeur0 + (depart + i) as f32 * 1000.0 + k as f32;
                b.extend_from_slice(&v.to_le_bytes());
            }
        }
        b
    }

    /// GGUF synthétique **Q4_0** : blocs de 18 octets (échelle f16 + 16 octets de
    /// nibbles). C'est le type le plus simple que `source_de` accepte — sans lui,
    /// aucun test ne peut construire un `Moe`, et donc le chemin des experts
    /// n'est couvert par rien (un correctif sans test ne vaut rien).
    ///
    /// Les dims sont données en convention numpy (le plus lent d'abord) et
    /// écrites à l'envers, comme ggml.
    pub(crate) fn gguf_synth_q4_0(tensors: &[(&str, Vec<u64>)], valeur0: f32) -> Vec<u8> {
        let mut b = Vec::new();
        let mut s = |b: &mut Vec<u8>, v: &str| {
            b.extend_from_slice(&(v.len() as u64).to_le_bytes());
            b.extend_from_slice(v.as_bytes());
        };
        b.extend_from_slice(b"GGUF");
        b.extend_from_slice(&3u32.to_le_bytes());
        b.extend_from_slice(&(tensors.len() as u64).to_le_bytes());
        b.extend_from_slice(&2u64.to_le_bytes());
        s(&mut b, "general.architecture");
        b.extend_from_slice(&8u32.to_le_bytes());
        s(&mut b, "essai");
        s(&mut b, "general.alignment");
        b.extend_from_slice(&4u32.to_le_bytes());
        b.extend_from_slice(&32u32.to_le_bytes());
        let mut offsets = Vec::new();
        let mut cur = 0u64;
        for (_, dims) in tensors {
            offsets.push(cur);
            let n: u64 = dims.iter().product();
            cur += n / 32 * 18;                      // Q4_0 : 18 octets par 32 poids
        }
        for ((nom, dims), off) in tensors.iter().zip(&offsets) {
            s(&mut b, nom);
            b.extend_from_slice(&(dims.len() as u32).to_le_bytes());
            for d in dims.iter().rev() { b.extend_from_slice(&d.to_le_bytes()); }
            b.extend_from_slice(&GGML_Q4_0.to_le_bytes());
            b.extend_from_slice(&off.to_le_bytes());
        }
        while b.len() % 32 != 0 { b.push(0); }
        for (i, (_, dims)) in tensors.iter().enumerate() {
            let n: u64 = dims.iter().product();
            for bloc in 0..n / 32 {
                // Échelle 0,25 (exacte en f16), nibbles déterministes.
                b.extend_from_slice(&Gguf::f32_to_f16(0.25).to_le_bytes());
                for j in 0..16u64 {
                    let idx = bloc * 32 + j;
                    let bas = ((idx + i as u64) % 15) as u8;
                    let haut = ((idx + i as u64 + 7) % 15) as u8;
                    b.push(bas | (haut << 4));
                }
            }
            let _ = valeur0;
        }
        b
    }

    /// GGUF synthétique Q8_0 : blocs de 34 octets (échelle f16 + 32 niveaux
    /// i8). Les niveaux sont `(i % 200) - 100` et l'échelle vaut 0,25, ce qui
    /// donne des valeurs exactement représentables : le produit scalaire attendu
    /// se calcule à la main, sans arrondi.
    fn gguf_synth_q8(nom: &str, n_lignes: usize, n_cols: usize, decalage: i32) -> Vec<u8> {
        let mut b = Vec::new();
        let mut s = |b: &mut Vec<u8>, v: &str| {
            b.extend_from_slice(&(v.len() as u64).to_le_bytes());
            b.extend_from_slice(v.as_bytes());
        };
        b.extend_from_slice(b"GGUF");
        b.extend_from_slice(&3u32.to_le_bytes());
        b.extend_from_slice(&1u64.to_le_bytes());
        b.extend_from_slice(&2u64.to_le_bytes());
        s(&mut b, "general.architecture");
        b.extend_from_slice(&8u32.to_le_bytes());
        s(&mut b, "essai");
        s(&mut b, "general.alignment");
        b.extend_from_slice(&4u32.to_le_bytes());
        b.extend_from_slice(&32u32.to_le_bytes());
        s(&mut b, nom);
        b.extend_from_slice(&2u32.to_le_bytes());
        b.extend_from_slice(&(n_cols as u64).to_le_bytes());
        b.extend_from_slice(&(n_lignes as u64).to_le_bytes());
        b.extend_from_slice(&GGML_Q8_0.to_le_bytes());
        b.extend_from_slice(&0u64.to_le_bytes());
        while b.len() % 32 != 0 { b.push(0); }
        for l in 0..n_lignes {
            for c in 0..n_cols / 32 {
                b.extend_from_slice(&Gguf::f32_to_f16(0.25).to_le_bytes());
                for j in 0..32 {
                    let niveau = (((l * 32 + c * 32 + j) as i32 + decalage) % 200 - 100) as i8;
                    b.push(niveau as u8);
                }
            }
        }
        b
    }

    /// `q8_dot_at` est le chemin le plus chaud du moteur (la tête de sortie) et
    /// il passe par une vue pré-résolue, donc par un offset. Ce test l'exerce
    /// contre un calcul direct : c'est le SEUL qui attrape une erreur d'origine
    /// du pointeur, parce qu'un test comparant deux chemins qui partagent la
    /// même origine ne peut pas la voir (c'est arrivé : le chemin AVX2 et le
    /// chemin scalaire étaient faux de la même façon, et la perplexité est
    /// passée à NaN sans qu'aucun test ne bronche).
    #[test]
    fn q8_dot_at_voit_les_bons_octets() {
        let (n_lignes, n_cols, decalage) = (5usize, 64usize, 7i32);
        let p = ecrire("drave_gguf_q8.gguf",
                       &gguf_synth_q8("w", n_lignes, n_cols, decalage));
        let g = Gguf::open(&p).unwrap();
        let v = g.q8_view("w");
        assert_eq!(v.n_cols, n_cols);
        assert_eq!(v.nb, n_cols / 32);
        let qx: Vec<i16> = (0..n_cols).map(|i| ((i as i32 % 13) - 6) as i16).collect();
        for ligne in 0..n_lignes {
            let attendu: f32 = (0..n_cols).map(|j| {
                let niveau = (((ligne * 32 + j) as i32 + decalage) % 200 - 100) as f32;
                0.25 * niveau * qx[j] as f32
            }).sum();
            let obtenu = g.q8_dot_at(&v, ligne, &qx);
            assert!((obtenu - attendu).abs() < 1e-3,
                    "ligne {ligne} : {obtenu} au lieu de {attendu}");
        }
        let _ = std::fs::remove_file(&p);
    }

    pub(crate) fn ecrire(nom: &str, octets: &[u8]) -> std::path::PathBuf {
        let p = std::env::temp_dir().join(nom);
        let mut f = File::create(&p).unwrap();
        f.write_all(octets).unwrap();
        p
    }

    /// Un modèle éclaté en deux fichiers doit se lire EXACTEMENT comme le même
    /// modèle d'un seul tenant : mêmes métadonnées, mêmes tenseurs, mêmes poids.
    /// C'est la propriété dont dépend tout le format en clusters — si elle est
    /// fausse, les mesures faites dessus ne veulent rien dire.
    #[test]
    fn multi_fichiers_egale_mono_fichier() {
        let t1: Vec<(&str, Vec<u64>)> =
            vec![("blk.0.attn_q.weight", vec![4, 8]), ("blk.1.ffn_gate.weight", vec![2, 3])];
        let t2: Vec<(&str, Vec<u64>)> =
            vec![("blk.2.ffn_down.weight", vec![5, 2]), ("blk.3.token_embd.weight", vec![3, 3])];
        // Mono-fichier : les quatre tenseurs, valeurs de référence.
        let tous: Vec<(&str, Vec<u64>)> = t1.iter().chain(t2.iter()).cloned().collect();
        let p_tous = ecrire("drave_gguf_tous.gguf", &gguf_synth(&tous, 0, 1.0));
        // Éclaté : deux fichiers, quatre tenseurs répartis, valeurs distinctes
        // PAR FICHIER (un lecteur qui se tromperait de fichier serait démasqué).
        let p_a = ecrire("drave_gguf_a.gguf", &gguf_synth(&t1, 0, 1.0));
        let p_b = ecrire("drave_gguf_b.gguf", &gguf_synth(&t2, 2, 1.0));

        let mono = Gguf::open(&p_tous).unwrap();
        let multi = Gguf::open_multi(&[&p_a, &p_b]).unwrap();

        assert_eq!(mono.tensors.len(), 4);
        assert_eq!(multi.tensors.len(), 4, "les tenseurs des deux fichiers doivent être réunis");
        assert_eq!(multi.nb_fichiers(), 2);
        assert_eq!(multi.meta.get("general.architecture").and_then(|m| m.as_str()),
                   Some("essai"), "les métadonnées du premier fichier doivent être reprises");

        for (a, b) in mono.tensors.iter().zip(&multi.tensors) {
            assert_eq!(a.name, b.name);
            assert_eq!(a.dims, b.dims);
            assert_eq!(a.ttype, b.ttype);
            assert_eq!(multi.dequant(&b.name), mono.dequant(&a.name),
                       "poids divergents pour {}", a.name);
        }
        // Le tenseur du second fichier doit VRAIMENT venir du second fichier.
        assert_eq!(multi.tensor("blk.3.token_embd.weight").unwrap().fichier, 1);
        assert_eq!(multi.tensor("blk.1.ffn_gate.weight").unwrap().fichier, 0);
        // Les POIDS sont identiques ; le total des fichiers ne l'est pas, et
        // c'est normal : chaque morceau paie son propre en-tête. Le comparer
        // serait comparer deux choses différentes.
        assert_eq!(multi.octets_poids(), mono.octets_poids());
        assert!(multi.octets_charges() > mono.octets_charges(),
                "un modèle éclaté en deux fichiers paie deux en-têtes");
        let _ = std::fs::remove_file(&p_tous);
        let _ = std::fs::remove_file(&p_a);
        let _ = std::fs::remove_file(&p_b);
    }

    /// Q2_K : notre déquantification doit rendre EXACTEMENT les valeurs de ggml.
    ///
    /// Le bloc est fabriqué à la main, et les valeurs attendues viennent du code
    /// de référence de ggml (`dequantize_row_q2_K`), vérifié sur deux couches
    /// réelles de DeepSeek-V4.1 (écart max 5e-8 sur 256 valeurs).
    #[test]
    fn q2k_concorde_avec_ggml() {
        // Toutes les échelles à 0x11 : sc = 1 et m = 1 pour chaque sous-bloc, ce
        // qui donne une formule vérifiable à la main :
        //     w = d·1·q − dmin·1 = q − 0,5     avec d = 1,0 et dmin = 0,5.
        let mut bloc = vec![0x11u8; 84];
        // Quants : 0b11_10_01_00 → les quatre décalages (0, 2, 4, 6) rendent
        // respectivement 0, 1, 2 et 3.
        for q in bloc[16..80].iter_mut() { *q = 0b11_10_01_00; }
        // d = 1,0 (0x3C00) et dmin = 0,5 (0x3800), en f16 little-endian.
        bloc[80] = 0x00; bloc[81] = 0x3C;
        bloc[82] = 0x00; bloc[83] = 0x38;
        let v = Gguf::dequant_q2k(&bloc);
        assert_eq!(v.len(), 256);
        // Le décalage `k` décide du quant, et l'indice de sortie est
        // `moitié·128 + k·32 + l`.
        for moitie in 0..2usize {
            for k in 0..4usize {
                for l in 0..32usize {
                    let idx = moitie * 128 + k * 32 + l;
                    let attendu = k as f32 - 0.5;
                    assert!((v[idx] - attendu).abs() < 1e-6,
                            "poids {idx} (moitié {moitie}, décalage {k}, l {l}) : \
{} au lieu de {attendu}", v[idx]);
                }
            }
        }
    }

    /// `open_avec_prefixes` est la route des clusters : huit fichiers portent
    /// les MÊMES noms de tenseurs, et seul le préfixe les distingue. Sans test,
    /// un défaut ici ferait disparaître sept clusters sur huit (c'est arrivé :
    /// l'inventaire annonçait 3,19 Go au lieu de 18,55).
    #[test]
    fn prefixes_distinguent_les_homonymes() {
        let t: Vec<(&str, Vec<u64>)> = vec![("blk.0.ffn_gate_exps.weight", vec![2, 3])];
        let p0 = ecrire("drave_gguf_p0.gguf", &gguf_synth(&t, 0, 1.0));
        let p1 = ecrire("drave_gguf_p1.gguf", &gguf_synth(&t, 1, 1.0));
        let p2 = ecrire("drave_gguf_p2.gguf", &gguf_synth(&t, 2, 1.0));
        let g = Gguf::open_avec_prefixes(&[&p0, &p1, &p2], &["", "cl0/", "cl1/"]).unwrap();
        assert_eq!(g.tensors.len(), 3, "trois fichiers, trois tenseurs homonymes");
        assert_eq!(g.nb_fichiers(), 3);
        assert_eq!(g.octets_poids(), 3 * 6 * 4);
        for (nom, f) in [("blk.0.ffn_gate_exps.weight", 0), ("cl0/blk.0.ffn_gate_exps.weight", 1),
                         ("cl1/blk.0.ffn_gate_exps.weight", 2)] {
            let t = g.tensor(nom).unwrap_or_else(|| panic!("{nom} absent"));
            assert_eq!(t.fichier, f, "« {nom} » doit venir du fichier {f}");
        }
        // Les trois valeurs sont distinctes : unlecteur qui se tromperait de
        // fichier serait démasqué.
        let v0 = g.dequant("blk.0.ffn_gate_exps.weight");
        let v1 = g.dequant("cl0/blk.0.ffn_gate_exps.weight");
        let v2 = g.dequant("cl1/blk.0.ffn_gate_exps.weight");
        assert_ne!(v0, v1);
        assert_ne!(v1, v2);
        assert!((v1[0] - v0[0] - 1000.0).abs() < 1e-3, "décalage de fichier attendu");
        // Et le mode en-tête seul doit voir la MÊME chose, sans les poids.
        let m = Gguf::open_meta_avec_prefixes(&[&p0, &p1, &p2], &["", "cl0/", "cl1/"]).unwrap();
        assert_eq!(m.tensors.len(), 3);
        assert_eq!(m.tensor("cl1/blk.0.ffn_gate_exps.weight").unwrap().fichier, 2);
        for p in [&p0, &p1, &p2] { let _ = std::fs::remove_file(p); }
    }

    /// Un type ggml hors table était compté zéro octet en silence. Le total
    /// devenait faux sans le dire — c'est le mécanisme exact qui avait fait
    /// annoncer 8,56 Go pour 86,9 Go de fichiers.
    #[test]
    fn type_inconnu_ne_compte_pas_zero_en_silence() {
        let t = TensorInfo { name: "x".into(), dims: vec![256, 4], ttype: 4_242,
                             offset: 0, fichier: 0 };
        assert_eq!(Gguf::octets_tensor_opt(&t), None);
        // Les types connus, eux, sont tous dans la table.
        for (ttype, attendu) in [(GGML_F32, 4 * 1024u64), (GGML_Q8_0, 34 * 32),
                                 (GGML_Q4_K, 144 * 4), (GGML_Q6_K, 210 * 4),
                                 (GGML_MXFP4, 17 * 32), (29, 56 * 4), (30, 2 * 1024)] {
            let t = TensorInfo { name: "x".into(), dims: vec![1024], ttype,
                                 offset: 0, fichier: 0 };
            assert_eq!(Gguf::octets_tensor_opt(&t), Some(attendu),
                       "type {ttype} : table fausse");
        }
    }

    /// `shard_de` et `chemins_du_modele` : la détection automatique des shards.
    #[test]
    fn shards_reconnus_et_rassembles() {
        assert_eq!(Gguf::shard_de("m-00002-of-00003.gguf"),
                   Some(("m".to_string(), 2, 3)));
        assert_eq!(Gguf::shard_de("a-b-c-00010-of-00012.gguf"),
                   Some(("a-b-c".to_string(), 10, 12)));
        // Un nom qui n'est pas un découpage ne doit pas être pris pour un.
        assert_eq!(Gguf::shard_de("modele.gguf"), None);
        assert_eq!(Gguf::shard_de("modele-of-3.gguf"), None);
        assert_eq!(Gguf::shard_de("modele-abc-of-00003.gguf"), None);

        // Deux morceaux sur trois : c'est INCOMPLET, et ça doit se dire.
        let d = std::env::temp_dir().join("drave_shards_test");
        let _ = std::fs::remove_dir_all(&d);
        std::fs::create_dir_all(&d).unwrap();
        let t: Vec<(&str, Vec<u64>)> = vec![("w", vec![2, 2])];
        for n in 1..=3 {
            std::fs::write(d.join(format!("m-{n:05}-of-00003.gguf")), gguf_synth(&t, n, 1.0)).unwrap();
        }
        let l = Gguf::chemins_du_modele(&d.join("m-00002-of-00003.gguf")).unwrap();
        assert_eq!(l.len(), 3, "les trois morceaux doivent être rassemblés dans l'ordre");
        assert!(l[0].to_string_lossy().ends_with("m-00001-of-00003.gguf"));
        std::fs::remove_file(d.join("m-00002-of-00003.gguf")).unwrap();
        let e = match Gguf::chemins_du_modele(&d.join("m-00001-of-00003.gguf")) {
            Ok(_) => panic!("un shard manquant doit être refusé"),
            Err(e) => e,
        };
        assert!(e.to_string().contains("incomplet"), "{e}");
        let _ = std::fs::remove_dir_all(&d);
    }

    /// Un même nom dans deux fichiers avec des poids différents est une faute
    /// d'assemblage : elle doit être refusée, pas départagée en silence.
    #[test]
    fn multi_fichiers_refuse_les_doublons_divergents() {
        let t: Vec<(&str, Vec<u64>)> = vec![("blk.0.attn_q.weight", vec![4, 4])];
        let p_a = ecrire("drave_gguf_d1.gguf", &gguf_synth(&t, 0, 1.0));
        let p_b = ecrire("drave_gguf_d2.gguf", &gguf_synth(&t, 5, 1.0));
        let e = match Gguf::open_multi(&[&p_a, &p_b]) {
            Ok(_) => panic!("un doublon divergent doit être refusé"),
            Err(e) => e,
        };
        assert!(e.to_string().contains("deux fois"), "message inattendu : {e}");
        // Le même tenseur recopié à l'identique, lui, est toléré.
        let p_c = ecrire("drave_gguf_d3.gguf", &gguf_synth(&t, 0, 1.0));
        let ok = Gguf::open_multi(&[&p_a, &p_c]).unwrap();
        assert_eq!(ok.tensors.len(), 1);
        for p in [&p_a, &p_b, &p_c] { let _ = std::fs::remove_file(p); }
    }
}
