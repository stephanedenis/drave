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
    fn cuLaunchKernel(f: *mut c_void, gx: c_uint, gy: c_uint, gz: c_uint,
                      bx: c_uint, by: c_uint, bz: c_uint, partage: c_uint,
                      flux: *mut c_void, params: *mut *mut c_void,
                      extra: *mut c_void) -> c_int;
    fn cuCtxSynchronize() -> c_int;
    fn cuMemFree_v2(dptr: u64) -> c_int;
    fn cuGetErrorName(code: c_int, nom: *mut *const c_char) -> c_int;
}

/// PTX compilé depuis `gpu/qtrinet_gpu.cu` par clang.
const PTX: &str = include_str!("../gpu/qtrinet_gpu.ptx");

#[inline]
fn cu_ctx(ctx: *mut c_void) {
    unsafe { cuCtxSetCurrent(ctx) };
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

pub struct Gpu {
    ctx: *mut c_void,
    module: *mut c_void,
    f_tete: *mut c_void,
    f_proj: *mut c_void,
    pub nom: String,
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
            let mut libre: usize = 0;
            let mut total: usize = 0;
            extern "C" {
                fn cuMemGetInfo_v2(libre: *mut usize, total: *mut usize) -> c_int;
            }
            cuMemGetInfo_v2(&mut libre, &mut total);
            Some(Gpu { ctx, module, f_tete, f_proj, nom: format!("GPU {ordinal}"), memoire_libre: libre })
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

/// Instance unique du processus. `QT_GPU` active le déport ; sans lui, aucune
/// ressource vidéo n'est touchée et le moteur reste strictement sur CPU.
static INSTANCE: std::sync::OnceLock<Option<Gpu>> = std::sync::OnceLock::new();

pub fn instance() -> Option<&'static Gpu> {
    INSTANCE.get_or_init(|| {
        if std::env::var("QT_GPU").is_err() { return None; }
        Gpu::ouvrir_auto()
    }).as_ref()
}

unsafe impl Send for Gpu {}
unsafe impl Sync for Gpu {}
unsafe impl Send for MatriceGpu {}
unsafe impl Sync for MatriceGpu {}
