# Session 6551e4dc — Tu es un relecteur adverse.

| | |
|---|---|
| Identifiant | `6551e4dc-b73d-4df7-8fc4-b8c9fdbb0688` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-01 11:57 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 50 |
| Appels d'outils | 63 |
| Fichiers touchés | 2 |
| Commandes | 46 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es un relecteur adverse. Tu ne modifies AUCUN fichier du dépôt : tu lis, tu vérifies, tu rapportes. Ton travail est de trouver ce qui est FAUX, pas de confirmer ce qui va bien. Tu peux écrire uniquement dans /tmp.  Dépôt : /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence GGUF en Rust, « std seul »). Les deux derniers commits (8f55e4f, b24a2e6) ont introduit : 1. un lecteur GG … [4270 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es un relecteur adverse. Tu ne modifies AUCUN fichier du dépôt : tu lis, tu vérifies, tu rapportes. Ton travail est d … [4550 caractères tronqués]

*63 appels d'outils.* Actions notables :

- bash — Inspect repo layout and file sizes
- bash — Show last two commits stats
- read
- bash — Find raw pointer usages
- bash — Locate Moe and numeros usages
- bash — Find partial-node usages
- bash — Find Gguf ownership holders
- bash — Find Moe::ou callers
- bash — List model.rs top-level items
- bash — Find Gguf usage in main.rs
- bash — Inspect Model::load construction
- bash — Diff of mmap commit in gguf.rs
- bash — Diff of model.rs and clusters.rs
- bash — Find multiple model loads
- … et 37 autres

**Synthèse produite :**

⏵ Rapport final : réponses aux 8 questions, preuves et correctifs.

**Révision auditée** : b24a2e6 (gguf.rs et model.rs inchangés sur disque). Pendant l'audit, HEAD est passé à 6a2dfcb et `clusters.rs` + `README.md` sont modifiés non commités (refactor `gardes_du_milieu`/`ouvrir_sous_ensemble`) : pour `clusters.rs`, ajouter **+26** après la ligne ~150. Aucun fichier du dépôt touché ; tout est dans `/tmp/revue`.

---

**1. mmap utilisé après munmap ? NON, aucun cas atteignable.**
Seule sortie de pointeur nu : `data_ptr` — `gguf.rs:915-918` `Some(self.tbuf(t).as_ptr())` — appelé uniquement par `charger_moe` (`model.rs:161` et `178`). Les `Vue4` (`model.rs:241` `pub base: *const u8`) vivent dans `Moe` → `Layer` → `Model.layers` (`model.rs:938`), et le `Gguf` propriétaire est le même `Model.g` (`model.rs:936`), construit par `Model::load` : `charger_moe(&g, l, cfg.n_expert)` (`model.rs:1673`) puis `Model { g, … }` (`model.rs:1949`). `Gguf`/`Tampon`/`Mappe` ne sont pas `Clone` ; ni `Vue4`, ni `Moe`, ni `Layer`, ni `DenseQ4` n'ont de `Drop` ; aucun `mem::forget`/`Box::leak` dans `src/`. Déplacer `Gguf` ne change pas la valeur du pointeur → sûr.
*Latent seulement* : (a) `Model` déclare `g` en premier, donc `munmap` a lieu avant le drop de `layers`/`head4` qui pointent dedans — sûr aujourd'hui parce qu'aucun `Drop` ne lit les poids ; (b) `Pool` est droppé après `g` et `impl Drop for Pool` (`engine.rs:786-791`) joint les fils ; (c) l'invariant « `g` survit aux pointeurs » n'est pas vérifié par le compilateur. Gravité : cosmétique/latent.

**2. Fuite si `Mappe::ouvrir` échoue, ou si `entete_de` rend `None` après mmap ? NON.**
`bufs` est un local (`gguf.rs:355`) droppé sur tout `?`/`Err` ; `Drop for Mappe` (`gguf.rs:67-71`) fait le `munmap` ; pas de `Clone` donc pas de double `munmap`. `entete_de` → `None` : `buf` n'est pas encore poussé et est droppé avec les précédents. Prémisse en partie fausse : un échec de `Mappe::ouvrir` **n'interrompt pas** l'ouverture — `ouvrir_tampon` (`gguf.rs:109-115`) imprime « mmap refusé … lecture complète » et retombe sur `read_to_end`. Seules les erreurs de lecture remontent.

**3. `Tampon::len` : OUI, correct.** `gguf.rs:91` `(**self).len()` déréférence vers `[u8]` ; `is_empty` (92) cohérent (et mort, `allow(dead_code)` ligne 3). Fichier vide : `Mappe::ouvrir` rend `ptr: null_mut(), len: 0` (`gguf.rs:48`) sans mmap, `Deref` rend `&[]` (`gguf.rs:62`), `Drop` saute `munmap` (`gguf.rs:69`). Vérifié sur un fichier 0 octet → erreur propre
… [5727 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/revue/gen.py` | 1 | 0 |
| `/tmp/revue/shards.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Inspect repo layout and file sizes
- **T1** Show last two commits stats
- **T1** Find raw pointer usages
- **T1** Locate Moe and numeros usages
- **T1** Find partial-node usages
- **T1** Find Gguf ownership holders
- **T1** Find Moe::ou callers
- **T1** List model.rs top-level items
- **T1** Find Gguf usage in main.rs
- **T1** Inspect Model::load construction
- **T1** Diff of mmap commit in gguf.rs
- **T1** Diff of model.rs and clusters.rs
- **T1** Find multiple model loads
- **T1** Find Gguf replacement or drop
- **T1** Inspect run path around Model::load
- **T1** Inspect vision mode model opens
- **T1** Check Drop impls and raw-pointer bench paths
- **T1** Read tail of Model::load
- **T1** Inspect all Gguf::open_auto call sites
- **T1** List available models and binary
- **T1** Search for cluster artifacts and --tensors flag
- **T1** Generate synthetic cluster directories
- **T1** Baseline run on complete synthetic cluster dir
- **T1** Run DRAVE_CLUSTERS case matrix
- **T1** Capture error messages for invalid values
- **T1** Run the release test suite once
- **T1** Create sparse cluster dirs
- **T1** Check documented partial-node semantics
- **T1** Read partial-node documentation
- **T1** Test sparse cluster directories
- **T1** Find all expert-vector index sites
- **T1** Read second Moe::ou call site
- **T1** Investigate missing test source
- **T1** Diff the dirty working tree
- **T1** Read rest of clusters.rs working diff
- **T1** Read gguf test helpers
- **T1** Inspect head tensor borrow path
- **T1** Check Pool Drop and DenseQ4 layout
- **T1** Test zero-length files and mmap toggle
- **T1** Capture zero-length file error message
- … et 6 autres

## 4. Mesures et résultats marquants

- **T1** `// fenêtre est un bloc de 4 × 4 jetons fusionnés, soit 8 × 8 patchs.`
- **T1** `/// Le ViT de Qwen2.5-VL commence par une convolution 14 × 14 sur une image`
- **T1** `/// 28 × 28 (deux patchs par côté, la taille minimale d'une fusion 2 × 2). Cette`
- **T1** `// Image 28 × 28 déterministe : dégradé + carré central, pour que la`
- **T1** `/// n'est plus bornée par la RAM (20 Go/s) mais par la VRAM (≈ 450 Go/s).`
- **T1** `/// cette machine : CPU 14–25 Go/s, PCIe x8 6,5 Go/s, NVLink 25,78 Go/s,`
- **T1** `/// GPU 380 Go/s en lecture locale.`
- **T1** `qwen3moe · 9 fichiers · 8 tenseurs · 0.00 Go de poids · en-têtes lus en 3.280144ms`
- **T1** `aucune             val=''                     dir=ok               rc=0  qwen3moe · 9 fichiers · 8 tenseurs · 0.00 Go de poids · en-têtes lus en 3.396173ms`
- **T1** `sous-ensemble      val='0,3'                  dir=ok               rc=0  qwen3moe · 3 fichiers · 2 tenseurs · 0.00 Go de poids · en-têtes lus en 1.827714ms`
- **T1** `desordre           val='3,0'                  dir=ok               rc=0  qwen3moe · 3 fichiers · 2 tenseurs · 0.00 Go de poids · en-têtes lus en 1.882543ms`
- **T1** `tous               val='0,1,2,3,4,5,6,7'      dir=ok               rc=0  qwen3moe · 9 fichiers · 8 tenseurs · 0.00 Go de poids · en-têtes lus en 3.280571ms`
- **T1** `tous demandes      val='0,1,2,3,4,5,6,7'      dir=manque           rc=0  qwen3moe · 8 fichiers · 7 tenseurs · 0.00 Go de poids · en-têtes lus en 3.048097ms`
- **T1** `sous-ensemble      val='0,3'                  dir=manque           rc=0  qwen3moe · 3 fichiers · 2 tenseurs · 0.00 Go de poids · en-têtes lus en 1.852105ms`
- **T1** `REPRISE.md:437:   ne tient qu'une somme partielle : dénominateur ×45,7, sortie 55× trop petite à`
- **T1** `// repasserait 4,4 Mo sur le bus à chaque jeton.`
- **T1** `qwen3moe · 9 fichiers · 8 tenseurs · 0.00 Go de poids · en-têtes lus en 3.257184ms`
- **T1** `qwen3moe · 9 fichiers · 8 tenseurs · 0.00 Go de poids · en-têtes lus en 3.365872ms`
- **T1** `qwen3moe · 8 fichiers · 7 tenseurs · 0.00 Go de poids · en-têtes lus en 3.006009ms`

