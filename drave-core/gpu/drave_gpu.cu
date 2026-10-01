// Noyaux GPU de Drave.
//
// Principe : les POIDS RESTENT SUR LE GPU. La bande passante est locale
// (380 Go/s mesurés, contre 6,5 Go/s de PCIe x8) ; ne traversent le bus que les
// activations — quelques kilo-octets par jeton. Déplacer les poids à chaque
// jeton serait plus lent que de les lire sur CPU (20 Go/s).
// Aucun en-tête : le noyau se compile en PTX avec clang, puis le pilote le
// compile à la volée. Cela évite le conflit entre les en-têtes glibc récents et
// ceux de CUDA, et rend le noyau indépendant de la boîte à outils.

// Demi-précision → simple, écrit à la main (pas de cuda_fp16.h).
__device__ __forceinline__ float f16_en_f32(unsigned short h) {
    const unsigned int s = (h >> 15) & 1u;
    const unsigned int e = (h >> 10) & 0x1Fu;
    const unsigned int m = h & 0x3FFu;
    unsigned int bits;
    if (e == 0) {
        if (m == 0) { bits = s << 31; }
        else {
            unsigned int mm = m; int ex = -1;
            while ((mm & 0x400u) == 0) { mm <<= 1; ++ex; }
            bits = (s << 31) | ((unsigned int)(127 - 15 - ex) << 23) | ((mm & 0x3FFu) << 13);
        }
    } else if (e == 31) {
        bits = (s << 31) | 0x7F800000u | (m << 13);
    } else {
        bits = (s << 31) | ((e + 127u - 15u) << 23) | (m << 13);
    }
    return __int_as_float((int)bits);
}

