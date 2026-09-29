#!/bin/bash
# Compile les noyaux en PTX — la chaîne qui marche sur cette machine.
#
# nvcc refuse gcc 15/16 (conflit d'en-têtes glibc) ; on passe donc par le
# backend NVPTX de clang, et le pilote compile le PTX à la volée. Comme aucun
# en-tête CUDA n'est disponible sans la boîte à outils, les qualificatifs
# (`__global__`, `__shared__`, …) viennent de `cuda_stub.h` — c'est la seule
# pièce à maintenir si les noyaux grossissent.
set -e
cd "$(dirname "$0")"
BUILTINS="$(clang -print-resource-dir)/include/__clang_cuda_builtin_vars.h"
clang++ -x cuda --cuda-device-only --cuda-gpu-arch=sm_75 -nocudalib -nocudainc \
    -O3 -S -include "$BUILTINS" -include cuda_stub.h -o qtrinet_gpu.ptx qtrinet_gpu.cu
echo "qtrinet_gpu.ptx régénéré ($(grep -c '' qtrinet_gpu.ptx) lignes)"
grep -c 'visible .entry' qtrinet_gpu.ptx | xargs echo "noyaux exportés :"
