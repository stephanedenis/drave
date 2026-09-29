// Noyaux GPU de Qtrinet.
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

}  // extern "C"