extern "C" {

// Tête de sortie Q8_0 : blocs de 34 octets (une échelle f16 + 32 niveaux).
// Le produit scalaire entier par bloc est exact, comme côté CPU : le résultat
// doit être identique au chemin scalaire.
__global__ void tete_q8(const unsigned char* __restrict__ w,
                        const int* __restrict__ x,
                        float* __restrict__ out,
                        int n_out, int nb) {
    extern __shared__ int xs[];
    const int n_in = nb * 32;
    for (int i = threadIdx.x; i < n_in; i += blockDim.x) xs[i] = x[i];
    __syncthreads();
    const int pas = blockDim.x * gridDim.x;
    for (int o = blockIdx.x * blockDim.x + threadIdx.x; o < n_out; o += pas) {
        const unsigned char* p = w + (size_t)o * (size_t)nb * 34u;
        float acc = 0.0f;
        for (int b = 0; b < nb; ++b) {
            const float d = f16_en_f32(*reinterpret_cast<const unsigned short*>(p + b * 34));
            const signed char* q = reinterpret_cast<const signed char*>(p + b * 34 + 2);
            const int* xb = xs + b * 32;
            int s = 0;
            #pragma unroll 8
            for (int j = 0; j < 32; ++j) s += (int)q[j] * xb[j];
            acc += d * (float)s;
        }
        out[o] = acc;
    }
}

// Projection Q8_0 : out[o] = somme sur l'entrée. Même disposition que la tête,
// avec un facteur d'échelle d'activation appliqué au résultat.
__global__ void proj_q8(const unsigned char* __restrict__ w,
                        const int* __restrict__ x,
                        float* __restrict__ out,
                        int n_out, int nb, float sx) {
    extern __shared__ int xs[];
    const int n_in = nb * 32;
    for (int i = threadIdx.x; i < n_in; i += blockDim.x) xs[i] = x[i];
    __syncthreads();
    const int pas = blockDim.x * gridDim.x;
    for (int o = blockIdx.x * blockDim.x + threadIdx.x; o < n_out; o += pas) {
        const unsigned char* p = w + (size_t)o * (size_t)nb * 34u;
        float acc = 0.0f;
        for (int b = 0; b < nb; ++b) {
            const float d = f16_en_f32(*reinterpret_cast<const unsigned short*>(p + b * 34));
            const signed char* q = reinterpret_cast<const signed char*>(p + b * 34 + 2);
            const int* xb = xs + b * 32;
            int s = 0;
            #pragma unroll 8
            for (int j = 0; j < 32; ++j) s += (int)q[j] * xb[j];
            acc += d * (float)s;
        }
        out[o] = acc * sx;
    }
}

// ---------------------------------------------------------------------------
// Réduction de warp par shuffle. `shfl.sync.down` est écrit en PTX en ligne :
// les intrinsèques `__shfl_down_sync` viennent des en-têtes CUDA, absents de
// cette chaîne de compilation.
__device__ __forceinline__ float shfl_bas(float v, int d) {
    float r;
    asm volatile("shfl.sync.down.b32 %0, %1, %2, 0x1f, 0xffffffff;"
                 : "=f"(r) : "f"(v), "r"(d));
    return r;
}

// Réduction « papillon » : `shfl.sync.bfly` laisse le RÉSULTAT COMPLET dans
// TOUTES les voies, là où `shfl.sync.down` ne le met que dans la voie 0. Les
// noyaux de projection s'en moquent (seule la voie 0 écrit), la softmax en ligne
// de l'attention NON : chaque voie a besoin du même maximum et de la même somme
// pour ré-échelonner son accumulateur.
__device__ __forceinline__ float shfl_xor(float v, int d) {
    float r;
    asm volatile("shfl.sync.bfly.b32 %0, %1, %2, 0x1f, 0xffffffff;"
                 : "=f"(r) : "f"(v), "r"(d));
    return r;
}

// Version **une warp par ligne**.
//
// L'ancien noyau lisait une ligne PAR FIL : deux fils d'une même warp lisaient
// des adresses distantes de `nb × 34` octets, donc chaque accès était une
// transaction distincte — mesuré : la tête passait de 23 à 159 ms, et le
// déport n'était pas rentable.
//
// Ici les 32 fils d'une warp travaillent sur la MÊME ligne : le fil `lane`
// traite les blocs `lane, lane+32, …`, et les blocs consécutifs occupent des
// adresses consécutives (34 octets d'écart), donc une warp couvre ~1 Ko
// contigu. La réduction se fait en mémoire partagée (pas de shuffle : aucun
// en-tête CUDA n'est disponible dans cette chaîne de compilation).
__global__ void tete_q8_warp(const unsigned char* __restrict__ w,
                             const int* __restrict__ x,
                             float* __restrict__ out,
                             int n_out, int nb) {
    extern __shared__ int xs[];
    const int n_in = nb * 32;
    const int tid = threadIdx.x;
    const int lane = tid & 31;
    const int warp = tid >> 5;
    const int warp_par_bloc = blockDim.x >> 5;
    for (int i = tid; i < n_in; i += blockDim.x) xs[i] = x[i];
    __syncthreads();
    const int warp_grille = (gridDim.x * blockDim.x) >> 5;
    for (int o = blockIdx.x * warp_par_bloc + warp; o < n_out; o += warp_grille) {
        const unsigned char* p = w + (size_t)o * (size_t)nb * 34u;
        float acc = 0.0f;
        for (int b = lane; b < nb; b += 32) {
            const float d = f16_en_f32(*reinterpret_cast<const unsigned short*>(p + b * 34));
            const signed char* q = reinterpret_cast<const signed char*>(p + b * 34 + 2);
            const int* xb = xs + b * 32;
            int s = 0;
            #pragma unroll 8
            for (int j = 0; j < 32; ++j) s += (int)q[j] * xb[j];
            acc += d * (float)s;
        }
        #pragma unroll
        for (int d = 16; d > 0; d >>= 1) acc += shfl_bas(acc, d);
        if (lane == 0) out[o] = acc;
    }
}

__global__ void proj_q8_warp(const unsigned char* __restrict__ w,
                             const int* __restrict__ x,
                             float* __restrict__ out,
                             int n_out, int nb, float sx) {
    extern __shared__ int xs[];
    const int n_in = nb * 32;
    const int tid = threadIdx.x;
    const int lane = tid & 31;
    const int warp = tid >> 5;
    const int warp_par_bloc = blockDim.x >> 5;
    for (int i = tid; i < n_in; i += blockDim.x) xs[i] = x[i];
    __syncthreads();
    const int warp_grille = (gridDim.x * blockDim.x) >> 5;
    for (int o = blockIdx.x * warp_par_bloc + warp; o < n_out; o += warp_grille) {
        const unsigned char* p = w + (size_t)o * (size_t)nb * 34u;
        float acc = 0.0f;
        for (int b = lane; b < nb; b += 32) {
            const float d = f16_en_f32(*reinterpret_cast<const unsigned short*>(p + b * 34));
            const signed char* q = reinterpret_cast<const signed char*>(p + b * 34 + 2);
            const int* xb = xs + b * 32;
            int s = 0;
            #pragma unroll 8
            for (int j = 0; j < 32; ++j) s += (int)q[j] * xb[j];
            acc += d * (float)s;
        }
        #pragma unroll
        for (int d = 16; d > 0; d >>= 1) acc += shfl_bas(acc, d);
        if (lane == 0) out[o] = acc * sx;
    }
}

// ---------------------------------------------------------------------------
// MXFP4 (gpt-oss) : même structure « une warp par ligne ». Un bloc fait
// 17 octets — un exposant E8M0 puis seize octets de nibbles (les BAS sont les
// poids 0–15, les HAUTS les poids 16–31, comme au CPU) — et la table E2M1 est
// doublée, d'où l'exposant décalé de un.
__device__ __forceinline__ int lut_mxfp4(unsigned int nib) {
    // 0, 1, 2, 3, 4, 6, 8, 12 puis les négatifs : la grille E2M1 doublée.
    const int t[16] = {0, 1, 2, 3, 4, 6, 8, 12, 0, -1, -2, -3, -4, -6, -8, -12};
    return t[nib & 15u];
}

__device__ __forceinline__ float echelle_e8m0(unsigned int e) {
    if (e == 0u)   return 1.1754944e-38f;          // plus petit normal
    if (e == 255u) return 0.0f;
    return __int_as_float((e - 1u) << 23);
}

__global__ void proj_mxfp4_warp(const unsigned char* __restrict__ w,
                                const int* __restrict__ x,
                                float* __restrict__ out,
                                int n_out, int nb, float sx) {
    extern __shared__ int xs[];
    const int n_in = nb * 32;
    const int tid = threadIdx.x;
    const int lane = tid & 31;
    const int warp = tid >> 5;
    const int warp_par_bloc = blockDim.x >> 5;
    for (int i = tid; i < n_in; i += blockDim.x) xs[i] = x[i];
    __syncthreads();
    const int warp_grille = (gridDim.x * blockDim.x) >> 5;
    for (int o = blockIdx.x * warp_par_bloc + warp; o < n_out; o += warp_grille) {
        const unsigned char* base = w + (size_t)o * (size_t)nb * 17u;
        float acc = 0.0f;
        for (int b = lane; b < nb; b += 32) {
            const unsigned char* p = base + (size_t)b * 17u;
            const float d = echelle_e8m0((unsigned int)p[0]);
            const unsigned char* qs = p + 1;
            const int* xb = xs + b * 32;
            int lo = 0, hi = 0;
            #pragma unroll
            for (int j = 0; j < 16; ++j) {
                const unsigned int octet = (unsigned int)qs[j];
                lo += lut_mxfp4(octet & 15u) * xb[j];
                hi += lut_mxfp4(octet >> 4) * xb[16 + j];
            }
            acc += (float)(lo + hi) * d;
        }
        #pragma unroll
        for (int d2 = 16; d2 > 0; d2 >>= 1) acc += shfl_bas(acc, d2);
        if (lane == 0) out[o] = acc * sx;
    }
}

// ---------------------------------------------------------------------------
// Q4_K (toute la famille Qwen en Q4_K_M) : super-blocs de 144 octets — deux
// demi-précisions (échelle et minimum), douze octets d'échelles/minimums
// entassés sur 6 bits, puis 128 octets de nibbles (256 poids).
// Le dépaquetage des 6 bits est celui du CPU, recopié à l'identique.
__device__ __forceinline__ void echelle_min_q4k(const unsigned char* sc, int j,
                                                int* echelle, int* minimum) {
    if (j < 4) {
        *echelle = sc[j] & 63;
        *minimum = sc[j + 4] & 63;
    } else {
        *echelle = (sc[j + 4] & 0x0F) | ((sc[j - 4] >> 6) << 4);
        *minimum = (sc[j + 4] >> 4)        | ((sc[j] >> 6) << 4);
    }
}

__global__ void proj_q4k_warp(const unsigned char* __restrict__ w,
                              const int* __restrict__ x,
                              float* __restrict__ out,
                              int n_out, int nb, float sx) {
    extern __shared__ int xs[];
    const int n_in = nb * 256;
    const int tid = threadIdx.x;
    const int lane = tid & 31;
    const int warp = tid >> 5;
    const int warp_par_bloc = blockDim.x >> 5;
    for (int i = tid; i < n_in; i += blockDim.x) xs[i] = x[i];
    __syncthreads();
    const int warp_grille = (gridDim.x * blockDim.x) >> 5;
    for (int o = blockIdx.x * warp_par_bloc + warp; o < n_out; o += warp_grille) {
        float total = 0.0f;
        for (int sup = lane; sup < nb; sup += 32) {
            const unsigned char* b = w + ((size_t)o * (size_t)nb + (size_t)sup) * 144u;
            const float d = f16_en_f32(*reinterpret_cast<const unsigned short*>(b));
            const float dmin = f16_en_f32(*reinterpret_cast<const unsigned short*>(b + 2));
            const int* xb0 = xs + sup * 256;
            #pragma unroll
            for (int g = 0; g < 4; ++g) {
                #pragma unroll
                for (int demi = 0; demi < 2; ++demi) {
                    int echelle, minimum;
                    echelle_min_q4k(b + 4, 2 * g + demi, &echelle, &minimum);
                    const int* xb = xb0 + g * 64 + demi * 32;
                    int sq = 0, sx_somme = 0;
                    #pragma unroll 8
                    for (int l = 0; l < 32; ++l) {
                        const int octet = (int)b[16 + g * 32 + l];
                        const int q = (demi == 0) ? (octet & 15) : (octet >> 4);
                        sq += q * xb[l];
                        sx_somme += xb[l];
                    }
                    total += d * (float)echelle * (float)sq
                           - dmin * (float)minimum * (float)sx_somme;
                }
            }
        }
        #pragma unroll
        for (int d2 = 16; d2 > 0; d2 >>= 1) total += shfl_bas(total, d2);
        if (lane == 0) out[o] = total * sx;
    }
}

// ---------------------------------------------------------------------------
// Q6_K (têtes liées et quelques tenseurs des mélanges Q4_K_M) : super-blocs de
// 210 octets — 128 octets de nibbles bas, 64 octets portant les DEUX bits de
// poids, seize échelles signées d'un octet (une par groupe de seize poids) et
// une demi-précision. Les deux moitiés de 128 poids ont chacune leurs 64 octets
// de ql, 32 de qh et 8 échelles.
//
// Position des huit groupes d'une moitié, telle que le noyau AVX2 du CPU la
// lit (l'ordre des groupes n'est PAS l'ordre des octets) :
//   k : (bloc de ql, nibble, bloc de qh, décalage des 2 bits)
//   0 : (0, bas,  0, 0)   1 : (1, bas,  1, 0)
//   2 : (2, bas,  0, 2)   3 : (3, bas,  1, 2)
//   4 : (0, haut, 0, 4)   5 : (1, haut, 1, 4)
//   6 : (2, haut, 0, 6)   7 : (3, haut, 1, 6)
__global__ void proj_q6k_warp(const unsigned char* __restrict__ w,
                              const int* __restrict__ x,
                              float* __restrict__ out,
                              int n_out, int nb, float sx) {
    extern __shared__ int xs[];
    const int n_in = nb * 256;
    const int tid = threadIdx.x;
    const int lane = tid & 31;
    const int warp = tid >> 5;
    const int warp_par_bloc = blockDim.x >> 5;
    for (int i = tid; i < n_in; i += blockDim.x) xs[i] = x[i];
    __syncthreads();
    const int warp_grille = (gridDim.x * blockDim.x) >> 5;
    for (int o = blockIdx.x * warp_par_bloc + warp; o < n_out; o += warp_grille) {
        const unsigned char* base = w + (size_t)o * (size_t)nb * 210u;
        float total = 0.0f;
        for (int sup = lane; sup < nb; sup += 32) {
            const unsigned char* p = base + (size_t)sup * 210u;
            const float d = f16_en_f32(*reinterpret_cast<const unsigned short*>(p + 208));
            const int* xb0 = xs + sup * 256;
            #pragma unroll
            for (int moitie = 0; moitie < 2; ++moitie) {
                const unsigned char* ql = p + moitie * 64;
                const unsigned char* qh = p + 128 + moitie * 32;
                const signed char* sc =
                    reinterpret_cast<const signed char*>(p + 192 + moitie * 8);
                const int* xb = xb0 + moitie * 128;
                #pragma unroll
                for (int k = 0; k < 8; ++k) {
                    const int bloc_ql = k & 3;                  // constant après déroulage
                    const int bas = (k < 4) ? 1 : 0;
                    const int bloc_qh = bloc_ql & 1;
                    const int dec = 2 * (bloc_ql >> 1) + (bas ? 0 : 4);
                    const unsigned char* qlb = ql + bloc_ql * 16;
                    const unsigned char* qhb = qh + bloc_qh * 16;
                    const int* xg = xb + k * 16;
                    int sq = 0;
                    #pragma unroll
                    for (int l = 0; l < 16; ++l) {
                        const int octet = (int)qlb[l];
                        const int nib = bas ? (octet & 15) : (octet >> 4);
                        const int q = (nib | ((((int)qhb[l] >> dec) & 3) << 4)) - 32;
                        sq += q * xg[l];
                    }
                    total += d * (float)sc[k] * (float)sq;
                }
            }
        }
        #pragma unroll
        for (int d2 = 16; d2 > 0; d2 >>= 1) total += shfl_bas(total, d2);
        if (lane == 0) out[o] = total * sx;
    }
}

// ---------------------------------------------------------------------------
// ATTENTION À KV DÉPORTÉ (étape E4 du plan 1 M).
//
// Le cache KV d'une couche vit en VRAM ; une passe calcule, pour `rep` têtes de
// requête partageant une même tête KV, la somme pondérée sur `n` clés. Chaque
// élément de K et de V n'est lu qu'UNE fois par tête KV et par passe (tuile de
// 32 clés en mémoire partagée), au lieu d'une fois par tête de requête : c'est
// ce qui rend le décodage à 1 M borné par la bande passante VRAM et non par
// celle de la RAM.
//
// Deux noyaux : le premier découpe les clés en `nsplit` tranches (sans quoi il
// n'y aurait qu'un bloc par tête KV — deux blocs sur 48 SM) et écrit un
// (max, somme, accumulateur) partiel ; le second recombine les tranches et
// applique les puits appris, exactement comme le fait le CPU.
//
// Disposition de la mémoire partagée :
//   shK[k * (hd + 1) + i] : tuile de clés en ligne, rembourrée d'un mot par
//                     ligne. Le rembourrage suffit à rendre la lecture sans
//                     conflit de banque (la voie `l` lit `l*(hd+1)+i`, soit
//                     `l + i` modulo 32 : une banque par voie), et il laisse le
//                     CHARGEMENT vectorisable — en transposé, quatre éléments
//                     consécutifs s'écrivaient dans quatre lignes différentes et
//                     les conversions restaient scalaires ;
//   shV[k * hd + i] : tuile de valeurs, disposition naturelle (les fils lisent
//                     des adresses consécutives) ;
//   shP[w * 32 + k] : poids de la tuile, écrits par la réduction puis relus en
//                     diffusion par l'accumulation.
// ---------------------------------------------------------------------------
// Lit l'élément `i` du vecteur `vec` (index global de (tête KV, position)).
// Les échelles sont PAR VECTEUR et par bloc de 32 : `vec * nb + i / 32`, et non
// un décalage en éléments — s'y tromper multipliait l'indice par `hd/32` et
// donnait des échelles absurdes (écart mesuré : 7e7).
__device__ __forceinline__ float kv_lire(const void* data, const float* scales,
                                         int bits, size_t vec, int i, int hd, int nb) {
    if (bits >= 32) return reinterpret_cast<const float*>(data)[vec * hd + i];
    const float sc = scales[vec * nb + i / 32];
    if (bits == 8) {
        return (float)(signed char)reinterpret_cast<const unsigned char*>(data)[vec * hd + i] * sc;
    }
    const unsigned char o =
        reinterpret_cast<const unsigned char*>(data)[vec * (hd / 2) + i / 2];
    int q = (i % 2 == 0) ? (o & 0x0F) : (o >> 4);
    if (q >= 8) q -= 16;
    return (float)q * sc;
}

__global__ void attn_kv_partiels(const void* __restrict__ kdata,
                                 const float* __restrict__ kscale,
                                 const void* __restrict__ vdata,
                                 const float* __restrict__ vscale,
                                 const float* __restrict__ q,     // [rep][hd]
                                 float* __restrict__ part,        // [nsplit][rep][hd+2]
                                 int n, int nsplit, int ctx, int hd, int nb,
                                 int rep, int bits, float scale) {
    extern __shared__ float sh[];
    float* shQ = sh;                 // rep * hd : la requête ENTIÈRE, partagée
    float* shK = shQ + rep * hd;     // 32 * (hd + 1), tuile de clés rembourrée
    float* shV = shK + 32 * (hd + 1); // 32 * hd
    float* shP = shV + 32 * hd;      // rep * 32
    const int tid = threadIdx.x;
    const int lane = tid & 31;
    const int warp = tid >> 5;
    const int kvh = blockIdx.x;
    const int sp = blockIdx.y;
    const int par_tranche = (n + nsplit - 1) / nsplit;
    const int debut = sp * par_tranche;
    const int fin = min(n, debut + par_tranche);
    const int nq = hd / 32;
    // La requête passe par la mémoire PARTAGÉE : chaque fil note SA clé et a
    // donc besoin des hd composantes entières, alors qu'un registre par fil ne
    // contient que les composantes de sa voie. Les garder en registres
    // multipliait la composante `lane` par tous les éléments de la clé — un
    // résultat plausible et faux (mesuré : écart 4e-1 sur des requêtes
    // aléatoires, et un accord parfait dès que la requête était un vecteur de
    // base, seule configuration où les deux lectures coïncident).
    for (int i = tid; i < rep * hd; i += blockDim.x) {
        shQ[i] = q[kvh * rep * hd + i];
    }
    float acc[4];
    #pragma unroll
    for (int o = 0; o < 4; ++o) acc[o] = 0.0f;
    float M = -1e30f, S = 0.0f;
    __syncthreads();     // la requête partagée est prête
    const size_t basekv = (size_t)kvh * ctx;
    for (int t0 = debut; t0 < fin; t0 += 32) {
        const int reste = min(32, fin - t0);
        // --- chargement coopératif de la tuile (K transposée, V naturelle)
        const int par4 = hd >> 2;              // groupes de 4 éléments
        for (int idx = tid; idx < reste * par4; idx += blockDim.x) {
            const int k = idx / par4, ib = idx % par4;
            const int i = ib << 2;
            const size_t vec = basekv + t0 + k;
            float kv[4], vv[4];
            if (bits == 8) {
                // Quatre octets d'un seul coup (un `unsigned int` : pas d'en-tête
                // CUDA ici, donc pas de `char4`), puis conversion et mise à
                // l'échelle sur les quatre.
                const unsigned int q4 = *reinterpret_cast<const unsigned int*>(
                    reinterpret_cast<const unsigned char*>(kdata) + vec * (size_t)hd + i);
                const unsigned int w4 = *reinterpret_cast<const unsigned int*>(
                    reinterpret_cast<const unsigned char*>(vdata) + vec * (size_t)hd + i);
                const float sk = kscale[vec * nb + (i >> 5)];
                const float sv = vscale[vec * nb + (i >> 5)];
                #pragma unroll
                for (int j = 0; j < 4; ++j) {
                    kv[j] = (float)(signed char)((q4 >> (8 * j)) & 0xFFu) * sk;
                    vv[j] = (float)(signed char)((w4 >> (8 * j)) & 0xFFu) * sv;
                }
            } else if (bits == 4) {
                const unsigned char* pk =
                    reinterpret_cast<const unsigned char*>(kdata) + vec * (size_t)(hd / 2) + (i >> 1);
                const unsigned char* pv =
                    reinterpret_cast<const unsigned char*>(vdata) + vec * (size_t)(hd / 2) + (i >> 1);
                const float sk = kscale[vec * nb + (i >> 5)];
                const float sv = vscale[vec * nb + (i >> 5)];
                #pragma unroll
                for (int j = 0; j < 4; ++j) {
                    int qk = (pk[j >> 1] >> (4 * (j & 1))) & 0x0F;
                    int qv = (pv[j >> 1] >> (4 * (j & 1))) & 0x0F;
                    if (qk >= 8) qk -= 16;
                    if (qv >= 8) qv -= 16;
                    kv[j] = (float)qk * sk;
                    vv[j] = (float)qv * sv;
                }
            } else {
                #pragma unroll
                for (int j = 0; j < 4; ++j) {
                    kv[j] = reinterpret_cast<const float*>(kdata)[vec * hd + i + j];
                    vv[j] = reinterpret_cast<const float*>(vdata)[vec * hd + i + j];
                }
            }
            #pragma unroll
            for (int j = 0; j < 4; ++j) {
                shK[k * (hd + 1) + i + j] = kv[j];
                shV[k * hd + i + j] = vv[j];
            }
        }
        __syncthreads();
        // --- score de la clé `lane` pour la tête `warp`
        float s = -1e30f;
        if (lane < reste) {
            s = 0.0f;
            const float* qw = shQ + warp * hd;
            const float* kl = shK + lane * (hd + 1);
            #pragma unroll 8
            for (int i = 0; i < hd; ++i) s += qw[i] * kl[i];
            s *= scale;      // 1/sqrt(hd) : sans lui, la softmax est trop plate
        }
        // --- maximum et somme de la tuile (réduction par warp)
        float mt = s;
        #pragma unroll
        for (int d = 16; d > 0; d >>= 1) mt = fmaxf(mt, shfl_xor(mt, d));
        const float Mn = fmaxf(M, mt);
        const float r = expf(M - Mn);
        const float p = (lane < reste) ? expf(s - Mn) : 0.0f;
        float st = p;
        #pragma unroll
        for (int d = 16; d > 0; d >>= 1) st += shfl_xor(st, d);
        shP[warp * 32 + lane] = p;
        S = S * r + st;
        #pragma unroll
        for (int o = 0; o < 4; ++o) acc[o] *= r;
        __syncwarp();
        // --- somme pondérée des valeurs : chaque fil porte hd/32 composantes
        #pragma unroll
        for (int k = 0; k < 32; ++k) {
            if (k < reste) {
                const float pj = shP[warp * 32 + k];
                #pragma unroll
                for (int o = 0; o < 4; ++o) {
                    if (o < nq) acc[o] += pj * shV[k * hd + o * 32 + lane];
                }
            }
        }
        M = Mn;
        __syncthreads();
    }
    // Indexé par (tranche, tête KV, tête de requête) : `gridDim.x` est le
    // nombre de têtes KV, et l'oublier faisait écrire tous les blocs de la même
    // tranche au même endroit.
    float* dst = part + (((size_t)sp * gridDim.x + kvh) * rep + warp) * (hd + 2);
    if (lane == 0) {
        dst[0] = M;
        dst[1] = S;
    }
    #pragma unroll
    for (int o = 0; o < 4; ++o) {
        if (o < nq) dst[2 + o * 32 + lane] = acc[o];
    }
}

// Recombine les tranches et applique les puits appris (facultatif).
__global__ void attn_kv_recombine(const float* __restrict__ part,
                                  const float* __restrict__ sinks,
                                  float* __restrict__ out,
                                  int nsplit, int hd, int rep) {
    const int tid = threadIdx.x;
    const int lane = tid & 31;
    const int warp = tid >> 5;
    const int kvh = blockIdx.x;
    float M = -1e30f, S = 0.0f;
    const int nq = hd / 32;
    float acc[4];
    #pragma unroll
    for (int o = 0; o < 4; ++o) acc[o] = 0.0f;
    for (int sp = 0; sp < nsplit; ++sp) {
        const float* p = part + (((size_t)sp * gridDim.x + kvh) * rep + warp) * (hd + 2);
        M = fmaxf(M, p[0]);
    }
    // ⚠️ `warp` est la tête de requête DANS le groupe KV, alors que la sortie
    // est écrite par tête GLOBALE (`out[(kvh * rep + warp) * hd + …]` juste en
    // dessous). Lire `sinks[warp]` donnait à la tête `kvh*rep + w` le puits de la
    // tête `w` : sur gpt-oss (64 têtes de requête, 8 têtes KV, puits allant de
    // -1,95 à +3,38) l'écart atteint 4,65 logit DANS un groupe, soit un facteur
    // 105 sur le terme de drainage du dénominateur. Trouvé par un relecteur
    // adversarial ; le chemin CPU, le noyau 3 du top-k et HF indexent tous par
    // tête globale — seul ce noyau était faux.
    if (sinks != nullptr) M = fmaxf(M, sinks[kvh * rep + warp]);
    for (int sp = 0; sp < nsplit; ++sp) {
        const float* p = part + (((size_t)sp * gridDim.x + kvh) * rep + warp) * (hd + 2);
        const float w = expf(p[0] - M);
        S += p[1] * w;
        #pragma unroll
        for (int o = 0; o < 4; ++o) {
            if (o < nq) acc[o] += p[2 + o * 32 + lane] * w;
        }
    }
    if (sinks != nullptr) S += expf(sinks[kvh * rep + warp] - M);
    const float inv = (S > 0.0f) ? 1.0f / S : 0.0f;
    #pragma unroll
    for (int o = 0; o < 4; ++o) {
        if (o < nq) out[(kvh * rep + warp) * hd + o * 32 + lane] = acc[o] * inv;
    }
}

}  // extern "C"

