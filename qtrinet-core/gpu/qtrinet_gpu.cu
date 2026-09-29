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

}  // extern "C"
