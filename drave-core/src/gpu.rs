//! Chemin GPU : noyaux PTX chargés par l'API **pilote** de CUDA.
//!
//! Rien n'est lié à l'édition : le noyau est du PTX, compilé à la volée par le
//! pilote. Le programme ne dépend donc que de `libcuda.so`, présent avec
//! n'importe quel pilote NVIDIA — pas de boîte à outils CUDA à l'exécution.
//!
//! Principe de placement : **les poids restent sur le GPU**. Mesuré : PCIe x8
//! 6,5 Go/s contre 380 Go/s en lecture locale et 20 Go/s sur CPU. Déplacer les
//! poids à chaque jeton coûterait plus cher que de les lire sur CPU ; ne
//! traversent donc le bus que les activations (quelques kilo-octets) et le
//! résultat.

use std::ffi::c_void;
use std::os::raw::{c_char, c_int, c_uint};

#[link(name = "cuda")]
extern "C" {
    fn cuInit(flags: c_uint) -> c_int;
    fn cuDeviceGet(dev: *mut c_int, ordinal: c_int) -> c_int;
    fn cuDevicePrimaryCtxRetain(ctx: *mut *mut c_void, dev: c_int) -> c_int;
    fn cuCtxCreate_v2(ctx: *mut *mut c_void, flags: c_uint, dev: c_int) -> c_int;
    fn cuCtxSetCurrent(ctx: *mut c_void) -> c_int;
    fn cuModuleLoadData(module: *mut *mut c_void, image: *const c_void) -> c_int;
    fn cuModuleGetFunction(f: *mut *mut c_void, module: *mut c_void, name: *const c_char) -> c_int;
    fn cuMemAlloc_v2(dptr: *mut u64, octets: usize) -> c_int;
    fn cuMemcpyHtoD_v2(dst: u64, src: *const c_void, octets: usize) -> c_int;
    fn cuMemcpyDtoH_v2(dst: *mut c_void, src: u64, octets: usize) -> c_int;
    fn cuMemcpyDtoD_v2(dst: u64, src: u64, octets: usize) -> c_int;
    fn cuLaunchKernel(f: *mut c_void, gx: c_uint, gy: c_uint, gz: c_uint,
                      bx: c_uint, by: c_uint, bz: c_uint, partage: c_uint,
                      flux: *mut c_void, params: *mut *mut c_void,
                      extra: *mut c_void) -> c_int;
    fn cuCtxSynchronize() -> c_int;
    fn cuMemFree_v2(dptr: u64) -> c_int;
    fn cuMemsetD32_v2(dst: u64, valeur: c_uint, n: usize) -> c_int;
    fn cuGetErrorName(code: c_int, nom: *mut *const c_char) -> c_int;
}

/// PTX compilé depuis `gpu/drave_gpu.cu` par clang.
const PTX: &str = include_str!("../gpu/drave_gpu.ptx");

#[inline]
fn cu_ctx(ctx: *mut c_void) {
    unsafe { cuCtxSetCurrent(ctx) };
}

/// Garantit `octets` dans un tampon VRAM : n'alloue QUE si la capacité actuelle
/// ne suffit pas, et libère l'ancien tampon alors. Les quatre tampons du top-k
/// (quelques kilo-octets) ne sont donc alloués qu'une fois.
///
/// # Safety
/// `p` doit être un pointeur de périphérique valide ou 0, et `cap` sa capacité.
unsafe fn vram_assurer(p: &mut u64, cap: &mut usize, octets: usize) -> bool {
    if *cap >= octets { return true; }
    if *p != 0 { cuMemFree_v2(*p); *p = 0; }
    *cap = 0;
    if cuMemAlloc_v2(p, octets) != 0 { return false; }
    *cap = octets;
    true
}

fn erreur(code: c_int, ou: &str) -> String {
    let mut nom: *const c_char = std::ptr::null();
    unsafe { cuGetErrorName(code, &mut nom) };
    let texte = if nom.is_null() {
        String::from("?")
    } else {
        unsafe { std::ffi::CStr::from_ptr(nom) }.to_string_lossy().into_owned()
    };
    format!("CUDA {ou} : {texte} ({code})")
}

/// Une matrice résidente sur le GPU, avec ses tampons d'entrée et de sortie.
pub struct MatriceGpu {
    poids: u64,
    x_dev: u64,
    out_dev: u64,
    pub n_out: usize,
    pub nb: usize,
    pub octets_poids: usize,
}

/// Cache KV d'UNE couche, résident en VRAM. Même disposition que `KvCache` :
/// `(tête KV, position)` puis la dimension de tête — les noyaux lisent donc les
/// octets du cache CPU tels quels, sans conversion.
pub struct KvGpu {
    pub k: u64,
    pub v: u64,
    pub sk: u64,
    pub sv: u64,
    pub n_kv: usize,
    /// Capacité LOGIQUE (positions adressables par le moteur).
    pub ctx: usize,
    /// Capacité ALLOUÉE (positions réellement en VRAM), doublée à la demande :
    /// un contexte de 1 M ne réserve plus 24 Go d'un coup alors qu'on n'en a
    /// écrit que quelques milliers — c'est la « pagination » du plan E4, faite
    /// par doublement, sans toucher au noyau (il reçoit la capacité courante
    /// comme pas).
    pub capacite: usize,
    pub hd: usize,
    pub nb: usize,
    /// 32 = f32, 8 = un octet par valeur, 4 = deux nibbles par octet.
    pub bits: u32,
    /// Tampon de SCORES du noyau `attn_scores` (réutilisé, comme les autres).
    pub scores_dev: u64,
    pub scores_cap: usize,
    /// Histogrammes du radix select du top-k : `[lignes][256]` u32. 14 têtes ×
    /// 1 ko = 14 ko, alloué une fois et réutilisé à chaque passe des quatre.
    pub histo_dev: u64,
    pub histo_cap: usize,
    /// Préfixes du radix select, un u32 par ligne (téléversés à chaque passe).
    pub prefixes_dev: u64,
    pub prefixes_cap: usize,
    /// Tampons de la collecte des k indices (`attn_topk_collecte`).
    pub topk: Option<TamponsTopk>,
    pub octets: usize,
    // Tampons de travail RÉUTILISÉS d'un jeton à l'autre. Les allouer à chaque
    // appel coûtait 24 couches × 6 appels CUDA par jeton : mesuré 24,5 ms/jeton
    // d'attention à 512 jetons, contre 2,9 ms sur CPU — le noyau n'était pas en
    // cause, c'étaient les allocations.
    pub q_dev: u64,
    pub part_dev: u64,
    pub out_dev: u64,
    pub sinks_dev: u64,
    pub q_cap: usize,
    pub part_cap: usize,
    pub out_cap: usize,
    pub sinks_cap: usize,
}

/// Tampons VRAM de la COLLECTE du top-k (noyaux 2b). Dimensionnés pour un
/// triplet (lignes, tranches, k) ; réalloués seulement quand l'un grandit.
pub struct TamponsTopk {
    pub lignes: usize,
    pub ntr: usize,
    pub k: usize,
    pub chunk: usize,
    /// `compte_sup[l][t]` puis `compte_eq[l][t]` — sortie du premier noyau.
    pub comptes: u64,
    pub cap_comptes: usize,
    /// `base_sup[l][t]` puis `base_eq[l][t]` — sommes préfixées par l'hôte.
    pub bases: u64,
    pub cap_bases: usize,
    /// `prefixes[l]`, puis `debut_egaux[l]`, puis `besoin[l]`.
    pub meta: u64,
    pub cap_meta: usize,
    /// `sortie[l][k]` : les indices retenus, par ordre croissant.
    pub sortie: u64,
    pub cap_sortie: usize,
}

pub struct Gpu {
    ctx: *mut c_void,
    module: *mut c_void,
    f_tete: *mut c_void,
    f_proj: *mut c_void,
    f_tete_warp: *mut c_void,
    f_proj_warp: *mut c_void,
    f_mxfp4_warp: *mut c_void,
    f_q4k_warp: *mut c_void,
    f_q6k_warp: *mut c_void,
    f_attn_part: *mut c_void,
    f_attn_recombine: *mut c_void,
    /// Scores seuls (premier noyau du top-k, `docs/plan-gpu-topk.md`).
    f_attn_scores: *mut c_void,
    /// Histogramme d'octet du radix select (noyau 2a du plan).
    f_attn_topk_histo: *mut c_void,
    /// Collecte des k indices : comptage par tranche puis écriture ordonnée.
    f_attn_topk_compte: *mut c_void,
    f_attn_topk_ecrit: *mut c_void,
    /// Softmax sur les k retenus + somme pondérée des V (noyau 3 du plan).
    f_attn_topk_somme: *mut c_void,
    /// Le top-k COMPLET d'une ligne en un lancement (noyau 4) : descente radix,
    /// collecte et somme, sans aucun aller-retour par l'hôte.
    f_attn_topk_tout: *mut c_void,
    pub nom: String,
    /// Numéro du périphérique, pour savoir qui est qui quand il y en a deux.
    pub ordinal: c_int,
    pub memoire_libre: usize,
}

impl Gpu {
    /// Ouvre le périphérique 0 et charge les noyaux. `None` si CUDA est absent
    /// ou si le chargement échoue — le moteur retombe alors sur le CPU.
    /// Essaie les périphériques dans l'ordre donné : celui qui pilote
    /// l'affichage peut refuser les allocations de calcul.
    pub fn ouvrir_auto() -> Option<Gpu> {
        for ord in [1, 0] {
            if let Some(g) = Gpu::ouvrir(ord) { return Some(g); }
            eprintln!("[gpu] périphérique {ord} indisponible, essai du suivant");
        }
        None
    }