// ---------------------------------------------------------------------------
// SCORES d'attention, SANS softmax ni valeurs — le premier des trois noyaux du
// top-k (docs/plan-gpu-topk.md). Il reprend la tuile de clés du noyau complet
// (`attn_kv_partiels`) et écrit les scores `rep × n` au lieu de les consommer :
// c'est ce que la sélection (noyau 2) doit lire, et ce que le banc compare à la
// référence CPU.
//
// Pourquoi un noyau séparé plutôt qu'un drapeau dans l'autre : le noyau complet
// calcule les scores PUIS les utilise dans la même boucle, et son état en ligne
// (max, somme) n'a pas de sens sans les valeurs. Séparer coûte une relecture des
// clés (la VRAM est rapide) et rend la sélection testable seule.
//
// q    : [rep][hd] pour UNE tête KV (le décalage est celui de l'appelant)
// sc   : [rep][n] — un score par tête de requête et par clé
// `extern "C"` : sans lui, clang++ MANGELLE le nom (`_Z11attn_scoresPKv…`) et
// `cuModuleGetFunction("attn_scores")` rend CUDA_ERROR_NOT_FOUND — les autres
// noyaux du fichier sont dans le bloc `extern "C"` du haut, celui-ci a été ajouté
// après. Une ligne, et le noyau se trouve.
extern "C" __global__ void attn_scores(const void* __restrict__ kdata,
                            const float* __restrict__ kscale,
                            const float* __restrict__ q,      // [rep][hd]
                            float* __restrict__ sc,           // [n_kv][rep][n]
                            int n, int nsplit, int ctx, int hd, int nb,
                            int rep, int bits, float scale) {
    extern __shared__ float sh[];
    float* shQ = sh;                  // rep * hd
    float* shK = shQ + rep * hd;      // 32 * (hd + 1), tuile rembourrée
    const int tid = threadIdx.x;
    const int lane = tid & 31;
    const int warp = tid >> 5;
    const int kvh = blockIdx.x;
    // Tranches : une grille de `n_kv` blocs laissait le GPU au repos (deux blocs
    // de 224 fils pour 262 144 clés, 1,2 Go/s à peine). Le découpage est celui du
    // noyau d'attention complet.
    const int sp = blockIdx.y;
    const int par_tranche = (n + nsplit - 1) / nsplit;
    const int debut = sp * par_tranche;
    const int fin = min(n, debut + par_tranche);
    for (int i = tid; i < rep * hd; i += blockDim.x) {
        shQ[i] = q[kvh * rep * hd + i];
    }
    __syncthreads();
    const size_t basekv = (size_t)kvh * ctx;
    for (int t0 = debut; t0 < fin; t0 += 32) {
        const int reste = min(32, fin - t0);
        const int par4 = hd >> 2;
        for (int idx = tid; idx < reste * par4; idx += blockDim.x) {
            const int k = idx / par4, ib = idx % par4;
            const int i = ib << 2;
            const size_t vec = basekv + t0 + k;
            float kv[4];
            if (bits == 8) {
                const unsigned int q4 = *reinterpret_cast<const unsigned int*>(
                    reinterpret_cast<const unsigned char*>(kdata) + vec * (size_t)hd + i);
                const float sk = kscale[vec * nb + (i >> 5)];
                #pragma unroll
                for (int j = 0; j < 4; ++j) {
                    kv[j] = (float)(signed char)((q4 >> (8 * j)) & 0xFFu) * sk;
                }
            } else if (bits == 4) {
                const unsigned char* pk =
                    reinterpret_cast<const unsigned char*>(kdata) + vec * (size_t)(hd / 2) + (i >> 1);
                const float sk = kscale[vec * nb + (i >> 5)];
                #pragma unroll
                for (int j = 0; j < 4; ++j) {
                    int qk = (pk[j >> 1] >> (4 * (j & 1))) & 0x0F;
                    if (qk >= 8) qk -= 16;
                    kv[j] = (float)qk * sk;
                }
            } else {
                #pragma unroll
                for (int j = 0; j < 4; ++j) {
                    kv[j] = reinterpret_cast<const float*>(kdata)[vec * hd + i + j];
                }
            }
            #pragma unroll
            for (int j = 0; j < 4; ++j) {
                shK[k * (hd + 1) + i + j] = kv[j];
            }
        }
        __syncthreads();
        if (lane < reste) {
            float s = 0.0f;
            const float* qw = shQ + warp * hd;
            const float* kl = shK + lane * (hd + 1);
            #pragma unroll 8
            for (int i = 0; i < hd; ++i) s += qw[i] * kl[i];
            // L'offset de la TÊTE KV est indispensable : chaque bloc écrit SA
            // tranche de `sc`, et sans lui tous les blocs écrasaient la même
            // (écart relatif 1,24 — c'est le banc qui l'a dit, pas une relecture).
            sc[((size_t)kvh * rep + warp) * n + t0 + lane] = s * scale;
        }
        __syncthreads();   // la tuile partagée va être réécrite au tour suivant
    }
}

