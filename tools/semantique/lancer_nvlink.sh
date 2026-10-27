#!/usr/bin/env bash
# Lance les deux rangs du protocole sémantique, un par GPU, avec NCCL sur NVLink.
# torchrun/elastic a refusé de démarrer sur cette machine ; deux rangs explicites
# font la même chose, et les journaux sont lisibles.
set -euo pipefail
RACINE="$(cd "$(dirname "$0")/../.." && pwd)"
PORT="${PORT:-29515}"
LOGS="${LOGS:-/tmp/semantique-nvlink-logs}"
mkdir -p "$LOGS"
export PYTHONPATH="$RACINE/tools"
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-2}"
export MKL_NUM_THREADS="${MKL_NUM_THREADS:-2}"
export NCCL_P2P_LEVEL=NVL
export NCCL_DEBUG="${NCCL_DEBUG:-WARN}"
export MASTER_ADDR=127.0.0.1
export MASTER_PORT="$PORT"
COMMUN="$*"
RANK=0 LOCAL_RANK=0 WORLD_SIZE=2 CUDA_VISIBLE_DEVICES=0 \
  "/home/stephane/gpu-env/bin/python" "$RACINE/tools/semantique/entrainer_nvlink.py" $COMMUN \
  > "$LOGS/rang0.log" 2>&1 &
P0=$!
RANK=1 LOCAL_RANK=0 WORLD_SIZE=2 CUDA_VISIBLE_DEVICES=1 \
  "/home/stephane/gpu-env/bin/python" "$RACINE/tools/semantique/entrainer_nvlink.py" $COMMUN \
  > "$LOGS/rang1.log" 2>&1 &
P1=$!
set +e
wait $P0; E0=$?
wait $P1; E1=$?
set -e
echo "== rang0 =="; tail -20 "$LOGS/rang0.log" || true
echo "== rang1 =="; tail -20 "$LOGS/rang1.log" || true
[ "$E0" -eq 0 ] && [ "$E1" -eq 0 ]
