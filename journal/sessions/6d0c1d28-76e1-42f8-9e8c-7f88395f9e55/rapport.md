# Session 6d0c1d28 — Tu es relecteur ADVERSARIAL de

| | |
|---|---|
| Identifiant | `6d0c1d28-76e1-42f8-9e8c-7f88395f9e55` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-09-30 20:04 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 31 |
| Appels d'outils | 36 |
| Fichiers touchés | 0 |
| Commandes | 21 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es relecteur ADVERSARIAL de code dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », std seul, noyaux PTX compilés par clang sans en-têtes CUDA). Ton but : TROUVER DES DÉFAUTS RÉELS en LISANT le code. Les bancs de ce dépôt ne les voient presque jamais ; les relectures si (deux relectures aujourd'hui ont trouvé un pointeur 0 après échec d'allocation  … [4747 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es relecteur ADVERSARIAL de code dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Ru … [5027 caractères tronqués]

*36 appels d'outils.* Actions notables :

- bash — Inspect repo state and file sizes
- grep
- read
- bash — Show atomicAddPartage and gpu.rs function index
- bash — Find atomicAddPartage definition
- bash — Show atomicAddPartage and attn_scores kernel
- bash — Show attn_scores output indexing
- bash — Locate bench topk function
- bash — Check commit contents, compiler script, build.rs
- bash — Check PTX canary and vram_assurer
- bash — Check PTX NaN canary and loading path
- bash — Read attn_topk_collecte body
- bash — Inspect kv_allouer and its call sites
- bash — Grep launch-count comments
- … et 10 autres

**Synthèse produite :**

⏵ Revue terminée ; rapport envoyé à l'agent parent.

\## Revue adversariale — noyau fusionné `attn_topk_tout`

**Note de révision** : j'ai commencé sur `8342f17` ; en cours d'audit, `ea1d155` (« Le filet du noyau 4 doit agir AVANT la somme ») a été commis par un autre agent (le `.cu` a changé sous moi à 20:06:56). Les constats sont donc donnés sur l'état **courant**, avec ce que `8342f17` avait de pire. Aucun fichier modifié.

\### 1. BLOQUANT (non corrigé) — course sur `shHisto[0]/[1]` entre deux passes de la descente
- **(a)** `drave-core/gpu/drave_gpu.cu:1013` vs `:1031-1032` :
  ```
  1013:  for (int i = tid; i < 256; i += blockDim.x) shHisto[i] = 0u;
  1027:      shHisto[0] = pref;  1028: shHisto[1] = (unsigned int)dessus;
  1030:  __syncthreads();  1031: pref = shHisto[0];  1032: dessus = (int)shHisto[1];
  1033:  }        // fin du corps : AUCUNE barrière
  ```
- **(b)** La barrière 1030 ordonne écriture→lecture *dans* une passe ; rien ne sépare les lectures 1031-1032 de la remise à zéro de la passe suivante. Les fils 0..255 écrivent, tous lisent → course (UB). **Preuve dans le PTX** : `bar.sync; ld.shared.b32 %r3,[sh]; ld.shared.b32 %r253,[sh+4]; @%p1 bra …; $L__BB14_13: st.shared.b32 [%rd168],0; … bra $L__BB14_13; $L__BB14_14: bar.sync 0;` — la boucle de zéro est bien entre les loads et la barrière suivante.
- **(c)** Un warp relâché tard lit `pref=0, dessus=0` : `monotone()` ne rend jamais 0 pour un flottant normal, donc son `nsup` = toute sa plage (128 à n=131 072). Le balayage gonfle `base_sup` des fils suivants → `shIdx[base_sup+rs] = i;` (l.1066) écrit jusqu'à ~n entiers au-delà des 21 504 octets alloués. Le filet (l.1094) passe **après** : il ne peut pas l'empêcher. Corruption partagée possible d'autres blocs résidents (pas de protection MMU partagée), y compris de `red`/`red2`/`shHisto[2]` — le filet lui-même.
- **(d)** Bloquant (UB + écriture non bornée), manifestation étroite.
- **(e)** `__syncthreads();` après la l.1032 (+ borne `if (base_sup + rs < k)`). Vérifier par `compute-sanitizer --tool racecheck`.

\### 2. Déjà corrigé par `ea1d155` (vérifié, à conserver)
Le NaN-poisen de `8342f17` (`l.1082`) était **écrasé** par la boucle finale (`out[ligne*hd + 0]`, fil 0) : filet mort, face au vrai contrôle hôte de la chaîne (`gpu.rs` ~905). ea1d155 le place avant la somme avec `return` uniforme — correct ; le PTX commis contient bien le correctif. Idem pour la course `m = red[0]` / `red[tid] = somme` (noyaux 3 et 4).

\### 3. Faux résultat silenc
… [1925 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Inspect repo state and file sizes
- **T1** Show atomicAddPartage and gpu.rs function index
- **T1** Find atomicAddPartage definition
- **T1** Show atomicAddPartage and attn_scores kernel
- **T1** Show attn_scores output indexing
- **T1** Locate bench topk function
- **T1** Check commit contents, compiler script, build.rs
- **T1** Check PTX canary and vram_assurer
- **T1** Check PTX NaN canary and loading path
- **T1** Read attn_topk_collecte body
- **T1** Inspect kv_allouer and its call sites
- **T1** Grep launch-count comments
- **T1** List all shared-array uses in kernel 4
- **T1** Check working tree modifications
- **T1** Compare working blob hash vs HEAD blob
- **T1** Show the new commit's diff
- **T1** Verify PTX reflects the fix
- **T1** Trace shared loads/stores and barriers in kernel-4 PTX
- **T1** Show PTX between reads and next barrier
- **T1** Inspect miroir_gpu capacity handling
- **T1** Final citation check

## 4. Mesures et résultats marquants

- **T1** `asm volatile("atom.global.add.u32 %0, [%1], %2;" : "=r"(ancien) : "l"(p), "r"(v) : "memory");`
- **T1** `asm volatile("cvta.to.shared.u64 %0, %1;" : "=l"(adresse) : "l"(p));`
- **T1** `asm volatile("atom.shared.add.u32 %0, [%1], %2;"`
- **T1** `638-    // de 224 fils pour 262 144 clés, 1,2 Go/s à peine). Le découpage est celui du`
- **T1** `quitte la VRAM. Le tampon `nh × n × 4` que le plan déclarait « trop » disparaît.`
- **T1** `| 4 096 | **0,13 ms** | 0,22 ms | 7,19e-7 |`
- **T1** `| 16 384 | **0,18 ms** | 0,43 ms | 9,15e-7 |`
- **T1** `| 65 536 | **0,43 ms** | 0,57 ms | 5,68e-7 |`
- **T1** `| 131 072 | **0,85 ms** | 0,89 ms | 6,36e-7 |`
- **T1** `| 262 144 | 1,58 ms | **1,35 ms** | 7,01e-7 |`
- **T1** `8397-	ld.param.b32 	%r36, [attn_topk_tout_param_7];`
- **T1** `8399-	ld.shared.b32 	%r219, [sh+8];`
- **T1** `8400-	setp.ne.b32 	%p82, %r219, 0;`
- **T1** `8405-	cvt.s64.s32 	%rd110, %r36;`
- **T1** `8406-	mul.lo.s64 	%rd111, %rd110, %rd6;`
- **T1** `8407-	shl.b64 	%rd112, %rd111, 2;`
- **T1** `8408-	add.s64 	%rd24, %rd2, %rd112;`
- **T1** `8412-	setp.ge.s32 	%p83, %r289, %r38;`
- **T1** `8413-	mov.b32 	%r284, 0fF149F2CA;`
- **T1** `117:	ld.shared.b32 	%r3, [sh];`
- **T1** `118:	ld.shared.b32 	%r253, [sh+4];`
- **T1** `195:	ld.shared.b32 	%r5, [sh];`
- **T1** `196:	ld.shared.b32 	%r257, [sh+4];`
- **T1** `273:	ld.shared.b32 	%r7, [sh];`
- **T1** `274:	ld.shared.b32 	%r261, [sh+4];`
- **T1** `351:	ld.shared.b32 	%r9, [sh];`
- **T1** `352:	ld.shared.b32 	%r10, [sh+4];`
- **T1** `sub.s32 	%r52, %r249, %r51;`
- **T1** `ld.shared.b32 	%r3, [sh];`
- **T1** `ld.shared.b32 	%r253, [sh+4];`
- **T1** `add.s64 	%rd168, %rd164, %rd163;`
- **T1** `mov.b32 	%r250, %r289;`
- **T1** `add.s32 	%r250, %r250, %r1;`
- **T1** `add.s64 	%rd168, %rd168, %rd165;`
- **T1** `setp.lt.u32 	%p11, %r250, 256;`
- **T1** `mov.b32 	%r251, %r289;`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : drave-core/gpu/cuda_stub.h:60:unsigned int atomicAddPartage(unsigned int* p, unsigned int v) { drave-core/gpu/drave_gpu.cu:756:            atomicAddPartage(&sh[(cle >> decalage) & 0xFFu], 1u); drave-c
- **T1** : commit 8342f175b9fc93bb7e3bd4a2bf689ab1cb80b903 Author: Stéphane <stephane@localhost> Date:   Wed Sep 30 20:03:47 2026 -0400      Noyau 4 : le top-k complet d'une ligne en UN lancement (8 lancements →