// ---------------------------------------------------------------------------
// SÉLECTION top-k, première moitié : l'HISTOGRAMME (noyau 2a). Chaque ligne
// (tête KV × tête de requête) a ses `n` scores ; on veut le k-ième plus grand
// sans trier n éléments. On transforme d'abord chaque score en entier MONOTONE
// (l'astuce classique : pour un f32 positif les bits sont déjà ordonnés, pour un
// négatif on inverse tout), puis on compte les 256 seaux des 8 bits de poids
// fort. L'hôte descend les seaux jusqu'à dépasser k : c'est le seuil, et il est
// exact — c'est le tri radix à deux passes du plan, dont la seconde (la collecte)
// vient après.
// ⚠️ Limite connue du contrat « l'ordre des entiers est l'ordre des scores » :
// elle est vraie pour deux valeurs DISTINCTES, pas pour ±0,0 — `monotone(-0,0)`
// vaut 0x7FFFFFFF et `monotone(+0,0)` vaut 0x80000000, alors que le f32 les
// déclare égaux — ni pour les NaN, rangés par leur bit de signe. Conséquence :
// si le k-ième score est un zéro signé, le départage des ex æquo peut différer
// de celui d'une référence f32. Relevé par un relecteur ; non observé en
// pratique (il faut une clé nulle et une échelle négative pour produire -0,0).
__device__ __forceinline__ unsigned int monotone(float f) {
    // Pas de `__float_as_uint` sans en-têtes CUDA : le reinterpret_cast fait le
    // même travail, et `__builtin_bit_cast` est disponible (voir cuda_stub.h).
    const unsigned int b = *reinterpret_cast<const unsigned int*>(&f);
    return (b & 0x80000000u) ? ~b : (b | 0x80000000u);
}
__device__ __forceinline__ float depuis_monotone(unsigned int u) {
    const unsigned int b = (u & 0x80000000u) ? (u & 0x7FFFFFFFu) : ~u;
    return *reinterpret_cast<const float*>(&b);
}