    pub fn ouvrir(ordinal: c_int) -> Option<Gpu> {
        unsafe {
            let rc = cuInit(0);
            if rc != 0 { eprintln!("{}", erreur(rc, "cuInit")); return None; }
            let mut dev: c_int = 0;
            let rc = cuDeviceGet(&mut dev, ordinal);
            if rc != 0 { eprintln!("{}", erreur(rc, "cuDeviceGet")); return None; }
            // Contexte **créé** plutôt que contexte principal : celui-ci est
            // partagé avec l'affichage et le pilote refuse l'allocation dans
            // certaines configurations (CUDA_ERROR_INVALID_CONTEXT, 201).
            let mut ctx: *mut c_void = std::ptr::null_mut();
            let rc = cuCtxCreate_v2(&mut ctx, 0, dev);
            if rc != 0 {
                eprintln!("{}", erreur(rc, "cuCtxCreate"));
                let rc = cuDevicePrimaryCtxRetain(&mut ctx, dev);
                if rc != 0 { eprintln!("{}", erreur(rc, "contexte")); return None; }
            }
            let rc = cuCtxSetCurrent(ctx);
            if rc != 0 { eprintln!("{}", erreur(rc, "cuCtxSetCurrent")); return None; }

            // Sonde : une allocation minuscule, juste après la création du
            // contexte, avant tout chargement de module.
            // NB : les points d'entrée NON versionnés du pilote (cuMemAlloc,
            // cuMemcpyHtoD…) échouent en CUDA 13 avec
            // CUDA_ERROR_INVALID_CONTEXT (201). Seuls les `_v2` fonctionnent —
            // trouvé en comparant les deux côte à côte.
            let mut temoin: u64 = 0;
            if cuMemAlloc_v2(&mut temoin, 4096) == 0 { cuMemFree_v2(temoin); }
            let mut ptx: Vec<u8> = PTX.as_bytes().to_vec();
            ptx.push(0);
            let mut module: *mut c_void = std::ptr::null_mut();
            let rc = cuModuleLoadData(&mut module, ptx.as_ptr() as *const c_void);
            if rc != 0 {
                eprintln!("{}", erreur(rc, "chargement du PTX"));
                return None;
            }
            let nom = std::ffi::CString::new("tete_q8").unwrap();
            let mut f_tete: *mut c_void = std::ptr::null_mut();
            let rc = cuModuleGetFunction(&mut f_tete, module, nom.as_ptr());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "fonction tete_q8"));
                return None;
            }
            let nom_p = std::ffi::CString::new("proj_q8").unwrap();
            let mut f_proj: *mut c_void = std::ptr::null_mut();
            let rc = cuModuleGetFunction(&mut f_proj, module, nom_p.as_ptr());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "fonction proj_q8"));
                return None;
            }
            let nom_tw = std::ffi::CString::new("tete_q8_warp").unwrap();
            let mut f_tete_warp: *mut c_void = std::ptr::null_mut();
            let rc = cuModuleGetFunction(&mut f_tete_warp, module, nom_tw.as_ptr());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "fonction tete_q8_warp"));
                return None;
            }
            let nom_pw = std::ffi::CString::new("proj_q8_warp").unwrap();
            let mut f_proj_warp: *mut c_void = std::ptr::null_mut();
            let rc = cuModuleGetFunction(&mut f_proj_warp, module, nom_pw.as_ptr());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "fonction proj_q8_warp"));
                return None;
            }
            let nom_mx = std::ffi::CString::new("proj_mxfp4_warp").unwrap();
            let mut f_mxfp4_warp: *mut c_void = std::ptr::null_mut();
            let rc = cuModuleGetFunction(&mut f_mxfp4_warp, module, nom_mx.as_ptr());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "fonction proj_mxfp4_warp"));
                return None;
            }
            let nom_q4k = std::ffi::CString::new("proj_q4k_warp").unwrap();
            let mut f_q4k_warp: *mut c_void = std::ptr::null_mut();
            let rc = cuModuleGetFunction(&mut f_q4k_warp, module, nom_q4k.as_ptr());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "fonction proj_q4k_warp"));
                return None;
            }
            let nom_q6k = std::ffi::CString::new("proj_q6k_warp").unwrap();
            let mut f_q6k_warp: *mut c_void = std::ptr::null_mut();
            let rc = cuModuleGetFunction(&mut f_q6k_warp, module, nom_q6k.as_ptr());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "fonction proj_q6k_warp"));
                return None;
            }
            let nom_p = std::ffi::CString::new("attn_kv_partiels").unwrap();
            let mut f_attn_part: *mut c_void = std::ptr::null_mut();
            let rc = cuModuleGetFunction(&mut f_attn_part, module, nom_p.as_ptr());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "fonction attn_kv_partiels"));
                return None;
            }
            let nom_s = std::ffi::CString::new("attn_scores").unwrap();
            let mut f_attn_scores: *mut c_void = std::ptr::null_mut();
            let rc = cuModuleGetFunction(&mut f_attn_scores, module, nom_s.as_ptr());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "fonction attn_scores"));
                return None;
            }
            let nom_h = std::ffi::CString::new("attn_topk_histo").unwrap();
            let mut f_attn_topk_histo: *mut c_void = std::ptr::null_mut();
            let rc = cuModuleGetFunction(&mut f_attn_topk_histo, module, nom_h.as_ptr());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "fonction attn_topk_histo"));
                return None;
            }
            let nom_tc = std::ffi::CString::new("attn_topk_compte").unwrap();
            let mut f_attn_topk_compte: *mut c_void = std::ptr::null_mut();
            let rc = cuModuleGetFunction(&mut f_attn_topk_compte, module, nom_tc.as_ptr());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "fonction attn_topk_compte"));
                return None;
            }
            let nom_te = std::ffi::CString::new("attn_topk_ecrit").unwrap();
            let mut f_attn_topk_ecrit: *mut c_void = std::ptr::null_mut();
            let rc = cuModuleGetFunction(&mut f_attn_topk_ecrit, module, nom_te.as_ptr());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "fonction attn_topk_ecrit"));
                return None;
            }
            let nom_ts = std::ffi::CString::new("attn_topk_somme").unwrap();
            let mut f_attn_topk_somme: *mut c_void = std::ptr::null_mut();
            let rc = cuModuleGetFunction(&mut f_attn_topk_somme, module, nom_ts.as_ptr());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "fonction attn_topk_somme"));
                return None;
            }
            let nom_tt = std::ffi::CString::new("attn_topk_tout").unwrap();
            let mut f_attn_topk_tout: *mut c_void = std::ptr::null_mut();
            let rc = cuModuleGetFunction(&mut f_attn_topk_tout, module, nom_tt.as_ptr());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "fonction attn_topk_tout"));
                return None;
            }
            let nom_r = std::ffi::CString::new("attn_kv_recombine").unwrap();
            let mut f_attn_recombine: *mut c_void = std::ptr::null_mut();
            let rc = cuModuleGetFunction(&mut f_attn_recombine, module, nom_r.as_ptr());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "fonction attn_kv_recombine"));
                return None;
            }
            let mut libre: usize = 0;
            let mut total: usize = 0;
            extern "C" {
                fn cuMemGetInfo_v2(libre: *mut usize, total: *mut usize) -> c_int;
            }
            cuMemGetInfo_v2(&mut libre, &mut total);
            Some(Gpu { ctx, module, f_tete, f_proj, f_tete_warp, f_proj_warp,
                       f_mxfp4_warp, f_q4k_warp, f_q6k_warp, f_attn_scores,
                       f_attn_topk_histo, f_attn_topk_compte, f_attn_topk_ecrit,
                       f_attn_topk_somme, f_attn_topk_tout,
                       f_attn_part, f_attn_recombine, ordinal,
                       nom: format!("GPU {ordinal}"), memoire_libre: libre })
        }
    }

    /// Réserve la place d'une matrice de tête et y **copie les poids une fois**.
    ///
    /// `blocs` est la tranche du fichier GGUF : les blocs Q8_0 y sont déjà dans
    /// la disposition attendue par le noyau (34 octets : échelle f16 + 32
    /// niveaux), donc la copie est un transfert brut, sans conversion.
    pub fn charger_tete(&self, blocs: &[u8], n_out: usize, _n_in: usize, nb: usize) -> Option<MatriceGpu> {
        // Le contexte courant est **par fil** : on le réinstalle avant chaque
        // opération plutôt que de supposer qu'il l'est resté.
        unsafe {
            cuCtxSetCurrent(self.ctx);
        }
        let octets_poids = n_out.checked_mul(nb)?.checked_mul(34)?;
        if blocs.len() < octets_poids { return None; }
        unsafe {
            let mut poids: u64 = 0;
            let rc = cuMemAlloc_v2(&mut poids, octets_poids);
            if rc != 0 { eprintln!("{}", erreur(rc, "allocation des poids")); return None; }
            let rc = cuMemcpyHtoD_v2(poids, blocs.as_ptr() as *const c_void, octets_poids);
            if rc != 0 { eprintln!("{}", erreur(rc, "copie des poids")); return None; }
            let mut x_dev: u64 = 0;
            cuMemAlloc_v2(&mut x_dev, nb * 32 * 4);
            let mut out_dev: u64 = 0;
            cuMemAlloc_v2(&mut out_dev, n_out * 4);
            Some(MatriceGpu { poids, x_dev, out_dev, n_out, nb, octets_poids })
        }
    }

    /// Copie **une fois** les poids d'une projection sur le GPU.
    pub fn charger_proj(&self, blocs: &[u8], n_out: usize, nb: usize) -> Option<MatriceGpu> {
        cu_ctx(self.ctx);
        self.charger_tete(blocs, n_out, 0, nb)
    }

    /// Réserve une matrice **MXFP4** (17 octets par bloc de 32 poids).
    pub fn charger_mxfp4(&self, blocs: &[u8], n_out: usize, nb: usize) -> Option<MatriceGpu> {
        cu_ctx(self.ctx);
        let octets_poids = n_out.checked_mul(nb)?.checked_mul(17)?;
        if blocs.len() < octets_poids { return None; }
        unsafe {
            let mut poids: u64 = 0;
            if cuMemAlloc_v2(&mut poids, octets_poids) != 0 { return None; }
            if cuMemcpyHtoD_v2(poids, blocs.as_ptr() as *const c_void, octets_poids) != 0 {
                return None;
            }
            let mut x_dev: u64 = 0;
            cuMemAlloc_v2(&mut x_dev, nb * 32 * 4);
            let mut out_dev: u64 = 0;
            cuMemAlloc_v2(&mut out_dev, n_out * 4);
            Some(MatriceGpu { poids, x_dev, out_dev, n_out, nb, octets_poids })
        }
    }

    /// Réserve une matrice **Q4_K** (144 octets par super-bloc de 256 poids).
    pub fn charger_q4k(&self, blocs: &[u8], n_out: usize, nb: usize) -> Option<MatriceGpu> {
        cu_ctx(self.ctx);
        let octets_poids = n_out.checked_mul(nb)?.checked_mul(144)?;
        if blocs.len() < octets_poids { return None; }
        unsafe {
            let mut poids: u64 = 0;
            if cuMemAlloc_v2(&mut poids, octets_poids) != 0 { return None; }
            if cuMemcpyHtoD_v2(poids, blocs.as_ptr() as *const c_void, octets_poids) != 0 {
                return None;
            }
            let mut x_dev: u64 = 0;
            cuMemAlloc_v2(&mut x_dev, nb * 256 * 4);
            let mut out_dev: u64 = 0;
            cuMemAlloc_v2(&mut out_dev, n_out * 4);
            Some(MatriceGpu { poids, x_dev, out_dev, n_out, nb, octets_poids })
        }
    }

    /// Réserve le cache KV d'une couche en VRAM. `None` si la VRAM manque :
    /// le moteur garde alors le cache en RAM, sans erreur.
    pub fn kv_allouer(&self, n_kv: usize, ctx: usize, hd: usize, bits: u32) -> Option<KvGpu> {
        cu_ctx(self.ctx);
        let nb = hd.div_ceil(32).max(1);
        // Première tranche : de quoi couvrir un préremplissage courant. Le
        // reste s'ajoute par doublement, à la demande.
        let mut m = KvGpu { k: 0, v: 0, sk: 0, sv: 0, n_kv, ctx, capacite: 0, hd, nb, bits,
                            scores_dev: 0, scores_cap: 0, histo_dev: 0, histo_cap: 0,
                            prefixes_dev: 0, prefixes_cap: 0, topk: None,
                            octets: 0, q_dev: 0, part_dev: 0, out_dev: 0, sinks_dev: 0,
                            q_cap: 0, part_cap: 0, out_cap: 0, sinks_cap: 0 };
        if !self.kv_assurer(&mut m, ctx.min(2048)) { return None; }
        Some(m)
    }

    /// Garantit `besoin` positions allouées. Double la capacité (et COPIE ce qui
    /// était écrit : le cache est déjà rempli) jusqu'à couvrir la demande.
    pub fn kv_assurer(&self, m: &mut KvGpu, besoin: usize) -> bool {
        cu_ctx(self.ctx);
        if besoin <= m.capacite { return true; }
        // Sans ce garde, `cap` plafonne à `m.ctx` et la boucle de doublement ne
        // termine jamais : un appelant qui demande plus que le contexte déclaré
        // pendait le processus au lieu de recevoir `false`.
        if besoin > m.ctx { return false; }
        let mut cap = m.capacite.max(1);
        while cap < besoin { cap = (cap * 2).min(m.ctx); }
        let pas = match m.bits { 32 => m.hd * 4, 8 => m.hd, 4 => m.hd / 2, _ => return false };
        let donnees = m.n_kv * cap * pas;
        let echelles = if m.bits >= 32 { 0 } else { m.n_kv * cap * m.nb * 4 };
        let total = donnees * 2 + echelles * 2;
        if total > self.memoire_libre { return false; }
        unsafe {
            let (mut k, mut v, mut sk, mut sv) = (0u64, 0u64, 0u64, 0u64);
            if cuMemAlloc_v2(&mut k, donnees) != 0 { return false; }
            if cuMemAlloc_v2(&mut v, donnees) != 0 { cuMemFree_v2(k); return false; }
            // Échec d'allocation des échelles : libérer k, v (et sk) avant de
            // rendre la main. Sans ces libérations, la VRAM déjà réservée
            // sortait de portée — et l'ancien cache restait alloué, donc la
            // consommation DOUBLAIT à chaque tentative (relevé par un relecteur).
            if echelles > 0 {
                if cuMemAlloc_v2(&mut sk, echelles) != 0 {
                    cuMemFree_v2(k); cuMemFree_v2(v); return false;
                }
                if cuMemAlloc_v2(&mut sv, echelles) != 0 {
                    cuMemFree_v2(k); cuMemFree_v2(v); cuMemFree_v2(sk); return false;
                }
            }
            // Recopie de l'ancien contenu : les positions sont contiguës par
            // tête KV, donc chaque tête se recopie d'un bloc.
            // La recopie est la SEULE chose qui sauve le cache déjà écrit lors
            // du doublement : son code de retour ne peut pas être ignoré, sinon
            // un tampon de VRAM non initialisée est publié comme valide.
            if m.capacite > 0 {
                let ancien = m.n_kv * m.capacite * pas;
                let ancien_e = m.n_kv * m.capacite * m.nb * 4;
                let mut recopie = true;
                for kvh in 0..m.n_kv {
                    if cuMemcpyDtoD_v2(k + (kvh * cap * pas) as u64,
                                       m.k + (kvh * m.capacite * pas) as u64,
                                       ancien / m.n_kv) != 0 { recopie = false; }
                    if cuMemcpyDtoD_v2(v + (kvh * cap * pas) as u64,
                                       m.v + (kvh * m.capacite * pas) as u64,
                                       ancien / m.n_kv) != 0 { recopie = false; }
                }
                if echelles > 0 {
                    for kvh in 0..m.n_kv {
                        if cuMemcpyDtoD_v2(sk + (kvh * cap * m.nb * 4) as u64,
                                           m.sk + (kvh * m.capacite * m.nb * 4) as u64,
                                           ancien_e / m.n_kv) != 0 { recopie = false; }
                        if cuMemcpyDtoD_v2(sv + (kvh * cap * m.nb * 4) as u64,
                                           m.sv + (kvh * m.capacite * m.nb * 4) as u64,
                                           ancien_e / m.n_kv) != 0 { recopie = false; }
                    }
                }
                if !recopie {
                    eprintln!("[gpu] recopie du cache KV en échec : l'ancien cache est gardé");
                    cuMemFree_v2(k); cuMemFree_v2(v);
                    if sk != 0 { cuMemFree_v2(sk); }
                    if sv != 0 { cuMemFree_v2(sv); }
                    return false;
                }
                cuMemFree_v2(m.k); cuMemFree_v2(m.v);
                if m.sk != 0 { cuMemFree_v2(m.sk); }
                if m.sv != 0 { cuMemFree_v2(m.sv); }
            }
            m.k = k; m.v = v; m.sk = sk; m.sv = sv;
            m.capacite = cap;
            m.octets = total;
            true
        }
    }

    /// Copie `t` positions consécutives d'une tête KV (les OCTETS du cache CPU,
    /// tels quels) — le cache est contigu en position, donc une seule copie
    /// suffit pour tout un lot : sans cela, un préremplissage de 512 jetons
    /// faisait 24 000 micro-copies et y passait un quart de seconde.
    pub fn kv_ecrire_tranche(&self, m: &mut KvGpu, kvh: usize, pos0: usize, t: usize,
                             k: &[u8], v: &[u8], sk: &[f32], sv: &[f32]) -> bool {
        cu_ctx(self.ctx);
        if kvh >= m.n_kv || t == 0 || pos0 + t > m.ctx { return false; }
        if !self.kv_assurer(m, pos0 + t) { return false; }
        let pas = match m.bits { 32 => m.hd * 4, 8 => m.hd, 4 => m.hd / 2, _ => return false };
        if k.len() < t * pas || v.len() < t * pas { return false; }
        let off = (kvh * m.capacite + pos0) * pas;
        unsafe {
            if cuMemcpyHtoD_v2(m.k + off as u64, k.as_ptr() as *const c_void, t * pas) != 0 {
                return false;
            }
            if cuMemcpyHtoD_v2(m.v + off as u64, v.as_ptr() as *const c_void, t * pas) != 0 {
                return false;
            }
            if m.bits < 32 {
                let offs = (kvh * m.capacite + pos0) * m.nb * 4;
                if !sk.is_empty()
                    && cuMemcpyHtoD_v2(m.sk + offs as u64, sk.as_ptr() as *const c_void,
                                       t * m.nb * 4) != 0 { return false; }
                if !sv.is_empty()
                    && cuMemcpyHtoD_v2(m.sv + offs as u64, sv.as_ptr() as *const c_void,
                                       t * m.nb * 4) != 0 { return false; }
            }
            true
        }
    }

    /// Un seul vecteur (`t = 1`).
    pub fn kv_ecrire(&self, m: &mut KvGpu, kvh: usize, pos: usize,
                     k: &[u8], v: &[u8], sk: &[f32], sv: &[f32]) -> bool {
        self.kv_ecrire_tranche(m, kvh, pos, 1, k, v, sk, sv)
    }

    /// Une passe d'attention sur le KV déporté : `rep` têtes de requête
    /// partageant une tête KV, `n` clés notées. `q` est `n_kv × rep × hd`.
    #[allow(clippy::too_many_arguments)]
    /// **Scores d'attention seuls** (`attn_scores`) : pour chaque tête KV, les
    /// `rep × n` scores `q·k × échelle`, sans softmax ni valeurs. C'est l'entrée
    /// de la sélection top-k (noyau 2 du plan), et ce que le banc compare au CPU.
    ///
    /// `sc` est `[n_kv][rep][n]`, aplati.
    pub fn attn_scores(&self, m: &mut KvGpu, q: &[f32], n: usize, scale: f32,
                       sc: &mut [f32]) -> bool {
        cu_ctx(self.ctx);
        let rep = if m.n_kv == 0 || m.hd == 0 { 0 } else { q.len() / (m.n_kv * m.hd) };
        let hd = m.hd;
        if rep == 0 || rep > 32 || hd % 32 != 0 { return false; }
        // `q` doit être un multiple exact de n_kv × hd : une division tronquée
        // donnerait un `rep` faux, donc un PAS de ligne faux dans le noyau —
        // des scores silencieusement faux.
        if q.len() % (m.n_kv * m.hd) != 0 { return false; }
        if n == 0 || n > m.capacite || sc.len() < m.n_kv * rep * n { return false; }
        let fils = (rep * 32) as c_uint;
        let partage = ((rep * hd + 32 * (hd + 1)) * 4) as c_uint;
        unsafe {
            let mut p_k = m.k;
            let mut p_sk = m.sk;
            let mut p_q = m.q_dev;
            if m.q_cap < q.len() {
                if m.q_dev != 0 { cuMemFree_v2(m.q_dev); }
                m.q_dev = 0;
                if cuMemAlloc_v2(&mut m.q_dev, q.len() * 4) != 0 { return false; }
                m.q_cap = q.len();
                p_q = m.q_dev;
            }
            if cuMemcpyHtoD_v2(p_q, q.as_ptr() as *const c_void, q.len() * 4) != 0 {
                return false;
            }
            let p_sc = m.scores_dev;
            if m.scores_cap < sc.len() {
                if m.scores_dev != 0 { cuMemFree_v2(m.scores_dev); }
                m.scores_dev = 0;
                // Capacité remise à ZÉRO avant l'allocation : si celle-ci
                // échoue, le prochain appel doit réessayer. La laisser à son
                // ancienne valeur faisait passer un pointeur 0 au noyau.
                m.scores_cap = 0;
                if cuMemAlloc_v2(&mut m.scores_dev, sc.len() * 4) != 0 { return false; }
                m.scores_cap = sc.len();
            }
            let mut p_sc = if m.scores_cap >= sc.len() { m.scores_dev } else { p_sc };
            // Le même découpage que le noyau complet : ~256 clés par tranche,
            // plafonné à 128 tranches.
            let nsplit = (n / 256).clamp(1, 128);
            let (n_i, nsplit_i, ctx_i, hd_i, nb_i, rep_i, bits_i) =
                (n as c_int, nsplit as c_int, m.capacite as c_int, hd as c_int,
                 m.nb as c_int, rep as c_int, m.bits as c_int);
            let (mut rep_c, mut bits_c, mut scale_c) = (rep_i, bits_i, scale);
            let mut params: [*mut c_void; 12] = [
                &mut p_k as *mut u64 as *mut c_void,
                &mut p_sk as *mut u64 as *mut c_void,
                &mut p_q as *mut u64 as *mut c_void,
                &mut p_sc as *mut u64 as *mut c_void,
                &n_i as *const c_int as *mut c_void,
                &nsplit_i as *const c_int as *mut c_void,
                &ctx_i as *const c_int as *mut c_void,
                &hd_i as *const c_int as *mut c_void,
                &nb_i as *const c_int as *mut c_void,
                &mut rep_c as *mut c_int as *mut c_void,
                &mut bits_c as *mut c_int as *mut c_void,
                &mut scale_c as *mut f32 as *mut c_void,
            ];
            let rc = cuLaunchKernel(self.f_attn_scores, m.n_kv as c_uint, nsplit as c_uint, 1,
                                    fils, 1, 1, partage, std::ptr::null_mut(),
                                    params.as_mut_ptr(), std::ptr::null_mut());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "lancement attn_scores"));
                return false;
            }
            if cuMemcpyDtoH_v2(sc.as_mut_ptr() as *mut c_void, p_sc, sc.len() * 4) != 0 {
                return false;
            }
        }
        true
    }

    /// **Scores seuls, SANS relecture** : le chemin que le moteur utilisera.
    ///
    /// Le banc relit les scores pour les comparer au CPU ; le moteur, lui, n'en a
    /// pas besoin — la sélection se fait en VRAM. À 262 144 clés la relecture
    /// pèse 14,7 Mo sur le bus PCIe, et 56 Mo à 1 M : la mesurer séparément est
    /// la seule façon de savoir ce que coûtera le chemin réel.
    pub fn attn_scores_sans_relecture(&self, m: &mut KvGpu, q: &[f32], n: usize,
                                      scale: f32) -> bool {
        cu_ctx(self.ctx);
        let rep = if m.n_kv == 0 || m.hd == 0 { 0 } else { q.len() / (m.n_kv * m.hd) };
        let hd = m.hd;
        if rep == 0 || rep > 32 || hd % 32 != 0 { return false; }
        if q.len() % (m.n_kv * m.hd) != 0 { return false; }
        if n == 0 || n > m.capacite { return false; }
        let besoin = m.n_kv * rep * n;
        // Le tampon de scores est le plus gros du dépôt : nh × n × 4 octets PAR
        // COUCHE — 56 Mo à 1 M pour 14 têtes, 9,2 Go pour gpt-oss. Le plan le
        // déclarait « trop » et il n'est budgété nulle part : une allocation qui
        // échoue faisait retomber le top-k sur le CPU (~100× plus lent) sans un
        // mot. Ici il se refuse explicitement, et on le dit.
        if besoin * 4 > self.memoire_libre / 4 {
            eprintln!("[topk] scores refusés : {:.2} Go par couche pour {} têtes × {} clés \
({:.2} Go libres) — repli CPU", (besoin * 4) as f64 / 1e9, m.n_kv * rep, n,
                      self.memoire_libre as f64 / 1e9);
            return false;
        }
        unsafe {
            if m.scores_cap < besoin {
                if m.scores_dev != 0 { cuMemFree_v2(m.scores_dev); }
                m.scores_dev = 0;
                m.scores_cap = 0;
                if cuMemAlloc_v2(&mut m.scores_dev, besoin * 4) != 0 {
                    eprintln!("[topk] allocation des scores impossible : {:.2} Go par couche",
                              (besoin * 4) as f64 / 1e9);
                    return false;
                }
                m.scores_cap = besoin;
            }
            let mut p_k = m.k;
            let mut p_sk = m.sk;
            let mut p_q = m.q_dev;
            if m.q_cap < q.len() {
                if m.q_dev != 0 { cuMemFree_v2(m.q_dev); }
                m.q_dev = 0;
                m.q_cap = 0;
                if cuMemAlloc_v2(&mut m.q_dev, q.len() * 4) != 0 { return false; }
                m.q_cap = q.len();
                p_q = m.q_dev;
            }
            if cuMemcpyHtoD_v2(p_q, q.as_ptr() as *const c_void, q.len() * 4) != 0 {
                return false;
            }
            let mut p_sc = m.scores_dev;
            let nsplit = (n / 256).clamp(1, 128);
            let (n_i, nsplit_i, ctx_i, hd_i, nb_i, rep_i, bits_i) =
                (n as c_int, nsplit as c_int, m.capacite as c_int, hd as c_int,
                 m.nb as c_int, rep as c_int, m.bits as c_int);
            let (mut rep_c, mut bits_c, mut scale_c) = (rep_i, bits_i, scale);
            let mut params: [*mut c_void; 12] = [
                &mut p_k as *mut u64 as *mut c_void,
                &mut p_sk as *mut u64 as *mut c_void,
                &mut p_q as *mut u64 as *mut c_void,
                &mut p_sc as *mut u64 as *mut c_void,
                &n_i as *const c_int as *mut c_void,
                &nsplit_i as *const c_int as *mut c_void,
                &ctx_i as *const c_int as *mut c_void,
                &hd_i as *const c_int as *mut c_void,
                &nb_i as *const c_int as *mut c_void,
                &mut rep_c as *mut c_int as *mut c_void,
                &mut bits_c as *mut c_int as *mut c_void,
                &mut scale_c as *mut f32 as *mut c_void,
            ];
            let rc = cuLaunchKernel(self.f_attn_scores, m.n_kv as c_uint, nsplit as c_uint, 1,
                                    (rep * 32) as c_uint, 1, 1,
                                    ((rep * hd + 32 * (hd + 1)) * 4) as c_uint,
                                    std::ptr::null_mut(), params.as_mut_ptr(),
                                    std::ptr::null_mut());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "lancement attn_scores (sans relecture)"));
                return false;
            }
            // Aucune synchronisation ici : le premier appel qui suit fait une
            // copie DtoH bloquante (histogramme, comptes ou sélection), et
            // l'ordre du flux suffit. Le `cuCtxSynchronize()` qui traînait là
            // contredisait son propre commentaire et coûtait un vidage de
            // pipeline par couche et par jeton (relevé par un relecteur).
        }
        true
    }

    /// **Histogramme d'un octet des scores** (noyau 2a, `docs/plan-gpu-topk.md`).
    ///
    /// Le score f32 est transformé en entier **monotone** (positif : les bits
    /// sont déjà ordonnés ; négatif : on inverse tout), si bien que l'ordre des
    /// entiers est l'ordre des scores. On histogramme alors l'octet `decalage`,
    /// en ne gardant que les scores dont les octets au-dessus valent le préfixe
    /// de leur ligne. C'est la brique des quatre passes du radix select.
    ///
    /// **Contrat** : `m.scores_dev` doit déjà contenir `lignes × n` scores
    /// écrits par [`Gpu::attn_scores`] (même disposition `[ligne][n]`).
    /// `prefixes` porte un u32 par ligne, `hist` reçoit `lignes × 256` compteurs.
    pub fn attn_topk_histo(&self, m: &mut KvGpu, lignes: usize, n: usize,
                           decalage: i32, prefixes: &[u32], hist: &mut [u32]) -> bool {
        cu_ctx(self.ctx);
        if lignes == 0 || n == 0 || hist.len() < lignes * 256 || prefixes.len() < lignes {
            eprintln!("[topk] tampons hôtes trop courts : {lignes} lignes, {n} clés, \
hist {}, préfixes {}", hist.len(), prefixes.len());
            return false;
        }
        if !(0..=24).contains(&decalage) || decalage % 8 != 0 {
            eprintln!("[topk] décalage {decalage} invalide (0, 8, 16 ou 24)");
            return false;
        }
        let besoin = lignes * 256 * 4;
        if m.scores_cap < lignes * n {
            eprintln!("[topk] scores en VRAM : {} < {} — appeler attn_scores d'abord",
                      m.scores_cap, lignes * n);
            return false;
        }
        unsafe {
            if m.histo_cap < besoin {
                if m.histo_dev != 0 { cuMemFree_v2(m.histo_dev); }
                m.histo_dev = 0;
                m.histo_cap = 0;
                let rc = cuMemAlloc_v2(&mut m.histo_dev, besoin);
                if rc != 0 { eprintln!("{}", erreur(rc, "histogrammes en VRAM")); return false; }
                m.histo_cap = besoin;
            }
            // Compteurs à zéro : le noyau ADDITIONNE (il ne peut pas zéroter une
            // case que personne ne visite).
            let rc = cuMemsetD32_v2(m.histo_dev, 0, lignes * 256);
            if rc != 0 { eprintln!("{}", erreur(rc, "remise à zéro des histogrammes")); return false; }
            let besoin_p = lignes * 4;
            if m.prefixes_cap < besoin_p {
                if m.prefixes_dev != 0 { cuMemFree_v2(m.prefixes_dev); }
                m.prefixes_dev = 0;
                m.prefixes_cap = 0;
                let rc = cuMemAlloc_v2(&mut m.prefixes_dev, besoin_p);
                if rc != 0 { eprintln!("{}", erreur(rc, "préfixes en VRAM")); return false; }
                m.prefixes_cap = besoin_p;
            }
            let rc = cuMemcpyHtoD_v2(m.prefixes_dev, prefixes.as_ptr() as *const c_void,
                                     besoin_p);
            if rc != 0 { eprintln!("{}", erreur(rc, "copie des préfixes")); return false; }
            let (n_i, ns_i, dec_i) =
                (n as c_int, ((n / 256).clamp(1, 128)) as c_int, decalage as c_int);
            let mut p_sc = m.scores_dev;
            let mut p_histo = m.histo_dev;
            let mut p_pref = m.prefixes_dev;
            let mut params: [*mut c_void; 6] = [
                &mut p_sc as *mut u64 as *mut c_void,
                &mut p_histo as *mut u64 as *mut c_void,
                &mut p_pref as *mut u64 as *mut c_void,
                &n_i as *const c_int as *mut c_void,
                &ns_i as *const c_int as *mut c_void,
                &dec_i as *const c_int as *mut c_void,
            ];
            let rc = cuLaunchKernel(self.f_attn_topk_histo, lignes as c_uint, ns_i as c_uint, 1,
                                    256, 1, 1, 256 * 4, std::ptr::null_mut(),
                                    params.as_mut_ptr(), std::ptr::null_mut());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "lancement attn_topk_histo"));
                return false;
            }
            let rc = cuMemcpyDtoH_v2(hist.as_mut_ptr() as *mut c_void, m.histo_dev, besoin);
            if rc != 0 { eprintln!("{}", erreur(rc, "relecture des histogrammes")); return false; }
        }
        true
    }

    /// **Collecte des k indices retenus** (noyaux 2b, `docs/plan-gpu-topk.md`).
    ///
    /// `prefixes[l]` est le score k-ième EXACT de la ligne (entier monotone),
    /// rendu par les quatre passes de [`Gpu::attn_topk_histo`], et
    /// `besoin[l] = k − (nombre de scores strictement au-dessus)`. La sortie
    /// contient, pour chaque ligne, les `k` indices **dans l'ordre du noyau** :
    /// d'abord ceux strictement au-dessus du seuil (indices croissants), puis les
    /// premiers égaux au seuil (indices croissants). Ce n'est PAS l'ordre
    /// croissant global, qui entrelace les deux groupes — mais c'est un ordre
    /// fixe et reproductible, et le même départage des ex æquo que le CPU.
    pub fn attn_topk_collecte(&self, m: &mut KvGpu, lignes: usize, n: usize, k: usize,
                              prefixes: &[u32], besoin: &[i32],
                              sortie: &mut [i32]) -> bool {
        cu_ctx(self.ctx);
        const CHUNK: usize = 4096;
        if lignes == 0 || n == 0 || k == 0 || k > n { return false; }
        if prefixes.len() < lignes || besoin.len() < lignes || sortie.len() < lignes * k {
            eprintln!("[topk] tampons hôtes trop courts pour la collecte");
            return false;
        }
        if m.scores_cap < lignes * n { return false; }
        let ntr = n.div_ceil(CHUNK);
        unsafe {
            // (Ré)allocation : les tampons ne grandissent que si un banc plus
            // long arrive — ils ne sont jamais libérés entre deux jetons.
            let t = m.topk.get_or_insert_with(|| TamponsTopk {
                lignes: 0, ntr: 0, k: 0, chunk: CHUNK,
                comptes: 0, cap_comptes: 0, bases: 0, cap_bases: 0,
                meta: 0, cap_meta: 0, sortie: 0, cap_sortie: 0,
            });
            // Le garde est piloté par les CAPACITÉS, pas par le triplet
            // (lignes, tranches, k) : c'est ce qui rend chaque échec
            // auto-réparateur. Avec un drapeau « dimensions déjà vues », un
            // `vram_assurer` qui échouait au milieu du `||` — il libère le
            // tampon et met sa capacité à zéro — laissait les dimensions
            // enregistrées INCHANGÉES : l'appel suivant, plus petit, sautait la
            // réallocation et passait un pointeur 0 au noyau. Trouvé par un
            // relecteur adversarial, sur le chemin d'échec d'allocation.
            let (besoin_c, besoin_b, besoin_m, besoin_s) =
                (2 * lignes * ntr * 4, 2 * lignes * ntr * 4, 3 * lignes * 4, lignes * k * 4);
            if t.cap_comptes < besoin_c || t.cap_bases < besoin_b
                || t.cap_meta < besoin_m || t.cap_sortie < besoin_s
            {
                if !vram_assurer(&mut t.comptes, &mut t.cap_comptes, besoin_c)
                    || !vram_assurer(&mut t.bases, &mut t.cap_bases, besoin_b)
                    || !vram_assurer(&mut t.meta, &mut t.cap_meta, besoin_m)
                    || !vram_assurer(&mut t.sortie, &mut t.cap_sortie, besoin_s)
                {
                    eprintln!("[topk] allocation VRAM de la collecte impossible \
({lignes} lignes, {ntr} tranches, k = {k})");
                    return false;
                }
                t.lignes = lignes; t.ntr = ntr; t.k = k; t.chunk = CHUNK;
            }
            let (p_comptes, p_bases, p_meta, mut p_sortie) =
                (t.comptes, t.bases, t.meta, t.sortie);
            // Métadonnées : préfixes | debut_egaux (= k − besoin) | besoin.
            let mut meta = vec![0i32; 3 * lignes];
            for l in 0..lignes {
                meta[l] = prefixes[l] as i32;
                meta[lignes + l] = (k as i32) - besoin[l];
                meta[2 * lignes + l] = besoin[l];
            }
            if cuMemcpyHtoD_v2(p_meta, meta.as_ptr() as *const c_void, lignes * 4) != 0 {
                return false;
            }
            if cuMemcpyHtoD_v2(p_meta + (lignes * 4) as u64,
                               meta[lignes..].as_ptr() as *const c_void, lignes * 4) != 0 {
                return false;
            }
            if cuMemcpyHtoD_v2(p_meta + (2 * lignes * 4) as u64,
                               meta[2 * lignes..].as_ptr() as *const c_void, lignes * 4) != 0 {
                return false;
            }
            let (n_i, chunk_i, k_i) = (n as c_int, CHUNK as c_int, k as c_int);
            let mut p_sc = m.scores_dev;
            let mut p_pref = p_meta;
            let mut p_cs = p_comptes;
            let mut p_ce = p_comptes + (lignes * ntr * 4) as u64;
            let mut params: [*mut c_void; 6] = [
                &mut p_sc as *mut u64 as *mut c_void,
                &mut p_pref as *mut u64 as *mut c_void,
                &mut p_cs as *mut u64 as *mut c_void,
                &mut p_ce as *mut u64 as *mut c_void,
                &n_i as *const c_int as *mut c_void,
                &chunk_i as *const c_int as *mut c_void,
            ];
            let rc = cuLaunchKernel(self.f_attn_topk_compte, lignes as c_uint, ntr as c_uint, 1,
                                    256, 1, 1, 0, std::ptr::null_mut(),
                                    params.as_mut_ptr(), std::ptr::null_mut());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "lancement attn_topk_compte"));
                return false;
            }
            // Sommes préfixées par ligne, sur l'hôte : ntr × lignes entiers.
            let mut sup = vec![0i32; lignes * ntr];
            let mut eq = vec![0i32; lignes * ntr];
            let octets = lignes * ntr * 4;
            if cuMemcpyDtoH_v2(sup.as_mut_ptr() as *mut c_void, p_comptes, octets) != 0
                || cuMemcpyDtoH_v2(eq.as_mut_ptr() as *mut c_void,
                                   p_comptes + octets as u64, octets) != 0 { return false; }
            let mut bases = vec![0i32; 2 * lignes * ntr];
            for l in 0..lignes {
                let (mut a, mut b) = (0i32, 0i32);
                for c in 0..ntr {
                    bases[l * ntr + c] = a;
                    bases[lignes * ntr + l * ntr + c] = b;
                    a += sup[l * ntr + c];
                    b += eq[l * ntr + c];
                }
                // Invariant : le seuil a été choisi pour que le compte tombe
                // exactement sur k. S'il ne tombe pas, la collecte écrirait
                // ailleurs que dans les k places — on refuse.
                if a != k as i32 - besoin[l] || b < besoin[l] {
                    eprintln!("[topk] ligne {l} : {a} au-dessus et {b} égaux pour besoin {} \
(k = {k}) — collecte refusée", besoin[l]);
                    return false;
                }
            }
            if cuMemcpyHtoD_v2(p_bases, bases.as_ptr() as *const c_void, 2 * octets) != 0 {
                return false;
            }
            let mut p_bs = p_bases;
            let mut p_be = p_bases + (lignes * ntr * 4) as u64;
            let mut p_de = p_meta + (lignes * 4) as u64;
            let mut p_be2 = p_meta + (2 * lignes * 4) as u64;
            let mut params2: [*mut c_void; 10] = [
                &mut p_sc as *mut u64 as *mut c_void,
                &mut p_pref as *mut u64 as *mut c_void,
                &mut p_bs as *mut u64 as *mut c_void,
                &mut p_be as *mut u64 as *mut c_void,
                &mut p_de as *mut u64 as *mut c_void,
                &mut p_be2 as *mut u64 as *mut c_void,
                &mut p_sortie as *mut u64 as *mut c_void,
                &n_i as *const c_int as *mut c_void,
                &chunk_i as *const c_int as *mut c_void,
                &k_i as *const c_int as *mut c_void,
            ];
            let rc = cuLaunchKernel(self.f_attn_topk_ecrit, lignes as c_uint, ntr as c_uint, 1,
                                    256, 1, 1, 0, std::ptr::null_mut(),
                                    params2.as_mut_ptr(), std::ptr::null_mut());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "lancement attn_topk_ecrit"));
                return false;
            }
            let rc = cuMemcpyDtoH_v2(sortie.as_mut_ptr() as *mut c_void, p_sortie,
                                     lignes * k * 4);
            if rc != 0 { eprintln!("{}", erreur(rc, "relecture de la sélection")); return false; }
        }
        true
    }

    /// **Noyau 3 : le softmax sur les k clés retenues, puis la somme pondérée
    /// des valeurs** (`attn_topk_somme`, `docs/plan-gpu-topk.md`).
    ///
    /// Un bloc par ligne (tête KV × tête de requête). Les k indices sont lus
    /// **en VRAM** — ceux qu'`attn_topk_collecte` vient d'y écrire —, donc
    /// aucun aller-retour par l'hôte. Les puits comptent dans le dénominateur,
    /// jamais dans le numérateur.
    ///
    /// `sinks` est indexé par ligne, comme le moteur. `bits` doit valoir 8
    /// (valeurs int8 + échelle par bloc de 32) ou 32 (valeurs f32) ; les
    /// valeurs 4 bits sont refusées plutôt que devinées.
    pub fn attn_topk_somme(&self, m: &mut KvGpu, lignes: usize, n: usize, k: usize,
                           hd: usize, rep: usize, sinks: Option<&[f32]>,
                           out: &mut [f32]) -> bool {
        cu_ctx(self.ctx);
        if lignes == 0 || n == 0 || k == 0 || k > 1024 || hd == 0 || hd > 1024 || rep == 0 {
            eprintln!("[topk] noyau 3 : dimensions refusées — {lignes} lignes, {n} clés, \
k = {k} (plafonné à 1024 : le partagé du noyau tient 2k + 256 flottants), hd = {hd}");
            return false;
        }
        if m.bits != 8 && m.bits != 32 {
            eprintln!("[topk] noyau 3 : valeurs {} bits non gérées (8 ou 32)", m.bits);
            return false;
        }
        if m.scores_cap < lignes * n || out.len() < lignes * hd {
            eprintln!("[topk] noyau 3 : scores ou sortie trop courts");
            return false;
        }
        // Les indices doivent déjà être en VRAM, à la bonne taille : le noyau 3
        // ne collecte pas, il consomme.
        let Some(t) = m.topk.as_ref() else {
            eprintln!("[topk] noyau 3 : aucune sélection en VRAM (appeler attn_topk_collecte)");
            return false;
        };
        if t.cap_sortie < lignes * k * 4 || t.lignes < lignes || t.k < k {
            eprintln!("[topk] noyau 3 : la sélection en VRAM est trop petite \
({} lignes × k = {} demandés)", lignes, k);
            return false;
        }
        let p_sortie = t.sortie;
        // Puits : recopiés dans le tampon déjà prévu par le cache KV.
        let mut p_sinks: u64 = 0;
        if let Some(si) = sinks {
            if si.len() < lignes { return false; }
            let besoin = lignes * 4;
            unsafe {
                if m.sinks_cap < besoin {
                    if m.sinks_dev != 0 { cuMemFree_v2(m.sinks_dev); }
                    m.sinks_dev = 0;
                    m.sinks_cap = 0;
                    if cuMemAlloc_v2(&mut m.sinks_dev, besoin) != 0 { return false; }
                    m.sinks_cap = besoin;
                }
                if cuMemcpyHtoD_v2(m.sinks_dev, si.as_ptr() as *const c_void, besoin) != 0 {
                    return false;
                }
            }
            p_sinks = m.sinks_dev;
        }
        let partage = ((2 * k + 256) * 4) as c_uint;
        if partage as usize > 48 * 1024 {
            eprintln!("[topk] noyau 3 : {partage} octets de partagé demandés (48 ko au plus)");
            return false;
        }
        unsafe {
            let mut p_sc = m.scores_dev;
            let mut p_v = m.v;
            let mut p_vs = m.sv;
            let mut p_idx = p_sortie;
            let mut p_out = 0u64;
            let octets_out = lignes * hd * 4;
            if m.out_cap < octets_out {
                if m.out_dev != 0 { cuMemFree_v2(m.out_dev); }
                m.out_dev = 0;
                m.out_cap = 0;
                if cuMemAlloc_v2(&mut m.out_dev, octets_out) != 0 { return false; }
                m.out_cap = octets_out;
            }
            p_out = m.out_dev;
            let (n_i, ctx_i, hd_i, nb_i, k_i, rep_i, bits_i) =
                (n as c_int, m.capacite as c_int, hd as c_int, m.nb as c_int,
                 k as c_int, rep as c_int, m.bits as c_int);
            let mut params: [*mut c_void; 13] = [
                &mut p_sc as *mut u64 as *mut c_void,
                &mut p_v as *mut u64 as *mut c_void,
                &mut p_vs as *mut u64 as *mut c_void,
                &mut p_idx as *mut u64 as *mut c_void,
                &mut p_sinks as *mut u64 as *mut c_void,
                &mut p_out as *mut u64 as *mut c_void,
                &n_i as *const c_int as *mut c_void,
                &ctx_i as *const c_int as *mut c_void,
                &hd_i as *const c_int as *mut c_void,
                &nb_i as *const c_int as *mut c_void,
                &k_i as *const c_int as *mut c_void,
                &rep_i as *const c_int as *mut c_void,
                &bits_i as *const c_int as *mut c_void,
            ];
            let rc = cuLaunchKernel(self.f_attn_topk_somme, lignes as c_uint, 1, 1,
                                    256, 1, 1, partage, std::ptr::null_mut(),
                                    params.as_mut_ptr(), std::ptr::null_mut());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "lancement attn_topk_somme"));
                return false;
            }
            let rc = cuMemcpyDtoH_v2(out.as_mut_ptr() as *mut c_void, p_out, octets_out);
            if rc != 0 { eprintln!("{}", erreur(rc, "relecture de l'attention")); return false; }
        }
        true
    }

    /// **Le top-k d'une ligne en UN lancement** (noyau 4, `docs/plan-gpu-topk.md`).
    ///
    /// Remplace la chaîne historique (4 passes d'histogramme + comptage +
    /// écriture + somme, soit 8 lancements et 17 transferts par couche et par
    /// jeton) par un seul noyau : descente radix en mémoire partagée, collecte
    /// déterministe des k indices, softmax et somme pondérée des V.
    ///
    /// **Contrat** : `m.scores_dev` doit déjà contenir `lignes × n` scores
    /// (appeler [`Gpu::attn_scores_sans_relecture`] juste avant — 1 lancement).
    /// `k ≤ 1024`, valeurs 8 ou 32 bits, `hd ≤ 1024`.
    pub fn attn_topk_tout(&self, m: &mut KvGpu, lignes: usize, n: usize, k: usize,
                          hd: usize, rep: usize, sinks: Option<&[f32]>,
                          out: &mut [f32]) -> bool {
        cu_ctx(self.ctx);
        if lignes == 0 || n == 0 || k == 0 || k > 1024 || hd == 0 || hd > 1024 || rep == 0 {
            eprintln!("[topk] noyau 4 : dimensions refusées — {lignes} lignes, {n} clés, \
k = {k} (≤ 1024), hd = {hd}");
            return false;
        }
        // `k > n` : la descente épuiserait les 256 seaux sans jamais atteindre k,
        // la collecte ne remplirait que n places et le filet refuserait APRÈS un
        // lancement complet — et avant lui, la somme lisait des indices non
        // initialisés. La collecte de la chaîne refuse déjà ce cas ; le noyau
        // fusionné doit le refuser aussi.
        if k > n {
            eprintln!("[topk] noyau 4 : k = {k} > n = {n} — sélection impossible");
            return false;
        }
        // Les comptages de la collecte passent par des `float` (réductions en
        // partagé) : exacts tant que n < 2^24.
        if n >= (1 << 24) {
            eprintln!("[topk] noyau 4 : n = {n} ≥ 2^24 — les comptages en float ne sont plus \
exacts");
            return false;
        }
        if m.bits != 8 && m.bits != 32 {
            eprintln!("[topk] noyau 4 : valeurs {} bits non gérées (8 ou 32)", m.bits);
            return false;
        }
        if m.scores_cap < lignes * n || out.len() < lignes * hd || n > m.capacite {
            eprintln!("[topk] noyau 4 : scores, sortie ou capacité KV trop courts");
            return false;
        }
        let fils = 1024usize;
        // 256 compteurs + k indices + k poids, puis 2 réductions (le tableau de
        // clés « réservé » a été retiré : il ne servait à rien).
        let partage = (256 + 2 * k) * 4 + 2 * fils * 4;
        if partage > 48 * 1024 {
            eprintln!("[topk] noyau 4 : {partage} octets de partagé demandés (48 ko au plus)");
            return false;
        }
        let mut p_sinks: u64 = 0;
        if let Some(si) = sinks {
            if si.len() < lignes { return false; }
            unsafe {
                if !vram_assurer(&mut m.sinks_dev, &mut m.sinks_cap, lignes * 4) { return false; }
                if cuMemcpyHtoD_v2(m.sinks_dev, si.as_ptr() as *const c_void, lignes * 4) != 0 {
                    return false;
                }
            }
            p_sinks = m.sinks_dev;
        }
        unsafe {
            if !vram_assurer(&mut m.out_dev, &mut m.out_cap, lignes * hd * 4) { return false; }
            let mut p_sc = m.scores_dev;
            let mut p_v = m.v;
            let mut p_vs = m.sv;
            let mut p_out = m.out_dev;
            let (n_i, ctx_i, hd_i, nb_i, k_i, rep_i, bits_i) =
                (n as c_int, m.capacite as c_int, hd as c_int, m.nb as c_int,
                 k as c_int, rep as c_int, m.bits as c_int);
            // Douze paramètres, exactement ceux du noyau (un tableau plus long
            // serait sans effet mais trompeur — un paramètre en trop ne se voit
            // qu'à la relecture).
            let mut params: [*mut c_void; 12] = [
                &mut p_sc as *mut u64 as *mut c_void,
                &mut p_v as *mut u64 as *mut c_void,
                &mut p_vs as *mut u64 as *mut c_void,
                &mut p_sinks as *mut u64 as *mut c_void,
                &mut p_out as *mut u64 as *mut c_void,
                &n_i as *const c_int as *mut c_void,
                &ctx_i as *const c_int as *mut c_void,
                &hd_i as *const c_int as *mut c_void,
                &nb_i as *const c_int as *mut c_void,
                &k_i as *const c_int as *mut c_void,
                &rep_i as *const c_int as *mut c_void,
                &bits_i as *const c_int as *mut c_void,
            ];
            let rc = cuLaunchKernel(self.f_attn_topk_tout, lignes as c_uint, 1, 1,
                                    fils as c_uint, 1, 1, partage as c_uint,
                                    std::ptr::null_mut(), params.as_mut_ptr(),
                                    std::ptr::null_mut());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "lancement attn_topk_tout"));
                return false;
            }
            let rc = cuMemcpyDtoH_v2(out.as_mut_ptr() as *mut c_void, p_out, lignes * hd * 4);
            if rc != 0 { eprintln!("{}", erreur(rc, "relecture du noyau 4")); return false; }
        }
        // Contrôle de la sortie : le noyau 4 écrit un NaN si sa collecte n'a pas
        // rempli les k places. Une sortie non finie est refusée plutôt que
        // publiée — c'est le seul filet possible, les indices ne quittant plus la
        // VRAM.
        if let Some(pos) = out.iter().position(|v| !v.is_finite()) {
            eprintln!("[topk] noyau 4 : sortie non finie à l'indice {pos} — collecte incomplète, \
repli CPU");
            return false;
        }
        true
    }

    pub fn attn_kv(&self, m: &mut KvGpu, q: &[f32], n: usize, scale: f32,
                   sinks: Option<&[f32]>, nsplit: usize,
                   part: &mut [f32], out: &mut [f32]) -> bool {
        cu_ctx(self.ctx);
        let rep = if m.n_kv == 0 { 0 } else { q.len() / (m.n_kv * m.hd) };
        let hd = m.hd;
        if rep == 0 || rep > 32 || hd % 32 != 0 || hd / 32 > 4 { return false; }
        if n == 0 || n > m.ctx { return false; }
        if out.len() < m.n_kv * rep * hd { return false; }
        // un partiel par (tranche, tête KV, tête de requête)
        if part.len() < nsplit * m.n_kv * rep * (hd + 2) { return false; }
        let fils = (rep * 32) as c_uint;
        let partage = ((rep * hd + 32 * (hd + 1) + 32 * hd + rep * 32) * 4) as c_uint;
        unsafe {
            let mut p_k = m.k;
            let mut p_v = m.v;
            let mut p_sk = m.sk;
            let mut p_sv = m.sv;
            if m.q_cap < q.len() {
                if m.q_dev != 0 { cuMemFree_v2(m.q_dev); }
                m.q_dev = 0;
                if cuMemAlloc_v2(&mut m.q_dev, q.len() * 4) != 0 { return false; }
                m.q_cap = q.len();
            }
            let mut p_q = m.q_dev;
            if cuMemcpyHtoD_v2(p_q, q.as_ptr() as *const c_void, q.len() * 4) != 0 {
                return false;
            }
            if m.part_cap < part.len() {
                if m.part_dev != 0 { cuMemFree_v2(m.part_dev); }
                m.part_dev = 0;
                if cuMemAlloc_v2(&mut m.part_dev, part.len() * 4) != 0 { return false; }
                m.part_cap = part.len();
            }
            let mut p_part = m.part_dev;
            // `ctx` passé au noyau = la capacité ALLOUÉE : c'est le pas entre
            // deux têtes KV dans la VRAM, pas la longueur logique.
            let (n_i, nsplit_i, ctx_i, hd_i, nb_i, rep_i, bits_i) =
                (n as c_int, nsplit as c_int, m.capacite as c_int, hd as c_int,
                 m.nb as c_int, rep as c_int, m.bits as c_int);
            let (mut rep_c, mut bits_c, mut scale_c) = (rep_i, bits_i, scale);
            // treize paramètres : les six premiers sont des adresses, les
            // suivants les tailles, et les trois derniers `rep`, `bits`, `scale`.
            let mut params2: [*mut c_void; 14] = [
                &mut p_k as *mut u64 as *mut c_void,
                &mut p_sk as *mut u64 as *mut c_void,
                &mut p_v as *mut u64 as *mut c_void,
                &mut p_sv as *mut u64 as *mut c_void,
                &mut p_q as *mut u64 as *mut c_void,
                &mut p_part as *mut u64 as *mut c_void,
                &n_i as *const c_int as *mut c_void,
                &nsplit_i as *const c_int as *mut c_void,
                &ctx_i as *const c_int as *mut c_void,
                &hd_i as *const c_int as *mut c_void,
                &nb_i as *const c_int as *mut c_void,
                &mut rep_c as *mut c_int as *mut c_void,
                &mut bits_c as *mut c_int as *mut c_void,
                &mut scale_c as *mut f32 as *mut c_void,
            ];
            let rc = cuLaunchKernel(self.f_attn_part, m.n_kv as c_uint, nsplit as c_uint, 1,
                                    fils, 1, 1, partage, std::ptr::null_mut(),
                                    params2.as_mut_ptr(), std::ptr::null_mut());
            if rc != 0 {
                eprintln!("{}", erreur(rc, "lancement attn_kv_partiels"));
                return false;
            }
            let mut p_sinks = m.sinks_dev;
            if let Some(s) = sinks {
                // `sinks_cap` compte des OCTETS, ici comme dans `attn_topk_somme`.
                // Le compter en ÉLÉMENTS dans cette fonction et en OCTETS dans
                // l'autre marchait par coïncidence (facteur 4 exactement) : après
                // un échec d'allocation, un pointeur 0 passait pour valide et le
                // puits était silencieusement ignoré. Relevé par un relecteur.
                if !vram_assurer(&mut m.sinks_dev, &mut m.sinks_cap, s.len() * 4) {
                    return false;
                }
                p_sinks = m.sinks_dev;
                if cuMemcpyHtoD_v2(p_sinks, s.as_ptr() as *const c_void, s.len() * 4) != 0 {
                    return false;
                }
            }
            // Même unité que partout : des octets.
            if !vram_assurer(&mut m.out_dev, &mut m.out_cap, out.len() * 4) { return false; }
            let mut p_out = m.out_dev;
            // six paramètres : le noyau de recombinaison a besoin de `rep`
            // (l'oublier faisait lire une valeur au hasard et écrivait hors du
            // tampon de sortie — plantage immédiat).
            let mut params3: [*mut c_void; 6] = [
                &mut p_part as *mut u64 as *mut c_void,
                &mut p_sinks as *mut u64 as *mut c_void,
                &mut p_out as *mut u64 as *mut c_void,
                &nsplit_i as *const c_int as *mut c_void,
                &hd_i as *const c_int as *mut c_void,
                &mut rep_c as *mut c_int as *mut c_void,
            ];
            let rc = cuLaunchKernel(self.f_attn_recombine, m.n_kv as c_uint, 1, 1,
                                    fils, 1, 1, 0, std::ptr::null_mut(),
                                    params3.as_mut_ptr(), std::ptr::null_mut());
            let ok = rc == 0 && cuCtxSynchronize() == 0;
            if ok {
                cuMemcpyDtoH_v2(out.as_mut_ptr() as *mut c_void, p_out, out.len() * 4);
            } else if rc != 0 {
                eprintln!("{}", erreur(rc, "lancement attn_kv_recombine"));
            }
            ok
        }
    }

    /// Réserve une matrice Q6_K (210 octets par super-bloc de 256 poids).
    /// Aucune conversion : le fichier est déjà dans la disposition du noyau.
    pub fn charger_q6k(&self, blocs: &[u8], n_out: usize, nb: usize) -> Option<MatriceGpu> {
        cu_ctx(self.ctx);
        let octets_poids = n_out.checked_mul(nb)?.checked_mul(210)?;
        if blocs.len() < octets_poids { return None; }
        unsafe {
            let mut poids: u64 = 0;
            if cuMemAlloc_v2(&mut poids, octets_poids) != 0 { return None; }
            if cuMemcpyHtoD_v2(poids, blocs.as_ptr() as *const c_void, octets_poids) != 0 {
                return None;
            }
            let mut x_dev: u64 = 0;
            cuMemAlloc_v2(&mut x_dev, nb * 256 * 4);
            let mut out_dev: u64 = 0;
            cuMemAlloc_v2(&mut out_dev, n_out * 4);
            Some(MatriceGpu { poids, x_dev, out_dev, n_out, nb, octets_poids })
        }
    }

    /// Une passe Q6_K : une warp par ligne, super-blocs partagés entre les fils.
    pub fn proj_q6k(&self, m: &MatriceGpu, x: &[i32], sx: f32) -> Option<Vec<f32>> {
        cu_ctx(self.ctx);
        let n_in = m.nb * 256;
        if x.len() < n_in { return None; }
        unsafe {
            if cuMemcpyHtoD_v2(m.x_dev, x.as_ptr() as *const c_void, n_in * 4) != 0 { return None; }
            let mut p_poids = m.poids;
            let mut p_x = m.x_dev;
            let mut p_out = m.out_dev;
            let n_out = m.n_out as c_int;
            let nb = m.nb as c_int;
            let mut params: [*mut c_void; 6] = [
                &mut p_poids as *mut u64 as *mut c_void,
                &mut p_x as *mut u64 as *mut c_void,
                &mut p_out as *mut u64 as *mut c_void,
                &n_out as *const c_int as *mut c_void,
                &nb as *const c_int as *mut c_void,
                &sx as *const f32 as *mut c_void,
            ];
            let fils: c_uint = 256;
            let blocs = ((m.n_out as c_uint) + (fils / 32) - 1) / (fils / 32);
            let partage = (n_in * 4) as c_uint;
            let rc = cuLaunchKernel(self.f_q6k_warp, blocs.min(65535), 1, 1, fils, 1, 1,
                                    partage, std::ptr::null_mut(),
                                    params.as_mut_ptr(), std::ptr::null_mut());
            if rc != 0 { eprintln!("{}", erreur(rc, "lancement proj_q6k_warp")); return None; }
            if cuCtxSynchronize() != 0 { return None; }
            let mut out = vec![0f32; m.n_out];
            if cuMemcpyDtoH_v2(out.as_mut_ptr() as *mut c_void, m.out_dev, m.n_out * 4) != 0 {
                return None;
            }
            Some(out)
        }
    }

    /// Une passe Q4_K : une warp par ligne, super-blocs partagés entre les fils.
    pub fn proj_q4k(&self, m: &MatriceGpu, x: &[i32], sx: f32) -> Option<Vec<f32>> {
        cu_ctx(self.ctx);
        let n_in = m.nb * 256;
        if x.len() < n_in { return None; }
        unsafe {
            if cuMemcpyHtoD_v2(m.x_dev, x.as_ptr() as *const c_void, n_in * 4) != 0 { return None; }
            let mut p_poids = m.poids;
            let mut p_x = m.x_dev;
            let mut p_out = m.out_dev;
            let n_out = m.n_out as c_int;
            let nb = m.nb as c_int;
            let mut params: [*mut c_void; 6] = [
                &mut p_poids as *mut u64 as *mut c_void,
                &mut p_x as *mut u64 as *mut c_void,
                &mut p_out as *mut u64 as *mut c_void,
                &n_out as *const c_int as *mut c_void,
                &nb as *const c_int as *mut c_void,
                &sx as *const f32 as *mut c_void,
            ];
            let fils: c_uint = 256;
            let blocs = ((m.n_out as c_uint) + (fils / 32) - 1) / (fils / 32);
            let partage = (n_in * 4) as c_uint;
            let rc = cuLaunchKernel(self.f_q4k_warp, blocs.min(65535), 1, 1, fils, 1, 1,
                                    partage, std::ptr::null_mut(),
                                    params.as_mut_ptr(), std::ptr::null_mut());
            if rc != 0 { eprintln!("{}", erreur(rc, "lancement proj_q4k_warp")); return None; }
            if cuCtxSynchronize() != 0 { return None; }
            let mut out = vec![0f32; m.n_out];
            if cuMemcpyDtoH_v2(out.as_mut_ptr() as *mut c_void, m.out_dev, m.n_out * 4) != 0 {
                return None;
            }
            Some(out)
        }
    }

    /// Une passe MXFP4 (experts de gpt-oss) : une warp par ligne.
    pub fn proj_mxfp4(&self, m: &MatriceGpu, x: &[i32], sx: f32) -> Option<Vec<f32>> {
        cu_ctx(self.ctx);
        let n_in = m.nb * 32;
        if x.len() < n_in { return None; }
        unsafe {
            if cuMemcpyHtoD_v2(m.x_dev, x.as_ptr() as *const c_void, n_in * 4) != 0 { return None; }
            let mut p_poids = m.poids;
            let mut p_x = m.x_dev;
            let mut p_out = m.out_dev;
            let n_out = m.n_out as c_int;
            let nb = m.nb as c_int;
            let mut params: [*mut c_void; 6] = [
                &mut p_poids as *mut u64 as *mut c_void,
                &mut p_x as *mut u64 as *mut c_void,
                &mut p_out as *mut u64 as *mut c_void,
                &n_out as *const c_int as *mut c_void,
                &nb as *const c_int as *mut c_void,
                &sx as *const f32 as *mut c_void,
            ];
            let fils: c_uint = 256;
            let blocs = ((m.n_out as c_uint) + (fils / 32) - 1) / (fils / 32);
            let partage = (n_in * 4) as c_uint;
            let rc = cuLaunchKernel(self.f_mxfp4_warp, blocs.min(65535), 1, 1, fils, 1, 1,
                                    partage, std::ptr::null_mut(),
                                    params.as_mut_ptr(), std::ptr::null_mut());
            if rc != 0 { eprintln!("{}", erreur(rc, "lancement proj_mxfp4_warp")); return None; }
            if cuCtxSynchronize() != 0 { return None; }
            let mut out = vec![0f32; m.n_out];
            if cuMemcpyDtoH_v2(out.as_mut_ptr() as *mut c_void, m.out_dev, m.n_out * 4) != 0 {
                return None;
            }
            Some(out)
        }
    }

    /// Une passe de projection : le facteur d'échelle d'activation est appliqué
    /// par le noyau, côté GPU.
    pub fn proj(&self, m: &MatriceGpu, x: &[i32], sx: f32) -> Option<Vec<f32>> {
        cu_ctx(self.ctx);
        let n_in = m.nb * 32;
        if x.len() < n_in { return None; }
        unsafe {
            let rc = cuMemcpyHtoD_v2(m.x_dev, x.as_ptr() as *const c_void, n_in * 4);
            if rc != 0 { return None; }
            let mut p_poids = m.poids;
            let mut p_x = m.x_dev;
            let mut p_out = m.out_dev;
            let n_out = m.n_out as c_int;
            let nb = m.nb as c_int;
            let mut params: [*mut c_void; 6] = [
                &mut p_poids as *mut u64 as *mut c_void,
                &mut p_x as *mut u64 as *mut c_void,
                &mut p_out as *mut u64 as *mut c_void,
                &n_out as *const c_int as *mut c_void,
                &nb as *const c_int as *mut c_void,
                &sx as *const f32 as *mut c_void,
            ];
            let fils: c_uint = 256;
            let blocs = ((m.n_out as c_uint) + fils - 1) / fils;
            let rc = cuLaunchKernel(self.f_proj, blocs.min(65535), 1, 1, fils, 1, 1,
                                    (n_in * 4) as c_uint, std::ptr::null_mut(),
                                    params.as_mut_ptr(), std::ptr::null_mut());
            if rc != 0 { eprintln!("{}", erreur(rc, "lancement proj")); return None; }
            let rc = cuCtxSynchronize();
            if rc != 0 { return None; }
            let mut out = vec![0f32; m.n_out];
            let rc = cuMemcpyDtoH_v2(out.as_mut_ptr() as *mut c_void, m.out_dev, m.n_out * 4);
            if rc != 0 { return None; }
            Some(out)
        }
    }

    /// Une passe de tête avec le noyau **une warp par ligne**.
    ///
    /// Le noyau d'origine lisait une ligne par fil : deux fils d'une même warp
    /// tombaient dans des lignes de cache différentes et chaque accès coûtait
    /// une transaction. Ici une warp couvre une ligne, donc ~1 Ko contigu.
    /// La mémoire partagée contient les activations PUIS les 32 accumulateurs
    /// par warp.
    pub fn tete_warp(&self, m: &MatriceGpu, x: &[i32]) -> Option<Vec<f32>> {
        unsafe { cuCtxSetCurrent(self.ctx) };
        let n_in = m.nb * 32;
        if x.len() < n_in { return None; }
        unsafe {
            let rc = cuMemcpyHtoD_v2(m.x_dev, x.as_ptr() as *const c_void, n_in * 4);
            if rc != 0 { return None; }
            let mut p_poids = m.poids;
            let mut p_x = m.x_dev;
            let mut p_out = m.out_dev;
            let n_out = m.n_out as c_int;
            let nb = m.nb as c_int;
            let mut params: [*mut c_void; 5] = [
                &mut p_poids as *mut u64 as *mut c_void,
                &mut p_x as *mut u64 as *mut c_void,
                &mut p_out as *mut u64 as *mut c_void,
                &n_out as *const c_int as *mut c_void,
                &nb as *const c_int as *mut c_void,
            ];
            let fils: c_uint = 256;
            let blocs = ((m.n_out as c_uint) + (fils / 32) - 1) / (fils / 32);
            let partage = (n_in * 4) as c_uint;   // plus de zone de réduction : shuffle
            let rc = cuLaunchKernel(self.f_tete_warp, blocs.min(65535), 1, 1, fils, 1, 1,
                                    partage, std::ptr::null_mut(),
                                    params.as_mut_ptr(), std::ptr::null_mut());
            if rc != 0 { eprintln!("{}", erreur(rc, "lancement tete_q8_warp")); return None; }
            let rc = cuCtxSynchronize();
            if rc != 0 { return None; }
            let mut out = vec![0f32; m.n_out];
            let rc = cuMemcpyDtoH_v2(out.as_mut_ptr() as *mut c_void, m.out_dev, m.n_out * 4);
            if rc != 0 { return None; }
            Some(out)
        }
    }

    /// Une passe de tête : activations → GPU, noyau, résultats → CPU.
    pub fn tete(&self, m: &MatriceGpu, x: &[i32]) -> Option<Vec<f32>> {
        unsafe { cuCtxSetCurrent(self.ctx) };
        let n_in = m.nb * 32;
        if x.len() < n_in { return None; }
        unsafe {
            let rc = cuMemcpyHtoD_v2(m.x_dev, x.as_ptr() as *const c_void, n_in * 4);
            if rc != 0 { eprintln!("{}", erreur(rc, "envoi des activations")); return None; }
            let mut p_poids = m.poids;
            let mut p_x = m.x_dev;
            let mut p_out = m.out_dev;
            let n_out = m.n_out as c_int;
            let nb = m.nb as c_int;
            let mut params: [*mut c_void; 5] = [
                &mut p_poids as *mut u64 as *mut c_void,
                &mut p_x as *mut u64 as *mut c_void,
                &mut p_out as *mut u64 as *mut c_void,
                &n_out as *const c_int as *mut c_void,
                &nb as *const c_int as *mut c_void,
            ];
            let fils: c_uint = 256;
            let blocs = ((m.n_out as c_uint) + fils - 1) / fils;
            let partage = (n_in * 4) as c_uint;
            let rc = cuLaunchKernel(self.f_tete, blocs.min(65535), 1, 1, fils, 1, 1,
                                    partage, std::ptr::null_mut(), params.as_mut_ptr(),
                                    std::ptr::null_mut());
            if rc != 0 { eprintln!("{}", erreur(rc, "lancement")); return None; }
            let rc = cuCtxSynchronize();
            if rc != 0 { eprintln!("{}", erreur(rc, "synchronisation")); return None; }
            let mut out = vec![0f32; m.n_out];
            let rc = cuMemcpyDtoH_v2(out.as_mut_ptr() as *mut c_void, m.out_dev, m.n_out * 4);
            if rc != 0 { eprintln!("{}", erreur(rc, "rapatriement")); return None; }
            Some(out)
        }
    }
}

