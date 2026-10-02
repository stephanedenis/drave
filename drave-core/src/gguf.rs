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

/// Demande au noyau de **lancer en avance** les lectures d'une plage mappée.
///
/// C'est la seule forme de parallélisme de lecture accessible depuis l'espace
/// utilisateur quand les poids sont mmappés : on ne peut pas lire soi-même sans
/// renoncer au mmap. Le noyau, lui, peut lancer plusieurs lectures de pages en
/// parallèle — et c'est ce qui compte, parce que le NVMe passe de 5,4 Go/s à un
/// lecteur à **31 Go/s à seize**.
///
/// Ne fait rien si la plage n'est pas mappée (modèle lu en mémoire) : l'appel
/// est alors sans objet, pas faux.
pub fn prelire(ptr: *const u8, octets: usize) {
    if ptr.is_null() || octets == 0 { return; }
    // `DRAVE_PRELIRE=0` la désactive : sans ce témoin, on ne pourrait pas dire
    // si un gain vient d'elle ou du cache qui se réchauffe d'un passage à
    // l'autre.
    if !prelire_active() { return; }
    unsafe { madvise(ptr as *mut u8, octets, MADV_WILLNEED); }
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
            Ok(m) => return Ok(Tampon::Mappe(m)),
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
    pub fn as_u64(&self) -> Option<u64> {
        match self {
            Meta::U32(v) => Some(*v as u64),
            Meta::U64(v) => Some(*v),
            Meta::I32(v) => Some(*v as u64),
            Meta::I64(v) => Some(*v as u64),
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
pub const GGML_Q4_K: u32 = 12;
pub const GGML_Q6_K: u32 = 14;

/// BF16 : un f32 dont on ne garde que les 16 bits de poids fort. Le convertir
/// n'est pas une approximation — c'est exactement ce que le format stocke.
#[inline]
pub fn bf16_to_f32(h: u16) -> f32 { f32::from_bits((h as u32) << 16) }

/// Octets par super-bloc : Q4_K = 2+2+12+128 (256 poids), Q6_K = 128+64+16+2.
pub const TAILLE_Q4K: usize = 144;
pub const TAILLE_Q6K: usize = 210;

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
    pub fn raw_levels(&self, name: &str) -> Vec<i8> {
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
            other => panic!("raw_levels : type {other} non géré"),
        }
        out
    }

    /// Déquantifie un bloc **Q2_K** (84 octets, 256 poids).
    ///
    /// Structure : 16 octets d'échelles (4 bits d'échelle, 4 bits de minimum par
    /// sous-bloc de 16 poids), 64 octets de quants 2 bits, puis d et dmin en f16.
    /// `x = d·sc·q − dmin·m`. C'est le type des `ffn_down_exps` de
    /// DeepSeek-V4.1 — sans lui, 59 Go du modèle restent illisibles.
    pub fn dequant_q2k(bloc: &[u8]) -> Vec<f32> {
        assert!(bloc.len() >= 84, "bloc Q2_K trop court : {}", bloc.len());
        let scales = &bloc[0..16];
        let qs = &bloc[16..80];
        let d = Self::f16_to_f32(u16::from_le_bytes([bloc[80], bloc[81]]));
        let dmin = Self::f16_to_f32(u16::from_le_bytes([bloc[82], bloc[83]]));
        let mut out = vec![0f32; 256];
        // Quatre passes de 64 poids : chaque octet porte quatre quants 2 bits,
        // lus aux décalages 0, 2, 4 et 6.
        for moitie in 0..2usize {
            let q = &qs[moitie * 32..moitie * 32 + 32];
            for l in 0..32usize {
                for (k, decal) in [0usize, 2, 4, 6].iter().enumerate() {
                    // L'ordre des échelles suit le parcours du code ggml :
                    // moitié, puis décalage, puis les deux sous-groupes de 16.
                    let is = moitie * 8 + k * 2 + (l / 16);
                    let sc = (scales[is] & 0x0F) as f32;
                    let m = (scales[is] >> 4) as f32;
                    let quant = ((q[l] >> decal) & 3) as f32;
                    out[moitie * 128 + k * 32 + l] = d * sc * quant - dmin * m;
                }
            }
        }
        out
    }

    /// Déquantifie une ligne d'un tenseur 2D, en f32.
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
            GGML_Q2_K => {
                let ns = n_cols / 256;
                for sup in 0..ns {
                    let p = (row * ns + sup) * 84;
                    out.extend_from_slice(&Self::dequant_q2k(&buf[p..]));
                }
            }
            GGML_Q2_K => {
                let ns = n_cols / 256;
                for sup in 0..ns {
                    let p = (row * ns + sup) * 84;
                    out.extend_from_slice(&Self::dequant_q2k(&buf[p..]));
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
            GGML_MXFP4 => {
                // 17 octets par bloc de 32 : exposant E8M0 puis nibbles E2M1.
                // L'échelle vaut 2^(e−127) ; e = 0 et e = 255 sont dégénérés.
                const KV: [f32; 16] = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0,
                                       0.0, -0.5, -1.0, -1.5, -2.0, -3.0, -4.0, -6.0];
                let nb = n / 32;
                for b in 0..nb {
                    let p = b * 17;
                    let e = buf[p] as u32;
                    let d = if e == 0 || e == 255 { 0.0 } else { f32::from_bits((e - 1) << 23) };
                    for j in 0..16 { out.push(KV[(buf[p + 1 + j] & 0x0F) as usize] * d); }
                    for j in 0..16 { out.push(KV[(buf[p + 1 + j] >> 4) as usize] * d); }
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
            other => panic!("dequant : type {other} non géré"),
        }
        out
    }
}

#[cfg(test)]
pub(crate) mod tests {
    use super::*;
    use std::io::Write;

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