// Histogramme d'un OCTET du score transformé en entier monotone. Un seul noyau
// sert les quatre passes du radix select : `decalage` dit quel octet (24, 16, 8,
// 0) et `prefixe` les octets DÉJÀ fixés au-dessus. Le filtre s'écrit
// `(cle >> decalage) >> 8 == prefixe` — deux décalages toujours < 32, donc pas de
// décalage par 32 (indéfini en C) quand `decalage == 24`.
extern "C" __global__ void attn_topk_histo(const float* __restrict__ sc,
                                           unsigned int* __restrict__ histo, // [lignes][256]
                                           const unsigned int* __restrict__ prefixes,
                                           int n, int nsplit, int decalage) {
    // Grille : (ligne, tranche) ; histogramme PARTAGÉ par bloc (256 u32 = 1 ko),
    // puis un atomicAdd par seau et par bloc — 256 atomiques au lieu de n.
    __shared__ unsigned int sh[256];
    const int ligne = blockIdx.x;
    const int sp = blockIdx.y;
    // Un préfixe PAR LIGNE : chaque tête de requête a son propre k-ième score,
    // donc sa propre descente. Un scalaire obligerait à relancer le noyau une
    // fois par tête.
    const unsigned int prefixe = prefixes[ligne];
    for (int i = threadIdx.x; i < 256; i += blockDim.x) sh[i] = 0u;
    __syncthreads();
    const int par = (n + nsplit - 1) / nsplit;
    const int debut = sp * par;
    const int fin = min(n, debut + par);
    const float* row = sc + (size_t)ligne * n;
    for (int i = debut + threadIdx.x; i < fin; i += blockDim.x) {
        const unsigned int cle = monotone(row[i]);
        if (((cle >> decalage) >> 8) == prefixe)
            atomicAddPartage(&sh[(cle >> decalage) & 0xFFu], 1u);
    }
    __syncthreads();
    for (int i = threadIdx.x; i < 256; i += blockDim.x) {
        if (sh[i]) atomicAdd(&histo[(size_t)ligne * 256 + i], sh[i]);
    }
}