/// Instance unique du processus. `DRAVE_GPU` active le déport ; sans lui, aucune
/// ressource vidéo n'est touchée et le moteur reste strictement sur CPU.
static INSTANCE: std::sync::OnceLock<Option<Gpu>> = std::sync::OnceLock::new();

/// Le SECOND périphérique, s'il y en a un (deux Quadro sur cette machine). Il
/// sert au KV déporté : la moitié des couches d'un côté, la moitié de l'autre.
static SECOND: std::sync::OnceLock<Option<Gpu>> = std::sync::OnceLock::new();

pub fn second() -> Option<&'static Gpu> {
    SECOND.get_or_init(|| {
        if std::env::var("DRAVE_GPU").is_err() { return None; }
        let premier = instance().map(|g| g.ordinal).unwrap_or(0);
        for ord in 0..4 {
            if ord == premier { continue; }
            if let Some(g) = Gpu::ouvrir(ord) { return Some(g); }
        }
        None
    }).as_ref()
}

static MACHINES: std::sync::OnceLock<Vec<&'static Gpu>> = std::sync::OnceLock::new();

/// Les périphériques disponibles, dans l'ordre — un seul si la seconde carte est
/// absente ou occupée.
pub fn machines() -> &'static [&'static Gpu] {
    MACHINES.get_or_init(|| {
        let mut v: Vec<&'static Gpu> = Vec::new();
        if let Some(a) = instance() { v.push(a); }
        if let Some(b) = second() { v.push(b); }
        v
    })
}

pub fn instance() -> Option<&'static Gpu> {
    INSTANCE.get_or_init(|| {
        if std::env::var("DRAVE_GPU").is_err() { return None; }
        Gpu::ouvrir_auto()
    }).as_ref()
}

unsafe impl Send for Gpu {}
unsafe impl Sync for Gpu {}
unsafe impl Send for MatriceGpu {}
unsafe impl Sync for MatriceGpu {}
