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