// ---------------------------------------------------------------------------
// Noyaux 2b : la COLLECTE des k indices retenus.
//
// Après les quatre passes d'histogramme, chaque ligne connaît le score k-ième
// EXACT (`prefixe`) et le nombre de scores strictement au-dessus. Il reste à
// écrire les indices : tous ceux strictement au-dessus, puis, parmi les égaux au
// seuil, les premiers par ORDRE D'INDEX — c'est ce départage qui rend le
// résultat reproductible, et il doit être le même que côté CPU.
//
// Deux temps, parce qu'un bloc ne peut pas connaître sa place globale avant que
// les blocs précédents aient compté : `attn_topk_compte` écrit les comptes par
// (ligne, tranche), l'hôte en fait la somme préfixée, `attn_topk_ecrit` écrit
// les indices. Chaque fil possède une plage CONTIGUË de la tranche : les
// écritures d'un fil sont donc déjà dans l'ordre des indices, et les rangs
// partent du bon pied. Une plage entrelacée (i += 256) casserait cet ordre.
// ---------------------------------------------------------------------------

extern "C" __global__ void attn_topk_compte(const float* __restrict__ sc,
                                            const unsigned int* __restrict__ prefixes,
                                            int* __restrict__ compte_sup, // [lignes][ntr]
                                            int* __restrict__ compte_eq,
                                            int n, int chunk) {
    __shared__ int cs[256];
    __shared__ int ce[256];
    const int ligne = blockIdx.x;
    const int tr = blockIdx.y;
    const int deb = tr * chunk;
    const int fin = min(n, deb + chunk);
    const unsigned int pref = prefixes[ligne];
    const float* row = sc + (size_t)ligne * n;
    const int t = threadIdx.x;
    const int par = (fin - deb + 255) / 256;
    const int d0 = deb + t * par;
    const int d1 = min(fin, d0 + par);
    int s = 0, e = 0;
    for (int i = d0; i < d1; i++) {
        const unsigned int cle = monotone(row[i]);
        if (cle > pref) s++;
        else if (cle == pref) e++;
    }
    cs[t] = s; ce[t] = e;
    __syncthreads();
    if (t == 0) {
        int a = 0, b = 0;
        for (int i = 0; i < 256; i++) { a += cs[i]; b += ce[i]; }
        compte_sup[(size_t)ligne * gridDim.y + tr] = a;
        compte_eq[(size_t)ligne * gridDim.y + tr] = b;
    }
}

