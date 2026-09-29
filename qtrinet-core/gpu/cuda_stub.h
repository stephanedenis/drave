// Sans en-têtes CUDA : les qualificatifs sont des attributs clang, et
// `__syncthreads` est un builtin du mode CUDA.
#define __device__ __attribute__((device))
#define __host__ __attribute__((host))
#define __global__ __attribute__((global))
#define __shared__ __attribute__((shared))
#define __constant__ __attribute__((constant))
#define __forceinline__ inline __attribute__((always_inline))
#define __restrict__ __restrict__
// Les identifiants de bloc et de fil viennent de
// `__clang_cuda_builtin_vars.h` (voir compiler.sh) : les redéclarer ici, même
// avec `device_builtin`, entre en conflit. Sans cet en-tête, clang émet
// `ld.global.b32 %r, [threadIdx]` au lieu des registres `%tid.x` — la lecture
// vaut 0, `pas = blockDim.x * gridDim.x` vaut 0, et le noyau boucle à l'infini
// sans le moindre message d'erreur.
static __attribute__((device)) __attribute__((always_inline)) float __int_as_float(int x) {
    return __builtin_bit_cast(float, x);
}
typedef __SIZE_TYPE__ size_t;
typedef unsigned long long uint64_t;

// Aucune bibliothèque CUDA n'est incluse : les fonctions mathématiques des
// noyaux d'attention sont écrites ici. `ex2.approx.f32` est l'instruction du
// matériel pour 2^x — l'erreur relative (~1e-7 sur la mantisse) est du même
// ordre que celle du reste du calcul en simple précision, et c'est ce que
// utilisent les noyaux d'attention écrits à la main.
static __attribute__((device)) __attribute__((always_inline)) float expf(float x) {
    float r;
    asm("ex2.approx.f32 %0, %1;" : "=f"(r) : "f"(x * 1.4426950408889634f));
    return r;
}
static __attribute__((device)) __attribute__((always_inline)) float fmaxf(float a, float b) {
    return a > b ? a : b;
}
static __attribute__((device)) __attribute__((always_inline)) int min(int a, int b) {
    return a < b ? a : b;
}
static __attribute__((device)) __attribute__((always_inline)) void __syncwarp() {
    asm volatile("bar.warp.sync 0xffffffff;" ::: "memory");
}