extern "C" __global__ void attn_topk_ecrit(const float* __restrict__ sc,
                                           const unsigned int* __restrict__ prefixes,
                                           const int* __restrict__ base_sup,  // [lignes][ntr]
                                           const int* __restrict__ base_eq,
                                           const int* __restrict__ debut_egaux, // [lignes]
                                           const int* __restrict__ besoin,      // [lignes]
                                           int* __restrict__ sortie,            // [lignes][k]
                                           int n, int chunk, int k) {
    __shared__ int cs[256];
    __shared__ int ce[256];
    const int ligne = blockIdx.x;
    const int tr = blockIdx.y;
    const int deb = tr * chunk;
    const int fin = min(n, deb + chunk);
    const unsigned int pref = prefixes[ligne];
    const float* row = sc + (size_t)ligne * n;
    const int t = threadIdx.x;
    const int par = (fin - deb + 255) / 256;
    const int d0 = deb + t * par;
    const int d1 = min(fin, d0 + par);
    int s = 0, e = 0;
    for (int i = d0; i < d1; i++) {
        const unsigned int cle = monotone(row[i]);
        if (cle > pref) s++;
        else if (cle == pref) e++;
    }
    cs[t] = s; ce[t] = e;
    __syncthreads();
    // Balayage exclusif par le fil 0 : 256 additions, une seule fois par bloc.
    if (t == 0) {
        int a = 0, b = 0;
        for (int i = 0; i < 256; i++) {
            const int si = cs[i], ei = ce[i];
            cs[i] = a; ce[i] = b;
            a += si; b += ei;
        }
    }
    __syncthreads();
    const int osup = base_sup[(size_t)ligne * gridDim.y + tr] + cs[t];
    const int oeq = base_eq[(size_t)ligne * gridDim.y + tr] + ce[t];
    const int depart = debut_egaux[ligne];
    const int combien = besoin[ligne];
    int* dst = sortie + (size_t)ligne * k;
    int rs = 0, re = 0;
    for (int i = d0; i < d1; i++) {
        const unsigned int cle = monotone(row[i]);
        if (cle > pref) {
            dst[osup + rs] = i;
            rs++;
        } else if (cle == pref && (oeq + re) < combien) {
            dst[depart + oeq + re] = i;
            re++;
        }
    }
}

// ---------------------------------------------------------------------------
// Noyau 3 : le softmax sur les k clés RETENUES, puis la somme pondérée des V.
// C'est le dernier des trois noyaux du top-k (docs/plan-gpu-topk.md).
//
// Un bloc par LIGNE (tête KV × tête de requête). Les k scores sont rassemblés
// en partagé, les k poids aussi : le max et le dénominateur se calculent donc
// UNE fois par ligne et non une fois par composante. Les puits comptent dans le
// dénominateur (comme partout ailleurs dans le moteur) et pas dans le numérateur.
//
// bits = 8 : valeurs int8 avec une échelle f32 par bloc de 32 canaux ;
// bits = 32 : valeurs f32 telles quelles. `ctx` est la capacité ALLOUÉE — c'est
// le pas entre deux positions du cache, comme dans `attn_kv_partiels`.
// ---------------------------------------------------------------------------

__device__ __forceinline__ float valeur_v(const void* __restrict__ vdata,
                                          const float* __restrict__ vscale,
                                          size_t base, int pos, int d,
                                          int hd, int nb, int bits) {
    const size_t vec = base + (size_t)pos;
    if (bits >= 32) {
        return reinterpret_cast<const float*>(vdata)[vec * (size_t)hd + d];
    }
    const float e = vscale[vec * (size_t)nb + (d >> 5)];
    const signed char* p = reinterpret_cast<const signed char*>(vdata);
    return (float)p[vec * (size_t)hd + d] * e;
}

extern "C" __global__ void attn_topk_somme(const float* __restrict__ sc,
                                           const void* __restrict__ vdata,
                                           const float* __restrict__ vscale,
                                           const int* __restrict__ idx,     // [lignes][k]
                                           const float* __restrict__ sinks, // [lignes] ou nullptr
                                           float* __restrict__ out,         // [lignes][hd]
                                           int n, int ctx, int hd, int nb,
                                           int k, int rep, int bits) {
    extern __shared__ float sh[];
    float* shS = sh;            // les k scores retenus
    float* shW = shS + k;       // leurs k poids exp(s − m)
    float* red = shW + k;       // réductions (blockDim.x cases)
    const int ligne = blockIdx.x;
    const int tid = threadIdx.x;
    const int kvh = ligne / rep;
    const float* sc_l = sc + (size_t)ligne * n;
    const int* ix = idx + (size_t)ligne * k;
    const size_t base = (size_t)kvh * ctx;

    float m = -1e30f;
    for (int j = tid; j < k; j += blockDim.x) {
        const float s = sc_l[ix[j]];
        shS[j] = s;
        m = fmaxf(m, s);
    }
    if (sinks != nullptr) m = fmaxf(m, sinks[ligne]);
    red[tid] = m;
    __syncthreads();
    for (int pas = blockDim.x >> 1; pas > 0; pas >>= 1) {
        if (tid < pas) red[tid] = fmaxf(red[tid], red[tid + pas]);
        __syncthreads();
    }
    m = red[0];
    // Même course que dans le noyau 4 : `red` est réutilisé pour la somme, et un
    // fil rapide pourrait écraser sa case avant que les autres aient lu `red[0]`.
    __syncthreads();
    float somme = 0.0f;
    for (int j = tid; j < k; j += blockDim.x) {
        const float w = expf(shS[j] - m);
        shW[j] = w;
        somme += w;
    }
    // ⚠️ Le puits s'ajoute UNE fois, pas une par fil : chaque fil tient une
    // somme PARTIELLE, et la réduction les additionne. L'ajouter dans la boucle
    // de tous les fils le comptait 256 fois — mesuré : dénominateur ×45,7 et
    // sortie 55× trop petite à k = 1. Le banc l'a dit en une ligne, la
    // relecture ne l'aurait pas vu.
    if (sinks != nullptr && tid == 0) somme += expf(sinks[ligne] - m);
    red[tid] = somme;
    __syncthreads();
    for (int pas = blockDim.x >> 1; pas > 0; pas >>= 1) {
        if (tid < pas) red[tid] += red[tid + pas];
        __syncthreads();
    }
    const float inv = (red[0] > 0.0f) ? 1.0f / red[0] : 0.0f;
    for (int d = tid; d < hd; d += blockDim.x) {
        float acc = 0.0f;
        for (int j = 0; j < k; j++) {
            acc += shW[j] * valeur_v(vdata, vscale, base, ix[j], d, hd, nb, bits);
        }
        out[(size_t)ligne * hd + d] = acc * inv;
    }
}

// ---------------------------------------------------------------------------
// Noyau 4 : TOUT le top-k d'une ligne en UN lancement.
//
// Pourquoi : la chaîne séparée (histogramme ×4, comptage, écriture, somme) coûte
// 8 lancements et 17 transferts par couche et par jeton — mesuré 12 µs par
// opération, soit ~65 % du temps d'attention déportée, ce qui repoussait le
// croisement avec le CPU entre 255 et 2 047 clés. Ici, un bloc par ligne :
//
//   1. quatre passes d'octets de la descente radix, chacune : histogramme de 256
//      seaux EN PARTAGÉ, puis le fil 0 descend les seaux et fixe l'octet du
//      préfixe (aucun aller-retour par l'hôte) ;
//   2. collecte des k indices dans l'ordre déterministe du contrat : ceux
//      strictement au-dessus du seuil, puis les égaux, chacun par indices
//      croissants (plages CONTIGUËS par fil, comme `attn_topk_ecrit`) ;
//   3. softmax sur ces k scores (puits compris au dénominateur) et somme
//      pondérée des V, lus en VRAM par les indices.
//
// Le tampon de scores complet `nh × n × 4` du plan disparaît : les scores ne sont
// lus qu'en VRAM, et les k indices retenus vivent en partagé.
//
// Contrainte de parallélisme, mesurée et assumée : 14 blocs (un par ligne) avec
// 1024 fils. Le travail est une lecture en flux (4 passes + 1 collecte), donc
// borné par la bande passante et non par le nombre d'unités : c'est le banc qui
// tranchera, pas l'intuition.
// ---------------------------------------------------------------------------

extern "C" __global__ void attn_topk_tout(const float* __restrict__ sc,
                                          const void* __restrict__ vdata,
                                          const float* __restrict__ vscale,
                                          const float* __restrict__ sinks,
                                          float* __restrict__ out,   // [lignes][hd]
                                          int n, int ctx, int hd, int nb,
                                          int k, int rep, int bits) {
    extern __shared__ float sh[];
    // Partagé : 256 compteurs, k clés (entier monotone), k indices, k poids,
    // 2 × blockDim réductions. k ≤ 1024.
    unsigned int* shHisto = reinterpret_cast<unsigned int*>(sh);
    unsigned int* shCle   = shHisto + 256;
    int*          shIdx   = reinterpret_cast<int*>(shCle + k);
    float*        shW     = reinterpret_cast<float*>(shIdx + k);
    float*        red     = shW + k;                 // blockDim.x cases
    float*        red2    = red + blockDim.x;        // blockDim.x cases
    const int ligne = blockIdx.x;
    const int tid = threadIdx.x;
    const int kvh = ligne / rep;
    const float* row = sc + (size_t)ligne * n;
    const size_t base = (size_t)kvh * ctx;

    unsigned int pref = 0u;
    int dessus = 0;
    for (int etape = 0; etape < 4; etape++) {
        const int decalage = 24 - 8 * etape;
        for (int i = tid; i < 256; i += blockDim.x) shHisto[i] = 0u;
        __syncthreads();
        for (int i = tid; i < n; i += blockDim.x) {
            const unsigned int cle = monotone(row[i]);
            if (((cle >> decalage) >> 8) == pref)
                atomicAddPartage(&shHisto[(cle >> decalage) & 0xFFu], 1u);
        }
        __syncthreads();
        if (tid == 0) {
            int cum = dessus;
            int b = 256;
            while (b > 0 && cum < k) { b--; cum += (int)shHisto[b]; }
            dessus = cum - (int)shHisto[b];
            pref = (pref << 8) | (unsigned int)b;
            shHisto[0] = pref;      // relu par tous après la barrière
            shHisto[1] = (unsigned int)dessus;
        }
        __syncthreads();
        pref = shHisto[0];
        dessus = (int)shHisto[1];
    }
    const int besoin = k - dessus;      // ≥ 1 par construction

    // ---- collecte : compte par fil sur une plage contiguë, balayage, écriture
    const int par = (n + blockDim.x - 1) / blockDim.x;
    const int d0 = tid * par;
    const int d1 = min(n, d0 + par);
    int nsup = 0, neq = 0;
    for (int i = d0; i < d1; i++) {
        const unsigned int cle = monotone(row[i]);
        if (cle > pref) nsup++;
        else if (cle == pref) neq++;
    }
    red[tid] = (float)nsup;
    red2[tid] = (float)neq;
    __syncthreads();
    if (tid == 0) {
        int a = 0, b = 0;
        for (int i = 0; i < blockDim.x; i++) {
            const int s = (int)red[i], e = (int)red2[i];
            red[i] = (float)a;
            red2[i] = (float)b;
            a += s; b += e;
        }
    }
    __syncthreads();
    const int base_sup = (int)red[tid];
    const int base_eq = (int)red2[tid];
    int rs = 0, re = 0;
    for (int i = d0; i < d1; i++) {
        const float s = row[i];
        const unsigned int cle = monotone(s);
        if (cle > pref) {
            shIdx[base_sup + rs] = i;
            shW[base_sup + rs] = s;
            rs++;
        } else if (cle == pref && (base_eq + re) < besoin) {
            shIdx[dessus + base_eq + re] = i;
            shW[dessus + base_eq + re] = s;
            re++;
        }
    }
    // Poison : si la collecte n'a pas rempli EXACTEMENT les k places (ce que la
    // descente garantit, mais un invariant non vérifié est un invariant qu'on
    // espère), les cases restantes contiendraient de la mémoire partagée
    // quelconque — une sortie plausible et fausse. Un NaN, lui, se voit : l'hôte
    // refuse la sortie non finie et rend la main au CPU.
    red[tid] = (float)(rs + re);
    __syncthreads();
    if (tid == 0) {
        int total = 0;
        for (int i = 0; i < blockDim.x; i++) total += (int)red[i];
        shHisto[2] = (total == k) ? 0u : 1u;
    }
    __syncthreads();
    // ⚠️ Le filet doit AGIR AVANT la somme, pas après : les cases de `shIdx` que
    // la collecte n'a pas remplies contiennent n'importe quoi, et la somme s'en
    // sert pour lire la VRAM — mesuré en sabotant la collecte exprès :
    // CUDA_ERROR_ILLEGAL_ADDRESS (700) et contexte empoisonné, le NaN écrit après
    // coup n'ayant jamais eu l'occasion d'être vu. On sort donc ici, sans somme,
    // avec un NaN que l'hôte refuse.
    if (shHisto[2] != 0u) {
        if (tid == 0) out[(size_t)ligne * hd] = __int_as_float(0x7FC00000);  // NaN
        return;
    }

    // ---- softmax sur ces k scores (indices en partagé, plus de relecture)
    float m = -1e30f;
    for (int j = tid; j < k; j += blockDim.x) m = fmaxf(m, shW[j]);
    if (sinks != nullptr) m = fmaxf(m, sinks[ligne]);
    red[tid] = m;
    __syncthreads();
    for (int pas = blockDim.x >> 1; pas > 0; pas >>= 1) {
        if (tid < pas) red[tid] = fmaxf(red[tid], red[tid + pas]);
        __syncthreads();
    }
    m = red[0];
    // Barrière AVANT de réutiliser `red` : sans elle, un fil assez rapide peut
    // écraser sa case pendant qu'un autre lit encore `red[0]` — la fenêtre est
    // étroite (il faut être désordonnancé pendant toute la boucle de somme), mais
    // elle existe, et une course qui ne se voit pas n'est pas une course absente.
    __syncthreads();
    float somme = 0.0f;
    for (int j = tid; j < k; j += blockDim.x) {
        const float w = expf(shW[j] - m);
        shW[j] = w;
        somme += w;
    }
    if (sinks != nullptr && tid == 0) somme += expf(sinks[ligne] - m);
    red[tid] = somme;
    __syncthreads();
    for (int pas = blockDim.x >> 1; pas > 0; pas >>= 1) {
        if (tid < pas) red[tid] += red[tid + pas];
        __syncthreads();
    }
    const float inv = (red[0] > 0.0f) ? 1.0f / red[0] : 0.0f;
    for (int d = tid; d < hd; d += blockDim.x) {
        float acc = 0.0f;
        for (int j = 0; j < k; j++) {
            acc += shW[j] * valeur_v(vdata, vscale, base, shIdx[j], d, hd, nb, bits);
        }
        out[(size_t)ligne * hd + d] = acc * inv;
    }
}
